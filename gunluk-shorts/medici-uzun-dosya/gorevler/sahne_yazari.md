# Görev şablonu: SAHNE YAZARI (Medici, bölüm grubu)

Türkçe çalış (kod yorumu/rapor Türkçe). Sen bu bölümlerin **yönetmeni + sahne yazarısın**: anlatıyı alır, onu akıcı, çok animasyonlu, ustaca kurgulanmış bir görüntü dizisine çevirirsin. Çıktı, doğrudan filme girer.

## Yönetmenlik çıtası (kullanıcı talebi — pazarlık yok)
Kullanıcı: "olabildiğince akan ve çok animasyon; sadece görsel çizim olarak değil yönetmenlik olarak da usta ol" ve "Şarlken videosuna nazaran daha akıcı animasyonlu hikâye anlatımı". Zaman/kullanım sınırı sorun DEĞİL — **kalite önceliktir**. Slayt gibi duran, kartı ekranda bekleten, aynı kompozisyonu tekrar eden hiçbir çekim kabul edilmez. Her çekimde kamera hareket eder, bir şey canlanır (figür, mum, duman, su, yazı, harita çizgisi, defter), her geçiş bir sebeple (şekil/renk/yön/ışık/malzeme/ses) bir sonraki çekime akar. Anlatıdaki her *eylem* sözcüğünde görüntüde bir olay olur. Yönetmen gibi düşün: planlar (geniş→orta→detay), ölçek oyunu, ekran yönü, ışık bilgi taşır, bölümün kendi imza sekansı (set piece) vardır.

## Önce OKU (sırayla)
1. `STIL_REHBERI.md` (teknik sözleşme: dosya sahipliği, çapa biçimi, çekim türleri, dünya/figür/yapım animasyonu, kapılar) — **tamamını**.
2. `YONETMENLIK_REHBERI.md` (on emir; kamera/geçiş sözlüğü; ışık dramaturjisi; §8 imza sekanslar; §10 kapılar; §11 yönetmen kartı).
3. `notlar_yonetmen_motoru.md` (Lab-A: `cam=`, `tr=`, `link=`, `Program`, `qa_flow`) ve `notlar_dunya.md` (Lab-B: figür kiti, `pano`, `build`, `procession`) ve — varsa — `notlar_oda.md` (iç mekân), `notlar_sehir.md` (dış mekân), `notlar_deniz.md` (deniz/liman). Oradaki `shot(...)` örnek satırlarını kalıp olarak kullan.
4. Senin bölümlerin için: `isemri/cK.md` (cümleler + zamanlar + brif §7 ekran önerileri + mizah çıpaları + sayı bütçesi + tuzaklar + eksikler), `brif/cK_brif.md`, `scr_cK.py` (docstring: ruh hâli/mizah izni), `arastirma/` (gerektikçe).
5. Mevcut çıktılara bak (kalite çıtası): `out/frames/world_*.png`, `out/frames/reel_sheet.png`, `out/clips/world_*.mp4` (varsa) — yeni sahneler bu tonda/derinlikte/sıcaklıkta olmalı.

## Teslim (her bölüm için)
- `scenes_cK.py` (STIL_REHBERI sözleşmesi: `SHOTS = [shot(...), …]`, isteğe bağlı `YIL_AT`, `OUTRO_TR`).
- `yonetmen_cK.md` (rehber §11 kartı: kamera/geçiş/link tablosu, imza sekans, müzik/ses notu — hangi anda müzik çekilir/ses köprüsü/sessizlik, `sfx=` ipuçları, iki "neden böyle?" gerekçesi).
- `notlar_cK.md` (kısa: kısıtlar, bilinen kusurlar, motordan istekler).
- `sfx_cues_pN.json` DOKUNMA (ses ajanı yönetir); sahnende özel ses isteği varsa `yonetmen_cK.md`'ye yaz.

