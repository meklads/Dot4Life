#!/usr/bin/env python3
"""Wave 14 DEEPEN (EN): school-type-comparison + quiet-home guides."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


SCHOOL_BODY = r"""
<div class="container">

<h1>Private School vs Homeschool vs Islamic School: The Complete Family Guide</h1>

<p>Choosing how to educate your children is one of the most consequential decisions a family can make. For Muslim and values-driven families, the decision is not just academic—it’s also spiritual, cultural, and practical. You are not only choosing a curriculum; you are choosing a daily environment that will shape your child’s habits, friendships, identity, and relationship with faith.</p>

<p>This guide gives you a clear comparison of the three main options—private secular school, homeschooling, and Islamic school—across the real-world dimensions families in the Gulf and beyond care about: academic outcomes, character formation, cost, schedule flexibility, and the home’s emotional bandwidth.</p>

<div class="tip"><p><strong>Quick principle:</strong> Don’t start with the options. Start with your family’s priorities. Then pick the option that best serves those priorities <em>for this year</em>. You can reassess annually.</p></div>

<h2 id="the-big-three">The Big Three Options</h2>
<div class="table-wrap"><table>
<tr><th>Factor</th><th>Private School</th><th>Homeschool</th><th>Islamic School</th></tr>
<tr><td>Academic rigor</td><td>Often high</td><td>Variable (parent-dependent)</td><td>Moderate to high (varies)</td></tr>
<tr><td>Faith integration</td><td>Low</td><td>Maximum</td><td>High</td></tr>
<tr><td>Social environment</td><td>Broad exposure</td><td>Curated</td><td>Faith-aligned (ideally)</td></tr>
<tr><td>Cost</td><td>High</td><td>Lower (materials + time)</td><td>Moderate</td></tr>
<tr><td>Parent involvement</td><td>Lower day-to-day</td><td>High (daily)</td><td>Moderate</td></tr>
<tr><td>Flexibility</td><td>Limited</td><td>High</td><td>Medium</td></tr>
</table></div>

<h2 id="private-school">Option 1: Private Secular School</h2>
<p><strong>What it’s great for:</strong> consistent structure, strong facilities, advanced academics, and a predictable schedule. Many families choose private school when both parents work demanding jobs and need a reliable daily rhythm.</p>
<p><strong>Common risks:</strong> values drift and social pressures. The issue is usually not “bad teachers.” It’s the daily normalization of what your family may not want normalized: casual language, unfiltered media culture, and friendship circles that pull identity away from faith. If you choose private school, you must plan the “second curriculum” at home: Qur’an, adab, family conversation, and boundaries around screens.</p>
<p><strong>Practical check:</strong> Ask how the school handles bullying, online culture, and parent communication. A beautiful campus with weak discipline can be exhausting for families.</p>

<h2 id="homeschool">Option 2: Homeschooling</h2>
<p><strong>What it’s great for:</strong> deep customization, faith-centered learning, and emotional safety for a child who struggles in a loud or chaotic school environment. Homeschooling can also support travel seasons, health needs, or a child who learns faster or slower than the standard classroom pace.</p>
<p><strong>Common risks:</strong> parent burnout and social isolation—especially if homeschooling is attempted without a community. Homeschooling is not only “teaching.” It’s also logistics: materials, routines, discipline, and managing your own patience. If the home is already overwhelmed, homeschooling may add pressure rather than reduce it.</p>
<p><strong>Make it realistic:</strong> many families succeed with a hybrid model: homeschool 3–4 days and join a co-op, tutor group, or mosque program 1–2 days.</p>

<h2 id="islamic-school">Option 3: Islamic School</h2>
<p><strong>What it’s great for:</strong> shared values, Arabic/Qur’an integration, and friendships that make it easier for children to feel “normal” while practicing Islam. For many children, this is the first place where hijab, salah, and halal boundaries feel socially supported rather than socially expensive.</p>
<p><strong>Common risks:</strong> inconsistent academic standards across schools, and occasional “culture” replacing “tarbiyah.” A school can carry the Islamic label and still struggle with teaching quality or student discipline. The solution is not cynicism—it’s evaluation.</p>
<p><strong>Practical check:</strong> ask for academic benchmarks, teacher retention, how they handle behavior, and how Qur’an is taught (memorization only, or meaning + character).</p>

