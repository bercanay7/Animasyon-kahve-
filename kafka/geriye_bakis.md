# Geriye bakış: Kafka, Dönüşüm

## Ne çıktı
- **Film:** 6:39 (render 62 dk + düzeltme parçaları 10 dk, 4 işçi); 48 cümle, 56 plan; ağaç baskı üslubu (cinecode `woodcut`, LemoLab MIT motoru); Emrullah sesi; özgün oda müziği (çello, keman, saat); 106 altyazı.
- **Kapaklar:** A "ARTIK O DEĞİL" (filmin ilk karesi: aralık kapı, ışık şeridi, kırmızı elma); B "SEVGİ KOŞULLU MU?" (4,5. sn: kapıda aile).
- **Shorts:** 32,6 sn; kanca "ARTIK O DEĞİL", ilk cümle izleyiciye kişisel soru; kapanış "Sen kendini hangi koşulla seviyorsun?".
- **Yayın metinleri:** `youtube.md`, `yayin.md`.
- **Kredi:** 10.832 (7 bölüm × 2 çekim); tahmin 10.750–10.900.
- **Kurul:** hiçbir kapıda toplanmadı (kullanıcının kararı, kullanım %89); ayrıntı `KURUL.md`.

## Talep kontrolü (bu videoda ilk kez; senaryodan önce)
| Ölçüt | Sonuç |
|---|---|
| (a) Tanınırlık | "dönüşüm kafka" otomatik tamamlamada özet, analiz, felsefesi, **animasyon**; Türkçe en çok izlenen video 1 M (Portal). Kontrol: "milton" ve "ikaros" aramaları konuya hiç ulaşmıyor (kasırga, futbolcu, işaret fişeği) |
| (b) Kişisel soru | "İşe yaramasan da seni severler miydi?" / "Sen kendini hangi koşulla seviyorsun?" |
| Boşluk | Türkçe Dönüşüm animasyonu neredeyse yok (tek video, 1,6 B) |
| Rakip açılar | "hepimiz böceğiz" (yabancılaşma), "yararlı olmayınca sevilmezsin" (8,5 B). Ayrım: gizli birikime sevinen Gregor (koşulu önce kendine koyar), kardeşinin adını ağzına almayan Grete, asıl dönüşen aile |
| Sonuç | Güçlü; konu korundu. Sonucu yayından sonra 48. saat ve 7. gün verisiyle sına: TO Milton ve İkaros'tan (%1–1,6) yüksek mi, göz atma testi geldi mi? |

## İşe yarayanlar
- **Talep kontrolünü senaryodan önce yapmak.** Otomatik tamamlama on dakikalık, bedava bir ölçüm; Milton ve İkaros'un neden geniş kitleye açılmadığını kontrol satırları açıkça gösterdi.
- **Kullanıcının önerisini tartmak.** Kullanıcı "beni derin düşüncelere atmadı" dedi; derinlik özetten değil metnin az bilinen ayrıntılarından kuruldu (gizli birikim satır 855–866, "hevesle başını salladı" 861, "kardeşimin adını ağzıma almayacağım" 1635–1636). Kullanıcı "koşullu sevgi" omurgasını seçti.
- **Kaynağın kendi kuralı üslup kararı oldu.** Kafka'nın "böcek çizilmesin" mektubu hem kanca (merak döngüsü) hem kodla çizimin zayıf yanının (beden) çözümü oldu. Kamera çoğunlukla yerden: izleyici Gregor'un yerinde.
- **Tek renk.** Kırmızı elma (metinde "küçük kırmızı elmalar", satır 1233–1234) filmin, kapağın ve Shorts'un ortak odağı.
- **Hazır motor.** cinecode woodcut demo motoru tek klasik betiğe paketlendi (`tools/bundle_woodcut.py` → `lib/woodcut.bundle.js`); üslup ilk karede oturdu, motor yazılmadı.

## İşe yaramayanlar ve dersler
1. **İzin denetleyicisi kredi harcayan çağrıları durdurabilir.** Yedi seslendirme çağrısından üçü otomatik izin denetleyicisince reddedildi (ücret alınmadı); kullanıcının açık izniyle yeniden gönderildi. Ders: kredi onayını kullanıcıdan çağrıdan hemen önce açık cümleyle al ("şu üç çağrıyı gönderiyorum").
2. **Senaryodan cümle çıkarınca numaralar kayar.** F05 çıkınca plan listesinde F06/F07 bir kaydı; P55'teki oyulmuş soru anlatımla uyuşmadı, render başladıktan sonra yakalandı. Ders: plan listesini yalnız senaryo kesinleştikten sonra yaz; ya da kimlikleri yeniden numaralama, çıkarılan cümlenin numarası boş kalsın.
3. **Bitiş ekranı cümleyle eşlenmeli.** "Sisifos'un hikâyesi ekranda" cümlesi bitiş ekranından 9 sn önce geçiyordu; kuyruk kısaltıldı. Ders: `vo/plan.json` "sonra" değeri, "ekranda" denen kelimeden ≤ 20 sn sonra bitecek şekilde hesaplanır.
4. **Dev yakın plan figürler kırık şekil gibi okunur.** Baş kadraj dışına taşınca geriye "borular" kaldı. Ders: yakın planda baş kadraj içinde olmalı (y ≈ 380), boy ≤ 1300 px.
5. **Whisper yine yoktu.** Sessizliğe dayalı hizalama iki cümle sınırını yanlış koydu (kısa cümleler: "Kızmadı.", kiracılar cümlesi); ölçümle elle düzeltildi. Telaffuz denetlenmedi.
6. **Ağaç baskı dokusu dosyayı şişirir.** Her karede değişen mürekkep ve kâğıt gürültüsü yüzünden 6:39'luk film H.264 CRF 20'de 310 MB, H.265 CRF 26'da bile 259 MB oldu (İkaros 5:55'te ~42 MB). Telefon kopyası H.265 CRF 32 ile 98 MB. Ders: bu üslupta baskı gürültüsü (`inkSeed`) her karede değil iki karede bir değişsin (tarifin "on twos" kuralı) ya da teslimde `-tune grain` + daha yüksek CRF denenip 1:1 kırpmayla karşılaştırılsın. Yedek olarak 55 sn'lik parçalar (`-f segment -c copy`) gönderildi.
7. **Bellek sınırı:** 4 render işçisi + ffmpeg SSIM ölçümü aynı anda çalışınca çekirdek bir süreci öldürdü. Ölçümü kısa kesitte ve işler bittikten sonra yap.
8. **Kurulsuz üretim.** Bütün kapılar başkan denetimiyle geçti. Bilinen zayıflıklar aşağıda; bağımsız göz olmadan bunların ne kadarının izleyiciyi rahatsız edeceğini bilmiyoruz.

## Bilinen zayıflıklar
- Oturan figürlerin kolları masaya uzanırken düz çubuk gibi; ellerin biçimi kaba.
- Bazı planlar yalnız yavaş yaklaşmayla hareket ediyor (P33, P34, P43, P44); donuk değil ama az olaylı.
- Kiracıların gür sakalı metne uygun, ama hassasiyet okuru görmedi.
- Telaffuz kulakla kontrol edilmedi (ör. "Verwandlung" anlatımda yok; "Grete", "Samsa", "Camus" adları dinlenmeli).
- Shorts kurulsuz; ilk 3 saniyede metin yoğun (kanca + altyazı).
