# Mary Stuart ve I. Elizabeth: kurul kaydı

## Kurulsuz üretim (kullanıcının kararı, 18 Kasım 2026)
Kullanıcı: "Bu kurul olayını burada kullanmayalım. Sadece ihtiyaç duyduğun yerde Fable'ı bir danışman olarak kullanabilirsin." Bağımsız kurul toplanmıyor; kapılar başkan denetimiyle geçiyor, ≥9 eşiği bağımsız ölçülmüyor. Fable tek danışman olarak yalnız gerekli noktalarda: senaryo (kaynak/doğruluk + hassasiyet) ve paketleme.

| Kapı | Durum | Denetim |
|---|---|---|
| Talep kontrolü + paketleme taslağı | Kurulsuz | Başkan; otomatik tamamlama + Türkçe video izlenmeleri (`uretim_plani.md`) |
| Üslup | Kullanıcının kararı | İlk deneme (Milton gravürü) kullanıcı itirazıyla bırakıldı; `silent-film` + `archive-lighttable` örnekleri kullanıcıya gösterildi, onay alındı |
| Kaynaklar | Başkan | K01–K41 (birinci el metinler `kaynak/metin/`), Z01–Z10 (Zweig, çalışma alanındaki Almanca metinden) |
| Senaryo rev0 → rev1 | **Fable danışman** (tek tur) + başkan | Aşağıda |

