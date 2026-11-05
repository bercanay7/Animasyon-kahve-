"""Zaman çizelgesi birleştirme + kare çizimi (MEDICI: geçişler, bölüm kartları, HUD = yıl rulosu + perde göstergesi, parça desteği).

    prog = Program()                    # tüm film (çekim listesi çözülmüş zamanlarla)
    prog = Program(part=2)              # Parça 2 (c3–c5): c3 t=0'da başlar (bölüm kartı yok), ilk çekimde 4 sn başlık bindirmesi, bitiş ekranı "SIRADAKİ PARÇA" (P1–P6; P7: "TÜM FİLM")
                                        #   parçanın kendi zaman çizelgesi (out_pN/timeline.json; parca.py) varsa o kullanılır; yoksa genel çizelge (t_off ile kaydırılır)
                                        #   part=None → MEDICI_PART ortam değişkeni ya da `out`→out_pN bağlantısı; part=0 → tam film
    prog = Program(shots=[...], end=T)  # çekim listesi (reel / qa_flow): çapasız, `a` = mutlak saniye; T = son çekimin bitişi
    img = prog.frame(n)                 # n. kare (uint8 RGB, post uygulanmış); parçada n=0 parçanın ilk karesi (global süre = n/FPS + prog.t_off)

Sahne dosyaları: scenes_c0.py … scenes_c16.py → SHOTS (shots.shot(...) listesi), isteğe bağlı YIL_AT = [(çapa/saniye, yıl), …] ve OUTRO_TR (kapanış geçişi).
Bölüm kartı = 3 sn sessizlik aralığı (önceki bölümün sonu → bu bölümün başı): canlı arka plan + ≤2,5 sn yazı. Ana başlık (fresco_title) Parça 1'de c0'dan sonra.

Geçiş modeli (YONETMENLIK_REHBERI §3): tr=(ad, süre[, opts]).
  * place="before" (varsayılan): geçiş gelen çekimin başlangıcında BİTER (giden çekimin son `süre` sn'si); "after": gelen çekimin ilk `süre` sn'sinde sürer
    (giden çekim kamerasıyla bitişinden sonra da sürer) — bölüm kartları bunu kullanır (anlatının son sözcükleri örtülmez).
  * Kamera devri: geçişli girişte gelen çekim `cam_in`, giden `cam_out` (kamera ucu durmaz; cilt_cam uç eğimini korur).
  * lead: yeni geçişlerde (iris/slide/zoomthru/carry/light/candle; opts lead=True/False ile değişir) gelen çekimin yerel saati geçiş BAŞLARKEN başlar
    (Shot.lead = süre): yeni sahne boş duvar değil yaşayan çekim olarak açılır. Anlatı çapaları (cx.at) etkilenmez; mutlak yerel saniyeler (at=0.4) süre kadar erken gelir.
  * ENG-B (Kasım 2026, kurul tur 1; notlar_hareket.md):
    - süre 0,25–2,4 sn (cilt_fx.TR_MIN/TR_MAX); tr="cut" ya da None = sert kesme (kamera kesmede durmaz: cam_in/out; ("cut", dict(carry=False)) durdurur)
    - geçiş ilerlemesi kareye kuantlı: N karelik geçişte k = (j+1)/(N+1) → ilk geçiş karesi giden çekimin kopyası değil, son karesi gelenin kopyası değil
    - cam= verilmemiş çekime tohumlu, ağırlıklı hareket (cilt_cam.auto_spec; ardışık aynı aile yok; Shot.cam_auto=True)
    - seçici deklanşör (Shot.shutter "auto"|True|False|N|dict): hızlı kamera/nesne karelerinde 180° alt-kare örneklemesi (Program.shutter_stats)
    - parça sonu bekleme END_HOLD (anlatı bittikten sonra son kare nefes alır, sonra bitiş geçişi); bitiş ekranı etiketleri #E9C770 ≥34 px
"""
import importlib
import math
import os

import cv2
import numpy as np
import skia

import cilt_fx as FX
import cilt_medici as CM
import shots as SH
import sk
from sk import FPS, H, W, Frame, clamp, ease_out, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER_IDS = [f"c{i}" for i in range(17)]
# bitiş ekranı (ENG-D, kurul tur 2 PK2-Y6 + SA1-Y8; başkan kabulü): 10 sn; YouTube bitiş-ekranı yuvaları çıkışın OUTRO_SLOT_FULL. sn'sinde TAM görünür ve son kareye
# dek kalır (eskisi 7 sn ve yuvalar yalnız son ≈3,5 sn görünüyordu). paket_P1.py YouTube bitiş ekranı başlangıcını OUTRO ve OUTRO_SLOT_FULL'dan hesaplar.
OUTRO = 10.0
OUTRO_SLOT_IN, OUTRO_SLOT_FADE = 0.55, 0.85                     # yuvalar: girer / tam görünene dek (sn, çıkış başından)
OUTRO_SLOT_FULL = OUTRO_SLOT_IN + OUTRO_SLOT_FADE               # = 1,4 sn: yuvaların TAM görünür olduğu an (çıkış başından; ≤ 1,5)
NEXT_PART_LINE = {1: "2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ"}           # sol yuvanın ("SIRADAKİ PARÇA") altındaki küçük satır (parça → metin; yoksa satır yok)
END_HOLD = 1.3                                                  # parça sonu: anlatı bittikten sonra son çekimde kalış (sn; c.t1 zaten ≈0,1 sn pay içerir → ≈1,4 sn nefes)
TAIL = END_HOLD + OUTRO                                         # miks kuyruğu (miks.py --tail): bekleme + bitiş ekranı = 11,3 sn (OUTRO değişince kendiliğinden)
SHUTTER_ANGLE = 180.0                                           # deklanşör açısı (derece): pozlama = açı/360 kare
# seçici deklanşör tetikleri (px/kare, 1920 ölçeği) — kalibrasyon: kurulun P1'i, 603 örnek (notlar_hareket.md §7); maliyet hedefi ≤ +%25
SHUTTER_V_CAM = 4.0                                             # cam= ön ayarının analitik ekran hızı
SHUTTER_V_GLOB = 8.0                                            # ölçülen küresel (kamera benzeri, afin) hız — türün iç kamerası (oda/pano/şehir), belge zumu
SHUTTER_OBJ_V, SHUTTER_OBJ_AREA = 16.0, 3.0                     # nesne: karenin ≥%3'ü ≥16 px/kare (koşan figürler, uçan sayfa, yağan sikke)
SHUTTER_V_HINT = 8.0                                            # anim.hint_speed ipucu
SHUTTER_N_FAST = 30.0                                           # bunun üstünde 5 alt örnek (altında 3; 60 üstü 7) + boşluk doldurma

