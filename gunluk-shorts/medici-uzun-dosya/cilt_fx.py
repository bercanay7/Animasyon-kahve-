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
from sk import C, Frame, H, W, clamp, ease_in, ease_io, ease_out, lerp, mix, smooth

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


def giornata_reveal(c, paths, order, k, draw_fn, span=0.72, soft=0.30, seam=True, wet=0.20, sweep=False):
    """k (0..1) ilerlemesinde yamaları sırayla açar. draw_fn(alpha): görüntüyü (kırpılmış tuvale) alfa ile çizer.
    sweep=True: her yama mala darbesi gibi soldan sağa (yumuşak kenarlı) açılır — hayalet/çapraz-solma yok.
    Her yamada: ıslak sıva koyulaşması (yeni açılan, sonra söner) + dikiş çizgisi."""
    for pth, o in zip(paths, order):
        a = smooth((k - o * span) / soft)
        if a <= 0:
            continue
        c.save()
        c.clipPath(pth, skia.ClipOp.kIntersect, True)
        if sweep:
            b = pth.getBounds()
            x_edge = b.left() - 30 + (b.width() + 60) * a
            # üç kademeli yumuşak kenar
            for j, (off, al) in enumerate(((0, 1.0), (14, 0.66), (28, 0.33))):
                c.save()
                c.clipRect(skia.Rect.MakeLTRB(b.left() - 40, b.top() - 4, x_edge - off, b.bottom() + 4))
                draw_fn(1.0 if j == 0 else 1.0)
                c.restore()
                if j == 0:
                    pass
            # ıslak koyulaşma: yalnız kenarın hemen gerisinde
            wl = wet * 4 * a * (1 - a)
            if wl > 0.004:
                sh = skia.GradientShader.MakeLinear([(x_edge - 160, 0), (x_edge, 0)], [C("#3A2A14", 0), C("#3A2A14", int(255 * wl))], [0, 1])
                c.drawRect(skia.Rect.MakeLTRB(b.left() - 40, b.top(), x_edge, b.bottom()), skia.Paint(Shader=sh))
        else:
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
    n = CW.lf(rs, h, w, 120) * 0.60 + CW.lf(rs, h, w, 46) * 0.30 + CW.lf(rs, h, w, 200) * 0.40
    n = (n - n.min()) / (n.max() - n.min())
    R = diag * 0.55 + n * 0.45
    return (R - R.min()) / (R.max() - R.min())


def _alpha_img(m):
    """float 0..1 (h,w) → skia.Image (beyaz, alfa = m)."""
    a = np.clip(m * 255, 0, 255).astype(np.uint8)
    arr = np.dstack([np.full_like(a, 255)] * 3 + [a])
    return sk.np_to_image(arr)


def blend_wash_skia(a, b, k, g=0.0, **_):
    """(Referans, yavaş ~360 ms) Pigment yıkaması — skia ölçekli kDstIn/kMultiply çizimleriyle. blend_wash ile aynı görüntüyü üretir; yalnız eşdeğerlik denetimi için tutulur."""
    kk = smooth(k)
    R = _wash_field(3)
    th = kk * 1.34 - 0.20
    wsoft = 0.20
    m = np.clip((th - R) / wsoft, 0, 1).astype(np.float32)
    m = m * m * (3 - 2 * m)
    glaze = (4 * m * (1 - m)).astype(np.float32)                       # cephe ortası = 1
    ring = np.exp(-((th - R - 0.015) / 0.018) ** 2).astype(np.float32)  # ince uç halkası
    out = Frame()
    out.c.drawImage(a.surf.makeImageSnapshot(), 0, 0)
    dst = skia.Rect.MakeWH(W, H)
    src_r = skia.Rect.MakeWH(480, 270)
    out.c.saveLayer(None, None)
    out.c.drawImage(b.surf.makeImageSnapshot(), 0, 0)
    out.c.drawImageRect(_alpha_img(m), src_r, dst, CM._LIN, skia.Paint(BlendMode=skia.BlendMode.kDstIn))
    out.c.restore()
    # sulu cam: çarpma ile ılık pigment (ocre) + hafif lapis kayması
    gl = skia.Paint(BlendMode=skia.BlendMode.kMultiply, ColorFilter=skia.ColorFilters.Blend(C("#C8A86A"), skia.BlendMode.kSrcIn))
    out.c.drawImageRect(_alpha_img(glaze * 0.55), src_r, dst, CM._LIN, gl)
    gl2 = skia.Paint(BlendMode=skia.BlendMode.kMultiply, ColorFilter=skia.ColorFilters.Blend(C("#5A6FA8"), skia.BlendMode.kSrcIn))
    out.c.drawImageRect(_alpha_img(np.roll(glaze, 6, 1) * 0.16), src_r, dst, CM._LIN, gl2)
    rg = skia.Paint(BlendMode=skia.BlendMode.kMultiply, ColorFilter=skia.ColorFilters.Blend(C("#7A5A30"), skia.BlendMode.kSrcIn))
    out.c.drawImageRect(_alpha_img(ring * 0.40), src_r, dst, CM._LIN, rg)
    return out




def blend_wash(a, b, k, g=0.0, **_):
    """Pigment yıkaması (suluboya silme): yeni görüntü ıslak, geniş yumuşak bir cepheyle açılır; cephede sulu pigment camı (ocre/lapis),
    en uçta birikmiş ince koyu halka (kahve-halkası etkisi). Görünüm değişmedi; hesap numpy/cv2'ye taşındı (360 ms → ~60 ms): maskeler 480×270'te hesaplanır,
    kDstIn karışımı = A + (B−A)·m, kMultiply camları = çarpım katsayısı 1 − α(1 − renk) (hepsi tek katsayı alanında), tam çözünürlüğe cv2 ile büyütülür."""
    kk = smooth(k)
    R = _wash_field(3)
    th = kk * 1.34 - 0.20
    wsoft = 0.20
    m = np.clip((th - R) / wsoft, 0, 1).astype(np.float32)
    m = m * m * (3 - 2 * m)
    glaze = (4 * m * (1 - m)).astype(np.float32)                       # cephe ortası = 1
    ring = np.exp(-((th - R - 0.015) / 0.018) ** 2).astype(np.float32)  # ince uç halkası
    # çarpım camları: ocre (0.55), lapis kayması (0.16, yatay 6 piksel), halka (0.40) → tek katsayı alanı (BGRA, uint8; alfa kanalı 255)
    fac = np.ones((R.shape[0], R.shape[1], 3), np.float32)
    for alpha_map, col in ((glaze * 0.55, "#C8A86A"), (np.roll(glaze, 6, 1) * 0.16, "#5A6FA8"), (ring * 0.40, "#7A5A30")):
        rr_, gg_, bb_ = sk.rgb(col)
        c_ = np.array([bb_, gg_, rr_], np.float32) / 255.0          # BGR sırası
        fac *= 1.0 - np.clip(alpha_map, 0, 1)[..., None] * (1.0 - c_)[None, None, :]
    fac8 = np.empty((R.shape[0], R.shape[1], 4), np.uint8)
    fac8[..., :3] = np.clip(fac * 255.0 + 0.5, 0, 255).astype(np.uint8)
    fac8[..., 3] = 255
    rgb_a = np.ascontiguousarray(a.surf.makeImageSnapshot().toarray(colorType=_BGRA, alphaType=_PRE))
    rgb_b = np.ascontiguousarray(b.surf.makeImageSnapshot().toarray(colorType=_BGRA, alphaType=_PRE))
    mu = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    o = cv2.blendLinear(rgb_a, rgb_b, 1.0 - mu, mu)
    o = cv2.multiply(o, cv2.resize(fac8, (W, H), interpolation=cv2.INTER_LINEAR), scale=1.0 / 255.0)
    out = Frame()
    out.c.drawImage(_img(o, opaque=True), 0, 0)
    return out


