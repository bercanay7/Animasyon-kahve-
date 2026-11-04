"""cilt_medici — MEDICI belgeseli görsel dili ("FRESK ve DEFTER"): çekirdek.

Bu modül ortak motorun (sk/shots/compose) ÜSTÜNE oturur; kancalar minimaldir:
  * `shots.py` sonunda `import cilt_kinds` → eski türler (title/medal/doc/…) yeni cilde uyarlanmış sürümleriyle ÜZERİNE yazılır,
    yeni türler (ledger/coin/palle/letter/skyline/network/frieze/fresco_title/…) kaydolur.
  * `compose.py` HUD (yıl rulosu + perde), bölüm kartı, geçişler (yıkama/sayfa/giornata) ve `post()` için bu modülü çağırır.

İçerik: pigment paleti + tema (gün/gece × perde I–III), duvar çizimi + ışık, ince tane (tooth), parçacıklar,
yazı sprite'ları (oyma / boyalı / yaldız), levha-süs yardımcıları, kamera, `post()` renk derecelendirme.
Ana kural: tek ışık yönü (sol-üst), pigmentler duvara işler (düz renk bloğu yok), altın yalnız vurguda.
"""
import functools
import math
import os

import cv2
import numpy as np
import skia

import cilt_wall as CW
import donem as DN
import sk
from sk import C, Frame, H, W, clamp, ease_io, ease_out, lerp, mix, seg, smooth

HERE = os.path.dirname(os.path.abspath(__file__))

# ───────────────────────────── pigment paleti ─────────────────────────────
PIG = dict(
    LIME="#F2EBD9", BONE="#EAE1CA", PLASTER="#E3D9BF", PLASTER_D="#CBBE9C",
    INK="#18130E", INK_S="#2B2118", UMBER="#5A3B25", UMBER_D="#38210F", SEPIA="#7D5B38", SEPIA_L="#A78558",
    LAPIS="#233C8C", LAPIS_D="#16286A", LAPIS_N="#0B1230", LAPIS_L="#4468C0", AZURITE="#2F6A93",
    CINNABAR="#B33620", VERMILION="#CC4A2D", CINNABAR_D="#74201A", ROSE="#C48B7F", MADDER="#8E3342",
    OCHRE="#C79A3C", OCHRE_L="#E2BC5E", OCHRE_D="#8A6422", SIENA="#A8602C",
    TERRA="#7C8B58", TERRA_D="#46563A", TERRA_L="#A8B47E", MALACHITE="#3E7A5A",
    GOLD="#D2A33E", GOLD_L="#F4DE90", GOLD_D="#86601F", GOLD_DD="#4F3510",
    BRONZE="#9A6A3A", BRONZE_D="#4A2C14", PATINA="#5E8A78",
    WHITE="#FFFFFF", BLACK="#000000",
)
PG = PIG

# yaldız / bronz metal rampaları (relief_sprite için)
sk.METAL["gold"] = None  # (aşağıda yaprak rampasıyla değiştirilir)
sk.METAL["leaf"] = [("#6E4A16", 0.0), ("#BE8A2C", 0.22), ("#F7E2A0", 0.50), ("#D1A239", 0.74), ("#80571B", 1.0)]
sk.METAL["leaf_dim"] = [("#3B2810", 0.0), ("#8A6422", 0.30), ("#D0AA5A", 0.55), ("#8A6422", 0.80), ("#3B2810", 1.0)]
sk.METAL["bronze_med"] = [("#1E120A", 0.0), ("#4E3019", 0.22), ("#8A5C30", 0.46), ("#C9955A", 0.68), ("#EBC587", 0.88), ("#5A3A1C", 1.0)]
sk.METAL["lapis"] = [("#0B1236", 0.0), ("#1E3680", 0.30), ("#5C86D6", 0.56), ("#1E3680", 0.80), ("#0B1236", 1.0)]
sk.METAL["cinnabar"] = [("#3A0E0A", 0.0), ("#A22E1A", 0.32), ("#E8745A", 0.56), ("#A22E1A", 0.80), ("#3A0E0A", 1.0)]
sk.METAL["terra"] = [("#1E2A18", 0.0), ("#566A42", 0.32), ("#B2C08A", 0.56), ("#566A42", 0.80), ("#1E2A18", 1.0)]
sk.METAL["gold"] = sk.METAL["leaf"]           # tüm simgeler/madalyalar yeni yaldız rampasını kullanır
sk.METAL["bronze"] = sk.METAL["bronze_med"]


# ───────────────────────────── tema ─────────────────────────────
class Theme:
    """Şu anki çekimin modu ('day'|'night') ve perdesi (1|2|3). Renk yardımcıları buradan okunur."""

    def __init__(self, mode="day", perde=2):
        self.set(mode, perde)

    def set(self, mode="day", perde=2):
        self.mode, self.perde = mode, int(perde)
        d = mode == "day"
        self.day = d
        if d:
            self.fg = "#1B140D"          # birincil yazı: mürekkep
            self.fg2 = "#4A3420"         # ikincil: umber
            self.fg3 = "#6A5238"         # soluk etiket
            self.acc = {1: "#A5321F", 2: "#A8321E", 3: "#861B16"}[self.perde]       # sinabar
            self.acc2 = "#1F3A86"        # lapis
            self.rule = "#5B4126"
            self.plate = ("#EEE6CF", "#DCCFAE")
            self.plate_edge = "#7C5C2E"
            self.shadow = "#2A1C10"
            self.gold = "#B07F22"        # açık zeminde altın = koyu varak (yalnız süs)
            self.hi = "#FFF9E6"
        else:
            self.fg = "#F5EACB"
            self.fg2 = "#D5C69F"
            self.fg3 = "#AFA27C"
            self.acc = "#EDB968"
            self.acc2 = "#7FA3E8"
            self.rule = "#CBA550"
            self.plate = ("#1A2552", "#0E1636") if self.perde != 3 else ("#3A1519", "#220C0E")
            self.plate_edge = "#D8B25A"
            self.shadow = "#000000"
            self.gold = "#E8C468"
            self.hi = "#FFF3CC"


TH = Theme()


def use(mode="day", perde=2):
    TH.set(mode, perde)
    return TH


_MISSING = object()


def _pull_cam(name, cx, kw):
    """kw'dan yönetmenlik alanlarını (cam, link, longtake, montage; map için view=) ayıkla; cam spec'ini cx.cam_spec'e koy.
    map türünde cam=(lon,lat,zoom) (üç sayı) eski anlamıyla (harita görünümü) kw'da kalır."""
    import shots as SH
    if name == "map" and "view" in kw:
        kw["cam"] = kw.pop("view")
    spec = _MISSING
    if "cam" in kw:
        v = kw["cam"]
        if not (name == "map" and SH._is_map_view(v)):
            spec = kw.pop("cam")
    for k_ in ("link", "longtake", "montage"):             # çekim alanları: kw'dan ayıkla, cx'e de yaz (Shot'tan gelen değer ezilmez)
        v_ = kw.pop(k_, _MISSING)
        if v_ is not _MISSING:
            setattr(cx, k_, v_)
        elif not hasattr(cx, k_):
            setattr(cx, k_, getattr(getattr(cx, "sh", None), k_, None if k_ == "link" else False))
    if spec is _MISSING:
        return getattr(cx, "cam_spec", None)
    cx.cam_spec = spec
    return spec


def ckind(name):
    """@ckind('ad'): shots.KINDS'e kayıt; çekim parametrelerine mode='day'|'night', perde=1|2|3, seed= eklenir (Ctx'ten de okunur).
    Yönetmenlik alanları (cam, link, longtake, montage) kw'dan ayıklanır: cam → cx.cam_spec / cx.cam_state (cilt_cam); `CM.Cam` onu uygular.
    map türü için kamera mapsk.Cam yamasıyla, rack odak bulanıklığı çekim sonunda (postfx) uygulanır."""
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(cx, mode=None, perde=None, **kw):
            import cilt_cam as CAM
            m = mode or getattr(cx, "mode", None) or "day"
            p = perde or getattr(cx, "perde", None) or 2
            use(m, p)
            cx.mode, cx.perde = m, p
            cx.f.cilt_mode = m
            cx.f.cilt_perde = p
            DN.push(cx, name, kw)                              # dönem katmanı: bu çekimin yılı (cx.year; marka/çekim-listesi → None)
            try:
                spec = _pull_cam(name, cx, kw)
                nested = getattr(cx, "_cam_for", _MISSING) is spec and spec is not None
                if not nested:                                     # iç içe çağrıda (bir tür ötekini çağırırsa) durum yeniden hesaplanmaz
                    CAM.attach(cx, name, kw, fn)
                    cx._cam_for = spec
                if name == "map" and getattr(cx, "cam_state", None) is not None:
                    with CAM.map_patch(cx):
                        r = fn(cx, **kw)
                else:
                    r = fn(cx, **kw)
                if not nested:
                    CAM.postfx(cx)
            finally:
                DN.pop()
            return r
        import shots as SH
        SH.KINDS[name] = wrapper
        wrapper._raw = fn
        return wrapper
    return deco


