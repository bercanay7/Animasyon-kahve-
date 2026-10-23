"""English subtitles: script text (tags removed) timed with the placed English word timestamps
(en/timeline_en.json) -> en/sisifos.en.srt.  Max 42 chars/line, 2 lines/cue, split at sentence/comma.
Usage: python3 en/tools/srt_en.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_en import *

MAXL, MAXC = 42, 84
MIN_DUR, TAIL, GAP = 1.0, 0.35, 0.08
tl = json.load(open(os.path.join(EN, 'timeline_en.json')))
WORDS = tl['words']

def fmt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

SENT = ('.', '?', '!', '.”', '?”', '!”', '."', '?"', '!"', '…', ':')
def strength(tok):
    """how good a break after this token is: 0 sentence end, 1 colon/ellipsis, 2 comma, 9 none"""
    t = tok.rstrip('"”')
    if t.endswith(('.', '?', '!')): return 0
    if t.endswith(('…', ':', ';')): return 1
    if t.endswith(','): return 2
    return 9

def wrap(toks):
    """best 1- or 2-line layout (each line <= MAXL); prefers punctuation and balanced lines"""
    s = ' '.join(toks)
    if len(s) <= MAXL: return s, 0
    best, bi = 1e9, None
    for i in range(1, len(toks)):
        a, b = ' '.join(toks[:i]), ' '.join(toks[i:])
        if len(a) > MAXL or len(b) > MAXL: continue
        cost = abs(len(a) - len(b)) * 0.5 + [0, 4, 6, 20, 20, 20, 20, 20, 20, 20][strength(toks[i - 1])]
        if cost < best: best, bi = cost, i
    if bi is None: return None, 1e9
    return ' '.join(toks[:bi]) + '\n' + ' '.join(toks[bi:]), best

def chunk_cost(toks, ws):
    txt, c = wrap(toks)
    if txt is None: return 1e9
    dur = ws[-1]['e'] - ws[0]['s']
    n = len(' '.join(toks))
    cost = c + [0, 3, 6, 40, 40, 40, 40, 40, 40, 40][strength(toks[-1])]
    if n < 16: cost += (16 - n) * 2          # avoid tiny flashes
    if dur > 7: cost += (dur - 7) * 10       # avoid long-standing cues
    if dur < 1.0: cost += 15
    return cost + 10                          # per-cue cost: fewer, fuller cues

cues = []
for sg in load_script():
    ws = [w for w in WORDS if w['id'] == sg['id']]
    toks = [w['w'] for w in ws]
    assert toks == [t for t in display_words(sg['tts']) if norm_words(t)], sg['id']
    n = len(toks)
    best = [0] + [1e18] * n; back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - 30), j):
            if len(' '.join(toks[i:j])) > MAXC + 1: continue
            c = best[i] + chunk_cost(toks[i:j], ws[i:j])
            if c < best[j]: best[j], back[j] = c, i
    parts, j = [], n
    while j > 0: parts.append((back[j], j)); j = back[j]
    for i, j in reversed(parts):
        txt, _ = wrap(toks[i:j])
        cues.append([ws[i]['s'], ws[j - 1]['e'], txt])

for i, c in enumerate(cues):
    nxt = cues[i + 1][0] if i + 1 < len(cues) else c[1] + 3
    c[1] = min(max(c[1] + TAIL, c[0] + MIN_DUR), nxt - GAP)
    assert c[1] > c[0]
    for line in c[2].split('\n'): assert len(line) <= MAXL, line
    assert c[2].count('\n') <= 1

out = os.path.join(EN, 'sisifos.en.srt')
with open(out, 'w', encoding='utf-8') as f:
    for i, (a, b, t) in enumerate(cues, 1):
        f.write(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}\n\n')
print(len(cues), 'cues ->', out)
