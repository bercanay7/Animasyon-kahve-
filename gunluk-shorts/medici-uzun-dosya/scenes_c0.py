"""c0 — Hiçbir Şey Buradan Çıkmayacak (1737–1743). KANCA, 101 sn, gerçek ses. Yönetmen kartı: yonetmen_c0.md.

KURUL TUR 1 (4 Kasım): 0–3,7 sn KAPAK YANKISI (K1 "SON MEDİCİ / MİRASI KİLİTLEDİ": 1743 imza masası, belge + zincir + asma kilit; kapak_medici.kapak_sahne_shot);
tarih künyesi okunur (koyu levha, ≥40 px, alt sağ); yatak odası 9,2 sn'de kesilir → arma + "MEDİCİ'NİN SON ÜYESİ"; 31 EKİM 1737 levhası (kontrast);
3. madde kartı alıntı DEĞİL ("3. MADDE · ÖZET"); harita "SINIR YAKLAŞIKTIR"; "çıkarılamayacaktı"da zincir + asma kilit (kapak motifi); 1737 koridor
figürleri SİLUET; gerekçe madalyonları hareketli; Uffizi revağı düz arşitrav; "nasıl geldi?" banka yerine Floransa silueti (banka seti c1/c2'ye kaldı).
Işık/zaman: kaynakta saat/hava YOK → oda `tod="dusk"` (alacakaranlık + mum havuzu; pencere nötr, AY/YILDIZ YOK, "gece" iddiası yok).
Tüm çekimler cümle/sözcük çapalı (mutlak saniye yalnız kapak yankısının başı: parça 0,0).
"""
import functools

import anim
import shots as SH
from shots import shot
import cilt_medici as CM
import kapak_medici as KP
import p1_ortak as P
import c0_kinds as K

if not getattr(SH.KINDS["kapak_kilit"], "_p1_ovl", False):     # kapak yankısına ekran-uzayı ovl (tarih künyesi); türün çizimi aynen kalır
    P.add_ovl(["kapak_kilit"])
    SH.KINDS["kapak_kilit"]._p1_ovl = True

DOC = K.DOC_FILL          # oda1743: belge ekranı doldurur (cams anahtarı)

ODA_DUSK = dict(tod="dusk", mode="night", perde=1)

_ECHO = KP.kapak_sahne_shot("K1", a=0.0, yazi=True, yazi_at=0.3, yazi_out=3.2, cam=("push",), label="kapak yankısı K1: SON MEDİCİ / MİRASI KİLİTLEDİ")
_ECHO.params["ovl"] = P.ov(P.tag("18 ŞUBAT 1743", 1590, 812, ("c0s1", "18", -0.05), size=46, out=("c0s2", -0.3)),
                           P.tag("FLORANSA", 1590, 888, ("c0s1", "Floransa", -0.3), size=38, out=("c0s2", -0.3)))

