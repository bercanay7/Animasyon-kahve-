"""cilt_wall — Medici cildi: kireç sıva (intonaco) duvar üreteci.

Duvar = (W+2·MG)×(H+2·MG) tek bir RGB görüntü; kameranın itme/kayma payı için kenarlarda MG px fazlalık.
Bileşenler: ton bulutları, giornata (günlük sıva yaması) dikişleri + yama tonları, craquelure (Voronoi mikro çatlak + dallanan
uzun çatlaklar), su lekeleri (kenarı koyu halkalı), çukur/kırık (lacuna), mala izleri, orta ölçekli kabartma gölgelendirme.
İnce tane (tooth) ayrı bir ekran-uzayı çarpan haritadır (`tooth_u8`): her kareye `post()` içinde bir kez çarpılır.

Gün modu: tek görüntü ("lit"). Gece modu: "dark" (lacivert-siyah) + "lit" (mum ışığında sıcak sıva); sahnede radyal maske ile karıştırılır.
Üretim ≈ 1–2 sn; PNG olarak `out/_cache/cilt/` altına önbelleğe alınır (WALL_VER artarsa yeniden üretilir).
"""
import math
import os

import cv2
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "_cache", "cilt")
W, H = 1920, 1080
MG = 100
WW, WH = W + 2 * MG, H + 2 * MG
WALL_VER = 3

# ───────────────────────────── paletler ─────────────────────────────
# (mod, perde) → duvar renkleri. Perde I: defter bejı; II: kireç beyazı (fresk renkleri öne çıksın); III: derin kırmızı-altın (barok).
WALLS = {
    ("day", 1): dict(base=(214, 202, 174), stain=(148, 118, 68), crack=(78, 58, 36), tone=0.034),
    ("day", 2): dict(base=(214, 209, 194), stain=(150, 124, 78), crack=(74, 56, 38), tone=0.030),
    ("day", 3): dict(base=(198, 160, 122), stain=(128, 84, 54), crack=(70, 40, 28), tone=0.034),
    ("night", 1): dict(dark=(15, 21, 36), lit=(186, 150, 104), stain=(96, 70, 44), crack=(30, 20, 14), tone=0.045),
    ("night", 2): dict(dark=(11, 17, 44), lit=(184, 148, 100), stain=(92, 66, 42), crack=(26, 18, 14), tone=0.045),
    ("night", 3): dict(dark=(28, 10, 13), lit=(158, 100, 68), stain=(88, 50, 34), crack=(34, 14, 12), tone=0.045),
}


# ───────────────────────────── gürültü ─────────────────────────────
def lf(rs, h, w, scale):
    """Düşük frekanslı birim-std gürültü (öz-boyut ≈ scale px)."""
    k = max(1, int(scale / 7))
    hh, ww = h // k + 3, w // k + 3
    n = rs.standard_normal((hh, ww)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), max(0.6, scale / 2.4 / k))
    n = (n - n.mean()) / (n.std() + 1e-6)
    if k > 1:
        n = cv2.resize(n, (ww * k, hh * k), interpolation=cv2.INTER_CUBIC)
    return n[:h, :w]


def gn(rs, h, w, sigma):
    n = rs.standard_normal((h, w)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), sigma)
    return n / (n.std() + 1e-6)


