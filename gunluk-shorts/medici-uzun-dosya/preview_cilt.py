#!/usr/bin/env python3
"""Medici cildi önizleme: ≥12 "kahraman" çekimi kontak sayfalarına çizer.

  python3 preview_cilt.py                 # her iki sayfa → out/frames/cilt_sheet_1.png (gün), cilt_sheet_2.png (gece + HUD + bölüm kartı + geçişler)
  python3 preview_cilt.py 1               # yalnız sayfa 1
  python3 preview_cilt.py --only title,ledger -k 2   # yalnız bu kahramanlar (ad), çekim başına 2 kare, tek sayfa → out/frames/cilt_only.png
  python3 preview_cilt.py --full ledger   # bir kahramanı tam çözünürlükte (orta kare) → out/frames/cilt_full_ledger.png
  python3 preview_cilt.py --ms            # kahraman başına ms/kare ölçümü

Not: out/timeline.json yalnız yer tutucudur; çekimler açık saniye kullanır (çapa yok).
"""
import argparse
import os
import sys
import time

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import cilt_medici as CM  # noqa: E402
import shots as SH  # noqa: E402
import sk  # noqa: E402
from sk import FPS, H, W  # noqa: E402

DUR = 8.0


def render(kind, params, ts, dur=DUR, post=True, perde=None, mode=None):
    """Tek çekimi verilen yerel saniyelerde çiz. Döner: [uint8 RGB]."""
    p = dict(params)
    sh = SH.shot(kind, 0.0, **p)
    sh.t0, sh.t1, sh.i = 0.0, dur, 1
    tl = SH.timeline()
    out = []
    for t in ts:
        f = sk.Frame()
        cx = SH.Ctx(f, t, sh, tl)
        if perde is not None:
            cx.perde = perde
        if mode is not None:
            cx.mode = mode
        SH.KINDS[kind](cx, **p)
        img = f.rgb()
        if post:
            m, pe = CM.mode_of(f)
            img = CM.post(img, int(t * FPS), m, pe)
        out.append(img)
    return out


def label(img, text):
    im = img.copy()
    cv2.rectangle(im, (0, 0), (im.shape[1], 46), (0, 0, 0), -1)
    cv2.putText(im, text, (12, 33), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (240, 215, 140), 2, cv2.LINE_AA)
    return im


def sheet(imgs, cols=2, scale=0.5, path="out/frames/sheet.png"):
    h, w = imgs[0].shape[:2]
    sw, sh_ = int(w * scale), int(h * scale)
    rows = (len(imgs) + cols - 1) // cols
    S = np.zeros((rows * sh_, cols * sw, 3), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        S[r * sh_:(r + 1) * sh_, c * sw:(c + 1) * sw] = cv2.resize(im, (sw, sh_), interpolation=cv2.INTER_AREA)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, cv2.cvtColor(S, cv2.COLOR_RGB2BGR))
    return path


# ───────────────────────────── kahramanlar ─────────────────────────────
# (ad, tür, parametreler, kare zamanları, süre, mode, perde)
def heroes():
    import cilt_hero
    return cilt_hero.HEROES


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=None, help="1 | 2 (yoksa ikisi)")
    ap.add_argument("--only", default=None)
    ap.add_argument("-k", type=int, default=1)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--full", default=None)
    ap.add_argument("--ms", action="store_true")
    a = ap.parse_args()
    import cilt_hero
    H_ = cilt_hero.HEROES
    if a.full:
        for h in H_:
            if h["ad"] == a.full:
                for i, img in enumerate(cilt_hero.render_hero(h, render, k=1)):
                    p = f"out/frames/cilt_full_{a.full}.png"
                    cv2.imwrite(p, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                    print(p)
        return
    if a.ms:
        for h in H_:
            if a.only and h["ad"] not in a.only.split(","):
                continue
            cilt_hero.measure(h, render)
        return
    pages = {"1": [h for h in H_ if h["sayfa"] == 1], "2": [h for h in H_ if h["sayfa"] == 2]}
    if a.only:
        names = a.only.split(",")
        sel = [h for h in H_ if h["ad"] in names]
        imgs = []
        for h in sel:
            imgs += [label(im, f'{h["ad"]}') for im in cilt_hero.render_hero(h, render, k=a.k)]
        print(sheet(imgs, a.cols, a.scale, "out/frames/cilt_only.png"))
        return
    for pg in ([a.page] if a.page else ["1", "2"]):
        imgs = []
        for h in pages[pg]:
            t0 = time.time()
            ims = cilt_hero.render_hero(h, render, k=1)
            imgs += [label(im, f'{h["ad"]}') for im in ims]
            print(f"  {h['ad']:14s} {time.time() - t0:5.1f} s", flush=True)
        print(sheet(imgs, a.cols, a.scale, f"out/frames/cilt_sheet_{pg}.png"))


if __name__ == "__main__":
    main()
