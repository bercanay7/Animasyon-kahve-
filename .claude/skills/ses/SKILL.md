---
name: ses
description: Ses tasarımı ve altyazı — audio.py tarzı sentezlenmiş müzik/efekt, LUFS hedefi, ElevenLabs çıktısıyla kurgu, altyazı, CC0 ses kaynakları. Müzik, efekt, seslendirme veya altyazı işinde kullan.
---
# Ses

Mevcut `audio.py` (numpy+scipy sentez) kalıbını koru; yeni ses scriptleri ayrı dosyada.

## Kurallar
- Hedef **-14 LUFS**, true peak ≤ -1.5 dB. Ölçüm: `pip install pyloudnorm` (MIT) → `pyloudnorm.Meter(sr).integrated_loudness(data)`; ffmpeg `loudnorm` render'da uygulanır.
- Vuruşa oturt: BPM ızgarası, efektler görsel vuruşla aynı karede.
- Sentez: sinüs/üçgen + zarf (ADSR), gürültü vuruşlar, hafif reverb; her şey kodla → telifsiz.

## Seslendirme: ElevenLabs (ekip kendi hallediyor)
Seslendirme ElevenLabs'te yapılır; burada TTS araştırılmaz/önerilmez. Bu repoda yalnızca:
- ElevenLabs çıktısını WAV/MP3 olarak `AUDIO=` ile render'a ver (loudnorm -14 LUFS zaten uygulanır).
- Konuşmaya göre kurgu: cümle sınırlarında görsel değişim; kelime zamanları için ElevenLabs transkripti (veya `faster-whisper`, MIT, `language="tr"`) → ASS altyazı (`pysubs2`) → render'da `subtitles=` ile yak.
- Müziği konuşmanın altında tut (≈ -18 dB), konuşma varken efektleri kıs.
- ElevenLabs lisans/plan ticari kullanım koşulları ekibin hesabına bağlıdır; `ASSETS.md`'ye plan notu düş.

## Hazır ses kaynakları
Kenney audio (CC0). Freesound: yalnız **CC0** filtresi, her dosyada lisansı tek tek doğrula (CC-BY atıf ister). Pixabay: CC0 değil, Content ID riski — `ASSETS.md`'ye yaz. pedalboard GPL-3.0: dağıtılan ürüne gömme.

## Bu kanalın ses hattı
Anlatıcı ElevenLabs **"Emrullah"** (kanalın sesi, değişmez; `voice_id` her seferinde `creative_list_voices` ile bulunur). Her bölüm iki çekim → Whisper doğrulama → `tools/build_vo.py`. Müzik `audio/score.py` (numpy/scipy, özgün), efektler ElevenLabs + `tools/mix.py` içinde sentez; hedef -14 LUFS / -1 dBTP (İngilizce dublaj -2 dBTP). **Kredi harcayan üretim yalnız kullanıcı açıkça isterse; aynı çağrıyı "yeniden dene" diye tekrarlama.** Ayrıntı: kökteki `CLAUDE.md`.
