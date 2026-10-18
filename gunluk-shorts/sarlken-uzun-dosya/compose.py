"""Zaman çizelgesi birleştirme + kare çizimi (geçişler, bölüm kartları, HUD).

    prog = Program()             # çekim listesi (çözülmüş zamanlarla)
    img = prog.frame(n)          # n. kare (uint8 RGB, post uygulanmış)
Sahne dosyaları: scenes_c0.py … scenes_c13.py → SHOTS (shots.shot(...) listesi). Bölüm kartları, ana başlık ve kapanış burada üretilir.
"""
import importlib
import math
import os

import cv2
import numpy as np
import skia

import shots as SH
import sk
from sk import FPS, H, W, Frame, clamp, ease_out, smooth

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTER_IDS = [f"c{i}" for i in range(14)]
OUTRO = 7.0

TITLES = {
    "c1": ("I", "Dört Tahtın Çocuğu", "1500 – 1518"),
    "c2": ("II", "Taç Satılık", "1519 – 1520"),
    "c3": ("III", "Şehirlerin İsyanı", "1520 – 1522"),
    "c4": ("IV", "Worms'ta Bir Keşiş", "1517 – 1522"),
    "c5": ("V", "İmparator Hep Başka Yerde", "1521 – 1555"),
    "c6": ("VI", "Kral, Esir, Düello", "1521 – 1544"),
    "c7": ("VII", "Sultan: Hiç Karşılaşmadılar", "1526 – 1547"),
    "c8": ("VIII", "Akdeniz'de Barbaros", "1534 – 1541"),
    "c9": ("IX", "Yeni Dünya: Altın, Gümüş ve Vicdan", "1519 – 1552"),
    "c10": ("X", "Faturayı Kim Ödedi?", "1519 – 1557"),
    "c11": ("XI", "Adamın Kendisi", "1526 – 1558"),
    "c12": ("XII", "Bırakmak", "1555 – 1558"),
    "c13": ("XIII", "Hesap", "1558"),
}
# cephe göstergesi: hangi bölümde hangi cephe (0 bankacı, 1 keşiş, 2 kral, 3 sultan, 4 miras) ışıyor
FRONT_OF = {"c2": 0, "c4": 1, "c5": 1, "c6": 2, "c7": 3, "c8": 3, "c10": 0, "c13": 4}
FRONT_FIRST = {0: "c2", 1: "c4", 2: "c6", 3: "c7", 4: "c13"}
FRONT_ON_AFTER = {"c2": [0], "c4": [0, 1], "c5": [0, 1], "c6": [0, 1, 2], "c7": [0, 1, 2, 3], "c8": [0, 1, 2, 3], "c9": [0, 1, 2, 3], "c10": [0, 1, 2, 3], "c11": [0, 1, 2, 3], "c12": [0, 1, 2, 3], "c13": [0, 1, 2, 3, 4]}


