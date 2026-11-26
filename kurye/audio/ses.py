#!/usr/bin/env python3
"""MEKTUPLAR (Zaman Kuryesi kimlik filmi): özgün müzik ve ses; yalnız numpy ile sentez (örnek ses yok, indirme yok, ücretli üretim yok).
Ezgi bu dosyada yazıldı. Mi bemol majör, ağır (60 vuruş/dk).
  SORU: Sib4 – Mib5 – Re5 – Sib4 (kurye başını meşeye kaldırınca; mektubu çıkarınca bir kez daha, armonili).
  YOL: mektup havadayken yükselen arpej (Mib – Do min – Lab – Sib), rüzgârla hızlanır.
  ÇİÇEK: mektup taca konunca (18.8 sn) yüksek çan ışıltısı; çiçekler açıldıkça yoğunlaşır.
  CEVAP: Sib5 – Sol5 – Fa5 – Mib5 (yapraklar kuryeye dönerken; sorunun inen eşi). Son akor Mib (add9) söner.
Ses: tarlada sürekli hafif rüzgâr; 11–14 sn soldan sağa geçen esinti (görüntüdeki dalgayla aynı an); mektup kâğıt hışırtısı.
Zamanlar kurye/tablo.html'deki zaman çizelgesiyle aynı (tSal 12.2, tVar 16.6, batış 17–25); ayak basma anları adimlar.json (adimlar.js).
    python3 kurye/audio/ses.py  -> kurye/audio/ses.wav (48 kHz stereo, -16 LUFS, iki geçişli doğrusal loudnorm)
"""
import re, wave, subprocess
from pathlib import Path
import numpy as np

SR = 48000; DUR = 25.0; N = int(DUR * SR)
HERE = Path(__file__).resolve().parent
L = np.zeros(N, np.float32); R = np.zeros(N, np.float32)
rng = np.random.default_rng(1926)
tBak, tCik, tSal, tVar = 7.2, 9.8, 12.2, 16.6

def put(sig, t, pan=0.0, g=1.0):
    a = int(t * SR); b = min(N, a + len(sig))
    if a >= N or b <= 0: return
    if a < 0: sig = sig[-a:]; a = 0; b = min(N, len(sig))
    s = (sig[:b - a] * g).astype(np.float32)
    L[a:b] += s * np.float32(np.sqrt(.5 * (1 - pan))); R[a:b] += s * np.float32(np.sqrt(.5 * (1 + pan)))

NOTA = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(n):
    m = re.match(r'([A-G])([#b]?)(-?\d)', n); return 12 * (int(m.group(3)) + 1) + NOTA[m.group(1)] + {'#': 1, 'b': -1, '': 0}[m.group(2)]
def hz(m): return 440 * 2 ** ((m - 69) / 12)

# ── çalgılar ──
def piyano(m, v=.6, d=3.0):
    """eğik tel kısmileri, iki aşamalı sönüm, yumuşak çekiç (gece piyanosu: parlak değil)"""
    f0 = hz(m); dd = d + 1.5; n = int(dd * SR); t = np.arange(n) / SR; B = .0003 * (1 + max(0, 60 - m) * .02)
    s = np.zeros(n)
    for k in range(1, 12):
        fk = f0 * k * np.sqrt(1 + B * k * k)
        if fk > 7000: break
        a = (1 / k ** 1.4) * (.3 + .7 * v) ** (k * .3)
        dec = max(.25, .5 + .045 * (m - 48)) * (1 + k * .5)
        for det in (-.0005, .0005):
            s += a * np.sin(2 * np.pi * fk * (1 + det) * t + k * 1.3) * (np.exp(-t * dec) * .6 + .4 * np.exp(-t * dec * .22))
    rel = np.ones(n); r0 = int(d * SR); rel[r0:] = np.exp(-np.arange(n - r0) / (.35 * SR))
    s *= rel * v; s[:96] *= np.linspace(0, 1, 96)
    return (s / 3.0).astype(np.float32)
