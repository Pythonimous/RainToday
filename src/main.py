from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.db import get_visit_stats, increment_visits, init_db
from src.services.geocode import CityNotFoundError, GeocodeServiceError, search_city
from src.services.weather import WeatherServiceError, get_rain_forecast

app = FastAPI()

# Serve static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/geocode")
def geocode(city: str = Query(..., description="City name to geocode")) -> Dict[str, Any]:
    try:
        return search_city(city)
    except CityNotFoundError as exc:
        raise HTTPException(status_code=404, detail="City not found") from exc
    except GeocodeServiceError as exc:
        raise HTTPException(status_code=502, detail="Geocoding API error") from exc


@app.get("/rain")
def rain(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    horizon: str = Query("today", description="Forecast horizon: today, 1h, 3h, 6h")
) -> Dict[str, Any]:
    try:
        return get_rain_forecast(lat, lon, horizon)
    except WeatherServiceError as exc:
        raise HTTPException(status_code=502, detail="Weather API error") from exc


@app.get("/stats")
def get_stats() -> Dict[str, int]:
    return get_visit_stats()


@app.post("/visit")
def record_visit() -> Dict[str, int]:
    """
    Record a new visit by incrementing counters.
    Returns the updated visit statistics.
    """
    return increment_visits()


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    # Serve the placeholder landing page
    return (static_dir / "index.html").read_text(encoding="utf-8")
