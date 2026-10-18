"""
miks.py — "MEDICI" parça miksleri: voice + müzik + SFX → −14 LUFS / ≤ −1 dBTP. HER PARÇA AYRI miks edilir.

    MEDICI_PART=2 python3 miks_kur.py                # tam miks → out_p2/mix_audio.m4a (+ stem'ler: stem_music.flac, stem_voice.flac, stem_sfx.flac, audio_report.txt)
    MEDICI_PART=2 python3 miks_kur.py --onizleme     # GEÇİCİ (Piper) ses ya da eksik bölüm varken: çıktılar ONIZLEME_ önekiyle yazılır, final adıyla ASLA
    MEDICI_PART=2 python3 miks_kur.py --onizleme --preview   # + out_p2/ses_onizleme/*.mp3 (20–30 sn'lik kesitler; kullanıcı dinler)

`out/` sembolik bağlantısına ve parca.kullan()'a DOKUNULMAZ; tüm yollar parca.OUT (= out_pN) üzerinden.
Final miks öncesi parca.assert_gercek_ses() ÇAĞRILIR (GECICI_SES.json varsa DURUR); --onizleme bunu atlar. Eksik bölümlü parça (ör. P1'de c6 yok) da yalnız önizleme olarak miks edilir.

Girdiler: out_pN/voice.wav (mono 48 kHz), voice_chapters.json, timeline.json (müzik hikâye çıpaları + SFX çapaları + QA),
          sfx_cues_pN.json (proje kökü; elle/sahne yazarlarınca beslenen kuyruk — JSON sözleşmesi sfx.py'de), out_pN/sfx_gecis.json (otomatik geçiş sesleri; isteğe bağlı).
t değerleri voice.wav zaman eksenindedir (parça başı = 0).

Zincir
  voice : 80 Hz HPF → sıkıştırıcı (2:1, −24 dBFS, atak 10 ms, bırakma 120 ms) → +1,5 dB @3 kHz → 7 kHz üstü yumuşak kısma + dinamik de-ess
  müzik : muzik.render_music (ham, −27,5 dBFS RMS; kesit/çıpa/kapılar) → 300 Hz–3 kHz arası −3 dB çukur → konuşmaya duyarlı ducking: konuşma−müzik farkı
          [SNR_TARGET, SNR_HI] = [20, 24] dB aralığına kapalı döngüyle çekilir (Şarlken: ≥14 dB) → bölüm kartı/başlık boşluğunda +9 dB yükseliş;
          müziğin sustuğu (kapı) pencereler seviyelemeye katılmaz → sessizlik bölgeleri gerçekten sessiz kalır
  sfx   : sfx.py kütüphanesi; sfx_cues_pN.json + otomatik geçiş sesleri + bölüm kartı vurguları (perde rengine göre); kaynak politikası (çan yasağı) uygulanır
  master: true-peak duyarlı ileri bakışlı yumuşak limiter + −14 LUFS (BS.1770 kapılı) yinelemeli kalibrasyon; AAC 192k sonrası true-peak yeniden doğrulanır.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter, sosfilt, sosfiltfilt, welch

import ses_dsp as D
from ses_dsp import SR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parca as PA  # noqa: E402  (yalnız PA.PART / PA.OUT / PA.assert_gercek_ses kullanılır; kullan() ÇAĞRILMAZ)

PART = PA.PART
OUT = PA.OUT
MAX_WORKERS = 2

FR = 480                      # 10 ms'lik analiz karesi (100 Hz zarf hızı)
TARGET_LUFS = -14.0
CEILING_DB = -1.8             # limiter tavanı (dBTP); AAC kodlaması ~0,4–0,6 dB ekler → m4a ≤ −1,0 (doğrulanır, gerekirse düşürülür)
SNR_TARGET = 20.0             # konuşma − müzik hedef farkı (dB) alt sınırı: "konuşma bölgelerinde müzik −20…−24 dB" (ayar: --snr LO,HI)
SNR_HI = 24.0                 # bundan fazla fark varsa müzik sınırlı yükseltilir (MAX_BOOST) — müzik hep 'duyulur' kalsın
MAX_BOOST = 3.0
MUSIC_EQ = [("peak", 420, -2.87, 1.1), ("peak", 900, -1.59, 1.0), ("peak", 1900, -3.01, 1.1)]   # 300 Hz–3 kHz ≈ −3 dB
VOICE_EQ = [("peak", 3000, +1.5, 0.9), ("highshelf", 7000, -2.5, 0.7)]
BLOOM_DB = 9.0                # boşlukta müzik, konuşma altı seviyesinin +9 dB üstüne çıkar (8–10 dB)
MIN_GAP_SEC = 1.5             # bundan kısa konuşma araları 'konuşma' sayılır (pompalama yok)
MUSIC_ACTIVE_DB = -70.0       # müzik kare gücü (dBFS²) bunun altındaysa 'müzik yok' (kapı) sayılır; seviyelemeye katılmaz
T0 = time.time()
PERDE_FLAVOR = {1: "altin", 2: "bedel", 3: "miras"}
PART_CHAPTERS = {1: [f"c{i}" for i in range(0, 7)], 2: [f"c{i}" for i in range(7, 12)], 3: [f"c{i}" for i in range(12, 17)]}


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


def expected_chapters():
    try:
        import script as S
        return list(S.PARTS[PART])
    except Exception:   # noqa
        return PART_CHAPTERS[PART]


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
    """voice (mono float32) → işlenmiş (mono float32) + istatistikler. Sıkıştırma sonrası aktif-kare ortalama gücü girdiye
    eşitlenir (makyaj kazancı), böylece 'konuşma ≈ −21 dBFS' referansı korunur."""
    x = v.astype(np.float64)
    pin = frame_power(v)
    ain = pin > 10 ** (-52.0 / 10)
    p_in = float(pin[ain].mean())
    x = sosfilt(butter(2, 80, "high", fs=SR, output="sos"), x)
    x, grs = D.compressor(x, thr_db=-24.0, ratio=2.0, attack=0.010, release=0.120, knee_db=6.0)
    comp = dict(max_gr=float(-grs.min()), mean_gr_active=float(-grs[grs < -0.05].mean()) if np.any(grs < -0.05) else 0.0,
                frac_active=float(np.mean(grs < -0.5)))
    x = D.eq_apply(x, VOICE_EQ)
    x, de = deess(x)
    pout = frame_power(x)
    mk = float(np.sqrt(p_in / (pout[ain].mean() + 1e-20)))
    x *= mk
    comp["makeup_db"] = float(20 * np.log10(mk))
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
    r = region.astype(np.int8)
    ch = np.flatnonzero(np.diff(np.concatenate([[1], r, [1]])))
    for a, b in zip(ch[0::2], ch[1::2]):
        if r[a:b].sum() == 0 and (b - a) >= int(min_gap * 100):
            gaps.append((int(a), int(b)))
    w = 100
    num = uniform_filter1d(Pv * act, w, mode="nearest")
    den = uniform_filter1d(act.astype(np.float64), w, mode="nearest")
    lev = 10 * np.log10(num / np.maximum(den, 1e-3) + 1e-12)
    lev = np.where(den > 0.05, lev, -26.0)
    lev = uniform_filter1d(lev, 150, mode="nearest")
    return dict(Pv=Pv, act=act, region=region, gaps=gaps, level_db=lev)


def depth_curve(level_db):
    """Konuşma düzeyine göre başlangıç ducking derinliği: sessiz konuşmada −11, yüksek konuşmada −14 dB (kapalı döngü SNR penceresine oturtur)."""
    return -11.0 - 3.0 * np.clip((level_db + 30.0) / 12.0, 0.0, 1.0)


def window_snr(Pv, Pm, act, G, lo, hi, mus=None):
    """[lo,hi) kare aralığında konuşma-müzik farkı (dB): konuşma-aktif (ve müzik-aktif) karelerde ortalama güçlerin oranı."""
    m = act[lo:hi] if mus is None else (act[lo:hi] & mus[lo:hi])
    if m.sum() < 200:
        return None
    pv = Pv[lo:hi][m].mean()
    pm = (Pm[lo:hi] * 10 ** (G[lo:hi] / 10.0))[m].mean()
    return 10 * np.log10(pv / (pm + 1e-20) + 1e-20)


def build_gain_curve(sa, Pm_raw, n_frames, chapters, bias=None, part=None, log_=log):
    """Müzik kazanç eğrisi (dB, 100 Hz): derinlik + pencere bazlı kapalı döngü seviyeleme (konuşma−müzik farkı [SNR_TARGET, SNR_HI]+bias aralığına
    çekilir; alt sınır sert, üst sınır sınırlı yükseltmeyle; müziğin sustuğu kareler hariç) + bölüm kartı/başlık yükselişleri."""
    Pv, act, region, gaps = sa["Pv"], sa["act"], sa["region"], sa["gaps"]
    mus = Pm_raw > 10 ** (MUSIC_ACTIVE_DB / 10.0)
    bias = np.zeros(n_frames) if bias is None else bias
    depth = depth_curve(sa["level_db"])
    G = depth.copy()
    W, H = 800, 200
    trims = np.zeros(n_frames)
    for it in range(6):
        trim_need = np.zeros(n_frames)
        boost = np.full(n_frames, np.inf)
        for lo in range(0, n_frames - W // 2, H):
            hi = min(n_frames, lo + W)
            s_ = window_snr(Pv, Pm_raw, act, G + trims, lo, hi, mus)
            if s_ is None:
                continue
            b_ = float(np.mean(bias[lo:hi]))
            if s_ < SNR_TARGET + b_:
                trim_need[lo:hi] = np.maximum(trim_need[lo:hi], SNR_TARGET + b_ - s_)
                boost[lo:hi] = 0.0
            else:
                b = float(np.clip(s_ - (SNR_HI + b_), 0.0, MAX_BOOST))
                boost[lo:hi] = np.minimum(boost[lo:hi], b)
        boost[~np.isfinite(boost)] = 0.0
        adj = np.where(trim_need > 0, -trim_need, boost)
        adj = uniform_filter1d(adj, 400, mode="nearest")
        if np.abs(adj).max() < 0.08:
            break
        trims += adj
    G = G + trims * region
    # ── bölüm kartı / başlık yükselişleri
    t_title = chapters[0]["t1"] if (part == 1 and chapters and chapters[0]["id"] == "c0") else None
    info_gaps = []
    for (a, b) in gaps:
        is_title = t_title is not None and abs(a / 100.0 - t_title) < 0.25
        d1, r1 = (-5, 50) if is_title else (12, 100)
        p1, r2 = 45, 45
        gd_a = G[max(a - 1, 0)]
        gd_b = G[min(b, n_frames - 1)] if b < n_frames else gd_a
        p0, p1_ = a + max(d1, 0) + int(r1 * 0.7), max(b - p1, a + 20)
        if p1_ <= p0:
            p0, p1_ = a, b
        Ppre = pre_level(Pm_raw, G, region, a)
        Pgap = Pm_raw[p0:p1_].mean() if p1_ > p0 else None
        if Ppre is None or Pgap is None or Pgap <= 1e-12:
            gopen = gd_a + BLOOM_DB
        else:
            gopen = 10 * np.log10(Ppre) + BLOOM_DB - 10 * np.log10(Pgap)
        gopen = float(np.clip(gopen, gd_a - 9.0, gd_a + 14.0))
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
        info_gaps.append(dict(a=a, b=b, p0=p0, p1=p1_, t0=a / 100.0, t1=b / 100.0, gain_change_db=round(gopen - gd_a, 2), open_db=round(gopen, 2),
                              title=bool(is_title)))
    G = uniform_filter1d(G, 7, mode="nearest")
    info = dict(gaps=info_gaps, trim_min=float(trims[region].min()), trim_max=float(trims[region].max()))
    return G, info


def pre_level(Pm_raw, G, region, a):
    """Boşluk öncesi son ~4 sn'lik konuşma karelerinde (G uygulanmış) ortalama müzik gücü (doğrusal)."""
    pre0, pre1 = max(a - 400, 0), max(a - 30, 1)
    sel = region[pre0:pre1]
    if sel.sum() < 20:
        return None
    return float((Pm_raw[pre0:pre1] * 10 ** (G[pre0:pre1] / 10.0))[sel].mean())


