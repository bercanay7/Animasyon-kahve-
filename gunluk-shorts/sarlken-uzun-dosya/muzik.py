"""
muzik.py — "ŞARLKEN" belgeseli için tamamen kodla sentezlenmiş, Rönesans esintili üretken müzik.

Tüm sesler numpy/scipy ile sentezdir (harici örnek/ses dosyası YOK, telifli melodi YOK; besteler tohumlu üretken ve özgün).
Enstrümanlar : lavta (Karplus–Strong, çift kurs), klavsen benzeri pluck, portatif org/regal, yaylı drone/çello (testere tablosu +
               vibrato + gövde rezonansı), formant süzgeçli koro pedi, çerçeve davulu, tef, gong, çan, timpani.
Armoni       : modal (Dorian / Mixolydian / Aeolian; c7'de Frigiyen, c9'da Lidyen renk). Tempo 58–84 bpm; her cue kendi tonikinde,
               cue sınırlarında yalnızca açık beşli (üçlüsüz) yatak → komşu cue'larla armonik çatışma olmaz.
Yapı         : her bölüm için ayrı 'cue'. Cue uzunluğu = bölüm + 3 sn kart + yarım çapraz geçişler (4–8 sn) ≈ bölüm + 7…11 sn;
               cue'lar eşit güçlü çapraz geçişle birleşir (merkez: bölüm kartı boşluğunun ortası). Yoğunluk eğrileri (tırmanma/boşalma)
               timeline.json'daki cümle kimliklerine çıpalanır (örn. Villalar, Mühlberg, Viyana, Cezayir fırtınası): ses yamalanınca
               çıpalar yeni zamanlara göre yeniden çözülür. c0'da gerilim yükselir; ana başlık anında (c0 t1 + 0,4 sn) TEK vuruş + altın tonlu
               D majör açılış; c13 sonunda soru açık kalır ama müzik çözülür ve söner (kuyruk süresi --tail).
Reverb       : algoritmik salon IR'ı (RT60≈2,2 sn, 500 Hz–1 kHz) + scipy.signal.fftconvolve.
Seviye       : ham müzik bandı (ducking ÖNCESİ) ortalama −27,5 dBFS RMS; ducking/yükseliş/EQ miks.py'dedir.

Kullanım (ayrı): python3 muzik.py --cue c3 --out /tmp/c3.wav     (tek cue önizleme)
                 python3 muzik.py --all --out /tmp/music.wav    (ducking'siz tüm müzik)
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import ses_dsp as D
from ses_dsp import SR, rng_for

HERE = os.path.dirname(os.path.abspath(__file__))


# ═══════════════════════════ modlar ve akorlar ═══════════════════════════
MODES = {
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
}


def deg_midi(tonic, mode, d):
    """Derece (tamsayı, negatif/7+ olabilir) → MIDI notası. tonic: ana ses MIDI numarası."""
    o, i = divmod(int(d), 7)
    return tonic + 12 * o + MODES[mode][i]


CHORD_EXT = {
    "": [0, 2, 4],
    "5": [0, 4],
    "sus2": [0, 1, 4],
    "sus4": [0, 3, 4],
    "add9": [0, 2, 4, 8],
    "7": [0, 2, 4, 6],
    "6": [0, 2, 4, 5],
}


def chord_degs(root, ext=""):
    return [root + k for k in CHORD_EXT[ext]]


# ═══════════════════════════ enstrümanlar (mono float64 döner) ═══════════════════════════
# referans seviyeleri (dB RMS; vel=0.7, kazanç=1): onset türü = ilk 1 sn enerji, sustain türü = nota ortası
REF = dict(lute=-24.0, harp=-25.0, organ=-27.0, bowed=-26.0, choir=-27.0,
           dum=-22.0, tek=-27.0, ka=-29.0, tef=-31.0, timp=-20.0, gong=-23.0, bell=-25.0, sub=-22.0)

def _level(y, ref_db, mode="onset"):
    """Notayı algısal-enerji referansına oturtur: 'onset' = vuruşun ilk 1 sn'sinin RMS'i (kısa sesler sıfır doldurulur),
    'sustain' = notanın ortası (%35–65). Böylece farklı çalgılar eşit kazançta dengeli duyulur."""
    n = len(y)
    if mode == "onset":
        k = SR
        r = np.sqrt(np.sum(y[:k] ** 2) / k)
    else:
        a, b = int(0.35 * n), max(int(0.65 * n), int(0.35 * n) + 64)
        r = np.sqrt(np.mean(y[a:b] ** 2))
    return y * (D.db2lin(ref_db) / (r + 1e-12))


def lute_note(f0, vel, rng, ring=1.0, double=True):
    """Lavta: Karplus–Strong, çift kurs (hafif detune), sert vuruşta parlak, yumuşakta mat."""
    t60 = float(np.clip(3.4 * (220.0 / f0) ** 0.6 * ring, 1.0, 5.4))
    dur = min(t60 * 0.8, 4.2)
    bright = 0.22 + 0.38 * vel
    y = D.ks_string(f0, dur, rng, S=0.5, t60=t60, bright=bright, pick=0.12 + 0.12 * rng.random(), damp=0.30, vel=1.0)
    if double and f0 > 150:
        f2 = f0 * 2 ** (rng.choice([-1.0, 1.0]) * rng.uniform(0.8, 2.4) / 1200)
        y = y + 0.6 * D.ks_string(f2, dur, rng, S=0.5, t60=t60, bright=bright, pick=0.15 + 0.1 * rng.random(), damp=0.30, vel=1.0)
    y = D.fade_edges(y, 0.0004, 0.05)
    return _level(y, REF["lute"] + 12 * (vel - 0.7))


def harpsichord_note(f0, vel, rng):
    """Klavsen benzeri: parlak, kısa sönümlü KS teli (8' + hafif 4'), 'jack' tıkırtısı."""
    t60 = float(np.clip(1.9 * (262.0 / f0) ** 0.5, 0.6, 3.0))
    dur = min(t60 * 0.85, 2.4)
    y = D.ks_string(f0, dur, rng, S=0.36, t60=t60, bright=0.95, pick=0.10 + 0.04 * rng.random(), damp=0.0, vel=1.0)
    y += 0.55 * D.ks_string(f0 * 2.0007, dur, rng, S=0.36, t60=t60 * 0.7, bright=0.95, pick=0.1, damp=0.0, vel=1.0)
    y += 0.35 * D.ks_string(f0 * 0.9993, dur, rng, S=0.36, t60=t60, bright=0.9, pick=0.13, damp=0.0, vel=1.0)
    t = np.arange(len(y)) / SR
    y += 0.35 * D.hp(rng.standard_normal(len(y)), 2500, 2) * np.exp(-t / 0.004)
    y = D.lp(y, 7500, 2)
    y = D.fade_edges(y, 0.0003, 0.04)
    return _level(y, REF["harp"] + 12 * (vel - 0.7))


def _organ_amp(f0, kind):
    if kind == "flute":       # 8' flüt: zayıf üst harmonikler
        return lambda f: (f0 / f) ** 2.1
    if kind == "principal":   # prensipal: parlak ama yumuşak
        return lambda f: (f0 / f) ** 1.15 / (1 + (f / 4200.0) ** 4)
    if kind == "reed":        # regal / dilli: kalın, burunsu, formantlı
        return lambda f: (f0 / f) ** 0.95 * (1 + 1.2 * np.exp(-((f - 1300.0) / 500.0) ** 2)) / (1 + (f / 3800.0) ** 4)
    return lambda f: (f0 / f) ** 1.5


LO_SR = 16000          # pedler (org/koro/yaylı) düşük örnek hızında üretilir (≤7 kHz içerik) → ~3× hızlı; sonra 48 kHz'e yükseltilir
UP = SR // LO_SR


def _up(y):
    return D.resample_poly(y, UP, 1)


def organ_note(f0, dur, vel, rng, stops=(("flute", 1.0, 1.0), ("principal", 0.45, 1.0), ("flute", 0.3, 2.0)),
               attack=0.06, release=0.35, trem=True, chiff=0.5):
    """Portatif org / regal: seçilen 'perdeler' (tür, seviye, oktav çarpanı) toplanır; chiff + hafif tremulant."""
    n = int(round(dur * LO_SR))
    y = np.zeros(n)
    for kind, lvl, mult in stops:
        ff = f0 * mult
        if ff > 6500:
            continue
        tab = D.additive_table(ff, _organ_amp(ff, kind), rng, phase="random", max_hz=7000, sr=LO_SR)
        y += lvl * D.wt_osc(tab, ff * (1 + rng.uniform(-0.0004, 0.0004)), n, phase0=rng.random(), sr=LO_SR)
    t = np.arange(n) / LO_SR
    if trem:
        y *= 1 + 0.025 * np.sin(D.PI2 * 4.3 * t + rng.uniform(0, 6.28))
    env = D.adsr(n, attack, 0.15, 0.9, release, sr=LO_SR)
    y *= env
    if chiff > 0:
        ch = D.bp(rng.standard_normal(n), 1400, 4200, 2, sr=LO_SR) * np.exp(-t / 0.03) * (1 - np.exp(-t / 0.004))
        y += chiff * 0.25 * ch * np.max(np.abs(y)) / (np.max(np.abs(ch)) + 1e-9)
    return _level(_up(y), REF["organ"] + 12 * (vel - 0.7), "sustain")


def _cello_amp(f0):
    g = lambda f, c, w: np.exp(-((f - c) / w) ** 2)
    return lambda f: (f0 / f) ** 0.95 * (1 + 1.3 * g(f, 260, 90) + 1.0 * g(f, 480, 130) + 0.7 * g(f, 1000, 260)) / (1 + (f / 3000.0) ** 2)


def bowed_note(f0, dur, vel, rng, attack=0.35, release=0.9, ens=2, vib=(5.1, 6.5), swell=0.08, bright=0.65):
    """Yaylı drone / çello: testere benzeri tablo × gövde rezonansları, gecikmeli vibrato, yay gürültüsü, yavaş yay baskısı dalgası."""
    n = int(round(dur * LO_SR))
    amp = _cello_amp(f0)
    if bright != 1.0:
        amp = (lambda a: (lambda f: a(f) / (1 + ((f / 1800.0) ** 2) * (1 / bright - 1) * 3)))(amp)
    tab = D.additive_table(f0, amp, rng, phase="saw", max_hz=7000, sr=LO_SR)
    y = np.zeros(n)
    for k in range(ens):
        cents = (k - (ens - 1) / 2) * 3.6 + rng.uniform(-0.8, 0.8)
        vb = D.vibrato(n, vib[0] * rng.uniform(0.94, 1.06), vib[1] * rng.uniform(0.7, 1.1), delay=0.45 + 0.2 * rng.random(), rise=1.2, rng=rng, sr=LO_SR)
        y += D.wt_osc(tab, f0 * 2 ** (cents / 1200) * vb, n, phase0=rng.random(), sr=LO_SR)
    y /= ens
    t = np.arange(n) / LO_SR
    bn = D.bp(rng.standard_normal(n), 700, 3800, 2, sr=LO_SR)
    y = y + 0.05 * bn * (0.4 + 0.6 * (1 - np.exp(-t / 0.2))) * np.max(np.abs(y)) / (np.max(np.abs(bn)) + 1e-9)
    lfo = 1 + swell * np.sin(D.PI2 * rng.uniform(0.11, 0.2) * t + rng.uniform(0, 6.28))
    y *= D.adsr(n, attack, 0.2, 0.92, release, sr=LO_SR) * lfo
    return _level(_up(y), REF["bowed"] + 12 * (vel - 0.7), "sustain")


VOWELS = {
    "a": [(780, 110, 0), (1150, 130, -7), (2800, 200, -22)],
    "o": [(450, 90, 0), (830, 110, -9), (2650, 200, -24)],
    "u": [(330, 80, 0), (720, 100, -14), (2500, 200, -30)],
    "e": [(420, 90, 0), (1750, 150, -12), (2600, 200, -22)],
}


def _vowel_amp(f0, vowel, shift=1.0):
    fm = VOWELS[vowel]

    def amp(f):
        s = np.full_like(f, 0.04, dtype=np.float64)
        for (F, bw, db) in fm:
            s = s + D.db2lin(db) / (1 + ((f - F * shift) / bw) ** 2)
        return s * (f0 / f) ** 0.7 / (1 + (f / 6000.0) ** 4)
    return amp


def choir_note(f0, dur, vel, rng, vowel="o", vowel2=None, morph=(0.3, 0.8), voices=3, attack=1.4, release=2.2, shift=1.0):
    """Koro pedi: formant (ünlü) şekilli tablo, 'voices' adet detune/vibratolu ses, nefes gürültüsü; ünlü morf (ör. o→a)."""
    n = int(round(dur * LO_SR))
    t = np.arange(n) / LO_SR
    tab1 = D.additive_table(f0, _vowel_amp(f0, vowel, shift), rng, phase="random", max_hz=7000, sr=LO_SR)
    tab2 = D.additive_table(f0, _vowel_amp(f0, vowel2, shift), rng, phase="random", max_hz=7000, sr=LO_SR) if vowel2 else None
    ya, yb = np.zeros(n), np.zeros(n)
    for k in range(voices):
        cents = (k - (voices - 1) / 2) * 11.0 + rng.uniform(-3, 3)
        vb = D.vibrato(n, rng.uniform(4.8, 5.9), rng.uniform(10, 22), delay=0.7 + 0.6 * rng.random(), rise=1.5, rng=rng, sr=LO_SR)
        ff = f0 * 2 ** (cents / 1200) * vb
        ph0 = rng.random()
        ya += D.wt_osc(tab1, ff, n, phase0=ph0, sr=LO_SR)
        if tab2 is not None:
            yb += D.wt_osc(tab2, ff, n, phase0=ph0, sr=LO_SR)
    if tab2 is not None:
        a, b = morph
        w = D.smoothstep((t - a * dur) / max((b - a) * dur, 1e-3))
        y = ya * (1 - w) + yb * w
    else:
        y = ya
    y /= voices
    vf = VOWELS[vowel]
    br = D.resonator(rng.standard_normal(n), vf[0][0], 220, sr=LO_SR) + 0.6 * D.resonator(rng.standard_normal(n), vf[1][0], 260, sr=LO_SR)
    y = y + 0.05 * br * np.max(np.abs(y)) / (np.max(np.abs(br)) + 1e-9)
    y *= D.adsr(n, attack, 0.5, 0.92, release, sr=LO_SR)
    return _level(_up(y), REF["choir"] + 12 * (vel - 0.7), "sustain")


def drum(kind, f, vel, rng):
    return _level(D.drum_hit(kind, f, 1.0, rng), REF[kind] + 18 * (vel - 0.7))


def tef(vel, rng):
    return _level(D.tef_hit(1.0, rng), REF["tef"] + 18 * (vel - 0.7))


def timp(f, vel, rng, dur=2.4):
    return _level(D.timpani_hit(f, 1.0, rng, dur=dur), REF["timp"] + 18 * (vel - 0.7))


def gong(f0, dur, vel, rng, bloom=1.0):
    return _level(D.gong_tone(f0, dur, 1.0, rng, bloom=bloom), REF["gong"] + 18 * (vel - 0.7))


def bell(f, dur, vel, rng, ring=1.0, strike=0.5):
    return _level(D.bell_tone(f, dur, 1.0, rng, ring=ring, strike=strike), REF["bell"] + 18 * (vel - 0.7))


def sub(f0, f1, dur, vel):
    return _level(D.sub_boom(f0, f1, dur, 1.0), REF["sub"] + 18 * (vel - 0.7))


# ═══════════════════════════ çalgı katmanı: son süzgeç + reverb gönderimi ═══════════════════════════
def _sos(bands):
    return np.concatenate([D.biquad(k, f, g, q) for (k, f, g, q) in bands], axis=0)


LAYER_FX = {
    "lute": dict(sos=_sos([("peak", 130, 3.0, 1.0), ("peak", 300, 2.0, 1.2), ("lp", 5200, 0, 0.7)]), send=0.50),
    "harp": dict(sos=_sos([("hp", 140, 0, 0.7), ("lp", 7000, 0, 0.7)]), send=0.50),
    "organ": dict(sos=_sos([("hp", 60, 0, 0.7), ("lp", 4800, 0, 0.7)]), send=0.58),
    "choir": dict(sos=_sos([("hp", 90, 0, 0.7), ("lp", 5200, 0, 0.7)]), send=0.66),
    "drone": dict(sos=_sos([("hp", 32, 0, 0.7), ("lp", 3200, 0, 0.7)]), send=0.38),
    "perc": dict(sos=_sos([("hp", 32, 0, 0.7)]), send=0.32),
    "bell": dict(sos=_sos([("hp", 80, 0, 0.7)]), send=0.66),
    "fx": dict(sos=None, send=0.62),
}


def _hz(m):
    return float(D.midi_hz(m))


# ═══════════════════════════ cue bağlamı ═══════════════════════════
class Cue:
    """Bir bölümün müzik cue'su: ritim ızgarası, akor çizelgesi, yoğunluk eğrisi ve ses tamponları."""

    def __init__(self, cid, spec, T, t0c, t1c, open_sec, close_sec, seed=0):
        self.cid, self.spec, self.T, self.t0c, self.t1c = cid, spec, float(T), float(t0c), float(t1c)
        self.rng = rng_for("cue", cid, seed)
        self.n = int(round(T * SR))
        self.tonic, self.mode = spec["tonic"], spec["mode"]
        self.meter = spec["meter"]
        self.beat = 60.0 / spec["bpm"]
        if self.meter == "4/4":
            self.spb, self.bar = 8, 4 * self.beat
        elif self.meter == "3/4":
            self.spb, self.bar = 6, 3 * self.beat
        else:  # 6/8: 'vuruş' = noktalı dörtlük
            self.spb, self.bar = 6, 2 * self.beat
        self.step = self.bar / self.spb
        self.arc = np.array(spec["arc"], dtype=np.float64)
        self.open_sec, self.close_sec = open_sec, close_sec
        self.t_open, self.t_close = open_sec, T - close_sec
        self.dry = np.zeros((self.n, 2), dtype=np.float32)
        self.send = np.zeros(self.n, dtype=np.float32)
        self.diag = {}   # katman → saniye başına enerji (yalnız ayar/teşhis için)
        self.note_log = None   # teşhis: [(katman, t, midi, süre)] — layer_melody doldurur
        self.chords = self._build_chords()

    # --- zaman / yoğunluk
    def u(self, t):
        return (t - self.t0c) / max(self.t1c - self.t0c, 1e-6)

    def I(self, t):
        return float(np.interp(self.u(t), self.arc[:, 0], self.arc[:, 1]))

    # --- akor çizelgesi: (t0, t1, derece, ek)
    def _build_chords(self):
        progs = self.spec["prog"]
        nb = int(np.ceil(self.T / self.bar))
        nb_open = max(1, int(np.ceil(self.open_sec / self.bar)))
        nb_close = max(1, int(np.ceil(self.close_sec / self.bar)))
        lim = max(nb - nb_close, nb_open)
        ch = [(0.0, nb_open * self.bar, 0, "5")]
        b = nb_open
        while b < lim:
            use_b = len(progs) > 1 and self.I(b * self.bar) >= self.spec.get("b_thr", 0.7)
            for (deg, k, ext) in (progs[1] if use_b else progs[0]):
                if b >= lim:
                    break
                k = min(k, lim - b)
                ch.append((b * self.bar, (b + k) * self.bar, deg, ext))
                b += k
        ch.append((b * self.bar, self.T + 30.0, 0, "5"))
        return ch

    def chord_at(self, t):
        for c in self.chords:
            if c[0] <= t < c[1]:
                return c
        return self.chords[-1]

    # --- tampon
    def put(self, layer, sig, t, gain=1.0, pan=0.0, send=None):
        fx = LAYER_FX[layer]
        if fx["sos"] is not None:
            sig = D.sosfilt(fx["sos"], sig)
        i = int(round(t * SR))
        if i >= self.n or i + len(sig) <= 0:
            return
        if i < 0:
            sig, i = sig[-i:], 0
        m = min(len(sig), self.n - i)
        s = sig[:m] * gain
        self._diag(layer, s, i)
        gl, gr = D.pan_gains(pan)
        self.dry[i:i + m, 0] += (s * gl).astype(np.float32)
        self.dry[i:i + m, 1] += (s * gr).astype(np.float32)
        self.send[i:i + m] += (s * (fx["send"] if send is None else send)).astype(np.float32)

    def _diag(self, layer, s, i):
        e = s * s
        first = i // SR
        edges = np.arange(first + 1, (i + len(s)) // SR + 1) * SR - i
        edges = edges[(edges > 0) & (edges < len(s))]
        idx = np.concatenate([[0], edges]).astype(np.int64)
        sums = np.add.reduceat(e, idx)
        d = self.diag.setdefault(layer, np.zeros(int(self.T) + 40))
        bins = first + np.arange(len(idx))
        ok = bins < len(d)
        d[bins[ok]] += sums[ok]

    def layer_report(self, a=0.0, b=None):
        """Katman başına [a,b) sn aralığında güç ortalaması (dBFS) — dengeyi ölçmek için."""
        b = b or self.T
        out = {}
        for k, d in self.diag.items():
            seg = d[int(a):int(b)]
            out[k] = round(float(10 * np.log10(np.sum(seg) / max(b - a, 1) / SR + 1e-18)), 1)
        return out

    def act(self, cfg, t):
        """Katman etkinliği 0..lvl: yoğunluk eşikleri (lo,hi), kesilme (cut) ve u-pencereleri (win)."""
        I = self.I(t)
        lo, hi = cfg.get("lo", -1.0), cfg.get("hi", -0.5)
        a = float(D.smoothstep((I - lo) / max(hi - lo, 1e-6)))
        cut = cfg.get("cut")
        if cut:
            a *= 1.0 - float(D.smoothstep((I - cut[0]) / max(cut[1] - cut[0], 1e-6)))
        win = cfg.get("win")
        if win:
            u = self.u(t)
            if not any(w0 <= u < w1 for (w0, w1) in win):
                return 0.0
        return a * cfg.get("lvl", 1.0)


# ═══════════════════════════ akor dizilimleri ═══════════════════════════
def voice_pad(c, deg, ext, prev, nv=4):
    """Koro/org pedi için yumuşak ses yürütmeli dizilim: bas kökte, üst sesler önceki notaya en yakın akor sesi."""
    degs = chord_degs(deg, ext)
    pcs = {deg_midi(c.tonic, c.mode, d) % 12 for d in degs}
    root_pc = deg_midi(c.tonic, c.mode, deg) % 12
    ranges = [(40, 55), (50, 62), (57, 69), (62, 76), (66, 79)][:nv]
    out = []
    for v, (lo, hi) in enumerate(ranges):
        cand = [m for m in range(lo, hi + 1) if m % 12 in pcs and (v > 0 or m % 12 == root_pc)]
        cand = [m for m in cand if m not in out] or cand
        tgt = prev[v] if prev is not None and v < len(prev) else (lo + hi) / 2 + (v - 1.5) * 1.0
        out.append(min(cand, key=lambda m: (abs(m - tgt), m)))
    # kök+beşli/üçlü eksikse bir ses ekle (açık beşli hariç)
    return out


def lute_voic(c, deg, ext, low=45):
    """Lavta için açık dizilim: [kök, beşli, kök+8, üçlü+8, beşli+8] (üçlü yoksa kök/beşli çiftleri)."""
    r = deg_midi(c.tonic, c.mode, deg)
    while r < low:
        r += 12
    while r >= low + 12:
        r -= 12
    f = r + (deg_midi(c.tonic, c.mode, deg + 4) - deg_midi(c.tonic, c.mode, deg))
    if ext in ("5",):
        return [r, f, r + 12, f + 12, r + 24]
    th = r + (deg_midi(c.tonic, c.mode, deg + (1 if ext == "sus2" else 3 if ext == "sus4" else 2)) - deg_midi(c.tonic, c.mode, deg))
    return [r, f, r + 12, th + 12, f + 12]


def deg_for_midi(c, m):
    return min(range(-14, 50), key=lambda d: abs(deg_midi(c.tonic, c.mode, d) - m))


# ═══════════════════════════ ritim kalıpları ═══════════════════════════
ARP = {
    "4/4": {"broken": [0, 1, 2, 3, 2, 1, 2, 1], "alberti": [0, 2, 1, 2, 0, 2, 1, 2], "ostinato": [0, 3, 2, 3, 1, 3, 2, 3],
            "sparse": [0, None, None, 2, None, 1, None, None], "pavane": [0, None, 2, None, 1, None, 2, None],
            "pulse": [0, None, 1, None, 0, None, 1, None], "roll": [0, 1, 2, 3, 4, 3, 2, 1],
            "tick": [0, 4, 0, 4, 0, 4, 0, 4]},
    "6/8": {"lilt": [0, 1, 2, 1, 2, 1], "gigue": [0, None, 2, 1, None, 2], "roll": [0, 1, 2, 3, 2, 1],
            "sparse": [0, None, None, 2, None, 1], "sea": [0, 1, 2, 3, 4, 3]},
    "3/4": {"waltz": [0, None, 1, 2, 1, 2], "sarab": [0, None, None, 2, None, 1], "roll": [0, 1, 2, 3, 2, 1],
            "sparse": [0, None, 1, None, 2, None], "lull": [0, 2, 1, 3, 1, 2]},
}
ACC = {"4/4": [1.0, .55, .78, .55, .92, .55, .75, .55], "6/8": [1.0, .5, .62, .92, .5, .62], "3/4": [1.0, .5, .78, .5, .78, .5]}

BASS = {
    "4/4": {"root13": [(0, "r"), (4, "f")], "drive": [(0, "r"), (1, "r"), (2, "o"), (3, "r"), (4, "f"), (5, "r"), (6, "o"), (7, "r")],
            "p332": [(0, "r"), (3, "r"), (6, "r")], "whole": [(0, "r")], "walk": [(0, "r"), (2, "f"), (4, "r"), (6, "o")],
            "tick": [(0, "r"), (2, "r"), (4, "r"), (6, "r")]},
    "6/8": {"lilt": [(0, "r"), (3, "f")], "drive": [(0, "r"), (2, "r"), (3, "f"), (5, "r")], "whole": [(0, "r")]},
    "3/4": {"waltz": [(0, "r")], "sarab": [(0, "r"), (4, "f")], "whole": [(0, "r")]},
}

PERC = {
    "4/4": {"heartbeat": "D..d....", "proc": "D.......", "proc2": "D...T...", "march": "D.t.D.t.", "drive": "DtTtDtTt",
            "p332": "D..T..D.", "dun": "D..tD.T.", "duyek": "D.TtD.T.", "none": "........"},
    "6/8": {"lilt": "D.T.t.", "gallop": "D.TD.T", "sea": "D..t..", "heart": "D.d...", "none": "......"},
    "3/4": {"sarab": "D..T.t", "light": "D....t", "proc3": "D.....", "none": "......"},
}
TEF = {
    "4/4": {"eighths": "x.yyx.yy", "sparse": "..y...y.", "drive": "xyxyxyxy"},
    "6/8": {"lilt": "x.yx.y", "sparse": "..y..y"},
    "3/4": {"light": "..y.y.", "sarab": "x.y.y."},
}

MOTIFS = {  # (derece farkı, vuruş-ızgarası uzunluğu [sekizlik]) — özgün, alçalan/çıkan figürler
    "bruksel": [(4, 4), (3, 2), (2, 2), (0, 8)],
    "merak": [(0, 1), (2, 1), (1, 1), (4, 3)],
    "sorgu": [(0, 2), (2, 2), (4, 2), (3, 2)],
    "agit": [(4, 3), (3, 1), (2, 2), (1, 2), (0, 4)],
    "yuruyus": [(0, 2), (0, 1), (2, 1), (1, 2), (0, 2)],
}


# ═══════════════════════════ katman üreticileri ═══════════════════════════
def layer_drone(c, cfg):
    mode = cfg.get("mode", "pedal")
    chunk = cfg.get("chunk_bars", 4) * c.bar
    t = 0.0
    while t < c.T - 0.3:
        L = min(chunk, c.T - t)
        tm = t + L / 2
        g = cfg["lvl"] * (0.5 + 0.5 * c.I(tm))
        if mode == "pedal":
            root = c.tonic
        else:
            root = deg_midi(c.tonic, c.mode, c.chord_at(t + 0.1)[2])
            while root > c.tonic + 9:
                root -= 12
            while root < c.tonic - 5:
                root += 12
        notes = [(root, 1.0, -0.12)]
        if cfg.get("fifth", True):
            notes.append((root + 7, 0.62, 0.14))
        for (m, gm, pan) in notes:
            y = bowed_note(_hz(m), L + 3.0, 0.7, c.rng, attack=1.6, release=2.2, bright=cfg.get("bright", 0.6))
            c.put("drone", y, t - 0.2, gain=g * gm, pan=pan)
        t += L


def layer_pad(c, cfg):
    prev = None
    nv = cfg.get("voices", 4)
    pans = [-0.1, -0.35, 0.3, 0.1, 0.45][:nv]
    for (t0, t1, deg, ext) in c.chords:
        if t0 >= c.T:
            break
        vo = voice_pad(c, deg, ext, prev, nv)
        prev = vo
        tm = (t0 + min(t1, c.T)) / 2
        a = c.act(cfg, tm)
        if a <= 0.015:
            continue
        dur = min(t1, c.T) - t0 + 2.8
        I = c.I(tm)
        for k, m in enumerate(vo):
            st = t0 - 0.5 + k * 0.10 + c.rng.uniform(0, 0.15)
            if cfg["inst"] == "choir":
                v1, v2 = cfg.get("vowel", ("o", "a"))
                y = choir_note(_hz(m), dur, 0.5 + 0.4 * I, c.rng, vowel=v1, vowel2=v2, voices=cfg.get("nvox", 3),
                               morph=(0.2, 0.75), attack=1.5, release=2.4, shift=cfg.get("shift", 1.0))
                c.put("choir", y, st, gain=a * (0.8 if k == 0 else 1.0), pan=pans[k])
            else:
                stops = cfg.get("stops", (("flute", 1.0, 1.0), ("principal", 0.4, 1.0), ("flute", 0.3, 2.0)))
                y = organ_note(_hz(m), dur, 0.5 + 0.4 * I, c.rng, stops=stops, attack=cfg.get("attack", 0.5), release=1.6)
                c.put("organ", y, st, gain=a * (0.8 if k == 0 else 1.0), pan=pans[k])


def layer_arp(c, cfg):
    pat = ARP[c.meter][cfg["pattern"]]
    acc = ACC[c.meter]
    layer = cfg.get("inst", "lute")
    b0 = int(np.ceil(c.t_open / c.bar))
    b1 = int(c.t_close / c.bar)
    for b in range(b0, b1):
        tb = b * c.bar
        a = c.act(cfg, tb + c.bar / 2)
        if a < 0.03:
            continue
        _, _, deg, ext = c.chord_at(tb + 0.01)
        vc = lute_voic(c, deg, ext, cfg.get("low", 45))
        I = c.I(tb)
        dens = cfg.get("p0", 0.6) + cfg.get("p1", 0.35) * I
        for s, idx in enumerate(pat):
            if idx is None or (s > 0 and c.rng.random() > dens):
                continue
            t = tb + s * c.step + c.rng.normal(0, 0.005)
            m = vc[idx % len(vc)] + cfg.get("transpose", 0)
            vel = float(np.clip(acc[s] * (0.5 + 0.5 * I) * c.rng.uniform(0.9, 1.08), 0.15, 1.0))
            f = _hz(m)
            y = lute_note(f, vel, c.rng) if layer == "lute" else harpsichord_note(f, vel, c.rng)
            pan = float(np.clip(-0.35 + (m - 45) / 42.0, -0.4, 0.55))
            c.put(layer, y, t, gain=a, pan=pan)
        if cfg.get("strum") and b % cfg["strum"] == 0 and I > 0.2:
            for j, idx in enumerate([0, 1, 2, 3]):
                m = vc[idx] + cfg.get("transpose", 0)
                c.put(layer, lute_note(_hz(m), 0.55, c.rng) if layer == "lute" else harpsichord_note(_hz(m), 0.55, c.rng),
                      tb + 0.02 * j, gain=a * 0.7, pan=-0.1 + 0.07 * j)


def _rhythm(c, nsteps, density, rng):
    """nsteps sekizliklik alanı, yoğunluğa bağlı nota süreleriyle doldurur (vuruşa yaslanma kurallı)."""
    out, p = [], 0
    while p < nsteps:
        left = nsteps - p
        opts = [(1, 0.6 * density ** 1.3 + 0.05), (2, 1.0), (3, 0.5 * (1 - density) + 0.2), (4, 0.9 * (1 - density) + 0.15),
                (6, 0.5 * (1 - density) ** 2), (8, 0.4 * (1 - density) ** 2.5)]
        w = []
        for d, wt in opts:
            if d > left:
                ok = False
            elif d in (1, 3):
                ok = True
            elif d in (2, 4, 6):
                ok = p % 2 == 0
            else:  # 8: yalnız ölçü başında
                ok = p % c.spb == 0 and c.spb == 8
            if d == 6 and c.spb == 6:
                ok = ok and p % 6 == 0
            w.append(wt if ok else 0.0)
        if sum(w) <= 0:
            d = 1
        else:
            d = opts[int(rng.choice(len(opts), p=np.array(w) / sum(w)))][0]
        out.append(d)
        p += d
    return out


def layer_melody(c, cfg):
    """Cümle (phrase) kurucu: ritim hücreleri → perde yürüyüşü (akor sesine yaslanan güçlü vuruşlar, cümle sonunda akor sesi).
    'motif': her cümlenin başında özgün figür; akor sesine göre kaydırılır, bazen ters çevrilir, kalanı yürüyüşle sürer."""
    inst = cfg.get("inst", "lute")
    play, rest = cfg.get("play", 2), cfg.get("rest", 2)
    lo_m, hi_m = cfg.get("reg", (60, 76))
    center = deg_for_midi(c, (lo_m + hi_m) // 2)
    dlo, dhi = deg_for_midi(c, lo_m), deg_for_midi(c, hi_m)
    motif = MOTIFS.get(cfg.get("motif"), None)
    b0 = int(np.ceil(c.t_open / c.bar))
    b1 = int(c.t_close / c.bar)
    ready = b0
    b = b0
    while b < b1:
        tb = b * c.bar
        a = c.act(cfg, tb + c.bar)
        if b < ready or a < 0.03 or c.rng.random() > cfg.get("prob", 0.9):
            b += 1
            continue
        nb = min(play, b1 - b)
        ready = b + play + rest
        nsteps = nb * c.spb
        I = c.I(tb)
        dens = float(np.clip(cfg.get("dens", 0.4) + 0.4 * (I - 0.4), 0.05, 0.95))
        durs = _rhythm(c, nsteps, dens, c.rng)
        # motif tohumu
        mot = None
        if motif and c.rng.random() < cfg.get("motif_p", 0.75) and len(durs) >= 3:
            _, _, deg0, ext0 = c.chord_at(tb + 0.01)
            tones0 = {(deg0 + k) % 7 for k in CHORD_EXT[ext0]}
            base_c = [x for x in range(dlo, dhi + 1) if x % 7 in tones0] or [center]
            var = str(c.rng.choice(["same", "same", "inv", "up", "down"]))
            shift = {"same": 0, "inv": 0, "up": 1, "down": -1}[var] + int(c.rng.integers(-1, 2))
            base = min(base_c, key=lambda x: (abs(x - (center + shift)), x))
            offs = [o for o, _ in motif]
            if var == "inv":
                offs = [-o for o in offs]
            mot = [int(np.clip(base + o - offs[0], dlo, dhi)) for o in offs]
        notes, cur, pos = [], None, 0
        for i, d in enumerate(durs):
            t = tb + pos * c.step
            _, _, deg, ext = c.chord_at(t + 0.01)
            tones = {deg_midi(c.tonic, c.mode, x) % 12 for x in chord_degs(deg, ext)}
            is_strong = pos % (c.spb // 2) == 0
            last = i == len(durs) - 1
            if mot is not None and i < len(mot):
                cur = mot[i]
            elif cur is None:
                cur = int(c.rng.integers(center - 2, center + 3))
            else:
                step = int(c.rng.choice([-3, -2, -1, 0, 1, 2, 3], p=[0.05, 0.14, 0.31, 0.06, 0.28, 0.12, 0.04]))
                pull = (center - cur) / 6.0
                if c.rng.random() < abs(pull):
                    step = int(np.sign(pull)) * max(1, abs(step))
                cur = int(np.clip(cur + step, dlo, dhi))
            if (is_strong or last) and not (mot is not None and i < len(mot)):
                cand = [x for x in range(max(dlo, cur - 3), min(dhi, cur + 3) + 1) if deg_midi(c.tonic, c.mode, x) % 12 in tones]
                if cand:
                    cur = min(cand, key=lambda x: (abs(x - cur), x))
            notes.append((t, cur, d))
            pos += d
        for (t, dg, d) in notes:
            m = deg_midi(c.tonic, c.mode, dg)
            if c.note_log is not None:
                c.note_log.append(("mel", round(t, 2), m, d))
            vel = float(np.clip((0.45 + 0.5 * I) * c.rng.uniform(0.9, 1.1), 0.2, 1.0))
            f = _hz(m)
            if inst == "lute":
                y, lay = lute_note(f, vel, c.rng), "lute"
            elif inst == "harp":
                y, lay = harpsichord_note(f, vel, c.rng), "harp"
            elif inst == "organ":
                y, lay = organ_note(f, max(d * c.step * 1.05, 0.6) + 0.6, vel, c.rng, stops=(("flute", 1.0, 1.0), ("principal", 0.25, 1.0)), attack=0.08, release=0.5), "organ"
            else:
                y, lay = bowed_note(f, max(d * c.step * 1.1, 0.8) + 0.8, vel, c.rng, attack=0.18, release=0.5, ens=2, bright=0.8), "drone"
            c.put(lay, y, t + c.rng.normal(0, 0.006), gain=a, pan=float(np.clip(0.05 + (m - 66) / 60.0, -0.3, 0.5)))
        b += play


def layer_bass(c, cfg):
    pat = BASS[c.meter][cfg["pattern"]]
    b0 = int(np.ceil(c.t_open / c.bar))
    b1 = int(c.t_close / c.bar)
    for b in range(b0, b1):
        tb = b * c.bar
        a = c.act(cfg, tb + c.bar / 2)
        if a < 0.03:
            continue
        _, _, deg, ext = c.chord_at(tb + 0.01)
        r = deg_midi(c.tonic, c.mode, deg)
        while r > c.tonic + 9:
            r -= 12
        while r < c.tonic - 5:
            r += 12
        I = c.I(tb)
        for (s, w) in pat:
            if s > 0 and c.rng.random() > cfg.get("p", 0.9):
                continue
            m = r + {"r": 0, "f": 7, "o": 12}[w] + cfg.get("transpose", 0)
            vel = float(np.clip(ACC[c.meter][s] * (0.55 + 0.45 * I) * c.rng.uniform(0.9, 1.05), 0.2, 1.0))
            if cfg.get("inst", "lute") == "lute":
                y = lute_note(_hz(m), vel, c.rng, ring=0.7, double=False)
                c.put("lute", y, tb + s * c.step + c.rng.normal(0, 0.004), gain=a, pan=-0.12)
            else:
                y = bowed_note(_hz(m), c.step * 1.5 + 0.4, vel, c.rng, attack=0.04, release=0.25, ens=1, bright=0.9)
                c.put("drone", y, tb + s * c.step, gain=a, pan=-0.1)


_DRUM_VEL = {"D": 1.0, "d": 0.55, "T": 0.9, "t": 0.5, "k": 0.6}


def layer_perc(c, cfg):
    pat = PERC[c.meter][cfg["pattern"]]
    tef_pat = TEF[c.meter].get(cfg.get("tef")) if cfg.get("tef") else None
    f0 = cfg.get("pitch", 98.0)
    b0 = int(np.ceil(c.t_open / c.bar))
    b1 = int(c.t_close / c.bar)
    for b in range(b0, b1):
        tb = b * c.bar
        a = c.act(cfg, tb + c.bar / 2)
        if a < 0.03:
            continue
        I = c.I(tb)
        for s, ch in enumerate(pat):
            if ch == ".":
                continue
            if s > 0 and c.rng.random() > cfg.get("p", 0.95):
                continue
            t = tb + s * c.step + c.rng.normal(0, 0.003)
            vel = _DRUM_VEL[ch] * (0.5 + 0.5 * I) * c.rng.uniform(0.9, 1.05)
            kind = "dum" if ch in "Dd" else ("tek" if ch in "Tt" else "ka")
            y = drum(kind, f0 * (c.rng.uniform(0.97, 1.03)), vel, c.rng)
            c.put("perc", y, t, gain=a * cfg.get("amp", 0.55), pan={"dum": 0.0, "tek": 0.3, "ka": -0.25}[kind])
        if tef_pat:
            for s, ch in enumerate(tef_pat):
                if ch == ".":
                    continue
                t = tb + s * c.step + c.rng.normal(0, 0.004)
                y = tef((1.0 if ch == "x" else 0.6) * (0.4 + 0.6 * I), c.rng)
                c.put("perc", y, t, gain=a * cfg.get("tef_amp", 0.30), pan=0.4)
        if cfg.get("fill") and b % cfg["fill"] == cfg["fill"] - 1 and I > 0.45:
            for j in range(4):
                t = tb + c.bar - (4 - j) * c.step / 2
                y = drum("tek" if j % 2 else "dum", f0, 0.45 + 0.12 * j, c.rng)
                c.put("perc", y, t, gain=a * cfg.get("amp", 0.55), pan=0.15)


def layer_bell(c, cfg):
    b0 = int(np.ceil(c.t_open / c.bar))
    b1 = int(c.t_close / c.bar)
    per, off = cfg.get("period", 4), cfg.get("offset", 0)
    for b in range(b0, b1):
        if (b - off) % per:
            continue
        tb = b * c.bar
        a = c.act(cfg, tb)
        if a < 0.03:
            continue
        m = cfg.get("midi", 62)
        if cfg.get("alt"):
            m += cfg["alt"][((b - off) // per) % len(cfg["alt"])]
        y = bell(_hz(m), cfg.get("dur", 6.5), 0.7, c.rng, ring=cfg.get("ring", 1.0), strike=0.5)
        c.put("bell", y, tb + c.rng.normal(0, 0.01), gain=a, pan=float(c.rng.uniform(-0.4, 0.4)))


# ═══════════════════════════ cue tanımları (bölüm ruh hali → müzik) ═══════════════════════════
# tonic: ana ses MIDI (bas yazmacı); arc: (u, yoğunluk) — u=0 bölüm başı, u=1 bölüm sonu; prog: [(derece, ölçü, ek)]
# Katmanlar: drone, choir (koro/org pedi), arp (lavta/klavsen arpej), arp2, bass, melody, perc, bell.
CUES = {
    # c0: soğuk açılış — gizemli, ağırbaşlı; gerilim yükselir, başlık anında tek vuruş + altın D majör (finale_c0)
    "c0": dict(mood="solemn", tonic=38, mode="dorian", bpm=58, meter="4/4", level_db=0.0,
               arc=[(-1, .05), (0, .10), (0.35, .22), (0.62, .36), (0.86, .55), (1.0, .70)],
               prog=[[(0, 2, "5"), (6, 2, "5"), (0, 2, "sus2"), (3, 2, "5")], [(0, 2, "sus2"), (6, 2, ""), (4, 2, "5"), (3, 2, "")]], b_thr=0.5,
               drone=dict(lvl=1.0, chunk_bars=2, fifth=True),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.4, lo=0.14, hi=0.5, voices=4),
               melody=dict(inst="lute", lvl=1.5, lo=-1, hi=-0.5, cut=(0.22, 0.45), play=2, rest=1, dens=0.3, reg=(55, 69), motif="bruksel", motif_p=1.0),
               perc=dict(pattern="heartbeat", lvl=0.9, lo=0.28, hi=0.7, pitch=92, amp=0.7),
               bell=dict(period=3, offset=1, midi=62, ring=1.4, lo=-1, hi=-0.5, cut=(0.3, 0.6), lvl=0.9),
               finale="c0",
               finale_gain=dict(rv=0.45, riser=0.10, roll=0.07, cluster=0.2, timp=0.35, timp2=0.28, gong=0.25, sub=0.12,
                                organ=0.3, choir=0.3, bowed=0.45, bell=0.4, lute=0.3)),
    # c1: merak/miras — dört tahtın çocuğu: lavta → klavsen → org → bas/davul sırayla girer (D mixolydian, 6/8)
    "c1": dict(mood="curious", tonic=38, mode="mixolydian", bpm=68, meter="6/8", level_db=-1.0,
               arc=[(-1, .30), (0, .34), (0.12, .43), ("c1s6", 0.28, .28), ("c1s10", 0.50, .52), ("c1s14", 0.66, .66), ("c1s16", 0.86, .50), (1.0, .42)],
               prog=[[(0, 2, ""), (6, 1, ""), (3, 1, ""), (0, 2, ""), (6, 1, ""), (3, 1, "")],
                     [(0, 1, ""), (3, 1, ""), (6, 1, ""), (3, 1, ""), (0, 2, ""), (4, 2, "")]], b_thr=0.5,
               drone=dict(lvl=0.5, chunk_bars=4, fifth=True),
               arp=dict(inst="lute", pattern="lilt", lvl=0.85, p0=0.75, p1=0.25),
               melody=dict(inst="harp", lvl=0.8, lo=0.36, hi=0.42, play=2, rest=2, dens=0.45, reg=(66, 81), motif="merak"),
               choir=dict(inst="organ", lvl=0.38, lo=0.40, hi=0.50, voices=3, stops=(("flute", 1.0, 1.0), ("flute", 0.3, 2.0)), attack=0.4),
               perc=dict(pattern="lilt", tef="lilt", lvl=0.5, lo=0.44, hi=0.55, pitch=110, amp=0.55),
               bass=dict(inst="lute", pattern="lilt", lvl=0.6, lo=0.48, hi=0.56)),
    # c2: taç satılık — gerilim: bas ostinato, klavsen 'sikke' parıltıları, regal org; Plus Ultra'da yükseliş (A dorian)
    "c2": dict(mood="tense", tonic=45, mode="dorian", bpm=68, meter="4/4", level_db=0.0,
               arc=[(-1, .28), (0, .30), (0.2, .40), ("c2s6", 0.40, .52), ("c2s8", 0.55, .66), ("c2s13", 0.88, .84), ("c2s14", 0.94, .60), (1.0, .55)],
               prog=[[(0, 2, ""), (6, 2, ""), (0, 2, ""), (3, 2, "")], [(0, 1, "5"), (6, 1, "5"), (3, 1, ""), (4, 1, ""), (0, 2, ""), (6, 2, "")]], b_thr=0.7,
               drone=dict(lvl=0.8, mode="roots", chunk_bars=2, fifth=False),
               bass=dict(inst="lute", pattern="p332", lvl=0.9, lo=0.25, hi=0.40),
               arp=dict(inst="harp", pattern="tick", lvl=0.5, lo=0.35, hi=0.50, p0=0.5, p1=0.4, transpose=12),
               perc=dict(pattern="p332", tef="sparse", lvl=0.8, lo=0.40, hi=0.55, pitch=98, fill=4),
               choir=dict(inst="organ", stops=(("reed", 1.0, 1.0), ("principal", 0.4, 1.0)), lvl=0.45, lo=0.55, hi=0.70, voices=4, attack=0.6),
               melody=dict(inst="lute", lvl=0.8, lo=0.55, hi=0.62, play=2, rest=2, dens=0.35, reg=(57, 72), motif="sorgu")),
    # c3: şehirlerin isyanı — acil, yürüyüş davulları; Villalar zirvesi sonra ağıt (E aeolian, 84 bpm)
    "c3": dict(mood="tense", tonic=40, mode="aeolian", bpm=84, meter="4/4", level_db=0.0,
               arc=[(-1, .32), (0, .36), ("c3s3", 0.35, .55), ("c3s4", 0.62, .90), ("c3s5", 0.74, .78), ("c3s6", 0.82, .30), (1.0, .24)],
               prog=[[(0, 2, ""), (5, 1, ""), (6, 1, ""), (0, 2, ""), (3, 1, ""), (4, 1, "")], [(0, 1, "5"), (6, 1, "5"), (5, 1, ""), (6, 1, ""), (0, 2, "5"), (4, 2, "5")]], b_thr=0.75,
               drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
               bass=dict(inst="lute", pattern="drive", lvl=0.8, lo=0.40, hi=0.55, p=0.92),
               perc=dict(pattern="march", tef="drive", lvl=0.8, lo=0.40, hi=0.55, pitch=96, fill=4),
               arp=dict(inst="lute", pattern="ostinato", lvl=0.55, lo=0.50, hi=0.65, p0=0.7, p1=0.3),
               choir=dict(inst="organ", stops=(("reed", 1.0, 1.0), ("principal", 0.5, 1.0)), lvl=0.5, lo=0.65, hi=0.8, voices=4, attack=0.4),
               melody=dict(inst="lute", lvl=0.85, lo=-1, hi=-0.5, win=[(("c3s6", 0.80), 2.0)], play=2, rest=2, dens=0.2, reg=(59, 74), motif="agit")),
    # c4: Worms'ta keşiş — koral: org + koro + çan (G mixolydian, 58 bpm)
    "c4": dict(mood="solemn", tonic=43, mode="mixolydian", bpm=58, meter="4/4", level_db=0.0,
               arc=[(-1, .22), (0, .26), ("c4s5", 0.30, .46), ("c4s6", 0.42, .62), ("c4s7", 0.52, .50), ("c4s8", 0.62, .66), ("c4s12", 0.78, .52), ("c4s15", 0.88, .36), (1.0, .28)],
               prog=[[(0, 2, ""), (3, 2, ""), (0, 2, "sus4"), (6, 2, "")], [(0, 2, ""), (4, 2, ""), (3, 2, ""), (0, 2, "5")]], b_thr=0.55,
               drone=dict(lvl=0.7, chunk_bars=4, fifth=True),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.75, lo=0.22, hi=0.40, voices=4),
               arp=dict(inst="lute", pattern="sparse", lvl=0.6, lo=0.28, hi=0.4, p0=0.8, p1=0.2),
               melody=dict(inst="organ", lvl=0.6, lo=0.45, hi=0.55, play=2, rest=2, dens=0.1, reg=(59, 74), motif="agit"),
               perc=dict(pattern="proc", lvl=0.7, lo=0.50, hi=0.62, pitch=90, amp=0.7),
               bell=dict(period=2, offset=0, midi=67, ring=1.3, lo=0.2, hi=0.3, lvl=0.5, alt=[0, 0, -5, 0])),
    # c5: imparator hep başka yerde — ağır, kasvetli; Mühlberg'de kısa heybet, sonra çözülüş (A aeolian, 62 bpm)
    "c5": dict(mood="grave", tonic=33, mode="aeolian", bpm=62, meter="4/4", level_db=0.0,
               arc=[(-1, .25), (0, .28), ("c5s3", 0.20, .42), ("c5s6", 0.45, .55), ("c5s9", 0.66, .78), ("c5s11", 0.80, .50), ("c5s13", 0.92, .42), (1.0, .35)],
               prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, ""), (3, 2, ""), (4, 2, ""), (0, 2, "5")]], b_thr=0.62,
               drone=dict(lvl=0.95, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
               choir=dict(inst="organ", stops=(("reed", 1.0, 1.0), ("principal", 0.35, 1.0), ("flute", 0.3, 2.0)), lvl=0.55, lo=0.30, hi=0.45, voices=4, attack=0.9),
               arp=dict(inst="lute", pattern="sparse", lvl=0.7, lo=0.20, hi=0.35, p0=0.8, p1=0.2),
               perc=dict(pattern="proc2", lvl=0.8, lo=0.38, hi=0.52, pitch=84, amp=0.7, fill=4),
               melody=dict(inst="organ", lvl=0.55, lo=0.48, hi=0.6, play=2, rest=2, dens=0.1, reg=(57, 72), motif="agit"),
               bell=dict(period=4, offset=2, midi=57, ring=1.6, lo=0.2, hi=0.35, cut=(0.7, 0.85), lvl=0.6)),
    # c6: kral, esir, düello — Pavia davulları, Roma'nın yağması, sonda 'Hanımlar Barışı' ferahlığı (E dorian, 76 bpm)
    "c6": dict(mood="tense", tonic=40, mode="dorian", bpm=76, meter="4/4", level_db=0.0,
               arc=[(-1, .30), (0, .35), ("c6s3", 0.20, .60), ("c6s5", 0.38, .50), ("c6s7", 0.52, .86), ("c6s9", 0.62, .70), ("c6s11", 0.72, .42), ("c6s12", 0.86, .36), (1.0, .30)],
               prog=[[(0, 2, ""), (6, 2, ""), (0, 2, "5"), (3, 2, "")], [(0, 1, "5"), (6, 1, "5"), (4, 1, ""), (3, 1, ""), (0, 2, ""), (6, 2, "5")]], b_thr=0.7,
               drone=dict(lvl=0.8, mode="roots", chunk_bars=2, fifth=True),
               bass=dict(inst="lute", pattern="drive", lvl=0.8, lo=0.42, hi=0.55, p=0.9, win=[(-1, ("c6s11", 0.70))]),
               perc=dict(pattern="march", tef="eighths", lvl=0.85, lo=0.40, hi=0.55, pitch=96, fill=4, win=[(-1, ("c6s11", 0.72))]),
               arp=dict(inst="lute", pattern="ostinato", lvl=0.6, lo=0.42, hi=0.58, p0=0.7, p1=0.3, win=[(-1, ("c6s11", 0.72))]),
               choir=dict(inst="organ", stops=(("reed", 1.0, 1.0), ("principal", 0.5, 1.0)), lvl=0.5, lo=0.60, hi=0.75, voices=4, attack=0.5),
               melody=dict(inst="harp", lvl=0.9, lo=-1, hi=-0.5, win=[(("c6s11", 0.72), 2.0)], play=2, rest=2, dens=0.45, reg=(64, 79), motif="merak")),
    # c7: Sultan — destansı: davul düzeni, regal org, koro, Viyana'da doruk; hafif Frigiyen renk (D phrygian, 80 bpm)
    "c7": dict(mood="epic", tonic=38, mode="phrygian", bpm=80, meter="4/4", level_db=1.5,
               arc=[(-1, .35), (0, .40), ("c7s3", 0.20, .62), ("c7s6", 0.42, .88), ("c7s8", 0.55, .96), ("c7s10", 0.66, .82), ("c7s14", 0.90, .45), (1.0, .38)],
               prog=[[(0, 2, "5"), (6, 2, ""), (0, 2, ""), (3, 2, "")], [(0, 1, ""), (1, 1, ""), (0, 1, ""), (6, 1, ""), (3, 2, ""), (0, 2, "5")]], b_thr=0.6,
               drone=dict(lvl=0.9, chunk_bars=2, fifth=True),
               bass=dict(inst="lute", pattern="drive", lvl=0.85, lo=0.35, hi=0.5, p=0.92),
               perc=dict(pattern="duyek", tef="eighths", lvl=0.95, lo=0.36, hi=0.5, pitch=90, fill=4, amp=0.65),
               arp=dict(inst="lute", pattern="roll", lvl=0.6, lo=0.40, hi=0.55, p0=0.7, p1=0.3, strum=2),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.6, lo=0.52, hi=0.68, voices=5, shift=1.0),
               arp2=dict(inst="harp", pattern="pulse", lvl=0.35, lo=0.5, hi=0.65, p0=0.7, p1=0.3, transpose=12),
               melody=dict(inst="organ", lvl=0.7, lo=0.5, hi=0.62, play=2, rest=2, dens=0.35, reg=(62, 77), motif="yuruyus"),
               bell=dict(period=4, offset=0, midi=62, ring=1.2, lo=0.6, hi=0.8, lvl=0.5, alt=[0, 7])),
    # c8: Akdeniz'de Barbaros — dalgalanan 6/8 deniz, gallop davulu; Cezayir fırtınası sonda (A mixolydian, 78 bpm)
    "c8": dict(mood="epic", tonic=45, mode="mixolydian", bpm=78, meter="6/8", level_db=1.2,
               arc=[(-1, .35), (0, .40), ("c8s2", 0.10, .60), ("c8s4", 0.30, .78), ("c8s7", 0.52, .76), ("c8s10", 0.86, .96), ("c8s11", 0.96, .40), (1.0, .38)],
               prog=[[(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "")], [(0, 1, ""), (3, 1, ""), (6, 1, ""), (3, 1, ""), (0, 2, "5"), (4, 2, "")]], b_thr=0.7,
               drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
               arp=dict(inst="lute", pattern="sea", lvl=0.7, lo=0.30, hi=0.45, p0=0.8, p1=0.2),
               bass=dict(inst="lute", pattern="drive", lvl=0.75, lo=0.45, hi=0.58, p=0.95),
               perc=dict(pattern="gallop", tef="lilt", lvl=0.85, lo=0.45, hi=0.58, pitch=92, fill=4, amp=0.65),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.55, lo=0.55, hi=0.7, voices=4),
               melody=dict(inst="organ", lvl=0.65, lo=0.50, hi=0.62, play=2, rest=2, dens=0.35, reg=(64, 79), motif="agit"),
               bell=dict(period=3, offset=0, midi=69, ring=1.0, lo=0.8, hi=0.9, lvl=0.45, alt=[0, -2, -5])),
    # c9: Yeni Dünya — şaşkınlık: parıltılı çanlar, yüksek koro, yükselen arpej; ortada vicdan gölgesi (C lydian, 66 bpm)
    "c9": dict(mood="wonder", tonic=36, mode="lydian", bpm=66, meter="4/4", level_db=0.0,
               arc=[(-1, .30), (0, .35), ("c9s2", 0.15, .66), ("c9s6", 0.42, .60), ("c9s7", 0.52, .38), ("c9s10", 0.70, .42), ("c9s13", 0.88, .64), (1.0, .55)],
               prog=[[(0, 2, ""), (1, 2, ""), (0, 2, "add9"), (4, 2, "")], [(5, 2, ""), (2, 2, ""), (4, 2, ""), (0, 2, "5")]], b_thr=0.0,
               drone=dict(lvl=0.7, chunk_bars=4, fifth=True, bright=0.7),
               choir=dict(inst="choir", vowel=("u", "a"), lvl=0.6, lo=0.30, hi=0.45, voices=4, shift=1.05),
               arp=dict(inst="lute", pattern="roll", lvl=0.75, lo=0.28, hi=0.4, p0=0.8, p1=0.2, low=48),
               arp2=dict(inst="harp", pattern="sparse", lvl=0.5, lo=0.5, hi=0.62, p0=0.8, p1=0.2, transpose=12),
               melody=dict(inst="harp", lvl=0.75, lo=0.36, hi=0.46, play=2, rest=2, dens=0.4, reg=(67, 83), motif="merak"),
               perc=dict(pattern="proc2", lvl=0.5, lo=0.55, hi=0.68, pitch=104, amp=0.55),
               bell=dict(period=2, offset=0, midi=74, ring=1.5, lo=0.30, hi=0.4, lvl=0.45, alt=[0, 7, 4, 9])),
    # c10: faturayı kim ödedi — defter tıkırtısı: sabit 'tik' arpej, soğuk bas, kasvetli org; çözülmeden biter (A dorian, 72 bpm)
    "c10": dict(mood="tense", tonic=45, mode="dorian", bpm=72, meter="4/4", level_db=-0.5,
                arc=[(-1, .30), (0, .32), ("c10s5", 0.50, .50), ("c10s8", 0.80, .74), (1.0, .50)],
                prog=[[(0, 2, ""), (0, 2, "sus2"), (6, 2, ""), (3, 2, "")], [(0, 2, "5"), (4, 2, ""), (3, 2, ""), (6, 2, "5")]], b_thr=0.68,
                drone=dict(lvl=0.8, mode="roots", chunk_bars=2, fifth=False, bright=0.5),
                arp=dict(inst="harp", pattern="tick", lvl=0.55, lo=0.2, hi=0.35, p0=0.9, p1=0.1, transpose=12),
                bass=dict(inst="lute", pattern="tick", lvl=0.8, lo=0.28, hi=0.4, p=0.95),
                perc=dict(pattern="none", tef="sparse", lvl=0.8, lo=0.4, hi=0.5, pitch=96, tef_amp=0.5),
                choir=dict(inst="organ", stops=(("reed", 1.0, 1.0), ("principal", 0.4, 1.0)), lvl=0.5, lo=0.5, hi=0.65, voices=4, attack=0.7),
                melody=dict(inst="lute", lvl=0.7, lo=0.45, hi=0.55, play=1, rest=3, dens=0.15, reg=(57, 70), motif="sorgu")),
    # c11: adamın kendisi — yakın: tek lavta, yumuşak çello, çok hafif koro; Isabel'e ağıt (D dorian, 3/4, 60 bpm)
    "c11": dict(mood="intimate", tonic=38, mode="dorian", bpm=60, meter="3/4", level_db=-2.0,
                arc=[(-1, .20), (0, .22), ("c11s2", 0.15, .26), ("c11s4", 0.50, .36), ("c11s5", 0.62, .44), ("c11s7", 0.80, .30), (1.0, .22)],
                prog=[[(0, 2, ""), (3, 2, ""), (0, 2, "sus2"), (6, 2, "")], [(0, 2, "add9"), (4, 2, ""), (3, 2, ""), (0, 2, "")]], b_thr=0.4,
                drone=dict(lvl=0.55, chunk_bars=4, fifth=True, bright=0.5),
                arp=dict(inst="lute", pattern="lull", lvl=0.9, lo=-1, hi=-0.5, p0=0.85, p1=0.15),
                melody=dict(inst="lute", lvl=1.0, lo=0.28, hi=0.38, play=2, rest=2, dens=0.35, reg=(60, 74), motif="bruksel"),
                choir=dict(inst="choir", vowel=("u", "o"), lvl=0.35, lo=0.30, hi=0.40, voices=3),
                bass=dict(inst="cello", pattern="whole", lvl=0.5, lo=0.30, hi=0.40)),
    # c12: bırakmak — Brüksel temasının dönüşü (c0 motifi), koro+org; Yuste'de seyrelir, çanlar (D aeolian, 58 bpm)
    "c12": dict(mood="solemn", tonic=38, mode="aeolian", bpm=58, meter="4/4", level_db=0.0,
                arc=[(-1, .20), (0, .30), ("c12s4", 0.30, .56), ("c12s5", 0.45, .60), ("c12s7", 0.62, .42), ("c12s8", 0.72, .36), ("c12s10", 0.90, .30), (1.0, .20)],
                prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, ""), (3, 2, ""), (6, 2, ""), (5, 2, "")]], b_thr=0.5,
                drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
                choir=dict(inst="choir", vowel=("o", "a"), lvl=0.7, lo=0.26, hi=0.40, voices=4),
                melody=dict(inst="organ", lvl=0.6, lo=0.30, hi=0.42, play=2, rest=2, dens=0.1, reg=(57, 72), motif="bruksel"),
                arp=dict(inst="lute", pattern="sparse", lvl=0.7, lo=-1, hi=-0.5, p0=0.8, p1=0.2),
                perc=dict(pattern="proc", lvl=0.6, lo=0.45, hi=0.55, pitch=88, amp=0.7),
                bell=dict(period=3, offset=0, midi=62, ring=1.5, lo=-1, hi=-0.5, lvl=0.65, alt=[0, 0, -7])),
    # c13: hesap — açık uçlu soru, yine de çözülen kapanış; Brüksel motifi D'ye iner, çanlar, sönüş (D dorian, 58 bpm)
    "c13": dict(mood="solemn", tonic=38, mode="dorian", bpm=58, meter="4/4", level_db=0.0,
                arc=[(-1, .20), (0, .26), ("c13s3", 0.30, .38), ("c13s8", 0.80, .52), (1.0, .42)],
                prog=[[(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "sus4")], [(0, 2, "sus2"), (3, 2, ""), (4, 2, ""), (0, 2, "5")]], b_thr=0.45,
                drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
                choir=dict(inst="choir", vowel=("o", "a"), lvl=0.65, lo=0.28, hi=0.42, voices=4),
                arp=dict(inst="lute", pattern="pavane", lvl=0.75, lo=-1, hi=-0.5, p0=0.85, p1=0.15),
                melody=dict(inst="lute", lvl=0.9, lo=0.30, hi=0.4, play=2, rest=2, dens=0.2, reg=(57, 72), motif="bruksel"),
                bell=dict(period=4, offset=1, midi=62, ring=1.5, lo=-1, hi=-0.5, lvl=0.6, alt=[0, -5]),
                finale="c13"),
}


