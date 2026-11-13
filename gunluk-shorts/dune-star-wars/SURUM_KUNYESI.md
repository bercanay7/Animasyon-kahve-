# Dune × Star Wars — sürüm künyesi (Kanal Anayasası, kalite kapısı)

- Tarih: 2026-10-16 · Seri: TESLİMAT #6 · Biçim: **özel video** (kullanıcı kararı, Shorts üst sınırı 3 dk) · Cilt: **kâğıt kesme diyorama** (kullanıcı kararı: her konu kendi çizim dilini taşır; bir önceki video blueprint'ti) · Kanca türü: **S (soru/merak)** · pencere_video_no: 2
- Süre: 156 sn, 3744 kare, 24 fps, 1080x1920 · Konuşulan kelime: 276 · Konuşulan yıl: 1977, 1985; sözle ayrıca "on iki", "yirmiden fazla", "on altı", "beş". Ekranda ayrıca 1965, 1984 ve ≈40 / ≈31 milyon $ ("kaynaklara göre yaklaşık" etiketiyle, seste yok)
- Ses: Piper VITS `dfki` (kuru erkek, yankı 0), **hız 0,90** (Sıtma videosunda 1,12), virgül boşluğu 0,22 sn, iki nokta 0,30 sn, cümle araları 0,35–0,90 sn · sherpa-onnx 1.13.8 · pyworld 0.3.5 (kadın dönüşümü kullanılmadı)
- Seçim: ifade başına en iyi-5 sentez; Whisper-medium (sherpa-onnx, çevrimdışı) doğrulaması, yabancı ad/sayı için jokerli WER (`tts_best.py`)
- Müzik/efekt: sentezlenmiş Frigya (Phrygian) ped + rüzgâr + hafif nabız, sahneye bağlı efektler (daktilo, tebeşir, vurma, klaket, damga); konuşma müziği 0,85, efektleri 0,40 oranında kısar
- Motor: Python 3.13.16 · Pillow 12.3.0 · numpy 2.5.3 · scipy 1.18.1 · pyloudnorm 0.2.0
- Kamera: her sahnede yavaş "nefes alan" itme + eliptik kayma (zoom %2,6–5), 3 vurgu anında kısa zoom itişi; HUD ve altyazı sabit; kapanışta sönerek ilk kareyle birebir aynı karta oturur
- Kodlama: ffmpeg 6.1.1 (libx264 crf 19, yuv420p, bt709, AAC 192k). Tane (grain) 0,0075: 0,05 değeri hareketli sahnede bit hızını 2,4× yapıp dosyayı 134 MB'a çıkardı
- Ölçüm (kodlanmış mp4): −14,0 LUFS, true peak −2,0 dBTP, LRA 1,9 LU · dosya 56,1 MB (≈2,9 Mb/sn)
- Kapılar: kaynak (`kaynaklar.md`; ikincil kaynaklar, arama özetleri — birincil metinler açılamadı, iddialar "anlatıldığına/bildirildiğine göre" diye çekinceli) ◐ · Türkçe/telaffuz (WER + sözlük; insan kulağı kontrolü YAPILMADI; özellikle "Dyun", "Tatuin", "Lukas", "Linç", "Cedinin") ◐ · QC (`qa.py` çıkış kodu 0; 9/9 kapı: kare sayısı, boş kare, HUD, yazısız seri, ilk=son kare, ilk ses, 2 sn'lik durağan pencere, freezedetect, süre) ✔
- Not (hareket sınırları): Anayasa "video başına ≤2 sarsıntı, ≤1 flaş" kuralı 40 sn'lik Shorts için yazıldı; 156 sn'lik özel videoda süreyle ölçeklenerek okundu (3 sarsıntı: damga, klaket, kapanış kartı; 3 flaş aynı anlarda). Gerekirse sonraki özel videolarda kural açıkça ölçeklenmeli.
