#!/usr/bin/env python3
"""Dış mekân/şehir dünyası önizlemesi (Lab-E): kontak sayfaları + kısa klipler + ölçümler.

  python3 preview_sehir.py                          # her şey: out/frames/sehir_<ad>.png (6 kare, zamana yayılmış) + out/clips/sehir_<ad>.mp4
  python3 preview_sehir.py meydan_ates kale_sur     # yalnız bu girdiler
  python3 preview_sehir.py --no-clip                # yalnız kontak sayfaları
  python3 preview_sehir.py --no-sheet               # yalnız klipler
  python3 preview_sehir.py --ms                     # ms/kare (post dâhil) ölçümü
  python3 preview_sehir.py --bake                   # kareaş bake süreleri (soğuk önbellek)
  python3 preview_sehir.py meydan_ates --at 6.5     # tek tam çözünürlüklü kare → out/frames/sehir_meydan_ates_t6.5.png
  python3 preview_sehir.py --workers 2 --scale 0.5

Girdiler: meydan_ates, meydan_odun, meydan_palle, meydan_pencere, meydan_kalabalik, sokak_kapi_gunduz, sokak_kapi_gece, sokak_yuruyus, kale_sur, kale_castel, kale_passetto, skyline_dikey.
Kare = preview_cilt.render ile aynı çizim yolu (CM.post dâhil). İşçi ≤2, ölçek 0.5. Arka planda süreç bırakmaz. `out` bağlantısına/parca.kullan()'a dokunmaz.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import cilt_medici as CM  # noqa: E402
import cilt_sehir as SE  # noqa: E402,F401
import shots as SH  # noqa: E402
import sk  # noqa: E402
from sk import FPS, H, W  # noqa: E402

OUT_FR = os.path.join(HERE, "out", "frames")
OUT_CL = os.path.join(HERE, "out", "clips")
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

# (ad, tür, parametreler, süre, mod, perde, klip_sn)
SEHIR = [
    ("meydan_ates", "sehir", dict(scene="meydan", act="ates"), 12.0, "night", 2, 12.0),
    ("meydan_odun", "sehir", dict(scene="meydan", act="odun"), 10.0, "night", 2, 10.0),
    ("meydan_palle", "sehir", dict(scene="meydan", act="palle", kick="PALLE! PALLE!"), 12.0, "day", 2, 12.0),
    ("meydan_pencere", "sehir", dict(scene="meydan", act="pencere"), 12.0, "night", 2, 12.0),
    ("meydan_kalabalik", "sehir", dict(scene="meydan", act="kalabalik", dir="l"), 10.0, "day", 1, 10.0),
    ("sokak_kapi_gunduz", "sehir", dict(scene="sokak", door="close", door_at=6.0), 10.0, "day", 2, 10.0),
    ("sokak_kapi_gece", "sehir", dict(scene="sokak", door="close", door_at=5.0, tod="night"), 10.0, "night", 2, 10.0),
    ("sokak_yuruyus", "sehir", dict(scene="sokak"), 12.0, "day", 2, 12.0),
    ("kale_sur", "sehir", dict(scene="kale", act="sur"), 12.0, "day", 3, 12.0),
    ("kale_castel", "sehir", dict(scene="kale", act="castel"), 10.0, "day", 3, 10.0),
    ("kale_passetto", "sehir", dict(scene="kale", act="passetto"), 14.0, "day", 3, 14.0),
    ("skyline_dikey", "sehir", dict(scene="skyline_dikey", tod="day"), 12.0, "day", 2, 12.0),
]
BY_NAME = {w[0]: w for w in SEHIR}


def frames_iter(kind, params, dur, ts, mode, perde, post=True, clip_dur=None):
    """preview_cilt.render ile aynı çizim yolu; kare başına üretici (bellek dostu). clip_dur verilirse çekim süresi buna ayarlanır."""
    p = dict(params)
    sh = SH.shot(kind, 0.0, **p)
    d = clip_dur or dur
    sh.t0, sh.t1, sh.i = 0.0, d, 1
    tl = SH.timeline()
    for t in ts:
        f = sk.Frame()
        cx = SH.Ctx(f, t, sh, tl)
        cx.perde = perde
        cx.mode = mode
        SH.KINDS[kind](cx, **p)
        img = f.rgb()
        if post:
            m, pe = CM.mode_of(f)
            img = CM.post(img, int(t * FPS), m, pe)
        yield img


def label(img, text):
    strip = np.zeros((46, img.shape[1], 3), np.uint8)
    cv2.putText(strip, text, (12, 33), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (240, 215, 140), 2, cv2.LINE_AA)
    return np.vstack([strip, img])


def make_sheet(name, scale=0.5, cols=2, n=6):
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [(i + 0.5) / n * dur for i in range(n)]
    imgs = []
    t0 = time.time()
    for t, img in zip(ts, frames_iter(kind, params, dur, ts, mode, perde, True)):
        imgs.append(label(img, f"{ad}  t={t:4.1f}s / {dur:.0f}s"))
    h, w = imgs[0].shape[:2]
    sw, sh_ = int(w * scale), int(h * scale)
    rows = (len(imgs) + cols - 1) // cols
    S = np.zeros((rows * sh_, cols * sw, 3), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        S[r * sh_:(r + 1) * sh_, c * sw:(c + 1) * sw] = cv2.resize(im, (sw, sh_), interpolation=cv2.INTER_AREA)
    os.makedirs(OUT_FR, exist_ok=True)
    path = os.path.join(OUT_FR, f"sehir_{ad}.png")
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path, time.time() - t0


def make_single(name, t):
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    img = next(frames_iter(kind, params, dur, [t], mode, perde, True))
    os.makedirs(OUT_FR, exist_ok=True)
    path = os.path.join(OUT_FR, f"sehir_{ad}_t{t:g}.png")
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return path


def make_clip(name, scale=0.5, fps=None):
    """6–14 sn mp4 (24 fps, post dâhil). Çekim süresi = klip süresi (kamera yolu klibe sığar)."""
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    fps = fps or FPS
    nfr = int(round(clip_s * fps))
    ts = [i / fps for i in range(nfr)]
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    os.makedirs(OUT_CL, exist_ok=True)
    path = os.path.join(OUT_CL, f"sehir_{ad}.mp4")
    t0 = time.time()
    use_ff = os.path.exists(FFMPEG)
    if use_ff:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-an",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        wr = proc.stdin
    else:
        vw = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    for img in frames_iter(kind, params, clip_s, ts, mode, perde, True, clip_dur=clip_s):
        small = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
        if use_ff:
            wr.write(small.tobytes())
        else:
            vw.write(cv2.cvtColor(small, cv2.COLOR_RGB2BGR))
    if use_ff:
        wr.close()
        proc.wait()
    else:
        vw.release()
    return path, time.time() - t0, nfr


def motion_energy(path):
    """Klibin hareket enerjisi: ardışık kare farklarının ortalaması + ölü (≈kopya) kare sayısı."""
    cap = cv2.VideoCapture(path)
    prev = None
    diffs = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (240, 135)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            diffs.append(float(np.mean(np.abs(g - prev))))
        prev = g
    cap.release()
    d = np.array(diffs) if diffs else np.zeros(1)
    return float(d.mean()), int((d < 0.02).sum()), len(d) + 1


LAST_BREAKDOWN = {}


def measure(name, n=8):
    """ms/kare (post dâhil): çekimin 0,1–0,9 aralığından n+1 kare (ilk kare ısınma sayılır, ortalamaya girmez). Şablon/zaman çizelgesi bir kez kurulur;
    yalnız kare çizimi + RGB okuma + CM.post ölçülür. Dönüş: (duvar ort, maks, ilk kare, CPU ort, medyan, en az). Paylaşımlı CPU'da ortalama şişer: medyan/en az daha güvenilirdir."""
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [(0.1 + 0.8 * i / n) * dur for i in range(n + 1)]
    it = frames_iter(kind, params, dur, ts, mode, perde, True)
    tm, cp = [], []
    global LAST_BREAKDOWN
    bd = {}
    for _ in ts:
        t1, c1 = time.perf_counter(), time.process_time()
        next(it)
        tm.append((time.perf_counter() - t1) * 1000)
        cp.append((time.process_time() - c1) * 1000)
        for k_, v_ in SE.TIMES.items():
            bd.setdefault(k_, []).append(v_)
    LAST_BREAKDOWN = {k_: float(np.median(v_[1:])) for k_, v_ in bd.items()}
    return float(np.mean(tm[1:])), float(np.max(tm[1:])), tm[0], float(np.mean(cp[1:])), float(np.median(tm[1:])), float(np.min(tm[1:]))


