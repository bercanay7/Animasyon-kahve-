#!/usr/bin/env python3
"""Figür kontak sayfaları (figür-lab aracı).

  python3 figs_sheet.py --grid noble,monk,woman --h 520 --out out/frames/g.png     # tek boy, ızgara (hızlı değerlendirme)
  python3 figs_sheet.py --scales noble,monk --out out/frames/figs_sheet_1.png        # her tür 5 boy (150,300,450,600,800) × 2 arka plan
  python3 figs_sheet.py --all --scales-pages                                          # tüm türler: out/frames/figs_sheet_N.png (sayfa başına 2 tür)
  python3 figs_sheet.py --bench                                                       # figure() maliyeti (ilk/önbellekli) ms
"""
import argparse
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import cv2  # noqa: E402
import numpy as np  # noqa: E402
import skia  # noqa: E402

import sk  # noqa: E402
import stage as ST  # noqa: E402
from sk import C, Frame, mix  # noqa: E402

GROUP1 = ["noble", "merchant", "cardinal", "scribe", "monk", "woman", "emperor_old", "prince", "page", "seated", "kneel", "pair_old_prince",
          "pikeman", "landsknecht", "janissary", "knight", "conquistador", "sailor", "native"]
GROUP2 = ["arquebusier", "halberdier", "horse", "horse_walk", "horse_rider", "cavalry_charge", "cavalry_charge_b", "sipahi", "sipahi_b", "peasant", "fisherman", "bearer",
          "inca_noble", "aztec_warrior", "friar_writing", "scholar_lectern", "child", "woman_seated", "man_seated_bed", "coffin", "crowd_a", "crowd_b", "crowd_c", "crowd_d",
          "crowd_e", "crowd_f"]
SIZES = [150, 300, 450, 600, 800]


