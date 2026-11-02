#!/usr/bin/env python3
"""Yayın sonrası kapak (Kanuni açısı): yayin/kapak_K1.jpg, kapak_K2.jpg (1280×720).
Neden: video göz atmada hiç denenmedi (1,0 B gösterim); Türk izleyici "Şarlken"i tanımıyor ama Kanuni'yi tanıyor.
Videoda Kanuni ve 1529 Viyana bölümü var (c7). Çalıştır: python3 kapak_kanuni.py [K1|K2|test]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import icons  # noqa: E402
import medal  # noqa: E402,F401
import scenes_lib  # noqa: E402,F401
import shots as SH  # noqa: E402
import sk  # noqa: E402
import skia  # noqa: E402
from kapak import save  # noqa: E402
from sk import H, W  # noqa: E402


def test():
    f = sk.Frame(); f.bg("night")
    SH.draw_medal(f, "suleyman", 480, 560, 700, "gold")
    SH.draw_medal(f, "karl_olgun", 1440, 560, 700, "gold")
    icons.draw_icon(f, "crown", 960, 300, size=200, metal="gold")
    icons.draw_icon(f, "crown_cracked", 960, 700, size=200, metal="gold")
    return save(f, "kapak_test")


def fit(text, face, size, maxw, track):
    w = sk.text_width(text, face, size, track)
    return size if w <= maxw else size * maxw / w


def duel(name, top, bottom):
    """İki rakip madalya yüz yüze: solda Kanuni, sağda Şarlken (aynalanmış, Kanuni'ye bakar); ortada çatlak taç (odak)."""
    f = sk.Frame(); f.bg("night")
    f.rays(alpha=0.5)
    f.circle(960, 590, 330, shader=f.rad(960, 590, 330, [("#FFE6A0", 0.0, 150), ("#C9962B", 0.45, 50), ("#C9962B", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    SH.draw_medal(f, "suleyman", 470, 590, 640, "gold", tilt=0.12)
    SH.draw_medal(f, "karl_olgun", 1450, 590, 640, "gold", flip=True, tilt=-0.12)
    icons.draw_icon(f, "crown_cracked", 960, 600, size=300, metal="gold", glow=0.7)
    s1 = fit(top, "title", 165, 1780, 8)
    f.gold(top, W / 2, 40 + s1 * 0.78, face="title", size=s1, track=8, glow=0.45)
    s2 = fit(bottom, "title", 165, 1500, 8)
    f.text(bottom, W / 2 - 80, 1040, face="title", size=s2, color="#E5483B", align="c", track=8, shadow=(4, 5, 8, "#000000"))
    f.vig(0.6)
    return save(f, name)


# ——— 2. tur (kurul: iki üye + çapraz eleştiri, başkan kararı) ———
# Kanuni küçük boyda Şarlken'le ikiz okunuyordu: kapak için daha iri, dolgun sarık ve uzun sorguç
import math  # noqa: E402
import medal_extra as MX  # noqa: E402


@MX.reg(MX.HAT, "turban_kapak")
def _hat_turban_kapak(cv, d):
    ax, ay, kx, ky = 480, 330, 1.16, 1.32
    T = lambda pts: [(ax + (x - ax) * kx, ay + (y - ay) * ky) for x, y in pts]  # noqa: E731
    pts = T([(336, 396), (320, 320), (318, 246), (338, 182), (404, 132), (486, 112), (568, 132), (622, 184), (644, 250), (624, 306), (560, 302), (500, 332), (430, 372), (380, 408)])
    path = MX.P(pts, True, 0.4)
    cv.fill(path, 214)
    with MX.clip(cv, path):
        MX.ov(cv, 480, 170, 180, 110, 236, blur=30)
        for k in range(11):
            y = 96 + k * 22
            MX.ln(cv, [(250, y + 40), (470, y - 22), (720, y + 104)], 146, 3.6, 0.5)
            MX.ln(cv, [(250, y + 53), (470, y - 9), (720, y + 117)], 192, 1.7, 0.5)
    cv.stroke(path, 108, 3.0)
    bx, by = 616, 168
    MX.circ(cv, bx, by, 28, 246)
    MX.circ(cv, bx, by, 28, 108, stroke=3)
    for k in range(6):
        a = k / 6 * 2 * math.pi
        MX.pearl(cv, bx + 20 * math.cos(a), by + 20 * math.sin(a), 4.6)
    MX.gem(cv, bx, by, 9, shape="dia")
    MX.plume(cv, [(616, 146), (612, 104), (620, 70), (632, 44)], 64, g=240)


MX.person("suleyman_kapak", MX.INSCR.get("suleyman"), nose=18, hook=-8, brow=4, lip=2, lip2=2, chin=-2, jaw=0.95, fore=0, age=0.2, neck=1.0,
          hat="turban_kapak", beard="goatee", blen=6, must="long", garment="kaftan_x", eye="almond", brow_style="arch", scale=0.90, dy=18)
medal.INSCR["suleyman_kapak"] = medal.INSCR.get("suleyman")


def _fit(text, size, maxw, track):
    w = sk.text_width(text, "title", size, track)
    return size if w <= maxw else size * maxw / w


def title_top(f, l1, l2, scrim=False):
    """İki satır üstte (rozet bölgesi x≥1420, y≥810 boş kalır); tek cümle gibi okunur. Videonun yazı tipi Cinzel korunur."""
    s1 = _fit(l1, 200, 1700, 6); s2 = _fit(l2, 260, 1720, 6)
    y1 = 62 + s1 * 0.74
    y2 = y1 + 22 + s2 * 0.74
    if scrim:
        # yazı bandının arkasında yumuşak kenarlı koyu şerit (yazılardan önce); kartalın üstünde (y≈365) 50 px'te söner
        f.rect(0, 0, W, 366, shader=f.lin(0, 0, 0, 366, [("#000000", 0.0, 190), ("#000000", 316 / 366, 170), ("#000000", 1.0, 0)]))
    f.gold(l1, W / 2, y1, face="title", size=s1, track=6, glow=0.45)
    f.text(l2, W / 2, y2, face="title", size=s2, color="#F05A48", align="c", track=6, shadow=(4, 5, 8, "#000000"), outline=(10, "#1A0E08") if scrim else None)
    return y2 + 10


def duel2(name, l1="KANUNİ'NİN RAKİBİ", l2="TAHTI BIRAKTI"):
    f = sk.Frame(); f.bg("night")
    f.rays(alpha=0.45)
    top = title_top(f, l1, l2)
    r = min(300, (1068 - top - 34) / 2); cy = top + 34 + r
    lx, rx = 450, 1470
    # taraf ışığı: düşük güçte (≤0,25), kırmızı yazıyla yarışmasın
    f.circle(lx, cy, r * 1.25, shader=f.rad(lx, cy, r * 1.25, [("#2F6B4A", 0.0, 60), ("#2F6B4A", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    f.circle(rx, cy, r * 1.25, shader=f.rad(rx, cy, r * 1.25, [("#8E1F26", 0.0, 60), ("#8E1F26", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    SH.draw_medal(f, "suleyman_kapak", lx, cy, 2 * r, "gold", tilt=0.12, alpha=0.84)
    SH.draw_medal(f, "karl_olgun", rx, cy, 2 * r, "gold", flip=True, tilt=-0.12, alpha=0.84)
    # yere bırakılmış bütün imparatorluk tacı (çatlak değil: kimse onu tahttan indirmedi), Şarlken'e doğru eğik; karenin en parlak öğesi
    cxk, cyk = 960, cy + 10
    f.circle(cxk, cyk, 300, shader=f.rad(cxk, cyk, 300, [("#FFF0C0", 0.0, 170), ("#E0B04A", 0.4, 85), ("#C9962B", 1.0, 0)]), blend=skia.BlendMode.kPlus)
    f.oval(cxk + 6, cyk + 132, 210, 22, shader=f.rad(cxk + 6, cyk + 132, 210, [("#000000", 0.0, 200), ("#000000", 1.0, 0)]))
    icons.draw_icon(f, "imperial_crown", cxk, cyk, size=420, metal="gold", glow=0.6, rot=0.08)
    f.vig(0.6)
    return save(f, name)


def hall(name, l1="KANUNİ'NİN RAKİBİ", l2="TAHTI BIRAKTI"):
    """K3: videonun ilk 5 saniyesindeki Brüksel salonu (25 Ekim 1555), aynı yazı; kapak vaadi açılışta karşılanır."""
    f = sk.Frame()
    from shots import Ctx, Shot
    import scenes_d as SD
    sh = Shot("theatre", 0.0, dict(scene="hall", cams=[(0, (1000, 560, 1.55))], p=dict(crowd=True, emperor=False, extra=lambda f, t: SD.draw_pair(f, 1010, 985, 520, 0.0)), vig=0.7, dust_n=0), None, "kapak")
    sh.t0, sh.t1, sh.i = 0.0, 8.0, 1
    cx = Ctx(f, 3.0, sh, SH.timeline())
    SH.KINDS["theatre"](cx, **sh.params)
    f.rect(0, 0, W, H, shader=f.lin(0, 0, 0, H, [("#000000", 0.0, 210), ("#000000", 0.45, 40), ("#000000", 1.0, 120)]))
    f.rect(0, 0, W, H, shader=f.lin(0, 0, W, 0, [("#000000", 0.0, 95), ("#000000", 0.33, 80), ("#000000", 0.4, 0), ("#000000", 0.62, 0), ("#000000", 0.68, 80), ("#000000", 1.0, 95)]))
    title_top(f, l1, l2, scrim=True)
    f.vig(0.6)
    return save(f, name)


if __name__ == "__main__":
    {"test": test,
     "K1": lambda: duel("kapak_K1", "KANUNİ'NİN RAKİBİ", "TAHTI BIRAKTI"),
     "K2": lambda: duel("kapak_K2", "KANUNİ'YE RAKİP OLDU", "SONRA HER ŞEYİ BIRAKTI"),
     "K1v2": lambda: duel2("kapak_K1v2"),
     "K3": lambda: hall("kapak_K3")}[sys.argv[1] if len(sys.argv) > 1 else "test"]()
