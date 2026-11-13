"""Kare birleştirme: sahneler + geçişler (whip / dikey / zoom) + flaş + HUD + altyazı. Kapanışta kanca kartına döner (ilk kare = son kare)."""
import math
import os

import numpy as np
from PIL import Image

import cues
import scenes as S
import ui
from engine import *  # noqa
from fx import whip, zoom_cut


DRIFT_ON = os.environ.get("DRIFT", "1") != "0"


def punch(t):
    k = 0.0
    for t0, a in cues.PUNCHES:
        u = t - t0
        if 0.0 <= u < 1.5:
            k += a * min(1.0, u / 0.06) * math.exp(-u / 0.28)
    return k


def drift(img, g, t):
    """Kamera: her sahnede yavaş nefes alan itme + eliptik kayma (HUD ve altyazı sonradan çizildiği için sabit kalır).
    Sarsıntı da burada uygulanır. Kapanışta 0'a iner (ilk kare = son kare)."""
    sx, sy = cues.shake(t)
    if not DRIFT_ON and not (sx or sy):
        return img
    u = max(0.0, t - cues.gstart(g))
    fade = 1.0 - smooth(prog(t, cues.CARD_T, cues.FINAL_T))
    r = smooth(u / 0.9) * fade if DRIFT_ON else 0.0
    d = r * (0.038 + 0.012 * math.sin(2 * math.pi * u / 8.5 - 1.1))
    m = W / 2 * (1 - 1 / (1.0 + d)) * 0.92
    z = 1.0 + d + punch(t) * fade
    w = 2 * math.pi / 10.5
    px = m * math.sin(w * u + 0.6 + 1.3 * g) + sx
    py = m * 1.5 * math.cos(w * u + 0.6 + 1.3 * g) + sy
    if abs(z - 1) < 1e-6 and abs(px) < 1e-3 and abs(py) < 1e-3:
        return img
    sw, sh = W / z, H / z
    x0, y0 = W / 2 + px - sw / 2, H / 2 + py - sh / 2
    return img.transform((W, H), Image.AFFINE, (sw / W, 0, x0, 0, sh / H, y0), resample=Image.BICUBIC)


def group_image(g, t):
    return drift(S.render_group(g, t), g, t)


def world_image(t):
    for tb, kind in cues.TRANS:
        if abs(t - tb) < cues.TW:
            gA, gB = cues.group_of(tb - 1e-3), cues.group_of(tb + 1e-3)
            p = (t - (tb - cues.TW)) / (2 * cues.TW)
            A, B = group_image(gA, t), group_image(gB, t)
            if kind == "whip":
                return whip(A, B, p, 0)
            if kind == "up":
                return whip(A, B, p, 1)
            return zoom_cut(A, B, p)
    return group_image(cues.group_of(t), t)


def render_frame(i):
    t = i / FPS
    final = t >= cues.FINAL_T
    if final or i == 0:
        t = 0.0
        img = S.scene_card(0.0, still=True)
    else:
        img = world_image(t)
        k = smooth(prog(t, cues.CARD_T, cues.FINAL_T))       # kapanış: karta yumuşak dönüş
        if k > 0:
            img = Image.blend(img, S.scene_card(0.0, still=True), k)
    fa = cues.flash_alpha(t) if not final else 0.0
    if fa > 0:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 240, 214)), min(1.0, fa))
    img = ui.bottom_shade(img)
    ui.draw_hud(img, t)
    if not final:
        ui.draw_captions(img, t)
    return img


def frame_bytes(i):
    return i, render_frame(i).tobytes()