def junction_pads(c, cid, level_db=-1.0):
    """Cue başında/sonunda (çapraz geçiş bölgesi) kökün açık beşlisinde (kök, beşli, oktav, beşli+8) org + koro yatağı:
    çapraz geçiş çukuru kapanır; seviye cue gövdesinin ölçülen gücüne (diag) göre ayarlanır."""
    d = c.diag
    a, b = int(c.t_open + 2), int(c.t_close - 2)
    if b <= a + 3 or not d:
        return
    e = sum(arr[a:b].sum() for arr in d.values()) / (b - a) / SR
    body_db = 10 * np.log10(e + 1e-18)
    root = c.tonic + 12 if c.tonic < 41 else c.tonic
    notes = [root, root + 7, root + 12, root + 19]
    unit_db = 10 * np.log10(len(notes) * 10 ** (REF["organ"] / 10) + 3 * 10 ** (REF["choir"] / 10))
    gain = 10 ** ((body_db + level_db - unit_db) / 20)

    def place(t0, dur, attack, release):
        for k, m in enumerate(notes):
            y = organ_note(_hz(m), dur, 0.7, c.rng, stops=(("flute", 1.0, 1.0), ("principal", 0.30, 1.0), ("flute", 0.25, 2.0)),
                           attack=attack, release=release, trem=False, chiff=0.0)
            c.put("organ", y, t0, gain=gain, pan=[-0.15, 0.15, -0.25, 0.25][k])
        for k, m in enumerate(notes[:3]):
            y = choir_note(_hz(m), dur, 0.7, c.rng, vowel="o", voices=3, attack=attack, release=release)
            c.put("choir", y, t0, gain=gain, pan=[-0.3, 0.3, 0.0][k])

    if cid != "c0":
        place(0.0, min(c.open_sec + 4.0, c.T), 1.5, 2.5)
    if cid not in ("c0", "c13"):
        t0 = c.t_close - 3.0
        place(t0, c.T - t0, 2.0, 1.0)


