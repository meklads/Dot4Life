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
OCCASIONS_PATH = ROOT / 'data' / 'capsule-occasions.json'
OCCASION_TPL_PATH = ROOT / 'data' / 'capsule-occasion-templates.json'
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


def template_tags(t: dict) -> set[str]:
    tags = set(t.get('tags') or [])
    tags.update(t.get('seasonal') or [])
    return tags


def is_forbidden_template(t: dict, forbidden: set[str]) -> bool:
    return bool(template_tags(t) & forbidden)


def load_all_templates() -> tuple[list[dict], dict]:
    tpl_file = load_json(TEMPLATES_PATH)
    base = tpl_file.get('templates') or tpl_file
    if isinstance(base, dict):
        base = list(base.values())
    extra: list[dict] = []
    if OCCASION_TPL_PATH.exists():
        occ_file = load_json(OCCASION_TPL_PATH)
        extra = occ_file.get('templates') or []
    # occasion templates first in pool so they compete fairly
    merged = extra + list(base)
    occasions_cfg = load_json(OCCASIONS_PATH) if OCCASIONS_PATH.exists() else {}
    return merged, occasions_cfg


def active_occasions(d: date, occasions_cfg: dict) -> list[dict]:
    active: list[dict] = []
    for occ in occasions_cfg.get('occasions') or []:
        for r in occ.get('ranges') or []:
            try:
                start = date.fromisoformat(r['start'])
                end = date.fromisoformat(r['end'])
            except (KeyError, ValueError, TypeError):
                continue
            if start <= d <= end:
                active.append(occ)
                break
    if not active:
        return []
    priority = occasions_cfg.get('priorityWhenOverlapping') or []
    rank = {oid: i for i, oid in enumerate(priority)}
    active.sort(key=lambda o: rank.get(o.get('id', ''), 999))
    return active


def primary_occasion(d: date, occasions_cfg: dict) -> dict | None:
    active = active_occasions(d, occasions_cfg)
    return active[0] if active else None


def occasion_match_score(t: dict, active: list[dict]) -> int:
    if not active:
        return 0
    tags = template_tags(t)
    score = 0
    for i, occ in enumerate(active):
        occ_tags = set(occ.get('templateTags') or [])
        if occ.get('id') in tags:
            score += 12 - i * 2
        overlap = tags & occ_tags
        if overlap:
            score += (8 - i) * len(overlap)
    return score


def preferred_categories(d: date, rules: dict, occasions_cfg: dict) -> list[str]:
    occ = primary_occasion(d, occasions_cfg)
    if occ and occ.get('preferredCategories'):
        base = list(occ['preferredCategories'])
        wd = str(d.weekday())
        weekday = rules['weekdayPreferredCategories'].get(wd, [])
        for c in weekday:
            if c not in base:
                base.append(c)
        return base
    wd = str(d.weekday())
    return rules['weekdayPreferredCategories'].get(
        wd, rules['validation']['allowedCategories']
    )


def max_faith_for_week(d: date, rules: dict, occasions_cfg: dict) -> int:
    week_start = d - timedelta(days=d.weekday())
    extra = rules['dedup']['maxFaithPerWeek']
    for i in range(7):
        day = week_start + timedelta(days=i)
        for occ in active_occasions(day, occasions_cfg):
            if occ.get('maxFaithPerWeek'):
                extra = max(extra, int(occ['maxFaithPerWeek']))
    return extra


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


def pick_template(
    d: date,
    templates: list[dict],
    by_date: dict[str, dict],
    rules: dict,
    occasions_cfg: dict,
    used_slugs_this_batch: set[str],
) -> dict | None:
    dedup = rules['dedup']
    window = dedup['slugWindowDays']
    blocked = recent_slugs(by_date, d, window) | used_slugs_this_batch
    forbidden = set(occasions_cfg.get('forbiddenTags') or [])

    week_start = d - timedelta(days=d.weekday())
    faith_budget = max_faith_for_week(d, rules, occasions_cfg) - week_faith_count(by_date, week_start)

    prev_cat = None
    prev_ds = (d - timedelta(days=1)).isoformat()
    if prev_ds in by_date:
        prev_cat = by_date[prev_ds].get('category')

    prefs = preferred_categories(d, rules, occasions_cfg)
    active = active_occasions(d, occasions_cfg)

    def score(t: dict) -> tuple:
        s = slug_of(t)
        if s in blocked or is_forbidden_template(t, forbidden):
            return (-999, 0, 0, s)
        cat = t['category']
        pref_rank = prefs.index(cat) if cat in prefs else len(prefs) + 1
        occ_bonus = occasion_match_score(t, active)
        consecutive_penalty = 5 if cat == prev_cat else 0
        faith_penalty = 8 if cat == 'faith' and faith_budget <= 0 else 0
        total = occ_bonus * 3 - pref_rank + consecutive_penalty + faith_penalty
        return (total, occ_bonus, -pref_rank, s)

    ranked = sorted(templates, key=score, reverse=True)
    best = ranked[0] if ranked else None
    if not best or score(best)[0] <= -100:
        for t in templates:
            if is_forbidden_template(t, forbidden):
                continue
            if slug_of(t) not in blocked and t['category'] != prev_cat:
                return t
        for t in templates:
            if is_forbidden_template(t, forbidden):
                continue
            if slug_of(t) not in blocked:
                return t
        return None
    return best


