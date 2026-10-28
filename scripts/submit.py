#!/usr/bin/env python3
"""ACU CSE 101 - Student Practice Submission Launcher.

===================================================
Runs local test suites and prepares a clean submission branch and Pull Request
to the upstream course repository.

Usage:
    python3 scripts/submit.py
    python3 scripts/submit.py --week week_01_intro
    python3 scripts/submit.py --test-only
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

try:
    from .course_automation import COURSE_REPOSITORY, student_login
    from .sync_course import checked_git, switch_to_workspace, workspace_lock
except ImportError:
    from course_automation import COURSE_REPOSITORY, student_login
    from sync_course import checked_git, switch_to_workspace, workspace_lock

# Terminal styling constants
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_available_weeks(repo_dir: str) -> list[str]:
    """Discover all exercise week folders."""
    exercises_dir = os.path.join(repo_dir, "exercises")
    if not os.path.isdir(exercises_dir):
        return []
    weeks = [
        os.path.basename(d)
        for d in sorted(glob.glob(os.path.join(exercises_dir, "week_*")))
        if os.path.isdir(d)
    ]
    return weeks


def detect_target_week(
    repo_dir: str, requested_week: str | None = None, file_path: str | None = None
) -> str:
    """Smart exercise auto-detection so students never need to type in the terminal."""
    available = get_available_weeks(repo_dir)
    if not available:
        print(
            f"{RED}Error: No week directories found in exercises/{RESET}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Explicit requested week
    if requested_week:
        for w in available:
            if requested_week == w or requested_week in w:
                return w
        print(
            f"{RED}Error: Week '{requested_week}' not found in {available}{RESET}",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. File path passed (e.g. from VS Code active file)
    if file_path:
        norm = os.path.normpath(file_path).replace("\\", "/")
        for w in available:
            if f"exercises/{w}" in norm:
                print(f"🎯 Auto-detected active exercise from open file: {CYAN}{BOLD}{w}{RESET}")
                return w

    # 3. Check uncommitted changes in exercises/
    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain", "exercises/"],
            cwd=repo_dir, capture_output=True, text=True, check=False,
        )
        if status_res.returncode == 0 and status_res.stdout.strip():
            modified = {
                w for w in available
                if any(f"exercises/{w}" in line.replace("\\", "/") for line in status_res.stdout.splitlines())
            }
            if len(modified) == 1:
                w = next(iter(modified))
                print(f"🎯 Auto-detected active exercise from modified files: {CYAN}{BOLD}{w}{RESET}")
                return w
    except OSError:
        pass

    # 4. Check filesystem modification timestamps of python files
    newest_week = None
    newest_mtime = -1.0
    for w in available:
        w_dir = os.path.join(repo_dir, "exercises", w)
        if os.path.isdir(w_dir):
            for root, _, files in os.walk(w_dir):
                if "__pycache__" in root:
                    continue
                for fname in files:
                    if fname.endswith(".py") and not fname.startswith("test_"):
                        fpath = os.path.join(root, fname)
                        try:
                            mtime = os.path.getmtime(fpath)
                            if mtime > newest_mtime:
                                newest_mtime = mtime
                                newest_week = w
                        except OSError:
                            pass

    if newest_week:
        print(f"🎯 Auto-detected active exercise from recent edits: {CYAN}{BOLD}{newest_week}{RESET}")
        return newest_week

    # 5. Default without blocking
    if len(available) == 1:
        return available[0]

    # If running interactively with a real TTY, give a quick prompt
    if sys.stdin.isatty():
        print(f"\n{BOLD}{CYAN}=== Select Week to Test / Submit ==={RESET}")
        for idx, w in enumerate(available, 1):
            print(f"  [{idx}] {w}")
        try:
            choice = input(f"\nEnter choice [1-{len(available)}] (default 1): ").strip()
            if not choice:
                return available[0]
            val = int(choice)
            if 1 <= val <= len(available):
                return available[val - 1]
        except (ValueError, KeyboardInterrupt):
            pass

    print(f"🎯 Defaulting to: {CYAN}{BOLD}{available[0]}{RESET}")
    return available[0]


select_week = detect_target_week


def run_tests(repo_dir: str, week: str) -> bool:
    """Executes pytest for the specified week's challenge test suite."""
    week_dir = os.path.join("exercises", week)
    full_path = os.path.join(repo_dir, week_dir)

    if not os.path.isdir(full_path):
        print(
            f"{RED}Error: Week directory not found: {week_dir}{RESET}",
            file=sys.stderr,
        )
        return False

    challenge_test = os.path.join(week_dir, "test_challenge.py")
    if os.path.isfile(os.path.join(repo_dir, challenge_test)):
        target = challenge_test
        print(
            f"\n{BOLD}{CYAN}🧪 Running Automated Graded Challenge Tests ({challenge_test})...{RESET}\n"
        )
    else:
        target = week_dir
        print(f"\n{BOLD}{CYAN}🧪 Running Automated Tests for {week}...{RESET}\n")

    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", target],
        cwd=repo_dir,
        check=False,
    )
    return res.returncode == 0


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


