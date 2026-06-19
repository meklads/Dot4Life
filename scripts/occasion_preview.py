#!/usr/bin/env python3
"""
Print active Dot4Life occasions for a date (debug / calendar review).

Usage:
  python3 scripts/occasion_preview.py
  python3 scripts/occasion_preview.py 2026-07-15
  python3 scripts/occasion_preview.py --days 14
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from auto_capsules_weekly import (  # noqa: E402
    active_occasions,
    load_json,
    load_all_templates,
    pick_template,
    primary_occasion,
    today_riyadh,
    OCCASIONS_PATH,
)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('start', nargs='?', help='Start date YYYY-MM-DD (default: today Riyadh)')
    ap.add_argument('--days', type=int, default=7, help='Number of days to preview')
    args = ap.parse_args()

    start = date.fromisoformat(args.start) if args.start else today_riyadh()
    _, occasions_cfg = load_all_templates()
    templates, _ = load_all_templates()
    by_date: dict = {}

    print(f'Occasions preview from {start} ({args.days} days)\n')
    for i in range(args.days):
        d = start + timedelta(days=i)
        active = active_occasions(d, occasions_cfg)
        primary = primary_occasion(d, occasions_cfg)
        tpl = pick_template(d, templates, by_date, load_json(ROOT / 'data' / 'capsule-rules.json'), occasions_cfg, set())
        names = ', '.join(o['id'] for o in active) or '—'
        title = tpl['title_en'] if tpl else 'NO TEMPLATE'
        occ_id = primary['id'] if primary else '—'
        print(f'{d.isoformat()}  [{occ_id}]  {names}')
        print(f'  → {title}')
        if tpl:
            by_date[d.isoformat()] = {'id': 'preview', 'category': tpl['category']}

if __name__ == '__main__':
    main()