# ═══════════════════════════ özel sahneler: c0 açılışı ve c13 kapanışı ═══════════════════════════
def _gate(c, t0, t1, ramp=0.008):
    """[t0,t1] aralığında dry ve send'i (ramp'lı) susturur — vuruş öncesi 'nefes kesen' boşluk."""
    i0, i1 = max(int(t0 * SR), 0), min(int(t1 * SR), c.n)
    r = int(ramp * SR)
    g = np.zeros(i1 - i0, dtype=np.float32)
    g[:r] = 0.5 + 0.5 * np.cos(np.pi * np.arange(r) / r)
    g[-r:] = 0.5 - 0.5 * np.cos(np.pi * np.arange(r) / r)
    c.dry[i0:i1] *= g[:, None]
    c.send[i0:i1] *= g


def finale_c0(c, t_hit, G=None):
    """c0: gerilim yükselişi (ters gong + gürültü yükselişi + hızlanan timpani rulosu + koro kümesi), 0,24 sn nefes boşluğu,
    t_hit anında TEK vuruş (timpani + gong + alt-bas) ve altın tonlu D majör açılış (org + koro + yaylı + çan parıltısı + lavta)."""
    g = dict(rv=0.30, riser=0.05, roll=0.10, cluster=0.35, timp=1.0, timp2=0.8, gong=0.55, sub=0.30,
             organ=0.55, choir=0.55, bowed=0.8, bell=0.7, lute=0.6)
    g.update(G or {})
    rng = c.rng
    pk = t_hit - 0.24
    # yükseliş
    rv = D.fade_edges(gong(146.83, 9.0, 0.9, rng)[::-1][-int(8.0 * SR):], 0.6, 0.0)
    c.put("fx", rv, pk - len(rv) / SR, gain=g["rv"])
    ri = _level(D.noise_riser(7.0, 300, 6500, rng, curve=1.4), -26.0, "sustain")
    c.put("fx", ri, pk - 7.0, gain=g["riser"])
    t, t0r = t_hit - 10.0, t_hit - 10.0
    k = 0
    while t < t_hit - 0.45:
        u = (t - t0r) / 9.5
        vel = 0.16 + 0.72 * u ** 1.3
        c.put("perc", timp(73.42, vel, rng, dur=1.4), t, gain=g["roll"], pan=0.12 if k % 2 else -0.12)
        t += max(0.55 * (1 - 0.84 * u), 0.085)
        k += 1
    for m in (50, 52, 53, 57, 59):
        y = choir_note(_hz(m), 11.8, 0.7, rng, vowel="o", vowel2="a", morph=(0.35, 0.95), attack=9.5, release=0.12, voices=3)
        c.put("choir", y, t_hit - 12.0, gain=g["cluster"], pan=float(rng.uniform(-0.4, 0.4)))
    _gate(c, pk, t_hit - 0.005)
    # tek vuruş
    c.put("perc", timp(73.42, 1.0, rng, dur=3.0), t_hit, gain=g["timp"])
    c.put("perc", timp(55.0, 0.9, rng, dur=3.0), t_hit, gain=g["timp2"])
    c.put("fx", gong(146.83, 10.0, 0.9, rng, bloom=1.3), t_hit, gain=g["gong"])
    c.put("fx", sub(64, 30, 4.0, 0.9), t_hit, gain=g["sub"])
    # altın D majör (üçlü: Fa# — 'Picardy'): org + koro + yaylı + çanlar + lavta
    cd = min(c.T - t_hit + 1.0, 12.0)
    pans = [-0.2, 0.2, -0.3, 0.3, 0.1, -0.1]
    for kk, m in enumerate((50, 57, 62, 66, 69, 74)):
        y = organ_note(_hz(m), cd, 0.85, rng, stops=(("flute", 1.0, 1.0), ("principal", 0.6, 1.0), ("reed", 0.3, 1.0), ("flute", 0.3, 2.0)),
                       attack=0.10, release=3.2)
        c.put("organ", y, t_hit + 0.012 * kk, gain=g["organ"], pan=pans[kk])
    for kk, m in enumerate((50, 57, 62, 66, 69)):
        y = choir_note(_hz(m), cd, 0.9, rng, vowel="a", voices=3, attack=0.55, release=3.2)
        c.put("choir", y, t_hit + 0.03 * kk, gain=g["choir"], pan=pans[kk])
    for (m, gg) in ((38, 1.0), (45, 0.7)):
        y = bowed_note(_hz(m), cd, 0.9, rng, attack=0.3, release=3.2, bright=1.0)
        c.put("drone", y, t_hit, gain=g["bowed"] * gg, pan=0.0)
    for kk, (m, gg) in enumerate(((74, 1.0), (81, 0.7), (90, 0.5), (86, 0.45))):
        c.put("bell", bell(_hz(m), 7.5, 0.75, rng, ring=1.7, strike=0.4), t_hit + 0.10 + 0.16 * kk, gain=gg * g["bell"], pan=0.3 * (1 if kk % 2 else -1))
    for kk, m in enumerate((50, 57, 62, 66, 69, 74)):
        c.put("lute", lute_note(_hz(m), 0.8, rng, ring=1.3), t_hit + 0.03 + 0.045 * kk, gain=g["lute"], pan=-0.2 + 0.08 * kk)


