# Şarlken Dosyası — Uzun Dosya #1 (durum ve kullanım)

**Konu:** İmparator V. Karl (Şarlken / I. Carlos): hayatı, çağı, dünya tarihine etkisi. Zaman Kuryesi'nin ilk uzun videosu. Soğuk açılış 25 Ekim 1555, Brüksel; sonra beş cephe: bankacı, keşiş, kral, sultan, miras.
**Durum (18 Ekim 2026):** video, altyazı, kapaklar, Kısa fragman ve yayın paneli hazır. Yükleme ve zamanlama Studio'da kullanıcıda (bu ortamda YouTube'a yayın yapabilen bağlayıcı yok).

## Çıktılar
| Dosya | Ne |
|---|---|
| `out/sarlken_uzun_yukleme.mp4` | **YouTube'a yüklenecek video**: 21:26, 1920×1080, 24 k/sn, CRF 22 (tune animation), ses −14,1 LUFS; kullanıcıya gönderilen sürüm (git dışı) |
| `out/sarlken_uzun.mp4` | ana kopya, ≈9 Mb/sn, 1,47 GB (git dışı; gönderim sınırı 500 MB'ı aştığı için yalnız bu ortamda) |
| `out/sarlken_onizleme_720p.mp4` | hızlı izleme sürümü (720p) |
| `teslim_parcalar/sarlken_uzun_ANA.mp4.001…004` | ana kopyanın dört parçası (≈350 MB'lık, gönderim sınırı için); birleştirme: `cat sarlken_uzun_ANA.mp4.00* > sarlken_uzun.mp4` ya da Windows'ta `copy /b …`; SHA-256 `402a4ec4856cacb7…` (git dışı) |
| `yayin/sarlken_tr.srt` (+ `.vtt`, `_zamansiz.txt`), `yayin/bolumler.txt` | Türkçe altyazı (v2: çakışmasız; v1'deki 23 çakışma Studio'da "Failed" verebiliyor), yedek biçimler, bölüm zaman damgaları |
| `yayin/kapak_A/B/C.jpg` | küçük resim adayları (A önerilen) |
| `yayin/sarlken_kisa_fragman.mp4` | dikey Kısa (giriş kancası, yakılmış altyazı) |
| `yayin/YAYIN_PAKETI.md`, `yayin/yayin_paneli.html` | başlık, açıklama, etiket, yorum, Studio adımları (panel: kopyala düğmeli) |
| `yayin/kulak_kontrol/*.mp3` | dört kısa ses kesiti (kulak kontrolü için) |

## Kararlar (gerekçeli)
- **Biçim:** 14 bölüm (giriş + 13), ≈21 dk. Süre sınırı yok denildi; her bölümde cümle başına bir görsel olay, kaynak sınıfı ekranda damgalı.
- **Görsel dil:** kahve-altın "boyalı levha"; diorama (siluet + parallaks), harita, madalya portreleri, belge/damga kartları. Tamamı kodla (Skia), fotoğraf yok. Madalyalar ve figürler stilize; gerçek yüz taklidi yok.
- **Ses:** ElevenLabs eleven_v4, anlatıcı Emrullah (`DpEiQMnL9WxMsymCsjPY`); aday: Eyyup Okan (`sqN4QwtcnanCCWx6TTYj`). Müzik ve 28 ses efekti sentez; miks −14 LUFS, TP < −1 dBTP. Gerçek kişi sesi klonlanmadı.
- **Kaynak kapısı:** her olgu CONFIRMED / NİTELİKLİ / ANEKDOT (rivayet) / YORUM / HAFIZA; rivayet ve tartışmalı yerler ekranda damgalı (RİVAYET, TARTIŞMALI, YAKLAŞIK…). Ayrıntı: `kaynaklar.md`, düzeltmeler: `METIN_DEGISIKLIKLERI.md`.
- **Zaman kaynağı:** `out/timeline.json` (cümle ve kelime zamanları). Çekimler cümle/sözcük çapalarına bağlı; ses değişirse görüntü uyar.

## Nasıl yeniden üretilir
```
python3 preview_chapter.py c4 --check          # çekim listesi, uyarılar, ms/kare (CPU süresi)
python3 preview_chapter.py c4 -k 2 --cols 4 --scale 0.4   # kontak sayfaları → out/frames/
python3 qa_program.py [--static]               # çapa, yer tutucu sahne, kare örnekleme (hata/ms)
python3 qa_text.py                             # ekran yazıları: anlatımda geçmeyen sayılar
python3 render.py --all --workers 4            # parçalı render (kaldığı yerden sürer; --segs 7-16 ile seçmeli)
python3 render.py --concat && python3 render.py --mux   # birleştir, miksi ekle → out/sarlken_uzun.mp4
python3 render.py --qa; python3 render.py --overview    # siyah/donuk bölge, kare hatası; genel bakış kareleri
python3 miks_kur.py                            # müzik + SFX + konuşma miksi (out/sfx_cues.json'dan efektler)
python3 make_srt.py; python3 kapak.py; python3 kisa_fragman.py; python3 yayin/panel_kur.py
```
Tek cümleyi yeniden seslendirmek: `script.py` → `ses_yama.py --prepare` → ElevenLabs (tek cümle, `generations_count=1`) → Scribe hizalama → `ses_yama.py --apply` → `miks_kur.py` → ilgili parçaları yeniden render (`.done` işaretini sil).
Sesi tümden değiştirmek (ör. B adayı): `script.py`'den tüm bölümleri yeniden seslendir (≈16 bin kredi + Scribe ≈7 bin), yeni zaman çizelgesini kur, `miks_kur.py`, tam render.

## Dosya haritası
- **Motor:** `sk.py` (Skia, tipografi, post), `shots.py` (çekim şablonları), `stage.py` (diorama, 1.5× süper-örnekli katmanlar, figür sprite önbelleği), `mapsk.py` (harita, döşeme önbelleği), `compose.py` (program, geçişler, HUD, bölüm kartları, kapanış), `render.py`.
- **Kütüphaneler:** `medal.py`/`medal_extra.py` (49 madalya), `icons.py`/`icons_extra.py` (64 simge), `figs_*.py` (52 figür tipi), sahne laboratuvarları `scenes_lib.py` (salon), `scenes_sea/field/siege.py` (deniz, ova, kuşatma), `scenes_rooms.py` (11 iç mekân); kataloglar `SAHNE_KATALOGU_*.md`, `notlar_figur_lab.md`, `notlar_madalya_lab.md`.
- **Bölümler:** `scenes_c0…c13.py` (+ `kinds_c*`, `stage_c*`, `shots_c*`, `kit_a.py`, `bw_lib.py`, `d_common.py`); her bölümün `notlar_cK.md` dosyasında çekim listesi, ekrandaki olgular ve kaynak sınıfı, bilinen kusurlar var.
- **Ses:** `miks_kur.py` → `miks.py`, `muzik.py`, `sfx.py`, `ses_dsp.py`; `ses_yama.py`; `ses_kontrol_listesi.md` ("şu 10 yeri dinle").
- **Yayın:** `make_srt.py`, `kapak.py`, `kisa_fragman.py`, `yayin/panel_kur.py`.
- **Denetim:** `qa_program.py`, `qa_text.py`, `preview_chapter.py`.

## Bilinen kusurlar (dürüst liste)
- **Kulak denetimi yapılmadı.** Özel adların telaffuzu (Şarlken, Yörg, Halkulvadi, Tenoçtitlan, Komünero) yalnız otomatik çözümlemeyle denetlendi; müzik ve SFX yalnız sayısal ölçüldü.
- Kalan HAFIZA maddeleri `kaynaklar.md` §7'de; yayından önce sayfa düzeyinde teyit önerilir.
- Haritalardaki sınırlar yaklaşık (ekranda yazar). Kuşatma kaleleri, Tenochtitlan ve bazı armalar şematik; figür-lab siluetleri sade (Wartburg yazarı sakalsız, kalabalıklar benzer).
- c11'de yatak odası c12 ile aynı oda; Mühlberg planı ve gezi ağı şematik (ekranda notlu). Gümüş akışı eğrisi şematik (c10).
- Sayaçlar animasyon sırasında ara değerlerden geçer (veri iddiası değil).
- Ses lisansı: ElevenLabs'te ticari kullanım ücretli plan ve Voice Library lisansına bağlı; yayın öncesi kontrol edilmeli. Studio'da "sentetik içerik: Evet" önerilir.
- Windsor.ai'ye YouTube bağlı değil; ölçüm Studio ekran görüntüleriyle ya da bağlantı kurulunca otomatik (`olcum/VERI_MERKEZI.md`).

## Çalışma günlüğü (özet)
Araştırma + kaynak kapısı → senaryo → motor → ElevenLabs sesi + yamalar → madalya/figür/sahne laboratuvarları (paralel ajanlar) → bölüm yazarları A–D → müzik/SFX/miks → render, birleştirme, denetim → yayın paketi. Oturum 04:22 ile 08:14 UTC arasında kota sınırı nedeniyle kesildi; A (c1,c2,c3,c10) ve D (c0,c9,c12,c13) bölüm yazarları son cilayı yarıda bıraktı, tüm bölümler çalışır durumda ve denetimden geçti.
