---
applyTo: "**"
---
# General Development Rules (Python)

Work in short, test-driven loops:
1. Write or update the tests you need first. Use `.github/instructions/testing.instructions.md` to choose the right layer and markers.
2. Implement the feature or fix.
3. Run the matching test slice (`pytest -m unit`, `pytest -m integration`, or a focused `-k` run).
4. Run type checks: `PYTHONPATH=. mypy .`.
5. Run the lint gate: `PYTHONPATH=. pytest -m lint` (executes `tests/lint/test_flake8.py`).
6. Add or adjust Playwright E2E tests whenever you introduce a new user flow.

## Validation Checklist

Before committing, run:
1. `PYTHONPATH=. pytest -m lint`
2. `PYTHONPATH=. mypy .`
3. `pytest -m "unit or integration"`
4. `npx playwright test` (once the E2E suite is in place)

When all tests pass:
* Update the **TODO list** to reflect the task completion.
* Update the **memory file** with current project state and relevant notes.
* Ensure the **lint suite** passes (`pytest -m lint`) and resolve any issues.
* Fix any **warnings or linting issues** (run `ruff check .` or `flake8`).
* Commit with a **clear, descriptive message**.
* Update these **development guidelines** if new lessons or conventions emerge.
* Stop — we will open a new chat for the next task.

---

## Retain Memory

Each project includes a `memory.md` file.

This file stores:
- The current project state  
- Context or design notes needed between sessions  

Do **not** mark task completions here — that belongs in the TODO list.  
Keep this file concise and up to date.

---

## Update Development Guidelines

Revise this file only if:
- You discover a better workflow
- You add or change key tools or testing practices

Keep it short and consistent with Python best practices.
