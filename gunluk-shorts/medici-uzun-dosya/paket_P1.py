#!/usr/bin/env python3
"""Parça 1 YouTube Studio paketi: başlık, açıklama, sabit yorum, etiketler, bölümler — zaman damgaları out_p1/timeline.json'dan.

  python3 paket_P1.py            # yayin/studio_paketi_P1/00–05 dosyalarını (00: yayın adımları) yazar, altyazıyı kopyalar ve denetler
Kurul tur 1 (kurul/KURUL.md, bölüm E; PK1 3c–3g, KA2-E2): T1 başlık, ilk 2 satır vaadi, dürüst yöntem cümlesi, gerçek kaynak listesi,
soru önde sabit yorum, P1'de olmayan adlar etiketten çıkar. Bölüm damgaları cümle çapasına bağlı: ses/kurgu değişince yeniden çalıştır.
Denetimler: ilk bölüm 0:00, açıklamadaki ilk zaman damgası 0:00 (listeden önce damga yok; PK1-Y1), her bölüm ≥ 10 sn, başlık ≤ 60 karakter (kapı 4),
açıklama ≤ 5000, etiketler toplamı ≤ 500 karakter.
"""
import json
import math
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out_p1")
PK = os.path.join(HERE, "yayin", "studio_paketi_P1")

BASLIK = "Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?"

# (çapa, başlık): çapa = cümle kimliği (cümle başı) | "bolum:cN" (önceki bölümün sonu: bölüm kartı dahil) | 0
BOLUMLER = [
    (0, "Son Medici ve 1737 sözleşmesi"),
    ("bolum:c1", "Florin: Floransa kendi altınını basıyor (1252)"),
    ("c1s11", "Kara Veba (1348)"),
    ("c1s15", "Ciompi isyanı (1378)"),
    ("c1s24", "Giovanni di Bicci ve ilk sermaye (1397)"),
    ("bolum:c2", "Faiz yasağı, kambiyo ve \"vicdan komitesi\""),
    ("c2s12", "Çifte kayıt: Medici'nin icadı mı?"),
    ("c2s15", "Cossa, papalık ve Medici'nin kasası"),
    ("c2s22", "Catasto: Floransa servetini sayıyor (1427)"),
]

KAYNAKLAR = """KAYNAKLAR
Birincil metinler:
• Giovanni Villani, Nuova Cronica (florinin basılması, 1338 nüfusu ve okullar, Bardi–Peruzzi ve III. Edward)
• Giovanni Boccaccio, Decameron, Birinci Gün, Giriş (1348 vebası)
• Marchionne di Coppo Stefani, Floransa Kroniği, Rubrica 634 (Delizie degli eruditi toscani XIII baskısı; RIS baskısında rub. 643): veba ve toplu mezarlar
• Dante, Cennet IX, 127–132 ("lanetli çiçek")
• Niccolò Machiavelli, Floransa Tarihi, III–IV. kitaplar (1378 olayları, Giovanni di Bicci'nin ölümü)
• Giovanni Cavalcanti, Floransa Tarihi, IV. kitap (Giovanni'nin son sözleri)
Araştırmalar ve veri tabanları:
• Raymond de Roover, The Rise and Decline of the Medici Bank, 1397–1494 (1963)
• Dizionario Biografico degli Italiani (Treccani): Giovanni di Bicci de' Medici, Giovanni Villani, Michele di Lando, Marchionne di Coppo Stefani, XXIII. Johannes (Baldassarre Cossa; karşı papa), Anna Maria Luisa de' Medici maddeleri
• Stefano Casciu, "Principessa di gran saviezza…", La Principessa saggia (Livorno 2006), s. 30–57 (Aile Sözleşmesi: on üç madde, Fransızca özgün, III. madde)
• Online Catasto of 1427 (yay. D. Herlihy, C. Klapisch-Zuber, R. B. Litchfield, A. Molho; Brown Üniversitesi): 1427 servet sayımı
Anlatımda anılan:
• Tim Parks, Medici Money (2005): kitabın kendisi okunmadı; aktarım kitabın özet notlarına dayanır, aynı bilgi de Roover'da doğrulandı
Rivayetler ekranda ANEKDOT damgasıyla, madalya portreleri TEMSİLÎ damgasıyla işaretlidir; videodaki bütün figürler temsilîdir, gerçek benzerlik iddiası yoktur.{BIRINCIL}"""