## Senaryo: Fable denetimi (18 Kasım, rev0 üzerinde)
Puanlar: kaynak/doğruluk 6,5; hassasiyet 8; kanca/tutma 6,5; Türkçe/seslendirme 7,5. Altı engelleyici bulgu.
Başkan her iddiayı kaynakla sınadı:
- **M10 (engelleyici):** Zweig'in hükmü ters aktarılmış. Almanca metinde doğrulandı (8. bölüm: "Elisabeth, die Realistin, siegt in der Geschichte, Maria Stuart, die Romantikerin, in Dichtung und Legende"). Düzeltildi.
- **H07–H09:** Camden'e göre Mary haberci dönmeden geçti; "vaat etmişti" → "yardım sözü verecekti, ama Mary cevabı beklemedi".
- **G08:** "on bir ay sonra" (feragatten itibaren 9 ay) → "Adada on bir aya yakın kaldı".
- **E07:** kaçış iki gece sonra; düzeltildi.
- **A07:** "aynı adada" coğrafi hata; cümle "bir kez bile yüz yüze gelmedi" oldu.
- **Kanca:** A 102 → 74 kelime; ilk cümle tarihsiz ("Bir kraliçe idam edilmek üzere…"); kapak A'nın vaadi ~0:10'da.
- **Hassasiyet:** Bothwell bölümündeki "tutku mu, zorbalık mı?" oylaması kaldırıldı (tanık zorbalık yazıyor; bölüm sorusu "Bothwell'le neden evlendi?"); "şehidin rengi" anlatıcı hükmünden Mary'nin bakışına çevrildi; "hiç çocuğu olmadı / soyu bitti" → "varis bırakmadı / Tudor hanedanı sona erdi".
- Diğer 18 bulgu (F06 "sersemletti", M09 "birkaç metre" çıkarıldı, J04, L13 "bu taçtaki hakkı", B08 kararı II. Henri verdi, G09 anahtar rivayeti çıkarıldı, F03 yumuşatıldı, "elim olay", Zweig'e "romantik/gerçekçi" atfı, F09, Brantôme "saraylı", "beş saate yakın", Knox "sonradan yazacaktı", L09–L10 sıra, E10 "Melville'in duyduğuna göre", J10 "kopyanın üstüne", J01, "sayvan") ve Türkçe/okunuş düzeltmeleri (Size yalvarırım, Dudley'yi, Abbey'ye, Calais/Brantôme/Stuart/Fotheringhay/Paulet okunuşları, Türkçe büyük İ) uygulandı.
- **Reddedilen yok.** B bölümü önerilen ~120 yerine 148 kelimede kaldı (Brantôme'un "Elveda Fransa" anı korunsun diye; başkan kararı).
- Fable'ın önerisi: tam ikinci tur gerekmez; değişen cümlelerle tek gerileme kontrolü yeter. Başkan bu kontrolü kendisi yaptı (aşağıdaki sayım).

rev1: 172 cümle, 2.063 kelime, ~21,5 dk; tts 14.480 karakter.

## Üslup kapısı, kurgu ve ses (kurulsuz; başkan denetimi, 18 Kasım)
- **Üslup kapısı:** manzara (A03 Solway), orta plan (A01 gravür ve kırmızı), yakın plan (B09 Clouet), 26 sn hareketli açılış (`ornek/acilis_0-26_mix.mp4`). Bulgular ve uygulananlar: karanlık zeminlerdeki tarama "yağmur" gibi okunuyordu (tarama eşiği .42 → .70, yoğunluk .4); bulutlar boncuk dizisi (bulanık kütleler); kırmızı koyu kalıyordu (kırmızı, çizimin açılmış tonuyla çarpılıyor); gravürde kırmızı düz kesik gibiydi (koyuluk maskesi: yalnız koyu kumaş, yumuşak kenar).
- **Kurgu:** 220 plan, ortalama 5,7 sn. `tools/kontrol.js` denetimi: ara yazı kartları sürenin %17,2'si (sınır %20), kart ≤ 8 sn, ardışık aynı ölçek yalnız A05/A05b (bilerek: iki profil, aynı karede değil), eksik sözcük çapası yok. Kurgu özetleri: `tools/ozet.js`.
- **Hassasiyet bulguları (başkan, görüntüde):**
  - Dans sahnesinde havaya kalkmış düz kollar selama benzeyebilirdi → çiftler el ele.
  - Anka kuşu simetrik ve açık kanatlı çizilince amblem kartalına benziyordu → yandan, kıvrık kanatlı, alevden yükselen kuş.
  - **Finden gravürünün sol altındaki ek resim idam anını (balta, kütük) gösteriyor** → bu gravürün kullanıldığı her planda örtüldü (A01, L07b, L13, Shorts, kapak B kırpması). Gardiner 1790 baskısı (kesik baş) hiç kullanılmadı.
  - İdam salonu çiziminde kütük ve balta yok; ILN 1861 baskısı baltayı dışarıda bırakan kırpmayla.
- **Ses:** özgün piyano/armonyum eşliği ve efektler (numpy sentez), miks −14,2 LUFS, tepe −1,5 dBFS. L11 "Ve salon sustu" boyunca müzik yok. Kulakla son onay kullanıcıda.

## Paketleme: Fable danışman (18 Kasım)
Puanlar: başlık 7; kapak A 6,5; kapak B 7,5. Başkan her bulguyu kapak karelerinde doğruladı:
- **B, hassasiyet (engelleyici aday, kabul):** kırmızının içinde dikey koyu kıvrım çizgisi ve kitabın köşesinde kırmızı leke kan gibi okunuyordu (tam boy kırpmada doğrulandı) → kitap ve el kırmızıdan çıkarıldı, kırmızı daha düz ve yumuşak kenarlı. Aynı düzeltme filmdeki A01, L07b, L13 planlarına da uygulandı.
- **B (kabul):** üst beden soluk, "siyah elbise" okunmuyordu → gravür daha koyu (kontrast 1,45); baş kadraja girdi; "KIRMIZI" yazısına ince krem kontur (gri değerde kayboluyordu).
- **A (kabul):** taçlı dev siluet satranç taşı ya da kaide üstünde büst gibi okunuyordu → yerine I. Elizabeth'in gerçek madalya profili (16. yy, The Met CC0) gökte, sola, teknedeki Mary'ye bakıyor; Mary ve tekne büyütüldü (kırmızı etek, uzanan el), bir kürekçi ve direk çıkarıldı; film çiziği kapakta azaltıldı.
- **Başlık (kısmen kabul):** "I. Elizabeth" kapısı öne alındı ("… | I. Elizabeth ve Mary Stuart"). "Kalbini mi Dinlersin, Mantığını mı?" alınmadı: başlık filmin kendi sorusunu tekrar etmeli.
- **Kayda geçen uyarı:** iki kapak iki vaat, ama yalnız B aranan kelimeyi ("idam") taşıyor; B kazanırsa sebebin "kırmızı" mı "idam" mı olduğu ayrılamaz.
- Sonrası: odak ölçümü A 5 odak (1. odak Mary, %50/%62), B 4 odak (1. odak yazı); akış taklitlerinde ikisi de 168 px'te okunuyor (`kapak/test/`).

## Yayın öncesi metin denetimi (18 Kasım; dört bulucu ajan, başkan doğrulaması)
Kullanıcı ajanlara izin verdi, sonra yükü fazla bularak hafiflettirdi: dört bulucu (A–E, F–I, J–M, yayın metinleri) 448 ekran yazısı ve iddiayı birinci el dosyalarla karşılaştırdı ve 61 bulgu getirdi. Planlanan iki şüpheci aşaması ve görsel denetim (hassasiyet taraması ve sessiz okuma) durduruldu; şüpheci yerine başkan şüpheli satırları kaynak dosyalarda kendisi doğruladı (Labanoff Workington ve 8 Şubat mektupları, Palliser, Paulet, Strickland).
- **Engelleyici, uygulandı:** ekranda "özgün belge" gibi duran ama uydurma ya da harfiyen olmayan yabancı dilde satırlar:
  - F05 (Elizabeth'in mektubunun Fransızcası depoda yok) ve F16 (Casket mektupları) → okunmaz karalama + "canlandırma" künyesi;
  - L14 (kaynakta olmayan "foy catholique" satırı) → Labanoff'tan harfiyen;
  - K07 (iki cümleden birleştirilmiş İngilizce) → Paulet mektubundan harfiyen, alt çizgi doğru satırda.
- **Önemli, uygulandı:**
  - H13b, H15, L03, L20b → kaynakla harfiyen ("eschappée prisonière");
  - H08, J04, J05, J08a, J10, L02 → karalama ya da şifre ("copie déchiffrée" etiketi kalktı);
  - künyeler: Clouet'nin 1561 portresinden kopya, NGS; "(?)" tarihler; Huys'a atfedilir; Currier & Ives 1868–70; Camden'ın aktarımı; Mumby'nin İngilizce özeti; "canlandırma";
  - "Paulet'e"; A06 kaynak satırı "Zweig'ın anlattığı hikâye";
  - B02 "Solway Moss savaşı · 24 Kasım 1542"; I08 "1568–69"; I09 Bolton eklendi, Chartley kale değil;
  - I13 annenin sözü "git"; I11 ve M07 sayvanda anka yok; E08/G05b haziran-temmuzda kar yok; M06 "Mary'nin soyu" ve "bugünkü kraliyet ailesi";
  - Shorts'ta L15 çıkarıldı (L14 olmadan Mary'nin bakışı kaynaksız kalıyordu);
  - açıklamada "on sekizine üç gün kala dul", "neredeyse on dokuz yıl", alıntıların hangi baskıdan çevrildiği, "Zweig'a göre" çerçevesi, kaynakça künyeleri, sabit yorumda "Zweig'a göre".
- **Kayda geçen, sonra seslendirmeyle düzeltilen (aşağıdaki "Seslendirme yaması"):** F02 "10 Şubat gecesi" (patlama 10 Şubat sabaha karşı; F03 etiketi doğru); L17 "haykırdı" (kaynak "dedi"); L20 "başıma gelen" (kaynak "başa gelen"); M13 "bir imparator daha" (Mary gönüllü bırakmadı); M10 "kazandı" (Zweig "kazanır"). Bölüm adı "On Dokuz Yıl" yuvarlama olarak kaldı (18 yıl 9 ay; Mary'nin kendisi "yirmi yıla yakın" der). Bir sonraki seslendirmede bu kalıplara dikkat.
- **Başkanın bulduğu teknik hata:** mektup yazısı hizayı kendisi kurmuyordu; önceki planın "ortala" ayarı sızınca metin kadrajdan taşıyordu (işçiler arası belirlenimciliği de bozabilirdi) → çizim durumu her karede sıfırlanıyor.
- Bulguların tamamı: oturumun çalışma alanında (`bulgular.txt`); burada özet.

## Son render tam boy kare kontrolü (18 Kasım; başkan)
Usta kopyadan 13 plan tam boy çekildi (A01, B02, F05, H13b, H15, I11, J04, K07, L13, L14, L20b, M06, M07). Metin denetimi düzeltmelerinin hepsi kareye geçmiş.
- **Düzeltildi, M06:** soy çizgisi adların üstünden geçiyordu ("VI. ve I. James" içindeki "I." çizginin altında kalıyor, "ı. James" okunuyordu) → çizgi adların arasında kesik.
- **Düzeltildi, A01 / L07b / L13 ve kapak B:** kitap ve eli kırmızıdan çıkaran dikdörtgen, kırmızı eteğin içinde köşeleri yuvarlak gri bir kutu gibi okunuyordu ("yapıştırılmış kâğıt") → çıkarma alanı kitabın ve parmakların çevresine sıkı çizildi. Kırmızı kitabın kenarına kadar geliyor, elde ve kitapta kırmızı yok (Fable'ın kan bulgusu korunuyor). Kapak B yeniden üretildi; odak ölçümü: 1. odak yine "KIRMIZI" yazısı, ikinci tepe kitap ve el; test seti yenilendi.
- **Doğrulandı, değişmedi:** I11, I12 ve M07'de "En ma fin est mon commencement" (Mary'nin Tutbury sayvanı, White), I13'te "git" (annesinin ankası, Drummond): ikisi de kaynakla uyumlu. J04 ve L14'teki dikey ak çizgi FilmPost'un film çiziği; M06'daki küçük nokta karede yer değiştiren toz.
- Yeniden üretilen parçalar: 0, 42, 43, 44, 48, 49 (`ONLY=`).
- **Düzeltildi, Shorts:** filmin künyesinin sonu ("… The Met (CC0)") dikey kırpmanın sol kenarında kesik kalıyor ve Shorts'un kendi künyesiyle üst üste biniyordu → Shorts'ta filmin üst katmanı (künye, etiket) çizilmiyor (`window.SHORTS_UST_YOK`); film usta kopyası değişmedi. Shorts yeniden üretildi (25,1 sn, −14,0 LUFS).

## Seslendirme yaması (18 Kasım; kullanıcı: "Seslendirme yapabilirsin sıkıntılı gördüğün yerleri")
Metin denetiminde kayda geçen beş anlatım sapması yeniden seslendirildi (Emrullah, eleven_v4, aynı akış; 665 karakter × 2 çekim = 1.330 kredi):
| Cümle | Eski | Yeni | Kaynak |
|---|---|---|---|
| F02 | "10 Şubat 1567 gecesi" | "10 Şubat 1567, sabaha karşı" | patlama 10 Şubat gece ikide (K15) |
| L17 | "Protestan dekan haykırdı:" | "Protestan dekan şöyle dedi:" | Wynkfielde: "Then sayde Mr. Deane" |
| L20 | "başıma gelen o elim olay" | "başa gelen o elim olay" | "hath befallen" (K36) |
| M10 | "tarihte kazandı" | "tarihte kazanır" (ekrandaki kart da) | Zweig: "siegt" (Z08) |
| M13 | "bir imparator daha vardı" | "bir imparator vardı" | Mary tahtı zorla bıraktı (K18) |
- **Yöntem:** her cümle önünde bir bağlam cümlesiyle okutuldu (doğal tonlama), bağlam kesildi, yeni cümle eski klibin yerine konuşma başı aynı ana gelecek biçimde oturtuldu (`tools/yama_vo.py`). Filmin geri kalanında hiçbir cümle kaymadı; müzik, efekt, altyazı ve Shorts'un zamanı aynı.
- **Seçim (iki çekimden):** hız eskiyle ×1,00–1,05, tını farkı en küçük olan: F02-a, L17-a, L20-b, M10-a, M13-a (`vo/yama/analiz.json`).
- **F02:** yeni okuma 0,46 sn uzundu (virgülden sonra 0,51 sn duraklama) → duraklama 0,25 sn'ye kısaltıldı (sessizlikte kesim, hız değişmedi), cümle 0,21 sn erken başlıyor; F03'e 0,52 sn ara.
- **Düzey:** eski cümlenin düzeyine; L17'de eski okuma haykırıştı (komşularından 7,5 dB yüksek), komşularının 1 dB üstüne kondu (diğer cümlelerle aynı ilişki).
- **Kontrol:** değişen yalnız bu beş bölge, ek yerleri sessizlikte (tık yok); "havaya" (patlama sesi) cümle sonuna 0,80 sn (eskisi 0,82); müzik ve efekt yeni zaman çizelgesiyle yeniden üretildi, miks −14,20 LUFS / −1,50 dBFS; altyazı farkı yalnız bu beş cümlede. Parçalar 15, 16, 45, 46, 50, 51 yeniden render edildi.
- **Kulakla son onay kullanıcıda:** `vo/yama/karsilastirma_eski_yeni.mp3` (her cümle önce eski, sonra yeni, bağlamıyla).
- **Yamadan sonra kare kontrolünde (önceden var olan) kusur:** M10'da "Stefan Zweig" künyesi, kamera Elizabeth'ten Mary'ye kayarken önce "I. ELİZABETH", sonra "MARY STUART" mezar etiketinin üstüne biniyordu → etiket bloğu 60 px yukarı (y 700 → 640); 50. parça yeniden render edildi.

## Müzik düzeltmesi (19 Kasım 2026, yayından bir gün önce; başkan)
- **Bulgu (Dorian Gray üretiminde):** `audio/score.py`'deki piyano sentezinde çok alçak notalarda (MIDI < ~37) sönüm katsayısı negatife düşüyor, nota üstel olarak büyüyor; normalleştirme bütün müziği bu patlamaya göre kısıyor. Aynı kodla müzik yeniden üretilince 1.249 saniyenin yalnız ~14'ünde müzik duyuluyordu. Miks LUFS'u (−14,2) bunu göstermedi: anlatım ölçümü taşıyordu. **Teslim edilen film ve Shorts müziksizdi** (Shorts'un son kartı tamamen sessiz).
- **Düzeltme:** `dec = max(.3, .55 + .05*(m-48)) * (1 + k*.55)`. Müzik, efekt ve miks yeniden üretildi: müzik medyanı −36 dB, 1.249 saniyenin 1.167'sinde −60 dB üstü; miks −14,3 LUFS / −1,5 dBFS. Seslendirme ve zaman çizelgesi aynı (ipuçları commit'tekiyle birebir).
- **Teslim:** film baştan render edildi (görüntü aynı; konteyner yenilendiği için usta kopya yoktu), YouTube ve telefon kopyaları ile Shorts yeni sesle yeniden üretildi.
- **Ders:** her müzik üretiminden sonra saniye saniye düzey eğrisi basılır (medyan ve "−60 dB üstü saniye" sayısı). Ses kurulu da müziği ayrı dosyada ölçer, miksin içinde değil.
