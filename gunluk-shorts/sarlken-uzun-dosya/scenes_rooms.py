"""ODA LABORATUVARI sahneleri: tower, counting_house, electors_hall, aachen, reichstag, road_night, cloister, bedroom, chapel,
ransom_room, debate_hall. Her sahne: layers() (bir kez pişer; numpy ile ışıklandırılmış perspektif oda + skia dekor) ve dyn() (küçük hareketler).
Kayıt: `import scenes_lib as SL` → `@SL.sc("ad")`. Ayrıntılar: SAHNE_KATALOGU_odalar.md
"""
import math

import numpy as np
import skia

import scenes_lib as SL
import sk
import stage as ST
import stage_rooms as R
from sk import C, H, W, clamp, mix, smooth
from stage import MARGIN

M = MARGIN
RF = R.rfigure


def _lights_xy(items):
    """[(x,y,r,col,a)] → lit_path ışık listesi"""
    return items


def _shadow_ellipse(f, x, y, rx, ry, a=0.55, blur=14):
    f.c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), skia.Paint(AntiAlias=True, Color=C("#000000", int(255 * a)),
                                                                              MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)))


def _stool(f, x, y, w=120, h=96, lights=(), col="#3a2616"):
    top = R.rrect_path(x - w / 2, y - h, w, 16, 4)
    R.lit_path(f, top, shade(col, 0.05), lights, rim="#b88a52", rim_w=1.2)
    for sx in (-1, 1):
        leg = R.rect_path(x + sx * w * 0.38 - 6, y - h + 14, 12, h - 14)
        R.lit_path(f, leg, shade(col, -0.2), lights)


def shade(c, k):
    return R.shade(c, k)


def _table(f, x, y, w=300, top_y=0, h=18, leg_h=150, lights=(), col="#3a2616", front=True):
    """Basit masa (önden). y: ayakların zemin hizası, top_y: tabla üstü."""
    top_y = top_y or (y - leg_h)
    top = R.rrect_path(x - w / 2, top_y, w, h, 3)
    R.lit_path(f, top, shade(col, 0.1), lights, rim="#d6a15a", rim_w=1.4, grad=f.lin(0, top_y, 0, top_y + h, [(shade(col, 0.22), 0.0), (shade(col, -0.2), 1.0)]))
    apron = R.rect_path(x - w / 2 + 14, top_y + h, w - 28, 22)
    R.lit_path(f, apron, shade(col, -0.3), lights)
    for sx in (-1, 1):
        leg = R.rect_path(x + sx * (w / 2 - 28) - 9, top_y + h, 18, y - top_y - h)
        R.lit_path(f, leg, shade(col, -0.28), lights)


def _jug(f, x, y, s=1.0, col="#6b4a2e", lights=()):
    p = skia.Path()
    p.moveTo(x - 14 * s, y)
    p.cubicTo(x - 24 * s, y - 14 * s, x - 22 * s, y - 40 * s, x - 10 * s, y - 52 * s)
    p.lineTo(x - 11 * s, y - 62 * s)
    p.lineTo(x + 11 * s, y - 62 * s)
    p.lineTo(x + 10 * s, y - 52 * s)
    p.cubicTo(x + 22 * s, y - 40 * s, x + 24 * s, y - 14 * s, x + 14 * s, y)
    p.close()
    R.lit_path(f, p, shade(col, -0.35), lights, rim="#e0b06a", rim_w=1.2)
    h = skia.Path()
    h.moveTo(x + 18 * s, y - 46 * s)
    h.cubicTo(x + 36 * s, y - 46 * s, x + 36 * s, y - 20 * s, x + 20 * s, y - 18 * s)
    f.path(h, style="stroke", sw=5 * s, color=shade(col, -0.45))


def _book(f, x, y, w=70, h=14, col="#5a2a1c", lights=(), ang=0.0, trim="#c9962b"):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(ang))
    p = R.rrect_path(-w / 2, -h, w, h, 2)
    R.lit_path(f, p, col, lights, rim="#e0b06a", rim_w=1.0)
    f.rect(-w / 2 + 3, -h + 3, w - 6, 1.6, color=trim, alpha=0.55)
    f.rect(-w / 2 + 3, -4, w - 6, 1.4, color=trim, alpha=0.4)
    f.rect(-w / 2 + w - 5, -h + 2, 4, h - 4, color="#d8ccaa", alpha=0.8)
    f.c.restore()


# ═══════════════════════════════════════════════════════════════════════
#  TOWER — Tordesillas / Madrid hücresi / Wartburg
# ═══════════════════════════════════════════════════════════════════════
_TOWER = {
    "tordesillas": dict(back=(300, 30, 1620, 900), vp=(990, 520), win=(905, 140, 1075, 400), T=130, splay=0.8, bars=3, hbars=1, bar_w=8,
                        wall="#4d4036", wall_seed=3, floor="flags", D=(-0.25, 0.9, -0.36), candle=(1292, 706), candle_z=960, figure="woman",
                        fig_xy=(776, 944, 430), moon_p=1.7, ambient=(0.006, 0.008, 0.016)),
    "cell": dict(back=(380, 60, 1540, 880), vp=(960, 500), win=(990, 120, 1150, 350), T=190, splay=0.74, bars=3, hbars=2, bar_w=9,
                 wall="#463d36", wall_seed=8, floor="flags", D=(0.30, 0.85, -0.42), candle=(1230, 726), candle_z=980, figure="man",
                 fig_xy=(906, 944, 590), moon_p=1.4, ambient=(0.006, 0.008, 0.015)),
    "wartburg": dict(back=(300, 20, 1620, 900), vp=(990, 520), win=(1010, 170, 1230, 440), T=120, splay=0.86, bars=0, hbars=0, bar_w=6,
                     wall="#4a3322", wall_seed=5, floor="planks", D=(-0.30, 0.86, -0.40), candle=(1182, 646), candle_z=940, figure="writer",
                     fig_xy=(930, 944, 420), moon_p=1.1, ambient=(0.007, 0.007, 0.014)),
}


@SL.sc("tower")
class Tower:
    """Dar taş kule odası. p: variant="tordesillas|cell|wartburg", night=True, figure="woman|man|writer|none" (varsayılan varyanta göre),
    candle=0..1.4 (alev boyutu; 0=yok), moon=1.0 (ay ışığı çarpanı)."""

    def __init__(self, p):
        self.p = p
        self.v = p.get("variant", "tordesillas")
        self.c = _TOWER.get(self.v, _TOWER["tordesillas"])
        self.night = p.get("night", True)
        self.fig = p.get("figure", self.c["figure"])
        self.candle = float(p.get("candle", 1.0))
        self.moonk = float(p.get("moon", 1.0))

    # -- yardımcılar
    def _box(self):
        c = self.c
        return R.Box(c["back"], vp=c["vp"], zb=1100.0, F=1100.0)

    def _outer(self, box):
        c = self.c
        return box.hole_outer(c["win"], c["T"], c["splay"])

    def _bars_x(self, outer):
        n = self.c["bars"]
        x0, y0, x1, y1 = outer
        return [x0 + (x1 - x0) * (i + 1) / (n + 1) for i in range(n)]

    def _bars_y(self, outer):
        n = self.c["hbars"]
        x0, y0, x1, y1 = outer
        return [y0 + (y1 - y0) * (i + 1) / (n + 1) for i in range(n)]

    def layers(self):
        p, c, v = self.p, self.c, self.v
        night = self.night
        box = self._box()
        outer = self._outer(box)
        zw = box.zb + c["T"]
        bxs, bys = self._bars_x(outer), self._bars_y(outer)
        D = c["D"]
        candle_on = self.candle > 0.01
        cx_, cy_ = c["candle"]
        cache = {}

        def room():
            if "room" in cache:
                return cache["room"]
            wall = R.mat_ashlar(c["wall"], seed=c["wall_seed"], bw=230, bh=100, stain=0.28, moss=0.06, tone=0.22)
            if v == "wartburg":
                wall = R.mat_planks("#3d2817", seed=4, pw=140, plen=5000, tone=0.14)
                side = R.mat_planks("#36231a", seed=6, pw=140, plen=5000, tone=0.14)
            else:
                side = R.mat_ashlar(c["wall"], seed=c["wall_seed"] + 2, bw=230, bh=100, stain=0.28, moss=0.05, tone=0.22)
            floor = R.mat_flags("#463d36", seed=5, size=190) if c["floor"] == "flags" else R.mat_planks("#4a3422", seed=2, pw=96, plen=620)
            ceil = R.mat_beams("#2b1d12", seed=7, pitch=250, bwid=70, plaster="#241a12", axis="a")
            mats = dict(back=wall, left=side, right=side, floor=floor, ceil=ceil)
            lights = []
            if candle_on:
                lights.append(R.Light((cx_, cy_ - 8, c["candle_z"]), R.warm(1.0), 2.4 * min(1.2, self.candle + 0.2), 230, spec=0.5, far=(520, (0.55, 0.20, 0.05), 0.10)))
            amb = c["ambient"] if night else (0.09, 0.10, 0.12)
            ox0, oy0, ox1, oy1 = outer
            if night:      # pencere çevresine soğuk yansıma
                lights.append(R.Light(((ox0 + ox1) / 2, (oy0 + oy1) / 2 + 40, zw - 90), (0.30, 0.42, 0.78), 0.9 * self.moonk, 330))
            moon = None
            if self.moonk > 0:
                gobo = R.window_gobo(box, outer, zw, xs=bxs, bar_w=c["bar_w"], ys=bys, bar_hw=c["bar_w"])
                moon = R.Moon(D, col=(0.42, 0.58, 1.0) if night else (0.8, 0.82, 0.86), power=c["moon_p"] * self.moonk * (1.0 if night else 0.8), win=gobo, pen=3.5, pen_k=0.010)
            rgb, cov = box.render(mats, lights, moon=moon, ambient=amb, expo=1.25, ao=0.55,
                                  holes=[dict(rect=c["win"], T=c["T"], splay=c["splay"], mat=side, ao=0.25)])
            cache["room"] = (rgb, cov)
            return cache["room"]

        def L0(f):          # dışarısı (pencereden görünen gökyüzü/manzara)
            if night:
                moon_xy = {"tordesillas": (1010, 236, 26), "cell": (1105, 232, 20), "wartburg": (1190, 262, 24)}[v]
                R.night_sky(f, moon=moon_xy, y_h=520, stars=90, seed=11)
                if v == "tordesillas":      # Duero ovası, uzakta kasaba/kilise siluetleri
                    ST.hills(f, 372, 14, "#070b14", seed=3, wavelength=0.006)
                    f.rect(-M, 380, W + 2 * M, 400, color="#05080f")
                    for i, (x, hh) in enumerate(((880, 46), (1120, 62), (1190, 38))):
                        f.rect(x - 10, 372 - hh, 20, hh, color="#05080f")
                        f.poly([(x - 14, 372 - hh), (x, 372 - hh - 22), (x + 14, 372 - hh)], color="#05080f")
                    for (x, y) in ((905, 382), (944, 380), (1160, 384), (1005, 378)):
                        f.circle(x, y, 1.6, color="#ffcf80", alpha=0.85)
                elif v == "cell":
                    f.rect(-M, 360, W + 2 * M, 500, color="#04070d")
                    for (x, hh, ww) in ((860, 34, 60), (940, 54, 50), (1000, 28, 70), (1070, 66, 44), (1150, 36, 70), (1230, 48, 50)):
                        f.rect(x, 372 - hh, ww, hh + 20, color="#05080f")
                        f.poly([(x - 4, 372 - hh), (x + ww / 2, 372 - hh - 14), (x + ww + 4, 372 - hh)], color="#05080f")
                    f.rect(1062, 262, 18, 120, color="#05080f")
                    f.poly([(1058, 262), (1071, 228), (1084, 262)], color="#05080f")
                    for (x, y) in ((880, 360), (962, 352), (1092, 348), (1170, 358)):
                        f.rect(x, y, 3, 5, color="#ffcf80", alpha=0.8)
                else:                       # Wartburg: ormanlı tepeler
                    ST.hills(f, 400, 22, "#060a12", seed=6, wavelength=0.005)
                    ST.hills(f, 440, 16, "#04070d", seed=9, wavelength=0.007)
                    ST.pines(f, 820, 1350, 450, 90, "#03050a", seed=4, dens=28)
                    for (x, y) in ((900, 470), (960, 478), (1040, 472)):
                        f.circle(x, y, 1.8, color="#ffcf80", alpha=0.7)
            else:
                f.rect(-M, -M, W + 2 * M, H + 2 * M, shader=f.lin(0, -M, 0, 600, [("#5a6674", 0.0), ("#a3adb8", 0.7), ("#c9ccc8", 1.0)]))
                ST.hills(f, 410, 18, "#59606a", seed=3, wavelength=0.006)
                ST.hills(f, 450, 14, "#444a52", seed=6, wavelength=0.007)

        def L1(f):          # oda kutusu + demir parmaklık
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # köşelerde karanlık sızıntı + hafif doku
            x0, y0, x1, y1 = outer
            if c["bars"] or c["hbars"]:
                for bx in bxs:
                    R.bar_rod(f, bx, y0 - 2, bx, y1 + 2, w=c["bar_w"], col="#0b0a0a", hl="#7f9bd0" if night else "#a8a8a8", hl_a=0.7, light=-1)
                for by in bys:
                    R.bar_rod(f, x0 - 2, by, x1 + 2, by, w=c["bar_w"] * 0.9, col="#0b0a0a", hl="#7f9bd0" if night else "#a8a8a8", hl_a=0.6, light=-1)
                f.rect(x0 - 5, y0 - 6, x1 - x0 + 10, 7, color="#0d0b0a")
                f.rect(x0 - 5, y1 - 1, x1 - x0 + 10, 7, color="#0d0b0a")
            if v == "wartburg":          # kurşun çerçeveli baklava pencere
                for u in range(-12, 13):
                    for (a0, a1) in (((x0, y0 + u * 26), (x1, y0 + u * 26 + (x1 - x0))), ((x0, y0 + u * 26 + (x1 - x0)), (x1, y0 + u * 26))):
                        f.c.save()
                        f.c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
                        f.line(a0[0], a0[1], a1[0], a1[1], color="#0c0a09", sw=3.0, alpha=0.9)
                        f.c.restore()
                f.rect(x0 - 5, y0 - 6, x1 - x0 + 10, 8, color="#1a120b")
                f.rect(x0 - 5, y1 - 2, x1 - x0 + 10, 8, color="#1a120b")
                f.rect(x0 - 5, y0 - 6, 8, y1 - y0 + 12, color="#1a120b")
                f.rect(x1 - 3, y0 - 6, 8, y1 - y0 + 12, color="#1a120b")
                f.line((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, color="#14100b", sw=7)
                f.line(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, color="#14100b", sw=7)
                if candle_on:       # cama yansıyan mum
                    R.glow(f, cx_ - 40, (y0 + y1) / 2 + 20, 90, "#ffb45a", 0.10)

        def L2(f):          # eşyalar + ışık huzmesi
            lights = []
            if candle_on:
                lights.append((cx_, cy_ + 10, 330, "#ff9c40", 0.55))
            fy = c["fig_xy"][1]
            if v == "tordesillas":
                self._props_tordesillas(f, lights)
            elif v == "cell":
                self._props_cell(f, lights)
            else:
                self._props_wartburg(f, lights)
            # ay ışığı huzmesi (hacimsel)
            if self.moonk > 0:
                polys = R.shaft_polys(box, outer, zw, D, bxs, c["bar_w"])
                mid_top = ((outer[0] + outer[2]) / 2, (outer[1] + outer[3]) / 2)
                for q in polys:
                    sh = skia.GradientShader.MakeLinear([mid_top, (mid_top[0] + D[0] * 520, mid_top[1] + 520 * 0.9)],
                                                        [C("#9fb8ec", int(255 * 0.30 * self.moonk)), C("#9fb8ec", int(255 * 0.12 * self.moonk)), C("#9fb8ec", 0)], [0.0, 0.55, 1.0]) if night else \
                        skia.GradientShader.MakeLinear([mid_top, (mid_top[0] + D[0] * 520, mid_top[1] + 520 * 0.9)], [C("#e8e8e0", 70), C("#e8e8e0", 28), C("#e8e8e0", 0)], [0.0, 0.55, 1.0])
                    pa = skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kPlus)
                    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
                    f.c.drawPath(sk.poly_path(q, True), pa)
            if candle_on:
                R.glow(f, cx_, cy_ - 4, 260, "#ff9c40", 0.14)

        def L3(f):          # ön plan: koyu çerçeve
            if v == "tordesillas":
                post = R.rect_path(-M - 40, -M, 170, H + 2 * M)
                R.lit_path(f, post, "#0b0705", [(cx_, cy_, 900, "#ff9c40", 0.08)])
                f.rect(120, -M, 18, H + 2 * M, shader=f.lin(120, 0, 138, 0, [("#3a2616", 0.0, 120), ("#000000", 1.0, 0)]))
            elif v == "cell":
                for x in (-M, W - 40):
                    f.rect(x, -M, 260, H + 2 * M, shader=f.lin(x, 0, x + 260, 0, [("#000000", 0.0, 240), ("#000000", 1.0, 0)] if x < 0 else [("#000000", 0.0, 0), ("#000000", 1.0, 240)]))
            else:
                f.rect(W - 120, -M, 300, H + 2 * M, shader=f.lin(W - 120, 0, W + 180, 0, [("#000000", 0.0, 0), ("#0b0705", 0.6, 235), ("#0b0705", 1.0, 255)]))
            R.vignette_frame(f, 0.72, 0.52)

        return [(0.12, L0), (0.85, L1), (1.0, L2), (1.38, L3)]

    # -- props
    def _props_tordesillas(self, f, lights):
        # alçak yatak (hasır + koyu battaniye)
        frame = R.rrect_path(318, 868, 410, 36, 5)
        R.lit_path(f, frame, "#241812", lights)
        mat_ = sk.smooth_path([(326, 872), (340, 842), (420, 832), (540, 836), (650, 834), (716, 850), (722, 872)], True, 0.5)
        R.lit_path(f, mat_, "#2d2217", lights)
        blank = sk.smooth_path([(380, 872), (392, 846), (470, 836), (560, 840), (640, 840), (718, 856), (722, 874)], True, 0.5)
        R.lit_path(f, blank, "#1a1311", lights)
        for k in range(5):
            f.line(430 + k * 58, 842 + (k % 2) * 3, 424 + k * 60, 872, color="#0a0706", sw=1.4, alpha=0.5)
        for k in range(14):
            f.line(330 + k * 6, 872, 322 + k * 5.4, 884 + (k % 3), color="#6a5530", sw=1.2, alpha=0.5)
        # duvarda haç
        f.rect(582, 392, 10, 96, color="#1a110a")
        f.rect(556, 418, 62, 10, color="#1a110a")
        f.line(587, 394, 587, 486, color="#8a6a40", sw=1.0, alpha=0.5)
        # masa + mum + testi
        _table(f, 1300, 936, w=300, top_y=790, lights=lights)
        R.candle_body(f, 1292, 790, h=84, w=17, holder=True)
        _jug(f, 1400, 790, 1.0, lights=lights)
        _book(f, 1210, 790, 78, 15, "#3a1e16", lights)
        # tabure
        _shadow_ellipse(f, 780, 950, 280, 22, 0.6, 16)

    def _props_cell(self, f, lights):
        # tahta sıra + saman
        bench = R.rrect_path(1120, 840, 330, 24, 4)
        R.lit_path(f, bench, "#2a1c12", lights, rim="#8f6a40", rim_w=1.2)
        for x in (1150, 1420):
            R.lit_path(f, R.rect_path(x - 9, 864, 18, 52), "#1c120b", lights)
        _table(f, 1230, 936, w=230, top_y=800, lights=lights)
        R.candle_body(f, 1230, 800, h=66, w=15, holder=True)
        # yazılmış/ katlanmış kâğıt
        f.poly([(1160, 800), (1196, 790), (1206, 798), (1170, 806)], color="#8b7d62", alpha=0.9)
        _shadow_ellipse(f, 930, 954, 150, 18, 0.6, 14)
        # zincir halkaları duvarda
        for i in range(6):
            f.oval(560 + i * 8, 540 + i * 18 + (i % 2) * 2, 5, 8, style="stroke", sw=2.4, color="#201a16")

    def _props_wartburg(self, f, lights):
        # yazı masası (pencere önü) + kitaplar + hokka
        _table(f, 1130, 936, w=520, top_y=708, lights=lights, col="#3d2817")
        R.candle_body(f, 1182, 708, h=70, w=16, holder=True)
        _book(f, 1010, 708, 120, 22, "#4b2418", lights, ang=-0.02)
        _book(f, 1014, 686, 100, 18, "#2b3a30", lights, ang=0.03)
        f.poly([(1076, 708), (1160, 698), (1196, 704), (1112, 716)], color="#cbbf9e", alpha=0.9)      # yazılı kâğıt
        for k in range(4):
            f.line(1086 + k * 5, 706 - k * 1.6, 1160 + k * 3, 700 - k * 1.2, color="#6a5a3a", sw=1.0, alpha=0.5)
        f.rrect(1240, 682, 20, 26, 4, color="#10090a")
        # yeşil çini soba (sağ köşe)
        stove = sk.smooth_path([(1450, 900), (1450, 640), (1462, 600), (1500, 586), (1590, 586), (1628, 600), (1640, 640), (1640, 900)], True, 0.12)
        R.lit_path(f, stove, "#1d3a2c", [(1182, 700, 560, "#ff9c40", 0.55)], rim="#7aa48a", rim_w=1.0,
                   grad=f.lin(1450, 0, 1640, 0, [("#0f2219", 0.0), ("#244a37", 0.35), ("#173026", 0.7), ("#0a1710", 1.0)]))
        f.c.save()
        f.c.clipPath(stove, skia.ClipOp.kIntersect, True)
        for i in range(6):
            f.line(1450 + i * 38, 586, 1450 + i * 38, 900, color="#06100b", sw=1.6, alpha=0.7)
        for j in range(9):
            f.line(1450, 600 + j * 36, 1640, 600 + j * 36, color="#06100b", sw=1.6, alpha=0.7)
            f.line(1450, 602 + j * 36, 1640, 602 + j * 36, color="#6fa88a", sw=0.8, alpha=0.18)
        f.c.restore()
        f.rect(1440, 896, 210, 12, color="#120c08")
        # duvarda kılıç
        sw_ = sk.poly_path([(536, 400), (552, 400), (564, 730), (548, 734)], True)
        R.lit_path(f, sw_, "#14100d", [(1182, 700, 760, "#ff9c40", 0.25)], rim="#9aa6c0", rim_w=1.2)
        f.rect(514, 392, 66, 10, color="#14100d")
        f.rect(514, 392, 66, 2, color="#b88a3a", alpha=0.6)
        f.rect(540, 360, 8, 34, color="#1a120b")
        f.circle(544, 354, 8, color="#8a6a30")
        f.rect(534, 726, 22, 12, color="#8a6a30", alpha=0.8)
        # tabure
        _shadow_ellipse(f, 960, 950, 250, 20, 0.6, 14)

    def dyn(self):
        p, c = self.p, self.c
        fig = self.fig
        cx_, cy_ = c["candle"]
        night = self.night
        cs = self.candle

        def D2(f, t):
            fx, fy, fh = c["fig_xy"]
            kinds = {"woman": "woman_seated", "man": "man_window", "writer": "writer_seated"}
            if fig in kinds:
                sway = math.sin(t * 0.7) * 0.004 if fig != "writer" else 0.0
                bob = math.sin(t * 0.9) * 1.2
                if fig == "man":
                    RF(f, kinds[fig], fx, fy, fh, rim="#E0A15A", rimd=(1.0, -0.15), rim2="#7FA0E8" if night else "#9aa0a8", rim2d=(0.8, -0.7), sway=sway, bob=bob)
                elif fig == "writer":
                    RF(f, kinds[fig], fx, fy, fh, rim="#F0B060", rimd=(1.0, -0.2), rim2="#7FA0E8", rim2d=(0.7, -0.8), sway=0.0, bob=math.sin(t * 2.4) * 1.5)
                else:
                    RF(f, kinds[fig], fx, fy, fh, rim="#E0A15A", rimd=(1.0, -0.15), rim2="#7FA0E8" if night else "#9aa0a8", rim2d=(0.8, -0.7), sway=sway, bob=bob)
            if cs > 0.01:
                R.flame(f, cx_, cy_ - 8 - (0 if self.v != "tordesillas" else 0), s=1.15 * cs, t=t, seed=1.0, halo=1.0, hr=210)
            polys_rect = (900, 520, 520, 460)
            R.motes(f, t, polys_rect, n=26, seed=4, col="#BFD2FF" if night else "#E8E8E0", a=0.5, drift=(4, 6))
            if cs > 0.01:
                R.motes(f, t, (cx_ - 180, cy_ - 200, 360, 260), n=14, seed=9, col="#FFD8A0", a=0.5, drift=(5, -4))

        return {2: D2}


