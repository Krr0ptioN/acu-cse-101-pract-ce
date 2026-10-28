"""Student tests and symlinks must never replace the course rubric."""

import pytest

from scripts.grading_context import resolve
from scripts.prepare_grading import prepare


def test_only_student_exercise_files_are_copied(tmp_path):
    course = tmp_path / "course"
    student = tmp_path / "student"
    for root in (course, student):
        week = root / "exercises/week_03_functions"
        week.mkdir(parents=True)
        for name in ("challenge.py", "practice.py", "test_challenge.py"):
            (week / name).write_text(root.name)
    assert prepare(course, student, "submit/week_03_functions") == "week_03_functions"
    assert (course / "exercises/week_03_functions/challenge.py").read_text() == "student"
    assert (course / "exercises/week_03_functions/test_challenge.py").read_text() == "course"
    file = student / "exercises/week_03_functions/challenge.py"
    file.unlink()
    file.symlink_to(course / "exercises/week_03_functions/test_challenge.py")
    with pytest.raises(ValueError, match="symlink"):
        prepare(course, student, "submit/week_03_functions")


def test_unknown_week_and_traversal_are_rejected(tmp_path):
    with pytest.raises(ValueError):
        prepare(tmp_path, tmp_path, "submit/../../main")


def test_dispatched_grading_uses_the_exact_student_commit():
    pr = {"number": 3, "user": {"login": "ada"}, "base": {"ref": "ada"},
          "head": {"sha": "a" * 40, "ref": "submit/week_03_functions",
                   "repo": {"fork": True, "full_name": "ada/course", "owner": {"login": "ada"}}}}

    class API:
        def request(self, path):
            return pr

    assert resolve(API(), 3)["head_sha"] == "a" * 40
    pr["base"]["ref"] = "main"
    with pytest.raises(ValueError, match="username"):
        resolve(API(), 3)
