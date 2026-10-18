"""Bölüm 11 — Adamın Kendisi (63 sn). Ton: yakın, sıcak, melankolik; mum ışığı.
Özel çekim türleri: kinds_c11.py (c11_ önekli). Ortak yardımcılar: bw_lib.py. Simgeler: icons_b.py."""
from shots import shot
import scenes_lib  # noqa: F401  (theatre şablonu + sahne aileleri)
import kinds_c11
import icons_b  # noqa: F401
from bw_lib import fadeout
from sk import W, H

F = ("fade", 0.8)
D = ("dip", 0.9)

GOUT_CAMS = [(0.0, (960, 560, 1.0)), (("c11s7", "perhiz", -0.5), (960, 560, 1.0)), (("c11s7", "yazılır", 0.3), (1060, 610, 1.22))]

TRAVEL_T = [("c11s8", "Almanya", -0.1), ("c11s8", "İtalya", -0.1), ("c11s8", "İspanya", -0.1), ("c11s8", "Hollanda", -0.1),
            ("c11s8", "Fransa", -0.1), ("c11s8", "Tunus", -0.1), ("c11s8", "Cezayir", -0.1)]


def _final_ov(cx):
    kinds_c11.road_overlay(("c11s9", "masada", -0.2), ("c11s9", "yollarda", -0.2))(cx)
    fadeout(cx, 1.0)


SHOTS = [
    # s1 — Peki bu devasa makinenin başındaki adam nasıldı?
    shot("c11_machine", a=("c11s1", 0.0), tr=F, man_at=("c11s1", "makinenin", -0.2), plate_at=("c11s1", "adam", -0.1), q_at=("c11s1", "nasıldı", -0.1), label="makine_ve_adam"),
    # s2 — Habsburg çenesi: ağzını tam kapatamadığı, çiğnemekte zorlandığı yazılır
    shot("c11_chin", a=("c11s2", -0.25), tr=F, zoom_at=("c11s2", "çenesi", -0.1), zoom_dur=2.4, label_at=("c11s2", "Habsburg", -0.1), tag_at=("c11s2", "yazılır", -0.15), label="cene"),
    # s3 — 2019 çalışması: küçük, kesin değil
    shot("c11_study", a=("c11s3", -0.25), tr=F, year_at=("c11s3", "2019'daki", -0.1), portrait_at=("c11s3", "portrelerindeki", -0.1), face_at=("c11s3", "yüz", -0.1),
         kin_at=("c11s3", "akraba", -0.15), link_at=("c11s3", "ilişkilendirdi", -0.25), small_at=("c11s3", "küçüktü", -0.45), sure_at=("c11s3", "kesin", -0.1), label="calisma_2019"),
    # s4 — 26 yaşında Portekizli kuzeni İsabel'le evlendi
    shot("c11_wed", a=("c11s4", -0.25), tr=F, age_at=("c11s4", "26", -0.1), isabel_at=("c11s4", "Portekizli", -0.2), ring_at=("c11s4", "evlendi", -0.2), label="evlilik"),
    # s5a — 1539: İsabel otuz beş yaşında öldü
    shot("c11_loss", a=("c11s5", -0.2), tr=F, year_at=("c11s5", "1539'da", -0.1), age_at=("c11s5", "otuz", -0.1), death_at=("c11s5", "öldü", -0.25), label="isabel_oldu"),
    # s5b — yaklaşık iki ay manastıra çekildi; bir daha da evlenmedi
    shot("bw_theatre", a=("c11s5", "Şarlken", -0.3), tr=D, scene="cloister", dust_n=36, cams=[(0.0, (960, 560, 1.0)), (("c11s5", "evlenmedi", 0.4), (980, 580, 1.2))], p=dict(time="dusk", monks=1, lamps=True),
         overlay=kinds_c11.cloister_overlay(("c11s5", "yaklaşık", -0.1), ("c11s5", "iki", -0.1), ("c11s5", "daha", -0.2)), label="manastir"),
    # s6 — ömrünün sonuna kadar siyah giydiği anlatılır
    shot("c11_black", a=("c11s6", -0.3), tr=F, black_at=("c11s6", "siyah", -0.4), tag_at=("c11s6", "anlatılır", -0.25), label="siyah"),
    # s7 — gut atakları, perhiz, bol yemek (bedroom: hasta yastıklara yaslı; bacakta zonklama, komodinde yemek)
    shot("bw_theatre", a=("c11s7", -0.3), tr=("fade", 0.5), scene="bedroom", dust_n=36, cams=GOUT_CAMS, p=dict(candle=1.0),
         overlay=kinds_c11.gout_overlay(GOUT_CAMS, ("c11s7", "Gut", -0.05), ("c11s7", "hareketsiz", -0.1), ("c11s7", "perhiz", -0.1), ("c11s7", "yemeği", -0.1), ("c11s7", "yazılır", -0.1)), label="gut_perhiz"),
    # s8 — bizzat dolaşarak yönetti: gezi ağı
    shot("map", a=("c11s8", -0.3), tr=F, cams=[(0.0, (5.0, 44.7, 1.10)), (("c11s8", "Cezayir", 0.5), (5.0, 44.7, 1.14))],
         regions=[dict(name="karl_kendi", color="habsburg", at=("c11s8", "imparatorluğu", -0.2), alpha=0.28)],
         extra=kinds_c11.make_travel(TRAVEL_T, dur=1.0), approx=True, label="gezi_agi"),
    # s9 — İmparatorluğu bir masada değil, yollarda taşıdı
    shot("map", a=("c11s9", -0.3), tr=F, cams=[(0.0, (5.0, 44.7, 1.14)), (("c11s9", "taşıdı", 0.5), (5.5, 44.5, 1.06))],
         regions=[dict(name="karl_kendi", color="habsburg", at=0.0, alpha=0.28)],
         extra=lambda cx, cam, mv: (kinds_c11.make_travel(TRAVEL_T, dur=1.0, all_done=True)(cx, cam, mv), _final_ov(cx)), approx=True, label="yollarda"),
]
