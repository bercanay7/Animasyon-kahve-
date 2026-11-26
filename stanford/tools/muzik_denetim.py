"""Müzik telefonda duyuluyor mu? (Frankenstein dersi + Stanford eki: hışırtı müzik sayılmaz)
Miks = a·anlatım + b·müzik + c·efekt (en küçük kareler) → her iz miksteki kazancıyla.
Telefon hoparlörü vekili: 300 Hz–8 kHz bant geçiren. Saniye saniye:
  tonlu müzik (audio/music_ton.wav: piyano, dron, akor; hışırtı/uğultu/motor yok) ve anlatım düzeyi, telefon bandında.
Kullanım: python3 tools/muzik_denetim.py [son_dosya.wav]   (son dosya verilirse müziğin oradaki kazancı da ölçülür)"""
import wave, json, re, sys, numpy as np
SR = 48000
def rd(p):
    w = wave.open(p); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768; return x.reshape(-1, ch).mean(1)
vo, mu, mt, ef, mix = rd('vo/vo.wav'), rd('audio/music.wav'), rd('audio/music_ton.wav'), rd('audio/efekt.wav'), rd('audio/mix.wav')
n = min(map(len, [vo, mu, mt, ef, mix])); vo, mu, mt, ef, mix = vo[:n], mu[:n], mt[:n], ef[:n], mix[:n]
import os
X = np.stack([vo, mu, ef], 1); coef, *_ = np.linalg.lstsq(X[::7], mix[::7], rcond=None)
if os.environ.get('KAZANC'): coef = np.array([float(v) for v in os.environ['KAZANC'].split(',')])   # miks henüz yenilenmediyse eski miksin kazançları
res = mix - X @ coef
print('kazançlar anlatım/müzik/efekt:', np.round(coef, 4), '| artık/miks dB: %.1f' % (10 * np.log10(np.mean(res ** 2) / np.mean(mix ** 2))))
TL = open('timeline.js').read(); CUES = json.loads(re.search(r'window\.CUES = (\{.*?\});', TL, re.S).group(1))
def tel(x, lo=300, hi=8000):
    out = np.zeros_like(x); B = SR * 8
    for i in range(0, len(x), B):
        s = x[i:i + B]; F = np.fft.rfft(s); f = np.fft.rfftfreq(len(s), 1 / SR); F[(f < lo) | (f > hi)] = 0; out[i:i + B] = np.fft.irfft(F, len(s))
    return out
sec = n // SR
def db(x): return 20 * np.log10(np.sqrt(np.mean(x[:sec * SR].reshape(sec, SR) ** 2, 1)) + 1e-9)
M, MT, V = mu * coef[1], mt * coef[1], vo * coef[0]
dM, dMt, dV = db(tel(M)), db(tel(MT)), db(tel(V))
konus = np.zeros(n, bool)
for c in CUES.values(): konus[int(c['s'] * SR):int(c['e'] * SR)] = True
kz = konus[:sec * SR].reshape(sec, SR).mean(1) > .5
ESIK = -55   # telefonda bu düzeyin altındaki tonlu müzik duyulmaz sayılır (Frankenstein ölçütü)
FARK = -24   # konuşmada tonlu müzik anlatımın bu kadar altındaysa maskelenir
duy = (dMt > ESIK) & (~kz | (dMt - dV > FARK))
print('telefon bandı, tüm müzik (hışırtı dahil): medyan %.1f dBFS' % np.median(dM))
print('telefon bandı, TONLU müzik: medyan %.1f | konuşmada %.1f | konuşma dışı %.1f' % (np.median(dMt), np.median(dMt[kz]), np.median(dMt[~kz])))
print('konuşmada tonlu müzik − anlatım (telefon bandı): medyan %.1f dB, en kötü %%10: %.1f' % (np.median((dMt - dV)[kz]), np.percentile((dMt - dV)[kz], 10)))
print('tonlu müziğin telefonda duyulduğu saniye: %d/%d (%%%d)' % (duy.sum(), sec, 100 * duy.mean()))
ara = []; i = 0
while i < sec:
    if not duy[i]:
        j = i
        while j < sec and not duy[j]: j += 1
        if j - i >= 5: ara.append((i, j))
        i = j
    else: i += 1
f = lambda s: '%d:%02d' % (s // 60, s % 60)
print('telefonda tonlu müziğin duyulmadığı ≥5 sn aralıklar (%d, toplam %d sn):' % (len(ara), sum(b - a for a, b in ara)))
for a, b in ara: print('  %s–%s (%d sn)' % (f(a), f(b), b - a))
if len(sys.argv) > 1:
    F = rd(sys.argv[1])[:n]; bf = []
    for s in range(sec):
        sl = slice(s * SR, (s + 1) * SR)
        if np.sqrt(np.mean(M[sl] ** 2)) < 1e-4: continue
        c, *_ = np.linalg.lstsq(np.stack([V[sl], M[sl], ef[sl] * coef[2]], 1), F[sl], rcond=None); bf.append(c[1])
    print('son dosyada müzik kazancı (1 = miksle aynı): medyan %.3f, en düşük %%5: %.3f' % (np.median(bf), np.percentile(bf, 5)))
np.savez('/tmp/claude-0/-home-user/fecdf416-d52a-5b19-840a-06fb4a2a3acf/scratchpad/muzik_st.npz', dM=dM, dMt=dMt, dV=dV, kz=kz, duy=duy)
