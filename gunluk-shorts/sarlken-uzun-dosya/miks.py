"""
miks.py — "ŞARLKEN" nihai ses mikseri: voice + müzik + SFX → −14 LUFS / ≤ −1 dBTP.

    python3 miks.py                   # tam miks (out/music.wav, out/sfx_bus.wav, out/mix_audio.wav, out/mix_audio.m4a, out/audio_report.txt)
    python3 miks.py --preview         # + out/audio_prev/ (her cue'dan ve ana SFX'lerden kısa WAV'lar, miks kesitleri)
    python3 miks.py --tail 7.0        # kapanış kartı süresi (konuşma sonrası müzik sönümü); mix = voice + tail

Girdiler: out/voice.wav (mono 48 kHz), out/voice_chapters.json, out/timeline.json (bilgi/QA), out/sfx_cues.json (isteğe bağlı;
yoksa yalnız bölüm kartı stinger'ları + c0 sonunda title_hit). sfx_cues.json t değerleri voice.wav zaman eksenindedir.

Zincir
  voice : 80 Hz HPF → sıkıştırıcı (2:1, −24 dBFS, atak 10 ms, bırakma 120 ms) → +1,5 dB @3 kHz → 7 kHz üstü yumuşak kısma + dinamik de-ess
  müzik : muzik.render_music (ham, −27,5 dBFS RMS) → 300 Hz–3 kHz arası −3 dB çukur → konuşmaya duyarlı ducking (−5…−8 dB),
          bölüm kartı/başlık boşluğunda +9 dB yükseliş; konuşma-müzik farkı ≥ 14 dB için kapalı döngü kırpma
  sfx   : sfx.py kütüphanesi, cue başına kazanç/pan/tohum; döngü sesleri konuşma altında −4 dB
  master: true-peak duyarlı ileri bakışlı yumuşak limiter + −14 LUFS (BS.1770 kapılı) yinelemeli kalibrasyon;
          AAC 192k kodlaması sonrası true-peak yeniden doğrulanır.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter, sosfilt, sosfiltfilt, welch

import ses_dsp as D
from ses_dsp import SR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

FR = 480                      # 10 ms'lik analiz karesi (100 Hz zarf hızı)
TARGET_LUFS = -14.0
CEILING_DB = -1.2             # limiter tavanı (dBTP); AAC sonrası ≤ −1,0 doğrulanır
SNR_TARGET = 14.6             # konuşma − müzik hedef farkı (dB); asgari 14,0 aranır
MUSIC_EQ = [("peak", 420, -2.87, 1.1), ("peak", 900, -1.59, 1.0), ("peak", 1900, -3.01, 1.1)]   # 300 Hz–3 kHz ≈ −3 dB
VOICE_EQ = [("peak", 3000, +1.5, 0.9), ("highshelf", 7000, -2.5, 0.7)]
BLOOM_DB = 9.0                # boşlukta müzik, konuşma altı seviyesinin +9 dB üstüne çıkar (8–10 dB)
MIN_GAP_SEC = 1.5             # bundan kısa konuşma araları 'konuşma' sayılır (pompalama yok)
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


# ═══════════════════════════ girdiler ═══════════════════════════
def load_inputs():
    voice, sr = D.read_wav(os.path.join(OUT, "voice.wav"))
    assert sr == SR, f"voice.wav {sr} Hz; 48000 bekleniyordu"
    voice = voice[:, 0]
    meta = json.load(open(os.path.join(OUT, "voice_chapters.json")))
    chapters = meta["chapters"]
    timeline = None
    tp = os.path.join(OUT, "timeline.json")
    if os.path.exists(tp):
        timeline = json.load(open(tp))
    return voice, chapters, float(meta["total"]), timeline


# ═══════════════════════════ ses (voice) zinciri ═══════════════════════════
def deess(x, lo=5200.0, hi=9800.0, ratio=2.5, max_red=5.0, pct=72, hop=24):
    """Dinamik de-ess: 5,2–9,8 kHz bandı ayrı (sıfır faz) ayıklanır, eşiği aşan ıslık anlarında yalnız o band kısılır."""
    sos = butter(2, [lo, hi], "band", fs=SR, output="sos")
    band = sosfiltfilt(sos, x)
    n = len(x)
    nh = n // hop + 1
    p = np.zeros(nh * hop)
    p[:n] = band * band
    e = 10 * np.log10(p.reshape(nh, hop).mean(axis=1) + 1e-12)
    act = e > -75
    thr = float(np.percentile(e[act], pct)) if np.any(act) else 0.0
    gr = -np.minimum(np.maximum(e - thr, 0.0) * (1 - 1 / ratio), max_red)
    dt = hop / SR
    grs = D._smooth_ar(gr, np.exp(-dt / 0.002), np.exp(-dt / 0.05))
    g = 10 ** (np.interp(np.arange(n), (np.arange(nh) + 0.5) * hop, grs) / 20.0)
    y = x - band + band * g
    return y, dict(thr_db=thr, max_gr=float(-grs.min()), mean_gr_active=float(-grs[act].mean()) if np.any(act) else 0.0)


def voice_chain(v):
    """voice (mono float32) → işlenmiş (mono float32) + istatistikler."""
    x = v.astype(np.float64)
    x = sosfilt(butter(2, 80, "high", fs=SR, output="sos"), x)
    x, grs = D.compressor(x, thr_db=-24.0, ratio=2.0, attack=0.010, release=0.120, knee_db=6.0)
    comp = dict(max_gr=float(-grs.min()), mean_gr_active=float(-grs[grs < -0.05].mean()) if np.any(grs < -0.05) else 0.0,
                frac_active=float(np.mean(grs < -0.5)))
    x = D.eq_apply(x, VOICE_EQ)
    x, de = deess(x)
    return x.astype(np.float32), dict(compressor=comp, deess=de)


# ═══════════════════════════ konuşma analizi ═══════════════════════════
def frame_power(x, n_frames=None):
    """x (n,) veya (n,2) → 10 ms kare başına ortalama güç (float64)."""
    n = len(x) // FR if n_frames is None else n_frames
    out = np.zeros(n)
    step = 2000
    for i in range(0, n, step):
        j = min(n, i + step)
        seg = x[i * FR:j * FR].astype(np.float64)
        if len(seg) < (j - i) * FR:
            seg = np.concatenate([seg, np.zeros(((j - i) * FR - len(seg),) + seg.shape[1:])])
        if seg.ndim == 2:
            out[i:j] = np.mean(seg.reshape(j - i, FR, seg.shape[1]) ** 2, axis=(1, 2))
        else:
            out[i:j] = np.mean(seg.reshape(j - i, FR) ** 2, axis=1)
    return out


def speech_analysis(voice, n_frames, min_gap=MIN_GAP_SEC):
    """Konuşma etkinliği: kare gücü → aktif; min_gap'ten kısa aralıklar köprülenir (konuşma bölgesi).
    Döner: dict(Pv, act, region, gaps[(a,b)] kare indeksleri, level_db (1 sn konuşma düzeyi))."""
    Pv = frame_power(voice, n_frames)
    db = 10 * np.log10(Pv + 1e-12)
    act = db > -52.0
    region = act.copy()
    idx = np.flatnonzero(act)
    gaps = []
    if len(idx):
        d = np.diff(idx)
        brk = np.flatnonzero(d > 1)
        for k in brk:
            a, b = idx[k] + 1, idx[k + 1]
            if (b - a) < int(min_gap * 100):
                region[a:b] = True
        last = idx[-1] + 1
    else:
        last = 0
    # boşluklar: bölge dışı ≥ min_gap'lik koşular
    r = region.astype(np.int8)
    ch = np.flatnonzero(np.diff(np.concatenate([[1], r, [1]])))
    for a, b in zip(ch[0::2], ch[1::2]):
        if r[a:b].sum() == 0 and (b - a) >= int(min_gap * 100):
            gaps.append((int(a), int(b)))
    # 1 sn kayan konuşma düzeyi (yalnız aktif kareler): derinlik eşlemesi için
    w = 100
    num = uniform_filter1d(Pv * act, w, mode="nearest")
    den = uniform_filter1d(act.astype(np.float64), w, mode="nearest")
    lev = 10 * np.log10(num / np.maximum(den, 1e-3) + 1e-12)
    lev = np.where(den > 0.05, lev, -26.0)
    lev = uniform_filter1d(lev, 150, mode="nearest")
    return dict(Pv=Pv, act=act, region=region, gaps=gaps, level_db=lev)


def depth_curve(level_db):
    """Konuşma düzeyine göre ducking derinliği: sessiz konuşmada −5, yüksek konuşmada −8 dB."""
    return -5.0 - 3.0 * np.clip((level_db + 30.0) / 12.0, 0.0, 1.0)


def window_snr(Pv, Pm, act, G, lo, hi):
    """[lo,hi) kare aralığında konuşma-müzik farkı (dB): aktif karelerde ortalama güçlerin oranı."""
    m = act[lo:hi]
    if m.sum() < 200:
        return None
    pv = Pv[lo:hi][m].mean()
    pm = (Pm[lo:hi] * 10 ** (G[lo:hi] / 10.0))[m].mean()
    return 10 * np.log10(pv / (pm + 1e-20) + 1e-20)


def build_gain_curve(sa, Pm_raw, n_frames, chapters, tail_frames, title_end_frame=None, log_=log):
    """Müzik kazanç eğrisi (dB, 100 Hz): ducking + SNR kırpması + bölüm kartı yükselişleri. Döner (G, info)."""
    Pv, act, region, gaps = sa["Pv"], sa["act"], sa["region"], sa["gaps"]
    depth = depth_curve(sa["level_db"])
    G = depth.copy()
    # ── kapalı döngü SNR kırpması (yalnız konuşma bölgesinde): pencere 8 sn / adım 2 sn
    W, H = 800, 200
    trims = np.zeros(n_frames)
    for it in range(4):
        need = np.zeros(n_frames)
        worst = 99.0
        for lo in range(0, n_frames - W // 2, H):
            hi = min(n_frames, lo + W)
            s = window_snr(Pv, Pm_raw, act, G + trims, lo, hi)
            if s is None:
                continue
            worst = min(worst, s)
            if s < SNR_TARGET:
                need[lo:hi] = np.maximum(need[lo:hi], SNR_TARGET - s)
        if need.max() <= 0.01:
            break
        add = uniform_filter1d(need, 400, mode="nearest")          # 4 sn yumuşatma
        add = np.maximum(add, need * 0.0) * 1.15 + 0.0
        trims -= add
    G = G + trims * region
    # ── bölüm kartı / başlık yükselişleri
    t_title = chapters[0]["t1"]
    info_gaps = []
    for (a, b) in gaps:
        is_title = abs(a / 100.0 - t_title) < 0.25
        d1, r1 = (-5, 50) if is_title else (12, 100)
        p1, r2 = 45, 45
        gd_a = G[max(a - 1, 0)]
        gd_b = G[min(b, n_frames - 1)] if b < n_frames else gd_a
        # plato aralığı: ham müzik gücü (yükseliş sonrası → düşüşe kadar)
        p0, p1_ = a + max(d1, 0) + int(r1 * 0.7), max(b - p1, a + 20)
        if p1_ <= p0:
            p0, p1_ = a, b
        pre0, pre1 = max(a - 400, 0), max(a - 30, 1)
        sel = region[pre0:pre1]
        Ppre = (Pm_raw[pre0:pre1] * 10 ** (G[pre0:pre1] / 10.0))[sel].mean() if sel.sum() > 20 else None
        Pgap = Pm_raw[p0:p1_].mean() if p1_ > p0 else None
        if Ppre is None or Pgap is None or Pgap <= 1e-12:
            gopen = gd_a + BLOOM_DB
        else:
            gopen = 10 * np.log10(Ppre) + BLOOM_DB - 10 * np.log10(Pgap)
        gopen = float(np.clip(gopen, gd_a - 6.0, gd_a + 12.0))
        s0 = a + d1
        for i in range(max(s0, 0), min(b, n_frames)):
            if i < s0 + r1:
                w = D.smoothstep((i - s0) / r1)
                G[i] = gd_a + (gopen - gd_a) * w
            elif b < n_frames and i >= b - p1:
                w = D.smoothstep((i - (b - p1)) / r2)
                G[i] = gopen + (gd_b - gopen) * w
            else:
                G[i] = gopen
        info_gaps.append(dict(t0=a / 100.0, t1=b / 100.0, rise_db=round(gopen - gd_a, 2), open_db=round(gopen, 2), title=bool(is_title)))
    G = uniform_filter1d(G, 7, mode="nearest")
    info = dict(gaps=info_gaps, trim_min=float(trims.min()), worst_window_before=None)
    return G, info


def apply_curve(x, G_db, sr=SR):
    """x (N,2) float32'e 100 Hz dB eğrisini örnek hızına doğrusal aradeğerleyerek uygular (yerinde)."""
    N = len(x)
    step = 1 << 22
    for i in range(0, N, step):
        j = min(N, i + step)
        t = np.arange(i, j) / float(FR) - 0.5
        g = np.interp(t, np.arange(len(G_db)), G_db)
        x[i:j] *= (10 ** (g / 20.0)).astype(np.float32)[:, None]
    return x


