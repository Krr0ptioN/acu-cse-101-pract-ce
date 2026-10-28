#!/usr/bin/env python3
"""ACU CSE 101 - Smart Course Material Sync Tool.

==============================================
Synchronizes the student workspace with newly published course challenges and
workshops from the upstream course repository without merge conflicts:

1. Auto-saves all current student work to the 'workspace' branch.
2. Ensures student changes are NEVER committed or pushed to 'main'.
3. Fetches newly released weekly folders from upstream/main.
4. Updates local 'main' from the canonical course repository and merges it into
   'workspace'.
5. Pushes the updated student workspace to the student's GitHub fork (origin).

Usage:
    python3 scripts/sync_course.py
"""

import fcntl
import os
import subprocess
import sys
from contextlib import contextmanager

# Terminal styling constants
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

DEFAULT_UPSTREAM_URL = os.environ.get(
    "COURSE_UPSTREAM_URL", "https://github.com/Krr0ptioN/acu-cse-101-pract-ce.git"
)
STUDENT_WORK_BRANCH = "workspace"


@contextmanager
def workspace_lock(repo_dir: str):
    """Serialize background saves and syncs within a workspace."""
    git_dir = checked_git(["rev-parse", "--absolute-git-dir"], repo_dir).stdout.strip()
    with open(os.path.join(git_dir, "course-workspace.lock"), "a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another course operation is running; synchronization will retry.")
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def run_git(cmd: list[str], cwd: str) -> subprocess.CompletedProcess:
    """Run a git command and return the completed process."""
    return subprocess.run(
        ["git"] + cmd, cwd=cwd, capture_output=True, text=True, check=False
    )


def checked_git(cmd: list[str], repo_dir: str) -> subprocess.CompletedProcess:
    """Stop synchronization when a Git operation fails."""
    result = run_git(cmd, repo_dir)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Git operation failed.")
    return result


def get_current_branch(repo_dir: str) -> str:
    """Return the name of the currently checked out git branch."""
    res = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_dir)
    return res.stdout.strip() or "main"


def ensure_upstream_remote(repo_dir: str):
    """Ensure the upstream course remote is configured."""
    remote_res = run_git(["remote", "get-url", "upstream"], repo_dir)
    if remote_res.returncode != 0:
        print(f"🔧 Configuring upstream remote: {CYAN}{DEFAULT_UPSTREAM_URL}{RESET}")
        checked_git(["remote", "add", "upstream", DEFAULT_UPSTREAM_URL], repo_dir)
    elif remote_res.stdout.strip() != DEFAULT_UPSTREAM_URL:
        print(f"🔧 Updating course remote: {CYAN}{DEFAULT_UPSTREAM_URL}{RESET}")
        checked_git(["remote", "set-url", "upstream", DEFAULT_UPSTREAM_URL], repo_dir)


def switch_to_workspace(repo_dir: str) -> str:
    """Switch to the persistent student branch without resetting it."""
    current_branch = get_current_branch(repo_dir)
    if current_branch != "main":
        return current_branch

    workspace_exists = run_git(
        ["show-ref", "--verify", "--quiet", f"refs/heads/{STUDENT_WORK_BRANCH}"],
        repo_dir,
    ).returncode == 0
    command = ["checkout", STUDENT_WORK_BRANCH] if workspace_exists else ["checkout", "-b", STUDENT_WORK_BRANCH]
    checkout_res = run_git(command, repo_dir)
    if checkout_res.returncode != 0:
        raise RuntimeError(checkout_res.stderr.strip() or "Unable to open the student workspace.")
    return STUDENT_WORK_BRANCH


def ensure_git_identity(repo_dir: str):
    """Ensure git user.name and user.email are set to prevent commit failures."""
    try:
        name_check = run_git(["config", "user.name"], repo_dir)
        if not name_check.stdout.strip():
            run_git(["config", "user.name", "CSE 101 Student"], repo_dir)
            run_git(["config", "user.email", "student@cse101.acibadam.edu.tr"], repo_dir)
    except OSError:
        pass


