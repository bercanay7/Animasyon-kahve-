"""cilt_cam — Medici cildi kamera sözlüğü (YONETMENLIK_REHBERI §2): `cam=` ön ayarını kamera durumuna çevirir.

Tür yazarı bir şey yapmaz: `shot(..., cam=…)`  →  `cilt_medici.ckind` sarmalayıcısı alanı ayıklar (`cx.cam_spec`) ve
`CM.Cam(cx, …)` spec'i görürse kendi varsayılan push/drift'ini bırakıp buradaki durumu uygular. `map` türü (kendi kamerası var)
`mapsk.Cam` yaması ile (map_patch) aynı ekran-uzayı hareketini alır. Kamera başka yerde çiziliyorsa (pano, theatre …): `cx.cam_state`.

cam= biçimleri
  "push" | ("push", 0.08[, opts])        yavaş itme (varsayılan %7)            · "pull" | ("pull", 0.07)   yavaş çekme
  ("pan", "r"|"l", px)                    yatay kayma + paralaks; r: kamera sağa gider (içerik SOLA akar)
  ("crane", "up"|"down", px)              dikey kayma; up: kamera yükselir (içerik AŞAĞI akar)
  ("orbit", derece)                       yörünge (≤12°): içerik bir yöne, duvar ters yöne kayar (paralaks) + hafif yuvarlanma
  "hand" | "hand2"                        elde kamera (genlik 1,5 / 4 px; seed'li, deterministik) + yavaş itme
  ("rack", (x,y), (x,y)[, opts])          odak kaydırma: odak noktası a→b; çevre bulanık (post), odak dairesi keskin
  ("track", yol_id)                       kayıtlı anahtar kareli yol (register_track; pano/Lab-B yolları da buraya kaydolur)
  [(çapa, (x, y, zoom, rot)), …]          serbest anahtar kare: çapa = yerel sn | (sid[, sözcük], ofset) | sid
 ENG-B (Kasım 2026, kurul tur 1) eklemeleri — notlar_hareket.md:
  "push" | ("push",) | ("push", "auto")   SÜREYE BAĞLI itme: miktar = 0,039·süre^0,47 (2,5 sn %6 · 8 sn %10,5 · 13 sn %13), tohumla ±%12 ve eğri çeşidi
                                          (io/out/in); ("push", 0.08) eski sabit miktar; ("push", dict(rate=0.012)) → %/sn
  ("pan", "r"|"l") / ("truck", …) / ("tilt", "up"|"down") / ("crane", …)  px verilmezse süreye bağlı; truck = derin paralaks (duvar ×0,15),
                                          tilt = dönme hissi (duvar ×0,85, içerikle birlikte), pan/crane = ×0,40 (eski)
  ("whip", "r"|"l"[, px][, dict(where="in"|"out"|"mid", at=çapa, dur=0.30)])   hızlı savrulma (hazırlık + oturma); deklanşör yönlü bulanıklık verir
  "hand" | ("hand", genlik) | "drift"     elde mikro sürüklenme: yavaş gezinme (≈0,1–0,35 Hz, 6 px) + ince titreşim + ±0,12° + süreye bağlı yarım itme
  "hand2"                                 güçlü elde (4 px titreşim; yalnız şiddet anları)
  ("rack", a, b, dict(axis="y", …))       düzlemsel derinlik: odak bandı a.y → b.y kayar; ön/arka (alt/üst) bulanır (axis yok: dairesel, eski)
Tüm biçimlerde son eleman isteğe bağlı opts sözlüğü olabilir: pivot=(x,y), push=0.03 (pan/crane ek itme), hand=genlik, drift=(dx,dy) (px, itme ile birlikte),
ease="io"|"out"|"in"|"lin" (zaman eğrisi), shake=[(çapa, genlik_px[, süre]), …] (darbe sarsıntısı; anim.shake).
cam= verilmezse compose.Program `auto_spec` ile tohumlu, ağırlıklı bir hareket seçer (ardışık aynı aile yok).

Kamera durumu: x,y = kamera konumu (px; +x kamera sağa → içerik sola akar, +y kamera aşağı), zoom (1 = nötr), rot (derece, + = içerik saat yönünde).
Zaman profili: Hermite (smoothstep ≡ ease_io); geçişte kamera devri için uç eğimi `CARRY` (cx.cam_in / cx.cam_out). t<0 (ön-tur) ve t>dur
doğrusal uzatılır (eğim sürekli) — gelen çekim hareket halinde başlar, giden çekim durmadan devam eder.
"""
import contextlib
import math
import zlib

import numpy as np

import sk
from sk import H, W, clamp

CARRY = 0.65                  # geçişte uç hızı (ortalama hızın katı); 0 → tam yumuşak duruş
CUT_SLOPE = 1.0               # SERT KESMEYLE birleşen uçta en küçük uç eğimi (= ortalama hız; yumuşatma yok — "hareket üstünde kesme", kurul tur 2 AN1-Y11; ENG-D)
BASE_PUSH = 0.07
AUTO_PUSH = (0.039, 0.47)     # süreye bağlı itme: miktar = a·süre^b  (2,5 sn %6 · 4 sn %7,6 · 8 sn %10,5 · 13 sn %13 · 16 sn %14,6) → hız kısa çekimde ≈2,4 %/sn, uzunda ≈0,9 %/sn
AUTO_PUSH_LIM = (0.045, 0.16)
PAN_RATE = 34.0               # süreye bağlı pan: px = 34·süre (110–300)
WALL_KIND = dict(pan=0.40, crane=0.40, truck=0.15, tilt=0.85, whip=0.55)   # duvar paralaks çarpanı (içeriğe göre)
PROFILES = {"io": None, "out": (1.8, 0.30), "in": (0.30, 1.8), "lin": (1.0, 1.0)}   # Hermite uç eğimleri (geçişte CARRY'den küçük olmaz)
HAND_BASE = 0.06              # elde kamerada altta yatan yavaş itme
ORBIT_R = 1000.0              # yörünge yarıçapı (px, içerik düzleminde)
WALL_K = 0.40                 # duvar paralaks çarpanı (içeriğe göre)
WALL_MG = (W / 2 + 100.0, H / 2 + 100.0)     # cilt_wall.MG = 100 → duvar görüntüsünün yarı boyutu

TRACKS = {}                   # yol_id → [(u 0..1, (x, y, zoom, rot)), …]  | callable(u) → (x, y, zoom, rot)
BAND_KINDS = {"skyline", "frieze", "procession"}   # tam genişlikte yatay şerit çizen türler: yatay kamera kayması şerit uçlarını açığa çıkarır → sabit örtme zumu (yeni şerit türleri buraya eklenir)
# ENG-D (kurul tur 2 AN2-K1 / TE1-Y5): tür adı pN_ önekiyle sarılmışsa (p1_procession, p6_skyline …) TABAN adla tanınır (base_kind);
# pan VE truck türün kendi kaydırmasına çevrilir (yön türün dir'iyle çelişmiyorsa); çevrilemezse genel öteleme + kaymanın GERÇEK kapsamından örtme zumu.
OWN_CAMERA = {"pano", "build"}        # kendi kamera yolu olan türler (pano: cams=, build: orbit=/crane): cam= alanı kabul edilir, cx.cam_spec'te durur ama CM.Cam'e UYGULANMAZ (çift hareket olmasın)
_WARNED = set()


