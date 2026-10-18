"""cilt_build — ZAMAN ATLAMALI YAPIM çekimleri (`build` çekim türü).

  build="dome"   : Brunelleschi'nin kubbesi. Sekizgen tambur üstünde sivri çift kabuk; balık kılçığı (spina pesce) tuğla sıra sıra yükselir (sıra sıra, halka boyunca
                   soldan sağa örülür), beyaz mermer nervürler, ahşap iskele halkası + dikmeler, vinç (halat + yük sarkacı) ve dönen çark, küçük işçi figürleri,
                   kireç ocağı dumanı, kuşlar. Kamera `crane up` (üst kenarı izler) + yavaş `orbit` (≤12°); gün ışığı ilerler (şafak → öğle → gün batımı).
  build="uffizi" : tek noktalı perspektifte iki kanatlı Uffizi avlusu + Arno ucundaki revak; cephe katları (portico → ara kat → piano nobile → çatı revağı) yükselir,
                   iskele, vinç, taş yığınları, işçiler, toz; kamera avluya doğru yavaşça ilerler ve yükselir; ışık ilerler.
`shot("build", a, build="dome", p=(çapa_başlangıç, çapa_bitiş), orbit=10, kick=…, caption=…)` — p verilmezse tüm çekim; cam/link/longtake/montage kabul edilir ve yok sayılır.
"""
import functools
import math

import numpy as np
import skia

import cilt_anim as FA
import cilt_city as CT
import cilt_medici as CM
import cilt_pano as PN
import cilt_scene as SC
import sk
from cilt_medici import TH, ckind
from sk import C, H, W, clamp, ease_io, mix, smooth

INK = "#2A1A0C"
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
D2R = math.pi / 180.0


# ═════════════════════════════ ışık: gün ilerler ═════════════════════════════
SKY_KEYS = [  # (p, üst, orta, ufuk, güneş rengi, genel ton alfa)
    (0.00, "#6C7FB8", "#F0B49A", "#FBD9A0", "#FFD08A"),
    (0.25, "#6F9ED6", "#BCD2E2", "#F4E8C8", "#FFF0C8"),
    (0.55, "#5E92D0", "#B4CEE2", "#F6EEDA", "#FFF8E0"),
    (0.80, "#7A8FC4", "#E8B896", "#FAD9A0", "#FFD79A"),
    (1.00, "#5A5C9C", "#E8946A", "#F6C58A", "#FFB86A"),
]


def _lerp_col(a, b, t):
    return mix(a, b, t)


def sky_cols(p):
    for i in range(len(SKY_KEYS) - 1):
        a, b = SKY_KEYS[i], SKY_KEYS[i + 1]
        if p <= b[0] + 1e-9:
            t = (p - a[0]) / max(1e-6, (b[0] - a[0]))
            t = t * t * (3 - 2 * t)
            return tuple(_lerp_col(a[k], b[k], t) for k in range(1, 5))
    return SKY_KEYS[-1][1:]


_SKYIMG = {}


def sky_image(p, h=900):
    """Gün evresine göre gökyüzü degradesi (p nicemlenir: 24 adım; görüntü önbelleği)."""
    key = int(round(p * 24))
    if key not in _SKYIMG:
        top, mid, hor, sun = sky_cols(key / 24.0)
        fr = sk.Frame(W, h)
        sh = skia.GradientShader.MakeLinear([(0, 0), (0, h * 0.82)], [C(top), C(mid), C(hor)], [0.0, 0.58, 1.0])
        fr.c.drawRect(skia.Rect.MakeWH(W, h), skia.Paint(Shader=sh))
        _SKYIMG[key] = fr.surf.makeImageSnapshot()
    return _SKYIMG[key]


def sun_state(p):
    """Güneş: azimut (sol=doğu → sağ=batı), yükseklik (0..1), renk."""
    az = lerp_(-70.0, 70.0, p)
    el = 0.18 + 0.82 * math.sin(math.pi * clamp(p)) ** 0.8
    return az, el, sky_cols(p)[3]


def lerp_(a, b, t):
    return a + (b - a) * t


# ═════════════════════════════ KUBBE ═════════════════════════════
NC = 40                    # kubbe sıra sayısı
R0 = 262.0                 # taban yarıçapı (sekizgen köşesine)
R_TOP = 34.0
H_DRUM = 168.0
H_DOME = 400.0
BASE_Y = 842.0             # zemin (ekran, kamera yükselmeden)


def prof(u):
    """Sivri kabuk profili: u∈[0,1] → yarıçap."""
    return R0 * (1.0 - u ** 1.7) ** 0.62 * (1 - 0.0) + R_TOP * u ** 2 * (1 - 0.0) * 0.0 + R_TOP * u


class DomeScene:
    def __init__(self, tod, seed):
        self.tod = tod
        self.seed = seed
        self.T = CT.Tint("night" if tod == "night" else "day")
        rs = np.random.RandomState(seed)
        self.houses = []
        x = -60
        while x < W + 100:
            bw, bh = rs.uniform(70, 150), rs.uniform(60, 130)
            self.houses.append((x, bw, bh, int(rs.randint(1, 10 ** 6))))
            x += bw + rs.uniform(-12, 8)
        self.cl = [(rs.uniform(0, 2400), rs.uniform(120, 360), rs.uniform(220, 440), rs.uniform(5, 13), rs.uniform(0.5, 0.95)) for _ in range(9)]

    # projeksiyon: (ρ, ψ(derece), Y) → ekran
    def proj(self, rho, psi, Y, a, e, cam_y, cx_=W / 2):
        pp = (psi - a) * D2R
        X = rho * math.sin(pp)
        Z = rho * math.cos(pp)
        ce, se = math.cos(e * D2R), math.sin(e * D2R)
        return cx_ + X, BASE_Y + cam_y - (Y * ce - Z * se), Z


def face_shade(psi_face, a, az_sun, el):
    """Yüz parlaklığı: güneş azimutuna göre."""
    ang = (psi_face - a - az_sun) * D2R
    d = math.cos(ang)
    return 0.62 + 0.40 * max(0.0, d) * (0.6 + 0.6 * el) - 0.14 * max(0.0, -d)


