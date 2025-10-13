
## Project State (2025-10-13)

- FastAPI backend serves static frontend and implements `/rain` and `/geocode` endpoints.
- `/rain` endpoint: accepts `lat`, `lon`, and `horizon` ("today", "1h", "3h", "6h"). Returns rain status, message, and details. Fully integrated with Open-Meteo API and applies correct rain logic for the selected time window.
- `/geocode` endpoint: accepts `city` param, returns `{lat, lon, name}` using Open-Meteo geocoding API, with `language=auto` for best-effort international support.
- Manual city input and fallback for denied/missing geolocation are fully implemented in the frontend.
- **Time horizon control**: Users can select Today, 1h, 3h, or 6h forecast using a slider/stepper UI. Both frontend and backend support dynamic time window selection.
- Frontend and backend tested with multiple cities (including ambiguous and international names). Non-Latin scripts (e.g., Chinese, Cyrillic) are not supported by Open-Meteo; a disclaimer is shown to users.
- All Phase 5 TODOs are complete.

### Frontend MVP (Phase 5)
- Static HTML frontend uses Tailwind (via CDN) for modern layout and transitions
- Geolocation via `navigator.geolocation` with robust fallback for denied/missing location
- Fetches `/rain` endpoint and displays result with humor
- **Time horizon slider/stepper** for Today, 1h, 3h, 6h
- Background color updates per rain condition (rain, maybe, no_rain)
- All UI is centered and responsive
- All Phase 5 TODOs are complete
