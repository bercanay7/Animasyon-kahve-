"""c16 — Hesap (1737 – bugün). FİLMİN SONU. Ağır giriş (ölüm odası; mizah KAPALI) → hafif-kuşkucu orta (tez sorgusu + sağlamlık haritası AKIŞIN İÇİNDE) → SESSİZ ağır kapanış.
Yönetmen kartı: yonetmen_c16.md · notlar: notlar_c16.md. Tüm çekimler cümle/sözcük çapalı (ses GEÇİCİ; ElevenLabs gelince zamanlar değişir).
Işık/zaman: c0 ile AYNI seçim (oda1743 `tod="dusk"`, `mode="night"`; AY/saat/hava iddiası YOK); skyline c0'ın açılış planı (dusk, seed=2) ve kamera TERS yönde.
Renk anahtarı: giriş = mum sarısı/kızıl oda; orta = soluk sıva + üç pigment (altın SAĞLAM · lacivert NİTELİKLİ · kızıl MİT); kapanış = lacivert-kor, tek sıcak ışık.
İmza sekans: «Aynı oda, ters yön» (s1–s2: c0'ın kamera yolu tersine; s3 belgeye zoomthru; s4–s6 c0'ın haritasına dönüş — özet kartı artık «SÖZ DEĞİL» damgalı)
  + «Sağlamlık haritası» (s13–s20: üç büyük şerit → üst HUD'a küçülür; her iddia kendi çekiminde şeride UÇAR) + sessiz son (s24–s25: kor-lacivert skyline, fener noktaları, ağır kararma).
KAPALI: ceset/organ/yüz; frengi satırı; 'bağışladı/miras bıraktı'; 'çürüttük'; Anna Maria Luisa'nın sözü olarak 'Hiçbir şey buradan çıkmayacak'; 'tüm Medici'ler bitti'.
"""
import functools

from shots import shot
import cilt_medici as CM
import p7_lib as L
import c0_kinds as K0
import c16_kinds as K
look = L.look
ov = L.ov

ODA = dict(tod="dusk", mode="night", perde=3)            # c0 ODA_DUSK ile aynı tod/mode; perde 3 = film sonu
FLO = (11.2558, 43.7696)
GEN = (8.9463, 44.4056)
VEN = (12.3155, 45.4408)
CAM = (-71.1167, 42.3736)


def band(tokens, sid, base):
    """Üst HUD şeridi (sağlamlık haritası): çekim başında TAM açık (c16_saglam'ın küçülmüş şeridinden devir); base = şeritte o ana dek yerleşmiş nokta sayıları."""
    return K.saglam_band(tokens, band_at=(sid, -1.2), base=base)