# ───────────────────────────── duvar ─────────────────────────────
_IMG = {}


def _img(arr):
    return sk.np_to_image(np.ascontiguousarray(arr))


def wall_images(mode, perde, seed=0):
    key = (mode, perde, seed)
    if key not in _IMG:
        a = CW.wall_arrays(mode, perde, seed)
        _IMG[key] = {k: _img(v) for k, v in a.items()}
    return _IMG[key]


_LIN = skia.SamplingOptions(skia.FilterMode.kLinear)


def cam_xf(c, s=1.0, dx=0.0, dy=0.0, flip=False, cx=W / 2, cy=H / 2):
    c.translate(cx + dx, cy + dy)
    c.scale(-s if flip else s, s)
    c.translate(-cx, -cy)


def draw_wall(f, mode=None, perde=None, seed=0, s=1.0, dx=0.0, dy=0.0, flip=False):
    """Duvar ('lit' görüntü; gündüz ve gece aynı yapı). Işık/gölge `relight()` ile içerik üzerinden de uygulanır."""
    mode = mode or TH.mode
    perde = perde or TH.perde
    im = wall_images(mode, perde, seed)
    c = f.c
    c.save()
    cam_xf(c, s, dx, dy, flip)
    c.drawImage(im["lit"], -CW.MG, -CW.MG, _LIN)
    c.restore()


def candle_light(t, seed=0, base=(W * 0.5, H * 0.45), r=760.0, sway=22.0):
    """Mum ışığı havuzu parametreleri: titreşen yarıçap/şiddet + hafif savrulan merkez."""
    f1 = math.sin(t * 7.1 + seed) * 0.5 + math.sin(t * 11.3 + seed * 2.1) * 0.3 + math.sin(t * 2.3 + seed) * 0.4
    k = 1.0 + 0.045 * f1
    x = base[0] + math.sin(t * 0.6 + seed) * sway
    y = base[1] + math.cos(t * 0.5 + seed * 1.3) * sway * 0.5
    return (x, y, r * (1.0 + 0.03 * f1), k)


_VIG = {}


def vig(f, strength=None, mode=None, inner=0.38):
    """Önbellekli vinyet (gün: sıcak umber, gece: derin lacivert-siyah)."""
    mode = mode or TH.mode
    if strength is None:
        strength = 0.34 if mode == "day" else 0.72
    key = (mode, round(strength, 2), inner)
    if key not in _VIG:
        fr = Frame()
        fr.clear(skia.ColorTRANSPARENT)
        col = "#3A2A16" if mode == "day" else "#02040C"
        r = max(W, H) * 0.80
        sh = skia.GradientShader.MakeRadial((W / 2, H * 0.48), r, [C(col, 0), C(col, 0), C(col, int(255 * strength * 0.55)), C(col, int(255 * strength))],
                                            [0.0, inner, 0.72, 1.0])
        fr.c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))
        _VIG[key] = fr.surf.makeImageSnapshot()
    f.c.drawImage(_VIG[key], 0, 0)


_LAYER = {}


def _baked(key, builder):
    if key not in _LAYER:
        fr = Frame()
        fr.clear(skia.ColorTRANSPARENT)
        builder(fr)
        _LAYER[key] = fr.surf.makeImageSnapshot()
    return _LAYER[key]


def _day_overlay():
    """Gündüz ışığı tek önbellekli katman (SrcOver): sol-üst sıcak aydınlık + sağ-alt serin gölge + yumuşak pencere huzmeleri.
    40 px taşmalı (yavaş kayma için)."""
    def b(fr):
        e = 40
        fr.c.translate(e, e)
        sh = skia.GradientShader.MakeLinear([(W * 0.15, H * 0.05), (W * 0.95, H * 1.0)], [C("#6E6E80", 0), C("#6E6E80", 0), C("#575566", 120)], [0.0, 0.42, 1.0])
        fr.c.drawRect(skia.Rect.MakeLTRB(-e, -e, W + e, H + e), skia.Paint(Shader=sh))
        gl = skia.GradientShader.MakeRadial((W * 0.20, H * 0.12), W * 0.85, [C("#FFF0C8", 70), C("#FFF0C8", 28), C("#FFF0C8", 0)], [0.0, 0.5, 1.0])
        fr.c.drawRect(skia.Rect.MakeLTRB(-e, -e, W + e, H + e), skia.Paint(Shader=gl))
        rs = np.random.RandomState(4)
        fr.layer_begin(blur=26)
        for i in range(5):
            x0 = -120 + i * 190 + rs.rand() * 60
            wd = 70 + rs.rand() * 90
            pts = [(x0, -60), (x0 + wd, -60), (x0 + wd + 980, H + 80), (x0 + 980, H + 80)]
            shf = skia.GradientShader.MakeLinear([(x0, -60), (x0 + 980, H + 80)], [C("#FFF2CC", int(255 * 0.10 * (0.55 + 0.4 * rs.rand()))), C("#FFF2CC", 0)], [0, 1])
            fr.c.drawPath(sk.poly_path(pts), skia.Paint(Shader=shf, AntiAlias=True))
        fr.layer_end()
    fr = Frame(W + 80, H + 80)
    fr.clear(skia.ColorTRANSPARENT)
    b(fr)
    return fr.surf.makeImageSnapshot()


def daylight(f, k=1.0, t=0.0):
    """Gün ışığı (tek blit)."""
    img = _LAYER.get(("daylight",))
    if img is None:
        img = _LAYER[("daylight",)] = _day_overlay()
    p = skia.Paint()
    if k < 1:
        p.setAlphaf(k)
    f.c.drawImage(img, -40 + math.sin(t * 0.12) * 18, -40, skia.SamplingOptions(), p)


def shaft(f, t, alpha=0.10, mode=None):
    """(eski ad) huzmeler artık daylight() katmanında; gece için ışık huzmesi yok."""
    return


# ───────────────────────────── parçacıklar ─────────────────────────────
_DOT = {}


def _dot():
    if "d" not in _DOT:
        n = 48
        yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        r = np.hypot(xx - n / 2 + 0.5, yy - n / 2 + 0.5) / (n / 2)
        a = np.clip(1 - r, 0, 1) ** 1.6
        arr = np.dstack([np.full((n, n), 255, np.uint8)] * 3 + [(a * 255).astype(np.uint8)])
        _DOT["d"] = sk.np_to_image(arr)
    return _DOT["d"]


def motes(f, t, n=40, seed=2, mode=None, alpha=None, rect=None, speed=(5.0, 3.0)):
    """Süzülen toz/pigment benekleri. Gün: pigment kırıntıları (lapis/sinabar/oker, soluk); gece: sıcak toz (toplamsal)."""
    mode = mode or TH.mode
    rs = np.random.RandomState(seed)
    x0, y0, w, h = rect if rect else (0, 0, W, H)
    dot = _dot()
    src = skia.Rect.MakeWH(48, 48)
    pig = [PIG["LAPIS"], PIG["CINNABAR"], PIG["OCHRE"], PIG["UMBER"], PIG["TERRA"]]
    for i in range(n):
        d = 0.35 + rs.rand() * 0.65
        px = (rs.rand() * w + t * speed[0] * d + math.sin(t * 0.45 + i) * 14 * d) % w
        py = (rs.rand() * h + t * speed[1] * d + math.cos(t * 0.33 + i * 1.7) * 11 * d) % h
        rr = (2.2 + 5.5 * d) * (0.7 + 0.3 * math.sin(t * 1.1 + i))
        tw = 0.45 + 0.55 * abs(math.sin(t * 0.55 + i * 2.1))
        if mode == "night":
            col, a, bl = "#FFE0A6", (alpha if alpha is not None else 0.55) * d * tw, skia.BlendMode.kPlus
        else:
            col, a, bl = pig[i % len(pig)], (alpha if alpha is not None else 0.32) * d * tw, skia.BlendMode.kSrcOver
        p = skia.Paint(AntiAlias=True, ColorFilter=skia.ColorFilters.Blend(C(col), skia.BlendMode.kSrcIn), BlendMode=bl)
        p.setAlphaf(clamp(a))
        f.c.drawImageRect(dot, src, skia.Rect.MakeXYWH(x0 + px - rr, y0 + py - rr, rr * 2, rr * 2), _LIN, p)


