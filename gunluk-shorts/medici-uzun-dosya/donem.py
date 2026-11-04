"""donem — DÖNEM (çağ) KATMANI: yıl → o yıl Floransa'da ne vardı / ne çizilir. Medici belgeseli için TEK DOĞRULUK KAYNAĞI.

Yıl kaynağı: compose her karede `cx.year` (HUD yılı, int) yazar; `cilt_medici.ckind` sarmalayıcısı çekim çizilirken `push(cx, tür)` ile bağlamı
kurar, çizim bitince `pop()` eder. Çizim kodu yılı `year()` ile okur (ya da açık `year=` parametresi alır).
ÇEKİM YILI: HUD yılı bir çekimin ortasında dönebilir (YIL_AT sözcük çapası); yapı/arma çekim ortasında değişmesin diye dönem yılı o çekim
boyunca HUD'da EN UZUN kalan yıldır (shot_year). Bölüm kartı: kendi `years` metninin ilk yılı.
Yıl YOKSA (None) — önizleme/reel/kapak gibi `Program(shots=…)` modu (HUD yılı yok), marka türleri (ana başlık, bitiş), cx.year'sız çağrılar — tüm
kural işlevleri None döner ve çağıran ESKİ (bugünkü) çizimi yapar: P2–P7 ve önizleme araçları bozulmaz.

Kurallar (tarihler ve kaynaklar: notlar_donem.md):
  duomo_stage(y)     Santa Maria del Fiore: nef (1296→1380) · tribünler (1380→1410) · tambur (1410→1415) · KUBBE 7 Ağu 1420 → 30 Ağu 1436 ·
                     FENER 1446 → 23 Nis 1461 · tepe TOPU + HAÇ (Verrocchio) 1471
  campanile_stage(y) Giotto çan kulesi: 19 Tem 1334 temel atma · 1337 ilk kat (Giotto) · 1348 kabartma + niş katları (A. Pisano; veba durdurur) · 1359 tam (Talenti)
  pv_stage(y)        Palazzo Vecchio: 1299 başlar · kule ≈1310 · 1314 tamam (uzak siluetlerde)
  sanlorenzo_dome(y) San Lorenzo'nun büyük kubbesi (Cappella dei Principi, Nigetti 1604) — öncesinde siluette kubbe yok
  medici_arms(y)     ≤1464: mavi (Fransa zambaklı) top YOK — 8 kırmızı palle (Cosimo dönemi kaydı; sayı 15. yy'da 5–11 arası değişken) ·
                     ≥1465 (XI. Louis, Montluçon, Mayıs 1465): üstte mavi top + 3 altın zambak, 5 kırmızı (Lorenzo dönemi biçimi)
  flags_allowed(y,b) Medici (palle) sancağı kamusal alay/kalabalıkta yalnız ≥1434 (Medici yönetimi) ve isyan/halk/lonca bağlamı dışında;
                     halk/lonca için nötr: Popolo (beyaz zemin kırmızı haç) · Komün (beyaz zemin kırmızı zambak) · düz renk
  medal_inscription  "PATER PATRIAE" yalnız ≥1464 (Signoria kararı 20 Mart 1465 = Floransa takviminde 1464); öncesi "COSMVS · MEDICES ·"

Denetim kaydı: LOG_ON=True iken çizim kodu `note(öğe, **nitelikler)` ile NE ÇİZDİĞİNİ yazar (çekim, kare zamanı, yıl ile); qa_donem.py bu kaydı
kuralların BAĞIMSIZ bir kopyasıyla denetler. Kayıt ucuzdur (kapalıyken tek bir if).
"""
import re
import sys

LOG_ON = False
LOG = []

# marka işareti türleri: dönem yok (ana başlık freski, bitiş ekranı) → eski çizim
BRAND_KINDS = {"fresco_title", "outro"}


# ───────────────────────────── bağlam ─────────────────────────────
class _Frame:
    __slots__ = ("year", "kind", "cx")

    def __init__(self, year, kind, cx):
        self.year, self.kind, self.cx = year, kind, cx


_STACK = []


def _find_program():
    """Çağrı yığınında compose.Program örneğini bul (yoksa None)."""
    fr = sys._getframe(2)
    for _ in range(16):
        if fr is None:
            break
        s = fr.f_locals.get("self")
        if s is not None and type(s).__name__ == "Program":
            return s
        fr = fr.f_back
    return None


