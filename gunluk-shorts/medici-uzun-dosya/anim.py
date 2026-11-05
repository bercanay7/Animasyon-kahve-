"""anim — genel hareket yardımcıları (ENG-B, Kasım 2026; kurul tur 1 AN1-E3/E8). Figür kitine BAĞLI DEĞİL: saf zaman → değer işlevleri
+ birkaç küçük çizim sarmalayıcısı. Hepsi deterministik (tohumlu) ve alt-kare zamanında da sürekli (deklanşör alt örneklemesi için).

Zaman sözleşmesi: t = çekimin yerel saati (cx.t, sn); t0 = olayın yerel saniyesi (cx.at(çapa)). Örnekler notlar_hareket.md'de.

  anticip(t, t0, dur, back=0.12, pre=0.22)      hazırlık: t0'dan önce `pre` sn ters yönde −back'e çekilir, t0'da asıl hareket başlar, t0+dur'da 1
  settle(t, t0, dur=0.45, over=0.12)            oturma: t0'da başlar, t0+dur'da hedefe (1) varır, `over` kadar aşar, sönümlü salınımla oturur
  wobble(t, t0, amp=1.0, freq=3.0, decay=5.0)   darbe sonrası sönümlü salınım (0 çevresinde): tüy kalem, sancak ucu, levha zinciri
  shake(t, t0, dur=0.25, amp=4.0, seed=0)       sarsıntı → (dx, dy) px (tohumlu, sönümlü; t0'da en güçlü)
  blink(t, seed=0, every=(2.4, 5.6), dur=0.16)  göz kırpma zamanlayıcısı → kapak eğrisi 0 (açık) .. 1 (kapalı)
  breathe(t, seed=0, amp=1.0, hz=0.22)          boşta nefes (yavaş, düzgün) → [−amp, amp]
  keyed(t, keys)                                 anahtar kare: keys=[(t, v[, "io"|"in"|"out"|"lin"|"back"|"settle"]), …]; v sayı ya da demet
  stamp_pose(t, t0, profile)                     damga vuruşu pozu (Pose): "squash" ezilme · "spin" dönme · "bounce" sekme · "drop" eski 4 kare · "ink" mürekkep
  stamp(f, text, x, y, t, t0, profile=…)         damgayı profil dönüşümüyle çizer (CM.stamp'ı sarar) + gölge sıçraması + mürekkep yayılması; darbe değerini döndürür
  impact_ovl(at, amp=4.0, dur=0.25)              ovl (p1_ortak.ov ile): çapada tüm kareyi kısa sarsar (ovl listesinin SONUNA koy)
  stamp_ovl(text, x, y, at, profile=…, …)        ovl: damga + isteğe bağlı kare sarsıntısı (at = DARBE anı)
  hint_speed(cx, px_per_frame)                   deklanşöre ipucu: bu karede hızlı nesne var (compose.Program okur; "auto" modda alt örnekleme)
"""
import math
import zlib

TAU = 2.0 * math.pi


# ───────────────────────────── temel eğriler ─────────────────────────────
def _clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)


def _smooth(x):
    x = _clamp(x)
    return x * x * (3.0 - 2.0 * x)


def _ease_io(x, p=2.2):
    x = _clamp(x)
    return 0.5 * (2 * x) ** p if x < 0.5 else 1.0 - 0.5 * (2 * (1 - x)) ** p


def _ease_in(x, p=2.0):
    return _clamp(x) ** p


def _ease_out(x, p=2.0):
    return 1.0 - (1.0 - _clamp(x)) ** p


def _back_out(x, s=1.70158):
    x = _clamp(x) - 1.0
    return x * x * ((s + 1) * x + s) + 1.0


EASE = {"io": _ease_io, "in": _ease_in, "out": _ease_out, "lin": _clamp, "smooth": _smooth, "back": _back_out}


