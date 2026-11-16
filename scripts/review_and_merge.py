#!/usr/bin/env python3
"""ACU CSE 101 - Student PR Reviewer & Squash Merger.

==================================================
Automatically reviews new student pull requests, verifies that exercises pass
course tests, approves the PR, posts a 'Thank you, good job.' comment, and
squash merges the PR into the student's dedicated branch.

Usage:
    python3 scripts/review_and_merge.py
    python3 scripts/review_and_merge.py --pr 25
    python3 scripts/review_and_merge.py --dry-run
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

try:
    from .course_automation import COURSE_REPOSITORY, GitHub, ensure_student_branch, student_login
except ImportError:
    from course_automation import COURSE_REPOSITORY, GitHub, ensure_student_branch, student_login

# Terminal styling constants
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

DEFAULT_COMMENT = "Thank you, good job."


def run_cmd(cmd: list[str], cwd: str | None = None, check: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command and return CompletedProcess."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def get_gh_token() -> str | None:
    """Resolve GitHub token from environment or gh auth token."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    res = run_cmd(["gh", "auth", "token"])
    if res.returncode == 0 and res.stdout.strip():
        return res.stdout.strip()
    return None


def detect_submission_week(pr: dict) -> str | None:
    """Extract exercise week from head branch name or changed file paths."""
    head_ref = pr.get("headRefName") or pr.get("head", {}).get("ref", "")
    match = re.search(r"(week_\d{2}_[a-z0-9_]+)", head_ref)
    if match:
        return match.group(1)

    # Fallback to inspecting changed files
    files = pr.get("files") or []
    for f in files:
        path = f.get("path") if isinstance(f, dict) else str(f)
        match = re.search(r"exercises/(week_\d{2}_[a-z0-9_]+)/", path)
        if match:
            return match.group(1)
    return None


def check_ci_status(pr: dict) -> bool | None:
    """Check if automated grading CI checks passed on GitHub Actions."""
    checks = pr.get("statusCheckRollup") or []
    for c in checks:
        name = c.get("name") or c.get("workflowName") or ""
        conclusion = (c.get("conclusion") or "").upper()
        if "TA Automated Grading" in name or name == "grade":
            if conclusion == "SUCCESS":
                return True
            if conclusion in ("FAILURE", "TIMED_OUT", "STARTUP_FAILURE"):
                return False
    return None


def verify_submission_locally(repo_dir: str, pr_number: int, week: str, repo: str) -> tuple[bool, str]:
    """Fetch PR files and verify against trusted course test suite."""
    trusted_week_dir = Path(repo_dir) / "exercises" / week
    test_challenge = trusted_week_dir / "test_challenge.py"
    if not test_challenge.is_file():
        return False, f"Trusted test file {test_challenge} does not exist."

    # Fetch PR head into temporary ref
    ref_spec = f"pull/{pr_number}/head"
    fetch_res = run_cmd(["git", "fetch", f"https://github.com/{repo}.git", f"{ref_spec}:refs/remotes/origin/pr/{pr_number}"], cwd=repo_dir)
    if fetch_res.returncode != 0:
        return False, f"Failed to fetch PR #{pr_number}: {fetch_res.stderr.strip()}"

    pr_ref = f"origin/pr/{pr_number}"

    with tempfile.TemporaryDirectory(prefix=f"verify-pr-{pr_number}-") as td:
        temp_dir = Path(td)
        # Copy trusted course exercises directory for that week
        shutil.copytree(trusted_week_dir, temp_dir / "exercises" / week)

        # Copy pytest.ini if present
        if (Path(repo_dir) / "pytest.ini").is_file():
            shutil.copyfile(Path(repo_dir) / "pytest.ini", temp_dir / "pytest.ini")

        # Extract student submission files from PR commit
        for file_name in ("challenge.py", "practice.py"):
            target_path = temp_dir / "exercises" / week / file_name
            cat_res = run_cmd(["git", "show", f"{pr_ref}:exercises/{week}/{file_name}"], cwd=repo_dir)
            if cat_res.returncode == 0 and cat_res.stdout:
                target_path.write_text(cat_res.stdout, encoding="utf-8")

        # Run pytest
        test_target = temp_dir / "exercises" / week / "test_challenge.py"
        test_res = run_cmd([sys.executable, "-m", "pytest", "-v", str(test_target)], cwd=td)
        passed = test_res.returncode == 0
        details = test_res.stdout.strip() or test_res.stderr.strip()
        return passed, details


