# Makkah & Madinah — Premium Integration QA

Date: 2026-09-17  
Scope: Brand integration + visual unification (not tool-engine redevelopment)

## A. Before / After

**Before:** Isolated `mk-topbar` / `mk-footer`, internal “vertical / Tool 01–05 / six doors / Live now” language, cream mini-site look separate from DotForLife.

**After:** Real DotForLife `#navbar` + mobile menu + `.site-footer` on all 12 Makkah pages; specialized `mk-subnav` subordinate; public name **Makkah & Madinah / مكة والمدينة**; premium hub with photo hero, planners, situation cards, tools hierarchy; breadcrumbs; contextual exit block before global footer.

## B. Files modified

- `makkah/index.html` (rebuild)
- `makkah/plan|stay|move|experience|tools|guides/index.html`
- `makkah/tools/*/index.html` (5 planners)
- `styles/makkah-hub.css` (rewrite for global chrome)
- `index.html` (nav/footer/mobile label + entry copy)
- `travel.html`, `islamic.html` (subnav label)
- `partials/header.html`, `partials/mobile-dropdown.html`, `partials/footer.html`
- `operating-system/TEAM-BUS.md`

## C. Files created

- `partials/makkah-global-header.html`
- `partials/makkah-subnav.html`
- `partials/makkah-global-footer.html`
- `scripts/makkah_apply_chrome.py`
- `reports/makkah-brand-integration-2026-09-17.md`

## D. Shared components reused

- Exact DotForLife header pattern (`#navbar`, `#mobile-dropdown`, lang/theme/hamburger IDs)
- Exact DotForLife `.site-footer` structure
- `global.css`, `home.css` (nav sizing), `global.js`
- Existing hero asset `/assets/images/hero-mecca-medina.webp`

## E. Global site changes

- Nav/footer/mobile label: **Makkah → Makkah & Madinah / مكة والمدينة**
- Homepage Makkah entry copy cleaned (no “dedicated room”)
- Travel + Islamic subnav labels updated
- Partials updated for future sync

## F. Makkah changes

- Chrome swap on all 12 pages
- Hub rebuilt as editorial + utility landing
- Tools index: destination planners vs supporting tools; no Tool 01–05
- Eyebrows / footers cleaned of internal language
- Breadcrumbs on child pages

## G. URL changes

None. All `/makkah/...` URLs preserved.

## H. SEO

- Hub title: `Makkah & Madinah — Practical Guides & Travel Tools | DotForLife`
- Canonical unchanged
- Breadcrumb schema updated to “Makkah & Madinah”
- OG image points to destination photo

## I. Mobile / RTL QA

- Structure verified: global hamburger IDs present; subnav horizontal scroll; bilingual spans intact
- Visual browser pass of AR RTL / EN LTR on live deploy deferred until Pages publish; local HTML/CSS reviewed for RTL-safe properties (`inline-end`, no LTR-only absolute chrome)

## J. Regression QA

- All 5 planner engines still load (`ENGINE` keys present)
- Tool HTML retains form roots + engine/ui scripts
- Chrome assertions: `navbar` + `site-footer` + `mk-subnav` on 12/12 pages
- Bad-copy scan: no `vertical` / `Tool 0` / `Coming soon` / `six doors` / `specialist room` in makkah HTML

## K. Remaining issues

- Live visual check after Cloudflare Pages deploy (header height + sticky subnav on real devices)
- Other pillar hubs (health/finance) main nav may still lack Makkah until a separate sync_mobile_chrome run — only homepage + partials + travel/islamic subnav were updated by design
