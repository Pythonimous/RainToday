---
id: UF-402
name: Background Color - Maybe Condition
last_updated: 2025-10-14
status: ready
---

# UF-402 — Background Color - Maybe Condition

## Goal
Show a yellow background when the forecast is uncertain.

## Actors
- Visitor who has fetched a weather result that returns maybe.

## Preconditions
- A weather check has completed.
- `/rain` response includes `condition: "maybe"`.

## Steps
1. Trigger a weather check via geolocation or manual search.
2. Receive a response indicating maybe.

## Edge Cases
- Repeated maybe responses should not accumulate multiple classes.
- Transitioning from rain or no_rain must remove their classes first.

## Expected Results
- Body element gains the `bg-yellow-100` class.
- Prior weather background classes are removed.
- Result message communicates uncertain conditions.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_background.py::test_background_maybe_condition.

## Notes (optional)
- Color choice conveys caution but should remain accessible; monitor contrast changes.---
id: UF-402
name: Background Color - Maybe Condition
last_updated: 2025-10-14
---

# UF-402 — Background Color - Maybe Condition

## Goal
Show a yellow background when the forecast is uncertain.

## Actors
- Visitor who has fetched a weather result that returns maybe.

## Preconditions
- A weather check has completed.
- `/rain` response includes `condition: "maybe"`.

## Steps
1. Trigger a weather check via geolocation or manual search.
2. Receive a response indicating maybe.

## Edge Cases
- Repeated maybe responses should not accumulate multiple classes.
- Transitioning from rain or no_rain must remove their classes first.

## Expected Results
- Body element gains the `bg-yellow-100` class.
- Prior weather background classes are removed.
- Result message communicates uncertain conditions.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_background.py::test_background_maybe_condition.

## Notes (optional)
- Color choice conveys caution but should remain accessible; monitor contrast changes.