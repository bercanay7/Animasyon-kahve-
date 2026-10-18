"""Bölüm 0 — Soğuk açılış: Brüksel, 25 Ekim 1555 (46 sn). Ton: sıcak altın/kara, merak. KİMLİK GİZLİ: isim levhası s8'den önce yok.
Ayna bölüm: c12 aynı salonun ikinci görünüşüdür (aynı `hall`; c12'de ağır altın ışık + ters kamera). Yazar D.
Not: kaynak kapısı gereği baston YOK (c0s4: 'Kolunu genç bir prensin omzuna dayamış') → `d_pair` bastonsuz figür."""
import math

import scenes_lib  # noqa: F401  (theatre)
import d_common as D  # noqa: F401  (wd_* türleri)
import scenes_d as SD
import shots_c0 as S0  # noqa: F401  (c0_* türleri)
import icons
import shots as SH
import sk
from d_common import A, AE, tag
from shots import shot
from sk import W, H

TL = SH.timeline()
T_H1 = TL.resolve(A("c0s2", -0.3))           # salonun ilk çekim başlangıcı (çift figürün konum sürekliliği için)


def _pair_x(T, t):
    """Çiftin sahne x'i: çekimler arasında sürekli (global zaman), çok yavaş sağa kayar."""
    return 1130.0 + 6.0 * (T + t - T_H1)


def _pair_extra(start_anchor, walk=False, h=520, y=985):
    T = TL.resolve(start_anchor)

    def extra(f, t):
        SD.draw_pair(f, _pair_x(T, t), y, h, t, walk=walk)
    return extra


# ── kamera anahtarları (çekim başına; ekran etiketleri için de kullanılır)
_S3 = A("c0s3", -0.3)
_CAM3 = SD.keys_local([(_S3, (1060, 600, 1.1)), (A("c0s3", "duruyor", 0.4), (1100, 588, 1.45))], _S3)


def _ov_brussels(cx):
    k = cx.amt(A("c0s2", "Brüksel'de", 0.0), 0.7)
    tag(cx.f, "BRÜKSEL", 96, 128, k, size=36, sub="büyük salon")


def _ov_age(cx):
    """'elli beş yaşında': çiftin başının yanında ince bir yaş levhası."""
    cam = SD.cam_at(cx.t, _CAM3)
    px = _pair_x(TL.resolve(_S3), cx.t)
    sx, sy = SD.scene_to_screen(px - 60, 556, cam)
    k = cx.amt(A("c0s3", "elli", -0.15), 0.6)
    if k > 0:
        # ince çizgi: levhadan başa
        tx, ty = sx - 330, sy - 150
        cx.f.line(tx + 150, ty + 60, sx - 36, sy - 20, color="#C9962B", sw=2, alpha=0.8 * k)
        cx.f.circle(sx - 36, sy - 20, 5, color="#F0D27A", alpha=k)
        tag(cx.f, "55 YAŞINDA", tx, ty, k, size=34)


_S5 = A("c0s7", -0.3)
_CAM5 = SD.keys_local([(_S5, (1120, 690, 1.55)), (A("c0s7", "başlıyor", 0.7), (1000, 560, 1.0))], _S5)


def _ov_flare(cx):
    """'hepsini bırakmaya başlıyor': pencerenin ışığı yavaşça taşar."""
    k = cx.amt(A("c0s7", "hepsini", -0.1), 2.2)
    if k > 0:
        cam = SD.cam_at(cx.t, _CAM5)
        sx, sy = SD.scene_to_screen(W / 2, 330, cam, depth=0.05)
        r = 520 + 700 * k
        cx.f.circle(sx, sy, r, shader=cx.f.rad(sx, sy, r, [("#FFE7B0", 0.0, int(150 * k)), ("#FFC46E", 0.5, int(60 * k)), ("#FFB347", 1.0, 0)]), blend=sk.skia.BlendMode.kPlus)