def _rng(seed, k=0):
    """Tohumlu [0,1) dizisi üreteci (Python random'a bağlı değil; süreçler arası aynı)."""
    s = (zlib.crc32(f"{seed}:{k}".encode()) ^ 0x9E3779B9) & 0xFFFFFFFF

    def nxt():
        nonlocal s
        s = (1664525 * s + 1013904223) & 0xFFFFFFFF
        return s / 4294967296.0
    return nxt


def _noise3(t, seed, axis, freq):
    """[-1, 1] düzgün tohumlu gürültü: üç sinüs (freq·(1, 1.37, 2.11)), rastgele faz."""
    r = _rng(seed, 100 + axis)
    v = 0.0
    for m, a in ((1.0, 0.62), (1.37, 0.28), (2.11, 0.10)):
        v += a * math.sin(TAU * freq * m * (0.9 + 0.2 * r()) * t + TAU * r())
    return v


# ───────────────────────────── hazırlık / oturma ─────────────────────────────
def anticip(t, t0, dur, back=0.12, pre=0.22, p=2.2):
    """Hazırlık (anticipation): [t0−pre, t0] arasında ters yöne −back'e iner (hızı t0'da 0), t0'dan itibaren dur sn'de 1'e çıkar.
    Dönüş: −back … 1. Örn. kol kalkmadan önce hafifçe geriye, kese atılmadan önce hafif çöküş."""
    if t <= t0 - pre:
        return 0.0
    if t < t0:
        return -back * _smooth((t - (t0 - pre)) / max(1e-6, pre))
    return -back + (1.0 + back) * _ease_io((t - t0) / max(1e-6, dur), p)


def _spring(tau, w, s):
    """2. derece adım tepkisi (0 → 1, aşmalı): 1 − e^(−sτ)(cos wτ + s/w sin wτ). τ<0 → 0."""
    if tau <= 0:
        return 0.0
    e = math.exp(-s * tau)
    return 1.0 - e * (math.cos(w * tau) + (s / w) * math.sin(w * tau))


def _spring_par(dur, over):
    """settle parametreleri: ilk 1-geçişi dur sn'de, ilk aşma `over` (0<over<1)."""
    over = _clamp(over, 1e-4, 0.9)
    L = -math.log(over)
    w = (math.pi - math.atan(math.pi / L)) / max(1e-4, dur)
    return w, L * w / math.pi


def settle(t, t0, dur=0.45, over=0.12):
    """Oturma (settle): t0'da 0'dan (hızı 0) başlar, t0+dur'da hedefe (1) varır, `over` kadar aşar ve sönümlü salınımla 1'e oturur.
    Dönüş: 0 … 1+over … 1. Konum/ölçek/açı için: v = a + (b − a)·settle(…)."""
    w, s = _spring_par(dur, over)
    return _spring(t - t0, w, s)


def wobble(t, t0, amp=1.0, freq=3.0, decay=5.0):
    """Darbe sonrası sönümlü salınım (0 çevresinde): amp·e^(−decay·τ)·sin(2π·freq·τ); τ<0 → 0. İkincil hareket (tüy, zincir, sancak ucu)."""
    tau = t - t0
    if tau <= 0:
        return 0.0
    return amp * math.exp(-decay * tau) * math.sin(TAU * freq * tau)


# ───────────────────────────── sarsıntı ─────────────────────────────
def shake(t, t0, dur=0.25, amp=4.0, seed=0, freq=10.0):
    """Sarsıntı (tohumlu, sönümlü): (dx, dy) px. t0'da en güçlü, (1 − τ/dur)² zarfla söner; 24 fps'te 6 karelik sarsıntı ≈ dur 0,25.
    freq ≤ 12 Hz (24 fps Nyquist); dikey bileşen %80."""
    tau = t - t0
    if tau < 0 or tau > dur:
        return 0.0, 0.0
    env = (1.0 - tau / dur) ** 2
    return amp * env * _noise3(t, seed, 0, freq), 0.8 * amp * env * _noise3(t, seed, 1, freq * 1.13)


# ───────────────────────────── göz kırpma ─────────────────────────────
_BLINKS = {}


