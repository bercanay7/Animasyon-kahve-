"""Kare birleştirme: sahneler + geçişler (whip / dikey / zoom / vuruş) + flaş + mermi sayacı + altyazı."""
import math

import numpy as np
from PIL import Image, ImageFilter

import cues
import scenes as S
import ui
from engine import *  # noqa


def whip(A, B, p, axis=0):
    pad = 420
    a = np.asarray(A, dtype=np.uint8)
    b = np.asarray(B, dtype=np.uint8)
    strip = np.concatenate([a, b], axis=1 - axis if axis == 0 else 0)
    if axis == 0:
        strip = np.pad(strip, ((0, 0), (pad, pad), (0, 0)), mode="edge")
    else:
        strip = np.pad(strip, ((pad, pad), (0, 0), (0, 0)), mode="edge")
    e = ease_io(p)
    size = W if axis == 0 else H
    off = int(round(e * size))
    bw = int(380 * math.sin(math.pi * clamp(p)) ** 0.9)
    n = 13 if bw > 6 else 1
    acc = np.zeros((H, W, 3), np.uint32)
    for j in range(n):
        d = int(round((j / (n - 1) - 0.5) * bw)) if n > 1 else 0
        x0 = pad + off + d
        acc += strip[:, x0:x0 + W, :] if axis == 0 else strip[x0:x0 + H, :, :]
    return Image.fromarray((acc // n).astype(np.uint8), "RGB")


def zoom_cut(A, B, p, white=0.55):
    if p < 0.5:
        k = ease_in(p / 0.5, 2)
        img, sc = A, 1.0 + 0.55 * k
    else:
        k = 1 - ease_out((p - 0.5) / 0.5, 2)
        img, sc = B, 1.0 + 0.35 * k
    w, h = int(W / sc), int(H / sc)
    x0, y0 = (W - w) // 2, (H - h) // 2
    out = img.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)
    r = 10 * (1 - abs(p - 0.5) * 2) ** 0.5 * 0 + 6 * (abs(p - 0.5) * 2) if False else 0
    fl = white * max(0.0, 1 - abs(p - 0.5) * 2.5)
    if fl > 0:
        out = Image.blend(out, Image.new("RGB", (W, H), (255, 255, 255)), fl)
    return out


def world_image(t):
    for tb, kind in cues.TRANS:
        if abs(t - tb) < cues.TW:
            gA, gB = cues.group_of(tb - 1e-3), cues.group_of(tb + 1e-3)
            p = (t - (tb - cues.TW)) / (2 * cues.TW)
            A, B = S.render_group(gA, t), S.render_group(gB, t)
            if kind == "whip":
                return whip(A, B, p, 0)
            if kind == "up":
                return whip(A, B, p, 1)
            return zoom_cut(A, B, p)
    return S.render_group(cues.group_of(t), t)


def render_frame(i):
    t = i / FPS
    final = t >= cues.FINAL_T
    if final or i == 0:
        t = 0.0
        img = S.scene_A(0.0, still=True)
    else:
        img = world_image(t)
    fa = cues.flash_alpha(t) if not final else 0.0
    if fa > 0:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), min(1.0, fa))
    ui.draw_hud(img, t)
    if not final:
        ui.draw_captions(img, t)
    return img


def frame_bytes(i):
    return i, render_frame(i).tobytes()