def blend_page(a, b, k, g=0.0, **_):
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
    sh3 = skia.GradientShader.MakeLinear([(-Lw, 0), (0, 0)],
                                         [C("#2A1C0C", 150), C("#2A1C0C", 40), C("#FFF8E0", 70), C("#6A5030", 160)], [0.0, 0.16, 0.86, 1.0])
    c.save()
    c.clipRect(skia.Rect.MakeLTRB(-Lw, -BIG, 0, BIG))
    c.drawRect(skia.Rect.MakeLTRB(-Lw, -BIG, 0, BIG), skia.Paint(Shader=sh3))
    c.restore()
    c.drawLine(0, -BIG, 0, BIG, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=C("#3A2A18", 150)))
    c.restore()
    return out


def blend_giornata(a, b, k, g=0.0, seed=7, **_):
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
    giornata_reveal(c, paths, order, smooth(k), dr, span=0.70, soft=0.30, sweep=True)
    return out


# ───────────────────────────── yeni geçişler (YONETMENLIK_REHBERI §3) ─────────────────────────────
# Kural: gelen çekim geçiş BAŞLARKEN doğar (Shot.lead = süre): gelen çekimin ilk karesi geçişin ilk karesindedir; böylece nesne/iris/zum
# geçişlerinde yeni sahne boş duvar değil yaşayan bir çekim olarak açılır. Giden çekim kamerası durmadan sürer (cam_out), gelen hareket halinde başlar (cam_in).
# `dir` = KAMERA yönü: "r" kamera sağa → her şey ekranda SOLA akar (ilerleme/yükseliş yönü; zaman çizgisi soldan sağa okunur); "l" tersi; "u" kamera yukarı → içerik aşağı.
NEW_TR = ("iris", "slide", "zoomthru", "carry", "light", "candle")
NO_CARRY = ("dip", "candle")                    # kamera devri yok (karanlık ara)
# gelen çekimin "doğum" payı (sn): çekim görünür olmadan önce bu kadar erken başlar → nesneleri geçişin başında hazırdır (kinds'ın cx.amt doğuş animasyonları görünmeden biter)
BIRTH = dict(iris=0.9, slide=0.9, zoomthru=0.5, carry=0.9, light=0.6, candle=0.5, yikama=0.7, sayfa=0.7, giornata=0.7, fade=0.6, dip=0.6, zoom=0.7, wipe=0.7, whip=0.0)
_BGRA = skia.ColorType.kBGRA_8888_ColorType
_PRE = skia.AlphaType.kPremul_AlphaType
_OPQ = skia.AlphaType.kOpaque_AlphaType
_LS = skia.SamplingOptions(skia.FilterMode.kLinear)
_NS = skia.SamplingOptions()
_PLUS = skia.BlendMode.kPlus
_STK = skia.Paint.kStroke_Style
_BLURN = skia.kNormal_BlurStyle


def norm_tr(tr):
    """tr → (ad, süre, opts) | None. tr=(ad, süre[, opts]) ya da 'ad'. Yeni geçişlerde süre ≤ 1,0 sn."""
    if not tr:
        return None
    if isinstance(tr, str):
        name, d, o = tr, 0.8, {}
    else:
        name = tr[0]
        d = float(tr[1]) if len(tr) > 1 else 0.8
        o = dict(tr[2]) if len(tr) > 2 and tr[2] else {}
    if name in NEW_TR:
        d = min(d, 1.0)
    return name, d, o


def lead_for(name, d, opts=None):
    """Gelen çekimin yerel saatinin geçiş başlangıcından ne kadar ÖNCE başladığı (Shot.lead, sn) = süre + doğum payı. place="after" ya da lead=False → 0.
    Yeni geçişlerde (NEW_TR) varsayılan açık; eski geçişlerde opts lead=True ile açılır. Yerel saat t=0 → "kesme anı − lead"."""
    o = opts or {}
    if o.get("place") == "after" or not o.get("lead", name in NEW_TR):
        return 0.0
    return float(d) + float(o.get("birth", BIRTH.get(name, 0.7)))


def _arr(fr):
    return fr.surf.makeImageSnapshot().toarray(colorType=_BGRA, alphaType=_PRE)


def _img(arr, opaque=True):
    return skia.Image.fromarray(np.ascontiguousarray(arr), colorType=_BGRA, alphaType=_OPQ if opaque else _PRE)


def _snap(fr):
    return fr.surf.makeImageSnapshot()


def _layer(w=W, h=H):
    fr = Frame(w, h)
    fr.clear(skia.ColorTRANSPARENT)
    return fr


def _blur_arr(arr, sx, sy=0.0, half=False):
    """BGRA dizisinde ayrık Gauss bulanıklığı (sx/sy px). Büyük sigmada eksen başına 2^n alt-örnekleyip bulanıklaştırır, doğrusal büyütür (cv2 büyük çekirdekte ~80 ms → ~8 ms)."""
    h, w = arr.shape[:2]
    fx = fy = 1
    while sx / fx > 4.0 and fx < 8:
        fx *= 2
    while sy / fy > 4.0 and fy < 8:
        fy *= 2
    if half and fx == 1 and fy == 1 and max(sx, sy) > 1.5:
        fx = fy = 2
    if fx == 1 and fy == 1:
        return cv2.GaussianBlur(arr, (0, 0), sigmaX=max(0.01, sx), sigmaY=max(0.01, sy))
    sm = cv2.resize(arr, (w // fx, h // fy), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), sigmaX=max(0.01, sx / fx), sigmaY=max(0.01, sy / fy))
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_LINEAR)


@functools.lru_cache(maxsize=4)
def _glow_img(n=256, power=2.0):
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    r = np.hypot(xx - n / 2 + 0.5, yy - n / 2 + 0.5) / (n / 2)
    a = np.clip(1 - r, 0, 1) ** power
    return sk.np_to_image(np.dstack([np.full((n, n), 255, np.uint8)] * 3 + [(a * 255).astype(np.uint8)]))


_GRID4 = {}


def _grid4():
    g_ = _GRID4.get("g")
    if g_ is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
        g_ = _GRID4["g"] = (xx * 4.0, yy * 4.0)
    return g_


def _up(small):
    """(H/4, W/4, 4) → tam çözünürlük (cv2 doğrusal: ~2 ms; skia ölçekli çizim yerine)."""
    return cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)


def _add_small(c, small, blend=_PLUS):
    c.drawImage(_img(_up(small), opaque=False), 0, 0, _NS, skia.Paint(BlendMode=blend))


def _glow_small(items):
    """Toplamsal parıltı katmanı (BGRA premul, 1/4 çözünürlük). items: [(x, y, R, '#hex', alpha, güç)]."""
    hh, ww = H // 4, W // 4
    xx, yy = _grid4()
    acc = np.zeros((hh, ww, 3), np.float32)
    for (x, y, R, col, al, pw) in items:
        if al <= 0.003 or R <= 1:
            continue
        x0, x1 = max(0, int((x - R) / 4) - 1), min(ww, int((x + R) / 4) + 2)
        y0, y1 = max(0, int((y - R) / 4) - 1), min(hh, int((y + R) / 4) + 2)
        if x1 <= x0 or y1 <= y0:
            continue
        r = np.hypot(xx[y0:y1, x0:x1] - x, yy[y0:y1, x0:x1] - y) / R
        v = np.clip(1.0 - r, 0.0, 1.0) ** pw * al
        rr_, gg_, bb_ = sk.rgb(col)
        acc[y0:y1, x0:x1] += v[..., None] * np.array([bb_, gg_, rr_], np.float32)
    out = np.zeros((hh, ww, 4), np.uint8)
    out[..., :3] = np.clip(acc, 0, 255)
    out[..., 3] = out[..., :3].max(axis=2)
    return out


def _glow(c, x, y, R, color, alpha, power=2.0, blend=_PLUS):
    """Yumuşak radyal parıltı. Küçük yarıçap: önbellekli sprite; büyük: 1/4 çözünürlükte hesapla + cv2 büyüt (hızlı)."""
    if alpha <= 0.003 or R <= 1:
        return
    if R > 300:
        _add_small(c, _glow_small([(x, y, R, color, alpha, power)]), blend)
        return
    p = skia.Paint(AntiAlias=True, ColorFilter=skia.ColorFilters.Blend(C(color), skia.BlendMode.kSrcIn), BlendMode=blend)
    p.setAlphaf(clamp(alpha))
    c.drawImageRect(_glow_img(256, power), skia.Rect.MakeWH(256, 256), skia.Rect.MakeLTRB(x - R, y - R, x + R, y + R), _LS, p)


