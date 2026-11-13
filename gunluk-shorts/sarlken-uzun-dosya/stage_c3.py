"""Bölüm 3 (Şehirlerin İsyanı) dioramaları: c3_sokak (meşaleli isyan sokağı). Toledo kuşatması sahne-lab'ın `siege` sahnesinden gelir.
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
            K.fig(f, "crowd_a", 90, 1190, 760, col="#060303", rim=RIM, face=1)
            K.fig(f, "peasant", 1850, 1200, 800, col="#060303", rim=RIM, face=-1)
            f.rect(-MARGIN, -MARGIN, W + 2 * MARGIN, 90, color="#0A0403", alpha=0.7)

        # derinlikler: 0.05 gök, 0.3 meydan, 0.7 duvar, 0.9 zemin; kalabalık (dyn) 0.9 katmanında; ön plan 1.35
        return [(0.05, L0), (0.3, L1), (0.7, L2), (0.9, L3), (1.35, L4)]

    def dyn(self):
        crowd, banners = self.crowd, self.banners

        def D3(f, t):
            for c in sorted(crowd, key=lambda q: q["y"]):
                bob = abs(math.sin(t * 2.2 + c["ph"])) * -c["h"] * 0.012
                K.fig(f, c["kind"], c["x"], c["y"], c["h"], col="#0A0504", rim=RIM, face=c["face"], bob=bob, sway=math.sin(t * 1.3 + c["ph"]) * 0.01)
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
