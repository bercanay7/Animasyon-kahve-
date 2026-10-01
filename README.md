# Dünya Kahve Günü · Instagram Animasyonu

20 saniyelik, 1080×1920 (9:16) Reels / Story videosu — tamamen kodla çizildi.

- `dunya-kahve-gunu.mp4` — Instagram'a yüklenecek video (H.264, 30 fps, AAC stereo ses)
- `kapak.png` — Reels kapak görseli
- `navitas-logo.svg` / `logo.js` — Navitas yatay logosu, orijinal renkler (logo.js canvas için gömülü sürüm)
- `animation.html` — animasyonun kaynağı; tarayıcıda açınca canlı oynar (tıklayınca başa sarar, `?t=12` ile tek kare)
- `audio.py` — ses tasarımı (sentezlenmiş müzik + efektler, telifsiz) → `audio.wav`: `python3 audio.py` (numpy + scipy)
- `render.js` — kare kare MP4 çıkışı, hareket bulanıklığıyla (`MB_SAMPLES=16`, varsayılan 8; 1 = kapalı), varsa `audio.wav`'ı ekler: `NODE_PATH=$(npm root -g) node render.js` (Playwright + ffmpeg gerekir)

## Tasarım
Modern, minimalist kinetik tipografi: kırık beyaz kâğıt (#EEE8DF), espresso siyahı (#1C1714) ve tek vurgu rengi yanık karamel (#B06C38).
Yazı tipleri: Instrument Serif (başlıklar) + Inter (künye ve gövde metni).

## Teknik notlar
- Hareket bulanıklığı: her kare, 180° obtüratör (yarım kare pozlama) içindeki alt karelerin ortalaması.
- Müzik 120 BPM; vuruş ızgarası 0.95 sn'deki damlaya hizalı. Koyu sahne (2.95), sayaç (8.45), fincanın tabağa oturması (11.45), fal metni (13.45) ve final (14.95) vuruşa denk gelir.
- Çizim: fincan ağzı ve kahve yüzeyi tabakla aynı perspektifte elips; değişken kalınlıklı, uçlarda incelen çizgiler (gövde > tabak > kulp/kaide); pudra şekerli lokum; düzensiz buhar.
- Fincan hareketleri: yudumda eğilme (kahve yüzeyi yatay kalır), kapatmadan önce hazırlık, oturuşta sönümlü sekme, yavaş başlayan kalkış.

## Senaryo
| Süre | Sahne |
|---|---|
| 0–3 sn | İlk karede "Bugün kahveler *bizden.*"; bir kahve damlası düşer, halkalar yayılır, damla büyüyüp ekranı kaplar |
| 3–6.3 sn | Koyu zemin: "Bugün · Dünya *Kahve* Günü." + "Bir fincan kahvenin kırk yıl hatırı vardır." |
| 6.3–7 sn | Açık panel aşağıdan yukarı siler |
| 7–10 sn | Tek çizgi Türk kahvesi fincanı (tabak + lokum) kendini çizer, köpüklü kahveyle dolar, buhar yükselir; "Saat 15.00" sayaç gibi döner |
| 10–15.4 sn | Kahve falı: kahve içilir, fincan tabağa kapatılır ("Fincanı kapattık…"), kalkar; tabak kuşbakışına döner, telveden kalp belirir — "Falınızda bugün 15.00'te *bir kahve var.*" Tabak küçülüp rozetin içine yerleşir |
| 15–20 sn | "Kahveler *bizden.*" — "Bugün saat 15.00'te tüm misafirlerimize ikramımızdır." + dönen "Afiyet olsun" rozeti + Navitas logosu |
