# 29 Ekim · Cumhuriyet 103 yaşında · Instagram Reels / Story

22 saniyelik, 1080×1920 (9:16) video. Navitas Spa & Sports Topkapı için. Kodla çizildi, ses sentezlendi.
Yapay zekâ görseli kullanılmadı: Atatürk fotoğrafları gerçek arşiv fotoğraflarıdır, imza Atatürk'ün kendi imzasıdır.

- `cumhuriyet-103.mp4`: Instagram'a yüklenecek video (H.264, 30 fps, AAC stereo ses)
- `kapak.png`: kapak görseli (kapanış karesi). Tek görsel Story olarak da kullanılabilir. Üretmek için: `NODE_PATH=$(npm root -g) node poster.js`
- `animation.html`: animasyonun kaynağı. Tarayıcıda açınca canlı oynar; tıklayınca başa sarar, `?t=15` ile tek kare gösterir.
- `audio.py`: ses tasarımı (sentezlenmiş müzik ve efektler, telifsiz) → `audio.wav`. Çalıştırma: `python3 audio.py` (numpy ve scipy gerekir)
- `render.js`: kare kare MP4 çıkışı, hareket bulanıklığıyla. Varsa `audio.wav`'ı ekler. Çalıştırma: `NODE_PATH=$(npm root -g) node render.js` (Playwright ve ffmpeg gerekir)
- `assets.py` → `assets.js`: `img/` klasöründeki fotoğrafları ve imzayı sayfaya gömer
- Logo (`../logo.js`) ve yazı tipleri (`../fonts`) üst klasörden gelir. Marcellus ve Hanken Grotesk, navitastopkapi.com'un yazı tipleridir.

## Senaryo
| Süre | Sahne |
|---|---|
| 0–4.8 sn | **28 Ekim 1923 · Çankaya.** Gece, lamba ışığı. Portre karanlıktan çıkar, saat tıkırdar: *"Efendiler, yarın Cumhuriyet'i ilan edeceğiz."* |
| 4.8–9.6 sn | Top atışı flaşıyla kesme, TBMM önü. **29 EKİM 1923 · Ankara · Saat 20.30**, *"Cumhuriyet ilan edildi."* Üç top atışı. |
| 9.6–13.6 sn | Işık sızıntısıyla geçiş, Ankara, 29 Ekim 1925. *"Türkiye Cumhuriyeti ilelebet payidar kalacaktır."* İmza altın mürekkeple akar. |
| 13.2–16.8 sn | Bayrak yukarıdan iner, ekranı kaplar ve dalgalanır. Müzikte doruk noktası. |
| 16.8–22.4 sn | Kamera geri çekilir: altın askıda bayrak, gece göğü, havai fişekler, İstanbul silueti. **29 EKİM**, *"Cumhuriyet Bayramımız kutlu olsun."*, 1923–2026 · 103. yıl, Navitas logosu. |

## Tasarım kararları
- **Gerçek arşiv, yapay zekâ yok.** Referans videodaki yapay zekâ görselleri yerine Atatürk'ün gerçek fotoğrafları kullanıldı. Her biri sahneye göre tonlandı (gece için lacivert-sıcak, 1923 için sepya, 1925 için gümüş). Üzerlerine film greni, toz, kıl ve titreme eklendi.
- **Tarihî doğruluk.** "Efendiler, yarın Cumhuriyet'i ilan edeceğiz." sözü 28 Ekim 1923 akşamı Çankaya'da söylendi. Cumhuriyet 29 Ekim 1923'te saat 20.30'da ilan edildi ve 101 pare top atışıyla kutlandı. Fotoğrafın altındaki not yalnızca tarihi kesin bilinen fotoğrafta (29 Ekim 1925) var. Meclis fotoğrafında ilan gününe ait olduğunu ima eden bir not yok.
- **Bayrak.** Türk Bayrağı Kanunu oranlarıyla çizildi (resmî SVG yolundan). Dikey asılışta gönder tarafı üstte kalır. Kumaş WebGL ile, ışık ve kıvrımlarla dalgalanır. **Bayrağın üzerine yazı konmadı.**
- **Arayüz güvenli alanı.** Bütün yazılar Reels ve Story arayüzünün kapatmadığı bantta durur (üstte kullanıcı adı, sağda simgeler, altta açıklama alanı). Referans videoda yazılar bu alanlara taşıyordu.
- **Marka dili.** navitastopkapi.com'un yazı tipleri (Marcellus başlıklar, Hanken Grotesk etiketler), Instrument Serif italik sözler, beyaz Navitas logosu.
- **Ses.** Marş ya da hazır müzik kullanılmadı, hepsi sentez: Re minörden Re majöre giden yaylı ve piyano teması, saat tıkırtısı, gerçek zamanlamayla top atışları, imza sırasında kalem hışırtısı, bayrak inişi ve dalgalanması, havai fişek ıslık, patlama ve çıtırtıları. Telefon hoparlörü için alçak frekanslar kısıldı, ses −14 LUFS'a normalize edildi.

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
