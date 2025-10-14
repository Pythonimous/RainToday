

# Will It Rain Today?

An interactive FastAPI app that answers “Will it rain today?” for your location or any city — quick, simple, and fun.

## Features
- FastAPI backend: `/rain`, `/geocode`, `/stats`, `/visit` (uses Open-Meteo; no API key)
- Static HTML frontend (Tailwind via CDN)
- Geolocation with graceful fallback to manual city search
- Time horizon control: Today, 1h, 3h, 6h
- Background color reflects rain condition (rain/maybe/no_rain)
- Humorous responses from `data/messages.json` (hot-reloaded)
- Visit counter with SQLite persistence (`data/stats.db`)

## Quick start
1) Run the server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
2) Open http://localhost:8000 and allow location (or use the Refine panel to search a city).

## Project layout
- Backend: `src/main.py`
- Frontend: `src/static/index.html`
- Services: `src/services/`
- Persistence: `src/db.py` (SQLite at `data/stats.db`)
- Messages: `data/messages.json`
- Tests: `tests/{unit,integration,e2e}` (+ `tests/lint/test_flake8.py`)

## Testing
Use the helper script:
```bash
./scripts/run_tests.sh unit          # Unit tests only
./scripts/run_tests.sh integration   # Integration tests only
./scripts/run_tests.sh fast          # Unit + integration
./scripts/run_tests.sh coverage      # Coverage report (htmlcov)
./scripts/run_tests.sh all           # Lint + types + unit + integration
./scripts/run_tests.sh e2e           # Playwright E2E (starts server if needed)
./scripts/run_tests.sh full          # Everything including E2E
```
Common one-liners:
- Lint: `pytest -m lint`
- Types: `mypy .`
- Unit: `pytest -m unit`
- Integration: `pytest -m integration`
- Coverage: `pytest -m "unit or integration" --cov=src --cov-report=html`
- E2E (manual):
  - Start: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
  - Run:   `pytest -m e2e`

## API snapshot
- GET `/rain`: `lat`, `lon`, `horizon` in {today, 1h, 3h, 6h} → `{will_rain, condition, message, ...}`
- GET `/geocode`: `city` → `{lat, lon, name}`
- GET `/stats`: visit counters (no mutation)
- POST `/visit`: increments and returns counters

Rain logic: probability > 60% or precipitation > 0.5mm → `rain`; 30% < probability ≤ 60% → `maybe`; else `no_rain`.

## Docs & notes
- User flows index: `docs/user_flows/index.md`
- Specification: `specification.md`
- Project memory: `memory.md`
- Tasks: `TODO.md`
- Dev/testing guidelines: `.github/instructions/development.instructions.md`, `.github/instructions/testing.instructions.md`
