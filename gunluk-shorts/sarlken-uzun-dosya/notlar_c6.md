# notlar_c6 — Bölüm VI · Kral, Esir, Düello (c6)  ·  yazar: bölüm yazarı C

Dosyalar: `scenes_c6.py` (çekim listesi), `stage_c6.py` (özel çekim türleri + `c6_santangelo` sahnesi), `stage_c678.py` (c6/c7/c8 ortak yardımcılar: `W()` çapa, `ic()`, `chip()`, `arrow()`, `scrim()`, kaplama üreticileri `ov_*`, `c678_sahne`, `c678_medals`, `c678_cift`).
Sürüm: yeni (yamalı) anlatı metnine göre (c6s1 "en kalıcı düşmanlarından biri", c6s3 "ordusu bozguna uğradı; François esir düştü", c6s4 "aktarıldığına göre", c6s10 "Sıkça anlatıldığına göre … imparatorun TEYZESİ").
Son durum: 22 kendi çekimim + bölüm kartı, 119 sn; sahne-lab `field`, `siege`, oda-lab `tower`(hücre) bağlı; "[sahne: … henüz yok]" yok.

## (a) Çekim listesi özeti (22 çekim + bölüm kartı)
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | c678_medals | karl_fransuva | 6.0 | V. Karl ↔ I. François madalyaları (ilki ortada başlar, ikincisi gelince kayar), kılıç simgesi; François gelmeden zambak ışıması |
| 2 | map | fransa_kusatma | 10.7 | Fransa mavi; İspanya, Hollanda, Burgonya (Franche-Comté), Napoli sırayla yanar; dört yönden kuşatma okları |
| 3 | c678_sahne (field) | pavia | 8.2 | sisli ova, süvari bozgunu; "24 ŞUBAT 1525", PAVIA, BOZGUN damgası, François madalyası + ESİR damgası |
| 4 | c6_mektup | mektup | 12.9 | anneye mektup (tek okunur satır: aktarılan söz; gerisi karalama) + "AKTARILDIĞINA GÖRE"; sonra üstüne yapıştırılmış yeni kâğıt şerit: ünlü söz + SONRADAN YAYGINLAŞTI |
| 5 | c678_sahne (tower/cell) | madrid_hucre | 1.8 | Madrid hücresi (oda-lab) + MADRİD + ESİR |
| 6 | c6_antlasma | madrid_antlasma | 4.8 | François madalyası + MADRİD ANTLAŞMASI 1526: İtalya / Flandre iddiaları yazılır, üstü çizilir, mühür |
| 7 | c6_rehin | rehin | 1.8 | iki oğul siluet (genç + çocuk), parmaklıklar, aya doğru uzanan kol, REHİN damgası |
| 8 | c6_yirt | antlasma_yirt | 6.5 | belge yırtılır (çatlak, iki yarı ayrılır, gölge), GEÇERSİZ damgası |
| 9 | c678_sahne (siege) | roma_kusatma | 2.3 | Roma kuşatması, alacakaranlık, yangın 0.6, merdivenler, köz; "6 MAYIS 1527", ROMA |
| 10 | c6_maas | maas_yok | 2.1 | para yığını üstü çizilir: MAAŞ ALINAMADI; alttan asker siluetleri |
| 11 | c678_sahne (siege) | roma_giris | 1.9 | Roma'ya giriş: gece, yangın 1.0, top ateşi, merdivenler, köz |
| 12 | c678_sahne (c6_santangelo) | sant_angelo | 2.7 | yanan şehir (duman sütunları + çatı alevleri), Tiber, köprü + kıyı duvarı, Castel Sant'Angelo; Klemens VII madalyası |
| 13 | c6_muhafiz | muhafiz_189_147 | 5.3 | 189 minik muhafız (27×7); 147'si (21 sütun) soldan sağa devrilir; sayaç 189 → 147 / 189 |
| 14 | c6_emir | emir_yok | 2.3 | Karl madalyası + boş, mühürsüz emir kâğıdı + EMİR YOK |
| 15 | c6_aylar | papa_aylarca | 4.4 | papa madalyası + zincir; MAYIS→ARALIK 1527 şeridi dolar; AYLARCA; YAKLAŞIK |
| 16 | map | roma_ingiltere | 5.0 | Roma → Londra kesikli ok; SIKÇA ANLATILIR |
| 17 | c6_zincir | zincir_catherine_henry | 8.1 | ROMA 1527 → PAPA → ARAGONLU CATHERINE (İMPARATORUN TEYZESİ; BOŞANMA ONAYLANAMADI) → HENRY VIII (anahtar kırılır: ROMA'DAN KOPTU); SIKÇA ANLATILIR damgası |
| 18 | c6_duello | duello | 9.1 | iki madalya yüz yüze, "YALANCI!" balonları, kılıçlar çarpışır → kaybolur; DÜELLO YAPILMADI |
| 19 | map | cambrai_harita | 2.6 | Cambrai (Fransa ↔ Habsburg sınırı), 1529 |
| 20 | c6_hanimlar | hanimlar_baris | 8.5 | İKİ KADIN (siluet) → Louise de Savoie + Margareta madalyaları, defne, HANIMLAR BARIŞI |
| 21 | c6_fidye | iki_milyon_ecu | 5.5 | iki oğul siluet; yağan altın paralar; 2.000.000 ALTIN ECÜ |
| 22 | c6_savas | savas_kronoloji | 6.3 | kesintili kırmızı savaş dilimleri 1521–1558 (YAKLAŞIK); PAVIA/MADRİD/CAMBRAI/CRÉPY işaretleri; BARIŞ defnesi; 1558 · ÖMRÜNÜN SONU |

Siege ayarları: `city="roma"`; #9 `time="dusk", fire=0.6, ladders=True`; #11 `time="night", fire=1.0, ladders=True, cannon_fire=True`. Geçişler: savaşlarda `whip`, belge/madalya çekimlerinde `fade`/`dip`. Her çekimde kamera/itme hareketi (`pushy` sarmalayıcı veya kamera dizisi) var; hiçbir kare tamamen donuk kalmıyor.

## (b) Bilinen kusurlar
- c6_savas: savaş dilimleri (1521–26, 1526–29, 1536–38, 1542–44, 1551–58) genel bilgidir; araştırma dosyalarında yalnız PAVIA/MADRİD/CAMBRAI/CRÉPY/1551-59/1558 var → "YAKLAŞIK" damgalı, hafıza.
- Harita bölge sınırları yaklaşık (Burgonya = Franche-Comté çokgeni); "SINIRLAR YAKLAŞIKTIR" altyazısı haritanın kendi.
- c6_mektup/doc kâğıtlarında yalnız aktarılan söz okunur; geri kalan satırlar bilerek karalama (uydurma metin yok).
- Medal yüzleri stilize (madalya-lab); Catherine/Louise/Margareta yüzleri madalya-lab'a ait.
- Roma siege çekimleri kısa (2.3 / 1.9 sn): anlatı cümlesi üç çekime bölündü (kuşatma → maaş kartı → giriş); tempo bilinçli hızlı.
- İki oğul (rehin/fidye) siluetleri figür-lab'ın `page` + `child` türleri; çocuk figürü bir kolu havada (pencereye uzanan el gibi okunuyor), uzun saçlı/zırhlı değil — tarihi kostüm yaklaşık.
- `--check` ms/kare ölçümü duvar saatiyle yapılıyor; makine yükü (load avg 8–12 / 4 çekirdek) iken sınır çekimleri (özellikle geçiş penceresine düşen kısa çekimler) 450 ms'yi aşabiliyor. CPU süresiyle ölçtüğümde en yüksek 268 ms (c6_maas, whip penceresi); tipik 140–230 ms.

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
- Roma/Sant'Angelo sahnelerinde hiçbir sayı/isim uydurulmadı; ekran yazıları yalnız anlatıdan (tarih, ROMA, CASTEL SANT'ANGELO).