def yayli(m, d, v=.4, atak=1.2):
    """yaylı yüzey: hafif ayrık ses kopyaları, yavaş giriş ve çıkış, ağır vibrato"""
    f0 = hz(m); n = int((d + 2.0) * SR); t = np.arange(n) / SR
    vib = 1 + .0025 * np.sin(2 * np.pi * 4.6 * t + m)
    s = np.zeros(n)
    for det in (-.004, 0, .0037):
        for k, a in ((1, 1), (2, .5), (3, .28), (4, .16), (5, .09), (6, .05)):
            s += a * np.sin(2 * np.pi * f0 * k * (1 + det) * np.cumsum(vib) / SR + k * det * 900)
    e = np.minimum(1, t / atak) ** 1.5 * np.where(t > d, np.exp(-(t - d) / .9), 1)
    return (s * e * v * .09).astype(np.float32)
def can(m, v=.3, d=3.5):
    """çan ve celesta arası: uyumsuz kısmiler, hızlı sönen parlaklık"""
    f0 = hz(m); n = int(d * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * (1.1 + r * .9)) for r, a in ((1, 1), (2.76, .35), (5.4, .14), (8.93, .06)))
    s[:48] *= np.linspace(0, 1, 48)
    return (s * v * .5).astype(np.float32)

# ── gürültü süzgeci (FFT'de; scipy yok) ──
def renkli_gurultu(n, f_lo, f_hi, egim=0.0, tohum=0):
    r = np.random.default_rng(tohum); X = np.fft.rfft(r.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR)
    m = ((f > f_lo) & (f < f_hi)).astype(float)
    m = np.convolve(m, np.ones(64) / 64, 'same') * (np.maximum(f, 20) / 1000) ** egim
    y = np.fft.irfft(X * m, n); return (y / (np.abs(y).max() + 1e-9)).astype(np.float32)
def zarf(nokta, n):
    """[(t, değer)] → örnek başına doğrusal zarf"""
    ts = np.array([p[0] for p in nokta]) * SR; vs = np.array([p[1] for p in nokta]); return np.interp(np.arange(n), ts, vs).astype(np.float32)

# ── efektler: ElevenLabs Sound Effects v3 (kullanıcının hesabı, 26 Kasım; efekt/ altında; seçim düzey eğrisi ve spektrumla) ──
# ortam_a (tarla, rüzgâr, uzak cırcır; 25 sn), esinti_a (tek güçlü esinti; doruk 2.5 sn), kagit_a (dönen zarf), kagit_b (zarf çantadan çıkar)
# EFEKT=0 ile eski sentez rüzgâr ve kâğıt kullanılır.
import os
EFEKT = os.environ.get('EFEKT', '1') != '0'
def yukle(ad):
    ham = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(HERE / 'efekt' / ad), '-af', 'highpass=f=90,highpass=f=90', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(ham, np.float32).reshape(-1, 2).copy()
EFL = []   # (yerleştirilmiş efekt, müziğe göre hedef dB): her biri kendi en gür yarım saniyesine göre ölçeklenir
def koy(x, t, hedef_db, a=0.0, b=None, giris=.05, cikis=.3):
    i0 = int(a * SR); i1 = len(x) if b is None else int(b * SR); y = x[i0:i1].copy(); n = len(y)
    e = np.ones(n, np.float32); gi = int(giris * SR); ci = int(cikis * SR)
    if gi: e[:gi] = np.linspace(0, 1, gi)
    if ci: e[-ci:] *= np.linspace(1, 0, ci)
    y *= e[:, None]; z = np.zeros((N, 2), np.float32); k = int(t * SR); m = min(N, k + n)
    if k < N: z[k:m] = y[:m - k]
    EFL.append((z, hedef_db))
def doruk_rms(z):
    h = SR // 2; v = [np.sqrt(np.mean(z[i:i + h] ** 2)) for i in range(0, len(z) - h, h)]; return max(v) + 1e-9
