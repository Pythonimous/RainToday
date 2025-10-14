---
id: UF-203
name: Manual City Search - Special Characters
last_updated: 2025-10-14
status: ready
---

# UF-203 — Manual City Search - Special Characters

## Goal
Support manual searches that include spaces, accents, or special characters.

## Actors
- Visitor entering a city with non-ASCII characters.

## Preconditions
- Refine panel is open.

## Steps
1. Open the refine panel.
2. Enter a city such as "São Paulo" in the input.
3. Click "Check" to fetch weather data.

## Edge Cases
- Browser encoding differences alter how characters are sent.
- Non-Latin scripts may still be unsupported by the upstream API.

## Expected Results
- Client encodes the city name correctly.
- `/geocode` returns matching coordinates for the provided name.
- Weather result appears with the correct background color.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_city_search.py::test_city_search_with_special_characters.

## Notes (optional)
- International support is best with Latin-based alphabets; document gaps elsewhere if discovered.