def finale_c13(c, t_final, G=None):
    """c13: soru açık kalır ama müzik çözülür — açık beşliye Fa# (üçlü) eklenir; Brüksel motifi D'ye iner; çanlar; sönüş."""
    g = dict(organ=0.6, choir=0.7, bowed=0.8, lute=0.8, bell=0.7)
    g.update(G or {})
    rng = c.rng
    cd = c.T - t_final + 0.5
    pans = [-0.2, 0.2, -0.3, 0.3, 0.1, -0.1]
    for kk, m in enumerate((50, 57, 62, 66, 69)):
        y = organ_note(_hz(m), cd, 0.7, rng, stops=(("flute", 1.0, 1.0), ("principal", 0.35, 1.0), ("flute", 0.3, 2.0)), attack=1.2, release=4.0)
        c.put("organ", y, t_final + 0.05 * kk, gain=g["organ"], pan=pans[kk])
    for kk, m in enumerate((50, 57, 62, 66, 69, 74)):
        y = choir_note(_hz(m), cd, 0.75, rng, vowel="o", vowel2="a", morph=(0.15, 0.6), voices=3, attack=1.8, release=4.0)
        c.put("choir", y, t_final + 0.08 * kk, gain=g["choir"], pan=pans[kk])
    for (m, gg) in ((38, 1.0), (45, 0.7)):
        y = bowed_note(_hz(m), cd, 0.8, rng, attack=1.2, release=4.0, bright=0.7)
        c.put("drone", y, t_final, gain=g["bowed"] * gg)
    for (dt, m, v) in ((0.4, 69, 0.55), (1.5, 67, 0.5), (2.6, 66, 0.5), (4.0, 62, 0.55)):
        c.put("lute", lute_note(_hz(m), v, rng, ring=1.6), t_final + dt, gain=g["lute"], pan=0.15)
    for (dt, m, gg, ring) in ((1.0, 62, 0.8, 1.4), (4.6, 50, 1.0, 1.8)):
        c.put("bell", bell(_hz(m), 7.5, 0.75, rng, ring=ring, strike=0.45), t_final + dt, gain=gg * g["bell"])


