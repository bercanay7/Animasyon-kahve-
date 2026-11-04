# ROUND 1: Mobil okunabilirlik ve marka tasarımcısı (tasarim)

**Dossier:** DOSSIER-01-tenisci-spa-fiyat.md. **Addenda read:** yok (klasörde ADDENDUM-01* dosyası bulunamadı; `ls kurul/` ile bakıldı).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** (b) Düzeltmelerle gönder. Bugünkü PDF olduğu gibi gitmesin: "%30'a varan" rozeti ile en küçük fiyat etiketleri bu koltuğun iki kırmızı çizgisini de aşıyor. Aşağıdaki tasarım düzeltmeleri (fiyat yapısı aynı kalır) yapılır, iki telefonda test edilir, sonra gönderilir.
**Confidence:** high (ölçülerin hepsi dosyanın kendisinden ölçüldü). WhatsApp'ın önizleme davranışıyla ilgili kısım medium; bu kısım varsayım ve cihazda test edilmedi.

## 1. Position and why

1. **Tasarımın temeli sağlam, ama kırmızı çizgiler aşılıyor.** Marka dili siteyle tutarlı. Kontrast her yerde WCAG AA'yı geçiyor, en düşük oran 4,80:1. Fontlar gömülü, metin gerçek metin olarak duruyor, WhatsApp bağlantısı çalışıyor. "Ucuz kampanya" görünümü yok, fiyatlar 18,8 pt ile en okunur öğe. Buna karşın önemli bilgi taşıyan üç öğe 9 pt'nin altında kalıyor: rozetteki "'A VARAN İNDİRİM" 7,6 pt, paket kartlarındaki "10 SEANS / 20 SEANS" 7,9 pt, bölüm etiketleri "KİŞİ BAŞI", "%30 İNDİRİMLİ" ve "İKİ KİŞİ TOPLAM" 8,7 pt. Kartımdaki kırmızı çizgi tam olarak bu: "telefonda 9 pt altına düşen önemli bilgi". Olduğu gibi gönderime bu yüzden karşıyım.
2. **İki indirim oranı aynı anda öne çıkıyor ve büyük olan yanlış yerde.** Kapağın en büyük sayısı "%30" (84 px, telefonda 30 pt; H1 ile aynı boy). Altındaki ilk liste ise %20 indirimli. 11 fiyat kaleminin 7'si %20, yalnızca 4 paket %30. "%30" sözünü dürüst kılan "'a varan" ekiyse sayının yaklaşık dörtte biri boyunda (7,6 pt'ye karşı 30 pt). Üstelik satır kesmesi kesme işaretini satır başına atıyor ("%30" / "’A VARAN"), bu Türkçe dizgide hatalı. Bu, kartımdaki ikinci kırmızı çizgi: "çelişkili vurgu". Benim çözümüm fiyat yapısını değiştirmiyor, yalnızca vurgu yapısını fiyat yapısına uyduruyor: oran her bölümün kendi başlığına yazılır, kapakta tek bir oran sayısı büyütülmez.
3. **Hiyerarşi ters kurulmuş.** En büyük başlık, en az bilgi taşıyan "Spa fiyat listesi" (84 px). Mesajın asıl kendisi olan "TENİSÇİLERE ÖZEL" ise 27 px'te kalıyor; bu telefonda 9,75 pt eder, sınırın altıdır. Kullanıcının özellikle istediği seans başı fiyat ("Seansı 1.225 TL") da 9,75 pt'de, yani en çok bakılması istenen sayı 10 pt'nin altında.
4. **Telefonda ilk ekran iyi, ama sohbet önizlemesi zayıf olabilir.** Genişliğe sığdırıldığında (390 pt) ilk ekrana ana mesaj, iki oran ve tek seansların 5 fiyatının hepsi giriyor. Bu, dosyanın belirtmediği olumlu bir veri. Sohbet balonundaki yatay küçük resim ise büyük olasılıkla yalnızca logo ve havluyu gösteriyor; "tenisçi" kelimesi ya hiç girmiyor ya da kenarda kalıyor (simülasyon §3'te, varsayım). Grupta insanların dosyayı açıp açmayacağına bu küçük resme bakarak karar verdiğini varsayıyorum. Bu yüzden başlık fotoğrafın üstüne alınmalı.
5. **Bu koltuğun çıkarı ve kaybı.** Kazandığı: okunur, dürüst vurgulu ve spa kalitesinde bir liste. Kaybettiği: büyük "%30" rozetinin dikkat çekme gücü. Pazarlama tarafı buna itiraz edebilir. Ben bu takası bilerek kabul ediyorum: dikkat çeken ama aldatıyor gibi görünen bir rozet, hem grup yöneticisinin güvenini hem markanın görünüşünü bozar.
6. **Düzeltmeyi prototipte denedim.** Düzeltmeler sayfayı uzatmıyor, tersine kısaltıyor: 3.639'dan 3.525 CSS px'e iniyor. Önemli metin en az 30 px oluyor (390 pt'de 10,8 pt, 360 dp'de 10,0 pt). Ayrıntılar §6'da.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **E1'in hesabı doğru ama eksik ve iyimser.** Ölçek doğru (390/1080 = 0,361; dosyadaki 0,48 × 0,75 = 0,36 ile aynı). Eksikler şunlar:
  - (a) "TENİSÇİLERE ÖZEL" (27 px, 9,75 pt), "Seansı X TL" (27 px, 9,75 pt), "WhatsApp'tan yazın" (24 px, 8,7 pt) ve "TL" birimi (26 px, 9,4 pt) listede yok.
  - (b) Boyutları önemine göre ayırmıyor. Kırmızı çizgiyi aşan üç öğe (rozet eki, seans sayısı, bölüm etiketleri) ayrıca belirtilmemiş.
  - (c) Yalnızca 390 pt'lik iPhone'u hesaplıyor. 360 dp genişlikteki yaygın Android telefonlarda her şey %7,7 daha küçük görünür: "10 SEANS" 7,3 pt'ye, rozet eki 7,0 pt'ye iner.
  - (d) PDF görüntüleyicilerin kenar boşlukları hesaba katılmamış (varsayım).
- **E2 yalnızca kaydırma sayısını veriyor, ilk ekranda ne göründüğünü vermiyor.** Ölçtüm: ilk ekran (yaklaşık 660 pt görünür alan, yani sayfanın 0–1.830 CSS px'i) başlığı, iki oranı ve tek seansların 5 fiyatını kapsıyor; paket kartları ikinci ekranda başlıyor. Bu bulgu tasarımın lehine ve dosyada yok.
- **E3 (sohbet önizlemesi) doğru şekilde varsayım diye işaretlenmiş, ama sonucu hiç tartışılmamış.** Sayfanın en/boy oranı 1:3,37. Küçük resim üstten yatay bir şerit olarak kırpılırsa ilk yaklaşık 565 CSS px görünür; "TENİSÇİLERE ÖZEL" yazısı ise 677 px'te başlıyor.
- **README.md güncel değil ve PDF ile çelişiyor (dosyada geçmiyor).** `tenisci-spa-fiyat/README.md` hâlâ şunları söylüyor: "Paketler bilerek eklenmedi", "%20 rozeti", tablo yalnızca tek seanslar. Güncel PDF'te ise paketler ve "%30" rozeti var. Klasöre bakan bir ekip arkadaşı ya da ön büro yanlış teklifi aktarabilir. README ayrıca uzun `onizleme.jpg`'yi "PDF açmak istemeyenler için" gönderilecek bir dosya olarak tanımlıyor. Dosya bu biçimi hiç değerlendirmiyor (bkz. §4).
- **Soru eksik kurulmuş.** Seçenekler yalnızca içerik ve fiyat üzerine kurulu; biçim sabit kabul edilmiş (tek, uzun PDF). Oysa kartımın sorusu "görsel (JPG) versiyon da gerekli mi?" bir biçim seçeneği. Benim cevabım: uzun JPG bu haliyle gönderilmemeli. Görsel isteniyorsa ayrı bir 4:5 kart hazırlanmalı (§6).
- **F20 küçük bir düzeltme gerektiriyor.** Tenis kortu çizimi sayfanın "arka planında" değil, yalnızca koyu alt bölümde ve %22 opaklıkla duruyor. Rozetteki satır kesmesi de "%30" / "’A VARAN" / "İNDİRİM" şeklinde.
- **PDF metinlerinin kaynağa uygunluğu.** Açıklamaları sitenin `lib/rituals.ts` dosyasıyla tek tek karşılaştırdım. Beşi kısaltılmış ama sadık. Derin Doku'da ise PDF "güçlü baskı" diyor; site "Daha belirgin baskıyı tercih edenler için ... Baskı, tercihinize göre ayarlanır" diyor. Sitenin bu masaj için kullandığı etiket "GEVŞEME". "KORTTAN SONRA" etiketinin işletme kaynaklarında karşılığı yok (F18 kuralı). Üstelik 19 px, yani telefonda 6,9 pt; zaten okunmuyor.
- **F22'yi doğruladım.** 810 × 2730 pt, 263.989 bayt, 7 gömülü font alt kümesi. Dosyada olmayan bir ek: PDF etiketli değil (`Tagged: no`). Ekran okuyucu kullananlar için bu küçük bir eksik.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Önemli metinlerin telefondaki boyu (390 pt / 360 dp): rozet eki 7,6 / 7,0; "10 SEANS" 7,9 / 7,3; bölüm etiketleri 8,7 / 8,0; "TENİSÇİLERE ÖZEL" 9,75 / 9,0; "Seansı X TL" 9,75 / 9,0; paket notu 9,75 / 9,0; "KORTTAN SONRA" 6,9 / 6,3; fiyatlar 18,8 / 17,3 pt | fact (ölçüm) + estimate (ölçek) | Playwright ile `index.html` 1080 px'te açılıp her metin düğümünün hesaplanmış `font-size` değeri okundu; ölçek: px × 390/1080 ve px × 360/1080 |
| 11 fiyat kaleminin 7'si %20, 4'ü %30 indirimli; kapaktaki en büyük sayı "%30" (84 px), "’A VARAN" 21 px | fact | `index.html` satır 117-120, 137-200 |
| Bütün renk çiftleri kontrastta AA'yı geçiyor: en düşük 4,80:1 (amber/kum, "KORTTAN SONRA"), soluk metin/kâğıt 5,54:1, alt bilgi 8,06:1 | fact (hesap) | WCAG 2.x göreli parlaklık formülü, `:root` renkleri, python |
| Genişliğe sığdırılmış ilk ekranda başlık, iki oran ve 5 tek seans fiyatının hepsi görünüyor; paketler ikinci ekranda | estimate | `pdftoppm` ile PDF 390 pt × 3 genişlikte işlendi; görünür alan ≈ 660 pt kabul edildi (iPhone 844 pt eksi üst ve alt çubuk yaklaşık 180 pt: varsayım) |
| Sohbet küçük resmi yatay şerit (≈1,91:1) ise yalnızca logo, havlu ve rozetin yarısı görünür, "tenisçi" kelimesi görünmez; 4:3 ise "TENİSÇİLERE ÖZEL" kenarda kalır | estimate (simülasyon) + assumption (WhatsApp'ın kırpma oranı) | `onizleme.jpg`'nin üstünden 1,91:1, 4:3 ve 1:1 kırpmalar; çıktılar `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/thumb_191.png` ve `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/thumb_43.png` |
| Uzun JPG (2160 × 7278) WhatsApp'ta standart kalitede uzun kenar ≈1.600 px'e indirilirse genişlik 475 px olur; yakınlaştırınca okunur ama bulanıktır | estimate + assumption (1.600 px sınırını bildiğim davranış diye kabul ettim, doğrulamadım) | PIL ile yeniden boyutlandırma; çıktı `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/wa_1600_pack_zoom.png` |
| Önerilen düzeltmelerle sayfa 3.525 CSS px'e iniyor (−113 px); en küçük metin 26 px (yalnızca marka alt satırı ve web adresi/tarih); bütün fiyat etiketleri 30 px; üç bölüm etiketi de 30 px'te tek satıra sığıyor; ilk 565 px'te "Tenisçilere özel spa fiyatları" ve oran satırı görünüyor | fact (prototip ölçümü) | `index.html`'in kopyası `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/proto.html` olarak düzenlendi, Playwright ile işlendi; görüntü: `/tmp/claude-0/-home-user/d6383d34-f4c3-53e1-9fb3-44f29c9d2c31/scratchpad/tasarim/proto_full.png`. Asıl dosyalara dokunulmadı |
| README.md PDF ile çelişiyor ("Paketler bilerek eklenmedi", "%20 rozeti") | fact | `tenisci-spa-fiyat/README.md` |
| PDF'teki Derin Doku açıklaması ("güçlü baskı") sitedekinden ("Baskı, tercihinize göre ayarlanır") ayrılıyor; "KORTTAN SONRA" için işletme kaynağı yok | fact | `/home/user/navitas-topkapi/lib/rituals.ts` (id "deep", etiket "GEVŞEME") |
| WhatsApp bağlantısı hazır mesajıyla birlikte PDF'e gömülü | fact | `strings` ile PDF'te `/URI (https://wa.me/905330713373?text=...)` görüldü |
| Türk mevzuatında "...'a varan" ifadesinin puntosuna dair bir hüküm olabilir | assumption (doğrulanamadı) | Bir web araması ve bir PDF denedim; Ticaret Bakanlığı'nın yanıltıcı indirim reklamlarını denetlediğine dair haberler çıktı (ör. https://www.hurriyet.com.tr/ekonomi/yuzde-90-indirim-aldatmacasi-bitiyor-42006887, https://www.dunya.com/ekonomi/ticaret-bakanligindan-indirim-kampanyalarina-siki-denetim-milyonluk-ceza-kapida-haberi-832712), ama "varan" ifadesinin boyutunu düzenleyen bir hüküm metni bulamadım. Bu, böyle bir hüküm olmadığı anlamına gelmez; bir profesyonele sorulmalı |
| Tenisçiler listeyi sık sık kortta ya da dışarıda, güneş altında okur; bu durumda düşük boy ve orta kontrast daha çok zorlar | assumption | Hedef kitle kartından çıkarım; ölçülmedi |

## 4. Risks from this seat

- **(a) Olduğu gibi gönderilirse.**
  - Sessiz başarısızlık: okuyan "%30" görür, ilk listede %20 bulur ve "yem" hissine kapılır. Şikâyet etmez, yazmaz, sadece geçer. Ölçümde bu "lead yok" olarak görünür ve fiyata yorulur; tasarımdan kaynaklandığı kimsenin aklına gelmez.
  - Paket kartlarında aynı isim iki kez geçiyor ("İsveç paketi" / "İsveç paketi"); 10'lu ile 20'liyi ayıran tek şey 7,9 pt'lik etiket ve fiyat. Masada karışıklığa yol açabilir (varsayım).
  - Sohbet küçük resmi genel bir spa reklamı gibi görünürse dosya hiç açılmaz (varsayım).
- **(b) Düzeltmelerle gönderilirse.** Risk, yeniden üretimde yeni bir hata çıkması (bir fiyatın yanlış kopyalanması). Bu yüzden gönderimden önce 11 fiyat tek tek kontrol edilmeli. Rozet kalkınca ilk bakıştaki çekicilik biraz azalır; bunu kabul ediyorum.
- **(c) Fiyat yapısı değiştirilirse.** Oran tek bir sayıya inerse tek ve dürüst bir kapak sayısı mümkün olur; bu tasarım açısından daha kolay. Ama süre, kontenjan ya da doğrulama satırları eklenecekse sessiz risk şudur: bunlar alt bilgideki 22 px'lik (7,9 pt) "Kasım 2026" satırının yanına, ince yazı olarak sıkıştırılır. Koşullar ancak okunursa adil olur; yeri en az 30 px ve fiyatların hemen altı olmalı.
- **(d) Gönderilmez ya da ertelenirse.** Bu koltuk bir şey kaybetmez; marka zarar görmez. Kayıp satış ve pazarlama tarafındadır.
- **Biçim riski (her seçenekte).** README'nin önerdiği gibi 2160 × 7278 px'lik uzun JPG resim olarak gönderilirse sohbet balonunda bir parçası görünür ve sıkıştırılır (varsayım). Ayrıca gruptan aylar sonra iletilen bir listede tek tarih ibaresi 7,9 pt'lik "Kasım 2026" olur; eski fiyat güncelmiş gibi dolaşır.

## 5. The cheapest decisive step

**Adım (yaklaşık 15 dakika):** Bugünkü PDF ile prototipten üretilen PDF'i, iki telefonun bulunduğu özel bir test WhatsApp grubuna gönderin. Telefonlardan biri iPhone (390 pt), diğeri yaygın bir Android (360 dp) olsun. Her telefonda üç ekran görüntüsü alın: (1) sohbet balonundaki küçük resim, (2) dosyaya dokununca açılan ilk ekran, (3) WhatsApp düğmesine basınca hazır mesajın açılıp açılmadığı.

**Önceden kararlaştırılan sonuçlar:**
- Küçük resim iki telefonda da zaten "TENİSÇİLERE ÖZEL" yazısını gösteriyorsa ve iki görüntüleyici de genişliğe sığdırarak açıyorsa, "başlığı fotoğrafın üstüne al" düzeltmesinden vazgeçerim. Yalnızca boyut ve rozet düzeltmelerini isterim.
- Android görüntüleyici sayfayı bütün olarak sığdırıp açıyorsa (fiyatlar 9 pt'nin altına iner), pozisyonum şuna döner: birincil biçim PDF değil, 4:5'lik bir görsel kart olmalı; PDF ikincil kalır.
- Düzeltilmiş sürümde 360 dp telefonda en küçük önemli metin 10 pt'ye ulaşıyor ve ana mesaj ilk ekranda görünüyorsa onay veririm.
- Hiçbir cihaz testi bugünkü rozeti kabul edilebilir yapamaz: sayı ile ekin boyu arasındaki 4'e 1 oran dosyanın kendisinde var.

## 6. Conditions and red lines

**Desteklemem için gereken düzeltmeler** (`index.html` üzerinden; CSS px, sayfa genişliği 1080; prototipte denendi):
1. **Rozet kalksın.** Satır 117-120'deki `.badge` bloğu silinir. İşletme mutlaka rozet istiyorsa yüzde içermeyen "TENİSÇİ / FİYATI" yazılır, iki satır da 30 px.
2. **Başlık fotoğrafın üstüne taşınsın.** Sıra şöyle olur: logo → başlık → giriş metni → fotoğraf. `.title{padding-right:0}` yapılır. H1 metni "Tenisçilere özel<br>spa fiyatları" olur, boyu 80 px. Üst satır (eyebrow) tenis topu simgesi + "KASIM 2026" olur, 30 px. Bu tarih zaten PDF'te var, burada okunur hale gelir. `.hero .photo{height:340px;border-radius:476px 476px 28px 28px / 220px 220px 28px 28px}` (eski değerler 480 ve 300).
3. **Bölüm başlıkları oranı taşısın.** "Masaj ve hamam / KİŞİ BAŞI" yerine "Tek seanslar / %20 İNDİRİM · KİŞİ BAŞI". "%30 İNDİRİMLİ" yerine "%30 İNDİRİM". "İKİ KİŞİ TOPLAM" yerine "%20 İNDİRİM · İKİ KİŞİ TOPLAM". `.ghead span{font-size:30px;letter-spacing:.12em}`. Ölçüldü: üçü de tek satıra sığıyor.
4. **Paket kartları.** `.cnt` etiketleri silinir. Kart adları "10 seans İsveç", "20 seans İsveç", "10 seans Mix", "20 seans Mix" olur, 34 px. `.pack .unit{font-size:30px}`, yani seans başı fiyat 10,8 pt. `.pnote{font-size:30px}`, `.old{font-size:28px}`. İsteğe bağlı: eski fiyat paket kartlarında da yeni fiyatın üstünde dursun, tek seans satırlarıyla aynı düzende.
5. **"KORTTAN SONRA" etiketi silinsin.** Derin Doku açıklaması sitedeki metne dönsün: "Boyun, omuz ve sırt; baskı tercihinize göre ayarlanır".
6. **Alt bölüm.** "RANDEVU" üst etiketi silinir; düğme kendini zaten anlatıyor. `.cta .t1{font-size:30px}`. `.brand .sub` ve `.legal` 22 px'ten 26 px'e çıkar.
7. **"Ön ödeme yok, randevuyla" maddesi.** Paketlerin hemen altındaki genel kutuda durduğu için görsel olarak paketleri de kapsıyor gibi okunuyor. İşletme paketlerin nasıl ödendiğini yazılı olarak verene kadar bu madde ya "Randevuyla" diye kısaltılır ya da işletmenin söylediği kapsamla yazılır. Kuralın içeriğine ben karar vermiyorum; yalnızca yerleşimin yanlış bir kapsam ima etmemesini istiyorum.
8. **Koşul satırları.** Başka koltukların istediği koşul satırları (geçerlilik tarihi, doğrulama, paket kuralları) işletme tarafından yazılırsa, onay işaretli kutunun ilk satırına ya da giriş metninin altına en az 30 px boyla konur, alt bilgiye konmaz. Tarih ya da kural uydurulmaz; boşluk bırakılır.
9. **README.** `README.md` PDF'e göre güncellenir ya da "güncel değil" diye işaretlenir.
10. **Görsel versiyon.** Görsel isteniyorsa uzun önizleme değil, ayrı bir 1080 × 1350 (4:5) kart hazırlanır. İçeriği: logo, H1 en az 80 px, oran satırı en az 48 px, 5 tek seansın yalnızca adı ve yeni fiyatı (en az 44 px), "Paket fiyatları PDF'te", WhatsApp numarası. Sohbet balonu yaklaşık 260 pt genişlikte görünür (varsayım); bu ölçek balonda yalnızca başlığın ve oran satırının okunmasını sağlar. wa.me bağlantısı görselde tıklanamaz, bu yüzden mesaj metnine konur.

**Kabul etmediğim şeyler:**
- Olduğu gibi gönderim.
- Niteleyici ekin ("'a varan", "başlayan") sayının yarısından küçük yazıldığı her rozet.
- Telefonda 9 pt'nin altında kalan koşul, tarih ya da ince yazı.
- 2160 × 7278 px'lik uzun JPG'nin birincil görsel olarak gönderilmesi.
- İşletmenin kaynaklarında karşılığı olmayan etiket ya da açıklama.

## 7. One line

Liste markaya yakışıyor ve ilk ekranı iyi, ama "%30'a varan" rozeti %20'lik listeyi bastırıyor ve önemli etiketler 7,6–8,7 pt'de kalıyor; rozeti kaldırıp oranları bölüm başlıklarına taşıyarak, bütün önemli metni en az 30 px yaparak ve iki telefonda test ederek düzeltilmiş halini gönderin.
