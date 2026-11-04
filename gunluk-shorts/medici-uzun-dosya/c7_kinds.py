"""c7_kinds — c7 «26 Nisan 1478» özel çekim türleri (Parça 3 sahne yazarı). `scenes_c7.py` içinde import edilir; `@CM.ckind` ile kaydolur.

AĞIR BÖLÜM, MİZAH KAPALI. Kaynakta olmayan çan / saat / şafak / ışık koşulu / Paskalya / koku GÖRÜNTÜDE DE YOK:
  * nef dünyası (`c7_nave`): çan sarkacı, mum/meşale/şamdan, asılı kandil, pencere ışık huzmesi, buhurdan YOK (cilt_pano.Nave alt sınıfı; yalnız sütun/tonoz/kalabalık/siluet).
  * Şiddet GÖSTERİLMEZ: siluet, işaret (ince parlak çizgi), gölge, pigment yıkama (kızıl bulut), tally (çetele) çizgileri. Beden/kan/ceset/asılı beden/ip YOK.
  * Renk anahtarı (brif): sabah kireç beyazı → defter sarısı (neden) → tunç/kızıl (saldırı; yalnız pigment) → lacivert (yas; ekran örtüsü, saat anlamı taşımaz).
Zamanlar cümle/sözcük çapalı (cx.at / cx.amt).
"""
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_cam
import cilt_kinds2 as K2
import cilt_medal as CMD
import cilt_medici as CM
import cilt_oda as OD
import cilt_pano as PN
import cilt_paper as PP
import icons
import icons_extra  # noqa: F401  (chains vb.)
import medal
import p3_lib as L
import sk
from cilt_medici import TH
from p3_lib import INK, INKR, P, S, FILLP, GRAD_V, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth
from sk import C, H, W

OV = PN.OV
SIL = "#120A06"
RIM = "#B8A888"


def look(wx, wy, z=1.0, rot=0.0):
    """Anahtar kare: dünya (wx,wy) noktası ekran merkezinde, zoom z (cam=[(çapa, look(...)), …])."""
    return (z * (wx - W / 2), z * (wy - H / 2), z, rot)


def veil(f, color="#1E2A5A", a=0.0):
    """Ekran örtüsü (renk anahtarı: lacivert yas / kızıl vurgu). Saat/ışık iddiası taşımaz."""
    if a <= 0.003:
        return
    f.c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(color, 255 * a))


def pigment_bloom(f, x, y, k, color="#8E2A1A", maxr=1500, a=0.85, seed=3):
    """Pigment yıkama: (x,y) merkezli, kenarı lekeli kızıl bulut büyür (k 0..1). Kan değil: boya yıkaması (sulu pigment, kâğıt dokusu üstünde).
    Hızlı: önceden renklendirilmiş radyal sprite'lar (PN.glow) + tamamlanınca düz dolgu."""
    if k <= 0.003:
        return
    c = f.c
    r = maxr * ease_out(k)
    rs = np.random.RandomState(seed)
    for i in range(8):
        ang = rs.uniform(0, 6.283)
        d = rs.uniform(0.0, 0.35) * r
        rr = r * rs.uniform(0.55, 0.95)
        PN.glow(c, x + math.cos(ang) * d, y + math.sin(ang) * d * 0.6, rr, color, a * rs.uniform(0.45, 0.72) * min(1.0, k * 2.2))
    PN.glow(c, x, y, r * 0.8, color, a * 0.8 * min(1.0, k * 2.0))
    if k > 0.55:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(color, int(255 * a * 0.92 * clamp((k - 0.55) / 0.35))))