def measure_rises(Pm_final, region, gaps_info):
    """Nihai müzik gücünden ölçülen yükseliş: plato ortalaması − boşluk öncesi konuşma altı ortalaması (dB)."""
    out = []
    for g in gaps_info:
        a, p0, p1 = g["a"], g["p0"], g["p1"]
        pre0, pre1 = max(a - 400, 0), max(a - 30, 1)
        sel = region[pre0:pre1]
        if sel.sum() < 20 or p1 <= p0:
            out.append(None)
            continue
        pre = Pm_final[pre0:pre1][sel].mean()
        pl = Pm_final[p0:p1].mean()
        if pre < 1e-12 or pl < 1e-12:
            out.append(None)
            continue
        out.append(float(10 * np.log10(pl / (pre + 1e-20) + 1e-20)))
    return out


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
def default_sfx_cues(chapters, tail, part):
    """Varsayılan cue'lar: P1'de c0 sonunda title_hit (c0 t1 + 0,4 sn; c1 kartı = ana başlık, stinger yok); her bölüm kartında (parçanın 2. bölümünden itibaren)
    chapter_stinger — perde rengine göre (altin/bedel/miras), gelen bölümün ana sesine akortlu. P2/P3'ün ilk bölümünde kart yoktur (doğrudan açılır)."""
    import muzik
    cues = []
    start_i = 1
    if part == 1 and chapters and chapters[0]["id"] == "c0":
        cues.append(dict(t=round(chapters[0]["t1"] + muzik.TITLE_DELAY, 3), name="title_hit", gain_db=-9.0, pan=0.0, seed=0, dur=None, loop=False,
                         params={"root": float(D.midi_hz(muzik.CUES["c0"]["tonic"]))}, id="p1-ana-baslik", note="ana başlık vuruşu"))
        start_i = 2
    fl = PERDE_FLAVOR[part]
    gdb = {"altin": -9.0, "bedel": -12.5, "miras": -11.0}[fl]
    for i in range(start_i, len(chapters)):
        prev, ch = chapters[i - 1], chapters[i]
        root = float(D.midi_hz(muzik.first_tonic(ch["id"]) + 12))
        cues.append(dict(t=round(prev["t1"] + 0.2, 3), name="chapter_stinger", gain_db=gdb, pan=0.0, seed=i + 10 * part, dur=None, loop=False,
                         params={"root": root, "flavor": fl}, id=f"kart-{ch['id']}", note=f"bölüm kartı {ch['id']}"))
    return cues


def render_sfx_bus(cues, N, sa, region_s):
    """cue listesi → (N,2) float32 SFX bus.
    Cue alanları: t (sn, voice ekseni), name, gain_db, pan (−1…1), seed, dur (sn|null), loop (bool), isteğe bağlı duck_db (konuşma altında kısma dB;
    varsayılan döngülerde −4, tekil seslerde 0), fade_in/fade_out (sn; döngülerde varsayılan 1,2) ve params (ör. {"root": 146.8, "flavor": "bedel"}).
    Bilinmeyen ad / hatalı cue atlanır ve uyarılır."""
    import sfx
    bus = np.zeros((N, 2), dtype=np.float32)
    cache = {}
    used = []
    for c in cues:
        try:
            name = c["name"]
            t = float(c["t"])
            dur = c.get("dur")
            loop = bool(c.get("loop", False)) or (name in sfx.LOOPABLE and dur is not None)
            key = (name, int(c.get("seed", 0)), dur, loop, json.dumps(c.get("params", {}), sort_keys=True))
            if key not in cache:
                cache[key] = sfx.sfx(name, int(c.get("seed", 0)), dur, loop, **c.get("params", {}))
            x = cache[key].astype(np.float32)
            fi, fo = c.get("fade_in"), c.get("fade_out")
            if loop and dur is not None:
                fi = 1.2 if fi is None else fi
                fo = 1.2 if fo is None else fo
            if fi or fo:
                x = D.fade_edges(x, float(fi or 0.0), float(fo or 0.0)).astype(np.float32)
            g = D.db2lin(float(c.get("gain_db", 0.0)))
            gl, gr = D.pan_gains(float(c.get("pan", 0.0)))
            i = int(round(t * SR))
            if i >= N or i + len(x) <= 0:
                log(f"  UYARI: sfx cue aralık dışı atlandı: {name} t={t}")
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
        except Exception as e:  # noqa — tek hatalı cue tüm miksi düşürmesin
            log(f"  UYARI: sfx cue atlandı ({c.get('name')} t={c.get('t')}): {type(e).__name__}: {e}")
    return bus, used


