"""c10_kinds — c10 «Rahip ve Kral» özel çekim türleri ve odaları (Parça 5 sahne yazarı). `scenes_c10.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dil: BEDEL perdesi — gece/alacakaranlık görsel dili (lapis → közer), kısa vuruşlar + ağır nefesler; yüz çizilmez (silüet/madalya siluet), şiddet ve beden yok
(darağacı yalnız silüet, idam = ışık/mum söner, ateş = yığın). Ekrana yalnız script/brif sözcükleri yazılır; çan/saat/koku/ışık iddiası yok.
Tüm zamanlar cümle/sözcük çapalı (cx.at / cx.amt); mutlak saniye yok.

İçerik
  * `c10_tepe`      — V1: Careggi tepesinden gece Floransa, tek pencere ışığı; kamera pencereye iner (zoomthru ile `careggi` odasına açılır)
  * `OD.ROOMS["careggi"]` — V1/V4: Careggi odası (yatak, pencere, masa, kapı); `oda` türüyle çağrılır (room="careggi"); yatan/ayaktaki siluetler `actors` ile
  * yardımcılar: `lying_man` (yatan erkek siluet; turn=0..1 duvara döner), `cam_xy` (kamera dönüşüm yardımcısı)
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_city as CT
import cilt_kinds2 as K2
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import cilt_scene as SC
import icons
import p5_lib as L
import sk
from cilt_medici import TH
from p5_lib import INK, P, S, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

SKY_Y = 168


def cam_xy(cam, wx, wy, layer=1.0):
    """CM.Cam altında dünya (wx,wy) noktasının ekran koordinatı (cam.begin(f, layer) ile aynı dönüşüm)."""
    px, py = cam.pivot
    s = 1.0 + (cam.s - 1.0) * layer
    return (px + cam.dx * layer + s * (wx - px), py + cam.dy * layer + s * (wy - py))


# ═════════════════════════════ V1 · Careggi tepesi (gece) ═════════════════════════════
VILLA = dict(x0=1330, x1=1840, yb=700, h=204)
WIN = (1600, 562)                       # yanan pencerenin merkezi (dünya = nötr kamerada ekran)
WIN_W, WIN_H = 50, 78


def _villa(f, T, t, lit, seed=3):
    """Careggi villası (stilize, Michelozzo tarzı blok): ashlar duvar, kırma çatı, solda loggia, sağda kule; yalnız bir pencere yanar."""
    c = f.c
    v = VILLA
    x0, x1, yb, h = v["x0"], v["x1"], v["yb"], v["h"]
    wall = T("#CDBC94")
    wall2 = T("#B7A47C")
    # gövde
    c.drawRect(skia.Rect.MakeLTRB(x0, yb - h, x1, yb), P(wall))
    c.drawRect(skia.Rect.MakeLTRB(x0, yb - h, x1, yb), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear(
        [(x0, 0), (x1, 0)], [C("#FFFFFF", 26), C("#FFFFFF", 0), C("#000000", 70)], [0.0, 0.4, 1.0])))
    rs = np.random.RandomState(seed)
    for k in range(7):                                                      # ashlar sıraları
        yy = yb - h + 26 + k * 24
        c.drawLine(x0, yy, x1, yy, S(wall2, 1.2, 140))
        for q in range(int((x1 - x0) / 58)):
            xx = x0 + q * 58 + (29 if k % 2 else 0) + rs.uniform(-3, 3)
            c.drawLine(xx, yy, xx, yy + 24, S(wall2, 1.0, 110))
    # çatı (kırma) + saçak
    roof = T("#B4552E")
    rp = sk.poly_path([(x0 - 26, yb - h + 6), (x0 + 70, yb - h - 74), (x1 - 150, yb - h - 74), (x1 + 26, yb - h + 6)])
    c.drawPath(rp, P(roof))
    for k in range(9):
        c.drawLine(x0 - 20 + k * 58, yb - h + 2, x0 + 70 + k * 34, yb - h - 72, S(mix(roof, "#000000", 0.35), 1.2, 140))
    c.drawPath(rp, S("#1A0F08", 1.6, 190))
    c.drawRect(skia.Rect.MakeLTRB(x0 - 26, yb - h + 4, x1 + 26, yb - h + 16), P(mix(wall, "#000000", 0.25)))
    # kule (torretta)
    tx0, tx1 = x1 - 128, x1 - 62
    c.drawRect(skia.Rect.MakeLTRB(tx0, yb - h - 134, tx1, yb - h + 6), P(wall))
    c.drawRect(skia.Rect.MakeLTRB(tx0 - 8, yb - h - 148, tx1 + 8, yb - h - 134), P(mix(wall, "#000000", 0.2)))
    for k in range(5):
        c.drawRect(skia.Rect.MakeLTRB(tx0 - 8 + k * 17, yb - h - 160, tx0 - 8 + k * 17 + 9, yb - h - 148), P(mix(wall, "#000000", 0.2)))
    c.drawRect(skia.Rect.MakeLTRB(tx0 + 22, yb - h - 112, tx1 - 22, yb - h - 76), P("#0C0A14"))
    c.drawRect(skia.Rect.MakeLTRB(tx0, yb - h - 134, tx1, yb - h + 6), S("#1A0F08", 1.4, 170))
    # loggia (solda): kemer sırası
    for k in range(4):
        ax = x0 + 22 + k * 56
        ap = skia.Path()
        ap.moveTo(ax, yb)
        ap.lineTo(ax, yb - 62)
        ap.arcTo(skia.Rect.MakeLTRB(ax, yb - 90, ax + 44, yb - 34), 180, 180, False)
        ap.lineTo(ax + 44, yb)
        ap.close()
        c.drawPath(ap, P("#0A0A18"))
        c.drawPath(ap, S("#1A0F08", 1.4, 190))
    # kapalı pencereler (sönük) — yalnız bir tanesi yanar
    for wx_ in (1420, 1510, 1690, 1780):
        wp = skia.Path()
        wp.addRect(skia.Rect.MakeLTRB(wx_ - 18, WIN[1] - 39, wx_ + 18, WIN[1] + 39))
        c.drawPath(wp, P("#0C0A14"))
        c.drawPath(wp, S("#1A0F08", 1.2, 170))
        c.drawLine(wx_, WIN[1] - 39, wx_, WIN[1] + 39, S("#2A2038", 1.0, 150))
    # yanan pencere: kemerli açıklık + sıcak cam + çıta + alev
    wx, wy = WIN
    w2, h2 = WIN_W / 2, WIN_H / 2
    op = skia.Path()
    op.moveTo(wx - w2, wy + h2)
    op.lineTo(wx - w2, wy - h2 + w2)
    op.arcTo(skia.Rect.MakeLTRB(wx - w2, wy - h2, wx + w2, wy - h2 + 2 * w2), 180, 180, False)
    op.lineTo(wx + w2, wy + h2)
    op.close()
    fl = 0.78 + 0.16 * math.sin(t * 9.1) + 0.08 * math.sin(t * 14.9 + 1.3) + 0.06 * math.sin(t * 3.3)
    fl = clamp(fl * lit)
    c.drawPath(op, P("#0C0A14"))
    c.save()
    c.clipPath(op, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeRadial((wx, wy + h2 * 0.45), WIN_H * 0.95, [C("#FFF0B0", int(255 * fl)), C("#FFC25E", int(255 * fl)), C("#B8641E", int(235 * fl))], [0.0, 0.5, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(wx - w2, wy - h2, wx + w2, wy + h2), skia.Paint(Shader=sh))
    # alev (pencere içinde küçük silüet): yumuşak, titrer
    fy = wy + h2 * 0.30
    lean = math.sin(t * 3.3) * 3.0 + math.sin(t * 9.1) * 1.2
    fp = skia.Path()
    fp.moveTo(wx - 5, fy + 6)
    fp.quadTo(wx - 9, fy - 8, wx + lean, fy - 22 * (0.9 + 0.1 * math.sin(t * 9.1)))
    fp.quadTo(wx + 9, fy - 8, wx + 5, fy + 6)
    fp.close()
    c.drawPath(fp, P("#FFF6D0", int(235 * fl)))
    c.drawLine(wx, wy - h2 + 8, wx, wy + h2, S("#4A2A10", 2.0, 190))                  # orta çıta
    c.drawLine(wx - w2, wy - h2 * 0.1, wx + w2, wy - h2 * 0.1, S("#4A2A10", 2.0, 190))
    c.restore()
    c.drawPath(op, S("#1A0F08", 2.4, 230))
    # taş söve
    sp = skia.Path()
    sp.addRect(skia.Rect.MakeLTRB(wx - w2 - 7, wy + h2, wx + w2 + 7, wy + h2 + 7))
    c.drawPath(sp, P(mix(wall, "#FFFFFF", 0.1)))
    # ışıma (dışa): çok büyük, yumuşak
    PN.glow(c, wx, wy, 150 * (0.75 + 0.25 * fl), "#FFB454", 0.30 * fl)
    PN.glow(c, wx, wy, 62 * (0.8 + 0.2 * fl), "#FFE29A", 0.50 * fl)


def _hill(f, T, seed=5):
    """Ön plan yamaç + selviler (koyu siluet): tepenin kendisi; villa bu platformun üstünde."""
    c = f.c
    pts = [(-2600, 830), (-1200, 826), (-60, 806), (200, 796), (500, 776), (800, 748), (1050, 722), (1200, 706), (1300, 700), (1900, 700), (2100, 706), (3200, 760), (5200, 820), (5200, 1300), (-2600, 1300)]
    path = sk.smooth_path(pts, True, 0.30)
    col = T("#2A3A33")
    c.drawPath(path, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 590), (0, 900)], [C(mix(col, "#0A1020", 0.25)), C(mix(col, "#05080F", 0.55))], [0.0, 1.0])))
    c.drawPath(path, S("#0A1008", 1.6, 200))
    rs = np.random.RandomState(seed)
    # sıra bağ/zeytin terasları (ince çizgiler) + patika
    for k in range(7):
        yy = 760 + k * 15
        pp = sk.smooth_path([(-60, yy + 52 - k * 3), (400, yy + 30 - k * 2), (900, yy - 8 - k), (1300, yy - 40 + k)], False, 0.5)
        c.drawPath(pp, S(T("#3C5040"), 1.2, 90 - k * 8))
    pth = sk.smooth_path([(1250, 702), (1120, 740), (860, 790), (500, 850), (180, 960)], False, 0.5)
    c.drawPath(pth, S(T("#6E6A52"), 9.0, 90))
    c.drawPath(pth, S(T("#8E866A"), 2.4, 70))
    for (x, y, h) in ((120, 806, 190), (260, 794, 150), (560, 774, 120), (980, 726, 130), (1250, 704, 170), (1900, 700, 160), (1990, 706, 210), (60, 812, 90)):
        SC.cypress(c, x, y, h, T("#1E2E24", 0.0), T("#3A5240", 0.0))


def _sky_img():
    """Gece gökyüzü (geniş, boya kaybı YOK): lapis degrade + yıldızlar + hilal."""
    def draw(fr):
        c = fr.c
        SC.sky_gradient(c, 4600, 640, "#070D2C", "#16266A", "#586CA8")
        rs = np.random.RandomState(11)
        for i in range(340):
            c.drawCircle(rs.uniform(0, 4600), rs.uniform(0, 420) ** 1.0, rs.uniform(0.7, 1.9), skia.Paint(AntiAlias=True, Color=C("#FFF2C4", int(rs.uniform(70, 220)))))
        mx, my = 2650, 150
        c.drawCircle(mx, my, 70, skia.Paint(AntiAlias=True, Color=C("#FFF1C0", 36), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)))
        disc = skia.Path()
        disc.addCircle(mx, my, 34)
        cut = skia.Path()
        cut.addCircle(mx - 14, my - 8, 29)
        try:
            res = skia.Op(disc, cut, skia.PathOp.kDifference_PathOp)
        except Exception:
            res = disc
        c.drawPath(res or disc, skia.Paint(AntiAlias=True, Color=C("#FFF3CE")))
    return L.bake("c10_sky", 4600, 640, draw)


@CM.ckind("c10_tepe")
def k_tepe(cx, seed=1, lit_at=0.0, scroll=70.0, ovl=None, **_):
    """Careggi tepesinden gece Floransa: uzak şehir pencere ışıklarıyla titrer, ön planda yamaç + villa, yalnız BİR pencere yanar (mum alevi titrer).
    Kamera (cam=[…look(WIN…)]) pencereye iner; zoomthru ile `careggi` odasına açılır. lit_at: pencere ışığının yandığı an (çapa)."""
    f = cx.f
    c = f.c
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    T = CT.Tint("night")
    PH = CT.PH
    Ly = CT.city_layers(PH, 1, "night")
    SP = CT.SPEEDS
    u = clamp(cx.t / max(1e-6, cx.dur), 0.0, 1.0)
    sc_ = clamp(scroll * u, 0.0, float(CT.PW_EXTRA))
    lit = smooth(clamp((cx.t - cx.at(lit_at)) / 1.2)) if lit_at is not None else 1.0
    # arka katmanlar: gökyüzü/tepe/şehir (paralaks: uzak katmanlar kamera hareketinden az etkilenir)
    cam.begin(f, layer=0.16)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-3000, SKY_Y, W + 3000, SKY_Y + PH))
    c.drawImage(_sky_img(), -1300 - sc_ * SP["sky"], SKY_Y, CM._LIN, skia.Paint(AntiAlias=True))
    c.restore()
    cam.end(f)
    cam.begin(f, layer=0.36)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-400, SKY_Y, W + 400, SKY_Y + PH))
    p = skia.Paint(AntiAlias=True)
    for key in ("hills", "far"):
        c.drawImage(Ly[key], -sc_ * SP[key], SKY_Y, CM._LIN, p)
        if key == "far":
            fx, fy = Ly["flag"]
            for k, (wx, wy, ww, wh) in enumerate(Ly["lit_far"][:18]):
                fl = clamp(0.5 + 0.9 * math.sin(cx.t * (2.4 + 0.37 * k) + k * 2.1) * math.sin(cx.t * 0.9 + k), 0.0, 1.0)
                if fl < 0.98:
                    c.drawRect(skia.Rect.MakeXYWH(wx - sc_ * SP["far"], SKY_Y + wy, ww, wh), skia.Paint(Color=C("#2A2234", int(190 * (1 - fl)))))
    c.restore()
    cam.end(f)
    # ön plan: yamaç + villa (daha güçlü paralaks)
    cam.begin(f, layer=1.0)
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-3000, SKY_Y, 5600, SKY_Y + PH))
    _hill(f, T)
    _villa(f, T, cx.t, lit)
    c.restore()
    # bant çerçevesi (asma bandı + altın şerit): yakınlaşınca ekrandan çıkar
    import cilt_orn as ORN
    px_, py_ = cam.pivot
    xa_ = px_ + (0 - px_ - cam.dx) / cam.s - 60
    xb_ = px_ + (W - px_ - cam.dx) / cam.s + 60
    for yy in (SKY_Y - 40, SKY_Y + PH):
        ORN.band_vine(f, xa_, yy, xb_, 40, alpha=1.0)
        c.drawLine(xa_, yy + (40 if yy < SKY_Y else 0), xb_, yy + (40 if yy < SKY_Y else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9))
    cam.end(f)
    # ışık havuzu: pencere çevresi (kamera yaklaştıkça havuz büyür)
    wxs, wys = cam_xy(cam, WIN[0], WIN[1], 1.0)
    z = max(1.0, cam.s)
    base = CM.candle_light(cx.t, seed, base=(wxs, wys), r=lerp(1500.0, 900.0 * min(z, 3.0) ** 0.55 + 420.0, smooth(clamp((z - 1.0) / 2.0))), sway=6.0 * z)
    CM.finish(f, cx, motes_n=20, light=base)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V1/V4 · Careggi odası ═════════════════════════════
GOLD = OD.GOLD
Y_FL, OV_, LH, F_WALL, F_FG = OD.Y_FL, OD.OV, OD.LH, OD.F_WALL, OD.F_FG


def lying_man(f, x, y, t, turn=0.0, color="#16100A", rim="#E8A860", rim_dir=1, scale=1.0, breath=1.0):
    """Yatakta yatan erkek SİLÜETİ (yandan; baş solda yastıkta, burun-çene çıkıntısı yüz ayrıntısı DEĞİL; örtü altında omuz/kalça/ayak kabarıklıkları). turn 0→1: yavaşça
    duvara döner (kabarıklık yükselir, baş çökmüş, profil kaybolur). (x,y) = yastığın alt-sol köşesi."""
    c = f.c
    b = 1.0 + 0.04 * math.sin(t * 1.1) * breath
    s = scale
    k = smooth(clamp(turn))
    sup = [(40, 8), (46, -22), (64, -52), (96, -62), (136, -58), (176, -46), (214, -50), (252, -48), (292, -40), (330, -44), (366, -34), (398, -24), (410, -6), (410, 8)]
    sid = [(40, 8), (44, -18), (60, -42), (96, -60), (140, -76), (190, -82), (240, -74), (290, -62), (336, -50), (372, -36), (398, -22), (410, -6), (410, 8), (410, 8)]
    pts = [(sup[i][0] * (1 - k) + sid[i][0] * k, sup[i][1] * (1 - k) + sid[i][1] * k) for i in range(len(sup))]
    hd = (4, -64, 62, -12)
    hd2 = (10, -52, 64, -2)
    hdr = [hd[i] * (1 - k) + hd2[i] * k for i in range(4)]

    def mound(dx, dy, col):
        q = [(x + (px * s) + dx, y + (py * s * (b if py < -4 else 1.0)) + dy) for px, py in pts]
        p = sk.smooth_path(q, True, 0.42)
        c.drawPath(p, P(col))
        h_ = skia.Path()
        h_.addOval(skia.Rect.MakeLTRB(x + hdr[0] * s + dx, y + hdr[1] * s + dy, x + hdr[2] * s + dx, y + hdr[3] * s + dy))
        c.drawPath(h_, P(col))
        nose = 1.0 - k                                              # burun/çene profili (yüz ayrıntısı yok: düz çıkıntı) duvara dönünce kaybolur
        if nose > 0.02:
            n_ = skia.Path()
            n_.moveTo(x + 56 * s + dx, y - 50 * s + dy)
            n_.lineTo(x + (62 + 9 * nose) * s + dx, y - 40 * s + dy)
            n_.lineTo(x + 58 * s + dx, y - 33 * s + dy)
            n_.close()
            c.drawPath(n_, P(col))
    if rim:
        mound(1.6 * rim_dir, -1.8, rim)
    mound(0, 0, color)


def _door_path(x, yb, w, h):
    r = w / 2
    p = skia.Path()
    p.moveTo(x - w / 2, yb)
    p.lineTo(x - w / 2, yb - h + r)
    p.arcTo(skia.Rect.MakeLTRB(x - w / 2, yb - h, x + w / 2, yb - h + 2 * r), 180, 180, False)
    p.lineTo(x + w / 2, yb)
    p.close()
    return p


class Careggi(OD.Room):
    """Careggi odası (Lorenzo'nun son günleri; V1/V4): yatak (başlık+tester, bordo örtü), arkada haç, sağda kemerli pencere (gece), masa + mum + kitaplar, solda kitaplık,
    sağda taş kapılı geçit. Yatan siluet `figure="lying"` (turn_at=çapa → duvara döner), diğer figürler `actors` ile (siluet). Yüz/ceset/ışık iddiası yok (mum = görsel dil)."""
    name = "careggi"
    PW = 2800
    BX0, BYB = 700, 785
    WIN_X, DOOR_X, TBL = 2000, 2470, (1340, 1540)
    CAND = (1440, 698)
    PILLOW = (700 + 62 + 6, 785 - 156)

    def build(self):
        self.layer("wall", F_WALL, self.Lw(F_WALL), self._draw_wall, wear=3)
        self.layer("main", 1.0, self.PW, self._draw_main, scale=1.2)
        self.layer("fg", F_FG, self.Lw(F_FG), self._draw_fg)

    def paths(self):
        return {"default": [(0.0, (1250, 0, 1.0)), (1.0, (1120, 0, 1.12))],
                "bed": [(0.0, (1150, 0, 1.0)), (1.0, (960, 50, 1.55))],
                "window": [(0.0, (1650, 0, 1.0)), (1.0, (2000, 20, 1.5))],
                "door": [(0.0, (1500, 0, 1.0)), (1.0, (2200, 0, 1.12))],
                "sweep_r": [(0.0, (900, 0, 1.03)), (1.0, (1700, 0, 1.03))]}

    def _draw_wall(self, fr, xa, xb):
        c, T = fr.c, self.T
        wx = self.wx
        OD.GRAD_V(c, xa, OV_ - 40, xb, Y_FL + 30, [(T("#9C8864"), 0.0), (T("#B09A74"), 1.0)])
        OD.plaster(c, xa, xb, OV_ - 40, Y_FL + 30, T, "#9C8864", "#B8A47C", amp=0.05, warm=(255, 244, 218), cool=(70, 50, 30))
        OD.cornice(c, xa, xb, 72, T, col="#5A4630", plaster="#9C8864", gold=False)
        OD.wainscot(c, xa, xb, Y_FL - 130, Y_FL + 18, T, "#4A3220", pw=180, seed=4)
        if OD._vis(wx(self.WIN_X), 260, xa, xb):
            OD.draw_window(c, T, wx(self.WIN_X), 205, 176, 350, night=True, shutters=True)
        if OD._vis(wx(1000), 60, xa, xb):
            OD.draw_crucifix(c, T, wx(1020), 215, 1.3)
        if OD._vis(wx(380), 260, xa, xb):
            OD.draw_bookcase(c, T, wx(400), 190, 440, 520, rows=4, seed=3, empty_frac=0.0)
        if OD._vis(wx(1700), 120, xa, xb):
            OD.draw_hanging(c, T, wx(1560), wx(1700), 235, 520, "#3A4A6A", GOLD, seed=5, damask=False) if False else None
        sh = OD.LGP((0, Y_FL - 30), (0, Y_FL + 30), [("#0A0F1A", 0.0, 0), ("#0A0F1A", 1.0, 80)])
        c.drawRect(skia.Rect.MakeLTRB(xa, Y_FL - 30, xb, Y_FL + 30), sh)

    def _draw_main(self, fr, xa, xb):
        c, T = fr.c, self.T
        OD.floor_planks(c, xa, xb, Y_FL, LH, T, "#4E3822", seed=4)
        if OD._vis(self.BX0 + 300, 340, xa, xb):
            OD.draw_bed(c, T, self.BX0, self.BYB, 560, 500, 190, cover=("#5A1E28", GOLD), tester=True, wood="#3E2814")
        if OD._vis(self.DOOR_X, 140, xa, xb):
            OD.doorway_stone(c, T, self.DOOR_X, 790, 170, 440)
        if OD._vis(sum(self.TBL) / 2, 120, xa, xb):
            x0t, x1t = self.TBL
            OD.BOX(c, x0t, 700, x1t, 716, "#4A2E18", T, ink=1.4)
            for lx in (x0t + 14, x1t - 14):
                OD.R(c, lx - 5, 716, lx + 5, 800, T("#3E2814"))
                OD.INKR(c, lx - 5, 716, lx + 5, 800, 1.1, 190)
            OD.draw_book(c, x0t + 30, 700, 72, 14, "#6A2E24")
            OD.draw_book(c, x0t + 34, 686, 62, 12, "#233C8C")
        if OD._vis(1780, 100, xa, xb):
            OD.draw_chest(c, T, 1700, 1880, 790, 106, "#3E2814")

    def _draw_fg(self, fr, xa, xb):
        c, T = fr.c, self.T
        fx = lambda x: W / 2 + (x - W / 2) * F_FG
        for x in (40, 2760):
            if OD._vis(fx(x), 90, xa, xb):
                xx = fx(x)
                OD.R(c, xx - 26, OV_ - 40, xx + 26, 900, "#1A100A")
                OD.HGRAD(c, xx - 26, OV_ - 40, xx + 26, 900, [("#FFFFFF", 0.0, 22), ("#000000", 1.0, 80)])

    def dyn_wall(self, ctx):
        f, t = ctx.f, ctx.t
        wx = self.wx
        if OD._vis(wx(self.WIN_X), 420, ctx.xa, ctx.xb):
            OD.window_light(f, wx(self.WIN_X), 222, 150, 300, t, dx=-300, y_floor=Y_FL + 20, a=0.12, seed=3, patch=False, dust=8, night=True, part="shaft")

    def dyn_main(self, ctx):
        f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
        T = self.T
        o = ctx.opts
        OD.window_light(f, self.WIN_X, 222, 150, 300, t, dx=-300, y_floor=Y_FL + 70, a=0.12, seed=3, patch=True, dust=0, night=True, part="patch", patch_h=110)
        # kapı açıklığı: koridor karanlığı + uzaktan solgun mavi
        if OD._vis(self.DOOR_X, 140, ctx.xa, ctx.xb):
            op = _door_path(self.DOOR_X, 790, 170, 440)
            c.save()
            c.clipPath(op, skia.ClipOp.kIntersect, True)
            c.drawRect(skia.Rect.MakeLTRB(self.DOOR_X - 90, 340, self.DOOR_X + 90, 792), OD.LGP((0, 340), (0, 792), [("#0A0E22", 0.0), ("#1A2448", 1.0)]))
            PN.glow(c, self.DOOR_X, 700, 150, "#7F96D8", 0.10)
            c.restore()
        # yatan siluet
        fig = o.get("figure", "lying")
        if fig:
            px, py = self.PILLOW
            turn = cx.amt(o["turn_at"], float(o.get("turn_dur", 2.4))) if "turn_at" in o else float(o.get("turn", 0.0))
            lying_man(f, px + 8, py + 10, t, turn=turn, color="#16100A", rim="#E8A860", rim_dir=1)
        # masa üstü: tüy kalem + mum
        cx_, cy_ = self.CAND
        lit = float(o.get("candle_lit", 1.0))
        if "snuff_at" in o:
            lit *= 1.0 - cx.amt(o["snuff_at"], 0.35)
        OD.quill(c, self.TBL[0] + 124, 696, -14.0, 0.5)
        OD.candle(f, cx_, cy_, 62, t, seed=2.2, lit=lit, holder=True)
        OD.draw_extra(ctx, "back")
        OD.dust_motes(c, t, cx_ - 260, cy_ - 240, cx_ + 260, cy_ + 30, n=12, seed=31, a=0.5, size=1.7, drift=(4, -2), col="#FFE2A0")

    def dyn_front(self, ctx):
        f, t = ctx.f, ctx.t
        OD.draw_extra(ctx, "front")
        if OD._vis(self.BX0 + 580, 120, ctx.xa, ctx.xb):
            OD.draw_drape(ctx.c, self.BX0 + 560 + 14, self.BYB - 492 + 28 + 30, 74, 395, t, col="#5A1E28", col2=GOLD, amp=0.04, seed=4, ph=1.1, tie=0.62)

    def dyn_fg(self, ctx):
        c, t = ctx.c, ctx.t
        rs = OD._RS(49)
        xa, xb = ctx.xa, ctx.xb
        for k in range(12):
            x = xa + ((rs.rand() * (xb - xa) + t * 10 * (0.5 + rs.rand())) % (xb - xa))
            y = 120 + rs.rand() * 700 + math.sin(t * 0.6 + k) * 14
            c.drawCircle(x, y, 1.6 + 2.0 * rs.rand(), OD.PT("#FFEFC4", int(30 + 50 * rs.rand())))

    def light(self, ctx):
        return (1180, 650, 1000.0, 1.0)

    def after_finish(self, ctx):
        fn = ctx.opts.get("after")
        if fn is not None:
            fn(ctx)


OD.ROOMS["careggi"] = Careggi


# ═════════════════════════════ V1 s6 / V2 · mektup sayfası ═════════════════════════════
@CM.ckind("c10_mektup")
def k_mektup(cx, at=0.0, n=10, dur=3.6, ghosts=(), seed=5, w=820, h=880, candle_xy=(1500, 720), page_xy=(780, 560), ovl=None, mono=0.0, **_):
    """Mektup sayfası (okunmaz satırlar tüy kalemle kendini yazar) + yanında mum. ghosts: kenar boşluğuna beliren/solan soluk işaretler (mektupta OLMAYAN şeyi göstermek için).
    Mum alevi sabit bir ekran konumundadır (eşleşmeli kesme: alev → alev)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="top", push=0.0, drift=(0.0, 0.0), mono=mono)
    k = cx.amt(at, 0.8)
    L.draw_letter(f, cx, page_xy[0], page_xy[1], w, h, at, rot=-0.03, n=n, dur=dur, seed=seed, k=k, ghosts=ghosts, off=0.3)
    fx, fy, br = OD.candle(f, candle_xy[0], candle_xy[1], 150, cx.t, seed=4.1, lit=1.0, holder=True)
    OD.dust_motes(c, cx.t, candle_xy[0] - 300, candle_xy[1] - 360, candle_xy[0] + 300, candle_xy[1] + 20, n=10, seed=17, a=0.5, size=1.8, drift=(4, -2), col="#FFE2A0")
    L.end(cx, cam, mono=mono, motes_n=12, light=CM.candle_light(cx.t, seed, base=(page_xy[0] + 260, 560), r=1250.0, sway=6.0))
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ kütüphane (boş raf yuvaları SABİT: önbellek anahtarı ayrı) ═════════════════════════════
class C10Lib(OD.Calisma):
    """San Marco/Medici kütüphanesi: raf yuvalarının ~%58'i BOŞ (c10 V1: «kütüphanesi bitmeden»). Ayrı oda adı → ayrı kareaş önbelleği (empty_frac sabit)."""
    name = "c10lib"

    def _empty_frac(self):
        return 0.58