def sparks(f, t, x, y, n=18, seed=3, h=260, alpha=0.8):
    """Mum/meşale kıvılcımı (yukarı süzülen)."""
    rs = np.random.RandomState(seed)
    dot, src = _dot(), skia.Rect.MakeWH(48, 48)
    for i in range(n):
        ph = (t * (0.10 + 0.12 * rs.rand()) + rs.rand()) % 1.0
        px = x + (rs.rand() - 0.5) * 70 + math.sin(t * 1.4 + i) * 22 * ph
        py = y - ph * h
        a = alpha * (1 - ph) * (0.5 + 0.5 * abs(math.sin(t * 5 + i)))
        rr = 3.0 + 3.0 * rs.rand()
        p = skia.Paint(AntiAlias=True, ColorFilter=skia.ColorFilters.Blend(C("#FFB55A"), skia.BlendMode.kSrcIn), BlendMode=skia.BlendMode.kPlus)
        p.setAlphaf(clamp(a))
        f.c.drawImageRect(dot, src, skia.Rect.MakeXYWH(px - rr, py - rr, rr * 2, rr * 2), _LIN, p)


# ───────────────────────────── kamera ─────────────────────────────
class Cam:
    """Çekim boyunca yavaş itme + kayma. içerik (s,dx,dy); duvar daha az hareket eder (paralaks).
    cx.cam_state varsa (shot(cam=…) verilmişse) tür varsayılanı (push/drift) yerine cilt_cam durumu uygulanır; yoksa davranış değişmez."""

    def __init__(self, cx, push=0.045, drift=(9.0, 4.0), base=1.0, ease=None, pivot=None):
        st = getattr(cx, "cam_state", None)
        self.state = st
        self.rot = 0.0
        if st is not None:
            self.s = base * st.s
            self.dx, self.dy = st.dx, st.dy
            self.rot = st.rot
            self.ws, self.wdx, self.wdy = st.ws, st.wdx, st.wdy
            self.pivot = st.pivot or pivot or (W / 2, H / 2)
            return
        carry = bool(getattr(cx, "cam_in", False) or getattr(cx, "cam_out", False))
        tt = cx.t if carry else clamp(cx.t, 0.0, cx.dur)  # geçişte çekim giriş öncesi (t<0) ve bitiş sonrası (t>dur) hareket sürer (doğrusal uzatma); aksi hâlde uçlarda sabit
        u = tt / max(1e-6, cx.dur)
        e = ease(u) if ease else u
        self.s = base * (1.0 + push * e)
        self.dx = drift[0] * (tt - cx.dur / 2)
        self.dy = drift[1] * (tt - cx.dur / 2)
        self.ws = 1.0 + push * 0.45 * e
        self.wdx, self.wdy = self.dx * 0.40, self.dy * 0.40
        self.pivot = pivot or (W / 2, H / 2)

    def wall(self, f, seed=0, flip=False):
        draw_wall(f, s=self.ws * 1.015, dx=self.wdx, dy=self.wdy, flip=flip, seed=seed)

    def begin(self, f, layer=1.0):
        """İçerik dönüşümünü uygula (layer: paralaks çarpanı; 1 = içerik). rot (derece) yalnız içeriğe: tam-kare döndürme pahalı (~90 ms), duvar dönmez."""
        c = f.c
        c.save()
        px, py = self.pivot
        s = 1.0 + (self.s - 1.0) * layer
        c.translate(px + self.dx * layer, py + self.dy * layer)
        if self.rot and layer:
            c.rotate(self.rot * layer)
        c.scale(s, s)
        c.translate(-px, -py)

    def end(self, f):
        f.c.restore()


# ───────────────────────────── post ─────────────────────────────
_TOOTH = {}
_GR = {}
_LUTS = {}


