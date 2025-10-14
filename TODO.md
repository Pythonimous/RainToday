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

* [x] Create `data/messages.json`.
* [x] Load messages in backend.
* [x] Select random message per condition.
* [x] Return message via `/rain`.
* [x] Display message prominently.
* [x] Verify messages update without code changes.

**Deliverable:** Dynamic, externalized humor messages.

---

## Phase 7. Test Suite Refactor and Integration Testing

**Goal:** Reorganize existing tests into clear categories and formalize integration testing structure.

* [x] Create structured testing layout:

  ```
  tests/
  ├── unit/
  ├── integration/
  └── e2e/          # (empty for now, to be used in Phase 8)
  ```
* [x] Move existing tests into appropriate folders:

  * **`unit/`** → tests that validate single functions or small components in isolation (no HTTP calls).
  * **`integration/`** → tests that call API endpoints or combine multiple components.
* [x] Update import paths and fixtures to reflect new folder structure.
* [x] Add a `conftest.py` at the root of `tests/` to share fixtures (e.g. FastAPI `TestClient`).
* [x] Use `pytest.mark.integration` and `pytest.mark.unit` markers to distinguish test types.
* [x] Verify all existing tests run after reorganization (`pytest -m "unit or integration"`).
* [x] Add one or two new **explicit integration tests** for `/rain` and `/geocode` endpoints to confirm proper separation.
* [x] Update `README.md` with test structure and example commands:

  ```
  pytest -m unit
  pytest -m integration
  ```
* [x] Update `.github/instructions/development.instructions.md` with new testing classification (see below).
* [x] Add linting/layered CI enforcement details once process stabilizes.

**Deliverable:** Structured and categorized test suite distinguishing unit and integration layers.

---

## Phase 8. End-to-End Testing

**Goal:** Introduce automated browser-based end-to-end tests using Playwright to verify critical user flows and backend integration.

* [x] Set up Playwright testing environment (`pip install playwright pytest-playwright`).
* [x] Run `playwright install` to install browser drivers.
* [x] Create `tests/e2e/` directory and add basic Playwright configuration.
* [x] Write initial tests for key flows:

  * Fetching `/rain` endpoint via frontend interaction.
  * Handling of geolocation permission granted/denied.
  * Manual city input fallback.
  * Slider (time horizon) control behavior.
  * Message display and background color switch.
* [x] Implement utility for test data or mock API responses if needed.
* [x] Integrate Playwright tests into the existing `pytest` workflow.
* [x] Add an E2E section to the `README.md` describing how to run tests.
* [x] Run all E2E tests locally and fix any failing cases.

**Deliverable:** Functional Playwright setup verifying main user scenarios end-to-end.

---

## Phase 9. Visitor Counter and Persistence

**Goal:** Track and show visits across deployments.

* [x] Implement persistent storage (SQLite with `data/stats.db`).
* [x] Increment `total_visits` and `today_visits`.
* [x] Create `/stats` endpoint (read-only).
* [x] Create `/visit` endpoint (increment and return counts).
* [x] Display counts on frontend.
* [x] Ensure atomic writes with SQLite transactions.
* [x] Test count persistence across restarts (integration tests).
* [x] Refactor API: separate read and increment endpoints for cleaner design.

**Deliverable:** Working, persistent visit counter with clean API separation.

---

## Phase 10. UI and Visual Enhancements

**Goal:** Improve visuals and polish. Thoroughly discuss all the changes with the user throughout.

* [x] Rearrange the UI elements to make it make more logical from a user flow standpoint. — Auto-geolocation on load, collapsible refine panel.
* [x] Add color themes and subtle animations. — Default indigo accent, fade-in animations, panel transitions.
* [x] Use responsive design. — Responsive layout maintained from previous phases.
* [x] Add transition effects for result display. — fadeInUp animation, smooth panel transitions.
* [x] Create footer with visit count and credits. — Footer with visit counts already in place from Phase 9.

**Deliverable:** Polished, visually dynamic UI with auto-geolocation and collapsible controls.

---

## Phase 11. Time Zone and Localization

**Goal:** Ensure local “today” correctness.

* [ ] Convert UTC to local timezone on backend.
* [ ] Adjust query range for local date boundaries.
* [ ] Validate daylight saving handling.
* [ ] Prepare basic i18n structure.

**Deliverable:** Accurate “today” handling in all timezones.

---

## Phase 12. Deployment and Domain Setup

**Goal:** Deploy and make public.

* [ ] Build Docker image and push to Lightsail.
* [ ] Deploy container service.
* [ ] Attach domain `willitrain.today`.
* [ ] Configure HTTPS and redirects for other domains.
* [ ] Validate uptime and latency.

**Deliverable:** Production-ready public deployment.

---

## Phase 13. Optional / Stretch Goals

* [ ] Improve database concurrency handling: Implement async write queue or connection pool to reduce "database is locked" errors under high concurrent load. Current 1s timeout with fail-fast strategy works for typical usage but could be optimized for production scale.
* [ ] Fix geolocation timeout mechanism: The app's 7-second timeout doesn't fire before browser permission denial. When geolocation hangs or is slow, browsers call the error callback with PERMISSION_DENIED instead of letting the app's timeout trigger. This affects both manual testing and E2E tests. Consider adjusting timeout logic or handling this browser behavior differently.
* [ ] Caching to minimize repeated API calls.
* [ ] Lightweight analytics (Plausible / GoatCounter).
* [ ] Social media shareable image.
* [ ] Multi-language support.
* [ ] Persistent user preferences.
* [ ] Animated weather icons or subtle effects.