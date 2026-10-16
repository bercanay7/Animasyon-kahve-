"""1x katman: serif altyazılar (kelime kelime pop, tema renkli vurgu) ve KANIT etiketi (HUD, y≈262)."""
import math

import cues
from paper import *  # noqa

CAP_Y = 1336
CAP_MAXW = 960
HUD_Y = 262
CAP_COL = (255, 246, 227)
CAP_STROKE = (30, 14, 8)


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
    for px in range(74, 47, -4):
        f = font(FONT_SERIF, px)
        space = f.getlength(" ") * 1.15
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
    lh = px * 1.28
    y0 = CAP_Y - (nl - 1) * lh / 2
    exit_k = 1.0 - prog(t, t1 - 0.06, t1) if i + 1 < len(PAGES) else 1.0
    ecol = cues.emph_color(t)
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
                col = ecol if w["emph"] else CAP_COL
                spr = word_sprite(w["show"], col, px, FONT_SERIF, 7, CAP_STROKE, True)
                blit(img, spr, x + wd / 2, y - rise, sc, al)
            x += wd + space


def draw_hud(img, t):
    n = cues.kanit(t)
    w, h = 410, 112
    ox, oy = W / 2 - w / 2, HUD_Y - h / 2
    p = Patch(w, h, bg=CREAM)
    p.cam(W / 2, H / 2, 1.0)
    # kâğıt etiket: delik + ince kenar
    p.circ(46, h / 2, 17, Hx("#2B1A12"))
    p.circ(46, h / 2, 11, Hx("#6B4B33"))
    p.line([(10, 10), (w - 10, 10), (w - 10, h - 10), (10, h - 10), (10, 10)], 2.4, Hx("#C9B58A"), 0.9, cap=False)
    p.text(172, h / 2 + 3, "KANIT", 44, INK, path=FONT_TITLE)
    if n is None:
        p.text(322, h / 2 + 3, "?", 70, RED, path=FONT_TITLE)
    else:
        p.text(322, h / 2 + 3, f"{n}/5", 66, RED if n < 5 else Hx("#1F7A45"), path=FONT_TITLE)
    patch = p.finish()
    jit = 0
    pulse = [ts for ts in cues.PULSES if 0 <= t - ts < 0.35]
    if pulse and n is not None:
        jit = int(round(math.sin((t - pulse[-1]) * 60) * 3))
    paste_panel(img, patch, ox, oy + jit, r=22, shadow=True)