def python_gh_api(repo_dir: str, args: list[str], body: str | None = None) -> str:
    """Python REST API fallback when GitHub CLI (gh) is not installed."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    # 1. repo view <origin> --json nameWithOwner,owner,parent,isFork
    if len(args) >= 2 and args[0] == "repo" and args[1] == "view":
        origin = args[2]
        slug = origin.replace(".git", "").strip()
        if "github.com/" in slug:
            slug = slug.split("github.com/")[-1]
        elif "github.com:" in slug:
            slug = slug.split("github.com:")[-1]
        parts = [p for p in slug.split("/") if p]
        if len(parts) >= 2:
            owner, name = parts[0], parts[1]
        else:
            owner, name = COURSE_REPOSITORY.split("/")
        url = f"https://api.github.com/repos/{owner}/{name}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ACU-CSE-101",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                parent = data.get("parent") or {}
                return json.dumps({
                    "nameWithOwner": data.get("full_name", f"{owner}/{name}"),
                    "owner": {"login": data.get("owner", {}).get("login", owner)},
                    "parent": {
                        "owner": {"login": parent.get("owner", {}).get("login", "")},
                        "name": parent.get("name", ""),
                    } if parent else None,
                    "isFork": data.get("fork", False),
                })
        except urllib.error.HTTPError as error:
            raise RuntimeError(f"Unable to access repository '{owner}/{name}': HTTP {error.code}") from error
        except Exception as error:
            raise RuntimeError(f"Unable to query repository information from GitHub: {error}") from error

    # 2. api <path>
    if args and args[0] == "api":
        path = args[1].lstrip("/")
        method = "GET"
        params = {}
        idx = 2
        while idx < len(args):
            if args[idx] == "--method" and idx + 1 < len(args):
                method = args[idx + 1].upper()
                idx += 2
            elif args[idx] == "-f" and idx + 1 < len(args):
                key, val = args[idx + 1].split("=", 1)
                params[key] = val
                idx += 2
            else:
                idx += 1
        query = ("?" + urllib.parse.urlencode(params)) if (method == "GET" and params) else ""
        url = f"https://api.github.com/{path}{query}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ACU-CSE-101",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data_bytes = json.dumps(params).encode() if (method != "GET" and params) else None
        req = urllib.request.Request(url, data=data_bytes, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode().strip()
        except urllib.error.HTTPError as error:
            if error.code == 404:
                raise RuntimeError(f"Resource not found: {path}") from error
            raise RuntimeError(f"GitHub API error {error.code}: {error.reason}") from error
        except Exception as error:
            raise RuntimeError(f"GitHub API request failed: {error}") from error

    # 3. pr create
    if len(args) >= 2 and args[0] == "pr" and args[1] == "create":
        repo = COURSE_REPOSITORY
        head = ""
        base = "main"
        title = ""
        body_content = body or ""
        idx = 2
        while idx < len(args):
            if args[idx] == "--repo" and idx + 1 < len(args):
                repo = args[idx + 1]
                idx += 2
            elif args[idx] == "--head" and idx + 1 < len(args):
                head = args[idx + 1]
                idx += 2
            elif args[idx] == "--base" and idx + 1 < len(args):
                base = args[idx + 1]
                idx += 2
            elif args[idx] == "--title" and idx + 1 < len(args):
                title = args[idx + 1]
                idx += 2
            elif args[idx] == "--body-file" and idx + 1 < len(args):
                with open(args[idx + 1], "r", encoding="utf-8") as bf:
                    body_content = bf.read()
                idx += 2
            else:
                idx += 1
        if not token:
            raise RuntimeError(
                "GitHub authentication required to submit. Please ensure GITHUB_TOKEN is available or install GitHub CLI (gh)."
            )
        url = f"https://api.github.com/repos/{repo}/pulls"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ACU-CSE-101",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        payload = json.dumps({"title": title, "head": head, "base": base, "body": body_content}).encode()
        req = urllib.request.Request(url, data=payload, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                return data.get("html_url", "")
        except urllib.error.HTTPError as error:
            err_body = error.read().decode()
            raise RuntimeError(f"Failed to create PR ({error.code}): {err_body}") from error
        except Exception as error:
            raise RuntimeError(f"Failed to create PR: {error}") from error

    # 4. pr edit
    if len(args) >= 3 and args[0] == "pr" and args[1] == "edit":
        pr_number = args[2]
        repo = COURSE_REPOSITORY
        base = None
        idx = 3
        while idx < len(args):
            if args[idx] == "--repo" and idx + 1 < len(args):
                repo = args[idx + 1]
                idx += 2
            elif args[idx] == "--base" and idx + 1 < len(args):
                base = args[idx + 1]
                idx += 2
            else:
                idx += 1
        if not token:
            raise RuntimeError("Authentication required to edit Pull Request.")
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ACU-CSE-101",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        payload = json.dumps({"base": base}).encode() if base else None
        req = urllib.request.Request(url, data=payload, method="PATCH", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                return data.get("html_url", "")
        except Exception as error:
            raise RuntimeError(f"Failed to edit PR: {error}") from error

    raise RuntimeError(f"Unsupported gh command: {args}")


def run_gh(repo_dir: str, args: list[str], body: str | None = None) -> str:
    """Execute gh command, falling back to direct Python GitHub API when gh is missing."""
    gh_bin = shutil.which("gh")
    if not gh_bin:
        for candidate in ("/usr/bin/gh", "/usr/local/bin/gh", "/home/vscode/.local/bin/gh"):
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                gh_bin = candidate
                break

    if gh_bin:
        try:
            result = subprocess.run(
                [gh_bin, *args], cwd=repo_dir, input=body, capture_output=True,
                text=True, check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            # If gh fails with missing token or not logged in, try Python fallback if token exists
            if "authentication" in (result.stderr.lower() + result.stdout.lower()):
                return python_gh_api(repo_dir, args, body)
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        except (OSError, RuntimeError) as error:
            # Fall back to Python API if possible
            try:
                return python_gh_api(repo_dir, args, body)
            except Exception:
                raise error from None

    return python_gh_api(repo_dir, args, body)


def ensure_git_identity(repo_dir: str):
    """Ensure git user name and email are configured to avoid author errors."""
    try:
        res = subprocess.run(
            ["git", "config", "user.name"],
            cwd=repo_dir, capture_output=True, text=True, check=False,
        )
        if not res.stdout.strip():
            subprocess.run(["git", "config", "user.name", "CSE 101 Student"], cwd=repo_dir, check=False)
            subprocess.run(["git", "config", "user.email", "student@cse101.acibadam.edu.tr"], cwd=repo_dir, check=False)
    except OSError:
        pass


def ensure_committed(repo_dir: str):
    """Save exercise edits without resetting the persistent workspace branch."""
    ensure_git_identity(repo_dir)
    switch_to_workspace(repo_dir)
    checked_git(["add", "exercises/"], repo_dir)
    status = checked_git(["status", "--porcelain", "exercises/"], repo_dir)
    if status.stdout.strip():
        checked_git(["commit", "-m", "Pre-submission snapshot", "--", "exercises/"], repo_dir)


def handle_submission(repo_dir: str, week: str):
    """Submit this week's files to the student's persistent course branch."""
    ensure_git_identity(repo_dir)
    with workspace_lock(repo_dir):
        _submit(repo_dir, week)


def _submit(repo_dir: str, week: str):
    if week not in get_available_weeks(repo_dir):
        raise RuntimeError("Unknown exercise week.")
    # Resolve the actual fork owner, never a guessed Git identity or local branch.
    origin = checked_git(["remote", "get-url", "origin"], repo_dir).stdout.strip()
    fork = json.loads(run_gh(repo_dir, ["repo", "view", origin, "--json", "nameWithOwner,owner,parent,isFork"]))
    parent = fork.get("parent") or {}
    if not fork.get("isFork") or f"{parent.get('owner', {}).get('login', '')}/{parent.get('name', '')}".lower() != COURSE_REPOSITORY.lower():
        raise RuntimeError("Submit from your personal fork of the course repository.")
    username = student_login(fork["owner"]["login"])

    # Target the student's branch; if not yet provisioned upstream, target main so pull_request_target provisions it
    target_base = username
    try:
        run_gh(repo_dir, ["api", f"repos/{COURSE_REPOSITORY}/git/ref/heads/{username}"])
    except RuntimeError:
        target_base = "main"

    ensure_committed(repo_dir)
    original_branch = get_current_branch(repo_dir)
    source = checked_git(["rev-parse", "HEAD"], repo_dir).stdout.strip()
    branch_name = f"submit/{week}"
    print(f"Preparing {username}:{branch_name} → {COURSE_REPOSITORY}:{target_base}")
    checked_git(["fetch", "origin", "+refs/heads/*:refs/remotes/origin/*"], repo_dir)
    if target_base == username:
        checked_git(["fetch", f"https://github.com/{COURSE_REPOSITORY}.git", f"refs/heads/{username}"], repo_dir)
    else:
        checked_git(["fetch", f"https://github.com/{COURSE_REPOSITORY}.git", "refs/heads/main"], repo_dir)

    try:
        checked_git(["checkout", "-B", branch_name, "FETCH_HEAD"], repo_dir)
        # Base each submission on the instructor's retained work; include only this week.
        checked_git(["restore", f"--source={source}", "--staged", "--worktree", "--", f"exercises/{week}"], repo_dir)
        changed = checked_git(["diff", "--cached", "--name-only"], repo_dir).stdout.strip()
        if not changed:
            print("This week's files already match your course branch; nothing new to submit.")
            return
        checked_git(["commit", "-m", f"Submission: {week}"], repo_dir)
        checked_git(["push", "--force-with-lease", "origin", f"HEAD:refs/heads/{branch_name}"], repo_dir)
        existing = json.loads(run_gh(repo_dir, [
            "api", "--method", "GET", f"repos/{COURSE_REPOSITORY}/pulls",
            "-f", "state=open", "-f", f"head={username}:{branch_name}",
        ]))
        if existing:
            pr = existing[0]
            if pr["base"]["ref"] != target_base and target_base == username:
                run_gh(repo_dir, ["pr", "edit", str(pr["number"]), "--repo", COURSE_REPOSITORY, "--base", username])
            print(f"Submission updated: {pr['html_url']}")
            return
        body = f"Automated submission for `{week}`.\n\nLocal challenge tests passed. Merge into `{username}` to retain this student's work.\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md") as body_file:
            body_file.write(body)
            body_file.flush()
            url = run_gh(repo_dir, [
                "pr", "create", "--repo", COURSE_REPOSITORY,
                "--head", f"{username}:{branch_name}", "--base", target_base,
                "--title", f"Submission: {week} ({username})", "--body-file", body_file.name,
            ])
        print(f"Submission successful: {url}")
    finally:
        checked_git(["checkout", original_branch], repo_dir)


def main():
    parser = argparse.ArgumentParser(
        description="ACU CSE 101 - Test Runner & Submission Launcher"
    )
    parser.add_argument(
        "--week",
        help="Target week to test/submit (e.g., 'week_01_intro')",
    )
    parser.add_argument(
        "--file",
        help="Active exercise file path (for auto-detecting the week)",
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only run tests without creating a submission branch",
    )

    args = parser.parse_args()
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    target_week = detect_target_week(repo_dir, args.week, args.file)
    passed = run_tests(repo_dir, target_week)

    if not passed:
        print(f"\n{RED}{BOLD}❌ Some tests failed.{RESET}")
        print(
            f"{YELLOW}Please review the test failures above, fix your code, and run submission again.{RESET}\n"
        )
        sys.exit(1)

    print(f"\n{GREEN}{BOLD}✅ All tests for {target_week} PASSED!{RESET}")

    if args.test_only:
        print("Test run completed.")
        sys.exit(0)

    try:
        handle_submission(repo_dir, target_week)
    except (RuntimeError, ValueError) as error:
        print(f"{RED}Submission could not finish:{RESET} {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