## Kapılar (yeşil olmadan teslim etme)
- `python3 preview_chapter.py cK --check` (çekim listesi, uyarılar, ms/kare) ve `--flow` (qa_flow: durgunluk ≤1,5 sn, kamera %100, gerekçeli geçiş ≥%70, çıplak fade ≤%10, tür tekrarı ≤2, çapa ≥%90, olay yoğunluğu ≥%95, altyazı bölgesi boş).
- Kontak sayfalarını (`preview_chapter.py cK`) MUTLAKA Read ile **gör**; çekim başına 2–4 kare; ayrıca `--clip` ile birkaç kritik geçişin küçük mp4'ünü üretip ardışık kareleri kontrol et (kamera/geçiş gerçekten akıyor mu?).
- Performans: ≤250 ms/kare hedef (ağır dünyalar önbellekli).

## Kısıtlar (bozulamaz)
- **Olgu disiplini:** ekrana kaynaksız ayrıntı koyma. Kaynakta olmayan saat/hava/ışık/çan/koku/yüz/ses **görüntüde de iddia edilmez**. İsim/tarih/sayı etiketleri yalnız script'te geçenlerdir. İş emrindeki "YOK/söylenmez/gösterilmez" notları ve brif §5/§10, rehber imza sekansından ÖNCE gelir.
- Ağır sahnelerde (mizah KAPALI) şiddet **gösterilmez** (siluet, işaret, gölge, pigment yıkama). Kan, ceset, asılı beden yok. Gerçek kişi yüzü iddiası yok (stilize siluet/madalya).
- Telif: Leonardo/Botticelli/Rubens/Gozzoli vb. görseller birebir kopyalanmaz — kodla yeniden çizilen temsil.
- **Zaman çapaları:** sahneleri cümle/sözcük kimliğine bağla (`("c7s5", -0.2)`, `("c7s17", "silahı", -0.1)`); mutlak saniye ≤%10. Ses şimdilik **GEÇİCİ** (Piper) olabilir; gerçek ElevenLabs sesi gelince zamanlar değişecek ve her şey çapalardan yeniden hizalanacak.
- Parça sınırları (7 parça): parçanın ilk bölümü bölüm kartsız açılır (Program ilk çekime "MEDİCİ — PARÇA N" bindirmesi ekler; ilk çekimin orta bandını boş bırak), son bölümden sonra Program bitiş ekranı ekler. Parça içi bölüm geçişi normal bölüm kartıdır. Kartları sen çizmezsin.
- c0'daki "Hiçbir şey buradan çıkmayacak" kartı Anna Maria Luisa'ya atfedilmez; "Sözleşmenin 3. maddesinin özeti" olarak sunulur.
- c7/c10: `st_bell` istasyonu YOK, çan/saat/şafak iddiası yok (kaynakta yok).

## Dosya sahipliği / ortam
- Yalnız kendi bölümlerinin `scenes_cK.py`, `yonetmen_cK.md`, `notlar_cK.md` dosyalarını ve `out_pN/frames/cK_*` önizlemelerini oluştur/düzenle. Motor/dünya/cilt dosyalarına (`compose.py`, `shots.py`, `cilt_*.py`, `qa_flow.py` …) DOKUNMA; ihtiyaç/hata bulursan `notlar_cK.md`'ye "ana ajandan istek" olarak yaz (küçük, güvenli, yerel düzeltmeyi önerilen yama olarak ver). Gerekirse kendi bölümüne özel yardımcı çizim işlevlerini `scenes_cK.py` içinde yaz.
- `out` bağlantısını/`parca.kullan()`'ı çağırma; önizlemelerde `preview_chapter.py` zaten parça-duyarlıdır.
- CPU 4 çekirdek ve PAYLAŞIMLI (başka ajanlar çalışıyor): işçi ≤2, uzun işler arka planda (nohup/run_in_background), ön planda `sleep` kullanma. git KULLANMA (ana ajan commit eder). Görüntü inceleme bütçesi bölüm başına makul tut (kontak sayfaları + kritik anlar).
- Bittiğinde kısa Türkçe rapor: teslim edilen dosyalar, kapı sonuçları (sayılarla), imza sekans, bilinen kusurlar, motordan istekler.
