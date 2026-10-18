"""Bölüm 0 — Soğuk açılış: Brüksel, 25 Ekim 1555 (örnek sahne dosyası: diğer bölümler bunun biçimini izler)."""
import math
from shots import shot
import scenes_lib  # theatre şablonunu kaydeder
import icons
import sk
from sk import W, H

def _q_overlay(cx):
    f = cx.f
    a = cx.amt(("c0s9", 0.0), 0.5)
    icons.draw_icon(f, "question", W * 0.80, H * 0.45, size=300, metal="gold", alpha=a, glow=0.5 * a)

SHOTS = [
    # 0:00 — tarih kartı (s1)
    shot("title", a=0.0, text="25 EKİM 1555", sub="BRÜKSEL", size=130, at=0.35, sub_at=("c0s2", 0.0), y=0.5, label="tarih"),
    # s2–s4 — Coudenberg salonu; yavaş yaklaşma
    shot("theatre", a=("c0s2", -0.5), tr=("fade", 0.9), scene="hall", cams=[(0.0, (960, 560, 1.0)), (("c0s5", -0.4), (990, 650, 1.55))], p=dict(), label="salon"),
    # s5 — "Avrupa'nın büyük bölümü": Habsburg toprakları yanar
    shot("map", a=("c0s5", -0.35), tr=("fade", 0.8), cams=[(0.0, (9, 46.5, 1.25)), (("c0s5", 3.0), (9, 46.5, 1.7))],
         regions=[dict(name="almanya", color="#7A6A3A", at=("c0s5", "Avrupa'nın", -0.2), alpha=0.35, hatch=True),
                  dict(name="ispanya", color="ispanya", at=("c0s5", "kırk", 0.0)), dict(name="hollanda", color="burgonya", at=("c0s5", "yıldır", 0.0)),
                  dict(name="franche_comte", color="burgonya", at=("c0s5", "yıldır", 0.2)), dict(name="avusturya", color="avusturya", at=("c0s5", "büyük", 0.0)),
                  dict(name="napoli", color="ispanya", at=("c0s5", "bölümünü", 0.0)), dict(name="sicilya", color="ispanya", at=("c0s5", "bölümünü", 0.1)),
                  dict(name="sardunya", color="ispanya", at=("c0s5", "bölümünü", 0.2))],
         labels=[dict(text="İSPANYA", lon=-4, lat=40.0, size=40, at=("c0s5", "kırk", 0.1)), dict(text="KUTSAL ROMA İMPARATORLUĞU", lon=11, lat=50.3, size=30, at=("c0s5", "Avrupa'nın", 0.0), color="#E8D8A0", track=8)],
         date=("1555", 0.2), label="avrupa"),
    # s6 — Yeni Dünya: Atlantik'in ötesi
    shot("map", a=("c0s6", -0.3), tr=("fade", 0.7), cams=[(0.0, (9, 46.5, 1.7)), (("c0s6", 2.0), (-62, 12, 0.62))],
         regions=[dict(name="ispanya", color="ispanya", at=0.0), dict(name="yeni_ispanya", color="ispanya", at=("c0s6", "fethedilen", 0.2)), dict(name="peru_ispanya", color="ispanya", at=("c0s6", "topraklar", 0.2))],
         labels=[dict(text="YENİ DÜNYA", lon=-80, lat=24, size=44, at=("c0s6", "Yeni", 0.2)), dict(text="ATLANTİK OKYANUSU", lon=-38, lat=33, size=32, color="#9FB8C8", at=("c0s6", 1.0))],
         routes=[dict(pts=[(-6, 37), (-30, 33), (-60, 25), (-80, 21)], at=("c0s6", "fethedilen", 0.0), dur=2.4, color="#F0D27A", width=5)],
         label="yeni_dunya"),
    # s7 — salona dönüş, yakın plan
    shot("theatre", a=("c0s7", -0.4), tr=("fade", 0.9), scene="hall", cams=[(0.0, (990, 640, 1.7)), (("c0s7", 3.0), (985, 700, 2.1))], p=dict(crowd=True), label="yakin"),
    # s8–s9 — kimse indirmedi / neden?
    shot("medal", a=("c0s8", -0.3), tr=("fade", 0.8), key="karl_yasli", name="V. KARL", role="İmparator · 55 yaşında", dates="1500 – 1558", pos="l", size=760, plate_at=0.8, extra=_q_overlay, label="medal"),
    # s10 — beş cephe
    shot("iconrow", a=("c0s10", -0.3), tr=("fade", 0.7), title="BEŞ CEPHE", size=210, y=H * 0.5,
         items=[dict(icon="coinbag", label="BANKACI", at=("c0s10", "bankacı", -0.2)), dict(icon="monk", label="KEŞİŞ", at=("c0s10", "keşiş", -0.2)),
                dict(icon="crown", label="KRAL", at=("c0s10", "kral", -0.2)), dict(icon="crescent", label="SULTAN", at=("c0s10", "sultan", -0.2)),
                dict(icon="family", label="MİRAS", at=("c0s10", "miras", -0.2))], label="cephe5"),
    # s11 — ilk kanıt: taç borçla alındı
    shot("emblem", a=("c0s11", -0.3), tr=("fade", 0.7), icon="imperial_crown", size=430, kick="İLK KANIT", sub=None, stampt=("BORÇLA", 960, 800, ("c0s11", "borçla", -0.1), 90), label="tac_borc"),
    # s12 — başlık
    shot("title", a=("c0s12", -0.2), tr=("fade", 0.6), text="ŞARLKEN", at=0.2, size=190, label="baslik"),
]