def brick_col(base, shade):
    return mix("#1A0E08", base, clamp(shade, 0.0, 1.35) / 1.35) if shade < 1.0 else mix(base, "#FFE9C0", min(0.35, (shade - 1.0) * 1.5))


def draw_dome(ctx_f, cx, p, t, tod, scene, a_orbit, kind="dome"):
    f = ctx_f
    c = f.c
    night = tod == "night"
    e = 13.0
    az_sun, el, sun_col = sun_state(p)
    a = a_orbit
    # ── ilerleme: kubbe yüksekliği
    n_done = p * NC * 1.0
    J = int(math.floor(n_done))
    frac = n_done - J
    J = min(J, NC)
    Y_top = H_DRUM + (J / NC) * H_DOME if J < NC else H_DRUM + H_DOME
    # kamera yükselir: üst kenarı ekranın ~40%'ında tut
    cam_y = max(0.0, (Y_top - 330.0)) * 0.92
    # ── gökyüzü + güneş
    c.drawImage(sky_image(p), 0, 70 - 60 + PN_OFF(), LIN) if False else None
    c.save()
    c.translate(0, 70)
    c.drawImage(sky_image(p), 0, 0)
    c.restore()
    # güneş (yay üzerinde)
    sx = W / 2 + az_sun / 70.0 * 780
    sy = 640 - 520 * el * 0.9 + 90
    for (r, aa) in ((190, 36), (110, 70), (48, 190)):
        c.drawCircle(sx, sy, r, skia.Paint(AntiAlias=True, Color=C(sun_col, aa), BlendMode=skia.BlendMode.kPlus, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.5) if r > 48 else None))
    c.drawCircle(sx, sy, 30, skia.Paint(AntiAlias=True, Color=C("#FFFBE8")))
    # bulutlar
    cs = PN.cloud_sprite()
    pt = skia.Paint()
    for (x0, y, L, sp, al) in scene.cl:
        x = (x0 + t * sp) % (W + 800) - 400
        pt.setAlphaf(al * (0.9 if not night else 0.3))
        c.drawImageRect(cs, skia.Rect.MakeWH(cs.width(), cs.height()), skia.Rect.MakeXYWH(x, y + 60 - cam_y * 0.15, L, L * 0.22), LIN, pt)
    # tepeler (Fiesole) — uzak, yavaş
    T = scene.T
    for (col, amp, sc, base, ph, fx) in (("#A9BDB6", 34, 520, 620, 0.0, 0.1), ("#93AFA5", 40, 380, 668, 2.0, 0.18)):
        cc = T(col, 0.2)
        pts = []
        xx = -8
        while xx <= W + 8:
            pts.append((xx, PN.ridge_y(xx + a * 12, base + 60 + cam_y * 0.2, amp, sc, ph)))
            xx += 8
        c.drawPath(sk.poly_path(pts + [(W + 8, 1000), (-8, 1000)]), skia.Paint(AntiAlias=True, Color=C(cc)))
    # ── kubbe
    N8 = 8
    base_ang = [k * 45.0 for k in range(N8)]            # yüz merkezleri
    corner_ang = [k * 45.0 - 22.5 for k in range(N8 + 1)]      # köşeler: yüz k: corner[k]..corner[k+1]
    cosR = math.cos(22.5 * D2R)
    stone_base = "#C65B33" if not night else "#4A2A22"

    def corner_pt(k, rho, Y):
        return scene.proj(rho / cosR, corner_ang[k], Y, a, e, cam_y)

    # tambur: yüzlerin ön/arka belirlenmesi
    def face_visible(k):
        return math.cos((base_ang[k] - a) * D2R) > -0.05

    order_back = [k for k in range(N8) if not face_visible(k)]
    order_front = [k for k in range(N8) if face_visible(k)]
    order_front.sort(key=lambda k: -abs(math.cos((base_ang[k] - a) * D2R)) + 0.0)
    # zemin taşıyıcı: tribün çatısı (kırmızı) — basit sekizgen taban
    base_poly = [scene.proj(R0 * 1.12 / cosR, corner_ang[k], -26.0, a, e, cam_y)[:2] for k in range(N8)]
    c.drawPath(sk.poly_path(base_poly), skia.Paint(AntiAlias=True, Color=C(T("#8E7E5E", 0.0))))
    # tambur yüzleri (ön) — mermer + yeşil bantlar + yuvarlak göz
    def draw_drum_face(k):
        q = [corner_pt(k, R0, 0.0), corner_pt(k + 1, R0, 0.0), corner_pt(k + 1, R0, H_DRUM), corner_pt(k, R0, H_DRUM)]
        sh = face_shade(base_ang[k], a, az_sun, el)
        col = brick_col(T("#EFE5CC", 0.0), sh)
        path = sk.poly_path([(x, y) for x, y, z in q])
        c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(col)))
        # yeşil mermer bantlar
        for fr_ in (0.30, 0.62):
            b0 = (q[0][0] + (q[3][0] - q[0][0]) * fr_, q[0][1] + (q[3][1] - q[0][1]) * fr_)
            b1 = (q[1][0] + (q[2][0] - q[1][0]) * fr_, q[1][1] + (q[2][1] - q[1][1]) * fr_)
            c.drawLine(b0[0], b0[1], b1[0], b1[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C(brick_col(T("#6E9878", 0.0), sh))))
        # göz (oculus)
        cx0 = sum(x for x, y, z in q) / 4
        cy0 = sum(y for x, y, z in q) / 4
        fw = abs(q[1][0] - q[0][0])
        rr = 0.17 * fw
        c.drawOval(skia.Rect.MakeLTRB(cx0 - rr * 1.0, cy0 - rr * 1.4, cx0 + rr * 1.0, cy0 + rr * 1.4), skia.Paint(AntiAlias=True, Color=C(brick_col(T("#2A2018", 0.0), 0.9))))
        c.drawOval(skia.Rect.MakeLTRB(cx0 - rr * 1.0, cy0 - rr * 1.4, cx0 + rr * 1.0, cy0 + rr * 1.4), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(brick_col(T("#E8DEC4", 0.0), sh))))
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 190)))
    for k in order_back:                                    # arka yüzler (tambur): koyu
        q = [corner_pt(k, R0, 0.0), corner_pt(k + 1, R0, 0.0), corner_pt(k + 1, R0, H_DRUM), corner_pt(k, R0, H_DRUM)]
        c.drawPath(sk.poly_path([(x, y) for x, y, z in q]), skia.Paint(AntiAlias=True, Color=C(brick_col(T("#EFE5CC", 0.0), 0.45))))
    # kubbe içi (arka yüzeyin iç görünüşü; açık tepe) — koyu tuğla
    def course_quad(k, j, rho_scale=1.0):
        u0, u1 = j / NC, (j + 1) / NC
        r0_, r1_ = prof(u0) * rho_scale, prof(u1) * rho_scale
        Y0, Y1 = H_DRUM + u0 * H_DOME, H_DRUM + u1 * H_DOME
        return [corner_pt(k, r0_, Y0), corner_pt(k + 1, r0_, Y0), corner_pt(k + 1, r1_, Y1), corner_pt(k, r1_, Y1)]
    jmax = J + (1 if frac > 0 else 0)
    for k in order_back:
        sh = 0.40
        for j in range(0, min(jmax, NC)):
            q = course_quad(k, j)
            col = brick_col(stone_base, sh)
            c.drawPath(sk.poly_path([(x, y) for x, y, z in q]), skia.Paint(AntiAlias=True, Color=C(col)))
    # ön yüzler: tambur
    for k in order_front:
        draw_drum_face(k)
    # ön yüzler: kubbe kabuğu sıraları (balık kılçığı)
    seam = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.1, Color=C("#5A2412", 120))
    for k in order_front:
        sh = face_shade(base_ang[k], a, az_sun, el)
        # küçük merdiven: ışık kenara çarpınca yumuşak degrade yok; düz tonlama
        for j in range(0, min(jmax, NC)):
            q = course_quad(k, j)
            partial = (j == J and frac > 0)
            pts = [(x, y) for x, y, z in q]
            col = brick_col(stone_base, sh * (0.95 + 0.10 * ((j * 7 + k * 3) % 5) / 5.0))
            if partial:
                # soldan sağa örülüyor: ilerleme yüz sıralamasına göre (k küçükten büyüğe)
                vis_i = order_front.index(k) if False else 0
                nfr = len(order_front)
                idx_ = sorted(order_front).index(k)
                rr_ = clamp(frac * nfr - idx_)
                if rr_ <= 0:
                    continue
                if rr_ < 1.0:
                    # kuvadrilateri kısmi kırp: sol kenardan rr_ oranında
                    p0, p1, p2, p3 = pts
                    pts = [p0, (p0[0] + (p1[0] - p0[0]) * rr_, p0[1] + (p1[1] - p0[1]) * rr_), (p3[0] + (p2[0] - p3[0]) * rr_, p3[1] + (p2[1] - p3[1]) * rr_), p3]
            path = sk.poly_path(pts)
            c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(col)))
            # balık kılçığı: kuşak boyunca zikzak
            p0, p1, p2, p3 = pts
            nz = 9
            zz = skia.Path()
            for i in range(nz + 1):
                u = i / nz
                bx, by = p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u
                tx, ty = p3[0] + (p2[0] - p3[0]) * u, p3[1] + (p2[1] - p3[1]) * u
                if i == 0:
                    zz.moveTo(bx, by)
                x_, y_ = (tx, ty) if i % 2 == 0 else (bx, by)
                zz.lineTo(x_, y_)
            c.drawPath(zz, seam)
            c.drawLine(p0[0], p0[1], p1[0], p1[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#3A1608", 150)))
    # nervürler (beyaz mermer): köşelerde
    top_u = min(1.0, jmax / NC)
    for k in range(N8 + 1):
        psi = corner_ang[k]
        if math.cos((psi - a) * D2R) < -0.25:
            continue
        pts = []
        nstep = max(2, jmax)
        for j in range(0, nstep + 1):
            u = min(1.0, j / NC)
            if j > jmax:
                break
            x_, y_, z_ = scene.proj(prof(u) / cosR, psi, H_DRUM + u * H_DOME, a, e, cam_y)
            pts.append((x_, y_))
        # tambur boyunca da (zeminden)
        base_pt = scene.proj(R0 / cosR, psi, 0.0, a, e, cam_y)[:2]
        pts = [base_pt, scene.proj(R0 / cosR, psi, H_DRUM, a, e, cam_y)[:2]] + pts
        path = sk.poly_path(pts, False)
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=13, Color=C(INK, 120), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9.5, Color=C(brick_col(T("#F2EAD4", 0.0), 1.05)), StrokeCap=skia.Paint.kRound_Cap))
    # tambur üst silme
    # fener (bitişte)
    if p > 0.965:
        k_ = smooth((p - 0.965) / 0.035)
        lx, ly, lz = scene.proj(0.0, 0.0, H_DRUM + H_DOME, a, e, cam_y)
        lw = 46
        c.save()
        c.translate(lx, ly)
        c.scale(1.0, 1.0)
        col = brick_col(T("#EFE5CC", 0.0), 1.0)
        top = -176 * k_
        c.drawRect(skia.Rect.MakeLTRB(-lw * 0.5, top, lw * 0.5, 0), skia.Paint(AntiAlias=True, Color=C(col)))
        c.drawRect(skia.Rect.MakeLTRB(-lw * 0.5, top, lw * 0.5, 0), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 190)))
        for dx in (-0.28, 0.0, 0.28):
            c.drawOval(skia.Rect.MakeLTRB(lw * dx - 5, top * 0.85, lw * dx + 5, top * 0.35), skia.Paint(AntiAlias=True, Color=C("#3A2A18", 210)))
        if k_ > 0.6:
            c.drawPath(sk.poly_path([(-lw * 0.6, top), (0, top - 74 * k_), (lw * 0.6, top)]), skia.Paint(AntiAlias=True, Color=C(brick_col(T("#E3D8BA", 0.0), 1.0))))
            c.drawCircle(0, top - 80 * k_, 6, skia.Paint(AntiAlias=True, Color=C("#D8A63A")))
        c.restore()
    # ── iskele: halka platform + dikmeler
    if p < 0.985:
        ring_r = (prof(min(1.0, jmax / NC)) if jmax < NC else R_TOP * 2) / cosR + 34
        Yp = H_DRUM + min(1.0, jmax / NC) * H_DOME if jmax >= 1 else H_DRUM
        _scaffold(c, scene, a, e, cam_y, ring_r, Yp, t, p, T, night)
    # ── işçiler (platformda) + vinç + toz
    if p < 0.985:
        _workers(f, scene, a, e, cam_y, ring_r, Yp, t, T)
        _crane(c, scene, a, e, cam_y, ring_r, Yp, t, T, p)
    # zemin: şehir siluetini ön plana çiz (ağaçlar/evler) + zemin şeridi
    gy = BASE_Y + cam_y
    c.drawRect(skia.Rect.MakeLTRB(0, gy - 30, W, 1100), skia.Paint(Color=C(T("#9A8A68", 0.0))))
    wins = []
    for (x, bw, bh, sd) in scene.houses:
        rs = np.random.RandomState(sd)
        CT.draw_house(c, x, gy + 4, bw, bh, rs, T, 0.0, wins)
    c.drawRect(skia.Rect.MakeLTRB(0, gy + 4, W, 1100), skia.Paint(Color=C(T("#8A7A58", 0.0))))
    for i in range(14):
        xx = ((i * 233 + 40) % (W + 200)) - 100
        c.drawLine(xx, gy + 20, xx + 30, gy + 20, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#3A2A18", 70)))
    # kireç ocağı + duman (sol)
    kx, ky = 170, gy - 8
    c.drawRect(skia.Rect.MakeLTRB(kx - 40, ky - 70, kx + 40, ky), skia.Paint(Color=C(T("#8A6A48", 0.0))))
    c.drawRect(skia.Rect.MakeLTRB(kx - 40, ky - 70, kx + 40, ky), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C(INK, 190)))
    c.drawOval(skia.Rect.MakeLTRB(kx - 14, ky - 40, kx + 14, ky - 6), skia.Paint(AntiAlias=True, Color=C("#FF9A3A", 230)))
    for q in range(8):
        ph = (t * 0.13 + q / 8.0) % 1.0
        FA._puff(c, kx + 8 + math.sin(ph * 5 + q) * 18 * ph + ph * 40 * (1 + 0.6 * math.sin(t * 0.3)), ky - 76 - ph * 260, 10 + 36 * ph, 0.34 * (1 - ph), "#C8C0B4" if not night else "#6A7A9A")
    return cam_y, ring_r if p < 0.985 else R_TOP * 2, Yp if p < 0.985 else Y_top


