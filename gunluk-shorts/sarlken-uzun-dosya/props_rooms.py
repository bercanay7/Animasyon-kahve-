"""Oda-lab dekor/eşya çizimleri (skia, pişirmede; küçük olanlar dyn'de de kullanılabilir). Işık listesi biçimi: [(x, y, R, '#renk', alfa)]."""
import math

import numpy as np
import skia

import sk
import stage as ST
import stage_rooms as R
from sk import C, H, W, mix
from stage import MARGIN

M = MARGIN
shade = R.shade


def lattice(f, rect, step=26, col="#0c0a09", sw=3.0, alpha=0.9, mullion=True, frame="#1a120b"):
    """Kurşun çıtalı baklava (elmas) cam şebekesi."""
    x0, y0, x1, y1 = rect
    f.c.save()
    f.c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    n = int((x1 - x0 + y1 - y0) / step) + 2
    for u in range(-n, n):
        f.line(x0, y0 + u * step, x1, y0 + u * step + (x1 - x0), color=col, sw=sw, alpha=alpha)
        f.line(x0, y0 + u * step + (x1 - x0), x1, y0 + u * step, color=col, sw=sw, alpha=alpha)
    f.c.restore()
    if frame:
        f.rect(x0 - 6, y0 - 7, x1 - x0 + 12, 9, color=frame)
        f.rect(x0 - 6, y1 - 2, x1 - x0 + 12, 9, color=frame)
        f.rect(x0 - 6, y0 - 7, 9, y1 - y0 + 14, color=frame)
        f.rect(x1 - 3, y0 - 7, 9, y1 - y0 + 14, color=frame)
    if mullion:
        f.line((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, color=frame, sw=8)
        f.line(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, color=frame, sw=8)


def coin_stack(f, x, y, n, r=15.0, th=5.2, seed=0, light=(-1.0, -1.0)):
    """Altın sikke sütunu (y: tabanın alt ucu). n: sikke sayısı."""
    rs = np.random.RandomState(seed)
    for i in range(n):
        jx = (rs.rand() - 0.5) * 2.2
        yc = y - i * th
        rx = r * (0.97 + 0.05 * rs.rand())
        ry = rx * 0.34
        f.oval(x + jx, yc, rx, ry, color="#6a4a14")
        f.rect(x + jx - rx, yc - th, rx * 2, th, shader=f.lin(x + jx - rx, 0, x + jx + rx, 0, [("#7a5518", 0.0), ("#d9aa3c", 0.45), ("#f1cf6a", 0.62), ("#8a6220", 1.0)]))
        f.oval(x + jx, yc - th, rx, ry, shader=f.lin(x + jx - rx, yc - th - ry, x + jx + rx, yc - th + ry, [("#f6dc84", 0.0), ("#d7a83a", 0.6), ("#a87a24", 1.0)]))
        f.oval(x + jx, yc - th, rx * 0.74, ry * 0.7, style="stroke", sw=0.8, color="#8a6220", alpha=0.7)
        f.line(x + jx - rx * 0.55, yc - th - ry * 0.55, x + jx - rx * 0.1, yc - th - ry * 0.8, color="#fff3c0", sw=1.0, alpha=0.5)


def coin_pile(f, cx, base_y, w, h, n, seed=0, r=(8.0, 12.0)):
    """Dağılmış sikke yığını (tümsek). Arkadan öne çizilir."""
    rs = np.random.RandomState(seed)
    pts = []
    for i in range(n):
        u = (rs.rand() + rs.rand() - 1.0)                 # üçgensel dağılım −1..1
        px = cx + u * w * 0.5
        mound = (1 - abs(u) ** 1.35)
        py = base_y - mound * h * (0.25 + 0.75 * rs.rand())
        pts.append((py, px, rs.rand()))
    pts.sort()
    for (py, px, q) in pts:
        rr = r[0] + (r[1] - r[0]) * q
        ang = (rs.rand() - 0.5) * 0.9
        f.c.save()
        f.c.translate(px, py)
        f.c.rotate(math.degrees(ang))
        f.oval(0, 1.6, rr, rr * 0.45, color="#5e4010")
        f.oval(0, 0, rr, rr * 0.45, shader=f.lin(-rr, -rr * 0.4, rr, rr * 0.4, [("#f5da80", 0.0), ("#d6a638", 0.55), ("#9a6c1e", 1.0)]))
        if q > 0.55:
            f.oval(-rr * 0.25, -rr * 0.16, rr * 0.28, rr * 0.1, color="#fff2bd", alpha=0.7)
        f.c.restore()


def balance(f, x, y, s=1.0, tilt=0.0, coins_l=3, coins_r=1, col="#b88a3a"):
    """Terazi (y: taban). tilt: radyan (+ = sağ kefe aşağı)."""
    dk = shade(col, -0.55)
    f.rect(x - 4 * s, y - 150 * s, 8 * s, 150 * s, shader=f.lin(x - 4 * s, 0, x + 4 * s, 0, [(dk, 0.0), (col, 0.5), (dk, 1.0)]))
    f.oval(x, y - 2 * s, 34 * s, 8 * s, color=dk)
    f.oval(x, y - 6 * s, 28 * s, 6 * s, color=shade(col, -0.25))
    f.circle(x, y - 152 * s, 8 * s, color=col)
    f.c.save()
    f.c.translate(x, y - 152 * s)
    f.c.rotate(math.degrees(tilt))
    f.line(-118 * s, 0, 118 * s, 0, color=shade(col, -0.2), sw=5 * s, cap="round")
    f.line(-118 * s, -1.5 * s, 118 * s, -1.5 * s, color=shade(col, 0.35), sw=1.4 * s, alpha=0.7)
    for sx, nc in ((-1, coins_l), (1, coins_r)):
        ex = sx * 118 * s
        # kefe: zincirler + tabak (kirişle birlikte döner ama kefe yatay kalır)
        f.c.save()
        f.c.translate(ex, 0)
        f.c.rotate(-math.degrees(tilt))
        for dxx in (-34, 34):
            f.line(0, 0, dxx * s, 70 * s, color=shade(col, -0.35), sw=1.3 * s)
        f.line(0, 0, 0, 70 * s, color=shade(col, -0.35), sw=1.1 * s)
        pan = skia.Path()
        pan.moveTo(-38 * s, 70 * s)
        pan.cubicTo(-30 * s, 88 * s, 30 * s, 88 * s, 38 * s, 70 * s)
        pan.close()
        f.path(pan, shader=f.lin(-38 * s, 70 * s, 38 * s, 88 * s, [(shade(col, 0.25), 0.0), (col, 0.5), (shade(col, -0.5), 1.0)]))
        f.oval(0, 70 * s, 38 * s, 5 * s, color=shade(col, -0.3))
        for k in range(nc):
            f.oval(-14 * s + k * 12 * s, 66 * s, 9 * s, 3.6 * s, color="#e8c05a")
        f.c.restore()
    f.c.restore()


def ledger_open(f, x, y, w=170, h=36, lights=(), lines=7, seed=1):
    """Açık büyük defter (hafif perspektif). y: alt kenar."""
    rs = np.random.RandomState(seed)
    left = sk.poly_path([(x - w / 2, y), (x - w / 2 + 8, y - h), (x, y - h + 6), (x, y)], True)
    right = sk.poly_path([(x, y), (x, y - h + 6), (x + w / 2 - 8, y - h), (x + w / 2, y)], True)
    f.poly([(x - w / 2 - 6, y + 5), (x - w / 2 + 4, y - h - 2), (x + w / 2 - 4, y - h - 2), (x + w / 2 + 6, y + 5)], color="#2a140d")
    R.lit_path(f, left, "#cdbb8c", lights + [(x - 20, y - h * 0.6, 120, "#ffd9a0", 0.35)], edge="#6a5638")
    R.lit_path(f, right, "#d3c194", lights + [(x - 20, y - h * 0.6, 120, "#ffd9a0", 0.35)], edge="#6a5638")
    for k in range(lines):
        u = (k + 1) / (lines + 1)
        yy = y - h * 0.15 - u * (h - 12)
        ln = rs.uniform(0.55, 0.92)
        f.line(x - w / 2 + 14 + (1 - u) * 2, yy, x - 7 - (1 - ln) * (w / 2 - 30), yy - 2 * (1 - u) * 0.3, color="#2a1a10", sw=1.1, alpha=0.5)
        f.line(x + 7, yy - 1, x + w / 2 - 14 - (1 - rs.uniform(0.55, 0.92)) * (w / 2 - 30), yy - 2 * (1 - u) * 0.3, color="#2a1a10", sw=1.1, alpha=0.5)
    f.line(x, y, x, y - h + 6, color="#4a3a24", sw=2)


def shelf_books(f, x0, y_bottom, w, rows=4, row_h=96, seed=1, lights=(), wood="#2a1c10"):
    """Defter/kitap rafı: raf tahtaları + renkli sırtlar."""
    rs = np.random.RandomState(seed)
    palette = ["#4a1f18", "#2b3a2a", "#3a2a18", "#53301c", "#1f2a3a", "#5a4020", "#3a1a22", "#40382a"]
    for r in range(rows):
        yb = y_bottom - r * row_h
        x = x0 + 8
        while x < x0 + w - 18:
            bw = rs.uniform(11, 26)
            bh = rs.uniform(row_h * 0.62, row_h * 0.9)
            col = palette[rs.randint(len(palette))]
            p = R.rect_path(x, yb - bh, bw, bh)
            R.lit_path(f, p, col, lights)
            f.line(x + 1.5, yb - bh + 8, x + 1.5, yb - 6, color="#d6a15a", sw=0.9, alpha=0.18)
            if rs.rand() > 0.5:
                f.rect(x, yb - bh * 0.7, bw, 2, color="#c9962b", alpha=0.45)
            x += bw + rs.uniform(0.5, 3.0)
        f.rect(x0, yb, w, 12, color=wood)
        f.rect(x0, yb, w, 2, color="#8a6a3a", alpha=0.6)
    f.rect(x0 - 8, y_bottom - rows * row_h - 6, 12, rows * row_h + 18, color=wood)
    f.rect(x0 + w - 4, y_bottom - rows * row_h - 6, 12, rows * row_h + 18, color=wood)


def chest(f, x, y, w=240, h=120, lights=(), open_k=1.0, gold=True):
    """Demir bantlı sandık (y: taban). Kapak açık, içi altın parıltılı."""
    body = R.rrect_path(x - w / 2, y - h, w, h, 6)
    R.lit_path(f, body, "#3a2414", lights, rim="#b88a52", rim_w=1.0)
    for k in (0.12, 0.5, 0.88):
        f.rect(x - w / 2 + w * k - 7, y - h, 14, h, color="#15100c")
        f.rect(x - w / 2 + w * k - 7, y - h, 14, 3, color="#6a6a70", alpha=0.5)
    f.rect(x - w / 2, y - h * 0.5 - 4, w, 8, color="#15100c")
    f.circle(x, y - h * 0.5, 10, color="#c9962b")
    f.circle(x, y - h * 0.5, 4, color="#2a1a08")
    if open_k > 0:
        top = sk.poly_path([(x - w / 2 + 6, y - h), (x - w / 2 + 22, y - h - 78 * open_k), (x + w / 2 - 22, y - h - 78 * open_k), (x + w / 2 - 6, y - h)], True)
        R.lit_path(f, top, "#2a190e", lights, rim="#a07a48", rim_w=1.0)
        f.rect(x - w / 2 + 20, y - h - 78 * open_k, w - 40, 7, color="#15100c")
        if gold:
            R.glow(f, x, y - h - 6, w * 0.9, "#ffc450", 0.42, sy=0.45)
            f.oval(x, y - h - 6, w / 2 - 12, 14, shader=f.lin(0, y - h - 20, 0, y - h + 8, [("#ffe9a0", 0.0), ("#e0a53a", 1.0)]))


def candelabra(f, x, y, branches=3, h=120, col="#b88a3a", arm=46):
    """Pirinç şamdan: sapı + kollar + mum gövdeleri (alevler dyn'de). Dönüş: alev uçlarının (x,y) listesi."""
    dk = shade(col, -0.5)
    f.oval(x, y - 2, 30, 7, color=dk)
    f.oval(x, y - 6, 24, 5, color=shade(col, -0.2))
    f.rect(x - 3.5, y - h, 7, h, shader=f.lin(x - 3.5, 0, x + 3.5, 0, [(dk, 0.0), (col, 0.5), (dk, 1.0)]))
    f.circle(x, y - h * 0.45, 6.5, color=col)
    tips = []
    n = branches
    for i in range(n):
        u = (i - (n - 1) / 2) / max(1, (n - 1) / 2) if n > 1 else 0
        ax = x + u * arm
        ay = y - h - abs(u) * 14
        p = skia.Path()
        p.moveTo(x, y - h * 0.7)
        p.quadTo(x + u * arm * 0.9, y - h * 0.6, ax, ay + 18)
        f.path(p, style="stroke", sw=3.4, color=col)
        f.oval(ax, ay + 18, 9, 3, color=shade(col, -0.2))
        f.rect(ax - 6, ay - 38, 12, 56, shader=f.lin(ax - 6, 0, ax + 6, 0, [("#9c8a5e", 0.0), ("#efe0b0", 0.5), ("#9c8a5e", 1.0)]))
        f.oval(ax, ay - 38, 6, 2, color="#fff1c8")
        tips.append((ax, ay - 38))
    return tips


def banner_hang(f, x, y, w, h, col="#27402c", trim="#c9962b", lights=(), icon=None):
    """Duvar halısı/sancak: dikdörtgen + altın şerit + saçak."""
    p = sk.poly_path([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + h), (x, y + h - 22), (x - w / 2, y + h)], True)
    R.lit_path(f, p, col, lights, rim=None, grad=f.lin(0, y, 0, y + h, [(shade(col, 0.1), 0.0), (col, 0.5), (shade(col, -0.35), 1.0)]))
    f.path(p, style="stroke", sw=3, color=trim, alpha=0.8)
    f.rect(x - w / 2 - 8, y - 6, w + 16, 8, color="#8a6a3a")
    f.rect(x - w / 2 + 12, y + 18, w - 24, 2.5, color=trim, alpha=0.6)
    f.rect(x - w / 2 + 12, y + h - 40, w - 24, 2.5, color=trim, alpha=0.6)
    for k in range(int(w / 14)):
        f.line(x - w / 2 + 7 + k * 14, y + h - 4, x - w / 2 + 7 + k * 14 + 1, y + h + 9, color=trim, sw=1.4, alpha=0.7)
    if icon:
        import icons
        icons.draw_icon(f, icon, x, y + h * 0.45, size=w * 0.5, metal="gold", shadow=False)


