# 🎓 ACU CSE 101: Introduction to Programming — Practice & Workshops

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Krr0ptioN/acu-cse-101-pract-ce)

Welcome to the official student practice workspace for **CSE 101: Introduction to Programming** at **Acıbadem University (2026 Academic Year)**.

This repository is aligned with the textbook **_Think Python_ by Allen B. Downey** and configured for instant, zero-setup programming in **GitHub Codespaces**.

---

## Quickstart (Get Coding in 2 Minutes)

### Step 1: Fork this Repository
Click the **Fork** button at the top-right of this repository page to create your personal copy under your GitHub account.

### Step 2: Open in GitHub Codespaces
In your forked repository, click the green **Code** button, select the **Codespaces** tab, and click **Create codespace on main**.
*(Everything is pre-installed for you: Python 3.12, VS Code extensions, test runners, and auto-save).*

### Step 3: Start Coding & Check
1. Open the current week's folder in the left sidebar: [`exercises/week_01_intro/practice.py`](exercises/week_01_intro/practice.py).
2. Write your code and calculations directly in `practice.py`.
3. Use the **`$(checklist) Course Tasks`** menu on the left side of the bottom status bar:
   - **`Run Tests`** checks your answers.
   - **`Submit`** sends your practice work to the TAs after your tests pass.
   - **`Sync Course`** downloads newly released weekly exercises.
   - **`Play`** runs the Python file currently open in the editor.

---


## Missing Course Tasks or Python Run button

Open **Terminal → New Terminal** in your Codespace. From the repository folder,
run the diagnostic even if the bottom menu is missing:

```bash
bash scripts/check_environment.sh --check
```

To install missing course packages and required editor extensions:

```bash
bash scripts/check_environment.sh --repair
```

Repair can take several minutes when downloading extensions. Network or install
failures are reported; restore connectivity and rerun the command. It does not
change your answers or Git branches. It requires the course's Python 3.12+
container; it does not install a replacement system Python.

If Python is missing or too old, use the Command Palette
(**Ctrl+Shift+P**, or **Cmd+Shift+P** on macOS) → **Codespaces: Rebuild Container**.
If Codespaces reports recovery mode, open **View creation log** and ask your TA
to resolve the reported container/setup failure before rebuilding again.

After repair, use **Developer: Reload Window**. If the top Run button still
fails, open a `.py` file and choose **Python: Select Interpreter → Enter
interpreter path**, then enter `/usr/local/bin/python`. An earlier interpreter
selection can override the repository default.

If **Course Tasks** is still missing:

- In Extensions, verify **Tasks** (`dragoscv.tasks2`) is installed and enabled in
  this Codespace. Also verify **Python**, **Pylance**, and **Python Debugger** are
  enabled. Installation checks cannot prove that an extension activated.
- Enable **View → Appearance → Status Bar** and reload the window.
- Use **Command Palette → Tasks: Run Task** to access **Run Tests**, **Submit**,
  **Sync Course**, **Play**, and **Check Environment** without the menu.

### TA rollout for existing Codespaces

1. Save all open student files. Bring the latest course files into the existing
   workspace using **Tasks: Run Task → Sync Course**, or
   `python3 scripts/sync_course.py` from the repository folder. If Python itself
   is unavailable, inspect the creation log and rebuild the existing container
   first, then sync. Resolve sync errors with the TA; do not reset student work.
2. Confirm the updated `scripts/check_environment.sh` and container configuration
   are present. If the diagnostic file is missing, the update has not arrived.
   Rebuild the container to apply the updated configuration. Merely restarting
   or syncing repository files does not apply container configuration changes.
3. Run the diagnostic and repair commands above, then reload the window and
   correct the interpreter selection if needed.
4. Open a Python exercise and verify that the top Run button and **Course Tasks
   → Play** execute it, and **Run Tests** launches pytest. Unfinished answers can
   fail course tests even when the environment is healthy.

New and rebuilt Codespaces check the environment whenever the editor attaches.
This read-only check is limited to 45 seconds and records output in the ignored
`.course-environment.log` at the repository root. Incomplete checks do not block
the editor; run the repair command in its terminal. Extension downloads may
still be finishing on the first attachment, so rerun the check afterward.
Keep existing Codespaces and student branches; deletion/recreation is not the
normal recovery procedure. Workspace files survive a container rebuild, but
customizations outside `/workspaces` may not.

## 📅 Course Curriculum & Progressive Weekly Releases

Exercises are released progressively week by week. Each week's challenge folder is kept in an independent release module:

