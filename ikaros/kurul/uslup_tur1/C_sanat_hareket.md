# Üslup kapısı tur 1: üye C (sanat yönetmeni + serigrafi geleneği + animasyon)

**Puan: 7/10. RED.**

Taban sağlam. Palet tarife sadık: şafak ve öğle paletleri tarifteki örneklerin aynısı. Gök bantları WPA dilinde, kayık baskı ve ışık hilali çalışıyor. Manzara ve orta plan afiş gibi duruyor, ucuz durmuyor. Sorun dört yerde: uçuşta kanadın "palmiye/eğrelti" okunması, kapak adayında yüzün kaybolması, uçuş sahnesinde derinlik olmaması ve tarife uymayan yeniden mürekkepleme. Hepsi bir turda düzelir.

## Düzeltmeler (önem sırasıyla)

1. **Uçuş: kanatlar hep yukarıda, bu yüzden yelken ya da palmiye gibi okunuyor** (x 600–1700, y 30–620).
   - Kodda `ang: -1.65 - fl*.55` ile kanat −2,2 ile −1,1 rad arasında gidip geliyor. Hiç yataya inmiyor, −1,1'de başın önüne geçiyor. 4,5 / 5,0 / 5,5. sn karelerinde Daidalos'un kanadı dikey bir eğrelti yaprağı gibi.
   - Çözüm: kanat arkaya ve yataya yakın dursun, çırpışta yatayın altına insin. Merkez yaklaşık −2,7, genlik yaklaşık ±0,75 rad (−2,0 ile −3,45 arası).
   - Kanat yukarı kalkarken toplansın (`span` ×0,8, `bend` −0,7), aşağı inerken tam açılsın. Aşağı vuruş döngünün yaklaşık %40'ı olsun (faz bükme). Gövde aşağı vuruşta yükselsin.
   - Uzak kanat V çizsin: `farDa` .25 → ~.6, açıklık ×0,8. Ritim "çırp-çırp-süzül" olsun; şimdiki eşit sinüs mekanik duruyor.

2. **Kanat biçimi: üçgen dişler testere ya da tarak gibi okunuyor** (`figur.js` `wing()`).
   - Birincil tüyler yuvarlak uçlu kapsül olsun, 5–6 tane, aralarında boşluk bulunsun ve uçta yelpaze gibi açılsın.
   - İkinciller sığ dalgalı (fistolu) kenar olsun, diş olmasın.
   - Bilek kırığı (`bend`) belirgin olsun: kuşu tanıtan şey bu "<" biçimi.
   - Fırsat: Ovidius tüyleri kır kavalı (*fistula*, VIII.189–192) gibi küçükten büyüğe dizer. C01'de anlatılan bu basamaklı dizilişi düz, paralel ikincillerle göstermek hem kuş gibi hem afiş gibi okunur.

