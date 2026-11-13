"""Kare birleştirme: sahne grupları + whip pan geçişleri + flaş + HUD + altyazı."""
import math

import numpy as np
from PIL import Image

import events as E
import scenes as S
import ui
from engine import *  # noqa

GROUP_EDGES = [6.0, 11.0, 32.0, 35.0]
FINAL_T = 41.9  # bu andan sonra kare, 0. kareyle birebir aynı


def group_of(t):
    g = 0
    for e in GROUP_EDGES:
        if t >= e:
            g += 1
    return g


def render_group(g, t):
    if g == 0:
        return S.scene_intro(t)
    if g == 1:
        return S.scene_map(t)
    if g == 2:
        return S.scene_harbor(t)
    if g == 3:
        return S.scene_env2(t)
    return S.scene_beach(t)


def whip(A, B, p):
    pad = 420
    a = np.asarray(A, dtype=np.uint8)
    b = np.asarray(B, dtype=np.uint8)
    strip = np.concatenate([a, b], axis=1)
    strip = np.pad(strip, ((0, 0), (pad, pad), (0, 0)), mode="edge")
    e = ease_io(p)
    off = int(round(e * W))
    bw = int(380 * math.sin(math.pi * clamp(p)) ** 0.9)
    n = 13 if bw > 6 else 1
    acc = np.zeros((H, W, 3), np.uint32)
    for j in range(n):
        d = int(round((j / (n - 1) - 0.5) * bw)) if n > 1 else 0
        x0 = pad + off + d
        acc += strip[:, x0:x0 + W, :]
    return Image.fromarray((acc // n).astype(np.uint8), "RGB")


def world_image(t):
    for b in E.WHIPS:
        if abs(t - b) < E.WHIP_HALF:
            gA, gB = group_of(b - 1e-3), group_of(b + 1e-3)
            p = (t - (b - E.WHIP_HALF)) / (2 * E.WHIP_HALF)
            return whip(render_group(gA, t), render_group(gB, t), p)
    return render_group(group_of(t), t)


def render_frame(i):
    t = i / FPS
    final = t >= FINAL_T
    if final:
        t = 0.0
        img = S.scene_intro(0.0)
    else:
        img = world_image(t)
        S.final_sparkle(img, t)
    img = ui.finalize(img)
    fa = E.flash_alpha(t) if not final else 0.0
    if fa > 0:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), min(1.0, fa))
    ui.draw_hud(img, t)
    if not final:
        ui.draw_captions(img, t)
    return img


def frame_bytes(i):
    return i, render_frame(i).tobytes()
