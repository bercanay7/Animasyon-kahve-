# Zaman Kuryesi · Zanzibar Savaşı (1896) — YouTube Shorts

1080×1920, 24 fps, 42.000 sn, Türkçe, seslendirmesiz; hikâye kelime kelime pop eden altyazılarla anlatılır.
Önceki Roma_Betonu kodu bu depolarda bulunamadığı için aynı yöntem sıfırdan kuruldu:
Python + Pillow, 2x süper örnekleme, yazılar kamera zoom'undan SONRA 1x tuvale, ham RGB → ffmpeg pipe, ses numpy/scipy ile sentez, −14 LUFS.

## Çıktılar (`out/`)
- `Zanzibar_Savasi.mp4` — H.264 (CRF 17, bt709), AAC 192k stereo 48 kHz, −14.1 LUFS, ≈ −1.1 dBTP
- `audio.wav`, `kontak_sayfasi.png` (her sahneden 3 kare, 6 sütun), `saniyelik_kareler.png` (videodan saniyede 1 kare)

## Çalıştırma
```
pip install pillow numpy scipy pyloudnorm
python3 audio.py                 # out/audio.wav  (−14 LUFS)
python3 render.py                # out/zanzibar_noaudio.mp4  (4 süreç, ~2 dk)
ffmpeg -i out/zanzibar_noaudio.mp4 -i out/audio.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart out/Zanzibar_Savasi.mp4
python3 qa.py                    # otomatik denetim + kontak sayfaları
python3 contact.py out/x.png 1.0 2.0 ...   # istenen anların kontak sayfası
```

## Dosyalar
| Dosya | Görev |
|---|---|
| `engine.py` | 2x süper örneklemeli çizim bağlamı, kamera (zoom/kaydırma/sarsıntı/parallax), easing, kelime sprite'ı |
| `art.py` | duvar saati, saray, İngiliz gemileri, Zaman Kuryesi + at, zarf, fatura, patlama/duman/alev |
| `events.py` | **ortak zaman çizelgesi**: top atışları, isabetler, savaş saati eğrisi, flaş/sarsıntı, tıkırtı — görüntü ve ses aynı veriyi kullanır |
| `scenes.py` | 5 sahne grubu (10 senaryo sahnesi) |
| `ui.py` | savaş saati (HUD, y≈260), altyazı yerleşimi, damga/mühür sprite'ları, vinyet |
| `compose.py` | whip pan geçişleri, flaş, HUD + altyazı, döngü karesi |
| `audio.py` | sentez + miks + −14 LUFS |
| `qa.py` | boş kare, HUD, yazısız seri, ilk/son kare, hareket denetimi |
| `fonts/` | Poppins Bold (altyazı/HUD), Lora Bold (başlık/damga) — OFL |

## Tutma tasarımı
- **Savaş saati** (⏱ MM:SS, y=260) her karede: 00:00 → (09:00'dan itibaren) 02:00 → 30:00 → 38:00'da donar, kırmızı yanıp söner → finalde 00:00'a sarılır.
- **Açık döngü**: 3. sn "asıl şok sonra geldi" → 32. sn zarf geri gelir → 38. sn cevap (fatura).
- **Döngü**: 41.9 sn'den sonraki kareler 0. kareyle birebir aynıdır (piksel farkı 0); ses, 42.0'daki tıkırtıyla 0.0'daki tıkırtıya bağlanır. Kapanış ekranı yok.
- Güvenli alan: içerik 200–1440 px, altyazı y≈1290–1400, en küçük yazı 42 px.

## Tarihsel not
Savaş saati, 09:00'daki ültimatom bitişinden sayılır (ilk atış 09:02 → 02:00); kaynaklara göre süre 38–45 dk arasında değişir (videoda not olarak belirtilir).
