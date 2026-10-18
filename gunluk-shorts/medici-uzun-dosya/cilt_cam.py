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
Tüm biçimlerde son eleman isteğe bağlı opts sözlüğü olabilir: pivot=(x,y), push=0.03 (pan/crane ek itme), hand=genlik, drift=(dx,dy) (px, itme ile birlikte).

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
BASE_PUSH = 0.07
HAND_BASE = 0.06              # elde kamerada altta yatan yavaş itme
ORBIT_R = 1000.0              # yörünge yarıçapı (px, içerik düzleminde)
WALL_K = 0.40                 # duvar paralaks çarpanı (içeriğe göre)
WALL_MG = (W / 2 + 100.0, H / 2 + 100.0)     # cilt_wall.MG = 100 → duvar görüntüsünün yarı boyutu

TRACKS = {}                   # yol_id → [(u 0..1, (x, y, zoom, rot)), …]  | callable(u) → (x, y, zoom, rot)
BAND_KINDS = {"skyline", "frieze", "procession"}   # tam genişlikte yatay şerit çizen türler: yatay kamera kayması şerit uçlarını açığa çıkarır → sabit örtme zumu (yeni şerit türleri buraya eklenir)
OWN_CAMERA = {"pano", "build"}        # kendi kamera yolu olan türler (pano: cams=, build: orbit=/crane): cam= alanı kabul edilir, cx.cam_spec'te durur ama CM.Cam'e UYGULANMAZ (çift hareket olmasın)
_WARNED = set()


# ───────────────────────────── yollar ─────────────────────────────
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
            return Plan(h, spec, amt=float(a[1]) if len(a) > 1 else BASE_PUSH, **o)
        if h == "pan":
            d = _dir(a[1] if len(a) > 1 else "r", ("r", "l"))
            return Plan("pan", spec, d=d, px=float(a[2]) if len(a) > 2 else 140.0, **o)
        if h == "crane":
            d = _dir(a[1] if len(a) > 1 else "up", ("up", "down"))
            return Plan("crane", spec, d=d, px=float(a[2]) if len(a) > 2 else 120.0, **o)
        if h == "orbit":
            return Plan("orbit", spec, deg=min(12.0, abs(float(a[1]))) if len(a) > 1 else 8.0, sgn=1.0 if len(a) < 2 or float(a[1]) >= 0 else -1.0, **o)
        if h in ("hand", "hand2"):
            amp = 1.5 if h == "hand" else 4.0
            if len(a) > 1:
                amp = float(a[1])
            o.setdefault("push", HAND_BASE)
            return Plan("hand", spec, amp=amp, strong=(h == "hand2"), **o)
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


# ───────────────────────────── durum ─────────────────────────────
class CamState:
    """Bir karenin kamera durumu. İçerik dönüşümü: nokta p → P + (dx,dy)·L + R(rot·L)·(1+(s−1)L)·(p−P)  (L: katman çarpanı; P: pivot).
    Ham kamera değerleri (x, y, zoom, rot) pano/theatre türleri için de açıktır."""
    __slots__ = ("x", "y", "zoom", "rot", "dx", "dy", "s", "pivot", "blur", "focus", "ws", "wdx", "wdy", "kind", "plan")

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
    if pl.kind == "keys":
        return [a for a, _ in pl.p["keys"]]
    if pl.kind == "rack" and pl.p.get("at") is not None:
        return [pl.p["at"]]
    return []