# ───────────────────────────── yollar ─────────────────────────────
def base_kind(name):
    """Sarmalayıcı önekini soy: p1_procession → procession, p5g_pano → pano (qa_flow.base_kind ile aynı kural). None → None."""
    if not name:
        return name
    import re
    return re.sub(r"^p\d+[a-z]*_", "", str(name))


def register_track(name, keys):
    """Anahtar kareli uzun plan yolu kaydet. keys: [(u, (x, y, zoom, rot)), …] (u 0..1 artan) ya da callable(u) → (x, y, zoom, rot).
    Pano/Lab-B yolları bunu çağırır; ("track", name) çekim kamerası olarak kullanılır."""
    TRACKS[name] = keys


register_track("sweep_r", [(0.0, (-150, 34, 1.00, 0.0)), (0.5, (0, -8, 1.045, 0.0)), (1.0, (150, -44, 1.10, 0.0))])
register_track("arc_up", [(0.0, (-70, 100, 1.00, 0.0)), (0.55, (24, -24, 1.06, 0.0)), (1.0, (96, -118, 1.13, 0.0))])
register_track("drop_l", [(0.0, (110, -80, 1.08, 0.0)), (0.5, (10, 6, 1.03, 0.0)), (1.0, (-120, 90, 1.00, 0.0))])


# ───────────────────────────── ayrıştırma ─────────────────────────────
class Plan:
    """Normalleştirilmiş kamera planı: kind ∈ push|pull|pan|crane|orbit|hand|rack|track|keys; p: parametreler."""
    __slots__ = ("kind", "p", "spec")

    def __init__(self, kind, spec, **p):
        self.kind, self.spec, self.p = kind, spec, p

    def __repr__(self):
        return f"Plan({self.kind}, {self.p})"


_PLANS = {}


def _split_opts(t):
    t = list(t)
    opts = {}
    if t and isinstance(t[-1], dict):
        opts = dict(t.pop())
    return t, opts


def parse(spec):
    """cam= değeri → Plan | None. Tanınmayan biçimde ValueError (sessiz geçme yok)."""
    if spec is None:
        return None
    if isinstance(spec, Plan):
        return spec
    key = repr(spec)
    pl = _PLANS.get(key)
    if pl is not None:
        return pl
    pl = _parse(spec)
    _PLANS[key] = pl
    return pl


def _dir(s, ok):
    s = str(s).lower()
    if s not in ok:
        raise ValueError(f"cam yönü {s!r} geçersiz (beklenen {ok})")
    return s


def _parse(spec):
    if isinstance(spec, str):
        spec = (spec,)
    if isinstance(spec, (tuple, list)) and spec and isinstance(spec[0], str):
        a, o = _split_opts(spec)
        h = a[0].lower()
        if h in ("push", "pull"):
            amt = None                                       # None → süreye bağlı (AUTO_PUSH); sayı → sabit (eski)
            if len(a) > 1 and not (isinstance(a[1], str) and a[1].lower() == "auto"):
                amt = float(a[1])
            return Plan(h, spec, amt=amt, **o)
        if h in ("pan", "truck"):
            d = _dir(a[1] if len(a) > 1 else "r", ("r", "l"))
            return Plan(h, spec, d=d, px=float(a[2]) if len(a) > 2 else None, **o)
        if h in ("crane", "tilt"):
            d = _dir(a[1] if len(a) > 1 else "up", ("up", "down"))
            return Plan(h, spec, d=d, px=float(a[2]) if len(a) > 2 else None, **o)
        if h == "whip":
            d = _dir(a[1] if len(a) > 1 else "r", ("r", "l"))
            o.setdefault("where", "mid" if o.get("at") is not None else "in")
            if o["where"] not in ("in", "out", "mid"):
                raise ValueError("whip where= 'in' | 'out' | 'mid' olmalı")
            return Plan("whip", spec, d=d, px=float(a[2]) if len(a) > 2 else 420.0, **o)
        if h == "orbit":
            return Plan("orbit", spec, deg=min(12.0, abs(float(a[1]))) if len(a) > 1 else 8.0, sgn=1.0 if len(a) < 2 or float(a[1]) >= 0 else -1.0, **o)
        if h in ("hand", "hand2", "drift"):
            strong = h == "hand2"
            amp = 4.0 if strong else 1.0                     # titreşim genliği (px); yavaş gezinme ayrıca `wander` (varsayılan 6 px; hand2'de 3)
            if len(a) > 1:
                amp = float(a[1])
            o.setdefault("push", None)                       # None → süreye bağlı itmenin yarısı
            o.setdefault("wander", 3.0 if strong else 6.0)
            return Plan("hand", spec, amp=amp, strong=strong, **o)
        if h == "rack":
            if len(a) < 3:
                raise ValueError("rack: ('rack', (xa,ya), (xb,yb)) bekleniyor")

            def pt(q):                                      # (0..2, 0..2) aralığındaki değerler ekran oranı sayılır: (0.5, 0.45) → (960, 486) px
                x_, y_ = float(q[0]), float(q[1])
                return (x_ * W, y_ * H) if (abs(x_) <= 2.0 and abs(y_) <= 2.0) else (x_, y_)
            return Plan("rack", spec, a=pt(a[1]), b=pt(a[2]), **o)
        if h == "track":
            return Plan("track", spec, id=a[1], **o)
        raise ValueError(f"bilinmeyen cam ön ayarı: {h!r}")
    if isinstance(spec, (tuple, list)) and spec:
        a, o = _split_opts(spec)
        keys = []
        for item in a:
            an, v = item
            v = tuple(float(x) for x in v)
            v = v + (0.0,) * (4 - len(v)) if len(v) < 4 else v
            if len(v) == 3:
                v = v + (0.0,)
            keys.append((an, v))
        if not keys:
            raise ValueError("cam: boş anahtar kare listesi")
        return Plan("keys", spec, keys=keys, **o)
    raise ValueError(f"cam= biçimi tanınmadı: {spec!r}")


# ───────────────────────────── matematik ─────────────────────────────
def hermite(u, s0, s1):
    """g(0)=0, g(1)=1, g'(0)=s0, g'(1)=s1; u<0 ve u>1'de doğrusal uzatma (eğim sürekli)."""
    if u <= 0.0:
        return s0 * u
    if u >= 1.0:
        return 1.0 + s1 * (u - 1.0)
    u2 = u * u
    u3 = u2 * u
    return (u3 - 2 * u2 + u) * s0 + (-2 * u3 + 3 * u2) + (u3 - u2) * s1


def _pchip(ts, vs, t, d0=0.0, d1=0.0):
    """Tek boyutlu monoton kübik (Fritsch–Carlson) ara değer; uçlarda d0/d1 eğimiyle doğrusal uzatma."""
    n = len(ts)
    if n == 1:
        return vs[0]
    if t <= ts[0]:
        return vs[0] + d0 * (t - ts[0])
    if t >= ts[-1]:
        return vs[-1] + d1 * (t - ts[-1])
    i = 0
    while i < n - 2 and t > ts[i + 1]:
        i += 1
    delta = [(vs[j + 1] - vs[j]) / max(1e-9, ts[j + 1] - ts[j]) for j in range(n - 1)]

    def der(j):
        if j == 0:
            return d0
        if j == n - 1:
            return d1
        if delta[j - 1] * delta[j] <= 0:
            return 0.0
        w1 = 2 * (ts[j + 1] - ts[j]) + (ts[j] - ts[j - 1])
        w2 = (ts[j + 1] - ts[j]) + 2 * (ts[j] - ts[j - 1])
        return (w1 + w2) / (w1 / delta[j - 1] + w2 / delta[j])
    h = max(1e-9, ts[i + 1] - ts[i])
    s = (t - ts[i]) / h
    s2, s3 = s * s, s * s * s
    return ((2 * s3 - 3 * s2 + 1) * vs[i] + (s3 - 2 * s2 + s) * h * der(i) + (-2 * s3 + 3 * s2) * vs[i + 1] + (s3 - s2) * h * der(i + 1))


