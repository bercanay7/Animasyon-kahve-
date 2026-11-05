# AN1 — TUR 3b · Animasyon ve kurgu / ANİMASYON YÖNETMENİ — Medici Parça 1 v3.1 (gerileme kontrolü)

## 1. Karar
**ONAY — 9,3 / 10.** Tur 3'te 9,0 vermiştim; eşik ≥9.

Tur 3'te açık, kısmen ya da yeni olarak bıraktığım dört hareket maddesinin dördü de v3.1'de kapandı: Y7, Y-N1, Y-N2, Y-N3. Benim alanımda gerileme bulmadım. Kalan tek yumuşak yer: ölüm döşeği çekimleri #89 ve #93 (541–546 sn penceresi, medyan 0,43). Bunları tur 3'te ağır sahne olarak kabul etmiştim; değişmedi.

| Başlık | Tur 3 | Tur 3b |
|---|---:|---:|
| Geçiş dili | 9,0 | 9,3 |
| Kamera (ölçülen) | 9,0 | 9,3 |
| Figür ve nesne animasyonu | 8,5 | 9,0 |
| Akış | 9,5 | 9,5 |
| Ölü/donuk kare | 9,0 | 9,5 |
| 24 fps + deklanşör | 8,5 | 9,3 |

## 2. Dayanak
**Sınır:** videoyu OYNATAMADIM, sesi DUYAMADIM.

