"""c2 — Defterin Sihri (1397–1429). Parça 1, 3/3 · PARÇA KAPANIŞI. Gerçek ses (v2 yaması). Yönetmen kartı: yonetmen_c2.md.

KURUL TUR 1 (4 Kasım): "kart vadisi" (403–589 sn) dünya/figür sahnelerine çevrildi. Giovanni = tekrar eden İNSAN ÇAPASI (kit banker seed 5:
koyu kızıl cüppe; c1 sonu banka köşesi → c2 açılış → Cossa'ya borç → Martinus'un tahtı → Signoria → oğullarına devir → ölüm döşeği → sadaka).
KURUL TUR 2 (5 Kasım, SCN-2): "DEFTER DÜNYADIR" — şema/infografik kartları masadaki açık deftere taşındı (c2_masa: İZ · KASA · CATASTO; aynı kartta
sıçrayan kesme yok, tek sürekli kamera, el + tüy kalem); nesne/el yakın planları (c2_yakin: kese · mitra · kalem); yer başına set farkı (Brugge Flaman,
papalık anahtar-tiara kumaşı, Konstanz kartallı, kâtip odası, Catasto dairesi, Stinche hücresi); ışık patlaması c2'de 2 (bölüm açılışı + kapı).
Kurallar: ardışık kart ≤3 · dünya çekimi ≤35 sn arayla · ardışık itme ≤3 · sert kesme ≈%35 (tr="cut") · geçiş süresi 0,35–1,8 sn.
Mizah (c2): faiz yasağı ↔ kambiyo ↔ vicdan komitesi; "faiz değil hediye"; "eski papa"; çifte kayıt miti. KAPALI: ölüm (siluet + mum), Cossa'nın esareti.
Kapı: "...bir hücreye kapatılacaktı." → Palazzo Vecchio kulesinde yavaş crane up, sessiz ve ağır (END_HOLD motor; bitiş ekranı Program'dan).
"""
import math

import skia

import anim
from shots import shot
import cilt_medici as CM
import p1_ortak as P
import c0_kinds as K0
import c1_kinds as K1
import c2_kinds as K
from sk import H, W, clamp, ease_io, smooth

G = P.GIOVANNI
BANKA = dict(room="p1banka", tod="day", mode="day", perde=1)
CAVALCANTI = dict(kind="soylu", seed=44, robe="#4E5A52", robe2="#2E3832", hat_col="#4A3424")   # SA2-Y9: Machiavelli'nin sarı-mavisinden AYRI (solgun gri-yeşil)


def light_sweep(a, b, alpha=0.20, col="#FFE6B0", w=420):
    """Zamanın akışı (C3, 'bir asra yakın sonra'): pencere ışığı sahnenin üstünden soldan sağa süpürür (ekran uzayı, yumuşak)."""
    def fn(cx):
        ta, tb = cx.at(a), cx.at(b)
        u = (cx.t - ta) / max(0.3, tb - ta)
        if u <= 0 or u >= 1:
            return
        e = ease_io(u, 1.3)
        x = -w + (W + 2 * w) * e
        k = math.sin(math.pi * u)
        pth = skia.Path()
        pth.moveTo(x - w * 0.5, 0); pth.lineTo(x + w * 0.5, 0); pth.lineTo(x + w * 0.5 - 300, H); pth.lineTo(x - w * 0.5 - 300, H); pth.close()
        p = cx.f.paint(col, alpha=alpha * k, blend=skia.BlendMode.kScreen, blur=60)
        cx.f.c.drawPath(pth, p)
    return fn