OD.ROOMS["c10lib"] = C10Lib


# ═════════════════════════════ V2/V6 · kürsü (nave panoramasında istasyon) ═════════════════════════════
def pict_whip(c, x, y, s, a=1.0, t=0.0):
    """Kırbaç piktogramı (altın-umber): sarmalı sap + üç düğümlü ince kuyruk (sallanır)."""
    c.save()
    c.translate(x, y)
    c.rotate(-18)
    h0, h1 = -s * 0.52, s * 0.10
    c.drawRoundRect(skia.Rect.MakeLTRB(-s * 0.06, h0, s * 0.06, h1), 8, 8, P("#6A4220", int(255 * a)))
    c.drawRoundRect(skia.Rect.MakeLTRB(-s * 0.06, h0, s * 0.06, h1), 8, 8, S("#1A0F06", 2.0, int(220 * a)))
    for q in range(6):                                                                   # sarma bantları
        yy = h0 + (q + 0.5) * (h1 - h0) / 6
        c.drawLine(-s * 0.06, yy, s * 0.06, yy + 5, S("#D8B060", 2.0, int(200 * a)))
    c.drawCircle(0, h0 - 4, s * 0.075, P("#D8B060", int(255 * a)))
    c.drawCircle(0, h0 - 4, s * 0.075, S("#1A0F06", 1.6, int(220 * a)))
    for k, dx in enumerate((-0.07, 0.0, 0.07)):
        p = skia.Path()
        p.moveTo(dx * s, h1)
        sw = math.sin(t * 2.6 + k * 1.4) * s * 0.07
        ex = dx * s * 3.2 + s * (0.12 - 0.12 * k) + sw
        p.cubicTo(dx * s + s * 0.20 + sw, h1 + s * 0.22, ex - s * 0.20, h1 + s * 0.40, ex, h1 + s * (0.70 + 0.08 * k))
        c.drawPath(p, S("#1A0F06", 5.0, int(220 * a)))
        c.drawPath(p, S("#B07A38", 2.4, int(255 * a)))
        for qq in (0.42, 0.70, 1.0):
            pts = sk.smooth_path([(dx * s, h1), (dx * s + s * 0.20 + sw, h1 + s * 0.22), (ex - s * 0.20, h1 + s * 0.40), (ex, h1 + s * (0.70 + 0.08 * k))], False, 0.5)
        ex2, ey2 = ex, h1 + s * (0.70 + 0.08 * k)
        c.drawCircle(ex2, ey2, s * 0.034, P("#E8C25A", int(255 * a)))
        c.drawCircle(ex2, ey2, s * 0.034, S("#1A0F06", 1.4, int(220 * a)))
    c.restore()


