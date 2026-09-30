# Dünya Kahve Günü · Instagram Animasyonu

15 saniyelik, 1080×1920 (9:16) Reels / Story videosu — tamamen kodla çizildi.

- `dunya-kahve-gunu.mp4` — Instagram'a yüklenecek video (H.264, 30 fps, sessiz ses kanalı)
- `kapak.png` — Reels kapak görseli
- `animation.html` — animasyonun kaynağı; tarayıcıda açınca canlı oynar (tıklayınca başa sarar, `?t=12` ile tek kare)
- `render.js` — kare kare MP4 çıkışı: `NODE_PATH=$(npm root -g) node render.js` (Playwright + ffmpeg gerekir)

## Senaryo
| Süre | Sahne |
|---|---|
| 0–3 sn | Kahve çekirdeği düşer, zıplar: "Psst… Yarın ne var, biliyor musun?" |
| 3–6.3 sn | Uykulu, boş fincan esner — "1 EKİM · Dünya Kahve Günü" |
| 6.3–7 sn | Kahve dalgası ekranı kaplar |
| 7–10 sn | Cezve Türk kahvesi döker, fincan uyanır, buhar kalbe döner; saat 15.00'e döner |
| 10–15 sn | Üç fincan tokuşturur: "Kahveler bizden! Yarın saat 15.00'te tüm misafirlerimize ikramımızdır" |
