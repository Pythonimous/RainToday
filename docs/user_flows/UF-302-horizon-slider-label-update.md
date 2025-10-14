---
id: UF-302
name: Horizon Slider - Label Update
last_updated: 2025-10-14
status: ready
---

# UF-302 — Horizon Slider - Label Update

## Goal
Update the horizon label to match the slider position in real time.

## Actors
- Visitor adjusting the time horizon slider.

## Preconditions
- Landing page is loaded.

## Steps
1. Locate the horizon slider control.
2. Move the slider through values 0 to 3.

## Edge Cases
- User drags quickly across multiple positions.
- Assistive technologies adjust the slider via keyboard input.

## Expected Results
- Label shows Today when value is 0.
- Label shows 1h, 3h, or 6h for values 1, 2, or 3 respectively.
- Label updates immediately after each change.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_horizon.py::test_horizon_slider_changes_label.

## Notes (optional)
- Label text feeds into the `/rain` request details described in UF-303.