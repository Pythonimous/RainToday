---
id: UF-101
name: Auto-Check Geolocation on Page Load (Denied)
last_updated: 2025-10-14
status: ready
---

# UF-101 — Auto-Check Geolocation on Page Load (Denied)

## Goal
Handle the initial load when the user denies the geolocation prompt.

## Actors
- Visitor who declines geolocation access.

## Preconditions
- Browser supports geolocation APIs.

## Steps
1. Open the application URL.
2. Deny the browser geolocation permission prompt.
3. Review the fallback options shown on the page.

## Edge Cases
- Browser auto-denies because the user blocked the site earlier.
- Permission is denied on one device but later granted on another.

## Expected Results
- Error message explains that location access was denied.
- "Try Again" button is visible for a quick retry.
- "Refine location" toggle is visible and the panel stays collapsed.
- City input focuses when the panel is opened manually.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_autocheck_geolocation.py::test_autocheck_geolocation_denied.

## Notes (optional)
- UX improvement about auto-opening the panel is tracked in COVERAGE_GAP_ANALYSIS.md (GAP-001 / ISSUE-001).