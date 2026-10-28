#!/usr/bin/env bash
# Works even when Python and the Course Tasks extension are unavailable.
set -uo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1
MODE="${1:---check}"
case "$MODE" in
    --check|--repair|--packages|--attach) ;;
    *) echo "Usage: bash scripts/check_environment.sh [--check|--repair|--packages|--attach]"; exit 2 ;;
esac

if [[ "$MODE" == --attach ]]; then
    # /workspaces persists across container rebuilds; *.log is ignored by Git.
    LOG="$ROOT/.course-environment.log"
    date -u > "$LOG"
    timeout 45s bash "$ROOT/scripts/check_environment.sh" --check 2>&1 | tee -a "$LOG"
    result=${PIPESTATUS[0]}
    if (( result != 0 )); then
        echo "Environment check incomplete or failed (exit $result). See $LOG."
        echo "Run: bash scripts/check_environment.sh --repair"
    fi
    # An advisory check must not prevent attaching to repair the workspace.
    exit 0
fi

failed=0
fail() { echo "FAIL: $*"; failed=1; }
PYTHON=/usr/local/bin/python
echo "Checking course environment in $ROOT"
if [[ ! -x "$PYTHON" ]] || ! timeout 8s "$PYTHON" -c 'import sys; sys.exit(sys.version_info < (3, 12))'; then
    fail "Expected Python 3.12+ at $PYTHON."
    echo "Python on PATH: $(command -v python3 || echo unavailable)"
    echo "Use Codespaces: Rebuild Container. If in recovery mode, inspect the creation log first."
else
    echo "OK: $PYTHON ($("$PYTHON" --version))"
    if [[ "$MODE" == --repair || "$MODE" == --packages ]]; then
        if ! timeout 180s "$PYTHON" -m pip install --disable-pip-version-check --retries 2 --timeout 15 -r "$ROOT/requirements.txt" -r "$ROOT/requirements-dev.txt"; then
            fail "Package installation failed. Check the output/network and rerun this command."
        fi
    fi
    if ! timeout 8s "$PYTHON" -c '
import importlib.metadata as m
import pytest
for name, minimum in (("pytest", (8, 0)), ("ruff", (0, 5))):
    version = m.version(name)
    assert tuple(map(int, version.split(".")[:2])) >= minimum, (name, version)
    print(f"OK: {name} {version}")
'; then
        fail "Course packages are missing or outdated. Run: bash scripts/check_environment.sh --repair"
    fi
fi

# Ensure GitHub CLI is available for seamless submissions
if command -v gh >/dev/null 2>&1; then
    echo "OK: gh ($(gh --version 2>/dev/null | head -n 1 || echo available))"
elif [[ "$MODE" == --repair || "$MODE" == --packages ]]; then
    if command -v apt-get >/dev/null 2>&1 && command -v curl >/dev/null 2>&1; then
        echo "Installing GitHub CLI (gh)..."
        (
            export DEBIAN_FRONTEND=noninteractive
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
            sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null 2>&1
            sudo apt-get update -qq >/dev/null 2>&1
            sudo apt-get install -y -qq gh >/dev/null 2>&1
        ) || true
    fi
fi

# Container creation precedes the editor connection; extensions are checked on attach.
if [[ "$MODE" != --packages ]]; then
    if ! command -v code >/dev/null 2>&1; then
        fail "VS Code CLI unavailable; extension verification is incomplete."
        echo "Run this command in the Codespace's VS Code terminal, or inspect Extensions manually."
    elif extensions=$(timeout 8s code --list-extensions 2>&1); then
        for extension in ms-python.python ms-python.vscode-pylance ms-python.debugpy dragoscv.tasks2; do
            if ! printf '%s\n' "$extensions" | grep -Fxiq "$extension"; then
                if [[ "$MODE" == --repair ]]; then
                    echo "Installing $extension..."
                    if ! timeout 60s code --install-extension "$extension"; then
                        fail "Could not install $extension. Check network access and retry."
                        continue
                    fi
                    if ! installed=$(timeout 8s code --list-extensions 2>&1) || ! printf '%s\n' "$installed" | grep -Fxiq "$extension"; then
                        fail "$extension installation could not be verified."
                        continue
                    fi
                else
                    fail "Missing extension: $extension. Run: bash scripts/check_environment.sh --repair"
                    continue
                fi
            fi
            echo "OK: installed $extension"
        done
    else
        fail "Unable to list VS Code extensions: $extensions"
    fi
    echo "Editor checks: extensions must be enabled in this Codespace; installation does not prove activation."
    echo "If Run fails: Python: Select Interpreter -> Enter interpreter path -> $PYTHON"
    echo "If Course Tasks is absent: enable Tasks (dragoscv.tasks2), show the status bar, then Developer: Reload Window."
    echo "Fallback: Command Palette -> Tasks: Run Task."
fi

if (( failed == 0 )); then
    echo "Environment checks passed."
else
    echo "Environment needs attention; follow the instructions above."
fi
exit "$failed"
