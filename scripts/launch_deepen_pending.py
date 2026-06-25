#!/usr/bin/env python3
"""Launch the next pending DEEPEN batch from deepen-launch-queue.json."""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "operating-system/deepen-launch-queue.json"
TICKETS = ROOT / "operating-system/handoff-tickets.json"
REPORTS = ROOT / "operating-system/reports"
TS = datetime.now().strftime("%Y-%m-%d %H:%M")


def parse_pending_report(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(
            r"\|\s*(\d+)\s*\|\s*(D\d+-\d+)\s*\|\s*([^\|]+)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)w\s*\|",
            line,
        )
        if m:
            rows.append(
                {
                    "num": m.group(1),
                    "id": m.group(2),
                    "slug": m.group(3).strip(),
                    "url": m.group(4).strip(),
                    "words": int(m.group(5)),
                }
            )
    return rows


def section_from_url(url: str) -> str:
    return url.strip("/").split("/")[0]


def cards(batch_num: str, batch_article: str, slug: str, url: str, words: int, section: str):
    batch_key = f"deepen-{batch_num}"
    prefix = batch_article.rsplit("-", 1)[0]
    n, a, c = f"{batch_article}N", f"{batch_article}A", f"{batch_article}C"
    title = slug.replace("-", " ")
    return [
        {
            "id": n,
            "slug": slug,
            "kind": "deepen",
            "batch": batch_key,
            "batch_article": batch_article,
            "col": "hema_writing",
            "stage": "revise",
            "step_ar": "📝 تعميق",
            "skill": "writing",
            "owner": "Hema",
            "article": f"DEEPEN {prefix} — {title}",
            "reason": f"{prefix} · body ~{words}w · {section}",
            "url_path": url,
            "site_section": section,
            "law_ref": "operating-system/WRITING-LAW.md",
            "assignee": "Hema · سكيل الكتابة",
            "task": "DEEPEN/كتابة — ثم «انتهى من عندي»",
            "command": f"{n}: deepen — {slug}",
            "ts": TS,
        },
        {
            "id": a,
            "slug": slug,
            "kind": "deepen",
            "batch": batch_key,
            "batch_article": batch_article,
            "col": "amer",
            "stage": "review",
            "step_ar": "🛡️ بوابة",
            "owner": "عامر",
            "article": f"QA {prefix} — {title}",
            "url_path": url,
            "assignee": "Cursor acting QA",
            "task": "مراجعة amer-mandate",
            "command": f"{a}: Cursor acting QA — {slug}",
            "depends_on": n,
            "ts": TS,
        },
        {
            "id": c,
            "slug": slug,
            "kind": "deepen",
            "batch": batch_key,
            "batch_article": batch_article,
            "col": "cursor",
            "stage": "build",
            "step_ar": "⚙️ بناء",
            "owner": "Cursor",
            "article": f"TECH_BUILD {prefix} — {title}",
            "url_path": url,
            "assignee": "Cursor",
            "task": "بناء + صورة + push",
            "command": f"{c}: TECH_BUILD — {slug}",
            "depends_on": a,
            "ts": TS,
        },
    ]


def main():
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    pending = next((b for b in queue["pending_batches"] if b.get("status") == "pending"), None)
    if not pending:
        print("no pending batch")
        return

    batch_id = pending["batch_id"]
    report_path = ROOT / pending["report"]
    if not report_path.exists():
        raise SystemExit(f"missing report: {report_path}")

    articles = parse_pending_report(report_path)
    if len(articles) != pending["count"]:
        raise SystemExit(f"expected {pending['count']} articles, got {len(articles)}")

    data = json.loads(TICKETS.read_text(encoding="utf-8"))
    existing = {c["id"] for c in data["cards"]}
    added = 0
    batch_num = batch_id.replace("D", "")
    for row in articles:
        bid = row["id"]
        sec = section_from_url(row["url"])
        for card in cards(batch_num, bid, row["slug"], row["url"], row["words"], sec):
            if card["id"] in existing:
                continue
            data["cards"].append(card)
            existing.add(card["id"])
            added += 1

    live_name = f"deepen-batch-{batch_num}.md"
    live_report = REPORTS / live_name
    live_report.write_text(report_path.read_text(encoding="utf-8").replace("PENDING — 20 مقال (لا تُطلَق قبل D14)", f"launched {datetime.now().strftime('%Y-%m-%d')}"), encoding="utf-8")

    data["updated"] = datetime.now().strftime("%Y-%m-%d")
    data[f"deepen_batch_{batch_num}"] = {"launched": datetime.now().strftime("%Y-%m-%d"), "count": pending["count"]}
    TICKETS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pending["status"] = "launched"
    pending["launched_at"] = TS
    queue["updated"] = datetime.now().strftime("%Y-%m-%d")
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"batch": batch_id, "added_cards": added, "report": str(live_report)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