<h2 id="decision-framework">A Simple Decision Framework</h2>
<p>Use this five-step framework before you visit any school. It will reduce confusion and prevent “marketing” from deciding for you.</p>
<ol>
  <li><strong>Define your top 3 priorities</strong> (for this year): academics, faith environment, mental health, flexibility, cost.</li>
  <li><strong>Define the non-negotiables</strong>: safety, discipline, prayer accommodation, language boundaries.</li>
  <li><strong>Assess family bandwidth</strong>: can a parent realistically homeschool daily without breaking the home?</li>
  <li><strong>Assess the child’s temperament</strong>: some children thrive with structure; others need flexibility.</li>
  <li><strong>Choose a one-year plan</strong> and schedule a review date (e.g., end of first term).</li>
</ol>

<h2 id="questions-to-ask">Questions to Ask on School Visits</h2>
<ul>
  <li>How do you handle bullying, disrespect, and online behavior?</li>
  <li>What is the homework load by grade—and how do you support struggling students?</li>
  <li>How do you communicate with parents (weekly updates, portals, meetings)?</li>
  <li>What does “character” education look like in practice?</li>
  <li>What is your policy on phones in class and during breaks?</li>
</ul>

<h2 id="gulf-reality">The Gulf Reality: Cost, Commute, and Energy</h2>
<p>In many Gulf cities, the biggest invisible cost is not tuition—it is commute time and daily energy. A school that looks perfect on paper can drain the home if it requires two hours of traffic daily. When parents are exhausted, the home becomes reactive, and values drift accelerates. Choose the option that leaves enough emotional capacity for the family to function.</p>

<p>Related: <a href="/health/quiet-home-family-guide-en.html">The Quiet Home</a> and <a href="/blog/friday-night-reset-family-en.html">Friday Night Reset</a> can strengthen any education choice by strengthening the home’s culture.</p>

<h2 id="child-fit">Child Fit: Match the Environment to the Child</h2>
<p>Two children in the same family may need two different approaches. Before choosing, describe your child in plain language. Do they need structure or freedom? Are they social or easily overwhelmed? Do they focus well in groups or do they learn better one-on-one?</p>
<p><strong>A structured child</strong> often thrives in private school with predictable expectations. <strong>A sensitive child</strong> may do better with homeschooling or an Islamic school with calmer culture. <strong>A highly social child</strong> can flourish anywhere—but only if the peer environment supports good habits.</p>
<p>Most education stress happens when the environment fights the child’s temperament. If your mornings are already tense, don’t blame the child first—consider the match.</p>

<h2 id="hybrid-options">Hybrid Models (Often the Best Middle)</h2>
<p>You do not have to choose a single “pure” model forever. Many families succeed with hybrid plans:</p>
<ul>
  <li><strong>Private school + home faith curriculum</strong>: Qur’an/Arabic time, mosque classes, family reading, and screen boundaries.</li>
  <li><strong>Islamic school + targeted tutoring</strong>: boost math/English or exam prep without changing the whole environment.</li>
  <li><strong>Homeschool + co-op days</strong>: social time and specialized classes without giving up flexibility.</li>
</ul>
<p>A hybrid approach reduces extremes: it prevents academic gaps without sacrificing a values-aligned home culture.</p>

<h2 id="money-time">The Real Cost: Money, Time, and Stress</h2>
<p>Tuition is only one layer. Add transport, uniforms, activities, lunches, and parent time. Homeschooling may look cheaper, but it “costs” daily parent focus. Private school may cost money, but “buys” structure. Islamic school may sit in between—but varies widely by city.</p>
<p>Ask yourself: what is our bottleneck this year—cash, time, or emotional capacity? Choose the option that protects the bottleneck.</p>

<h2 id="one-year-plan">Write a One-Year Plan (Then Review)</h2>
<p>Write a one-page plan: the option you chose, why you chose it, and what “success” looks like. Then schedule a review date. At the review, ask three questions:</p>
<ol>
  <li>Is my child safer, calmer, and more respectful?</li>
  <li>Is academic progress steady (not perfect, but steady)?</li>
  <li>Is faith practice easier or harder at home?</li>