def _grain_bank(amp):
    if amp not in _GR:
        rs = np.random.RandomState(21)
        bank = []
        for _ in range(6):
            g = rs.randn(H // 2, W // 2).astype(np.float32)
            g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
            pos = np.clip(g * amp, 0, 255).astype(np.uint8)
            neg = np.clip(-g * amp, 0, 255).astype(np.uint8)
            bank.append((cv2.merge([pos, pos, pos]), cv2.merge([neg, neg, neg])))
        _GR[amp] = bank
    return _GR[amp]


def _lut(mode, perde):
    key = (mode, perde)
    if key not in _LUTS:
        x = np.arange(256, dtype=np.float32) / 255.0
        if mode == "day":
            contrast, lift = 1.05, 1.5
            y = np.clip((x - 0.5) * contrast + 0.5, 0, 1)
            y = np.clip(y + (lift / 255.0) * (1 - y), 0, 1)
            warm = {1: 0.020, 2: 0.012, 3: 0.034}[perde]
            r = np.clip(y * (1 + warm) + 0.002, 0, 1)
            g = y
            b = np.clip(y * (1 - warm * 1.7) + (0.010 * (1 - y)), 0, 1)
        else:
            contrast = 1.10
            y = np.clip((x - 0.46) * contrast + 0.46, 0, 1)
            y = y ** 1.04
            r = np.clip(y * (1.03 + (0.03 if perde == 3 else 0.0)) - 0.002, 0, 1)
            g = y
            b = np.clip(y * 0.96 + 0.012 * (1 - y), 0, 1)
        lut = np.stack([r, g, b], 1) * 255
        _LUTS[key] = np.ascontiguousarray(np.clip(lut, 0, 255).astype(np.uint8).reshape(256, 1, 3))
    return _LUTS[key]


def tooth_img(strength=1.0):
    if strength not in _TOOTH:
        t = CW.tooth(5, strength)
        _TOOTH[strength] = cv2.merge([t, t, t])
    return _TOOTH[strength]


def post(img, n=0, mode="day", perde=2, bloom=None, grain=1.35, tooth=1.0, fade=1.0):
    """img uint8 RGB (H,W,3) → uint8 RGB. Işıma (yumuşak diz eşikli) + renk derecelendirme + sıva tanesi (ekran-uzayı) + ince film greni (σ≈grain düzey)."""
    a = img
    thr, kb = (238, 0.16) if mode == "day" else (206, 0.24)
    if bloom is None:
        bloom = kb
    if bloom > 0:
        small = cv2.resize(a, (W // 8, H // 8), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
        mask = cv2.subtract(gray, thr)
        if cv2.countNonZero(mask) > 6:
            mask = cv2.multiply(mask, 255.0 / max(8, 255 - thr))
            hi = cv2.bitwise_and(small, small, mask=mask)
            hi = cv2.addWeighted(cv2.GaussianBlur(hi, (0, 0), 2.5), 0.7 * bloom, cv2.GaussianBlur(hi, (0, 0), 7.0), 0.7 * bloom, 0)
            up = cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR)
            a = cv2.add(a, up)
    a = cv2.LUT(a, _lut(mode, perde))
    if tooth > 0:
        a = cv2.multiply(a, tooth_img(tooth), scale=1.0 / 230.0)
    if grain > 0:
        pos, neg = _grain_bank(float(grain))[n % 6]
        a = cv2.add(a, pos)
        a = cv2.subtract(a, neg)
    if fade < 1.0:
        a = cv2.convertScaleAbs(a, alpha=max(0.0, fade))
    return a


# ───────────────────────────── yazı sprite'ları ─────────────────────────────
def _shade_map(h, k=1.0):
    gx = cv2.Sobel(h, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(h, cv2.CV_32F, 0, 1, ksize=3)
    return (0.55 * gx + 0.65 * gy) * k


def _crinkle(shape, seed=7, k=1.0):
    """Yaldız kâğıdı kırışıklığı dokusu (0..1)."""
    rs = np.random.RandomState(seed)
    h, w = shape
    a = CW.gn(rs, h, w, 2.2) * 0.6 + CW.gn(rs, h, w, 5.5) * 0.7 + CW.gn(rs, h, w, 1.2) * 0.3
    sh = _shade_map(a)
    sh = sh / (np.abs(sh).std() + 1e-6)
    return np.clip(0.5 + 0.24 * k * sh, 0, 1)


class Spr:
    """Önbellekli yazı sprite'ı: img, (ox,oy) taban çizgisi noktası, genişlik. Yumuşak gölge/ışıma görüntüleri tembel üretilir ve önbelleğe alınır
    (kare başına ImageFilter bulanıklığı yok)."""
    __slots__ = ("img", "ox", "oy", "w", "h", "wid", "alpha", "_sh", "_gl")

    def __init__(self, img, ox, oy, w, h, wid, alpha=None):
        self.img, self.ox, self.oy, self.w, self.h, self.wid, self.alpha = img, ox, oy, w, h, wid, alpha
        self._sh = self._gl = None

    def shadow_img(self):
        if self._sh is None:
            self._sh = blur_sil(self.alpha, max(1.5, self.h * 0.02), (0, 0, 0))
        return self._sh

    def glow_img(self, color=None):
        if self._gl is None:
            self._gl = {}
        key = color or "-"
        if key not in self._gl:
            self._gl[key] = blur_sil(self.alpha, self.h * 0.07, sk.rgb(color) if color else (255, 255, 255), keep_color=(color is None), src=self)
        return self._gl[key]


def blur_sil(alpha_u8, sigma, color=(0, 0, 0), keep_color=False, src=None):
    """alfa kanalından bulanık siluet görüntüsü (renk sabit; keep_color: kaynak sprite renklerini bulanıkla). Yerel biçimli skia.Image."""
    a = alpha_u8.astype(np.float32)
    ab = cv2.GaussianBlur(a, (0, 0), sigma)
    if keep_color and src is not None:
        rgba = src.img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType, alphaType=skia.AlphaType.kUnpremul_AlphaType)
        rgb = cv2.GaussianBlur(rgba[..., :3].astype(np.float32), (0, 0), sigma)
        arr = np.dstack([rgb, ab]).astype(np.uint8)
    else:
        arr = np.dstack([np.full(a.shape, color[0], np.uint8), np.full(a.shape, color[1], np.uint8), np.full(a.shape, color[2], np.uint8), np.clip(ab, 0, 255).astype(np.uint8)])
    return sk.np_to_image(arr)


@functools.lru_cache(maxsize=700)
def engraved(text, face="title", size=90, track=6.0, color="#1B140D", depth=1.0, lit=True):
    """Oyma (içe çökük) harf: sol-üst ışıkta sol-üst iç duvar gölgeli, sağ-alt iç duvar parlak; dışta ince parlak dudak."""
    pad = int(size * 0.35) + 8
    m, (ox, oy) = sk.text_mask(text, face, size, track, pad=pad)
    sig = max(0.7, size / 70.0)
    h = -cv2.GaussianBlur(m, (0, 0), sig) * depth
    sh = _shade_map(h, 1.0)
    sh = sh / (np.abs(sh).max() + 1e-6)
    r, g, b = sk.rgb(color)
    base = np.array([r, g, b], np.float32)
    k = 0.85 if lit else 0.4
    bright = np.clip(sh, 0, 1)[..., None]
    dark = np.clip(-sh, 0, 1)[..., None]
    col = base[None, None, :] * (1 - k * 0.55 * dark) + (255.0 - base)[None, None, :] * (k * 0.55) * bright
    a = np.clip(m, 0, 1)
    # dış alt-sağ parlak dudak
    s1 = max(1, int(round(size / 55)))
    shifted = np.roll(np.roll(m, s1, 0), s1, 1)
    lip = cv2.GaussianBlur(np.clip(shifted - m, 0, 1) * 0.55, (0, 0), 0.6)
    lipc = np.array([255, 250, 236], np.float32)
    ta = a + lip * (1 - a)
    rgb = (col * a[..., None] + lipc[None, None, :] * (lip * (1 - a))[..., None]) / np.clip(ta, 1e-4, 1)[..., None]
    arr = np.dstack([np.clip(rgb, 0, 255), np.clip(ta, 0, 1) * 255]).astype(np.uint8)
    wid = sk.text_width(text, face, size, track)
    return Spr(sk.np_to_image(arr), ox, oy, arr.shape[1], arr.shape[0], wid, arr[..., 3])


@functools.lru_cache(maxsize=700)
def painted(text, face="title", size=90, track=6.0, color="#A8321E", rough=1.0, seed=3):
    """Fresk boyası harf: kenarı hafif pürüzlü, pigment yoğunluğu değişken (sıvaya işlemiş)."""
    pad = int(size * 0.3) + 8
    m, (ox, oy) = sk.text_mask(text, face, size, track, pad=pad)
    rs = np.random.RandomState(seed)
    nz = CW.gn(rs, m.shape[0], m.shape[1], max(1.0, size / 40.0))
    mb = cv2.GaussianBlur(m, (0, 0), max(0.8, size / 90.0))
    mr = np.clip((mb + nz * 0.07 * rough - 0.5) * 6 + 0.5, 0, 1)
    mr = np.clip(mr * 0.5 + m * 0.5, 0, 1)
    dens = 1 + 0.08 * CW.gn(rs, m.shape[0], m.shape[1], 3.0) + 0.05 * nz
    r, g, b = sk.rgb(color)
    rgb = np.clip(np.array([r, g, b], np.float32)[None, None, :] * dens[..., None], 0, 255)
    arr = np.dstack([rgb, np.clip(mr * 0.96, 0, 1) * 255]).astype(np.uint8)
    wid = sk.text_width(text, face, size, track)
    return Spr(sk.np_to_image(arr), ox, oy, arr.shape[1], arr.shape[0], wid, arr[..., 3])


@functools.lru_cache(maxsize=300)
def gilt(text, face="title", size=120, track=8.0, metal="leaf", spec=0.85, bevel=None):
    """Altın varak harf: kırışık doku + kenarlarda kırmızı bol (bole) izi + sert özgül parlama."""
    pad = int(size * 0.3) + 10
    m, (ox, oy) = sk.text_mask(text, face, size, track, pad=pad)
    tex = _crinkle(m.shape, 11, 1.0)
    bev = bevel or max(1.4, size / 32.0)
    spr = sk.relief_sprite(m, metal, bevel=bev, strength=1.05, spec=spec, tex=tex)
    # bole: kenara yakın pikseller kırmızımsı kahve
    mb = cv2.GaussianBlur(m, (0, 0), max(1.0, size / 80.0))
    edge = np.clip(1.0 - mb * 1.35, 0, 1) * (m > 0.05)
    bole = np.array([138, 58, 34], np.float32)
    rgb = spr[..., :3].astype(np.float32)
    rgb = rgb * (1 - edge[..., None] * 0.28) + bole * edge[..., None] * 0.28
    spr[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    wid = sk.text_width(text, face, size, track)
    return Spr(sk.np_to_image(spr), ox, oy, spr.shape[1], spr.shape[0], wid, spr[..., 3])


def draw_spr(f, spr, x, y, align="c", alpha=1.0, scale=1.0, glow=0.0, reveal=None, glow_color=None, shadow=0.0, glint=None):
    """Sprite'ı taban çizgisi (x,y) noktasına çiz. reveal: 0..1 soldan açılım (yumuşak kenar). shadow: alt-sağ yumuşak gölge şiddeti."""
    c = f.c
    sx = x - (spr.wid / 2 if align == "c" else spr.wid if align == "r" else 0) * scale
    c.save()
    c.translate(sx, y)
    c.scale(scale, scale)
    c.translate(-spr.ox, -spr.oy)
    if reveal is not None and reveal < 1.0:
        if reveal <= 0:
            c.restore()
            return
        x_edge = (spr.ox + spr.wid * reveal)
        c.saveLayer(skia.Rect.MakeWH(spr.w, spr.h), None)
    if shadow > 0:
        pp = skia.Paint(AntiAlias=True)
        pp.setAlphaf(clamp(0.55 * shadow * alpha))
        c.drawImage(spr.shadow_img(), spr.h * 0.012, spr.h * 0.02, _LIN, pp)
    if glow > 0:
        gp = skia.Paint(AntiAlias=True)
        gp.setAlphaf(clamp(glow * alpha))
        c.drawImage(spr.glow_img(glow_color), 0, 0, _LIN, gp)
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(alpha))
    c.drawImage(spr.img, 0, 0, _LIN, p)
    if glint is not None and 0.0 <= glint <= 1.0:
        # parlama: yalnız dar bir bant içinde (saveLayer + SrcATop yalnız bu bantta → ucuz)
        bw = spr.h * 0.34
        gx = -spr.h * 0.5 + (spr.w + spr.h) * glint
        L_, R_ = max(0.0, gx - bw), min(float(spr.w), gx + bw)
        if R_ > L_:
            c.save()
            c.clipRect(skia.Rect.MakeLTRB(L_, 0, R_, spr.h))
            c.saveLayer(skia.Rect.MakeLTRB(L_, 0, R_, spr.h), None)
            c.drawImage(spr.img, 0, 0, _LIN, skia.Paint(AntiAlias=True))
            sh = skia.GradientShader.MakeLinear([(gx - bw * 0.7, 0), (gx + bw * 0.25, spr.h * 0.5)], [C("#FFFFFF", 0), C("#FFF2C0", int(125 * alpha)), C("#FFFFFF", 0)], [0, 0.5, 1])
            c.drawRect(skia.Rect.MakeLTRB(L_, 0, R_, spr.h), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kSrcATop))
            c.restore()
            c.restore()
    if reveal is not None and reveal < 1.0:
        fw = max(8.0, spr.h * 0.25)
        sh = skia.GradientShader.MakeLinear([(x_edge - fw, 0), (x_edge, 0)], [skia.ColorBLACK, skia.ColorTRANSPARENT], [0, 1])
        # DstIn: x_edge solu görünür, sağı silinir
        mask_p = skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kDstIn)
        c.drawRect(skia.Rect.MakeLTRB(0, 0, x_edge, spr.h), mask_p)
        c.drawRect(skia.Rect.MakeLTRB(x_edge, 0, spr.w, spr.h), skia.Paint(Color=skia.ColorTRANSPARENT, BlendMode=skia.BlendMode.kClear))
        c.restore()
    c.restore()
    return spr.wid * scale


