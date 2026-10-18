"""Zaman çizelgesi birleştirme + kare çizimi (MEDICI: geçişler, bölüm kartları, HUD = yıl rulosu + perde göstergesi, parça desteği).

    prog = Program()                    # tüm film (çekim listesi çözülmüş zamanlarla)
    prog = Program(part=2)              # Parça 2 (c7–c11): c7 t=0'da başlar (bölüm kartı yok), ilk çekimde 4 sn başlık bindirmesi, bitiş ekranı "SIRADAKİ PARÇA"
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
OUTRO = 7.0

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
# perde = parça: I ALTIN (c0–c6), II BEDEL (c7–c11), III MİRAS (c12–c16)
PERDE_OF = {**{f"c{i}": 1 for i in range(0, 7)}, **{f"c{i}": 2 for i in range(7, 12)}, **{f"c{i}": 3 for i in range(12, 17)}}
PERDE_FIRST = {"c1": 1, "c7": 2, "c12": 3}                     # perde etiketi bu bölüm kartında gösterilir (tam film modunda)
PART_CHAPTERS = {1: [f"c{i}" for i in range(0, 7)], 2: [f"c{i}" for i in range(7, 12)], 3: [f"c{i}" for i in range(12, 17)]}
PART_FIRST = {1: "c0", 2: "c7", 3: "c12"}
HUD_SKIP = ("chapter_card", "fresco_title", "outro", "black")
CARD_KINDS = ("chapter_card", "fresco_title", "outro", "black")
PART_TITLE_IN, PART_TITLE_OUT = 1.2, 4.8                        # parça başlık bindirmesi: girer / çıkar (parça başından sn)
CARD_TR = ("yikama", 0.9, dict(place="after"))                 # bölüm kartı / ana başlık girişi: malzeme geçişi, sessiz aralıkta


def default_part():
    """part=None iken parça: MEDICI_PART ortam değişkeni (parca.py) ya da `out` bağlantısının out_pN'e çevrilmiş olması; yoksa None (tam film)."""
    v = os.environ.get("MEDICI_PART", "").strip()
    if v in ("1", "2", "3"):
        return int(v)
    try:
        import re
        m = re.search(r"out_p([123])$", os.path.realpath(os.path.join(HERE, "out")))
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
    def __init__(self, chapters=None, fast=False, part=None, shots=None, end=None):
        self.fast = fast
        self.hud = True
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
            raise ValueError(f"part 1, 2 ya da 3 olmalı: {part!r}")
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
            self._add(SH.shot("outro", a=last["t1"], tr=otr, link="material", mode="night", perde=part or 3, part=part, label="bitiş ekranı"), last["t1"], last["t1"] + OUTRO)
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
            self._check_cam(s)
        self.total = (self.shots[-1].t1 - self.t_off) if self.shots else 0.0
        self._link_flags()

    def _link_flags(self):
        """Geçişlerde kamera devri (cam_in/cam_out), etkin geçiş (tr_eff) ve gelen çekim saati (lead)."""
        for s in self.shots:
            s.cam_in = s.cam_out = False
            s.lead = 0.0
            s.tr_eff = None
        for i in range(1, len(self.shots)):
            s, p = self.shots[i], self.shots[i - 1]
            t = FX.norm_tr(s.tr)
            if not t:
                continue
            name, d, o = t
            if name not in FX.TR and name not in ("fade", "dip", "zoom", "whip", "wipe"):
                raise ValueError(f"bilinmeyen geçiş '{name}' (çekim #{s.i} {s.kind} '{s.label}'); geçerli: {sorted(list(FX.TR) + ['fade', 'dip', 'zoom', 'whip', 'wipe'])}")
            place = o.get("place", "before")
            cap = (p.dur if place != "after" else s.dur) * 0.85
            d = max(0.2, min(d, cap)) if cap > 0.2 else max(0.05, cap)
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
        return None

    def _perde_at(self, g, s=None):
        if s is not None and "perde" in s.params and s.params["perde"]:
            return s.params["perde"]
        if not self.hud:
            return 2
        if self.part:
            return self.part
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
        cx.year = self.ys.at(g)[0]
        SH.KINDS[s.kind](cx, **s.params)
        return f

    def _trans_at(self, g, i):
        """g anında etkin geçiş → (idx_a, idx_b, ad, süre, opts, k) | None."""
        s = self.shots[i]
        if i > 0 and s.tr_eff:
            name, d, o = s.tr_eff
            if o.get("place") == "after" and g < s.t0 + d:
                return i - 1, i, name, d, o, clamp((g - s.t0) / d)
        if i + 1 < len(self.shots):
            nx = self.shots[i + 1]
            if nx.tr_eff:
                name, d, o = nx.tr_eff
                if o.get("place") != "after" and g >= nx.t0 - d:
                    return i, i + 1, name, d, o, clamp((g - (nx.t0 - d)) / d)
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
        else:
            ia, ib, name, d, opts, k = tr
            sa, sb = self.shots[ia], self.shots[ib]
            fa = self._render_shot(sa, g)
            fb = self._render_shot(sb, g)
            ma, pa = CM.mode_of(fa)
            mb, pb = CM.mode_of(fb)
            f = self._blend(fa, fb, k, name, g, d, opts)
            if (ma, pa) != (mb, pb):                         # renk derecelendirme geçişte yumuşakça karışır (LUT sıçraması yok)
                pmix = (ma, pa, mb, pb, smooth((k - 0.20) / 0.60))
            mode, pd = (mb, pb) if k > 0.5 else (ma, pa)
            s = sb if k > 0.5 else sa
        f.cilt_mode, f.cilt_perde = mode, pd
        self._overlay(f, g, s)
        img = f.rgb()
        if post:
            if pmix is not None:
                ma, pa, mb, pb, w = pmix
                if w <= 0.001:
                    img = CM.post(img, n, ma, pa)
                elif w >= 0.999:
                    img = CM.post(img, n, mb, pb)
                else:
                    img = cv2.addWeighted(CM.post(img, n, ma, pa), 1.0 - w, CM.post(img, n, mb, pb), w, 0)
            else:
                img = CM.post(img, n, mode, pd)
        return img

    def _blend(self, a, b, k, kind_, g, d=0.8, opts=None):
        opts = {x: v for x, v in (opts or {}).items() if x not in ("place", "lead")}
        if kind_ in FX.TR:
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
    def _overlay(self, f, g, s):
        tp = g - self.t_off
        if self.part in (2, 3) and self._pf_in and 0.0 <= tp <= PART_TITLE_OUT + 0.2 and s.kind not in ("chapter_card", "fresco_title", "outro"):
            FX.part_title(f, tp, self.part, PART_TITLE_IN, PART_TITLE_OUT)       # parça başlık bindirmesi (HUD'dan bağımsız)
        if s.kind in HUD_SKIP or not self.hud:
            return
        cid = self._chapter_of(g)
        if cid is None:
            return
        c = self.tl.chapters[cid]
        tl_ = g - c["t0"]
        FX.progress_line(f, (g - self.t_off) / max(1e-6, self.total), self._chap_marks)
        if cid != "c0" and tl_ < 5.5:
            n, title, _, _ = TITLES[cid]
            a = smooth(tl_ / 0.6) * (1 - smooth((tl_ - 4.6) / 0.9))
            FX.chapter_tag(f, f"{n} · {sk.tr_upper(title)}", a)
        FX.hud(f, g, self.ys, PERDE_OF[cid])


