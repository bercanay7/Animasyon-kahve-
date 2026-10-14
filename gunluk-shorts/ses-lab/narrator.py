"""
Klas ama heyecanlı Türkçe anlatıcı (ücretsiz, çevrimdışı): Piper VITS + sherpa-onnx + stüdyo işleme.

  render(sentences, out_dir, voice="dfki", profile=PROFILE)  →  out/voice.wav + out/timeline.json

Metin işareti:  gösterilen=söylenen   *vurgulu kelimeler*   (virgül/iki nokta → ifade sınırı, ayrı sentezlenir)
İşleme: ifade bazlı sentez (doğal duraklar), vurgulu kelimelerde enerji ve parlaklık, derin/sıcak EQ,
        gerçek kompresör (attack/release), hafif oda yankısı. Perde yükseltme YOK (cızırtılı/ince ses yapar).
"""
import glob, json, os, re, wave
from fractions import Fraction
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve, resample_poly, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "ses-modelleri")
SR = 48000

PROFILE = dict(
    speed=1.06,          # genel tempo
    pitch=0.985,         # <1: biraz daha derin/otoriter
    noise_scale=0.60,    # düşük: temiz, kararlı ses
    noise_scale_w=0.70,
    gap_comma=0.11, gap_colon=0.16, gap_end=0.0,
    emph_gain_db=3.0, emph_bright_db=3.0,
    excl_boost_db=1.5,   # '!' biten ifadelerde ek enerji
    q_rise=0.04,         # '?' sonunda hafif yükselen ton (oran)
    reverb_wet=0.085, reverb_time=0.55,
    f0_scale=1.0, formant=1.0,   # kadın sesi: f0_scale≈1.65, formant≈1.17 (pyworld ile cinsiyet dönüşümü)
)


def syl(s):
    return max(1, sum(ch in "aeıioöuüAEIİOÖUÜ" for ch in s))


LEX = {}   # telaffuz sözlüğü: yazılış -> söylenen (ör. "yığılanlar": "yıılanlar")


def parse(text):
    toks, emph = [], False
    for raw in text.split(" "):
        starts = raw.startswith("*")
        ends = raw.rstrip(",:.!?").endswith("*")
        if starts:
            emph = True
        e0 = emph
        raw = raw.replace("*", "")
        m0 = re.search(r"([,:.!?]+)$", raw)
        tail = m0.group(1) if m0 else ""
        core = raw[: len(raw) - len(tail)] if tail else raw
        show, say = core.split("=", 1) if "=" in core else (core, core)
        if "=" not in core and core.lower() in LEX:
            say = LEX[core.lower()]
        toks.append(dict(show=(show + tail).replace("_", " "), say=(say + tail).replace("_", " "), emph=e0, punct=tail))
        if ends:
            emph = False
    return toks


def chunks_of(toks):
    out, cur = [], []
    for t in toks:
        cur.append(t)
        if t["punct"]:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def load_tts(voice, profile):
    import sherpa_onnx
    d = glob.glob(os.path.join(MODELS, f"ex_{voice}", "*"))[0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d + "/*.onnx")[0], tokens=d + "/tokens.txt", data_dir=d + "/espeak-ng-data",
                                                    noise_scale=profile["noise_scale"], noise_scale_w=profile["noise_scale_w"]), num_threads=4))
    return sherpa_onnx.OfflineTts(cfg)


def _trim(y, thr=0.01, pad=0.012):
    idx = np.where(np.abs(y) > thr)[0]
    if len(idx) == 0:
        return y
    return y[max(0, idx[0] - int(pad * SR)): min(len(y), idx[-1] + int(pad * SR))]


def _pitch_glide(y, k0, k1):
    """Süre boyunca perde oranı k0→k1 (zamanla değişen yeniden örnekleme); k>1 daha ince/yüksek"""
    n = len(y)
    rate = np.linspace(k0, k1, n)
    pos = np.cumsum(rate)
    pos = pos[pos < n - 1]
    return np.interp(pos, np.arange(n), y)


