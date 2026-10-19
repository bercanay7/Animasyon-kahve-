# Dış mekân / şehir dünyası — Lab-E notları (taslak, ilerleme kaydı)

Durum (kayıt): `cilt_sehir.py` + `preview_sehir.py` yazıldı; `cilt_kinds4.py` korumalı import döngüsüne `"cilt_sehir"` eklendi.
Tamamlanan ön ayar: **meydan** (ates, odun, palle, pencere). Sıradakiler: sokak, kale (sur/castel/passetto), skyline_dikey. Bu dosya bitişte tam sürümle (API, ölçümler, kusurlar, c0–c16 tablosu) yeniden yazılacak.

Komutlar: `python3 preview_sehir.py [ad…] [--no-clip] [--ms] [--bake] [--at SN] [--workers 2]` → `out/frames/sehir_<ad>.png`, `out/clips/sehir_<ad>.mp4`.
