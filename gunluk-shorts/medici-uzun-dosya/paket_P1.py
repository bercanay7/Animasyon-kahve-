#!/usr/bin/env python3
"""Parça 1 YouTube Studio paketi: başlık, açıklama, sabit yorum, etiketler, bölümler — zaman damgaları out_p1/timeline.json'dan.

  python3 paket_P1.py            # yayin/studio_paketi_P1/01–05 dosyalarını yazar ve denetler
Kurul tur 1 (kurul/KURUL.md, bölüm E; PK1 3c–3g, KA2-E2): T1 başlık, ilk 2 satır vaadi, dürüst yöntem cümlesi, gerçek kaynak listesi,
soru önde sabit yorum, P1'de olmayan adlar etiketten çıkar. Bölüm damgaları cümle çapasına bağlı: ses/kurgu değişince yeniden çalıştır.
Denetimler: ilk bölüm 0:00, her bölüm ≥ 10 sn, başlık ≤ 60 karakter (kapı 4), açıklama ≤ 5000, etiketler toplamı ≤ 500 karakter.
"""
import json
import math
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

KAYNAKLAR = """KAYNAKLAR (bu parçada gerçekten dayanılanlar)
• Niccolò Machiavelli, Floransa Tarihi (Istorie fiorentine), III–IV. kitaplar: 1378 olayları, Giovanni di Bicci'nin ölümü (birincil metin; Project Gutenberg İngilizce çevirisi üzerinden kontrol edildi)
{BIRINCIL}• Dizionario Biografico degli Italiani (Treccani): Giovanni di Bicci de' Medici, Anna Maria Luisa de' Medici, Gian Gastone de' Medici maddeleri
• Raymond de Roover, The Rise and Decline of the Medici Bank, 1397–1494 (1963)
• Tim Parks, Medici Money (2005)
• Aile Sözleşmesi (Patto di famiglia, 31 Ekim 1737): Uffizi ve Floransa Belediyesi yayınları
Not: Bazı olgular ikincil kaynak özetlerine dayanır; bunlar anlatımda "… göre / aktarılır" diye, rivayetler ekranda ANEKDOT damgasıyla işaretlidir."""

BIRINCIL_EK = ""          # KAY teyit tablosu (kurul/teyit_P1.md) sonucu doldurulur: gerçekten okunan birincil metinler


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
1743'te son Medici'nin ölümünden 1252'de basılan ilk florine geri sarıyoruz. {kambiyo}'de faiz yasağı ve "vicdan komitesi".

18 Şubat 1743, Floransa. Yetmiş beş yaşında bir kadın ölüyor: Toskana'yı yönetmiş Medici hattının son üyesi Anna Maria Luisa. 31 Ekim 1737'de imzalanan Aile Sözleşmesi'nin 3. maddesine göre ailenin galerileri, tabloları, heykelleri ve kütüphaneleri Floransa'dan ve Büyük Dukalık'tan çıkarılamayacaktı. Peki bir bankacı ailesi, mirasını bir şehre bağlayacak noktaya nasıl geldi?

Medici'nin hikâyesi yedi parçada. Bu ilk parçada o odadan geriye, florin şehrine gidiyoruz: altın florinin doğuşu, veba ve Ciompi isyanı, Giovanni di Bicci'nin bankası, kambiyo, çifte kayıt ve "vicdan komitesi".

Kaynak niteliği ekranda damgalarla (ANEKDOT, MİT, "… göre") ve anlatımda "göre / aktarılır" kipleriyle belirtilir. Sözleşmenin 3. maddesi ve Dante dizesindeki Türkçe karşılıklar bize aittir. Kaynaklar çeliştiğinde videoda bunu açıkça söylüyoruz.

BÖLÜMLER
{bol_txt}

{KAYNAKLAR.replace("{BIRINCIL}", BIRINCIL_EK)}

Sıradaki: 2/7, Cosimo'nun kulesi, sürgün ve dönüş.

Ses: yapay zekâ ile üretilmiş anlatıcı sesi (ElevenLabs, "Emrullah"). Çizim, harita ve animasyonların tamamı kodla üretilmiştir; müzik ve ses efektleri sentezdir. Haritalardaki sınırlar yaklaşıktır.

#Medici #Floransa #Rönesans #TarihBelgeseli
"""
    yorum = f"""Soru: Kilise faizi yasaklamıştı; bankacılar kambiyo ve "faiz değil, hediye" gibi yollar buldu ({kambiyo}). Sizce bu zekâ mıydı, dolambaçlı yol mu?
Rakamlar ve tarihler açıklamadaki kaynaklara dayanır; rivayetler videoda ANEKDOT damgasıyla işaretlidir. Tam kaynak ve teyit tablosunu isteyene paylaşırız.
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
    os.makedirs(PK, exist_ok=True)
    open(os.path.join(PK, "01_baslik.txt"), "w", encoding="utf-8").write(BASLIK + "\n")
    open(os.path.join(PK, "02_aciklama.txt"), "w", encoding="utf-8").write(aciklama)
    open(os.path.join(PK, "03_sabit_yorum.txt"), "w", encoding="utf-8").write(yorum)
    open(os.path.join(PK, "04_etiketler.txt"), "w", encoding="utf-8").write(et_txt + "\n")
    open(os.path.join(PK, "05_bolumler.txt"), "w", encoding="utf-8").write(bol_txt + "\n")
    print(f"başlık ({len(BASLIK)}): {BASLIK}")
    print(bol_txt)
    print(f"açıklama {len(aciklama)} kar., etiketler {len(et_txt)} kar., toplam süre {ts(tl['total'] if 'total' in tl else 0)}")
    if hata:
        raise SystemExit("PAKET HATASI: " + "; ".join(hata))
    print("paket yazıldı:", PK)


if __name__ == "__main__":
    main()
