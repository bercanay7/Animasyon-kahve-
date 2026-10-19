"""c12_kinds — c12 «Dük» özel çekim türleri (Parça 6 sahne yazarı). `scenes_c12.py` içinde import edilir; `@CM.ckind` ile kaydolur.

Dünya koordinatı = nötr kamerada ekran koordinatı (1920×1080). Kamera: `cam=[(çapa, look(wx, wy, z)), …]` (p6_lib.look) ya da `cam=("push", …)`.
Kaynak disiplini: yüz yok (siluet/simge/madalya), şiddet yok (ceset, kan, iskelet yok); ekrana yalnız script/brif sözcükleri yazılır.
Her tür `ovl=` (çapaya bağlı bindirme) kabul eder; ovl ışıktan SONRA çizilir. Tüm zamanlar çapalıdır (cx.at / cx.amt).

Türler
  c12_takvim  : üç takvim yaprağı (29 MART · 29 HAZİRAN · 29 TEMMUZ) masaya düşer; "üç ayrı 29" şakası (yapraklar sırayla zıplar)
  c12_plan    : Floransa planı (Palazzo Vecchio · Uffizi U avlusu · Arno · Ponte Vecchio · Pitti): 13 makam iğnesi dağınıktır → tek çatıya toplanır; Vasari Koridoru çizgisi çizilir
  c12_unvan   : ünvan rayı (levhalar zincir olur; damgalar Roma/Viyana; fatura kâğıdı)
  c12_1562    : üç tarih kartı + üç mum (tek uzun plan, sola kayma): her kartta mum söner; "dört hafta" parantezi
  c12_rivayet : gravür diyagram: rivayet zinciri + çok sonra çıkan kâğıt, "ilk yazan: ?"
  c12_ceket   : mezar kapağı kayar; kırmızı atlas ceket (iskelet YOK, yalnız ceket)
  c12_daire   : paha biçilmiş "devlet dairesi": çerçeveler tezgâhta ilerler, palle mührü her birine basılır
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_medici as CM
import cilt_oda as OD
import cilt_paper as PP
import cilt_pano as PN
import functools
import icons
import p6_lib as L
import sk
from cilt_medici import TH
from p6_lib import INK, P, S, look, ov
from sk import C, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

INK_BROWN = "#2A180D"


def _wood(c, y0, x0=-1800, x1=3800, depth=700, a=255):
    """Masa/tezgâh yüzeyi: koyu ahşap bant + damar çizgileri + üst kenar parlaması."""
    sh = skia.GradientShader.MakeLinear([(0, y0), (0, y0 + depth)], [C("#7A5230", a), C("#4A2C16", a), C("#2A170B", a)], [0.0, 0.45, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y0 + depth), skia.Paint(Shader=sh))
    rs = np.random.RandomState(5)
    for i in range(46):
        yy = y0 + 18 + rs.rand() * (depth - 30)
        xa = x0 + rs.rand() * (x1 - x0)
        c.drawLine(xa, yy, xa + 220 + rs.rand() * 520, yy + rs.uniform(-3, 3), S("#2A170B", 1.3, 70 + rs.randint(0, 50)))
    c.drawLine(x0, y0 + 1.5, x1, y0 + 1.5, S("#E8C78A", 2.2, 150))
    c.drawLine(x0, y0 + 5, x1, y0 + 5, S("#2A170B", 3.0, 130))


# ═════════════════════════════ c12_takvim ═════════════════════════════
LEAF_W, LEAF_H = 360, 480


def _leaf(f, cx, x, y, rot, month, day, tag, sub, a=1.0, seed=3, lift=0.0, glow=0.0, hl=0.0):
    c = f.c
    pp = PP.paper_image(LEAF_W, LEAF_H, seed, (244, 236, 210), "deckle", (), 30, 0.6)
    pp.draw(f, x, y - lift, rot=rot, alpha=a, shadow=0.55 * (1.0 - min(1.0, lift / 60.0)))
    c.save()
    c.translate(x, y - lift)
    c.rotate(math.degrees(rot))
    # ay bandı
    f.rect(-LEAF_W / 2 + 14, -LEAF_H / 2 + 14, LEAF_W - 28, 96, color="#A8321E", alpha=0.96 * a)
    f.rect(-LEAF_W / 2 + 14, -LEAF_H / 2 + 14, LEAF_W - 28, 96, style="stroke", sw=2.2, color="#4A130C", alpha=0.7 * a)
    for i, xx in enumerate((-96, 96)):
        f.circle(xx, -LEAF_H / 2 + 32, 7, color="#2A1A0C", alpha=0.55 * a)
    CM.ink(f, month, 0, -LEAF_H / 2 + 86, face="title", size=54, color="#F6E7B6", align="c", track=8, alpha=a, emboss=False)
    # gün
    sp = CM.engraved(day, "title", 250, 4.0, "#1B140D")
    CM.draw_spr(f, sp, 0, 62, "c", alpha=a, glow=glow * 0.5, glow_color="#FFE9A8" if glow else None)
    if hl > 0.003:
        f.rrect(-LEAF_W / 2 + 40, -92, LEAF_W - 80, 232, 14, style="stroke", sw=5.0, color="#B33620", alpha=0.85 * hl * a)
    # alt etiket
    f.line(-LEAF_W / 2 + 40, 150, LEAF_W / 2 - 40, 150, color="#7A5A2E", sw=2.0, alpha=0.7 * a)
    if tag:
        CM.ink(f, tag, 0, 192, face="title_m", size=30, color=INK_BROWN, align="c", track=5, alpha=a, emboss=False)
    if sub:
        CM.ink(f, sub, 0, 228, face="cap_i", size=30, color="#5A3E22", align="c", alpha=a, emboss=False)
    c.restore()


@CM.ckind("c12_takvim")
def k_takvim(cx, leaves=(), jumps=(), jump_dur=0.55, actor=None, table_y=700, seed=3, ovl=None, **_):
    """leaves=[dict(month, day='29', tag, sub, at, x, y=500, rot)] — `at`'ta yaprak yukarıdan düşer, masaya oturur (küçük sekme). jumps=[çapa…]: i. yaprak o anda zıplar + vurgu çerçevesi.
    actor=dict(x, y, h, at, action='idle'|'point', kind='soylu', dir=-1, seed): masanın arkasında duran figür (siluet)."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    if actor:
        ak = cx.amt(actor.get("at", 0.0), 0.7)
        if ak > 0.01:
            OD.sil_actor(f, actor.get("kind", "soylu"), actor["x"], actor["y"], actor["h"], t, action=actor.get("action", "idle"), dir=actor.get("dir", -1), seed=actor.get("seed", 5),
                         color="#2A1A10", rim="#E8B070", rim_dir=1, alpha=ak, **actor.get("p", {}))
    _wood(c, table_y)
    for i, lv in enumerate(leaves):
        ta = cx.at(lv["at"])
        u = clamp((t - ta) / 0.55)
        if u <= 0:
            continue
        x, y = lv.get("x", 960), lv.get("y", 500)
        rot = lv.get("rot", 0.0)
        yy = lerp(-420, 0.0, ease_in(u, 2.2))
        rr = rot + (1 - u) * 0.34 * (1 if i % 2 == 0 else -1)
        bn = max(0.0, 1.0 - (t - ta - 0.55) / 0.40) if t > ta + 0.55 else 0.0
        lift = -yy * 1.0 + 26 * bn * abs(math.sin((t - ta - 0.55) * 13.0))
        hl = 0.0
        if i < len(jumps):
            tj = cx.at(jumps[i])
            uj = clamp((t - tj) / jump_dur)
            if 0 < uj < 1:
                lift += 70 * math.sin(math.pi * uj) ** 0.8
                rr += 0.06 * math.sin(math.pi * uj * 2) * (1 if i % 2 == 0 else -1)
            hl = clamp((t - tj) / 0.2) * (1.0 - smooth(clamp((t - tj - 1.6) / 0.6)))
        _leaf(f, cx, x, y, rr, lv.get("month", "MART"), lv.get("day", "29"), lv.get("tag"), lv.get("sub"), a=clamp(u * 5), seed=lv.get("seed", 5 + i * 3), lift=lift,
              glow=0.0, hl=hl)
    L.end(cx, cam, motes_n=26)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_plan ═════════════════════════════
