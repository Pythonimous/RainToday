# Will It Rain Today? — TODO / Development Roadmap

## Phase 1. Setup and Environment

**Goal:** Establish a working local environment with a functional “Hello World” prototype.
* [x] Initialize Git repository and base project structure.
* [x] Create Python virtual environment and activate it.
* [x] Install dependencies (`fastapi`, `uvicorn`, `requests`).
* [x] Create `Dockerfile` and `.dockerignore`.
* [x] Implement minimal FastAPI server returning “Hello World”.
* [x] Serve simple placeholder landing page.
* [x] Test local server integration.

**Deliverable:** Functional prototype serving an HTML page.

---

## Phase 2. Weather Data Integration

**Goal:** Connect backend to a weather API and expose `/rain`.

* [x] Create `/rain` endpoint with parameters `lat`, `lon`, `horizon`.
* [x] Integrate Open-Meteo API.
* [x] Parse response, evaluate rain logic.
* [x] Return structured JSON.
* [x] Verify using test coordinates.

**Deliverable:** Working API returning correct rain condition.

---

## Phase 3. Frontend Prototype

**Goal:** Implement minimal client interaction.

* [x] Create Tailwind layout.
* [x] Add “Will it rain today?” button.
* [x] Implement `navigator.geolocation`.
* [x] Fetch `/rain` endpoint and display result.
* [x] Apply background color per condition.
* [x] Add fallback for denied geolocation.

**Deliverable:** Interactive MVP answering “Will it rain today?”.

---

## Phase 4. Location Refinement

**Goal:** Enable manual city input.

* [x] Add input field + “Search” button.
* [x] Implement `/geocode` endpoint using Open-Meteo geocoding.
* [x] Integrate fallback for missing geolocation.
* [x] Test multiple cities.

**Deliverable:** Manual location refinement working.

---

## Phase 5. Time Horizon Control

**Goal:** Add “Today / 1h / 3h / 6h” slider control.

* [x] Implement slider/stepper UI.
* [x] Extend `/rain` to handle horizon logic.
* [x] Query time range dynamically.
* [x] Display selected horizon.
* [x] Validate accuracy.

**Deliverable:** Functional time horizon selection.

---

## Phase 6. Response Messaging System

**Goal:** Introduce externalized humorous responses.

* [ ] Create `data/messages.json`.
* [ ] Load messages in backend.
* [ ] Select random message per condition.
* [ ] Return message via `/rain`.
* [ ] Display message prominently.
* [ ] Verify messages update without code changes.

**Deliverable:** Dynamic, externalized humor messages.

---

## Phase 7. Visitor Counter and Persistence

**Goal:** Track and show visits across deployments.

* [ ] Implement persistent storage (`data/stats.json` or SQLite).
* [ ] Increment `total_visits` and `today_visits`.
* [ ] Create `/stats` endpoint.
* [ ] Display counts on frontend.
* [ ] Ensure atomic writes.
* [ ] Test across restarts.

**Deliverable:** Working, persistent visit counter.

---

## Phase 8. UI and Visual Enhancements

**Goal:** Improve visuals and polish.

* [ ] Add color themes and subtle animations.
* [ ] Use responsive design.
* [ ] Add transition effects for result display.
* [ ] Create footer with visit count and credits.

**Deliverable:** Polished, visually dynamic UI.

---

## Phase 9. Time Zone and Localization

**Goal:** Ensure local “today” correctness.

* [ ] Convert UTC to local timezone on backend.
* [ ] Adjust query range for local date boundaries.
* [ ] Validate daylight saving handling.
* [ ] Prepare basic i18n structure.

**Deliverable:** Accurate “today” handling in all timezones.

---

## Phase 10. Deployment and Domain Setup

**Goal:** Deploy and make public.

* [ ] Build Docker image and push to Lightsail.
* [ ] Deploy container service.
* [ ] Attach domain `willitrain.today`.
* [ ] Configure HTTPS and redirects for other domains.
* [ ] Validate uptime and latency.

**Deliverable:** Production-ready public deployment.

---

## Phase 11. Optional / Stretch Goals

* [ ] Caching to minimize repeated API calls.
* [ ] Lightweight analytics (Plausible / GoatCounter).
* [ ] Social media shareable image.
* [ ] Multi-language support.
* [ ] Persistent user preferences.
* [ ] Animated weather icons or subtle effects.

```