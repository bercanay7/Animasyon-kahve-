# Medici Parça 1/7 — sürüm künyesi (Kanal Anayasası, kalite kapısı)

**Durum (5 Kasım 2026):** **v3.1** hazır (kurul tur 3 düzeltmeleri; tur 3'te 10 üyeden 9'u ONAY), **kurul tur 3b (v3.1 gerileme kontrolü) sürüyor** (sonuç `kurul/KURUL.md`). Yayın kararı ve YouTube Studio ayarları kanal sahibinde. Kulak kontrolü (yamalı cümleler + orijinal kayıttan iki yer) kullanıcıda: `yayin/KULAK_KONTROL_P1.md`.

## Dosya
- `out_p1/medici_P1.mp4` (**v3.1**) — 1920×1080, 24 fps (CFR), 14.437 kare, **601,54 sn (10:01,5)**; H.264 High **seviye 4.1, 4 referans** (libx264 crf 19, preset slow, aq-mode 3, psy-rd 1.0:0.15, VBV 24M/48M; kurul TE1-Y6), ≈11,5 Mb/sn; **BT.709 sınırlı aralık** (rgb24 → yuv420p dönüşümü açıkça BT.709; kurul TE1 bulgusu düzeltildi), SAR 1:1; AAC 205 kb/sn; ses ve görüntü dili `tur`; faststart. Dosya 862 MB (yüklemeye uygun; repoya girmez).
- Üretim: `p1_uret.sh` (VER=v31: qa_flow → geçiş sesleri → miks → render → birleştir → mux → QA; bütün oda önbelleği yeniden çizildi); render 13 segment, 2 işçi, 33,8 dk, kare hatası 0; `.done` dosyalarında çizelge özetinin yanında **kod özeti** (ae58fa355abb; 13 segment tek özet) ve birleştirmede kare sayısı/akış imzası/renk etiketi öz sınaması (kurul TE1-Y11, §8); segment başında deklanşör ısınması (n0−1 çizilip atılır) ve `.done` dosyalarında zaman çizelgesi özeti, birleştirme öncesi denetlendi (kurul TE1 §5–6); birleşim kayıpsız (`-c copy`).

