---
id: UF-400
name: Background Color - Rain Condition
last_updated: 2025-10-14
status: ready
---

# UF-400 — Background Color - Rain Condition

## Goal
Show a gray background when the forecast reports rain.

## Actors
- Visitor who has fetched a weather result that returns rain.

## Preconditions
- A weather check has completed.
- `/rain` response includes `condition: "rain"`.

## Steps
1. Trigger a weather check via geolocation or manual search.
2. Receive a response indicating rain.

## Edge Cases
- Multiple consecutive rain queries should not stack duplicate classes.
- CSS caches must refresh correctly after hot reloads.

## Expected Results
- Body element gains the `bg-gray-200` class.
- Any previous weather background classes are removed.
- Result message communicates the rainy condition.

## Related Tests
- Unit: None.
- Integration: tests/integration/test_rain_endpoint.py::test_rain_endpoint_valid_params.
- E2E: tests/e2e/test_background.py::test_background_rain_condition.

## Notes (optional)
- Message text may vary because responses are randomized.