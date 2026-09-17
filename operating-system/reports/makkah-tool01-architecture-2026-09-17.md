# Tool 01 — Makkah Trip Planner · Audit + Architecture

> Date: 2026-09-17  
> Scope: **Tool 01 only** · URL `/makkah/tools/makkah-trip-planner/`  
> Status: **READY TO BUILD** after this check (no code shipped in this doc)

---

## 1) Codebase audit (what exists)

| Layer | Finding | Decision for Tool 01 |
|--------|---------|----------------------|
| Framework | Static HTML site (GitHub Pages + Cloudflare). No React/Vue app for content tools. | **Vanilla HTML + CSS + JS** — same as Return to Hotel / Qibla |
| Routing | Directory `index.html` under `/makkah/…` · CF strips `.html` | Create `makkah/tools/makkah-trip-planner/index.html` |
| Makkah vertical | Hub + Plan/Stay/Move/Experience/Tools/Guides live | Nest planner under Tools; keep vertical chrome |
| Design system | `makkah-hub.css` + `tools-shared` / `tools-flagship` | Extend with `styles/pages/makkah-trip-planner.css` · reuse mk-topbar/subnav |
| i18n | `data-lang` + `.en`/`.ar` spans + `lang-toggle` + `lang-redirect.js` | **Reuse** — no new i18n framework |
| Analytics | GA4 `G-3G1XPV4F0G` · `dflTrack` pattern on Return to Hotel | Add `dflTrack` + named events from prompt |
| Forms/stepper | No shared planner stepper component today | New small module under `scripts/makkah/` (reusable for Tools 02–05) |
| SEO utils | Manual canonical / OG / BreadcrumbList / FAQ JSON-LD | Same pattern as makkah hubs |
| Policy | Freeze exception active for `/makkah/` only · Batch 04 still blocked | Build allowed |

### Related live assets (link, do not rebuild)
- `/tools/return-to-hotel` — CTA from result when relevant  
- `/tools/qibla` — related tool link  
- Guides clustered on `/makkah/plan/` and `/makkah/guides/`  
- Placeholder card “Makkah Trip Planner · Coming soon” on `/makkah/tools/` → **upgrade to live link**

### Explicit non-goals (this build)
Madinah planner · Makkah→Madinah · Hotel Decision · Family/Elderly planner · homepage redesign · LLM API · accounts · booking

---

## 2) Target architecture

```
makkah/tools/makkah-trip-planner/
  index.html                 # shell + SEO + static content + #planner mount
styles/pages/
  makkah-trip-planner.css    # mobile-first stepper UI (uses makkah tokens)
scripts/makkah/
  planner-shared.js          # progress, option cards, storage helpers (reuse later)
  trip-planner-engine.js     # deterministic rules: inputs → day blocks
  trip-planner-ui.js         # steps, regenerate, share/copy, analytics hooks
```

### Data separation (for Tools 02–05 reuse)

| Module | Responsibility |
|--------|----------------|
| **Inputs** | `{ duration, arrival, departure, adults, children, elderly, walking, pace, interests[], lodging, hotelName?, startPref? }` |
| **Rules** | Pure functions → `{ days: [{ title, blocks: [{ slot, items[] }] }], summary, flags }` |
| **Content** | AR/EN strings for block templates (no invented hours/distances) |
| **UI** | Stepper only; never embeds rules |

### UX flow (≈60–90s)
`Trip → Group → Pace → Stay → Preferences → Plan → Adjust/Share`

### Indexability
- **Only** `/makkah/tools/makkah-trip-planner/` is `index,follow`  
- Share via hash/local non-sensitive state — **no** indexable result URLs  

### Analytics events
`makkah_planner_view|start|step_complete|complete|regenerate|share|copy|restart`  
(+ aggregate duration / pace / group bucket — no PII)

---

## 3) Planning engine (deterministic MVP)

**Inputs that change output:** duration, arrival/departure, kids, elderly+walking, pace, interests, lodging.

**Hard rules:** light arrival day · buffered departure · more rest if kids/elderly/low walking · no minute-by-minute · no fatwas · no fabricated distances/hours · worship blocks stay generic.

**Adjust controls after generate:** More relaxed / More active / More family / More shopping / More history — mapped to rule deltas, not random regen.

---

## 4) Integration checklist (when building)

1. Create planner page + CSS + 3 JS modules  
2. Wire live card on `/makkah/tools/` (remove Coming soon for Tool 01 only)  
3. CTA on `/makkah/` and `/makkah/plan/`  
4. Related links: Return to Hotel, Qibla, family/elderly guides  
5. Regenerate `_redirects` / sitemap via existing scripts  
6. QA: AR/EN · mobile · combinations · events · no regression on hub/qibla/hotel  

---

## 5) Risks & mitigations

| Risk | Mitigation |
|------|------------|
| Generic “same plan for everyone” | Fixture matrix of ≥8 input combos in QA |
| Thin hub copy around tool | Static How it works / Who it’s for / Tips on page |
| Scope creep into other 4 tools | Shared `planner-shared.js` only; no extra routes |
| SEO explosion | Single canonical; no result URLs |

---

## 6) Verdict

**Architecture fit: GO.**  
Stack, routing, Makkah chrome, i18n, analytics, and freeze exception all support Tool 01 as a **static interactive utility** under `/makkah/tools/makkah-trip-planner/`.

No blocker. Next step when you say **نفذ**: implement Tool 01 only per this plan.
