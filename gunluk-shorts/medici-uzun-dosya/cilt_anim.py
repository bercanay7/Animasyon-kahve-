"""cilt_anim — Medici cildi: HAREKETLİ FİGÜR KİTİ (cilt_figs üzerine; aynı çizgi / pigment / altın filet dili) + `procession` çekim türü.

Mimari ("kâğıt-kesim kukla" + mesh kaplama):
  * Her kostüm bir kez parçalara boyanır (PFig → sprite; torso, etek, baş, kollar, bacaklar, ayakkabı, eller, pelerin) ve önbelleğe alınır.
  * Kare başına yalnız İSKELET çözülür: yürüyüş = ayak yörüngesi + 2-kemik IK (ayak kaymaz), kollar FK/IK, gövde eğimi/zıplaması, baş dengesi;
    kollar-bacaklar `Skin` ile (omurga boyunca Catmull-Rom → skia.drawVertices) BÜKÜLÜR — eklemlerde kopukluk ve kesik çizgi yok;
    etek/pelerin kumaşı ise yürüyüşe tepki veren (sallanma, adımla öne itilme, rüzgâr dalgası) mesh'tir.
  * Pozlar arası geçiş eklem uzayında (konum/açı) yumuşak enterpolasyondur; kare çevirme yoktur.
Maliyet: ≈0,2–0,5 ms (h≈150) … 1–2 ms (h≈300) figür başına.

Genel API (hepsi `f` = sk.Frame, `t` saniye, `y` = ayak hizası ekran y'si, `h` = nominal boy px):
    FA.walker(f, kind, x, y, h, t, speed=90, dir=1, phase=0, **stil)        yürüyen figür (speed = zemine göre px/sn; 0 → bekleme/nefes)
    FA.actor(f, kind, x, y, h, t, action, dir=1, **p)                        yazma/sayma/işaret/konuşma/selam/diz çökme/el sıkışma … (bkz. ACTIONS)
    FA.crowd(f, t, rect, n, seed=1, wave=0.0, mode="mill", dir=1, ...)       kalabalık (faz kaymalı, dalga)
    FA.procession(f, t, ...)                                                 alay üretici (sancaktar, atlı, paj, ağır cübbeliler)
    FA.rider(f, x, y, h, t, speed=120, gait="walk", dir=1, **stil)           ata biniş (yürüyüş/tırıs/dörtnala)
    FA.threat(f, t, x, y, h, ...)                                            şiddet İŞARETİ: yalnız siluet jest (hançer yükselir), kan yok
Kimlikler (kind): tuccar, banker, katip, rahip, kardinal, soylu, soylu_f, asker, halk, cocuk, papa, kesis, denizci.
"""
import functools
import math
import random
import zlib

import numpy as np
import skia

import cilt_figs as FG
import cilt_medici as CM
import figs_horse as FH
import figs_kit as K
import figs_parts as FP
import sk
from figs_kit import K as KC, ell, lens, limb, place, poly, sp
from sk import C, H, W, clamp, mix, smooth

PIG = CM.PIG
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
INK = FG.INK
D2R = math.pi / 180.0


# ═════════════════════════════ matematik yardımcıları ═════════════════════════════
def lerp(a, b, t):
    return a + (b - a) * t


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease5(t):
    t = clamp(t)
    return t * t * t * (t * (t * 6 - 15) + 10)


def rot(x, y, deg):
    """(x,y) noktasını orijin çevresinde deg derece döndür (+ = saat yönü, ekran y aşağı)."""
    a = deg * D2R
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


def ik2(ax, ay, tx, ty, l1, l2, bend):
    """İki-kemik IK. (ax,ay) kök, (tx,ty) hedef. bend=+1/−1 dirsek tarafı. Dönüş: (ex,ey,wx,wy) — wx,wy erişilen uç (hedef erişim dışıysa kısaltılır)."""
    dx, dy = tx - ax, ty - ay
    d0 = math.hypot(dx, dy)
    dmax = (l1 + l2) * 0.9995
    dmin = abs(l1 - l2) + 1e-3
    d = min(max(d0, dmin), dmax)
    if d0 < 1e-6:
        dx, dy, d0 = 0.0, 1.0, 1.0
    ux, uy = dx / d0, dy / d0
    wx, wy = ax + ux * d, ay + uy * d
    cosA = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    A = math.acos(max(-1.0, min(1.0, cosA)))
    a = math.atan2(uy, ux) + bend * A
    return ax + l1 * math.cos(a), ay + l1 * math.sin(a), wx, wy


def hash01(*a):
    """Deterministik 0..1 sahte rastgele."""
    x = 0
    for v in a:
        x = (x * 1103515245 + int(v * 1000003) + 12345) & 0x7FFFFFFF
    x = (x ^ (x >> 13)) * 1274126177 & 0x7FFFFFFF
    return (x % 100003) / 100003.0


# ═════════════════════════════ sprite + mesh kaplama ═════════════════════════════
class Spr:
    """Kırpılmış sprite: figür başlangıcı (ayak, 0,0) görüntüde (ox,oy) pikselinde."""
    __slots__ = ("img", "ox", "oy", "w", "h")

    def __init__(self, img, ox, oy):
        self.img, self.ox, self.oy = img, ox, oy
        self.w, self.h = img.width(), img.height()


def blit(c, spr, jx, jy, X, Y, ang=0.0, sx=1.0):
    """Sprite'ı eklem noktası (jx,jy: figür-koordinatı) → hedef (X,Y); ang derece döndür; sx: x ölçeği (ayna)."""
    ix, iy = spr.ox + jx, spr.oy + jy
    if ang == 0.0 and sx == 1.0:
        c.drawImage(spr.img, X - ix, Y - iy, LIN)
        return
    c.save()
    c.translate(X, Y)
    if ang:
        c.rotate(ang)
    if sx != 1.0:
        c.scale(sx, 1.0)
    c.drawImage(spr.img, -ix, -iy, LIN)
    c.restore()


_CR = {}


def _cr_weights(u):
    u2 = u * u
    u3 = u2 * u
    b = (-0.5 * u3 + u2 - 0.5 * u, 1.5 * u3 - 2.5 * u2 + 1.0, -1.5 * u3 + 2.0 * u2 + 0.5 * u, 0.5 * u3 - 0.5 * u2)
    d = (-1.5 * u2 + 2 * u - 0.5, 4.5 * u2 - 5 * u, -4.5 * u2 + 4 * u + 0.5, 1.5 * u2 - u)
    return b, d


class Skin:
    """Omurga boyunca bükülen sprite (mesh). Dinlenme omurgası (resim pikselinde) → güncel omurga (hedef koordinat).
    Satırlar omurga boyunca (segment başına rows[k]); iki sütun (arka/ön kenar) — her satırda eşleme d'de doğrusal olduğundan iki sütun yeter.
    pts: n+1 eklem noktası (Catmull-Rom ile yumuşatılır). Yalnız büyük dönüş/bükülme gereken parçalar (kol, bacak, at bacağı, kuyruk) için;
    kumaş (giysi, pelerin) hızlı `Strips` ile çizilir."""
    __slots__ = ("img", "n", "R", "Wm", "Dm", "tex", "idx", "dl", "dr", "pad0", "pad1", "shader", "paint", "nrows", "rest_len")

    def __init__(self, spr, rest, rows=(4, 4)):
        """spr: Spr; rest: dinlenme eklemleri figür koordinatında [(x,y)…] (dikey omurga)."""
        self.img = spr.img
        rest = [(spr.ox + x, spr.oy + y) for (x, y) in rest]
        self.n = n = len(rest) - 1
        rp = np.array(rest, float)
        seg = rp[1:] - rp[:-1]
        slen = np.hypot(seg[:, 0], seg[:, 1])
        ks, us = [], []
        for k in range(n):
            m = rows[k] if k < len(rows) else rows[-1]
            for j in range(m):
                ks.append(k)
                us.append(j / m)
        ks.append(n - 1)
        us.append(1.0)
        ks = np.array(ks)
        us = np.array(us)
        R = self.R = len(ks)
        Wm = np.zeros((R, n + 3))
        Dm = np.zeros((R, n + 3))
        for i in range(R):
            b, d = _cr_weights(float(us[i]))
            Wm[i, ks[i]:ks[i] + 4] = b
            Dm[i, ks[i]:ks[i] + 4] = d
        self.Wm, self.Dm = Wm, Dm
        tpos = rp[ks] + seg[ks] * us[:, None]
        tang = seg[ks] / np.maximum(slen[ks][:, None], 1e-9)
        for i in range(R):
            if us[i] == 0.0 and ks[i] > 0:
                a = seg[ks[i] - 1] / max(slen[ks[i] - 1], 1e-9)
                m = a + tang[i]
                tang[i] = m / max(np.hypot(m[0], m[1]), 1e-9)
        w_, h_ = spr.img.width(), spr.img.height()
        t0, t1 = tang[0], tang[-1]
        nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
        self.pad0 = float(max(0.0, rp[0, 1]))
        self.pad1 = float(max(0.0, h_ - rp[-1, 1]))
        xs = tpos[:, 0]
        self.dl = float(np.max(xs))
        self.dr = float(w_ - np.min(xs))
        top = tpos[0] - t0 * self.pad0
        bot = tpos[-1] + t1 * self.pad1
        allpos = np.vstack([top[None, :], tpos, bot[None, :]])
        alln = np.vstack([nrm[0][None, :], nrm, nrm[-1][None, :]])
        back = allpos + alln * self.dl
        front = allpos - alln * self.dr
        self.nrows = R + 2
        tex = []
        for i in range(self.nrows):
            tex.append(skia.Point(float(back[i, 0]), float(back[i, 1])))
            tex.append(skia.Point(float(front[i, 0]), float(front[i, 1])))
        self.tex = tex
        idx = []
        for i in range(self.nrows - 1):
            a, b, c2, d = 2 * i, 2 * i + 1, 2 * i + 2, 2 * i + 3
            idx += [a, b, c2, b, d, c2]
        self.idx = idx
        self.shader = spr.img.makeShader(skia.TileMode.kClamp, skia.TileMode.kClamp, LIN)
        self.paint = skia.Paint(AntiAlias=False)
        self.paint.setShader(self.shader)
        self.rest_len = float(slen.sum())

    def draw(self, c, pts, alpha=1.0, cf=None):
        n = self.n
        Pe = np.empty((n + 3, 2))
        Pe[1:n + 2] = pts
        Pe[0] = 2 * Pe[1] - Pe[2]
        Pe[n + 2] = 2 * Pe[n + 1] - Pe[n]
        pos = self.Wm @ Pe
        tan = self.Dm @ Pe
        tl = np.sqrt(tan[:, 0] ** 2 + tan[:, 1] ** 2) + 1e-9
        tx = tan[:, 0] / tl
        ty = tan[:, 1] / tl
        px, py = pos[:, 0], pos[:, 1]
        # pad satırları: üst/alt uzantı
        bxs = np.concatenate(([px[0] - tx[0] * self.pad0], px, [px[-1] + tx[-1] * self.pad1]))
        bys = np.concatenate(([py[0] - ty[0] * self.pad0], py, [py[-1] + ty[-1] * self.pad1]))
        ntx = np.concatenate(([tx[0]], tx, [tx[-1]]))
        nty = np.concatenate(([ty[0]], ty, [ty[-1]]))
        nx, ny = -nty, ntx
        bx = (bxs + nx * self.dl).tolist()
        by = (bys + ny * self.dl).tolist()
        fx = (bxs - nx * self.dr).tolist()
        fy = (bys - ny * self.dr).tolist()
        P_ = skia.Point
        verts = []
        for i in range(self.nrows):
            verts.append(P_(bx[i], by[i]))
            verts.append(P_(fx[i], fy[i]))
        vt = skia.Vertices.MakeCopy(skia.Vertices.kTriangles_VertexMode, verts, self.tex, None, self.idx)
        if cf is None:
            p = self.paint
        else:
            p = skia.Paint(AntiAlias=False)
            p.setShader(self.shader)
            p.setColorFilter(cf)
        p.setAlphaf(alpha)
        c.drawVertices(vt, p)


class Strips:
    """Sprite'ı yatay şeritlere böler; her şerit kare başına (dx, dy, sol/sağ kenar ötelemesi) ile çizilir — yalnız öteleme/ölçek olduğundan
    döndürmeli çizimden ≈5× hızlıdır (kumaş: giysi, pelerin, bayrak). Kesme çizgileri piksele oturur: dikiş görünmez."""
    __slots__ = ("img", "ox", "oy", "w", "h", "r0", "r1", "n", "ycen", "srcs", "paint", "wid")

    def __init__(self, spr, y0, y1, step):
        """y0,y1: figür koordinatı aralığı; step: şerit yüksekliği (px)."""
        self.img, self.ox, self.oy, self.w, self.h = spr.img, spr.ox, spr.oy, spr.w, spr.h
        a = int(max(0, math.floor(spr.oy + y0)))
        b = int(min(spr.h, math.ceil(spr.oy + y1)))
        n = max(2, int(round((b - a) / float(step))))
        edges = np.linspace(a, b, n + 1).round().astype(int)
        self.r0 = edges[:-1]
        self.r1 = edges[1:]
        self.n = n
        self.ycen = ((self.r0 + self.r1) * 0.5 - spr.oy)            # figür koordinatı
        self.srcs = [skia.Rect.MakeLTRB(0, int(self.r0[i]), spr.w, int(self.r1[i])) for i in range(n)]
        self.paint = skia.Paint(AntiAlias=False)

    def draw(self, c, dx, dy, exl, exr, alpha=1.0, cf=None):
        if cf is None:
            pt = self.paint
        else:
            pt = skia.Paint(AntiAlias=False)
            pt.setColorFilter(cf)
        pt.setAlphaf(alpha)
        ox, oy, w = self.ox, self.oy, self.w
        r0, r1 = self.r0.tolist(), self.r1.tolist()
        dxl, dyl = dx.tolist(), dy.tolist()
        el, er = exl.tolist(), exr.tolist()
        R_ = skia.Rect.MakeLTRB
        img = self.img
        srcs = self.srcs
        for i in range(self.n):
            c.drawImageRect(img, srcs[i], R_(-ox + dxl[i] + el[i], r0[i] - oy + dyl[i], -ox + w + dxl[i] + er[i], r1[i] - oy + dyl[i] + 0.6), LIN, pt)


# ═════════════════════════════ renk / kostüm şablonları ═════════════════════════════
SKINS = ["#E7C4A0", "#DDB48C", "#D3A57C", "#EBCBA6", "#C99A70", "#E2BD97"]
ROBES = ["#A8321E", "#233C8C", "#2E7A5A", "#7A2E56", "#C79A3C", "#1F5A7A", "#8A3A1E", "#5A3A8A", "#B8553A", "#3F6E52"]
DARKS = ["#2A1F18", "#34261C", "#1E2438", "#3A2A24"]
HOSES = ["#233C8C", "#A8321E", "#2E7A5A", "#7A2E56", "#D9CFAF", "#C79A3C", "#1F5A7A"]
HAIRS = ["#5A3A22", "#2A1A10", "#B8862A", "#8A8A82", "#7A4A24", "#3A261A"]
PATS = ["diamond", "fleur", "dots", "quatrefoil", "stripe", "pomegranate"]
GOLD = "#E0B84E"

# body: short | mid | long | woman ; hem: etek kenarı (h oranı, −0.012 = yer)
TEMPL = dict(
    tuccar=dict(body="mid", hem=-0.17, robes=["#233C8C", "#8E3342", "#2E6A4F", "#B8553A", "#1F5A7A"], hats=["mazzocchio", "mazzocchio", "flatcap", "beret"], beard=[None, "short", None, "stache"], pat=0.55, stride=1.0, fur=False, purse=True),
    banker=dict(body="long", hem=-0.04, robes=["#6A1E24", "#1E2438", "#233C8C", "#34261C"], hats=["scholar", "flatcap", "scholar"], beard=[None, "short", None], pat=0.0, stride=0.80, fur=True, purse=False),
    rahip=dict(body="long", hem=-0.012, robes=["#2A1F18", "#34261C", "#1E2438"], hats=["biretta", "biretta", "coif"], beard=[None], pat=0.0, stride=0.74, fur=False, trim="#EDE4CC", surplice=True),
    kardinal=dict(body="long", hem=-0.012, robes=["#A8321E", "#B33620", "#9C2A1C"], hats=["galero", "barrete_k"], beard=[None, "short", None], pat=0.0, stride=0.74, fur=False, trim="#EDE4CC", surplice=True),
    papa=dict(body="long", hem=-0.012, robes=["#EDE4CC"], hats=["tiara"], beard=[None, "short"], pat=0.0, stride=0.68, fur=False, trim="#E0B84E", mozzetta="#A8321E"),
    kesis=dict(body="long", hem=-0.012, robes=["#E8E0C8"], hats=["cowl"], beard=[None], pat=0.0, stride=0.82, fur=False, cloak="#1E1A18", nose=1.30, aging="o"),
    soylu=dict(body="long", hem=-0.040, robes=ROBES, hats=["mazzocchio", "mazzocchio", "tall", "beret"], beard=[None, "short", "stache", None], pat=0.85, stride=0.86, fur=False, dag=0.020, cloakp=0.45),
    soylu_f=dict(body="woman", hem=-0.012, robes=["#A8321E", "#233C8C", "#2E7A5A", "#7A2E56", "#C79A3C", "#1F5A7A", "#B8553A"], hats=["veil", "frenchhood", "tall", "coif"], beard=[None], pat=0.75, stride=0.80, fur=False, head="f", hair=["#B8862A", "#5A3A22", "#2A1A10", "#7A4A24"]),
    asker=dict(body="short", hem=-0.36, robes=["#A8321E", "#233C8C", "#2E7A5A", "#8A3A1E"], hats=["sallet", "morion", "sallet"], beard=[None, "stache", "short", None], pat=0.15, stride=1.0, fur=False, sword=True, armor=True),
    halk=dict(body="mid", hem=-0.28, robes=["#B8956A", "#8A6A48", "#9A7A4A", "#6E7F58", "#A84E34", "#7A5A3A"], hats=["woolcap", "coif", "straw", "woolcap"], beard=[None, "short", "stache", None], pat=0.0, stride=1.0, fur=False, apron=True),
    cocuk=dict(body="short", hem=-0.38, robes=["#A8321E", "#2E7A5A", "#233C8C", "#C79A3C", "#B8955A"], hats=[None, "woolcap", "flatcap"], beard=[None], pat=0.0, stride=1.0, fur=False, build="child", head="c", hair=["#5A3A22", "#2A1A10", "#B8862A", "#7A4A24"]),
    denizci=dict(body="short", hem=-0.35, robes=["#EDE4CC", "#C79A3C", "#233C8C", "#A8321E"], hats=["woolcap", "woolcap", "straw"], beard=[None, "short", "full", "stache"], pat=0.5, stride=1.05, fur=False, barefoot=True, stripe=True, sleeves="short"),
)
ALIAS = dict(katip="banker", kadin="soylu_f", muhafiz="asker", tuccar2="tuccar", baba="papa", savonarola="kesis", keşiş="kesis", kardinal2="kardinal", denizci2="denizci", cocuk2="cocuk", page="cocuk", noble="soylu",
             elder="banker", guard="asker", sailor="denizci", merchant="tuccar", priest="rahip", monk="kesis", pope="papa", cardinal="kardinal", child="cocuk", commoner="halk")
KINDS_ALL = list(TEMPL.keys())


def _pick(rs, lst):
    return lst[rs.randint(len(lst))]


