---
id: UF-202
name: Manual City Search - City Not Found
last_updated: 2025-10-14
status: ready
---

# UF-202 — Manual City Search - City Not Found

## Goal
Handle a manual search when the geocode service cannot locate the city.

## Actors
- Visitor searching for an unrecognized city name.

## Preconditions
- Refine panel is open.

## Steps
1. Enter a city name that the geocode service cannot resolve.
2. Click the "Check" button or press Enter.

## Edge Cases
- Temporary upstream outage returns a 500 error instead of 404.
- User retries quickly with a corrected spelling.

## Expected Results
- `/geocode` returns an error and the UI shows "Could not find city...".
- Background color does not change.
- User can edit the input and try again.

## Related Tests
- Unit: None.
- Integration: tests/integration/test_geocode_endpoint.py::test_geocode_endpoint_not_found.
- E2E: tests/e2e/test_city_search.py::test_city_search_geocode_failure.

## Notes (optional)
- Consider logging repeated failures to spot upstream availability issues.