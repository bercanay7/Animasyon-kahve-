"""Son miks: anlatım + müzik (konuşma altında kısılır) + ses efektleri → audio/mix.wav (-14 LUFS, ≤ -1 dBTP)

python3 tools/mix.py            # tam miks
python3 tools/mix.py --stems    # ayrıca audio/stems/*.wav
python3 tools/mix.py --vo en/vo_en.wav --out audio/mix_en.wav   # İngilizce dublajlı miks
"""
import json, sys, os, re
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln
from scipy import signal
from scipy.ndimage import maximum_filter1d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
rng = np.random.default_rng(7)
A = lambda p: os.path.join(ROOT, p)

DUR = float(re.search(r'window\.DUR\s*=\s*([\d.]+)', open(A('timeline.js')).read()).group(1))
N = int(np.ceil(DUR * SR))
db = lambda g: 10 ** (g / 20)


# ——— yardımcılar ———
def env_ad(n, a, d, shape=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * shape / max(d, 1e-4))
    return e

def bp(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos')
    return signal.sosfilt(sos, x)

def lp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'lowpass', fs=SR, output='sos'), x)

def hp(x, f, order=2):
    return signal.sosfilt(signal.butter(order, f, 'highpass', fs=SR, output='sos'), x)

def sweep_filter(x, f0, f1, q=1.2):
    """zamanla değişen band geçiren (durum-değişken süzgeç, örnek örnek)"""
    n = len(x); f = np.geomspace(f0, f1, n) if f0 > 0 and f1 > 0 else np.linspace(f0, f1, n)
    g = np.tan(np.pi * np.clip(f, 20, SR * .45) / SR); k = 1 / q
    a1 = 1 / (1 + g * (g + k)); a2 = g * a1; a3 = g * a2
    y = np.zeros(n); ic1 = ic2 = 0.0
    for i in range(n):
        v3 = x[i] - ic2; v1 = a1[i] * ic1 + a2[i] * v3; v2 = ic2 + a2[i] * ic1 + a3[i] * v3
        ic1 = 2 * v1 - ic1; ic2 = 2 * v2 - ic2; y[i] = v1
    return y

def norm(x, peak=.9):
    m = np.max(np.abs(x)) + 1e-9
    return x * (peak / m)

def resample_rate(x, rate):
    if abs(rate - 1) < 1e-4: return x
    idx = np.arange(0, len(x) - 1, rate)
    return np.interp(idx, np.arange(len(x)), x)

def fade(x, fi, fo):
    n = len(x); x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a > 0: x[:min(a, n)] *= np.sin(np.linspace(0, np.pi / 2, a))[:min(a, n)] ** 2
    if b > 0: x[max(0, n - b):] *= np.cos(np.linspace(0, np.pi / 2, b))[-min(b, n):] ** 2
    return x


# ——— sentez sesler ———
def s_whoosh(len=.8, rev=False, down=False, **_):
    n = int(len * SR); t = np.linspace(0, 1, n)
    x = rng.standard_normal(n)
    f0, f1 = (2500, 250) if down else (300, 2400)
    y = sweep_filter(x, f0, f1, .9) + .5 * sweep_filter(rng.standard_normal(n), f0 * 1.6, f1 * 1.6, 1.4)
    e = np.sin(np.pi * t) ** 1.5 if not rev else t ** 2.2 * (1 - np.clip((t - .96) / .04, 0, 1))
    return norm(y * e)

def s_boom(big=False, **_):
    d = 3.2 if big else 1.6; n = int(d * SR); t = np.arange(n) / SR
    f = 46 + 44 * np.exp(-t * 7); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * (1.4 if big else 2.6))
    click = lp(rng.standard_normal(n), 900) * np.exp(-t * 40) * .6
    rum = lp(rng.standard_normal(n), 140, 4) * np.exp(-t * 1.6) * (2.4 if big else 1.2)
    y = np.tanh(1.6 * (body + click + rum))
    return norm(y)

def s_knock(rate=1, **_):
    n = int(.35 * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * rate * t) * np.exp(-t * dcy) for f, a, dcy in [(190, 1, 28), (430, .5, 40), (780, .3, 60), (1500, .12, 90)])
    y += bp(rng.standard_normal(n), 800, 4000) * np.exp(-t * 160) * .5
    return norm(y)

