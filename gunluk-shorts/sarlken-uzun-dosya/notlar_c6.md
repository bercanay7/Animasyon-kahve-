# notlar_c6 — Bölüm VI · Kral, Esir, Düello (c6)  ·  yazar: bölüm yazarı C

Dosyalar: `scenes_c6.py` (çekim listesi), `stage_c6.py` (özel çekim türleri + `c6_santangelo` sahnesi), `stage_c678.py` (c6/c7/c8 ortak yardımcılar: `W()` çapa, `ic()`, `chip()`, `arrow()`, kaplama üreticileri, `c678_sahne`, `c678_medals`, `c678_cift`).
Sürüm: yeni (yamalı) anlatı metnine göre yazıldı (c6s1 "en kalıcı düşmanlarından biri", c6s3 "ordusu bozguna uğradı; François esir düştü", c6s4 "aktarıldığına göre", c6s10 "Sıkça anlatıldığına göre … imparatorun TEYZESİ").

## (a) Çekim listesi özeti (23 çekim + bölüm kartı, ≈ 119 sn)
| # | tür | etiket | ne gösteriyor |
|---|---|---|---|
| 1 | c678_medals | karl_fransuva | V. Karl ↔ I. François madalyaları (kılıç simgesi) |
| 2 | map | fransa_kusatma | Fransa mavi; İspanya, Hollanda, Burgonya (Franche-Comté), Napoli sırayla yanar; kuşatma okları |
| 3 | c678_sahne (field) | pavia | sisli ova, süvari bozgunu; "24 ŞUBAT 1525", PAVIA, BOZGUN damgası, François madalyası + ESİR |
| 4 | c6_mektup | mektup | anneye mektup (tek okunur satır: aktarılan söz; geri kalanı karalama) + "AKTARILDIĞINA GÖRE"; sonra üstüne yapıştırılmış yeni kâğıt şerit: ünlü söz + SONRADAN YAYGINLAŞTI |
| 5 | c678_sahne (tower/cell) | madrid_hucre | Madrid hücresi (oda-lab) + MADRİD + ESİR |
| 6 | c6_antlasma | madrid_antlasma | François madalyası + MADRİD ANTLAŞMASI 1526: İtalya / Flandre iddiaları yazılır, üstü çizilir, mühür |
| 7 | c6_rehin | rehin | iki oğul siluet, parmaklıklar, REHİN damgası |
| 8 | c6_yirt | antlasma_yirt | belge yırtılır (çatlak, iki yarı ayrılır), GEÇERSİZ damgası |
| 9 | c678_sahne (siege) | roma_kusatma | Roma, alacakaranlık, merdivenler; "6 MAYIS 1527" |
| 10 | c6_maas | maas_yok | para yığını üstü çizilir: MAAŞ ALINAMADI; alttan asker siluetleri |
| 11 | c678_sahne (siege) | roma_giris | Roma'ya giriş (gece, yangın) |
| 12 | c678_sahne (c6_santangelo) | sant_angelo | yanan şehir, Tiber, köprü, Castel Sant'Angelo silueti; Klemens VII madalyası |
| 13 | c6_muhafiz | muhafiz_189_147 | 189 minik muhafız (27×7); 147'si (21 sütun) soldan sağa devrilir; sayaç 189 → 147 / 189 |
| 14 | c6_emir | emir_yok | Karl madalyası + boş, mühürsüz emir kâğıdı + EMİR YOK |
| 15 | c6_aylar | papa_aylarca | papa madalyası + zincir; MAYIS→ARALIK 1527 şeridi dolar; AYLARCA; YAKLAŞIK |
| 16 | map | roma_ingiltere | Roma → Londra kesikli ok; SIKÇA ANLATILIR |
| 17 | c6_zincir | zincir_catherine_henry | ROMA 1527 → PAPA → ARAGONLU CATHERINE (İMPARATORUN TEYZESİ; BOŞANMA ONAYLANAMADI) → HENRY VIII (anahtar kırılır: ROMA'DAN KOPTU); SIKÇA ANLATILIR damgası |
| 18 | c6_duello | duello | iki madalya yüz yüze, "YALANCI!" balonları, kılıçlar çarpışır → kaybolur; DÜELLO YAPILMADI |
| 19 | map | cambrai_harita | Cambrai (Fransa ↔ Habsburg sınırı), 1529 |
| 20 | c6_hanimlar | hanimlar_baris | İKİ KADIN (siluet) → Louise de Savoie + Margareta madalyaları, defne, HANIMLAR BARIŞI |
| 21 | c6_fidye | iki_milyon_ecu | iki oğul siluet; yağan altın paralar; 2.000.000 ALTIN ECÜ |
| 22 | c6_savas | savas_kronoloji | kesintili kırmızı savaş dilimleri 1521–1558 (YAKLAŞIK); PAVIA/MADRİD/CAMBRAI/CRÉPY işaretleri; BARIŞ defnesi; 1558 · ÖMRÜNÜN SONU |

## (b) Bilinen kusurlar
- Roma siege çekimleri (#9, #11) sahne-lab `siege` ailesine bağlı (lab teslim edince yeniden ayarlanır; o zamana dek yer tutucu).
- c6_savas: savaş dilimleri (1521–26, 1526–29, 1536–38, 1542–44, 1551–58) genel bilgidir; araştırma dosyalarında yalnız PAVIA/MADRİD/CAMBRAI/CRÉPY/1551-59/1558 var → "YAKLAŞIK" damgalı.
- Harita bölge sınırları yaklaşık (Burgonya = Franche-Comté).
- c6_mektup/doc kâğıtlarında yalnız aktarılan söz okunur; geri kalan satırlar bilerek karalama (uydurma metin yok).
- Medal yüzleri stilize (madalya-lab); Catherine/Louise/Margareta yüzleri madalya-lab'a ait.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- I. François Fransa Kralı; Pavia 24 Şubat 1525 — CONFIRMED (A5 #1). BOZGUN: yeni anlatı (ordu esir değil, bozguna uğradı).
- Mektup "bana şeref ve canım kaldı" — NİTELİKLİ (A5 #2), "AKTARILDIĞINA GÖRE"; ünlü slogan — ANEKDOT, damga SONRADAN YAYGINLAŞTI.
- Madrid Antlaşması 1526; İtalya/Flandre'den vazgeçiş; iki oğul rehin; serbest kalınca reddetme (GEÇERSİZ) — CONFIRMED (A5 #3; 14 Ocak 1526).
- 6 Mayıs 1527 Roma; maaşsız asker — CONFIRMED (A5 #4). Papa = Klemens VII (A5 #5).
- 189 / 147 İsviçreli muhafız — CONFIRMED (A5 #5, Britannica). "İmparator emir vermemişti" — CONFIRMED (A5 #4).
- Papa "aylarca" elde: MAYIS→ARALIK 1527 şeridi — NİTELİKLİ (A5 #5: Haziran'da teslim, 6 Aralık 1527'ye dek) → YAKLAŞIK damgası.
- Roma Yağması → Catherine'in boşanması → Henry'nin kopuşu zinciri — HAFIZA H26 (arama özetiyle DOĞRULANDI); Catherine = imparatorun TEYZESİ (ekranda "İMPARATORUN TEYZESİ"; "hala" hiçbir yerde yazılmadı); damga SIKÇA ANLATILIR.
- 1528 karşılıklı "yalancı"/düello çağrısı, yapılmadı — NİTELİKLİ (A5 #8) → DÜELLO YAPILMADI.
- Cambrai 1529; Louise de Savoie (François'nın annesi), Margareta (Şarlken'in halası); "Hanımlar Barışı" — CONFIRMED (A5 #6). 2.000.000 altın ecü — CONFIRMED (A5 #6).
- Kronoloji: PAVIA 1525, MADRİD 1526, CAMBRAI 1529 (CONFIRMED), CRÉPY 1544 (NİTELİKLİ A5 #7), 1551–59 savaşı (H27, DOĞRULANDI), Şarlken'in ölümü 1558 (A5 #21). Savaş dilimleri: HAFIZA, YAKLAŞIK damgalı.

## (d) Ana ajandan istekler / uyarılar
1. `shots.py` genel şablonlarında **demet çapa (anchor tuple) çöküyor**: `k_medals` (`it.get("at") + 0.4`), `k_counter` (`at + 0.3`), `k_emblem` (`at + 0.3`), `k_quote` (`at + 0.15*i`) → `TypeError`. Öneri: `cx.amt(at, dur, off=sabit)`. Geçici çözüm: kendi modülümde çapa-güvenli kopyalar (`c678_medals`, `c678_cift`); `doc`'ta `at=` yalnız sayı (kayan) verilebilir.
2. `theatre` önbellek anahtarı liste parametrelerini dışlıyor (lab bunu bilinçli bırakmış); aynı sahneyi farklı `p` ile üst üste kullanan çekimler için ek `tag="..."` skaler anahtarı verdim.
3. Madrid hücresi (oda-lab `tower`/cell) kullanıldı; Roma çekimleri `siege` (sahne-lab) bekliyor.