def _smoothstep(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def h_extent(plan):
    """Planın içerik düzleminde en büyük yatay kayması (px, tek yönde): şerit türlerinde örtme zumu için."""
    p, k = plan.p, plan.kind
    if k == "pan":
        return p["px"] / 2.0
    if k == "orbit":
        return ORBIT_R * math.sin(math.radians(p["deg"]) / 2.0)
    if k == "hand":
        return float(p["amp"])
    if k == "track":
        tr = TRACKS.get(p["id"])
        return max(abs(v[1][0]) for v in tr) if tr and not callable(tr) else 0.0
    if k == "keys":
        return max(abs(v[0]) for _, v in p["keys"])
    return 0.0


def state(cx, spec, plan=None, kind=None, native_pan=False):
    """cam spec'i → CamState (cx: Ctx; t, dur, cam_in/out, seed, at()). spec None ise None. kind: çekim türü adı (şerit türlerinde örtme zumu).
    native_pan: yatay kayma türün kendi kaydırmasına devredildi (adapt) → genel yatay öteleme uygulanmaz."""
    plan = plan or parse(spec)
    if plan is None:
        return None
    t, dur = float(cx.t), max(1e-6, float(cx.dur))
    u = t / dur
    cin, cout = bool(getattr(cx, "cam_in", False)), bool(getattr(cx, "cam_out", False))
    s0, s1 = (CARRY if cin else 0.0), (CARRY if cout else 0.0)
    g = hermite(u, s0, s1)
    seed = int(getattr(cx, "seed", 1))
    p = plan.p
    k = plan.kind
    st = CamState()
    st.kind, st.plan = k, plan
    x = y = rot = 0.0
    z = 1.0
    kwall = WALL_K
    if k == "push":
        z = 1.0 + p["amt"] * g
    elif k == "pull":
        z = 1.0 + p["amt"] * (1.0 - g)
    elif k == "pan":
        sgn = 1.0 if p["d"] == "r" else -1.0
        x = 0.0 if native_pan else sgn * p["px"] * (g - 0.5)
        z = 1.0 + p.get("push", 0.02) * g
    elif k == "crane":
        sgn = -1.0 if p["d"] == "up" else 1.0           # kamera yukarı: y azalır, içerik aşağı akar
        y = sgn * p["px"] * (g - 0.5)
        z = 1.0 + p.get("push", 0.02) * g
    elif k == "orbit":
        phi = math.radians(p["deg"]) * (g - 0.5) * p["sgn"]
        x = ORBIT_R * math.sin(phi)
        z = 1.0 + p.get("push", 0.03) * g
        rot = -math.degrees(phi) * 0.10
        kwall = -0.35
    elif k == "hand":
        a = p["amp"]
        x = a * hand_noise(t, seed, 0)
        y = a * 0.75 * hand_noise(t, seed, 1)
        z = 1.0 + p.get("push", HAND_BASE) * g
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
                dg = (g - gc) * (CARRY if (cin if g < 0 else cout) else 0.0)
                x, y, z, rot = x + sl[0] * dg, y + sl[1] * dg, max(0.05, z + sl[2] * dg), rot + sl[3] * dg
        else:
            us = [kk[0] for kk in tr]
            ch = [[kk[1][c] for kk in tr] for c in range(4)]
            ch[2] = [math.log(max(1e-6, v)) for v in ch[2]]
            out = []
            for c in range(4):
                seg0 = (ch[c][1] - ch[c][0]) / max(1e-9, us[1] - us[0]) if len(us) > 1 else 0.0
                seg1 = (ch[c][-1] - ch[c][-2]) / max(1e-9, us[-1] - us[-2]) if len(us) > 1 else 0.0
                d0 = seg0 * (CARRY if cin else 0.0)
                d1 = seg1 * (CARRY if cout else 0.0)
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
            out.append(_pchip(ts, chans[c], t, sl0 * (CARRY if cin else 0.0), sl1 * (CARRY if cout else 0.0)))
        x, y, z, rot = out[0], out[1], math.exp(out[2]), out[3]
    # ek: drift, hand katkısı (her ön ayarda opts ile)
    dr = p.get("drift")
    if dr:
        x += dr[0] * (t - dur / 2)
        y += dr[1] * (t - dur / 2)
    if k != "hand" and p.get("hand"):
        a = float(p["hand"]) if not isinstance(p["hand"], bool) else 1.5
        x += a * hand_noise(t, seed, 0)
        y += a * 0.75 * hand_noise(t, seed, 1)
    if kind in BAND_KINDS and not native_pan:              # şerit uçları açığa çıkmasın: kaymayı örtecek sabit zum
        z *= 1.0 + h_extent(plan) / (W / 2.0) * 1.03
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


# ───────────────────────────── çekim hazırlığı (ckind sarmalayıcısı çağırır) ─────────────────────────────
def _sig(fn):
    import inspect
    try:
        return inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return {}


def _native_skyline(plan, kw, raw):
    ps = _sig(raw)
    if not all(k in ps for k in ("pan", "dir", "x0")) or any(k in kw for k in ("pan", "dir", "x0")) or plan.p["px"] > 500:
        return False
    kw["pan"] = float(plan.p["px"])
    kw["dir"] = 1 if plan.p["d"] == "r" else -1
    kw["x0"] = 0.0 if plan.p["d"] == "r" else float(plan.p["px"])
    return True


def _native_procession(plan, kw, raw):
    ps = _sig(raw)
    if "pan" not in ps or "pan" in kw:
        return False
    kw["pan"] = (plan.p["d"], float(plan.p["px"]))
    return True


def _native_frieze(plan, kw, raw, dur):
    ps = _sig(raw)
    if plan.p["d"] != "r" or not all(k in ps for k in ("speed", "x0")) or any(k in kw for k in ("speed", "x0")):
        return False
    kw["speed"] = float(plan.p["px"]) / max(1.0, dur)
    return True


def attach(cx, kind_name, kw, raw=None):
    """cx.cam_state'i hesapla (spec varsa). map: kendi drift'ini sıfırla (çift itme olmasın). OWN_CAMERA türleri: durum uygulanmaz.
    Şerit türlerinde (skyline / procession / frieze) ("pan","r"|"l",px) türün kendi kaydırmasına çevrilir (gerçek paralaks; şerit ucu açılmaz); çevrilemezse genel öteleme + örtme zumu."""
    spec = getattr(cx, "cam_spec", None)
    cx.cam_state = None
    if spec is None or kind_name in OWN_CAMERA:
        return None
    plan = parse(spec)
    native = False
    if plan is not None and plan.kind == "pan" and raw is not None:
        if kind_name == "skyline":
            native = _native_skyline(plan, kw, raw)
        elif kind_name == "procession":
            native = _native_procession(plan, kw, raw)
        elif kind_name == "frieze":
            native = _native_frieze(plan, kw, raw, float(cx.dur))
    cx.cam_state = state(cx, spec, plan=plan, kind=kind_name, native_pan=native)
    if kind_name == "map" and not kw.get("cams") and "drift" not in kw:
        kw["drift"] = (0.0, 0.0, 0.0)
    return cx.cam_state


@contextlib.contextmanager
def map_patch(cx):
    """map türü kendi mapsk.Cam'ini kullanır: oluşturulan her Cam'e ekran-uzayı kayma/zoom eklenir (içerik +dx kayar → dünya merkezi −dx/zoom)."""
    st = getattr(cx, "cam_state", None)
    if st is None or (abs(st.dx) < 1e-3 and abs(st.dy) < 1e-3 and abs(st.s - 1.0) < 1e-6):
        yield
        return
    import mapsk
    orig = mapsk.Cam

    class _Cam(orig):
        def __init__(self, lon, lat, zoom, rot=0.0, cx=W / 2, cy=H / 2):
            z = zoom * st.s
            super().__init__(lon, lat, z, rot, cx, cy)
            self.wx -= st.dx / z
            self.wy -= st.dy / z
    mapsk.Cam = _Cam
    try:
        yield
    finally:
        mapsk.Cam = orig


# ───────────────────────────── odak (rack) bulanıklığı ─────────────────────────────
_MASK = {}


def _focus_mask(fx, fy, r):
    """(270, 480) float32: odak dairesi içinde 1, dışında 0 (yumuşak kenar); 1/4 çözünürlük."""
    sh = (H // 4, W // 4)
    yy, xx = np.mgrid[0:sh[0], 0:sh[1]].astype(np.float32)
    d = np.hypot(xx * 4 - fx, yy * 4 - fy)
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
    m = _focus_mask(fx, fy, r)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    out = cv2.blendLinear(arr, blur, m, 1.0 - m)
    out = np.ascontiguousarray(out)
    im = skia.Image.fromarray(out, colorType=skia.ColorType.kBGRA_8888_ColorType, alphaType=skia.AlphaType.kPremul_AlphaType)
    f.c.save()
    f.c.resetMatrix()
    f.c.drawImage(im, 0, 0, skia.SamplingOptions(), skia.Paint(BlendMode=skia.BlendMode.kSrc))
    f.c.restore()


# ───────────────────────────── statik analiz (qa_flow) ─────────────────────────────
def describe(spec):
    """qa_flow için: {'kind', 'dir', 'scale', 'shift'} (yaklaşık toplam ölçek değişimi oranı ve kayma px) ya da None."""
    pl = parse(spec)
    if pl is None:
        return None
    p, k = pl.p, pl.kind
    d = dict(kind=k, dir=None, scale=0.0, shift=0.0, h=0.0, v=0.0)
    if k in ("push", "pull"):
        d["scale"] = p["amt"]
        d["dir"] = "in" if k == "push" else "out"
    elif k == "pan":
        d.update(shift=p["px"], dir=p["d"], h=(1 if p["d"] == "r" else -1) * p["px"], scale=p.get("push", 0.02))
    elif k == "crane":
        d.update(shift=p["px"], dir=p["d"], v=(1 if p["d"] == "up" else -1) * p["px"], scale=p.get("push", 0.02))
    elif k == "orbit":
        d.update(shift=2 * ORBIT_R * math.sin(math.radians(p["deg"]) / 2), scale=p.get("push", 0.03), dir="orbit")
    elif k == "hand":
        d.update(shift=p["amp"] * 2, scale=p.get("push", HAND_BASE), dir="hand2" if p["strong"] else "hand")
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
    return d


def motion_ok(spec):
    """SPEC §1-1(a): ≥%6 ölçek ya da ≥120 px kayma."""
    d = describe(spec)
    return bool(d) and (d["scale"] >= 0.06 - 1e-9 or d["shift"] >= 120.0 - 1e-9)


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