# ═══════════════════════════════════════════════════════════════════════
#  COUNTING_HOUSE — bankacı sayım odası (Augsburg / Anvers)
# ═══════════════════════════════════════════════════════════════════════
import props_rooms as PR
CW_, CH_ = W + 2 * MARGIN, H + 2 * MARGIN


@SL.sc("counting_house")
class CountingHouse:
    """Bankacının sayım odası: lambrili yeşil duvar, kirişli tavan, dama zemin, iki vitray pencere, avize, büyük masa (ekose örtü),
    defter, terazi, para yığınları, kasa, katipler.
    p: coins=0..1 (0.55), coins_t=None|(t0,t1) yerel sn'de 0→coins dolar (dyn), clerks=0..4 (2), chandelier=True, balance_tilt=0.0 (rad; None=hafif salınır)."""

    def __init__(self, p):
        self.p = p
        self.coins = float(p.get("coins", 0.55))
        self.coins_t = p.get("coins_t")
        self.clerks = int(p.get("clerks", 2))
        self.chand = p.get("chandelier", True)

    BACK = (250, 40, 1670, 880)
    VP = (960, 470)
    WINS = [(470, 170, 610, 430), (1310, 170, 1450, 430)]
    T, SPL = 110.0, 0.80
    TABLE = dict(far=835, near=905, fx=(610, 1310), nx=(520, 1400), drop=1030)
    CAND = [(720, 846), (1196, 846)]

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=1100.0, F=1100.0)

    def layers(self):
        box = self._box()
        cache = {}
        wins = self.WINS
        outers = [box.hole_outer(w, self.T, self.SPL) for w in wins]
        zw = box.zb + self.T
        coins = self.coins
        coins_t = self.coins_t
        chand = self.chand

        def room():
            if "r" in cache:
                return cache["r"]
            plaster = R.mat_plaster("#2c3a2c", seed=5, stain=0.45, tone=0.10)
            wood = R.mat_planks("#3a2616", seed=8, pw=110, plen=800, tone=0.14)
            # lambri sınırı: Yd = (y-vy)*zb/F ; y=668 → 198
            b0 = (668 - self.VP[1]) * 1.0
            wall = R.mat_split(plaster, wood, b0, trim="#9a7a3a")
            floor = R.mat_checker("#241d18", "#4d4338", size=130, seed=4)
            ceil = R.mat_beams("#2a1c11", seed=7, pitch=260, bwid=76, plaster="#3a3322", axis="a")
            mats = dict(back=wall, left=wall, right=wall, floor=floor, ceil=ceil)
            lights = [R.Light((960, 185, 880), R.warm(1.0), 1.15, 560, spec=0.2),
                      R.Light((self.CAND[0][0], 760, 900), R.warm(1.0), 1.5, 260, spec=0.5, far=(520, (0.55, 0.20, 0.05), 0.10)),
                      R.Light((self.CAND[1][0], 760, 900), R.warm(1.0), 1.5, 260, spec=0.5, far=(520, (0.55, 0.20, 0.05), 0.10))]
            moons = []
            for (o, sg) in zip(outers, (1, -1)):
                g = R.window_gobo(box, o, zw, xs=[(o[0] + o[2]) / 2], bar_w=7, ys=[(o[1] + o[3]) / 2], bar_hw=7)
                moons.append(R.Moon((0.42 * sg, 0.85, -0.42), col=(1.0, 0.66, 0.30), power=1.2, win=g, pen=4.0, pen_k=0.012))
            holes = [dict(rect=w, T=self.T, splay=self.SPL, mat=wood, ao=0.25) for w in wins]
            rgb, cov = box.render(mats, lights, moon=moons, ambient=(0.010, 0.012, 0.010), expo=1.25, ao=0.55, holes=holes)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L0(f):          # pencerelerden görünen akşam gökyüzü + şehir
            f.rect(-M, -M, W + 2 * M, H + 2 * M, shader=f.lin(0, -M, 0, 520, [("#1a1830", 0.0), ("#5a2f3a", 0.55), ("#d27a38", 0.9), ("#f0a85a", 1.0)]))
            R.glow(f, 540, 470, 300, "#ffb060", 0.5, sy=0.6)
            R.glow(f, 1380, 470, 300, "#ffb060", 0.5, sy=0.6)
            for (ox, oy) in ((540, 0), (1380, 0)):
                PR.roof_silhouette(f, 470, ox - 260, ox + 260, col="#150c10", seed=int(ox) % 7 + 1, spires=1)
            for i in range(30):
                f.circle(np.random.RandomState(i).uniform(300, 1600), np.random.RandomState(i + 40).uniform(-100, 260), 1.2, color="#ffe8c8", alpha=0.35)

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            for (o, w) in zip(outers, wins):
                x0, y0, x1, y1 = o
                PR.lattice(f, o, step=22, col="#0e0a08", sw=2.6, alpha=0.9, frame="#1a120b")

        def L2(f):          # arka duvar eşyaları
            lights = [(960, 190, 560, "#ffb45a", 0.38), (self.CAND[0][0], 780, 300, "#ff9c40", 0.40), (self.CAND[1][0], 780, 300, "#ff9c40", 0.40)]
            PR.banner_hang(f, 960, 130, 190, 330, "#2a4630", "#c9962b", lights, icon="coinbag")
            PR.shelf_books(f, 640, 640, 230, rows=3, row_h=88, seed=3, lights=lights)
            PR.shelf_books(f, 1050, 640, 230, rows=3, row_h=88, seed=9, lights=lights)
            PR.chest(f, 1500, 876, 210, 104, lights, open_k=0.9)
            PR.chest(f, 380, 880, 170, 84, lights, open_k=0.0, gold=False)
            # zemin gölgeleri
            _shadow_ellipse(f, 960, 900, 520, 26, 0.55, 20)

        def L3(f):          # masa + üstündekiler (statik kısım)
            t = self.TABLE
            top = sk.poly_path([(t["fx"][0], t["far"]), (t["fx"][1], t["far"]), (t["nx"][1], t["near"]), (t["nx"][0], t["near"])], True)
            lights = [(self.CAND[0][0], 850, 250, "#ffb060", 0.30), (self.CAND[1][0], 850, 250, "#ffb060", 0.30), (960, 190, 600, "#ffb45a", 0.10)]
            R.lit_path(f, top, "#152b1d", lights, rim="#a8812c", rim_w=1.6,
                       grad=f.lin(0, t["far"], 0, t["near"], [("#1f3a28", 0.0), ("#10231a", 1.0)]))
            # ekose örtü çizgileri (perspektif)
            f.c.save()
            f.c.clipPath(top, skia.ClipOp.kIntersect, True)
            for i in range(0, 15):
                u = i / 14.0
                xa = t["fx"][0] + (t["fx"][1] - t["fx"][0]) * u
                xb = t["nx"][0] + (t["nx"][1] - t["nx"][0]) * u
                f.line(xa, t["far"], xb, t["near"], color="#c9a24a", sw=1.2, alpha=0.35)
            for j in range(1, 5):
                yy = t["far"] + (t["near"] - t["far"]) * (j / 5.0) ** 1.2
                f.line(t["fx"][0] - 100, yy, t["fx"][1] + 100, yy, color="#c9a24a", sw=1.2, alpha=0.33)
            f.c.restore()
            front = sk.poly_path([(t["nx"][0], t["near"]), (t["nx"][1], t["near"]), (t["nx"][1] - 14, t["drop"]), (t["nx"][0] + 14, t["drop"])], True)
            R.lit_path(f, front, "#14281c", lights, grad=f.lin(0, t["near"], 0, t["drop"], [("#14291d", 0.0), ("#070e0a", 1.0)]))
            f.rect(t["nx"][0] + 14, t["drop"] - 14, t["nx"][1] - t["nx"][0] - 28, 14, color="#c9962b", alpha=0.7)
            for k in range(10):
                f.rect(t["nx"][0] + 24 + k * 87, t["drop"] - 12, 8, 12, color="#c9962b", alpha=0.5)
            # defter, mum, divit, mektup
            PR.ledger_open(f, 880, 884, w=190, h=40, lights=lights, seed=2)
            PR.wax_seal_letter(f, 1090, 878, 56, 30, -0.12, lights)
            PR.inkwell(f, 780, 870)
            for (cx, cy) in self.CAND:
                PR.candelabra(f, cx, cy, branches=3, h=120)
            if self.coins_t is None:
                self._coins(f, coins)
            return

        def L4(f):          # ön plan: karanlık kiriş/zincir ve kenar karartma
            f.rect(-M, -M, 120 + M, H + 2 * M, shader=f.lin(-M, 0, 120, 0, [("#000000", 0.0, 235), ("#000000", 1.0, 0)]))
            f.rect(W - 120, -M, 120 + M, H + 2 * M, shader=f.lin(W - 120, 0, W + M, 0, [("#000000", 0.0, 0), ("#000000", 1.0, 235)]))
            R.vignette_frame(f, 0.7, 0.55)

        return [(0.1, L0), (0.85, L1), (1.0, L2), (1.14, L3), (1.4, L4)]

    def _coins(self, f, k):
        """k: 0..1 (statik) — masa üstündeki sikke sütunları/yığınları; k büyüdükçe sütun sayısı/yığın artar."""
        if k <= 0.001:
            return
        stacks = [(660, 880, 5), (700, 884, 8), (740, 880, 4), (1160, 882, 6), (1200, 886, 9), (1240, 882, 5), (1290, 878, 4), (1030, 890, 3),
                  (1330, 872, 3), (640, 872, 3)]
        n = len(stacks)
        for i, (x, y, cnt) in enumerate(stacks):
            u = min(1.0, max(0.0, k * (n + 3) / n - i / n))
            c = int(round(cnt * u * (0.6 + 0.4 * min(1, k * 1.4))))
            if c > 0:
                PR.coin_stack(f, x, y, c, r=15, seed=i)
        if k > 0.25:
            PR.coin_pile(f, 1370, 900, 160 + 100 * k, 40 + 36 * k, int(60 + 220 * k), seed=2)
        if k > 0.55:
            PR.coin_pile(f, 560, 900, 120 + 70 * k, 30 + 26 * k, int(40 + 150 * (k - 0.4)), seed=5)

    def dyn(self):
        clerks = self.clerks
        coins_t = self.coins_t
        coins = self.coins
        chand = self.chand
        CAND = self.CAND

        def D2(f, t):
            # katipler (alçak sıralarda), ayna simetrik
            spots = [(150, 972, 340, 1, 190), (1770, 972, 340, -1, 190), (420, 908, 250, 1, 150), (1500, 908, 250, -1, 150)]
            for i, (x, y, h, face, dw) in enumerate(spots[:clerks]):
                dk = h * 0.30
                deskx = x + face * dk
                PR.desk_slant(f, min(deskx, deskx + face * h * 0.7) if face > 0 else deskx - h * 0.7, y, w=h * 0.7, h=h * 0.58, lights=[(960, 600, 900, "#ffb45a", 0.12)])
                RF(f, "clerk_seated", x, y, h, rim="#F0B060", rimd=(1.0, -0.3), rim2="#FFC878", rim2d=(0.3, -1.0), face=face, bob=math.sin(t * 2.2 + i) * 1.4)
            if chand:
                cxs = (960, 190, 150)
                ST.chandelier(f, 960, 190, 150)
                for i in range(8):
                    a = math.pi * 2 * i / 8
                    R.flame(f, 960 + math.cos(a) * 150, 190 + math.sin(a) * 33 - 22, s=0.8, t=t, seed=i * 1.7, halo=0.4, hr=90)
            R.motes(f, t, (300, 120, 1300, 700), n=30, seed=3, col="#FFD9A0", a=0.45, drift=(4, -3))

        def D3(f, t):
            for i, (cx, cy) in enumerate(CAND):
                tips = [(cx - 46 * 0 + (j - 1) * 46, cy - 120 - abs(j - 1) * 14 - 38) for j in range(3)]
                for j, (fx, fy) in enumerate(tips):
                    R.flame(f, fx, fy, s=1.0, t=t, seed=i * 3 + j, halo=0.55, hr=120, a=0.95)
            # terazi (hafif salınım)
            tilt = self.p.get("balance_tilt")
            tilt = (math.sin(t * 0.9) * 0.05 + 0.035) if tilt is None else tilt
            PR.balance(f, 1010, 862, 0.62, tilt, coins_l=3 if coins > 0.3 else 1, coins_r=1)
            if coins_t is not None:
                t0, t1 = coins_t
                k = coins * smooth((t - t0) / max(0.1, t1 - t0))
                self._coins(f, k)
            # sikke parıltıları
            kk = coins if coins_t is None else coins * smooth((t - coins_t[0]) / max(0.1, coins_t[1] - coins_t[0]))
            if kk > 0.05:
                rs = np.random.RandomState(7)
                pa = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
                for i in range(10):
                    x = rs.choice([rs.uniform(640, 760), rs.uniform(1150, 1330)])
                    y = rs.uniform(820, 885)
                    a = max(0.0, math.sin(t * (1.5 + rs.rand() * 2) + i * 2.3)) ** 6 * kk
                    if a > 0.05:
                        pa.setColor(C("#FFF2C0", int(255 * a)))
                        f.c.drawCircle(x, y, 2.4, pa)
                        pa.setColor(C("#FFF2C0", int(120 * a)))
                        f.c.drawLine(x - 9, y, x + 9, y, pa)
                        f.c.drawLine(x, y - 9, x, y + 9, pa)

        return {2: D2, 3: D3}


# ═══════════════════════════════════════════════════════════════════════
#  ELECTORS_HALL — Frankfurt, yedi seçmen
# ═══════════════════════════════════════════════════════════════════════
def _floor_pts(box, R_, Zc, n=72, Xc=0.0, yscale=1.0):
    """Zeminde (Xc,Zc) merkezli R_ yarıçaplı çemberin ekran noktaları."""
    YF = (box.by1 - box.vy) * box.zb / box.F
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append(box.screen(Xc + R_ * math.cos(a), YF, Zc + R_ * math.sin(a) * yscale))
    return pts


