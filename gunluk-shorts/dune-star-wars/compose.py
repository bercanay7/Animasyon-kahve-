"""Kare birleştirme: sahneler + geçişler (whip / dikey / zoom) + flaş + KANIT etiketi + altyazı."""
import math
import os

import numpy as np
from PIL import Image

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
    bw = int(300 * math.sin(math.pi * clamp(p)) ** 0.9)
    n = 11 if bw > 6 else 1
    acc = np.zeros((H, W, 3), np.uint32)
    for j in range(n):
        d = int(round((j / (n - 1) - 0.5) * bw)) if n > 1 else 0
        x0 = pad + off + d
        acc += strip[:, x0:x0 + W, :] if axis == 0 else strip[x0:x0 + H, :, :]
    return Image.fromarray((acc // n).astype(np.uint8), "RGB")


def zoom_cut(A, B, p, white=0.45):
    if p < 0.5:
        k = ease_in(p / 0.5, 2)
        img, sc = A, 1.0 + 0.45 * k
    else:
        k = 1 - ease_out((p - 0.5) / 0.5, 2)
        img, sc = B, 1.0 + 0.30 * k
    w, h = int(W / sc), int(H / sc)
    x0, y0 = (W - w) // 2, (H - h) // 2
    out = img.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)
    fl = white * max(0.0, 1 - abs(p - 0.5) * 2.5)
    if fl > 0:
        out = Image.blend(out, Image.new("RGB", (W, H), (255, 240, 214)), fl)
    return out


GSTART = [0.0] + [tb for tb, _ in cues.TRANS]
DRIFT_ON = os.environ.get("DRIFT", "1") != "0"


def punch(t):
    """Vurgu anlarında hızlı zoom itişi: 0,06 sn'de girer, ~0,3 sn'de söner."""
    k = 0.0
    for t0, a in cues.PUNCHES:
        u = t - t0
        if 0.0 <= u < 1.5:
            k += a * min(1.0, u / 0.06) * math.exp(-u / 0.28)
    return k


def drift(img, g, t):
    """Kâğıt diorama kamerası: her sahnede yavaş nefes alan itme/çekme + hafif kayma (sahne yerel zamanı).
    Dünya görüntüsüne uygulanır; HUD ve altyazı sonradan çizildiği için sabit kalır. Kapanışta 0'a iner (ilk kare = son kare)."""
    if not DRIFT_ON:
        return img
    u = max(0.0, t - GSTART[g])
    r = smooth(u / 0.9) * (1.0 - smooth(prog(t, cues.FINAL_T - 1.5, cues.FINAL_T)))
    if r <= 1e-4:
        return img
    d = r * (0.038 + 0.012 * math.sin(2 * math.pi * u / 8.5 - 1.1))
    m = W / 2 * (1 - 1 / (1.0 + d)) * 0.92     # kayma payı yalnız taban zoom'dan (itiş yanlamasına sarsmasın)
    z = 1.0 + d + punch(t) * (1.0 - smooth(prog(t, cues.FINAL_T - 1.5, cues.FINAL_T)))
    w = 2 * math.pi / 10.5                      # eliptik yol: hız hiçbir an sıfıra inmez
    px = m * math.sin(w * u + 0.6 + 1.3 * g)
    py = m * 1.5 * math.cos(w * u + 0.6 + 1.3 * g)
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
        img = S.scene_hook(0.0, still=True)
    else:
        img = world_image(t)
    fa = cues.flash_alpha(t) if not final else 0.0
    if fa > 0:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 240, 214)), min(1.0, fa))
    ui.draw_hud(img, t)
    if not final:
        ui.draw_captions(img, t)
    return img


def frame_bytes(i):
    return i, render_frame(i).tobytes()