_NOISE = {}


def _noise_bank(seed, k):
    key = (seed, k)
    b = _NOISE.get(key)
    if b is None:
        rs = np.random.RandomState((zlib.crc32(f"{seed}:{k}".encode()) ^ 0x5bd1e995) & 0x7FFFFFFF)
        base = np.array([0.55, 1.15, 2.05, 3.35, 5.10])
        fr = base * (0.88 + 0.24 * rs.rand(len(base)))
        ph = rs.rand(len(base)) * 2 * math.pi
        am = np.array([1.0, 0.8, 0.55, 0.32, 0.16])
        b = (fr, ph, am / am.sum())
        _NOISE[key] = b
    return b


def hand_noise(t, seed, k):
    """[-1, 1] düzgün, deterministik titreşim (beş sinüs; seed + eksen k)."""
    fr, ph, am = _noise_bank(seed, k)
    return float(np.sum(am * np.sin(2 * math.pi * fr * t + ph)))


def slow_noise(t, seed, k):
    """[-1, 1] yavaş gezinme (≈0,09–0,35 Hz; elde mikro sürüklenme). hand_noise ile aynı bankadan, 1/6 frekans."""
    fr, ph, am = _noise_bank(seed + 7919, k)
    return float(np.sum(am[:4] * np.sin(2 * math.pi * fr[:4] / 6.0 * t + ph[:4])) / max(1e-6, am[:4].sum()))


def _u01(seed, k):
    """Tohumlu düzgün [0,1) (süreçler arası aynı)."""
    return (zlib.crc32(f"{seed}/{k}".encode()) & 0xFFFFFF) / float(0x1000000)


def auto_push(dur, seed=None):
    """Süreye bağlı itme miktarı: a·süre^b (AUTO_PUSH), tohumla ×0,88–1,12; AUTO_PUSH_LIM içinde."""
    a, b = AUTO_PUSH
    v = a * max(0.5, float(dur)) ** b
    if seed is not None:
        v *= 0.88 + 0.24 * _u01(seed, 1)
    return clamp(v, *AUTO_PUSH_LIM)


_PX_RULE = {"pan": (PAN_RATE, 110.0, 300.0), "truck": (26.0, 90.0, 240.0), "tilt": (20.0, 70.0, 180.0), "crane": (22.0, 80.0, 200.0)}


def auto_px(kind, dur, seed=None):
    """Süreye bağlı kayma (px): pan 34 px/sn (110–300), truck 26 (90–240), tilt 20 (70–180), crane 22 (80–200); tohumla ×0,88–1,12."""
    r, lo, hi = _PX_RULE[kind]
    v = clamp(r * float(dur), lo, hi)
    if seed is not None:
        v *= 0.88 + 0.24 * _u01(seed, 2)
    return v


# ───────────────────────────── durum ─────────────────────────────
class CamState:
    """Bir karenin kamera durumu. İçerik dönüşümü: nokta p → P + (dx,dy)·L + R(rot·L)·(1+(s−1)L)·(p−P)  (L: katman çarpanı; P: pivot).
    Ham kamera değerleri (x, y, zoom, rot) pano/theatre türleri için de açıktır."""
    __slots__ = ("x", "y", "zoom", "rot", "dx", "dy", "s", "pivot", "blur", "focus", "ws", "wdx", "wdy", "kind", "plan", "faxis", "mblur")

    def __init__(self):
        self.x = self.y = self.rot = 0.0
        self.zoom = 1.0
        self.dx = self.dy = 0.0
        self.s = 1.0
        self.pivot = None
        self.blur = 0.0
        self.focus = None
        self.ws, self.wdx, self.wdy = 1.0, 0.0, 0.0
        self.kind = None
        self.plan = None
        self.faxis = None             # rack: None (dairesel) | "y" (düzlemsel derinlik)
        self.mblur = None             # whip: (vx, vy) px/kare — deklanşör yönlü bulanıklığı için (compose okur)

    def layer(self, L):
        """Katman çarpanı L için (dx, dy, s, rot)."""
        return self.dx * L, self.dy * L, 1.0 + (self.s - 1.0) * L, self.rot * L


def wall_cover(wdx, wdy, hx=WALL_MG[0], hy=WALL_MG[1]):
    """Duvar görüntüsü (yarı boyut hx,hy; merkez çevresinde ölçek s, sonra (wdx,wdy) ötelenir) ekranı örtsün diye gereken en küçük ölçek."""
    need = 1.0
    for qx in (-W / 2, W / 2):
        for qy in (-H / 2, H / 2):
            rx, ry = qx - wdx, qy - wdy
            need = max(need, abs(rx) / hx, abs(ry) / hy)
    return need


def _anchor_t(cx, a):
    return float(cx.at(a))                                  # çözülemeyen çapa KeyError verir (sessiz 0 sn'ye düşmez)


def anchors_of(spec):
    """Spec'teki anlatı çapaları (anahtar kare çapaları, rack at=) — Program kurulurken doğrulanır."""
    pl = parse(spec)
    if pl is None:
        return []
    out = []
    if pl.kind == "keys":
        out += [a for a, _ in pl.p["keys"]]
    if pl.kind in ("rack", "whip") and pl.p.get("at") is not None:
        out.append(pl.p["at"])
    for it in (pl.p.get("shake") or []):
        out.append(it[0])
    return out


def _smoothstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def _px(plan, dur, seed=None):
    p = plan.p
    return p["px"] if p.get("px") is not None else auto_px(plan.kind, dur, seed)


def h_extent(plan, dur=6.0, seed=None):
    """Planın içerik düzleminde en büyük yatay kayması (px, tek yönde): şerit türlerinde örtme zumu için."""
    p, k = plan.p, plan.kind
    if k in ("pan", "truck"):
        return _px(plan, dur, seed) / 2.0
    if k == "whip":
        return p["px"] * (0.5 if p.get("where") == "mid" else 1.0)
    if k == "orbit":
        return ORBIT_R * math.sin(math.radians(p["deg"]) / 2.0)
    if k == "hand":
        return float(p["amp"]) + float(p.get("wander", 0.0))
    if k == "track":
        tr = TRACKS.get(p["id"])
        return max(abs(v[1][0]) for v in tr) if tr and not callable(tr) else 0.0
    if k == "keys":
        return max(abs(v[0]) for _, v in p["keys"])
    return 0.0


def _whip_in(tau, wd):
    """Savrulma girişi: 1 → 0, başta hızlı, ≈%6 aşma ve oturma (τ<0: aynı eğimle doğrusal)."""
    w = math.pi / (2.0 * max(0.05, wd))
    sg = 1.41 / max(0.05, wd)
    if tau < 0:
        return 1.0 + sg * (-tau)
    return math.exp(-sg * tau) * math.cos(w * tau)


