"""1x katman: kelime kelime pop eden altyazı (fosforlu vurgu) ve mermi sayacı (HUD, y≈260)."""
import math
from functools import lru_cache

from PIL import Image, ImageDraw

import cues
from art import *  # noqa
from engine import *  # noqa
from sketch import *  # noqa

CAP_Y = 1330
CAP_MAXW = 960
HUD_Y = 262


class Patch(Ctx):
    """Küçük bir bölgeyi (ox,oy,w,h) 2x süper örnekleyerek çizen bağlam — dünya koordinatı = ekran koordinatı."""

    def __init__(self, ox, oy, w, h):
        self.im = Image.new("RGB", (int(w * SS), int(h * SS)), PAPER)
        self.d = ImageDraw.Draw(self.im)
        self.cx, self.cy, self.z = W / 2 + ox, H / 2 + oy, 1.0
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
        brk = last in ".!?:" or (last == "," and len(cur) >= 4) or len(cur) >= 7
        # çok kısa cümle sonu sonraki sayfaya yapışmasın
        if brk or i == len(words) - 1:
            pages.append(cur)
            cur = []
    # tek kelimelik artıkları öncekiyle birleştir
    out = []
    for p in pages:
        if out and len(p) == 1 and len(out[-1]) < 6 and out[-1][-1]["show"][-1:] not in ".!?:":
            out[-1] += p
        else:
            out.append(p)
    return out


PAGES = build_pages()


def _layout(page):
    for px in range(88, 51, -4):
        f = font(FONT_POP, px)
        space = px * 0.30
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


@lru_cache(maxsize=512)
def _hl_sprite(w, h, seed):
    """Fosforlu kalem şeridi (hafif pürüzlü uçlar), 2x"""
    k = 2
    lay = Image.new("RGBA", (int(w * k) + 40, int(h * k) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    W2, H2 = int(w * k), int(h * k)
    pts = [(14, 12 + rng_hash(seed, 1) * 10), (W2 + 14, 4 + rng_hash(seed, 2) * 12), (W2 + 22, H2 * 0.5), (W2 + 10, H2 + 6 - rng_hash(seed, 3) * 10),
           (10, H2 + 12 - rng_hash(seed, 4) * 8), (4, H2 * 0.5)]
    d.polygon(pts, fill=HL + (235,))
    return lay


def draw_captions(img, t):
    # geçerli sayfa
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
    lh = px * 1.2
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
                sc = max(0.05, back_out(u, 1.7)) * (0.94 + 0.06 * exit_k)
                al = clamp(u * 5) * exit_k
                rise = (1 - ease_out(u, 3)) * 16
                if w["emph"]:
                    hw = wd + 22
                    hh = px * 0.82
                    spr = _hl_sprite(int(hw), int(hh), sum(map(ord, w["show"])) % 997)
                    sweep = ease_out(prog(t, ts, ts + 0.22))
                    sp2 = spr.crop((0, 0, int(spr.width * max(0.02, sweep)), spr.height))
                    blit(img, sp2, x + wd / 2 - (hw * (1 - sweep)) / 2, y - rise + px * 0.07, sc, al * 0.95, rot=-1.5)
                spr = word_sprite(w["show"], INK, px, FONT_POP, 6, PAPER, False)
                blit(img, spr, x + wd / 2, y - rise, sc, al)
            x += wd + space


# ───────────────────────── mermi sayacı (HUD) ─────────────────────────
def fmt(n):
    s = f"{int(n):,}".replace(",", ".")
    return s


def hud_patch(t, locked_flash=0.0):
    n = cues.ammo(t)
    w, h = 580, 112
    ox, oy = W / 2 - w / 2, HUD_Y - h / 2
    p = Patch(ox, oy, w, h)
    p.cam(W / 2, H / 2, 1.0)
    box = [(10, 12), (w - 10, 10), (w - 8, h - 12), (12, h - 10)]
    p.poly(box, PAPER)
    shape(p, box, INK, 6, 7, t, 1.8, smooth=False)
    if locked_flash > 0:
        shape(p, [(6, 8), (w - 6, 6), (w - 4, h - 8), (8, h - 6)], ACC, 6 * locked_flash + 2, 8, t, 2.4, smooth=False)
    bullet(p, 62, h / 2 + 2, 1.8, -18, 3, t)
    p.text(208, h / 2 + 3, "MERMİ", 42, ACC, path=FONT_POP)
    p.text(448, h / 2 + 4, fmt(n), 66, INK, path=FONT_POP)
    return p.finish(), (int(ox), int(oy))


def draw_hud(img, t):
    flash = 0.0
    tl = cues.wt("I", 1) + 0.18
    if tl <= t < tl + 0.5:
        flash = 1 - (t - tl) / 0.5
    patch, pos = hud_patch(t, flash)
    # sayaç artarken kutu hafifçe titrer
    jit = 0
    if cues.AMMO_KEYS[0][0] < t < tl:
        jit = int(round(math.sin(t * 40) * 2))
    img.paste(patch, (pos[0], pos[1] + jit))
