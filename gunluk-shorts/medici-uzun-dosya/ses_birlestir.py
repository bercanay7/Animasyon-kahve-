"""ElevenLabs bölüm seslerini (ses_ham/cN_v1.mp3) tek anlatım kanalında birleştirir.
 - uzun sessizlikleri (>MAXGAP) kısaltır (dramatik duraklar kalır, boşluk çekilmez),
 - bölümleri aynı konuşma seviyesine getirir,
 - bölümler arası bölüm-kartı boşluğu bırakır,
 - out/voice.wav (48 kHz mono 16 bit), out/voice_chapters.json, out/voice_for_scribe.mp3 üretir.
Kullanım: python3 ses_birlestir.py [--version v1]"""
import json, os, subprocess, sys, wave
import numpy as np
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parca as PA
import script as S
RAW = os.path.join(HERE, "ses_ham")
OUT = PA.OUT
os.makedirs(OUT, exist_ok=True)
SR = 48000
MAXGAP = 0.85          # bundan uzun sessizlik bu değere indirilir
GAP_THR_DB = -42       # tepe RMS'e göre sessizlik eşiği
CARD_GAP = {"c0": 6.5}  # c0 sonrası ana başlık (fresco_title: panel 0,3–3,7 sn açılır, başlık 2,6 sn, ≥1,5 sn tutuş) — Parça 1
DEFAULT_GAP = 3.0       # bölüm kartı boşluğu
TARGET_RMS_DB = -21.0   # aktif konuşma RMS hedefi (nihai miks −14 LUFS'a ayrıca ayarlanır)
CHAPTERS = S.PARTS[PA.PART] if PA.PART else [c["id"] for c in S.CHAPTERS]
VERSION = {c: "v1" for c in CHAPTERS}
for a in sys.argv[1:]:
    if "=" in a:
        k, v = a.split("="); VERSION[k] = v


def load(cid):
    mp3 = os.path.join(RAW, f"{cid}_{VERSION[cid]}.mp3")
    wav = os.path.join(RAW, f"{cid}_{VERSION[cid]}_48k.wav")
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-ar", str(SR), "-ac", "1", wav], check=True)
    w = wave.open(wav)
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    return x


def rms_db(a):
    return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9)


def squeeze_gaps(x):
    hop = int(0.01 * SR)
    n = len(x) // hop
    e = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    db = 20 * np.log10(e + 1e-9)
    thr = np.percentile(db, 95) + GAP_THR_DB      # tepeye yakın seviyeye göre
    sil = db < thr
    # baş/son sessizliği 0,18 sn'ye indir
    first = int(np.argmax(~sil)); last = n - int(np.argmax(~sil[::-1]))
    head = max(0, first - int(0.18 / 0.01)); tail = min(n, last + int(0.30 / 0.01))
    keep_ranges = []
    i = head
    cur_start = head
    saved = 0.0
    out = []
    xfade = int(0.02 * SR)
    pos = head
    while pos < tail:
        if sil[pos]:
            j = pos
            while j < tail and sil[j]:
                j += 1
            dur = (j - pos) * 0.01
            if dur > MAXGAP:
                # [pos, j) içinden ortadan (dur-MAXGAP) kes: başta 0,35 sn, sonda kalan
                keep_a = int(0.35 / 0.01)
                keep_b = int(MAXGAP / 0.01) - keep_a
                out.append(x[cur_start * hop:(pos + keep_a) * hop])
                cur_start = j - keep_b
                saved += dur - MAXGAP
            pos = j
        else:
            pos += 1
    out.append(x[cur_start * hop:tail * hop])
    # çapraz geçişle birleştir
    y = out[0]
    for seg in out[1:]:
        if len(seg) < 2 * xfade or len(y) < 2 * xfade:
            y = np.concatenate([y, seg]); continue
        fade = np.linspace(0, 1, xfade)
        y = np.concatenate([y[:-xfade], y[-xfade:] * (1 - fade) + seg[:xfade] * fade, seg[xfade:]])
    return y, saved


def active_rms_db(y):
    hop = int(0.02 * SR)
    fr = np.array([rms_db(y[i:i + hop]) for i in range(0, len(y) - hop, hop)])
    act = fr[fr > np.percentile(fr, 95) - 22]
    return float(np.mean(act))


def main():
    parts, meta, t = [], [], 0.0
    total_saved = 0.0
    avail = [c for c in CHAPTERS if os.path.exists(os.path.join(RAW, f"{c}_{VERSION[c]}.mp3")) or os.path.exists(os.path.join(RAW, f"{c}_{VERSION[c]}_48k.wav"))]
    missing = [c for c in CHAPTERS if c not in avail]
    if missing:
        print('UYARI: ham ses yok, atlandı:', missing)
    for cid in avail:
        x = load(cid)
        y, saved = squeeze_gaps(x)
        total_saved += saved
        g = TARGET_RMS_DB - active_rms_db(y)
        y = y * (10 ** (g / 20))
        gap = CARD_GAP.get(cid, DEFAULT_GAP) if cid != avail[-1] else 0.0
        meta.append(dict(id=cid, t0=round(t, 3), t1=round(t + len(y) / SR, 3), dur=round(len(y) / SR, 3),
                         raw=round(len(x) / SR, 3), saved=round(saved, 2), gain_db=round(g, 2), gap_after=gap))
        parts.append(y)
        t += len(y) / SR
        if gap:
            parts.append(np.zeros(int(gap * SR)))
            t += gap
    v = np.concatenate(parts)
    peak = np.max(np.abs(v))
    if peak > 0.95:
        v = v * (0.95 / peak)
    with wave.open(os.path.join(OUT, "voice.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(v, -1, 1) * 32767).astype("<i2").tobytes())
    json.dump(dict(sr=SR, total=round(len(v) / SR, 3), chapters=meta), open(os.path.join(OUT, "voice_chapters.json"), "w"), indent=1)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(OUT, "voice.wav"), "-ar", "44100", "-ac", "1",
                    "-b:a", "96k", os.path.join(OUT, "voice_for_scribe.mp3")], check=True)
    scratch = [c for c in avail if VERSION[c] != "v1"]
    flag = os.path.join(OUT, "GECICI_SES.json")
    if scratch:
        json.dump(dict(chapters=scratch, not_="Piper geçici anlatım — NİHAİ ÜRÜNDE KULLANILMAZ"), open(flag, "w"), ensure_ascii=False, indent=1)
        print("UYARI: GEÇİCİ (scratch) ses var:", scratch, "→ final mux/render durdurulur (parca.assert_gercek_ses)")
    elif os.path.exists(flag):
        os.remove(flag)
    print(f"voice.wav {len(v)/SR:.1f} s ({len(v)/SR/60:.2f} dk); kısaltılan boşluk toplamı {total_saved:.1f} s")
    for m in meta:
        print(f"  {m['id']:4s} t0={m['t0']:7.2f} dur={m['dur']:6.1f} (ham {m['raw']:6.1f}, -{m['saved']:4.1f}s) kazanç {m['gain_db']:+.1f} dB")


if __name__ == "__main__":
    main()