def spr_wid(spr, scale=1.0):
    return spr.wid * scale


# ───────────────────────────── metin kısayolları ─────────────────────────────
# ───────────────────────────── kontrast zemini (TE2) ─────────────────────────────
AUTO_SCRIM = True           # ink(): serbest yazının arka planı ölçülür; kontrast hedefin altındaysa yumuşak zemin (levha üstündeki yazıda zaten tetiklenmez)
KICK_SCRIM = True           # kick(): serbest büyük-harf etiketler
SCRIM_SMALL, SCRIM_LARGE, SCRIM_LARGE_PX = 4.5, 3.0, 46.0     # hedef oranlar (WCAG); ≥46 px (ekran) "büyük yazı"
SCRIM_LOG = []              # LOG_TEXT iken tetiklenen zeminler (qa_yerlesim)


def _hex_rgb(col):
    if isinstance(col, str) and col.startswith("#") and len(col) in (7, 9):
        return int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)
    return None


def _lin_c(v):
    v = v / 255.0
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def rel_lum(rgb):
    """WCAG göreli parlaklık (sRGB 0..255)."""
    r, g, b = rgb
    return 0.2126 * _lin_c(r) + 0.7152 * _lin_c(g) + 0.0722 * _lin_c(b)


def contrast_ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


_LUT_LIN = np.array([_lin_c(v) for v in range(256)], np.float32)


def contrast_scrim(f, x0, y0, x1, y1, color, size, alpha=1.0, force=False):
    """Yazı kutusunun (yerel) arkasındaki GERÇEK pikselleri ölç; yazı rengiyle kontrast hedefin (küçük 4,5:1, büyük 3:1) altındaysa
    kutunun arkasına yumuşak kenarlı koyu (açık yazı) / açık (koyu yazı) zemin çiz. Dönüş: (ölçülen oran, zemin alfası)."""
    rgb = _hex_rgb(color)
    if rgb is None:
        return None, 0.0
    try:
        M = f.c.getTotalMatrix()
        sc = math.sqrt(abs(M.getScaleX() * M.getScaleY() - M.getSkewX() * M.getSkewY()))
        l, t_, r, b = device_rect(f, x0, y0, x1, y1)
        fsx, fsy = _frame_scale(f)
        fw, fh = getattr(f, "w", W), getattr(f, "h", H)
        L_, T_ = int(max(0, l * fsx)), int(max(0, t_ * fsy))
        R_, B_ = int(min(fw, r * fsx)), int(min(fh, b * fsy))
        if R_ - L_ < 4 or B_ - T_ < 4:
            return None, 0.0
        img = f.surf.makeImageSnapshot(skia.IRect.MakeLTRB(L_, T_, R_, B_))
        arr = img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
    except Exception:                                      # noqa: BLE001
        return None, 0.0
    if arr is None or arr.size == 0:
        return None, 0.0
    if arr.shape[0] > 24 or arr.shape[1] > 96:
        arr = cv2.resize(arr, (min(96, arr.shape[1]), min(24, arr.shape[0])), interpolation=cv2.INTER_AREA)
    lum = 0.2126 * _LUT_LIN[arr[..., 0]] + 0.7152 * _LUT_LIN[arr[..., 1]] + 0.0722 * _LUT_LIN[arr[..., 2]]
    lt = rel_lum(rgb)
    light_text = lt > 0.30
    lb = float(np.percentile(lum, 80 if light_text else 20))
    cr = contrast_ratio(lt, lb)
    target = SCRIM_LARGE if size * sc / fsx >= SCRIM_LARGE_PX else SCRIM_SMALL
    if cr >= target and not force:
        return cr, 0.0
    if light_text:
        scol, ls = "#120C07", rel_lum((18, 12, 7))
        lmax = (lt + 0.05) / target - 0.05
        need = (lb - lmax) / max(1e-4, lb - ls)
    else:
        scol, ls = "#F6EEDA", rel_lum((246, 238, 218))
        lmin = (lt + 0.05) * target - 0.05
        need = (lmin - lb) / max(1e-4, ls - lb)
    a_s = clamp(need * 1.18 + 0.06, 0.0, 0.88)
    if a_s <= 0.01:
        return cr, 0.0
    hh = y1 - y0
    px, py = hh * 0.55, hh * 0.30
    rad = hh * 0.45
    p = skia.Paint(AntiAlias=True, Color=C(scol), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, max(2.0, hh * 0.28)))
    p.setAlphaf(clamp(a_s * alpha))
    f.c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x0 - px, y0 - py, x1 + px, y1 + py), rad, rad), p)
    if LOG_TEXT:
        SCRIM_LOG.append(dict(box=(round(l, 1), round(t_, 1), round(r, 1), round(b, 1)), ratio=round(cr, 2), target=target, a=round(a_s, 3),
                              g=round(float(getattr(getattr(DN.current(), "cx", None), "g", 0.0) or 0.0), 3) if DN.current() else None))
    return cr, a_s


def _log_text(f, typ, text, x0, y0, x1, y1, size=0.0, alpha=1.0, color=None):
    """LOG_TEXT iken yazı/levha kutusunu ekran uzayında kaydet (qa_yerlesim)."""
    if not LOG_TEXT or alpha < 0.30:
        return
    try:
        M = f.c.getTotalMatrix()
        sc = math.sqrt(abs(M.getScaleX() * M.getScaleY() - M.getSkewX() * M.getSkewY()))
        box = device_rect(f, x0, y0, x1, y1)
    except Exception:                                      # noqa: BLE001
        return
    fr = DN.current()
    cx = fr.cx if fr else None
    sh = getattr(cx, "sh", None)
    fw, fh = getattr(f, "w", W), getattr(f, "h", H)
    TEXT_LOG.append(dict(type=typ, text=text, size=round(size * sc / _frame_scale(f)[0], 1), box=tuple(round(v, 1) for v in box), alpha=round(alpha, 2),
                         color=color, main=not (abs(fw * H - fh * W) > 2 or fw < W * 0.25), kind=(fr.kind if fr else None),
                         shot=getattr(sh, "i", None), label=getattr(sh, "label", None), g=round(float(getattr(cx, "g", 0.0)), 3) if cx is not None else None))


