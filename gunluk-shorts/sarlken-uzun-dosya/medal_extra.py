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


def fillp(cv, pts, g, t=0.45, blur=0.0):
    cv.fill(P(pts, True, t), g, blur)


def fillq(cv, pts, g, blur=0.0):
    cv.fill(poly(pts), g, blur)


def ln(cv, pts, g, w, t=0.5, blur=0.0):
    cv.stroke(P(pts, False, t), g, w, blur)


def seg(cv, p, q, g, w):
    cv.stroke(poly([p, q], False), g, w)


def ov(cv, x, y, rx, ry, g, blur=0.0, rot=0.0, stroke=0.0):
    c = cv.c
    c.save()
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


def flow(cv, roots, tips, g, w, bend=0.0, waves=0.0, amp=0.0, n=12, t=0.5, seed=1, jit=0.0):
    """Köklerden uçlara akan saç/sakal telleri (düzgün eğriler)."""
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


def plume(cv, pts, w, g=234, seed=2, barbs=12, shaft=5.0):
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
                      g - 48, 2.1)
            if rs.rand() < 0.55:
                cv.stroke(poly([(float(q[0] + 4), float(q[1])), (float(q2[0] + 4), float(q2[1] - 2))], False), g + 26, 1.6)
    # kenar boncukları (kürk ucu)
    edge = a + nr * (width * 0.5)
    for i in range(0, len(edge), 2):
        circ(cv, float(edge[i][0]), float(edge[i][1]), 5.5, g + (tipg if tipg is not None else 10))


def fur_fill(cv, path, g, seed=5, n=240, L=(14, 26), ang=math.pi / 2, sd=0.5, gd=46):
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
def _skin_x(cv, d):
    outline = medal.head_paths(d)
    p = P(outline, True, 0.45)
    cv.fill(p, 120)
    skull = skia.Path()
    skull.addOval(skia.Rect.MakeLTRB(344, 168, 598, 560))
    cv.fill(skull, 120)
    nk = d["neck"]
    neck = P([(430, 560), (560 - (nk - 1) * 14, 628), (578 + (nk - 1) * 26, 700), (606 + (nk - 1) * 30, 770), (560, 830),
              (420, 830), (356, 760), (352, 620)], True, 0.35)
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
    # ── burun
    ln(cv, [(626 + n * 0.5, 480), (616, 486), (606, 484)], 70, 5)
    ln(cv, [(604, 440 + hk), (592, 470), (600, 488)], 100, 3)
    # ── ağız
    md = d.get("mouth", "std")
    cy0, cy1 = {"std": (529, 526), "stern": (535, 527), "smile": (523, 527)}[md]
    ln(cv, [(560, cy0 + 1), (580, 526 + (cy0 - cy1) * 0.2), (602 + lip * 0.5, cy1 + mo * 6)], 56, 6)
    ln(cv, [(578, 556), (600 + lip2 * 0.3, 556)], 98, 3)
    if lip + lip2 > 9:      # dolgun dudak kenarı
        ln(cv, [(612 + lip, 513), (598, 521), (582, 525)], 96, 2.2)
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
    pts = [(586, 262), (520, 210), (430, 192), (356, 232), (318, 330), (304, 460), (296, 590), (300, 720), (330, 800), (386, 790),
           (414, 700), (430, 600), (448, 520), (470, 452), (506, 382), (552, 314)]
    mass(cv, pts, 186)
    top = [(574, 252), (500, 208), (420, 198), (356, 238), (320, 330)]
    bot = [(468, 700), (420, 760), (372, 800), (322, 790), (296, 720)]
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
    pts = [(594, 304), (582, 262), (520, 220), (430, 200), (360, 234), (330, 330), (320, 450), (324, 560), (350, 612), (410, 614),
           (440, 560), (458, 486), (480, 420), (512, 360), (540, 322), (570, 310)]
    mass(cv, pts, 186)
    roots = [pl([(584, 256), (500, 212), (420, 202), (360, 238), (332, 330)], i / 15) for i in range(16)]
    tips = [pl([(592, 304), (540, 318), (478, 430), (456, 540), (410, 612), (344, 590)], i / 15) for i in range(16)]
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
            mass_texture(cv, pts, seed, short, (9, 15), math.radians(75), 0.55, sg, sw - 0.2, t=t,
                         dirfn=lambda x, y: math.radians(58 + max(0, min(60, (y - 480) * 0.28))) if x > 470 else math.radians(95))
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
    top = [(448, 418), (498, 446), (548, 480), (588, 508)]
    bot = [(606, 540), (624, 572), (636 + ch, 618), (632 + ch * .6, 700), (608, 790), (576, 852), (544, 900), (508, 858), (472, 782),
           (440, 692), (410, 606), (396, 520), (412, 456)]
    beard_shape(cv, top, bot, 172, n=26, bend=12, waves=1.2, amp=10, seed=66, jit=0.35, nn=14)


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
    _skin_x(cv, d)
    BUST.get(d.get("garment"), BUST["plain"])(cv, d)
    for tb, kk in ((HAIR, "hair"),):
        f = tb.get(d.get(kk))
        if f:
            f(cv, d)
    f = BEARD.get(d.get("beard"))
    if f:
        f(cv, d)
    _features_x(cv, d)
    _must(cv, d)
    f = HAT.get(d.get("hat"))
    if f:
        f(cv, d)
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
    plume(cv, [(618, 232), (660, 198), (706, 204), (728, 244)], 24, g=232)