def PN_OFF():
    return 0


def _scaffold(c, scene, a, e, cam_y, ring_r, Yp, t, p, T, night):
    wood = T("#7A5230", 0.0)
    dark = "#3A2410"
    nseg = 36
    # arka yarı (platform): önce çiz
    def ring_pts(r, Y, psi0, psi1):
        return [scene.proj(r, psi0 + (psi1 - psi0) * i / 18.0, Y, a, e, cam_y)[:2] for i in range(19)]
    back = ring_pts(ring_r, Yp, a + 90, a + 270)
    c.drawPath(sk.poly_path(back, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, Color=C(dark, 220), StrokeCap=skia.Paint.kRound_Cap))
    c.drawPath(sk.poly_path(back, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
    # ön yarı + dikmeler
    front = ring_pts(ring_r, Yp, a - 90, a + 90)
    for lvl in (0, 1, 2):
        Yl = Yp - lvl * 105
        if Yl < H_DRUM * 0.4:
            continue
        rr = ring_r + lvl * 14
        fp = ring_pts(rr, Yl, a - 90, a + 90)
        c.drawPath(sk.poly_path(fp, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.5, Color=C(dark, 220), StrokeCap=skia.Paint.kRound_Cap))
        c.drawPath(sk.poly_path(fp, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.6, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
    for k in range(-4, 5):
        psi = a + k * 22.5
        x0, y0, z0 = scene.proj(ring_r, psi, Yp + 54, a, e, cam_y)
        x1, y1, z1 = scene.proj(ring_r + 28, psi, max(0.0, Yp - 230), a, e, cam_y)
        c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(dark, 220), StrokeCap=skia.Paint.kRound_Cap))
        c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
        if k < 4:
            xn, yn, zn = scene.proj(ring_r + 8, psi + 22.5, Yp - 62, a, e, cam_y)
            xm, ym, zm = scene.proj(ring_r + 8, psi, Yp - 4, a, e, cam_y)
            c.drawLine(xm, ym, xn, yn, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C(wood)))


def _workers(f, scene, a, e, cam_y, ring_r, Yp, t, T):
    c = f.c
    kinds = ["halk", "halk", "tuccar", "denizci", "halk", "cocuk", "halk"]
    rs = np.random.RandomState(9)
    for i, psi_off in enumerate((-64, -41, -17, 8, 31, 55, 74)):
        psi = a + psi_off
        x, y, z = scene.proj(ring_r - 6, psi, Yp, a, e, cam_y)
        k = kinds[i % len(kinds)]
        dirn = 1 if (i % 2 == 0) else -1
        FA.actor(f, k, x, y + 2, 46, t + i * 0.7, action="talk" if i % 3 else "idle", dir=dirn, seed=i + 60, phase=i * 0.21, energy=0.6)
    # tuğla taşıyan işçi (platformda yürür)
    for i in range(2):
        u = ((t * 0.045 + i * 0.5) % 1.0)
        psi = a - 66 + u * 132
        x, y, z = scene.proj(ring_r - 12, psi, Yp, a, e, cam_y)
        FA.walker(f, "halk", x, y + 2, 46, t, speed=24.0, dir=1, seed=70 + i, phase=i * 0.4, prop="basket")


def _crane(c, scene, a, e, cam_y, ring_r, Yp, t, T, p):
    """Vinç: platform kenarında direk + bom; halat yer çarkına iner; yük sallanarak çıkıp iner; çark döner."""
    wood = T("#7A5230", 0.0)
    dark = "#3A2410"
    psi_c = a + 58
    bx, by, bz = scene.proj(ring_r, psi_c, Yp, a, e, cam_y)
    tx, ty = bx, by - 190
    # direk (iki ayaklı)
    for dx in (-18, 18):
        c.drawLine(bx + dx, by + 4, tx + dx * 0.25, ty, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C(dark), StrokeCap=skia.Paint.kRound_Cap))
        c.drawLine(bx + dx, by + 4, tx + dx * 0.25, ty, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.4, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
    # bom (dışa uzanır)
    ex, ey = tx + 150, ty + 36
    c.drawLine(tx, ty, ex, ey, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C(dark), StrokeCap=skia.Paint.kRound_Cap))
    c.drawLine(tx, ty, ex, ey, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.4, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
    c.drawLine(tx + 4, ty + 40, ex - 4, ey + 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C(wood)))
    # yer çarkı (sağ altta) — dönen
    gx, gy = ex + 90, BASE_Y + cam_y - 62
    cyc = 7.0
    ph = (t % cyc) / cyc
    up = smooth(ph / 0.55) * (1 if ph < 0.55 else 0.0) + (1 - smooth((ph - 0.62) / 0.38)) * (1 if ph >= 0.55 else 0.0)
    load_x = ex + math.sin(t * 1.3) * 3.0 * (up)
    load_y = lerp_(gy - 20, ey + 40, up)
    # halat
    c.drawLine(ex, ey, load_x, load_y, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C("#6A5A3A", 235)))
    # yük (tuğla paketi)
    c.drawRect(skia.Rect.MakeLTRB(load_x - 14, load_y, load_x + 14, load_y + 20), skia.Paint(AntiAlias=True, Color=C("#B8553A")))
    c.drawRect(skia.Rect.MakeLTRB(load_x - 14, load_y, load_x + 14, load_y + 20), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 200)))
    for k in range(3):
        c.drawLine(load_x - 14, load_y + 6 + k * 5, load_x + 14, load_y + 6 + k * 5, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#5A2412", 150)))
    # çark: halat ucundan çevrilen büyük tekerlek
    wr = 52
    c.save()
    c.translate(gx, gy)
    c.rotate((load_y * 1.2) % 360)
    c.drawCircle(0, 0, wr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C(dark)))
    c.drawCircle(0, 0, wr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4.2, Color=C(wood)))
    for k in range(8):
        ang = k * math.pi / 4
        c.drawLine(0, 0, wr * math.cos(ang), wr * math.sin(ang), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C(wood)))
    c.drawCircle(0, 0, 7, skia.Paint(AntiAlias=True, Color=C(dark)))
    c.restore()
    c.drawLine(gx, gy + wr, gx, BASE_Y + cam_y, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(dark)))
    # halat çark ile bom arasında
    c.drawLine(gx - wr * 0.98, gy, ex, ey, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=C("#6A5A3A", 160)))
    # toz: platform üstünde
    for q in range(6):
        ph2 = (t * 0.22 + q / 6.0) % 1.0
        FA._puff(c, bx - 160 + q * 40 + math.sin(ph2 * 4 + q) * 12, by - 24 - ph2 * 90, 8 + 20 * ph2, 0.20 * (1 - ph2), "#D8C8A8")


