"""1x katman: mono altyazılar (kelime kelime pop, amber vurgu) ve benzerlik sayacı (HUD, y≈262)."""
import math

import numpy as np
from PIL import Image, ImageDraw

import cues
from bp import *  # noqa
from engine import *  # noqa

CAP_Y = 1332
CAP_MAXW = 990
HUD_Y = 262


class Patch(Ctx):
    def __init__(self, ox, oy, w, h, bg=(0, 0, 0)):
        self.im = Image.new("RGB", (int(w * SS), int(h * SS)), bg)
        self.d = ImageDraw.Draw(self.im)
        self.cx, self.cy, self.z = W / 2, H / 2, 1.0
        self.shx = self.shy = 0.0
        self.par = 1.0
        self.size = (int(w), int(h))

    def finish(self):
        return self.im.reduce(SS)


def build_pages():
    words = []
    for s in cues.TL["sentences"]:
        words += s["words"]
    pages, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        last = w["show"][-1] if w["show"] else ""
        brk = last in ".!?:" or (last == "," and len(cur) >= 3) or len(cur) >= 5
        if brk or i == len(words) - 1:
            pages.append(cur)
            cur = []
    out = []
    for p in pages:
        if out and len(p) == 1 and len(out[-1]) < 4 and out[-1][-1]["show"][-1:] not in ".!?:":
            out[-1] += p
        else:
            out.append(p)
    return out


PAGES = build_pages()


def _layout(page):
    for px in range(76, 47, -4):
        f = font(FONT_MONO, px)
        space = px * 0.60
        widths = [f.getlength(w["show"]) for w in page]
        lines, cur, cw = [], [], 0.0
        for i, wd in enumerate(widths):
            add = wd if not cur else space + wd
            if cur and cw + add > CAP_MAXW:
                lines.append(cur)
                cur, cw = [i], wd
            else:
                cur.append(i)
                cw += add
        if cur:
            lines.append(cur)
        if len(lines) <= 2:
            return lines, widths, space, px
    return lines, widths, space, px


_PL = [_layout(p) for p in PAGES]


def draw_captions(img, t):
    cur = None
    for i, p in enumerate(PAGES):
        t0 = p[0]["t0"] - 0.03
        t1 = (PAGES[i + 1][0]["t0"] - 0.03) if i + 1 < len(PAGES) else cues.CAP_END
        if t0 <= t < t1:
            cur = (i, t0, t1)
            break
    if cur is None:
        return
    i, t0, t1 = cur
    page = PAGES[i]
    lines, widths, space, px = _PL[i]
    nl = len(lines)
    lh = px * 1.3
    y0 = CAP_Y - (nl - 1) * lh / 2
    exit_k = 1.0 - prog(t, t1 - 0.06, t1) if i + 1 < len(PAGES) else 1.0
    for li, idxs in enumerate(lines):
        tot = sum(widths[j] for j in idxs) + space * (len(idxs) - 1)
        x = W / 2 - tot / 2
        y = y0 + li * lh
        for j in idxs:
            w = page[j]
            wd = widths[j]
            ts = w["t0"] - 0.03
            u = (t - ts) / 0.18
            if u > 0:
                sc = max(0.05, back_out(u, 1.8)) * (0.94 + 0.06 * exit_k)
                al = clamp(u * 5) * exit_k
                rise = (1 - ease_out(u, 3)) * 14
                col = AMBER if w["emph"] else (255, 255, 255)
                spr = word_sprite(w["show"], col, px, FONT_MONO, 7, NAVY_DK, False)
                blit(img, spr, x + wd / 2, y - rise, sc, al)
            x += wd + space


def draw_hud(img, t):
    n = cues.sims(t)
    shown = int(round(n))
    w, h = 560, 116
    ox, oy = W / 2 - w / 2, HUD_Y - h / 2
    p = Patch(ox, oy, w, h, bg=NAVY_DK)
    p.cam(W / 2, H / 2, 1.0)
    box = [(8, 8), (w - 8, 8), (w - 8, h - 8), (8, h - 8)]
    p.poly(box, (8, 30, 62))
    full = shown >= 5 and t > cues.RESET1
    col = GREEN if full else LINE
    L(p, box, 4, col, 1.0, 1.0, glow=False, closed=True)
    for (x, y, dx, dy) in ((8, 8, 1, 1), (w - 8, 8, -1, 1), (8, h - 8, 1, -1), (w - 8, h - 8, -1, -1)):
        L(p, [(x, y + dy * 18), (x, y), (x + dx * 18, y)], 7, AMBER, 1.0, 1.0, glow=False)
    p.text(172, h / 2 + 3, "BENZERLİK", 44, LINE_DIM if not full else GREEN, path=FONT_MONO)
    p.text(448, h / 2 + 5, f"{shown}/5", 68, AMBER if not full else GREEN, path=FONT_MONO)
    patch = p.finish()
    jit = 0
    pulse = [ts for ts in cues.SIM_T if 0 <= t - ts < 0.35]
    if pulse:
        jit = int(round(math.sin((t - pulse[-1]) * 60) * 3))
    img.paste(patch, (int(ox), int(oy) + jit))
