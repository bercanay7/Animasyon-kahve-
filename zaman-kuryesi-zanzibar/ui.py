"""1x tuvale (kamera sonrası) çizilen katman: savaş saati (HUD), altyazılar, damga/mühür sprite'ları."""
import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

import events as E
from engine import *  # noqa

GOLD = C["gold"]
WHITE = (255, 255, 255)
NAVY = C["navy"]
RED_HUD = hexc("#FF3B30")

# ─────────────────────────── ALTYAZILAR ───────────────────────────
# (başlangıç, bitiş, metin)  — *yıldızlı* kelimeler altın sarısı
CAPS = [
    (0.0, 1.55, "Tarihin *en kısa* savaşı."),
    (1.55, 3.00, "Sadece *38 dakika* sürdü."),
    (3.00, 4.45, "Ama asıl şok,"),
    (4.45, 6.00, "savaştan *sonra* geldi."),
    (6.00, 8.05, "1896, *Zanzibar.*"),
    (8.05, 11.00, "Sultan ölüyor, yerine *Halid* geçiyor."),
    (11.00, 13.25, "İngiltere’nin şartı:"),
    (13.25, 16.00, "*Saat 9’a kadar* çekil."),
    (16.00, 18.25, "Halid *çekilmiyor.*"),
    (18.25, 20.00, "Ve saat 09:02..."),
    (20.00, 24.00, "Saray *topa tutuluyor.*"),
    (24.00, 28.00, "Sultanın gemisi *batıyor.*"),
    (28.00, 30.00, "Bayrak *iniyor.*"),
    (30.00, 32.00, "Savaş *bitti.*"),
    (32.00, 35.00, "Peki ya *o şok?*"),
    (35.00, 36.45, "İngiltere,"),
    (36.45, 38.55, "attığı *mermilerin parasını*"),
    (38.55, 40.00, "*Zanzibar’a ödetti.*"),
    (40.00, 41.90, "Hepsi bir *kahve molasından* kısa."),
]
CAP_EXIT = 0.10
CAP_MAXW = 960
CAP_Y = 1332


def parse_words(text):
    words, cur, gold = [], "", False
    for ch in text:
        if ch == "*":
            if cur:
                words.append((cur, gold))
                cur = ""
            gold = not gold
        elif ch == " ":
            if cur:
                words.append((cur, gold))
                cur = ""
        else:
            cur += ch
    if cur:
        words.append((cur, gold))
    return words


def layout(words, px):
    f = font(FONT_POP, px)
    space = px * 0.30
    widths = [f.getlength(w) for w, _ in words]
    lines, cur, cw = [], [], 0.0
    for i, w in enumerate(widths):
        add = w if not cur else space + w
        if cur and cw + add > CAP_MAXW:
            lines.append(cur)
            cur, cw = [i], w
        else:
            cur.append(i)
            cw += add
    if cur:
        lines.append(cur)
    return lines, widths, space


def caption_layout(text):
    words = parse_words(text)
    for px in range(88, 67, -4):  # önce tek satır, büyük
        lines, widths, space = layout(words, px)
        if len(lines) == 1:
            return words, lines, widths, space, px
    for px in range(80, 51, -4):  # değilse iki satır
        lines, widths, space = layout(words, px)
        if len(lines) <= 2:
            return words, lines, widths, space, px
    lines, widths, space = layout(words, 52)
    return words, lines, widths, space, 52


_CAPLAY = {c[2]: caption_layout(c[2]) for c in CAPS}


def draw_captions(img, t):
    for (t0, t1, text) in CAPS:
        if not (t0 <= t < t1):
            continue
        words, lines, widths, space, px = _CAPLAY[text]
        n = len(words)
        dt = min(0.30, max(0.15, (t1 - t0) * 0.62 / n))
        exit_k = 1.0 - prog(t, t1 - CAP_EXIT, t1)
        nl = len(lines)
        lh = px * 1.18
        y0 = CAP_Y - (nl - 1) * lh / 2
        for li, idxs in enumerate(lines):
            tot = sum(widths[i] for i in idxs) + space * (len(idxs) - 1)
            x = W / 2 - tot / 2
            y = y0 + li * lh
            for i in idxs:
                wd = widths[i]
                ts = t0 + 0.02 + i * dt
                u = (t - ts) / 0.24
                if u > 0:
                    sc = back_out(u, 2.6)
                    sc = max(0.02, sc) * (0.9 + 0.1 * exit_k)
                    al = clamp(u * 4) * exit_k
                    rise = (1 - ease_out(u, 3)) * 14
                    col = GOLD if words[i][1] else WHITE
                    spr = word_sprite(words[i][0], col, px)
                    blit(img, spr, x + wd / 2, y - rise, sc, al)
                x += wd + space