# ═════════════════════════════ UFFIZI ═════════════════════════════
class Persp:
    """Tek noktalı perspektif: X yanal (sol −), Y yukarı, Z derinlik (kameradan uzak +)."""

    def __init__(self, f, hz, cx=W / 2, camy=0.0):
        self.f, self.hz, self.cx, self.camy = f, hz, cx, camy

    def pt(self, X, Y, Z):
        s = self.f / Z
        return self.cx + X * s, self.hz - (Y - self.camy) * s


COURT_W = 13.0
WALL_Z0, WALL_Z1 = 7.0, 120.0
LEVELS = [(0.0, 7.5, "portico"), (7.5, 11.5, "mezz"), (11.5, 19.0, "nobile"), (19.0, 24.0, "attic")]
BAY = 4.4


def draw_uffizi(f, cx, p, t, tod, scene_seed):
    c = f.c
    night = tod == "night"
    T = CT.Tint("night" if night else "day")
    az, el, sun_col = sun_state(p)
    u_dolly = ease_io(clamp(cx.t / max(cx.dur, 1e-6)))
    fl = 300.0 + 120.0 * u_dolly
    hz = 520.0 - 60.0 * p
    camy = 4.2 + 6.0 * p
    P = Persp(fl, hz, W / 2, camy)
    # ── gökyüzü, tepeler, nehir (uzak uç)
    c.save()
    c.translate(0, 70)
    c.drawImage(sky_image(p), 0, 0)
    c.restore()
    cs = PN.cloud_sprite()
    pt = skia.Paint()
    rs = np.random.RandomState(scene_seed)
    for i in range(8):
        x0, y, L, sp = rs.uniform(0, 2400), rs.uniform(150, 380), rs.uniform(240, 460), rs.uniform(5, 12)
        x = (x0 + t * sp) % (W + 800) - 400
        pt.setAlphaf(0.8 if not night else 0.25)
        c.drawImageRect(cs, skia.Rect.MakeWH(cs.width(), cs.height()), skia.Rect.MakeXYWH(x, y, L, L * 0.22), LIN, pt)
    for (col, amp, sc, base, ph) in (("#A9BDB6", 30, 520, hz - 8, 0.0), ("#93AFA5", 34, 380, hz + 10, 2.0)):
        cc = T(col, 0.25)
        pts = []
        xx = -8
        while xx <= W + 8:
            pts.append((xx, PN.ridge_y(xx, base, amp, sc, ph)))
            xx += 8
        c.drawPath(sk.poly_path(pts + [(W + 8, 1100), (-8, 1100)]), skia.Paint(AntiAlias=True, Color=C(cc)))
    # nehir şeridi (ufukta)
    ry0 = hz + 8
    c.drawRect(skia.Rect.MakeLTRB(0, ry0, W, ry0 + 60), skia.Paint(Color=C(T("#8FB0B0", 0.1))))
    for k in range(18):
        yy = ry0 + 6 + (k * 37) % 50
        xx = (k * 190 + t * (8 + k % 4)) % (W + 100) - 50
        c.drawLine(xx, yy, xx + 30, yy, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=C("#FFFFFF", 90)))
    # ── avlu zemini
    zf = skia.Path()
    pts = [P.pt(-COURT_W / 2, 0, WALL_Z0 - 4), P.pt(COURT_W / 2, 0, WALL_Z0 - 4), P.pt(COURT_W / 2, 0, WALL_Z1), P.pt(-COURT_W / 2, 0, WALL_Z1)]
    c.drawPath(sk.poly_path(pts), skia.Paint(AntiAlias=True, Color=C(T("#B8A880", 0.0))))
    for zi in range(0, 28):
        Z = WALL_Z0 + (1.12 ** zi) - 1
        if Z > WALL_Z1:
            break
        a_, b_ = P.pt(-COURT_W / 2, 0, Z), P.pt(COURT_W / 2, 0, Z)
        c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C("#4A3A22", 90)))
    for xi in range(-6, 7):
        a_, b_ = P.pt(xi * COURT_W / 12, 0, WALL_Z0 - 4), P.pt(xi * COURT_W / 12, 0, WALL_Z1)
        c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=0.9, Color=C("#4A3A22", 70)))
    # ── Arno ucundaki revak (derinde, enine)
    _uffizi_end(c, P, T, p, night)
    # ── iki kanat (arkadan öne: uzak başta; sol kanat biraz önce biter)
    lvl_p = [clamp(p * 4.3 - 0.0), clamp(p * 4.3 - 0.55), clamp(p * 4.3 - 1.15), clamp(p * 4.3 - 1.8)]       # sağ kanat
    lvl_l = [clamp(p * 4.7 - 0.0), clamp(p * 4.7 - 0.55), clamp(p * 4.7 - 1.15), clamp(p * 4.7 - 1.8)]       # sol kanat (önde)
    for side, lv in ((1, lvl_p), (-1, lvl_l)):
        _uffizi_wing(c, P, T, side, lv, az, el, night, t)
    # ── iskele/vinç/işçi/toz — avlu içinde
    _uffizi_site(f, P, T, p, t, lvl_p, lvl_l, night)
    return P


