---
id: UF-100
name: Auto-Check Geolocation on Page Load (Granted)
last_updated: 2025-10-14
status: ready
---

# UF-100 — Auto-Check Geolocation on Page Load (Granted)

## Goal
Fetch weather automatically when the user grants geolocation on load.

## Actors
- Visitor whose browser grants geolocation access.

## Preconditions
- Browser supports geolocation APIs.
- User has not blocked geolocation for the site.

## Steps
1. Open the application URL.
2. Accept the browser geolocation permission prompt.
3. Wait for the automatic weather update.

## Edge Cases
- Permission was previously granted, so the prompt does not appear.
- Browser returns cached coordinates instead of a fresh reading.

## Expected Results
- App requests geolocation immediately after load.
- Coordinates are received from the browser.
- Weather result appears without manual interaction.
- Background color updates to match the reported condition.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_autocheck_geolocation.py::test_autocheck_geolocation_granted.

## Notes (optional)
- Manual search remains available if the auto result is incorrect.