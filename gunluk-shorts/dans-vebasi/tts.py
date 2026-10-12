"""
Ücretsiz, çevrimdışı Türkçe seslendirme (Piper VITS modeli + sherpa-onnx) → heyecanlı ses işleme → timeline.json

Metin işaretlemesi:  gösterilen=söylenen   (örn. 20=yirmi, 1932=bin_dokuz_yüz_otuz_iki)
                     *...*  → vurgulu (sarı fosforlu kalem) kelimeler
Çıktı: out/voice.wav (48 kHz mono, boşluklarla yerleşik), out/timeline.json (cümle ve kelime zamanları)
Kullanım: python3 tts.py [--voice=fettah|dfki|fahrettin]
"""
import glob, json, os, re, sys, wave
import numpy as np
from fractions import Fraction
from scipy.signal import butter, sosfilt, resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "ses-modelleri")
SR = 48000
VOICE = "fettah"
for a in sys.argv[1:]:
    if a.startswith("--voice="):
        VOICE = a.split("=")[1]

# (id, metin, hız, perde çarpanı, kazanç, sonrasındaki boşluk sn)
SENTENCES = [
    ("A", "Bir kadın sokakta dansa başladı, ve *günlerce duramadı!*", 1.00, 1.10, 1.00, 0.26),
    ("B", "Ama asıl çılgınlık, *yetkililerin çözümüydü!*", 1.02, 1.12, 1.00, 0.22),
    ("C", "Yıl *1518=bin_beş_yüz_on_sekiz*, Strazburg.", 1.02, 1.07, 0.95, 0.20),
    ("D", "Bir haftada *34=otuz_dört* kişi katıldı, bir ayda *400=dört_yüz!*", 1.05, 1.14, 1.05, 0.22),
    ("E", "Yemek yok, uyku yok! Yorgunluktan yığılanlar bile oldu!", 1.05, 1.14, 1.05, 0.20),
    ("F", "Doktorlar *sıcak kan* dedi. Çözüm mü? *Daha fazla dans!*", 1.05, 1.14, 1.05, 0.20),
    ("G", "Sahne kurdular, *müzisyenler tuttular!*", 1.04, 1.12, 1.00, 0.22),
    ("H", "Dans bitmek yerine, *daha da yayıldı!*", 1.04, 1.14, 1.05, 0.24),
    ("I", "Sonunda müziği yasakladılar, ve dansçıları bir türbeye götürdüler.", 1.04, 1.10, 1.00, 0.24),
    ("J", "Bilim insanları hâlâ emin değil: *ergot zehirlenmesi mi, toplu histeri mi?*", 1.05, 1.10, 1.00, 0.26),
    ("K", "Ve dans, *müzik susunca bitti!*", 1.00, 1.14, 1.05, 0.55),
    ("L", "Bazen çözüm, *sessizliktir.*", 0.90, 1.02, 0.95, 0.0),
]
SPEED_K = 1.08   # genel tempo çarpanı (heyecanlı/hızlı anlatım)
START = 0.05     # ilk cümlenin başlangıcı (sn)
TAIL = 1.15      # son kelimeden sonra sessiz kuyruk (skor karesi)


def syl(s):
    return max(1, sum(ch in "aeıioöuüAEIİOÖUÜ" for ch in s))


def parse(text):
    """→ [(göster, söylenen, vurgulu, noktalama)]"""
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
        if "=" in core:
            show, say = core.split("=", 1)
        else:
            show, say = core, core
        show, say = show + tail, say + tail
        punct = tail
        if re.fullmatch(r"[\d.]+", show):      # 10.000 gibi sayılardaki nokta cümle sonu değil
            punct = ""
        toks.append((show.replace("_", " "), say.replace("_", " "), e0, punct))
        if ends:
            emph = False
    return toks


def load_tts():
    import sherpa_onnx
    d = glob.glob(os.path.join(MODELS, f"ex_{VOICE}", "*"))[0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(d + "/*.onnx")[0], tokens=d + "/tokens.txt",
                                                    data_dir=d + "/espeak-ng-data"), num_threads=4))
    return sherpa_onnx.OfflineTts(cfg)