def _sweep(ax, ay, stops, alpha=255):
    return skia.GradientShader.MakeSweep(ax, ay, [C(c_, alpha) for _, c_ in stops], [p_ for p_, _ in stops])


# ───────────── iris ─────────────
OBJ_R = dict(florin=235.0, palle=268.0, sun=170.0, moon=150.0, dome=215.0, lens=230.0, seal=95.0)
_GOLD = [(0.00, "#C99A35"), (0.12, "#7A5518"), (0.25, "#5A3D12"), (0.37, "#B88A2C"), (0.50, "#EBCB78"), (0.62, "#FFF1B8"), (0.75, "#F0D27A"), (0.88, "#C99A35"), (1.00, "#C99A35")]
_RED = [(0.00, "#B33620"), (0.15, "#74201A"), (0.30, "#5A1710"), (0.45, "#A22E1A"), (0.58, "#E8745A"), (0.70, "#F2A08A"), (0.85, "#C24428"), (1.00, "#B33620")]
_STONE = [(0.00, "#A59A82"), (0.15, "#7A705C"), (0.30, "#5E5646"), (0.45, "#9A8F77"), (0.60, "#D4CAB0"), (0.72, "#EAE1CA"), (0.88, "#B4A98E"), (1.00, "#A59A82")]
_SILVER = [(0.00, "#B8C4D8"), (0.20, "#7A879C"), (0.40, "#5C677A"), (0.55, "#E6EEF9"), (0.70, "#FFFFFF"), (0.85, "#C5D0E2"), (1.00, "#B8C4D8")]
_WAX = [(0.00, "#A52A1C"), (0.15, "#6E1710"), (0.30, "#58110C"), (0.45, "#9A2616"), (0.58, "#D4573C"), (0.70, "#EE8E70"), (0.85, "#B8321F"), (1.00, "#A52A1C")]


def _ring_metal(c, ax, ay, rr, w, stops, al, dark="#3A2610", ticks=0, hi="#FFF6D0", beads=0, bead_col="#EBCB78"):
    """Kabartmalı halka: koyu dış hat + açı süpürme degradesi + iç parlak bant + ince filetolar (+ tırtıl/boncuk)."""
    c.drawCircle(ax, ay, rr, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w + 5, Color=C(dark, int(235 * al))))
    c.drawCircle(ax, ay, rr, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w, Shader=_sweep(ax, ay, stops, int(255 * al))))
    c.drawCircle(ax, ay, rr - w * 0.2, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w * 0.30, Color=C(hi, int(100 * al)), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 1.6)))
    for off in (-0.5, 0.5):
        c.drawCircle(ax, ay, rr + off * w, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=2.0, Color=C(dark, int(210 * al))))
    if ticks and rr < 1500:
        th = np.linspace(0, 2 * math.pi, int(ticks), endpoint=False)
        r0, r1 = rr + w * 0.5 - w * 0.30, rr + w * 0.5 - 1.5
        pth = skia.Path()
        for t_ in th:
            ct, sn = math.cos(t_), math.sin(t_)
            pth.moveTo(ax + ct * r0, ay + sn * r0)
            pth.lineTo(ax + ct * r1, ay + sn * r1)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=max(1.5, w * 0.05), Color=C(dark, int(150 * al))))
    if beads and rr < 1500:
        for t_ in np.linspace(0, 2 * math.pi, int(beads), endpoint=False):
            bx, by, br = ax + math.cos(t_) * rr, ay + math.sin(t_) * rr, w * 0.19
            c.drawCircle(bx, by, br, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((bx - br * 0.3, by - br * 0.35), br * 1.4, [C("#FFF6D0", int(255 * al)), C(bead_col, int(255 * al)), C("#5A3D12", int(255 * al))], [0, 0.5, 1])))


def _ring_fall(c, gx, gy, ax, ay, r_a, r_b, alphas, hue):
    """r_a..r_b yarıçap aralığında (merkez ax,ay) gradyan merkezi (gx,gy) olan radyal alfa düşüşü: alphas=(a_a, a_b) siyah; hue=0 siyah."""
    R = max(2.0, r_b + math.hypot(gx - ax, gy - ay))
    cols = [C("#000000", int(alphas[0])), C("#000000", int(alphas[0])), C("#000000", int(alphas[0] * 0.45 + alphas[1] * 0.55)), C("#000000", int(alphas[1]))]
    pos = [0.0, max(0.0, (r_a - math.hypot(gx - ax, gy - ay)) / R), max(0.001, (0.5 * (r_a + r_b)) / R), min(1.0, r_b / R)]
    pos = sorted(pos)
    sh = skia.GradientShader.MakeRadial((gx, gy), R, cols, pos)
    c.drawCircle(ax, ay, 0.5 * (r_a + r_b), skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=max(1.0, r_b - r_a), Shader=sh))


def _iris_ring(fr, ax, ay, rr, obj, k, al, g, Rfar):
    c = fr.c
    if al <= 0.003 or rr - 80 > Rfar:
        return
    w = clamp(rr * 0.075, 12.0, 66.0)
    shadows = rr < 820
    if obj == "sun":
        _glow(c, ax, ay, rr * 1.55, "#FFD98A", 0.55 * al, 1.6)
        n = 30
        pth = skia.Path()
        for i in range(n):
            a0 = 2 * math.pi * i / n + g * 0.18
            ln = rr * (0.42 if i % 2 else 0.70)
            hw = 0.045
            pth.moveTo(ax + math.cos(a0 - hw) * rr * 0.98, ay + math.sin(a0 - hw) * rr * 0.98)
            pth.lineTo(ax + math.cos(a0) * (rr + ln), ay + math.sin(a0) * (rr + ln))
            pth.lineTo(ax + math.cos(a0 + hw) * rr * 0.98, ay + math.sin(a0 + hw) * rr * 0.98)
            pth.close()
        c.drawPath(pth, skia.Paint(AntiAlias=True, Color=C("#FFE7A6", int(120 * al)), BlendMode=_PLUS))
        c.drawCircle(ax, ay, rr, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=max(6, w * 0.55), Color=C("#FFF3C4", int(235 * al))))
        c.drawCircle(ax, ay, rr + max(6, w * 0.55) * 0.5, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=2, Color=C("#8A6422", int(180 * al))))
        return
    if shadows:                                   # dışa yumuşak gölge (halka bandında radyal degrade: blur maskesi yok → hızlı)
        _ring_fall(c, ax + 3, ay + 8, ax, ay, rr + w * 0.5 - 6, rr + w * 0.5 + 46, (110 * al, 0), 0)
    if obj == "florin":
        _ring_metal(c, ax, ay, rr, w, _GOLD, al, ticks=clamp(rr / 5.5, 56, 240))
    elif obj == "palle":
        _ring_metal(c, ax, ay, rr, w * 1.05, _RED, al, dark="#3A0E0A", hi="#FFD6C8")
        for off in (-0.40, 0.40):
            c.drawCircle(ax, ay, rr + off * w * 1.05, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=max(2.0, w * 0.07), Color=C("#EBCB78", int(235 * al))))
        for t_ in np.linspace(0, 2 * math.pi, 12, endpoint=False):
            if rr < 1500:
                bx, by, br = ax + math.cos(t_) * rr, ay + math.sin(t_) * rr, w * 0.17
                c.drawCircle(bx, by, br, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeRadial((bx - br * 0.3, by - br * 0.35), br * 1.4, [C("#FFF6D0", int(255 * al)), C("#D1A239", int(255 * al)), C("#5A3D12", int(255 * al))], [0, 0.5, 1])))
    elif obj == "dome":
        _ring_metal(c, ax, ay, rr, w * 1.15, _STONE, al, dark="#2E2A20", hi="#FFFFFF")
        if rr < 1500:
            th = np.linspace(0, 2 * math.pi, int(clamp(rr / 7, 40, 150)), endpoint=False)
            pth = skia.Path()
            for t_ in th:
                ct, sn = math.cos(t_), math.sin(t_)
                pth.moveTo(ax + ct * (rr - w * 0.55), ay + sn * (rr - w * 0.55))
                pth.lineTo(ax + ct * (rr + w * 0.55), ay + sn * (rr + w * 0.55))
            c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=1.6, Color=C("#2E2A20", int(120 * al))))
    elif obj == "moon":
        _glow(c, ax, ay, rr * 1.35, "#CFE0FF", 0.30 * al, 1.8)
        _ring_metal(c, ax, ay, rr, w * 0.7, _SILVER, al, dark="#2A3550", hi="#FFFFFF")
    elif obj == "lens":
        c.drawCircle(ax, ay, rr + 3.5, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=3.0, Color=C("#FF5A4A", int(95 * al))))
        c.drawCircle(ax, ay, rr - 3.5, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=3.0, Color=C("#4A7AFF", int(95 * al))))
        _ring_metal(c, ax, ay, rr, w * 0.62, _SILVER, al, dark="#1A2030", hi="#FFFFFF")
        for ang, ln in ((-2.35, 0.55), (0.80, 0.35)):
            r_ = pathR = rr - w * 0.15
            pth = skia.Path()
            pth.addArc(skia.Rect.MakeLTRB(ax - r_, ay - r_, ax + r_, ay + r_), math.degrees(ang), math.degrees(ln))
            c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=max(4, w * 0.22), StrokeCap=skia.Paint.kRound_Cap, Color=C("#FFFFFF", int(190 * al)), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 2.2)))
    elif obj == "seal":
        pts = []
        for i in range(48):
            t_ = 2 * math.pi * i / 48
            pts.append((ax + math.cos(t_) * rr * (1 + 0.05 * math.sin(t_ * 7 + 1) + 0.035 * math.sin(t_ * 13 + 2.2)), ay + math.sin(t_) * rr * (1 + 0.05 * math.sin(t_ * 7 + 1) + 0.035 * math.sin(t_ * 13 + 2.2))))
        pth = sk.smooth_path(pts, True, 0.5)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w * 1.25 + 5, Color=C("#3A0E0A", int(235 * al))))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w * 1.25, Shader=_sweep(ax, ay, _WAX, int(255 * al))))
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=w * 0.34, Color=C("#FFD6C8", int(95 * al)), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 2.0)))
    else:
        _ring_metal(c, ax, ay, rr, w, _GOLD, al, ticks=clamp(rr / 5.5, 56, 240))
    if obj in ("florin", "palle", "seal", "dome"):      # dönen parıltı
        ang = -2.3 + 2.9 * k
        gx, gy = ax + math.cos(ang) * rr, ay + math.sin(ang) * rr
        _glow(c, gx, gy, w * 2.4, "#FFF3C4", 0.75 * al, 1.8)


