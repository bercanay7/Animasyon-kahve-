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
    t = h["t"][0]
    render(h["kind"], h["params"], [t], dur=h["dur"], perde=h.get("perde"), mode=h.get("mode"))
    t0 = time.process_time()
    n = 4
    for i in range(n):
        render(h["kind"], h["params"], [t + 0.1 * (i + 1)], dur=h["dur"], perde=h.get("perde"), mode=h.get("mode"))
    print(f"{h['ad']:14s} {(time.process_time() - t0) / n * 1000:6.0f} ms/kare")
