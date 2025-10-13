from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json


messages_path = Path(__file__).parent.parent / "data" / "messages.json"
def load_messages():
    try:
        with open(messages_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Fallback to default messages if file missing or invalid
        return {
            "rain": ["YES. Bring an umbrella."],
            "no_rain": ["Nope. Dry as your sense of humor."],
            "maybe": ["Maybe. The clouds are indecisive."]
        }

messages = load_messages()

app = FastAPI()

# Serve static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# /rain endpoint


from fastapi import Query, HTTPException
import requests
from typing import Optional
import random


# /geocode endpoint
@app.get("/geocode")
def geocode(city: str = Query(..., description="City name to geocode")):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "auto", "format": "json"}
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail="Geocoding API error")
    results = data.get("results", [])
    if not results:
        raise HTTPException(status_code=404, detail="City not found")
    result = results[0]
    return {"lat": result["latitude"], "lon": result["longitude"], "name": result.get("name", city)}



@app.get("/rain")
def rain(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    horizon: str = Query("today", description="Forecast horizon: today, 1h, 3h, 6h")
):
    # Map horizon string to number of hours
    horizon_map = {
        "today": 24,
        "1h": 1,
        "3h": 3,
        "6h": 6
    }
    hours = horizon_map.get(horizon, 24)

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
    precip_prob = data.get("hourly", {}).get("precipitation_probability", [])[:hours]
    precip_mm = data.get("hourly", {}).get("precipitation", [])[:hours]
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


    # Use messages loaded from messages.json
    global messages
    # Reload messages on every request to allow live updates without restart
    messages = load_messages()
    message = random.choice(messages.get(condition, ["No message available."]))

    return {
        "will_rain": will_rain,
        "condition": condition,
        "message": message,
        "lat": lat,
        "lon": lon,
        "horizon": horizon,
        "hours": hours
    }

@app.get("/", response_class=HTMLResponse)
def root():
    # Serve the placeholder landing page
    with open(static_dir / "index.html", "r", encoding="utf-8") as f:
        return f.read()
