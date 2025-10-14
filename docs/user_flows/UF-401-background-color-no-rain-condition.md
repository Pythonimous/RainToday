---
id: UF-401
name: Background Color - No Rain Condition
last_updated: 2025-10-14
status: ready
---

# UF-401 — Background Color - No Rain Condition

## Goal
Show a blue background when the forecast reports no rain.

## Actors
- Visitor who has fetched a weather result that returns no_rain.

## Preconditions
- A weather check has completed.
- `/rain` response includes `condition: "no_rain"`.

## Steps
1. Trigger a weather check via geolocation or manual search.
2. Receive a response indicating no rain.

## Edge Cases
- Switching from other conditions must remove old classes before applying blue.
- Quick successive requests should always reflect the latest state.

## Expected Results
- Body element gains the `bg-blue-200` class.
- Prior weather background classes are removed.
- Result message confirms dry conditions.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_background.py::test_background_no_rain_condition.

## Notes (optional)
- Weather messages come from `data/messages.json` and may change over time.