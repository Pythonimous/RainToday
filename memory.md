

## Project State (2025-10-14)

**Phase 10 (UI Enhancements & Auto-Geolocation) is complete:**
- **Auto-check geolocation on page load**: App attempts geolocation immediately on load; handles granted, denied, and timeout cases gracefully.
- **Collapsible refine panel**: Controls (city input, horizon slider) hidden by default in collapsed panel; "Refine" button toggles open/close.
- **Try Again button**: Lets users retry geolocation after initial denial.
- **UI simplification**: Removed theme selector; default indigo accent throughout.
- **Database concurrency improvements**: Enabled WAL mode and added _get_connection() helper with optimized settings; single atomic UPDATE statement eliminates race conditions.
- **User flow documentation**: Created comprehensive `docs/user_flows/` directory with 19 flow files (UF-001 through UF-404) documenting all major user journeys.
- **Test coverage updates**: All E2E tests updated for new UI structure (refine panel, result-message element); all tests passing.

**Phase 9 (Visitor Counter) is complete**: SQLite-based persistent counter with clean API design.
  - `/visit` (POST): Records a visit, increments counters, returns updated stats.
  - `/stats` (GET): Read-only endpoint to fetch current visit counts without incrementing.
  - Database: `data/stats.db` with atomic SQLite transactions.
  - Tests: Unit tests for db functions, integration tests for endpoints and persistence, E2E tests for UI display.
  - Frontend: Calls `/visit` on page load automatically via JavaScript.

**Phase 8 (E2E Testing)**: Full Playwright test suite with 5 modules covering all major user flows.

**Test structure** follows best practices:
  - `tests/unit/`: Isolated function tests with mocks
  - `tests/integration/`: API endpoint tests and database persistence tests  
  - `tests/e2e/`: Full browser-based Playwright tests
  - `tests/lint/`: Flake8 conformance checks

**Type checking** is part of the standard gate: `mypy.ini` excludes test modules while covering application code.

**Documentation**: README and `.github/instructions/development.instructions.md` document the validation checklist (lint, mypy, pytest) and testing taxonomy.

## Architecture Notes (2025-10-14)

- Extracted geocoding and weather integrations into `src/services/geocode.py` and `src/services/weather.py`, keeping FastAPI handlers thin and easier to test.
- Added message helper module (`src/services/messages.py`) to centralize message loading/selection logic.
- Introduced `get_visit_stats()` in `src/db.py` so the `/stats` handler reuses the shared database boundary.
- Added unit tests covering the new service layer (`tests/unit/test_messages_service.py`, `tests/unit/test_weather_service.py`) and updated existing DB and geocode unit tests to target the refactored helpers.
- Consolidated integration coverage for the weather-related routes into `tests/integration/test_weather_endpoints.py`, replacing the overlapping geocode/rain endpoint files.

## Close-Phase Verification (2025-10-14)

All validation gates passed for the current phase:
- **Lint**: `pytest -m lint` → 1 passed. Flake8 clean.
- **Type checking**: `mypy .` → Success, no issues in 7 source files.
- **Unit & Integration tests**: `pytest -m "unit or integration"` → 27 passed.
- **E2E tests**: Not rerun this pass (no new flows touched); latest recorded run remained green.

All quality gates remain green. Project is in a stable, committable state.

## Planning Updates (2025-10-14)

- Added Phase 11 "User Flow Audit" in `TODO.md` to prune redundant user flows and align Playwright coverage; renumbered subsequent phases.
- Reordered later phases to execute deployment ahead of time-zone localization and clarified that localization work stays lightweight, now including sample RU/PT message translations.
- Trimmed Phase 14 stretch bullets for brevity while keeping intent intact.