def gather_sfx_cues(a, chapters, tail, timeline, gates):
    """Tüm SFX kaynaklarını birleştirir: sfx_cues_pN.json (proje kökü) + out_pN/sfx_gecis.json (otomatik geçiş sesleri) + varsayılan (başlık/kart vurguları).
    Çapalar timeline.json'dan çözülür; politika (çan yasağı) uygulanır; müzik sessizlik bölgelerinde otomatik geçiş sesi çalmaz."""
    import sfx
    sent = D.sent_index(timeline)
    quiet = [(g["a"], g["b"]) for g in gates if g.get("floor_db") is None or (g["floor_db"] is not None and g["floor_db"] <= -24)]
    raw, ayar = sfx.load_cue_file(a.sfx_cues)
    cues, warns = sfx.resolve_cues(raw, sent, chapters, quiet_zones=quiet, warn=lambda *x: log(*x))
    n_manual = len(cues)
    n_gecis = 0
    gp = os.path.join(OUT, "sfx_gecis.json")
    if os.path.exists(gp) and not a.no_gecis and ayar.get("gecis_sesleri", True):
        graw, _ = sfx.load_cue_file(gp)
        gc, gw = sfx.resolve_cues(graw, sent, chapters, quiet_zones=quiet, warn=lambda *x: log(*x))
        cues += gc
        warns += gw
        n_gecis = len(gc)
    n_def = 0
    if ayar.get("varsayilan_stinger", True) and not a.no_stinger:
        dc = default_sfx_cues(chapters, tail, PART)
        cues += dc
        n_def = len(dc)
    cues.sort(key=lambda c: c["t"])
    return cues, dict(manual=n_manual, gecis=n_gecis, default=n_def, warns=warns, ayar=ayar)


# ═══════════════════════════ master ═══════════════════════════
def master(mix, target=TARGET_LUFS, ceiling=CEILING_DB, hop=24):
    """mix (N,2) float32 → (y float32, bilgi). K-ağırlıklı güç ve true-peak zarfı BİR KEZ hop düzeyinde hesaplanır; kazanç ve
    limiter eğrisi hop düzeyinde yinelenir (saniyeler); sonuç gerçek BS.1770 ölçümüyle doğrulanıp gerekirse bir kez düzeltilir."""
    t = time.time()
    pk = D.k_power_hop(mix, hop)
    ph = D.hop_peaks(mix, hop)
    log(f"  master: K-ağırlıklı güç + true-peak zarfı hazır ({time.time() - t:.1f} sn)")
    ceil = D.db2lin(ceiling)
    g = target - D.lufs_from_hop_power(pk)
    for it in range(12):
        gl = D.limiter_curve(ph * D.db2lin(g), ceil, hop, 0.008, 0.120)
        L = D.lufs_from_hop_power(pk * D.db2lin(g) ** 2 * gl ** 2)
        err = target - L
        if abs(err) < 0.004:
            break
        g += err
    log(f"  master: kazanç {g:+.2f} dB, limiter maks. {-20 * np.log10(gl.min()):.2f} dB, tahmini {L:.3f} LUFS")
    y = None
    for fix in range(3):
        y = D.apply_hop_gain(mix, gl, D.db2lin(g), hop)
        st = D.loudness_stats(y)
        err = target - st["integrated"]
        log(f"  master: ölçülen {st['integrated']:.3f} LUFS (hata {err:+.3f})")
        if abs(err) < 0.03:
            break
        g += err
        gl = D.limiter_curve(ph * D.db2lin(g), ceil, hop, 0.008, 0.120)
    tp = D.true_peak_db(y)
    grdb = 20 * np.log10(gl + 1e-12)
    return y, dict(gain_db=float(g), stats=st, true_peak=float(tp), gr_max=float(-grdb.min()),
                   gr_frac_gt1=float(np.mean(grdb < -1.0)), gr_frac_gt3=float(np.mean(grdb < -3.0)), ceiling=float(ceiling))


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


def pyln_measure(x):
    """Bağımsız üçüncü ölçüm: pyloudnorm (BS.1770-4). x (N,2) float32. Yoksa None."""
    try:
        import pyloudnorm as pyln
        m = pyln.Meter(SR)
        return float(m.integrated_loudness(x.astype(np.float64)))
    except Exception as e:  # noqa
        log("  pyloudnorm ölçümü yapılamadı:", type(e).__name__)
        return None


def encode_m4a(wav, m4a):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", m4a], check=True)


def encode_flac(x, path):
    """float32 (N,) ya da (N,2) → 16-bit FLAC (ffmpeg boru hattı). Stem'ler disk dostu saklanır."""
    ch = 1 if x.ndim == 1 else x.shape[1]
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(ch), "-i", "-", "-c:a", "flac", "-sample_fmt", "s16", path],
                         stdin=subprocess.PIPE)
    step = 1 << 22
    for i in range(0, len(x), step):
        p.stdin.write(np.ascontiguousarray(x[i:i + step], dtype="<f4").tobytes())
    p.stdin.close()
    p.wait()


