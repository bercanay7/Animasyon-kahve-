# KURUL BRİFİ — Medici Parça 1 (TUR 1: son render + kapak + yayın paketi kapısı)

Sen "Zaman Kuryesi" kanalının BAĞIMSIZ KURUL'unda bir üyesin. Kanalın kurul yöntemi `/home/user/sisifos-wt/CLAUDE.md` içinde ("Kurul (bağımsız değerlendirme) yöntemi" ve "Kapak dersleri"): OKU. Her alanda iki üye vardır, her biri FARKLI bir mercekle bakar; **bağımsız ilk bakışta başka üyenin raporunu görmezsin ve başka üyenin yazdığı dosyaları OKUMAZSIN** (`kurul/tur1/` altında yalnız kendi dosyanı yaz). Başkan (ana oturum) çapraz eleştiriyi sonra ister. Eşik ≥9/10 ONAY.

## Ne değerlendiriliyor
**Medici Parça 1/7** (c0–c2; 10:02; 1920×1080, 24 fps, H.264 + AAC; ElevenLabs "Emrullah" sesiyle gerçek anlatım; sentez müzik/SFX; ekranın tamamı KODLA çizilmiş animasyon). Yeni bir kanal videosu değil, 7 parçalı Medici serisinin ilk parçası: anlatıcı hikâyeyi 1743'teki son Medici kadınından (Anna Maria Luisa) başlatır, florin şehrine döner, Giovanni di Bicci'nin bankasını, kambiyoyu, çifte kaydı ve "vicdan komitesi"ni anlatır; sonu Cosimo'nun kuledeki hücresine bağlanan bir kapıdır.

**Kullanıcının görsel talebi (pazarlıksız):** "olabildiğince akan ve çok animasyon; sadece görsel çizim olarak değil yönetmenlik olarak da usta ol." Kanal çıtası: Sisifos/Orfeus videoları (kodla çizilmiş, güçlü kapaklı); kullanıcı ayrıca şunu sordu: **"Bu animasyon ve çizim motorundan emin misin? Bağımsız kurula bir değerlendirt."** Bu yüzden ALANINA göre motoru da değerlendir (aşağıdaki "Motor sorusu").

## Kanıt (hepsi bu makinede; mutlak yollar)
Proje: `/home/user/Animasyon-kahve-/gunluk-shorts/medici-uzun-dosya/` (aşağıda `P/`).
- **Video:** `P/out_p1/medici_P1.mp4` (601 MB; kopyalama; kare çıkarmak için kendi scratch dizininde ffmpeg kullan, ör. `ffmpeg -ss 125 -i … -frames:v 1 x.png`). Sen videoyu OYNATAMAZSIN, sesi dinleyemezsin: kare dizileri, ölçümler ve belgelerle değerlendir; bunu raporunda açıkça belirt.
- **Hazır kanıt paketi:** `P/out_p1/kurul/`: `genel_01…04.png` (tüm süreyi ≈9 sn adımla tarayan 4×4 kontak sayfaları), `gecis_*.png` (10 geçiş çevresinde 0,125 sn adımlı 8 karelik şeritler: akış/hareket kanıtı), `tam_01…12_*.png` (tam çözünürlüklü 12 kare), `hareket.json` (0,5 sn adımlı kare farkı eğrisi), `teknik.json` (ffprobe), `qa_flow_ozet.txt` (yönetmenlik kapıları: 11 GEÇTİ / 0 KALDI; çekim tablosu: kamera, geçiş, link, süre).
- **Kapaklar:** `P/yayin/kapak_P1_A.jpg` (ana başlık freski), `_B.jpg` (1743 odası + belge), `_C.jpg` (florin yığını); `kapak_P1_kontrol.png` (320×180 üçlü şerit). Kanal referansları: `/home/user/sisifos-wt/sisifos/kapak.png`, `kapak_b.png`, `/home/user/sisifos-wt/orfeus/kapak_final_*.jpg`, `/home/user/sisifos-wt/sarlken_kapak/*.jpg`.
- **Yayın paketi taslağı:** `P/yayin/studio_paketi_P1/` (01_baslik, 02_aciklama, 03_sabit_yorum, 04_etiketler, 05_bolumler, SRT), `P/yayin/medici_P1_tr.srt`, `P/yayin/YAYIN_TASLAK.md` (7 parça için başlık alternatifleri).
- **Anlatı metni ve kaynaklar:** `cd P && python3 script.py c0` (ve c1, c2; söylenen metin), `P/scr_c0.py…scr_c2.py` (ekran metni + kaynak sınıfı etiketleri), `P/kaynaklar_P1.md` (kaynak kapısı: ● hiçbiri; ◐/○ düzeyi; yayın öncesi teyit listesi), `P/brif/c0_brif.md…c2_brif.md`, `P/arastirma/` (araştırma notları).
- **Sahne yönetmen kartları:** `P/yonetmen_c0.md`, `yonetmen_c1.md`, `yonetmen_c2.md`, `notlar_c0.md…notlar_c2.md`; sahne dosyaları `P/scenes_c0.py…c2.py`.
- **Motor belgeleri:** `P/STIL_REHBERI.md`, `P/YONETMENLIK_REHBERI.md` (on emir, kamera/geçiş sözlüğü, ölçülebilir kapılar), `P/notlar_yonetmen_motoru.md`, `P/notlar_dunya.md`, `P/notlar_oda.md`, `P/notlar_sehir.md`, `P/notlar_deniz.md`, `P/KAPSAM_VE_YAPI.md`.
- **Kanal çıtası (karşılaştırma):** Sisifos hattı (Chromium + Canvas 2D): `/home/user/sisifos-wt/sisifos/README.md`, `/home/user/sisifos-wt/CLAUDE.md` (30 fps, 4 alt örnekli hareket bulanıklığı, vazo-resmi figür iskeleti, 1920×1080 CRF 18). Kanalın Anayasası: `/home/user/Animasyon-kahve-/gunluk-shorts/konsey/KANAL_ANAYASASI.md` (özellikle §12-15/16/18, §4 miks).