# ─────────────────────────── SAVAŞ SAATİ (HUD) ───────────────────────────
PILL_W, PILL_H = 330, 98
HUD_Y = 260
HUD_ICON_X = W / 2 - 112  # simge merkezi (yaklaşık 428)


def _hud_icon(d, cx, cy, r, color, ang, bg):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=int(r * 0.16))
    d.rectangle([cx - r * 0.22, cy - r * 1.32, cx + r * 0.22, cy - r * 1.02], fill=color)
    d.rectangle([cx - r * 0.55, cy - r * 1.42, cx + r * 0.55, cy - r * 1.28], fill=color)
    a = math.radians(ang)
    d.line([(cx, cy), (cx + math.sin(a) * r * 0.72, cy - math.cos(a) * r * 0.72)], fill=color, width=int(r * 0.16))
    d.ellipse([cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13], fill=color)


@lru_cache(maxsize=4096)
def hud_sprite(mm, ss, colon, invert, red, icon_ang, pop):
    """2x sprite (RGBA). red: kırmızı mod; invert: kırmızı arka plan/koyu yazı (yanıp sönme)"""
    k = 2
    w, h = int(PILL_W * k), int(PILL_H * k)
    pad = 24
    lay = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    # gölge
    d.rounded_rectangle([pad, pad + 8, pad + w, pad + h + 8], radius=h // 2, fill=(0, 0, 0, 90))
    if red and invert:
        bg, fg, bd = RED_HUD, (255, 255, 255), (255, 255, 255)
    elif red:
        bg, fg, bd = hexc("#2B0F14"), RED_HUD, RED_HUD
    else:
        bg, fg, bd = NAVY, GOLD, GOLD
    d.rounded_rectangle([pad, pad, pad + w, pad + h], radius=h // 2, fill=bg + (245,), outline=bd, width=3 * k)
    f = font(FONT_POP, 62 * k)
    cell = 37 * k
    colw = 20 * k
    total = 4 * cell + colw
    icon_r = 24 * k
    gap = 18 * k
    block = icon_r * 2 + gap + total
    x0 = pad + w / 2 - block / 2
    cy = pad + h / 2
    _hud_icon(d, x0 + icon_r, cy + 4 * k, icon_r * 0.9, fg, icon_ang, bg)
    x = x0 + icon_r * 2 + gap
    ty = cy - 2 * k
    s = f"{mm:02d}{ss:02d}"
    for i, ch in enumerate(s):
        if i == 2:
            d.text((x + colw / 2, ty), ":", font=f, fill=fg if colon else mix(bg, fg, 0.30), anchor="mm")
            x += colw
        d.text((x + cell / 2, ty), ch, font=f, fill=fg, anchor="mm")
        x += cell
    if pop > 1.001:
        pass
    return lay


def hud_state(t):
    sec = E.war_sec(t)
    mode = E.hud_mode(t)
    isec = int(sec)
    mm, ss = isec // 60, isec % 60
    red = mode == "frozen"
    invert = red and (int((t - E.T_FREEZE) * 4) % 2 == 1)
    if mode == "idle":
        colon = (t % 1.0) < 0.55
        icon_ang = (int(t) * 6 + 360 * back_out(prog(t % 1.0, 0, 0.14)) / 60) if t < 16 else 0.0
        icon_ang = (t * 360.0) % 360 if t < 16 else icon_ang
    elif mode == "frozen":
        colon = True
        icon_ang = 0.0
    else:
        colon = True
        icon_ang = (t * 720.0) % 360
    if mode == "rewind":
        icon_ang = (-t * 1080.0) % 360
    return mm, ss, colon, invert, red, icon_ang


def draw_hud(img, t, scale=1.0, cx=W / 2, cy=HUD_Y):
    mm, ss, colon, invert, red, ang = hud_state(t)
    # tık vuruşunda hafif nabız
    pulse = 1.0
    if E.hud_mode(t) == "idle" and t < 16:
        pulse = 1 + 0.035 * math.sin(math.pi * clamp((t % 1.0) / 0.18)) if (t % 1.0) < 0.18 else 1.0
    if E.hud_mode(t) == "frozen":
        pulse = 1 + 0.03 * math.sin((t - E.T_FREEZE) * 8 * math.pi) ** 2
    spr = hud_sprite(mm, ss, colon, invert, red, int(ang // 3) * 3, 1)
    blit(img, spr, cx, cy, scale * pulse, 1.0)


# ─────────────────────────── SPRITE'LAR ───────────────────────────
@lru_cache(maxsize=8)
def date_stamp_sprite(text="27 AĞUSTOS 1896"):
    k = 2
    f = font(FONT_LORA, 84 * k)
    l, t0, r, b = f.getbbox(text)
    w, h = int(r - l + 90 * k), int(150 * k)
    pad = 20
    lay = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([pad + 8, pad + 12, pad + w + 8, pad + h + 12], radius=26, fill=(0, 0, 0, 100))
    d.rounded_rectangle([pad, pad, pad + w, pad + h], radius=26, fill=(255, 244, 218, 250), outline=C["red"], width=9 * k // 2)
    d.rounded_rectangle([pad + 16, pad + 16, pad + w - 16, pad + h - 16], radius=18, outline=C["red"], width=3 * k)
    d.text((pad + w / 2, pad + h / 2 + 4), text, font=f, fill=C["red_dk"], anchor="mm")
    return lay


@lru_cache(maxsize=2)
def seal_sprite():
    """Büyük kırmızı mühür: '38 DAKİKA'"""
    k = 2
    S = 640 * k
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = S / 2
    red = (205, 32, 52)
    d.ellipse([c - 300 * k, c - 292 * k, c + 300 * k, c + 308 * k], fill=(0, 0, 0, 90))
    d.ellipse([c - 300 * k, c - 300 * k, c + 300 * k, c + 300 * k], fill=red)
    d.ellipse([c - 270 * k, c - 270 * k, c + 270 * k, c + 270 * k], outline=(255, 226, 214), width=8 * k)
    d.ellipse([c - 238 * k, c - 238 * k, c + 238 * k, c + 238 * k], outline=(255, 226, 214), width=3 * k)
    # tırtıklı kenar
    for i in range(48):
        a = i * 2 * math.pi / 48
        x, y = c + math.cos(a) * 300 * k, c + math.sin(a) * 300 * k
        d.ellipse([x - 9 * k, y - 9 * k, x + 9 * k, y + 9 * k], fill=red)
    f1 = font(FONT_LORA, 250 * k)
    f2 = font(FONT_LORA, 92 * k)
    d.text((c, c - 36 * k), "38", font=f1, fill=(255, 244, 232), anchor="mm")
    d.text((c, c + 124 * k), "DAKİKA", font=f2, fill=(255, 244, 232), anchor="mm")
    # yıldızlar
    for sx in (-1, 1):
        px, py = c + sx * 168 * k, c + 196 * k
        pts = []
        for j in range(10):
            r_ = 22 * k if j % 2 == 0 else 9 * k
            a = -math.pi / 2 + j * math.pi / 5
            pts.append((px + math.cos(a) * r_, py + math.sin(a) * r_))
        d.polygon(pts, fill=(255, 226, 214))
    return lay


@lru_cache(maxsize=16)
def note_sprite(text, px=42):
    return word_sprite(text, hexc("#FFF1D0"), px, stroke=4)


def draw_stamp_pop(img, spr, cx, cy, u, rot, end_scale=1.0, start_scale=2.6):
    """u: geçen süre (sn). Damga vuruşu: büyükten oturur."""
    if u < 0:
        return
    k = ease_out(prog(u, 0, 0.14), 3)
    sc = lerp(start_scale, end_scale, k)
    if u > 0.14:
        sc = end_scale * (1 + 0.04 * math.exp(-(u - 0.14) / 0.12) * math.sin((u - 0.14) * 40))
    al = clamp(u / 0.06)
    blit(img, spr, cx, cy, sc, al, rot)


# ─────────────────────────── GENEL KATMAN ───────────────────────────
_VIG = None


def vignette_arrays():
    global _VIG
    if _VIG is None:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.hypot((x - W / 2) / (W * 0.75), (y - H * 0.47) / (H * 0.62))
        vig = 1 - 0.30 * np.clip(r - 0.45, 0, 1) ** 1.6
        band = np.clip((y - 1130) / 220.0, 0, 1) * 0.40
        _VIG = (vig.astype(np.float32), band.astype(np.float32))
    return _VIG


def finalize(img, extra_dark=0.0):
    """vinyet + alt yazı bandı (okunurluk). img: PIL RGB"""
    vig, band = vignette_arrays()
    a = np.asarray(img, dtype=np.float32)
    a *= vig[..., None]
    a *= (1 - band[..., None] * 0.9)
    if extra_dark > 0:
        a *= (1 - extra_dark)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
