"""MADALYA-LAB ek portreleri (Şarlken dosyası): medal.py'ye DOKUNMADAN yeni kişiler + yeni saç/şapka/sakal/giysi türleri.

Mimari
- `medal.PEOPLE[anahtar] = dict(..., _x=True)` olan kişiler aşağıdaki "genişletilmiş hat" ile çizilir (medal.portrait_height yamalanır);
  diğer 26 mevcut kişi hiç değişmez (eski hat aynen çalışır).
- Genişletilmiş hat: deri(kafa+boyun) → büst/giysi → saç → sakal → yüz çizgileri → bıyık → başlık → takılar.
  Yükseklik haritası (gri 0..255) üstüne çizilir; medal._relief_from_height kabartmaya çevirir (altın/royal/forest/bronze…).
- Tablolar: HAIR, BEARD, BUST, HAT, ACC  (ad → fn(cv, d)). Yeni tür eklemek için `@reg(HAT, "ad")`.
- Parametreler (medal.py'dekilere ek): eye (std|wide|narrow|heavy|almond), brow_style (std|arch|heavy|stern|raised|bushy),
  lash (kadın kirpiği), mouth (std|stern|smile), must (short|droop|handle|pencil|long), ear (False → kulak saçla kapalı),
  earring (pearl|ring|inca|aztec), cheek (0..1 elmacık), puff (iri yanak), blen/bstyle (sakal), acc (takı listesi).
Hepsi stilize "madalya portresi"dir (fotoğraf/benzerlik iddiası yok); yerli hükümdarlar onurlu tasvir edilir.
"""
import math
import zlib
from contextlib import contextmanager

import cv2
import numpy as np
import skia

import sk
import icons            # ek metal rampaları (royal, forest, crimson, violet, onyx, teal)
import medal
from medal import _Canvas, PEOPLE, INSCR, S

HAIR, HAT, BEARD, BUST, ACC = {}, {}, {}, {}, {}


def reg(table, name):
    def deco(fn):
        table[name] = fn
        return fn
    return deco


# ═════════════════════════════ ilkeller ═════════════════════════════
def P(pts, close=False, t=0.5):
    return sk.smooth_path(pts, close, t)


def poly(pts, close=True):
    return sk.poly_path(pts, close)


def _paint(g, stroke=0.0, blur=0.0):
    p = skia.Paint(AntiAlias=True, Color=skia.Color(int(g), int(g), int(g), 255))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


_S = {"clip": None}


def fillp(cv, pts, g, t=0.45, blur=0.0):
    path = P(pts, True, t)
    cv.fill(path, g, blur)
    if not blur:
        _S["clip"] = path


def fillq(cv, pts, g, blur=0.0):
    cv.fill(poly(pts), g, blur)


def ln(cv, pts, g, w, t=0.5, blur=0.0):
    cv.stroke(P(pts, False, t), g, w, blur)


def seg(cv, p, q, g, w):
    cv.stroke(poly([p, q], False), g, w)


def ov(cv, x, y, rx, ry, g, blur=0.0, rot=0.0, stroke=0.0):
    c = cv.c
    c.save()
    if blur and _S["clip"] is not None:
        c.clipPath(_S["clip"], skia.ClipOp.kIntersect, True)
    c.translate(x, y)
    if rot:
        c.rotate(rot)
    c.drawOval(skia.Rect.MakeLTRB(-rx, -ry, rx, ry), _paint(g, stroke, blur))
    c.restore()


def circ(cv, x, y, r, g, blur=0.0, stroke=0.0):
    cv.c.drawCircle(x, y, r, _paint(g, stroke, blur))


@contextmanager
def clip(cv, path):
    cv.c.save()
    cv.c.clipPath(path, skia.ClipOp.kIntersect, True)
    try:
        yield
    finally:
        cv.c.restore()


def rs_of(key):
    return np.random.RandomState(zlib.crc32(str(key).encode()) & 0x7FFFFFFF)


def cr(pts, n=14, closed=False):
    """Catmull-Rom örnekleme → (M,2) dizi."""
    p = np.asarray(pts, float)
    m = len(p)
    out = []
    for i in (range(m) if closed else range(m - 1)):
        p0 = p[(i - 1) % m] if (closed or i > 0) else p[i]
        p1, p2 = p[i], p[(i + 1) % m]
        p3 = p[(i + 2) % m] if (closed or i + 2 < m) else p[(i + 1) % m]
        for k in range(n):
            t = k / n
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    if not closed:
        out.append(p[-1])
    return np.array(out)


def tangents(a):
    t = np.gradient(a, axis=0)
    n = np.hypot(t[:, 0], t[:, 1])[:, None] + 1e-6
    return t / n


def along(a, n):
    """Yoğun noktalı eğri üzerinde eşit yay uzunluklu n nokta + teğetler."""
    seglen = np.hypot(*np.diff(a, axis=0).T)
    cum = np.r_[0, np.cumsum(seglen)]
    ts = np.linspace(0, cum[-1], n)
    xs = np.interp(ts, cum, a[:, 0])
    ys = np.interp(ts, cum, a[:, 1])
    pts = np.stack([xs, ys], 1)
    return pts, tangents(pts) if n > 1 else np.array([[1.0, 0.0]])


def flow(cv, roots, tips, g, w, bend=0.0, waves=0.0, amp=0.0, n=12, t=0.5, seed=1, jit=0.0, autoclip=True):
    """Köklerden uçlara akan saç/sakal telleri (düzgün eğriler); son dolgu yoluna (_S["clip"]) kırpılır."""
    if autoclip and _S["clip"] is not None:
        cv.c.save()
        cv.c.clipPath(_S["clip"], skia.ClipOp.kIntersect, True)
        try:
            return flow(cv, roots, tips, g, w, bend, waves, amp, n, t, seed, jit, autoclip=False)
        finally:
            cv.c.restore()
    rs = np.random.RandomState(seed)
    for r, tp in zip(roots, tips):
        r = np.array(r, float)
        tp = np.array(tp, float)
        v = tp - r
        L = math.hypot(*v) + 1e-6
        nrm = np.array([-v[1], v[0]]) / L
        ph = rs.uniform(0, 6.28)
        bj = bend * (1 + jit * rs.uniform(-1, 1))
        pts = []
        for k in range(n + 1):
            s = k / n
            q = r + v * s + nrm * (bj * math.sin(math.pi * s) + amp * math.sin(2 * math.pi * waves * s + ph) * s)
            pts.append((float(q[0]), float(q[1])))
        cv.stroke(sk.smooth_path(pts, False, t), g, w)


def lerp2(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def pearl(cv, x, y, r=7, g=246):
    circ(cv, x, y, r + 2.4, 104, stroke=2.4)
    circ(cv, x, y, r, g)
    circ(cv, x - r * 0.3, y - r * 0.3, r * 0.3, min(255, g + 9))


def gem(cv, x, y, r, g=250, shape="cab"):
    circ(cv, x, y, r + 3.5, 96, stroke=3.2)
    if shape == "dia":
        fillq(cv, [(x, y - r * 1.25), (x + r, y), (x, y + r * 1.25), (x - r, y)], g)
        seg(cv, (x - r * .9, y), (x + r * .9, y), 150, 1.8)
        seg(cv, (x, y - r), (x, y + r), 150, 1.8)
    elif shape == "sq":
        cv.fill(poly([(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]), g)
        circ(cv, x, y, r * 0.5, 160, stroke=1.8)
    else:
        circ(cv, x, y, r, g)
        circ(cv, x, y, r * 0.58, 168, stroke=1.8)
        circ(cv, x - r * 0.28, y - r * 0.3, r * 0.22, 255)


def beads_on(cv, pts, n, r=6, g=246, dense=18):
    a = cr(pts, dense)
    q, _ = along(a, n)
    for x, y in q:
        pearl(cv, float(x), float(y), r, g)


def chain(cv, pts, n, rx=15, ry=9, g=236, w=4.2, dense=18, start=0.0, end=1.0):
    a = cr(pts, dense)
    q, tg = along(a, n)
    for i in range(n):
        s = i / max(1, n - 1)
        if s < start or s > end:
            continue
        ang = math.degrees(math.atan2(tg[i][1], tg[i][0]))
        if i % 2 == 0:
            ov(cv, float(q[i][0]), float(q[i][1]), rx, ry, g, rot=ang, stroke=w)
        else:
            ov(cv, float(q[i][0]), float(q[i][1]), rx * 0.55, ry * 1.05, g - 14, rot=ang, stroke=w * 0.9)


def ribbon(cv, pts, w0, w1, g, n=14, wprof=None, seam=None, seamg=120):
    """Değişken genişlikli şerit (ince uçlu kuyruk, bıyık, tüy…)."""
    a = cr(pts, n)
    tg = tangents(a)
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    m = len(a)
    ws = []
    for i in range(m):
        s = i / (m - 1)
        ws.append((w0 + (w1 - w0) * s) * (wprof(s) if wprof else 1.0) / 2)
    ws = np.array(ws)[:, None]
    L = a + nr * ws
    R = a - nr * ws
    ptsp = [tuple(map(float, p)) for p in np.vstack([L, R[::-1]])]
    cv.fill(poly(ptsp), g)
    if seam:
        cv.stroke(poly([tuple(map(float, p)) for p in a], False), seamg, seam)
    return a, nr, ws


def plume(cv, pts, w, g=234, seed=2, barbs=16, shaft=5.0):
    """Tüy: gövde + tarak + tarak çizikleri."""
    a, nr, ws = ribbon(cv, pts, w, 0, g, n=14, wprof=lambda s: (math.sin(math.pi * min(1, s * 1.12 + 0.06)) ** 0.65))
    cv.stroke(poly([tuple(map(float, p)) for p in a], False), 130, 2.2)
    for k in range(barbs):
        i = int((k + 0.5) / barbs * (len(a) - 1))
        for sgn in (-1, 1):
            p0 = a[i]
            p1 = a[min(len(a) - 1, i + 3)] + nr[i] * ws[i] * sgn * 1.0
            cv.stroke(poly([(float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1]))], False), g - 78, 1.5)
    cv.stroke(poly([tuple(map(float, p)) for p in a[:-1]], False), g + 12, shaft)


def fur_band(cv, spine, width, seed=3, g=176, step=1, L=(16, 28), flare=0.0, tipg=None, rows=3):
    """Kürk şeridi: kalın taban + rastgele kıl çizikleri."""
    rs = np.random.RandomState(seed)
    a = cr(spine, 18)
    tg = tangents(a)
    nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
    cv.stroke(P(spine, False, 0.5), g, width)
    for i in range(0, len(a), step):
        p = a[i]
        for _ in range(rows):
            off = (rs.rand() - 0.5) * width * 0.92
            q = p + nr[i] * off
            ang = math.pi / 2 + rs.uniform(-0.45, 0.45) + flare * (off / max(1, width))
            ll = rs.uniform(*L)
            q2 = (q[0] + math.cos(ang) * ll * 0.5, q[1] + math.sin(ang) * ll)
            cv.stroke(P([(float(q[0]), float(q[1])), (float((q[0] + q2[0]) / 2 + rs.uniform(-3, 3)), float((q[1] + q2[1]) / 2)), (float(q2[0]), float(q2[1]))], False, 0.5),
                      g - 38, 1.9)
            if rs.rand() < 0.55:
                cv.stroke(poly([(float(q[0] + 4), float(q[1])), (float(q2[0] + 4), float(q2[1] - 2))], False), g + 20, 1.5)
    # kenar boncukları (kürk ucu)
    edge = a + nr * (width * 0.5)
    for i in range(0, len(edge), 2):
        circ(cv, float(edge[i][0]), float(edge[i][1]), 5.5, g + (tipg if tipg is not None else 10))


def fur_fill(cv, path, g, seed=5, n=240, L=(14, 26), ang=math.pi / 2, sd=0.5, gd=38):
    """Bir yolun içini kürk dokusuyla doldur."""
    rs = np.random.RandomState(seed)
    b = path.getBounds()
    cv.fill(path, g)
    with clip(cv, path):
        for _ in range(n):
            x = rs.uniform(b.left(), b.right())
            y = rs.uniform(b.top(), b.bottom())
            a = ang + rs.uniform(-sd, sd)
            ll = rs.uniform(*L)
            x2, y2 = x + math.cos(a) * ll, y + math.sin(a) * ll
            cv.stroke(P([(x, y), ((x + x2) / 2 + rs.uniform(-3, 3), (y + y2) / 2), (x2, y2)], False, 0.5), g - gd, 2.0)
            if rs.rand() < 0.5:
                cv.stroke(poly([(x + 3, y), (x2 + 3, y2)], False), g + 22, 1.5)


def fleuron(cv, x, y, s, g=238):
    ov(cv, x, y - s * 0.52, s * 0.19, s * 0.52, g)
    for sgn in (-1, 1):
        ov(cv, x + sgn * s * 0.33, y - s * 0.34, s * 0.15, s * 0.36, g, rot=sgn * 38)
    cv.fill(poly([(x - s * 0.34, y), (x + s * 0.34, y), (x + s * 0.26, y - s * 0.2), (x - s * 0.26, y - s * 0.2)]), g)
    seg(cv, (x, y - s * 0.95), (x, y - s * 0.28), g - 90, 1.8)


def cross_at(cv, x, y, s, g=240):
    cv.fill(poly([(x - s * 0.1, y - s), (x + s * 0.1, y - s), (x + s * 0.1, y), (x - s * 0.1, y)]), g)
    cv.fill(poly([(x - s * 0.42, y - s * 0.72), (x + s * 0.42, y - s * 0.72), (x + s * 0.42, y - s * 0.52), (x - s * 0.42, y - s * 0.52)]), g)


# ═════════════════════════════ deri: kafa + boyun ═════════════════════════════
def _outline_x(d):
    pts = medal.face_points(d)
    ck = d.get("ck", 1.0)

    def cy(y):
        return y if y <= 470 else 470 + (y - 470) * ck
    jowl = d["jowl"]
    under = [(560, 640 + 6 * jowl * 10), (500 - 18 * jowl, 640 + 28 * jowl), (430 - 14 * jowl, 590 + 18 * jowl), (396, 520)]
    back = [(372, 430), (400, 330), (470, 270)]
    return [(x, cy(y)) for x, y in pts + under] + back


def _skin_x(cv, d):
    outline = _outline_x(d)
    p = P(outline, True, 0.45)
    cv.fill(p, 120)
    skull = skia.Path()
    skull.addOval(skia.Rect.MakeLTRB(344, 204, 598, 560))
    cv.fill(skull, 120)
    nk = d["neck"]
    nb = d.get("nback", 352)
    neck = P([(430, 560), (560 - (nk - 1) * 14, 628), (578 + (nk - 1) * 26, 700), (606 + (nk - 1) * 30, 770), (560, 830),
              (max(420, nb + 66), 830), (nb + 4, 760), (nb, 620)], True, 0.35)
    cv.fill(neck, 96)
    cv.fill(p, 128, blur=2.0)
    allp = skia.Op(skia.Op(p, skull, skia.PathOp.kUnion_PathOp), neck, skia.PathOp.kUnion_PathOp)
    with clip(cv, allp):
        ov(cv, 510, 510, 80, 90, 150, blur=22)                         # yanak hacmi
        if d.get("puff"):
            ov(cv, 500, 540, 100 + 20 * d["puff"], 110 + 20 * d["puff"], 150, blur=26)
        if d["jowl"] > 0:
            ov(cv, 500, 610 + d["jowl"] * 10, 70, 50 + d["jowl"] * 20, 140, blur=16)
        ov(cv, 540, 335, 70, 45, 150, blur=16)                         # alın/kaş hacmi
        if d.get("cheek"):
            ov(cv, 528, 438, 44, 26, 128 + 34 * d["cheek"], blur=13, rot=-24)