def desk_slant(f, x, y, w=300, h=190, lights=(), col="#3a2616"):
    """Katip yazı sırası (eğik tabla). x: sol uç, y: zemin. Tabla yüksekliği h."""
    top = sk.poly_path([(x, y - h), (x + w, y - h - 8), (x + w, y - h + 12), (x, y - h + 18)], True)
    R.lit_path(f, top, shade(col, 0.1), lights, rim="#d6a15a", rim_w=1.2)
    for lx in (x + 20, x + w - 24):
        R.lit_path(f, R.rect_path(lx - 8, y - h + 14, 16, h - 14), shade(col, -0.3), lights)
    f.rect(x + 20, y - h * 0.45, w - 44, 8, color=shade(col, -0.35))
    return top


def inkwell(f, x, y, s=1.0):
    f.rrect(x - 9 * s, y - 16 * s, 18 * s, 16 * s, 3 * s, color="#0f0a09")
    f.rect(x - 9 * s, y - 16 * s, 18 * s, 2 * s, color="#7a6a58", alpha=0.6)
    f.line(x + 5 * s, y - 14 * s, x + 20 * s, y - 52 * s, color="#d8ceb2", sw=1.6 * s)
    f.poly([(x + 20 * s, y - 52 * s), (x + 34 * s, y - 40 * s), (x + 22 * s, y - 36 * s)], color="#e6dcc2", alpha=0.8)


