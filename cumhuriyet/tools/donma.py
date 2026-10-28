"""Donma taraması: videodaki her kareyi 320×180 griye indirip ardışık kare farkını ölçer; ≥ süre boyunca
fark eşiğin altında kalan aralıkları ("kare durdu") listeler. Kumlanma tabanı ~0,3 civarıdır.
python3 tools/donma.py film.mp4 [eşik=0.6] [süre=0.8]"""
import subprocess, sys
import numpy as np
src = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else .6; mind = float(sys.argv[3]) if len(sys.argv) > 3 else .8
w, h = 320, 180
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
fps = 30.0; prev = None; d = []
while True:
    b = p.stdout.read(w * h)
    if len(b) < w * h: break
    f = np.frombuffer(b, np.uint8).astype(np.int16)
    if prev is not None: d.append(np.abs(f - prev).mean())
    prev = f
d = np.array(d); t = (np.arange(len(d)) + 1) / fps
print(f'{len(d) + 1} kare; fark medyanı {np.median(d):.2f}, %5 {np.percentile(d, 5):.2f}')
low = d < thr; runs = []; i = 0
while i < len(low):
    if low[i]:
        j = i
        while j < len(low) and low[j]: j += 1
        if (j - i) / fps >= mind: runs.append((t[i], t[j - 1], d[i:j].mean()))
        i = j
    else: i += 1
for a, b, m in runs: print(f'  durgun {a:7.2f}–{b:7.2f} sn ({b - a:.1f} sn), ortalama fark {m:.2f}')
print('durgun aralık yok' if not runs else f'{len(runs)} durgun aralık')
