# Tool 04 QA — Makkah Hotel Decision Tool · 2026-09-17

## Delivered
| Item | Path |
|------|------|
| Page | `makkah/tools/hotel-decision/index.html` |
| Engine | `scripts/makkah/hotel-decision-engine.js` |
| UI | `scripts/makkah/hotel-decision-ui.js` |
| Shared | `planner-shared.js` · `makkah-trip-planner.css` |
| Wired | `/makkah/` · `/makkah/tools/` · `/makkah/stay/` |

## Verified hotel data
**None in project.** Mode B uses **manual traits only** (access/family/value/comfort as user-declared). Missing → “Not available”. No invented prices/distances.

## Modes
- **A — Decision profile:** stay type + prioritize + why + checklist
- **B — Compare ≤3 hotels:** fit-for-your-trip labels from user-entered traits only

## Tests run
| Test | Result |
|------|--------|
| Engine 7 input cases | **PASS** |
| Category variation | **PASS** |
| Manual compare (incl. unknown) | **PASS** |
| Adjustment | **PASS** |
| Tools 01–03 regression | **PASS** |
| No fabricated SAR/meters/rankings | **PASS** |
| Sitemap + routes | **PASS** |

## Analytics
`hotel_decision_view|start|step_complete|complete|adjust|compare|share|copy|restart`

## Left for Tool 05
Family / Elderly Planner only.

## Assumptions
- Editorial hotel guides linked; no live inventory/API
- Commercial ranking/affiliates not implemented (architecture remains neutral)
