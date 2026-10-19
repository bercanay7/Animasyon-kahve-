"""
muzik.py — "MEDICI" belgeseli (7 yayın parçası, 17 bölüm) için tamamen kodla sentezlenmiş, Rönesans esintili üretken müzik.

Tüm sesler numpy/scipy ile sentezdir (harici örnek/ses dosyası YOK, telifli melodi YOK; besteler tohumlu üretken ve özgün).
Ses kimliği : lavta (Karplus–Strong, çift kurs), klavsen, portatif org/regal, viola da gamba (drone + "çekilen yay"), formant süzgeçli koro pedi,
              çerçeve davulu (dum/tek/ka) + tef zilleri, gong/çan (YALNIZ müzikal tını; olay çanı değil), timpani/alt-bas (yalnız vurgu).
Perde paleti: BÖLÜM bazlı (parçadan bağımsız): ALTIN c0–c6 (Mixolydian/Ionian — sıcak, altın tonlu) · BEDEL c7–c11 (Dorian → Frigiyen/Aeolian —
              koyulaşan) · MİRAS c12–c16 (Lidyen/Aeolian — ağıt–parlak karışımı). Tempo 52–84 bpm. Her cue/bölüm kendi tonikinde; cue sınırlarında
              yalnız açık beşli (üçlüsüz) yatak → komşu cue'larla armonik çatışma olmaz.
Motifler    : "florin" (3–4 notalık yükselen parlak figür, ALTIN) · "palle" (altılı ritim: 2+2+2 hemiola) · "bedel" (alçak, tek çekilen yay, BEDEL) ·
              "miras" (sakin, tekrar eden üç nota; c0'da düşen, c16'da TERS çevrilmiş yankı) · Lorenzo teması (c6) · Duomo kubbesi (c4) ·
              "dönüş" (1434; c10'da geri sarılmış). Hepsi özgün, mod derecesi cinsinden tanımlı.
Yapı        : her bölüm için 'cue' (bölüm + 3 sn kart + yarım çapraz geçişler); bir bölüm birden çok 'kesit'e (section) bölünebilir (mod/tempo/
              çalgı değişimi, çapraz geçiş = cümle çıpasında). Yoğunluk eğrileri, olaylar (events), tema girişleri (theme), SESSİZLİK
              KAPILARI (gates: c7 yıldız an — sessizliğe giriş 0,6 sn önce) ve kuru duraklar (stops) timeline.json CÜMLE KİMLİKLERİNE çıpalı:
              ses yamalanınca (geçici Piper → ElevenLabs) çıpalar yeni zamanlara göre YENİDEN ÇÖZÜLÜR; çözülemeyen çıpa varsayılan u'ya düşer.
Parça       : 7 yayın parçası (script.PARTS: P1=c0–c2 · P2=c3–c5 · P3=c6–c7 · P4=c8–c9 · P5=c10–c11 · P6=c12–c13 · P7=c14–c16; ≈10 dk), her parça AYRI
              üretilir: MEDICI_PART=1..7 → out_pN/ (voice_chapters.json, timeline.json). Parçanın ilk bölümü t=0'da açılır (P1: c0 sonunda ana başlık
              vuruşu = c0 t1 + 0,4 sn; P2…P7: bölüm kartı yok, ilk çekimde 1,2–4,8 sn başlık bindirmesi); P1…P6 sonu "SIRADAKİ PARÇA" ekranı için 7 sn
              çözülme (varsayılan 'dissolve'; bölüm özel kapanış: spec'te end_kind — c11 'p2' çözülmeyen sus4, c16 'p3' çözülüş), P7 sonu "TÜM FİLM" +
              çözülüp söner. Parça sınırları BU DOSYADA sabit değildir: script.PARTS okunur (yoksa aşağıdaki PARTS_FALLBACK).
Reverb      : algoritmik salon IR'ı (RT60≈2,2 sn) + scipy.signal.fftconvolve.
Seviye      : ham müzik bandı (ducking ÖNCESİ) ortalama −27,5 dBFS RMS; ducking/yükseliş/EQ miks.py'dedir.
Önbellek    : kesit başına .npy (float16); anahtar = SENTEZ kodu özeti + çözülmüş spec (çıpalardan gelen zamanlar dahil) + geometri + tohum.

Kullanım (ayrı):  MEDICI_PART=3 python3 muzik.py --cue c7 --out /tmp/c7.wav      (tek cue/kesit önizleme; tüm kesitleri: --cue c13)
                  MEDICI_PART=3 python3 muzik.py --all --out /tmp/music.wav      (ducking'siz tüm parça müziği)
                  MEDICI_OUT_DIR=/yol  → out_pN yerine başka dizin (deneme/fixture için)
"""
import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import ses_dsp as D
from ses_dsp import SR, rng_for

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_WORKERS = 1          # paylaşımlı 4 çekirdekli, 16 GB makine: tek işçi (koordinatör kuralı; bellek taşmasını önler)

# ═══════════════════════════ parça tablosu (script.PARTS'tan; sabit kodlanmaz) ═══════════════════════════
PARTS_FALLBACK = {1: ["c0", "c1", "c2"], 2: ["c3", "c4", "c5"], 3: ["c6", "c7"], 4: ["c8", "c9"], 5: ["c10", "c11"], 6: ["c12", "c13"], 7: ["c14", "c15", "c16"]}
PERDE_FLAVOR = {1: "altin", 2: "bedel", 3: "miras"}


def part_table():
    """{parça: [bölüm kimlikleri]} — script.PARTS (tek doğru kaynak); script yüklenemezse PARTS_FALLBACK (2026-10-19 kararı: 7 parça)."""
    try:
        import script as S
        return {int(k): list(v) for k, v in S.PARTS.items()}
    except Exception:   # noqa
        return {k: list(v) for k, v in PARTS_FALLBACK.items()}


def part_chapters(n):
    return part_table()[int(n)]


def perde_of(cid):
    """Bölümün perdesi (1 ALTIN c0–c6 · 2 BEDEL c7–c11 · 3 MİRAS c12–c16). Perde BÖLÜM bazlıdır, parçaya bağlı değildir."""
    i = int(str(cid).lstrip("c"))
    return 1 if i <= 6 else (2 if i <= 11 else 3)


def flavor_of(cid):
    return PERDE_FLAVOR[perde_of(cid)]


def out_dir(part):
    """Parça çıktı dizini: out_pN (MEDICI_OUT_DIR ile değiştirilebilir — deneme/fixture). `out/` sembolik bağlantısı KULLANILMAZ."""
    return os.environ.get("MEDICI_OUT_DIR") or os.path.join(HERE, f"out_p{int(part)}")



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


def _gamba_amp(f0):
    """Viola da gamba: çello'dan daha burunsu/ince; 2.–5. harmonikler öne çıkar, ~1,2 kHz formantı, 3 kHz üstü çabuk söner."""
    g = lambda f, c, w: np.exp(-((f - c) / w) ** 2)
    return lambda f: (f0 / f) ** 0.85 * (1 + 1.0 * g(f, 330, 100) + 1.7 * g(f, 1200, 320) + 0.8 * g(f, 2300, 480)) / (1 + (f / 2700.0) ** 3)


def bowed_note(f0, dur, vel, rng, attack=0.35, release=0.9, ens=2, vib=(5.1, 6.5), swell=0.08, bright=0.65, body="cello", bend=0.0):
    """Yaylı drone / çello / viola da gamba: testere benzeri tablo × gövde rezonansları, gecikmeli vibrato, yay gürültüsü, yavaş yay baskısı dalgası.
    body="gamba": burunsu gövde + daha az vibrato. bend: son %40'ta cent cinsinden perde sapması (negatif = 'çekilen yay' düşüşü)."""
    n = int(round(dur * LO_SR))
    amp = _gamba_amp(f0) if body == "gamba" else _cello_amp(f0)
    if body == "gamba":
        vib = (vib[0] * 0.93, vib[1] * 0.55)
    if bright != 1.0:
        amp = (lambda a: (lambda f: a(f) / (1 + ((f / 1800.0) ** 2) * (1 / bright - 1) * 3)))(amp)
    tab = D.additive_table(f0, amp, rng, phase="saw", max_hz=7000, sr=LO_SR)
    t = np.arange(n) / LO_SR
    bendv = np.ones(n)
    if bend:
        bendv = 2.0 ** (bend / 1200.0 * D.smoothstep((t - 0.6 * dur) / max(0.4 * dur, 1e-3)))
    y = np.zeros(n)
    for k in range(ens):
        cents = (k - (ens - 1) / 2) * 3.6 + rng.uniform(-0.8, 0.8)
        vb = D.vibrato(n, vib[0] * rng.uniform(0.94, 1.06), vib[1] * rng.uniform(0.7, 1.1), delay=0.45 + 0.2 * rng.random(), rise=1.2, rng=rng, sr=LO_SR)
        y += D.wt_osc(tab, f0 * 2 ** (cents / 1200) * vb * bendv, n, phase0=rng.random(), sr=LO_SR)
    y /= ens
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


