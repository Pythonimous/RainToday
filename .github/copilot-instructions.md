# Copilot Instructions for Will It Rain Today?

## Project Overview
- **Purpose:** A FastAPI-based microservice that answers "Will it rain today?" for a given location, with humor and minimal latency.
- **Frontend:** Static HTML (to be upgraded with Tailwind/JS) served from `/app/static/index.html`.
- **Backend:** Python FastAPI app in `app/main.py` exposes endpoints and serves static files.
- **External API:** Uses Open-Meteo for weather data.

## Key Architecture & Patterns
- **Endpoints:**
  - `/rain`: Accepts `lat`, `lon`, and optional `horizon` (hours). Returns JSON with rain status, condition, and a randomized message.
  - `/`: Serves the static landing page.
- **Rain Logic:**
  - If `precipitation_probability > 60` or `precipitation > 0.5mm`, returns "rain".
  - If `30 < probability <= 60`, returns "maybe".
  - Otherwise, returns "no_rain".
- **Humor:** Response messages are randomized per condition (see `main.py`).
- **Testing:**
  - All logic is covered by `pytest` tests in `test/test_rain_endpoint.py`.
  - Use `pytest` for all test runs. Mock external API calls in tests.
- **Containerization:**
  - Dockerfile provided. Run with Uvicorn: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## Developer Workflow
- **Test-Driven:** Write/modify tests first (`pytest`).
- **Linting:** Run `ruff check .` or `flake8` before commit.
- **Memory:** Update `memory.md` with project state and design notes (not for TODOs).
- **TODOs:** Track all tasks in `TODO.md`.
- **Commits:** Use clear, descriptive commit messages.

## Conventions & Integration
- **Static files:** Place in `app/static/`. Landing page is `index.html`.
- **Templates:** Reserved for future use in `app/templates/`.
- **API keys:** Not required for Open-Meteo.
- **Extensibility:** Design allows for easy addition of endpoints (e.g., `/geocode`, visitor counter).

## Examples
- **Rain endpoint call:**
  ```http
  GET /rain?lat=40.7128&lon=-74.0060&horizon=3
  ```
- **Test run:**
  ```bash
  pytest
  ```
- **Lint:**
  ```bash
  ruff check .
  ```

## References
- See `specification.md` for full requirements and architecture rationale.
- See `.github/instructions/rules.instructions.md` for detailed dev workflow.