def costume(kind, seed=0, **over):
    """Kostüm tarifi (hashable tuple). kind + seed → tutarlı rastgele; over: robe=, robe2=, hat=, hat_col=, hair=, skin=, hose_l=, hose_r=, pat=(tür,renk)|None, beard=, cloak=, build=, sleeves=…"""
    kind = ALIAS.get(kind, kind)
    T = TEMPL[kind]
    rs = np.random.RandomState((zlib.crc32(kind.encode()) & 0xFFFF) * 7 + int(seed) * 131 + 17)
    d = dict(kind=kind, body=T["body"], hem=T["hem"], build=T.get("build", "adult"), head=T.get("head", "m"), sleeves=T.get("sleeves", "long"), nose=T.get("nose", 1.05), aging=T.get("aging", "m"),
             stride=T.get("stride", 1.0))
    d["robe"] = _pick(rs, T["robes"])
    d["robe2"] = GOLD if kind not in ("rahip", "kesis") else "#6A5A48"
    if "trim" in T:
        d["robe2"] = T["trim"]
    hat = _pick(rs, T["hats"])
    d["hat"] = hat or "none"
    d["hat_col"] = {"galero": "#A8321E", "barrete_k": "#A8321E", "biretta": "#1E1A18", "cowl": "#1E1A18", "tiara": "#EDE4CC", "sallet": "#8A8E96", "morion": "#8A8E96", "scholar": _pick(rs, DARKS), "veil": "#EDE4CC",
                    "coif": "#EDE4CC", "straw": "#C8A45A", "woolcap": _pick(rs, ["#A8321E", "#233C8C", "#8A6A48", "#6E7F58"])}.get(hat, _pick(rs, ROBES))
    if kind == "papa":
        d["hat_col"] = "#EDE4CC"
    d["hair"] = _pick(rs, T.get("hair", HAIRS))
    d["skin"] = _pick(rs, SKINS)
    d["hose_l"], d["hose_r"] = _pick(rs, HOSES), _pick(rs, HOSES)
    if kind in ("rahip", "kardinal", "papa", "kesis", "banker", "halk", "denizci"):
        d["hose_l"] = d["hose_r"] = {"rahip": "#1E1A18", "kardinal": "#A8321E", "papa": "#EDE4CC", "kesis": "#1E1A18", "banker": "#2A1F18", "halk": "#6A5A48", "denizci": "#B8A47A"}[kind]
    d["beard"] = _pick(rs, T["beard"])
    p = T.get("pat", 0.0)
    d["pat"] = (_pick(rs, PATS), GOLD) if rs.rand() < p else None
    if T.get("stripe"):
        d["pat"] = ("stripe", "#A8321E" if d["robe"] != "#A8321E" else "#233C8C")
    d["fur"] = T.get("fur", False)
    d["purse"] = T.get("purse", False)
    d["apron"] = T.get("apron", False)
    d["sword"] = T.get("sword", False)
    d["armor"] = T.get("armor", False)
    d["dag"] = T.get("dag", 0.0)
    d["barefoot"] = T.get("barefoot", False) or (kind == "halk" and rs.rand() < 0.35)
    d["surplice"] = T.get("surplice", False)
    d["mozzetta"] = T.get("mozzetta", None)
    d["cloak"] = T.get("cloak", None)
    if T.get("cloakp") and rs.rand() < T["cloakp"]:
        d["cloak"] = _pick(rs, ROBES)
    if kind in ("soylu_f",):
        d["hair_s"] = _pick(rs, ["bun", "long", "bun"])
    d.update({k: v for k, v in over.items() if v is not None})
    if "hat" in over and over["hat"] is None:
        d["hat"] = "none"
    return tuple(sorted(d.items(), key=lambda kv: kv[0]))


# ═════════════════════════════ parça boyama ═════════════════════════════
def _add_hat3(F, kind, hx, hy, hh, rot_=0.0, back=None):
    """cilt_figs.add_hat2 + papalık tacı + hennin."""
    if kind == "tiara":
        P = []
        P.append((sp([KC(-0.40, -0.40), (-0.43, -0.78), (-0.30, -1.20), (-0.10, -1.55), (0.12, -1.58), (0.30, -1.22), (0.44, -0.78), KC(0.42, -0.40), (0.0, -0.34)], True, 0.8), 1.0, 0.0))
        for (y0, wd) in ((-0.52, 0.47), (-0.86, 0.40), (-1.18, 0.30)):
            P.append((sp([KC(-wd, y0), (0.0, y0 + 0.06), KC(wd, y0), (wd * 0.98, y0 - 0.075), (0.0, y0 - 0.02), (-wd * 0.98, y0 - 0.075)], True, 0.7), 0.0, 0.75))
        P.append((sp([KC(-0.46, -0.40), (0.0, -0.33), KC(0.46, -0.40), (0.44, -0.50), (0.0, -0.43), (-0.44, -0.50)], True, 0.6), 0.0, 0.4))
        P.append((ell(0.0, -1.64, 0.055, 0.055), 1.0, 0.55))
        P.append((poly([(-0.012, -1.68), (0.012, -1.68), (0.012, -1.82), (-0.012, -1.82)]), 1.0, 0.55))
        P.append((poly([(-0.07, -1.76), (0.07, -1.76), (0.07, -1.735), (-0.07, -1.735)]), 1.0, 0.55))
        for part in P:
            if back in (None, False):
                F.fill(place(part[0], hx, hy, hh, rot_), rim=part[1], tone=part[2])
    elif kind == "hennin":
        P = [(sp([KC(0.36, -0.30), (0.20, -0.80), (-0.10, -1.90), (-0.22, -1.96), (-0.42, -0.80), KC(-0.46, -0.28), (-0.1, -0.20)], True, 0.8), 1.0, 0.0),
             (sp([KC(-0.20, -1.90), (-0.60, -1.95), (-1.05, -1.40), (-0.95, -0.70), (-0.60, -1.20), KC(-0.30, -1.55)], True, 0.8), 0.7, 0.55, "back")]
        for part in P:
            is_back = len(part) > 3
            if back is None or back == is_back:
                F.fill(place(part[0], hx, hy, hh, rot_), rim=part[1], tone=part[2])
    else:
        FG.add_hat2(F, kind, hx, hy, hh, rot_, back)


def _hand_point():
    """İşaret eden el (el-birimi: bilek (0,0), parmaklar +x): yumruk gövde + uzamış işaret parmağı."""
    return sp([KC(0, -0.15), (0.14, -0.20), (0.30, -0.22), (0.45, -0.17), (0.50, -0.30), (0.78, -0.34), (1.18, -0.32), KC(1.28, -0.28), (1.18, -0.22), (0.78, -0.20), (0.62, -0.14), (0.66, -0.02), (0.62, 0.10),
               (0.50, 0.16), (0.34, 0.20), (0.14, 0.17), KC(0, 0.14)], True, 0.9)


def _hand_spr(skin, h, kind):
    F = FG.PFig(h)
    F.col = skin
    s = 0.085 * h
    if kind == "point":
        F.fill(place(_hand_point(), 0, 0, s, 0), rim=1.0)
    elif kind == "fist":
        F.fill(K.hand_pt("fist", 0, 0, s * 0.95, 0), rim=1.0)
        F.fill(K.hand_pt("thumb_fist", 0, 0, s * 0.95, 0), rim=1.0)
    else:
        F.fill(K.hand_pt("open", 0, 0, s, 0), rim=1.0)
        F.fill(K.hand_pt("thumb", 0, 0, s, 0), rim=1.0)
    img, ox, oy = F.sprite(pad=5)
    return Spr(img, ox, oy)


@functools.lru_cache(maxsize=256)
def hand_sprite(skin, h, kind):
    return _hand_spr(skin, h, kind)


@functools.lru_cache(maxsize=256)
def shoe_sprite(color, h, barefoot=False, kind="sharp", skin="#E7C4A0"):
    F = FG.PFig(h)
    if barefoot:
        F.col = skin
        F.fill(K.shoe(-0.014 * h, 0, 0.115 * h, 0.034 * h, 1, "round"), rim=1.0)
    else:
        F.col = color
        F.fill(K.shoe(-0.014 * h, 0, 0.14 * h, 0.036 * h, 1, kind), rim=1.0)
    img, ox, oy = F.sprite(pad=5)
    return Spr(img, ox, oy)


class Kit:
    """Bir kostümün (spec + bake_h) boyalı parçaları + iskelet ölçüleri (px, bake_h'ye göre)."""
    pass


def _dims(spec, h):
    d = dict(spec)
    child = d["build"] == "child"
    cs = 0.80 if child else 1.0
    hh_scale = 1.30 if child else 1.0
    hb = h * cs
    B = dict(
        hip=(0.0, -0.43 * hb), sho=(0.0, -0.70 * hb), neck=(0.002 * hb, -0.752 * hb), head=(0.022 * hb, -0.84 * hb), hh=0.115 * hb * hh_scale,
        ua=0.150 * hb, fa=0.135 * hb, th=0.205 * hb, sh=0.190 * hb, ah=0.035 * hb, hb=hb, h=h, hand=0.085 * hb)
    return B


def _paint_head(spec, h, B):
    d = dict(spec)
    F = FG.PFig(h)
    hb = B["hb"]
    hx, hy = B["head"]
    hh = B["hh"]
    kind = d["head"]
    F.col = d["skin"]
    nx, ny = B["neck"]
    F.fill(limb([(hx - 0.010 * hb, hy + 0.04 * hb), (nx - 0.010 * hb, ny + 0.012 * hb)], [0.062 * hb, 0.082 * hb], cap0=0, cap1=0), rim=0.9)
    hat = d["hat"]
    hat_on = hat not in ("none", None)
    if hat_on:
        F.col = d["hat_col"]
        _add_hat3(F, hat, hx, hy, hh, 0, back=True)
    hair_k = d.get("hair_s") or ("long" if kind in ("m",) else ("bob" if kind in ("c",) else "bun"))
    if kind == "m" and d["kind"] in ("halk", "asker", "denizci"):
        hair_k = "bob"
    if d["hair"] and hat not in ("cowl",) and not (hat == "tiara"):
        F.col = d["hair"]
        F.fill(place(FP.hair_path(hair_k), hx, hy, hh, 0), rim=1.0)
    F.col = d["skin"]
    F.fill(place(K.head_path(kind if kind != "m" else d["aging"], nose=d["nose"]), hx, hy, hh, 0), rim=1.0)
    # göz + kaş (küçük ama canlandırır)
    if hh > 11:
        F.col = INK
        F.fill(place(ell(0.215, -0.045, 0.034, 0.024, -8), hx, hy, hh, 0), rim=0.0, tone=0.2, alpha=0.9, bound=False)
        F.fill(place(lens((0.17, -0.115), (0.32, -0.105), 0.016, -0.02), hx, hy, hh, 0), rim=0.0, tone=0.2, alpha=0.55, bound=False)
    if kind == "c" and not hat_on:
        F.col = d["hair"]
        F.fill(place(sp([KC(0.36, -0.20), (0.34, -0.42), (0.18, -0.52), (-0.10, -0.54), (-0.36, -0.42), (-0.46, -0.16), (-0.30, -0.12), (-0.18, -0.30), (0.05, -0.40), (0.26, -0.30)], True, 0.8), hx, hy, hh, 0), rim=1.0)
    if d["beard"]:
        F.col = d["hair"] if d["hair"] else "#5A3A22"
        F.fill(place(K.beard_path(d["beard"]), hx, hy, hh, 0), rim=0.9)
    if hat_on:
        F.col = d["hat_col"]
        _add_hat3(F, hat, hx, hy, hh, 0, back=False)
        if hat in ("sallet", "morion"):
            F.gold(sp([place(sp([(-0.5, -0.2), (0.0, -0.27), (0.44, -0.2)], False), hx, hy, hh, 0).getPoint(i) for i in range(3)], False), hh * 0.04, "#D6D8DC", 0.7) if False else None
    img, ox, oy = F.sprite(pad=6)
    return Spr(img, ox, oy)


def _robe_params(spec, h, B):
    d = dict(spec)
    hb = B["hb"]
    body, hem = d["body"], d["hem"]
    if body == "short":
        P = dict(sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.095, front_sh=0.085, chest=(-0.105, 0.095, -0.66), waist=(-0.09, 0.09, -0.52), hip=(-0.115, 0.13, -0.46), hem=(-0.14, 0.17, hem), nfold=3, amp=0.010, dag=0.028)
    elif body == "mid":
        P = dict(sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.100, front_sh=0.090, chest=(-0.112, 0.098, -0.66), waist=(-0.095, 0.092, -0.51), hip=(-0.14, 0.14, -0.40), hem=(-0.18, 0.19, hem), nfold=4, amp=0.008, dag=0.0)
    elif body == "woman":
        P = dict(sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.090, front_sh=0.085, chest=(-0.105, 0.112, -0.665), waist=(-0.082, 0.085, -0.535), hip=(-0.16, 0.16, -0.30), hem=(-0.235, 0.225, hem), nfold=5, amp=0.008, dag=0.0, wave_b=0.014, wave_f=0.012)
    else:   # long
        P = dict(sh_y=-0.755, nb=(-0.04, 0.05), back_sh=-0.105, front_sh=0.095, chest=(-0.115, 0.10, -0.66), waist=(-0.10, 0.095, -0.50), hip=(-0.15, 0.15, -0.30), hem=(-0.215, 0.21, hem), nfold=4, amp=0.008, dag=d.get("dag", 0.0), wave_b=0.01, wave_f=0.01)
    return P


def _paint_robe(spec, h, B):
    """Tüm giysi (omuz→etek) tek PFig; sonra gövde/etek olarak dilimlenir."""
    d = dict(spec)
    hb = B["hb"]
    F = FG.PFig(h)
    P = _robe_params(spec, h, B)
    F.col = d["robe"]
    if d["kind"] == "kesis":
        F.col = d["robe"]
    pat = d["pat"]
    F.pat = (pat[0], pat[1], 0.75) if pat else None
    F.fill(FP.robe_path(hb, **P), rim=1.0)
    F.pat = None
    waist_y = P["waist"][2]
    hem_y = P["hem"][2]
    # kıvrımlar
    if d["body"] in ("long", "woman", "mid"):
        FP.robe_folds(F, hb, -0.065, 0.065, waist_y + 0.02, hem_y - 0.03 if d["body"] != "mid" else hem_y - 0.01, 4, 0.0075, seed=3)
    # etek kenarı altın / şerit
    robe2 = d["robe2"]
    if d["body"] != "short":
        hw = P["hem"]
        F.gold(sp([(hw[0] * 0.92 * hb, (hem_y - 0.012) * hb), (hw[0] * 0.40 * hb, (hem_y - 0.004) * hb), (0, (hem_y - 0.012) * hb), (hw[1] * 0.40 * hb, (hem_y - 0.004) * hb), (hw[1] * 0.92 * hb, (hem_y - 0.012) * hb)], False), hb * 0.0055, robe2, 0.95)
    # kürk yaka / hırka (banker)
    if d["fur"]:
        F.col = "#8A7A66"
        F.fill(K.fur_collar(0.0 * hb, -0.745 * hb, 0.30 * hb, 0.060 * hb, tuft=7), rim=0.9)
        # etek altı kürk şeridi
        F.col = "#8A7A66"
        F.fill(FP.fur_band([(-0.19 * hb, (hem_y - 0.03) * hb), (0.0, (hem_y - 0.034) * hb), (0.19 * hb, (hem_y - 0.03) * hb)], 0.035 * hb, 0.016 * hb, side=1, seed=5), rim=0.9)
    # mozzetta (papa)
    if d["mozzetta"]:
        F.col = d["mozzetta"]
        F.fill(sp([KC(-0.115 * hb, -0.742 * hb), (-0.125 * hb, -0.65 * hb), (-0.10 * hb, -0.57 * hb), (0.0, -0.545 * hb), (0.10 * hb, -0.57 * hb), (0.125 * hb, -0.65 * hb), KC(0.105 * hb, -0.742 * hb), (0.0, -0.76 * hb)], True, 0.8), rim=1.0)
        F.gold(sp([(-0.10 * hb, -0.575 * hb), (0.0, -0.548 * hb), (0.10 * hb, -0.575 * hb)], False), hb * 0.005, "#EDE4CC", 0.95)
    if d["surplice"]:
        # beyaz rochet/surplice: etek altından kısa dantel bandı + omuz
        F.col = "#EDE4CC"
        yb = max(hem_y - 0.115, waist_y + 0.05)
        hw = P["hem"]
        F.fill(sp([KC(hw[0] * 0.95 * hb, (hem_y - 0.005) * hb), (hw[0] * 0.85 * hb, (yb + 0.05) * hb), KC(hw[0] * 0.75 * hb, yb * hb), (0.0, (yb - 0.01) * hb), KC(hw[1] * 0.75 * hb, yb * hb), (hw[1] * 0.85 * hb, (yb + 0.05) * hb), KC(hw[1] * 0.95 * hb, (hem_y - 0.005) * hb),
                      (0.0, (hem_y - 0.012) * hb)], True, 0.7), rim=0.9)
        for i in range(10):
            xx = lerp(hw[0] * 0.9, hw[1] * 0.9, i / 9.0) * hb
            F.fill(poly([(xx - 0.007 * hb, (hem_y - 0.007) * hb), (xx, (hem_y - 0.034) * hb), (xx + 0.007 * hb, (hem_y - 0.007) * hb)]), rim=0.0, tone=0.0, alpha=0.4, bound=False)
    # önlük (halk)
    if d["apron"]:
        F.col = "#E8E0C8"
        F.fill(sp([KC(0.0, (waist_y + 0.01) * hb), (0.085 * hb, (waist_y + 0.02) * hb), (0.115 * hb, (hem_y + 0.05) * hb), KC(0.10 * hb, (hem_y - 0.01) * hb), (0.0, (hem_y - 0.02) * hb), (-0.02 * hb, (hem_y + 0.08) * hb)], True, 0.7), rim=0.9, tone=0.1)
    # kemer
    wb = P["waist"]
    F.col = robe2 if d["kind"] not in ("rahip", "kesis") else "#6A5A48"
    if d["kind"] == "kesis":
        F.col = "#7A6A50"
    if d["kind"] == "papa":
        F.col = "#E0B84E"
    F.fill(poly([(wb[0] * hb, (wb[2] - 0.019) * hb), (wb[1] * hb, (wb[2] - 0.019) * hb), (wb[1] * hb, (wb[2] + 0.019) * hb), (wb[0] * hb, (wb[2] + 0.019) * hb)]), rim=1.0, bound=False)
    # kesenin kemerden sarkan çantası
    if d["purse"]:
        F.col = "#6A4A2C"
        F.fill(sp([KC(0.040 * hb, (wb[2] + 0.015) * hb), (0.085 * hb, (wb[2] + 0.04) * hb), (0.085 * hb, (wb[2] + 0.095) * hb), (0.04 * hb, (wb[2] + 0.10) * hb), KC(0.018 * hb, (wb[2] + 0.04) * hb)], True, 0.8), rim=1.0)
    # kılıç kını (asker): beline asılı, arkaya sarkar; kabze önde
    if d["sword"]:
        F.col = "#3A2A1C"
        F.fill(K.bar(-0.045 * hb, (wb[2] + 0.02) * hb, -0.145 * hb, (wb[2] + 0.235) * hb, 0.032 * hb, 0.022 * hb), rim=0.9)
        F.col = "#D6B040"
        F.fill(K.bar(-0.14 * hb, (wb[2] + 0.222) * hb, -0.148 * hb, (wb[2] + 0.248) * hb, 0.026 * hb, 0.02 * hb), rim=0.9)
        F.col = "#7A5A2A"
        F.fill(K.bar(-0.040 * hb, (wb[2] + 0.005) * hb, -0.028 * hb, (wb[2] - 0.055) * hb, 0.020 * hb, 0.016 * hb), rim=0.9)
        F.fill(K.bar(-0.062 * hb, (wb[2] - 0.012) * hb, -0.010 * hb, (wb[2] - 0.012) * hb, 0.014 * hb, 0.014 * hb), rim=0.9)
    if d["armor"]:
        # göğüs: palle işlemeli tabard şeridi (Medici muhafızı)
        F.col = "#E0B84E"
        for k in range(3):
            F.fill(ell(0.0 + 0.0 * hb, (-0.69 + 0.045 * k) * hb, 0.016 * hb, 0.016 * hb), rim=0.0, tone=0.0, alpha=0.9, bound=False)
    return F, P


def _slice(spr_full, y_top, y_bot):
    """Sprite'tan [y_top, y_bot] (figür koordinatı) yatay dilim → Spr (ox,oy ayarlı)."""
    top = int(max(0, math.floor(spr_full.oy + y_top)))
    bot = int(min(spr_full.h, math.ceil(spr_full.oy + y_bot)))
    sub = spr_full.img.makeSubset(skia.IRect.MakeLTRB(0, top, spr_full.w, bot))
    return Spr(sub, spr_full.ox, spr_full.oy - top)


def _paint_arm(spec, h, B, far):
    d = dict(spec)
    hb = B["hb"]
    F = FG.PFig(h)
    sx, sy = 0.0, B["sho"][1]
    ex, ey = 0.0, sy + B["ua"]
    wx, wy = 0.0, ey + B["fa"]
    col = d["robe"] if d["kind"] != "kesis" else d["cloak"] or "#1E1A18"
    if d["kind"] == "papa":
        col = "#EDE4CC"
    if d["kind"] == "halk" and d["sleeves"] == "long":
        col = d["robe"]
    shade = 0.18 if far else 0.0
    sc = mix(col, "#2A1A0C", shade)
    if d["sleeves"] == "short":
        # kısa kollu: gövde renginde üst kol + çıplak ön kol
        F.col = mix(d["skin"], "#2A1A0C", shade)
        F.fill(limb([(sx, ey - 0.03 * hb), (ex, (ey + wy) / 2), (wx, wy)], [0.058 * hb, 0.052 * hb, 0.046 * hb], cap0=0.3, cap1=0.2), rim=0.9)
        F.col = sc
        pat = d["pat"]
        F.pat = (pat[0], pat[1], 0.7) if pat else None
        F.fill(limb([(sx, sy), (sx, sy + 0.05 * hb), (ex, ey + 0.02 * hb)], [0.094 * hb, 0.09 * hb, 0.08 * hb], cap0=0.5, cap1=0.1), rim=1.0)
        F.pat = None
    else:
        F.col = sc
        pat = d["pat"]
        F.pat = (pat[0], pat[1], 0.7) if pat else None
        wide = 1.12 if d["kind"] in ("soylu", "soylu_f", "kardinal", "papa", "banker") else 1.0
        F.fill(limb([(sx, sy), (sx, sy + 0.5 * B["ua"]), (ex, ey), (ex, ey + 0.55 * B["fa"]), (wx, wy)], [0.105 * hb, 0.102 * hb * wide, 0.096 * hb * wide, 0.093 * hb * wide, 0.092 * hb * wide], cap0=0.5, cap1=0.0), rim=1.0 if not far else 0.6)
        F.pat = None
        F.col = d["robe2"] if d["kind"] in ("soylu", "soylu_f", "banker", "tuccar") else mix(sc, "#EDE4CC", 0.15)
        F.fill(poly([(-0.049 * hb * wide, wy - 0.022 * hb), (0.049 * hb * wide, wy - 0.022 * hb), (0.049 * hb * wide, wy + 0.002 * hb), (-0.049 * hb * wide, wy + 0.002 * hb)]), rim=0.9, bound=False)
    img, ox, oy = F.sprite(pad=4)
    spr = Spr(img, ox, oy)
    return spr, [(sx, sy), (ex, ey), (wx, wy)]