def wax_seal_letter(f, x, y, w=60, h=34, ang=-0.1, lights=()):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(ang))
    p = sk.poly_path([(-w / 2, 0), (-w / 2 + 6, -h), (w / 2 + 2, -h + 3), (w / 2 - 6, 0)], True)
    R.lit_path(f, p, "#cdbb8c", lights, edge="#6a5638")
    f.circle(0, -h * 0.45, 5, color="#8e1f26")
    f.c.restore()


def roof_silhouette(f, y, x0, x1, col="#05080f", seed=1, gables=True, spires=2):
    """Pencereden görünen şehir çatıları (gece/alacakaranlık)."""
    rs = np.random.RandomState(seed)
    x = x0
    while x < x1:
        w = rs.uniform(50, 120)
        hh = rs.uniform(30, 90)
        f.rect(x, y - hh, w, hh + 400, color=col)
        if gables:
            f.poly([(x - 4, y - hh), (x + w / 2, y - hh - rs.uniform(18, 46)), (x + w + 4, y - hh)], color=col)
        x += w + rs.uniform(-6, 10)
    for k in range(spires):
        sx = x0 + (x1 - x0) * (0.25 + 0.5 * rs.rand())
        f.rect(sx - 9, y - 170, 18, 200, color=col)
        f.poly([(sx - 13, y - 170), (sx, y - 270), (sx + 13, y - 170)], color=col)


