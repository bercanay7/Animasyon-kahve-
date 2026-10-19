#!/usr/bin/env python3
"""Deniz / liman / gemi dünyası önizlemesi (Lab-C): kontak sayfaları + kısa klipler + ölçümler.

  python3 preview_deniz.py                         # her şey: out/frames/deniz_<ad>.png (6 kare) + out/clips/deniz_<ad>.mp4
  python3 preview_deniz.py acik_kadirga rota_pisa_napoli   # yalnız bu girdiler
  python3 preview_deniz.py --no-clip | --no-sheet | --ms | --bake | --workers 2 | --scale 0.5
  python3 preview_deniz.py --at acik_kadirga 4.0   # tam çözünürlüklü tek kare → out/frames/deniz_<ad>_t<sn>.png

Kare = preview_world ile aynı çizim yolu (CM.post dâhil). İşçi ≤2, ölçek 0,5. Arka planda süreç bırakmaz.
"""
import argparse
import math
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

import cilt_anim as FA  # noqa: E402,F401
import cilt_medici as CM  # noqa: E402
import cilt_deniz as DN  # noqa: E402,F401
import shots as SH  # noqa: E402
import sk  # noqa: E402
from sk import FPS, H, W  # noqa: E402

OUT_FR = os.path.join(HERE, "out", "frames")
OUT_CL = os.path.join(HERE, "out", "clips")
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

# ═════════════════════════════ girdiler: (ad, tür, parametreler, süre, mod, perde, klip_sn) ═════════════════════════════
WORLD = [
    ("acik_kadirga", "deniz", dict(scene="acik", tod="day", ships=[
        dict(kind="kadirga", x0=300, x1=1500, y=650, scale=1.0, flag="hristiyan", t0=0.0, t1=10.0, ease="lin"),
        dict(kind="nao", x0=1750, x1=1250, y=500, scale=0.8, flag="venedik", t0=0.0, t1=12.0, ease="lin")]), 12.0, "day", 1, 12.0),
]
BY_NAME = {w[0]: w for w in WORLD}


def frames_iter(kind, params, dur, ts, mode, perde, post=True, clip_dur=None):
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
    path = os.path.join(OUT_FR, f"deniz_{ad}.png")
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path, time.time() - t0


def make_still(name, t, scale=1.0):
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    img = next(frames_iter(kind, params, dur, [t], mode, perde, True))
    if scale != 1.0:
        img = cv2.resize(img, (int(W * scale), int(H * scale)), interpolation=cv2.INTER_AREA)
    os.makedirs(OUT_FR, exist_ok=True)
    path = os.path.join(OUT_FR, f"deniz_{ad}_t{t:g}.png")
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return path


def make_clip(name, scale=0.5, fps=None):
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    fps = fps or FPS
    nfr = int(round(clip_s * fps))
    ts = [i / fps for i in range(nfr)]
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    os.makedirs(OUT_CL, exist_ok=True)
    path = os.path.join(OUT_CL, f"deniz_{ad}.mp4")
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


def measure(name, n=8):
    """ms/kare (post dâhil): çekimin farklı anlarından n kare (ısınma 1 kare). Dönüş: (duvar ort, duvar maks, ilk kare, CPU ort)."""
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [(0.1 + 0.8 * i / n) * dur for i in range(n + 1)]
    tm, cp = [], []
    for t in ts:
        t1, c1 = time.perf_counter(), time.process_time()
        list(frames_iter(kind, params, dur, [t], mode, perde, True))
        tm.append((time.perf_counter() - t1) * 1000)
        cp.append((time.process_time() - c1) * 1000)
    return float(np.mean(tm[1:])), float(np.max(tm[1:])), tm[0], float(np.mean(cp[1:]))


def bake_times():
    res = []
    cdir = DN.CACHE
    if os.path.isdir(cdir):
        for fn in os.listdir(cdir):
            if fn.startswith("deniz_"):
                os.remove(os.path.join(cdir, fn))
    DN._IMGS.clear()
    for name in ("liman_marsilya_1533", "liman_pera", "kiyi_otranto"):
        if name in BY_NAME:
            t0 = time.perf_counter()
            list(frames_iter(*BY_NAME[name][1:3], BY_NAME[name][3], [1.0], BY_NAME[name][4], BY_NAME[name][5], False))
            res.append((name, time.perf_counter() - t0))
    return res


def motion_energy(name, n=40):
    """Klip hareket enerjisi: ardışık karelerin ortalama mutlak farkı (240×135 gri) ve 0,5 sn'lik ölü (kopya) pencere sayısı."""
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [i * 0.5 for i in range(int(clip_s / 0.5))]
    prev, vals = None, []
    for img in frames_iter(kind, params, clip_s, ts, mode, perde, False, clip_dur=clip_s):
        g = cv2.cvtColor(cv2.resize(img, (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY).astype(np.float32)
        if prev is not None:
            vals.append(float(np.mean(np.abs(g - prev))))
        prev = g
    return float(np.mean(vals)), float(np.min(vals)), sum(1 for v in vals if v < 0.6)


def _job(args):
    name, scale, do_sheet, do_clip = args
    out = []
    try:
        if do_sheet:
            p, s = make_sheet(name, scale)
            out.append(f"{name:24s} sayfa {s:5.1f} s -> {os.path.relpath(p, HERE)}")
        if do_clip:
            p, s, n = make_clip(name, scale)
            out.append(f"{name:24s} klip  {s:5.1f} s ({n} kare) -> {os.path.relpath(p, HERE)}")
    except Exception as e:  # noqa: BLE001
        import traceback
        out.append(f"{name:24s} HATA: {e!r}\n{traceback.format_exc()}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--no-clip", action="store_true")
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--ms", action="store_true")
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--energy", action="store_true")
    ap.add_argument("--at", nargs=2, metavar=("AD", "SN"))
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--scale", type=float, default=0.5)
    a = ap.parse_args()
    if a.at:
        print(make_still(a.at[0], float(a.at[1]), a.scale if a.scale != 0.5 else 1.0))
        return
    names = a.names or [w[0] for w in WORLD]
    for n in names:
        if n not in BY_NAME:
            print("bilinmeyen girdi:", n, "—", ", ".join(BY_NAME))
            return
    if a.bake:
        for n, sec in bake_times():
            print(f"bake {n:24s} {sec:5.1f} s")
        return
    if a.ms:
        for n in names:
            avg, mx, first, cpu = measure(n)
            print(f"{n:24s} duvar ort {avg:6.1f} ms  maks {mx:6.1f} ms  CPU ort {cpu:6.1f} ms  ilk kare {first:6.0f} ms", flush=True)
        return
    if a.energy:
        for n in names:
            m, mn, dead = motion_energy(n)
            print(f"{n:24s} hareket enerjisi ort {m:5.2f}  min {mn:5.2f}  ölü pencere {dead}", flush=True)
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