def _paint_leg(spec, h, B, far):
    d = dict(spec)
    hb = B["hb"]
    F = FG.PFig(h)
    hx, hy = B["hip"]
    kx, ky = 0.0, hy + B["th"]
    ax, ay = 0.0, ky + B["sh"]
    col = d["hose_l"] if far else d["hose_r"]
    if d["barefoot"]:
        col = d["skin"]
    col = mix(col, "#2A1A0C", 0.30 if far else 0.0)
    F.col = col
    P = [(hx, hy), (hx, hy + 0.5 * B["th"]), (kx, ky), (kx, ky + 0.35 * B["sh"]), (ax, ay)]
    F.fill(limb(P, [0.074 * hb, 0.068 * hb, 0.050 * hb, 0.056 * hb, 0.034 * hb], cap0=0.3, cap1=0.25), rim=0.8 if not far else 0.5)
    img, ox, oy = F.sprite(pad=4)
    spr = Spr(img, ox, oy)
    return spr, [(hx, hy), (kx, ky), (ax, ay)]


def _paint_cloak(spec, h, B):
    d = dict(spec)
    hb = B["hb"]
    F = FG.PFig(h)
    col = d["cloak"]
    F.col = col
    pat = d["pat"] if d["kind"] in ("soylu", "soylu_f") else None
    F.pat = (pat[0], pat[1], 0.8) if pat else None
    hem = d["hem"] if d["body"] != "short" else -0.30
    ytop = -0.755 * hb
    ybot = (hem if hem < -0.1 else -0.10) * hb
    F.fill(sp([KC(0.045 * hb, ytop), (-0.04 * hb, ytop - 0.005 * hb), (-0.12 * hb, -0.70 * hb), (-0.19 * hb, -0.48 * hb), (-0.25 * hb, -0.25 * hb), KC(-0.27 * hb, ybot), (-0.14 * hb, ybot + 0.02 * hb), (-0.03 * hb, ybot + 0.005 * hb), KC(0.02 * hb, ybot - 0.02 * hb),
               (0.045 * hb, -0.40 * hb)], True, 0.85), rim=1.0)
    F.pat = None
    F.gold(sp([(-0.25 * hb, ybot - 0.01 * hb), (-0.14 * hb, ybot + 0.015 * hb), (-0.02 * hb, ybot - 0.005 * hb)], False), hb * 0.0055, d["robe2"], 0.9)
    for x0, x1, y1 in ((-0.07, -0.13, -0.22), (-0.03, -0.065, -0.17), (-0.095, -0.17, -0.14)):
        F.crease((x0 * hb, -0.64 * hb), (x1 * hb, y1 * hb), 0.012 * hb, 0.008 * hb, hi=False)
    img, ox, oy = F.sprite(pad=5)
    return Spr(img, ox, oy), ytop, ybot


@functools.lru_cache(maxsize=160)
def build_kit(spec, h):
    """spec: costume() tuple; h: bake boyu (px)."""
    d = dict(spec)
    kit = Kit()
    kit.spec, kit.d, kit.h = spec, d, h
    B = _dims(spec, h)
    kit.B = B
    hb = B["hb"]
    # --- giysi (omuz → etek): tek sprite, kare başına şeritlerle kumaş gibi çizilir
    F, P = _paint_robe(spec, h, B)
    full = Spr(*F.sprite(pad=5))
    wy = P["waist"][2] * hb
    kit.waist_rest = (0.0, wy)
    hem_y = P["hem"][2] * hb
    kit.hem_y = hem_y
    kit.robe = Strips(full, -2.0 * h, 2.0 * h, step=max(4.0, 0.020 * hb))
    kit.torso_sp = _slice(full, -2.0 * h, B["hip"][1] + 0.075 * hb)
    kit.robe_low = Strips(full, B["hip"][1] + 0.0 * hb, 2.0 * h, step=max(4.0, 0.022 * hb))
    kit.hem_w = (P["hem"][0] * hb, P["hem"][1] * hb)
    kit.skirt_len = hem_y - B["hip"][1]
    # --- baş
    kit.head = _paint_head(spec, h, B)
    # --- kollar
    sp_a, rest_a = _paint_arm(spec, h, B, False)
    kit.arm_n = Skin(sp_a, rest_a, rows=(4, 4))
    sp_b, rest_b = _paint_arm(spec, h, B, True)
    kit.arm_f = Skin(sp_b, rest_b, rows=(4, 4))
    # --- bacaklar (yere ulaşan etek yoksa)
    kit.legs = d["body"] in ("short", "mid")
    if kit.legs:
        sp_l, rest_l = _paint_leg(spec, h, B, False)
        kit.leg_n = Skin(sp_l, rest_l, rows=(4, 4))
        sp_l2, rest_l2 = _paint_leg(spec, h, B, True)
        kit.leg_f = Skin(sp_l2, rest_l2, rows=(4, 4))
    shc = "#1E1A18" if d["kind"] in ("rahip", "kesis") else "#2C1C10"
    kit.shoe_n = shoe_sprite(shc, int(round(hb)), d["barefoot"], "sharp" if d["kind"] not in ("halk", "denizci") else "round", d["skin"])
    kit.shoe_f = kit.shoe_n
    # --- pelerin (şerit kumaş)
    kit.cloak = None
    if d["cloak"]:
        spc, ctop, cbot = _paint_cloak(spec, h, B)
        kit.cloak = Strips(spc, ctop - 4, cbot + 6, step=max(4.0, 0.024 * hb))
        kit.cloak_y = (ctop, cbot)
    # --- eller
    kit.hands = {k: hand_sprite(d["skin"], int(round(hb)), k) for k in ("open", "fist", "point")}
    return kit


# ═════════════════════════════ iskelet çözümü + figür çizimi ═════════════════════════════
class Pose:
    """Kare başına çözülmüş iskelet (bake px, figür koordinatı: ayak orijin, +x ileri, y yukarı −)."""
    __slots__ = ("hip", "tor", "head", "sho", "neck", "legs", "arms", "robe", "cloak", "props", "foot", "hands", "waist", "scale_y", "_sk", "extra", "robe_low")

    def __init__(self):
        self.props = []
        self.robe = None
        self.cloak = None
        self.robe_low = None
        self.scale_y = 1.0
        self.extra = None


def solve(kit, hip, tor, head_ang, ank_f, ank_n, fang_f, fang_n, arm_f, arm_n, hk_f="open", hk_n="open"):
    """hip: (x,y); tor: gövde dönüşü (°, + ileri eğim); ank_*: ayak bileği hedefi; arm_*: ('ik',(tx,ty)) | ('ang',(üst kol °, ön kol bükümü °)) | ('fk',(ex,ey,wx,wy))."""
    B = kit.B
    p = Pose()
    p.hip = hip
    p.tor = tor
    p.head = head_ang
    dx, dy = rot(B["sho"][0] - B["hip"][0], B["sho"][1] - B["hip"][1], tor)
    p.sho = (hip[0] + dx, hip[1] + dy)
    dx, dy = rot(B["neck"][0] - B["hip"][0], B["neck"][1] - B["hip"][1], tor)
    p.neck = (hip[0] + dx, hip[1] + dy)
    p.waist = (hip[0], hip[1])
    th, sh = B["th"], B["sh"]
    legs = []
    for ank in (ank_f, ank_n):
        kx, ky, ax, ay = ik2(hip[0], hip[1], ank[0], ank[1], th, sh, -1.0)
        legs.append(((hip[0], hip[1]), (kx, ky), (ax, ay)))
    p.legs = legs
    p.foot = (fang_f, fang_n)
    arms = []
    hands = []
    for spec, hk in ((arm_f, hk_f), (arm_n, hk_n)):
        mode, val = spec
        s = p.sho
        if mode == "ik":
            ex, ey, wx, wy = ik2(s[0], s[1], val[0], val[1], B["ua"], B["fa"], 1.0)
        elif mode == "ik-":
            ex, ey, wx, wy = ik2(s[0], s[1], val[0], val[1], B["ua"], B["fa"], -1.0)
        elif mode == "ang":
            a1 = val[0] * D2R
            ex, ey = s[0] + B["ua"] * math.sin(a1), s[1] + B["ua"] * math.cos(a1)
            a2 = (val[0] + val[1]) * D2R
            wx, wy = ex + B["fa"] * math.sin(a2), ey + B["fa"] * math.cos(a2)
        else:
            ex, ey, wx, wy = val
        arms.append(((s[0], s[1]), (ex, ey), (wx, wy)))
        hands.append(hk)
    p.arms = arms
    p.hands = hands
    return p


def finish_cloth(kit, p, T, ph=0.0, sway=0.0, lag=0.0, wave=0.0, fpush=0.0, bpush=0.0, flare=0.0, breath=0.0):
    """Giysi (ve pelerin) şerit deformasyonu: gövde eğimi (kayma), etek sallanması (sarkaç), arkaya gecikme, kumaş dalgası, ön/arka kenar itmesi."""
    B = kit.B
    hb = B["hb"]
    hx0, hy0 = B["hip"]
    y = kit.robe.ycen
    sin_t = math.sin(p.tor * D2R)
    above = y < hy0
    sh = np.where(above, (hy0 - y) * sin_t, 0.0)
    Lh = max(1.0, kit.hem_y - hy0)
    v = np.clip((y - hy0) / Lh, 0.0, 1.0)
    lat = Lh * v * np.sin((sway * (0.35 + 0.65 * v)) * D2R) - lag * v * v + wave * np.sin(ph - v * 2.4) * v
    dx = p.hip[0] - hx0 + sh + lat
    dy = np.full_like(y, p.hip[1] - hy0)
    if breath:
        dy = dy + np.where(above, -breath * hb * 0.004 * np.clip((hy0 - y) / (0.3 * hb), 0, 1), 0.0)
    v18 = v ** 1.8
    exl = -(bpush + flare) * v18 + wave * 0.9 * np.sin(ph + v * 3.0 + 1.0) * v18
    exr = (fpush + flare * 0.6) * v18 + wave * 0.7 * np.sin(ph + v * 3.0) * v18
    p.robe = (dx, dy, exl, exr)
    if abs(p.tor) > 6.0:
        y2 = kit.robe_low.ycen
        v2 = np.clip((y2 - hy0) / Lh, 0.0, 1.0)
        lat2 = Lh * v2 * np.sin((sway * (0.35 + 0.65 * v2)) * D2R) - lag * v2 * v2 + wave * np.sin(ph - v2 * 2.4) * v2
        v182 = v2 ** 1.8
        p.robe_low = (p.hip[0] - hx0 + lat2, np.full_like(y2, p.hip[1] - hy0),
                      -(bpush + flare) * v182 + wave * 0.9 * np.sin(ph + v2 * 3.0 + 1.0) * v182, (fpush + flare * 0.6) * v182 + wave * 0.7 * np.sin(ph + v2 * 3.0) * v182)
    if kit.cloak is not None:
        ctop, cbot = kit.cloak_y
        yc = kit.cloak.ycen
        u = np.clip((yc - ctop) / max(1.0, cbot - ctop), 0.0, 1.0)
        cdx = (p.sho[0] - 0.0) + sh_c(p, yc, ctop) - (lag * 1.1 + 0.02 * hb) * u ** 1.5 + 0.3 * wave * np.sin(ph * 1.3 - u * 2.0) * u + 0.2 * Lh * np.sin(sway * D2R * 0.8) * u
        cdy = np.full_like(yc, p.sho[1] - B["sho"][1])
        cexl = -(0.03 * hb + flare * 1.2) * u ** 1.5
        cexr = np.zeros_like(yc)
        p.cloak = (cdx, cdy, cexl, cexr)
    return p


def sh_c(p, yc, ctop):
    return 0.0 * yc


def draw_fig(c, kit, p, alpha=1.0, cf=None, layers=("back", "legs", "body", "head", "arms")):
    """Çözülmüş iskeleti (figür koordinatlarında) çiz. Çağıran c'ye zaten ölçek/ayna/öteleme uygulamıştır."""
    B = kit.B
    if "back" in layers:
        if kit.cloak is not None and p.cloak is not None:
            kit.cloak.draw(c, *p.cloak, alpha, cf)
        s, e, w = p.arms[0]
        kit.arm_f.draw(c, [s, e, w], alpha, cf)
        _hand(c, kit, p, 0, alpha, cf)
        for pr in p.props:
            if pr[0] == "far":
                pr[1](c)
    if "legs" in layers:
        for i, (leg, sk_, shn) in enumerate(((p.legs[0], getattr(kit, "leg_f", None), kit.shoe_f), (p.legs[1], getattr(kit, "leg_n", None), kit.shoe_n))):
            if kit.legs and sk_ is not None:
                sk_.draw(c, [leg[0], leg[1], leg[2]], alpha, cf)
            ax, ay = leg[2]
            blit(c, shn, 0.0, -B["ah"], ax, ay, p.foot[i])
    if "body" in layers and p.robe is not None:
        if p.robe_low is not None and abs(p.tor) > 6.0:
            kit.robe_low.draw(c, *p.robe_low, alpha, cf)
            bx, by = B["hip"]
            if alpha < 1.0 or cf is not None:
                pt = skia.Paint(AntiAlias=False)
                pt.setAlphaf(alpha)
                if cf is not None:
                    pt.setColorFilter(cf)
                c.save()
                c.translate(p.hip[0], p.hip[1])
                c.rotate(p.tor)
                c.drawImage(kit.torso_sp.img, -(kit.torso_sp.ox + bx), -(kit.torso_sp.oy + by), LIN, pt)
                c.restore()
            else:
                blit(c, kit.torso_sp, bx, by, p.hip[0], p.hip[1], p.tor)
        else:
            kit.robe.draw(c, *p.robe, alpha, cf)
    if "head" in layers:
        nx, ny = B["neck"]
        blit(c, kit.head, nx, ny, p.neck[0], p.neck[1], p.tor + p.head)
    if "arms" in layers:
        for pr in p.props:
            if pr[0] == "mid":
                pr[1](c)
        s, e, w = p.arms[1]
        kit.arm_n.draw(c, [s, e, w], alpha, cf)
        _hand(c, kit, p, 1, alpha, cf)
        for pr in p.props:
            if pr[0] == "near":
                pr[1](c)


def _hand(c, kit, p, i, alpha, cf):
    s, e, w = p.arms[i]
    ang = math.degrees(math.atan2(w[1] - e[1], w[0] - e[0]))
    hs = kit.hands[p.hands[i]]
    if alpha < 1.0 or cf is not None:
        pt = skia.Paint(AntiAlias=False)
        pt.setAlphaf(alpha)
        if cf is not None:
            pt.setColorFilter(cf)
        c.save()
        c.translate(w[0], w[1])
        c.rotate(ang)
        c.drawImage(hs.img, -hs.ox, -hs.oy, LIN, pt)
        c.restore()
    else:
        blit(c, hs, 0.0, 0.0, w[0], w[1], ang)


# ═════════════════════════════ yürüyüş / koşu / bekleme ═════════════════════════════
def _smin(vals, k):
    m = min(vals)
    return m - math.log(sum(math.exp(-k * (v - m)) for v in vals)) / k


def _foot(u, beta, A, lift, toe):
    """Ayak yörüngesi (gövdeye göre x, yükseklik y ≥ 0, açı°, duruş?): u∈[0,1): duruş [0,beta), salınım [beta,1)."""
    if u < beta:
        k = u / beta
        x = A * (1 - 2 * k)
        ang = -10.0 * (1 - ease(k / 0.16)) + toe * ease((k - 0.62) / 0.38)
        return x, 0.0, ang, True
    k = (u - beta) / (1 - beta)
    x = -A + 2 * A * ease5(k)
    y = lift * math.sin(math.pi * k) ** 0.85
    ang = lerp(toe, -12.0, ease(min(1.0, k * 1.35))) if k < 0.85 else lerp(-12.0, -10.0, (k - 0.85) / 0.15)
    return x, y, ang, False


def gait(kit, T, v, phase=0.0, run=False, stride=1.0, pace=1.0):
    """Zemine göre hız v (bake px/sn) için yürüyüş/koşu pozu (ayak kaymaz). Dönüş: Pose (kol sallanması dâhil)."""
    B = kit.B
    hb = B["hb"]
    vh = v / hb
    if run:
        s_len = hb * clamp(0.62 * (vh / 1.4) ** 0.5, 0.25, 0.80)
        beta, lift, toe = 0.34, 0.10 * hb, 30.0
    else:
        s_len = hb * clamp(0.43 * (max(vh, 1e-3) / 0.8) ** 0.4 * stride, 0.09, 0.52)
        beta = 0.62
        lift = 0.050 * hb * (0.6 + 0.4 * min(1.0, vh / 0.5))
        toe = 24.0
    cadence = v / s_len * pace
    f_cyc = cadence / 2.0
    u_n = (T * f_cyc + phase) % 1.0
    u_f = (u_n + 0.5) % 1.0
    A = s_len * beta
    ah = B["ah"]
    Lm = 0.985 * (B["th"] + B["sh"])
    feet = [_foot(u_f, beta, A, lift, toe), _foot(u_n, beta, A, lift, toe)]

    def hip_h(u_a, u_b):
        hs = []
        for uu in (u_a, u_b):
            fx, fy, fa, st = _foot(uu, beta, A, lift, toe)
            if st:
                hs.append(math.sqrt(max(Lm * Lm - fx * fx, (0.6 * Lm) ** 2)))
        if hs:
            return _smin(hs, 40.0 / hb) if len(hs) > 1 else hs[0]
        return Lm * 0.995 + (0.045 * hb if run else 0.0)
    if run:
        Hh = sum(hip_h((u_f + d) % 1.0, (u_n + d) % 1.0) for d in (-0.06, -0.03, 0.0, 0.03, 0.06)) / 5.0
    else:
        Hh = 0.5 * hip_h(u_f, u_n) + 0.5 * hip_h((u_f + 0.015) % 1.0, (u_n + 0.015) % 1.0)
    hip = (0.0, -(ah + Hh))
    ph2 = 2 * math.pi * 2 * u_n
    lean0 = (2.0 + 6.0 * clamp(vh / 1.5)) if not run else 11.0
    tor = lean0 + 1.1 * math.sin(ph2 + 0.6) * (1.6 if run else 1.0)
    head_ang = -0.55 * (tor - lean0) - lean0 * 0.35 + 0.8 * math.sin(ph2 + 1.3)
    ank, fang = [], []
    for (fx, fy, fa, st) in feet:
        ank.append((hip[0] + fx + 0.012 * hb, -(ah + fy) - (0.020 * hb * max(0.0, math.sin(max(0.0, fa) * D2R)) if st else 0.0)))
        fang.append(fa)
    Aa = clamp(10.0 + 26.0 * clamp(s_len / (0.43 * hb)), 8.0, 34.0) * (stride ** 0.5) * (1.7 if run else 1.0)
    Aa *= 0.75 if kit.d["body"] in ("long", "woman") else 1.0
    th_n = -Aa * math.cos(2 * math.pi * u_n)
    th_f = Aa * math.cos(2 * math.pi * u_n)
    fl = 85.0 if run else 14.0
    ka_n = fl + (0 if run else 20.0 * max(0.0, th_n / Aa))
    ka_f = fl + (0 if run else 20.0 * max(0.0, th_f / Aa))
    p = solve(kit, hip, tor, head_ang, ank[0], ank[1], fang[0], fang[1], ("ang", (th_f, ka_f)), ("ang", (th_n, ka_n)))
    aF = max(ank[0][0], ank[1][0]) - hip[0]
    aB = hip[0] - min(ank[0][0], ank[1][0])
    sway = -2.5 * math.sin(ph2 + 0.2) * (v / hb) * 1.3 - (7.0 if run else 0.0) - 1.6 * vh
    p._sk = (sway, aF, aB, 0.0)
    return p