def _whip_out(tau, wd, back=0.04):
    """Savrulma çıkışı: kısa hazırlık (−back) sonra hızlanarak 1'e (kesme ya da geçiş anında en hızlı); τ>wd doğrusal sürer."""
    a = 0.30 * wd
    if tau <= 0:
        return 0.0
    if tau < a:
        return -back * (3 * (tau / a) ** 2 - 2 * (tau / a) ** 3)
    u = (tau - a) / max(1e-6, wd - a)
    if u <= 1.0:
        return -back + (1.0 + back) * u ** 2.4
    return 1.0 + (1.0 + back) * 2.4 * (u - 1.0)


def _whip_mid(t, ta, wd, back=0.05, pre=0.16, over=0.07):
    """Çekim içinde savrulma: ta'dan önce hafif hazırlık, ta'da hızlı geçiş (ilk varış wd sn), hafif aşma ve oturma → −back … 1."""
    if t < ta:
        return -back * (3 * clamp((t - (ta - pre)) / pre) ** 2 - 2 * clamp((t - (ta - pre)) / pre) ** 3)
    L = -math.log(over)
    w = (math.pi - math.atan(math.pi / L)) / max(0.05, wd)
    sg = L * w / math.pi
    tau = t - ta
    e = math.exp(-sg * tau)
    return -back + (1.0 + back) * (1.0 - e * (math.cos(w * tau) + (sg / w) * math.sin(w * tau)))


def _prof_slopes(prof, cin, cout, kin=False, kout=False):
    """Hermite uç eğimleri. cin/cout: geçişle birleşen uç (CARRY); kin/kout: SERT KESMEYLE birleşen uç → en az CUT_SLOPE (yumuşatma yok)."""
    if prof in (None, "io"):
        s0, s1 = (CARRY if cin else 0.0), (CARRY if cout else 0.0)
    elif prof == "out":
        s0, s1 = 1.8, (0.30 if cout else 0.0)
    elif prof == "in":
        s0, s1 = (0.30 if cin else 0.0), 1.8
    else:
        s0, s1 = 1.0, 1.0                                    # lin
    if kin:
        s0 = max(s0, CUT_SLOPE)
    if kout:
        s1 = max(s1, CUT_SLOPE)
    return s0, s1


def _end_factor(c_, k_):
    """Anahtar kare / yol uçlarında eğim çarpanı: sert kesme → CUT_SLOPE, geçiş → CARRY, serbest uç → 0 (yumuşak duruş)."""
    return CUT_SLOPE if k_ else (CARRY if c_ else 0.0)


def auto_profile(seed):
    """Süreye bağlı (auto) itmede eğri çeşidi: io %45 · out %40 (hızlı giriş, uzun yumuşak çıkış) · in %15 (gerilim: hızlanan)."""
    r = _u01(seed, 3)
    return "io" if r < 0.45 else ("out" if r < 0.85 else "in")


