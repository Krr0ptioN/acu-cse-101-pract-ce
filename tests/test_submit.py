"""Exercise submission snapshots against real repositories and a mocked GitHub API."""

import json

import pytest
from test_sync_course import git
from test_sync_course import repos as shared_repos

from scripts import submit


@pytest.fixture
def repos(tmp_path, monkeypatch):
    return shared_repos.__wrapped__(tmp_path, monkeypatch)


def test_submission_targets_username_and_only_includes_selected_week(repos, monkeypatch):
    course, student, fork = repos
    git(student, "fetch", "--unshallow", str(course))
    git(course, "branch", "ada")
    git(student, "push", "origin", "main")
    git(student, "checkout", "-b", "workspace")
    (student / "exercises/week_01/practice.py").write_text("print(42)\n")
    other = student / "exercises/week_02"
    other.mkdir()
    (other / "practice.py").write_text("print('other work')\n")
    original_git = submit.checked_git

    def local_git(args, repo):
        args = [str(course) if arg == f"https://github.com/{submit.COURSE_REPOSITORY}.git" else arg for arg in args]
        return original_git(args, repo)

    monkeypatch.setattr(submit, "checked_git", local_git)
    calls = []

    def github(repo, args, body=None):
        calls.append(args)
        if args[:2] == ["repo", "view"]:
            owner, name = submit.COURSE_REPOSITORY.split("/")
            return json.dumps({"isFork": True, "owner": {"login": "ada"}, "parent": {"owner": {"login": owner}, "name": name}})
        if args[:2] == ["pr", "create"]:
            return "https://github.com/teacher/course/pull/1"
        if "pulls" in args[3:4]:
            return "[]"
        if "-f" in args:
            return "[]"
        return "{}"

    monkeypatch.setattr(submit, "run_gh", github)
    submit.handle_submission(str(student), "week_01")
    creation = next(args for args in calls if args[:2] == ["pr", "create"])
    assert creation[creation.index("--base") + 1] == "ada"
    assert creation[creation.index("--head") + 1] == "ada:submit/week_01"
    assert creation[creation.index("--repo") + 1] == submit.COURSE_REPOSITORY
    assert git(student, "branch", "--show-current") == "workspace"
    assert git(fork, "show", "submit/week_01:exercises/week_01/practice.py") == "print(42)"
    assert "week_02" not in git(fork, "ls-tree", "--name-only", "submit/week_01:exercises")
    assert (student / "exercises/week_02/practice.py").is_file()


def test_failed_submission_does_not_create_pr_and_restores_workspace(repos, monkeypatch):
    _course, student, _ = repos
    git(student, "checkout", "-b", "workspace")
    # Fail before preparing the submission when its destination is unavailable.
    monkeypatch.setattr(submit, "run_gh", lambda *args: (_ for _ in ()).throw(RuntimeError("API unavailable")))
    with pytest.raises(RuntimeError, match="API unavailable"):
        submit.handle_submission(str(student), "week_01")
    assert git(student, "branch", "--show-current") == "workspace"


def test_detect_target_week_from_file_path(tmp_path):
    repo = tmp_path / "repo"
    (repo / "exercises/week_01_intro").mkdir(parents=True)
    (repo / "exercises/week_02_vars").mkdir(parents=True)
    file_path = str(repo / "exercises/week_02_vars/practice.py")
    assert submit.detect_target_week(str(repo), file_path=file_path) == "week_02_vars"


def test_detect_target_week_from_modified_file(tmp_path):
    repo = tmp_path / "repo"
    (repo / "exercises/week_01_intro").mkdir(parents=True)
    (repo / "exercises/week_02_vars").mkdir(parents=True)
    git(repo, "init")
    git(repo, "config", "user.name", "Tester")
    git(repo, "config", "user.email", "tester@example.com")
    (repo / "exercises/week_01_intro/practice.py").write_text("print(1)\n")
    (repo / "exercises/week_02_vars/practice.py").write_text("print(2)\n")
    git(repo, "add", "exercises/")
    git(repo, "commit", "-m", "init")
    # Modify week 2 only
    (repo / "exercises/week_02_vars/practice.py").write_text("print('updated')\n")
    assert submit.detect_target_week(str(repo)) == "week_02_vars"


def test_ensure_git_identity_configures_missing_identity(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "empty_gitconfig"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(tmp_path / "empty_system_gitconfig"))
    git(repo, "init")
    submit.ensure_git_identity(str(repo))
    name = git(repo, "config", "user.name")
    assert name == "CSE 101 Student"


def test_run_gh_fallback_when_gh_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(submit.shutil, "which", lambda cmd: None)
    monkeypatch.setattr(submit.os.path, "isfile", lambda path: False)
    monkeypatch.setattr(submit, "python_gh_api", lambda repo, args, body=None: '{"status": "ok"}')
    result = submit.run_gh(str(tmp_path), ["api", "repos/test"])
    assert result == '{"status": "ok"}'