def _blink_times(seed, every, double, t_max):
    key = (seed, every, double)
    lst = _BLINKS.get(key)
    if lst is None or lst[-1] < t_max:
        r = _rng(seed, 7)
        out = [] if lst is None else list(lst)
        t = (out[-1] if out else -r() * every[1])
        while t < t_max + every[1]:
            t += every[0] + (every[1] - every[0]) * r()
            out.append(t)
            if r() < double:                       # çift kırpma
                t += 0.24 + 0.06 * r()
                out.append(t)
        _BLINKS[key] = lst = out
    return lst


def blink(t, seed=0, every=(2.4, 5.6), dur=0.16, double=0.15):
    """Göz kırpma zamanlayıcısı: zaman → kapak eğrisi 0 (açık) .. 1 (kapalı). Tohumlu aralıklar (every sn), %15 çift kırpma.
    Kapanış hızlı (%35), açılış yavaş. Figüre bağlı değil: çizerken göz yüksekliğini (1 − blink) ile ölçekle."""
    if t < 0:
        return 0.0
    times = _blink_times(seed, tuple(every), double, t)
    lo, hi = 0, len(times) - 1
    while lo < hi:                                 # son kırpma ≤ t
        mid = (lo + hi + 1) // 2
        if times[mid] <= t:
            lo = mid
        else:
            hi = mid - 1
    tb = times[lo]
    if tb > t:
        return 0.0
    p = (t - tb) / dur
    if p >= 1.0:
        return 0.0
    return _smooth(p / 0.35) if p < 0.35 else 1.0 - _smooth((p - 0.35) / 0.65)


def breathe(t, seed=0, amp=1.0, hz=0.22):
    """Boşta nefes: yavaş, düzgün salınım [−amp, amp] (tohumlu faz + hafif düzensizlik). Ölçek için 1 + 0.006·breathe(...)."""
    r = _rng(seed, 3)
    ph = TAU * r()
    return amp * (0.82 * math.sin(TAU * hz * t + ph) + 0.18 * math.sin(TAU * hz * 2.37 * t + 2.0 * ph))


# ───────────────────────────── anahtar kare ─────────────────────────────
def keyed(t, keys):
    """Anahtar kare ara değer. keys=[(t, v[, ease]), …] artan t; ease bir SONRAKİ parçanın eğrisi: io|in|out|lin|smooth|back|settle.
    v sayı ya da aynı uzunlukta demet; uçlarda sabit."""
    if not keys:
        return 0.0
    if t <= keys[0][0]:
        return keys[0][1]
    for i in range(len(keys) - 1):
        ta, va = keys[i][0], keys[i][1]
        tb, vb = keys[i + 1][0], keys[i + 1][1]
        if t <= tb:
            ez = keys[i][2] if len(keys[i]) > 2 else "io"
            u = (t - ta) / max(1e-9, tb - ta)
            if ez == "settle":
                k = settle(u, 0.0, 1.0, 0.10)
            else:
                k = EASE.get(ez, _ease_io)(u)
            if isinstance(va, (tuple, list)):
                return tuple(a + (b - a) * k for a, b in zip(va, vb))
            return va + (vb - va) * k
    return keys[-1][1]


# ───────────────────────────── damga vuruşu ─────────────────────────────
class Pose:
    """Damga/nesne vuruş pozu: sx, sy ölçek; rot (derece, eklenir); dx, dy (px); alpha; ink (0..1 mürekkep yayılması); lift (0..1: kâğıttan
    yükseklik → gölge kayması); impact (0..1 darbe zarfı: sarsıntı için); vis (çizilsin mi)."""
    __slots__ = ("sx", "sy", "rot", "dx", "dy", "alpha", "ink", "lift", "impact", "vis")

    def __init__(self, **k):
        self.sx = self.sy = 1.0
        self.rot = self.dx = self.dy = 0.0
        self.alpha = 1.0
        self.ink = self.lift = self.impact = 0.0
        self.vis = True
        for a, b in k.items():
            setattr(self, a, b)

    def __repr__(self):
        return "Pose(" + ", ".join(f"{a}={getattr(self, a):.3g}" if isinstance(getattr(self, a), float) else f"{a}={getattr(self, a)}" for a in self.__slots__) + ")"