</ol>
<p>If two of three are declining, you don’t need more motivation—you need a new plan.</p>
<p>Make the plan simple, readable, and shared between both parents.</p>

<h2 id="faq">FAQ</h2>

<div class="faq-item">
<div class="faq-question">Is one option always “best” for Muslim families?</div>
<div class="faq-answer">No. The best option is the one your family can sustain with good character, stable routines, and a strong faith environment at home. Many families change paths by season and stage.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if Islamic school is weak academically?</div>
<div class="faq-answer">You can supplement with tutoring, reading habits, and structured homework support. Evaluate the specific school rather than the label, and ask for benchmarks.</div>
</div>

<div class="faq-item">
<div class="faq-question">Can we homeschool while both parents work?</div>
<div class="faq-answer">Sometimes, but it usually requires a hybrid plan (tutor/co-op/support) and a very clear routine. If the home is already stretched, start with small changes first.</div>
</div>

<div class="faq-item">
<div class="faq-question">How do we protect faith in a private school environment?</div>
<div class="faq-answer">Build a strong “home curriculum”: Qur’an/Arabic time, prayer routines, clear screen boundaries, and weekly family conversation. The home must counterbalance the outside culture.</div>
</div>

<div class="faq-item">
<div class="faq-question">When should we reassess our decision?</div>
<div class="faq-answer">Set a review date before you start—end of term or end of semester. If the child’s mental health, faith practice, or safety is deteriorating, reassess sooner.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> This is general educational information, not legal, financial, or professional advice. Consult licensed educators or specialists for your specific child’s needs.</p></div>

</div>
"""


QUIET_BODY = r"""
<div class="container">

<h1>The Quiet Home: A Family Guide to Lowering the Volume of Modern Life</h1>

<p>Modern life is loud. Not just in decibels, but in the constant demand for attention: background television, overlapping devices, never-ending notifications, and the mental noise of “always on.” For families, the result is predictable: shorter tempers, fragmented conversation, and a home that feels busy even when no one is doing much.</p>

<p>This guide offers a practical framework for building a quieter home—one where silence is possible, where conversation can happen without competing with screens, and where every family member can rest enough to thrive.</p>

<div class="tip"><p><strong>What we mean by “quiet”:</strong> not a silent house, but a home where noise is intentional. Sound is chosen—not default.</p></div>

<h2 id="why-it-matters">Why a Quiet Home Matters</h2>
<p>Noise is not only an annoyance. Chronic background noise makes the brain work harder to filter input, which can reduce attention and patience—especially for children. If you want more calm, you don’t start with “discipline.” You start with the environment.</p>

<p>For parents, noise is a hidden burnout amplifier. The home becomes a place where you can’t fully recover. A quieter home is not luxury; it is maintenance for the nervous system.</p>

<div class="tip"><p><strong>Authority note:</strong> The <a href="https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health" target="_blank" rel="noopener">World Health Organization</a> regularly summarizes how environmental conditions affect health and stress. The same principle applies indoors: environment shapes regulation.</p></div>

<h2 id="what-is-quiet">What Is a Quiet Home?</h2>
<p>A quiet home is not a home where children never play. It is a home with rhythms: times for play and times for stillness. It is a home where meals are not drowned in a screen soundtrack, and where a child can hear a parent’s voice without competition.</p>

<p>In many Muslim homes, quiet also has spiritual meaning. Stillness makes space for reflection, du‘a, and presence. Quiet is not empty. It is a container for the heart.</p>

<h2 id="five-steps">Five Practical Steps (That Actually Work)</h2>

<h3 id="step-1">1) Make silence the default</h3>
<p>If the TV is on but no one is watching, turn it off. If music is running “in the background,” pause it. The default state of the home should be silence. Sound becomes a choice, not a habit.</p>

<h3 id="step-2">2) Create one daily quiet window</h3>
<p>Start with 30 minutes in a predictable slot: after Maghrib, or right after school. No screens. No music. No multitasking. Reading, drawing, prayer, or calm play only. Consistency matters more than length.</p>