# ═════════════════════════════ NEF DÜNYASI (çan / mum / ışık huzmesi YOK) ═════════════════════════════
class C7Nave(PN.Nave):
    """cilt_pano.Nave'nin sadeleştirilmiş sürümü: sütun sırası, tonoz, vitray pencereler, zemin; ÇAN SARKACI / ŞAMDAN-MUM / ASILI KANDİL / IŞIK HUZMESİ yok.
    Kalabalık ve figürler `stations` ile gelir (st_crowd, st_sil, st_ayin)."""
    name = "c7_nave"

    def build(self):
        super().build()
        self.candles = []                                     # şamdan/mum yok (kaynaksız)

    def default_stations(self):
        return []

    def _draw_wall(self, fr, xa, xb):
        super()._draw_wall(fr, xa, xb)
        # kör kemerlerdeki kandil ışığını sil (kaynaksız ışık yok): kemer içi düz koyu zemin
        c = fr.c
        i0 = int(math.floor(xa / PN.BAY)) - 1
        i1 = int(math.ceil(xb / PN.BAY)) + 1
        for i in range(i0, i1 + 1):
            xc = i * PN.BAY + PN.BAY / 2
            c.drawCircle(xc, PN.Y_FLOOR - 120, 46, skia.Paint(AntiAlias=True, Color=C("#2C221A")))

    NOCOL = [(4300, 6700), (7000, 8300), (8500, 9900)]       # ana düzlem x aralıkları: ön plan sütunu aksiyonu örtmesin

    def _draw_fg(self, fr, xa, xb):
        c = fr.c
        T = self.T
        step = 1180
        i0 = int(math.floor(xa / step)) - 1
        R_, INKR_ = PN.R, PN.INKR
        for i in range(i0, i0 + int((xb - xa) / step) + 3):
            x = i * step + 540
            if x < xa - 200 or x > xb + 200:
                continue
            xm = x / 1.38
            if any(a_ <= xm <= b_ for a_, b_ in self.NOCOL):
                continue
            w = 118
            col = T("#5C5C56", 0.0)
            R_(c, x - w / 2, OV - 40, x + w / 2, 960, col)
            sh = skia.GradientShader.MakeLinear([(x - w / 2, 0), (x + w / 2, 0)], [C("#FFFFFF", 48), C("#FFFFFF", 0), C("#000000", 90)], [0, 0.33, 1.0])
            c.drawRect(skia.Rect.MakeLTRB(x - w / 2, OV - 40, x + w / 2, 960), skia.Paint(Shader=sh))
            INKR_(c, x - w / 2, OV - 40, x + w / 2, 960, 1.5, 190)
            for yy in (150, 176, 196):
                R_(c, x - w * 0.7, yy, x + w * 0.7, yy + (18 if yy == 150 else 12), T("#6A6A62", 0.0))
                INKR_(c, x - w * 0.7, yy, x + w * 0.7, yy + (18 if yy == 150 else 12), 1.2, 180)
            R_(c, x - w * 0.72, 830, x + w * 0.72, 960, T("#4A4A44", 0.0))
            INKR_(c, x - w * 0.72, 830, x + w * 0.72, 960, 1.4, 190)
            for k in range(-2, 3):
                c.drawLine(x + k * 20, 220, x + k * 20, 822, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#000000", 36)))

    def dyn_wall(self, ctx):
        # ışık huzmesi ve asılı kandil çizilmez; yalnız havada süzülen toz (atmosfer)
        c, t = ctx.c, ctx.t
        rs = PN._RS(7)
        for k in range(16):
            x = ctx.xa + ((rs.rand() * (ctx.xb - ctx.xa) + t * 9 * (0.5 + rs.rand())) % (ctx.xb - ctx.xa))
            y = 160 + rs.rand() * 560 + math.sin(t * 0.5 + k) * 10
            c.drawCircle(x, y, 1.4 + 1.8 * rs.rand(), skia.Paint(AntiAlias=True, Color=C("#EFE5C8", int(60 + 70 * rs.rand()))))

    def dyn_main(self, ctx):
        xa, xb = ctx.xa, ctx.xb
        for st in ctx.stations:
            fn = st.get("fn")
            if fn is None:
                continue
            x = st.get("x", 0)
            if x < xa - 1200 or x > xb + 1200:
                continue
            ctx.st = st
            fn(ctx, st)


PN.WORLDS["c7_nave"] = C7Nave


def _ts(ctx, st):
    return ctx.t - st.get("_at", 0.0)


def st_crowd(ctx, st):
    """Kalabalık istasyonu. st: x0, x1, n, seed, mode ('stand' | 'kneel' | 'to_kneel' | 'rise'), kneel_at / rise_at (çapa), gap=(x0,x1) boş bırakılan aralık, h, y0, y1.
    to_kneel: kalabalık `kneel_at` anında dalga halinde diz çöker (soldan sağa)."""
    f, t, cx = ctx.f, ctx.t, ctx.cx
    x0, x1 = st["x0"], st["x1"]
    mem = FA.crowd_members(st.get("seed", 1), st.get("n", 30), (x0, st.get("y0", 772), x1, st.get("y1", 858)), st.get("h", (214, 252)))
    mode = st.get("mode", "stand")
    tk = cx.at(st["kneel_at"]) if st.get("kneel_at") is not None else None
    tr = cx.at(st["rise_at"]) if st.get("rise_at") is not None else None
    gap = st.get("gap")
    for m in mem:
        if m["x"] < ctx.xa - 240 or m["x"] > ctx.xb + 240:
            continue
        if gap and gap[0] < m["x"] < gap[1]:
            continue
        kit, bh = FA.kit_for(m["kind"], m["seed"], m["h"])
        T = t
        if mode == "stand":
            p = FA.act_talk(kit, T + m["r2"] * 3.0, m["phase"], energy=0.35) if m["talk"] else FA.stand(kit, T + m["r2"] * 3.0, m["phase"])
        elif mode == "kneel":
            p = FA.act_kneel(kit, T, m["phase"], t0=-3.0, dur=0.1, rise_at=(tr + 0.5 * (m["x"] - x0) / max(1.0, x1 - x0) + 0.2 * m["r"]) if tr is not None else None)
        elif mode == "to_kneel":
            t0_ = (tk if tk is not None else 1e9) + 0.9 * (m["x"] - x0) / max(1.0, x1 - x0) + 0.35 * m["r"]
            p = FA.act_kneel(kit, T, m["phase"], t0=t0_, dur=1.3)
        else:
            p = FA.stand(kit, T, m["phase"])
        FA.cloth_for(kit, p, T, m["phase"] * 6.28, lag=0.0, wave=0.0)
        FA._draw_pose(f, kit, bh, p, m["x"], m["y"], m["h"], m["dir0"], 1.0, None)


def st_sil(ctx, st):
    """Siluet figür istasyonu (yüz yok). st: x, y, h, kind, seed, dir, action, walk=(x_son, hız), walk_at (çapa), at, fade_x, prop, color, alpha_at / alpha_out (çapa; solma)."""
    f, t, cx = ctx.f, ctx.t, ctx.cx
    x, y, h = st["x"], st.get("y", 840), st.get("h", 262)
    dirn = st.get("dir", 1)
    al = 1.0
    if st.get("alpha_in") is not None:
        al *= clamp((t - cx.at(st["alpha_in"])) / 0.6)
    if st.get("alpha_out") is not None:
        al *= 1.0 - clamp((t - cx.at(st["alpha_out"])) / 0.8)
    if al <= 0.01:
        return
    walk = st.get("walk")
    v_now = 0.0
    if walk is not None:
        x1, v = walk
        w0 = cx.at(st["walk_at"]) if st.get("walk_at") is not None else 0.0
        dist = x1 - x
        u = clamp((t - w0) * abs(v) / max(1.0, abs(dist)))
        x = x + dist * u
        dirn = 1 if dist >= 0 else -1
        v_now = abs(v) if 0 < u < 1 else 0.0
    if "fade_x" in st:
        xa_, xb_ = st["fade_x"]
        al *= clamp((xb_ - x) / (xb_ - xa_)) if xb_ > xa_ else clamp((x - xb_) / (xa_ - xb_))
        if al <= 0.01:
            return
    col = st.get("color", SIL)
    hat_kw = {"hat": st.get("hat")} if ("hat" in st or st.get("kind", "soylu") == "soylu") else {}
    if walk is not None:
        OD.sil_actor(f, st.get("kind", "soylu"), x, y, h, t, dir=dirn, seed=st.get("seed", 3), color=col, rim=st.get("rim", RIM), rim_dir=st.get("rim_dir", 1), alpha=al, walker=v_now, prop=st.get("prop"), run=bool(st.get("run")) and v_now > 0, **hat_kw)
    else:
        kw = {}
        if st.get("at") is not None and st.get("action", "idle") in ("bow", "kneel", "point", "write", "count", "threat", "cheer", "pray", "handshake"):
            kw["t0"] = cx.at(st["at"])
        for k_ in ("target", "depth", "dur", "mode", "period", "pray", "rise_at"):
            if k_ in st:
                kw[k_] = cx.at(st[k_]) if k_ == "rise_at" else st[k_]
        OD.sil_actor(f, st.get("kind", "soylu"), x, y, h, t, action=st.get("action", "idle"), dir=dirn, seed=st.get("seed", 3), color=col, rim=st.get("rim", RIM), rim_dir=st.get("rim_dir", 1),
                     alpha=al, prop=st.get("prop"), **kw, **hat_kw)


def st_ayin(ctx, st):
    """Yüksek ayin alayı (kaynaklı: «yüksek ayin»): haçlı rahip, kitaplı kardinal, çocuk; yavaş yürür. Mum/meşale/buhurdan YOK."""
    f, t = ctx.f, ctx.t
    x = st["x"]
    yg = 836
    base = x + st.get("speed", 46.0) * t
    FA.walker(f, "rahip", base + 260, yg, 252, t, speed=st.get("speed", 46.0), dir=1, seed=51, prop="cross", phase=0.0)
    FA.walker(f, "kardinal", base + 130, yg + 6, 250, t, speed=st.get("speed", 46.0), dir=1, seed=52, prop="book", phase=0.35)
    FA.walker(f, "cocuk", base, yg + 12, 214, t, speed=st.get("speed", 46.0), dir=1, seed=53, phase=0.1)
    FA.walker(f, "rahip", base - 130, yg + 16, 238, t, speed=st.get("speed", 46.0), dir=1, seed=55, phase=0.6)


def st_mark(ctx, st):
    """İŞARET (hançer işareti): hedef figürün gövdesinde kısa, parlak, ince çizgi — çapa anında çakar, sönerken pigment yıkama başlar.
    st: x, y (işaret merkezi), at, ang (derece), L (uzunluk). Kan/yara çizilmez."""
    c = ctx.c
    ts = _ts(ctx, st)
    if ts < 0 or ts > 1.1:
        return
    k = 1.0 - clamp(ts / 1.1)
    x, y = st["x"], st["y"]
    ang = math.radians(st.get("ang", -62))
    Lg = st.get("L", 120)
    dx, dy = math.cos(ang) * Lg / 2, math.sin(ang) * Lg / 2
    grow = clamp(ts / 0.12)
    c.drawLine(x - dx * grow, y - dy * grow, x + dx * grow, y + dy * grow, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C("#FFF1C4", int(120 * k)), StrokeCap=skia.Paint.kRound_Cap, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)))
    c.drawLine(x - dx * grow, y - dy * grow, x + dx * grow, y + dy * grow, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#FFFFFF", int(255 * k)), StrokeCap=skia.Paint.kRound_Cap))



def _human_path(x, y, h, w=0.30):
    """Basit insan silueti yolu (baş + omuz + gövde): ayak (x,y), boy h. Kesik çizgi çerçeve için."""
    hr = h * 0.072
    hy = y - h + hr * 1.1
    p = skia.Path()
    p.addCircle(x, hy, hr)
    bw = h * w
    p.moveTo(x - bw * 0.50, y - h * 0.80)
    p.quadTo(x - bw * 0.62, y - h * 0.55, x - bw * 0.46, y - h * 0.30)
    p.lineTo(x - bw * 0.52, y)
    p.lineTo(x + bw * 0.52, y)
    p.lineTo(x + bw * 0.46, y - h * 0.30)
    p.quadTo(x + bw * 0.62, y - h * 0.55, x + bw * 0.50, y - h * 0.80)
    p.quadTo(x, y - h * 0.86, x - bw * 0.50, y - h * 0.80)
    p.close()
    return p


def st_gap(ctx, st):
    """Boş yer: kesik çizgili insan çerçevesi (henüz gelmemiş kişi). st: x, y, h, at, col, a."""
    c, t = ctx.c, ctx.t
    ts = _ts(ctx, st)
    k = clamp(ts / 0.9)
    if k <= 0.003:
        return
    x, y, h = st["x"], st.get("y", 844), st.get("h", 262)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C(st.get("col", "#2A1A0C"), int(210 * k * st.get("a", 1.0))), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    pa.setPathEffect(skia.DashPathEffect.Make([13, 11], -t * 14))
    c.drawPath(_human_path(x, y, h * (0.97 + 0.03 * k)), pa)
    c.drawPath(_human_path(x, y, h * (0.97 + 0.03 * k)), skia.Paint(AntiAlias=True, Color=C("#FFFFFF", int(26 * k))))


def st_stain(ctx, st):
    """Zeminde lacivert pigment lekesi (beden YOK): büyür, yavaşça oturur. st: x, y, rx, ry, at, dur, col, a."""
    c = ctx.c
    ts = _ts(ctx, st)
    k = ease_out(clamp(ts / st.get("dur", 2.4)))
    if k <= 0.003:
        return
    x, y = st["x"], st.get("y", 842)
    rx, ry = st.get("rx", 190) * (0.35 + 0.65 * k), st.get("ry", 30) * (0.35 + 0.65 * k)
    col = st.get("col", "#1C2A66")
    a = st.get("a", 0.78)
    rs = np.random.RandomState(7)
    for i in range(5):
        dx = rs.uniform(-0.45, 0.45) * rx
        dy = rs.uniform(-0.3, 0.3) * ry
        c.drawOval(skia.Rect.MakeLTRB(x + dx - rx * rs.uniform(0.45, 0.8), y + dy - ry * rs.uniform(0.5, 0.9), x + dx + rx * rs.uniform(0.45, 0.8), y + dy + ry * rs.uniform(0.5, 0.9)),
                   skia.Paint(AntiAlias=True, Color=C(col, int(255 * a * 0.34 * k)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9)))
    c.drawOval(skia.Rect.MakeLTRB(x - rx * 0.78, y - ry * 0.7, x + rx * 0.78, y + ry * 0.7), skia.Paint(AntiAlias=True, Color=C("#0E1640", int(255 * a * 0.42 * k)), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5)))


def st_walk_group(ctx, st):
    """Siluet grubu (hepsi aynı hat boyunca): st: items=[dict(st_sil alanları)] — bire bir st_sil çağırır (kısayol)."""
    for it in st["items"]:
        d = dict(it)
        d.setdefault("_at", st.get("_at", 0.0))
        st_sil(ctx, d)