def ink(f, text, x, y, face="cap", size=44, color=None, align="l", track=0.0, alpha=1.0, emboss=True, log=True, scrim=None):
    """Duvara işlenmiş yazı: vektör metin; gündüz hafif parlak alt dudak, gece hafif gölge.
    scrim: None → modül ayarı (AUTO_SCRIM) · 'auto'/True → arka plan kontrastı ölçülür, hedefin altındaysa yumuşak koyu/açık zemin · False → yok."""
    color = color or TH.fg
    if not text:
        return 0.0
    blob, wid = sk.text_blob(face, text, size, track)
    ox = x - (wid / 2 if align == "c" else wid if align == "r" else 0)
    c = f.c
    if log and LOG_TEXT:
        _log_text(f, "ink", text, ox, y - size * 0.80, ox + wid, y + size * 0.24, size, alpha, color)
    if scrim is None:
        scrim = AUTO_SCRIM
    if scrim and alpha > 0.02:
        contrast_scrim(f, ox, y - size * 0.80, ox + wid, y + size * 0.24, color, size, alpha)
    if emboss and TH.day:
        c.save(); c.translate(ox + 0.8, y + 1.3)
        c.drawTextBlob(blob, 0, 0, f.paint("#FFF8E4", alpha=0.55 * alpha))
        c.restore()
    elif emboss:
        c.save(); c.translate(ox + 1.5, y + 2.5)
        c.drawTextBlob(blob, 0, 0, f.paint("#000000", alpha=0.55 * alpha, blur=2.0))
        c.restore()
    c.save(); c.translate(ox, y)
    c.drawTextBlob(blob, 0, 0, f.paint(color, alpha=alpha))
    c.restore()
    return wid


def kick(f, text, x, y, alpha=1.0, size=30, track=10, align="c", face="title_m", color=None, scrim=None):
    """Küçük büyük-harf etiket (Cinzel). Serbest etiket olduğundan kontrast zemini varsayılan olarak AÇIK (scrim=None → KICK_SCRIM)."""
    return ink(f, text, x, y, face=face, size=size, color=color or TH.fg2, align=align, track=track, alpha=alpha, scrim=KICK_SCRIM if scrim is None else scrim)


def fit_size(text, face, size, max_w, track=0.0):
    w = sk.text_width(text, face, size, track)
    return size if w <= max_w else size * max_w / w


# ───────────────────────────── süs / levha ─────────────────────────────
def wobble(paint, seg=9.0, dev=1.3, seed=0):
    paint.setPathEffect(skia.DiscretePathEffect.Make(seg, dev, seed))
    return paint


def rule(f, x0, y0, x1, y1, color=None, sw=2.0, alpha=1.0, wob=1.0, seed=0):
    """El çizimi ince çizgi."""
    p = f.paint(color or TH.rule, style="stroke", sw=sw, alpha=alpha, cap="round")
    wobble(p, 10.0, 0.9 * wob, seed)
    f.c.drawLine(x0, y0, x1, y1, p)


def diamond(f, x, y, r, color=None, alpha=1.0):
    f.poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], color=color or TH.rule, alpha=alpha)


def flourish_rule(f, x, y, w, alpha=1.0, color=None, grow=1.0):
    """Ortada baklava, iki yana incelen çizgi (oyma başlık altı süsü)."""
    color = color or TH.rule
    ww = w * 0.5 * clamp(grow)
    if ww <= 0:
        return
    for sgn in (-1, 1):
        sh = skia.GradientShader.MakeLinear([(x, y), (x + sgn * ww, y)], [C(color, int(255 * alpha)), C(color, 0)], [0.0, 1.0])
        f.c.drawRect(skia.Rect.MakeLTRB(min(x, x + sgn * ww), y - 1.2, max(x, x + sgn * ww), y + 1.2), skia.Paint(Shader=sh))
    diamond(f, x, y, 7, color, alpha)
    f.circle(x - 22, y, 2.6, color=color, alpha=alpha * 0.9)
    f.circle(x + 22, y, 2.6, color=color, alpha=alpha * 0.9)


def tablet(f, x, y, w, h, alpha=1.0, rot=0.0, edge=None, fill=None, shadow=True, corner=10, border=True, log=True):
    """Boyalı sıva levha (isim/etiket): ılık dolgu, çift ince çerçeve, köşe benekleri; gündüz krem, gece lacivert."""
    edge = edge or TH.plate_edge
    c = f.c
    if log and LOG_TEXT and not rot:
        _log_text(f, "tablet", None, x, y, x + w, y + h, 0.0, alpha)
    c.save()
    c.translate(x + w / 2, y + h / 2)
    if rot:
        c.rotate(math.degrees(rot))
    c.translate(-w / 2, -h / 2)
    if shadow:
        f.rrect(5, 8, w, h, corner + 2, color="#000000", alpha=(0.30 if TH.day else 0.55) * alpha, blur=9)
    top, bot = fill or TH.plate
    f.rrect(0, 0, w, h, corner, shader=f.lin(0, 0, 0, h, [(top, 0.0), (bot, 1.0)]), alpha=alpha)
    # sıva tanesi (levha üstü hafif benek)
    if TH.day:
        f.rrect(0, 0, w, h, corner, style="stroke", sw=9, color="#7A5A2E", alpha=0.10 * alpha)
    if border:
        p = f.paint(edge, style="stroke", sw=2.8, alpha=0.95 * alpha)
        wobble(p, 14.0, 0.8, 3)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, 0, w, h), corner, corner), p)
        p2 = f.paint(edge, style="stroke", sw=1.2, alpha=0.65 * alpha)
        wobble(p2, 14.0, 0.7, 5)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(9, 9, w - 18, h - 18), max(2, corner - 5), max(2, corner - 5)), p2)
        for (cx_, cy_) in ((9, 9), (w - 9, 9), (9, h - 9), (w - 9, h - 9)):
            f.circle(cx_, cy_, 3.2, color=edge, alpha=0.9 * alpha)
    c.restore()


# ───────────────────────────── yerleşim güvencesi (ekran uzayı) ─────────────────────────────
SAFE_RECT = (90.0, 60.0, 1830.0, 1020.0)          # yazı/levha güvenli alanı (1920×1080 ekran uzayı; STİL_REHBERİ: kenardan ≥90 px)
HUD_RECT_DEFAULT = (1480.0, 10.0, 1900.0, 118.0)  # cilt_fx.HUD_RECT yoksa (ENG-B HUD'u küçültünce kendi sabitini tanımlar; burada yalnız okunur)
HUD_GAP = 14.0                                    # levha–HUD arası en az boşluk (px)
SUB_BAND = (938.0, 1042.0)                        # altyazı şeridi (y) — yalnız denetim için
LOG_PLATES = False                                # True: her çizilen isim levhası PLATE_LOG'a (qa_yerlesim)
PLATE_LOG = []
LOG_TEXT = False                                  # True: ink/kick/stamp/tablet ekran kutuları TEXT_LOG'a (qa_yerlesim --yazi)
TEXT_LOG = []


def hud_rect():
    """HUD dikdörtgeni (ekran uzayı): cilt_fx.HUD_RECT (ENG-B) ya da varsayılan."""
    r = None
    try:
        import cilt_fx
        r = getattr(cilt_fx, "HUD_RECT", None)
    except Exception:                                      # noqa: BLE001 — döngüsel içe aktarma sırasında
        r = None
    try:
        return tuple(float(v) for v in (r or HUD_RECT_DEFAULT))[:4]
    except (TypeError, ValueError):
        return HUD_RECT_DEFAULT


def _frame_scale(f):
    return (getattr(f, "w", W) or W) / float(W), (getattr(f, "h", H) or H) / float(H)


def device_rect(f, x0, y0, x1, y1):
    """Yerel (tuval) dikdörtgen → ekran uzayı sınırlayıcı kutu (l, t, r, b), 1920×1080 ölçeğinde."""
    r = f.c.getTotalMatrix().mapRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    sx, sy = _frame_scale(f)
    return (r.left() / sx, r.top() / sy, r.right() / sx, r.bottom() / sy)


def _hits(a, b, g=0.0):
    return a[2] > b[0] - g and a[0] < b[2] + g and a[3] > b[1] - g and a[1] < b[3] + g