SHOTS = [
    # 0:00 — tarih kartı (s1)
    shot("title", a=0.0, text="25 EKİM 1555", size=132, at=0.35, y=0.5, label="tarih"),
    # s2 — Brüksel'de büyük salon tıklım tıklım dolu (geniş; kamera yavaşça kalabalığa süzülür — c12'de TERS gelir)
    shot("theatre", a=A("c0s2", -0.3), tr=("fade", 0.9), scene="hall", cams=[(0.0, (960, 560, 1.0)), (A("c0s3", -0.4), (1010, 612, 1.24))],
         p=dict(emperor=False, extra=_pair_extra(A("c0s2", -0.3))), overlay=_ov_brussels, label="salon_genis"),
    # s3 — ortada, 55 yaşında, ayakta zor duruyor
    shot("theatre", a=_S3, tr=("fade", 0.7), scene="hall", cams=_CAM3 and [(t, v) for t, v in _CAM3],
         p=dict(emperor=False, extra=_pair_extra(_S3)), overlay=_ov_age, label="cift_orta"),
    # s4 — kolunu genç prensin omzuna dayamış (yakın plan: el + omuz; baston YOK)
    shot("theatre", a=A("c0s4", -0.2), tr=("fade", 0.5), scene="hall", cams=[(0.0, (1175, 655, 2.0)), (AE("c0s4", 0.9), (1205, 628, 2.4))],
         p=dict(emperor=False, extra=_pair_extra(A("c0s4", -0.2))), label="omuz_yakin"),
    # s5a — kırk yıldır (kum saati akar, 40 sayılır; c12'de "40 YIL" zaman çizgisi olarak geri gelir)
    shot("c0_forty", a=A("c0s5", "adam", -0.05), tr=("fade", 0.6), at_num=A("c0s5", "kırk", -0.12), at_unit=A("c0s5", "yıldır", -0.1), count_dur=0.45, label="kirk_yil"),
    # s5b — Avrupa'nın büyük bölümünü yönetiyor (Habsburg toprakları sırayla yanar)
    shot("map", a=A("c0s5", "Avrupa'nın", 0.12), tr=("fade", 0.5), cams=[(0.0, (7, 46.0, 1.28)), (AE("c0s5", 0.4), (6, 45.2, 1.5))],
         regions=[dict(name="ispanya", color="ispanya", at=A("c0s5", "Avrupa'nın", 0.2)),
                  dict(name="hollanda", color="burgonya", at=A("c0s5", "büyük", -0.2)), dict(name="franche_comte", color="burgonya", at=A("c0s5", "büyük", -0.05)),
                  dict(name="almanya", color="#7A6A3A", at=A("c0s5", "büyük", 0.1), alpha=0.35, hatch=True),
                  dict(name="avusturya", color="avusturya", at=A("c0s5", "bölümünü", -0.05)),
                  dict(name="napoli", color="ispanya", at=A("c0s5", "yönetiyor", -0.1)), dict(name="sicilya", color="ispanya", at=A("c0s5", "yönetiyor", 0.0)),
                  dict(name="sardunya", color="ispanya", at=A("c0s5", "yönetiyor", 0.1))],
         labels=[dict(text="İSPANYA", lon=-3.5, lat=41.3, size=40, at=A("c0s5", "Avrupa'nın", 0.3)),
                 dict(text="KUTSAL ROMA İMPARATORLUĞU", lon=14.5, lat=51.6, size=30, at=A("c0s5", "bölümünü", -0.1), color="#E8D8A0", track=8)],
         date=("1555", A("c0s5", "Avrupa'nın", -0.1)), label="avrupa"),
    # s6 — Yeni Dünya'da fethedilen topraklar da onun adına (Atlantik'in ötesi: geniş kadraj, wipe ile açılır)
    shot("map", a=A("c0s6", -0.3), tr=("wipe", 0.9), cams=[(0.0, (-44, 27, 0.66)), (AE("c0s6", 0.0), (-46, 26, 0.70))],
         regions=[dict(name="ispanya", color="ispanya", at=0.0), dict(name="yeni_ispanya", color="ispanya", at=A("c0s6", "fethedilen", 0.2)),
                  dict(name="peru_ispanya", color="ispanya", at=A("c0s6", "topraklar", 0.2))],
         labels=[dict(text="YENİ DÜNYA", lon=-75, lat=36, size=44, at=A("c0s6", "Yeni", 0.1)), dict(text="ATLANTİK OKYANUSU", lon=-38, lat=33, size=32, color="#9FB8C8", at=A("c0s6", "Dünya'da", 0.3))],
         routes=[dict(pts=[(-6, 37), (-24, 33), (-52, 24), (-76, 19.5)], at=A("c0s6", "fethedilen", -0.3), dur=2.2, color="#F0D27A", width=5)],
         icons_=[dict(kind="ship", lon=-6, lat=37, size=70, at=A("c0s6", "fethedilen", -0.3), route=[(-6, 37), (-24, 33), (-52, 24), (-76, 19.5)], move_at=A("c0s6", "fethedilen", -0.3), move_dur=2.2, bob=3, glow=0.3)],
         label="yeni_dunya"),
    # s7 — ve bugün, hepsini bırakmaya başlıyor (geri çekilen kamera, taşan pencere ışığı)
    shot("theatre", a=_S5, tr=("fade", 0.9), scene="hall", cams=[(t, v) for t, v in _CAM5],
         p=dict(emperor=False, extra=_pair_extra(_S5, walk=True)), overlay=_ov_flare, label="salon_birakma"),
    # s8 — kimse onu tahttan indirmedi (ilk kez bir levha: V. KARL)
    shot("medal", a=A("c0s8", -0.35), tr=("fade", 0.8), key="karl_yasli", name="V. KARL", role="İmparator", dates="1500 – 1558", pos="c", size=700, plate_at=A("c0s8", "tahttan", -0.15), label="medal"),
    # s9 — peki neden?
    shot("emblem", a=A("c0s9", -0.2), tr=("fade", 0.4), icon="question", size=560, at=0.0, label="neden"),
    # s10 — beş cephe: bankacı, keşiş, kral, sultan, miras
    shot("c0_fronts", a=A("c0s10", -0.3), tr=("fade", 0.7), at_title=A("c0s10", "beş", -0.2), at_slots=A("c0s10", "Cevap", 0.0),
         words=[A("c0s10", "bankacı", -0.15), A("c0s10", "keşiş", -0.15), A("c0s10", "kral", -0.15), A("c0s10", "sultan", -0.15), A("c0s10", "miras", -0.15)],
         at_all=A("c0s10", "miras", 0.6), label="cephe5"),
    # s11a — ilk kanıt, taç daha takılmadan ortaya çıkıyor
    shot("emblem", a=A("c0s11", -0.3), tr=("fade", 0.7), icon="imperial_crown", size=440, kick="İLK KANIT", at=0.3, label="ilk_kanit"),
    # s11b — o taç, büyük ölçüde borçla alındı
    shot("c0_borc", a=A("c0s11", "taç", -0.3, 1), tr=("fade", 0.6), at_coins=A("c0s11", "büyük", -0.35), at_big=A("c0s11", "büyük", -0.1), at_stamp=A("c0s11", "borçla", -0.1), label="tac_borc"),
    # s12 — başlık
    shot("title", a=A("c0s12", -0.2), tr=("fade", 0.6), text="ŞARLKEN", at=0.2, size=190, label="baslik"),
]