STAMP_PROFILES = ("squash", "spin", "bounce", "drop", "ink")
APPROACH = dict(squash=0.20, spin=0.30, bounce=0.20, drop=0.17, ink=0.05)      # darbeden önce görünür olma süresi (sn)


def stamp_pose(t, t0, profile="squash", dur=None, seed=0):
    """Damga vuruşu pozu. t0 = DARBE anı (sözcük çapası buraya). Profiller:
      squash  ezilme: yukarıdan hızlanarak iner (1,55→1), darbede yassılır (sx 1,13 / sy 0,84) ve yaylanarak oturur; mürekkep yayılır
      spin    dönme: −38° ve 1,7× ölçekten dönerek iner, açı küçük aşmayla oturur
      bounce  sekme: düşer, iki kez sekip (14 px, 5 px) oturur; her temasta hafif ezilme
      drop    eski davranış: büyükten küçüğe 4 kare (back_out)
      ink     yerinde mürekkep: ölçek 0,97→1, mürekkep yayılır, kenar keskinleşir (sessiz vurgu)"""
    pr = profile if profile in STAMP_PROFILES else "squash"
    ap = APPROACH[pr] if dur is None else float(dur)
    tau = t - t0
    if tau < -ap:
        return Pose(vis=False, alpha=0.0)
    imp = math.exp(-max(0.0, tau) / 0.09) if tau >= 0 else 0.0
    ink = _ease_out(tau / 0.35, 2.5) if tau >= 0 else 0.0
    if pr == "squash":
        if tau < 0:
            u = 1.0 + tau / ap                                  # 0 → 1 (darbeye yaklaşım)
            e = _ease_in(u, 2.2)
            s = 1.55 - 0.55 * e
            return Pose(sx=s, sy=s, alpha=_smooth(u / 0.35), lift=1.0 - e, dy=-18.0 * (1.0 - e))
        sq = wobble(t, t0, 1.0, 5.2, 11.0)                      # yay: ezilme → hafif uzama → oturma
        return Pose(sx=1.0 + 0.13 * sq, sy=1.0 - 0.16 * sq, ink=ink, impact=imp, dy=3.0 * max(0.0, sq))
    if pr == "spin":
        if tau < 0:
            u = 1.0 + tau / ap
            e = _ease_out(u, 1.6)
            s = 1.7 - 0.7 * _ease_in(u, 1.8)
            return Pose(sx=s, sy=s, rot=-38.0 * (1.0 - e), alpha=_smooth(u / 0.3), lift=1.0 - _ease_in(u, 1.8))
        wb = wobble(t, t0, 1.0, 5.0, 12.0)                       # darbede hafif ezilme; açı küçük aşmayla oturur
        return Pose(rot=4.0 * wobble(t, t0, 1.0, 2.6, 6.0), ink=ink, impact=imp, sx=1.0 + 0.05 * wb, sy=1.0 - 0.06 * wb)
    if pr == "bounce":
        g_h = 70.0                                              # düşüş yüksekliği (px)
        if tau < 0:
            u = 1.0 + tau / ap
            e = _ease_in(u, 2.0)
            return Pose(dy=-g_h * (1.0 - e), alpha=_smooth(u / 0.3), lift=1.0 - e, sx=1.04, sy=1.04)
        # iki seki: 0–0,22 sn (14 px), 0,22–0,36 sn (5 px)
        b1, b2 = 0.22, 0.14
        if tau < b1:
            h = 14.0 * 4 * (tau / b1) * (1 - tau / b1)
            lf = h / g_h
        elif tau < b1 + b2:
            u2 = (tau - b1) / b2
            h = 5.0 * 4 * u2 * (1 - u2)
            lf = h / g_h
        else:
            h, lf = 0.0, 0.0
        sq = math.exp(-((tau % b1 if tau < b1 + b2 else 9.0) / 0.035) ** 2) if tau < b1 + b2 else 0.0
        return Pose(dy=-h, sx=1.0 + 0.10 * sq, sy=1.0 - 0.12 * sq, lift=lf, ink=ink, impact=imp)
    if pr == "drop":
        if tau < 0:
            u = 1.0 + tau / ap
            s = 1.0 + (1 - _back_out(u)) * 0.9
            return Pose(sx=s, sy=s, alpha=min(1.0, u * 3), lift=1.0 - u)
        return Pose(ink=ink * 0.6, impact=imp)
    # ink
    if tau < 0:
        u = 1.0 + tau / ap
        return Pose(alpha=0.25 * u, sx=0.97, sy=0.97)
    k = _ease_out(tau / 0.45, 2.0)
    s = 0.97 + 0.03 * k
    return Pose(sx=s, sy=s, alpha=0.25 + 0.75 * k, ink=k, impact=0.35 * imp)


