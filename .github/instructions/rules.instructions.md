---
applyTo: "**"
---
# General Development Rules (Python)

You should follow **task-based, test-driven development**.  
For each task:
1. Write the **tests first** (`pytest` preferred, or `unittest` if legacy-compatible).
2. Implement the code.
3. Run tests to ensure correctness:
   - `pytest` to run all tests
   - `pytest -k "TestTypeConversion"` to run a specific test

When all tests pass:
* Update the **TODO list** to reflect the task completion.
* Update the **memory file** with current project state and relevant notes.
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