if EFEKT:
    koy(yukle('ortam_a.mp3'), 0, -14, giris=1.2, cikis=1.5)                 # tarla yatağı
    koy(yukle('esinti_a.mp3'), 10.1, -3, giris=.3, cikis=1.0)              # esinti: müziği bir an örter
    koy(yukle('esinti_b.mp3'), 18.6, -11, giris=.6, cikis=1.2)             # ikinci, hafif esinti: yapraklar kopar
    koy(yukle('kagit_b.mp3'), 9.7, -9, .4, 1.4, giris=.02, cikis=.2)       # zarf çantadan çıkar
    koy(yukle('kagit_a.mp3'), 10.7, -5, giris=.1, cikis=1.4)               # rüzgâr zarfı alır, döner

# ── ayak sesi (sentez): topuk vuruşu (alçak, kısa) + kuru toprak ve ot çıtırtısı (tanecikli dar bant gürültü) ──
import json
def adim(v=1.0, tohum=0):
    r = np.random.default_rng(100 + tohum); n = int(.22 * SR); t = np.arange(n) / SR
    vur = np.sin(2 * np.pi * (95 + 30 * r.random()) * t * (1 - t * 1.5)) * np.exp(-t / .018)
    tane = (r.random(n) < .035).astype(np.float32) * r.standard_normal(n)
    cit = np.fft.irfft(np.fft.rfft(tane) * ((np.fft.rfftfreq(n, 1 / SR) > 900) & (np.fft.rfftfreq(n, 1 / SR) < 5200)), n)
    cit *= np.exp(-np.maximum(0, t - .012) / .05) * (t > .008)
    x = vur * .55 + cit / (np.abs(cit).max() + 1e-9) * .5
    return np.stack([x, x], 1).astype(np.float32) * v
ADIM = json.loads((HERE / 'adimlar.json').read_text())
if EFEKT:
    for i, a in enumerate(ADIM + [{'t': 6.62, 'ayak': 0}, {'t': 6.95, 'ayak': 1}]):
        uz = min(1, .55 + .45 * (1 - a['t'] / 7))                     # kurye uzaklaştıkça sesi kısılır
        koy(adim(1, i), a['t'] - .005, -15 - 9 * (1 - uz) - (4 if a['t'] > 6.5 else 0), giris=0, cikis=.05)

# ── rüzgâr (sentez yedeği): sürekli alçak hışırtı + 11–14 sn esinti (soldan sağa: pan -0.8 → +0.8) ──
taban = renkli_gurultu(N, 80, 1400, -.5, 1) * .5 + renkli_gurultu(N, 300, 3500, -.8, 2) * .25
dalga = renkli_gurultu(N, 180, 5200, -.35, 3)
tt = np.arange(N) / SR
taban_z = zarf([(0, .0), (1.2, .5), (10.6, .55), (16, .6), (22, .42), (25, .25)], N) * (1 + .18 * np.sin(2 * np.pi * .13 * tt) + .1 * np.sin(2 * np.pi * .41 * tt))
dalga_z = np.exp(-((tt - 12.6) / 1.15) ** 2) + .3 * np.exp(-((tt - 19.6) / 1.5) ** 2)
pan_d = np.clip((tt - 12.6) / 1.6, -1, 1) * .8
g_s = 0.0 if EFEKT else 1.0
L += g_s * (taban * taban_z * .055 + dalga * dalga_z * .2 * np.sqrt(.5 * (1 - pan_d))).astype(np.float32)
R += g_s * (np.roll(taban, 4800) * taban_z * .055 + dalga * dalga_z * .2 * np.sqrt(.5 * (1 + pan_d))).astype(np.float32)
# başak hışırtısı: esintide ince yüksek tıkırtı
his = renkli_gurultu(N, 2500, 9000, 0, 4) * (rng.random(N) < .004).astype(np.float32)
his = np.convolve(his, np.exp(-np.arange(200) / 30), 'same').astype(np.float32)
put(his * (dalga_z * .5 + .08) * .5 * g_s, 0, -.1)

