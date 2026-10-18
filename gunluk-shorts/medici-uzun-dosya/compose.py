"""Zaman çizelgesi birleştirme + kare çizimi (MEDICI: geçişler, bölüm kartları, HUD = yıl rulosu + perde göstergesi).

    prog = Program()             # çekim listesi (çözülmüş zamanlarla)
    img = prog.frame(n)          # n. kare (uint8 RGB, post uygulanmış)
Sahne dosyaları: scenes_c0.py … scenes_c16.py → SHOTS (shots.shot(...) listesi) ve isteğe bağlı YIL_AT = [(çapa/saniye, yıl), …].
Bölüm kartları, ana başlık (fresco_title) ve kapanış burada üretilir. Bölüm kartı = 3 sn sessizlik aralığı (önceki bölümün sonu → bu bölümün başı).
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
# perde: I PARA (c0–c3), II GÜZELLİK (c4–c10), III MİRAS (c11–c16)
PERDE_OF = {**{f"c{i}": 1 for i in range(0, 4)}, **{f"c{i}": 2 for i in range(4, 11)}, **{f"c{i}": 3 for i in range(11, 17)}}
PERDE_FIRST = {"c1": 1, "c4": 2, "c11": 3}                     # perde etiketi bu bölüm kartında gösterilir
HUD_SKIP = ("chapter_card", "fresco_title", "outro", "black")


class Program:
    def __init__(self, chapters=None, fast=False):
        self.tl = SH.timeline()
        self.shots = []
        self.fast = fast
        self.total = self.tl.total + OUTRO
        vc = self.tl.chapters
        chs = chapters or [c for c in CHAPTER_IDS if c in vc]
        present = [c for c in CHAPTER_IDS if c in vc]
        self._years = []
        self._chap_mod = {}
        for cid in present:
            if cid not in chs:
                continue
            i = CHAPTER_IDS.index(cid)
            c = vc[cid]
            prev_id = next((p for p in reversed(CHAPTER_IDS[:i]) if p in vc), None)
            if prev_id is not None:
                t0, t1 = vc[prev_id]["t1"], c["t0"]
                if cid == "c1":
                    self._add(SH.shot("fresco_title", a=t0, mode="night", perde=1), t0, t1)
                elif t1 - t0 > 0.5:
                    n, title, years, _ = TITLES[cid]
                    kw = {}
                    if cid in PERDE_FIRST:
                        kw["perde_label"] = f"PERDE {FX.ROMAN[PERDE_OF[cid]]} — {FX.PERDE_NAMES[PERDE_OF[cid]]}"
                    self._add(SH.shot("chapter_card", a=t0, n=n, title=title, years=years, perde=PERDE_OF[cid], **kw), t0, t1)
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
        # kapanış
        if present and (chapters is None or present[-1] in chs):
            last = vc[present[-1]]
            self._add(SH.shot("outro", a=last["t1"], tr=("fade", 0.7), mode="night", perde=3), last["t1"], last["t1"] + OUTRO)
        self.shots.sort(key=lambda s: s.t0)
        for i, s in enumerate(self.shots):
            s.i = i
        self.total = self.shots[-1].t1
        # yıl çizelgesi: bölüm başlangıç yılı + sahne dosyasının YIL_AT listesi
        for cid in present:
            if cid not in chs:
                continue
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
        self._chap_marks = [vc[c]["t0"] / self.total for c in present[1:]]

    def _add(self, s, t0, t1):
        s.t0, s.t1 = float(t0), float(t1)
        assert s.t1 > s.t0 - 1e-6, f"çekim süresi ≤ 0: {s.kind} {s.a} {t0}→{t1}"
        self.shots.append(s)

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
        cx = SH.Ctx(f, g - s.t0, s, self.tl)
        cx.perde = self._perde_at(g, s)
        cx.year = self.ys.at(g)[0]
        SH.KINDS[s.kind](cx, **s.params)
        return f

    def frame(self, n, post=True):
        g = n / FPS
        i = self.shot_at(g)
        s = self.shots[i]
        f = self._render_shot(s, g)
        mode, pd = CM.mode_of(f)
        # geçiş: sonraki çekim girişi
        if i + 1 < len(self.shots):
            nx = self.shots[i + 1]
            tr = nx.tr
            if tr:
                kind_, d = tr[0], tr[1]
                if g >= nx.t0 - d:
                    k = clamp((g - (nx.t0 - d)) / d)
                    f2 = self._render_shot(nx, g)
                    m2, p2 = CM.mode_of(f2)
                    f = self._blend(f, f2, k, kind_, g)
                    if k > 0.5:
                        mode, pd = m2, p2
                    s = nx if k > 0.5 else s
        f.cilt_mode, f.cilt_perde = mode, pd
        self._overlay(f, g, s)
        img = f.rgb()
        if post:
            img = CM.post(img, n, mode, pd)
        return img

    def _blend(self, a, b, k, kind_, g):
        if kind_ in FX.TR:
            return FX.blend(kind_, a, b, k, g)
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
        if s.kind in HUD_SKIP:
            return
        cid = self._chapter_of(g)
        if cid is None:
            return
        c = self.tl.chapters[cid]
        tl_ = g - c["t0"]
        FX.progress_line(f, g / self.total, self._chap_marks)
        if cid != "c0" and tl_ < 5.5:
            n, title, _, _ = TITLES[cid]
            a = smooth(tl_ / 0.6) * (1 - smooth((tl_ - 4.6) / 0.9))
            FX.chapter_tag(f, f"{n} · {sk.tr_upper(title)}", a)
        FX.hud(f, g, self.ys, PERDE_OF[cid])


# ───────────────────────────── kapanış çekimi ─────────────────────────────
@CM.ckind("outro")
def k_outro(cx, **_):
    """Kapanış: palle arması + yaldız 'ZAMAN KURYESİ' + YouTube bitiş-ekranı yuvaları (sol: video karesi, sağ: abone ol)."""
    import cilt_orn as ORN
    import cilt_props as CP
    f = cx.f
    cam = CM.bgfill(f, cx, seed=2, cam=CM.Cam(cx, push=0.03, drift=(4.0, 2.0)))
    cam.begin(f)
    out = 1 - smooth((cx.t - (cx.dur - 1.2)) / 1.2)
    a = cx.amt(0.3, 1.2) * out
    sp = CM.gilt("ZAMAN KURYESİ", "title", 92, 16.0)
    CM.draw_spr(f, sp, W / 2, H * 0.27, "c", alpha=a, glow=0.25 * a, shadow=0.6)
    CM.kick(f, "TESLİMAT TAMAM", W / 2, H * 0.27 + 62, alpha=cx.amt(1.0, 1.0) * out, size=30, track=18, color="#E6C472")
    CP.draw_arms(f, W / 2, H * 0.455, 200, alpha=cx.amt(1.4, 1.0) * out, shadow=0.5)
    k = cx.amt(2.6, 0.9) * out
    for (x, y, w, h, lab) in ((330, 640, 520, 292, "SIRADAKİ TESLİMAT"), (1070, 640, 520, 292, "ABONE OL  ·  ZAMAN KURYESİ")):
        f.rrect(x, y, w, h, 12, color="#000000", alpha=0.30 * k)
        ORN.hairline_frame(f, x, y, w, h, alpha=0.95 * k, color="#D8B25A", gap=8)
        CM.ink(f, lab, x + w / 2, y + h + 46, face="cap_b", size=28, color="#E6D3A0", align="c", track=7, alpha=0.95 * k)
    cam.end(f)
    CM.finish(f, cx, motes_n=36)