## Motor hakkında bilmen gerekenler (kısa)
Medici motoru: Python 3 + skia-python (CPU) + numba; kendi "fresk ve defter" cildi; ≈35 çekim türü (başlık, harita, defter, belge, madalya, sayaç, çubuk/soy ağacı/ağ, panorama, yapım animasyonu, iç mekân `oda`, dış mekân `sehir`, deniz `deniz/liman`, figür kiti [yandan "kesme-bebek": yürüme, konuşma, yazma, sayma…]); kamera ön ayarları (push/pull/pan/crane/orbit/hand/rack/track/keyframes); 12 geçiş türü, her geçiş bir `link=` gerekçesine bağlı (şekil/renk/yön/ışık/malzeme/ses); cümle/sözcük çapaları (ses değişse görüntü kayar); `qa_flow` ölçülebilir kapıları. 24 fps; hareket bulanıklığı YALNIZ geçişlerde (deklanşör ≈0,3 kare), çekim içi kamera/figür hareketinde yok; kare başına ≈100–350 ms (4 işçiyle 10 dk'lık parça ≈17 dk render). Kullanıcı ses/sözcük ve kaynak konularında "tek hata kabul etmem" çizgisinde.

## RAPOR BİÇİMİ (kendi dosyan: `P/kurul/tur1/<KOD>.md`; sonra başkana kısa özet mesajı ver)
1. **Karar:** ONAY ya da RED + puan (x/10; eşik ≥9) — alan puanını ver, "iyi niyetli" şişirme yapma.
2. **Ne gördüm / neye dayandım:** bakılan dosyalar/kareler/ölçümler (hangi kare ya da zaman damgası); sesi duyamadığını ve videoyu oynatamadığını kabul et.
3. **Sıralı düzeltme listesi:** her madde: kare/zaman damgası + 1920×1080 koordinatı (gerekirse) + NE yapılmalı + ÖNEM (engelleyici / önemli / küçük). Engelleyici = bu düzelmeden yayına çıkılmaz.
4. **En emin olmadığım nokta.**
5. **Motor sorusu (alanına göre, 6–10 cümle):** "Bu motor [alanın açısından] yeterli mi? Sisifos hattıyla kıyasla somut fark nedir? Yeniden yazmaya/başka motora geçmeye değer mi, yoksa mevcut motoru iyileştirmek mi? En yüksek getirili 3 iyileştirme (maliyet tahminiyle)." Dürüst ol: "iyi" demek için yazma; zayıf yer varsa adını koy.
6. Başka üyenin görüşünü bilmediğini varsay; çekimser kalma, gerekçeli ol.

Yalnız `P/kurul/tur1/<KOD>.md` dosyanı yaz (ve /tmp altında scratch). Diğer dosyalara DOKUNMA. git KULLANMA. Ağır süreç çalıştırma (render yok); ffmpeg ile kare çıkarma ve küçük Python serbest; aynı anda tek ağır işlem.