STAMP_BACK = True              # kurul tur 2 TE2-Y5: damganın altına kâğıt yaması — yazı ↔ hemen arkasındaki zemin ≥4,5:1
STAMP_BACK_ALPHA = 0.95        # yamanın örtücülüğü (en koyu / en desenli arka planda da hedef tutsun)
STAMP_CR_MIN = 7.0             # koyu mürekkep ↔ açık kâğıt NOMİNAL hedef: renk derecelendirme (post) kontrastı ≈%30 düşürüyor → son karede ölçülen ≥4,5:1
STAMP_CR_MIN_NIGHT = 6.0       # açık (gece) mürekkep ↔ koyu kâğıt
PAPER_LIGHT = ("#FCF7EA", "#F3EBD7")      # koyu (sinabar) mürekkep → açık kâğıt fişi
PAPER_DARK = ("#24180F", "#160E09")       # açık (gece) mürekkep → koyu kâğıt fişi


def _lum(hexcol):
    """WCAG göreli parlaklık ('#RRGGBB')."""
    import sk
    v = []
    for ch in sk.rgb(hexcol):
        c = ch / 255.0
        v.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def _cr(la, lb):
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def stamp_back_colors(color):
    """Mürekkep rengine göre (kâğıt üst/alt rengi, gerekirse koyulaştırılmış/açılmış mürekkep). Damga dili korunur: kırmızı mürekkep, yalnız tonu."""
    import sk
    li = _lum(color)
    dark_ink = li < 0.22
    paper = PAPER_LIGHT if dark_ink else PAPER_DARK
    lp = min(_lum(paper[0]), _lum(paper[1])) if dark_ink else max(_lum(paper[0]), _lum(paper[1]))
    ink = color
    k = 0.0
    target = STAMP_CR_MIN if dark_ink else STAMP_CR_MIN_NIGHT
    while _cr(_lum(ink), lp) < target and k < 0.6:              # mürekkebi kâğıttan uzaklaştır (koyu mürekkebi koyulaştır, açığı aç)
        k += 0.04
        ink = sk.mix(color, "#1A0604" if dark_ink else "#FFF1E6", k)
    return paper, ink