def chair_high(f, x, y, s=1.0, lights=(), col="#3a2412", trim="#c9962b", pointed=True):
    """Yüksek arkalıklı oyma koltuk (önden). y: zemin. s: ölçek (1.0 → koltuk genişliği ~130 px)."""
    wd, bh, sh = 134 * s, 340 * s, 112 * s
    tp = bh + 44 * s
    pts = [(x - wd / 2, y - sh), (x - wd / 2, y - bh + 70 * s), (x - wd * 0.28, y - bh + 8 * s), (x, y - tp), (x + wd * 0.28, y - bh + 8 * s), (x + wd / 2, y - bh + 70 * s), (x + wd / 2, y - sh)]
    back = sk.smooth_path(pts, True, 0.18) if pointed else R.rect_path(x - wd / 2, y - bh, wd, bh - sh)
    R.lit_path(f, back, col, lights, rim="#9a7440", rim_w=1.4 * s, grad=f.lin(0, y - tp, 0, y - sh, [(shade(col, 0.18), 0.0), (col, 0.5), (shade(col, -0.35), 1.0)]))
    f.path(back, style="stroke", sw=2.2 * s, color=trim, alpha=0.55)
    # panel içi çift çizgi + dörtyaprak
    inner = sk.smooth_path([(a * 0.78 + x * 0.22, b * 0.8 + (y - sh) * 0.2) for a, b in pts[:-1]] + [(x + wd * 0.39, y - sh - 6 * s)], False, 0.18)
    f.path(inner, style="stroke", sw=1.4 * s, color=trim, alpha=0.4)
    for k in range(4):
        a = math.pi / 2 * k
        f.circle(x + math.cos(a) * 12 * s, y - bh * 0.62 + math.sin(a) * 12 * s, 9 * s, style="stroke", sw=1.6 * s, color=trim, alpha=0.5)
    f.circle(x, y - tp - 2 * s, 7 * s, color=trim, alpha=0.8)
    # oturak + yan kollar + ayaklar
    seat = R.rrect_path(x - wd / 2 - 10 * s, y - sh, wd + 20 * s, 20 * s, 4 * s)
    R.lit_path(f, seat, shade(col, 0.05), lights, rim="#b08850", rim_w=1.2 * s)
    f.rect(x - wd / 2 - 10 * s, y - sh + 20 * s, wd + 20 * s, 8 * s, color=trim, alpha=0.55)
    for sx in (-1, 1):
        R.lit_path(f, R.rect_path(x + sx * (wd / 2 + 2 * s) - 7 * s, y - sh - 52 * s, 14 * s, 52 * s), shade(col, -0.1), lights)
        R.lit_path(f, R.rect_path(x + sx * (wd / 2 - 6 * s) - 8 * s, y - sh + 28 * s, 16 * s, sh - 28 * s), shade(col, -0.35), lights)