def blend_iris(a, b, k, g=0.0, d=0.8, at=None, obj="florin", r=None, inv=False, **_):
    """Iris: ekrandaki yuvarlak nesne (obj) A ile birlikte büyür, kenarında nesnenin halkası; B halkanın içinde açılır ve ekranı doldurur.
    at=(x,y) nesne merkezi, r=nesnenin ekrandaki yarıçapı (px; obj varsayılanı OBJ_R), inv=True: ters yön (B'nin içinden A'ya daralır)."""
    if inv:
        return blend_iris(b, a, 1.0 - k, g, d, at=at, obj=obj, r=r, inv=False)
    ax, ay = at or (W / 2, H * 0.47)
    r0 = float(r or OBJ_R.get(obj, 230.0))
    Rfar = math.hypot(max(ax, W - ax), max(ay, H - ay))
    Rend = Rfar * 1.03 + 90 + (66 if obj != "sun" else 0)
    e = ease_io(clamp(k), 2.3)
    rr = r0 * (Rend / r0) ** e
    S = rr / r0
    out = Frame()
    c = out.c
    imgA, imgB = _snap(a), _snap(b)
    c.save()
    c.translate(ax, ay)
    c.scale(S, S)
    c.translate(-ax, -ay)
    c.drawImage(imgA, 0, 0, _LS)
    c.restore()
    k_in = smooth(k / 0.10)
    sb = 1.0 + (0.28 if obj == "lens" else 0.12) * (1.0 - e)
    pth = skia.Path()
    pth.addCircle(ax, ay, max(1.0, rr))
    c.save()
    c.clipPath(pth, skia.ClipOp.kIntersect, True)
    pp = skia.Paint()
    pp.setAlphaf(k_in)
    c.translate(ax, ay)
    c.scale(sb, sb)
    c.translate(-ax, -ay)
    c.drawImage(imgB, 0, 0, _LS, pp)
    c.restore()
    if obj != "sun" and rr < 1500:                       # B üstüne iç gölge (halkanın derinliği)
        c.save()
        c.clipPath(pth, skia.ClipOp.kIntersect, True)
        _ring_fall(c, ax, ay, ax, ay, rr - 70, rr - 2, (0, 125 * k_in), 0)
        c.restore()
    _iris_ring(out, ax, ay, rr, obj, k, k_in, g, Rfar)
    return out


# ───────────── slide ─────────────
def blend_slide(a, b, k, g=0.0, d=0.8, dir="r", seam=True, punch=0.03, **_):
    """Slide: iki çekim aynı yönde birlikte kayar (tek kamera, iki yer). dir = kamera yönü (r: içerik sola akar). Hareket bulanıklığı + hafif zum vuruşu + fresk dikişi."""
    e = ease_io(clamp(k), 2.1)
    vx, vy = {"r": (-1, 0), "l": (1, 0), "u": (0, 1), "d": (0, -1)}.get(dir, (-1, 0))
    ox, oy = vx * W, vy * H
    zs = 1.0 + punch * math.sin(math.pi * e)
    out = Frame()
    c = out.c
    imgA, imgB = _snap(a), _snap(b)

    def draw(img, px, py):
        c.save()
        c.translate(W / 2 + px, H / 2 + py)
        c.scale(zs, zs)
        c.translate(-W / 2, -H / 2)
        c.drawImage(img, 0, 0, _LS)
        c.restore()
    draw(imgA, ox * e, oy * e)
    draw(imgB, -ox * (1 - e), -oy * (1 - e))
    if seam:                                              # B'nin A'yı örttüğü kenar: ince ışık çizgisi + A tarafına yumuşak gölge
        amp = math.sin(math.pi * e)
        if vx:
            xs = W / 2 - ox * (1 - e) + (-W / 2 * zs if vx < 0 else W / 2 * zs)
            xe = xs + vx * 70
            g1 = skia.GradientShader.MakeLinear([(xs, 0), (xe, 0)], [C("#1A1208", int(95 * amp)), C("#1A1208", 0)], [0, 1])
            c.drawRect(skia.Rect.MakeLTRB(min(xs, xe), 0, max(xs, xe), H), skia.Paint(Shader=g1))
            c.drawRect(skia.Rect.MakeLTRB(xs - 1, 0, xs + 1, H), skia.Paint(Color=C("#FFF4D6", int(110 * amp))))
        else:
            ys = H / 2 - oy * (1 - e) + (-H / 2 * zs if vy < 0 else H / 2 * zs)
            ye = ys + vy * 70
            g1 = skia.GradientShader.MakeLinear([(0, ys), (0, ye)], [C("#1A1208", int(95 * amp)), C("#1A1208", 0)], [0, 1])
            c.drawRect(skia.Rect.MakeLTRB(0, min(ys, ye), W, max(ys, ye)), skia.Paint(Shader=g1))
            c.drawRect(skia.Rect.MakeLTRB(0, ys - 1, W, ys + 1), skia.Paint(Color=C("#FFF4D6", int(110 * amp))))
    # hareket bulanıklığı (deklanşör ≈ 0,3 kare)
    kk = clamp(k)
    de_dk = max(0.0, (ease_io(clamp(kk + 0.01), 2.1) - ease_io(clamp(kk - 0.01), 2.1)) / 0.02)
    dist = W if vx else H
    sp = de_dk * dist / max(1e-6, d * 24.0)                 # px/kare
    sig = sp * 0.15
    if sig > 1.2:
        arr = _arr(out)
        arr = _blur_arr(arr, sig if vx else 0.0, sig if vy else 0.0, half=True)
        out2 = Frame()
        out2.c.drawImage(_img(arr), 0, 0)
        return out2
    return out