def stand(kit, T, phase=0.0, arms=None, tor_add=0.0, head_add=0.0, hip_add=(0.0, 0.0), feet=None, cm=0.0):
    """Bekleme pozu: nefes, ağırlık aktarımı, kol sarkması, baş eğimi. arms: sho → (arm_f, arm_n, hk_f, hk_n) geri çağrımı (jest/eylem);
    feet: (ank_f, ank_n, fang_f, fang_n) ayak geçersiz kılma; tor_add/head_add: ek dönüş (°); hip_add: pelvis ötelemesi (px)."""
    B = kit.B
    hb = B["hb"]
    ah = B["ah"]
    Lm = 0.985 * (B["th"] + B["sh"])
    ph = phase * 6.283
    sw = math.sin(T * 0.62 + ph)
    fx_n, fx_f = 0.040 * hb, -0.034 * hb
    hip = (0.012 * hb * sw + hip_add[0], -(ah + Lm) + 0.004 * hb * abs(sw) + hip_add[1])
    breath = math.sin(T * 1.9 + ph)
    tor = 0.8 * math.sin(T * 0.62 + ph + 0.6) + 0.2 * breath + tor_add
    head = 1.2 * math.sin(T * 0.43 + ph * 1.7) + 0.5 * math.sin(T * 1.9 + ph) + head_add
    dr = 0.010 * hb
    th = 0.272 * hb
    dxs, dys = rot(B["sho"][0] - B["hip"][0], B["sho"][1] - B["hip"][1], tor)
    sho = (hip[0] + dxs, hip[1] + dys)
    if arms is None:
        arm_f = ("ik", (sho[0] - 0.006 * hb + dr * math.sin(T * 0.7 + ph + 1.0), sho[1] + th - 0.004 * hb + 0.004 * hb * breath))
        arm_n = ("ik", (sho[0] + 0.036 * hb + dr * math.sin(T * 0.8 + ph), sho[1] + th + 0.004 * hb * breath))
        hk_f = hk_n = "open"
    else:
        arm_f, arm_n, hk_f, hk_n = arms(sho)
    if feet is None:
        ank_f, ank_n, fa_f, fa_n = (fx_f, -ah), (fx_n, -ah), 0.0, 0.0
    else:
        ank_f, ank_n, fa_f, fa_n = feet
    p = solve(kit, hip, tor, head, ank_f, ank_n, fa_f, fa_n, arm_f, arm_n, hk_f, hk_n)
    p._sk = (1.2 * math.sin(T * 0.62 + ph + 1.2), 0.0, 0.0, breath)
    return p


def idle(kit, T, phase=0.0, mood=0.0):
    return stand(kit, T, phase)


def cloth_for(kit, p, T, ph=0.0, lag=0.0, wave=0.0):
    """gait/idle çıktısına kumaş (giysi + pelerin) deformasyonunu uygula."""
    sway, aF, aB, breath = p._sk
    hb = kit.B["hb"]
    long_ = kit.d["body"] in ("long", "woman", "mid")
    k = 0.30 if long_ else 0.12
    return finish_cloth(kit, p, T, ph=T * 3.1 + ph, sway=sway, lag=lag, wave=wave * hb * 0.5 + hb * 0.004, fpush=max(0.0, aF) * k * (1.6 if kit.d["body"] != "short" else 0.9),
                        bpush=max(0.0, aB) * k * 0.9, flare=hb * 0.004, breath=breath)


# ═════════════════════════════ ekrana çizim (genel kapı) ═════════════════════════════
BAKE_H = [40, 48, 56, 64, 72, 84, 96, 110, 128, 148, 170, 196, 224, 256, 292, 332, 380, 436, 500]
_COS = {}


def _bake_for(h):
    for b in BAKE_H:
        if h <= b * 1.06:
            return b
    return BAKE_H[-1]


SCALE_HINT = 1.0          # bağlam ölçeği (kamera zumu): sprite pişirme boyu h·SCALE_HINT'e göre seçilir (zumda keskin kalır)


def set_scale_hint(z):
    global SCALE_HINT
    SCALE_HINT = float(z)


def kit_for(kind, seed, h, **stil):
    key = (kind, seed, tuple(sorted(stil.items(), key=lambda kv: kv[0])) if stil else ())
    spec = _COS.get(key)
    if spec is None:
        spec = _COS[key] = costume(kind, seed, **stil)
    bh = _bake_for(h * SCALE_HINT)
    return build_kit(spec, bh), bh


def place_fig(c, x, y, h, bake_h, dirn=1):
    s = h / bake_h
    c.translate(x, y)
    c.scale(dirn * s, s)


def _draw_pose(f, kit, bh, p, x, y, h, dirn, alpha=1.0, cf=None, layers=None, extra=None):
    c = f.c
    c.save()
    place_fig(c, x, y, h, bh, dirn)
    if layers is None:
        draw_fig(c, kit, p, alpha, cf)
    else:
        draw_fig(c, kit, p, alpha, cf, layers)
    if extra is not None:
        extra(c, p, kit)
    c.restore()


def walker(f, kind, x, y, h, t, speed=90.0, dir=1, phase=0.0, seed=0, alpha=1.0, run=False, cf=None, layers=None, prop=None, flag=None, extra=None, **stil):
    """Tek yürüyen figür. x,y = ayak noktası (ekran); h nominal boy; speed = zemine göre px/sn (≈0 → bekleme); dir=±1; phase 0..1.
    prop: staff | crosier | spear | halberd | pole (sancak: flag=(device,w,h,c1,c2)) | book | cross | torch | sack | basket."""
    kit, bh = kit_for(kind, seed, h, **stil)
    s = h / bh
    v = abs(speed) / s
    if v < 2.0:
        p = stand(kit, t, phase)
    else:
        p = gait(kit, t, v, phase, run=run, stride=kit.d.get("stride", 1.0))
    if prop:
        attach_prop(kit, p, prop, t, "near", flag=flag, v=v)
    cloth_for(kit, p, t, phase * 6.28, lag=min(v * 0.06, 0.22 * bh) * (1.5 if run else 1.0), wave=0.0)
    _draw_pose(f, kit, bh, p, x, y, h, dir, alpha, cf, layers, extra)
    return p


# ═════════════════════════════ aksesuarlar (el = orijin; −y yukarı) ═════════════════════════════
def ramp(T, t0, d):
    return ease((T - t0) / max(1e-6, d))


def pulse_(T, t0, rise, hold, fall):
    """t0'da yükselir (rise sn), hold sn bekler, fall sn'de iner → 0..1."""
    return ramp(T, t0, rise) * (1.0 - ramp(T, t0 + rise + hold, fall))


@functools.lru_cache(maxsize=256)
def prop_sprite(name, h, c1="#6A4A2C", c2=GOLD):
    F = FG.PFig(h)
    if name == "staff":
        F.col = c1
        F.fill(K.bar(0, 0.34 * h, 0, -0.80 * h, 0.017 * h, 0.013 * h), rim=0.9)
        F.col = c2
        F.fill(ell(0, -0.806 * h, 0.019 * h, 0.019 * h), rim=1.0)
    elif name == "crosier":
        F.col = c2
        F.fill(K.bar(0, 0.34 * h, 0, -0.94 * h, 0.016 * h, 0.013 * h), rim=1.0)
        for (yy, ww) in ((-0.915, 0.060), (-0.95, 0.090), (-0.985, 0.120)):
            F.fill(K.bar(-ww * h / 2, yy * h, ww * h / 2, yy * h, 0.014 * h, 0.014 * h), rim=1.0)
        F.fill(K.bar(0, -0.90 * h, 0, -1.03 * h, 0.017 * h, 0.017 * h), rim=1.0)
    elif name in ("spear", "halberd"):
        F.col = c1
        F.fill(K.bar(0, 0.38 * h, 0, -1.02 * h, 0.016 * h, 0.013 * h), rim=0.9)
        F.col = "#C8CCD2"
        if name == "spear":
            F.fill(sp([KC(0, -1.16 * h), (0.020 * h, -1.09 * h), (0.016 * h, -1.03 * h), KC(0, -1.00 * h), (-0.016 * h, -1.03 * h), (-0.020 * h, -1.09 * h)], True, 0.8), rim=1.0)
        else:
            F.fill(sp([KC(0.0, -0.99 * h), (0.07 * h, -0.995 * h), (0.105 * h, -0.95 * h), (0.07 * h, -0.90 * h), KC(0.0, -0.91 * h)], True, 0.7), rim=1.0)
            F.fill(sp([KC(0.0, -1.20 * h), (0.012 * h, -1.10 * h), KC(0.0, -1.0 * h), (-0.012 * h, -1.10 * h)], True, 0.8), rim=1.0)
    elif name == "pole":
        F.col = c1
        F.fill(K.bar(0, 0.34 * h, 0, -1.06 * h, 0.018 * h, 0.014 * h), rim=0.9)
        F.col = c2
        F.fill(ell(0, -1.08 * h, 0.022 * h, 0.022 * h), rim=1.0)
    elif name == "book":
        F.col = c1
        F.fill(poly([(-0.032 * h, -0.07 * h), (0.040 * h, -0.07 * h), (0.040 * h, 0.07 * h), (-0.032 * h, 0.07 * h)]), rim=1.0)
        F.col = c2
        F.fill(poly([(-0.032 * h, -0.07 * h), (-0.024 * h, -0.07 * h), (-0.024 * h, 0.07 * h), (-0.032 * h, 0.07 * h)]), rim=0.9, bound=False)
        F.fill(poly([(0.030 * h, -0.012 * h), (0.045 * h, -0.012 * h), (0.045 * h, 0.012 * h), (0.030 * h, 0.012 * h)]), rim=0.9, bound=False)
    elif name == "quill":
        F.col = "#F1EBDC"
        F.fill(K.feather_path(0, 0, -0.150 * h, -0.150 * h, 0.050 * h, bend=-0.025 * h), rim=1.0)
        F.col = "#2A1A0C"
        F.fill(poly([(0, 0), (0.016 * h, 0.034 * h), (-0.004 * h, 0.010 * h)]), rim=0.0, bound=True)
    elif name == "torch":
        F.col = "#4A3220"
        F.fill(K.bar(0, 0.14 * h, 0, -0.22 * h, 0.022 * h, 0.019 * h), rim=0.9)
        F.col = "#7A4A2A"
        F.fill(sp([KC(-0.026 * h, -0.20 * h), (0.0, -0.245 * h), KC(0.026 * h, -0.20 * h), (0.020 * h, -0.17 * h), (-0.020 * h, -0.17 * h)], True, 0.8), rim=1.0)
    elif name == "cross":
        F.col = c1
        F.fill(K.bar(0, 0.08 * h, 0, -0.16 * h, 0.014 * h, 0.014 * h), rim=1.0)
        F.fill(K.bar(-0.05 * h, -0.095 * h, 0.05 * h, -0.095 * h, 0.014 * h, 0.014 * h), rim=1.0)
    elif name == "sack":
        F.col = c1
        F.fill(sp([(-0.07 * h, 0.0), (-0.08 * h, -0.10 * h), (-0.04 * h, -0.19 * h), KC(0.0, -0.215 * h), (0.05 * h, -0.19 * h), (0.09 * h, -0.10 * h), (0.07 * h, 0.0), (0.0, 0.03 * h)], True, 0.9), rim=1.0)
        F.gold(sp([(-0.04 * h, -0.19 * h), (0.0, -0.17 * h), (0.05 * h, -0.19 * h)], False), h * 0.005, "#4A3220", 0.9)
    elif name == "basket":
        F.col = c1
        F.fill(sp([KC(-0.065 * h, -0.07 * h), (-0.05 * h, 0.0), (0.0, 0.02 * h), (0.05 * h, 0.0), KC(0.065 * h, -0.07 * h)], True, 0.8), rim=1.0)
        F.gold(sp([(-0.06 * h, -0.04 * h), (0.0, -0.03 * h), (0.06 * h, -0.04 * h)], False), h * 0.005, "#6A4A2C", 0.9)
        F.gold(sp([(-0.06 * h, -0.07 * h), (-0.03 * h, -0.17 * h), (0.0, -0.20 * h), (0.03 * h, -0.17 * h), (0.06 * h, -0.07 * h)], False), h * 0.007, "#6A4A2C", 0.95)
    elif name == "dagger":
        F.col = "#C8CCD2"
        F.fill(sp([KC(0, -0.20 * h), (0.013 * h, -0.12 * h), (0.017 * h, -0.045 * h), (-0.017 * h, -0.045 * h), (-0.013 * h, -0.12 * h)], True, 0.8), rim=1.0)
        F.col = "#7A5A2A"
        F.fill(K.bar(-0.035 * h, -0.040 * h, 0.035 * h, -0.040 * h, 0.014 * h, 0.014 * h), rim=1.0)
        F.fill(K.bar(0, -0.035 * h, 0, 0.04 * h, 0.018 * h, 0.018 * h), rim=1.0)
    elif name == "hammer":
        F.col = "#6A4A2C"
        F.fill(K.bar(0, 0.05 * h, 0, -0.12 * h, 0.012 * h, 0.010 * h), rim=0.9)
        F.col = "#6E7480"
        F.fill(poly([(-0.032 * h, -0.158 * h), (0.050 * h, -0.158 * h), (0.050 * h, -0.108 * h), (-0.032 * h, -0.108 * h)]), rim=1.0)
    elif name == "trowel":
        F.col = "#6A4A2C"
        F.fill(K.bar(0, 0.03 * h, 0, -0.04 * h, 0.012 * h, 0.010 * h), rim=0.9)
        F.col = "#C8CCD2"
        F.fill(poly([(0, -0.045 * h), (0.050 * h, -0.062 * h), (0.098 * h, -0.075 * h), (0.050 * h, -0.088 * h), (0.0, -0.075 * h)]), rim=1.0)
    elif name == "coin":
        F.col = "#E0B84E"
        F.fill(ell(0, 0, 0.022 * h, 0.012 * h), rim=1.0)
    else:
        raise KeyError(name)
    return Spr(*F.sprite(pad=4))


def _prop_fn(name, h, hand, ang, c1="#6A4A2C", c2=GOLD, layer="near", cf=None):
    spr = prop_sprite(name, int(round(h)), c1, c2)

    def fn(c):
        if cf is not None:
            pt = skia.Paint(AntiAlias=False)
            pt.setColorFilter(cf)
            c.save()
            c.translate(hand[0], hand[1])
            c.rotate(ang)
            c.drawImage(spr.img, -spr.ox, -spr.oy, LIN, pt)
            c.restore()
        else:
            blit(c, spr, 0.0, 0.0, hand[0], hand[1], ang)
    return (layer, fn)


class ColStrips:
    """Dikey dilimli kumaş (bayrak): sap kenarı sabit, serbest uç dalgalanır. Sprite: sol→sağ. draw(dy[], dh[]): dilim başına kayma/boy ölçeği."""
    __slots__ = ("img", "ox", "oy", "w", "h", "n", "edges", "srcs", "paint")

    def __init__(self, spr, n=14):
        self.img, self.ox, self.oy, self.w, self.h = spr.img, spr.ox, spr.oy, spr.w, spr.h
        self.n = n
        self.edges = np.linspace(0, spr.w, n + 1).round().astype(int).tolist()
        self.srcs = [skia.Rect.MakeLTRB(self.edges[i], 0, self.edges[i + 1], spr.h) for i in range(n)]
        self.paint = skia.Paint(AntiAlias=False)

    def draw(self, c, dy, dh, alpha=1.0, cf=None):
        pt = self.paint
        if cf is not None:
            pt = skia.Paint(AntiAlias=False)
            pt.setColorFilter(cf)
        pt.setAlphaf(alpha)
        R_ = skia.Rect.MakeLTRB
        e = self.edges
        for i in range(self.n):
            hh = self.h * dh[i]
            c.drawImageRect(self.img, self.srcs[i], R_(-self.ox + e[i], -self.oy + dy[i] + (self.h - hh) * 0.5, -self.ox + e[i + 1] + 0.6, -self.oy + dy[i] + (self.h - hh) * 0.5 + hh), LIN, pt)


class VStrips:
    """Dikey dilimler: gövde eğimi/sıçraması için dilim başına dikey kayma (yalnız öteleme → hızlı)."""
    __slots__ = ("img", "ox", "oy", "w", "h", "n", "edges", "srcs", "xcen", "paint")

    def __init__(self, spr, step=8.0):
        self.img, self.ox, self.oy, self.w, self.h = spr.img, spr.ox, spr.oy, spr.w, spr.h
        n = max(2, int(round(spr.w / float(step))))
        self.n = n
        self.edges = np.linspace(0, spr.w, n + 1).round().astype(int).tolist()
        self.srcs = [skia.Rect.MakeLTRB(self.edges[i], 0, self.edges[i + 1], spr.h) for i in range(n)]
        self.xcen = np.array([(self.edges[i] + self.edges[i + 1]) * 0.5 - spr.ox for i in range(n)])
        self.paint = skia.Paint(AntiAlias=False)

    def draw(self, c, dy, dx=0.0, alpha=1.0, cf=None):
        pt = self.paint
        if cf is not None:
            pt = skia.Paint(AntiAlias=False)
            pt.setColorFilter(cf)
        pt.setAlphaf(alpha)
        R_ = skia.Rect.MakeLTRB
        e = self.edges
        top = -self.oy
        bot = top + self.h
        dyl = dy.tolist()
        for i in range(self.n):
            c.drawImageRect(self.img, self.srcs[i], R_(-self.ox + e[i] + dx, top + dyl[i], -self.ox + e[i + 1] + dx + 0.6, bot + dyl[i]), LIN, pt)


@functools.lru_cache(maxsize=64)
def flag_sprite(device, w, h, c1="#E0B84E", c2="#B33620"):
    """Sancak bezi (w×h px; sol = serbest uç, sağ = sap kenarı). device: medici | lily | cross | plain | stripes."""
    F = FG.PFig(max(w, h) * 2)
    F.col = c1
    pts = [KC(0, 0), (w * 0.5, h * 0.02), KC(w, 0), KC(w, h), (w * 0.5, h * 0.98), KC(0, h)]
    if device in ("medici", "lily", "cross", "plain", "stripes"):
        # kırlangıç kuyruklu: serbest uçta çatal
        pts = [KC(0, 0), (w * 0.5, h * 0.03), KC(w, 0), KC(w, h), (w * 0.5, h * 0.97), KC(0, h), (w * 0.13, h * 0.5)]
    F.fill(poly([(p[0], p[1]) for p in pts]), rim=1.0)
    if device == "medici":
        F.col = c2
        r = h * 0.15
        for (xx, yy) in ((0.42, 0.28), (0.62, 0.28), (0.52, 0.50), (0.72, 0.50), (0.42, 0.72), (0.62, 0.72)):
            F.fill(ell(w * xx, h * yy, r * 0.78, r * 0.78), rim=1.0, bound=False)
    elif device == "lily":
        F.col = c2
        F.fill(CP_lily(w * 0.55, h * 0.50, h * 0.78), rim=0.9, bound=False)
    elif device == "cross":
        F.col = c2
        F.fill(poly([(w * 0.50, h * 0.08), (w * 0.60, h * 0.08), (w * 0.60, h * 0.92), (w * 0.50, h * 0.92)]), rim=0.9, bound=False)
        F.fill(poly([(w * 0.22, h * 0.40), (w * 0.88, h * 0.40), (w * 0.88, h * 0.52), (w * 0.22, h * 0.52)]), rim=0.9, bound=False)
    elif device == "stripes":
        F.col = c2
        for k in range(3):
            F.fill(poly([(w * (0.25 + 0.22 * k), 0), (w * (0.25 + 0.22 * k + 0.10), 0), (w * (0.25 + 0.22 * k + 0.10), h), (w * (0.25 + 0.22 * k), h)]), rim=0.0, tone=0.0, bound=False)
    F.gold(poly([(1.5, 1.5), (w - 1.5, 1.5)], False), 2.0, "#6A4A1C", 0.8)
    F.gold(poly([(1.5, h - 1.5), (w - 1.5, h - 1.5)], False), 2.0, "#6A4A1C", 0.8)
    return Spr(*F.sprite(pad=3))


def CP_lily(cx, cy, s):
    import cilt_props as CP
    return CP.lily_path(cx, cy, s)


# ═════════════════════════════ eylemler (poz üreticiler) ═════════════════════════════
def _relaxed(sho, hb, T, ph, side):
    dr = 0.010 * hb
    if side == "n":
        return ("ik", (sho[0] + 0.036 * hb + dr * math.sin(T * 0.8 + ph), sho[1] + 0.272 * hb))
    return ("ik", (sho[0] - 0.006 * hb + dr * math.sin(T * 0.7 + ph + 1.0), sho[1] + 0.268 * hb))


def act_idle(kit, T, phase=0.0, **_):
    return stand(kit, T, phase)


