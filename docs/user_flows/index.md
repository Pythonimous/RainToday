# User Flow Index

Track end-to-end user journeys for this project. Each flow file uses the `UF-###` naming convention so automation can discover, diff, and test them.

> The scaffold ships without project-specific flows; downstream projects copy UF-000 and add their own entries below. Keep each file's front matter (`id`, `name`, `last_updated`, `status`) in sync with this table.

| ID | Name | Path | Summary | Status | Last Updated |
|----|------|------|---------|--------|--------------|
| UF-000 | Template | docs/user_flows/UF-000-template.md | Copy this file to seed project-specific user flows. | draft | 2025-10-14 |
| UF-001 | Initial Page Load | docs/user_flows/UF-001-initial-page-load.md | Landing page loads default UI and starts auto geolocation. | ready | 2025-10-14 |
| UF-100 | Auto-Check Geolocation on Page Load (Granted) | docs/user_flows/UF-100-auto-check-geolocation-on-page-load-granted.md | Auto geolocation runs after permission grant and shows weather. | ready | 2025-10-14 |
| UF-101 | Auto-Check Geolocation on Page Load (Denied) | docs/user_flows/UF-101-auto-check-geolocation-on-page-load-denied.md | Permission denial shows retry message and keeps refine panel closed. | ready | 2025-10-14 |
| UF-102 | Auto-Check Geolocation Timeout | docs/user_flows/UF-102-auto-check-geolocation-timeout.md | Timeout after seven seconds shows fallback manual search guidance. | in-progress | 2025-10-14 |
| UF-103 | Try Again After Initial Denial | docs/user_flows/UF-103-try-again-after-initial-denial.md | Try Again re-requests geolocation and displays a fresh result. | ready | 2025-10-14 |
| UF-200 | Manual City Search (Happy Path) | docs/user_flows/UF-200-manual-city-search-happy-path.md | Manual city search fetches geocode, calls rain endpoint, updates UI. | ready | 2025-10-14 |
| UF-201 | Manual City Search - Empty Input | docs/user_flows/UF-201-manual-city-search-empty-input.md | Empty manual search shows validation message and blocks API calls. | ready | 2025-10-14 |
| UF-202 | Manual City Search - City Not Found | docs/user_flows/UF-202-manual-city-search-city-not-found.md | Geocode failure shows error while keeping background unchanged. | ready | 2025-10-14 |
| UF-203 | Manual City Search - Special Characters | docs/user_flows/UF-203-manual-city-search-special-characters.md | Special character city names encode correctly and return weather. | ready | 2025-10-14 |
| UF-300 | Refine Panel - Toggle Open/Close | docs/user_flows/UF-300-refine-panel-toggle-open-close.md | Refine toggle and Escape control panel open and close states. | ready | 2025-10-14 |
| UF-301 | Refine Panel - Single Input Instance | docs/user_flows/UF-301-refine-panel-single-input-instance.md | Ensure refine panel renders only one city input element. | ready | 2025-10-14 |
| UF-302 | Horizon Slider - Label Update | docs/user_flows/UF-302-horizon-slider-label-update.md | Slider movement updates horizon label immediately for each value. | ready | 2025-10-14 |
| UF-303 | Horizon Slider - Affects Weather Query | docs/user_flows/UF-303-horizon-slider-affects-weather-query.md | Selected horizon value travels with rain request for accuracy. | ready | 2025-10-14 |
| UF-400 | Background Color - Rain Condition | docs/user_flows/UF-400-background-color-rain-condition.md | Rain forecast updates background to gray and shows rain message. | ready | 2025-10-14 |
| UF-401 | Background Color - No Rain Condition | docs/user_flows/UF-401-background-color-no-rain-condition.md | No-rain forecast updates background to blue with dry message. | ready | 2025-10-14 |
| UF-402 | Background Color - Maybe Condition | docs/user_flows/UF-402-background-color-maybe-condition.md | Maybe forecast updates background to yellow to convey uncertainty. | ready | 2025-10-14 |
| UF-403 | Background Color - Transitions Between Conditions | docs/user_flows/UF-403-background-color-transitions-between-conditions.md | Sequential checks swap background classes without leftover states. | ready | 2025-10-14 |
| UF-404 | Visit Counter Display | docs/user_flows/UF-404-visit-counter-display.md | Visit counts increment and display non-negative totals on load. | ready | 2025-10-14 |

## How to use
- Start here to locate the relevant flow ID and file path.
- Load the specific flow file before implementing or updating behavior.
- Update this table whenever you add, rename, or retire a flow. Keep the rows ordered by Flow ID.