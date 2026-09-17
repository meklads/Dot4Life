# Tool 03 QA — Makkah → Madinah Planner · 2026-09-17

## Delivered
| Item | Path |
|------|------|
| Page | `makkah/tools/makkah-to-madinah-planner/index.html` |
| Engine | `scripts/makkah/makkah-madinah-engine.js` |
| UI | `scripts/makkah/makkah-madinah-ui.js` |
| Shared reused | `planner-shared.js` · `makkah-trip-planner.css` · Makkah chrome |
| Wired | `/makkah/` · `/makkah/tools/` · `/makkah/move/` · Tool 01/02 related |

## Transfer-specific logic
- Door-to-door stages: prepare → depart → travel → arrive → settle
- Mode scoring: train / private car / bus (qualitative; no fares/times)
- Honors user transport preference without claiming objective “best”
- Luggage / children / elderly / walking / pace / priority / flexibility adapt checklists
- Adjustment chips: simpler · comfort · flexibility · family · luggage

## Tests run
| Test | Result |
|------|--------|
| Engine 8 input cases | **PASS** |
| Plan variation (light/active vs family/elderly/heavy) | **PASS** |
| Adjustment luggage | **PASS** |
| Tool 01 regression | **PASS** |
| Tool 02 regression | **PASS** |
| No invented SAR/times/guarantees in sample output | **PASS** |
| Sitemap + routes include tool | **PASS** |

## Analytics
`makkah_madinah_planner_view|start|step_complete|complete|adjust|share|copy|restart`

## Assumptions
- Official note links to SAR homepage as a general current-info pointer (not embedded schedules)
- No live transport APIs
- Form IDs use `mmp-` prefix; storage `dfl-makkah-madinah-plan`

## Left for later
- Tools 04–05
- Live schedule/fare integration (out of scope)
- Browser visual RTL pass after deploy