# ───────────── zoomthru ─────────────
def _zoom_taps(small, cx_, cy_, z, delta, n):
    """small: BGRA yarı çözünürlük; (cx_,cy_) çevresinde z ölçeği, ±delta/2 yayılımda n kare ortalaması (zum bulanıklığı)."""
    hh, ww = small.shape[:2]
    acc = np.zeros((hh, ww, 4), np.float32)
    for j in range(n):
        s = z * (1.0 + delta * ((j / (n - 1)) - 0.5)) if n > 1 else z
        M = np.float32([[s, 0, cx_ * (1 - s)], [0, s, cy_ * (1 - s)]])
        cv2.accumulate(cv2.warpAffine(small, M, (ww, hh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), acc)
    return cv2.convertScaleAbs(acc, alpha=1.0 / n)


def blend_zoomthru(a, b, k, g=0.0, d=0.9, at=None, at_b=None, depth=5.0, **_):
    """Zum-geçiş: A'nın bir ayrıntısına (at) hızlanarak zum sürer; içinden B yerleşik pozdan (at_b) geri çekilerek açılır. Ölçek geçişi (harita → şehir, defter satırı → oda)."""
    ax, ay = at or (W / 2, H * 0.5)
    bx, by = at_b or at or (W / 2, H * 0.5)
    kA = clamp(k / 0.60)
    lzA = math.log(depth) * ease_in(kA, 2.0)
    kB = clamp((k - 0.26) / 0.74)
    lzB = math.log(max(1.1, depth * 0.62)) * (1.0 - ease_out(kB, 2.4))
    wB = smooth((k - 0.34) / 0.30)
    zA, zB = math.exp(lzA), math.exp(lzB)
    out = Frame()
    if k < 0.10 or k > 0.90:                                  # tek katman: tam çözünürlük, bulanıklık yok
        src, z, px, py = (a, zA, ax, ay) if k < 0.5 else (b, zB, bx, by)
        c = out.c
        c.save()
        c.translate(px, py)
        c.scale(z, z)
        c.translate(-px, -py)
        c.drawImage(_snap(src), 0, 0, _LS)
        c.restore()
        return out
    dk = 0.02
    sA = abs(math.log(depth) * (ease_in(clamp((k + dk) / 0.60), 2.0) - ease_in(clamp((k - dk) / 0.60), 2.0)) / (2 * dk))
    sB = abs(math.log(max(1.1, depth * 0.62)) * (ease_out(clamp((k + dk - 0.26) / 0.74), 2.4) - ease_out(clamp((k - dk - 0.26) / 0.74), 2.4)) / (2 * dk))
    per_frame = 1.0 / max(1e-6, d * 24.0)
    dA, dB = sA * per_frame * 0.5, sB * per_frame * 0.5       # göreli ölçek yayılımı (deklanşör 0,5 kare)
    sa = cv2.resize(_arr(a), (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    sb_ = cv2.resize(_arr(b), (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    nA = int(clamp(dA * 480 / 3.0 + 1, 1, 9))
    nB = int(clamp(dB * 480 / 3.0 + 1, 1, 9))
    A2 = _zoom_taps(sa, ax / 2, ay / 2, zA, dA, nA)
    B2 = _zoom_taps(sb_, bx / 2, by / 2, zB, dB, nB)
    o = cv2.addWeighted(A2, 1.0 - wB, B2, wB, 0)
    gl = 4.0 * wB * (1.0 - wB)                                # çözülme ortasında ince ılık sır (malzeme: pigment)
    if gl > 0.01:
        col = np.array([106, 168, 200, 255], np.float32) / 255.0      # BGRA: oker
        o = (o.astype(np.float32) * ((1 - 0.16 * gl) + 0.16 * gl * col)).astype(np.uint8)
    o = cv2.resize(o, (W, H), interpolation=cv2.INTER_LINEAR)
    out.c.drawImage(_img(o), 0, 0)
    return out


# ───────────── carry ─────────────
def _band_pts(bw, h, g, seed, amp, ragged=0.0, slant=0.10, x0=0.0):
    """Eğik, dalgalı şerit kenarları (yerel koordinat: merkez çizgisi x0 + slant·(y−h/2))."""
    rs = np.random.RandomState(seed)
    ph = rs.rand(6) * 6.283
    ys = np.linspace(-60, h + 60, 52)
    L, R = [], []
    for y in ys:
        cxl = x0 + slant * (y - h / 2)
        wv1 = amp * math.sin(y / 97 + ph[0] + g * 2.6) + amp * 0.5 * math.sin(y / 41 + ph[1] + g * 4.1)
        wv2 = amp * math.sin(y / 89 + ph[2] + g * 2.2) + amp * 0.5 * math.sin(y / 37 + ph[3] + g * 3.6)
        L.append((cxl - bw / 2 + wv1 + ragged * (rs.rand() - 0.5) * 2, y))
        R.append((cxl + bw / 2 + wv2 + ragged * (rs.rand() - 0.5) * 2, y))
    return L, R


def _silk(c, L, R, c1, h, sheen=True, g=0.0):
    """İpek bant: ana yol dolgusu (yatay degrade) + eğik ışık şeritleri."""
    path = sk.smooth_path(L + R[::-1], True, 0.45)
    xa, xb = min(p[0] for p in L) - 20, max(p[0] for p in R) + 20
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    sh = skia.GradientShader.MakeLinear([(xa, 0), (xb, 0)], [C(c1[0]), C(c1[1]), C(c1[2]), C(c1[3]), C(c1[4])], [0.0, 0.22, 0.46, 0.74, 1.0])
    c.drawRect(skia.Rect.MakeLTRB(xa, -60, xb, h + 60), skia.Paint(Shader=sh))
    if sheen:
        for j in range(4):
            xx = xa + ((g * 190 + j * 150) % (xb - xa + 240)) - 120
            c.drawPath(sk.poly_path([(xx, -60), (xx + 46, -60), (xx + 46 - 0.1 * (h + 120), h + 60), (xx - 0.1 * (h + 120), h + 60)]), skia.Paint(AntiAlias=True, Color=C("#FFE2D0", 46)))
    c.restore()
    return path


def _strip_layer(style, bw, h, g, k, pad=190, trail=1):
    """Taşıyıcı şeridi ayrı saydam yüzeye çiz (merkez x = pad + bw/2, y=h/2'de); gölge dahil. trail: arkada sürüklenen şeritlerin yönü (+1 sağ, −1 sol)."""
    fr = _layer(int(bw + 2 * pad), h)
    c = fr.c
    x0 = pad + bw / 2
    st = _STK
    if style == "ink":
        L, R = _band_pts(bw, h, g, 5, 11.0, ragged=9.0, x0=x0)
    elif style == "paper":
        L, R = _band_pts(bw, h, g, 7, 3.0, ragged=12.0, x0=x0)
    else:
        L, R = _band_pts(bw, h, g, 3, 16.0 if style == "ribbon" else 13.0, x0=x0)
    path = sk.poly_path(L + R[::-1]) if style in ("ink", "paper") else sk.smooth_path(L + R[::-1], True, 0.45)
    # arkadan sürüklenen ince kurdeleler (ribbon): lapis + yaldız
    if style == "ribbon":
        for j, (off, wd, cols_) in enumerate(((78, 58, ("#0B1236", "#1E3680", "#4468C0", "#233C8C", "#0B1236")), (176, 34, ("#6E4A16", "#BE8A2C", "#F7E2A0", "#D1A239", "#80571B")))):
            Lj, Rj = _band_pts(wd, h, g + 0.55 * (j + 1), 20 + j, 20.0 + 6 * j, x0=x0 + trail * (bw / 2 + off))
            c.save()
            c.translate(8, 6)
            c.drawPath(sk.smooth_path(Lj + Rj[::-1], True, 0.45), skia.Paint(AntiAlias=True, Color=C("#000000", 70), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 8)))
            c.restore()
            _silk(c, Lj, Rj, cols_, h, sheen=False, g=g)
            c.drawPath(sk.smooth_path(Lj + Rj[::-1], True, 0.45), skia.Paint(AntiAlias=True, Style=st, StrokeWidth=1.6, Color=C("#1A1208", 140)))
    # gölge
    c.save()
    c.translate(12, 9)
    c.drawPath(path, skia.Paint(AntiAlias=True, Color=C("#000000", 95), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 13)))
    c.restore()
    c.save()
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    xa, xb = min(p[0] for p in L) - 20, max(p[0] for p in R) + 20
    if style == "ribbon":
        _silk(c, L, R, ("#5A1710", "#A22E1A", "#E8745A", "#B33620", "#5A1710"), h, sheen=True, g=g)
    elif style == "banner":
        sh = skia.GradientShader.MakeLinear([(xa, 0), (xb, 0)], [C("#7A1E14"), C("#B33620"), C("#CC4A2D"), C("#A22E1A"), C("#6A1810")], [0.0, 0.2, 0.5, 0.78, 1.0])
        c.drawRect(skia.Rect.MakeLTRB(xa, -60, xb, h + 60), skia.Paint(Shader=sh))
        rs = np.random.RandomState(8)
        for i in range(60):                                  # dokuma izi
            xx = xa + rs.rand() * (xb - xa)
            c.drawLine(xx, 0, xx + (rs.rand() - 0.5) * 6, h, skia.Paint(AntiAlias=True, Style=st, StrokeWidth=1.0, Color=C("#FFE2D0", 14)))
    elif style == "ink":
        c.drawRect(skia.Rect.MakeLTRB(xa, -60, xb, h + 60), skia.Paint(Color=C("#1B130C")))
        rs = np.random.RandomState(11)
        for i in range(70):                                  # kuru fırça izleri
            yy = rs.rand() * h
            x1 = xa + rs.rand() * (xb - xa) * 0.5
            c.drawLine(x1, yy, x1 + (0.25 + 0.75 * rs.rand()) * (xb - xa), yy + (rs.rand() - 0.5) * 3, skia.Paint(AntiAlias=True, Style=st, StrokeWidth=1.0 + 2.2 * rs.rand(), Color=C("#5A4632", int(34 + 70 * rs.rand()))))
    else:                                                     # paper
        c.drawRect(skia.Rect.MakeLTRB(xa, -60, xb, h + 60), skia.Paint(Shader=skia.GradientShader.MakeLinear([(xa, 0), (xb, 0)], [C("#CDB88A"), C("#EADFC0"), C("#E6D5AE"), C("#C9B488")], [0, 0.25, 0.7, 1.0])))
        rs = np.random.RandomState(4)
        for i in range(int(h / 34)):
            yy = 20 + i * 34
            ww = 50 + rs.rand() * 210
            xx = x0 - bw * 0.34 + rs.rand() * 30 + 0.10 * (yy - h / 2)
            c.drawLine(xx, yy, xx + ww, yy + (rs.rand() - 0.5) * 2, skia.Paint(AntiAlias=True, Style=st, StrokeWidth=2.2, Color=C("#5A3B25", 95)))
    c.restore()
    # kenar süsü / ek ayrıntılar
    if style in ("ribbon", "banner"):
        for side, P in ((0, L), (1, R)):
            inset = [(p[0] + (15 if side == 0 else -15), p[1]) for p in P]
            c.drawPath(sk.smooth_path(inset, False, 0.45), skia.Paint(AntiAlias=True, Style=st, StrokeWidth=2.6, Color=C("#EBCB78", 225), PathEffect=skia.DashPathEffect.Make([11, 8], 0)))
            c.drawPath(sk.smooth_path(P, False, 0.45), skia.Paint(AntiAlias=True, Style=st, StrokeWidth=2.0, Color=C("#3A0E0A", 160)))
    if style == "banner":
        for yy in (h * 0.20, h * 0.50, h * 0.80):
            xm = x0 + 0.10 * (yy - h / 2)
            CM.mini_palle(fr, xm, yy, 205, color="#F6E6B0", alpha=0.97)
            fr.circle(xm, yy, 128, style="stroke", sw=5, color="#EBCB78", alpha=0.95)
            fr.circle(xm, yy, 140, style="stroke", sw=1.6, color="#3A0E0A", alpha=0.6)
        for p in R[::2]:                                       # saçak (arka kenar)
            c.drawLine(p[0], p[1], p[0] + 24, p[1] + 3, skia.Paint(AntiAlias=True, Style=st, StrokeWidth=2.8, Color=C("#EBCB78", 205)))
    elif style == "ink":
        rs = np.random.RandomState(13)
        lead = L if trail > 0 else R
        for i in range(34):                                    # ön kenarda sıçrama + kıl uçları
            yy = rs.rand() * h
            xx = lead[0][0] + 0.10 * (yy - h / 2) - 6 - rs.rand() * 90
            c.drawCircle(xx, yy, 1.5 + rs.rand() * 5, skia.Paint(AntiAlias=True, Color=C("#1B130C", int(210 - xx % 60))))
        for i in range(48):                                    # arka kenarda kuru fırça kılları
            yy = rs.rand() * h
            xx = R[0][0] + 0.10 * (yy - h / 2) + rs.rand() * 8
            c.drawLine(xx - 4, yy, xx + 18 + rs.rand() * 90, yy + (rs.rand() - 0.5) * 2, skia.Paint(AntiAlias=True, Style=st, StrokeWidth=1.2 + 1.6 * rs.rand(), Color=C("#1B130C", int(70 + 90 * rs.rand()))))
    elif style == "paper":
        for P in (L, R):                                       # yırtık lif kenarı
            c.drawPath(sk.poly_path(P, False), skia.Paint(AntiAlias=True, Style=st, StrokeWidth=3.4, Color=C("#F6EDD6", 230)))
        CM.wax_seal(fr, x0, h * 0.5, r=56, palle=True)
    return fr


def blend_carry(a, b, k, g=0.0, d=0.8, dir="r", strip="ribbon", slant=0.10, **_):
    """Carry: ön plandan bir öğe (strip: ribbon | ink | banner | paper) ekranı süpürür; değişim şeridin arkasında olur. dir = kamera yönü (r: şerit sağdan sola geçer)."""
    style = strip if strip in ("ribbon", "ink", "banner", "paper") else "ribbon"
    bw = {"ribbon": 330.0, "ink": 400.0, "banner": 420.0, "paper": 380.0}[style]
    left = dir in ("r", "u")                      # şerit sağdan sola
    pad = 400 if style == "ribbon" else 190
    ext = bw / 2 + 90 + abs(slant) * H / 2 + (230 if style == "ribbon" else 0)
    e = ease_io(clamp(k), 1.9)
    x_from, x_to = (W + ext, -ext) if left else (-ext, W + ext)
    xc = x_from + (x_to - x_from) * e
    out = Frame()
    c = out.c
    imgA, imgB = _snap(a), _snap(b)
    c.drawImage(imgA, 0, 0)
    yt, yb = -60, H + 60                          # B: şeridin arkasında kalan bölge (merkez çizgisi eğik)
    xt, xb = xc + slant * (yt - H / 2), xc + slant * (yb - H / 2)
    poly = [(xt, yt), (W + 50, yt), (W + 50, yb), (xb, yb)] if left else [(-50, yt), (xt, yt), (xb, yb), (-50, yb)]
    c.save()
    c.clipPath(sk.poly_path(poly), skia.ClipOp.kIntersect, True)
    c.drawImage(imgB, 0, 0)
    c.restore()
    lay = _strip_layer(style, bw, H, g, k, pad, trail=1 if left else -1)
    kk = clamp(k)
    de_dk = max(0.0, (ease_io(clamp(kk + 0.01), 1.9) - ease_io(clamp(kk - 0.01), 1.9)) / 0.02)
    sp = de_dk * abs(x_to - x_from) / max(1e-6, d * 24.0)
    sig = sp * (0.09 if style in ("ribbon", "banner") else 0.11)
    arr = _arr(lay)
    if sig > 1.2:
        arr = _blur_arr(arr, sig, 0.0)
    c.drawImage(_img(arr, opaque=False), xc - pad - bw / 2, 0)
    return out


# ───────────── light ─────────────
_LGRID = {}


def _light_maps(ax, ay):
    """(1/4 çözünürlük) mesafe haritası r ve açı indeks haritası (0..719): kaynak noktasına göre; önbellekli."""
    key = (int(ax), int(ay))
    m = _LGRID.get(key)
    if m is None:
        hh, ww = H // 4, W // 4
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        dx, dy = xx * 4 - ax, yy * 4 - ay
        r = np.hypot(dx, dy)
        th = np.arctan2(dy, dx)
        idx = ((th + math.pi) / (2 * math.pi) * 720.0).astype(np.int32) % 720
        if len(_LGRID) > 12:
            _LGRID.clear()
        m = _LGRID[key] = (r, idx, th)
    return m


def blend_light(a, b, k, g=0.0, d=0.8, at=None, col="#FFD98A", rays=True, spread=1.7, dim=0.46, tint=0.55, **_):
    """Işık: sıcak ışık huzmesi yükselir (at: kaynak, varsayılan alt orta); çevre kararır, merkez altına boyanır (beyaza boğulma yok); B ışığın içinden doğar.
    Tek yumuşak tepe (sin^1.6). Işık alanı 1/4 çözünürlükte hesaplanır (~25 ms)."""
    ax, ay = at or (W / 2, H * 0.80)
    kk = clamp(k)
    I = math.sin(math.pi * kk) ** 1.6
    w = smooth((kk - 0.20) / 0.40)
    out = Frame()
    c = out.c
    c.drawImage(_snap(a), 0, 0)
    pp = skia.Paint()
    pp.setAlphaf(w)
    c.drawImage(_snap(b), 0, 0, _NS, pp)
    if I <= 0.004:
        return out
    r, idx, th = _light_maps(ax, ay)
    base = math.atan2(H / 2 - ay, W / 2 - ax)
    G = 0.72 * np.exp(-(r / 760.0) ** 1.15) + 0.42 * np.exp(-(r / 250.0) ** 1.4)
    R_ = np.zeros_like(G)
    if rays:
        n = 11
        prof = np.zeros(720, np.float32)
        tt = (np.arange(720, dtype=np.float32) + 0.5) / 720.0 * 2 * math.pi - math.pi
        for i in range(n):
            thi = base + (i - (n - 1) / 2) * (spread / (n - 1)) + 0.05 * math.sin(g * 0.9 + i * 1.7)
            hw = 0.022 + 0.014 * math.sin(i * 2.3 + 1.0) ** 2
            dth = (tt - thi + math.pi) % (2 * math.pi) - math.pi
            prof += (0.5 + 0.5 * math.sin(i * 1.3 + 0.4)) * np.exp(-(dth / hw) ** 2)
        R_ = prof[idx] * np.exp(-r / 1500.0)
    G = np.clip(G, 0.0, 1.0)
    br, bg_, bb = sk.rgb(col)[2], sk.rgb(col)[1], sk.rgb(col)[0]
    # 1) çevre kararması (siyah alfa)
    dk = np.zeros(G.shape + (4,), np.uint8)
    dk[..., 3] = np.clip(dim * I * np.clip((r - 240.0) / 1100.0, 0.0, 1.0) ** 1.0 * 255, 0, 255)
    c.drawImage(_img(_up(dk), opaque=False), 0, 0)
    # 2) sıcak boya (SrcOver): merkez altına doğru kayar, beyaza kırpılmaz
    al = np.clip(tint * I * G, 0.0, 0.92)
    tn = np.zeros(G.shape + (4,), np.uint8)
    tn[..., 0], tn[..., 1], tn[..., 2] = (al * br).astype(np.uint8), (al * bg_).astype(np.uint8), (al * bb).astype(np.uint8)
    tn[..., 3] = (al * 255).astype(np.uint8)
    c.drawImage(_img(_up(tn), opaque=False), 0, 0)
    # 3) huzmeler + sıcak çekirdek (toplamsal, düşük)
    add = np.zeros(G.shape + (4,), np.uint8)
    rv = np.clip(0.30 * I * R_, 0.0, 1.0)
    add[..., 0], add[..., 1], add[..., 2] = (rv * br * 0.9).astype(np.uint8), (rv * bg_ * 0.9).astype(np.uint8), (rv * bb * 0.9).astype(np.uint8)
    add[..., 3] = np.maximum(np.maximum(add[..., 0], add[..., 1]), add[..., 2])
    _add_small(c, add)
    _glow(c, ax, ay, 300, "#FFF1C8", 0.50 * I, 1.8)
    return out


# ───────────── candle ─────────────
def _flame(c, x, y, s, g, al, tilt=0.0, seed=0):
    """Mum alevi (damla): s ölçek (1 ≈ 58 px yükseklik), titreşim g'ye bağlı (deterministik)."""
    if s <= 0.02 or al <= 0.01:
        return
    fl = 1.0 + 0.07 * math.sin(g * 11.3 + seed) + 0.04 * math.sin(g * 19.7 + seed * 2.1)
    sw = 4.0 * math.sin(g * 6.1 + seed) * s + tilt
    h_, w_ = 58.0 * s * fl, 17.0 * s
    pth = skia.Path()
    pth.moveTo(x, y)
    pth.cubicTo(x - w_, y - h_ * 0.30, x - w_ * 0.70 + sw * 0.3, y - h_ * 0.78, x + sw, y - h_)
    pth.cubicTo(x + w_ * 0.70 + sw * 0.3, y - h_ * 0.78, x + w_, y - h_ * 0.30, x, y)
    pth.close()
    _glow(c, x, y - h_ * 0.45, 150 * s, "#FFB45A", 0.55 * al, 1.8)
    c.drawPath(pth, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x, y), (x, y - h_)], [C("#FFF8E0", int(255 * al)), C("#FFD27A", int(255 * al)), C("#E8741C", int(230 * al))], [0.0, 0.45, 1.0])))
    c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=1.2, Color=C("#FFF2C0", int(110 * al))))
    c.drawOval(skia.Rect.MakeLTRB(x - w_ * 0.28, y - h_ * 0.30, x + w_ * 0.28, y - h_ * 0.02), skia.Paint(AntiAlias=True, Color=C("#3A5AA8", int(150 * al))))


