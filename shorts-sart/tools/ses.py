#!/usr/bin/env python3
"""Şart Shorts'u: anlatım kesitlerini filmin seslendirmesinden keser, Shorts zaman çizelgesini yazar.
    python3 shorts-sart/tools/ses.py shorts-sart/narkissos
Girdi: <proje>/kurgu.js  (window.KURGU = {...}; saf JSON)
  film:     filmin klasörü (depo köküne göre), ör. "narkissos"; vo/vo.wav ve timeline.js oradan okunur
  kesit:    [{ad, a: [a0, a1] (filmde anlatım aralığı, sn), ...}  ya da  {ad, d: sn} (sessiz kesit: müzik ve görüntü sürer)]
Çıktı: <proje>/vo/vo.wav (48 kHz mono, kesitler uç uca, uçlarda 15 ms yumuşatma)
       <proje>/zaman.js    window.SZ = {CUES, WORDS, DUR, KESIT: [{ad, t0, t1, a0}]}   (sayfa için)
       <proje>/timeline.js window.CUES / WORDS / DUR (müzik betiği score.py için; filmin biçimi)
Kesit uçları kelime ortasına düşerse uyarır (kesim gerçek duraklamada yapılır)."""
import json, re, sys, wave
from pathlib import Path
import numpy as np

SR = 48000
P = Path(sys.argv[1]).resolve()
ROOT = Path(__file__).resolve().parents[2]
K = json.loads(re.search(r'window\.KURGU\s*=\s*(\{.*\});?\s*$', (P / 'kurgu.js').read_text(encoding='utf-8'), re.S).group(1))
FILM = ROOT / K['film']
TL = (FILM / 'timeline.js').read_text(encoding='utf-8')
CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
WORDS = json.loads(re.search(r'window\.WORDS = (\[.*?\]);', TL, re.S).group(1))

with wave.open(str(FILM / 'vo' / 'vo.wav')) as w:
    assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2
    vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

out, words, kes, t = [], [], [], 0.0
fade = int(.015 * SR)
for k in K['kesit']:
    if 'a' in k:
        a0, a1 = k['a']
        i0, i1 = int(round(a0 * SR)), int(round(a1 * SR))
        x = vo[i0:i1].copy()
        r = np.linspace(0, 1, fade, dtype=np.float32); x[:fade] *= r; x[-fade:] *= r[::-1]
        for wd in WORDS:
            if wd['e'] <= a0 or wd['s'] >= a1: continue
            if wd['s'] < a0 - .01 or wd['e'] > a1 + .01:
                print(f'  UYARI {k["ad"]}: "{wd["d"]}" kesit ucunda bölünüyor ({wd["s"]:.2f}-{wd["e"]:.2f})')
                continue
            words.append({**wd, 's': round(wd['s'] - a0 + t, 3), 'e': round(wd['e'] - a0 + t, 3)})
        d = (i1 - i0) / SR
    else:
        d = float(k['d']); a0 = None
        x = np.zeros(int(round(d * SR)), np.float32)
    out.append(x)
    kes.append({'ad': k['ad'], 't0': round(t, 4), 't1': round(t + d, 4), 'a0': a0})
    t += d
# uzatma: son kesitten sonra müzik ve görüntü süren kuyruk (kurgu.son sn)
son = float(K.get('son', 0))
out.append(np.zeros(int(round(son * SR)), np.float32))
y = np.concatenate(out); DUR = len(y) / SR

cues = {}
for wd in words:
    c = cues.setdefault(wd['id'], {'s': wd['s'], 'e': wd['e'], 'sec': 0})
    c['s'] = min(c['s'], wd['s']); c['e'] = max(c['e'], wd['e'])

(P / 'vo').mkdir(exist_ok=True)
with wave.open(str(P / 'vo' / 'vo.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(np.clip(np.round(y * 32767), -32768, 32767).astype('<i2').tobytes())
J = lambda o: json.dumps(o, ensure_ascii=False)
(P / 'zaman.js').write_text('// shorts-sart/tools/ses.py üretti (elle değiştirme): Shorts zamanında cümleler, kelimeler, kesitler\n'
                           f'window.SZ = {J({"CUES": cues, "WORDS": words, "DUR": round(DUR, 3), "KESIT": kes})};\n', encoding='utf-8')
(P / 'timeline.js').write_text('// shorts-sart/tools/ses.py üretti (müzik betiği için; sayfa zaman.js kullanır)\n'
                              f'window.CUES = {J(cues)};\nwindow.WORDS = {J(words)};\nwindow.DUR = {DUR:.3f};\n', encoding='utf-8')
print(f'{P.name}: {len(kes)} kesit, {len(words)} kelime, süre {DUR:.2f} sn')
for k in kes: print(f'  {k["t0"]:6.2f}–{k["t1"]:6.2f}  {k["ad"]}')