def _shelf(y, f0, gain_db, kind="low", q=0.707):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    cw, sw = np.cos(w0), np.sin(w0)
    al = sw / (2 * q)
    if kind == "low":
        b0 = A * ((A + 1) - (A - 1) * cw + 2 * np.sqrt(A) * al); b1 = 2 * A * ((A - 1) - (A + 1) * cw); b2 = A * ((A + 1) - (A - 1) * cw - 2 * np.sqrt(A) * al)
        a0 = (A + 1) + (A - 1) * cw + 2 * np.sqrt(A) * al; a1 = -2 * ((A - 1) + (A + 1) * cw); a2 = (A + 1) + (A - 1) * cw - 2 * np.sqrt(A) * al
    else:
        b0 = A * ((A + 1) + (A - 1) * cw + 2 * np.sqrt(A) * al); b1 = -2 * A * ((A - 1) + (A + 1) * cw); b2 = A * ((A + 1) + (A - 1) * cw - 2 * np.sqrt(A) * al)
        a0 = (A + 1) - (A - 1) * cw + 2 * np.sqrt(A) * al; a1 = 2 * ((A - 1) - (A + 1) * cw); a2 = (A + 1) - (A - 1) * cw - 2 * np.sqrt(A) * al
    return lfilter([b0 / a0, b1 / a0, b2 / a0], [1, a1 / a0, a2 / a0], y)


def _peak(y, f0, gain_db, q=1.0):
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * f0 / SR
    al = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    b = [1 + al * A, -2 * cw, 1 - al * A]
    a = [1 + al / A, -2 * cw, 1 - al / A]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], y)


def compress(y, thr_db=-26.0, ratio=3.2, attack=0.004, release=0.14, makeup_db=7.0):
    thr = 10 ** (thr_db / 20)
    a_a = np.exp(-1 / (attack * SR))
    a_r = np.exp(-1 / (release * SR))
    env = 0.0
    g = np.empty(len(y))
    ab = np.abs(y)
    for i in range(len(y)):
        x = ab[i]
        env = a_a * env + (1 - a_a) * x if x > env else a_r * env + (1 - a_r) * x
        if env > thr:
            g[i] = (env / thr) ** (1 / ratio - 1)
        else:
            g[i] = 1.0
    return y * g * 10 ** (makeup_db / 20)


def studio(y, profile):
    y = sosfilt(butter(2, 70, "high", fs=SR, output="sos"), y)
    y = _shelf(y, 190, 2.4, "low")           # sıcaklık
    y = _peak(y, 3200, 2.0, 0.9)             # netlik
    y = _shelf(y, 7500, -2.5, "high")        # tizi yumuşat (sibilans)
    y = compress(y)
    # hafif oda yankısı
    n = int(profile["reverb_time"] * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    ir = rng.standard_normal(n) * np.exp(-t / (profile["reverb_time"] / 4.5))
    ir = sosfilt(butter(2, 5200, "low", fs=SR, output="sos"), ir)
    ir[: int(0.012 * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(y, ir)[: len(y)]
    return y * (1 - profile["reverb_wet"] * 0.5) + wet * profile["reverb_wet"] * 1.6


def _gender(x, sr, f0_scale, formant):
    """WORLD vokoder: perde (f0) ve ses yolu (formant) ayrı ölçeklenir → doğal kadın/erkek dönüşümü"""
    import pyworld as pw
    x = np.ascontiguousarray(x, dtype=np.float64)
    f0, t = pw.harvest(x, sr, f0_floor=60.0, f0_ceil=400.0, frame_period=5.0)
    sp = pw.cheaptrick(x, f0, t, sr)
    ap = pw.d4c(x, f0, t, sr)
    if abs(formant - 1.0) > 1e-3:
        nb = sp.shape[1]
        src = np.clip(np.arange(nb) / formant, 0, nb - 1)
        sp = np.stack([np.interp(src, np.arange(nb), r) for r in sp])
    y = pw.synthesize(f0 * f0_scale, sp, ap, sr, frame_period=5.0)
    return y * (np.max(np.abs(x)) / (np.max(np.abs(y)) + 1e-9))


def synth_chunk(tts, toks, speed, pitch, prof, sent_energy=1.0):
    text = " ".join(t["say"] for t in toks)
    last = toks[-1]["punct"]
    a = tts.generate(text, sid=0, speed=speed)
    x = np.array(a.samples, dtype=np.float64)
    if prof.get("f0_scale", 1.0) != 1.0 or prof.get("formant", 1.0) != 1.0:
        x = _gender(x, a.sample_rate, prof["f0_scale"], prof["formant"])
    # sona doğru perde: '?' yükselir, '!' hafif yükselip düşer
    k_end = pitch * (1 + (prof["q_rise"] if "?" in last else 0.0))
    fr = Fraction(SR, a.sample_rate)
    y = resample_poly(x, fr.numerator, fr.denominator)
    y = _pitch_glide(y, pitch, k_end) if abs(k_end - pitch) > 1e-4 or abs(pitch - 1) > 1e-4 else y
    y = _trim(y)
    return y


def _gaps(y, min_gap=0.06):
    hop = int(0.005 * SR)
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y) - hop, hop)])
    sil = env < 0.02 * (env.max() + 1e-9) * 6
    return sil