PW_, PH_ = 1640, 920
PS_ = 1.5


def _riv_y(x):
    return 178 + 34 * math.sin(x / 310.0 + 0.4) + 0.04 * x


RIV_W = 96
PV_R = (-345, -105, -200, 12)
PIAZZA_R = (-200, -105, -104, 12)
U_W = (-104, -78, -62, 122)
U_E = (62, -78, 104, 122)
U_B = (-104, 92, 104, 138)
PONTE_X = 262
PITTI_R = (430, 290, 735, 410)
CORRIDOR = [(-205, -34), (-120, -52), (-83, -34), (-83, 104), (-10, 116), (78, 104), (132, 146), (205, 158), (PONTE_X, 168), (PONTE_X + 6, 262), (330, 292), (420, 330), (500, 346), (590, 352)]
PIN_POS = [(-650, -300), (-520, -172), (-420, -330), (-290, -240), (-170, -330), (-60, -218), (74, -262), (210, -330), (350, -190), (480, -300), (640, -210), (-610, 48), (590, -60)]
U_SLOTS = ([(-83, -52 + i * 38) for i in range(5)] + [(-34 + i * 34, 115) for i in range(3)] + [(83, -52 + i * 38) for i in range(5)])


def _rect(c, r, fill, a=255, stroke=INK, sw=1.4, rad=2):
    rr = skia.Rect.MakeLTRB(*r)
    c.drawRoundRect(rr, rad, rad, P(fill, a))
    c.drawRoundRect(rr, rad, rad, S(stroke, sw, 190))


@functools.lru_cache(maxsize=2)
def _plan_baked(seed=7):
    pp = PP.paper_image(PW_, PH_, seed, (236, 224, 190), "deckle", (), 44, 0.9)
    fr = sk.Frame(int(PW_ * PS_), int(PH_ * PS_))
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    c.scale(PS_, PS_)
    c.translate(PW_ / 2, PH_ / 2)
    c.clipRect(skia.Rect.MakeLTRB(-PW_ / 2 + 36, -PH_ / 2 + 36, PW_ / 2 - 36, PH_ / 2 - 36))
    rs = np.random.RandomState(seed)
    # nehir
    n = 60
    top = [(x, _riv_y(x) - RIV_W / 2) for x in np.linspace(-PW_ / 2, PW_ / 2, n)]
    bot = [(x, _riv_y(x) + RIV_W / 2) for x in np.linspace(PW_ / 2, -PW_ / 2, n)]
    river = sk.poly_path(top + bot)
    c.drawPath(river, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(0, 100), (0, 300)], [C("#8FB4C2"), C("#5F8CA3")], [0, 1])))
    for k in range(7):
        pts = [(x, _riv_y(x) + (k - 3) * 11 + 3 * math.sin(x / 40.0 + k)) for x in np.linspace(-PW_ / 2, PW_ / 2, 90)]
        c.drawPath(sk.smooth_path(pts, False, 0.5), S("#EAF4F2", 1.6, 120))
    c.drawPath(sk.poly_path(top, False), S(INK, 2.0, 200))
    c.drawPath(sk.poly_path(bot[::-1], False), S(INK, 2.0, 200))
    # ev blokları (kuzey ve güney yaka)
    roofs = ["#DCC49C", "#D2B48A", "#E2CDA8", "#CDAA82", "#D8BE96"]
    avoid = [PV_R, PIAZZA_R, (U_W[0] - 20, U_W[1] - 20, U_E[2] + 20, U_B[3] + 22), (PONTE_X - 40, 0, PONTE_X + 40, 500), (PITTI_R[0] - 30, PITTI_R[1] - 30, PITTI_R[2] + 30, PH_)]
    for gx in range(-780, 790, 50):
        for gy in range(-420, 430, 42):
            x = gx + rs.uniform(-8, 8)
            y = gy + rs.uniform(-6, 6)
            w, h = rs.uniform(30, 44), rs.uniform(26, 36)
            ry = _riv_y(x)
            if abs((y + h / 2) - ry) < RIV_W / 2 + 18:
                continue
            if y > ry and x > 380:
                continue
            if any(a_[0] < x + w and x < a_[2] and a_[1] < y + h and y < a_[3] for a_ in avoid):
                continue
            if rs.rand() < 0.26:
                continue
            _rect(c, (x, y, x + w, y + h), roofs[rs.randint(len(roofs))], 255, "#6A5030", 0.9, 2)
            c.drawLine(x + 3, y + h * 0.5, x + w - 3, y + h * 0.5, S("#6A5030", 0.7, 70))
    # Piazza (açık taş zemin)
    _rect(c, PIAZZA_R, "#E8DCC2", 255, INK, 1.2, 3)
    for i in range(1, 6):
        c.drawLine(PIAZZA_R[0] + i * 16, PIAZZA_R[1] + 4, PIAZZA_R[0] + i * 16, PIAZZA_R[3] - 4, S("#B8A888", 0.9, 150))
    # Palazzo Vecchio: bloğun içi avlu + sol üstte kule
    _rect(c, PV_R, "#B8845C", 255, INK, 2.0, 3)
    inner = (PV_R[0] + 34, PV_R[1] + 30, PV_R[2] - 34, PV_R[3] - 24)
    _rect(c, inner, "#D8C49C", 255, INK, 1.2, 2)
    _rect(c, (PV_R[0] + 2, PV_R[1] + 2, PV_R[0] + 44, PV_R[1] + 44), "#8A5A3A", 255, INK, 1.8, 2)
    for i in range(12):
        xx = PV_R[0] + 6 + i * ((PV_R[2] - PV_R[0] - 12) / 11.0)
        c.drawRect(skia.Rect.MakeXYWH(xx - 3, PV_R[1] - 5, 6, 6), P("#8A5A3A"))
    # Pitti sarayı + Boboli
    gard = [(PITTI_R[0] + 10, PITTI_R[3]), (PITTI_R[0] + 60, PITTI_R[3] + 90), (PITTI_R[2] + 40, PITTI_R[3] + 120), (PITTI_R[2] + 40, PITTI_R[3] + 20)]
    c.drawPath(sk.poly_path(gard), skia.Paint(AntiAlias=True, Color=C("#9DB07A", 230)))
    c.drawPath(sk.poly_path(gard), S(INK, 1.3, 170))
    for i in range(16):
        c.drawCircle(PITTI_R[0] + 40 + rs.rand() * 290, PITTI_R[3] + 20 + rs.rand() * 90, 9 + 5 * rs.rand(), P("#5C7A48", 210))
    _rect(c, PITTI_R, "#C9A070", 255, INK, 2.0, 3)
    _rect(c, (PITTI_R[0] + 70, PITTI_R[1] + 36, PITTI_R[2] - 70, PITTI_R[3] - 6), "#E3D2AE", 255, INK, 1.2, 2)
    for i in range(9):
        c.drawLine(PITTI_R[0] + 14 + i * 33, PITTI_R[1] + 10, PITTI_R[0] + 14 + i * 33, PITTI_R[1] + 28, S(INK, 1.2, 150))
    # Ponte Vecchio
    y0 = _riv_y(PONTE_X) - RIV_W / 2 - 10
    y1 = _riv_y(PONTE_X) + RIV_W / 2 + 10
    _rect(c, (PONTE_X - 26, y0, PONTE_X + 26, y1), "#7A5638", 255, INK, 1.8, 2)
    for k in range(6):
        yy = y0 + 4 + k * (y1 - y0 - 8) / 6.0
        c.drawRect(skia.Rect.MakeXYWH(PONTE_X - 25, yy, 14, 12), P("#B58A52"))
        c.drawRect(skia.Rect.MakeXYWH(PONTE_X + 11, yy, 14, 12), P("#B58A52"))
    # Uffizi: kesikli iz (taslak) — dolgu çekim içinde çizilir
    fr_img = fr.surf.makeImageSnapshot()
    return pp, fr_img


