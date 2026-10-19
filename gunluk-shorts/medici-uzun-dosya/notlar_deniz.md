# Deniz, liman ve gemi dünyası — Lab-C notları (19 Ekim 2026) — TASLAK (çalışma sürüyor; her aşamada güncellenir)

Dosyalar: `cilt_deniz.py` (modül), `preview_deniz.py` (önizleme), `notlar_deniz.md` (bu belge), `out/frames/deniz_*.png`, `out/clips/deniz_*.mp4`, önbellek `out/_cache/world/deniz_*_<sürüm>.png` (sürüm = dosya içerik özeti; kod değişince eski dosyalar otomatik silinir).
`cilt_kinds4.py` sonundaki korumalı import `cilt_deniz`'i yükler (dokunulmadı). Kendi kamerası olan türler `cilt_cam.OWN_CAMERA`'ya çalışma anında eklenir (pano gibi): `cams=` kullanılır; `cam=` ön ayarı `cams` yoksa yolun yerine geçer.

## Komutlar (proje dizininden; TEK işçi, ölçek 0,5, kare kare yazım)
```
python3 preview_deniz.py acik_kadirga --no-clip     # kontak sayfası (6 kare) → out/frames/deniz_acik_kadirga.png
python3 preview_deniz.py acik_kadirga               # sayfa + klip → out/clips/deniz_acik_kadirga.mp4
python3 preview_deniz.py --at acik_kadirga 5.0      # tam çözünürlüklü tek kare
python3 preview_deniz.py --ms acik_kadirga          # ms/kare (CM.post dâhil)
python3 preview_deniz.py --energy acik_kadirga      # klip hareket enerjisi + ölü pencere
```

## 1. Çekim türleri (taslak; ayrıntı sonda)
* `deniz` (scene="acik"|"rota"|"filo"|"kiyi") ve takma türler `deniz_rota`, `deniz_filo`, `deniz_kiyi` (tür tekrarı kuralı için ayrı adlar), `liman` (variant=…, year=…).
* Ortak parametreler: `tod` (day|dusk|night|fire), `ships=[dict(kind, x0, x1 | dir+speed, y, scale, flag, t0, t1, sails, oars, crew, highlight, route, ease)]`, `cams=[(çapa,(x,y,zoom)),…]`, `wind`, `wind_dir`, `swell`, `foam`, `horizon`, `sun`, `birds`, `clouds`, `coast`, `kick`, `caption`.
* Bağımsız işlevler: `ship(f, kind, x, y, h, t, dir=1, flag=None, sails=True, oars=True, …)`, `wave_layers(f, t, tod, …)`, `flag(c, x, y, w, h, t, …)`, `gulls(ctx, …)`, `sky_image/draw_sun/draw_clouds`.
