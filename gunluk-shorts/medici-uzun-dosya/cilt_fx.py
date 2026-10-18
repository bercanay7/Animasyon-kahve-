"""cilt_fx — Medici cildi: geçişler (pigment yıkaması / defter sayfası çevirme / giornata açılımı), giornata yama yardımcıları, HUD.

Geçiş API'si (compose.Program._blend çağırır):  blend(kind, a, b, k, g) → Frame   kind ∈ {'yikama','sayfa','giornata'}
HUD: hud(f, g, year_state, perde, bar)  — sağ üst 420×110 alanında yıl rulosu + ince perde göstergesi; bölüm adı sol üstte (ilk 5,5 sn).
"""
import functools
import math

import cv2
import numpy as np
import skia

import cilt_medici as CM
import cilt_wall as CW
import sk
from sk import C, Frame, H, W, clamp, ease_io, mix, smooth

PIG = CM.PIG


# ───────────────────────────── giornata yamaları ─────────────────────────────
@functools.lru_cache(maxsize=12)
def giornata_paths(seed, w=W, h=H):
    """(paths: [skia.Path], order: [0..1 sıra oranı]) — ekran uzayında yamalar; sıra: sol-üst → sağ-alt, hafif karışık."""
    polys, seams = CW.giornate_polys(seed, w, h, band=(150, 260), cell=(300, 620))
    rs = np.random.RandomState(seed + 5)
    paths, keys = [], []
    for p in polys:
        pa = skia.Path()
        pa.addPoly([(float(x), float(y)) for x, y in p], True)
        paths.append(pa)
        cx, cy = float(p[:, 0].mean()), float(p[:, 1].mean())
        keys.append(cy / h * 0.62 + cx / w * 0.30 + rs.rand() * 0.22)
    order = np.argsort(np.argsort(keys)) / max(1, len(keys) - 1)
    return paths, [float(o) for o in order]


def giornata_reveal(c, paths, order, k, draw_fn, span=0.72, soft=0.30, seam=True, wet=0.20):
    """k (0..1) ilerlemesinde yamaları sırayla açar. draw_fn(alpha): görüntüyü (kırpılmış tuvale) alfa ile çizer.
    Her yamada: ıslak sıva koyulaşması + dikiş çizgisi (açılırken parlar, sonra söner)."""
    n = len(paths)
    for pth, o in zip(paths, order):
        a = smooth((k - o * span) / soft)
        if a <= 0:
            continue
        c.save()
        c.clipPath(pth, skia.ClipOp.kIntersect, True)
        draw_fn(a)
        e = 4 * a * (1 - a)
        if wet > 0 and e > 0.01:
            c.drawPaint(skia.Paint(Color=C("#3A2A14", int(255 * wet * e))))
        c.restore()
        if seam:
            e = 0.25 + 0.75 * 4 * a * (1 - a)
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, Color=C("#2A1C0E", int(150 * e * min(1.0, a * 3))))
            c.drawPath(pth, p)
            p2 = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.2, Color=C("#FFF4D6", int(130 * e * min(1.0, a * 3))))
            c.save(); c.translate(1.6, 1.6)
            c.drawPath(pth, p2)
            c.restore()


# ───────────────────────────── geçişler ─────────────────────────────
@functools.lru_cache(maxsize=4)
def _wash_field(seed=3):
    """Yıkama cephesi alanı R(x,y) ∈ [0,1] (480×270): çapraz gradyan + sıvı lekeli gürültü."""
    w, h = 480, 270
    rs = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    diag = (xx / w * 0.78 + yy / h * 0.22)
    n = CW.lf(rs, h, w, 52) * 0.55 + CW.lf(rs, h, w, 16) * 0.25 + CW.lf(rs, h, w, 120) * 0.45
    n = (n - n.min()) / (n.max() - n.min())
    R = diag * 0.60 + n * 0.40
    return (R - R.min()) / (R.max() - R.min())


def _alpha_img(m):
    """float 0..1 (h,w) → skia.Image (beyaz, alfa = m)."""
    a = np.clip(m * 255, 0, 255).astype(np.uint8)
    arr = np.dstack([np.full_like(a, 255)] * 3 + [a])
    return sk.np_to_image(arr)


