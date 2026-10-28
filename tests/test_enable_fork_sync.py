"""The first student sync should install and activate the recurring workflow."""

from types import SimpleNamespace

from scripts import enable_fork_sync as setup


def test_initial_sync_updates_main_and_workspace_then_enables_schedule(monkeypatch, tmp_path):
    monkeypatch.setattr(setup.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(
        stdout="https://github.com/ada/course.git\n", returncode=0,
    ))
    calls = []

    def api(repo, *args, **kwargs):
        calls.append((args, kwargs))
        if args == ("repos/ada/course",):
            return {"parent": {"full_name": setup.COURSE_REPOSITORY}}
        if args == ("repos/ada/course/actions/permissions",):
            return {"enabled": False}
        return {}

    monkeypatch.setattr(setup, "github", api)
    syncs = []
    monkeypatch.setattr(setup, "sync_branches", lambda *args: syncs.append(args))
    setup.enable_fork_sync(str(tmp_path))
    assert syncs[0][1:] == (f"https://github.com/{setup.COURSE_REPOSITORY}.git", "https://github.com/ada/course.git")
    assert calls[-2] == (("repos/ada/course/actions/permissions", "--method", "PUT"), {"data": {"enabled": True}})
    assert calls[-1][0] == ("repos/ada/course/actions/workflows/course-sync.yml/enable", "--method", "PUT")


def test_local_remotes_do_not_try_to_enable_github_actions(monkeypatch, tmp_path):
    monkeypatch.setattr(setup.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(
        stdout="/tmp/fork.git\n", returncode=0,
    ))
    monkeypatch.setattr(setup, "github", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("Unexpected API call")))
    setup.enable_fork_sync(str(tmp_path))