def shield(f, x, y, w, col="#8e1f26", trim="#c9962b", charge=None, lights=()):
    """Gotik kalkan. charge: 'cross'|'bar'|'star'|None."""
    h = w * 1.2
    p = skia.Path()
    p.moveTo(x - w / 2, y - h / 2)
    p.lineTo(x + w / 2, y - h / 2)
    p.lineTo(x + w / 2, y + h * 0.1)
    p.cubicTo(x + w / 2, y + h * 0.35, x + w * 0.2, y + h * 0.5, x, y + h / 2)
    p.cubicTo(x - w * 0.2, y + h * 0.5, x - w / 2, y + h * 0.35, x - w / 2, y + h * 0.1)
    p.close()
    R.lit_path(f, p, col, lights, grad=f.lin(0, y - h / 2, 0, y + h / 2, [(shade(col, 0.2), 0.0), (col, 0.5), (shade(col, -0.35), 1.0)]))
    f.path(p, style="stroke", sw=max(2.0, w * 0.045), color=trim)
    if charge == "cross":
        f.rect(x - w * 0.07, y - h * 0.38, w * 0.14, h * 0.8, color=trim, alpha=0.9)
        f.rect(x - w * 0.34, y - h * 0.12, w * 0.68, w * 0.14, color=trim, alpha=0.9)
    elif charge == "bar":
        f.rect(x - w / 2 + 3, y - h * 0.1, w - 6, h * 0.2, color=trim, alpha=0.9)
    elif charge == "star":
        import icons
        icons.draw_icon(f, "star", x, y, size=w * 0.6, metal="gold", shadow=False)