@SL.sc("electors_hall")
class ElectorsHall:
    """Frankfurt seçim salonu: yarım daire yedi koltuk, sivri vitray pencerelerden süzülen ışık huzmeleri, taş sütunlar, zemin halkası.
    p: seats=7 (1..7), occupied=True (koltuklarda adsız seçmen siluetleri), light_t=None|(t0,t1) yerel sn'de koltuklar sırayla parlar,
    daylight=1.0 (pencere ışığı çarpanı)."""

    BACK = (380, 110, 1540, 800)
    VP = (960, 460)
    ZC, RX, RZ = 790.0, 430.0, 250.0
    PHI = {7: [-70, -47, -23, 0, 23, 47, 70]}
    GEAR = {7: ["mitre", "kurhut", "kurhut", "mitre", "kurhut", "crown", "mitre"]}

    def __init__(self, p):
        self.p = p
        self.n = int(clamp(p.get("seats", 7), 1, 7))
        self.occ = p.get("occupied", True)
        self.light_t = p.get("light_t")
        self.day = float(p.get("daylight", 1.0))

    def _seats(self):
        n = self.n
        if n >= 7:
            idx = list(range(7))
        else:
            order = [3, 2, 4, 1, 5, 0, 6]
            idx = sorted(order[:n])
        box = R.Box(self.BACK, vp=self.VP, zb=1100.0, F=1100.0)
        YF = (box.by1 - box.vy) * box.zb / box.F
        out = []
        for i in idx:
            ph = math.radians(self.PHI[7][i])
            X = self.RX * math.sin(ph)
            Z = self.ZC + self.RZ * math.cos(ph)
            x, _ = box.screen(X, 0, Z)
            y = box.vy + YF * box.F / Z
            sc = box.F / Z
            out.append(dict(i=i, x=x, y=y, s=sc, gear=self.GEAR[7][i]))
        return out

    def layers(self):
        box = R.Box(self.BACK, vp=self.VP, zb=1100.0, F=1100.0)
        cache = {}
        seats = self._seats()
        day = self.day
        win = [(960, 150, 190, 430), (700, 190, 150, 360), (1220, 190, 150, 360)]      # (cx, top, w, h)

        def room():
            if "r" in cache:
                return cache["r"]
            stone = R.mat_stone_fine("#7a6b57", seed=4, course=52)
            floor = R.mat_checker("#2a241f", "#463d33", size=150, seed=6)
            ceil = R.mat_beams("#5a4c3e", seed=7, pitch=340, bwid=74, plaster="#352d25", axis="b")
            mats = dict(back=stone, left=stone, right=stone, floor=floor, ceil=ceil)
            lights = [R.Light((330, 640, 820), R.warm(1.0), 1.4, 260, spec=0.3), R.Light((1590, 640, 820), R.warm(1.0), 1.4, 260, spec=0.3),
                      R.Light((960, 120, 760), (0.5, 0.42, 0.30), 0.5, 600)]
            moons = []
            for (cx, top, w, h) in win:
                g = dict(z=box.zb, wrect=((cx - w / 2 - box.vx), (top - box.vy), (cx + w / 2 - box.vx), (top + h - box.vy)))
                dx = (cx - 960) / 960.0 * -0.35
                moons.append(R.Moon((dx, 0.72, -0.62), col=(1.0, 0.82, 0.52), power=1.15 * day, win=g, pen=6.0, pen_k=0.018))
            rgb, cov = box.render(mats, lights, moon=moons, ambient=(0.009, 0.008, 0.009), expo=1.0, ao=0.6)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # lanset pencereler (emisyon)
            for (cx, top, w, h) in win:
                PR.pointed_window(f, cx, top + h / 2, w, h, glow=("#fff0c8", "#f2b050"), frame="#241609", edge="#9a7440", k=1.2,
                                  pane=["#ffd68a", "#9ec0ff", "#ff9a7a", "#ffe9b0"])
                R.glow(f, cx, top + h * 0.45, w * 1.7, "#ffd9a0", 0.22 * day)

        def L2(f):
            lights = [(330, 640, 330, "#ff9c40", 0.45), (1590, 640, 330, "#ff9c40", 0.45), (960, 600, 900, "#ffd090", 0.07)]
            # yer halkası (altın + koyu)
            for (r_, col, a, sw) in ((235, "#c9962b", 0.65, 4.0), (200, "#7a5518", 0.5, 2.4), (150, "#c9962b", 0.4, 2.0)):
                pts = _floor_pts(box, r_, 790.0)
                f.path(sk.poly_path(pts, True), style="stroke", sw=sw, color=col, alpha=a)
            # yıldız
            sp = []
            for k in range(16):
                rr = 235 if k % 2 == 0 else 120
                a = math.pi * 2 * k / 16
                sp.append(_floor_pts(box, rr, 790.0, n=1)[0] if False else box.screen(rr * math.cos(a), (box.by1 - box.vy), 790.0 + rr * math.sin(a)))
            f.path(sk.poly_path(sp, True), style="stroke", sw=1.6, color="#c9962b", alpha=0.35)
            # ışık huzmeleri
            for (cx, top, w, h) in win:
                dx = (cx - 960) / 960.0 * -0.35
                polys = R.shaft_polys(box, (cx - w / 2, top, cx + w / 2, top + h), box.zb, (dx, 0.72, -0.62), [], 8)
                for q in polys:
                    _soft_hull(f, q, "#ffe2a8", 0.20 * day)
            # koltuklar (arkadan öne)
            for st in sorted(seats, key=lambda s: s["y"]):
                PR.chair_high(f, st["x"], st["y"], st["s"] * 1.05, lights, col="#35210f", trim="#c9962b")
            # yan şamdanlar
            for sx in (330, 1590):
                PR.candelabra(f, sx, 940, branches=5, h=240, arm=64)
                f.rect(sx - 14, 936, 28, 8, color="#1a120a")

        def L3(f):          # ön plan: koyu sütunlar
            for sx in (-1, 1):
                x = W / 2 + sx * 980
                col = R.rect_path(x - 90, -M, 180, H + 2 * M)
                R.lit_path(f, col, "#2a2016", [(W / 2 + sx * 700, 540, 700, "#ffb060", 0.18)], rim=None,
                           grad=f.lin(x - 90, 0, x + 90, 0, [("#0b0705", 0.0), ("#3a2c1e", 0.55), ("#0b0705", 1.0)]))
            R.vignette_frame(f, 0.72, 0.55)

        return [(0.85, L1), (1.0, L2), (1.35, L3)]

    def dyn(self):
        seats = self._seats()
        occ = self.occ
        light_t = self.light_t
        n = len(seats)

        def D2(f, t):
            order = sorted(seats, key=lambda s: s["y"])
            # 1) parlama (figürün ARKASINDA: siluet kenarı parlar, yüz parlamaz)
            if light_t is not None:
                t0, t1 = light_t
                for st in order:
                    ti = t0 + (t1 - t0) * (st["i"] / 6.0)
                    k = smooth((t - ti) / 0.5)
                    if k > 0.01:
                        hy = st["y"] - (300 * 0.86 * st["s"] if occ else 330 * st["s"])
                        R.glow(f, st["x"], hy, 190 * st["s"] * (0.8 + 0.2 * k), "#FFC860", 0.50 * k)
                        R.glow(f, st["x"], hy - 6 * st["s"], 80 * st["s"], "#FFF3C8", 0.55 * k)
                        f.circle(st["x"], hy - 34 * st["s"], 62 * st["s"] * (0.9 + 0.1 * k), style="stroke", sw=2.4 * st["s"], color="#FFE9A8", alpha=0.75 * k)
            # 2) seçmenler
            for st in order:
                if occ:
                    h = 300 * st["s"]
                    RF(f, "elector_" + st["gear"], st["x"], st["y"] - 4 * st["s"], h, rim="#FFE2A8", rimd=(0.0, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1),
                       bob=math.sin(t * 0.8 + st["i"]) * 1.0)
            for sx in (330, 1590):
                tips = [(sx + (j - 2) * 32, 940 - 240 - abs(j - 2) * 12 - 38) for j in range(5)]
                for j, (fx, fy) in enumerate(tips):
                    R.flame(f, fx, fy, s=1.0, t=t, seed=sx * 0.01 + j, halo=0.5, hr=130)
            R.motes(f, t, (360, 130, 1200, 760), n=34, seed=5, col="#FFE2A8", a=0.5, drift=(3, 5))

        return {1: D2}


def _soft_hull(f, q, col, a):
    """Çokgen (n>4) ışık huzmesi, yumuşak."""
    pa = skia.Paint(AntiAlias=True, Color=C(col, int(255 * a)), BlendMode=skia.BlendMode.kPlus)
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7))
    f.c.drawPath(sk.poly_path(q, True), pa)


# ═══════════════════════════════════════════════════════════════════════
#  AACHEN — Palatin Şapeli (taç giyme)
# ═══════════════════════════════════════════════════════════════════════
@SL.sc("aachen")
class Aachen:
    """Aachen Şapeli iç mekânı: iki katlı kırmızı/beyaz kemerli galeri, altın mozaik tavan, çark avize, ışık huzmeleri, mermer zemin.
    Merkezde diz çökmüş genç Karl, iki yanında piskopos; taç ışık huzmesinde iner.
    p: crown_t=(t0,t1) yerel sn'de taç iner (varsayılan (1.5,5.5)), crown_show=True (inmeden önce de yukarıda soluk görünür),
    figure=True, bishops=True, attend=True (arka plan nedimleri), flash=1.0 (taç oturunca parlama)."""

    BACK = (430, 100, 1490, 860)
    VP = (960, 470)

    def __init__(self, p):
        self.p = p
        self.crown_t = tuple(p.get("crown_t", (1.5, 5.5)))
        self.show = p.get("crown_show", True)
        self.fig = p.get("figure", True)
        self.bishops = p.get("bishops", True)
        self.attend = p.get("attend", True)
        self.flash = float(p.get("flash", 1.0))

    KING = (960, 962, 330)           # x, ayak y, boy
    BISH = [(650, 946, 380, 1), (1270, 946, 380, -1)]

    def layers(self):
        box = R.Box(self.BACK, vp=self.VP, zb=1100.0, F=1100.0)
        cache = {}

        def room():
            if "r" in cache:
                return cache["r"]
            fb = (self.BACK[3] - self.VP[1])
            arc = R.mat_arcade(fb, stone="#a69880", brick="#8a3528", white="#d3c7a8", bay=215.0, seed=5)
            floor = R.mat_checker("#8c8068", "#3d352c", size=170, seed=3)
            ceil = R.mat_mosaic("#c9962b", seed=2, tile=9.0)
            mats = dict(back=arc, left=arc, right=arc, floor=floor, ceil=ceil)
            lights = [R.Light((960, 235, 830), R.warm(1.0), 3.0, 560, spec=0.7, far=(900, (0.6, 0.30, 0.10), 0.25)),
                      R.Light((960, 120, 700), (0.65, 0.5, 0.3), 1.0, 500, spec=1.0)]
            rgb, cov = box.render(mats, lights, ambient=(0.010, 0.009, 0.009), expo=1.1, ao=0.6, bump=1.1)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)

        def L2(f):
            # yer madalyonu
            YF = (box.by1 - box.vy)
            for (r_, col, a, sw) in ((240, "#c9962b", 0.55, 4.0), (205, "#7a5518", 0.5, 2.4), (130, "#c9962b", 0.4, 2.0)):
                pts = [box.screen(r_ * math.cos(2 * math.pi * i / 72), YF, 900.0 + r_ * math.sin(2 * math.pi * i / 72)) for i in range(72)]
                f.path(sk.poly_path(pts, True), style="stroke", sw=sw, color=col, alpha=a)
            # ışık huzmeleri (üst pencerelerden)
            for (x0, x1, ex0, ex1, a) in ((560, 650, 760, 900, 0.20), (1270, 1360, 1020, 1160, 0.20), (880, 1040, 900, 1020, 0.14)):
                _soft_hull(f, [(x0, 110), (x1, 110), (ex1, 960), (ex0, 960)], "#ffe0a0", a)
            # avize (Barbarossa çarkı): zincirler + halka + kuleler
            cx, cy, rx, ry = 960, 330, 250, 46
            for ang in (-2.4, -0.74, 0.74, 2.4):
                px = cx + math.cos(ang) * rx * 0.9
                py = cy + math.sin(ang) * ry * 0.9
                f.line(px, py, 960 + (px - 960) * 0.15, -M, color="#2a1c0a", sw=3.4)
                f.line(px, py, 960 + (px - 960) * 0.15, -M, color="#c9962b", sw=1.0, alpha=0.55)
            for (rr, sw, col) in ((1.0, 13, "#8a6220"), (0.96, 5, "#e9c35a"), (0.62, 6, "#8a6220"), (0.60, 2.2, "#e9c35a")):
                f.oval(cx, cy, rx * rr, ry * rr, style="stroke", sw=sw, color=col)
            f.oval(cx, cy + 8, rx, ry, style="stroke", sw=3, color="#2a1c0a", alpha=0.7)
            for i in range(16):
                a = 2 * math.pi * i / 16
                px, py = cx + math.cos(a) * rx, cy + math.sin(a) * ry
                if math.sin(a) < 0:      # arka yarı: kule siluet
                    f.rect(px - 7, py - 34, 14, 34, color="#6a4a14")
                else:
                    f.rect(px - 8, py - 40, 16, 40, shader=f.lin(px - 8, 0, px + 8, 0, [("#7a5518", 0.0), ("#e9c35a", 0.5), ("#7a5518", 1.0)]))
                    for q in range(3):
                        f.rect(px - 8 + q * 6, py - 46, 4, 7, color="#c9962b")
                f.rect(px - 4, py - 74, 8, 34, shader=f.lin(px - 4, 0, px + 4, 0, [("#9c8a5e", 0.0), ("#efe0b0", 0.5), ("#9c8a5e", 1.0)]))
            R.glow(f, cx, cy + 30, 360, "#ffb060", 0.20, sy=0.5)
            # nedimler / soylular (arka planda, sisli)
            if self.attend:
                for (x0, x1, seed) in ((470, 640, 3), (1280, 1450, 8)):
                    ST.crowd(f, 1, x0, x1, 868, 40, 250, 1.0, ["noble", "cardinal", "scribe", "noble"], col="#0e0906", rim="#8a5a2a", seed=seed, dens=62, face=1 if x0 < 900 else -1, depth_fog="#2A170C")
            _shadow_ellipse(f, 960, 970, 340, 22, 0.6, 18)

        def L3(f):
            for sx in (-1, 1):
                x = W / 2 + sx * 1010
                col = R.rect_path(x - 100, -M, 200, H + 2 * M)
                R.lit_path(f, col, "#2a2016", [(W / 2 + sx * 720, 540, 700, "#ffb060", 0.15)],
                           grad=f.lin(x - 100, 0, x + 100, 0, [("#0b0705", 0.0), ("#3a2c1e", 0.5), ("#0b0705", 1.0)]))
            R.vignette_frame(f, 0.75, 0.52)

        return [(0.82, L1), (1.0, L2), (1.36, L3)]

    def dyn(self):
        t0, t1 = self.crown_t
        kx, ky, kh = self.KING
        show, fig, bish, flash = self.show, self.fig, self.bishops, self.flash

        def D2(f, t):
            # piskoposlar
            if bish:
                for (x, y, h, face) in self.BISH:
                    RF(f, "bishop_standing", x, y, h, rim="#FFD890", rimd=(0.0, -1.0), rim2="#E39A4A", rim2d=(-face * 0.9, 0.1), face=face, bob=math.sin(t * 0.7 + x) * 1.0)
            if fig:
                RF(f, "king_kneel", kx, ky, kh, rim="#FFD890", rimd=(0.3, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1), bob=math.sin(t * 0.9) * 0.8)
            # taç inişi
            head_y = ky - kh * 0.80
            u = smooth((t - t0) / max(0.1, t1 - t0))
            y_start = head_y - 330
            cy = y_start + (head_y - 10 - y_start) * u
            vis = 1.0 if t >= t0 else (0.55 if show else 0.0)
            vis *= smooth((t + 0.2) / 0.8)
            if vis > 0.01:
                cxp = kx + kh * 0.07
                R.glow(f, cxp, cy - 14, 120 + 40 * u, "#FFE3A0", 0.45 * vis)
                cp = R.crown_path(1.0, 0, 0, 130, 70)
                f.c.save()
                f.c.translate(cxp, cy)
                f.c.drawPath(cp, skia.Paint(AntiAlias=True, Shader=f.lin(0, -80, 0, 0, [("#fff0b0", 0.0, int(255 * vis)), ("#e0a830", 0.5, int(255 * vis)), ("#8a6220", 1.0, int(255 * vis))])))
                f.c.drawPath(cp, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C("#fff6c8", int(200 * vis))))
                for k in range(5):
                    f.circle(-48 + k * 24, -14, 3.2, color="#d33a2a" if k % 2 else "#3a7ad0", alpha=0.9 * vis)
                f.c.restore()
                # iz bırakan kıvılcımlar
                if t0 - 0.2 < t < t1 + 0.6:
                    rs = np.random.RandomState(11)
                    pa = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
                    for i in range(18):
                        ph = (t * 0.9 + rs.rand()) % 1.0
                        sx = cxp + (rs.rand() - 0.5) * 120
                        sy = cy - 20 + ph * 160 * (0.4 + rs.rand())
                        pa.setColor(C("#FFE9A0", int(200 * (1 - ph) * vis)))
                        f.c.drawCircle(sx, sy, 1.6 + rs.rand() * 1.4, pa)
            # oturunca parlama
            if t > t1 and flash > 0:
                k = max(0.0, 1.0 - (t - t1) / 1.4)
                R.glow(f, kx + kh * 0.07, head_y - 10, 380 * (1 + (1 - k) * 0.6), "#FFF0C0", 0.55 * k * flash)
                R.glow(f, kx + kh * 0.07, head_y - 10, 110, "#FFFFFF", 0.7 * k * flash)
            # avize alevleri
            cx, cy2, rx, ry = 960, 330, 250, 46
            for i in range(16):
                a = 2 * math.pi * i / 16
                px, py = cx + math.cos(a) * rx, cy2 + math.sin(a) * ry
                R.flame(f, px, py - 78 - (0 if math.sin(a) >= 0 else -4), s=0.75, t=t, seed=i * 1.9, halo=0.5 if math.sin(a) >= 0 else 0.35, hr=80)
            R.motes(f, t, (440, 120, 1040, 800), n=40, seed=6, col="#FFE2A8", a=0.5, drift=(3, 4))

        return {1: D2}


# ═══════════════════════════════════════════════════════════════════════
#  REICHSTAG — Worms (1521)
# ═══════════════════════════════════════════════════════════════════════
def shade_(c, k):
    return R.shade(c, k)


def _persp(box, YF=None):
    YF = (box.by1 - box.vy) * box.zb / box.F if YF is None else YF

    def P(X, hf, Z):
        return (box.vx + X * box.F / Z, box.vy + (YF - hf) * box.F / Z)
    return P, YF


def _quad(f, pts, col, lights=(), rim=None, grad=None, a=1.0):
    p = sk.poly_path(pts, True)
    R.lit_path(f, p, col, lights, rim=rim, grad=grad, a=a)


