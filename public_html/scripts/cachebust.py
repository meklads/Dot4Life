#!/usr/bin/env python3
"""Auto cache-busting: stamp every local CSS link with a content hash (?v=<hash>).
Run before each deploy:  python3 scripts/cachebust.py
Idempotent — only changes when the CSS file content changes."""
import re, hashlib, glob, os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def h(rel):
    p=os.path.join(root, rel.lstrip('/'))
    if not os.path.isfile(p): return None
    return hashlib.md5(open(p,'rb').read()).hexdigest()[:8]
pat=re.compile(r'href="(/styles/[^"?]+\.css)(?:\?v=[^"]*)?"')
changed=0
for f in glob.glob(os.path.join(root,'**','*.html'), recursive=True):
    if '/.trash/' in f or '/components/' in f: continue
    s=open(f,encoding='utf-8').read(); orig=s
    def repl(m):
        ver=h(m.group(1))
        return f'href="{m.group(1)}?v={ver}"' if ver else m.group(0)
    s=pat.sub(repl, s)
    if s!=orig: open(f,'w',encoding='utf-8').write(s); changed+=1
print(f"cachebust: stamped {changed} files")
