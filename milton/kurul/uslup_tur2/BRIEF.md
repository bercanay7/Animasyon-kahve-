# Üslup kapısı, tur 2: yanan göl karesi (A02)

Tur 1 RED (6,05–6,3) sonrası yeniden kuruldu. Aşağıdakiler **iddiadır**; kareye bakıp kendiniz doğrulayın.

## Kullanıcının bağlayıcı isteği
"Çizim çok göz yormasın. Ucuz ve kalitesiz durmasın, olabildiğince profesyonel olsun."

## Yaptığım değişiklikler (iddia)
1. **Motor v2:** tarama artık ekran filtresi değil; her biçimin kendi tarama türü var (düz, yay, kavisli akış). Çizgi aralığı seyrek ve kalın (5,6–9 px).
2. **Kıl gibi çizgi yok:** en ince çizgi aralığın %10'u, en kalını %88'i; ötesi düz siyah. Çapraz tarama kapalı (küçük boyda benek yapıyordu).
3. **Kademeli çizgi uçları:** çizgiler kâğıda ve siyaha aynı hizada girmez; her çizginin eşiği ayrıdır ve ucu sivrilir. Ton geçişinde düz sınır ya da daire izi kalmamalı.
4. **Figür:** heykel mankeni bırakıldı. Oranlı iskeletten çizilen koyu siluet + ışık yönünde kenar ışığı; zırh ince açık çizgiyle (göğüs zırhı, kuşak, omuzluk). Çıplaklık çağrışımı olmamalı (kırmızı çizgi 6).
5. **Kanat:** üç kütle (sırt, örtü tüyleri, uçuş tüyleri), tüyler 2–4'lük kümeler; yanık kanatta eksik ve kırık tüyler, bir kanat sarkık (asimetri).
6. **Doğa:** bulut üç sert tonlu yumrular; alevler birbirine kaynayan diller, içi temiz kâğıt; kaya fasetli; göl tek yatay tarama + yansıma sütunları; zincir 34 px halka.
7. **Değer planı:** karenin ~%73'ü düz siyah, ~%18'i temiz kâğıt, ~%9'u taramalı ara ton. Tek odak: figürün arkasındaki ufuk parıltısı.
8. **Titreşim:** ardışık iki kare (t=1,000 ve 1,033) arasında ortalama fark 0,43/255; en kötü 64×64 blok 13,3 (alev). Tur 1'de en kötü blok 40'tı.

## Dosyalar (hepsi bu klasörde)
- `t0001.00.jpg` (ana kare, 1920×1080), `t0001.03.jpg` (bir sonraki kare), `t0003.00.jpg`, `t0006.00.jpg`
- `kucuk_640.jpg`, `kucuk_427.jpg`, `kucuk_246.jpg`, `kucuk_168.jpg`, `telefon_427_x3.jpg`
- `figur_pozlar.jpg`: siluet figürün beş pozu (ayakta, yürüyen, diz çökmüş, ışıklı başmelek, küçük boy)
- `kanat_parlak.jpg`, `kanat_yanik.jpg`, `kanat_gecis.jpg` (parlaktan yanığa üç ara durum), `kanat_yarasa.jpg`
- Tur 1 karesi ve Doré levhaları: `../uslup_tur1/` (`kare_t1.jpg`, `ref/`)
- Kod: `lib/gravur.js`, `lib/siluet.js`, `lib/kanat.js`, `lib/prim.js`, `lib/sahne/gol.js`. Kare üretmek isterseniz: `cd milton && PAGE=uslup.html node shot.js <klasör> <t>` (kendi klasörünüze; bu klasördeki dosyaların üzerine yazmayın).

## İstenen rapor
`kurul/uslup_tur2/<KOD>.json` (KOD: U-Sanat, U-Gravur ya da U-Teknik):
- `puan` (ağırlıklı, 10 üzerinden) ve ölçüt puanları; `karar`: ONAY (≥ 9,0 ve hiçbir ölçüt < 7) ya da RED
- tur 1 bulgularınızın her biri için: giderildi / kısmen / giderilmedi
- 1920×1080 koordinatlı, sıralı düzeltme listesi (her madde: ne, nerede, nasıl)
- "bu üslup 24 dakika boyunca göz yorar mı?" sorusuna açık cevap
- "en emin olmadığım nokta"
Geçici betiklerinizin adına kodunuzu ön ek yapın (ör. `U-Teknik_olc.py`), işiniz bitince silin. Başka dosyaya dokunmayın, commit yapmayın.
