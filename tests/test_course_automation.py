"""Verify fork synchronization and username branch routing without GitHub writes."""

from urllib.error import HTTPError

import pytest
from test_sync_course import git, publish
from test_sync_course import repos as shared_repos

from scripts import course_automation as automation
from scripts import sync_course


@pytest.fixture
def repos(tmp_path, monkeypatch):
    return shared_repos.__wrapped__(tmp_path, monkeypatch)


def test_fork_sync_preserves_answers_and_updates_both_branches(repos, tmp_path):
    course, student, fork = repos
    git(student, "fetch", "--unshallow", str(course))
    git(student, "checkout", "-b", "workspace")
    answer = student / "exercises/week_01/practice.py"
    answer.write_text("print(42)\n")
    git(student, "add", ".")
    git(student, "commit", "-m", "Student answers")
    saved = git(student, "rev-parse", "HEAD")
    git(student, "push", "origin", "main", "workspace")
    publish(course)
    runner = tmp_path / "runner"
    runner.mkdir()
    automation.sync_branches(runner, str(course), str(fork))
    assert git(fork, "show", "workspace:exercises/week_01/practice.py") == "print(42)"
    for branch in ("main", "workspace"):
        assert git(fork, "show", f"{branch}:exercises/week_02/challenge.py") == "# Week 02"
    git(fork, "merge-base", "--is-ancestor", saved, "workspace")
    head = git(fork, "rev-parse", "workspace")
    second = tmp_path / "second"
    second.mkdir()
    automation.sync_branches(second, str(course), str(fork))
    assert git(fork, "rev-parse", "workspace") == head
    # A Codespace with older local history must still be able to save and push.
    answer.write_text("print(43)\n")
    sync_course.sync_course(str(student))
    assert git(fork, "show", "workspace:exercises/week_01/practice.py") == "print(43)"
    git(fork, "merge-base", "--is-ancestor", head, "workspace")


def test_fork_without_workspace_gets_one(repos, tmp_path):
    course, student, fork = repos
    git(student, "fetch", "--unshallow", str(course))
    git(student, "push", "origin", "main")
    publish(course)
    automation.sync_branches(tmp_path / "runner", str(course), str(fork))
    assert git(fork, "rev-parse", "main") == git(fork, "rev-parse", "workspace")


class FakeGitHub:
    def __init__(self):
        self.refs = {"main": "course-sha"}
        self.calls = []

    def request(self, path, method="GET", data=None):
        self.calls.append((path, method, data))
        if "/git/ref/heads/" in path:
            branch = path.rsplit("/", 1)[1]
            if branch not in self.refs:
                raise HTTPError(path, 404, "Not Found", {}, None)
            return {"object": {"sha": self.refs[branch]}}
        if path.endswith("/git/refs"):
            self.refs[data["ref"].removeprefix("refs/heads/")] = data["sha"]
            return {}
        if path == "repos/ada/course":
            return {"parent": {"full_name": "teacher/course"}}
        if "/pulls/" in path:
            return {}
        if path.endswith("/dispatches"):
            return {}
        raise AssertionError(path)


def test_student_branch_is_created_once_and_never_reset():
    api = FakeGitHub()
    automation.ensure_student_branch(api, "teacher/course", "ada")
    assert api.refs["ada"] == "course-sha"
    api.refs["ada"] = "instructor-merged-work"
    api.refs["main"] = "new-course-sha"
    automation.ensure_student_branch(api, "teacher/course", "ada")
    assert api.refs["ada"] == "instructor-merged-work"


def submission():
    return {
        "number": 3, "user": {"login": "ada"}, "base": {"ref": "main"},
        "head": {"ref": "submit/week_01_intro", "repo": {
            "fork": True, "full_name": "ada/course", "owner": {"login": "ada"},
        }},
    }


def test_existing_main_pr_is_routed_to_username_branch():
    api = FakeGitHub()
    assert automation.route_submission(api, "teacher/course", submission())
    assert ("repos/teacher/course/pulls/3", "PATCH", {"base": "ada"}) in api.calls
    assert api.calls[-1][2] == {"ref": "main", "inputs": {"pull-request-number": "3"}}


def test_unrelated_author_cannot_route_another_students_pr():
    api = FakeGitHub()
    pr = submission()
    pr["user"]["login"] = "someone-else"
    assert not automation.route_submission(api, "teacher/course", pr)
    assert api.calls == []


@pytest.mark.parametrize("login", ["main", "workspace", "../main", "name/branch"])
def test_invalid_student_branches_are_rejected(login):
    with pytest.raises(ValueError):
        automation.ensure_student_branch(FakeGitHub(), "teacher/course", login)


@pytest.mark.parametrize("permissions", [None, {}, {"push": False}])
def test_fork_uses_its_own_token_without_user_permission_flags(monkeypatch, permissions):
    class InstallationAPI:
        def request(self, path, method="GET", data=None):
            assert path == "repos/ada/course"
            metadata = {"full_name": "ada/course", "parent": {"full_name": "teacher/course"}}
            if permissions is not None:
                metadata["permissions"] = permissions
            return metadata

    pushes = []
    monkeypatch.setattr(automation, "sync_branches", lambda *args: pushes.append(args))
    results = automation.synchronize(InstallationAPI(), "ada/course", course="teacher/course")
    assert len(pushes) == 1
    assert results == [("ada/course", "main and workspace synchronized")]


def test_real_push_errors_still_fail_the_fork_sync(monkeypatch):
    class API:
        def request(self, path):
            return {"full_name": "ada/course", "parent": {"full_name": "teacher/course"}}

    def reject_push(*args):
        raise RuntimeError("Git push rejected: write access not granted")

    monkeypatch.setattr(automation, "sync_branches", reject_push)
    result = automation.synchronize(API(), "ada/course", course="teacher/course")
    assert result[0][1].startswith("FAILED: Git push rejected")


def test_course_provisions_branches_without_student_fork_secrets(monkeypatch):
    class API(FakeGitHub):
        def pages(self, path):
            if path == "repos/teacher/course/forks":
                return iter([{"full_name": "ada/course", "owner": {"login": "ada"}}])
            assert path == "repos/teacher/course/pulls?state=open"
            return iter([])

    api = API()
    monkeypatch.setattr(automation, "sync_branches", lambda *args: pytest.fail("Course token cannot write student forks"))
    result = automation.synchronize(api, "teacher/course", course="teacher/course")
    assert api.refs["ada"] == "course-sha"
    assert "automatic updates run in the fork's own workflow" in result[0][1]