# ── kâğıt: mektup çantadan çıkar (9.8), rüzgâr alır ve döner (12.2–18.8): genliği dönüş hızıyla atan dar bant hışırtı ──
kag = renkli_gurultu(N, 1500, 7000, -.2, 5)
kz = np.zeros(N, np.float32)
kz += np.exp(-((tt - 9.95) / .12) ** 2) * .6 + np.exp(-((tt - 10.3) / .08) ** 2) * .3
uc = (tt > tSal) & (tt < tVar)
a = np.where(uc, tt - tSal, 0)
kz += uc * (np.abs(np.sin(a * 3.4 * np.pi / 2 + .4)) ** 6) * np.exp(-a * .28) * .9
pan_k = np.where(uc, -.3 + .9 * np.clip(a / 6.6, 0, 1), -.3)
L += g_s * (kag * kz * .09 * np.sqrt(.5 * (1 - pan_k))).astype(np.float32); R += g_s * (kag * kz * .09 * np.sqrt(.5 * (1 + pan_k))).astype(np.float32)

# ── müzik ──
# yüzey: Mib ve Sib uzun yaylı; batışta Lab'a ve geri Mib'e
# yüzey: Mib (bekleyiş) → Do min (yolculuk) → Lab maj (çiçek: doruk, kabarır) → Mib add9 (cevap; sessizliğe söner)
for n, t0, d, v, at in (('Eb3', .4, 11.6, .34, 1.2), ('Bb2', .4, 11.6, .26, 1.2), ('G3', 3.0, 9.0, .16, 1.2),
                        ('C3', 12.0, 4.6, .34, 1.0), ('G3', 12.0, 4.6, .26, 1.0), ('Eb4', 12.0, 4.6, .16, 1.0),
                        ('Ab2', 16.4, 3.9, .9, 2.2), ('Eb3', 16.4, 3.9, .8, 2.2), ('C4', 16.4, 3.9, .62, 2.2), ('Ab4', 16.8, 3.5, .42, 2.0), ('Eb5', 17.2, 3.1, .26, 1.8),
                        ('Eb3', 20.2, 2.6, .5, .8), ('Bb3', 20.2, 2.6, .36, .8), ('G4', 20.2, 2.6, .24, .8), ('F4', 20.4, 2.4, .15, .8)):
    put(yayli(midi(n), d, v, at), t0, (midi(n) - 50) * .01)
# SORU (baş kalkınca), ikinci kez mektup elde (armonili)
def dizi(seq, t0, bpm=60, v=.55, pan=.1):
    t = t0; b = 60 / bpm
    for n, d in seq:
        for x in n.split('+'):
            if x != '-': put(piyano(midi(x), v, d * b * 1.4), t, pan + (midi(x) - 64) * .008)
        t += d * b
    return t
dizi([('Bb4', 1), ('Eb5', 1), ('D5', 1.4), ('Bb4', 2)], tBak + .1, v=.42)
dizi([('Bb4+Eb4', 1), ('Eb5+G4', 1), ('D5+Bb4', 1.2), ('Bb4+F4', 1.6)], tCik + .25, bpm=66, v=.38)
# YOL: rüzgâr mektubu alınca yükselen arpej; esintiyle hızlanır, konuşa doğru seyrelir
ak = [['Eb3', 'Bb3', 'G4', 'Bb4'], ['C3', 'G3', 'Eb4', 'G4'], ['Ab2', 'Eb3', 'C4', 'Eb4'], ['Bb2', 'F3', 'D4', 'F4']]
t = tSal; i = 0
while t < tVar - .2:
    u = (t - tSal) / (tVar - tSal); a4 = ak[min(3, int(u * 4))]
    put(piyano(midi(a4[i % 4]) + (12 if i % 8 >= 4 and u > .4 else 0), .3 + .12 * np.sin(np.pi * u), .9), t, -.25 + .5 * (i % 4) / 3)
    t += .3 + .14 * np.sin(np.pi * u) ** 2 * -1 + .12; i += 1
