# Y-Tipo düzeltme raporu (tur 1)

Kare yolları: önce `scratchpad/tipo_once/`, sonra `scratchpad/tipo_fix/`, `tipo_fix2/`, `tipo_s/`; geçiş taraması `tipo_gecis2/` (13 kart x 8 kare; katkı sayfaları `_P0xx.png`). Hepsi `/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/` altında. Çizime (figür, sahne) dokunulmadı; `lib/acts/*.js` için `node --check` temiz; `planlar_kaynak.py` çalıştırıldı (142 plan).

## Madde madde

1. **P031** `sav.js:571`: alıntı koyu bulutun içine, kâğıt rengi, iki satır (x 1330, y 250, 72 px); `Wd('D02','sen') - 1.0`'da belirir (4,7 sn görünür). Kare: `tipo_fix/t0319.30, t0321.00, t0322.90`.
2. **Geçişler.** Kök neden `film.js`'te: `chapterCard` ve `quote` geçiş alfasını (`drawOver`) *eziyor* (`ctx.globalAlpha = …` atıyor, çarpmıyor); `sav_kart` da öyleydi. Düzeltmeler (film.js'e dokunmadan):
   - `sav_kart` çarpma yapıyor (`sav.js`); P030 kartı 1,0 sn kaydı (`sav.js:370`).
   - P104 ALKIŞ (`mec.js:472`), P065 GÜNEŞE İTİRAF (`nif.js:516`), P095 YILANIN İÇİNDE (`adn.js:820`), P083 ADEN’DE (`adn.js:558`): kart lt − 1,0 (önceki yazı p = .5'te, yani lt .7'de söner; kart ≥ 0,3 sn sonra belirir). P040 (`gol.js:152`) ve P018 (`cen.js:74`, fade .8): lt − .7. P056 ve P008 zaten ≥ 1,2 sn gecikmeliydi. P119/P131 (`oku.js:270,272`): başlık yazısı `st.at + 1.2`.
   - **Yeni bulgu P055 → P056:** P055 alıntısı (quote) geçiş boyunca tam opak kalıp P056 kartı belirirken ekranda duruyordu, sonra aniden kesiliyordu. `mec.js:465` içinde vekil bağlamla yazı 0,6 sn'de söner.
   - Tarama: 13 kart geçişi (`tipo_gecis2/_P008…_P131.png`). Başka çakışma yok; P103'ün `Kazanmıştır.` yazısı (`txt`) alfayı çarptığı için zaten düzgün sönüyor.