def bake_times():
    """Kareaş bake süreleri (soğuk önbellek): yalnız sehir_* dosyaları silinir."""
    res = []
    seen = set()
    for ad, kind, params, dur, mode, perde, clip_s in SEHIR:
        scene, act = params.get("scene"), params.get("act") or SE.DEFAULT_ACT.get(params.get("scene"))
        tod = params.get("tod") or SE.ACT_TOD.get((scene, act)) or ("night" if mode == "night" else "day")
        w = SE.get_sworld(scene, act, tod)
        if (w.name, tod) in seen:
            continue
        seen.add((w.name, tod))
        for fn in os.listdir(SE.CACHE) if os.path.isdir(SE.CACHE) else []:
            if fn.startswith(f"{w.name}_{tod}_"):
                os.remove(os.path.join(SE.CACHE, fn))
        w2 = SE.CLASSES.get((scene, act)) or SE.CLASSES.get((scene, None))
        t0 = time.perf_counter()
        w3 = w2(tod)
        n = w3.bake_all()
        res.append((w.name, tod, n, time.perf_counter() - t0))
    return res


def _job(args):
    name, scale, do_sheet, do_clip = args
    out = []
    try:
        if do_sheet:
            p, s = make_sheet(name, scale)
            out.append(f"{name:20s} sayfa {s:5.1f} s -> {os.path.relpath(p, HERE)}")
        if do_clip:
            p, s, n = make_clip(name, scale)
            me, dead, tot = motion_energy(p)
            out.append(f"{name:20s} klip  {s:5.1f} s ({n} kare, {os.path.getsize(p) / 1e6:.1f} MB, hareket {me:.2f}, ölü kare {dead}/{tot}) -> {os.path.relpath(p, HERE)}")
    except Exception as e:  # noqa: BLE001
        import traceback
        out.append(f"{name:20s} HATA: {e!r}\n{traceback.format_exc()}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--no-clip", action="store_true")
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--ms", action="store_true")
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--at", type=float, default=None)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--scale", type=float, default=0.5)
    a = ap.parse_args()
    names = a.names or [w[0] for w in SEHIR]
    for n in names:
        if n not in BY_NAME:
            print("bilinmeyen girdi:", n, "—", ", ".join(BY_NAME))
            return
    if a.bake:
        for nm, tod, n, sec in bake_times():
            print(f"bake {nm:16s} {tod:6s} {n:3d} kareaş  {sec:5.1f} s")
        return
    if a.at is not None:
        for n in names:
            print(make_single(n, a.at))
        return
    if a.ms:
        for n in names:
            avg, mx, first, cpu, med, mn = measure(n)
            print(f"{n:20s} duvar ort {avg:6.1f} ms  medyan {med:6.1f}  en az {mn:6.1f}  maks {mx:6.1f} ms  CPU ort {cpu:6.1f} ms  ilk kare {first:6.0f} ms")
            print("    döküm (medyan ms): " + "  ".join(f"{k_}={v_:.0f}" for k_, v_ in sorted(LAST_BREAKDOWN.items(), key=lambda kv: -kv[1]) if v_ >= 2.0))
        return
    jobs = [(n, a.scale, not a.no_sheet, not a.no_clip) for n in names]
    workers = max(1, min(2, a.workers))
    t0 = time.time()
    if workers == 1 or len(jobs) == 1:
        for j in jobs:
            print(_job(j), flush=True)
    else:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(workers) as pool:
            for r in pool.imap_unordered(_job, jobs):
                print(r, flush=True)
    print(f"toplam {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
