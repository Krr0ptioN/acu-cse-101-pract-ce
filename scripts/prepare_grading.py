"""Overlay student exercise files onto the trusted course tests for one week."""

import os
import re
import shutil
import stat
from pathlib import Path


def prepare(course: Path, submission: Path, head_ref: str):
    match = re.fullmatch(r"submit/(week_\d{2}_[a-z0-9_]+)", head_ref)
    if not match:
        raise ValueError("Expected a submit/week_XX_name submission branch.")
    week = match[1]
    target = course / "exercises" / week
    if not (target / "test_challenge.py").is_file():
        raise ValueError(f"No trusted challenge tests published for {week}.")
    for name in ("challenge.py", "practice.py"):
        source = submission / "exercises" / week / name
        # Reject symlinks in every component; do not copy student tests or config.
        relative = source.relative_to(submission)
        current = submission
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                raise ValueError(f"Submission contains a symlink: {relative}")
        if not stat.S_ISREG(source.stat().st_mode):
            raise ValueError(f"Expected a regular exercise file: {relative}")
        shutil.copyfile(source, target / name)
    return week


if __name__ == "__main__":
    prepare(Path.cwd(), Path("student-submission"), os.environ["HEAD_REF"])
