# Orfeus: kapak sistemine uyan yeni kapak (27 Kasım 2026)

Video yayında: **Orfeus ve Evridiki: Ölüleri İkna Etti, Kendini Durduramadı** (4:48, 22 Ekim). Başlık değişmez.

## Ne
- `A.jpg`: yeni kapak, yazı **ÇIKIŞTA / KAYBETTİ**. "KAYBETTİ" Evridiki'nin solgun mavisinde (`#9ED8F2`), "ÇIKIŞTA" fildişi (`#F3EAD7`). Bebas Neue 300 px.
- `A_yazisiz.jpg`: aynı sahnenin yazısız hâli (test aracı yazıyı iki karenin farkından ölçer).
- `test/A_test.jpg`, `test/A_test.txt`: test seti (küçültmeler, gri değer, odak, mobil akış, TV, rozet).
- Çizim `../lib/kapak.js`, sayfa `../kapak_sistem.html`, çekim `node <mutlak>/orfeus/tools/kapak.js orfeus/kapak A '{}'` ve ayrı süreçle `... A_yazisiz '{"yazisiz":1}'`.
- Eski kapaklar (`../kapak_final_A_arkana_bakma.jpg`, `../kapak_c_son_adimda.jpg` …) yerinde duruyor; eski hat `../kapak.js` + `../shot.js` değişmedi.

## Neden
- `kanal/KAPAK_SISTEMI.md` eski kapaklar arasında "önce Orfeus" diyor. Kanalın en aykırı kapağıydı: doygun mavi-turuncu palet, büyük beyaz gözlü karikatür yüzler, sarı yazı, yazı sağda.
- Yeni kapak filmin kâğıt kesme üslubunda kaldı: köşeli mağara kayası, kâğıt katı gölgesi, kâğıt pullarına ayrılan Evridiki.
  - Yazı sol üstte.
  - Orfeus sağda koyu siluet. Yüzü ¾, başında defne tacı, elinde lir; göz küçük ve sıcak tonda.
  - Zemin bastırılmış lacivert.
  - Tek renkli nesne Evridiki'nin ışığı; vurgu kelimesi de o renkte.
  - Karenin en parlak yeri iki elin arası.
  - Sağ alt süre rozetinin altında yalnız koyu pelerin var.
- Yazı bir çelişki söylüyor: çıkış kurtuluştur, kaybın yeri değil. Neyi ve neden kaybettiğini kapak söylemiyor, cevabı başlık veriyor ("Kendini Durduramadı").
  - "ARKANA BAKMA!" bir uyarı kalıbıydı, çelişki değildi.
  - Kapak yazısı başlığın hiçbir sözcüğünü tekrar etmiyor.
- Doğruluk: "çıkışta" açısından `../paket2/KARAR.md`'deki "son adımda" ile aynı kaynaklara dayanıyor.
  - Vergilius, *Georgica* IV: *iam luce sub ipsa*, ışığın hemen altında.
  - Ovidius, *Metamorphoses* X: yeryüzünün kenarından uzak değillerdi.

## Vaadin filmde karşılanması
Depoda Orfeus senaryosu ya da altyazısı yok; açılışın ilk 5 saniyesi depodan doğrulanamadı (`KARAR.md`'de de açık nokta).
- Kapağın vaadi mitin doruğunda karşılanıyor: Orfeus çıkışın eşiğinde dönüp bakıyor, Evridiki geri çekiliyor.
- Yüklemeden önce kullanıcı filmin ilk 5 saniyesine bakmalı: çıkış ya da dönüp bakma anı orada görünüyor ya da söyleniyor mu? Görünmüyorsa kapak yine de değişebilir. Ama vaat ancak dorukta karşılanır; bu durum 48. saat okumasına not düşülür.

## Nasıl yüklenir
1. **Önce süren testin bitmesi beklenir.** 17 Kasım'da "ARKANA BAKMA!" ile "SON ADIMDA BAKTI" arasında "Test ve karşılaştır" sürüyordu; o gün kalan süre ≈11 gün 8 saatti, yani test ≈28 Kasım'da biter. Kural: testi süren kapağa test bitmeden dokunulmaz. Sonuç (izlenme süresi payları) `analiz/`'e yazılır.
2. Studio → Orfeus videosu → Ayrıntılar → Küçük resim → **Yükle** → `orfeus/kapak/A.jpg`. Tek kapak olarak yüklenir, A/B testi açılmaz. Başlık değişmez, böylece tek değişken kapak olur.
3. Değişiklik tarihi ve saati not edilir.

## Ölçüm
- Karşılaştırma değişiklikten önceki eşit dönemle yapılır: değişiklikten önceki 48 saat ve 7 gün ile sonraki 48 saat ve 7 gün.
- Bakılacaklar: gösterim, **TO**, ortalama izleme süresi, **gösterim başına izlenme süresi** (TO × ortalama izleme).
- Referans (17 Kasım, ömür boyu): TO %1,5, ortalama izlenme %48,7, 0:30'da %61,3.
- Eğri ~100–400 izleyicilik; ±3 puanın altındaki fark yok sayılır. Gösterim az olacağı için TO farkı ancak 7. günde anlamlı okunur.
- Okuma `analiz/` altına yazılır.