def act_talk(kit, T, phase=0.0, energy=1.0, **_):
    """Konuşurken jest: vurgu atımlarıyla eli öne açar, baş vurguda hafifçe eğilir."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    env = 0.55 + 0.45 * math.sin(T * 0.9 + ph)
    beat = max(0.0, math.sin(T * 3.4 + ph * 2.0 + 0.7 * math.sin(T * 0.6)))
    env2 = max(0.0, math.sin(T * 0.47 + ph + 2.0))

    def arms(sho):
        gx = sho[0] + (0.20 + 0.05 * math.sin(T * 2.0 + ph) + 0.035 * beat) * hb * (0.55 + 0.45 * energy)
        gy = sho[1] + (0.17 - 0.07 * beat + 0.025 * math.sin(T * 1.4 + ph)) * hb - 0.04 * hb * env * energy
        fx = sho[0] + (0.07 + 0.10 * env2) * hb
        fy = sho[1] + (0.26 - 0.13 * env2) * hb
        return ("ik", (fx, fy)), ("ik", (gx, gy)), "open", "open"
    return stand(kit, T, phase, arms=arms, head_add=2.4 * beat * energy, tor_add=0.8 * beat * energy)


def act_bow(kit, T, phase=0.0, t0=0.5, dur=2.2, depth=34.0, **_):
    """Selam: gövde kalçadan öne eğilir, baş uyar, el göğse gider; bekler; kalkar."""
    hb = kit.B["hb"]
    u = (T - t0) / dur
    b = ease5(clamp(u / 0.38)) * (1 - ease5(clamp((u - 0.62) / 0.38)))
    th = depth * b

    def arms(sho):
        chest = (sho[0] + 0.07 * hb, sho[1] + 0.11 * hb)
        hang = (sho[0] + 0.02 * hb, sho[1] + 0.268 * hb)
        k = ease(clamp(b * 1.6))
        return ("ik", hang), ("ik", (lerp(_relaxed(sho, hb, T, 0, "n")[1][0], chest[0], k), lerp(_relaxed(sho, hb, T, 0, "n")[1][1], chest[1], k))), "open", "open"
    return stand(kit, T, phase, arms=arms, tor_add=th, head_add=0.38 * th, hip_add=(-0.05 * hb * math.sin(th * D2R), 0.02 * hb * b))


def _kneel_feet(kit, k):
    hb = kit.B["hb"]
    ah = kit.B["ah"]
    ank_n = (lerp(0.040, 0.20, k) * hb, -ah)
    ank_f = (lerp(-0.034, -0.205, k) * hb, -ah - 0.01 * hb * k)
    return ank_f, ank_n, lerp(0.0, 168.0, ease(clamp(k * 1.2))), 0.0


def act_kneel(kit, T, phase=0.0, t0=0.5, dur=1.6, rise_at=None, pray=1.0, **_):
    """Diz çökme: pelvis iner, arka diz yere değer, ön ayak ilerler, eller göğüste kenetlenir, baş eğilir. rise_at: kalkış zamanı."""
    hb = kit.B["hb"]
    ah = kit.B["ah"]
    k = ramp(T, t0, dur)
    if rise_at is not None:
        k *= 1.0 - ramp(T, rise_at, dur)
    th = kit.B["th"]
    hip_y_stand = -(ah + 0.985 * (th + kit.B["sh"]))
    hip_y_kneel = -(th * 1.02 + 0.0)
    hip = (0.0, 0.0)
    hip_add = (-0.03 * hb * k, (hip_y_kneel - hip_y_stand) * k)
    feet = _kneel_feet(kit, k)
    bounce = 0.004 * hb * math.sin(T * 1.9 + phase * 6.28)

    def arms(sho):
        pr = ease(clamp(k * 1.4)) * pray
        tgt = (sho[0] + 0.115 * hb, sho[1] + 0.105 * hb + bounce)
        n0, f0 = _relaxed(sho, hb, T, phase * 6.28, "n"), _relaxed(sho, hb, T, phase * 6.28, "f")
        a = ("ik", (lerp(n0[1][0], tgt[0], pr), lerp(n0[1][1], tgt[1], pr)))
        b = ("ik", (lerp(f0[1][0], tgt[0] - 0.01 * hb, pr), lerp(f0[1][1], tgt[1] + 0.004 * hb, pr)))
        return b, a, "open", "open"
    p = stand(kit, T, phase, arms=arms, tor_add=-2.0 * k, head_add=10.0 * k * pray, hip_add=hip_add, feet=feet)
    p._sk = (0.0, 0.0, 0.0, p._sk[3])
    return p


def act_point(kit, T, phase=0.0, t0=0.6, dur=3.0, target=(1.0, -0.35), **_):
    """İşaret etme: kol hedef yönüne uzanır; işaret parmağı; gövde/baş hafifçe döner."""
    hb = kit.B["hb"]
    k = pulse_(T, t0, 0.55, dur, 0.55)
    ux, uy = target
    n = math.hypot(ux, uy) or 1.0
    ux, uy = ux / n, uy / n
    reach = 0.965 * (kit.B["ua"] + kit.B["fa"])

    def arms(sho):
        n0 = _relaxed(sho, hb, T, phase * 6.28, "n")
        tgt = (sho[0] + ux * reach, sho[1] + uy * reach + 0.004 * hb * math.sin(T * 2.2))
        a = ("ik", (lerp(n0[1][0], tgt[0], k), lerp(n0[1][1], tgt[1], k)))
        return _relaxed(sho, hb, T, phase * 6.28, "f"), a, "open", ("point" if k > 0.25 else "open")
    return stand(kit, T, phase, arms=arms, tor_add=3.0 * k, head_add=-6.0 * k * (1 if uy < -0.2 else -0.5))


def act_cheer(kit, T, phase=0.0, amount=1.0, hop=0.4, **_):
    """Coşku: kollar havada (Palle! Palle!), hafif sıçrama; amount 0..1 kol yüksekliği."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    k = amount
    jump = max(0.0, math.sin(T * 6.2 + ph)) ** 1.5 * hop * 0.035 * hb * k

    def arms(sho):
        w = math.sin(T * 6.2 + ph + 0.8)
        up_n = (sho[0] + (0.10 + 0.03 * w) * hb, sho[1] - (0.27 + 0.02 * w) * hb)
        up_f = (sho[0] + (0.04 - 0.03 * w) * hb, sho[1] - (0.26 - 0.02 * w) * hb)
        n0, f0 = _relaxed(sho, hb, T, ph, "n"), _relaxed(sho, hb, T, ph, "f")
        return ("ik", (lerp(f0[1][0], up_f[0], k), lerp(f0[1][1], up_f[1], k))), ("ik", (lerp(n0[1][0], up_n[0], k), lerp(n0[1][1], up_n[1], k))), "fist" if k > 0.5 else "open", "fist" if k > 0.5 else "open"
    return stand(kit, T, phase, arms=arms, hip_add=(0.0, -jump), head_add=-6.0 * k)


def act_pray(kit, T, phase=0.0, **_):
    hb = kit.B["hb"]
    ph = phase * 6.283

    def arms(sho):
        tgt = (sho[0] + 0.115 * hb, sho[1] + 0.105 * hb + 0.003 * hb * math.sin(T * 1.9 + ph))
        return ("ik", (tgt[0] - 0.01 * hb, tgt[1] + 0.004 * hb)), ("ik", tgt), "open", "open"
    return stand(kit, T, phase, arms=arms, head_add=9.0 + 2.0 * math.sin(T * 0.8 + ph), tor_add=2.0)


# ── oturan figür (yazma / sayma) ────────────────────────────────────────────
DESK_Y = -0.415         # masa üstü (hb oranı)


def _sit_base(kit, T, phase, lean, head, arms, hip_add=(0.0, 0.0)):
    B = kit.B
    hb, ah = B["hb"], B["ah"]
    ph = phase * 6.283
    breath = math.sin(T * 1.9 + ph)
    hip = (-0.03 * hb + hip_add[0], -0.305 * hb + hip_add[1])
    feet = ((0.17 * hb, -ah), (0.205 * hb, -ah), -8.0, -6.0)
    dxs, dys = rot(B["sho"][0] - B["hip"][0], B["sho"][1] - B["hip"][1], lean)
    sho = (hip[0] + dxs, hip[1] + dys)
    arm_f, arm_n, hk_f, hk_n = arms(sho)
    p = solve(kit, hip, lean + 0.3 * breath, head, feet[0], feet[1], feet[2], feet[3], arm_f, arm_n, hk_f, hk_n)
    p._sk = (0.0, 0.0, 0.0, breath)
    return p