def s_chime(rate=1, **_):
    f0 = 660 * rate; n = int(3.2 * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6)) * np.exp(-t * dcy) for r, a, dcy in [(1, 1, 1.2), (2.01, .45, 2.0), (2.76, .35, 2.6), (5.4, .15, 4.5), (8.93, .06, 7)])
    y *= np.minimum(1, t / .004)
    return norm(y)

def s_clink(**_):
    n = int(.9 * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(2350, 1, 7), (3830, .6, 9), (6120, .35, 12), (2410, .5, 7.5)])
    return norm(y * np.minimum(1, t / .001))

def s_shimmer(len=1.4, **_):
    n = int((len + 1.6) * SR); y = np.zeros(n)
    for k in range(14):
        t0 = int(rng.uniform(0, len) * SR); f = rng.choice([1320, 1760, 1980, 2640, 2960, 3520]) * rng.uniform(.995, 1.005)
        m = n - t0; tt = np.arange(m) / SR
        y[t0:] += rng.uniform(.3, .8) * np.sin(2 * np.pi * f * tt) * np.exp(-tt * rng.uniform(3, 6))
    t = np.arange(n) / SR
    y += hp(rng.standard_normal(n), 6000) * .05 * np.exp(-((t - len * .5) / (len * .5)) ** 2)
    return norm(y)

def s_tick(rate=1, **_):
    n = int(.12 * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 2600 * rate * t) * .6 + np.sin(2 * np.pi * 4300 * rate * t) * .4) * np.exp(-t * 70)
    y += bp(rng.standard_normal(n), 2000, 9000) * np.exp(-t * 300)
    return norm(y)