SHOTS = [
    # ── 1. s1–s2: 18 Şubat 1743 — AYNI oda, c0'ın kamera yolu TERS (arma → yatak); nedimeler yatağın yanında (siluet) ──────────────────
    shot("p7_oda", ("c16s1", -0.1), room="oda1743", figure="lying", **ODA, longtake=True,
         actors=[dict(kind="soylu_f", x=900, y=872, h=300, sil=True, walk=(880, 130), walk_at=("c16s2", "nedimelerince", -1.1), seed=3, dir=-1),
                 dict(kind="soylu_f", x=1010, y=884, h=300, sil=True, walk=(960, 130), walk_at=("c16s2", "nedimelerince", -0.9), seed=5, dir=-1)],
         cams=[(("c16s1", -0.1), (1740, 30, 1.25)), (("c16s1", "Yetmiş", 0.0), (1150, 20, 1.15)), (("c16s1", "Anna", -0.2), (985, 30, 1.2)),
               (("c16s2", "anlatıya", 0.0), (900, 30, 1.2)), (("c16s2", "yıkanmasını", 0.0), (860, 40, 1.34))],
         ovl=ov(L.date_plate("18 ŞUBAT 1743", ("c16s1", "18", -0.1), out=("c16s2", "açılmamasını", 0.0)),
                L.tag("75 YAŞINDA", 1560, 690, ("c16s1", "Yetmiş", -0.1), size=34, w=330, out=("c16s2", "Bir", 0.0)),
                L.tag("ANNA MARIA LUISA", 1480, 790, ("c16s1", "Anna", -0.1), size=36, w=520, out=("c16s2", "yüzüyle", 0.0)),
                L.stamp("BİR ANLATIYA GÖRE", 1420, 330, ("c16s2", "anlatıya", -0.1), size=48, rot=-0.06),
                L.tag("BEDENİ AÇILMASIN", 1500, 520, ("c16s2", "açılmamasını", -0.15), size=34, w=520),
                L.tag("YÜZ VE ELLER", 540, 250, ("c16s2", "yüzüyle", -0.1), size=34, w=420),
                L.tag("YALNIZ NEDİMELER", 540, 350, ("c16s2", "yalnız", -0.1), size=34, w=500)),
         link="scale", label="aynı oda, ters yön: 18 Şubat 1743 (yatan siluet, nedimeler)"),
    # ── 2. s3 (ilk yarı): 31 Ekim 1737 imza masası → belgeye iniş ─────────────────────────────────────────────────────────────────────
    shot("p7_oda", ("c16s3", -0.1), room="oda1743", figure="seated", seal_at=("c16s3", "imzalanan", 0.0), **ODA, kick="31 EKİM 1737",
         cams=[(("c16s3", -0.1), (1700, 40, 1.3)), (("c16s3", "sözleşmeye", 0.0), (1820, 50, 1.5)), (("c16s3", "denir;", -0.3), (1900, 80, 2.4)), (("c16s3", "bir", -0.15), K0.DOC_FILL)],
         ovl=ov(L.tag("ÇOĞU ZAMAN: BAĞIŞ", 960, 150, ("c16s3", "çoğu", -0.1), size=40, w=700, out=("c16s3", "bir", -0.2))),
         tr=("candle", 1.0, dict(at=(960, 640), at_b=(1500, 540))), link="light", label="31 Ekim 1737 imza masası → belge"),
    # ── 3. s3 (ikinci yarı): belge — bağış değil, devir koşulu; Lorraine'in kabulü ────────────────────────────────────────────────────
    shot("c0_belge", ("c16s3", "bir", -0.15), mode="night", perde=3,
         cams=[(("c16s3", "bir", -0.15), (0, 0, 0.97)), (("c16s3", "devir", -0.2), (100, 40, 1.15)), (("c16s3", "Lorraine,", -0.1), (260, 160, 1.35)), (("c16s3", "kabul", 0.4), (300, 200, 1.42))],
         seals=(("c16s3", "bir", 0.1), ("c16s3", "Lorraine,", 0.0)), names_at=("ANNA MARIA LUISA", "LORRAINE TARAFI", ("c16s3", "bir", 0.2), ("c16s3", "Lorraine,", 0.2)),
         num_at=("c16s3", "bir", 0.1), num_dur=1.0, fr_at=None,
         ovl=ov(L.tag("BAĞIŞ", 250, 330, ("c16s3", "bir", 0.0), size=44, w=300),
                L.stamp("AKADEMİK YORUM", 1620, 270, ("c16s3", "akademik", -0.1), size=44, rot=-0.06),
                L.tag("DEVİR KOŞULU", 1620, 440, ("c16s3", "devir", -0.1), size=38, w=430),
                L.tag("ÇIKARILAMAZ", 1620, 600, ("c16s3", "çıkarılamayacağını", -0.3), size=38, w=430),
                L.icon("keys", 1620, 730, 130, ("c16s3", "çıkarılamayacağını", -0.2), metal="silver"),
                L.stamp("KABUL", 1220, 860, ("c16s3", "kabul", -0.1), size=60, rot=-0.07)),
         tr=("zoomthru", 0.9, dict(at=(960, 520), at_b=(960, 520))), link="scale", cam=("push", 0.07), label="belge: bağış değil devir koşulu; Lorraine kabul eder"),
    # ── 4. s4–s6: c0'ın Büyük Dukalık haritasına dönüş — yağmayı hukuken önleme; özet kartı SÖZ DEĞİL; uygulama bilinmiyor ─────────────
    shot("c16_harita", ("c16s4", -0.1), mode="day", perde=3, approx=False,
         cams=[(("c16s4", -0.1), (11.2, 43.5, 4.6)), (("c16s5", "Hiçbir", 0.0), (11.12, 43.4, 5.6)), (("c16s6", -0.1), (11.2, 43.6, 4.9))],
         regions=[dict(name="c0_toskana", color="ochre", at=("c16s4", -0.1), alpha=0.6, dur=1.2)],
         cities=[dict(lon=11.25, lat=43.77, name="FLORANSA", kind="capital", at=("c16s4", "Floransa'nın", -0.2), size=34)],
         icons_=[dict(kind="crown", route=[(14.2, 44.9), (13.2, 44.5), (12.45, 44.0)], at=("c16s4", "hanedanın", -0.2), move_at=("c16s4", "hanedanın", -0.1), move_dur=1.8, size=96, metal="gold")],
         cam=("push", 0.06),
         extra=functools.partial(K0.sinir_extra, label_at=("c16s4", "Floransa'nın", -0.3), items_at=("c16s4", "hazinelerini", -0.3), lock_at=("c16s4", "hukuken", -0.1),
                                 quote_at=("c16s5", "Hiçbir", -0.1), quote_out=("c16s6", "bilmiyoruz", -0.2)),
         ovl=ov(L.tag("UFFIZI'YE GÖRE", 400, 150, ("c16s4", -0.05), size=38, w=500, out=("c16s5", -0.2)),
                L.tag("YENİ HANEDAN", 1500, 330, ("c16s4", "hanedanın", -0.1), size=34, w=420, out=("c16s5", -0.2)),
                L.stamp("HUKUKEN ÖNLEMEK", 1450, 520, ("c16s4", "hukuken", -0.1), size=46, rot=-0.06, out=("c16s5", -0.2)),
                L.tag("ANNA MARIA LUISA", 440, 560, ("c16s5", "Anna", -0.1), size=34, w=480, out=("c16s6", -0.1)),
                L.stamp("BİLİNEN BİR SÖZ DEĞİL", 1380, 575, ("c16s5", "bilinen", -0.15), size=46, rot=-0.07, out=("c16s6", -0.1)),
                L.tag("UYGULAMASI: BİLİNMİYOR", 960, 150, ("c16s6", "uygulandığını", -0.1), size=38, w=640),
                L.icon("question", 1560, 480, 220, ("c16s6", "bilmiyoruz", -0.3), glow=0.3, bob=4)),
         tr=("slide", 0.9, dict(dir="u")), link="dir", label="c0'ın haritasına dönüş: hukuken önleme; özet kartı SÖZ DEĞİL; uygulama bilinmiyor"),
    # ── 5. s7–s8: Medici'ler Rönesans'ı yarattı mı? → tek yaratıcı değil, en görünür patronlardan biri ───────────────────────────────
    shot("c16_patron", ("c16s7", -0.1), mode="day", view="siralama", q_at=("c16s7", -0.1), row_at=("c16s8", -0.1), tek_at=("c16s8", "tek", -0.1), deg_at=("c16s8", "değil", -0.1),
         gor_at=("c16s8", "görünür", -0.1), cam=("push", 0.07), tr=("yikama", 0.9), link="material", label="Rönesans'ı yarattı mı? → patron sırası"),
    # ── 6. s9: kubbe yün loncası; Strozzi · Rucellai · Tornabuoni; Primavera başka kol ─────────────────────────────────────────────
    shot("p7_skyline", ("c16s9", -0.1), mode="day", tod="day", seed=2, pan=0, cam=("push", 0.07),
         ovl=ov(K.bale_ov(1260, 440, ("c16s9", "yün", -0.2), s=1.5),
                L.tag("YÜN LONCASI", 1260, 560, ("c16s9", "Kubbeyi", -0.1), size=38, w=440, sub="KUBBEYİ YAPTIRDI"),
                L.tag("STROZZI", 360, 560, ("c16s9", "Strozzi,", -0.2), size=36, w=300, sub="SİPARİŞ"),
                L.tag("RUCELLAI", 860, 600, ("c16s9", "Rucellai,", -0.2), size=36, w=300, sub="SİPARİŞ"),
                L.tag("TORNABUONI", 1660, 600, ("c16s9", "Tornabuoni", -0.2), size=36, w=380, sub="SİPARİŞ"),
                L.tag("PRIMAVERA", 1560, 190, ("c16s9", "Primavera", -0.2), size=38, w=440, sub="BÜYÜK OLASILIKLA BAŞKA BİR KOL"),
                L.icon("shield", 1560, 330, 110, ("c16s9", "ailenin", -0.2), glow=0.2)),
         tr=("sayfa", 0.9), link="material", label="Floransa: kubbe, üç sipariş, Primavera (başka kol)"),
    # ── 7. s10: Gombrich ↔ Goldthwaite ───────────────────────────────────────────────────────────────────────────────────────────
    shot("c16_tartisma", ("c16s10", -0.1), mode="day", h_at=("c16s10", -0.1), g_at=("c16s10", "Gombrich,", -0.3), uniq_at=("c16s10", "benzersiz", -0.1), tip_at=("c16s10", "tipik", -0.15),
         itiraz_at=("c16s10", "itiraz", -0.1), w_at=("c16s10", "Goldthwaite", -0.25), talep_at=("c16s10", "talebini", -0.15), city_at=("c16s10", "şehirde", -0.1),
         coin_at=("c16s10", "biriken", -0.1), link_at=("c16s10", "bağladı.", -0.5), cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="Gombrich: tipik değil · Goldthwaite: biriken zenginlik"),
    # ── 8. s11: görünürlük kaynaklardan: Vespasiano övdü; Vasari Medici'nin hizmetinde ─────────────────────────────────────────────
    shot("p7_oda", ("c16s11", -0.1), room="calisma", variant="kutuphane", figure="desk", path="scribe", mode="day", cam=("push", 0.07),
         ovl=ov(L.tag("GÖRÜNÜRLÜĞÜN BİR KISMI: KAYNAKLAR", 960, 150, ("c16s11", "Görünürlüğün", -0.1), size=36, w=900, out=("c16s11", "Vespasiano", 0.3)),
                L.tag("VESPASIANO", 520, 250, ("c16s11", "Vespasiano", -0.1), size=38, w=420),
                L.tag("COSIMO'YU ÖVDÜ", 520, 340, ("c16s11", "övdü", -0.2), size=34, w=460),
                L.tag("VASARI", 1400, 250, ("c16s11", "Vasari", -0.1), size=38, w=340),
                L.tag("MEDİCİ'NİN HİZMETİNDE", 1400, 340, ("c16s11", "hizmetindeydi", -0.5), size=34, w=560)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="kütüphane: Vespasiano övdü, Vasari hizmetindeydi"),
    # ── 9. s12: ayıran ölçek ve siyasi görünürlüktü ───────────────────────────────────────────────────────────────────────────────
    shot("c16_patron", ("c16s12", -0.1), mode="day", view="olcek", in_at=("c16s12", -0.1), grow_at=("c16s12", "ölçek", -0.2), spot_at=("c16s12", "siyasi", -0.15), cam=("push", 0.07),
         ovl=ov(L.tag("ÖLÇEK", 330, 300, ("c16s12", "ölçek", -0.15), size=40, w=300),
                L.tag("SİYASİ GÖRÜNÜRLÜK", 1460, 230, ("c16s12", "siyasi", -0.1), size=38, w=600)),
         tr=("yikama", 0.9), link="material", label="Medici'yi ayıran: ölçek ve siyasi görünürlük"),
    # ── 10. s13: SAĞLAMLIK HARİTASI — üç büyük şerit; küçülüp HUD'a oturur ────────────────────────────────────────────────────
    shot("c16_saglam", ("c16s13", -0.1), mode="day", d_at=(("c16s13", "Şimdi", 0.0), ("c16s13", "anlattıklarımızı", 0.0), ("c16s13", "sağlamlığına", -0.15)), shrink_at=("c16s13", "ayıralım", 0.0),
         cam=("push", 0.07), tr=("sayfa", 0.9), link="material", label="sağlamlık haritası: altın SAĞLAM · lacivert NİTELİKLİ · kızıl MİT"),
    # ── 11. s14: çifte kayıt — Medici icat etmedi; Cenova 1340 · Venedik 1407 → MİT ───────────────────────────────────────────────
    shot("p7_map", ("c16s14", -0.1), mode="day", approx=False, perde=3, cam=("push", 0.07),
         cams=[(("c16s14", -0.1), (11.3, 44.4, 5.0)), (("c16s14", "Cenova'da", 0.0), (10.6, 44.6, 5.6))],
         cities=[dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c16s14", "Çifte", -0.2), size=34, side="r")],
         extra=L.mx(L.mpin(GEN[0], GEN[1], ("c16s14", "Cenova'da", -0.15), color="#2F4F8A", label="CENOVA", size=34),
                    L.mpin(VEN[0], VEN[1], ("c16s14", "Venedik'te", -0.15), color="#2F4F8A", label="VENEDİK", size=34),
                    L.marrow([GEN, (10.2, 44.3), FLO], ("c16s14", "çok", -0.1), dur=1.4, color="#2F4F8A", width=6.0, dash=(14, 10), label="ÖNCE"),
                    L.marrow([VEN, (11.9, 44.6), FLO], ("c16s14", "önce", -0.2), dur=1.2, color="#2F4F8A", width=6.0, dash=(14, 10))),
         ovl=ov(L.tag("ÇİFTE KAYIT", 960, 150, ("c16s14", "Çifte", -0.1), size=42, w=520, out=("c16s14", "Cenova'da", 0.4)),
                L.stamp("İCAT ETMEDİ", 1120, 800, ("c16s14", "etmedi;", -0.2), size=56, rot=-0.06),
                L.tag("1340", 420, 380, ("c16s14", "Cenova'da", 0.0), size=44, w=200),
                L.tag("1407", 1500, 300, ("c16s14", "Venedik'te", 0.0), size=44, w=200),
                band([dict(lane=2, label="ÇİFTE KAYIT", at=("c16s14", "icat", -0.1), src=(1100, 780))], "c16s14", (0, 0, 0))),
         tr=("slide", 0.9, dict(dir="u")), link="dir", label="çifte kayıt: Cenova 1340 / Venedik 1407 → MİT"),
    # ── 12. s15: opera ve piyano — Medici sarayında doğdu, icat onların değil → NİTELİKLİ ─────────────────────────────────────────
    shot("c16_sahne", ("c16s15", -0.1), mode="day", op_at=("c16s15", "Opera", -0.1), pi_at=("c16s15", "piyano", -0.2), no_at=("c16s15", "onların", -0.2), cam=("push", 0.07),
         ovl=band([dict(lane=1, label="OPERA · PİYANO", at=("c16s15", "ortaya", -0.2), src=(960, 650))], "c16s15", (0, 0, 1)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="opera ve piyano: sarayda ortaya çıktı, icat değil → NİTELİKLİ"),
    # ── 13. s16: Uffizi ilk modern müze mi? Capitoline 1734 → MİT ──────────────────────────────────────────────────────────────────
    shot("c16_muze", ("c16s16", -0.1), mode="day", view="iki", u_at=("c16s16", -0.1), ilk_at=("c16s16", "ilk", -0.2), oysa_at=("c16s16", "oysa", -0.1), c_at=("c16s16", "Roma'daki", -0.2),
         ac_at=("c16s16", "halka", -0.3), cam=("push", 0.07),
         ovl=band([dict(lane=2, label="UFFIZI: İLK", at=("c16s16", "oysa", 0.0), src=(520, 330))], "c16s16", (0, 1, 1)),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="Uffizi ↔ Capitoline 1734 → MİT"),
    # ── 14. s17: Medici → Fugger → Rothschild: benzetme, bağ yok → MİT ─────────────────────────────────────────────────────────────
    shot("c16_patron", ("c16s17", -0.1), mode="day", view="zincir", in_at=("c16s17", -0.1), l1_at=("c16s17", "Fugger'e,", -0.3), l2_at=("c16s17", "Rothschild'e", -0.3), bn_at=("c16s17", "benzetmeden", -0.1),
         no_at=("c16s17", "süreklilik", -0.1), cam=("push", 0.07),
         ovl=band([dict(lane=2, label="FUGGER, ROTHSCHILD", at=("c16s17", "benzetmeden", 0.0), src=(960, 480))], "c16s17", (0, 1, 2)),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="Medici'den Rothschild'e zincir: benzetme → MİT"),
    # ── 15. s18: banka resmen 1494'te bitti; çözülme şube şube; suçlu tek kişi değil → NİTELİKLİ ──────────────────────────────────
    shot("p7_map", ("c16s18", -0.1), mode="day", approx=False, perde=3, cam=("push", 0.07),
         cams=[(("c16s18", -0.1), (7.2, 46.4, 2.6)), (("c16s18", "çözülme", 0.0), (6.4, 46.6, 2.9))],
         cities=[dict(lon=FLO[0], lat=FLO[1], name="FLORANSA", kind="capital", at=("c16s18", "Banka", -0.2), size=32, side="r")],
         extra=L.mx(*[L.mglow(lo, la, ("c16s18", "Banka", -0.1), out=("c16s18", "şube", 0.1 + 0.42 * i), r=26.0) for i, (lo, la) in enumerate([(12.5, 41.9), (12.33, 45.44), (9.19, 45.46), (6.14, 46.2), (4.83, 45.76), (3.22, 51.21), (-0.12, 51.5)])],
                    *[L.mpin(lo, la, ("c16s18", "Banka", -0.1), color="#D9A532", out=("c16s18", "şube", 0.1 + 0.42 * i), r=9.0, ring=False) for i, (lo, la) in enumerate([(12.5, 41.9), (12.33, 45.44), (9.19, 45.46), (6.14, 46.2), (4.83, 45.76), (3.22, 51.21), (-0.12, 51.5)])]),
         ovl=ov(L.stamp("1494: RESMEN BİTTİ", 1380, 190, ("c16s18", "1494'te", -0.15), size=52, rot=-0.05),
                L.tag("ÇOK ÖNCEDEN", 960, 880, ("c16s18", "çok", -0.1), size=36, w=440),
                L.tag("ŞUBE ŞUBE", 1540, 880, ("c16s18", "şube", -0.1), size=36, w=380),
                L.tag("SUÇLU TEK KİŞİ DEĞİL", 960, 760, ("c16s18", "suçlu", -0.1), size=38, w=640),
                band([dict(lane=1, label="BANKA 1494", at=("c16s18", "resmen", -0.1), src=(960, 460))], "c16s18", (0, 1, 3))),
         tr=("yikama", 0.9), link="material", label="banka resmen 1494'te bitti; şube şube söner → NİTELİKLİ"),
    # ── 16. s19: defterler — Floransa Devlet Arşivi ve Harvard → NİTELİKLİ ────────────────────────────────────────────────────────
    shot("p7_map", ("c16s19", -0.1), mode="day", approx=False, perde=3, cam=("push", 0.07),
         cams=[(("c16s19", -0.1), (11.3, 43.9, 3.4)), (("c16s19", "Arşivi'nde,", 0.0), (11.3, 43.9, 3.0)), (("c16s19", "kısmı", 1, -0.4), (-28.0, 43.0, 0.66))],
         extra=L.mx(L.mpin(FLO[0], FLO[1], ("c16s19", "Floransa", -0.2), color="#B03020", size=30),
                    L.mpin(CAM[0], CAM[1], ("c16s19", "Harvard'da.", -0.2), color="#2F4F8A", size=30),
                    L.marrow([FLO, (-20.0, 52.0), CAM], ("c16s19", "kısmı", 1, -0.3), dur=1.7, color="#7A5C32", width=7.0, dash=(16, 11))),
         ovl=ov(L.icon("book", 960, 330, 150, ("c16s19", "defterlerinin", -0.2), out=("c16s19", "Floransa", 0.3)),
                L.tag("FLORANSA DEVLET ARŞİVİ", 760, 760, ("c16s19", "Floransa", 0.0), size=36, w=640, out=("c16s19", "Harvard'da.", -0.5)),
                L.tag("HARVARD", 560, 760, ("c16s19", "Harvard'da.", -0.1), size=42, w=360, sub="AİLENİN BİR KOLUNUN DEFTERLERİ"),
                band([dict(lane=1, label="DEFTERLER", at=("c16s19", "Harvard'da.", 0.2), src=(960, 500))], "c16s19", (0, 2, 3))),
         tr=("slide", 0.9, dict(dir="r")), link="dir", label="defterler: Floransa Devlet Arşivi ↔ Harvard → NİTELİKLİ"),
    # ── 17. s20: banka öldü; kurumlar kaldı: Opificio çalışıyor, Uffizi 1769 → SAĞLAM ───────────────────────────────────────────────
    shot("c16_kurum", ("c16s20", -0.1), mode="day", ledger_at=("c16s20", "Banka", -0.1), kurum_at=("c16s20", "kurumlar", -0.15), opif_at=("c16s20", "Opificio", -0.2), work_at=("c16s20", "Pietre", -0.2),
         bugun_at=("c16s20", "bugün", -0.1), uffizi_at=("c16s20", "Uffizi", -0.2), yil_at=("c16s20", "1769'dan", -0.1), acik_at=("c16s20", "halka", -0.1), cam=("push", 0.07),
         ovl=band([dict(lane=0, label="OPIFICIO", at=("c16s20", "çalışıyor,", -0.1), src=(960, 560)), dict(lane=0, label="UFFIZI 1769", at=("c16s20", "1769'dan", 0.0), src=(1560, 560))],
                  "c16s20", (0, 3, 3)),
         tr=("sayfa", 0.9), link="material", label="banka öldü; kurumlar kaldı: Opificio + Uffizi 1769 → SAĞLAM"),
    # ── 18. s21: düzelttiğimiz hikâyeler bir arada ───────────────────────────────────────────────────────────────────────────────
    shot("c16_mit_tablo", ("c16s21", -0.1), mode="day", start_at=("c16s21", -0.1), head_at=("c16s21", "düzelttiğimiz", -0.5), dt=0.40, cam=("push", 0.06),
         tr=("yikama", 0.9), link="material", label="mit kapanış tablosu: düzeltilen hikâyeler"),
    # ── 19. s22: mezar yakın zamanda açıldığında — ayrı kap; ölüm nedeni belirsiz (sessiz, ağır) ────────────────────────────────
    shot("c16_mezar", ("c16s22", -0.1), mode="night", perde=3, open_at=("c16s22", "açıldığında", -0.2), date_at=("c16s22", "yakın", 0.0), kap_at=("c16s22", "ayrı", -0.1), bel_at=("c16s22", "belirsiz", -0.3),
         cam=("push", 0.07), tr=("dip", 1.0), link="light", label="mezar (2012–13): ayrı kap; ölüm nedeni belirsiz"),
    # ── 20. s23 (ilk yarı): her 18 Şubat'ta tarihî alay ───────────────────────────────────────────────────────────────────────────
    shot("p7_procession", ("c16s23", -0.1), mode="day", dir="r", density=0.8, mix=dict(banner=0.30, noble=0.22, page=0.18, guard=0.10, elder=0.10, cleric=0.06, common=0.04),
         pan=("r", 700), speed=110.0, seed=4,
         ovl=ov(L.date_plate("18 ŞUBAT", ("c16s23", "18", -0.1)),
                L.tag("ANNA MARIA LUISA'YI ANAR", 1250, 160, ("c16s23", "Anna", -0.1), size=38, w=760),
                L.tag("TARİHÎ ALAY", 1250, 250, ("c16s23", "tarihî", -0.1), size=34, w=420)),
         cam=("push", 0.07), tr=("light", 0.9, dict(at=(1560, 640))), link="light", label="her 18 Şubat: tarihî alay"),
    # ── 21. s23 (ikinci yarı): Palazzo Vecchio'dan Medici Şapelleri'ne yürünür; belediye müzeleri ücretsiz ───────────────────────────
    shot("c16_yuruyus", ("c16s23", "Palazzo", -0.2), mode="day", pv_at=("c16s23", "Palazzo", -0.2), route_at=("c16s23", "Palazzo", -0.1), walk_at=("c16s23", "Palazzo", 0.1), walk_dur=3.4,
         ch_at=("c16s23", "Şapelleri'ndeki", -0.3), ticket_at=("c16s23", "belediye", -0.2), free_at=("c16s23", "ücretsizdir.", -0.35), cam=("push", 0.07),
         tr=("carry", 0.9, dict(strip="paper", dir="r")), link="carry", label="yürüyüş: Palazzo Vecchio → Medici Şapelleri; müzeler ücretsiz"),
    # ── 22. s24: Para gitti, banka gitti (florin söner; defter söner) ───────────────────────────────────────────────────────────────
    shot("c16_para", ("c16s24", -0.1), mode="night", perde=3, gone_at=("c16s24", "gitti,", -0.1), ledger_at=("c16s24", "banka", -0.1), gone2_at=("c16s24", "gitti.", -0.1),
         cam=("push", 0.07), tr=("dip", 1.0), link="light", label="Para gitti, banka gitti"),
    # ── 23. s25: SESSİZ SON — c0'ın açılış skyline'ı, kamera TERS; tek ışık; yaldız cümle; fener noktaları; ağır kararma ────────────
    shot("p7_skyline", ("c16s25", -0.1), mode="night", tod="dusk", seed=2, pan=300, perde=3, cam=("pan", "l", 300), longtake=True,
         ovl=ov(K.window_glow(330, 700, ("c16s25", "kadının", -0.2), r=150.0),
                K.gold_script(("c16s25", "imzaladığı", -0.2), y=250.0, dur=1.9),
                K.lantern_dots(("c16s25", "her", -0.1), y=786.0, dur=6.5),
                K.end_dim(("c16s25", "anan", -0.2), alpha=0.72, dur=2.6)),
         tr=("dip", 1.2), link="light", label="son: c0'ın skyline'ı ters yönde; tek ışık; fener noktaları; kararma"),
]
YIL_AT = [(("c16s1", "1743.", 0.0), 1743), (("c16s3", 0), 1737), (("c16s16", "Capitoline", 0.0), 1734), (("c16s18", "1494'te", 0.0), 1494), (("c16s20", "1769'dan", 0.0), 1769),
          (("c16s22", 0), 2013), (("c16s23", 0), 2026)]
