# Tool 02 QA — Madinah Trip Planner · 2026-09-17

## Delivered
| Item | Path |
|------|------|
| Page | `makkah/tools/madinah-trip-planner/index.html` |
| Engine | `scripts/makkah/madinah-trip-planner-engine.js` |
| UI | `scripts/makkah/madinah-trip-planner-ui.js` |
| Shared reused | `scripts/makkah/planner-shared.js` · `styles/pages/makkah-trip-planner.css` |
| Wired | `/makkah/` · `/makkah/plan/` · `/makkah/tools/` · Tool 01 related link |

## Madinah-specific logic (not a rename of Tool 01)
- Arrival options include **From Makkah** (transfer-recovery day)
- Departure includes **Going to Makkah** / continue in KSA
- Calmer rest baseline (+1) + `quiet` interest
- Nabawi-oriented worship blocks; intentional flexible/empty hours on long stays
- Day titles and content reference Madinah rhythm

## Tests run
| Test | Result |
|------|--------|
| Engine 8 input cases | **PASS** |
| Plan A (active+history) ≠ Plan B (family+elderly+relaxed) | **PASS** |
| Adjustment → relaxed | **PASS** |
| Tool 01 regression (3-day generate) | **PASS** |
| No fatwa / invented distance / fee claims in sample outputs | **PASS** |
| Sitemap `/makkah/tools/madinah-trip-planner` | **PASS** |
| Routes regenerated | **PASS** |

## Analytics events
`madinah_planner_view|start|step_complete|complete|regenerate|share|copy|restart`

## Left for later
- Tools 03–05
- Live hotel geospatial
- LLM wording
- Browser visual RTL pass on production after deploy

## Assumptions
- Reuse Tool 01 CSS class family (`mtp`) for product consistency
- Form IDs use `mdp-` prefix; storage key `dfl-madinah-trip-plan`
- Directory URL `/makkah/tools/madinah-trip-planner/`