def state(cx, spec, plan=None, kind=None, native_pan=False):
    """cam spec'i → CamState (cx: Ctx; t, dur, cam_in/out, seed, at()). spec None ise None. kind: çekim türü adı (şerit türlerinde örtme zumu).
    native_pan: yatay kayma türün kendi kaydırmasına devredildi (adapt) → genel yatay öteleme uygulanmaz."""
    plan = plan or parse(spec)
    if plan is None:
        return None
    t, dur = float(cx.t), max(1e-6, float(cx.dur))
    u = t / dur
    cin, cout = bool(getattr(cx, "cam_in", False)), bool(getattr(cx, "cam_out", False))
    kin, kout = bool(getattr(cx, "cut_in", False)), bool(getattr(cx, "cut_out", False))   # sert kesmeyle birleşen uç (compose._link_flags)
    seed = int(getattr(cx, "seed", 1))
    aseed = int(getattr(cx, "cam_seed", seed))             # kararlı tohum (parça/tam film aynı): süreye bağlı miktar, eğri çeşidi, odak kayması
    p = plan.p
    k = plan.kind
    auto_amt = k in ("push", "pull") and p.get("amt") is None and p.get("rate") is None
    prof = p.get("ease") or (auto_profile(aseed) if auto_amt else None)
    s0, s1 = _prof_slopes(prof, cin, cout, kin, kout)
    g = hermite(u, s0, s1)
    st = CamState()
    st.kind, st.plan = k, plan
    x = y = rot = 0.0
    z = 1.0
    kwall = WALL_K
    if k in ("push", "pull"):
        amt = p.get("amt")
        if amt is None:
            amt = float(p["rate"]) * dur if p.get("rate") is not None else auto_push(dur, aseed)
        z = 1.0 + amt * g if k == "push" else 1.0 + amt * (1.0 - g)
        if auto_amt and p.get("pivot") is None:             # süreye bağlı itmede odak merkezi tohumla hafif kayar (hep tam ortaya itme yok)
            st.pivot = (W / 2 + 260.0 * (_u01(aseed, 4) - 0.5), H / 2 + 140.0 * (_u01(aseed, 5) - 0.5))
    elif k in ("pan", "truck"):
        sgn = 1.0 if p["d"] == "r" else -1.0
        px = _px(plan, dur, aseed)
        x = 0.0 if native_pan else sgn * px * (g - 0.5)
        z = 1.0 + p.get("push", 0.02 if k == "pan" else 0.015) * g
        kwall = WALL_KIND[k]
    elif k in ("crane", "tilt"):
        sgn = -1.0 if p["d"] == "up" else 1.0               # kamera yukarı: y azalır, içerik aşağı akar
        y = sgn * _px(plan, dur, aseed) * (g - 0.5)
        z = 1.0 + p.get("push", 0.02) * g
        kwall = WALL_KIND[k]
    elif k == "whip":
        sgn = 1.0 if p["d"] == "r" else -1.0
        px, wd, where = float(p["px"]), float(p.get("dur", 0.30)), p.get("where", "in")
        if where == "in":
            x = -sgn * px * _whip_in(t, wd)
        elif where == "out":
            x = sgn * px * _whip_out(t - (dur - wd), wd)
        else:
            ta = _anchor_t(cx, p["at"]) if p.get("at") is not None else dur * 0.5
            x = sgn * px * (_whip_mid(t, ta, wd) - 0.5)
        z = 1.0 + 0.03 + p.get("push", 0.02) * g             # sabit %3 örtme + hafif itme (kenar açılmasın)
        kwall = WALL_KIND["whip"]
    elif k == "orbit":
        phi = math.radians(p["deg"]) * (g - 0.5) * p["sgn"]
        x = ORBIT_R * math.sin(phi)
        z = 1.0 + p.get("push", 0.03) * g
        rot = -math.degrees(phi) * 0.10
        kwall = -0.35
    elif k == "hand":
        a, wa = p["amp"], float(p.get("wander", 0.0))
        x = a * hand_noise(t, seed, 0) + wa * slow_noise(t, seed, 0)
        y = a * 0.75 * hand_noise(t, seed, 1) + wa * 0.7 * slow_noise(t, seed, 1)
        rot = 0.12 * slow_noise(t, seed, 2) if wa > 0 else 0.0
        pu = p.get("push")
        pu = 0.5 * auto_push(dur, aseed) if pu is None else float(pu)
        z = 1.0 + pu * g + (0.004 * slow_noise(t, seed, 3) if wa > 0 else 0.0)
    elif k == "rack":
        ra, rb = p["a"], p["b"]
        ta = p.get("at", None)
        t_a = _anchor_t(cx, ta) if ta is not None else dur * 0.30
        t_d = float(p.get("dur", max(0.8, dur * 0.34)))
        r = _smoothstep((t - t_a) / t_d)
        fx, fy = ra[0] + (rb[0] - ra[0]) * r, ra[1] + (rb[1] - ra[1]) * r
        z = 1.0 + p.get("push", 0.05) * g
        st.pivot = (fx, fy)
        sig = float(p.get("sigma", 5.0))
        st.blur = sig * (1.0 + 0.55 * math.sin(math.pi * r))
        st.focus = (fx, fy, float(p.get("r", 300.0)))
        st.faxis = p.get("axis")
    elif k == "track":
        tr = TRACKS.get(p["id"])
        if tr is None:
            if p["id"] not in _WARNED:
                _WARNED.add(p["id"])
                print(f"[cilt_cam] uyarı: bilinmeyen yol {p['id']!r} → 'sweep_r' kullanıldı")
            tr = TRACKS["sweep_r"]
        gc = clamp(g)
        if callable(tr):
            x, y, z, rot = tr(gc)
            if g != gc:                                   # ön-tur / aşım: uç eğimiyle doğrusal uzatma
                e = 0.002
                v1, v2 = (tr(gc), tr(gc + e)) if g < 0 else (tr(gc - e), tr(gc))
                sl = [(v2[c] - v1[c]) / e for c in range(4)]
                dg = (g - gc) * (_end_factor(cin, kin) if g < 0 else _end_factor(cout, kout))
                x, y, z, rot = x + sl[0] * dg, y + sl[1] * dg, max(0.05, z + sl[2] * dg), rot + sl[3] * dg
        else:
            us = [kk[0] for kk in tr]
            ch = [[kk[1][c] for kk in tr] for c in range(4)]
            ch[2] = [math.log(max(1e-6, v)) for v in ch[2]]
            out = []
            for c in range(4):
                seg0 = (ch[c][1] - ch[c][0]) / max(1e-9, us[1] - us[0]) if len(us) > 1 else 0.0
                seg1 = (ch[c][-1] - ch[c][-2]) / max(1e-9, us[-1] - us[-2]) if len(us) > 1 else 0.0
                d0 = seg0 * _end_factor(cin, kin)
                d1 = seg1 * _end_factor(cout, kout)
                v = _pchip(us, ch[c], gc, d0, d1)
                # uzatma: g dışına çıkıldıysa uç eğimiyle doğrusal sürdür
                if g < 0:
                    v = ch[c][0] + d0 * g
                elif g > 1:
                    v = ch[c][-1] + d1 * (g - 1.0)
                out.append(v)
            x, y, z, rot = out[0], out[1], math.exp(out[2]), out[3]
    elif k == "keys":
        ks = sorted(((_anchor_t(cx, a), v) for a, v in p["keys"]), key=lambda kv: kv[0])
        ts = [kv[0] for kv in ks]
        for i in range(1, len(ts)):
            if ts[i] <= ts[i - 1] + 1e-4:
                ts[i] = ts[i - 1] + 1e-4
        chans = [[kv[1][c] for kv in ks] for c in range(4)]
        chans[2] = [math.log(max(1e-6, v)) for v in chans[2]]
        out = []
        for c in range(4):
            if len(ts) > 1:
                sl0 = (chans[c][1] - chans[c][0]) / (ts[1] - ts[0])
                sl1 = (chans[c][-1] - chans[c][-2]) / (ts[-1] - ts[-2])
            else:
                sl0 = sl1 = 0.0
            out.append(_pchip(ts, chans[c], t, sl0 * _end_factor(cin, kin), sl1 * _end_factor(cout, kout)))
        x, y, z, rot = out[0], out[1], math.exp(out[2]), out[3]
    # ek: drift, hand katkısı, darbe sarsıntısı (her ön ayarda opts ile)
    dr = p.get("drift")
    if dr:
        x += dr[0] * (t - dur / 2)
        y += dr[1] * (t - dur / 2)
    if k != "hand" and p.get("hand"):
        a = float(p["hand"]) if not isinstance(p["hand"], bool) else 1.5
        x += a * hand_noise(t, seed, 0)
        y += a * 0.75 * hand_noise(t, seed, 1)
    if p.get("shake"):
        import anim
        for j, it in enumerate(p["shake"]):
            sx_, sy_ = anim.shake(t, _anchor_t(cx, it[0]), float(it[2]) if len(it) > 2 else 0.25, float(it[1]), seed=seed * 31 + j)
            x += sx_
            y += sy_
    if kind and base_kind(kind) in BAND_KINDS and not native_pan:   # şerit uçları açığa çıkmasın: kaymanın GERÇEK kapsamını örtecek sabit zum
        z *= _band_cover(cx, plan, dur)
    st.x, st.y, st.zoom, st.rot = x, y, z, rot
    st.dx, st.dy, st.s = -x, -y, z
    pv = p.get("pivot")
    if pv is not None and st.pivot is None:
        st.pivot = (float(pv[0]), float(pv[1]))
    # duvar (paralaks): içeriğin WALL_K'sı; zoom'un %45'i; ekranı örtecek şekilde
    st.wdx, st.wdy = st.dx * kwall, st.dy * kwall
    ws0 = 1.0 + (z - 1.0) * 0.45
    st.ws = max(ws0, wall_cover(st.wdx, st.wdy) / 1.015)
    return st


class _At:
    """state()'i başka bir yerel saatte değerlendirmek için hafif Ctx vekili (çapalar aynı çekimde çözülür)."""
    __slots__ = ("t", "dur", "cam_in", "cam_out", "cut_in", "cut_out", "seed", "cam_seed", "_cx")

    def __init__(self, cx, t):
        self._cx = cx
        self.t, self.dur = t, cx.dur
        self.cam_in, self.cam_out = getattr(cx, "cam_in", False), getattr(cx, "cam_out", False)
        self.cut_in, self.cut_out = getattr(cx, "cut_in", False), getattr(cx, "cut_out", False)
        self.seed = getattr(cx, "seed", 1)
        self.cam_seed = getattr(cx, "cam_seed", self.seed)

    def at(self, a, key=None, off=0.0):
        return self._cx.at(a, key, off)


_COVER = {}