@SL.sc("reichstag")
class Reichstag:
    """Worms Reichstag'ı: yüksek gotik salon (sol duvarda sivri pencereler, huzmeler yatay çapraz), uzakta kürsüde küçük Karl (taht + sancak),
    iki yanda sıralar ve kalabalık, ortada halı koridor, tek başına keşiş.
    p: monk=True, books=True (masada kitap yığını), emperor=True (tahtta Karl + yan seçmenler), crowd=True (yan sıralar), monk_z=1000 (keşişin koridordaki derinliği; 700..1500),
    sun=1.0 (pencere ışığı)."""

    BACK = (620, 200, 1300, 660)
    VP = (960, 440)
    ZB = 2000.0

    def __init__(self, p):
        self.p = p
        self.monk = p.get("monk", True)
        self.books = p.get("books", True)
        self.emp = p.get("emperor", True)
        self.crowd = p.get("crowd", True)
        self.monk_z = float(p.get("monk_z", 1000.0))
        self.sun = float(p.get("sun", 1.0))

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    def layers(self):
        box = self._box()
        P, YF = _persp(box)
        cache = {}
        sun = self.sun
        XL = (self.BACK[0] - self.VP[0]) * self.ZB / 1100.0

        # pencere geometrisi (a: duvar boyunca derinlik arka duvardan kameraya; Z = ZB - a)
        PITCH, NWIN, A0, WW = 300.0, 4, 180.0, 170.0
        H1, SPR, H3 = 250.0, 600.0, 760.0
        Zmin = self.ZB - (A0 + (NWIN - 1) * PITCH + WW)     # en yakın pencerenin Z başlangıcı
        D = (0.78, 0.60, -0.33)

        def room():
            if "r" in cache:
                return cache["r"]
            fb = YF
            left = R.mat_hallwall(fb, stone="#6a5c4a", pitch=PITCH, a0=A0, nwin=NWIN, w=WW, h1=H1, spring=SPR, h3=H3, seed=4, power=2.6 * sun)
            right = R.mat_stone_fine("#5a4d3d", seed=9, course=56)
            back = R.mat_stone_fine("#5b4e3e", seed=6, course=56)
            floor = R.mat_stripe(R.mat_flags("#211c17", seed=5, size=200), R.mat_carpet("#4e1218"), 95.0)
            ceil = R.mat_beams("#33241a", seed=7, pitch=300, bwid=100, plaster="#40362a", axis="b")
            mats = dict(back=back, left=left, right=right, floor=floor, ceil=ceil)
            lights = []
            for (y_, Z_) in ((337, 1500), (306, 1150), (259, 850)):
                lights.append(R.Light((960, y_, Z_), R.warm(1.0), 1.2, 340, spec=0.2))
            lights.append(R.Light((960, 520, 1900), R.warm(1.0), 1.4, 260, spec=0.2))
            win = dict(axis="x", x=XL, wrect=(Zmin, YF - H3, Zmin + WW, YF - H1), pitch=PITCH, n=NWIN, spring=YF - SPR)
            moon = R.Moon(D, col=(1.0, 0.86, 0.60), power=1.15 * sun, win=win, pen=7.0, pen_k=0.02)
            rgb, cov = box.render(mats, lights, moon=moon, ambient=(0.007, 0.007, 0.011), expo=0.95, ao=0.6)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # sağ duvara asılı sancaklar (duvarla aynı katmanda: kayma yok)
            for Zc in (1750, 1400, 1050, 780):
                q = [P(618, 600, Zc - 90), P(618, 600, Zc + 90), P(618, 280, Zc + 90), P(618, 280, Zc - 90)]
                col = "#5a1016" if Zc % 2 else "#1c3326"
                _quad(f, q, col, [(960, 400, 800, "#ff9c40", 0.15)], rim="#c9962b",
                      grad=f.lin(0, q[0][1], 0, q[2][1], [(shade_(col, 0.12), 0.0), (col, 0.5), (shade_(col, -0.4), 1.0)]))
                mid = [P(618, 560, Zc - 90), P(618, 560, Zc + 90)]
                f.line(mid[0][0], mid[0][1], mid[1][0], mid[1][1], color="#c9962b", sw=2.0, alpha=0.6)
                f.circle((q[0][0] + q[1][0] + q[2][0] + q[3][0]) / 4, (q[0][1] + q[2][1]) / 2, max(6.0, abs(q[1][0] - q[0][0]) * 0.18), style="stroke", sw=2.0, color="#c9962b", alpha=0.7)

        def L2(f):
            warm_l = [(960, 520, 520, "#ff9c40", 0.22), (960, 300, 700, "#ffb060", 0.10)]
            # pencere huzmeleri (statik; pişirmede)
            for q in R.shaft_polys_x(box, XL, (Zmin, YF - H3, Zmin + WW, YF - H1), D, PITCH, NWIN):
                _soft_hull(f, q, "#ffe2a8", 0.17 * sun)
            # ── kürsü (dais): 3 basamak
            steps = [(420, 0, 45, 1700), (330, 45, 90, 1790), (205, 90, 135, 1880)]
            for (hx, h0, h1, zf) in steps:
                front = [P(-hx, h0, zf), P(hx, h0, zf), P(hx, h1, zf), P(-hx, h1, zf)]
                topq = [P(-hx, h1, zf), P(hx, h1, zf), P(hx * 0.98, h1, 2000), P(-hx * 0.98, h1, 2000)]
                _quad(f, front, "#3a2a1e", warm_l, rim=None, grad=f.lin(0, front[2][1], 0, front[0][1], [("#5a4630", 0.0), ("#241812", 1.0)]))
                _quad(f, topq, "#5a1a20", warm_l, rim="#c9962b", grad=f.lin(0, topq[2][1], 0, topq[0][1], [("#7a2028", 0.0), ("#4a1218", 1.0)]))
            # arka sancak/halı + gölgelik (baldachin)
            tx0, ty0 = P(-300, 560, 1995)
            tx1, ty1 = P(300, 90, 1995)
            PR.banner_hang(f, 960, ty0, (tx1 - tx0), (ty1 - ty0) + 10, "#6b1a22", "#c9962b", warm_l, icon="eagle")
            cy_top = P(0, 640, 1900)[1]
            cx0, cx1 = P(-330, 0, 1900)[0], P(330, 0, 1900)[0]
            canopy = sk.poly_path([(cx0 - 20, cy_top - 12), (cx1 + 20, cy_top - 12), (cx1 + 8, cy_top + 40), (960, cy_top + 62), (cx0 - 8, cy_top + 40)], True)
            R.lit_path(f, canopy, "#7a1c26", warm_l, rim="#c9962b", rim_w=2.0, grad=f.lin(0, cy_top - 12, 0, cy_top + 60, [("#9a2630", 0.0), ("#5a1018", 1.0)]))
            for sx in (-1, 1):
                dr = sk.poly_path([(960 + sx * (cx1 - 960) + sx * 14, cy_top + 20), (960 + sx * (cx1 - 960) - sx * 10, cy_top + 44), (960 + sx * (cx1 - 960) * 0.84, P(0, 200, 1900)[1]),
                                   (960 + sx * (cx1 - 960) * 1.05, P(0, 140, 1900)[1])], True)
                R.lit_path(f, dr, "#5a1018", warm_l, rim=None)
            # taht + Karl + seçmenler
            tp = P(0, 135, 1965)
            sc_t = 1100.0 / 1965.0
            ST.throne(f, tp[0], tp[1] + 6, 0.52 * 1.0, c="#6A1E26")
            if self.emp:
                for (X, kind, hh) in ((-110, "elector_kurhut", 130), (110, "elector_cap", 130), (-225, "elector_mitre", 132), (225, "elector_mitre", 132)):
                    pp = P(X, 90, 1840)
                    RF(f, kind, pp[0], pp[1], hh * 1100.0 / 1840.0, rim="#FFD890", rimd=(0.3, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1))
                RF(f, "elector_crown", tp[0], tp[1] + 2, 150 * sc_t * 1.0, rim="#FFE2A8", rimd=(0.0, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1))
            # koruyucular
            for sx in (-1, 1):
                pp = P(sx * 330, 0, 1700)
                ST.figure(f, "landsknecht", pp[0], pp[1], 170 * 1100.0 / 1700.0, col="#0C0705", rim="#C58A44", face=-sx)
            # sıralar + kalabalık (derinlikten öne; dışta olan önce)
            if self.crowd:
                rs = np.random.RandomState(21)
                hats = ["beret", "cap", "galero", "mitre", "hood", "beret", "cap", "beret"]
                for side in (-1, 1):
                    for (rowX, hf0) in ((520, 0), (410, 0), (310, 0)):
                        X = side * rowX
                        zA, zB = 760, 1700
                        # bank: yan yüz + oturak
                        inner = side * (rowX - 52)
                        outer = side * (rowX + 36)
                        q_front = [P(inner, 0, zA), P(inner, 0, zB), P(inner, 46, zB), P(inner, 46, zA)]
                        q_top = [P(inner, 46, zA), P(inner, 46, zB), P(outer, 46, zB), P(outer, 46, zA)]
                        _quad(f, q_front, "#2a1a10", warm_l, rim=None, grad=f.lin(0, q_front[2][1], 0, q_front[0][1], [("#3a2616", 0.0), ("#150d08", 1.0)]))
                        _quad(f, q_top, "#34200f", warm_l, rim="#8a6a3a")
                        z = zB
                        while z > zA:
                            pp = P(X + rs.uniform(-8, 8), 0, z)
                            hh = rs.uniform(150, 168) * 1100.0 / z
                            col = "#0c0705" if rowX > 400 else "#0a0604"
                            RF(f, "sit_" + hats[rs.randint(len(hats))], pp[0], pp[1], hh, col=col, rim="#C58A44" if side < 0 else "#B07A3A", rimd=(1.0, -0.5) if side < 0 else (-1.0, -0.4),
                               rim2="#7FA0E8", rim2d=(0.0, -1.0), face=-side)
                            z -= rs.uniform(66, 96) * (z / 1300.0)
            if self.monk:
                pm_ = P(0, 0, self.monk_z)
                R.glow(f, pm_[0], pm_[1] - 6, 220 * 1100.0 / self.monk_z, "#FFE2A8", 0.20, sy=0.22)
            # masa + kitaplar
            if self.books:
                pt = P(0, 0, 1290)
                s_ = 1100.0 / 1290.0
                tw, th = 135 * s_, 82 * s_
                top = sk.poly_path([(pt[0] - tw / 2 - 4, pt[1] - th), (pt[0] + tw / 2 + 4, pt[1] - th), (pt[0] + tw / 2, pt[1] - th + 8 * s_), (pt[0] - tw / 2, pt[1] - th + 8 * s_)], True)
                R.lit_path(f, top, "#4a3220", warm_l + [(pt[0], pt[1] - th - 20, 160, "#ffd9a0", 0.25)], rim="#c99c5a", rim_w=1.0)
                R.lit_path(f, R.rect_path(pt[0] - tw / 2, pt[1] - th + 8 * s_, tw, th - 8 * s_), "#2a1a0e", warm_l)
                for k, (col_, bw, bh) in enumerate((("#5a1c18", 52, 12), ("#2a3a2a", 46, 11), ("#4a3018", 50, 12), ("#6a2a1c", 40, 10), ("#2a2030", 44, 11))):
                    PR._book if False else None
                    yb = pt[1] - th - sum(x[2] for x in ((0, 0, 12), (0, 0, 11), (0, 0, 12), (0, 0, 10), (0, 0, 11))[:k]) * s_
                    _book(f, pt[0] + (-4 if k % 2 else 3) * s_, yb, bw * s_, bh * s_, col_, warm_l, ang=(-0.02 if k % 2 else 0.03))
            # avize halkaları
            for (y_, Z_) in ((337, 1500), (306, 1150), (259, 850)):
                s_ = 1100.0 / Z_
                rr = 150 * s_
                f.line(960, -M, 960, y_ - 14, color="#1a120a", sw=3.0)
                f.oval(960, y_, rr, rr * 0.2, style="stroke", sw=max(3, 8 * s_), color="#9a7430")
                f.oval(960, y_, rr * 0.55, rr * 0.11, style="stroke", sw=max(2, 4 * s_), color="#9a7430")
                for i in range(8):
                    a = math.pi * 2 * i / 8
                    cx_, cy_ = 960 + math.cos(a) * rr, y_ + math.sin(a) * rr * 0.2
                    f.rect(cx_ - 3 * s_, cy_ - 24 * s_, 6 * s_, 24 * s_, color="#e9dcb4")

        def L3(f):          # ön plan: yakın bankların karanlık siluetleri
            rs = np.random.RandomState(5)
            for side in (-1, 1):
                for (rowX, z0) in ((330, 640), (470, 700)):
                    pp = P(side * rowX, 0, z0)
                    RF(f, "sit_" + ["beret", "hood", "galero", "cap"][rs.randint(4)], pp[0], pp[1] + 20, 160 * 1100.0 / z0, col="#040201", rim="#8A5A2A", rimd=(1.0 if side < 0 else -1.0, -0.5), face=-side)
            f.rect(-M, H - 60, W + 2 * M, 60 + M, shader=f.lin(0, H - 60, 0, H + M, [("#000000", 0.0, 0), ("#000000", 1.0, 235)]))
            R.vignette_frame(f, 0.7, 0.55)

        return [(0.8, L1), (1.0, L2), (1.3, L3)]

    def dyn(self):
        box = self._box()
        P, YF = _persp(box)
        monk, books, emp = self.monk, self.books, self.emp
        mz = self.monk_z
        PITCH, NWIN, A0, WW = 300.0, 4, 180.0, 170.0
        Zmin = self.ZB - (A0 + (NWIN - 1) * PITCH + WW)
        XL = (self.BACK[0] - self.VP[0]) * self.ZB / 1100.0
        D = (0.78, 0.60, -0.33)
        polys = None

        def D2(f, t):
            nonlocal polys
            if polys is None:
                polys = R.shaft_polys_x(box, XL, (Zmin, YF - 760, Zmin + WW, YF - 250), D, PITCH, NWIN)
            # huzmeler: SABİT ama pişirmede çizilemedi (dyn'de pahalı) → yalnız kıvılcım/toz; huzme L2'de değil burada ucuz çizim yerine statik çokgen kullanılmadı
            pp = P(0, 0, mz)
            if monk:
                ST.figure(f, "monk", pp[0], pp[1], 205 * 1100.0 / mz, col="#0B0705", rim="#E0A15A", face=1, sway=math.sin(t * 0.8) * 0.004, bob=math.sin(t * 1.1) * 0.8)
            R.motes(f, t, (360, 150, 1200, 720), n=44, seed=7, col="#FFE8B8", a=0.5, drift=(6, 4))
            for (y_, Z_) in ((337, 1500), (306, 1150), (259, 850)):
                s_ = 1100.0 / Z_
                rr = 150 * s_
                for i in range(8):
                    a = math.pi * 2 * i / 8
                    R.flame(f, 960 + math.cos(a) * rr, y_ + math.sin(a) * rr * 0.2 - 24 * s_, s=0.75 * s_ + 0.2, t=t, seed=i * 1.3 + Z_, halo=0.4, hr=80 * s_ + 30)

        return {1: D2}


# ═══════════════════════════════════════════════════════════════════════
#  ROAD_NIGHT — gece yolu (Worms→Wartburg, Innsbruck sedye kaçışı)
# ═══════════════════════════════════════════════════════════════════════
def _ridge(x, amp=26.0, base=840.0, slope=0.0):
    """Yol çizgisinin y'si (yumuşak dalgalı tepe sırtı)."""
    return base + amp * math.sin(x / 330.0 + 0.7) + amp * 0.45 * math.sin(x / 117.0) + slope * (x - 960.0)


def _mount_pts(x0, x1, base, amp, seed, step=22, sharp=1.0):
    rs = np.random.RandomState(seed)
    pts = []
    n = int((x1 - x0) / step) + 2
    # fraktal tepe sırası: orta nokta kaydırma
    arr = np.zeros(n)
    h = amp
    arr[0], arr[-1] = rs.rand() * amp * 0.4, rs.rand() * amp * 0.4
    seg = n - 1
    while seg > 1:
        half = seg // 2
        for i in range(0, n - 1, seg):
            j = i + seg
            if j >= n:
                continue
            m = i + half
            arr[m] = (arr[i] + arr[j]) / 2 + (rs.rand() - 0.5) * h
        seg = half
        h *= 0.55 * sharp + 0.2
    arr = arr - arr.min()
    for i in range(n):
        pts.append((x0 + i * step, base - arr[i]))
    return pts