def _uffizi_end(c, P, T, p, night):
    Z = WALL_Z1
    xl, yl = P.pt(-COURT_W / 2, 0, Z)
    xr, yr = P.pt(COURT_W / 2, 0, Z)
    # uç revak: üç kemerli (Serliana benzeri) — geçide açılan koyu boşluk + nehir
    ytop = P.pt(0, 11.0, Z)[1]
    c.drawRect(skia.Rect.MakeLTRB(xl, ytop, xr, yl), skia.Paint(Color=C(T("#D8C8A0", 0.2))))
    c.drawRect(skia.Rect.MakeLTRB(xl, ytop, xr, yl), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 150)))
    n = 3
    for i in range(n):
        x0 = xl + (xr - xl) * (i + 0.15) / n
        x1 = xl + (xr - xl) * (i + 0.85) / n
        path = skia.Path()
        path.moveTo(x0, yl)
        path.lineTo(x0, ytop + (yl - ytop) * 0.40)
        path.arcTo(skia.Rect.MakeLTRB(x0, ytop + (yl - ytop) * 0.40 - (x1 - x0) / 2, x1, ytop + (yl - ytop) * 0.40 + (x1 - x0) / 2), 180, 180, False)
        path.lineTo(x1, yl)
        path.close()
        c.drawPath(path, skia.Paint(AntiAlias=True, Color=C(T("#9CB8C0", 0.3))))
        c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 160)))