def blend_wash(a, b, k, g=0.0):
    """Pigment yıkaması (suluboya silme): yeni görüntü ıslak, sızan bir cepheyle açılır; cephe kenarında koyu pigment halkası."""
    kk = smooth(k)
    R = _wash_field(3)
    th = kk * 1.28 - 0.16
    wsoft = 0.12
    m = np.clip((th - R) / wsoft, 0, 1).astype(np.float32)
    m = m * m * (3 - 2 * m)
    edge = (4 * m * (1 - m)).astype(np.float32)
    out = Frame()
    out.c.drawImage(a.surf.makeImageSnapshot(), 0, 0)
    dst = skia.Rect.MakeWH(W, H)
    src_r = skia.Rect.MakeWH(480, 270)
    out.c.saveLayer(None, None)
    out.c.drawImage(b.surf.makeImageSnapshot(), 0, 0)
    out.c.drawImageRect(_alpha_img(m), src_r, dst, CM._LIN, skia.Paint(BlendMode=skia.BlendMode.kDstIn))
    out.c.restore()
    # pigment halkası: ocre-umber kenar (çarpma) + hafif lapis sızıntısı
    ring = skia.Paint(BlendMode=skia.BlendMode.kMultiply, ColorFilter=skia.ColorFilters.Blend(C("#8A6A3C"), skia.BlendMode.kSrcIn))
    out.c.drawImageRect(_alpha_img(edge * 0.55), src_r, dst, CM._LIN, ring)
    return out


def blend_page(a, b, k, g=0.0):
    """Defter sayfası çevirme: sayfa sağ kenardan kalkıp sola katlanır (hafif eğik kıvrım, silindirik gölge); altta yeni çekim."""
    kk = ease_io(clamp(k), 2.4)
    th = math.radians(5.5)
    xf = W * (1.04 - 1.10 * kk)            # kıvrım merkezi (ekran x)
    P = (xf, H * 0.5)
    BIG = 4000
    out = Frame()
    c = out.c
    imgA = a.surf.makeImageSnapshot()
    c.drawImage(b.surf.makeImageSnapshot(), 0, 0)
    # B üzerine kıvrımın sağında gölge (yerel koordinat: u sağa)
    c.save(); c.translate(*P); c.rotate(math.degrees(th))
    sh = skia.GradientShader.MakeLinear([(0, 0), (190, 0)], [C("#1A1208", 150), C("#1A1208", 0)], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(0, -BIG, 260, BIG), skia.Paint(Shader=sh))
    c.restore()
    # düz kalan kısım (u<0)
    c.save()
    c.translate(*P); c.rotate(math.degrees(th))
    c.clipRect(skia.Rect.MakeLTRB(-BIG, -BIG, 0, BIG))
    c.rotate(-math.degrees(th)); c.translate(-P[0], -P[1])
    c.drawImage(imgA, 0, 0)
    c.restore()
    # düz kısımda kıvrım yakınında silindir aydınlığı + kıvrılan sayfanın gölgesi
    c.save(); c.translate(*P); c.rotate(math.degrees(th))
    L = max(30.0, min(520.0, W * 0.5 * (1.1 * kk + 0.02)))
    sh2 = skia.GradientShader.MakeLinear([(-L * 0.9, 0), (0, 0)], [C("#1A1208", 0), C("#1A1208", int(120 * clamp(kk * 3)))], [0, 1])
    c.drawRect(skia.Rect.MakeLTRB(-L * 0.9, -BIG, 0, BIG), skia.Paint(Shader=sh2))
    c.restore()
    # katlanan sayfa: sağ bölge, ayna dönüşü; ters yüz = krem kâğıt + silik hayalet
    c.save()
    c.translate(*P); c.rotate(math.degrees(th)); c.scale(-1, 1)
    c.clipRect(skia.Rect.MakeLTRB(-BIG, -BIG, 0, BIG))
    c.rotate(-math.degrees(th)); c.translate(-P[0], -P[1])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=C("#E9DFC2")))
    pg = skia.Paint(); pg.setAlphaf(0.16)
    c.drawImage(imgA, 0, 0, skia.SamplingOptions(), pg)
    c.restore()
    # katlanan sayfada silindirik shading (kıvrımda parlak, uzaklaştıkça koyu) + kenar çizgisi
    c.save(); c.translate(*P); c.rotate(math.degrees(th))
    Lw = min(W * 1.1 * kk + 4, 1900)
    sh3 = skia.GradientShader.MakeLinear([(-Lw, 0), (-Lw * 0.82, 0), (-Lw * 0.10, 0), (0, 0)],
                                         [C("#2A1C0C", 150), C("#2A1C0C", 40), C("#FFF8E0", 70), C("#6A5030", 160)], [0.0, 0.16, 0.86, 1.0])
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-Lw, -BIG, 0, BIG))
    c.drawRect(skia.Rect.MakeLTRB(-Lw, -BIG, 0, BIG), skia.Paint(Shader=sh3))
    c.restore()
    c.drawLine(0, -BIG, 0, BIG, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C("#3A2A18", 150)))
    c.restore()
    return out