def act_write(kit, T, phase=0.0, t0=0.0, quill=True, **_):
    """Defter yazan (oturan): satır boyunca kayan tüy kalem, mürekkep hokkasına daldırma, sayfa tutan sol el; başı ve gövdesi satırı izler."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    cyc = 7.0
    tt = (T - t0 + phase * 3.0) % cyc
    line_t = 5.1
    # satır boyunca ilerleme
    if tt < line_t:
        prog = tt / line_t
        dip = 0.0
    else:
        prog = 1.0
        dip = (tt - line_t) / (cyc - line_t)         # 0..1: hokkaya git-gel
    wx = 0.205 + 0.14 * prog                          # kalem ucu x (hb)
    scr = (0.0065 * math.sin(T * 17.0 + ph) + 0.004 * math.sin(T * 9.3)) * (1 - ease(clamp(dip * 4)))
    scry = 0.0030 * math.sin(T * 13.0)
    ink_x, ink_y = 0.44, DESK_Y - 0.02
    lift = 0.0
    if dip > 0:
        a = math.sin(math.pi * clamp(dip)) ** 0.9
        wx = lerp(wx, ink_x, ease5(clamp(dip * 1.7)) if dip < 0.5 else 1 - ease5(clamp((dip - 0.5) * 2.0)) * 0.0)
        if dip > 0.5:
            wx = lerp(ink_x, 0.205, ease5(clamp((dip - 0.55) / 0.45)))
        lift = 0.045 * a
    hx = (wx + scr) * hb
    hy = (DESK_Y - 0.004 - lift + scry) * hb

    def arms(sho):
        # sol el sayfayı tutar, satır sonunda biraz kayar
        fx, fy = 0.215 * hb, (DESK_Y - 0.003) * hb
        return ("ik", (fx, fy)), ("ik", (hx, hy)), "open", "fist"
    lean = 9.0 + 2.0 * prog
    head = 14.0 + 3.0 * math.sin(T * 0.9 + ph) - 3.0 * prog
    p = _sit_base(kit, T, phase, lean, head, arms)
    ang_q = 28.0 - 10.0 * lift / 0.045 * 0.0
    if quill:
        e_, w = p.arms[1][1], p.arms[1][2]
        fa = math.atan2(w[1] - e_[1], w[0] - e_[0])
        qx, qy = w[0] + math.cos(fa) * 0.05 * hb, w[1] + math.sin(fa) * 0.05 * hb
        p.props.append(_prop_fn("quill", hb * 0.8, (qx, qy), 4.0 + 4.0 * math.sin(T * 17.0 + ph) * (1 - clamp(dip * 4)), layer="near"))
    p.extra = dict(desk=True, ink=(ink_x * hb, ink_y * hb), prog=prog, line=int(((T - t0) // cyc)) if T > t0 else 0, wr=(hx, hy))
    return p


def act_count(kit, T, phase=0.0, t0=0.0, period=1.6, **_):
    """Para sayma (oturan): sağ el soldaki yığından bir florin alıp sağdaki sütuna istifler; sütun büyür; sol el yığını iter."""
    hb = kit.B["hb"]
    ph = phase * 6.283
    tt = ((T - t0) / period)
    n = int(tt) if tt >= 0 else 0
    u = tt - math.floor(tt) if tt >= 0 else 0.0
    xa, xb = 0.44, 0.255                              # kaynak yığın, hedef sütun (hb)
    stackh = 0.0068 * (n % 9 + 1)
    # evre: 0-.25 yığına in, .25-.4 kapan/kaldır, .4-.75 kemer, .75-.9 bırak, .9-1 geri
    if u < 0.22:
        k = ease(u / 0.22)
        hx, hy, grab = xa, DESK_Y - 0.05 * (1 - k) - 0.01, False
    elif u < 0.40:
        k = ease((u - 0.22) / 0.18)
        hx, hy, grab = xa, DESK_Y - 0.01 - 0.06 * k, k > 0.4
    elif u < 0.74:
        k = ease5((u - 0.40) / 0.34)
        hx = lerp(xa, xb, k)
        hy = DESK_Y - 0.07 - 0.04 * math.sin(math.pi * k) - 0.0 * k
        grab = True
    elif u < 0.90:
        k = ease((u - 0.74) / 0.16)
        hx = xb
        hy = lerp(DESK_Y - 0.07, DESK_Y - 0.01 - stackh, k)
        grab = k < 0.8
    else:
        k = ease((u - 0.90) / 0.10)
        hx = lerp(xb, xa, k * 0.6)
        hy = lerp(DESK_Y - 0.01 - stackh, DESK_Y - 0.05, k)
        grab = False

    def arms(sho):
        return ("ik", (0.50 * hb, (DESK_Y - 0.004) * hb)), ("ik", (hx * hb, hy * hb)), "open", ("fist" if grab else "open")
    p = _sit_base(kit, T, phase, 7.0, 12.0 + 3 * math.sin(T * 1.2 + ph), arms)
    wr = p.arms[1][2]
    p.extra = dict(desk=True, coins=dict(n=n, u=u, grab=grab, hand=(wr[0], wr[1]), xa=xa * hb, xb=xb * hb, stackh=stackh * hb), wr=(hx * hb, hy * hb))
    return p


def act_handshake(kit, T, phase=0.0, t0=0.5, M=(0.30, -0.50), lead=0.0, **_):
    """El sıkışma yarısı (iki figürden biri): hedef M (figür koordinatı, hb), ileri uzanır, 3 kez sallar, bırakır. İki figürü `handshake()` birleştirir."""
    hb = kit.B["hb"]
    k = pulse_(T, t0, 0.55, 1.45, 0.55)
    pump = 0.022 * math.sin((T - t0 - 0.5) * 2 * math.pi * 2.7) * ease(clamp((T - t0 - 0.4) / 0.2)) * k

    def arms(sho):
        tgt = ((M[0]) * hb, (M[1] + pump) * hb)
        n0 = _relaxed(sho, hb, T, phase * 6.28, "n")
        a = ("ik", (lerp(n0[1][0], tgt[0], k), lerp(n0[1][1], tgt[1], k)))
        return _relaxed(sho, hb, T, phase * 6.28, "f"), a, "open", "open"
    return stand(kit, T, phase, arms=arms, tor_add=5.0 * k, head_add=3.0 * k)


def act_threat(kit, T, phase=0.0, t0=0.4, dur=1.2, **_):
    """ŞİDDET İŞARETİ (yalnız jest): saldırgan öne atılır, kolu hançerle yukarı kalkar; gövde ileri eğik. Siluet çiziminde kullanılır."""
    hb = kit.B["hb"]
    k = ramp(T, t0, dur * 0.55) * (1 - 0.0 * ramp(T, t0 + dur * 2, 0.5))
    ah = kit.B["ah"]
    ank_n = (lerp(0.04, 0.26, k) * hb, -ah)
    ank_f = (lerp(-0.034, -0.17, k) * hb, -ah)

    def arms(sho):
        up = (sho[0] + 0.04 * hb, sho[1] - 0.285 * hb)
        tgt = (lerp(_relaxed(sho, hb, T, 0, "n")[1][0], up[0], k), lerp(_relaxed(sho, hb, T, 0, "n")[1][1], up[1], k))
        fr = (sho[0] + 0.22 * hb * k + (1 - k) * 0.0, sho[1] + 0.16 * hb)
        return ("ik", (lerp(_relaxed(sho, hb, T, 0, "f")[1][0], fr[0], k), lerp(_relaxed(sho, hb, T, 0, "f")[1][1], fr[1], k))), ("ik", tgt), "open", "fist"
    p = stand(kit, T, phase, arms=arms, tor_add=16.0 * k, head_add=-4.0 * k, hip_add=(0.04 * hb * k, 0.04 * hb * k), feet=(ank_f, ank_n, -6.0 * k, -4.0 * k))
    w = p.arms[1][2]
    p.props.append(_prop_fn("dagger", kit.B["hb"], w, -4.0 * k, layer="near"))
    return p


def _kf(u, keys):
    """Anahtar kare enterpolasyonu: keys=[(u, değer…)]; segment içinde ease. Dönüş: değer demeti."""
    for i in range(len(keys) - 1):
        a, b = keys[i], keys[i + 1]
        if u <= b[0] or i == len(keys) - 2:
            k = ease(clamp((u - a[0]) / max(1e-6, b[0] - a[0])))
            return tuple(lerp(a[j], b[j], k) for j in range(1, len(a)))
    return tuple(keys[-1][1:])


def act_work(kit, T, phase=0.0, mode="lay", period=None, high=0.0, **_):
    """Şantiye işi (kalıcı döngü). mode: lay = harç/tuğla alıp duvara yerleştirir (malalı) | strike = çekiçle keski vuruşu | haul = halat çeker (geriye yaslanır).
    high: duvar yüksekliği (−1 alçak … +1 baş üstü)."""
    hb = kit.B["hb"]
    ah = kit.B["ah"]
    if mode == "strike":
        per = period or 0.62
        u = (T / per + phase) % 1.0
        lift, tor, hx, hy, ang = _kf(u, [(0.0, 0.0, 6.0, 0.26, 0.06, 80.0), (0.58, 1.0, 2.0, 0.17, -0.20, 8.0), (0.70, 0.0, 8.0, 0.27, 0.07, 82.0), (1.0, 0.0, 6.0, 0.26, 0.06, 80.0)])

        def arms(sho):
            n = ("ik", (sho[0] + hx * hb, sho[1] + hy * hb))
            fr = ("ik", (sho[0] + 0.25 * hb, sho[1] + 0.12 * hb))
            return fr, n, "fist", "fist"
        p = stand(kit, T, phase, arms=arms, tor_add=tor, head_add=-1.5 * (1 - lift))
        w = p.arms[1][2]
        p.props.append(_prop_fn("hammer", kit.B["hb"], w, ang, layer="near"))
        return p
    if mode == "haul":
        per = period or 1.5
        u = (T / per + phase) % 1.0
        pull, = _kf(u, [(0.0, 0.0), (0.12, 0.0), (0.58, 1.0), (0.70, 1.0), (1.0, 0.0)])
        ank_n = (0.115 * hb, -ah)
        ank_f = (-0.090 * hb, -ah)

        def arms(sho):
            fx = lerp(sho[0] + 0.26 * hb, sho[0] + 0.11 * hb, pull)
            fy = lerp(sho[1] + 0.02 * hb, sho[1] + 0.27 * hb, pull)
            return ("ik", (fx - 0.02 * hb, fy - 0.03 * hb)), ("ik", (fx, fy)), "fist", "fist"
        p = stand(kit, T, phase, arms=arms, tor_add=-9.0 * pull + 3.0 * (1 - pull), head_add=3.0 * pull, hip_add=(-0.035 * hb * pull, 0.012 * hb * pull), feet=(ank_f, ank_n, 0.0, 0.0))
        w = p.arms[1][2]
        rp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.5, 0.014 * hb), Color=C("#7A6A44"), StrokeCap=skia.Paint.kRound_Cap)

        def rope(c, w=w, hb=hb, pull=pull, rp=rp):
            pa = skia.Path()
            pa.moveTo(w[0], w[1])
            pa.quadTo(w[0] + 0.30 * hb, w[1] - 0.30 * hb + 0.08 * hb * (1.0 - pull), w[0] + 0.66 * hb, w[1] - 0.86 * hb)
            c.drawPath(pa, rp)
        p.props.append(("near", rope))
        return p
    per = period or 1.8
    u = (T / per + phase) % 1.0
    hy_w = 0.07 - 0.20 * high
    px, py = 0.12, 0.45
    wx = 0.30
    hx, hy, tor, fist = _kf(u, [(0.00, wx, hy_w, 4.0, 0.0), (0.26, px, py, 15.0, 0.0), (0.34, px, py, 15.0, 1.0), (0.44, px, py - 0.06, 11.0, 1.0), (0.74, wx, hy_w, 5.0, 1.0), (0.84, wx + 0.014, hy_w + 0.012, 5.0, 1.0), (0.92, wx, hy_w, 5.0, 0.0), (1.0, wx, hy_w, 4.0, 0.0)])

    def arms(sho):
        n = ("ik", (sho[0] + hx * hb, sho[1] + hy * hb))
        fr = ("ik", (sho[0] + 0.07 * hb, sho[1] + 0.24 * hb))
        return fr, n, "open", ("fist" if fist > 0.5 else "open")
    p = stand(kit, T, phase, arms=arms, tor_add=tor, head_add=-0.3 * tor)
    w = p.arms[1][2]
    p.props.append(_prop_fn("trowel", kit.B["hb"], w, 70.0 - 40.0 * fist, layer="near"))
    return p


ACTIONS = dict(idle=act_idle, talk=act_talk, bow=act_bow, kneel=act_kneel, point=act_point, cheer=act_cheer, pray=act_pray, write=act_write, count=act_count, handshake=act_handshake, threat=act_threat, work=act_work)
STIL_KEYS = ("robe", "robe2", "hat", "hat_col", "hair", "skin", "hose_l", "hose_r", "pat", "beard", "cloak", "build", "sleeves", "nose", "body", "hem", "head", "barefoot")


def actor(f, kind, x, y, h, t, action="idle", dir=1, seed=0, phase=0.0, alpha=1.0, cf=None, extra=None, **p):
    """Eylem oynatan figür. action: idle | talk | bow | kneel | point | cheer | pray | write | count | handshake | threat.
    Parametreler (eyleme göre): t0 (başlangıç sn), dur, depth, target=(dx,dy), rise_at, energy, amount, M …  prop='staff'|'book'… ile eline aksesuar."""
    stil = {k: v for k, v in p.items() if k in STIL_KEYS}
    ap = {k: v for k, v in p.items() if k not in STIL_KEYS}
    kit, bh = kit_for(kind, seed, h, **stil)
    prop = ap.pop("prop", None)
    fn = ACTIONS[action]
    pz = fn(kit, t, phase=phase, **ap)
    if prop:
        attach_prop(kit, pz, prop, t, ap.get("prop_hand", "near"))
    sway, aF, aB, breath = pz._sk
    cloth_for(kit, pz, t, phase * 6.28, lag=0.0, wave=0.0)
    c = f.c
    c.save()
    place_fig(c, x, y, h, bh, dir)
    ex = pz.extra
    if ex and ex.get("desk"):
        draw_fig(c, kit, pz, alpha, cf, ("back", "legs", "body", "head"))
        draw_desk(c, kit, pz, t, alpha)
        draw_fig(c, kit, pz, alpha, cf, ("arms",))
        draw_desk_top(c, kit, pz, t, alpha)
    else:
        draw_fig(c, kit, pz, alpha, cf)
    if extra is not None:
        extra(c, pz, kit)
    c.restore()
    return pz


def attach_prop(kit, p, prop, T, hand="near", flag=None, v=0.0):
    """Aksesuarı el konumuna bağla (yürüyüş/bekleme)."""
    hb = kit.B["hb"]
    i = 1 if hand == "near" else 0
    s, e, w = p.arms[i]
    layer = "near" if i == 1 else "far"
    if prop in ("staff", "crosier", "spear", "halberd", "pole"):
        # kol öne uzanır, sopa dikey; sopanın ucu zemine değer
        tgt = (p.sho[0] + 0.15 * hb, p.sho[1] + 0.17 * hb)
        ex, ey, wx, wy = ik2(p.sho[0], p.sho[1], tgt[0], tgt[1], kit.B["ua"], kit.B["fa"], 1.0)
        arms = list(p.arms)
        arms[i] = ((p.sho[0], p.sho[1]), (ex, ey), (wx, wy))
        p.arms = arms
        hk = list(p.hands)
        hk[i] = "fist"
        p.hands = hk
        ang_p = 2.0 + 1.5 * math.sin(T * 1.7)
        p.props.append(_prop_fn(prop, hb, (wx, wy), ang_p, layer="mid" if i == 1 else "far"))
        if prop == "pole" and flag is not None:
            a_ = ang_p * D2R
            top = (wx + 0.98 * hb * math.sin(a_), wy - 0.98 * hb * math.cos(a_))
            p.props.append(("mid" if i == 1 else "far", _flag_fn(top, hb, T, flag, v)))
    elif prop in ("book", "cross"):
        tgt = (p.sho[0] + 0.095 * hb, p.sho[1] + 0.10 * hb)
        ex, ey, wx, wy = ik2(p.sho[0], p.sho[1], tgt[0], tgt[1], kit.B["ua"], kit.B["fa"], 1.0)
        arms = list(p.arms)
        arms[i] = ((p.sho[0], p.sho[1]), (ex, ey), (wx, wy))
        p.arms = arms
        hk = list(p.hands)
        hk[i] = "fist"
        p.hands = hk
        p.props.append(_prop_fn(prop, hb, (wx + 0.012 * hb, wy - 0.02 * hb), 0.0, layer="near" if i == 1 else "far"))
    elif prop == "torch":
        tgt = (p.sho[0] + 0.17 * hb, p.sho[1] - 0.04 * hb)
        ex, ey, wx, wy = ik2(p.sho[0], p.sho[1], tgt[0], tgt[1], kit.B["ua"], kit.B["fa"], 1.0)
        arms = list(p.arms)
        arms[i] = ((p.sho[0], p.sho[1]), (ex, ey), (wx, wy))
        p.arms = arms
        hk = list(p.hands)
        hk[i] = "fist"
        p.hands = hk
        p.props.append(_prop_fn("torch", hb, (wx, wy), 6.0, layer="near" if i == 1 else "far"))
        p.props.append(("near", _flame_fn((wx + 0.006 * hb, wy - 0.245 * hb * 0.95), hb, T)))
    elif prop in ("sack", "basket"):
        if prop == "sack":
            tgt = (p.sho[0] - 0.02 * hb, p.sho[1] - 0.06 * hb)
            ex, ey, wx, wy = ik2(p.sho[0], p.sho[1], tgt[0], tgt[1], kit.B["ua"], kit.B["fa"], -1.0)
            arms = list(p.arms)
            arms[i] = ((p.sho[0], p.sho[1]), (ex, ey), (wx, wy))
            p.arms = arms
            hk = list(p.hands)
            hk[i] = "fist"
            p.hands = hk
            p.props.append(_prop_fn("sack", hb, (p.sho[0] - 0.045 * hb, p.sho[1] - 0.0 * hb), -18.0, layer="far"))
        else:
            tgt = (p.sho[0] + 0.07 * hb, p.sho[1] + 0.24 * hb)
            ex, ey, wx, wy = ik2(p.sho[0], p.sho[1], tgt[0], tgt[1], kit.B["ua"], kit.B["fa"], 1.0)
            arms = list(p.arms)
            arms[i] = ((p.sho[0], p.sho[1]), (ex, ey), (wx, wy))
            p.arms = arms
            hk = list(p.hands)
            hk[i] = "fist"
            p.hands = hk
            p.props.append(_prop_fn("basket", hb, (wx + 0.01 * hb, wy + 0.0 * hb), 0.0, layer="near"))


def _flag_fn(top, hb, T, flag, v=0.0, ph=0.0):
    """Sancak: sapın üstünde, arkaya (−x) akan dalgalı bez. flag=(device, w, h, c1, c2) (w,h hb oranı)."""
    device, fw, fh, c1, c2 = flag
    wpx, hpx = max(8, int(fw * hb)), max(8, int(fh * hb))
    spr = flag_sprite(device, wpx, hpx, c1, c2)
    cs = _COLSTRIPS.get((device, wpx, hpx, c1, c2))
    if cs is None:
        cs = _COLSTRIPS[(device, wpx, hpx, c1, c2)] = ColStrips(spr, n=max(8, wpx // 7))
    n = cs.n
    wind = 0.45 + min(1.0, v / (0.5 * hb))

    def fn(c):
        dy = np.zeros(n)
        dh = np.ones(n)
        for i in range(n):
            u = 1.0 - (i + 0.5) / n                   # 0 sap ... 1 serbest uç  (sprite: sol = serbest uç, sağ = sap)
            ph_ = T * 7.0 - u * 4.2 + ph
            dy[i] = math.sin(ph_) * 0.07 * hpx * (u ** 1.1) * wind + math.sin(T * 2.3 + u) * 0.01 * hpx * u
            dh[i] = 1.0 + 0.05 * math.sin(ph_ + 1.0) * u * wind
        c.save()
        c.translate(top[0] - wpx, top[1] + 0.02 * hpx)
        cs.draw(c, dy.tolist(), dh.tolist())
        c.restore()
    return fn


_COLSTRIPS = {}


def _flame_fn(pos, hb, T):
    def fn(c):
        x, y = pos
        fl = 0.8 + 0.2 * math.sin(T * 23.0) + 0.12 * math.sin(T * 37.0)
        r = hb * 0.06 * fl
        for (rr, col, a) in ((r * 2.4, "#FF9A3A", 70), (r * 1.4, "#FFC561", 150), (r * 0.8, "#FFF0B0", 235)):
            c.drawOval(skia.Rect.MakeLTRB(x - rr * 0.62, y - rr * 1.5 - 0.0, x + rr * 0.62, y + rr * 0.5), skia.Paint(AntiAlias=True, Color=C(col, a), BlendMode=skia.BlendMode.kPlus if rr > r else skia.BlendMode.kSrcOver))
    return fn


# masa / defter / hokka / florin çizimleri (oturan eylemler için)
@functools.lru_cache(maxsize=16)
def desk_sprite(h):
    """Yan görünüşte masa: ahşap levha + ön panel + ayaklar (hb=h). Origin = zemin, x orijin = figürün kalçası."""
    F = FG.PFig(h)
    F.col = "#8A5A32"
    x0, x1 = 0.12 * h, 0.78 * h
    yt = DESK_Y * h
    F.fill(poly([(x0, yt), (x1, yt), (x1, yt + 0.035 * h), (x0, yt + 0.035 * h)]), rim=1.0)
    F.col = "#6E4524"
    F.fill(poly([(x0 + 0.02 * h, yt + 0.035 * h), (x1 - 0.02 * h, yt + 0.035 * h), (x1 - 0.02 * h, -0.02 * h), (x0 + 0.02 * h, -0.02 * h)]), rim=0.8)
    F.col = "#E3C27A"
    F.gold(poly([(x0 + 0.03 * h, yt + 0.06 * h), (x1 - 0.03 * h, yt + 0.06 * h)], False), h * 0.004, "#D6A93E", 0.9)
    F.fill(poly([(x0 + 0.02 * h, yt + 0.035 * h), (x0 + 0.05 * h, yt + 0.035 * h), (x0 + 0.05 * h, 0), (x0 + 0.02 * h, 0)]), rim=0.7, tone=0.05)
    return Spr(*F.sprite(pad=4))


@functools.lru_cache(maxsize=16)
def stool_sprite(h):
    F = FG.PFig(h)
    F.col = "#6E4524"
    yt = -0.285 * h
    F.fill(poly([(-0.14 * h, yt), (0.09 * h, yt), (0.09 * h, yt + 0.03 * h), (-0.14 * h, yt + 0.03 * h)]), rim=1.0)
    F.fill(K.bar(-0.11 * h, yt + 0.03 * h, -0.13 * h, 0, 0.02 * h, 0.02 * h), rim=0.9)
    F.fill(K.bar(0.06 * h, yt + 0.03 * h, 0.08 * h, 0, 0.02 * h, 0.02 * h), rim=0.9)
    return Spr(*F.sprite(pad=4))


def draw_desk(c, kit, p, T, alpha=1.0):
    """Gövde üstüne masa ön paneli + sandalye (kollardan ÖNCE çizilmez: gövde → masa → kollar)."""
    hb = kit.B["hb"]
    st = stool_sprite(int(round(hb)))
    ds = desk_sprite(int(round(hb)))
    pt = skia.Paint(AntiAlias=False)
    if alpha < 1.0:
        pt.setAlphaf(alpha)
    # sandalye gövdenin ALTINA (bacaklar zaten çizildi) — kalçanın altında görünür
    c.drawImage(st.img, -st.ox, -st.oy, LIN, pt)
    c.drawImage(ds.img, -ds.ox, -ds.oy, LIN, pt)


def draw_desk_top(c, kit, p, T, alpha=1.0):
    """Masa üstü: defter/sayfa + yazılı satırlar, hokka, florin yığınları (kollardan SONRA)."""
    hb = kit.B["hb"]
    ex = p.extra or {}
    yt = DESK_Y * hb
    c.save()
    pa = skia.Paint(AntiAlias=True)
    pa.setAlphaf(alpha)
    if "coins" in ex:
        cn = ex["coins"]
        for (xx, nn, col) in ((cn["xa"], 9, "#E0B84E"), ):
            for k in range(nn):
                _coin(c, xx - 0.02 * hb, yt - 0.006 * hb * k, hb, alpha)
        stack = cn["n"] % 9 + (0 if cn["u"] >= 0.82 else 0)
        for k in range(stack):
            _coin(c, cn["xb"], yt - 0.0068 * hb * k, hb, alpha)
        # sol yanda gelen/giden küçük torba
        if cn["grab"]:
            _coin(c, cn["hand"][0] + 0.004 * hb, cn["hand"][1] + 0.02 * hb, hb, alpha)
    else:
        # defter: açık iki sayfa (yan görünüşte ince paralelkenar) + satırlar
        x0, x1 = 0.20 * hb, 0.38 * hb
        pg = sp([KC(x0, yt), (x0 + 0.03 * hb, yt - 0.026 * hb), KC(x1 + 0.03 * hb, yt - 0.026 * hb), KC(x1, yt)], True, 0.2)
        c.drawPath(pg, skia.Paint(AntiAlias=True, Color=C("#EDE4C8", int(255 * alpha))))
        c.drawPath(pg, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.0, hb * 0.0035), Color=C(INK, int(190 * alpha))))
        prog = ex.get("prog", 0.0)
        ln = ex.get("line", 0)
        nl = 3
        for k in range(nl):
            fy = yt - 0.006 * hb - 0.007 * hb * k
            fx0 = x0 + 0.008 * hb + 0.007 * hb * k * 1.1
            ln_full = (x1 - x0 - 0.03 * hb)
            done = 1.0 if k < (ln % nl) else (prog if k == (ln % nl) else 0.0)
            if ln >= nl:
                done = 1.0 if k != (ln % nl) else prog
            if done > 0.01:
                c.drawLine(fx0, fy, fx0 + ln_full * done, fy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(0.9, hb * 0.0032), Color=C("#2A1A0C", int(220 * alpha))))
        # hokka
        ix, iy = ex.get("ink", (0.44 * hb, yt - 0.02 * hb))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(ix - 0.016 * hb, yt - 0.034 * hb, ix + 0.016 * hb, yt), 3, 3), skia.Paint(AntiAlias=True, Color=C("#1E1A18", int(255 * alpha))))
        c.drawRect(skia.Rect.MakeLTRB(ix - 0.010 * hb, yt - 0.040 * hb, ix + 0.010 * hb, yt - 0.034 * hb), skia.Paint(AntiAlias=True, Color=C("#7A5A2A", int(255 * alpha))))
    c.restore()


def _coin(c, x, y, hb, alpha=1.0):
    rx, ry = 0.021 * hb, 0.0075 * hb
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry * 0.4), skia.Paint(AntiAlias=True, Color=C("#8A6422", int(255 * alpha))))
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry * 1.4, x + rx, y + ry * 0.2), skia.Paint(AntiAlias=True, Color=C("#E8C25A", int(255 * alpha))))
    c.drawOval(skia.Rect.MakeLTRB(x - rx * 0.55, y - ry * 1.15, x + rx * 0.2, y - ry * 0.1), skia.Paint(AntiAlias=True, Color=C("#FFF0B0", int(150 * alpha))))


# ═════════════════════════════ AT + BİNİCİ (cilt_figs boyası; bacaklar IK ile yürür) ═════════════════════════════
COATS = ["#F0E8D4", "#8A5A38", "#3A2A20", "#C8A878", "#B8B0A0", "#6A4A30", "#5A3A26"]
MANES = ["#6B5A44", "#2A1A10", "#9A8A70", "#3A2A1C"]
CLOTHS = ["#A8321E", "#233C8C", "#2E7A5A", "#7A2E56", "#C79A3C", "#1F5A7A", "#8A3A1E"]
RHATS = ["mazzocchio", "mazzocchio", "flatcap", "beret", "scholar", "tall", "woolcap"]

FORE_REST = [(0.30, -0.50), (0.30, -0.265), (0.30, -0.075), (0.30, 0.0)]
HIND_REST = [(-0.40, -0.58), (-0.40, -0.30), (-0.40, -0.075), (-0.40, 0.0)]
LEGS_L = dict(f=(0.235, 0.265), h=(0.28, 0.30))          # (üst, alt) kemik boyları (hs)

GAIT = dict(
    walk=dict(A=0.19, beta=0.70, lift=0.085, ph=dict(hn=0.00, fn=0.25, hf=0.50, ff=0.75), pitch=1.3, bobf=0.0),
    trot=dict(A=0.24, beta=0.46, lift=0.130, ph=dict(fn=0.00, hf=0.00, ff=0.50, hn=0.50), pitch=1.8, bobf=0.01),
    gallop=dict(A=0.40, beta=0.28, lift=0.220, ph=dict(hn=0.00, hf=0.10, fn=0.42, ff=0.52), pitch=4.2, bobf=0.04),
)


def horse_spec(seed=0, **over):
    rs = np.random.RandomState(seed * 977 + 31)
    d = dict(coat=_pick(rs, COATS), mane=_pick(rs, MANES), cloth=_pick(rs, CLOTHS), cl_pat=(_pick(rs, PATS), "#E8E0C0"), capar=True,
             robe=_pick(rs, ROBES), robe2=GOLD, hat=_pick(rs, RHATS), hat_col=_pick(rs, ROBES), hose=_pick(rs, HOSES), hair=_pick(rs, HAIRS), pat=(_pick(rs, PATS), GOLD),
             skin=_pick(rs, SKINS), beard=_pick(rs, [None, None, "short", "stache"]))
    d.update(over)
    return tuple(sorted(d.items(), key=lambda kv: kv[0]))


class HKit:
    pass


def _paint_horse_body(hs, coat, mane, bridle="#A8321E"):
    """paint_horse'un gövde parçası (bacak/kuyruk/yele yok): kulaklar, gövde-boyun-baş, göz, burun, dizgin."""
    P = FH.HORSE_WALK
    poll = P["poll"]
    L = 0.31
    top, muz, bot, throat, eye, nostril, lip, (ax, ay, nx, ny) = FH._head_geometry(poll, L, P["head_ang"])
    shade = mix(coat, "#3A2A18", 0.20)
    F = FG.PFig(hs)
    h = hs
    dy = 0.0
    ex = poll[0] - 0.020
    ey = poll[1] - 0.005
    F.col = shade
    F.fill(sp(FH._hp([KC(ex - 0.016, ey), (ex - 0.026, ey - 0.055), KC(ex - 0.008, ey - 0.118), (ex + 0.020, ey - 0.056), KC(ex + 0.022, ey)], h), True, 0.8), rim=0.6)
    W0 = (0.20, -0.765)
    crest = []
    dxn, dyn = poll[0] - W0[0], poll[1] - W0[1]
    Ln = math.hypot(dxn, dyn)
    cnx, cny = dyn / Ln, -dxn / Ln
    for t in (0.18, 0.38, 0.58, 0.78):
        b = 0.040 * math.sin(math.pi * t)
        crest.append((W0[0] + dxn * t + cnx * b, W0[1] + dyn * t + cny * b))
    B0 = (0.425, -0.60)
    under = []
    for t in (0.22, 0.48, 0.74):
        tx_, ty_ = throat
        q = (tx_ + (B0[0] - tx_) * t, ty_ + (B0[1] - ty_) * t)
        bulge = -0.018 * math.sin(math.pi * t)
        under.append((q[0] + bulge * 0.7, q[1] + bulge * 0.6))
    under = under[::-1]
    body = [KC(-0.515, -0.755 + dy), (-0.45, -0.780 + dy), (-0.34, -0.785 + dy), (-0.20, -0.755 + dy), (-0.02, -0.738 + dy), (0.10, -0.745 + dy), (0.20, -0.766 + dy)] + crest + top + muz + bot + [throat] + under + [
        B0, (0.438, -0.535), (0.405, -0.455), (0.32, -0.418), (0.18, -0.402), (0.02, -0.402), (-0.14, -0.425), (-0.27, -0.452), (-0.38, -0.49), (-0.50, -0.545), (-0.552, -0.625), (-0.548, -0.70)]
    body = [(q[0] * h, q[1] * h, "c") if len(q) > 2 else (q[0] * h, q[1] * h) for q in body]
    F.col = coat
    F.fill(sp(body, True, 1.0), rim=1.0)
    F.col = shade
    F.line(sp(FH._hp([(-0.36, -0.77), (-0.31, -0.62), (-0.30, -0.49)], h), False), h * 0.004, tone=0.0, alpha=0.30)
    F.line(sp(FH._hp([(0.16, -0.755), (0.25, -0.62), (0.30, -0.50)], h), False), h * 0.004, tone=0.0, alpha=0.30)
    F.col = coat
    F.fill(sp(FH._hp([KC(ex - 0.020 + 0.032, ey + 0.004), (ex - 0.030 + 0.032, ey - 0.054), KC(ex - 0.008 + 0.032, ey - 0.121), (ex + 0.024 + 0.032, ey - 0.056), KC(ex + 0.026 + 0.032, ey + 0.004)], h), True, 0.8), rim=1.0)
    F.col = mane
    F.fill(sp(FH._hp([KC(poll[0] + 0.03, poll[1] - 0.012), (poll[0] + 0.07, poll[1] + 0.005), (poll[0] + 0.065, poll[1] + 0.055), (poll[0] + 0.04, poll[1] + 0.07), (poll[0] + 0.035, poll[1] + 0.03)], h), True, 0.8), rim=1.0, bound=False)
    F.col = INK
    F.fill(ell(eye[0] * h, eye[1] * h, 0.010 * h, 0.0075 * h, -20), rim=0.0, tone=0.2, alpha=0.9, bound=False)
    F.fill(ell(nostril[0] * h, nostril[1] * h, 0.0085 * h, 0.0125 * h, -30), rim=0.0, tone=0.2, alpha=0.55, bound=False)
    F.col = bridle

    def Wh(u, v):
        return (poll[0] + L * (u * ax + v * nx), poll[1] + L * (u * ay + v * ny))
    for pts in ([Wh(0.34, -0.06), Wh(0.30, 0.20), Wh(0.30, 0.45)], [Wh(0.12, -0.06), Wh(0.10, 0.12), Wh(0.14, 0.28)], [Wh(0.78, -0.002), Wh(0.77, 0.12), Wh(0.80, 0.24)]):
        F.gold(sp(FH._hp(pts, h), False), h * 0.0042, "#C23A24", 0.95)
    return Spr(*F.sprite(pad=5))