FINALES = {"c0": finale_c0, "c13": finale_c13}


# ═══════════════════════════ cue geometrisi ve çalma ═══════════════════════════
XFADE = [6.0, 5.0, 4.0, 7.0, 6.0, 5.0, 5.0, 4.0, 7.0, 5.0, 7.0, 6.0, 8.0]   # i. sınırdaki çapraz geçiş süresi (cue i → i+1), sn
TITLE_DELAY = 0.4        # başlık vuruşu: c0 t1 + 0,4 sn
TARGET_RMS_DB = -27.5    # ducking ÖNCESİ müzik bandının ortalama RMS hedefi (dBFS)


def geometry(chapters, total, tail):
    """Her cue için başlangıç/bitiş (video zaman ekseni), bölümün cue içindeki yeri ve çapraz geçişler.
    Çapraz geçiş merkezi: bölüm kartı boşluğunun ortası (c0→c1: başlık vuruşunun 3 sn sonrası)."""
    n = len(chapters)
    J = []
    for i in range(n - 1):
        if i == 0:
            J.append(chapters[0]["t1"] + TITLE_DELAY + 3.0)
        else:
            J.append(chapters[i]["t1"] + chapters[i].get("gap_after", 3.0) / 2)
    geo = []
    for i, ch in enumerate(chapters):
        xin = XFADE[i - 1] if i > 0 else 0.0
        xout = XFADE[i] if i < n - 1 else 0.0
        start = (J[i - 1] - xin / 2) if i > 0 else 0.0
        end = (J[i] + xout / 2) if i < n - 1 else total + tail
        geo.append(dict(id=ch["id"], start=start, end=end, T=end - start, t0c=ch["t0"] - start, t1c=ch["t1"] - start,
                        xin=xin, xout=xout, t0=ch["t0"], t1=ch["t1"]))
    return geo


