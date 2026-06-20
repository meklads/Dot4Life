# Homepage Design v1 — Baseline (Frozen)

> **Status:** LOCKED · **Date:** 2026-06-20 · **Git tag:** `v1` · **Commit:** `3757e8c`

Any change to homepage layout, section order, column law, or bilingual direction rules **after this point** requires explicit approval and should bump to `v2`.

---

## Scope

Applies to `index.html` and homepage CSS layers ending with `styles/home-tickets-unified.css` (authoritative).

---

## Canvas & spacing

- Page background: white (`--dfl-page-bg: #ffffff`)
- Max content width: `1260px` · gutter `24px` · gap `24px`
- Section vertical rhythm: halved (`--dfl-section-y` ~ `clamp(1.25rem, 2.5vw, 1.75rem)`)
- No grey section bands · no «تجربتك اليومية» label on featured

---

## Hero

- Dark green gradient · headline **white** (EN + AR)
- **EN:** Libre Franklin · **AR:** Almarai
- Subcopy + trust line: white at 88% / 72% opacity

---

## Featured Stories (قصص مميزة)

- **4-column grid** (Verywell skeleton)
- Row 1: Hero cols 1–2 (~50%) · What's New col 3 (~25%) · Promo col 4 (~25%)
- Row 1 heights: stretch-aligned (equal ticket height)
- Row 2: four equal cards on same 4 tracks
- Images: hero 3:2 · promo framed 6:5 · cards 3:2
- Header scroll: natural green gradient (not flat `#054241`)

---

## Decisions & Comparisons (مقارنات وقرارات)

| Language | Layout |
|----------|--------|
| **Arabic** | Title above grid · sidebar **left** (38%) · articles **right** (62%) · RTL inside cards |
| **English** | Title inside **right sidebar** · articles **left** (~65%) · Verywell divider list rows |

---

## Latest Articles (جديد المقالات والأدلة)

- **4 equal columns** on desktop — all tickets identical (image top, text below)
- **No oversized first card** · no horizontal hero card in feed
- Tablet: 2 cols · Mobile: 1 col

---

## Typography (English site-wide on homepage)

- Headlines: Libre Franklin · Body/meta: Merriweather palette via `typography-en.css`
- Ink `#1a313c` · teal kicker `#1a5e73`

---

## CSS load order (homepage)

Last wins: `home-tickets-unified.css` — do not regress older flex/grid layers without updating unified file.

### Pinned cache busters (v1)

| Asset | Query |
|-------|-------|
| `global.css` | `?v=20260624t` |
| `home-tickets-unified.css` | `?v=20260624t` |
| `home-refined.css` | `?v=20260624t` |

---

## Restore command

```bash
git checkout v1 -- index.html styles/home-tickets-unified.css styles/typography-en.css styles/home-refined.css styles/home-section-bands.css styles/home.css
```

See `operating-system/homepage-design-v1.json` for full file manifest.