def sstep(a, b, x):
    t = np.clip((x - a) / (b - a + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


# ───────────────────────────── giornata ─────────────────────────────
def _wobble_line(rs, n, amp, step_s=0.35):
    """Yavaş sapan rastgele yürüyüş (n nokta), ±amp."""
    v = np.zeros(n, np.float32)
    x = 0.0
    for i in range(n):
        x += rs.normal(0, step_s)
        x *= 0.97
        v[i] = x
    v = np.clip(v, -amp, amp)
    return v


def giornate_polys(seed, w, h, band=(190, 330), cell=(380, 760)):
    """Giornata yamaları. Dönüş: (polys: [np.array(N,2)], seams: [np.array(N,2)]).
    Yatay pontate bantları + her bant içinde dikey bölmeler; kenarlar hafif dalgalı/eğik (elle sıvanmış)."""
    rs = np.random.RandomState(seed)
    ys = [0.0]
    while ys[-1] < h:
        ys.append(ys[-1] + rs.uniform(*band))
    ys[-1] = float(h)
    if ys[-1] - ys[-2] < 90 and len(ys) > 2:      # çok ince son bandı bir öncekine kat
        ys.pop(-2)
    step = 10
    nx = w // step + 2
    # her yatay sınır: y(x) = y0 + tilt·x + dalga
    hb = []
    for i, y0 in enumerate(ys):
        if i == 0 or i == len(ys) - 1:
            hb.append(np.full(nx, y0, np.float32))
        else:
            tilt = rs.normal(0, 0.012)
            hb.append(y0 + tilt * (np.arange(nx) * step - w / 2) + _wobble_line(rs, nx, 7.0))
    polys, seams = [], []
    for bi in range(len(ys) - 1):
        top, bot = hb[bi], hb[bi + 1]
        xs = [0.0]
        while xs[-1] < w:
            xs.append(xs[-1] + rs.uniform(*cell))
        xs[-1] = float(w)
        if xs[-1] - xs[-2] < 150 and len(xs) > 2:
            xs.pop(-2)
        for xi in range(len(xs) - 1):
            x0, x1 = xs[xi], xs[xi + 1]
            i0, i1 = int(x0 // step), int(math.ceil(x1 / step))
            tpts = [(k * step if k * step > x0 else x0, float(top[k])) for k in range(i0, i1 + 1) if k * step <= x1 + step]
            bpts = [(k * step if k * step > x0 else x0, float(bot[k])) for k in range(i0, i1 + 1) if k * step <= x1 + step]
            tpts = [(min(max(x, x0), x1), y) for x, y in tpts]
            bpts = [(min(max(x, x0), x1), y) for x, y in bpts]
            # dikey kenarlar (dalgalı)
            def vline(x, ya, yb):
                m = max(2, int(abs(yb - ya) // 12))
                wv = _wobble_line(rs, m, 5.0)
                return [(x + float(wv[k]), ya + (yb - ya) * k / (m - 1)) for k in range(m)]
            left = vline(x0, tpts[0][1], bpts[0][1])
            right = vline(x1, tpts[-1][1], bpts[-1][1])
            poly = tpts + right[1:] + bpts[::-1] + left[::-1][1:]
            polys.append(np.array(poly, np.float32))
            if xi < len(xs) - 2:
                seams.append(np.array(right, np.float32))
        if bi > 0:
            seams.append(np.array([(k * step, float(top[k])) for k in range(nx)], np.float32))
    # alan çarpıtma: kenarlar düzensiz (elle sıvanmış yamalar) — aynı alan hem çokgenlere hem dikişlere uygulanır
    amp = 15.0
    gh, gw = h // 8 + 2, w // 8 + 2
    fx = lf(rs, gh, gw, 150 / 8) * amp
    fy = lf(rs, gh, gw, 150 / 8) * amp

    def warp(P):
        gx = np.clip(P[:, 0] / 8.0, 0, gw - 1.001)
        gy = np.clip(P[:, 1] / 8.0, 0, gh - 1.001)
        ix, iy = gx.astype(int), gy.astype(int)
        ax, ay = gx - ix, gy - iy
        def samp(F):
            return (F[iy, ix] * (1 - ax) * (1 - ay) + F[iy, ix + 1] * ax * (1 - ay) + F[iy + 1, ix] * (1 - ax) * ay + F[iy + 1, ix + 1] * ax * ay)
        return np.stack([P[:, 0] + samp(fx), P[:, 1] + samp(fy)], 1).astype(np.float32)
    polys = [warp(p) for p in polys]
    seams = [warp(p) for p in seams]
    return polys, seams


# ───────────────────────────── çatlaklar ─────────────────────────────
def micro_craquelure(rs, h, w, ncell=520, warp=6.0):
    """Voronoi sınırlarından ince çatlak ağı (yarı çözünürlükte hesaplanır). 0..1 (1 = çatlak çizgisi)."""
    hh, ww = h // 2, w // 2
    seeds = rs.rand(ncell, 2) * np.array([ww, hh])
    tree = cKDTree(seeds)
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    dx = lf(rs, hh, ww, 64) * warp * 0.5
    dy = lf(rs, hh, ww, 64) * warp * 0.5
    pts = np.stack([xx + dx, yy + dy], -1).reshape(-1, 2)
    d, _ = tree.query(pts, k=2)
    gap = (d[:, 1] - d[:, 0]).reshape(hh, ww).astype(np.float32)
    line = np.clip(1.0 - gap / 1.15, 0, 1)
    region = sstep(0.75, 1.35, lf(rs, hh, ww, 240))          # çatlak yalnız bazı bölgelerde
    flow = sstep(-0.9, 0.5, lf(rs, hh, ww, 26))               # çizgiler kesintili
    line = line * region * flow
    return cv2.resize(line, (w, h), interpolation=cv2.INTER_LINEAR)


def long_cracks(rs, h, w, n=9, starts=None):
    """Dallanan uzun saç teli çatlaklar → float 0..1."""
    m = np.zeros((h, w), np.uint8)

    def walk(x, y, ang, length, depth, g0):
        step = rs.uniform(5.0, 8.0)
        turn = 0.0
        ang0 = ang
        pts = [(x, y)]
        for s in range(int(length / step)):
            turn = turn * 0.80 + rs.normal(0, 0.075)
            ang += turn
            ang = ang0 + max(-0.95, min(0.95, ang - ang0))
            x += math.cos(ang) * step
            y += math.sin(ang) * step
            pts.append((x, y))
            if depth < 2 and rs.rand() < 0.022:
                walk(x, y, ang + rs.choice([-1, 1]) * rs.uniform(0.6, 1.2), length * rs.uniform(0.25, 0.5), depth + 1, g0 * 0.8)
            if not (-50 < x < w + 50 and -50 < y < h + 50):
                break
        npt = len(pts)
        for i in range(npt - 1):
            g = int(g0 * (1.0 - 0.75 * i / max(1, npt - 1)))
            cv2.line(m, (int(pts[i][0]), int(pts[i][1])), (int(pts[i + 1][0]), int(pts[i + 1][1])), g, 1, cv2.LINE_AA)

    for k in range(n):
        if starts is not None and len(starts) and rs.rand() < 0.65:
            x, y = starts[rs.randint(len(starts))]
        else:
            # kenarlardan başlayan çatlaklar (köşe/tavan etkisi)
            e = rs.randint(4)
            x, y = [(rs.uniform(0, w), 0), (w, rs.uniform(0, h)), (rs.uniform(0, w), h), (0, rs.uniform(0, h))][e]
        ang = rs.uniform(0, 2 * math.pi)
        walk(x, y, ang, rs.uniform(260, 820), 0, rs.uniform(190, 255))
    return cv2.GaussianBlur(m.astype(np.float32) / 255.0, (0, 0), 0.55)


# ───────────────────────────── lekeler ─────────────────────────────
def stains(rs, h, w, n_big=3, n_small=2):
    """Su lekeleri (iç ton, gelgit izi): tavandan süzülen sızıntılar, köşe nemi, alt kenarda yükselen nem. İnce ve yumuşak."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    warpn = lf(rs, h, w, 110)
    warpn2 = lf(rs, h, w, 40)
    inner = np.zeros((h, w), np.float32)
    for i in range(n_big):
        px = rs.uniform(0.0, 1.0) * w
        py = rs.uniform(-0.04, 0.05) * h
        r = rs.uniform(120, 230)
        ry = r * rs.uniform(1.3, 2.4)                  # aşağı sarkan uzamış leke
        d = np.sqrt(((xx - px) / r) ** 2 + ((yy - py) / ry) ** 2)
        d = d * (1.0 + 0.40 * warpn + 0.12 * warpn2)
        inner = np.maximum(inner, sstep(1.0, 0.6, d) * rs.uniform(0.5, 0.9))
    for i in range(n_small):
        px, py = rs.uniform(0, w), rs.uniform(0.1, 0.95) * h
        r = rs.uniform(40, 110)
        d = np.sqrt(((xx - px) / r) ** 2 + ((yy - py) / (r * rs.uniform(0.7, 1.2))) ** 2)
        d = d * (1.0 + 0.35 * warpn + 0.12 * warpn2)
        inner = np.maximum(inner, sstep(1.0, 0.55, d) * rs.uniform(0.25, 0.5))
    # yükselen nem: alt kenarda dalgalı yatay bant
    damp_y = h * (0.935 + 0.012 * warpn) + 8 * warpn2
    inner = np.maximum(inner, sstep(0.0, 70.0, yy - damp_y) * 0.55)
    inner = cv2.GaussianBlur(inner, (0, 0), 16.0)
    gxx = cv2.Sobel(inner, cv2.CV_32F, 1, 0, ksize=3)
    gyy = cv2.Sobel(inner, cv2.CV_32F, 0, 1, ksize=3)
    rim = np.sqrt(gxx * gxx + gyy * gyy)
    rim = np.clip(rim / (rim.max() + 1e-6) * 1.6, 0, 1)
    return inner * 0.40, rim * 0.45


def pits(rs, h, w, n=80):
    """Küçük çukurlar: (koyu iç, açık alt-sağ kenar)."""
    dark = np.zeros((h, w), np.uint8)
    for i in range(n):
        x, y = int(rs.uniform(0, w)), int(rs.uniform(0, h))
        r = rs.choice([1, 1, 1, 1, 2])
        cv2.circle(dark, (x, y), int(r), int(rs.uniform(110, 255)), -1, cv2.LINE_AA)
    dk = dark.astype(np.float32) / 255.0
    hi = np.roll(np.roll(dk, 1, 0), 1, 1)
    hi = np.clip(hi - dk, 0, 1)
    return dk, hi


def chips(rs, h, w, n=3):
    """Plaster kaybı: kenarlara yakın küçük düzensiz kırıklar → (maske, kenar gölgesi)."""
    m = np.zeros((h, w), np.uint8)
    for i in range(n):
        e = rs.randint(4)
        cx, cy = [(rs.uniform(0.05, 0.95) * w, rs.uniform(0.02, 0.10) * h), (rs.uniform(0.90, 0.99) * w, rs.uniform(0.1, 0.9) * h),
                  (rs.uniform(0.05, 0.95) * w, rs.uniform(0.90, 0.99) * h), (rs.uniform(0.01, 0.08) * w, rs.uniform(0.1, 0.9) * h)][e]
        r = rs.uniform(18, 52)
        k = 10
        pts = []
        for j in range(k):
            a = 2 * math.pi * j / k
            rr = r * rs.uniform(0.55, 1.15)
            pts.append((int(cx + math.cos(a) * rr * 1.4), int(cy + math.sin(a) * rr)))
        cv2.fillPoly(m, [np.array(pts, np.int32)], 255, cv2.LINE_AA)
    mf = m.astype(np.float32) / 255.0
    edge = np.clip(cv2.GaussianBlur(mf, (0, 0), 2.0) - mf * 0.6, 0, 1)
    return mf, edge


# ───────────────────────────── yapı (renkten bağımsız) ─────────────────────────────
def structure(seed, w=WW, h=WH):
    rs = np.random.RandomState(seed)
    S = {}
    S["lf"] = lf(rs, h, w, 380)
    S["mf"] = lf(rs, h, w, 120)
    S["hf"] = lf(rs, h, w, 38)
    S["warm"] = lf(rs, h, w, 300)
    # mala izleri (yönlü yumuşak kavisler)
    tn = rs.standard_normal((h // 3, w // 3)).astype(np.float32)
    ang = rs.uniform(-0.35, 0.35)
    tn = cv2.GaussianBlur(tn, (0, 0), sigmaX=34 / 3, sigmaY=5 / 3)
    tn = cv2.resize((tn - tn.mean()) / (tn.std() + 1e-6), (w, h), interpolation=cv2.INTER_CUBIC)
    mrot = cv2.getRotationMatrix2D((w / 2, h / 2), math.degrees(ang), 1.0)
    S["trowel"] = cv2.warpAffine(tn, mrot, (w, h), borderMode=cv2.BORDER_REFLECT)
    # orta ölçek kabartma yüksekliği
    hgt = 0.30 * gn(rs, h, w, 3.0) + 0.55 * gn(rs, h, w, 7.5) + 0.70 * lf(rs, h, w, 24)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3)
    sh = 0.55 * gx + 0.65 * gy
    S["relief"] = sh / (np.abs(sh).std() + 1e-6)
    h2 = 0.35 * lf(rs, h, w, 22) + 0.9 * lf(rs, h, w, 52) + 0.9 * lf(rs, h, w, 110)
    sh2 = 0.55 * cv2.Sobel(h2, cv2.CV_32F, 1, 0, ksize=3) + 0.65 * cv2.Sobel(h2, cv2.CV_32F, 0, 1, ksize=3)
    S["relief2"] = sh2 / (np.abs(sh2).std() + 1e-6)
    # giornata
    polys, seams = giornate_polys(seed * 7 + 1, w, h)
    lab = np.zeros((h, w), np.uint16)
    for i, p in enumerate(polys):
        cv2.fillPoly(lab, [p.astype(np.int32)], i + 1)
    nb = len(polys) + 1
    bvals = np.clip(rs.normal(0, 0.012, nb), -0.026, 0.026).astype(np.float32)
    wvals = np.clip(rs.normal(0, 0.011, nb), -0.022, 0.022).astype(np.float32)
    gvals = rs.uniform(0.8, 1.25, nb).astype(np.float32)
    S["gi_b"] = cv2.GaussianBlur(bvals[lab], (0, 0), 0.8)
    S["gi_w"] = cv2.GaussianBlur(wvals[lab], (0, 0), 0.8)
    S["gi_g"] = gvals[lab]
    sm = np.zeros((h, w), np.uint8)
    for s in seams:
        cv2.polylines(sm, [s.astype(np.int32).reshape(-1, 1, 2)], False, 255, 1, cv2.LINE_AA)
    sm = cv2.GaussianBlur(sm.astype(np.float32) / 255.0, (0, 0), 0.6)
    vary = sstep(-1.2, 0.2, lf(rs, h, w, 90)) * 0.8 + 0.2           # dikiş boyunca görünürlük değişir
    sm = sm * vary
    S["seam"] = sm
    S["seam_hi"] = np.clip(np.roll(np.roll(sm, 2, 0), 2, 1) - sm * 0.9, 0, 1)
    # çatlaklar
    starts = []
    for s in seams:
        for q in s[::6]:
            starts.append((float(q[0]), float(q[1])))
    S["crack_m"] = micro_craquelure(rs, h, w)
    S["crack_l"] = long_cracks(rs, h, w, n=11, starts=starts)
    S["stain_in"], S["stain_rim"] = stains(rs, h, w)
    S["pit_dk"], S["pit_hi"] = pits(rs, h, w)
    S["chip"], S["chip_edge"] = chips(rs, h, w)
    # kenar yaşlanması
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ex = np.minimum(xx, w - 1 - xx) / 110.0
    ey = np.minimum(yy, h - 1 - yy) / 100.0
    S["edge"] = sstep(1.0, 0.0, np.minimum(ex, ey)) ** 1.5 * 0.9
    return S


def _tint(col, rgb, a):
    """col (h,w,3) float, rgb sabit renk, a (h,w) → karıştır."""
    return col * (1 - a[..., None]) + np.array(rgb, np.float32) * a[..., None]


def colorize(S, pal, kind="day", raking=1.0):
    """kind: 'day' | 'dark' | 'lit'. Dönüş uint8 RGB (h,w,3)."""
    base = np.array(pal["base"] if kind == "day" else pal["dark"] if kind == "dark" else pal["lit"], np.float32)
    h, w = S["lf"].shape
    tone = pal["tone"]
    t = tone * S["lf"] + 0.6 * tone * S["mf"] + 0.30 * tone * S["hf"] + 0.014 * S["trowel"]
    col = np.empty((h, w, 3), np.float32)
    col[:] = base
    col *= (1 + t + S["gi_b"])[..., None]
    wsh = 0.020 * S["warm"] + S["gi_w"]
    col[..., 0] *= 1 + wsh
    col[..., 2] *= 1 - wsh * 1.5
    # orta kabartma
    k_rel = {"day": 0.004, "dark": 0.010, "lit": 0.007 * raking}[kind]
    col *= (1 + k_rel * S["relief"] * S["gi_g"])[..., None]
    k_rel2 = {"day": 0.010, "dark": 0.012, "lit": 0.015 * raking}[kind]
    col *= (1 + k_rel2 * S["relief2"])[..., None]
    # su lekeleri
    st = np.array(pal["stain"], np.float32)
    if kind == "dark":
        st = st * 0.30
    elif kind == "lit":
        st = st * 0.95
    col = _tint(col, st, np.clip(S["stain_in"] * (0.30 if kind != "dark" else 0.35), 0, 0.5))
    col *= (1 - 0.07 * S["stain_rim"])[..., None] if kind != "dark" else (1 - 0.10 * S["stain_rim"])[..., None]
    # çukur / kırık
    ck = np.array(pal["crack"], np.float32)
    col = _tint(col, base * 0.74 if kind != "dark" else ck, np.clip(S["chip"] * (0.16 if kind != "dark" else 0.25), 0, 1))
    col *= (1 - 0.12 * S["chip_edge"])[..., None]
    col *= (1 - 0.40 * S["pit_dk"])[..., None]
    col *= (1 + 0.28 * S["pit_hi"])[..., None]
    # giornata dikişi
    seam_k = {"day": 0.20, "dark": 0.10, "lit": 0.24 * raking}[kind]
    col *= (1 - seam_k * S["seam"])[..., None]
    col *= (1 + seam_k * 0.55 * S["seam_hi"])[..., None]
    # çatlaklar
    cm = np.clip(S["crack_m"] * 0.45 + S["crack_l"] * 1.0, 0, 1)
    ck_k = {"day": 0.50, "dark": 0.30, "lit": 0.62}[kind]
    col = _tint(col, ck, np.clip(cm * ck_k, 0, 0.85))
    chi = np.clip(np.roll(np.roll(cm, 1, 0), 1, 1) - cm, 0, 1)
    col *= (1 + (0.16 if kind != "dark" else 0.10) * chi)[..., None]
    # kenar yaşlanması
    if kind == "day":
        col = _tint(col, np.array(pal["base"], np.float32) * np.array([0.84, 0.80, 0.70], np.float32), S["edge"] * 0.30)
    elif kind == "lit":
        col *= (1 - 0.10 * S["edge"])[..., None]
    return np.clip(col, 0, 255).astype(np.uint8)


# ───────────────────────────── ince tane (ekran-uzayı çarpan) ─────────────────────────────
def tooth(seed=5, strength=1.0):
    """1920×1080 uint8 (kazanç·230): intonaco kum tanesi + gözenek. 230 ≈ 1.0, aralık ≈ 0.90–1.07.
    Model: seyrek kum taneleri (kubbe) + çok ince gaussian + birkaç iri tane + gözenekler; tek ışık sol-üst."""
    rs = np.random.RandomState(seed)
    h = 0.30 * gn(rs, H, W, 0.65)
    for dens, sg, amp in ((0.10, 0.95, 0.55), (0.035, 1.6, 0.75), (0.006, 2.6, 1.0)):
        g = (rs.rand(H, W) < dens).astype(np.float32) * rs.uniform(0.5, 1.0, (H, W)).astype(np.float32)
        h += amp * cv2.GaussianBlur(g, (0, 0), sg) * (sg * 2.2)
    h += 0.18 * gn(rs, H, W, 7.0)
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3)
    sh = 0.55 * gx + 0.65 * gy
    sh /= (np.abs(sh).std() + 1e-6)
    gain = 1.0 + 0.020 * strength * sh + 0.012 * strength * (h - h.mean()) / (h.std() + 1e-6)
    # gözenek: seyrek koyu noktalar (+ alt-sağ parlak dudak)
    sp = rs.rand(H, W)
    pores = (sp < 0.0016).astype(np.float32)
    pores = cv2.GaussianBlur(pores, (0, 0), 0.8) * 3.0
    gain *= 1.0 - 0.10 * np.clip(pores, 0, 1)
    gain *= np.where(sp > 0.9988, 1.035, 1.0)
    return np.clip(gain * 230.0, 0, 255).astype(np.uint8)


# ───────────────────────────── önbellek ─────────────────────────────
def _png_path(name):
    os.makedirs(CACHE, exist_ok=True)
    return os.path.join(CACHE, f"{name}_v{WALL_VER}.png")


def wall_arrays(mode, perde, seed):
    """(day) → {'lit': rgb}; (night) → {'dark': rgb, 'lit': rgb}. Diske önbellekli."""
    pal = WALLS[(mode, perde)]
    kinds = ["lit"] if mode == "night" else ["day"]
    out, missing = {}, []
    for k in kinds:
        p = _png_path(f"wall_{mode}{perde}_{seed}_{k}")
        if os.path.exists(p):
            out[k] = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB)
        else:
            missing.append(k)
    if missing:
        S = structure(seed * 13 + perde * 3 + (1 if mode == "night" else 0))
        for k in missing:
            arr = colorize(S, pal, k, raking=1.0)
            cv2.imwrite(_png_path(f"wall_{mode}{perde}_{seed}_{k}"), cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_PNG_COMPRESSION, 3])
            out[k] = arr
    if mode == "day":
        out["lit"] = out.pop("day")
    return out


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    S = structure(1)
    print("yapı", time.time() - t)
    t = time.time()
    a = colorize(S, WALLS[("day", 2)], "day")
    print("renk", time.time() - t)
    cv2.imwrite("out/frames/_wall_day.png", cv2.cvtColor(a[MG:MG + H, MG:MG + W], cv2.COLOR_RGB2BGR))
