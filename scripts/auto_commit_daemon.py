#!/usr/bin/env python3
"""ACU CSE 101 - Background Auto-Commit Watcher Daemon.

=====================================================
Monitors the exercises/ directory and automatically creates git commits
whenever students edit and save their code, removing the need for manual
git commands.
"""

import datetime
import fcntl
import os
import subprocess
import sys
import time

try:
    from .sync_course import workspace_lock
except ImportError:
    from sync_course import workspace_lock

WATCH_INTERVAL_SECONDS = 3.0
COURSE_SYNC_INTERVAL_SECONDS = 300.0


def is_git_repo(repo_dir: str) -> bool:
    """Check if the directory is a valid git repository."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        return res.returncode == 0 and res.stdout.strip() == "true"
    except OSError:
        return False


def get_git_status(repo_dir: str) -> list[str]:
    """Return a list of changed/untracked files in the repository."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain", "exercises/"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode != 0:
            return []
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        return lines
    except OSError:
        return []


def get_current_branch(repo_dir: str) -> str:
    """Return the name of the currently checked out git branch."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        return res.stdout.strip() or "main"
    except OSError:
        return "main"


def log_message(repo_dir: str, message: str, verbose: bool = False):
    """Log to .git/auto_commit.log silently, and to stdout only if verbose."""
    log_dir = os.path.join(repo_dir, ".git")
    if os.path.isdir(log_dir):
        log_file = os.path.join(log_dir, "auto_commit.log")
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                now_str = (
                    datetime.datetime.now(datetime.timezone.utc)
                    .astimezone()
                    .strftime("%Y-%m-%d %H:%M:%S")
                )
                f.write(f"[{now_str}] {message}\n")
        except OSError:
            pass
    if verbose:
        print(message)


def perform_auto_commit(
    repo_dir: str, changed_lines: list[str], verbose: bool = False
) -> bool:
    """Stages and commits changes in exercises/ to the workspace branch silently."""
    try:
        # Protect 'main' branch - ensure student work is always on 'workspace'
        curr_branch = get_current_branch(repo_dir)
        if curr_branch == "main":
            subprocess.run(
                ["git", "checkout", "workspace"] if subprocess.run(
                    ["git", "show-ref", "--verify", "--quiet", "refs/heads/workspace"],
                    cwd=repo_dir, capture_output=True, check=False,
                ).returncode == 0 else ["git", "checkout", "-b", "workspace"],
                cwd=repo_dir,
                capture_output=True,
                check=False,
            )
            log_message(
                repo_dir,
                "Switched from 'main' to 'workspace' branch to keep main clean.",
                verbose,
            )

        # 1. Stage exercises/
        subprocess.run(
            ["git", "add", "exercises/"],
            cwd=repo_dir,
            capture_output=True,
            check=False,
        )

        # 2. Extract changed file names for commit message
        file_names = []
        for line in changed_lines:
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                file_names.append(os.path.basename(parts[1]))

        summary = ", ".join(file_names[:3])
        if len(file_names) > 3:
            summary += f" and {len(file_names) - 3} more"

        now_str = (
            datetime.datetime.now(datetime.timezone.utc)
            .astimezone()
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        commit_msg = f"Auto-save: {summary} ({now_str})"

        # 3. Commit
        res = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            log_message(repo_dir, f"Auto-saved: {summary}", verbose)
            # 4. Push to student's fork (origin/workspace) so work is always publicly available
            push_res = subprocess.run(
                ["git", "push", "origin", f"HEAD:refs/heads/{curr_branch}"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            if push_res.returncode == 0:
                log_message(repo_dir, f"Auto-pushed {summary} to origin/{curr_branch}", verbose)
            else:
                log_message(repo_dir, f"Auto-push will retry later: {push_res.stderr.strip()}", verbose)
        return res.returncode == 0
    except OSError:
        return False


def synchronize_course(repo_dir: str, verbose: bool = False) -> bool:
    """Load the latest sync script each time; retry failures on the next interval."""
    result = subprocess.run(
        [sys.executable, os.path.join(repo_dir, "scripts", "sync_course.py")],
        cwd=repo_dir, capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        log_message(repo_dir, f"Course sync will retry: {result.stdout.strip()} {result.stderr.strip()}", verbose)
        return False
    log_message(repo_dir, "Course materials synchronized automatically.", verbose)
    return True


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Only one watcher should own this repository after repeated starts.
    git_dir_result = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=repo_dir,
        capture_output=True, text=True, check=False,
    )
    if git_dir_result.returncode != 0:
        return
    with open(os.path.join(git_dir_result.stdout.strip(), "course-daemon.lock"), "a") as daemon_lock:
        try:
            fcntl.flock(daemon_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        watch_workspace(repo_dir, verbose)


def watch_workspace(repo_dir: str, verbose: bool):

    # If git user is not configured, set default course identity
    try:
        name_check = subprocess.run(
            ["git", "config", "user.name"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if not name_check.stdout.strip():
            subprocess.run(
                ["git", "config", "user.name", "CSE 101 Student"],
                cwd=repo_dir,
                check=False,
            )
            subprocess.run(
                ["git", "config", "user.email", "student@cse101.acibadam.edu.tr"],
                cwd=repo_dir,
                check=False,
            )
    except OSError:
        pass

    log_message(repo_dir, "Auto-commit daemon started.", verbose)

    next_course_sync = 0.0
    while True:
        try:
            if is_git_repo(repo_dir):
                if time.monotonic() >= next_course_sync:
                    synchronize_course(repo_dir, verbose)
                    next_course_sync = time.monotonic() + COURSE_SYNC_INTERVAL_SECONDS
                changed = get_git_status(repo_dir)
                if changed:
                    with workspace_lock(repo_dir):
                        perform_auto_commit(repo_dir, changed, verbose=verbose)
            time.sleep(WATCH_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            log_message(repo_dir, "Auto-commit daemon stopped.", verbose)
            sys.exit(0)
        except (OSError, RuntimeError) as error:
            log_message(repo_dir, f"Background operation will retry: {error}", verbose)
            time.sleep(WATCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