SHOTS = [
    # ── 0. KAPAK YANKISI (0,3–3,5 sn): kapakla aynı kare — belge + zincir + asma kilit; kahraman yazı motorda; tarih künyesi alt sağda ──
    _ECHO,
    # ── 1. 1743 odası: yatak (silüet, nefes), isim levhası ──────────────────
    shot("p1_oda", ("c0s2", -0.15), room="oda1743", figure="lying", **ODA_DUSK,
         cams=[(("c0s2", -0.15), (1000, 30, 1.12)), (("c0s2", "Luisa", 0.0), (960, 34, 1.22)), (("c0s3", -0.1), (900, 40, 1.30))],
         ovl=P.plate("ANNA MARİA LUİSA", 1400, 760, ("c0s2", "Anna", -0.1), w=700),
         cam=("push",), tr=("light", 0.6, dict(at=(900, 700))), link="light", label="1743 odası: yatak (siluet)"),
    # ── 2. "Toskana'yı yönetmiş Medici hattının son üyesi o." — arma parlar; levha: MEDİCİ HANEDANININ SON ÜYESİ (kurul tur 2 KA2-D3: anlatımın
    #       "Toskana'yı yönetmiş … hattının" nitelemesi düşmesin; iki satır: armaya taşmaz) (kesme 9,2 sn) ──
    shot("p1_palle", ("c0s3", -0.1), size=560, pos=(640, 520), mode="night", perde=1,
         ovl=P.ov(P.plate("ANNA MARİA LUİSA", 1340, 330, ("c0s3", "Toskana'yı", -0.2), w=720),
                  K.tag_lines(["MEDİCİ HANEDANININ", "SON ÜYESİ"], 1340, 560, ("c0s3", "son", -0.35), size=52, x_min=990),
                  P.glint(640, 470, ("c0s3", "son", -0.1), r=300, dur=1.4)),
         cam=("push", dict(ease="out")), tr="cut", link="audio", label="arma: Medici'nin son üyesi"),
    # ── 3. Boş taht, yabancı birlik siluetleri girer ───────────────────────
    shot("p1_oda", ("c0s4", -0.1), room="salon", variant="taht", path="taht_in", **ODA_DUSK,
         actors=[dict(kind="asker", x=2430, y=872, h=300, sil=True, prop="halberd", walk=(2080, 140), walk_at=("c0s4", "yabancı", -0.7), seed=3),
                 dict(kind="asker", x=2560, y=884, h=300, sil=True, prop="halberd", walk=(2210, 140), walk_at=("c0s4", "yabancı", -0.5), seed=5),
                 dict(kind="asker", x=980, y=872, h=300, sil=True, prop="halberd", walk=(1330, 140), walk_at=("c0s4", "yabancı", -0.7), seed=7, dir=1),
                 dict(kind="asker", x=850, y=884, h=300, sil=True, prop="halberd", walk=(1200, 140), walk_at=("c0s4", "yabancı", -0.5), seed=9, dir=1)],
         ovl=P.tag("5 YIL 7 AY ÖNCE", 560, 860, ("c0s4", "beş", -0.1), size=40, out=("c0s4", "ölmüştü", 0.9)),
         cam=("push",), tr=("iris", 0.9, dict(obj="palle", at=(640, 520), r=200)), link="shape", label="boş taht, yabancı birlik"),
    # ── 4. Medici salonu: palle frizi; tek siluet "hâlâ o duruyordu" (aynı saray → sert kesme) ──
    shot("p1_oda", ("c0s5", -0.1), room="salon", variant="medici", **ODA_DUSK,
         cams=[(("c0s5", -0.1), (1100, 0, 1.0)), (("c0s5", "yüzyıllarca", 0.0), (1450, 20, 1.1)), (("c0s5", "hâlâ", 0.0), (1760, 50, 1.45))],
         actors=[dict(kind="soylu_f", x=1900, y=858, h=300, action="idle", sil=True, layer="front", seed=4)],
         cam=("pan", "r"), tr="cut", link="cam", label="Medici salonu, tek siluet"),
    # ── 5. 31 Ekim 1737 (zaman sıçraması, mum) · ölümünden 114 gün sonra: takvim ──
    shot("c0_takvim", ("c0s6", -0.15), mode="night", perde=1, show_at=("c0s6", -0.3), start_at=("c0s6", "ölümünden", -0.3), end_at=("c0s6", "dört", 0.2), first=("9", "TEMMUZ", "1737"),
         ovl=P.tag("31 EKİM 1737", 1290, 250, ("c0s6", "31", -0.2), size=58),
         cam=("tilt", "down", 140), tr=("candle", 1.6, dict(at=(960, 640), at_b=(630, 420))), link="light", label="31 Ekim 1737 · 114 gün"),
    # ── 6. bir sözleşme imzalandı: kalem + mühür; kamera belgeye iner ───────
    shot("p1_oda", ("c0s6", "sözleşme", -0.5), room="oda1743", figure="seated", seal_at=("c0s6", "imzalandı", -0.1), **ODA_DUSK,
         cams=[(("c0s6", "sözleşme", -0.5), (1820, 50, 1.5)), (("c0s6", "imzalandı", 0.0), (1900, 80, 2.4)), (("c0s7", -0.1), DOC)],
         cam=("push",), tr="cut", link="audio", label="imza, mühür, belgeye iniş"),
    # ── 7a. Belge: iki yan, iki mühür, 13 madde, FRANSIZCA ─────────────────
    shot("c0_belge", ("c0s7", -0.1), mode="night", perde=1,
         cams=[(("c0s7", -0.1), (0, 0, 0.97)), (("c0s7", "Luisa", 0.0), (-300, 150, 1.5)), (("c0s7", "Lorraine", 0.2), (300, 150, 1.5)),
               (("c0s8", -0.1), (0, 0, 1.0)), (("c0s8", "on", 0.0), (-420, 20, 1.8)), (("c0s8", "ve", 0.0), (-150, -40, 1.25)), (("c0s8", "Fransızca", 0.2), (80, -90, 1.2)),
               (("c0s9", -0.15), (40, -110, 1.28))],
         seals=(("c0s7", "Anna", 0.0), ("c0s7", "Lorraine", 0.3)),
         names_at=("ANNA MARİA LUİSA", "LORRAINE TARAFI", ("c0s7", "Luisa", 0.15), ("c0s7", "tarafı", -0.3)),
         pen_at=("c0s7", "Bir", 0.0),
         num_at=("c0s8", "on", 0.0), num_dur=1.2, fr_at=("c0s8", "Fransızca", 0.0),
         # "13 MADDE" (kurul tur 2 C1): kâğıdın DIŞINDA, masa üstünde, belge düzlemine bağlı (doc x −760); kamera sağa kayınca kâğıtla birlikte
         # kadrajdan çıkar, "Fransızca"da söner → Romen rakamlarının (I–XIII) üstüne asla binmez (eski: ekran x 235'te sabit, 42–43,9 sn çakışma)
         ovl=K.belge_sayac([(("c0s7", -0.1), (0, 0, 0.97)), (("c0s7", "Luisa", 0.0), (-300, 150, 1.5)), (("c0s7", "Lorraine", 0.2), (300, 150, 1.5)),
                            (("c0s8", -0.1), (0, 0, 1.0)), (("c0s8", "on", 0.0), (-420, 20, 1.8)), (("c0s8", "ve", 0.0), (-150, -40, 1.25)), (("c0s8", "Fransızca", 0.2), (80, -90, 1.2)),
                            (("c0s9", -0.15), (40, -110, 1.28))], (-760, -25),
                           ("c0s8", "on", -0.35), 13, dur=0.7, unit="MADDE", size=180, bg=True, min_w=300, unit_size=40, out=("c0s8", "Fransızca", -0.15)),
         tr=("zoomthru", 0.9, dict(at=(960, 520), at_b=(960, 520))), link="scale", cam="hand", label="belge: iki mühür, 13 madde, FRANSIZCA"),
    # ── 7b. ITALIANO yazılır, çizilir — KESME İLE YAKIN PLAN (kurul tur 2 AN2-Ö1 #8: eski ×1,21 sıçrama → ×1,64 ve konu ITALIANO'nun yazılacağı satır;
    #        Romen rakamları kadraj dışında); yakında yavaş itme (≈%1,5/sn), çizgi çekilince hızlı geri çekiliş + carry ──
    shot("c0_belge", ("c0s9", -0.1), mode="night", perde=1,
         cams=[(("c0s9", -0.1), (0, -170, 2.1)), (("c0s9", "diliyle", 0.0), (0, -172, 2.18)), (("c0s9", "yazılmamıştı", 0.45), (0, -176, 2.24)), (("c0s10", -0.4), (0, 0, 1.0))],
         seals=(("c0s7", 0.0), ("c0s7", 0.0)), names_at=("ANNA MARİA LUİSA", "LORRAINE TARAFI", ("c0s7", 0.0), ("c0s7", 0.0)),
         num_at=("c0s8", "on", 0.0), num_dur=0.01, fr_at=("c0s8", 0.0),
         it_at=("c0s9", "diliyle", 0.0), it_strike_at=("c0s9", "yazılmamıştı", -0.2),
         tr="cut", link="cam", cam="hand", label="ITALIANO yazılır, çizilir"),
    # ── 8. Masa başı siluet: odak (bilmiyoruz → biliyoruz) ─────────────────
    shot("p1_oda", ("c0s10", -0.1), room="oda1743", figure="seated", **ODA_DUSK,
         cams=[(("c0s10", -0.1), DOC), (("c0s10", "düşündüğünü", 0.0), (1850, 70, 1.6)), (("c0s11", 0.0), (1880, 60, 1.75))],
         ovl=P.ov(K.soru_ovl(("c0s10", "bilmiyoruz", -0.2), x=905, y=480, size=230, out=("c0s10", "ama", -0.1)),
                  P.glint(1180, 690, ("c0s10", "biliyoruz", -0.6), r=190, dur=1.4)),
         cam=("pull",), tr=("carry", 0.95, dict(strip="paper", dir="r")), link="carry", label="masa başı: bilmiyoruz → biliyoruz"),
    # ── 9. III. madde vurgulanır ──────────────────────────────────────────
    shot("c0_belge", ("c0s11", -0.1), mode="night", perde=1,
         cams=[(("c0s11", -0.1), (0, 0, 1.0)), (("c0s11", "üçüncü", 0.0), (0, -60, 1.7)), (("c0s12", "İtalyanca", 0.3), (0, -160, 2.5))],
         seals=(("c0s7", 0.0), ("c0s7", 0.0)), num_at=("c0s8", "on", 0.0), num_dur=0.01, fr_at=("c0s8", 0.0), hl_at=("c0s11", "üçüncü", -0.2), scrim_at=("c0s11", "üçüncü", -0.2),
         tr=("zoomthru", 0.6, dict(at=(960, 560), at_b=(960, 520))), link="scale", cam=("push",), label="III. madde"),
    # ── 10. Galeri: zoomthru ile açılan Vasari koridoru (1737 figürleri SİLUET); beş kalem sıralanır ──
    shot("p1_pano", ("c0s12", -0.1), pano="p1corridor", tod="day", mode="day", perde=1, stations=[],
         cams=[(("c0s12", -0.1), (2300, 0, 1.08)), (("c0s12", "kütüphaneler", 0.0), (3300, 10, 1.12)), (("c0s12", "Floransa", -0.3), (4300, 0, 1.2))],
         ovl=P.ov(K.hazine_ovl([("c0_galeri", "GALERİLER", ("c0s12", "galeriler", -0.15)), ("c0_tablo", "TABLOLAR", ("c0s12", "tablolar", -0.15)), ("c0_heykel", "HEYKELLER", ("c0s12", "heykeller", -0.15)),
                                ("book_open", "KÜTÜPHANELER", ("c0s12", "kütüphaneler", -0.15)), ("c0_mucevher", "MÜCEVHERLER", ("c0s12", "mücevherler", -0.15)),
                                ("chest", "ÖTEKİ\nKIYMETLİ ŞEYLER", ("c0s12", "öteki", -0.1))], gap=310, size=100),
                  anim.stamp_ovl("ÇEVİRİ", 1460, 260, ("c0s12", "İtalyanca", 0.4), "ink", rot=-0.08, size=50)),
         tr=("zoomthru", 0.9, dict(at=(960, 230), at_b=(960, 520))), link="scale", cam=("truck", "r"), label="galeri: Vasari koridoru, 5 kalem"),
    # ── 11. Harita: Büyük Dukalık (SINIR YAKLAŞIKTIR); "çıkarılamayacaktı"da zincir + asma kilit; 3. MADDE · ÖZET kartı ──
    shot("c0_harita", ("c0s12", "Floransa", -0.4), mode="day", perde=1, approx=False,
         cams=[(("c0s12", "Floransa", -0.4), (11.1, 43.4, 5.0)), (("c0s12", "çıkarılamayacaktı", 0.6), (11.12, 43.4, 6.3)), (("c0s13", "devletin", -0.5), (11.12, 43.42, 6.5))],
         regions=[dict(name="c0_toskana", color="ochre", at=("c0s12", "Büyük", -0.2), alpha=0.6, dur=1.2)],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c0s12", "Floransa", -0.2), size=36)],
         extra=functools.partial(K.sinir_extra, border_at=("c0s12", "Büyük", 0.4), label_at=("c0s12", "Dukalık", -0.2), items_at=("c0s12", "Floransa", 0.0), lock_at=("c0s12", "çıkarılamayacaktı", 0.1),
                                 quote_at=("c0s12", "çıkarılamayacaktı", 0.65), quote_out=None),
         # kurul tur 2 (yerleşim): etiket "3. MADDE · ÖZET" kartının sol-alt köşesine biniyordu (x≈480–568, y≈852–900) → sol üst, deniz üstü
         ovl=P.tag("SINIR YAKLAŞIKTIR", 330, 300, ("c0s12", "Büyük", 0.4), size=36),
         # ENG-D "beyan ↔ gerçekleşen" kapısı (kurul tur 2 AN1-Y2): kayma kilit anına doğru hızlanır (ease in) — beyan edilen hareket ölçülenle tutarlı
         cam=("truck", "r", dict(ease="in")), tr=("slide", 0.6, dict(dir="u")), link="dir", label="harita: Büyük Dukalık, zincir + kilit, 3. madde özeti"),
    # ── 12. Gerekçe: üç madalyon (oturarak gelir, simge sallanır, parıltı) ───
    shot("c0_gerekce", ("c0s13", "devletin", -0.5), mode="day", perde=1,
         draw_at=("c0s13", "aktarılır", -0.3), stamp=("c0s13", "aktarılır", -0.1),
         items=[dict(icon="crown", label="DEVLETİN SÜSÜ", at=("c0s13", "devletin", -0.1)), dict(icon="scales", label="HALKIN YARARI", at=("c0s13", "halkın", -0.1)),
                dict(icon="globe", label="YABANCILARIN MERAKI", at=("c0s13", "yabancıların", -0.1))],
         # kurul tur 2 (AN1-Y8/SA1-Y7): ışık patlaması c0+c1'de yalnız iki ifşa anında → burada malzeme geçişi: sözleşmenin sayfası çevrilir (gerekçe
         # maddesi); lead + erken draw_at: sayfa açılırken başlık ve halkalar zaten çiziliyor (boş parşömenle açılış yok, AN1-Y6)
         cam=("truck", "r", 160), tr=("sayfa", 0.7, dict(lead=True)), link="material", label="gerekçe: süs, yarar, merak"),
    # ── 13. Bugünün kuyruğu: "Yabancıların merakı." (sert kesme, ses köprüsü) — BUGÜN: HUD gizli (kurul tur 2 AN2-K5/SA2-Y3/KA2-D2) ──
    shot("c0_kuyruk", ("c0s14", 0), mode="day", perde=1, cam=("pan", "r"), hud=False,
         sign_at=("c0s15", "Uffizi", 0.0), kick_at=("c0s15", "Bugün", -0.1), coin_at=("c0s15", "müşterisi", 0.0),
         tr="cut", link="audio", label="Uffizi kuyruğu (bugün)"),
    # ── 14. "Peki bir bankacı ailesi … nasıl geldi?" — mirasın bağlandığı şehir (alacakaranlık), soru işareti (bilinçli ters yön) ──
    shot("p1_skyline", ("c0s16", -0.1), seed=2, tod="dusk", mode="night", perde=1, pan=220,
         ovl=P.ov(K.soru_ovl(("c0s16", "geldi", -0.15), out=("c0s17", 0.0))),
         cam=("pan", "l", 220), tr=("slide", 0.6, dict(dir="l")), link="dir", label="nasıl geldi? (Floransa silueti)"),
    # ── 15–16. Kılıçlar değil, altın sikke; geri sarma: 1252 ───────────────
    shot("c0_sikke", ("c0s17", -0.05), mode="night", perde=1, cam=("push",),
         sw_at=("c0s17", "kılıçlarda", -0.1), no_at=("c0s17", "değil", -0.1), coin_at=("c0s17", "altın", -0.2),
         cd_a=("c0s18", "Saati", 0.1), cd_b=("c0s18", "1252", 0.15),
         tr=("yikama", 1.2), link="material", label="kılıç değil sikke; 1252"),
]
YIL_AT = [(("c0s6", "1737", -0.2), 1737), (("c0s18", "geri", -0.1), 1252)]
