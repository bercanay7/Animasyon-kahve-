"""Bölüm 3 (Şehirlerin İsyanı) dioramaları: c3_sokak (meşaleli isyan sokağı), c3_toledo (kuşatılmış Toledo).
scenes_lib/stage API'si ile; ortak dosyalara dokunmaz."""
import math

import numpy as np
import skia

import kit_a as K
import scenes_lib as SL
import sk
import stage as ST
from sk import H, W, lerp, mix
from stage import MARGIN

RIM = "#D98A44"


def _wall(f, side, rs):
    """Perspektifli sokak duvarı: yakın kenardan uzağa daralan çokgen + pencereler + sıva izleri."""
    xn = -300 if side < 0 else W + 300
    xf = 540 if side < 0 else W - 540
    top_n, bot_n, top_f, bot_f = 20, 1040, 330, 700
    poly = [(xn, top_n), (xf, top_f), (xf, bot_f), (xn, bot_n)]
    f.path(sk.poly_path(poly), shader=f.lin(xn, 0, xf, 0, [("#1A0B09", 0.0), ("#3E1C12", 1.0)]))
    # katlar (yatay çizgiler)
    for r in (0.30, 0.62):
        f.path(sk.poly_path([(xn, lerp(top_n, bot_n, r)), (xf, lerp(top_f, bot_f, r))], False), style="stroke", sw=3, color="#0A0403", alpha=0.55)
    for u in np.linspace(0.07, 0.93, 8):
        x = lerp(xn, xf, u)
        yt, yb = lerp(top_n, top_f, u), lerp(bot_n, bot_f, u)
        h = yb - yt
        s = 1 - u * 0.58
        for yy in (0.17, 0.46, 0.78):
            lit = rs.rand() > 0.38
            ww, wh = 78 * s, 128 * s
            wy = yt + h * yy
            if lit:
                f.rect(x - ww / 2 - 10, wy - wh / 2 - 10, ww + 20, wh + 20, color="#FF9A40", alpha=0.16, blur=14)
                f.rect(x - ww / 2, wy - wh / 2, ww, wh, shader=f.lin(0, wy - wh / 2, 0, wy + wh / 2, [("#FFD58A", 0.0), ("#E0802E", 1.0)]))
                f.line(x, wy - wh / 2, x, wy + wh / 2, color="#2A130C", sw=3 * s)
                f.line(x - ww / 2, wy, x + ww / 2, wy, color="#2A130C", sw=3 * s)
            else:
                f.rect(x - ww / 2, wy - wh / 2, ww, wh, color="#120807")
            f.rect(x - ww / 2 - 6, wy - wh / 2 - 8, ww + 12, 8, color="#2A130C")
    # çatı kenarı
    f.path(sk.poly_path([(xn, top_n), (xf, top_f)], False), style="stroke", sw=8, color="#0A0403")


