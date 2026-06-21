# C-F2 — Hub redirect map (BUILD VERIFIED — Cursor)
Date: 2026-06-21T14:10:58
Backup: `outputs/backups/hubs-20260621-141057`

| Source | Target |
|--------|--------|
| `/blog/complete-family-financial-planning-ar.html` | `/finance.html` |
| `/blog/complete-family-financial-planning-en.html` | `/finance.html` |
| `/blog/complete-family-financial-planning.html` | `/finance.html` |
| `/blog/complete-family-systems-productivity-hub-ar.html` | `/productivity.html` |
| `/blog/complete-family-systems-productivity-hub-en.html` | `/productivity.html` |
| `/blog/complete-family-systems-productivity-hub.html` | `/productivity.html` |
| `/blog/complete-family-travel-activities-hub-ar.html` | `/travel.html` |
| `/blog/complete-family-travel-activities-hub-en.html` | `/travel.html` |
| `/blog/complete-family-travel-activities-hub.html` | `/travel.html` |
| `/blog/complete-gulf-family-financial-life-hub-ar.html` | `/finance.html` |
| `/blog/complete-gulf-family-financial-life-hub-en.html` | `/finance.html` |
| `/blog/complete-gulf-family-financial-life-hub.html` | `/finance.html` |
| `/blog/complete-gulf-family-health-wellness-ar.html` | `/health.html` |
| `/blog/complete-gulf-family-health-wellness-en.html` | `/health.html` |
| `/blog/complete-gulf-family-health-wellness.html` | `/health.html` |
| `/blog/complete-household-budget-system-ar.html` | `/finance-wealth/family-budget-plan.html` |
| `/blog/complete-household-budget-system-en.html` | `/finance-wealth/family-budget-plan.html` |
| `/blog/complete-household-budget-system.html` | `/finance-wealth/family-budget-plan.html` |
| `/blog/complete-islamic-lifestyle-guide-ar.html` | `/islamic.html` |
| `/blog/complete-islamic-lifestyle-guide-en.html` | `/islamic.html` |
| `/blog/complete-islamic-lifestyle-guide.html` | `/islamic.html` |

Hub files converted: **21**
Internal link replacements: **111**

## Verification
- No `adsbygoogle` in hub stubs
- `meta http-equiv="refresh"` + `location.replace` on each hub
- `grep -rl 'complete-family-financial-planning' --include='*.html'` should only hit redirect stubs / backups