| Week | Directory | Think Python Chapters | Topic Summary | Status |
|:---:|:---|:---|:---|:---:|
| **01** | [`exercises/week_01_intro/`](exercises/week_01_intro/) | Ch. 1 & 2 | The Way of the Program & Basic Arithmetic | **Released** |
| **02** | `exercises/week_02_variables/` | Ch. 2 | Variables, Expressions and Statements | *Weekly Release* |
| **03** | `exercises/week_03_functions/` | Ch. 3 | Functions, Parameters and Return Values | *Weekly Release* |
| **04–05** | [`exercises/week_04_conditions_loops_recursion/`](exercises/week_04_conditions_loops_recursion/) | Ch. 5 & 7 | Conditions, Boolean Expressions, for / while Loops & Simple Recursion | **Released together** |
| **06** | `exercises/week_06_strings_lists/` | Ch. 8 & 10 | Strings, Indexing, Slicing & Lists | *Weekly Release* |
| **07** | *Midterm I Review* | Ch. 1–10 | Comprehensive Practice Review | *In Class* |
| **08** | `exercises/week_08_dictionaries_tuples/` | Ch. 11 & 12 | Dictionaries and Tuples | *Weekly Release* |
| **09** | `exercises/week_09_files/` | Ch. 14 | File Reading, Writing and Exceptions | *Weekly Release* |
| **10** | `exercises/week_10_classes_objects/` | Ch. 15 | Classes, Objects and 2D Geometry | *Weekly Release* |
| **11** | `exercises/week_11_classes_functions/` | Ch. 16 | Classes, Time and Pure Functions | *Weekly Release* |
| **12** | `exercises/week_12_classes_methods/` | Ch. 17 | Object-Oriented Methods & Operator Overloading | *Weekly Release* |
| **13** | `exercises/week_13_inheritance/` | Ch. 18 | Inheritance & Card Deck Polymorphism | *Weekly Release* |
| **14** | *Midterm II Review* | Ch. 11–18 | Comprehensive OOP & Data Structures Review | *In Class* |
| **15** | *Final Project Prep* | All | Course Synthesis & Final Project | *In Class* |

---

## 🔄 Automatic Course Updates

Codespaces automatically check for new course materials at startup and every five
minutes while running. Published weeks appear in the workspace without student
action. The background watcher saves exercise changes before syncing, keeps
student answers when updates overlap, and backs up the working branch to the
student fork. Temporary network or backup failures are logged and retried.

The **Sync Course** action in **Course Tasks** is also available for an immediate
check. Instructor diagnostics are recorded in `.git/auto_commit.log`.

Existing Codespaces that still run the old save-only watcher require a one-time
instructor-managed rollout of the updated scripts. Publishing to the course
repository alone cannot replace a process already running in a student Codespace.

## Instructor automation and student submissions

The **Sync course and prepare student branches** GitHub Action runs on pushes to
course `main`, every Monday at **14:30 Istanbul time** (11:30 UTC), and by manual dispatch. It creates a persistent branch
named after each fork owner's GitHub username. Existing student branches are
never reset. It also redirects older `submit/week_*` PRs from `main` to the
student's username branch.

Submissions contain only the selected week's exercise folder. The Submit action
opens a PR from `student:submit/week_03_functions` into
`Krr0ptioN/acu-cse-101-pract-ce:student`. Instructor merges retain each student's
work on that branch. Automated grading uses the published course tests and the
bundled TA action, with results in the Actions job summary. Read-only fork tokens
may prevent posting a PR comment; they do not prevent grading.

### Automatic fork synchronization

Each fork's scheduled workflow uses GitHub's built-in `GITHUB_TOKEN` with
`contents: write` to update **its own** `main` and `workspace`. Students do not
configure tokens or secrets. The sync tool attempts an atomic Git push; a real
push rejection fails the run instead of being hidden behind a success message.
Repository metadata permission flags are not used to reject installation tokens.

The course repository's workflow provisions username branches and routes PRs.
It delegates normal fork updates to the workflow running inside each fork, since
its own token cannot write other repositories. For instructor-managed deployments
only, an optional `COURSE_SYNC_TOKEN` can authorize central writes to forks that
have already granted that credential access. That is not required for student
fork workflows.

The workflow merges course `main` into each fork's `main` and `workspace`,
preferring existing student content when edits overlap. New files and weeks are
added. Both branches are pushed atomically; concurrent pushes or unresolved
conflicts fail safely and are retried on the next run. It never force-pushes
student branches and never executes student code during synchronization.

After students bring in this update and run **Sync Course** once, the sync tool
also updates their fork's `main` and `workspace`, enables GitHub Actions when
needed, and activates the scheduled workflow using their existing GitHub login.
Each fork then updates itself every **Monday at 14:30 Istanbul time** using its
own `GITHUB_TOKEN`. Students do not need a shared instructor token or recurring
manual repository syncs. If GitHub refuses the initial activation because the
login lacks permissions, the tool reports that setup failed; this must be
resolved once before automatic updates can run.

GitHub can delay scheduled jobs during service load and disables inactive public
repository schedules after 60 days. The scheduled workflow runs from the fork's
default branch, which is why the first setup updates `main` as well as `workspace`.

Remote branch updates do not change files in a running Codespace. The course's
background watcher fetches updates every five minutes once its updated version
has been installed. Older save-only watchers still need instructor-managed
installation; a GitHub Action cannot replace a running process in a Codespace.
