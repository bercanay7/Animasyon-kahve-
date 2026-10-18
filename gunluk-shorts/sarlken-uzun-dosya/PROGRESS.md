# Şarlken Dosyası — Uzun Dosya #1 (çalışma notları ve durum)

**Görev (kullanıcı, 2026-10-18 gece):** İmparator Şarlken (V. Karl / I. Carlos) dönemini bütün yönleriyle (hayatı, dünya tarihine etkisi) anlatan ilk uzun video. Süre sınırı yok; soru sorma; animasyon, ses, paylaşım dahil her şeyi ben yönetirim. Ses için ElevenLabs tercih edildi. Geçmiş videolara takılma, öne bak.

## Kararlar (ben verdim, gerekçeli)
- **Biçim:** Uzun Dosya, 16:9 (1920×1080, 24 fps), hedef ≈15–18 dk, bölümlü (≈12 bölüm × 60–100 sn), soğuk açılış = 25 Ekim 1555 Brüksel abdikasyonu.
- **Cilt (görsel dil):** "parşömen + mürekkep + yaldız" (Rönesans harita/gravür/el yazması). Önceki videolardan ayrı: guaj kukla (Pellagra), kâğıt kesme (Dune), mavi baskı (Titanik/Sıtma). Karakterler eklemli kuklaların uyarlaması (`kukla.py`), haritalar Natural Earth 50m (kamu malı) + elle çizilmiş tarihsel bölge poligonları (shapely), armalar kodla.
- **Ses:** ElevenLabs'e bu ortamdan erişilemiyor (ağ politikası `api.elevenlabs.io`'yu 403 ile engelliyor, ortamda anahtar yok). Bu yüzden: (1) animatik için Piper `fahrettin` (en iyi-K + zor sözcük kapısı), (2) `ses_paketi/` ElevenLabs'e yapıştırılacak paragraf bazlı metin + okunuş notları, (3) `ses_ice_aktar.py` dış sesi `timeline.json`'a hizalar → tek komutla yeniden render.
- **Zaman kaynağı:** `out/timeline.json` (cümle ve kelime zamanları) → `cues.py` → sahneler/altyazı/ses efektleri (Pellagra ile aynı düzen). Ses değişince görüntü otomatik uyar.
- **Yazı tipleri (OFL, Türkçe glifler denetlendi):** Cinzel (başlık), Cormorant Garamond (altyazı/gövde), IM Fell English/DW Pica (harita etiketi), EB Garamond.
- **Kaynak kapısı:** her olgu CONFIRMED/NİTELİKLİ/ANEKDOT; anekdotlar "rivayet" diye anlatılır. Çıktı: `kaynaklar.md`.

## Dosya haritası
`engine.py` (16:9 çizim bağlamı) · `inkpaint.py` (boyalı şekil ilkelleri) · `paper.py` (parşömen/çerçeve/mühür/süs) · `mapper.py` + `regions.py` (harita) · `figures.py` (karakterler) · `heraldry.py` (armalar) · `shots.py` (çekim şablonları) · `scenes.py` (bölüm/çekim listesi) · `script.py` (anlatım) · `tts.py`/`tts_best.py`/`dogrula.py` (ses) · `ses_ice_aktar.py` · `cues.py` · `ui.py` (altyazı, bölüm kartı) · `audio.py` · `compose.py` · `render.py` · `qa.py`.

## Durum (en son güncelleme aşağıda)
- [x] Klasör, yazı tipleri, harita verisi
- [ ] Araştırma (5 ajan: A1 miras/seçim, A2 Reform, A3 Osmanlı/Akdeniz, A4 Yeni Dünya/finans, A5 Fransa/kişisel/abdikasyon)
- [ ] Senaryo + okunuş + ses paketi
- [ ] Motor + harita + karakterler + çekim şablonları
- [ ] Sahneler
- [ ] Ses (animatik) + müzik + miks
- [ ] Render + QA + düzeltmeler
- [ ] Yayın paketi + fragman (Kısa) + özet