def _candle_body(c, x, y_top, y_bot, al, melt=0.0):
    """Mum gövdesi (fildişi balmumu, eriyik damla); y_top: fitil/alev tabanı."""
    w_ = 44.0
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w_ / 2, y_top, x + w_ / 2, y_bot), 8, 8)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w_ / 2 + 8, y_top + 10, x + w_ / 2 + 8, y_bot + 6), 8, 8), skia.Paint(AntiAlias=True, Color=C("#000000", int(110 * al)), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 8)))
    c.drawRRect(rr, skia.Paint(AntiAlias=True, Shader=skia.GradientShader.MakeLinear([(x - w_ / 2, 0), (x + w_ / 2, 0)], [C("#B8A47C", int(255 * al)), C("#F2E6C4", int(255 * al)), C("#E8D8AE", int(255 * al)), C("#A8946A", int(255 * al))], [0, 0.35, 0.7, 1.0])))
    c.drawOval(skia.Rect.MakeLTRB(x - w_ / 2, y_top - 5, x + w_ / 2, y_top + 7), skia.Paint(AntiAlias=True, Color=C("#FFF2D0", int(255 * al))))
    c.drawLine(x, y_top - 3, x + 1, y_top - 14, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=2.4, Color=C("#2A1C0E", int(255 * al))))
    for dx_, ln in ((-w_ * 0.28, 46), (w_ * 0.12, 74), (w_ * 0.34, 30)):                  # eriyik damlaları
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x + dx_ - 4, y_top + 2, x + dx_ + 4, y_top + 2 + ln * (0.6 + 0.4 * melt)), 4, 4), skia.Paint(AntiAlias=True, Color=C("#FFF4DA", int(210 * al))))