def stamp_back(f, x, y, text, size, rot, alpha, seed=0, ink=None):
    """Damga kâğıt fişi: damganın çerçevesinden biraz büyük, hafif farklı açıyla oturmuş, yumuşak gölgeli kâğıt (gece koyu kâğıt).
    (x, y, rot) damganın OTURDUĞU yer — fiş damgayla birlikte zıplamaz/dönmez (damga fişe vurur). ink: damganın (özgün) mürekkebi → kâğıt kutbu."""
    if alpha <= 0.003:
        return
    import skia
    import sk
    import cilt_medici as CM
    paper, _ink = stamp_back_colors(ink or (CM.TH.acc if CM.TH.day else "#E56A52"))
    c = f.c
    wd = sk.text_width(text, "title", size, 7) + 64
    mx, my = 0.17 * size + 6, 0.13 * size + 4
    x0, y0, x1, y1 = -wd / 2 - mx, -size * 0.86 - my, wd / 2 + mx, size * 0.66 + my
    r = _rng(f"{text}:{seed}", 31)
    tilt = math.degrees(rot) + (0.55 + 0.5 * r()) * (1 if r() < 0.5 else -1)
    c.save()
    c.translate(x, y)
    c.rotate(tilt)
    day = CM.TH.day
    sp = skia.Paint(AntiAlias=True, Color=sk.C("#120A04", int(255 * (0.26 if day else 0.50) * alpha)),
                    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5.0))
    rr = 0.10 * size
    c.drawRoundRect(skia.Rect.MakeLTRB(x0 + 3, y0 + 5, x1 + 3, y1 + 5), rr, rr, sp)
    pp = skia.Paint(AntiAlias=True)
    pp.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [sk.C(paper[0]), sk.C(paper[1])]))
    pp.setAlphaf(STAMP_BACK_ALPHA * alpha)
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), rr, rr, pp)
    ep = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.3, Color=sk.C("#7C5C2E" if day else "#C9A45A", int(255 * 0.45 * alpha)))
    c.drawRoundRect(skia.Rect.MakeLTRB(x0 + 0.6, y0 + 0.6, x1 - 0.6, y1 - 0.6), rr, rr, ep)
    c.restore()


def stamp(f, text, x, y, t, t0, profile="squash", rot=-0.10, size=56, color=None, alpha=1.0, draw=None, shadow=True, ink=True, seed=0, back=None, **kw):
    """Damgayı profil pozuyla çiz. draw: çizim işlevi (varsayılan cilt_medici.stamp; imza draw(f, text, x, y, rot=, size=, color=, alpha=, t=1.0, **kw)).
    Gölge sıçraması: damga kâğıttan yüksekken yumuşak gölge sağ-alta kayar, darbede altına toplanır. Mürekkep: darbeden sonra kenarda hafif yayılma.
    back: kâğıt fişi (None → STAMP_BACK; yalnız varsayılan CM.stamp çiziminde): damga fişe vurur; mürekkep gerekirse koyulaştırılır (TE2-Y5).
    Dönüş: darbe zarfı (0..1) — kamera/kare sarsıntısı için (impact_ovl ya da cam=(…, dict(shake=[…])))."""
    p = stamp_pose(t, t0, profile, seed=seed)
    if not p.vis or p.alpha <= 0.003:
        return 0.0
    import skia
    use_back = False
    ink0 = None
    if draw is None:
        import cilt_medici as CM
        draw = CM.stamp
        use_back = STAMP_BACK if back is None else bool(back)
        if color is None:
            color = CM.TH.acc if CM.TH.day else "#E56A52"          # CM.stamp ile aynı varsayılan (mürekkep gölgesi de bu renkte)
        if use_back:
            ink0 = color
            color = stamp_back_colors(color)[1]
    c = f.c
    a = alpha * p.alpha
    import sk
    wd = sk.text_width(text, "title", size, 8) + 60
    hh = size * 1.5
    col = color or "#A8261E"
    if use_back:                                               # kâğıt fişi damgadan önce görünür (damga ona iner); oturduğu yerde sabit
        ap = APPROACH.get(profile if profile in STAMP_PROFILES else "squash", 0.2)
        kb = _smooth((t - t0 + ap) / max(ap, 0.25))            # yaklaşımın başında 0 → (en geç darbeden 0,2 sn sonra) 1; sürekli
        stamp_back(f, x, y, text, size, rot, alpha * kb, seed=seed, ink=ink0)
    if shadow and p.lift > 0.01:                               # gölge sıçraması (kâğıttan yükseklik)
        c.save()
        c.translate(x + p.dx + 16 * p.lift, y + p.dy + 22 * p.lift)
        c.rotate(math.degrees(rot) + p.rot)
        c.scale(p.sx, p.sy)
        sp = skia.Paint(AntiAlias=True, Color=sk.C("#1A1008", int(255 * 0.30 * a * (0.4 + 0.6 * p.lift))),
                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6 + 14 * p.lift))
        c.drawRoundRect(skia.Rect.MakeLTRB(-wd / 2, -size * 0.85, wd / 2, -size * 0.85 + hh), 10, 10, sp)
        c.restore()
    if ink and p.ink > 0.01:                                   # mürekkep yayılması (çarpma, kâğıda işler)
        c.save()
        c.translate(x + p.dx, y + p.dy)
        c.rotate(math.degrees(rot) + p.rot)
        grow = 1.0 + 0.06 * p.ink
        c.scale(grow, grow)
        ip = skia.Paint(AntiAlias=True, Color=sk.C(col, int(255 * (0.07 if use_back else 0.16) * a * p.ink)), BlendMode=skia.BlendMode.kMultiply,
                        MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9.0))
        c.drawRoundRect(skia.Rect.MakeLTRB(-wd / 2 - 6, -size * 0.85 - 6, wd / 2 + 6, -size * 0.85 + hh + 6), 12, 12, ip)
        c.restore()
    c.save()
    c.translate(x + p.dx, y + p.dy)
    c.rotate(p.rot)
    c.scale(p.sx, p.sy)
    c.translate(-x, -y)
    draw(f, text, x, y, rot=rot, size=size, color=color, alpha=a, t=1.0, **kw)
    c.restore()
    return p.impact