def _u_rects():
    return [U_W, U_E, U_B]


def _uffizi_fill(c, k, a=1.0):
    """Uffizi U avlusu: k=0 → kesikli iz; k=1 → dolu (çatı hatları)."""
    for r in _u_rects():
        rr = skia.Rect.MakeLTRB(*r)
        if k > 0.01:
            c.drawRoundRect(rr, 2, 2, P("#C7A06C", int(255 * k * a)))
            c.drawRoundRect(rr, 2, 2, S(INK, 1.8, int(220 * k * a)))
            if r[2] - r[0] < 80:
                for yy in np.arange(r[1] + 8, r[3] - 4, 9):
                    c.drawLine(r[0] + 3, yy, r[2] - 3, yy, S("#8A5E32", 0.9, int(120 * k * a)))
            else:
                for xx in np.arange(r[0] + 8, r[2] - 4, 9):
                    c.drawLine(xx, r[1] + 3, xx, r[3] - 3, S("#8A5E32", 0.9, int(120 * k * a)))
        if k < 0.99:
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C("#6A4A28", int(200 * (1 - k) * a)))
            p.setPathEffect(skia.DashPathEffect.Make([6, 5], 0))
            c.drawRoundRect(rr, 2, 2, p)


def _pin(c, x, y, a=1.0, s=1.0, col="#B33620"):
    c.save()
    c.translate(x, y)
    c.scale(s * 1.7, s * 1.7)
    c.drawOval(skia.Rect.MakeLTRB(-8, -3, 8, 3), P("#2A1A0C", int(70 * a)))
    c.drawLine(0, 0, 0, -34, S("#4A2C16", 2.4, int(255 * a)))
    c.drawRect(skia.Rect.MakeLTRB(0, -36, 28, -18), P(col, int(255 * a)))
    c.drawRect(skia.Rect.MakeLTRB(0, -36, 28, -18), S("#4A130C", 1.4, int(255 * a)))
    c.drawLine(4, -29, 24, -29, S("#F6E7B6", 1.4, int(200 * a)))
    c.drawLine(4, -24, 18, -24, S("#F6E7B6", 1.4, int(200 * a)))
    c.restore()


