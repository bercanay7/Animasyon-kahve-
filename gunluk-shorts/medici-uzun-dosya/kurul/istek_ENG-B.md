# ENG-B → Başkan: istekler ve bildirimler (4 Kasım 2026)

1. **Kamera ön ayarları `cilt_cam.py`'de** (cilt_fx/compose/shots dışında): brif gereği bildiriyorum; bu dosyayı düzenledim (açık sayılı eski `cam=` değerleri birebir aynı kamera durumunu verir — eski/yeni karşılaştırma farkı 0).
2. **Miks kuyruğu:** parça sonu bekleme eklendi (`compose.END_HOLD = 1,3` sn; anlatı bittikten sonra son çekim sürer, sonra bitiş ekranı). Video 1,3 sn uzar → `miks.py --tail 8.3` (= `compose.TAIL`). `miks_kur.py` içindeki `gate_windows(..., 7.0, ...)` kuyruk sabitleri de 8,3 olmalı (sizin dosyanız).
3. **CARD_GAP:** fresk başlığı 4,5 sn'lik karta göre yeniden zamanlandı (panel 0–1,5 sn, MEDİCİ 1,4 sn'de tam, çıkış geçişine dek ≥2,2 sn tam okunur). Önerilen `ses_birlestir.CARD_GAP["c0"] = 4.5` (güncel çizelgede zaten 4,5 görünüyor).
4. **Geçiş sesleri:** geçiş süreleri/kesmeler değişti → `MEDICI_PART=1 python3 miks_kur.py --sadece-gecis` ile `sfx_gecis.json` yeniden üretilmeli (motor sesleri Program'dan okur; kesmelere ses gitmez).
5. **YouTube uç ekranı:** bitiş ekranı yuvaları 30 px yukarı alındı: (330, 610, 520×292) ve (1070, 610, 520×292); Studio'daki uç ekran öğeleri buna hizalanmalı. Etiketler #E9C770 38 px, koyu levha üstünde.
6. **YONETMENLIK_REHBERI.md (sizin dosyanız) güncellenmeli:** HUD "sağ üst 420×110" → `cilt_fx.HUD_RECT` (1548, 72, 1848, 138); §3 "süre ≤ 1,0 sn" → 0,25–2,4 sn + `tr="cut"`; §2 `cam=` verilmezse artık tohumlu otomatik seçim (qa "örtük" saymıyor); §10 yeni kapılar. Ayrıntı: `notlar_hareket.md`.
7. **Duvar önbelleği:** `cilt_wall.WALL_VER = 4` (giornata yumuşatma). 18 duvarın v4'ü üretildi, v3 PNG'leri silindi (34 MB). Yazım artık atomik (paralel işçi yarım PNG okumaz).
8. **Deklanşör ve QA araçları:** `Program.frame(n, post=False)` çağrılarında (qa_flow, qa_yerlesim, qa_donem) deklanşör uygulanmaz; render (`post=True`) uygular. `Program(part=N, shutter=False)` tümden kapatır.
