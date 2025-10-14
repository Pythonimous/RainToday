---
applyTo: "**"
---
# Testing Checklist

- Run `flake8` early or rely on `pytest -m lint` for the gate.
- Run `mypy .` and clear every reported issue.
- Use `pytest` for the full suite when confidence is needed.
- Scope to unit work with `pytest -m unit`; keep tests isolated and fast.
- Cover integrations via `pytest -m integration`; mock external services.
- Combine coverage with `pytest -m "unit or integration"` when reviewing.
- Execute `pytest -m e2e` only when end-to-end behavior must be proven.
- Align `pytest -m e2e` coverage with the flows listed in docs/user_flows/index.md; add scenarios when new UF files appear.
- Prefer `./scripts/run_tests.sh` for repeatable local runs.
- Launch `./scripts/run_e2e_tests.sh` when browser flows are required.
- Share fixtures through `tests/conftest.py` to avoid duplication.
- If end-to-end tests fail, ensure the server is running on port 8000. If it is offline, use `uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/uvicorn.log 2>&1 &` to start it in the background, and `pkill -f "uvicorn src.main:app"` to stop it.