3. **P001** `nif.js:470`: x 1480, y 108, sağ kenar ≈ 1780; **A01 ve G07'ye künye** "KAYIP CENNET · IV. 75" (40 px, quote künyesi: Cinzel, ls 3, bulutun içinde). **P137** `nif.js:825`: aynı yerleşim (1480, 108). **P072** `nif.js:610`: G07'de yazı zaten sol üstte (x 440; sağ taşma yok); tarama çizgilerinin üstündeki "…nnemim." okunmuyordu, `panel .9` + künye eklendi. P072'nin yeri P001/P137 ile aynı olamaz (G07 farklı kare: bulut solda). Kare: `tipo_s/t0005.60, t0735.20, t1450.60`.
4. **P055** `mec.js:465`: alt koyu kütle (y 836, 72 px, panel .85); figür/taht/sütundan uzak. **P109** `mec.js:401`: y 120, 72 px, panel .92; belirme `Wd('J07','kral') − 0,4` (≈ 3,5 sn görünür). Kare: `tipo_fix/t0568.00, t1116.50`.
5. **P050** `gol.js:297`: etiketler koyu gökte (x 1580, y 410/640), panel .85; ok çizgisi artık yazının sol ucundan çıkıyor (eskiden kodda öncelik hatası yüzünden yazının ortasına varıp yazıyı kesiyordu). **P058** `kap.js:142`: (760, 200), panel .9. **P059** `kap.js:159-161`: iki parça da panel .9, sol mızrak çizgisinin sağına kaydırıldı (x0 1120). Kare: `tipo_fix/t0503.30, t0602.20, t0613.90`.
6. **Yıl/yer:** `oda.js:845` `oda_yil` (sol kenar x 140, y 110, Cinzel 56, ls 6, panel .7); P011 "LONDRA, 1660" (`oda.js:615`) ve P118 "1674" (`oda.js:784`) aynı biçim/köşe. **P013 "1667" kaldırıldı** (`oda.js:686`; `planlar_kaynak.py` B05 yazısı boş). Kare: `tipo_fix/t0108.00, t0118.00, t1219.00`.
7. **Ölçek:** bütün `quote(...)` px ≥ 72 (adn 4, cen 1, gol 4, nif_soz varsayılanı + G14, oda 2); `gol.js:227` tekrar alıntı 66 px. P048 üç satırlı alıntı + ikinci alıntı karede kontrol edildi (çakışma yok). Kare: `tipo_fix/t0405.50, t0462.00, t0473.00, t0481.00, t0686.00, t0752.00, t0819.00, t0983.00`. P098 alıntısı (72 px) kanada taşıyordu: `adn.js:896` x 430, maxW 620 (iki satır, koyu kenar).
8. **P120** `kit.js:513`: "KAYIP CENNET · I. 26" (40 px, ls 3). Kare: `tipo_fix2/t1232.40`. **P140** `oda.js:842-843`: künye x 1530 → 1440 (sağ kenar 1880'e taşıyordu; şimdi ≈ 1725), alıntı da aynı eksene alındı.
9. **P121** `oku.js:331`: "WILLIAM BLAKE · 1790–93"; plaka 740 px'e genişletildi (x 440–1180; `oku.js:330`); `planlar_kaynak.py` güncel. Kare: `tipo_fix/t1252.00`.
10. **Alt bant:** P142 "ZAMAN KURYESİ" y 790 (alt kenar ≈ 815; ayraç çizgisi 735); P132 Cabanel künyesi y 808, 54 px (≈ 835); **P129 "Cromwell, 1657"**: zemin çizgisi (y 799) ile 840 arasına sığmadığı için yazı zemin çizgisinin ÜSTÜNE, figürler arasına alındı (960, 400; 68 px). Kare: `tipo_fix/t1340.00, t1372.00, t1531.00`, `tipo_fix2/t1340.00`.
11. **Tırnak/metin (P028, P089, P125):** ekran yazıları `planlar.json` ile aynı. Fark altyazı/anlatımla:
    - P028: ekranda tırnaklı "binlerce hainin arasında sadık kalan tek kişi"; anlatım ve altyazı tırnaksız, dolaylı aktarım ("Milton onu şöyle anlatır: …"). Tırnak kalıyor (kurul onaylı metin); karar başkanın.
    - P089: ekranda tırnaklı "zorbaların bahanesi: zorunluluk" (özet); anlatımda "zorbaların hep sığındığı bahaneyle, zorunlulukla" (uzun, tırnaklı cümlenin içinde). Ekran, sözün tam alıntısı değil özeti.
    - P125: ekranda tırnaklı "yükseldiği kadar alçalır"; anlatımda tırnaksız ("yükselmeye kalkan, yükseldiği kadar alçalır").
    - Yapılan: değişiklik yok. İstenirse P028/P125 tırnakları kaldırılabilir (yalnız `planlar.json` + kod; 1 satır).
12. **Apostrof:** düz ' → ’: "ADEN’DE BİR YABANCI" (`adn.js:558`), "Tanrı’nın" (`kit.js:512`), "Kayıp Cennet’e" (`oku.js:351`). (Başlık kartı ve levha dışında ekranda başka düz apostrof yok.)
13. **P142** `kit.js:548-552`: video kutusu tam 780×439 (x 150–930, y 232–671), abone dairesi çap 280 (merkez 1470, 452), aralarında 240 px, ikisi x 120–1800'de. Kare: `tipo_fix/t1531.00`.
14. **P117 YOK** `kit.js:493`: `kit_a(t, tY − .4, .5)`, `bulamayacak` başlarken (1212,48) tam yazılı. Kare: `tipo_fix/t1212.60, t1213.20`.

Ek: `cen_kart` sorusu 56 → 64 px, satır aralığı 76 (`cen.js:69`; P018 ve P083). Kare: `tipo_fix2/t0168.50, t0851.00`.

## Uygulanamayan / başkandan istek
- **`lib/film.js` (zorunlu değil ama kalıcı çözüm):** `quote()` içindeki `ctx.globalAlpha = …` (panel, satır ve künye) ve `chapterCard()` içindeki `ctx.globalAlpha = E.sine(a)` çarpmaya (`*=`) çevrilirse geçiş alfası (`drawOver`) çalışır; o zaman yukarıdaki lt kaymaları gereksiz (ama zararsız) kalır ve P055'teki vekil bağlam da kalkabilir. Şimdilik quote tabanlı bütün yazılar, ardından fade/black geçiş gelince tam opak kalıp geçiş sonunda aniden kesiliyor (P055 hariç tek tek düzeltilmedi; kart komşuluğunda başka örnek yok).
- Çizim değişikliği gerektiren madde yok. P028 yazısı (y 190, 72 px) sol üstte ışın çizgilerine denk geliyor (bu turun listesinde değil; ışıklı zeminde mürekkep rengi, okunuyor).
- P059'da sağ mızrak ucu etiketin hemen altında ince bir çizgi olarak kalıyor (panel .9 ile soluk).
