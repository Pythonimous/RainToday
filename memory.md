

## Project State (2025-10-13)

- Type checking is part of the standard gate: `mypy.ini` excludes test modules while covering application code.
- README and `.github/instructions/development.instructions.md` now document the validation checklist (lint, mypy, pytest) and testing taxonomy.
- Phase 7 documentation tasks are fully closed in `TODO.md`; focus can shift to Phase 8 Playwright scaffolding.
- Root-level `__init__.py` was removed to keep package resolution unambiguous for mypy.
- Errant `development-guidelines.md` file at the repo root is gone; guidance now lives in the instructions directory.
- Requirements now include `types-requests` so HTTP calls retain stub coverage during type checks.

**Next:** Begin Phase 8 by setting up Playwright tooling and authoring the first browser smoke tests.