def st_door(ctx, st):
    """Sakristi kapısı (nef içinde, tunç iki kanat + taş sivri kemer çerçeve). st: x, y, h, open (sabit) | open0 + close_at/dur (kapanır). Aralıktan ışık çizilmez (koyu iç)."""
    c, cx = ctx.c, ctx.cx
    x, y, h = st["x"], st.get("y", 852), st.get("h", 400)
    op = st.get("open", 0.0)
    if st.get("close_at") is not None:
        u = clamp((ctx.t - cx.at(st["close_at"])) / st.get("dur", 1.5))
        op = st.get("open0", 0.85) * (1.0 - smooth(u))
    w = h * 0.56
    # taş çerçeve (sivri kemer)
    ap = skia.Path()
    ap.moveTo(x - w * 0.5 - 26, y)
    ap.lineTo(x - w * 0.5 - 26, y - h * 0.80)
    ap.quadTo(x - w * 0.5 - 26, y - h * 1.10, x, y - h * 1.22)
    ap.quadTo(x + w * 0.5 + 26, y - h * 1.10, x + w * 0.5 + 26, y - h * 0.80)
    ap.lineTo(x + w * 0.5 + 26, y)
    ap.close()
    c.drawPath(ap, P("#8F928A"))
    c.drawPath(ap, S("#1A1008", 2.6, 220))
    inner = skia.Path()
    inner.moveTo(x - w * 0.5, y)
    inner.lineTo(x - w * 0.5, y - h * 0.80)
    inner.quadTo(x - w * 0.5, y - h * 1.04, x, y - h * 1.14)
    inner.quadTo(x + w * 0.5, y - h * 1.04, x + w * 0.5, y - h * 0.80)
    inner.lineTo(x + w * 0.5, y)
    inner.close()
    c.drawPath(inner, P("#17100B"))
    OD.door_bronze(ctx.f, x, y, h * 0.96, open_amount=op, w=w, seed=st.get("seed", 5), light=False, t=ctx.t)



def st_hl(ctx, st):
    """Pencere/nesne vurgusu: kesikli dikdörtgen çerçeve (pigment kızılı) + hafif lacivert dolgu. st: x, y (alt-orta), w, h, at, col."""
    c, t = ctx.c, ctx.t
    ts = _ts(ctx, st)
    k = clamp(ts / 0.7)
    if k <= 0.003:
        return
    x, y, w, h = st["x"], st["y"], st.get("w", 90), st.get("h", 110)
    r = skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y)
    c.drawRoundRect(r, 8, 8, P("#1C2A66", int(60 * k)))
    pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C(st.get("col", "#8E2A1A"), int(235 * k)), StrokeCap=skia.Paint.kRound_Cap)
    pr.setPathEffect(skia.DashPathEffect.Make([12, 9], -t * 12))
    c.drawRoundRect(r, 8, 8, pr)


def draw_tags(f, cx, tags):
    """Ekran uzayı levhalar: tags=[dict(text, at, x, y, size, track, sub, hold, w)]."""
    for d in tags or ():
        L.tag(f, cx, d["text"], d["x"], d["y"], at=d["at"], size=d.get("size", 36), track=d.get("track", 7), sub=d.get("sub"), hold=d.get("hold"), w=d.get("w"), dur=d.get("dur", 0.55), face=d.get("face", "title_m"))


def _auto_y(cams):
    """cams=[(çapa,(x,y,z))]: y=None → zum ne olursa olsun figürlerin ayakları bantta kalacak şekilde otomatik dikey kayma (y = 380 − 370/z)."""
    if not cams:
        return cams
    out = []
    for a, v in cams:
        x, y, z = v[0], v[1], v[2]
        if y is None:
            y = max(0.0, 380.0 - 370.0 / max(1.0, z))
        out.append((a, (x, y, z)))
    return out


@CM.ckind("c7_nef")
def k_c7_nef(cx, stations=(), cams=None, tags=(), veil_=None, bloom=None, shake=None, kick=None, caption=None, **kw):
    """Nef (Santa Maria del Fiore) — `c7_nave` panorama dünyası (çan/mum/ışık huzmesi yok) + üst katman:
    tags=[dict(text, at, x, y, hold, sub, size, dy)] dünya koordinatında (x, ayak y) levhalar kamerayı izler; veil_=(renk, alfa, çapa_a, süre) ekran örtüsü;
    bloom=dict(x, y (ekran), at, color, maxr, dur) pigment yıkama; shake=(çapa, süre, genlik) kısa el kamerası sarsıntısı (hand2 yalnız V6–V7)."""
    import shots as SH
    ucams = _auto_y(cams)
    if shake is not None and ucams:
        t0 = cx.at(shake[0])
        dt = cx.t - t0
        if 0 <= dt < shake[1]:
            a_ = shake[2] * math.exp(-dt * 4.0)
            ucams = [(a, (v[0] + a_ * math.sin(cx.t * 61.0), v[1] + a_ * 0.6 * math.sin(cx.t * 47.0 + 1.0), v[2])) for a, v in ucams]
    SH.KINDS["pano"](cx, pano="c7_nave", cams=ucams, stations=list(stations), kick=kick, caption=caption, **kw)
    f = cx.f
    if cams and tags:
        camx, camy, z = L.cam_probe(cx, ucams, None)
        for d in tags:
            sx, sy = L.world_to_screen(camx, camy, z, d["x"], d.get("y", 840) - d.get("h", 280) - 28)
            sy += d.get("dy", 0)
            sx += d.get("dx", 0)
            if -200 < sx < W + 200:
                L.tag(f, cx, d["text"], sx, sy, at=d["at"], size=d.get("size", 36), track=d.get("track", 7), sub=d.get("sub"), hold=d.get("hold"), dur=0.55)
    if bloom is not None:
        k = clamp((cx.t - cx.at(bloom["at"])) / bloom.get("dur", 1.0))
        bx, by = bloom.get("x"), bloom.get("y")
        if "wx" in bloom and cams:
            camx, camy, z = L.cam_probe(cx, ucams, None)
            bx, by = L.world_to_screen(camx, camy, z, bloom["wx"], bloom["wy"])
        pigment_bloom(f, bx, by, k, color=bloom.get("color", "#8E2A1A"), maxr=bloom.get("maxr", 1500), a=bloom.get("a", 0.85))
    if veil_ is not None:
        col, a_, anc, dur = veil_
        veil(f, col, a_ * clamp((cx.t - cx.at(anc)) / dur))


cilt_cam.OWN_CAMERA.add("c7_nef")


# ═════════════════════════════ ortak sarmalayıcılar (tag/damga/örtü; gravür seçeneği) ═════════════════════════════
def _overlay(f, cx, tags=(), stamps=(), veil_=None):
    draw_tags(f, cx, tags)
    for s_ in stamps or ():
        L.stamp_at(f, cx, s_[0], s_[1], s_[2], s_[3], rot=s_[5] if len(s_) > 5 else -0.09, size=s_[4] if len(s_) > 4 else 44)
    if veil_ is not None:
        col, a_, anc, dur = veil_
        veil(f, col, a_ * clamp((cx.t - cx.at(anc)) / dur))


@CM.ckind("c7_med")
def k_c7_med(cx, tags=(), stamps=(), veil_=None, mono=False, icons_=(), **kw):
    """Standart `medal` + ekran levhaları / damgalar / lacivert örtü; icons_=[dict(kind, x, y, size, at, metal, glow)] madalya üstüne simge (ör. zincir)."""
    import shots as SH
    if mono:
        L.mono_begin(cx.f)
    SH.KINDS["medal"](cx, **kw)
    if mono:
        L.mono_end(cx.f)
    for d in icons_:
        k = ease_out(cx.amt(d["at"], d.get("dur", 0.7)))
        if k > 0.01:
            icons.draw_icon(cx.f, d["kind"], d["x"], d["y"] + (1 - k) * d.get("drop", 0), size=d.get("size", 400) * (0.9 + 0.1 * k), metal=d.get("metal", "bronze"), alpha=k, shadow=True, glow=d.get("glow", 0.0))
    _overlay(cx.f, cx, tags, stamps, veil_)


@CM.ckind("c7_oda")
def k_c7_oda(cx, tags=(), stamps=(), veil_=None, mono=False, **kw):
    """`oda` dünyası + ekran levhaları/damga/örtü (gravür seçeneği)."""
    import shots as SH
    if mono:
        L.mono_begin(cx.f)
    SH.KINDS["oda"](cx, **kw)
    if mono:
        L.mono_end(cx.f)
    _overlay(cx.f, cx, tags, stamps, veil_)


@CM.ckind("c7_sehir")
def k_c7_sehir(cx, tags=(), stamps=(), veil_=None, mono=False, follow=(), **kw):
    """`sehir` dünyası + ekran levhaları/damga/örtü (gravür seçeneği). follow=[dict(text, at, x (sayı|callable(t)), y, h, dy, sub, hold, size)]: dünya koordinatında kişiyi izleyen levha (kw['cams'] gerekir)."""
    import shots as SH
    if mono:
        L.mono_begin(cx.f)
    SH.KINDS["sehir"](cx, **kw)
    if mono:
        L.mono_end(cx.f)
    if follow and kw.get("cams"):
        camx, camy, z = L.cam_probe(cx, kw["cams"], None)
        for d in follow:
            wx = d["x"](cx.t) if callable(d["x"]) else d["x"]
            sx, sy = L.world_to_screen(camx, camy, z, wx, d.get("y", 850) - d.get("h", 260) - 30)
            if -200 < sx < W + 200:
                L.tag(cx.f, cx, d["text"], sx + d.get("dx", 0), sy + d.get("dy", 0), at=d["at"], size=d.get("size", 32), track=d.get("track", 6), sub=d.get("sub"), hold=d.get("hold"), dur=0.5)
    _overlay(cx.f, cx, tags, stamps, veil_)


