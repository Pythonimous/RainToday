---
id: UF-301
name: Refine Panel - Single Input Instance
last_updated: 2025-10-14
status: ready
---

# UF-301 — Refine Panel - Single Input Instance

## Goal
Ensure only one city input field exists when the refine panel is open.

## Actors
- Visitor opening the refine panel.

## Preconditions
- Landing page is loaded.

## Steps
1. Click the "Refine" toggle to open the panel.
2. Inspect the form fields displayed inside the panel.

## Edge Cases
- Panel is opened and closed repeatedly during the same session.
- Browser restores the page from cache after navigation.

## Expected Results
- Only one `#city-input` element exists in the DOM.
- Input accepts text without duplication or focus issues.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_refine_panel.py::test_single_city_input_when_panel_open.

## Notes (optional)
- Guards against duplicate inputs caused by repeated component initialization.