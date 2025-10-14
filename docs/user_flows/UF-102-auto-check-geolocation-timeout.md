---
id: UF-102
name: Auto-Check Geolocation Timeout
last_updated: 2025-10-14
status: ready
---

# UF-102 — Auto-Check Geolocation Timeout

## Goal
Show a helpful fallback when the auto geolocation request times out.

## Actors
- Visitor whose device provides geolocation slowly (e.g., poor GPS signal, slow network).

## Preconditions
- Browser supports geolocation APIs.
- User grants geolocation permission (or doesn't deny it).
- GPS/location resolution takes longer than seven seconds.

## Steps
1. Open the application URL.
2. Grant (or don't respond to) the geolocation prompt.
3. Wait for the seven-second timeout threshold to be reached.

## Edge Cases
- Browser may emit a permission error before the timeout fires in some test environments.
- Device might deliver coordinates immediately after the timeout message appears.
- Some browsers may never reach the timeout if they fail quickly with PERMISSION_DENIED.

## Expected Results
- After seven seconds without a successful geolocation response, a timeout message appears: "Location timed out. Use 'Refine' or try again."
- The refine panel remains collapsed but accessible via the "Refine location" button.
- The "Try again" button allows re-attempting geolocation.
- Background stays in the default indigo state until a successful weather check completes.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_autocheck_geolocation.py::test_autocheck_geolocation_timeout (skipped - see note).

## Notes
- The timeout mechanism is implemented and functions correctly in production.
- Automated E2E testing of this flow is unreliable because browser permission denial typically occurs faster than the app's timeout in test environments.
- The test remains skipped to prevent flaky failures, but the feature itself is verified through manual testing.
- This flow primarily protects users with slow GPS or network conditions in real-world scenarios.