BIRINCIL_EK = ""          # KAY teyit tablosu (kurul/teyit_P1.md) sonucu doldurulur: gerçekten okunan birincil metinler


_SAYI = {1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş", 6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz"}
_ONLAR = {1: "on", 2: "yirmi", 3: "otuz", 4: "kırk", 5: "elli"}


def ek(damga, tur="de"):
    """Zaman damgasına bulunma ('de) ya da ayrılma ('den) eki: okunuşun son sözcüğüne göre ünlü uyumu + sert ünsüz.
    '9:53', 'den' → "'ten" (elli üç); '9:54', 'de' → "'te" (elli dört); '5:40', 'de' → "'ta" (kırk)."""
    mm, ss = (int(x) for x in damga.split(":")[-2:])
    n = ss if ss else mm
    w = _SAYI[n % 10] if n % 10 else _ONLAR.get(n // 10, "sıfır")
    unlu = [c for c in w if c in "aıoueiöü"][-1]
    on = unlu in "eiöü"
    sert = w[-1] in "çfhkpsşt"
    if tur == "de":
        return "'" + ("t" if sert else "d") + ("e" if on else "a")
    return "'" + ("t" if sert else "d") + ("en" if on else "an")


def ts(t):
    t = int(math.floor(max(0.0, t)))
    return f"{t // 60}:{t % 60:02d}" if t < 3600 else f"{t // 3600}:{(t % 3600) // 60:02d}:{t % 60:02d}"


def zamanlar():
    tl = json.load(open(os.path.join(OUT, "timeline.json"), encoding="utf-8"))
    sent = {s["id"]: s for s in tl["sentences"]}
    ch = {c["id"]: c for c in tl["chapters"]}
    order = [c["id"] for c in tl["chapters"]]
    out = []
    for a, ad in BOLUMLER:
        if a == 0:
            t = 0.0
        elif isinstance(a, str) and a.startswith("bolum:"):
            cid = a.split(":")[1]
            prev = order[order.index(cid) - 1]
            t = ch[prev]["t1"]                         # bölüm kartı dahil (make_srt ile aynı kural)
        else:
            t = sent[a]["t0"] - 0.25
        out.append((t, ad))
    return out, tl


def video_suresi():
    """Yükleme dosyasının süresi (sn): ffprobe; dosya yoksa anlatım sonu + compose.TAIL (8,3 sn)."""
    import subprocess
    v = os.path.join(OUT, "medici_P1.mp4")
    if os.path.exists(v):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v],
                           capture_output=True, text=True)
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    tl = json.load(open(os.path.join(OUT, "timeline.json"), encoding="utf-8"))
    return float(tl.get("total", 0.0)) + 8.3


def bitis_zamanlari(dur):
    """YouTube bitiş ekranı başlangıcı ve videodaki yuvaların tam göründüğü an (sn). Çıkış çekimi videonun son compose.OUTRO saniyesi;
    yuvalar çıkış başından compose.OUTRO_SLOT_FULL sn sonra tam görünür (yoksa eski değer 3,5). Öğeler yuvalardan 0,5 sn önce başlar;
    YouTube en az 5 sn ister."""
    try:
        import compose
        outro, full = float(compose.OUTRO), float(getattr(compose, "OUTRO_SLOT_FULL", 3.5))
    except Exception:                                      # noqa: BLE001
        outro, full = 7.0, 3.5
    yuva = dur - outro + full
    # Öğeler yuvalar TAM göründükten sonraki ilk tam saniyede başlar (kurul tur 3 PK2-N2: 9:52,0'da kule hâlâ silinmenin altında,
    # çerçeveler 9:52,3'te soluk, 9:52,9'da tam → 9:53). YouTube en az 5 sn ister; sığmazsa son 5 sn.
    es = math.ceil(yuva)
    if dur - es < 5.0:
        es = math.floor(dur - 5.0)
    return int(es), math.floor(yuva)