def _program_has_years(prog):
    """`compose.Program(shots=…)` (reel/kapak/qa çekim listesi) modunda YearState boştur ve cx.year anlamsız (1397 varsayılanı) gelir."""
    if prog is None:
        return True
    if not getattr(prog, "hud", True):
        return False
    e = getattr(getattr(prog, "ys", None), "e", None)
    return bool(e) if e is not None else True


_SHOT_YEAR = {}


def shot_year(prog, sh):
    """Çekimin DÖNEM yılı: çekim süresince HUD'da en uzun kalan yıl (eşitlikte sonraki). Yapılar çekim ortasında 'pop' etmesin diye
    yıl çekim boyunca sabittir (HUD yılı çekimin ortasında dönse bile)."""
    key = (id(prog), id(sh), getattr(sh, "t0", 0.0), getattr(sh, "t1", 0.0))
    v = _SHOT_YEAR.get(key)
    if v is None:
        ys = getattr(prog, "ys", None)
        t0, t1 = float(getattr(sh, "t0", 0.0)), float(getattr(sh, "t1", 0.0))
        if ys is None or t1 <= t0:
            return None
        n = max(8, int((t1 - t0) * 4))
        acc = {}
        for i in range(n):
            y = ys.at(t0 + (t1 - t0) * (i + 0.5) / n)[0]
            acc[y] = acc.get(y, 0) + 1
        v = max(acc.items(), key=lambda kv: (kv[1], kv[0]))[0]
        if len(_SHOT_YEAR) > 4000:
            _SHOT_YEAR.clear()
        _SHOT_YEAR[key] = v
    return v


def _years_param(kw):
    """chapter_card: years="1397 – 1429" → 1397 (kartın kendi dönemi)."""
    v = (kw or {}).get("years")
    if not v:
        return None
    m = re.search(r"(1[0-9]{3})", str(v))
    return int(m.group(1)) if m else None


def push(cx, kind, kw=None):
    """ckind sarmalayıcısı çağırır: bu çekimin dönem yılını belirle ve yığına koy. Dönüş: yıl (ya da None)."""
    if cx is not None and _STACK and _STACK[-1].cx is cx:
        y = None if kind in BRAND_KINDS else _STACK[-1].year              # iç içe tür (p1_x → x): dış çekimin kararı geçerli
    else:
        y = getattr(cx, "year", None)
        prog = _find_program() if y is not None else None
        if y is not None and not _program_has_years(prog):
            y = None
        elif y is not None and prog is not None and getattr(cx, "sh", None) is not None:
            y = shot_year(prog, cx.sh) or y
        if kind in BRAND_KINDS:
            y = None
        elif kind == "chapter_card":
            y = _years_param(kw) if y is not None else None
        if y is not None:
            try:
                y = int(y)
            except (TypeError, ValueError):
                y = None
    _STACK.append(_Frame(y, kind, cx))
    return y


_LAST = [None]


def pop():
    """Çekim çizimi bitti. Son çekimin bağlamı, bir sonraki çekim başlayana dek 'son bağlam' olarak kalır: türün DIŞINDA ama aynı kareye
    çizilen katmanlar (p1_ortak.add_ovl `ovl=` kaplamaları, geçiş şeritleri, HUD) da o çekimin yılını görür."""
    if _STACK:
        _LAST[0] = _STACK.pop()


def year():
    """Şu an çizilen çekimin dönem yılı (yoksa None → eski çizim)."""
    fr = current()
    return fr.year if fr is not None else None


def current():
    if _STACK:
        return _STACK[-1]
    return _LAST[0]


def reset():
    """Bağlamı tümden temizle (araçlar: Program dışı çizimden önce)."""
    _STACK.clear()
    _LAST[0] = None


class use_year:
    """Açık bağlam (araçlar/testler): `with donem.use_year(1378): …`."""

    def __init__(self, y, kind="test"):
        self.y, self.kind = y, kind

    def __enter__(self):
        _STACK.append(_Frame(self.y, self.kind, None))
        return self.y

    def __exit__(self, *a):
        pop()


_UNSET = object()


def resolve(y=_UNSET):
    """Açık yıl parametresi (verildiyse) ya da bağlam yılı."""
    return year() if y is _UNSET else y