def _features_x(cv, d):
    a = d["age"]
    br, n, hk, lip, lip2 = d["brow"], d["nose"], d["hook"], d["lip"], d["lip2"]
    mo = d.get("mouth_open", 0.0)
    eye = d.get("eye", "std")
    bs = d.get("brow_style", "std")
    # ── kaş
    brows = {
        "std": ([(520, 360), (556, 348), (594, 350 + br * 0.2)], 9 + br * 0.5, 66),
        "arch": ([(524, 358), (548, 344), (576, 342), (598, 354)], 5.5, 76),
        "heavy": ([(510, 366), (550, 348), (598, 354)], 14.5, 58),
        "stern": ([(514, 346), (556, 350), (600, 368)], 12, 60),
        "raised": ([(526, 352), (556, 338), (590, 344)], 6.5, 80),
        "bushy": ([(512, 364), (540, 350), (570, 346), (600, 356)], 16, 62),
    }[bs]
    ln(cv, brows[0], brows[2], brows[1])
    if bs in ("heavy", "bushy", "stern"):
        for k in range(5):
            seg(cv, (528 + k * 14, 356 - (k % 2) * 2), (534 + k * 14, 348 - (k % 2) * 3), 96, 1.6)
    # ── göz
    cx, cy = 556, 376
    wd, ht, ir = {"std": (1, 1, 6), "wide": (1.06, 1.45, 7.6), "narrow": (1.0, 0.62, 5), "heavy": (1.0, 0.8, 5.6), "almond": (1.08, 1.0, 5.6)}[eye]
    ir = d.get("iris", ir)
    c = cv.c
    c.save()
    if eye == "almond":
        c.translate(cx, cy); c.rotate(-5); c.translate(-cx, -cy)
    cv.fill(P([(cx - 22 * wd, cy + 2), (cx, cy - 8 * ht), (cx + 26 * wd, cy), (cx, cy + 8 * ht)], True), 60)
    ln(cv, [(cx - 26 * wd, cy - 2), (cx, cy - 13 * ht), (cx + 30 * wd, cy - 4)], 90, 4)
    ln(cv, [(cx - 22 * wd, cy + 16), (cx + 2, cy + 21 * max(ht, .8)), (cx + 26 * wd, cy + 16)], 90, 3 + a * 2)
    circ(cv, cx + 4, cy, ir, 30)
    if eye == "heavy" or a > 0.5:
        ln(cv, [(cx - 28, cy - 17), (cx, cy - 25), (cx + 34, cy - 13)], 102, 2.6)
    c.restore()
    if d.get("lash"):
        for (x0, y0, x1, y1) in [(cx + 30, cy - 4, cx + 39, cy - 9), (cx + 26, cy - 9, cx + 32, cy - 17), (cx + 18, cy - 12, cx + 21, cy - 20)]:
            seg(cv, (x0, y0), (x1, y1), 72, 2.2)
    # ── burun + ağız (çocukta alt yüz sıkıştırılır)
    ck = d.get("ck", 1.0)
    cv.c.save()
    if ck != 1.0:
        cv.c.translate(0, 470 * (1 - ck))
        cv.c.scale(1, ck)
    ln(cv, [(626 + n * 0.5, 480), (616, 486), (606, 484)], 70, 5)
    ln(cv, [(604, 440 + hk), (592, 470), (600, 488)], 100, 3)
    # ── ağız
    md = d.get("mouth", "std")
    cy0, cy1 = {"std": (529, 526), "stern": (535, 527), "smile": (523, 527)}[md]
    ln(cv, [(560, cy0 + 1), (580, 526 + (cy0 - cy1) * 0.2), (602 + lip * 0.5, cy1 + mo * 6)], 56, 6)
    ln(cv, [(578, 556), (600 + lip2 * 0.3, 556)], 98, 3)
    if lip + lip2 > 9:      # dolgun dudak kenarı
        ln(cv, [(612 + lip, 513), (598, 521), (582, 525)], 96, 2.2)
    cv.c.restore()
    # ── kulak
    if d.get("ear", True):
        ear = P([(440, 412), (452, 396), (472, 402), (472, 440), (456, 470), (444, 454)], True)
        cv.fill(ear, 136)
        cv.stroke(ear, 78, 5.5)
        ln(cv, [(452, 414), (462, 420), (460, 448)], 90, 3)
    # ── yaş çizgileri
    if a > 0.2:
        ln(cv, [(590, 492), (578, 520), (572, 548)], 92, 2.5 + a * 3)
    if a > 0.4:
        ln(cv, [(500, 380), (486, 390), (484, 410)], 98, 2 + a * 2)
        ln(cv, [(530, 400), (520, 424)], 104, 1.8 + a * 1.5)
        ln(cv, [(536, 398), (558, 406), (584, 400)], 108, 2.0)
    if a > 0.6:
        ln(cv, [(500, 346), (540, 338)], 108, 2)
        ln(cv, [(495, 322), (550, 312)], 110, 2)
    if a > 0.75:
        ln(cv, [(496, 298), (546, 290)], 112, 1.8)
    # ── gravür taraması: elmacık altı + çene altı/boyun gölgesi (sakalsız yüzlerde)
    if d.get("shade", False) and not d.get("beard"):
        ck = d.get("ck", 1.0)
        cv.c.save()
        if ck != 1.0:
            cv.c.translate(0, 470 * (1 - ck))
            cv.c.scale(1, ck)
        for k in range(5):
            x0, y0 = 486 + k * 15, 462 + k * 7
            ln(cv, [(x0, y0), (x0 - 9, y0 + 20 + k)], 118, 1.7)
        for k in range(3):
            ln(cv, [(452 + k * 26, 604 + k * 3), (466 + k * 26, 640 + k * 3)], 104, 1.7)
        cv.c.restore()
        if d.get("neck", 1.0) >= 0.95:
            for k in range(3):
                ln(cv, [(470 + k * 16, 650), (480 + k * 16, 700)], 100, 1.7)


# ═════════════════════════════ büst / giysi tabanı ═════════════════════════════
NECK = {
    "high": [(352, 640), (430, 626), (520, 624), (588, 636)],
    "mid": [(350, 688), (430, 686), (520, 696), (600, 716)],
    "low": [(350, 700), (440, 722), (530, 758), (612, 800)],
}


def body(cv, neck_pts, g=74, extra_l=0):
    y1 = neck_pts[-1][1]
    pts = [(110 - extra_l, 1070), (140 - extra_l, 970), (196, 868), (262, 792), (316, 744)] + list(neck_pts) + \
          [(690, y1 + 50), (770, y1 + 112), (860, y1 + 200), (920, 1070)]
    path = P(pts, True, 0.4)
    cv.fill(path, g)
    with clip(cv, path):
        ov(cv, 540, 930, 240, 130, g + 22, blur=34)         # göğüs hacmi
        ov(cv, 330, 800, 90, 60, g + 14, blur=22)           # omuz yuvarlağı
    return pts


def folds(cv, starts, ends, g=52, w=3.0, bend=14, seed=4):
    flow(cv, starts, ends, g, w, bend=bend, seed=seed, jit=0.5, n=8)


@reg(BUST, "plain")
def _b_plain(cv, d):
    body(cv, NECK["mid"])
    ln(cv, [(350, 688), (430, 686), (520, 696), (600, 716)], 150, 14)
    folds(cv, [(320, 860), (420, 800)], [(300, 1000), (380, 1000)])


# ═════════════════════════════ saç ═════════════════════════════
def pl(pts, t):
    a = np.asarray(pts, float)
    cum = np.r_[0, np.cumsum(np.hypot(*np.diff(a, axis=0).T))]
    s = min(max(t, 0.0), 1.0) * cum[-1]
    return (float(np.interp(s, cum, a[:, 0])), float(np.interp(s, cum, a[:, 1])))


def mass(cv, pts, g, t=0.45, edge=112):
    path = P(pts, True, t)
    cv.fill(path, g)
    cv.stroke(path, edge, 2.4)
    _S["clip"] = path


def curl(cv, x, y, r, g=140, w=2.4, turns=1.7, flip=1):
    pts = []
    for k in range(24):
        a = k / 23 * turns * 2 * math.pi
        rr = r * (1 - 0.72 * k / 23)
        pts.append((x + flip * rr * math.cos(a), y + rr * math.sin(a)))
    ln(cv, pts, g, w)


def mass_texture(cv, pts, seed, n, L, ang, sd, g, w, t=0.45, dirfn=None):
    path = P(pts, True, t)
    rs = np.random.RandomState(seed)
    b = path.getBounds()
    with clip(cv, path):
        for _ in range(n):
            x = rs.uniform(b.left(), b.right())
            y = rs.uniform(b.top(), b.bottom())
            a = (dirfn(x, y) if dirfn else ang) + rs.uniform(-sd, sd)
            ll = rs.uniform(*L)
            cv.stroke(poly([(x, y), (x + math.cos(a) * ll, y + math.sin(a) * ll)], False), g, w)


def hatch_fill(cv, pts, seed, spacing, L, dirfn, g, w, jit=0.3, t=0.42):
    path = P(pts, True, t)
    rs = np.random.RandomState(seed)
    b = path.getBounds()
    with clip(cv, path):
        y = b.top()
        row = 0
        while y < b.bottom() + spacing:
            x = b.left() + (spacing / 2 if row % 2 else 0)
            while x < b.right() + spacing:
                px = x + rs.uniform(-jit, jit) * spacing
                py = y + rs.uniform(-jit, jit) * spacing
                a = dirfn(px, py) + rs.uniform(-0.13, 0.13)
                ll = rs.uniform(*L)
                cv.stroke(poly([(px, py), (px + math.cos(a) * ll, py + math.sin(a) * ll)], False), g, w)
                x += spacing
            y += spacing * 0.78
            row += 1


def strands_between(cv, top, bot, n, g, w, bend=0.0, waves=0.0, amp=0.0, seed=1, jit=0.3, rev=True, nn=12):
    roots, tips = [], []
    for i in range(n):
        t = (i + 0.5) / n
        roots.append(pl(top, t))
        tips.append(pl(bot, 1 - t if rev else t))
    flow(cv, roots, tips, g, w, bend=bend, waves=waves, amp=amp, n=nn, seed=seed, jit=jit)


@reg(HAIR, "wavy")           # Filip / Lajos: omuza inen dalgalı saç + lüleler
def _h_wavy(cv, d):
    pts = [(586, 262), (520, 212), (430, 194), (356, 236), (320, 330), (306, 450), (300, 560), (284, 640), (308, 704), (362, 690),
           (398, 646), (424, 590), (448, 520), (472, 452), (506, 382), (550, 316)]
    mass(cv, pts, 188)
    top = [(574, 252), (500, 210), (420, 200), (356, 240), (322, 330)]
    bot = [(476, 590), (430, 640), (380, 690), (330, 706), (296, 690)]
    strands_between(cv, top, bot, 17, 144, 2.6, bend=-30, waves=1.3, amp=13, seed=11, jit=0.35, rev=False)
    strands_between(cv, top, bot, 16, 166, 1.5, bend=-20, waves=1.3, amp=10, seed=12, jit=0.4, rev=False)
    for (x, y, f) in [(296, 690, 1), (326, 714, 1), (366, 702, 1), (404, 668, 1)]:
        curl(cv, x, y, 15, 138, 2.4, 1.6, f)


@reg(HAIR, "bowl")           # Fernando: düz, çene hizasında kesik "tas" saç + alın perçemi
def _h_bowl(cv, d):
    pts = [(598, 304), (582, 262), (522, 222), (430, 204), (362, 242), (338, 330), (334, 440), (346, 524), (388, 556), (444, 548),
           (470, 500), (482, 436), (500, 362), (520, 320), (560, 308)]
    mass(cv, pts, 186)
    roots = [pl([(584, 258), (500, 214), (420, 206), (364, 244), (342, 330)], i / 17) for i in range(18)]
    tips = [pl([(592, 302), (540, 316), (490, 400), (472, 500), (420, 552), (356, 524)], i / 17) for i in range(18)]
    flow(cv, roots, tips, 142, 2.3, bend=-8, n=10, seed=3, jit=0.3)
    seg(cv, (588, 300), (532, 316), 120, 2.6)           # perçem alt çizgisi


@reg(HAIR, "long_flow")      # Şarlman: omuzlara inen düz-hafif dalgalı uzun saç
def _h_longflow(cv, d):
    pts = [(586, 262), (520, 210), (430, 192), (356, 232), (324, 330), (314, 460), (310, 590), (316, 700), (346, 770), (396, 764),
           (420, 690), (434, 600), (450, 520), (470, 452), (506, 382), (552, 314)]
    mass(cv, pts, 186)
    top = [(574, 252), (500, 208), (420, 198), (356, 238), (326, 330)]
    bot = [(472, 690), (430, 740), (386, 770), (340, 766), (312, 700)]
    strands_between(cv, top, bot, 19, 142, 2.4, bend=-26, waves=1.1, amp=9, seed=21, jit=0.3, rev=False)
    strands_between(cv, top, bot, 18, 164, 1.4, bend=-18, waves=1.1, amp=7, seed=22, jit=0.4, rev=False)


@reg(HAIR, "crop")           # kısa kırpık saç, kulak açık
def _h_crop(cv, d):
    pts = [(578, 266), (500, 212), (420, 212), (362, 262), (342, 340), (352, 424), (384, 452), (412, 402), (440, 350), (490, 312), (540, 288)]
    mass(cv, pts, 186)
    mass_texture(cv, pts, 31, 150, (12, 22), math.radians(165), 0.7, 138, 1.9)
    mass_texture(cv, pts, 32, 90, (10, 16), math.radians(160), 0.8, 164, 1.4)


@reg(HAIR, "child")          # çocuk: çene hizasında düz saç + perçem
def _h_child(cv, d):
    pts = [(594, 304), (582, 262), (520, 222), (430, 204), (364, 238), (336, 330), (328, 430), (334, 506), (366, 548), (410, 544),
           (436, 508), (456, 462), (480, 412), (512, 360), (540, 324), (570, 310)]
    mass(cv, pts, 186)
    roots = [pl([(584, 258), (500, 214), (420, 206), (364, 242), (338, 330)], i / 15) for i in range(16)]
    tips = [pl([(592, 304), (540, 318), (480, 420), (456, 500), (410, 544), (350, 520)], i / 15) for i in range(16)]
    flow(cv, roots, tips, 142, 2.3, bend=-8, n=10, seed=5, jit=0.3)
    seg(cv, (592, 302), (540, 320), 118, 2.6)


@reg(HAIR, "inca")           # düz, parlak, "tas" kesim; kulak açık
def _h_inca(cv, d):
    pts = [(590, 272), (520, 228), (430, 214), (362, 252), (338, 340), (334, 440), (346, 530), (392, 562), (430, 534), (436, 472),
           (440, 420), (470, 384), (520, 332), (568, 302)]
    mass(cv, pts, 188)
    roots = [pl([(580, 262), (500, 220), (420, 212), (362, 250), (340, 340)], i / 19) for i in range(20)]
    tips = [pl([(566, 304), (520, 334), (462, 392), (434, 480), (392, 560), (350, 530)], i / 19) for i in range(20)]
    flow(cv, roots, tips, 148, 1.9, bend=-6, n=10, seed=7, jit=0.25)


@reg(HAIR, "sides")          # yaşlı: şapka altından yanlarda ince saç
def _h_sides(cv, d):
    pts = [(412, 286), (360, 318), (344, 410), (360, 500), (400, 524), (426, 470), (432, 404), (446, 340)]
    mass(cv, pts, 182)
    mass_texture(cv, pts, 41, 70, (14, 24), math.radians(100), 0.45, 140, 1.8)


@reg(HAIR, "thin_back")      # dolgun sakallı kişiler: şapka altı uzun düz saç (omuz)
def _h_thinback(cv, d):
    pts = [(560, 280), (480, 226), (400, 224), (350, 280), (326, 390), (318, 520), (322, 640), (360, 700), (404, 676), (424, 590),
           (440, 500), (462, 430), (500, 370), (540, 322)]
    mass(cv, pts, 184)
    top = [(552, 270), (480, 228), (400, 228), (350, 290), (330, 380)]
    bot = [(448, 600), (420, 660), (372, 700), (336, 650), (322, 560)]
    strands_between(cv, top, bot, 15, 142, 2.3, bend=-14, seed=51, jit=0.3, rev=False)


# ═════════════════════════════ sakal / bıyık ═════════════════════════════
def beard_shape(cv, top, bot, g=172, n=22, sg=140, sw=1.9, bend=0.0, waves=0.0, amp=0.0, seed=1, jit=0.4, rev=True, nn=10,
                short=0, t=0.42):
    pts = list(top) + list(bot)
    cv.fill(P(pts, True, t), g)
    cv.fill(P(pts, True, t), g + 6, blur=5)
    cv.stroke(P(pts, True, t), 104, 2.6)
    with clip(cv, P(pts, True, t)):
        if short:
            hatch_fill(cv, pts, seed, 8.6 if short > 150 else 10.0, (6, 10),
                       lambda x, y: math.radians(64 + 30 * max(0.0, min(1.0, (x - 470) / 130.0)) + 10 * max(0.0, min(1.0, (y - 620) / 90.0))),
                       sg, sw - 0.35, t=t)
        else:
            strands_between(cv, top, bot, n, sg, sw, bend=bend, waves=waves, amp=amp, seed=seed, jit=jit, rev=rev, nn=nn)
            strands_between(cv, top, bot, n - 4, sg + 24, sw - 0.5, bend=bend * 0.7, waves=waves, amp=amp * 0.8, seed=seed + 1, jit=jit, rev=rev, nn=nn)


TOP = [(450, 420), (500, 448), (548, 482), (588, 510)]


@reg(BEARD, "trim")          # kırpılmış sakal (Padilla/Welser)
def _be_trim(cv, d):
    ch = d["chin"]
    top = [(456, 424), (504, 452), (548, 486), (586, 514)]
    bot = [(592, 540), (600, 566), (612 + ch, 598), (598 + ch * .7, 636), (552, 652), (486, 648), (430, 606), (404, 540), (420, 470)]
    beard_shape(cv, top, bot, 170, short=200, seed=61)


@reg(BEARD, "cropped")       # çok kısa/yakın (Johann Friedrich)
def _be_cropped(cv, d):
    ch = d["chin"]
    top = [(456, 428), (504, 456), (548, 490), (586, 518)]
    bot = [(594, 546), (602, 572), (610 + ch, 602), (596 + ch * .7, 640), (552, 660), (480, 660), (426, 618), (402, 548), (420, 476)]
    beard_shape(cv, top, bot, 168, short=230, seed=62)


@reg(BEARD, "goatee")        # bıyık + kısa sivri sakal (Bravo)
def _be_goatee(cv, d):
    ch = d["chin"]
    L = d.get("blen", 30)
    top = [(470, 470), (520, 500), (560, 526)]
    bot = [(594, 556), (608 + ch, 598), (602 + ch * .7, 648 + L), (572, 668 + L), (536, 634), (500, 590), (462, 520)]
    beard_shape(cv, top, bot, 170, short=120, seed=63)


@reg(BEARD, "full_round")    # dolgun, yuvarlak (Maldonado)
def _be_fullround(cv, d):
    ch, L = d["chin"], d.get("blen", 0)
    top = [(450, 420), (500, 446), (548, 480), (588, 508)]
    bot = [(602, 540), (616, 568), (626 + ch, 610), (620 + ch * .7, 660 + L * .3), (588, 712 + L), (540, 734 + L), (490, 720 + L * .8),
           (440, 676), (410, 604), (398, 520), (412, 460)]
    beard_shape(cv, top, bot, 172, n=24, bend=10, seed=64, jit=0.35)


@reg(BEARD, "broad")         # iri, yayvan (Frederik)
def _be_broad(cv, d):
    ch = d["chin"]
    top = [(446, 410), (494, 436), (544, 470), (590, 504)]
    bot = [(608, 534), (628, 568), (646 + ch, 616), (642 + ch * .7, 690), (606, 764), (548, 796), (486, 776), (430, 714), (398, 620),
           (386, 520), (404, 452)]
    beard_shape(cv, top, bot, 172, n=26, bend=16, seed=65, jit=0.4)


@reg(BEARD, "long_flow")     # Şarlman: göğse inen dalgalı uzun sakal
def _be_longflow(cv, d):
    ch = d["chin"]
    top = [(470, 442), (512, 466), (552, 492), (590, 514)]
    bot = [(606, 540), (624, 572), (634 + ch, 618), (630 + ch * .6, 700), (606, 780), (574, 836), (546, 872), (512, 836), (478, 772),
           (446, 690), (424, 612), (418, 540), (436, 478)]
    beard_shape(cv, top, bot, 172, n=24, bend=12, waves=1.2, amp=10, seed=66, jit=0.35, nn=14)


