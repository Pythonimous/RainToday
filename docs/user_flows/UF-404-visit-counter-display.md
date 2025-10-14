---
id: UF-404
name: Visit Counter Display
last_updated: 2025-10-14
status: ready
---

# UF-404 — Visit Counter Display

## Goal
Show accurate visit counts when the page loads.

## Actors
- Visitor viewing the landing page.

## Preconditions
- Backend database is reachable.

## Steps
1. Load the landing page.
2. Wait for the page to call the `/visit` endpoint.

## Edge Cases
- Database lock may delay the increment.
- Offline mode prevents the request and leaves stale counts.

## Expected Results
- `/visit` increments total and today visit counts.
- `#total-visits` and `#today-visits` elements show numeric values.
- Values are non-negative integers, not placeholder text.

## Related Tests
- Unit: tests/unit/test_db.py::test_increment_visits; tests/unit/test_db.py::test_increment_visits_concurrency; tests/unit/test_db.py::test_date_rollover; tests/unit/test_db.py::test_persistence_across_calls.
- Integration: tests/integration/test_stats_endpoint.py::test_visit_endpoint_increments; tests/integration/test_stats_endpoint.py::test_stats_endpoint_read_only; tests/integration/test_stats_persistence.py::test_database_persistence_across_restarts; tests/integration/test_stats_persistence.py::test_database_survives_date_rollover.
- E2E: tests/e2e/test_visit_counts.py::test_visit_counts_display.

## Notes (optional)
- Integration tests cover persistence and date rollover to keep the E2E flow simple.