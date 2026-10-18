"""Bölüm 9 — Yeni Dünya: Altın, Gümüş ve Vicdan (≈109 sn). Ton: tropik yeşil + altın + kan; son kısım vicdan (sade).
Yazar D. Ağır konularda (esaret, idam, fetih) sakin ve saygılı görsel dil; yerli halk klişe/karikatür YOK (madalya + harita + belge ağırlıklı)."""
import math

import scenes_lib  # noqa: F401  (theatre şablonu)
import d_common  # noqa: F401  (wd_* türleri)
import shots_c9 as S9
import sk
from d_common import A, AE, icn
from shots import shot
from sk import W, H

C9 = "c9"

SHOTS = [
    # s1 — "hiç görmedi / onun adına fethedildi": Atlantik; kesikli çizgi yarı yolda söner; fetih bölgeleri yanar
    shot("map", a=A("c9s1", -0.25), tr=("fade", 0.8), cams=[(0.0, (-38, 29, 0.62)), (A("c9s1", "fethedildi", 1.6), (-46, 26, 0.72))],
         regions=[dict(name="ispanya", color="ispanya", at=0.3),
                  dict(name="yeni_ispanya", color="ispanya", at=A("c9s1", "fethedildi", -0.1)), dict(name="peru_ispanya", color="ispanya", at=A("c9s1", "fethedildi", 0.15))],
         labels=[dict(text="ATLANTİK OKYANUSU", lon=-42, lat=19.5, size=30, color="#9FB8C8", at=0.8, track=12),
                 dict(text="YENİ DÜNYA", lon=-96, lat=33, size=36, at=A("c9s1", "Yeni", -0.1), track=12)],
         extra=S9.open_extra, label="atlantik_hic"),
    # s2a — Cortés: Küba → Veracruz → Tenochtitlan (izinsiz)
    shot("map", a=A("c9s2", -0.1), tr=("fade", 0.8), cams=[(0.0, (-87.0, 21.4, 1.85)), (A("c9s2", "yola", -0.4), (-88.2, 21.0, 2.05))],
         regions=[dict(name="aztek", color="#C0762B", at=A("c9s2", "Hernán", 0.0), alpha=0.40)],
         labels=[dict(text="KÜBA", lon=-79.0, lat=21.9, size=34, at=A("c9s2", "Küba", -0.1)), dict(text="AZTEK", lon=-98.4, lat=22.9, size=30, color="#F0D8A0", at=A("c9s2", "Hernán", 0.3))],
         routes=[dict(pts=[(-82.4, 23.1), (-86.9, 20.6), (-92.5, 19.5), (-96.1, 19.2), (-99.13, 19.43)], at=A("c9s2", "yola", -0.25), dur=2.3, color="#F0D27A", width=6)],
         cities=[dict(lon=-96.1, lat=19.2, name="VERACRUZ", kind="town", at=A("c9s2", "yola", 0.9), side="b", size=28),
                 dict(lon=-99.13, lat=19.43, name="TENOCHTİTLAN", kind="capital", at=A("c9s2", "yola", 1.7), side="t", size=28)],
         notes=[dict(text="KÜBA VALİSİNİN İZNİ OLMADAN", x=120, y=190, at=A("c9s2", "izni", -0.15), w=700, size=36)],
         date=("1519", A("c9s2", 0.0)), extra=S9.cortes_extra, label="cortes_rota"),
    # s2b — Tenochtitlan düştü (göl kenti; siege/tenochtitlan — sahne-lab)
    shot("theatre", a=A("c9s2", "13", -0.4), tr=("fade", 1.0), scene="siege", cams=[(0.0, (960, 540, 1.0)), (AE("c9s2", 0.6), (960, 590, 1.28))],
         p=dict(city="tenochtitlan", time="dusk", fire=0.6), overlay=S9.tenoch_overlay, label="tenochtitlan"),
    # s3 — Cortés'in mektupları: fethi anlatan ama kendini savunan
    shot("wd_doc", a=A("c9s3", -0.15), tr=("fade", 0.8), tone="#C9B484", title="CORTÉS'İN MEKTUPLARI", w=1080, h=700, size=54, head_size=50, line_dt=0.6,
         scribbles=5, scribble_at=A("c9s3", "uzun", 0.0), scribbles_first=True,
         lines=[("Fethi anlatır,", A("c9s3", "fethi", -0.1)), ("ama kendini savunur.", A("c9s3", "kendini", -0.1))],
         hl=dict(line=1, text="ama kendini savunur.", at=A("c9s3", "savunan", -0.2)),
         caption="CARTAS DE RELACIÓN", label="cortes_mektup"),
    # s4a — Dürer + sergilenen Aztek eserleri
    shot("c9_durer", a=A("c9s4", -0.15), tr=("fade", 0.8), at_br=A("c9s4", "Brüksel", -0.1), at_az=A("c9s4", "Aztek", -0.2), at_ob=A("c9s4", "eserlerini", -0.3), at_ch=A("c9s4", "görüp", -0.1), label="durer_sergi"),
    # s4b — değerlerini yaklaşık yüz bin florin tahmin etti
    shot("wd_counter", a=A("c9s4", "değerlerini", -0.1), tr=("fade", 0.6), value=100000, prefix="≈ ", unit="FLORİN", at=A("c9s4", "yaklaşık", -0.05), dur=1.7, size=210,
         bg_icons=[dict(icon="sun_disc", x=W * 0.5, y=H * 0.5, size=760, at=0.0, metal="gold", alpha=0.10)],
         stamps=[("TAHMİN", W * 0.76, H * 0.27, A("c9s4", "tahmin", -0.1), 70, -0.12)], label="yuz_bin_florin"),
    # s5a — 1532, Cajamarca (İnka topraklarında)
    shot("map", a=A("c9s5", -0.15), tr=("fade", 0.8), cams=[(0.0, (-72, -5, 1.9)), (A("c9s5", "Cajamarca", 0.0), (-76.5, -7.6, 2.5))],
         regions=[dict(name="inka", color="#D08A2A", at=0.3, alpha=0.5)],
         labels=[dict(text="İNKA İMPARATORLUĞU", lon=-73.5, lat=-12.5, size=30, color="#F6E3B0", at=A("c9s5", "Cajamarca", 0.2), track=10)],
         cities=[dict(lon=-78.52, lat=-7.16, name="CAJAMARCA", kind="siege", at=A("c9s5", "Cajamarca", -0.1), side="r", size=32)],
         date=("1532", A("c9s5", 0.0)), label="cajamarca_harita"),
    # s5b — Pizarro, Atahualpa'yı esir aldı
    shot("wd_medals", a=A("c9s5", "Francisco", 0.1), tr=("fade", 0.5), size=520, y=H * 0.44,
         items=[dict(key="pizarro", name="FRANCISCO PIZARRO", role="Konkistador", metal="bronze", at=A("c9s5", "Francisco", -0.1)),
                dict(key="atahualpa", name="ATAHUALPA", role="İnka Hükümdarı", metal="bronze", flip=True, at=A("c9s5", "Atahualpa", -0.25))], label="pizarro_atahualpa"),
    # s6 — Fidye: bir oda dolusu altın, 1.326.539 peso (ransom_room — oda-lab)
    shot("theatre", a=A("c9s6", -0.2), tr=("fade", 0.8), scene="ransom_room", cams=[(0.0, (960, 540, 1.0)), (AE("c9s6", 0.0), (960, 575, 1.22))],
         p=dict(fill_t=(0.5, 5.6)), overlay=S9.ransom_overlay, label="fidye_odasi"),
    # s7 — idam (sakin: madalya altından kararır)
    shot("wd_medal_swap", a=A("c9s7", -0.2), tr=("dip", 0.8), key="atahualpa", metal_a="bronze", metal_b="onyx", swap_at=A("c9s7", "idam", -0.35), swap_dur=1.3,
         name="ATAHUALPA", role="İnka Hükümdarı", size=600, dark_at=A("c9s7", "edildi", -0.2), dark_dur=1.8, dark_to=0.75, label="idam_sessiz"),
    # s8 — kraliyetin payı beşte bir
    shot("c9_fifth", a=A("c9s8", -0.25), tr=("fade", 0.7), at_crown=A("c9s8", "Kraliyetin", -0.1), at_label=A("c9s8", "payı", -0.2), at_g=A("c9s8", "ganimetin", -0.1), at_one=A("c9s8", "beşte", -0.1), label="beste_bir"),
    # s9a — Yeni Yasalar 1542
    shot("wd_doc", a=A("c9s9", -0.2), tr=("fade", 0.8), tone="#C9B484", title="YENİ YASALAR  ·  1542", w=1100, h=400, size=56, head_size=52, line_dt=0.6,
         lines=[("Yerlileri köle yapmak yasaktır.", A("c9s9", "yerlileri", -0.1))],
         hl=dict(line=0, start="Yerlileri ", text="köle yapmak yasaktır.", at=A("c9s9", "köle", -0.15)),
         seal=True, seal_at=A("c9s9", "yasaktı", 0.2), label="yeni_yasalar"),
    # s9b — yerleşimciler öfkelendi; yasayı getiren Peru valisi öldürüldü
    shot("map", a=A("c9s9", "Yerleşimciler", -0.3), tr=("fade", 0.8), cams=[(0.0, (-37.17, 16.26, 0.383)), (AE("c9s9", 0.0), (-37.9, 15.8, 0.39))],
         regions=[dict(name="ispanya", color="ispanya", at=0.0, alpha=0.5), dict(name="peru_ispanya", color="ispanya", at=0.2, alpha=0.5)],
         labels=[dict(text="ATLANTİK OKYANUSU", lon=-13.5, lat=-8, size=28, color="#9FB8C8", at=0.4, track=12), dict(text="PERU", lon=-70.5, lat=-3.5, size=32, at=A("c9s9", "Yerleşimciler", 0.2), track=14)],
         routes=[dict(pts=[(-6.3, 37.2), (-30, 27), (-58, 14), (-79.5, 9), (-77.0, -12.0)], at=A("c9s9", "yasayı", -0.1), dur=2.3, color="#F0D27A", width=4, dash=(12, 10), arrow=False)],
         icons_=[dict(kind="torch", lon=-76.0, lat=-7.0, size=84, at=A("c9s9", "öfkelendi", -0.5), metal="crimson", bob=3, glow=0.3),
                 dict(kind="torch", lon=-72.0, lat=-10.5, size=84, at=A("c9s9", "öfkelendi", -0.3), metal="crimson", bob=3, glow=0.3),
                 dict(kind="torch", lon=-78.5, lat=-13.5, size=84, at=A("c9s9", "öfkelendi", -0.1), metal="crimson", bob=3, glow=0.3),
                 dict(kind=icn("flag", "shield"), route=[(-6.3, 37.2), (-30, 27), (-58, 14), (-79.5, 9), (-77.0, -12.0)], at=A("c9s9", "yasayı", -0.1), move_at=A("c9s9", "yasayı", -0.1), move_dur=2.3, size=90, metal="gold", bob=2, glow=0.25),
                 dict(kind="skull", lon=-77.0, lat=-12.0, size=96, at=A("c9s9", "öldürüldü", -0.05), metal="onyx", glow=0.0)],
         notes=[dict(text="YERLEŞİMCİLER", x=50, y=640, at=A("c9s9", "Yerleşimciler", 0.0), w=360, size=32),
                dict(text="PERU VALİSİ", x=50, y=740, at=A("c9s9", "valisi", -0.2), w=360, size=32)], label="peru_valisi"),
    # s10a — 1550, Valladolid; fetihler geçici olarak durdu
    shot("map", a=A("c9s10", -0.2), tr=("dip", 0.9), cams=[(0.0, (-3, 40.8, 2.3)), (AE("c9s10", -2.5), (-4.7, 41.6, 4.6))],
         regions=[dict(name="ispanya", color="ispanya", at=0.2, alpha=0.5)],
         cities=[dict(lon=-4.72, lat=41.65, name="VALLADOLID", kind="capital", at=A("c9s10", "Valladolid", -0.1), side="r", size=34)],
         notes=[dict(text="FETİHLER GEÇİCİ OLARAK DURDURULDU", x=120, y=190, at=A("c9s10", "durdurdu", -0.6, alt=("fetihleri",)), w=760, size=36)],
         date=("1550", A("c9s10", 0.0)), label="valladolid_1550"),
    # s10b — iki adam karşı karşıya: Sepúlveda ve Las Casas
    shot("wd_vs", a=A("c9s10", "iki", -0.35), tr=("fade", 0.8), size=500, gap=660, ring_at=A("c9s10", "iki", -0.2),
         left=dict(key="sepulveda", metal="silver", name="SEPÚLVEDA", at=A("c9s10", "Sepúlveda", -0.25)),
         right=dict(key="lascasas", metal="ivory", name="LAS CASAS", flip=True, at=A("c9s10", "Las", -0.25)),
         center=dict(icon="scales", at=A("c9s10", "karşı", -0.2), sway=True, size=170), label="sepulveda_lascasas"),
    # s11 — köleliğe layık / fetih bir suç; resmî kazanan yok (debate_hall — oda-lab)
    shot("theatre", a=A("c9s11", -0.2), tr=("fade", 0.8), scene="debate_hall", cams=[(0.0, (960, 540, 1.0)), (AE("c9s11", 0.0), (960, 585, 1.22))],
         p=dict(lecterns=2), overlay=S9.debate_overlay, label="tartisma"),
    # s12 — ilk dünya turu: Sanlúcar → Güney Amerika → Pasifik → Moluk → Ümit Burnu → Sanlúcar
    shot("map", a=A("c9s12", -0.2), tr=("fade", 0.9), cam=(0, -7, 0.165), compass=(1790, 930, 56), mountains=False,
         extra=S9.circum_extra(A("c9s12", "turu", -0.5), dur_a=2.2, dur_b=2.5, flag_at=A("c9s12", "bayrağı", -0.1)),
         date=("1519 – 1522", A("c9s12", "ilk", -0.1)), label="dunya_turu"),
    # s13a — Magellan yolda öldü
    shot("wd_medal_swap", a=A("c9s13", -0.2), tr=("fade", 0.8), key="magellan", metal_a="bronze", metal_b="onyx", swap_at=A("c9s13", "öldü", -0.35), swap_dur=1.0,
         name="MAGELLAN", role="Denizci", size=580, dark_at=A("c9s13", "öldü", 0.2), dark_dur=0.8, dark_to=0.35, label="magellan_oldu"),
    # s13b — tek gemi, Elcano, on sekiz Avrupalı
    shot("wd_counter", a=A("c9s13", "Eve", -0.25), tr=("fade", 0.8), value=18, unit="AVRUPALI SAĞ KALDI", size=250, pos=(W * 0.70, H * 0.60), at=A("c9s13", "on", -0.1), dur=1.2,
         medal_=dict(key="elkano", metal="bronze", x=W * 0.27, y=H * 0.57, size=500, at=A("c9s13", "Elcano", -0.2), name="ELCANO", role="Kaptan"),
         extra=S9.fleet_extra(A("c9s13", "Eve", -0.1), A("c9s13", "tek", -0.1), A("c9s13", "Elcano", -0.2), A("c9s13", "on", -0.1)), label="elcano_on_sekiz"),
    # s14 — arma: bir küre ve "Primus circumdedisti me"
    shot("c9_arma", a=A("c9s14", -0.25), tr=("fade", 1.0), at_karl=A("c9s14", "Şarlken", -0.1), at_elcano=A("c9s14", "ona", -0.15), at_arma=A("c9s14", "arma", -0.35), at_globe=A("c9s14", "küre", -0.25), at_motto=A("c9s14", "yazı", -0.2),
         words=[("PRIMUS", A("c9s14", "Primus", -0.05)), ("CIRCUMDEDISTI", A("c9s14", "circumdedisti", -0.05)), ("ME", A("c9s14", "me", -0.05))], at_tr=A("c9s14", "Beni", -0.1), label="arma_primus"),
]
