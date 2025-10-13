from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Serve static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# /rain endpoint

from fastapi import Query, HTTPException
import requests
from typing import Optional
import random


@app.get("/rain")
def rain(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    horizon: int = Query(24, description="Forecast horizon in hours (default: 24)")
):
    # Query Open-Meteo API for hourly precipitation probability and precipitation
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "precipitation_probability,precipitation",
        "forecast_days": 1,
        "timezone": "auto"
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail="Weather API error")

    # Extract relevant data for the requested horizon (hours)
    precip_prob = data.get("hourly", {}).get("precipitation_probability", [])[:horizon]
    precip_mm = data.get("hourly", {}).get("precipitation", [])[:horizon]
    max_prob = max(precip_prob) if precip_prob else 0
    total_mm = sum(precip_mm) if precip_mm else 0

    # Rain logic per specification
    if max_prob > 60 or total_mm > 0.5:
        condition = "rain"
        will_rain = True
    elif 30 < max_prob <= 60:
        condition = "maybe"
        will_rain = False
    else:
        condition = "no_rain"
        will_rain = False

    # Placeholder messages (to be replaced by messages.json in later phase)
    messages = {
        "rain": ["YES. Bring an umbrella.", "Rain’s coming. Don’t say I didn’t warn you."],
        "no_rain": ["Nope. Dry as your sense of humor.", "You’re safe. For now."],
        "maybe": ["Maybe. The clouds are indecisive.", "Unclear. Flip a coin."]
    }
    message = random.choice(messages[condition])

    return {
        "will_rain": will_rain,
        "condition": condition,
        "message": message,
        "lat": lat,
        "lon": lon,
        "horizon": horizon
    }

@app.get("/", response_class=HTMLResponse)
def root():
    # Serve the placeholder landing page
    with open(static_dir / "index.html", "r", encoding="utf-8") as f:
        return f.read()
