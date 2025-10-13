# Test Suite Structure

Tests are organized as follows:

```
tests/
├── unit/          # Isolated logic tests (no HTTP calls)
├── integration/   # API endpoint and multi-component tests
├── e2e/           # End-to-end browser tests (Playwright)
├── conftest.py    # Shared fixtures
```

## Running Tests

- **Unit tests:**
  ```
  pytest -m unit
  ```
- **Integration tests:**
  ```
  pytest -m integration
  ```
- **All tests:**
  ```
  pytest -m "unit or integration"
  ```

## Markers
- `@pytest.mark.unit` for unit tests
- `@pytest.mark.integration` for integration tests

See `.github/instructions/testing.instructions.md` for conventions.
