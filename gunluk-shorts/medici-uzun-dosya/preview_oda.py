#!/usr/bin/env python3
"""İç mekân dünyası önizlemesi (Lab-D): kontak sayfaları + kısa klipler + ölçümler.

  python3 preview_oda.py                          # her şey: out/frames/oda_<ad>.png (6 kare) + out/clips/oda_<ad>.mp4
  python3 preview_oda.py oda1743_gece_in salon_napoli   # yalnız bu girdiler
  python3 preview_oda.py --list                   # girdi adları
  python3 preview_oda.py --no-clip | --no-sheet   # yalnız sayfa / yalnız klip
  python3 preview_oda.py --ms                     # ms/kare (post dâhil) ölçümü
  python3 preview_oda.py --frame oda1743_gece_in 6.0 [--full]   # tek kare out/frames/oda_<ad>_t<sn>.png (varsayılan yarı çözünürlük)
  python3 preview_oda.py --bake                   # tüm odaların kareaş pişirme süreleri (soğuk önbellek: oda önbelleğini siler)
  python3 preview_oda.py --workers 2 --scale 0.5

Kare = preview_cilt.render ile aynı çizim yolu (CM.post dâhil). İşçi ≤2, ölçek 0,5. Arka planda süreç bırakmaz.
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
import cilt_oda as OD  # noqa: E402
import shots as SH  # noqa: E402
import sk  # noqa: E402
from sk import FPS, H, W  # noqa: E402

OUT_FR = os.path.join(HERE, "out", "frames")
OUT_CL = os.path.join(HERE, "out", "clips")
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

# (ad, parametreler, süre, mod, perde, klip_sn)  — hepsi shot("oda", …)
ODA = [
    ("oda1743_gece_in", dict(room="oda1743", path="in"), 12.0, "night", 1, 12.0),
    ("oda1743_gece_out", dict(room="oda1743", path="out", figure="lying"), 12.0, "night", 3, 12.0),
    ("oda1743_gun", dict(room="oda1743", path="sweep_r", figure="seated"), 10.0, "day", 1, 10.0),
    ("oda1743_yatak", dict(room="oda1743", path="bed", figure="lying"), 8.0, "night", 1, 8.0),
]
BY_NAME = {w[0]: w for w in ODA}


def make_shot(params, dur):
    p = dict(params)
    sh = SH.shot("oda", 0.0, **p)
    sh.t0, sh.t1, sh.i = 0.0, dur, 1
    return sh, p


def frames_iter(name, ts, post=True, dur=None):
    ad, params, d0, mode, perde, clip_s = BY_NAME[name]
    d = dur or d0
    sh, p = make_shot(params, d)
    tl = SH.timeline()
    for t in ts:
        f = sk.Frame()
        cx = SH.Ctx(f, t, sh, tl)
        cx.perde = perde
        cx.mode = mode
        SH.KINDS["oda"](cx, **p)
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
    ad, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [(i + 0.5) / n * dur for i in range(n)]
    imgs = []
    t0 = time.time()
    for t, img in zip(ts, frames_iter(name, ts)):
        imgs.append(label(img, f"{ad}  t={t:4.1f}s / {dur:.0f}s"))
    h, w = imgs[0].shape[:2]
    sw, sh_ = int(w * scale), int(h * scale)
    rows = (len(imgs) + cols - 1) // cols
    S = np.zeros((rows * sh_, cols * sw, 3), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        S[r * sh_:(r + 1) * sh_, c * sw:(c + 1) * sw] = cv2.resize(im, (sw, sh_), interpolation=cv2.INTER_AREA)
    os.makedirs(OUT_FR, exist_ok=True)
    path = os.path.join(OUT_FR, f"oda_{ad}.png")
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path, time.time() - t0


def make_frame(name, t, full=False):
    img = next(frames_iter(name, [t]))
    if not full:
        img = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    os.makedirs(OUT_FR, exist_ok=True)
    path = os.path.join(OUT_FR, f"oda_{name}_t{t:g}.png")
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return path


def make_clip(name, scale=0.5, fps=None):
    ad, params, dur, mode, perde, clip_s = BY_NAME[name]
    fps = fps or FPS
    nfr = int(round(clip_s * fps))
    ts = [i / fps for i in range(nfr)]
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    os.makedirs(OUT_CL, exist_ok=True)
    path = os.path.join(OUT_CL, f"oda_{ad}.mp4")
    t0 = time.time()
    use_ff = os.path.exists(FFMPEG)
    if use_ff:
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-an",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        wr = proc.stdin
    else:
        vw = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    for img in frames_iter(name, ts, True, dur=clip_s):
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
    """ms/kare (çekim + RGB + CM.post): çekimin içinden n kare (ısınma 1 kare). Dönüş: (duvar ort, duvar maks, ilk kare, CPU ort)."""
    ad, params, dur, mode, perde, clip_s = BY_NAME[name]
    ts = [(0.05 + 0.9 * i / n) * dur for i in range(n + 1)]
    tm, cp = [], []
    for t in ts:
        t1, c1 = time.perf_counter(), time.process_time()
        list(frames_iter(name, [t]))
        tm.append((time.perf_counter() - t1) * 1000)
        cp.append((time.process_time() - c1) * 1000)
    return float(np.mean(tm[1:])), float(np.max(tm[1:])), tm[0], float(np.mean(cp[1:]))


def bake_times():
    import cilt_pano as PN
    res = []
    seen = set()
    for ad, params, *_ in ODA:
        key = (params.get("room"), params.get("variant"), params.get("tod") or ("night" if _[1] == "night" else "day"))
        if key in seen:
            continue
        seen.add(key)
        w = OD.get_room(key[0], key[1], key[2])
        pref = f"oda_{w.key}_{w.tod}_"
        if os.path.isdir(PN.CACHE):
            for fn in os.listdir(PN.CACHE):
                if fn.startswith(pref):
                    os.remove(os.path.join(PN.CACHE, fn))
        w2 = OD.ROOMS[key[0]](key[1], key[2])
        t0 = time.perf_counter()
        n = w2.bake_all()
        res.append((key, n, time.perf_counter() - t0))
    return res


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
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-clip", action="store_true")
    ap.add_argument("--no-sheet", action="store_true")
    ap.add_argument("--ms", action="store_true")
    ap.add_argument("--bake", action="store_true")
    ap.add_argument("--frame", nargs=2, metavar=("AD", "SN"))
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--scale", type=float, default=0.5)
    a = ap.parse_args()
    if a.list:
        for w in ODA:
            print(w[0])
        return
    if a.frame:
        print(make_frame(a.frame[0], float(a.frame[1]), a.full))
        return
    names = a.names or [w[0] for w in ODA]
    for n in names:
        if n not in BY_NAME:
            print("bilinmeyen girdi:", n, "—", ", ".join(BY_NAME))
            return
    if a.bake:
        for key, n, sec in bake_times():
            print(f"bake {str(key):44s} {n:3d} kareaş  {sec:5.1f} s")
        return
    if a.ms:
        for n in names:
            avg, mx, first, cpu = measure(n)
            print(f"{n:24s} duvar ort {avg:6.1f} ms  maks {mx:6.1f} ms  CPU ort {cpu:6.1f} ms  ilk kare {first:6.0f} ms")
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