def blend_giornata(a, b, k, g=0.0, seed=7):
    """Giornata açılımı: yeni çekim, freskin günlük sıva yamaları gibi sırayla açılır (ıslak koyulaşma + dikiş çizgisi)."""
    paths, order = giornata_paths(seed)
    out = Frame()
    c = out.c
    c.drawImage(a.surf.makeImageSnapshot(), 0, 0)
    imgB = b.surf.makeImageSnapshot()

    def dr(al):
        p = skia.Paint()
        p.setAlphaf(clamp(al))
        c.drawImage(imgB, 0, 0, skia.SamplingOptions(), p)
    giornata_reveal(c, paths, order, smooth(k), dr, span=0.70, soft=0.30)
    return out


TR = dict(yikama=blend_wash, sayfa=blend_page, giornata=blend_giornata)


def blend(kind, a, b, k, g=0.0):
    return TR[kind](a, b, k, g)


# ───────────────────────────── HUD ─────────────────────────────
PERDE_NAMES = {1: "PARA", 2: "GÜZELLİK", 3: "MİRAS"}
ROMAN = {1: "I", 2: "II", 3: "III"}


class YearState:
    """HUD yıl durumu: entries=[(t_global, yıl)] artan; roll_dur: yıl değişiminde rulo süresi."""

    def __init__(self, entries, roll_dur=0.95):
        self.e = sorted(entries)
        self.roll = roll_dur

    def at(self, g):
        """→ (cur, prev, p): p=1 rulo bitmiş; p<1 prev→cur yuvarlanıyor."""
        cur, prev, t0 = None, None, -1e9
        for t, y in self.e:
            if t <= g + 1e-9:
                prev, cur, t0 = cur, y, t
            else:
                break
        if cur is None:
            return (self.e[0][1] if self.e else 1397), None, 1.0
        if prev is None or prev == cur:
            return cur, None, 1.0
        return cur, prev, clamp((g - t0) / self.roll)


def _digit_roll(f, x, base_y, ch_old, ch_new, p, size, color, cw, clip_rect=None):
    """Tek hane: eski üstten çıkar, yeni alttan girer (yumuşak)."""
    e = ease_io(p, 3)
    dy = size * 0.95
    if ch_old is not None and e < 1:
        CM.ink(f, ch_old, x, base_y - dy * e, face="title", size=size, color=color, align="c", alpha=(1 - e) ** 1.2, emboss=False)
    CM.ink(f, ch_new, x, base_y + dy * (1 - e), face="title", size=size, color=color, align="c", alpha=min(1.0, e * 1.6 + (1.0 if ch_old is None else 0.0)), emboss=False)


