# Dünya Kahve Günü · Instagram Story Animasyonu

9 saniyelik, 1080×1920 (9:16) Story videosu — tamamen kodla çizildi ve sentezlendi. Navitas spa & sports için.

- `dunya-kahve-gunu.mp4` — Instagram'a yüklenecek video (H.264, 30 fps, AAC stereo ses)
- `kapak.png` — kapak görseli ("KAHVELER bizden!")
- `dunya-kahve-gunu-story.png` — tek görsel Story (1080×1920), videoyla aynı tasarım dili: `NODE_PATH=$(npm root -g) node poster.js`
- `animation.html` — animasyonun kaynağı; tarayıcıda açınca canlı oynar (tıklayınca başa sarar, `?t=3` ile tek kare)
- `audio.py` — ses tasarımı (sentezlenmiş müzik + efektler, telifsiz) → `audio.wav`: `python3 audio.py` (numpy + scipy)
- `render.js` — kare kare MP4 çıkışı, hareket bulanıklığıyla (`MB_SAMPLES=16`, varsayılan 8; 1 = kapalı), varsa `audio.wav`'ı ekler: `NODE_PATH=$(npm root -g) node render.js` (Playwright + ffmpeg gerekir)
- `navitas-logo.svg` / `logo.js` — Navitas yatay logosu, orijinal renkler; logo.js ayrıca turuncu zeminler için beyaz sürümü içerir

## Tasarım
Story için hızlı, dikkat çekici kinetik tipografi: marka turuncusu (#E17610), lacivert (#202F50), espresso, karamel ve krem arasında sert sahne geçişleri.
Kalın, düz, geometrik çizimler (kuşbakışı Türk kahvesi fincanı, kahve çekirdekleri). Inter Black başlıklar + Instrument Serif italik vurgu.

## Teknik notlar
- 120 BPM; her vuruşta (0.5 sn) ekranda bir şey değişir. Sahne geçişleri, kamera sarsıntıları ve ses vuruşları aynı ızgarada.
- Hareket bulanıklığı: her kare, 180° obtüratör (yarım kare pozlama) içindeki alt karelerin ortalaması.
- İlk kare boş değildir: "BUGÜN" yazısı ilk karede çarparak girmektedir, kahve çekirdekleri uçuşur.

## Senaryo
| Süre | Sahne |
|---|---|
| 0–1 sn | Turuncu: "BUGÜN" çarparak girer, çekirdekler uçuşur, "DÜNYA KAHVE GÜNÜ" etiketi |
| 1–2.5 sn | Espresso daire ekranı kaplar; kuşbakışı Türk kahvesi fincanı, dönen köpük, "KAHVELER"; çekirdek patlaması |
| 2.5–4 sn | Kamera köpüğe dalar: "KAHVELER *bizden!*" |
| 4–6 sn | Eğik kayan şeritler: "BÜTÜN GÜN", fincanlar, "SABAHTAN AKŞAMA" |
| 6–9 sn | Krem kapanış: Navitas logosu, "Bütün gün kahveler *bizden.*", "Tüm misafirlerimize ikramımızdır.", "1 EKİM · DÜNYA KAHVE GÜNÜ" |