@reg(BEARD, "white_long")    # Doria: uzun beyaz, iki uca ayrılan
def _be_white(cv, d):
    ch = d["chin"]
    top = [(448, 420), (498, 448), (548, 482), (588, 510)]
    bot = [(604, 540), (620, 572), (630 + ch, 616), (624 + ch * .6, 690), (610, 770), (590, 842), (560, 790), (534, 846), (506, 790),
           (470, 730), (436, 664), (408, 596), (396, 520), (412, 458)]
    beard_shape(cv, top, bot, 176, n=26, bend=10, waves=1.4, amp=9, seed=67, jit=0.35, nn=14)


@reg(BEARD, "short_gray")    # Sepúlveda: kısa gri sakal (çene + yanak)
def _be_gray(cv, d):
    ch = d["chin"]
    top = [(458, 428), (506, 458), (550, 490), (586, 516)]
    bot = [(592, 544), (600, 570), (610 + ch, 604), (600 + ch * .7, 646), (556, 664), (486, 658), (430, 612), (406, 544), (422, 474)]
    beard_shape(cv, top, bot, 168, short=170, seed=68, sg=146)


@reg(BEARD, "ship")          # Magellan: sivri çene sakalı, kırpık yanak
def _be_ship(cv, d):
    ch = d["chin"]
    top = [(472, 452), (514, 476), (554, 500), (590, 522)]
    bot = [(596, 550), (606, 576), (614 + ch, 608), (610 + ch * .8, 654), (600 + ch * .6, 706), (576, 686), (548, 662), (490, 652),
           (440, 614), (418, 542), (436, 482)]
    beard_shape(cv, top, bot, 170, short=200, seed=69)


@reg(BEARD, "chinstrap")     # Sepúlveda: yalnız çene hattı boyunca ince gri sakal
def _be_chinstrap(cv, d):
    ch = d["chin"]
    top = [(450, 506), (498, 544), (546, 568), (590, 574)]
    bot = [(602, 588), (612 + ch, 608), (600 + ch * .7, 646), (552, 662), (486, 654), (436, 614), (418, 560)]
    beard_shape(cv, top, bot, 168, short=150, seed=70, sg=146)


def _must(cv, d):
    k = d.get("must")
    if not k:
        return
    lip = d["lip"]
    P0 = (616, 500)
    shapes = {
        "short": ([P0, (596, 502), (572, 512), (552, 526)], 17, 7),
        "droop": ([P0, (592, 500), (564, 510), (546, 534), (540, 566)], 17, 5),
        "handle": ([P0, (592, 502), (562, 510), (540, 520), (524, 506), (520, 490)], 16, 5),
        "pencil": ([P0, (598, 504), (574, 512), (556, 520)], 8, 4),
        "long": ([P0, (588, 500), (556, 514), (528, 544), (512, 590)], 18, 5),
    }
    pts, w0, w1 = shapes[k]
    a, nr, ws = ribbon(cv, pts, w0, w1, 178, n=10, wprof=lambda s: 1 - 0.0 * s)
    cv.stroke(poly([tuple(map(float, p)) for p in a], False), 120, 2.0)
    for off in (-0.45, 0.45):
        q = a + nr * ws * off
        cv.stroke(poly([tuple(map(float, p)) for p in q], False), 140, 1.3)
    ln(cv, [(556, 531), (580, 528), (602 + lip * .5, 530)], 60, 3.4)      # ağız çizgisi bıyığın altından


# ═════════════════════════════ hat: yer tutucu + boru hattı ═════════════════════════════
@reg(HAT, "none")
def _hat_none(cv, d):
    pass


def render_x(d):
    cv = _Canvas()
    _S["clip"] = None
    _skin_x(cv, d)
    _S["clip"] = None
    BUST.get(d.get("garment"), BUST["plain"])(cv, d)
    _S["clip"] = None
    f = HAIR.get(d.get("hair"))
    if f:
        f(cv, d)
    _S["clip"] = None
    f = BEARD.get(d.get("beard"))
    if f:
        f(cv, d)
    _S["clip"] = None
    _features_x(cv, d)
    _must(cv, d)
    _S["clip"] = None
    f = HAT.get(d.get("hat"))
    if f:
        f(cv, d)
    _S["clip"] = None
    accs = d.get("acc") or []
    if isinstance(accs, str):
        accs = [accs]
    for a in accs:
        ACC[a](cv, d)
    return cv.arr()


_orig_portrait_height = medal.portrait_height


def _portrait_height(key, flip=False):
    d = medal.PEOPLE.get(key)
    if d and d.get("_x"):
        h = render_x(d)
        return h[:, ::-1] if flip else h
    return _orig_portrait_height(key, flip)


medal.portrait_height = _portrait_height


# ═════════════════════════════ başlıklar (1) ═════════════════════════════
def _rim(cv, pts, w, g, grooveg=140, gw=1.8):
    ln(cv, pts, g, w)
    for off in (-w * 0.5 + 1.5, w * 0.5 - 1.5):
        ln(cv, [(x, y + off) for x, y in pts], grooveg, gw)


@reg(HAT, "burg_bonnet")      # Filip: Burgonya yassı şapkası — mücevher broş + uzun tüy
def _hat_burg(cv, d):
    crown = [(318, 300), (316, 238), (364, 190), (452, 164), (550, 168), (626, 200), (662, 246), (650, 276), (600, 284), (520, 268),
             (430, 278), (360, 312)]
    fillp(cv, crown, 212)
    ov(cv, 490, 204, 140, 34, 232, blur=16)
    rim = [(326, 302), (430, 278), (520, 270), (600, 286), (656, 258)]
    for i in range(11):
        e = pl(rim, 0.04 + 0.92 * i / 10)
        mid = lerp2((500, 202), e, 0.5)
        ln(cv, [(500 + (e[0] - 500) * 0.1, 200), (mid[0], mid[1] - 10), (e[0], e[1] - 8)], 158, 2.4)
    _rim(cv, rim, 24, 236)
    # broş (enseigne)
    bx, by = 606, 240
    circ(cv, bx, by, 32, 246)
    circ(cv, bx, by, 32, 110, stroke=3)
    for k in range(7):
        a = k / 7 * 2 * math.pi
        pearl(cv, bx + 23 * math.cos(a), by + 23 * math.sin(a), 5.2)
    gem(cv, bx, by, 13, shape="dia")
    ln(cv, [(bx + 6, by + 30), (bx + 8, by + 46)], 200, 2.4)
    pearl(cv, bx + 8, by + 54, 7)
    plume(cv, [(612, 228), (576, 172), (500, 134), (420, 126), (346, 156), (306, 216), (296, 288)], 46, g=238)
    plume(cv, [(618, 232), (660, 196), (708, 200), (732, 242)], 32, g=232)


@reg(HAT, "barrete")          # Fernando: koyu yumuşak başlık (sade rozetli)
def _hat_barrete(cv, d):
    base = [(344, 300), (350, 236), (400, 196), (480, 178), (560, 190), (610, 226), (620, 262), (588, 282), (520, 264), (440, 270), (380, 300)]
    fillp(cv, base, 214)
    ov(cv, 484, 212, 108, 28, 230, blur=12)
    _rim(cv, [(356, 292), (440, 268), (520, 262), (598, 278)], 18, 232)
    ln(cv, [(420, 202), (472, 224), (544, 232)], 156, 2.4)
    ln(cv, [(480, 184), (522, 206), (582, 226)], 156, 2.2)
    ln(cv, [(380, 250), (410, 226), (450, 210)], 156, 2.0)
    if not d.get("nobadge"):
        circ(cv, 572, 262, 15, 240)                 # küçük rozet
        circ(cv, 572, 262, 15, 110, stroke=2.6)
        gem(cv, 572, 262, 7, shape="dia")
    if d.get("plumed"):
        plume(cv, [(566, 240), (590, 196), (634, 176), (672, 190)], 30, g=236)


@reg(HAT, "castilian_veil")   # Isabel: kenar bantlı beyaz peçe — mücevherli ön kenar
def _hat_cveil(cv, d):
    veil = [(592, 264), (544, 212), (450, 186), (366, 222), (326, 318), (306, 460), (296, 600), (284, 730), (300, 820), (380, 836),
            (420, 744), (436, 650), (446, 590), (458, 500), (480, 420), (506, 350), (540, 300), (568, 276)]
    fillp(cv, veil, 206, 0.42)
    ov(cv, 440, 300, 90, 70, 224, blur=22)
    top = [(556, 226), (470, 194), (390, 214), (340, 280)]
    bot = [(452, 650), (420, 742), (372, 812), (318, 786)]
    strands_between(cv, top, bot, 10, 150, 2.6, bend=-16, waves=0.8, amp=8, seed=71, jit=0.5, rev=False)
    front = [(594, 266), (568, 278), (540, 302), (506, 352), (480, 422), (458, 502), (446, 592), (438, 652)]
    ln(cv, front, 232, 20)
    ln(cv, front, 150, 1.8)
    beads_on(cv, front, 10, r=6.4)
    ln(cv, [(596, 268), (544, 222), (462, 200)], 150, 3)
    gem(cv, 560, 292, 9, shape="dia")


@reg(HAT, "imperial_crown")   # Şarlman: sekizgen taç bandı + zambak uçlar + haç taşıyan kemer
def _hat_icrown(cv, d):
    band = [(344, 300), (346, 240), (400, 214), (490, 198), (580, 206), (626, 226), (630, 268), (600, 290), (520, 270), (436, 276), (372, 306)]
    fillp(cv, band, 220, 0.42)
    ov(cv, 490, 238, 120, 18, 236, blur=9)
    top = [(352, 244), (400, 220), (490, 204), (580, 212), (622, 232)]
    bot = [(374, 304), (436, 279), (520, 272), (600, 292), (628, 268)]
    ln(cv, top, 150, 2.4)
    ln(cv, bot, 150, 2.4)
    for t in (0.2, 0.4, 0.6, 0.8):
        seg(cv, pl(top, t), pl(bot, t), 150, 2.4)
    for i, t in enumerate((0.1, 0.3, 0.5, 0.7, 0.9)):
        a, b = pl(top, t), pl(bot, t)
        gem(cv, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 11, shape="cab" if i % 2 == 0 else "dia")
    for t in (0.14, 0.5, 0.86):
        x, y = pl(top, t)
        fleuron(cv, x, y + 6, 64)
    arch = [(616, 228), (596, 162), (530, 126), (448, 120), (386, 152), (360, 230)]
    ln(cv, arch, 232, 20)
    ln(cv, arch, 150, 2.2)
    beads_on(cv, arch, 9, r=4.6)
    circ(cv, 486, 122, 17, 240)
    circ(cv, 486, 122, 17, 110, stroke=2.6)
    cross_at(cv, 486, 104, 52)


# ═════════════════════════════ giysi / büst (1) ═════════════════════════════
@reg(BUST, "fur_jacket")       # Filip: kürk şal yaka + Altın Post zinciri
def _b_furjacket(cv, d):
    body(cv, NECK["mid"], 74)
    folds(cv, [(330, 900), (440, 860), (560, 880)], [(300, 1040), (420, 1040), (600, 1040)], seed=7)
    ln(cv, [(560, 790), (590, 900), (610, 1040)], 52, 3)
    fur_band(cv, [(380, 684), (440, 700), (520, 718), (612, 758), (672, 834), (716, 930)], 80, seed=5, g=176)
    chain(cv, [(376, 700), (452, 752), (540, 788), (624, 822)], 11, rx=18, ry=10)
    gem(cv, 636, 836, 12, shape="dia")


def band_poly(cv, top, bot, g, groove=110, gw=2.2, t=0.35):
    """top (arkadan öne) + bot (önden arkaya) kenarlı şerit."""
    pts = list(top) + list(bot)
    cv.fill(P(pts, True, t), g)
    cv.stroke(P(pts, True, t), groove, gw)


@reg(BUST, "dark_doublet")     # Fernando: yüksek yaka, düğmeler, zincir
def _b_darkdoublet(cv, d):
    body(cv, NECK["high"], 72)
    folds(cv, [(330, 900), (440, 840)], [(300, 1040), (420, 1040)], seed=8)
    seg(cv, (586, 740), (606, 1040), 48, 3)
    for i in range(5):
        circ(cv, 592 + i * 4.2, 780 + i * 50, 7.5, 210)
        circ(cv, 592 + i * 4.2, 780 + i * 50, 7.5, 100, stroke=2)
    band_poly(cv, [(352, 600), (430, 596), (520, 616), (592, 646)], [(614, 716), (520, 694), (430, 678), (342, 690)], 164)
    ln(cv, [(356, 604), (430, 598), (520, 618), (590, 648)], 214, 6)          # gömlek kenarı
    ln(cv, [(344, 668), (430, 658), (520, 676), (606, 702)], 112, 2.2)
    chain(cv, [(384, 716), (470, 770), (556, 796), (650, 820)], 10, rx=17, ry=9.5)
    gem(cv, 660, 832, 11, shape="sq")


@reg(BUST, "dark_gown_collar")  # Isabel: koyu kadife elbise + altın-inci gerdanlık
def _b_darkgown(cv, d):
    body(cv, NECK["mid"], 70)
    folds(cv, [(320, 880), (430, 840), (540, 880)], [(290, 1040), (410, 1040), (560, 1040)], seed=9)
    ln(cv, [(350, 690), (430, 690), (520, 704), (600, 724)], 150, 22)
    for row, n in (([(396, 704), (470, 730), (540, 750), (614, 776)], 8), ([(372, 740), (460, 778), (548, 802), (642, 834)], 10)):
        a = cr(row, 16)
        q, _ = along(a, n)
        for i, (x, y) in enumerate(q):
            if i % 2 == 0:
                gem(cv, float(x), float(y), 12, shape="cab")
            else:
                pearl(cv, float(x), float(y), 8)
    ln(cv, [(574, 800), (590, 850)], 220, 3)
    cross_at(cv, 590, 892, 44)


@reg(BUST, "mantle_brooch")    # Şarlman: işlemeli manto yakası + büyük tokalı kopça
def _b_mantle(cv, d):
    body(cv, [(350, 650), (430, 652), (520, 666), (600, 692)], 78)
    sp = [(344, 646), (430, 662), (520, 684), (604, 714)]
    for k in range(8):
        a = 300 + k * 36
        ln(cv, [(a, 800 + k * 16), (a + 60, 860 + k * 14), (a + 100, 1000)], 54, 3)
    ln(cv, sp, 196, 40)
    ln(cv, [(x, y - 20) for x, y in sp], 120, 2)
    ln(cv, [(x, y + 20) for x, y in sp], 120, 2)
    beads_on(cv, [(x, y - 13) for x, y in sp], 10, r=4.6)
    beads_on(cv, [(x, y + 13) for x, y in sp], 10, r=4.6)
    for t in (0.18, 0.5, 0.82):
        x, y = pl(sp, t)
        gem(cv, x, y, 9.5, shape="dia")
    bx, by = 616, 770
    circ(cv, bx, by, 38, 232)
    circ(cv, bx, by, 38, 110, stroke=3)
    circ(cv, bx, by, 28, 120, stroke=2)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        gem(cv, bx + 31 * math.cos(a), by + 31 * math.sin(a), 5.2, shape="cab")
    gem(cv, bx, by, 14, shape="cab")


# ═════════════════════════════ başlıklar (2) ═════════════════════════════
@reg(HAT, "hennin")           # Burgonyalı Maria: geriye yatık kesik koni + elmas kafes + arkadan inen geniş peçe
def _hat_hennin(cv, d):
    veil = [(344, 112), (424, 88), (452, 112), (440, 220), (420, 340), (404, 480), (396, 640), (390, 790), (320, 836), (270, 790),
            (282, 620), (296, 450), (312, 300), (326, 190)]
    mass(cv, veil, 192, 0.4)
    ov(cv, 360, 400, 50, 220, 206, blur=26)
    top = [(380, 124), (352, 180), (330, 290)]
    bot = [(380, 800), (330, 790), (284, 770)]
    strands_between(cv, top, bot, 9, 142, 2.0, bend=-14, waves=0.9, amp=7, seed=81, jit=0.5, rev=False)
    ln(cv, [(452, 112), (440, 220), (420, 340), (404, 480), (396, 640), (390, 790)], 226, 5)
    cone = [(590, 270), (372, 306), (342, 118), (420, 86)]
    path = P(cone, True, 0.1)
    cv.fill(path, 214)
    with clip(cv, path):
        ov(cv, 440, 190, 90, 60, 232, blur=26, rot=-35)
        for k in range(-10, 14):
            seg(cv, (300 + k * 34, 60), (300 + k * 34 + 330, 380), 156, 1.7)
            seg(cv, (300 + k * 34 + 330, 60), (300 + k * 34, 380), 156, 1.7)
    cv.stroke(path, 108, 2.6)
    ln(cv, [(344, 116), (420, 88)], 236, 12)
    ln(cv, [(374, 298), (480, 282), (590, 262)], 234, 20)
    beads_on(cv, [(374, 298), (480, 282), (590, 262)], 9, r=5.6)
    gem(cv, 566, 262, 8, shape="dia")
    gem(cv, 470, 283, 8, shape="cab")
    ln(cv, [(594, 270), (580, 292)], 140, 2.2)


@reg(HAT, "gable_hood")       # Catherine: açılı çatı kenarlı gable hood + mücevherli billiment + arka lappet
def _hat_gable(cv, d):
    border = [(562, 156), (548, 226), (524, 300), (494, 380), (468, 452), (452, 524), (446, 590)]
    ridge = [(570, 150), (480, 150), (400, 186), (344, 262)]
    back = [(316, 380), (306, 520), (300, 680), (318, 790), (384, 806), (418, 716), (436, 620)]
    strip = [(556, 198), (582, 236), (592, 268), (548, 304), (524, 250)]
    mass(cv, strip, 184)
    flow(cv, [(560, 206), (572, 214), (580, 226)], [(536, 290), (548, 292), (560, 296)], 128, 1.8, bend=4, n=6)
    pts = ridge + back + border[::-1]
    fillp(cv, pts, 208, 0.16)
    cv.stroke(P(pts, True, 0.16), 108, 2.4)
    ov(cv, 440, 230, 90, 36, 226, blur=18, rot=-18)
    top = [(420, 190), (360, 260), (326, 400)]
    bot = [(430, 700), (372, 790), (320, 776)]
    strands_between(cv, top, bot, 8, 150, 2.4, bend=-12, waves=0.7, amp=7, seed=91, jit=0.5, rev=False)
    ln(cv, border, 234, 28, 0.3)
    ln(cv, border, 150, 1.8, 0.3)
    a = cr(border, 14)
    q, _ = along(a, 9)
    for i, (x, y) in enumerate(q):
        if i % 2 == 0:
            gem(cv, float(x), float(y), 9.5, shape="cab" if i % 4 == 0 else "dia")
        else:
            pearl(cv, float(x), float(y), 6)