def _anchor_u(sid, default_u, ch, sent_by_id, dt=0.0):
    sn = sent_by_id.get(sid)
    if sn is None:
        return float(default_u)
    return float(np.clip((sn["t0"] + dt - ch["t0"]) / max(ch["t1"] - ch["t0"], 1e-6), 0.01, 0.99))


def resolve_spec(spec, ch, sent_by_id):
    """Cue tanımındaki hikâye çıpalarını (cümle kimliği → u) sayısal değerlere çevirir: arc noktaları ("c3s4", varsayılan_u, yoğunluk[, dt]) ve
    katman pencereleri win=[(a, b)] (a/b sayı ya da ("c6s11", varsayılan_u)). Bulunamazsa varsayılan u kullanılır → ses yamalarında kırılmaz."""
    import copy
    sp = copy.deepcopy(spec)
    arc = []
    for a in sp["arc"]:
        if isinstance(a[0], str):
            sid, du, I = a[0], a[1], a[2]
            dt = a[3] if len(a) > 3 else 0.0
            arc.append((_anchor_u(sid, du, ch, sent_by_id, dt), float(I)))
        else:
            arc.append((float(a[0]), float(a[1])))
    arc.sort(key=lambda p: p[0])
    for i in range(1, len(arc)):
        if arc[i][0] <= arc[i - 1][0]:
            arc[i] = (arc[i - 1][0] + 1e-3, arc[i][1])
    sp["arc"] = arc
    for k, v in list(sp.items()):
        if isinstance(v, dict) and v.get("win"):
            v["win"] = [tuple(_anchor_u(x[0], x[1], ch, sent_by_id) if isinstance(x, (tuple, list)) else float(x) for x in w) for w in v["win"]]
    return sp