def pointed_window(f, cx, cy, w, h, glow=("#ffe9b8", "#e8a84a"), frame="#2b190c", edge="#8a6338", tracery=True, k=1.0, pane=None):
    """Sivri vitray pencere (düz): içi parlak (emisyon). ST.gothic_window ile aynı geometri; pane ile renkli camlar."""
    ST.gothic_window(f, cx, cy, w, h, glow=glow, stone=frame, edge=edge, tracery=tracery, k=k)
    if pane:
        inner = ST.pointed_arch_path(cx, cy + h / 2, w, h)
        f.c.save()
        f.c.clipPath(inner, skia.ClipOp.kIntersect, True)
        rs = np.random.RandomState(int(cx) % 97)
        for i in range(6):
            for j in range(3):
                col = pane[rs.randint(len(pane))]
                f.rect(cx - w / 2 + j * w / 3, cy - h / 2 + i * h / 6, w / 3, h / 6, color=col, alpha=0.30, blend=skia.BlendMode.kMultiply)
        f.c.restore()


def cypress(f, x, y, h, w=None, col="#0a110b", rim="#5a7a58", rim_a=0.35, seed=1, rim_dir=1):
    """Selvi ağacı siluet (y: gövde dibi). Pürüzlü kenarlı uzun damla; bir yanda hafif kenar ışığı."""
    w = w or h * 0.17
    rs = np.random.RandomState(seed)
    n = 26
    L, Rr = [], []
    for i in range(n + 1):
        u = i / n
        yy = y - h * u
        prof = math.sin(math.pi * min(1.0, u * 0.98 + 0.02)) ** 0.62 * (1 - 0.15 * u)
        jit = 1 + (rs.rand() - 0.5) * 0.16
        wd = w * prof * jit
        L.append((x - wd, yy))
        Rr.append((x + wd * (1 + (rs.rand() - 0.5) * 0.1), yy))
    pts = L + Rr[::-1]
    path = sk.smooth_path(pts, True, 0.25)
    f.path(path, shader=f.lin(x - w, 0, x + w, 0, [(shade(col, 0.1 if rim_dir < 0 else -0.1), 0.0), (col, 0.5), (shade(col, 0.1 if rim_dir > 0 else -0.1), 1.0)]))
    f.c.save()
    f.c.clipPath(path, skia.ClipOp.kIntersect, True)
    for i in range(40):                      # yaprak dokusu
        yy = y - rs.rand() * h
        xx = x + (rs.rand() - 0.5) * w * 1.4
        f.line(xx, yy, xx + rs.uniform(-3, 3), yy - rs.uniform(10, 26), color="#1a2a18", sw=2.0, alpha=0.5)
    f.c.restore()
    if rim_a > 0:
        rpts = (Rr if rim_dir > 0 else L)
        f.path(sk.smooth_path(rpts, False, 0.25), style="stroke", sw=1.8, color=rim, alpha=rim_a)
    f.rect(x - w * 0.08, y - 6, w * 0.16, 14, color=shade(col, -0.3))


def fountain(f, x, y, s=1.0, stone="#6a6054", lights=(), rim="#c9b890"):
    """Taş çeşme/kuyu (önden): havuz + orta sütun + üst tas. y: taban."""
    bas = sk.smooth_path([(x - 150 * s, y), (x - 160 * s, y - 40 * s), (x + 160 * s, y - 40 * s), (x + 150 * s, y)], True, 0.2)
    R.lit_path(f, bas, stone, lights, rim=rim, rim_w=1.4, grad=f.lin(0, y - 40 * s, 0, y, [(shade(stone, 0.2), 0.0), (shade(stone, -0.35), 1.0)]))
    f.oval(x, y - 40 * s, 160 * s, 22 * s, color="#0e1218")
    f.oval(x, y - 40 * s, 160 * s, 22 * s, style="stroke", sw=3 * s, color=shade(stone, 0.2))
    f.oval(x, y - 38 * s, 130 * s, 15 * s, shader=f.lin(0, y - 52 * s, 0, y - 26 * s, [("#8da8c8", 0.0, 120), ("#1c2838", 1.0, 200)]))
    col_ = R.rect_path(x - 12 * s, y - 130 * s, 24 * s, 92 * s)
    R.lit_path(f, col_, stone, lights, rim=rim, rim_w=1.2)
    f.oval(x, y - 132 * s, 52 * s, 11 * s, color=shade(stone, -0.15))
    f.oval(x, y - 134 * s, 52 * s, 11 * s, style="stroke", sw=2 * s, color=shade(stone, 0.2))
    f.oval(x, y - 134 * s, 44 * s, 8 * s, color="#16202c")


