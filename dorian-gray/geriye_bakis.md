# Dorian Gray'in Portresi: geriye bakış (19 Kasım 2026; kurulsuz üretim, başkan)

Çalışma düzeni kullanıcının kararıydı: kurul, puanlama ve çok ajanlı akış yok. Bütün kapılar başkan denetimiyle geçti. Fable üretim sırasında hiç danışılmadı (takılınan yer olmadı); yayından önce bir kez bütün işi yorumladı (aşağıda "Fable son yorumu").

## Ne işe yaradı
- **Talep kontrolü güçlü çıktı:** "dorian gray" Türkçe aramada 204 B medyan (Sisifos'un ~3, Kafka'nın ~5 katı) ve öneriler kitap okuru aramaları (kitap yorumu, inceleme, özet). Kapı başlıkta öne alındı, soru ("Kimse Görmeseydi Ne Yapardın?") filmin ilk ve son cümlesi.
- **Kullanıcının hatırladığı yorum kaynakla sınandı:** "Wilde kendini üç karakterde gösterdi" sözü romanda değil, Wilde'ın Ralph Payne'e mektubunda (Hart-Davis 1962, s. 352); önsözden duyulmuş olabilir. Videoda mektup kullanıldı, tarih doğrulanamadığı için anlatımda tarih yok.
- **İki metin bir kaynaktı:** 1890 dergi metninde dilek "her şeyi verirdim", 1891 kitapta "ruhumu verirdim". Fark sahnenin içinde tek cümle (B07) ve dergi sayfasının kendisiyle gösterildi; analiz kuyruğu yok.
- **Karma üslup (dünya gravür, yalnız portre yağlıboya):** "kimse görmese" fikri görüntünün kuralı oldu. Dorian'ın yüzü yalnız portrede, renk yalnız tabloda. Kapakta renkli yüz siyah-beyaz karede tek odak.
- **Gerçek görseller yer yer** (kullanıcının "belgeselvari" önerisi): Sarony fotoğrafları (Met CC0), Lippincott sayfaları, Doré'nin 1872 Londra'sı. Doré levhaları zaten gravür olduğu için film diline dikişsiz girdi.

