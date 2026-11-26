# Depodan çıkarılan video dosyaları (27 Kasım 2026)

Bitmiş video çıktıları güncel sürümden çıkarıldı: yeni oturumlar her açılışta ~560 MB'ı boşuna indiriyordu. Hepsi çıktıdır; hiçbir betik bunları girdi olarak kullanmaz (`render.js`/`render.py` üretir, `qa.py` üretileni denetler).
Git geçmişinde duruyorlar. Biri gerekirse:

```bash
git show f951739c7e1554914ceb2bf3339198c803b1f8dc:YOL > dosya.mp4
```

Kural: bitmiş video depoya girmez (`.gitignore`: `*.mp4`). Teslim kopyaları kullanıcının arşivinde (Google Drive önerisi, `kanal/DURUM.md`). Küçük önizleme gerçekten gerekiyorsa `git add -f`.

| Dosya | Boyut |
|---|---|
| `29-ekim/cumhuriyet-103-siyah-beyaz.mp4` | 28.8 MB |
| `29-ekim/cumhuriyet-103.mp4` | 38.6 MB |
| `gunluk-shorts/dans-vebasi/out/Dans_Salgini.mp4` | 39.0 MB |
| `gunluk-shorts/dans-vebasi/out/Dans_Salgini_kucuk.mp4` | 23.4 MB |
| `gunluk-shorts/dune-star-wars/out/Dune_Star_Wars.mp4` | 56.1 MB |
| `gunluk-shorts/emu-savasi/out/Emu_Savasi.mp4` | 37.5 MB |
| `gunluk-shorts/emu-savasi/out/Emu_Savasi_kucuk.mp4` | 22.1 MB |
| `gunluk-shorts/pellagra-mikrop-degildi/out/Pellagra_Mikrop_Degildi.mp4` | 71.1 MB |
| `gunluk-shorts/pellagra-mikrop-degildi/out/Pellagra_Mikrop_Degildi_fahrettin.mp4` | 63.8 MB |
| `gunluk-shorts/sitma-geri-dondu/out/Sitma_Geri_Dondu.mp4` | 18.8 MB |
| `gunluk-shorts/titanik-kehaneti/out/Titanik_Kehaneti.mp4` | 16.6 MB |
| `gunluk-shorts/titanik-kehaneti/out/Titanik_Kehaneti_erkek.mp4` | 17.0 MB |
| `gunluk-shorts/titanik-kehaneti/out/eski/Titanik_v1_erkek.mp4` | 17.0 MB |
| `gunluk-shorts/titanik-kehaneti/out/eski/Titanik_v1_kadin.mp4` | 17.0 MB |
| `gunluk-shorts/titanik-kehaneti/out/noaudio.mp4` | 15.6 MB |
| `sisifos/sisifos_shorts.mp4` | 29.3 MB |
| `zaman-kuryesi-zanzibar/out/Zanzibar_Savasi.mp4` | 30.9 MB |