def pict_flood(c, x, y, s, a=1.0, t=0.0):
    """Tufan piktogramı (lapis): üst üste dalga şeritleri + köpük kıvrımları."""
    for k in range(4):
        yy = y - s * 0.30 + k * s * 0.20
        p = skia.Path()
        n = 14
        for i in range(n + 1):
            u = i / n
            xx = x - s * 0.62 + u * s * 1.24
            yv = yy + math.sin(u * 9.0 + t * 2.2 + k * 1.3) * s * 0.06
            if i == 0:
                p.moveTo(xx, yv)
            else:
                p.lineTo(xx, yv)
        p.lineTo(x + s * 0.62, yy + s * 0.30)
        p.lineTo(x - s * 0.62, yy + s * 0.30)
        p.close()
        c.drawPath(p, P(["#4E78C8", "#3A62B4", "#2A4C98", "#1E3A7E"][k], int(235 * a)))
        c.drawPath(p, S("#0E1A44", 1.8, int(200 * a)))
        for q in range(3):
            fx = x - s * 0.45 + q * s * 0.42 + math.sin(t * 1.4 + q + k) * 6
            c.drawCircle(fx, yy - s * 0.03 + math.sin(t * 2.2 + q) * 3, s * 0.035, P("#EAF2FF", int(190 * a)))


def pict_pop(cx, at, dur=0.5):
    """Belirme eğrisi (0→1, taşmalı)."""
    k = clamp((cx.t - cx.at(at)) / dur)
    return k, sk.back_out(k) if k < 1 else 1.0


def pulpit(f, x, yg, t, tint=1.0):
    """Taş kürsü (sağdan görünüm; sol yanda merdiven): ayak sütunu + altıgen kasa (kemerli panel) + ahşap korkuluk. (x,yg) = taban merkezi; dönüş: (kasa üst y, merdiven (x0,y0,x1,y1))."""
    c = f.c
    stone, stone2 = "#A6A08A", "#8A846E"
    top = yg - 260
    # merdiven (sola, yükselen basamaklar)
    sx0, sy0 = x - 250, yg
    sx1, sy1 = x - 78, top + 110
    steps = 7
    for i in range(steps):
        u0, u1 = i / steps, (i + 1) / steps
        xa, xb = sx0 + (sx1 - sx0) * u0, sx0 + (sx1 - sx0) * u1
        ya = sy0 + (sy1 - sy0) * u1
        c.drawRect(skia.Rect.MakeLTRB(xa, ya, xb + 2, yg), P(mix(stone, "#000000", 0.10 + 0.04 * (i % 2))))
        c.drawLine(xa, ya, xb + 2, ya, S("#F4EAD0", 2.0, 150))
        c.drawRect(skia.Rect.MakeLTRB(xa, ya, xb + 2, yg), S("#2A1E10", 1.1, 150))
    c.drawLine(sx0, sy0 - 150, sx1, sy1 - 90, S("#4A3018", 7.0, 240))                    # küpeşte
    c.drawLine(sx0, sy0 - 150, sx1, sy1 - 90, S("#C79A3C", 2.0, 160))
    # ayak sütunu
    c.drawRect(skia.Rect.MakeLTRB(x - 44, top + 130, x + 44, yg), P(stone2))
    c.drawRect(skia.Rect.MakeLTRB(x - 56, yg - 26, x + 56, yg), P(stone))
    c.drawRect(skia.Rect.MakeLTRB(x - 44, top + 130, x + 44, yg), S("#2A1E10", 1.4, 180))
    # kasa (altıgen tub: yukarı genişleyen yamuk)
    tub = sk.poly_path([(x - 78, top + 4), (x + 98, top + 4), (x + 76, top + 138), (x - 56, top + 138)])
    c.drawPath(tub, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x - 78, 0), (x + 98, 0)], [C("#C4BCA2"), C(stone), C("#6E6852")], [0.0, 0.5, 1.0])))
    c.save()
    c.clipPath(tub, skia.ClipOp.kIntersect, True)
    for k in range(3):                                                                      # kemerli paneller
        px0 = x - 64 + k * 56
        ap = skia.Path()
        ap.moveTo(px0, top + 126)
        ap.lineTo(px0, top + 62)
        ap.arcTo(skia.Rect.MakeLTRB(px0, top + 40, px0 + 44, top + 84), 180, 180, False)
        ap.lineTo(px0 + 44, top + 126)
        ap.close()
        c.drawPath(ap, P("#5A5242", 150))
        c.drawPath(ap, S("#2A1E10", 1.3, 180))
    c.restore()
    c.drawPath(tub, S("#2A1E10", 2.0, 220))
    c.drawRect(skia.Rect.MakeLTRB(x - 92, top - 14, x + 112, top + 6), P("#5A3A1E"))
    c.drawRect(skia.Rect.MakeLTRB(x - 92, top - 14, x + 112, top + 6), S("#2A1608", 1.4, 200))
    c.drawLine(x - 90, top - 8, x + 110, top - 8, S("#C79A3C", 1.6, 170))
    return top, (sx0, sy0, sx1, sy1)


