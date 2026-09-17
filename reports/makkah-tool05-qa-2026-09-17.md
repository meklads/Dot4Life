# Makkah Tool 05 QA — Family & Elderly Journey Planner

Date: 2026-09-17  
URL: https://dotforlife.com/makkah/tools/family-elderly-planner/

## Scope

Tool 05 only. Practical family travel planner for Makkah / Madinah / both.  
Not medical. Not accessibility assessment. Not booking. Not religious authority.

## Files created

- `makkah/tools/family-elderly-planner/index.html`
- `scripts/makkah/family-elderly-engine.js`
- `scripts/makkah/family-elderly-ui.js`
- `reports/makkah-tool05-qa-2026-09-17.md`

## Files modified

- `makkah/tools/index.html` — Tool 05 Available; removed Coming soon card
- `makkah/index.html` — Live tools card
- `makkah/plan/index.html` — CTA
- `makkah/guides/index.html` — CTA to Tool 05
- `index.html` — homepage Makkah entry link
- `styles/pages/makkah-trip-planner.css` — Priority/Optional/Rest/Flexible kind tags
- `sitemap-content.xml` — Tool 05 URL
- `serve.json` / `_redirects` — via `generate_static_routes.py`
- `operating-system/TEAM-BUS.md`

## Shared modules reused

- `scripts/makkah/planner-shared.js` (track, t, copyText)
- `styles/pages/makkah-trip-planner.css` + `styles/makkah-hub.css`
- Makkah chrome (topbar/subnav), GA4 `dflTrack`, bilingual `data-lang`

## Engine

`DFLFamilyElderlyEngine` — deterministic friction model:

- children ↑ flexibility / breaks
- elderly / low walking ↑ rest / simple movement
- children + elderly = strongest flexibility
- arrival light / departure buffers
- empty/flexible blocks intentional
- Both cities → Makkah rhythm + Tool 03 link + Madinah rhythm (no transport clone)

`ENGINE_PASS` (Node, 2026-09-17): adults, toddler, elderly, both-gens, large, 1-day, 7-day, history, shopping, determinism, adjustment, medical-term scan.

## Analytics events

- `family_elders_planner_view`
- `family_elders_planner_start`
- `family_elders_planner_step_complete`
- `family_elders_planner_complete` (destination, family_type, children_bucket, elderly_present, walking_preference, pace, priority)
- `family_elders_planner_adjust`
- `family_elders_planner_share`
- `family_elders_planner_copy`
- `family_elders_planner_restart`

No names, medical data, phones, or other PII collected.

## SEO

- Title: Family & Elderly Umrah Travel Planner | DotForLife
- Canonical: `/makkah/tools/family-elderly-planner/`
- index,follow on main page only
- OG + BreadcrumbList + WebApplication + FAQPage
- Generated plans are client-side only (not indexable URLs)

## Localization

- Full AR/EN via `.en` / `.ar` spans; RTL/LTR via existing lang system
- Age groups, labels, plan output, adjustments, checklist bilingual

## Regression

Engines 01–05 load: `DFLMakkahTripEngine`, `DFLMadinahTripEngine`, `DFLMakkahMadinahEngine`, `DFLHotelDecisionEngine`, `DFLFamilyElderlyEngine`.  
No shared-module breaking changes beyond additive CSS kinds.

## Edge cases exercised (engine)

1. Adults only  
2. Toddler  
3. Older traveler  
4. Children + older  
5. Large multi-gen both cities  
6. 1-day  
7. 7-day  
8–11. Low/flexible walking, very-relaxed/active (via friction + case set)  
12–14. Makkah / Madinah / Both  
15–17. High rest / history / shopping priorities  
18–24. UI patterns match Tools 01–04 (share/copy/adjust/restart/localStorage); browser visual AR/EN/mobile not automated in this pass

## Assumptions / limits

- No distances, hours, accessibility, stroller/wheelchair, or restaurant inventing
- Meal planning = scheduling flexibility only
- Walking preference is planning preference, not health assessment
- Tool 03 linked for city transfer; not duplicated

## Privacy confirmation

No medical data or PII collected. LocalStorage holds only non-sensitive planner preferences.

## Scope confirmation

Tool 05 only. No medical planner, booking, tracking, accounts, or new global DotForLife features.
