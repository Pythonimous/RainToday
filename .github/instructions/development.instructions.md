---
applyTo: "**"
---
# Development Loop

- Frame the smallest useful change before touching code.
- Write or update the tests that prove the change.
- Implement just enough code to satisfy the tests.
- Run the specific `pytest` slice for the area you touched.
- Spot-check style with `flake8` when rapid feedback helps.
- Run `mypy .` and resolve every type error.
- Run `pytest -m lint` to enforce the shared lint gate.
- Capture durable context in `memory.md` as you go.
- When the work is stable, execute `.github/prompts/close-phase.prompt.md`.
- Repeat the loop until the feature is ready to hand off.
