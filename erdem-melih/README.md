# Erdem Melih Tattoo Studio: Reels kurgusu (22 Kasım 2026)

Kanal dışı iş (kullanıcının isteği). Büyük video dosyaları depoya girmez; yalnız kod, logo ve fontlar.

| Dosya | Ne |
|---|---|
| `tools/logo_temizle.py` | Instagram profil ekran görüntüsünden logoyu ayıklar, 5 kat büyütür, kenarları yumuşatır: `logo/em_logo_beyaz.png` (şeffaf), `logo/em_rozet.png` (siyah daire) |
| `tools/hazirla.sh` | iPhone MOV → vidstab ile sabitlenmiş 1440x2560 ara kopya |
| `audio/muzik.py` | Özgün müzik (numpy sentezi, 96 BPM; logo vuruşu tam 5,0 sn'de). Lisans sorunu yok |
| `kurgu.py` | 1080x1920 Reels: renk düzeni, iPad'e doğru yavaş yaklaşma, iki yazı (Cinzel; logodaki serife yakın), zoom vuruşu, logo kartı + ışık süpürmesi + "RANDEVU İÇİN DM". `--muziksiz` ile Instagram'ın kendi müziği eklenecek sürüm; `--kare=N:dosya.png` ile tek kare |
| `fonts/` | Cinzel (SIL OFL 1.1) |

Akış:
```
tools/hazirla.sh IMG_3515.MOV ara/
python3 audio/muzik.py ara/muzik.wav 8.5
python3 kurgu.py ara/stab.mov ara/muzik.wav ErdemMelih_Reel_muzikli.mp4
python3 kurgu.py ara/stab.mov ara/muzik.wav ErdemMelih_Reel_muziksiz.mp4 --muziksiz
```
Yeni klipte `kurgu.py` içindeki `KEYS` (izlenecek nesnenin konumu) ve yazı metinleri değiştirilir.

Kullanılan açık kaynaklar: FFmpeg + vid.stab (GPL; yalnız araç olarak, çıktıya kod girmez), Pillow, numpy, Cinzel (OFL).
