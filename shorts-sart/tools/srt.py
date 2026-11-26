#!/usr/bin/env python3
"""Shorts altyazısı (SRT): python3 shorts-sart/tools/srt.py shorts-sart/narkissos → <proje>/<ad>_sart.tr.srt
Her cümle (kesitte kalan sözcükleriyle) bir satır; 42 karakteri aşarsa iki satıra bölünür. Kaynak zaman.js (Shorts zamanı)."""
import json, re, sys
from pathlib import Path
P = Path(sys.argv[1]).resolve()
Z = json.loads(re.search(r'window\.SZ = (\{.*\});', (P / 'zaman.js').read_text(encoding='utf-8'), re.S).group(1))
ts = lambda t: f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}'
bloklar, cur = [], []
for w in Z['WORDS']:
    if not w['d']: continue
    cur.append(w)
    if re.search(r'[.?!:]”?$', w['d']) or len(' '.join(x['d'] for x in cur)) > 70: bloklar.append(cur); cur = []
if cur: bloklar.append(cur)
out = []
for i, b in enumerate(bloklar):
    s = ' '.join(x['d'] for x in b)
    if len(s) > 42:
        k = len(s) // 2; j = s.rfind(' ', 0, k + 8); s = s[:j] + '\n' + s[j + 1:]
    e = min(b[-1]['e'] + .4, bloklar[i + 1][0]['s'] - .05) if i + 1 < len(bloklar) else b[-1]['e'] + .6
    out.append(f'{i + 1}\n{ts(b[0]["s"])} --> {ts(e)}\n{s}\n')
f = P / f'{P.name}_sart.tr.srt'; f.write_text('\n'.join(out), encoding='utf-8'); print(f, len(out), 'altyazı')