@reg(HAT, "barrete")          # Fernando: koyu yumuşak başlık (sade rozetli)
def _hat_barrete(cv, d):
    base = [(344, 300), (350, 236), (400, 196), (480, 178), (560, 190), (610, 226), (620, 262), (588, 282), (520, 264), (440, 270), (380, 300)]
    fillp(cv, base, 214)
    ov(cv, 484, 212, 108, 28, 230, blur=12)
    _rim(cv, [(356, 292), (440, 268), (520, 262), (598, 278)], 18, 232)
    ln(cv, [(420, 202), (472, 224), (544, 232)], 156, 2.4)
    ln(cv, [(480, 184), (522, 206), (582, 226)], 156, 2.2)
    ln(cv, [(380, 250), (410, 226), (450, 210)], 156, 2.0)
    circ(cv, 572, 262, 15, 240)                     # küçük rozet
    circ(cv, 572, 262, 15, 110, stroke=2.6)
    gem(cv, 572, 262, 7, shape="dia")


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
    fur_band(cv, [(342, 668), (420, 694), (520, 718), (612, 758), (672, 834), (716, 930)], 80, seed=5, g=176)
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
    body(cv, NECK["mid"], 78)
    sp = [(344, 676), (430, 694), (520, 716), (604, 746)]
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
    bx, by = 616, 800
    circ(cv, bx, by, 38, 232)
    circ(cv, bx, by, 38, 110, stroke=3)
    circ(cv, bx, by, 28, 120, stroke=2)
    for k in range(8):
        a = k / 8 * 2 * math.pi
        gem(cv, bx + 31 * math.cos(a), by + 31 * math.sin(a), 5.2, shape="cab")
    gem(cv, bx, by, 14, shape="cab")


# ═════════════════════════════ kişiler ═════════════════════════════
def person(key, inscr, **kw):
    base = dict(nose=12, hook=2, brow=3, lip=2, lip2=3, chin=2, jaw=1.0, fore=0, age=0.3, jowl=0.0, neck=1.0,
                hair="none", hat="none", beard=None, garment="plain", mouth_open=0.0, _x=True, scale=1.1, dy=-20)
    base.update(kw)
    PEOPLE[key] = base
    INSCR[key] = inscr


person("filip", "PHILIPPVS · PVLCHER · DVX · BVRGVNDIAE ·", nose=15, hook=1, brow=2, lip=4, lip2=9, chin=15, jaw=1.0, fore=1, age=0.0,
       neck=1.05, hair="wavy", hat="burg_bonnet", garment="fur_jacket", eye="wide", brow_style="arch", ear=False, cheek=0.6,
       scale=1.06, dy=-14)
person("fernando", "FERNANDVS · ARAGONVM · REX · CATHOLICVS ·", nose=19, hook=3, brow=6, lip=1, lip2=1, chin=8, jaw=1.1, fore=0, age=0.55,
       jowl=0.1, neck=1.0, hair="bowl", hat="barrete", garment="dark_doublet", eye="narrow", brow_style="stern", mouth="stern",
       ear=False, scale=1.14, dy=-20)
person("isabel_kastilya", "ELISABET · REGINA · CASTELLAE · LEGIONIS ·", nose=9, hook=1, brow=3, lip=1, lip2=3, chin=8, jaw=0.9, fore=2,
       age=0.5, jowl=0.1, neck=0.9, hat="castilian_veil", garment="dark_gown_collar", eye="std", brow_style="arch", lash=True,
       mouth="stern", ear=False, scale=1.12, dy=-20)
person("sarlman", "KAROLVS · MAGNVS · IMPERATOR · AVGVSTVS ·", nose=17, hook=3, brow=6, lip=2, lip2=3, chin=8, jaw=1.15, fore=0, age=0.5,
       jowl=0.1, neck=1.2, hair="long_flow", hat="imperial_crown", beard="long_flow", must="droop", garment="mantle_brooch",
       eye="heavy", brow_style="heavy", ear=False, scale=1.0, dy=-10)

try:
    medal.medal_array.cache_clear()
except Exception:
    pass