def _band_cover(cx, plan, dur):
    """Şerit türünde genel yatay ötelemenin (pan/truck/whip/orbit/hand + drift/hand/sarsıntı ekleri) GERÇEK en büyük |x|'ini çekimin görünür
    aralığında (−0,1 … süre+0,7 sn: deklanşör alt örnekleri ve "after" geçişlerindeki uzatma dâhil) sayısal olarak bulur → şerit ucunu kapatan sabit zum.
    (Eski h_extent yalnız ±px/2 varsayıyordu; geçiş uzatması, drift ve sarsıntı şerit ucunu açıyordu — kurul tur 2 AN2-K1 / TE1-Y5.) Önbellekli."""
    key = (repr(plan.spec), round(float(dur), 3), bool(getattr(cx, "cam_in", False)), bool(getattr(cx, "cam_out", False)),
           bool(getattr(cx, "cut_in", False)), bool(getattr(cx, "cut_out", False)), int(getattr(cx, "seed", 1)), int(getattr(cx, "cam_seed", 1)))
    v = _COVER.get(key)
    if v is None:
        ext = 0.0
        n = 48
        for j in range(n + 1):
            tt = -0.1 + (float(dur) + 0.8) * j / n
            s_ = state(_At(cx, tt), None, plan=plan, kind=None)
            ext = max(ext, abs(s_.x))
        if plan.kind == "hand" or plan.p.get("hand"):          # titreşim tepeleri örnek aralarına düşebilir: genlik payı
            ext += float(plan.p.get("amp", 0.0) if plan.kind == "hand" else (plan.p["hand"] if not isinstance(plan.p["hand"], bool) else 1.5))
        v = 1.0 + (ext + 2.0) / (W / 2.0)
        if len(_COVER) > 512:
            _COVER.clear()
        _COVER[key] = v
    return v


_PROBE = [(0.0, 0.0), (-W / 2, -H / 2), (W / 2, -H / 2), (-W / 2, H / 2), (W / 2, H / 2), (-W / 2, 0.0), (W / 2, 0.0), (0.0, -H / 2), (0.0, H / 2)]


def _map_pts(st):
    px, py = st.pivot or (W / 2, H / 2)
    cr, sr = math.cos(math.radians(st.rot)), math.sin(math.radians(st.rot))
    out = []
    for qx, qy in _PROBE:
        X, Y = W / 2 + qx - px, H / 2 + qy - py
        out.append((px + st.dx + st.s * (cr * X - sr * Y), py + st.dy + st.s * (sr * X + cr * Y)))
    return out


def screen_speed(cx, spec=None, plan=None, kind=None, dt=1.0 / 24.0):
    """Kamera kaynaklı ekran hızı (px/kare, 1920 ölçeği) cx.t'de: içerik dönüşümünün t ± dt/2 arası en büyük nokta yer değiştirmesi (köşe/kenar/merkez).
    Dönüş: (en büyük, merkez vx, merkez vy) — deklanşör (compose) yönlü bulanıklık için. spec yoksa (0, 0, 0)."""
    plan = plan or parse(spec)
    if plan is None:
        return 0.0, 0.0, 0.0
    a = state(_At(cx, cx.t - dt / 2), None, plan=plan, kind=kind)
    b = state(_At(cx, cx.t + dt / 2), None, plan=plan, kind=kind)
    pa, pb = _map_pts(a), _map_pts(b)
    vmax = max(math.hypot(q[0] - r[0], q[1] - r[1]) for q, r in zip(pa, pb))
    return vmax, pb[0][0] - pa[0][0], pb[0][1] - pa[0][1]



# ───────────────────────────── çekim hazırlığı (ckind sarmalayıcısı çağırır) ─────────────────────────────
def _sig(fn):
    import inspect
    try:
        return inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return {}


SKYLINE_MAX_PX = 500.0       # skyline kendi kaydırması cilt_city.PW_EXTRA (520 px) ile sınırlı: daha büyük kayma yerleşik çevrilemez


def _dir_sign(v):
    """Tür dir parametresi → ±1 (1 / "r" / "R" → +1; -1 / "l" → −1); tanınmazsa None."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return 1 if v >= 0 else -1
    if isinstance(v, str) and v:
        return 1 if v[0].lower() == "r" else (-1 if v[0].lower() == "l" else None)
    return None


def _native_skyline(plan, kw, raw, px):
    """skyline yerleşik kaydırma (4 katman paralaks, şerit ucu açılmaz). Sahne türün pan= miktarını da yazmışsa (P1/P6/P7'de yaygın: aynı hareket iki kez
    beyan ediliyordu → genel öteleme + tür kaydırması ÜST ÜSTE biniyordu) kamera beyanı geçerlidir; dir= verilmişse yönle çelişmemeli; x0 verilmişse çevrilmez."""
    ps = _sig(raw)
    if not all(k in ps for k in ("pan", "dir", "x0")) or "x0" in kw or px > SKYLINE_MAX_PX:
        return False
    sg = 1 if plan.p["d"] == "r" else -1
    if "dir" in kw and _dir_sign(kw["dir"]) not in (None, sg):
        return False
    kw["pan"] = float(px)
    kw["dir"] = sg
    kw["x0"] = 0.0 if sg > 0 else float(px)
    return True


def _native_procession(plan, kw, raw, px):
    """procession yerleşik kaydırma: pan=(yön, toplam px). Türün dir= yönüyle çelişen beyanda (ör. dir='l' alay + ("truck","r")) çevrilmez: alayın yürüyüş yönü
    sahne kararıdır (§1-6); o zaman genel öteleme + örtme zumu uygulanır."""
    ps = _sig(raw)
    if "pan" not in ps or "pan" in kw:
        return False
    if "dir" in kw and _dir_sign(kw["dir"]) not in (None, 1 if plan.p["d"] == "r" else -1):
        return False
    kw["pan"] = (plan.p["d"], float(px))
    return True


def _native_frieze(plan, kw, raw, dur, px):
    ps = _sig(raw)
    if plan.p["d"] != "r" or not all(k in ps for k in ("speed", "x0")) or any(k in kw for k in ("speed", "x0")):
        return False
    kw["speed"] = float(px) / max(1.0, dur)
    return True


def _inner_raw(bk, kind_name, raw):
    """Sarmalanmış şerit türü (p1_procession …) için iç türün çiğ çizim işlevi (imza denetimi); sarmalanmamışsa raw."""
    if bk == kind_name:
        return raw
    try:
        import shots as SH
        fn = SH.KINDS.get(bk)
    except Exception:
        fn = None
    return getattr(fn, "_raw", fn) if fn is not None else None


def attach(cx, kind_name, kw, raw=None):
    """cx.cam_state'i hesapla (spec varsa). map: kendi drift'ini sıfırla (çift itme olmasın). OWN_CAMERA türleri: durum uygulanmaz.
    Şerit türlerinde (skyline / procession / frieze; pN_ önekli sarmalayıcılar da TABAN adla — ENG-D) ("pan"|"truck", "r"|"l"[, px]) türün kendi
    kaydırmasına çevrilir (gerçek paralaks; şerit ucu açılmaz); çevrilemezse genel öteleme + kaymanın gerçek kapsamından örtme zumu (_band_cover)."""
    spec = getattr(cx, "cam_spec", None)
    cx.cam_state = None
    if spec is None or kind_name in OWN_CAMERA:
        return None
    plan = parse(spec)
    native = False
    bk = base_kind(kind_name)
    if plan is not None and plan.kind in ("pan", "truck") and bk in BAND_KINDS:
        braw = _inner_raw(bk, kind_name, raw)
        if braw is not None:
            px = _px(plan, float(cx.dur), int(getattr(cx, "cam_seed", getattr(cx, "seed", 1))))
            if bk == "skyline":
                native = _native_skyline(plan, kw, braw, px)
            elif bk == "procession":
                native = _native_procession(plan, kw, braw, px)
            elif bk == "frieze":
                native = _native_frieze(plan, kw, braw, float(cx.dur), px)
    cx.cam_state = state(cx, spec, plan=plan, kind=kind_name, native_pan=native)
    if bk == "map":
        if not kw.get("cams") and "drift" not in kw:
            kw["drift"] = (0.0, 0.0, 0.0)
        try:                                                # doku dünya kilidi için çekimin başvuru zumu (anahtar kare zumlarının geometrik ortası)
            zs = [float(v[2]) for _, v in (kw.get("cams") or []) if len(v) > 2]
            v0 = kw.get("cam", kw.get("view"))
            if not zs and isinstance(v0, (tuple, list)) and len(v0) == 3:
                zs = [float(v0[2])]
            if zs:
                cx._map_zref = math.exp(sum(math.log(max(1e-6, z_)) for z_ in zs) / len(zs))
        except Exception:
            pass
    return cx.cam_state


@contextlib.contextmanager
def map_patch(cx):
    """map türü kendi mapsk.Cam'ini kullanır: oluşturulan her Cam'e ekran-uzayı kayma/zoom eklenir (içerik +dx kayar → dünya merkezi −dx/zoom).
    ENG-D: son oluşturulan Cam (çizimde kullanılan) cx.world_xf'e yazılır → compose kâğıt dokusunu harita dünyasına kilitler (kurul tur 2 TE1 §7)."""
    st = getattr(cx, "cam_state", None)
    move = not (st is None or (abs(st.dx) < 1e-3 and abs(st.dy) < 1e-3 and abs(st.s - 1.0) < 1e-6))
    import mapsk
    orig = mapsk.Cam
    ctx_ = cx

    class _Cam(orig):
        def __init__(self, lon, lat, zoom, rot=0.0, cx=W / 2, cy=H / 2):
            z = zoom * st.s if move else zoom
            super().__init__(lon, lat, z, rot, cx, cy)
            if move:
                self.wx -= st.dx / z
                self.wy -= st.dy / z
            try:
                ctx_.world_xf = ("map", float(self.wx), float(self.wy), float(self.zoom), float(self.cx), float(self.cy))
            except Exception:
                pass
    mapsk.Cam = _Cam
    try:
        yield
    finally:
        mapsk.Cam = orig


