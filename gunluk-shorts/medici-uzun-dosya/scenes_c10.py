from shots import shot
from sk import ease_out
import cilt_medici as CM
import p5_lib as L
import c10_kinds as K
look = L.look
from cilt_sehir import DOOR_X, YG
CAMS_A = [(("c10s13", -0.1), (2700, 60, 1.0)), (("c10s14", "Palazzo", 0.0), (3150, 70, 1.12)), (("c10s15", -0.55), (3380, 86, 1.28))]
CAMS_B = [(("c10s15", -0.55), (3380, 86, 1.28)), (("c10s16", 0.0), (3500, 92, 1.38)), (("c10s17", -0.1), (3520, 96, 1.42))]
CAMS_C = [(("c10s17", -0.1), (3520, 96, 1.42)), (("c10s17", "bilmiyoruz;", 0.0), (3560, 104, 1.52)), (("c10s17", "kaçtı;", -0.4), (3560, 104, 1.52)), (("c10s17", "ilk", -0.5), (2900, 70, 1.15))]
KING_X0, KING_V = 8700, 80.0
CAMS21 = [(("c10s21", -0.2), (7950, 0, 1.0)), (("c10s21", "Floransa'ya", -0.2), (8100, 20, 1.15)), (("c10s21", "mızrağı", -0.2), (8000, 40, 1.4)), (("c10s22", -0.4), (7800, 50, 1.6))]
WOK = L.WOv(CAMS21)
WOB = L.WOv(CAMS_B)
WOC = L.WOv(CAMS_C)
_STIL_MEN = [dict(robe="#7A6A4A", robe2="#B8BCC4", hat_col="#5A5A60"), dict(robe="#4A5A6A", robe2="#B8BCC4", hat_col="#5A5A60"), dict(robe="#6A3A2A", robe2="#B8BCC4", hat_col="#5A5A60")]
# A: yürüyüş (yerel t=0 çekim başından lead kadar önce; hız sabit) — B: kapı önünde dururlar
ACTORS_A = [dict(kind="soylu", x0=1880, dir=1, speed=135.0, h=226, seed=2, phase=0.0, y=YG - 6, stil=dict(robe="#6E1A22", robe2="#D2A33E", hat_col="#1A1008"))] + \
    [dict(kind="asker", x0=1880 - 96 * (i + 1), dir=1, speed=135.0, h=216, seed=11 + i, phase=0.3 * (i + 1), y=YG - 6 + 4 * i, prop="halberd" if i != 1 else "spear", stil=_STIL_MEN[i]) for i in range(3)]
ACTORS_B = [dict(kind="soylu", x0=3478, dir=1, speed=0.0, h=226, seed=2, y=YG - 6, action="idle", stil=dict(robe="#6E1A22", robe2="#D2A33E", hat_col="#1A1008"))] + \
    [dict(kind="asker", x0=3478 - 96 * (i + 1), dir=1, speed=0.0, h=216, seed=11 + i, y=YG - 6 + 4 * i, prop="halberd" if i != 1 else "spear", action="idle", stil=_STIL_MEN[i]) for i in range(3)]


def paper_hour(cx, sx, sy, z, s=1.0):
    """Kapıya çivilenmiş yırtık kenarlı kâğıt + kum saati (BİR SAAT emri)."""
    import cilt_paper as PP
    k = cx.amt(("c10s16", "saat", -0.3), 0.6)
    if k <= 0.003:
        return
    pp = PP.paper_image(300, 250, 8, (226, 212, 180), "torn", (), 40, 1.2)
    pp.draw(cx.f, sx, sy - (1 - ease_out(k)) * 40 * z, rot=-0.04, scale=s * z * (0.8 + 0.2 * ease_out(k)), alpha=k, shadow=0.6)
    import icons
    icons.draw_icon(cx.f, "hourglass", sx, sy - 6 * z * s, size=150 * z * s, metal="bronze", alpha=k)
    for dx in (-100, 100):
        cx.f.circle(sx + dx * z * s, sy - 96 * z * s, 7 * z * s, color="#2A1A0C", alpha=0.9 * k)