@reg(HAT, "french_hood")      # Louise de Savoie: beyaz coif üstünde siyah hilal başlık + mücevherli iç kenar + arka perde
def _hat_french(cv, d):
    coif = [(592, 266), (548, 214), (450, 188), (366, 224), (330, 320), (340, 420), (420, 360), (500, 300), (560, 282)]
    mass(cv, coif, 196)
    mass_texture(cv, coif, 101, 70, (12, 20), math.radians(120), 0.4, 150, 1.5)
    outer = [(588, 254), (540, 200), (450, 172), (366, 206), (318, 300), (300, 420), (296, 560), (300, 700), (318, 800)]
    inner = [(352, 800), (350, 700), (346, 560), (352, 430), (372, 340), (420, 272), (500, 238), (560, 248)]
    pts = outer + inner
    fillp(cv, pts, 214, 0.36)
    cv.stroke(P(pts, True, 0.36), 108, 2.4)
    ov(cv, 420, 220, 100, 30, 232, blur=16, rot=-14)
    flow(cv, [(330, 360), (322, 420), (314, 480), (308, 540)], [(332, 800), (322, 800), (312, 796), (306, 790)], 150, 2.4, bend=-6, n=8)
    inn = [(560, 248), (500, 238), (420, 272), (372, 340), (352, 430)]
    ln(cv, inn, 232, 14, 0.4)
    beads_on(cv, inn, 8, r=6)
    ln(cv, [(588, 256), (540, 204), (452, 176), (368, 210)], 234, 12)
    gem(cv, 560, 248, 9, shape="dia")


@reg(HAT, "widow_wimple")     # Macaristanlı Mary: siyah dul başlığı + beyaz pileli barbe (boğaza inen) + peçe
def _hat_widow(cv, d):
    hood = [(600, 272), (562, 220), (452, 184), (366, 220), (326, 320), (312, 470), (304, 610), (296, 740), (312, 820), (384, 822),
            (424, 736), (440, 650), (452, 560), (470, 470), (500, 396), (536, 336), (574, 296)]
    mass(cv, hood, 208, 0.38)
    ov(cv, 420, 250, 90, 40, 228, blur=18, rot=-18)
    top = [(540, 230), (450, 196), (376, 230), (338, 300)]
    bot = [(448, 760), (418, 816), (360, 816), (312, 800)]
    strands_between(cv, top, bot, 10, 148, 2.4, bend=-12, waves=0.8, amp=7, seed=111, jit=0.5, rev=False)
    # beyaz pileli fırfır yaka (dul kıyafeti): çene açıkta kalır
    sp = [(448, 686), (496, 704), (552, 710), (618, 724)]
    ln(cv, sp, 214, 30)
    a = cr(sp, 12)
    q, _ = along(a, 14)
    for x, y in q:
        circ(cv, float(x), float(y) + 15, 9.5, 214)
        circ(cv, float(x), float(y) + 15, 9.5, 120, stroke=1.6)
    for x, y in q:
        circ(cv, float(x), float(y) - 15, 8, 206)
    ln(cv, [(x, y) for x, y in sp], 126, 1.8)
    ln(cv, [(436, 600), (484, 640), (534, 656), (584, 648)], 226, 7)
    ln(cv, [(602, 274), (576, 298), (540, 338), (504, 396), (474, 466)], 234, 12)
    if d.get("peak"):
        pk = [(604, 274), (594, 300), (566, 338), (532, 336), (556, 304), (574, 282)]
        fillp(cv, pk, 206, 0.3)
        cv.stroke(P(pk, True, 0.3), 108, 2.2)
        beads_on(cv, [(448, 686), (496, 704), (552, 710), (618, 724)], 10, r=5.2)


@reg(HAT, "toca")             # María Pacheco: yuvarlak dolanmış kumaş "toca" (yatay sargı) + arka peçe
def _hat_toca(cv, d):
    tail = [(356, 380), (336, 500), (312, 650), (300, 780), (336, 820), (372, 700), (394, 560), (404, 430)]
    mass(cv, tail, 196, 0.4)
    flow(cv, [(372, 420), (358, 440), (350, 460), (344, 480)], [(348, 800), (334, 806), (322, 800), (314, 790)], 146, 2.2, bend=-6, n=8)
    wrap = [(598, 276), (572, 214), (490, 166), (394, 172), (332, 230), (312, 330), (320, 430), (358, 486), (418, 446), (442, 384), (492, 334), (554, 298)]
    path = P(wrap, True, 0.45)
    cv.fill(path, 210)
    with clip(cv, path):
        ov(cv, 450, 214, 130, 54, 232, blur=24)
        for k in range(7):                                  # yatay sargı rulolarının kavisleri
            y = 190 + k * 40
            ln(cv, [(300, y + 50), (400, y), (500, y - 6), (590, y + 36)], 150, 3.0, 0.5)
            ln(cv, [(300, y + 62), (400, y + 12), (500, y + 6), (590, y + 48)], 182, 1.4, 0.5)
    cv.stroke(path, 108, 2.6)
    ln(cv, [(600, 278), (562, 298), (504, 334), (450, 386)], 234, 12)
    gem(cv, 566, 270, 8, shape="dia")


@reg(HAT, "child_cap")        # çocuk Karl: küçük yumuşak bere + kısa tüy
def _hat_child(cv, d):
    base = [(352, 304), (350, 248), (392, 210), (470, 192), (548, 206), (594, 242), (602, 272), (560, 286), (500, 270), (430, 278), (380, 306)]
    fillp(cv, base, 214)
    ov(cv, 480, 220, 90, 24, 232, blur=12)
    _rim(cv, [(360, 298), (440, 276), (520, 270), (598, 282)], 16, 232)
    ln(cv, [(410, 212), (470, 228), (540, 232)], 156, 2.2)
    circ(cv, 574, 262, 13, 240)
    circ(cv, 574, 262, 13, 110, stroke=2.4)
    gem(cv, 574, 262, 6, shape="dia")
    plume(cv, [(584, 234), (614, 196), (650, 184), (680, 202)], 34, g=236)


@reg(HAT, "kalpak")           # Zápolya: uzun kürk kalpak + mücevherli tokalı tüy
def _hat_kalpak(cv, d):
    cap = [(368, 308), (346, 190), (352, 138), (440, 112), (540, 112), (620, 134), (626, 192), (610, 270), (560, 284), (484, 266), (420, 280)]
    path = P(cap, True, 0.2)
    fur_fill(cv, path, 204, seed=121, n=420, L=(14, 26), ang=math.radians(-80), sd=0.7)
    with clip(cv, path):
        ov(cv, 486, 200, 120, 60, 224, blur=26)
    cv.stroke(path, 108, 2.6)
    ln(cv, [(366, 296), (430, 278), (520, 270), (606, 276)], 226, 14)
    # tüy tokası
    bx, by = 592, 204
    circ(cv, bx, by, 26, 244)
    circ(cv, bx, by, 26, 108, stroke=3)
    for k in range(6):
        a = k / 6 * 2 * math.pi
        pearl(cv, bx + 18 * math.cos(a), by + 18 * math.sin(a), 4.4)
    gem(cv, bx, by, 9, shape="dia")
    plume(cv, [(598, 194), (596, 158), (600, 130), (606, 112)], 28, g=238)
    plume(cv, [(586, 190), (576, 158), (568, 134)], 20, g=232)


@reg(HAT, "beret_wide")       # Frederik: geniş, yumuşak, sade koyu bere + kordon
def _hat_beretwide(cv, d):
    pts = [(298, 300), (304, 232), (364, 182), (470, 160), (574, 170), (648, 208), (674, 254), (642, 286), (582, 292), (500, 272), (420, 284), (340, 312)]
    path = P(pts, True, 0.45)
    cv.fill(path, 214)
    with clip(cv, path):
        ov(cv, 490, 208, 160, 40, 232, blur=18)
    ln(cv, [(372, 214), (440, 196), (520, 200)], 154, 2.6)
    ln(cv, [(420, 242), (500, 226), (590, 232)], 154, 2.4)
    ln(cv, [(350, 262), (400, 246), (452, 244)], 154, 2.2)
    cv.stroke(path, 108, 2.6)
    rim = [(330, 304), (430, 282), (520, 274), (600, 290), (652, 262)]
    _rim(cv, rim, 20, 232)
    ln(cv, [(330, 316), (430, 296), (520, 288), (600, 304)], 200, 3)
    if not d.get("nobadge"):
        circ(cv, 604, 270, 15, 242)
        circ(cv, 604, 270, 15, 108, stroke=2.6)
        gem(cv, 604, 270, 7, shape="cab")
    if d.get("plumed"):
        plume(cv, [(596, 246), (640, 196), (690, 184), (722, 206)], 32, g=236)


@reg(HAT, "beret_feathers")   # Johann Friedrich: iri tüylü bere (kenarda yarıklı) + broş
def _hat_beretfeath(cv, d):
    pts = [(292, 302), (296, 230), (358, 176), (468, 152), (580, 164), (658, 204), (690, 254), (656, 288), (590, 294), (504, 274), (420, 286), (336, 316)]
    path = P(pts, True, 0.45)
    cv.fill(path, 214)
    with clip(cv, path):
        ov(cv, 490, 204, 170, 40, 234, blur=18)
    for i in range(10):
        e = pl([(326, 306), (430, 284), (520, 276), (600, 292), (660, 264)], 0.04 + 0.92 * i / 9)
        seg(cv, (e[0], e[1] - 8), (e[0] + 4, e[1] - 26), 150, 2.4)
    ln(cv, [(380, 212), (450, 192), (528, 196)], 154, 2.4)
    cv.stroke(path, 108, 2.6)
    _rim(cv, [(326, 306), (430, 284), (520, 276), (600, 292), (660, 264)], 22, 234)
    plume(cv, [(600, 262), (560, 190), (480, 140), (390, 126), (322, 150), (284, 214), (278, 292)], 48, g=238)
    plume(cv, [(612, 262), (640, 200), (600, 130), (520, 96)], 34, g=234)
    plume(cv, [(620, 266), (672, 214), (700, 160)], 26, g=230)
    bx, by = 612, 268
    circ(cv, bx, by, 28, 246)
    circ(cv, bx, by, 28, 108, stroke=3)
    for k in range(7):
        a = k / 7 * 2 * math.pi
        pearl(cv, bx + 20 * math.cos(a), by + 20 * math.sin(a), 4.6)
    gem(cv, bx, by, 10, shape="dia")


@reg(HAT, "mascapaicha")      # Atahualpa: dokuma llautu bandı + kızıl püskül (borla) + iki dik tüy + altın plaka
def _hat_masca(cv, d):
    top = [(602, 244), (520, 224), (430, 224), (358, 248)]
    bot = [(354, 304), (430, 284), (520, 284), (598, 304)]
    band_poly(cv, top, bot[::-1], 222, groove=110)
    path = P(top + bot[::-1], True, 0.35)
    with clip(cv, path):
        for k in range(-8, 16):
            seg(cv, (330 + k * 24, 330), (330 + k * 24 + 70, 210), 150, 2.0)
        ln(cv, [(356, 272), (440, 254), (520, 254), (600, 274)], 120, 2.0)
    for tt in (0.0, 1.0):
        pass
    ln(cv, [(356, 244), (430, 222), (520, 222), (602, 242)], 238, 7)
    ln(cv, [(354, 306), (430, 286), (520, 286), (598, 306)], 238, 7)
    # püskül (borla): bandın önünden alna sarkan kalın saçaklı demet
    tas = [(574, 292), (618, 300), (632, 348), (590, 352)]
    fillp(cv, tas, 234, 0.2)
    cv.stroke(P(tas, True, 0.2), 104, 2.4)
    for i in range(6):
        seg(cv, (584 + i * 8, 306 + i * 1.4), (592 + i * 8, 348 + i * 0.6), 118, 2.2)
    for i in range(5):
        circ(cv, 592 + i * 9, 352, 5.6, 236)
    circ(cv, 598, 296, 14, 246)
    circ(cv, 598, 296, 14, 108, stroke=2.4)
    # altın plaka
    circ(cv, 536, 266, 17, 246)
    circ(cv, 536, 266, 17, 106, stroke=2.6)
    circ(cv, 536, 266, 8, 130, stroke=2)
    # iki dik tüy
    plume(cv, [(562, 236), (556, 180), (562, 128), (578, 84)], 46, g=238)
    plume(cv, [(520, 232), (508, 184), (504, 140), (512, 102)], 40, g=234)


@reg(HAT, "xiuhhuitzolli")    # Moctezuma: turkuaz mozaik diadem (sivri ön levha) + kuetzal tüyü yelesi + arka şerit
def _hat_xiuh(cv, d):
    # arka tüy yelesi (quetzal)
    plume(cv, [(420, 236), (372, 168), (320, 128), (262, 124)], 34, g=232)
    plume(cv, [(440, 232), (406, 156), (374, 110), (334, 84)], 32, g=236)
    plume(cv, [(470, 230), (454, 150), (446, 100), (432, 74)], 30, g=234)
    top = [(604, 250), (520, 236), (430, 238), (360, 258)]
    bot = [(354, 304), (430, 286), (520, 286), (598, 304)]
    band_poly(cv, top, bot[::-1], 220, groove=110)
    # sivri ön levha
    plate = [(488, 256), (498, 194), (518, 134), (550, 82), (582, 124), (604, 192), (616, 268)]
    path = P(plate, True, 0.3)
    cv.fill(path, 226)
    with clip(cv, path):
        for k in range(-4, 14):
            seg(cv, (480 + k * 15, 60), (480 + k * 15, 300), 150, 1.6)
        for k in range(-2, 16):
            seg(cv, (470, 70 + k * 15), (660, 70 + k * 15), 150, 1.6)
        ov(cv, 552, 170, 40, 84, 246, blur=16)
    cv.stroke(path, 106, 2.6)
    path2 = P(top + bot[::-1], True, 0.35)
    with clip(cv, path2):
        for k in range(-6, 14):
            seg(cv, (330 + k * 18, 330), (330 + k * 18, 210), 150, 1.6)
        for k in range(0, 6):
            seg(cv, (330, 232 + k * 14), (640, 232 + k * 14), 150, 1.6)
    ln(cv, [(356, 244), (430, 224), (520, 226), (604, 244)], 240, 6)
    ln(cv, [(354, 306), (430, 288), (520, 288), (598, 306)], 240, 6)
    gem(cv, 552, 190, 11, shape="dia")
    # arka şerit
    ribbon(cv, [(358, 292), (332, 370), (318, 470)], 24, 14, 218, n=10, seam=2.0, seamg=140)


@reg(HAT, "seaman_cap")       # Magellan: yuvarlak denizci şapkası + öne kıvrık siperlik
def _hat_seaman(cv, d):
    crown = [(350, 302), (352, 238), (398, 196), (478, 178), (556, 194), (600, 232), (608, 266), (570, 278), (480, 262), (400, 278)]
    fillp(cv, crown, 214)
    ov(cv, 480, 214, 100, 28, 232, blur=12)
    _rim(cv, [(358, 298), (440, 276), (520, 270), (600, 278)], 22, 232)
    visor = [(560, 280), (646, 268), (660, 244), (606, 248)]
    fillp(cv, visor, 226, 0.25)
    cv.stroke(P(visor, True, 0.25), 108, 2.2)
    circ(cv, 480, 186, 9, 240)
    circ(cv, 480, 186, 9, 108, stroke=2.2)
    for k in range(4):
        ln(cv, [(420 + k * 38, 276), (426 + k * 34, 224), (440 + k * 30, 192)], 156, 2.0)


@reg(HAT, "biretta")          # Sepúlveda: dilimli bilgin bonesi + tutam
def _hat_biretta(cv, d):
    base = [(356, 300), (364, 238), (410, 208), (520, 198), (584, 218), (602, 266), (580, 284), (480, 266), (398, 284)]
    fillp(cv, base, 212, 0.3)
    ov(cv, 480, 226, 100, 24, 228, blur=10)
    ln(cv, [(374, 252), (420, 200), (470, 168)], 234, 13)
    ln(cv, [(480, 262), (500, 210), (510, 168)], 234, 13)
    ln(cv, [(570, 270), (574, 216), (556, 176)], 234, 13)
    ln(cv, [(374, 252), (420, 200), (470, 168)], 150, 1.6)
    ln(cv, [(480, 262), (500, 210), (510, 168)], 150, 1.6)
    ln(cv, [(570, 270), (574, 216), (556, 176)], 150, 1.6)
    _rim(cv, [(362, 294), (440, 274), (520, 268), (590, 280)], 16, 230)
    circ(cv, 514, 156, 15, 238)
    circ(cv, 514, 156, 15, 108, stroke=2.4)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        seg(cv, (514 + 10 * math.cos(a), 156 + 10 * math.sin(a)), (514 + 20 * math.cos(a), 156 + 20 * math.sin(a)), 150, 1.6)


@reg(HAT, "merchant_cap")     # Welser: yüksek, bol, pileli tüccar başlığı
def _hat_merchant(cv, d):
    pts = [(354, 302), (344, 214), (380, 148), (466, 124), (558, 144), (606, 204), (608, 264), (566, 282), (484, 264), (410, 280)]
    path = P(pts, True, 0.4)
    cv.fill(path, 212)
    with clip(cv, path):
        ov(cv, 480, 190, 100, 60, 230, blur=22)
        for k in range(9):
            ln(cv, [(374 + k * 28, 280), (372 + k * 28, 210), (404 + k * 24, 140)], 152, 2.2, 0.5)
    cv.stroke(path, 108, 2.6)
    ln(cv, [(344, 214), (380, 168), (440, 150), (520, 160), (574, 190)], 236, 8)
    _rim(cv, [(360, 296), (440, 274), (520, 268), (598, 280)], 18, 232)
    circ(cv, 470, 126, 12, 240)
    circ(cv, 470, 126, 12, 108, stroke=2.2)
    circ(cv, 574, 264, 12, 242)
    circ(cv, 574, 264, 12, 108, stroke=2.2)