# ───────────────────────────── odak (rack) bulanıklığı ─────────────────────────────
_MASK = {}


def _focus_mask(fx, fy, r, axis=None):
    """(270, 480) float32: odak dairesi (axis=None) ya da odak bandı (axis="y": düzlemsel derinlik, yalnız |y − fy|) içinde 1, dışında 0 (yumuşak kenar); 1/4 çözünürlük."""
    sh = (H // 4, W // 4)
    yy, xx = np.mgrid[0:sh[0], 0:sh[1]].astype(np.float32)
    d = np.abs(yy * 4 - fy) if axis == "y" else np.hypot(xx * 4 - fx, yy * 4 - fy)
    m = np.clip((r * 1.45 - d) / (r * 0.95), 0.0, 1.0)
    return m * m * (3 - 2 * m)


def postfx(cx):
    """Kare çizildikten sonra: rack için çevre bulanıklığı (odak dairesi keskin). Tam-kare skia bulanıklığı ~230 ms; burada 1/4 çözünürlükte cv2 (≈15 ms)."""
    st = getattr(cx, "cam_state", None)
    if st is None or st.blur < 0.5 or st.focus is None:
        return
    import cv2
    import skia
    f = cx.f
    arr = f.surf.makeImageSnapshot().toarray(colorType=skia.ColorType.kBGRA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType)
    arr = np.ascontiguousarray(arr)
    small = cv2.resize(arr, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    sig = max(0.4, st.blur / 4.0)
    small = cv2.GaussianBlur(small, (0, 0), sig)
    blur = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)
    fx, fy, r = st.focus
    m = _focus_mask(fx, fy, r, getattr(st, "faxis", None))
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    out = cv2.blendLinear(arr, blur, m, 1.0 - m)
    out = np.ascontiguousarray(out)
    im = skia.Image.fromarray(out, colorType=skia.ColorType.kBGRA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType)
    f.c.save()
    f.c.resetMatrix()
    f.c.drawImage(im, 0, 0, skia.SamplingOptions(), skia.Paint(BlendMode=skia.BlendMode.kSrc))
    f.c.restore()


# ───────────────────────────── statik analiz (qa_flow) ─────────────────────────────
def describe(spec, dur=None):
    """qa_flow için: {'kind', 'family', 'dir', 'scale', 'shift', 'h', 'v'} (yaklaşık toplam ölçek değişimi oranı ve kayma px) ya da None.
    dur: çekim süresi (süreye bağlı miktarlar için; yoksa 6 sn varsayılır)."""
    pl = parse(spec)
    if pl is None:
        return None
    dd = 6.0 if dur is None else max(0.5, float(dur))
    p, k = pl.p, pl.kind
    d = dict(kind=k, dir=None, scale=0.0, shift=0.0, h=0.0, v=0.0)
    if k in ("push", "pull"):
        amt = p.get("amt")
        if amt is None:
            amt = float(p["rate"]) * dd if p.get("rate") is not None else auto_push(dd)
        d["scale"] = amt
        d["dir"] = "in" if k == "push" else "out"
        d["auto"] = p.get("amt") is None
    elif k in ("pan", "truck"):
        px = _px(pl, dd)
        d.update(shift=px, dir=p["d"], h=(1 if p["d"] == "r" else -1) * px, scale=p.get("push", 0.02 if k == "pan" else 0.015))
    elif k in ("crane", "tilt"):
        px = _px(pl, dd)
        d.update(shift=px, dir=p["d"], v=(1 if p["d"] == "up" else -1) * px, scale=p.get("push", 0.02))
    elif k == "whip":
        d.update(shift=p["px"], dir=p["d"], h=(1 if p["d"] == "r" else -1) * p["px"], scale=0.03)
    elif k == "orbit":
        d.update(shift=2 * ORBIT_R * math.sin(math.radians(p["deg"]) / 2), scale=p.get("push", 0.03), dir="orbit")
    elif k == "hand":
        pu = p.get("push")
        d.update(shift=p["amp"] * 2 + float(p.get("wander", 0.0)) * 2, scale=(0.5 * auto_push(dd) if pu is None else pu), dir="hand2" if p["strong"] else "hand")
    elif k == "rack":
        d.update(shift=math.hypot(p["b"][0] - p["a"][0], p["b"][1] - p["a"][1]), scale=p.get("push", 0.05), dir="rack")
    elif k == "track":
        tr = TRACKS.get(p["id"])
        d["dir"] = "track"
        if tr and not callable(tr):
            xs = [v[1][0] for v in tr]
            ys = [v[1][1] for v in tr]
            zs = [v[1][2] for v in tr]
            d.update(shift=max(max(xs) - min(xs), max(ys) - min(ys)), scale=max(zs) / min(zs) - 1.0)
            d["h"] = xs[-1] - xs[0]                       # + : kamera sağa
            d["v"] = -(ys[-1] - ys[0])                    # + : kamera yukarı
            d["zdir"] = 1 if zs[-1] > zs[0] * 1.005 else (-1 if zs[-1] < zs[0] / 1.005 else 0)
        else:
            d["known"] = tr is not None
    elif k == "keys":
        ks = [v for _, v in p["keys"]]
        xs = [v[0] for v in ks]
        ys = [v[1] for v in ks]
        zs = [v[2] for v in ks]
        d.update(shift=max(max(xs) - min(xs), max(ys) - min(ys)), scale=max(zs) / min(zs) - 1.0, dir="keys")
        d["h"] = xs[-1] - xs[0]
        d["v"] = -(ys[-1] - ys[0])
        d["zdir"] = 1 if zs[-1] > zs[0] * 1.005 else (-1 if zs[-1] < zs[0] / 1.005 else 0)
    d["family"] = _family_of(d)
    return d


def _family_of(d):
    k = d["kind"]
    if k in ("push", "pull", "pan", "truck", "crane", "tilt", "whip", "orbit", "hand", "rack"):
        return k
    # track / keys: baskın harekete göre (ölçek ≥ %5 ve kayma < 140 px → itme/çekme; değilse yatay → pan, dikey → crane)
    sc, sh = d.get("scale", 0.0), d.get("shift", 0.0)
    if sc >= 0.05 and sh < 140.0:
        return "pull" if d.get("zdir", 1) < 0 else "push"
    if sh < 20.0 and sc < 0.02:
        return "static"
    return "pan" if abs(d.get("h", 0.0)) >= abs(d.get("v", 0.0)) else "crane"


def family(spec, dur=None):
    """cam spec'inin hareket ailesi: push | pull | pan | truck | tilt | crane | whip | orbit | hand | rack | static (anahtar kareliler baskın harekete göre) | None."""
    d = describe(spec, dur)
    return d["family"] if d else None


def motion_ok(spec, dur=None):
    """SPEC §1-1(a): ≥%6 ölçek ya da ≥120 px kayma (süreye bağlı miktarlar dur ile hesaplanır)."""
    d = describe(spec, dur)
    return bool(d) and (d["scale"] >= 0.06 - 1e-9 or d["shift"] >= 120.0 - 1e-9)


# ───────────────────────────── otomatik seçim (cam= verilmemiş çekimler) ─────────────────────────────
AUTO_W = dict(push=0.28, pull=0.13, pan=0.18, truck=0.11, tilt=0.06, crane=0.06, hand=0.12, orbit=0.06)
OPPOSITE = dict(push="pull", pull="push", tilt="crane", crane="tilt")


def auto_spec(kind, dur, seed, prev=None, hdir="r", vdir="up"):
    """cam= verilmemiş çekim için tohumlu, ağırlıklı hareket (compose.Program çağırır). prev: önceki çekimin ailesi (aynı aile ve push↔pull art arda seçilmez).
    hdir/vdir: bölümün baskın yatay/dikey yönü (yön sözleşmesi §1-6; açık cam'lerden devralınır). Miktarlar süreye bağlı (auto_push / auto_px).
    Dönüş: cam spec (tuple)."""
    w = dict(AUTO_W)
    if kind in BAND_KINDS:                                  # şerit türleri: pan yerleşik kaydırmaya çevrilir (gerçek paralaks) — tohumlu seçim P2–P7'de değişmesin diye taban ad değil
        w.update(pan=0.50, truck=0.0, orbit=0.0, tilt=0.0)
    if kind == "map":
        w.update(orbit=0.0, tilt=0.0, truck=0.06)
    if dur < 2.6:                                           # kısa çekim: hızlı itme/çekme/kayma; yörünge ve dikey yok
        w.update(orbit=0.0, tilt=0.0, crane=0.0)
    if prev:
        w[prev] = 0.0
        if prev in OPPOSITE:
            w[OPPOSITE[prev]] = 0.0
    tot = sum(w.values())
    r = _u01(seed, 11) * tot
    fam = "push"
    for k_, v in w.items():
        if r < v:
            fam = k_
            break
        r -= v
    if fam in ("push", "pull"):
        return (fam,)
    if fam in ("pan", "truck"):
        return (fam, hdir)
    if fam == "tilt":
        return ("tilt", vdir)
    if fam == "crane":
        return ("crane", vdir)
    if fam == "orbit":
        return ("orbit", round((4.0 + 4.0 * _u01(seed, 12)) * (1 if hdir == "r" else -1), 1))
    return ("hand",)


# ───────────────────────────── öz sınama ─────────────────────────────
def _selftest():
    """python3 cilt_cam.py → her ön ayar için: t<0 / t>dur uzatması çökmesin, uç hızları sürekli (geçişte kamera devri), hand deterministik."""
    class _Cx:
        def __init__(self, t, dur, cin, cout, seed=7):
            self.t, self.dur, self.cam_in, self.cam_out, self.seed = t, dur, cin, cout, seed

        def at(self, a, key=None, off=0.0):
            return float(a) + off
    specs = ["push", "pull", ("pan", "r", 160), ("pan", "l", 160), ("crane", "up", 130), ("crane", "down", 130), ("orbit", 10), "hand", "hand2",
             ("rack", (500, 500), (1400, 500)), ("track", "sweep_r"), [(0, (0, 0, 1, 0)), (3, (80, -30, 1.1, 0)), (6, (160, -60, 1.2, 2.0))]]
    ok = True
    for sp in specs:
        pl = parse(sp)
        dur = 6.0
        # t<0 : hız sürekliliği (carry-in) — t=0'daki sayısal türev ile t=-0.05'teki türev yakın olmalı
        def pos(t, cin, cout):
            st = state(_Cx(t, dur, cin, cout), sp)
            return st.x, st.y, math.log(st.zoom), st.rot
        for cin, cout in ((True, True), (False, False)):
            v_neg = [(a - b) / 0.04 for a, b in zip(pos(-0.02, cin, cout), pos(-0.06, cin, cout))]
            v_pos = [(a - b) / 0.04 for a, b in zip(pos(0.06, cin, cout), pos(0.02, cin, cout))]
            v_end_a = [(a - b) / 0.04 for a, b in zip(pos(dur - 0.02, cin, cout), pos(dur - 0.06, cin, cout))]
            v_end_b = [(a - b) / 0.04 for a, b in zip(pos(dur + 0.06, cin, cout), pos(dur + 0.02, cin, cout))]
            if pl.kind == "hand":
                continue
            jump = max(abs(a - b) for a, b in zip(v_neg, v_pos))
            jump2 = max(abs(a - b) for a, b in zip(v_end_a, v_end_b))
            vmid = [(a - b) / 0.04 for a, b in zip(pos(dur / 2 + 0.02, cin, cout), pos(dur / 2 - 0.02, cin, cout))]
            scale = max(1e-9, max(abs(x) for x in vmid))                  # tipik (orta) hız: süreksizlik buna göre küçük olmalı
            # taşıma açıkken hız ≠ 0 olmalı; yumuşak durmada ≈ 0
            moving = max(abs(x) for x in v_pos) > 1e-4 if cin else True
            print(f"{str(sp)[:34]:34s} cin={int(cin)} cout={int(cout)}  hız süreksizliği(giriş) {jump:8.3f}  (çıkış) {jump2:8.3f}  hareketli={moving}")
            ok = ok and jump <= 0.15 * scale + 0.02 and jump2 <= 0.15 * scale + 0.02
        # hand determinizmi
        a1, a2 = pos(1.234, False, False), pos(1.234, False, False)
        assert a1 == a2
    print("ÖZ SINAMA:", "GEÇTİ" if ok else "KALDI")
    return ok


if __name__ == "__main__":
    _selftest()