def excite(x, sr, pitch, gain):
    """Heyecanlı ses: perde+tempo yükseltme (yeniden örnekleme), parlaklık, sıkıştırma"""
    fr = Fraction(SR, 1) / (Fraction(sr, 1) * Fraction(pitch).limit_denominator(1000))
    y = resample_poly(x, fr.numerator, fr.denominator)
    y = sosfilt(butter(2, 90, "high", fs=SR, output="sos"), y)
    pres = sosfilt(butter(2, [2200, 5200], "band", fs=SR, output="sos"), y)
    y = y + 0.55 * pres
    y = y / (np.max(np.abs(y)) + 1e-9)
    y = np.tanh(2.2 * y) / np.tanh(2.2)          # yumuşak sıkıştırma
    return y * gain * 0.9


def trim(y, thr=0.012, pad=0.02):
    idx = np.where(np.abs(y) > thr)[0]
    if len(idx) == 0:
        return y
    a, b = max(0, idx[0] - int(pad * SR)), min(len(y), idx[-1] + int(pad * SR))
    return y[a:b]


def internal_gaps(y, min_gap=0.075):
    """Konuşma içindeki sessizlik aralıkları (sn, başlangıç-bitiş)"""
    hop = int(0.005 * SR)
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y) - hop, hop)])
    sil = env < 0.02
    gaps, i = [], 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]:
                j += 1
            if (j - i) * 0.005 >= min_gap and i > 4 and j < len(sil) - 4:
                gaps.append((i * 0.005, j * 0.005))
            i = j
        else:
            i += 1
    return gaps


def main():
    tts = load_tts()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    timeline, chunks, t = [], [], START
    total = START
    for sid, text, speed, pitch, gain, gap in SENTENCES:
        toks = parse(text)
        spoken = " ".join(tk[1] for tk in toks)
        a = tts.generate(spoken, sid=0, speed=speed * SPEED_K / pitch)
        x = np.array(a.samples, dtype=np.float64)
        y = trim(excite(x, a.sample_rate, pitch, gain))
        dur = len(y) / SR
        gaps = internal_gaps(y)
        punct_idx = [i for i, tk in enumerate(toks[:-1]) if tk[3]]
        sel = []
        if punct_idx and len(gaps) >= len(punct_idx):
            sel = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[:len(punct_idx)])
        segs = []
        if sel:
            prev, p0 = 0, 0.0
            for pi, g in zip(punct_idx, sel):
                cp = (g[0] + g[1]) / 2
                segs.append((prev, pi + 1, p0, cp))
                prev, p0 = pi + 1, cp
            segs.append((prev, len(toks), p0, dur))
        else:
            segs.append((0, len(toks), 0.0, dur))
        words = []
        for (i0, i1, s0, s1) in segs:
            w = np.array([syl(toks[i][1]) + (0 if (i == i1 - 1 and i1 == len(toks)) else (1.0 if toks[i][3] in (",", ":") else 1.8 if toks[i][3] else 0)) for i in range(i0, i1)], float)
            edges = np.concatenate([[0], np.cumsum(w)]) / w.sum()
            for j, i in enumerate(range(i0, i1)):
                words.append(dict(show=toks[i][0], emph=bool(toks[i][2]), t0=round(t + s0 + (s1 - s0) * edges[j], 3),
                                  t1=round(t + s0 + (s1 - s0) * edges[j + 1], 3)))
        timeline.append(dict(id=sid, t0=round(t, 3), t1=round(t + dur, 3), words=words, text=text,
                             gaps_found=len(gaps), gaps_expected=len(punct_idx)))
        chunks.append((t, y))
        t += dur + gap
        total = t - gap
    end = total + TAIL
    T = float(int(np.ceil(end)))  # tam saniyeye yuvarla
    n = int(T * SR)
    voice = np.zeros(n)
    for (t0, y) in chunks:
        i = int(t0 * SR)
        voice[i:i + len(y)] += y[: n - i]
    voice = np.clip(voice, -1, 1)
    with wave.open(os.path.join(HERE, "out", "voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((voice * 32767).astype("<i2").tobytes())
    json.dump(dict(duration=T, voice=VOICE, last_word_end=round(total, 3), sentences=timeline),
              open(os.path.join(HERE, "out", "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"ses={VOICE} süre={T:.0f} sn  (son kelime {total:.2f} sn)")
    for s in timeline:
        print(f"  {s['id']} {s['t0']:6.2f}–{s['t1']:6.2f}  boşluk {s['gaps_found']}/{s['gaps_expected']}  {s['text'][:58]}")


if __name__ == "__main__":
    main()