def bg_amber(f, x0, y0, w, h):
    f.rect(x0, y0, w, h, shader=f.lin(0, y0, 0, y0 + h, [("#4A2E18", 0.0), ("#2A1A0E", 0.55), ("#150C07", 1.0)]))
    f.circle(x0 + w * 0.55, y0 + h * 0.30, h * 0.75, shader=f.rad(x0 + w * 0.55, y0 + h * 0.30, h * 0.75, [("#FFD58A", 0.0, 90), ("#FFB347", 0.5, 28), ("#FFB347", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    f.rect(x0, y0 + h - 40, w, 40, color="#0E0805", alpha=0.6)


def bg_mist(f, x0, y0, w, h):
    f.rect(x0, y0, w, h, shader=f.lin(0, y0, 0, y0 + h, [("#C9CFCB", 0.0), ("#A9B1AE", 0.6), ("#8A938F", 1.0)]))
    f.rect(x0, y0 + h - 40, w, 40, color="#6E7774", alpha=0.7)


def draw_label(f, s, x, y, size=22, color="#E8D8A0"):
    f.text(s, x, y, face="cap_b", size=size, color=color, shadow=(1, 1, 2, "#000000"))


def _sprite_w(k, s, col="#0C0705", rim="#C58A44"):
    img, ox, oy = ST._fig_sprite(k, int(round(s)), col, rim, 0.0)
    return img.width(), ox


def render_scales(kinds, path, sizes=SIZES, col="#0C0705", rim="#C58A44"):
    """Her tür: bir bant; bantta iki arka plan yan yana (solda amber, sağda sisli), her biri 5 boyda aynı zemin çizgisinde (aralık = sprite genişliği)."""
    gap = 50
    top = 70
    bands = []
    for k in kinds:
        ws = [_sprite_w(k, s, col, rim) for s in sizes]
        bands.append((ws, sum(w for w, _ in ws) + gap * (len(sizes) + 1)))
    bw = max(b[1] for b in bands)
    bh = max(sizes) + top + 70
    Wd = bw * 2
    Hd = bh * len(kinds)
    f = Frame(Wd, Hd)
    f.clear('#000000')
    for r, k in enumerate(kinds):
        y0 = r * bh
        ws = bands[r][0]
        for side, bgf in enumerate((bg_amber, bg_mist)):
            x0 = side * bw
            bgf(f, x0, y0, bw, bh)
            x = x0 + gap
            for s, (wd, ox) in zip(sizes, ws):
                yy = y0 + bh - 40
                ST.figure(f, k, x + ox, yy, s, col=col, rim=rim if side == 0 else "#B8863F")
                x += wd + gap
            draw_label(f, f"{k}", x0 + 14, y0 + 34, 30, "#F0D27A" if side == 0 else "#2A2218")
    img = f.rgb()
    if img.shape[1] > 4200:                       # çok geniş türler (süvari, tabut) için sayfayı küçült
        sc = 4200 / img.shape[1]
        img = cv2.resize(img, (4200, int(img.shape[0] * sc)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return img.shape


def render_grid(kinds, path, h=520, cols=None, col="#0C0705", rim="#C58A44", mist=False, cellw=None):
    n = len(kinds)
    cols = cols or min(n, 5)
    cw = cellw or int(h * 0.80)
    ch = int(h * 1.30)
    rows = (n + cols - 1) // cols
    f = Frame(cols * cw, rows * ch)
    f.clear('#000000')
    for i, k in enumerate(kinds):
        r, c = divmod(i, cols)
        x0, y0 = c * cw, r * ch
        (bg_mist if mist else bg_amber)(f, x0, y0, cw, ch)
        ST.figure(f, k, x0 + cw * 0.5, y0 + ch - 50, h, col=col, rim=rim)
        draw_label(f, k, x0 + 10, y0 + 28, 22, "#F0D27A" if not mist else "#2A2218")
    img = f.rgb()
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return img.shape


def bench(kinds, hs=(300, 520)):
    print(f"{'tür':18s}" + "".join(f"{'ilk@'+str(h):>11s}{'sonra@'+str(h):>11s}" for h in hs))
    f = Frame(1920, 1080)
    worst = 0
    for k in kinds:
        row = f"{k:18s}"
        for h in hs:
            ST._fig_sprite.cache_clear() if False else None
            hh = h + (hash(k) % 7)          # farklı boy = önbellekte yok
            t = time.time()
            ST.figure(f, k, 900, 900, hh)
            a = (time.time() - t) * 1000
            t = time.time()
            for _ in range(5):
                ST.figure(f, k, 900, 900, hh)
            b = (time.time() - t) * 1000 / 5
            worst = max(worst, b)
            row += f"{a:11.1f}{b:11.2f}"
        print(row)
    print("en kötü önbellekli figure() ms:", round(worst, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", default=None)
    ap.add_argument("--scales", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--group", default=None, help="1 veya 2")
    ap.add_argument("--h", type=int, default=520)
    ap.add_argument("--cols", type=int, default=None)
    ap.add_argument("--mist", action="store_true")
    ap.add_argument("--out", default="out/frames/figs_grid.png")
    ap.add_argument("--pages", action="store_true", help="figs_sheet_N.png sayfaları (sayfa başına 2 tür, 5 boy × 2 arka plan)")
    ap.add_argument("--bench", action="store_true")
    ap.add_argument("--cellw", type=int, default=None)
    a = ap.parse_args()
    os.makedirs("out/frames", exist_ok=True)
    allk = [k for k in (GROUP1 + GROUP2) if k in ST.FIGX or k in ST.FIG or k == "pair_old_prince"]
    if a.bench:
        bench(allk)
        return
    if a.grid:
        kinds = a.grid.split(",")
        print(render_grid(kinds, a.out, a.h, a.cols, mist=a.mist, cellw=a.cellw))
        return
    if a.scales:
        print(render_scales(a.scales.split(","), a.out))
        return
    if a.pages or a.all:
        kinds = allk if a.group is None else (GROUP1 if a.group == "1" else GROUP2)
        kinds = [k for k in kinds if k in allk]
        for i in range(0, len(kinds), 2):
            p = f"out/frames/figs_sheet_{i // 2 + 1}.png"
            render_scales(kinds[i:i + 2], p)
            print(p, kinds[i:i + 2])
        return


if __name__ == "__main__":
    main()
