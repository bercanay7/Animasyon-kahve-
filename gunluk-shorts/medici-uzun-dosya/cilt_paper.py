"""cilt_paper — Medici cildi: kâğıt/parşömen ve defter (ledger) yüzeyleri.

paper_image(...): lifli, lekeli (foxing), kenarı yıpranmış/deckle/yırtık kâğıt sprite'ı (RGBA, yerel biçimli skia.Image) + alfa (gölge için).
ledger_spread(...): açık defter (iki sayfa): deri cilt kenarı, sayfa kalınlığı çizgileri, ortada sırt gölgesi, satır cetveli (kahve), kırmızı (sinabar) çift dikey çizgiler,
                    başlıklar (DEBITORI / CREDITORI), sayfa tanesi. Statik kısım bir kez pişer; satır yazıları çekim içinde çizilir.
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import sk
from sk import C, Frame, H, W, clamp, mix

PIG = CM.PIG


def _fibers(rs, h, w, density=1100.0, amp=1.0):
    fib = np.zeros((h, w), np.uint8)
    n = int(w * h / density)
    for _ in range(n):
        x, y = rs.randint(0, w), rs.randint(0, h)
        L = rs.randint(6, 26)
        a = rs.uniform(0, math.pi)
        cv2.line(fib, (x, y), (int(x + math.cos(a) * L), int(y + math.sin(a) * L)), int(rs.randint(40, 120) * amp), 1, cv2.LINE_AA)
    return cv2.GaussianBlur(fib.astype(np.float32) / 255.0, (0, 0), 0.7)


def _edge_alpha(rs, w, h, pad, edge):
    """Kenar maskesi (0..1, (h+2pad, w+2pad)): cut (düz), deckle (ince tırtıklı), torn (yırtık)."""
    H_, W_ = h + 2 * pad, w + 2 * pad
    m = np.zeros((H_, W_), np.uint8)
    amp1, amp2 = {"cut": (0.0, 0.4), "deckle": (1.6, 0.8), "torn": (4.5, 1.8)}[edge]
    pts = []
    n = max(40, (w + h) // 6)
    per = []
    for i in range(n):
        per.append((pad + w * i / n, pad))
    for i in range(n // 2):
        per.append((pad + w, pad + h * i / (n // 2)))
    for i in range(n):
        per.append((pad + w - w * i / n, pad + h))
    for i in range(n // 2):
        per.append((pad, pad + h - h * i / (n // 2)))
    k = len(per)
    lowf = np.cumsum(rs.normal(0, 0.55, k))
    lowf = lowf - np.linspace(lowf[0], lowf[-1], k)          # kapalı döngü
    lowf = np.clip(lowf, -3.5 * amp1 - 1, 3.5 * amp1 + 1)
    for i, (x, y) in enumerate(per):
        pts.append((x + rs.randn() * amp2 + (lowf[i] * (0.6 if y in (pad, pad + h) else 0.0)) * (1 if amp1 else 0),
                    y + rs.randn() * amp2 + (lowf[i] * (0.6 if x in (pad, pad + w) else 0.0)) * (1 if amp1 else 0)))
    cv2.fillPoly(m, [np.array(pts, np.int32)], 255, cv2.LINE_AA)
    return m.astype(np.float32) / 255.0


class Paper:
    __slots__ = ("img", "alpha", "w", "h", "pad", "_sh")

    def __init__(self, img, alpha, w, h, pad):
        self.img, self.alpha, self.w, self.h, self.pad, self._sh = img, alpha, w, h, pad, None

    def shadow(self):
        if self._sh is None:
            self._sh = CM.blur_sil((self.alpha * 255).astype(np.uint8), 11.0, (20, 12, 4))
        return self._sh

    def draw(self, f, cx, cy, rot=0.0, scale=1.0, alpha=1.0, shadow=0.55, off=(0, 0)):
        """Merkez (cx,cy). Gölge sağ-alt."""
        c = f.c
        c.save()
        c.translate(cx, cy)
        if rot:
            c.rotate(math.degrees(rot))
        c.scale(scale, scale)
        if shadow > 0:
            p = skia.Paint(AntiAlias=True)
            p.setAlphaf(clamp(shadow * alpha))
            c.drawImage(self.shadow(), -self.w / 2 - self.pad + 9, -self.h / 2 - self.pad + 14, CM._LIN, p)
        p = skia.Paint(AntiAlias=True)
        p.setAlphaf(clamp(alpha))
        c.drawImage(self.img, -self.w / 2 - self.pad, -self.h / 2 - self.pad, CM._LIN, p)
        c.restore()


@functools.lru_cache(maxsize=24)
def paper_image(w, h, seed=3, tone=(233, 222, 190), edge="deckle", folds=(), pad=44, wear=1.0):
    """Kâğıt/parşömen: tone=(r,g,b). folds: [('v',0..1),('h',0..1)] katlanma izleri. wear: yıpranma şiddeti."""
    rs = np.random.RandomState(seed)
    H_, W_ = h + 2 * pad, w + 2 * pad
    fib = _fibers(rs, H_, W_)
    base = np.empty((H_, W_, 3), np.float32)
    base[:] = np.array(tone, np.float32)
    t = 0.030 * CW.lf(rs, H_, W_, 90) + 0.020 * CW.lf(rs, H_, W_, 26) + 0.05 * (fib - fib.mean()) + 0.012 * CW.gn(rs, H_, W_, 1.0)
    base *= (1 + t)[..., None]
    # lekeler (foxing)
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    fox = np.zeros((H_, W_), np.float32)
    for _ in range(int(26 * wear)):
        x, y = rs.uniform(0, W_), rs.uniform(0, H_)
        r = rs.uniform(3, 14)
        fox = np.maximum(fox, np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (2 * (r * 0.55) ** 2))) * rs.uniform(0.12, 0.34))
    stain_c = np.array([150, 112, 62], np.float32)
    base = base * (1 - fox[..., None]) + stain_c * fox[..., None]
    for _ in range(int(2 * wear)):
        x, y, r = rs.uniform(0, W_), rs.uniform(0, H_), rs.uniform(110, 260)
        st = np.exp(-(((xx - x) ** 2 + (yy - y) ** 2) / (2 * r ** 2))) * rs.uniform(0.05, 0.12) * wear
        base = base * (1 - st[..., None]) + stain_c * 0.9 * st[..., None]
    am = _edge_alpha(rs, w, h, pad, edge)
    dist = cv2.distanceTransform((am > 0.5).astype(np.uint8), cv2.DIST_L2, 3)
    edge_dark = np.clip(1 - dist / 26.0, 0, 1) ** 1.6
    base = base * (1 - 0.20 * wear * edge_dark[..., None]) + np.array([120, 84, 40], np.float32) * 0.20 * wear * edge_dark[..., None] * 0.35
    # katlanma izleri
    for kind, pos in folds:
        if kind == "v":
            x0 = pad + w * pos
            d = (xx - x0 + 2.5 * np.sin(yy / 61.0))
            base *= (1 - 0.14 * np.exp(-(d / 2.2) ** 2))[..., None]
            base *= (1 + 0.07 * np.exp(-((d - 3.0) / 2.4) ** 2))[..., None]
            base *= (1 - 0.05 * np.clip(-d / 90.0, 0, 1) * np.clip(1 + d / 90.0, 0, 1))[..., None]
        else:
            y0 = pad + h * pos
            d = (yy - y0 + 2.5 * np.sin(xx / 71.0))
            base *= (1 - 0.14 * np.exp(-(d / 2.2) ** 2))[..., None]
            base *= (1 + 0.07 * np.exp(-((d - 3.0) / 2.4) ** 2))[..., None]
    # ince tooth (kâğıt yüzeyi)
    sh = CM._shade_map(CW.gn(rs, H_, W_, 1.1) * 0.5 + fib * 0.6)
    sh = sh / (np.abs(sh).std() + 1e-6)
    base *= (1 + 0.016 * sh)[..., None]
    arr = np.dstack([np.clip(base, 0, 255), am * 255]).astype(np.uint8)
    return Paper(sk.np_to_image(arr), am, w, h, pad)


# ───────────────────────────── DEFTER (açık, iki sayfa) ─────────────────────────────
LED_W, LED_H = 1560, 900
LED_PAD = 36
ROW0, ROWH = 226, 60          # satır başlangıcı ve aralık (sayfa içi y)
NROWS = 10


AMT_COLS = (122, 72, 78)          # f., s., d. sütun genişlikleri
AMT_TOT = sum(AMT_COLS)
LAB_MIN = 36                       # etiket küçültme tabanı (px); tavsiye: etiket ≤ ~20 karakter


def amt_cols(x1):
    """Sayfa sağ kenarı x1 için tutar sütunları: (amt_x0, [sağa hizalı x'ler], [kırmızı çizgi x'leri])."""
    a0 = x1 - 36 - AMT_TOT
    return a0, [a0 + AMT_COLS[0] - 10, a0 + AMT_COLS[0] + AMT_COLS[1] - 10, a0 + AMT_TOT - 10], [a0, a0 + AMT_COLS[0], a0 + AMT_COLS[0] + AMT_COLS[1]]


def led_layout():
    """Sayfa geometrisi: (sol sayfa x0,x1; sağ sayfa x0,x1; satır sütunları)."""
    pg_w = (LED_W - 2 * 30) / 2
    L0, L1 = 30, 30 + pg_w
    R0, R1 = L1, LED_W - 30
    return dict(L0=L0, L1=L1, R0=R0, R1=R1)


@functools.lru_cache(maxsize=8)
def ledger_spread(seed=5, tone=(236, 224, 192), title_l="DEBITORI", title_r="CREDITORI", head="", cols=("f.", "s.", "d."), rows=NROWS):
    """Açık defter görüntüsü (Skia yerel). Dönüş: skia.Image (LED_W+2·LED_PAD × LED_H+2·LED_PAD) + alfa dizisi."""
    pad = LED_PAD
    w, h = LED_W, LED_H
    rs = np.random.RandomState(seed)
    fr = Frame(w + 2 * pad, h + 2 * pad)
    fr.clear(skia.ColorTRANSPARENT)
    c = fr.c
    # deri cilt (sayfaların altında, kenarda 22 px görünür)
    leather = skia.Path()
    leather.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(pad - 4, pad - 4, w + 8, h + 8), 12, 12))
    c.drawPath(leather, skia.Paint(AntiAlias=True, Color=C("#000000", 130), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)))
    lt = CW.lf(rs, h + 8, w + 8, 40) * 0.07 + CW.gn(rs, h + 8, w + 8, 1.4) * 0.05
    larr = np.empty((h + 8, w + 8, 3), np.float32)
    larr[:] = np.array([74, 44, 26], np.float32)
    larr *= (1 + lt)[..., None]
    c.drawImage(sk.np_to_image(np.dstack([np.clip(larr, 0, 255), np.full((h + 8, w + 8), 255, np.float32)]).astype(np.uint8)), pad - 4, pad - 4)
    # sayfa kalınlığı: dış kenarlarda ince çizgiler
    lay = led_layout()
    for k in range(7):
        o = 4 + k * 2.2
        a = 150 - k * 14
        for (x0, x1, side) in ((lay["L0"], lay["L1"], -1), (lay["R0"], lay["R1"], 1)):
            xo = pad + (x0 - o) if side < 0 else pad + (x1 + o)
            c.drawLine(xo, pad + 14 + k * 1.5, xo, pad + h - 14 - k * 1.2, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#C9B98E" if k % 2 == 0 else "#8A7650", a)))
    # iki sayfa (kâğıt dokulu)
    pw = lay["L1"] - lay["L0"]
    pph = h - 56
    for (x0, side) in ((lay["L0"], -1), (lay["R0"], 1)):
        pp = paper_image(int(pw), int(pph), seed + (0 if side < 0 else 1), tone, "cut", (), 0, 0.9)
        c.drawImage(pp.img, pad + x0, pad + 28)
    # sırt gölgesi (ortada)
    mx = pad + lay["L1"]
    sh = skia.GradientShader.MakeLinear([(mx - 120, 0), (mx, 0)], [C("#2A1A08", 0), C("#2A1A08", 120)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(mx - 120, pad + 28, mx, pad + h - 28), skia.Paint(Shader=sh))
    sh2 = skia.GradientShader.MakeLinear([(mx, 0), (mx + 120, 0)], [C("#2A1A08", 130), C("#2A1A08", 0)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(mx, pad + 28, mx + 120, pad + h - 28), skia.Paint(Shader=sh2))
    c.drawRect(skia.Rect.MakeLTRB(mx - 2, pad + 28, mx + 2, pad + h - 28), skia.Paint(Color=C("#1A1006", 190)))
    # cetvel: satır çizgileri + sinabar çift dikey çizgiler
    ink = "#5A3E22"
    red = "#A8321E"
    for (x0, x1, side) in ((lay["L0"], lay["L1"], -1), (lay["R0"], lay["R1"], 1)):
        for i in range(rows + 1):
            y = pad + ROW0 + i * ROWH
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(ink, 92))
            p.setPathEffect(skia.DiscretePathEffect.Make(18.0, 0.8, i * 3 + (0 if side < 0 else 1)))
            c.drawLine(pad + x0 + 36, y, pad + x1 - 36, y, p)
        # kırmızı dikey çizgiler: sol kenar boşluğu + tutar sütunları
        xs = [x0 + 52] if side < 0 else [x0 + 36]
        amt_x0, _rights, _rules = amt_cols(x1)
        for xr in (xs[0], *_rules):
            for dd in (0, 5):
                p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C(red, 150))
                p.setPathEffect(skia.DiscretePathEffect.Make(26.0, 0.7, int(xr) % 9))
                c.drawLine(pad + xr + dd, pad + ROW0 - 52, pad + xr + dd, pad + ROW0 + rows * ROWH + 20, p)
        # üst başlık
        tt = title_l if side < 0 else title_r
        sp = CM.engraved(tt, "title_m", 36, 10.0, "#3A2616", 0.6)
        CM.draw_spr(fr, sp, pad + (x0 + x1) / 2, pad + 142, "c", alpha=0.92)
        for k, cl in enumerate(cols):
            cx_ = pad + _rights[k] - 20
            fr.text(cl, cx_, pad + ROW0 - 22, face="cap_b", size=28, color="#7A3A1E", align="c", alpha=0.9)
    if head:
        sp = CM.painted(head, "title", 44, 8.0, "#8E2A1A", 1.0, 4)
        CM.draw_spr(fr, sp, pad + lay["L0"] + 70, pad + 84, "l", alpha=0.95)
    # sayfa kenarı koyulması
    for (x0, x1) in ((lay["L0"], lay["L1"]), (lay["R0"], lay["R1"])):
        edge = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, Color=C("#6A4A22", 46), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        c.save()
        c.clipRect(skia.Rect.MakeLTRB(pad + x0, pad + 28, pad + x1, pad + h - 28))
        c.drawRect(skia.Rect.MakeLTRB(pad + x0, pad + 28, pad + x1, pad + h - 28), edge)
        c.restore()
    img = fr.surf.makeImageSnapshot()
    alpha = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8)
    alpha[pad - 4:pad + h + 4, pad - 4:pad + w + 4] = 255
    return img, alpha


def hand(f, text, x, y, face="fell_i", size=44, color="#2A1A0E", alpha=1.0, jitter=1.2, seed=0, align="l", track=0.0):
    """El yazısı hissi: sözcükler ayrı çizilir, taban çizgisi ve eğim hafif oynar. Dönüş: toplam genişlik."""
    words = text.split(" ")
    sp_w = sk.text_width(" ", face, size, track)
    total = sk.text_width(text, face, size, track)
    xo = x - (total / 2 if align == "c" else total if align == "r" else 0)
    rs = np.random.RandomState(seed)
    cx = xo
    c = f.c
    for w_ in words:
        dy = rs.normal(0, jitter)
        rot = rs.normal(0, 0.012)
        ww = sk.text_width(w_, face, size, track)
        c.save()
        c.translate(cx, y + dy)
        c.rotate(math.degrees(rot))
        blob, _ = sk.text_blob(face, w_, size, track)
        c.drawTextBlob(blob, 0, 0, f.paint(color, alpha=alpha))
        c.restore()
        cx += ww + sp_w
    return total
