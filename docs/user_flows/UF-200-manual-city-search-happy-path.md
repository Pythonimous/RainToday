---
id: UF-200
name: Manual City Search (Happy Path)
last_updated: 2025-10-14
status: ready
---

# UF-200 — Manual City Search (Happy Path)

## Goal
Search for a city manually and show the weather result.

## Actors
- Visitor using the refine panel controls.

## Preconditions
- Landing page has loaded.
- Refine panel is available.

## Steps
1. Click the "Refine" toggle to open the panel.
2. Enter a valid city name in the input field.
3. Click the "Check" button.

## Edge Cases
- Network latency delays geocode or rain responses.
- City names with spaces require correct encoding.

## Expected Results
- App calls `/geocode` with the provided city name.
- App calls `/rain` with the returned coordinates and selected horizon.
- Result message describes the forecast for the requested city.
- Background color aligns with the reported condition.

## Related Tests
- Unit: None.
- Integration: tests/integration/test_geocode_endpoint.py::test_geocode_endpoint_success.
- E2E: tests/e2e/test_city_search.py::test_city_search_flow.

## Notes (optional)
- Manual search works whether or not geolocation succeeded earlier.