def make_capsule(d: date, template: dict, idx: int, occasions_cfg: dict) -> dict:
    ds = d.isoformat()
    cid = f"cap_{ds.replace('-', '')}_{idx:02d}"
    cap = {
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
    occ = primary_occasion(d, occasions_cfg)
    if occ:
        cap['occasion'] = occ['id']
        cap['occasion_ar'] = occ.get('label_ar', '')
        cap['occasion_en'] = occ.get('label_en', '')
    return cap


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


def refresh_future_occasions(
    by_date: dict[str, dict],
    templates: list[dict],
    rules: dict,
    occasions_cfg: dict,
    today: date,
) -> list[str]:
    """Re-pick autopilot capsules from today onward that predate occasion support."""
    refreshed: list[str] = []
    for ds in sorted(by_date.keys()):
        if ds < today.isoformat():
            continue
        cap = by_date[ds]
        if cap.get('occasion') or cap.get('source') not in ('autopilot', None, 'generator'):
            continue
        d = date.fromisoformat(ds)
        used = {slug_of(by_date[k]) for k in by_date if k != ds and by_date[k].get('slug')}
        tpl = pick_template(d, templates, by_date, rules, occasions_cfg, used)
        if not tpl:
            continue
        idx = int(ds.replace('-', '')[-2:]) if ds[-2:].isdigit() else 0
        by_date[ds] = make_capsule(d, tpl, idx % 100, occasions_cfg)
        refreshed.append(ds)
    return refreshed


def run(force: bool = False, dry_run: bool = False, refresh: bool = False) -> int:
    rules = load_json(RULES_PATH)
    templates, occasions_cfg = load_all_templates()

    today = today_riyadh()
    buf = rules['buffer']
    min_ahead = buf['minDaysAhead']
    batch = buf['generateBatchSize']

    if OUT.exists():
        payload = load_json(OUT)
    else:
        payload = {'updated': today.isoformat(), 'mode': 'static', 'byDate': {}, 'byId': {}}

    by_date: dict[str, dict] = dict(payload.get('byDate') or {})

    if refresh:
        refreshed = refresh_future_occasions(by_date, templates, rules, occasions_cfg, today)
        if refreshed and not dry_run:
            by_id = rebuild_by_id(by_date)
            payload['byDate'] = dict(sorted(by_date.items()))
            payload['byId'] = by_id
            payload['updated'] = today.isoformat()
            payload['autopilot'] = {
                'version': 2,
                'rulesVersion': rules.get('version', 1),
                'lastRun': datetime.now(RIYADH).isoformat(timespec='seconds'),
                'lastRunTz': 'Asia/Riyadh',
                'daysAhead': days_ahead(by_date, today),
                'refreshedDates': refreshed,
                'templatePool': len(templates),
                'occasionsEnabled': True,
            }
            OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            bump_config_version(today)
            print(f'Refreshed {len(refreshed)} future capsules with occasion rules: {", ".join(refreshed)}')
        elif refreshed:
            print(f'DRY RUN — would refresh: {", ".join(refreshed)}')
        elif not force:
            print('No future capsules to refresh.')

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

        template = pick_template(cursor, templates, by_date, rules, occasions_cfg, used_slugs)
        if not template:
            print('ERROR: no template available — expand capsule-templates.json', file=sys.stderr)
            return 1

        cap = make_capsule(cursor, template, idx_base, occasions_cfg)
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
        'occasionsEnabled': bool(occasions_cfg.get('occasions')),
        'occasionCount': len(occasions_cfg.get('occasions') or []),
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
    ap.add_argument('--refresh', action='store_true', help='Re-pick future autopilot capsules with occasion rules')
    args = ap.parse_args()
    sys.exit(run(force=args.force, dry_run=args.dry_run, refresh=args.refresh))


if __name__ == '__main__':
    main()
