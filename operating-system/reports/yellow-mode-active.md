# 🟡 YELLOW MODE — Cursor Interim Command (Active)
> **Activated:** 2026-06-21 · **Owner:** Ghost (Joost) — explicit delegation: «استلام مكانه وتشغيل الفريق والحلقة»
> **Reason:** Amer session limit (~4h until reset 6pm Asia/Riyadh)
> **Ends when:** Amer returns + ACK handback, or Ghost `LOOP RESUME GREEN`
> **UI:** [`system/gsystem.html`](/system/gsystem.html) (GSystem — read-only dashboard)

## Who leads what (interim)
| Role | Interim owner | Allowed | Forbidden |
|------|---------------|---------|-----------|
| **Command / BUILD VERIFY (objective)** | **Cursor** | Gate checks, proof bundle, board updates | Subjective text re-approval |
| **TECH_BUILD** | **Cursor** | FIFO on pre-approved queue | Homepage v1 changes |
| **Text APPROVED (new)** | **Amer** (frozen) | — | No new APPROVED without Amer or `EMERGENCY APPROVE [id]` from Ghost |
| **LIVE / AdSense / v1** | **Ghost** | Release when READY | — |
| **Drafts (Ship/Hema)** | **Hema** | Queue drafts A-09+ in `drafts/` only | HTML, schema, publish |

## Current loop state (as of activation)
| Item | Track | State |
|------|-------|-------|
| 1–2 | A-01 investment + budget | **BUILD VERIFIED ✅** (Ghost delegation + Cursor objective v3 ALL PASS) |
| 3 | A-07 rent-vs-buy | **TECH_BUILD ✅** → AUTO-VERIFIED pending Amer spot-check |
| 4 | A-07 oman-property-roi | **BLOCKED** — page is calculator shell; needs surgical inject, not full template replace |
| 5–16 | various | QUEUE — TECH_BUILD after 3–4 |

## Gates enforced (Cursor)
- C-F4: `grep -c "—"` = 0 on every built HTML
- Article + FAQPage JSON-LD + hreflang + WebP hero + alt + og:image
- `scripts/build-from-approved-draft.py` fails build if em-dash present

## Handback to Amer
When Amer returns:
1. Spot-check BUILD VERIFIED 1–2 + AUTO-VERIFIED 3
2. Confirm or REOPEN with specific line refs
3. Post `ACK HANDOFF` on this file → GREEN mode

## Team ping (copy to Hema)
> YELLOW MODE active. Continue **drafts only** for A-09+. No HTML. No new submissions for APPROVED until Amer back unless Ghost EMERGENCY APPROVE.
