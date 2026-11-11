# Üslup kapısı, tur 5: yanan göl karesi (A04)

Tur 4: U-Sanat 8,2 · U-Gravur 8,0 · U-Teknik 8,55; üçünüz de "engelleyen bulgu yok" dediniz. Eşik 9 olduğu için kapı açılmadı; kalan somut bulgular düzeltildi. Aşağıdakiler **iddiadır**; kendiniz doğrulayın.

## Yaptığım değişiklikler (iddia)
1. **Alevde tek dil (U-Sanat 1, U-Gravur 1 ve 3):** her boyda kâğıt beyazı kütle + içinde dipten yukarı akan, sivrilen 2–3 mürekkep vuruşu (beyaz çizginin tersi). Yay taraması yalnız kadrajı kesen en yakın alevde (sağ alt). Taban şeridi her boyda taramasız ve dillerin arasını kapatıyor (maça biçimli siyah boşluk yok). Ufuk alevleri simetrik çift değil, düzensiz 5–6 dil. Sağ alt alev yeniden kuruldu.
2. **Bulut (U-Sanat 2, U-Gravur 2):** başlangıcı ya da kenar hilali öndeki yumrunun altında kalan vuruş çizilmiyor (yüzen kırıntı yok).
3. **Kaya (U-Gravur):** vuruş uzunlukları 16–190 px arasında düzensiz, daha seyrek.
4. **Huzme (U-Gravur, U-Sanat):** kaynakta kalın, uca doğru sivri.
5. **Göl (U-Teknik 1):** ufuk aralığı 9,5 px'ten başlıyor.
6. **Vuruş uçları (U-Teknik 2):** kanatta, figürde, bulutta ve kayada en ince yer 2 px; uçlar küt bitiyor.
7. **Zincir (U-Sanat 3):** geniş planda yalnız bilek halkası; zincir bilgisini plan listesindeki ayrı yakın plan (A04'te "zincirlerle" kelimesi) taşıyacak.
8. Benim ölçümüm: kare farkı 0,35/255; en kötü 64 px blok 8,3 (sağ alt alev); koyu (<60) %73,6; kâğıt (>200) %17,2.

## Dosyalar (bu klasörde)
`t0001.00.jpg` (ana kare), `t0001.03.jpg`, `t0003.00.jpg`, `t0006.00.jpg`, `yakin_z1.25.jpg`, `kucuk_640.png`, `kucuk_427.png`, `kucuk_246.png`, `telefon_427_x3.png`, `figur_pozlar.jpg`, `figur_gol_pozu.jpg`, `kanat_gol.jpg`. Kare üretmek: `cd milton && PAGE=uslup.html node shot.js <kendi klasörünüz> <t>`.

## İstenen rapor
`kurul/uslup_tur5/<KOD>.json`: `puan`, ölçüt puanları, `karar` (ONAY ≥ 9,0 ve hiçbir ölçüt < 7), tur 4 bulgularınızın durumu, kalan düzeltmeler (engelleyen / sonra düzeltilebilir), "en emin olmadığım nokta". Puanı dürüstçe verin: kapıyı açmak için yükseltmeyin; 9'un altındaysa 9'a ne kadar kaldığını ve hangi tek değişikliğin en çok puan getireceğini yazın. Başka dosyaya dokunmayın, commit yapmayın.