## Ne zorladı, ne öğrendik
- **Piyano sentezinde gizli hata (Mary Stuart'tan devralındı):** çok alçak notalarda (MIDI < ~37; D1, E1, B♭0) sönüm katsayısı negatife düşüyor, nota milyonlarca kat büyüyor; normalleştirme bütün müziği bu patlamaya göre kısıyor ve geri kalanı duyulmuyor. Dorian'da ilk üretimde fark edildi (müzik eğrisi baştan sona -180 dB). Aynı kodla Mary Stuart'ın müziği yeniden üretilince filmin 1.249 saniyesinin yalnız 14'ünde müzik duyuluyordu: **Mary Stuart müziksiz teslim edilmiş olmalı.** Düzeltme: `dec = max(.3, …)`. Ders: **her müzik üretiminden sonra saniye saniye düzey eğrisi basılır** (medyan ve "-60 dB üstü saniye" sayısı); miks LUFS'u bunu göstermez, çünkü ebur128 sessiz bölümleri kapıdan atar ve kalan birkaç saniyeye göre ölçer.
- **Kurgu özeti küçük karede kırpmayı saklar:** dergi sayfası planı (P017) dilek satırını hiç göstermiyordu ("How sad it is" paragrafının üst yarısı); 480 px'lik özette fark edilmedi, tam boy karede görüldü. Hassasiyet ve içerik kontrolü tam boy karede yapılır (Mary Stuart dersiyle aynı).
- **Plan kimliği kayması ve geri dönüş değeri:** planlar bölününce `sahneler.js`'teki kimlikler kaydı; `arka:` işlevi çerçeve matrisini döndürmeyince portre görünmedi. Ders: plan listesi senaryo kesinleşince yazılır; portreli planlarda `arka` her zaman matris döndürür (denetim: `ozet.js` sayfasında renkli tuval var mı).
- **Kodla figür:** silindir şapkalı Viktorya figürü koyu siluetle okunuyor; el ve yakın plan nesneler (yerdeki el, kitap) zayıf kaldı. Çözüm hep aynı: daha koyu zemin, tek ışık havuzu, daha büyük ölçek.
- **Kapakta duman çizgisi:** B kapağının ilk taslağında Henry'nin dumanı portrenin yüzünü kesiyordu; "yüzü kesen çizgi" bıçak gibi okunur. Duman ağızdaki sigaradan başlatıldı ve portreye değmeden Dorian'ın kulağında bitti.
- **Render maliyeti:** portreli kareler 2–10 sn (yakın planlar pahalı). Impasto'nun süper örneklemesi 2 → 1,5 görünümü değiştirmeden süreyi üçte bir kısalttı (`?ss=1.5`).
- **Render betiğinde yol hatası:** `PARTS` mutlak yol verilince `path.join` onu proje klasörüne ekliyordu; deneme parçaları depoya girdi, çıkarıldı. `path.resolve` ile düzeltildi.

## Fable son yorumu (19 Kasım, son render ve kapaklardan sonra; tek tur)
Fable bütün kurgu özeti sayfalarına, ~30 tam boy kareye, senaryoya, SRT'ye, iki kapağa, `youtube.md` ve `yayin.md`'ye baktı; alıntıları Mason ve 1891 metniyle karşılaştırdı. Politika ya da doğruluk açısından engelleyici bulgu yok dedi; iki engelleyici, altı önemli bulgu verdi. Başkan her birini karede ya da metinde doğruladı.

**Uygulananlar**
- **(Engelleyici) Portredeki yaka papaz yakası gibi okunuyordu:** simsiyah giysinin ortasında küçük beyaz dikdörtgen ve koyu şerit. "Günah, ruh, vicdan" anlatımıyla birlikte "günahkâr rahip" okuması doğar; filmin tek renkli ve en çok bakılan görseli. Beyaz gömlek önü, kanatlı dik yaka, geniş gri ipek fular, altın iğne ve açık ceket yakalarıyla Viktorya beyefendisine çevrildi (`lib/portre_ciz.js`); bütün portreli parçalar ve kapak B yeniden üretildi. **Ders:** hassasiyet taraması kıyafet ayrıntısına da bakar; tek renkli küçük bir dikdörtgen bir mesleği (ve dini) çağırır.
- **(Engelleyici) `yayin.md` bitiş ekranını ters tarif ediyordu** ("sol yarı boş"); doğrusu sağ yarı. Düzeltildi. **Ders:** bitiş ekranı tarifi son render'ın karesine bakılarak yazılır, plan listesinden değil.
- **G11 yüzüklerinden tanınan el (6:36):** el zeminle aynı tonda tarandığı için "konuşma balonu" gibi okunuyordu, parmaklar ve yüzükler hiç görünmüyordu. Neden: iç içe `GR.frame` göreli değil mutlak çalışıyor; parmaklar kadrajın dışına çiziliyordu. Parmaklar el çerçevesinde elle döndürüldü, el soluk, zemin koyu, arkadaki ışık çizgileri kaldırıldı.
- **C05 Sibyl (2:04):** dümdüz ~30° kalkık kol selam gibi okunuyordu (Mary Stuart'taki dans dersiyle aynı). Kol dirsekten kırık, öne uzanır; Dorian arkadan ışıkla seçilir oldu.
- **E09 cinayet (4:33):** kol ötekinin başının üstüne kalkıyordu. İlk düzeltme (kol öne) daha kötü oldu: el yüze dokunuyor gibi duruyordu. Son hâl: temas ve kalkık kol yok, Dorian adım atar, ışık söner.
- **F04 kitaba basılan el (5:08):** açık kitaba basan el yemin gibi okunabilir; el artık kitabı alt kenarından itiyor.
- **Kapak A:** "GÖRMEDİ"nin İ'si çerçevenin çizgili kenarına biniyordu (küçükte "GÖRMED"); harf aralığı daraltılıp yazı sola alındı (harf yüksekliği %18,8'de kaldı). Ele parmak aralıkları eklendi.
- **Kapak B:** yazı şövaleye ve pencereye biniyordu; yazının altına koyu bant kondu.
- **Başlık 54 → 42 karakter:** "Dorian Gray: Kimse Görmeseydi Ne Yapardın?". Mobil akışta eski başlık "…Ne Yap" diye kesiliyor, soru düşüyordu.
- **G12 avukatın sorusu** ("Bu ahlaksız bir kitap değil mi?") kaynakta birebir yok, Carson'ın sorularının özeti; açıklamaya "özetidir, birebir alıntı değildir" notu eklendi.

**Reddedilenler (gerekçesiyle)**
- **B02 çevirisi** ("İçine kendimden fazlasını koydum"; aslı "I have put too much of myself into it"): Türkçede "kendimden fazlasını koydum" gündelik dilde "gereğinden fazla kendimi koydum" anlamında da okunur; anlam kayması küçük. Ekran yazısını değiştirmek sesle yazıyı ayırır, sesi düzeltmek kredi ister. Sonraki videoda kural: tırnak içi alıntının çevirisi seslendirmeden önce aslıyla satır satır karşılaştırılır.
- **Kapak B'de portreyi büyütmek:** denendi; büyüyen kadrajda yazı portrenin başına biniyor ve Dorian portrenin yarısını örtüyor. Bant yeterli görüldü.
- **0:08–0:16 Wilde fotoğrafı ve başlık sayfası (kanca sonrası köprü):** Fable da kabul edilebilir dedi (tek cümle, A03 somut vaat veriyor). Kanalın üç kez ölçtüğü sızıntı yeri olduğu için 48. saat eğrisinde bu aralığa ayrıca bakılacak.

**Açık kalan (Fable'ın en emin olmadığı):** okunuşlar ("Vayld", "Holvırd") ve fısıltı etiketli cümleler kulakla onaylanmalı; ses dinlenemedi.

## Açık kalanlar
- Kulakla son onay kullanıcıda: "Dorian Grey" ve "Oskar Vayld" okunuşu, B06 dilek tonu, G08–G11 doruk, müzik ve sessizlikler (E09 sonrası 1,8 sn, G09 "çığlık" 3,2 sn).
- Shorts yapılmadı (isteğe bağlı; aday kesitler `youtube.md`).
- Sonuçlar 48. saat (6 Aralık) ve 7. gün (11 Aralık; yayın 4 Aralık'a kaydırıldı) verisiyle `CLAUDE.md`'ye yazılır: talep kontrolünün dördüncü sınaması (a güçlü: "dorian gray"; b güçlü) ve kanalın ilk 4 kelimelik kapak yazısı denemesi (B).