def hud(f, g, ys, perde, mode="day"):
    """Sağ üst: lapis tabletli yıl rulosu + I/II/III perde göstergesi. Alan: x∈[1500,1920], y∈[0,110]."""
    cur, prev, p = ys.at(g)
    x0, y0, w, h = 1498, 20, 382, 82
    c = f.c
    # tablet (her modda lapis: kontrast sabit)
    f.rrect(x0 + 4, y0 + 7, w, h, 12, color="#000000", alpha=0.42, blur=8)
    f.rrect(x0, y0, w, h, 12, shader=f.lin(x0, y0, x0, y0 + h, [("#1E3282", 0.0), ("#0F1B52", 1.0)]), alpha=0.97)
    f.rrect(x0, y0, w, h, 12, style="stroke", sw=2.2, color="#D8B25A", alpha=0.95)
    f.rrect(x0 + 6, y0 + 6, w - 12, h - 12, 8, style="stroke", sw=1.0, color="#D8B25A", alpha=0.55)
    # perde göstergesi (sol bölme)
    px = x0 + 22
    for i in (1, 2, 3):
        s = ROMAN[i]
        on = i == perde
        wd = sk.text_width(s, "title_m", 28, 2)
        col = "#F4D98A" if on else "#8E9FD2"
        CM.ink(f, s, px + wd / 2, y0 + 49, face="title_m", size=28, color=col, align="c", track=2, alpha=1.0 if on else 0.9, emboss=False)
        if on:
            f.rect(px - 2, y0 + 58, wd + 4, 2.5, color="#F4D98A", alpha=0.95)
        px += wd + 14
    # ayırıcı
    f.line(x0 + 128, y0 + 16, x0 + 128, y0 + h - 16, color="#D8B25A", sw=1.4, alpha=0.6)
    # yıl (rulo)
    s_new = str(cur)
    s_old = str(prev) if prev is not None else None
    size = 56
    cw = sk.text_width("0", "title", size, 0) + 3
    cxr = x0 + 128 + (w - 128) / 2
    xs = cxr - cw * len(s_new) / 2 + cw / 2
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(x0 + 134, y0 + 6, x0 + w - 8, y0 + h - 6))
    for i, chn in enumerate(s_new):
        cho = s_old[i] if (s_old is not None and i < len(s_old)) else None
        changed = cho is not None and cho != chn and p < 1
        if changed:
            # her hane biraz farklı gecikmeyle
            pp = clamp((p * (1.0 + 0.35 * (len(s_new) - 1 - i) / max(1, len(s_new) - 1))) - 0.1 * (len(s_new) - 1 - i))
            _digit_roll(f, xs + i * cw, y0 + 61, cho, chn, clamp(pp), size, "#F6DD92", cw)
        else:
            CM.ink(f, chn, xs + i * cw, y0 + 61, face="title", size=size, color="#F6DD92", align="c", emboss=False)
    c.restore()


def chapter_tag(f, text, a=1.0):
    """Sol üst bölüm adı (lapis levha). text hazır: 'IV · KUBBE VE KEFARET'."""
    if a <= 0:
        return
    sz = 30
    wd = min(780, sk.text_width(text, "title_m", sz, 5) + 52)
    x, y = 60, 28
    f.rrect(x + 3, y + 6, wd, 54, 10, color="#000000", alpha=0.40 * a, blur=7)
    f.rrect(x, y, wd, 54, 10, shader=f.lin(x, y, x, y + 54, [("#1E3282", 0.0), ("#0F1B52", 1.0)]), alpha=0.96 * a)
    f.rrect(x, y, wd, 54, 10, style="stroke", sw=1.8, color="#D8B25A", alpha=0.9 * a)
    CM.ink(f, text, x + 26, y + 37, face="title_m", size=sz, color="#F1E1AE", align="l", track=5, alpha=a, emboss=False)


def progress_line(f, prog, marks=()):
    """Alt kenarda çok ince ilerleme çizgisi (altyazı bölgesini işgal etmez: 5 px)."""
    f.rect(0, H - 5, W, 5, color="#000000", alpha=0.40)
    f.rect(0, H - 4, W * prog, 3, color="#D8B25A", alpha=0.9)
    for m in marks:
        f.rect(m * W - 1, H - 7, 2, 7, color="#F4DD92", alpha=0.7)