def st_pulpit(ctx, st):
    """Kürsü istasyonu (pano nave): Savonarola SİLÜETİ merdivenden çıkar (climb_at), kürsüde konuşur; piktogramlar (kılıç/kırbaç/tufan: syms) cümlede belirir; ateş/meclis (extra) için `fn2`.
    st: x, climb_at (çapa), syms=[(ad, çapa)], who ('sav'|'clerk'), cheer_at."""
    f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
    x = st["x"]
    yg = 836
    top, (sx0, sy0, sx1, sy1) = pulpit(f, x, yg, t)
    who = st.get("who", "sav")
    t_climb = cx.at(st["climb_at"]) if st.get("climb_at") is not None else -9.0
    u = clamp((t - t_climb) / 1.9)
    kind = "kesis" if who == "sav" else "banker"
    col = "#0A0604"
    H_ = 262
    if u < 1.0 and st.get("climb_at") is not None:
        ux = ease_io(u)
        px = sx0 - 30 + ((x - 8) - (sx0 - 30)) * ux
        py = yg - (yg - (top + 120)) * clamp(ux * 1.15)
        OD.sil_actor(f, kind, px, py, H_, t, dir=1, seed=12, color=col, rim="#E8A860", rim_dir=-1, walker=70.0 if 0.0 < u < 1.0 else 0.0)
    elif u >= 1.0 or st.get("climb_at") is None:
        sym_t = [cx.at(a_) for _, a_ in st.get("syms", [])]
        pointing = any(0.0 <= t - s_ < 1.5 for s_ in sym_t)
        if pointing:
            OD.sil_actor(f, kind, x - 8, top + 120, H_, t, action="point", dir=1, seed=12, color=col, rim="#E8A860", rim_dir=-1, t0=min(s_ for s_ in sym_t if 0.0 <= t - s_ < 1.5), dur=1.4, target=(0.15, -1.0))
        else:
            OD.sil_actor(f, kind, x - 8, top + 120, H_, t, action="talk", dir=1, seed=12, color=col, rim="#E8A860", rim_dir=-1, energy=1.5)
    # kasanın önü korkuluğun altında kalsın: tekrar ön yüzü çiz (figürün belden aşağısını örter)
    tubf = sk.poly_path([(x - 78, top + 4), (x + 98, top + 4), (x + 76, top + 138), (x - 56, top + 138)])
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x - 100, top - 2, x + 120, top + 150))
    c.drawPath(tubf, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x - 78, 0), (x + 98, 0)], [C("#C4BCA2"), C("#A6A08A"), C("#6E6852")], [0.0, 0.5, 1.0])))
    for k in range(3):
        px0 = x - 64 + k * 56
        ap = skia.Path()
        ap.moveTo(px0, top + 126)
        ap.lineTo(px0, top + 62)
        ap.arcTo(skia.Rect.MakeLTRB(px0, top + 40, px0 + 44, top + 84), 180, 180, False)
        ap.lineTo(px0 + 44, top + 126)
        ap.close()
        c.drawPath(ap, P("#5A5242", 150))
        c.drawPath(ap, S("#2A1E10", 1.3, 180))
    c.drawPath(tubf, S("#2A1E10", 2.0, 220))
    c.drawRect(skia.Rect.MakeLTRB(x - 92, top - 14, x + 112, top + 6), P("#5A3A1E"))
    c.drawRect(skia.Rect.MakeLTRB(x - 92, top - 14, x + 112, top + 6), S("#2A1608", 1.4, 200))
    c.drawLine(x - 90, top - 8, x + 110, top - 8, S("#C79A3C", 1.6, 170))
    c.restore()
    # piktogramlar: kürsünün üstünde, sırayla belirir
    nsy = len(st.get("syms", []))
    for i, (nm, a_) in enumerate(st.get("syms", [])):
        k, kb = pict_pop(cx, a_, 0.55)
        if k <= 0.003:
            continue
        sx = x + 24 + (i - (nsy - 1) / 2.0) * 250
        sy = top - 235 - 14 * math.sin(t * 1.3 + i) + (1 - ease_out(k)) * 60
        sc = 150.0 * (0.4 + 0.6 * kb)
        PN.glow(c, sx, sy, sc * 1.4, "#FFD27A", 0.30 * k)
        if nm == "sword":
            icons.draw_icon(f, "sword", sx, sy, size=sc * 1.25, metal="gold", alpha=k, rot=0.0)
        elif nm == "whip":
            pict_whip(c, sx, sy, sc, k, t)
        elif nm == "flood":
            pict_flood(c, sx, sy, sc, k, t)
        elif nm == "flame":
            icons.draw_icon(f, "torch", sx, sy, size=sc * 1.2, metal="gold", alpha=k)
        elif nm == "hall":
            icons.draw_icon(f, "pillars", sx, sy, size=sc * 1.2, metal="gold", alpha=k)
        elif nm == "bag":
            icons.draw_icon(f, "coinbag", sx, sy, size=sc * 1.1, metal="gold", alpha=k)


# ═════════════════════════════ V2 s9 · kırmızı yerine kandan şapka (ANEKDOT, gravür + sinabar) ═════════════════════════════
def draw_galero(c, x, y, s, col="#A8321E", a=1.0, rot=0.0, tassels=1.0, wet=0.0):
    """Kardinal şapkası (galero), önden: geniş yassı kenar + sığ tepe + iki yanda sarkan kordon ve püsküller (satır satır). wet>0: ıslak pigment parlaması (kan DEĞİL: boya)."""
    if a <= 0.003:
        return
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(math.degrees(rot))
    al = int(255 * a)
    dark = mix(col, "#000000", 0.38)
    # kordonlar + püsküller (kenarın iki ucundan aşağı)
    for sg in (-1, 1):
        cp = skia.Path()
        cp.moveTo(sg * s * 0.92, s * 0.04)
        cp.cubicTo(sg * s * 1.10, s * 0.30, sg * s * 0.98, s * 0.62, sg * s * 0.94, s * 0.98 * tassels + 0.001)
        c.drawPath(cp, S("#1A0F08", 3.4, int(al * 0.9)))
        for r in range(5):
            if r / 5.0 > tassels:
                break
            yy = s * (0.36 + r * 0.16)
            for q in range(r + 1):
                xx = sg * s * (0.96 + 0.02 * r) + (q - r / 2.0) * s * 0.07
                c.drawCircle(xx, yy, s * 0.032, P(col, al))
                c.drawCircle(xx, yy, s * 0.032, S("#1A0F08", 1.0, int(al * 0.8)))
    # kenar alt yüzü + üst yüzü
    brim = skia.Path()
    brim.addOval(skia.Rect.MakeLTRB(-s, -s * 0.18, s, s * 0.20))
    c.drawPath(brim, P(dark, al))
    top = skia.Path()
    top.addOval(skia.Rect.MakeLTRB(-s * 0.98, -s * 0.20, s * 0.98, s * 0.10))
    c.drawPath(top, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-s, -s * 0.2), (s, s * 0.1)], [C(mix(col, "#FFFFFF", 0.22), al), C(col, al), C(dark, al)], [0.0, 0.5, 1.0])))
    c.drawPath(top, S("#1A0F08", 2.0, int(al * 0.85)))
    # tepe
    cr = skia.Path()
    cr.moveTo(-s * 0.46, -s * 0.06)
    cr.quadTo(-s * 0.52, -s * 0.70, 0, -s * 0.72)
    cr.quadTo(s * 0.52, -s * 0.70, s * 0.46, -s * 0.06)
    cr.quadTo(0, s * 0.04, -s * 0.46, -s * 0.06)
    cr.close()
    c.drawPath(cr, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((-s * 0.18, -s * 0.46), s * 0.9, [C(mix(col, "#FFFFFF", 0.28), al), C(col, al), C(dark, al)], [0.0, 0.55, 1.0])))
    c.drawPath(cr, S("#1A0F08", 2.0, int(al * 0.85)))
    if wet > 0.01:
        c.drawOval(skia.Rect.MakeLTRB(-s * 0.28, -s * 0.62, -s * 0.02, -s * 0.38), P("#FFFFFF", int(70 * wet * a)))
    c.restore()


