#!/usr/bin/env python3
"""Van Gogh miksi: seslendirme + müzik (konuşmanın altında kısılır) + ortam yatakları (plan setine göre) + nokta efektler.
Girdi: vo/vo.wav, audio/music.wav, audio/efekt/*.mp3 (ElevenLabs, kayit.json), vo/planlar.json (tools/plan_disa.js), timeline.js
Çıktı: audio/mix.wav (48 kHz stereo; -14 LUFS / -1 dBTP iki geçişli loudnorm). STEM=muzik → yalnız müzik izinin miksteki kazancıyla (telefon denetimi)
"""
import json, re, wave, subprocess, os
from pathlib import Path
import numpy as np
SR = 48000; HERE = Path(__file__).resolve().parent; FILM = HERE.parent
TL = (FILM / 'timeline.js').read_text(); CUES = json.loads(TL.split('window.CUES = ')[1].split(';\n')[0]); WORDS = json.loads(TL.split('window.WORDS = ')[1].split(';\n')[0])
DUR = float(re.search(r'window\.DUR = ([\d.]+)', TL).group(1)); N = int(DUR * SR)
PL = json.loads((FILM / 'vo' / 'planlar.json').read_text())['planlar']
def W(i, w, n=0):
    k = 0
    for x in WORDS:
        if x['id'] == i and x['w'].startswith(w):
            if k == n: return x['s']
            k += 1
    print('kelime yok', i, w); return CUES[i]['s']
