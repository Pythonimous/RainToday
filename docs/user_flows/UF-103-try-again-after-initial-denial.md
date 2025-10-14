---
id: UF-103
name: Try Again After Initial Denial
last_updated: 2025-10-14
status: ready
---

# UF-103 — Try Again After Initial Denial

## Goal
Let the user retry geolocation after rejecting the first prompt.

## Actors
- Visitor who denied geolocation once and now wants to grant it.

## Preconditions
- UF-101 has occurred and the "Try Again" button is visible.

## Steps
1. Click the "Try Again" button.
2. Accept the renewed geolocation permission prompt.
3. Wait for the automatic weather update to finish.

## Edge Cases
- Browser reuses cached coordinates from an earlier session.
- Permission changes in browser settings instead of through the prompt.

## Expected Results
- App issues a fresh geolocation request.
- Weather result appears with updated message and styling.
- Background color reflects the returned condition.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_autocheck_geolocation.py::test_try_again_after_denial.

## Notes (optional)
- Flow relies on the denial state described in UF-101.