@CM.ckind("c10_sapka")
def k_sapka(cx, seed=9, hood_at=0.0, papa_at=0.0, hat_at=0.0, offer_at=0.0, refuse_at=0.0, strike_at=0.0, blood_at=0.0, settle_at=0.0, ovl=None, **_):
    """ANEKDOT (gravür; şapkalar sinabar pigment): solda tiaralı papa siluet-madalyası, sağda kukuletalı Savonarola siluet-madalyası. Kırmızı galero papadan Savonarola'ya UZANIR (offer_at),
    o başını çevirir (refuse_at), kırmızı şapkanın üstüne ink çizgisi çekilir (strike_at), yerine koyu şarap-kırmızısı (kan rengi pigment) şapka belirir (blood_at) ve kukuletanın üstünde durur (settle_at)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.0, drift=(0.0, 0.0), mono=1.0)
    t = cx.t
    xl, xr, ym, Rm = 520, 1400, 590, 205
    kl, kr = cx.amt(papa_at, 0.9), cx.amt(hood_at, 0.9)
    ref = cx.amt(refuse_at, 0.8)
    L.sil_medal(f, xl, ym, Rm * (0.9 + 0.1 * ease_out(kl)), hat="tiara", alpha=kl, tilt=0.025 * math.sin(t * 0.7), nose=1.0)
    L.sil_medal(f, xr, ym, Rm * (0.9 + 0.1 * ease_out(kr)), hat="hood", alpha=kr, tilt=0.025 * math.sin(t * 0.6 + 1.0) + 0.10 * ref, flip=True, nose=1.0)
    L.end(cx, cam, mono=1.0, motes_n=14, light=CM.candle_light(t, seed, base=(W / 2, 520), r=1500.0, sway=8.0))
    # renkli vurgu (gravürden sonra, aynı kamerada)
    cam.begin(f)
    ka = cx.amt(hat_at, 0.7)
    ko = ease_io(clamp((t - cx.at(offer_at)) / 1.3))
    kb = cx.amt(blood_at, 0.8)
    kst = ease_out(clamp((t - cx.at(strike_at)) / 0.5), 2)
    hx = lerp(xl + 230, xr - 330, ko)
    hy = 360 - 60 * math.sin(ko * math.pi) + 8 * math.sin(t * 1.7)
    ks = 1.0 - kb * 0.0
    if ka > 0.003:
        out = 1.0 - smooth(clamp((t - cx.at(blood_at)) / 0.6))
        draw_galero(c, hx, hy, 118 * (0.5 + 0.5 * ease_out(ka)), "#B02A1C", a=ka * out, rot=-0.08 + 0.12 * ko, wet=0.6)
        if kst > 0.01 and out > 0.02:
            pa = f.paint("#1A0F08", style="stroke", sw=9.0, alpha=0.92 * out)
            CM.wobble(pa, 8.0, 1.4, 4)
            c.drawLine(hx - 150 * kst + 60, hy + 60 - 120 * kst, hx - 150 + 60 + 300 * kst * 0.5 + 0, hy - 60 + 0, pa) if False else c.drawLine(hx - 130, hy + 70, hx - 130 + 260 * kst, hy + 70 - 140 * kst, pa)
    if kb > 0.003:
        ks2 = ease_out(clamp((t - cx.at(settle_at)) / 1.2))
        bx = lerp(hx, xr + 10, ks2)
        by = lerp(hy, ym - 255, ks2)
        PN.glow(c, bx, by, 190, "#6E0E0E", 0.30 * kb)
        draw_galero(c, bx, by, 126 * (0.5 + 0.5 * ease_out(kb)), "#6E0E0E", a=kb, rot=0.05, wet=1.0)
    cam.end(f)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V3 s11 · ittifak ağı (Floransa ve Napoli bağdan çıkar) ═════════════════════════════
@CM.ckind("c10_ittifak")
def k_ittifak(cx, seed=3, web_at=0.0, break_at=0.0, ring_at=0.0, out_at=0.0, ovl=None, **_):
    """Denge ağı: beş düğüm (Floransa, Napoli + üç adsız) altın iplerle bağlı → ipler çözülür (break_at) → üç düğüm yeni, sıkı bir halka kurar (ring_at: «ittifak») →
    Floransa ve Napoli küçülüp dışarı itilir, onlara giden iplik söner (out_at). Adsız düğümlerin kimliği söylenmez (kaynak: üyeler söylenmez)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="top", push=0.03, drift=(5.0, 2.0))
    t = cx.t
    P5 = {"F": (560, 600), "N": (1360, 640), "A": (760, 360), "B": (1160, 330), "C": (960, 760)}
    # yeni halka: A,B,C merkeze yaklaşır
    kr = ease_io(clamp((t - cx.at(ring_at)) / 1.6))
    ko = ease_io(clamp((t - cx.at(out_at)) / 1.5))
    P_ = {}
    for k_, (x, y) in P5.items():
        if k_ in "ABC":
            cxn, cyn = 960, 540
            P_[k_] = (lerp(x, cxn + (x - cxn) * 0.62, kr), lerp(y, cyn + (y - cyn) * 0.62, kr))
        elif k_ == "F":
            P_[k_] = (lerp(x, x - 230, ko), lerp(y, y + 90, ko))
        else:
            P_[k_] = (lerp(x, x + 230, ko), lerp(y, y + 90, ko))
    kw = cx.amt(web_at, 1.2)
    kbrk = ease_in(clamp((t - cx.at(break_at)) / 1.2))
    pairs = [("F", "A"), ("F", "B"), ("F", "C"), ("F", "N"), ("N", "A"), ("N", "B"), ("N", "C"), ("A", "B"), ("B", "C"), ("A", "C")]
    for (a_, b_) in pairs:
        xa, ya = P_[a_]
        xb, yb = P_[b_]
        in_ring = a_ in "ABC" and b_ in "ABC"
        outer = not in_ring
        if outer:
            k = kw * (1.0 - kbrk)
            col = "#C79A3C"
            wd = 4.0
            if kbrk > 0.02 and ko > 0:
                k *= 1.0 - ko
        else:
            k = kw * (1.0 - kbrk * (1.0 - kr * 1.0)) if kr < 0.01 else kw * (1.0 - kbrk * (1.0 - kr))
            col = "#E8C25A" if kr > 0.5 else "#C79A3C"
            wd = 4.0 + 5.0 * kr
        if k <= 0.01:
            continue
        mx_, my_ = (xa + xb) / 2, (ya + yb) / 2
        sag = 18 * math.sin(t * 1.3 + xa * 0.01) * (1.0 - k) * 4.0
        p = skia.Path()
        p.moveTo(xa, ya)
        p.quadTo(mx_, my_ + sag, xb, yb)
        pa = f.paint(col, style="stroke", sw=wd, alpha=0.95 * k)
        if kbrk > 0.02 and outer:
            pa.setPathEffect(skia.DashPathEffect.Make([16, 12 + 30 * kbrk], -t * 24))
        c.drawPath(p, pa)
        c.drawPath(p, f.paint("#FFFFFF", style="stroke", sw=max(1.2, wd * 0.25), alpha=0.25 * k))
    # halka vurgusu
    if kr > 0.02:
        rx = sum(P_[k_][0] for k_ in "ABC") / 3
        ry = sum(P_[k_][1] for k_ in "ABC") / 3
        rr = 250 * (0.8 + 0.2 * kr)
        c.drawCircle(rx, ry, rr, f.paint("#E8C25A", style="stroke", sw=3.0 + 4 * kr, alpha=0.55 * kr))
        PN.glow(c, rx, ry, rr * 1.3, "#E8C25A", 0.12 * kr)
    # düğümler
    for k_, (x, y) in P_.items():
        base = cx.amt(web_at, 0.7, off={"F": 0.0, "N": 0.15, "A": 0.3, "B": 0.45, "C": 0.6}[k_])
        if base <= 0.003:
            continue
        s = 150.0
        if k_ in "FN":
            s *= 1.0 - 0.38 * ko
        gray = ko if k_ in "FN" else 0.0
        c.save()
        c.translate(x, y)
        f.circle(4, 8, s * 0.5, color="#000000", alpha=0.28 * base, blur=6)
        col_a, col_b = ("#F1E3B8", "#C79A3C") if k_ in "ABC" else ("#E6D2A0", "#9A7A38")
        if gray > 0:
            col_a, col_b = mix(col_a, "#8A8A88", gray), mix(col_b, "#5A5A58", gray)
        c.drawCircle(0, 0, s * 0.5, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((-s * 0.15, -s * 0.2), s * 0.8, [C(col_a, int(255 * base)), C(col_b, int(255 * base)), C(mix(col_b, "#000000", 0.45), int(255 * base))], [0.0, 0.55, 1.0])))
        c.drawCircle(0, 0, s * 0.5, S("#2A1A0C", 3.0, int(230 * base)))
        c.restore()
        icn = {"F": "fleur", "N": "crown", "A": "castle", "B": "tower", "C": "shield"}[k_]
        icons.draw_icon(f, icn, x, y, size=s * 0.62, metal="bronze" if gray < 0.5 else "lead", alpha=base, shadow=False)
    # adlar (yalnız Floransa ve Napoli)
    xf, yf = P_["F"]
    xn, yn = P_["N"]
    L.tag("FLORANSA", xf, yf + 128, ("c10s11", "Floransa", -0.1), size=32, w=300)(cx)
    L.tag("NAPOLİ", xn, yn + 128, ("c10s11", "Napoli", -0.1), size=32, w=270)(cx)
    cam.end(f)
    CM.finish(f, cx, motes_n=20)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V4 s19 · Fransisken kılığı (kardinal → rahip) ═════════════════════════════
