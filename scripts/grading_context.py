"""Resolve and validate a submitted PR before a read-only grading job checks it out."""

import os
import re

try:
    from .course_automation import COURSE_REPOSITORY, GitHub, student_login
except ImportError:
    from course_automation import COURSE_REPOSITORY, GitHub, student_login


def resolve(api, number):
    pr = api.request(f"repos/{COURSE_REPOSITORY}/pulls/{int(number)}")
    repo = pr["head"].get("repo")
    if not repo or not repo.get("fork"):
        raise ValueError("Expected a student fork submission.")
    username = student_login(repo["owner"]["login"])
    if pr["base"]["ref"] != username or pr["user"]["login"].lower() != username.lower():
        raise ValueError("Submission must target its fork owner's username branch.")
    if not re.fullmatch(r"submit/week_\d{2}_[a-z0-9_]+", pr["head"]["ref"]):
        raise ValueError("Unexpected submission branch.")
    if not re.fullmatch(r"[a-f0-9]{40}", pr["head"]["sha"]):
        raise ValueError("Unexpected submission commit.")
    return {"head_repo": repo["full_name"], "head_sha": pr["head"]["sha"],
            "head_ref": pr["head"]["ref"], "pull_number": str(pr["number"])}


if __name__ == "__main__":
    values = resolve(GitHub(os.environ["GH_TOKEN"]), os.environ["PR_NUMBER"])
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.writelines(f"{key}={value}\n" for key, value in values.items())