def build_cue(cid, g, tail, seed=0, spec=None):
    """Bir cue'nun tüm katmanlarını (reverb öncesi) üretir → Cue nesnesi (dry + send tamponları)."""
    spec = spec or CUES[cid]
    open_sec = g["xin"] + 1.0 if g["xin"] > 0 else 3.0
    close_sec = g["xout"] + 1.0 if g["xout"] > 0 else (tail + 0.75 if cid == "c13" else 4.0)
    c = Cue(cid, spec, g["T"], g["t0c"], g["t1c"], open_sec, close_sec, seed=seed)
    for key, fn in (("drone", layer_drone), ("choir", layer_pad), ("arp", layer_arp), ("arp2", layer_arp), ("bass", layer_bass),
                    ("melody", layer_melody), ("perc", layer_perc), ("bell", layer_bell)):
        if spec.get(key):
            fn(c, spec[key])
    junction_pads(c, cid, spec.get("pad_db", -1.0))
    fin = spec.get("finale")
    if fin == "c0":
        FINALES["c0"](c, g["t1c"] + TITLE_DELAY, spec.get("finale_gain"))
    elif fin == "c13":
        FINALES["c13"](c, g["t1c"] + 0.25, spec.get("finale_gain"))
    return c


def finish_cue(c, cid):
    """Reverb (algoritmik IR + fftconvolve) + cue ana süzgeci → float32 (n,2)."""
    ir = D.hall_ir(2.2)
    wet = D.reverb_wet(c.send, ir)[:c.n]
    out = c.dry + wet * 1.0
    out = D.sosfilt(_sos([("hp", 28, 0, 0.7), ("highshelf", 6500, -2.5, 0.7)]), out, axis=0).astype(np.float32)
    if cid == "c13":
        out = D.fade_edges(out, 0.0, 3.4)
    return out


