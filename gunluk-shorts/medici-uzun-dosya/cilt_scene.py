"""cilt_scene — Medici cildi sahne resimleri: friz manzarası (Gozzoli tarzı tepeler/selvi/portakal/şato), Floransa silueti (Duomo kubbesi, Giotto çan kulesi,
Palazzo Vecchio kulesi, Vaftizhane, Arno + Ponte Vecchio). Hepsi vektör (Skia) + numpy doku/aşınma; sprite/katman olarak önbelleklenir.
Fresk hissi: pigment kenarı (ince mürekkep), çatlak ağı + boya kaybı (alfa delikleri: altta sıva görünür)."""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import sk
from sk import C, Frame, clamp, mix

PIG = CM.PIG


def _ridge(rs, width, base, amp, scale, octaves=3):
    """Tepe çizgisi: x → y (yumuşak gürültü)."""
    xs = np.arange(0, width + 8, 8, dtype=np.float32)
    y = np.zeros_like(xs)
    a = 1.0
    f = 1.0
    ph = rs.uniform(0, 100, octaves)
    for o in range(octaves):
        y += a * np.sin(xs / (scale / f) + ph[o]) * 0.6 + a * 0.4 * np.sin(xs / (scale * 0.37 / f) + ph[o] * 1.7)
        a *= 0.5
        f *= 2.0
    y = base + y / 1.6 * amp
    return xs, y


def _poly_from_ridge(xs, ys, bottom):
    pts = [(float(x), float(y)) for x, y in zip(xs, ys)]
    pts += [(float(xs[-1]), bottom), (float(xs[0]), bottom)]
    return sk.poly_path(pts, True)


def cypress(c, x, y, h, col="#2E4A33", rim="#4F6E4A"):
    """Selvi (alev biçimli koyu yeşil)."""
    w = h * 0.17
    p = sk.smooth_path([(x, y - h), (x + w * 0.55, y - h * 0.72), (x + w, y - h * 0.38), (x + w * 0.8, y), (x - w * 0.8, y), (x - w, y - h * 0.38), (x - w * 0.55, y - h * 0.72)], True, 0.5)
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=C(col)))
    c.save()
    c.clipPath(p, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(x - w * 1.1, y - h, x - w * 0.15, y), skia.Paint(Color=C(rim, 110)))
    c.restore()
    c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#14200E", 190)))
    c.drawRect(skia.Rect.MakeLTRB(x - 1.6, y, x + 1.6, y + h * 0.06), skia.Paint(Color=C("#3A2A18")))


def umbrella_pine(c, x, y, h, col="#3C5A38"):
    c.drawRect(skia.Rect.MakeLTRB(x - h * 0.02, y - h * 0.62, x + h * 0.02, y), skia.Paint(Color=C("#4A3220")))
    for dx, dy, r in ((0, -0.78, 0.26), (-0.18, -0.70, 0.18), (0.20, -0.72, 0.19)):
        c.drawOval(skia.Rect.MakeLTRB(x + dx * h - r * h, y + dy * h - r * h * 0.55, x + dx * h + r * h, y + dy * h + r * h * 0.55), skia.Paint(AntiAlias=True, Color=C(col)))
    c.drawOval(skia.Rect.MakeLTRB(x - h * 0.30, y - h * 0.86, x + h * 0.05, y - h * 0.72), skia.Paint(AntiAlias=True, Color=C("#6E8E58", 120)))