<h3 id="step-3">3) The one-device rule in shared rooms</h3>
<p>In the living room, only one active device at a time. If a parent is working on a laptop, the TV stays off. If a child is watching a program, everyone else is off devices. This single rule removes layered noise instantly.</p>

<h3 id="step-4">4) Build a “quiet corner”</h3>
<p>A chair, warm light, a basket of books, and no devices. That’s enough. Teach children that needing quiet is normal. A quiet corner prevents meltdowns by giving the nervous system a place to cool down.</p>

<h3 id="step-5">5) Protect the hour before sleep</h3>
<p>Dim lights. Silence notifications. Avoid screens entirely. Read, pray, or sit together. If your evenings are chaotic, you will carry that chaos into tomorrow. A quiet bedtime is a family investment.</p>

<h2 id="digital-noise">Digital Noise: The Hidden Problem</h2>
<p>Even when the house is physically quiet, the phone can keep the brain loud. Notifications create micro-stress. The solution is simple: set “Do Not Disturb” during family windows, and keep charging outside bedrooms.</p>

<p>If you want a calmer home, treat the dining table like a phone-free zone. You’ll be surprised how quickly conversation returns when attention is not divided.</p>

<h2 id="kids-and-teens">Kids, Teens, and Realistic Expectations</h2>
<p><strong>Young kids:</strong> don’t chase perfect quiet. Aim for “quieter.” Make quiet time short and consistent.</p>
<p><strong>Teens:</strong> negotiate boundaries instead of declaring war. Invite them to co-design the rules: phone outside bedroom after a certain time, and one device in shared rooms.</p>

<h2 id="work-from-home">Work-from-home boundaries</h2>
<p>If your living room becomes an office, the home never fully rests. Create a visual boundary: a small desk, a headset, and a clear “work is over” ritual (closing the laptop, putting it away). Your family needs signals that you are present again.</p>

<h2 id="sound-audit">Do a 15-minute sound audit</h2>
<p>Walk through your home and list every “always-on” sound: TV, YouTube in the kitchen, a child’s tablet, a parent’s phone videos, and even constant voice notes. Most families don’t realize they are stacking audio layers until they write them down.</p>
<p>Then choose one change for the week: remove one layer completely. Quiet is built by subtraction.</p>

<h2 id="meal-protocol">A simple meal protocol</h2>
<p>Meals are where the quiet home becomes real. Try this protocol for one week:</p>
<ul>
  <li>Phones stay out of reach (basket or drawer).</li>
  <li>No TV in the background.</li>
  <li>One opening question: “What was one hard thing and one good thing today?”</li>
  <li>One closing line: “Alhamdulillah for this meal.”</li>
  <li>Keep it short and consistent.</li>
</ul>
<p>The goal is not a perfect dinner. The goal is a predictable place where attention returns to people.</p>

<h2 id="home-design">Small home design changes</h2>
<p>You don’t need renovation. You need a few low-cost adjustments: a rug to reduce echo, curtains to soften sound, and a habit of closing doors during loud activities. If your home is open-plan, create “zones” with furniture so that homework is not in the same sound stream as entertainment.</p>

<h2 id="teens-phone-plan">A teen-friendly phone plan</h2>
<p>Teens often resist “quiet rules” because they hear them as control. Reframe the goal: “We want the home to feel calmer for everyone.” Then agree on two boundaries that apply to parents too:</p>
<ul>
  <li><strong>No phones at meals</strong> (adults included).</li>
  <li><strong>Charging outside bedrooms</strong> at a fixed time.</li>
</ul>
<p>Give teens a voice in the details (exact time, where the charging station lives). Cooperation beats policing.</p>

<h2 id="guests">Guests, extended family, and crowded homes</h2>
<p>Many Gulf homes are social by design. Quiet does not mean isolation. It means designating small pockets of stillness even on busy days. If guests are present, protect the essentials: a phone-free meal, a short quiet wind-down for children, and a clear bedtime routine.</p>

