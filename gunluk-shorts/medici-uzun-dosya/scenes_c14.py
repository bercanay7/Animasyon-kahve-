"""c14 — Yıldızlar, Notalar, Taşlar (1584–1737). PARÇA 7 AÇILIŞI (bölüm kartsız; Program ilk çekime «MEDİCİ — PARÇA VII — YILDIZLAR VE HESAP» bindirmesi ekler:
ilk çekimin orta bandı boş). Yönetmen kartı: yonetmen_c14.md · notlar: notlar_c14.md. Tüm çekimler cümle/sözcük çapalı (mutlak saniye yok).
Renk anahtarı: parlak umber/şeftali sıva + altın (MİRAS günbatımı) · Galileo'da lapis-gece · 1633'te ağır kızıl-kahve karanlık, tek ışık · piyanoda ahşap + fildişi.
Bölümün ipi (YORUM): Medici icatçı değil, ev sahibidir: SAHNE · MAAŞ · ENVANTER (köşe sayacı; s24'te «İCAT» ✕).
İmza sekans: «MERCEK» (c14s11–c14s17): baba lavtası ↔ teleskop → iris(mercek) → Jüpiter/uydular → defter → iki seçenek → kapak → paket → rota → uydu adları (etiketler düşer).
Mizah: Bandini soyadı (s4), Caccini'nin altı hafta önceki notası (s10), yıldızlar aileye zimmetlendi/etiketler düşer (s17), envanterde «yeni icat» + «piano ↔ FORTE» (s21–s22).
KAPALI/ağır: 1633 (s18–s19): süssüz, karanlık, tek ışık; geçişler candle/dip.
"""
from shots import shot
import cilt_medici as CM
import p7_lib as L
import c14_kinds as K
look = L.look
ov = L.ov

# ── tekrar kullanılan yerleşimler ──
ROMA = dict(lon=12.4964, lat=41.9028)
IST = dict(lon=28.98, lat=41.01)
PAD = (11.8767, 45.4064)
FLO = (11.2558, 43.7696)

SAHNE = ("SAHNE", ("c14s7", "sahnelendi.", -0.3), "ok")
ENVANTER = ("ENVANTER", ("c14s21", "envanterinde", 0.0), "ok")