def screen_fit(f, x0, y0, x1, y1, avoid_hud=True, safe=None):
    """Kamera dönüşümü altındaki yerel dikdörtgenin EKRAN UZAYINDAKİ son yerini güvenli alana ve HUD dışına kıstırır.
    Dönüş: (dx, dy, k, info) — yerel öteleme + dikdörtgen merkezine göre ölçek (k ≤ 1; yalnız kutu güvenli alandan büyükse).
    Önce merkez korunur, taşan kenar içeri kaydırılır; HUD ile kesişirse aşağı ya da sola (küçük yer değiştirme) itilir."""
    M = f.c.getTotalMatrix()
    sx, sy = _frame_scale(f)
    S = safe or SAFE_RECT
    SL, ST, SR, SB = S
    l, t_, r, b = device_rect(f, x0, y0, x1, y1)
    req = (l, t_, r, b)
    dw, dh = r - l, b - t_
    k = min(1.0, (SR - SL) / max(1e-6, dw), (SB - ST) / max(1e-6, dh))
    if k < 1.0:
        cxm, cym = (l + r) / 2, (t_ + b) / 2
        dw, dh = dw * k, dh * k
        l, r, t_, b = cxm - dw / 2, cxm + dw / 2, cym - dh / 2, cym + dh / 2
    ddx = (SL - l) if l < SL else ((SR - r) if r > SR else 0.0)
    ddy = (ST - t_) if t_ < ST else ((SB - b) if b > SB else 0.0)
    l, r, t_, b = l + ddx, r + ddx, t_ + ddy, b + ddy
    hud_hit = False
    if avoid_hud:
        hr = hud_rect()
        g = HUD_GAP
        if _hits((l, t_, r, b), hr, g):
            hud_hit = True
            down = (hr[3] + g) - t_
            left = (hr[0] - g) - r
            cand = []
            if b + down <= SB + 0.5:
                cand.append((abs(down), 0.0, down))
            if l + left >= SL - 0.5:
                cand.append((abs(left), left, 0.0))
            if not cand:
                cand.append((abs(down), 0.0, down))
            _, ex, ey = min(cand)
            ddx += ex
            ddy += ey
            l, r, t_, b = l + ex, r + ex, t_ + ey, b + ey
    dx = dy = 0.0
    if ddx or ddy:
        inv = skia.Matrix()
        if M.invert(inv):
            v = inv.mapVector(ddx * sx, ddy * sy)
            dx, dy = v.x(), v.y()
    return dx, dy, k, dict(req=req, box=(l, t_, r, b), moved=(ddx, ddy), k=k, hud=hud_hit)


PLATE_PAD = 55.0            # isim satırı yatay iç payı (her yan) — eski davranış: wn + 110
PLATE_SUB_PAD = 40.0        # rol / yıl satırı yatay iç payı (her yan)
PLATE_MIN_TITLE = 34.0      # çok uzun adda Cinzel isim en çok buraya kadar küçülür (okunurluk tabanı)


def plate_layout(name, role=None, dates=None, w=None, name_font=("title_m", 50.0, 5.0), role_font=("cap_i", 34.0, 0.0), dates_font=("cap", 30.0, 3.0),
                 min_w=460.0, line_h=(104.0, 44.0, 40.0)):
    """İsim levhası ölçüleri: `w` artık ALT SINIR (kutu metin + paydan küçük olamaz); çok uzun metin güvenli alana sığmazsa yazı `fit_size` ile
    küçülür (isim ≥34 px). Dönüş: dict(ww, hh, nsz, rsz, dsz, wn, wr, wd)."""
    max_w = SAFE_RECT[2] - SAFE_RECT[0]
    nf, ns, ntr = name_font
    nsz = ns
    wn = sk.text_width(name, nf, nsz, ntr) if name else 0.0
    if wn + 2 * PLATE_PAD > max_w:
        nsz = max(PLATE_MIN_TITLE, fit_size(name, nf, ns, max_w - 2 * PLATE_PAD, ntr))
        wn = sk.text_width(name, nf, nsz, ntr)
    rsz = dsz = 0.0
    wr = wd = 0.0
    if role:
        rf, rs_, rtr = role_font
        rsz = max(26.0, fit_size(role, rf, rs_, max_w - 2 * PLATE_SUB_PAD, rtr))
        wr = sk.text_width(role, rf, rsz, rtr)
    if dates:
        df, ds_, dtr = dates_font
        dsz = max(24.0, fit_size(dates, df, ds_, max_w - 2 * PLATE_SUB_PAD, dtr))
        wd = sk.text_width(dates, df, dsz, dtr)
    base = float(w) if w else float(min_w)
    ww = max(base, wn + 2 * PLATE_PAD, (wr + 2 * PLATE_SUB_PAD) if role else 0.0, (wd + 2 * PLATE_SUB_PAD) if dates else 0.0)
    hh = line_h[0] + (line_h[1] if role else 0.0) + (line_h[2] if dates else 0.0)
    return dict(ww=ww, hh=hh, nsz=nsz, rsz=rsz, dsz=dsz, wn=wn, wr=wr, wd=wd)


def _log_plate(f, name, role, dates, L, info, w_req):
    if not LOG_PLATES:
        return
    fr = DN.current()
    cx = fr.cx if fr else None
    sh = getattr(cx, "sh", None)
    PLATE_LOG.append(dict(text=name, role=role, dates=dates, w_req=w_req, ww=round(L["ww"], 1), hh=round(L["hh"], 1),
                          nsz=round(L["nsz"], 1), wn=round(L["wn"], 1), wr=round(L["wr"], 1), wd=round(L["wd"], 1),
                          box=tuple(round(v, 1) for v in info["box"]), req=tuple(round(v, 1) for v in info["req"]),
                          moved=tuple(round(v, 1) for v in info["moved"]), k=round(info["k"], 3), hud=info["hud"],
                          main=bool(info.get("main", True)), kind=(fr.kind if fr else None), shot=getattr(sh, "i", None), label=getattr(sh, "label", None),
                          g=round(float(getattr(cx, "g", 0.0)), 3) if cx is not None else None, t=round(float(getattr(cx, "t", 0.0)), 3) if cx is not None else None))


def plate_place(f, cx_, y, L, avoid_hud=True):
    """Levha kutusunun (son konum, t=1) ekran kıskacı. Ana kare (1920×1080 oranlı) değilse kıskaç yok. Dönüş: (dx, dy, k, info)."""
    x0, y0 = cx_ - L["ww"] / 2, y
    fw, fh = getattr(f, "w", W), getattr(f, "h", H)
    if abs(fw * H - fh * W) > 2 or fw < W * 0.25:
        l, t_, r, b = device_rect(f, x0, y0, x0 + L["ww"], y0 + L["hh"])
        return 0.0, 0.0, 1.0, dict(req=(l, t_, r, b), box=(l, t_, r, b), moved=(0.0, 0.0), k=1.0, hud=False, main=False)
    return screen_fit(f, x0, y0, x0 + L["ww"], y0 + L["hh"], avoid_hud=avoid_hud)


def name_plate(f, name, role=None, dates=None, cx_=W / 2, y=800, alpha=1.0, w=None, t=1.0, avoid_hud=True):
    """Madalya/portre altı isim levhası (Cinzel isim, Cormorant italik rol, yıllar). t: açılış 0..1.
    `w` ALT SINIRDIR (kutu metinden dar olamaz); son kutu EKRAN UZAYINDA güvenli alana (x∈[90,1830], y∈[60,1020]) ve HUD dışına kıstırılır
    (kamera itmesi/kayması hesaba katılır; gerekirse levha küçülür). LOG_PLATES iken kutu PLATE_LOG'a yazılır."""
    a = alpha * smooth(t)
    if a <= 0:
        return
    L = plate_layout(name, role, dates, w)
    ww, hh = L["ww"], L["hh"]
    dx, dy, k, info = plate_place(f, cx_, y, L, avoid_hud)
    if a > 0.05:
        _log_plate(f, name, role, dates, L, info, w)
    c = f.c
    c.save()
    if dx or dy:
        c.translate(dx, dy)
    if k < 0.999:
        c.translate(cx_, y + hh / 2)
        c.scale(k, k)
        c.translate(-cx_, -(y + hh / 2))
    x = cx_ - ww / 2
    yy = y + (1 - smooth(t)) * 16
    tablet(f, x, yy, ww, hh, alpha=a, log=False)
    ink(f, name, cx_, yy + 66, face="title_m", size=L["nsz"], color=TH.fg, align="c", track=5, alpha=a, log=False)
    yb = yy + 66
    if role:
        yb += 44
        ink(f, role, cx_, yb, face="cap_i", size=L["rsz"], color=TH.fg2, align="c", alpha=a, log=False)
    if dates:
        yb += 40
        ink(f, dates, cx_, yb, face="cap", size=L["dsz"], color=TH.fg3, align="c", track=3, alpha=a * 0.95, log=False)
    c.restore()


