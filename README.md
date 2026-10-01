# Dünya Kahve Günü · Instagram Animasyonu

15 saniyelik, 1080×1920 (9:16) Reels / Story videosu — tamamen kodla çizildi.

- `dunya-kahve-gunu.mp4` — Instagram'a yüklenecek video (H.264, 30 fps, sessiz ses kanalı)
- `kapak.png` — Reels kapak görseli
- `animation.html` — animasyonun kaynağı; tarayıcıda açınca canlı oynar (tıklayınca başa sarar, `?t=12` ile tek kare)
- `render.js` — kare kare MP4 çıkışı: `NODE_PATH=$(npm root -g) node render.js` (Playwright + ffmpeg gerekir)

## Tasarım
Modern, minimalist kinetik tipografi: kırık beyaz kâğıt (#EEE8DF), espresso siyahı (#1C1714) ve tek vurgu rengi yanık karamel (#B06C38).
Yazı tipleri: Instrument Serif (başlıklar) + Inter (künye ve gövde metni).

## Senaryo
| Süre | Sahne |
|---|---|
| 0–3 sn | İlk karede "Bugün kahveler *bizden.*"; bir kahve damlası düşer, halkalar yayılır, damla büyüyüp ekranı kaplar |
| 3–6.3 sn | Koyu zemin: "Bugün · Dünya *Kahve* Günü." + "Bir fincan kahvenin kırk yıl hatırı vardır." |
| 6.3–7 sn | Açık panel aşağıdan yukarı siler |
| 7–10.3 sn | Tek çizgi fincan kendini çizer, kahveyle dolar, buhar yükselir; "Saat 15.00" sayaç gibi döner |
| 10.3–15 sn | "Kahveler *bizden.*" — "Bugün saat 15.00'te tüm misafirlerimize ikramımızdır." + dönen "Afiyet olsun" rozeti |
