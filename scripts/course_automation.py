"""Synchronize course forks and provision persistent student submission branches.

Runs only trusted Git operations and GitHub API calls, never student programs.
"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

COURSE_REPOSITORY = "Krr0ptioN/acu-cse-101-pract-ce"


class GitHub:
    def __init__(self, token):
        self.token = token

    def request(self, path, method="GET", data=None):
        request = Request(
            f"https://api.github.com/{path}",
            data=json.dumps(data).encode() if data is not None else None,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urlopen(request, timeout=60) as response:
            body = response.read()
            return json.loads(body) if body else {}

    def pages(self, path):
        separator = "&" if "?" in path else "?"
        page = 1
        while True:
            items = self.request(f"{path}{separator}per_page=100&page={page}")
            yield from items
            if len(items) < 100:
                break
            page += 1


def student_login(login):
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", login):
        raise ValueError("Invalid student GitHub username.")
    if login.lower() in {"main", "workspace", "gh-pages"}:
        raise ValueError(f"Username {login} conflicts with a reserved course branch.")
    return login


def ensure_student_branch(api, course, login):
    """Create from course main once; never move an existing student branch."""
    login = student_login(login)
    path = f"repos/{course}/git/ref/heads/{login}"
    try:
        return api.request(path)["object"]["sha"]
    except HTTPError as error:
        if error.code != 404:
            raise
    sha = api.request(f"repos/{course}/git/ref/heads/main")["object"]["sha"]
    try:
        api.request(f"repos/{course}/git/refs", "POST", {"ref": f"refs/heads/{login}", "sha": sha})
    except HTTPError as error:
        # A simultaneous submission may already have provisioned this branch.
        if error.code != 422:
            raise
        return api.request(path)["object"]["sha"]
    return sha


def git(repo, *args):
    result = subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args],
        capture_output=True, text=True, check=False,
        env={**os.environ, **({"GH_TOKEN": os.environ["COURSE_SYNC_TOKEN"]} if os.environ.get("COURSE_SYNC_TOKEN") else {})},
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def sync_branches(repo, course_url, fork_url):
    """Merge updates without resets, then atomically push both fork branches.

    The temporary repository never checks out or executes student workflows.
    A concurrent student push rejects the atomic push instead of losing work.
    """
    Path(repo).mkdir(parents=True, exist_ok=True)
    git(repo, "init")
    git(repo, "config", "user.name", "Course Sync Bot")
    git(repo, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git(repo, "remote", "add", "origin", fork_url)
    git(repo, "remote", "add", "course", course_url)
    git(repo, "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*")
    git(repo, "fetch", "course", "+refs/heads/main:refs/remotes/course/main")
    git(repo, "checkout", "-b", "main", "refs/remotes/origin/main")
    git(repo, "merge", "-X", "ours", "refs/remotes/course/main", "-m", "Sync course main")
    refs = git(repo, "for-each-ref", "--format=%(refname)", "refs/remotes/origin/workspace").splitlines()
    workspace = "refs/remotes/origin/workspace" if refs else "refs/remotes/origin/main"
    git(repo, "checkout", "-b", "workspace", workspace)
    git(repo, "merge", "-X", "ours", "main", "-m", "Sync published course materials")
    git(repo, "push", "--atomic", "origin", "main:refs/heads/main", "workspace:refs/heads/workspace")


def route_submission(api, course, pr, grade=True):
    """Route metadata only; no PR checkout or student code execution."""
    head_repo = pr["head"].get("repo")
    if not head_repo or not head_repo.get("fork") or not pr["head"]["ref"].startswith("submit/"):
        return False
    login = student_login(head_repo["owner"]["login"])
    if pr["user"]["login"].lower() != login.lower():
        return False
    # Validate actual parentage, rather than trusting a branch name or author.
    fork = api.request("repos/" + head_repo["full_name"])
    if fork.get("parent", {}).get("full_name", "").lower() != course.lower():
        return False
    ensure_student_branch(api, course, login)
    if pr["base"]["ref"] != login:
        api.request(f"repos/{course}/pulls/" + str(pr["number"]), "PATCH", {"base": login})
    # Older fork branches still contain the obsolete workflow. Dispatch trusted
    # main explicitly, instead of depending on the workflow in the student's PR.
    if grade:
        api.request(f"repos/{course}/actions/workflows/ta-grading.yml/dispatches", "POST", {
            "ref": "main", "inputs": {"pull-request-number": str(pr["number"])},
        })
    return True


def synchronize(api, repository, course=COURSE_REPOSITORY, fork_api=None, branches_only=False):
    """Provision all student branches centrally, or sync only the current fork."""
    central = repository.lower() == course.lower()
    forks = list(api.pages(f"repos/{course}/forks")) if central else [api.request(f"repos/{repository}")]
    results = []
    for fork in forks:
        name = fork["full_name"]
        try:
            if central:
                ensure_student_branch(api, course, fork["owner"]["login"])
            elif fork.get("parent", {}).get("full_name", "").lower() != course.lower():
                raise ValueError("This repository is not a direct fork of the course repository.")
            if branches_only or (central and fork_api is None):
                results.append((name, "student branch ready; automatic updates run in the fork's own workflow"))
                continue
            # GITHUB_TOKEN is an installation token, not a user token. The
            # repository metadata permission flags are not an authorization
            # check for that token. Let the actual atomic Git push decide.
            with tempfile.TemporaryDirectory(prefix="course-fork-sync-") as directory:
                sync_branches(directory, f"https://github.com/{course}.git", f"https://github.com/{name}.git")
            results.append((name, "main and workspace synchronized"))
        except (HTTPError, RuntimeError, ValueError) as error:
            results.append((name, f"FAILED: {error}"))
    if central:
        for pr in api.pages(f"repos/{course}/pulls?state=open"):
            try:
                owner = ((pr["head"].get("repo") or {}).get("owner") or {}).get("login")
                route_submission(api, course, pr, grade=pr["base"]["ref"] != owner)
            except (HTTPError, ValueError) as error:
                results.append(("PR #" + str(pr["number"]), f"FAILED: {error}"))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", COURSE_REPOSITORY))
    parser.add_argument("--branches-only", action="store_true")
    args = parser.parse_args()
    api = GitHub(os.environ["GH_TOKEN"])
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request_target":
        if args.repository.lower() != COURSE_REPOSITORY.lower():
            raise RuntimeError("Submission routing runs only in the course repository.")
        event = json.loads(Path(event_path).read_text())
        route_submission(api, args.repository, event["pull_request"])
        return 0
    fork_token = os.environ.get("COURSE_SYNC_TOKEN")
    if args.repository.lower() != COURSE_REPOSITORY.lower():
        # Forks always use their own built-in GITHUB_TOKEN, never a student secret.
        fork_token = None
        os.environ.pop("COURSE_SYNC_TOKEN", None)
    results = synchronize(api, args.repository, fork_api=GitHub(fork_token) if fork_token else None,
                          branches_only=args.branches_only)
    report = "## Course synchronization\n\n" + "\n".join(f"- {repo}: {status}" for repo, status in results) + "\n"
    print(report)
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a") as output:
            output.write(report)
    return int(any(status.startswith(("BLOCKED:", "FAILED:")) for _, status in results))


if __name__ == "__main__":
    raise SystemExit(main())
