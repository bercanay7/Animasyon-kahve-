---
name: ses
description: Ses tasarımı ve altyazı — audio.py tarzı sentezlenmiş müzik/efekt, LUFS hedefi, faster-whisper ile Türkçe altyazı, TTS lisans uyarıları, CC0 ses kaynakları. Müzik, efekt, seslendirme veya altyazı işinde kullan.
---
# Ses

Mevcut `audio.py` (numpy+scipy sentez) kalıbını koru; yeni ses scriptleri ayrı dosyada.

## Kurallar
- Hedef **-14 LUFS**, true peak ≤ -1.5 dB. Ölçüm: `pip install pyloudnorm` (MIT) → `pyloudnorm.Meter(sr).integrated_loudness(data)`; ffmpeg `loudnorm` render'da uygulanır.
- Vuruşa oturt: BPM ızgarası, efektler görsel vuruşla aynı karede.
- Sentez: sinüs/üçgen + zarf (ADSR), gürültü vuruşlar, hafif reverb; her şey kodla → telifsiz.

## Altyazı (kendi seslendirmen için)
```bash
pip install faster-whisper stable-ts pysubs2
```
faster-whisper (MIT) `language="tr"`, CPU `compute_type="int8"`; kelime zamanları → stable-ts → pysubs2 ile ASS (UTF-8, font Patrick Hand/Baloo 2). Render'da `subtitles=` filtresiyle yak.

## Türkçe TTS — DİKKAT (ticari YouTube için)
Güvenli ve iyi açık Türkçe TTS **bulunamadı**. Yasak/riskli: Piper `tr_TR-dfki` (CC BY-NC-SA), Coqui XTTS-v2 (CPML, ticari değil), Meta MMS-TTS (CC-BY-NC). Kokoro (Apache-2.0) Türkçeyi desteklemiyor görünüyor (doğrulanmadı). Seçenekler: insan seslendirme + Whisper altyazı; sentez "mırıltı" dili + altyazı; ücretli ticari TTS (ElevenLabs bağlı).

## Hazır ses kaynakları
Kenney audio (CC0). Freesound: yalnız **CC0** filtresi, her dosyada lisansı tek tek doğrula (CC-BY atıf ister). Pixabay: CC0 değil, Content ID riski — `ASSETS.md`'ye yaz. pedalboard GPL-3.0: dağıtılan ürüne gömme.
