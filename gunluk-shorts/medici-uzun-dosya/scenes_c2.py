"""c2 — Defterin Sihri (1397–1429). Parça 1, 3/3 · PARÇA KAPANIŞI. Gerçek ses (v2 yaması). Yönetmen kartı: yonetmen_c2.md.

KURUL TUR 1 (4 Kasım): "kart vadisi" (403–589 sn) dünya/figür sahnelerine çevrildi. Giovanni = tekrar eden İNSAN ÇAPASI (kit banker seed 5:
koyu kızıl cüppe; c1 sonu banka köşesi → c2 açılış → Cossa'ya borç → Martinus'un tahtı → Signoria → oğullarına devir → ölüm döşeği → sadaka).
2 figürlü eylemler: kambiyo (kese → poliçe elden ele), mevduat (kese → lütuf), Kilise müşterisi, Cossa'ya borç, Konstanz (taç düşer),
çifte kayıt yazan kâtip, kapı kapı catasto, devir, ölüm döşeği konuşması (ANEKDOT).
Kurallar: ardışık kart ≤3 · dünya çekimi ≤35 sn arayla · ardışık itme ≤3 · sert kesme ≈%35 (tr="cut") · geçiş süresi 0,35–1,8 sn · ≥12 sn çekim yok.
Mizah (c2): faiz yasağı ↔ kambiyo ↔ vicdan komitesi; "faiz değil hediye"; "eski papa"; çifte kayıt miti. KAPALI: ölüm (siluet + mum), Cossa'nın esareti.
Kapı: "...bir hücreye kapatılacaktı." → Palazzo Vecchio kulesinde yavaş crane up, sessiz ve ağır (END_HOLD motor; bitiş ekranı Program'dan).
"""
import functools

import anim
from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c0_kinds as K0
import c1_kinds as K1
import c2_kinds as K

G = P.GIOVANNI
BANKA = dict(room="p1banka", tod="day", mode="day", perde=1)