def encode_mp3(x, path, bitrate="160k", fade=0.25):
    """Önizleme kesiti → mp3 (libmp3lame). x (n,2) float32."""
    x = D.fade_edges(x, fade, fade).astype(np.float32)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libmp3lame", "-b:a", bitrate, path],
                         stdin=subprocess.PIPE)
    p.stdin.write(np.ascontiguousarray(x, dtype="<f4").tobytes())
    p.stdin.close()
    p.wait()


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
THIRD_OCT = [(63, 125), (125, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]


def band_energy(x):
    """x (N,) veya (N,2) → band payları (%) ve centroid (Hz), Welch ile."""
    m = x if x.ndim == 1 else (x[:, 0].astype(np.float64) + x[:, 1]) * 0.5
    m = m[: (len(m) // 8192) * 8192][::1]
    if len(m) < 8192:
        return [0.0, 0.0, 0.0], 0.0
    f, p = welch(m.astype(np.float64), SR, nperseg=8192, noverlap=0)
    tot = p.sum() + 1e-30
    out = []
    for name, lo, hi in BANDS:
        out.append(p[(f >= lo) & (f < hi)].sum() / tot * 100)
    cen = float((p * f).sum() / tot)
    return out, cen


def octave_profile(x):
    """Oktav bandı başına göreli düzey (dB; en güçlü bant = 0)."""
    m = x if x.ndim == 1 else (x[:, 0].astype(np.float64) + x[:, 1]) * 0.5
    m = m[: (len(m) // 8192) * 8192]
    if len(m) < 8192:
        return [0.0] * len(THIRD_OCT)
    f, p = welch(m.astype(np.float64), SR, nperseg=8192, noverlap=0)
    e = np.array([p[(f >= lo) & (f < hi)].sum() for (lo, hi) in THIRD_OCT]) + 1e-30
    e = 10 * np.log10(e)
    return list(e - e.max())


def rms_db_frames(x, mask_frames):
    """Kare maskesindeki kareler üzerinde ortalama güç (dBFS)."""
    P = frame_power(x, len(mask_frames))
    return 10 * np.log10(P[mask_frames].mean() + 1e-20)


def seg_rms_db(x, t0, t1):
    a, b = max(0, int(t0 * SR)), min(len(x), int(t1 * SR))
    if b <= a:
        return -200.0
    s = x[a:b].astype(np.float64)
    return float(10 * np.log10(np.mean(s * s) + 1e-20))


def clip_count(x, thr=0.9995):
    c = 0
    for i in range(0, len(x), 1 << 22):
        c += int(np.sum(np.abs(x[i:i + (1 << 22)]) >= thr))
    return c


def window_snr_stats(Pv, Pm_final, act, mus, W=800, H=400):
    """Parça boyunca 8 sn'lik pencerelerde konuşma−müzik farkı (dB) dağılımı (müzik-aktif ve konuşma-aktif karelerde)."""
    vals = []
    n = len(Pv)
    for lo in range(0, n - W // 2, H):
        hi = min(n, lo + W)
        m = act[lo:hi] & mus[lo:hi]
        if m.sum() < 300:
            continue
        vals.append(10 * np.log10(Pv[lo:hi][m].mean() / (Pm_final[lo:hi][m].mean() + 1e-20)))
    return np.array(vals)


# ═══════════════════════════ ana akış ═══════════════════════════
def main():
    ap = argparse.ArgumentParser(description="Medici parça miksi (voice + müzik + SFX)")
    ap.add_argument("--tail", type=float, default=7.0, help="bitiş ekranı (sn): mix = voice + tail (compose.OUTRO = 7)")
    ap.add_argument("--onizleme", action="store_true", help="geçici ses / eksik bölüm: çıktılar ONIZLEME_ önekiyle; assert_gercek_ses atlanır")
    ap.add_argument("--preview", action="store_true", help="out_pN/ses_onizleme/ altına 20–30 sn'lik mp3 kesitleri")
    ap.add_argument("--fresh", action="store_true", help="müzik önbelleğini yok say")
    ap.add_argument("--no-m4a", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--sfx-cues", default=None, help="varsayılan: proje kökünde sfx_cues_pN.json")
    ap.add_argument("--cache-dir", default=None, help="cue önbelleği (varsayılan: out_pN/_audio_cache; git'e girmez)")
    ap.add_argument("--no-stems", action="store_true", help="stem FLAC'lerini yazma")
    ap.add_argument("--keep-wav", action="store_true", help="mix_audio.wav'ı da sakla (varsayılan: ölçümden sonra silinir)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--snr", default=None, help="konuşma−müzik pencere sınırları 'LO,HI' dB (varsayılan 20,24)")
    ap.add_argument("--no-gecis", action="store_true", help="out_pN/sfx_gecis.json'u (otomatik geçiş sesleri) kullanma")
    ap.add_argument("--no-stinger", action="store_true", help="varsayılan başlık/kart vurgularını ekleme")
    a = ap.parse_args()
    global SNR_TARGET, SNR_HI
    if a.snr:
        SNR_TARGET, SNR_HI = [float(x) for x in a.snr.split(",")]
    if PART is None:
        raise SystemExit("MEDICI_PART=1|2|3 gerekli (out/ sembolik bağlantısı KULLANILMAZ): MEDICI_PART=2 python3 miks_kur.py")
    a.sfx_cues = a.sfx_cues or os.path.join(HERE, f"sfx_cues_p{PART}.json")

    import muzik
    import sfx
    voice, chapters, total, timeline = load_inputs()
    present = [c["id"] for c in chapters]
    missing = [c for c in expected_chapters() if c not in present]
    temp = os.path.exists(os.path.join(OUT, "GECICI_SES.json"))
    if not a.onizleme:
        PA.assert_gercek_ses(OUT)          # geçici ses varsa DURUR (SystemExit)
        if missing:
            raise SystemExit(f"DURDU: P{PART}'de eksik bölüm {missing} — final miks yapılmaz; önizleme için --onizleme kullanın.")
    onizleme = a.onizleme or temp or bool(missing)
    pref = "ONIZLEME_" if onizleme else ""
    if onizleme:
        log(f"*** ÖNİZLEME miksi (geçici ses: {temp}; eksik bölüm: {missing or '-'}) → çıktılar '{pref}' önekiyle; final adıyla YAZILMAZ ***")

    def P_(name):
        return os.path.join(OUT, pref + name)
    tail = float(a.tail)
    Nv = len(voice)
    if abs(Nv / SR - total) > 0.05:
        log(f"UYARI: voice.wav süresi {Nv / SR:.3f} sn ≠ voice_chapters.json total {total:.3f} sn (voice.wav esas alınır)")
    total = Nv / SR
    N = Nv + int(round(tail * SR))
    nf = N // FR
    log(f"P{PART}: voice {Nv / SR:.2f} sn + kuyruk {tail:.2f} sn = {N / SR:.2f} sn; {len(chapters)} bölüm ({', '.join(present)})")

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
    cache = None if a.fresh else (a.cache_dir or os.path.join(OUT, "_audio_cache"))
    music, minfo = muzik.render_music(chapters, total, tail, workers=min(a.workers or MAX_WORKERS, MAX_WORKERS), cache_dir=cache, seed=a.seed, timeline=timeline)
    assert len(music) == N, (len(music), N)
    log(f"müzik hazır ({minfo['render_sec']} sn), global kazanç {minfo['global_gain_db']:+.2f} dB, {len(minfo['cues'])} kesit, {len(minfo['gates'])} sessizlik kapısı")
    rms_nominal = muzik._robust_rms_db(music)

    # 4) müzik bus: EQ + ducking/yükseliş (bölüm başına SNR yanlılığı: snr_bias)
    music_eq = D.eq_apply(music, MUSIC_EQ).astype(np.float32)
    del music
    junc_steps = junction_raw_steps(chapters, music_eq)
    Pm_raw = frame_power(music_eq, nf)
    bias = np.zeros(nf)
    for c in minfo["cues"]:
        spec_bias = c.get("snr_bias", 0.0)
        if spec_bias:
            lo, hi = int(c["s0"] * 100), min(int(c["s1"] * 100), nf)
            bias[lo:hi] = spec_bias
    bias = uniform_filter1d(bias, 300, mode="nearest")
    G, ginfo = build_gain_curve(sa, Pm_raw, nf, chapters, bias=bias, part=PART, log_=log)
    music_d = apply_curve(music_eq, G)
    log(f"ducking eğrisi: konuşma bölgesi ort. {G[sa['region']].mean():+.2f} dB; yükseliş {len(ginfo['gaps'])} boşlukta; seviyeleme {ginfo['trim_min']:+.2f} … {ginfo['trim_max']:+.2f} dB")

    # 5) SFX bus
    cues, sinfo = gather_sfx_cues(a, chapters, tail, timeline, minfo["gates"])
    log(f"sfx: {len(cues)} cue (elle {sinfo['manual']} + geçiş {sinfo['gecis']} + varsayılan {sinfo['default']}); uyarı {len(sinfo['warns'])}")
    sfxbus, used = render_sfx_bus(cues, N, sa, region_s)
    json.dump(cues, open(P_("sfx_cues_used.json"), "w"), indent=1, ensure_ascii=False)

    # 6) toplam + master
    mix = music_d.copy()
    mix[:, 0] += vfull
    mix[:, 1] += vfull
    mix += sfxbus
    pre = D.loudness_stats(mix)
    log(f"miks (master öncesi): {pre['integrated']:.2f} LUFS")
    final, minf = master(mix, TARGET_LUFS, CEILING_DB)
    del mix
    wav_path = P_("mix_audio.wav")
    m4a_path = P_("mix_audio.m4a")
    D.write_wav(wav_path, final, SR, 16)
    log(f"{os.path.basename(wav_path)} yazıldı: {minf['stats']['integrated']:.2f} LUFS, TP {minf['true_peak']:.2f} dBTP")

    m4a_info = None
    ceiling = CEILING_DB
    if not a.no_m4a and shutil.which("ffmpeg"):
        for attempt in range(3):
            encode_m4a(wav_path, m4a_path)
            tmp = P_("_m4a_check.wav")
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
            if attempt == 2:
                log(f"  UYARI: AAC sonrası true-peak {tp_m4a:.2f} dBTP > −1,0 (3 deneme sonrası)")
                break
            ceiling -= (tp_m4a + 1.0) + 0.15
            log(f"  AAC sonrası TP aşımı → tavan {ceiling:.2f} dBTP ile yeniden")
            mix2 = music_d.copy()
            mix2[:, 0] += vfull
            mix2[:, 1] += vfull
            mix2 += sfxbus
            final, minf = master(mix2, TARGET_LUFS, ceiling)
            del mix2
            D.write_wav(wav_path, final, SR, 16)
    else:
        log("m4a atlandı")

    # 7) ölçüm/QA
    ff = ffmpeg_loudnorm(wav_path)
    pyl = pyln_measure(final)
    ctx = dict(a=a, chapters=chapters, total=total, tail=tail, N=N, vinfo=vinfo, sa=sa, G=G, ginfo=ginfo, minfo=minfo, minf=minf, m4a=m4a_info, ff=ff, pyl=pyl,
               voice_raw=voice_raw_full, vproc=vfull, music=music_d, sfxbus=sfxbus, final=final, rms_nominal=rms_nominal, cues=cues, used=used, sinfo=sinfo,
               nf=nf, pre=pre, timeline=timeline, region_s=region_s, onizleme=onizleme, temp=temp, missing=missing, pref=pref, Pm_raw=Pm_raw, bias=bias, junc_steps=junc_steps)
    report = write_report(ctx)
    open(P_("audio_report.txt"), "w", encoding="utf-8").write(report + "\n")
    print(report)
    if not a.no_stems:
        t = time.time()
        encode_flac(music_d, P_("stem_music.flac"))
        encode_flac(vfull, P_("stem_voice.flac"))
        encode_flac(sfxbus, P_("stem_sfx.flac"))
        log(f"stem'ler yazıldı (FLAC; {time.time() - t:.0f} sn)")
    if a.preview:
        write_previews(ctx)
    if not a.keep_wav and os.path.exists(wav_path):
        os.remove(wav_path)
    log("bitti.")


# ═══════════════════════════ rapor ═══════════════════════════
def timeline_check(timeline, act, nf, chapters):
    """timeline.json ↔ voice.wav uyumu: cümle içi konuşma payı (≥0,85 beklenir), cümle arası aralıkta konuşma payı (≤0,3),
    bölüm sınırları (ilk cümle başı / son cümle sonu ↔ bölüm t0/t1)."""
    if not timeline:
        return None
    S = timeline["sentences"]
    inside, between = [], []
    for k, sn in enumerate(S):
        lo, hi = int(sn["t0"] * 100), min(int(sn["t1"] * 100), nf)
        if hi > lo + 5:
            inside.append(float(act[lo:hi].mean()))
        if k + 1 < len(S) and S[k + 1]["ch"] == sn["ch"]:
            g0, g1 = int(sn["t1"] * 100) + 5, int(S[k + 1]["t0"] * 100) - 5
            if g1 > g0 + 10:
                between.append(float(act[g0:g1].mean()))
    offs = []
    for ch in chapters:
        ss = [x for x in S if x["ch"] == ch["id"]]
        if ss:
            offs.append((ch["id"], ss[0]["t0"] - ch["t0"], ch["t1"] - ss[-1]["t1"]))
    return dict(n=len(S), inside_mean=float(np.mean(inside)), inside_min=float(np.min(inside)), n_low=int(np.sum(np.array(inside) < 0.8)),
                between_mean=float(np.mean(between)) if between else 0.0, offs=offs, total=timeline.get("total"))


def junction_raw_steps(chapters, music_eq):
    """Kavşak (bölüm kartı boşluğunun ortası) çevresinde (±8 sn) ham müzik bandının (ducking ÖNCESİ) 1 sn RMS dizisi → en büyük ardışık adım (dB).
    Ham bantta kart etkisi (yükseliş) yoktur; çapraz geçişlerin (kesit sınırı) dB sıçrama yapıp yapmadığını ölçer."""
    out = []
    for i in range(len(chapters) - 1):
        a = chapters[i]
        tc = a["t1"] + a.get("gap_after", 3.0) / 2
        seg = music_eq[max(int((tc - 8.0) * SR), 0):int((tc + 8.0) * SR)]
        mm = seg.mean(axis=1)
        nwin = len(mm) // SR
        r = 10 * np.log10(np.mean(mm[:nwin * SR].reshape(nwin, SR).astype(np.float64) ** 2, axis=1) + 1e-14)
        out.append(float(np.max(np.abs(np.diff(r)))) if len(r) > 1 else 0.0)
    return out


def junction_report(chapters, final, steps):
    """Bölümler arası geçiş sıçramaları: (1) nihai mikste, konuşmalı bölgelerde 12 sn'lik entegre LUFS farkı (önceki bölümün sonu ↔ sonraki bölümün başı);
    (2) ham müzik bandında kavşak çevresi en büyük 1 sn adımı (junction_raw_steps)."""
    rows = []
    for i in range(len(chapters) - 1):
        a, b = chapters[i], chapters[i + 1]
        la = D.loudness_stats(final[int(max(a["t1"] - 12.0, a["t0"]) * SR):int((a["t1"] - 0.3) * SR)])["integrated"]
        lb = D.loudness_stats(final[int((b["t0"] + 0.3) * SR):int(min(b["t0"] + 12.0, b["t1"]) * SR)])["integrated"]
        rows.append(dict(a=a["id"], b=b["id"], lufs_a=float(la), lufs_b=float(lb), d=float(lb - la), music_step=float(steps[i])))
    return rows


def write_report(c):
    import muzik
    from collections import Counter
    L = []
    P = L.append
    a, chapters, total, tail, N = c["a"], c["chapters"], c["total"], c["tail"], c["N"]
    vinfo, sa, G, ginfo, minfo, minf, m4a, ff = c["vinfo"], c["sa"], c["G"], c["ginfo"], c["minfo"], c["minf"], c["m4a"], c["ff"]
    voice_raw, vproc, music, sfxbus, final = c["voice_raw"], c["vproc"], c["music"], c["sfxbus"], c["final"]
    nf, st = c["nf"], minf["stats"]
    act = sa["act"]
    ttl = "ÖNİZLEME " if c["onizleme"] else ""
    P(f"MEDICI — PARÇA {PART} — {ttl}SES RAPORU (miks.py)")
    P("=" * 80)
    if c["onizleme"]:
        P(f"*** ÖNİZLEME: geçici (Piper) ses = {c['temp']}; eksik bölüm = {c['missing'] or '-'}. Bu miks NİHAİ DEĞİLDİR; çıktı adları '{c['pref']}' önekli; gerçek ses gelince "
          f"(çıpalar yeniden çözülür) `MEDICI_PART={PART} python3 miks_kur.py` ile yeniden üretin. ***")
    P(f"süre: mix {N / SR:.3f} sn = voice {total:.3f} + bitiş ekranı {tail:.2f}; 48 kHz stereo; çıktı AAC 192k (+ FLAC stem'ler)")
    P(f"bölümler: {', '.join(x['id'] for x in chapters)}; konuşma−müzik penceresi: [{SNR_TARGET:.0f}, {SNR_HI:.0f}] dB (bölüm yanlılığı: snr_bias)")
    P("")
    P("[1] NİHAİ MİKS")
    P(f"  entegre loudness (BS.1770, kendi ölçümüm) : {st['integrated']:.2f} LUFS   (hedef −14,0)")
    if ff:
        P(f"  ffmpeg loudnorm ölçümü (bağımsız)          : {ff.get('input_i')} LUFS ; LRA {ff.get('input_lra')} LU ; eşik {ff.get('input_thresh')}")
    if c["pyl"] is not None:
        P(f"  pyloudnorm ölçümü (bağımsız, üçüncü)       : {c['pyl']:.2f} LUFS")
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
    snr_all = rms_db_frames(vproc, act) - rms_db_frames(music, act)
    sfx_all = rms_db_frames(sfxbus, act)
    P(f"  konuşma RMS (işlenmiş, ön-master) : {rms_db_frames(vproc, act):.1f} dBFS   (ham ses {rms_db_frames(voice_raw, act):.1f})")
    P(f"  müzik RMS (konuşma altında)       : {rms_db_frames(music, act):.1f} dBFS   → konuşma − müzik = {snr_all:.1f} dB   (hedef {SNR_TARGET:.0f}…{SNR_HI:.0f})")
    P(f"  SFX RMS (konuşma karelerinde)     : {sfx_all:.1f} dBFS")
    P(f"  müzik bandı ort. RMS (ducking öncesi, nominal): {c['rms_nominal']:.1f} dBFS   (şart −24…−28)")
    reg = sa["region"]
    mus = c["Pm_raw"] > 10 ** (MUSIC_ACTIVE_DB / 10.0)
    Pv, Pm = frame_power(vproc, nf), frame_power(music, nf)
    wv = window_snr_stats(Pv, Pm, act, mus)
    P(f"  8 sn pencerelerde konuşma−müzik (n={len(wv)}): p5 {np.percentile(wv, 5):.1f} · p25 {np.percentile(wv, 25):.1f} · medyan {np.median(wv):.1f} · p75 {np.percentile(wv, 75):.1f} · p95 {np.percentile(wv, 95):.1f} dB; "
      f"[{SNR_TARGET - 1:.0f}, {SNR_HI + 2:.0f}] içinde %{100 * np.mean((wv >= SNR_TARGET - 1) & (wv <= SNR_HI + 2)):.0f}")
    P(f"  DUCK DERİNLİĞİ (müzik kazancı; nominal bandına göre, konuşma bölgesi): ort. {G[reg].mean():+.2f} dB, aralık {G[reg].min():+.1f} … {G[reg].max():+.1f}; "
      f"kapalı döngü seviyeleme {ginfo['trim_min']:+.2f} … {ginfo['trim_max']:+.2f} dB")
    P("  bölüm bazında (konuşma-aktif kareler; kare = 10 ms):")
    P("   bölüm   konuşma   müzik    fark   ducking ort.   en kötü 8 sn penceresi   en iyi 8 sn")
    worst_all, best_all = 99.0, -99.0
    for ch in chapters:
        lo, hi = int(ch["t0"] * 100), min(int(ch["t1"] * 100), nf)
        m = act[lo:hi]
        pv = Pv[lo:hi][m].mean()
        pm = Pm[lo:hi][m].mean()
        w = 800
        ws, wb = 99.0, -99.0
        for s0 in range(lo, hi - w // 2, 200):
            s1 = min(hi, s0 + w)
            mm = act[s0:s1] & mus[s0:s1]
            if mm.sum() >= 300:
                v = 10 * np.log10(Pv[s0:s1][mm].mean() / (Pm[s0:s1][mm].mean() + 1e-20))
                ws, wb = min(ws, v), max(wb, v)
        worst_all, best_all = min(worst_all, ws), max(best_all, wb)
        dk = G[lo:hi][sa["region"][lo:hi]].mean()
        P(f"   {ch['id']:5s} {10 * np.log10(pv):7.1f}  {10 * np.log10(pm + 1e-20):7.1f}  {10 * np.log10(pv / (pm + 1e-20)):6.1f}   {dk:+6.1f} dB      {ws:6.1f} dB          {wb:6.1f} dB")
    P(f"  en kötü 8 sn penceresi (tüm bölümler): {worst_all:.1f} dB ; en iyi: {best_all:.1f} dB")
    rises = measure_rises(Pm, reg, ginfo["gaps"])
    P("  bölüm kartı / başlık boşluklarında müzik yükselişi (ölçülen: plato − konuşma altı düzey; hedef 8–10 dB):")
    for g, r in zip(ginfo["gaps"], rises):
        rs = "   ölçülemedi" if r is None else f"   yükseliş {r:+5.1f} dB"
        P(f"   t={g['t0']:8.2f}–{g['t1']:8.2f} sn{rs}   (kazanç değişimi {g['gain_change_db']:+.1f} dB)" + ("   [ana başlık]" if g["title"] else ""))
    P("  bölüm bazında nihai miks loudness (gerçek BS.1770; bölüm süresi boyunca, kart boşlukları hariç):")
    P("   bölüm  entegre LUFS  kısa-dönem maks.  anlık maks.")
    chl = []
    for ch in chapters:
        a_, b_ = int(ch["t0"] * SR), min(int(ch["t1"] * SR), len(final))
        sc = D.loudness_stats(final[a_:b_])
        chl.append(sc["integrated"])
        P(f"   {ch['id']:5s} {sc['integrated']:10.2f}   {sc['shortterm_max']:12.1f}   {sc['momentary_max']:10.1f}")
    P("")
    P("[3] BÖLÜMLER ARASI GEÇİŞ SIÇRAMALARI (dB)")
    P("   geçiş       mikste 12 sn LUFS (önceki sonu → sonraki başı)    fark     ham müzik bandında maks. 1 sn adımı (±8 sn)")
    jr = junction_report(chapters, final, c["junc_steps"])
    for r in jr:
        P(f"   {r['a']:>4s}→{r['b']:<4s}  {r['lufs_a']:8.2f} → {r['lufs_b']:8.2f}                          {r['d']:+5.2f}      {r['music_step']:5.1f}")
    P("")
    P("[4] SESSİZLİK BÖLGELERİ (müzik kapıları; c7 yıldız an vb.)")
    P("   kesit   başlangıç–bitiş (sn)   tür             müzik RMS (ducking sonrası)   SFX RMS   miks−ses RMS (kestirim)   not")
    gate_rows = []
    for g in minfo["gates"]:
        a0, b0 = g["a"], g["b"]
        m_db = seg_rms_db(music, a0, b0)
        s_db = seg_rms_db(sfxbus, a0, b0)
        nov = 10 * np.log10(10 ** (m_db / 10) + 10 ** (s_db / 10) + 1e-20)
        kind = "TAM SESSİZ" if g["floor_db"] is None else f"kısık ({g['floor_db']} dB)"
        gate_rows.append((g, m_db, s_db, kind))
        P(f"   {g['seg']:6s} {a0:8.2f}–{b0:8.2f}   {kind:14s}  {m_db:8.1f} dBFS                {s_db:8.1f}   {nov + minf['gain_db']:8.1f} dBFS (final ölçeği)   {g.get('note', '')}")
    if not minfo["gates"]:
        P("   (bu parçada tanımlı kapı yok)")
    P("")
    P("[5] SPEKTRAL DENGE (Welch, güç payı %)  düşük<250 Hz | orta 250–4k | yüksek>4k | centroid")
    for nm, arr in (("voice (ham)", voice_raw), ("voice (işlenmiş)", vproc), ("müzik (mikste)", music), ("sfx bus", sfxbus), ("MIKS (nihai)", final)):
        b, cen = band_energy(arr)
        P(f"  {nm:18s} {b[0]:5.1f} | {b[1]:5.1f} | {b[2]:5.1f} | {cen:6.0f} Hz")
    P("  oktav profili (göreli dB; bantlar 63–125–250–500–1k–2k–4k–8k–16k Hz):")
    for nm, arr in (("voice (işlenmiş)", vproc), ("müzik (mikste)", music), ("MIKS (nihai)", final)):
        P(f"    {nm:18s} " + " ".join(f"{v:6.1f}" for v in octave_profile(arr)))
    P("")
    P("[6] SES (voice) ZİNCİRİ")
    cc = vinfo["compressor"]
    P(f"  HPF 80 Hz; sıkıştırıcı 2:1 / −24 dBFS / 10 ms / 120 ms (maks. azaltma {cc['max_gr']:.1f} dB, aktifken ort. {cc['mean_gr_active']:.1f} dB, süre %{cc['frac_active'] * 100:.1f}); makyaj kazancı {cc['makeup_db']:+.1f} dB (ham ses düzeyine);")
    P(f"  +1,5 dB @3 kHz presence; 7 kHz üstü yüksek raf −2,5 dB + dinamik de-ess (5,2–9,8 kHz; eşik {vinfo['deess']['thr_db']:.1f} dB, maks. {vinfo['deess']['max_gr']:.1f} dB)")
    P("")
    P("[7] MÜZİK KESİTLERİ (ham bant; bölüm/kesit başına karakter)")
    P("  kesit    ruh       mod         bpm  ölçü  başlangıç  bitiş    uzunluk  (bölüm süresi)  çapraz geçiş (giriş/çıkış)  ön-kazanç  snr_bias  olay/tema/kapı")
    for ci in minfo["cues"]:
        P(f"  {ci['id']:7s} {ci['mood']:9s} {ci['mode']:10s} {ci['bpm']:4d}  {ci['meter']:4s} {ci['start']:9.2f} {ci['end']:8.2f} {ci['length']:8.2f}  ({ci['chapter_dur']:6.2f})        {ci['xin']:.0f} / {ci['xout']:.0f} sn          {ci['pre_gain_db']:+.1f} dB   {ci['snr_bias']:+.1f}    {ci['events']}/{ci['themes']}/{ci['gates']}")
    ir = D.hall_ir(2.2)
    rt = D.measure_rt60(ir[:, 0])
    P(f"  reverb: algoritmik salon IR'ı, fftconvolve; ölçülen RT60: 500 Hz {rt[500]:.2f} sn, 1 kHz {rt[1000]:.2f} sn (ort. {0.5 * (rt[500] + rt[1000]):.2f} sn), 2 kHz {rt[2000]:.2f} sn")
    if PART == 1 and chapters[0]["id"] == "c0":
        P(f"  c0 başlık vuruşu: c0 t1 + {muzik.TITLE_DELAY:.1f} sn = {chapters[0]['t1'] + muzik.TITLE_DELAY:.2f} sn")
    P(f"  parça kapanışı: son bölüm t1 = {chapters[-1]['t1']:.2f} → çözülme {chapters[-1]['t1'] + 0.25:.2f} sn, sönüş {N / SR:.2f} sn (kuyruk {tail:.1f} sn)")
    P("")
    P("[8] SFX")
    cnt = Counter(c["used"])
    si = c["sinfo"]
    P(f"  cue sayısı: {len(c['cues'])} (elle/JSON {si['manual']}, otomatik geçiş {si['gecis']}, varsayılan başlık/kart {si['default']}); kullanılan: " + ", ".join(f"{k}×{v}" for k, v in sorted(cnt.items())))
    for w in si["warns"]:
        P("   uyarı: " + w)
    import sfx
    P(f"  kütüphane ({len(sfx.SFX_NAMES)}): " + ", ".join(sfx.SFX_NAMES))
    P("")
    tc = timeline_check(c["timeline"], act, nf, chapters)
    P("[9] ZAMAN ÇİZELGESİ UYUMU (timeline.json ↔ voice.wav)")
    if tc:
        P(f"  {tc['n']} cümle; cümle içinde konuşma payı ort. {tc['inside_mean']:.3f} (en düşük {tc['inside_min']:.2f}); cümle arası aralıkta konuşma payı ort. {tc['between_mean']:.3f} (≈0 beklenir)")
        bad = [(i, a_, b_) for (i, a_, b_) in tc["offs"] if abs(a_) > 0.6 or abs(b_) > 0.6]
        P("  bölüm sınırı kayması (ilk cümle başı − t0 | t1 − son cümle sonu): " + "; ".join(f"{i}: {a_:+.2f}/{b_:+.2f}" for (i, a_, b_) in tc["offs"]))
        P("  " + ("UYARI: >0,6 sn kayma: " + ", ".join(i for i, _, _ in bad) if bad else "tüm bölüm sınırları ≤0,6 sn içinde uyumlu"))
    else:
        P("  timeline.json yok / okunamadı")
    P("")
    P("[10] KONTROL LİSTESİ")
    chk = []

    def ck(name, ok, val):
        chk.append((name, ok, val))
    ck("entegre loudness −14 ± 0,5 LUFS", abs(st["integrated"] + 14) <= 0.5, f"{st['integrated']:.2f}")
    if c["pyl"] is not None:
        ck("pyloudnorm bağımsız ölçüm −14 ± 0,6 LUFS", abs(c["pyl"] + 14) <= 0.6, f"{c['pyl']:.2f}")
    ck("true-peak ≤ −1,0 dBTP (wav)", minf["true_peak"] <= -1.0, f"{minf['true_peak']:.2f}")
    if m4a:
        ck("true-peak ≤ −1,0 dBTP (m4a çözülmüş)", m4a["tp"] <= -1.0, f"{m4a['tp']:.2f}")
    ck("kırpılan örnek sayısı = 0", clip_count(final) == 0, str(clip_count(final)))
    ck("DC ofset < 1e-3", float(np.max(np.abs(dc))) < 1e-3, f"{np.max(np.abs(dc)):.1e}")
    ck(f"konuşma − müzik genel ≥ {SNR_TARGET - 1:.0f} dB", snr_all >= SNR_TARGET - 1.0, f"{snr_all:.1f}")
    ck(f"konuşma − müzik en kötü 8 sn pencere ≥ {SNR_TARGET - 1.5:.1f} dB", worst_all >= SNR_TARGET - 1.5, f"{worst_all:.1f}")
    ck("konuşma − müzik pencerelerinin %80'i [hedef−1, hedef_üst+2] içinde", np.mean((wv >= SNR_TARGET - 1) & (wv <= SNR_HI + 2)) >= 0.8,
       f"%{100 * np.mean((wv >= SNR_TARGET - 1) & (wv <= SNR_HI + 2)):.0f}")
    ck("müzik nominal ort. RMS −24…−28 dBFS", -28.2 <= c["rms_nominal"] <= -23.8, f"{c['rms_nominal']:.1f}")
    ck("süre = voice + kuyruk (±1 örnek)", abs(len(final) - N) <= 1, f"{len(final) / SR:.3f} sn")
    rv = [r for r in rises if r is not None]
    ck("boşluk yükselişi 8–10 dB (ölçülen, ±0,7)", bool(rv) and all(7.3 <= r <= 10.7 for r in rv), f"min {min(rv):.1f} maks {max(rv):.1f}" if rv else "-")
    if jr:
        ck("geçişte 12 sn LUFS sıçraması ≤ 1,5 dB (tüm geçişler)", all(abs(r["d"]) <= 1.5 for r in jr), f"maks {max(abs(r['d']) for r in jr):.2f}")
        ck("ham müzik bandında kavşak 1 sn adımı ≤ 4 dB", all(r["music_step"] <= 4.0 for r in jr), f"maks {max(r['music_step'] for r in jr):.1f}")
    for (g, m_db, s_db, kind) in gate_rows:
        if g["floor_db"] is None:
            ck(f"sessizlik bölgesi {g['seg']} {g['a']:.1f}–{g['b']:.1f}: müzik ≤ −80 dBFS", m_db <= -80.0, f"{m_db:.1f}")
    if tc:
        okb = all(abs(a_) <= 0.6 and abs(b_) <= 0.6 for (_, a_, b_) in tc["offs"])
        ck("timeline.json uyumu (cümle içi konuşma ≥ 0,70; cümle arası ≤ 0,10; bölüm sınırı ≤ 0,6 sn)",
           tc["inside_mean"] >= 0.70 and tc["between_mean"] <= 0.10 and okb, f"{tc['inside_mean']:.3f} / {tc['between_mean']:.3f}")
    for name, ok, val in chk:
        P(f"  [{'GEÇTİ' if ok else 'KALDI'}] {name}  → {val}")
    P("")
    P(f"YENİDEN ÜRETME (tek komut): MEDICI_PART={PART} python3 miks_kur.py" + (" --onizleme" if c["onizleme"] else "") + "     (+ --preview ile out_pN/ses_onizleme/ mp3 kesitleri)")
    P(f"  girdiler : out_p{PART}/voice.wav, voice_chapters.json, timeline.json, sfx_cues_p{PART}.json, [out_p{PART}/sfx_gecis.json]")
    P(f"  çıktılar : out_p{PART}/{c['pref']}mix_audio.m4a, {c['pref']}stem_music|voice|sfx.flac, {c['pref']}sfx_cues_used.json, {c['pref']}audio_report.txt")
    P(f"toplam çalışma süresi: {time.time() - T0:.0f} sn")
    c["_chk"] = chk
    return "\n".join(L)


# ═══════════════════════════ önizleme mp3'leri ═══════════════════════════
PREVIEWS = {
    1: [("01_c0_baslik_vurusu", ("c0s16", 0.0), 30, True, "c0 sonu: yükseliş → TEK vuruş → altın D majör → florin figürü (ana başlık)"),
        ("02_c1_florin_ve_veba", ("c1s28", 0.0), 28, True, "c1: sermaye on bin florin (florin motifi) — kısa kesit"),
        ("03_c1_veba_ve_ciompi", ("c1s13", 0.0), 30, True, "c1: veba (renk solar) → Ciompi (davul yükselir)"),
        ("04_c3_donus_1434", ("c3s16", 0.0), 28, True, "c3: Cosimo'nun dönüşü ('dönüş' motifi)"),
        ("05_c4_kubbe_kutsama", ("c4s8", 0.0), 30, True, "c4: kubbe + kutsama korali (duomo motifi)"),
        ("06_c5_lir_ve_lorenzo", ("c5s10", 0.0), 28, True, "c5: Orfik lir kadansı ... Lorenzo'ya geçiş"),
        ("07_c6_lorenzo_temasi", ("c6s17", 0.0), 28, True, "c6: Lorenzo teması (c6 sesi gelince)"),
        ("08_p1_kapanis_golge", ("c6s25", 0.0), 30, True, "P1 sonu: altın → gölge, bedel yayı, 7 sn çözülme (c6 sesi gelince)")],
    2: [("01_c7_acilis_parca_basligi", 0.0, 26, True, "P2 açılışı: 'bedel' yayı (başlık bindirmesi 1,2–4,8 sn), kilise girişinde müzik çekilir"),
        ("02_c7_yildiz_an_girisi", ("c7s14", 0.0), 30, True, "c7 V4→V5: müzik sessizliğe giriş (0,6 sn önce) — YILDIZ AN"),
        ("03_c7_yildiz_an_cikisi", ("c7s22", 0.0), 30, True, "c7 V7→V8: tunç kapı, sessizlikten yavaş dönüş"),
        ("04_c7_palle_meydan", ("c7s29", 0.0), 28, True, "c7 V10: 'palle, palle' (altılı ritim) ve Lorenzo pencerede"),
        ("05_c8_konuk_mu_rehine_mi", ("c8s10", 0.0), 28, True, "c8: müzik çekilir — 'Konuk muydu, rehine mi?'"),
        ("06_c8_isiklar_sonuyor", ("c8s33", 0.0), 30, True, "c8 sonu: şube ışıkları birer birer sönüyor"),
        ("07_c10_9_kasim", ("c10s12", 0.0), 30, True, "c10: 9 Kasım — kısa vuruşlar, kapı, 1 sn sessizlik, uzak trompet"),
        ("08_c10_ates", ("c10s24", 0.0), 30, True, "c10: ilk ateş ... (ateş çıtırtısı + ağır org)"),
        ("09_c11_roma_1527", ("c11s16", 0.0), 30, True, "c11: Roma 1527 — sakin sayaç, ağır"),
        ("10_p2_kapanis_nasil", ("c11s36", 0.0), 30, True, "P2 sonu: Alessandro → 'Nasıl?' → çözülmeyen sus4, 7 sn çözülme")],
    3: [("01_c12_acilis_parca_basligi", 0.0, 26, True, "P3 açılışı: 'miras' hücresi (başlık bindirmesi), makine gibi tık-tık"),
        ("02_c12_uffizi", ("c12s11", 0.0), 28, True, "c12: Uffizi kendini kurar (Vasari koridoru)"),
        ("03_c12_1562_sessizlik", ("c12s19", 0.0), 30, True, "c12: 1562 — neredeyse sessizlik, 'dört haftada üç ölüm'de tam sessizlik"),
        ("04_c13_catherine_marie", ("c13s22", 0.0), 30, True, "c13: Catherine → Marie (A aeolian → C lidyen, kesit geçişi)"),
        ("05_c13_1572_sessizlik", ("c13s11", 0.0), 30, True, "c13: 1572 — ses çekilir, tam sessizlik 3 sn (çan yok)"),
        ("06_c14_yildizlar", ("c14s11", 0.0), 30, True, "c14: Galileo'nun dört yıldızı (klavsen)"),
        ("07_c14_euridice_recitativo", ("c14s7", 0.0), 30, True, "c14: Euridice — özgün recitativo-tarzı süreklilik"),
        ("08_c15_yorgun", ("c15s17", 0.0), 30, True, "c15: yorgun, seyrek — soy ağacı solar"),
        ("09_c16_donus_ters_motif", ("c16s1", 0.0), 30, True, "c16: c0'ın odası — 'miras' hücresi TERS çevrilmiş"),
        ("10_p3_kapanis", ("c16s24", 0.0), 30, True, "P3 sonu: çözülüş, son lavta notası, son sessizlik")],
}


def write_previews(c):
    """out_pN/ses_onizleme/*.mp3: nihai miksten 26–30 sn'lik kesitler (+ ham müzik kesitleri, RMS −20 dBFS'e normalli) + OKU_BENI.txt."""
    import muzik
    sent = D.sent_index(c["timeline"])
    pdir = os.path.join(OUT, "ses_onizleme")
    os.makedirs(pdir, exist_ok=True)
    pref = c["pref"]
    log(f"önizleme mp3'leri → {pdir}")
    final, music_d = c["final"], c["music"]
    G = c["G"]
    gl = (10 ** (-G / 20.0)).astype(np.float32)
    lines = []
    for (stem, start, dur, with_music, label) in PREVIEWS.get(PART, []):
        t0 = D.anchor_time(start, sent) if not isinstance(start, (int, float)) else float(start)
        if t0 is None:
            lines.append(f"  (atlandı: {stem} — çapa çözülemedi: {start})")
            continue
        t0 = max(0.0, t0 - 1.0)
        t1 = min(t0 + dur, len(final) / SR)
        ex = final[int(t0 * SR):int(t1 * SR)]
        if len(ex) < 5 * SR:
            lines.append(f"  (atlandı: {stem} — kesit çok kısa)")
            continue
        encode_mp3(ex, os.path.join(pdir, f"{pref}{stem}_mix.mp3"))
        if with_music:
            i0, i1 = int(t0 * SR), int(t1 * SR)
            fr = (np.arange(i0, i1) / float(FR)).astype(np.int64).clip(0, len(gl) - 1)
            raw = (c["music"][i0:i1] * gl[fr][:, None]).astype(np.float32)        # ducking öncesi (ham) bant
            r = float(np.sqrt(np.mean(raw.astype(np.float64) ** 2)) + 1e-12)
            if r > 1e-5:
                y = raw * (D.db2lin(-20.0) / r)
                pk = float(np.max(np.abs(y)))
                if pk > D.db2lin(-3.0):
                    y = y * (D.db2lin(-3.0) / pk)
                encode_mp3(y.astype(np.float32), os.path.join(pdir, f"{pref}{stem}_muzik.mp3"))
        lines.append(f"  {pref}{stem}_mix.mp3 (+_muzik.mp3)  t={t0:7.1f}–{t1:7.1f} sn  — {label}")
    # SFX demo
    try:
        import sfx
        demo = []
        gap = np.zeros((int(0.5 * SR), 2), dtype=np.float32)
        for nm in ("page_turn", "quill_scratch", "wax_seal_stamp", "stamp_thud", "coin_clink", "door_bolt", "lock_click", "door_bronze", "crowd_murmur", "crowd_chant",
                   "fire_crackle", "horse_hooves", "hoof_far", "sea_waves", "rope_creak", "paper_rustle", "keyboard_action", "glass_chime", "candle_flame", "distant_trumpet"):
            x = sfx.sfx(nm, 0, 3.0 if nm in sfx.LOOPABLE else None)
            x = x[:int(4.0 * SR)]
            demo += [(x * 0.35).astype(np.float32), gap]
        encode_mp3(np.concatenate(demo), os.path.join(pdir, f"{pref}00_sfx_katalog_demo.mp3"), fade=0.05)
        lines.append(f"  {pref}00_sfx_katalog_demo.mp3  — SFX kataloğundan seçmeler (sırayla: sayfa, kalem, mühür, damga, sikke, sürgü, kilit, tunç kapı, kalabalık, haykırış, ateş, nal, uzak at, deniz, halat, kâğıt, klavye, cam, mum, trompet)")
    except Exception as e:   # noqa
        lines.append(f"  (SFX demo yazılamadı: {type(e).__name__}: {e})")
    hdr = [f"MEDICI P{PART} — ses önizleme kesitleri ({'ÖNİZLEME miksi: geçici ses / eksik bölüm' if c['onizleme'] else 'final miks'})",
           "mix = nihai miksten (konuşma + müzik + efekt; −14 LUFS); muzik = ducking'siz ham müzik (kulakla müziği değerlendirmek için; RMS −20 dBFS).", ""]
    open(os.path.join(pdir, f"{pref}OKU_BENI.txt"), "w", encoding="utf-8").write("\n".join(hdr + lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
