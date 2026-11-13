"""figs_kit — kâğıt-kesim siluet figür araç takımı (figür-lab).

Hepsi saf geometri + küçük bir "Fig" çizim listesi: yollar (skia.Path) oluşturulur, `Fig.build()` → (sınır_yolu, çiz(canvas,col,rim)).
Sprite önbelleklidir (stage._fig_sprite): maliyet figx kurulumunda/ilk çizimde ödenir, kare başına yalnız blit.

Koordinatlar: ayak (0,0), yukarı −y, birim = piksel (figx(h, lean) h verir).  Baş birimi ("hu"): baş yüksekliği 1, merkez (0,0),
yüz +x'e bakar (3/4 profil).  `place(path, x, y, s, rot, flip)` baş-birimli yolları figür koordinatına yerleştirir.
Işık: sol-üst → kenar ışığı (rim) sol/üst kenarlarda, her parçanın kendi "kâğıt katmanı" kenarında.
"""
import math

import skia

from sk import C, mix

# ───────────────────────────── geometri ─────────────────────────────


def K(x, y):
    """Köşe noktası (spline'da keskin)."""
    return (x, y, "c")


def sp(pts, closed=True, k=1.0):
    """Köşe destekli yumuşak spline (Bezier, tutamaç = kiriş/3·k). Noktalar: (x,y) yumuşak, K(x,y) köşe."""
    P = [(float(p[0]), float(p[1])) for p in pts]
    cor = [len(p) > 2 for p in pts]
    n = len(P)
    path = skia.Path()
    path.moveTo(*P[0])
    nseg = n if closed else n - 1
    for i in range(nseg):
        j = (i + 1) % n
        dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        cx_, cy_ = dx / L, dy / L
        if cor[i] or (not closed and i == 0):
            ti = (cx_, cy_)
        else:
            a, b = P[(i - 1) % n], P[j]
            ux, uy = b[0] - a[0], b[1] - a[1]
            ul = math.hypot(ux, uy)
            ti = (ux / ul, uy / ul) if ul > 1e-9 else (cx_, cy_)
        if cor[j] or (not closed and j == n - 1):
            tj = (cx_, cy_)
        else:
            a, b = P[i], P[(j + 1) % n]
            ux, uy = b[0] - a[0], b[1] - a[1]
            ul = math.hypot(ux, uy)
            tj = (ux / ul, uy / ul) if ul > 1e-9 else (cx_, cy_)
        hl = L * k / 3.0
        path.cubicTo(P[i][0] + ti[0] * hl, P[i][1] + ti[1] * hl, P[j][0] - tj[0] * hl, P[j][1] - tj[1] * hl, P[j][0], P[j][1])
    if closed:
        path.close()
    return path


def poly(pts, closed=True):
    p = skia.Path()
    p.moveTo(float(pts[0][0]), float(pts[0][1]))
    for q in pts[1:]:
        p.lineTo(float(q[0]), float(q[1]))
    if closed:
        p.close()
    return p


def place(path, x=0.0, y=0.0, s=1.0, rot=0.0, flip=False, ox=0.0, oy=0.0):
    """Yolun kopyası: yerel (ox,oy) noktası (x,y)'ye gelir; önce ölçek (flip→x aynası), sonra döndürme (derece), sonra taşıma."""
    q = skia.Path(path)
    m = skia.Matrix()
    m.setTranslate(-ox, -oy)
    m.postScale(-s if flip else s, s)
    if rot:
        m.postRotate(rot)
    m.postTranslate(x, y)
    q.transform(m)
    return q


def ell(cx, cy, rx, ry, rot=0.0):
    p = skia.Path()
    p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry))
    if rot:
        m = skia.Matrix()
        m.setRotate(rot, cx, cy)
        p.transform(m)
    return p


def union(*paths):
    out = skia.Path()
    for p in paths:
        out.addPath(p)
    return out