# ───────────────────────────── kurallar ─────────────────────────────
def _lin(y, y0, y1):
    if y <= y0:
        return 0.0
    if y >= y1:
        return 1.0
    return (y - y0) / float(y1 - y0)


class DuomoStage(tuple):
    """(nave, tribune, drum, dome, lantern, ball) — hepsi 0..1 (ball 0/1). Önbellek anahtarı olarak kullanılabilir (yuvarlanmış)."""
    __slots__ = ()
    _fields = ("nave", "tribune", "drum", "dome", "lantern", "ball")

    def __new__(cls, nave, tribune, drum, dome, lantern, ball):
        q = lambda v: round(float(v), 3)
        return tuple.__new__(cls, (q(nave), q(tribune), q(drum), q(dome), q(lantern), 1.0 if ball else 0.0))

    nave = property(lambda s: s[0])
    tribune = property(lambda s: s[1])
    drum = property(lambda s: s[2])
    dome = property(lambda s: s[3])
    lantern = property(lambda s: s[4])
    ball = property(lambda s: s[5] > 0.5)

    @property
    def full(self):
        return self.dome >= 1.0 and self.lantern >= 1.0 and self.ball

    def tag(self):
        return "d" + "_".join(f"{int(round(v * 1000)):d}" for v in self)


FULL_DUOMO = DuomoStage(1, 1, 1, 1, 1, 1)


def duomo_stage(y=_UNSET):
    """Santa Maria del Fiore'nin y yılındaki durumu; None → eski çizim (tam kubbe + fener + top/haç).
    nave: 1296 temel → 1380 yan nefler örtülü (1378 orta nef) · tribune: 1380 → 1410 · drum (tambur): 1410 → 1415 ·
    dome: 7 Ağu 1420 → 30 Ağu 1436 (oran ≈ (y−1420)/16) · lantern: 1446 → 23 Nis 1461 · ball (top+haç, Verrocchio): ≥1471."""
    y = resolve(y)
    if y is None:
        return None
    return DuomoStage(_lin(y, 1296, 1380), _lin(y, 1380, 1410), _lin(y, 1410, 1415), _lin(y, 1420, 1436), _lin(y, 1446, 1461), y >= 1471)


_CAMP = [(1334, 0.0), (1337, 0.15), (1348, 0.33), (1350, 0.33), (1359, 1.0)]


def campanile_stage(y=_UNSET):
    """Giotto çan kulesi yükseklik oranı (0..1); None → eski çizim (tam).
    1334 temel (19 Temmuz) · 1337 Giotto ölür: ilk kat (≈0,15) · 1348 A. Pisano kabartma + niş katları (≈0,33; veba durdurur) · 1350–1359 Talenti üç pencereli kat → tam."""
    y = resolve(y)
    if y is None:
        return None
    if y < _CAMP[0][0]:
        return 0.0
    for (y0, v0), (y1, v1) in zip(_CAMP, _CAMP[1:]):
        if y0 <= y <= y1:
            return round(v0 + (v1 - v0) * _lin(y, y0, y1), 3)
    return 1.0


def pv_stage(y=_UNSET):
    """Palazzo Vecchio (uzak siluet): <1299 yok · 1299 → 1314 yükselir (kule ≈1310) · ≥1314 tam. None → eski çizim."""
    y = resolve(y)
    if y is None:
        return None
    return round(_lin(y, 1299, 1314), 3)


def sanlorenzo_dome(y=_UNSET):
    """San Lorenzo'nun silueti belirleyen büyük kubbesi (Cappella dei Principi; Nigetti tasarımı 1604). None → eski (çizilir)."""
    y = resolve(y)
    if y is None:
        return None
    return y >= 1604


ARMS_STD = "std"            # eski/varsayılan: üstte mavi zambaklı top + 5 kırmızı (1465 sonrası; Lorenzo'dan itibaren 6 top)
ARMS_RED8 = "red8"          # 1465 öncesi: altın zeminde 8 kırmızı palle (mavi top yok)


def medici_arms(y=_UNSET):
    """Medici arması biçimi: None (yıl yok → eski: ARMS_STD) | dict(variant, blue, n).
    ≤1464: mavi top YOK, 8 kırmızı palle (Cosimo dönemi; 15. yy'da sayı 5–11 arası değişken → 6–8 bandında güvenli seçim) · ≥1465: ARMS_STD."""
    y = resolve(y)
    if y is None:
        return None
    if y <= 1464:
        return dict(variant=ARMS_RED8, blue=False, n=8)
    return dict(variant=ARMS_STD, blue=True, n=6)


