# Üslup kapısı tur 1: D (hassasiyet/hukuk + erişilebilirlik)

**Puan: 8,0/10. Karar: RED** (düzeltmeler kolay, üslubun kendisi güvenli). **Veto: yok.**

## Bulgular
- **Telif/taklit:** Hiçbir karede yazı, logo, park adı ya da tanınır bir afiş kompozisyonu yok. Basamaklı gök ve halkalı güneş tarifin kendi dilbilgisi. Matisse'in *Icare*'ına benzerlik yok: koyu teal kullanılıyor, göğüste kırmızı nokta yok, mavi zemin üstünde sarı yıldız yok. `silk.js` yalnız motor; demo kompozisyonu yok, MIT metni yanında duruyor. Öneri: dosyanın başına tek satırlık bir telif ve lisans başlığı eklenmeli.
- **Kanatlı figür ve melek okuması:** Uçuş karelerinde iki kanat sırttan çıkıyor ve yukarı kalkık. Kollar görünmüyor, bu yüzden küçük boyda "melek" okunuyor. Bu saldırgan değil, ama yanlış okunuyor. Ayrıca E02 ("çıplak kollarını çırptı") kolların görünmesini gerektiriyor.
- **Öğle paleti (8–15 sn):** Kırmızı güneş diski (225,83,59) açık gök üstünde duruyor. Bu üç şey olarak okunabiliyor:
  - Japon bayrağı;
  - kırmızı daire ve kanatlı siluet yan yana gelince **THY logosu** (Türk izleyici için güçlü);
  - kırmızı merkezli **hedef tahtası**.

  Disk ile gök arasındaki karşıtlık 1,62:1; kırmızı-mavi eşit parlaklıkta titreşir. Fizik de yanlış: öğle güneşi beyazdır.
- **Uçurum:** Figürler aşağı değil ufka bakıyor, yani kırmızı çizgiye uygun. Ama kenara yakınlar: İkaros'un ayağı x≈795'te, kenar x≈858'de.
- **Çocuk bedeni ve giysisi:** Çıplaklık yok. Ama `orta`'daki bileğe kadar koyu giysi cüppe ya da çarşaf gibi okunabilir. Diz boyu, kemerli bir khiton hem Yunan'a uygun hem güvenli olur.
- **Okunurluk (ölçüldü):**
  - `yakin` (kapak adayı): yüz ile gök arasında **1,16:1**. 168 px'te yüz kayboluyor; sırtı dönük, kapüşonlu bir figür gibi okunuyor. Başın çevresindeki kayıt payı 12–15 px (tarif 1–3 px diyor), parlak bir hale gibi duruyor.
  - `orta`: çocuğun alt gövdesi ile deniz arasında 2,14:1. Daidalos'un teal arka bacağı teal denizin üstünde neredeyse görünmüyor.
  - `manzara` 640 px'te: sırttaki kanatlar çam ağacı gibi okunuyor.
  - Üst gövdelerde karşıtlık 8:1, iyi.

## Düzeltme listesi (1920×1080)
1. **ucus öğle, güneş (≈1410,210; r≈120):** Kırmızıdan beyaz-altın renge (#F6EBC8 civarı) çekilmeli. Kanatlı siluet hiçbir karede diskin önünden geçmemeli. *(Zorunlu.)*
2. **yakin:**
   - yüz bölgesi (850–945, 400–560): arka planla karşıtlık ≥3:1 olmalı. Örnek: yüz krem, başın arkasındaki gök şeridi pas tonu (#B5583F civarı); iki renk ≈3,7:1 verir;
   - başın çevresindeki kayıt payı (700–950, 375–400) ≤3 px'e inmeli;
   - kapakta ¾ yüz düşünülmeli.
3. **ucus kanatları (650–930, 30–480 ve 1180–1420, 120–500):**
   - omuz koşumu ya da kayışı ve üst kolda bağ görünmeli;
   - kol kanadın ön kenarı boyunca uzanmalı, el kanadın iskeletini kavramalı.
4. **orta:**
   - çocuk (600–700, 480–880): diz boyu kemerli tunik; denizin tarafında 2–3 px kâğıt payı;
   - Daidalos'un arka bacağı (1070–1130, 730–860): ya koyu mürekkeple ya da kâğıt payıyla ayrılmalı.
5. **manzara figürleri (700–800, 410–522):**
   - kenardan en az bir figür boyu (≈110 px) içeri alınmalı, başlar düz ya da yukarı baksın;
   - kanatlar küçükken açık siluetle çizilmeli ya da figürler ×1,5 büyütülmeli.
6. **İnce gök şeritleri (≤5 px; ör. manzarada y≈150, 200, 365):** ≥6 px olmalı ya da bunların üstünde zum/kaydırma yapılmamalı. Aksi hâlde 360p'de ve telefonda titrer.

## Sonraki sahneler için kırmızı çizgiler
Mevcut çizgiler geçerli (E05'te mezar yok, İkarya'da kilise yok). Bunlara ek:

1. **Düşüş (E01–E03):**
   - önden, kolları açık figür olmaz (haç okunur);
   - Matisse kombinasyonu olmaz: koyu siluet + göğüste kırmızı nokta + mavi zemin + saçılmış sarı yıldız ya da tüy. Tüyler krem rengi olsun;
   - çarpma ya da sıçrama gösterilmez;
   - mum ya da güneş parlamasında saniyede 3'ten fazla parlaklık değişimi olmaz (WCAG 2.3.1), özellikle kırmızıda.
2. **Güneşe yaklaşma:** Baş hiçbir karede güneş diskinin ya da halkaların merkezine girmez (hale okunur).
3. **Çocuk güvenliği:**
   - C08'deki öpüş alından olur, ağız yakın planı olmaz;
   - D02'de aşağıdan bakış tuniğin altına bakmaz, siluetler uzak kalır;
   - yayında "çocuklara özel değil" işaretlenir.
4. **D02–D03 "tanrı sandılar":** İnsanlar ayakta durup başını kaldırır.
   - diz çöken, secde eden, avuç açan ya da sıra hâlinde eğilen figür olmaz;
   - uçanların çevresine ışın ya da hale çizilmez.
5. **F05–F06 (Akropolis ve Athena):**
   - Athena önden, simetrik, kolları açık ve haleli bir kadın figürü olarak çizilmez (Meryem okunur). Miğferli ve mızraklı profil, baykuş ya da ışık kullanılır;
   - Parthenon serbesttir, kilise ya da cami silueti kullanılmaz.
6. **G01 ve G08:**
   - "üç uçuş" ortası yüksek, simetrik bir üçlü olarak dizilmez (Golgota okunur);
   - Bruegel sahnesi kendi üslubumuzla yeniden kurulur, tablonun fotoğrafı kullanılmaz;
   - suda kalan bacaklar küçük olur (≤%3 kare yüksekliği) ve tunik kenarı görünür;
   - Auden dizesi ekranda yer almaz.

## En emin olmadığım nokta
THY çağrışımının gücünden emin değilim. Logo stilize bir kaz, güneş ise bir güneş; hukuken risk düşük. Yine de izleyicinin "reklam mı?" diye düşünmesi ve hedef tahtası okuması, renk değişikliğinin neredeyse bedava olmasıyla birlikte ağır basıyor. Melek okumasını hassasiyet değil netlik sorunu saydım.
