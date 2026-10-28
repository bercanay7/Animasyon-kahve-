"""Donma taraması: videodaki her kareyi 320×180 griye indirip her kareyi ARA saniye önceki kareyle karşılaştırır
(varsayılan 1 sn; figür pozları ikişerli olduğu için ardışık kare farkı yanıltıcıdır: yönetmenlik kurulu, 3. tur).
≥ süre boyunca fark eşiğin altında kalan aralıkları ("kare durdu") listeler.
python3 tools/donma.py film.mp4 [eşik=0.9] [süre=0.8] [ara=1.0]"""
import subprocess, sys
import numpy as np
src = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else .9; mind = float(sys.argv[3]) if len(sys.argv) > 3 else .8
gap = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
w, h = 320, 180
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
fps = 30.0; G = max(1, int(round(gap * fps))); buf = []; d = []
while True:
    b = p.stdout.read(w * h)
    if len(b) < w * h: break
    f = np.frombuffer(b, np.uint8).astype(np.int16)
    buf.append(f)
    if len(buf) > G: d.append(np.abs(f - buf.pop(0)).mean())
d = np.array(d); t = (np.arange(len(d)) + G) / fps
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