@SL.sc("c3_sokak")
class Sokak:
    """Gece, Kastilya şehri sokağı: kızıl gökyüzü, iki yanda pencereleri yanan evler, meşaleli/sancaklı kalabalık."""

    def __init__(self, p):
        self.p = p
        rs = np.random.RandomState(11)
        # kalabalık (x, ayak_y, boy, yüz, tür, meşale?)
        self.crowd = []
        kinds = ["crowd_a", "crowd_b", "crowd_c", "crowd_d", "crowd_e", "crowd_f", "peasant", "woman", "merchant", "peasant", "child"]
        for row, (y, h, n, x0, x1) in enumerate([(718, 120, 16, 600, 1320), (800, 190, 15, 380, 1540), (910, 290, 13, 120, 1800), (1040, 420, 8, -60, 1980)]):
            for k in range(n):
                x = x0 + (k + rs.rand() * 0.7) * (x1 - x0) / n
                kind = kinds[rs.randint(len(kinds))] if (row == 3 and k % 3) is not None else kinds[rs.randint(len(kinds))]
                torch = rs.rand() < (0.34 if row >= 1 else 0.2)
                self.crowd.append(dict(x=x, y=y + rs.randn() * 5, h=h * (0.92 + 0.16 * rs.rand()), face=1 if rs.rand() > 0.5 else -1, kind=kind, torch=torch, ph=rs.rand() * 6, row=row))
        self.banners = [(520, 700, "#8E1F26"), (790, 660, "#7B1B22"), (1170, 660, "#8E1F26"), (1420, 700, "#6B1D24"), (300, 820, "#7B1B22"), (1650, 820, "#8E1F26")]

    def layers(self):
        rs = np.random.RandomState(5)

        def L0(f):
            ST.sky_gradient(f, "#12080A", "#5C2018", y1=660)
            f.circle(960, 600, 800, shader=f.rad(960, 600, 800, [("#FF7A3C", 0.0, 135), ("#A8381E", 0.45, 60), ("#A8381E", 1.0, 0)]), blend=skia.BlendMode.kPlus)
            for i in range(10):
                f.oval(rs.rand() * W, 70 + rs.rand() * 280, 260 + rs.rand() * 200, 36 + rs.rand() * 30, color="#1A0C0E", alpha=0.55, blur=26)
            ST.skyline(f, 660, ["tower", "spire", "dome", "house", "spire"], -200, W + 200, 190, "#230D0C", seed=4, win="#FFB060", gap=(40, 110))
            f.rect(-MARGIN, 660, W + 2 * MARGIN, 700, color="#1A0A0A")

        def L1(f):                       # sokağın sonundaki meydan: katedral kulesi + parıltı
            f.circle(960, 600, 330, shader=f.rad(960, 600, 330, [("#FFC070", 0.0, 150), ("#FF8A3A", 0.5, 60), ("#FF8A3A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
            ST.skyline(f, 700, ["spire", "tower", "dome"], 640, 1280, 250, "#2A100C", seed=9, win="#FFC070", gap=(20, 60))
            f.rect(640, 690, 640, 40, color="#2A100C")

        def L2(f):                       # sokak duvarları
            _wall(f, -1, rs)
            _wall(f, 1, rs)

        def L3(f):                       # taş zemin
            f.path(sk.poly_path([(-MARGIN, 1100 + MARGIN), (-300, 1040), (540, 700), (W - 540, 700), (W + 300, 1040), (W + MARGIN, 1100 + MARGIN)]),
                   shader=f.lin(0, 700, 0, 1080, [("#2A140E", 0.0), ("#4C2C1A", 1.0)]))
            for i in range(-11, 12):
                f.line(960 + i * 38, 700, 960 + i * 250, 1120, color="#0A0403", sw=2.2, alpha=0.4)
            for j in range(10):
                yy = 700 + (380) * (j / 9) ** 1.7
                f.line(0, yy, W, yy, color="#0A0403", sw=1.5 + j * 0.3, alpha=0.32)
            f.oval(960, 860, 760, 190, shader=f.rad(960, 860, 760, [("#FF9A40", 0.0, 90), ("#FF9A40", 1.0, 0)]), blend=skia.BlendMode.kPlus)

        def L4(f):                       # ön plan siluetleri (kenarlarda kırpılmış)
            ST.figure(f, "crowd_a", 90, 1190, 760, col="#060303", rim=RIM, face=1)
            ST.figure(f, "peasant", 1850, 1200, 800, col="#060303", rim=RIM, face=-1)
            f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, 90, color="#0A0403", alpha=0.7)

        # derinlikler: 0.05 gök, 0.3 meydan, 0.7 duvar, 0.9 zemin; kalabalık (dyn) 0.9 katmanında; ön plan 1.35
        return [(0.05, L0), (0.3, L1), (0.7, L2), (0.9, L3), (1.35, L4)]

    def dyn(self):
        crowd, banners = self.crowd, self.banners

        def D3(f, t):
            for c in sorted(crowd, key=lambda q: q["y"]):
                bob = abs(math.sin(t * 2.2 + c["ph"])) * -c["h"] * 0.012
                ST.figure(f, c["kind"], c["x"], c["y"], c["h"], col="#0A0504", rim=RIM, face=c["face"], bob=bob, sway=math.sin(t * 1.3 + c["ph"]) * 0.01)
                if c["torch"]:
                    hx = c["x"] + c["face"] * c["h"] * 0.20
                    hy = c["y"] - c["h"] * 0.60 + bob
                    top = hy - c["h"] * 0.30
                    f.line(hx, hy, hx + c["face"] * c["h"] * 0.03, top, color="#1A0C06", sw=max(2.0, c["h"] * 0.022))
                    K.flame(f, hx + c["face"] * c["h"] * 0.03, top, c["h"] * 0.17, t, lit=1.0, seed=c["ph"])
            for (x, y, col) in banners:
                f.line(x, y, x, y - 330, color="#150B07", sw=7)
                ST.banner(f, x + 6, y - 322, 110, 170, color=col, trim="#C9962B", icon="castle", wave=math.sin(t * 2.6 + x * 0.01) * 6)
            sk.embers(f, t, n=30, rect=(0, 120, W, 720))

        return {3: D3}


# ───────────────────────────── Toledo kuşatması ─────────────────────────────
@SL.sc("c3_toledo")
class Toledo:
    """Tepedeki Toledo: Alcázar + katedral kulesi; duman, yangın ışıltıları, top parlamaları; önde kuşatma ateşleri."""

    def __init__(self, p):
        self.p = p

    @staticmethod
    def hill_poly():
        return [(-300, 900), (120, 760), (420, 640), (700, 500), (880, 360), (1000, 262), (1260, 262), (1420, 380), (1650, 540), (1950, 700), (2300, 860), (2300, 1200), (-300, 1200)]

    def layers(self):
        rs = np.random.RandomState(23)
        hill = self.hill_poly()

        def L0(f):
            ST.sky_gradient(f, "#1A1214", "#6A3A2A", y1=720)
            f.circle(1100, 560, 900, shader=f.rad(1100, 560, 900, [("#FF7A3C", 0.0, 70), ("#A8381E", 0.5, 35), ("#A8381E", 1.0, 0)]), blend=skia.BlendMode.kPlus)
            for i in range(11):
                f.oval(rs.rand() * W, 60 + rs.rand() * 330, 240 + rs.rand() * 220, 34 + rs.rand() * 34, color="#241416", alpha=0.6, blur=28)
            ST.hills(f, 650, 60, "#2A1A1C", seed=2, step=70, wavelength=0.003)
            ST.hills(f, 720, 44, "#201416", seed=5, step=70, wavelength=0.005)

        def L1(f):                       # nehir (Tajo): kıvrımlı koyu şerit + parıltılar
            pts = [(-300, 930), (300, 880), (800, 900), (1300, 860), (1800, 905), (2300, 880)]
            band = sk.smooth_path(pts + [(2300, 1200), (-300, 1200)], True, 0.4)
            f.path(band, shader=f.lin(0, 850, 0, 1100, [("#2A3A44", 0.0), ("#0E161C", 1.0)]))
            f.path(sk.smooth_path(pts, False, 0.4), style="stroke", sw=3, color="#9FB8C8", alpha=0.35)
            for i in range(30):
                x = rs.rand() * W
                f.line(x, 905 + rs.rand() * 120, x + 40 + rs.rand() * 70, 905 + rs.rand() * 120, color="#C8DCE8", sw=1.6, alpha=0.2)

        def L2(f):                       # tepe + ev kümeleri + surlar + Alcázar + katedral
            p = sk.poly_path(hill, True)
            f.path(p, shader=f.lin(0, 262, 0, 900, [("#1C100E", 0.0), ("#0F0807", 1.0)]))
            f.c.save()
            f.c.clipPath(p, skia.ClipOp.kIntersect, True)
            for k in range(190):
                x = -100 + rs.rand() * (W + 200)
                ytop = np.interp(x, [h[0] for h in hill[:-3]], [h[1] for h in hill[:-3]])
                y = ytop + 30 + rs.rand() * (880 - ytop - 30)
                w = 24 + rs.rand() * 46 * (0.6 + (y - 262) / 700)
                h = 22 + rs.rand() * 40 * (0.6 + (y - 262) / 700)
                col = mix("#1E100D", "#3A1E14", rs.rand())
                f.rect(x, y - h, w, h, color=col)
                f.poly([(x - 4, y - h), (x + w / 2, y - h - 14 - rs.rand() * 10), (x + w + 4, y - h)], color=mix(col, "#000000", 0.35))
                if rs.rand() < 0.16:
                    f.rect(x + w * 0.35, y - h * 0.6, w * 0.2, h * 0.28, color="#FFB04A", alpha=0.9)
            f.c.restore()
            f.path(p, style="stroke", sw=3, color="#C58A44", alpha=0.35)
            # sur
            for i in range(0, 26):
                x = 140 + i * 72
                ytop = np.interp(x, [h[0] for h in hill[:-3]], [h[1] for h in hill[:-3]]) + 70
                if 800 < x < 1450:
                    continue
                f.rect(x, ytop, 60, 18, color="#160B09")
            # Alcázar
            ax, ay = 1130, 262
            f.rect(ax - 190, ay - 100, 380, 120, shader=f.lin(0, ay - 100, 0, ay + 20, [("#3A2018", 0.0), ("#1E100C", 1.0)]))
            for sx in (-1, 1):
                f.rect(ax + sx * 190 - 34, ay - 175, 68, 195, color="#2A1710")
                for q in range(4):
                    f.rect(ax + sx * 190 - 34 + q * 19, ay - 190, 12, 18, color="#2A1710")
                f.poly([(ax + sx * 190 - 40, ay - 175), (ax + sx * 190, ay - 235), (ax + sx * 190 + 40, ay - 175)], color="#160B09")
            for q in range(14):
                f.rect(ax - 190 + q * 28, ay - 116, 18, 18, color="#2A1710")
            for q in range(6):
                f.rect(ax - 140 + q * 55, ay - 60, 16, 30, color="#FFB04A", alpha=0.85)
            # katedral kulesi
            cx_ = 830
            f.rect(cx_ - 30, 150, 60, 250, color="#24120E")
            f.poly([(cx_ - 38, 150), (cx_, 30), (cx_ + 38, 150)], color="#180C09")
            f.rect(cx_ - 4, 8, 8, 40, color="#180C09")
            f.rect(cx_ - 14, 20, 28, 7, color="#180C09")
            for q in range(4):
                f.rect(cx_ - 8, 190 + q * 50, 16, 26, color="#FF9A3A", alpha=0.7)

        def L3(f):                       # önde kuşatma kampı: çadırlar + şarapnel çitleri
            for (x, y, s) in ((120, 1010, 1.4), (420, 1050, 1.1), (1480, 1030, 1.3), (1780, 1060, 1.6)):
                f.poly([(x - 100 * s, y), (x, y - 120 * s), (x + 100 * s, y)], color="#0B0605")
                f.line(x, y - 120 * s, x, y - 150 * s, color="#0B0605", sw=4)
            for i in range(12):
                x = 60 + i * 160
                f.line(x, 1040, x, 1000, color="#0B0605", sw=5)
            f.rect(-MARGIN, 1030, W + 2 * MARGIN, 120, color="#070403")

        return [(0.1, L0), (0.35, L1), (0.7, L2), (1.1, L3)]

    def dyn(self):
        def D2(f, t):
            # duman sütunları + yangın ışığı (tepenin farklı yerlerinden)
            for (x, y, w, h, sd) in ((620, 520, 240, 520, 1), (1050, 420, 300, 600, 2), (1480, 520, 240, 520, 3), (880, 560, 200, 420, 4)):
                f.circle(x, y + 20, 70, shader=f.rad(x, y + 20, 70, [("#FF6A2A", 0.0, int(120 + 40 * math.sin(t * 5 + sd))), ("#FF6A2A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
                K.puffs(f, x, y, t + sd * 3, w=w, h=h, n=7, seed=sd + 40, color="#241A18", alpha=0.5)
            sk.embers(f, t, n=40, rect=(300, 200, 1500, 600))

        def D3(f, t):
            # kuşatma ateşleri + top parlamaları
            for k, (x, y) in enumerate(((260, 1000), (700, 1030), (1300, 1020), (1640, 1005))):
                K.flame(f, x, y, 46, t, lit=1.0, seed=k * 2.1)
            for k, (x, y) in enumerate(((300, 930), (1560, 940))):
                ph = (t * 0.55 + k * 0.47) % 1.0
                if ph < 0.1:
                    a = 1 - ph / 0.1
                    f.circle(x, y, 130, shader=f.rad(x, y, 130, [("#FFF0C0", 0.0, int(230 * a)), ("#FF9A3A", 0.4, int(110 * a)), ("#FF9A3A", 1.0, 0)]), blend=skia.BlendMode.kPlus)

        return {2: D2, 3: D3}