@CM.ckind("c10_kilik")
def k_kilik(cx, seed=5, walk_at=0.0, door_x=1022, rev=True, x0=1650.0, sp=170.0, tags=None, ovl=None, **_):
    """Dar sokak, taş kemerli yan kapı: kırmızı giysili KARDİNAL (rev: sağdan sola = düşüş/çıkış yönü) yürür, kapı sövesinin ardından geçerken solar; öte yanda kahverengi
    FRANSİSKEN kılığı belirir ve çıkıp gider. Alay yok, yüz yok (profil figür). `walk_at`: yürüyüşün başladığı an (çapa); `tags=dict(card=çapa, fran=çapa)`: izleyen levhalar."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress=None, push=0.04, drift=(0.0, 0.0))
    t = cx.t
    T = OD.OTint("night")
    yb = 840
    d = -1 if rev else 1
    # sokak zemini + taş duvar
    OD.floor_planks(c, -200, 2300, 800, 1000, T, "#4A4038", seed=3, w0=200.0)
    OD.ashlar(c, -200, 2300, 140, 800, T, "#8A7E68", 64.0, seed=2)
    OD.cornice(c, -200, 2300, 130, T, col="#5A4A34", plaster="#8A7E68", gold=False)
    OD.doorway_stone(c, T, door_x, yb - 50, 190, 400)
    # kapı açıklığı: karanlık + sıcak sızıntı
    op = _door_path(door_x, yb - 50, 190, 400)
    c.save()
    c.clipPath(op, skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(door_x - 100, 300, door_x + 100, 800), OD.LGP((0, 300), (0, 800), [("#0A0814", 0.0), ("#2A1A12", 1.0)]))
    PN.glow(c, door_x, 640, 150, "#FFB454", 0.22)
    c.restore()
    # meşale demirleri (iki yanda)
    for sx in (door_x - 320, door_x + 320):
        OD.sconce(c, T, sx, 400, 1.2, 1 if sx > door_x else -1)
        OD.candle(f, sx + (40 if sx > door_x else -40), 420, 40, t, seed=sx * 0.01, holder=False, smoke=False)
    # figürler: kardinal (renkli) → kapı sövesinde kaybolur; fransisken (kahverengi) kapıdan sonra çıkar
    w0 = cx.at(walk_at)
    xw = x0 + d * sp * max(0.0, t - w0)
    jx = door_x + 135 if rev else door_x - 135                                    # söve merkezi: geçiş (kardinal → rahip) sövenin ardında olur
    fade = clamp((d * (xw - jx) + 85.0) / 170.0)
    h_ = 372
    if fade < 1.0:
        FA.walker(f, "kardinal", xw, yb, h_, t, speed=sp if t > w0 else 0.0, dir=d, seed=52, alpha=1.0 - smooth(fade))
    if fade > 0.0:
        FA.walker(f, "kesis", xw, yb, h_ * 0.97, t, speed=sp * 0.8, dir=d, seed=7, alpha=smooth(clamp((fade - 0.2) / 0.8)), robe="#6B4A2E", robe2="#C9B58A", hat="hood", hat_col="#6B4A2E", beard=None)
    # kapı sövesi ön plan (figürün kapıdan geçtiği hissi)
    jx0 = door_x + 110 if rev else door_x - 160
    c.drawRect(skia.Rect.MakeLTRB(jx0, 300, jx0 + 50, 800), P(T("#8A7E68"), 255))
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=CM.candle_light(t, seed, base=(door_x * 0.8, 560), r=1100.0, sway=8.0))
    if tags:
        fx = xw + 0.0
        ty = yb - h_ - 70
        if tags.get("card") is not None:
            L.tag("GİOVANNİ", fx, ty, tags["card"], size=32, w=330, sub="kardinal", out=tags.get("fran"), out_dur=0.35)(cx)
        if tags.get("fran") is not None:
            L.tag("FRANSİSKEN RAHİBİ", fx, ty, tags["fran"], size=30, w=440, sub="sade kılık", off=0.1)(cx)
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V4 s17 · Piero şehirden kaçar (sokak istasyonu: at + toz) ═════════════════════════════
def st_piero(ctx, st):
    """Sokak istasyonu: Piero kapının önünde durur (`turn_at`: kapıya sırtını döner); `flee_at` çapasında SOLA (düşüş/kaçış yönü) koşarak gider (toz + pelerin). `?` simgesi (`ask_at`..`ask_out`): iç dünya bilinmez.
    At YOK (\"atına atlayıp\" ANEKDOT, söylenmez): yaya koşu. st: x (kapı önü), flee_at, ask_at, ask_out, turn_at."""
    f, c, t, cx = ctx.f, ctx.c, ctx.t, ctx.cx
    x = st["x"]
    yg = 846
    tf = cx.at(st["flee_at"])
    tt = cx.at(st["turn_at"]) if st.get("turn_at") is not None else tf
    stil = dict(robe="#6E1A22", robe2="#D2A33E", hat_col="#1A1008")
    if t < tf:
        FA.walker(f, "soylu", x, yg - 6, 224, t, speed=0.0, dir=1 if t < tt else -1, seed=2, **stil)
        ka = cx.amt(st["ask_at"], 0.6) * (1.0 - cx.amt(st["ask_out"], 0.5))
        if ka > 0.01:
            icons.draw_icon(f, "question", x + 6, yg - 292 + math.sin(t * 2.0) * 6, size=116, metal="bronze", alpha=0.95 * ka, glow=0.0)
        if tt - 0.2 < t < tt + 0.5:                                           # dönüş anı: küçük toz
            ph = clamp((t - tt + 0.2) / 0.7)
            FA._puff(c, x - 18, yg - 10 - ph * 16, 16 + 30 * ph, 0.35 * (1 - ph), "#CDB98E")
    else:
        u = t - tf
        v = 60.0 + 420.0 * clamp(u / 0.9)
        xr = x - (60.0 * u + 0.5 * 420.0 * min(u, 0.9) ** 2 / 0.9 + max(0.0, u - 0.9) * 420.0)
        for k in range(10):                                                  # toz izi: ayaklardan geriye
            ph = clamp((u - 0.05 * k) / 1.3)
            if 0 < ph < 1:
                FA._puff(c, xr + 40 + k * 30 + ph * 50, yg - 12 - ph * 26, 16 + 36 * ph, 0.5 * (1 - ph) ** 1.2, "#CDB98E")
        FA.walker(f, "soylu", xr, yg - 6, 224, t, speed=v, dir=-1, seed=2, **stil)


# ═════════════════════════════ V5 s21 · Charles'ın girişi: yatay mızrak ═════════════════════════════
def lance_prop(length=7.5):
    """Atlının eline yatay tutulan mızrak (mızrak yatay çizgi): sap + çelik uç + kırlangıç flama. hk.u = atın birim boyu."""
    def prop(c, hk):
        u = hk.u
        hx, hy = 0.31 * u, -0.27 * u
        c.save()
        c.translate(hx, hy)
        L_ = u * length
        c.drawRect(skia.Rect.MakeLTRB(-0.3 * u, -0.028 * u, L_, 0.028 * u), P("#6A4A2C"))
        c.drawRect(skia.Rect.MakeLTRB(-0.3 * u, -0.028 * u, L_, 0.028 * u), S("#1A0F08", 1.2, 200))
        tip = sk.poly_path([(L_, -0.07 * u), (L_ + 0.42 * u, 0), (L_, 0.07 * u)])
        c.drawPath(tip, P("#B8BCC4"))
        c.drawPath(tip, S("#1A0F08", 1.2, 220))
        fl = sk.poly_path([(L_ - 0.5 * u, -0.028 * u), (L_ - 1.4 * u, -0.30 * u), (L_ - 1.15 * u, -0.10 * u), (L_ - 1.4 * u, 0.10 * u), (L_ - 0.5 * u, 0.028 * u)])
        c.drawPath(fl, P("#233C8C"))
        c.drawPath(fl, S("#1A0F08", 1.2, 200))
        c.restore()
    return prop


def st_king(ctx, st):
    """Fransa Kralı (atlı, lacivert kaparişli, yatay mızrak) ve maiyeti: sağdan sola yavaş yürüyüş (istila = düşüş yönü). x dünya konumu zamanla `speed` ile akar.
    st: x (t=0 konumu), speed, len; foot=n (yaya mızrakçı). Yüz yok; kral: yalnız silüet/kaparis/mızrak."""
    f, c, t = ctx.f, ctx.c, ctx.t
    sp = st.get("speed", 60.0)
    x = st["x"] - sp * t
    for i in range(st.get("foot", 3)):                                               # arka sıra: yaya mızrakçılar (yatay mızrak yerine dik mızrak = alay ritmi)
        FA.walker(f, "asker", x + 520 + i * 118, 846 + 5 * (i % 2), 214, t, speed=sp, dir=-1, seed=21 + i, phase=0.37 * i, prop="spear", robe=["#233C8C", "#2A4A9A", "#1E3478"][i % 3], robe2="#E8C25A", hat_col="#5A5A60")
    FA.rider(f, x + 300, 846, 300, t, speed=sp, gait="walk", dir=-1, seed=8, coat="#B8B0A0", cloth="#233C8C", cl_pat=("fleur", "#E8C25A"), robe="#233C8C", robe2="#E8C25A", hat="beret", hat_col="#233C8C", prop=lance_prop(st.get("len", 7.0) * 0.9))
    FA.rider(f, x, 846, 330, t, speed=sp, gait="walk", dir=-1, seed=3, coat="#EFE8DA", cloth="#233C8C", cl_pat=("fleur", "#E8C25A"), robe="#233C8C", robe2="#E8C25A", hat="beret", hat_col="#E8C25A", prop=lance_prop(st.get("len", 7.5)))


# ═════════════════════════════ V5 s22 · Capponi taslağı yırtar; trompete çanla yanıt (ANEKDOT, gravür) ═════════════════════════════
def _tear_line(h, seed=4, amp=26.0, n=14):
    """Taslağın ortasından geçen tırtıklı yırtık çizgisi (yerel koordinat: x ofseti; y −h/2 … h/2)."""
    rs = np.random.RandomState(seed)
    ys = [-h / 2 + h * i / n for i in range(n + 1)]
    xs = [rs.uniform(-amp, amp) * (0.4 if i in (0, n) else 1.0) for i in range(n + 1)]
    return list(zip(xs, ys))


def draw_sheet(c, w, h, seed=3, a=1.0):
    """Şart taslağı: parşömen sayfa + okunmaz satırlar + imza bloğu (mono katmanında çizilir)."""
    r = skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2)
    al = int(255 * a)
    c.drawRect(r, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-w / 2, -h / 2), (w / 2, h / 2)], [C("#EFE4C6", al), C("#D8C9A0", al)], [0.0, 1.0])))
    c.drawRect(r, S("#4A3A24", 2.2, int(210 * a)))
    rs = np.random.RandomState(seed)
    c.drawRect(skia.Rect.MakeLTRB(-w / 2 + 44, -h / 2 + 46, w / 2 - 44, -h / 2 + 50), P("#3A2616", int(150 * a)))
    n = 10
    for i in range(n):
        y = -h / 2 + 96 + i * (h - 230) / n
        L.scribble(c, -w / 2 + 44, w / 2 - 44 - (rs.rand() * 90 if i % 3 == 2 else 0.0), y, seed=seed * 11 + i, col="#3A2616", a=int(175 * a), amp=3.0, w=2.2)
    c.drawCircle(w / 2 - 78, h / 2 - 66, 34, P("#5A3A22", int(230 * a)))
    c.drawCircle(w / 2 - 78, h / 2 - 66, 34, S("#2A1608", 2.0, int(230 * a)))
    L.scribble(c, -w / 2 + 50, -w / 2 + 190, h / 2 - 56, seed=seed + 90, col="#3A2616", a=int(190 * a), amp=6.0, w=2.6)


def trumpet(c, x, y, s, rot=0.0, a=1.0, col="#C79A3C"):
    """Düz trompet pictogramı (yatay, çan solda): ağızlık sağda, uzun boru, kıvrım, geniş çan. s: boru uzunluğunun yarısı."""
    if a <= 0.003:
        return
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    al = int(255 * a)
    dark = mix(col, "#000000", 0.45)
    tube = skia.Path()
    tube.moveTo(s, 0)
    tube.lineTo(-s * 0.55, 0)
    tube.cubicTo(-s * 0.7, -s * 0.30, -s * 0.52, -s * 0.30, -s * 0.46, -s * 0.12)
    c.drawPath(tube, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=s * 0.10, Color=C(dark, al), StrokeCap=skia.Paint.kRound_Cap))
    c.drawPath(tube, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=s * 0.065, Color=C(col, al), StrokeCap=skia.Paint.kRound_Cap))
    bell = sk.poly_path([(-s * 0.52, -s * 0.05), (-s * 1.02, -s * 0.34), (-s * 1.05, s * 0.34), (-s * 0.52, s * 0.05)])
    c.drawPath(bell, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-s, -s * 0.3), (-s * 0.5, s * 0.3)], [C(mix(col, "#FFFFFF", 0.35), al), C(col, al), C(dark, al)], [0.0, 0.5, 1.0])))
    c.drawPath(bell, S("#1A0F08", 2.0, int(al * 0.9)))
    c.drawOval(skia.Rect.MakeLTRB(-s * 1.08, -s * 0.34, -s * 0.98, s * 0.34), P(dark, al))
    c.drawRect(skia.Rect.MakeLTRB(s * 0.92, -s * 0.07, s * 1.06, s * 0.07), P(dark, al))
    c.restore()


def sound_rays(c, x, y, r0, n, k, phase, a, col="#E8C25A", spread=1.0, direction=-1, w=5.0):
    """Trompet ışınları: çan yönünde yayılan kısa yaylar (k: 0..1 yayılma)."""
    if a <= 0.003 or k <= 0.0:
        return
    for i in range(n):
        ph = (phase + i / n) % 1.0
        rr = r0 + 360 * ph
        al = a * (1 - ph) ** 1.2
        if al < 0.02:
            continue
        p = skia.Path()
        ang0, ang1 = (180 - 34 * spread, 180 + 34 * spread) if direction < 0 else (-34 * spread, 34 * spread)
        p.addArc(skia.Rect.MakeLTRB(x - rr, y - rr, x + rr, y + rr), ang0, ang1 - ang0)
        c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * (1 - 0.5 * ph), Color=C(col, int(255 * al * k)), StrokeCap=skia.Paint.kRound_Cap))


def _hall(c, t):
    """Gravür salon dekoru (mono katmanında): iki sütun, geride kemer, taş zemin. Yalnız y 160–930 (altyazı bandı boş)."""
    for x0 in (96, 1754):
        c.drawRect(skia.Rect.MakeLTRB(x0, 190, x0 + 72, 868), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x0, 0), (x0 + 72, 0)], [C("#A89A78"), C("#D4C8A6"), C("#8A7C5C")], [0.0, 0.45, 1.0])))
        c.drawRect(skia.Rect.MakeLTRB(x0 - 14, 168, x0 + 86, 196), P("#8A7C5C"))
        c.drawRect(skia.Rect.MakeLTRB(x0 - 14, 856, x0 + 86, 884), P("#8A7C5C"))
        c.drawRect(skia.Rect.MakeLTRB(x0, 190, x0 + 72, 868), S("#3A2E1A", 2.0, 170))
        for k in range(4):
            c.drawLine(x0 + 12 + k * 16, 204, x0 + 12 + k * 16, 852, S("#3A2E1A", 1.2, 70))
    arch = skia.Path()
    arch.moveTo(520, 860)
    arch.lineTo(520, 470)
    arch.arcTo(skia.Rect.MakeLTRB(520, 190, 1400, 750), 180, 180, False)
    arch.lineTo(1400, 860)
    c.drawPath(arch, S("#6A5A3A", 34.0, 70))
    c.drawPath(arch, S("#3A2E1A", 2.0, 150))
    c.drawRect(skia.Rect.MakeLTRB(0, 868, W, 930), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 868), (0, 930)], [C("#B8A988", 255), C("#7A6C50", 255)], [0.0, 1.0])))
    c.drawLine(0, 868, W, 868, S("#3A2E1A", 2.0, 170))
    for k in range(9):
        c.drawLine(120 + k * 210, 868, 60 + k * 240, 930, S("#3A2E1A", 1.2, 90))