# ───────────── altın eşyalar (Cajamarca fidyesi) ─────────────
def _gold_grad(f, x0, y0, x1, y1, dark=0.0):
    return f.lin(x0, y0, x1, y1, [("#fff0b0", 0.0), ("#e0a830", 0.38), ("#a87a24", 0.72), ("#5a3c10", 1.0)])


def g_plate(f, x, y, r, rot=0.0):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.oval(0, 2.0, r, r * 0.36, color="#5a3c10")
    f.oval(0, 0, r, r * 0.36, shader=_gold_grad(f, -r, -r * 0.36, r, r * 0.36))
    f.oval(0, 0, r * 0.72, r * 0.25, style="stroke", sw=max(0.8, r * 0.04), color="#fff0b0", alpha=0.55)
    f.oval(-r * 0.2, -r * 0.1, r * 0.25, r * 0.08, color="#ffffff", alpha=0.35)
    f.c.restore()


def g_sheet(f, x, y, w, h, rot=0.0):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    p = sk.poly_path([(-w / 2, -h / 2), (w / 2 + h * 0.2, -h / 2), (w / 2, h / 2), (-w / 2 - h * 0.2, h / 2)], True)
    f.path(p, shader=_gold_grad(f, -w / 2, -h / 2, w / 2, h / 2))
    f.path(p, style="stroke", sw=1.0, color="#fff0b0", alpha=0.6)
    f.line(-w * 0.3, -h * 0.2, w * 0.3, -h * 0.2, color="#fff6c8", sw=1.2, alpha=0.5)
    f.c.restore()


def g_vase(f, x, y, s, rot=0.0):
    """İnka aryballos'u: sivri tabanlı gövde, dar boyun, geniş ağız, iki kulp."""
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.c.scale(s, s)
    body = skia.Path()
    body.moveTo(0, 0)
    body.cubicTo(-22, -6, -30, -34, -20, -58)
    body.cubicTo(-14, -70, -8, -74, -8, -82)
    body.lineTo(-13, -92)
    body.lineTo(13, -92)
    body.lineTo(8, -82)
    body.cubicTo(8, -74, 14, -70, 20, -58)
    body.cubicTo(30, -34, 22, -6, 0, 0)
    body.close()
    f.path(body, shader=f.lin(-30, 0, 30, 0, [("#6a4814", 0.0), ("#f1cf6a", 0.42), ("#c9962b", 0.6), ("#5a3c10", 1.0)]))
    f.path(body, style="stroke", sw=1.2, color="#fff0b0", alpha=0.35)
    f.oval(0, -92, 13, 3.4, color="#fff0b0", alpha=0.8)
    for sx in (-1, 1):
        h = skia.Path()
        h.moveTo(sx * 19, -52)
        h.cubicTo(sx * 34, -50, sx * 34, -32, sx * 24, -30)
        f.path(h, style="stroke", sw=4.2, color="#c9962b")
    f.rect(-22, -50, 44, 3, color="#6a4814", alpha=0.6)
    f.c.restore()


def g_cup(f, x, y, s, rot=0.0):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    f.c.scale(s, s)
    p = sk.poly_path([(-10, 0), (10, 0), (16, -40), (-16, -40)], True)
    f.path(p, shader=f.lin(-16, 0, 16, 0, [("#6a4814", 0.0), ("#f1cf6a", 0.45), ("#5a3c10", 1.0)]))
    f.oval(0, -40, 16, 4.5, color="#fff0b0", alpha=0.85)
    f.oval(0, -40, 13, 3.2, color="#3a2608")
    f.rect(-14, -20, 28, 3, color="#fff0b0", alpha=0.35)
    f.c.restore()


def g_llama(f, x, y, s, flip=1):
    f.c.save()
    f.c.translate(x, y)
    f.c.scale(s * flip, s)
    pts = [(-22, -22), (-22, -34), (-8, -36), (6, -34), (10, -52), (12, -66), (20, -70), (24, -66), (20, -60), (16, -48), (16, -34), (14, -24), (14, 0), (10, 0), (8, -22), (-8, -22), (-10, 0), (-14, 0), (-16, -22)]
    p = sk.smooth_path(pts, True, 0.18)
    f.path(p, shader=f.lin(-24, -70, 24, 0, [("#fff0b0", 0.0), ("#e0a830", 0.4), ("#8a6220", 1.0)]))
    f.path(p, style="stroke", sw=1.0, color="#fff0b0", alpha=0.5)
    f.c.restore()