@SL.sc("road_night")
class RoadNight:
    """Gece yolu: tepe sırtında ilerleyen kafile (yandan), ay, dağ/orman siluetleri, meşaleler, isteğe yağmur.
    p: litter=False (sedye + 2 taşıyıcı), riders=3 (0..6 atlı), torches=3 (0..6 meşaleci), rain=0..1 (0), mountains=True (alp zirveleri; False=yumuşak orman tepeleri),
    moon=True, walk=14 (px/sn ilerleme; 0=durağan), x0=None (kafile başı başlangıç x; None=kafile ekranda ortalanır), dir=1 (1: sağa, -1: sola), fog=0.5."""

    def __init__(self, p):
        self.p = p
        self.litter = bool(p.get("litter", False))
        rd, tc, rn = p.get("riders", 3), p.get("torches", 3), p.get("rain", 0.0)
        self.riders = (3 if rd else 0) if isinstance(rd, bool) else int(rd)
        self.torches = (3 if tc else 0) if isinstance(tc, bool) else int(tc)
        self.rain = (0.6 if rn else 0.0) if isinstance(rn, bool) else float(rn)
        self.mount = p.get("mountains", True)
        self.moon = p.get("moon", True)
        self.walk = float(p.get("walk", 14.0))
        self.x0 = p.get("x0")
        self.dir = 1 if p.get("dir", 1) >= 0 else -1
        self.fog = float(p.get("fog", 0.5))

    def _group(self):
        """Kafile sırası (baştan sona): [(tür, ofset_px, boy_px)] — ofset kafile başından geriye doğru."""
        seq = []
        riders, torches = self.riders, self.torches
        if self.litter:
            seq += [("torch", 0, 250), ("rider", 1, 400)] if riders else [("torch", 0, 250)]
            seq += [("torch", 2, 250)] if torches > 1 else []
            seq += [("bearer", 3, 220), ("litter", 4, 220), ("bearer", 5, 220)]
            for i in range(max(0, riders - 1)):
                seq.append(("rider", 6 + i, 400))
            for i in range(max(0, torches - 2)):
                seq.append(("torch", 7 + i, 250))
        else:
            order = []
            ri, ti = riders, torches
            while ri > 0 or ti > 0:
                if ri > 0:
                    order.append(("rider", 400)); ri -= 1
                if ti > 0:
                    order.append(("torch", 250)); ti -= 1
            for i, (k, h) in enumerate(order):
                seq.append((k, i, h))
        # px konumları
        out = []
        x = 0.0
        for k, i, h in seq:
            gap = {"rider": 330, "torch": 170, "bearer": 150, "litter": 420}[k]
            out.append((k, x, h))
            x += gap
        return out

    def layers(self):
        mount, moon, rain, fog = self.mount, self.moon, self.rain, self.fog
        litter = self.litter

        def L0(f):          # gökyüzü
            top, mid, hor = ("#04060c", "#0b1424", "#1c2c48") if rain < 0.5 else ("#06080c", "#0e131c", "#1d2735")
            f.rect(-M, -M, W + 2 * M, H + 2 * M, shader=f.lin(0, -M, 0, 760, [(top, 0.0), (mid, 0.55), (hor, 1.0)]))
            rs = np.random.RandomState(3)
            if rain < 0.6:
                for i in range(110):
                    f.circle(rs.uniform(-M, W + M), rs.uniform(-M, 520), 0.7 + rs.rand() * 1.1, color="#DDE8FF", alpha=0.15 + 0.5 * rs.rand() * (1 - rain))
            if moon:
                mx, my, mr = 1450, 230, 62
                R.glow(f, mx, my, mr * 9, "#6f93d0", 0.30 * (1 - 0.5 * rain))
                R.glow(f, mx, my, mr * 3.6, "#b8cdf2", 0.45 * (1 - 0.6 * rain))
                f.circle(mx, my, mr, shader=f.rad(mx - mr * 0.25, my - mr * 0.25, mr * 1.4, [("#ffffff", 0.0), ("#e5edfb", 0.6), ("#b4c3df", 1.0)]), alpha=1 - 0.5 * rain)
                rm = np.random.RandomState(9)
                for i in range(8):
                    ang, rad = rm.rand() * 6.28, rm.rand() * mr * 0.7
                    f.circle(mx + math.cos(ang) * rad, my + math.sin(ang) * rad, mr * (0.1 + 0.16 * rm.rand()), color="#8E9DBA", alpha=0.22)
            # bulutlar
            nc = 8 + int(10 * rain)
            for i in range(nc):
                cx_, cy_ = rs.uniform(-M, W + M), rs.uniform(60, 560)
                w_, h_ = rs.uniform(260, 700), rs.uniform(26, 70)
                a = rs.uniform(0.3, 0.6) + 0.35 * rain
                pa = skia.Paint(AntiAlias=True, Color=C("#070b14" if rain < 0.5 else "#0b0f16", int(255 * min(0.95, a))), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
                f.c.drawOval(skia.Rect.MakeLTRB(cx_ - w_, cy_ - h_, cx_ + w_, cy_ + h_), pa)
                if moon and rain < 0.7:
                    pa2 = skia.Paint(AntiAlias=True, Color=C("#8FA9D8", 34), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
                    f.c.drawOval(skia.Rect.MakeLTRB(cx_ - w_ * 0.85, cy_ - h_ * 1.1, cx_ + w_ * 0.8, cy_ - h_ * 0.05), pa2)

        def L1(f):          # uzak dağlar
            if mount:
                for (base, amp, seed, col, a_hi) in ((640, 330, 4, "#16233a", 0.5), (700, 250, 7, "#0f1a2d", 0.35)):
                    pts = _mount_pts(-M, W + M, base, amp, seed, step=18, sharp=1.2)
                    path = sk.poly_path(pts + [(W + M, H + M), (-M, H + M)], True)
                    f.path(path, shader=f.lin(0, base - amp, 0, base + 60, [(mix(col, "#2a3f66", 0.45), 0.0), (col, 0.6), (mix(col, "#05080f", 0.4), 1.0)]))
                    f.path(sk.poly_path(pts, False), style="stroke", sw=1.4, color="#a5bde6", alpha=a_hi * 0.35 * (1 if moon else 0.4))
                    # ay ışıklı yamaçlar: sağa bakan (inen) kenarlar boyunca açık dolgu şeritleri
                    for i in range(0, len(pts) - 1):
                        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
                        if yb > ya + 2 and ya < base - amp * 0.35:
                            q = [(xa, ya), (xb, yb), (xb - 6, yb + (yb - ya) * 1.8 + 14), (xa - 6, ya + 22)]
                            soft_ = skia.Paint(AntiAlias=True, Color=C("#cfe0fa", int(255 * 0.13 * (1 if moon else 0.3))), BlendMode=skia.BlendMode.kPlus)
                            f.c.drawPath(sk.poly_path(q, True), soft_)
            else:
                for (base, amp, seed, col) in ((690, 90, 5, "#111c30"), (740, 70, 8, "#0c1626")):
                    pts = [(xx, base + math.sin(xx * 0.004 + seed) * amp + math.sin(xx * 0.011 + seed * 2) * amp * 0.4) for xx in range(-M, W + M + 40, 40)]
                    f.path(sk.poly_path(pts + [(W + M, H + M), (-M, H + M)], True), color=col)
                    f.path(sk.poly_path(pts, False), style="stroke", sw=2.0, color="#8ea8d4", alpha=0.25)
            # alçak sis
            f.rect(-M, 640, W + 2 * M, 200, shader=f.lin(0, 640, 0, 840, [("#7d93bd", 0.0, 0), ("#7d93bd", 1.0, int(60 + 80 * fog))]))

        def L2(f):          # orta plan: orman tepeleri
            for (base, amp, seed, col, y_p, hp, dn) in ((770, 60, 11, "#0a121f", 770, 120, 34), (820, 40, 13, "#070c15", 820, 150, 40)):
                pts = [(xx, base + math.sin(xx * 0.006 + seed) * amp + math.sin(xx * 0.017 + seed * 1.7) * amp * 0.35) for xx in range(-M, W + M + 40, 40)]
                f.path(sk.poly_path(pts + [(W + M, H + M), (-M, H + M)], True), color=col)
                ST.pines(f, -M, W + M, base + amp * 0.2, hp, col, seed=seed, dens=dn)
                f.path(sk.poly_path(pts, False), style="stroke", sw=1.6, color="#7f9bd0", alpha=0.18 if moon else 0.06)
            f.rect(-M, 780, W + 2 * M, 160, shader=f.lin(0, 780, 0, 940, [("#6f86b0", 0.0, 0), ("#6f86b0", 1.0, int(50 + 70 * fog))]))

        def L3(f):          # yol sırtı (kafile burada yürür)
            pts = [(xx, _ridge(xx)) for xx in range(-M, W + M + 30, 30)]
            ground = sk.poly_path(pts + [(W + M, H + M), (-M, H + M)], True)
            f.path(ground, shader=f.lin(0, 800, 0, 1100, [("#121a2a", 0.0), ("#080b13", 0.5), ("#04060a", 1.0)]))
            # yol bandı (ay ışıklı ıslak toprak)
            band = [(x, y + 6) for x, y in pts] + [(x, y + 42) for x, y in reversed(pts)]
            f.path(sk.poly_path(band, True), shader=f.lin(0, 760, 0, 880, [("#2c3b57", 0.0, 150), ("#16202f", 1.0, 150)]))
            f.path(sk.poly_path(pts, False), style="stroke", sw=2.4, color="#8ea8d4", alpha=0.32 if moon else 0.1)
            rs = np.random.RandomState(8)
            for i in range(22):         # su birikintileri
                x = rs.uniform(-100, W + 100)
                y = _ridge(x) + rs.uniform(14, 36)
                wd = rs.uniform(30, 90)
                f.oval(x, y, wd, 3.2, color="#a6bde6" if moon else "#58667f", alpha=0.35 if moon else 0.2)
            # kaya/çalı
            for i in range(14):
                x = rs.uniform(-150, W + 150)
                y = _ridge(x) + rs.uniform(40, 120)
                f.oval(x, y, rs.uniform(18, 52), rs.uniform(8, 22), color="#04060a")

        def L4(f):          # ön plan: kara yamaç + iri çam siluetleri
            pts = [(xx, 1010 + math.sin(xx * 0.005) * 28) for xx in range(-M, W + M + 40, 40)]
            f.path(sk.poly_path(pts + [(W + M, H + M), (-M, H + M)], True), color="#020305")
            for (x, hh, seed) in ((70, 520, 2), (1840, 600, 5), (-120, 700, 9), (2040, 460, 11)):
                ST.pines(f, x - 90, x + 90, 1040, hh, "#020305", seed=seed, dens=120)
            rsg = np.random.RandomState(4)
            for i in range(120):             # ön plan ot/çalı kılıçları
                x = rsg.uniform(-M, W + M)
                y = 1030 + math.sin(x * 0.005) * 28 + rsg.uniform(-8, 20)
                hgt = rsg.uniform(30, 110)
                f.poly([(x - 4, y + 10), (x + rsg.uniform(-14, 14), y - hgt), (x + 5, y + 10)], color="#020305")
            for (x, w_, h_) in ((260, 130, 60), (1500, 170, 80), (980, 90, 40)):
                f.oval(x, 1060, w_, h_, color="#020305")
                f.oval(x - w_ * 0.25, 1060 - h_ * 0.7, w_ * 0.5, h_ * 0.18, color="#5e7aa8", alpha=0.10 if moon else 0.03)
            f.rect(-M, 940, W + 2 * M, 140 + M, shader=f.lin(0, 940, 0, 1080 + M, [("#000000", 0.0, 0), ("#000000", 1.0, 200)]))
            R.vignette_frame(f, 0.7, 0.5)

        return [(0.04, L0), (0.2, L1), (0.5, L2), (1.0, L3), (1.4, L4)]

    def dyn(self):
        grp = self._group()
        walk, dr = self.walk, self.dir
        Lg = (grp[-1][1] if grp else 0.0)
        x0 = self.x0 if self.x0 is not None else (960.0 + dr * Lg / 2.0 - dr * 100.0)
        rain = self.rain
        moon = self.moon
        litter = self.litter

        def D3(f, t):
            xl = x0 + walk * t * dr          # kafile başı
            place = []
            for idx, (k, off, hh) in enumerate(grp):
                x = xl - off * dr
                y = _ridge(x) + 34
                tilt = math.atan2(_ridge(x + 6) - _ridge(x - 6), 12.0) * 0.8 * dr
                ph = t * 3.0 + idx * 1.3
                bob = abs(math.sin(ph)) * -3.5 if walk > 0.1 else 0
                place.append((idx, k, x, y, hh, tilt, bob))
            # 1) meşale parıltıları (figürlerin ARKASINDA kalsın)
            for (idx, k, x, y, hh, tilt, bob) in place:
                if k == "torch":
                    R.glow(f, x + 40 * dr, y - hh * 0.30, hh * 1.0, "#FF9A3A", 0.12, sy=0.8)
            # 2) figürler
            rimd = (-0.5 * dr, -1.0)
            rc = "#9db6dc" if moon else "#6f84a8"
            for (idx, k, x, y, hh, tilt, bob) in place:
                if k == "rider":
                    RF(f, "horse_rider", x, y, hh, rim=rc, rimd=rimd, rim2="#E0A15A", rim2d=(1.0 * dr, 0.1), face=dr, bob=bob * 0.6)
                elif k == "torch":
                    RF(f, "torchbearer", x, y, hh, rim=rc, rimd=rimd, rim2="#FFB35A", rim2d=(1.0 * dr, -0.2), face=dr, bob=bob)
                elif k == "bearer":
                    RF(f, "bearer", x, y, hh, rim=rc, rimd=rimd, rim2="#E0A15A", rim2d=(1.0 * dr, 0.0), face=dr, bob=bob)
                elif k == "litter":
                    RF(f, "litter", x, y, hh, rim=rc, rimd=rimd, rim2="#E0A15A", rim2d=(1.0 * dr, 0.0), face=dr, bob=bob * 0.9)
            # 3) alevler/kıvılcımlar (en üstte)
            tip = R.TORCH_TIP["torchbearer"]
            for (idx, k, x, y, hh, tilt, bob) in place:
                if k == "torch":
                    fx, fy = x + tip[0] * hh * dr, y + bob + tip[1] * hh
                    R.flame(f, fx, fy + 6, s=1.4, t=t, seed=idx * 1.7, halo=1.0, hr=170, col_out="#FF8A24")
                    R.embers_lite(f, t, fx, fy - 20, n=8, seed=idx + 3, rise=70)
            if rain > 0.02:
                sk.rain(f, t, n=int(110 + 160 * rain), seed=8, angle=-0.28, length=34 + 20 * rain, alpha=0.20 + 0.22 * rain, speed=1500)
            else:
                R.motes(f, t, (200, 500, 1500, 400), n=10, seed=2, col="#FFB060", a=0.35, drift=(8, -6))

        def D4(f, t):
            if rain > 0.02:
                sk.rain(f, t, n=int(70 + 120 * rain), seed=21, angle=-0.30, length=70 + 30 * rain, alpha=0.18 + 0.2 * rain, speed=1900, color="#a8bed4")

        return {3: D3, 4: D4}


# ═══════════════════════════════════════════════════════════════════════
#  CLOISTER — Yuste manastır avlusu
# ═══════════════════════════════════════════════════════════════════════
@SL.sc("cloister")
class Cloister:
    """Yuste avlusu: iki katlı kemerli galeri (karşı kanat + yan kanatlar, perspektif), ortada çim parter + çeşme, selviler, turuncu ağaçlar,
    galeride yanan lambalar, gezinen keşişler.
    p: time="dusk"|"day"|"night" (dusk), monks=1 (0..3 yürüyen keşiş), lamps=True (galeri kemerlerinde lamba ışığı), walk=1.0 (keşiş hız çarpanı)."""

    BACK = (330, 300, 1590, 880)
    VP = (960, 600)
    ZB = 1500.0
    BAY = 335.0
    LO = (250.0, 215.0, 26.0, 330.0)
    GAL = (150.0, 470.0, 18.0, 575.0)

    def __init__(self, p):
        self.p = p
        self.time = p.get("time", "dusk")
        self.monks = int(p.get("monks", 1))
        self.lamps = p.get("lamps", True)
        self.walk = float(p.get("walk", 1.0))

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    def _glow_prob(self):
        if not self.lamps:
            return 0.0
        return {"day": 0.0, "dusk": 0.40, "night": 0.55}.get(self.time, 0.4)

    def _lamp_bays(self):
        pr = self._glow_prob()
        out = []
        if pr <= 0:
            return out
        for k in range(-6, 7):
            if R.hash2(np.array([k]), np.array([1]), 5 + 77)[0] < pr:
                X = (k + 0.5) * self.BAY
                out.append(960 + X * 1100.0 / self.ZB)
        return out

    def layers(self):
        box = self._box()
        tm = self.time
        cache = {}
        fb = (self.BACK[3] - self.VP[1]) * self.ZB / 1100.0
        gp = self._glow_prob()
        lamp_x = self._lamp_bays()

        def room():
            if "r" in cache:
                return cache["r"]
            st = {"day": ("#c8b895", "#b3a283", "#d6c8a8"), "dusk": ("#a89674", "#8f7f64", "#b6a684"), "night": ("#8a7c64", "#756a56", "#968a72")}[tm]
            arc = R.mat_arcade(fb, stone=st[0], brick=st[1], white=st[2], bay=self.BAY, lo=self.LO, gal=self.GAL, seed=6, recess="#0b0907",
                               glow_prob=gp, glow=(1.0, 0.62, 0.30), glow_power=1.3)
            floor = R.mat_garden(bed=(-520.0, 520.0, 170.0, 720.0), seed=11)
            mats = dict(back=arc, left=arc, right=arc, floor=floor, ceil=arc)
            amb = {"day": (0.12, 0.12, 0.13), "dusk": (0.052, 0.046, 0.062), "night": (0.012, 0.015, 0.030)}[tm]
            D = {"day": (-0.45, 0.75, -0.48), "dusk": (-0.62, 0.40, -0.45), "night": (0.40, 0.70, -0.55)}[tm]
            col, pw = {"day": ((1.0, 0.90, 0.70), 1.6), "dusk": ((1.0, 0.52, 0.28), 1.1), "night": ((0.40, 0.56, 0.96), 0.75)}[tm]
            moon = R.Moon(D, col=col, power=pw, win=None)
            lights = []
            for lx in lamp_x:
                lights.append(R.Light((lx, 560, self.ZB + 60), (1.0, 0.62, 0.30), 0.9, 230))
            rgb, cov = box.render(mats, lights, moon=moon, ambient=amb, expo=1.2, ao=0.55, only=("back", "left", "right", "floor"))
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L0(f):          # gökyüzü + çatı arkasındaki çan kulesi
            if tm == "day":
                f.rect(-M, -M, W + 2 * M, 900, shader=f.lin(0, -M, 0, 640, [("#5f8fbd", 0.0), ("#9dbfd8", 0.65), ("#e6ddc4", 1.0)]))
                R.glow(f, 380, 160, 360, "#fff2c0", 0.55)
                rs = np.random.RandomState(4)
                for i in range(7):
                    cx_, cy_ = rs.uniform(-M, W + M), rs.uniform(40, 360)
                    f.c.drawOval(skia.Rect.MakeLTRB(cx_ - 300, cy_ - 34, cx_ + 300, cy_ + 34), skia.Paint(AntiAlias=True, Color=C("#ffffff", 120), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)))
            elif tm == "dusk":
                f.rect(-M, -M, W + 2 * M, 900, shader=f.lin(0, -M, 0, 640, [("#171c3d", 0.0), ("#6a3558", 0.5), ("#d9763a", 0.88), ("#f3a85c", 1.0)]))
                R.glow(f, 1500, 330, 520, "#ff9a4a", 0.45, sy=0.55)
                rs = np.random.RandomState(5)
                for i in range(7):
                    cx_, cy_ = rs.uniform(-M, W + M), rs.uniform(140, 440)
                    f.c.drawOval(skia.Rect.MakeLTRB(cx_ - 320, cy_ - 22, cx_ + 320, cy_ + 22), skia.Paint(AntiAlias=True, Color=C("#ff8a50", 90), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20)))
                for i in range(40):
                    f.circle(rs.uniform(-M, W + M), rs.uniform(-M, 220), 1.0 + rs.rand(), color="#ffe8d0", alpha=0.5 * rs.rand())
            else:
                R.night_sky(f, moon=(520, 160, 30), y_h=620, stars=110, seed=14, clouds=True)
            # çan kulesi + çatılar (siluet)
            col = "#0d0a0c" if tm != "day" else "#6a5a4a"
            f.rect(250, 70, 130, 260, color=col)
            f.poly([(238, 70), (315, -20), (392, 70)], color=col)
            f.rect(300, 120, 30, 60, color="#05040a" if tm != "day" else "#3a2f26")
            if tm != "day":
                f.rect(305, 128, 20, 40, color="#ffb85a", alpha=0.6 if tm == "dusk" else 0.9)
            f.rect(1330, 150, 200, 190, color=col)
            f.poly([(1320, 150), (1430, 70), (1540, 150)], color=col)

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # karşı kanat çatısı (kiremit)
            x0, y0, x1, y1 = self.BACK
            roof_col = {"day": "#8a4a30", "dusk": "#5a3028", "night": "#2a1a1c"}[tm]
            rp = sk.poly_path([(x0 - 36, y0 + 6), (x1 + 36, y0 + 6), (x1 + 10, y0 - 86), (x0 - 10, y0 - 86)], True)
            R.lit_path(f, rp, roof_col, [(960, y0 - 40, 900, {"day": "#fff0c8", "dusk": "#ff9a4a", "night": "#6f93d0"}[tm], 0.18)], grad=f.lin(0, y0 - 86, 0, y0 + 6, [(shade_(roof_col, -0.25), 0.0), (roof_col, 0.6), (shade_(roof_col, -0.5), 1.0)]))
            for i in range(1, 6):
                yy = y0 - 86 + i * 15.3
                f.line(x0 - 36 + (86 - i * 15.3) * 0.28, yy, x1 + 36 - (86 - i * 15.3) * 0.28, yy, color="#000000", sw=1.6, alpha=0.35)
            for i in range(int((x1 - x0) / 34)):
                f.line(x0 + i * 34, y0 - 86 + 8, x0 + i * 34 - 10, y0 + 4, color="#000000", sw=1.0, alpha=0.22)
            f.rect(x0 - 40, y0 + 4, x1 - x0 + 80, 10, color=shade_(roof_col, -0.5))

        def L2(f):          # bahçe: selviler, ağaçlar, çeşme
            skyc = {"day": "#e8d8a8", "dusk": "#ff9a5a", "night": "#7fa0e0"}[tm]
            rim_a = {"day": 0.30, "dusk": 0.55, "night": 0.45}[tm]
            lt = [(960, 960, 520, {"day": "#fff0c8", "dusk": "#ff9a4a", "night": "#6f93d0"}[tm], 0.10)]
            # çeşme
            PR.fountain(f, 960, 975, 1.0, stone="#5a5046" if tm != "day" else "#8a7e6a", lights=lt)
            # turuncu ağaçlar (yuvarlak taçlı)
            for (x, y, s_, seed) in ((700, 940, 1.0, 3), (1230, 940, 1.0, 8)):
                f.rect(x - 7 * s_, y - 70 * s_, 14 * s_, 70 * s_, color="#120c08")
                rs = np.random.RandomState(seed)
                for i in range(46):
                    ang, rad = rs.rand() * 6.28, rs.rand() ** 0.6 * 78 * s_
                    cx_, cy_ = x + math.cos(ang) * rad * 1.1, y - 128 * s_ + math.sin(ang) * rad * 0.9
                    f.circle(cx_, cy_, rs.uniform(18, 30) * s_, color="#0f1a0e" if i % 3 else "#16240f")
                for i in range(9):
                    f.circle(x + rs.uniform(-70, 70) * s_, y - 128 * s_ + rs.uniform(-60, 50) * s_, 4.2 * s_, color="#d98a2a" if tm != "night" else "#6a4a1a", alpha=0.95)
                f.path(sk.smooth_path([(x - 96 * s_, y - 124 * s_), (x, y - 214 * s_), (x + 96 * s_, y - 124 * s_)], False, 0.5), style="stroke", sw=1.6, color=skyc, alpha=rim_a * 0.6)
            # selviler
            for (x, y, h_, seed, d_) in ((470, 930, 520, 1, 1), (1480, 930, 560, 2, -1), (590, 900, 330, 5, 1), (1370, 900, 360, 6, -1)):
                PR.cypress(f, x, y, h_, seed=seed, rim=skyc, rim_a=rim_a, rim_dir=d_)
            _shadow_ellipse(f, 960, 985, 260, 14, 0.5, 14)

        def L3(f):          # ön plan: yakın galeri sütunları
            for sx in (-1, 1):
                x = W / 2 + sx * 1000
                col = R.rect_path(x - 80, -M, 160, H + 2 * M)
                R.lit_path(f, col, "#2a2016", [(W / 2 + sx * 640, 600, 700, {"day": "#fff0c8", "dusk": "#ff9a4a", "night": "#6f93d0"}[tm], 0.10)],
                           grad=f.lin(x - 80, 0, x + 80, 0, [("#0b0705", 0.0), ("#3a2c1e", 0.5), ("#0b0705", 1.0)]))
                f.rect(x - 112, 80, 224, 34, color="#0b0705")
                f.rect(x - 96, 114, 192, 10, color="#14100c")
            R.vignette_frame(f, 0.7 if tm != "day" else 0.45, 0.55)

        return [(0.06, L0), (0.85, L1), (1.0, L2), (1.4, L3)]

    def dyn(self):
        tm = self.time
        monks = self.monks
        walk = self.walk
        lamp_x = self._lamp_bays()

        def D2(f, t):
            # galeri lambaları (titreşen parıltı)
            for i, lx in enumerate(lamp_x):
                fl = R.flicker(t, i * 1.7, 0.6)
                R.glow(f, lx, 545, 70 * fl, "#FFB060", 0.20)
            # keşişler
            specs = [(0.00, 1, 22), (0.55, -1, 17), (0.30, 1, 12)]
            for i in range(min(3, monks)):
                ph, dr, spd = specs[i]
                span = 1000.0
                u = (ph * span + walk * spd * t) % span
                x = 440 + u if dr > 0 else 1440 - u
                y = 905 + (1 if i == 1 else 0) * 24
                hh = 150 + 14 * (1 if i == 1 else 0)
                bob = abs(math.sin(t * 2.6 + i)) * -2.5
                if tm == "night" and i == 0:
                    R.glow(f, x + dr * 40, y - hh * 0.45, 120, "#FFA848", 0.22)
                ST.figure(f, "monk", x, y, hh, col="#0B0705", rim="#C58A44" if tm != "day" else "#6a5a44", face=dr, sway=math.sin(t * 2.6 + i) * 0.006, bob=bob)
                if tm == "night" and i == 0:
                    R.flame(f, x + dr * 52, y - hh * 0.36, s=0.9, t=t, seed=3.3, halo=0.6, hr=90)
            if tm != "day":
                R.motes(f, t, (420, 520, 1100, 420), n=18, seed=3, col="#FFD9A0" if tm == "dusk" else "#BFD2FF", a=0.4, drift=(3, -2))

        return {2: D2}


