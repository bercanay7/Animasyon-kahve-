# Y-Tipo (tipografi tasarımcısı): ilk tam kurgu, tur 1

Merceğim: filmdeki tüm ekran yazıları (bölüm kartları, alıntılar ve künyeleri, etiketler, levha yazıları, kapanış soruları, bitiş ekranı). Baktığım malzeme: `ozet/son/sayfa01–08.jpg` (82 yazılı planın hepsi), tam boy kareler (`scratchpad/kurgu2`, `kurgu2b`), kendi aldığım kareler (`scratchpad/kurul_ytipo/`: t1055–t1057, t1218–t1220, t0310–t0322, t0152/158, t0460/470, t0568, t0735, t1237 ve birleşik sayfalar m1/m2/m3/ph), 427 px telefon küçültmesi (`kurul_ytipo/ph.png`) ve yazı kodu (`lib/film.js` 92–148, `lib/acts/*.js`, `kit.js`). Piksel boyları koddaki `px` değerlerinden alındı; küçüğe sınıflananlar karede de doğrulandı.

## 1. Puan ve karar

**Genel: 7,3 / 10. RED** (eşik 9,0; "okunurluk" ölçütü 7'nin altında olduğu için tek başına engel).

| Ölçüt (ağırlık) | Puan | Not |
|---|---|---|
| Okunurluk: telefon/TV, karşıtlık, boy (30%) | 6,3 | Alıntı kuralı (≥64) neredeyse tutuyor; künye (29 px) ve bölüm kartı sorusu (50–56 px) kural dışı; bir alıntı koyu zeminde mürekkep renginde |
| Yerleşim: güvenli alan, figür/odak, satır kırma (20%) | 7,0 | Büyük kısmı temiz; birkaç alıntı yüz/taht/çizgi taramasının üstünde; bir alıntı x>1800 |
| Tutarlılık: aynı tür yazı, aynı biçim (20%) | 7,2 | Levha yazıları ile bindirme yazıları iki ayrı ölçek; künye ve yıl etiketlerinin boyu ve yeri serbest |
| Yazım ve noktalama (10%) | 9,0 | Metin hatası yok; küçük noktalama inceliği var (apostrof, Cinzel küçük büyük harfler) |
| Zamanlama: belirme ve kalma süresi (10%) | 8,0 | Çoğu kelime başına 0,35 sn + 1 sn kuralını rahat geçiyor; iki alıntı kısa kalıyor; iki yerde iki yazı katmanı üst üste |
| Bitiş ekranı (10%) | 8,3 | Yer ayrımı makul; ince ayar önerisi var |

Kuralın ölçülü hâli: alıntılar için 64 px alt sınır `gol.js:227` (58 px) dışında tutuyor; etiket/künye 40 px sınırını `kaynak` satırları (px×0,42 ≈ 28–30 px) ve bölüm kartı soru satırları (50 px) bozuyor.

## 2. Engelleyici bulgular

1. **P031 (D02), alıntı koyu bulutun üstünde mürekkep renginde, okunmuyor.** `sav.js:570` `col: INK_CSS, panel: false`. Kare `kurul_ytipo/t0322.00.png`: "Sen de özgü…" açık zeminde görünüyor, geri kalanı siyah bulutun içinde kayboluyor. Üstelik yazı ancak ~319,7. sn'de belirip plan 323,37'de bitiyor: 9 kelimelik cümle için görünür süre 3,7 sn (gerekli ≈ 4,15 sn). Yayına bu hâliyle çıkılamaz; altyazı bandı cümleyi taşıyor ama ekran alıntısı bozuk görünür.
2. **Künye (`kaynak`) satırları telefonda ve TV'de okunmuyor.** `film.js:126` künye boyu `px × 0,42`: 66–70 px'lik alıntıda 28–30 px, %85 saydamlık; P046'da (`kurgu2/kare/t0470.20`, ph.png sağ üst) ve P047'de zeminin ışık taramasına karışıyor, 427 px'te hiç okunmuyor. Kullanıcının kuralı etiket ≥ 40 px. Dört yerde var: P014, P046, P047, P140. Kaynak gösterimi telif ve doğruluk açısından da önemli olduğu için engelleyici sayıyorum.

## 3. Sıralı düzeltme listesi

1. **P031 (305,72–323,37; alıntı belirişi ~319,7 sn).** Yer: x 190–1730, y 110. Sorun: mürekkep renkli alıntı siyah bulutun üstüne düşüyor; yarısı görünmez. Düzeltme: `col` PAPER, `panel .7`, ya da alıntıyı açık zemine (sol alt ışık huzmeleri, x 200–900, y 560–640) al; iki satıra böl ("Sen de özgür değilsin;" / "kendi kendinin tutsağısın."); `t0`'u `Wd('D02','sen')−0,6`'ya çek ki 4,3 sn görünsün. Kazanç: +0,5. Kare: `kurul_ytipo/t0322.00.png`.
2. **Tüm `kaynak` künyeleri (P014 2:15–2:30, P046 7:44–8:01, P047 7:53–8:02, P140 25:00–25:22).** Künye px×0,42 yerine sabit 40 px, tam opak, harf aralığı 3; alıntıyla arası ≥ 30 px. P046'da künyeyi alıntının altında ışıklı tarama yerine panelin içine al (`panel` künyeyi de kapsasın: şu an panel yalnız alıntı satırlarını ölçüyor, künye panel dışında kalıyor, `film.js:124–126`). Kazanç: +0,5.
3. **Bölüm kartı soruları (P040, P052/P056, P064/P065, P083, P095, P103/P104; 50 px, `cen.js` 56 px).** Bölüm başına merak sorusu kanalın tutma silahı ama 50 px'te telefonda 11 px'e iniyor (`kurul_ytipo/ph.png` sol üst ve orta üst). Düzeltme: soru 64 px'e (başlık 92 px kalsın), panel yarıçapını `y+30, 760×250` yerine `900×300`; P064/P065 ve P095'te soru satırının arkasında yatay tarama çizgileri okunurluğu bozuyor (kare `kurgu2/kare/t0963.67`, `kurgu2b/kare/t0655.68`): paneli `.82`'den `.9`'a çıkar. Kazanç: +0,5.
4. **P103 / P104 (1054,16–1062,2): iki yazı katmanı üst üste.** `kurul_ytipo/t1057.00.png`: "Kazanmıştır." (y 640) hâlâ görünürken ALKIŞ kartı (y 220) belirmeye başlıyor; ikisi aynı karede, biri sönük. Düzeltme: "Kazanmıştır."'ın sönme süresini ALKIŞ geçişinden 0,5 sn önce bitir ya da kartı `d` kadar geciktir. Ayrıca "Kazanmıştır." tek başına 3,7 sn'lik planda 84 px alıntı ama ekranda tek satır, ortada kaybolmuş; panelsiz siyah üzerinde kalıyor, iyi, ama üstündeki yağlı beyaz mercek şekli (ince elips, y 160) ne olduğu anlaşılmıyor. Kazanç: +0,3.
5. **P001 (0,9–6,24) "“Ben cehennemim.”", x 1560 merkez, 84 px.** Metin ~620 px geniş: sağ kenar ≈ 1870, güvenli alan 1800'ün 70 px dışında (TV taşması). Kapak vaadinin yazısı olduğu için en çok görülen kare. Düzeltme: x 1430'a çek (sol kenar ≈ 1120), ya da iki satıra böl. Aynı yerleşimli L07 "gururu" (x 1560) kısa olduğu için sorun değil; ayna çifti P001/P137 tutarlı kalsın. Kazanç: +0,3.
6. **P055 (559,59–572,38) "Diz çökmeyi reddeden melek…", (960,150).** Yazı Şeytan'ın başı ve taht sırtlığının üstünde; gri halka panel kafayı karartıyor (`kurul_ytipo/t0568.00.png`). Hem figür hem yazı zarar görüyor. Düzeltme: yazıyı y 80–100'e kaldır (güvenli alanın üstü, kafanın üstü) ya da sola x 500'e çek; panelsiz, PAPER renk, 70 px. Aynı sorun P109 (y 150, solundaki sütunu keser; `ozet/son/sayfa06` P109): alıntı sütun çizgisinden geçiyor, x 960 yerine ortalı ama sütun x 130–290 ve 1700 ile çakışıyor, "Önünde" ilk iki harfi sütun üstünde kalıyor. Kazanç: +0,3.
7. **P029 / P030 (285,7–305,7): "DOKUZ GÜN" kartı iki yüzlü diptik üstüne sızıyor.** `kurgu2b/kare/t0295.90.png`: başlık yarı saydam, "D O K U Z   G Ü N" sağ kolun ve kalabalığın üstünden geçiyor, kaldıran kolla çakışıyor; soru ("Asıl başkaldıran kim?") hâlâ ekranda. Geçiş çakışması ~1,4 sn. Düzeltme: kart `tr.end` kaydırmasını 0,6 sn'ye indir ya da diptiğin son 0,6 sn'sinde soruyu söndür (iki bölüm başlığı yazısı bir arada kalmasın). Kazanç: +0,3.
8. **P050 (489,68–503,7) "gurur · pişmanlık" ve P058/P059 "GÜNAH", "ÖLÜM · kendi oğlu".** Üçü de ince tarama zemini ve ışık huzmesi çizgileri üstünde; P050'de "PİŞMANLIK" yarısı kayıp (`ozet/son/sayfa03` P050, P058, P059: "GÜNAH" dalgalı taramada, "ÖLÜM · KENDİ OĞLU" mızrağın çapraz çizgisinden geçiyor). Düzeltme: `panel: .7` (şu an P058 `etiket` varsayılanı .7 ama p059 ikinci parça `panel: 0`!); P059 ikinci parçayı da panelli yap, yazıyı mızrak çizgisinden uzak (x 700 civarı) yerleştir; 56 px kalsın. Kazanç: +0,3.
9. **Yıl etiketlerinin yeri ve boyu serbest (P011 "LONDRA, 1660" 44 px sol üst (300,110); P013 "1667" 52 px sağ üst (1620,170); P118 "1674" 56 px, (700,360) ortada boş siyahta).** Üç aynı tür yazı üç farklı yer, üç boy. P118'de yıl, bir mumun solunda anlamsız bir yerde yüzüyor (`kurul_ytipo/t1219.50.png`). Düzeltme: üçünü 56 px, aynı üst-sol köşe (300,110) ve aynı biçim (Cinzel, ls 6); P118 için de (300,110). Kazanç: +0,3.
10. **Alıntı ölçeği iki ayrı dünyada.** Levhalarda (kit) 76–92 px ("Tanrı insanı…" 92 px, "Onu orada tutan neydi?" 80 px, "Asıl başkaldıran kim?" 84), bindirmelerde (quote) 64–72 px; P048'deki tekrar alıntı 58 px (`gol.js:227`). Aynı "tırnaklı Şeytan sözü" film boyunca bir büyüyüp bir küçülüyor. Düzeltme: bindirme alıntılarını 72 px'e, tekrar alıntıyı 66 px'e çıkar; üç satıra inen alıntılarda panel ölçülsün. Kazanç: +0,3.
11. **P109 kısa kalıyor.** "Önünde diz çökülen kral, şimdi karnının üstünde." (7 kelime) 3,3 sn görünür, gerekli ≈ 3,45 sn; P031 ile birlikte tek eksik. Düzeltme: `t0`'ı `Wd('J07','kral') − 0,4`'e çek. Kazanç: +0,1.
12. **P120 künyesi biçimi ayrık.** "(I. 26)" parantezli 44 px, öteki künyeler "KAYIP CENNET · I. 263" biçiminde. Düzeltme: "KAYIP CENNET · I. 26" olarak aynı biçim. Kazanç: +0,1.
13. **Apostrof ve küçük büyük harf.** "ADEN'DE BİR YABANCI", "Tanrı'nın", "Kayıp Cennet'e Önsöz": düz apostrof (') yerine ’. Cinzel'de küçük harf "küçük büyük harf" görünüyor ("Nifates Dağı", "ÖLÜM · kendi oğlu", "LUCIFER · ışık taşıyan"): bilinçliyse tutarlı; "İ/I" doğru çiziliyor (İRADE, İNTİKAM, BİR DAMLA YAŞ, YILANIN İÇİNDE doğru). Kazanç: +0,1.
14. **Bitiş ekranı (P142, 1515,43–1545,98).** `kurgu2/kare/t1530.71.png`: video kutusu x 150–930, y 220–685 (780×465, ≈ 16:9, YouTube video öğesi için uygun), abone dairesi x 1222–1578, y 270–630 (çap ≈ 356). İkisi çakışmıyor, güvenli alanda; "ZAMAN KURYESİ" y 830, altyazı bandının (y>880) üstünde. İnce ayar: YouTube'un video öğesi için 16:9 yerine kutuyu birebir 16:9 yap (780×439) ve daireyi 280 çapına küçült (YouTube abone öğesi küçük dairedir; 356 px kare kenarında gereksiz büyük çerçeve çizgisi kalır); sağda 1578–1880 arası boş (asimetri). 30,6 sn sabit kare, YouTube bitiş ekranı en çok 20 sn: son 20 sn'ye yerleştirin. Kazanç: +0,1.
15. **P117 "YOK" ve tek kelimelik dul.** "YOK" (kutu içinde tek kelime) belirişi `bulamayacak` ile (1212,38) ve plan 1214,56'da bitiyor: 1,2 sn tam görünür, tek kelime için yeterli ama vuruş anı "MERHAMET" yanında 5 sn geç kalıyor (`kurgu2b/t1212.95.png`'de yarı yazılmış "Y"). Düzeltme: sağ sütun cümlesini sol sütunla simetrik hızlandır ya da P118 karartmasını 0,4 sn geciktir. Kazanç: +0,1.

## 4. İyi olan ve korunması gereken

1. Yazı dili sistemi: başlıklar Cinzel büyük harf aralıklı, alıntılar Cormorant italik; koyu levhada kâğıt, açık levhada mürekkep rengi. Tek tek planlar iyi okunuyor (P006 başlık sayfası, P018, P026, P112, P119, P127, P131, P141).
2. Levha yazıları (kit.js) cömert boyda: 80–112 px, kâğıt zeminde mürekkep; telefonda rahat okunuyor.
3. Metin doğruluğu: planlar.json ile ekran yazısı, senaryo ve künye (I. 26, I. 254–255, I. 263, III. 41–42, III. 51–52) tutarlı; Türkçe büyük harf (İ, Ş, Ğ, Ü) doğru.
4. Bölüm kartı kalıbı (çizgi + başlık + soru) ve P018/P020 "IŞIK TAŞIYAN / LUCIFER · ışık taşıyan" çifti: iyi bir tekrar dili; P001 ↔ P137 ayna yerleşimi doğru.
5. Zamanlama: yazı çoğunlukla ilgili kelimeye bağlı belirip yeterince kalıyor (P098 12,8 sn, P087 7,9 sn, P055 5,9 sn görünür).

## 5. En emin olmadığım nokta

Cinzel'in küçük harfleri (Nifates Dağı, ÖLÜM · kendi oğlu, gurur · pişmanlık) bilinçli küçük büyük harf mi yoksa yazı tipi dönüşümü mü olduğunu bilmiyorum; ayrıca P050 etiketlerinin (ve P058/P059'un) tam göründüğü anı değil yalnız %90 karesini gördüm, orada "PİŞMANLIK"ın yarısı kayıp çıktı ama etiketin doğduğu andaki kontrastı ayrıca ölçmedim.