@reg(HAT, "royal_cap_crown")  # Lajos II: kadife bere + mücevherli taç bandı + zambak uçlar
def _hat_royalcap(cv, d):
    cap = [(346, 300), (344, 230), (394, 184), (486, 164), (572, 182), (614, 226), (620, 268), (582, 286), (500, 268), (420, 280), (372, 308)]
    fillp(cv, cap, 214)
    ov(cv, 490, 214, 110, 28, 232, blur=12)
    ln(cv, [(410, 206), (480, 222), (560, 226)], 156, 2.2)
    top = [(352, 266), (420, 248), (500, 242), (574, 252), (618, 266)]
    bot = [(618, 304), (560, 292), (500, 288), (420, 292), (360, 308)]
    band_poly(cv, top, bot, 228, groove=108)
    for i, t in enumerate((0.12, 0.3, 0.5, 0.7, 0.88)):
        x, y = pl(top, t)
        fleuron(cv, x, y + 4, 54)
        a, b = pl(top, t), pl(bot, 1 - t)
    for i, t in enumerate((0.2, 0.5, 0.8)):
        a, b = pl(top, t), pl(bot, 1 - t)
        gem(cv, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 8.5, shape="cab" if i % 2 == 0 else "dia")
    plume(cv, [(412, 212), (376, 150), (326, 116), (270, 126)], 42, g=236)


@reg(HAT, "flatcap_x")        # genç Karl: geniş yassı bere + mücevher + kısa tüy
def _hat_flatcap_x(cv, d):
    base = [(326, 298), (336, 242), (392, 202), (480, 188), (560, 198), (612, 228), (634, 262), (606, 280), (536, 266), (450, 278), (372, 306)]
    fillp(cv, base, 216)
    ov(cv, 480, 226, 130, 28, 234, blur=14)
    _rim(cv, [(336, 296), (430, 276), (520, 268), (606, 280)], 20, 234)
    ln(cv, [(384, 228), (452, 212), (530, 216)], 156, 2.4)
    ln(cv, [(366, 262), (410, 244), (462, 242)], 156, 2.0)
    circ(cv, 584, 262, 15, 242)
    circ(cv, 584, 262, 15, 108, stroke=2.6)
    gem(cv, 584, 262, 7, shape="dia")
    plume(cv, [(590, 244), (626, 204), (668, 188), (700, 204)], 32, g=236)


@reg(HAT, "kalot")            # Doria: kapalı küçük kalot + düğme
def _hat_kalot(cv, d):
    base = [(358, 320), (366, 244), (432, 200), (522, 204), (584, 246), (596, 292), (530, 278), (452, 284), (396, 332)]
    fillp(cv, base, 214, 0.4)
    ov(cv, 490, 232, 90, 24, 232, blur=10)
    _rim(cv, [(372, 314), (450, 290), (530, 282), (594, 294)], 14, 230)
    for k in range(7):
        ln(cv, [(388 + k * 32, 290), (396 + k * 30, 238), (420 + k * 26, 208)], 154, 2.0)
    circ(cv, 488, 206, 10, 238)
    circ(cv, 488, 206, 10, 108, stroke=2.2)


@reg(HAT, "toque_brim")       # Padilla: yüksek yumuşak başlık + kalın kıvrık kenar
def _hat_toque(cv, d):
    crown = [(358, 298), (352, 224), (394, 172), (470, 154), (552, 168), (598, 212), (606, 262), (570, 280), (490, 264), (420, 276)]
    fillp(cv, crown, 214)
    ov(cv, 480, 200, 100, 36, 232, blur=14)
    ln(cv, [(400, 190), (470, 214), (550, 220)], 154, 2.4)
    ln(cv, [(380, 240), (430, 220), (500, 226)], 154, 2.2)
    _rim(cv, [(350, 302), (430, 278), (520, 270), (610, 284)], 30, 234)
    ln(cv, [(350, 302), (430, 278), (520, 270), (610, 284)], 110, 1.6)


@reg(HAT, "feather_beret")    # Bravo: öne eğik küçük bere + uzun sarkık tüy
def _hat_featherberet(cv, d):
    pts = [(344, 296), (350, 232), (402, 190), (490, 176), (566, 196), (606, 238), (610, 270), (566, 284), (496, 268), (420, 280), (372, 304)]
    fillp(cv, pts, 214)
    ov(cv, 490, 218, 100, 24, 232, blur=12)
    _rim(cv, [(356, 296), (440, 274), (520, 268), (606, 280)], 18, 232)
    for k in range(5):
        ln(cv, [(380 + k * 44, 270), (410 + k * 40, 224), (440 + k * 36, 196)], 156, 2.0)
    circ(cv, 588, 256, 13, 242)
    circ(cv, 588, 256, 13, 108, stroke=2.4)
    gem(cv, 588, 256, 6, shape="dia")
    plume(cv, [(592, 246), (574, 188), (510, 150), (430, 140), (362, 170), (320, 230)], 36, g=236)


@reg(HAT, "plain_coif")       # Maldonado: kulağı örten sade koyu başlık
def _hat_coif(cv, d):
    pts = [(342, 330), (348, 238), (406, 192), (488, 180), (560, 206), (600, 262), (586, 294), (520, 278), (452, 284), (398, 340), (384, 432), (352, 424)]
    fillp(cv, pts, 214, 0.4)
    ov(cv, 470, 224, 100, 30, 230, blur=14)
    _rim(cv, [(358, 306), (440, 282), (520, 276), (592, 290)], 12, 226)
    ln(cv, [(354, 330), (384, 340), (392, 420)], 150, 2.2)
    for k in range(6):
        ln(cv, [(386 + k * 34, 280), (396 + k * 30, 232), (420 + k * 26, 200)], 154, 1.9)


