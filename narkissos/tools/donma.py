"""Donma taraması (cumhuriyet/tools/donma.py'den): render edilmiş videoda her kareyi 320×180 griye indirip ARA saniye önceki kareyle karşılaştırır.
≥ süre boyunca fark eşiğin altında kalan aralıkları ("kare durdu") planıyla listeler. Kanal kuralı: donuk plan yok (her plan ilk saniyeden hareketli).
python3 tools/donma.py video.mp4 [eşik=0.9] [süre=0.8] [ara=1.0] [--bas=0]
--bas: video filmin hangi saniyesinden başlıyor (ARALIK ile alınmış parça render için). Animatik (960×540) de taranabilir; yer tutucular yavaş yaklaştığı için
eşik altında kalabilir: anlamlı sonuç gerçek sahnelerde. Fark ölçeği 0–255 gri; vazo zemininde yavaş yaklaşma ≈ 0,5–1,5 verir."""
import json, os, re, subprocess, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
src = args[0]; thr = float(args[1]) if len(args) > 1 else .9; mind = float(args[2]) if len(args) > 2 else .8; gap = float(args[3]) if len(args) > 3 else 1.0
bas = next((float(a.split('=')[1]) for a in sys.argv if a.startswith('--bas=')), 0.0)
# plan sınırları (planlar.json + timeline.js; film.js A() ile aynı çözüm)
tl = open(os.path.join(ROOT, 'timeline.js'), encoding='utf-8').read()
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', tl, re.S).group(1)); WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', tl, re.S).group(1))
P = json.load(open(os.path.join(ROOT, 'planlar.json'), encoding='utf-8'))
norm = lambda w: re.sub(r'[^\wçğıöşü]', '', w.lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
def A(at):
    m = re.match(r'^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$', at); sid, w, n, off = m.group(1), m.group(2), int(m.group(3) or 0), float(m.group(4) or 0)
    t = CUES[sid]['s']
    if w:
        h = [x for x in WORDS if x['id'] == sid and x['w'].startswith(norm(w))]
        if len(h) > n: t = h[n]['s']
    return t + off
rows = sorted((A(p['at']), pid) for pid, p in P.items())
def plan_of(t):
    q = rows[0][1]
    for s, pid in rows:
        if s <= t + 1e-6: q = pid
    return q
w, h = 320, 180
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
fps = 30.0; G = max(1, int(round(gap * fps))); buf = []; d = []
while True:
    b = p.stdout.read(w * h)
    if len(b) < w * h: break
    f = np.frombuffer(b, np.uint8).astype(np.int16); buf.append(f)
    if len(buf) > G: d.append(np.abs(f - buf.pop(0)).mean())
d = np.array(d); t = (np.arange(len(d)) + G) / fps + bas
print(f'{len(d) + G} kare; {gap:.1f} sn arayla fark medyanı {np.median(d):.2f}, %5 {np.percentile(d, 5):.2f}')
low = d < thr; runs = []; i = 0
while i < len(low):
    if low[i]:
        j = i
        while j < len(low) and low[j]: j += 1
        if (j - i) / fps >= mind: runs.append((t[i] - gap, t[j - 1], d[i:j].mean()))
        i = j
    else: i += 1
for a, b, m in runs: print(f'  durgun {a:7.2f}–{b:7.2f} sn ({b - a:.1f} sn), ortalama fark {m:.2f}  {plan_of(a + .01)} → {plan_of(b)}')
print('durgun aralık yok' if not runs else f'{len(runs)} durgun aralık')
