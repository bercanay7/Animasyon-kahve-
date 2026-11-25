# Üslup örnekleri: Fable'ın Stanford önerisi (25 Kasım 2026)

Kullanıcının 8 örneğinden (r1–r3, v0–v4; çözümlemeler `kanal/motorlar/`) Stanford'a ne alınır. Öneri, karar değil; başkan karede doğrular.

## Fable: Stanford'a örneklerden ne alınır

**Karar: üslup değişmez, yalnız kâğıt dünyası zenginleşir.** Altı kareyi aldım (P01, P02, P05, P10, P19, P20; `--rs=0.5`).

- **Monitör dünyası çalışıyor.** P01 koridor, P10 sıra ve P19 kapılar kuralı tek bakışta söylüyor. Buraya renk, kontur ya da panel girmez.
- **Zayıf halka kâğıt dünyası.**
  - P05 teyp: tek kalınlıkta ince siyah kontur, düz dolgu, çamur kahve zemin. Işık ve derinlik yok; monitör karelerinin yanında taslak gibi duruyor.
  - P20: kalın çerçeveli monitör ve boş bej alan. Karenin ortasında ne olduğu okunmuyor, "boş masa, kimse yok" fikri geçmiyor.
- Kullanıcının sevdiği örneklerin ortak yanı da burada eksik olan şey: ışığın düz bir biçim olması ve derinliğin katmanla kurulması.

### Alınacaklar

| Örnek | Öğe | Dünya | Dosya |
|---|---|---|---|
| r1 | Sert kenarlı tek ışık kaması, bir ton açık, sözcüğe bağlı kayar | gözlem odası (P05, P20) | `setler.js`: kâğıt setine `kama(x, y, açı, t)` çokgeni; `ekran.js` değişmez |
| r3 | Bitmişlikle derinlik: teyp tam tonlu, arka duvar ve kapı soluk kesik çizgi; alt köşede kontursuz koyu sandalye arkası | gözlem odası | `setler.js` (arka plan çizgi sınıfı), `figur.js` (kontursuz ön plan lekesi) |
| r2 | Değişken kalınlıklı kontur: gölge yanında kalın, ışık yanında kopuk | teyp, masa | `setler.js`: teybin `stroke` çağrıları genişlik zarflı yola çevrilir |
| v0 | Rölanti: makara, VU ibresi ve kayıt lambası 3 karede bir tutulur; doygun renk karenin ≤ %2'si | P05 | sahne dosyası; motor değişmez |
| v4 | En koyu biçim en parlak noktanın önünde: monitör parıltısı önünde koyu sandalye; koridorda uzak siluet bir kademe açık | P20, P01 | `setler.js`; `figur.js`'e derinlik tonu parametresi |
| v2 | Cilalı zeminde tek tonlu ters yansıma | koridor monitörü | `figur.js`: `scale(1,-1)` kopya |

Sıra: önce kama ve bitmişlik (P05 ile P20'yi kurtarır), sonra rölanti. Yansıma ve derinlik tonu takvim izin verirse yapılır.

### Alınmayacaklar

- **Çizilmiş yüz** (r1, r2, r3, v1): Eshelman, Jaffe ve Maslach yaşıyor; kişilik hakkı riski var ve kodun en zayıf yanı. r3'ün karikatür oranı ayrıca hakaret okunur.
- **Paletler** (kehribar, pastel, mor-sarı, haki): "renk yalnız kayıtta" kuralını bozar. Kama rengi kâğıdın kendi tonundan seçilir.
- **Panel bölmesi** (r1): çekici, ama `film.js` ortak dosya ve plan listesi yazılmış. Koyu zeminde açık dikey ve yatay aralık haç okunur. Bu videoya girmez, sonraki işe not edilir.
- **v1 ve v3'ün tamamı:** Duffy ayısı, BMW ızgarası ve belirli zırh tasarımı telifli. Tatil ve hız tonu konuya ters.
- **Basamaklı zaman ve sürtünme lekesi** (v3): denenmemiş, figürler yazılmış. Takvim dar: Narkissos 24 Kasım'da çıktı, sıra dolu.
- **Yeni motor:** Stanford için yazılmaz. Kullanıcının ayrı motor isteği ayrı iştir; en uygun adaylar yüzsüz olan v2 (düz vektör) ve v4 (ışık sisi).

### Tam boy karede yeniden bakılacaklar

- **P05 makaraları:** içlerindeki halka ve oval "hedef tahtası" kalıbına yakın; kontur düzeltilirken halka eklenmez.
- **P02 gözlüğü:** koyu silüette açık göz lekesi "bembeyaz göz" kuralının sınırında; parıltı küçük ve sıcak kalmalı.
- **P10:** sıra hâlinde dik figürler; yuvarlak tepe ve eşit aralık mezar taşı okumasına karşı taranır.
- **Kama:** figürün arkasına gelirse hale, çaprazı kutsal ışık okunabilir.

Kareler: `/tmp/claude-0/-home-user/fecdf416-d52a-5b19-840a-06fb4a2a3acf/scratchpad/fable_stanford/tum.png`. Hepsi iddiadır; başkan karede doğrular.