def oku(p, ch=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()
def db(x): return 10 ** (x / 20)
vo = oku(FILM / 'vo' / 'vo.wav', 1)[:, 0]; vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
mu = oku(HERE / 'music.wav'); mu = np.pad(mu, ((0, max(0, N - len(mu))), (0, 0)))[:N]
# konuşma zarfı: 20 ms RMS, atak 80 ms, bırakma 450 ms
h = int(.02 * SR); r = np.sqrt(np.convolve(vo ** 2, np.ones(h) / h, 'same'))[::h]
kon = (r > db(-42)).astype(float); env = np.zeros_like(kon); a = 1 - np.exp(-1 / (.08 / .02)); b = 1 - np.exp(-1 / (.45 / .02))
for i in range(1, len(kon)): env[i] = env[i - 1] + ((a if kon[i] > env[i - 1] else b) * (kon[i] - env[i - 1]))
duck = np.interp(np.arange(N) / SR, np.arange(len(env)) * .02, db(-7) * (1 - env) + db(-15) * env)   # müzik: boşlukta -7 dB, konuşma altında -15 dB
muzik = mu * duck[:, None]
fx = np.zeros((N, 2), np.float32)
EF = {k: oku(HERE / 'efekt' / f'{k}.mp3') for k in ['oda', 'zarf', 'tren', 'ruzgar', 'galeri', 'kalem', 'lamba']}
EF['zarf'] = EF['zarf'][int(1.25 * SR):]   # dosyada vuruş 1,35. saniyede: ses inişle aynı anda
EF['lamba'] = EF['lamba'][:int(1.6 * SR)] * np.linspace(1, 0, int(1.6 * SR))[:, None]
for k in EF: EF[k] /= (np.max(np.abs(EF[k])) + 1e-9)           # her efekt kendi tepesine (yatak ölçeği taşmasın)
def koy(k, t, g, d=None, fi=.05, fo=.3):
    s = EF[k]
    if d is not None:   # döngülü yatak
        n = int(d * SR); reps = int(np.ceil(n / len(s))) + 1; s = np.concatenate([s] * reps)[:n]
    s = s.copy(); f1, f2 = int(fi * SR), int(fo * SR)
    if f1: s[:f1] *= np.linspace(0, 1, f1)[:, None]
    if f2 and len(s) > f2: s[-f2:] *= np.linspace(1, 0, f2)[:, None]
    i0 = int(t * SR); i1 = min(N, i0 + len(s))
    if i0 < N: fx[i0:i1] += s[:i1 - i0] * db(g)
YATAK = {'oda': ('oda', -30), 'masa': ('oda', -33), 'salon': ('galeri', -30), 'tarla': ('ruzgar', -27), 'tb_sari_ev': ('ruzgar', -36), 'tb_selvili_tarla': ('ruzgar', -32), 'tb_firtina': ('ruzgar', -28), 'tren': ('ruzgar', -38), 'tb_rhone': ('ruzgar', -38)}
for p in PL:
    y = YATAK.get(p['sahne']);
    if y and p['d'] > .2: koy(y[0], p['s'], y[1], d=p['d'] + .4, fi=.3, fo=.4)
    if p['sahne'] == 'tren' and p['id'] in ('B08', 'D03', 'H01t', 'I01c'): koy('tren', p['s'] + .2, -20 if p['id'] not in ('H01t', 'I01c') else -26, fi=.4, fo=1.2)
# nokta efektler (sözcüğe bağlı; v2: görüntüdeki inişle eşleşir)
koy('zarf', W('A01', 'bir', 1) + .25 + .6 - .05, -20, fi=.02)                       # "her hafta bir zarf daha": A01b'de düşen zarf

for i in range(0, 40, 3):
    t_ = CUES['A02']['s'] + i * .12 - 1.2 + .5
    if t_ >= CUES['A02']['s']: koy('zarf', t_, -28 - (i % 7), fi=.02)
for i in range(0, 26, 2):
    t_ = W('D07', 'sarı') + i * .28 + .45
    if t_ < CUES['E01']['s'] - .3: koy('zarf', t_, -28, fi=.02)
koy('zarf', W('B01', 'pusula') + .1, -26, fi=.02)                                     # pusula açılır
koy('zarf', W('D02', 'ertesi'), -26, fi=.1)                                            # telgraf kapı altından kayar
koy('zarf', CUES['D04']['s'] + .8, -28, fi=.02); koy('zarf', CUES['D04']['s'] + 1.2, -30, fi=.02)   # iki bilet
for i in range(3): koy('zarf', W('H06', 'üç') - .3 + i * .45 + .5, -24, fi=.02)          # üç cilt masaya konur (v3: sözcüğe bağlı)
koy('zarf', W('C02', 'yollar') - .5, -30, fi=.05); koy('zarf', W('C02', 'ikincisi') + .3, -28, fi=.05)   # zarf gider, açılmış döner
for i in range(2): koy('zarf', W('C08', 'ikimizin') + .3 + i * .15, -30, fi=.05)      # iki zarf yan yana kayar
koy('zarf', CUES['I03']['s'] + .5, -28, fi=.02)                                        # son zarf açılır
koy('kalem', CUES['C01']['s'] + .2, -26); koy('kalem', CUES['G07']['s'] + .3, -28); koy('kalem', W('H03', 'birer'), -30)
koy('kalem', W('F03', 'amcasından'), -26)                                              # doğum mektubunda ad yazılır (v3: F03b)
koy('kalem', W('F07', 'deftere') - .2, -28); koy('kalem', CUES['D02']['s'] + .2, -30); koy('kalem', CUES['H09']['s'] + .3, -30); koy('kalem', W('G07', 'biz') - .2, -30)
koy('lamba', CUES['G11']['e'] + .3, -27, fi=.15, fo=.3)                                # lamba cümle bittikten sonra söner
koy('ruzgar', W('G09', 'öldü'), -22, d=CUES['G10']['s'] - W('G09', 'öldü'), fi=.8, fo=1.0)   # ölüm anı: yalnız rüzgâr
if os.environ.get('STEM') == 'muzik': mix = muzik
else: mix = muzik + fx + vo[:, None] * db(0)
tmp = HERE / '_mix_ham.wav'
with wave.open(str(tmp), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); x = mix / (np.max(np.abs(mix)) + 1e-9) * .9; w.writeframes((x * 32767).astype(np.int16).tobytes())
out = HERE / ('muzik_stem.wav' if os.environ.get('STEM') == 'muzik' else 'mix.wav')
m = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(tmp), '-af', 'loudnorm=I=-14:TP=-1:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-af', af, '-ar', str(SR), str(out)]); tmp.unlink()
print(out.name, 'giriş', js['input_i'], 'LUFS')
