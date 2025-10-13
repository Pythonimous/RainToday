

## Project State (2025-10-13)

- Type checking is part of the standard gate: `mypy.ini` excludes test modules while covering application code.
- README and `.github/instructions/development.instructions.md` now document the validation checklist (lint, mypy, pytest) and testing taxonomy.
- Phase 8 is now complete: full Playwright E2E test suite covering smoke tests, city search, horizon selection, geolocation flows, and background color changes.
- E2E tests use mocked API responses and browser permissions to ensure deterministic, isolated testing.
- Test structure: `tests/e2e/` with conftest.py, 5 test modules, 17 test cases total.
- All E2E tests pass cleanly; lint and type checks remain green.
- `run_e2e_tests.sh` script provided for convenient E2E test execution with server check.
- Requirements updated with `playwright` and `pytest-playwright` packages.
- pytest.ini updated with `e2e` marker for test categorization.

**Next:** Move to Phase 9 (Visitor Counter and Persistence) or Phase 10 (UI Enhancements) based on priorities.
