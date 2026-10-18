#!/usr/bin/env python3
"""Dünya ve figür animasyonu önizlemesi (GÖREV B): kontak sayfaları + kısa klipler + ölçümler.

  python3 preview_world.py                       # her şey: out/frames/world_<ad>.png (6 kare, zamana yayılmış) + out/clips/world_<ad>.mp4
  python3 preview_world.py pano_florence build_dome   # yalnız bu girdiler
  python3 preview_world.py --no-clip             # yalnız kontak sayfaları
  python3 preview_world.py --no-sheet            # yalnız klipler
  python3 preview_world.py --ms                  # ms/kare (post dâhil) ölçümü
  python3 preview_world.py --bake                # pano bake süreleri (soğuk önbellek)
  python3 preview_world.py --workers 2 --scale 0.5

Girdiler: kit_walk, kit_acts, kit_riders, kit_crowd (figür kiti), procession, procession_l, pano_florence, pano_florence_night, pano_nave, pano_corridor, build_dome,
build_uffizi, build_dome_night. Kare = preview_cilt.render ile aynı yol (CM.post dâhil). İşçi ≤2, ölçek 0.5. Arka planda süreç bırakmaz.
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
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import cilt_anim as FA  # noqa: E402
import cilt_medici as CM  # noqa: E402
import shots as SH  # noqa: E402
import sk  # noqa: E402
from cilt_medici import TH, ckind  # noqa: E402
from sk import FPS, H, W  # noqa: E402

OUT_FR = os.path.join(HERE, "out", "frames")
OUT_CL = os.path.join(HERE, "out", "clips")
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"


# ═════════════════════════════ figür kiti galerileri (yalnız önizleme çekimleri) ═════════════════════════════
def _stage(f, cx, seed=4):
    """Fresk bandı sahnesi: duvar + asma bantları + krem zemin; zemin çizgisi y=…"""
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 150, W, 950))
    sh = skia.GradientShader.MakeLinear([(0, 150), (0, 950)], [sk.C("#F1E6C4"), sk.C("#E5D6AC"), sk.C("#C9B58A")], [0.0, 0.62, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(0, 150, W, 950), skia.Paint(Shader=sh))
    c.restore()
    for yy in (110, 950):
        FA.vine_band(f, yy, 1.0)
    for yy in (150, 950):
        c.drawLine(-40, yy, W + 40, yy, f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9))


def _label(f, text, x, y, size=26):
    CM.ink(f, text, x, y, face="cap_i", size=size, color=TH.fg, align="c", emboss=False)


KINDS12 = ["tuccar", "banker", "rahip", "kardinal", "soylu", "soylu_f", "asker", "halk", "cocuk", "papa", "kesis", "denizci"]


@ckind("world_kit_walk")
def k_kit_walk(cx, **_):
    """12 kostüm tipi yürür (iki sıra; her biri kendi hızında, ayak kaymaz)."""
    f = cx.f
    _stage(f, cx)
    for i, k in enumerate(KINDS12):
        row, col = divmod(i, 6)
        y = 560 + row * 350
        v = 78.0 + 11.0 * (i % 5)
        x = ((col * 330 + 120 + v * cx.t + row * 90) % (W + 420)) - 210
        FA.walker(f, k, x, y, 300 if k != "cocuk" else 250, cx.t, speed=v, seed=2 + i, phase=(i * 0.17) % 1.0)
        _label(f, k, 180 + col * 330, y + 44)


ACT_GRID = [
    ("tuccar", "idle", {}, 0), ("banker", "talk", {}, 0), ("rahip", "bow", {"t0": 0.6}, 6.0), ("soylu", "kneel", {"t0": 0.5, "rise_at": 3.4}, 6.0),
    ("halk", "point", {"t0": 0.6, "dur": 2.4}, 6.0), ("halk", "cheer", {}, 0), ("kardinal", "pray", {}, 0),
    ("banker", "write", {}, 0), ("banker", "count", {}, 0), ("halk", "work", {"mode": "lay"}, 0), ("halk", "work", {"mode": "strike"}, 0),
    ("denizci", "work", {"mode": "haul"}, 0), ("soylu_f", "talk", {"energy": 0.8}, 0), ("asker", "idle", {}, 0)]


@ckind("world_kit_acts")
def k_kit_acts(cx, **_):
    """Eylemler: bekleme, konuşma, selam, diz çökme, işaret, coşku, dua, yazı, para sayma, mala/çekiç/halat işi; el sıkışma + şiddet SİLUETİ ayrı hücrelerde."""
    f = cx.f
    _stage(f, cx)
    for i, (kind, act, kw, per) in enumerate(ACT_GRID):
        row, col = divmod(i, 7)
        x = 150 + col * 270
        y = 520 + row * 380
        tt = (cx.t % per) if per else cx.t
        FA.actor(f, kind, x, y, 270, tt, action=act, seed=3 + i, phase=(i * 0.21) % 1.0, **kw)
        _label(f, act + ("/" + kw["mode"] if "mode" in kw else ""), x, y + 44, 22)
    FA.handshake(f, "tuccar", "banker", W - 360, 900 - 30, 250, cx.t % 7.0, seedA=21, seedB=22)
    _label(f, "handshake", W - 360, 944, 22)


@ckind("world_kit_riders")
def k_kit_riders(cx, **_):
    """Atlılar: yürüyüş / tırıs / dörtnala (toynak kaymaz; gövde sallanır), iki yön."""
    f = cx.f
    _stage(f, cx)
    for i, (g, v, y) in enumerate((("walk", 70.0, 400), ("trot", 150.0, 660), ("gallop", 330.0, 920))):
        d = 1 if i % 2 == 0 else -1
        x = ((i * 500 + 300 + d * v * cx.t) % (W + 700)) - 350
        FA.rider(f, x, y, 270, cx.t, speed=v, gait=g, dir=d, seed=5 + i)
        _label(f, g, 160, y - 120, 30)


@ckind("world_kit_crowd")
def k_kit_crowd(cx, **_):
    """Kalabalık (60 kişi, faz kaydırmalı): dolaşan → coşku dalgası → yürüyüş kolu."""
    f = cx.f
    _stage(f, cx)
    t = cx.t
    if t < 4.0:
        FA.crowd(f, t, (120, 540, 1800, 900), 58, seed=3, wave=0.0, mode="mill", h=(150, 250))
        _label(f, "mill", 160, 215, 30)
    elif t < 8.0:
        FA.crowd(f, t, (120, 540, 1800, 900), 58, seed=3, wave=1.0, mode="cheer", h=(150, 250), wave_speed=1.2)
        _label(f, "cheer + dalga", 200, 215, 30)
    else:
        FA.crowd(f, t, (120, 540, 1800, 900), 58, seed=3, wave=0.3, mode="march", dir="r", h=(150, 250), speed=90.0)
        _label(f, "march", 160, 215, 30)


# ═════════════════════════════ girdiler ═════════════════════════════
# (ad, tür, parametreler, süre, mod, perde, klip_sn)
WORLD = [
    ("kit_walk", "world_kit_walk", {}, 10.0, "day", 2, 8.0),
    ("kit_acts", "world_kit_acts", {}, 10.0, "day", 2, 10.0),
    ("kit_riders", "world_kit_riders", {}, 10.0, "day", 2, 8.0),
    ("kit_crowd", "world_kit_crowd", {}, 12.0, "day", 2, 12.0),
    ("procession", "procession", dict(dir="r", density=1.0), 12.0, "day", 2, 12.0),
    ("procession_l", "procession", dict(dir="l", density=1.5, seed=4), 10.0, "day", 2, 10.0),
    ("pano_florence", "pano", dict(pano="florence", tod="day"), 14.0, "day", 2, 12.0),
    ("pano_florence_night", "pano", dict(pano="florence", tod="night"), 14.0, "night", 2, 12.0),
    ("pano_nave", "pano", dict(pano="nave"), 14.0, "day", 2, 12.0),
    ("pano_corridor", "pano", dict(pano="corridor"), 12.0, "day", 2, 12.0),
    ("build_dome", "build", dict(build="dome", p=(0.0, 11.0)), 12.0, "day", 2, 12.0),
    ("build_uffizi", "build", dict(build="uffizi", p=(0.0, 11.0)), 12.0, "day", 2, 12.0),
    ("build_dome_night", "build", dict(build="dome", p=(0.0, 7.0), tod="night"), 8.0, "night", 2, 8.0),
]
BY_NAME = {w[0]: w for w in WORLD}


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
    path = os.path.join(OUT_FR, f"world_{ad}.png")
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path, time.time() - t0


def make_clip(name, scale=0.5, fps=None):
    """6–12 sn mp4 (24 fps, post dâhil). Çekim süresi = klip süresi (kamera yolu klibe sığar)."""
    ad, kind, params, dur, mode, perde, clip_s = BY_NAME[name]
    fps = fps or FPS
    nfr = int(round(clip_s * fps))
    ts = [i / fps for i in range(nfr)]
    w, h = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    os.makedirs(OUT_CL, exist_ok=True)
    path = os.path.join(OUT_CL, f"world_{ad}.mp4")
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
    """ms/kare (post dâhil): çekimin ortasından n kare (ısınma 1 kare). Dönüş: (duvar ort, duvar maks, ilk kare, CPU ort).
    CPU süresi (process_time) paylaşımlı makinede duvar süresinden daha güvenilirdir."""
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
    import cilt_pano as PN
    res = []
    for pano, tod in (("florence", "day"), ("florence", "night"), ("nave", "day"), ("corridor", "day")):
        cdir = PN.CACHE
        if os.path.isdir(cdir):
            for fn in os.listdir(cdir):
                if fn.startswith(f"{pano}_{tod}_"):
                    os.remove(os.path.join(cdir, fn))
        n, sec = PN.bake_world(pano, tod)
        res.append((pano, tod, n, sec))
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
            out.append(f"{name:20s} klip  {s:5.1f} s ({n} kare) -> {os.path.relpath(p, HERE)}")
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
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--scale", type=float, default=0.5)
    a = ap.parse_args()
    names = a.names or [w[0] for w in WORLD]
    for n in names:
        if n not in BY_NAME:
            print("bilinmeyen girdi:", n, "—", ", ".join(BY_NAME))
            return
    if a.bake:
        for pano, tod, n, sec in bake_times():
            print(f"bake {pano:9s} {tod:6s} {n:3d} kareaş  {sec:5.1f} s")
        return
    if a.ms:
        for n in names:
            avg, mx, first, cpu = measure(n)
            print(f"{n:20s} duvar ort {avg:6.1f} ms  maks {mx:6.1f} ms  CPU ort {cpu:6.1f} ms  ilk kare {first:6.0f} ms")
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
