---
id: UF-102
name: Auto-Check Geolocation Timeout
last_updated: 2025-10-14
status: in-progress
---

# UF-102 — Auto-Check Geolocation Timeout

## Goal
Show a helpful fallback when the auto geolocation request times out.

## Actors
- Visitor whose device provides geolocation slowly.

## Preconditions
- Browser supports geolocation APIs.
- User grants geolocation access.
- GPS response takes longer than seven seconds.

## Steps
1. Open the application URL.
2. Grant the geolocation prompt.
3. Wait until the timeout threshold is reached.

## Edge Cases
- Browser may emit a permission error before the timeout fires.
- Device might deliver coordinates just after the timeout message.

## Expected Results
- After roughly seven seconds a timeout message appears.
- Manual search controls remain available for fallback.
- Background stays in the default state until a city search runs.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_autocheck_geolocation.py::test_autocheck_geolocation_timeout (skipped).

## Notes (optional)
- Browser behavior currently prevents the timeout flow from completing; see test skip rationale.