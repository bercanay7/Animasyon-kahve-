# Günlük Shorts — "Zaman Kuryesi"

> **Kurallar:** her yeni video `konsey/KANAL_ANAYASASI.md`'ye göre yapılır (21 koltuklu danışma kurulunun kararı; gerekçe: `konsey/RECOMMENDATION.md`).

Her video kendi klasöründe (kod + çıktı). Ortak altyapı: Pillow 2x süper örnekleme, 1x metin katmanı, ffmpeg pipe, numpy/scipy ses, −14 LUFS.

| Klasör | Konu | Stil | Ses |
|---|---|---|---|
| `../zaman-kuryesi-zanzibar/` | Tarihin en kısa savaşı (1896) | düz renkli illüstrasyon + kinetik yazı | müzik/efekt, seslendirmesiz |
| `emu-savasi/` | Emu Savaşı (1932) | **kara kalem / kömür çizimi**, titreyen çizgiler | **heyecanlı Türkçe seslendirme (ücretsiz, çevrimdışı)** |
| `dans-vebasi/` | Dans Vebası (1518) | kâğıt-kesme kolaj | heyecanlı Türkçe seslendirme |
| `titanik-kehaneti/` | Titanik'in Kehaneti (v2, TESLİMAT #4) | blueprint | kuru erkek ses (Piper dfki) |
| `sitma-geri-dondu/` | Türkiye'de sıtma: neredeyse bitti, neden döndü? (TESLİMAT #5) | blueprint + Türkiye haritası/nokta | kuru erkek ses, en iyi-5 sentez + Whisper doğrulama |
| `dune-star-wars/` | Dune × Star Wars: Tatooine Arrakis'ten mi geldi? (TESLİMAT #6, **özel video**, 2 dk 36 sn) | **kâğıt kesme diyorama** (katmanlı kumullar, gölgeli kâğıt, "KANIT n/5" etiketi, serif altyazı) | kuru erkek ses, **yavaş tempo** (hız 0,90; cümle araları 0,4–0,9 sn), en iyi-5 sentez + Whisper doğrulama |
| `pellagra-mikrop-degildi/` | Pellagra: mikrop değildi, tabaktı (TESLİMAT #7, **özel video**, ~1 dk 33 sn) | **guaj kukla** (boyalı kâğıt-kukla: gölgesiz boyalı alanlar, mürekkep kontur, eklemli kuklalar, sahne başına palet, whip geçişleri; Alfa Slab One + Fraunces) | `fahrettin` sesi (Piper, CC0 veri seti; kullanıcının kör test seçimi), hız 0,96, cümle araları 0,4–0,95 sn, en iyi-5 sentez + zor sözcük kapısı + Whisper doğrulama |

## Yönetim belgeleri (2026-10-17)

| Belge | Ne |
|---|---|
| `konsey/VIZYON.md` | **vizyon, amaç, kapsam** (tarih + edebiyat + oyun + kesişim), biçim merdiveni (Kısa → Özel → Uzun Dosya), ses vizyonu (2026-10-18) |
| `konsey/KANAL_ANAYASASI.md` | **v2.1**: kurallar (kimlik, kanca, ses, kapılar, ölçüt, platform haritası, uyum, kadans, ölçüm) |
| `konsey/ANAYASA_ANALIZI_2026-10-17.md` | v1 → v2 analizi: gerçek veri, bulgular (B1–B9), gerekçeler, kaynaklar |
| `konsey/YOL_HARITASI.md` | 13 haftalık işletim planı: fazlar, yayın kuyruğu, haftalık ritim, deneyler, kapılar, riskler, karar bekleyenler |
| `olcum/` | ölçüm günlüğü (`olcum.csv`) ve protokol |
| `konsey/ses_testi/lisans_karsilastirma/` | ses lisansı kör testi (A/B/C) |
| `konsey/ses_testi/SES_BRIFI.md` | ses brifi ve 60 sn test metni (kendi ses / seslendirmen / premium TTS) |

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

Stil fikirleri: kara kalem (bu video), çöp adam, kinetik tipografi (yalnız yazı), harita animasyonu, defter/karalama, blueprint (mavi çizim), kolaj/kağıt kesim, guaj kukla (boyalı kâğıt kukla — TESLİMAT #7 kullandı).

**Kural (kullanıcı düzeltmesi, 2026-10-15):** her konu kendi çizim diline sahip olur — bir önceki videonun cildi (blueprint, kara kalem, kâğıt kesme …) tekrar kullanılmaz; anlatım yavaş ve bağlamlı olur (ayrıntı: `konsey/KANAL_ANAYASASI.md` §12).