def yayin_adimlari(bol, kambiyo, dur):
    """00_yayin_adimlari.txt (kurul tur 2, PK1-Y3; PK2-Y2): Studio'da sırayla uygulanacak adımlar."""
    es_s, yuva_s = bitis_zamanlari(dur)
    es, yuva = ts(es_s), ts(yuva_s)
    mm, ss = divmod(dur, 60)
    sure = f"{int(mm)}:{int(ss):02d}"
    ilk, son = bol[0][1], bol[-1]
    return f"""YAYIN ADIMLARI: Medici Parça 1/7
(paket_P1.py üretir; değiştirmek için betiği düzelt ve yeniden çalıştır. Kaynak: kurul tur 2, PK1-Y3.)

Bütün işlemler YouTube Studio'da (studio.youtube.com) yapılır. Adımları sırayla uygula.

0. YÜKLEMEDEN ÖNCE
- Kulak kontrolü: yayin/KULAK_KONTROL_P1.md içindeki klipleri dinle (14 yamalı cümle + orijinal kayıttan 2 yer). Yanlış okunan bir yer varsa yalnız o cümle yeniden seslendirilir (ElevenLabs kredisi harcar; senin onayınla).
- Kayıt için: ElevenLabs hesabında "Emrullah" kütüphane sesinin kullanım koşullarının ekran görüntüsünü al (SURUM_KUNYESI_P1.md, lisans notu).

DOSYALAR (bu klasör: yayin/studio_paketi_P1/)
- medici_P1.mp4: video, {sure}, 1920×1080. Depoda yok; ayrıca gönderilir.
- kapak_P1_K1.jpg: VARSAYILAN kapak ("SON MEDİCİ / MİRASI KİLİTLEDİ").
- kapak_P1_K2.jpg: test kapağı ("FAİZ YASAKTI").
- 01_baslik.txt, 02_aciklama.txt, 03_sabit_yorum.txt, 04_etiketler.txt (05_bolumler.txt açıklamanın içinde zaten var).
- medici_P1_tr.srt: Türkçe altyazı. Telefonda .srt seçilemezse medici_P1_tr.vtt.
- ESKI_kapaklar/: YÜKLEME (eski sürüm).

1. YÜKLE
1) Oluştur → Video yükle → medici_P1.mp4.
2) Ayrıntılar:
   - Başlık: {BASLIK}
   - Açıklama: 02_aciklama.txt'nin TAMAMI ({len(bol)} bölüm damgası içinde). Açıklamaya başka zaman damgası EKLEME: ilk damga 0:00 olmalı, yoksa bölümler oluşmayabilir.
   - Küçük resim: kapak_P1_K1.jpg. İlk yüklenen kapak varsayılan kalır; videonun ilk 3 saniyesi bu kapağın yankısıdır.
     Kanalda "Test ve karşılaştır" açıksa K2'yi de ekle (3. bölüm).
   - Oynatma listesi: "Medici (7 parça)". Yoksa "Yeni oynatma listesi" ile oluştur; açıklaması: "Floransa'nın bankacı ailesi Medici, 1252'den 1743'e: yedi parça, her biri yaklaşık on dakika."
   - Kitle: "Hayır, çocuklara özel değil". Yaş sınırı yok.
   - Daha fazla göster:
     · Ücretli tanıtım: yok.
     · "Değiştirilmiş veya yapay içerik": Hayır (kanal uygulaması: video kodla çizilmiş animasyon, gerçek kişi ya da olay gerçekçi biçimde üretilmedi; yapay zekâ sesi açıklamanın sonunda yazılı). Kurul üyesi KA2'nin şerhi: YouTube Yardım metnine dayanarak "Evet" öneriyor. Son karar senin.
     · Etiketler: 04_etiketler.txt.
     · Video dili: Türkçe. Altyazı sertifikası: gerekmez. Kategori: Eğitim.
     · Otomatik bölümler: açık kalabilir; açıklamadaki damgalar önceliklidir.
3) Video öğeleri:
   - Altyazı ekle → Dosya yükle → "Zamanlamalı" → medici_P1_tr.srt (dil: Türkçe).
   - Bitiş ekranı: {es}{ek(es, 'den')} videonun sonuna kadar (YouTube en az 5 sn istiyor). Videodaki iki çerçeve {yuva}{ek(yuva, 'de')} belirir:
     · Sol çerçeve ("SIRADAKİ PARÇA"): P2 yayınlanana dek "İzleyiciye en uygun video" öğesi (YouTube seçer). Yalnız bu videoyu içeren
       oynatma listesini KOYMA: izleyiciyi aynı videoya döndürür (kurul PK2-Y2). P2 yayınlanınca bu öğeyi P2 videosuyla değiştir.
     · Sağ çerçeve ("ABONE OL · ZAMAN KURYESİ"): "Abone ol" öğesi.
     Öğeleri çerçevelerin üstüne yerleştir, dışına taşırma.
4) Görünürlük: Planla → Pazar 20:00 (GMT+3). Parçalar arası bir hafta.

2. YAYINDAN HEMEN SONRA
- Sabit yorum: 03_sabit_yorum.txt'yi kanal hesabıyla yorum olarak yaz → ⋮ → Sabitle. İçindeki {kambiyo} tıklanabilir bağlantı olur.
- Bölümler: ilerleme çubuğunda {len(bol)} bölüm görünmeli ("0:00 {ilk}" … "{ts(son[0])} {son[1]}"). Görünmüyorsa açıklamayı bir kez daha kaydet; yine yoksa bana yaz.
- Altyazı: CC düğmesinde "Türkçe" görünmeli (otomatik altyazı değil, yüklediğin dosya).
- P2'nin yayın tarihi kesinleşince sabit yorumun son satırına yaz (ör. "Sıradaki: 2/7, Pazar 20:00"). Videodaki "SIRADAKİ PARÇA · 2/7" çerçevesine
  ilk hafta YouTube başka bir video koyar; bu satır izleyiciye P2'nin ne zaman geleceğini söyler (kurul PK2-N2).
- P2 YAYINLANDIĞI GÜN: bu videonun bitiş ekranında sol öğeyi ("İzleyiciye en uygun video") P2 videosuyla değiştir.

3. KAPAK TESTİ ("Test ve karşılaştır")
- K1 + K2; test sürerken başlığa dokunma; 14 gün ya da YouTube sonuç verene kadar.
- YouTube kazananı TO'ya göre değil izlenme süresi payına göre seçer. Test sonuçsuz biterse ilk yüklenen kapak (K1) kalır.
- K2 kazanırsa açılışı kırpma: ilk cümle ("18 Şubat 1743, Floransa.") K1 yankısının altında başlıyor ve test sonucu bu açılışla ölçüldü.
- Özellik hesapta yoksa: K1 ile 72 saat bekle. Gösterim başına izlenme süresine bak (TO × ortalama izleme süresi). 2–3 gün yeni gösterim dalgası gelmezse K2'ye geç ve aynı trafik kaynağında (Göz at) önce/sonra karşılaştır.

4. ANALİZ (48. saat ve 7. gün)
- Studio → Analytics: Erişim (gösterim, TO, trafik kaynakları), Etkileşim (ortalama izleme süresi, izleyici tutma eğrisi, 0:30'da kalan %), Kitle. Ekran görüntülerini bana gönder; dersler CLAUDE.md'ye yazılır.
- Kıyas: 0:30'da kalan (en iyisi Şarlken, %79), ortalama izlenme %40 ve üstü iyi, gösterim başına izlenme süresi.

5. SONRAKİ BAŞLIK TESTİ İÇİN (kapak testi bittikten sonra; her seferinde tek değişken)
- T2: Medici (1/7): Son Medici Mirasını Kilitledi. Peki Nasıl?
- T3: Medici Ailesi (1/7): Faiz Yasaktı, Kilise Müşteri Oldu (kaynak üyeleri KA1 ve KA2 kurul tur 3'te onayladı: de Roover, papalık mevduatı ve Camera Apostolica; ironi kurumun maliyesine yönelik, inanca değil).
"""