def route_pr_base(api: GitHub, repo: str, pr_number: int, current_base: str, expected_base: str) -> bool:
    """Ensure PR targets the student's designated branch instead of main."""
    if current_base.lower() == expected_base.lower():
        return True
    try:
        ensure_student_branch(api, repo, expected_base)
        api.request(f"repos/{repo}/pulls/{pr_number}", method="PATCH", data={"base": expected_base})
        print(f"  🔀 Re-routed base branch from '{current_base}' to '{expected_base}'")
        return True
    except Exception as error:
        print(f"  {RED}Failed to re-route base branch to '{expected_base}': {error}{RESET}")
        return False


def approve_pr(repo: str, pr_number: int, message: str) -> bool:
    """Submit an approving review for the pull request."""
    res = run_cmd(["gh", "pr", "review", str(pr_number), "-R", repo, "--approve", "--body", message])
    if res.returncode == 0:
        return True
    # Fallback to direct REST API
    token = get_gh_token()
    if not token:
        return False
    try:
        api = GitHub(token)
        api.request(f"repos/{repo}/pulls/{pr_number}/reviews", method="POST", data={
            "event": "APPROVE",
            "body": message,
        })
        return True
    except Exception as error:
        print(f"  {YELLOW}Warning: could not post review approval: {error}{RESET}")
        return False


def comment_on_pr(repo: str, pr_number: int, comment: str) -> bool:
    """Post comment on the pull request."""
    res = run_cmd(["gh", "pr", "comment", str(pr_number), "-R", repo, "--body", comment])
    if res.returncode == 0:
        return True
    token = get_gh_token()
    if not token:
        return False
    try:
        api = GitHub(token)
        api.request(f"repos/{repo}/issues/{pr_number}/comments", method="POST", data={"body": comment})
        return True
    except Exception as error:
        print(f"  {YELLOW}Warning: could not post comment: {error}{RESET}")
        return False


def squash_merge_pr(repo: str, pr_number: int) -> bool:
    """Squash and merge the pull request."""
    res = run_cmd(["gh", "pr", "merge", str(pr_number), "-R", repo, "--squash", "--admin"])
    if res.returncode == 0:
        return True
    token = get_gh_token()
    if not token:
        return False
    try:
        api = GitHub(token)
        api.request(f"repos/{repo}/pulls/{pr_number}/merge", method="PUT", data={"merge_method": "squash"})
        return True
    except Exception as error:
        print(f"  {RED}Merge error: {error}{RESET}")
        return False


