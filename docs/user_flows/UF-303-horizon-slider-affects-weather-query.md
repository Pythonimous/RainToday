---
id: UF-303
name: Horizon Slider - Affects Weather Query
last_updated: 2025-10-14
status: ready
---

# UF-303 — Horizon Slider - Affects Weather Query

## Goal
Send the selected horizon value with each weather request.

## Actors
- Visitor running a manual city search.

## Preconditions
- Refine panel is open.
- Horizon slider is visible.

## Steps
1. Set the horizon slider to the desired value.
2. Enter a city name.
3. Click the "Check" button.

## Edge Cases
- User changes the slider between repeated searches.
- Cached API responses might obscure horizon mismatches.

## Expected Results
- `/rain` requests include the `horizon` query parameter that matches the slider.
- Backend returns a forecast for the requested horizon window.
- Result message and background reflect the returned condition.

## Related Tests
- Unit: None.
- Integration: tests/integration/test_rain_endpoint.py::test_rain_endpoint_valid_params.
- E2E: tests/e2e/test_horizon.py::test_horizon_affects_rain_query; tests/e2e/test_horizon.py::test_horizon_1h_parameter.

## Notes (optional)
- Coverage assumes the mapping defined in UF-302 remains accurate.