@CM.ckind("c10_capponi")
def k_capponi(cx, seed=6, cap_at=0.0, king_at=0.0, sheet_at=0.0, tear_at=0.0, trumpet_at=0.0, bell_at=0.0, ovl=None, **_):
    """ANEKDOT (gravür): solda Capponi (siluet madalya), sağda kral (siluet madalya); aralarında kralın şart taslağı (sheet_at'ta kral tarafından kayarak gelir).
    tear_at: taslak Capponi'nin önünde yırtılır (kısa duraksama → iki yarı savrulur). trumpet_at: kral tarafında trompet ışınları; bell_at: Capponi tarafında çanlar sallanır, halkaları
    trompet ışınlarını bastırır (karşılığında çanla yanıt). Ses yok; ışın/halka görsel dilidir."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.045, drift=(6.0, 3.0), mono=1.0)
    t = cx.t
    _hall(c, t)
    xl, xr, ym, Rm = 470, 1450, 610, 196
    kc, kk = cx.amt(cap_at, 0.9), cx.amt(king_at, 0.9)
    t_tear = cx.at(tear_at)
    ft = clamp((t - t_tear) / 1.0)
    kb = cx.amt(bell_at, 0.7)
    kt = cx.amt(trumpet_at, 0.6)
    lean = 0.06 * ease_out(clamp((t - cx.at(sheet_at)) / 1.2)) * (1.0 - ft) + 0.035 * ft
    L.sil_medal(f, xl, ym, Rm * (0.9 + 0.1 * ease_out(kc)), hat="cap", alpha=kc, tilt=0.025 * math.sin(t * 0.7) + lean * 0.6 * (1 + 0.7 * kb), nose=1.0)
    L.sil_medal(f, xr, ym, Rm * (0.9 + 0.1 * ease_out(kk)), hat="helm", alpha=kk, tilt=0.025 * math.sin(t * 0.6 + 1.0) - 0.05 * kb - 0.02 * math.sin(t * 7.0) * kt * (1 - kb), flip=True, nose=1.0)
    # taslak: sağdan (kral) gelir → ortada durur → yırtılır
    ks = ease_io(clamp((t - cx.at(sheet_at)) / 1.3))
    sw_, sh_ = 380, 520
    sx = lerp(xr - 120, 960, ks)
    sy = ym + 6 - 70 * math.sin(ks * math.pi) + 5 * math.sin(t * 1.3) * (1 - ft)
    sa = cx.amt(sheet_at, 0.5)
    if sa > 0.003:
        if ft <= 0.0:
            c.save()
            c.translate(sx, sy)
            c.rotate(math.degrees(0.03 * math.sin(t * 1.1) + 0.05 * (1 - ks)))
            f.circle(8, 14, sw_ * 0.5, color="#000000", alpha=0.20 * sa, blur=16)
            draw_sheet(c, sw_, sh_, a=sa)
            c.restore()
        else:
            tl = _tear_line(sh_)
            crack = clamp(ft * 3.0)                                                 # 0..1: çatlak yukarıdan aşağı çizilir (tek duraklama)
            sep = ease_out(clamp((ft - 0.28) / 0.72), 2.2)
            fade = 1.0 - smooth(clamp((t - t_tear - 1.2) / 1.0))
            for sgn in (-1, 1):
                if fade <= 0.01:
                    continue
                poly = [(tx, ty) for (tx, ty) in tl]
                if sgn < 0:
                    pts = [(-sw_ / 2 - 4, -sh_ / 2)] + poly + [(-sw_ / 2 - 4, sh_ / 2)]
                else:
                    pts = [(sw_ / 2 + 4, -sh_ / 2)] + poly + [(sw_ / 2 + 4, sh_ / 2)]
                pth = sk.poly_path(pts)
                c.save()
                c.translate(sx + sgn * (6 + 190 * sep), sy + 80 * sep ** 2)
                c.rotate(math.degrees(sgn * (0.02 + 0.34 * sep)))
                c.clipPath(pth, skia.ClipOp.kIntersect, True)
                f.circle(8, 14, sw_ * 0.5, color="#000000", alpha=0.16 * fade, blur=16)
                draw_sheet(c, sw_, sh_, a=fade)
                c.restore()
                c.save()
                c.translate(sx + sgn * (6 + 190 * sep), sy + 80 * sep ** 2)
                c.rotate(math.degrees(sgn * (0.02 + 0.34 * sep)))
                ep = skia.Path()
                ep.moveTo(*poly[0])
                for q in poly[1:]:
                    ep.lineTo(*q)
                c.drawPath(ep, S("#F6EEDA", 3.0, int(210 * fade)))
                c.restore()
            if sep < 0.5:                                                          # çatlak çizgisi (kısa, koyu)
                cp = skia.Path()
                m = max(1, int(len(tl) * crack))
                cp.moveTo(sx + tl[0][0], sy + tl[0][1])
                for q in tl[1:m + 1]:
                    cp.lineTo(sx + q[0], sy + q[1])
                c.drawPath(cp, S("#1A0F08", 4.0, int(255 * (1 - sep * 2))))
            if 0.0 < ft < 0.9:                                                     # kâğıt tozu/kıymıkları
                for i in range(14):
                    rs = np.random.RandomState(i + 5)
                    ph = clamp((t - t_tear - 0.25 - 0.02 * i) / 1.3)
                    if 0 < ph < 1:
                        dx = rs.uniform(-1, 1) * 260 * ph
                        dy = -60 + 220 * ph ** 2 + rs.uniform(-40, 40) * ph
                        c.save()
                        c.translate(sx + dx, sy + dy)
                        c.rotate(math.degrees(rs.uniform(-3, 3) * ph))
                        c.drawRect(skia.Rect.MakeLTRB(-8, -5, 8, 5), P("#E8DDBF", int(220 * (1 - ph))))
                        c.restore()
    # trompetler (kral tarafı): iki çapraz trompet + ışınlar; çanlar gelince ışınlar solar
    ty_ = 250
    tx_ = xr - 20
    suppress = ease_in(clamp((t - cx.at(bell_at) - 0.5) / 1.6))
    if kt > 0.003:
        pop = ease_out(kt)
        for sg, rot in ((-1, -0.18), (1, 0.18)):
            trumpet(c, tx_ + sg * 0.0, ty_ + sg * 62, 175 * (0.6 + 0.4 * pop), rot=rot + 0.03 * math.sin(t * 9.0 + sg) * (1 - suppress), a=kt * (1.0 - 0.55 * suppress))
        sound_rays(c, tx_ - 190, ty_ + 6, 50, 4, kt * (1.0 - suppress), t * 0.9, 0.95, direction=-1, spread=1.0, w=8.0)
    # çanlar (Capponi tarafı): sallanan iki çan + büyüyen halkalar
    if kb > 0.003:
        bx, by = xl + 10, 250
        for i, (dx, sc, ph) in enumerate(((-110, 1.0, 0.0), (120, 0.84, 1.7))):
            sw = math.sin(t * 4.2 + ph) * 0.34 * min(1.0, (t - cx.at(bell_at)) * 1.2 + 0.2)
            c.save()
            c.translate(bx + dx, by - 90)
            c.rotate(math.degrees(sw))
            icons.draw_icon(f, "bell", 0, 120, size=240 * sc * (0.7 + 0.3 * ease_out(kb)), metal="bronze", alpha=kb)
            c.restore()
        for i in range(5):
            ph = ((t - cx.at(bell_at)) * 0.8 - i * 0.22) % 1.1
            if t < cx.at(bell_at):
                break
            rr = 70 + 520 * ph
            al = (1 - ph / 1.1) ** 1.3 * kb
            if al > 0.03:
                c.drawCircle(bx, by + 40, rr, S("#E8C25A", 8.0 * (1 - ph * 0.5), int(255 * al * 0.85)))
    L.end(cx, cam, mono=1.0, motes_n=14, light=CM.candle_light(t, seed, base=(W / 2, 520), r=1500.0, sway=8.0))
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V5 s23 · Büyük Konsey: yurttaş siluetleri sırayla yerine oturur ═════════════════════════════
_BUST_COLS = ["#1E1612", "#261A16", "#1A1A22", "#221A1C", "#2A2018", "#1C2018"]


def _bust_img(var):
    col = _BUST_COLS[var % 6]
    hat = var % 3

    def draw(fr):
        c = fr.c
        sh = skia.Path()
        sh.moveTo(2, 84)
        sh.cubicTo(4, 54, 18, 45, 32, 45)
        sh.cubicTo(46, 45, 60, 54, 62, 84)
        sh.close()
        c.drawPath(sh, P(col))
        c.drawRect(skia.Rect.MakeLTRB(26, 36, 38, 50), P(col))
        c.drawOval(skia.Rect.MakeLTRB(19, 9, 47, 43), P(col))
        if hat == 1:                                                    # berretto
            hp = skia.Path()
            hp.moveTo(16, 24)
            hp.cubicTo(16, 2, 50, 0, 49, 22)
            hp.lineTo(44, 24)
            hp.cubicTo(36, 14, 26, 14, 20, 26)
            hp.close()
            c.drawPath(hp, P(mix(col, "#000000", 0.35)))
        elif hat == 2:                                                  # mazzocchio benzeri yuvarlak şapka
            c.drawOval(skia.Rect.MakeLTRB(14, 8, 52, 26), P(mix(col, "#000000", 0.30)))
        c.drawPath(sh, S(mix(col, "#E8B878", 0.4), 1.4, 140))
        c.drawOval(skia.Rect.MakeLTRB(19, 9, 47, 43), S(mix(col, "#E8B878", 0.4), 1.2, 110))
    return L.bake(("c10bust", var), 64, 86, draw)


@CM.ckind("c10_konsey")
def k_konsey(cx, seed=7, fill_at=0.0, ovl=None, rows=8, **_):
    """Büyük Konsey salonu (ön cephe): arkada kemerli duvar, perspektifli zemin, sıra sıra bank. Yurttaş siluetleri (yüz yok) ortadan dışa, önden arkaya DALGA halinde yerlerine oturur
    (fill_at: dalganın başladığı an). Sayı/etiket bindirmeyle. Salon üstü y<470 boş (etiket/sayaç alanı)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.045, drift=(8.0, 0.0))
    t = cx.t
    # arka duvar: kemer dizisi
    c.drawRect(skia.Rect.MakeLTRB(120, 470, 1800, 560), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 470), (0, 560)], [C("#B9A980"), C("#8A7A58")], [0.0, 1.0])))
    for i in range(9):
        ax = 200 + i * 190
        ap = skia.Path()
        ap.moveTo(ax - 62, 560)
        ap.lineTo(ax - 62, 410)
        ap.arcTo(skia.Rect.MakeLTRB(ax - 62, 348, ax + 62, 472), 180, 180, False)
        ap.lineTo(ax + 62, 560)
        ap.close()
        c.drawPath(ap, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 350), (0, 560)], [C("#3A2E22"), C("#6A5A44")], [0.0, 1.0])))
        c.drawPath(ap, S("#2A1E10", 2.2, 200))
        c.drawRect(skia.Rect.MakeLTRB(ax + 62, 360, ax + 128, 560), P("#A39270"))
    c.drawRect(skia.Rect.MakeLTRB(120, 540, 1800, 560), P("#7A6A48"))
    # zemin: perspektif tahta çizgileri
    gp = skia.Path()
    gp.addPoly([skia.Point(120, 560), skia.Point(1800, 560), skia.Point(1920, 930), skia.Point(0, 930)], True)
    c.drawPath(gp, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 560), (0, 930)], [C("#8A7452"), C("#B79C6C")], [0.0, 1.0])))
    for k in range(-8, 9):
        c.drawLine(960 + k * 70, 560, 960 + k * 150, 930, S("#4A3A20", 1.3, 80))
    # sıralar: arkadan öne
    R_ = rows
    items = []
    for r in range(R_):
        yb = 586 + r * (290.0 / (R_ - 1)) * (1 + 0.05 * r / R_)
        s = 0.55 + 0.15 * r
        n = int(1560 / (62 * s))
        x0 = 960 - n * 62 * s / 2
        for k in range(n):
            x = x0 + (k + 0.5) * 62 * s
            if abs(x - 960) < 70 * s:
                continue
            var = int((r * 7 + k * 13 + seed) % 6)
            dly = 0.9 * abs(x - 960) / 800.0 + 0.9 * (R_ - 1 - r) / R_ + ((k * 37 + r * 11) % 10) * 0.012
            items.append((r, yb, s, x, var, dly))
    for r in range(R_):
        yb = 586 + r * (290.0 / (R_ - 1)) * (1 + 0.05 * r / R_)
        s = 0.55 + 0.15 * r
        # bank şeridi (satırın önünde)
        c.drawRect(skia.Rect.MakeLTRB(130 - 7 * r, yb + 8, 1790 + 7 * r, yb + 8 + 7 + 1.2 * r), P("#5A3E22"))
        for (r2, yb2, s2, x, var, dly) in items:
            if r2 != r:
                continue
            k = cx.amt(fill_at, 0.30, off=dly)
            if k <= 0.003:
                continue
            im = _bust_img(var)
            sc = s2 * 1.12 * (0.35 + 0.65 * ease_out(k))
            L.blit(c, im, x + math.sin(t * 0.9 + x * 0.05) * 0.8, yb2 + 30 * s2 * (1.0 - ease_out(k)), a=k, sx=sc, ax=0.5, ay=1.0)
        c.drawRect(skia.Rect.MakeLTRB(130 - 7 * r, yb + 8, 1790 + 7 * r, yb + 8 + 7 + 1.2 * r), P("#5A3E22"))
    cam.end(f)
    CM.finish(f, cx, motes_n=16, light=CM.candle_light(t, seed, base=(W / 2, 420), r=1500.0, sway=8.0))
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V5 s24 · salon planı (bank sıraları) + Savonarola (kesikli: «yazılır») ═════════════════════════════
@CM.ckind("c10_plan")
def k_plan(cx, seed=4, draw_at=0.0, draw_dur=2.4, sav_at=0.0, arrow_at=0.0, ovl=None, **_):
    """Salon PLANI (kuşbakışı): parşömen sayfada dış duvar, sütunlar, iki blok bank sırası, merkezde koridor, uçta kürsü; mürekkeple kendini çizer (draw_at..draw_dur).
    Solda kukuletalı Savonarola siluet-madalyası KESİKLİ halkayla (kaynak «yazılır»: kesinlik yok), plana uzanan kesikli ok (arrow_at: «belirleyici»)."""
    f, c, cam = L.begin(cx, bg="wall", seed=seed, dress="both", push=0.04, drift=(-6.0, 2.0))
    t = cx.t
    px, py, pw, ph = 1080, 540, 1160, 700
    k0 = cx.amt(draw_at, 0.5)
    kp = ease_io(clamp((t - cx.at(draw_at)) / draw_dur))
    # sayfa
    c.save()
    c.translate(px, py)
    c.rotate(-1.2 + 0.4 * math.sin(t * 0.5))
    f.circle(10, 16, pw * 0.5, color="#000000", alpha=0.20 * k0, blur=20)
    r = skia.Rect.MakeLTRB(-pw / 2, -ph / 2, pw / 2, ph / 2)
    c.drawRect(r, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-pw / 2, -ph / 2), (pw / 2, ph / 2)], [C("#EFE4C6", int(255 * k0)), C("#D8C9A0", int(255 * k0))], [0.0, 1.0])))
    c.drawRect(r, S("#4A3A24", 2.4, int(220 * k0)))
    c.drawLine(-pw / 2, 4, pw / 2, 4, S("#8A7850", 1.6, int(70 * k0)))            # orta kıvrım
    ink = "#3A2616"
    # dış duvar (kapanan dikdörtgen)
    x0, x1, y0, y1 = -pw / 2 + 80, pw / 2 - 80, -ph / 2 + 80, ph / 2 - 80
    wall = skia.Path()
    wall.addRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    pe = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6.0, Color=C(ink, int(235 * k0)), StrokeJoin=skia.Paint.kMiter_Join)
    ln = 2 * ((x1 - x0) + (y1 - y0))
    pe.setPathEffect(skia.DashPathEffect.Make([max(0.1, ln * clamp(kp * 1.6)), ln], 0))
    c.drawPath(wall, pe)
    # sütunlar
    for i in range(9):
        kk = clamp(kp * 2.4 - 0.3 - i * 0.05)
        if kk <= 0:
            continue
        for yy in (y0 + 26, y1 - 26):
            c.drawCircle(x0 + 70 + i * (x1 - x0 - 140) / 8, yy, 9 * ease_out(kk), P(ink, int(220 * k0)))
    # banklar: iki blok, 7 sıra, her sıra kısa dikdörtgenler
    for blk in (-1, 1):
        for row in range(7):
            yy = y0 + 110 + row * 62
            kk = clamp(kp * 3.0 - 0.6 - row * 0.12 - (0.1 if blk > 0 else 0.0))
            if kk <= 0:
                continue
            xa = (x0 + 150) if blk < 0 else (60 + 20)
            xb = (-60 - 20) if blk < 0 else (x1 - 150)
            xe = xa + (xb - xa) * ease_out(kk)
            c.drawRect(skia.Rect.MakeLTRB(xa, yy, xe, yy + 24), P("#B89A66", int(255 * k0)))
            c.drawRect(skia.Rect.MakeLTRB(xa, yy, xe, yy + 24), S(ink, 2.2, int(230 * k0)))
    # kürsü (sağ uç, yarım daire) + giriş oku (sol)
    kd = clamp(kp * 2.8 - 1.4)
    if kd > 0:
        dais = skia.Path()
        dais.arcTo(skia.Rect.MakeLTRB(x1 - 150, -70, x1 - 10, 70), -90, 180 * kd, True)
        c.drawPath(dais, S(ink, 6.0, int(235 * k0)))
        c.drawCircle(x1 - 80, 0, 14 * ease_out(kd), P("#A8321E", int(240 * k0)))
    c.restore()
    # Savonarola: kesikli halka (kaynak: yazılır)
    ks = cx.amt(sav_at, 0.9)
    xs_, ys_, Rs = 330, 560, 190
    if ks > 0.003:
        L.sil_medal(f, xs_, ys_ - 4 * math.sin(t * 1.2), Rs * (0.9 + 0.1 * ease_out(ks)), hat="hood", alpha=ks, tilt=0.03 * math.sin(t * 0.8), nose=1.0)
        ring = skia.Path()
        ring.addCircle(xs_, ys_, Rs + 18)
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#A8321E", int(235 * ks)))
        pr.setPathEffect(skia.DashPathEffect.Make([20, 14], -t * 18))
        c.drawPath(ring, pr)
    # kesikli ok: madalyadan plana
    ka = ease_out(clamp((t - cx.at(arrow_at)) / 1.1))
    if ka > 0.01:
        ap = skia.Path()
        ap.moveTo(xs_ + Rs + 30, ys_ - 40)
        ap.cubicTo(xs_ + Rs + 120, ys_ - 190, px - 330, py - 170, px - 200, py - 40)
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6.0, Color=C("#A8321E", int(240 * ka)), StrokeCap=skia.Paint.kRound_Cap)
        L_ = 900.0
        pa.setPathEffect(skia.DashPathEffect.Make([22, 14], -t * 30))
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(xs_ + Rs + 10, 0, xs_ + Rs + 30 + (px - 200 - xs_ - Rs) * ka, H))
        c.drawPath(ap, pa)
        c.restore()
        if ka > 0.95:
            hp = sk.poly_path([(px - 200, py - 40), (px - 236, py - 76), (px - 168, py - 80)])
            c.drawPath(hp, P("#A8321E", 235))
    cam.end(f)
    CM.finish(f, cx, motes_n=14, light=CM.candle_light(t, seed, base=(W * 0.55, 480), r=1500.0, sway=8.0))
    if ovl is not None:
        ovl(cx)


