"""Altyazı bölgesi taraması: her altyazı sayfasının tam göründüğü anda DÜNYA karesinde (altyazı/HUD'suz) bölgenin
kenar yoğunluğunu ölçer. Kart/etiket/damga gibi metin taşıyan nesne bölgeye girerse yoğunluk yükselir.
Beklenen: yalnız kum tepesi / zemin gibi arka plan dokusu (kenar ≲ 2,7) kalır.
Kullanım: python3 capzone.py   → konsola en yoğun 30 sayfa, out/capzone_top.png (ilk 24 sayfanın altyazı şeridi)"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

import numpy as np
from multiprocessing import Pool
from PIL import Image

import compose
import cues
import ui
from engine import FPS, W


def job(args):
    k, t = args
    lines, widths, space, px = ui._PL[k]
    nl = len(lines)
    lh = px * 1.28
    y0 = ui.CAP_Y - (nl - 1) * lh / 2
    top, bot = int(y0 - px * 0.7), int(y0 + (nl - 1) * lh + px * 0.7)
    world = compose.world_image(t)
    a = np.asarray(world.convert("L"), np.float32)[top:bot, 60:W - 60]
    gx = np.abs(np.diff(a, axis=1)).mean()
    gy = np.abs(np.diff(a, axis=0)).mean()
    crop = compose.render_frame(int(round(t * FPS))).crop((0, 1150, W, 1470)).resize((540, 160), Image.LANCZOS)
    return k, t, float(a.std()), float(gx + gy), top, bot, crop


if __name__ == "__main__":
    jobs = []
    for k, p in enumerate(ui.PAGES):
        t0 = p[0]["t0"] - 0.03
        t1 = (ui.PAGES[k + 1][0]["t0"] - 0.03) if k + 1 < len(ui.PAGES) else cues.CAP_END
        t = min(t1 - 0.05, p[-1]["t0"] + 0.35)
        if 0.3 < t < cues.FINAL_T - 0.2:
            jobs.append((k, t))
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=2)
    res.sort(key=lambda r: -r[3])
    print("sayfa sayısı:", len(res))
    for r in res[:30]:
        print(f"sayfa {r[0]:3d} t={r[1]:7.2f} std={r[2]:5.1f} kenar={r[3]:5.2f} y[{r[4]},{r[5]}]  '{' '.join(w['show'] for w in ui.PAGES[r[0]])}'")
    sheet = Image.new("RGB", (1080, 160 * 12))
    for i, r in enumerate(res[:24]):
        sheet.paste(r[6], ((i % 2) * 540, (i // 2) * 160))
    sheet.save(os.path.join(HERE, "out", "capzone_top.png"))