@CM.ckind("c12_plan")
def k_plan(cx, built=False, pins_at=None, pins_dt=0.12, fly_at=None, fly_dt=0.075, fly_dur=1.0, u_fill_at=None, tabela_at=None, tabela_text="13 MAKAM",
           corr_at=None, corr_dur=3.0, lab_pv=None, lab_uf=None, lab_pitti=None, lab_arno=None, lab_ponte=None, seed=7, ovl=None, **_):
    """Floransa planı. built=True: U avlusu hazır, iğne yok. pins_at: 13 iğne sırayla çıkar; fly_at: iğneler U'ya uçar (tek çatı); u_fill_at: avlu dolar; tabela_at: «13 MAKAM» tabelası;
    corr_at/corr_dur: Vasari Koridoru çizgisi (Uffizi → Palazzo Vecchio … Arno … Pitti); lab_*: etiketler (çapa)."""
    f, c, cam = L.begin(cx, seed=seed, dress="top")
    t = cx.t
    pp, img = _plan_baked(seed)
    pp.draw(f, 960, 540, rot=0.0, scale=1.0, alpha=1.0, shadow=0.7)
    c.save()
    c.translate(960, 540)
    c.save()
    c.scale(1.0 / PS_, 1.0 / PS_)
    c.drawImage(img, -PW_ * PS_ / 2, -PH_ * PS_ / 2, CM._LIN, skia.Paint(AntiAlias=True))
    c.restore()
    # Uffizi
    kf = 1.0 if built else (cx.amt(u_fill_at, 1.0) if u_fill_at is not None else 0.0)
    _uffizi_fill(c, kf)
    # iğneler
    if not built and pins_at is not None:
        tp = cx.at(pins_at)
        tf = cx.at(fly_at) if fly_at is not None else 1e9
        for i, (px, py) in enumerate(PIN_POS):
            ta = tp + i * pins_dt
            k = clamp((t - ta) / 0.3)
            if k <= 0.003:
                continue
            tfi = tf + i * fly_dt
            u = clamp((t - tfi) / fly_dur)
            sx, sy = U_SLOTS[i]
            if u <= 0:
                _pin(c, px, py, a=clamp(k * 2), s=0.6 + 0.4 * sk.back_out(k))
                c.drawCircle(px, py + 1, 16 * (1 - k) + 2, S("#B33620", 2, int(160 * (1 - k))))
            elif u < 1:
                e = ease_io(u, 2.2)
                x = lerp(px, sx, e)
                y = lerp(py, sy, e) - 110 * math.sin(math.pi * e)
                _pin(c, x, y, a=1.0, s=1.0 - 0.45 * e)
            else:
                # yuvaya oturdu: küçük altın pencere işareti
                c.drawRect(skia.Rect.MakeXYWH(sx - 6, sy - 7, 12, 14), P("#E8C468", 255))
                c.drawRect(skia.Rect.MakeXYWH(sx - 6, sy - 7, 12, 14), S("#4A130C", 1.2, 220))
    # koridor çizgisi
    if corr_at is not None:
        kc = ease_io(clamp((t - cx.at(corr_at)) / corr_dur), 1.6)
        if kc > 0.002:
            pts = L.thread_pts(CORRIDOR, 0.0, kc, 10)
            path = sk.poly_path(pts, False)
            c.drawPath(path, S("#2A1A0C", 14, 150))
            c.drawPath(path, S("#E2C07A", 10, 255))
            pd = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C("#A8321E", 235), StrokeCap=skia.Paint.kRound_Cap)
            pd.setPathEffect(skia.DashPathEffect.Make([14, 10], -t * 40))
            c.drawPath(path, pd)
            hx, hy = pts[-1]
            c.drawCircle(hx, hy, 9, P("#FFF1B8", 255))
            c.drawCircle(hx, hy, 9, S("#7A3A10", 2, 255))
            c.drawCircle(hx, hy, 24, S("#FFF1B8", 2.2, int(200 * (1 - kc))))
    # etiketler
    def lab(text, x, y, at, size=30, rot=0.0):
        k = cx.amt(at, 0.6)
        if k <= 0.003:
            return
        c.save()
        c.translate(x, y + (1 - k) * 8)
        c.rotate(rot)
        wd = sk.text_width(text, "title_m", size, 4) + 34
        CM.tablet(f, -wd / 2, -size * 0.9, wd, size * 1.5, alpha=0.95 * k, corner=6)
        CM.ink(f, text, 0, size * 0.18, face="title_m", size=size, color=TH.fg, align="c", track=4, alpha=k, emboss=False)
        c.restore()
    if lab_pv is not None:
        lab("PALAZZO VECCHIO", -272, -138, lab_pv, 24)
    if lab_uf is not None:
        lab("UFFIZI", 0, 28, lab_uf, 30)
    if lab_ponte is not None:
        lab("PONTE VECCHIO", PONTE_X - 8, 118, lab_ponte, 22)
    if lab_pitti is not None:
        lab("PİTTİ SARAYI", 585, 270, lab_pitti, 26)
    if lab_arno is not None:
        lab("ARNO", -430, _riv_y(-430) + 6, lab_arno, 28, rot=0.04)
    # tabela: 13 MAKAM (U'nun üstünde sallanır)
    if tabela_at is not None:
        k = cx.amt(tabela_at, 0.7)
        if k > 0.003:
            ex = sk.back_out(k)
            sw = 0.05 * math.sin(t * 2.2) * (1 - k * 0.4)
            c.save()
            c.translate(150, -190 - (1 - ex) * 200)
            c.rotate(math.degrees(sw))
            wd = sk.text_width(tabela_text, "title", 44, 7) + 90
            c.drawLine(-wd / 2 + 24, -52, -wd / 2 + 24, 0, S("#4A2C16", 2.4, 255))
            c.drawLine(wd / 2 - 24, -52, wd / 2 - 24, 0, S("#4A2C16", 2.4, 255))
            CM.tablet(f, -wd / 2, 0, wd, 80, alpha=k, corner=8)
            CM.ink(f, tabela_text, 0, 55, face="title", size=44, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
            c.restore()
    c.restore()
    L.end(cx, cam, motes_n=18)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_unvan ═════════════════════════════
def _arrow(f, x0, y0, x1, y1, k, col="#7A5A2E", sw=4.0):
    if k <= 0.003:
        return
    xe, ye = lerp(x0, x1, ease_io(k)), lerp(y0, y1, ease_io(k))
    f.line(x0, y0, xe, ye, color=col, sw=sw, alpha=0.95)
    if k > 0.9:
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            f.line(x1, y1, x1 - 20 * math.cos(a + da * 0.2) * 1.0 + 0, y1 - 20 * math.sin(a + da * 0.2) * 1.0, color=col, sw=sw, alpha=0.95 * clamp((k - 0.9) * 10))


@CM.ckind("c12_unvan")
def k_unvan(cx, plates=(), rail_y=330, link=True, invoice=None, crown=None, coins=None, seed=11, ovl=None, **_):
    """Ünvan rayı. plates=[dict(x, main, sub=None, at, strike=çapa|None, stamp=[(metin, çapa, dx, dy, rot)], w=520, icon=None)]; plakalar arası ok (link).
    invoice=dict(at, x, y, stamp=(metin, çapa)): sağdan kayarak gelen fatura kâğıdı (satırlar okunmaz; rakam YOK). crown=dict(x, y, at, out=None): taç simgesi. coins=dict(x,y,at)."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    # raf: yaldız çubuk + kancalar
    xs = [p["x"] for p in plates] or [960]
    x0, x1 = min(xs) - 700, max(xs) + 900
    f.rect(x0, rail_y - 14, x1 - x0, 22, shader=f.lin(0, rail_y - 14, 0, rail_y + 8, [("#E8C468", 0.0), ("#B07F22", 0.5), ("#6A4A12", 1.0)]), alpha=0.98)
    f.line(x0, rail_y + 9, x1, rail_y + 9, color="#2A170B", sw=3.0, alpha=0.6)
    prev = None
    for i, p in enumerate(plates):
        k = cx.amt(p["at"], 0.6)
        if k <= 0.003:
            continue
        w = p.get("w", 520)
        h = 150 if p.get("sub") else 118
        sway = 0.03 * math.sin(t * 1.7 + i) * (1 - k * 0.5)
        ex = sk.back_out(k)
        x, y = p["x"], rail_y + 10 + (1 - ex) * -160
        c.save()
        c.translate(x, y)
        c.rotate(math.degrees(sway))
        for dx in (-w / 2 + 40, w / 2 - 40):
            f.line(dx, 0, dx * 0.96, 70, color="#4A2C16", sw=2.6, alpha=k)
        f.circle(0, 0, 3, color="#4A2C16")
        c.translate(0, 70)
        CM.tablet(f, -w / 2, 0, w, h, alpha=k, corner=10)
        mainsz = CM.fit_size(p["main"], "title", 44, w - 70, 6)
        CM.ink(f, p["main"], 0, 60 if not p.get("sub") else 58, face="title", size=mainsz, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
        if p.get("sub"):
            CM.ink(f, p["sub"], 0, 108, face="cap_i", size=32, color=TH.fg2, align="c", alpha=k, emboss=False)
        if p.get("strike") is not None:
            ks = cx.amt(p["strike"], 0.35)
            if ks > 0.003:
                f.line(-w / 2 + 30, 58, -w / 2 + 30 + (w - 60) * ks, 40, color="#A8201A", sw=9, alpha=0.92)
        for st in p.get("stamp", ()):
            txt, at, dx, dy, rot = st
            kk = cx.amt(at, 0.3)
            if kk > 0.003:
                CM.stamp(f, txt, dx, dy, rot=rot, size=p.get("stamp_size", 44), alpha=1.0, t=kk)
        c.restore()
        if link and prev is not None:
            pk = cx.amt(p["at"], 0.5, off=-0.05)
            _arrow(f, prev["x"] + prev.get("w", 520) / 2 + 12, rail_y + 150, p["x"] - w / 2 - 12, rail_y + 150, pk)
        prev = p
    if crown:
        k = cx.amt(crown["at"], 0.6)
        if crown.get("out") is not None:
            k *= 1.0 - cx.amt(crown["out"], 0.4)
        if k > 0.003:
            yy = crown.get("y", 160) + (1 - k) * -90 + 6 * math.sin(t * 1.8)
            c.drawCircle(crown["x"], yy, 120, P("#F0D27A", int(40 * k)))
            icons.draw_icon(f, "crown", crown["x"], yy, size=crown.get("size", 200), metal="gold", alpha=k, glow=0.25 * k)
    if coins:
        k = cx.amt(coins["at"], 0.6)
        if k > 0.003:
            icons.draw_icon(f, "coins", coins["x"], coins["y"] + (1 - k) * -60, size=coins.get("size", 150), metal="gold", alpha=k, glow=0.15)
    if invoice:
        ta = cx.at(invoice["at"])
        u = ease_out(clamp((t - ta) / 0.9), 3)
        if u > 0.003:
            iw, ih = 360, 470
            ix = invoice["x"] + (1 - u) * 900
            iy = invoice.get("y", 600) + 14 * math.sin(t * 1.4)
            pp = PP.paper_image(iw, ih, 31, (246, 240, 222), "deckle", (("h", 0.5),), 30, 0.5)
            pp.draw(f, ix, iy, rot=0.05 * (1 - u) + 0.03, alpha=1.0, shadow=0.55)
            c.save()
            c.translate(ix, iy)
            c.rotate(1.7 * (1 - u) + 1.7)
            for j in range(9):
                yy = -170 + j * 40
                wl = 220 if j % 3 else 150
                f.line(-wl / 2 - 20, yy, wl / 2 - 20, yy + 2, color="#4A3420", sw=2.4, alpha=0.5 * u)
            CM.ink(f, invoice.get("title", "FATURA"), 0, -190, face="title", size=44, color=TH.fg, align="c", track=8, alpha=u, emboss=False)
            if invoice.get("stamp"):
                kk = cx.amt(invoice["stamp"][1], 0.3)
                if kk > 0.003:
                    CM.stamp(f, invoice["stamp"][0], 10, 120, rot=-0.18, size=40, alpha=1.0, t=kk)
            c.restore()
    L.end(cx, cam, motes_n=24)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_1562 ═════════════════════════════
def _date_card(f, cx, x, y, k, big, small=None, double=None, w=560):
    """Tarih kartı: Cinzel büyük tarih (+ isteğe bağlı iki değerli «6 ↔ 12» gösterimi)."""
    CM.tablet(f, x - w / 2, y, w, 168, alpha=k, corner=12)
    if double:
        a, b, tail = double
        sz = 76
        wa = sk.text_width(a, "title", sz, 4)
        wb = sk.text_width(b, "title", sz, 4)
        wt = sk.text_width(tail, "title_m", 40, 6)
        gap = 78
        tot = wa + gap + wb + 22 + wt
        x0 = x - tot / 2
        CM.ink(f, a, x0, y + 100, face="title", size=sz, color=TH.fg, align="l", track=4, alpha=k, emboss=False)
        ax0, ax1 = x0 + wa + 12, x0 + wa + gap - 12
        f.line(ax0, y + 76, ax1, y + 76, color=TH.fg, sw=3.4, alpha=0.9 * k)
        for dx_, sg in ((ax0, 1), (ax1, -1)):
            f.line(dx_, y + 76, dx_ + sg * 14, y + 66, color=TH.fg, sw=3.4, alpha=0.9 * k)
            f.line(dx_, y + 76, dx_ + sg * 14, y + 86, color=TH.fg, sw=3.4, alpha=0.9 * k)
        CM.ink(f, b, x0 + wa + gap, y + 100, face="title", size=sz, color=TH.fg, align="l", track=4, alpha=k, emboss=False)
        CM.ink(f, tail, x0 + wa + gap + wb + 22, y + 100, face="title_m", size=40, color=TH.fg, align="l", track=6, alpha=k, emboss=False)
    else:
        CM.ink(f, big, x, y + 100, face="title", size=CM.fit_size(big, "title", 78, w - 60, 5), color=TH.fg, align="c", track=5, alpha=k, emboss=False)
    if small:
        CM.ink(f, small, x, y + 148, face="cap_i", size=30, color=TH.fg2, align="c", alpha=k, emboss=False)


@CM.ckind("c12_1562")
def k_1562(cx, stations=(), span=None, seed=17, ovl=None, **_):
    """Üç tarih kartı + üç mum (tek uzun plan; kamera sola/yana kayar). stations=[dict(x, big, small, double=(a,b,tail)|None, name, sub, at, snuff_at)].
    Mum söner: duman yükselir, ışık havuzu daralır. span=dict(at, x0, x1, label): «dört hafta» parantezi (çapa). Sessiz, yavaş; gösterilen yalnız tarih, ad, mum."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    # raf: koyu taş tezgâh
    xs = [s["x"] for s in stations]
    x0, x1 = min(xs) - 900, max(xs) + 900
    f.rect(x0, 800, x1 - x0, 140, shader=f.lin(0, 800, 0, 940, [("#2A2018", 0.0), ("#120C08", 1.0)]), alpha=1.0)
    f.line(x0, 800, x1, 800, color="#6A5438", sw=3.0, alpha=0.7)
    lits = []
    for i, s in enumerate(stations):
        k = cx.amt(s["at"], 0.8)
        ts = cx.at(s["snuff_at"])
        lit = 1.0 - ease_io(clamp((t - ts) / 1.0)) if t >= ts else 1.0
        lits.append(lit if k > 0.05 else 0.0)
        if k <= 0.003:
            continue
        x = s["x"]
        _date_card(f, cx, x, 150 + (1 - k) * -40, k, s.get("big", ""), s.get("small"), s.get("double"))
        OD.candle(f, x, 790, 300, t, seed=3 + i * 7, lit=lit, holder=True, halo=1.0)
        w = 520
        CM.tablet(f, x - w / 2, 812, w, 100 + (24 if s.get("sub") else 0), alpha=k, corner=10)
        CM.ink(f, s["name"], x, 870, face="title_m", size=44, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
        if s.get("sub"):
            CM.ink(f, s["sub"], x, 906, face="cap_i", size=28, color=TH.fg2, align="c", alpha=k, emboss=False)
    if span:
        k = cx.amt(span["at"], 0.9)
        if k > 0.003:
            xa, xb = span["x0"], span["x1"]
            ye = 112
            e = ease_io(k)
            f.line(xa, ye, lerp(xa, xb, e), ye, color="#E8C468", sw=5, alpha=0.95)
            for xx in (xa, xb):
                if (xx == xa) or k > 0.95:
                    f.line(xx, ye - 18, xx, ye + 18, color="#E8C468", sw=5, alpha=0.95)
            lab = span.get("label", "DÖRT HAFTA")
            wd = sk.text_width(lab, "title", 54, 8) + 80
            CM.tablet(f, (xa + xb) / 2 - wd / 2, ye - 96, wd, 80, alpha=k, corner=10)
            CM.ink(f, lab, (xa + xb) / 2, ye - 40, face="title", size=54, color=TH.fg, align="c", track=8, alpha=k, emboss=False)
    vis = [l for l in lits if l > 0.0] or [0.0]
    on = sum(1 for s_, l in zip(stations, lits) if l > 0.02) / max(1, len(stations))
    L.end(cx, cam, light=CM.candle_light(t, seed, base=(W / 2, 560), r=1050.0, sway=14.0), motes_n=14, k=0.50 + 0.50 * on)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_rivayet (gravür) ═════════════════════════════
def _dotted_arrow(c, x0, y0, x1, y1, k, t, col="#3A2A18", sw=3.4):
    if k <= 0.003:
        return
    e = ease_io(k)
    xe, ye = lerp(x0, x1, e), lerp(y0, y1, e)
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=sw, Color=C(col, 235), StrokeCap=skia.Paint.kRound_Cap)
    p.setPathEffect(skia.DashPathEffect.Make([9, 12], -t * 26))
    c.drawLine(x0, y0, xe, ye, p)
    if k > 0.96:
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (0.5, -0.5):
            c.drawLine(x1, y1, x1 - 26 * math.cos(a + da), y1 - 26 * math.sin(a + da), S(col, sw, 235))


@CM.ckind("c12_rivayet")
def k_rivayet(cx, a_nodes=0.0, a1=None, a2=None, a_axis=None, a_slip=None, a_q=None, seed=23, ovl=None, **_):
    """Gravür (sepya) diyagram: GIOVANNI ← GARZIA ← COSIMO noktalı oklar (RİVAYET: ayrıntıda hiçbir belge yok), altta zaman ekseni: 1562 ... çok sonra: kâğıt (ilk yazan: ?).
    a_nodes: düğümler; a1/a2: oklar; a_axis: eksen; a_slip: kâğıt; a_q: soru işareti."""
    f, c, cam = L.begin(cx, seed=seed, dress=None, mono=1.0)
    t = cx.t
    ny = 470
    nodes = [(560, "GIOVANNI"), (1040, "GARZIA"), (1520, "COSIMO")]
    for i, (nx, nm) in enumerate(nodes):
        k = cx.amt(a_nodes, 0.6, off=i * 0.22)
        if k <= 0.003:
            continue
        r = 92 * (0.8 + 0.2 * sk.back_out(k))
        c.drawCircle(nx, ny, r + 8, P("#2A180D", int(60 * k)))
        c.drawCircle(nx, ny, r, P("#E8D8B0", int(255 * k)))
        c.drawCircle(nx, ny, r, S(INK, 3.4, int(255 * k)))
        c.drawCircle(nx, ny, r - 14, S(INK, 1.6, int(200 * k)))
        # baş-omuz siluet (yüz yok)
        c.drawCircle(nx, ny - 18, 24, P("#3A2616", int(235 * k)))
        pth = skia.Path()
        pth.moveTo(nx - 46, ny + 50); pth.quadTo(nx - 44, ny + 6, nx, ny + 8); pth.quadTo(nx + 44, ny + 6, nx + 46, ny + 50); pth.close()
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(nx - r + 6, ny - r + 6, nx + r - 6, ny + r - 6))
        c.drawPath(pth, P("#3A2616", int(235 * k)))
        c.restore()
        CM.ink(f, nm, nx, ny + r + 64, face="title_m", size=38, color=TH.fg, align="c", track=6, alpha=k, emboss=False)
    if a1 is not None:
        _dotted_arrow(c, 1040 - 100, ny, 560 + 100, ny, clamp((t - cx.at(a1)) / 0.8), t)
    if a2 is not None:
        _dotted_arrow(c, 1520 - 100, ny, 1040 + 100, ny, clamp((t - cx.at(a2)) / 0.8), t)
    # zaman ekseni
    ay = 800
    if a_axis is not None:
        k = ease_io(clamp((t - cx.at(a_axis)) / 3.2), 1.4)
        if k > 0.003:
            x0_, x1_ = 520, 3400
            xe = lerp(x0_, x1_, k)
            c.drawLine(x0_, ay, xe, ay, S("#3A2616", 5, 235))
            c.drawLine(x0_, ay - 20, x0_, ay + 20, S("#3A2616", 5, 235))
            CM.ink(f, "1562", x0_, ay + 70, face="title", size=44, color=TH.fg, align="c", track=6, alpha=1.0, emboss=False)
            for j in range(1, 14):
                xx = x0_ + j * 222
                if xx < xe:
                    c.drawLine(xx, ay - 8, xx, ay + 8, S("#3A2616", 2.2, 200))
            if xe > 1800:
                CM.ink(f, "ÇOK SONRA", 1900, ay - 36, face="title_m", size=34, color=TH.fg2, align="c", track=8, alpha=clamp((xe - 1800) / 300), emboss=False)
    if a_slip is not None:
        k = cx.amt(a_slip, 0.8)
        if k > 0.003:
            sx_ = 3100
            pp = PP.paper_image(380, 300, 41, (232, 220, 188), "torn", (), 30, 1.1)
            pp.draw(f, sx_, ay - 220 + (1 - k) * 40, rot=0.05, alpha=k, shadow=0.6)
            for j in range(6):
                yy = ay - 330 + j * 40 + (1 - k) * 40
                c.drawLine(sx_ - 130, yy, sx_ - 130 + (250 if j % 3 else 180) * k, yy + 2, S("#4A3420", 2.4, int(170 * k)))
    if a_q is not None:
        k = cx.amt(a_q, 0.7)
        if k > 0.003:
            CM.ink(f, "İLK YAZAN", 3100, ay + 72, face="title_m", size=36, color=TH.fg, align="c", track=7, alpha=k, emboss=False)
            sp = CM.engraved("?", "title", 150, 4.0, "#1B140D")
            CM.draw_spr(f, sp, 3100, ay - 150, "c", alpha=k * (0.8 + 0.2 * math.sin(t * 3)), scale=0.9 + 0.1 * ease_out(k))
    L.end(cx, cam, mono=1.0, motes_n=16)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_ceket ═════════════════════════════
