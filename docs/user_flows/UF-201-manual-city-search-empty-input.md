---
id: UF-201
name: Manual City Search - Empty Input
last_updated: 2025-10-14
status: ready
---

# UF-201 — Manual City Search - Empty Input

## Goal
Prevent empty submissions and guide the user to enter a city name.

## Actors
- Visitor attempting to search without typing a city.

## Preconditions
- Refine panel is open.

## Steps
1. Leave the city input blank.
2. Click the "Check" button or press Enter.

## Edge Cases
- User tabs away and submits via keyboard shortcut.
- Browser autofill inserts whitespace characters only.

## Expected Results
- Frontend validation blocks the request.
- Result area shows "Please enter a city name."
- Input field stays focused for quick correction.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_city_search.py::test_city_search_empty_input.

## Notes (optional)
- Validation happens client-side before any API request.