def paper_stamp(f, text, x, y, rot=-0.10, size=56, color=None, alpha=1.0, t=1.0, back=None, seed=0):
    """cilt_medici.stamp ile AYNI imza (+ back, seed): sahnelerdeki doğrudan CM.stamp çağrıları bunu kullanınca kâğıt fişi ve
    ≥4,5:1 mürekkep tonu gelir (TE2-Y5). t: CM.stamp'taki çarpma animasyonu (0 → 1); fiş damgayla birlikte (t·3) belirir, oturduğu yerde durur."""
    if t <= 0:
        return
    import cilt_medici as CM
    use_back = STAMP_BACK if back is None else bool(back)
    if color is None:
        color = CM.TH.acc if CM.TH.day else "#E56A52"
    if use_back:
        stamp_back(f, x, y, text, size, rot, alpha * min(1.0, t * 3.0), seed=seed, ink=color)
        color = stamp_back_colors(color)[1]
    CM.stamp(f, text, x, y, rot=rot, size=size, color=color, alpha=alpha, t=t)


# ───────────────────────────── ovl kurucuları (p1_ortak.ov ile birlikte) ─────────────────────────────
def jolt(f, dx, dy, zoom=None):
    """Çizilmiş kareyi (dx, dy) kaydırarak yeniden çiz (kenarlar açılmasın diye hafif büyütme). Sarsıntı karelerinde ≈6 ms."""
    if abs(dx) < 0.05 and abs(dy) < 0.05:
        return
    import skia
    from sk import H, W
    img = f.surf.makeImageSnapshot()
    z = zoom if zoom is not None else 1.0 + 2.2 * max(abs(dx), abs(dy)) / min(W, H)
    c = f.c
    c.save()
    c.resetMatrix()
    c.translate(W / 2 + dx, H / 2 + dy)
    c.scale(z, z)
    c.translate(-W / 2, -H / 2)
    c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(BlendMode=skia.BlendMode.kSrc))
    c.restore()


def impact_ovl(at, amp=4.0, dur=0.25, seed=0):
    """ovl: `at` çapasında tüm kare kısa ve sönümlü sarsılır (2–6 px önerilir). p1_ortak.ov(...) listesinin SONUNA koy (önce çizilenleri kaydırır)."""
    def fn(cx):
        t0 = cx.at(at)
        dx, dy = shake(cx.t, t0, dur, amp, seed=seed + getattr(cx, "seed", 0))
        jolt(cx.f, dx, dy)
    return fn