@CM.ckind("c7_palle")
def k_c7_palle(cx, tags=(), stamps=(), veil_=None, crown_at=None, **kw):
    """`palle` arması (altın zemin) + isteğe bağlı KESİKLİ TAÇ (unvan yok): crown_at çapasında arma üstünde kesik çizgili taç belirir, üstü çizilir."""
    import shots as SH
    SH.KINDS["palle"](cx, **kw)
    f = cx.f
    c = f.c
    if crown_at is not None:
        k = cx.amt(crown_at, 0.9)
        if k > 0.003:
            x, y = 960, 232
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#2A1A0C", int(225 * k)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            pr.setPathEffect(skia.DashPathEffect.Make([16, 12], -cx.t * 16))
            w_ = 270
            pts = [(x - w_ / 2, y + 74), (x - w_ / 2 - 8, y - 22), (x - w_ / 4, y + 26), (x, y - 56), (x + w_ / 4, y + 26), (x + w_ / 2 + 8, y - 22), (x + w_ / 2, y + 74)]
            p = skia.Path()
            p.moveTo(*pts[0])
            for q in pts[1:]:
                p.lineTo(*q)
            p.close()
            c.drawPath(p, pr)
            c.drawLine(x - w_ / 2 - 20, y + 100, x + w_ / 2 + 20, y + 100, pr)
    _overlay(f, cx, tags, stamps, veil_)


for _k in ("c7_oda", "c7_sehir"):
    cilt_cam.OWN_CAMERA.add(_k)


# ═════════════════════════════ ortak: kâğıt zemin ═════════════════════════════
def _paper(cx, seed=1, dress="top"):
    f = cx.f
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=dress)
    cam.begin(f)
    return cam


def _node_name(f, text, x, y, size=30, al=1.0, track=7):
    CM.ink(f, text, x, y, face="title_m", size=size, color=TH.fg, align="c", track=track, alpha=al, emboss=False)


def _arrow_path(c, p0, p1, k, col="#8E2A1A", w=4.4, dash=(15, 11), a=225, head=True, t=0.0, bend=0.0):
    """p0→p1 kesikli ok (k: 0..1 uzama). bend: dik yönde yay."""
    if k <= 0.003:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    ctrl = (mx + nx * bend, my + ny * bend)
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(ctrl[0], ctrl[1], p1[0], p1[1])
    pm = skia.PathMeasure(path, False)
    seg = skia.Path()
    pm.getSegment(0, pm.getLength() * clamp(k), seg, True)
    pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap)
    if dash:
        pr.setPathEffect(skia.DashPathEffect.Make(list(dash), -t * 24))
    c.drawPath(seg, pr)
    if head and k > 0.97:
        pos, tan = pm.getPosTan(pm.getLength())
        ang = math.atan2(tan.fY, tan.fX)
        hs = 22
        tri = skia.Path()
        tri.moveTo(pos.fX, pos.fY)
        tri.lineTo(pos.fX - hs * math.cos(ang - 0.45), pos.fY - hs * math.sin(ang - 0.45))
        tri.lineTo(pos.fX - hs * math.cos(ang + 0.45), pos.fY - hs * math.sin(ang + 0.45))
        tri.close()
        c.drawPath(tri, skia.Paint(AntiAlias=True, Color=C(col, int(a))))


