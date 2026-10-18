"""cilt_hero — preview_cilt.py için kahraman çekim tanımları (gün: sayfa 1, gece/HUD/kart/geçiş: sayfa 2)."""
import time

import cilt_medici as CM
import numpy as np
from sk import FPS, H, W

LEDGER_L = [
    dict(text="Per lana di Francia", amt=(412, 6, 8), at=0.8),
    dict(text="Per seta di Lucca", amt=(180, 0, 0), at=2.2),
    dict(text="A messer Cosimo", amt=(1500, 0, 0), at=3.6, hl=7.6),
    dict(text="Per cambio di Bruggia", amt=(96, 3, 4), at=5.0, strike=8.4),
    dict(text="Alla compagnia di Roma", amt=(250, 0, 0), at=6.4),
    dict(text="Per la bottega", amt=(31, 4, 0), at=7.6),
]
LEDGER_R = [
    dict(text="Da Giovanni di Bicci", amt=(1500, 0, 0), at=1.5),
    dict(text="Da Vieri di Cambio", amt=(640, 2, 0), at=2.9),
    dict(text="Per merce venduta", amt=(88, 5, 6), at=4.3),
]
HEROES = [
    dict(ad="fresco_title", kind="fresco_title", params=dict(), t=[5.4], dur=9.0, sayfa=2, mode="night", perde=2),
    dict(ad="title_day", kind="title", params=dict(text="MEDİCİ", sub="BANKACILAR AİLESİ", kick="FLORANSA", at=0.3), t=[3.2], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="palle_day", kind="palle", params=dict(kick="ALTI TOP", caption="Medici arması", at=0.2), t=[3.0], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="coin_day", kind="coin", params=dict(kick="1252", sub="Florin", caption="Bir yüzünde zambak, ötekinde Vaftizci Yahya", at=0.2, n=4), t=[3.0], dur=8.0, sayfa=1, mode="day", perde=1),
    dict(ad="chapter_card", kind="chapter_card", params=dict(n="IV", title="Kubbe ve Kefaret", years="1418 – 1460'lar", perde_label="PERDE II — BEDEL"), t=[1.6], dur=3.0, sayfa=2, mode="night", perde=2),
    dict(ad="quote_day", kind="quote", params=dict(text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", src="Aile Antlaşması, 1737", at=0.2), t=[3.5], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="ledger", kind="ledger", params=dict(left=LEDGER_L, right=LEDGER_R, head="MCCCXCVII", total=dict(text="Somma", amt=(2469, 2, 6), at=9.2, row=8), focus=(900, 420)),
         t=[10.5], dur=12.0, sayfa=1, mode="day", perde=1),
    dict(ad="letter", kind="letter", params=dict(addr=("Al Magnifico Signore", "Lorenzo de' Medici", "in Firenze"), open_at=3.6, seal_at=0.7,
                                                 lines=[("Magnifico et honorando padre,", 4.6), ("ho ricevuto la vostra lettera", 5.9), ("et subito ho dato ordine ai nostri", 7.2), ("a Bruggia et a Londra.", 8.5)],
                                                 sig=("Il vostro Piero", 10.0), date="a dì 12 d'aprile"),
         t=[11.6], dur=14.0, sayfa=1, mode="day", perde=2),
    dict(ad="doc", kind="doc", params=dict(title="CONVENTIO", lines=[("Che nulla si tolga da Firenze,", 1.2), ("né quadri, né statue, né libri,", 2.6), ("ma tutto resti per ornamento", 4.0), ("della città et per utilità del pubblico.", 5.4)],
                                           seal=True, seal_at=7.0, date="31 ottobre 1737", hl=(-250, 80, 780), hl_at=6.2, at=0.2),
         t=[8.2], dur=10.0, sayfa=1, mode="day", perde=3),
    dict(ad="medal_day", kind="medal", params=dict(key="m_cosimo", name="COSIMO DE' MEDICI", role="banker ve şehrin sessiz efendisi", dates="1389 – 1464", pos="c", at=0.2), t=[3.4], dur=8.0, sayfa=1, mode="day", perde=1),
    dict(ad="medals_day", kind="medals", params=dict(items=[dict(key="m_cosimo", name="COSIMO", role="1389 – 1464"), dict(key="m_lorenzo", name="LORENZO", role="1449 – 1492")], size=560, vs=2.0), t=[3.6], dur=8.0, sayfa=1, mode="day", perde=2),
    dict(ad="map_day", kind="map", params=dict(
        cam=(6.0, 47.6, 1.75),
        regions=[dict(name="floransa", color="floransa", at=0.3, alpha=0.62), dict(name="papalik", color="papalik", at=0.5, alpha=0.5), dict(name="venedik", color="azurite", at=0.7, alpha=0.5),
                 dict(name="milano", color="terra", at=0.9, alpha=0.5)],
        cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=1.0, side="b", size=34), dict(lon=12.5, lat=41.9, name="Roma", at=1.3, size=32), dict(lon=12.33, lat=45.44, name="Venedik", at=1.5, size=32, side="r"),
                dict(lon=9.19, lat=45.46, name="Milano", at=1.7, size=32, side="t"), dict(lon=6.14, lat=46.2, name="Cenevre", at=1.9, size=32, side="t"), dict(lon=4.83, lat=45.76, name="Lyon", at=2.1, size=32, side="l"),
                dict(lon=3.22, lat=51.21, name="Brugge", at=2.3, size=32, side="r"), dict(lon=-0.12, lat=51.5, name="Londra", at=2.5, size=32, side="t")],
        routes=[dict(pts=[(11.25, 43.77), (6.14, 46.2), (3.22, 51.21)], at=2.4, dur=2.0, width=6), dict(pts=[(3.22, 51.21), (-0.12, 51.5)], at=4.0, dur=1.0, width=6)],
        date=("1470", 0.5)), t=[6.0], dur=9.0, sayfa=1, mode="day", perde=2),
    dict(ad="timeline_day", kind="timeline", params=dict(a0=1390, a1=1500, step=10, title="PARA — İTİBAR — İKTİDAR",
        events=[(1397, "Orsanmichele köşesi", 0.8), (1429, "Giovanni ölür", 1.5), (1434, "Cosimo döner", 2.2), (1464, "Cosimo ölür", 2.9), (1478, "Pazzi", 3.6), (1494, "Sürgün", 4.3)],
        hl=(1434, 1464, "30 YIL", 3.2)), t=[6.0], dur=9.0, sayfa=1, mode="day", perde=1),
    dict(ad="network_day", kind="network", params=dict(title="EVLİLİK, ORTAKLIK, REKABET", nodes=[dict(id="m", name="MEDICI", key="m_cosimo", x=0.50, y=0.42, size=190, at=0.3), dict(id="b", name="BARDI", initials="B", x=0.22, y=0.30, at=0.8, color="lapis"),
        dict(id="t", name="TORNABUONI", initials="T", x=0.27, y=0.62, at=1.1, color="terra"), dict(id="o", name="ORSINI", initials="O", x=0.78, y=0.30, at=1.4, color="madder"),
        dict(id="p", name="PAZZI", initials="P", x=0.76, y=0.62, at=1.7, color="umber"), dict(id="s", name="SFORZA", initials="S", x=0.50, y=0.78, at=2.0, color="azurite")],
        edges=[("m", "b", "evlilik", 1.0), ("m", "t", "evlilik", 1.3), ("m", "o", "evlilik", 1.6), ("m", "p", "rakip", 1.9), ("m", "s", "ittifak", 2.2), ("b", "t", "ortaklik", 2.5)]),
        t=[6.0], dur=9.0, sayfa=1, mode="day", perde=2),
    dict(ad="tree_day", kind="tree", params=dict(title="BİR HANEDANIN ÜÇ KUŞAĞI", size=210, nodes=[
        dict(id="g", key="m_giovanni", name="GIOVANNI", dates="1360 – 1429", x=0.5, y=0.26, at=0.3), dict(id="c", key="m_cosimo", name="COSIMO", dates="1389 – 1464", x=0.34, y=0.60, at=1.0),
        dict(id="l", key="m_lorenzo", name="LORENZO", dates="1449 – 1492", x=0.66, y=0.60, at=1.7)], edges=[("g", "c", 0.7), ("g", "l", 1.4)]), t=[5.0], dur=9.0, sayfa=1, mode="day", perde=1),
    dict(ad="bars_day", kind="bars", params=dict(title="ÖRNEK VERİ", items=[("Roma", 120, "lapis", 0.4), ("Venedik", 90, "cinnabar", 0.9), ("Brugge", 70, "ochre", 1.4), ("Londra", 45, "terra", 1.9)], unit="FLORİN", maxv=130), t=[5.0], dur=9.0, sayfa=1, mode="day", perde=1),
    dict(ad="stacked_day", kind="stacked", params=dict(title="ÖRNEK PAYLAŞIM", parts=[("ÇEYİZ", 1500, "ochre", 0.4), ("ORTAKLIK", 3000, "lapis", 1.2), ("KÂR", 4200, "cinnabar", 2.0)], total_label="8.700 FLORİN"), t=[5.0], dur=9.0, sayfa=1, mode="day", perde=1),
    dict(ad="iconrow_day", kind="iconrow", params=dict(title="BANKACININ MASASI", items=[dict(icon="coins", label="FLORİN"), dict(icon="scales", label="TERAZİ"), dict(icon="quill", label="KALEM"), dict(icon="book", label="DEFTER"), dict(icon="scroll", label="SENET")]), t=[4.5], dur=9.0, sayfa=1, mode="day", perde=1),
    dict(ad="frieze_day", kind="frieze", params=dict(seed=3, speed=34.0, kick="MAGİ ALAYI TARZI"), t=[5.0], dur=12.0, sayfa=1, mode="day", perde=2),
    dict(ad="skyline_day", kind="skyline", params=dict(seed=1, pan=300.0, kick="FLORANSA, 1434", labels=[dict(on="duomo", at=1.4), dict(on="pv", at=2.1), dict(on="ponte", at=2.8), dict(on="campanile", at=3.5)]), t=[5.0], dur=12.0, sayfa=1, mode="day", perde=2),
    dict(ad="counter_day", kind="counter", params=dict(value=1500, unit="florin", label="Piccarda'nın çeyizi", coin=True, at=0.2), t=[3.2], dur=8.0, sayfa=1, mode="day", perde=1),
    dict(ad="skyline_night", kind="skyline", params=dict(seed=2, pan=300.0, kick="FLORANSA, GECE", caption="Pazzi sabahından önceki gece"), t=[5.0], dur=12.0, sayfa=2, mode="night", perde=2),
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
    """Malzeme geçişleri (yıkama / sayfa / giornata) ortada."""
    import cilt_fx as FX
    out = []
    A = lambda: _frame_of("quote", dict(text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", at=0.1), 4.0, 8.0, "day", 2)
    B = lambda: _frame_of("palle", dict(kick="ALTI TOP", caption="Medici arması", at=0.0), 2.0, 8.0, "day", 2)
    for kind, k in (("yikama", 0.5), ("sayfa", 0.5), ("giornata", 0.5)):
        f = FX.blend(kind, A(), B(), k)
        f.cilt_mode, f.cilt_perde = "day", 2
        out.append(CM.post(f.rgb(), 3, "day", 2))
    return out


def hero_trans2(render):
    """Yeni geçişler (YONETMENLIK §3): iris · slide · zoomthru · carry · light · candle — her biri k=0,5'te (gerçek kullanım: preview_reel.py)."""
    import cilt_fx as FX
    out = []
    qa = dict(text="Hiçbir şey buradan çıkmayacak.", who="ANNA MARIA LUISA", at=0.1)
    pa = dict(kick="ALTI TOP", caption="Medici arması", at=0.0)
    co = dict(kick="1252", sub="Florin", at=0.0, n=1)
    sk_ = dict(seed=1, pan=200, kick="FLORANSA")
    cases = [("iris", ("coin", co, 3.0), ("skyline", sk_, 2.0), dict(at=(960, 508), obj="florin", r=252)),
             ("slide", ("skyline", sk_, 4.0), ("quote", qa, 3.0), dict(dir="r")),
             ("zoomthru", ("skyline", sk_, 4.0), ("palle", pa, 3.0), dict(at=(1150, 560))),
             ("carry", ("palle", pa, 3.0), ("quote", qa, 3.0), dict(dir="r", strip="ribbon")),
             ("light", ("quote", qa, 4.0), ("palle", pa, 3.0), dict()),
             ("candle", ("quote", qa, 4.0), ("palle", pa, 3.0), dict(at=(1700, 600)))]
    for kind, (ka, pa_, ta), (kb, pb, tb), opts in cases:
        f = FX.blend(kind, _frame_of(ka, pa_, ta, 8.0, "day", 2), _frame_of(kb, pb, tb, 8.0, "day", 2), 0.5, 9.0, d=0.9, **opts)
        f.cilt_mode, f.cilt_perde = "day", 2
        out.append(CM.post(f.rgb(), 3, "day", 2))
    return out


CUSTOM = dict(hud=hero_hud, trans=hero_trans, trans2=hero_trans2)
