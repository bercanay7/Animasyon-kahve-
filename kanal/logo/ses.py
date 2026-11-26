# Logo hareketinin sesi: python3 kanal/logo/ses.py  ->  cikti/logo_hareket.wav (48 kHz, stereo)
# hareket.html zaman çizelgesiyle eş: dönüş 0,25–1,2 · taneler 1,08–2,0 · kum akışı 1,95–2,5 · nokta oturur 2,55 · yazı 3,85
# Hepsi sentez (gürültü + sinüs), tohumlu; dış ses dosyası yok.
import numpy as np, wave, os
SR, SN = 48000, 6.5
n = int(SR * SN); t = np.arange(n) / SR
rng = np.random.default_rng(7)

def bant(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def zarf(a, b, egri=1.0):
    u = np.clip((t - a) / (b - a), 0, 1)
    return np.sin(np.pi * u) ** egri

out = np.zeros(n)
# 1) dönüş: yumuşak hava hışırtısı, bant 300–1400 Hz
out += bant(rng.standard_normal(n), 300, 1400) * zarf(.25, 1.25, 1.5) * .22
# 2) taneler dağılır: kısa kum tıkırtıları, yoğunluk ortada
for i in range(420):
    t0 = 1.08 + (2.0 - 1.08) * (rng.random() ** .8)
    k = int(t0 * SR); L = int(.004 * SR)
    if k + L >= n: continue
    out[k:k + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / (L / 5)) * .05 * (.5 + rng.random())
out = out + bant(out, 2500, 12000) * .4
# 3) kum akışı: ince sürekli hışırtı, 3–9 kHz
out += bant(rng.standard_normal(n), 3000, 9000) * zarf(1.95, 2.55, .7) * .07
# 4) nokta oturur: tahta "tok", 2,55
k = np.maximum(t - 2.55, -1e-3); m = t >= 2.55
tok = np.where(m, (np.sin(2 * np.pi * 165 * k) + .45 * np.sin(2 * np.pi * 330 * k)) * np.exp(-k * 18), 0)
tik = np.where(m & (k < .004), rng.standard_normal(n) * np.exp(-k * 900), 0)
out += tok * .55 + bant(tik, 1500, 6000) * .25
# 5) yazı gelir: tek sıcak çan (La bemol, kısmi seslerle), 3,85
k = np.maximum(t - 3.85, -1e-3); m = t >= 3.85
can = sum(a * np.sin(2 * np.pi * f * k) * np.exp(-k * d) for f, a, d in [(415.3, 1, 1.6), (830.6, .35, 2.4), (1245.9, .15, 3.2), (207.65, .3, 1.2)])
out += np.where(m, can * np.minimum(k / .01, 1), 0) * .16
# sona doğru yumuşak kesiş
out *= np.clip((SN - t) / .4, 0, 1)
# stereo: tanelere hafif genişlik
gen = bant(rng.standard_normal(n), 2500, 9000) * zarf(1.08, 2.5, .8) * .015
L, R = out + gen, out - gen
st = np.stack([L, R], 1); st /= np.abs(st).max() * 1.12
yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cikti', 'logo_hareket.wav')
with wave.open(yol, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('✓', yol)