<h2 id="troubleshooting">Troubleshooting when it doesn’t work</h2>
<p>If the house gets louder after you try to make it quieter, it usually means the transition was too fast. Reduce the scope: one rule, one room, one time window. When that stabilizes, add the next layer.</p>
<p>If one parent keeps breaking the rule, don’t argue in front of children. Agree privately on a realistic version you can both sustain. A small consistent boundary is stronger than a big inconsistent one.</p>
<p>If children keep “testing” the new quiet window, treat it like any habit: expect resistance for a week, stay calm, and keep the boundary short. The goal is not to win a fight. The goal is to teach the nervous system a new normal.</p>

<h2 id="starter-plan">A 7-day starter plan</h2>
<div class="table-wrap"><table>
<tr><th>Day</th><th>Experiment</th></tr>
<tr><td>1</td><td>Turn off background TV completely</td></tr>
<tr><td>2</td><td>One-device rule in the living room</td></tr>
<tr><td>3</td><td>30-minute quiet window after Maghrib</td></tr>
<tr><td>4</td><td>Phone-free dinner</td></tr>
<tr><td>5</td><td>Quiet corner setup</td></tr>
<tr><td>6</td><td>Screen-free hour before bed</td></tr>
<tr><td>7</td><td>Review: what changed in mood and sleep?</td></tr>
</table></div>

<p>Related: <a href="/blog/notification-cost-productivity-en.html">The Cost of Notifications</a> and <a href="/blog/friday-night-reset-family-en.html">Friday Night Reset</a>.</p>

<h2 id="faq">FAQ</h2>
<p>Short answers to the questions families ask when they try to make their home quieter.</p>

<div class="faq-item">
<div class="faq-question">Will my kids get bored in a quiet home?</div>
<div class="faq-answer">At first, some will. Boredom is often the doorway to imagination. Start small and stay consistent for two weeks.</div>
</div>

<div class="faq-item">
<div class="faq-question">What if my spouse disagrees?</div>
<div class="faq-answer">Propose a 7-day experiment. Results speak: better sleep, longer conversations, less friction.</div>
</div>

<div class="faq-item">
<div class="faq-question">Can a home be quiet with toddlers?</div>
<div class="faq-answer">Yes with realistic expectations. The goal is not silence; it’s intentional noise with calm pockets.</div>
</div>

<div class="faq-item">
<div class="faq-question">How much quiet time is enough?</div>
<div class="faq-answer">Start with 30 minutes daily. Consistency matters more than long sessions.</div>
</div>

<div class="faq-item">
<div class="faq-question">Is turning off the TV enough?</div>
<div class="faq-answer">It helps, but digital noise from notifications and multiple devices is a major part of the problem. Combine TV-off with phone boundaries.</div>
</div>

<div class="tip"><p><strong>Disclaimer:</strong> This is general health and family education, not medical or mental health advice. If you or your child has significant anxiety, sleep disorders, or hearing issues, consult a licensed professional.</p></div>