# ═════════════════════════════ c7s7, c7s10: komplo panosu (madalya düğümleri) ═════════════════════════════
@CM.ckind("c7_ag")
def k_c7_ag(cx, nodes=(), edges=(), tags=(), stamps=(), seed=41, veil_=None, **_):
    """Kâğıt üstünde madalya düğümleri + ip/ok kenarları. nodes=[dict(id, key, name, x, y, size, at, out (çapa: solar+gri), ring (çapa: kesikli halka), sub, hub=True (görünmez düğüm))];
    edges=[(a, b, çapa, stil)] stil: 'red' (kesikli kızıl ok) | 'gold' (düz yaldız çizgi) | 'ink'. Kaynak: yalnız bölümde adı geçen kişiler; yüz iddiası yok (stilize madalya)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    pos = {n["id"]: (n["x"], n["y"], n.get("size", 240)) for n in nodes}
    for e in edges:
        a, b, at = e[0], e[1], e[2]
        stl = e[3] if len(e) > 3 else "red"
        k = ease_io(cx.amt(at, 1.0))
        pa, pb = pos[a], pos[b]
        ra = 0.0 if any(n["id"] == a and n.get("hub") for n in nodes) else pa[2] * 0.56
        rb = 0.0 if any(n["id"] == b and n.get("hub") for n in nodes) else pb[2] * 0.56
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        ln = math.hypot(dx, dy) or 1.0
        na = next((n for n in nodes if n["id"] == a), {})
        nb = next((n for n in nodes if n["id"] == b), {})
        p0 = (pa[0] + dx / ln * ra, pa[1] + dy / ln * ra)
        p1 = (pb[0] - dx / ln * rb, pb[1] - dy / ln * rb)
        if na.get("eoff") is not None:
            p0 = (pa[0], pa[1] + na["eoff"])
        if nb.get("eoff_in") is not None:
            p1 = (pb[0], pb[1] + nb["eoff_in"])
        bend = e[4] if len(e) > 4 else 0.0
        if stl == "red":
            _arrow_path(c, p0, p1, k, "#8E2A1A", 4.6, (15, 11), 230, head=not any(n["id"] == b and n.get("hub") for n in nodes), t=cx.t, bend=bend)
        elif stl == "gold":
            _arrow_path(c, p0, p1, k, "#B8923C", 4.0, None, 235, head=False, t=cx.t, bend=bend)
        else:
            _arrow_path(c, p0, p1, k, "#4A3A28", 3.0, (10, 8), 200, head=False, t=cx.t, bend=bend)
    for n in nodes:
        if n.get("hub"):
            continue
        k = ease_out(cx.amt(n["at"], 0.8))
        if k <= 0.01:
            continue
        x, y, sz = n["x"], n["y"], n.get("size", 240)
        ko = ease_io(cx.amt(n["out"], 0.9)) if n.get("out") is not None else 0.0
        c.save()
        if ko > 0.01:
            c.saveLayer(None, skia.Paint(ColorFilter=L.gray_filter(0.85 * ko)))
        CMD.draw_medal_b(f, n["key"], x, y + (1 - k) * 18, sz * (0.92 + 0.08 * k), "bronze", alpha=k * (1 - 0.35 * ko), tilt=0.07 * math.sin(cx.t * 0.55 + x * 0.01))
        if ko > 0.01:
            c.restore()
        c.restore()
        if n.get("ring") is not None:
            kr = ease_out(cx.amt(n["ring"], 0.6))
            if kr > 0.01:
                pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.2, Color=C("#8E2A1A", int(225 * kr)), StrokeCap=skia.Paint.kRound_Cap)
                pr.setPathEffect(skia.DashPathEffect.Make([16, 12], -cx.t * 18))
                c.drawCircle(x, y, sz * 0.58, pr)
        al = k * (1 - 0.4 * ko)
        _node_name(f, n["name"], x, y + sz * 0.63 + 12, size=n.get("nsize", 30), al=al)
        if n.get("sub"):
            CM.ink(f, n["sub"], x, y + sz * 0.63 + 12 + n.get("nsize", 30) * 0.95, face="cap_i", size=n.get("nsize", 30) * 0.78, color=TH.fg2, align="c", alpha=al, emboss=False)
    cam.end(f)
    _overlay(f, cx, tags, stamps, veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ gravür figür/mekân yardımcıları ═════════════════════════════
def _bust(c, x, ysh, w, col="#1A1008", a=255, bob=0.0):
    """Masa başı büst siluet: omuz hattı (ysh) üstünde baş + gövde (aşağı doğru taşar, masa örter)."""
    r = w * 0.26
    c.drawCircle(x, ysh - r * 1.25 + bob, r, P(col, a))
    p = skia.Path()
    p.moveTo(x - w * 0.52, ysh + 220)
    p.lineTo(x - w * 0.50, ysh + w * 0.12)
    p.quadTo(x - w * 0.44, ysh - w * 0.06, x - w * 0.12, ysh - w * 0.04 + bob)
    p.lineTo(x + w * 0.12, ysh - w * 0.04 + bob)
    p.quadTo(x + w * 0.44, ysh - w * 0.06, x + w * 0.50, ysh + w * 0.12)
    p.lineTo(x + w * 0.52, ysh + 220)
    p.close()
    c.drawPath(p, P(col, a))


def _church(c, x, y, w, h, col="#3A3228", line="#1A1008", a=255):
    """Katedral cephesi (genel, sivri kemerli): gövde + beşik çatı + gül pencere + üç kapı + yan kule bloğu (çan YOK)."""
    body = skia.Rect.MakeLTRB(x - w / 2, y - h, x + w / 2, y)
    c.drawRect(body, P(col, a))
    c.drawRect(body, S(line, 2.4, 220))
    gable = sk.poly_path([(x - w / 2 - 14, y - h), (x, y - h - h * 0.30), (x + w / 2 + 14, y - h)])
    c.drawPath(gable, P(col, a))
    c.drawPath(gable, S(line, 2.4, 220))
    # kubbe (arkada)
    c.drawArc(skia.Rect.MakeLTRB(x - w * 0.30, y - h - h * 0.62, x + w * 0.30, y - h * 0.9), 180, 180, True, P("#4A4034", a))
    # gül pencere
    c.drawCircle(x, y - h * 0.68, w * 0.10, P("#E8DCC0", int(a * 0.85)))
    c.drawCircle(x, y - h * 0.68, w * 0.10, S(line, 2.4, 220))
    for k in range(8):
        ang = k * math.pi / 4
        c.drawLine(x, y - h * 0.68, x + math.cos(ang) * w * 0.10, y - h * 0.68 + math.sin(ang) * w * 0.10, S(line, 1.6, 200))
    # üç kapı
    for dx in (-w * 0.28, 0, w * 0.28):
        dw = w * 0.15 if dx == 0 else w * 0.11
        dh = h * 0.42 if dx == 0 else h * 0.32
        p = skia.Path()
        p.moveTo(x + dx - dw / 2, y)
        p.lineTo(x + dx - dw / 2, y - dh + dw * 0.5)
        p.quadTo(x + dx, y - dh - dw * 0.35, x + dx + dw / 2, y - dh + dw * 0.5)
        p.lineTo(x + dx + dw / 2, y)
        p.close()
        c.drawPath(p, P("#120A06", a))
    # yan pilastr
    for sx in (-1, 1):
        c.drawRect(skia.Rect.MakeLTRB(x + sx * w * 0.5 - 14, y - h, x + sx * w * 0.5 + 14, y), P("#2A241C", a))


# ═════════════════════════════ c7s8: ilk plan — ziyafet → kilise (gravür) ═════════════════════════════
@CM.ckind("c7_plan")
def k_c7_plan(cx, a_open=0.0, a_feast=None, a_gap=None, a_move=None, a_church=None, a_stamp=None, tags=(), seed=43, **_):
    """İlk plan ziyafette uygulanacaktı; Giuliano gelmeyince saldırı kiliseye kaydırıldı (ANLATILIR → gravür dili). Sol: sofra + masa başı siluetler, bir BOŞ sandalye (kesikli); sağ: katedral cephesi; aralarında kesikli ok."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    kf = ease_out(cx.amt(a_feast, 0.8)) if a_feast is not None else ka
    kg = ease_out(cx.amt(a_gap, 0.8)) if a_gap is not None else 0.0
    km = ease_io(cx.amt(a_move, 1.3)) if a_move is not None else 0.0
    kc = ease_out(cx.amt(a_church, 0.9)) if a_church is not None else 0.0
    L.mono_begin(f)
    c.save()
    c.translate(0, (1 - ka) * 12)
    # sofra
    if kf > 0.01:
        tx0, tx1, ty = 150, 900, 640
        # masa başı büstler (arkada)
        for i, bx in enumerate((250, 380, 650, 780)):
            _bust(c, bx, ty - 112, 120, "#1A1008", int(255 * kf), bob=1.6 * math.sin(cx.t * 1.1 + i * 1.7))
        # boş sandalye: kesik çizgili büst
        if kg > 0.01:
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.4, Color=C("#1A1008", int(230 * kg)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
            pr.setPathEffect(skia.DashPathEffect.Make([12, 10], -cx.t * 12))
            c.drawPath(_human_path(515, ty + 70, 330, 0.34), pr)
        # masa
        c.drawRect(skia.Rect.MakeLTRB(tx0, ty - 26, tx1, ty + 14), P("#C9B88E", int(255 * kf)))
        c.drawRect(skia.Rect.MakeLTRB(tx0, ty - 26, tx1, ty + 14), S("#1A1008", 2.6, 230 * kf))
        c.drawRect(skia.Rect.MakeLTRB(tx0 + 14, ty + 14, tx1 - 14, ty + 120), P("#B8A678", int(255 * kf)))
        c.drawRect(skia.Rect.MakeLTRB(tx0 + 14, ty + 14, tx1 - 14, ty + 120), S("#1A1008", 2.0, 200 * kf))
        for i in range(9):
            xx = tx0 + 40 + i * 84
            c.drawLine(xx, ty + 14, xx - 6, ty + 120, S("#1A1008", 1.4, 120 * kf))
        for i, px in enumerate((250, 380, 515, 650, 780)):
            c.drawOval(skia.Rect.MakeLTRB(px - 34, ty - 38, px + 34, ty - 24), P("#F4EEDC", int(255 * kf)))
            c.drawOval(skia.Rect.MakeLTRB(px - 34, ty - 38, px + 34, ty - 24), S("#1A1008", 1.6, 210 * kf))
        # kadehler
        for gx_ in (315, 585, 715):
            c.drawLine(gx_, ty - 26, gx_, ty - 50, S("#1A1008", 2.4, 230 * kf))
            c.drawPath(sk.poly_path([(gx_ - 11, ty - 74), (gx_ + 11, ty - 74), (gx_ + 7, ty - 50), (gx_ - 7, ty - 50)]), P("#E8DCC0", int(255 * kf)))
            c.drawPath(sk.poly_path([(gx_ - 11, ty - 74), (gx_ + 11, ty - 74), (gx_ + 7, ty - 50), (gx_ - 7, ty - 50)]), S("#1A1008", 1.6, 220 * kf))
    # kilise
    if kc > 0.01:
        c.save()
        c.translate(0, (1 - kc) * 20)
        _church(c, 1450, 800, 560, 420, a=int(255 * kc))
        c.restore()
    c.restore()
    L.mono_end(f)
    # ok (renkli kesikli, gravür dışı)
    _arrow_path(c, (930, 520), (1130, 460), km, "#8E2A1A", 5.0, (16, 12), 235, head=True, t=cx.t, bend=-70)
    cam.end(f)
    draw_tags(f, cx, tags)
    if a_stamp is not None:
        L.stamp_at(f, cx, "ANLATILIR", 960, 250, a_stamp, rot=-0.07, size=52)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s14: yoklama — «sarılır gibi yapıp» (gravür) ═════════════════════════════
@CM.ckind("c7_yoklama")
def k_c7_yoklama(cx, a_open=0.0, a_embrace=None, a_check=None, a_armor=None, a_stamp=None, tags=(), seed=44, **_):
    """İki siluet karşı karşıya: soldaki Francesco yaklaşıp sarılır gibi yapar, eli ötekinin giysisinin altını yoklar (el vurma/yoklama hareketi);
    Giuliano'nun gövdesinde KESİKLİ zırh çerçevesi + «?» (ANLATILIR; gravür)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    ke = ease_io(cx.amt(a_embrace, 1.2)) if a_embrace is not None else 0.0
    kz = ease_out(cx.amt(a_armor, 0.8)) if a_armor is not None else 0.0
    te = cx.at(a_embrace) if a_embrace is not None else 0.0
    tc = cx.at(a_check) if a_check is not None else te + 3.0
    t0h = te if cx.t < tc - 0.35 else tc - 0.35
    yg, h = 905, 640
    xg = 1130
    xf = 700 + 150 * ke
    L.mono_begin(f)
    OD.sil_actor(f, "soylu", xg, yg, h, cx.t, action="idle", dir=-1, seed=8, color="#2A2218", rim=RIM, rim_dir=1, alpha=ka, hat=None)
    OD.sil_actor(f, "soylu", xf, yg, h * 0.98, cx.t, action="handshake", dir=1, seed=3, color="#14100A", rim=RIM, rim_dir=-1, alpha=ka, t0=t0h, M=(0.40, -0.52), hat=None)
    L.mono_end(f)
    if kz > 0.01:
        cx_, cy_ = xg - 6, yg - h * 0.60
        sc = h / 560.0
        pa = skia.Path()
        pa.moveTo(cx_ - 64 * sc, cy_ - 108 * sc)
        pa.quadTo(cx_, cy_ - 126 * sc, cx_ + 64 * sc, cy_ - 108 * sc)
        pa.lineTo(cx_ + 78 * sc, cy_ - 20 * sc)
        pa.quadTo(cx_ + 56 * sc, cy_ + 66 * sc, cx_, cy_ + 92 * sc)
        pa.quadTo(cx_ - 56 * sc, cy_ + 66 * sc, cx_ - 78 * sc, cy_ - 20 * sc)
        pa.close()
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.6, Color=C("#8E2A1A", int(235 * kz)), StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        pr.setPathEffect(skia.DashPathEffect.Make([13, 10], -cx.t * 14))
        c.drawPath(pa, pr)
        CM.ink(f, "?", cx_ + 150 * sc, cy_ - 150 * sc + (1 - kz) * 14, face="title", size=120, color="#8E2A1A", align="c", alpha=kz, emboss=False)
    cam.end(f)
    draw_tags(f, cx, tags)
    if a_stamp is not None:
        L.stamp_at(f, cx, "ANLATILIR", 960, 168, a_stamp, rot=-0.07, size=52)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s15: iki anlatı — komünyon ↔ ekmeğin kaldırılması ═════════════════════════════
def _host(c, x, y, r, a=1.0, glow=0.0):
    if glow > 0.01:
        PN.glow(c, x, y, r * 3.2, "#FFE9A8", 0.35 * glow * a)
    c.drawCircle(x, y, r, P("#F6F0DC", int(255 * a)))
    c.drawCircle(x, y, r, S("#2A1A0C", 2.4, 230 * a))
    c.drawLine(x - r * 0.42, y, x + r * 0.42, y, S("#8A6A30", 2.0, 200 * a))
    c.drawLine(x, y - r * 0.42, x, y + r * 0.42, S("#8A6A30", 2.0, 200 * a))


def _chalice(c, x, y, s=1.0, a=1.0):
    p = skia.Path()
    p.moveTo(x - 26 * s, y - 62 * s)
    p.lineTo(x + 26 * s, y - 62 * s)
    p.quadTo(x + 24 * s, y - 20 * s, x + 4 * s, y - 14 * s)
    p.lineTo(x + 4 * s, y + 6 * s)
    p.lineTo(x + 22 * s, y + 14 * s)
    p.lineTo(x - 22 * s, y + 14 * s)
    p.lineTo(x - 4 * s, y + 6 * s)
    p.lineTo(x - 4 * s, y - 14 * s)
    p.quadTo(x - 24 * s, y - 20 * s, x - 26 * s, y - 62 * s)
    p.close()
    c.drawPath(p, P("#C9A24A", int(255 * a)))
    c.drawPath(p, S("#2A1A0C", 2.2, 230 * a))


@CM.ckind("c7_iki_anlati")
def k_c7_iki_anlati(cx, a_open=0.0, a_l1=None, a_l2=None, a_r1=None, a_r2=None, a_kimi1=None, a_kimi2=None, tags=(), seed=45, **_):
    """Bölünmüş ekran: SOL «KİMİ… komünyon alışını söyler» (papaz sunakta), SAĞ «KİMİ… ekmeğin kaldırıldığı anı» (papaz, eller yukarıda, ekmek). İki varyant, tek cümle (Poliziano'ya atıf yok)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    for side, (x0, x1, kk, a1, a2, head, label, act) in enumerate((
            (70, 930, a_kimi1, a_l1, a_l2, "KİMİ", "KOMÜNYON", "pray"),
            (990, 1850, a_kimi2, a_r1, a_r2, "KİMİ", "EKMEĞİN KALDIRILMASI", "cheer"))):
        kp = ease_out(cx.amt(kk, 0.8)) if kk is not None else ka
        if kp < 0.99:
            # henüz anlatılmamış panel: kesikli boş çerçeve (yürüyen karıncalar) + «?»
            pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.6, Color=C("#2A1A0C", int(180 * ka * (1 - kp))), StrokeCap=skia.Paint.kRound_Cap)
            pr.setPathEffect(skia.DashPathEffect.Make([14, 11], -cx.t * 22))
            c.drawRoundRect(skia.Rect.MakeLTRB(x0, 190, x1, 840), 14, 14, pr)
            CM.ink(f, "?", (x0 + x1) / 2, 560, face="title", size=170, color="#2A1A0C", align="c", alpha=0.35 * ka * (1 - kp) * (0.8 + 0.2 * math.sin(cx.t * 2.4 + side)), emboss=False)
        if kp <= 0.01:
            continue
        mx = (x0 + x1) / 2
        c.save()
        c.translate(0, (1 - kp) * 18)
        # panel: kâğıt tablet
        CM.tablet(f, x0, 190, x1 - x0, 650, alpha=kp, corner=14)
        CM.ink(f, head, mx, 262, face="cap_i", size=42, color=TH.fg2, align="c", track=4, alpha=kp, emboss=False)
        # sunak
        c.drawRect(skia.Rect.MakeLTRB(mx - 190, 640, mx + 190, 700), P("#B8A678", int(255 * kp)))
        c.drawRect(skia.Rect.MakeLTRB(mx - 190, 640, mx + 190, 700), S("#2A1A0C", 2.4, 230 * kp))
        c.drawRect(skia.Rect.MakeLTRB(mx - 210, 624, mx + 210, 644), P("#D8CBA4", int(255 * kp)))
        c.drawRect(skia.Rect.MakeLTRB(mx - 210, 624, mx + 210, 644), S("#2A1A0C", 2.2, 230 * kp))
        # papaz siluet
        t0 = cx.at(a1) if a1 is not None else 0.0
        OD.sil_actor(f, "rahip", mx, 622, 380, cx.t, action=act, dir=1, seed=7 + side, color=SIL, rim=RIM, alpha=kp)
        if side == 0:
            _chalice(c, mx - 90, 616, 0.9, kp)
            ka2 = ease_out(cx.amt(a2, 0.6)) if a2 is not None else 0.0
            _host(c, mx + 70, 612 - 8 * ka2, 22, kp)
        else:
            kh = ease_out(cx.amt(a2, 0.7)) if a2 is not None else 0.0
            ky = 612 - (250 + 20 * kh) * kh
            _host(c, mx + 22, ky if kh > 0.01 else 612, 38, kp, glow=kh)
        c.restore()
        # etiket
        k2 = cx.amt(a2 if a2 is not None else kk, 0.6)
        if k2 > 0.01:
            wd = sk.text_width(label, "title_m", 38, 6) + 70
            CM.tablet(f, mx - wd / 2, 760 - 40 + (1 - k2) * 10, wd, 80, alpha=k2, corner=8)
            CM.ink(f, label, mx, 772, face="title_m", size=38, color=TH.fg, align="c", track=6, alpha=k2, emboss=False)
    # ortadaki ayrım çizgisi
    c.drawLine(960, 200, 960, 830, S("#2A1A0C", 3.0, 190 * ka))
    cam.end(f)
    draw_tags(f, cx, tags)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ çetele (tally): sayılar yazılır, ceset/kan çizilmez ═════════════════════════════