## (d) Ana ajandan istekler / uyarılar
1. `shots.py` genel şablonlarında **demet çapa (anchor tuple) çöküyor**: `k_medals` (`it.get("at") + 0.4`), `k_counter` (`at + 0.3`), `k_emblem` (`at + 0.3`), `k_quote` (`at + 0.15*i`) → `TypeError`. Öneri: `cx.amt(at, dur, off=sabit)`. Geçici çözüm: kendi modülümde çapa-güvenli kopyalar (`c678_medals`, `c678_cift`); `doc`'ta `at=` yalnız sayı verilebilir. (Diğer bölüm yazarları `(sid,"sözcük",off)` çapasıyla bu şablonları kullanırsa aynı çökmeyi görür.)
2. `theatre` önbellek anahtarı liste parametrelerini (`armies`, `ships`) dışlıyor; aynı skaler `p` ile farklı ordu/gemi listesi veren iki çekim aynı (önbellekteki) sahneyi gösterir. Çözüm: her çekime benzersiz skaler `tag="..."` verdim. Başka bölümler için de geçerli.
3. `preview_chapter.py --check` ms/kare'yi duvar saatiyle ölçüyor; ortak makine yoğunken sahte uyarı üretiyor. `time.process_time()` ile ölçmek daha güvenilir olur (isteğe bağlı).
4. Sahne-lab `siege` Güns/Viyana toplu isabetlerinde tek tük blok piksel kalıntıları (enkaz karesi) gösterebiliyor; hareket içinde fark edilmiyor, bilgi olarak.