def stamp(f, text, x, y, rot=-0.10, size=56, color=None, alpha=1.0, t=1.0):
    """Sinabar damga (RİVAYET, TARTIŞMALI …): lapis/sinabar mürekkep, aşınmış kenar; t: çarpma animasyonu."""
    if t <= 0:
        return
    color = color or (TH.acc if TH.day else "#E56A52")
    sc = 1.0 + (1 - sk.back_out(t)) * 0.8 if t < 1 else 1.0
    a = alpha * min(1.0, t * 3)
    wd = sk.text_width(text, "title", size, 7) + 64
    c = f.c
    c.save(); c.translate(x, y); c.rotate(math.degrees(rot)); c.scale(sc, sc)
    for dy_, sw, aa in ((0, 5.5, 0.88), (0, 2.0, 0.8)):
        pad = 0 if sw > 3 else 9
        p = f.paint(color, style="stroke", sw=sw, alpha=aa * a)
        wobble(p, 7.0, 0.9, 7)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-wd / 2 + pad, -size * 0.86 + pad, wd - 2 * pad, size * 1.52 - 2 * pad), 8, 8), p)
    sp = painted(text, "title", int(size), 7.0, color, 1.4, 11)
    draw_spr(f, sp, 0, size * 0.28, align="c", alpha=0.94 * a)
    c.restore()


def wax_seal(f, x, y, r=54, color="#A52A1C", alpha=1.0, t=1.0, mono=None, palle=False):
    """Balmumu mühür: düzensiz kenarlı kırmızı damla, iç halka, ortada harf ya da palle izi."""
    if t <= 0:
        return
    sc = 1.0 + (1 - sk.back_out(t)) * 0.55 if t < 1 else 1.0
    a = alpha * min(1.0, t * 4)
    c = f.c
    c.save(); c.translate(x, y); c.scale(sc, sc)
    f.circle(4, 9, r * 1.08, color="#000000", alpha=0.42 * a, blur=7)
    pts = [(math.cos(i * 0.4488 + 0.3) * r * (1 + 0.075 * math.sin(i * 3.1 + 1) + 0.04 * math.sin(i * 7.3)),
            math.sin(i * 0.4488 + 0.3) * r * (1 + 0.075 * math.cos(i * 2.3) + 0.04 * math.sin(i * 5.9))) for i in range(14)]
    path = sk.smooth_path(pts, True, 0.55)
    f.path(path, shader=f.rad(-r * 0.32, -r * 0.34, r * 1.7, [(mix(color, "#FFFFFF", 0.38), 0.0), (color, 0.45), (mix(color, "#000000", 0.55), 1.0)]), alpha=a)
    f.circle(0, 0, r * 0.68, style="stroke", sw=3.2, color=mix(color, "#000000", 0.45), alpha=0.85 * a)
    f.circle(0, 0, r * 0.68 + 2.5, style="stroke", sw=1.6, color=mix(color, "#FFFFFF", 0.45), alpha=0.55 * a)
    if palle:
        mini_palle(f, 0, 0, r * 1.05, mono=True, color=mix(color, "#000000", 0.5), alpha=0.9 * a)
    elif mono:
        f.text(mono, 0, r * 0.28, face="title", size=r * 0.95, color=mix(color, "#000000", 0.5), align="c", alpha=0.9 * a)
    c.restore()


def mini_palle(f, x, y, s, mono=False, color="#7A2018", alpha=1.0):
    """Küçük altı-top (palle) şeması; mono=True mühür/oyuk için tek renk."""
    for (dx, dy, rr) in PALLE_POS:
        px, py = x + (dx - 0.5) * s * 0.78, y + (dy - 0.52) * s * 0.78
        f.circle(px, py, rr * s * 0.78, color=color, alpha=alpha)


# palle konumları (kalkan birimi 1×1.15): üst mavi (büyük) + 5 kırmızı
PALLE_POS = [(0.50, 0.17, 0.150), (0.19, 0.34, 0.125), (0.81, 0.34, 0.125), (0.27, 0.63, 0.125), (0.73, 0.63, 0.125), (0.50, 0.86, 0.125)]


# ───────────────────────────── yardımcılar ─────────────────────────────
def fmt_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


def bgfill(f, cx, seed=0, flip=False, cam=None, dress=None):
    """Ortak arka plan: duvar (+ isteğe bağlı giydirme: dress='both'|'top'|'bottom'|None). Işık içerikten sonra `finish/relight` ile. Dönüş: Cam."""
    cam = cam or Cam(cx)
    cam.wall(f, seed=seed % 3, flip=flip)
    if dress:
        import cilt_orn
        cilt_orn.dress(f, cam, top=dress in ("both", "top"), bottom=dress in ("both", "bottom"))
    return cam


_RL = {}


_POOL = {}
POOL_STOPS = [(0.0, 0.22), (0.18, 0.25), (0.42, 0.42), (0.70, 0.66), (1.00, 0.86), (1.30, 0.945)]


def _pool_img(hue, n=640):
    """Mum havuzu kaplaması (önbellekli, n×n, [-1.3R,1.3R] kapsar): merkezde sıcak-koyu kahve, dışa doğru lacivert-siyah (alfa artar)."""
    key = (hue, n)
    if key not in _POOL:
        yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        p = np.hypot(xx - n / 2 + 0.5, yy - n / 2 + 0.5) / (n / 2) * 1.3
        ps = [q for q, _ in POOL_STOPS]
        al = np.interp(p, ps, [a_ for _, a_ in POOL_STOPS]).astype(np.float32)
        rs = np.random.RandomState(3)
        al = np.clip(al + rs.uniform(-0.004, 0.004, al.shape).astype(np.float32), 0, 1)
        t = np.clip((p - 0.05) / 0.55, 0, 1)
        t = t * t * (3 - 2 * t)
        warm = np.array([46, 22, 10], np.float32)
        cool = np.array(hue, np.float32)
        col = warm[None, None, :] * (1 - t[..., None]) + cool[None, None, :] * t[..., None]
        arr = np.dstack([col, al * 255]).astype(np.uint8)
        _POOL[key] = sk.np_to_image(arr)
    return _POOL[key]


def relight(f, cx=None, light=None, k=1.0, shaft_a=None, t=None):
    """İçerik çizildikten SONRA ışık: gündüz → sol-üstten sıcak aydınlık + sağ-alt gölge + huzme (tek blit); gece → mum havuzu dışı lacivert-siyaha batar
    (tek geçiş: tüm kareyi etkiler, böylece duvara işlenmiş içerik de aynı ışıkla aydınlanır). Hepsi SrcOver (hızlı yol)."""
    t = cx.t if (cx is not None and t is None) else (t or 0.0)
    if TH.mode == "day":
        daylight(f, k, t)
        return
    if light is None:
        light = candle_light(t, getattr(cx, "seed", 0) if cx is not None else 0)
    x, y, r, kk = light
    kk = clamp(kk * k, 0.0, 1.3)
    hue = (6, 12, 46) if TH.perde != 3 else (30, 7, 10)
    n = 640
    img = _pool_img(hue, n)
    D = 1.3 * r
    gain = clamp(1.0 - 0.45 * (kk - 1.0), 0.0, 1.0)
    p = skia.Paint()
    p.setAlphaf(gain)
    c = f.c
    c.drawImageRect(img, skia.Rect.MakeWH(n, n), skia.Rect.MakeLTRB(x - D, y - D, x + D, y + D), _LIN, p)
    edge = skia.Paint(Color=skia.Color(hue[0], hue[1], hue[2], int(255 * 0.945 * gain)))
    L, T_, R_, B_ = x - D, y - D, x + D, y + D
    if L > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, L, H), edge)
    if R_ < W:
        c.drawRect(skia.Rect.MakeLTRB(R_, 0, W, H), edge)
    if T_ > 0:
        c.drawRect(skia.Rect.MakeLTRB(max(0, L), 0, min(W, R_), T_), edge)
    if B_ < H:
        c.drawRect(skia.Rect.MakeLTRB(max(0, L), B_, min(W, R_), H), edge)


def finish(f, cx, motes_n=34, vig_s=None, seed=2, dust=True, light=None, k=1.0, shaft_a=None):
    relight(f, cx, light=light, k=k, shaft_a=shaft_a)
    if dust and motes_n:
        motes(f, cx.t, n=motes_n, seed=seed)
    vig(f, vig_s)


def mode_of(f):
    return getattr(f, "cilt_mode", "day"), getattr(f, "cilt_perde", 2)
