# Will It Rain Today? — Software Specification (PRD)

## 1. Overview

**Project Name:** Will It Rain Today?  
**Type:** Single-page weather microservice  
**Goal:** A lightweight, humorous, single-click web app that tells the user whether it will rain soon or today, with configurable time horizons, minimal latency, and a clean aesthetic.  

The application detects the user’s geolocation, retrieves forecast data from a free weather API, and returns a funny, context-aware message (“YES”, “NO”, “MAYBE”) along with a dynamic background or themed visual. Users can also refine their location manually and check different time horizons.  

---

## 2. Objectives

- Provide an instant, low-friction way to check if it will rain.
- Keep backend and frontend lightweight and independent.
- Maintain a playful “vibe” while ensuring technical reliability and scalability.
- Enable later extensions (custom APIs, caching, analytics, etc.) without major refactors.

---

## 3. System Architecture

**Frontend:**  
- Static site (HTML + Tailwind CSS + JavaScript).  
- Served from FastAPI static mount or a CDN.  
- Responsible for location request, user input, and rendering API response.  

**Backend:**  
- FastAPI (Python) containerized and deployed on AWS Lightsail.  
- Handles all API interactions (weather data, message generation, visitor counters).  
- Communicates with an external weather API (e.g., Open-Meteo).  
- Stores persistent visitor counters in a lightweight storage backend (SQLite or S3-hosted JSON).  

**Deployment:**  
- AWS Lightsail container service.  
- Domain: `willitrain.today` (canonical), with redirects from other purchased domains.  

---

## 4. Functional Requirements

### 4.1 Core Features

| Feature | Description | Priority |
|----------|--------------|----------|
| **Main Button** | A button labeled “Will it rain today?” that triggers geolocation acquisition and API call. | High |
| **Geolocation Detection** | Obtain latitude/longitude via browser API. Fallback to manual location input if denied. | High |
| **Manual Location Input** | Allow user to type a city name; backend geocodes it via Open-Meteo geocoding or Nominatim. | Medium |
| **Weather Query** | Backend queries weather API for precipitation probability/amount for the user’s location and chosen time horizon. | High |
| **Time Horizon Selection** | Slider or stepper control to select horizon (“Today”, “1h”, “3h”, “6h”). | High |
| **Response Message** | Display randomized, pre-defined funny message corresponding to result (“YES”, “NO”, “MAYBE”). | High |
| **Response Visuals** | Background color or CSS animation changes based on rain result. | Medium |
| **Visitor Counter** | Display total and daily visit counts. Persistent across deployments. | Medium |

---

## 5. Functional Details

### 5.1 User Flow
1. User opens page.  
2. Browser requests geolocation permission.  
3. If granted, latitude/longitude are sent to backend.  
4. Backend determines:
   - Local date based on coordinates (user’s timezone).  
   - Forecast data for selected time horizon.  
   - Rain status (rain / no rain / uncertain).  
   - Random humorous message from external message set.  
5. Frontend displays:
   - Message in large type.  
   - Matching background color or animation.  
   - Visitor count.  

### 5.2 Message System
- Message templates stored in a separate file (`messages.json`).  
- Structure:
  ```json
  {
    "rain": ["YES. Bring an umbrella.", "Rain’s coming. Don’t say I didn’t warn you."],
    "no_rain": ["Nope. Dry as your sense of humor.", "You’re safe. For now."],
    "maybe": ["Maybe. The clouds are indecisive.", "Unclear. Flip a coin."]
  }
````

* Backend selects random message from category corresponding to computed rain condition.

### 5.3 Weather Decision Logic

* Backend evaluates precipitation probability and total precipitation:

  ```python
  if precip_prob > 60 or precip_mm > 0.5:
      condition = "rain"
  elif 30 < precip_prob <= 60:
      condition = "maybe"
  else:
      condition = "no_rain"
  ```
* Horizon control adjusts which time window is queried.
* “Today” queries the next 24 hours (local to user).

### 5.4 Visitor Counter

* Persistent storage (SQLite or JSON file).
* Schema:

  ```python
  {
    "total_visits": 12345,
    "daily": {
        "2025-10-10": 542
    }
  }
  ```
* Updated per visit (once per unique session).
* Displayed in page footer.

---

## 6. API Endpoints

| Endpoint   | Method | Parameters              | Description                                   |         |                          |
| ---------- | ------ | ----------------------- | --------------------------------------------- | ------- | ------------------------ |
| `/rain`    | GET    | `lat`, `lon`, `horizon` | Returns JSON: `{ rain: bool, condition: "rain | no_rain | maybe", message: str }`. |
| `/geocode` | GET    | `city`                  | Returns `{ lat, lon }` from text query.       |         |                          |
| `/stats`   | GET    | —                       | Returns `{ total_visits, today_visits }`.     |         |                          |

---

## 7. Non-Functional Requirements

| Category            | Requirement                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| **Performance**     | Response time < 500 ms (excluding weather API latency).                            |
| **Reliability**     | Graceful fallback if geolocation or weather API fails.                             |
| **Scalability**     | Container-based; horizontal scaling possible on Lightsail.                         |
| **Maintainability** | Messages, thresholds, and API endpoints configurable via external files.           |
| **Security**        | CORS restricted to allowed origins; no user data retention beyond location lookup. |
| **Compliance**      | GDPR-friendly (no tracking, anonymized analytics).                                 |

---

## 8. UI Specifications

### 8.1 Layout

* Single centered button and slider.
* Large, animated “YES” / “NO” / “MAYBE” text result.
* Visitor counter at bottom right.
* Optional footer with credits and source link.

### 8.2 Colors / Themes

| Condition | Background               | Text  |
| --------- | ------------------------ | ----- |
| Rain      | Gradient blue            | White |
| No rain   | Pale yellow              | Black |
| Maybe     | Gray / shifting gradient | White |

---

## 9. Data Sources

* **Weather API:** Open-Meteo (`https://api.open-meteo.com/v1/forecast`)
* **Geocoding API:** Open-Meteo geocoding or Nominatim.
* **Storage:** Local SQLite or persistent JSON file (mounted Lightsail volume).

---

## 10. Future Extensions

* Hourly chart or minimal visual of forecast.
* API rate limiting / caching layer.
* Social sharing (“Tell your friends it’s raining”).
* Persistent user preferences (cookies / local storage).
* Localization for multiple languages.
* Self-hosted statistics dashboard (e.g., Plausible integration).
