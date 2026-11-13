# ROUND 1: Art director (artdir)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (klasörde ADDENDUM-01*.md araması yapıldı, dosya bulunamadı; bu "henüz yazılmamış" anlamına gelebilir, "hiç olmayacak" demek değildir).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** C (hibrit), ama "sabit baskın, değişken kısıtlı": sabit iskelet + en çok 3 adlı "cilt" + cilt-konu eşlemesi. Günlük serbest stil (A'nın stil kısmı) reddedilir; tam tek-stil kilidi (B) de veri gelene kadar ertelenir.
**Confidence:** medium (estetik yargı sağlam; "tanınırlık büyümeyi artırır" bağı kanıtsız, aşağıda açık).

## 1. Position and why

1. **Koltuğumun çıkarı:** Marka tanınırlığı ve estetik tutarlılık. 4 videoda 4 farklı stil (düz illüstrasyon, kara kalem, kâğıt kesme, blueprint) var; kanal sayfasına giren biri bunu "karışık deneme" olarak okur. Kırmızı çizgim tam olarak budur. (Varsayım: kanal sayfası ızgarasını görmedim.)
2. **Kullanıcının umuduyla çatışma:** "Love, Death & Robots" benzetmesi bu kanal için yanlış kurulmuş. O bir antoloji markasıdır; her bölümün çatısı sabittir, bölümler arası çeşitlilik bir adın altında satılır. Bizde 4 videolu, sıfır marka sermayeli bir kanal var. Çeşitliliği satmak için önce satılacak bir ad gerekir. (Yorum; kanıt yok.)
3. **Yine de tam kilit (B) değil:** Dossier'de stilin izlemeyi etkilediğine dair hiçbir ölçüm yok (F2). Kilitlediğim şey tek bir stil olursa, çeşitliliğin getirdiği olası kazancı kanıtsız atmış olurum. Hibrit geri alınabilir; B kısmen alınamaz (dossier da öyle diyor).
4. **Somut öneri (C'nin içeriği):**
   - **Sabit iskelet:** tek font ailesi (Türkçe İ/Ş/Ğ doğrulanmış), HUD sayacı aynı yer/boyut/renk, tek **imza vurgu rengi** (her cildin paletinde aynı hex), açılış kancası kartının yerleşimi, son kare = ilk kare, ses kimliği.
   - **Cilt envanteri = 3:** kara kalem, kâğıt kesme, blueprint. Düz illüstrasyon (Zanzibar) şimdilik emekli (o video seslendirmesiz de olduğu için zaten ayrı bir tür).
   - **Cilt-konu eşlemesi yazılı olsun:** blueprint = teknik/öngörü/mühendislik (Titanik), kara kalem = savaş/doğa/ağır (Emu), kâğıt kesme = tuhaf/halk/ritüel (Dans). Böylece çeşitlilik rastgele değil, okunabilir bir sistem olur: izleyici "bu cilt = bu tür hikâye" öğrenir.
   - Yeni cilt eklemek için: mevcut cilt en az 5 videoda kullanılmış olmalı.
5. **Maliyet dürüstlüğü:** Pipeline'ın itirazı haklı. F5'e göre her video yeni `scenes.py/ui.py/art.py/cues.py` gerektiriyor; yani hibritin tasarruf getirmesi için `ui.py` ve `cues.py` ortak motora çekilmeli ve cilt yalnız `art.py` + palet olmalı. Bunu yapmazsak "hibrit" günlük emeği azaltmaz, artırır.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **A "hiçbir şeyi değiştirme" değil.** A'nın tanımı "her videoda yeni stil" içeriyor; bu, B'ye göre en büyük sapmadır. Doğru adı "maksimum stil varyansı"dır. Sorunun kendisi (stil sabit mi, değişken mi) A'nın içine gömülmüş, yani seçenekler tek eksende değil üç eksende (stil, ses, konu) karışık paketlenmiş. Tutum: seçenekler faktörlere ayrılmalı.
- **F2 / E1-E3: karıştırıcı değişkenler.** Emu (1700) ve Dans (100) farklı stil, farklı konu, farklı kanca (F7), farklı yayın zamanı/ses sürümü (F3: Emu yeniden seslendirildi, hangi sürümün yayına gittiği belirsiz). n=2, ölçüm tarihi ve metrik belirsiz. "Stil işe yaradı/yaramadı" sonucu bu veriden **çıkmaz**; ben de "sabit stil kazanır" demek için bu veriyi kullanmıyorum. Dans ilk karede kanca kartı yoktu (F7, doğrulanmamış): en olası sebep görsel stilden önce bu.
- **Zanzibar seslendirmesiz** (F1); karşılaştırma tablosunda ses değişkeni olarak ayrı işaretlenmeli.
- **Görüntülenme tanımı belirsiz.** Dossier E7'yi "doğrulanmadı" diye bırakmış. Baktım (aşağıda): sayım tanımı değişmiş. Kullanıcının "100 izlendi" sayısının hangi tanıma göre olduğu bilinmeden videolar arası karşılaştırma zayıf.
- **Eksik seçenek:** "Cilt sayısını sınırla + stil-konu eşlemesi" yok; C bunu içeriyor ama dossier'in C tanımı ("illüstrasyon cildi" serbest) sınırsız.
- **HUD konumu denetlenmemiş.** Sayaç y≈260 / 1920 (üst ~%13). Shorts üst arayüz katmanının bu bölgeyle çakışıp çakışmadığı doğrulanmadı (doğrulanamadı, yokluğu kanıtlanmadı). Alt %25 kuralının kaynağı da dossier'de verilmemiş.
- Rakip varsayımı (E6) sistematik değil; "kodla çizim farklılaşmadır" iddiası ancak cilt tutarlıysa avantajdır, tutarsızsa amatörlük işaretidir.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Shorts azami süresi artık 3 dk; 40 sn bir kısıt değil bir tercih | fact | YouTube Help "Understand three-minute YouTube Shorts" (support.google.com/youtube/answer/15424877), WebSearch ile bulundu |
| Shorts görüntülenme tanımı değişti (oynatma başlangıcı sayılır; eski metrik "engaged views"); daha yeni bir blog yazısı 24 Ağustos 2026'dan itibaren ilk kareden sayımı anlatıyor, iki kaynak birbirinden farklı tanımlıyor | fact (kısmen çelişkili) | YouTube Help + blog.youtube "engaged views" yazısı; snippet düzeyinde okudum, tam sayfa doğrulanmadı |
| 4 videoda 4 farklı stil var | fact | Dossier F1 (kendim doğrulamadım) |
| Stil çeşitliliği tanımayı düşürür | assumption | E3 ile aynı, kanıt yok; ölçüm yok |
| Cilt başına ~3-4 video olacak 14 günde çeşitlilik-izlenme farkı istatistiksel olarak ayırt edilemez | estimate | Sayım: 14 video / 3-4 cilt; gürültü yüksek (yöntem: yalnızca örneklem büyüklüğü akıl yürütmesi, güç hesabı yapmadım) |
| Cilt değişiminin üretim maliyeti ortak motor yoksa artar | estimate | F5'ten çıkarım |

## 4. Risks from this seat

- **A:** Sessiz hata: kanal sayfasında dağınık ızgara; izleyici abone olurken "bir sonraki ne gelecek" göremez. Hiçbir metrik bunu tek başına göstermez.
- **B:** Tek stile erken kilitlenmek ve o stilin konuya uymaması (blueprint ile Dans Salgını). Sessiz risk: sanatçı yorgunluğu, şablon "kalıp" hissi.
- **C:** Cilt-konu eşlemesi uygulanmazsa "tutarlı çeşitlilik" gerçekte A'nın yeniden etiketlenmiş hali olur. Ayrıca iskelet çok kalın olursa (HUD+kanca kartı ekranı kaplarsa) illüstrasyon küçülür ve ayırt edici güç kaybolur.
- **Kendi kör noktam:** Estetik ölçüt kullanıyorum; izleyici verisi tersini söylerse bu raporu bırakırım. Üretim süresini hafife alma eğilimim pipeline raporuyla dengelenmeli.

## 5. The cheapest decisive step

Maliyet ~15 dakika, üretim yok: YouTube Studio'dan 4 videonun **yayın tarihi/saati, "izlenenlere karşı kaydıranlar", ortalama izlenme yüzdesi, trafik kaynağı** ekran görüntüleri + 4 videonun ilk karelerini yan yana kontak sayfası. Sonra 14 gün boyunca **kanca kuralını sabitle** (her videoda ilk karede kanca kartı) ve cildi cilt-konu eşlemesine göre sür.

**Önceden yazılmış karar kuralı (eşikler varsayımdır):**
- Eğer 4 videonun kaydıran oranı kancaya göre ayrışıyorsa (kancalı olanlar iyi, Dans kötü) ve stile göre ayrışmıyorsa: stil davası ikincil kalır, hibriti hafifletirim (cilt sayısı serbest, iskelet yalnız HUD+font+renk).
- Eğer 14 günde, kanca kuralı sabitken, bir cildin ortanca "izlenenlere karşı kaydıran" oranı diğerlerinden >=10 puan iyiyse (cilt başına >=4 video ve konu türü aynı): o cilde yaklaşır, tek cilde (B) geçişi savunurum.
- Eğer çeşitli ciltli videolar, aynı kancayla, tutarlı biçimde tek cildi geçiyorsa: art director olarak çeşitlilik lehine pozisyonumu bırakırım.
- 14 günde fark yoksa (beklenen sonuç): iskeletin kalıcı, cilt sayısının 3'te kalmasını savunurum; stil kanıtı gelmediği için "tanınırlık" ucuz sigorta olarak yapılır.

## 6. Conditions and red lines

- Kırmızı çizgi: kanal sayfasında 4+ birbirinden alakasız stil; günlük yeni stil icadı; okunmayan küçük yazı için stil ödünü (renktipo'ya katılırım: >=40 px).
- Şart: `ui.py` ve `cues.py` ortak motora çekilmeden üçüncü cilde geçilmez; yeni cilt = yalnız palet + `art.py`.
- Şart: yeni cilt maliyet tavanı (varsayım): 90 dakikayı aşan cilt bir sonraki haftaya kalır.
- Kanal anayasasına girecek maddeler:
  1. **V1:** Tek font ailesi, HUD sayacı sabit konum/boyut/renk (üst arayüz çakışması kontrol edilene kadar y değeri geçici).
  2. **V2:** Tek imza vurgu rengi; her cildin paletinde birebir aynı.
  3. **V3:** 90 gün boyunca en çok 3 aktif cilt; cilt-konu eşlemesi yazılı; yeni cilt ancak mevcut cilt >=5 videoda kullanıldıktan sonra.
  4. **V4:** İlk kare = kanca kartı + cildin en güçlü kompozisyonu; son kare = ilk kare.
  5. **V5:** Her sahnede tek baskın nesne; 200 px genişliğe küçültülünce silüet okunur (illustrator'ın "net silüet" ilkesi).
  6. **V6:** Cilt özel kare hızı hileleri (12 fps gibi) yalnız illüstrasyonda; HUD ve yazı 24 fps.

## 7. One line

Kimlik önce gelir: sabit iskelet ve en çok üç adlı cilt, cilt-konu eşlemesiyle; ama stil kanıtı olmadığı için tek stile kilitlenmem ve 14 günlük ucuz veri çekimi sonucuna göre yönümü değiştiririm.
