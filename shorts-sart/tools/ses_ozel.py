#!/usr/bin/env python3
"""Shorts'a özel seslendirme (film kaydından kesmeden): tek çekimden Shorts zaman çizelgesi.
    python3 shorts-sart/tools/ses_ozel.py shorts-sart/gilgamis-ses
Girdi: <proje>/kurgu.js (window.KURGU; saf JSON)
  vo:     {"dosya": "vo/cekim_a.mp3", "kazanc": {"1": 7, "2": 4}}   (parça no → dB; sessiz başlayan parçayı gövdeyle eşitlemek için)
  cumle:  [{"id": "C1", "metin": "Yedi gündür uyuyorsun."}, ...]   metinde "|" kayıttaki bir duraklamayı işaretler (cümle içi parça)
  kesit:  [{"ad": ..., "cumle": ["C3", "C4"]}, ...]                plan sırası; plan sınırı cümleler arası duraklamanın ortası
  son:    son sözcükten sonra süren kuyruk (sn)
Parça sayısı (cümleler + "|") kayıttaki sesli bölüm sayısına eşit olmalı; değilse durur (kesim gerçek duraklamada yapılır).
Sözcük zamanı: parçanın SESLİ karelerine harf uzunluğuyla dağıtılır (ikaros/gilgamis hizala.py yöntemi; ±0,2 sn tahmin).
Çıktı: <proje>/vo/vo.wav (48 kHz mono), zaman.js (window.SZ), timeline.js (score.py için), vo/hizalama.json (rapor)."""
import json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
P = Path(sys.argv[1]).resolve()
K = json.loads(re.search(r'window\.KURGU\s*=\s*(\{.*\});?\s*$', (P / 'kurgu.js').read_text(encoding='utf-8'), re.S).group(1))
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(P / K['vo']['dosya']), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).copy()

# sesli kareler (10 ms) ve ≥ 120 ms duraklamalar
hop = SR // 100
rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), 'same'))[::hop]
thr = max(1e-4, np.percentile(rms, 20) * 2.2); v = rms > thr
vi = np.where(v)[0]; f0, f1 = vi[0], vi[-1] + 1
sil, i = [], f0
while i < f1:
    if not v[i]:
        j = i
        while j < f1 and not v[j]: j += 1
        if j - i >= 12: sil.append((i, j))
        i = j
    else: i += 1
parcalar = []   # (başlangıç, bitiş) kare
s = f0
for a, b in sil: parcalar.append((s, a)); s = b
parcalar.append((s, f1))

norm = lambda w: re.sub(r"[^\wçğıöşüâî]+", '', w.replace('İ', 'i').replace('I', 'ı').lower().replace('â', 'a').replace('î', 'i').replace('û', 'u'))
metin_parca = []  # (cümle id, [sözcükler])
for c in K['cumle']:
    for p in c['metin'].split('|'):
        metin_parca.append((c['id'], [w for w in p.split() if norm(w)]))
if len(metin_parca) != len(parcalar):
    print(f'DUR: metinde {len(metin_parca)} parça, kayıtta {len(parcalar)} sesli bölüm')
    for a, b in parcalar: print(f'  {a / 100:.2f}-{b / 100:.2f}')
    sys.exit(1)

# kazanç: parça parça (duraklamalarda 40 ms geçişle)
g = np.ones(len(x))
for k, db in K['vo'].get('kazanc', {}).items():
    a, b = parcalar[int(k) - 1]
    lo = sil[int(k) - 2][0] if int(k) > 1 else 0                      # önceki duraklamanın başından
    hi = sil[int(k) - 1][1] if int(k) - 1 < len(sil) else len(v)        # sonraki duraklamanın sonuna
    lo_s, hi_s = int(((lo + a) / 2) * hop), int(((b + hi) / 2) * hop)  # duraklama ortalarında geçiş
    g[lo_s:hi_s] = 10 ** (db / 20)
k = np.ones(int(.04 * SR)) / int(.04 * SR); g = np.convolve(g, k, 'same')
y = x * g
pk = np.abs(y).max()
if pk > .95: y *= .95 / pk

words, rapor = [], []
for (cid, ws), (a, b) in zip(metin_parca, parcalar):
    fr = np.where(v[a:b])[0] + a                        # sesli kareler
    L = np.array([len(norm(w)) + 1 for w in ws], float); cum = np.concatenate([[0], np.cumsum(L)]) / L.sum()
    n = len(fr)
    for wi, w in enumerate(ws):
        i0 = fr[min(n - 1, int(round(cum[wi] * (n - 1))))]; i1 = fr[min(n - 1, int(round(cum[wi + 1] * (n - 1))))] + 1
        words.append({'id': cid, 'w': norm(w), 'd': w, 's': round(i0 / 100, 3), 'e': round(i1 / 100, 3)})
    rapor.append({'id': cid, 'parca': ' '.join(ws), 's': a / 100, 'e': b / 100})
son = float(K.get('son', 0))
DUR = round(f1 / 100 + son, 3)
y = np.concatenate([y, np.zeros(max(0, int(DUR * SR) - len(y)), np.float32)])[:int(DUR * SR)]

cues = {}
for w in words:
    c = cues.setdefault(w['id'], {'s': w['s'], 'e': w['e'], 'sec': 0}); c['s'] = min(c['s'], w['s']); c['e'] = max(c['e'], w['e'])
kes = []
for i, kk in enumerate(K['kesit']):
    s0 = 0.0 if i == 0 else round((cues[K['kesit'][i - 1]['cumle'][-1]]['e'] + cues[kk['cumle'][0]]['s']) / 2, 3)
    kes.append({'ad': kk['ad'], 't0': s0})
for i, kk in enumerate(kes): kk['t1'] = kes[i + 1]['t0'] if i + 1 < len(kes) else DUR

(P / 'vo').mkdir(exist_ok=True)
with wave.open(str(P / 'vo' / 'vo.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(np.clip(np.round(y * 32767), -32768, 32767).astype('<i2').tobytes())
J = lambda o: json.dumps(o, ensure_ascii=False)
(P / 'zaman.js').write_text('// shorts-sart/tools/ses_ozel.py üretti (elle değiştirme): Shorts zamanında cümleler, kelimeler, planlar\n'
                           f'window.SZ = {J({"CUES": cues, "WORDS": words, "DUR": DUR, "KESIT": kes})};\n', encoding='utf-8')
(P / 'timeline.js').write_text('// shorts-sart/tools/ses_ozel.py üretti (müzik betiği için; sayfa zaman.js kullanır)\n'
                              f'window.CUES = {J(cues)};\nwindow.WORDS = {J(words)};\nwindow.DUR = {DUR:.3f};\n', encoding='utf-8')
(P / 'vo' / 'hizalama.json').write_text(J(rapor), encoding='utf-8')
print(f'{P.name}: {len(parcalar)} parça, {len(words)} sözcük, süre {DUR:.2f} sn')
for r in rapor: print(f'  {r["s"]:6.2f}–{r["e"]:6.2f}  {r["id"]}  {r["parca"]}')
for kk in kes: print(f'  plan {kk["ad"]}: {kk["t0"]:.2f}–{kk["t1"]:.2f}')