def main():
    bol, tl = zamanlar()
    hata = []
    if bol[0][0] != 0:
        hata.append("ilk bölüm 0:00 değil")
    for (t0, a0), (t1, a1) in zip(bol, bol[1:]):
        if t1 - t0 < 10:
            hata.append(f"bölüm < 10 sn: {a0}")
    if len(BASLIK) > 60:
        hata.append(f"başlık {len(BASLIK)} > 60")
    bol_txt = "\n".join(f"{ts(t)} {ad}" for t, ad in bol)
    kambiyo = ts(dict((a, t) for t, a in bol)["Faiz yasağı, kambiyo ve \"vicdan komitesi\""])
    aciklama = f"""Medici Ailesi (1/7): Kilise faizi yasaklamıştı; bir bankacı ailesi yine de para kazanmanın yolunu buldu.
1743'te son Medici'nin ölümünden 1252'de basılan ilk florine geri sarıyoruz; faiz yasağı ve "vicdan komitesi" de bu parçada.

18 Şubat 1743, Floransa. Yetmiş beş yaşında bir kadın ölüyor: Toskana'yı yönetmiş Medici hattının son üyesi Anna Maria Luisa. 31 Ekim 1737'de imzalanan Aile Sözleşmesi'nin 3. maddesine göre ailenin galerileri, tabloları, heykelleri ve kütüphaneleri Floransa'dan ve Büyük Dukalık'tan çıkarılamayacaktı. Peki bir bankacı ailesi, mirasını bir şehre bağlayacak noktaya nasıl geldi?

Medici'nin hikâyesi yedi parçada. Bu ilk parçada o odadan geriye, florin şehrine gidiyoruz: altın florinin doğuşu, veba ve Ciompi isyanı, Giovanni di Bicci'nin bankası, kambiyo, çifte kayıt ve "vicdan komitesi".

Kaynak niteliği ekranda damgalarla (ANEKDOT, MİT, "… göre") ve anlatımda "göre / aktarılır" kipleriyle belirtilir. Sözleşmenin 3. maddesi, Dante dizesi ve Machiavelli ile Cavalcanti'den aktarılan sözlerin Türkçeleri bize aittir; Machiavelli ve Cavalcanti'nin sözleri özetle aktarılmıştır, ekrandaki İtalyanca satırlar özgün metinlerden kısa alıntılardır. Önemli çelişkilerde (Cossa'nın kurtarılması, Giovanni'nin son sözleri) bunu videoda açıkça söylüyoruz.

BÖLÜMLER
{bol_txt}

{KAYNAKLAR.replace("{BIRINCIL}", BIRINCIL_EK)}

Sıradaki: 2/7, Cosimo'nun kulesi, sürgün ve dönüş.

Ses: yapay zekâ ile üretilmiş anlatıcı sesi (ElevenLabs, "Emrullah"). Çizim, harita ve animasyonların tamamı kodla üretilmiştir; müzik ve ses efektleri sentezdir. Haritalardaki sınırlar yaklaşıktır.

#Medici #Floransa #Rönesans #TarihBelgeseli
"""
    yorum = f"""Soru: Kilise faizi yasaklamıştı; bankacılar kambiyo ve "faiz değil, hediye" gibi yollar buldu ({kambiyo}). Sizce bu zekâ mıydı, dolambaçlı yol mu?
Rakam ve tarihlerin dayanakları açıklamadaki kaynaklardır (1427 sayımı için Online Catasto of 1427); rivayetler videoda ANEKDOT, madalya portreleri TEMSİLÎ damgasıyla işaretlidir; bütün figürler temsilîdir. Tam kaynak ve teyit tablosunu isteyene paylaşırız.
Sıradaki: 2/7, Cosimo'nun kulesi, sürgün ve dönüş.
"""
    etiket = ["Medici", "Medici Ailesi", "Medici Ailesi Tarihi", "Mediciler", "Medici bankası", "faiz yasağı", "kambiyo",
              "Orta Çağ bankacılığı", "Floransa", "Floransa tarihi", "Rönesans", "Florin", "Giovanni di Bicci", "Ciompi İsyanı",
              "Kara Veba", "çifte kayıt", "bankacılık tarihi", "Anna Maria Luisa de Medici", "İtalya tarihi", "tarih belgeseli",
              "Zaman Kuryesi"]
    et_txt = ", ".join(etiket)
    if len(et_txt) > 500:
        hata.append(f"etiketler {len(et_txt)} > 500")
    if len(aciklama) > 5000:
        hata.append(f"açıklama {len(aciklama)} > 5000")
    # YouTube bölümleri: açıklamadaki İLK zaman damgası 0:00 olmalı (kurul tur 2, PK1-Y1); listeden önce damga yazma
    ilk = re.search(r"(?<![\d:])\d{1,2}:\d{2}(?::\d{2})?(?![\d:])", aciklama)
    if not ilk or ilk.group(0) != "0:00":
        hata.append(f"açıklamadaki ilk damga {ilk.group(0) if ilk else 'yok'} (0:00 olmalı)")
    if not aciklama.split("BÖLÜMLER\n", 1)[-1].startswith("0:00 "):
        hata.append("bölüm listesi 0:00 ile başlamıyor")
    os.makedirs(PK, exist_ok=True)
    open(os.path.join(PK, "01_baslik.txt"), "w", encoding="utf-8").write(BASLIK + "\n")
    open(os.path.join(PK, "02_aciklama.txt"), "w", encoding="utf-8").write(aciklama)
    open(os.path.join(PK, "03_sabit_yorum.txt"), "w", encoding="utf-8").write(yorum)
    open(os.path.join(PK, "04_etiketler.txt"), "w", encoding="utf-8").write(et_txt + "\n")
    open(os.path.join(PK, "05_bolumler.txt"), "w", encoding="utf-8").write(bol_txt + "\n")
    open(os.path.join(PK, "00_yayin_adimlari.txt"), "w", encoding="utf-8").write(yayin_adimlari(bol, kambiyo, video_suresi()))
    # altyazı paketin içinde de güncel olsun (make_srt.py yayin/ altına yazar)
    import shutil
    for uz in ("srt", "vtt"):
        kay = os.path.join(HERE, "yayin", f"medici_P1_tr.{uz}")
        if os.path.exists(kay):
            shutil.copy2(kay, os.path.join(PK, f"medici_P1_tr.{uz}"))
    # YAYIN_TASLAK'ın gösterdiği eski konum da aynı listeyi taşısın (kurul tur 2, PK1-Y2)
    open(os.path.join(HERE, "yayin", "bolumler_P1.txt"), "w", encoding="utf-8").write(bol_txt + "\n")
    print(f"başlık ({len(BASLIK)}): {BASLIK}")
    print(bol_txt)
    print(f"açıklama {len(aciklama)} kar., etiketler {len(et_txt)} kar., anlatım sonu {ts(tl['total'] if 'total' in tl else 0)}")
    if hata:
        raise SystemExit("PAKET HATASI: " + "; ".join(hata))
    print("paket yazıldı:", PK)


if __name__ == "__main__":
    main()
