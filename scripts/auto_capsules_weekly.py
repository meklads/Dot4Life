#!/usr/bin/env python3
"""
Dot4Life Capsule Autopilot — weekly buffer refill with strict D4L rules.

Reads data/capsule-rules.json + data/capsule-templates.json,
extends data/capsules-published.json when fewer than minDaysAhead remain.

Usage:
  python3 scripts/auto_capsules_weekly.py          # refill if needed
  python3 scripts/auto_capsules_weekly.py --force  # always add 7 days
  python3 scripts/auto_capsules_weekly.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'capsules-published.json'
RULES_PATH = ROOT / 'data' / 'capsule-rules.json'
TEMPLATES_PATH = ROOT / 'data' / 'capsule-templates.json'
CONFIG_PATH = ROOT / 'scripts' / 'dfl-config.js'
RIYADH = ZoneInfo('Asia/Riyadh')
ARABIC_RE = re.compile(r'[\u0600-\u06FF]')


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def today_riyadh() -> date:
    return datetime.now(RIYADH).date()


def slug_of(entry: dict) -> str:
    if entry.get('slug'):
        return entry['slug']
    title = entry.get('title_en', '')
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:48]


def validate_capsule(entry: dict, rules: dict) -> list[str]:
    errs: list[str] = []
    v = rules['validation']
    for field in ('title_en', 'title_ar', 'subtitle_en', 'subtitle_ar',
                  'body_en', 'body_ar', 'tip_en', 'tip_ar', 'category', 'emoji'):
        if not (entry.get(field) or '').strip():
            errs.append(f'missing {field}')
    if entry.get('category') not in v['allowedCategories']:
        errs.append(f"invalid category {entry.get('category')}")
    if len((entry.get('body_en') or '')) < v['minBodyLength']:
        errs.append('body_en too short')
    if len((entry.get('body_ar') or '')) < v['minBodyLength']:
        errs.append('body_ar too short')
    if v.get('requireArabicScript') and not ARABIC_RE.search(entry.get('title_ar', '')):
        errs.append('title_ar lacks Arabic script')
    return errs


def is_ramadan_season(d: date) -> bool:
    """Approximate Ramadan windows — extend manually or via rules in future."""
    # 2026 Ramadan ~ Feb 18 – Mar 19 (approximate; adjust yearly)
    windows = [
        (date(2026, 2, 18), date(2026, 3, 19)),
        (date(2027, 2, 8), date(2027, 3, 9)),
    ]
    return any(start <= d <= end for start, end in windows)


def recent_slugs(by_date: dict[str, dict], before: date, window: int) -> set[str]:
    slugs: set[str] = set()
    for ds, cap in by_date.items():
        try:
            d = date.fromisoformat(ds)
        except ValueError:
            continue
        if before - timedelta(days=window) <= d < before:
            slugs.add(slug_of(cap))
    return slugs


def week_faith_count(by_date: dict[str, dict], week_start: date) -> int:
    count = 0
    for i in range(7):
        ds = (week_start + timedelta(days=i)).isoformat()
        cap = by_date.get(ds)
        if cap and cap.get('category') == 'faith':
            count += 1
    return count


def preferred_categories(d: date, rules: dict) -> list[str]:
    wd = str(d.weekday())
    prefs = rules['weekdayPreferredCategories'].get(wd, rules['validation']['allowedCategories'])
    if is_ramadan_season(d):
        seasonal = rules.get('seasonal', {})
        if d.weekday() in seasonal.get('ramadanPreferOnWeekdays', []):
            return ['meals'] + [c for c in prefs if c != 'meals']
    return prefs


def pick_template(
    d: date,
    templates: list[dict],
    by_date: dict[str, dict],
    rules: dict,
    used_slugs_this_batch: set[str],
) -> dict | None:
    dedup = rules['dedup']
    window = dedup['slugWindowDays']
    blocked = recent_slugs(by_date, d, window) | used_slugs_this_batch

    week_start = d - timedelta(days=d.weekday())
    faith_budget = dedup['maxFaithPerWeek'] - week_faith_count(by_date, week_start)

    prev_cat = None
    prev_ds = (d - timedelta(days=1)).isoformat()
    if prev_ds in by_date:
        prev_cat = by_date[prev_ds].get('category')

    prefs = preferred_categories(d, rules)
    ramadan = is_ramadan_season(d)

    def score(t: dict) -> tuple:
        s = slug_of(t)
        if s in blocked:
            return (-999, 0, 0, s)
        cat = t['category']
        pref_rank = prefs.index(cat) if cat in prefs else len(prefs) + 1
        ramadan_bonus = 0
        if ramadan and 'ramadan' in (t.get('tags') or t.get('seasonal') or []):
            ramadan_bonus = -2
        consecutive_penalty = 5 if cat == prev_cat else 0
        faith_penalty = 8 if cat == 'faith' and faith_budget <= 0 else 0
        return (-pref_rank - ramadan_bonus + consecutive_penalty + faith_penalty, pref_rank, hash(s) % 1000, s)

    ranked = sorted(templates, key=score, reverse=True)
    best = ranked[0] if ranked else None
    if not best or score(best)[0] <= -100:
        # fallback: any non-blocked
        for t in templates:
            if slug_of(t) not in blocked and t['category'] != prev_cat:
                return t
        for t in templates:
            if slug_of(t) not in blocked:
                return t
        return None
    return best


def make_capsule(d: date, template: dict, idx: int) -> dict:
    ds = d.isoformat()
    cid = f"cap_{ds.replace('-', '')}_{idx:02d}"
    return {
        'id': cid,
        'slug': slug_of(template),
        'category': template['category'],
        'emoji': template['emoji'],
        'title_en': template['title_en'],
        'title_ar': template['title_ar'],
        'subtitle_en': template['subtitle_en'],
        'subtitle_ar': template['subtitle_ar'],
        'body_en': template['body_en'],
        'body_ar': template['body_ar'],
        'tip_en': template['tip_en'],
        'tip_ar': template['tip_ar'],
        'source': 'autopilot',
        'generated_at': datetime.now(RIYADH).isoformat(timespec='seconds'),
    }


def rebuild_by_id(by_date: dict[str, dict]) -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    for cap in by_date.values():
        by_id[cap['id']] = cap
    return by_id


def prune_old(by_date: dict[str, dict], keep_days: int, today: date) -> dict[str, dict]:
    cutoff = today - timedelta(days=keep_days)
    return {
        ds: cap for ds, cap in by_date.items()
        if date.fromisoformat(ds) >= cutoff
    }


def days_ahead(by_date: dict[str, dict], today: date) -> int:
    future = [date.fromisoformat(ds) for ds in by_date if ds >= today.isoformat()]
    if not future:
        return 0
    return (max(future) - today).days


def bump_config_version(today: date) -> bool:
    if not CONFIG_PATH.exists():
        return False
    text = CONFIG_PATH.read_text(encoding='utf-8')
    ver = today.strftime('%Y%m%d') + 'a'
    new_text, n = re.subn(
        r"(DFL\.capsulesJsonVersion\s*=\s*')[^']+(')",
        rf"\g<1>{ver}\2",
        text,
        count=1,
    )
    if n:
        CONFIG_PATH.write_text(new_text, encoding='utf-8')
        return True
    return False


def run(force: bool = False, dry_run: bool = False) -> int:
    rules = load_json(RULES_PATH)
    tpl_file = load_json(TEMPLATES_PATH)
    templates = tpl_file.get('templates') or tpl_file
    if isinstance(templates, dict):
        templates = list(templates.values())

    today = today_riyadh()
    buf = rules['buffer']
    min_ahead = buf['minDaysAhead']
    batch = buf['generateBatchSize']

    if OUT.exists():
        payload = load_json(OUT)
    else:
        payload = {'updated': today.isoformat(), 'mode': 'static', 'byDate': {}, 'byId': {}}

    by_date: dict[str, dict] = dict(payload.get('byDate') or {})
    ahead = days_ahead(by_date, today)

    if not force and ahead >= min_ahead:
        print(f'OK — {ahead} days ahead (min {min_ahead}). No generation needed.')
        return 0

    to_add = batch if not force else batch
    if not force and ahead < min_ahead:
        to_add = max(batch, min_ahead - ahead + 1)

    # Start after last scheduled date or today
    if by_date:
        last = max(date.fromisoformat(ds) for ds in by_date)
        cursor = max(last + timedelta(days=1), today)
    else:
        cursor = today

    created: list[str] = []
    used_slugs: set[str] = set()
    idx_base = 0

    for _ in range(to_add):
        ds = cursor.isoformat()
        if ds in by_date:
            cursor += timedelta(days=1)
            continue

        template = pick_template(cursor, templates, by_date, rules, used_slugs)
        if not template:
            print('ERROR: no template available — expand capsule-templates.json', file=sys.stderr)
            return 1

        cap = make_capsule(cursor, template, idx_base)
        errs = validate_capsule(cap, rules)
        if errs:
            print(f'ERROR: validation failed for {ds}: {errs}', file=sys.stderr)
            return 1

        by_date[ds] = cap
        used_slugs.add(slug_of(template))
        created.append(ds)
        idx_base = (idx_base + 1) % 100
        cursor += timedelta(days=1)

    by_date = prune_old(by_date, buf['maxPastDaysKept'], today)
    by_id = rebuild_by_id(by_date)

    payload['byDate'] = dict(sorted(by_date.items()))
    payload['byId'] = by_id
    payload['updated'] = today.isoformat()
    payload['mode'] = 'static'
    payload['autopilot'] = {
        'version': 1,
        'rulesVersion': rules.get('version', 1),
        'lastRun': datetime.now(RIYADH).isoformat(timespec='seconds'),
        'lastRunTz': 'Asia/Riyadh',
        'daysAhead': days_ahead(by_date, today),
        'createdDates': created,
        'templatePool': len(templates),
    }

    if dry_run:
        print(f'DRY RUN — would create {len(created)} capsules: {created}')
        print(f'  days ahead after: {payload["autopilot"]["daysAhead"]}')
        return 0

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    bump_config_version(today)
    print(f'Wrote {OUT} — added {len(created)} days: {", ".join(created)}')
    print(f'  buffer: {payload["autopilot"]["daysAhead"]} days ahead')
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description='Dot4Life capsule autopilot')
    ap.add_argument('--force', action='store_true', help='Generate batch even if buffer OK')
    ap.add_argument('--dry-run', action='store_true', help='Preview without writing')
    args = ap.parse_args()
    sys.exit(run(force=args.force, dry_run=args.dry_run))


if __name__ == '__main__':
    main()