# ═══════════════════════════════════════════════════════════════════════
#  BEDROOM — Yuste yatak odası
# ═══════════════════════════════════════════════════════════════════════
_SIDE = {}


def _pkey(scene, p):
    return scene + repr(sorted((k, v) for k, v in p.items() if isinstance(v, (str, int, float, bool, tuple))))


def _drape(f, x0, y0, x1, y1, col="#5a1a20", lights=(), folds=7, trim="#c9962b", sx=1):
    """Dikey perde (kıvrımlı): dikdörtgen üstüne gradyanlı dikey kıvrım şeritleri."""
    p = sk.poly_path([(x0, y0), (x1, y0), (x1 + sx * 10, y1), (x0 - sx * 6, y1)], True)
    R.lit_path(f, p, col, lights, grad=f.lin(x0, 0, x1, 0, [(shade_(col, -0.45), 0.0), (shade_(col, 0.1), 0.25), (shade_(col, -0.5), 0.45), (shade_(col, 0.08), 0.7), (shade_(col, -0.5), 1.0)]))
    f.c.save()
    f.c.clipPath(p, skia.ClipOp.kIntersect, True)
    for k in range(folds):
        xx = x0 + (x1 - x0) * (k + 0.5) / folds
        f.line(xx, y0, xx + sx * 6, y1, color="#000000", sw=2.5, alpha=0.3)
    f.c.restore()
    f.line(x0, y0 + 2, x1, y0 + 2, color=trim, sw=2.0, alpha=0.7)


@SL.sc("bedroom")
class Bedroom:
    """Yuste yatak odası: baldaken yatak (kırmızı perdeler), yastıklara yaslanmış hasta yaşlı adam, komodinde mum + yemek tepsisi, ay ışıklı küçük pencere, haç.
    p: candle=1.0 (0..1.4 alev boyutu/ışığı; 0=mum yok), fade_candle_t=None|(t0,t1) yerel sn'de mum söner (oda soğuk aya kalır, duman çıkar),
    patient=True (hasta figürü), food=True, moon=1.0 (pencere ay ışığı)."""

    BACK = (300, 70, 1620, 880)
    VP = (960, 500)
    ZB = 1200.0
    WIN = (1290, 190, 1450, 470)
    T, SPL = 140.0, 0.82
    CANDLE = (1270, 628)

    def __init__(self, p):
        self.p = p
        self.candle = float(p.get("candle", 1.0))
        self.fade = p.get("fade_candle_t")
        self.patient = p.get("patient", True)
        self.food = p.get("food", True)
        self.moonk = float(p.get("moon", 1.0))

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    def layers(self):
        box = self._box()
        cache = {}
        outer = box.hole_outer(self.WIN, self.T, self.SPL)
        zw = box.zb + self.T
        cx_, cy_ = self.CANDLE
        key = _pkey("bedroom", self.p)
        need_dark = self.fade is not None

        def render(candle_on):
            plaster = R.mat_plaster("#62564a", seed=5, rough=0.35, stain=0.4, tone=0.08)
            wood = R.mat_planks("#34221a", seed=8, pw=120, plen=2400, tone=0.14)
            b0 = (880 - 170 - 500) * self.ZB / 1100.0 * 1.0
            wall = R.mat_split(plaster, wood, b0, trim="#8a6a3a")
            floor = R.mat_planks("#3f2c1e", seed=3, pw=110, plen=700, tone=0.18)
            ceil = R.mat_beams("#2a1c11", seed=7, pitch=280, bwid=80, plaster="#6a5d4e", axis="a")
            mats = dict(back=wall, left=wall, right=wall, floor=floor, ceil=ceil)
            lights = []
            if candle_on and self.candle > 0.01:
                lights.append(R.Light((cx_, cy_ - 4, 1060), R.warm(1.0), 2.6 * min(1.2, self.candle + 0.2), 300, spec=0.5, far=(620, (0.55, 0.20, 0.05), 0.12)))
            moon = None
            ox0, oy0, ox1, oy1 = outer
            if self.moonk > 0:
                g = R.window_gobo(box, outer, zw, xs=[(ox0 + ox1) / 2], bar_w=7, ys=[(oy0 + oy1) / 2], bar_hw=7)
                moon = R.Moon((-0.30, 0.85, -0.42), col=(0.42, 0.58, 1.0), power=1.5 * self.moonk, win=g, pen=4.0, pen_k=0.012)
                lights.append(R.Light(((ox0 + ox1) / 2, (oy0 + oy1) / 2 + 30, zw - 90), (0.30, 0.42, 0.78), 0.8 * self.moonk, 320))
            amb = (0.007, 0.008, 0.015) if candle_on else (0.005, 0.0065, 0.014)
            return box.render(mats, lights, moon=moon, ambient=amb, expo=1.25, ao=0.55, holes=[dict(rect=self.WIN, T=self.T, splay=self.SPL, mat=wood, ao=0.25)])

        def room():
            if "r" in cache:
                return cache["r"]
            cache["r"] = render(True)
            return cache["r"]

        def L0(f):
            R.night_sky(f, moon=(1390, 250, 20), y_h=520, stars=70, seed=17, clouds=True)
            # uzakta kilise/avlu çatıları
            f.rect(-M, 470, W + 2 * M, 300, color="#04070d")
            f.rect(1330, 380, 70, 120, color="#05080f")
            f.poly([(1322, 380), (1365, 330), (1408, 380)], color="#05080f")
            R.glow(f, 1365, 440, 40, "#ffb060", 0.35)

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            x0, y0, x1, y1 = outer
            PR.lattice(f, outer, step=24, col="#0b0907", sw=2.6, alpha=0.9, frame="#1a120b")
            # duvarda haç (duvarla birlikte)
            f.rect(594, 232, 14, 110, color="#1a110a")
            f.rect(566, 262, 70, 12, color="#1a110a")
            f.line(601, 234, 601, 340, color="#9a7a48", sw=1.0, alpha=0.4)

        def L2(f):
            lights = []
            if self.candle > 0.01:
                lights.append((cx_, cy_ + 30, 360, "#ff9c40", 0.55 * min(1.2, self.candle + 0.2)))
            self._props(f, lights)

        def L3(f):
            f.rect(-M, -M, 150 + M, H + 2 * M, shader=f.lin(-M, 0, 150, 0, [("#000000", 0.0, 240), ("#000000", 1.0, 0)]))
            f.rect(W - 120, -M, 120 + M, H + 2 * M, shader=f.lin(W - 120, 0, W + M, 0, [("#000000", 0.0, 0), ("#000000", 1.0, 230)]))
            R.vignette_frame(f, 0.72, 0.52)

        layers = [(0.1, L0), (0.85, L1), (1.0, L2), (1.38, L3)]
        if need_dark:
            def bake_dark():
                rgb, cov = render(False)
                f = sk.Frame(CW_, CH_)
                f.clear(skia.ColorTRANSPARENT)
                f.c.translate(M, M)
                R.draw_np(f, rgb, cov)
                _SIDE[key] = f.surf.makeImageSnapshot()
            bake_dark()
        return layers

    # -- eşyalar
    def _props(self, f, lights):
        cx_, cy_ = self.CANDLE
        # yatak (uzun kenarı bize dönük, baş solda)
        yb = 905
        # arka gölge
        _shadow_ellipse(f, 700, yb + 6, 420, 24, 0.6, 18)
        # perde direkleri + tavan çerçevesi (baldaken)
        for x in (356, 1044):
            post = R.rect_path(x - 15, 150, 30, yb - 150)
            R.lit_path(f, post, "#2e1b0e", lights, rim="#9a7440", rim_w=1.0, grad=f.lin(x - 15, 0, x + 15, 0, [("#120a05", 0.0), ("#4a2e18", 0.45), ("#120a05", 1.0)]))
            for q in range(8):
                f.line(x - 14, 190 + q * 90, x + 14, 205 + q * 90, color="#000000", sw=2, alpha=0.25)
            f.circle(x, 148, 20, color="#c9962b", alpha=0.85)
        tester = R.rect_path(330, 156, 740, 34)
        R.lit_path(f, tester, "#2a190d", lights, rim="#c9962b", rim_w=1.4)
        val = sk.poly_path([(335, 190), (1065, 190), (1065, 236)] + [(1065 - i * 40.5, 236 + (10 if i % 2 else 0)) for i in range(1, 19)] + [(335, 236)], True)
        R.lit_path(f, val, "#6a1a22", lights, grad=f.lin(0, 190, 0, 246, [("#7a2028", 0.0), ("#4a1218", 1.0)]))
        for i in range(19):
            f.line(335 + i * 40.5, 242, 335 + i * 40.5, 252, color="#c9962b", sw=2, alpha=0.7)
        # perdeler (iki yanda toplanmış)
        _drape(f, 336, 236, 440, yb - 4, "#5a1a20", lights, folds=6, sx=1)
        _drape(f, 960, 236, 1064, yb - 4, "#5a1a20", lights, folds=6, sx=-1)
        # arka başlık ve ayak ucu
        head = sk.poly_path([(366, yb - 70), (366, 330), (380, 300), (420, 296), (440, 330), (440, yb - 70)], True)
        R.lit_path(f, head, "#2e1b0e", lights, rim="#8a6a3a", rim_w=1.0)
        # yatak çerçevesi (yan yüz) + ayaklar
        rail = R.rect_path(360, 806, 690, 40)
        R.lit_path(f, rail, "#2a190d", lights, rim="#9a7440", rim_w=1.0, grad=f.lin(0, 806, 0, 846, [("#4a2e18", 0.0), ("#1a0e06", 1.0)]))
        for x in (372, 1030):
            R.lit_path(f, R.rect_path(x - 12, 846, 24, yb - 846), "#1a0e06", lights)
        # şilte/keten + yastıklar
        lin = sk.smooth_path([(372, 806), (380, 744), (470, 720), (700, 726), (880, 730), (1030, 744), (1040, 806)], True, 0.45)
        R.lit_path(f, lin, "#a79e86", lights + [(cx_ - 100, 740, 420, "#ffd9a0", 0.30)], rim=None,
                   grad=f.lin(0, 720, 0, 806, [("#c8bfa4", 0.0), ("#8c826c", 1.0)]))
        for (px, py, rot, w_) in ((440, 650, -0.26, 190), (500, 700, -0.10, 170)):
            f.c.save()
            f.c.translate(px, py)
            f.c.rotate(math.degrees(rot))
            pil = sk.smooth_path([(-w_ / 2, 0), (-w_ * 0.4, -52), (0, -62), (w_ * 0.4, -50), (w_ / 2, 0), (w_ * 0.4, 44), (0, 56), (-w_ * 0.4, 46)], True, 0.5)
            R.lit_path(f, pil, "#b8af96", lights + [(cx_ - 600, 700, 500, "#ffd9a0", 0.35)], rim="#e8dcc0", rim_w=1.0,
                       grad=f.lin(0, -62, 0, 56, [("#d6cdb2", 0.0), ("#8e856f", 1.0)]))
            f.c.restore()
        # hasta yaşlı adam (bust figürü) burada çizilir (statik) — nefes dyn'de
        # battaniye (kırmızı-altın yorgan), hasta bacak şişkin
        blk = sk.smooth_path([(560, 806), (566, 752), (640, 736), (760, 742), (880, 738), (975, 726), (1034, 744), (1042, 806)], True, 0.5)
        R.lit_path(f, blk, "#5a1a20", lights + [(cx_ - 120, 760, 380, "#ffb060", 0.45)], rim="#c9962b", rim_w=1.2,
                   grad=f.lin(0, 726, 0, 806, [("#8a2630", 0.0), ("#4a1218", 1.0)]))
        for k in range(7):
            f.line(600 + k * 62, 744 + (k % 2) * 3, 592 + k * 62, 804, color="#000000", sw=2.2, alpha=0.28)
        f.line(566, 770, 1040, 760, color="#c9962b", sw=2.0, alpha=0.5)
        # hasta bacağı için minder
        cush = sk.smooth_path([(930, 744), (960, 716), (1018, 714), (1038, 740), (1000, 760)], True, 0.5)
        R.lit_path(f, cush, "#7a6a50", lights, rim="#d8c8a0", rim_w=1.0)
        # komodin + mum + yemek
        top_y = 716
        tbl = R.rrect_path(1130, top_y, 270, 16, 3)
        R.lit_path(f, tbl, "#3a2616", lights, rim="#d6a15a", rim_w=1.4, grad=f.lin(0, top_y, 0, top_y + 16, [("#5a3a20", 0.0), ("#2a180c", 1.0)]))
        R.lit_path(f, R.rect_path(1146, top_y + 16, 238, 26), "#2a190d", lights)
        for x in (1150, 1380):
            R.lit_path(f, R.rect_path(x - 11, top_y + 16, 22, yb - top_y - 16), "#241508", lights)
        R.lit_path(f, R.rect_path(1160, top_y + 54, 210, 70), "#2c1a0e", lights)       # çekmece
        f.circle(1265, top_y + 90, 6, color="#c9962b", alpha=0.8)
        R.candle_body(f, self.CANDLE[0], top_y, h=88, w=18, holder=True)
        if self.food:
            for (px, w_) in ((1190, 62),):                 # tabak + ekmek
                f.oval(px, top_y - 2, w_ / 2, 8, color="#c8bfa4")
                f.oval(px, top_y - 4, w_ / 2 - 5, 6, color="#a99d83")
                f.oval(px - 2, top_y - 12, 17, 10, color="#9a6a32")
                f.oval(px + 10, top_y - 10, 11, 7, color="#8a5a2a")
            # kapaklı kap
            f.oval(1350, top_y - 2, 36, 9, color="#6a5a3a")
            f.path(sk.smooth_path([(1316, top_y - 4), (1322, top_y - 30), (1350, top_y - 44), (1378, top_y - 30), (1384, top_y - 4)], True, 0.5), shader=f.lin(1316, 0, 1384, 0, [("#5a4a2a", 0.0), ("#d8c28a", 0.5), ("#5a4a2a", 1.0)]))
            f.circle(1350, top_y - 48, 5, color="#d8c28a")
            # kadeh
            f.poly([(1224, top_y - 4), (1244, top_y - 4), (1240, top_y - 30), (1228, top_y - 30)], color="#a8321e", alpha=0.9)
            f.rect(1233, top_y - 4, 2, 4, color="#c9b890")
            _jug(f, 1300, top_y, 0.75, lights=lights)

    def dyn(self):
        p = self.p
        candle = self.candle
        fade = self.fade
        patient = self.patient
        key = _pkey("bedroom", p)
        cx_, cy_ = self.CANDLE
        top_y = 716

        def D1(f, t):           # oda katmanı: mum sönünce soğuk-karanlık versiyona geçiş
            if fade is None:
                return
            k = smooth((t - fade[0]) / max(0.1, fade[1] - fade[0]))
            img = _SIDE.get(key)
            if img is not None and k > 0.004:
                pa = skia.Paint(AntiAlias=True)
                pa.setAlphaf(k)
                f.c.drawImage(img, -M, -M, skia.SamplingOptions(skia.FilterMode.kLinear), pa)

        def D2(f, t):
            k = 0.0 if fade is None else smooth((t - fade[0]) / max(0.1, fade[1] - fade[0]))
            if patient:
                RF(f, "old_man_bed", 545, 752, 205, rim="#FFC878", rimd=(1.0, -0.2), rim2="#7FA0E8", rim2d=(0.8, -0.7), bob=math.sin(t * 0.7) * 1.2)
            if k > 0.003:
                f.rect(-M, -M, W + 2 * M, H + 2 * M, color="#02030a", alpha=0.74 * k)
            # mum
            if candle > 0.01:
                if fade is None:
                    R.flame(f, cx_, top_y - 88 - 6, s=1.25 * candle, t=t, seed=2.0, halo=1.0, hr=220)
                else:
                    life = 1.0 - k
                    flutter = 1.0 + 0.9 * math.sin(t * 38.0) * (k ** 0.7) * life
                    s_ = 1.25 * candle * max(0.0, life) ** 0.55 * (0.8 + 0.2 * flutter)
                    if s_ > 0.03:
                        R.flame(f, cx_, top_y - 88 - 6, s=s_, t=t * (1 + 2 * k), seed=2.0, halo=max(0.0, life) ** 0.8, hr=220, a=min(1.0, life * 3.0))
                    if k > 0.85 and t > fade[0] + (fade[1] - fade[0]) * 0.92:
                        age = t - (fade[0] + (fade[1] - fade[0]) * 0.92)
                        n_seg = 30
                        ln = min(1.0, (age + 0.2) / 3.2)
                        pts = []
                        for i in range(n_seg + 1):
                            u = i / n_seg * ln
                            pts.append((cx_ + math.sin(u * 7.0 + t * 1.3) * (6 + 34 * u) + math.sin(u * 3.0 - t) * 6, top_y - 94 - u * 230))
                        fade_a = min(1.0, age / 0.5) * max(0.0, 1 - age / 7.0)
                        top_pt = pts[-1]
                        for (sw_, a_) in ((16, 0.10), (8, 0.16), (3.2, 0.22)):
                            sh = skia.GradientShader.MakeLinear([(cx_, top_y - 94), top_pt], [C("#aab0c0", int(255 * a_ * fade_a)), C("#aab0c0", 0)], [0.0, 1.0])
                            f.path(sk.smooth_path(pts, False, 0.5), style="stroke", sw=sw_, shader=sh, cap="round")
            R.motes(f, t, (300, 150, 1300, 700), n=24, seed=3, col="#FFD9A0" if (fade is None or k < 0.5) else "#BFD2FF", a=0.4, drift=(3, -3))

        return {1: D1, 2: D2}