- **Okuduklarım:**
  - `KURUL_BRIFI_P1_TUR3B.md`, `tur3_duzeltme_listesi.md`, `KURUL.md` ("Tur 3 — v3 sınaması");
  - `duzeltme_tur3/SCN-3.md` (§1, §3) ve `ENG-E.md` (§1, §2, §6, §10, §11);
  - `out_p1/qa_flow_v31.txt` (20 GEÇTİ · 0 KALDI · 1 UYARI; UYARI kabul edilmiş #15 yön uyarısı);
  - `out_p1/uretim_v31.log` (14.437 kare, 601,54 sn).
- **Ölçümler v3.1 videosunda yeniden koşuldu**, tur 3'teki yöntemlerle. Scratch dizini: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/an1v31/`.
  - Her kare için kare farkı → `pf_v31.json`.
  - 8 kare/sn merkez maskeli zincirleme LK kamera → `chainC_v31.json`, `chainrepC2_v31.txt`.
  - Farneback hız profilleri (eller, anahtarlar).
  - Kare dizileri ve büyütmeler (JPEG):
    - `yn1_v31.jpg`, `hands_v31.jpg`;
    - `coin_zoom_v31.jpg`, `y7_events_v31.jpg`, `calendar_counter_v31.jpg`;
    - `counter88_v31.jpg`, `ghost_check_v31.jpg`, `c2_new_v31.jpg`, `f110_v31.jpg`.
- **Yöntem notu:** `ffmpeg -ss` ile kare dizisi çekerken ilk kare çift geliyor. Bu kareyi attım, ölçümleri ona göre yaptım.

| Ölçü (bütün video) | v3 | **v3.1** |
|---|---:|---:|
| Kare farkı medyanı: bütün / çekim içi | 1,36 / 1,32 | 1,37 / 1,33 |
| Sessiz süre (0,5 sn medyanı <0,25) | 12,6 sn (%2,1) | **7,2 sn (%1,2)** |
| ≥1,5 sn sessiz koşu | 2 | **0** |
| Neredeyse özdeş ardışık kare | 14 çift (12'si #63'te) | **2 çift**: 25,42–25,46, mumun kasıtlı karanlık anı |
| Kesme girişi/çıkışı donuk (<0,12) | 3 | **0** (38 kesmede) |
| Kayan 10 sn pencere medyanı <0,5 | 359 / 541–546 / bitiş ekranı | **541–546 / bitiş ekranı** |

## 3. Tur 3 maddelerimin durumu

| Madde | Durum | Kanıt (v3.1) |
|---|---|---|
| **Y7** Küçük hızlı nesnelerde deklanşör | **KAPANDI** | Ayrıntı aşağıda. |
| **Y-N1** 367,9–369,3 ölü bağlantı | **KAPANDI** | `yn1_v31.jpg`. #63 harita artık iterek ilerliyor: +%14,5 ve −107 px / 7,3 sn, ≈%2/sn (v3: −%2,8). Son saniyedeki kare farkı 0,65–0,95 (v3: 0,01–0,09, donma). Kesme hareket üstünde: önce 0,70, sonra 1,08. BORÇ #64'ün ilk karesinde (368,86) hazır. #63 çekim içi medyanı 0,47 → 1,15. |
| **Y-N2** Yakın plan ellerde katı kayma | **KAPANDI** | Ayrıntı aşağıda. Çekim içi medyan #62 0,84 → 1,24; #81 0,20 → 0,93. |
| **Y-N3** Kesme girişinde 1 karelik duruş | **KAPANDI** | Kesme sonrası ilk üç adım: 43,9 (#8) 0,37/0,45/0,57 (v3: 0,07); 575,5 (#98) 1,91/2,00/1,93 (v3: 0,11); 355,8 (#62) 1,34 (v3: 0,21); 78,0 (#14) 3,19. 38 kesmenin hiçbirinde donuk uç yok. |
| Y4 kalanı (#93 ölüm döşeği, 541–546) | **KABUL** (tur 3'teki gibi) | #93 medyanı 0,40; itme ≈%0,4/sn. Ağır sahne; ölü kare yok. |
| Y11 / Y6 kalanı / E4 / motor önerisi 3 (seçici deklanşör) | **KAPANDI** | Yukarıdaki satırlar. |

**Y7 ayrıntısı:**
- **Florin yağmuru (389,6–389,8):** sikkeler 20 px/kare hızda. 3× büyütmede hareket yönünde yumuşamış kenarlar ve alt-kare izleri var (`coin_zoom_v31.jpg`); v3'te jilet gibi keskindiler.
- **CİOMPİ damgası:** yaklaşırken bulanık (236,15–236,23), çarpmada keskin (236,28) (`y7_events_v31.jpg`). FRANSIZCA damgası da yaklaşırken bulanık (41,88–41,92), 42,01'de keskin (`ghost_check_v31.jpg`).
- **Takvim yaprakları (30,4–30,8)** bulanık. "N GÜN" sayacı ise temiz, hayalet rakam yok (`calendar_counter_v31.jpg`; ENG-E'nin `t_nom` düzeltmesi tutuyor).
- **Doğrulamadıklarım:** uçan kitap (300,8) ve sadaka sikkeleri bu ölçekte küçük kaldı. Ajanların program ölçümüne güveniyorum (0 → 18/32).

**Y-N2 ayrıntısı** (`hands_v31.jpg`):
- **#62 kese:** el kesmeden ≈39 px/kare hızla geçip pürüzsüzce 6'ya yavaşlıyor. Sonraki el hareketi çan eğrisinde. v3'teki "27 → 4 px/kare, iki karede durma" yok. Bilek açısı 355,85 → 356,7 arasında değişiyor. Tüccarın kolu keseyle kadrajdan çıkıyor (359,6).
- **#81 mitra:** papalık eli kadraj dışından girip 76'dan 3 px/kare'ye pürüzsüzce yavaşlıyor ve oturuyor. Kamera +%6 itiyor ve kayıyor.
- **#83 kasa yakın planı (yeni):** el anahtarları kesmenin içinden ≈50 px/kare ile getiriyor ve yumuşakça 3'e iniyor; bırakma ve geri çekilme hareketi de çan eğrisinde.

## 4. v3.1 gerilemeleri (benim alanım)
**Engelleyici ya da önemli gerileme bulmadım.** Baktıklarım:

1. **Alt-kare örneklemede hayalet rakam/yazı:** yok.
   - FRANSIZCA damgası (N=7) sırasında "13 MADDE" sayacında yok (41,80–42,09).
   - #88'de 150.000 sayacı hızla sayarken yok (514,85–515,60, `counter88_v31.jpg`).
   - Takvim sayacında yok.
2. **Yeni çekimler:**
   - #83 kasa: −%21,9 çekme ve −347 px kayma.
   - #88 eğik defterler: +%15,5 ve −438 px.
   - #72 ve #85 masa çekimleri hareketli; ölü açılış yok (`c2_new_v31.jpg`).
3. **Kâğıt dokusu `BORDER_WRAP`:** kare farkı istatistiği v3 ile aynı. 110,0 sn'de ENG-E'nin andığı "içerik aynalaması" karede görünmüyor; simetrik asılı kumaşlar (`f110_v31.jpg`). Başkanla aynı sonuç.
4. **1737 belgesinin asemik yazısı (#7–#8):** belge yavaş itmede kararlı. #8 içi kare farkı 0,4–0,6, kaynama ya da titreşim yok.

**Not (P2'ye):**
- Yakın plan ellerin "eldiven" silueti SA1 E-1'in maddesi; hareket artık iyi.
- Ölüm döşeği çekimleri #89 ve #93'e mum titremesi ya da nefes gibi hafif bir ortam hareketi eklenebilir; P1 için şart değil.

## 5. En emin olmadığım nokta
- **Küçük nesnelerdeki deklanşör:** florin yağmuru, damgalar ve takvim yapraklarında bulanıklığı videoda gördüm. Uçan kitap ve sadaka sikkelerinde ise yalnız ajanların program ölçümüne dayanıyorum.
- **Algı:** büyütmede görülen alt-kare izlerinin (üç örnekli yumuşama) normal hızda "bulanık sikke" mi yoksa "çift kontur" mu okunduğunu oynatmadan bilemem. 180° pozlama ve ≈20 px/kare hızda beklenen görünüm bu.
