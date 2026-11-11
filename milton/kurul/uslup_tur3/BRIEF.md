# Üslup kapısı, tur 3: yanan göl karesi (A04)

Tur 2: U-Sanat 7,15 · U-Gravur 6,85 · U-Teknik 8,05 (hepsi RED). Bulgularınızın hepsi kabul edildi; aşağıdakiler **iddiadır**, karelere bakıp kendiniz doğrulayın.

## Kullanıcının bağlayıcı isteği
"Çizim çok göz yormasın. Ucuz ve kalitesiz durmasın, olabildiğince profesyonel olsun."

## Yaptığım değişiklikler (iddia)
1. **Figür (yeniden yazıldı):** bütün beden tek kütle maskede birleşiyor; kenar ışığı ve "beyaz çizgi" parça başına değil bütün siluete bir kez uygulanıyor (eklem iç çizgisi yok). Kalın boyun, eğimli omuz, kas kavisli kol, büyük el; klasik profil; arkaya akan yumuşak saç kütlesi. Göğüste yay yok: koyu figürde yalnız yaka, kemer ve omuzluk kenarı. Yırtık pelerin. Göl pozu asimetrik değil ama iki kol da suda, zincirler ön kolun suya girdiği noktadan çıkıyor.
2. **Yönetmenlik kuralı:** Şeytan filmde çoğunlukla orta ve uzak planda, kanat ve pelerinle sarılı koyu siluet olarak kullanılacak (kodla çizimin zayıf yanı olan yakın beden ve yüz planlarından kaçınılacak).
3. **Bulut:** eş merkezli halka taraması yok. Yumru tek ton kütle; biçimi ışık yanında kenarı izleyen, uçları sivrilen 1–4 hilal veriyor ("beyaz çizgi").
4. **Kanat:** yanık kanat düz siyah kütle; ışık kenarında 3 seyrek beyaz çizgi; ayrık sivri uçuş tüyleri; kesintisiz ön kenar ışığı; halka tarama yok; kanat ucu suya giriyor.
5. **Çizgi aralığı:** gök 12, bulut 11, göl 12,5, kaya ve genel 9, tüy 9 px. Beyaz aralık en az 3 px, siyah çizgi en az 1,7 px. Çizgi uçları kademeli ve sivri.
6. **Yarık ve huzme:** keskin dar yırtık + dört kısa, sivrilen huzme (çapraz kurdele yok).
7. **Göl:** ufka yakın kuşak dışında düz siyah + yansıma tireleri. **Kaya:** koyu siluet + ışıklı sırt çizgisi. **Alev:** daha az ve daha büyük dil ("ot" görüntüsü yok); ufuk bandı alçaldı.
8. **Değer:** ufuk parıltısı genişletildi, vinyet azaltıldı. Koyu piksel oranı ve titreşim ölçümünü kendiniz yapın (benim ölçümüm: kare farkı ~0,4/255).
9. **Kamera:** motor artık gerçek kaydırma ve yaklaşmayı destekliyor; tarama çizgileri dünyaya bağlı (yaklaşınca kalınlaşır). `yakin_z1.5.jpg` aynı sahnenin 1,5 kat yakın hâli.

## Dosyalar (bu klasörde)
- `t0001.00.jpg` (ana kare, 1920×1080), `t0001.03.jpg` (sonraki kare), `t0003.00.jpg`, `t0006.00.jpg`, `yakin_z1.5.jpg`
- `kucuk_640.png`, `kucuk_427.png`, `kucuk_246.png`, `telefon_427_x3.png`
- `figur_pozlar.jpg`, `figur_gol_pozu.jpg`, `figur_lum.jpg` (ışık 1 → 0), `figur_hareket.jpg`
- `kanat_parlak.jpg`, `kanat_yanik.jpg`, `kanat_gecis.jpg`, `kanat_gol.jpg`
- `yazi_alinti.jpg`, `yazi_bolum_karti.jpg`: ekran yazısı denemeleri (Cinzel + Cormorant Garamond). Puanlamaya girmez; görüş yazabilirsiniz.
- `on_deneme_cennet.jpg`: **puanlamaya girmez.** Tur 2'deki "cennet ve Aden kâğıt ağırlıklı kurulsun" önerinize karşılık ilk eskiz: cehennem tarifinin tersi (hafif taralı açık gök üstünde kâğıt beyazı kütleler, gölge yanında mürekkep hilalleri). Açık figür ve saflar henüz ham; yalnız şu soruya cevap istiyorum: **bu tarif doğru yönde mi, ne değişmeli?**
- Önceki turlar: `../uslup_tur2/`, `../uslup_tur1/` (Doré levhaları `../uslup_tur1/ref/`).
- Kod: `lib/gravur.js`, `lib/siluet.js`, `lib/kanat.js`, `lib/prim.js`, `lib/sahne/gol.js`. Kare üretmek: `cd milton && PAGE=uslup.html node shot.js <kendi klasörünüz> <t>` (yakın plan: `EXTRA="z=1.5&cx=900&cy=640"`). Bu klasördeki dosyaların üzerine yazmayın.

## İstenen rapor
`kurul/uslup_tur3/<KOD>.json`: `puan` (ağırlıklı) ve ölçüt puanları; `karar` (ONAY: ≥ 9,0 ve hiçbir ölçüt < 7; değilse RED); tur 2 bulgularınızın her biri için giderildi / kısmen / giderilmedi; 1920×1080 koordinatlı sıralı düzeltme listesi; "24 dakika göz yorar mı?"; cennet eskizi için yön görüşü; "en emin olmadığım nokta". Geçici dosyalarınız kendi klasörünüzde, adında kodunuz olsun. Başka dosyaya dokunmayın, commit yapmayın.