def _tally_layout(n, area=(260, 400, 1660, 900)):
    """n çentik → beşli gruplar; grid (cols×rows) ve hücre boyutu. Dönüş: [(gx, gy)], cell_w, cell_h, kaç grup."""
    ng = (n + 4) // 5
    x0, y0, x1, y1 = area
    aw, ah = x1 - x0, y1 - y0
    best = None
    for cols in range(1, ng + 1):
        rows = (ng + cols - 1) // cols
        cw = aw / cols
        ch = ah / rows
        s = min(cw / 1.0, ch / 1.0 * 1.05)
        if best is None or s > best[0]:
            best = (s, cols, rows, cw, ch)
    _, cols, rows, cw, ch = best
    pos = []
    for g in range(ng):
        r_, c_ = divmod(g, cols)
        pos.append((x0 + (c_ + 0.5) * cw, y0 + (r_ + 0.5) * ch))
    return pos, min(cw, ch * 1.05), ch


def _stroke(c, p0, p1, col, w, a, wob_seed):
    rs = np.random.RandomState(wob_seed)
    mx, my = (p0[0] + p1[0]) / 2 + rs.uniform(-2.5, 2.5), (p0[1] + p1[1]) / 2 + rs.uniform(-2.5, 2.5)
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(mx, my, p1[0], p1[1])
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=C(col, int(a)), StrokeCap=skia.Paint.kRound_Cap)
    pa.setPathEffect(skia.DiscretePathEffect.Make(9.0, 1.2, wob_seed % 997))
    c.drawPath(path, pa)


