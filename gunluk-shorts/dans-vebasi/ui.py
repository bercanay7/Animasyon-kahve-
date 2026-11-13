"""1x katman: kâğıt etiket altyazıları (kelime kelime pop) ve dansçı sayacı (HUD, y≈262)."""
import math
import numpy as np
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

import cues
from art import *  # noqa
from cutout import *  # noqa
from engine import *  # noqa

CAP_Y = 1332
CAP_MAXW = 980
HUD_Y = 262
TAG_PAD = 22


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


# ───────────────────────── altyazı sayfaları ─────────────────────────
def build_pages():
    words = []
    for s in cues.TL["sentences"]:
        words += s["words"]
    pages, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        last = w["show"][-1] if w["show"] else ""
        brk = last in ".!?:" or (last == "," and len(cur) >= 3) or len(cur) >= 6
        if brk or i == len(words) - 1:
            pages.append(cur)
            cur = []
    out = []
    for p in pages:
        if out and len(p) == 1 and len(out[-1]) < 5 and out[-1][-1]["show"][-1:] not in ".!?:":
            out[-1] += p
        else:
            out.append(p)
    return out


PAGES = build_pages()


def _layout(page):
    for px in range(84, 51, -4):
        f = font(FONT_POP, px)
        space = px * 0.22
        widths = [f.getlength(w["show"]) + 2 * TAG_PAD * px / 80 for w in page]
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


@lru_cache(maxsize=1024)
def tag_sprite(word, emph, px, seed):
    """Kâğıt etiket üstünde kelime (2x RGBA): kenarlar el kesimi, gölgeli"""
    k = 2
    f = font(FONT_POP, px * k)
    tw = f.getlength(word)
    pad = int(TAG_PAD * px / 80 * k)
    w, h = int(tw + 2 * pad), int(px * 1.28 * k)
    m = 26
    lay = Image.new("RGBA", (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    r = lambda a, b: rng_hash(seed, a, b) * 7 - 3.5
    pts = [(m + r(1, 1) * k, m + r(1, 2) * k), (m + w + r(2, 1) * k, m + r(2, 2) * k), (m + w + r(3, 1) * k, m + h + r(3, 2) * k),
           (m + r(4, 1) * k, m + h + r(4, 2) * k)]
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 5 * k, y + 7 * k) for x, y in pts], fill=(24, 14, 8, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(3 * k))
    lay = Image.alpha_composite(lay, sh)
    d = ImageDraw.Draw(lay)
    cx, cy = sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4
    d.polygon([(x + (x - cx) * 0.02, y + (y - cy) * 0.04) for x, y in pts], fill=PARCH_LT + (255,))
    inner = [(x + (cx - x) * 0.02, y + (cy - y) * 0.03) for x, y in pts]
    d.polygon(inner, fill=(RED if emph else PARCH_LT) + (255,))
    if not emph:
        d.polygon(inner, fill=(250, 240, 214, 255))
    d.text((cx, cy + 3 * k), word, font=f, fill=(250, 236, 208) if emph else INK, anchor="mm")
    return lay


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
    lh = px * 1.42
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
            u = (t - ts) / 0.20
            if u > 0:
                sc = max(0.05, back_out(u, 1.9)) * (0.94 + 0.06 * exit_k)
                al = clamp(u * 5) * exit_k
                rise = (1 - ease_out(u, 3)) * 18
                seed = sum(map(ord, w["show"])) % 997
                rot = (rng_hash(seed, 5) - 0.5) * 6.0
                blit(img, tag_sprite(w["show"], bool(w["emph"]), px, seed), x + wd / 2, y - rise, sc, al, rot=rot)
            x += wd + space


# ───────────────────────── dansçı sayacı (HUD) ─────────────────────────
def draw_hud(img, t):
    n = cues.dancers(t)
    w, h = 560, 118
    ox, oy = W / 2 - w / 2, HUD_Y - h / 2
    p = Patch(ox, oy, w, h, bg=(0, 0, 0))
    p.cam(W / 2, H / 2, 1.0)
    # saydam arka plan yerine kâğıt levha: önce örnek renkle doldur
    pl = [(8, 12), (w - 8, 8), (w - 6, h - 10), (10, h - 6)]
    c = Cut(p, t, shadow=(5, 7), shadow_a=0.35, rim=3.0, wob=1.0)
    c.add(pl, BROWN_DK, 3)
    c.add([(x + (w / 2 - x) * 0.04, y + (h / 2 - y) * 0.10) for x, y in pl], PARCH_LT, 4, rim=False)
    c.flush()
    # küçük dansçı simgesi
    ph = t * 9.0
    dancer(p, 66, h - 12, 0.30, t, ph, kind=0, seed=2, face=False)
    p.text(230, h / 2 + 2, "DANSÇI", 44, RED, path=FONT_POP)
    p.text(430, h / 2 + 4, str(n), 66, INK, path=FONT_POP)
    patch = p.finish()
    # kâğıt levhanın dışı: ana görüntüden alınan arka planla birleştir (koyu pikselleri maskele)
    mask = Image.new("L", patch.size, 0)
    md = ImageDraw.Draw(mask)
    for q in range(1):
        md.polygon([(x + 0, y + 0) for x, y in pl], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.0))
    # gölge dahil tüm bölgeyi maskele: kenarlardan yumuşak
    full = Image.new("L", patch.size, 255)
    ar = np.asarray(patch, dtype=np.int16)
    isbg = (ar.sum(axis=2) < 6)
    m = Image.fromarray(np.where(isbg, 0, 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.8))
    img.paste(patch, (int(ox), int(oy)), m)
