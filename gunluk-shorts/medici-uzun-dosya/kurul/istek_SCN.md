# istek_SCN — P1 sahne yazarından motor isteklerı (kurul tur 1, 4 Kasım)

Sahne tarafında geçici çözümle kapatılanlar ve motorda kalıcı çözüm isteyenler. Dosya sahipliği: sahne yazarı yalnız `scenes_c0–c2.py`, `c0–c2_kinds.py`, `p1_ortak.py`, `yonetmen_c0–c2.md`, `notlar_c0–c2.md`.

## ENG-B (compose / cilt_fx / qa_flow)
1. **Çekim başına HUD gizleme** (`shot(hud=False)` ya da `HUD_SKIP`'e tür ekleme): SA2-Ö1 "Cenova 1340 / Pacioli 1494 zaman çizelgesi çekimlerinde rozeti kıs ya da gizle" (c2 çekim 12, `p1_timeline`, ≈414–422 sn; HUD 1402 gösterirken kart 1340/1494 diyor). Kapak yankısı için HUD gizleme ENG-B'de yapıldı (teşekkürler).
2. **Bölüm düzeyi kaplama kancası** (sahne modülünde `OVERLAY = fn(cx)` → bölümün tüm çekimlerinde, geçişlerde iki yanın üstünde bir kez): c1 yol haritası çipleri (PK2-K7) şimdilik `P.with_ovl(SHOTS, P.roadmap(...))` ile her çekime ekleniyor; geçiş sırasında iki çekimde aynı konumda çizildiği için görünür sorun yok ama motor kancası daha temiz olur.
3. **Aile etiketleri**: yeni sahnelerde aile varsayılanları doğru (p1_oda/p1_sehir = dünya, c1_okul/c1_machiavelli/c2_sadaka = figür, kapak_kilit = kart). Ek istek yok; `AILE` sözlüğü gerekmedi.

## ENG-A / cilt_oda (oda alt sınıfları)
4. **Raf nişi için yatık defter seçeneği**: `cilt_oda.draw_alcove(..., flat=True)` (1397–1430 için yatık yığın; SA2-K5). Şimdilik `p1_ortak.P1Banka._draw_wall` üst sınıfın duvar çizimini kopyalayıp `_alcove_flat` kullanıyor (iç yardımcılara bağımlı: `FILLP, LGP, _RS, R, draw_book, GRAD_V, ashlar, cornice, draw_window, wainscot`). Motorda seçenek olursa kopya kaldırılır. Aynısı `Calisma/kutuphane` için de (c1s20 ve c2 Machiavelli odası ≈1520: sırt dışarı kabul).
5. **Oda katmanı önbelleği sürümü**: disk önbelleği `oda_{world}_{tod}_{katman}_{i}_{OVER}.png` alt sınıf çizim kodu değişince bayat kalıyor (P1Banka duvarı için `out/_cache/world/oda_p1banka_*_wall_*` elle silindi). İstek: sınıf özniteliği `CACHE_VER` dosya adına girsin.
6. **Alt sınıf kayıtları** (`OD.ROOMS["p1banka"|"p1ofis"|"p1salon"|"p1yatak"]`, `_PN.WORLDS["p1corridor"]`) çalışma anında `p1_ortak` içinde; motor iç adları değişirse bunlar kırılır — değişiklikte haber verin.

## Kapak (kapak_medici)
7. `kapak_kilit` türü `ovl` almıyor; sahne dosyası `P.add_ovl(["kapak_kilit"])` ile sarıyor (tarih künyesi için). Türe yerleşik `kunye=(satır1, satır2)` parametresi olursa sarmalama kaldırılır.

## Madalya (cilt_medal v3)
8. 1438 öncesi madalyalara motorun otomatik "TEMSİLÎ" damgası: c2'deki elle eklenen "TEMSİLÎ PORTRE" levhaları kaldırıldı (Lorenzo c2s27, Cosimo c2s34); c1'de madalya kalmadı (Giovanni artık figür).