def _paint_horse_mane(hs, mane):
    F = FG.PFig(hs)
    P = FH.HORSE_WALK
    poll = P["poll"]
    W0 = (0.20, -0.765)
    F.col = mane
    FH._mane_locks(F, (W0[0] + 0.02, W0[1] - 0.012), (poll[0] - 0.015, poll[1] + 0.005), hs, n=7, long=0.95, flick=0.25)
    return Spr(*F.sprite(pad=4))


def _paint_horse_leg(hs, coat, kind, far):
    F = FG.PFig(hs)
    shade = mix(coat, "#3A2A18", 0.20)
    F.col = shade if far else coat
    joints = FORE_REST if kind == "f" else HIND_REST
    FH._hleg(F, joints, kind, hs, rim=0.40 if far else 1.0)
    spr = Spr(*F.sprite(pad=4))
    rest = [(x * hs, y * hs) for (x, y) in joints]
    return spr, rest


def _paint_horse_tail(hs, mane):
    F = FG.PFig(hs)
    F.col = mane
    tp = [(-0.56, -0.745), (-0.56, -0.66), (-0.56, -0.56), (-0.56, -0.46), (-0.56, -0.36), (-0.56, -0.27)]
    wd = [0.045, 0.085, 0.095, 0.085, 0.052, 0.012]
    F.fill(limb([(x * hs, y * hs) for x, y in tp], [w * hs for w in wd], cap0=0.4, cap1=0.0), rim=1.0)
    F.crease((-0.575 * hs, -0.68 * hs), (-0.575 * hs, -0.32 * hs), 0.008 * hs, 0.012 * hs, alpha=0.5)
    spr = Spr(*F.sprite(pad=4))
    return spr, [(-0.56 * hs, -0.745 * hs), (-0.56 * hs, -0.51 * hs), (-0.56 * hs, -0.27 * hs)]


@functools.lru_cache(maxsize=48)
def build_hkit(spec, bake_h):
    d = dict(spec)
    hs = bake_h / 1.2
    k = HKit()
    k.spec, k.d, k.h, k.hs = spec, d, bake_h, hs
    body = _paint_horse_body(hs, d["coat"], d["mane"])
    k.mane = _paint_horse_mane(hs, d["mane"])
    k.legs = {}
    for name, kind, far in (("ff", "f", True), ("hf", "h", True), ("hn", "h", False), ("fn", "f", False)):
        spr, rest = _paint_horse_leg(hs, d["coat"], kind, far)
        k.legs[name] = Skin(spr, rest, rows=(3, 4, 2))
    spr, rest = _paint_horse_tail(hs, d["mane"])
    k.tail = Skin(spr, rest, rows=(4, 4))
    k.tail_len = 0.475 * hs
    F = FG.PFig(hs)
    cap = None
    if d["capar"]:
        FG.paint_caparison(F, hs, cloth=d["cloth"], pat=d["cl_pat"])
        cap = Spr(*F.sprite(pad=4))
    parts = [body] + ([cap] if cap is not None else [])
    L_ = max(p.ox for p in parts)
    T_ = max(p.oy for p in parts)
    R_ = max(p.w - p.ox for p in parts)
    B_ = max(p.h - p.oy for p in parts)
    fr = sk.Frame(int(L_ + R_), int(T_ + B_))
    fr.clear(skia.ColorTRANSPARENT)
    for p in parts:
        fr.c.drawImage(p.img, L_ - p.ox, T_ - p.oy)
    k.body = Spr(fr.surf.makeImageSnapshot(), L_, T_)
    k.body_v = VStrips(k.body, step=max(5.0, 0.028 * hs))
    # binici: oturak noktası (0,0)
    R = FG.PFig(bake_h)
    u = 0.45 * hs
    FG.paint_rider(R, 0.0, 0.0, u, d["robe"], d["robe2"], d["hat"], d["hat_col"], d["skin"], d["hair"], d["pat"], None, d["hose"], d["beard"])
    k.rider = Spr(*R.sprite(pad=6))
    k.rider_s = Strips(k.rider, -3.0 * bake_h, 3.0 * bake_h, step=max(4.0, 0.022 * bake_h))
    k.seat = (-0.005 * hs, -0.735 * hs)
    k.u = u
    return k


def _hpath(u, A, beta, lift):
    x, y, a, st = _foot(u, beta, A, lift, 0.0)
    return x, y, st


def horse_pose(hk, T, v, gait="walk", phase=0.0):
    """At iskeleti: dört bacak (üst, diz, bilek, toynak), gövde ötelemesi/eğimi, kuyruk açısı. v: zemine göre bake-px/sn."""
    hs = hk.hs
    G = GAIT[gait]
    A, beta, lift = G["A"], G["beta"], G["lift"]
    S = 2 * A / beta
    f = (v / hs) / S if v > 1e-3 else 0.0
    out = {}
    stance_dy = []
    legs = {}
    for name, rest in (("fn", FORE_REST), ("ff", FORE_REST), ("hn", HIND_REST), ("hf", HIND_REST)):
        u = (T * f + G["ph"][name] + phase) % 1.0
        x, y, st = _hpath(u, A, beta, lift)
        top = rest[0]
        legs[name] = (u, x, y, st)
        if st:
            Ltot = abs(top[1]) * 0.992
            stance_dy.append(math.sqrt(max(Ltot * Ltot - x * x, (0.7 * Ltot) ** 2)) - abs(top[1]))
    if v < 1e-3:
        dyb = 0.0
    elif stance_dy:
        dyb = _smin(stance_dy, 40.0) if len(stance_dy) > 1 else stance_dy[0]
    else:
        dyb = G["bobf"] * 0.6
    if G["bobf"] > 0 and v > 1e-3:
        # uçuş fazı yumuşatması: ±0.02 çevrim örnekle
        acc = 0.0
        for dphi in (-0.04, -0.02, 0.0, 0.02, 0.04):
            sd = []
            for name, rest in (("fn", FORE_REST), ("ff", FORE_REST), ("hn", HIND_REST), ("hf", HIND_REST)):
                u = (T * f + G["ph"][name] + phase + dphi) % 1.0
                x, y, st = _hpath(u, A, beta, lift)
                if st:
                    Ltot = abs(rest[0][1]) * 0.992
                    sd.append(math.sqrt(max(Ltot * Ltot - x * x, (0.7 * Ltot) ** 2)) - abs(rest[0][1]))
            acc += (_smin(sd, 40.0) if len(sd) > 1 else sd[0]) if sd else G["bobf"] * 1.2
        dyb = acc / 5.0
    cyc = (T * f + phase) % 1.0
    pitch = G["pitch"] * math.sin(2 * math.pi * cyc * (1.0 if gait != "trot" else 2.0) + 0.6) if v > 1e-3 else 0.6 * math.sin(T * 0.5 + phase * 6.28)
    out["legs"] = legs
    out["dy"] = dyb * hs
    out["pitch"] = pitch
    out["f"] = f
    return out


def _ik_leg(hk, name, top_w, hoof_w, bend):
    """Üst nokta → toynak hedefi için 2 kemikli IK; bilek, diz–toynak doğrusu üzerinde. Dönüş: [top, knee, fetlock, hoof]."""
    hs = hk.hs
    l1, l2 = LEGS_L["f" if name[0] == "f" else "h"]
    kx, ky, hx, hy = ik2(top_w[0], top_w[1], hoof_w[0], hoof_w[1], l1 * hs, l2 * hs, bend)
    fx, fy = kx + (hx - kx) * 0.72, ky + (hy - ky) * 0.72
    return [top_w, (kx, ky), (fx, fy), (hx, hy)]


def draw_rider(c, hk, T, x, y, h, bake_h, speed=120.0, gait="walk", dirn=1, phase=0.0, alpha=1.0, cf=None, prop=None, pose_out=None):
    """x,y: ayak hizası ekran; h: zeminden binici başlığına boy (px) — build_rider ile aynı sözleşme."""
    s = h / bake_h
    hs = hk.hs
    v = abs(speed) / s
    P = horse_pose(hk, T, v, gait, phase)
    dy = P["dy"]
    pitch = P["pitch"]
    pvx, pvy = -0.35 * hs, -0.60 * hs
    rad = pitch * D2R
    cs, sn = math.cos(rad), math.sin(rad)

    def bt(px, py):
        qx, qy = px - pvx, py - pvy
        return pvx + qx * cs - qy * sn, pvy + qx * sn + qy * cs + dy
    c.save()
    c.translate(x, y)
    c.scale(dirn * s, s)
    pt = None
    if alpha < 1.0 or cf is not None:
        pt = skia.Paint(AntiAlias=False)
        pt.setAlphaf(alpha)
        if cf is not None:
            pt.setColorFilter(cf)
    # bacaklar (uzaklar önce)
    for name in ("ff", "hf", "hn", "fn"):
        u, hx_rel, hy_rel, st = P["legs"][name]
        rest = FORE_REST if name[0] == "f" else HIND_REST
        top_w = bt(rest[0][0] * hs, rest[0][1] * hs)
        hoof = (rest[0][0] * hs + hx_rel * hs, -hy_rel * hs)
        pts = _ik_leg(hk, name, top_w, hoof, -1.0 if name[0] == "f" else 1.0)
        hk.legs[name].draw(c, pts, alpha, cf)
    # kuyruk
    G = GAIT[gait]
    fr = P["f"]
    if gait == "gallop":
        psi = 74.0 + 6.0 * math.sin(T * 7.0 + phase * 6.28)
    elif gait == "trot":
        psi = 28.0 + 9.0 * math.sin(T * 4.0 + phase * 6.28)
    else:
        psi = 7.0 + 7.0 * math.sin(T * 1.7 + phase * 6.28) + (min(1.0, v / (hs * 0.3)) * 8.0)
    dock = bt(-0.52 * hs, -0.745 * hs)
    L = hk.tail_len
    a1 = psi * D2R
    a2 = (psi * 1.35 + 6.0 * math.sin(T * 3.1 + phase * 4.0)) * D2R
    mid = (dock[0] - 0.5 * L * math.sin(a1), dock[1] + 0.5 * L * math.cos(a1))
    end = (mid[0] - 0.5 * L * math.sin(a2), mid[1] + 0.5 * L * math.cos(a2))
    hk.tail.draw(c, [dock, mid, end], alpha, cf)
    # gövde (+ kapariş): dikey dilimlerle eğim (arka kalçadan) + sıçrama
    xs = hk.body_v.xcen
    dyv = dy + (xs - pvx) * math.sin(rad)
    hk.body_v.draw(c, dyv, 0.0, alpha, cf)
    # yele: boyun çizgisinde hafif dalgalanma
    mr = (3.0 + 7.0 * (1.0 if gait == "gallop" else 0.3)) * math.sin(T * (9.0 if gait == "gallop" else 3.2) + phase * 5.0) + (6.0 if gait == "gallop" else 0.0) + pitch
    mp = bt(0.37 * hs, -0.87 * hs)
    c.save()
    c.translate(mp[0], mp[1])
    c.rotate(mr)
    if pt is None:
        c.drawImage(hk.mane.img, -hk.mane.ox - 0.37 * hs, -hk.mane.oy + 0.87 * hs, LIN)
    else:
        c.drawImage(hk.mane.img, -hk.mane.ox - 0.37 * hs, -hk.mane.oy + 0.87 * hs, LIN, pt)
    c.restore()
    # binici: oturak noktasında gövde eğimi + kendi sallanması (şerit kaydırma)
    sway = -0.7 * pitch + 1.1 * math.sin(T * (6.0 if gait == "gallop" else 2.4) + phase * 6.28) * (0.4 if v < 1e-3 else 1.0)
    sp_ = bt(hk.seat[0], hk.seat[1])
    ang = math.sin((pitch + sway) * D2R)
    yc = hk.rider_s.ycen
    dxr = sp_[0] - yc * ang
    dyr = np.full_like(yc, sp_[1])
    z = np.zeros_like(yc)
    hk.rider_s.draw(c, dxr, dyr, z, z, alpha, cf)
    if prop:
        c.save()
        c.translate(sp_[0], sp_[1])
        c.rotate(pitch + sway)
        prop(c, hk)
        c.restore()
    c.restore()
    return P


def rider(f, x, y, h, t, speed=120.0, gait="walk", dir=1, seed=0, phase=0.0, alpha=1.0, cf=None, prop=None, **stil):
    """Atlı: at (yürüyüş/tırıs/dörtnala; bacaklar IK ile — toynak kaymaz) + binici. h = zeminden binici başlığına boy (px)."""
    spec = horse_spec(seed, **stil)
    bh = _bake_for(h * SCALE_HINT)
    hk = build_hkit(spec, bh)
    return draw_rider(f.c, hk, t, x, y, h, bh, speed=speed, gait=gait, dirn=dir, phase=phase, alpha=alpha, cf=cf, prop=prop)


# ═════════════════════════════ İKİ FİGÜRLÜ SAHNELER ═════════════════════════════
def handshake(f, kindA, kindB, x, y, h, t, gap=0.60, t0=0.5, seedA=0, seedB=1, alpha=1.0, **stil):
    """El sıkışma: A (sağa bakar) soldan, B sağdan; eller ortada buluşur, 3 kez sallanır. x = ikisinin ortası, gap = aralık (h oranı)."""
    xa, xb = x - gap * h * 0.5, x + gap * h * 0.5
    kitA, bhA = kit_for(kindA, seedA, h)
    kitB, bhB = kit_for(kindB, seedB, h * 0.97)
    sA, sB = h / bhA, h * 0.97 / bhB
    Mw = (x, y - 0.50 * h)
    pa = act_handshake(kitA, t, 0.1, t0=t0, M=((Mw[0] - xa) / sA / kitA.B["hb"], (Mw[1] - y) / sA / kitA.B["hb"]))
    pb = act_handshake(kitB, t, 0.6, t0=t0 + 0.05, M=((xb - Mw[0]) / sB / kitB.B["hb"], (Mw[1] - y) / sB / kitB.B["hb"]))
    for kit, bh, p, xx, dd, hh, ph in ((kitA, bhA, pa, xa, 1, h, 0.1), (kitB, bhB, pb, xb, -1, h * 0.97, 0.6)):
        cloth_for(kit, p, t, ph * 6.28, lag=0.0, wave=0.0)
        _draw_pose(f, kit, bh, p, xx, y, hh, dd, alpha, None, ("back", "legs", "body", "head"))
    for kit, bh, p, xx, dd, hh in ((kitB, bhB, pb, xb, -1, h * 0.97), (kitA, bhA, pa, xa, 1, h)):
        _draw_pose(f, kit, bh, p, xx, y, hh, dd, alpha, None, ("arms",))


def threat(f, t, x, y, h, dir=1, t0=0.4, dur=1.2, victim="kardinal", attacker="asker", alpha=1.0, color="#1A1008", rim="#E8A860", gap=0.55, seed=0):
    """ŞİDDET İŞARETİ: yalnız siluet. Saldırgan öne atılır, hançerli kolu yukarı kalkar; kurban kayar/dönmeye çalışır. Kan yok. Renk: koyu siluet + sıcak kenar ışığı."""
    flat = skia.ColorFilters.Blend(C(color), skia.BlendMode.kSrcIn)
    warm = skia.ColorFilters.Blend(C(rim), skia.BlendMode.kSrcIn)
    kitA, bhA = kit_for(attacker, seed, h)
    kitV, bhV = kit_for(victim, seed + 1, h * 0.98)
    sA, sV = h / bhA, h * 0.98 / bhV
    k = ramp(t, t0, dur * 0.55)
    xa = x - dir * gap * h * 0.5 + dir * 0.10 * h * k
    xv = x + dir * gap * h * 0.5 + dir * 0.015 * h * k
    pa = act_threat(kitA, t, 0.0, t0=t0, dur=dur)
    cloth_for(kitA, pa, t, 0.0, lag=0.0, wave=0.0)
    # kurban: gövde hafif geri yaslanır, kollar yarı açık
    hbv = kitV.B["hb"]

    def arms_v(sho):
        return ("ik", (sho[0] - 0.03 * hbv * k, sho[1] + 0.25 * hbv)), ("ik", (sho[0] + 0.15 * hbv * k, sho[1] + 0.12 * hbv - 0.08 * hbv * k)), "open", "open"
    pv = stand(kitV, t, 0.4, arms=arms_v, tor_add=-6.0 * k, head_add=-5.0 * k)
    cloth_for(kitV, pv, t, 0.0, lag=0.0, wave=0.0)
    # kurbanı saldırganın karşısına çevir (dir tersi)
    for off, cf_ in ((1.6, warm), (0.0, flat)):
        for kit, bh, p, xx, dd, hh in ((kitV, bhV, pv, xv, -dir, h * 0.98), (kitA, bhA, pa, xa, dir, h)):
            c = f.c
            c.save()
            c.translate(-off * dir, -off * 0.9)
            _draw_pose(f, kit, bh, p, xx, y, hh, dd, alpha, cf_)
            c.restore()


# ═════════════════════════════ KALABALIK ═════════════════════════════
CROWD_MIX = dict(halk=0.34, tuccar=0.14, soylu=0.07, soylu_f=0.10, cocuk=0.06, asker=0.05, rahip=0.05, denizci=0.03, banker=0.05, kesis=0.03, katip=0.0, papa=0.0, kardinal=0.02)


_CM_CACHE = {}


def crowd_members(seed, n, rect, h, mix=None):
    key = (seed, n, tuple(rect), tuple(h), tuple(sorted(mix.items())) if mix else None)
    r = _CM_CACHE.get(key)
    if r is None:
        if len(_CM_CACHE) > 200:
            _CM_CACHE.clear()
        r = _CM_CACHE[key] = _crowd_members(seed, n, rect, h, mix)
    return r


def _crowd_members(seed, n, rect, h, mix=None):
    rs = np.random.RandomState(seed * 7919 + 13)
    x0, y0, x1, y1 = rect
    mix = mix or CROWD_MIX
    kinds = [k for k, w in mix.items() if w > 0]
    wts = np.array([mix[k] for k in kinds], float)
    wts /= wts.sum()
    out = []
    for i in range(n):
        yy = y0 + (y1 - y0) * (rs.rand() ** 0.85)
        dep = (yy - y0) / max(1.0, (y1 - y0))
        hh = lerp(h[0], h[1], dep) * rs.uniform(0.92, 1.08)
        kind = kinds[rs.choice(len(kinds), p=wts)]
        out.append(dict(i=i, kind=kind, seed=int(rs.randint(0, 9999)), x=x0 + (x1 - x0) * rs.rand(), y=yy, h=hh, phase=rs.rand(), A=rs.uniform(18, 70), P=rs.uniform(11, 28), ph=rs.uniform(0, 6.28),
                        talk=rs.rand() < 0.45, dir0=1 if rs.rand() < 0.5 else -1, r=rs.rand(), r2=rs.rand()))
    out.sort(key=lambda d: d["y"])
    return out


