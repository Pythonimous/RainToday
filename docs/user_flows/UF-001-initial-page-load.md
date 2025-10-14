---
id: UF-001
name: Initial Page Load
last_updated: 2025-10-14
status: ready
---

# UF-001 — Initial Page Load

## Goal
Load the landing page and display the default UI.

## Actors
- Visitor using a modern web browser.

## Preconditions
- None.

## Steps
1. Navigate to the application URL.
2. Wait for the page assets to finish loading.

## Edge Cases
- Slow network connections delay the first render.
- First-time visitors may see a geolocation prompt.

## Expected Results
- Heading, city input, horizon slider, refine toggle, and check button are visible.
- Horizon label shows Today.
- Visit counter increments and displays updated totals.
- Auto geolocation request starts in the background.

## Related Tests
- Unit: None.
- Integration: tests/integration/test_homepage_layout.py::test_homepage_contains_key_elements.
- E2E: tests/e2e/test_smoke.py::test_homepage_loads; tests/e2e/test_smoke.py::test_initial_background_color.

## Notes (optional)
- Auto geolocation continues in UF-100 through UF-103.