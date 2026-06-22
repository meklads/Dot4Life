#!/usr/bin/env python3
"""
Amer remediation (2026-06-22): remove fabricated internal authority quotes and
off-topic copy-pasted "Citation-Ready" callout blocks from blog/guides articles.

A fabricated block is a <div class="callout gold"> ... </div> whose content
contains the signature "Key Insights - Citation-Ready" or "Key quotable statement"
(invented authority quotes attributed to non-existent DOTFORLIFE internal sources,
plus uncited empirical claims). These violate content-standards.md (E-E-A-T,
no fabricated studies, no off-topic copy-paste).

Removal is div-balanced and safe: it removes only the matched block.
Verifies tag balance is preserved (block had equal <div>/</div>).
"""
import sys, re, io

SIG = re.compile(r'Key Insights\s*-\s*Citation-Ready|Key quotable statement', re.I)
OPEN = re.compile(r'<div class="callout gold">')

def count(tag, s):
    return len(re.findall(tag, s))

def strip_file(path, dry=False):
    with io.open(path, 'r', encoding='utf-8') as fh:
        lines = fh.readlines()
    out = []
    i = 0
    removed = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if OPEN.search(line):
            # find matching </div> by balancing, capture block
            bal = count(r'<div', line) - count(r'</div>', line)
            block = [line]
            j = i + 1
            while j < n and bal > 0:
                block.append(lines[j])
                bal += count(r'<div', lines[j]) - count(r'</div>', lines[j])
                j += 1
            blocktext = ''.join(block)
            if SIG.search(blocktext):
                # sanity: block must be div-balanced
                if count(r'<div', blocktext) == count(r'</div>', blocktext):
                    removed += 1
                    i = j  # skip block
                    # also swallow a single trailing blank line if present
                    if i < n and lines[i].strip() == '':
                        i += 1
                    continue
            # not a target block; keep the opening line, continue normally
        out.append(line)
        i += 1
    if removed and not dry:
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.writelines(out)
    # integrity check
    before = ''.join(lines)
    after = ''.join(out)
    bal_before = count(r'<div', before) - count(r'</div>', before)
    bal_after = count(r'<div', after) - count(r'</div>', after)
    return removed, bal_before, bal_after

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith('--')]
    total = 0
    for p in paths:
        r, bb, ba = strip_file(p, dry=dry)
        flag = 'OK' if bb == ba else 'WARN-BALANCE-CHANGED'
        print(f"{'[dry] ' if dry else ''}{p}: removed={r} div_balance {bb}->{ba} {flag}")
        total += r
    print(f"TOTAL blocks removed: {total}")