def g_bar(f, x, y, w, h, rot=0.0):
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    p = sk.poly_path([(-w / 2, h / 2), (w / 2, h / 2), (w / 2 - h * 0.3, -h / 2), (-w / 2 + h * 0.3, -h / 2)], True)
    f.path(p, shader=f.lin(0, -h / 2, 0, h / 2, [("#fff0b0", 0.0), ("#e0a830", 0.5), ("#7a5518", 1.0)]))
    f.line(-w / 2 + h * 0.3, -h / 2, w / 2 - h * 0.3, -h / 2, color="#ffffff", sw=1.2, alpha=0.5)
    f.c.restore()


def g_mask(f, x, y, r, rot=0.0):
    """Güneş diski (Inti): halkalı disk + ışınlar."""
    f.c.save()
    f.c.translate(x, y)
    f.c.rotate(math.degrees(rot))
    for i in range(14):
        a = 2 * math.pi * i / 14
        f.poly([(math.cos(a - 0.14) * r, math.sin(a - 0.14) * r), (math.cos(a) * r * 1.38, math.sin(a) * r * 1.38), (math.cos(a + 0.14) * r, math.sin(a + 0.14) * r)], color="#c9962b")
    f.circle(0, 0, r, shader=f.rad(-r * 0.3, -r * 0.3, r * 1.4, [("#fff0b0", 0.0), ("#e0a830", 0.5), ("#7a5518", 1.0)]))
    f.circle(0, 0, r * 0.62, style="stroke", sw=max(1.0, r * 0.07), color="#8a6220")
    f.circle(0, 0, r * 0.26, color="#fff0b0", alpha=0.75)
    f.c.restore()


def hoard_items(seed=3, n=260, cx=930.0, base=888.0, half=470.0, H=360.0):
    """Altın yığını öğeleri: [dict(tür,x,y,s,rot,rank)] — yığın profili tümsek; rank 0..1 (alttan üste, jitter'lı)."""
    rs = np.random.RandomState(seed)
    items = []
    tries = 0
    while len(items) < n and tries < n * 30:
        tries += 1
        x = cx + (rs.rand() * 2 - 1) * half
        u = abs(x - cx) / half
        skew = 1.0 - 0.28 * np.tanh((x - cx) / half * 1.5)
        top = base - H * max(0.0, 1 - u ** 2.0) ** 0.85 * skew
        y = base - 6 - rs.rand() ** 0.8 * (base - top)
        if y > base - 4:
            continue
        kind = rs.choice(["plate", "sheet", "vase", "cup", "llama", "bar", "mask"], p=[0.26, 0.2, 0.12, 0.10, 0.08, 0.14, 0.10])
        depth = (base - y) / H
        s = 0.8 + 0.5 * (1 - depth * 0.3) + rs.rand() * 0.3
        rank = float(np.clip((base - y) / H * 0.82 + rs.rand() * 0.18, 0, 1))
        items.append(dict(k=kind, x=x, y=y, s=s, rot=(rs.rand() - 0.5) * 1.0, rank=rank, f=1 if rs.rand() > 0.5 else -1, seed=int(rs.randint(1 << 30))))
    items.sort(key=lambda d: d["y"])
    return items


def draw_hoard(f, items, rank_lo=0.0, rank_hi=1.0):
    for it in items:
        if not (rank_lo < it["rank"] <= rank_hi):
            continue
        k, x, y, s, rot = it["k"], it["x"], it["y"], it["s"], it["rot"]
        if k == "plate":
            g_plate(f, x, y, 34 * s, rot * 0.5)
        elif k == "sheet":
            g_sheet(f, x, y, 62 * s, 26 * s, rot)
        elif k == "vase":
            g_vase(f, x, y + 10, 0.78 * s, rot * 0.7)
        elif k == "cup":
            g_cup(f, x, y + 4, 0.8 * s, rot * 0.6)
        elif k == "llama":
            g_llama(f, x, y + 2, 0.85 * s, it["f"])
        elif k == "bar":
            g_bar(f, x, y, 52 * s, 20 * s, rot * 0.6)
        else:
            g_mask(f, x, y, 24 * s, rot * 0.5)
