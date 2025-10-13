
# Will It Rain Today?

An interactive microservice that answers “Will it rain today?” for your location — fast, fun, and vibe-coded. Crafted with test-driven development and maximum test coverage for confidence.

## Features
- **FastAPI backend** with `/rain` endpoint (uses Open-Meteo, no API key required)
- **Static HTML frontend** (Tailwind CSS via CDN)
- **Geolocation**: Uses your browser to get your location (with fallback message if denied)
- **Live rain check**: Click the button to get a real-time answer for your location
- **Background color** changes based on rain condition (rain, maybe, no rain)
- **Humorous responses**
- **Fully responsive and centered UI**

## Usage
1. **Run the server:**
	```bash
	uvicorn app.main:app --host 0.0.0.0 --port 8000
	```
2. **Open your browser:**
	Go to [http://localhost:8000](http://localhost:8000)
3. **Click "Will it rain today?"**
	- Allow location access to get a personalized answer
	- If denied, you'll see a helpful fallback message

## Development
- **Backend:** `app/main.py` (FastAPI)
- **Frontend:** `app/static/index.html` (Tailwind, JS)
- **Tests:** `test/test_rain_endpoint.py` (pytest, all logic covered)
- **Memory:** `memory.md` (project state)
- **TODOs:** `TODO.md` (task tracking)
- **Instructions:** `.github/copilot-instructions.md` and `.github/instructions/rules.instructions.md`

## Architecture
- `/rain` endpoint: Accepts `lat`, `lon`, and optional `horizon` (hours). Returns JSON with rain status, condition, and a randomized message.
- Rain logic: If `precipitation_probability > 60` or `precipitation > 0.5mm`, returns "rain". If `30 < probability <= 60`, returns "maybe". Otherwise, returns "no_rain".
- Frontend: Uses Tailwind for layout and transitions, and updates background color per rain condition.

## References
- See `.github/copilot-instructions.md` for full architecture and workflow details.