def orange_tree(c, x, y, h, rs):
    """Portakal/nar ağacı: koyu yeşil yuvarlak taç + turuncu meyveler."""
    c.drawRect(skia.Rect.MakeLTRB(x - h * 0.03, y - h * 0.45, x + h * 0.03, y), skia.Paint(Color=C("#4A3220")))
    R = h * 0.36
    cy = y - h * 0.68
    c.drawCircle(x, cy, R, skia.Paint(AntiAlias=True, Color=C("#35552F")))
    c.drawCircle(x - R * 0.28, cy - R * 0.26, R * 0.62, skia.Paint(AntiAlias=True, Color=C("#4C7A3C", 150)))
    c.drawCircle(x, cy, R, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#14200E", 190)))
    for i in range(int(14 + h / 18)):
        a = rs.uniform(0, 2 * math.pi)
        rr = R * math.sqrt(rs.uniform(0.05, 0.85))
        c.drawCircle(x + math.cos(a) * rr, cy + math.sin(a) * rr, h * 0.026, skia.Paint(AntiAlias=True, Color=C("#E08A2E")))
        c.drawCircle(x + math.cos(a) * rr - h * 0.008, cy + math.sin(a) * rr - h * 0.008, h * 0.009, skia.Paint(AntiAlias=True, Color=C("#FFE3A0", 170)))


def castle(c, x, y, s, wall="#E6D9B8", roof="#B4552E"):
    """Tepe şatosu (Gozzoli tarzı): surlu, kuleli, kırmızı kiremit çatılı."""
    c.drawRect(skia.Rect.MakeLTRB(x - s * 0.55, y - s * 0.50, x + s * 0.55, y), skia.Paint(Color=C(wall)))
    for k in range(7):
        c.drawRect(skia.Rect.MakeLTRB(x - s * 0.55 + k * s * 0.17, y - s * 0.58, x - s * 0.55 + k * s * 0.17 + s * 0.09, y - s * 0.50), skia.Paint(Color=C(wall)))
    for dx, hh in ((-0.45, 0.95), (0.42, 0.80)):
        c.drawRect(skia.Rect.MakeLTRB(x + dx * s - s * 0.10, y - hh * s, x + dx * s + s * 0.10, y), skia.Paint(Color=C(mix(wall, "#FFFFFF", 0.1))))
        c.drawPath(sk.poly_path([(x + dx * s - s * 0.14, y - hh * s), (x + dx * s, y - (hh + 0.28) * s), (x + dx * s + s * 0.14, y - hh * s)]), skia.Paint(AntiAlias=True, Color=C(roof)))
    c.drawRect(skia.Rect.MakeLTRB(x - s * 0.12, y - s * 0.28, x + s * 0.12, y), skia.Paint(Color=C("#3A2A18")))
    for dx in (-0.30, 0.28):
        c.drawRect(skia.Rect.MakeLTRB(x + dx * s - s * 0.03, y - s * 0.38, x + dx * s + s * 0.03, y - s * 0.30), skia.Paint(Color=C("#3A2A18")))
    c.drawRect(skia.Rect.MakeLTRB(x - s * 0.55, y - s * 0.50, x + s * 0.55, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#3A2A18", 160)))


def sky_gradient(c, w, h, top="#6F94CE", mid="#B8CCDC", hor="#F0E5C6"):
    sh = skia.GradientShader.MakeLinear([(0, 0), (0, h)], [C(top), C(mid), C(hor)], [0.0, 0.62, 1.0])
    c.drawRect(skia.Rect.MakeWH(w, h), skia.Paint(Shader=sh))


def clouds(c, w, h, rs, n=7):
    for i in range(n):
        x, y = rs.uniform(0, w), rs.uniform(h * 0.05, h * 0.55)
        L = rs.uniform(180, 420)
        for k in range(4):
            c.drawOval(skia.Rect.MakeLTRB(x + k * L * 0.18, y - 10 - rs.uniform(0, 8), x + k * L * 0.18 + L * 0.5, y + 10 + rs.uniform(0, 6)), skia.Paint(AntiAlias=True, Color=C("#FFFFFF", 70), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7)))


def _bake_texture(arr, rs, loss=0.5, cracks=0.8):
    """Bant görüntüsüne çatlak ağı + kenarlardan başlayan boya kaybı (alfa delikleri)."""
    h, w = arr.shape[:2]
    cm = np.clip(CW.micro_craquelure(rs, h, w, ncell=max(180, int(w * h / 3200)), warp=6.0) * 0.5 + CW.long_cracks(rs, h, w, n=max(3, w // 500)) * 1.0, 0, 1)
    col = arr[..., :3].astype(np.float32)
    col = col * (1 - cm[..., None] * 0.55 * cracks) + np.array([200, 188, 160], np.float32) * cm[..., None] * 0.20 * cracks
    # kayıp: kenarlara yakın gürültü eşiği
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ed = np.minimum(np.minimum(yy, h - 1 - yy) / (h * 0.5), np.minimum(xx, w - 1 - xx) / (w * 0.5))
    ln = CW.lf(rs, h, w, 28) * 0.7 + CW.lf(rs, h, w, 8) * 0.5
    edge_w = np.clip(1.0 - ed * 5.0, 0, 1)
    lossm = CW.sstep(1.55 - 0.25 * loss, 1.95 - 0.25 * loss, ln + edge_w * 1.1)
    al = arr[..., 3].astype(np.float32) * (1 - lossm)
    plast = np.array([205, 195, 168], np.float32)
    edge = np.clip(cv2.GaussianBlur(lossm, (0, 0), 1.4) - lossm * 0.7, 0, 1)
    col = col * (1 - edge[..., None] * 0.45) + plast * edge[..., None] * 0.45
    return np.dstack([np.clip(col, 0, 255), np.clip(al, 0, 255)]).astype(np.uint8)


def _to_arr(fr):
    return fr.surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)


@functools.lru_cache(maxsize=8)
def sky_layer(width, h, seed=1, mode="day"):
    """Gökyüzü + uzak tepeler (opak), çatlak ve kenar kaybı ile."""
    rs = np.random.RandomState(seed)
    fr = Frame(width, h)
    c = fr.c
    if mode == "day":
        sky_gradient(c, width, h * 0.7)
        clouds(c, width, h * 0.7, rs)
    else:
        sky_gradient(c, width, h * 0.7, "#0C1840", "#1F3270", "#6B7FB8")
        for i in range(int(width / 14)):
            c.drawCircle(rs.uniform(0, width), rs.uniform(0, h * 0.40), rs.uniform(0.8, 2.0), skia.Paint(AntiAlias=True, Color=C("#FFF2C4", int(rs.uniform(90, 230)))))
    horizon = h * 0.46
    for k, (col, amp, sc, off) in enumerate((("#A9BDB6", 34, 560, 0.0), ("#93AFA5", 40, 380, 36), ("#7F9E92", 46, 260, 74))):
        if mode != "day":
            col = mix(col, "#14234A", 0.62)
        xs, ys = _ridge(rs, width, horizon + off, amp, sc)
        c.drawPath(_poly_from_ridge(xs, ys, h), skia.Paint(AntiAlias=True, Color=C(col)))
        c.drawPath(sk.poly_path([(float(x), float(y)) for x, y in zip(xs, ys)], False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C(mix(col, "#2A3A30", 0.5), 160)))
        if k == 1:
            for j in range(max(2, width // 900)):
                i = rs.randint(10, len(xs) - 10)
                castle(c, float(xs[i]), float(ys[i]) + 2, rs.uniform(30, 44), "#E9DEC0" if mode == "day" else "#6C7AA8", "#B5603A" if mode == "day" else "#3A3A6A")
    arr = _to_arr(fr)
    arr[..., 3] = 255
    out = _bake_texture(arr, rs, 0.45, 0.7)
    return sk.np_to_image(out)


@functools.lru_cache(maxsize=8)
def mid_layer(width, h, seed=2, mode="day"):
    """Orta plan (şeffaf üstü): terra verde tepeler, selvi/portakal/şemsiye çam, şato, patika, ön plan çimen+çiçek; çatlak + kenar kaybı."""
    rs = np.random.RandomState(seed)
    fr = Frame(width, h)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    night = mode != "day"
    top = h * 0.56
    xs, ys = _ridge(rs, width, top, 34, 440)
    gp = _poly_from_ridge(xs, ys, h)
    g1, g2 = ("#8FA469", "#6E8650") if not night else ("#2B3F3A", "#1C2B2A")
    sh = skia.GradientShader.MakeLinear([(0, top - 40), (0, h)], [C(g1), C(g2)], [0, 1])
    c.drawPath(gp, skia.Paint(AntiAlias=True, Shader=sh))
    c.drawPath(sk.poly_path([(float(x), float(y)) for x, y in zip(xs, ys)], False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C("#2E3E22", 190)))
    # patika
    path = skia.Path()
    px = width * 0.18
    path.moveTo(px, top + 20)
    for k in range(1, 9):
        path.quadTo(px + (60 if k % 2 else -60) * (1 + k * 0.2), top + k * (h - top) / 8 - 18, px + 20 * k, top + k * (h - top) / 8 + 6)
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, Color=C("#E0CF9E", 150 if not night else 40), StrokeCap=skia.Paint.kRound_Cap))
    # ağaçlar ve şato
    for i in range(int(width / 150)):
        x = rs.uniform(0, width)
        idx = int(clamp(x / 8, 0, len(xs) - 1))
        y = float(ys[idx]) + rs.uniform(4, 40)
        hh = rs.uniform(110, 190)
        r = rs.rand()
        if r < 0.45:
            cypress(c, x, y, hh, "#2E4A33" if not night else "#16241E", "#4F6E4A" if not night else "#2A4036")
        elif r < 0.70:
            umbrella_pine(c, x, y, hh * 0.9, "#3C5A38" if not night else "#1A2A22")
        else:
            orange_tree(c, x, y, hh * 0.8, rs)
    for j in range(max(1, width // 1700)):
        i = rs.randint(40, len(xs) - 40)
        castle(c, float(xs[i]), float(ys[i]) + 4, rs.uniform(70, 96), "#E6D9B8" if not night else "#6F7AA0", "#B4552E" if not night else "#3C3A66")
    # ön plan: çimen kümeleri ve çiçekler
    gy0 = h * 0.72
    c.drawRect(skia.Rect.MakeLTRB(0, gy0, width, h), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, gy0), (0, h)], [C("#7A8F52", 0), C("#566C3A", 235)], [0, 1])))
    for i in range(int(width / 6)):
        x = rs.uniform(0, width)
        y = rs.uniform(gy0 + 6, h)
        L = rs.uniform(8, 20)
        c.drawLine(x, y, x + rs.uniform(-4, 4), y - L, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=C("#2E4A22" if not night else "#16241A", int(rs.uniform(90, 200)))))
    cols = ["#F4EEDC", "#D8483A", "#E8B93A", "#F4EEDC", "#6E7FD0"]
    for i in range(int(width / 38)):
        x = rs.uniform(0, width)
        y = rs.uniform(gy0 + 14, h - 6)
        r = rs.uniform(2.4, 5.0)
        col = cols[rs.randint(len(cols))]
        c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=C(col)))
        c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#2A1A0C", 130)))
    arr = _to_arr(fr)
    out = _bake_texture(arr, rs, 0.5, 0.8)
    return sk.np_to_image(out)