def s_hoof(**_):
    n = int(.25 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (110 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 30) + lp(rng.standard_normal(n), 1200) * np.exp(-t * 60) * .8
    return norm(y)

def s_thud(**_):
    n = int(.6 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * np.cumsum(55 + 50 * np.exp(-t * 25)) / SR) * np.exp(-t * 9) + lp(rng.standard_normal(n), 500) * np.exp(-t * 35) * .7
    return norm(np.tanh(1.5 * y))

def s_sting(rate=1, **_):
    n = int(2.2 * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for f in [98, 146.8, 196, 233.1]:
        for det in (-.25, .25):
            y += signal.sawtooth(2 * np.pi * f * rate * (1 + det / 100) * t + rng.uniform(0, 6))
    y = lp(y, 1400)
    e = np.minimum(1, t / .06) * np.exp(-t * 1.6)
    return norm(y * e)

def s_riser(len=2.0, **_):
    n = int(len * SR); t = np.linspace(0, 1, n)
    y = sweep_filter(rng.standard_normal(n), 200, 3200, 2.0)
    f = 110 * 2 ** (t * 2); y += .25 * np.sin(2 * np.pi * np.cumsum(f) / SR) * t
    return norm(y * t ** 2.5 * (1 - np.clip((t - .97) / .03, 0, 1)))

def s_scratch(rate=1, **_):
    n = int(.3 * SR); t = np.arange(n) / SR
    y = bp(rng.standard_normal(n), 1800 * rate, 6000) * np.sin(np.pi * np.clip(t / .22, 0, 1)) ** .7
    return norm(y)

def s_pen(len=2.0, **_):
    n = int(len * SR); t = np.arange(n) / SR
    strokes = np.zeros(n); s = 0
    while s < len:
        d = rng.uniform(.08, .28); a = int(s * SR); b = min(n, int((s + d) * SR))
        strokes[a:b] = np.sin(np.linspace(0, np.pi, b - a)) * rng.uniform(.5, 1); s += d + rng.uniform(.02, .12)
    grit = bp(rng.standard_normal(n), 2500, 8000) * (1 + .5 * np.sin(2 * np.pi * 37 * t))
    return norm(grit * strokes)

def s_page(**_):
    n = int(.7 * SR); t = np.arange(n) / SR
    y = bp(rng.standard_normal(n), 900, 7000) * (np.sin(np.pi * np.clip(t / .55, 0, 1)) ** 1.5) * (1 + .6 * np.sin(2 * np.pi * 23 * t) * np.exp(-t * 3))
    y += lp(rng.standard_normal(n), 300) * np.exp(-t * 12) * .4
    return norm(y)

def s_crack(**_):
    n = int(2.5 * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for k in range(9):
        t0 = int((k * .05 + rng.uniform(0, .03)) * SR); m = n - t0; tt = np.arange(m) / SR
        y[t0:] += hp(rng.standard_normal(m), 1500) * np.exp(-tt * 120) * (1 - k / 12)
    y += np.sin(2 * np.pi * 4200 * t) * np.exp(-t * 3) * .08 + np.sin(2 * np.pi * 6650 * t) * np.exp(-t * 4) * .05
    y += lp(rng.standard_normal(n), 120, 4) * np.exp(-t * 1.5) * 1.5
    return norm(y)

def s_stop(**_):
    return norm(np.concatenate([s_thud() * .8 + np.pad(s_knock(rate=.8) * .4, (0, int(.25 * SR)))[:int(.6 * SR)]]))

def s_ticks(len=4, **_):
    n = int(len * SR); y = np.zeros(n); k = 0
    tk = s_tick(rate=.55) * .6
    for s in np.arange(0, len, .5):
        a = int(s * SR); seg = tk if k % 2 == 0 else resample_rate(tk, 1.2) * .7
        m = min(n - a, seg.shape[0]); y[a:a + m] += seg[:m]; k += 1
    return y

def s_room(len=10, **_):
    n = int(len * SR)
    y = lp(rng.standard_normal(n), 380, 2) + .3 * lp(rng.standard_normal(n), 1800, 2)
    return norm(y, .5)

SYNTH = dict(whoosh=s_whoosh, boom=s_boom, knock=s_knock, chime=s_chime, clink=s_clink, shimmer=s_shimmer, tick=s_tick, hoof=s_hoof,
             thud=s_thud, sting=s_sting, riser=s_riser, scratch=s_scratch, pen=s_pen, page=s_page, crack=s_crack, stop=s_stop, ticks=s_ticks, room=s_room)
# döngü sentezleri tam uzunlukta üretilir
LOOP_SYNTH = {'ticks', 'room'}
# yankı gönderimi (dB), ad başına
SEND = dict(chime=-6, shimmer=-6, boom=-10, thunder=-12, eagle=-9, wings=-14, sting=-8, clink=-8, lock=-12, chains=-12, crack=-6,
            rock_crash=-12, knock=-12, door=-12, riser=-10, whoosh=-14, thud=-14, alarm=-14, page=-18)

CLIPS = {}
def clip(name):
    if name not in CLIPS:
        alias = {'scrape': ('stone_scrape', .55, .9)}
        if name in alias:
            src, off, ln = alias[name]; y = clip(src)
            seg = y[int(off * SR):int((off + ln) * SR)]
            CLIPS[name] = norm(fade(seg, .02, .4))
        else:
            y, _ = librosa.load(A(f'audio/sfx/{name}.mp3'), sr=SR, mono=True)
            y = y - np.mean(y)
            e = np.abs(y); on = np.argmax(e > e.max() * .03)
            y = y[max(0, on - int(.008 * SR)):]
            CLIPS[name] = norm(y)
    return CLIPS[name]

def peak_pos(y):
    e = np.convolve(y ** 2, np.ones(480) / 480, 'same')
    return int(np.argmax(e))

def loop_to(y, n, xf=.6):
    """y'yi n örneğe eşit güçlü çapraz geçişlerle döngüler"""
    x = int(xf * SR)
    if len(y) <= 2 * x: y = np.tile(y, 3)
    out = np.zeros(n + len(y)); pos = 0; w = np.linspace(0, np.pi / 2, x)
    while pos < n:
        seg = y.copy(); seg[:x] *= np.sin(w); seg[-x:] *= np.cos(w)
        out[pos:pos + len(seg)] += seg; pos += len(seg) - x
    return out[:n]


def place(bus, x, t0, pan=0.0):
    a = int(round(t0 * SR))
    if a < 0:
        x = x[..., -a:].copy(); a = 0
        k = min(int(.08 * SR), x.shape[-1]); x[..., :k] *= np.linspace(0, 1, k)  # ilk karede ani başlangıç olmasın
    m = min(len(x), N - a)
    if m <= 0: return
    if x.ndim == 1:
        th = (pan + 1) * np.pi / 4
        bus[0, a:a + m] += x[:m] * np.cos(th)
        bus[1, a:a + m] += x[:m] * np.sin(th)
    else:
        bus[:, a:a + m] += x[:, :m]


# dile özel efekt düzeltmeleri (İngilizce anlatımın sözcük yerleri farklı): (yaklaşık zaman, ad, ek dB)
EN_SFX = [(1.70, 'chains', -6), (402.05, 'whoosh', -6), (183.16, 'clink', -4), (89.45, 'thunder', -3)]
def build_sfx(lang='tr'):
    ev = json.load(open(A('audio/sfx_events.json')))
    if lang == 'en':
        for e in ev:
            for t_, n_, d_ in EN_SFX:
                if e['name'] == n_ and abs(e['t'] - t_) < .5: e['g'] = e.get('g', 0) + d_
    dry = np.zeros((2, N)); send = np.zeros((2, N))
    for e in ev:
        name = e['name']; g = db(e.get('g', 0)); rate = e.get('rate', 1)
        if e.get('loop'):
            n = int(e['len'] * SR)
            if name in LOOP_SYNTH:
                L = SYNTH[name](len=e['len'] + .1); R = SYNTH[name](len=e['len'] + .1) if name == 'room' else L
                L, R = L[:n], R[:n]
            else:
                y = resample_rate(clip(name), rate); off = int(e.get('off', 0) * SR)
                y = np.roll(y, -off)
                L = loop_to(y, n); R = loop_to(np.roll(y, len(y) // 2), n)
            L = fade(L, e.get('fi', 1), e.get('fo', 1)); R = fade(R, e.get('fi', 1), e.get('fo', 1))
            x = np.stack([L, R]) * g * .7071
            place(dry, x, e['t'])
            if name in SEND: place(send, x * db(SEND[name]), e['t'])
            continue
        if name in SYNTH:
            kw = {k: e[k] for k in ('len', 'rev', 'down', 'big', 'rate') if k in e}
            y = SYNTH[name](**kw)
            if 'len' in e and name not in ('whoosh', 'riser', 'shimmer', 'pen'):
                y = y[:int(e['len'] * SR)]
            if name == 'shimmer' and 'len' in e:  # parıltı kuyruğu len + .4 sn'de biter
                y = y[:int((e['len'] + .4) * SR)]
        else:
            y = resample_rate(clip(name), rate)
            y = y[int(e.get('off', 0) * SR):]
            if 'len' in e: y = y[:int(e['len'] * SR)]
        y = fade(y, e.get('fi', .003), e.get('fo', .02))
        t0 = e['t'] - (peak_pos(y) / SR if e.get('at') == 'peak' else 0)
        pan = e.get('pan', 0.0)
        place(dry, y * g, t0, pan)
        if name in SEND: place(send, y * g * db(SEND[name]), t0, pan)
    return dry, send


def reverb_ir(dur=2.4, pre=.02):
    n = int(dur * SR); t = np.arange(n) / SR
    ir = []
    for ch in range(2):
        x = rng.standard_normal(n) * np.exp(-t * 6.9 / dur)
        x = lp(x, 5200) * (1 - np.exp(-t * 300))
        ir.append(np.concatenate([np.zeros(int(pre * SR)), x]))
    ir = np.array(ir); ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    return ir

def apply_reverb(x, ir):
    return np.stack([signal.fftconvolve(x[c], ir[c])[:N] for c in range(2)])


def envelope(x, win=.03):
    w = int(win * SR)
    e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
    return e

def smooth_gain(target, att=.08, rel=.6):
    """tek kutuplu, ayrı saldırı/bırakma ile kazanç yumuşatma (100 Hz kontrol hızı)"""
    hop = SR // 100; tg = target[::hop]; g = np.empty_like(tg); cur = 1.0
    aa, ar = np.exp(-1 / (att * 100)), np.exp(-1 / (rel * 100))
    for i, v in enumerate(tg):
        c = aa if v < cur else ar; cur = c * cur + (1 - c) * v; g[i] = cur
    return np.interp(np.arange(len(target)), np.arange(len(g)) * hop, g)


def peq(x, f0, gdb, q=1.0):
    A = 10 ** (gdb / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)

def compress(x, thr_db, ratio=3.0, att=.008, rel=.1):
    w = int(.005 * SR); p = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same')) + 1e-9
    lvl = 20 * np.log10(p); over = np.maximum(0, lvl - thr_db); gr = -over * (1 - 1 / ratio)
    hop = SR // 1000; g = gr[::hop]; out = np.empty_like(g); cur = 0.0
    aa, ar = np.exp(-1 / (att * 1000)), np.exp(-1 / (rel * 1000))
    for i, v in enumerate(g):
        c = aa if v < cur else ar; cur = c * cur + (1 - c) * v; out[i] = cur
    gg = np.interp(np.arange(len(x)), np.arange(len(out)) * hop, out)
    return x * 10 ** (gg / 20), gg

def voice_chain(vo, sentence_gains=True):
    cues = json.loads(re.search(r'window\.CUES = (\{.*?\});', open(A('timeline.js')).read()).group(1))
    gains = {'F05': -5, 'E04': -3.5, 'F04': -3, 'H04': -3, 'C08': 2, 'E02': 2.5, 'A04': 1.5} if sentence_gains else {}
    g = np.ones(len(vo))
    for k, d in gains.items():
        if k in cues:
            a, b = int(cues[k]['s'] * SR) - int(.05 * SR), int(cues[k]['e'] * SR) + int(.1 * SR)
            g[a:b] = db(d)
    g = np.convolve(g, np.ones(int(.04 * SR)) / int(.04 * SR), 'same')
    vo = vo * g
    vo = peq(vo, 250, -2, .9); vo = peq(vo, 3500, 1.5, .8)
    L = pyln.Meter(SR).integrated_loudness(vo)
    vo, gr = compress(vo, L + 6, 3.0)
    vo = limiter(vo[None, :], db(pyln.Meter(SR).integrated_loudness(vo) + 13))[0]
    return vo

def limiter(x, ceil=.89, look=.005, rel=.08):
    a = np.max(np.abs(x), axis=0)
    w = int(look * SR)
    pk = maximum_filter1d(a, w + 1, origin=-(w // 2))  # ileriye bakan tepe
    need = np.minimum(1, ceil / (pk + 1e-9))
    hop = 48; tg = need[::hop]; g = np.empty_like(tg); cur = 1.0; ar = np.exp(-hop / (rel * SR))
    for i, v in enumerate(tg):
        cur = v if v < cur else ar * cur + (1 - ar) * v; g[i] = cur
    gg = np.interp(np.arange(x.shape[1]), np.arange(len(g)) * hop, g)
    gg = np.minimum(gg, need)  # kesin tavan
    return x * gg


def true_peak(x):
    up = signal.resample_poly(x, 4, 1, axis=1)
    return 20 * np.log10(np.max(np.abs(up)) + 1e-12)


def main():
    stems = '--stems' in sys.argv
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    vo_path, out_path = A(arg('--vo', 'vo/vo.wav')), A(arg('--out', 'audio/mix.wav'))
    meter = pyln.Meter(SR)
    vo, sr = sf.read(vo_path, always_2d=False)
    assert sr == SR
    vo = np.pad(vo, (0, max(0, N - len(vo))))[:N].astype(np.float64)
    vo = hp(vo, 70)
    vo *= db(-16 - meter.integrated_loudness(vo))
    vo = voice_chain(vo, sentence_gains=vo_path.endswith('vo/vo.wav'))
    vo *= db(-16 - meter.integrated_loudness(vo))   # anlatım -16 LUFS
    ir = reverb_ir()
    # anlatım: hafif oda sıcaklığı
    vo2 = np.stack([vo, vo])
    vo_send = apply_reverb(vo2 * db(-26), reverb_ir(1.2))

    # müzik
    mpath = A('audio/music.wav')
    if os.path.exists(mpath):
        mu, msr = sf.read(mpath, always_2d=True)
        mu = mu.T.astype(np.float64)
        if msr != SR: mu = librosa.resample(mu, orig_sr=msr, target_sr=SR)
        if mu.shape[0] == 1: mu = np.vstack([mu, mu])
        mu = np.pad(mu, ((0, 0), (0, max(0, N - mu.shape[1]))))[:, :N]
        mu = np.stack([signal.sosfilt(signal.butter(4, 35, 'highpass', fs=SR, output='sos'), ch) for ch in mu])
        mu = np.stack([peq(ch, 60, -2.5, .7) for ch in mu])
        mu *= db(-21 - meter.integrated_loudness(mu.T))
        cues_ = json.loads(re.search(r'window\.CUES = (\{.*?\});', open(A('timeline.js')).read()).group(1))
        extra = np.ones(N)
        for a_, b_, d_ in [(cues_['G10']['s'] - .15, cues_['G10']['e'] + .1, -4.5), (22.7, 23.15, -2), (16.9, 18.8, -5), (141.0, 141.7, -3), (150.6, 151.7, -4), (267.3, 268.1, -6), (268.1, 270.9, -4), (270.9, 272.4, -6)]:
            extra[int(a_ * SR):int(b_ * SR)] = db(d_)
        extra = np.convolve(extra, np.ones(int(.15 * SR)) / int(.15 * SR), 'same')
        mu *= extra
        # konuşma altında kısma (-7 dB), ön-bakışlı
        ve = envelope(vo); thr = db(-42)
        act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1)
        target = db(-3 * act)  # müzik zaten konuşma altına göre bestelendi; hafif ek kısma
        look = int(.12 * SR); target = np.concatenate([target[look:], np.ones(look)])
        duck = smooth_gain(target, .1, .7)
        mu *= duck
    else:
        print('UYARI: audio/music.wav yok, müziksiz miks')
        mu = np.zeros((2, N))

    fx, fx_send = build_sfx('en' if 'vo_en' in vo_path else 'tr')
    hp30 = signal.butter(4, 30, 'highpass', fs=SR, output='sos')
    fx = np.stack([signal.sosfilt(hp30, ch) for ch in fx]); fx_send = np.stack([signal.sosfilt(hp30, ch) for ch in fx_send])
    # efektleri konuşma altında hafifçe kıs (-3 dB), anlamı örtmesin
    ve = envelope(vo); act = np.clip((20 * np.log10(ve + 1e-9) + 42) / 10, 0, 1)
    fduck = smooth_gain(db(-3 * act), .05, .5)
    fx *= fduck; fx_send *= fduck
    wet = apply_reverb(fx_send, ir)

    mix = vo2 + vo_send + mu + fx + wet
    # ana: hafif glue, sınırlayıcı, yüksek ses
    mix = limiter(mix, .7)
    L = meter.integrated_loudness(mix.T)
    mix *= db(-14 - L)
    # gerçek tepe tavanı (--tp): İngilizce sibilantlar AAC kodlamada taşmasın diye EN için -2.0 kullanılır
    tpT = float(arg('--tp', '-1.0'))
    mix = limiter(mix, db(tpT - .6))
    for _ in range(8):
        tp = true_peak(mix)
        if tp <= tpT: break
        mix = limiter(mix, db(tpT - .6 - (tp - tpT) - .1))
    L2 = meter.integrated_loudness(mix.T)
    print(f'LUFS {L2:.2f}  TP {true_peak(mix):.2f} dBTP  süre {N / SR:.2f}s')
    sf.write(out_path, mix.T.astype(np.float32), SR, subtype='PCM_24')
    if stems:
        os.makedirs(A('audio/stems'), exist_ok=True)
        for nm, x in [('vo', vo2 + vo_send), ('music', mu), ('sfx', fx + wet)]:
            sf.write(A(f'audio/stems/{nm}.wav'), x.T.astype(np.float32), SR, subtype='FLOAT')


if __name__ == '__main__':
    main()