def _uffizi_wing(c, P, T, side, lv, az, el, night, t):
    """Kanat cephesi (perspektif): her seviye için kısmi yükseklik; ara katlarda kemer/pencere, çatıda revak."""
    Xw = side * COURT_W / 2
    shade = 0.78 + 0.28 * (math.cos((90 + side * 90 - az) * D2R) * 0.5 + 0.5) * (0.5 + 0.6 * el)
    wall = brick_col(T("#E1D2AA", 0.1), shade)
    wall_d = brick_col(T("#C9B88C", 0.1), shade)
    # z dilimleri (bay)
    nb = int((WALL_Z1 - WALL_Z0) / BAY)
    bays = [(WALL_Z0 + i * BAY, WALL_Z0 + (i + 1) * BAY) for i in range(nb)]
    # arkadan öne çiz
    for (z0, z1) in reversed(bays):
        for li, (y0, y1, name) in enumerate(LEVELS):
            prog = lv[li]
            if prog <= 0.001:
                continue
            ytop = y0 + (y1 - y0) * prog
            q = [P.pt(Xw, y0, z0), P.pt(Xw, y0, z1), P.pt(Xw, ytop, z1), P.pt(Xw, ytop, z0)]
            c.drawPath(sk.poly_path(q), skia.Paint(AntiAlias=True, Color=C(wall if (li % 2 == 0) else wall_d)))
            # bay çizgileri
            c.drawLine(q[0][0], q[0][1], q[3][0], q[3][1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 110)))
            # açıklıklar (yalnızca tamamlanmış kısım)
            if prog >= 0.98:
                zc0, zc1 = z0 + BAY * 0.22, z0 + BAY * 0.78
                if name == "portico":
                    ya, yb = y0, y1 - 1.4
                    o = [P.pt(Xw, ya, zc0), P.pt(Xw, ya, zc1), P.pt(Xw, yb, zc1), P.pt(Xw, yb, zc0)]
                    ap = skia.Path()
                    ap.moveTo(*o[0]); ap.lineTo(*o[3])
                    mid_top = ((o[3][0] + o[2][0]) / 2, (o[3][1] + o[2][1]) / 2 - (abs(o[2][0] - o[3][0]) * 0.5))
                    ap.quadTo(o[3][0], mid_top[1], mid_top[0], mid_top[1])
                    ap.quadTo(o[2][0], mid_top[1], o[2][0], o[2][1]); ap.lineTo(*o[1]); ap.close()
                    c.drawPath(ap, skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", 0.0), 235)))
                    c.drawPath(ap, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 170)))
                elif name == "nobile":
                    ya, yb = y0 + 1.6, y1 - 1.5
                    o = [P.pt(Xw, ya, zc0 + BAY * 0.08), P.pt(Xw, ya, zc1 - BAY * 0.08), P.pt(Xw, yb, zc1 - BAY * 0.08), P.pt(Xw, yb, zc0 + BAY * 0.08)]
                    c.drawPath(sk.poly_path(o), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", 0.0), 225)))
                    c.drawPath(sk.poly_path(o), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 170)))
                    ped = [P.pt(Xw, yb, zc0 + BAY * 0.02), P.pt(Xw, yb, zc1 - BAY * 0.02), P.pt(Xw, yb + 0.7, (zc0 + zc1) / 2)]
                    c.drawPath(sk.poly_path(ped), skia.Paint(AntiAlias=True, Color=C(T("#EDE4CC", 0.0))))
                    c.drawPath(sk.poly_path(ped), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 150)))
                elif name == "mezz":
                    ya, yb = y0 + 0.8, y1 - 0.8
                    o = [P.pt(Xw, ya, z0 + BAY * 0.35), P.pt(Xw, ya, z0 + BAY * 0.65), P.pt(Xw, yb, z0 + BAY * 0.65), P.pt(Xw, yb, z0 + BAY * 0.35)]
                    c.drawPath(sk.poly_path(o), skia.Paint(AntiAlias=True, Color=C(T("#3A2A1C", 0.0), 225)))
                else:   # çatı revağı
                    ya, yb = y0 + 0.6, y1 - 1.0
                    o = [P.pt(Xw, ya, zc0), P.pt(Xw, ya, zc1), P.pt(Xw, yb, zc1), P.pt(Xw, yb, zc0)]
                    c.drawPath(sk.poly_path(o), skia.Paint(AntiAlias=True, Color=C(T("#4A3626", 0.0), 235)))
    # silmeler (katlar arası çizgi) ve çatı
    for li, (y0, y1, name) in enumerate(LEVELS):
        prog = lv[li]
        if prog <= 0.001:
            continue
        ytop = y0 + (y1 - y0) * prog
        a_ = P.pt(Xw, ytop, WALL_Z0)
        b_ = P.pt(Xw, ytop, WALL_Z1)
        c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=C(INK, 180)))
    if lv[3] > 0.98:
        # çatı saçağı + kiremit
        a_ = P.pt(Xw, 24.0, WALL_Z0)
        b_ = P.pt(Xw, 24.0, WALL_Z1)
        a2 = P.pt(Xw - side * 1.6, 24.8, WALL_Z0)
        b2 = P.pt(Xw - side * 1.6, 24.8, WALL_Z1)
        c.drawPath(sk.poly_path([a_, b_, b2, a2]), skia.Paint(AntiAlias=True, Color=C(T("#B4552E", 0.0))))