def arms_variant(y=_UNSET):
    a = medici_arms(y)
    return a["variant"] if a else ARMS_STD


NEUTRAL_FLAGS = ("cross", "lily", "plain")           # Popolo haçı · Komün zambağı · düz renk
UPRISING = {"ciompi", "isyan", "halk", "lonca", "popolo", "milis"}


def flags_allowed(y=_UNSET, ctx="genel"):
    """İzinli sancak cihazları; None → eski (sınırsız). Medici (palle) sancağı: yalnız y ≥ 1434 ve isyan/halk/lonca bağlamı dışında.
    'stripes' (mavi-sarı Ciompi şeritleri) kaynaksız → dönem modunda kullanılmaz."""
    y = resolve(y)
    if y is None:
        return None
    if (ctx or "genel") in UPRISING or y < 1434:
        return NEUTRAL_FLAGS
    return NEUTRAL_FLAGS + ("medici",)


# sancak renkleri (cilt_anim.FLAGS ile aynı düzen: (cihaz, zemin, işaret))
FLAG_COLORS = {"lily": ("lily", "#F4EEDC", "#B33620"), "cross": ("cross", "#F4EEDC", "#B33620"), "plain": ("plain", "#E0B84E", "#B33620"),
               "plain_g": ("plain", "#2E7A5A", "#E0B84E")}


def flag_sub(flag, y=_UNSET, ctx="genel"):
    """(cihaz, c1, c2) → dönem kuralına uyan sancak. İzinsiz Medici cihazı → düz altın (SA2: 'düz altın'); 'stripes' → Komün zambağı.
    İzinli Medici cihazı yıla göre 'medici_old' (≤1464: 8 kırmızı palle) / 'medici_new' (≥1465: mavi top). y yoksa aynen döner."""
    y = resolve(y)
    if flag is None or y is None:
        return flag
    dev = flag[0]
    ok = flags_allowed(y, ctx)
    if dev in ("medici", "medici_old", "medici_new"):
        if "medici" not in ok:
            return FLAG_COLORS["plain"]
        return ("medici_old" if y <= 1464 else "medici_new",) + tuple(flag[1:])
    if dev not in ok:
        return FLAG_COLORS["lily"] if dev == "stripes" else FLAG_COLORS["plain_g"]
    return flag


def medal_inscription(text, y=_UNSET):
    """Madalya kenar yazısı: 'PATER · PATRIAE' yalnız ≥1464 (Signoria kararı 20 Mart 1465; Floransa takviminde 1464). y yoksa aynen."""
    y = resolve(y)
    if not text or y is None:
        return text
    if "PATER" in text and y < 1464:
        t = re.sub(r"\s*·?\s*PATER\s*·?\s*PATRIAE\s*·?", " ·", text).strip()
        t = re.sub(r"(\s*·\s*)+$", " ·", t)
        return t
    return text


# ───────────────────────────── denetim kaydı ─────────────────────────────
def note(element, **attrs):
    """Çizim kodu NE çizdiğini yazar (LOG_ON iken). Kayıt: çekim türü/etiketi/indisi, kare (global sn), yıl, öğe, nitelikler."""
    if not LOG_ON:
        return
    fr = current()
    cx = fr.cx if fr else None
    sh = getattr(cx, "sh", None)
    LOG.append(dict(el=element, year=fr.year if fr else None, kind=(fr.kind if fr else None), shot=getattr(sh, "i", None),
                    label=getattr(sh, "label", None), g=round(float(getattr(cx, "g", 0.0)), 3) if cx is not None else None, **attrs))


def note_once_per_frame(element, **attrs):
    """Aynı karede aynı öğe+nitelik birden çok yazılmasın (katman/kareaş döngüleri)."""
    if not LOG_ON:
        return
    fr = current()
    cx = fr.cx if fr else None
    key = (element, id(cx), getattr(cx, "g", None), tuple(sorted(attrs.items())))
    if LOG and LOG[-1].get("_k") == key:
        return
    note(element, **attrs)
    if LOG:
        LOG[-1]["_k"] = key


def ascii_tag(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", str(s))