# ÇİÇEK: mektup taca konar; yüksek çanlar çiçeklerin yayılışıyla (pentatonik Mib)
pent = ['Eb6', 'F6', 'G6', 'Bb6', 'C7', 'Eb7', 'Bb5', 'G5']
# varış: mektup taca girer (tek, yumuşak piyano notası + çan)
put(piyano(midi('Eb6'), .34, 2.5), tVar - .02, .35); put(can(midi('Eb6'), .4, 5), tVar, .35); put(can(midi('Bb6'), .26, 5), tVar + .03, .45)
for k in range(26):
    tk = tVar + .25 + 2.8 * (k / 26) ** 1.2 + rng.random() * .15
    put(can(midi(pent[int(rng.random() * len(pent))]), .2 * (1 - k / 34), 3.0), tk, .1 + .6 * rng.random())
# ÇİÇEK doruğu: Lab majör kırık akor yükselir (17–20 sn)
for j, (n, tj) in enumerate([('Ab3', 16.9), ('C4', 17.25), ('Eb4', 17.6), ('Ab4', 17.95), ('C5', 18.3), ('Eb5', 18.65), ('G5', 19.0), ('Ab5', 19.35)]):
    put(piyano(midi(n), .36 + .02 * j, 1.8), tj, -.3 + .08 * j)
# CEVAP: yapraklar kuryeye dönerken; sorunun inen eşi
dizi([('Bb5', 1), ('G5', 1), ('F5', 1.3), ('Eb5+G4', 2.6)], 19.7, bpm=56, v=.4, pan=-.1)
put(piyano(midi('Eb3'), .26, 2.6), 22.4, -.2); put(piyano(midi('Bb3'), .22, 2.4), 22.45, -.1); put(piyano(midi('F4'), .18, 2.2), 22.55, .1)

# ── yankı (FFT konvolüsyonu) ──
def yanki(x, sure=3.0, kuru=.78, islak=.34, tohum=7):
    r = np.random.default_rng(tohum); n = int(sure * SR); t = np.arange(n) / SR
    ir = r.standard_normal(n) * np.exp(-t / .7); ir[:int(.025 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    F = 1 << int(np.ceil(np.log2(len(x) + n))); y = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
    return (x * kuru + y * islak).astype(np.float32)
L = yanki(L, tohum=7); R = yanki(R, tohum=8)
# efekt yolu: müzikten sonra, yankısız (açık hava); düzeyi müziğin etkin düzeyine göre
if EFEKT:
    m_rms = np.sqrt(np.mean(L[int(8 * SR):int(20 * SR)] ** 2 + R[int(8 * SR):int(20 * SR)] ** 2) / 2)
    for z, hdb in EFL:
        g = m_rms * 10 ** (hdb / 20) / doruk_rms(z); L += z[:, 0] * g; R += z[:, 1] * g
# giriş ve çıkış
e = zarf([(0, 0), (.8, 1), (22.8, 1), (24.9, 0)], N); L *= e; R *= e

# ── yaz + düzey: ffmpeg loudnorm (-14 LUFS, -1 dBTP) ──
ham = HERE / 'ses_ham.wav'; son = HERE / 'ses.wav'
x = np.stack([L, R], 1); x = x / (np.abs(x).max() + 1e-9) * .7
with wave.open(str(ham), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes())
# iki geçişli doğrusal loudnorm (tek geçiş dinamik kipte hedefi tutturmuyor ve dinamiği eziyor)
import json as _j
olc = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(ham), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=18:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = _j.loads(olc[olc.rindex('{'):olc.rindex('}') + 1])
af = (f"loudnorm=I=-16:TP=-1.5:LRA=18:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ham), '-af', af, '-ar', str(SR), str(son)], check=True)
ham.unlink()
print('yazıldı:', son)
