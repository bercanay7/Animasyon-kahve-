# Erdem Melih Tattoo Studio: Reels kurgusu (22 Kasım 2026)

Kanal dışı iş (kullanıcının isteği). Büyük video dosyaları depoya girmez; yalnız kod, logo ve fontlar.

| Dosya | Ne |
|---|---|
| `tools/logo_temizle.py` | Instagram profil ekran görüntüsünden logoyu ayıklar, 5 kat büyütür, kenarları yumuşatır: `logo/em_logo_beyaz.png` (şeffaf), `logo/em_rozet.png` (siyah daire) |
| `tools/hazirla.sh` | iPhone MOV → vidstab ile sabitlenmiş 1440x2560 ara kopya |
| `audio/muzik.py` | Özgün müzik (numpy sentezi, 96 BPM; logo vuruşu tam 5,0 sn'de). Lisans sorunu yok |
| `kurgu.py` | 1080x1920 Reels: renk düzeni, iPad'e doğru yavaş yaklaşma, iki yazı (Cinzel; logodaki serife yakın), zoom vuruşu, logo kartı + ışık süpürmesi + "RANDEVU İÇİN DM". `--yazisiz` ile hiç yazı ve üst logo olmadan, yalnız sonda logo (kullanıcının son tercihi, 22 Kasım); `--muziksiz` ile Instagram'ın kendi müziği eklenecek sürüm; `--kare=N:dosya.png` ile tek kare |
| `kurgu_surec.py` | İkinci Reels (IMG_3514, 14 sn, Drive'dan): 01 KARŞILAMA → 02 TASARIM → 03 UYGULAMA. Hız eğrisi (yürüyüşler 2 kat, hareket bulanıklığıyla), yazı arkasında yumuşak koyu bant, son vuruşta mor dövme şablonuna yaklaşma (konum renkle ölçüldü). Logo 12,5 sn'de, toplam 16 sn |
| `fonts/` | Cinzel (SIL OFL 1.1) |

Akış:
```
tools/hazirla.sh IMG_3515.MOV ara/
python3 audio/muzik.py ara/muzik.wav 8.5
python3 kurgu.py ara/stab.mov ara/muzik.wav ErdemMelih_Reel_muzikli.mp4
python3 kurgu.py ara/stab.mov ara/muzik.wav ErdemMelih_Reel_muziksiz.mp4 --muziksiz
```
İkinci Reels:
```
tools/hazirla.sh IMG_3514.MOV ara2/   # (bu klipte smoothing=18, optzoom=2 kullanıldı)
python3 audio/muzik.py ara2/muzik.wav 16.0 20 2.75,6.85
python3 kurgu_surec.py ara2/stab.mov ara2/muzik.wav ErdemMelih_Surec_muzikli.mp4
```
Drive'daki 10 MB'tan büyük dosya: kullanıcı dosyayı "bağlantıya sahip herkes" yapınca `drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t` ile indirildi.

Yeni klipte `kurgu.py` içindeki `KEYS` (izlenecek nesnenin konumu) ve yazı metinleri değiştirilir.

Kullanılan açık kaynaklar: FFmpeg + vid.stab (GPL; yalnız araç olarak, çıktıya kod girmez), Pillow, numpy, Cinzel (OFL).
