"""c5 — Konsil, Kitap, Platon (1439 – 1492). Parça 2 / 3. bölüm (parça kapanışı). Çekim listesi; özel türler c5_kinds.py, ortak yardımcılar p2_lib.py / c3_kinds.py / c4_kinds.py."""
from shots import shot
import cilt_medici as CM
import c5_kinds as K
look = K.look


def _ist_extra(cx, cm, mv):
    """c5s4: Floransa'dan İstanbul'a vaat edilen yardım (kesik ok) yarı yolda söner; İstanbul'da kırmızı halka (şiddet yok)."""
    import math
    import skia
    from p2_lib import S, P, clamp, ease_io, ease_out, lerp
    f = cx.f
    c = f.c
    t = cx.t
    x0, y0 = cm.ll(11.2558, 43.7696)
    x1, y1 = cm.ll(28.9784, 41.0082)
    k = ease_io(clamp((t - cx.at(("c5s4", "Vaat", -0.2))) / 1.4), 1.6)
    xe, ye = lerp(x0, x1, 0.52 * k), lerp(y0, y1, 0.52 * k) - 80 * math.sin(math.pi * 0.52 * k)
    pth = skia.Path()
    pth.moveTo(x0, y0)
    pth.quadTo((x0 + x1) / 2, min(y0, y1) - 160, x1, y1)
    pm = skia.PathMeasure(pth, False)
    seg = skia.Path()
    pm.getSegment(0, pm.getLength() * 0.52 * k, seg, True)
    pp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=11.0, Color=skia.Color(199, 154, 60, int(235 * (1.0 - 0.7 * clamp((t - cx.at(("c5s4", "gelmedi;", 0.0))) / 0.8)))), StrokeCap=skia.Paint.kRound_Cap)
    pp.setPathEffect(skia.DashPathEffect.Make([20.0, 14.0], -t * 40))
    c.drawPath(seg, pp)
    kg = ease_out(clamp((t - cx.at(("c5s4", "gelmedi;", 0.0))) / 0.6), 3)
    if kg > 0.003:
        import icons
        icons.draw_icon(f, "question", xe + 10, ye - 70 + 8 * math.sin(t * 3.0), size=110 * kg, metal="gold", alpha=kg, shadow=True)
    kr = ease_out(clamp((t - cx.at(("c5s4", "1453'te", -0.2))) / 0.9), 2.6)
    if kr > 0.003:
        for q, rr in enumerate((46, 70, 94)):
            c.drawCircle(x1, y1, rr * kr, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7.0 - q * 1.5, Color=skia.Color(168, 36, 28, int(235 * (1 - 0.25 * q)))))
        c.drawCircle(x1, y1, 14 * kr, P("#A8241C"))