def dry_tick(rng, vel=0.6):
    """Kuru 'tıkırtı' (klavsen çubuğu / tahta): mizah duraklarının işareti. Mono, ~80 ms."""
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    y = D.bp(rng.standard_normal(n), 1800, 6500, 2) * np.exp(-t / 0.004) * 1.4
    y += np.sin(D.PI2 * 1650 * t) * np.exp(-t / 0.006) * 0.6 + 0.5 * np.sin(D.PI2 * 410 * t) * np.exp(-t / 0.012)
    y *= np.minimum(1.0, t / 0.0004)
    return y * (D.db2lin(-22.0 + 12 * (vel - 0.6)) / (np.sqrt(np.sum(y[:SR // 2] ** 2) / (SR // 2)) + 1e-12))


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
    """Bir bölümün (ya da bölüm kesitinin) müzik cue'su: ritim ızgarası, akor çizelgesi, yoğunluk eğrisi ve ses tamponları."""

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
        self.gates = []   # (t_fade_start, t_silent_a, t_silent_b, t_fade_end, floor_lin) — cue süresi eksenindedir
        self.events_log = []   # teşhis: (t, tür)
        self.chords = self._build_chords()

    # --- zaman / yoğunluk
    def u(self, t):
        return (t - self.t0c) / max(self.t1c - self.t0c, 1e-6)

    def I(self, t):
        return float(np.interp(self.u(t), self.arc[:, 0], self.arc[:, 1]))

    def t_of(self, sec):
        """Bölüm (kesit) başından saniye → cue süresi ekseni."""
        return self.t0c + float(sec)

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

    def add_gate(self, a_sec, b_sec, lead=0.6, rel=3.0, floor_db=None):
        """Sessizlik kapısı: [a,b] (bölüm saniyesi) arası müzik 'floor' seviyesine iner (None = tam sessizlik).
        Giriş: a'dan `lead` sn ÖNCE başlar ve a'da biter; çıkış: b'den `rel` sn'de geri açılır."""
        ta, tb = self.t_of(a_sec), self.t_of(b_sec)
        floor = 0.0 if floor_db is None else float(D.db2lin(floor_db))
        self.gates.append((ta - lead, ta, tb, tb + rel, floor))

    def gate_env(self):
        """Tüm kapıların birleşik kazanç zarfı (n,) — reverb SONRASI uygulanır."""
        env = np.ones(self.n, dtype=np.float32)
        for (t_s, ta, tb, t_e, floor) in self.gates:
            i0, i1, i2, i3 = [int(round(x * SR)) for x in (t_s, ta, tb, t_e)]
            i0c, i1c, i2c, i3c = [int(np.clip(x, 0, self.n)) for x in (i0, i1, i2, i3)]
            g = np.ones(self.n, dtype=np.float32)
            if i1 > i0:
                u = (np.arange(i0c, i1c) - i0) / (i1 - i0)
                g[i0c:i1c] = floor + (1 - floor) * (0.5 + 0.5 * np.cos(np.pi * u))
            g[i1c:i2c] = floor
            if i3 > i2:
                u = (np.arange(i2c, i3c) - i2) / (i3 - i2)
                g[i2c:i3c] = floor + (1 - floor) * (0.5 - 0.5 * np.cos(np.pi * u))
            env = np.minimum(env, g)
        return env


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
            "tick": [0, 4, 0, 4, 0, 4, 0, 4],
            "florin": [0, 1, 2, 3, None, 2, None, None],           # yükselen parlak figür (sikke cıngırtısı)
            "ledger": [0, None, 4, None, 0, 4, None, None],         # defter: iki sütun, kuru tık-tık
            "recit": [0, None, None, None, 2, None, None, None],    # recitativo yatağı (nadir akor sesi)
            "hush": [0, None, None, None, None, None, None, None]},
    "6/8": {"lilt": [0, 1, 2, 1, 2, 1], "gigue": [0, None, 2, 1, None, 2], "roll": [0, 1, 2, 3, 2, 1],
            "sparse": [0, None, None, 2, None, 1], "sea": [0, 1, 2, 3, 4, 3],
            "florin": [0, 1, 2, 3, None, 1], "palle": [0, 2, 1, 2, 1, 2],
            "hush": [0, None, None, None, None, None]},
    "3/4": {"waltz": [0, None, 1, 2, 1, 2], "sarab": [0, None, None, 2, None, 1], "roll": [0, 1, 2, 3, 2, 1],
            "sparse": [0, None, 1, None, 2, None], "lull": [0, 2, 1, 3, 1, 2],
            "florin": [0, 1, 2, 3, None, None], "pavane": [0, None, 2, None, 1, None],
            "hush": [0, None, None, None, None, None]},
}
ACC = {"4/4": [1.0, .55, .78, .55, .92, .55, .75, .55], "6/8": [1.0, .5, .62, .92, .5, .62], "3/4": [1.0, .5, .78, .5, .78, .5]}

BASS = {
    "4/4": {"root13": [(0, "r"), (4, "f")], "drive": [(0, "r"), (1, "r"), (2, "o"), (3, "r"), (4, "f"), (5, "r"), (6, "o"), (7, "r")],
            "p332": [(0, "r"), (3, "r"), (6, "r")], "whole": [(0, "r")], "walk": [(0, "r"), (2, "f"), (4, "r"), (6, "o")],
            "tick": [(0, "r"), (2, "r"), (4, "r"), (6, "r")], "pedal": [(0, "r"), (4, "r")]},
    "6/8": {"lilt": [(0, "r"), (3, "f")], "drive": [(0, "r"), (2, "r"), (3, "f"), (5, "r")], "whole": [(0, "r")]},
    "3/4": {"waltz": [(0, "r")], "sarab": [(0, "r"), (4, "f")], "whole": [(0, "r")]},
}

PERC = {
    "4/4": {"heartbeat": "D..d....", "proc": "D.......", "proc2": "D...T...", "march": "D.t.D.t.", "drive": "DtTtDtTt",
            "p332": "D..T..D.", "dun": "D..tD.T.", "duyek": "D.TtD.T.", "none": "........",
            "palle": "DtDtDt..",            # altılı ritim (altı vuruş + soluk): Medici arması
            "ceremony": "D...t.t."},
    "6/8": {"lilt": "D.T.t.", "gallop": "D.TD.T", "sea": "D..t..", "heart": "D.d...", "none": "......",
            "palle": "DtDtDt",              # 2+2+2 hemiola: altı eşit vuruş
            "oar": "D..D.."},
    "3/4": {"sarab": "D..T.t", "light": "D....t", "proc3": "D.....", "none": "......", "palle": "DtDtDt"},
}
TEF = {
    "4/4": {"eighths": "x.yyx.yy", "sparse": "..y...y.", "drive": "xyxyxyxy"},
    "6/8": {"lilt": "x.yx.y", "sparse": "..y..y"},
    "3/4": {"light": "..y.y.", "sarab": "x.y.y."},
}

# melodi tohumları: (derece farkı, vuruş-ızgarası uzunluğu [sekizlik]) — özgün figürler; layer_melody akor sesine göre kaydırır/çevirir
MOTIFS = {
    "bruksel": [(4, 4), (3, 2), (2, 2), (0, 8)],
    "merak": [(0, 1), (2, 1), (1, 1), (4, 3)],
    "sorgu": [(0, 2), (2, 2), (4, 2), (3, 2)],
    "agit": [(4, 3), (3, 1), (2, 2), (1, 2), (0, 4)],
    "yuruyus": [(0, 2), (0, 1), (2, 1), (1, 2), (0, 2)],
    # --- Medici
    "florin": [(0, 1), (2, 1), (4, 1), (7, 5)],             # yükselen 4 nota: parlak, pizzicato
    "miras": [(4, 3), (4, 3), (2, 6)],                      # sakin, tekrar eden üç nota (iki aynı + düşen üçlü)
    "lorenzo": [(2, 2), (4, 2), (5, 3), (4, 1)],            # Lorenzo temasının ilk ölçüsü
    "defter": [(0, 1), (4, 1), (0, 1), (4, 1), (2, 4)],     # defter satırı: tık-tık-tık
    "dolasim": [(0, 3), (1, 1), (2, 2), (1, 2)],            # sakin, dolanan
}

# açık (ızgaraya serbest) tema satırları — layer_theme; (derece, süre[adım]); derece ana sese göre, 7 = üst oktav, negatif = aşağı
THEMES = {
    "florin": [(0, 1), (2, 1), (4, 1), (7, 5)],
    "florin3": [(2, 1), (4, 1), (7, 4)],
    "florin_uzun": [(0, 2), (2, 2), (4, 2), (7, 8)],
    "miras": [(4, 3), (4, 3), (2, 10)],                     # düşen üçlü ile kapanan hücre (c0, c12, c15; c16'da invert=True ile TERS)
    "bedel": [(0, 16)],                                     # tek uzun nota; alçak, çekilen yay (gamba) — BEDEL perdesinin imzası
    "lorenzo": [(2, 2), (4, 2), (5, 3), (4, 1),             # 4 ölçülük tema (4/4, 32 adım): yay biçimi, tonikte kapanır
                (2, 2), (1, 2), (2, 4),
                (4, 2), (5, 2), (7, 3), (6, 1),
                (4, 3), (2, 1), (1, 2), (0, 2)],
    "duomo": [(0, 4), (2, 4), (4, 4), (7, 8), (5, 4), (4, 4), (0, 8)],   # kubbe: yükselen yay, inen yay
    "donus": [(0, 2), (4, 2), (7, 2), (9, 6)],              # 1434 dönüşü: beşli sıçrama, oktav, dokuzlu
    "yildiz": [(7, 2), (9, 2), (11, 2), (14, 6)],           # Jüpiter'in dört uydusu
}
THEMES["donus_ters"] = list(reversed(THEMES["donus"]))      # 1494: aynı figür geri sarılmış (c10)


# ═══════════════════════════ katman üreticileri ═══════════════════════════
def layer_drone(c, cfg):
    mode = cfg.get("mode", "pedal")
    chunk = cfg.get("chunk_bars", 4) * c.bar
    body = cfg.get("body", "gamba")
    t = 0.0
    while t < c.T - 0.3:
        L = min(chunk, c.T - t)
        tm = t + L / 2
        g = cfg["lvl"] * (0.5 + 0.5 * c.I(tm))
        if "win" in cfg:
            g *= 1.0 if any(w0 <= c.u(tm) < w1 for (w0, w1) in cfg["win"]) else 0.0
        if g <= 0.01:
            t += L
            continue
        if mode == "pedal":
            root = c.tonic
        else:
            root = deg_midi(c.tonic, c.mode, c.chord_at(t + 0.1)[2])
            while root > c.tonic + 9:
                root -= 12
            while root < c.tonic - 5:
                root += 12
        while body == "gamba" and root < 38:     # bas viyol en alt teli D2
            root += 12
        notes = [(root, 1.0, -0.12)]
        if cfg.get("fifth", True):
            notes.append((root + 7, 0.62, 0.14))
        for (m, gm, pan) in notes:
            y = bowed_note(_hz(m), L + 3.0, 0.7, c.rng, attack=cfg.get("attack", 1.6), release=2.2, bright=cfg.get("bright", 0.6), body=body)
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
                y, lay = bowed_note(f, max(d * c.step * 1.1, 0.8) + 0.8, vel, c.rng, attack=0.18, release=0.5, ens=2, bright=0.8, body=cfg.get("body", "cello")), "drone"
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
                y = bowed_note(_hz(m), c.step * 1.5 + 0.4, vel, c.rng, attack=0.04, release=0.25, ens=1, bright=0.9, body=cfg.get("body", "cello"))
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
    """Müzikal çan/çıngırak tınısı (parıltı). OLAY ÇANI DEĞİLDİR; c7 ve c10 cue'larında kullanılmaz."""
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


# ═══════════════════════════ tema / olay / recitativo katmanları ═══════════════════════════
_REG_CENTER = dict(lute=64, harp=72, organ=60, gamba=40, choir=60, bell=84)


def _snap(c, t, on=True):
    if not on:
        return t
    return round(t / c.step) * c.step


def _line_notes(c, it):
    """Tema satırı → (midi listesi, süre[adım] listesi). Seçenekler: retro (geri sar), invert (ilk notaya göre ters çevir), deg0 (derece kaydır),
    oct (oktav), center (kayıt merkezi MIDI). Hepsi mod derecesi cinsinden → her zaman diyatonik."""
    line = list(it["notes"] if it.get("notes") else THEMES[it["motif"]])
    if it.get("retro"):
        line = line[::-1]
    degs = [d for d, _ in line]
    durs = [x for _, x in line]
    if it.get("invert"):
        d0 = degs[0]
        degs = [2 * d0 - d for d in degs]
    degs = [d + it.get("deg0", 0) for d in degs]
    midis = [deg_midi(c.tonic, c.mode, d) for d in degs]
    inst = it.get("inst", "lute")
    ctr = it.get("center", _REG_CENTER.get(inst, 64))
    shift = 12 * int(round((ctr - float(np.mean(midis))) / 12.0)) + 12 * it.get("oct", 0)
    return [m + shift for m in midis], durs


def _play_note(c, inst, m, t, dur_s, vel, gain, pan, it=None):
    """Tek nota: lavta/klavsen/org/gamba/koro/çan; dur_s = nota süresi (sn)."""
    it = it or {}
    f = _hz(m)
    if inst == "lute":
        c.put("lute", lute_note(f, vel, c.rng, ring=it.get("ring", 1.0)), t, gain=gain, pan=pan)
    elif inst == "harp":
        c.put("harp", harpsichord_note(f, vel, c.rng), t, gain=gain, pan=pan)
    elif inst == "organ":
        y = organ_note(f, dur_s + 0.9, vel, c.rng, stops=it.get("stops", (("flute", 1.0, 1.0), ("principal", 0.3, 1.0))),
                       attack=it.get("attack", 0.10), release=it.get("release", 0.7), chiff=it.get("chiff", 0.3))
        c.put("organ", y, t, gain=gain, pan=pan)
    elif inst == "gamba":
        y = bowed_note(f, dur_s + 1.2, vel, c.rng, attack=it.get("attack", 0.5), release=it.get("release", 1.2), ens=2,
                       bright=it.get("bright", 0.6), body="gamba", bend=it.get("bend", 0.0))
        c.put("drone", y, t, gain=gain, pan=pan)
    elif inst == "choir":
        y = choir_note(f, dur_s + 1.5, vel, c.rng, vowel=it.get("vowel", "o"), vowel2=it.get("vowel2"), voices=it.get("nvox", 3),
                       attack=it.get("attack", 0.8), release=it.get("release", 1.5))
        c.put("choir", y, t, gain=gain, pan=pan)
    elif inst == "bell":
        c.put("bell", bell(f, dur_s + 2.0, vel, c.rng, ring=it.get("ring", 1.2), strike=0.4), t, gain=gain, pan=pan)
    else:
        raise ValueError(f"bilinmeyen çalgı: {inst}")


def layer_theme(c, items):
    """Açık tema girişleri: [dict(motif|notes, sec, inst, g, vel, deg0, oct, invert, retro, stretch, snap, rep, gap)]. Zamanlar bölüm saniyesi."""
    for it in items:
        inst = it.get("inst", "lute")
        midis, durs = _line_notes(c, it)
        t0 = _snap(c, c.t_of(it["sec"]), it.get("snap", True))
        stretch = it.get("stretch", 1.0)
        rep = int(it.get("rep", 1))
        span = sum(durs) * c.step * stretch
        for r in range(rep):
            pos = 0.0
            for k, (m, d) in enumerate(zip(midis, durs)):
                t = t0 + r * (span + it.get("gap", 0.0)) + pos
                dur_s = d * c.step * stretch
                vel = float(it.get("vel", 0.7)) * (1.0 if k else 1.08)
                pan = it.get("pan", float(np.clip(0.05 + (m - 62) / 70.0, -0.35, 0.45)))
                if inst in ("organ", "gamba", "choir", "bell") or it.get("hold"):
                    pass
                _play_note(c, inst, m, t + c.rng.normal(0, 0.004), dur_s, vel, it.get("g", 1.0), pan, it)
                if c.note_log is not None:
                    c.note_log.append(("theme:" + str(it.get("motif", "?")), round(t, 2), m, d))
                pos += dur_s
        c.events_log.append((c.t_of(it["sec"]), "theme:" + str(it.get("motif", "notes")), inst))


def _midi_list(c, ev):
    if "midi" in ev:
        return list(ev["midi"])
    return [deg_midi(c.tonic, c.mode, d) + 12 * ev.get("oct", 0) for d in ev["deg"]]


def layer_events(c, events):
    """Çıpalı olaylar. kind: timp | dum | tek | ka | seq | gong | sub | lute | harp | organ | choir | gamba | riser | tick | stop.
    Zaman: ev["sec"] (bölüm saniyesi; resolve_spec çıpadan hesaplar)."""
    for ev in events:
        k = ev["kind"]
        t = c.t_of(ev["sec"])
        g = ev.get("g", 1.0)
        rng = c.rng
        c.events_log.append((t, k))
        if k == "timp":
            c.put("perc", timp(ev.get("f", _hz(c.tonic - 12)), ev.get("vel", 0.8), rng, dur=ev.get("dur", 2.6)), t, gain=g, pan=ev.get("pan", 0.0))
        elif k in ("dum", "tek", "ka"):
            c.put("perc", drum(k, ev.get("f", ev.get("pitch", 92.0)), ev.get("vel", 0.8), rng), t, gain=g, pan=ev.get("pan", {"dum": 0.0, "tek": 0.3, "ka": -0.25}[k]))
        elif k == "seq":       # perküsyon dizisi: hits=[(dt, tür, vel)]
            for (dt, kind, vel) in ev["hits"]:
                if kind == "timp":
                    y = timp(ev.get("tf", _hz(c.tonic - 12)), vel, rng, dur=ev.get("dur", 2.0))
                else:
                    y = drum(kind, ev.get("f", 92.0) * rng.uniform(0.97, 1.03), vel, rng)
                c.put("perc", y, t + dt + rng.normal(0, 0.003), gain=g, pan=ev.get("pan", 0.0))
        elif k == "gong":
            c.put("fx", gong(ev.get("f", _hz(c.tonic + 12)), ev.get("dur", 8.0), ev.get("vel", 0.8), rng, bloom=ev.get("bloom", 1.0)), t, gain=g)
        elif k == "sub":
            c.put("fx", sub(ev.get("f0", 64), ev.get("f1", 30), ev.get("dur", 3.5), ev.get("vel", 0.8)), t, gain=g)
        elif k in ("lute", "harp"):
            ms = _midi_list(c, ev)
            sp = ev.get("strum", 0.03)
            for j, m in enumerate(ms):
                y = lute_note(_hz(m), ev.get("vel", 0.6), rng, ring=ev.get("ring", 1.0)) if k == "lute" else harpsichord_note(_hz(m), ev.get("vel", 0.6), rng)
                c.put(k, y, t + sp * j, gain=g, pan=ev.get("pan", -0.15 + 0.08 * j))
        elif k == "organ":
            ms = _midi_list(c, ev)
            for j, m in enumerate(ms):
                y = organ_note(_hz(m), ev.get("dur", 4.0), ev.get("vel", 0.6), rng, stops=ev.get("stops", (("flute", 1.0, 1.0), ("principal", 0.35, 1.0), ("flute", 0.25, 2.0))),
                               attack=ev.get("attack", 0.5), release=ev.get("release", 1.8), chiff=ev.get("chiff", 0.2), trem=True)
                c.put("organ", y, t + 0.03 * j, gain=g, pan=[-0.2, 0.2, -0.3, 0.3, 0.1, -0.1][j % 6])
        elif k == "choir":
            ms = _midi_list(c, ev)
            for j, m in enumerate(ms):
                y = choir_note(_hz(m), ev.get("dur", 5.0), ev.get("vel", 0.6), rng, vowel=ev.get("vowel", "o"), vowel2=ev.get("vowel2"), voices=ev.get("nvox", 3),
                               attack=ev.get("attack", 1.2), release=ev.get("release", 2.0))
                c.put("choir", y, t + 0.05 * j, gain=g, pan=[-0.3, 0.3, 0.0, -0.15, 0.15, 0.0][j % 6])
        elif k == "gamba":
            ms = _midi_list(c, ev)
            for j, m in enumerate(ms):
                y = bowed_note(_hz(m), ev.get("dur", 6.0), ev.get("vel", 0.7), rng, attack=ev.get("attack", 1.2), release=ev.get("release", 1.8), ens=2,
                               bright=ev.get("bright", 0.55), body="gamba", bend=ev.get("bend", 0.0))
                c.put("drone", y, t + 0.02 * j, gain=g, pan=ev.get("pan", -0.1 + 0.2 * j))
        elif k == "riser":
            y = _level(D.noise_riser(ev.get("dur", 5.0), ev.get("f0", 300), ev.get("f1", 5000), rng, curve=ev.get("curve", 1.4)), -26.0, "sustain")
            c.put("fx", y, t - ev.get("dur", 5.0) + ev.get("peak", 0.0), gain=g)
        elif k == "tick":
            c.put("harp", dry_tick(rng, ev.get("vel", 0.6)), t, gain=g, pan=ev.get("pan", 0.2))
        elif k == "stop":       # kuru durak (mizah): müzik kısa süre kesilir + kuru tık
            hold = ev.get("hold", 0.9)
            c.add_gate(ev["sec"], ev["sec"] + hold, lead=ev.get("lead", 0.04), rel=ev.get("rel", 0.30), floor_db=None)
            c.put("harp", dry_tick(rng, 0.55), t + 0.02, gain=g, pan=0.2)
        else:
            raise ValueError(f"bilinmeyen olay: {k}")


def layer_recit(c, cfg):
    """Recitativo-tarzı süreklilik (basso continuo + deklamasyon): ızgaraya KİLİTLİ DEĞİL, serbest ritim (rubato). Her 'cümle': alçak gamba/lavta
    bası + yayılmış lavta akoru + klavsen deklamasyonu (okuma sesi çevresinde kısa notalar, sonda inen kadans). Özgün; var olan hiçbir
    parçaya (Peri, Caccini...) gönderme yok. cfg: lvl, lo, hi, inst ('harp'|'lute'), tone (okuma derecesi), tempo (süre çarpanı), gap=(a,b) sn."""
    rng = c.rng
    t = c.t_open + 0.8
    end = c.T - c.close_sec
    tone = cfg.get("tone", 4)
    inst = cfg.get("inst", "harp")
    gap = cfg.get("gap", (1.2, 3.0))
    tempo = cfg.get("tempo", 1.0)
    lo_m, hi_m = cfg.get("reg", (62, 80))
    dlo, dhi = deg_for_midi(c, lo_m), deg_for_midi(c, hi_m)
    while t < end - 2.0:
        a = c.act(cfg, t)
        if a < 0.05:
            t += 1.0
            continue
        _, _, deg, ext = c.chord_at(t)
        root = deg_midi(c.tonic, c.mode, deg)
        while root > c.tonic + 9:
            root -= 12
        while root < c.tonic - 5:
            root += 12
        while root < 38:
            root += 12
        n = int(rng.integers(5, 10))
        durs = [float(rng.choice([0.14, 0.18, 0.24, 0.32, 0.46, 0.7], p=[0.2, 0.25, 0.22, 0.15, 0.12, 0.06])) * tempo for _ in range(n)]
        durs[-1] *= 2.2
        plen = sum(durs) + 0.4
        # bas: uzun, yumuşak (continuo)
        y = bowed_note(_hz(root), plen + 1.6, 0.55, rng, attack=0.35, release=1.2, ens=1, bright=0.5, body="gamba")
        c.put("drone", y, t, gain=a * cfg.get("bass_g", 0.8), pan=-0.1)
        # yayılmış akor
        vc = lute_voic(c, deg, ext, 45)
        for j, m in enumerate(vc[:4]):
            c.put("lute", lute_note(_hz(m), 0.5, rng), t + 0.03 + 0.05 * j, gain=a * cfg.get("chord_g", 0.8), pan=-0.2 + 0.1 * j)
        # deklamasyon
        cur = tone
        tt = t + 0.35
        tones = {deg_midi(c.tonic, c.mode, x) % 12 for x in chord_degs(deg, ext)}
        for i, d in enumerate(durs):
            if i == n - 1:      # kadans: akor sesine in
                cand = [x for x in range(dlo, dhi + 1) if deg_midi(c.tonic, c.mode, x) % 12 in tones and x <= cur]
                cur = max(cand) if cand else cur - 1
            elif i >= n - 3:
                cur = cur - 1
            else:
                cur = int(np.clip(tone + int(rng.choice([-1, 0, 0, 0, 1, 2], p=[0.15, 0.3, 0.2, 0.1, 0.15, 0.1])), dlo, dhi))
            cur = int(np.clip(cur, dlo, dhi))
            m = deg_midi(c.tonic, c.mode, cur)
            vel = float(np.clip((0.55 if i in (0, n - 1) else 0.42) * rng.uniform(0.85, 1.1), 0.2, 0.9))
            f = _hz(m)
            y = harpsichord_note(f, vel, rng) if inst == "harp" else lute_note(f, vel, rng)
            c.put("harp" if inst == "harp" else "lute", y, tt, gain=a, pan=float(np.clip((m - 66) / 40.0, -0.3, 0.45)))
            tt += d
        t += plen + float(rng.uniform(*gap))


# ═══════════════════════════ kavşak yatakları ═══════════════════════════
def _span_db(d, a, b):
    """diag (saniye başına enerji) → [a,b) sn aralığının ortalama gücü (dB); boşsa None."""
    a, b = max(int(a), 0), int(b)
    if b <= a:
        return None
    e = sum(arr[a:b].sum() for arr in d.values()) / (b - a) / SR
    return 10 * np.log10(e + 1e-18)


def junction_pads(c, level_db=-1.0, start=True, end=True):
    """Cue başında/sonunda (çapraz geçiş bölgesi) kökün açık beşlisinde (kök, beşli, oktav, beşli+8) org + koro yatağı:
    çapraz geçiş çukuru kapanır. Seviye = cue gövdesinin gücü ile KENARIN YEREL gücünün küçüğü (diag) + level_db:
    cue sönerek bitiyorsa (düşük yoğunluk) yatak gövde düzeyine zıplayıp kavşakta 8–9 dB'lik basamak yapmaz."""
    d = c.diag
    a, b = int(c.t_open + 2), int(c.t_close - 2)
    if b <= a + 3 or not d:
        return
    body_db = _span_db(d, a, b)
    root = c.tonic + 12 if c.tonic < 41 else c.tonic
    notes = [root, root + 7, root + 12, root + 19]
    unit_db = 10 * np.log10(len(notes) * 10 ** (REF["organ"] / 10) + 3 * 10 ** (REF["choir"] / 10))

    def gain_for(local_db):
        ref = body_db if local_db is None else min(body_db, local_db)
        return 10 ** ((ref + level_db - unit_db) / 20)

    # kenarın yerel gücü: açılışta çapraz geçişin hemen ardından 8 sn, kapanışta çapraz geçişten hemen önceki 8 sn
    loc_start = _span_db(d, c.t_open + 1.0, c.t_open + 9.0)
    loc_end = _span_db(d, c.t_close - 9.0, c.t_close - 1.0)

    def place(t0, dur, attack, release, gain):
        for k, m in enumerate(notes):
            y = organ_note(_hz(m), dur, 0.7, c.rng, stops=(("flute", 1.0, 1.0), ("principal", 0.30, 1.0), ("flute", 0.25, 2.0)),
                           attack=attack, release=release, trem=False, chiff=0.0)
            c.put("organ", y, t0, gain=gain, pan=[-0.15, 0.15, -0.25, 0.25][k])
        for k, m in enumerate(notes[:3]):
            y = choir_note(_hz(m), dur, 0.7, c.rng, vowel="o", voices=3, attack=attack, release=release)
            c.put("choir", y, t0, gain=gain, pan=[-0.3, 0.3, 0.0][k])

    if start:
        place(0.0, min(c.open_sec + 4.0, c.T), 1.5, 2.5, gain_for(loc_start))
    if end:
        t0 = c.t_close - 3.0
        place(t0, c.T - t0, 2.0, 1.0, gain_for(loc_end))


# ═══════════════════════════ özel sahneler: c0 başlık vuruşu ve parça kapanışları ═══════════════════════════
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
    """c0 (P1): gerilim yükselişi (ters gong + gürültü yükselişi + hızlanan timpani rulosu + koro kümesi), 0,24 sn nefes boşluğu,
    t_hit anında TEK vuruş (timpani + gong + alt-bas) ve altın tonlu D majör açılış (org + koro + gamba + çan parıltısı + lavta);
    ardından 'florin' figürü (D–F#–A–D', lavta) ilk kez duyulur."""
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
    # altın D majör (üçlü: Fa# — 'Picardy'): org + koro + gamba + çanlar + lavta
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
        y = bowed_note(_hz(m), cd, 0.9, rng, attack=0.3, release=3.2, bright=1.0, body="gamba")
        c.put("drone", y, t_hit, gain=g["bowed"] * gg, pan=0.0)
    for kk, (m, gg) in enumerate(((74, 1.0), (81, 0.7), (90, 0.5), (86, 0.45))):
        c.put("bell", bell(_hz(m), 7.5, 0.75, rng, ring=1.7, strike=0.4), t_hit + 0.10 + 0.16 * kk, gain=gg * g["bell"], pan=0.3 * (1 if kk % 2 else -1))
    for kk, m in enumerate((50, 57, 62, 66, 69, 74)):
        c.put("lute", lute_note(_hz(m), 0.8, rng, ring=1.3), t_hit + 0.03 + 0.045 * kk, gain=g["lute"], pan=-0.2 + 0.08 * kk)
    # florin: sikke figürünün ilk duyuluşu (D4–F#4–A4–D5), vuruş sönerken
    for kk, m in enumerate((62, 66, 69, 74)):
        c.put("lute", lute_note(_hz(m), 0.62, rng, ring=1.5), t_hit + 1.7 + 0.26 * kk, gain=g["lute"] * 1.1, pan=0.1 + 0.05 * kk)
    c.put("bell", bell(_hz(86), 6.0, 0.6, rng, ring=1.6, strike=0.3), t_hit + 2.8, gain=0.35 * g["bell"], pan=0.2)


def finale_end(c, t_final, kind, G=None):
    """Parça kapanışları (7 sn'lik 'SIRADAKİ PARÇA' / 'TÜM FİLM' ekranı süresince çözülme). Spec'te bölüm/kesit düzeyinde end_kind=… ile seçilir
    (yoksa 'dissolve'); yalnız PARÇANIN SON kesitinde çalışır.
    dissolve : bölümün kendi tonikinde açık beşli + gamba drone + tek hafif lavta notası; sade çözülme (P1…P6 varsayılanı)
    p1  : altın majör → minöre soğuyan akor ('gölge') + alçak 'bedel' yayı; açık uç (D tonikli bölümler için; şu an hiçbir bölümde seçili değil)
    p2  : çözülmeyen sus4 akoru; çok hafif 'miras' hücresi (sonraki parçanın habercisi); açık uç (c11 → P5 sonu)
    p3  : D majör çözülüş (Picardy), ters çevrilmiş 'miras' hücresi (yükselen üçlü), son lavta notası ve sessizlik (c16 → P7 sonu, film sonu)"""
    g = dict(organ=0.55, choir=0.6, bowed=0.8, lute=0.8, bell=0.5)
    g.update(G or {})
    rng = c.rng
    cd = c.T - t_final + 0.5
    pans = [-0.2, 0.2, -0.3, 0.3, 0.1, -0.1]
    st_o = (("flute", 1.0, 1.0), ("principal", 0.35, 1.0), ("flute", 0.3, 2.0))
    if kind == "p1":
        for kk, m in enumerate((50, 57, 62, 66, 69)):               # D majör (altın) — 2,6 sn
            c.put("organ", organ_note(_hz(m), 3.4, 0.7, rng, stops=st_o, attack=0.5, release=1.6), t_final + 0.04 * kk, gain=g["organ"], pan=pans[kk])
        for kk, m in enumerate((50, 57, 62, 66)):
            c.put("choir", choir_note(_hz(m), 3.4, 0.75, rng, vowel="o", vowel2="a", morph=(0.15, 0.6), voices=3, attack=0.8, release=1.6), t_final + 0.06 * kk, gain=g["choir"], pan=pans[kk])
        t2 = t_final + 2.4                                          # D minör: üçlü 'soğur'
        for kk, m in enumerate((50, 57, 62, 65, 69)):
            c.put("organ", organ_note(_hz(m), cd - 2.4, 0.6, rng, stops=st_o, attack=1.6, release=4.0), t2 + 0.05 * kk, gain=g["organ"] * 0.9, pan=pans[kk])
        for kk, m in enumerate((50, 57, 62, 65)):
            c.put("choir", choir_note(_hz(m), cd - 2.4, 0.6, rng, vowel="o", voices=3, attack=1.8, release=4.0), t2 + 0.07 * kk, gain=g["choir"] * 0.9, pan=pans[kk])
        c.put("drone", bowed_note(_hz(38), cd - 2.0, 0.8, rng, attack=2.0, release=4.0, bright=0.5, body="gamba", bend=-35), t_final + 2.0, gain=g["bowed"])
        c.put("lute", lute_note(_hz(57), 0.5, rng, ring=1.8), t_final + 3.8, gain=g["lute"], pan=0.1)
    elif kind == "p2":
        for kk, m in enumerate((50, 57, 62, 67)):                   # D sus4: çözülmez
            c.put("organ", organ_note(_hz(m), cd, 0.6, rng, stops=st_o, attack=1.2, release=4.5), t_final + 0.05 * kk, gain=g["organ"], pan=pans[kk])
        for kk, m in enumerate((50, 57, 62, 67)):
            c.put("choir", choir_note(_hz(m), cd, 0.6, rng, vowel="o", voices=3, attack=1.6, release=4.5), t_final + 0.07 * kk, gain=g["choir"] * 0.9, pan=pans[kk])
        c.put("drone", bowed_note(_hz(38), cd, 0.8, rng, attack=1.4, release=4.0, bright=0.5, body="gamba", bend=-45), t_final, gain=g["bowed"])
        for kk, (dt, m) in enumerate(((1.2, 69), (2.3, 69), (3.6, 65))):      # miras hücresi (A–A–F): P3'ün habercisi
            c.put("lute", lute_note(_hz(m), 0.42, rng, ring=1.8), t_final + dt, gain=g["lute"] * 0.9, pan=0.15)
    elif kind == "p3":
        for kk, m in enumerate((50, 57, 62, 66, 69, 74)):           # D majör çözülüş
            c.put("organ", organ_note(_hz(m), cd, 0.7, rng, stops=st_o, attack=1.2, release=4.0), t_final + 0.05 * kk, gain=g["organ"], pan=pans[kk])
        for kk, m in enumerate((50, 57, 62, 66, 69, 74)):
            c.put("choir", choir_note(_hz(m), cd, 0.75, rng, vowel="o", vowel2="a", morph=(0.15, 0.6), voices=3, attack=1.8, release=4.0), t_final + 0.08 * kk, gain=g["choir"], pan=pans[kk])
        c.put("drone", bowed_note(_hz(38), cd, 0.8, rng, attack=1.2, release=4.0, bright=0.7, body="gamba"), t_final, gain=g["bowed"])
        # ters çevrilmiş miras hücresi: A–A–C# (yükselen), sonra son lavta D
        for dt, m, v in ((0.5, 69, 0.55), (1.7, 69, 0.5), (2.9, 73, 0.55), (4.6, 62, 0.5)):
            c.put("lute", lute_note(_hz(m), v, rng, ring=1.8), t_final + dt, gain=g["lute"], pan=0.12)
        c.put("bell", bell(_hz(86), 6.5, 0.6, rng, ring=1.5, strike=0.35), t_final + 3.4, gain=g["bell"] * 0.6, pan=0.2)
    else:   # "dissolve": açık beşliyle sade çözülme (üçlüsüz: sonraki parçanın tonuyla çatışmaz) + tek hafif lavta notası
        for kk, m in enumerate((c.tonic + 12, c.tonic + 19, c.tonic + 24)):
            c.put("organ", organ_note(_hz(m), cd, 0.6, rng, stops=st_o, attack=1.0, release=4.0), t_final + 0.05 * kk, gain=g["organ"], pan=pans[kk])
        c.put("drone", bowed_note(_hz(max(c.tonic, 38)), cd, 0.7, rng, attack=1.2, release=4.0, bright=0.5, body="gamba"), t_final, gain=g["bowed"])
        if cd > 5.0:
            c.put("lute", lute_note(_hz(c.tonic + 19), 0.42, rng, ring=1.8), t_final + 2.8, gain=g["lute"] * 0.8, pan=0.12)


FINALES = {"c0": finale_c0}


# ═══════════════════════════ cue geometrisi ve çalma ═══════════════════════════
DEFAULT_XF = 5.0
XFADE = {   # (önceki bölüm, sonraki bölüm): çapraz geçiş süresi (sn); merkez = bölüm kartı boşluğunun ortası. Yalnız AYNI parçadaki komşu bölümler kullanılır
    ("c0", "c1"): 6.0, ("c1", "c2"): 5.0, ("c2", "c3"): 5.0, ("c3", "c4"): 6.0, ("c4", "c5"): 5.0, ("c5", "c6"): 5.0,
    ("c6", "c7"): 5.0, ("c7", "c8"): 5.0, ("c8", "c9"): 6.0, ("c9", "c10"): 5.0, ("c10", "c11"): 6.0,
    ("c12", "c13"): 6.0, ("c13", "c14"): 5.0, ("c14", "c15"): 6.0, ("c15", "c16"): 7.0,
}
TITLE_DELAY = 0.4        # P1 ana başlık vuruşu: c0 t1 + 0,4 sn
TARGET_RMS_DB = -27.5    # ducking ÖNCESİ müzik bandının ortalama RMS hedefi (dBFS)
FINAL_FADE = 3.4         # parça sonunda son çıkış sönümü (sn)


def plan_segments(chapters, total, tail, sent):
    """Bölüm listesi → kesit (segment) planı. Her kesit: id, ch, spec (ham), start/end (parça ses ekseni), s0/s1 (kesitin ad. aralığı: arc/çıpa u'sunun
    tabanı), xin/xout (çapraz geçişler), first/final. Çapraz geçiş merkezi: bölüm kartı boşluğunun ortası (c0→c1: başlık vuruşunun 3 sn sonrası);
    kesit sınırı merkezi: kesit 'until' çıpası."""
    n = len(chapters)
    J = []
    for i in range(n - 1):
        a, b = chapters[i], chapters[i + 1]
        if a["id"] == "c0" and b["id"] == "c1":
            J.append(a["t1"] + TITLE_DELAY + 3.0)
        else:
            J.append(a["t1"] + a.get("gap_after", 3.0) / 2)
    segs = []
    for i, ch in enumerate(chapters):
        cid = ch["id"]
        xin = XFADE.get((chapters[i - 1]["id"], cid), DEFAULT_XF) if i > 0 else 0.0
        xout = XFADE.get((cid, chapters[i + 1]["id"]), DEFAULT_XF) if i < n - 1 else 0.0
        c_start = (J[i - 1] - xin / 2) if i > 0 else 0.0
        c_end = (J[i] + xout / 2) if i < n - 1 else total + tail
        spec = CUES[cid]
        secs = spec.get("sections")
        if not secs:
            segs.append(dict(id=cid, ch=cid, k=0, nsec=1, spec=spec, start=c_start, end=c_end, s0=ch["t0"], s1=ch["t1"], ch0=ch["t0"], ch1=ch["t1"], xin=xin, xout=xout,
                             first=(i == 0), final=(i == n - 1)))
            continue
        base = {k: v for k, v in spec.items() if k != "sections"}
        bounds, xfs = [ch["t0"]], []
        for sc in secs[:-1]:
            anc, du = sc["until"]
            tb = D.anchor_time(anc, sent)
            if tb is None:
                tb = ch["t0"] + du * (ch["t1"] - ch["t0"])
            bounds.append(float(tb))
            xfs.append(float(sc.get("xf", 4.0)))
        bounds.append(ch["t1"])
        for k, sc in enumerate(secs):
            sp = {**base, **{kk: vv for kk, vv in sc.items() if kk not in ("until", "xf")}}
            s0, s1 = bounds[k], bounds[k + 1]
            xin_k = xin if k == 0 else xfs[k - 1]
            xout_k = xout if k == len(secs) - 1 else xfs[k]
            st = c_start if k == 0 else (s0 - xin_k / 2)
            en = c_end if k == len(secs) - 1 else (s1 + xout_k / 2)
            segs.append(dict(id=f"{cid}.{k + 1}", ch=cid, k=k, nsec=len(secs), spec=sp, start=st, end=en, s0=s0, s1=s1, ch0=ch["t0"], ch1=ch["t1"], xin=xin_k, xout=xout_k,
                             first=(i == 0 and k == 0), final=(i == n - 1 and k == len(secs) - 1)))
    return segs


def first_tonic(cid):
    """Bölümün ilk kesitinin tonik MIDI'si (bölüm kartı vurgusu bu sese akortlanır)."""
    sp = CUES[cid]
    secs = sp.get("sections")
    return int(secs[0].get("tonic", sp["tonic"]) if secs else sp["tonic"])


def gate_windows(chapters, total, tail, timeline):
    """Render ETMEDEN müzik sessizlik kapılarını (parça ses ekseninde) döndürür: [dict(seg, a, b, lead, rel, floor_db, note)]."""
    sent = D.sent_index(timeline)
    out = []
    for sg in plan_segments(chapters, total, tail, sent):
        sp = resolve_spec(sg["spec"], sg, sent)
        for (a, b, lead, rel, floor_db, note) in sp.get("_gates", []):
            out.append(dict(seg=sg["id"], a=round(sg["s0"] + a, 3), b=round(sg["s0"] + b, 3), lead=lead, rel=rel, floor_db=floor_db, note=note))
    return out


def _anchor_t(anchor, sent, seg):
    """Çıpa → parça ekseninde saniye. timeline'da cümle yoksa (ör. c6: ses henüz yok) DEFAULT_U tablosundan kestirir."""
    t = D.anchor_time(anchor, sent)
    if t is not None:
        return float(t)
    a = (anchor, 0.0) if isinstance(anchor, str) else anchor
    a = list(a)
    du = DEFAULT_U.get(a[0])
    if du is None:
        return None
    c0, c1 = seg["ch0"], seg["ch1"]
    if len(a) <= 2:
        return c0 + du[0] * (c1 - c0) + (float(a[1]) if len(a) == 2 else 0.0)
    base = du[1] if (isinstance(a[1], str) and a[1] in ("end", "son", "t1")) else du[0]
    return c0 + base * (c1 - c0) + float(a[-1])


def _anchor_u(anchor, default_u, seg, sent, dt=0.0):
    t = _anchor_t(anchor, sent, seg)
    if t is None:
        return float(default_u if default_u is not None else 0.5)
    s0, s1 = seg["s0"], seg["s1"]
    return float(np.clip((t + dt - s0) / max(s1 - s0, 1e-6), 0.005, 0.995))


def _sec_of(at, u, seg, sent, dt=0.0):
    t = _anchor_t(at, sent, seg) if at is not None else None
    if t is None:
        t = seg["s0"] + float(u if u is not None else 0.0) * (seg["s1"] - seg["s0"])
    return float(t - seg["s0"] + dt)


def resolve_spec(spec, seg, sent):
    """Ham spec -> cozulmus spec (derin kopya): arc noktalari (capa, varsayilan_u, yogunluk[, dt]) -> (u, yogunluk); katman pencereleri win=[(a,b)];
    events/theme: at (capa) + u (varsayilan) -> sec (kesit basindan saniye); gates -> '_gates' (a_sec, b_sec, lead, rel, floor_db, not).
    Capa bulunamazsa DEFAULT_U/varsayilan u kullanilir -> ses yamalarinda/kismi parcada kirilmaz."""
    import copy
    sp = copy.deepcopy(spec)
    arc = []
    for a in sp["arc"]:
        if isinstance(a[0], (str, tuple, list)):
            dt = a[3] if len(a) > 3 else 0.0
            arc.append((_anchor_u(a[0], a[1], seg, sent, dt), float(a[2])))
        else:
            arc.append((float(a[0]), float(a[1])))
    arc.sort(key=lambda p: p[0])
    for i in range(1, len(arc)):
        if arc[i][0] <= arc[i - 1][0]:
            arc[i] = (arc[i - 1][0] + 1e-3, arc[i][1])
    sp["arc"] = arc
    for k, v in list(sp.items()):
        if isinstance(v, dict) and v.get("win"):
            v["win"] = [tuple(_anchor_u(x[0], x[1], seg, sent) if isinstance(x, (tuple, list)) else float(x) for x in w) for w in v["win"]]
    for key in ("events", "theme"):
        out = []
        for ev in sp.get(key, []) or []:
            ev = dict(ev)
            ev["sec"] = _sec_of(ev.pop("at", None), ev.pop("u", None), seg, sent, ev.pop("dt", 0.0))
            out.append(ev)
        sp[key] = out
    gates = []
    for gt in sp.get("gates", []) or []:
        a = _sec_of(gt["a"], gt.get("ua"), seg, sent, gt.get("adt", 0.0))
        b = _sec_of(gt["b"], gt.get("ub"), seg, sent, gt.get("bdt", 0.0))
        rel = float(gt.get("rel", 3.0))
        if gt.get("floor_db") is not None:
            # 'kısık' kapı (tam sessizlik değil): müzik geri gelirken sıçramasın — açılma hızı en çok ~3,5 dB/sn (en çok 8 sn)
            rel = max(rel, min(8.0, abs(float(gt["floor_db"])) / 3.5))
        gates.append((a, max(b, a + 0.2), float(gt.get("lead", 0.6)), rel, gt.get("floor_db"), gt.get("note", "")))
    sp["_gates"] = gates
    return sp


def build_cue(seg, tail, seed=0):
    """Bir kesitin tüm katmanlarını (reverb öncesi) üretir → Cue nesnesi (dry + send tamponları + kapılar). seg['spec'] ÇÖZÜLMÜŞ olmalı."""
    spec = seg["spec"]
    T = seg["end"] - seg["start"]
    xin, xout = seg["xin"], seg["xout"]
    open_sec = xin + 1.0 if xin > 0 else 3.0
    close_sec = xout + 1.0 if xout > 0 else (tail + 0.75 if seg["final"] else 4.0)
    c = Cue(seg["id"], spec, T, seg["s0"] - seg["start"], seg["s1"] - seg["start"], open_sec, close_sec, seed=seed)
    for key, fn in (("drone", layer_drone), ("choir", layer_pad), ("arp", layer_arp), ("arp2", layer_arp), ("bass", layer_bass),
                    ("melody", layer_melody), ("perc", layer_perc), ("bell", layer_bell)):
        if spec.get(key):
            fn(c, spec[key])
    if spec.get("recit"):
        layer_recit(c, spec["recit"])
    if spec.get("theme"):
        layer_theme(c, spec["theme"])
    if spec.get("events"):
        layer_events(c, spec["events"])
    for (a, b, lead, rel, floor_db, _note) in spec.get("_gates", []):
        c.add_gate(a, b, lead=lead, rel=rel, floor_db=floor_db)
    fin = spec.get("finale")                              # "c0": P1 ana başlık vuruşu (c0 t1 + 0,4 sn)
    if fin is None and seg["final"]:                      # parçanın son kesiti: 7 sn'lik 'SIRADAKİ PARÇA' / 'TÜM FİLM' süresince çözülme
        fin = spec.get("end_kind", "dissolve")
    junction_pads(c, spec.get("pad_db", -1.0), start=xin > 0, end=(xout > 0 and fin != "c0"))
    if fin == "c0":
        FINALES["c0"](c, c.t1c + TITLE_DELAY, spec.get("finale_gain"))
    elif fin in ("p1", "p2", "p3", "dissolve"):
        finale_end(c, c.t1c + 0.25, fin, spec.get("finale_gain"))
    return c


def finish_cue(c, final=False):
    """Reverb (algoritmik IR + fftconvolve) + kapı zarfı (reverb SONRASI: kuyruklar da susar) + cue ana süzgeci → float32 (n,2)."""
    ir = D.hall_ir(2.2)
    wet = D.reverb_wet(c.send, ir)[:c.n]
    out = c.dry + wet * 1.0
    if c.gates:
        out = out * c.gate_env()[:, None]
    out = D.sosfilt(_sos([("hp", 28, 0, 0.7), ("highshelf", 6500, -2.5, 0.7)]), out, axis=0).astype(np.float32)
    if final:
        out = D.fade_edges(out, 0.0, FINAL_FADE).astype(np.float32)
    return out


def _render_job(job):
    """Çok işlemli çalıştırma için üst düzey fonksiyon: tek kesit üretir (float32 (n,2), reverb dahil, seviyesiz)."""
    c = build_cue(job["seg"], job["tail"], job["seed"])
    return job["seg"]["id"], finish_cue(c, final=job["seg"]["final"])


def _robust_rms_db(x, sr=SR, mask=None):
    """1 sn'lik pencerelerin güç ortalaması; sessiz pencereler atılır, en yüksek %8 pencere kırpılır (vuruş/doruklar
    seviyeyi domine etmesin). mask: (nwin,) bool — False olan pencereler (kapılı bölgeler) hesaba katılmaz."""
    m = x.mean(axis=1) if x.ndim == 2 else x
    w = sr
    nwin = len(m) // w
    if nwin < 2:
        return D.rms_db(m)
    p = np.mean(m[:nwin * w].reshape(nwin, w) ** 2, axis=1)
    keep_m = p > 1e-9
    if mask is not None:
        keep_m &= mask[:nwin]
    p = p[keep_m]
    if len(p) < 2:
        return D.rms_db(m)
    p = np.sort(p)
    keep = p[: max(1, int(len(p) * 0.92))]
    return float(10 * np.log10(np.mean(keep) + 1e-18))


def _code_hash():
    """Önbellek anahtarının kod payı: SENTEZ kodu (muzik.py'nin 'POST-SENTEZ' işaretine kadar olan kısmı + ses_dsp.py). Kavşak düzeltmesi, birleştirme, CLI ve
    CUES/DEFAULT_U tabloları hariçtir: cue tanımı değişince yalnız o kesit (çözülmüş spec anahtarda) yeniden üretilir, birleştirme koduna dokunmak her şeyi silmez."""
    h = hashlib.md5()
    src = open(os.path.join(HERE, "muzik.py"), "rb").read()
    h.update(src[:src.index(b"# @@POST" b"-SENTEZ@@")])
    h.update(open(os.path.join(HERE, "ses_dsp.py"), "rb").read())
    return h.hexdigest()[:12]


def _window_mask(core0_s, n_win, gates_cue, pad=0.6):
    """Çekirdek bölgedeki 1 sn'lik pencereler için: kapılı (sessiz/kısık) bölgelerle çakışmayanlar True. gates_cue: (a, b, lead, rel) — cue süresi ekseni."""
    m = np.ones(n_win, dtype=bool)
    for (a, b, lead, rel) in gates_cue:
        i0 = int(np.floor(a - lead - pad - core0_s))
        i1 = int(np.ceil(b + rel + pad - core0_s))
        m[max(i0, 0):max(min(i1 + 1, n_win), 0)] = False
    return m


# @@POST-SENTEZ@@ — bu işaretten sonrası (kavşak düzeltmesi, birleştirme, CLI, DEFAULT_U, CUES) önbellek anahtarına girmez
TRIM_MAX_DB = 3.0        # kavşak düzey eşlemesinde bir kesit ucuna uygulanabilecek en çok düzeltme (dB)
TRIM_TOL_DB = 1.0        # kesit sonu ↔ sonraki kesit başı düzey farkı bunun altındaysa dokunulmaz
TRIM_RAMP = 10.0         # düzeltmenin gövdede sıfıra döndüğü yumuşak geçiş süresi (sn)
TRIM_WIN = 6.0           # kavşağa komşu ölçüm penceresi (sn): çapraz geçişin hemen dışındaki 6 sn


def _edge_level_db(x, a_s, b_s, gates=(), pad=0.6):
    """x (n,2) içinde [a_s, b_s) sn aralığındaki 1 sn'lik pencere güçlerinin ORTANCASI (dB). Kapılı (sessiz/kısık) bölgelerle çakışan ve
    sessiz (< −80 dB) pencereler atılır; 3'ten az pencere kalırsa None (düzeltme yapılmaz). gates: (a, b, lead, rel) — cue süresi ekseni."""
    i0, i1 = max(int(a_s), 0), int(b_s)
    if i1 - i0 < 3:
        return None
    m = x.mean(axis=1) if x.ndim == 2 else x
    ps = []
    for k in range(i0, i1):
        if (k + 1) * SR > len(m):
            break
        if any(k + 1 > ga - gl - pad and k < gb + gr + pad for (ga, gb, gl, gr) in gates):
            continue
        p = float(np.mean(m[k * SR:(k + 1) * SR].astype(np.float64) ** 2))
        if p > 1e-8:
            ps.append(p)
    if len(ps) < 3:
        return None
    return float(10 * np.log10(np.median(ps) + 1e-18))


def _junction_trims(plan, xs):
    """Kavşak düzey eşlemesi: ardışık iki kesit (çapraz geçiş merkezi) için önceki kesit sonunun ve sonraki kesit başının (çapraz geçiş bölgesinin hemen
    dışındaki 9 sn) ortanca düzeyini (kapılı bölgeler hariç) karşılaştırır; fark > TRIM_TOL_DB ise iki ucu birbirine doğru çeker (her uca en çok ±TRIM_MAX_DB).
    Döner: {kesit_id: (baş_dB, son_dB)}. Çıpalara bağlı olduğundan ses yamalanınca otomatik yeniden hesaplanır (kesit önbelleği bozulmaz)."""
    trims = {}
    ordered = sorted([g for g in plan if g["id"] in xs], key=lambda g: g["start"])
    for p, q in zip(ordered[:-1], ordered[1:]):
        if p["xout"] <= 0 or q["xin"] <= 0 or abs(p["xout"] - q["xin"]) > 0.05:
            continue
        xp, xq = xs[p["id"]], xs[q["id"]]
        gp = [(a + (p["s0"] - p["start"]), b + (p["s0"] - p["start"]), l, r) for (a, b, l, r, f, n) in p["spec"].get("_gates", [])]
        gq = [(a + (q["s0"] - q["start"]), b + (q["s0"] - q["start"]), l, r) for (a, b, l, r, f, n) in q["spec"].get("_gates", [])]
        Tp = len(xp) / SR
        lp = _edge_level_db(xp, Tp - p["xout"] - 1.0 - TRIM_WIN, Tp - p["xout"] - 1.0, gp)
        lq = _edge_level_db(xq, q["xin"] + 1.0, q["xin"] + 1.0 + TRIM_WIN, gq)
        if lp is None or lq is None:
            continue
        d = lq - lp
        if abs(d) <= TRIM_TOL_DB:
            continue
        half = float(np.clip(d / 2.0, -TRIM_MAX_DB, TRIM_MAX_DB))
        tp, hq = trims.get(p["id"], (0.0, 0.0)), trims.get(q["id"], (0.0, 0.0))
        trims[p["id"]] = (tp[0], +half)          # önceki kesit sonu sonrakine doğru
        trims[q["id"]] = (-half, hq[1])          # sonraki kesit başı öncekine doğru
    return trims


def _trim_curve(n, xin, xout, head_db, tail_db):
    """Kesit boyunca doğrusal kazanç eğrisi (n,): baş ucunda head_db (çapraz geçiş + 1 sn boyunca sabit) → TRIM_RAMP sn'de 0 dB; son ucunda 0 dB → tail_db
    (çapraz geçiş bölgesinden önce biter, sonuna dek sabit). Yarım kosinüs geçişler; kısa kesitte geçiş süresi küçülür."""
    db = np.zeros(n, dtype=np.float64)
    hb = int((xin + 1.0) * SR) if xin > 0 else 0
    tb = n - int((xout + 1.0) * SR) if xout > 0 else n
    room = max(tb - hb, 0)
    ramp = int(min(TRIM_RAMP * SR, room / 2))
    if abs(head_db) > 1e-6 and hb > 0:
        db[:hb] += head_db
        if ramp > 0:
            db[hb:hb + ramp] += head_db * 0.5 * (1 + np.cos(np.linspace(0, np.pi, ramp)))
    if abs(tail_db) > 1e-6 and tb < n:
        db[tb:] += tail_db
        if ramp > 0:
            db[tb - ramp:tb] += tail_db * 0.5 * (1 - np.cos(np.linspace(0, np.pi, ramp)))
    return (10 ** (db / 20.0)).astype(np.float32)


def _spec_anchors(spec):
    """Bir cue/kesit spec'indeki tüm çıpaları (yer, çıpa) olarak döndürür: arc, events/theme 'at', gates a/b, katman pencereleri (win), kesit sınırı (until)."""
    out = []
    for a in spec.get("arc", []) or []:
        if isinstance(a[0], (str, tuple, list)):
            out.append(("arc", a[0]))
    for key in ("events", "theme"):
        for ev in spec.get(key, []) or []:
            if ev.get("at") is not None:
                out.append((key, ev["at"]))
    for gt in spec.get("gates", []) or []:
        out.append(("gate", gt["a"]))
        out.append(("gate", gt["b"]))
    for k, v in spec.items():
        if isinstance(v, dict) and v.get("win"):
            for w in v["win"]:
                for x in w:
                    out.append((f"{k}.win", x[0] if isinstance(x, (tuple, list)) else x))
    for sc in spec.get("sections", []) or []:
        out.append(("until", sc["until"][0]) if sc.get("until") else ("until", None))
        out.extend(_spec_anchors(sc))
    return [(w, a) for (w, a) in out if a is not None]


def anchor_audit(chapters, timeline):
    """Parçadaki bölümlerin CUES çıpalarını timeline.json'a karşı denetler. Döner: (toplam, [(bölüm, yer, çıpa, durum)]); durum: 'cümle yok' (kimlik çizelgede yok → DEFAULT_U'ya düşer)
    | 'sözcük yok' (cümle var, sözcük anahtarı bulunamadı → cümle başına düşer)."""
    sent = D.sent_index(timeline)
    bad, n = [], 0
    for ch in chapters:
        cid = ch["id"] if isinstance(ch, dict) else ch
        if cid not in CUES:
            continue
        for where, anc in _spec_anchors(CUES[cid]):
            n += 1
            a = [anc] if isinstance(anc, str) else list(anc)
            if a[0] not in sent:
                bad.append((cid, where, anc, "cümle yok"))
            elif len(a) >= 3 and isinstance(a[1], str) and a[1] not in ("end", "son", "t1") and D.anchor_time(a, sent) is None:
                bad.append((cid, where, anc, "sözcük yok"))
    return n, bad


def render_music(chapters, total, tail=7.0, workers=None, cache_dir=None, seed=0, verbose=True, only=None, timeline=None):
    """Tüm kesitleri üretir, çapraz geçişle birleştirir, ortalama RMS'i TARGET_RMS_DB'ye getirir.
    Döner: (music float32 (N,2), info dict). N = (total + tail)·SR. Ducking YOK (miks.py uygular).
    info: cues (kesit tablosu), gates (video ekseninde sessizlik kapıları), global_gain_db, render_sec."""
    t_start = time.time()
    sent = D.sent_index(timeline)
    segs = plan_segments(chapters, total, tail, sent)
    N = int(round((total + tail) * SR))
    code = _code_hash()
    jobs, plan = [], []
    for sg in segs:
        sp = resolve_spec(sg["spec"], sg, sent)
        sg2 = dict(sg, spec=sp)
        plan.append(sg2)
        if only and sg["ch"] not in only and sg["id"] not in only:
            continue
        jobs.append(dict(seg=sg2, tail=tail, seed=seed))
    results, todo = {}, []
    for j in jobs:
        if cache_dir:
            key = hashlib.md5(json.dumps([j["seg"], tail, seed, code], sort_keys=True, default=str).encode()).hexdigest()[:16]
            fp = os.path.join(cache_dir, f"cue_{j['seg']['id']}_{key}.npy")
            j["_fp"] = fp
            if os.path.exists(fp):
                results[j["seg"]["id"]] = np.load(fp).astype(np.float32)
                continue
        todo.append(j)
    if todo:
        workers = max(1, min(int(workers or MAX_WORKERS), MAX_WORKERS))
        order = sorted(todo, key=lambda j: -(j["seg"]["end"] - j["seg"]["start"]))
        if workers > 1 and len(order) > 1:
            with ProcessPoolExecutor(max_workers=min(workers, len(order))) as ex:
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
                for old in glob.glob(os.path.join(cache_dir, f"cue_{j['seg']['id']}_*.npy")):   # eski sürümler birikmesin
                    try:
                        os.remove(old)
                    except OSError:
                        pass
                np.save(j["_fp"], results[j["seg"]["id"]].astype(np.float16))
    # birleştir — 1. aşama: kesit başına düzey (TARGET_RMS_DB + level_db) ve sol/sağ dengesi
    out = np.zeros((N, 2), dtype=np.float32)
    info = dict(cues=[], plan=plan, gates=[], stops=[], code=code)
    xs, gains = {}, {}
    for g in plan:
        if g["id"] not in results:
            continue
        x = results[g["id"]].astype(np.float32)
        spec = g["spec"]
        core0 = int((g["xin"] + 1.0) * SR) if g["xin"] else 0
        core1 = len(x) - int((g["xout"] + 1.0) * SR) if g["xout"] else len(x)
        if core1 - core0 < 4 * SR:
            core0, core1 = 0, len(x)
        off = g["s0"] - g["start"]
        mask = _window_mask(core0 / SR, (core1 - core0) // SR, [(a_ + off, b_ + off, l_, r_) for (a_, b_, l_, r_, f_, n_) in spec.get("_gates", [])])
        rdb = _robust_rms_db(x[core0:core1], mask=mask)
        gain = D.db2lin(TARGET_RMS_DB + spec.get("level_db", 0.0) - rdb)
        # sol/sağ güç dengesi (pan dağılımı bir yana kaymasın): L kanalı ±1,5 dB içinde eşitlenir
        pl, pr = np.mean(x[core0:core1:7, 0].astype(np.float64) ** 2), np.mean(x[core0:core1:7, 1].astype(np.float64) ** 2)
        lr = float(np.clip(0.5 * 10 * np.log10((pr + 1e-18) / (pl + 1e-18)), -1.5, 1.5))
        xs[g["id"]] = x * np.array([gain * D.db2lin(lr), gain / D.db2lin(lr)], dtype=np.float32)
        gains[g["id"]] = gain
    # 2. aşama: kavşak düzey eşlemesi (kesit sonu ↔ sonraki kesit başı ortanca düzeyleri birbirine yaklaştırılır)
    jtrim = _junction_trims(plan, xs)
    info["trims"] = {k: (round(float(h), 2), round(float(t), 2)) for k, (h, t) in jtrim.items()}
    for g in plan:
        if g["id"] not in xs:
            continue
        x, gain, spec = xs.pop(g["id"]), gains[g["id"]], g["spec"]
        th, tt = jtrim.get(g["id"], (0.0, 0.0))
        if abs(th) > 1e-3 or abs(tt) > 1e-3:
            x = x * _trim_curve(len(x), g["xin"], g["xout"], th, tt)[:, None]
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
        gts = [dict(seg=g["id"], a=round(g["s0"] + a_, 3), b=round(g["s0"] + b_, 3), lead=l_, rel=r_, floor_db=f_, note=n_)
               for (a_, b_, l_, r_, f_, n_) in spec.get("_gates", [])]
        for gg in gts:           # iki kesitte de tanımlı aynı kapıyı bir kez raporla
            dup = [x for x in info["gates"] if abs(x["a"] - gg["a"]) < 0.02 and abs(x["b"] - gg["b"]) < 0.02]
            if dup:
                dup[0]["seg"] += "+" + gg["seg"]
            else:
                info["gates"].append(gg)
        for ev in spec.get("events", []) or []:          # kuru duraklar (stop): kısa, bilinçli düzey çukurları — kavşak ölçümünde kapı gibi sayılır
            if ev.get("kind") == "stop":
                a_ = round(g["s0"] + ev["sec"], 3)
                if not any(abs(x["a"] - a_) < 0.02 for x in info["stops"]):
                    info["stops"].append(dict(seg=g["id"], a=a_, b=round(a_ + ev.get("hold", 0.9), 3), lead=ev.get("lead", 0.04), rel=ev.get("rel", 0.30)))
        info["cues"].append(dict(id=g["id"], ch=g["ch"], mood=spec["mood"], mode=spec["mode"], bpm=spec["bpm"], meter=spec["meter"], arc=spec["arc"],
                                 tonic_midi=spec["tonic"], start=round(g["start"], 2), end=round(g["end"], 2),
                                 length=round(g["end"] - g["start"], 2), chapter_dur=round(g["s1"] - g["s0"], 2), xin=g["xin"], xout=g["xout"],
                                 pre_gain_db=round(float(20 * np.log10(gain)), 2), snr_bias=float(spec.get("snr_bias", 0.0)),
                                 events=len(spec.get("events", [])), themes=len(spec.get("theme", [])), gates=len(gts), s0=round(g["s0"], 2), s1=round(g["s1"], 2)))
    # genel ölçek: tüm bandın (sessizlik hariç) ortalama RMS'i TARGET_RMS_DB
    glob = _robust_rms_db(out)
    g2 = D.db2lin(TARGET_RMS_DB - glob)
    out *= np.float32(g2)
    info["global_gain_db"] = round(float(20 * np.log10(g2)), 2)
    info["render_sec"] = round(time.time() - t_start, 1)
    return out, info


# ═══════════════════════════ komut satırı (yalnız müzik önizleme) ═══════════════════════════
def _part_dir():
    """MEDICI_PART zorunlu: out/ sembolik bağlantısına DOKUNULMAZ; her şey out_pN/ altında."""
    p = os.environ.get("MEDICI_PART")
    if not p:
        raise SystemExit("MEDICI_PART=1..7 gerekli (örn. MEDICI_PART=3 python3 muzik.py --cue c7)")
    return int(p), out_dir(int(p))


def _load_chapters(outdir):
    j = json.load(open(os.path.join(outdir, "voice_chapters.json")))
    return j["chapters"], j["total"]


def diag_cue(cid_or_seg, chapters, total, tail, timeline, seed=0):
    """Tek kesiti süreç içinde kurar (önbelleksiz) ve katman enerjisi / olay / kapı tablosunu yazdırır — ayar için."""
    sent = D.sent_index(timeline)
    segs = plan_segments(chapters, total, tail, sent)
    for sg in segs:
        if sg["id"] == cid_or_seg or sg["ch"] == cid_or_seg:
            sp = resolve_spec(sg["spec"], sg, sent)
            sg2 = dict(sg, spec=sp)
            c = build_cue(sg2, tail, seed)
            print(f"--- {sg['id']}: {sp['mood']} {sp['mode']} {sp['bpm']}bpm {sp['meter']} start={sg['start']:.2f} end={sg['end']:.2f} (T={c.T:.1f})")
            print("    arc:", [(round(u, 3), round(i, 2)) for u, i in sp["arc"]])
            for a in range(0, int(c.T), 20):
                b = min(a + 20, int(c.T) + 1)
                rep = c.layer_report(a, b)
                print(f"    {a:4d}-{b:4d} s  I={c.I(a + 10):.2f}  " + "  ".join(f"{k}:{v:6.1f}" for k, v in sorted(rep.items())))
            print("    kapılar:", [(round(g[1], 2), round(g[2], 2), round(g[4], 4)) for g in c.gates])
            print("    olaylar:", [(round(t, 1), k) for t, k, *_ in sorted(c.events_log, key=lambda e: e[0])][:60])


def main():
    ap = argparse.ArgumentParser(description="Medici müziği: ham (ducking'siz) müzik üretir.")
    ap.add_argument("--cue", help="tek cue/kesit (ör. c3, c13, c13.2) — önizleme WAV")
    ap.add_argument("--all", action="store_true", help="tüm müzik")
    ap.add_argument("--diag", help="kesit/bölüm: katman enerjisi tablosu (önbelleksiz, süreç içi)")
    ap.add_argument("--tail", type=float, default=7.0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--cache", default=None)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    part, outdir = _part_dir()
    chs, total = _load_chapters(outdir)
    tp = os.path.join(outdir, "timeline.json")
    tl = json.load(open(tp)) if os.path.exists(tp) else None
    if a.diag:
        diag_cue(a.diag, chs, total, a.tail, tl, a.seed)
        return
    only = [a.cue] if a.cue else None
    x, info = render_music(chs, total, a.tail, workers=a.workers, cache_dir=a.cache, only=only, timeline=tl, seed=a.seed)
    outp = a.out or os.path.join(outdir, "_muzik_ham.wav")
    if a.cue:
        sel = [c for c in info["cues"] if c["id"] == a.cue or c["ch"] == a.cue]
        s, e = int(min(c["start"] for c in sel) * SR), int(max(c["end"] for c in sel) * SR)
        x = x[s:e]
    D.write_wav(outp, x, SR)
    print("yazıldı:", outp, f"{len(x) / SR:.1f} sn", info["render_sec"], "sn")

DEFAULT_U = {   # cümle kimliği -> (başlangıç_u, bitiş_u): bölüm süresinin oranı (çıpa çözülemezse kullanılır; c6 sözcük sayısından kestirim)
    "c0s1": (0.0014, 0.0294), "c0s2": (0.038, 0.0825), "c0s3": (0.0907, 0.1244), "c0s4": (0.1327, 0.1924), "c0s5": (0.1989, 0.252),
    "c0s6": (0.2601, 0.3345), "c0s7": (0.3426, 0.3842), "c0s8": (0.3922, 0.4263), "c0s9": (0.4345, 0.4805), "c0s10": (0.4889, 0.5292),
    "c0s11": (0.5375, 0.5536), "c0s12": (0.5616, 0.6777), "c0s13": (0.6857, 0.762), "c0s14": (0.7705, 0.784), "c0s15": (0.7951, 0.8486),
    "c0s16": (0.8562, 0.9047), "c0s17": (0.9135, 0.9514), "c0s18": (0.9597, 0.9997),
    "c1s1": (0.0007, 0.0296), "c1s2": (0.0333, 0.0544), "c1s3": (0.0573, 0.0868), "c1s4": (0.0898, 0.1005), "c1s5": (0.1039, 0.1287),
    "c1s6": (0.1322, 0.1791), "c1s7": (0.1825, 0.1909), "c1s8": (0.1944, 0.2318), "c1s9": (0.2353, 0.274), "c1s10": (0.277, 0.3175),
    "c1s11": (0.321, 0.3398), "c1s12": (0.3435, 0.3822), "c1s13": (0.3858, 0.4342), "c1s14": (0.4374, 0.4537), "c1s15": (0.4571, 0.4754),
    "c1s16": (0.4787, 0.5225), "c1s17": (0.5252, 0.5517), "c1s18": (0.5546, 0.603), "c1s19": (0.6071, 0.6374), "c1s20": (0.6417, 0.6818),
    "c1s21": (0.6846, 0.6966), "c1s22": (0.7006, 0.7158), "c1s23": (0.7185, 0.7336), "c1s24": (0.7389, 0.7699), "c1s25": (0.7729, 0.7992),
    "c1s26": (0.7992, 0.8404), "c1s27": (0.844, 0.8849), "c1s28": (0.8886, 0.9293), "c1s29": (0.9324, 0.9393), "c1s30": (0.9426, 0.9614),
    "c1s31": (0.9644, 0.971), "c1s32": (0.9734, 0.9999),
    "c2s1": (0.0005, 0.0034), "c2s2": (0.0065, 0.0305), "c2s3": (0.033, 0.069), "c2s4": (0.072, 0.1014), "c2s5": (0.1036, 0.1189),
    "c2s6": (0.1222, 0.1428), "c2s7": (0.1459, 0.1833), "c2s8": (0.1854, 0.1916), "c2s9": (0.1943, 0.2144), "c2s10": (0.2176, 0.2446),
    "c2s11": (0.248, 0.2728), "c2s12": (0.2756, 0.2866), "c2s13": (0.2888, 0.3179), "c2s14": (0.3211, 0.3492), "c2s15": (0.3527, 0.3849),
    "c2s16": (0.3878, 0.4047), "c2s17": (0.4072, 0.4365), "c2s18": (0.4386, 0.4676), "c2s19": (0.4705, 0.4853), "c2s20": (0.4884, 0.5349),
    "c2s21": (0.5399, 0.5732), "c2s22": (0.5765, 0.6033), "c2s23": (0.606, 0.6408), "c2s24": (0.6436, 0.6564), "c2s25": (0.6594, 0.7044),
    "c2s26": (0.707, 0.7354), "c2s27": (0.7388, 0.773), "c2s28": (0.7739, 0.7911), "c2s29": (0.7941, 0.8435), "c2s30": (0.8475, 0.8975),
    "c2s31": (0.9021, 0.9108), "c2s32": (0.9136, 0.9378), "c2s33": (0.9403, 0.9531), "c2s34": (0.9587, 0.9753), "c2s35": (0.9783, 0.9995),
    "c3s1": (0.0007, 0.0272), "c3s2": (0.0315, 0.0505), "c3s3": (0.0545, 0.0654), "c3s4": (0.0692, 0.0857), "c3s5": (0.0895, 0.1171),
    "c3s6": (0.1204, 0.1521), "c3s7": (0.156, 0.2006), "c3s8": (0.2037, 0.2516), "c3s9": (0.255, 0.2645), "c3s10": (0.2682, 0.2784),
    "c3s11": (0.2822, 0.3095), "c3s12": (0.3127, 0.3473), "c3s13": (0.3513, 0.3837), "c3s14": (0.387, 0.3973), "c3s15": (0.4013, 0.4135),
    "c3s16": (0.4167, 0.4647), "c3s17": (0.4688, 0.5012), "c3s18": (0.5048, 0.5219), "c3s19": (0.5269, 0.563), "c3s20": (0.5669, 0.5907),
    "c3s21": (0.5951, 0.6204), "c3s22": (0.624, 0.65), "c3s23": (0.6533, 0.681), "c3s24": (0.6848, 0.7062), "c3s25": (0.7102, 0.7568),
    "c3s26": (0.7604, 0.7755), "c3s27": (0.7785, 0.8143), "c3s28": (0.8182, 0.8681), "c3s29": (0.872, 0.8941), "c3s30": (0.8951, 0.9183),
    "c3s31": (0.922, 0.9657), "c3s32": (0.9684, 0.973), "c3s33": (0.9761, 1.0),
    "c4s1": (0.0007, 0.0212), "c4s2": (0.0247, 0.0583), "c4s3": (0.062, 0.0964), "c4s4": (0.0998, 0.1268), "c4s5": (0.1308, 0.1703),
    "c4s6": (0.173, 0.2015), "c4s7": (0.2052, 0.2357), "c4s8": (0.2391, 0.2573), "c4s9": (0.2604, 0.2736), "c4s10": (0.2764, 0.2981),
    "c4s11": (0.3018, 0.3371), "c4s12": (0.3405, 0.3679), "c4s13": (0.3714, 0.3981), "c4s14": (0.402, 0.4568), "c4s15": (0.4599, 0.4716),
    "c4s16": (0.474, 0.5023), "c4s17": (0.5049, 0.5267), "c4s18": (0.5303, 0.5589), "c4s19": (0.5627, 0.5955), "c4s20": (0.5984, 0.6091),
    "c4s21": (0.6128, 0.6175), "c4s22": (0.62, 0.6527), "c4s23": (0.6567, 0.7053), "c4s24": (0.7088, 0.7413), "c4s25": (0.7452, 0.7951),
    "c4s26": (0.7956, 0.817), "c4s27": (0.8202, 0.8523), "c4s28": (0.8563, 0.9038), "c4s29": (0.9076, 0.9347), "c4s30": (0.9383, 0.9475),
    "c4s31": (0.9505, 0.972), "c4s32": (0.9771, 0.9818), "c4s33": (0.984, 0.9998),
    "c5s1": (0.0008, 0.0561), "c5s2": (0.061, 0.118), "c5s3": (0.1236, 0.1674), "c5s4": (0.1717, 0.198), "c5s5": (0.205, 0.2751),
    "c5s6": (0.2797, 0.3402), "c5s7": (0.3455, 0.4123), "c5s8": (0.4172, 0.4363), "c5s9": (0.4424, 0.4986), "c5s10": (0.5026, 0.5415),
    "c5s11": (0.547, 0.5813), "c5s12": (0.5877, 0.6369), "c5s13": (0.6419, 0.6749), "c5s14": (0.6791, 0.6979), "c5s15": (0.7041, 0.7718),
    "c5s16": (0.7767, 0.7912), "c5s17": (0.795, 0.8447), "c5s18": (0.8499, 0.8934), "c5s19": (0.8987, 0.9521), "c5s20": (0.957, 0.975),
    "c5s21": (0.9812, 0.9995),
    "c6s1": (0.0, 0.0516), "c6s2": (0.0524, 0.075), "c6s3": (0.0762, 0.1032), "c6s4": (0.1048, 0.1149), "c6s5": (0.1167, 0.129),
    "c6s6": (0.131, 0.1759), "c6s7": (0.1786, 0.2158), "c6s8": (0.219, 0.2486), "c6s9": (0.2524, 0.2885), "c6s10": (0.2929, 0.333),
    "c6s11": (0.3381, 0.3893), "c6s12": (0.3952, 0.4198), "c6s13": (0.4262, 0.4573), "c6s14": (0.4643, 0.4995), "c6s15": (0.5071, 0.5324),
    "c6s16": (0.5405, 0.598), "c6s17": (0.6071, 0.6473), "c6s18": (0.6571, 0.6895), "c6s19": (0.7, 0.7294), "c6s20": (0.7405, 0.781),
    "c6s21": (0.7929, 0.8068), "c6s22": (0.819, 0.8326), "c6s23": (0.8452, 0.8584), "c6s24": (0.8714, 0.8982), "c6s25": (0.9119, 0.9334),
    "c6s26": (0.9476, 0.9733), "c6s27": (0.9881, 0.985),
    "c7s1": (0.0002, 0.0144), "c7s2": (0.0123, 0.0325), "c7s3": (0.0305, 0.0585), "c7s4": (0.0558, 0.0791), "c7s5": (0.0791, 0.1072),
    "c7s6": (0.1069, 0.1431), "c7s7": (0.1431, 0.1743), "c7s8": (0.1724, 0.195), "c7s9": (0.1931, 0.2144), "c7s10": (0.2123, 0.2444),
    "c7s11": (0.2421, 0.2604), "c7s12": (0.2577, 0.2679), "c7s13": (0.2673, 0.2873), "c7s14": (0.2869, 0.3212), "c7s15": (0.3185, 0.346),
    "c7s16": (0.3438, 0.359), "c7s17": (0.3564, 0.377), "c7s18": (0.375, 0.3946), "c7s19": (0.3922, 0.4034), "c7s20": (0.4008, 0.4143),
    "c7s21": (0.4121, 0.4311), "c7s22": (0.4293, 0.4587), "c7s23": (0.4565, 0.4755), "c7s24": (0.473, 0.4863), "c7s25": (0.4863, 0.5097),
    "c7s26": (0.5072, 0.5382), "c7s27": (0.5363, 0.5628), "c7s28": (0.56, 0.5828), "c7s29": (0.5808, 0.6067), "c7s30": (0.6064, 0.6371),
    "c7s31": (0.6345, 0.6649), "c7s32": (0.6623, 0.6887), "c7s33": (0.6868, 0.707), "c7s34": (0.7049, 0.7248), "c7s35": (0.7228, 0.7357),
    "c7s36": (0.7336, 0.7635), "c7s37": (0.7617, 0.7759), "c7s38": (0.7733, 0.7937), "c7s39": (0.7919, 0.8113), "c7s40": (0.8109, 0.8446),
    "c7s41": (0.8425, 0.8686), "c7s42": (0.8686, 0.9059), "c7s43": (0.9059, 0.9327), "c7s44": (0.9306, 0.9388), "c7s45": (0.9388, 0.9526),
    "c7s46": (0.9505, 0.9855), "c7s47": (0.9833, 0.999),
    "c8s1": (0.0002, 0.0364), "c8s2": (0.0337, 0.0685), "c8s3": (0.0657, 0.1092), "c8s4": (0.1056, 0.1309), "c8s5": (0.1309, 0.1697),
    "c8s6": (0.1669, 0.1847), "c8s7": (0.1847, 0.2155), "c8s8": (0.213, 0.2508), "c8s9": (0.2479, 0.2718), "c8s10": (0.2691, 0.284),
    "c8s11": (0.2809, 0.3345), "c8s12": (0.3322, 0.3461), "c8s13": (0.3454, 0.3738), "c8s14": (0.3738, 0.422), "c8s15": (0.4213, 0.4538),
    "c8s16": (0.4512, 0.4988), "c8s17": (0.4958, 0.5071), "c8s18": (0.5071, 0.5437), "c8s19": (0.5408, 0.5516), "c8s20": (0.551, 0.575),
    "c8s21": (0.5742, 0.6031), "c8s22": (0.6026, 0.6493), "c8s23": (0.6467, 0.6896), "c8s24": (0.6858, 0.7025), "c8s25": (0.7025, 0.7354),
    "c8s26": (0.7327, 0.7564), "c8s27": (0.7537, 0.7961), "c8s28": (0.7924, 0.8327), "c8s29": (0.8303, 0.8684), "c8s30": (0.8654, 0.8997),
    "c8s31": (0.897, 0.9339), "c8s32": (0.931, 0.9631), "c8s33": (0.9595, 0.9763), "c8s34": (0.9738, 0.9986),
    "c9s1": (0.0003, 0.0325), "c9s2": (0.0292, 0.0712), "c9s3": (0.0674, 0.1142), "c9s4": (0.1109, 0.1474), "c9s5": (0.1439, 0.1816),
    "c9s6": (0.1783, 0.2278), "c9s7": (0.2235, 0.2772), "c9s8": (0.2739, 0.3275), "c9s9": (0.3265, 0.3482), "c9s10": (0.3482, 0.4202),
    "c9s11": (0.4168, 0.4363), "c9s12": (0.4357, 0.4609), "c9s13": (0.4609, 0.4829), "c9s14": (0.4784, 0.5301), "c9s15": (0.5258, 0.5381),
    "c9s16": (0.5349, 0.5949), "c9s17": (0.5912, 0.6517), "c9s18": (0.6482, 0.701), "c9s19": (0.6978, 0.7219), "c9s20": (0.7184, 0.7631),
    "c9s21": (0.7587, 0.7905), "c9s22": (0.7874, 0.8367), "c9s23": (0.8331, 0.8652), "c9s24": (0.8619, 0.8923), "c9s25": (0.889, 0.9297),
    "c9s26": (0.9255, 0.9574), "c9s27": (0.9539, 0.9713), "c9s28": (0.968, 0.9984),
    "c10s1": (0.0002, 0.0306), "c10s2": (0.0283, 0.0537), "c10s3": (0.0511, 0.0835), "c10s4": (0.0808, 0.1045), "c10s5": (0.1021, 0.1473),
    "c10s6": (0.1447, 0.1682), "c10s7": (0.1649, 0.2076), "c10s8": (0.2076, 0.2458), "c10s9": (0.2434, 0.2758), "c10s10": (0.2726, 0.3007),
    "c10s11": (0.2979, 0.3321), "c10s12": (0.3297, 0.3707), "c10s13": (0.3707, 0.3863), "c10s14": (0.3835, 0.4103), "c10s15": (0.4081, 0.4308),
    "c10s16": (0.4285, 0.4442), "c10s17": (0.4417, 0.4817), "c10s18": (0.4811, 0.4951), "c10s19": (0.4923, 0.5183), "c10s20": (0.5161, 0.5511),
    "c10s21": (0.5478, 0.5808), "c10s22": (0.5785, 0.6207), "c10s23": (0.6182, 0.6494), "c10s24": (0.6473, 0.6684), "c10s25": (0.6684, 0.6961),
    "c10s26": (0.6933, 0.7257), "c10s27": (0.7235, 0.7531), "c10s28": (0.7507, 0.7825), "c10s29": (0.7803, 0.7968), "c10s30": (0.7945, 0.815),
    "c10s31": (0.8115, 0.8589), "c10s32": (0.8589, 0.8927), "c10s33": (0.89, 0.9087), "c10s34": (0.9087, 0.9499), "c10s35": (0.9469, 0.9759),
    "c10s36": (0.9726, 0.9987),
    "c11s1": (0.0002, 0.0388), "c11s2": (0.0366, 0.0622), "c11s3": (0.0603, 0.0935), "c11s4": (0.0907, 0.1328), "c11s5": (0.1328, 0.1622),
    "c11s6": (0.1604, 0.178), "c11s7": (0.1753, 0.2029), "c11s8": (0.2008, 0.2298), "c11s9": (0.2298, 0.248), "c11s10": (0.2458, 0.2731),
    "c11s11": (0.2712, 0.2999), "c11s12": (0.2994, 0.3276), "c11s13": (0.3253, 0.3547), "c11s14": (0.3547, 0.3841), "c11s15": (0.3841, 0.4265),
    "c11s16": (0.4247, 0.4415), "c11s17": (0.4391, 0.4605), "c11s18": (0.4584, 0.4815), "c11s19": (0.4792, 0.5022), "c11s20": (0.5022, 0.5281),
    "c11s21": (0.5281, 0.5525), "c11s22": (0.5517, 0.59), "c11s23": (0.5877, 0.6095), "c11s24": (0.6068, 0.6493), "c11s25": (0.6468, 0.6849),
    "c11s26": (0.6826, 0.7072), "c11s27": (0.7049, 0.736), "c11s28": (0.736, 0.7777), "c11s29": (0.7757, 0.8087), "c11s30": (0.8065, 0.8256),
    "c11s31": (0.8256, 0.8561), "c11s32": (0.8534, 0.8871), "c11s33": (0.8871, 0.9194), "c11s34": (0.9174, 0.9413), "c11s35": (0.9391, 0.965),
    "c11s36": (0.965, 0.9822), "c11s37": (0.98, 0.9973), "c11s38": (0.9949, 0.999),
    "c12s1": (0.0002, 0.028), "c12s2": (0.0252, 0.0589), "c12s3": (0.0566, 0.0907), "c12s4": (0.0881, 0.1268), "c12s5": (0.1268, 0.1506),
    "c12s6": (0.1481, 0.197), "c12s7": (0.1944, 0.2164), "c12s8": (0.2138, 0.232), "c12s9": (0.232, 0.2742), "c12s10": (0.2716, 0.3053),
    "c12s11": (0.3053, 0.3371), "c12s12": (0.3343, 0.3534), "c12s13": (0.3511, 0.3725), "c12s14": (0.3698, 0.4126), "c12s15": (0.412, 0.4274),
    "c12s16": (0.4242, 0.4488), "c12s17": (0.4488, 0.4756), "c12s18": (0.4731, 0.5155), "c12s19": (0.5124, 0.5362), "c12s20": (0.5362, 0.561),
    "c12s21": (0.561, 0.5849), "c12s22": (0.5849, 0.5996), "c12s23": (0.5996, 0.6324), "c12s24": (0.6324, 0.6708), "c12s25": (0.6683, 0.6845),
    "c12s26": (0.6845, 0.7348), "c12s27": (0.7324, 0.7711), "c12s28": (0.7707, 0.78), "c12s29": (0.78, 0.8049), "c12s30": (0.8049, 0.8415),
    "c12s31": (0.8415, 0.8776), "c12s32": (0.8776, 0.9228), "c12s33": (0.9202, 0.9361), "c12s34": (0.9335, 0.9559), "c12s35": (0.9536, 0.9988),
    "c13s1": (0.0003, 0.0316), "c13s2": (0.0294, 0.064), "c13s3": (0.064, 0.0904), "c13s4": (0.0876, 0.1029), "c13s5": (0.0998, 0.1203),
    "c13s6": (0.1203, 0.1357), "c13s7": (0.1357, 0.1629), "c13s8": (0.1602, 0.1784), "c13s9": (0.1784, 0.2016), "c13s10": (0.199, 0.2447),
    "c13s11": (0.2447, 0.283), "c13s12": (0.283, 0.3135), "c13s13": (0.3112, 0.3458), "c13s14": (0.3436, 0.3574), "c13s15": (0.3542, 0.3785),
    "c13s16": (0.3763, 0.4195), "c13s17": (0.4172, 0.4508), "c13s18": (0.4484, 0.4776), "c13s19": (0.4749, 0.4953), "c13s20": (0.4927, 0.5162),
    "c13s21": (0.5138, 0.5595), "c13s22": (0.5564, 0.5951), "c13s23": (0.5919, 0.612), "c13s24": (0.6092, 0.6315), "c13s25": (0.629, 0.6671),
    "c13s26": (0.6647, 0.6851), "c13s27": (0.6824, 0.6997), "c13s28": (0.6997, 0.7238), "c13s29": (0.7216, 0.7647), "c13s30": (0.7647, 0.789),
    "c13s31": (0.7866, 0.808), "c13s32": (0.808, 0.8431), "c13s33": (0.8409, 0.8748), "c13s34": (0.8721, 0.9039), "c13s35": (0.9009, 0.9231),
    "c13s36": (0.9209, 0.9564), "c13s37": (0.9537, 0.9755), "c13s38": (0.9731, 0.9987),
    "c14s1": (0.0003, 0.0575), "c14s2": (0.0543, 0.094), "c14s3": (0.0908, 0.144), "c14s4": (0.1407, 0.1814), "c14s5": (0.1785, 0.2083),
    "c14s6": (0.2041, 0.2628), "c14s7": (0.2628, 0.3134), "c14s8": (0.31, 0.3428), "c14s9": (0.3388, 0.3804), "c14s10": (0.3804, 0.4086),
    "c14s11": (0.4055, 0.4363), "c14s12": (0.4363, 0.4758), "c14s13": (0.4728, 0.523), "c14s14": (0.5198, 0.5691), "c14s15": (0.5663, 0.6047),
    "c14s16": (0.6015, 0.6385), "c14s17": (0.6356, 0.6622), "c14s18": (0.6622, 0.7301), "c14s19": (0.727, 0.7499), "c14s20": (0.7499, 0.8056),
    "c14s21": (0.8056, 0.8475), "c14s22": (0.8442, 0.892), "c14s23": (0.889, 0.9167), "c14s24": (0.9167, 0.9471), "c14s25": (0.9441, 0.9713),
    "c14s26": (0.9672, 0.9983),
    "c15s1": (0.0005, 0.0719), "c15s2": (0.0676, 0.1095), "c15s3": (0.1059, 0.1629), "c15s4": (0.1629, 0.2051), "c15s5": (0.2051, 0.2512),
    "c15s6": (0.2476, 0.2912), "c15s7": (0.287, 0.3473), "c15s8": (0.3425, 0.409), "c15s9": (0.4053, 0.4829), "c15s10": (0.4829, 0.5406),
    "c15s11": (0.5367, 0.5991), "c15s12": (0.5955, 0.633), "c15s13": (0.633, 0.6801), "c15s14": (0.6762, 0.7506), "c15s15": (0.7465, 0.8),
    "c15s16": (0.8, 0.8445), "c15s17": (0.8445, 0.9122), "c15s18": (0.909, 0.9687), "c15s19": (0.9644, 0.9981),
    "c16s1": (0.0003, 0.0423), "c16s2": (0.038, 0.0898), "c16s3": (0.0849, 0.1534), "c16s4": (0.1497, 0.1936), "c16s5": (0.1895, 0.2414),
    "c16s6": (0.2378, 0.267), "c16s7": (0.2621, 0.2833), "c16s8": (0.2794, 0.3223), "c16s9": (0.3214, 0.3659), "c16s10": (0.3625, 0.435),
    "c16s11": (0.4306, 0.4782), "c16s12": (0.4738, 0.5041), "c16s13": (0.499, 0.5258), "c16s14": (0.522, 0.5666), "c16s15": (0.5629, 0.5987),
    "c16s16": (0.5949, 0.6386), "c16s17": (0.6342, 0.6819), "c16s18": (0.6769, 0.7305), "c16s19": (0.7264, 0.7526), "c16s20": (0.7526, 0.8145),
    "c16s21": (0.8087, 0.8431), "c16s22": (0.8382, 0.8826), "c16s23": (0.8778, 0.9519), "c16s24": (0.9483, 0.9661), "c16s25": (0.9626, 0.9981),
}


# ═══════════════════════════ cue tanımları (bölüm ruh hali → müzik) ═══════════════════════════
# tonic: ana ses MIDI (bas yazmacı); arc: (u, yoğunluk) | A("cNsK", yoğunluk[, dt]) — u=0 bölüm (kesit) başı, u=1 sonu; prog: [(derece, ölçü, ek)]
# Katmanlar: drone (gamba), choir (koro/org pedi), arp, arp2 (lavta/klavsen), bass, melody, perc (çerçeve davulu), bell (YALNIZ müzikal tını),
# theme (açık motif girişleri), events (çıpalı vuruş/akor/durak), gates (sessizlik kapıları), recit (c14), sections (mod/tempo değişimi).
# ÇAN KURALI: c7 (26 Nisan) ve c10 (9 Kasım) cue'larında 'bell' katmanı/olayı YOK (olay çanı kaynakta yok; ses değil, müzik bile çan çağrıştırmaz).
def A(sid, I, dt=0.0):
    return (sid, None, I, dt)


def W(a, b):
    """Katman penceresi: a ve b çıpa (cümle kimliği ya da ("cNsK","end",dt))."""
    return ((a, None), (b, None))


def E(kind, at, **kw):
    return dict(kind=kind, at=at, **kw)


def TH(motif, at, **kw):
    return dict(motif=motif, at=at, **kw)


def STOP(at, hold=0.9, **kw):
    return dict(kind="stop", at=at, hold=hold, **kw)


def GATE(a, b, lead=0.6, rel=3.0, floor_db=None, note="", **kw):
    return dict(a=a, b=b, lead=lead, rel=rel, floor_db=floor_db, note=note, **kw)


def END(sid, dt=0.0):
    return (sid, "end", dt)


STOP_OPEN = (("flute", 1.0, 1.0), ("principal", 0.35, 1.0), ("flute", 0.25, 2.0))
REED = (("reed", 1.0, 1.0), ("principal", 0.4, 1.0))

CUES = {
    # ───────────────────────────── ALTIN perdesi (c0–c6) ─────────────────────────────
    # c0: soğuk açılış — 1743 ölüm odası; sakin, ağırbaşlı. 'miras' hücresi (düşen üçlü) lavtada; başlık anında TEK vuruş + altın D majör, ardından florin figürü
    "c0": dict(mood="solemn", tonic=38, mode="dorian", bpm=58, meter="4/4", level_db=0.0,
               arc=[(-1, .05), (0, .08), A("c0s2", .10), A("c0s6", .16), A("c0s9", .18), A("c0s11", .24), A("c0s12", .28), A("c0s14", .16),
                    A("c0s15", .34), A("c0s16", .42), A("c0s17", .58), A("c0s18", .70), (1.0, .72)],
               prog=[[(0, 2, "5"), (6, 2, "5"), (0, 2, "sus2"), (3, 2, "5")], [(0, 2, "sus2"), (6, 2, ""), (4, 2, "5"), (3, 2, "")]], b_thr=0.5,
               drone=dict(lvl=1.0, chunk_bars=2, fifth=True),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.4, lo=0.14, hi=0.5, voices=4),
               melody=dict(inst="lute", lvl=1.2, lo=-1, hi=-0.5, cut=(0.30, 0.50), play=2, rest=1, dens=0.3, reg=(55, 69), motif="miras", motif_p=1.0),
               perc=dict(pattern="heartbeat", lvl=0.9, lo=0.36, hi=0.7, pitch=92, amp=0.7),
               theme=[TH("miras", "c0s1", dt=0.8, inst="lute", vel=0.55),
                      TH("miras", "c0s6", dt=0.2, inst="lute", vel=0.5),
                      TH("miras", "c0s11", dt=0.0, inst="organ", vel=0.5, hold=True)],
               events=[STOP(END("c0s9", -0.35), hold=0.8)],        # tek kuru dokunuş: "Floransa'nın diliyle bile yazılmamıştı"
               finale="c0",
               finale_gain=dict(rv=0.45, riser=0.10, roll=0.07, cluster=0.2, timp=0.35, timp2=0.28, gong=0.25, sub=0.12,
                                organ=0.3, choir=0.3, bowed=0.45, bell=0.4, lute=0.3)),
    # c1: florin şehri — 6/8 hafif dans; florin motifi (yükselen parlak figür). Veba: renk solar (arp/koro kesilir, yalnız gamba + seyrek nota);
    # Ciompi: davul yükselir, "ezildi"de ani sessizlik; Giovanni'nin tezgâhı: florin geri döner. (G mixolydian, 72 bpm)
    "c1": dict(mood="curious", tonic=43, mode="mixolydian", bpm=72, meter="6/8", level_db=-0.5,
               arc=[(-1, .34), (0, .38), A("c1s2", .46), A("c1s3", .38), A("c1s4", .48), A("c1s7", .52), A("c1s9", .42), A("c1s10", .36),
                    A("c1s11", .22), A("c1s13", .12), A("c1s14", .10), A("c1s15", .30), A("c1s17", .45), A("c1s18", .72), A("c1s19", .62),
                    A("c1s21", .45), A("c1s22", .22), A("c1s23", .12), A("c1s24", .28), A("c1s26", .36), A("c1s27", .42), A("c1s28", .50),
                    A("c1s29", .62), A("c1s30", .70), A("c1s31", .50), A("c1s32", .42), (1.0, .38)],
               prog=[[(5, 2, "5"), (1, 2, ""), (0, 2, "5"), (6, 2, "")],
                     [(0, 2, ""), (6, 1, ""), (3, 1, ""), (0, 2, ""), (6, 1, ""), (3, 1, "")]], b_thr=0.26,
               drone=dict(lvl=0.5, chunk_bars=4, fifth=True),
               arp=dict(inst="lute", pattern="lilt", lvl=0.85, lo=0.30, hi=0.38, p0=0.75, p1=0.25),
               arp2=dict(inst="harp", pattern="florin", lvl=0.45, lo=0.46, hi=0.54, p0=0.8, p1=0.2, transpose=12),
               melody=dict(inst="harp", lvl=0.8, lo=0.40, hi=0.46, play=2, rest=2, dens=0.45, reg=(66, 81), motif="florin"),
               choir=dict(inst="organ", lvl=0.38, lo=0.50, hi=0.60, voices=3, stops=(("flute", 1.0, 1.0), ("flute", 0.3, 2.0)), attack=0.4),
               perc=dict(pattern="gallop", tef="lilt", lvl=0.9, lo=0.34, hi=0.5, pitch=100, amp=0.6, win=[W("c1s15", END("c1s22", -0.5))]),
               bass=dict(inst="lute", pattern="lilt", lvl=0.6, lo=0.44, hi=0.52),
               theme=[TH("florin_uzun", ("c1s2", "florin", 0.0), inst="lute", vel=0.62, oct=0),
                      TH("florin", ("c1s29", "florindi", -0.1), inst="harp", vel=0.7),
                      TH("florin_uzun", ("c1s30", "masa", 0.0), inst="lute", vel=0.6),
                      TH("bedel", "c1s11", dt=0.5, inst="gamba", vel=0.5, bend=-30, g=0.9)],
               events=[E("timp", "c1s18", dt=0.4, vel=0.8, g=0.5),
                       E("organ", "c1s30", dt=0.4, deg=[0, 4, 7, 9], oct=1, vel=0.5, dur=5.0, attack=0.6, g=0.5),
                       STOP(END("c1s21", -0.2), hold=0.8)],
               gates=[GATE(END("c1s22", -0.5), END("c1s23", 0.0), lead=0.3, rel=2.5, floor_db=-30, note="Ciompi ezildi")]),
    # c2: defter — kuru, ironik; 'ledger' tık-tık arpej (klavsen), bas ostinato, ölçülü kuru duraklar (mizah). Giovanni'nin ölümü ve son sözler: yumuşar. (A mixolydian, 70 bpm)
    "c2": dict(mood="dry", tonic=45, mode="mixolydian", bpm=70, meter="4/4", level_db=0.0,
               arc=[(-1, .34), (0, .36), A("c2s1", .38), A("c2s3", .50), A("c2s5", .55), A("c2s6", .46), A("c2s8", .42), A("c2s9", .50),
                    A("c2s11", .58), A("c2s13", .50), A("c2s15", .55), A("c2s18", .50), A("c2s19", .45), A("c2s21", .56), A("c2s22", .52),
                    A("c2s25", .60), A("c2s26", .30), A("c2s27", .28), A("c2s28", .26), A("c2s29", .30), A("c2s31", .26), A("c2s32", .30),
                    A("c2s33", .38), A("c2s34", .32), A("c2s35", .46), (1.0, .50)],
               prog=[[(0, 2, ""), (6, 2, ""), (0, 2, ""), (3, 2, "")], [(0, 1, "5"), (6, 1, "5"), (3, 1, ""), (4, 1, ""), (0, 2, ""), (6, 2, "")]], b_thr=0.44,
               drone=dict(lvl=0.7, mode="roots", chunk_bars=2, fifth=False),
               bass=dict(inst="lute", pattern="p332", lvl=0.85, lo=0.26, hi=0.38),
               arp=dict(inst="harp", pattern="ledger", lvl=0.55, lo=0.30, hi=0.42, p0=0.85, p1=0.1, transpose=12),
               perc=dict(pattern="p332", tef="sparse", lvl=0.6, lo=0.46, hi=0.58, pitch=98, amp=0.5, fill=4),
               choir=dict(inst="organ", stops=REED, lvl=0.42, lo=0.56, hi=0.68, voices=4, attack=0.6),
               melody=dict(inst="lute", lvl=0.75, lo=0.40, hi=0.50, play=2, rest=2, dens=0.3, reg=(57, 72), motif="defter"),
               events=[STOP(END("c2s8", -0.1)), STOP(END("c2s19", -0.2)), STOP(END("c2s33", -0.1), hold=1.0),
                       E("lute", ("c2s35", "kule", 0.0), deg=[0, 4], oct=0, vel=0.5, g=0.8)]),
    # c3: kule ve sürgün — gerilim → sessiz güç. Hücre: seyrek damla; torbalar: sinsi ostinato; 1434 dönüşü: 'dönüş' motifi (org+lavta). (E aeolian, 66 bpm)
    "c3": dict(mood="tense", tonic=40, mode="aeolian", bpm=66, meter="4/4", level_db=0.0,
               arc=[(-1, .34), (0, .36), A("c3s1", .38), A("c3s2", .36), A("c3s5", .50), A("c3s6", .58), A("c3s7", .44), A("c3s9", .40), A("c3s10", .34),
                    A("c3s11", .38), A("c3s13", .42), A("c3s15", .46), A("c3s16", .56), A("c3s17", .70), A("c3s18", .50), A("c3s19", .46), A("c3s20", .52),
                    A("c3s21", .50), A("c3s22", .56), A("c3s25", .62), A("c3s26", .48), A("c3s28", .52), A("c3s29", .46), A("c3s30", .26), A("c3s31", .30),
                    A("c3s32", .24), A("c3s33", .34), (1.0, .34)],
               prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 1, "5"), (6, 1, "5"), (5, 1, ""), (6, 1, ""), (0, 2, "5"), (4, 2, "5")]], b_thr=0.55,
               drone=dict(lvl=0.85, mode="roots", chunk_bars=2, fifth=True),
               bass=dict(inst="lute", pattern="p332", lvl=0.8, lo=0.36, hi=0.5),
               arp=dict(inst="lute", pattern="sparse", lvl=0.6, lo=0.20, hi=0.32, p0=0.8, p1=0.2),
               arp2=dict(inst="lute", pattern="ostinato", lvl=0.5, lo=0.30, hi=0.42, p0=0.7, p1=0.3, win=[W("c3s22", END("c3s25", 0.0))]),
               choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.62, hi=0.75, voices=4, attack=0.5),
               perc=dict(pattern="proc", lvl=0.7, lo=0.42, hi=0.55, pitch=90, amp=0.6),
               melody=dict(inst="lute", lvl=0.7, lo=0.46, hi=0.56, play=2, rest=2, dens=0.25, reg=(59, 74), motif="sorgu"),
               theme=[TH("bedel", "c3s9", dt=0.2, inst="gamba", vel=0.55, bend=-30, g=0.9),
                      TH("donus", ("c3s17", "döndü", -0.2), inst="organ", vel=0.6, stretch=1.6, hold=True),
                      TH("donus", ("c3s17", "döndü", -0.2), inst="lute", vel=0.6, stretch=1.6, oct=1)],
               events=[STOP(END("c3s3", -0.1)), STOP(END("c3s10", -0.1), hold=1.0), STOP(END("c3s32", -0.1)),
                       E("organ", "c3s33", dt=3.0, deg=[0, 4, 7, 9], oct=0, vel=0.5, dur=7.0, attack=0.8, g=0.55)]),
    # c4: kubbe — sıcak; kubbe katman katman yükselir (duomo motifi), kutsamada koro+org koral, kefaret/yatırım sorusu açık kalır. (G mixolydian, 64 bpm)
    "c4": dict(mood="warm", tonic=43, mode="mixolydian", bpm=64, meter="4/4", level_db=0.0,
               arc=[(-1, .24), (0, .26), A("c4s1", .28), A("c4s3", .34), A("c4s4", .44), A("c4s5", .40), A("c4s7", .42), A("c4s8", .46), A("c4s9", .66),
                    A("c4s11", .70), A("c4s12", .58), A("c4s13", .46), A("c4s14", .34), A("c4s17", .36), A("c4s18", .36), A("c4s20", .44), A("c4s21", .46),
                    A("c4s23", .50), A("c4s25", .50), A("c4s26", .56), A("c4s27", .56), A("c4s28", .66), A("c4s29", .70), A("c4s30", .42), A("c4s31", .38),
                    A("c4s32", .22), A("c4s33", .32), (1.0, .30)],
               prog=[[(0, 2, ""), (3, 2, ""), (0, 2, "sus4"), (6, 2, "")], [(0, 2, ""), (4, 2, ""), (3, 2, ""), (0, 2, "5")]], b_thr=0.55,
               drone=dict(lvl=0.6, chunk_bars=4, fifth=True),
               choir=dict(inst="choir", vowel=("o", "a"), lvl=0.75, lo=0.30, hi=0.44, voices=4),
               arp=dict(inst="lute", pattern="pavane", lvl=0.65, lo=0.26, hi=0.38, p0=0.8, p1=0.2),
               arp2=dict(inst="harp", pattern="florin", lvl=0.4, lo=0.52, hi=0.62, p0=0.8, p1=0.2, transpose=12),
               melody=dict(inst="organ", lvl=0.55, lo=0.44, hi=0.54, play=2, rest=2, dens=0.12, reg=(59, 74), motif="dolasim"),
               bass=dict(inst="lute", pattern="walk", lvl=0.6, lo=0.42, hi=0.54),
               perc=dict(pattern="proc", tef="sparse", lvl=0.6, lo=0.52, hi=0.62, pitch=90, amp=0.6),
               theme=[TH("duomo", ("c4s4", "tasarımı", 0.0), inst="organ", vel=0.6, stretch=1.2, hold=True),
                      TH("duomo", "c4s9", dt=0.3, inst="organ", vel=0.65, stretch=1.0, hold=True),
                      TH("duomo", "c4s9", dt=0.3, inst="lute", vel=0.6, oct=1)],
               events=[E("organ", "c4s10", dt=0.0, midi=[43, 50, 55, 59, 62, 67], vel=0.6, dur=9.0, attack=0.9, g=0.7),
                       E("choir", "c4s10", dt=0.4, midi=[55, 62, 67, 71], vel=0.65, dur=8.0, attack=1.4, g=0.7, vowel="o", vowel2="a"),
                       STOP(END("c4s20", -0.1)), STOP(END("c4s23", -0.1), hold=0.8)],
               gates=[GATE(("c4s32", 0.0), END("c4s32", 0.0), lead=0.3, rel=2.0, floor_db=-18, note="Duvarlar dikilmişti")]),
    # c5: konsil, kitap, Platon — sıcak, düşünceli; 3/4 sarabande; Doğu heyeti alayı (davul), 1453 sessizlik, Orfik lir (lavta kadansı), Lorenzo'ya geçiş. (D mixolydian, 63 bpm)
    "c5": dict(mood="warm", tonic=38, mode="mixolydian", bpm=63, meter="3/4", level_db=-0.5,
               arc=[(-1, .30), (0, .34), A("c5s1", .36), A("c5s2", .46), A("c5s3", .56), A("c5s4", .24), A("c5s5", .40), A("c5s6", .38), A("c5s7", .42),
                    A("c5s8", .56), A("c5s9", .40), A("c5s10", .42), A("c5s11", .46), A("c5s12", .44), A("c5s13", .38), A("c5s14", .30), A("c5s15", .46),
                    A("c5s16", .52), A("c5s17", .42), A("c5s19", .50), A("c5s20", .40), A("c5s21", .46), (1.0, .50)],
               prog=[[(0, 2, ""), (3, 2, ""), (0, 2, "sus2"), (6, 2, "")], [(0, 2, "add9"), (4, 2, ""), (3, 2, ""), (0, 2, "")]], b_thr=0.5,
               drone=dict(lvl=0.6, chunk_bars=4, fifth=True),
               choir=dict(inst="organ", stops=(("flute", 1.0, 1.0), ("flute", 0.3, 2.0)), lvl=0.45, lo=0.34, hi=0.46, voices=4, attack=0.7),
               arp=dict(inst="lute", pattern="sarab", lvl=0.8, lo=0.26, hi=0.38, p0=0.85, p1=0.15),
               arp2=dict(inst="harp", pattern="pavane", lvl=0.4, lo=0.46, hi=0.56, p0=0.8, p1=0.2, transpose=12),
               melody=dict(inst="lute", lvl=0.8, lo=0.36, hi=0.46, play=2, rest=2, dens=0.3, reg=(57, 72), motif="dolasim"),
               perc=dict(pattern="sarab", tef="sarab", lvl=0.6, lo=0.30, hi=0.40, pitch=100, amp=0.55,
                         win=[W("c5s2", END("c5s3", 0.0)), W("c5s15", END("c5s19", 0.0))]),
               theme=[dict(notes=[(0, 1), (2, 1), (4, 1), (5, 1), (7, 1), (9, 5)], at=("c5s11", "lir", 0.1), inst="lute", vel=0.6, snap=False, g=0.9),
                      dict(notes=[(2, 2), (4, 2), (5, 3), (4, 1)], at="c5s21", dt=1.0, inst="harp", vel=0.5, stretch=1.3, g=0.8)],
               events=[E("timp", ("c5s4", "düştü", 0.0), f=55.0, vel=0.7, dur=3.0, g=0.5),
                       E("gamba", ("c5s4", "düştü", 0.0), deg=[0], oct=0, vel=0.6, dur=5.0, attack=0.8, bend=-30, g=0.7),
                       STOP(END("c5s11", -0.1))],
               gates=[GATE(("c5s4", "düştü", 0.0), END("c5s4", 0.6), lead=0.2, rel=2.5, floor_db=-20, note="1453")]),
    # c6: Lorenzo — sıcak, hafif; Lorenzo teması (4 ölçü, yay biçimi). Giostra: davul + hızlı arpej. İki kesit: [parlak D ionian] → [gölge: D dorian, açık uç; 'bedel' yayı c7'ye köprü]. P3'ün ilk bölümü (t=0'da açılır); c7'ye normal kartla geçer.
    "c6": dict(mood="warm", tonic=38, mode="ionian", bpm=72, meter="4/4", level_db=0.0,
               sections=[
                   dict(until=(END("c6s25", 0.0), 0.965), xf=4.0,
                        arc=[(-1, .34), (0, .38), A("c6s1", .36), A("c6s5", .40), A("c6s6", .34), A("c6s9", .50), A("c6s10", .52), A("c6s13", .50), A("c6s14", .46),
                             A("c6s15", .50), A("c6s17", .64), A("c6s18", .54), A("c6s19", .56), A("c6s20", .72), A("c6s21", .76), A("c6s22", .64),
                             A("c6s23", .42), A("c6s24", .30), A("c6s25", .30), (1.0, .26)],
                        prog=[[(0, 2, ""), (3, 2, ""), (4, 2, ""), (0, 2, "")], [(0, 2, ""), (5, 2, ""), (3, 2, ""), (4, 2, "")]], b_thr=0.5,
                        drone=dict(lvl=0.5, chunk_bars=4, fifth=True),
                        choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.45, lo=0.46, hi=0.56, voices=4, attack=0.5),
                        arp=dict(inst="lute", pattern="alberti", lvl=0.7, lo=0.30, hi=0.42, p0=0.8, p1=0.2),
                        arp2=dict(inst="harp", pattern="florin", lvl=0.42, lo=0.52, hi=0.62, p0=0.8, p1=0.2, transpose=12),
                        bass=dict(inst="lute", pattern="walk", lvl=0.6, lo=0.46, hi=0.56),
                        melody=dict(inst="harp", lvl=0.7, lo=0.42, hi=0.52, play=2, rest=2, dens=0.4, reg=(64, 79), motif="lorenzo"),
                        perc=dict(pattern="palle", tef="eighths", lvl=0.8, lo=0.5, hi=0.6, pitch=96, amp=0.55, win=[W("c6s20", END("c6s22", 0.0))]),
                        theme=[TH("lorenzo", "c6s1", dt=0.6, inst="lute", vel=0.55, g=0.9),
                               TH("lorenzo", "c6s9", dt=0.2, inst="harp", vel=0.6),
                               TH("lorenzo", ("c6s17", "Muhteşem", -0.3), inst="organ", vel=0.65, hold=True, g=0.9),
                               TH("lorenzo", ("c6s17", "Muhteşem", -0.3), inst="lute", vel=0.6, oct=1),
                               TH("lorenzo", ("c6s20", "turnuva", -0.2), inst="lute", vel=0.7, stretch=0.85, oct=1),
                               TH("lorenzo", "c6s25", dt=0.4, inst="lute", vel=0.45, stretch=1.45, g=0.9)],
                        events=[STOP(END("c6s19", -0.1), hold=0.8)]),
                   dict(mood="grave", mode="dorian", bpm=54, level_db=-1.0,
                        arc=[(-1, .22), (0, .24), A("c6s26", .30), A("c6s27", .42), (1.0, .36)],
                        prog=[[(0, 2, "5"), (6, 2, ""), (3, 2, ""), (0, 2, "sus2")]], b_thr=2.0,
                        drone=dict(lvl=0.8, chunk_bars=4, fifth=True, bright=0.5),
                        choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.45, lo=0.22, hi=0.32, voices=4, attack=0.9),
                        arp=dict(inst="lute", pattern="sparse", lvl=0.5, lo=0.24, hi=0.34, p0=0.8, p1=0.2),
                        perc=dict(pattern="none", lvl=0.0),
                        theme=[TH("lorenzo", "c6s26", dt=0.5, inst="lute", vel=0.42, stretch=1.5, g=0.9),
                               TH("bedel", ("c6s27", "ölecekti", -1.0), inst="gamba", vel=0.6, bend=-40, g=1.0)])]),

    # ───────────────────────────── BEDEL perdesi (c7–c11) ─────────────────────────────
    # c7: 26 Nisan 1478 — AĞIR, mizah kapalı. İki kesit: [D dorian: kilise girişi, defter ve kin, plan] → (V5–V7 sessizliğinin İÇİNDE mod değişir) → [D frigiyen: sonrası].
    # 'bedel' motifi (alçak, tek çekilen yay). c6'dan sonra normal bölüm kartıyla gelir (P3: c6–c7). Kilise girişinde müzik yok (ayin yankısı + kalabalık uğultusu — SFX);
    # V5–V7 (c7s15–c7s23) yıldız an: müzik ÇEKİLİR (sessizliğe giriş 0,6 sn önce), tam sessizlik; V8'de yavaşça geri döner. ÇAN YOK.
    "c7": dict(mood="heavy", tonic=38, mode="dorian", bpm=56, meter="4/4", level_db=-1.0, snr_bias=0.5,
               sections=[
                   dict(until=(("c7s20", 0.0), 0.43), xf=3.0, mode="dorian",
                        arc=[(-1, .12), (0, .16), A("c7s1", .18), A("c7s2", .08), A("c7s3", .08), A("c7s4", .26), A("c7s5", .32), A("c7s6", .38), A("c7s7", .42),
                             A("c7s8", .44), A("c7s9", .50), A("c7s10", .52), A("c7s11", .46), A("c7s12", .36), A("c7s13", .30), A("c7s14", .22),
                             A("c7s15", .05), (1.0, .05)],
                        prog=[[(0, 2, "5"), (6, 2, ""), (0, 2, "5"), (3, 2, "")], [(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "sus4")]], b_thr=0.45,
                        drone=dict(lvl=0.9, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
                        arp=dict(inst="harp", pattern="ledger", lvl=0.45, lo=0.20, hi=0.30, p0=0.9, p1=0.1, transpose=12),
                        arp2=dict(inst="lute", pattern="sparse", lvl=0.6, lo=0.36, hi=0.48, p0=0.8, p1=0.2),
                        bass=dict(inst="lute", pattern="pedal", lvl=0.7, lo=0.34, hi=0.46),
                        choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.30, hi=0.44, voices=4, attack=0.7),
                        perc=dict(pattern="heartbeat", lvl=0.8, lo=0.32, hi=0.44, pitch=80, amp=0.7, win=[W("c7s5", END("c7s14", 0.0))]),
                        theme=[TH("bedel", "c7s1", dt=0.7, inst="gamba", vel=0.7, bend=-30, g=1.0)],
                        gates=[GATE(("c7s2", 1.0), END("c7s3", -2.0), lead=0.6, rel=2.5, floor_db=None, note="kilise girişi: ayin yankısı + kalabalık uğultusu (SFX), müzik yok"),
                               GATE(("c7s15", 0.0), END("c7s23", 0.0), lead=0.6, rel=4.0, floor_db=None, note="YILDIZ AN V5–V7: müzik çekilir")]),
                   dict(mode="phrygian", level_db=-1.0,
                        arc=[(-1, .05), (0, .05), A("c7s24", .12), A("c7s25", .26), A("c7s26", .42), A("c7s27", .52), A("c7s28", .56), A("c7s29", .50),
                             A("c7s30", .64), A("c7s31", .50), A("c7s32", .30), A("c7s35", .26), A("c7s37", .20), A("c7s38", .30), A("c7s41", .34),
                             A("c7s43", .32), A("c7s44", .26), A("c7s46", .24), A("c7s47", .20), (1.0, .14)],
                        prog=[[(0, 2, "5"), (1, 2, ""), (0, 2, "5"), (6, 2, "")], [(0, 2, ""), (1, 2, ""), (0, 2, ""), (3, 2, "")]], b_thr=0.45,
                        drone=dict(lvl=0.9, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
                        arp=dict(inst="harp", pattern="ledger", lvl=0.45, lo=0.20, hi=0.30, p0=0.9, p1=0.1, transpose=12),
                        arp2=dict(inst="lute", pattern="sparse", lvl=0.6, lo=0.36, hi=0.48, p0=0.8, p1=0.2),
                        bass=dict(inst="lute", pattern="pedal", lvl=0.7, lo=0.34, hi=0.46),
                        choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.30, hi=0.44, voices=4, attack=0.7),
                        perc=dict(pattern="heartbeat", lvl=0.8, lo=0.32, hi=0.44, pitch=80, amp=0.7, win=[W("c7s26", END("c7s31", 0.0))]),
                        theme=[TH("bedel", "c7s25", dt=0.3, inst="gamba", vel=0.45, bend=-25, g=0.9),
                               dict(notes=[(2, 2), (4, 2), (5, 3), (4, 5)], at="c7s38", dt=0.4, inst="lute", vel=0.5, g=0.9),
                               dict(notes=[(0, 3), (1, 3), (0, 6)], at="c7s39", dt=0.2, inst="organ", vel=0.5, hold=True, g=0.8),
                               TH("bedel", END("c7s46", 0.0), dt=-2.0, inst="gamba", vel=0.6, bend=-35, g=1.0)],
                        events=[E("timp", ("c7s27", "kapana", 0.0), f=48.0, vel=0.7, dur=2.6, g=0.45),
                                E("seq", ("c7s30", "palle", 0.0), hits=[(0.0, "dum", .9), (0.30, "tek", .55), (0.60, "dum", .9), (0.90, "tek", .55), (1.20, "dum", .9), (1.50, "tek", .55)], f=88.0, g=0.55),
                                E("seq", ("c7s30", "palle", 2.4), hits=[(0.0, "dum", .9), (0.30, "tek", .55), (0.60, "dum", .9), (0.90, "tek", .55), (1.20, "dum", .9), (1.50, "tek", .55)], f=88.0, g=0.5),
                                E("organ", ("c7s31", "alkışlandı", 0.0), midi=[50, 57, 62, 66], vel=0.5, dur=4.5, attack=0.4, release=2.0, g=0.45),
                                E("gamba", "c7s40", dt=0.0, deg=[0], oct=0, vel=0.5, dur=6.0, attack=0.9, bend=-30, g=0.6)],
                        gates=[GATE(("c7s15", 0.0), END("c7s23", 0.0), lead=0.6, rel=4.0, floor_db=None, note="YILDIZ AN V5–V7: müzik çekilir")])]),
    # c8: Aslanın İni — ciddi, diplomatik; 6/8 deniz. "Konuk muydu, rehine mi?" ve "O sırada Lorenzo Napoli'deydi." cümlelerinde müzik çekilir; sonda şube ışıkları sönüyor. (A dorian, 66 bpm)
    "c8": dict(mood="serious", tonic=45, mode="dorian", bpm=66, meter="6/8", level_db=0.0,
               arc=[(-1, .28), (0, .30), A("c8s1", .34), A("c8s3", .48), A("c8s5", .62), A("c8s6", .46), A("c8s7", .40), A("c8s9", .36), A("c8s10", .34),
                    A("c8s11", .18), A("c8s12", .28), A("c8s14", .34), A("c8s15", .46), A("c8s17", .40), A("c8s18", .20), A("c8s19", .10), A("c8s20", .26),
                    A("c8s21", .34), A("c8s22", .30), A("c8s23", .34), A("c8s24", .30), A("c8s25", .66), A("c8s26", .50), A("c8s27", .38), A("c8s28", .30),
                    A("c8s30", .32), A("c8s31", .30), A("c8s32", .26), A("c8s33", .24), A("c8s34", .22), (1.0, .14)],
               prog=[[(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "")], [(0, 1, ""), (3, 1, ""), (6, 1, ""), (3, 1, ""), (0, 2, "5"), (4, 2, "")]], b_thr=0.5,
               drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
               arp=dict(inst="lute", pattern="sea", lvl=0.65, lo=0.28, hi=0.40, p0=0.8, p1=0.2),
               bass=dict(inst="lute", pattern="drive", lvl=0.7, lo=0.40, hi=0.52, p=0.9),
               perc=dict(pattern="gallop", tef="lilt", lvl=0.8, lo=0.40, hi=0.52, pitch=92, amp=0.55,
                         win=[W("c8s3", END("c8s5", 0.0)), W("c8s25", END("c8s26", 0.0))]),
               choir=dict(inst="organ", stops=REED, lvl=0.45, lo=0.44, hi=0.58, voices=4, attack=0.6),
               melody=dict(inst="harp", lvl=0.55, lo=0.46, hi=0.56, play=2, rest=2, dens=0.3, reg=(64, 79), motif="agit"),
               events=[STOP(END("c8s9", -0.1)), STOP(END("c8s31", -0.1), hold=1.0),
                       E("lute", ("c8s34", "Londra", 0.0), deg=[7], vel=0.6, g=0.9), E("lute", ("c8s34", "Londra", 1.5), deg=[5], vel=0.5, g=0.85),
                       E("lute", ("c8s34", "Londra", 3.2), deg=[4], vel=0.42, g=0.8), E("lute", ("c8s34", "Londra", 5.2), deg=[2], vel=0.34, g=0.75),
                       E("lute", ("c8s34", "Londra", 7.6), deg=[0], vel=0.28, g=0.7)],
               gates=[GATE(("c8s11", 0.0), END("c8s11", -0.4), lead=0.3, rel=2.5, floor_db=-24, note="Konuk muydu, rehine mi?"),
                      GATE(("c8s19", -0.1), END("c8s19", 0.0), lead=0.3, rel=1.8, floor_db=None, note="O sırada Lorenzo Napoli'deydi")]),
    # c9: defter kapanıyor — kuru-hüzünlü; tık-tık defter, şubeler tek tek kapanır (inen lavta notaları), "güzellik kaldı"da sıcak akor, sonda tehdit. (G aeolian, 60 bpm)
    "c9": dict(mood="dry", tonic=43, mode="aeolian", bpm=60, meter="4/4", level_db=-0.5,
               arc=[(-1, .30), (0, .32), A("c9s1", .34), A("c9s3", .38), A("c9s6", .36), A("c9s7", .42), A("c9s8", .40), A("c9s10", .34), A("c9s11", .38),
                    A("c9s13", .32), A("c9s14", .30), A("c9s15", .26), A("c9s17", .34), A("c9s19", .30), A("c9s20", .36), A("c9s21", .30), A("c9s22", .26),
                    A("c9s24", .22), A("c9s25", .24), A("c9s26", .34), A("c9s27", .48), A("c9s28", .52), (1.0, .50)],
               prog=[[(0, 2, ""), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, "5"), (3, 2, ""), (4, 2, ""), (5, 2, "")]], b_thr=0.45,
               drone=dict(lvl=0.7, mode="roots", chunk_bars=2, fifth=False, bright=0.5),
               arp=dict(inst="harp", pattern="ledger", lvl=0.5, lo=0.22, hi=0.34, p0=0.9, p1=0.1, transpose=12),
               bass=dict(inst="lute", pattern="tick", lvl=0.7, lo=0.26, hi=0.38, p=0.95),
               choir=dict(inst="organ", stops=REED, lvl=0.45, lo=0.40, hi=0.55, voices=4, attack=0.7),
               melody=dict(inst="lute", lvl=0.7, lo=0.38, hi=0.48, play=2, rest=3, dens=0.2, reg=(57, 72), motif="dolasim"),
               events=[STOP(END("c9s9", -0.1)), STOP(END("c9s19", -0.1), hold=1.0), STOP(END("c9s20", -0.5), hold=0.7),
                       E("lute", END("c9s10", -0.8), deg=[4], vel=0.5, g=0.9), E("lute", END("c9s13", -0.8), deg=[2], vel=0.45, g=0.85),
                       E("lute", ("c9s14", "Milano", 0.0), deg=[7], vel=0.5, g=0.85), E("lute", ("c9s14", "Avignon", 0.0), deg=[5], vel=0.45, g=0.8),
                       E("lute", ("c9s14", "Brugge", 0.0), deg=[4], vel=0.4, g=0.8), E("lute", ("c9s14", "Venedik", 0.0), deg=[2], vel=0.35, g=0.75),
                       E("organ", ("c9s27", "güzellik", -0.2), midi=[43, 50, 55, 59, 62], vel=0.55, dur=5.0, attack=0.5, release=2.5, g=0.55),
                       E("choir", ("c9s27", "güzellik", 0.0), midi=[55, 62, 67, 71], vel=0.5, dur=5.0, attack=0.8, g=0.5, vowel="a"),
                       E("organ", "c9s28", dt=0.0, midi=[40, 47, 52], vel=0.5, dur=7.0, attack=1.4, g=0.5)]),
    # c10: Rahip ve Kral — AĞIR; E frigiyen. 9 Kasım (c10s13–c10s20): KISA VURUŞLAR, yatak yok, kapı tek hamlede, 1 sn sessizlik, uzak trompet (SFX). ÇAN YOK.
    # Ateş (c10s25–c10s30, c10s34): gece lapis → közer. "Dönüş" motifi (1434) geri sarılmış olarak c10s20'de. (E phrygian, 58 bpm)
    "c10": dict(mood="heavy", tonic=40, mode="phrygian", bpm=58, meter="4/4", level_db=-0.5,
                arc=[(-1, .22), (0, .22), A("c10s1", .20), A("c10s3", .24), A("c10s4", .28), A("c10s6", .30), A("c10s7", .34), A("c10s8", .46), A("c10s9", .50),
                     A("c10s10", .36), A("c10s11", .38), A("c10s12", .52), A("c10s13", .18), A("c10s14", .40), A("c10s15", .54), A("c10s16", .36),
                     A("c10s17", .22), A("c10s18", .40), A("c10s19", .30), A("c10s20", .40), A("c10s21", .60), A("c10s22", .66), A("c10s23", .50),
                     A("c10s24", .46), A("c10s25", .54), A("c10s26", .58), A("c10s27", .52), A("c10s28", .42), A("c10s29", .38), A("c10s30", .56),
                     A("c10s31", .50), A("c10s32", .48), A("c10s33", .52), A("c10s34", .60), A("c10s35", .30), A("c10s36", .28), (1.0, .18)],
                prog=[[(0, 2, "5"), (1, 2, ""), (0, 2, "5"), (5, 2, "")], [(0, 2, ""), (1, 2, ""), (6, 2, ""), (0, 2, "5")]], b_thr=0.5,
                drone=dict(lvl=0.85, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
                arp=dict(inst="lute", pattern="sparse", lvl=0.5, lo=0.18, hi=0.30, p0=0.8, p1=0.2),
                choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.44, hi=0.58, voices=4, attack=0.6),
                perc=dict(pattern="march", lvl=0.8, lo=0.36, hi=0.48, pitch=84, amp=0.6, win=[W("c10s21", END("c10s22", 0.0))]),
                theme=[TH("donus_ters", ("c10s20", "Şimdi", -0.1), inst="organ", vel=0.55, stretch=1.7, hold=True, g=0.9),
                       TH("donus_ters", ("c10s20", "Şimdi", -0.1), inst="lute", vel=0.55, stretch=1.7, oct=0, g=0.9),
                       TH("bedel", "c10s34", dt=1.0, inst="gamba", vel=0.6, bend=-35, g=1.0),
                       TH("florin3", ("c10s36", "ordunun", 0.0), inst="lute", vel=0.45, stretch=1.3, g=0.8)],
                events=[E("timp", "c10s13", dt=0.1, f=54.0, vel=0.85, dur=3.0, g=0.7),
                        E("dum", ("c10s14", "Palazzo", 0.0), vel=0.7, f=80, g=0.6), E("tek", ("c10s14", "girmek", 0.0), vel=0.6, f=80, g=0.5),
                        E("seq", ("c10s15", "kapandı", -0.05), hits=[(0.0, "timp", 1.0), (0.0, "dum", 1.0), (0.10, "tek", .6)], f=84.0, tf=54.0, g=0.85),
                        E("tek", ("c10s16", "saat", 0.0), vel=0.55, f=84, g=0.45), E("tek", ("c10s16", "saat", 0.42), vel=0.5, f=84, g=0.4),
                        E("dum", ("c10s18", "özgürlük", -0.5), vel=0.6, f=84, g=0.5), E("dum", ("c10s18", "özgürlük", 0.0), vel=0.7, f=84, g=0.55),
                        STOP(("c10s22", "yırttı", 0.0), hold=1.1), STOP(END("c10s28", -0.1)),
                        E("organ", "c10s25", dt=0.0, deg=[0, 4], oct=0, vel=0.5, dur=8.0, attack=1.0, g=0.5),
                        E("gamba", "c10s36", dt=0.3, deg=[0], oct=0, vel=0.55, dur=7.0, attack=1.0, bend=-30, g=0.6)],
                gates=[GATE(("c10s15", "kapandı", 0.30), ("c10s15", "kapandı", 1.7), lead=0.05, rel=0.5, floor_db=None, note="kapı çarptı: 1 sn sessizlik (uzak trompet = SFX)"),
                       GATE(END("c10s34", 0.0), END("c10s35", 0.0), lead=0.4, rel=2.5, floor_db=-20, note="küller Arno'ya")]),
    # c11: Papa Oğulları — üç kesit: [Prato: ağır] → [Leo X alayı: görkemli-ironik, mizah V2–V3] → [Roma 1527 → kuşatma → Alessandro: ağır, sonda sessizlik]. P5 sonu: end_kind='p2' kapanışı (çözülmeyen sus4; P6'nın 'miras' hücresine köprü).
    "c11": dict(mood="heavy", tonic=38, mode="phrygian", bpm=54, meter="4/4", level_db=-1.0,
                sections=[
                    dict(until=(END("c11s3", 0.0), 0.12), xf=4.0, mood="heavy", mode="phrygian", bpm=54, level_db=-1.0,
                         arc=[(-1, .26), (0, .30), A("c11s1", .32), A("c11s2", .40), A("c11s3", .36), (1.0, .34)],
                         prog=[[(0, 2, "5"), (1, 2, ""), (0, 2, "5"), (6, 2, "")], [(0, 2, ""), (1, 2, ""), (6, 2, ""), (0, 2, "5")]], b_thr=0.38,
                         drone=dict(lvl=0.85, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
                         choir=dict(inst="organ", stops=REED, lvl=0.45, lo=0.30, hi=0.42, voices=4, attack=0.6),
                         arp=dict(inst="lute", pattern="sparse", lvl=0.5, lo=0.20, hi=0.30, p0=0.8, p1=0.2),
                         events=[E("timp", "c11s1", dt=0.3, f=54.0, vel=0.75, dur=3.0, g=0.5)]),
                    dict(until=(END("c11s13", 0.0), 0.30), xf=4.0, mood="epic", mode="mixolydian", bpm=80, level_db=0.0,
                         arc=[(-1, .30), (0, .34), A("c11s4", .42), A("c11s5", .54), A("c11s6", .52), A("c11s7", .40), A("c11s8", .34), A("c11s9", .46),
                              A("c11s10", .50), A("c11s11", .42), A("c11s12", .44), A("c11s13", .22), (1.0, .20)],
                         prog=[[(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "")], [(0, 2, ""), (3, 2, ""), (4, 2, ""), (0, 2, "")]], b_thr=0.4,
                         drone=dict(lvl=0.55, chunk_bars=4, fifth=True),
                         arp=dict(inst="harp", pattern="florin", lvl=0.6, lo=0.30, hi=0.42, p0=0.85, p1=0.15),
                         arp2=dict(inst="lute", pattern="pavane", lvl=0.5, lo=0.34, hi=0.46, p0=0.8, p1=0.2),
                         choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.46, hi=0.58, voices=4, attack=0.4),
                         perc=dict(pattern="ceremony", tef="sparse", lvl=0.7, lo=0.40, hi=0.52, pitch=96, amp=0.55, win=[W("c11s5", END("c11s6", 0.0))]),
                         melody=dict(inst="harp", lvl=0.6, lo=0.40, hi=0.50, play=2, rest=2, dens=0.4, reg=(66, 81), motif="florin"),
                         events=[STOP(END("c11s6", -0.1), hold=0.8), STOP(END("c11s10", -0.1), hold=1.0), STOP(END("c11s12", -0.1))]),
                    dict(mood="heavy", mode="aeolian", bpm=52, level_db=-1.5, end_kind="p2", snr_bias=0.5,
                         arc=[(-1, .22), (0, .30), A("c11s14", .38), A("c11s15", .50), A("c11s16", .56), A("c11s17", .60), A("c11s18", .50), A("c11s19", .44),
                              A("c11s20", .40), A("c11s21", .34), A("c11s22", .30), A("c11s23", .26), A("c11s24", .44), A("c11s25", .50), A("c11s26", .54),
                              A("c11s27", .46), A("c11s28", .62), A("c11s29", .50), A("c11s30", .36), A("c11s31", .30), A("c11s32", .30), A("c11s33", .24),
                              A("c11s34", .30), A("c11s35", .20), A("c11s36", .20), A("c11s37", .16), A("c11s38", .12), (1.0, .10)],
                         prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, ""), (3, 2, ""), (4, 2, "5"), (5, 2, "")]], b_thr=0.5,
                         drone=dict(lvl=0.9, mode="roots", chunk_bars=2, fifth=True, bright=0.5),
                         choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.40, hi=0.55, voices=4, attack=0.7),
                         arp=dict(inst="lute", pattern="sparse", lvl=0.5, lo=0.18, hi=0.30, p0=0.8, p1=0.2),
                         bass=dict(inst="lute", pattern="pedal", lvl=0.7, lo=0.36, hi=0.48),
                         perc=dict(pattern="proc2", lvl=0.8, lo=0.40, hi=0.50, pitch=80, amp=0.6, win=[W("c11s15", END("c11s19", 0.0)), W("c11s24", END("c11s29", 0.0))]),
                         events=[E("dum", ("c11s17", "yüz", 0.0), vel=0.7, f=80, g=0.5), E("dum", ("c11s17", "yedisi", 0.0), vel=0.6, f=80, g=0.45),
                                 E("dum", ("c11s18", "kırk", 0.0), vel=0.5, f=80, g=0.4),
                                 E("timp", ("c11s28", "kurşun", 0.0), f=54.0, vel=0.7, dur=2.8, g=0.45),
                                 E("lute", ("c11s31", "çıktı", 0.0), deg=[0, 2, 4], oct=1, strum=0.18, vel=0.45, g=0.8),
                                 E("lute", ("c11s33", "vaat", 0.0), deg=[0, 4], oct=0, strum=0.5, vel=0.4, g=0.7),
                                 E("gamba", ("c11s33", "uyuyakalmıştı", 0.0), deg=[0], oct=0, vel=0.45, dur=6.0, attack=1.2, bend=-25, g=0.6),
                                 E("dum", ("c11s34", "döndü", 0.0), vel=0.55, f=76, g=0.5), E("dum", ("c11s34", "öldürdüler", 0.0), vel=0.6, f=76, g=0.5)],
                         gates=[GATE(END("c11s34", -1.0), END("c11s35", -0.6), lead=0.6, rel=3.0, floor_db=None, note="kısa olay → sessizlik")])]),

    # ───────────────────────────── MİRAS perdesi (c12–c16) ─────────────────────────────
    # c12: Dük — soğukkanlı-otoriter; makine gibi tık-tık + org pedalı; Uffizi kendini kurar; 1562 (c12s19–c12s25) AĞIR: neredeyse sessizlik, "dört haftada üç ölüm"de tam sessizlik;
    # Lepanto saygılı-nötr (zafer fanfarı yok). P6 açılışı (t=0): 'miras' hücresi (lavta). (A aeolian, 66 bpm)
    "c12": dict(mood="cold", tonic=45, mode="aeolian", bpm=66, meter="4/4", level_db=0.0,
                arc=[(-1, .30), (0, .34), A("c12s1", .36), A("c12s3", .42), A("c12s4", .50), A("c12s5", .44), A("c12s7", .38), A("c12s9", .40), A("c12s10", .46),
                     A("c12s11", .52), A("c12s13", .50), A("c12s14", .58), A("c12s15", .50), A("c12s16", .56), A("c12s18", .58), A("c12s19", .22), A("c12s22", .12),
                     A("c12s24", .14), A("c12s25", .10), A("c12s26", .30), A("c12s28", .42), A("c12s29", .40), A("c12s31", .38), A("c12s32", .50), A("c12s33", .42),
                     A("c12s34", .28), A("c12s35", .40), (1.0, .38)],
                prog=[[(0, 2, "5"), (6, 2, ""), (5, 2, ""), (6, 2, "")], [(0, 2, ""), (3, 2, ""), (4, 2, "5"), (0, 2, "")]], b_thr=0.5,
                drone=dict(lvl=0.8, mode="roots", chunk_bars=2, fifth=True),
                arp=dict(inst="harp", pattern="tick", lvl=0.6, lo=0.22, hi=0.34, p0=0.85, p1=0.1, transpose=12),
                bass=dict(inst="lute", pattern="tick", lvl=0.7, lo=0.28, hi=0.40),
                choir=dict(inst="organ", stops=REED, lvl=0.5, lo=0.50, hi=0.62, voices=4, attack=0.5),
                melody=dict(inst="lute", lvl=0.6, lo=0.44, hi=0.54, play=2, rest=2, dens=0.3, reg=(57, 72), motif="sorgu"),
                perc=dict(pattern="march", lvl=0.7, lo=0.44, hi=0.56, pitch=94, amp=0.55, win=[W("c12s16", END("c12s18", 0.0)), W("c12s32", END("c12s33", 0.0))]),
                theme=[TH("miras", "c12s1", dt=0.8, inst="lute", vel=0.5, g=0.9),
                       TH("miras", ("c12s28", "güzelliği", 0.0), inst="organ", vel=0.5, hold=True, g=0.8)],
                events=[STOP(END("c12s7", -0.1)), STOP(END("c12s13", -0.1), hold=1.0), STOP(END("c12s31", -0.1), hold=1.0)],
                gates=[GATE(("c12s19", 0.0), END("c12s25", 0.0), lead=0.6, rel=3.0, floor_db=-30, note="1562: neredeyse sessizlik"),
                       GATE(("c12s22", "haftada", -0.2), END("c12s22", 0.2), lead=0.4, rel=2.0, floor_db=None, note="dört haftada üç ölüm: tam sessizlik")]),
    # c13: İki Kraliçe — iki kesit: [Catherine: A aeolian, 1572'de neredeyse sessizlik, mit endüstrisinde kuru duraklar] → [Marie: C lidyen, Rubens galerisi görkemli-ironik, Köln'de soğuk sessizlik]
    "c13": dict(mood="duo", tonic=45, mode="aeolian", bpm=60, meter="4/4", level_db=0.0,
                sections=[
                    dict(until=(END("c13s22", 0.0), 0.55), xf=4.0, mood="duo", mode="aeolian", bpm=60, meter="4/4", tonic=45,
                         arc=[(-1, .28), (0, .32), A("c13s1", .40), A("c13s4", .44), A("c13s5", .38), A("c13s6", .42), A("c13s7", .34), A("c13s8", .26),
                              A("c13s9", .38), A("c13s10", .40), A("c13s11", .16), A("c13s13", .10), A("c13s14", .10), A("c13s15", .34), A("c13s16", .36),
                              A("c13s17", .46), A("c13s18", .42), A("c13s20", .44), A("c13s21", .56), A("c13s22", .24), (1.0, .22)],
                         prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, ""), (3, 2, ""), (6, 2, ""), (5, 2, "")]], b_thr=0.45,
                         drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
                         arp=dict(inst="lute", pattern="sparse", lvl=0.6, lo=0.22, hi=0.34, p0=0.8, p1=0.2),
                         arp2=dict(inst="harp", pattern="ledger", lvl=0.5, lo=0.34, hi=0.46, p0=0.9, p1=0.1, transpose=12, win=[W("c13s15", END("c13s20", 0.0))]),
                         choir=dict(inst="choir", vowel=("o", "a"), lvl=0.55, lo=0.34, hi=0.46, voices=4),
                         bass=dict(inst="lute", pattern="walk", lvl=0.6, lo=0.40, hi=0.52),
                         perc=dict(pattern="palle", lvl=0.7, lo=0.28, hi=0.40, pitch=92, amp=0.5, win=[W("c13s5", END("c13s6", 0.0)), W("c13s21", END("c13s21", 0.0))]),
                         theme=[TH("bedel", "c13s7", dt=3.0, inst="gamba", vel=0.5, bend=-30, g=0.8),
                                dict(notes=[(0, 2), (2, 2), (4, 2), (7, 6)], at=("c13s21", "gerçek", 0.0), inst="harp", vel=0.6, g=0.9)],
                         events=[STOP(END("c13s17", -0.1), hold=1.0), STOP(END("c13s20", -0.1)), STOP(("c13s19", "yüzyıla", 0.0), hold=0.7)],
                         gates=[GATE(END("c13s7", -2.0), END("c13s7", 0.0), lead=0.3, rel=2.0, floor_db=None, note="Henri'nin ölümü: dip, sessizlik"),
                                GATE(("c13s11", 0.0), END("c13s14", -3.0), lead=0.6, rel=1.5, floor_db=-30, note="1572: ses çekilir"),
                                GATE(END("c13s14", -3.0), END("c13s14", 0.0), lead=0.3, rel=2.0, floor_db=None, note="1572: tam sessizlik 3 sn")]),
                    dict(mood="duo", mode="lydian", bpm=72, meter="3/4", tonic=48, level_db=0.0,
                         arc=[(-1, .30), (0, .34), A("c13s23", .40), A("c13s25", .46), A("c13s26", .50), A("c13s27", .46), A("c13s28", .50), A("c13s29", .46),
                              A("c13s30", .42), A("c13s31", .34), A("c13s32", .62), A("c13s33", .56), A("c13s34", .60), A("c13s35", .22), A("c13s36", .18),
                              A("c13s37", .22), A("c13s38", .30), (1.0, .26)],
                         prog=[[(0, 2, ""), (1, 2, ""), (0, 2, "add9"), (4, 2, "")], [(0, 2, ""), (4, 2, ""), (5, 2, ""), (1, 2, "")]], b_thr=0.45,
                         drone=dict(lvl=0.55, chunk_bars=4, fifth=True, bright=0.6),
                         arp=dict(inst="lute", pattern="pavane", lvl=0.65, lo=0.26, hi=0.38, p0=0.8, p1=0.2),
                         arp2=dict(inst="harp", pattern="florin", lvl=0.5, lo=0.46, hi=0.56, p0=0.8, p1=0.2, transpose=12),
                         choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.5, lo=0.46, hi=0.58, voices=4, attack=0.5),
                         melody=dict(inst="harp", lvl=0.6, lo=0.44, hi=0.54, play=2, rest=2, dens=0.35, reg=(66, 81), motif="florin"),
                         perc=dict(pattern="light", tef="light", lvl=0.5, lo=0.52, hi=0.62, pitch=100, amp=0.45),
                         events=[STOP(END("c13s26", -0.1), hold=1.0), STOP(END("c13s32", -0.2), hold=0.8),
                                 E("harp", ("c13s38", "gökyüzüne", 0.0), deg=[9, 11], oct=1, vel=0.4, strum=0.4, g=0.8),
                                 E("harp", ("c13s38", "yazdırıyordu", 0.0), deg=[14], oct=1, vel=0.35, g=0.7)],
                         gates=[GATE(("c13s35", 0.0), END("c13s37", 0.0), lead=0.5, rel=3.0, floor_db=-28, note="Köln: oda sessizliği")])]),
    # c14: Yıldızlar, Notalar, Taşlar — üç kesit: [matbaa/sert taş: parlak-meraklı F lidyen] → [Euridice: özgün recitativo-tarzı süreklilik (klavsen+lavta+gamba), D dorian] →
    # [Galileo'nun yıldızları (dört uydu), 1633 AĞIR süssüz, Cristofori envanteri, azalan satırlar]
    "c14": dict(mood="bright", tonic=41, mode="lydian", bpm=66, meter="3/4", level_db=0.0,
                sections=[
                    dict(until=(END("c14s6", 0.0), 0.16), xf=4.0, mood="bright", mode="lydian", bpm=66, meter="3/4", tonic=41,
                         arc=[(-1, .30), (0, .36), A("c14s1", .42), A("c14s2", .48), A("c14s3", .46), A("c14s4", .44), A("c14s5", .40), A("c14s6", .50), (1.0, .46)],
                         prog=[[(0, 2, ""), (1, 2, ""), (0, 2, "add9"), (4, 2, "")], [(0, 2, ""), (4, 2, ""), (5, 2, ""), (1, 2, "")]], b_thr=0.4,
                         drone=dict(lvl=0.5, chunk_bars=4, fifth=True, bright=0.6),
                         arp=dict(inst="harp", pattern="florin", lvl=0.55, lo=0.30, hi=0.42, p0=0.85, p1=0.15, transpose=12),
                         arp2=dict(inst="lute", pattern="pavane", lvl=0.6, lo=0.34, hi=0.46, p0=0.8, p1=0.2),
                         choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.4, lo=0.44, hi=0.56, voices=4, attack=0.5),
                         melody=dict(inst="lute", lvl=0.6, lo=0.40, hi=0.50, play=2, rest=2, dens=0.35, reg=(64, 79), motif="florin"),
                         perc=dict(pattern="light", tef="light", lvl=0.5, lo=0.42, hi=0.52, pitch=104, amp=0.45),
                         events=[STOP(END("c14s4", -0.1), hold=0.9)]),
                    dict(until=(END("c14s11", 0.0), 0.50), xf=4.0, mood="bright", mode="dorian", bpm=54, meter="4/4", tonic=38, level_db=-0.5,
                         arc=[(-1, .30), (0, .38), A("c14s7", .46), A("c14s8", .50), A("c14s9", .50), A("c14s10", .46), A("c14s11", .40), (1.0, .38)],
                         prog=[[(0, 2, ""), (3, 2, ""), (0, 2, "sus2"), (6, 2, "")], [(0, 2, "add9"), (4, 2, ""), (3, 2, ""), (0, 2, "")]], b_thr=0.5,
                         drone=dict(lvl=0.45, chunk_bars=4, fifth=True, bright=0.55),
                         choir=dict(inst="organ", stops=(("flute", 1.0, 1.0), ("flute", 0.3, 2.0)), lvl=0.35, lo=0.30, hi=0.42, voices=3, attack=0.7),
                         recit=dict(inst="harp", lvl=1.0, lo=0.20, hi=0.30, tone=4, tempo=1.0, gap=(1.2, 2.6), reg=(62, 80), bass_g=0.7, chord_g=0.8),
                         events=[STOP(END("c14s10", -0.1), hold=1.0)]),
                    dict(mood="bright", mode="lydian", bpm=60, meter="3/4", tonic=41, level_db=-0.5,
                         arc=[(-1, .30), (0, .38), A("c14s12", .46), A("c14s13", .50), A("c14s14", .62), A("c14s15", .52), A("c14s16", .46), A("c14s17", .40),
                              A("c14s18", .26), A("c14s19", .22), A("c14s20", .36), A("c14s21", .46), A("c14s22", .44), A("c14s23", .40), A("c14s24", .36),
                              A("c14s25", .34), A("c14s26", .20), (1.0, .14)],
                         prog=[[(0, 2, ""), (1, 2, ""), (0, 2, "add9"), (4, 2, "")], [(0, 2, ""), (4, 2, ""), (5, 2, ""), (1, 2, "")]], b_thr=0.42,
                         drone=dict(lvl=0.5, chunk_bars=4, fifth=True, bright=0.6),
                         arp=dict(inst="harp", pattern="florin", lvl=0.5, lo=0.30, hi=0.42, p0=0.85, p1=0.15, transpose=12),
                         arp2=dict(inst="lute", pattern="pavane", lvl=0.6, lo=0.34, hi=0.46, p0=0.8, p1=0.2, win=[W("c14s20", END("c14s25", 0.0))]),
                         choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.45, lo=0.46, hi=0.58, voices=4, attack=0.5),
                         melody=dict(inst="harp", lvl=0.55, lo=0.44, hi=0.54, play=2, rest=2, dens=0.35, reg=(66, 82), motif="dolasim"),
                         theme=[dict(motif="yildiz", notes=[(7, 2), (9, 2), (11, 2)], at=("c14s12", "üç", -0.2), inst="harp", vel=0.55, oct=1, stretch=1.7, g=0.9),
                                dict(notes=[(14, 6)], at=("c14s12", "dörde", 0.0), inst="harp", vel=0.6, oct=1, g=0.9),
                                TH("bedel", "c14s18", dt=0.5, inst="gamba", vel=0.5, bend=-30, g=0.9)],
                         events=[E("organ", ("c14s14", "yıldızları", -0.3), midi=[41, 48, 53, 57, 60, 64], vel=0.5, dur=6.0, attack=0.6, release=2.4, g=0.5),
                                 STOP(END("c14s17", -0.1), hold=0.9), STOP(END("c14s24", -0.1), hold=1.0)],
                         gates=[GATE(("c14s18", 0.0), END("c14s19", 0.0), lead=0.5, rel=3.0, floor_db=-16, note="1633: süssüz"),
                                GATE(END("c14s26", -2.5), END("c14s26", 0.0), lead=0.5, rel=2.0, floor_db=-14, note="envanter satırları azalıyor")])]),
    # c15: Son Medici'ler — yorgun, seyrek; üç katmanlı ölçek (2006 → 2010 → 2026) yükselen üç nota; aile ağacı: inen notalar; "bir kadın ve imzalanacak bir sözleşme" → miras hücresi. (A aeolian, 54 bpm)
    "c15": dict(mood="weary", tonic=45, mode="aeolian", bpm=54, meter="4/4", level_db=-2.0, snr_bias=1.0,
                arc=[(-1, .24), (0, .26), A("c15s1", .30), A("c15s2", .28), A("c15s3", .26), A("c15s4", .32), A("c15s5", .40), A("c15s6", .30), A("c15s7", .32),
                     A("c15s8", .30), A("c15s9", .36), A("c15s10", .34), A("c15s11", .36), A("c15s13", .30), A("c15s14", .34), A("c15s15", .28), A("c15s16", .26),
                     A("c15s17", .22), A("c15s18", .20), A("c15s19", .22), (1.0, .18)],
                prog=[[(0, 2, "5"), (5, 2, ""), (6, 2, ""), (0, 2, "5")], [(0, 2, ""), (3, 2, ""), (4, 2, "5"), (5, 2, "")]], b_thr=0.5,
                drone=dict(lvl=0.6, chunk_bars=4, fifth=True, bright=0.5),
                arp=dict(inst="lute", pattern="sparse", lvl=0.5, lo=0.22, hi=0.32, p0=0.75, p1=0.2),
                choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.35, lo=0.26, hi=0.36, voices=4, attack=0.8),
                melody=dict(inst="lute", lvl=0.55, lo=0.28, hi=0.38, play=1, rest=3, dens=0.15, reg=(57, 70), motif="dolasim"),
                theme=[TH("bedel", END("c15s2", 0.0), dt=0.2, inst="gamba", vel=0.45, bend=-30, g=0.8),
                       TH("bedel", ("c15s17", "öldü", 0.0), inst="gamba", vel=0.5, bend=-35, g=0.9),
                       TH("miras", ("c15s19", "kadın", -0.3), inst="lute", vel=0.5, stretch=1.3, g=0.9)],
                events=[E("lute", ("c15s4", "2006", 0.0), deg=[0], oct=1, vel=0.5, g=0.8), E("lute", ("c15s4", "2010", 0.0), deg=[2], oct=1, vel=0.5, g=0.8),
                        E("harp", ("c15s5", "2026", 0.0), deg=[4, 7], oct=2, vel=0.45, strum=0.25, g=0.9),
                        STOP(END("c15s1", -0.1)), STOP(END("c15s6", -0.1), hold=1.0), STOP(END("c15s14", -0.1)),
                        E("lute", ("c15s17", "kendi", 0.0), deg=[4], oct=0, vel=0.4, g=0.8), E("lute", ("c15s18", "Viyana", 0.0), deg=[2], oct=0, vel=0.34, g=0.75)]),
    # c16: Hesap — üç kesit: [c0'ın odasına dönüş: D dorian, 'miras' hücresi TERS ÇEVRİLMİŞ] → [kuşkucu orta: hafif, kuru; sağlamlık haritası] → [sessiz kapanış, çözülüş; son sessizlik].
    "c16": dict(mood="solemn", tonic=38, mode="dorian", bpm=58, meter="4/4", level_db=0.0,
                sections=[
                    dict(until=(END("c16s6", 0.0), 0.20), xf=4.0, mood="solemn", mode="dorian", bpm=58, meter="4/4", tonic=38,
                         arc=[(-1, .05), (0, .08), A("c16s1", .10), A("c16s3", .16), A("c16s4", .18), A("c16s5", .30), A("c16s6", .22), (1.0, .20)],
                         prog=[[(0, 2, "5"), (6, 2, "5"), (0, 2, "sus2"), (3, 2, "5")], [(0, 2, "sus2"), (6, 2, ""), (4, 2, "5"), (3, 2, "")]], b_thr=0.5,
                         drone=dict(lvl=1.0, chunk_bars=2, fifth=True),
                         choir=dict(inst="choir", vowel=("o", "a"), lvl=0.4, lo=0.14, hi=0.5, voices=4),
                         theme=[TH("miras", "c16s1", dt=0.8, inst="lute", vel=0.55, invert=True),
                                TH("miras", ("c16s5", "çıkmayacak", -0.6), inst="lute", vel=0.55, invert=True, stretch=1.2),
                                TH("miras", ("c16s5", "çıkmayacak", -0.6), inst="organ", vel=0.45, invert=True, stretch=1.2, hold=True, g=0.7)]),
                    dict(until=(END("c16s21", 0.0), 0.82), xf=4.0, mood="dry", mode="mixolydian", bpm=72, meter="4/4", tonic=38, level_db=-0.5,
                         arc=[(-1, .26), (0, .30), A("c16s7", .38), A("c16s8", .42), A("c16s9", .46), A("c16s10", .44), A("c16s12", .46), A("c16s13", .48),
                              A("c16s14", .50), A("c16s16", .50), A("c16s17", .46), A("c16s18", .42), A("c16s20", .46), A("c16s21", .36), (1.0, .30)],
                         prog=[[(0, 2, ""), (6, 2, ""), (3, 2, ""), (0, 2, "")], [(0, 2, ""), (3, 2, ""), (4, 2, ""), (0, 2, "")]], b_thr=0.45,
                         drone=dict(lvl=0.55, chunk_bars=4, fifth=True),
                         arp=dict(inst="harp", pattern="ledger", lvl=0.55, lo=0.28, hi=0.40, p0=0.85, p1=0.1, transpose=12),
                         arp2=dict(inst="lute", pattern="pavane", lvl=0.55, lo=0.36, hi=0.46, p0=0.8, p1=0.2),
                         bass=dict(inst="lute", pattern="tick", lvl=0.6, lo=0.34, hi=0.46),
                         choir=dict(inst="organ", stops=STOP_OPEN, lvl=0.4, lo=0.44, hi=0.56, voices=4, attack=0.5),
                         melody=dict(inst="lute", lvl=0.6, lo=0.40, hi=0.50, play=2, rest=2, dens=0.3, reg=(57, 72), motif="defter"),
                         events=[STOP(END("c16s7", -0.1), hold=0.8), STOP(END("c16s14", -0.1)), STOP(END("c16s16", -0.1)), STOP(END("c16s17", -0.1), hold=1.0)]),
                    dict(mood="solemn", mode="dorian", bpm=54, meter="4/4", tonic=38, level_db=-0.5, end_kind="p3",
                         arc=[(-1, .24), (0, .26), A("c16s22", .28), A("c16s23", .34), A("c16s24", .30), A("c16s25", .34), (1.0, .30)],
                         prog=[[(0, 2, "5"), (6, 2, ""), (3, 2, ""), (0, 2, "sus2")], [(0, 2, "add9"), (4, 2, ""), (3, 2, ""), (0, 2, "")]], b_thr=0.5,
                         drone=dict(lvl=0.8, chunk_bars=4, fifth=True),
                         choir=dict(inst="choir", vowel=("o", "a"), lvl=0.5, lo=0.22, hi=0.34, voices=4),
                         arp=dict(inst="lute", pattern="sparse", lvl=0.55, lo=0.22, hi=0.32, p0=0.8, p1=0.2),
                         theme=[TH("miras", "c16s23", dt=0.5, inst="lute", vel=0.5, invert=True, g=0.9),
                                TH("miras", ("c16s25", "şehir", -2.2), inst="lute", vel=0.5, invert=True, stretch=1.3, g=0.9)])]),
}


if __name__ == "__main__":
    main()