def process_pull_request(
    pr: dict,
    repo_dir: str,
    repo: str,
    token: str,
    dry_run: bool = False,
    comment: str = DEFAULT_COMMENT,
) -> bool:
    """Review, approve, comment, and squash merge a single student PR."""
    pr_number = pr["number"]
    title = pr.get("title", "")
    author = pr.get("author", {}).get("login") or pr.get("user", {}).get("login", "")
    current_base = pr.get("baseRefName") or pr.get("base", {}).get("ref", "")

    print(f"\n{BOLD}{CYAN}------------------------------------------------------------{RESET}")
    print(f"{BOLD}🔍 Processing PR #{pr_number}: {title}{RESET}")
    print(f"  Author: {author} | Base: {current_base}")

    if not author:
        print(f"  {RED}Error: Could not resolve PR author.{RESET}")
        return False

    api = GitHub(token)
    try:
        username = student_login(author)
    except ValueError as e:
        print(f"  {RED}Invalid student login: {e}{RESET}")
        return False

    # 1. Route base branch to student branch
    if not route_pr_base(api, repo, pr_number, current_base, username):
        return False

    # 2. Detect week
    week = detect_submission_week(pr)
    if not week:
        print(f"  {YELLOW}Warning: Could not detect exercise week for PR #{pr_number}. Skipping.{RESET}")
        return False
    print(f"  📅 Detected submission week: {BOLD}{week}{RESET}")

    # 3. Verify tests (CI check or local pytest verification)
    ci_passed = check_ci_status(pr)
    if ci_passed is True:
        print(f"  {GREEN}✓ CI Automated Grading passed on GitHub Actions.{RESET}")
        passed = True
    else:
        print(f"  🧪 Running local test suite against student submission for {week}...")
        passed, details = verify_submission_locally(repo_dir, pr_number, week, repo)
        if passed:
            print(f"  {GREEN}✓ Local test suite passed!{RESET}")
        else:
            print(f"  {RED}❌ Tests failed for {week}:{RESET}")
            for line in details.splitlines()[-10:]:
                print(f"     {line}")
            return False

    if dry_run:
        print(f"  {YELLOW}[Dry Run] Would approve, comment '{comment}', and squash merge PR #{pr_number}.{RESET}")
        return True

    # 4. Approve PR
    review_msg = f"Reviewed: All automated tests for `{week}` passed successfully. Well done!"
    if approve_pr(repo, pr_number, review_msg):
        print(f"  {GREEN}✓ PR #{pr_number} approved.{RESET}")
    else:
        print(f"  {YELLOW}Notice: PR #{pr_number} approval skipped or already approved.{RESET}")

    # 5. Comment on PR
    if comment_on_pr(repo, pr_number, comment):
        print(f"  {GREEN}✓ Posted comment: \"{comment}\"{RESET}")

    # 6. Squash merge
    if squash_merge_pr(repo, pr_number):
        print(f"  {GREEN}{BOLD}🎉 Successfully squashed and merged PR #{pr_number} into '{username}'!{RESET}")
        return True
    else:
        print(f"  {RED}❌ Failed to squash merge PR #{pr_number}.{RESET}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="ACU CSE 101 - Review, approve, comment, and squash merge student PRs."
    )
    parser.add_argument("--repo", default=COURSE_REPOSITORY, help="GitHub repository (owner/name)")
    parser.add_argument("--pr", type=int, help="Specific PR number to process")
    parser.add_argument("--comment", default=DEFAULT_COMMENT, help="Comment to leave on merged PR")
    parser.add_argument("--limit", type=int, default=200, help="Max number of PRs to process (default: 200)")
    parser.add_argument("--dry-run", action="store_true", help="Inspect and test without approving or merging")
    args = parser.parse_args()

    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    token = get_gh_token()
    if not token:
        print(f"{RED}Error: GitHub token required. Please login with 'gh auth login' or export GH_TOKEN.{RESET}", file=sys.stderr)
        return 1

    api = GitHub(token)

    if args.pr:
        pr = api.request(f"repos/{args.repo}/pulls/{args.pr}")
        prs = [pr]
    else:
        # Fetch all open PRs using gh cli for complete fields (like statusCheckRollup)
        gh_res = run_cmd([
            "gh", "pr", "list", "-R", args.repo, "--state", "open", "--limit", str(args.limit),
            "--json", "number,title,author,headRefName,baseRefName,files,statusCheckRollup,mergeable"
        ], cwd=repo_dir)
        if gh_res.returncode == 0 and gh_res.stdout.strip():
            prs = json.loads(gh_res.stdout)
        else:
            prs = list(api.pages(f"repos/{args.repo}/pulls?state=open"))

    if not prs:
        print(f"\n{GREEN}No open pull requests found in {args.repo}.{RESET}\n")
        return 0

    print(f"\n{BOLD}Found {len(prs)} open pull request(s) in {args.repo}.{RESET}")
    success_count = 0
    fail_count = 0

    for pr in prs:
        ok = process_pull_request(pr, repo_dir, args.repo, token, dry_run=args.dry_run, comment=args.comment)
        if ok:
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{BOLD}=== Summary ==={RESET}")
    print(f"{GREEN}Merged / Verified: {success_count}{RESET}")
    if fail_count > 0:
        print(f"{RED}Failed / Skipped: {fail_count}{RESET}")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