def _jacket_paths():
    body = [(-170, -150), (-70, -170), (70, -170), (170, -150), (150, 60), (160, 200), (-160, 200), (-150, 60)]
    slv_l = [(-170, -150), (-250, -120), (-330, 90), (-350, 190), (-262, 200), (-232, 100), (-150, 60)]
    slv_r = [(170, -150), (250, -120), (330, 90), (350, 190), (262, 200), (232, 100), (150, 60)]
    return body, slv_l, slv_r


@CM.ckind("c12_ceket")
def k_ceket(cx, open_at=0.0, reveal_at=None, glint_at=None, seed=29, ovl=None, **_):
    """Mezar kapağı (taş) sola kayar; içinde yalnız KIRMIZI ATLAS CEKET (iskelet/beden YOK). reveal_at: ceket belirir; glint_at: atlas parıltısı geçer."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    cxx, cyy = 960, 560
    # kovuk
    f.rrect(cxx - 640, cyy - 330, 1280, 660, 18, color="#0C0907", alpha=1.0)
    f.rrect(cxx - 640, cyy - 330, 1280, 660, 18, style="stroke", sw=6, color="#2A241C", alpha=1.0)
    kr = cx.amt(reveal_at if reveal_at is not None else open_at, 1.4, off=0.0 if reveal_at is not None else 1.0)
    if kr > 0.003:
        # sıcak spot
        f.circle(cxx, cyy, 620, shader=f.rad(cxx, cyy, 620, [("#B8743A", 0.0, int(120 * kr)), ("#3A2010", 0.6, int(50 * kr)), ("#000000", 1.0, 0)]))
        # kumaş zemin (koyu kadife)
        f.rrect(cxx - 560, cyy - 270, 1120, 540, 10, color="#2A1A1A", alpha=0.9 * kr)
        body, sl, sr = _jacket_paths()
        paint = skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(cxx - 300, cyy - 200), (cxx + 300, cyy + 220)], [C("#6E100C"), C("#B8261A"), C("#8A1810")], [0, 0.5, 1]))
        paint.setAlphaf(clamp(kr))
        c.save()
        c.translate(cxx, cyy)
        c.rotate(-4.0)
        for poly in (sl, sr, body):
            pth = sk.poly_path(poly)
            c.drawPath(pth, paint)
            c.drawPath(pth, S("#3A0806", 3.0, int(230 * kr)))
        # yaka + ön ayrım + düğmeler + kesikler
        c.drawLine(0, -170, 0, 200, S("#3A0806", 2.6, int(200 * kr)))
        c.drawLine(-60, -168, 0, -120, S("#E8C468", 2.2, int(200 * kr)))
        c.drawLine(60, -168, 0, -120, S("#E8C468", 2.2, int(200 * kr)))
        for j in range(9):
            c.drawCircle(-14, -100 + j * 33, 5.2, P("#E8C468", int(255 * kr)))
            c.drawCircle(14, -100 + j * 33, 5.2, P("#E8C468", int(255 * kr)))
        for j in range(5):
            yy = -90 + j * 62
            c.drawLine(-120, yy, -62, yy + 4, S("#D8503A", 2.0, int(170 * kr)))
            c.drawLine(120, yy, 62, yy + 4, S("#D8503A", 2.0, int(170 * kr)))
        for sg in (-1, 1):
            for j in range(4):
                yy = -80 + j * 70
                c.drawLine(sg * (262 + j * 20), yy + 80, sg * (300 + j * 18), yy + 90, S("#D8503A", 1.8, int(150 * kr)))
        # atlas parıltısı
        if glint_at is not None:
            g = clamp((t - cx.at(glint_at)) / 1.6)
            if 0 < g < 1:
                gx = -480 + 960 * g
                c.save()
                c.clipPath(sk.poly_path(body), skia.ClipOp.kIntersect, True)
                c.drawRect(skia.Rect.MakeLTRB(gx - 90, -240, gx + 90, 260), skia.Paint(Shader=skia.GradientShader.MakeLinear([(gx - 90, -140), (gx + 90, 140)], [C("#FFFFFF", 0), C("#FFD8C0", 150), C("#FFFFFF", 0)], [0, 0.5, 1])))
                c.restore()
                for poly in (sl, sr):
                    c.save()
                    c.clipPath(sk.poly_path(poly), skia.ClipOp.kIntersect, True)
                    c.drawRect(skia.Rect.MakeLTRB(gx - 90, -240, gx + 90, 260), skia.Paint(Shader=skia.GradientShader.MakeLinear([(gx - 90, -140), (gx + 90, 140)], [C("#FFFFFF", 0), C("#FFD8C0", 120), C("#FFFFFF", 0)], [0, 0.5, 1])))
                    c.restore()
        c.restore()
    # taş kapak: sola kayar
    u = ease_io(clamp((t - cx.at(open_at)) / 2.4), 2.0)
    lx = cxx - u * 1500
    shake = 5 * math.sin(t * 38) * (1 - abs(2 * u - 1)) if 0 < u < 1 else 0.0
    f.rrect(lx - 660 + shake, cyy - 345, 1320, 690, 20, shader=f.lin(lx, cyy - 345, lx, cyy + 345, [("#6A6258", 0.0), ("#4A443C", 1.0)]), alpha=1.0)
    f.rrect(lx - 660 + shake, cyy - 345, 1320, 690, 20, style="stroke", sw=5, color="#1E1A14", alpha=1.0)
    rs = np.random.RandomState(8)
    for j in range(40):
        xx = lx - 620 + rs.rand() * 1240
        yy = cyy - 320 + rs.rand() * 640
        c.drawLine(xx, yy, xx + rs.uniform(20, 90), yy + rs.uniform(-10, 10), S("#2A261E", 1.4, 90))
    # kapaktaki oyma haç (yalnız simge)
    icons.draw_icon(f, "cross", lx + shake, cyy, size=230, metal="bronze", alpha=0.55)
    if u > 0.02:
        f.rect(lx + 660, cyy - 330, 400, 660, color="#000000", alpha=0.0)
    L.end(cx, cam, light=CM.candle_light(t, seed, base=(W / 2, 560), r=1100.0, sway=8.0), motes_n=22, k=0.7)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_daire ═════════════════════════════
def _mini_frame(c, x, y, w, h, seed, a=1.0):
    rs = np.random.RandomState(seed)
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 4, y - h / 2 + 6, w, h), P("#000000", int(60 * a)))
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x, y - h / 2), (x, y + h / 2)], [C("#E8C468", int(255 * a)), C("#8A6422", int(255 * a))], [0, 1])))
    iw, ih = w - 26, h - 26
    ix, iy = x - iw / 2, y - ih / 2
    sky = [("#8FB4C8", "#E8D8B0"), ("#C88A5A", "#EAD0A0"), ("#6A86A8", "#DCCFA8"), ("#A8A07A", "#E6DAB4")][seed % 4]
    c.drawRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), skia.Paint(Shader=skia.GradientShader.MakeLinear([(x, iy), (x, iy + ih)], [C(sky[0], int(255 * a)), C(sky[1], int(255 * a))], [0, 1])))
    hill = skia.Path()
    hill.moveTo(ix, iy + ih)
    hill.lineTo(ix, iy + ih * 0.66)
    hill.quadTo(ix + iw * 0.35, iy + ih * (0.45 + 0.1 * rs.rand()), ix + iw * 0.7, iy + ih * 0.66)
    hill.quadTo(ix + iw * 0.9, iy + ih * 0.72, ix + iw, iy + ih * 0.6)
    hill.lineTo(ix + iw, iy + ih)
    hill.close()
    c.drawPath(hill, P(["#5E7A48", "#7A8A52", "#4A6A50", "#8A7A48"][seed % 4], int(255 * a)))
    # küçük figür silueti
    fx = ix + iw * (0.3 + 0.4 * rs.rand())
    c.drawCircle(fx, iy + ih * 0.52, 8, P("#2A1A0C", int(235 * a)))
    c.drawRect(skia.Rect.MakeXYWH(fx - 9, iy + ih * 0.52 + 8, 18, 36), P("#2A1A0C", int(235 * a)))
    c.drawRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), S("#2A1A0C", 2.0, int(200 * a)), )
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), S("#4A3410", 2.6, int(255 * a)))


@CM.ckind("c12_daire")
def k_daire(cx, belt_at=0.0, sign_at=None, n=9, speed=400.0, spacing=470.0, seed=37, ovl=None, **_):
    """Çerçeveler tezgâhta soldan sağa ilerler; ortadaki mühür tokmağı her birine palle basar (devlet dairesi); solda memur yazar. sign_at: «DEVLET DAİRESİ» tabelası."""
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    ty = 760
    _wood(c, ty, depth=420)
    c.drawRect(skia.Rect.MakeLTRB(-1800, ty - 22, 3800, ty), P("#2A170B", 255))
    t0 = cx.at(belt_at)
    # memur (solda, masa arkasında)
    FA.actor(f, "banker", 230, ty + 4, 470, t, action="write", dir=1, seed=4, alpha=cx.amt(belt_at, 0.8))
    stamp_x = 1010
    ts = []
    for i in range(n):
        xf = stamp_x - spacing * 1.3 + speed * (t - t0) - i * spacing
        ti = t0 + (stamp_x - (stamp_x - spacing * 1.3 - i * spacing)) / speed
        ts.append(ti)
        if xf < -300 or xf > 2300:
            continue
        _mini_frame(c, xf, ty - 210, 310, 390, seed=3 + i * 5)
        # mühür izi (ti'den sonra)
        km = clamp((t - ti) / 0.18)
        if km > 0.003:
            CM.mini_palle(f, xf, ty - 200, 104, mono=True, color="#B33620", alpha=0.92 * km)
    # tokmak
    ph = 0.0
    for ti in ts:
        d = abs(t - ti)
        if d < 0.18:
            ph = max(ph, 1.0 - d / 0.18)
    top = 110
    hy = lerp(top + 130, ty - 318, ease_out(ph, 2.0)) if ph > 0 else top + 130
    c.drawRect(skia.Rect.MakeLTRB(stamp_x - 9, 0, stamp_x + 9, hy), P("#5A3A1C", 255))
    c.drawRect(skia.Rect.MakeLTRB(stamp_x - 9, 0, stamp_x + 9, hy), S("#2A170B", 1.6, 220))
    c.drawRoundRect(skia.Rect.MakeLTRB(stamp_x - 54, hy, stamp_x + 54, hy + 54), 8, 8, P("#8A1810", 255))
    c.drawRoundRect(skia.Rect.MakeLTRB(stamp_x - 54, hy, stamp_x + 54, hy + 54), 8, 8, S("#2A0806", 2.6, 255))
    c.drawRect(skia.Rect.MakeLTRB(stamp_x - 30, hy - 22, stamp_x + 30, hy + 4), P("#B07F22", 255))
    if sign_at is not None:
        k = cx.amt(sign_at, 0.8)
        if k > 0.003:
            wd = 960
            c.save()
            c.translate(960, 150 - (1 - sk.back_out(k)) * 220)
            for dx in (-wd / 2 + 60, wd / 2 - 60):
                f.line(dx, -120, dx, 0, color="#4A2C16", sw=3, alpha=k)
            CM.tablet(f, -wd / 2, 0, wd, 112, alpha=k, corner=10)
            CM.ink(f, "DEVLET DAİRESİ", 0, 76, face="title", size=64, color=TH.fg, align="c", track=10, alpha=k, emboss=False)
            c.restore()
    L.end(cx, cam, motes_n=22)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_sancak ═════════════════════════════
@CM.ckind("c12_sancak")
def k_sancak(cx, rise_at=0.0, rise_dur=2.4, c1="#F6EEDA", c2="#B8261A", pole_x=470, flag_w=980, flag_h=600, seed=41, ovl=None, **_):
    """Şövalye tarikatının sancağı (beyaz zemin, kızıl haç) direğe çekilir ve dalgalanır; ardında akşam göğü + güneş parıltısı. (kurdu: sancak yükselir)"""
    import cilt_deniz as DN
    f, c, cam = L.begin(cx, seed=seed, dress=None, bg="clear", clear="#E9C998")
    t = cx.t
    sh = f.lin(0, -400, 0, 1500, [("#8FA2C4", 0.0), ("#E9C998", 0.5), ("#F4D6A4", 1.0)])
    f.rect(-600, -400, 3400, 2400, shader=sh)
    f.circle(1500, 330, 170, shader=f.rad(1500, 330, 170, [("#FFF4D0", 0.0, 255), ("#FFE2A0", 0.5, 200), ("#FFE2A0", 1.0, 0)]))
    f.circle(1500, 330, 520, shader=f.rad(1500, 330, 520, [("#FFE9B0", 0.0, 90), ("#FFE9B0", 1.0, 0)]))
    rs = np.random.RandomState(4)
    for i in range(7):
        cxx = 200 + i * 300 + rs.rand() * 120
        cyy = 220 + rs.rand() * 380
        for j in range(4):
            f.oval(cxx + j * 70 - 100, cyy + rs.rand() * 20, 160 + rs.rand() * 80, 36 + rs.rand() * 14, color="#FFFFFF", alpha=0.22 + 0.1 * rs.rand(), blur=14)
    k = ease_out(clamp((t - cx.at(rise_at)) / rise_dur), 2.2)
    top_y = lerp(820, 150, k)
    # direk
    f.rect(pole_x - 12, 90, 24, 1100, shader=f.lin(pole_x - 12, 0, pole_x + 12, 0, [("#8A5A32", 0.0), ("#C8925A", 0.4), ("#4A2C16", 1.0)]))
    f.circle(pole_x, 82, 26, shader=f.rad(pole_x - 6, 74, 30, [("#FFF1B8", 0.0, 255), ("#B07F22", 1.0, 255)]))
    c.drawLine(pole_x, 90, pole_x, 1190, S("#2A170B", 1.6, 200))
    # sancak
    DN.flag(c, pole_x + 12, top_y, flag_w, flag_h, t, shape="rect", dev="cross", c1=c1, c2=c2, c3=c2, wind=0.85, amp=1.0)
    # çekme ipi
    c.drawLine(pole_x + 30, 130, pole_x + 30, top_y + flag_h, S("#4A3410", 2.0, 220))
    # zemin: taş
    f.rect(-600, 1010, 3400, 400, shader=f.lin(0, 1010, 0, 1410, [("#7A6A52", 0.0), ("#3A2E22", 1.0)]))
    f.line(-600, 1010, 3400, 1010, color="#E8D6AA", sw=3, alpha=0.6)
    L.end(cx, cam, motes_n=18)
    if ovl:
        ovl(cx)


# ═════════════════════════════ c12_dal ═════════════════════════════
def _bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def _tapered(c, pts, w0, w1, k, col, edge="#2A170B", a=255):
    """Uzunluğun k oranına kadar incelen dal gövdesi."""
    n = max(2, int(len(pts) * k))
    pp = pts[:n + 1]
    if len(pp) < 2:
        return pp[-1] if pp else None
    L_, R_ = [], []
    for i, (x, y) in enumerate(pp):
        j0, j1 = max(0, i - 1), min(len(pp) - 1, i + 1)
        dx, dy = pp[j1][0] - pp[j0][0], pp[j1][1] - pp[j0][1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        w = lerp(w0, w1, i / max(1, len(pts) - 1)) / 2
        L_.append((x + nx * w, y + ny * w))
        R_.append((x - nx * w, y - ny * w))
    path = sk.poly_path(L_ + R_[::-1])
    c.drawPath(path, P(col, a))
    c.drawPath(path, S(edge, 2.4, int(0.9 * a)))
    for q in range(1, 5):
        i0 = int(len(pp) * q / 5)
        if i0 < len(pp) - 1:
            c.drawLine(pp[i0][0], pp[i0][1], pp[min(len(pp) - 1, i0 + 6)][0] + 4, pp[min(len(pp) - 1, i0 + 6)][1], S("#4A2C16", 1.6, int(0.5 * a)))
    return pp[-1]


def _leafcl(c, x, y, r, ang, col, a=255):
    c.save()
    c.translate(x, y)
    c.rotate(ang)
    pth = skia.Path()
    pth.moveTo(0, 0)
    pth.quadTo(r * 0.55, -r * 0.5, r * 1.3, 0)
    pth.quadTo(r * 0.55, r * 0.5, 0, 0)
    c.drawPath(pth, P(col, a))
    c.drawPath(pth, S("#2F4A24", 1.0, int(0.6 * a)))
    c.restore()


@CM.ckind("c12_dal")
def k_dal(cx, grow_at=0.0, branch_at=None, bud_at=None, medal_at=None, medal_key="m_cosimo1", shield_at=None, seed=43, ovl=None, **_):
    """Medici ağacı: ana gövde yükselir (kalkan), YAN KOL sağa uzar, ucunda tomurcuk → madalya açılır. (yan kol = soyut sözcük oyunu; ağaç dalı)"""
    import cilt_medal as CMD
    f, c, cam = L.begin(cx, seed=seed, dress=None)
    t = cx.t
    kg = ease_out(clamp((t - cx.at(grow_at)) / 1.6), 2.0)
    sway = math.sin(t * 0.9) * 6
    trunk = _bez((620, 1180), (600 + sway * 0.4, 900), (640 + sway, 600), (610 + sway * 1.5, 360))
    _tapered(c, trunk, 96, 34, kg, "#6A4426")
    # ana taç yaprakları
    if kg > 0.5:
        rs = np.random.RandomState(7)
        top = trunk[-1]
        for i in range(34):
            ang = rs.uniform(0, 360)
            rr = rs.uniform(30, 150)
            x = top[0] + math.cos(math.radians(ang)) * rr * 1.3
            y = top[1] - 40 + math.sin(math.radians(ang)) * rr * 0.8
            _leafcl(c, x, y, 52, ang + math.sin(t * 1.3 + i) * 8, ["#6A8A4A", "#7FA058", "#5A7A3E"][i % 3], int(255 * clamp((kg - 0.5) * 2)))
    # kalkan (MEDİCİ)
    if shield_at is not None:
        ks = cx.amt(shield_at, 0.7)
        if ks > 0.003:
            icons.draw_icon(f, "shield", trunk[-1][0] + 8, trunk[-1][1] - 40 - (1 - ks) * 80, size=210 * (0.8 + 0.2 * ease_out(ks)), metal="gold", alpha=ks, glow=0.2 * ks)
    # yan kol
    kb = ease_io(clamp((t - cx.at(branch_at)) / 1.5), 1.8) if branch_at is not None else 0.0
    tip = None
    if kb > 0.002:
        br = _bez((612, 780), (780 + sway, 760), (960, 700), (1280 + sway, 560))
        tip = _tapered(c, br, 46, 16, kb, "#6A4426")
        rs = np.random.RandomState(11)
        for i in range(int(18 * kb)):
            j = int(len(br) * min(1.0, (i + 1) / 19.0 * kb))
            if j < len(br):
                x, y = br[j]
                _leafcl(c, x, y - 6, 34, -40 - 20 * (i % 3) + math.sin(t * 1.5 + i) * 7, "#7FA058")
                _leafcl(c, x, y + 6, 30, 38 + 15 * (i % 2) + math.sin(t * 1.4 + i) * 7, "#6A8A4A")
    # tomurcuk → madalya
    if tip is not None and bud_at is not None:
        kd = cx.amt(bud_at, 0.5)
        if kd > 0.003 and medal_at is not None and cx.t < cx.at(medal_at):
            c.drawCircle(tip[0], tip[1], 20 * kd, P("#A8D07A", int(255 * kd)))
            c.drawCircle(tip[0], tip[1], 20 * kd, S("#2F4A24", 2, int(255 * kd)))
    if tip is not None and medal_at is not None:
        km = cx.amt(medal_at, 0.9)
        if km > 0.003:
            e = ease_out(km, 2.4)
            mx, my = tip[0] + 90, tip[1] - 10
            ms = 400 * (0.15 + 0.85 * e)
            c.drawCircle(mx, my, ms * 0.62, P("#FFF1B8", int(55 * km)))
            CMD.draw_medal_b(f, medal_key, mx, my, ms, "bronze", False, alpha=km, tilt=0.12 * math.sin(t * 0.6), inscription=False, shadow=0.5)
            CM.name_plate(f, "COSIMO", None, None, cx_=mx, y=my + ms * 0.52, t=cx.amt(medal_at, 0.6, off=0.5), w=380)
    L.end(cx, cam, motes_n=24)
    if ovl:
        ovl(cx)
