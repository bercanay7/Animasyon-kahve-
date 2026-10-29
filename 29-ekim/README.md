# 29 Ekim · Cumhuriyet 103 yaşında · Instagram Reels / Story

35 saniyelik, 1080×1920 (9:16), seslendirmeli video. Navitas Spa & Sports Topkapı için. Kodla çizildi, müzik ve efektler sentezlendi.
Görseller yapay zekâyla üretilmedi: Atatürk fotoğrafları gerçek arşiv fotoğraflarıdır, imza Atatürk'ün kendi imzasıdır. İki portre yapay zekâyla yalnızca renklendirildi.

- `cumhuriyet-103.mp4`: Instagram'a yüklenecek video (H.264, 30 fps, AAC stereo ses). Seslendirmeli, renkli portreler ve Gençliğe Hitabe bölümüyle.
- `cumhuriyet-103-siyah-beyaz.mp4`: ilk sürüm, 22 sn. Fotoğraflar siyah-beyaz, Gençliğe Hitabe yerine "ilelebet payidar kalacaktır" sözü var. Kaynak kodu git geçmişinde (ilk commit).
- `kapak.png`: kapak görseli (kapanış karesi). Tek görsel Story olarak da kullanılabilir. Üretmek için: `NODE_PATH=$(npm root -g) node poster.js`
- `animation.html`: animasyonun kaynağı. Tarayıcıda açınca canlı oynar; tıklayınca başa sarar, `?t=15` ile tek kare gösterir.
- `audio.py`: ses tasarımı (sentezlenmiş müzik ve efektler, telifsiz; seslendirmeyi yerleştirir, konuşurken müziği kısar) → `audio.wav`. Çalıştırma: `python3 audio.py` (numpy, scipy ve ffmpeg gerekir)
- `ses/seslendirme.mp3`: anlatıcı kaydı (ElevenLabs, `eleven_v4` modeli, "Hebun Tuna" sesi). `audio.py` içindeki `VO` listesi kaydı dört parçaya bölüp videodaki yerlerine koyar. Kelimelerin zamanları kayıttan çıkarıldı (faster-whisper ile kelime zaman damgaları); yazılar söylendikleri anda belirir.
- `render.js`: kare kare MP4 çıkışı, hareket bulanıklığıyla. Varsa `audio.wav`'ı ekler. Çalıştırma: `NODE_PATH=$(npm root -g) node render.js` (Playwright ve ffmpeg gerekir)
- `assets.py` → `assets.js`: `img/` klasöründeki fotoğrafları ve imzayı sayfaya gömer
- `img/*-renk.jpg`: renklendirilmiş portreler. [DDColor](https://github.com/piddnad/DDColor) modeliyle (Qualcomm AI Hub'ın ONNX sürümü, Apache 2.0) üretildi: model yalnızca renk kanallarını tahmin eder, parlaklık ve ayrıntı orijinal fotoğraftan gelir. 1925 fotoğrafındaki mavi ve yeşil lekeler temizlendi. Meclis fotoğrafı model tarafından inandırıcı biçimde renklendirilemediği için sepya bırakıldı.
- Logo (`../logo.js`) ve yazı tipleri (`../fonts`) üst klasörden gelir. Marcellus ve Hanken Grotesk, navitastopkapi.com'un yazı tipleridir.

## Senaryo
| Süre | Sahne |
|---|---|
| 0–4.8 sn | **28 Ekim 1923 · Çankaya.** Gece, lamba ışığı. Renkli portre karanlıktan çıkar, saat tıkırdar. Anlatıcı: *"Efendiler… yarın Cumhuriyet'i ilan edeceğiz."* |
| 4.8–12 sn | Flaşla kesme, TBMM önü (sepya arşiv). Anlatıcı: *"29 Ekim 1923. Saat 20.30… Cumhuriyet ilan edildi."* Yazılar söylendikçe gelir; ardından top atışları. |
| 12–26.4 sn | Işık sızıntısıyla geçiş, renkli portre (Ankara, 29 Ekim 1925). **Gençliğe Hitabe** anlatıcının sesiyle, kelime kelime, dört parça hâlinde: *"Ey Türk istikbalinin evlâdı! İşte, bu ahval ve şerait içinde dahi vazifen; Türk İstiklâl ve Cumhuriyetini kurtarmaktır! Muhtaç olduğun kudret, damarlarındaki asil kanda mevcuttur!"* Ardından imza altın mürekkeple akar. |
| 26–29.6 sn | Bayrak yukarıdan iner, ekranı kaplar ve dalgalanır. Müzikte doruk noktası. |
| 29.6–35.2 sn | Kamera geri çekilir: altın askıda bayrak, gece göğü, havai fişekler, İstanbul silueti. **29 EKİM**, *"Cumhuriyet Bayramımız kutlu olsun."*, 1923–2026 · 103. yıl, Navitas logosu. Anlatıcı: *"Cumhuriyetimizin yüz üçüncü yılı kutlu olsun!"* |

## Tasarım kararları
- **Gerçek arşiv.** Referans videodaki yapay zekâyla üretilmiş görseller yerine Atatürk'ün gerçek fotoğrafları kullanıldı. Önerilen videodaki gibi portreler renklendirildi; yüz, ifade ve ayrıntı fotoğrafın kendisidir. Her fotoğraf sahneye göre tonlandı (gece için lacivert-sıcak lamba ışığı, 1923 için sepya arşiv). Üzerlerine film greni, toz, kıl ve titreme eklendi.
- **Gençliğe Hitabe.** Önerilen videodaki gibi son cümleler kelime kelime gelir; her kelime belirirken kısa bir altın parıltı alır, "evlâdı", "Cumhuriyetini", "asil kanda" altın italik vurgulanır. Metin Nutuk'taki yazımla (evlâdı, İstiklâl) verildi.
- **Tarihî doğruluk.** "Efendiler, yarın Cumhuriyet'i ilan edeceğiz." sözü 28 Ekim 1923 akşamı Çankaya'da söylendi. Cumhuriyet 29 Ekim 1923'te saat 20.30'da ilan edildi ve 101 pare top atışıyla kutlandı. Meclis fotoğrafının tarihi kesin olmadığı için üzerinde ilan gününe ait olduğunu söyleyen bir not yok. Top atışları, tarihte olduğu gibi ilandan sonra gelir.
- **Bayrak.** Türk Bayrağı Kanunu oranlarıyla çizildi (resmî SVG yolundan). Dikey asılışta gönder tarafı üstte kalır. Kumaş WebGL ile, ışık ve kıvrımlarla dalgalanır. **Bayrağın üzerine yazı konmadı.**
- **Arayüz güvenli alanı.** Bütün yazılar Reels ve Story arayüzünün kapatmadığı bantta durur (üstte kullanıcı adı, sağda simgeler, altta açıklama alanı). Referans videoda yazılar bu alanlara taşıyordu.
- **Marka dili.** navitastopkapi.com'un yazı tipleri (Marcellus başlıklar, Hanken Grotesk etiketler), Instrument Serif italik sözler, beyaz Navitas logosu.
- **Seslendirme.** Önerilen videodaki okuma başkasına ait bir kayıt olduğu için kullanılmadı; yerine ElevenLabs'te tok, olgun bir belgesel anlatıcı sesiyle yeni bir okuma üretildi. Atatürk'ün sesi taklit edilmedi; anlatıcı onun sözlerini okur. Konuşma sırasında müzik yaklaşık 8 dB, efektler 5 dB kısılır.
- **Ses.** Marş ya da hazır müzik kullanılmadı, hepsi sentez: Re minörden Re majöre giden yaylı ve piyano teması (cümle başlarına ve vurgulu kelimelere denk gelen yumuşak notalar), saat tıkırtısı, ilandan sonra top atışları, imza sırasında kalem hışırtısı, bayrak inişi ve dalgalanması, havai fişek ıslık, patlama ve çıtırtıları. Telefon hoparlörü için alçak frekanslar kısıldı, ses −14 LUFS'a normalize edildi.

## Önerilen Instagram açıklaması
> Bir gece, "Efendiler, yarın Cumhuriyet'i ilan edeceğiz." dendi.
> Ertesi akşam saat 20.30'da bir milletin yarını yazıldı.
>
> Cumhuriyetimizin 103. yılında, Gazi Mustafa Kemal Atatürk'ü ve silah arkadaşlarını saygı, minnet ve özlemle anıyoruz.
> 29 Ekim Cumhuriyet Bayramımız kutlu olsun! 🇹🇷
>
> #29Ekim #CumhuriyetBayramı #Cumhuriyet103Yaşında #NavitasTopkapı

## Kaynaklar
Fotoğraflar ve imza Wikimedia Commons'tan alındı; hepsi kamu malıdır:
- [Portret van de Turkse leider Mustafa Kemal Atatürk](https://commons.wikimedia.org/wiki/File:Portret_van_de_Turkse_leider_Mustafa_Kemal_Ataturk_(Atat%C3%BCrk_Kemal_Pascha)_(1881-1938)_in_westers_(3x4_close_cropped).jpg)
- [Atatürk TBMM'den çıkarken](https://commons.wikimedia.org/wiki/File:Atat%C3%BCrk_TBMM%27den_%C3%A7%C4%B1karken.jpg)
- [Reisicumhur Mustafa Kemal Cumhuriyet Bayramı kutlamalarında, Ankara, 29 Ekim 1925](https://commons.wikimedia.org/wiki/File:Reisicumhur_Mustafa_Kemal_Cumhuriyet_Bayram%C4%B1_kutlamalar%C4%B1nda,_Ankara,_29_Ekim_1925.png)
- [Signature of Mustafa Kemal Atatürk](https://commons.wikimedia.org/wiki/File:Signature_of_Mustafa_Kemal_Atat%C3%BCrk.svg)
- [Flag of Turkey](https://commons.wikimedia.org/wiki/File:Flag_of_Turkey.svg) (bayrağın ay-yıldız yolu)