def stamp_ovl(text, x, y, at, profile="squash", rot=-0.10, size=56, color=None, out=None, out_dur=0.4, jolt_amp=0.0, seed=0, **kw):
    """ovl: profilli damga. at = DARBE anı (eski P.stamp'ta `at` iniş başlangıcıydı; burada vuruşun kendisi). out: solma çapası.
    jolt_amp > 0 ise darbede kare de sarsılır (o zaman bu ovl'u listenin sonuna koy)."""
    def fn(cx):
        t0 = cx.at(at)
        a = 1.0 if out is None else 1.0 - _smooth((cx.t - cx.at(out)) / out_dur)
        if a <= 0.003:
            return
        imp = stamp(cx.f, text, x, y, cx.t, t0, profile, rot=rot, size=size, color=color, alpha=a, seed=seed, **kw)
        if profile in ("squash", "bounce", "drop") and cx.t - t0 > -APPROACH[profile]:
            hint_speed(cx, 9.0 if cx.t < t0 else 0.0)
        if jolt_amp > 0 and imp > 0.01:
            dx, dy = shake(cx.t, t0, 0.25, jolt_amp, seed=seed + 11)
            jolt(cx.f, dx, dy)
    return fn


# ───────────────────────────── deklanşör ipucu ─────────────────────────────
def hint_speed(cx, px_per_frame):
    """Bu karede ekranda hızlı hareket eden bir nesne var (px/kare, 1920 ölçeği). compose.Program "auto" deklanşörde alt-kare örneklemesine karar verirken
    kamera hızı ve ölçülen akışla birlikte okur. Hızlı nesne çizen her kod çağırabilir (bozuk para yağmuru, uçan tüy, çekiç)."""
    try:
        v = float(px_per_frame)
        if v > getattr(cx, "speed_hint", 0.0):
            cx.speed_hint = v
    except (TypeError, ValueError):
        pass


def speed_of(p0, p1, dt):
    """İki konum arası ekran hızı (px/kare, 24 fps): hint_speed için yardımcı. dt sn."""
    return math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / max(1e-6, dt) / 24.0


if __name__ == "__main__":                                       # öz sınama: süreklilik + aralıklar
    ok = True
    for f_, a in ((lambda t: anticip(t, 1.0, 0.5), "anticip"), (lambda t: settle(t, 1.0, 0.4, 0.12), "settle"), (lambda t: wobble(t, 1.0), "wobble")):
        vals = [f_(i / 240.0) for i in range(0, 720)]
        jump = max(abs(b - a_) for a_, b in zip(vals[:-1], vals[1:]))
        print(f"{a:8s} min {min(vals):+.3f} maks {max(vals):+.3f} son {vals[-1]:+.3f} en büyük adım {jump:.4f}")
        ok = ok and jump < 0.08
    s = settle(10, 0, 0.4, 0.12)
    ok = ok and abs(s - 1) < 1e-3 and abs(max(settle(i / 200, 0, 0.4, 0.12) for i in range(400)) - 1.12) < 0.01
    print("settle aşma", max(settle(i / 200, 0, 0.4, 0.12) for i in range(400)))
    bl = [blink(i / 24.0, seed=3) for i in range(24 * 60)]
    print("blink: 60 sn'de kapalı kare", sum(1 for b in bl if b > 0.5), " kırpma sayısı ≈", sum(1 for a_, b in zip(bl[:-1], bl[1:]) if a_ <= 0.5 < b))
    for pr in STAMP_PROFILES:
        ps = [stamp_pose(i / 24.0, 1.0, pr) for i in range(0, 48)]
        print(f"{pr:7s}", " ".join(f"{p.sx:.2f}/{p.sy:.2f}/{p.dy:+.0f}/{p.rot:+.0f}" for p in ps[18:32:2]))
    print("ÖZ SINAMA:", "GEÇTİ" if ok else "KALDI")
