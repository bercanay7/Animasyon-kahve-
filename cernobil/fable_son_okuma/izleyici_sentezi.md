# İzleyici sentezi ve doğrulama · Çernobil'in çayı

Fable'ın üç izleyicisi (A telefonda öğrenci, B 1986'yı Karadeniz'de yaşamış 60'lık, C hata arayan şüpheci) ilk teslimi zamanlı izledi (`izleyici_raporlari.md`). Kural: üçünün ortak düşüşü bulgudur, tek kişininki zevk. Her iddia başkan tarafından tam boy karede ve kodda doğrulandı; karar sütunu başkanındır.

## Ortak düşüşler (bulgu)
1. **Dönen rakamlar** (2:22 bekerel tanımı ve sekiz sayı karesi). `D.sayi` belirirken henüz oturmamış rakamları rastgele rakamla gösteriyordu; tanım karesinde "1 Bq = saniyede 9 bozunma" duruyordu. "Sayıyı sor" diyen bir videoda duraklatılan karede yanlış sayı.
2. **Kürekli kırmızı tümsek** (4:12–4:20, P41). Tek tümsek + dik saplanmış kürek: B'de taze mezar, A'da "bu ne"; "harmanlanmıştı" sözünü anlatmıyor.
3. **Künye bandı figürlerin üstünde** (11 plan).
4. **"7 AY ÖNCE"** (0:30, P07): Ocak 1987'ye göre 8 ay, Ağustos 1986'ya göre 3 ay. Nesnel hata.
5. **6:12–7:04 görsel durgunluk** (F bölümü: harita + boş form, kâğıtlar, yağmurda üç ev).

## Ortak yükselişler
- 0:00–0:28 kanca (kapak vaadi 6. sn, soru 20. sn, hikâye 0:30).
- 1:42–2:40 toplama → 5 kg/1 kg → 600'e karşı 15.000.
- 2:42–3:40 bakanın kendi sözleri, yorumsuz: doruk.
- 8:04–9:10 gömme, 8:38 kupürün geri dönüşü, köylülerin sorusu.
- 9:52 bardak zinciri ve 10:54 kapanış. C taraf ve abartı bulamadı; B'nin hassasiyeti korunmuş.

