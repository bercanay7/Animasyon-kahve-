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
                 fig_xy=(930, 950, 520), moon_p=1.4, ambient=(0.006, 0.008, 0.015)),
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
            for st in sorted(seats, key=lambda s: s["y"]):
                if occ:
                    h = 300 * st["s"]
                    RF(f, "elector_" + st["gear"], st["x"], st["y"] - 4 * st["s"], h, rim="#FFE2A8", rimd=(0.0, -1.0), rim2="#E39A4A", rim2d=(0.9, 0.1),
                       bob=math.sin(t * 0.8 + st["i"]) * 1.0)
                if light_t is not None:
                    t0, t1 = light_t
                    ti = t0 + (t1 - t0) * (st["i"] / 6.0 if n == 7 else st["i"] / 6.0)
                    k = smooth((t - ti) / 0.5)
                    if k > 0.01:
                        hy = st["y"] - (300 * 0.9 * st["s"] if occ else 330 * st["s"])
                        R.glow(f, st["x"], hy, 170 * st["s"] * (0.8 + 0.2 * k), "#FFC860", 0.55 * k)
                        R.glow(f, st["x"], hy - 10 * st["s"], 60 * st["s"], "#FFF3C8", 0.65 * k)
                        f.circle(st["x"], hy - 30 * st["s"], 58 * st["s"] * (0.9 + 0.1 * k), style="stroke", sw=2.2 * st["s"], color="#FFE9A8", alpha=0.7 * k)
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
