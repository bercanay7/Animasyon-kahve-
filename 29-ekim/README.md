# 29 Ekim · Cumhuriyet 103 yaşında · Instagram Reels / Story

48 saniyelik, 1080×1920 (9:16) video. Navitas Spa & Sports Topkapı için. Atatürk'ün kendi sesi ve 1933 film görüntüsü, İzmir Marşı ve Onuncu Yıl Marşı, Türkçe anlatıcı, renklendirilmiş arşiv fotoğrafları.

- `cumhuriyet-103.mp4`: Instagram'a yüklenecek video (H.264, 30 fps, AAC stereo ses)
- `cumhuriyet-103-siyah-beyaz.mp4`: ilk sürüm, 22 sn, siyah-beyaz, sentez müzikli, seslendirmesiz
- `kapak.png`: kapak görseli (kapanış karesi). Tek görsel Story olarak da kullanılabilir. Üretmek için: `NODE_PATH=$(npm root -g) node poster.js`
- `animation.html`: animasyonun kaynağı. Tarayıcıda açınca canlı oynar; tıklayınca başa sarar, `?t=15` ile tek kare gösterir. Film bölümünde tuval saydamdır; film yalnızca render çıktısında görünür.
- `kaynaklar.sh`: dışarıdan alınan kaynakları archive.org'dan indirip kullanılan parçaları keser → `kaynak/` (git'e eklenmez). Render'dan önce bir kez çalıştırın.
- `audio.py`: ses miksi → `audio.wav`. Açılıştaki müzik ve efektler sentezlenir; anlatıcıyı, Atatürk'ün sesini ve marşları yerleştirir, konuşurken müziği kısar. Çalıştırma: `python3 audio.py` (numpy, scipy ve ffmpeg gerekir)
- `render.js`: kare kare MP4 çıkışı, hareket bulanıklığıyla. Film bölümünü tuvalin altına ffmpeg ile ekler, `audio.wav`'ı bağlar. Çalıştırma: `NODE_PATH=$(npm root -g) node render.js` (Playwright ve ffmpeg gerekir)
- `ses/seslendirme.mp3`: anlatıcı kaydı (ElevenLabs, `eleven_v4`, "Hebun Tuna" sesi)
- `assets.py` → `assets.js`: `img/` klasöründeki fotoğrafları ve imzayı sayfaya gömer
- `img/*-renk.jpg`: renklendirilmiş portreler ([DDColor](https://github.com/piddnad/DDColor), Qualcomm AI Hub'ın ONNX sürümü). Model yalnızca renk kanallarını tahmin eder; parlaklık ve ayrıntı orijinal fotoğraftan gelir. Meclis fotoğrafı inandırıcı biçimde renklenmediği için sepya bırakıldı.
- Logo (`../logo.js`) ve yazı tipleri (`../fonts`) üst klasörden gelir. Marcellus ve Hanken Grotesk, navitastopkapi.com'un yazı tipleridir.

## Senaryo
| Süre | Görüntü | Ses |
|---|---|---|
| 0–4.8 sn | **28 Ekim 1923 · Çankaya.** Gece, lamba ışığı, renkli portre | Anlatıcı: *"Efendiler… yarın Cumhuriyet'i ilan edeceğiz."* Saat tıkırtısı, yaylılar |
| 4.8–12 sn | TBMM önü (sepya arşiv). **29 EKİM 1923 · Ankara · Saat 20.30** | Anlatıcı: *"29 Ekim 1923. Saat 20.30… Cumhuriyet ilan edildi."* 10.6'da top atışları ve **İzmir Marşı** |
| 12–26.1 sn | Renkli portre (Ankara, 29 Ekim 1925), **Gençliğe Hitabe** kelime kelime, ardından imza | Anlatıcı Gençliğe Hitabe'yi okur, altta İzmir Marşı kısık |
| 26.1–37.7 sn | **Onuncu Yıl Nutku filmi** (29 Ekim 1933): yakın plan, sonra kürsünün genel planı. Altyazı söylendiği anda gelir | **Atatürk'ün kendi sesi:** *"Bugün, Cumhuriyetimizin onuncu yılını doldurduğu en büyük bayramdır. Kutlu olsun!"* |
| 37.3–40.9 sn | "Kutlu olsun!"un ardından bayrak yukarıdan iner ve dalgalanır | **Onuncu Yıl Marşı:** *"Çıktık açık alınla, on yılda her savaştan…"* |
| 40.9–48.1 sn | Altın askıda bayrak, gece göğü, havai fişekler, İstanbul silueti. **29 EKİM**, *"Cumhuriyet Bayramımız kutlu olsun."*, 1923–2026 · 103. yıl, Navitas logosu | Marş "her savaştan"da biter, yavaşça kısılır |

## Tasarım kararları
- **Gerçek arşiv.** Atatürk'ün gerçek fotoğrafları ve gerçek film görüntüsü kullanıldı; yapay zekâyla görüntü üretilmedi. Portreler yalnızca renklendirildi. Fotoğraflar sahneye göre tonlandı, üzerlerine film greni, toz, kıl ve titreme eklendi.
- **Ses ve yazı senkronu.** Anlatıcının ve Atatürk'ün her kelimesinin zamanı kayıtlardan çıkarıldı (ses enerjisi ve faster-whisper ile kelime zaman damgaları). Yazılar kelime söylendiği anda belirir.
- **Film.** Onuncu Yıl Nutku filminin ilk 11.6 saniyesi. Yakın plan dikey kırpıldı, genel plan bulanık zemin üzerinde 16:9 pencere içinde. Kaynaktaki kanal logoları kadraj dışında bırakıldı.
- **Seslendirme.** Anlatıcı Atatürk'ün sesini taklit etmez; onun sözlerini okur. Atatürk'ün sesi yalnızca kendi kaydından gelir.
- **Tarihî doğruluk.** "Efendiler, yarın Cumhuriyet'i ilan edeceğiz." sözü 28 Ekim 1923 akşamı Çankaya'da söylendi. Cumhuriyet 29 Ekim 1923'te saat 20.30'da ilan edildi ve top atışlarıyla kutlandı. Onuncu Yıl Nutku 29 Ekim 1933'te Ankara'da okundu. Meclis fotoğrafının tarihi kesin olmadığı için üzerinde tarih notu yok.
- **Bayrak.** Türk Bayrağı Kanunu oranlarıyla çizildi (resmî SVG yolundan). Dikey asılışta gönder tarafı üstte kalır. Kumaş WebGL ile, ışık ve kıvrımlarla dalgalanır. **Bayrağın üzerine yazı konmadı.**
- **Arayüz güvenli alanı.** Bütün yazılar Reels ve Story arayüzünün kapatmadığı bantta durur.
- **Marka dili.** navitastopkapi.com'un yazı tipleri, Instrument Serif italik sözler, beyaz Navitas logosu.

## Telif notu
Marşlar ve film başkalarına ait kayıtlardır ve işletmenin isteğiyle kullanıldı. Onuncu Yıl Marşı'nın bestesi (Cemal Reşit Rey) ve sözleri hâlâ telif kapsamında. Kayıtlar TSK Armoni Mızıkası'na, film kopyası yayıncısına aittir. İzmir Marşı'nın ezgisi anonimdir. Instagram, telif tespit ederse videonun sesini kısabilir ya da paylaşımı sınırlayabilir. Böyle olursa videoyu müziksiz yükleyip marşı Instagram'ın kendi müzik kütüphanesinden ekleyebilirsiniz. Ancak işletme hesaplarında bu kütüphane kısıtlı olabilir. Bu kayıtlar telif nedeniyle git'e konmadı; `kaynaklar.sh` onları indirir.

## Önerilen Instagram açıklaması
> Bir gece, "Efendiler, yarın Cumhuriyet'i ilan edeceğiz." dendi.
> Ertesi akşam saat 20.30'da bir milletin yarını yazıldı.
>
> Cumhuriyetimizin 103. yılında, Gazi Mustafa Kemal Atatürk'ü ve silah arkadaşlarını saygı, minnet ve özlemle anıyoruz.
> 29 Ekim Cumhuriyet Bayramımız kutlu olsun! 🇹🇷
>
> #29Ekim #CumhuriyetBayramı #Cumhuriyet103Yaşında #NavitasTopkapı

## Kaynaklar
Fotoğraflar ve imza (Wikimedia Commons, kamu malı):
- [Portret van de Turkse leider Mustafa Kemal Atatürk](https://commons.wikimedia.org/wiki/File:Portret_van_de_Turkse_leider_Mustafa_Kemal_Ataturk_(Atat%C3%BCrk_Kemal_Pascha)_(1881-1938)_in_westers_(3x4_close_cropped).jpg)
- [Atatürk TBMM'den çıkarken](https://commons.wikimedia.org/wiki/File:Atat%C3%BCrk_TBMM%27den_%C3%A7%C4%B1karken.jpg)
- [Reisicumhur Mustafa Kemal Cumhuriyet Bayramı kutlamalarında, Ankara, 29 Ekim 1925](https://commons.wikimedia.org/wiki/File:Reisicumhur_Mustafa_Kemal_Cumhuriyet_Bayram%C4%B1_kutlamalar%C4%B1nda,_Ankara,_29_Ekim_1925.png)
- [Signature of Mustafa Kemal Atatürk](https://commons.wikimedia.org/wiki/File:Signature_of_Mustafa_Kemal_Atat%C3%BCrk.svg)
- [Flag of Turkey](https://commons.wikimedia.org/wiki/File:Flag_of_Turkey.svg) (bayrağın ay-yıldız yolu)

Film ve marşlar (archive.org, `kaynaklar.sh`):
- [Atatürk Onuncu Yıl Nutku](https://archive.org/details/ata_20250210) (film ve ses)
- [Türk Ordu Marşı: "İzmir Marşı"](https://archive.org/details/youtube-rNPUp1hkpJQ)
- ["Onuncu Yıl Marşı" - TSK Armoni Mızıkası](https://archive.org/details/youtube-NNUMtvlFskw)