def _smoke(c, x, y, p, g, al):
    """Sönen fitilden yükselen duman (p: 0..1 ilerleme)."""
    if p <= 0 or al <= 0.01:
        return
    for j in range(3):
        pth = skia.Path()
        pth.moveTo(x, y)
        h_ = 260 * p * (0.8 + 0.2 * j)
        pts = [(x + math.sin(g * 2.1 + j * 1.7 + u * 6.0) * (10 + 34 * u) * (0.6 + 0.4 * j), y - u * h_) for u in np.linspace(0, 1, 14)]
        pth = sk.smooth_path(pts, False, 0.5)
        c.drawPath(pth, skia.Paint(AntiAlias=True, Style=_STK, StrokeWidth=3.0 + 7 * p, StrokeCap=skia.Paint.kRound_Cap, Color=C("#C9C2B4", int(80 * al * (1 - p) ** 1.2)), MaskFilter=skia.MaskFilter.MakeBlur(_BLURN, 3 + 6 * p)))


def _pool_alpha(shape, cx_, cy_, R, scale=4):
    """Mum havuzu: merkezde 0 (açık), dışarıda 1 (karanlık). (h/scale, w/scale) float32."""
    hh, ww = shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    dd = np.hypot(xx * scale - cx_, yy * scale - cy_)
    t = np.clip((dd - 0.20 * R) / max(1.0, 0.80 * R), 0.0, 1.0)
    t = t * t * (3 - 2 * t)
    return np.clip(t ** 0.85, 0.0, 1.0)