# bölüm → (roma no, başlık, yıl aralığı metni, başlangıç yılı)
TITLES = {
    "c0": ("", "Hiçbir Şey Buradan Çıkmayacak", "1737 – 1743", 1743),
    "c1": ("I", "Florin Şehri", "1252 – 1397", 1252),
    "c2": ("II", "Defterin Sihri", "1397 – 1429", 1397),
    "c3": ("III", "Kule ve Sürgün", "1433 – 1464", 1433),
    "c4": ("IV", "Kubbe ve Kefaret", "1418 – 1460'lar", 1418),
    "c5": ("V", "Konsil, Kitap, Platon", "1439 – 1492", 1439),
    "c6": ("VI", "Lorenzo", "1449 – 1478", 1449),
    "c7": ("VII", "26 Nisan 1478", "1478", 1478),
    "c8": ("VIII", "Aslanın İni", "1478 – 1481", 1478),
    "c9": ("IX", "Defter Kapanıyor", "1470 – 1494", 1470),
    "c10": ("X", "Rahip ve Kral", "1492 – 1498", 1492),
    "c11": ("XI", "Papa Oğulları", "1512 – 1537", 1512),
    "c12": ("XII", "Dük", "1537 – 1574", 1537),
    "c13": ("XIII", "İki Kraliçe", "1533 – 1642", 1533),
    "c14": ("XIV", "Yıldızlar, Notalar, Taşlar", "1584 – 1737", 1584),
    "c15": ("XV", "Son Medici'ler", "1587 – 1737", 1587),
    "c16": ("XVI", "Hesap", "1737 – bugün", 1737),
}
# perde (bölüm bazlı): I ALTIN (c0–c6), II BEDEL (c7–c11), III MİRAS (c12–c16). Yayın PARÇALARI (7 adet) ayrıdır: script.PARTS'tan gelir.
PERDE_OF = {**{f"c{i}": 1 for i in range(0, 7)}, **{f"c{i}": 2 for i in range(7, 12)}, **{f"c{i}": 3 for i in range(12, 17)}}
PERDE_FIRST = {"c1": 1, "c7": 2, "c12": 3}                     # perde etiketi bu bölüm kartında gösterilir (tam film modunda)
import script as _S                                            # noqa: E402  (PARTS tek yerde tanımlı)
PART_CHAPTERS = {p: list(cs) for p, cs in _S.PARTS.items()}
PART_FIRST = {p: cs[0] for p, cs in PART_CHAPTERS.items()}
N_PARTS = len(PART_CHAPTERS)
HUD_SKIP = ("chapter_card", "fresco_title", "outro", "black", "kapak_kilit", "kapak_kese")   # kapak yankısı (c0 0–3,7 sn) HUD'suz (ENG-A 7a)
CARD_KINDS = ("chapter_card", "fresco_title", "outro", "black")
PART_TITLE_IN, PART_TITLE_OUT = 1.2, 4.8                        # parça başlık bindirmesi: girer / çıkar (parça başından sn)
CARD_TR = ("yikama", 0.9, dict(place="after"))                 # bölüm kartı / ana başlık girişi: malzeme geçişi, sessiz aralıkta


def default_part():
    """part=None iken parça: MEDICI_PART ortam değişkeni (parca.py) ya da `out` bağlantısının out_pN'e çevrilmiş olması; yoksa None (tam film)."""
    v = os.environ.get("MEDICI_PART", "").strip()
    if v.isdigit() and int(v) in PART_CHAPTERS:
        return int(v)
    try:
        import re
        m = re.search(r"out_p([1-9])$", os.path.realpath(os.path.join(HERE, "out")))
        if m:
            return int(m.group(1))
    except OSError:
        pass
    return None


_PART_TL = [False]


def _use_part_timeline(part):
    """Parçanın kendi zaman çizelgesi (parca.py düzeni: out_pN/timeline.json, parçanın ilk bölümü t=0) varsa onu yükle; `out` zaten oraya bağlıysa dokunma.
    SH.TL önbelleği değiştirilir ki cx.at / SH.timeline() çağıran herkes aynı çizelgeyi görsün. part yoksa varsayılan çizelgeye dön."""
    tp = os.path.join(HERE, f"out_p{part}", "timeline.json") if part else None
    if part and os.path.exists(tp):
        if os.path.realpath(tp) != os.path.realpath(os.path.join(HERE, "out", "timeline.json")):
            SH.TL = SH.Timeline(tp)
            _PART_TL[0] = True
    elif _PART_TL[0]:
        SH.TL = None
        _PART_TL[0] = False


_BGRA = skia.ColorType.kBGRA_8888_ColorType
_GRID = {}


def _bgra(f):
    return f.surf.makeImageSnapshot().toarray(colorType=_BGRA, alphaType=skia.AlphaType.kPremul_AlphaType)