def lens(p0, p1, w, bend=0.0):
    """İnce mercek (kıvrım çizgisi): p0→p1, orta genişlik w, kiriş normali yönünde bend kadar eğri."""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    mx, my = (x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend
    p = skia.Path()
    p.moveTo(x0, y0)
    p.quadTo(mx + nx * w, my + ny * w, x1, y1)
    p.quadTo(mx - nx * w, my - ny * w, x0, y0)
    p.close()
    return p


def bar(x0, y0, x1, y1, w0, w1=None, r0=False, r1=False):
    """Konik çubuk (sopa/mızrak/kılıç gövdesi). r0/r1: uçlarda yuvarlak başlık."""
    w1 = w0 if w1 is None else w1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    p = poly([(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)])
    if r0:
        p.addOval(skia.Rect.MakeLTRB(x0 - w0 / 2, y0 - w0 / 2, x0 + w0 / 2, y0 + w0 / 2))
    if r1:
        p.addOval(skia.Rect.MakeLTRB(x1 - w1 / 2, y1 - w1 / 2, x1 + w1 / 2, y1 + w1 / 2))
    return p


def limb(P, W, cap0=0.5, cap1=0.5, k=1.0):
    """Kol/bacak/kıvrımlı gövde parçası: P=[(x,y)…] omurga, W=[genişlik…]; uç başlığı cap (0 = düz kesim, 0.5 = yuvarlak)."""
    n = len(P)
    Lp, Rp = [], []
    for i in range(n):
        if i == 0:
            tx, ty = P[1][0] - P[0][0], P[1][1] - P[0][1]
        elif i == n - 1:
            tx, ty = P[-1][0] - P[-2][0], P[-1][1] - P[-2][1]
        else:
            tx, ty = P[i + 1][0] - P[i - 1][0], P[i + 1][1] - P[i - 1][1]
        tl = math.hypot(tx, ty) or 1.0
        tx, ty = tx / tl, ty / tl
        nx, ny = -ty, tx
        w = W[i] / 2
        Lp.append((P[i][0] + nx * w, P[i][1] + ny * w, "c") if (i in (0, n - 1) and False) else (P[i][0] + nx * w, P[i][1] + ny * w))
        Rp.append((P[i][0] - nx * w, P[i][1] - ny * w))
    pts = []
    t0 = (P[1][0] - P[0][0], P[1][1] - P[0][1])
    l0 = math.hypot(*t0) or 1.0
    t1 = (P[-1][0] - P[-2][0], P[-1][1] - P[-2][1])
    l1 = math.hypot(*t1) or 1.0
    for i in range(n):
        pts.append(K(*Lp[i]) if (i == n - 1 and cap1 == 0) else Lp[i])
    if cap1 > 0:
        pts.append((P[-1][0] + t1[0] / l1 * W[-1] * cap1, P[-1][1] + t1[1] / l1 * W[-1] * cap1))
    for i in range(n - 1, -1, -1):
        pts.append(K(*Rp[i]) if (i == n - 1 and cap1 == 0) or (i == 0 and cap0 == 0) else Rp[i])
    if cap0 > 0:
        pts.append((P[0][0] - t0[0] / l0 * W[0] * cap0, P[0][1] - t0[1] / l0 * W[0] * cap0))
    if cap0 == 0:
        pts[0] = K(*Lp[0])
    return sp(pts, True, k)


def arc_pts(cx, cy, rx, ry, a0, a1, n=8):
    """Elips yayı noktaları (derece; 0=sağ, 90=aşağı)."""
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        out.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return out


# ───────────────────────────── Fig: parça listesi + çizim ─────────────────────────────
class Fig:
    """Kâğıt-kesim figür: sıralı parçalar (arkadan öne). fill: koyu gövde + sol-üst kenar ışığı; kıvrım/çizgi/oyuk/düz renk."""

    def __init__(self, h, lean=0.0):
        self.h = float(h)
        self.ops = []
        self.bound = skia.Path()
        self.kx = -1.5 * lean

    # --- parça ekleme
    def fill(self, path, rim=1.0, tone=0.0, alpha=1.0, bound=True, glow=0.0):
        """Gövde parçası. rim: kenar ışığı gücü (0..1), tone: col→rim karışımı (0 koyu), glow: iç yumuşak ışıltı (sol kenardan)."""
        self.ops.append(("fill", path, rim, tone, alpha, glow))
        if bound:
            self.bound.addPath(path)
        return path

    def cut(self, path):
        """Negatif alan (kâğıt oyuğu): o ana kadar çizilenden siler."""
        self.ops.append(("cut", path))

    def line(self, path, width, tone=0.3, alpha=0.6, cap="round"):
        self.ops.append(("line", path, width, tone, alpha, cap))

    def solid(self, path, color, alpha=1.0, bound=False):
        self.ops.append(("solid", path, color, alpha))
        if bound:
            self.bound.addPath(path)

    def crease(self, p0, p1, w, bend=0.0, hi=True, alpha=0.62):
        """Kumaş kıvrımı: koyu-açık mercek + sol kenarda ince ışık."""
        self.fill(lens(p0, p1, w, bend), rim=0, tone=0.20, alpha=alpha, bound=False)
        if hi:
            d = w * 0.95
            self.fill(lens((p0[0] - d, p0[1]), (p1[0] - d, p1[1]), w * 0.42, bend), rim=0, tone=1.0, alpha=0.30, bound=False)

    def glowdot(self, x, y, r, color="#FFD58A", alpha=0.85, bound=False):
        """Parlama (toplamsal): mum/meşale alevi. bound=True ise sprite sınırına dahil edilir (halo kırpılmasın)."""
        self.ops.append(("glow", x, y, r, color, alpha))
        if bound:
            p = skia.Path()
            p.addCircle(x, y, r)
            self.bound.addPath(p)

    def merge(self, other, dx=0.0, dy=0.0, s=1.0, flip=False, rot=0.0):
        """Başka bir Fig'in parçalarını (ölçekle/ayna/döndür/taşı) bu Fig'e ekle (çiftler, atlı = at + binici). rot: derece (+ = saat yönü)."""
        m = skia.Matrix()
        m.setScale(-s if flip else s, s)
        if rot:
            m.postRotate(rot)
        m.postTranslate(dx, dy)

        def T(p):
            q = skia.Path(p)
            q.transform(m)
            return q
        for op in other.ops:
            k = op[0]
            if k == "fill":
                _, path, rs, tone, alpha, glow = op
                self.ops.append(("fill", T(path), rs, tone, alpha, glow))
            elif k == "cut":
                self.ops.append(("cut", T(op[1])))
            elif k == "line":
                _, path, wd, tone, alpha, cap = op
                self.ops.append(("line", T(path), wd * s, tone, alpha, cap))
            elif k == "solid":
                self.ops.append(("solid", T(op[1]), op[2], op[3]))
            elif k == "glow":
                _, x, y, r, color, alpha = op
                pt = m.mapXY(x, y)
                self.ops.append(("glow", pt.x(), pt.y(), r * s, color, alpha))
        self.bound.addPath(T(other.bound))

    # --- çıktı
    def build(self):
        b = skia.Path(self.bound)
        if self.kx:
            b.transform(self._mat())
        return b, self._draw

    def _mat(self):
        m = skia.Matrix()
        m.setAll(1, self.kx, 0, 0, 1, 0, 0, 0, 1)
        return m

    def _crescent(self, c, path, rim, w, rs, shader):
        """Kenar ışığı: parçanın kendisi ∖ (sağ-aşağı kaydırılmış kendisi) = sol-üst ince hilal. Katman (saveLayer) yerine çift kırpma (≈2× hızlı)."""
        c.save()
        c.clipPath(path, skia.ClipOp.kIntersect, True)
        off = skia.Path(path)
        off.offset(w * 1.05, w * 0.85)
        c.clipPath(off, skia.ClipOp.kDifference, True)
        p1 = skia.Paint(AntiAlias=True)
        p1.setShader(shader)
        if rs < 1.0:
            p1.setAlphaf(max(0.0, rs))
        c.drawPaint(p1)
        c.restore()

    def _draw(self, c, col, rim):
        h = self.h
        w = max(0.9, h * 0.0068)
        warm = rim or "#6A4A2A"
        shader = None
        if rim:
            shader = skia.GradientShader.MakeLinear([(0, -h), (0, 0)], [C(rim, 255), C(rim, 140)], [0.0, 1.0])
        self._dstout = skia.Paint(AntiAlias=True, Color=C("#000000"), BlendMode=skia.BlendMode.kDstOut)
        c.save()
        if self.kx:
            c.concat(self._mat())
        for op in self.ops:
            k = op[0]
            if k == "fill":
                _, path, rs, tone, alpha, glow = op
                cc = col if not tone else mix(col, warm, tone)
                p = skia.Paint(AntiAlias=True, Color=C(cc))
                if alpha < 1:
                    p.setAlphaf(alpha)
                c.drawPath(path, p)
                if glow > 0 and rim:
                    b = path.getBounds()
                    c.save()
                    c.clipPath(path, skia.ClipOp.kIntersect, True)
                    gp = skia.Paint(AntiAlias=True)
                    gp.setShader(skia.GradientShader.MakeLinear([(b.left(), 0), (b.left() + b.width() * 0.75, 0)], [C(rim, int(255 * glow)), C(rim, 0)], [0.0, 1.0]))
                    c.drawRect(b, gp)
                    c.restore()
                if rim and rs > 0:
                    self._crescent(c, path, rim, w, rs, shader)
            elif k == "cut":
                c.drawPath(op[1], skia.Paint(AntiAlias=True, BlendMode=skia.BlendMode.kClear))
            elif k == "line":
                _, path, wd, tone, alpha, cap = op
                p = skia.Paint(AntiAlias=True, Color=C(mix(col, warm, tone)))
                p.setStyle(skia.Paint.kStroke_Style)
                p.setStrokeWidth(max(0.8, wd))
                p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
                p.setStrokeJoin(skia.Paint.kRound_Join)
                if alpha < 1:
                    p.setAlphaf(alpha)
                c.drawPath(path, p)
            elif k == "solid":
                _, path, color, alpha = op
                p = skia.Paint(AntiAlias=True, Color=C(color))
                if alpha < 1:
                    p.setAlphaf(alpha)
                c.drawPath(path, p)
            elif k == "glow":
                _, x, y, r, color, alpha = op
                p = skia.Paint(AntiAlias=True)
                p.setShader(skia.GradientShader.MakeRadial((x, y), r, [C(color, int(255 * alpha)), C(color, int(255 * alpha * 0.35)), C(color, 0)], [0.0, 0.35, 1.0]))
                p.setBlendMode(skia.BlendMode.kPlus)
                c.drawCircle(x, y, r, p)
        c.restore()


# ───────────────────────────── baş profili (baş-birimi: yükseklik 1, merkez 0, yüz +x) ─────────────────────────────
# Yüz çizgisi x≈0.36. Gözler y≈-0.04, burun tabanı +0.165, ağız +0.255, çene alt +0.5.
_FACE_X = 0.36


def head_path(kind="m", nose=1.0, chin=0.0, brow=1.0, lip=1.0, bald=False):
    """Baş+yüz yolu (boyun hariç). kind: m (erkek), f (kadın), c (çocuk), o (yaşlı: çökük yanak, belirgin burun/çene)."""
    fx = _FACE_X

    def nz(x):
        return fx + (x - fx) * nose
    if kind == "f":
        pts = [(-0.30, 0.34), (-0.41, 0.12), (-0.45, -0.12), (-0.36, -0.36), (-0.12, -0.49), (0.12, -0.50), (0.29, -0.41), (0.345, -0.26),
               (0.36, -0.13), (0.345, -0.08), (nz(0.385), 0.02), (nz(0.45), 0.12), K(nz(0.385), 0.16), (0.395, 0.205), (0.375, 0.245),
               (0.39, 0.285), (0.35, 0.335), (0.36 + chin, 0.425), (0.30 + chin, 0.495), (0.12, 0.495), (-0.10, 0.40)]
    elif kind == "c":
        pts = [(-0.30, 0.34), (-0.43, 0.12), (-0.48, -0.14), (-0.38, -0.38), (-0.12, -0.50), (0.14, -0.50), (0.32, -0.40), (0.38, -0.22),
               (0.385, -0.10), (0.365, -0.05), (nz(0.395), 0.04), (nz(0.43), 0.10), K(nz(0.385), 0.135), (0.385, 0.18), (0.37, 0.22),
               (0.385, 0.255), (0.35, 0.30), (0.36 + chin, 0.40), (0.30 + chin, 0.485), (0.12, 0.49), (-0.10, 0.40)]
    elif kind == "o":
        pts = [(-0.30, 0.34), (-0.40, 0.12), (-0.45, -0.12), (-0.36, -0.36), (-0.12, -0.49), (0.12, -0.50), (0.29, -0.40), (0.345, -0.24),
               (0.38 * brow + 0.0, -0.13), (0.35, -0.065), (nz(0.405), 0.03), (nz(0.50), 0.15), K(nz(0.395), 0.175), (0.40, 0.215), (0.365, 0.26),
               (0.385, 0.295), (0.345, 0.345), (0.375 + chin, 0.43), (0.325 + chin, 0.50), (0.15, 0.49), (-0.10, 0.40)]
    else:
        pts = [(-0.30, 0.34), (-0.40, 0.12), (-0.45, -0.12), (-0.36, -0.36), (-0.12, -0.49), (0.12, -0.50), (0.30, -0.40), (0.355, -0.24),
               (0.375 * brow, -0.12), (0.35, -0.07), (nz(0.40), 0.03), (nz(0.485), 0.135), K(nz(0.40), 0.165), (0.41, 0.21 if lip > 0 else 0.2),
               (0.375, 0.255), (0.395, 0.295), (0.355, 0.345), (0.375 + chin, 0.43), (0.31 + chin, 0.50), (0.15, 0.50), (-0.10, 0.40)]
    return sp(pts, True)


def beard_path(kind="point", chin=0.0):
    """Sakal (baş-birimi). point: sivri kısa; short: kısa/bakımlı; full: gür uzun; stache: bıyık (yalnız)."""
    if kind == "stache":
        return sp([K(0.395, 0.165), (0.455, 0.205), (0.47, 0.235), (0.41, 0.245), (0.33, 0.232), K(0.34, 0.20)], True, 0.9)
    if kind == "short":
        return sp([(0.00, 0.10), (0.20, 0.22), (0.34, 0.285), (0.39 + chin, 0.37), (0.395 + chin, 0.47), (0.36 + chin, 0.58), (0.22, 0.60), (0.04, 0.50),
                   (-0.08, 0.36), (-0.12, 0.16)], True)
    if kind == "full":
        return sp([(-0.04, 0.02), (0.18, 0.20), (0.34, 0.265), (0.43 + chin, 0.36), (0.45 + chin, 0.56), (0.40 + chin, 0.78), (0.28, 0.90), (0.10, 0.80),
                   (-0.08, 0.60), (-0.18, 0.34), (-0.16, 0.10)], True)
    return sp([(0.04, 0.16), (0.22, 0.25), (0.34, 0.28), (0.395 + chin, 0.37), (0.415 + chin, 0.52), (0.37 + chin, 0.72), (0.30, 0.80), (0.20, 0.62),
               (0.06, 0.50), (-0.06, 0.34), (-0.08, 0.16)], True)


def neck_path(hx, hy, hh, bx, by, wt=0.50, wb=0.70, fwd=0.0):
    """Boyun: baş merkezi (hx,hy) → omuz tabanı (bx,by). wt/wb: üst/alt genişlik (baş yüksekliği cinsinden)."""
    return limb([(hx - 0.02 * hh, hy + 0.30 * hh), (bx, by)], [wt * hh, wb * hh], cap0=0, cap1=0)


# ───────────────────────────── eller (el-birimi: bilek (0,0), parmaklar +x, uzunluk 1) ─────────────────────────────
def hand_open():
    """Gevşek açık el (parmaklar hafif bükülü, başparmak ayrık)."""
    return sp([K(0, -0.16), (0.14, -0.20), (0.34, -0.21), (0.62, -0.19), (0.84, -0.14), (0.99, -0.07), (1.0, 0.0), (0.93, 0.07), (0.78, 0.11),
               (0.80, 0.15), (0.70, 0.19), (0.52, 0.17), (0.34, 0.16), (0.14, 0.15), K(0, 0.14)], True)


def hand_thumb_fist():
    """Yumruk başparmağı: parmakların üstünden öne kıvrılan kısa parça."""
    return sp([K(0.24, -0.12), (0.34, -0.27), (0.50, -0.30), (0.62, -0.24), (0.58, -0.17), (0.44, -0.18), K(0.34, -0.08)], True, 0.9)


def hand_thumb(open_=0.0):
    """Başparmak (ayrı parça; açık elin üstünde)."""
    return sp([K(0.12, -0.14), (0.28, -0.30 - open_ * 0.1), (0.46, -0.37 - open_ * 0.1), (0.52, -0.33), (0.40, -0.25), (0.34, -0.17), K(0.24, -0.12)], True)


def hand_fist():
    """Kavrayan yumruk (sopa/kabze tutan): parmak boğumları (pürüzlü üst kenar) + başparmak ayrı parça (hand_thumb('fist'))."""
    return sp([K(0, -0.15), (0.14, -0.21), (0.30, -0.235), (0.40, -0.215), (0.50, -0.235), (0.60, -0.205), (0.72, -0.13), (0.76, -0.03), (0.72, 0.07), (0.62, 0.17), (0.40, 0.225), (0.18, 0.195), K(0, 0.14)], True)


def hand_pt(kind, x, y, s, rot=0.0, flip=False):
    return place({"open": hand_open, "fist": hand_fist, "thumb": hand_thumb, "thumb_fist": hand_thumb_fist}[kind](), x, y, s, rot, flip)


# ───────────────────────────── ortak yardımcılar ─────────────────────────────
def shoe(x, y, w, h_, front=1, kind="round"):
    """Ayakkabı (x,y: topuk-altı merkezi; ön +x*front). Kare burun (1520'ler) / sivri."""
    f = front
    if kind == "sharp":
        pts = [K(x - w * 0.35 * f, y - h_), (x + w * 0.15 * f, y - h_ * 1.05), (x + w * 0.6 * f, y - h_ * 0.55), K(x + w * 1.05 * f, y), K(x - w * 0.35 * f, y)]
    elif kind == "square":
        pts = [K(x - w * 0.35 * f, y - h_ * 1.05), (x + w * 0.15 * f, y - h_ * 1.0), (x + w * 0.7 * f, y - h_ * 0.7), K(x + w * 0.98 * f, y - h_ * 0.35), K(x + w * 0.98 * f, y), K(x - w * 0.35 * f, y)]
    else:
        pts = [K(x - w * 0.35 * f, y - h_ * 1.05), (x + w * 0.2 * f, y - h_ * 1.0), (x + w * 0.7 * f, y - h_ * 0.62), (x + w * 1.0 * f, y - h_ * 0.2), K(x + w * 0.95 * f, y), K(x - w * 0.35 * f, y)]
    return sp(pts, True, 0.8)


def fur_collar(cx, cy, w, h_, tuft=7, seed=1, front=0.5):
    """Kürk yaka: omuzlara oturan, tüylü (tırtıklı) alt kenarlı yarım halka. (cx,cy) boyun tabanı merkezi, w toplam genişlik."""
    pts = [K(cx - w / 2, cy - h_ * 0.1), (cx - w * 0.38, cy - h_ * 0.55), (cx - w * 0.12, cy - h_ * 0.72), (cx + w * 0.14, cy - h_ * 0.70), (cx + w * 0.38, cy - h_ * 0.50), K(cx + w / 2, cy + h_ * 0.05)]
    n = tuft
    for i in range(n):
        u = 1 - i / (n - 1)
        x = cx - w / 2 + w * u
        yy = cy + h_ * (0.38 + 0.38 * math.sin(math.pi * u) * 0.9)
        pts.append(K(x + w * 0.015, yy + h_ * 0.30))
        pts.append(K(x - w * 0.012, yy))
    return sp(pts, True, 0.7) if False else poly([(p[0], p[1]) for p in pts])


def feather_path(x0, y0, x1, y1, w, bend=0.0, barbs=True):
    """Tüy (kuş tüyü/ostrich): tabandan uca, ince mızrak biçimi + hafif tırtık."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    pts = [K(x0, y0)]
    n = 7
    for i in range(1, n):
        u = i / n
        wd = w * math.sin(math.pi * min(1.0, u * 0.95 + 0.03)) ** 0.8 * (1 - 0.15 * u)
        cx_, cy_ = x0 + dx * u + nx * bend * math.sin(math.pi * u), y0 + dy * u + ny * bend * math.sin(math.pi * u)
        jag = (0.12 * w if (barbs and i % 2 == 0) else 0.0)
        pts.append((cx_ + nx * (wd / 2 + jag), cy_ + ny * (wd / 2 + jag)))
    pts.append(K(x1 + nx * bend * 0.0, y1))
    back = []
    for i in range(n - 1, 0, -1):
        u = i / n
        wd = w * math.sin(math.pi * min(1.0, u * 0.95 + 0.03)) ** 0.8 * (1 - 0.15 * u)
        cx_, cy_ = x0 + dx * u + nx * bend * math.sin(math.pi * u), y0 + dy * u + ny * bend * math.sin(math.pi * u)
        jag = (0.12 * w if (barbs and i % 2 == 1) else 0.0)
        back.append((cx_ - nx * (wd / 2 + jag), cy_ - ny * (wd / 2 + jag)))
    return sp(pts + back, True, 0.9)


def hem_wave(x0, x1, y, n, amp, ph=0.0, drop=0.0):
    """Etek kenarı noktaları (soldan sağa): n dalga; tepe/çukur."""
    out = []
    for i in range(n * 2 + 1):
        u = i / (n * 2)
        x = x0 + (x1 - x0) * u
        out.append((x, y + math.sin(u * math.pi * 2 * n + ph) * amp - drop * u))
    return out