CANDLE_P = 0.62                                                 # sönme: R = Rfull·(1−e)^P; 0,5 = ışıklı alan doğrusal azalır ama kenardaki alevde son adım 32 luma/kare; 0,62 → en büyük adım ≈23 (24 fps)


def blend_candle(a, b, k, g=0.0, d=0.9, at=None, at_b=None, **_):
    """Mum: A'nın mumu söner (ışık havuzunun ALANI doğrusala yakın daralır → parlaklık düzgün düşer, duman), kısa karanlık, yeni mum yanar ve B ışık havuzu genişleyerek açılır.
    Ölüm / gece / zaman atlaması. Mum çekimin üstüne eklenen tek nesnedir (at: alev konumu; at_b: yeni alev)."""
    ax, ay = at or (W / 2, H * 0.62)
    bx, by = at_b or (ax, ay)
    kk = clamp(k)
    out = Frame()
    c = out.c
    first = kk < 0.5
    c.drawImage(_snap(a if first else b), 0, 0)
    far = math.hypot(max((ax if first else bx), W - (ax if first else bx)), max((ay if first else by), H - (ay if first else by)))
    Rfull = 1.25 * far                                          # ekranı tümüyle aydınlatan havuz yarıçapı
    flick = 1.0 + 0.035 * math.sin(g * 9.1) + 0.02 * math.sin(g * 17.3 + 1.0)
    mixl = lambda x: 0.5 * smooth(x) + 0.5 * clamp(x)         # yarı-doğrusal geçiş: parlaklık sıçramasız
    if first:
        e1 = mixl(kk / 0.50)
        R = (Rfull * max(0.0, 1.0 - e1) ** CANDLE_P + 60.0 * (1 - smooth((kk - 0.40) / 0.10))) * flick
        m = smooth(kk / 0.25)
        px, py, flame_s, fal = ax, ay, 1.0 - smooth((kk - 0.42) / 0.07), smooth(kk / 0.14)
        smoke = clamp((kk - 0.45) / 0.30)
        black = smooth((kk - 0.43) / 0.07)
    else:
        e2 = mixl((kk - 0.55) / 0.45)
        R = (Rfull * max(0.0, e2) ** 0.62 + 50.0 * smooth((kk - 0.55) / 0.07)) * flick
        m = 1.0 - smooth((kk - 0.72) / 0.28)
        px, py, flame_s, fal = bx, by, smooth((kk - 0.55) / 0.08), 1.0 - smooth((kk - 0.84) / 0.12)
        smoke = 0.0
        black = 1.0 - smooth((kk - 0.52) / 0.14)
    # karanlık örtüsü: 1/4 çözünürlükte alfa → cv2 ile büyüt (yumuşak)
    pa = _pool_alpha((H // 4, W // 4), px, py, max(R, 1.0))
    al = np.clip(np.maximum(pa * m, black), 0, 1)
    rgba = np.zeros((H // 4, W // 4, 4), np.uint8)
    rgba[..., 3] = (al * 255).astype(np.uint8)
    c.drawImage(_img(_up(rgba), opaque=False), 0, 0)
    # ılık parıltı (alevin çevresi)
    warm = clamp(fal) * (1.0 - 0.6 * black) if flame_s > 0.05 else 0.0
    _glow(c, px, py - 30, 520 * clamp(R / 260.0, 0.35, 1.0) * flick, "#FFB45A", 0.38 * warm, 1.7)
    # mum + alev (karanlıkta tek görünen nesne)
    cal = clamp(fal) if first else 1.0 - smooth((kk - 0.78) / 0.18)
    if cal > 0.01:
        _candle_body(c, px, py + 8, min(H - 70, py + 250), cal, melt=kk)
        _flame(c, px, py, max(0.0, flame_s), g, cal, seed=3 if first else 5)
    if first and smoke > 0:
        _smoke(c, px, py - 4, smoke, g, 1.0)
    return out


TR = dict(yikama=blend_wash, sayfa=blend_page, giornata=blend_giornata,
          iris=blend_iris, slide=blend_slide, zoomthru=blend_zoomthru, carry=blend_carry, light=blend_light, candle=blend_candle)


def blend(kind, a, b, k, g=0.0, d=0.8, **opts):
    """Geçiş karesi: kind ∈ TR; a=giden, b=gelen (Frame); k 0..1; g küresel sn; d geçiş süresi (sn, hareket bulanıklığı için); opts geçişe özgü."""
    return TR[kind](a, b, k, g, d=d, **opts)


# ───────────────────────────── HUD ─────────────────────────────
PERDE_NAMES = {1: "ALTIN", 2: "BEDEL", 3: "MİRAS"}
PART_LABEL = {1: "PARÇA I — ALTIN", 2: "PARÇA II — BEDEL", 3: "PARÇA III — MİRAS"}
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


def part_title(f, t, part, t_in=1.2, t_out=4.8):
    """Parça 2/3 başlık bindirmesi (YONETMENLIK §9): ilk çekimin ÜZERİNDE (çekim hareketi sürer): yaldız "MEDİCİ" + alt satır "PARÇA II — BEDEL".
    t: parça başından saniye; t_in'de girer (0,9 sn açılım), t_out'ta çıkar (0,8 sn). Okunurluk için yumuşak koyu elips + yaldız gölgesi."""
    fi = smooth((t - t_in) / 0.9)
    fo = 1.0 - smooth((t - (t_out - 0.8)) / 0.8)
    a = fi * fo
    if a <= 0.003:
        return
    c = f.c
    cy = H * 0.455
    # okunurluk perdesi: yumuşak koyu elips (önbellekli radyal sprite)
    p = skia.Paint(AntiAlias=True, ColorFilter=skia.ColorFilters.Blend(C("#0C0905"), skia.BlendMode.kSrcIn))
    p.setAlphaf(0.62 * a)
    c.drawImageRect(_glow_img(256, 1.05), skia.Rect.MakeWH(256, 256), skia.Rect.MakeLTRB(W / 2 - 1000, cy - 270, W / 2 + 1000, cy + 300), _LS, p)
    rise = (1.0 - fi) * 16 - (1.0 - fo) * 12
    c.save()
    c.translate(0, rise)
    size = 176
    sp = CM.gilt("MEDİCİ", "title", size, size * 0.14)
    rv = smooth((t - t_in) / 1.0)
    gl = ((t - t_in - 1.0) * 0.55) % 2.6 if t > t_in + 1.0 else None
    CM.draw_spr(f, sp, W / 2, cy + size * 0.30, "c", alpha=a, reveal=clamp(rv * 1.15), glow=0.30 * a, shadow=0.75, glint=gl if (gl is not None and gl < 1) else None)
    ka = smooth((t - t_in - 0.55) / 0.7) * fo
    CM.flourish_rule(f, W / 2, cy + size * 0.30 + 44, 760, alpha=ka, color="#E9C770", grow=smooth((t - t_in - 0.55) / 0.9))
    lab = PART_LABEL.get(part, "")
    f.text(lab, W / 2 + 3, cy + size * 0.30 + 118, face="title_m", size=50, color="#F8EBC0", align="c", track=15, alpha=ka, shadow=(2, 3, 6, "#120C06"))
    c.restore()
