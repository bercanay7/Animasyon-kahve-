# 29 Ekim Cumhuriyet Bayramı · Navitas

- `29-ekim-story.png`: tek görsel Story (1080×1920). Krem zemin, dalgalanan bayrak, kırmızı "29 EKİM", "Cumhuriyet Bayramımız kutlu olsun!", kemerli pencerelerde fitness, spa-havuz ve yüzme fotoğrafları, "CUMHURİYETİMİZİN 103. YILI".
- `29-ekim-zumba.mp4`: Zumba videosunun 29 Ekim kurgusu (1080×1920, 30 fps, 18.8 sn, H.264 + AAC). Ses, kaynak videonun kendi müziği; son 0.9 saniyede kısılıyor.
- `kaynak/`: ham malzeme (Zumba videosu ve üç fotoğraf).
- `story.html`, `zumba.html`: tasarımların kaynağı. `common.js` bayrak, yazı, fotoğraf ve logo yardımcılarını içerir; logo için `../logo.js`, fontlar için `../fonts/` kullanılır.
- `render.js`: çıktıları üretir (Playwright ve ffmpeg gerekir).
  - `node render.js story`: Story PNG'sini üretir.
  - `node render.js video`: videoyu üretir. İlk çalıştırmada kaynak videodan kareleri `build/` klasörüne çıkarır.
  - `FRAMES=0,45,300 node render.js video`: yalnızca `frames/` klasörüne önizleme kareleri yazar.

## Bayrak
Bayrak `common.js` içinde 2893 sayılı Türk Bayrağı Kanunu'ndaki ölçülerle çizilir: boy 1.5G, dış hilal Ø 0.5G, iç hilal Ø 0.4G, merkezler arası 1/16 G, yıldız çemberi Ø 1/4 G ve iç hilale uzaklığı 1/3 G. Bayrağın üzerine yazı ya da logo konmaz, yazılar her zaman bayrağın dışında durur.

## Video kurgusu
Müzik yaklaşık 113 BPM'dir (bir vuruş 0.53 sn). Yazı değişimleri ve zoom vuruşları bu ızgaraya oturur.

| Süre | Sahne |
|---|---|
| 0–1.5 sn | Kırmızı blok kaynaktaki "ZUMBA fitnes" yazısını kapatır: "CUMHURİYET BAYRAMI'NA ÖZEL / 29 EKİM / Cumhuriyetimiz 103 yaşında!" |
| 1.5–4.2 sn | Blok şeride daralır: "HEP BİRLİKTE / ZUMBA / ile kutluyoruz!". Kaynak yazı 4.1 sn'de biter, şerit sola fırlar. |
| 4.2–13.7 sn | Dans görüntüsü, güçlü vuruşlarda hafif zoom. Etiketler: "Cumhuriyet coşkusu / Zumba enerjisi!", ardından "Sen de / aramıza katıl!" |
| 13.7–14.3 sn | Kırmızı perde geçişi. Kaynaktaki hazır geçiş efekti ve siyah bantlı yatay kadraj çıkarıldı. |
| 14.0–18.8 sn | Kapanış: bayrak, "29 EKİM", "Cumhuriyet Bayramımız kutlu olsun!", grubun yatay çekimi kart içinde, "DETAYLAR İÇİN WHATSAPP · 0533 071 33 73", Navitas logosu |

## Atatürk Story'leri (28 ve 29 Ekim)
- `28-ekim-ataturk-story.png`: bugün (28 Ekim) için. "Efendiler, yarın Cumhuriyeti ilan edeceğiz." alıntısı ve imza olduğu gibi duruyor, altta yalnızca Navitas logosu var.
- `29-ekim-ataturk-story.png`: 29 Ekim için. Eski alıntı silindi, imza korundu. Üstte "29 EKİM CUMHURİYET BAYRAMIMIZ KUTLU OLSUN", altında "Ne mutlu Türküm diyene!" (10. Yıl Nutku, 29 Ekim 1933) ve Navitas logosu var.
- Zemin `kaynak/ataturk-referans.jpg` (paylaşılan ekran görüntüsü). `ataturk.py` görseli kırpar ve büyütür, 29 Ekim için alıntı yazısını OpenCV ile siler. `ataturk.html` yazıyı ve logoyu ekler.
- `node render.js ataturk` iki PNG'yi üretir; gerekirse önce `ataturk.py`'yi çalıştırır.
