"""Exercise setup failure paths without installing packages or extensions."""
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = "ms-python.python\nms-python.vscode-pylance\nms-python.debugpy\ndragoscv.tasks2\n"


@pytest.fixture
def environment(tmp_path):
    repo = tmp_path / "course with spaces"
    (repo / "scripts").mkdir(parents=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for command in ("bash", "dirname", "timeout", "tee", "date", "grep", "touch", "cat"):
        (bin_dir / command).symlink_to(shutil.which(command))
    python = bin_dir / "course-python"
    python.write_text('''#!/bin/bash
if [[ "$*" == *sys.version_info* ]]; then exit "${BAD_PYTHON:-0}"; fi
if [[ "$1" == --version ]]; then echo 'Python 3.12.0'; exit 0; fi
if [[ "$1" == -m ]]; then
    [[ "$*" == *"requirements.txt"* && "$*" == *"requirements-dev.txt"* ]] || exit 9
    [[ "${INSTALL_FAIL:-0}" == 0 ]] || exit 1
    touch "$STATE/packages"
    exit 0
fi
[[ -f "$STATE/packages" ]]
''')
    python.chmod(0o755)
    code = bin_dir / "code"
    code.write_text('''#!/bin/bash
if [[ "$1" == --list-extensions ]]; then
    [[ "${LIST_FAIL:-0}" == 0 ]] || exit 1
    cat "$STATE/extensions"
elif [[ "$1" == --install-extension ]]; then
    [[ "${INSTALL_FAIL:-0}" == 0 ]] || exit 1
    echo "$2" >> "$STATE/extensions"
else exit 2
fi
''')
    code.chmod(0o755)
    script = repo / "scripts/check_environment.sh"
    script.write_text((ROOT / "scripts/check_environment.sh").read_text().replace(
        "PYTHON=/usr/local/bin/python", f'PYTHON="{python}"'
    ))
    (repo / "extensions").write_text(EXTENSIONS)
    (repo / "packages").touch()
    env = {**os.environ, "PATH": str(bin_dir), "STATE": str(repo)}

    def run(mode="--check", **overrides):
        return subprocess.run(
            ["/bin/bash", str(script), mode], cwd=tmp_path,
            env={**env, **overrides}, text=True, capture_output=True, timeout=15,
        )

    return repo, bin_dir, run


def test_success_from_other_directory_and_repeatable_repair(environment):
    _, _, run = environment
    for mode in ("--check", "--repair", "--repair"):
        result = run(mode)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Environment checks passed" in result.stdout


@pytest.mark.parametrize("missing", [True, False])
def test_missing_or_old_python_requires_rebuild(environment, missing):
    _, bin_dir, run = environment
    if missing:
        (bin_dir / "course-python").unlink()
    result = run(BAD_PYTHON="1")
    assert result.returncode == 1
    assert "Codespaces: Rebuild Container" in result.stdout


def test_missing_packages_and_extensions_are_repaired(environment):
    repo, _, run = environment
    (repo / "packages").unlink()
    (repo / "extensions").write_text("")
    result = run()
    assert result.returncode == 1
    assert "Course packages are missing" in result.stdout
    assert "Missing extension: dragoscv.tasks2" in result.stdout
    assert run("--repair").returncode == 0
    assert run().returncode == 0


def test_installation_failure_is_not_success(environment):
    repo, _, run = environment
    (repo / "packages").unlink()
    (repo / "extensions").write_text("")
    result = run("--repair", INSTALL_FAIL="1")
    assert result.returncode == 1
    assert "Package installation failed" in result.stdout
    assert "Could not install dragoscv.tasks2" in result.stdout
    assert "Environment checks passed" not in result.stdout


def test_cli_failure_reports_incomplete_check(environment):
    _, bin_dir, run = environment
    assert run(LIST_FAIL="1").returncode == 1
    (bin_dir / "code").unlink()
    result = run()
    assert result.returncode == 1
    assert "extension verification is incomplete" in result.stdout
    assert run("--packages").returncode == 0


def test_attach_logs_failure_without_blocking_editor(environment):
    repo, _, run = environment
    result = run("--attach", BAD_PYTHON="1")
    assert result.returncode == 0
    assert "check incomplete or failed" in result.stdout
    assert "Expected Python 3.12+" in (repo / ".course-environment.log").read_text()


def test_attach_timeout_is_visible(environment):
    _, bin_dir, run = environment
    timeout = bin_dir / "timeout"
    timeout.unlink()
    timeout.write_text("#!/bin/bash\nexit 124\n")
    timeout.chmod(0o755)
    result = run("--attach")
    assert result.returncode == 0
    assert "exit 124" in result.stdout


def test_editor_interpreter_defaults_agree():
    container = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text())
    workspace = json.loads((ROOT / ".vscode/settings.json").read_text())
    assert container["customizations"]["vscode"]["settings"]["python.defaultInterpreterPath"] == workspace["python.defaultInterpreterPath"] == "/usr/local/bin/python"
