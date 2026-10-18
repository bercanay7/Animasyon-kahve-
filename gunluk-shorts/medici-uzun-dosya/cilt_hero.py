"""cilt_hero — preview_cilt.py için kahraman çekim tanımları (gün: sayfa 1, gece/HUD/kart/geçiş: sayfa 2)."""
import time

import cilt_medici as CM
import numpy as np
from sk import FPS, H, W

HEROES = [
    dict(ad="fresco_title", kind="fresco_title", params=dict(), t=[5.4], dur=9.0, sayfa=2, mode="night", perde=2),
    dict(ad="title_day", kind="title", params=dict(text="MEDİCİ", sub="BANKACILAR AİLESİ", kick="FLORANSA", at=0.3), t=[3.2], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="palle_day", kind="palle", params=dict(kick="ALTI TOP", caption="Medici arması", at=0.2), t=[3.0], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="coin_day", kind="coin", params=dict(kick="1252", sub="Florin", caption="Bir yüzünde zambak, ötekinde Vaftizci Yahya", at=0.2, n=4), t=[3.0], dur=8.0, sayfa=1, mode="day", perde=1),
    dict(ad="chapter_card", kind="chapter_card", params=dict(n="IV", title="Kubbe ve Kefaret", years="1418 – 1460'lar", perde_label="PERDE II — GÜZELLİK"), t=[1.6], dur=3.0, sayfa=2, mode="night", perde=2),
    dict(ad="quote_day", kind="quote", params=dict(text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", src="Aile Antlaşması, 1737", at=0.2), t=[3.5], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="counter_day", kind="counter", params=dict(value=1500, unit="florin", label="Piccarda'nın çeyizi", coin=True, at=0.2), t=[3.2], dur=8.0, sayfa=1, mode="day", perde=1),
]


def render_hero(h, render, k=1):
    ts = h["t"] if k == 1 else [h["dur"] * (0.25 + 0.6 * i / max(1, k - 1)) for i in range(k)]
    return render(h["kind"], h["params"], ts, dur=h["dur"], perde=h.get("perde"), mode=h.get("mode"))


def measure(h, render):
    """Tek iş parçacığı (render.py ile aynı: cv2.setNumThreads(1)); duvar saati ms/kare, ısınmadan sonra."""
    import cv2
    cv2.setNumThreads(1)
    t = h["t"][0]
    render(h["kind"], h["params"], [t], dur=h["dur"], perde=h.get("perde"), mode=h.get("mode"))
    t0 = time.perf_counter()
    n = 5
    for i in range(n):
        render(h["kind"], h["params"], [t + 0.1 * (i + 1)], dur=h["dur"], perde=h.get("perde"), mode=h.get("mode"))
    ms = (time.perf_counter() - t0) / n * 1000
    print(f"{h['ad']:14s} {ms:6.0f} ms/kare")
    return ms


# ───────────────────────────── bileşik kahramanlar (HUD / geçişler) ─────────────────────────────
def _frame_of(kind, params, t, dur, mode, perde):
    import shots as SH
    import sk
    sh = SH.shot(kind, 0.0, **params)
    sh.t0, sh.t1, sh.i = 0.0, dur, 1
    f = sk.Frame()
    cx = SH.Ctx(f, t, sh, SH.timeline())
    cx.perde, cx.mode = perde, mode
    SH.KINDS[kind](cx, **params)
    return f


def hero_hud(render):
    """Gündüz çekimi + HUD (yıl rulosu orta kare) + bölüm adı levhası; ayrıca gece çekimi + HUD."""
    import cilt_fx as FX
    out = []
    for mode, perde, year_from, year_to, kw in (("day", 2, 1417, 1418, dict(text="1418", sub="Brunelleschi kubbe için yarışmaya girer", kick="FLORANSA", at=0.2)),
                                               ("night", 3, 1511, 1512, dict(text="1512", sub="Medici'ler Floransa'ya döner", kick="FLORANSA", at=0.2))):
        f = _frame_of("title", kw, 3.4, 8.0, mode, perde)
        ys = FX.YearState([(0.0, year_from), (3.0, year_to)], roll_dur=1.0)
        FX.hud(f, 3.45, ys, perde)
        FX.chapter_tag(f, "IV · KUBBE VE KEFARET", 1.0)
        img = f.rgb()
        out.append(CM.post(img, 3, mode, perde))
    return out


def hero_trans(render):
    import cilt_fx as FX
    out = []
    A = lambda: _frame_of("quote", dict(text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", at=0.1), 4.0, 8.0, "day", 2)
    B = lambda: _frame_of("palle", dict(kick="ALTI TOP", caption="Medici arması", at=0.0), 2.0, 8.0, "day", 2)
    for kind, k in (("yikama", 0.5), ("sayfa", 0.5), ("giornata", 0.5)):
        f = FX.blend(kind, A(), B(), k)
        f.cilt_mode, f.cilt_perde = "day", 2
        out.append(CM.post(f.rgb(), 3, "day", 2))
    return out


CUSTOM = dict(hud=hero_hud, trans=hero_trans)