def crowd(f, t, rect, n, seed=1, wave=0.0, mode="mill", dir=1, h=(130, 240), speed=70.0, mix=None, scroll=0.0, rise_at=None, alpha=1.0, loop=True, cf=None, wave_speed=1.0, cull=260, view=None):
    """Kalabalık. rect=(x0,y0,x1,y1): ayakların durduğu ekran bölgesi (y0 uzak sıra, y1 yakın sıra); h=(uzak,yakın) boy.
    mode: mill (dolaşan/konuşan) | stand | kneel (diz çökmüş; rise_at ile dalga halinde kalkar) | cheer (kollar havada, dalga) | march (dir yönünde yürür) | run (kaçış).
    wave: 0..1 — x boyunca ilerleyen dalga (eğilme/kol kaldırma); scroll: kameranın yatay kayması (px)."""
    mem = crowd_members(seed, n, rect, h, mix)
    x0, y0, x1, y1 = rect
    Wd = (x1 - x0)
    dirn = 1 if dir in (1, "r") else -1
    out_n = 0
    for m in mem:
        xi = m["x"]
        if mode in ("march", "run"):
            sp_ = speed * (0.85 + 0.3 * m["r"]) * (2.6 if mode == "run" else 1.0)
            xw = xi + dirn * sp_ * t
            if loop:
                xw = x0 + ((xw - x0) % (Wd + 2 * cull)) - cull
        elif mode == "mill":
            xw = xi + m["A"] * math.sin(2 * math.pi * t / m["P"] + m["ph"])
        else:
            xw = xi
        xs = xw - scroll
        if view is not None:
            if xs < view[0] - cull or xs > view[1] + cull:
                continue
        elif xs < -cull or xs > W + cull:
            continue
        yy = m["y"]
        hh = m["h"]
        dvx = 0.0
        face = dirn if mode in ("march", "run") else m["dir0"]
        if mode == "mill":
            dvx = m["A"] * (2 * math.pi / m["P"]) * math.cos(2 * math.pi * t / m["P"] + m["ph"])
            face = 1 if dvx > 0 else -1
            if abs(dvx) < 9.0:
                face = m["dir0"] if (int(t / m["P"] * 0.5 + m["r"] * 5) % 2 == 0) else -m["dir0"]
        kit, bh = kit_for(m["kind"], m["seed"], hh)
        s_ = hh / bh
        T = t + m["r2"] * 3.0
        wv = 0.0
        if wave:
            wv = math.sin(2 * math.pi * (t * 0.45 * wave_speed) - xw * 0.0055 * dirn)
        if mode == "kneel":
            ra = None if rise_at is None else rise_at + 0.55 * (xw - x0) / max(1.0, Wd) * 3.0 + m["r"] * 0.8
            p = act_kneel(kit, T, m["phase"], t0=0.0 - 3.0, dur=0.1, rise_at=ra)
            if wave:
                p.tor += 2.5 * wv * wave
        elif mode == "cheer":
            amt = clamp(0.35 + 0.65 * (0.5 + 0.5 * wv) * (0.4 + 0.6 * wave) if wave else 0.8)
            p = act_cheer(kit, T, m["phase"], amount=amt, hop=0.5 + 0.5 * m["r"])
        elif mode in ("march", "run"):
            v = (sp_ * (1.0 if mode == "march" else 1.0)) / s_
            p = gait(kit, T, v, m["phase"], run=(mode == "run"), stride=kit.d.get("stride", 1.0)) if v > 2 else stand(kit, T, m["phase"])
            if wave:
                p.tor += 1.6 * wv * wave
        else:   # mill / stand
            vv = abs(dvx) / s_
            if mode == "mill" and abs(dvx) >= 9.0:
                p = gait(kit, T, vv, m["phase"], stride=kit.d.get("stride", 1.0))
            elif m["talk"]:
                p = act_talk(kit, T, m["phase"], energy=0.7 + 0.5 * m["r"])
            else:
                p = stand(kit, T, m["phase"])
            if wave:
                p.tor += 2.0 * wv * wave
        lag = min((sp_ if mode in ("march", "run") else abs(dvx)) / s_ * 0.06, 0.22 * bh) * (1.5 if mode == "run" else 1.0)
        cloth_for(kit, p, T, m["phase"] * 6.28, lag=lag, wave=0.0)
        a_ = alpha
        _draw_pose(f, kit, bh, p, xs, yy, hh, face, a_, cf)
        out_n += 1
    return out_n


# ═════════════════════════════ ALAY (Gozzoli "Magi Alayı": gerçekten yürüyen friz) ═════════════════════════════
PROC_MIX = dict(rider=0.30, noble=0.20, page=0.12, banner=0.11, guard=0.09, elder=0.08, cleric=0.04, common=0.06)
FLAGS = [("medici", "#E0B84E", "#B33620"), ("lily", "#F4EEDC", "#B33620"), ("cross", "#F4EEDC", "#B33620"), ("stripes", "#233C8C", "#E0B84E"), ("plain", "#2E7A5A", "#E0B84E"), ("medici", "#E0B84E", "#B33620")]
ROW_DEF = [dict(y=444, h=(190, 245), gap=(170, 330), g=0.74, w=0.72), dict(y=543, h=(265, 330), gap=(260, 470), g=0.86, w=0.84), dict(y=650, h=(350, 430), gap=(430, 700), g=1.0, w=0.97)]


def _smooth_ease_int(t, tin, tout, total):
    """Kamera hız eğrisi e(t): tin sn'de 0→1, son tout sn'de 1→0 (smoothstep); E(t)=∫e. t<0 için e=1 (geçişte çekim öncesi de akar)."""
    if t < 0:
        return t

    def Ein(x):
        if tin <= 1e-6:
            return x
        if x >= tin:
            return x - tin * 0.5
        u = x / tin
        return tin * (u ** 3 - 0.5 * u ** 4)
    T0 = total - tout
    if tout > 1e-6 and total > tout and t > T0:
        u = min(1.0, (t - T0) / tout)
        return Ein(T0) + tout * (u - (u ** 3 - 0.5 * u ** 4))
    return Ein(t)


def procession_cast(seed, dirn, density=1.0, mix=None, rows=None, span=None, margin=520):
    """Alay listesi (ekran uzayı, t=0 konumları). Dönüş: [dict(row, kind('walker'|'rider'), …)]."""
    rs = np.random.RandomState(seed * 1237 + 5)
    rows = rows or ROW_DEF
    mix = mix or PROC_MIX
    keys = [k for k, w in mix.items() if w > 0]
    wts = np.array([mix[k] for k in keys], float)
    wts /= wts.sum()
    xmin, xmax = -margin, (span or W) + margin
    cast = []
    for ri, R in enumerate(rows):
        x = xmin + rs.uniform(0, R["gap"][1])
        while x < xmax:
            cat = keys[rs.choice(len(keys), p=wts)]
            h = rs.uniform(*R["h"])
            u = dict(row=ri, x0=x, h=h, phase=rs.rand(), seed=int(rs.randint(0, 99999)), wk=R["w"] * rs.uniform(0.9, 1.1), cat=cat, y=R["y"] + rs.uniform(-6, 8) * (0.5 + ri * 0.4))
            if cat == "rider":
                u["kind"] = "rider"
                u["gait"] = "walk" if rs.rand() < 0.86 else "trot"
                u["banner"] = FLAGS[rs.randint(len(FLAGS))] if rs.rand() < 0.22 else None
                u["h"] = h * 1.14
            else:
                u["kind"] = "walker"
                if cat == "noble":
                    u["ck"] = "soylu" if rs.rand() < 0.62 else "soylu_f"
                elif cat == "page":
                    u["ck"] = "cocuk"
                    u["h"] = h * 0.86
                elif cat == "banner":
                    u["ck"] = ["soylu", "asker", "tuccar"][rs.randint(3)]
                    u["prop"] = "pole"
                    u["flag"] = FLAGS[rs.randint(len(FLAGS))]
                elif cat == "guard":
                    u["ck"] = "asker"
                    u["prop"] = "spear" if rs.rand() < 0.6 else "halberd"
                elif cat == "elder":
                    u["ck"] = ["banker", "tuccar", "kesis"][rs.randint(3)]
                    if rs.rand() < 0.4:
                        u["prop"] = ["staff", "book"][rs.randint(2)]
                elif cat == "cleric":
                    u["ck"] = ["rahip", "kardinal"][rs.randint(2)]
                    u["prop"] = ["book", "cross", None][rs.randint(3)]
                else:
                    u["ck"] = ["halk", "denizci", "tuccar"][rs.randint(3)]
                    if rs.rand() < 0.3:
                        u["prop"] = ["sack", "basket"][rs.randint(2)]
            cast.append(u)
            x += rs.uniform(*R["gap"]) / max(0.3, density) * (1.15 if cat == "rider" else 1.0)
    return cast


_TUFT = {}


def _tuft_sprite(sz, seed):
    key = (int(sz), seed)
    if key not in _TUFT:
        fr = sk.Frame(int(sz * 1.5) + 8, int(sz * 1.2) + 8)
        fr.clear(skia.ColorTRANSPARENT)
        rs = np.random.RandomState(seed)
        cx_, by = fr.w / 2, fr.h - 4
        for i in range(9):
            a = rs.uniform(-0.55, 0.55)
            L = sz * rs.uniform(0.55, 1.05)
            col = ["#3E5A2C", "#5A7A3A", "#4A6A32", "#6E8A44"][rs.randint(4)]
            p = skia.Path()
            p.moveTo(cx_ + rs.uniform(-4, 4), by)
            p.quadTo(cx_ + a * L * 0.5, by - L * 0.6, cx_ + a * L, by - L)
            fr.c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.4, sz * 0.045), Color=C(col, 235), StrokeCap=skia.Paint.kRound_Cap))
        if rs.rand() < 0.6:
            fx, fy = cx_ + rs.uniform(-sz * 0.3, sz * 0.3), by - sz * rs.uniform(0.35, 0.8)
            col = ["#F4EEDC", "#D8483A", "#E8B93A", "#6E7FD0"][rs.randint(4)]
            fr.c.drawCircle(fx, fy, max(2.0, sz * 0.07), skia.Paint(AntiAlias=True, Color=C(col)))
            fr.c.drawCircle(fx, fy, max(2.0, sz * 0.07), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#2A1A0C", 140)))
        _TUFT[key] = (fr.surf.makeImageSnapshot(), fr.w, fr.h)
    return _TUFT[key]


def _grass_row(f, y, sz, scroll, seed, alpha=1.0, spacing=150, night=False):
    """Zemin referansı: sıra hızında kayan çimen/çiçek öbekleri (ayak kayması hissini yok eder)."""
    c = f.c
    img0 = [_tuft_sprite(sz, seed + k) for k in range(4)]
    n = int(W / spacing) + 4
    off = scroll % spacing
    pt = skia.Paint(AntiAlias=False)
    if alpha < 1.0:
        pt.setAlphaf(alpha)
    for i in range(-1, n):
        idx = int(math.floor((i * spacing - 0 + scroll) / spacing))
        rs_ = ((idx * 2654435761) & 0xFFFF) / 65535.0
        x = i * spacing - off + (rs_ - 0.5) * spacing * 0.7
        im, w_, h_ = img0[idx % 4]
        c.drawImage(im, x - w_ / 2, y - h_ + 4 + (rs_ * 12 - 4) * (sz / 40.0), LIN, pt)


_PUFF = {}


def _puff(c, x, y, r, a, col="#CDB98E"):
    img = CM._dot()
    pt = skia.Paint(AntiAlias=True, ColorFilter=skia.ColorFilters.Blend(C(col), skia.BlendMode.kSrcIn))
    pt.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeWH(48, 48), skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), LIN, pt)


def procession(f, t, cast, dirn=1, speed=120.0, rows=None, total=None, ease=(0.0, 0.0), y_off=0.0, alpha=1.0, grass=True, dust=True, night=False, cull=520):
    """Alayı çiz: `cast` = procession_cast(...). Sıralar arkadan öne, her sıra kendi zemin hızında (paralaks). speed = kamera yan kayma hızı (px/sn).
    Dönüş: çizilen birim sayısı. (x ekranı: X0 + dirn·(w·t − g·E(t)); yürüyüş hızı zemine göre w)."""
    rows = rows or ROW_DEF
    E = _smooth_ease_int(t, ease[0], ease[1], total or 1e9)
    n_drawn = 0
    for ri, R in enumerate(rows):
        g = speed * R["g"]
        scroll = g * E
        sz = R["h"][1] * 0.11
        if grass:
            _grass_row(f, R["y"] + y_off + 6, sz, dirn * scroll, seed=ri * 17 + 3, alpha=0.95, spacing=int(R["h"][1] * 0.62), night=night)
        units = [u for u in cast if u["row"] == ri]
        units.sort(key=lambda u: u["y"])
        for u in units:
            w = speed * u["wk"]
            xs = u["x0"] + dirn * (w * t - scroll)
            if xs < -cull or xs > W + cull:
                continue
            yy = u["y"] + y_off
            if u["kind"] == "rider":
                prop = None
                if u.get("banner"):
                    dev, c1, c2 = u["banner"]
                    prop = _rider_banner(dev, c1, c2, t)
                rider(f, xs, yy, u["h"], t, speed=w, gait=u["gait"], dir=dirn, seed=u["seed"], phase=u["phase"], alpha=alpha, prop=prop)
                if dust and u["gait"] != "walk":
                    _rider_dust(f, u, t, xs, yy, w, dirn, g, E)
            else:
                walker(f, u["ck"], xs, yy, u["h"], t, speed=w, dir=dirn, phase=u["phase"], seed=u["seed"], alpha=alpha, prop=u.get("prop"), flag=((u["flag"][0], 0.60, 0.42, u["flag"][1], u["flag"][2]) if u.get("flag") else None))
            n_drawn += 1
    return n_drawn


def _rider_banner(dev, c1, c2, T):
    def prop(c, hk):
        u = hk.u
        hand = (0.31 * u, -0.27 * u)
        spr = prop_sprite("pole", int(round(u * 2.2)), "#6A4A2C", GOLD)
        c.save()
        c.translate(hand[0], hand[1])
        c.rotate(-4.0 + 2.0 * math.sin(T * 2.0))
        c.drawImage(spr.img, -spr.ox, -spr.oy, LIN)
        c.restore()
        hb = u * 2.2
        top = (hand[0] + 0.98 * hb * math.sin(math.radians(-4.0)), hand[1] - 0.98 * hb)
        _flag_fn(top, hb, T, (dev, 0.55, 0.40, c1, c2), 0.6)(c)
    return prop


def _rider_dust(f, u, t, xs, yy, w, dirn, g, E):
    """Toynak temaslarında yerde kalan (zemin çerçevesine bağlı) toz öbekleri."""
    gaitd = GAIT[u["gait"]]
    A, beta = gaitd["A"], gaitd["beta"]
    S = 2 * A / beta
    hs = u["h"] / 1.2
    fcyc = (w / hs) / S if w > 1e-3 else 0.0
    if fcyc <= 0:
        return
    for leg, ph in gaitd["ph"].items():
        if leg not in ("hn", "fn"):
            continue
        k0 = math.floor(t * fcyc + ph + u["phase"])
        for k in (k0, k0 - 1):
            te = (k - ph - u["phase"]) / fcyc
            age = t - te
            if 0.0 <= age < 1.0:
                rest = FORE_REST if leg[0] == "f" else HIND_REST
                gp = (rest[0][0] + A) * hs
                xp = u["x0"] + dirn * (w * te + gp) - dirn * g * E
                _puff(f.c, xp, yy - 2 - 16 * age, hs * (0.05 + 0.10 * age), 0.38 * (1 - age) ** 1.3)


# ═════════════════════════════ atmosfer yardımcıları (pano/yapım ile ortak) ═════════════════════════════
def atmo_birds(c, t, n, a, x0=0, x1=W, y0=300, y1=500, speed=26.0, night=False, seed=1, size=1.0, col="#2A1A0C"):
    """Kanat çırpan kuşlar (V çizgisi): sürü halinde akar. (x0..x1, y0..y1) bölgesinde."""
    if night:
        return
    rs = np.random.RandomState(seed * 31 + 7)
    Wd = (x1 - x0) + 360
    for i in range(n):
        sp_ = speed * (0.8 + 0.5 * rs.rand())
        bx = x0 - 180 + (rs.rand() * Wd + t * sp_) % Wd
        by = y0 + (y1 - y0) * rs.rand() + math.sin(t * 0.7 + i * 1.9) * 16
        fl = math.sin(t * 10.0 + i * 2.3 + rs.rand() * 6) * 5.5
        s = (0.7 + 0.5 * rs.rand()) * size
        pth = skia.Path()
        pth.moveTo(bx - 9 * s, by + fl * s * 0.4)
        pth.quadTo(bx - 4 * s, by - 4 * s - fl * s, bx, by)
        pth.quadTo(bx + 4 * s, by - 4 * s - fl * s, bx + 9 * s, by + fl * s * 0.4)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0 * s, Color=C(col, int(190 * a)), StrokeCap=skia.Paint.kRound_Cap))


# ═════════════════════════════ `procession` çekim türü ═════════════════════════════
BAND_Y, BAND_H = 172, 680
_VINE = {}


def vine_band(f, y, alpha=1.0, x0=-40, x1=W + 40):
    """Asma bandı (ORN.band_vine) — bir kez pişirilir, kare başına tek blit (≈10 ms tasarruf)."""
    import cilt_orn as ORN
    key = (int(x1 - x0), 40)
    img = _VINE.get(key)
    if img is None:
        fr = sk.Frame(int(x1 - x0), 40)
        fr.clear(skia.ColorTRANSPARENT)
        ORN.band_vine(fr, 0, 0, int(x1 - x0), 40)
        img = _VINE[key] = fr.surf.makeImageSnapshot()
    pt = skia.Paint()
    if alpha < 1.0:
        pt.setAlphaf(clamp(alpha))
    f.c.drawImage(img, x0, y, skia.SamplingOptions(), pt)


def _pan_args(pan, speed, dur, dir_):
    """pan: None | px/sn | 'r'|'l' | ('r'|'l', toplam_px) | ('pan','r',px)."""
    dirn = 1 if dir_ in (1, "r", "R") else -1
    sp = speed
    if pan is not None:
        if isinstance(pan, (int, float)):
            sp = abs(float(pan))
            dirn = 1 if pan >= 0 else -1 if dir_ in (None,) else dirn
        elif isinstance(pan, str):
            dirn = 1 if pan.lower().startswith("r") else -1
        elif isinstance(pan, (tuple, list)):
            tt = list(pan)
            if tt and tt[0] == "pan":
                tt = tt[1:]
            if tt and isinstance(tt[0], str):
                dirn = 1 if tt[0].lower().startswith("r") else -1
                if len(tt) > 1:
                    sp = abs(float(tt[1])) / max(1.0, dur)
            elif tt:
                sp = abs(float(tt[0]))
    return dirn, sp


def _install_procession():
    import cilt_orn as ORN
    import cilt_scene as SC
    from cilt_medici import TH, ckind

    @ckind("procession")
    def k_procession(cx, seed=1, dir="r", density=1.0, mix=None, speed=125.0, pan=None, kick=None, caption=None, at=0.0, x0=0.0, ease=(0.9, 0.9), tod=None, rows=None, birds=5, dust=True, **_):
        """Gozzoli "Magi alayı" üslubunda KESİNTİSİZ, gerçekten yürüyen friz: sancaktarlar, atlılar (yürüyüş/tırıs; toz), pajlar, muhafızlar, ağır cübbeliler.
        3 derinlik sırası (her sıra kendi zemin hızında), arka plan peyzajı paralaks (gökyüzü 0,45 · tepe/ağaç 0,85), yön dir='r'|'l' (Medici yükselişi = r).
        density: yoğunluk; mix: dict(rider, noble, page, banner, guard, elder, cleric, common) ağırlıkları; speed/pan: kamera yan kayma (px/sn | 'r' | ('r', toplam_px));
        cam/link/longtake/montage parametreleri kabul edilir ve yok sayılır."""
        f = cx.f
        night = not TH.day
        mode = "night" if night else "day"
        dirn, spd = _pan_args(pan, speed, cx.dur, dir)
        cam = CM.Cam(cx, push=0.02, drift=(0.0, 2.0))
        CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
        cam.begin(f)
        c = f.c
        travel = int(spd * (cx.dur + 3) * 1.0 + 200)
        wsky = W + int(0.45 * travel) + 40
        wmid = W + int(0.85 * travel) + 40
        wsky = int(math.ceil(wsky / 400.0) * 400)
        wmid = int(math.ceil(wmid / 400.0) * 400)
        sky = SC.sky_layer(wsky, BAND_H, seed, mode)
        mid = SC.mid_layer(wmid, BAND_H, seed + 1, mode)
        t = cx.t
        E = _smooth_ease_int(t, ease[0], ease[1], cx.dur)
        a = cx.amt(at, 0.8)
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(0, BAND_Y, W, BAND_Y + BAND_H))
        p = skia.Paint(AntiAlias=False)
        p.setAlphaf(a)
        so = x0 + spd * 0.45 * E
        mo = x0 + spd * 0.85 * E
        if dirn > 0:
            c.drawImage(sky, -so, BAND_Y, CM._LIN, p)
            c.drawImage(mid, -mo, BAND_Y, CM._LIN, p)
        else:
            c.drawImage(sky, -(wsky - W) + so, BAND_Y, CM._LIN, p)
            c.drawImage(mid, -(wmid - W) + mo, BAND_Y, CM._LIN, p)
        atmo_birds(c, t, birds, a, 0, W, BAND_Y + 40, BAND_Y + 190, speed=30.0 * dirn if dirn > 0 else 30.0, night=night, seed=seed)
        cast = _cast_cache(seed, dirn, float(density), tuple(sorted((mix or {}).items())))
        procession(f, t, cast, dirn, spd, rows=None, total=cx.dur, ease=ease, y_off=BAND_Y, alpha=a, dust=dust, night=night)
        c.restore()
        for yy in (BAND_Y - 40, BAND_Y + BAND_H):
            vine_band(f, yy, a)
            c.drawLine(-40, yy + (40 if yy < BAND_Y else 0), W + 40, yy + (40 if yy < BAND_Y else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a))
        if kick:
            CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
        if caption:
            wd = sk.text_width(caption, "cap_i", 40) + 90
            CM.tablet(f, 90, BAND_Y + BAND_H + 54 - 4, wd, 66, alpha=cx.amt(at + 0.8, 0.7), corner=8)
            CM.ink(f, caption, 90 + wd / 2, BAND_Y + BAND_H + 54 + 44, face="cap_i", size=40, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
        cam.end(f)
        CM.finish(f, cx, motes_n=26)
    return k_procession


@functools.lru_cache(maxsize=8)
def _cast_cache(seed, dirn, density, mixt):
    return procession_cast(seed, dirn, density, dict(mixt) if mixt else None)


try:
    _install_procession()
except Exception as _e:         # pragma: no cover — cilt_medici/shots yüklenirken döngüsel içe aktarma ise sessiz kal
    import sys as _sys
    print("[uyarı] procession kaydı:", _e, file=_sys.stderr)
