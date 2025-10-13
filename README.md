

# Will It Rain Today?

An interactive microservice that answers “Will it rain today?” for your location or any city — fast, fun, and vibe-coded. Crafted with test-driven development and maximum test coverage for confidence.

## Features
- **FastAPI backend** with `/rain` and `/geocode` endpoints (uses Open-Meteo, no API key required)
- **Static HTML frontend** (Tailwind CSS via CDN)
- **Geolocation**: Uses your browser to get your location (with fallback to manual city input)
- **Manual city search**: Enter any city name to check rain status anywhere in the world
- **Live rain check**: Click the button or search to get a real-time answer
- **Time horizon control**: Choose between Today, 1h, 3h, or 6h forecast using a slider/stepper
- **Background color** changes based on rain condition (rain, maybe, no rain)
- **Humorous responses**: Now fully externalized in `data/messages.json` for easy editing and live updates
- **Live message updates**: Edit `data/messages.json` and see new messages instantly, no backend restart required
- **Fully responsive and centered UI**
- **Multi-city and international support** (Latin/English names recommended)

## Usage
1. **Run the server:**
	```bash
	uvicorn app.main:app --host 0.0.0.0 --port 8000
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
- **Backend:** `app/main.py` (FastAPI)
- **Frontend:** `app/static/index.html` (Tailwind, JS)
- **Tests:** `tests/` (pytest, all logic and endpoints covered)
- **Memory:** `memory.md` (project state)
- **TODOs:** `TODO.md` (task tracking)
- **Instructions:** `.github/copilot-instructions.md` and `.github/instructions/rules.instructions.md`


## Architecture
- `/rain` endpoint: Accepts `lat`, `lon`, and `horizon` ("today", "1h", "3h", or "6h"). Returns JSON with rain status, condition, and a **randomized humorous message** (from `data/messages.json`).
- `/geocode` endpoint: Accepts `city` param, returns `{lat, lon, name}` for manual city search (uses Open-Meteo geocoding).
- Rain logic: If `precipitation_probability > 60` or `precipitation > 0.5mm`, returns "rain". If `30 < probability <= 60`, returns "maybe". Otherwise, returns "no_rain".
- **Humor messages are externalized**: You can edit `data/messages.json` to add, remove, or change responses for each condition. Changes are reflected instantly in the API and frontend.
- Frontend: Uses Tailwind for layout and transitions, updates background color per rain condition, and supports both geolocation and manual city search. The humorous message is displayed prominently in the result area.


## Data
- `data/messages.json`: Contains all humorous responses for each rain condition. Edit this file to update or add new messages. No backend restart required.

## References
- See `.github/copilot-instructions.md` for full architecture and workflow details.