def _uffizi_site(f, P, T, p, t, lvl_r, lvl_l, night):
    c = f.c
    wood = T("#7A5230", 0.0)
    dark = "#3A2410"
    # iskele: sağ kanatta yapım seviyesine kadar dikmeler; sol kanatta kısa
    for side, lv in ((1, lvl_r), (-1, lvl_l)):
        cur = 0
        for li in range(4):
            if 0.001 < lv[li] < 0.98:
                cur = li
        done_top = LEVELS[cur][0] + (LEVELS[cur][1] - LEVELS[cur][0]) * lv[cur]
        if all(v >= 0.98 for v in lv):
            continue
        Xw = side * (COURT_W / 2 - 0.6)
        for zi in range(0, 9):
            Z = WALL_Z0 + 2 + zi * 9.5
            x0, y0 = P.pt(Xw, 0, Z)
            x1, y1 = P.pt(Xw, done_top + 3.0, Z)
            c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.6, 70.0 / Z * 0.5), Color=C(dark, 220), StrokeCap=skia.Paint.kRound_Cap))
            c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.0, 70.0 / Z * 0.3), Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
        for ylev in (3.0, 7.0, 11.0, 15.0, 19.0):
            if ylev > done_top + 3.5:
                break
            a_ = P.pt(Xw, ylev, WALL_Z0 + 2)
            b_ = P.pt(Xw, ylev, WALL_Z0 + 2 + 8 * 9.5)
            c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3.2, Color=C(dark, 230)))
            c.drawLine(a_[0], a_[1], b_[0], b_[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C(wood)))
        # işçiler: üst platformda
        for k in range(6):
            Z = WALL_Z0 + 6 + k * 13.0 + 3 * math.sin(k + side)
            x, y = P.pt(Xw + side * -0.9, done_top + 3.0, Z)
            hh = max(14.0, 520.0 / Z)
            FA.actor(f, ["halk", "tuccar", "denizci", "halk", "cocuk", "halk"][k], x, y, hh, t + k * 0.6, action="talk" if k % 2 else "idle", dir=1 if (k + side) % 2 == 0 else -1, seed=80 + k + side * 5, phase=k * 0.2, energy=0.5)
    # taş yığınları ve arabalar (avlu zemini)
    rs = np.random.RandomState(12)
    for i in range(7):
        Z = WALL_Z0 + 3 + i * 14 + rs.uniform(0, 6)
        X = rs.uniform(-4.0, 4.0)
        x, y = P.pt(X, 0, Z)
        s = 230.0 / Z
        for q in range(4):
            c.drawRect(skia.Rect.MakeLTRB(x - s * 1.4 + q * s * 0.2, y - s * (0.7 + 0.3 * q), x + s * 1.4 - q * s * 0.2, y - s * (0.3 * q)), skia.Paint(AntiAlias=True, Color=C(T(["#B8A47A", "#A8946A", "#C9B88C"][q % 3], 0.0))))
        c.drawRect(skia.Rect.MakeLTRB(x - s * 1.4, y - s * 1.0, x + s * 1.4, y), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, Color=C(INK, 140)))
    # avluda yürüyen taşıyıcılar
    for i in range(4):
        u = (t * 0.02 + i * 0.27) % 1.0
        Z = WALL_Z0 + 6 + u * 90
        X = (-3.2 if i % 2 else 3.0) + 0.6 * math.sin(i + t * 0.3)
        x, y = P.pt(X, 0, Z)
        hh = max(16.0, 640.0 / Z)
        FA.walker(f, "halk", x, y, hh, t, speed=hh * 0.28, dir=-1 if i % 2 else 1, seed=90 + i, phase=i * 0.3, prop="sack" if i % 2 == 0 else "basket")
    # vinç (sağ ön): direk + bom + yük
    cx_, cy_ = P.pt(4.8, 0, 22)
    s = 520.0 / 22
    mast_top = (cx_, cy_ - 15 * s * 0.55)
    c.drawLine(cx_, cy_, mast_top[0], mast_top[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=C(dark), StrokeCap=skia.Paint.kRound_Cap))
    c.drawLine(cx_, cy_, mast_top[0], mast_top[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C(wood), StrokeCap=skia.Paint.kRound_Cap))
    bom_e = (mast_top[0] - 120, mast_top[1] + 20)
    c.drawLine(mast_top[0], mast_top[1], bom_e[0], bom_e[1], skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C(dark), StrokeCap=skia.Paint.kRound_Cap))
    cyc = 8.0
    ph = (t % cyc) / cyc
    up = smooth(ph / 0.5) if ph < 0.5 else 1 - smooth((ph - 0.58) / 0.42)
    ly = lerp_(cy_ - 10, bom_e[1] + 50, up)
    c.drawLine(bom_e[0], bom_e[1], bom_e[0] + 2 * math.sin(t * 1.2) * up, ly, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.8, Color=C("#6A5A3A", 235)))
    c.drawRect(skia.Rect.MakeLTRB(bom_e[0] - 16, ly, bom_e[0] + 16, ly + 22), skia.Paint(AntiAlias=True, Color=C("#B8A47A")))
    c.drawRect(skia.Rect.MakeLTRB(bom_e[0] - 16, ly, bom_e[0] + 16, ly + 22), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C(INK, 200)))
    # toz bulutları (yapım katında)
    for side, lv in ((1, lvl_r), (-1, lvl_l)):
        if all(v >= 0.98 for v in lv):
            continue
        cur = max(li for li in range(4) if lv[li] > 0.001) if any(v > 0.001 for v in lv) else 0
        topy = LEVELS[cur][0] + (LEVELS[cur][1] - LEVELS[cur][0]) * lv[cur]
        for q in range(5):
            ph2 = (t * 0.2 + q / 5.0 + side * 0.13) % 1.0
            Z = WALL_Z0 + 10 + q * 17
            x, y = P.pt(side * (COURT_W / 2 - 2.0 + 3 * ph2), topy + 1 + ph2 * 3, Z)
            FA._puff(c, x, y, 6 + 26 * ph2 * (260.0 / Z) * 0.6 / 3, 0.22 * (1 - ph2), "#D8C8A8")