# ───────────────────────────── alay (cast) ─────────────────────────────
ROBES = ["#A8321E", "#233C8C", "#2E7A5A", "#7A2E56", "#C79A3C", "#1F5A7A", "#D9CFAF", "#8A3A1E"]
HATS = ["mazzocchio", "mazzocchio", "flatcap", "beret", "scholar", "biretta", "coif", "tall", "woolcap"]
COATS = ["#F0E8D4", "#8A5A38", "#3A2A20", "#C8A878", "#B8B0A0", "#6A4A30"]
HOSES = ["#233C8C", "#A8321E", "#2E7A5A", "#7A2E56", "#D9CFAF"]
HAIRS = ["#5A3A22", "#2A1A10", "#B8862A", "#8A8A82", "#7A4A24"]
PATS = ["diamond", "fleur", "dots", "quatrefoil", "stripe", "pomegranate"]


def make_cast(seed, travel, n_front=5, n_mid=5, n_far=5, width=None):
    """Alay listesi: [dict(kind, spec, h, x, y, phase, depth)] — x çizim-uzayı (şerit); y = ayak hizası (bant içi)."""
    import cilt_figs as FG
    rs = np.random.RandomState(seed)
    width = width or (1920 + travel)
    cast = []

    def pick(lst):
        return lst[rs.randint(len(lst))]

    def rider(h, y, x, depth):
        r1, r2 = pick(ROBES), pick(ROBES)
        sp_ = FG.spec(coat=pick(COATS), mane=pick(["#6B5A44", "#2A1A10", "#9A8A70"]), cloth=pick(ROBES), robe=r1, robe2="#E0B84E", hat=pick(HATS), hat_col=pick(ROBES), hose=pick(HOSES),
                      hair=pick(HAIRS), pat=(pick(PATS), "#E0B84E"), cl_pat=(pick(PATS), "#E8E0C0"), pose="walk" if rs.rand() < 0.8 else "stand", beard=pick([None, None, "short", "stache"]))
        cast.append(dict(kind="rider", spec=sp_, h=h, x=x, y=y, phase=rs.uniform(0, 6.28), depth=depth))

    def walker(h, y, x, depth, kind=None):
        k = kind or pick(["page", "noble", "noble", "page", "elder"])
        sp_ = FG.spec(kind=k, robe=pick(ROBES), robe2="#E0B84E", hat=pick(HATS), hat_col=pick(ROBES), hair=pick(HAIRS), hose_l=pick(HOSES), hose_r=pick(HOSES),
                      pat=(pick(PATS), "#E0B84E"), beard="full" if k == "elder" else None, stride=rs.uniform(0.7, 1.1))
        cast.append(dict(kind="walker", spec=sp_, h=h, x=x, y=y, phase=rs.uniform(0, 6.28), depth=depth))
    # satır satır: uzak (küçük, tepede) → orta → ön; her satır şerit genişliğini doldurur
    x = rs.uniform(60, 260)
    while x < width + 100:
        if rs.rand() < 0.5:
            rider(rs.uniform(215, 255), rs.uniform(436, 452), x, 0)
        else:
            walker(rs.uniform(185, 215), rs.uniform(436, 452), x, 0)
        x += rs.uniform(260, 520)
    x = rs.uniform(0, 300)
    while x < width + 100:
        if rs.rand() < 0.5:
            rider(rs.uniform(305, 345), rs.uniform(534, 552), x, 1)
        else:
            walker(rs.uniform(270, 310), rs.uniform(534, 552), x, 1)
        x += rs.uniform(380, 700)
    x = rs.uniform(0, 400)
    while x < width + 100:
        if rs.rand() < 0.62:
            rider(rs.uniform(430, 480), rs.uniform(640, 660), x, 2)
        else:
            walker(rs.uniform(380, 420), rs.uniform(640, 660), x, 2)
        x += rs.uniform(560, 900)
    cast.sort(key=lambda d: (d["depth"], d["y"]))
    return cast