SHOTS = [
    shot("p2_map", ("c5s1", -0.1), view=(11.45, 44.3, 13.0), mode="day", cam=("push", 0.10), regions=[],
         cities=[dict(lon=11.6196, lat=44.8378, name="FERRARA", kind="town", at=("c5s1", "Ferrara'daki", -0.4), size=40, color="#233C8C", side="l"), dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c5s1", "konsil", -0.2), size=40, color="#B33620", side="r")],
         routes=[dict(pts=[(11.6196, 44.8378), (11.45, 44.30), (11.2558, 43.7696)], at=("c5s1", "konsil", -0.7), dur=1.6, color="#C79A3C", width=10.0)],
         icons_=[dict(kind="cross", route=[(11.6196, 44.8378), (11.45, 44.30), (11.2558, 43.7696)], at=("c5s1", -0.1), move_at=("c5s1", "konsil", -0.7), move_dur=1.7, size=96, metal="gold")],
         date=("1439", ("c5s1", 0.1)), link=None, tr=None, label="Ferrara'daki konsil Floransa'ya taşındı",
         over=[dict(t="tag", text="KONSİL", x=420, y=150, at=("c5s1", "konsil", -0.1), size=40, w=300)]),
    shot("c5_etkenler", ("c5s1", "masraf,", -0.4), mode="day", cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 520))), link="light", label="masraf, veba korkusu, Cosimo'nun teklifi: birlikte etkili"),
    shot("c5_heyet", ("c5s2", -0.1), mode="day", cam=[(("c5s2", 0.0), look(960, 540, 1.0)), (("c5s2", "heyetinin", -0.3), look(1100, 560, 1.12))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="yaklaşık yedi yüz kişilik Rum heyeti"),
    shot("c5_heyet", ("c5s2", "masraflarını", -0.5), mode="day", cam=[(("c5s2", "masraflarını", -0.5), look(1100, 560, 1.12)), (("c5s2", "misafir.", -0.3), look(1180, 540, 0.96))],
         tr=("zoomthru", 0.9, dict(at=(1100, 600), at_b=(960, 560))), link="scale", label="Floransa masrafları üstlenmeyi önerir: cömert ev sahibi, kalabalık misafir"),
    shot("c5_birlik", ("c5s3", -0.1), mode="day", cam=("push", 0.07), tr=("sayfa", 0.8), link="material", label="Temmuz 1439: Doğu ile Batı kiliselerinin birliği ilan edilir"),
    shot("c5_birlik", ("c5s3", "Bizans", -0.4), mode="day", cam=[(("c5s3", "Bizans", -0.4), look(960, 540, 1.0)), (("c5s3", "istemişti.", -0.2), look(760, 520, 1.15))],
         tr=("slide", 0.8, dict(dir="l")), link="dir", label="Bizans birliği Osmanlı tehdidi yüzünden istemişti"),
    shot("p2_map", ("c5s4", -0.1), view=(21.4, 42.2, 2.4), mode="day", cam=("push", 0.07), regions=[], extra=_ist_extra,
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c5s4", -0.1), size=36, color="#B33620", side="r"), dict(lon=28.9784, lat=41.0082, name="İSTANBUL", kind="capital", at=("c5s4", "İstanbul", -0.5), size=40, color="#233C8C", side="r")],
         date=("1453", ("c5s4", "1453'te", -0.3)), tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="vaat edilen yardım gelmedi; 1453'te İstanbul düştü"),
    shot("c5_plethon", ("c5s5", -0.1), mode="day", cam=[(("c5s5", 0.0), look(700, 540, 1.05)), (("c5s5", "Plethon'un", -0.3), look(780, 560, 1.18)), (("c5s5", "uyandı;", -0.4), look(1160, 520, 1.15))],
         tr=("yikama", 0.8), link="material", label="Ficino'ya göre Plethon'u dinlemek Cosimo'da Platon merakını uyandırdı (gravür)"),
    shot("c5_plethon", ("c5s5", "uyandı;", -0.35), mode="day", cam=[(("c5s5", "uyandı;", -0.3), look(1000, 540, 1.0)), (("c5s5", "dermiş.", -0.3), look(1000, 540, 1.07))],
         tr=("zoomthru", 0.9, dict(at=(1160, 280), at_b=(960, 540))), link="scale", label="Floransalılar Plethon'a «ikinci Platon» dermiş"),
    shot("c5_yunanca", ("c5s6", -0.1), mode="day", cam=[(("c5s6", 0.0), look(560, 540, 1.1)), (("c5s6", "Manuel", -0.4), look(900, 540, 1.0))],
         tr=("yikama", 0.8), link="color", label="Yunanca öğretimi 1453'te başlamadı (MİT)"),
    shot("c5_yunanca", ("c5s6", "Manuel", -0.35), mode="day", cam=[(("c5s6", "Manuel", -0.3), look(1100, 560, 1.0)), (("c5s6", "vermişti.", -0.2), look(1250, 560, 1.08))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Manuel Chrysoloras Floransa'da 1396–1397'de ders vermişti"),
    shot("c5_niccoli", ("c5s7", -0.1), mode="day", cam=[(("c5s7", 0.0), look(800, 560, 1.0)), (("c5s7", "borçları", -0.3), look(900, 560, 1.12))],
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Niccoli borç içinde öldü; Cosimo borçları üstlendi"),
    shot("c5_niccoli", ("c5s7", "sekiz", -0.5), mode="day", cam=[(("c5s7", "sekiz", -0.4), look(960, 540, 1.0)), (("c5s7", "gitti.", -0.3), look(1300, 560, 1.0))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="≈800 el yazması Cosimo'nun denetiminde; San Marco'ya gitti"),
    shot("c5_kutuphane", ("c5s8", -0.1), mode="day", cam=[(("c5s8", -0.1), look(1000, 560, 1.0)), (("c5s8", "doğdu.", -0.3), look(1150, 540, 1.1))],
         tr=("light", 0.9, dict(at=(960, 520))), link="light", label="Floransa'nın halka açık bir kitaplığı doğdu"),
    shot("c5_careggi", ("c5s9", -0.1), mode="day", cam=("push", 0.08), tr=("light", 0.9, dict(at=(1000, 500))), link="light", label="1463 dolaylarında Ficino'nun derlemesindeki mektup"),
    shot("c5_careggi", ("c5s9", "Careggi'ye", -0.4), mode="day", cam=("push", 0.09), tr=("zoomthru", 0.9, dict(at=(760, 640), at_b=(960, 560))), link="scale", label="Careggi'ye tarlasını değil zihnini işlemek için geldi"),
    shot("c5_lir", ("c5s10", -0.1), mode="day", cam=[(("c5s10", 0.0), look(960, 540, 1.0)), (("c5s10", "kitabını", -0.5), look(1010, 560, 1.15))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Ficino'dan Platon'un kitabını ve Orfik lirini getirmesini ister"),
    shot("c5_liste", ("c5s11", -0.1), mode="day", cam=("push", 0.07), tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="bir bankacı için fena bir alışveriş listesi değil"),
    shot("c5_armagan", ("c5s12", -0.1), mode="day", cam=[(("c5s12", 0.0), look(800, 560, 1.0)), (("c5s12", "şehirde", -0.3), look(1100, 560, 1.0))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Ficino'ya Platon'un bütün eserleri, şehirde ve Careggi yakınında birer ev"),
    shot("c5_akademi", ("c5s13", -0.1), mode="day", cam=[(("c5s13", 0.0), look(960, 540, 1.0)), (("c5s13", "ama", -0.2), look(960, 540, 1.1))],
         tr=("sayfa", 0.8), link="material", label="sonradan «Platon Akademisi» dendi"),
    shot("c5_akademi", ("c5s13", "tüzüğü", -0.55), mode="day", cam=[(("c5s13", "tüzüğü", -0.5), look(960, 540, 1.1)), (("c5s13", "tutulmadı.", -0.2), look(960, 560, 1.0))],
         tr=("zoomthru", 0.9, dict(at=(960, 340), at_b=(960, 540))), link="scale", label="tüzüğü yoktu, üye kaydı tutulmadı"),
    shot("c5_yil", ("c5s14", -0.1), mode="day", cam=("push", 0.08), tr=("carry", 0.9, dict(strip="ribbon", dir="r")), link="carry", label="Cosimo bu mektuptan yaklaşık bir yıl sonra öldü"),
    shot("c5_lascaris_giris", ("c5s15", -0.1), mode="day", cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 520))), link="light", label="torunu Lorenzo, Janus Lascaris'i Doğu'ya gönderir"),
    shot("p2_map", ("c5s15", "1490", -0.15), view=(18.0, 40.4, 3.3), mode="day", cam=("push", 0.07), regions=[],
         cities=[dict(lon=11.2558, lat=43.7696, name="FLORANSA", kind="capital", at=("c5s15", "1490", -0.4), size=36, color="#B33620", side="r")],
         labels=[dict(text="DOĞU", lon=27.0, lat=39.0, size=52, color="#233C8C", at=("c5s15", "iki", -0.2))],
         routes=[dict(pts=[(11.2558, 43.7696), (14.6, 41.4), (19.5, 39.2), (24.5, 38.4)], at=("c5s15", "1490", -0.05), dur=1.4, color="#233C8C", width=11.0),
                 dict(pts=[(11.2558, 43.7696), (15.2, 42.0), (20.4, 40.2), (25.2, 39.4)], at=("c5s15", "1491'de", -0.3), dur=1.4, color="#A8321E", width=11.0)],
         date=("1490 · 1491", ("c5s15", "1490", -0.05)), tr=("zoomthru", 0.9, dict(at=(1300, 520), at_b=(960, 540))), link="scale", label="1490 ve 1491: iki yolculuk"),
    shot("c5_pazarlik", ("c5s15", "el", -0.4), mode="day", cam=[(("c5s15", "el", -0.3), look(900, 560, 1.0)), (("c5s15", "pazarlık", -0.3), look(1100, 560, 1.12))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="el yazması toplasın, II. Bayezid'le pazarlık yapsın"),
    shot("p2_map", ("c5s16", -0.1), view=(24.0, 39.9, 9.0), mode="day", cam=("push", 0.08), regions=[],
         cities=[dict(lon=24.33, lat=40.16, name="ATHOS", kind="town", at=("c5s16", -0.1), size=44, color="#233C8C", side="r")],
         icons_=[dict(kind="mountain", lon=24.33, lat=40.16, size=130, at=("c5s16", "Athos'a", -0.4), metal="gold")],
         routes=[dict(pts=[(21.2, 38.8), (22.6, 39.5), (24.33, 40.16)], at=("c5s16", "Athos'a", -0.5), dur=1.0, color="#A8321E", width=11.0)],
         date=("1491", ("c5s16", 0.0)), tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="1491'de Athos'a uğradı"),
    shot("c5_defter", ("c5s17", -0.1), mode="day", cam=[(("c5s17", 0.0), look(640, 560, 1.08)), (("c5s17", "listesi", 0.0), look(700, 560, 1.18))],
         tr=("sayfa", 0.8), link="material", label="cep defteri: Lorenzo'nun istediği metinlerin listesi"),
    shot("c5_defter", ("c5s17", "kütüphanesinin", -0.5), mode="day", cam=[(("c5s17", "kütüphanesinin", -0.4), look(700, 560, 1.18)), (("c5s17", "içeriği.", -0.2), look(1230, 560, 1.18))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="ve Medici kütüphanesinin o günkü içeriği"),
    shot("c5_sayac", ("c5s18", -0.1), mode="day", cam=("push", 0.07), tr=("light", 0.9, dict(at=(960, 520))), link="light", label="Lascaris iki yüz el yazması getirdiğini söyler"),
    shot("c5_sayac", ("c5s18", "defterdeki", -0.5), mode="day", cam=[(("c5s18", "defterdeki", -0.4), look(960, 540, 1.0)), (("c5s18", "katı.", -0.2), look(1060, 480, 1.1))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="defterdeki liste bunun neredeyse iki katı"),
    shot("c5_bilinmiyor", ("c5s19", -0.1), mode="day", cam=("push", 0.07), tr=("carry", 0.9, dict(strip="ink", dir="r")), link="carry", label="pazarlığın ayrıntısını bilmiyoruz"),
    shot("c5_bilinmiyor", ("c5s19", "tahtsız", -0.6), mode="day", cam=[(("c5s19", "tahtsız", -0.5), look(960, 540, 1.0)), (("c5s19", "yürütüyordu.", -0.3), look(1040, 540, 1.1))],
         tr=("zoomthru", 0.9, dict(at=(960, 540), at_b=(960, 540))), link="scale", label="tahtsız efendinin kitap hesabını Osmanlı topraklarında bir Rum bilgin yürütüyordu"),
    shot("c5_liste_lorenzo", ("c5s20", -0.1), mode="day", cam=[(("c5s20", 0.0), look(960, 540, 1.0)), (("c5s21", "Lorenzo'ya", -0.3), look(960, 520, 1.06))],
         tr=("slide", 0.8, dict(dir="r")), link="dir", label="Lascaris'in listesi Lorenzo için yazılmıştı; şimdi listenin sahibine bakalım"),
]
OUTRO_TR = ("iris", 1.0, dict(obj="palle", at=(960, 491), r=100))
YIL_AT = [(("c5s4", "1453'te", -0.3), 1453), (("c5s9", "1463", -0.2), 1463), (("c5s15", "1491'de", -0.3), 1491)]
