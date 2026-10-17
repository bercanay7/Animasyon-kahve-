"""Geçiş efektleri: yatay/dikey whip (hareket bulanıklı) ve zoom kesmesi."""
import math

import numpy as np
from PIL import Image

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


def zoom_cut(A, B, p, white=0.40):
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