## Ölçüm
- Ses: **−14,04 LUFS** (BS.1770; ffmpeg ve pyloudnorm bağımsız ölçümleri −14,04), **true peak −1,80 dBTP** (AAC çözülmüş −1,48), LRA 3,5 LU; video/ses süre farkı 0,01 sn; bitiş ekranı kuyruğu 11,3 sn (çıkış 10 sn).
- Görüntü QA (`render.py --qa`): kare hatası 0; siyah/donuk bölge 0.
- Akış ve yerleşim (`qa_flow.py --part 1`, `out_p1/qa_flow_v31.txt`): **20 GEÇTİ · 0 KALDI · 1 UYARI · 1 PAS** (v3: 19 GEÇTİ · 2 UYARI; "beyan ↔ gerçekleşen kamera" UYARI'dan GEÇTİ'ye; `qa_yerlesim` yeni "yarım yazı" uyarısı: yalnız 55,8 sn'de III. maddeye itilirken kenardan kayan Romen rakamları, geçici). Önceki v3 sonucu — tur 2 sonrası yeni kapılar: beyan ↔ gerçekleşen kamera, aynı görüntü kesmesi, ışık geçişi bütçesi (≤4); `qa_yerlesim` artık levha/yazı çakışmasını da ihlal sayar (ihlal 0); dönem ihlali 0 (`qa_donem`, Loggia kuralı dahil). Hareket: durgun kare oranı %0,17, en uzun durgun koşu 0,5 sn (`out_p1/kurul/hareket.json`).
- Altyazı (`yayin/medici_P1_tr.srt`): 158 replik, ort. 14,0 kar/sn, azami 17,0; ≤ 2 satır; yetim replik birleştirme, sayı/unvan ve ad parçacığı bölünme kuralları ("III. Edward", "Michele di Lando"; `make_srt.py`).

## Anlatım ve ses lisansı
- Ses: **ElevenLabs kütüphane sesi "Emrullah"** (voice_id `DpEiQMnL9WxMsymCsjPY`, kategori *professional*; kütüphane tanımı: "Emrullah Uzun brings over 20 years of professional voice-over…"), model `eleven_v4`, `generations_count=1`. voice_id her üretimde `creative_list_voices` ile doğrulandı (CLAUDE.md kuralı).
- Bölüm sesleri c0–c2: 18 Ekim 2026. **Cümle yamaları (4 Kasım 2026): 14 cümle, 1.840 kredi** — c1s10, c1s11, c1s16, c1s18, c1s23, c1s24, c1s26, c2s1, c2s7, c2s10, c2s20, c2s21, c2s27, c2s30 (gerekçeler `kurul/KURUL.md`; ham klipler ve kaynak kaydı `ses_ham/yama_p1/`, `KAYNAK.json`). Yöntem: ilk sözcüğün yutulmasına karşı başa kesilecek bağlam cümlesi, kırpma, yerel ASR (Whisper medium, sherpa-onnx) doğrulaması, ham bölüm sesine 10 ms ızgarasında yerleştirme (`ses_yama_bolum.py`; yama dışı örnekler v1 ile bit bit aynı).
- Hizalama (`ses_hizala_asr.py`): 85/85 cümle durakta başlar/biter; seste bulunmayan sözcük 0 (önceden 2: orijinal kayıtta "Çözüm," ve "Roma'da" yutulmuştu — yamalandı).
- **Lisans notu:** ses, sahibinin ElevenLabs Ses Kütüphanesi'nde ticari kullanıma açtığı profesyonel bir sestir; kanal bu sesi klonlamadı, taklit etmedi ya da değiştirmedi; kullanım ElevenLabs hizmet koşulları ve kullanıcının ücretli aboneliği kapsamındadır. Anayasa U3 ("gerçek bir kişinin sesi klonlanmaz/taklit edilmez") ile çelişmez: bu bir taklit değil, sahibinin **rızalı lisansla** paylaştığı kütüphane sesidir (kurul tur 2, KA2-Y7). Kütüphane kullanım koşullarının ekran görüntüsü kanal sahibinin hesabından alınmalıdır (bu ortamdan erişilemiyor).

## YouTube Studio
- **"Değiştirilmiş veya yapay içerik": Hayır** (kanal uygulaması; CLAUDE.md kanal dersleri) + açıklamada "Ses: yapay zekâ ile üretilmiş anlatıcı sesi (ElevenLabs, "Emrullah")…" satırı. Gerekçe: içerik açıkça kodla çizilmiş animasyon; gerçek bir kişinin söylemediği bir şeyi söylüyormuş gibi gösterilmesi ya da gerçekçi olay/kişi üretimi yok.
- **Muhalefet şerhi:** KA2 (tur 1 Ö6, tur 2) YouTube Yardım metnine dayanarak **"Evet"** öneriyor. Son karar kanal sahibinin.

## Görsel, müzik, efekt
- Görüntünün tamamı kodla çizildi (Python 3.13.16, skia-python 144.0.post2, numpy 2.5.3, numba 0.68.0; ffmpeg 6.1.1). Harici görsel, fotoğraf, yapay zekâ görseli yok. Kurul tur 1 sonrası motor: dönem katmanı (`donem.py`), ekran uzayında levha kıstırma ve otomatik kontrast zemini, HUD 300×66, 0,25–2,4 sn geçişler ve sert kesme, seçici deklanşör (hareket bulanıklığı), madalya v3 (1438 öncesi otomatik TEMSİLÎ damgası), figür temas gölgesi.
- Müzik ve efektler sentez (`muzik.py`, `sfx.py`; 85 müzik çıpası, 105 SFX cue, 62 otomatik geçiş sesi); yazı tipleri SIL OFL (Cinzel, Cormorant, EB Garamond).
- Kapaklar (motor + Pillow): `yayin/studio_paketi_P1/kapak_P1_K1.jpg` ("SON MEDİCİ / MİRASI KİLİTLEDİ") ve `kapak_P1_K2.jpg` ("FAİZ YASAKTI"); denetim `out_p1/kapak/kapak_qa_P1.png` (kahraman yazı ≥ %18, kontrast 10,1:1 / 10,4:1, süre rozeti ve fare üstü bölgeleri boş, koyu temada kenar ayrışması: 168 px kenar ort. gri 38, gri < 25 payı %8–10; parıltı kolları yok; K2 arması videoyla aynı red8). Yayın: K1 varsayılan, Test ve Karşılaştır 14 gün, başlık sabit (`yayin/studio_paketi_P1/00_yayin_adimlari.txt`).

## Kaynak kapısı
- `kaynaklar_P1.md` (85 cümle): **● 51 · ◐ 17 · ○ 2 · ANEKDOT 1 · YORUM 12 · — 2**; cümle cümle teyit tablosu `kurul/teyit_P1.md` (birincil metinler curl ile açıldı: Villani, Boccaccio, Stefani, Dante, Machiavelli, Cavalcanti; araştırmalar: de Roover 1963 tam metin, Treccani DBI, Casciu 2006, Online Catasto of 1427).
- Paket metni: `yayin/studio_paketi_P1/01–05` (`paket_P1.py`): başlık "Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?", 9 bölüm damgası, kaynak listesi yalnız gerçekten okunanlar (Tim Parks "anlatımda anılan; okunmadı" diye ayrı).

## Kurul
- Tur 1 (P1 v1): 10/10 RED (AN1 6,5 · AN2 7,0 · SA1 7,5 · SA2 5,0 · KA1 6,0 · KA2 7,0 · PK1 6,0 · PK2 6,0 · TE1 8,0 · TE2 7,0); motor kararı: yeniden yazma değil, iyileştirme.
- Tur 2 (P1 v2): PK1 9,0 ONAY; diğerleri RED (AN1 7,5 · AN2 8,4 · SA1 8,6 · SA2 8,5 · KA1 8,5 veto · KA2 8,0 veto · PK2 8,5 · TE1 8,7 · TE2 8,6). Ortak engelleyici: papanın elinde hançer (471,7 sn) → şiddetsiz "bulla" jesti. Düzeltmeler dört pakette (ENG-C, ENG-D, SCN-1, SCN-2) + başkan; raporlar `kurul/duzeltme_tur2/`.
- Tur 3 (P1 v3): sürüyor; sonuçlar `kurul/KURUL.md`.
