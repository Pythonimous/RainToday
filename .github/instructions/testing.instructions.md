---
applyTo: "**"
---
# Testing Conventions

All tests must live in the `tests/` directory and be organized by type:

```
├──
tests/
├── unit/          # Isolated logic tests
├── integration/   # Component and endpoint interaction tests
├── e2e/           # Full user-flow browser tests (Playwright)
└── lint/          # Flake8 style checks


```

### Unit Tests
- Validate **individual functions** or classes in isolation.
- Should **not perform network calls** or depend on other services.
- Mark each test with `@pytest.mark.unit` and run them via `pytest -m unit`.

### Integration Tests
- Validate **FastAPI endpoints** and **multi-component interactions**.
- Use FastAPI `TestClient` or similar tools for HTTP calls.
- Mark with `@pytest.mark.integration` and run via `pytest -m integration`.
- Mock external APIs (`pytest-mock`, `unittest.mock`) so tests stay deterministic.
- Add or update integration coverage whenever endpoints or cross-module flows change.

### End-to-End (E2E) Tests
- Live in `tests/e2e/`.
- Use **Playwright** to exercise full browser journeys.
- Run with `npx playwright test`.
- Add or update scenarios whenever UX flows or user-facing behaviors evolve.

### Lint Suite
- `pytest -m lint` executes `tests/lint/test_flake8.py` to enforce `.flake8`.
- Fix all reported style issues before continuing.

### Shared Fixtures
- Place reusable fixtures in `tests/conftest.py` so they are available across test layers.

See `.github/instructions/development.instructions.md` for the full workflow checklist and when to run each layer.

Run commands:
```

pytest -m unit
pytest -m integration
pytest -m "unit or integration"
pytest -m lint

```

Refer back to `.github/instructions/rules.instructions.md` for the overall workflow guidelines.