def sync_course(repo_dir: str):
    print(
        f"\n{BOLD}{CYAN}=== 🔄 ACU CSE 101: Syncing Weekly Course Materials ==={RESET}\n"
    )

    ensure_git_identity(repo_dir)
    ensure_upstream_remote(repo_dir)

    # 1. Ensure student work is in 'workspace', not 'main', before auto-saving.
    curr_branch = switch_to_workspace(repo_dir)

    # Auto-save any uncommitted work first
    checked_git(["add", "exercises/"], repo_dir)
    status_res = checked_git(["status", "--porcelain", "exercises/"], repo_dir)
    if status_res.stdout.strip():
        print("💾 Auto-saving current work before synchronization...")
        checked_git(["commit", "-m", "Auto-save before course sync", "--", "exercises/"], repo_dir)

    # 2. Fetch the latest released weekly modules from upstream main
    print("📡 Checking for newly released challenges and workshops from upstream...")
    # Codespaces may use shallow clones; recover ancestry before merging.
    fetch_command = ["fetch"]
    if checked_git(["rev-parse", "--is-shallow-repository"], repo_dir).stdout.strip() == "true":
        fetch_command.append("--unshallow")
    # Explicitly update the tracking ref even in single-branch student clones.
    fetch_command.extend(["upstream", "+refs/heads/main:refs/remotes/upstream/main"])
    checked_git(fetch_command, repo_dir)

    # 3. Update local main without checking it out.
    checked_git(["branch", "-f", "main", "upstream/main"], repo_dir)

    # 4. Merge new weekly folders from main into the student's working branch
    print(f"📦 Merging newly published course challenges into '{curr_branch}'...")
    # Prefer student edits when course updates overlap their completed answers.
    merge_res = run_git(
        ["merge", "-X", "ours", "main", "-m", "Sync: pull newly published course exercises"],
        repo_dir,
    )
    if merge_res.returncode != 0:
        abort_res = run_git(["merge", "--abort"], repo_dir)
        detail = merge_res.stderr.strip() or merge_res.stdout.strip()
        if abort_res.returncode != 0:
            detail += "\nPlease ask your TA to help resolve the merge state."
        raise RuntimeError(detail)

    # The scheduled action may have advanced the fork while this Codespace ran.
    # Incorporate that history before backing up, without dropping local answers.
    checked_git(["fetch", "origin", "+refs/heads/*:refs/remotes/origin/*"], repo_dir)
    remote_ref = f"refs/remotes/origin/{curr_branch}"
    if run_git(["show-ref", "--verify", "--quiet", remote_ref], repo_dir).returncode == 0:
        remote_merge = run_git(
            ["merge", "-X", "ours", remote_ref, "-m", "Sync fork workspace history"], repo_dir
        )
        if remote_merge.returncode != 0:
            run_git(["merge", "--abort"], repo_dir)
            raise RuntimeError(remote_merge.stderr.strip() or remote_merge.stdout.strip())

    print(f"\n{GREEN}{BOLD}🎉 Your local workspace is fully up to date.{RESET}")
    print(f"Newly published challenges are available on '{curr_branch}'.")

    # 5. Push only the student's workspace. The canonical course main remains
    # the source of future updates and is never overwritten in the student's fork.
    print("\n☁️ Backing up your workspace to your GitHub fork...")
    checked_git(["push", "origin", f"HEAD:refs/heads/{curr_branch}"], repo_dir)
    print("✅ Fork synchronized.\n")

    # First sync also activates the recurring workflow in the student's fork.
    # Load the newly synced helper from disk, even in an older watcher process.
    helper = os.path.join(repo_dir, "scripts", "enable_fork_sync.py")
    if os.path.isfile(helper):
        try:
            setup = subprocess.run(
                [sys.executable, helper], cwd=repo_dir, capture_output=True, text=True, check=False
            )
            if setup.returncode:
                print("ℹ️ Note: Automatic scheduled workflow could not be registered yet. Local sync succeeded.")
            else:
                print("📅 Automatic updates enabled: Mondays at 14:30 Istanbul time.")
        except OSError:
            pass


def main():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    try:
        with workspace_lock(repo_dir):
            sync_course(repo_dir)
    except RuntimeError as error:
        print(f"{RED}Course sync could not finish:{RESET} {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
