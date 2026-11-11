# Kapı 2b: ilk hareketli sahne (A04, yanan göl; film zamanı 20,2–35,8 sn)

Üslup karesi altı turda dil olarak onaylandı (U-Teknik 9,0; U-Sanat 8,35; U-Gravur 8,45; engelleyen bulgu yok). U-Sanat'ın önerisiyle kapının kalanı bu sahneye taşındı: aynı ölçütlerle, bu kez **hareket hâlinde** puanlayın. Aşağıdakiler iddiadır; kendiniz doğrulayın.

## Sahne
Anlatım (A04): "Hikâye, onun gözlerini açtığı yerde başlar: yanan bir gölün ortasında. Dokuz gün düşmüştü. Etrafında alev var ama ışık yok; yalnızca görünür bir karanlık. Kırılmaz zincirlerle bu göle bağlı."
- 21,2'ye kadar siyah; "gözlerini"de iki ince göz ışığı açılır, bir kez ağır kırpar.
- "yanan"da karanlıktan açılış; yakınlık 1,25'ten 1,0'a yavaş geri çekilme.
- "dokuz"da baş yarığa doğru kalkar; nefes; kanatta hafif salınım; alevler yavaş.
- "görünür"de sol üstte GÖRÜNÜR KARANLIK etiketi.
- "zincirlerle"de kesme: zincir yakın planı (ayrı ölçekte çizilmiş kadraj): suya inen ön kol, perçinli bilezik, suya dalan halkalar.

## Tur 6'dan sonra değişenler (iddia)
1. Oyma titremesi: bütün kenar ve çizgilerde dünyaya bağlı, zamanla değişmeyen 1,2 px'lik sapma (U-Gravur'un "9 için gereken son şey" dediği).
2. Kanadın önündeki "mum" (alev ucu) kaldırıldı; sağ alt alev çifti X yapmıyor; sağ bulut ucundaki spiral gitti; uzak alevlerde diken yok.
3. Açılışta görüntü siyahtan açılırken kısa bir an ara gri ton var (geçiş).
4. Benim ölçümüm (ardışık kare farkı, 0–255): 24,0 sn 1,4; 28,0 sn 4,8 (geri çekilme sürerken bütün çizgiler kamerayla kayıyor); 31,0 sn 3,0; 34,5 sn 1,6. Koyu piksel %72–77.

## Dosyalar (bu klasörde)
- `t0021.00.jpg` … `t0035.50.jpg`: 0,5 sn aralıkla 30 kare. `ozet.jpg`: hepsi tek sayfada.
- Ardışık kare çiftleri: `t0024.00`/`t0024.03`, `t0028.00`/`t0028.03`, `t0031.00`/`t0031.03`, `t0034.50`/`t0034.53`.
- Telefon boyu: `t0024.00_telefon_427_x3.png`, `t0030.00_…`, `t0034.50_…`.
- Kendi karelerinizi üretmek için: `cd /home/user/Animasyon-kahve-/milton && node shot.js <kendi klasörünüz> <t1> <t2> …` (film zamanı, saniye; PNG yazar).

## Sorular
1. Hareket anlamlı ve yeterli mi (az ama anlamlı ilkesi)? Fazla durağan ya da gereksiz hareketli yer var mı?
2. Geri çekilme sırasında çizgilerin kayması (kamera hareketi) rahatsız eder mi? (U-Teknik: 0,0333 sn aralıklı 10–15 kare üretip ölçün; öneri: yakınlaşma yerine yalnız yatay kaydırma mı kullanılmalı?)
3. Zincir yakın planı sahnenin diliyle tutarlı mı?
4. Etiket yazısı (GÖRÜNÜR KARANLIK) okunur ve yerinde mi?
5. Puan (aynı ölçütler) ve karar: ONAY ≥ 9,0 ve hiçbir ölçüt < 7. Kalan düzeltmeler: engelleyen / bölüm kurulunda düzeltilebilir.

## İstenen rapor
`kurul/uslup_a04/<KOD>.json`. Puanı dürüstçe verin. Başka dosyaya dokunmayın, commit yapmayın; geçici dosyalar kendi klasörünüzde.