# ───────────────────────────── kapanış çekimi ─────────────────────────────
@CM.ckind("outro")
def k_outro(cx, part=None, **_):
    """Kapanış: palle arması + yaldız 'ZAMAN KURYESİ' + YouTube bitiş-ekranı yuvaları. Parça 1/2: sol 'SIRADAKİ PARÇA'; Parça 3: sol 'TÜM FİLM'; sağ 'ABONE OL · ZAMAN KURYESİ'.
    part=None (tek parça / tam film): mevcut etiketler ('SIRADAKİ TESLİMAT')."""
    import cilt_orn as ORN
    import cilt_props as CP
    f = cx.f
    cam = CM.bgfill(f, cx, seed=2, cam=CM.Cam(cx, push=0.03, drift=(4.0, 2.0)))
    cam.begin(f)
    out = 1 - smooth((cx.t - (cx.dur - 1.2)) / 1.2)
    a = cx.amt(0.3, 1.2) * out
    sp = CM.gilt("ZAMAN KURYESİ", "title", 92, 16.0)
    gl = ((cx.t - 1.6) * 0.30) % 2.4 if cx.t > 1.6 else None
    CM.draw_spr(f, sp, W / 2, H * 0.27, "c", alpha=a, glow=0.25 * a, shadow=0.6, glint=gl if (gl is not None and gl < 1) else None)
    CM.kick(f, "TESLİMAT TAMAM", W / 2, H * 0.27 + 62, alpha=cx.amt(1.0, 1.0) * out, size=30, track=18, color="#E6C472")
    CP.draw_arms(f, W / 2, H * 0.455, 200, alpha=cx.amt(1.4, 1.0) * out, shadow=0.5, glint=((cx.t * 0.30 + 0.2) % 2.2) if (cx.t * 0.30 + 0.2) % 2.2 < 1 else None)
    k = cx.amt(2.6, 0.9) * out
    left = {1: "SIRADAKİ PARÇA", 2: "SIRADAKİ PARÇA", 3: "TÜM FİLM"}.get(part, "SIRADAKİ TESLİMAT")
    right = "ABONE OL · ZAMAN KURYESİ" if part else "ABONE OL  ·  ZAMAN KURYESİ"
    br = 0.80 + 0.20 * (0.5 + 0.5 * math.sin(cx.t * 1.7))          # yuvaların çerçevesi hafif nefes alır (durağan değil)
    for (x, y, w, h, lab) in ((330, 640, 520, 292, left), (1070, 640, 520, 292, right)):
        f.rrect(x, y, w, h, 12, color="#000000", alpha=0.30 * k)
        ORN.hairline_frame(f, x, y, w, h, alpha=0.95 * k * br, color="#D8B25A", gap=8)
        CM.ink(f, lab, x + w / 2, y + h + 46, face="cap_b", size=28, color="#E6D3A0", align="c", track=7, alpha=0.95 * k)
    cam.end(f)
    CM.finish(f, cx, motes_n=36)