3. **Yakın plan ve kapak: yüz gökte kayboluyor.**
   - Işık mürekkebi (#F2B27A) ile sky2 (#EE9A73) arasındaki kontrast 1,20; sky1 ile 1,24. 168 px'te yüz siliniyor, baş koyu bir yumru olarak "arkasını dönmüş" okunuyor (gri değerde de aynı).
   - Çözüm: yüz dolgusunu (`fig.face`) kaldır. Profil koyu kalsın (near, kontrast 5,4), ışık yalnız profilin iç kenarında hilal olsun (`litInk` bunu zaten veriyor).
   - Bulut (x 1280–1840, y 520–670) kâğıt rengiyle güneşle aynı parlaklıkta (L≈0,80) ve odağı bölüyor. Kaldır ya da sky1 ile bas, küçült, güneşten uzaklaştır.
   - Bu ikisi yapılırsa kapak olabilir. Tek siluet + tek güneş güçlü, sol üstte yazıya yer var.

4. **Uçuş sahnesinde paralaks yok, deniz kameraya kilitli.**
   - Uzak ada (`ridge(1200,2900)`) ekranda −38 px/sn kayıyor, bulutlar −28 px/sn: uzak olan yakından hızlı.
   - Parıltılar `x0 = cam.cx-1100`'e bağlı olduğu için ekranda sabit. 0. ve 3. sn karelerinde aynı yerdeler. Kaya kayarken su durmuş gibi.
   - Çözüm: her düzleme bir derinlik katsayısı ver (ada .15, bulut .35, uzak deniz .5, yakın bantlar ve kaya 1). Parıltıları dünyaya sabitle; satır satır yakına doğru hızlansınlar. Uçuşu en çok bu satacak.

5. **Yeniden mürekkepleme tarife uymuyor** (`film.js` `baski()`: `wipeRegion 'right'`, 0,7 sn).
   - Dikey ve yırtık kenarlı bir silme var, rakle görünmüyor. 8,2 sn karesinde "kâğıt yırtığı" ya da kurgu silmesi gibi okunuyor.
   - Tarife göre çapraz bir cephe olmalı, 0,35–0,45 sn sürmeli, `SK.squeegee` ile bıçak, mürekkep boncuğu ve sapın bir parçası görünmeli. Bir müzik vuruşuna denk gelmeli.

6. **Baba ile oğul siluetten ayrılmıyor.**
   - Uçuşta ikisi de kısa tunikli ve hemen hemen aynı boyda (46/42).
   - Orta planda Daidalos (h 50) İkaros'la (h 72) aynı zemin çizgisinde (y≈870) duruyor: geride değil, çocuk gibi okunuyor. Oğul baba gibi okunuyor.
   - Çözüm: Daidalos'a her planda `long: true` ver. Hafif kambur olsun (lean .2). Sakalı göğüs çizgisinin önüne taşsın, yoksa koyu gövdede eriyor. İkaros ~0,75 ölçekte olsun.
   - Orta planda Daidalos İkaros'un hemen yanına gelsin (x≈1000) ve kanadın kayışını bağlasın (C04). Şimdi boşluğa uzanan kol (x 660–740, y 560–660) "hata" gibi.

7. **Orta plan:**
   - İkaros'un uzak bacağı mid mürekkebiyle mid denizin üstünde (x 1070–1130, y 730–860), görünmüyor. Uzak uzvun mürekkebini alttaki mürekkebe göre seç.
   - Yerdeki ışık rengi elipsler (y 900–1030) konfeti ya da yaprak gibi okunuyor ve en doygun alt öğe olduğu için gözü çekiyor. 5–6 tane gerçek tüy biçimi (sap + bayrak) yap, mid mürekkebiyle bas, Daidalos'un ayak dibine koy.
   - Uzak sırtın dik sol kenarı (x 1240) İkaros'un bacağıyla teğet. Sırtı x 1350'den başlat ve ucunu suya doğru incelt.

8. **Manzara:**
   - Katlı kanatlar (x 700–800, y 410–520) 640 px'te küçük çam ağaçları gibi okunuyor. Damla biçimli, uçları dize inen düzgün bir katlı kanat yap. Ayrıca B03'te kanat henüz yok; hangi cümleye ait olduğuna bak.
   - Yalıyar %40'lık ölü bir koyu kütle. Tarifteki "ışıklı yüz"ü ver: güneşe bakan kenara (x 780–860) mid ya da far ile bir yüz, iki katman çizgisi oyması.
   - Güneş diskinin sky1'e kontrastı 1,21, neredeyse görünmüyor. Diskin dibindeki ilk halkayı sky2 ile bas.
   - Uzak sırtın dik sol kenarı (x 975) karton gibi; incelt.

9. **Deniz bantları jaluzi gibi** (manzara y 860–1080, uçuş y 920–1100). Dört eşit, tam genişlikte düz şerit var. 2–3 basamağa indir, `bandSteps` içindeki `curve`'ü kullan, uçları sivri kesik olsun.

10. **Balıkçı** (h 16): baş kaldırma 640 px'te görünmüyor; Bruegel kafiyesi buna dayanıyor. h 26 yap ve hareketi siluette değiştir: göz siper eli, olta ucunun düşmesi.

11. **Güneş ve figür:** 6. ve 12. sn'de kanatlar güneş diskinin üstüne biniyor; 15. sn'de bir baş halkaya yaklaşıyor (hale riski). Doruğa (E bölümü) kadar güneşi temiz tut: güneş x +120 olsun ya da figürler 60 px aşağı.

12. **Doku:** iğne delikleri koyu alanlarda çok sık ve eşit; yalıyarda yıldızlı gece gibi duruyor. Yoğunluğu yarıya indir, düşük frekanslı lekelenmeyi biraz artır, çekiş yönünde hafif sürütme izi ekle.

13. **Hareket notu (D01):** Daidalos "dönüp dönüp bakıyor". Uçuşta 3 sn'de bir başın arkaya dönmesi bu planın en anlamlı jesti olur; ayrı bir kare olarak sına.

## En emin olmadığım nokta
Kollar kanadın içindeyken saf yan görünüşte çırpan bir insan siluetinin telefon boyunda "kanatlı insan" diye okunup okunmayacağı. 1. madde düzeltilse de alttan ¾ bakış (iki kanat açık V, gövde kısalmış) daha iyi okunabilir. İki kareyle A/B önerilir. Ayrıca öğle güneşi (açık sarı halkalı kırmızı disk) bir an hedef tahtası gibi okunuyor. Öğlede diski boş kâğıt bırakıp halkaları kırmızı basmak ("kâğıt en parlak renktir") daha sıcak ve tehlikeli okunabilir; bu bir zevk kararı.