def render(sentences, out_dir, voice="dfki", profile=None, start=0.05, tail=1.15, gap_after_last=0.0, speed_k=None):
    prof = dict(PROFILE)
    if profile:
        prof.update(profile)
    tts = load_tts(voice, prof)
    os.makedirs(out_dir, exist_ok=True)
    timeline, pieces, t = [], [], start
    total = start
    for sid, text, speed, energy, gap in sentences:
        toks = parse(text)
        sp = prof["speed"] * speed * (speed_k or 1.0)
        # ifade ifade sentezle
        cur = t
        words_out = []
        seq = []
        for ci, ch in enumerate(chunks_of(toks)):
            y = synth_chunk(tts, ch, sp, prof["pitch"] * (1 + 0.012 * (energy - 1)), prof, energy)
            dur = len(y) / SR
            w = np.array([syl(x["say"]) for x in ch], float)
            edges = np.concatenate([[0], np.cumsum(w)]) / w.sum()
            # enerji: vurgulu kelimeler + '!' boost
            env_g = np.ones(len(y))
            bright = np.zeros(len(y))
            for j, wd in enumerate(ch):
                a0, a1 = int(edges[j] * len(y)), int(edges[j + 1] * len(y))
                if wd["emph"]:
                    g = 10 ** (prof["emph_gain_db"] / 20)
                    ramp = np.minimum(1, np.minimum(np.arange(a1 - a0), np.arange(a1 - a0)[::-1]) / (0.03 * SR))
                    env_g[a0:a1] = 1 + (g - 1) * ramp
                    bright[a0:a1] = ramp
            if "!" in ch[-1]["punct"]:
                env_g *= 10 ** (prof["excl_boost_db"] / 20)
            hi = sosfilt(butter(2, 2600, "high", fs=SR, output="sos"), y) * bright * (10 ** (prof["emph_bright_db"] / 20) - 1)
            y = (y + hi) * env_g * (1.0 + 0.06 * (energy - 1))
            seq.append((ch, y, dur))
        # birleştir
        pos = 0.0
        buf = []
        for ci, (ch, y, dur) in enumerate(seq):
            for j, wd in enumerate(ch):
                w = np.array([syl(x["say"]) for x in ch], float)
                edges = np.concatenate([[0], np.cumsum(w)]) / w.sum()
                words_out.append(dict(show=wd["show"], emph=bool(wd["emph"]), t0=round(cur + pos + dur * edges[j], 3), t1=round(cur + pos + dur * edges[j + 1], 3)))
            buf.append((pos, y))
            p = ch[-1]["punct"]
            gp = prof["gap_colon"] if ":" in p else prof["gap_comma"] if "," in p else 0.0
            pos += dur + gp
        s_dur = pos - (gp if seq else 0)
        timeline.append(dict(id=sid, t0=round(cur, 3), t1=round(cur + s_dur, 3), words=words_out, text=text))
        for p0, y in buf:
            pieces.append((cur + p0, y))
        t = cur + s_dur + gap
        total = cur + s_dur
    end = total + tail
    T = float(int(np.ceil(end)))
    n = int(T * SR)
    voice_buf = np.zeros(n)
    for (t0, y) in pieces:
        i = int(t0 * SR)
        voice_buf[i:i + len(y)] += y[: n - i]
    voice_buf = studio(voice_buf, prof)
    # seviye: konuşulan bölgelerin RMS'i -16.5 dBFS, yumuşak tepe sınırlayıcı
    act = np.abs(voice_buf) > 0.02 * np.max(np.abs(voice_buf))
    rms = np.sqrt(np.mean(voice_buf[act] ** 2))
    voice_buf = voice_buf * (10 ** (-16.5 / 20) / (rms + 1e-9))
    voice_buf = np.tanh(voice_buf / 0.8) * 0.8
    with wave.open(os.path.join(out_dir, "voice.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(voice_buf, -1, 1) * 32767).astype("<i2").tobytes())
    json.dump(dict(duration=T, voice=voice, last_word_end=round(total, 3), sentences=timeline), open(os.path.join(out_dir, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    return T, total, voice_buf
