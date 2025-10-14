

## Project State (2025-10-13)

- Type checking is part of the standard gate: `mypy.ini` excludes test modules while covering application code.
- README and `.github/instructions/development.instructions.md` document the validation checklist (lint, mypy, pytest) and testing taxonomy.
- **Phase 9 (Visitor Counter) is complete**: SQLite-based persistent counter with clean API design.
  - `/visit` (POST): Records a visit, increments counters, returns updated stats.
  - `/stats` (GET): Read-only endpoint to fetch current visit counts without incrementing.
  - Database: `data/stats.db` with atomic SQLite transactions.
  - Tests: Unit tests for db functions, integration tests for endpoints and persistence, E2E tests for UI display.
  - Frontend: Calls `/visit` on page load automatically via JavaScript.
- **Phase 8 (E2E Testing)**: Full Playwright test suite with 5 modules covering all major user flows.
- Test structure follows best practices:
  - `tests/unit/`: Isolated function tests with mocks
  - `tests/integration/`: API endpoint tests and database persistence tests  
  - `tests/e2e/`: Full browser-based Playwright tests
  - `tests/lint/`: Flake8 conformance checks
- All tests pass: 19 unit/integration tests, lint and mypy checks green.

**Phase 10 (UI Enhancements) implemented — pending user visual sign-off.**

Summary of changes:
- Reorganized layout: primary action first, then horizon, then city search.
- Added accent theme toggle (Indigo, Emerald) without altering background color logic used by tests.
- Fade/slide animation for the result block; kept IDs and selectors stable for tests.
- Responsive footer with visit counts and a Credits & Source link.

All unit/integration/E2E tests pass after these changes. Once visuals are approved, we will mark Phase 10 as complete and proceed to Phase 11 (Time Zone & Localization).
