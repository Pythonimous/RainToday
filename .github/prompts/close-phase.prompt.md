---
mode: 'agent'
description: 'Close the current project phase by reviewing, testing, and committing all updates.'
---

# Phase Closure Instructions

0. When PYTHONPATH-related import bugs appear, run `export PYTHONPATH=.` (or prefix the commands below with `PYTHONPATH=.`) before continuing.
1. Run `pytest -m lint` to ensure the Flake8 lint gate passes.
2. Run `mypy .` to perform static type checking and fix all issues.
3. Run `pytest` to execute all unit tests and fix any failing tests.
4. (Future) When Playwright tests exist, run `npx playwright test` as part of this step.
5. Update `TODO.md` to mark all current-phase tasks as completed.
6. Update `README.md` with new features and changes.
7. Update `memory.md` to capture the current state, key updates, and learnings.
8. Update `.gitignore` if new files or directories should be ignored.
9. Run `git diff --name-only main` and review each changed file for completeness.
10. Verify that all items in the TODO list are completed.
11. Add all modified files to the staging area.
12. Commit changes with a clear message:
    ```
    git add .
    git commit -m "Close current project phase: finalized tasks and documentation"
    ```

Ensure all code passes checks, tests, and reviews before committing.