def _flow_feats(a, b):
    """İki küçük gri kare (240×135) arası hareket (px/kare, 1920 ölçeği) → (küresel, nesne_alanı_%, nesne_p90):
    küresel = tüm kareye afin (öteleme+ölçek+dönme) oturtulmuş akışın köşe/merkez hızı (TE1 yöntemi: kamera ya da türün iç kamerası);
    nesne = değişimi HAREKETLE açıklanan (geri sarılmış fark < ham farkın yarısı; belirme/solma sayılmaz) ve > SHUTTER_OBJ_V px/kare pikseller (% kare alanı, p90 hız).
    Neredeyse durgun karede (ort. fark < 0,35) (0, 0, 0)."""
    d = cv2.absdiff(a, b)
    if float(d.mean()) < 0.35:
        return 0.0, 0.0, 0.0
    fl = cv2.calcOpticalFlowFarneback(b, a, None, 0.5, 3, 11, 3, 5, 1.1, 0)     # b → a: a(x) ≈ b(x + fl)
    h, w = a.shape
    sc = W / float(w)
    G = _GRID.get((h, w))
    if G is None:
        gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        A = np.stack([(gx - w / 2).ravel(), (gy - h / 2).ravel(), np.ones(h * w, np.float32)], 1)
        G = _GRID[(h, w)] = (gx, gy, A, np.linalg.pinv(A))
    gx, gy, A, Ap = G
    cu, cv_ = Ap @ fl[..., 0].ravel(), Ap @ fl[..., 1].ravel()
    vg = max(math.hypot(cu[0] * x + cu[1] * y + cu[2], cv_[0] * x + cv_[1] * y + cv_[2]) for x in (-w / 2, 0.0, w / 2) for y in (-h / 2, 0.0, h / 2)) * sc
    wb = cv2.remap(a, gx + fl[..., 0], gy + fl[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    r = cv2.absdiff(b, wb).astype(np.float32)
    dd = d.astype(np.float32)
    valid = (dd > 6.0) & (r < 0.5 * dd)
    mag = np.hypot(fl[..., 0], fl[..., 1]) * sc
    fast = valid & (mag > SHUTTER_OBJ_V)
    nf = int(fast.sum())
    return float(vg), 100.0 * nf / float(h * w), (float(np.percentile(mag[fast], 90)) if nf >= 8 else 0.0)


def _gap_fill(avg, first, last, frac):
    """Alt örnekler arası boşluğu doldur (çok hızlı karelerde): İLK ve SON alt örnek arasındaki piksel başına akış (Farneback, 240×135) ölçülür;
    ortalama görüntü bu alan boyunca ±frac/2 (komşu iki örnek arası oran) kaydırılıp 5 dokunuşla ortalanır (yarım çözünürlükte). Zum/paralaks/nesne
    hareketi piksel başına doğru; ekrana sabit yazı/levhanın akışı 0 → keskin kalır (ayrıca yalnız örneklerin ayrıştığı piksellerde uygulanır)."""
    hh, ww = avg.shape[:2]
    gs = [cv2.cvtColor(cv2.resize(x[::4, ::4], (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_BGRA2GRAY) for x in (first, last)]
    fl = cv2.calcOpticalFlowFarneback(gs[1], gs[0], None, 0.5, 4, 13, 3, 5, 1.1, 0)       # son → ilk (küçük px)
    h2, w2 = hh // 2, ww // 2
    flh = cv2.resize(fl, (w2, h2), interpolation=cv2.INTER_LINEAR) * (w2 / 240.0)        # yarım çözünürlük px
    src = cv2.resize(avg, (w2, h2), interpolation=cv2.INTER_AREA)
    gx, gy = np.meshgrid(np.arange(w2, dtype=np.float32), np.arange(h2, dtype=np.float32))
    acc = np.zeros(src.shape, np.uint16)
    taps = [(-0.5 + (j + 0.5) / 5.0) * frac for j in range(5)]
    for t in taps:
        np.add(acc, cv2.remap(src, gx + t * flh[..., 0], gy + t * flh[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE), out=acc, casting="unsafe")
    sm = cv2.resize(cv2.convertScaleAbs(acc, alpha=1.0 / len(taps)), (ww, hh), interpolation=cv2.INTER_LINEAR)
    q = 4
    da = cv2.absdiff(cv2.resize(first, (ww // q, hh // q), interpolation=cv2.INTER_AREA), cv2.resize(last, (ww // q, hh // q), interpolation=cv2.INTER_AREA)).max(axis=2)
    m = (da > 6).astype(np.float32)
    m = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)), (0, 0), 1.5)
    m = np.ascontiguousarray(np.clip(cv2.resize(m, (ww, hh), interpolation=cv2.INTER_LINEAR), 0.0, 1.0))
    return cv2.blendLinear(avg, sm, 1.0 - m, m)


# ───────────── kâğıt dokusu + film greni (ENG-D, kurul tur 2 TE1 §7 / Y8) ─────────────
# Eski: CM.post sıva tanesini (tooth) EKRANA çakılı çarpıyordu (kamera kayınca resim dokunun altından kayıyor → "üstüne filtre" hissi; ölçüm TE1:
# içerikle birlikte kaydırılmış korelasyon 0,07–0,16, sıfır kaymada 0,34–0,43) ve gren 6 karelik döngüydü (n % 6).
# Yeni: doku DÜNYAYA kilitli — her karede çekimin kamera dönüşümü (cilt_cam durumu · oda/pano dünyası · harita kamerası) tersine çevrilerek doku
# içerikle birlikte kayar ve ölçeklenir (deklanşörlü karede alt örneklerin dönüşümleriyle ortalanır: doku da hareket bulanıklığı alır; geçişte iki
# çekimin dokusu karışır). Gren ekranda kalır ama döngüsüz: 4 geniş alan × kare başına tohumlu (96 px'lik) kaydırma.
PAPER_WORLD = True                                              # False: eski ekran-uzayı doku (karşılaştırma / geri dönüş)
PAPER_TOOTH, PAPER_GRAIN = 1.0, 1.35                            # CM.post varsayılanlarıyla aynı güç
GRAIN_FIELDS, GRAIN_PAD = 4, 96
_PAPER = {}


def _tooth1():
    t = _PAPER.get("tooth")
    if t is None:
        t = _PAPER["tooth"] = np.ascontiguousarray(CM.tooth_img(PAPER_TOOTH)[:, :, 0])
    return t


def _grain_fields():
    g = _PAPER.get("grain")
    if g is None:
        rs = np.random.RandomState(4093)
        g = []
        for _ in range(GRAIN_FIELDS):
            a = rs.randn((H + GRAIN_PAD) // 2, (W + GRAIN_PAD) // 2).astype(np.float32)
            a = cv2.resize(a, (W + GRAIN_PAD, H + GRAIN_PAD), interpolation=cv2.INTER_LINEAR)
            pos = np.clip(a * PAPER_GRAIN, 0, 255).astype(np.uint8)
            neg = np.clip(-a * PAPER_GRAIN, 0, 255).astype(np.uint8)
            g.append((cv2.merge([pos, pos, pos]), cv2.merge([neg, neg, neg])))
        _PAPER["grain"] = g
    return g


def _h32(x):
    x = (int(x) * 0x9E3779B1 + 0x7F4A7C15) & 0xFFFFFFFF
    x ^= x >> 15
    x = (x * 0x2C1B3C6D) & 0xFFFFFFFF
    x ^= x >> 12
    return x


def grain_at(n):
    """n. karenin (pos, neg) gren katmanları: alan = h(n) % 4, kaydırma (ox, oy) ∈ [0, 96)² — deterministik, döngüsüz (4·96² birleşim)."""
    h = _h32(n)
    pos, neg = _grain_fields()[h % GRAIN_FIELDS]
    ox, oy = (h >> 4) % GRAIN_PAD, (h >> 12) % GRAIN_PAD
    return pos[oy:oy + H, ox:ox + W], neg[oy:oy + H, ox:ox + W]


def paper_matrix(cx):
    """Çekim bağlamı → ekran → doku koordinatı 2×3 dönüşümü (warpAffine WARP_INVERSE_MAP) ya da None (ekrana çakılı).
    Öncelik: cx.world_xf (oda/pano dünyası: cilt_pano.Ctx · harita: cilt_cam.map_patch) → cx.cam_state (CM.Cam ile çizen türler). Ölçek çekimin
    başvuru zumuna göredir (pano: kamera yolunun ortası; harita: anahtar kare zumlarının geometrik ortası) → doku taneleri ekranda ≈ sabit boyda kalır."""
    if cx is None:
        return None
    xf = getattr(cx, "world_xf", None)
    if xf and xf[0] == "pano":
        _, camx, camy, z, yc, hc = xf
        pc = getattr(cx, "_pano_cam", None)
        try:
            zr = float(pc.at(pc.dur / 2.0)[2]) if pc is not None else z
        except Exception:
            zr = z
        k = zr / max(1e-6, z)
        return np.float32([[k, 0.0, zr * camx - k * W / 2.0], [0.0, k, zr * (hc + camy) - k * yc]])
    if xf and xf[0] == "map":
        _, wx, wy, z, ccx, ccy = xf
        zr = float(getattr(cx, "_map_zref", z) or z)
        k = zr / max(1e-6, z)
        return np.float32([[k, 0.0, zr * wx - k * ccx], [0.0, k, zr * wy - k * ccy]])
    st = getattr(cx, "cam_state", None)
    if st is not None:
        k = 1.0 / max(1e-6, st.s)
        px, py = st.pivot or (W / 2.0, H / 2.0)
        return np.float32([[k, 0.0, px - (px + st.dx) * k], [0.0, k, py - (py + st.dy) * k]])
    return None


def paper(img, n, samples=()):
    """Kâğıt dokusu (dünyaya kilitli; samples = [(çekim bağlamı, ağırlık), …]) + döngüsüz film greni. img: uint8 RGB (CM.post tooth=0, grain=0 sonrası)."""
    t1 = _tooth1()
    acc, tot = None, 0.0
    for cx_, w in (samples if PAPER_WORLD else ()):
        if w <= 1e-4:
            continue
        M = paper_matrix(cx_)
        tw = t1 if M is None else cv2.warpAffine(t1, M, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
        if acc is None and len(samples) == 1:
            acc, tot = tw, -1.0
            break
        acc = tw.astype(np.float32) * w if acc is None else acc + tw.astype(np.float32) * w
        tot += w
    if acc is None:
        tw = t1
    elif tot < 0:
        tw = acc
    else:
        tw = np.clip(acc / max(1e-6, tot) + 0.5, 0, 255).astype(np.uint8)
    a = cv2.multiply(img, cv2.cvtColor(tw, cv2.COLOR_GRAY2RGB), scale=1.0 / 230.0)
    pos, neg = grain_at(n)
    a = cv2.add(a, pos)
    return cv2.subtract(a, neg)


class _StubTL:
    """timeline.json yokken (reel) çapasız çalışma."""
    total = 0.0
    chapters = {}
    sent = {}
    order = []

    def resolve(self, a):
        if isinstance(a, (int, float)):
            return float(a)
        raise KeyError(f"çapa çözülemez (zaman çizelgesi yok): {a!r}")

    def t0(self, sid):
        raise KeyError(sid)

    def word(self, *a, **k):
        raise KeyError(a)


class Program:
    def __init__(self, chapters=None, fast=False, part=None, shots=None, end=None, shutter=True):
        self.fast = fast
        self.hud = True
        self.shutter = bool(shutter)                           # seçici deklanşör açık mı (qa örneklemesi kapatır)
        self.shutter_stats = dict(frames=0, blur=0, extra_renders=0, ms_extra=0.0, ms_flow=0.0, ms_total=0.0, by_n={})
        self._sprev = None                                     # (n, çekim, geçiş mi, küçük gri) — akış ölçümü için önceki kare
        self.t_off = 0.0
        self.shots = []
        self._years = []
        self._chap_mod = {}
        self._chap_marks = []
        self._pf_in = False                                    # parçanın ilk bölümü bu programda mı (başlık bindirmesi + t_off)
        if shots is None:
            part = default_part() if part is None else (part or None)      # None → ortam/out bağlantısı; 0/False → tam film
        else:
            part = part or None
        if part is not None and part not in PART_CHAPTERS:
            raise ValueError(f"part 1..{len(PART_CHAPTERS)} olmalı: {part!r}")
        self.part = part
        if shots is not None:
            try:
                self.tl = SH.timeline()
            except (FileNotFoundError, OSError):
                self.tl = _StubTL()
            self.hud = False                                   # çekim listesi modu: bölüm/HUD mantığı yok (reel, qa_flow)
            self._from_shots(list(shots), end)
            return
        _use_part_timeline(part)
        self.tl = SH.timeline()
        vc = self.tl.chapters
        present = [c for c in CHAPTER_IDS if c in vc]
        if chapters:
            chs = [c for c in CHAPTER_IDS if c in chapters and c in vc]
        elif part:
            chs = [c for c in PART_CHAPTERS[part] if c in vc]
        else:
            chs = list(present)
        pf = PART_FIRST.get(part) if part else None
        self._pf_in = bool(pf and pf in chs)
        for cid in present:
            if cid not in chs:
                continue
            i = CHAPTER_IDS.index(cid)
            c = vc[cid]
            prev_id = next((p for p in reversed(CHAPTER_IDS[:i]) if p in vc), None)
            is_first_of_part = self._pf_in and cid == pf
            if prev_id is not None and not is_first_of_part:
                t0, t1 = vc[prev_id]["t1"], c["t0"]
                if cid == "c1":
                    self._add(SH.shot("fresco_title", a=t0, mode="night", perde=1, tr=CARD_TR, link="material", label="ana başlık"), t0, t1)
                elif t1 - t0 > 0.5:
                    n, title, years, _ = TITLES[cid]
                    kw = {}
                    if cid in PERDE_FIRST:
                        kw["perde_label"] = f"PERDE {FX.ROMAN[PERDE_OF[cid]]} — {FX.PERDE_NAMES[PERDE_OF[cid]]}"
                    self._add(SH.shot("chapter_card", a=t0, n=n, title=title, years=years, perde=PERDE_OF[cid], tr=CARD_TR, link="material", label=f"bölüm kartı {cid}", **kw), t0, t1)
            try:
                mod = importlib.import_module(f"scenes_{cid}")
                lst = mod.SHOTS
                self._chap_mod[cid] = mod
            except ModuleNotFoundError:
                lst = [SH.shot("black", a=c["t0"], text=f"[{cid}]")]
            lst = [s for s in lst]
            for k, s in enumerate(lst):
                ts = self.tl.resolve(s.a)
                te = self.tl.resolve(lst[k + 1].a) if k + 1 < len(lst) else c["t1"]
                if k == 0:
                    ts = c["t0"] if cid != "c0" else 0.0
                self._add(s, ts, te)
        # kapanış (bitiş ekranı): parçada parçanın son bölümünden sonra; tam filmde son bölümden sonra
        if part:
            last_id = chs[-1] if chs else None
        elif chapters is None:
            last_id = present[-1] if present else None
        else:
            last_id = present[-1] if (present and present[-1] in chs) else None
        if last_id:
            last = vc[last_id]
            otr = getattr(self._chap_mod.get(last_id), "OUTRO_TR", None) or CARD_TR
            hold = float(getattr(self._chap_mod.get(last_id), "END_HOLD", END_HOLD))     # sahne modülü END_HOLD ile değiştirebilir
            t_out = last["t1"] + hold
            if self.shots and abs(self.shots[-1].t1 - last["t1"]) < 1e-6:
                self.shots[-1].t1 = t_out                       # son çekim anlatıdan sonra `hold` sn sürer (son kare nefes alır)
            self._last_hold = (last_id, last["t1"], t_out)
            self._add(SH.shot("outro", a=t_out, tr=otr, link="material", mode="night", perde=PERDE_OF.get(last_id, 3), part=part, label="bitiş ekranı"), t_out, t_out + OUTRO)
        self.t_off = vc[pf]["t0"] if self._pf_in else 0.0
        self._finalize()
        # yıl çizelgesi: bölüm başlangıç yılı + sahne dosyasının YIL_AT listesi
        for cid in chs:
            c = vc[cid]
            self._years.append((c["t0"] if cid != "c0" else 0.0, TITLES[cid][3]))
            mod = self._chap_mod.get(cid)
            ya = (getattr(mod, "YIL_AT", None) or getattr(mod, "yil_at", None)) if mod else None
            for a, yr in (ya or []):
                try:
                    self._years.append((self.tl.resolve(a), int(yr)))
                except KeyError:
                    pass
        self.ys = FX.YearState(self._years)
        span = max(1e-6, self.total)
        base = chs if (part or chapters) else present
        self._chap_marks = [(vc[c]["t0"] - self.t_off) / span for c in base[1:]]

    # ---- kurulum
    def _from_shots(self, lst, end):
        """Çekim listesi (reel / qa_flow): a = mutlak saniye (sayı); son çekim end'e kadar (yoksa +5 sn)."""
        for k, s in enumerate(lst):
            ts = float(self.tl.resolve(s.a))
            if k + 1 < len(lst):
                te = float(self.tl.resolve(lst[k + 1].a))
            else:
                te = float(end) if end is not None else ts + 5.0
            self._add(s, ts, te)
        self.t_off = self.shots[0].t0 if self.shots else 0.0
        self._finalize()
        self.ys = FX.YearState([])
        self._chap_marks = []

    def _add(self, s, t0, t1):
        s.t0, s.t1 = float(t0), float(t1)
        assert s.t1 > s.t0 - 1e-6, f"çekim süresi ≤ 0: {s.kind} {s.a} {t0}→{t1}"
        self.shots.append(s)

    def _check_cam(self, s):
        """cam= biçimini ve çapalarını kurulumda doğrula (hata kare çizerken sessizce yutulmasın)."""
        if s.cam is None:
            return
        import cilt_cam
        try:
            for a in cilt_cam.anchors_of(s.cam):
                if not isinstance(a, (int, float)):
                    self.tl.t0(a) if isinstance(a, str) else self.tl.resolve(a)
        except KeyError as e:
            raise KeyError(f"cam çapası çözülemedi (çekim {s.kind} '{s.label}'): {e}")
        except ValueError as e:
            raise ValueError(f"cam= geçersiz (çekim {s.kind} '{s.label}'): {e}")

    def _finalize(self):
        self.shots.sort(key=lambda s: s.t0)
        for i, s in enumerate(self.shots):
            s.i = i
        self._auto_cams()
        for s in self.shots:
            self._check_cam(s)
        self.total = (self.shots[-1].t1 - self.t_off) if self.shots else 0.0
        self._link_flags()

    def _auto_cams(self):
        """cam= verilmemiş çekimlere tohumlu, ağırlıklı hareket (hep itme değil; ardışık aynı aile yok). Yatay/dikey yön bölümün açık cam'lerinden devralınır."""
        import cilt_cam
        own = cilt_cam.OWN_CAMERA
        prev_fam, hdir, vdir = None, "r", "up"
        for s in self.shots:
            if s.kind in CARD_KINDS:
                prev_fam = None
                continue
            if s.kind in own:
                prev_fam = None
                continue
            if s.cam is None and not getattr(s, "cam_auto", False):
                s.cam = cilt_cam.auto_spec(s.kind, max(0.5, s.dur), s.stable_seed, prev=prev_fam, hdir=hdir, vdir=vdir)
                s.cam_auto = True
            try:
                d = cilt_cam.describe(s.cam, s.dur)
            except Exception:
                d = None
            if d:
                prev_fam = d["family"]
                if d["kind"] in ("pan", "truck", "whip") and not s.cam_auto:
                    hdir = d["dir"]
                if d["kind"] in ("crane", "tilt") and not s.cam_auto:
                    vdir = d["dir"]

    def _link_flags(self):
        """Geçişlerde kamera devri (cam_in/cam_out), etkin geçiş (tr_eff) ve gelen çekim saati (lead).
        Sert kesmede ayrıca cut_in/cut_out (ENG-D, kurul tur 2 AN1-Y11 "hareket üstünde kesme"): kesmeyle birleşen uçta kamera eğrisi yumuşamaz
        (cilt_cam: uç eğimi ≥ 1 = ortalama hız; cilt_pano.PanoCam: anahtar karelerin uç eğimi sıfır değil, ilk/son parçanın eğimi)."""
        for s in self.shots:
            s.cam_in = s.cam_out = False
            s.cut_in = s.cut_out = False
            s.lead = 0.0
            s.tr_eff = None
        for i in range(1, len(self.shots)):
            s, p = self.shots[i], self.shots[i - 1]
            t = FX.norm_tr(s.tr)
            if not t:                                           # sert kesme ("cut" / None): kamera kesmede durmaz (kesmede hareket), lead yok
                if FX.cut_opts(s.tr).get("carry", True) and s.kind not in CARD_KINDS and p.kind not in CARD_KINDS:
                    s.cam_in = s.cut_in = True
                    p.cam_out = p.cut_out = True
                elif FX.cut_opts(s.tr).get("carry", True):
                    s.cam_in = True
                    p.cam_out = True
                continue
            name, d, o = t
            if name not in FX.TR and name not in ("fade", "dip", "zoom", "whip", "wipe"):
                raise ValueError(f"bilinmeyen geçiş '{name}' (çekim #{s.i} {s.kind} '{s.label}'); geçerli: {sorted(list(FX.TR) + ['fade', 'dip', 'zoom', 'whip', 'wipe'])}")
            place = o.get("place", "before")
            cap = (p.dur if place != "after" else s.dur) * 0.85
            d = max(FX.TR_MIN, min(d, cap)) if cap > FX.TR_MIN else max(0.05, cap)
            s.tr_eff = (name, d, o)
            if name not in FX.NO_CARRY:
                s.cam_in = True
                p.cam_out = True
            s.lead = FX.lead_for(name, d, o)

    # ---- kare
    def shot_at(self, g):
        lo, hi = 0, len(self.shots) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.shots[mid].t0 <= g + 1e-9:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def _chapter_of(self, g):
        for cid in CHAPTER_IDS:
            c = self.tl.chapters.get(cid)
            if c and c["t0"] - 0.01 <= g <= c["t1"] + 0.01:
                return cid
        lh = getattr(self, "_last_hold", None)                   # parça sonu bekleme: son bölüm sürer (HUD/ilerleme çizgisi sönmez)
        if lh and lh[1] - 0.01 <= g <= lh[2] + 0.01:
            return lh[0]
        return None

    def _perde_at(self, g, s=None):
        if s is not None and "perde" in s.params and s.params["perde"]:
            return s.params["perde"]
        if not self.hud:
            return 2
        cid = self._chapter_of(g)
        if cid is None and g < 0:
            cid = "c0"
        if cid is None:
            # kartlar/geçiş boşlukları: bir sonraki bölümün perdesi
            for c in CHAPTER_IDS:
                cc = self.tl.chapters.get(c)
                if cc and cc["t0"] >= g:
                    return PERDE_OF[c]
            return 3
        return PERDE_OF.get(cid, 2)

    def _render_shot(self, s, g, frame=None):
        f = frame or Frame()
        cx = SH.Ctx(f, g - s.t0 + s.lead, s, self.tl)
        cx.perde = self._perde_at(g, s)
        cx.year = self.ys.at(g)[0] if self.ys.e else None      # çekim listesi (reel/kapak) modunda yıl yok (donem.py sözleşmesi; ENG-A 7)
        SH.KINDS[s.kind](cx, **s.params)
        f._cx = cx                                             # deklanşör: kamera durumu + anim.hint_speed ipucu
        return f

    def _kq(self, g, ga, gb):
        """Kareye kuantlı geçiş ilerlemesi: [ga, gb) penceresine düşen N karenin j.'si için k = (j+1)/(N+1).
        Böylece ilk geçiş karesi giden çekimin (k=0), son geçiş karesi gelen çekimin (k=1) kopyası olmaz: donma/çift kare yok (kurul AN1-E7)."""
        e = 1e-7
        n0 = math.ceil((ga - self.t_off) * FPS - e)
        n1 = math.ceil((gb - self.t_off) * FPS - e)
        n = round((g - self.t_off) * FPS)
        N = max(1, n1 - n0)
        if abs((g - self.t_off) * FPS - n) > 1e-3:              # kare dışı zaman (alt-kare): sürekli k
            return clamp((g - ga) / max(1e-6, gb - ga))
        return clamp((n - n0 + 1) / (N + 1))

    def _trans_at(self, g, i):
        """g anında etkin geçiş → (idx_a, idx_b, ad, süre, opts, k) | None."""
        s = self.shots[i]
        if i > 0 and s.tr_eff:
            name, d, o = s.tr_eff
            if o.get("place") == "after" and g < s.t0 + d:
                return i - 1, i, name, d, o, self._kq(g, s.t0, s.t0 + d)
        if i + 1 < len(self.shots):
            nx = self.shots[i + 1]
            if nx.tr_eff:
                name, d, o = nx.tr_eff
                if o.get("place") != "after" and g >= nx.t0 - d:
                    return i, i + 1, name, d, o, self._kq(g, nx.t0 - d, nx.t0)
        return None

    def frame(self, n, post=True):
        g = n / FPS + self.t_off
        i = self.shot_at(g)
        s = self.shots[i]
        pmix = None
        tr = self._trans_at(g, i)
        if tr is None:
            f = self._render_shot(s, g)
            mode, pd = CM.mode_of(f)
            hud_a = self._hud_vis(s)
            if self.shutter and post:                         # QA çağrıları (post=False) deklanşörsüz: ölçüm/yerleşim kareleri tek örnek
                f = self._shutter(f, s, i, g, n)
            cxs = getattr(f, "_cxs", None)                     # doku: deklanşörlü karede alt örneklerin kamera dönüşümleri (doku da bulanır)
            tex = [(c_, 1.0) for c_ in cxs] if cxs else [(getattr(f, "_cx", None), 1.0)]
        else:
            if self.shutter and post:
                self._sprev = (n, i, True, None)
            ia, ib, name, d, opts, k = tr
            sa, sb = self.shots[ia], self.shots[ib]
            fa = self._render_shot(sa, g)
            fb = self._render_shot(sb, g)
            ma, pa = CM.mode_of(fa)
            mb, pb = CM.mode_of(fb)
            wt = smooth((k - 0.20) / 0.60)
            tex = [(getattr(fa, "_cx", None), 1.0 - wt), (getattr(fb, "_cx", None), wt)]   # geçişte iki çekimin dokusu karışır (sıçrama yok)
            f = self._blend(fa, fb, k, name, g, d, opts)
            if (ma, pa) != (mb, pb):                         # renk derecelendirme geçişte yumuşakça karışır (LUT sıçraması yok)
                pmix = (ma, pa, mb, pb, smooth((k - 0.20) / 0.60))
            mode, pd = (mb, pb) if k > 0.5 else (ma, pa)
            s = sb if k > 0.5 else sa
            hk = smooth((k - 0.15) / 0.70)
            hud_a = (1.0 - hk) * self._hud_vis(sa) + hk * self._hud_vis(sb)   # HUD geçişte yumuşak söner/doğar (yarıda pat diye değil)
        f.cilt_mode, f.cilt_perde = mode, pd
        self._overlay(f, g, s, hud_a)
        img = f.rgb()
        if post:
            if pmix is not None:
                ma, pa, mb, pb, w = pmix
                if w <= 0.001:
                    img = CM.post(img, n, ma, pa, tooth=0, grain=0)
                elif w >= 0.999:
                    img = CM.post(img, n, mb, pb, tooth=0, grain=0)
                else:
                    img = cv2.addWeighted(CM.post(img, n, ma, pa, tooth=0, grain=0), 1.0 - w, CM.post(img, n, mb, pb, tooth=0, grain=0), w, 0)
            else:
                img = CM.post(img, n, mode, pd, tooth=0, grain=0)
            img = paper(img, n, tex)                          # dünyaya kilitli kâğıt dokusu + döngüsüz gren (ENG-D)
        return img

    # ---- seçici deklanşör (hareket bulanıklığı) ─────────────────────────────
    def _shutter_mode(self, s, cx):
        """Shot.shutter → ("off" | "auto" | N (zorunlu alt örnek; 0 = hıza göre ≥3), açı)."""
        m = getattr(s, "shutter", "auto")
        ang = SHUTTER_ANGLE
        if m is None or m is False or m == "off" or (isinstance(m, (int, float)) and not isinstance(m, bool) and m <= 1):
            return "off", ang
        if m is True or m == "on":
            return 0, ang
        if isinstance(m, (int, float)):
            return max(2, min(9, int(m))), ang
        if isinstance(m, dict):
            ang = float(m.get("angle", ang))
            if m.get("at") is not None and cx is not None:
                ta = cx.at(m["at"])
                if ta <= cx.t <= ta + float(m.get("dur", 1.0)):
                    return int(m.get("n", 0)), ang
                return ("auto" if m.get("auto", True) else "off"), ang
            if "n" in m:
                return int(m["n"]), ang
        return "auto", ang

    def _shutter(self, f, s, i, g, n):
        """Seçici deklanşör: karenin ekran hızı = en büyük(kamera analitiği [cilt_cam.screen_speed], önceki kareden ölçülen akış [nesne + türün iç kamerası],
        anim.hint_speed ipucu). Hızlıysa 180° pozlamada (açı/360 kare) N alt-kare yeniden çizilip ortalanır (post ve HUD'dan ÖNCE; çekim sınırı aşılmaz).
        auto: cam= analitiği ≥4 · ölçülen küresel hız ≥8 · karenin ≥%3'ü ≥16 px/kare · ipucu ≥8 → N=3 (≥30 px/kare: 5; ≥60: 7). Örnekler arası boşluk >3 px ise
        ilk/son örnek arası piksel akışıyla doldurulur (_gap_fill). Geçiş karelerine uygulanmaz (kendi bulanıklığı var)."""
        import time as _t
        import cilt_cam
        stt = self.shutter_stats
        stt["frames"] += 1
        cx = getattr(f, "_cx", None)
        mode, ang = self._shutter_mode(s, cx)
        if mode == "off":
            self._sprev = (n, i, False, None)
            return f
        t0 = _t.perf_counter()
        vcam = vx = vy = 0.0
        spec = getattr(cx, "cam_spec", None) if cx is not None else None
        if spec is not None and s.kind not in cilt_cam.OWN_CAMERA:
            try:
                vcam, vx, vy = cilt_cam.screen_speed(cx, spec, kind=s.kind)
            except Exception:
                vcam = 0.0
        vhint = float(getattr(cx, "speed_hint", 0.0) or 0.0) if cx is not None else 0.0
        arr = _bgra(f)
        small = cv2.cvtColor(cv2.resize(arr[::4, ::4], (240, 135), interpolation=cv2.INTER_AREA), cv2.COLOR_BGRA2GRAY)   # 4'lü seyreltme + alan (≈1,6 ms)
        vglob = area = vobj = 0.0
        pv = self._sprev
        if pv is not None and pv[0] == n - 1 and pv[1] == i and not pv[2] and pv[3] is not None:
            vglob, area, vobj = _flow_feats(pv[3], small)
        self._sprev = (n, i, False, small)
        stt["ms_flow"] += (_t.perf_counter() - t0) * 1000
        objhit = area >= SHUTTER_OBJ_AREA
        v = max(vcam, vglob, vhint, vobj if objhit else 0.0)
        if isinstance(mode, int):
            N = mode if mode >= 2 else (7 if v >= 2 * SHUTTER_N_FAST else (5 if v >= SHUTTER_N_FAST else 3))
        else:
            if vcam < SHUTTER_V_CAM and vglob < SHUTTER_V_GLOB and not objhit and vhint < SHUTTER_V_HINT:
                stt["ms_total"] += (_t.perf_counter() - t0) * 1000
                return f
            N = 7 if v >= 2 * SHUTTER_N_FAST else (5 if v >= SHUTTER_N_FAST else 3)
        E = ang / 360.0 / FPS                                       # pozlama (sn)
        offs = [E * ((j + 0.5) / N - 0.5) for j in range(N)]
        lo, hi = s.origin - 0.5 / FPS, s.t1 + 0.5 / FPS             # çekim sınırı (yerel saat aralığı) aşılmaz
        acc = np.zeros(arr.shape, np.uint16)                      # N ≤ 9 → uint16 taşmaz
        first = last = None
        cxs = []                                                  # alt örneklerin çekim bağlamları (kâğıt dokusu da aynı pozlamayla bulanır — ENG-D)
        t1 = _t.perf_counter()
        for o in offs:
            if abs(o) < 1e-9:
                aj = arr
                cxs.append(cx)
            else:
                fj = self._render_shot(s, min(max(g + o, lo), hi))
                aj = _bgra(fj)
                cxs.append(getattr(fj, "_cx", None))
                stt["extra_renders"] += 1
            np.add(acc, aj, out=acc, casting="unsafe")
            first = aj if first is None else first
            last = aj
        stt["ms_extra"] += (_t.perf_counter() - t1) * 1000
        out = cv2.convertScaleAbs(acc, alpha=1.0 / N)
        gap = v * (E * FPS) / N                                     # alt örnekler arası ekran aralığı (px)
        if gap > 3.0 and N >= 3:                                    # çok hızlı hareket: kopyalar arası boşluğu piksel başına akış boyunca doldur
            out = _gap_fill(out, first, last, 1.0 / (N - 1))
            stt["gap_fill"] = stt.get("gap_fill", 0) + 1
        f2 = Frame()
        f2.c.drawImage(skia.Image.fromarray(np.ascontiguousarray(out), colorType=_BGRA, alphaType=skia.AlphaType.kOpaque_AlphaType), 0, 0)
        f2._cxs = cxs
        for a_ in ("cilt_mode", "cilt_perde", "_cx"):
            if hasattr(f, a_):
                setattr(f2, a_, getattr(f, a_))
        stt["blur"] += 1
        stt["by_n"][N] = stt["by_n"].get(N, 0) + 1
        stt["ms_total"] += (_t.perf_counter() - t0) * 1000
        return f2

    def _blend(self, a, b, k, kind_, g, d=0.8, opts=None):
        opts = {x: v for x, v in (opts or {}).items() if x not in ("place", "lead")}
        if kind_ in FX.TR:
            opts.setdefault("year", self.ys.at(g)[0] if self.ys.e else None)     # geçiş kaplamaları (sancak şeridi palle'si) dönem yılıyla çizilir
            return FX.blend(kind_, a, b, k, g, d=d, **opts)
        kk = smooth(k)
        if kind_ == "fade":
            a.blit(b, alpha=kk)
            return a
        if kind_ == "dip":
            if k < 0.5:
                a.rect(0, 0, W, H, color="#0A0806", alpha=smooth(k * 2))
                return a
            b.rect(0, 0, W, H, color="#0A0806", alpha=1 - smooth((k - 0.5) * 2))
            return b
        if kind_ == "zoom":
            out = Frame()
            out.c.save(); out.c.translate(W / 2, H / 2); out.c.scale(1 + 0.25 * kk, 1 + 0.25 * kk); out.c.translate(-W / 2, -H / 2)
            out.blit(a, alpha=1 - kk); out.c.restore()
            out.blit(b, alpha=kk)
            return out
        if kind_ == "whip":
            out = Frame()
            sh = -W * kk
            p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(40 * math.sin(math.pi * k) + 0.1, 0.1))
            out.c.save(); out.c.translate(sh, 0)
            out.c.drawImage(a.surf.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)
            out.c.restore()
            out.c.save(); out.c.translate(W + sh, 0)
            out.c.drawImage(b.surf.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)
            out.c.restore()
            return out
        if kind_ == "wipe":
            out = Frame()
            out.blit(a)
            out.c.save()
            x = W * kk
            out.c.clipRect(skia.Rect.MakeLTRB(0, 0, x, H))
            out.blit(b)
            out.c.restore()
            sh = skia.GradientShader.MakeLinear([(x - 120, 0), (x + 120, 0)], [sk.C("#000000", 0), sk.C("#FFE2A0", 90), sk.C("#000000", 0)], [0, 0.5, 1])
            out.c.drawRect(skia.Rect.MakeLTRB(x - 120, 0, x + 120, H), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kPlus))
            return out
        a.blit(b, alpha=kk)
        return a

    # ---- HUD / kaplama
    @staticmethod
    def _hud_vis(s):
        return 0.0 if (s.kind in HUD_SKIP or not getattr(s, "hud", True)) else 1.0

    def _overlay(self, f, g, s, hud_a=None):
        tp = g - self.t_off
        if self.part and self.part >= 2 and self._pf_in and 0.0 <= tp <= PART_TITLE_OUT + 0.2 and s.kind not in ("chapter_card", "fresco_title", "outro"):
            FX.part_title(f, tp, self.part, PART_TITLE_IN, PART_TITLE_OUT)       # parça başlık bindirmesi (HUD'dan bağımsız)
        ha = self._hud_vis(s) if hud_a is None else float(hud_a)
        if ha <= 0.003 or not self.hud:
            return
        cid = self._chapter_of(g)
        if cid is None:
            return
        c = self.tl.chapters[cid]
        tl_ = g - c["t0"]
        FX.progress_line(f, (g - self.t_off) / max(1e-6, self.total), self._chap_marks, alpha=ha)
        if cid != "c0" and tl_ < 5.5:
            n, title, _, _ = TITLES[cid]
            a = smooth(tl_ / 0.6) * (1 - smooth((tl_ - 4.6) / 0.9))
            FX.chapter_tag(f, f"{n} · {sk.tr_upper(title)}", a * ha)
        FX.hud(f, g, self.ys, PERDE_OF[cid], alpha=ha)


# ───────────────────────────── kapanış çekimi ─────────────────────────────
@CM.ckind("outro")
def k_outro(cx, part=None, **_):
    """Kapanış: palle arması + yaldız 'ZAMAN KURYESİ' + YouTube bitiş-ekranı yuvaları. Parça 1–6: sol 'SIRADAKİ PARÇA'; son parça (7): sol 'TÜM FİLM'; sağ 'ABONE OL · ZAMAN KURYESİ'.
    part=None (tek parça / tam film): mevcut etiketler ('SIRADAKİ TESLİMAT')."""
    import cilt_orn as ORN
    import cilt_props as CP
    f = cx.f
    cam = CM.bgfill(f, cx, seed=2, cam=CM.Cam(cx, push=0.025, drift=(2.4, 1.2)))   # 10 sn'lik çıkış: kayma yarıya indi (toplam ≈ ±12 px)
    cam.begin(f)
    out = 1 - smooth((cx.t - (cx.dur - 0.6)) / 0.6)              # yalnız başlık/arma son 0,6 sn'de hafif söner; yuvalar ve etiketler SON KAREYE dek kalır (PK2-Y6)
    a = cx.amt(0.3, 1.2) * out
    ty = H * 0.27
    # başlığın arkasında koyu hale (SA1-Y8 / PK2: kabartma "ZAMAN KURYESİ" ≈3,0:1 → ≥4,5:1): yatay elips, kenarı yumuşak
    f.c.save()
    f.c.translate(W / 2, ty - 30)
    f.c.scale(1.0, 0.19)
    f.circle(0, 0, 760, shader=f.rad(0, 0, 760, [("#050302", 0.0, int(232 * a)), ("#050302", 0.58, int(196 * a)), ("#050302", 1.0, 0)]))
    f.c.restore()
    sp = CM.gilt("ZAMAN KURYESİ", "title", 92, 16.0)
    gl = ((cx.t - 1.6) * 0.30) % 2.4 if cx.t > 1.6 else None
    CM.draw_spr(f, sp, W / 2, ty, "c", alpha=a, glow=0.32 * a, shadow=0.75, glint=gl if (gl is not None and gl < 1) else None)
    CM.kick(f, "TESLİMAT TAMAM", W / 2, ty + 66, alpha=cx.amt(1.0, 1.0) * out, size=36, track=18, color="#F2D98A")
    CP.draw_arms(f, W / 2, H * 0.455, 200, alpha=cx.amt(1.4, 1.0) * out, shadow=0.5, glint=((cx.t * 0.30 + 0.2) % 2.2) if (cx.t * 0.30 + 0.2) % 2.2 < 1 else None)
    cam.end(f)
    CM.finish(f, cx, motes_n=36)
    # YouTube bitiş-ekranı yuvaları EKRANA SABİT (YouTube öğeleri sabit konumda biner; eskiden kamerayla kayıyordu) · çıkışın OUTRO_SLOT_FULL. sn'sinde tam
    k = cx.amt(OUTRO_SLOT_IN, OUTRO_SLOT_FADE)
    left = ("TÜM FİLM" if part == N_PARTS else "SIRADAKİ PARÇA") if part else "SIRADAKİ TESLİMAT"
    right = "ABONE OL · ZAMAN KURYESİ" if part else "ABONE OL  ·  ZAMAN KURYESİ"
    br = 0.80 + 0.20 * (0.5 + 0.5 * math.sin(cx.t * 1.7))          # yuvaların çerçevesi hafif nefes alır (durağan değil)
    slots = ((330, 610, 520, 292, left), (1070, 610, 520, 292, right))
    for (x, y, w, h, lab) in slots:
        f.rrect(x, y, w, h, 12, color="#000000", alpha=0.30 * k)
        ORN.hairline_frame(f, x, y, w, h, alpha=0.95 * k * br, color="#E9C770", gap=8)
    # etiketler (kurul SA1-Ö5 / TE2-Ö6: #E9C770, ≥34 px, okunur kontrast); sol yuvanın altında sonraki parça satırı (PK2-Y6: "2/7 · …")
    nxt = NEXT_PART_LINE.get(part) if part else None
    for j, (x, y, w, h, lab) in enumerate(slots):
        sz, trk = 38.0, 5.0
        while sk.text_width(lab, "title_m", sz, trk) > 640 and sz > 34.0:   # ≥34 px korunur; yuvalar arası 220 px boşluk etiket taşmasını alır
            sz, trk = sz - 1.0, max(2.0, trk - 0.75)
        wd = sk.text_width(lab, "title_m", sz, trk) + 48
        yb = y + h + 50
        sub = nxt if (j == 0 and nxt) else None
        ssz, strk = 28.0, 3.0
        if sub:
            while sk.text_width(sub, "title_m", ssz, strk) > 660 and ssz > 24.0:
                ssz, strk = ssz - 1.0, max(1.5, strk - 0.5)
            wd = max(wd, sk.text_width(sub, "title_m", ssz, strk) + 48)
        hh = sz + 26 + ((ssz + 14) if sub else 0)                  # alt kenar ≤ 1020 (güvenli alan)
        f.rrect(x + w / 2 - wd / 2, yb - sz - 8, wd, hh, 10, color="#0B0805", alpha=0.62 * k)
        f.text(lab, x + w / 2, yb, face="title_m", size=sz, color="#E9C770", align="c", track=trk, alpha=k, shadow=(2, 3, 4, "#000000"))
        if sub:
            f.text(sub, x + w / 2, yb + ssz + 14, face="title_m", size=ssz, color="#F2E4B8", align="c", track=strk, alpha=k, shadow=(2, 2, 3, "#000000"))
