# Günlük Shorts — "Zaman Kuryesi"

> **Kurallar:** her yeni video `konsey/KANAL_ANAYASASI.md`'ye göre yapılır (21 koltuklu danışma kurulunun kararı; gerekçe: `konsey/RECOMMENDATION.md`).

Her video kendi klasöründe (kod + çıktı). Ortak altyapı: Pillow 2x süper örnekleme, 1x metin katmanı, ffmpeg pipe, numpy/scipy ses, −14 LUFS.

| Klasör | Konu | Stil | Ses |
|---|---|---|---|
| `../zaman-kuryesi-zanzibar/` | Tarihin en kısa savaşı (1896) | düz renkli illüstrasyon + kinetik yazı | müzik/efekt, seslendirmesiz |
| `emu-savasi/` | Emu Savaşı (1932) | **kara kalem / kömür çizimi**, titreyen çizgiler | **heyecanlı Türkçe seslendirme (ücretsiz, çevrimdışı)** |

## Ücretsiz Türkçe seslendirme (para yok, hesap yok)
Piper VITS Türkçe modelleri (`fettah`, `dfki`, `fahrettin`) + `sherpa-onnx` (pip). Çevrimdışı çalışır, ~0.3 sn'de 6 sn konuşma üretir.
```
pip install sherpa-onnx
# modeller (GitHub sürüm dosyası, ~67 MB her biri):
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2   (dfki, fahrettin de aynı kalıpta)
tar xjf vits-piper-tr_TR-fettah-medium.tar.bz2 -C ses-modelleri/ex_fettah
cd emu-savasi && python3 tts.py --voice=fettah
```
`tts.py`: cümleleri sentezler → "heyecanlı" işleme (perde+tempo yükseltme, parlaklık, sıkıştırma) → kelime zamanlarını `out/timeline.json`'a yazar. Görüntü ve altyazı bu zamanlara bağlanır.
`ses-modelleri/ornekler/` içinde üç sesin örnekleri var.

## Yeni gün, yeni video (iş akışı)
1. `emu-savasi/` klasörünü kopyala → `yeni-konu/`.
2. `tts.py` içindeki `SENTENCES` listesini yeni metinle değiştir (`gösterilen=söylenen`, `*vurgu*`).
3. `scenes.py` içinde sahneleri `timeline.json` zamanlarına (`wt("C", 3)` gibi) bağlayarak çiz.
4. `python3 tts.py && python3 audio.py && python3 render.py` → mux → `python3 qa.py`.

Stil fikirleri: kara kalem (bu video), çöp adam, kinetik tipografi (yalnız yazı), harita animasyonu, defter/karalama, blueprint (mavi çizim), kolaj/kağıt kesim.
