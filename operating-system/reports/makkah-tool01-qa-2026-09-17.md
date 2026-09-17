# Tool 01 QA — Makkah Trip Planner · 2026-09-17

## Delivered
| Item | Path |
|------|------|
| Page | `makkah/tools/makkah-trip-planner/index.html` |
| CSS | `styles/pages/makkah-trip-planner.css` |
| Shared | `scripts/makkah/planner-shared.js` |
| Engine | `scripts/makkah/trip-planner-engine.js` |
| UI | `scripts/makkah/trip-planner-ui.js` |
| Wired | `/makkah/` · `/makkah/plan/` · `/makkah/tools/` |

## Tests run
| Test | Result |
|------|--------|
| Engine 5 input combos (1d relaxed, 5d active+shop/history, 3d kids, 3d elderly low walk, lt1 airport) | **PASS** — blocks present, plans differ |
| Adjustment → relaxed | **PASS** |
| No fatwa / invented distance / fee claims in output JSON | **PASS** |
| HTML canonical + scripts + 6 panels | **PASS** |
| Sitemap includes `/makkah/tools/makkah-trip-planner` | **PASS** |
| Routes regenerated | **PASS** |

## Analytics events (wired)
`makkah_planner_view|start|step_complete|complete|regenerate|share|copy|restart`

## Left for later
- Tools 02–05
- Live hotel geospatial
- LLM wording
- Browser visual RTL pass on production after deploy (code supports `data-lang`)

## Assumptions
- Static stack (no React) per DotForLife convention
- Directory URL `/makkah/tools/makkah-trip-planner/`
- Deterministic rules only
