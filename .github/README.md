# Lightweight Python Agent Template
Lean scaffold for agentic Python projects with linting, typing, and layered tests ready to run.

## Quick Start
```bash
pip install -r requirements.txt   # or the project's chosen manager
flake8
mypy .
pytest
# optional:
./scripts/run_tests.sh
./scripts/run_e2e_tests.sh
```

> Default package path is `src`. Export `SOURCE_DIR=your_module` and update `src/` if you pick a different name.

## Repo Glance
```
.
├── .github/
│   ├── instructions/
│   └── prompts/
├── scripts/
│   ├── run_e2e_tests.sh
│   └── run_tests.sh
├── src/
├── tests/
│   ├── integration/
│   ├── lint/
│   └── unit/
├── memory.md
├── mypy.ini
└── pytest.ini
```

## Project Initialization
- Run `.github/prompts/make-specs.prompt.md` to generate `specification.md`.
- Run `.github/prompts/make-todo.prompt.md` to generate `TODO.md`.

## References
- Development workflow: `.github/instructions/development.instructions.md`
- Testing workflow: `.github/instructions/testing.instructions.md`
- Prompt library: `.github/prompts/`
