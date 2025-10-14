

# Will It Rain Today?

An interactive microservice that answers “Will it rain today?” for your location or any city — fast, fun, and vibe-coded. Crafted with test-driven development and maximum test coverage for confidence.

## Features
- **FastAPI backend** with `/rain`, `/geocode`, `/stats`, and `/visit` endpoints (uses Open-Meteo, no API key required)
- **Static HTML frontend** (Tailwind CSS via CDN)
- **Geolocation**: Uses your browser to get your location (with fallback to manual city input)
- **Manual city search**: Enter any city name to check rain status anywhere in the world
- **Live rain check**: Click the button or search to get a real-time answer
- **Time horizon control**: Choose between Today, 1h, 3h, or 6h forecast using a slider/stepper
- **Background color** changes based on rain condition (rain, maybe, no rain)
- **Humorous responses**: Fully externalized in `data/messages.json` for easy editing and live updates
- **Live message updates**: Edit `data/messages.json` and see new messages instantly, no backend restart required
- **Visitor counter**: Tracks total and daily visits with SQLite persistence across server restarts
- **Fully responsive and centered UI**
- **Multi-city and international support** (Latin/English names recommended)

## Usage
1. **Run the server:**
	```bash
	uvicorn src.main:app --host 0.0.0.0 --port 8000
	```
2. **Open your browser:**
	Go to [http://localhost:8000](http://localhost:8000)
3. **Check the weather:**
	- Use the slider/stepper to select your forecast horizon: Today, 1h, 3h, or 6h
	- Click "Will it rain today?" and allow location access for a personalized answer
	- Or, enter a city name and click "Search" to check any location
	- If denied, you'll see a helpful fallback and can use manual search
	- _Note: For best results, use English or Latin city names. Non-Latin scripts (e.g., 中文, кириллица) may not be supported yet._

## Development
- **Backend:** `src/main.py` (FastAPI)
- **Frontend:** `src/static/index.html` (Tailwind, JS)
- **Tests:**
	- `tests/unit/` — Unit tests (no HTTP calls)
	- `tests/integration/` — Integration/API endpoint tests
	- `tests/e2e/` — End-to-end browser tests (Playwright)
	- `tests/conftest.py` — Shared fixtures
	- `tests/lint/test_flake8.py` — Lint gate ensuring the codebase stays flake8-clean
- **Guidelines:** `.github/instructions/development.instructions.md` (workflow, testing, lint/type policy)
- **Memory:** `memory.md` (project state)
- **TODOs:** `TODO.md` (task tracking)
- **Instructions:** `.github/copilot-instructions.md` and `.github/instructions/rules.instructions.md`

### Validation Checklist

### Quick Test Commands

Use the convenience script for common scenarios:
```bash
./scripts/run_tests.sh unit          # Unit tests only
./scripts/run_tests.sh integration   # Integration tests only
./scripts/run_tests.sh fast          # Unit + integration
./scripts/run_tests.sh coverage      # With coverage report
./scripts/run_tests.sh all           # Full validation (no E2E)
./scripts/run_tests.sh e2e           # E2E tests (requires server)
./scripts/run_tests.sh full          # Everything including E2E
```

### Individual Test Commands

- Lint gate:
	```bash
	pytest -m lint
	```
- Type checking:
	```bash
	mypy .
	```
- Unit tests:
	```bash
	pytest -m unit
	```
- Integration tests:
	```bash
	pytest -m integration
	```
- Tests with coverage:
	```bash
	pytest -m "unit or integration" --cov=app --cov-report=html
	```
- End-to-end tests (requires running server):
	```bash
	# Start the server in one terminal:
	uvicorn src.main:app --host 0.0.0.0 --port 8000
	
	# Run E2E tests in another terminal:
	pytest -m e2e
	
	# Or use the helper script (checks if server is running):
	./scripts/run_e2e_tests.sh [--headed] [--browser <chromium|firefox|webkit>]
	```
- Full test suite:
	```bash
	pytest
	```


## Architecture

### API Endpoints
- **`GET /rain`**: Accepts `lat`, `lon`, and `horizon` ("today", "1h", "3h", or "6h"). Returns JSON with rain status, condition, and a randomized humorous message (from `data/messages.json`).
- **`GET /geocode`**: Accepts `city` param, returns `{lat, lon, name}` for manual city search (uses Open-Meteo geocoding).
- **`GET /stats`**: Read-only endpoint that returns current visit statistics without incrementing counters.
- **`POST /visit`**: Records a new visit, increments counters, and returns updated statistics.

### Business Logic
- **Rain logic**: If `precipitation_probability > 60` or `precipitation > 0.5mm`, returns "rain". If `30 < probability <= 60`, returns "maybe". Otherwise, returns "no_rain".
- **Humor messages**: Externalized in `data/messages.json`. Edit this file to add, remove, or change responses for each condition. Changes are reflected instantly.
- **Visitor tracking**: SQLite database (`data/stats.db`) tracks total visits and daily visits. Counts persist across server restarts. Daily visits reset at midnight local time.

### Frontend
- Uses Tailwind for layout and transitions
- Updates background color per rain condition
- Supports both geolocation and manual city search
- Calls `POST /visit` on page load to record visit and display counts
- Displays humorous message prominently in result area


## Data
- **`data/messages.json`**: Contains all humorous responses for each rain condition. Edit this file to update or add new messages. No backend restart required.
- **`data/stats.db`**: SQLite database that persists visitor counts (total and daily). Automatically created on first run.

## References
- See `.github/copilot-instructions.md` for full architecture and workflow details.
