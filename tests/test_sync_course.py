"""Exercise course sync against real local Git repositories."""
import subprocess

import pytest

from scripts import sync_course


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, text=True, capture_output=True
    ).stdout.strip()


@pytest.fixture
def repos(tmp_path, monkeypatch):
    course = tmp_path / "course"
    course.mkdir()
    git(course, "init", "-b", "main")
    git(course, "config", "user.name", "Test")
    git(course, "config", "user.email", "test@example.com")
    first = course / "exercises/week_01/practice.py"
    first.parent.mkdir(parents=True)
    first.write_text("# starter\n")
    git(course, "add", ".")
    git(course, "commit", "-m", "Week 01")
    student = tmp_path / "student"
    subprocess.run(["git", "clone", "--depth", "1", "--single-branch", course.as_uri(), str(student)], check=True, capture_output=True)
    git(student, "config", "user.name", "Student")
    git(student, "config", "user.email", "student@example.com")
    fork = tmp_path / "fork.git"
    subprocess.run(["git", "init", "--bare", str(fork)], check=True, capture_output=True)
    git(student, "remote", "set-url", "origin", str(fork))
    # A narrow upstream fetch configuration must not prevent refreshing main.
    git(student, "remote", "add", "upstream", str(course))
    git(student, "config", "remote.upstream.fetch", "+refs/heads/workspace:refs/remotes/upstream/workspace")
    monkeypatch.setattr(sync_course, "DEFAULT_UPSTREAM_URL", str(course))
    monkeypatch.setenv("COURSE_UPSTREAM_URL", str(course))
    return course, student, fork


def publish(course):
    (course / "exercises/week_01/practice.py").write_text("# revised starter\n")
    second = course / "exercises/week_02/challenge.py"
    second.parent.mkdir()
    second.write_text("# Week 02\n")
    git(course, "add", ".")
    git(course, "commit", "-m", "Publish Week 02")


def test_sync_delivers_new_week_preserves_answers_and_pushes_workspace(repos):
    course, student, fork = repos
    answer = student / "exercises/week_01/practice.py"
    answer.write_text("print(42)\n")
    publish(course)
    sync_course.sync_course(str(student))
    assert git(student, "branch", "--show-current") == "workspace"
    assert answer.read_text() == "print(42)\n"
    assert (student / "exercises/week_02/challenge.py").is_file()
    assert git(student, "rev-parse", "main") == git(course, "rev-parse", "main")
    assert git(fork, "rev-parse", "workspace") == git(student, "rev-parse", "HEAD")
    assert "refs/heads/main" not in git(fork, "show-ref")
    before = git(student, "rev-parse", "HEAD")
    sync_course.sync_course(str(student))
    assert git(student, "rev-parse", "HEAD") == before


def test_fetch_failure_stops_before_changing_main(repos):
    course, student, _ = repos
    before = git(student, "rev-parse", "main")
    course.rename(course.with_name("unavailable"))
    with pytest.raises(RuntimeError):
        sync_course.sync_course(str(student))
    assert git(student, "rev-parse", "main") == before


def test_failed_backup_is_reported_after_local_update(repos):
    course, student, _ = repos
    publish(course)
    git(student, "remote", "set-url", "origin", str(student / "missing.git"))
    with pytest.raises(RuntimeError):
        sync_course.sync_course(str(student))
    assert (student / "exercises/week_02/challenge.py").is_file()


def test_background_watcher_delivers_week_without_student_action(repos):
    import shutil

    from scripts import auto_commit_daemon

    course, student, _ = repos
    publish(course)
    scripts_dir = student / "scripts"
    scripts_dir.mkdir()
    shutil.copyfile(sync_course.__file__, scripts_dir / "sync_course.py")
    assert auto_commit_daemon.synchronize_course(str(student))
    assert (student / "exercises/week_02/challenge.py").is_file()


def test_watcher_syncs_at_startup_and_retries(monkeypatch, tmp_path):
    from scripts import auto_commit_daemon as daemon

    attempts = []
    monkeypatch.setattr(daemon, "is_git_repo", lambda repo: True)
    monkeypatch.setattr(daemon, "get_git_status", lambda repo: [])
    monkeypatch.setattr(daemon, "log_message", lambda *args: None)
    monkeypatch.setattr(daemon, "synchronize_course", lambda *args: attempts.append(args) or False)
    times = iter([0, 0, 301, 301])
    monkeypatch.setattr(daemon.time, "monotonic", lambda: next(times))
    sleeps = []

    def sleep(seconds):
        sleeps.append(seconds)
        if len(sleeps) == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(daemon.time, "sleep", sleep)
    with pytest.raises(SystemExit):
        daemon.watch_workspace(str(tmp_path), False)
    assert len(attempts) == 2


def test_auto_commit_daemon_commits_and_pushes_to_origin(repos):
    from scripts import auto_commit_daemon as daemon

    course, student, fork = repos
    git(student, "fetch", "--unshallow", str(course))
    git(student, "push", "origin", "main")
    git(student, "checkout", "-b", "workspace")
    (student / "exercises/week_01/practice.py").write_text("print('auto saved work')\n")
    changed = daemon.get_git_status(str(student))
    assert changed
    success = daemon.perform_auto_commit(str(student), changed, verbose=False)
    assert success
    # Verify commit made on student repo
    assert git(student, "show", "HEAD:exercises/week_01/practice.py") == "print('auto saved work')"
    # Verify auto-push reached fork (origin)
    assert git(fork, "show", "workspace:exercises/week_01/practice.py") == "print('auto saved work')"