# ═══════════════════════════ SFX bus ═══════════════════════════
def default_sfx_cues(chapters, tail):
    """sfx_cues.json yoksa: c0 sonunda title_hit (c0 t1 + 0,4 sn); her bölüm kartında (c2…c13) boşluğun ilk 0,2 sn'sinde
    chapter_stinger (c1'in kartı = ana başlık: title_hit onu zaten kapsar). Stinger, gelen bölümün ana sesine akortlanır."""
    import muzik
    cues = []
    cues.append(dict(t=round(chapters[0]["t1"] + 0.4, 3), name="title_hit", gain_db=-6.0, pan=0.0, seed=0, dur=None, loop=False,
                     params={"root": float(D.midi_hz(muzik.CUES["c0"]["tonic"] + 12 * 0)) * 1.0}))
    for i in range(2, len(chapters)):
        prev, ch = chapters[i - 1], chapters[i]
        root = float(D.midi_hz(muzik.CUES[ch["id"]]["tonic"] + 12))
        cues.append(dict(t=round(prev["t1"] + 0.2, 3), name="chapter_stinger", gain_db=-9.0, pan=0.0, seed=i, dur=None, loop=False,
                         params={"root": root}))
    return cues


def render_sfx_bus(cues, N, sa, region_s):
    """cue listesi → (N,2) float32 SFX bus. Döngü sesleri dur boyunca tekrarlanır (1,2 sn giriş/çıkış), konuşma altında ducking."""
    import sfx
    bus = np.zeros((N, 2), dtype=np.float32)
    cache = {}
    used = []
    for c in cues:
        name = c["name"]
        t = float(c["t"])
        dur = c.get("dur")
        loop = bool(c.get("loop", False)) or (name in sfx.LOOPABLE and dur is not None)
        key = (name, int(c.get("seed", 0)), dur, loop, json.dumps(c.get("params", {}), sort_keys=True))
        if key not in cache:
            cache[key] = sfx.sfx(name, int(c.get("seed", 0)), dur, loop, **c.get("params", {}))
        x = cache[key].astype(np.float32)
        if loop and dur is not None:
            x = D.fade_edges(x, 1.2, 1.2).astype(np.float32)
        elif name in sfx.LOOPABLE and dur is None:
            pass
        g = D.db2lin(float(c.get("gain_db", 0.0)))
        gl, gr = D.pan_gains(float(c.get("pan", 0.0)))
        i = int(round(t * SR))
        if i >= N or i + len(x) <= 0:
            continue
        a = max(0, -i)
        m = min(len(x) - a, N - max(i, 0))
        seg = x[a:a + m] * np.array([gl, gr], dtype=np.float32) * np.float32(g)
        duck = c.get("duck_db")
        if duck is None:
            duck = -4.0 if (name in sfx.LOOPABLE) else 0.0
        if duck != 0.0:
            rs = region_s[(np.arange(max(i, 0), max(i, 0) + m) // FR).clip(0, len(region_s) - 1)]
            seg = seg * (10 ** (duck * rs / 20.0)).astype(np.float32)[:, None]
        bus[max(i, 0):max(i, 0) + m] += seg
        used.append(name)
    return bus, used


# ═══════════════════════════ master ═══════════════════════════
def master(mix, target=TARGET_LUFS, ceiling=CEILING_DB, max_iter=6):
    """mix (N,2) float32 → (y float32, bilgi). Yinelemeli: kazanç → limiter → LUFS ölç → düzelt."""
    st0 = D.loudness_stats(mix)
    g = target - st0["integrated"]
    log(f"  master: ön-limiter entegre {st0['integrated']:.2f} LUFS → ilk kazanç {g:+.2f} dB")
    y = None
    for it in range(max_iter):
        x = mix * np.float32(D.db2lin(g))
        y, grs = D.limiter(x, ceiling_db=ceiling, lookahead=0.005, release=0.120)
        del x
        st = D.loudness_stats(y)
        err = target - st["integrated"]
        log(f"  master it{it}: gain {g:+.2f} dB → {st['integrated']:.2f} LUFS (limiter maks. {-grs.min():.2f} dB)")
        if abs(err) < 0.03:
            break
        g += err
    tp = D.true_peak_db(y)
    return y, dict(gain_db=float(g), stats=st, true_peak=float(tp), gr_max=float(-grs.min()),
                   gr_frac_gt1=float(np.mean(grs < -1.0)), gr_frac_gt3=float(np.mean(grs < -3.0)), ceiling=float(ceiling))


def ffmpeg_loudnorm(path):
    """ffmpeg loudnorm ilk geçiş ölçümü (JSON): input_i, input_tp, input_lra, input_thresh. Başarısızsa None."""
    if not shutil.which("ffmpeg"):
        return None
    try:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True, timeout=900)
        txt = r.stderr
        a = txt.rindex("{")
        b = txt.index("}", a)
        return json.loads(txt[a:b + 1])
    except Exception as e:  # noqa
        log("  ffmpeg loudnorm ölçümü başarısız:", e)
        return None


def encode_m4a(wav, m4a):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", m4a], check=True)


def read_f32_wav(path):
    """pcm_f32le WAV okur (wave modülü float'u desteklemez) → (n,ch) float32."""
    import struct
    with open(path, "rb") as f:
        data = f.read()
    pos = 12
    fmt = None
    while pos < len(data):
        cid = data[pos:pos + 4]
        sz = struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if cid == b"fmt ":
            fmt = struct.unpack("<HHIIHH", data[pos + 8:pos + 24])
        elif cid == b"data":
            ch = fmt[1]
            x = np.frombuffer(data[pos + 8:pos + 8 + sz], dtype="<f4").reshape(-1, ch)
            return x.astype(np.float32)
        pos += 8 + sz + (sz & 1)
    raise ValueError("data yok")


# ═══════════════════════════ QA ölçümleri ═══════════════════════════
BANDS = [("düşük (<250 Hz)", 20, 250), ("orta (250 Hz–4 kHz)", 250, 4000), ("yüksek (>4 kHz)", 4000, 20000)]


def band_energy(x):
    """x (N,) veya (N,2) → band payları (%) ve centroid (Hz), Welch ile."""
    m = x if x.ndim == 1 else (x[:, 0].astype(np.float64) + x[:, 1]) * 0.5
    m = m[: (len(m) // 8192) * 8192][::1]
    f, p = welch(m.astype(np.float64), SR, nperseg=8192, noverlap=0)
    tot = p.sum() + 1e-30
    out = []
    for name, lo, hi in BANDS:
        out.append(p[(f >= lo) & (f < hi)].sum() / tot * 100)
    cen = float((p * f).sum() / tot)
    return out, cen


def rms_db_frames(x, mask_frames):
    """Kare maskesindeki kareler üzerinde ortalama güç (dBFS)."""
    P = frame_power(x, len(mask_frames))
    return 10 * np.log10(P[mask_frames].mean() + 1e-20)


def clip_count(x, thr=0.9995):
    c = 0
    for i in range(0, len(x), 1 << 22):
        c += int(np.sum(np.abs(x[i:i + (1 << 22)]) >= thr))
    return c


# ═══════════════════════════ ana akış ═══════════════════════════
def main():
    ap = argparse.ArgumentParser(description="Şarlken nihai miks (voice + müzik + SFX)")
    ap.add_argument("--tail", type=float, default=7.0, help="kapanış kartı (sn): mix = voice + tail")
    ap.add_argument("--preview", action="store_true", help="out/audio_prev/ kısa WAV'lar + miks kesitleri")
    ap.add_argument("--fresh", action="store_true", help="müzik önbelleğini yok say")
    ap.add_argument("--no-m4a", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--sfx-cues", default=os.path.join(OUT, "sfx_cues.json"))
    ap.add_argument("--stems", action="store_true", help="ducking'li müzik (music_ducked.wav) ve işlenmiş ses (voice_proc.wav) de yaz")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    import muzik
    import sfx
    voice, chapters, total, timeline = load_inputs()
    tail = float(a.tail)
    Nv = len(voice)
    N = Nv + int(round(tail * SR))
    nf = N // FR
    log(f"voice {Nv / SR:.2f} sn + kuyruk {tail:.2f} sn = {N / SR:.2f} sn; {len(chapters)} bölüm")

    # 1) ses zinciri
    vproc, vinfo = voice_chain(voice)
    log(f"voice zinciri tamam: sıkıştırma maks. {vinfo['compressor']['max_gr']:.1f} dB, de-ess maks. {vinfo['deess']['max_gr']:.1f} dB")
    vfull = np.zeros(N, dtype=np.float32)
    vfull[:Nv] = vproc
    voice_raw_full = np.zeros(N, dtype=np.float32)
    voice_raw_full[:Nv] = voice

    # 2) konuşma analizi
    sa = speech_analysis(voice_raw_full, nf)
    Pv_proc = frame_power(vfull, nf)
    sa["Pv"] = Pv_proc          # SNR işlenmiş ses üzerinden ölçülür
    region_s = uniform_filter1d(sa["region"].astype(np.float64), 40, mode="nearest")
    log(f"konuşma bölgesi {sa['region'].mean() * 100:.1f}% ; boşluk (≥{MIN_GAP_SEC} sn) sayısı {len(sa['gaps'])}")

    # 3) müzik (ham, ducking'siz)
    cache = None if a.fresh else os.path.join(OUT, "_audio_cache")
    music, minfo = muzik.render_music(chapters, total, tail, workers=a.workers, cache_dir=cache, seed=a.seed)
    assert len(music) == N, (len(music), N)
    log(f"müzik hazır ({minfo['render_sec']} sn), global kazanç {minfo['global_gain_db']:+.2f} dB")
    D.write_wav(os.path.join(OUT, "music.wav"), music, SR, 16)
    log("out/music.wav yazıldı (ham, ducking'siz nominal bant)")
    rms_nominal = muzik._robust_rms_db(music)

    # 4) müzik bus: EQ + ducking/yükseliş
    music = D.eq_apply(music, MUSIC_EQ).astype(np.float32)
    Pm_raw = frame_power(music, nf)
    G, ginfo = build_gain_curve(sa, Pm_raw, nf, chapters, int(tail * 100), log_=log)
    music = apply_curve(music, G)
    log(f"ducking eğrisi: konuşma bölgesi ort. {G[sa['region']].mean():+.2f} dB; yükseliş {len(ginfo['gaps'])} boşlukta; kırpma maks. {ginfo['trim_min']:.2f} dB")

    # 5) SFX bus
    if os.path.exists(a.sfx_cues):
        cues = json.load(open(a.sfx_cues))
        log(f"sfx_cues.json okundu: {len(cues)} cue")
    else:
        cues = default_sfx_cues(chapters, tail)
        log(f"sfx_cues.json yok → varsayılan {len(cues)} cue (title_hit + bölüm kartı stinger'ları)")
    sfxbus, used = render_sfx_bus(cues, N, sa, region_s)
    D.write_wav(os.path.join(OUT, "sfx_bus.wav"), sfxbus, SR, 16)
    log("out/sfx_bus.wav yazıldı")

    # 6) toplam + master
    mix = music.copy()
    mix[:, 0] += vfull
    mix[:, 1] += vfull
    mix += sfxbus
    pre = D.loudness_stats(mix)
    log(f"miks (master öncesi): {pre['integrated']:.2f} LUFS")
    final, minf = master(mix, TARGET_LUFS, CEILING_DB)
    wav_path = os.path.join(OUT, "mix_audio.wav")
    m4a_path = os.path.join(OUT, "mix_audio.m4a")
    D.write_wav(wav_path, final, SR, 16)
    log(f"out/mix_audio.wav yazıldı: {minf['stats']['integrated']:.2f} LUFS, TP {minf['true_peak']:.2f} dBTP")

    m4a_info = None
    ceiling = CEILING_DB
    if not a.no_m4a and shutil.which("ffmpeg"):
        for attempt in range(3):
            encode_m4a(wav_path, m4a_path)
            tmp = os.path.join(OUT, "_m4a_check.wav")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", m4a_path, "-c:a", "pcm_f32le", "-ar", "48000", "-f", "wav", tmp], check=True)
            dec = read_f32_wav(tmp)
            os.remove(tmp)
            tp_m4a = D.true_peak_db(dec)
            st_m4a = D.loudness_stats(dec)
            log(f"  m4a doğrulama: {st_m4a['integrated']:.2f} LUFS, TP {tp_m4a:.2f} dBTP")
            m4a_info = dict(tp=float(tp_m4a), lufs=float(st_m4a["integrated"]), size_mb=os.path.getsize(m4a_path) / 1e6, len=len(dec) / SR)
            del dec
            if tp_m4a <= -1.0:
                break
            ceiling -= (tp_m4a + 1.0) + 0.15
            log(f"  AAC sonrası TP aşımı → tavan {ceiling:.2f} dBTP ile yeniden")
            final, minf = master(mix, TARGET_LUFS, ceiling)
            D.write_wav(wav_path, final, SR, 16)
    else:
        log("m4a atlandı")

    # 7) ölçüm/QA
    ff = ffmpeg_loudnorm(wav_path)
    write_report(a, chapters, total, tail, N, vinfo, sa, G, ginfo, minfo, minf, m4a_info, ff, voice_raw_full, vfull, music, sfxbus, final,
                 rms_nominal, cues, used, nf, pre)
    if a.stems:
        D.write_wav(os.path.join(OUT, "music_ducked.wav"), music, SR, 16)
        D.write_wav(os.path.join(OUT, "voice_proc.wav"), vfull, SR, 16)
    if a.preview:
        write_previews(a, chapters, minfo, final, music, sfxbus, vfull, timeline)
    log("bitti.")


# ═══════════════════════════ rapor ═══════════════════════════
def write_report(a, chapters, total, tail, N, vinfo, sa, G, ginfo, minfo, minf, m4a, ff, voice_raw, vproc, music, sfxbus, final,
                 rms_nominal, cues, used, nf, pre):
    import muzik
    L = []
    P = L.append
    st = minf["stats"]
    P("ŞARLKEN — SES RAPORU (miks.py)")
    P("=" * 78)
    P(f"süre: mix {N / SR:.2f} sn = voice {total:.2f} + kapanış {tail:.2f}; örnekleme 48 kHz stereo; çıktı 16-bit PCM + AAC 192k")
    P("")
    P("[1] NİHAİ MİKS — mix_audio.wav")
    P(f"  entegre loudness (BS.1770, kendi ölçümüm) : {st['integrated']:.2f} LUFS   (hedef −14,0)")
    if ff:
        P(f"  ffmpeg loudnorm ölçümü (bağımsız)          : {ff.get('input_i')} LUFS ; LRA {ff.get('input_lra')} LU ; eşik {ff.get('input_thresh')}")
    P(f"  true-peak (4× aşırı örnekleme)            : {minf['true_peak']:.2f} dBTP   (hedef ≤ −1,0)")
    if ff:
        P(f"  ffmpeg true-peak                           : {ff.get('input_tp')} dBTP")
    P(f"  kısa-dönem (3 sn) tepe / anlık tepe       : {st['shortterm_max']:.1f} / {st['momentary_max']:.1f} LUFS ; LRA {st['lra']:.1f} LU")
    P(f"  limiter: tavan {minf['ceiling']:.2f} dBTP; maks. kazanç azaltma {minf['gr_max']:.2f} dB; >1 dB azaltma süresi %{minf['gr_frac_gt1'] * 100:.3f}; >3 dB %{minf['gr_frac_gt3'] * 100:.4f}")
    P(f"  master kazancı (toplamdan sonra)          : {minf['gain_db']:+.2f} dB")
    P(f"  örnek tepe: {20 * np.log10(np.max(np.abs(final)) + 1e-12):.2f} dBFS ; kırpılan örnek sayısı (|x|≥0,9995): {clip_count(final)}")
    dc = final.astype(np.float64).mean(axis=0)
    P(f"  DC ofset: L {dc[0]:+.2e}  R {dc[1]:+.2e}")
    if m4a:
        P(f"  mix_audio.m4a (AAC 192k): {m4a['size_mb']:.1f} MB, {m4a['len']:.2f} sn; çözülmüş TP {m4a['tp']:.2f} dBTP; {m4a['lufs']:.2f} LUFS")
    P("")
    P("[2] KONUŞMA / MÜZİK (kendi ölçümüm; konuşma-aktif karelerde ortalama güç)")
    act = sa["act"]
    snr_all = rms_db_frames(vproc, act) - rms_db_frames(music, act)
    sfx_all = rms_db_frames(sfxbus, act)
    P(f"  konuşma RMS (işlenmiş, ön-master) : {rms_db_frames(vproc, act):.1f} dBFS")
    P(f"  müzik RMS (konuşma altında)       : {rms_db_frames(music, act):.1f} dBFS   → konuşma − müzik = {snr_all:.1f} dB   (şart ≥ 14)")
    P(f"  SFX RMS (konuşma karelerinde)     : {sfx_all:.1f} dBFS")
    P(f"  müzik bandı ort. RMS (ducking öncesi, nominal): {rms_nominal:.1f} dBFS   (şart −24…−28)")
    P("  bölüm bazında (konuşma-aktif kareler; kare = 10 ms):")
    P("   bölüm   konuşma   müzik    fark   ducking ort.   en kötü 8 sn penceresi")
    Pv, Pm = frame_power(vproc, nf), frame_power(music, nf)
    worst_all = 99.0
    for ch in chapters:
        lo, hi = int(ch["t0"] * 100), min(int(ch["t1"] * 100), nf)
        m = act[lo:hi]
        pv = Pv[lo:hi][m].mean()
        pm = Pm[lo:hi][m].mean()
        w = 800
        ws = 99.0
        for s0 in range(lo, hi - w // 2, 200):
            s1 = min(hi, s0 + w)
            mm = act[s0:s1]
            if mm.sum() >= 300:
                ws = min(ws, 10 * np.log10(Pv[s0:s1][mm].mean() / (Pm[s0:s1][mm].mean() + 1e-20)))
        worst_all = min(worst_all, ws)
        dk = G[lo:hi][sa["region"][lo:hi]].mean()
        P(f"   {ch['id']:5s} {10 * np.log10(pv):7.1f}  {10 * np.log10(pm):7.1f}  {10 * np.log10(pv / (pm + 1e-20)):6.1f}   {dk:+6.1f} dB      {ws:6.1f} dB")
    P(f"  en kötü 8 sn penceresi (tüm bölümler): {worst_all:.1f} dB")
    P(f"  ducking: konuşma bölgesinde ort. {G[sa['region']].mean():+.2f} dB (aralık {G[sa['region']].min():+.1f} … {G[sa['region']].max():+.1f}); SNR kırpması maks. {ginfo['trim_min']:.2f} dB")
    P("  bölüm kartı / başlık boşluklarında müzik yükselişi (konuşma altı seviyeye göre):")
    for g in ginfo["gaps"]:
        P(f"   t={g['t0']:8.2f}–{g['t1']:8.2f} sn   yükseliş {g['rise_db']:+5.1f} dB" + ("   [ana başlık]" if g["title"] else ""))
    P("")
    P("[3] SPEKTRAL DENGE (Welch, güç payı %)  düşük<250 Hz | orta 250–4k | yüksek>4k | centroid")
    for nm, arr in (("voice (ham)", voice_raw), ("voice (işlenmiş)", vproc), ("müzik (mikste)", music), ("sfx bus", sfxbus), ("MIKS (nihai)", final)):
        b, cen = band_energy(arr)
        P(f"  {nm:18s} {b[0]:5.1f} | {b[1]:5.1f} | {b[2]:5.1f} | {cen:6.0f} Hz")
    P("")
    P("[4] SES (voice) ZİNCİRİ")
    c = vinfo["compressor"]
    P(f"  HPF 80 Hz; sıkıştırıcı 2:1 / −24 dBFS / 10 ms / 120 ms (maks. azaltma {c['max_gr']:.1f} dB, aktifken ort. {c['mean_gr_active']:.1f} dB, süre %{c['frac_active'] * 100:.1f});")
    P(f"  +1,5 dB @3 kHz presence; 7 kHz üstü yüksek raf −2,5 dB + dinamik de-ess (5,2–9,8 kHz; eşik {vinfo['deess']['thr_db']:.1f} dB, maks. {vinfo['deess']['max_gr']:.1f} dB)")
    P("")
    P("[5] MÜZİK CUE'LARI (ham bant; ses/müzik karakteri)")
    P("  cue  ruh        mod         bpm  ölçü  başlangıç  bitiş    uzunluk  (bölüm süresi)  çapraz geçiş (giriş/çıkış)  ön-kazanç")
    for ci in minfo["cues"]:
        P(f"  {ci['id']:4s} {ci['mood']:9s}  {ci['mode']:10s} {ci['bpm']:4d}  {ci['meter']:4s} {ci['start']:9.2f} {ci['end']:8.2f} {ci['length']:8.2f}  ({ci['chapter_dur']:6.2f})        {ci['xin']:.0f} / {ci['xout']:.0f} sn          {ci['pre_gain_db']:+.1f} dB")
    P("")
    P("[6] SFX")
    from collections import Counter
    cnt = Counter(used)
    P(f"  cue sayısı: {len(cues)} ; kullanılan ad(lar): " + ", ".join(f"{k}×{v}" for k, v in sorted(cnt.items())))
    P(f"  kütüphane ({len(sfx_names())}): " + ", ".join(sfx_names()))
    P("")
    P("[7] KONTROL LİSTESİ")
    chk = []

    def ck(name, ok, val):
        chk.append((name, ok, val))
    ck("entegre loudness −14 ± 0,5 LUFS", abs(st["integrated"] + 14) <= 0.5, f"{st['integrated']:.2f}")
    ck("true-peak ≤ −1,0 dBTP (wav)", minf["true_peak"] <= -1.0, f"{minf['true_peak']:.2f}")
    if m4a:
        ck("true-peak ≤ −1,0 dBTP (m4a çözülmüş)", m4a["tp"] <= -1.0, f"{m4a['tp']:.2f}")
    ck("kırpılan örnek sayısı = 0", clip_count(final) == 0, str(clip_count(final)))
    ck("DC ofset < 1e-3", float(np.max(np.abs(dc))) < 1e-3, f"{np.max(np.abs(dc)):.1e}")
    ck("konuşma − müzik ≥ 14 dB (genel)", snr_all >= 14.0, f"{snr_all:.1f}")
    ck("konuşma − müzik ≥ 14 dB (en kötü 8 sn pencere ≥ 13)", worst_all >= 13.0, f"{worst_all:.1f}")
    ck("müzik nominal ort. RMS −24…−28 dBFS", -28.2 <= rms_nominal <= -23.8, f"{rms_nominal:.1f}")
    ck("süre = voice + kuyruk (±1 örnek)", abs(len(final) - N) <= 1, f"{len(final) / SR:.3f} sn")
    rises = [g["rise_db"] for g in ginfo["gaps"]]
    ck("boşluk yükselişi 8–10 dB (tümü)", all(7.0 <= r <= 11.5 for r in rises) if rises else False, f"min {min(rises):.1f} maks {max(rises):.1f}" if rises else "-")
    for name, ok, val in chk:
        P(f"  [{'GEÇTİ' if ok else 'KALDI'}] {name}  → {val}")
    P("")
    P(f"toplam çalışma süresi: {time.time() - T0:.0f} sn")
    txt = "\n".join(L)
    open(os.path.join(OUT, "audio_report.txt"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)


def sfx_names():
    import sfx
    return sfx.SFX_NAMES


# ═══════════════════════════ önizleme ═══════════════════════════
def _excerpt(x, t0, t1, lead=0.02):
    i0, i1 = max(0, int(t0 * SR)), min(len(x), int(t1 * SR))
    return x[i0:i1]


def _prev_norm(x, rms_target=-20.0, peak_max=-3.0):
    """Önizleme için: RMS'i hedefe getir, tepeyi sınırla (yumuşak)."""
    r = np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-12
    y = x * (D.db2lin(rms_target) / r)
    pk = np.max(np.abs(y))
    if pk > D.db2lin(peak_max):
        y = y * (D.db2lin(peak_max) / pk)
    return y.astype(np.float32)


def write_previews(a, chapters, minfo, final, music_in_mix, sfxbus, vproc, timeline):
    import muzik
    import sfx
    pdir = os.path.join(OUT, "audio_prev")
    os.makedirs(pdir, exist_ok=True)
    log(f"önizleme → {pdir}")
    raw, _ = D.read_wav(os.path.join(OUT, "music.wav"))
    lines = []
    for ci in minfo["cues"]:
        cid = ci["id"]
        spec = muzik.CUES[cid]
        ch = [c for c in chapters if c["id"] == cid][0]
        g = [g for g in minfo["geo"] if g["id"] == cid][0]
        if cid == "c0":
            t0, t1 = ch["t1"] + 0.4 - 12.0, ch["t1"] + 0.4 + 12.0
        elif cid == "c13":
            t0, t1 = min(ch["t1"] + a.tail, len(raw) / SR) - 24.0, ch["t1"] + a.tail
        else:
            arc = np.array(spec["arc"])
            u = arc[np.argmax(arc[:, 1]), 0]
            tc = ch["t0"] + float(np.clip(u, 0.2, 0.8)) * (ch["t1"] - ch["t0"])
            t0, t1 = tc - 11.0, tc + 11.0
        seg = _excerpt(raw, t0, t1)
        D.write_wav(os.path.join(pdir, f"cue_{cid}_{spec['mood']}.wav"), _prev_norm(seg), SR, 16)
        # sayısal özet
        b, cen = band_energy(seg)
        m = seg.mean(axis=1)
        crest = 20 * np.log10(np.max(np.abs(m)) / (np.sqrt(np.mean(m ** 2)) + 1e-12))
        lines.append(f"  {cid:4s} {spec['mood']:9s} {spec['mode']:10s} {spec['bpm']:3d} bpm  kesit {t0:7.1f}–{t1:7.1f} sn  RMS {D.rms_db(seg.mean(axis=1)):6.1f} dBFS  bantlar {b[0]:4.1f}/{b[1]:4.1f}/{b[2]:4.1f} %  centroid {cen:5.0f} Hz  crest {crest:4.1f} dB")
    # SFX önizlemeleri
    for nm in sfx.SFX_NAMES:
        x = sfx.sfx(nm, 0)
        D.write_wav(os.path.join(pdir, f"sfx_{nm}.wav"), x, SR, 16)
    # miks kesitleri: açılış + başlık + bölüm kartları
    t_hit = chapters[0]["t1"] + 0.4
    D.write_wav(os.path.join(pdir, "mix_00_acilis_soguk_acilis_ve_baslik.wav"), _excerpt(final, 0, t_hit + 12.0), SR, 16)
    for i in range(1, len(chapters)):
        t = chapters[i]["t0"]
        D.write_wav(os.path.join(pdir, f"mix_{i:02d}_kart_{chapters[i]['id']}.wav"), _excerpt(final, t - 9.0, t + 7.0), SR, 16)
    D.write_wav(os.path.join(pdir, "mix_99_kapanis.wav"), _excerpt(final, chapters[-1]["t1"] - 12.0, len(final) / SR), SR, 16)
    with open(os.path.join(OUT, "audio_report.txt"), "a", encoding="utf-8") as f:
        f.write("\n[8] ÖNİZLEME DOSYALARI (out/audio_prev/) — cue kesitleri (RMS −20 dBFS'e normalli) ve sayısal özetleri\n")
        f.write("\n".join(lines) + "\n")
        f.write(f"  + sfx_*.wav ({len(sfx.SFX_NAMES)} adet), mix_*.wav (açılış, {len(chapters) - 1} bölüm kartı, kapanış)\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
