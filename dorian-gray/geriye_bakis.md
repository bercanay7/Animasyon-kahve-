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

## Fable son yorumu
(render ve kapaklardan sonra eklenecek)

## Açık kalanlar
- Kulakla son onay kullanıcıda: "Dorian Grey" ve "Oskar Vayld" okunuşu, B06 dilek tonu, G08–G11 doruk, müzik ve sessizlikler (E09 sonrası 1,8 sn, G09 "çığlık" 3,2 sn).
- Shorts yapılmadı (isteğe bağlı; aday kesitler `youtube.md`).
- Sonuçlar 48. saat (2 Aralık) ve 7. gün (7 Aralık) verisiyle `CLAUDE.md`'ye yazılır: talep kontrolünün dördüncü sınaması (a güçlü: "dorian gray"; b güçlü) ve kanalın ilk 4 kelimelik kapak yazısı denemesi (B).