def _render_job(job):
    """Çok işlemli çalıştırma için üst düzey fonksiyon: tek cue üretir (float32 (n,2), reverb dahil, seviyesiz)."""
    c = build_cue(job["id"], job["geo"], job["tail"], job["seed"], job.get("spec"))
    return job["id"], finish_cue(c, job["id"])


def _robust_rms_db(x, sr=SR):
    """1 sn'lik pencerelerin güç ortalaması; sessiz pencereler atılır, en yüksek %8 pencere kırpılır (vuruş/doruklar
    seviyeyi domine etmesin)."""
    m = x.mean(axis=1) if x.ndim == 2 else x
    w = sr
    nwin = len(m) // w
    if nwin < 2:
        return D.rms_db(m)
    p = np.mean(m[:nwin * w].reshape(nwin, w) ** 2, axis=1)
    p = p[p > 1e-9]
    if len(p) < 2:
        return D.rms_db(m)
    p = np.sort(p)
    keep = p[: max(1, int(len(p) * 0.92))]
    return float(10 * np.log10(np.mean(keep) + 1e-18))


def _code_hash():
    import hashlib
    h = hashlib.md5()
    for f in ("muzik.py", "ses_dsp.py"):
        h.update(open(os.path.join(HERE, f), "rb").read())
    return h.hexdigest()[:12]


def render_music(chapters, total, tail=7.0, workers=None, cache_dir=None, seed=0, verbose=True, only=None, timeline=None):
    """Tüm cue'ları üretir, çapraz geçişle birleştirir, ortalama RMS'i TARGET_RMS_DB'ye getirir.
    Döner: (music float32 (N,2), info dict). N = (total + tail)·SR. Ducking YOK (miks.py uygular)."""
    t_start = time.time()
    geo = geometry(chapters, total, tail)
    N = int(round((total + tail) * SR))
    ch = _code_hash()
    sent_by_id = {sn["id"]: sn for sn in (timeline or {}).get("sentences", [])}
    ch_by_id = {c_["id"]: c_ for c_ in chapters}
    jobs = []
    for g in geo:
        if only and g["id"] not in only:
            continue
        jobs.append(dict(id=g["id"], geo=g, tail=tail, seed=seed, spec=resolve_spec(CUES[g["id"]], ch_by_id[g["id"]], sent_by_id)))
    results = {}
    todo = []
    for j in jobs:
        key = None
        if cache_dir:
            import hashlib
            key = hashlib.md5(json.dumps([j["geo"], tail, seed, j["spec"], ch], sort_keys=True, default=str).encode()).hexdigest()[:16]
            fp = os.path.join(cache_dir, f"cue_{j['id']}_{key}.npy")
            j["_fp"] = fp
            if os.path.exists(fp):
                results[j["id"]] = np.load(fp)
                continue
        todo.append(j)
    if todo:
        workers = workers or max(1, min(os.cpu_count() or 1, 4))
        order = sorted(todo, key=lambda j: -j["geo"]["T"])
        if workers > 1 and len(order) > 1:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                for cid, arr in ex.map(_render_job, order):
                    results[cid] = arr
                    if verbose:
                        print(f"  cue {cid} hazır ({time.time() - t_start:5.1f} sn)", flush=True)
        else:
            for j in order:
                cid, arr = _render_job(j)
                results[cid] = arr
                if verbose:
                    print(f"  cue {cid} hazır ({time.time() - t_start:5.1f} sn)", flush=True)
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            import glob
            for j in todo:
                for old in glob.glob(os.path.join(cache_dir, f"cue_{j['id']}_*.npy")):   # eski sürümler birikmesin
                    try:
                        os.remove(old)
                    except OSError:
                        pass
                np.save(j["_fp"], results[j["id"]])
    # birleştir
    out = np.zeros((N, 2), dtype=np.float32)
    info = dict(cues=[], geo=geo)
    for i, g in enumerate(geo):
        if g["id"] not in results:
            continue
        x = results[g["id"]].astype(np.float32)
        spec = [j for j in jobs if j["id"] == g["id"]][0]["spec"]
        core0, core1 = int((g["xin"] + 1.0) * SR) if g["xin"] else 0, len(x) - int((g["xout"] + 1.0) * SR) if g["xout"] else len(x)
        rdb = _robust_rms_db(x[core0:core1])
        gain = D.db2lin(TARGET_RMS_DB + spec.get("level_db", 0.0) - rdb)
        # sol/sağ güç dengesi (pan dağılımı bir yana kaymasın): L kanalı ±1,5 dB içinde eşitlenir
        pl, pr = np.mean(x[core0:core1:7, 0].astype(np.float64) ** 2), np.mean(x[core0:core1:7, 1].astype(np.float64) ** 2)
        lr = float(np.clip(0.5 * 10 * np.log10((pr + 1e-18) / (pl + 1e-18)), -1.5, 1.5))
        x = x * np.array([gain * D.db2lin(lr), gain / D.db2lin(lr)], dtype=np.float32)
        env = np.ones(len(x), dtype=np.float32)
        if g["xin"] > 0:
            k = int(g["xin"] * SR)
            env[:k] = np.sin(np.linspace(0, np.pi / 2, k)).astype(np.float32)
        else:
            k = int(1.0 * SR)
            env[:k] = np.sin(np.linspace(0, np.pi / 2, k)).astype(np.float32) ** 2
        if g["xout"] > 0:
            k = int(g["xout"] * SR)
            env[-k:] *= np.cos(np.linspace(0, np.pi / 2, k)).astype(np.float32)
        s = int(round(g["start"] * SR))
        m = min(len(x), N - s)
        out[s:s + m] += x[:m] * env[:m, None]
        info["cues"].append(dict(id=g["id"], mood=spec["mood"], mode=spec["mode"], bpm=spec["bpm"], meter=spec["meter"], arc=spec["arc"],
                                 tonic_midi=spec["tonic"], start=round(g["start"], 2), end=round(g["end"], 2),
                                 length=round(g["T"], 2), chapter_dur=round(g["t1"] - g["t0"], 2), xin=g["xin"], xout=g["xout"],
                                 pre_gain_db=round(float(20 * np.log10(gain)), 2)))
    # genel ölçek: tüm bandın (sessizlik hariç) ortalama RMS'i TARGET_RMS_DB
    glob = _robust_rms_db(out)
    g2 = D.db2lin(TARGET_RMS_DB - glob)
    out *= np.float32(g2)
    info["global_gain_db"] = round(float(20 * np.log10(g2)), 2)
    info["render_sec"] = round(time.time() - t_start, 1)
    return out, info


# ═══════════════════════════ komut satırı (yalnız müzik önizleme) ═══════════════════════════
def _load_chapters():
    j = json.load(open(os.path.join(HERE, "out", "voice_chapters.json")))
    return j["chapters"], j["total"]


def main():
    ap = argparse.ArgumentParser(description="Şarlken müziği: ham (ducking'siz) müzik üretir.")
    ap.add_argument("--cue", help="tek cue (ör. c3) — önizleme WAV")
    ap.add_argument("--all", action="store_true", help="tüm müzik")
    ap.add_argument("--tail", type=float, default=7.0)
    ap.add_argument("--out", default=os.path.join(HERE, "out", "music_raw.wav"))
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--cache", default=None)
    a = ap.parse_args()
    chs, total = _load_chapters()
    only = [a.cue] if a.cue else None
    tp = os.path.join(HERE, "out", "timeline.json")
    tl = json.load(open(tp)) if os.path.exists(tp) else None
    x, info = render_music(chs, total, a.tail, workers=a.workers, cache_dir=a.cache, only=only, timeline=tl)
    if a.cue:
        g = [g for g in info["geo"] if g["id"] == a.cue][0]
        s, e = int(g["start"] * SR), int(g["end"] * SR)
        x = x[s:e]
    D.write_wav(a.out, x, SR)
    print("yazıldı:", a.out, f"{len(x) / SR:.1f} sn", info["render_sec"], "sn")


if __name__ == "__main__":
    main()