</div>
"""


FAQ_DATA: dict[str, list[tuple[str, str]]] = {
    "comparisons/school-type-comparison-guide-en.html": [
        ("Is one option always best for Muslim families?", "No. The best option is the one your family can sustain with stable routines, safety, and a strong home culture. Many families switch by season and stage."),
        ("What if Islamic school is weak academically?", "Supplement with tutoring, reading habits, and structured homework support. Evaluate the specific school rather than the label, and ask for benchmarks."),
        ("Can we homeschool while both parents work?", "Sometimes, but it usually requires a hybrid plan and a strict routine. If the home is already stretched, start small and build support first."),
        ("How do we protect faith in a private school environment?", "Build a strong home curriculum: prayer routines, Qur’an/Arabic time, screen boundaries, and weekly family conversation."),
        ("When should we reassess our decision?", "Set a review date before you start (end of term/semester). Reassess sooner if safety, mental health, or faith practice is deteriorating."),
    ],
    "health/quiet-home-family-guide-en.html": [
        ("Will my kids get bored in a quiet home?", "At first, some will. Boredom is often the doorway to imagination. Start small and stay consistent for two weeks."),
        ("What if my spouse disagrees?", "Propose a 7-day experiment. Results speak: better sleep, longer conversations, less friction."),
        ("Can a home be quiet with toddlers?", "Yes with realistic expectations. The goal is not silence; it’s intentional noise with calm pockets."),
        ("How much quiet time is enough?", "Start with 30 minutes daily. Consistency matters more than long sessions."),
        ("Is turning off the TV enough?", "It helps, but digital noise from notifications and multiple devices is a major part of the problem. Combine TV-off with phone boundaries."),
    ],
}

BODY_MAP = {
    "comparisons/school-type-comparison-guide-en.html": SCHOOL_BODY,
    "health/quiet-home-family-guide-en.html": QUIET_BODY,
}

HERO_ALT = {
    "comparisons/school-type-comparison-guide-en.html": "A parent comparing school options on a notebook with a calm family background",
    "health/quiet-home-family-guide-en.html": "A calm living room with warm light and a quiet family atmosphere",
}

TOC_MAP = {
    "comparisons/school-type-comparison-guide-en.html": [
        ("#the-big-three", "The Big Three Options"),
        ("#private-school", "Private School"),
        ("#homeschool", "Homeschooling"),
        ("#islamic-school", "Islamic School"),
        ("#decision-framework", "Decision Framework"),
        ("#questions-to-ask", "Questions to Ask"),
        ("#faq", "FAQ"),
    ],
    "health/quiet-home-family-guide-en.html": [
        ("#why-it-matters", "Why It Matters"),
        ("#five-steps", "Five Steps"),
        ("#digital-noise", "Digital Noise"),
        ("#kids-and-teens", "Kids & Teens"),
        ("#starter-plan", "7-Day Plan"),
        ("#faq", "FAQ"),
    ],
}


def faq_json(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        ensure_ascii=False,
        separators=(",", ":"),
    )


def replace_container(html: str, new_body: str) -> str:
    return re.sub(
        r'(<article class="article-body">.*?<div class="container">)(.*?)(</div>\s*</article>)',
        lambda m: m.group(1) + new_body.strip() + "\n" + m.group(3),
        html,
        count=1,
        flags=re.S,
    )


def upsert_faq_schema(html: str, faqs: list[tuple[str, str]]) -> str:
    block = f'<script type="application/ld+json">{faq_json(faqs)}</script>'
    if re.search(r'"@type"\s*:\s*"FAQPage"', html):
        return re.sub(
            r'<script type="application/ld\+json">\{[^<]*"@type"\s*:\s*"FAQPage"[^<]*\}</script>',
            block,
            html,
            count=1,
        )
    return html.replace("</head>", block + "\n</head>", 1)


def fix_hero_alt(html: str, alt: str) -> str:
    html = re.sub(
        r'(<section class="article-banner"[^>]*>.*?<img[^>]*alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<figure class="hero"><img[^>]*alt=")[^"]*(")',
        rf"\1{alt}\2",
        html,
        count=1,
    )
    return html


def fix_meta_em_dash(html: str) -> str:
    return html.replace("—", ",")


def update_toc(html: str, items: list[tuple[str, str]]) -> str:
    links = "\n".join(f'<a href="{h}" class="toc-item">{t}</a>' for h, t in items)
    new_toc = f'<div class="sidebar-module sidebar-toc"><h4>📑 Contents</h4>\n{links}\n</div>'
    return re.sub(
        r'<div class="sidebar-module sidebar-toc">.*?</div>',
        new_toc,
        html,
        count=1,
        flags=re.S,
    )


def patch(path: str) -> None:
    fp = ROOT / path
    html = fp.read_text(encoding="utf-8")
    html = replace_container(html, BODY_MAP[path])
    html = upsert_faq_schema(html, FAQ_DATA[path])
    html = fix_hero_alt(html, HERO_ALT[path])
    html = fix_meta_em_dash(html)
    html = update_toc(html, TOC_MAP[path])
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-08"', html, count=1)
    fp.write_text(html, encoding="utf-8")
    print(f"Patched {path}")


def main() -> int:
    for p in BODY_MAP:
        patch(p)
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *BODY_MAP.keys()],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.stderr.strip():
        print(r.stderr, file=sys.stderr)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())