# ═════════════════════════════ giysi / büst (2) ═════════════════════════════
def neck_jewels(cv, row, n, r_gem=10, r_pearl=6.4, every=2):
    a = cr(row, 16)
    q, _ = along(a, n)
    for i, (x, y) in enumerate(q):
        if i % every == 0:
            gem(cv, float(x), float(y), r_gem, shape="cab" if (i // every) % 2 == 0 else "dia")
        else:
            pearl(cv, float(x), float(y), r_pearl)


def pendant_cross(cv, x, y, s=44):
    ln(cv, [(x - 14, y - 52), (x - 4, y - 22)], 214, 2.6)
    ln(cv, [(x + 14, y - 52), (x + 4, y - 22)], 214, 2.6)
    cross_at(cv, x, y + s * 0.5, s)
    gem(cv, x, y + s * 0.02, 6, shape="cab")


@reg(BUST, "jeweled_gown")     # Maria (Burgonya) / Catherine: kare dekolte, mücevherli kenar, inci kolye
def _b_jgown(cv, d):
    body(cv, NECK["low"], 70)
    folds(cv, [(300, 900), (420, 890), (540, 930)], [(280, 1040), (400, 1040), (540, 1040)], seed=21)
    chem = [(352, 706), (440, 728), (530, 764), (610, 806), (626, 850), (540, 806), (440, 776), (350, 748)]
    fillp(cv, chem, 138, 0.3)
    for k in range(7):
        seg(cv, (372 + k * 36, 730 + k * 10), (380 + k * 36, 758 + k * 16), 106, 1.8)
    sp = [(344, 750), (440, 782), (540, 820), (636, 870)]
    ln(cv, sp, 214, 36)
    ln(cv, [(x, y - 18) for x, y in sp], 108, 1.8)
    ln(cv, [(x, y + 18) for x, y in sp], 108, 1.8)
    neck_jewels(cv, sp, 9, 9.5, 6)
    beads_on(cv, [(402, 706), (470, 738), (540, 762), (604, 794)], 10, r=5.4)
    if d.get("gv") == "tudor":
        pendant_cross(cv, 566, 800, 40)
    else:
        ln(cv, [(568, 776), (574, 818)], 210, 2.4)
        gem(cv, 576, 832, 11, shape="dia")
        pearl(cv, 564, 858, 6)
        pearl(cv, 590, 858, 6)


@reg(BUST, "gown_fur")         # Louise: koyu elbise + kürk kenarlı dekolte + uzun mücevher kolye
def _b_gownfur(cv, d):
    body(cv, NECK["mid"], 70)
    folds(cv, [(300, 900), (420, 870), (540, 910)], [(280, 1040), (400, 1040), (540, 1040)], seed=22)
    fur_band(cv, [(390, 694), (440, 706), (520, 726), (610, 768), (662, 840)], 58, seed=23, g=172)
    neck_jewels(cv, [(396, 722), (470, 752), (548, 778), (626, 816)], 9, 9.5, 6)
    chain(cv, [(430, 740), (500, 800), (560, 850)], 6, rx=11, ry=7, g=224, w=3.4)


@reg(BUST, "black_dress")      # Mary (Macar): sade siyah elbise + omuz kıvrımları
def _b_blackdress(cv, d):
    body(cv, NECK["high"], 66)
    folds(cv, [(300, 880), (400, 820), (520, 860), (610, 800)], [(280, 1040), (380, 1040), (500, 1040), (620, 1040)], seed=24, g=46, bend=18)
    ln(cv, [(350, 700), (430, 700), (520, 724), (606, 760)], 150, 12)
    circ(cv, 590, 840, 13, 240)
    circ(cv, 590, 840, 13, 106, stroke=2.4)
    gem(cv, 590, 840, 6, shape="dia")


@reg(BUST, "dark_gown_plain")  # Pacheco: yüksek yakalı koyu elbise + ince fırfır + haç
def _b_gownplain(cv, d):
    body(cv, NECK["high"], 68)
    folds(cv, [(300, 880), (420, 830), (540, 870)], [(280, 1040), (400, 1040), (540, 1040)], seed=25)
    band_poly(cv, [(352, 606), (430, 606), (520, 626), (592, 652)], [(612, 720), (520, 698), (430, 684), (344, 692)], 154)
    for k in range(11):
        pt = pl([(352, 600), (430, 600), (520, 620), (592, 646)], k / 10)
        circ(cv, pt[0], pt[1] - 4, 8, 210)
    ln(cv, [(344, 680), (430, 672), (520, 690), (606, 714)], 108, 2.2)
    chain(cv, [(404, 726), (480, 776), (556, 800)], 7, rx=12, ry=7.5, g=226, w=3.4)
    pendant_cross(cv, 586, 808, 40)


@reg(BUST, "child_doublet")    # çocuk Karl: beyaz yaka + düğmeler + küçük kolye (kısa boyun)
def _b_child(cv, d):
    nk = [(350, 664), (430, 662), (520, 672), (602, 694)]
    body(cv, nk, 76)
    folds(cv, [(320, 900), (440, 850)], [(300, 1040), (420, 1040)], seed=26)
    seg(cv, (588, 730), (610, 1040), 50, 3)
    for i in range(4):
        circ(cv, 596 + i * 5, 780 + i * 50, 7, 214)
        circ(cv, 596 + i * 5, 780 + i * 50, 7, 104, stroke=2)
    sp = [(350, 664), (430, 668), (520, 682), (604, 706)]
    ln(cv, sp, 206, 26)
    ln(cv, [(x, y + 13) for x, y in sp], 110, 1.8)
    a = cr(sp, 10)
    q, _ = along(a, 12)
    for x, y in q:
        circ(cv, float(x), float(y) + 14, 7.5, 206)
    ln(cv, [(420, 706), (500, 766), (570, 790)], 218, 3)
    gem(cv, 574, 800, 10, shape="dia")


@reg(BUST, "leather_jerkin")   # Padilla: deri yelek, çapraz bağcık
def _b_jerkin(cv, d):
    body(cv, NECK["mid"], 72)
    folds(cv, [(300, 900), (430, 850)], [(280, 1040), (410, 1040)], seed=27)
    band_poly(cv, [(352, 662), (430, 658), (520, 676), (596, 700)], [(612, 740), (520, 724), (430, 712), (344, 720)], 148)
    ln(cv, [(352, 660), (430, 654), (520, 672), (596, 696)], 206, 5)
    for i in range(5):
        y = 770 + i * 40
        seg(cv, (586 + i * 4, y), (632 + i * 4, y + 30), 222, 3.2)
        seg(cv, (632 + i * 4, y), (586 + i * 4, y + 30), 222, 3.2)
        circ(cv, 586 + i * 4, y, 4.6, 238)
        circ(cv, 632 + i * 4, y, 4.6, 238)
    ln(cv, [(300, 800), (400, 760), (500, 784)], 112, 2.4)


@reg(BUST, "cloak_buttons")    # Bravo: omuza atılmış pelerin + yüksek yaka + düğmeler
def _b_cloak(cv, d):
    body(cv, NECK["high"], 72)
    ln(cv, [(250, 880), (350, 830), (470, 850), (570, 920), (620, 1040)], 112, 3)
    folds(cv, [(280, 960), (390, 900)], [(270, 1040), (380, 1040)], seed=28)
    band_poly(cv, [(352, 616), (430, 612), (520, 632), (594, 660)], [(612, 722), (520, 700), (430, 688), (344, 698)], 160)
    ln(cv, [(344, 672), (430, 664), (520, 682), (606, 708)], 110, 2.2)
    for i in range(5):
        circ(cv, 600 + i * 4.2, 760 + i * 44, 8.5, 226)
        circ(cv, 600 + i * 4.2, 760 + i * 44, 8.5, 104, stroke=2.2)
    chain(cv, [(380, 716), (460, 772), (546, 800)], 8, rx=14, ry=8, g=230, w=3.6)


@reg(BUST, "lawyer_robe")      # Maldonado: kadife yüzlü uzun cüppe + iki beyaz sarkık yaka
def _b_lawyer(cv, d):
    body(cv, NECK["mid"], 72)
    folds(cv, [(300, 880), (420, 840), (520, 890)], [(280, 1040), (400, 1040), (540, 1040)], seed=29)
    left = [(394, 694), (448, 706), (520, 726), (590, 770), (630, 860), (660, 1040)]
    ln(cv, left, 150, 62)
    ln(cv, [(x - 31, y - 4) for x, y in left], 106, 2.2)
    ln(cv, [(x + 31, y + 4) for x, y in left], 106, 2.2)
    for k in range(2):
        fillq(cv, [(588 + k * 26, 740 + k * 6), (616 + k * 26, 750 + k * 6), (630 + k * 26, 838), (600 + k * 26, 832)], 208)
        cv.stroke(poly([(588 + k * 26, 740 + k * 6), (616 + k * 26, 750 + k * 6), (630 + k * 26, 838), (600 + k * 26, 832)]), 108, 2)
    ln(cv, [(394, 676), (448, 688), (520, 706), (590, 746)], 204, 8)


@reg(BUST, "fur_gown_wide")    # Frederik / JF: devasa kürk şal yaka + madalyonlu zincir
def _b_furwide(cv, d):
    body(cv, NECK["mid"], 72)
    folds(cv, [(300, 900), (420, 860)], [(280, 1040), (400, 1040)], seed=31)
    w = d.get("furw", 112)
    fur_band(cv, [(384, 676), (440, 694), (520, 716), (622, 764), (694, 850), (744, 960)], w, seed=32, g=176, rows=4)
    if not d.get("nochain"):
        chain(cv, [(372, 704), (452, 756), (548, 790), (636, 834)], 11, rx=17, ry=10)
        circ(cv, 662, 872, 30, 242)
        circ(cv, 662, 872, 30, 106, stroke=3.2)
        circ(cv, 662, 872, 20, 120, stroke=2.2)
        if d.get("garm") == "saxony":
            fillq(cv, [(662, 852), (680, 872), (662, 892), (644, 872)], 250)
        else:
            gem(cv, 662, 872, 10, shape="dia")
    if d.get("slash"):
        for k in range(6):
            seg(cv, (250 + k * 20, 900 + k * 4), (300 + k * 20, 960 + k * 4), 100, 3)


@reg(BUST, "courtly_jacket")   # Lajos: brokar lozenge desenli ceket + kürk kenarlı pelerin + inci yaka
def _b_courtly(cv, d):
    body(cv, NECK["mid"], 76)
    path = P([(110, 1070), (140, 970), (196, 868), (262, 792), (316, 744), (350, 688), (430, 686), (520, 696), (600, 716), (690, 766), (770, 828), (860, 916), (920, 1070)], True, 0.4)
    with clip(cv, path):
        for k in range(-4, 14):
            seg(cv, (160 + k * 46, 760), (160 + k * 46 + 300, 1100), 112, 2.0)
            seg(cv, (160 + k * 46 + 300, 760), (160 + k * 46, 1100), 112, 2.0)
        for r in range(7):
            for k in range(-4, 14):
                x, y = 160 + k * 46 + (23 if r % 2 else 0), 790 + r * 46
                circ(cv, x, y, 3.6, 200)
    fur_band(cv, [(222, 906), (284, 826), (336, 774)], 40, seed=41, g=172)
    sp = [(350, 688), (430, 692), (520, 706), (604, 730)]
    ln(cv, sp, 214, 24)
    beads_on(cv, [(x, y - 7) for x, y in sp], 11, r=5.4)
    beads_on(cv, [(x, y + 9) for x, y in sp], 11, r=5.4)
    chain(cv, [(410, 740), (490, 796), (566, 820)], 8, rx=13, ry=8, g=232, w=3.4)
    gem(cv, 576, 832, 11, shape="dia")


@reg(BUST, "dolama")           # Zápolya: macar dolaması — yüksek kürk yaka, enlemesine kordon kapamaları, mente
def _b_dolama(cv, d):
    body(cv, NECK["mid"], 72)
    fur_band(cv, [(222, 906), (292, 826), (350, 784), (420, 800)], 46, seed=51, g=172)
    for i in range(5):
        y = 780 + i * 34
        seg(cv, (486 - i * 6, y), (626 + i * 7, y), 224, 7)
        ov(cv, 486 - i * 6, y, 13, 9, 224, stroke=3)
        circ(cv, 626 + i * 7, y, 7.5, 240)
    seg(cv, (620, 740), (660, 1040), 52, 3)
    fur_band(cv, [(372, 676), (440, 692), (520, 712), (606, 744)], 54, seed=52, g=176, rows=3)


@reg(BUST, "dark_robe")        # Doria: şal yakalı koyu cüppe + Altın Post zinciri
def _b_darkrobe(cv, d):
    body(cv, NECK["mid"], 70)
    folds(cv, [(290, 900), (420, 860), (520, 900)], [(270, 1040), (400, 1040), (520, 1040)], seed=61)
    lap = [(384, 694), (440, 706), (520, 728), (596, 770), (650, 860), (690, 980)]
    ln(cv, lap, 156, 72)
    ln(cv, [(x - 36, y - 6) for x, y in lap], 106, 2.4)
    ln(cv, [(x + 36, y + 6) for x, y in lap], 106, 2.4)
    chain(cv, [(386, 706), (470, 760), (556, 794), (644, 838)], 11, rx=18, ry=10.5, g=238)
    circ(cv, 668, 856, 16, 244)
    circ(cv, 668, 856, 16, 106, stroke=2.6)
    gem(cv, 668, 856, 6, shape="dia")


@reg(BUST, "tunic_inca")       # Atahualpa: tokapu kareli unku bandı + saçaklı yacolla
def _b_unku(cv, d):
    body(cv, NECK["low"], 76)
    for k in range(9):
        ln(cv, [(250 + k * 18, 930), (270 + k * 18, 990), (262 + k * 18, 1040)], 46, 2.4, 0.4)
    sp = [(340, 700), (430, 728), (530, 770), (630, 832)]
    ln(cv, sp, 170, 62)
    a = cr(sp, 16)
    q, tg = along(a, 11)
    for i, (x, y) in enumerate(q):
        ang = math.degrees(math.atan2(tg[i][1], tg[i][0]))
        c = cv.c
        c.save(); c.translate(float(x), float(y)); c.rotate(ang)
        c.drawRect(skia.Rect.MakeLTRB(-22, -22, 22, 22), _paint(232))
        c.drawRect(skia.Rect.MakeLTRB(-22, -22, 22, 22), _paint(108, 2.6))
        c.drawRect(skia.Rect.MakeLTRB(-13, -13, 13, 13), _paint(160, 2.2))
        if i % 2 == 0:
            c.drawRect(skia.Rect.MakeLTRB(-7, -7, 7, 7), _paint(252))
        else:
            c.drawLine(-13, -13, 13, 13, _paint(120, 2.2))
            c.drawLine(13, -13, -13, 13, _paint(120, 2.2))
        c.restore()
    for k in range(12):
        t = k / 11
        x, y = pl([(326, 740), (300, 840), (270, 960)], t)
        seg(cv, (x, y), (x - 12, y + 40), 190, 3)
    ln(cv, [(330, 760), (300, 830), (262, 1000)], 118, 2.2)


@reg(BUST, "tilmatli")         # Moctezuma: omuzda düğümlü tilmatli + basamaklı kenar + yeşim gerdanlık
def _b_tilma(cv, d):
    body(cv, NECK["mid"], 74)
    folds(cv, [(300, 920), (420, 880)], [(280, 1040), (400, 1040)], seed=71)
    # basamaklı (xicalcoliuhqui) kenar şeridi
    top = [(260, 790), (330, 760), (400, 770)]
    sp = [(260, 960), (360, 900), (470, 884), (570, 906), (650, 960)]
    ln(cv, sp, 150, 46)
    pts = []
    a = cr(sp, 16)
    q, tg = along(a, 14)
    for i, (x, y) in enumerate(q):
        ang = math.degrees(math.atan2(tg[i][1], tg[i][0]))
        cv.c.save(); cv.c.translate(float(x), float(y)); cv.c.rotate(ang)
        st = [(-14, 14), (-14, 2), (-4, 2), (-4, -8), (6, -8), (6, -16)] if i % 2 == 0 else [(-14, -14), (-14, -2), (-4, -2), (-4, 8), (6, 8), (6, 16)]
        cv.c.drawPath(poly(st, False), _paint(236, 5.0))
        cv.c.restore()
    # yeşim gerdanlık (çok sıra)
    for row, n in (([(392, 696), (468, 724), (540, 748), (616, 778)], 11), ([(374, 722), (462, 756), (548, 782), (636, 816)], 12),
                   ([(358, 748), (454, 788), (556, 816), (652, 854)], 13)):
        beads_on(cv, row, n, r=7.4, g=238)
    gem(cv, 556, 818, 13, shape="cab")
    # omuz düğümü
    kx, ky = 640, 900
    circ(cv, kx, ky, 28, 232)
    circ(cv, kx, ky, 28, 106, stroke=3)
    ln(cv, [(kx - 22, ky - 12), (kx, ky), (kx + 22, ky + 12)], 120, 2.6)
    ln(cv, [(kx + 22, ky - 12), (kx, ky), (kx - 22, ky + 12)], 120, 2.6)


@reg(BUST, "explorer_doublet")  # Magellan: yüksek yaka + çapraz bağcık + haç madalyonu
def _b_explorer(cv, d):
    body(cv, NECK["high"], 72)
    folds(cv, [(300, 900), (420, 850)], [(280, 1040), (400, 1040)], seed=81)
    band_poly(cv, [(352, 610), (430, 606), (520, 626), (592, 654)], [(612, 722), (520, 700), (430, 684), (344, 694)], 158)
    ln(cv, [(354, 612), (430, 608), (520, 628), (590, 656)], 212, 5)
    for i in range(4):
        y = 748 + i * 38
        seg(cv, (586 + i * 4, y), (630 + i * 4, y + 28), 218, 3)
        seg(cv, (630 + i * 4, y), (586 + i * 4, y + 28), 218, 3)
    chain(cv, [(386, 722), (462, 776), (540, 806)], 7, rx=14, ry=8, g=232, w=3.4)
    pendant_cross(cv, 566, 818, 40)


@reg(BUST, "academic_robe")    # Sepúlveda: uzun cüppe, iki beyaz sarkık bant (rabat), omuzda kapüşon kıvrımı
def _b_academic(cv, d):
    body(cv, NECK["mid"], 70)
    folds(cv, [(300, 880), (410, 840), (520, 890)], [(280, 1040), (390, 1040), (520, 1040)], seed=91)
    ln(cv, [(250, 880), (320, 800), (400, 790), (470, 830)], 150, 40)
    ln(cv, [(250, 860), (320, 780), (400, 770), (470, 810)], 110, 2)
    ln(cv, [(344, 676), (430, 696), (520, 724), (596, 764)], 160, 22)
    for k in range(2):
        pts = [(572 + k * 30, 748 + k * 8), (604 + k * 30, 760 + k * 8), (616 + k * 30, 880), (586 + k * 30, 876)]
        fillq(cv, pts, 214)
        cv.stroke(poly(pts), 108, 2)
        seg(cv, (592 + k * 30, 770 + k * 8), (598 + k * 30, 870), 150, 1.6)
    ln(cv, [(344, 660), (430, 678), (520, 704), (596, 746)], 206, 6)


@reg(BUST, "fur_gown_merchant")  # Welser: V yakalı kürk astarlı cüppe + zincir + kese
def _b_merchant(cv, d):
    body(cv, NECK["mid"], 72)
    folds(cv, [(300, 900), (420, 860)], [(280, 1040), (400, 1040)], seed=92)
    fur_band(cv, [(384, 684), (444, 700), (516, 722), (596, 774), (640, 868), (664, 980)], 74, seed=93, g=174, rows=3)
    chain(cv, [(376, 706), (452, 758), (540, 790), (620, 830)], 10, rx=16, ry=9.5, g=236)
    circ(cv, 632, 846, 18, 244)
    circ(cv, 632, 846, 18, 106, stroke=2.6)
    gem(cv, 632, 846, 7, shape="cab")


# ═════════════════════════════ takılar (kulak süsleri) ═════════════════════════════
@reg(ACC, "ear_inca")          # Atahualpa: iri altın kulak diski (orejón)
def _acc_ear_inca(cv, d):
    x, y = 458, 482
    circ(cv, x, y, 33, 248)
    circ(cv, x, y, 33, 104, stroke=3.2)
    circ(cv, x, y, 24, 122, stroke=2.6)
    circ(cv, x, y, 15, 236)
    circ(cv, x, y, 15, 110, stroke=2.2)
    circ(cv, x, y, 6, 252)


@reg(ACC, "ear_aztec")         # Moctezuma: turkuaz-altın kulak makarası + sarkaç
def _acc_ear_aztec(cv, d):
    x, y = 458, 480
    circ(cv, x, y, 26, 246)
    circ(cv, x, y, 26, 104, stroke=3)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        seg(cv, (x + 11 * math.cos(a), y + 11 * math.sin(a)), (x + 22 * math.cos(a), y + 22 * math.sin(a)), 130, 2)
    circ(cv, x, y, 9, 252)
    ln(cv, [(x, y + 26), (x + 2, y + 52)], 220, 3.2)
    fillq(cv, [(x - 8, y + 52), (x + 10, y + 52), (x + 8, y + 78), (x - 6, y + 78)], 240)
    cv.stroke(poly([(x - 8, y + 52), (x + 10, y + 52), (x + 8, y + 78), (x - 6, y + 78)]), 108, 2)


@reg(ACC, "ear_pearl")
def _acc_ear_pearl(cv, d):
    x, y = 460, 474
    ln(cv, [(x, y), (x + 2, y + 18)], 214, 2.4)
    pearl(cv, x + 2, y + 28, 8)


# ═════════════════════════════ eski kişileri yükseltme: yeni türler ═════════════════════════════
@reg(HAIR, "tonsure")          # keşiş tonsürü: tepe açık, çevrede saç halkası
def _h_tonsure(cv, d):
    pts = [(520, 340), (452, 322), (392, 336), (354, 394), (344, 474), (358, 544), (394, 562), (432, 522), (438, 462), (448, 414), (476, 386), (520, 356)]
    mass(cv, pts, 184)
    roots = [pl([(508, 344), (446, 328), (394, 342), (360, 400)], i / 11) for i in range(12)]
    tips = [pl([(476, 388), (446, 436), (432, 504), (398, 556)], i / 11) for i in range(12)]
    flow(cv, roots, tips, 142, 2.2, bend=-6, n=8, seed=211, jit=0.3)


@reg(HAIR, "curly")            # Büyük İskender: geriye taranmış dalgalı saç + alın kıvrımları
def _h_curly(cv, d):
    pts = [(584, 268), (520, 212), (430, 202), (364, 240), (340, 324), (350, 412), (388, 448), (418, 398), (442, 352), (490, 314), (542, 292)]
    mass(cv, pts, 188)
    top = [(574, 256), (500, 214), (420, 208), (362, 246), (342, 324)]
    bot = [(470, 322), (420, 372), (386, 440), (352, 410), (342, 350)]
    strands_between(cv, top, bot, 16, 142, 2.4, bend=-18, waves=1.2, amp=8, seed=212, jit=0.3, rev=False)
    for (x, y, f) in [(572, 280, 1), (548, 298, -1), (522, 312, 1), (498, 326, -1)]:
        curl(cv, x, y, 12, 136, 2.2, 1.5, f)


@reg(HAT, "tudor_bonnet")      # Henri VIII: yassı Tudor bonesi, mücevherli kenar, uzun tüy
def _hat_tudor(cv, d):
    pts = [(298, 302), (306, 240), (372, 194), (480, 174), (586, 186), (652, 226), (680, 264), (650, 292), (582, 298), (500, 280), (420, 292), (338, 316)]
    path = P(pts, True, 0.45)
    cv.fill(path, 214)
    with clip(cv, path):
        ov(cv, 490, 214, 170, 38, 234, blur=18)
    cv.stroke(path, 108, 2.6)
    rim = [(330, 308), (430, 288), (520, 280), (602, 294), (660, 268)]
    _rim(cv, rim, 26, 236)
    for i in range(7):
        x, y = pl(rim, 0.06 + 0.88 * i / 6)
        if i % 2 == 0:
            gem(cv, x, y, 8, shape="cab" if i % 4 == 0 else "dia")
        else:
            pearl(cv, x, y, 5.6)
    plume(cv, [(404, 200), (480, 156), (570, 160), (640, 200), (676, 262)], 50, g=238)
    plume(cv, [(420, 204), (500, 176), (580, 190), (626, 232)], 30, g=232)


@reg(HAT, "barett_plain")      # Luther / Melanchthon: sade, yumuşak, siyah Barett
def _hat_barett(cv, d):
    pts = [(304, 302), (310, 238), (370, 192), (470, 172), (570, 182), (638, 216), (664, 258), (634, 286), (574, 294), (500, 276), (424, 288), (344, 312)]
    path = P(pts, True, 0.45)
    cv.fill(path, 212)
    with clip(cv, path):
        ov(cv, 484, 212, 150, 36, 230, blur=18)
    ln(cv, [(376, 214), (446, 198), (520, 202)], 154, 2.4)
    ln(cv, [(420, 240), (500, 224), (588, 232)], 154, 2.2)
    cv.stroke(path, 108, 2.6)
    _rim(cv, [(334, 306), (430, 286), (520, 278), (600, 292), (652, 266)], 18, 228)


@reg(HAT, "turban_x")          # Süleyman: iri, sarmal bantlı sarık + mücevherli sorguç
def _hat_turban(cv, d):
    pts = [(336, 396), (320, 320), (318, 246), (338, 182), (404, 132), (486, 112), (568, 132), (622, 184), (644, 250), (624, 306), (560, 302), (500, 332), (430, 372), (380, 408)]
    path = P(pts, True, 0.4)
    cv.fill(path, 212)
    with clip(cv, path):
        ov(cv, 480, 200, 150, 90, 232, blur=26)
        for k in range(9):
            y = 140 + k * 20
            ln(cv, [(290, y + 70), (470, y - 18), (676, y + 56)], 146, 3.4, 0.5)
            ln(cv, [(290, y + 82), (470, y - 6), (676, y + 68)], 190, 1.6, 0.5)
    cv.stroke(path, 108, 2.8)
    _rim(cv, [(330, 300), (430, 294), (540, 290), (626, 302)], 26, 234)
    bx, by = 594, 214
    circ(cv, bx, by, 24, 246)
    circ(cv, bx, by, 24, 108, stroke=3)
    for k in range(6):
        a = k / 6 * 2 * math.pi
        pearl(cv, bx + 17 * math.cos(a), by + 17 * math.sin(a), 4.2)
    gem(cv, bx, by, 8, shape="dia")
    plume(cv, [(594, 196), (590, 156), (598, 124), (612, 100)], 34, g=238)


@reg(HAT, "turban_small_x")    # Barbaros: kırmızı kavuk + dolanmış sarık + sarkan uç
def _hat_turban_s(cv, d):
    cap = [(354, 394), (354, 206), (392, 146), (468, 124), (548, 144), (592, 206), (596, 278), (540, 290), (450, 290), (400, 372)]
    fillp(cv, cap, 206, 0.35)
    ov(cv, 470, 190, 80, 60, 228, blur=20)
    wrap = [(342, 386), (344, 300), (348, 252), (398, 222), (500, 214), (592, 238), (616, 292), (560, 312), (470, 322), (404, 376)]
    path = P(wrap, True, 0.4)
    cv.fill(path, 224)
    with clip(cv, path):
        for k in range(-4, 14):
            seg(cv, (320 + k * 26, 330), (320 + k * 26 + 96, 196), 148, 3.0)
            seg(cv, (326 + k * 26, 330), (326 + k * 26 + 96, 196), 190, 1.4)
    cv.stroke(path, 108, 2.6)
    ln(cv, [(350, 296), (440, 284), (540, 284), (610, 292)], 238, 6)
    ribbon(cv, [(352, 290), (326, 360), (316, 440)], 26, 14, 220, n=10, seam=2.0, seamg=140)
    gem(cv, 566, 262, 9, shape="dia")


@reg(HAT, "gold_haube")        # Fugger: altın ağlı yuvarlak Haube
def _hat_haube(cv, d):
    base = [(344, 324), (352, 238), (420, 184), (512, 176), (586, 222), (606, 286), (540, 278), (450, 286), (380, 334)]
    path = P(base, True, 0.4)
    cv.fill(path, 214)
    with clip(cv, path):
        ov(cv, 490, 226, 110, 40, 232, blur=16)
        for k in range(-6, 14):
            seg(cv, (300 + k * 26, 130), (300 + k * 26 + 190, 340), 156, 1.8)
            seg(cv, (300 + k * 26 + 190, 130), (300 + k * 26, 340), 156, 1.8)
        for r in range(8):
            for k in range(-2, 14):
                circ(cv, 300 + k * 26 + (13 if r % 2 else 0), 150 + r * 26, 3.4, 242)
    cv.stroke(path, 108, 2.6)
    _rim(cv, [(374, 322), (452, 296), (532, 288), (598, 296)], 16, 234)
    circ(cv, 500, 180, 9, 242)


@reg(HAT, "camauro_x")         # Klemens: kulakları örten kırmızı kadife camauro + ermin kenar
def _hat_camauro(cv, d):
    pts = [(584, 274), (562, 214), (482, 176), (392, 190), (346, 258), (338, 340), (342, 430), (378, 482), (420, 442), (436, 362), (480, 314), (542, 290)]
    mass(cv, pts, 212, 0.4)
    ov(cv, 440, 240, 90, 50, 232, blur=20, rot=-20)
    ln(cv, [(420, 190), (388, 260), (372, 380)], 156, 2.4)
    fur_band(cv, [(592, 270), (546, 298), (490, 350), (452, 430), (434, 506)], 34, seed=213, g=206, rows=2, L=(12, 20))
    for (x, y) in [(560, 290), (520, 322), (486, 366), (460, 420), (446, 478)]:
        ov(cv, x, y, 3.4, 7, 70)


@reg(HAT, "mourning_veil")     # Juana: sade siyah peçe + beyaz keten alın bandı
def _hat_mveil(cv, d):
    veil = [(592, 264), (544, 212), (450, 186), (366, 222), (326, 318), (306, 460), (296, 600), (284, 730), (300, 820), (380, 836),
            (420, 744), (436, 650), (446, 590), (458, 500), (480, 420), (506, 350), (540, 300), (568, 276)]
    fillp(cv, veil, 200, 0.42)
    cv.stroke(P(veil, True, 0.42), 108, 2.4)
    ov(cv, 440, 300, 90, 70, 218, blur=22)
    top = [(556, 226), (470, 194), (390, 214), (340, 280)]
    bot = [(452, 650), (420, 742), (372, 812), (318, 786)]
    strands_between(cv, top, bot, 11, 140, 2.8, bend=-16, waves=0.8, amp=8, seed=221, jit=0.5, rev=False)
    front = [(594, 266), (568, 278), (540, 302), (506, 352), (480, 422), (458, 502), (446, 592), (438, 652)]
    ln(cv, front, 228, 14)
    ln(cv, [(x - 8, y + 2) for x, y in front], 130, 1.6)
    ln(cv, [(596, 268), (544, 222), (462, 200)], 150, 3)


@reg(HAT, "jeweled_net")       # Portekizli İsabel: ortadan ayrık saç, mücevherli ağ, elmaslı alın bandı
def _hat_jnet(cv, d):
    hair = [(588, 268), (520, 220), (430, 204), (362, 240), (336, 330), (326, 450), (322, 560), (340, 640), (384, 640), (410, 580), (436, 500),
            (462, 430), (500, 372), (548, 318)]
    mass(cv, hair, 188)
    strands_between(cv, [(576, 258), (500, 218), (420, 208), (360, 244), (334, 330)], [(470, 560), (430, 620), (380, 646), (344, 630), (330, 560)],
                    15, 144, 2.4, bend=-24, waves=1.0, amp=9, seed=215, jit=0.3, rev=False)
    net = [(528, 238), (440, 206), (366, 250), (342, 346), (350, 470), (420, 430), (456, 340), (500, 292)]
    path = P(net, True, 0.4)
    cv.fill(path, 208)
    with clip(cv, path):
        for k in range(-6, 14):
            seg(cv, (300 + k * 24, 180), (300 + k * 24 + 160, 520), 242, 2.2)
            seg(cv, (300 + k * 24 + 160, 180), (300 + k * 24, 520), 242, 2.2)
        for r in range(9):
            for k in range(-2, 12):
                circ(cv, 300 + k * 24 + (12 if r % 2 else 0) + 80, 190 + r * 34, 3.8, 246)
    cv.stroke(path, 108, 2.4)
    dia = [(594, 270), (544, 232), (468, 212), (398, 234)]
    ln(cv, dia, 236, 12)
    beads_on(cv, dia, 9, r=5)
    gem(cv, 566, 246, 11, shape="dia")


@reg(HAT, "broad_hat")         # Maksimilyan: geniş kenarlı, tepeli şapka + kürk kenar + rozet
def _hat_broad(cv, d):
    brim = [(248, 280), (296, 244), (420, 228), (540, 228), (656, 244), (708, 280), (660, 304), (540, 312), (410, 312), (296, 304)]
    fillp(cv, brim, 214, 0.3)
    ov(cv, 480, 262, 210, 22, 232, blur=14)
    cv.stroke(P(brim, True, 0.3), 108, 2.4)
    with clip(cv, P(brim, True, 0.3)):
        rs = rs_of("broad")
        for _ in range(120):
            x, y = rs.uniform(250, 706), rs.uniform(232, 312)
            seg(cv, (x, y), (x + rs.uniform(-3, 3), y + rs.uniform(6, 11)), 156, 1.7)
    crown = [(380, 256), (392, 190), (466, 160), (556, 176), (596, 232), (574, 262), (486, 254), (408, 264)]
    fillp(cv, crown, 224, 0.35)
    cv.stroke(P(crown, True, 0.35), 108, 2.4)
    ln(cv, [(388, 250), (476, 238), (564, 244), (592, 252)], 238, 12)
    ln(cv, [(420, 196), (480, 176), (546, 186)], 160, 2.2)
    circ(cv, 566, 228, 15, 244)
    circ(cv, 566, 228, 15, 108, stroke=2.4)
    gem(cv, 566, 228, 7, shape="dia")


@reg(HAT, "morion_x")          # Pizarro: tepelikli morion + kayık siperlik + perçinler
def _hat_morion(cv, d):
    dome = [(344, 304), (352, 228), (412, 180), (492, 166), (570, 186), (612, 238), (616, 292), (540, 282), (450, 288), (380, 310)]
    fillp(cv, dome, 216, 0.4)
    comb = [(378, 224), (420, 150), (490, 116), (562, 126), (606, 172), (614, 238), (562, 198), (490, 178), (420, 198)]
    fillp(cv, comb, 228, 0.35)
    cv.stroke(P(comb, True, 0.35), 108, 2.6)
    ln(cv, [(402, 214), (446, 168), (500, 148), (556, 156), (590, 190)], 150, 2.6)
    brim = [(318, 232), (350, 296), (450, 312), (540, 308), (640, 296), (684, 224), (650, 276), (540, 282), (440, 286), (360, 272)]
    fillp(cv, brim, 222, 0.3)
    cv.stroke(P(brim, True, 0.3), 108, 2.4)
    for k in range(9):
        circ(cv, 372 + k * 30, 296 - (k % 2), 5.2, 244)
    ln(cv, [(352, 288), (450, 282), (560, 282), (628, 290)], 150, 2.2)


@reg(HAT, "knit_cap")          # Elkano: kıvrık kenarlı yumuşak denizci takkesi, arkaya düşen uç
def _hat_knit(cv, d):
    crown = [(358, 270), (348, 202), (366, 150), (418, 118), (478, 124), (530, 160), (566, 214), (604, 268), (540, 262), (450, 262)]
    path = P(crown, True, 0.4)
    cv.fill(path, 212)
    with clip(cv, path):
        ov(cv, 450, 190, 90, 70, 230, blur=20)
        for k in range(10):
            ln(cv, [(350 + k * 26, 276), (352 + k * 22, 210), (380 + k * 18, 140)], 154, 2.0, 0.5)
    cv.stroke(path, 108, 2.4)
    band_poly(cv, [(346, 268), (430, 252), (520, 248), (600, 262)], [(612, 304), (530, 296), (440, 298), (358, 312)], 228, groove=108)
    for k in range(9):
        seg(cv, (368 + k * 28, 262 + (k % 2) * 3), (372 + k * 28, 304), 150, 1.8)
    circ(cv, 424, 118, 13, 242)
    circ(cv, 424, 118, 13, 108, stroke=2.2)


@reg(HAT, "diadem")            # Büyük İskender: sade kraliyet bandı (diadem) + arkadan inen iki şerit
def _hat_diadem(cv, d):
    pts = [(592, 268), (544, 236), (452, 222), (380, 246), (350, 300)]
    ln(cv, pts, 236, 14)
    ln(cv, [(x, y - 7) for x, y in pts], 130, 1.6)
    ln(cv, [(x, y + 7) for x, y in pts], 130, 1.6)
    ribbon(cv, [(352, 288), (326, 360), (338, 440)], 22, 12, 226, n=10, seam=1.8, seamg=140)
    ribbon(cv, [(360, 296), (350, 372), (372, 450)], 20, 12, 220, n=10, seam=1.8, seamg=140)
    gem(cv, 560, 244, 7, shape="dia")


@reg(BEARD, "long_pointed_x")  # Barbaros: uzun, dolgun, ucu sivrilen sakal
def _be_longpointed(cv, d):
    ch = d["chin"]
    top = [(452, 418), (500, 446), (548, 480), (590, 508)]
    bot = [(606, 540), (626, 574), (638 + ch, 620), (632 + ch * .6, 700), (614, 780), (586, 852), (556, 790), (520, 730), (480, 694),
           (440, 650), (410, 596), (398, 520), (414, 456)]
    beard_shape(cv, top, bot, 172, n=26, bend=12, waves=1.2, amp=9, seed=233, jit=0.35, nn=14)


# — giysiler —
@reg(BUST, "monk_habit")       # Luther (siyah) / Las Casas (beyaz): kukuleta + iç yaka çizgisi + skapüler
def _b_monk(cv, d):
    white = d.get("habit") == "white"
    body(cv, [(350, 668), (430, 668), (520, 680), (600, 702)], 150 if white else 72)
    folds(cv, [(300, 900), (420, 860), (540, 900)], [(280, 1040), (400, 1040), (540, 1040)], seed=231, g=(104 if white else 50))
    cow = [(300, 726), (352, 664), (440, 648), (520, 672), (606, 722), (650, 808), (620, 872), (520, 842), (420, 800), (340, 790)]
    path = P(cow, True, 0.4)
    cv.fill(path, 170 if white else 120)
    with clip(cv, path):
        ov(cv, 470, 770, 150, 60, (190 if white else 150), blur=24)
        for k in range(8):
            ln(cv, [(300 + k * 40, 700), (320 + k * 40, 790), (330 + k * 40, 880)], (130 if white else 80), 2.6)
    cv.stroke(path, 100, 2.6)
    ln(cv, [(372, 664), (446, 674), (520, 696), (604, 738)], 222, 8)
    for x in (560, 612):
        ln(cv, [(x, 860), (x + 10, 1040)], (118 if white else 60), 3)
    ln(cv, [(500, 884), (540, 900), (600, 892)], (130 if white else 70), 2.6)


@reg(BUST, "kaftan_x")         # Süleyman / Barbaros: ayakta yaka, çintemani desenli kaftan, kürklü omuz
def _b_kaftan(cv, d):
    body(cv, NECK["high"], 76)
    path = P([(110, 1070), (140, 970), (196, 868), (262, 792), (316, 744), (352, 640), (430, 628), (520, 646), (592, 676), (690, 742), (770, 812),
              (860, 900), (920, 1070)], True, 0.4)
    with clip(cv, path):
        for r in range(8):
            for k in range(-3, 12):
                x = 150 + k * 52 + (26 if r % 2 else 0)
                y = 742 + r * 46
                circ(cv, x, y, 5.0, 216)
                circ(cv, x - 8, y + 9, 4.2, 216)
                circ(cv, x + 8, y + 9, 4.2, 216)
        for r in range(6):
            ln(cv, [(150, 760 + r * 52), (300, 740 + r * 52), (450, 774 + r * 52), (600, 744 + r * 52), (760, 776 + r * 52)], 112, 2.0)
    fur_band(cv, [(222, 906), (284, 826), (336, 774)], 40, seed=235, g=172)
    band_poly(cv, [(352, 600), (430, 596), (520, 616), (592, 646)], [(612, 716), (520, 694), (430, 678), (342, 690)], 168)
    ln(cv, [(356, 604), (430, 598), (520, 618), (590, 648)], 214, 5)
    ln(cv, [(344, 668), (430, 658), (520, 676), (606, 702)], 112, 2.2)
    seg(cv, (606, 720), (650, 1040), 52, 3)
    for i in range(5):
        circ(cv, 612 + i * 8, 762 + i * 50, 8, 226)
        circ(cv, 612 + i * 8, 762 + i * 50, 8, 104, stroke=2)
    ln(cv, [(300, 840), (400, 860), (500, 900)], 120, 2.4)


@reg(BUST, "ruff_black_x")     # II. Felipe: siyah giysi, değirmen taşı yaka, Altın Post zinciri
def _b_ruff(cv, d):
    body(cv, NECK["high"], 68)
    folds(cv, [(300, 900), (420, 860)], [(280, 1040), (400, 1040)], seed=236)
    for i in range(5):
        circ(cv, 604 + i * 6, 790 + i * 46, 7, 208)
    chain(cv, [(340, 760), (430, 812), (528, 842), (624, 872)], 11, rx=17, ry=10, g=238)
    gem(cv, 636, 884, 11, shape="dia")
    sp = [(376, 662), (450, 678), (524, 696), (594, 722), (628, 756)]
    a = cr(sp, 14)
    q, tg = along(a, 17)
    for row in (0, 1):
        for i, (x, y) in enumerate(q):
            ang = math.degrees(math.atan2(tg[i][1], tg[i][0])) + 90
            ov(cv, float(x), float(y) + row * 22, 17, 30, 214 + row * 6, rot=ang)
            ov(cv, float(x), float(y) + row * 22, 17, 30, 118, rot=ang, stroke=2.0)


@reg(BUST, "cassock_x")        # Klemens: mozzetta (omuz pelerini), ermin yaka, düğme sırası, göğüs haçı
def _b_cassock(cv, d):
    body(cv, NECK["mid"], 70)
    moz = [(250, 820), (318, 760), (400, 722), (520, 738), (610, 772), (662, 852), (644, 944), (520, 984), (400, 962), (300, 922)]
    path = P(moz, True, 0.4)
    cv.fill(path, 150)
    with clip(cv, path):
        ov(cv, 470, 850, 170, 80, 176, blur=26)
        for k in range(8):
            ln(cv, [(260 + k * 48, 770), (270 + k * 48, 860), (276 + k * 48, 960)], 106, 2.4)
    cv.stroke(path, 100, 2.6)
    fur_band(cv, [(384, 692), (450, 706), (522, 724), (600, 758)], 42, seed=237, g=206, rows=2, L=(10, 18))
    for i in range(8):
        circ(cv, 598 + i * 6, 792 + i * 24, 7, 226)
        circ(cv, 598 + i * 6, 792 + i * 24, 7, 104, stroke=2)
    chain(cv, [(430, 762), (500, 820), (556, 846)], 6, rx=11, ry=7, g=226, w=3.4)


@reg(BUST, "armor_x")          # Pizarro / Moritz / İskender: gorget, omuz plakası, göğüs sırtı, perçinler
def _b_armor(cv, d):
    greek = d.get("gv") == "greek"
    body(cv, NECK["mid"], 82)
    pa = skia.Path()
    pa.addOval(skia.Rect.MakeLTRB(206, 770, 420, 900))
    cv.fill(pa, 196)
    for k in range(3):
        ln(cv, [(226 + k * 6, 806 + k * 28), (310, 790 + k * 28), (402, 812 + k * 28)], 112, 2.4)
    cv.stroke(pa, 106, 2.6)
    band_poly(cv, [(352, 650), (430, 646), (520, 664), (596, 690)], [(612, 744), (520, 722), (430, 710), (344, 718)], 198)
    for k in range(3):
        ln(cv, [(350, 664 + k * 18), (430, 660 + k * 17), (520, 678 + k * 16), (600, 702 + k * 15)], 112, 2.2)
    if greek:
        for dx in (-1, 1):
            ln(cv, [(520 + dx * 64, 770), (520 + dx * 84, 850), (520 + dx * 46, 920)], 120, 3.0)
        ln(cv, [(420, 800), (520, 820), (620, 800)], 120, 2.4)
        cl = [(250, 830), (330, 780), (420, 800), (440, 900), (360, 980), (270, 960)]
        fillp(cv, cl, 168, 0.4)
        cv.stroke(P(cl, True, 0.4), 106, 2.4)
        for k in range(5):
            ln(cv, [(280 + k * 24, 830 + k * 10), (310 + k * 20, 900), (320 + k * 14, 970)], 120, 2.2)
        gem(cv, 440, 800, 12, shape="cab")
    else:
        ln(cv, [(596, 748), (640, 880), (660, 1040)], 224, 12)
        ln(cv, [(596, 748), (640, 880), (660, 1040)], 112, 1.6)
        for i in range(8):
            circ(cv, 574 + i * 9, 790 + i * 34, 5.4, 246)
        ln(cv, [(330, 900), (440, 880), (560, 900)], 118, 2.4)
        ln(cv, [(300, 960), (440, 940), (580, 970)], 118, 2.4)

# ═════════════════════════════ takma adlar ═════════════════════════════
HAT["copilli"] = HAT["xiuhhuitzolli"]
HAT["gable_hood_x"] = HAT["gable_hood"]
BUST["tunik_inca"] = BUST["tunic_inca"]
HAT["hood_dark"] = HAT["widow_wimple"]


# ═════════════════════════════ kişiler ═════════════════════════════
def person(key, inscr, **kw):
    base = dict(nose=12, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=1.0, fore=0, age=0.3, jowl=0.0, neck=1.0,
                hair="none", hat="none", beard=None, garment="plain", mouth_open=0.0, _x=True, scale=1.1, dy=-20)
    base.update(kw)
    PEOPLE[key] = base
    INSCR[key] = inscr


# — Habsburg / Burgonya / İberya —
person("filip", "PHILIPPVS · PVLCHER · DVX · BVRGVNDIAE ·", nose=14, hook=0, brow=2, lip=4, lip2=9, chin=15, jaw=0.95, fore=1, age=0.0,
       neck=1.05, hair="wavy", hat="burg_bonnet", garment="fur_jacket", eye="wide", brow_style="arch", ear=False, cheek=0.6,
       scale=0.98, dy=-12)
person("fernando", "FERNANDVS · ARAGONVM · REX · CATHOLICVS ·", nose=22, hook=4, brow=6, lip=0, lip2=0, chin=6, jaw=1.15, fore=0, age=0.6,
       jowl=0.1, neck=1.0, hair="bowl", hat="barrete", garment="dark_doublet", eye="narrow", brow_style="stern", mouth="stern",
       ear=False, scale=1.14, dy=-20)
person("maria_burgonya", "MARIA · DVCISSA · BVRGVNDIAE ·", nose=8, hook=-3, brow=1, lip=3, lip2=5, chin=4, jaw=0.82, fore=3, age=0.0,
       neck=0.8, nback=384, hat="hennin", garment="jeweled_gown", eye="almond", lash=True, brow_style="arch", ear=False, scale=1.0, dy=-4)
person("isabel_kastilya", "ELISABET · REGINA · CASTELLAE · LEGIONIS ·", nose=10, hook=0, brow=3, lip=1, lip2=3, chin=11, jaw=0.9, fore=2,
       age=0.5, jowl=0.1, neck=0.9, nback=378, hat="castilian_veil", garment="dark_gown_collar", eye="std", brow_style="arch", lash=True,
       mouth="stern", ear=False, scale=1.12, dy=-20)
person("sarlman", "KAROLVS · MAGNVS · IMPERATOR · AVGVSTVS ·", nose=20, hook=4, brow=7, lip=2, lip2=3, chin=12, jaw=1.15, fore=0, age=0.5,
       jowl=0.1, neck=1.2, hair="long_flow", hat="imperial_crown", beard="long_flow", must="droop", garment="mantle_brooch",
       eye="heavy", brow_style="heavy", ear=False, scale=0.93, dy=0)
person("karl_cocuk", "CAROLVS · ARCHIDVX · AVSTRIAE · BVRGVND ·", nose=2, hook=-6, brow=0, lip=4, lip2=6, chin=8, jaw=0.7, fore=4, age=0.0,
       neck=0.72, nback=394, hair="child", hat="child_cap", garment="child_doublet", eye="wide", iris=9.5, brow_style="raised", ear=False,
       cheek=0.9, puff=0.5, ck=0.84, scale=1.04, dy=-4)
PEOPLE["karl_cocuk"].update(chin=6, jaw=0.62)
# — Komünero —
person("padilla", "IOANNES · DE · PADILLA · TOLETANVS ·", nose=12, hook=0, brow=6, lip=2, lip2=3, chin=8, jaw=1.2, fore=0, age=0.25,
       neck=1.1, hair="crop", hat="toque_brim", beard="trim", must="short", garment="leather_jerkin", eye="std", brow_style="heavy",
       scale=1.1, dy=-14)
person("bravo", "IOANNES · BRAVO · SEGOBIENSIS · MDXXI ·", nose=18, hook=5, brow=4, lip=0, lip2=2, chin=2, jaw=0.95, fore=1, age=0.3,
       neck=1.05, hair="crop", hat="feather_beret", beard="goatee", must="handle", garment="cloak_buttons", eye="wide", brow_style="std",
       scale=1.1, dy=-16)
person("maldonado", "FRANCISCVS · MALDONADO · SALMANTICENSIS ·", nose=9, hook=-1, brow=3, lip=2, lip2=3, chin=0, jaw=1.0, fore=0, age=0.45,
       jowl=0.15, neck=1.15, hat="plain_coif", beard="full_round", must="short", garment="lawyer_robe", eye="heavy", brow_style="bushy",
       scale=1.1, dy=-18)
person("maria_pacheco", "MARIA · PACHECO · TOLETI · DEFENSATRIX ·", nose=10, hook=-1, brow=2, lip=3, lip2=5, chin=8, jaw=0.85, fore=2, age=0.25,
       neck=0.85, nback=380, hat="toca", garment="dark_gown_plain", eye="narrow", lash=True, brow_style="arch", mouth="stern", ear=False,
       cheek=0.5, scale=1.1, dy=-16)
# — Reform / Saksonya —
person("frederik_bilge", "FRIDERICVS · SAPIENS · DVX · SAXONIAE ·", nose=18, hook=3, brow=4, lip=1, lip2=2, chin=2, jaw=1.3, fore=0, age=0.5,
       jowl=0.5, neck=1.4, puff=0.6, hair="thin_back", hat="beret_wide", beard="broad", must="short", garment="fur_gown_wide",
       eye="heavy", brow_style="std", scale=1.04, dy=-14, furw=112)
person("johann_friedrich", "IOHANNES · FRIDERICVS · ELECTOR · SAXONIAE ·", nose=5, hook=-4, brow=2, lip=0, lip2=1, chin=-6, jaw=1.6, fore=3,
       age=0.4, jowl=0.9, neck=1.5, puff=1.0, hair="crop", hat="beret_feathers", beard="cropped", must="pencil", garment="fur_gown_wide",
       garm="saxony", slash=True, furw=100, eye="narrow", brow_style="std", scale=0.94, dy=-6)
# — Hanımlar —
person("louise_savoy", "LVDOVICA · SABAVDIAE · REGENS · FRANCIAE ·", nose=18, hook=6, brow=3, lip=1, lip2=2, chin=0, jaw=0.95, fore=2, age=0.5,
       jowl=0.2, neck=0.88, nback=374, hat="french_hood", garment="gown_fur", eye="heavy", brow_style="arch", lash=True, mouth="stern", ear=False,
       scale=1.1, dy=-18)
person("catherine_aragon", "CATHARINA · ARAGONIA · ANGLIAE · REGINA ·", nose=8, hook=-2, brow=2, lip=4, lip2=6, chin=10, jaw=0.85, fore=3,
       age=0.3, jowl=0.15, neck=0.9, nback=376, puff=0.5, hat="gable_hood", garment="jeweled_gown", gv="tudor", eye="std", lash=True,
       brow_style="arch", ear=False, cheek=0.3, scale=1.08, dy=-10)
person("mary_macar", "MARIA · HVNGARIAE · ET · BOHEMIAE · REGINA ·", nose=12, hook=2, brow=3, lip=3, lip2=11, chin=20, jaw=0.95, fore=2,
       age=0.35, neck=0.9, nback=376, hat="widow_wimple", garment="black_dress", eye="std", lash=True, brow_style="stern", mouth="stern", ear=False,
       scale=1.1, dy=-18)
# — Macaristan —
person("lajos2", "LVDOVICVS · II · HVNGARIAE · REX ·", nose=6, hook=-3, brow=1, lip=3, lip2=8, chin=5, jaw=0.8, fore=2, age=0.0, neck=0.9,
       hair="wavy", hat="royal_cap_crown", garment="courtly_jacket", eye="wide", brow_style="arch", ear=False, cheek=0.3, scale=1.0, dy=-8)
person("zapolya", "IOANNES · DE · ZAPOLYA · HVNGARIAE · REX ·", nose=20, hook=2, brow=6, lip=1, lip2=2, chin=7, jaw=1.15, fore=0, age=0.35,
       neck=1.1, hair="sides", hat="kalpak", must="long", garment="dolama", eye="heavy", brow_style="heavy", scale=1.0, dy=-4)
# — Akdeniz / Yeni Dünya / Bilginler —
person("doria", "ANDREAS · DORIA · PATER · PATRIAE ·", nose=22, hook=5, brow=6, lip=1, lip2=1, chin=-4, jaw=1.0, fore=-2, age=0.9,
       jowl=0.25, neck=1.0, hair="sides", hat="kalot", beard="white_long", must="long", garment="dark_robe", eye="heavy", brow_style="bushy",
       scale=1.1, dy=-14)
person("atahualpa", "ATAWALLPA · SAPA · INKA · TAWANTINSUYU ·", nose=11, hook=-1, brow=2, lip=3, lip2=5, chin=2, jaw=1.0, fore=-2, age=0.12,
       neck=1.05, hair="inca", hat="mascapaicha", garment="tunic_inca", acc=["ear_inca"], eye="almond", brow_style="std", cheek=1.0,
       scale=0.96, dy=-2)
person("moctezuma", "MOTEUCZOMA · XOCOYOTZIN · HUEY · TLATOANI ·", nose=16, hook=4, brow=5, lip=4, lip2=6, chin=8, jaw=1.2, fore=0, age=0.45,
       jowl=0.15, neck=1.1, hair="inca", hat="xiuhhuitzolli", garment="tilmatli", acc=["ear_aztec"], eye="heavy", brow_style="std",
       cheek=0.4, scale=0.96, dy=-2)
person("magellan", "FERDINANDVS · MAGELLANVS · LVSITANVS ·", nose=14, hook=2, brow=5, lip=1, lip2=2, chin=10, jaw=1.15, fore=0, age=0.35,
       neck=1.1, hair="crop", hat="seaman_cap", beard="ship", must="short", garment="explorer_doublet", eye="narrow", brow_style="heavy",
       scale=1.1, dy=-16)
person("sepulveda", "IOANNES · GENESIVS · SEPVLVEDA ·", nose=13, hook=1, brow=4, lip=1, lip2=2, chin=-2, jaw=0.85, fore=0, age=0.75,
       jowl=0.1, neck=0.95, hair="sides", hat="biretta", beard="chinstrap", must="pencil", garment="academic_robe", eye="narrow",
       brow_style="stern", mouth="stern", scale=1.08, dy=-10)
person("welser", "BARTHOLOMAEVS · WELSER · AVGVSTANVS ·", nose=11, hook=-2, brow=3, lip=3, lip2=3, chin=5, jaw=1.0, fore=1, age=0.4,
       jowl=0.2, neck=1.1, hair="crop", hat="merchant_cap", beard="trim", garment="fur_gown_merchant", eye="std", brow_style="raised",
       scale=1.06, dy=-8)

# — Karl ve Fransuva için İSTEĞE BAĞLI zengin varyantlar (eski anahtarlar değişmez; *_x anahtarı seçilirse giysili büst gelir) —
person("karl_genc_x", medal.INSCR["karl_genc"], nose=10, hook=6, brow=4, lip=3, lip2=10, chin=26, jaw=1.0, fore=0, age=0.0, neck=1.0,
       mouth_open=0.35, hair="child", hat="flatcap_x", garment="fur_jacket", eye="heavy", brow_style="arch", ear=False,
       scale=1.02, dy=-10)
person("karl_olgun_x", medal.INSCR["karl_olgun"], nose=12, hook=8, brow=5, lip=3, lip2=11, chin=30, jaw=1.05, fore=0, age=0.45, jowl=0.1,
       neck=1.05, mouth_open=0.3, hair="crop", hat="barrete", beard="trim", garment="dark_doublet", eye="heavy", brow_style="std",
       scale=1.08, dy=-14)
person("karl_yasli_x", medal.INSCR["karl_yasli"], nose=13, hook=9, brow=5, lip=2, lip2=12, chin=32, jaw=1.0, fore=-2, age=0.9, jowl=0.35,
       neck=0.95, mouth_open=0.4, hair="sides", hat="kalot", beard="full_round", blen=0, garment="black_dress", eye="heavy",
       brow_style="stern", mouth="stern", scale=1.08, dy=-14)
person("fransuva_x", medal.INSCR["fransuva"], nose=34, hook=-6, brow=4, lip=4, lip2=5, chin=2, jaw=1.05, fore=2, age=0.2, jowl=0.1,
       neck=1.0, hair="wavy", hat="beret_feathers", beard="goatee", must="handle", garment="fur_jacket", eye="wide", brow_style="std",
       ear=False, scale=0.94, dy=-6)

NEW_KEYS = ["filip", "fernando", "maria_burgonya", "isabel_kastilya", "sarlman", "karl_cocuk", "padilla", "bravo", "maldonado",
            "maria_pacheco", "frederik_bilge", "johann_friedrich", "louise_savoy", "catherine_aragon", "mary_macar", "lajos2", "zapolya",
            "doria", "atahualpa", "moctezuma", "magellan", "sepulveda", "welser"]
VARIANT_KEYS = ["karl_genc_x", "karl_olgun_x", "karl_yasli_x", "fransuva_x"]    # isteğe bağlı zengin (giysili büst) varyantlar

# ═════════════════════════════ ESKİ 26 KİŞİNİN YÜKSELTİLMESİ ═════════════════════════════
# Eski sürümler *_old anahtarıyla saklanır (aynı yüz parametreleri, eski çizim hattı); asıl anahtarlar _x hattına geçer. INSCR aynı kalır.
OLD_KEYS = ["karl_genc", "karl_olgun", "karl_yasli", "fransuva", "henri8", "luther", "melanchthon", "suleyman", "barbaros", "fugger",
            "klemens", "felipe2", "juana", "isabel", "ferdinand", "maksimilyan", "kortes", "pizarro", "lascasas", "moritz", "orange",
            "margareta", "tiziano", "durer", "elkano", "makedonya"]
for _k in OLD_KEYS:
    if _k in PEOPLE and not PEOPLE[_k].get("_x"):
        PEOPLE[_k + "_old"] = dict(PEOPLE[_k])
        INSCR[_k + "_old"] = INSCR.get(_k)
for _k in ("karl_genc", "karl_olgun", "karl_yasli", "fransuva"):
    PEOPLE[_k] = PEOPLE[_k + "_x"]                       # INSCR değişmez


def upg(key, **kw):
    person(key, INSCR.get(key), **kw)


upg("henri8", nose=2, hook=0, brow=2, lip=-4, lip2=-2, chin=-4, jaw=1.5, fore=4, age=0.3, jowl=0.6, neck=1.5, puff=1.0, hair="crop",
    hat="tudor_bonnet", beard="cropped", must="pencil", garment="courtly_jacket", eye="narrow", brow_style="std", ear=False,
    scale=0.94, dy=-6)
upg("luther", nose=8, hook=2, brow=3, lip=2, lip2=4, chin=0, jaw=1.4, fore=3, age=0.35, jowl=0.7, neck=1.4, puff=0.7, hair="sides",
    hat="barett_plain", garment="monk_habit", eye="wide", brow_style="heavy", scale=1.04, dy=-12)
upg("melanchthon", nose=8, hook=3, brow=3, lip=1, lip2=2, chin=-2, jaw=0.9, fore=3, age=0.4, jowl=0.1, neck=0.9, nback=368, hair="thin_back",
    hat="barett_plain", beard="trim", garment="academic_robe", eye="narrow", brow_style="raised", ear=False, scale=1.04, dy=-12)
upg("suleyman", nose=18, hook=-8, brow=4, lip=2, lip2=2, chin=-2, jaw=0.95, fore=0, age=0.2, neck=1.0, hat="turban_x", beard="goatee",
    blen=6, must="long", garment="kaftan_x", eye="almond", brow_style="arch", scale=0.96, dy=-4)
upg("barbaros", nose=16, hook=-4, brow=5, lip=3, lip2=3, chin=4, jaw=1.1, fore=0, age=0.5, jowl=0.1, neck=1.1, hat="turban_small_x",
    beard="long_pointed_x", must="long", garment="kaftan_x", eye="narrow", brow_style="heavy", scale=1.02, dy=-8)
upg("fugger", nose=16, hook=4, brow=3, lip=1, lip2=2, chin=2, jaw=0.9, fore=2, age=0.5, jowl=0.1, neck=0.95, hair="wavy", hat="gold_haube",
    garment="fur_gown_merchant", eye="narrow", brow_style="std", ear=False, scale=1.06, dy=-10)
upg("klemens", nose=14, hook=5, brow=4, lip=2, lip2=3, chin=0, jaw=1.0, fore=2, age=0.6, jowl=0.2, neck=1.0, hat="camauro_x", beard="full_round",
    blen=30, must="short", garment="cassock_x", eye="heavy", brow_style="std", ear=False, scale=1.08, dy=-14)
upg("felipe2", nose=10, hook=5, brow=3, lip=3, lip2=9, chin=22, jaw=0.95, fore=2, age=0.1, neck=1.0, mouth_open=0.25, hair="crop", hat="barrete",
    nobadge=True, plumed=True, beard="goatee", blen=40, must="short", garment="ruff_black_x", eye="wide", brow_style="std", scale=1.06, dy=-10)
upg("juana", nose=10, hook=2, brow=2, lip=2, lip2=6, chin=14, jaw=0.9, fore=2, age=0.4, neck=0.9, nback=378, hat="mourning_veil",
    garment="black_dress", eye="std", lash=True, brow_style="arch", ear=False, scale=1.1, dy=-18)
upg("isabel", nose=8, hook=0, brow=1, lip=2, lip2=4, chin=8, jaw=0.8, fore=3, age=0.0, neck=0.85, nback=380, hat="jeweled_net",
    garment="jeweled_gown", gv="tudor", eye="almond", lash=True, brow_style="arch", ear=False, scale=1.08, dy=-12)
upg("ferdinand", nose=12, hook=5, brow=4, lip=2, lip2=8, chin=18, jaw=1.0, fore=0, age=0.2, jowl=0.05, neck=1.0, mouth_open=0.2, hair="wavy",
    hat="flatcap_x", garment="dark_doublet", eye="std", brow_style="std", ear=False, scale=1.02, dy=-10)
upg("maksimilyan", nose=28, hook=10, brow=5, lip=2, lip2=5, chin=12, jaw=0.95, fore=0, age=0.55, jowl=0.1, neck=1.0, hair="thin_back",
    hat="broad_hat", garment="fur_gown_wide", furw=96, eye="heavy", brow_style="std", scale=0.92, dy=-4)
upg("kortes", nose=10, hook=2, brow=4, lip=2, lip2=3, chin=4, jaw=1.1, fore=0, age=0.3, jowl=0.05, neck=1.1, hair="crop", hat="feather_beret",
    beard="full_round", blen=10, must="short", garment="explorer_doublet", eye="narrow", brow_style="heavy", scale=1.08, dy=-14)
upg("pizarro", nose=12, hook=4, brow=6, lip=1, lip2=2, chin=2, jaw=1.15, fore=-2, age=0.6, jowl=0.1, neck=1.15, hair="sides", hat="morion_x",
    beard="full_round", blen=50, must="short", garment="armor_x", eye="narrow", brow_style="stern", scale=0.98, dy=-8)
upg("lascasas", nose=9, hook=3, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=3, age=0.7, jowl=0.05, neck=0.9, hair="tonsure", beard="short_gray",
    garment="monk_habit", habit="white", eye="std", brow_style="arch", scale=1.1, dy=-16)
upg("moritz", nose=14, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=1.0, fore=0, age=0.1, neck=1.0, hair="wavy", hat="beret_wide", plumed=True,
    nobadge=True, beard="trim", garment="armor_x", eye="almond", brow_style="std", ear=False, scale=0.96, dy=-8)
upg("orange", nose=12, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=0.9, fore=2, age=0.0, neck=0.95, hair="crop", hat="barrete", plumed=True,
    beard="trim", garment="cloak_buttons", eye="std", brow_style="raised", scale=1.04, dy=-10)
upg("margareta", nose=10, hook=2, brow=2, lip=2, lip2=7, chin=14, jaw=0.9, fore=2, age=0.35, neck=0.9, nback=376, hat="widow_wimple", peak=True,
    garment="black_dress", eye="std", lash=True, brow_style="stern", mouth="stern", ear=False, scale=1.1, dy=-18)
upg("tiziano", nose=12, hook=2, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=2, age=0.7, jowl=0.05, neck=0.9, hat="plain_coif",
    beard="full_round", blen=40, must="short", garment="dark_robe", eye="heavy", brow_style="bushy", scale=1.1, dy=-14)
upg("durer", nose=12, hook=2, brow=3, lip=1, lip2=2, chin=0, jaw=0.9, fore=2, age=0.3, neck=0.95, hair="wavy", beard="trim",
    garment="fur_gown_wide", furw=96, nochain=True, eye="wide", brow_style="arch", ear=False, scale=1.08, dy=-12)
upg("elkano", nose=12, hook=2, brow=4, lip=2, lip2=3, chin=2, jaw=1.1, fore=0, age=0.3, jowl=0.05, neck=1.1, hair="crop", hat="knit_cap",
    beard="trim", garment="leather_jerkin", eye="narrow", brow_style="heavy", scale=1.06, dy=-14)
upg("makedonya", nose=10, hook=0, brow=3, lip=2, lip2=3, chin=0, jaw=1.0, fore=2, age=0.2, neck=1.0, hair="curly", hat="diadem",
    garment="armor_x", gv="greek", eye="wide", brow_style="arch", cheek=0.4, scale=1.08, dy=-12)

UPGRADED = OLD_KEYS[:]

try:
    medal.medal_array.cache_clear()
except Exception:
    pass