# ═════════════════════════════ çekim türü ═════════════════════════════
_SCENES = {}


@ckind("build")
def k_build(cx, build="dome", p=None, orbit=10.0, tod=None, kick=None, caption=None, at=0.0, seed=3, frame=True, **_):
    """Zaman atlamalı yapım. build: dome | uffizi. p=(çapa_başlangıç, çapa_bitiş): ilerleme 0→1 (ease_io); p=None → tüm çekim; p tek sayıysa sabit ilerleme.
    orbit: kamera yörüngesi (≤12°, kubbede). tod: day | night. Gün ışığı (güneş yayı, gökyüzü rengi, yüz parlaklığı) ilerlemeyle akar; toz/duman/kuş/vinç çalışır.
    cam/link/longtake/montage kabul edilir ve yok sayılır."""
    f = cx.f
    c = f.c
    night_theme = not TH.day
    tod = tod or ("night" if night_theme else "day")
    dur = max(cx.dur, 1e-3)
    if p is None:
        ta, tb = 0.0, dur
    elif isinstance(p, (int, float)):
        ta, tb = 0.0, 1e9
    else:
        try:
            ta, tb = cx.at(p[0]), cx.at(p[1])
        except Exception:
            ta, tb = float(p[0]), float(p[1])
    if isinstance(p, (int, float)):
        pr = float(p)
    else:
        pr = ease_io(clamp((cx.t - ta) / max(1e-6, tb - ta)))
    band = (150, 800) if frame else (140, 800)
    a_ = cx.amt(at, 0.9) if at else 1.0
    cam = CM.Cam(cx, push=0.0, drift=(0.0, 0.0))
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, 0, W, band[0] + 2))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, band[0] + band[1] - 2, W, H))
    CM.bgfill(f, cx, seed=seed, cam=cam, dress=None)
    c.restore()
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(0, band[0], W, band[0] + band[1]))
    c.translate(0, band[0] - 70)
    key = (build, tod, seed)
    if build == "dome":
        sc = _SCENES.get(key)
        if sc is None:
            sc = _SCENES[key] = DomeScene(tod, seed)
        a_orbit = (clamp(cx.t / dur) - 0.5) * 2.0 * min(12.0, abs(orbit)) * 0.5
        draw_dome(f, cx, pr, cx.t, tod, sc, a_orbit)
    else:
        draw_uffizi(f, cx, pr, cx.t, tod, seed)
    c.restore()
    if frame:
        for yy in (band[0] - 40, band[0] + band[1]):
            FA.vine_band(f, yy, a_)
            c.drawLine(-40, yy + (40 if yy < band[0] else 0), W + 40, yy + (40 if yy < band[0] else 0), f.paint(TH.gold, style="stroke", sw=2.6, alpha=0.9 * a_))
    if kick:
        CM.kick(f, kick, W / 2, 104, alpha=cx.amt(at + 0.4, 0.8), size=34, track=14)
    if caption:
        wd = sk.text_width(caption, "cap_i", 44) + 100
        cyy = band[0] + band[1] - 70
        CM.tablet(f, W / 2 - wd / 2, cyy - 36, wd, 76, alpha=cx.amt(at + 0.8, 0.7), corner=10)
        CM.ink(f, caption, W / 2, cyy + 14, face="cap_i", size=44, color=TH.fg, align="c", alpha=cx.amt(at + 0.8, 0.7), emboss=False)
    # gün batımına doğru sıcak örtü (ışık sıcaklığı hikâye bilgisi); gece: mum havuzu
    sunA = 0.0
    if tod == "night":
        CM.finish(f, cx, motes_n=18, light=CM.candle_light(cx.t, seed, base=(W * 0.5, H * 0.46), r=1500.0, sway=10.0))
    else:
        warm = smooth((pr - 0.78) / 0.22) * 0.20 + smooth((0.18 - pr) / 0.18) * 0.12
        if warm > 0:
            c.drawRect(skia.Rect.MakeLTRB(0, band[0], W, band[0] + band[1]), skia.Paint(Color=C("#FF9A4A", int(255 * warm)), BlendMode=skia.BlendMode.kSoftLight))
        CM.finish(f, cx, motes_n=22)
