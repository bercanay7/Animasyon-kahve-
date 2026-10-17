"""1x katman: Fraunces altyazılar (kelime kelime pop, lamba sarısı vurgu) ve HUD (KANIT + 4 kapsüllük sayaç; seri adı yalnız açıklamada)."""
import math

import cues
from guaj import *  # noqa

CAP_Y = 1336
CAP_MAXW = 960
HUD_Y = 262
CAP_COL = (255, 244, 220)
CAP_STROKE = (36, 20, 10)


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
    for px in range(78, 51, -4):
        f = font(FONT_SOFT, px)
        space = f.getlength(" ") * 1.12
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
    lh = px * 1.26
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
                col = cues.EMPH_C if w["emph"] else CAP_COL
                spr = word_sprite(w["show"], col, px, FONT_SOFT, 7, CAP_STROKE, True)
                blit(img, spr, x + wd / 2, y - rise, sc, al)
            x += wd + space


# ───────────────────────── HUD ─────────────────────────
HUD_W, HUD_H = 600, 104


def _capsule(p, cx, cy, w, h, fill_k, age):
    """4 kapsüllük sayaç: boşken kontur, dolunca kiremit kırmızısı + onay; dolum anında küçük pop."""
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - h / 2, cy + h / 2
    sc = 1.0
    if age is not None and age < 0.35:
        sc = 1.0 + 0.32 * math.sin(clamp(age / 0.35) * math.pi)
    X = Xf(cx, cy, sc, rot=-14)
    body = [X.p(-w / 2, -h / 2), X.p(w / 2, -h / 2), X.p(w / 2, h / 2), X.p(-w / 2, h / 2)]
    left = [X.p(-w / 2, -h / 2), X.p(0, -h / 2), X.p(0, h / 2), X.p(-w / 2, h / 2)]
    p.line(body + [body[0]], 6, CREAM, 1.0, cap=True)
    p.poly(body, Hx("#4A3322"))
    if fill_k > 0:
        right = [X.p(0, -h / 2), X.p(w / 2, -h / 2), X.p(w / 2, h / 2), X.p(0, h / 2)]
        p.poly(left, CREAM)
        p.poly(right, BRICK)
        p.line(body + [body[0]], 4, INK, 1.0, cap=True)
        p.line([X.p(0, -h / 2), X.p(0, h / 2)], 3, INK, 0.8, cap=False)
    else:
        p.line(body + [body[0]], 3, Hx("#8A6A4A"), 1.0, cap=True)


def draw_hud(img, t):
    n = cues.kanit(t)
    w, h = HUD_W, HUD_H
    ox, oy = W / 2 - w / 2, HUD_Y - h / 2
    p = Patch(w, h, bg=Hx("#2A170C"))
    p.cam(W / 2, H / 2, 1.0)
    # boyalı etiket: iç çerçeve + yazı
    p.line([(8, 8), (w - 8, 8), (w - 8, h - 8), (8, h - 8), (8, 8)], 3, Hx("#8A6A4A"), 0.9, cap=False)
    p.text(128, h / 2 + 3, "KANIT", 44, CREAM, path=FONT_SLAB)
    for i in range(4):
        age = cues.kanit_age(t, i)
        _capsule(p, 282 + i * 80, h / 2 + 1, 62, 30, 1.0 if age is not None else 0.0, age)
    patch = p.finish()
    jit = 0
    pulse = [ts for ts in cues.PULSES if 0 <= t - ts < 0.35]
    if pulse and n:
        jit = int(round(math.sin((t - pulse[-1]) * 60) * 3))
    _paste_panel(img, patch, ox, oy + jit)


def _paste_panel(img, patch, x, y, r=20):
    w, h = patch.size
    m = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    img.paste(patch, (int(x), int(y)), m)


def bottom_shade(img, k=0.34):
    """Alt bölgede sabit koyu geçiş: altyazı okunurluğu (her karede aynı → döngü ve ilk=son kare bozulmaz)."""
    a = np.asarray(img, dtype=np.float32)
    ys = np.arange(H, dtype=np.float32)
    g = np.clip((ys - 1150) / 330, 0, 1) ** 1.3 * k
    a *= (1 - g)[:, None, None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