SHOTS = [
    # ── 1. Çözüm kambiyodaydı · Kilise faizi yasakladı · bankacılar bir yol buldu — c1'in köşe masasından (Giovanni) devam, salon açılır ──
    shot("p1_oda", ("c2s1", -0.1), **BANKA,
         cams=[(("c2s1", -0.1), (560, 60, 1.52)), (("c2s2", "Kilise", 0.0), (820, 40, 1.30)), (("c2s2", "bankacılar", -0.2), (1150, 20, 1.15)), (("c2s3", -0.2), (1300, 20, 1.12))],
         ovl=P.ov(P.pop_label("KAMBİYO", 960, 236, ("c2s1", "kambiyodaydı", -0.25), size=118, track=16, out=("c2s2", "Kilise", 0.5)),
                  P.glint(960, 226, ("c2s1", "kambiyodaydı", 0.1), r=190),
                  P.tablet_icon("cross", "KİLİSE: FAİZ = TEFECİLİK", 660, 340, ("c2s2", "Kilise", -0.1), w=760, size=36, out=("c2s2", "bankacılar", -0.3)),
                  anim.stamp_ovl("YASAK", 1460, 440, ("c2s2", "yasaklamıştı", 0.05), "squash", rot=-0.08, size=84, out=("c2s2", "bankacılar", -0.2)),
                  P.icon_at("compass", 960, 450, ("c2s2", "yol", -0.25), size=240, glow=True, bob=8),
                  P.tag("BİR YOL", 960, 660, ("c2s2", "buldular", -0.3), size=52)),
         cam=("pull",), tr=("light", 0.6, dict(at=(960, 540))), link="light", label="banka: kambiyo; Kilise faizi yasakladı; bir yol"),
    # ── 2. Brugge: parayı peşin verirsin (kese) · karşılığında Barselona'ya çekilmiş poliçe alırsın — 2 BÜYÜK figür, elden ele ──
    shot("p1_oda", ("c2s3", -0.15), room="salon", variant="napoli", tod="day", mode="day", perde=1, map_at=("c2s3", "Barselona'ya", -0.3),
         actors=[dict(kind="banker", seed=52, x=1150, y=870, h=440, action="talk", dir=1, layer="front", phase=0.2),
                 dict(kind="tuccar", seed=8, x=1560, y=870, h=440, action="idle", dir=-1, layer="front")],
         cams=[(("c2s3", -0.15), (1500, 20, 1.12)), (("c2s3", "Brugge'de", 0.0), (1380, 60, 1.32)), (("c2s3", "karşılığında", 0.0), (1395, 66, 1.40)), (("c2s4", -0.25), (1430, 70, 1.46))],
         ovl=P.ov(P.plate("BRUGGE", 560, 160, ("c2s3", "Brugge'de", -0.3), role="KLASİK BİR ÖRNEK", w=560),
                  P.prop_arc("p1_kese", (726, 690), (1097, 690), ("c2s3", "peşin", -0.1), dur=0.8, size=120, lift=110, show_from=("c2s3", "parayı", -0.4), metal="bronze"),
                  P.prop_arc("scroll", (1058, 660), (690, 680), ("c2s3", "alırsın", -0.4), dur=0.8, size=118, lift=90, show_from=("c2s3", "karşılığında", -0.1)),
                  P.tag("BARSELONA'YA ÇEKİLMİŞ POLİÇE", 960, 300, ("c2s3", "Barselona'ya", -0.2), size=40)),
         cam=("push",), tr=("slide", 0.7, dict(dir="r")), link="dir", label="Brugge: kese verilir, poliçe alınır"),
    # ── 3. Vadesi gelince tahsil; ikinci poliçeyle para geri döner; kazanç = kur farkı (tek harita, anahtar kareli) ──
    shot("p1_map", ("c2s4", -0.15), mode="day", perde=1, approx=False,
         cams=[(("c2s4", -0.15), (2.7, 45.3, 1.85)), (("c2s4", "ikinci", -0.3), (2.8, 45.3, 1.95)), (("c2s4", "kazanç", -0.3), (2.8, 45.4, 1.78))],
         cities=[dict(lon=3.22, lat=51.21, name="BRUGGE", kind="capital", at=-0.5, size=36), dict(lon=2.17, lat=41.39, name="BARSELONA", kind="capital", at=-0.5, size=36)],
         routes=[dict(pts=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], at=("c2s4", -0.1), dur=1.0, width=7, color="#A8321E"),
                 dict(pts=[(2.17, 41.39), (5.1, 46.0), (3.22, 51.21)], at=("c2s4", "ikinci", -0.3), dur=1.6, width=7, color="#233C8C")],
         icons_=[dict(kind="scroll", lon=3.22, lat=51.21, size=84, at=("c2s4", -0.1), route=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], move_at=("c2s4", -0.05), move_dur=1.1, glow=0.0),
                 dict(kind="coins", lon=2.17, lat=41.39, size=100, at=("c2s4", "tahsil", -0.3), bob=4),
                 dict(kind="scroll", lon=2.17, lat=41.39, size=84, at=("c2s4", "ikinci", -0.2), route=[(2.17, 41.39), (5.1, 46.0), (3.22, 51.21)], move_at=("c2s4", "poliçeyle", -0.3), move_dur=1.4, glow=0.0),
                 dict(kind="coinbag", lon=3.22, lat=51.21, size=100, at=("c2s4", "geri", -0.1), bob=4)],
         ovl=P.ov(P.tag("VADESİ GELİNCE TAHSİL", 560, 250, ("c2s4", "Vadesi", -0.1), size=40, out=("c2s4", "kazanç", -0.3)),
                  P.pop_label("KUR FARKI", 1440, 250, ("c2s4", "kur", -0.1), size=84, track=10)),
         cam=("pull",), tr=("zoomthru", 0.55, dict(at=(690, 680), at_b=(960, 520))), link="scale", label="poliçe gider, para döner: kur farkı"),
    # ── 4. Ortada borç yok, faiz yok; yalnızca kur farkı ─────────────────────
    shot("c2_nolist", ("c2s5", -0.15), mode="day", perde=1, borc_at=("c2s5", "borç", -0.25), borc_x=("c2s5", "yok", -0.15), faiz_at=("c2s5", "faiz", -0.25), faiz_x=("c2s5", "yok", 1, -0.15), kur_at=("c2s5", "yalnızca", -0.2),
         cam=("pan", "r"), tr="cut", link="audio", label="BORÇ ✗ FAİZ ✗ KUR FARKI ✓"),
    # ── 5. vicdan komitesi (mizah): Medici salonu, masa başı siluetler ─────────
    shot("p1_oda", ("c2s6", -0.15), room="salon", variant="medici", sil=True, tod="day", mode="day", perde=1, path="heads",
         ovl=P.ov(anim.stamp_ovl("VİCDAN KOMİTESİ", 960, 320, ("c2s6", "vicdan", 0.1), "bounce", rot=-0.05, size=88),
                  P.icon_at("scales", 1500, 470, ("c2s6", "departmanı", -0.1), size=190, glow=True, bob=6),
                  P.tag("EN YARATICI DEPARTMAN", 1440, 640, ("c2s6", "yaratıcı", -0.2), size=36)),
         cam=("pan", "r"), tr="cut", link="audio", label="vicdan komitesi"),
    # ── 6. mevduat: kese masaya; faiz yazılmaz; banker lütuf olarak öder (kese geri döner, mudi eğilir) ──
    shot("p1_oda", ("c2s7", -0.15), **BANKA,
         actors=[dict(kind="soylu", seed=21, x=2200, y=880, h=430, action="bow", at=("c2s7", "lütuf", 0.2), dur=1.2, depth=16.0, dir=-1, layer="front")],
         cams=[(("c2s7", -0.15), (1950, 50, 1.25)), (("c2s7", "faiz", 0.0), (1925, 58, 1.33)), (("c2s7", "banker", 0.0), (1905, 66, 1.42)), (("c2s8", -0.3), (1895, 72, 1.48))],
         ovl=P.ov(P.plate("TİM PARKS", 520, 170, ("c2s7", "Parks'ın", -0.2), role="AKTARDIĞINA GÖRE", w=520, out=("c2s7", "banker", -0.3)),
                  P.prop_arc("p1_kese", (1226, 700), (901, 760), ("c2s7", "mevduata", -0.1), dur=0.9, size=110, lift=90, show_from=("c2s7", -0.15), out=("c2s7", "lütuf", -0.3), metal="bronze"),
                  P.tag("FAİZ", 760, 360, ("c2s7", "faiz", -0.2), size=52, out=("c2s7", "banker", 0.0)),
                  P.crossout(760, 360, 70, ("c2s7", "yazılmaz", -0.1), out=("c2s7", "banker", 0.0), sw=12),
                  P.prop_arc("p1_kese", (880, 740), (1200, 690), ("c2s7", "lütuf", -0.2), dur=0.8, size=84, lift=100, show_from=("c2s7", "lütuf", -0.4), metal="bronze")),
         cam=("push",), tr="cut", link="audio", label="mevduat: faiz yazılmaz; lütuf"),
    # ── 7. Faiz değil, hediye (kese; vuruş) ──────────────────────────────────
    shot("c2_hediye", ("c2s8", -0.2), mode="day", perde=1, tag_at=("c2s8", "Faiz", -0.15), open_at=("c2s8", "Faiz", -0.3), strike_at=("c2s8", "değil", -0.05), gift_at=("c2s8", "hediye", -0.1),
         cam=("push", dict(rate=0.03)), tr="cut", link="audio", label="faiz değil, hediye"),
    # ── 8. Üstelik müşterilerinden biri Kilise'nin ta kendisi: kardinal keseyi bankacıya verir ──
    shot("p1_oda", ("c2s9", -0.15), room="sakristi", tod="day", mode="day", perde=1, open=0.15,
         actors=[dict(kind="kardinal", seed=9, x=2050, y=870, h=440, action="idle", dir=1, layer="front"),
                 dict(kind="banker", seed=52, x=2420, y=870, h=440, action="bow", at=("c2s9", "kendisiydi", -0.4), dur=1.0, depth=12.0, dir=-1, layer="front")],
         cams=[(("c2s9", -0.15), (2150, 40, 1.22)), (("c2s9", "Kilise'nin", 0.0), (2230, 60, 1.38))],
         ovl=P.ov(P.tag("MÜŞTERİ: KİLİSE", 600, 220, ("c2s9", "müşterilerinden", -0.2), size=46),
                  P.prop_arc("coinbag", (1135, 690), (1505, 700), ("c2s9", "yasaklayan", -0.2), dur=0.9, size=120, lift=110, show_from=("c2s9", "müşterilerinden", -0.3)),
                  P.glint(1505, 640, ("c2s9", "kendisiydi", -0.1), r=170)),
         cam=("push",), tr="cut", link="audio", label="müşteri: Kilise'nin ta kendisi"),
    # ── 9. Roma şubesi: ayrı sermaye yok; kasayı Kilise'nin parası doldurdu ───
    shot("c2_kasa", ("c2s10", -0.15), mode="day", perde=1, branch_at=("c2s10", "Roma", -0.2), nocap_at=("c2s10", "ayrı", -0.2), church_at=("c2s10", "Kilise'nin", -0.3), fill_at=("c2s10", "kasayı", -0.1), fill_to=("c2s10", "doldurdu", 0.3),
         ovl=P.tag("DE ROOVER'A GÖRE", 1480, 860, ("c2s10", "Roover'a", 0.0), size=40),
         cam=("pan", "r"), tr=("zoomthru", 0.5, dict(at=(1505, 700), at_b=(960, 520))), link="scale", label="Roma şubesi: kasayı Kilise doldurdu"),
    # ── 10. 25 Mart 1402: Venedik şubesi; Floransa'da o gün yılbaşı ─────────
    shot("p1_map", ("c2s11", -0.15), mode="day", perde=1, approx=False,
         cams=[(("c2s11", -0.15), (11.9, 44.7, 3.6)), (("c2s11", "Venedik", 0.0), (12.0, 44.9, 4.6)), (("c2s11", "yılbaşıydı", 0.0), (11.8, 44.6, 4.0))],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c2s11", -0.0), size=36), dict(lon=12.34, lat=45.44, name="VENEDİK", kind="capital", at=("c2s11", "Venedik", -0.25), size=38)],
         routes=[dict(pts=[(11.25, 43.77), (11.9, 44.7), (12.34, 45.44)], at=("c2s11", "Venedik", -0.3), dur=1.4, width=7)],
         ovl=P.ov(P.tag("25 MART 1402", 470, 250, ("c2s11", "Mart", -0.3), size=52),
                  anim.stamp_ovl("YILBAŞI", 1440, 420, ("c2s11", "yılbaşıydı", 0.0), "bounce", rot=-0.07, size=70),
                  P.icon_at("hourglass", 440, 520, ("c2s11", "Floransa'da", -0.1), size=170, glow=True, bob=5)),
         cam=("pan", "r"), tr=("yikama", 1.6), link="material", label="25 Mart 1402: Venedik şubesi; yılbaşı"),
    # ── 11. Çifte kaydı Medici'ler icat etti derler (MİT): kâtip yazar, aynı florin iki sütuna, sütunlar dengelenir ──
    shot("p1_oda", ("c2s12", -0.15), room="salon", variant="napoli", tod="day", mode="day", perde=1,
         actors=[dict(kind="banker", seed=61, x=1016, y=823, h=282, action="write", seated=True, dir=1)],
         cams=[(("c2s12", -0.15), (1270, 50, 1.36)), (("c2s13", -0.2), (1250, 56, 1.40))],
         ovl=P.ov(K.cifte_panel(("c2s12", "Çifte", 0.0), ("c2s12", "kaydı", 0.25), ("c2s12", "icat", 0.0)),
                  anim.stamp_ovl("MİT", 1640, 300, ("c2s12", "derler", 0.0), "drop", rot=-0.1, size=104)),
         cam="hand", tr="cut", link="audio", label="çifte kayıt: kâtip; MİT"),
    # ── 12. Etmediler: Cenova 1340 … (Venedik 1407 KALDIRILDI; arma yerine sözcük) ──
    shot("p1_timeline", ("c2s13", -0.15), hud=False, a0=1320, a1=1520, step=20, mode="day", perde=1, title="ÇİFTE KAYDIN İZİ",
         events=[(1340, "CENOVA", ("c2s13", "Cenova'nın", -0.1)), (1494, "PACIOLI", ("c2s13", "biridir", -0.2))], hl=None,
         ovl=P.ov(anim.stamp_ovl("ETMEDİLER", 960, 800, ("c2s13", "Etmediler", 0.1), "spin", rot=-0.04, size=84, out=("c2s13", "tarihli", 0.0)),
                  P.tag("MEDİCİ İCADI", 1500, 300, ("c2s13", "eski", -0.4), size=40),
                  P.crossout(1500, 300, 170, ("c2s13", "eski", 0.0), sw=10)),
         cam=("pan", "r"), tr="cut", link="audio", label="çifte kayıt: Cenova 1340 → Pacioli 1494"),
    # ── 13a. Medici'nin farkı defterde değil, yapıdaydı (vuruş: DEFTER ✗ → YAPI) ──
    shot("p1_network", ("c2s14", -0.15), mode="day", perde=1, title="MEDİCİ'NİN FARKI: YAPI", legend=False, size=170,
         nodes=[dict(id="f", name="FLORANSA", icon="coinbag", x=0.50, y=0.46, at=("c2s14", "yapıdaydı", -0.3), size=200)],
         edges=[],
         ovl=P.ov(P.icon_at("book", 640, 560, ("c2s14", "defterde", -0.3), size=170, out=("c2s14", "yapıdaydı", 0.2)),
                  P.crossout(640, 560, 120, ("c2s14", "değil", -0.1), out=("c2s14", "yapıdaydı", 0.2)),
                  P.tag("DEFTER DEĞİL", 640, 800, ("c2s14", "defterde", -0.1), size=40, out=("c2s14", "yapıdaydı", 0.2))),
         cam=("push", 0.08), tr=("light", 0.6, dict(at=(960, 480))), link="light", label="fark defterde değil, yapıda"),
    # ── 13b. her şubenin kendi ortaklığı, kendi defteri (aynı ağ; sert kesme) ──
    shot("p1_network", ("c2s14", "her", -0.2), mode="day", perde=1, title="MEDİCİ'NİN FARKI: YAPI", legend=False, size=170,
         nodes=[dict(id="f", name="FLORANSA", icon="coinbag", x=0.50, y=0.42, at=("c2s14", -0.15), size=190),
                dict(id="r", name="ROMA", icon="book", x=0.20, y=0.58, at=("c2s14", "şubenin", -0.1), size=160),
                dict(id="v", name="VENEDİK", icon="book", x=0.80, y=0.58, at=("c2s14", "kendi", -0.1), size=160)],
         edges=[("f", "r", "ortaklik", ("c2s14", "ortaklığı", -0.2)), ("f", "v", "ortaklik", ("c2s14", "ortaklığı", 0.1))],
         ovl=P.ov(P.tag("KENDİ ORTAKLIĞI", 480, 860, ("c2s14", "ortaklığı", -0.1), size=38),
                  P.tag("KENDİ DEFTERİ", 1440, 860, ("c2s14", "defteri", -0.15), size=38)),
         cam=("pull", 0.08), tr="cut", link="audio", label="her şubenin kendi ortaklığı ve defteri"),
    # ── 14. Giovanni Cossa'ya borç verir; adam XXIII. Johannes adıyla papa olur (tiara) — 2 BÜYÜK figür ──
    shot("p1_oda", ("c2s15", -0.15), room="p1ofis", variant="ofis", tod="day", mode="day", perde=1, figure=None,
         actors=[dict(G, x=1000, y=880, h=460, action="talk", dir=1, layer="front"),
                 dict(kind="kardinal", seed=9, x=1400, y=880, h=460, action="idle", dir=-1, layer="front")],
         cams=[(("c2s15", -0.15), (1150, 50, 1.25)), (("c2s15", "borç", 0.0), (1200, 60, 1.32)), (("c2s15", "papa", 0.0), (1330, 40, 1.46))],
         ovl=P.ov(P.plate("GIOVANNI", 520, 300, ("c2s15", "Giovanni", -0.2), w=420, out=("c2s15", "adam", 0.0)),
                  P.plate("BALDASSARRE COSSA", 900, 190, ("c2s15", "Baldassarre", -0.2), role="KİLİSE ADAMI", w=700, out=("c2s15", "XXIII.", -0.3)),
                  P.prop_arc("p1_kese", (803, 697), (1143, 697), ("c2s15", "borç", -0.1), dur=0.8, size=110, lift=110, show_from=("c2s15", "Giovanni", 0.0), metal="bronze"),
                  P.prop_arc("p1_tiara", (1061, 200), (1061, 452), ("c2s15", "adıyla", 0.0), dur=0.9, size=150, lift=0, show_from=("c2s15", "adıyla", -0.3), glow=True),
                  P.plate("COSSA = XXIII. JOHANNES", 900, 190, ("c2s15", "XXIII.", -0.1), role="PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR", w=760)),
         cam=("truck", "r"), tr=("light", 0.7, dict(at=(960, 520))), link="light", label="Giovanni → Cossa: borç; papa (tiara)"),
    # ── 15. 1415: Konstanz Konsili onu indirdi — boş taht, ruhban sırası; taç düşer (sola: düşüş) ──
    shot("p1_oda", ("c2s16", -0.15), room="p1salon", variant="konstanz", tod="day", mode="day", perde=1,
         actors=[dict(kind="kardinal", seed=31, x=1230, y=870, h=420, action="idle", dir=1, layer="front"),
                 dict(kind="rahip", seed=32, x=1360, y=860, h=400, action="idle", dir=1, layer="back"),
                 dict(kind="rahip", seed=33, x=2060, y=860, h=400, action="idle", dir=-1, layer="back"),
                 dict(kind="kardinal", seed=35, x=2190, y=870, h=420, action="point", at=("c2s16", "indirdi", -0.3), dir=-1, layer="front")],
         cams=[(("c2s16", -0.15), (1720, 30, 1.18)), (("c2s16", "indirdi", 0.0), (1600, 50, 1.26))],
         ovl=P.ov(P.tag("KONSTANZ KONSİLİ · 1415", 640, 190, ("c2s16", "Konstanz", -0.3), size=46),
                  P.prop_arc("p1_tiara", (1000, 650), (720, 960), ("c2s16", "indirdi", -0.25), dur=0.9, size=130, lift=-40, show_from=("c2s16", -0.15), rot1=-1.2),
                  anim.impact_ovl(("c2s16", "indirdi", 0.6), amp=4)),
         cam=("pan", "l"), tr="cut", link="audio", label="Konstanz 1415: taht boş, taç düşer"),
    # ── 16. kefalet mi fidye mi: kaynaklar ayrışıyor ─────────────────────────
    shot("c2_ayrim", ("c2s17", -0.15), mode="day", perde=1, walk_at=("c2s17", "İndirilen", -0.1), fork_at=("c2s17", "Giovanni'nin", -0.3), left_at=("c2s17", "kefaletle", -0.25), right_at=("c2s17", "fidyeyle", -0.25), stamp_at=("c2s17", "ayrışıyor", -0.3),
         cam=("pan", "r"), tr="cut", link="audio", label="kefalet mi fidye mi: yol ayrımı"),
    # ── 17a. Vaftizhane anıtı: gisant, perde; "ESKİ PAPA" oyulur ─────────────
    shot("c2_mezar", ("c2s18", -0.15), mode="day", perde=1, place_at=("c2s18", "Vaftizhane'ye", -0.3), carve_at=("c2s18", "eski", -0.5), carve_to=("c2s18", "papa", 0.35),
         cam=("tilt", "up", 120), tr=("light", 1.0, dict(at=(960, 760))), link="light", label="Cossa'nın anıtı: ESKİ PAPA"),
    # ── 17b. Papa V. Martinus itiraz etti (papalık salonu, ayakta işaret) ─────
    shot("p1_oda", ("c2s19", -0.15), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="point", at=("c2s19", "itiraz", -0.25), dir=-1, layer="back")],
         cams=[(("c2s19", -0.15), (1560, 40, 1.30)), (("c2s19", "Yazıt", 0.0), (1590, 46, 1.36))],
         ovl=P.ov(P.tag("V. MARTINUS", 640, 220, ("c2s19", "Martinus", -0.3), size=48),
                  anim.stamp_ovl("İTİRAZ", 1050, 380, ("c2s19", "itiraz", 0.15), "spin", rot=-0.10, size=76)),
         cam=("push",), tr="cut", link="audio", label="V. Martinus itiraz eder"),
    # ── 17c. Yazıt kaldı (aynı anıt, parıltı) ────────────────────────────────
    shot("c2_mezar", ("c2s19", "Yazıt", -0.15), mode="day", perde=1, carve_at=("c2s18", "eski", -0.5), carve_to=("c2s18", "papa", 0.35), stay_at=("c2s19", "Yazıt", 0.0),
         cam=("tilt", "up", 130), tr="cut", link="cam", label="yazıt kaldı"),
    # ── 18a. kaynak: de Roover'ın andığı arşiv belgeleri (BELGE — rivayet değil; teyit_P1 c2s20); mitra borca karşılık ──
    shot("c2_rivayet", ("c2s20", -0.15), mode="day", perde=1, medal=False, pawn_at=("c2s20", "belgelere", -0.2), pawn_label="BORÇ KARŞILIĞI",
         ovl=P.ov(P.plate("DE ROOVER", 600, 170, ("c2s20", "De", -0.25), role="ANDIĞI ARŞİV BELGELERİ", w=640),
                  anim.stamp_ovl("BELGE · DE ROOVER", 1250, 360, ("c2s20", "belgelere", 0.0), "drop", rot=-0.06, size=50)),
         cam=("tilt", "down", 130), tr=("sayfa", 0.5), link="material", label="belge (de Roover): mitra borç karşılığı"),
    # ── 18b. Martinus mitrayı geri ister (papalık salonu; Giovanni elinde mitra) ─────────────────
    shot("p1_oda", ("c2s20", "Martinus", -0.3), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="point", at=("c2s20", "geri", -0.3), dir=-1, layer="back"),
                 dict(G, x=1180, y=890, h=470, action="idle", dir=1, layer="front")],
         cams=[(("c2s20", "Martinus", -0.3), (1450, 40, 1.25)), (("c2s20", "Giovanni'yi", -0.3), (1480, 44, 1.30))],
         ovl=P.ov(P.icon_at("c2_mitra", 690, 690, ("c2s20", "Martinus", -0.3), size=150, bob=4),
                  P.tag("BORÇ KARŞILIĞI BIRAKILAN MİTRA", 760, 200, ("c2s20", "borca", -0.2), size=40)),
         cam=("push",), tr="cut", link="audio", label="Martinus mitrayı geri ister"),
    # ── 18c. aforoz tehdidi (yakın iki kişilik; sert kesme) ─────────────────────────────────────
    shot("p1_oda", ("c2s20", "Giovanni'yi", -0.3), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="threat", at=("c2s20", "aforozla", -0.35), dir=-1, layer="back"),
                 dict(G, x=1180, y=890, h=470, action="bow", at=("c2s20", "tehdit", 0.0), dir=1, layer="front")],
         cams=[(("c2s20", "Giovanni'yi", -0.3), (1400, 70, 1.55)), (("c2s21", -0.2), (1380, 76, 1.62))],
         ovl=P.ov(P.icon_at("c2_mitra", 640, 700, ("c2s20", "Giovanni'yi", -0.3), size=170, bob=3),
                  P.tag("AFOROZ TEHDİDİ", 960, 200, ("c2s20", "aforozla", 0.1), size=56, dur=0.25),
                  anim.impact_ovl(("c2s20", "aforozla", 0.2), amp=3)),
         cam=("push",), tr="cut", link="cam", label="aforoz tehdidi (belgeli)"),
    # ── 19a. Papalığın resmî kasa memurluğu (anahtar; 1422'den sonra) — teyit_P1 c2s21 (DBI) ──
    shot("p1_emblem", ("c2s21", -0.15), icon="p1_anahtar", metal="gold", size=420, pos=(960, 560), mode="day", perde=1,
         ovl=P.ov(P.tag("PAPALIĞIN RESMÎ KASA MEMURLUĞU", 960, 190, ("c2s21", "kasa", -0.4), size=46),
                  P.tag("1422'DEN SONRA", 960, 860, ("c2s21", "1422'den", -0.2), size=48),
                  P.glint(960, 520, ("c2s21", "memurluğu", 0.0), r=220, dur=1.0)),
         cam=("push", 0.08), tr=("light", 0.7, dict(at=(960, 560))), link="light", label="kasa memurluğu: 1422'den sonra"),
    # ── 19b. MONTAJ: 22 yıl kesintisiz (düz şerit) ───────────────────────────
    shot("p1_emblem", ("c2s21", "yirmi", -0.15), icon="p1_anahtar", metal="gold", size=300, pos=(380, 560), mode="day", perde=1, montage=True,
         ovl=K.kasa_cubuk(800, 560, 960, ("c2s21", -0.2), ("c2s21", "yirmi", -0.1), ("c2s21", "ardından", -0.1)),
         cam=("truck", "r", 130), tr="cut", link="audio", label="22 yıl kesintisiz"),
    # ── 19c. MONTAJ: + 18 yıl aralıklı (kesikli şerit) ───────────────────────
    shot("p1_emblem", ("c2s21", "ardından", -0.2), icon="p1_anahtar", metal="gold", size=300, pos=(380, 560), mode="day", perde=1, montage=True,
         ovl=P.ov(K.kasa_cubuk(800, 560, 960, ("c2s21", -0.2), ("c2s21", "yirmi", -0.1), ("c2s21", "ardından", -0.1)),
                  P.tag("MEDİCİ'DE KALDI", 1280, 860, ("c2s21", "Medici'de", -0.2), size=44)),
         cam=("pull", 0.07), tr="cut", link="audio", label="+ 18 yıl aralıklı"),
    # ── 20. 1427: Floransa hanelerin servetini tek tek yazdırdı — kayıt görevlileri kapı kapı ──
    shot("p1_sehir", ("c2s22", -0.15), scene="sokak", tod="day", mode="day", perde=1,
         actors=[dict(kind="banker", seed=61, x0=560, dir=1, speed=64, h=300, prop="book", at=("c2s22", -0.15)),
                 dict(kind="banker", seed=62, x0=430, dir=1, speed=64, h=296, prop="quill", at=("c2s22", -0.15)),
                 dict(kind="halk", seed=3, x0=1540, dir=-1, speed=0, h=280, action="talk", at=("c2s22", -0.15)),
                 dict(kind="soylu_f", seed=6, x0=1660, dir=-1, speed=0, h=270, action="idle", at=("c2s22", -0.15))],
         cams=[(("c2s22", -0.15), (900, 40, 1.15)), (("c2s23", -0.2), (1220, 50, 1.22))],
         ovl=P.ov(P.tag("KATASTO · 1427", 560, 200, ("c2s22", "1427'de", -0.2), size=48),
                  P.tag("HANE HANE", 1380, 200, ("c2s22", "tek", -0.2), size=42)),
         cam=("truck", "r"), tr=("slide", 0.5, dict(dir="r")), link="dir", label="catasto: görevliler kapı kapı"),
    # ── 21a–c. MONTAJ (kesmeler): 9.780 hane · 137 hane = %29,8 · en zengini Strozzi ──
    shot("c2_katasto", ("c2s23", -0.15), mode="day", perde=1, write_at=("c2s23", -0.6), write_to=("c2s23", "hane", 0.0), title_at=("c2s23", -1.0),
         ovl=P.tag("137 HANE", 1500, 260, ("c2s23", "yüz", -0.2), size=48),
         cam=("push", dict(rate=0.025)), montage=True, tr="cut", link="audio", label="catasto: 9.780 hane"),
    shot("p1_stacked", ("c2s23", "kayıtlı", -0.3), parts=[("137 HANE", 29.8, "gold", ("c2s23", "yüzde", -0.3)), ("GERİ KALAN HANELER", 70.2, "umber", ("c2s23", "yüzde", 0.0))], total=100, unit="%", title="KAYITLI SERVET", total_label="%29,8",
         mode="day", perde=1, dur=0.9,
         ovl=anim.stamp_ovl("BİR HESABA GÖRE", 1480, 250, ("c2s23", "hesaba", 0.0), "ink", rot=-0.06, size=44),
         cam=("pan", "r"), montage=True, tr="cut", link="audio", label="137 hane ≈ %30"),
    shot("p1_emblem", ("c2s23", "en", -0.15), icon="chest", metal="gold", size=420, pos=(1180, 560), mode="day", perde=1,
         ovl=P.ov(P.plate("PALLA STROZZI", 560, 300, ("c2s23", "Palla", -0.5), role="1427'NİN EN ZENGİNİ", w=720),
                  P.count_up(560, 640, ("c2s23", "zengini", -0.05), 162925, dur=0.8, unit="FLORİN · BRÜT", size=150, bg=True, min_w=500, unit_size=36)),
         cam=("push",), montage=True, tr="cut", link="audio", label="1427'nin en zengini: Palla Strozzi"),
    # ── 22. Giovanni sayımın yürürlüğe girmesini destekledi (Signoria salonu) ──
    shot("p1_oda", ("c2s24", -0.15), room="salon", variant="signoria", tod="day", mode="day", perde=1,
         actors=[dict(kind="soylu", seed=11, x=1016, y=823, h=282, action="listen", seated=True, dir=1),
                 dict(kind="soylu", seed=14, x=2384, y=823, h=282, action="listen", seated=True, dir=-1, rim_dir=-1),
                 dict(G, x=1700, y=885, h=460, action="talk", dir=-1, layer="front")],
         cams=[(("c2s24", -0.15), (1640, 50, 1.26)), (("c2s25", -0.2), (1680, 60, 1.32))],
         ovl=P.ov(P.tag("GIOVANNI · CATASTO'YU DESTEKLEDİ", 760, 200, ("c2s24", "Giovanni", -0.1), size=42),
                  anim.stamp_ovl("DESTEKLEDİ", 1360, 420, ("c2s24", "destekledi", 0.0), "squash", rot=-0.06, size=60)),
         cam="hand", tr="cut", link="audio", label="Giovanni catasto'yu destekledi"),
    # ── 23. 1420: yönetimi oğullarına bıraktı (defter + anahtar elden ele) ─────
    shot("p1_oda", ("c2s25", -0.15), room="p1ofis", variant="ofis", tod="day", mode="day", perde=1, figure=None,
         actors=[dict(G, x=980, y=880, h=450, action="point", at=("c2s25", "oğullarına", -0.3), dir=1, layer="front"),
                 dict(P.COSIMO, x=1340, y=880, h=450, action="idle", dir=-1, layer="front"),
                 dict(P.LORENZO_V, x=1530, y=870, h=430, action="idle", dir=-1, layer="back")],
         cams=[(("c2s25", -0.15), (1260, 50, 1.42)), (("c2s25", "1397'den", -0.3), (1210, 60, 1.24))],
         ovl=P.ov(P.tag("1420 · YÖNETİM OĞULLARINA", 700, 190, ("c2s25", "1420'de", -0.1), size=44),
                  P.prop_arc("book", (760, 690), (1160, 690), ("c2s25", "oğullarına", -0.2), dur=0.8, size=120, lift=90, show_from=("c2s25", -0.15)),
                  P.prop_arc("p1_anahtar", (780, 610), (1180, 620), ("c2s25", "bırakmıştı", -0.2), dur=0.7, size=90, lift=70, show_from=("c2s25", -0.15))),
         cam=("pull",), tr=("slide", 0.6, dict(dir="r")), link="dir", label="1420: yönetim oğullarına"),
    # ── 24. 1397'den o yıla kadar defterler 150 bini aşkın florin kâr gösterir ─
    shot("p1_ledger", ("c2s25", "1397'den", -0.3), head="1397 – 1420", title_l="DEBITORI", title_r="CREDITORI",
         left=[dict(text="Banka defterleri", at=("c2s25", "defterler", -0.3), hl=("c2s25", "kâr", -0.2))], right=[dict(text="Kâr", at=("c2s25", "florin", -0.4))],
         total=dict(text="1397–1420 KÂR", amt=("150.000+ fl.",), at=("c2s25", "yüz", -0.1), row=7),
         mode="day", perde=1, seed=7, focus=(780, 560),
         ovl=P.ov(P.count_up(960, 215, ("c2s25", "yüz", -0.2), 150000, dur=1.0, unit="FLORİN KÂR", size=150, bg=True, suffix="+"),
                  P.tag("DEFTERLER GÖSTERİR", 1460, 860, ("c2s25", "gösterir", -0.1), size=40)),
         cam=("pull",), tr=("sayfa", 0.6), link="material", label="defterler: 150 bini aşkın florin kâr"),
    # ── 25. 20 Şubat 1429'da öldü; Floransa takvimine göre hâlâ 1428 (ölüm döşeği: siluet, mum söner; yer/saat/tanık iddiası yok) ──
    shot("p1_oda", ("c2s26", -0.15), room="p1yatak", variant="olum", tod="dusk", mode="night", perde=1, figure="lying",
         cams=[(("c2s26", -0.15), (820, 40, 1.25)), (("c2s27", -0.2), (760, 50, 1.33))],
         ovl=P.ov(P.candle_ovl(1229, 728, 120, snuff_at=("c2s26", "öldü", -0.1)),
                  K.yil_panel(("c2s26", "20", -0.3), ("c2s26", "hâlâ", -0.2), ("c2s26", "Floransa", -0.1), x=1430, y=250)),
         cam=("push",), tr=("candle", 1.8, dict(at=(1229, 680), at_b=(960, 560))), link="light", label="20 Şubat 1429: ölüm döşeği (siluet)"),
    # ── 26. Lorenzo'nun (torununun oğlu) kaydına göre 180 bin florin ─────────
    shot("p1_medal", ("c2s27", -0.15), key="m_lorenzo", metal="bronze", pos="l", size=540, at=0.0, mode="day", perde=1,
         ovl=P.ov(P.plate("LORENZO", 1410, 330, ("c2s27", "torununun", -0.3), role="TORUNUNUN OĞLU · İLERİDE MUHTEŞEM", w=820),
                  P.count_up(1380, 640, ("c2s27", "servet", 0.15), 180000, dur=1.2, unit="FLORİN", size=170, bg=True),
                  P.tag("LORENZO'NUN KAYDINA GÖRE", 1380, 860, ("c2s27", "kaydına", 0.0), size=38)),   # TEMSİLÎ damgası motorda (1438 öncesi madalya; cilt_medal v3)
         cam=("pan", "r"), tr=("light", 0.8, dict(at=(500, 500))), link="light", label="Lorenzo'nun kaydına göre 180 bin florin"),
    # ── 27. son sözler iki kalemden, iki biçimde ─────────────────────────────
    shot("c2_kalemler", ("c2s28", -0.15), mode="day", perde=1, left_at=("c2s28", "kalemden", -0.4), right_at=("c2s28", "iki", 1, -0.1),
         write_a=("c2s28", "kalemden", -0.1), write_b=("c2s28", "iki", 1, 0.1),
         cam=("truck", "r"), tr="cut", link="audio", label="iki kalem, iki biçim"),
    # ── 28. Machiavelli bir asra yakın sonra onun (Giovanni'nin) ağzından oğullarına bir konuşma yazar: rulo yazarın masasından yaşlı adamın ağzına uzar ──
    shot("c1_machiavelli", ("c2s29", -0.15), mode="day", perde=1, rebel_who="old", rebel_at=("c2s29", "onun", -0.3),
         scroll_at=("c2s29", "konuşma", -0.4), scroll_to=("c2s29", "yazar", 0.6),
         ovl=P.plate("MACHIAVELLİ", 620, 170, ("c2s29", "Machiavelli", -0.2), role="BİR ASRA YAKIN SONRA", w=700),
         cam=("push",), tr=("slide", 0.4, dict(dir="r")), link="dir", label="Machiavelli yazar: onun ağzından"),
    # ── 29. ...huzurla gidiyordur; kıskançlık istediğinden doğar — ölüm döşeği, iki oğul (ANEKDOT, Machiavelli'ye göre) ──
    shot("p1_oda", ("c2s29", "huzurla", -0.4), room="p1yatak", variant="olum", tod="dusk", mode="night", perde=1, figure="lying",
         actors=[dict(P.COSIMO, x=780, y=880, h=430, action="idle", sil=True, dir=-1, rim_dir=-1, layer="front"),
                 dict(P.LORENZO_V, x=930, y=878, h=420, action="idle", sil=True, dir=-1, rim_dir=-1, layer="front")],
         cams=[(("c2s29", "huzurla", -0.4), (700, 50, 1.30)), (("c2s30", -0.3), (740, 60, 1.38))],
         ovl=P.ov(K.tomar(560, 470, ("c2s29", "huzurla", -0.1), ("c2s29", "doğar", 0.0), w=560, dirn=1, lines=4),
                  P.tag("MACHIAVELLİ'YE GÖRE", 640, 200, ("c2s29", "huzurla", -0.3), size=40),
                  anim.stamp_ovl("ANEKDOT", 1460, 300, ("c2s29", "kıskançlık", 0.0), "ink", rot=-0.06, size=56)),
         cam="hand", tr="cut", link="audio", label="ölüm döşeği konuşması (ANEKDOT)"),
    # ── 30a. Cavalcanti 1440'larda, olaya daha yakın bir kalemle (yazı odası) ─
    shot("p1_oda", ("c2s30", -0.15), room="calisma", variant="hucre", tod="day", mode="day", perde=1, figure=None, lamp_day=0.6,
         actors=[dict(kind="soylu", seed=44, x=946, y=823, h=280, action="write", seated=True, dir=1)],
         cams=[(("c2s30", -0.15), (1100, 20, 1.20)), (("c2s30", "kimse", -0.3), (1170, 56, 1.48))],
         ovl=P.ov(P.plate("CAVALCANTI", 620, 170, ("c2s30", "Cavalcanti", -0.2), role="1440'LARDA · OLAYA DAHA YAKIN", w=760)),
         cam=("push",), tr=("light", 0.5, dict(at=(1200, 560))), link="light", label="Cavalcanti yazar"),
    # ── 30b. ...kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli — Cavalcanti'nin sayfası yazılır (vuruş kartı; ANEKDOT) ──
    shot("c2_kalemler", ("c2s30", "kimse", -0.3), mode="day", perde=1, only="b", right_at=("c2s30", "kimse", -0.6), write_b=("c2s30", "kimse", -0.2), stamp_at=("c2s30", "kederlenmemeli", -0.4),
         cam=[(("c2s30", "kimse", -0.3), (-330, 0, 1.18, 0)), (("c2s31", -0.2), (-300, 10, 1.30, 0))],
         ovl=P.tag("CAVALCANTI'YE GÖRE", 600, 200, ("c2s30", "kimse", 0.0), size=40),
         tr="cut", link="cam", label="Cavalcanti'nin sayfası (ANEKDOT)"),
    # ── 31. hangisi gerçekten söylendi, bilmiyoruz ───────────────────────────
    shot("c2_kalemler", ("c2s31", -0.15), mode="day", perde=1, left_at=("c2s31", -0.6), right_at=("c2s31", -0.6), write_a=("c2s29", -0.5), write_b=("c2s30", "başka", -0.3), q_at=("c2s31", "bilmiyoruz", -0.6),
         cam=("pull",), tr=("slide", 0.35, dict(dir="r")), link="dir", label="hangisi söylendi: bilmiyoruz"),
    # ── 32. Machiavelli onu yoksulun ihtiyacını kimse istemeden giderirken çizer (Giovanni verir) ──
    shot("c2_sadaka", ("c2s32", -0.15), mode="day", perde=1, who_at=("c2s32", "Machiavelli", -0.2), give_at=("c2s32", "yoksulun", -0.35), stamp_at=("c2s32", "çizer", -0.2),
         cam=("truck", "r"), tr=("slide", 0.6, dict(dir="r")), link="dir", label="yoksulun ihtiyacı (Giovanni; ANEKDOT)"),
    # ── 33. Ama o kalem Medici'nin siparişiyle çalışıyordu — Machiavelli'nin odası (yakın), Medici mührü düşer ──
    shot("p1_oda", ("c2s33", -0.15), room="calisma", variant="kutuphane", tod="day", mode="day", perde=1, figure=None,
         actors=[dict(P.MACHIAVELLI, x=1366, y=823, h=280, action="write", seated=True, dir=1)],
         cams=[(("c2s33", -0.15), (1500, 70, 1.55)), (("c2s34", -0.2), (1470, 64, 1.48))],
         ovl=P.ov(P.tag("O KALEM", 620, 200, ("c2s33", "kalem", -0.3), size=46),
                  P.seal_drop(1360, 430, ("c2s33", "siparişiyle", -0.1), r=110, label="MEDİCİ SİPARİŞİ")),
         cam=("pull",), tr="cut", link="audio", label="o kalem Medici'nin siparişiyle çalışıyordu"),
    # ── 34. Giovanni öldüğünde oğlu Cosimo kırk yaşına yaklaşıyordu ─────────
    shot("p1_medal", ("c2s34", -0.15), key="m_cosimo", metal="bronze", pos="l", size=640, at=0.0, mode="night", perde=1,
         ovl=P.ov(P.plate("COSIMO", 1380, 330, ("c2s34", "Cosimo", -0.15), role="GIOVANNI'NİN OĞLU", w=700),
                  P.count_up(1380, 640, ("c2s34", "Cosimo", 0.1), 39, dur=1.0, unit="YAŞINDAYDI", size=190, bg=True, unit_size=40),
                  P.tag("1389 DOĞUMLU", 1380, 850, ("c2s34", "kırk", -0.4), size=38)),   # TEMSİLÎ damgası motorda (1438 öncesi madalya)
         cam=("push",), tr=("iris", 0.9, dict(obj="seal", at=(500, 500), r=320)), link="shape", label="Cosimo: kırk yaşına yaklaşıyordu"),
    # ── 35. KAPI: şehrin en yüksek kulesinde bir hücre — sessiz, ağır (crane up; desatürasyon; END_HOLD motor) ──
    shot("p1_sehir", ("c2s35", -0.15), scene="skyline_dikey", tod="day", mode="day", perde=1,
         cams=[(("c2s35", -0.15), (1120, 2900, 1.08)), (("c2s35", "kulesinde", 0.0), (1120, 3700, 1.02)), (("c2s35", "kapatılacaktı", 0.4), (1120, 4160, 1.0))],
         ovl=P.ov(P.desat(("c2s35", "şehrin", -0.1), ("c2s35", "kapatılacaktı", 0.3), k_max=0.75, dark=0.62, tint="#4A5068", tint_a=0.14),
                  P.glint(960, 520, ("c2s35", "hücreye", 0.0), r=70, dur=2.0, alpha=0.5)),
         cam=("crane", "up", 300), tr=("light", 1.6, dict(at=(960, 520))), link="light", label="kapı: şehrin en yüksek kulesi"),
]
YIL_AT = [(("c2s11", "1402'de", -0.1), 1402), (("c2s15", "papa", -0.1), 1410), (("c2s16", "1415'te", -0.1), 1415), (("c2s18", "öldü", -0.1), 1419),
          (("c2s21", "1422'den", -0.1), 1422), (("c2s22", "1427'de", -0.1), 1427), (("c2s25", "1420'de", -0.1), 1420),
          (("c2s26", "1429'da", -0.1), 1429)]
