# Üslup kapısı, tur 4: yanan göl karesi (A04)

Tur 3: U-Sanat 7,85 · U-Gravur 7,4 · U-Teknik 8,55. Bulgularınız `KURUL.md` "Tur 3" başlığında karara bağlandı (biri gerekçesiyle reddedildi). Aşağıdakiler **iddiadır**; karelere bakıp kendiniz doğrulayın.

## Kullanıcının bağlayıcı isteği
"Çizim çok göz yormasın. Ucuz ve kalitesiz durmasın, olabildiğince profesyonel olsun."

## Yaptığım değişiklikler (iddia)
1. **Beyaz çizgi forma girdi (U-Gravur 2):** kenara paralel "eko" çizgileri kalktı. Bulutta tek kenar hilali + ışık yanından kütlenin içine giren, kıvrılan, uzunluğu ve aralığı düzensiz sivri vuruşlar; kayada üst kenardan inen vuruşlar; figürde ve kanatta aynı dil (gövdede kesit boyunca, uzuvlarda eksene çapraz, kanatta tüy yönünde).
2. **Kanatta gri yok (U-Gravur 1):** bütün çizgiler tam opak kâğıt ya da mürekkep; çizgi kalınlıkla söner; en kalın yeri 3–4 px. Çizgi yalnız ışığa bakan tüylerde.
3. **Omuz ve saç (U-Gravur 3, U-Sanat):** yaka çizgisi ve üçlü şerit kalktı, tek omuzluk çizgisi var; saç dış hattı tek yumuşak dalga + üç kısa beyaz tel; el yumruk olarak okunur.
4. **Alev (U-Sanat 1, U-Gravur 3):** küçük ve orta diller taramasız kâğıt beyazı, S kavisli, birbirine kaynar; uzak bant taramasız; su çizgisindeki dikey taralı şeritler (barkod) kalktı; sağ alttaki tek oval kırıntı kaldırıldı; alev hızı düşürüldü.
5. **Göl ve gök (U-Sanat 2, U-Gravur):** göl taraması perspektifli (ufukta 7,5 px, önde 12,5 px); ufuktan uzakta düz siyah; gökte taralı kuşak daraltıldı; figürün arkasındaki parıltının taramasız kâğıt çekirdeği büyütüldü.
6. **Yarık ve huzme (U-Sanat 3, U-Gravur):** yarıktan yelpaze gibi açılan altı ince, sivrilen huzme; en uzunları figüre ulaşır.
7. **Zincir:** kısa, bilekten suya dalar. **Kenar ışıkları** en az 3 px (U-Teknik 1).
8. **Reddedilen (U-Teknik 3):** "yaklaşmada ton beyaza kayıyor". Aynı dünya yamalarında ortalama parlaklık z 1,0 → 1,5: 67,4 → 64,3; 147,6 → 142,8; 26,4 → 27,0; 49,2 → 49,1 (fark vinyet, ±%3). Yine de kural: kamera yaklaşması 1,25 katı geçmez; daha yakın kadraj kesmeyle kurulur. `yakin_z1.25.jpg` bu sınırı gösterir.
9. Benim ölçümüm: kare farkı ~0,47/255; koyu piksel ~%73, kâğıt ~%23. Kendiniz ölçün.

## Dosyalar (bu klasörde)
`t0001.00.jpg` (ana kare), `t0001.03.jpg`, `t0003.00.jpg`, `t0006.00.jpg`, `yakin_z1.25.jpg`, `kucuk_640.png`, `kucuk_427.png`, `kucuk_246.png`, `telefon_427_x3.png`, `figur_pozlar.jpg`, `figur_gol_pozu.jpg`, `figur_lum.jpg`, `kanat_parlak.jpg`, `kanat_yanik.jpg`, `kanat_gol.jpg`. Önceki turlar: `../uslup_tur3/` vb. Kare üretmek: `cd milton && PAGE=uslup.html node shot.js <kendi klasörünüz> <t>`.

## Karar sorusu (lütfen açıkça cevaplayın)
Bu kapının amacı tek karede **üslubun dilini** onaylamaktır; sahne sahne incelik sonraki bölüm kurullarında yeniden denetlenecek. Puanınız 9'un altındaysa, **sahne üretimine başlamayı engelleyen** bulgularla (dilin kendisi yanlışsa) **sahne üretimi sırasında düzeltilebilecek** bulguları ayrı listeleyin.

## İstenen rapor
`kurul/uslup_tur4/<KOD>.json`: `puan`, ölçüt puanları, `karar` (ONAY ≥ 9,0 ve hiçbir ölçüt < 7), tur 3 bulgularınızın durumu, koordinatlı düzeltme listesi (engelleyen / sonra düzeltilebilir diye iki bölüm), "en emin olmadığım nokta". Başka dosyaya dokunmayın, commit yapmayın; geçici dosyalar kendi klasörünüzde.