# ═════════════════════════════ V6 s27 · «Botticelli yaktı» şakası: boş çerçeve + KANIT YOK ═════════════════════════════
def blank_frame(c, x, y, w, h, a=1.0, rot=0.0, burn=0.0, q=0.0, t=0.0):
    """BOŞ yaldızlı tablo çerçevesi (içi çıplak keten; hiçbir resim çizilmez → Botticelli kopyası yok). burn: 0..1 kızarıp kararır; q: «?» görünürlüğü."""
    if a <= 0.003:
        return
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(rot))
    al = int(255 * a)
    o = skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2)
    i = skia.Rect.MakeLTRB(-w / 2 + 22, -h / 2 + 22, w / 2 - 22, h / 2 - 22)
    c.drawRect(o.makeOffset(6, 10), P("#000000", int(70 * a)))
    c.drawRect(o, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(-w / 2, -h / 2), (w / 2, h / 2)], [C("#F0D27A", al), C("#C79A3C", al), C("#8A6A22", al)], [0.0, 0.5, 1.0])))
    c.drawRect(o, S("#3A2A10", 2.4, al))
    c.drawRect(i, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, -h / 2), (0, h / 2)], [C("#E6DCC0", al), C("#CDBF9C", al)], [0.0, 1.0])))
    c.drawRect(i, S("#4A3A20", 2.0, al))
    for sx_ in (-1, 1):                                                     # köşe süsleri
        for sy_ in (-1, 1):
            c.drawCircle(sx_ * (w / 2 - 11), sy_ * (h / 2 - 11), 8, P("#8A6A22", al))
    if q > 0.01:
        icons.draw_icon(FA_FRAME(c), "question", 0, 4, size=min(w, h) * 0.55, metal="bronze", alpha=q * a, glow=0.0)
    if burn > 0.01:
        c.drawRect(o, P("#FF7A1A", int(150 * burn * a)))
        c.drawRect(o, P("#1A0F08", int(170 * max(0.0, burn - 0.3) * a)))
    c.restore()


class _CF:
    """icons.draw_icon bir Frame ister; tuvale sarılı geçici çerçeve."""
    def __init__(self, c):
        self.c = c


def FA_FRAME(c):
    return _CF(c)


def joke_ovl(card_at, hang_at, fly_at, q_at, stamp_at, out_at, target=(1260, 700)):
    """«Botticelli yaktı» kartı (fırça) + sallanan boş çerçeve → ateşe uçar, yanar; üç boş çerçeve + «?» ; KANIT YOK damgası tek ağır vuruş."""
    card = L.brush("BOTTİCELLİ YAKTI", 960, 230, card_at, size=92, color="#F6E7B8", dur=1.1, rough=1.6, out=out_at)

    def fn(cx):
        card(cx)
        f, c, t = cx.f, cx.f.c, cx.t
        kh = cx.amt(hang_at, 0.7)
        tf = cx.at(fly_at)
        u = clamp((t - tf) / 1.0)
        out = 1.0 - cx.amt(out_at, 0.5)
        if kh > 0.003 and u < 1.0:
            hx = 640
            ky = lerp(-120, 470, ease_out(kh, 2.4))
            if u <= 0.0:
                sw = 0.06 * math.sin(t * 2.6) * kh
                x, y, rot, burn = hx, ky, sw, 0.0
                for dx in (-70, 70):                                        # asma ipleri
                    c.drawLine(hx + dx, 150, hx + dx * 0.9, y - 100, S("#3A2A10", 3.0, int(220 * kh)))
            else:
                ue = ease_in(u)
                x = lerp(hx, target[0], ue)
                y = lerp(ky, target[1], ue) - 220 * math.sin(math.pi * ue)
                rot = 0.06 + 3.2 * ue
                burn = clamp((u - 0.55) / 0.45)
            blank_frame(c, x, y, 190 * (1.0 - 0.35 * max(0.0, u - 0.5)), 250 * (1.0 - 0.35 * max(0.0, u - 0.5)), a=kh * (1.0 - smooth(clamp((u - 0.8) / 0.2))) * out, rot=rot, burn=burn, q=cx.amt(q_at, 0.3, off=-0.6) * (1.0 - u), t=t)
        kq = cx.amt(q_at, 0.5)
        if kq > 0.003:
            for i, (qx, qy, rr) in enumerate(((560, 420, -0.05), (860, 360, 0.04), (1160, 430, -0.03))):
                kk = cx.amt(q_at, 0.45, off=0.18 * i)
                if kk <= 0.003:
                    continue
                blank_frame(c, qx, qy + 10 * math.sin(t * 1.6 + i * 1.7) + (1 - ease_out(kk)) * -60, 170, 220, a=kk * out, rot=rr + 0.04 * math.sin(t * 1.9 + i), q=1.0, t=t)
        L.stamp("KANIT YOK", 960, 600, stamp_at, size=96, rot=-0.07, out=out_at)(cx)
    return fn