CAMS10 = [(("c10s10", -0.2), (1300, 40, 1.55)), (("c10s10", "konseyler", -0.2), (1650, 50, 1.3)), (("c10s11", -0.3), (2050, 40, 1.2))]
WO10 = L.WOv(CAMS10)
SHOTS = [
    shot("c10_tepe", ("c10s1", 0), mode="night", perde=2,
         cam=[(("c10s1", 0), look(960, 540, 1.0)), (("c10s1", "Careggi", 0.0), look(1600, 562, 1.8)), (("c10s2", -0.35), look(1600, 562, 7.0))], label="Careggi tepesi",
         ovl=L.ov(L.date_plate("NİSAN 1492", ("c10s1", "43", -0.2)), L.tag("LORENZO DE' MEDİCİ", 1260, 180, ("c10s1", "Lorenzo", -0.1), size=32, out=("c10s1", "Careggi", 0.0), w=520))),
    shot("oda", ("c10s2", 0), room="careggi", mode="night", perde=2, figure="lying",
         cams=[(("c10s2", 0), (2000, -80, 2.6)), (("c10s2", "dostu", 0.0), (1150, 30, 1.35)), (("c10s3", -0.3), (980, 40, 1.55))],
         actors=[dict(kind="banker", x=900, y=806, h=288, action="pray", dir=-1, sil="#0E0806", seed=4, rim_dir=1, layer="front"),
                 dict(kind="soylu", x=1010, y=806, h=284, action="pray", dir=-1, sil="#0E0806", seed=9, rim_dir=1, layer="front")],
         after=L.after_ov(L.wtag("POLİZİANO", 900, 470, ("c10s2", "Poliziano", -0.1), sub="şair", size=30, w=300), L.wtag("PICO DELLA MIRANDOLA", 1010, 380, ("c10s2", "Pico", -0.1), sub="genç filozof", size=30, w=470)),
         tr=("zoomthru", 1.0, dict(at=(960, 540), at_b=(960, 380))), link="scale", label="Careggi: başucunda iki dost"),
    shot("p5_oda", ("c10s3", -0.2), room="c10lib", variant="kutuphane", mode="night", perde=2, empty_frac=0.5, figure="desk", sil=True,
         cams=[(("c10s3", -0.2), (1500, 20, 1.35)), (("c10s3", "bitmeden", -0.5), (1050, 0, 1.15)), (("c10s3", "esirgemesini", 0.0), (1250, 0, 1.0)), (("c10s4", -0.3), (1560, 60, 1.45))],
         ovl=L.ov(L.letter_ovl(1500, 600, 500, 680, ("c10s3", "mektubuna", -0.3), out=("c10s3", "söyledi", 0.6), n=8, dur=5.4, seed=7, tone=(226, 212, 180)),
                  L.tag("POLİZİANO'NUN MEKTUBU", 560, 190, ("c10s3", "Poliziano'nun", -0.1), size=32, w=560, out=("c10s3", "Pico'ya", 0.0))),
         tr=("candle", 1.0, dict(at=(960, 700))), link="light", label="kütüphane: bitmemiş raf, mektup"),
    shot("oda", ("c10s4", -0.1), room="careggi", mode="night", perde=2, figure="lying",
         cams=[(("c10s4", -0.1), (1500, 20, 1.3)), (("c10s4", "oradaydı", 0.0), (1280, 30, 1.4)), (("c10s5", -0.3), (1060, 40, 1.55))],
         actors=[dict(kind="banker", x=880, y=806, h=288, action="pray", dir=-1, sil="#0E0806", seed=4, rim_dir=1, layer="front"),
                 dict(kind="soylu", x=960, y=806, h=284, action="pray", dir=-1, sil="#0E0806", seed=9, rim_dir=1, layer="front"),
                 dict(kind="kesis", x=1700, y=806, h=292, action="idle", dir=-1, sil="#0A0604", seed=12, rim_dir=-1, layer="front", walk=(1060, 150.0), walk_at=("c10s4", -0.1))],
         after=L.after_ov(L.wtagf("SAVONAROLA", lambda cx: L.walk_x(cx, 1700, 1060, 150.0, ("c10s4", -0.1)), 440, ("c10s4", "Savonarola", -0.1), size=30, w=340), L.wtag("POLİZİANO'YA GÖRE", 880, 330, ("c10s4", "Poliziano'ya", -0.1), size=24, w=380, dx=-60)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Savonarola yatağa yaklaşır"),
    shot("p5g_oda", ("c10s5", -0.2), room="careggi", mode="night", perde=2, figure="lying", mono_at=("c10s5", -0.3), mono_dur=1.0, turn_at=("c10s5", "duvara", -0.3), turn_dur=2.4,
         cams=[(("c10s5", -0.2), (1060, 40, 1.55)), (("c10s5", "üçüncüde", 0.0), (1100, 40, 1.65)), (("c10s6", -0.3), (1040, 30, 1.8))],
         actors=[dict(kind="banker", x=880, y=806, h=288, action="pray", dir=-1, sil="#0E0806", seed=4, rim_dir=1, layer="front"),
                 dict(kind="kesis", x=1060, y=806, h=292, action="idle", dir=-1, sil="#0A0604", seed=12, rim_dir=-1, layer="front")],
         ovl=L.ov(L.stamp("ANEKDOT", 1560, 220, ("c10s5", "yandaşları", 0.0), size=60, rot=-0.08),
                  L.tag("I", 1620, 430, ("c10s5", "üç", 0.0), size=44, w=150), L.tag("II", 1620, 540, ("c10s5", "şart,", 0.3), size=44, w=150), L.tag("III", 1620, 650, ("c10s5", "şart,", 0.6), size=44, w=150),
                  L.tick(1730, 428, ("c10s5", "evet,", 0.0)), L.tick(1740, 538, ("c10s5", "evet,", 0.45)),
                  L.tag("FLORANSA'YA ÖZGÜRLÜK", 1560, 790, ("c10s5", "Floransa'ya", -0.1), size=28, w=540, out=("c10s5", "duvara", 0.6))),
         tr=("yikama", 0.8), link="material", label="ANEKDOT: üç şart, duvara dönmüş yüz (gravür)"),
    shot("c10_mektup", ("c10s6", -0.2), mode="night", perde=2, at=("c10s6", -0.2), n=10, dur=3.6, seed=5,
         ghosts=[dict(text="I · II · III", dy=70, at=("c10s6", "üç", 0.0), out=("c10s6", "geçiyor", 0.4), size=70, x=0), dict(text="duvar", dy=300, at=("c10s6", "duvar", -0.4), out=("c10s7", -0.2), size=64, x=0)],
         cam=("push", 0.05), tr=("sayfa", 0.9), link="material", label="mektupta ne üç şart ne duvar"),
    shot("p5_oda", ("c10s7", -0.2), room="calisma", variant="hucre", mode="night", perde=2, figure="desk",
         cams=[(("c10s7", -0.2), (1334, 120, 2.4)), (("c10s7", "1475'te", 0.2), (1150, 50, 1.45)), (("c10s7", "genç", 0.0), (1100, 20, 1.25))],
         ovl=L.ov(L.tag("GİROLAMO SAVONAROLA", 960, 190, ("c10s7", "Girolamo", -0.1), size=36, w=700, out=("c10s7", "genç", 0.0)), L.date_plate("1475", ("c10s7", "1475'te", -0.1))),
         tr=("zoomthru", 1.0, dict(at=(1500, 590), at_b=(960, 540))), link="light", label="hücre: kandil, kukuletalı siluet"),
    shot("p5_map", ("c10s7", "genç", 0.0), view=(11.45, 44.55, 9.0), mode="day", perde=2, regions=[],
         cams=[(("c10s7", "genç", 0.0), (11.52, 44.74, 20.0)), (("c10s7", "Bologna'da", -0.2), (11.48, 44.67, 23.0)), (("c10s8", -0.3), (11.44, 44.62, 21.0))],
         cities=[dict(lon=11.3426, lat=44.4949, name="BOLOGNA", kind="town", at=("c10s7", "Bologna'da", -0.2), size=40, side="l"), dict(lon=11.6199, lat=44.8381, name="", kind="town", at=("c10s7", "tıp", -0.2), size=34)],
         routes=[dict(pts=[(11.6199, 44.8381), (11.55, 44.72), (11.45, 44.60), (11.3426, 44.4949)], at=("c10s7", "yürüyerek", -0.2), dur=1.8, color="#A8321E", width=10.0, dash=(20, 14))],
         icons_=[dict(kind="book_open", lon=11.6199, lat=44.8381, size=150, at=("c10s7", "tıp", -0.2), metal="gold"), dict(kind="monk", lon=11.3426, lat=44.4949, size=170, at=("c10s7", "Dominiken", -0.1), metal="gold")],
         ovl=L.ov(L.date_plate("1475", ("c10s7", "tıp", -1.0))), tr=("yikama", 0.8), link="material", label="harita: Bologna'ya yürüyüş"),
    shot("p5_pano", ("c10s8", -0.2), pano="nave", tod="night", mode="night", perde=2,
         cams=[(("c10s8", -0.2), (2150, 0, 1.0)), (("c10s8", "kürsüde", -0.4), (2500, -30, 1.25)), (("c10s9", -0.4), (2540, -50, 1.5))],
         stations=[dict(x=2500, at_frac=0.0, fn=K.st_pulpit, climb_at=("c10s8", "manastırın", -0.2), syms=[("sword", ("c10s8", "kılıçtan", -0.2)), ("whip", ("c10s8", "kırbaçtan", -0.2)), ("flood", ("c10s8", "tufandan", -0.2))])],
         ovl=L.ov(L.date_plate("1491", ("c10s8", "1491'de", -0.1), out=("c10s8", "1494'e", 0.0)), L.date_plate("1494", ("c10s8", "1494'e", 0.0))),
         tr=("yikama", 0.8), link="material", label="kürsü: kılıç, kırbaç, tufan"),
    shot("c10_sapka", ("c10s9", -0.2), mode="day", perde=2, papa_at=("c10s9", "Papa'nın", -0.1), hood_at=("c10s9", "ona", -0.3), hat_at=("c10s9", "kardinal", -0.1), offer_at=("c10s9", "önerdiği", -0.2),
         refuse_at=("c10s9", "onun", -0.1), strike_at=("c10s9", "yerine", -0.1), blood_at=("c10s9", "kandan", -0.2), settle_at=("c10s9", "şapka", 0.0),
         cam=("push", 0.05), ovl=L.ov(L.stamp("ANEKDOT", 1560, 200, ("c10s9", "söylediği", 0.0), size=62, rot=-0.08)),
         tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="ANEKDOT: kırmızı yerine kandan şapka"),
    shot("p5_oda", ("c10s10", -0.2), room="salon", variant="signoria", mode="day", perde=2,
         cams=CAMS10,
         actors=[dict(kind="soylu", x=1330, y=690, h=268, action="talk", dir=1, seed=41, layer="behind", energy=0.8),
                 dict(kind="rahip", x=1590, y=690, h=262, action="bow", dir=1, seed=43, layer="behind", at=("c10s10", "onayladı", -0.6), depth=18, dur=1.6),
                 dict(kind="banker", x=1800, y=690, h=262, action="bow", dir=1, seed=44, layer="behind", at=("c10s10", "onayladı", -0.45), depth=18, dur=1.6),
                 dict(kind="tuccar", x=2010, y=690, h=262, action="bow", dir=-1, seed=45, layer="behind", at=("c10s10", "onayladı", -0.3), depth=18, dur=1.6),
                 dict(kind="soylu", x=2220, y=690, h=262, action="bow", dir=-1, seed=46, layer="behind", at=("c10s10", "onayladı", -0.15), depth=18, dur=1.6)],
         ovl=WO10.tag("PİERO", 1330, 380, ("c10s10", "Piero", -0.1), size=34, w=260),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="genç Piero, itirazsız onay"),
    shot("c10_ittifak", ("c10s11", -0.2), mode="day", perde=2, web_at=("c10s11", -0.1), break_at=("c10s11", "çözülüyordu", -0.1), ring_at=("c10s11", "kurulan", -0.2), out_at=("c10s11", "dışında", 0.0),
         cam=("push", 0.05), ovl=L.ov(L.date_plate("1493", ("c10s11", "1493'te", -0.1), x=96, y=330)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 540))), link="scale", label="denge çözülür: Floransa ve Napoli dışarıda"),
    # ── V3 devam: Sarzana ─────────────────────────────────────────────────────────────────────────────────────
    shot("p5_map", ("c10s12", -0.2), view=(10.7, 44.0, 11.0), mode="day", perde=2, regions=[],
         cams=[(("c10s12", -0.2), (11.0, 44.0, 10.5)), (("c10s12", "Sarzana'daki", -0.3), (10.5, 44.05, 12.0)), (("c10s12", "Alpler'i", -0.2), (10.4, 44.1, 12.5))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c10s12", -0.2), size=40, color="#B33620", side="r"),
                 dict(lon=9.9619, lat=44.1105, name="SARZANA", kind="town", at=("c10s12", "Sarzana'daki", -0.2), size=40, side="l")],
         routes=[dict(pts=[(11.2558, 43.7696), (10.95, 43.92), (10.45, 44.06), (9.9619, 44.1105)], at=("c10s12", "görüşmeyi", 0.0), dur=3.2, color="#A8321E", width=10.0, dash=(20, 14))],
         extra=L.map_extra(L.mm_medal([(11.2558, 43.7696), (10.95, 43.92), (10.45, 44.06), (9.9619, 44.1105)], ("c10s12", "görüşmeyi", 0.0), dur=3.2, R_px=84, hat="berretto"),
                           L.mm_icons([(9.9619, 44.1105)], "tent", ("c10s12", "kampta", -0.1), size=130, metal="cinnabar")),
         ovl=L.ov(L.tag("EKİMİN SONU", 960, 180, ("c10s12", "ekimin", -0.1), size=34, w=470, out=("c10s12", "kampta", 0.3))),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="harita: Piero Sarzana'ya"),
    shot("p5_map", ("c10s12", "Alpler'i", -0.2), view=(9.0, 44.6, 8.0), mode="day", perde=2, regions=[],
         cams=[(("c10s12", "Alpler'i", -0.2), (8.4, 44.8, 8.0)), (("c10s12", "Charles'a", -0.4), (9.4, 44.5, 9.5)), (("c10s12", "kalelerini", -0.3), (10.15, 43.95, 11.0)), (("c10s13", -0.4), (10.2, 43.95, 11.5))],
         cities=[dict(lon=9.9619, lat=44.1105, name="SARZANA", kind="town", at=("c10s12", "Alpler'i", -0.2), size=36, side="l"), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c10s12", "Alpler'i", -0.2), size=36, color="#B33620", side="r")],
         routes=[dict(pts=[(6.7, 45.15), (7.6, 45.02), (8.5, 44.82), (9.25, 44.52), (9.9619, 44.1105)], at=("c10s12", "Alpler'i", -0.2), dur=2.4, color="#233C8C", width=11.0, arrow=True)],
         icons_=[dict(kind="mountain", lon=6.9, lat=45.22, size=150, at=("c10s12", "Alpler'i", -0.2), metal="gold"),
                 dict(kind="crown", route=[(6.7, 45.15), (7.6, 45.02), (8.5, 44.82), (9.25, 44.52), (9.9619, 44.1105)], at=("c10s12", "Alpler'i", -0.2), move_at=("c10s12", "Alpler'i", -0.2), move_dur=2.4, size=100, metal="lapis")],
         extra=L.map_extra(L.mm_tag(6.9, 45.22, "ALPLER", ("c10s12", "Alpler'i", -0.1), size=30, dy=-120, w=260),
                           L.mm_flip_icons([(9.96, 44.11), (10.22, 43.96), (10.40, 43.72), (10.31, 43.55)], "castle", ("c10s12", "kalelerini", -0.2), ("c10s12", "bıraktı", -0.15), "cinnabar", "lapis", size=96),
                           L.mm_tag(11.2558, 43.7696, "SIGNORIA", ("c10s12", "Signoria'ya", -0.1), strike_at=("c10s12", "sormadan", -0.1), size=28, dx=0, dy=-110, w=300)),
         ovl=L.ov(L.tag("VIII. CHARLES", 960, 170, ("c10s12", "VIII.", -0.1), size=34, w=470, sub="Fransa Kralı", out=("c10s12", "kalelerini", 0.0))),
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="harita: Alpler'i aşan kral, kaleler"),
    # ── V4 · 9 Kasım ───────────────────────────────────────────────────────────────────────────────────────
    shot("p5_sehir", ("c10s13", -0.1), scene="sokak", door="close", door_at=("c10s17", 0.0), tod="day", mode="day", perde=2,
         cams=CAMS_A, actors=ACTORS_A,
         ovl=L.ov(L.engr("9 KASIM 1494", 960, 260, ("c10s13", -0.05), size=112, track=14, dur=1.2, out=("c10s14", "silahlı", 0.2)), L.label("BİR PAZAR", 960, 345, ("c10s13", "pazar.", -0.9), size=44, out=("c10s14", "silahlı", 0.2))),
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", longtake=True, label="9 Kasım: Piero silahlı adamlarıyla kapıya"),
    shot("p5_sehir", ("c10s15", -0.55), scene="sokak", door="close", door_at=("c10s15", "kapandı", -0.12), tod="day", mode="day", perde=2,
         cams=CAMS_B, actors=ACTORS_B,
         ovl=L.ov(L.tag("LUCA CORSİNİ", 960, 200, ("c10s15", "Luca", -0.1), size=32, w=480, sub="Signoria üyesi", out=("c10s16", -0.3)), L.stamp("○ TEK KAYNAK", 1560, 250, ("c10s15", "anlatılır", -0.1), size=48, rot=-0.07, out=("c10s16", -0.2)),
                  WOB.draw(paper_hour, 3600, 846 - 250), L.label("BİR SAAT İÇİNDE", 960, 120, ("c10s16", "saat", -0.2), size=36, track=10)),
         link="dir", label="kapı yüzüne kapanır; BİR SAAT"),
    shot("p5_sehir", ("c10s17", -0.1), scene="sokak", door="close", door_at=("c10s15", "kapandı", -0.12), tod="day", mode="day", perde=2,
         cams=CAMS_C, actors=ACTORS_B[1:], stations=[dict(x=3478, at=0.0, fn=K.st_piero, flee_at=("c10s17", "kaçtı;", -0.1), ask_at=("c10s17", "düşündüğünü", -0.1), ask_out=("c10s17", "ama", 0.0), turn_at=("c10s17", "çıkmadı,", 0.0))],
         ovl=L.ov(WOC.draw(lambda cx, sx, sy, z: paper_hour(cx, sx, sy, z, 0.55), 3600, 846 - 345)),
         link="cam", label="Piero ne düşündüğü bilinmez; huzura çıkmaz, kaçar"),
    shot("p5_map", ("c10s17", "durağının", 0.0), view=(11.3, 44.1, 9.0), mode="day", perde=2, regions=[],
         cams=[(("c10s17", "durağının", 0.0), (11.26, 44.0, 11.0)), (("c10s17", "Bologna", 0.0), (11.30, 44.12, 12.0)), (("c10s18", -0.3), (11.32, 44.2, 12.6))],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c10s17", "durağının", 0.0), size=38, color="#B33620", side="l"),
                 dict(lon=11.3426, lat=44.4949, name="", kind="town", at=("c10s17", "Bologna", -0.1), size=38, side="r")],
         routes=[dict(pts=[(11.2558, 43.7696), (11.28, 43.98), (11.32, 44.25), (11.3426, 44.4949)], at=("c10s17", "ilk", -0.1), dur=1.7, color="#A8321E", width=10.0, dash=(20, 14))],
         extra=L.map_extra(L.mm_medal([(11.2558, 43.7696), (11.28, 43.98), (11.32, 44.25), (11.3426, 44.4949)], ("c10s17", "ilk", -0.1), dur=1.7, R_px=70, hat="berretto"),
                           L.mm_tag(11.3426, 44.4949, "BOLOGNA", ("c10s17", "Bologna", -0.1), size=36, dx=210, dy=0, w=320)),
         ovl=L.ov(L.stamp("○ TEK KAYNAK", 1560, 250, ("c10s17", "yazılır", -0.1), size=48, rot=-0.07)),
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="harita: ilk durak Bologna (yazılır)"),
    # ── V4 devam: meydan çağrısı, Giovanni, aynı alay tersine ─────────────────────────────────────────────────
    shot("p5_sehir", ("c10s18", -0.2), scene="meydan", act="kalabalik", tod="day", mode="day", perde=2, dir="l", flags="lily", n=26,
         ovl=L.ov(L.brush("HALK VE ÖZGÜRLÜK", 960, 262, ("c10s18", "halk", -0.15), size=132, color="#A8321E", dur=1.3, out=("c10s18", "özgürlük.", 1.4))),
         tr=("yikama", 0.8), link="material", label="meydan: eski çağrı yükselir (halk ve özgürlük)"),
    shot("c10_kilik", ("c10s19", -0.2), mode="night", perde=2, walk_at=("c10s19", -0.3), cam=("push", 0.05),
         tags=dict(card=("c10s19", "Giovanni", -0.1), fran=("c10s19", "Fransisken", 0.0)),
         tr=("light", 0.9, dict(at=(960, 640))), link="light", label="Giovanni kapı sövesinde Fransisken kılığına girer"),
    shot("p5_procession", ("c10s20", -0.2), dir="r", density=0.9, mix=dict(rider=0.24, noble=0.22, page=0.14, banner=0.26, guard=0.04, elder=0.06, cleric=0.02, common=0.02), pan=("r", 700), speed=110.0, seed=7, mode="day", perde=2,
         ovl=L.ov(L.date_plate("1434", ("c10s20", "1434'te", -0.1)), L.tag("60 YIL ÖNCE", 960, 232, ("c10s20", "Altmış", -0.1), size=52, w=540, out=("c10s20", "aile", 0.0))),
         tr=("carry", 0.9, dict(strip="banner", dir="r")), link="carry", label="1434: aile zaferle döner (soldan sağa)"),
    shot("p5_procession", ("c10s20", "Şimdi", -0.3), dir="l", density=0.9, mix=dict(rider=0.24, noble=0.22, page=0.14, banner=0.26, guard=0.04, elder=0.06, cleric=0.02, common=0.02), pan=("l", 700), speed=110.0, seed=7, mode="night", perde=2,
         ovl=L.ov(L.date_plate("1494", ("c10s20", "Şimdi", 0.0)), L.tag("GİDİŞ SIRASI", 960, 232, ("c10s20", "gidiş", -0.1), size=52, w=540, out=("c10s20", "onlardaydı.", 0.7))),
         tr=("slide", 0.9, dict(dir="l")), link="dir", label="aynı alay tersine, gece: gidiş sırası onlarda"),
    shot("p5g_pano", ("c10s21", -0.2), pano="florence", tod="day", mode="day", perde=2, cams=CAMS21, mono_at=("c10s21", "mızrağı", -0.25), mono_dur=1.0,
         stations=[dict(x=KING_X0, at=0.0, fn=K.st_king, speed=KING_V, foot=3)],
         ovl=L.ov(L.date_plate("17 KASIM", ("c10s21", "17", -0.1), out=("c10s21", "mızrağı", 0.0)), WOK.tagf("VIII. CHARLES", lambda cx: KING_X0 - KING_V * cx.t - 10, 846 - 470, ("c10s21", "Charles", -0.1), sub="Fransa Kralı", size=32, w=440, out=("c10s21", "mızrağı", 0.0)),
                  L.stamp("ANEKDOT", 1560, 215, ("c10s21", "diye", 0.0), size=60, rot=-0.08)),
         tr=("carry", 0.9, dict(strip="banner", dir="l")), link="carry", label="17 Kasım: Charles Floransa'ya girer; yatay mızrak (ANEKDOT)"),
    # ── V5 · Kral ve yeni düzen ────────────────────────────────────────────────────────────────────────────
    shot("c10_capponi", ("c10s22", -0.2), mode="day", perde=2, cap_at=("c10s22", "müzakerecilerinden", -0.1), king_at=("c10s22", "kralın", -0.3), sheet_at=("c10s22", "şart", -0.3),
         tear_at=("c10s22", "yırttı;", -0.25), trumpet_at=("c10s22", "trompetlere", -0.1), bell_at=("c10s22", "çanlarla", -0.1), cam=("push", 0.05),
         ovl=L.ov(L.tag("PİERO CAPPONİ", 470, 858, ("c10s22", "Piero", -0.1), size=32, w=430, sub="müzakereci"),
                  L.tag("ŞART TASLAĞI", 960, 150, ("c10s22", "şart", -0.1), size=32, w=380, sub="kralın", out=("c10s22", "yırttı;", 0.2)),
                  L.tag("TROMPET", 1450, 858, ("c10s22", "trompetlere", -0.1), size=30, w=300),
                  L.stamp("ANEKDOT", 960, 150, ("c10s22", "söylediği", 0.0), size=60, rot=-0.06)),
         tr=("sayfa", 0.8), link="material", label="ANEKDOT: Capponi taslağı yırtar; trompete çanla yanıt"),
    shot("c10_konsey", ("c10s23", -0.2), mode="day", perde=2, fill_at=("c10s23", "Büyük", -0.2), cam=("push", 0.05),
         ovl=L.ov(L.date_plate("ARALIK", ("c10s23", "Aralıkta", -0.1), out=("c10s23", "Venedik'ten", 0.0)),
                  L.tag("VENEDİK'TEN ESİNLENEN", 560, 200, ("c10s23", "Venedik'ten", -0.1), size=32, w=620, out=("c10s23", "Büyük", 0.5)),
                  L.tag("BÜYÜK KONSEY", 620, 270, ("c10s23", "Büyük", -0.05), size=44, w=560),
                  L.count_up(1400, 300, ("c10s23", "üç", -0.1), 3000, dur=1.8, suffix="+", size=120, unit="YURTTAŞ", unit_size=34)),
         tr=("zoomthru", 0.9, dict(at=(960, 560), at_b=(960, 540))), link="scale", label="Büyük Konsey: üç binden fazla yurttaş"),
    shot("c10_plan", ("c10s24", -0.2), mode="day", perde=2, draw_at=("c10s24", -0.1), sav_at=("c10s24", "Savonarola'nın", -0.2), arrow_at=("c10s24", "belirleyici", -0.3), cam=("push", 0.05),
         ovl=L.ov(L.tag("SAVONAROLA", 330, 810, ("c10s24", "Savonarola'nın", -0.1), size=32, w=380, sub="payı"),),
         tr=("zoomthru", 0.8, dict(at=(960, 560), at_b=(960, 540))), link="scale", label="salon planı; Savonarola'nın payı (kesikli: yazılır)"),
    # ── V6 · Kibirlerin Yakılması (meydan, dusk; kamera yığın merkezine kilitli) ───────────────────────────────
    shot("p5_sehir", ("c10s25", -0.2), scene="meydan", act="ates", tod="dusk", mode="day", perde=2, longtake=True,
         items_at=[("c10s26", "ayna,", -0.1), ("c10s26", "peruk,", -0.1), ("c10s26", "iskambil,", -0.1), ("c10s26", "zar", -0.1), ("c10s26", "çalgılar", -0.1)],
         fire_at=("c10s25", "ateş", -0.35), fire_dur=7.5,
         ovl=L.ov(L.engr("7 ŞUBAT 1497", 960, 240, ("c10s25", "7", -0.15), size=104, track=14, dur=1.2, out=("c10s25", "Signoria", 0.0)),
                  L.tag("KARNAVAL GÜNLERİ", 960, 340, ("c10s25", "Karnaval", -0.1), size=34, w=520, out=("c10s25", "Signoria", 0.0)),
                  L.tag("SİGNORİA MEYDANI", 960, 250, ("c10s25", "Signoria", -0.1), size=38, w=560, out=("c10s25", "ilk", 0.0)),
                  L.tag("İLK ATEŞ", 960, 250, ("c10s25", "ilk", -0.05), size=44, w=380, out=("c10s26", "Ateşe", 0.3)),
                  L.tag("AYNA", 300, 330, ("c10s26", "ayna,", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("PERUK", 300, 400, ("c10s26", "peruk,", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("KOZMETİK", 300, 470, ("c10s26", "kozmetik,", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("İSKAMBİL", 300, 540, ("c10s26", "iskambil,", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("ZAR", 300, 610, ("c10s26", "zar", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("ÇALGILAR", 300, 680, ("c10s26", "çalgılar", -0.1), size=30, w=250, out=("c10s26", "listede", 0.0)),
                  L.tag("BİR LİSTEDE", 1560, 300, ("c10s26", "listede", -0.1), size=32, w=380, out=("c10s27", -0.2)),
                  L.tag("RESİM", 1560, 370, ("c10s26", "resim", -0.1), size=30, w=250, out=("c10s27", -0.2)),
                  L.tag("HEYKEL", 1560, 440, ("c10s26", "heykel", -0.1), size=30, w=250, out=("c10s27", -0.2)),
                  L.stamp("ANEKDOT", 1560, 250, ("c10s27", "sık", -0.1), size=60, rot=-0.08, out=("c10s28", -0.3)),
                  K.joke_ovl(("c10s27", "Botticelli'nin", -0.15), ("c10s27", "kendi", -0.2), ("c10s27", "attığı", -0.3), ("c10s27", "hangi", -0.1), ("c10s27", "göstermiyor.", -0.45), ("c10s28", -0.2))),
         tr=("sayfa", 0.9), link="material", label="Kibirler yanar: ilk ateş, eşyalar ateşe"),
    shot("black", ("c10s28", -0.2), text="[devam]", label="yer tutucu"),
]