@CM.ckind("c7_tally")
def k_c7_tally(cx, n=19, a0=0.0, a1=None, wash=None, num=None, num_at=None, sub=None, sub_at=None, area=(260, 400, 1660, 900), mark_col=None, tags=(), veil_=None, wash_k=1.0, seed=47, num_col=None, **_):
    """Çetele çizgileri (beşli gruplar), a0→a1 arasında teker teker çizilir. wash: None | 'red' | 'navy' (pigment yıkama zemini; önceki çekimden devam eder). num: büyük sayı yazısı (num_at'ta oyulur), sub: altyazı satırı (sub_at).
    Hiçbir beden/kan çizilmez; yalnız sayma işareti."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    if wash:
        col = {"red": "#8E2A1A", "navy": "#1C2A66"}.get(wash, wash)

        def _wash(fr):
            pigment_bloom(fr, W / 2, H / 2 - 40, 1.0, color=col, maxr=1900 * wash_k, a=0.96, seed=seed)
            fr.c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P(col, 70))
        L.blit(c, L.bake(("c7wash", col, seed, wash_k), W, H, _wash), W / 2, H / 2)
    mc = mark_col or ("#F4EEDC" if wash else "#2A1A0C")
    pos, cell, ch = _tally_layout(n, area)
    t0 = cx.at(a0)
    t1 = cx.at(a1) if a1 is not None else t0 + n * 0.12
    prog = clamp((cx.t - t0) / max(0.05, t1 - t0))
    shown = prog * n
    sc = min(1.0, cell / 240.0)
    for g, (gx, gy) in enumerate(pos):
        for j in range(5):
            idx = g * 5 + j
            if idx >= n:
                break
            kk = clamp(shown - idx)
            if kk <= 0.001:
                continue
            w_ = 9.0 * (0.55 + 0.45 * sc)
            hh = min(ch * 0.80, 300 * (0.45 + 0.55 * sc))
            if j < 4:
                xx = gx + (j - 1.5) * (cell * 0.17)
                p0 = (xx, gy - hh / 2)
                p1 = (xx + 3, gy - hh / 2 + hh * kk)
            else:
                p0 = (gx - cell * 0.33, gy + hh * 0.30)
                p1 = (gx - cell * 0.33 + cell * 0.66 * kk, gy + hh * 0.30 - hh * 0.62 * kk)
            _stroke(c, p0, p1, mc, w_, 235, 1000 + idx * 17)
    cam.end(f)
    if num is not None and num_at is not None:
        kn = cx.amt(num_at, 0.9)
        if kn > 0.003:
            sp = CM.engraved(num, "title", 190, 14.0, num_col or ("#F4EEDC" if wash else TH.fg))
            CM.draw_spr(f, sp, W / 2, 330 - (1 - kn) * 10, "c", alpha=min(1.0, kn * 1.6), reveal=clamp(kn * 1.2), shadow=0.5)
    if sub is not None:
        L.tag(f, cx, sub, W / 2, 470 if num else 330, at=sub_at, size=34, track=8, dur=0.5, w=sk.text_width(sub, "title_m", 34, 8) + 80)
    _overlay(f, cx, tags, (), veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s31: Lorenzo pencerede (gravür; ANLATILIR) ═════════════════════════════
@CM.ckind("c7_pencere")
def k_c7_pencere(cx, a_open=0.0, a_win=None, a_wave=None, a_cheer=None, a_stamp=None, tags=(), seed=48, veil_=None, **_):
    """Medici Sarayı'nın penceresi: karanlık kemerli pencerede Lorenzo SİLUETİ (boynunda sargı bandı, el kaldırır), altta alkışlayan kalabalık siluetleri; pencere çevresinde altın parıltı (renkli işaret). Gravür dili (anlatılır)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    kw = ease_out(cx.amt(a_win, 0.9)) if a_win is not None else ka
    kv = ease_in(clamp(cx.amt(a_wave, 1.2))) if a_wave is not None else 0.0
    kc = ease_out(cx.amt(a_cheer, 0.9)) if a_cheer is not None else 0.0
    L.mono_begin(f)
    # sarayın taş duvarı (bugnato sıraları)
    wx0, wx1, wy0, wy1 = 320, 1600, 130, 760
    c.drawRect(skia.Rect.MakeLTRB(wx0, wy0, wx1, wy1), P("#BFA77F", int(255 * ka)))
    rs = np.random.RandomState(5)
    rowh = 62
    for r_i, yy in enumerate(range(wy0, wy1, rowh)):
        c.drawLine(wx0, yy, wx1, yy, S("#3A2A18", 1.8, 150 * ka))
        off = (r_i % 2) * 90
        for xx in range(wx0 + off, wx1, 180):
            c.drawLine(xx, yy, xx, yy + rowh, S("#3A2A18", 1.4, 120 * ka))
    c.drawRect(skia.Rect.MakeLTRB(wx0, wy0, wx1, wy1), S("#1A1008", 3.0, 230 * ka))
    c.drawRect(skia.Rect.MakeLTRB(wx0 - 30, wy1 - 6, wx1 + 30, wy1 + 28), P("#8E8576", int(255 * ka)))
    # pencere (sivri çift kemer)
    px, py, pw, ph = 960, 540, 250, 380
    arch = skia.Path()
    arch.moveTo(px - pw / 2, py)
    arch.lineTo(px - pw / 2, py - ph * 0.62)
    arch.quadTo(px - pw / 2, py - ph, px, py - ph * 1.08)
    arch.quadTo(px + pw / 2, py - ph, px + pw / 2, py - ph * 0.62)
    arch.lineTo(px + pw / 2, py)
    arch.close()
    c.drawPath(arch, P("#1A1008", int(255 * ka)))
    c.drawPath(arch, S("#E8DCC0", 12, 235 * ka))
    c.drawPath(arch, S("#1A1008", 2.6, 235 * ka))
    # pencere içi: Lorenzo
    if kw > 0.01:
        c.save()
        c.clipPath(arch, skia.ClipOp.kIntersect, True)
        by = py - 40 + (1 - kw) * 130
        c.drawCircle(px, by - 112, 44, P("#C8BA9A", int(255 * kw)))               # baş (yüzsüz; açık siluet)
        sh = skia.Path()
        sh.moveTo(px - 118, py + 10)
        sh.lineTo(px - 108, by - 22)
        sh.quadTo(px - 70, by - 52, px - 24, by - 58)
        sh.lineTo(px + 24, by - 58)
        sh.quadTo(px + 70, by - 52, px + 108, by - 22)
        sh.lineTo(px + 118, py + 10)
        sh.close()
        c.drawPath(sh, P("#C8BA9A", int(255 * kw)))
        # boyunda sargı bandı
        c.drawPath(sk.smooth_path([(px - 40, by - 72), (px, by - 58), (px + 40, by - 72)], False, 0.5), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=15, Color=C("#FFFFFF", int(255 * kw)), StrokeCap=skia.Paint.kRound_Cap))
        # kalkan kol (el sallar)
        sw = math.sin(cx.t * 5.2) * 0.35 * kv
        ax, ay = px + 92, by - 20
        ex, ey = ax + 40 + 30 * math.sin(sw), ay - 96 - 18 * math.cos(sw)
        c.drawLine(ax, ay, ex, ey, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=30 * kv + 0.1, Color=C("#C8BA9A", int(255 * kv)), StrokeCap=skia.Paint.kRound_Cap))
        c.drawCircle(ex, ey - 6, 17 * kv, P("#C8BA9A", int(255 * kv)))
        c.restore()
    # alkışlayan kalabalık (alt)
    if kc > 0.01:
        kinds = ("halk", "tuccar", "soylu", "soylu_f", "cocuk", "halk", "banker", "halk")
        for i in range(10):
            xx = 360 + i * 135 + (i % 2) * 28
            OD.sil_actor(f, kinds[i % len(kinds)], xx, 900 + (i % 2) * 8, 210 - (i % 3) * 14, cx.t, action="cheer", dir=1 if i % 2 else -1, seed=60 + i, color="#1A1008", rim="#B8A888", alpha=kc, amount=0.8, hop=0.6)
    L.mono_end(f)
    # altın parıltı (renk işareti): pencere çevresi
    if kw > 0.01:
        PN.glow(c, px, py - 150, 380, "#FFD27A", 0.36 * kw)
    cam.end(f)
    draw_tags(f, cx, tags)
    if a_stamp is not None:
        L.stamp_at(f, cx, "ANLATILIR", 960, 100, a_stamp, rot=-0.06, size=50)
    _overlay(f, cx, (), (), veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s38–c7s41: taraflar (üç sütun) ═════════════════════════════
@CM.ckind("c7_taraflar")
def k_c7_taraflar(cx, title=None, cols=(), tags=(), veil_=None, seed=49, **_):
    """Üç sütun: FLORANSA | ROMA | TARİHÇİLER (üçüncü sütun başlığı çapasında belirir; öncesinde gizli). cols=[dict(head, at, x, items=[dict(text|lines, at)], sub, sub_at, dim_at)];
    title=(metin, çapa) üst başlık. Öğeler çapalarında belirir; aynı öğeler sonraki çekimde zaten görünür (çapa geçmiş)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    if title is not None:
        kt = cx.amt(title[1], 0.8)
        if kt > 0.003:
            sp = CM.engraved(title[0], "title", 72, 12.0, TH.fg)
            CM.draw_spr(f, sp, W / 2, 150, "c", alpha=min(1.0, kt * 1.5), reveal=clamp(kt * 1.15))
    for col in cols:
        kh = ease_out(cx.amt(col["at"], 0.8))
        if kh <= 0.01:
            continue
        x = col["x"]
        wd = col.get("w", 540)
        c.save()
        c.translate(0, (1 - kh) * 16)
        CM.tablet(f, x - wd / 2, 230, wd, 650, alpha=kh, corner=14)
        CM.ink(f, col["head"], x, 310, face="title_m", size=44, color=TH.fg, align="c", track=8, alpha=kh, emboss=False)
        c.drawLine(x - wd * 0.36, 336, x + wd * 0.36, 336, S("#2A1A0C", 2.0, 170 * kh))
        if col.get("sub"):
            ks = cx.amt(col.get("sub_at", col["at"]), 0.6)
            CM.ink(f, col["sub"], x, 372, face="cap_i", size=30, color=TH.fg2, align="c", alpha=kh * ks, emboss=False)
        if col.get("icon"):
            first = col["items"][0]["at"] if col.get("items") else None
            kfirst = cx.amt(first, 0.6) if first is not None else 0.0
            ki_ = ease_out(cx.amt(col["at"], 0.9)) * (1.0 - kfirst)
            if ki_ > 0.01:
                icons.draw_icon(f, col["icon"], x, 620, size=col.get("icon_size", 230), metal=col.get("metal", "gold"), alpha=ki_, shadow=True, glow=0.1)
        yy = 430
        for it in col.get("items", ()):
            lines = it["text"].split("\n")
            ki = cx.amt(it["at"], 0.6)
            if ki > 0.003:
                for li, ln in enumerate(lines):
                    CM.ink(f, ln, x, yy + li * 44 + (1 - ki) * 8, face=it.get("face", "fell_i"), size=it.get("size", 38), color=it.get("color", INK), align="c", alpha=kh * ki, emboss=False)
                if it.get("hl"):
                    c.drawRect(skia.Rect.MakeLTRB(x - wd * 0.42, yy - 34, x + wd * 0.42, yy + len(lines) * 44 - 4), P("#E8C98A", int(70 * ki * kh)))
            yy += len(lines) * 44 + 34
        c.restore()
    cam.end(f)
    _overlay(f, cx, tags, (), veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s43: Medici süzgeci ═════════════════════════════
@CM.ckind("c7_suzgec")
def k_c7_suzgec(cx, a_open=0.0, a_fall=None, a_gap=None, a_none=None, names=(), tags=(), seed=50, veil_=None, **_):
    """Süzgeç (Medici topları) üstünden anlatı sayfaları geçer ve süzülmüş (kızıl topla damgalı) çıkar; altta kesikli BOŞ sayfa «Pazzi'lerin kendi sesi» + YOK damgası.
    names=[ad,…]: sayfa başlıkları (bölümde adı geçen kaynaklar)."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    cxs, cys, R_ = 960, 400, 280
    # süzgeç: tunç halka + ağ
    c.save()
    c.clipPath(skia.Path().addCircle(cxs, cys, R_ - 8), skia.ClipOp.kIntersect, True)
    c.drawRect(skia.Rect.MakeLTRB(cxs - R_, cys - R_, cxs + R_, cys + R_), P("#E8DCC0", int(70 * ka)))
    for k in range(-9, 10):
        c.drawLine(cxs + k * 28, cys - R_, cxs + k * 28, cys + R_, S("#5A3E22", 1.4, 150 * ka))
        c.drawLine(cxs - R_, cys + k * 28, cxs + R_, cys + k * 28, S("#5A3E22", 1.4, 150 * ka))
    c.restore()
    # sayfalar (süzgeçten geçer)
    t0 = cx.at(a_fall) if a_fall is not None else 0.0
    n = len(names)
    for i, nm in enumerate(names):
        ts = t0 + i * 0.55
        u = (cx.t - ts) / 2.6
        if u <= 0 or u >= 1.25:
            continue
        xx = cxs + (i - (n - 1) / 2) * 120
        yy = lerp(90, 760, clamp(u / 1.1))
        passed = yy > cys + 12
        w_, h_ = 150, 110
        al = ka * clamp(u * 5) * (1 - clamp((yy - (cys + R_ + 20)) / 90.0))
        c.save()
        c.translate(xx, yy)
        c.rotate(-4 + 3 * i + 2 * math.sin(cx.t * 1.3 + i))
        if yy < cys - 20 or yy > cys + 20:
            c.drawRect(skia.Rect.MakeLTRB(-w_ / 2, -h_ / 2, w_ / 2, h_ / 2), P("#F1E8CE", int(255 * al)))
            c.drawRect(skia.Rect.MakeLTRB(-w_ / 2, -h_ / 2, w_ / 2, h_ / 2), S("#2A1A0C", 2.0, 220 * al))
            for q in range(3):
                c.drawLine(-w_ * 0.36, -h_ * 0.16 + q * 22, w_ * 0.36, -h_ * 0.16 + q * 22, S("#3A2616", 1.6, 150 * al))
            CM.ink(f, nm, 0, -h_ * 0.30, face="cap_i", size=22, color=TH.fg, align="c", alpha=al, emboss=False)
            if passed:
                c.drawCircle(w_ * 0.30, h_ * 0.28, 15, P("#B33620", int(255 * al)))
                c.drawCircle(w_ * 0.30, h_ * 0.28, 15, S("#2A1A0C", 1.6, 220 * al))
        c.restore()
    # süzgeç ön halka + palle toplar
    c.drawCircle(cxs, cys, R_, S("#8A5A24", 16, 255 * ka))
    c.drawCircle(cxs, cys, R_, S("#2A1A0C", 2.6, 230 * ka))
    for k in range(6):
        ang = math.radians(-90 + (k - 2.5) * 22)
        bx, by = cxs + math.cos(ang) * (R_ + 32), cys + math.sin(ang) * (R_ + 32)
        c.drawCircle(bx, by, 17, P("#B33620", int(255 * ka)))
        c.drawCircle(bx, by, 17, S("#2A1A0C", 1.8, 230 * ka))
    # boş sayfa (kesikli) + YOK
    kg = ease_out(cx.amt(a_gap, 0.8)) if a_gap is not None else 0.0
    if kg > 0.01:
        pr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=C("#2A1A0C", int(220 * kg)), StrokeCap=skia.Paint.kRound_Cap)
        pr.setPathEffect(skia.DashPathEffect.Make([16, 12], -cx.t * 14))
        c.drawRect(skia.Rect.MakeLTRB(670, 745, 1250, 905), pr)
        CM.ink(f, "PAZZİ'LERİN KENDİ SESİ", 960, 840, face="title_m", size=30, color=TH.fg, align="c", track=5, alpha=kg, emboss=False)
    cam.end(f)
    if a_none is not None:
        L.stamp_at(f, cx, "YOK", 1390, 810, a_none, rot=-0.10, size=72)
    _overlay(f, cx, tags, (), veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s46: Bertoldo madalyası — dönen madalya ═════════════════════════════
@CM.ckind("c7_madalya")
def k_c7_madalya(cx, a_open=0.0, flips=(), a_cast=None, tags=(), stamps=(), size=620, pos=(960, 500), veil_=None, seed=51, **_):
    """İki yüzlü madalya: flips=[çapa,…] her çapada madalya ters döner (Lorenzo yüzü ↔ Giuliano yüzü). Başta ısı kızıllığı soğur («bronza döküldü»; a_cast). Yüz iddiası yok: stilize madalya."""
    f = cx.f
    c = f.c
    cam = _paper(cx, seed)
    ka = ease_out(cx.amt(a_open, 0.9))
    th = 0.0
    for fa in flips:
        u = clamp((cx.t - cx.at(fa)) / 0.75)
        th += ease_io(u) * math.pi
    face = int(math.floor((th + math.pi / 2) / math.pi)) % 2
    cs = abs(math.cos(th))
    keys = ("c7_pazzi_lor", "c7_pazzi_giu")
    key = keys[face]
    ins = medal.INSCR.get(key)
    img = CMD.medal_img(key, "bronze", ins, False, 720)
    x, y = pos
    s = size / 720.0
    PN.glow(c, x, y, size * 0.95, "#FFD27A", 0.20 * ka)
    c.save()
    c.translate(x + size * 0.035, y + size * 0.055)
    c.scale(s * max(0.03, cs), s)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(0.55 * ka)
    c.drawImage(CMD.medal_shadow(key, "bronze", ins, False, 720), -360, -360, CM._LIN, p)
    c.restore()
    c.save()
    c.translate(x, y)
    c.scale(s * max(0.03, cs), s)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(ka)
    c.drawImage(img, -360, -360, CM._LIN, p)
    # dönerken kenara doğru kararma
    if cs < 0.98:
        c.drawCircle(0, 0, 352, P("#1A1008", int(120 * (1 - cs) * ka)))
    # ısı kızıllığı (döküm): soğur
    if a_cast is not None:
        kh = 1.0 - clamp((cx.t - cx.at(a_cast)) / 2.4)
        if kh > 0.01:
            c.drawCircle(0, 0, 352, P("#FF7A28", int(150 * kh * ka)))
    c.restore()
    # kenar kalınlığı (ince elips) tam yanda
    if cs < 0.14:
        c.drawOval(skia.Rect.MakeLTRB(x - size * 0.03, y - size * 0.49, x + size * 0.03, y + size * 0.49), P("#8A5A24", int(255 * (1 - cs / 0.14) * ka)))
    cam.end(f)
    _overlay(f, cx, tags, stamps, veil_)
    CM.finish(f, cx, motes_n=22)


# ═════════════════════════════ c7s47: Floransa'nın Papa'yla barışı — ip kopar ═════════════════════════════
@CM.ckind("c7_son")
def k_c7_son(cx, a_open=0.0, a_thread=None, a_snap=None, a_veil=None, tags=(), veil_=None, seed=52, **_):
    """Solda Medici arması, sağda papalık anahtarları; ince altın ip ikisini bağlar. «ölmüştü» çapasında ip KOPAR (iki yarı sarkar, solar); renk lacivert yasa döner."""
    import shots as SH
    f = cx.f
    c = f.c
    ts = cx.at(a_snap) if a_snap is not None else 1e9
    dt = cx.t - ts
    # arma (palle) sol — standart palle kind (pos/size)
    SH.KINDS["palle"](cx, at=0.1, size=560, pos=(520, 500))
    ka = ease_out(cx.amt(a_open, 0.9))
    # anahtarlar sağ
    icons.draw_icon(f, "keys", 1400, 500, size=520, metal="gold", alpha=ka, shadow=True, glow=0.1)
    # ip
    kt = ease_io(cx.amt(a_thread, 1.4)) if a_thread is not None else ka
    x0, y0, x1, y1 = 800, 500, 1150, 500
    if kt > 0.01:
        if dt < 0:
            sag = 28 * math.sin(cx.t * 1.1) + 20
            path = skia.Path()
            path.moveTo(x0, y0)
            path.quadTo((x0 + x1) / 2, y0 + sag * 2, x1, y1)
            pm = skia.PathMeasure(path, False)
            seg = skia.Path()
            pm.getSegment(0, pm.getLength() * kt, seg, True)
            c.drawPath(seg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#C79A3C", int(240 * ka)), StrokeCap=skia.Paint.kRound_Cap))
        else:
            k = clamp(dt / 1.6)
            for sgn, xa_, xb_ in ((-1, x0, (x0 + x1) / 2), (1, x1, (x0 + x1) / 2)):
                drop = ease_in(k) * 150
                path = skia.Path()
                path.moveTo(xa_, y0)
                path.quadTo((xa_ + xb_) / 2, y0 + 30 + drop * 0.5, xb_ - sgn * -10 * k, y0 + drop)
                al = (1 - clamp((dt - 0.6) / 1.2)) * ka
                c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5.0, Color=C("#C79A3C", int(240 * al)), StrokeCap=skia.Paint.kRound_Cap))
    _overlay(f, cx, tags, (), None)
    # lacivert yas: kopuştan sonra derinleşir
    kv = ease_in(clamp((cx.t - cx.at(a_veil)) / 2.8)) if a_veil is not None else (ease_in(clamp(dt / 2.4)) if dt > 0 else 0.0)
    if veil_ is not None:
        col, a_, anc, dur = veil_
        veil(f, col, a_ * clamp((cx.t - cx.at(anc)) / dur))
    veil(f, "#101A44", 0.45 * kv)


@CM.ckind("c7_doc")
def k_c7_doc(cx, tags=(), stamps=(), veil_=None, **kw):
    """Standart `doc` + ekran levhaları/damga/örtü."""
    import shots as SH
    SH.KINDS["doc"](cx, **kw)
    _overlay(cx.f, cx, tags, stamps, veil_)


@CM.ckind("c7_map")
def k_c7_map(cx, tags=(), stamps=(), veil_=None, **kw):
    """Standart `map` + ekran levhaları/damga/örtü."""
    import shots as SH
    SH.KINDS["map"](cx, **kw)
    _overlay(cx.f, cx, tags, stamps, veil_)


for _k in ("c7_map",):
    cilt_cam.OWN_CAMERA.discard(_k)