# ═══════════════════════════════════════════════════════════════════════
#  CHAPEL — mum ışıklı şapel, sunak, tabut
# ═══════════════════════════════════════════════════════════════════════
@SL.sc("chapel")
class Chapel:
    """Yuste şapeli: uzun yüksek nef, yan kemerler, kirişli tonoz, arkada yaldızlı retabl + sunak (6 şamdan), nefin ortasında yüksek mumlarla çevrili tabut.
    p: coffin=True (siyah örtülü tabut + altın haç), candles=1.0 (alev boyutu/ışık çarpanı), mourners=3 (0..4 diz çökmüş keşiş), incense=True (tütsü dumanı)."""

    BACK = (650, 160, 1270, 720)
    VP = (960, 470)
    ZB = 1800.0

    def __init__(self, p):
        self.p = p
        self.coffin = p.get("coffin", True)
        self.cs = float(p.get("candles", 1.0))
        self.mourners = int(p.get("mourners", 3))
        self.incense = p.get("incense", True)

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    def layers(self):
        box = self._box()
        P, YF = _persp(box)
        cache = {}
        cs = self.cs
        coffin = self.coffin

        def room():
            if "r" in cache:
                return cache["r"]
            fb = YF
            side = R.mat_arcade(fb, stone="#6d6050", brick="#6d6050", white="#7a6c5a", bay=400.0, lo=(220.0, 250.0, 26.0, 370.0), gal=(130.0, 560.0, 18.0, 640.0), seed=7,
                                recess="#0a0807", glow_prob=0.95, glow=(0.22, 0.34, 0.72), glow_power=0.30)
            back = R.mat_stone_fine("#5a4d3e", seed=6, course=56)
            floor = R.mat_stripe(R.mat_flags("#241f1a", seed=5, size=190), R.mat_carpet("#1a1014", seed=3), 110.0, edge="#6a5226")
            ceil = R.mat_beams("#4a3f33", seed=7, pitch=380, bwid=96, plaster="#2a251f", axis="b")
            mats = dict(back=back, left=side, right=side, floor=floor, ceil=ceil)
            k = min(1.3, 0.3 + cs)
            lights = [R.Light((960, 600, 1730), R.warm(1.0), 2.2 * k, 330, spec=0.4, far=(900, (0.55, 0.20, 0.05), 0.16)),
                      R.Light((P(0, 150, 1250)[0], P(0, 150, 1250)[1], 1250), R.warm(1.0), 2.0 * k, 300, spec=0.6),
                      R.Light((960, 160, 1500), (0.6, 0.35, 0.18), 0.5 * k, 700)]
            rgb, cov = box.render(mats, lights, moon=None, ambient=(0.008, 0.008, 0.014), expo=1.2, ao=0.6, bump=1.0)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # retabl (yaldızlı)
            gl = [(960, 600, 520, "#ffb060", 0.30), (960, 420, 380, "#ffd9a0", 0.10)]
            body = sk.poly_path([(700, 640), (700, 330), (740, 292), (960, 214), (1180, 292), (1220, 330), (1220, 640)], True)
            R.lit_path(f, body, "#6a4a14", gl, rim="#e9c35a", rim_w=2.0, grad=f.lin(0, 214, 0, 640, [("#9a7228", 0.0), ("#6e4c1a", 0.5), ("#3a2810", 1.0)]))
            f.c.save()
            f.c.clipPath(body, skia.ClipOp.kIntersect, True)
            # sütunlar
            for xx in (740, 830, 1090, 1180):
                col = R.rect_path(xx - 14, 300, 28, 340)
                R.lit_path(f, col, "#8a6220", gl, rim="#f1d27a", rim_w=1.0, grad=f.lin(xx - 14, 0, xx + 14, 0, [("#3a2608", 0.0), ("#d9aa3c", 0.4), ("#4a3210", 1.0)]))
                f.rect(xx - 18, 292, 36, 14, color="#e9c35a", alpha=0.85)
                for q in range(9):
                    f.line(xx - 13, 320 + q * 36, xx + 13, 334 + q * 36, color="#2a1a06", sw=1.6, alpha=0.5)
            # orta kemerli niş (koyu) + haç
            niche = ST.pointed_arch_path(960, 600, 150, 300)
            f.path(niche, color="#120c08")
            f.path(niche, style="stroke", sw=3, color="#f1d27a", alpha=0.8)
            f.rect(955, 360, 10, 120, color="#d9aa3c", alpha=0.9)
            f.rect(925, 395, 70, 10, color="#d9aa3c", alpha=0.9)
            f.circle(960, 392, 5, color="#fff0b0", alpha=0.9)
            # yan nişlerde heykelcik siluetleri
            for xx in (785, 1135):
                nic = ST.pointed_arch_path(xx, 560, 60, 190)
                f.path(nic, color="#120c08")
                f.path(nic, style="stroke", sw=2, color="#e9c35a", alpha=0.6)
                f.oval(xx, 480, 11, 14, color="#2a1a0c")
                f.path(sk.smooth_path([(xx - 18, 560), (xx - 12, 498), (xx, 488), (xx + 12, 498), (xx + 18, 560)], True, 0.4), color="#2a1a0c")
            # predella bandı
            f.rect(700, 600, 520, 40, color="#4a3210", alpha=0.9)
            for xx in range(724, 1220, 66):
                f.rrect(xx, 608, 50, 24, 4, style="stroke", sw=1.4, color="#e9c35a", alpha=0.5)
            f.c.restore()
            # küçük üst haç
            f.rect(955, 176, 10, 40, color="#e9c35a")
            f.rect(944, 188, 32, 8, color="#e9c35a")

        def L2(f):
            gl = [(960, 640, 520, "#ffb060", 0.28)]
            # basamaklar
            for (hx, h0, h1, zf) in ((330, 0, 40, 1640), (270, 40, 80, 1700), (220, 80, 120, 1760)):
                front = [P(-hx, h0, zf), P(hx, h0, zf), P(hx, h1, zf), P(-hx, h1, zf)]
                topq = [P(-hx, h1, zf), P(hx, h1, zf), P(hx * 0.98, h1, 1800), P(-hx * 0.98, h1, 1800)]
                _quad(f, front, "#3a3026", gl, grad=f.lin(0, front[2][1], 0, front[0][1], [("#5a4a38", 0.0), ("#1c1610", 1.0)]))
                _quad(f, topq, "#2a2018", gl, rim="#8a6a3a", grad=f.lin(0, topq[2][1], 0, topq[0][1], [("#4a3a28", 0.0), ("#2a2018", 1.0)]))
            # sunak masası + beyaz örtü
            a0 = P(-190, 120, 1790)
            a1 = P(190, 120, 1790)
            at = [P(-190, 120, 1760), P(190, 120, 1760), P(190, 190, 1760), P(-190, 190, 1760)]
            _quad(f, at, "#cfc4a8", gl + [(960, 560, 360, "#ffd9a0", 0.35)], rim="#e8dcc0",
                  grad=f.lin(0, at[2][1], 0, at[0][1], [("#e8dfc4", 0.0), ("#a89d82", 1.0)]))
            f.rect(at[0][0], at[0][1] - 5, at[1][0] - at[0][0], 6, color="#c9962b", alpha=0.8)
            # sunak şamdanları (alevler dyn)
            for X in (-165, -105, -45, 45, 105, 165):
                px = P(X, 190, 1760)
                s_ = 1100.0 / 1760
                f.rect(px[0] - 3 * s_, px[1] - 70 * s_, 6 * s_, 70 * s_, shader=f.lin(px[0] - 3 * s_, 0, px[0] + 3 * s_, 0, [("#7a5a20", 0.0), ("#d9aa3c", 0.5), ("#5a4010", 1.0)]))
                f.oval(px[0], px[1] - 2 * s_, 12 * s_, 4 * s_, color="#d9aa3c")
                f.rect(px[0] - 5 * s_, px[1] - 128 * s_, 10 * s_, 58 * s_, shader=f.lin(px[0] - 5 * s_, 0, px[0] + 5 * s_, 0, [("#9c8a5e", 0.0), ("#efe0b0", 0.5), ("#9c8a5e", 1.0)]))
            # tabut + katafalk
            cz = 1250.0
            if coffin:
                # katafalk (ayaklı sehpa)
                for sx in (-1, 1):
                    for zz in (cz - 80, cz + 80):
                        p0, p1 = P(sx * 60, 0, zz), P(sx * 60, 38, zz)
                        f.rect(p0[0] - 5, p1[1], 10, p0[1] - p1[1], color="#120c08")
                pall_top = [P(-52, 96, cz - 100), P(52, 96, cz - 100), P(52, 96, cz + 100), P(-52, 96, cz + 100)]
                end_face = [P(-52, 38, cz - 100), P(52, 38, cz - 100), P(52, 96, cz - 100), P(-52, 96, cz - 100)]
                side_l = [P(-52, 38, cz - 100), P(-52, 96, cz - 100), P(-52, 96, cz + 100), P(-52, 38, cz + 100)]
                side_r = [P(52, 38, cz - 100), P(52, 96, cz - 100), P(52, 96, cz + 100), P(52, 38, cz + 100)]
                lt2 = [(960, 800, 240, "#ffb060", 0.10)]
                for q, col in ((side_l, "#0c0a0e"), (side_r, "#0c0a0e"), (pall_top, "#14101a"), (end_face, "#0f0c14")):
                    _quad(f, q, col, lt2, rim=None)
                # pall sarkıntıları (drape) — uç yüzde
                for k in range(8):
                    xa = end_face[0][0] + (end_face[1][0] - end_face[0][0]) * (k + 0.5) / 8
                    f.line(xa, end_face[3][1], xa + 1, end_face[0][1], color="#000000", sw=1.6, alpha=0.4)
                f.path(sk.poly_path(pall_top, True), style="stroke", sw=1.6, color="#c9962b", alpha=0.6)
                # altın haç (üst yüzde)
                cx0 = (pall_top[0][0] + pall_top[1][0] + pall_top[2][0] + pall_top[3][0]) / 4
                cy0 = (pall_top[0][1] + pall_top[2][1]) / 2
                f.path(sk.poly_path([(cx0 - 4, cy0 - 20), (cx0 + 4, cy0 - 20), (cx0 + 6, cy0 + 24), (cx0 - 6, cy0 + 24)], True), color="#d9aa3c", alpha=0.9)
                f.path(sk.poly_path([(cx0 - 22, cy0 - 8), (cx0 + 22, cy0 - 8), (cx0 + 24, cy0 - 1), (cx0 - 24, cy0 - 1)], True), color="#d9aa3c", alpha=0.9)
            # tabut çevresinde yüksek şamdanlar
            for (X, zz) in ((-130, cz - 90), (130, cz - 90), (-130, cz + 5), (130, cz + 5), (-130, cz + 100), (130, cz + 100)):
                p0 = P(X, 0, zz)
                s_ = 1100.0 / zz
                ph = 150 * s_
                f.rect(p0[0] - 4 * s_, p0[1] - ph, 8 * s_, ph, shader=f.lin(p0[0] - 4 * s_, 0, p0[0] + 4 * s_, 0, [("#4a3210", 0.0), ("#c9962b", 0.5), ("#3a2608", 1.0)]))
                f.oval(p0[0], p0[1] - 2, 18 * s_, 6 * s_, color="#b88a30")
                f.rect(p0[0] - 8 * s_, p0[1] - ph - 50 * s_, 16 * s_, 52 * s_, shader=f.lin(p0[0] - 8 * s_, 0, p0[0] + 8 * s_, 0, [("#9c8a5e", 0.0), ("#efe0b0", 0.5), ("#9c8a5e", 1.0)]))
            # diz çökmüş keşişler (nefin iki yanında)
            rs = np.random.RandomState(9)
            spots = [(-210, 1100, 1), (230, 1130, -1), (-200, 1400, 1), (215, 1420, -1)]
            for (X, zz, face) in spots[:self.mourners]:
                pp = P(X, 0, zz)
                RF(f, "monk_kneel", pp[0], pp[1], 210 * 1100.0 / zz, col="#050302", rim="#C58A44", rimd=(-face * 0.9, -0.3), face=face)
            _shadow_ellipse(f, 960, P(0, 0, 1250)[1] + 4, 230, 14, 0.6, 14)

        def L3(f):
            # ön plan: sıra/bank siluetleri
            for sx in (-1, 1):
                f.rect(W / 2 + sx * 900 - 90, 700, 180, 600, color="#050302")
                f.rect(W / 2 + sx * 900 - 110, 690, 220, 22, color="#0a0604")
            f.rect(-M, H - 90, W + 2 * M, 90 + M, shader=f.lin(0, H - 90, 0, H + M, [("#000000", 0.0, 0), ("#000000", 1.0, 235)]))
            R.vignette_frame(f, 0.74, 0.5)

        return [(0.8, L1), (1.0, L2), (1.35, L3)]

    def dyn(self):
        box = self._box()
        P, YF = _persp(box)
        cs = self.cs
        coffin = self.coffin
        cz = 1250.0
        inc = self.incense

        def D1(f, t):
            for X in (-165, -105, -45, 45, 105, 165):
                px = P(X, 190, 1760)
                s_ = 1100.0 / 1760
                R.flame(f, px[0], px[1] - 128 * s_ - 3, s=0.72 * cs, t=t, seed=X * 0.013, halo=0.4, hr=80)
            for (X, zz) in ((-130, cz - 90), (130, cz - 90), (-130, cz + 5), (130, cz + 5), (-130, cz + 100), (130, cz + 100)):
                p0 = P(X, 0, zz)
                s_ = 1100.0 / zz
                R.flame(f, p0[0], p0[1] - 150 * s_ - 52 * s_ - 4, s=0.95 * cs * s_ + 0.3, t=t, seed=X * 0.01 + zz * 0.01, halo=0.7, hr=130 * s_ + 40)
            # kutsal lamba (kırmızı)
            lp = P(0, 360, 1500)
            f.line(lp[0], -M, lp[0], lp[1] - 20, color="#2a1c0a", sw=2.0)
            f.oval(lp[0], lp[1], 14, 8, color="#7a5518")
            R.flame(f, lp[0], lp[1] - 8, s=0.7, t=t, seed=7.7, halo=0.9, hr=70, col_out="#FF3a22", col_in="#FFB0A0", halo_col="#FF4a2a")
            if inc:                    # tütsü dumanı (ucuz: degradeli kıvrımlı çizgiler)
                for j, (x0_, ph_) in enumerate(((1126, 0.0), (1138, 2.1))):
                    pts = [(x0_ + math.sin(u * 6.2 + t * 0.9 + ph_) * (5 + 40 * u) + math.sin(u * 2.4 - t * 0.5) * 8, 770 - u * 300) for u in [i / 28 for i in range(29)]]
                    for (sw_, a_) in ((18, 0.05), (8, 0.08), (3, 0.12)):
                        sh = skia.GradientShader.MakeLinear([(x0_, 770), (x0_, 470)], [C("#b4b0be", int(255 * a_)), C("#b4b0be", 0)], [0.0, 1.0])
                        f.path(sk.smooth_path(pts, False, 0.5), style="stroke", sw=sw_, shader=sh, cap="round")
            R.motes(f, t, (600, 200, 760, 600), n=26, seed=4, col="#FFD9A0", a=0.45, drift=(2, -4))

        return {1: D1}