def stamp_hold(text, x, y, until, rot=-0.06, size=54):
    """Önceki çekimdeki damga kesmeden sonra AYNI ekran yerinde bir süre daha durur ve söner (KA2-D8: ≥2 sn okunur)."""
    def fn(cx):
        a = 1.0 - smooth(clamp((cx.t - cx.at(until)) / 0.4))
        if a > 0.003:
            CM.stamp(cx.f, text, x, y, rot=rot, size=size, alpha=a, t=1.0)
    return fn


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
    # ── 2a. Brugge (Flaman salonu: kanal manzaralı haç kasalı pencere, soğuk kuzey ışığı, dama taş) — 'klasik bir örnek' ──
    shot("p1_oda", ("c2s3", -0.15), room="salon", variant="brugge", tod="day", mode="day", perde=1, map_at=("c2s3", "Barselona'ya", -0.3),
         actors=[dict(kind="banker", seed=52, x=1150, y=870, h=440, action="talk", dir=1, layer="front", phase=0.2),
                 dict(kind="tuccar", seed=8, x=1560, y=870, h=440, action="idle", dir=-1, layer="front")],
         cams=[(("c2s3", -0.15), (1500, 20, 1.12)), (("c2s3", "Brugge'de", 0.0), (1380, 60, 1.30)), (("c2s3", "parayı", -0.3), (1365, 66, 1.38))],
         ovl=P.ov(P.plate("BRUGGE", 560, 160, ("c2s3", "Klasik", 0.0), role="KLASİK BİR ÖRNEK", w=560),
                  P.icon_at("p1_kese", 727, 690, ("c2s3", "Brugge'de", 0.2), size=110, metal="bronze", bob=3)),
         cam=("push",), tr=("slide", 0.7, dict(dir="r")), link="dir", label="Brugge: Flaman salonu, klasik bir örnek"),
    # ── 2b. YAKIN PLAN (≥2×, el + nesne): kese peşin verilir, karşılığında Barselona'ya çekilmiş poliçe alınır ──
    shot("c2_yakin", ("c2s3", "parayı", -0.3), scene="kese", give_at=("c2s3", "peşin", -0.15), pol_at=("c2s3", "karşılığında", 0.05), push=0.07, mode="day", perde=1,
         ovl=P.tag("BARSELONA'YA ÇEKİLMİŞ POLİÇE", 960, 190, ("c2s3", "Barselona'ya", -0.2), size=44),
         family="dunya", tr="cut", link="cam", label="yakın plan: kese elden ele, poliçe karşılığında"),
    # ── 3. Vadesi gelince tahsil; ikinci poliçeyle para geri döner; kazanç = kur farkı (BRUGGE etiketi kadrajda; BARSELONA solda, simge üstünü örtmez) ──
    shot("p1_map", ("c2s4", -0.15), mode="day", perde=1, approx=False,
         cams=[(("c2s4", -0.15), (2.7, 46.2, 1.72)), (("c2s4", "ikinci", -0.3), (2.8, 46.3, 1.80)), (("c2s4", "kazanç", -0.3), (2.8, 46.4, 1.68))],
         cities=[dict(lon=3.22, lat=51.21, name="BRUGGE", kind="capital", at=-0.5, size=36), dict(lon=2.17, lat=41.39, name="BARSELONA", kind="capital", at=-0.5, size=36, side="l")],
         routes=[dict(pts=[(3.22, 51.21), (0.9, 46.3), (2.17, 41.39)], at=("c2s4", -0.1), dur=1.0, width=7, color="#A8321E"),
                 dict(pts=[(2.17, 41.39), (5.1, 46.0), (3.22, 51.21)], at=("c2s4", "ikinci", -0.3), dur=1.6, width=7, color="#233C8C")],
         icons_=[dict(kind="scroll", lon=3.22, lat=51.21, size=84, at=("c2s4", -0.1), route=[(3.22, 51.21), (0.9, 46.3), (2.25, 41.85)], move_at=("c2s4", -0.05), move_dur=1.1, glow=0.0),
                 dict(kind="coins", lon=2.6, lat=42.2, size=96, at=("c2s4", "tahsil", -0.3), bob=4),
                 dict(kind="scroll", lon=2.17, lat=41.39, size=84, at=("c2s4", "ikinci", -0.2), route=[(2.6, 42.2), (5.1, 46.0), (3.22, 51.0)], move_at=("c2s4", "poliçeyle", -0.3), move_dur=1.4, glow=0.0),
                 dict(kind="coinbag", lon=3.6, lat=50.7, size=100, at=("c2s4", "geri", -0.1), bob=4),
                 dict(kind="coin", lon=4.6, lat=50.0, size=64, at=("c2s4", "kazanç", 0.0), bob=7),          # C3: anlatıya bağlı ikinci hareket — kazanç (kur farkı) kesenin yanında belirir, sallanır
                 dict(kind="coin", lon=4.9, lat=49.5, size=56, at=("c2s4", "kur", -0.1), bob=6)],
         ovl=P.ov(P.tag("VADESİ GELİNCE TAHSİL", 560, 250, ("c2s4", "Vadesi", -0.1), size=40, out=("c2s4", "kazanç", -0.3)),
                  P.pop_label("KUR FARKI", 1440, 250, ("c2s4", "kur", -0.1), size=84, track=10)),
         cam=("pull",), tr=("zoomthru", 0.55, dict(at=(760, 470), at_b=(960, 520))), link="scale", label="poliçe gider, para döner: kur farkı"),
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
    # ── 9. Roma şubesi zamanla sermayesiz (de Roover: sermaye 1426'da çekildi); kasayı Kilise'nin parası dolduruyordu ───
    shot("c2_kasa", ("c2s10", -0.15), mode="day", perde=1, branch_at=("c2s10", "Roma", -0.2), nocap_at=("c2s10", "sermayesiz", -0.2), church_at=("c2s10", "Kilise'nin", -0.3), fill_at=("c2s10", "kasayı", -0.1), fill_to=("c2s10", "dolduruyordu", 0.3),
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
    # ── 11. Çifte kaydı Medici'ler icat etti derler (MİT): kâtip odası (yeşil badana, göz pencereler, defter rafları) ──
    shot("p1_oda", ("c2s12", -0.15), room="salon", variant="katip", tod="day", mode="day", perde=1,
         actors=[dict(kind="banker", seed=61, x=1016, y=823, h=282, action="write", seated=True, dir=1)],
         cams=[(("c2s12", -0.15), (1270, 50, 1.36)), (("c2s13", -0.2), (1250, 56, 1.40))],
         ovl=P.ov(K.cifte_panel(("c2s12", "Çifte", 0.0), ("c2s12", "kaydı", 0.25), ("c2s12", "icat", 0.0)),
                  anim.stamp_ovl("MİT", 1640, 300, ("c2s12", "derler", 0.0), "drop", rot=-0.1, size=104)),
         cam="hand", tr="cut", link="audio", label="çifte kayıt: kâtip; MİT"),
    # ── 12. MASA · İZ (tek sürekli kamera, 15,6 sn): kâtibin defterinden masadaki deftere — sol sayfa çifte kaydın izi (Cenova 1340 …),
    #        kamera sağ sayfaya kayar: Medici'nin farkı yapıda (Floransa → Roma, Venedik). Eski #71–#73 (zaman çizgisi + iki ağ kartı) tek çekim. ──
    shot("c2_masa", ("c2s13", -0.15), v="iz", mode="day", perde=1, longtake=True, family="dunya",
         start=("c2s13", -0.15), stamp_at=("c2s13", "Etmediler", 0.1), myth_at=("c2s13", "eski", -0.6), myth_x=("c2s13", "eski", 0.05),
         events=[(1340, "CENOVA", ("c2s13", "Cenova'nın", -0.1), True), (1494, "PACİOLİ", ("c2s13", "biridir", -0.2), True)],
         head_at=("c2s14", -0.15), book_at=("c2s14", "defterde", -0.3), book_x=("c2s14", "değil", -0.1),
         nodes=[("f", ("c2s14", "yapıdaydı", -0.3)), ("r", ("c2s14", "şubenin", -0.1)), ("v", ("c2s14", "kendi", -0.1))],
         edges=[("f", "r", ("c2s14", "ortaklığı", -0.25)), ("f", "v", ("c2s14", "ortaklığı", 0.1))],
         labels=[("KENDİ ORTAKLIĞI", ("c2s14", "ortaklığı", -0.1), 870), ("KENDİ DEFTERİ", ("c2s14", "defteri", -0.15), 935)],
         cams=[(("c2s13", -0.15), (1060, 860, 0.98)), (("c2s13", "Cenova'nın", 0.0), (880, 845, 1.12)), (("c2s13", "1340", 0.3), (820, 850, 1.20)),
               (("c2s13", "eski", -0.4), (900, 845, 1.10)), (("c2s13", "biridir", 0.35), (1040, 860, 1.02)), (("c2s14", "farkı", 0.0), (1620, 870, 1.10)),
               (("c2s14", "yapıdaydı", 0.0), (1690, 880, 1.14)), (("c2s14", "her", 0.0), (1690, 895, 1.04)), (("c2s14", "vardı", 0.5), (1680, 900, 1.08))],
         tr=("zoomthru", 0.6, dict(at=(1410, 520), at_b=(960, 540))), link="scale", label="masa · iz: Cenova 1340 → yapı (tek kamera)"),
    # ── 14. Giovanni Cossa'ya borç verir; adam XXIII. Johannes adıyla papa olur (BEYAZ tiara, altın taçlar) — levhalar çakışmaz (GIOVANNI solda-aşağıda) ──
    shot("p1_oda", ("c2s15", -0.15), room="p1ofis", variant="ofis", tod="day", mode="day", perde=1, figure=None,
         actors=[dict(G, x=1000, y=880, h=460, action="talk", dir=1, layer="front"),
                 dict(kind="kardinal", seed=9, x=1400, y=880, h=460, action="idle", dir=-1, layer="front")],
         cams=[(("c2s15", -0.15), (1150, 50, 1.25)), (("c2s15", "borç", 0.0), (1200, 60, 1.32)), (("c2s15", "papa", 0.0), (1330, 40, 1.46))],
         ovl=P.ov(P.plate("GİOVANNİ", 420, 410, ("c2s15", "Giovanni", -0.2), w=420, out=("c2s15", "adam", 0.0)),
                  P.plate("BALDASSARRE COSSA", 900, 190, ("c2s15", "Baldassarre", -0.2), role="KİLİSE ADAMI", w=740, out=("c2s15", "XXIII.", -0.3)),
                  P.prop_arc("p1_kese", (803, 697), (1143, 697), ("c2s15", "borç", -0.1), dur=0.8, size=110, lift=110, show_from=("c2s15", "Giovanni", 0.0), metal="bronze"),
                  P.prop_arc(P.tiara_draw, (1061, 200), (1061, 452), ("c2s15", "adıyla", 0.0), dur=0.9, size=150, lift=0, show_from=("c2s15", "adıyla", -0.3), glow=True),
                  P.plate("COSSA = XXIII. JOHANNES", 900, 190, ("c2s15", "XXIII.", -0.1), role="PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR", w=870)),
         cam=("truck", "r"), tr=("zoomthru", 0.6, dict(at=(1050, 361), at_b=(803, 697))), link="scale", label="Giovanni → Cossa: borç; papa (tiara)"),
    # ── 15. 1415: Konstanz Konsili onu indirdi — imparatorluk kartallı kumaşlar, açık meşe; taç düşer (sola: düşüş) ──
    shot("p1_oda", ("c2s16", -0.15), room="p1salon", variant="konstanz", tod="day", mode="day", perde=1,
         actors=[dict(kind="kardinal", seed=31, x=1230, y=870, h=420, action="idle", dir=1, layer="front"),
                 dict(kind="rahip", seed=32, x=1360, y=860, h=400, action="idle", dir=1, layer="back"),
                 dict(kind="rahip", seed=33, x=2060, y=860, h=400, action="idle", dir=-1, layer="back"),
                 dict(kind="kardinal", seed=35, x=2190, y=870, h=420, action="point", at=("c2s16", "indirdi", -0.3), dir=-1, layer="front")],
         cams=[(("c2s16", -0.15), (1720, 30, 1.18)), (("c2s16", "indirdi", 0.0), (1600, 50, 1.26))],
         ovl=P.ov(P.tag("KONSTANZ KONSİLİ · 1415", 640, 190, ("c2s16", "Konstanz", -0.3), size=46),
                  P.prop_arc(P.tiara_draw, (1000, 650), (720, 960), ("c2s16", "indirdi", -0.25), dur=0.9, size=130, lift=-40, show_from=("c2s16", -0.15), rot1=-1.2),
                  anim.impact_ovl(("c2s16", "indirdi", 0.6), amp=4)),
         cam=("pan", "l"), tr="cut", link="audio", label="Konstanz 1415: taht boş, taç düşer"),
    # ── 16. kefalet mi fidye mi: kaynaklar ayrışıyor (HUD 1418: kurtuluş 1418 / fidye 1419, DBI) ──
    shot("c2_ayrim", ("c2s17", -0.15), mode="day", perde=1, walk_at=("c2s17", "İndirilen", -0.1), fork_at=("c2s17", "Giovanni'nin", -0.3), left_at=("c2s17", "kefaletle", -0.25), right_at=("c2s17", "fidyeyle", -0.25), stamp_at=("c2s17", "ayrışıyor", -0.3),
         cam=("pan", "r"), tr="cut", link="audio", label="kefalet mi fidye mi: yol ayrımı"),
    # ── 17a. Vaftizhane anıtı: Latince yazıt "IOANNES QVONDAM PAPA" oyulur; Türkçesi levhada (ÇEVİRİ BİZE AİT). Ölüm: mum geçişi ──
    shot("c2_mezar", ("c2s18", -0.15), mode="day", perde=1, place_at=("c2s18", "Vaftizhane'ye", -0.3), carve_at=("c2s18", "mezarına", -0.1), carve_to=("c2s18", "papa", 0.3),
         ovl=P.tag("ESKİ PAPA · ÇEVİRİ BİZE AİT", 960, 372, ("c2s18", "eski", -0.15), size=44),
         cam=("tilt", "up", 120), tr=("candle", 1.0, dict(at=(960, 560), at_b=(440, 820))), link="light", label="Cossa'nın anıtı: IOANNES QVONDAM PAPA"),
    # ── 17b. Papa V. Martinus itiraz etti (papalık salonu: anahtar-tiara kumaşı, beyaz-altın perde; İTİRAZ damgası figürün DIŞINDA) ─────
    shot("p1_oda", ("c2s19", -0.15), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="point", at=("c2s19", "itiraz", -0.25), dir=-1, layer="back")],
         cams=[(("c2s19", -0.15), (1560, 40, 1.30)), (("c2s19", "Yazıt", 0.0), (1590, 46, 1.36))],
         ovl=P.ov(P.tag("V. MARTİNUS", 520, 220, ("c2s19", "Martinus", -0.3), size=48),
                  anim.stamp_ovl("İTİRAZ", 520, 440, ("c2s19", "itiraz", 0.15), "spin", rot=-0.10, size=76)),
         cam=("push",), tr="cut", link="audio", label="V. Martinus itiraz eder"),
    # ── 17c. Yazıt kaldı (aynı anıt, parıltı; Latince yazıt + Türkçesi) ────────
    shot("c2_mezar", ("c2s19", "Yazıt", -0.15), mode="day", perde=1, carve_at=("c2s18", "mezarına", -0.1), carve_to=("c2s18", "papa", 0.3), stay_at=("c2s19", "Yazıt", 0.0),
         ovl=P.tag("ESKİ PAPA · ÇEVİRİ BİZE AİT", 960, 372, ("c2s18", "eski", -0.15), size=44),
         cam=("tilt", "up", 130), tr="cut", link="cam", label="yazıt kaldı"),
    # ── 18a. kaynak: de Roover'ın andığı arşiv belgeleri (BELGE); damga erken basılır ve sonraki çekimde de durur (KA2-D8: ≥2 sn) ──
    shot("c2_rivayet", ("c2s20", -0.15), mode="day", perde=1, medal=False, pawn_at=("c2s20", "belgelere", -0.2), pawn_label="BORÇ KARŞILIĞI",
         ovl=P.ov(P.plate("DE ROOVER", 600, 170, ("c2s20", "De", -0.25), role="ANDIĞI ARŞİV BELGELERİ", w=640),
                  anim.stamp_ovl("BELGE · DE ROOVER", 600, 400, ("c2s20", "De", 0.35), "drop", rot=-0.06, size=50)),
         cam=("tilt", "down", 130), tr=("sayfa", 0.5), link="material", label="belge (de Roover): mitra borç karşılığı"),
    # ── 18b. Martinus mitrayı geri ister (papalık salonu; Giovanni elinde mitra) ─────────────────
    shot("p1_oda", ("c2s20", "Martinus", -0.3), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="point", at=("c2s20", "geri", -0.3), dir=-1, layer="back"),
                 dict(G, x=1180, y=890, h=470, action="idle", dir=1, layer="front", prop="mitra")],     # mitra Giovanni'nin elinde (SA1 tur 3 N1)
         cams=[(("c2s20", "Martinus", -0.3), (1330, 10, 1.02)), (("c2s20", "mitrayı", -0.25), (1345, 12, 1.05))],
         ovl=P.ov(stamp_hold("BELGE · DE ROOVER", 600, 400, ("c2s20", "Cossa'nın", 0.3), size=50),
                  P.tag("BORÇ KARŞILIĞI BIRAKILAN MİTRA", 760, 200, ("c2s20", "borca", -0.2), size=40)),
         cam=("push",), tr="cut", link="audio", label="Martinus mitrayı geri ister"),
    # ── 18b'. YAKIN PLAN (≥2×): rehin mitra Giovanni'nin elinde; papalık eli uzanır ("geri almak için") ──
    shot("c2_yakin", ("c2s20", "mitrayı", -0.25), scene="mitra", reach_at=("c2s20", "geri", -0.25), push=0.05, mode="day", perde=1,
         family="dunya", tr="cut", link="cam", label="yakın plan: rehin mitra, papalık eli"),
    # ── 18c. aforoz tehdidi (yakın iki kişilik; sert kesme; 18b'ye göre ≥1,5× yakın). Papa mühürlü belgeyi kaldırır (şiddet jesti YOK; kurul tur 2 AN1-Y1/AN2-E1) ──
    shot("p1_oda", ("c2s20", "Giovanni'yi", -0.3), room="p1salon", variant="papa", tod="day", mode="day", perde=1,
         actors=[dict(kind="papa", seed=7, x=1640, y=689, h=440, action="admonish", at=("c2s20", "aforozla", -0.45), dir=-1, layer="back"),
                 dict(G, x=1180, y=890, h=470, action="bow", at=("c2s20", "tehdit", 0.0), dir=1, layer="front", prop="mitra")],   # eğilirken mitra elde kalır (SA1 tur 3 N1)
         cams=[(("c2s20", "Giovanni'yi", -0.3), (1400, 0, 1.55)), (("c2s21", -0.2), (1380, 6, 1.62))],
         ovl=P.ov(P.tag("AFOROZ TEHDİDİ", 960, 140, ("c2s20", "aforozla", 0.1), size=56, dur=0.25),
                  anim.impact_ovl(("c2s20", "aforozla", 0.2), amp=3)),
         cam=("push",), tr="cut", link="cam", label="aforoz tehdidi (belgeli)"),
    # ── 19. MASA · KASA (tek çekim, 10,6 sn): papalık kasası (kızıl kadife) — bir el anahtarları deftere bırakır; sağ sayfada 1422'den
    #        22 YIL düz mürekkep şerit dolar, + 18 YIL kesikli; MEDİCİ'DE KALDI. Eski #83–#85 (üç anahtar kartı, iki sıçrayan kesme) tek çekim. ──
    shot("c2_masa", ("c2s21", -0.15), v="kasa", mode="day", perde=1, family="dunya",
         head_at=("c2s21", -0.1), head2_at=("c2s21", "kasa", -0.3), start_at=("c2s21", "1422'den", -0.2), a_at=("c2s21", "yirmi", -0.1), b_at=("c2s21", "ardından", -0.1),
         medici_at=("c2s21", "Medici'de", -0.2),
         keys=dict(in_at=("c2s21", "resmî", -0.2), put_at=("c2s21", "memurluğu", 0.1), size=360, **{"from": (2300.0, 250.0), "to": (905.0, 900.0)}),
         hand=dict(ang=205.0, size=230, sleeve="#6E1C1E", cuff="#C9A23A", flip=True),
         cams=[(("c2s21", -0.15), (1300, 860, 0.92)), (("c2s21", "memurluğu", 0.0), (1060, 880, 1.08)), (("c2s21", "1422'den", -0.2), (1120, 880, 1.04)),
               (("c2s21", "sonra", 0.1), (1640, 880, 1.14)), (("c2s21", "ardından", 0.0), (1690, 880, 1.20)), (("c2s21", "Medici'de", 0.0), (1480, 880, 1.00)),
               (("c2s22", -0.2), (1460, 875, 0.97))],
         tr="cut", link="audio", label="masa · kasa: el anahtarları bırakır; 22 + 18 yıl"),
    # ── 20. 1427: CATASTO dairesi — hane reisleri yazılı beyannamelerini (portata) masaya getirir; görevliler yazar (kapı kapı DEĞİL; KA1/KA2/SA2-Y6).
    #        Gün ışığında renkli figürler (simsiyah siluet yaya yok). ──
    shot("p1_oda", ("c2s22", -0.15), room="salon", variant="catasto", tod="day", mode="day", perde=1,
         actors=[dict(kind="banker", seed=61, x=1016, y=823, h=282, action="write", seated=True, dir=1),
                 dict(kind="banker", seed=62, x=2384, y=823, h=282, action="write", seated=True, dir=-1, rim_dir=-1),
                 dict(kind="tuccar", seed=9, x=1300, y=880, h=430, action="bow", at=("c2s22", "tek", -0.3), dur=1.2, depth=12.0, dir=-1, layer="front", prop="book"),
                 dict(kind="halk", seed=3, x=2350, y=884, h=420, walk=(1640, 70), walk_at=("c2s22", -0.15), dir=-1, layer="front", prop="book"),
                 dict(kind="soylu_f", seed=6, x=2700, y=878, h=400, walk=(1900, 66), walk_at=("c2s22", "Floransa", -0.2), dir=-1, layer="front", prop="book"),
                 dict(kind="soylu", seed=14, x=3050, y=882, h=420, walk=(2150, 72), walk_at=("c2s22", "servetini", -0.3), dir=-1, layer="front", prop="book")],
         cams=[(("c2s22", -0.15), (1300, 40, 1.15)), (("c2s22", "yazdırdı", 0.0), (1520, 50, 1.20)), (("c2s23", -0.2), (1680, 56, 1.24))],
         ovl=P.ov(P.tag("CATASTO · 1427", 560, 200, ("c2s22", "1427'de", -0.2), size=48),
                  P.tag("HANE REİSLERİNİN BEYANNAMESİ · PORTATA", 1060, 300, ("c2s22", "yazdırdı", -0.2), size=36)),
         cam=("truck", "r"), tr=("slide", 0.5, dict(dir="r")), link="dir", label="catasto dairesi: beyanname getiren hane reisleri"),
    # ── 21. MASA · CATASTO (tek çekim, 9,2 sn): görevlilerin masasındaki kayıt defteri — 9.780 hane ızgarası yazılır, 137 hane altın;
    #        ALT KENARDA %29,8 mürekkep şeridi (BİR HESABA GÖRE); kamera sağ sayfaya: PALLA STROZZİ · 163.000. Eski #87–#89 montaj kartları tek çekim. ──
    shot("c2_masa", ("c2s23", -0.15), v="catasto", mode="day", perde=1, family="dunya",
         start=("c2s23", -0.15), fill_at=("c2s23", -0.1), fill_to=("c2s23", "hane", 0.0), h137_at=("c2s23", "yüz", -0.2),
         bar_at=("c2s23", "kayıtlı", -0.3), fill_bar_at=("c2s23", "yüzde", -0.3), stamp_at=("c2s23", "kayıtlı", 0.2),
         name_at=("c2s23", "Palla", -0.5), role_at=("c2s23", "en", -0.1), num_at=("c2s23", "zengini", -0.05),
         cams=[(("c2s23", -0.15), (1000, 870, 1.00)), (("c2s23", "hane", 0.0), (900, 880, 1.10)), (("c2s23", "kayıtlı", 0.1), (900, 1040, 1.22)),
               (("c2s23", "tutuyordu", 0.0), (920, 1030, 1.18)), (("c2s23", "zengini", 0.0), (1680, 900, 1.12)), (("c2s24", -0.2), (1700, 900, 1.17))],
         tr="cut", link="cam", label="masa · catasto: 9.780 hane, %29,8 kenarda, Strozzi"),
    # ── 22. Giovanni sayımın yürürlüğe girmesini destekledi (Signoria salonu) ──
    shot("p1_oda", ("c2s24", -0.15), room="salon", variant="signoria", tod="day", mode="day", perde=1,
         actors=[dict(kind="soylu", seed=11, x=1016, y=823, h=282, action="listen", seated=True, dir=1),
                 dict(kind="soylu", seed=14, x=2384, y=823, h=282, action="listen", seated=True, dir=-1, rim_dir=-1),
                 dict(G, x=1700, y=885, h=460, action="talk", dir=-1, layer="front")],
         cams=[(("c2s24", -0.15), (1640, 50, 1.26)), (("c2s25", -0.2), (1680, 60, 1.32))],
         ovl=P.ov(P.tag("GİOVANNİ · CATASTO'YU DESTEKLEDİ", 760, 200, ("c2s24", "Giovanni", -0.1), size=42),
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
    # ── 24. 1397'den o yıla kadar defterler 150 bini aşkın florin kâr gösterir (sayaç yuvarlak adımlarla; "+" yalnız son değerde — KA2-D10) ─
    shot("p1_ledger", ("c2s25", "1397'den", -0.3), head="1397 – 1420", title_l="DEBITORI", title_r="CREDITORI",
         left=[dict(text="Banka defterleri", at=("c2s25", "defterler", -0.3), hl=("c2s25", "kâr", -0.2))], right=[dict(text="Kâr", at=("c2s25", "florin", -0.4))],
         total=dict(text="1397–1420 KÂR", amt=("150.000+ fl.",), at=("c2s25", "yüz", -0.1), row=7),
         mode="day", perde=1, seed=7, focus=(780, 560),
         ovl=P.ov(P.count_up(960, 215, ("c2s25", "yüz", -0.35), 150000, dur=0.9, unit="FLORİN KÂR", size=150, bg=True, suffix="+", step=5000, suffix_final=True),
                  P.tag("DEFTERLER GÖSTERİR", 1460, 860, ("c2s25", "gösterir", -0.1), size=40)),
         cam=("pull",), tr=("sayfa", 0.6), link="material", label="defterler: 150 bini aşkın florin kâr"),
    # ── 25. 20 Şubat 1429'da öldü; Floransa takvimine göre hâlâ 1428 (ölüm döşeği: siluet, mum söner; yer/saat/tanık iddiası yok) ──
    shot("p1_oda", ("c2s26", -0.15), room="p1yatak", variant="olum", tod="dusk", mode="night", perde=1, figure="lying",
         cams=[(("c2s26", -0.15), (820, 40, 1.25)), (("c2s27", -0.2), (760, 50, 1.33))],
         ovl=P.ov(P.candle_ovl(1229, 728, 120, snuff_at=("c2s26", "öldü", -0.1)),
                  K.yil_panel(("c2s26", "20", -0.3), ("c2s26", "hâlâ", -0.2), ("c2s26", "Floransa", -0.1), x=1430, y=250)),
         cam=("push",), tr=("candle", 1.2, dict(at=(1229, 680), at_b=(960, 560))), link="light", label="20 Şubat 1429: ölüm döşeği (siluet)"),
    # ── 26. Lorenzo'nun (torununun oğlu) kaydına göre 180 bin florin (zaman uçurumu: dip) ─────────
    shot("p1_medal", ("c2s27", -0.15), key="m_lorenzo", metal="bronze", pos="l", size=540, at=0.0, mode="day", perde=1,
         ovl=P.ov(P.plate("LORENZO", 1410, 330, ("c2s27", "torununun", -0.3), role="TORUNUNUN OĞLU · İLERİDE MUHTEŞEM", w=820),
                  P.count_up(1380, 640, ("c2s27", "servet", 0.15), 180000, dur=1.2, unit="FLORİN", size=170, bg=True, step=5000),
                  P.tag("LORENZO'NUN KAYDINA GÖRE", 1380, 860, ("c2s27", "kaydına", 0.0), size=38)),   # TEMSİLÎ damgası motorda (1438 öncesi madalya; cilt_medal v3)
         cam=("pan", "r"), tr=("dip", 0.8), link="light", label="Lorenzo'nun kaydına göre 180 bin florin"),
    # ── 27. son sözler iki kalemden, iki biçimde — sayfalar İLK karede hazır (ölü açılış yok); kaynağın kendi sözleri soluk el yazısıyla akar ──
    shot("c2_kalemler", ("c2s28", -0.15), mode="day", perde=1, write_a=("c2s28", "kalemden", -0.1), write_b=("c2s28", "iki", 1, 0.1),
         cam=("truck", "r"), tr="cut", link="audio", label="iki kalem, iki biçim"),
    # ── 28. Machiavelli bir asra yakın sonra onun (Giovanni'nin) ağzından oğullarına bir konuşma yazar: rulo yazarın masasından yaşlı adamın ağzına uzar;
    #        ikinci sürekli hareket (C3): "bir asra yakın sonra" — pencere ışığı sahneyi süpürür (zaman akar) ──
    shot("c1_machiavelli", ("c2s29", -0.15), mode="day", perde=1, rebel_who="old", rebel_at=("c2s29", "onun", -0.3),
         scroll_at=("c2s29", "konuşma", -0.4), scroll_to=("c2s29", "yazar", 0.6),
         ovl=P.ov(light_sweep(("c2s29", -0.1), ("c2s29", "onun", 0.2), alpha=0.32),
                  P.plate("MACHİAVELLİ", 620, 170, ("c2s29", "Machiavelli", -0.2), role="BİR ASRA YAKIN SONRA", w=700)),
         cam=("push",), tr=("slide", 0.4, dict(dir="r")), link="dir", label="Machiavelli yazar: onun ağzından"),
    # ── 29. ...huzurla gidiyordur; kıskançlık istediğinden doğar — ölüm döşeği, iki oğul; tomarda söz GERÇEK harflerle (anlatımla birebir; ANEKDOT) ──
    shot("p1_oda", ("c2s29", "huzurla", -0.4), room="p1yatak", variant="olum", tod="dusk", mode="night", perde=1, figure="lying",
         actors=[dict(P.COSIMO, x=780, y=880, h=430, action="idle", sil=True, dir=-1, rim_dir=-1, layer="front"),
                 dict(P.LORENZO_V, x=930, y=878, h=420, action="idle", sil=True, dir=-1, rim_dir=-1, layer="front")],
         cams=[(("c2s29", "huzurla", -0.4), (700, 50, 1.30)), (("c2s30", -0.3), (740, 60, 1.38))],
         ovl=P.ov(K.tomar(500, 500, ("c2s29", "huzurla", -0.3), ("c2s29", "huzurla", 0.3), w=700, dirn=1,
                          words=[("huzurla gidiyordur", ("c2s29", "huzurla", -0.05)), ("ve kıskançlık,", ("c2s29", "ve", -0.05)),
                                 ("insana verilenden değil,", ("c2s29", "insana", -0.05)), ("istediğinden doğar.", ("c2s29", "istediğinden", -0.05))]),
                  P.tag("MACHİAVELLİ'YE GÖRE", 640, 200, ("c2s29", "huzurla", -0.3), size=40),
                  anim.stamp_ovl("ANEKDOT", 1460, 300, ("c2s29", "kıskançlık", 0.0), "ink", rot=-0.06, size=56)),
         cam="hand", tr="cut", link="audio", label="ölüm döşeği konuşması (ANEKDOT)"),
    # ── 30a. Cavalcanti 1430'larda, HAPİSTE, olaya daha yakın bir kalemle — Stinche hücresi (taş, parmaklıklı pencere, saman şilte); ayrı kostüm ─
    shot("p1_oda", ("c2s30", -0.15), room="p1zindan", tod="day", mode="day", perde=1, figure=None, lamp_day=0.6,
         actors=[dict(CAVALCANTI, x=946, y=823, h=280, action="write", seated=True, dir=1)],
         cams=[(("c2s30", -0.15), (1100, 20, 1.20)), (("c2s30", "kimse", -0.3), (1170, 56, 1.48))],
         ovl=P.ov(P.plate("CAVALCANTİ", 620, 170, ("c2s30", "Cavalcanti", -0.2), role="HAPİSTE · 1430'LAR · OLAYA DAHA YAKIN", w=760)),
         cam=("push",), tr=("sayfa", 0.5), link="material", label="Cavalcanti yazar (Stinche hücresi)"),
    # ── 30b. ...kimse dünyevi tasaları sonsuz huzurla değiş tokuş ettiği için kederlenmemeli — sayfaya söz GERÇEK harflerle, anlatımla birebir (ANEKDOT) ──
    shot("c2_kalemler", ("c2s30", "kimse", -0.3), mode="day", perde=1, only="b", right_at=("c2s30", "kimse", -0.95), write_b=("c2s30", "kimse", -0.3), stamp_at=("c2s30", "kederlenmemeli", -0.4),
         lines_b=[("kimse dünyevi tasaları", ("c2s30", "kimse", -0.05)), ("sonsuz huzurla", ("c2s30", "sonsuz", -0.05), True),
                  ("değiş tokuş ettiği için", ("c2s30", "değiş", -0.05)), ("kederlenmemeli.", ("c2s30", "kederlenmemeli", -0.05))],
         cam=[(("c2s30", "kimse", -0.3), (380, -30, 1.08, 0)), (("c2s30", "huzurla", 0.0), (430, 0, 1.24, 0)), (("c2s31", -0.2), (470, 24, 1.40, 0))],
         ovl=P.tag("CAVALCANTİ'YE GÖRE", 560, 880, ("c2s30", "kimse", 0.0), size=40),
         tr="cut", link="cam", label="Cavalcanti'nin sayfası (ANEKDOT)"),
    # ── 31. hangisi gerçekten söylendi, bilmiyoruz — iki sayfa, iki söz yan yana (yazılmış) ───────────────────────────
    shot("c2_kalemler", ("c2s31", -0.15), mode="day", perde=1, full=True, q_at=("c2s31", "bilmiyoruz", -0.6),
         lines_a=[("huzurla gidiyordur", 0.0), ("ve kıskançlık,", 0.0), ("insana verilenden değil,", 0.0), ("istediğinden doğar.", 0.0)],
         lines_b=[("kimse dünyevi tasaları", 0.0), ("sonsuz huzurla", 0.0, True), ("değiş tokuş ettiği için", 0.0), ("kederlenmemeli.", 0.0)],
         cam=("pull",), tr=("slide", 0.35, dict(dir="r")), link="dir", label="hangisi söylendi: bilmiyoruz"),
    # ── 32. Machiavelli onu yoksulun ihtiyacını kimse istemeden giderirken çizer (Giovanni verir; derinlikli, eşit aralıksız yoksullar) ──
    shot("c2_sadaka", ("c2s32", -0.15), mode="day", perde=1, who_at=("c2s32", "Machiavelli", -0.2), give_at=("c2s32", "yoksulun", -0.35), stamp_at=("c2s32", "çizer", -0.2),
         cam=("truck", "r"), tr=("slide", 0.6, dict(dir="r")), link="dir", label="yoksulun ihtiyacı (Giovanni; ANEKDOT)"),
    # ── 33. YAKIN PLAN (≥2×, el + tüy kalem): "o kalem" eseri yazar; Medici siparişinin mührü düşer — NESNE YILI 1520: zambaklı üst top + 5 top (std) ──
    shot("c2_yakin", ("c2s33", -0.15), scene="kalem", write_at=("c2s33", -0.1), seal_at=("c2s33", "siparişiyle", -0.1), seal_label="MEDİCİ SİPARİŞİ",
         seal_year=1520, seal_variant="std", seal_x=1200, seal_y=620, push=0.0, mode="day", perde=1,
         ovl=P.tag("O KALEM", 520, 200, ("c2s33", "kalem", -0.3), size=46),
         family="dunya", tr="cut", link="audio", label="yakın plan: o kalem; Medici siparişi (1520 mührü)"),
    # ── 34. Giovanni öldüğünde oğlu Cosimo kırk yaşına yaklaşıyordu — levhalar erken (≈580,6), yaş SAYILMAZ, çıkış ≤1,0 sn (AN2-K4) ─────────
    shot("p1_medal", ("c2s34", -0.15), key="m_cosimo", metal="bronze", pos="l", size=640, at=0.0, mode="night", perde=1,
         ovl=P.ov(P.plate("COSİMO", 1380, 330, ("c2s34", "öldüğünde", 0.0), role="GİOVANNİ'NİN OĞLU", w=700),
                  P.count_up(1380, 640, ("c2s34", "oğlu", -0.1), 39, dur=0.6, unit="YAŞINDAYDI", size=190, bg=True, unit_size=40, count=False),
                  P.tag("1389 DOĞUMLU", 1380, 850, ("c2s34", "Cosimo", 0.0), size=38)),   # TEMSİLÎ damgası motorda (1438 öncesi madalya)
         cam=("push",), tr=("iris", 0.9, dict(obj="seal", at=(1200, 620), r=170)), link="shape", label="Cosimo: kırk yaşına yaklaşıyordu"),
    # ── 35. KAPI: şehrin en yüksek kulesinde bir hücre — sessiz, ağır (crane up; desatürasyon; END_HOLD motor). Işık geçişi ≤1,0 sn ──
    shot("p1_sehir", ("c2s35", -0.15), scene="skyline_dikey", tod="day", mode="day", perde=1,
         cams=[(("c2s35", -0.15), (1120, 2900, 1.08)), (("c2s35", "kulesinde", 0.0), (1120, 3700, 1.02)), (("c2s35", "kapatılacaktı", 0.4), (1120, 4160, 1.0))],   # SA1-K3 şerit = arkadaki çan kulesinin kule kenarından taşan dilimi (yatay paralaks yok → kamera x çözmez; SCN-1 isteği: cilt_sehir SkylineDikey XD)
         ovl=P.ov(P.desat(("c2s35", "şehrin", -0.1), ("c2s35", "kapatılacaktı", 0.3), k_max=0.75, dark=0.62, tint="#4A5068", tint_a=0.14),
                  P.glint(960, 520, ("c2s35", "hücreye", 0.0), r=70, dur=2.0, alpha=0.5)),
         cam=("crane", "up", 300), tr=("light", 1.0, dict(at=(960, 520))), link="light", label="kapı: şehrin en yüksek kulesi"),
]
YIL_AT = [(("c2s11", "1402'de", -0.1), 1402), (("c2s15", "papa", -0.1), 1410), (("c2s16", "1415'te", -0.1), 1415), (("c2s17", -0.1), 1418),
          (("c2s18", "öldü", -0.1), 1419), (("c2s21", "1422'den", -0.1), 1422), (("c2s22", "1427'de", -0.1), 1427), (("c2s25", "1420'de", -0.1), 1420),
          (("c2s26", "1429'da", -0.1), 1429)]