SHOTS = [
    # ── 1. Roma haritası: Floransa değil, Roma (orta bant ilk 4,8 sn boş: pimler alt-sağda) ───────────
    shot("p7_map", ("c14s1", 0), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c14s1", 0), (8.3, 43.4, 4.0)), (("c14s1", "Büyük", -0.3), (8.3, 43.4, 4.05)), (("c14s1", "Kardinal", -0.5), (12.3, 42.6, 6.0)), (("c14s1", "bir", 0.0), (12.4, 42.3, 6.8))],
         cities=[dict(lon=ROMA["lon"], lat=ROMA["lat"], name="ROMA", kind="capital", at=("c14s1", "Roma'da,", -0.1), size=42, side="r"),
                 dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c14s1", "Büyük", -0.2), size=34, side="l")],
         icons_=[dict(kind="keys", lon=12.43, lat=41.97, size=100, at=("c14s1", "Papa", -0.1), metal="gold")],
         extra=L.mx(L.mtag(ROMA["lon"], ROMA["lat"], "PAPA XIII. GREGORIUS", ("c14s1", "desteğiyle", 0.85), dx=-390, dy=-130, size=32),
                    L.mtag(ROMA["lon"], ROMA["lat"], "KARDİNAL FERDINANDO", ("c14s1", "Kardinal", -0.1), dx=-400, dy=60, size=32, sub="BÜYÜK DÜK COSIMO'NUN OĞLU"),
                    L.mimpact(ROMA["lon"], ROMA["lat"], ("c14s1", "Roma'da,", 0.0), color="#B33620", n=2)),
         label="Roma, 1584: Papa ve Kardinal Ferdinando"),
    # ── 2. Matbaa atölyesi (geniş): Medici Doğu Dilleri Matbaası kuruldu ───────────────────────────
    shot("c14_baski", ("c14s1", "bir", -0.15), mode="day", seed=3, thumps=[], books=[],
         cam=[(("c14s1", "bir", -0.15), look(960, 540, 1.0)), (("c14s2", -0.1), look(1150, 520, 1.16))],
         ovl=ov(L.tag("MEDİCİ DOĞU DİLLERİ MATBAASI", 960, 150, ("c14s1", "Medici", -0.1), size=36, w=1040, out=("c14s2", 0.2))),
         tr=("zoomthru", 0.9, dict(at=(981, 657), at_b=(1150, 520))), link="scale", label="atölye: pres, dizgi dolabı, kurutma ipi"),
    # ── 3. Granjon punç keser; dizgi sağdan sola ────────────────────────────────────────────────────
    shot("c14_harf", ("c14s2", -0.1), mode="day", cut_at=("c14s2", 0.0), cut_dur=1.25, set_at=("c14s2", "Arapça", 1, -0.4), set_dt=0.16, n=8,
         cam=[(("c14s2", -0.1), look(700, 540, 1.45)), (("c14s2", "Granjon", 0.0), look(780, 520, 1.28)), (("c14s2", "kesti;", 0.1), look(1250, 560, 1.1)),
              (("c14s2", "Arapça", 1, -0.9), look(2150, 560, 1.05)), (("c14s2", "İncil,", 0.0), look(2380, 540, 1.22))],
         ovl=ov(L.tag("ROBERT GRANJON", 1480, 230, ("c14s2", "Robert", -0.1), size=38, out=("c14s2", "Arapça", 1, -0.5))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="punç oyma; harfler sağdan sola dizilir"),
    # ── 4. Pres: her sözcükte bir baskı, her baskıda bir kitap ─────────────────────────────────────
    shot("c14_baski", ("c14s2", "İncil,", -0.5), mode="day", seed=3,
         thumps=[("c14s2", "İncil,", -0.25), ("c14s2", "Kanun'u", -0.3), ("c14s2", "Öklid", -0.25), ("c14s2", "basıldı.", -0.2)],
         books=[dict(at=("c14s2", "İncil,", 0.15), col="#8A2E1E"), dict(at=("c14s2", "Kanun'u", 0.1), col="#233C8C"), dict(at=("c14s2", "Öklid", 0.15), col="#2E6A46")],
         cam=[(("c14s2", "İncil,", -0.5), look(1220, 540, 1.0)), (("c14s3", -0.1), look(1340, 520, 1.1))],
         ovl=ov(L.tag("ARAPÇA İNCİL · 1590–91", 1630, 470, ("c14s2", "İncil,", 0.2), size=26, w=520),
                L.tag("İBN SİNA · KANUN · 1593", 1630, 400, ("c14s2", "Kanun'u", 0.2), size=26, w=520),
                L.tag("ÖKLİD · 1594", 1630, 330, ("c14s2", "Öklid", 0.2), size=26, w=520)),
         tr=("zoomthru", 0.9, dict(at=(1560, 760), at_b=(1230, 600))), link="scale", label="pres: İncil, Kanun, Öklid"),
    # ── 5. İstanbul: ferman çıktı (harita pan r: Roma → İstanbul) ──────────────────────────────────
    shot("p7_map", ("c14s3", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c14s3", -0.1), (20.0, 40.6, 2.6)), (("c14s3", "ferman", -0.3), (26.0, 40.9, 3.8)), (("c14s3", "çıkmıştı:", 0.3), (28.6, 41.0, 5.0))],
         cities=[dict(lon=ROMA["lon"], lat=ROMA["lat"], name="ROMA", kind="capital", at=("c14s3", -0.1), size=38, side="r"),
                 dict(lon=IST["lon"], lat=IST["lat"], name="İSTANBUL", kind="capital", at=("c14s3", "İstanbul'dan", -0.1), size=42, side="r")],
         icons_=[dict(kind="scroll", lon=28.8, lat=41.25, size=120, at=("c14s3", "ferman", -0.1), metal="gold", glow=0.3)],
         extra=L.mx(L.mimpact(IST["lon"], IST["lat"], ("c14s3", "ferman", -0.1), color="#D8A63A", n=3)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="harita: İstanbul'dan ferman"),
    # ── 6. Ferman: yasak değil, koruma ─────────────────────────────────────────────────────────────
    shot("c14_ferman", ("c14s3", "III.", -1.0), mode="day", unroll_at=("c14s3", "III.", -0.9), seal_at=("c14s3", "Murad,", 0.2), men_at=("c14s3", "kitap", -1.3),
         shield_at=("c14s3", "koruma", -0.1), no_at=("c14s3", "yasak", -0.1), ok_at=("c14s3", "koruma.", -0.05), cam=("push", 0.07),
         ovl=ov(L.tag("III. MURAD", 700, 790, ("c14s3", "III.", -0.1), size=40, sub="İSTANBUL'DAN FERMAN", w=560)),
         tr=("zoomthru", 0.9, dict(at=(1000, 520), at_b=(700, 420))), link="scale", label="ferman: tomar, mühür, tüccarlar, kalkan"),
    # ── 7. Bandini: aynı soyadı, bağ yok (mizah) ───────────────────────────────────────────────────
    shot("c14_bandini", ("c14s4", -0.1), mode="day", a1=("c14s4", "Orazio", -0.3), a2=("c14s4", "1478'de", -0.4), link_at=("c14s4", "bağ", -0.6), no_at=("c14s4", "yok.", -0.3),
         cam=("pan", "r", 150), tr=("sayfa", 0.9), link="material", label="Bandini ↔ Bandini (kayıt yok)"),
    # ── 8. Satış beklenenin altında (rota: Roma → İstanbul, kitaplar yığılır) ──────────────────────
    shot("p7_map", ("c14s5", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c14s5", -0.1), (21.0, 41.0, 2.8)), (("c14s5", "satışının", -0.4), (27.4, 41.2, 4.6))],
         cities=[dict(lon=ROMA["lon"], lat=ROMA["lat"], name="ROMA", kind="capital", at=("c14s5", -0.1), size=38, side="r"),
                 dict(lon=IST["lon"], lat=IST["lat"], name="İSTANBUL", kind="capital", at=("c14s5", -0.1), size=42, side="r")],
         routes=[dict(pts=[(12.4964, 41.9028), (14.2, 40.2), (16.6, 38.9), (19.2, 37.8), (22.6, 37.6), (25.6, 39.0), (28.98, 41.01)], at=("c14s5", "baskıların", -0.4), dur=2.2, color="#233C8C", width=7.0, dash=(18, 12))],
         icons_=[dict(kind="book", route=[(12.4964, 41.9028), (14.2, 40.2), (16.6, 38.9), (19.2, 37.8), (22.6, 37.6), (25.6, 39.0), (28.98, 41.01)], at=("c14s5", "baskıların", -0.4), move_at=("c14s5", "baskıların", -0.4), move_dur=2.2, size=84, metal="gold"),
                 dict(kind="book", lon=28.7, lat=40.8, size=76, at=("c14s5", "beklenenin", 0.0), metal="gold"), dict(kind="book", lon=29.0, lat=40.62, size=76, at=("c14s5", "altında", -0.2), metal="gold"),
                 dict(kind="book", lon=29.3, lat=40.8, size=76, at=("c14s5", "kaldığı", -0.2), metal="gold")],
         ovl=ov(L.stamp("○ TEK KAYNAK", 960, 840, ("c14s5", "anlatılır.", -0.3), size=44, rot=-0.05)),
         tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="harita: Roma→İstanbul, satılmayan kitaplar"),
    # ── 9. Uffizi'nin doğu kanadı ──────────────────────────────────────────────────────────────────
    shot("p7_build", ("c14s6", -0.1), mode="day", build="uffizi", p=1.0, orbit=7, tod="day", cam=("orbit", 7),
         ovl=ov(L.tag("BÜYÜK DÜK FERDINANDO", 560, 190, ("c14s6", "Ferdinando,", -0.1), size=34, w=640, out=("c14s6", "sert", -0.3)),
                L.tag("UFFİZİ · DOĞU KANADI", 1380, 190, ("c14s6", "doğu", -0.2), size=34, w=600, out=("c14s6", "sert", -0.3))),
         tr=("giornata", 0.9), link="material", label="Uffizi (doğu kanadı)"),
    # ── 10. Sert taş kakma: parçalar yerine oturur ───────────────────────────────────────────────
    shot("c14_pietra", ("c14s6", "sert", -0.5), mode="day", start_at=("c14s6", "taşla", 0.0), dt=0.28, polish_at=("c14s6", "çalışıyor.", -0.2), cam=("push", 0.07),
         ovl=ov(L.tag("OPIFICIO DELLE PIETRE DURE", 960, 175, ("c14s6", "Opificio", -0.2), size=38, w=980),
                L.tag("BUGÜN DE ÇALIŞIYOR", 960, 880, ("c14s6", "bugün", -0.1), size=34, w=560)),
         tr=("zoomthru", 0.9, dict(at=(1500, 560), at_b=(960, 470))), link="scale", label="Opificio: taş kakma"),
    # ── 11. 5 Ekim 1600: Floransa, vekâleten ──────────────────────────────────────────────────────
    shot("p7_skyline", ("c14s7", -0.1), mode="day", seed=4, tod="day", pan=320, cam=("pan", "r", 320),
         ovl=ov(L.date_plate("5 EKİM 1600", ("c14s7", "5", -0.1), out=("c14s7", "ertesi", -0.4)),
                L.tag("MARIE DE' MEDICI", 960, 190, ("c14s7", "Marie", -0.1), size=38, w=640, out=("c14s7", "ertesi", -0.4)),
                L.tag("VEKÂLETEN", 960, 300, ("c14s7", "vekâleten", -0.15), size=34, w=420, out=("c14s7", "ertesi", -0.4)),
                L.icon("ring", 1560, 380, 130, ("c14s7", "vekâleten", -0.1), out=("c14s7", "ertesi", -0.4), glow=0.3, bob=4)),
         tr=("yikama", 0.9), link="material", label="Floransa: düğün (vekâleten)"),
    # ── 12. Pitti: perde açılır (Euridice) ───────────────────────────────────────────────────────
    shot("p7_oda", ("c14s7", "ertesi", -0.35), room="perde", path="in", open_at=("c14s7", "Pitti", -0.1), open_dur=3.2, mode="night", cam=("push", 0.07),
         ovl=ov(L.date_plate("6 EKİM 1600", ("c14s7", "ertesi", -0.1)),
                L.tag("PİTTİ SARAYI", 960, 170, ("c14s7", "Pitti", 0.0), size=36, w=520, out=("c14s7", "Euridice", -0.4)),
                L.engr("EURİDİCE", 960, 190, ("c14s7", "Euridice", -0.3), size=96, style="gilt", dur=1.0, glow=0.4, out=("c14s8", 0.1)),
                K.tracker([SAHNE])),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Pitti: perde açılır"),
    # ── 13. Sahne: Orfeo ve Euridice ─────────────────────────────────────────────────────────────
    shot("p7_oda", ("c14s8", -0.12), room="perde", path="stage", open=1.0, mode="night", cam=("push", 0.07),
         ovl=ov(L.tag("ORFEO", 700, 250, ("c14s8", "Orfeo'yu", -0.2), size=36, sub="JACOPO PERİ", w=420),
                L.tag("EURİDİCE", 1240, 250, ("c14s8", "Euridice'yi", -0.2), size=36, sub="VİTTORİA ARCHİLEİ", w=500),
                K.tracker([SAHNE])),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 540))), link="scale", label="sahne yakını: Orfeo/Euridice siluetleri"),
    # ── 14. En eski tam ulaşan opera / Dafne'nin müziği kayıp ─────────────────────────────────────
    shot("c14_nota", ("c14s9", -0.15), mode="day",
         pages=[dict(x=620, y=500, at=("c14s9", 0.0), write=(("c14s9", "müziği", -0.3), 2.0), title="EURİDİCE", seed=3, nseed=7),
                dict(x=1300, y=500, at=("c14s9", "Dafne", -0.5), write=(("c14s9", "Dafne", -0.3), 0.9), fade_at=("c14s9", "müziği", 1, -0.2), title="DAFNE", seed=8, nseed=11,
                     stamp=("MÜZİĞİ KAYIP", ("c14s9", "kayıp.", -0.5), "#A8321E"))],
         cam=("push", 0.07),
         ovl=ov(L.tag("TAM ULAŞAN EN ESKİ", 620, 130, ("c14s9", "tam", -0.1), size=34, w=560), K.tracker([SAHNE])),
         tr=("sayfa", 0.9), link="material", label="Euridice (tam) ↔ Dafne (müziği kayıp)"),
    # ── 15. Caccini önce bastırdı: altı hafta (mizah) ─────────────────────────────────────────────
    shot("c14_nota", ("c14s10", -0.1), mode="day",
         pages=[dict(x=520, y=500, at=("c14s10", 0.0), print_at=("c14s10", "notalarını", 0.0), title="CACCINI", seed=5, nseed=3),
                dict(x=1400, y=500, at=("c14s10", 0.0), print_at=("c14s10", "bastırmıştı.", 0.75), title="PERİ", seed=9, nseed=5)],
         weeks=dict(at=("c14s10", "altı", -0.4), dur=2.0, x=960, y=500), cam=("pan", "r", 150),
         ovl=ov(K.tracker([SAHNE])),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Caccini ↔ Peri: altı hafta"),
    # ── 16. Baba–oğul: lavta ↔ teleskop ──────────────────────────────────────────────────────────
    shot("c14_baba_oglu", ("c14s11", -0.1), mode="day", a1=("c14s11", -0.1), a2=("c14s11", "astronom", -0.2), link_at=("c14s11", "babasıydı.", -0.5), cam=("pan", "r", 130),
         ovl=ov(L.tag("VİNCENZO GALİLEİ", 540, 170, ("c14s11", "Vincenzo", -0.1), size=34, w=560, out=("c14s12", 0.0)),
                L.tag("GALİLEO", 1440, 170, ("c14s11", "Galileo'nun", -0.1), size=34, w=360, out=("c14s12", 0.0))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="baba (lavta) ↔ oğul (teleskop)"),
    # ── 17. YILDIZ AN: mercek görüntüsü, üç «yıldız» ─────────────────────────────────────────────
    shot("c14_gok", ("c14s12", -0.15), mode="night", view="gok", jup=(900.0, 560.0), jr=104.0,
         moons_at=[("c14s12", "yanında", 0.0), ("c14s12", "üç", -0.1), ("c14s12", "küçük", 0.0)], cam=("push", 0.08),
         ovl=ov(L.date_plate("7 OCAK 1610", ("c14s12", "7", -0.1), out=("c14s12", "ocak", 1, 0.0))),
         tr=("iris", 0.9, dict(obj="lens", at=(1690, 420), r=150)), link="shape", label="mercek: Jüpiter ve üç yıldız"),
    # ── 18. Gözlem defteri: sayı dörde çıktı ─────────────────────────────────────────────────────
    shot("c14_gok", ("c14s12", "ocak", 1, -0.25), mode="day", view="defter",
         rows=[(("c14s12", "ocak", 1, 0.0), [-120, -60, 90]), (("c14s12", "bitmeden", -0.2), [-100, 40, 130]), (("c14s12", "bitmeden", 0.3), [-140, -30, 70]),
               (("c14s12", "dörde", -0.1), [-110, -50, 60, 140]), (("c14s12", "çıktı.", -0.2), [-130, 30, 80, 150])], cam=("push", 0.07),
         tr=("zoomthru", 0.9, dict(at=(900, 560), at_b=(960, 236))), link="scale", label="gözlem defteri: 3 → 4"),
    # ── 19. İki seçenek: Cosmica / Medicea ───────────────────────────────────────────────────────
    shot("c14_mektup", ("c14s13", -0.3), mode="day", hdr_at=("c14s13", "iki", -0.2), left_at=("c14s13", "yalnız", 0.0), right_at=("c14s13", "dört", -0.1),
         q_at=("c14s13", "mı", 1, -0.1), pick_at=("c14s14", "ikincisini", 0.0), cam=("push", 0.07),
         tr=("sayfa", 0.9), link="material", label="mektup: Cosmica / Medicea; saray seçti"),
    # ── 20. Sidereus Nuncius kapağı ─────────────────────────────────────────────────────────────
    shot("c14_kapak", ("c14s14", "13", -0.3), mode="day", title_at=("c14s14", "Sidereus", -0.3), band_at=("c14s14", "Medici", -0.3), cam=("push", 0.07),
         ovl=ov(L.date_plate("13 MART 1610", ("c14s14", "13", -0.1)), L.tag("VENEDİK", 1560, 190, ("c14s14", "Venedik'te", -0.1), size=36, w=340),
                L.tag("YILDIZ HABERCİSİ", 1560, 880, ("c14s14", "Yıldız", -0.1), size=32, w=520)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="kapak: MEDICEA SIDERA"),
    # ── 21. Kitap + alet paketi ──────────────────────────────────────────────────────────────────
    shot("c14_paket", ("c14s15", -0.1), mode="day", book_at=("c14s15", "Kitap", -0.1), scope_at=("c14s15", "teleskopla", -0.3), tie_at=("c14s15", "birlikte", -0.5),
         seal_at=("c14s15", "Dük'e", -0.4), send_at=("c14s15", "yazılır.", -0.35), cam=("push", 0.07),
         ovl=ov(L.stamp("○ TEK KAYNAK", 1500, 300, ("c14s15", "yazılır.", -0.1), size=44, rot=-0.06)),
         tr=("zoomthru", 0.9, dict(at=(960, 500), at_b=(640, 560))), link="shape", label="kitap + teleskop paketi"),
    # ── 22. O yaz: Padua → Floransa ───────────────────────────────────────────────────────────────
    shot("p7_map", ("c14s16", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c14s16", -0.1), (11.9, 44.9, 5.2)), (("c14s16", "ayrılıp", 0.0), (11.7, 44.6, 5.6))],
         cities=[dict(lon=PAD[0], lat=PAD[1], name="PADUA", kind="town", at=("c14s16", "Padua'dan", -0.3), size=38, side="r"),
                 dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c14s16", "Padua'dan", 0.0), size=38, side="r")],
         routes=[dict(pts=[(PAD[0], PAD[1]), (11.7, 44.7), (11.4, 44.2), (FLO[0], FLO[1])], at=("c14s16", "ayrılıp", -0.1), dur=1.8, color="#A8321E", width=8.0, dash=(18, 12))],
         icons_=[dict(kind="pillars", lon=PAD[0] - 0.12, lat=PAD[1] + 0.2, size=84, at=("c14s16", "Padua'dan", -0.3), metal="gold"),
                 dict(kind="scroll", route=[(PAD[0], PAD[1]), (11.7, 44.7), (11.4, 44.2), (FLO[0], FLO[1])], at=("c14s16", "ayrılıp", -0.1), move_at=("c14s16", "ayrılıp", -0.1), move_dur=1.8, size=84, metal="gold")],
         ovl=ov(L.tag("BÜYÜK DÜK'ÜN BİRİNCİ MATEMATİKÇİSİ VE FİLOZOFU", 960, 830, ("c14s16", "Büyük", -0.2), size=34, w=1280, out=("c14s17", -0.2)),
                L.stamp("DERS YÜKÜ YOK", 1560, 400, ("c14s16", "ders", -0.1), size=44, rot=-0.07, color="#2E6A46")),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Padua → Floransa (1. kez)"),
    # ── 23. Adlar tutmadı: etiketler düşer (mizah vuruşu) ────────────────────────────────────────
    shot("c14_gok", ("c14s17", -0.1), mode="night", view="adlar", drop_at=("c14s17", "tutmadı:", -0.25), jup=(960.0, 450.0), jr=70.0, cam=("push", 0.07),
         tr=("light", 0.9, dict(at=(960, 450))), link="light", label="MEDİCİ etiketleri düşer, MARIUS gelir"),
    # ── 24. 1633: ağır, süssüz ────────────────────────────────────────────────────────────────────
    shot("c14_dava", ("c14s18", -0.1), mode="night", montage=True, sahne="terazi", date_at=("c14s18", 0.0), date_txt="1633", cam=("push", 0.07),
         tr=("candle", 1.0, dict(at=(960, 450), at_b=(960, 520))), link="light", label="1633: terazi, tek ışık"),
    shot("c14_dava", ("c14s18", "Yargılanan", -0.2), mode="night", montage=True, sahne="kitap", book_at=("c14s18", "kitabı", -0.2), seal_at=("c14s18", "ithaf", -0.5), cam=("push", 0.07),
         ovl=ov(L.tag("BÜYÜK DÜK II. FERDINANDO", 1520, 320, ("c14s18", "Ferdinando'ya", -0.3), size=34, w=660)),
         tr=("dip", 0.9), link="light", label="Dialogo: ithaf mührü"),
    shot("c14_dava", ("c14s18", "Ferdinando", 1, -0.4), mode="night", montage=True, sahne="dilekce", letters_at=(("c14s18", "aklanmasını", -0.6), ("c14s18", "mahkûmiyetten", -0.2), ("c14s18", "temkinli", -0.3)), cam=("pan", "r", 150),
         tr=("candle", 1.0, dict(at=(480, 640), at_b=(440, 640))), link="light", label="temkinli girişimler: üç mektup kapıya kayar"),
    shot("c14_dava", ("c14s19", -0.1), mode="night", montage=True, sahne="isik", lamp_shrink_at=("c14s19", "yere", -0.6), cam=("pull", 0.07),
         tr=("candle", 1.0, dict(at=(440, 640), at_b=(300, 600))), link="light", label="lamba havuzu: kollayabildiği yere kadar"),
    # ── 25. Prens Ferdinando, Padovalı usta (aynı rota, ikinci yolcu) ──────────────────────────────
    shot("p7_map", ("c14s20", -0.1), mode="day", approx=False, cam=("push", 0.07),
         cams=[(("c14s20", -0.1), (11.5, 44.3, 4.6)), (("c14s20", "Padovalı", -0.2), (11.7, 44.6, 5.6)), (("c14s20", "sarayın", -0.3), (11.5, 44.2, 5.0))],
         cities=[dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c14s20", -0.1), size=38, side="r"),
                 dict(lon=PAD[0], lat=PAD[1], name="PADUA", kind="town", at=("c14s20", "Padovalı", -0.2), size=38, side="r")],
         routes=[dict(pts=[(PAD[0], PAD[1]), (11.7, 44.7), (11.4, 44.2), (FLO[0], FLO[1])], at=("c14s20", "klavsen", -0.2), dur=2.0, color="#A8321E", width=8.0, dash=(18, 12))],
         icons_=[dict(kind="scroll", route=[(PAD[0], PAD[1]), (11.7, 44.7), (11.4, 44.2), (FLO[0], FLO[1])], at=("c14s20", "klavsen", -0.2), move_at=("c14s20", "klavsen", -0.2), move_dur=2.0, size=84, metal="gold")],
         extra=L.mx(L.mtag(FLO[0], FLO[1], "PRENS FERDİNANDO", ("c14s20", "Prens", -0.1), dx=-30, dy=-170, size=32, sub="III. COSIMO'NUN OĞLU", w=520),
                    L.mtag(PAD[0], PAD[1], "BARTOLOMEO CRISTOFORI", ("c14s20", "Bartolomeo", -0.2), dx=440, dy=90, size=30, sub="KLAVSEN USTASI", w=560)),
         tr=("light", 0.9, dict(at=(440, 640))), link="light", label="Floransa ↔ Padua: ikinci çağrı"),
    shot("c14_atolye", ("c14s20", "sarayın", -0.3), mode="day", a_master=("c14s20", "sarayın", -0.2), n=3,
         cam=[(("c14s20", "sarayın", -0.3), look(960, 540, 1.0)), (("c14s21", -0.1), look(1900, 540, 1.1))],
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="saray: klavsenler, usta"),
    # ── 26. Envanter satırı: yeni icat edilmiş ───────────────────────────────────────────────────
    shot("p7_ledger", ("c14s21", -0.1), mode="day", head="1700 · MEDİCİ ENVANTERİ", title_l="CALEM", title_r="ENVANTER", cam=("push", 0.07),
         left=[dict(text="arpicembalo", at=("c14s21", "envanterinde", 0.0)), dict(text="“yeni icat edilmiş”", at=("c14s21", "“yeni", -0.1), hl=("c14s21", "ettiği”,", -0.1)),
               dict(text="çekiçli · sönümleyicili", at=("c14s21", "çekiçli", -0.2))],
         right=[], focus=(520, 340),
         ovl=ov(L.stamp("ÇEVİRİ BİZE AİT", 1500, 220, ("c14s21", "ettiği”,", 0.0), size=40, rot=-0.07), K.tracker([SAHNE, ENVANTER])),
         tr=("sayfa", 0.9), link="material", label="envanter: yeni icat edilmiş arpicembalo"),
    shot("c14_piyano", ("c14s21", "çekiçli", -0.45), mode="day",
         presses=[(("c14s21", "çekiçli", 0.0), ("c14s21", "sönümleyicili", 0.0), 0.35), (("c14s21", "sönümleyicili", 0.5), ("c14s22", 0.0), 0.9)],
         tags=[("ÇEKİÇ", (860, 430), (640, 230), ("c14s21", "çekiçli", -0.1)), ("SÖNÜMLEYİCİ", (1220, 420), (1500, 230), ("c14s21", "sönümleyicili", -0.1))],
         cam=[(("c14s21", "çekiçli", -0.45), look(1000, 580, 1.25)), (("c14s22", -0.1), look(1010, 540, 1.5))],
         ovl=ov(K.tracker([SAHNE, ENVANTER])),
         tr=("zoomthru", 0.9, dict(at=(520, 420), at_b=(1000, 560))), link="scale", label="mekanizma: tuş, itici, çekiç, tel, sönümleyici"),
    # ── 27. Piano ve forte (gazete) ──────────────────────────────────────────────────────────────
    shot("c14_gazete", ("c14s22", -0.1), mode="day", head_at=("c14s22", "Maffei'nin", 0.0), piano_at=("c14s22", "piano", -0.1), forte_at=("c14s22", "forte'li", -0.1), cam=("push", 0.07),
         ovl=ov(L.tag("SCİPİONE MAFFEİ", 960, 130, ("c14s22", "Scipione", -0.1), size=34, w=560), K.tracker([SAHNE, ENVANTER])),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="gazete: piano ↔ FORTE"),
    # ── 28. Bugüne kalan üç piyano ───────────────────────────────────────────────────────────────
    shot("c14_vitrin", ("c14s23", -0.1), mode="day",
         cases=[dict(x=700, city="NEW YORK", year="1720", at=("c14s23", "New", -0.5), spot=("c14s23", "üç", -0.5)), dict(x=1500, city="ROMA", year="1722", at=("c14s23", "Roma'da,", -0.5), spot=("c14s23", "piyano", -0.2)),
                dict(x=2300, city="LEİPZİG", year="1726", at=("c14s23", "Leipzig'de.", -0.5), spot=("c14s23", "bugüne", 0.0))],
         cam=[(("c14s23", -0.1), look(700, 540, 1.0)), (("c14s23", "Leipzig'de.", 0.3), look(2300, 540, 1.0))],
         tr=("yikama", 0.9), link="material", label="üç vitrin: New York, Roma, Leipzig"),
    # ── 29. Medici'nin payı: maaş + envanter; icat değil ───────────────────────────────────────
    shot("c14_pay", ("c14s24", -0.1), mode="day", no_at=("c14s24", "icat", -0.2), pay_at=("c14s24", "maaş", -0.2), inv_at=("c14s24", "envantere", -0.3), cam=("push", 0.07),
         tr=("sayfa", 0.9), link="material", label="sahne · maaş · envanter — icat değil"),
    # ── 30. Tek bir satır ────────────────────────────────────────────────────────────────────────
    shot("p7_ledger", ("c14s25", -0.1), mode="day", head="", title_l="", title_r="", cam=("push", 0.08),
         left=[dict(text="arpicembalo — yeni icat edilmiş", at=("c14s25", "tek", -0.3), hl=("c14s25", "doğar.", -0.4))], right=[], focus=(520, 300),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(900, 520))), link="scale", label="envanterde tek satır"),
    # ── 31. Kapı: ailenin kendi satırları azalıyordu ─────────────────────────────────────────────
    shot("c14_azalan", ("c14s26", -0.1), mode="night", rows_at=("c14s26", 0.0), dim_at=("c14s26", "kendi", -0.2), dim_dt=0.42,
         cam=[(("c14s26", -0.1), look(960, 540, 1.0)), (("c14s26", "satırları", 0.0), look(1180, 540, 1.1))],
         tr=("sayfa", 0.9), link="material", label="satırlar sürer; aile satırları söner (kapı → c15)"),
]
YIL_AT = [(("c14s1", 0), 1584), (("c14s2", "Arapça", 1, 0.0), 1593), (("c14s3", "III.", 0.0), 1588), (("c14s7", 0), 1600), (("c14s12", 0), 1610), (("c14s18", 0), 1633),
          (("c14s20", 0), 1688), (("c14s21", 0), 1700), (("c14s22", "Scipione", 0.0), 1711), (("c14s23", "Leipzig'de.", 0.0), 1726)]