# ═══════════════════════════════════════════════════════════════════════
#  RANSOM_ROOM — Cajamarca fidye odası
# ═══════════════════════════════════════════════════════════════════════
@SL.sc("ransom_room")
class RansomRoom:
    """Cajamarca fidye odası: İnka taş işçiliği (trapez nişler), duvarlarda yüksekte KIRMIZI çizgi, yüksekteki delikten giren ışık huzmesi,
    sağda parlak kapı (İspanyol askerler siluet), yığılan altın eşyalar (vazo, levha, heykelcik, kadeh, maske, külçe), tutsak Atahualpa (tüylü başlık, kolu çizgiye uzanmış).
    p: fill_t=None|(t0,t1) yerel sn'de yığın fill0→fill oranına dolar; fill=1.0 (son seviye; fill_t yoksa sabit), fill0=0.0, prisoner=True, soldiers=2 (0..3), door=True."""

    BACK = (380, 120, 1540, 880)
    VP = (960, 480)
    ZB = 1300.0
    HOLE = (468, 226, 548, 306)
    RED_HF = 430.0
    HEAP = dict(cx=870.0, base=888.0, half=440.0, H=360.0)
    J = 14

    def __init__(self, p):
        self.p = p
        self.fill_t = p.get("fill_t")
        self.fill = float(p.get("fill", 1.0))
        self.fill0 = float(p.get("fill0", 0.0))
        self.prisoner = p.get("prisoner", True)
        self.soldiers = int(p.get("soldiers", 2))
        self.door = p.get("door", True)

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    def _bbox(self):
        h = self.HEAP
        return (int(h["cx"] - h["half"] - 70), int(h["base"] - h["H"] - 90), int(2 * h["half"] + 140), int(h["H"] + 130))

    def layers(self):
        box = self._box()
        cache = {}
        k0 = self.ZB / 1100.0
        fb = (self.BACK[3] - self.VP[1]) * k0
        key = _pkey("ransom_room", self.p)
        hole_outer = box.hole_outer(self.HOLE, 120.0, 0.8)
        zw = box.zb + 120.0
        door_on = self.door
        items = PR.hoard_items(seed=3, **self.HEAP)
        fill_static = self.fill

        def room():
            if "r" in cache:
                return cache["r"]
            inc = R.mat_inca("#6a5d52", seed=3)
            back = R.mat_inca_wall(fb, inca=inc, niches=[(-430, 470, 690, 150, 100), (-145, 470, 690, 150, 100), (145, 470, 690, 150, 100)], red=(self.RED_HF, 15.0),
                                   door=(430, 520, 215, 150) if door_on else None, door_power=2.6)
            side = R.mat_inca_wall(fb, inca=R.mat_inca("#625549", seed=5), niches=[(150, 215, 430, 150, 104)], pitch=340.0, red=(self.RED_HF, 15.0))
            floor = R.mat_plaster("#4a3a2a", seed=7, rough=0.6, stain=0.4, tone=0.1)
            ceil = R.mat_beams("#2b1d12", seed=7, pitch=260, bwid=70, plaster="#3a2c1c", axis="a")
            mats = dict(back=back, left=side, right=side, floor=floor, ceil=ceil)
            lights = [R.Light((930, 740, 1100), (1.0, 0.72, 0.30), 0.9, 420), R.Light((930, 500, 1000), (0.7, 0.5, 0.2), 0.35, 700)]
            moons = []
            if door_on:
                dxc = 430.0
                g = dict(z=box.zb, wrect=(dxc - 105.0, fb - 520.0 - (fb - 472.7) * 0 - (472.7 - 472.7) - 472.7 + 472.7 - 520 + 520 - 472.7 + 0, dxc + 105.0, 0.0))
                # kapı açıklığı: dünya Y (aşağı +) aralığı: zemin=fb → üst = fb-520
                g["wrect"] = (dxc - 105.0, fb - 520.0, dxc + 105.0, fb)
                moons.append(R.Moon((-0.45, 0.32, -0.83), col=(1.0, 0.88, 0.62), power=1.7, win=g, pen=6.0, pen_k=0.014))
            gh = R.window_gobo(box, hole_outer, zw)
            moons.append(R.Moon((0.52, 0.66, -0.54), col=(0.95, 0.92, 0.85), power=1.6, win=gh, pen=3.0, pen_k=0.010))
            rgb, cov = box.render(mats, lights, moon=moons, ambient=(0.016, 0.013, 0.011), expo=1.2, ao=0.6,
                                  holes=[dict(rect=self.HOLE, T=120.0, splay=0.8, mat=inc, ao=0.2)])
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L0(f):
            f.rect(-M, -M, W + 2 * M, H + 2 * M, shader=f.lin(0, -M, 0, 700, [("#e8f0f6", 0.0), ("#b8d0e4", 0.6), ("#7aa0c0", 1.0)]))
            ST.hills(f, 350, 20, "#5a7088", seed=2, wavelength=0.005)

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)

        bx, by, bw_, bh_ = self._bbox()

        def L2(f):
            # delikten gelen ışık huzmesi + kapı huzmesi (statik)
            for q in R.shaft_polys(box, hole_outer, zw, (0.52, 0.66, -0.54), [], 8):
                _soft_hull(f, q, "#fff4d8", 0.20)
            if door_on:
                dr = ((960 + (430 - 105) * 1100.0 / self.ZB), 480 + (fb - 520 - 472.7 + 472.7) * 0 + (fb - 520) * 1100.0 / self.ZB, (960 + (430 + 105) * 1100.0 / self.ZB), 480 + fb * 1100.0 / self.ZB)
                for q in R.shaft_polys(box, (dr[0], dr[1], dr[2], dr[3]), box.zb, (-0.45, 0.32, -0.83), [], 8):
                    _soft_hull(f, q, "#ffe9b8", 0.13)
            # yığın (statik: fill_t yoksa son seviye)
            if self.fill_t is None and fill_static > 0:
                PR.draw_hoard(f, items, 0.0, fill_static)
            _shadow_ellipse(f, 930, 896, 560, 20, 0.5, 18)
            R.glow(f, 880, 780, 460, "#ffc450", 0.30 * (fill_static if self.fill_t is None else 0.0), sy=0.6)

        def L3(f):
            R.vignette_frame(f, 0.74, 0.5)
            for sx in (-1, 1):
                f.rect(W / 2 + sx * 1040 - 90, -M, 180, H + 2 * M, shader=f.lin(W / 2 + sx * 1040 - 90, 0, W / 2 + sx * 1040 + 90, 0, [("#000000", 0.0, 235), ("#16110c", 0.5, 245), ("#000000", 1.0, 235)]))

        layers = [(0.1, L0), (0.85, L1), (1.0, L2), (1.36, L3)]
        if self.fill_t is not None:
            def bake_snaps():
                surf = skia.Surface(bw_, bh_)
                c = surf.getCanvas()
                c.clear(skia.ColorTRANSPARENT)
                fr = sk.Frame(1, 1)
                fr.c = c
                fr.w, fr.h = bw_, bh_
                c.translate(-bx, -by)
                snaps = [None]
                for j in range(1, self.J + 1):
                    PR.draw_hoard(fr, items, (j - 1) / self.J, j / self.J)
                    snaps.append(surf.makeImageSnapshot())
                _SIDE[key + "|snaps"] = snaps
            bake_snaps()
        return layers

    def dyn(self):
        key = _pkey("ransom_room", self.p)
        fill_t, fill, fill0 = self.fill_t, self.fill, self.fill0
        bx, by, bw_, bh_ = self._bbox()
        J = self.J
        prisoner, soldiers, door_on = self.prisoner, self.soldiers, self.door
        items = PR.hoard_items(seed=3, **self.HEAP)
        fb = (self.BACK[3] - self.VP[1]) * self.ZB / 1100.0

        def D2(f, t):
            k = fill
            if fill_t is not None:
                u = smooth((t - fill_t[0]) / max(0.1, fill_t[1] - fill_t[0]))
                k = fill0 + (fill - fill0) * u
                snaps = _SIDE.get(key + "|snaps")
                if snaps and k > 0.003:
                    x = k * J
                    j = int(min(J, math.floor(x)))
                    fr = x - j
                    pa = skia.SamplingOptions(skia.FilterMode.kLinear)
                    if j >= 1:
                        f.c.drawImage(snaps[j], bx, by, pa, skia.Paint())
                    if j < J and fr > 0.01:
                        p2 = skia.Paint()
                        p2.setAlphaf(fr)
                        f.c.drawImage(snaps[j + 1], bx, by, pa, p2)
                R.glow(f, 880, 780, 460, "#ffc450", 0.30 * k, sy=0.6)
            # parıltılar
            if k > 0.08:
                rs = np.random.RandomState(5)
                pa = skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kPlus)
                for i in range(14):
                    it = items[int(rs.randint(len(items)))]
                    if it["rank"] > k:
                        continue
                    a = max(0.0, math.sin(t * (1.2 + 1.5 * rs.rand()) + i * 3.1)) ** 8
                    if a > 0.06:
                        x, y = it["x"], it["y"]
                        pa.setColor(C("#FFF6C8", int(255 * a)))
                        f.c.drawCircle(x, y, 2.6, pa)
                        pa.setColor(C("#FFF6C8", int(140 * a)))
                        f.c.drawLine(x - 12, y, x + 12, y, pa)
                        f.c.drawLine(x, y - 12, x, y + 12, pa)
            # asker siluetleri (kapıda)
            if door_on:
                dxs = [960 + 430 * 1100.0 / 1300 + d for d in (-34, 30, 78)]
                for i in range(min(3, soldiers)):
                    ST.figure(f, "conquistador", dxs[i], 886 + (i == 2) * 2, 330 - 14 * i, col="#08050a", rim="#FFE2A8", face=-1, sway=math.sin(t * 0.8 + i) * 0.003)
            if prisoner:
                RF(f, "atahualpa", 640, 944, 430, rim="#FFD890", rimd=(1.0, -0.4), rim2="#FFF0C8", rim2d=(0.8, -0.9), bob=math.sin(t * 0.8) * 1.2)
            R.motes(f, t, (440, 160, 1100, 760), n=40, seed=8, col="#FFF0C8", a=0.55, drift=(3, 5))

        return {2: D2}


# ═══════════════════════════════════════════════════════════════════════
#  DEBATE_HALL — Valladolid 1550 (Las Casas ↔ Sepúlveda)
# ═══════════════════════════════════════════════════════════════════════
def _lectern(f, x, y, s=1.0, lights=(), col="#3a2616", face=1):
    """Eğik tablalı kürsü (önden/yan karışık): y zemin. face yönünde kitap açık."""
    post = R.rect_path(x - 14 * s, y - 96 * s, 28 * s, 96 * s)
    R.lit_path(f, post, shade_(col, -0.2), lights, rim="#b88a52", rim_w=1.0, grad=f.lin(x - 14 * s, 0, x + 14 * s, 0, [("#1a0e06", 0.0), (shade_(col, 0.1), 0.5), ("#1a0e06", 1.0)]))
    base = R.rrect_path(x - 44 * s, y - 10 * s, 88 * s, 10 * s, 3)
    R.lit_path(f, base, shade_(col, -0.3), lights)
    top = sk.poly_path([(x - 52 * s, y - 100 * s), (x + 52 * s, y - 100 * s), (x + 44 * s * face, y - 128 * s), (x - 44 * s * face, y - 128 * s)], True)
    R.lit_path(f, top, shade_(col, 0.05), lights, rim="#d6a15a", rim_w=1.4)
    f.rect(x - 50 * s, y - 102 * s, 100 * s, 6 * s, color=shade_(col, -0.4))
    bk = sk.poly_path([(x - 34 * s, y - 106 * s), (x + 34 * s, y - 106 * s), (x + 30 * s, y - 122 * s), (x - 30 * s, y - 122 * s)], True)
    R.lit_path(f, bk, "#cdbb8c", lights, edge="#6a5638")
    f.line(x, y - 106 * s, x, y - 122 * s, color="#4a3a24", sw=1.5)


@SL.sc("debate_hall")
class DebateHall:
    """Valladolid 1550 tartışma salonu: yüksek taş salon (iki yan duvarda sivri pencereler, çapraz huzmeler), arkada yüksek kürsüde jüri sırası (yeşil örtülü masa),
    ön planda iki kürsü ve karşılıklı konuşmacılar, kâtipler, yan sıralarda dinleyiciler.
    p: lecterns=2 (0..2 konuşmacılı kürsü), jury=7 (0..9), crowd=True, left='friar', right='scholar' (konuşmacı tipi: friar|scholar), sun=1.0."""

    BACK = (480, 170, 1440, 760)
    VP = (960, 450)
    ZB = 1600.0

    def __init__(self, p):
        self.p = p
        self.lecterns = int(clamp(p.get("lecterns", 2), 0, 2))
        self.jury = int(clamp(p.get("jury", 7), 0, 9))
        self.crowd = p.get("crowd", True)
        self.left = p.get("left", "friar")
        self.right = p.get("right", "scholar")
        self.sun = float(p.get("sun", 1.0))

    def _box(self):
        return R.Box(self.BACK, vp=self.VP, zb=self.ZB, F=1100.0)

    LECT = [(-300.0, 900.0, 1), (300.0, 900.0, -1)]

    def layers(self):
        box = self._box()
        P, YF = _persp(box)
        cache = {}
        sun = self.sun
        XL = (self.BACK[0] - self.VP[0]) * self.ZB / 1100.0
        XR = (self.BACK[2] - self.VP[0]) * self.ZB / 1100.0
        PITCH, NWIN, A0, WW = 310.0, 3, 260.0, 160.0
        H1, SPR, H3 = 240.0, 560.0, 720.0
        Zmin = self.ZB - (A0 + (NWIN - 1) * PITCH + WW)
        DL = (0.72, 0.58, -0.36)
        DR = (-0.72, 0.58, -0.36)
        jury_n = self.jury

        def room():
            if "r" in cache:
                return cache["r"]
            wl = R.mat_hallwall(YF, stone="#6a5c4b", pitch=PITCH, a0=A0, nwin=NWIN, w=WW, h1=H1, spring=SPR, h3=H3, seed=4, power=2.3 * sun)
            wr = R.mat_hallwall(YF, stone="#625546", pitch=PITCH, a0=A0, nwin=NWIN, w=WW, h1=H1, spring=SPR, h3=H3, seed=8, power=2.3 * sun)
            back = R.mat_stone_fine("#5e5040", seed=6, course=54)
            floor = R.mat_checker("#27211b", "#463c30", size=170, seed=6)
            ceil = R.mat_beams("#34261a", seed=7, pitch=290, bwid=96, plaster="#403628", axis="b")
            mats = dict(back=back, left=wl, right=wr, floor=floor, ceil=ceil)
            lights = [R.Light((960, 380, 1000), R.warm(1.0), 1.0, 380, spec=0.2), R.Light((960, 460, 1560), R.warm(1.0), 1.2, 300)]
            wL = dict(axis="x", x=XL, wrect=(Zmin, YF - H3, Zmin + WW, YF - H1), pitch=PITCH, n=NWIN, spring=YF - SPR)
            wR = dict(axis="x", x=XR, wrect=(Zmin, YF - H3, Zmin + WW, YF - H1), pitch=PITCH, n=NWIN, spring=YF - SPR)
            moons = [R.Moon(DL, col=(1.0, 0.86, 0.62), power=1.05 * sun, win=wL, pen=7.0, pen_k=0.02), R.Moon(DR, col=(1.0, 0.86, 0.62), power=0.85 * sun, win=wR, pen=7.0, pen_k=0.02)]
            rgb, cov = box.render(mats, lights, moon=moons, ambient=(0.008, 0.008, 0.012), expo=0.98, ao=0.6)
            cache["r"] = (rgb, cov)
            return cache["r"]

        def L1(f):
            rgb, cov = room()
            R.draw_np(f, rgb, cov)
            # arka duvar: haç + sancaklar (duvarla aynı katman)
            for sx in (-1, 1):
                x, y = 960 + sx * 330, 310
                PR.banner_hang(f, x, 190, 150, 300, "#5a1016" if sx < 0 else "#1c3326", "#c9962b", [(960, 420, 800, "#ff9c40", 0.15)], icon="crown" if sx < 0 else "book")
            f.rect(949, 250, 22, 190, color="#1a0e08")
            f.rect(906, 296, 108, 22, color="#1a0e08")
            f.line(960, 252, 960, 436, color="#9a7a48", sw=1.2, alpha=0.5)
            f.path(sk.smooth_path([(944, 330), (960, 318), (976, 330), (972, 380), (948, 380)], True, 0.5), color="#2a1a10")
            R.glow(f, 960, 330, 160, "#ffb060", 0.14)

        def L2(f):
            warm_l = [(960, 560, 520, "#ff9c40", 0.20), (960, 300, 700, "#ffb060", 0.08)]
            # pencere huzmeleri (iki yandan)
            for q in R.shaft_polys_x(box, XL, (Zmin, YF - H3, Zmin + WW, YF - H1), DL, PITCH, NWIN):
                _soft_hull(f, q, "#ffe2a8", 0.15 * sun)
            for q in R.shaft_polys_x(box, XR, (Zmin, YF - H3, Zmin + WW, YF - H1), DR, PITCH, NWIN):
                _soft_hull(f, q, "#ffe2a8", 0.12 * sun)
            # jüri kürsüsü (dais)
            for (hx, h0, h1, zf) in ((600, 0, 40, 1420), (560, 40, 80, 1470)):
                front = [P(-hx, h0, zf), P(hx, h0, zf), P(hx, h1, zf), P(-hx, h1, zf)]
                topq = [P(-hx, h1, zf), P(hx, h1, zf), P(hx * 0.98, h1, 1600), P(-hx * 0.98, h1, 1600)]
                _quad(f, front, "#3a2a1c", warm_l, grad=f.lin(0, front[2][1], 0, front[0][1], [("#5a4630", 0.0), ("#241812", 1.0)]))
                _quad(f, topq, "#2a2018", warm_l, rim="#8a6a3a")
            # koltuklar + jüri üyeleri (ön görünüş oturan siluetler)
            if jury_n > 0:
                gears = ["mitre", "cap", "galero", "kurhut", "cap", "galero", "mitre", "cap", "kurhut"]
                span = 760.0
                xs_ = [(-span / 2 + span * (i + 0.5) / jury_n) if jury_n > 1 else 0.0 for i in range(jury_n)]
                order = sorted(range(jury_n), key=lambda i: abs(xs_[i]), reverse=True)
                for i in order:
                    X = xs_[i]
                    pb = P(X, 80, 1560)
                    sc_ = 1100.0 / 1560.0
                    PR.chair_high(f, pb[0], pb[1], 0.50 * sc_ * 1.35, warm_l, col="#35210f", trim="#c9962b")
                    RF(f, "elector_" + gears[i % len(gears)], pb[0], pb[1] - 2, 150 * sc_, rim="#FFE2A8", rimd=(0.0, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1))
            # jüri masası (yeşil örtü, altın saçak) — jüri üyelerinin önünde
            tz = 1500.0
            tfront = [P(-470, 0 + 80, tz - 70), P(470, 80, tz - 70), P(470, 80 + 62, tz - 70), P(-470, 80 + 62, tz - 70)]
            ttop = [P(-470, 80 + 62, tz - 70), P(470, 80 + 62, tz - 70), P(470, 80 + 62, tz + 30), P(-470, 80 + 62, tz + 30)]
            _quad(f, ttop, "#1c3a28", warm_l, rim="#c9962b", grad=f.lin(0, ttop[2][1], 0, ttop[0][1], [("#2a4a36", 0.0), ("#16301f", 1.0)]))
            _quad(f, tfront, "#14281c", warm_l, grad=f.lin(0, tfront[2][1], 0, tfront[0][1], [("#1c3a28", 0.0), ("#0a150e", 1.0)]))
            for k in range(26):
                xa = tfront[0][0] + (tfront[1][0] - tfront[0][0]) * (k + 0.5) / 26
                f.line(xa, tfront[0][1] - 3, xa, tfront[0][1] + 4, color="#c9962b", sw=2.0, alpha=0.7)
            f.line(tfront[0][0], tfront[0][1], tfront[1][0], tfront[1][1], color="#c9962b", sw=2.0, alpha=0.7)
            # masada kâğıt/kitap/mum
            pm = P(-120, 80 + 62, tz - 20)
            PR.ledger_open(f, pm[0], pm[1], w=120 * 1100.0 / tz, h=26 * 1100.0 / tz, lights=warm_l, seed=3)
            for X in (260, -300):
                pc = P(X, 80 + 62, tz - 20)
                R.candle_body(f, pc[0], pc[1], h=60 * 1100.0 / tz, w=12 * 1100.0 / tz, holder=True)
            # yan bankların seyircileri
            if self.crowd:
                rs = np.random.RandomState(31)
                hats = ["beret", "cap", "galero", "mitre", "hood", "beret", "cap"]
                for side in (-1, 1):
                    for rowX in (560, 450):
                        inner = side * (rowX - 50)
                        outer = side * (rowX + 36)
                        zA, zB = 820, 1380
                        q_front = [P(inner, 0, zA), P(inner, 0, zB), P(inner, 46, zB), P(inner, 46, zA)]
                        q_top = [P(inner, 46, zA), P(inner, 46, zB), P(outer, 46, zB), P(outer, 46, zA)]
                        _quad(f, q_front, "#2a1a10", warm_l, grad=f.lin(0, q_front[2][1], 0, q_front[0][1], [("#3a2616", 0.0), ("#150d08", 1.0)]))
                        _quad(f, q_top, "#34200f", warm_l, rim="#8a6a3a")
                        z = zB
                        while z > zA:
                            pp = P(side * rowX + rs.uniform(-8, 8), 0, z)
                            hh = rs.uniform(150, 166) * 1100.0 / z
                            RF(f, "sit_" + hats[rs.randint(len(hats))], pp[0], pp[1], hh, col="#0b0705", rim="#C58A44", rimd=(1.0, -0.5) if side < 0 else (-1.0, -0.4), rim2="#7FA0E8", rim2d=(0.0, -1.0), face=-side)
                            z -= rs.uniform(70, 96) * (z / 1300.0)
            # kâtipler
            for (X, face) in ((-610, 1), (610, -1)):
                pp = P(X, 0, 1400)
                sc_ = 1100.0 / 1400.0
                hh = 150 * sc_
                dk = hh * 0.30
                PR.desk_slant(f, (pp[0] + face * hh * 0.30) if face > 0 else (pp[0] - hh * 0.30 - hh * 0.7), pp[1], w=hh * 0.7, h=hh * 0.58, lights=warm_l)
                RF(f, "clerk_seated", pp[0], pp[1], hh, rim="#F0B060", rimd=(1.0, -0.3), rim2="#FFC878", rim2d=(0.3, -1.0), face=face)
            # kürsüler (konuşmacılar dyn'de)
            for i, (X, Z, face) in enumerate(self.LECT[:self.lecterns]):
                pp = P(X, 0, Z)
                s_ = 1100.0 / Z
                _lectern(f, pp[0] + face * 46 * s_, pp[1], s_ * 1.0, warm_l, face=face)

        def L3(f):
            rs = np.random.RandomState(5)
            for side in (-1, 1):
                pp = P(side * 520, 0, 700)
                RF(f, "sit_" + ["beret", "hood", "galero"][rs.randint(3)], pp[0], pp[1] + 22, 165 * 1100.0 / 700, col="#040201", rim="#8A5A2A", rimd=(1.0 if side < 0 else -1.0, -0.5), face=-side)
            f.rect(-M, H - 70, W + 2 * M, 70 + M, shader=f.lin(0, H - 70, 0, H + M, [("#000000", 0.0, 0), ("#000000", 1.0, 230)]))
            R.vignette_frame(f, 0.7, 0.55)

        return [(0.8, L1), (1.0, L2), (1.3, L3)]

    def dyn(self):
        box = self._box()
        P, YF = _persp(box)
        n = self.lecterns
        kinds = [("orator_" + self.left, 1), ("orator_" + self.right, -1)]

        def D2(f, t):
            for i, (X, Z, face) in enumerate(self.LECT[:n]):
                pp = P(X, 0, Z)
                s_ = 1100.0 / Z
                kind = kinds[i][0]
                # konuşmacı: hafif öne-arkaya vurgulu jest (sway) + nefes
                gest = math.sin(t * 1.3 + i * 2.1) * 0.012
                RF(f, kind, pp[0], pp[1], 196 * s_, rim="#FFD890", rimd=(0.8 * face, -0.5), rim2="#FFE2A8", rim2d=(0.0, -1.0), face=face, sway=gest, bob=math.sin(t * 1.0 + i) * 1.0)
            R.motes(f, t, (400, 140, 1120, 740), n=40, seed=7, col="#FFE8B8", a=0.5, drift=(5, 4))

        return {1: D2}
