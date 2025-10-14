---
id: UF-300
name: Refine Panel - Toggle Open/Close
last_updated: 2025-10-14
status: ready
---

# UF-300 — Refine Panel - Toggle Open/Close

## Goal
Allow users to open and close the refine panel as needed.

## Actors
- Visitor interacting with the refine controls.

## Preconditions
- Landing page is loaded.

## Steps
1. Click the "Refine" toggle to open the panel.
2. Click the toggle again to close the panel.
3. Press Escape while the panel is open to close it.

## Edge Cases
- Rapid toggles still leave the panel in a consistent state.
- Keyboard focus remains inside the panel when Escape is pressed.

## Expected Results
- Panel gains the `panel-open` class when expanded.
- Panel returns to the `panel-collapsed` class when closed.
- Escape key closes the panel when it is open.

## Related Tests
- Unit: None.
- Integration: None.
- E2E: tests/e2e/test_refine_panel.py::test_refine_toggle_open_close_escape.

## Notes (optional)
- Initial state is collapsed so manual controls stay hidden on load.