class Program:
    def __init__(self, chapters=None, fast=False):
        self.tl = SH.timeline()
        self.shots = []
        self.fast = fast
        self.total = self.tl.total + OUTRO
        chs = chapters or CHAPTER_IDS
        vc = self.tl.chapters
        for i, cid in enumerate(CHAPTER_IDS):
            if cid not in chs:
                continue
            c = vc[cid]
            if i > 0:
                prev = vc[CHAPTER_IDS[i - 1]]
                t0, t1 = prev["t1"], c["t0"]
                if cid == "c1":
                    self._add(SH.shot("title", a=t0, text="ŞARLKEN", sub="DÜNYAYI TESLİM EDEN İMPARATOR", kick="ZAMAN KURYESİ  ·  TESLİMAT", at=-4.0, sub_at=0.35, kick_at=0.15), t0, t1)
                else:
                    n, title, years = TITLES[cid]
                    fr = FRONT_ON_AFTER.get(cid)
                    self._add(SH.shot("chapter_card", a=t0, n=n, title=title, years=years, fronts=fr, fnow=FRONT_OF.get(cid)), t0, t1)
            try:
                mod = importlib.import_module(f"scenes_{cid}")
                lst = mod.SHOTS
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
        last = vc["c13"]
        if "c13" in chs:
            self._add(SH.shot("outro", a=last["t1"]), last["t1"], last["t1"] + OUTRO + 0.0)
        self.shots.sort(key=lambda s: s.t0)
        for i, s in enumerate(self.shots):
            s.i = i
        self.total = self.shots[-1].t1
        self._hud_cache = {}

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

    def _render_shot(self, s, g, frame=None):
        f = frame or Frame()
        cx = SH.Ctx(f, g - s.t0, s, self.tl)
        SH.KINDS[s.kind](cx, **s.params)
        return f

    def frame(self, n, post=True):
        g = n / FPS
        i = self.shot_at(g)
        s = self.shots[i]
        f = self._render_shot(s, g)
        # geçiş: sonraki çekim girişi
        if i + 1 < len(self.shots):
            nx = self.shots[i + 1]
            tr = nx.tr
            if tr:
                kind_, d = tr[0], tr[1]
                if g >= nx.t0 - d:
                    k = clamp((g - (nx.t0 - d)) / d)
                    f2 = self._render_shot(nx, g)
                    f = self._blend(f, f2, k, kind_, g)
        if s.tr and (g - s.t0) < 0:
            pass
        self._overlay(f, g, s)
        img = f.rgb()
        if post:
            card = s.kind in ("chapter_card",)
            img = sk.post(img, n, grain=1.0, bloom=0.2)
        return img

    def _blend(self, a, b, k, kind_, g):
        kk = smooth(k)
        if kind_ == "fade":
            a.blit(b, alpha=kk)
            return a
        if kind_ == "dip":
            # siyaha dalıp çık
            if k < 0.5:
                a.rect(0, 0, W, H, color="#000000", alpha=smooth(k * 2))
                return a
            b.rect(0, 0, W, H, color="#000000", alpha=1 - smooth((k - 0.5) * 2))
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
    def _chapter_of(self, g):
        for cid in CHAPTER_IDS:
            c = self.tl.chapters.get(cid)
            if c and c["t0"] - 0.01 <= g <= c["t1"] + 0.01:
                return cid
        return None

    def _overlay(self, f, g, s):
        if s.kind in ("chapter_card", "title", "outro", "black"):
            return
        cid = self._chapter_of(g)
        if cid is None:
            return
        c = self.tl.chapters[cid]
        tl_ = g - c["t0"]
        # ilerleme çizgisi (çok ince)
        prog = g / self.total
        f.rect(0, H - 5, W, 5, color="#000000", alpha=0.45)
        f.rect(0, H - 4, W * prog, 3, color="#C9962B", alpha=0.85)
        for cc in CHAPTER_IDS[1:]:
            x = self.tl.chapters[cc]["t0"] / self.total * W
            f.rect(x - 1, H - 6, 2, 6, color="#F0D27A", alpha=0.7)
        # bölüm adı (bölüm başında 5 sn)
        if cid != "c0" and tl_ < 5.5:
            n, title, _ = TITLES[cid]
            a = smooth(tl_ / 0.6) * (1 - smooth((tl_ - 4.6) / 0.9))
            f.text(f"{n} · {sk.tr_upper(title)}", 70, 74, face="title_m", size=24, color="#E3CF98", align="l", track=6, alpha=0.85 * a, shadow=(2, 2, 3, "#000000"))
        # cephe göstergesi
        fr = FRONT_ON_AFTER.get(cid)
        if fr and cid not in ("c13",) or (cid == "c13" and tl_ > 0):
            now = FRONT_OF.get(cid)
            fro = FRONT_ON_AFTER.get(cid, [])
            x0 = W - 70 - 5 * 66
            a = 0.9
            for i, (ic, nm) in enumerate(SH.FRONT_ICONS):
                x = x0 + i * 66 + 30
                on = i in fro
                if i == now:
                    f.circle(x, 78, 30, shader=f.rad(x, 78, 30, [("#F0D27A", 0.0, int(110 + 40 * math.sin(g * 4))), ("#F0D27A", 1.0, 0)]))
                import icons
                icons.draw_icon(f, ic, x, 78, size=40 if i != now else 46, metal="gold" if on else "bronze", alpha=a if on else 0.3, shadow=False)


# ───────────────────────────── kapanış çekimi ─────────────────────────────
@SH.kind("outro")
def k_outro(cx):
    """Kapanış: başlık + beş cephe (hepsi yanık) + YouTube bitiş-ekranı yuvaları (sol: video karesi, sağ: abone ol)."""
    f = cx.f
    f.bg("night"); f.rays(alpha=0.35)
    sk.dust(f, cx.t, n=70)
    out = 1 - smooth((cx.t - (cx.dur - 1.2)) / 1.2)
    a = cx.amt(0.3, 1.2) * out
    f.gold("ZAMAN KURYESİ", W / 2, H * 0.30, face="title", size=96, track=14, alpha=a)
    SH.kicker(f, "TESLİMAT TAMAM", W / 2, H * 0.30 + 66, alpha=cx.amt(1.0, 1.0) * out, size=30, track=18)
    SH.cephe_row(f, [0, 1, 2, 3, 4], None, y=H * 0.47, alpha=cx.amt(1.6, 0.9) * out, t=cx.t, size=58, gap=190)
    # bitiş ekranı yuvaları (Studio'da öğeler bu karelere hizalanır)
    k = cx.amt(2.6, 0.9) * out
    for (x, y, w, h, lab) in ((330, 640, 520, 292, "SIRADAKİ TESLİMAT"), (1070, 640, 520, 292, "ABONE OL  ·  ZAMAN KURYESİ")):
        f.rrect(x, y, w, h, 14, color="#000000", alpha=0.28 * k)
        f.rrect(x, y, w, h, 14, style="stroke", sw=2.2, color="#C9962B", alpha=0.85 * k)
        f.rrect(x + 8, y + 8, w - 16, h - 16, 9, style="stroke", sw=1.0, color="#C9962B", alpha=0.35 * k)
        SH.kicker(f, lab, x + w / 2, y + h + 44, alpha=0.9 * k, size=24, track=8, face="cap_b")
    f.vig(0.65)
