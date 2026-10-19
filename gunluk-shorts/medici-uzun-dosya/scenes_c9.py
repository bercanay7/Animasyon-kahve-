"""c9 — Defter Kapanıyor (1470 – 1494). PARÇA 4 KAPANIŞI (bölüm kartı Program'dan; bitiş ekranı SIRADAKİ PARÇA). Yönetmen kartı: yonetmen_c9.md.
Renk anahtarı: defter kremi + soğuk lapis/kurşun gri (banka solar) + kızıl damga (aforoz, el koyma) + son çekimlerde bronz altın (güzellik kaldı).
Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok). Mizah: kuruma/usule (aforoz ↔ ucuz Türk şapı, iki efendi, kaynaklar da uzlaşmıyor, kime sorduğunuza bağlı);
KAPALI: Lorenzo'nun ölümü, Portinari'nin kişisel çöküşü, 1494 el koyma/sürgün (V6).
"""
from shots import shot
import cilt_medici as CM
import p4_lib as L
import c8_kinds as K8
import c9_kinds as K
look = L.look

OUTRO_TR = ("candle", 1.2, dict(at=(1500, 720), at_b=(960, 700)))

SHOTS = [
    # ── 1. Lorenzo'nun parlayan Floransa'sı: Duomo yürüyüşünden bankacının masasına kayış ───────────────────────
    shot("p4_pano", ("c9s1", 0), pano="florence", tod="day", mode="day", perde=2, cam=("pan", "l", 2800),
         cams=[(("c9s1", 0), (8400, 10, 1.0)), (("c9s1", "parlarken,", 0.0), (6900, 20, 1.08)), (("c9s1", "defteri", -0.1), (5620, 60, 1.42))],
         label="Floransa parlıyor, kamera bankacının masasına kayar"),
    # ── 2. Defter sessizce incelir (yapraklar kalkıp toz olur) ────────────────────────────────────────────────────
    shot("c9_defter", ("c9s1", "defteri", -0.35), mode="day", perde=2, phase="thin", thin_at=("c9s1", "sessizce", -0.15), thin_dur=3.2, seed=5, cam=("push", 0.06),
         tr=("zoomthru", 0.8, dict(at=(960, 640), at_b=(960, 560))), link="scale", label="defter incelir"),
    # ── 3. Şap: taş tezgâhta kristaller büyür ──────────────────────────────────────────────────────────────────
    shot("c9_sap", ("c9s2", -0.3), mode="day", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.engr("ŞAP", 960, 190, ("c9s2", "şapa", -0.05), size=130, track=22, style="gilt", glow=0.2),
                  L.label("BOYAYI KUMAŞA TUTTURAN MİNERAL", 960, 880, ("c9s2", "boyayı", -0.1), size=34, track=10, out=("c9s2", "Floransa'nın", -0.1))),
         tr=("carry", 0.9, dict(strip="paper", dir="l")), link="carry", label="şap kristalleri"),
    # ── 4. Boyahaneler: boya bezleri (Floransa yünüyle bağ = çıkarım) ──────────────────────────────────────────────
    shot("p4_pano", ("c9s2", "Floransa'nın", -0.5), pano="florence", tod="day", mode="day", perde=2, cam=("pan", "r", 1050),
         cams=[(("c9s2", "Floransa'nın", -0.5), (1000, 10, 1.0)), (("c9s2", "ihtiyaç", 0.0), (1500, 20, 1.14)), (("c9s2", "mineral.", 0.3), (2050, 30, 1.2))],
         ovl=L.ov(L.tag("BOYAHANELER", 960, 190, ("c9s2", "boyahanelerinin", -0.2), size=36, w=560, sub="FLORANSA", out=("c9s3", 0.2))),
         tr=("yikama", 0.9), link="material", label="boyahaneler: bezler rüzgârda"),
    # ── 5. Batı'nın şapı Foça'dan; 1455'te Osmanlı'ya geçince yol kesilir; papalık Tolfa'da yatak bulur ───────────────
    shot("p4_map", ("c9s3", -0.25), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c9s3", -0.25), (24.6, 39.0, 4.3)), (("c9s3", "1455'te", 0.0), (23.4, 38.9, 4.6)), (("c9s3", "papalık", -0.2), (15.5, 40.8, 4.5)), (("c9s3", "Tolfa'da", 0.3), (12.9, 42.0, 7.0))],
         cities=[dict(lon=26.7519, lat=38.6692, name="FOÇA", kind="town", at=("c9s3", "Foça'dan", -0.35), size=34, side="b")],
         icons_=[dict(kind="ship", route=[(26.6, 38.7), (25.0, 37.2), (22.8, 36.0), (20.0, 36.8), (17.2, 38.4), (15.6, 38.1), (14.0, 39.6), (12.0, 41.2), (10.3, 43.5)], at=("c9s3", "Foça'dan", -0.2), move_at=("c9s3", "Foça'dan", -0.1), move_dur=2.9, size=84, metal="gold"),
                 dict(kind="pickaxe", lon=11.95, lat=42.12, size=84, at=("c9s3", "Tolfa'da", -0.1), metal="gold"), dict(kind="keys", lon=12.4964, lat=41.9028, size=76, at=("c9s3", "papalık", 0.0), metal="gold")],
         labels=[dict(text="TOLFA", lon=11.95, lat=42.25, size=34, track=14, at=("c9s3", "Tolfa'da", 0.0), color="#5A3E1E", face="title_m")],
         extra=L.mx(L.marrow([(26.6, 38.7), (25.0, 37.2), (22.8, 36.0), (20.0, 36.8), (17.2, 38.4), (15.6, 38.1), (14.0, 39.6), (12.0, 41.2), (10.3, 43.5)], ("c9s3", "Batı'nın", 0.0), dur=2.8, color="#3A6A9E", width=7.0, dash=(22, 14), out=("c9s3", "geçince", 0.1)),
                    L.mflag(26.7519, 38.6692, ("c9s3", "1455'te", 0.0), color="#B33620", emblem="crescent", h=110.0, w=64.0, out=None)),
         ovl=L.ov(L.date_plate("1455", ("c9s3", "1455'te", -0.1)), L.tag("OSMANLI", 1500, 330, ("c9s3", "Osmanlı'ya", -0.15), size=34, w=360, out=("c9s3", "papalık", 0.2))),
         tr=("iris", 0.9, dict(obj="seal", at=(960, 540), r=140)), link="shape", label="harita: Foça yolu kesilir, Tolfa"),
    # ── 6. 1466: pazarlama hakkı bir gruba (Piero de' Medici'nin de içinde olduğu) ──────────────────────────────────
    shot("c9_hak", ("c9s4", -0.4), mode="day", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.date_plate("1466", ("c9s4", "1466'da,", -0.1)),
                  L.tag("PIERO DE' MEDICI", 830, 880, ("c9s4", "Piero", -0.05), size=32, w=520, out=("c9s4", "gruba", 0.4)),
                  L.tag("BİR GRUP", 960, 160, ("c9s4", "gruba", -0.35), size=36, w=360)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="belge: dört mühür, biri Medici"),

    # ── 7. Papa aforozla tehdit eder; alıcılar yine de daha ucuz Türk şapına yönelir (mizah a: kurumun silahı ↔ fiyat) ───────────────
    shot("p4_map", ("c9s5", -0.25), mode="day", perde=2, cam=("push", 0.05), approx=False,
         cams=[(("c9s5", -0.25), (17.0, 40.7, 2.35)), (("c9s5", "ucuz", 0.0), (18.0, 40.3, 2.75))],
         icons_=[dict(kind="keys", lon=12.4964, lat=41.9028, size=110, at=("c9s5", "Papa,", -0.1), metal="gold"),
                 dict(kind="ship", route=[(26.6, 38.7), (25.0, 37.2), (22.8, 36.0), (20.0, 36.8), (17.2, 38.4), (15.6, 38.1), (14.0, 39.6), (12.0, 41.2), (10.3, 43.5)], at=("c9s5", "alıcılar", -0.4), move_at=("c9s5", "alıcılar", -0.3), move_dur=3.4, size=92, metal="gold")],
         extra=L.mx(L.marrow([(26.6, 38.7), (25.0, 37.2), (22.8, 36.0), (20.0, 36.8), (17.2, 38.4), (15.6, 38.1), (14.0, 39.6), (12.0, 41.2), (10.3, 43.5)], ("c9s5", "Türk", -0.1), dur=1.8, color="#A8321E", width=9.0, label="TÜRK ŞAPI")),
         ovl=L.ov(L.stamp("AFOROZ", 960, 430, ("c9s5", "aforozla", -0.1), size=96, rot=-0.10, out=("c9s5", "alıcılar", 0.6)),
                  L.tag("DAHA UCUZ", 1300, 810, ("c9s5", "ucuz", -0.15), size=38, w=400)),
         tr=("iris", 0.9, dict(obj="seal", at=(830, 758), r=62)), link="shape", label="aforoz damgası, altından gemi geçer"),
    # ── 8. Şaptan ne kazandığını bilmiyoruz; 1475'te şapta zarar yazılıyordu diye aktarılır ─────────────────────────────────────────
    shot("p4_ledger", ("c9s6", -0.3), mode="day", perde=2, cam=("push", 0.07), head="ŞAP", title_l="KAZANÇ", title_r="1475", seed=9,
         left=[dict(text="ŞAP · KAZANÇ", amt="?", at=("c9s6", "kazandığını", -0.1), dur=1.2)],
         right=[dict(text="ŞAP · 1475", amt="ZARAR", at=("c9s6", "1475'te", 0.0), hl=("c9s6", "zarar", -0.1), dur=1.6)],
         ovl=L.ov(K8.icon_pop("question", 700, 600, ("c9s6", "bilmiyoruz;", -0.4), out=("c9s6", "yalnız,", 0.2), size=170),
                  L.stamp("○ AKTARILIR", 1350, 640, ("c9s6", "aktarılır.", -0.7), size=46, rot=-0.07)),
         tr=("sayfa", 0.9), link="material", label="defter: kazanç ?, 1475 zarar"),
    # ── 9. Brugge'de yardımcı Portinari; Cosimo güvenmezdi ───────────────────────────────────────────────────────────────────────
    shot("p4_oda", ("c9s7", -0.25), room="banka", path="sweep_r", mode="day", perde=2, cam=("push", 0.06),
         ovl=L.ov(L.tag("BRUGGE", 480, 190, ("c9s7", "Brugge'de", -0.1), size=36, w=420, out=("c9s7", "anlatılır;", 0.4)),
                  L.tag("TOMMASO PORTINARI", 1380, 240, ("c9s7", "Tommaso", -0.1), size=34, w=640, sub="YARDIMCI", out=("c9s7", "anlatılır;", 0.4))),
         tr=("zoomthru", 0.9, dict(at=(700, 520), at_b=(960, 560))), link="scale", label="Brugge şubesi, yardımcı Portinari"),
    # ── 10. Cosimo ölünce (mum söner) Portinari müdür ve ortak ────────────────────────────────────────────────────────────────
    shot("c9_iki", ("c9s7", "ama", -0.35), phase="devir", mode="night", perde=2, cam=[(("c9s7", "ama", -0.35), look(960, 540, 1.0)), (("c9s7", "ortağı", 0.0), look(1130, 540, 1.12))],
         ovl=L.ov(L.tag("MÜDÜR", 1170, 800, ("c9s7", "müdürü", -0.15), size=36, w=300), L.tag("ORTAK", 1590, 800, ("c9s7", "ortağı", -0.15), size=36, w=300)),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Cosimo'nun mumu söner, Portinari parlar"),
    # ── 11. Portinari, Cesur Şarl'a büyük teminatsız krediler verdi; borç geri ödenmedi ───────────────────────────────────────────────
    shot("c9_iki", ("c9s8", -0.15), phase="kredi", mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.stamp("TEMİNATSIZ", 700, 900, ("c9s8", "teminatsız", -0.1), size=60, rot=-0.06, out=("c9s8", "geri", -0.3)),
                  L.stamp("GERİ ÖDENMEDİ", 1220, 900, ("c9s8", "ödenmedi.", -0.35), size=56, rot=-0.06)),
         tr=("carry", 0.9, dict(strip="ribbon", dir="r")), link="carry", label="sikkeler Portinari'den dükün yanına akar"),
    # ── 12. Hem Medici'nin müdürü hem dükün danışmanı: iki efendi (mizah b; palle ve taç iplerle çeker) ────────────────────────────
    shot("p4_medal", ("c9s9", -0.2), key="m_portinari", metal="bronze", name="TOMMASO PORTINARI", role="stilize profil", cam=("orbit", 12), mode="night", perde=2,
         ovl=L.ov(K.marionet(("c9s9", "Medici'nin", -0.3), ("c9s9", "dükün", -0.3), ("c9s9", "iki", -0.2)),
                  L.tag("MEDİCİ'NİN MÜDÜRÜ", 340, 330, ("c9s9", "müdürüydü", -0.2), size=30, w=520), L.tag("DÜKÜN DANIŞMANI", 1580, 330, ("c9s9", "danışmanı:", -0.3), size=30, w=520),
                  L.stamp("İKİ EFENDİ", 1560, 700, ("c9s9", "efendiye", -0.2), size=62, rot=-0.05)),
         tr=("zoomthru", 0.8, dict(at=(540, 470), at_b=(960, 470), depth=3.0)), link="scale", label="marionet: palle ve taç çeker"),
    # ── 13. Medici Brugge'yi tasfiyeye karar verdi; şube 1480 ya da 1481'de kapandı ─────────────────────────────────────────────────
    shot("p4_map", ("c9s10", -0.25), mode="day", perde=2, cam=("push", 0.05), approx=False, style="lapis",
         cams=[(("c9s10", -0.25), (4.6, 50.6, 7.5)), (("c9s10", "üstlenmeye", 0.0), (3.9, 51.0, 9.0)), (("c9s10", "kapandı.", 0.0), (3.4, 51.15, 10.5))],
         cities=[dict(lon=3.2247, lat=51.2093, name="BRUGGE", kind="town", at=("c9s10", "Brugge'yi", -0.3), size=36, side="r", color="#FFD27A")],
         extra=L.mx(L.mglow(3.2247, 51.2093, ("c9s10", "Medici", 0.0), out=("c9s10", "kapandı.", 0.1), r=36.0),
                    L.mflag(3.2247, 51.2093, ("c9s10", "Medici", 0.1), color="#8A2018", emblem="palle", h=100.0, w=60.0, out=("c9s10", "üstlenmeye", 0.1), flip=True),
                    L.mflag(3.2247, 51.2093, ("c9s10", "üstlenmeye", 0.2), color="#2F5A8A", emblem="plain", h=100.0, w=60.0, flip=True)),
         ovl=L.ov(L.date_plate("1480 YA DA 1481", ("c9s10", "1480", -0.1)), L.dim(("c9s10", "kapandı.", 0.3), alpha=0.35, dur=1.5),
                  L.tag("PORTINARI ÜSTLENİR", 1500, 250, ("c9s10", "Portinari'yi", -0.1), size=32, w=600, out=("c9s10", "kapandı.", 0.4))),
         tr=("carry", 0.9, dict(strip="ink", dir="l")), link="carry", label="harita: Brugge bayrak değişir, ışık söner"),
    # ── 14. Londra şubesi 1466–1471 arası Kral IV. Edward'a toplam 26.000 sterlinden fazla kredi (£10.500 YOK) ──────────────────────
    shot("c9_londra", ("c9s11", -0.25), mode="night", perde=2, cam=[(("c9s11", -0.25), look(960, 540, 1.0)), (("c9s11", "yirmi", 0.0), look(1000, 560, 1.05)), (("c9s11", "verdi.", 0.0), look(960, 560, 1.12))],
         ovl=L.ov(L.stamp("○ TOPLAM KREDİ", 1640, 880, ("c9s11", "fazla", -0.2), size=42, rot=-0.06)),
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="Londra: krediler krala akar, sayaç 26.000+"),
    # ── 15. Kısmen ödendi; Güller Savaşı suçlanır; rakamlar kaynaktan kaynağa değişir (mizah a) ──────────────────────────────────────
    shot("c9_gul", ("c9s12", -0.2), mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.engr("GÜLLER SAVAŞI", 1300, 230, ("c9s12", "Güller", -0.1), size=60, track=14, style="engraved", color="#5A1A10", out=("c9s12", "rakamlar", 0.2)),
                  L.stamp("RAKAMLAR DEĞİŞİR", 1305, 900, ("c9s12", "değişir.", -0.6), size=44, rot=-0.05)),
         tr=("carry", 0.9, dict(strip="ribbon", dir="l")), link="carry", label="geri ödenen sikkeler, güller, ≠ kaynaklar"),
    # ── 16. Londra şubesi 1477–1478 arasında tasfiye edildi (mum söner; 51.533 FL zarar kartı ○) ──────────────────────────────────────
    shot("c9_zaman", ("c9s13", -0.25), mode="night", perde=2, cam=("push", 0.05), axis=(1475, 1480), ticks=1, y0=360.0, x0=500.0, x1=1560.0,
         bars=[dict(name="LONDRA", a=1477, b=1478, at=("c9s13", "1477", -0.15), dur=1.5, label="1477–78")],
         ovl=L.ov(L.count_up(960, 720, ("c9s13", "1478", 0.1), 51533, dur=1.4, unit="LONDRA ZARARI", size=120, suffix=" FL"), L.stamp("○ TEK KAYNAK", 1500, 860, ("c9s13", "edildi.", -0.3), size=40, rot=-0.07)),
         tr=("sayfa", 0.9), link="material", label="Londra çubuğu biter, lamba söner, zarar kartı"),
    # ── 17. Milano, Avignon, Brugge, Venedik: şubeler tek tek kapandı (kandiller söner, defterler kapanır) ───────────────────────────
    shot("p4_oda", ("c9s14", -0.25), room="banka", path="close", close_at=("c9s14", "Milano,", 0.05), close_dur=7.4, mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.tag("MİLANO", 400, 190, ("c9s14", "Milano,", -0.1), size=32, w=300, out=("c9s14", "Avignon,", 0.2)),
                  L.tag("AVİNYON", 760, 190, ("c9s14", "Avignon,", -0.1), size=32, w=300, out=("c9s14", "Brugge,", 0.2)),
                  L.tag("BRUGGE", 1120, 190, ("c9s14", "Brugge,", -0.1), size=32, w=300, out=("c9s14", "Venedik:", 0.2)),
                  L.tag("VENEDİK", 1480, 190, ("c9s14", "Venedik:", -0.1), size=32, w=300, out=("c9s14", "şubeler", 0.6))),
         tr=("candle", 1.0, dict(at=(1000, 470), at_b=(960, 600))), link="light", label="KAPANIŞ: kandiller tek tek söner"),

    # ── 18. Suçlu kimdi? (çark hızla döner; kapanmış banka karanlığından ışıkla açılır) ───────────────────────────────────────────────
    shot("c9_cark", ("c9s14", "kapandı.", 0.2), phase="spin", mode="night", perde=2, cam=("push", 0.05),
         tr=("light", 0.9, dict(at=(960, 480))), link="light", label="suçlama çarkı döner (Suçlu kimdi?)"),
    # ── 19. Medici siparişiyle tarih yazan Machiavelli (kütüphane; palle mührü) ───────────────────────────────────────────────────────────
    shot("p4_oda", ("c9s16", -0.3), room="calisma", variant="kutuphane", figure="desk", path="scribe", mode="day", perde=2, cam=("push", 0.06),
         ovl=L.ov(L.tag("MACHIAVELLI", 480, 190, ("c9s16", "yazan", -0.1), size=36, w=500, sub="TARİHÇİ", out=("c9s16", "atar:", 0.3)),
                  K.seal_pop(1450, 330, ("c9s16", "siparişiyle", 0.0), r=58, out=("c9s16", "atar:", 0.3)),
                  L.tag("MEDİCİ SİPARİŞİYLE", 1450, 230, ("c9s16", "siparişiyle", 0.1), size=30, w=520, out=("c9s16", "atar:", 0.3))),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Machiavelli yazar (Medici siparişi)"),
    # ── 20. Suçu ajanlara atar (çark AJANLAR'da durur) ──────────────────────────────────────────────────────────────────────────────────
    shot("c9_cark", ("c9s16", "ajanlara", 0.0), phase="land", land_at=("c9s16", "atar:", 0.45), agents_at=("c9s16", "ajanlarının", -0.2), mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.tag("MACHIAVELLI'YE GÖRE", 360, 300, ("c9s16", "Lorenzo", -0.2), size=30, w=560, sub="AJANLARIN UYGUNSUZ DAVRANIŞLARI", out=("c9s16", "yüzünden.", 0.8))),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="çark AJANLAR'da durur"),
    # ── 21. Sassetti 1463'ten 1490'daki ölümüne dek ≈30 yıl genel müdür ──────────────────────────────────────────────────────────────────
    shot("p4_timeline", ("c9s17", -0.3), mode="day", perde=2, a0=1460, a1=1500, step=10, title="GENEL MÜDÜR", at=("c9s17", -0.2), y=560.0,
         hl=(1463, 1490, "≈ 30 YIL", ("c9s17", "yaklaşık", -0.2)),
         events=[(1463, "SASSETTİ", ("c9s17", "1463'ten", 0.0)), (1490, "ÖLÜMÜ", ("c9s17", "ölümüne", -0.25))], cam=("push", 0.05),
         tr=("iris", 0.9, dict(obj="florin", at=(960, 480), r=74)), link="shape", label="Sassetti: ≈30 yıl genel müdür"),
    # ── 22. Treccani: «verimsiz bir mali örgütlenme» ─────────────────────────────────────────────────────────────────────────────────────
    shot("p4_quote", ("c9s17", "İtalyan", -0.5), text="verimsiz bir mali örgütlenme", who="TRECCANI", src="İTALYAN ANSİKLOPEDİSİ", at=2.0, size=88, mode="day", perde=2, cam=("push", 0.06),
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="Treccani tanımı"),
    # ── 23. de Roover: parlak devlet adamı, iş adamı değil ───────────────────────────────────────────────────────────────────────────────
    shot("p4_medal", ("c9s18", -0.3), key="m_lorenzo", metal="bronze", name="LORENZO", role="stilize profil", pos="l", size=620, cam=("orbit", 10), mode="day", perde=2,
         ovl=L.ov(L.tag("RAYMOND DE ROOVER'A GÖRE", 1540, 120, ("c9s18", "Raymond", -0.2), size=30, w=640),
                  K.icon_at("crown", 1470, 290, ("c9s18", "devlet", -0.25), size=190), K.check_cross(1690, 290, ("c9s18", "adamıydı,", -0.15), ok=True),
                  K.icon_at("coinbag", 1470, 760, ("c9s18", "iş", -0.2), size=190), K.check_cross(1690, 760, ("c9s18", "değil;", -0.4), ok=False),
                  L.stamp("○ YAKLAŞIK ÖZET", 1540, 900, ("c9s18", "değil;", -0.1), size=38, rot=-0.06)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="de Roover: devlet adamı ✓, iş adamı ✗"),
    # ── 24. Goldthwaite: 1500 öncesi genel banka krizi görmez ─────────────────────────────────────────────────────────────────────────────
    shot("c9_kriz", ("c9s18", "Goldthwaite", -0.35), mode="day", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.tag("GOLDTHWAITE", 960, 170, ("c9s18", "Goldthwaite", -0.2), size=34, w=420),
                  L.stamp("GENEL KRİZ YOK", 960, 860, ("c9s18", "görmez.", -0.45), size=66, rot=-0.05),
                  L.stamp("○ YAKLAŞIK ÖZET", 1520, 190, ("c9s18", "banka", -0.2), size=34, rot=-0.06)),
         tr=("zoomthru", 0.9, dict(at=(1230, 690), at_b=(960, 470))), link="scale", label="Goldthwaite: sakin çizgi, kriz yok"),
    # ── 25. Yani bankayı kimin batırdığı, kime sorduğunuza bağlı (mizah c: çark oturmaz) ────────────────────────────────────────────────────
    shot("c9_cark", ("c9s19", -0.3), phase="spin2", mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.stamp("YORUM", 1560, 270, ("c9s19", "bağlı.", -0.25), size=48, rot=-0.07)),
         tr=("carry", 0.9, dict(strip="ink", dir="l")), link="carry", label="çark oturmaz: kime sorduğunuza bağlı"),
    # ── 26. Sassetti Santa Trinita'da Ghirlandaio'ya kendi şapelini yaptırıyordu (giornata; ironi) ─────────────────────────────────────────
    shot("c9_sapel", ("c9s20", -0.3), mode="day", perde=2, cam=[(("c9s20", -0.3), look(960, 540, 1.0)), (("c9s20", "Ghirlandaio'ya", 0.0), look(1000, 560, 1.12)), (("c9s21", -0.4), look(1080, 600, 1.2))],
         ovl=L.ov(L.tag("SASSETTİ", 330, 190, ("c9s20", "Sassetti", -0.15), size=34, w=380, out=("c9s20", "1480'lerde", 0.4)),
                  L.date_plate("1480'LER", ("c9s20", "1480'lerde", -0.1)),
                  L.tag("SANTA TRINITA", 1540, 190, ("c9s20", "Trinita'da", -0.2), size=34, w=500),
                  L.tag("GHIRLANDAIO", 1540, 290, ("c9s20", "Ghirlandaio'ya", -0.15), size=34, w=460)),
         tr=("light", 0.9, dict(at=(1000, 300))), link="light", label="şapel: giornata, ironi (defter incelirken)"),
    # ── 27. Kasım 1494: Lorenzo'nun oğlu Piero kaçtı; Signoria Medici'yi sürgün etti (siluet; mizah KAPALI) ─────────────────────────────────
    shot("p4_sehir", ("c9s21", -0.3), scene="sokak", tod="dusk", mode="night", perde=2, cam=("pan", "l", 1100),
         cams=[(("c9s21", -0.3), (3500, 40, 1.0)), (("c9s21", "kaçtı;", 0.0), (2900, 40, 1.05)), (("c9s22", -0.4), (2300, 44, 1.12))],
         actors=[dict(kind="soylu", x0=3560, y=818, h=300, dir=-1, speed=330, action="walk", seed=8, cf="#14101A"), dict(kind="halk", x0=3760, y=822, h=280, dir=-1, speed=320, action="walk", seed=19, cf="#14101A", phase=0.4)],
         ovl=L.ov(L.date_plate("KASIM 1494", ("c9s21", "Kasım", -0.1)), L.stamp("SÜRGÜN", 1400, 380, ("c9s21", "sürgün", -0.1), size=86, rot=-0.08)),
         tr=("candle", 1.0, dict(at=(1784, 826), at_b=(1500, 600))), link="light", label="Piero kaçar (siluet), sürgün"),
    # ── 28. Cumhuriyet Palazzo Medici'ye ve öteki konutlara resmen el koydu (mühür bandı) ────────────────────────────────────────────────────
    shot("c9_saray", ("c9s22", -0.3), phase="el", mode="night", perde=2,
         cam=[(("c9s22", -0.3), look(960, 540, 1.0)), (("c9s22", "koydu;", 0.0), look(700, 640, 1.30))],
         ovl=L.ov(L.tag("CUMHURİYET", 1230, 150, ("c9s22", "Cumhuriyet", -0.1), size=34, w=420, out=("c9s22", "resmen", 0.4)),
                  L.tag("PALAZZO MEDİCİ", 800, 150, ("c9s22", "Palazzo", -0.1), size=34, w=520, out=("c9s22", "resmen", 0.4)),
                  L.stamp("EL KONDU", 1100, 560, ("c9s22", "resmen", -0.15), size=110, rot=-0.10)),
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="Palazzo Medici: mühür bandı, EL KONDU"),
    # ── 29. Donatello'nun David'i ve Judith'i Palazzo Vecchio'ya taşındı (araba şehirden geçer) ────────────────────────────────────────────────
    shot("c9_saray", ("c9s22", "Donatello'nun", -0.2), phase="tas", mode="night", perde=2,
         cam=[(("c9s22", "Donatello'nun", -0.2), look(640, 590, 1.0)), (("c9s22", "Judith'i", 0.0), look(1560, 590, 1.0)), (("c9s22", "taşındı.", 0.3), look(2200, 560, 1.08))],
         ovl=L.ov(L.tag("DONATELLO", 960, 140, ("c9s22", "Donatello'nun", -0.2), size=34, w=420, out=("c9s22", "Vecchio'ya", -0.4)),
                  L.tag("DAVID", 780, 260, ("c9s22", "David'i", -0.15), size=30, w=300, out=("c9s22", "Vecchio'ya", -0.4)), L.tag("JUDITH", 1140, 260, ("c9s22", "Judith'i", -0.15), size=30, w=300, out=("c9s22", "Vecchio'ya", -0.4)),
                  L.tag("PALAZZO VECCHIO", 1460, 170, ("c9s22", "Vecchio'ya", -0.1), size=34, w=560)),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="bronzlar Palazzo Vecchio'ya taşınır"),
    # ── 30. Kalabalık bahçelere daldı; saray kısmen yağmalandı, resmen el kondu (kesit: alt kat kalabalık, üst kat ışıklı ve boş) ────────────
    shot("c9_kesit", ("c9s23", -0.3), mode="night", perde=2, cam=[(("c9s23", -0.3), look(960, 560, 1.0)), (("c9s23", "kondu.", 0.2), look(1180, 620, 1.18))],
         ovl=L.ov(L.stamp("RESMEN EL KONDU", 960, 150, ("c9s23", "resmen", -0.15), size=80, rot=-0.06)),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="kesit: alt kat kalabalık, üst kat ışıklı ve boş"),
    # ── 31. Bankanın bütün mülkü, Floransa'daki masası dahil, kayyumlara verildi (KAYYUM mührü, 15.445 FL ○) ─────────────────────────────────
    shot("p4_oda", ("c9s24", -0.4), room="banka", path="default", mode="night", perde=2, cam=("pull", 0.06),
         ovl=L.ov(L.stamp("KAYYUM", 960, 470, ("c9s24", "kayyumlara", -0.1), size=130, rot=-0.08),
                  L.count_up(1440, 700, ("c9s24", "masası", -0.2), 15445, dur=1.3, unit="ALACAK", size=96, suffix=" FL"),
                  L.stamp("○ TEK KAYNAK", 1440, 880, ("c9s24", "verildi.", -0.3), size=36, rot=-0.06)),
         tr=("zoomthru", 0.9, dict(at=(1000, 700), at_b=(960, 560))), link="scale", label="bankanın masası kayyumlara"),
    # ── 32. Resmî son 1494; fiilî çözülme 1470'lerden beri şube şube sürdü (aralık çubukları) ─────────────────────────────────────────────────
    shot("c9_zaman", ("c9s25", -0.35), mode="night", perde=2, cam=("push", 0.05), axis=(1470, 1496), ticks=5, y0=330.0, x0=520.0, x1=1800.0,
         shade=dict(a=1470, b=1494, at=("c9s25", "fiilî", -0.25), label="FİİLÎ ÇÖZÜLME"),
         marks=[dict(year=1494, text="RESMÎ SON", at=("c9s25", "Resmî", 0.0), up=True)],
         bars=[dict(name="LONDRA", a=1477, b=1478, at=("c9s25", "çözülme", 0.0), dur=0.9), dict(name="MİLANO", a=1478, b=1479, at=("c9s25", "1470'lerden", 0.0), dur=0.9),
               dict(name="AVİNYON", a=1479, b=1480, at=("c9s25", "1470'lerden", 0.5), dur=0.9), dict(name="BRUGGE", a=1480, b=1481, at=("c9s25", "beri", -0.3), dur=0.9),
               dict(name="VENEDİK", a=1481, b=1481, at=("c9s25", "şube", -0.1), dur=0.6)],
         ovl=L.ov(L.stamp("○ ARALIKLAR YAKLAŞIK", 1400, 920, ("c9s25", "sürüyordu.", -0.5), size=32, rot=-0.05)),
         tr=("sayfa", 0.9), link="material", label="aralık çubukları: resmî son 1494, fiilî çözülme"),
    # ── 33. Banka sona ermişti; ama Donatello'nun bronzları Palazzo Vecchio'ya taşındı (soğuk karanlık → altın ışık) ──────────────────────────
    shot("c9_saray", ("c9s26", -0.3), phase="vecchio", mode="night", perde=2, cam=[(("c9s26", -0.3), look(960, 560, 1.0)), (("c9s26", "taşındı.", 0.0), look(960, 520, 1.16))],
         ovl=L.ov(L.tag("DONATELLO", 690, 190, ("c9s26", "Donatello'nun", -0.1), size=32, w=360), L.tag("PALAZZO VECCHIO", 1230, 190, ("c9s26", "Palazzo", -0.1), size=32, w=520)),
         tr=("light", 1.0, dict(at=(960, 300), col="#FFD27A", rays=True)), link="light", label="bronzlar altın ışıkta (güzellik kaldı)"),
    # ── 34. Banka öldü, güzellik kaldı (defter kapanır, mum söner; kapak altın parlar) ──────────────────────────────────────────────────────────
    shot("c9_defter", ("c9s27", -0.5), phase="close", close_at=("c9s27", "öldü,", -0.2), snuff_at=("c9s27", "öldü,", 0.15), mode="night", perde=2, cam=("push", 0.05),
         ovl=L.ov(L.glint(960, 535, ("c9s27", "kaldı.", -0.25), r=300, dur=1.4)),
         tr=("dip", 0.8), link="light", label="defter kapanır (banka öldü)"),
    # ── 35. KAPI: Peki o güne nasıl gelindi? Bir kralın Alpler'i aşmasıyla, bir rahibin vaazlarıyla ─────────────────────────────────────────────────
    shot("p4_map", ("c9s28", -0.25), mode="day", perde=2, style="lapis", cam=("push", 0.05), approx=False, frame=True,
         cams=[(("c9s28", -0.25), (10.2, 44.4, 3.2)), (("c9s28", "kralın", 0.0), (8.6, 45.0, 3.8)), (("c9s28", "rahibin", -0.2), (10.6, 44.2, 4.3))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c9s28", "Medici'yi", -0.2), size=32, side="b", color="#FFD27A")],
         icons_=[dict(kind="mountain", lon=7.4, lat=45.7, size=120, at=("c9s28", "Alpler'i", -0.4), metal="silver"), dict(kind="mountain", lon=9.0, lat=46.3, size=100, at=("c9s28", "Alpler'i", -0.2), metal="silver"),
                 dict(kind="monk", lon=11.2558, lat=43.62, size=108, at=("c9s28", "rahibin", -0.15), metal="gold"),
                 dict(kind="crown", route=[(5.8, 45.2), (6.7, 44.95), (7.7, 45.0), (8.9, 44.7), (10.2, 44.1), (11.1, 43.85)], at=("c9s28", "kralın", -0.1), move_at=("c9s28", "kralın", -0.05), move_dur=2.5, size=132, metal="gold")],
         extra=L.mx(L.mglow(11.2558, 43.7696, ("c9s28", "Medici'yi", -0.2), r=30.0), L.mflag(11.2558, 43.7696, ("c9s28", "Medici'yi", -0.1), color="#8A2018", emblem="palle", h=96.0, w=58.0, out=("c9s28", "sürgüne", 0.3)),
                    L.marrow([(11.2558, 43.9), (10.2, 44.4), (9.0, 44.9)], ("c9s28", "sürgüne", 0.0), dur=1.2, color="#C95A40", width=7.0, dash=(18, 12)),
                    
                    L.mimpact(11.2558, 43.77, ("c9s28", "vaazlarıyla.", -0.9), dur=2.2, color="#E8B060", n=4)),
         ovl=L.ov(L.date_plate("KASIM 1494", ("c9s28", "Medici'yi", -0.2), out=("c9s28", "kralın", 0.0)), L.dim(("c9s28", "vaazlarıyla.", 0.3), alpha=0.42, dur=1.2)),
         tr=("iris", 1.0, dict(obj="palle", at=(960, 535), r=130)), link="shape", label="KAPI: kral Alpler'i aşar, rahip vaaz verir"),
]
YIL_AT = [(("c9s1", 0), 1470), (("c9s6", "1475'te", -0.1), 1475), (("c9s13", "1478", -0.1), 1478), (("c9s14", "1481'e", -0.1), 1481), (("c9s21", "1494'te", -0.1), 1494)]