## Tek kişilik düşüşler (zevk)
- A: 1:08 yaprak yakın planı 10 sn; 9:20 boş arazi; 4:22–5:08 kurum kavgası (C'nin en sevdiği yer).
- B: 6:56 "Bir hikâye bir ölçümün yerini tutmaz." (C için videonun güvencesi.)
- B: 7:54 "altı depo" denirken üç depo; sızıntı lekeleri perde gibi.
- C: 0:54 "görünmez bulut" haritada çizili, açıklama "radyasyon hiç çizilmedi" diyor; 9:12 56 → 58 bin açıklamasız; canlandırma belgeler; 9:52 zincirde başbakan yok.

## Doğrulama ve karar (başkan)
| # | İddia | Doğrulama | Karar |
|---|---|---|---|
| 1 | Bekerel tanımında yanlış rakam; bütün sayılarda karıştırma | Kodda doğru (`lib/dekor.js` `sayi`: `p < 1` iken rastgele rakam). Planlarda P28'de "653", tanım karesinde yanlış sayı görüldü | **Düzeltildi.** Sayı artık soldan sağa daktilo gibi basılıyor; ara karede yanlış rakam yok. Birim sayı tamamlanınca çıkıyor |
| 2 | P41 mezar / kırmızı leke okuması | Tam boy karede doğru: tek tümsek, dik kürek, toprak zemin | **Düzeltildi.** Kürek kaldırıldı. Beton döşemede iki yığın ("YÜKSEK" koyu, "DÜŞÜK" açık); yapraklar yay çizerek ortadaki üçüncü yığına akıyor; "ort. 10.000" ortada. Sayı uydurulmadı |
| 3 | Künye çakışmaları | 26 künyeli planın hepsine bakıldı; 11'inde figür ya da nesne üstünde (P03, P15, P17, P41, P43, P61, P63, P66, P67, P70, P83) | **Düzeltildi.** Bu planlarda künye boş bölgeye taşındı (üst, orta ya da sağ alt). Belge karelerinde kâğıdın alt kenarına binenler okunur durumda; dokunulmadı |
| 4 | "7 AY ÖNCE" | Doğru; DOGRULAMA kararı (göreli süre yok) ile de çelişiyordu | **Düzeltildi:** "MAYIS 1986 · RİZE" |
| 5 | F bölümü durgun | Donma taraması 5 sn'yi aşan aralık bulmamıştı (kamera ve yağmur hareketi var); ama olay yok, doğru | **Kısmen.** P55'te köy halkaları birer birer beliriyor ("ölçülmedi" hareketle); P58'de ortadaki evin ışıklı penceresine yavaş yaklaşma. Plan bölünmedi |
| 6 | "OCAK 1987" bandı çatı çizgileri altında | Doğru | **Düzeltildi** (bütün tarih bantları): yazının arkası kâğıt rengi |
| 7 | TV'deki figürün kalçasında çıkıntı (1:36) | Tam boy karede kollar kalçada bükük; karın çıkıntısı gibi okunabilir | **Düzeltildi:** ön kol göğüs hizasında konuşma jesti, arka kol sarkık |
| 8 | "Altı depo" ama üç | Doğru | **Düzeltildi:** iki sıra, altı depo |
| 9 | 56 / 58 bin | Kaynakta ikisi de var (`kaynak/DOGRULAMA.md`) | **Düzeltildi** (kredi yok): 58.070 karesine küçük not "Ocak 1987 açıklaması: 56.000 ton"; açıklamaya miktarların kaynakta 56-58 bin arasında değiştiği satırı |
| 10 | Zincirde başbakan yok | Doğru (G02 "bakanın ve başbakanın sözüne") | **Düzeltildi:** "BAKAN" etiketi "HÜKÜMET" |
| 11 | Canlandırma belgeler | Doğru: kâğıtlar canlandırma, cümleler gazeteden | Açıklamaya not eklendi |
| 12 | "Radyasyon hiç çizilmedi" ↔ haritadaki bulut | Doğru: haritada bulutun yolu var | Açıklama cümlesi düzeltildi |
| 13 | 6:56 cümlesi (B) | Tek kişilik; cümle bilimsel çizginin kendisi | **Reddedildi** (değişmez). Sabit yorum yumuşatıldı: "Hatıranı yaz; hastalık konusunda videoda söylediğimizden fazlasını biz de bilmiyoruz" |
| 14 | 22 → ~24 bin (1990 → 1993) | Kaynakta iki ayrı tahmin; video ikisini de gazeteye bağlıyor | Bırakıldı; seslendirme yaması ister, kazancı küçük |
| 15 | AT sınırı süt ve mamada 370 | Doğru; video yalnız çaydan söz ediyor | Bırakıldı |
| 16 | Kapak: önce A | A vaadi 6. saniyede karşılanıyor, tek odak; B küçükte "kum torbası" | Kabul: test A ile başlar, B ikinci. B'nin yeniden çizimi (çay rengini büyütme) isteğe bağlı, sonraki işe not |

| 17 | (başkan, yeniden render sonrası) Donma | Rakamlar artık dönmediği için iki plan durgunlaştı: P23 (5 kg → 1 kg sonrası 6,9 sn), P83 (5,1 sn) | **Düzeltildi:** P23'te "1 kg" yığınına, P83'te bardağa ve sayıya yaklaşma; yalnız iki aralık yeniden üretilip filme eklendi |

Seslendirme yaması gereken bulgu yok; kredi harcanmadı.

## Yöntem notu
- Fable'a verilen: 2 sn arayla izleme sayfaları (`tools/izleme_dokumu.py`), her plandan bir kare, kapaklar, senaryo, kaynak dosyası. Ses verilmedi; ses bulgusu yok.
- Fable iki bulgunun nedenini kodda kendisi buldu (rakam karıştırma); doğru çıktı.
- Lale'deki gibi en değerli çıktı ortak düşüşler oldu; "tek kişinin düşüşü zevktir" kuralı B'nin 6:56 itirazını ve A'nın kurum bölümü sıkıntısını ayırmaya yaradı.
