# ROUND 1: Motion designer (motion)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md için klasörü taradım; dosya bulunamadı. Bu "aradım ve bulamadım" demektir, "ek yok" iddiası değildir; sonradan eklenirse okumadım).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Seçenek C (hibrit), ama "iskelet" önce hareket dilidir: tek bir ortak motion kiti (easing, kamera, yazı belirmesi, kesme ritmi, döngü kapanışı) kilitlenir; yalnız illüstrasyon cildi videodan videoya değişir. Bundan önce 14 gün boyunca D'nin ucuz yarısı (hareket yoğunluğu ile tutma eğrisini yan yana okuma) yapılır.
**Confidence:** medium

## 1. Position and why

1. **Hareket dili, "her videoda farklı stil" kararının bedelsiz taşınabilen kısmıdır.** Kara kalem, kâğıt kesme, blueprint farklı yüzey ister; ama easing eğrisi, vuruşa hizalı kesme, kelime belirme ritmi ve döngü kapanışı yüzeyden bağımsızdır. Bunları sabitlersem izleyici "bu kanalın ritmi bu" diye tanır; renk ve çizgi değişse de. Buyume ve artdir'in "tutarlılık" derdini ben hareketle karşılarım, boyayla değil. (Teşvikim: akıcılık ve ritim; kazanırım: tek motor, kaybederim: video başına özgün hareket kuralları.)
2. **Her 2-3 sn'de görsel değişim kuralı benim zorunlu maddem; ama "çok efekt" değil "okunur değişim".** Tavan: video başına en çok 2 ekran sarsıntısı, en çok 1 flaş, her yazı en az okunma süresi kadar ekranda (tahmin: Türkçe için ~12-14 karakter/sn rahat okuma; yöntem: genel okuma hızı varsayımı, ölçülmedi). Bu tavanlar hem benim "abartı" kör noktama hem izleyicinin yorgunluğuna karşı kilittir.
3. **Dans Salgını'nın 12 fps stop-motion hissi stil olarak savunulabilir ama bu kanalda risktir.** 24 fps çıktıda 12 fps her kareyi ikiler; sahne durağan kalırsa F6'daki "2 sn'lik hareket penceresi" QA'sı geçse bile gözde "donmuş" okunabilir. Dans'ın (100) Emu'ya (1700) göre düşüklüğünü buna bağlamam (n=2, çoklu karışıklık); ama stop-motion'ı varsayılan değil, istisna yaparım.
4. **Döngü kurgusu benim işim:** "son kare = ilk kare" (F6) tek başına döngü değildir. Son 0,5 sn'de hareket, ilk karedeki durumuna easing ile yaklaşmalı; yoksa sıçrama hissi tekrar izlemeyi değil kaydırmayı tetikler. Bu, retention'ın döngü talebini ucuza karşılar.
5. **Seytan'a karşı:** "Hiçbir şeyi değiştirme" (A) motion açısından bile kötü bir sabit değil, çünkü her video için yeni `scenes.py/ui.py/art.py/cues.py` yazılıyor (F5): hareket kuralları her seferinde yeniden icat edilir, kalite videodan videoya rastgele değişir. Maliyeti sessizdir.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Karışık baz (F2/E1):** Emu (1700) ile Dans (100) karşılaştırılırken tarih, ölçüm ve ses sürümü belli değil; F3'e göre Emu yeniden seslendirildi, yani 1700'ün hangi sürüme ait olduğu bilinmiyor. Aynı anda konu, kanca (F7: Dans'ta kanca kartı yok), ses, stil, fps ve yayın zamanı farklı. Hareketin etkisi bu veriden okunamaz.
- **Metrik sorunu:** Dosyada "görüntülenme" ölçüsü tanımsız. Mart 2025'ten beri Shorts'ta görüntülenme oynatma başlayınca sayılıyor (aşağıdaki kanıta bakın); 100 görüntülenme "100 kişi izledi ve bıraktı" değil "algoritma çok az kişiye gösterdi" olabilir. Bu kancaya karşı kaydırma ile dağıtım kısıtını birbirinden ayırmaz. "Engaged views" / tutma ayrı okunmalı.
- **E7 doğrulandı (kısmen):** Shorts üst sınırı Ekim 2024'ten beri 180 sn; 40 sn'lik format bir kural gereği değil tercihtir. Dosya "bazı kurallar değişti" diyor ama bunu açıkça yazmıyor; 40 sn hedefinin gerekçesi (tutma mı, üretim yükü mü) belirtilmemiş.
- **Güvenli alan eksik tarif:** Dosya yalnız alt %25 diyor. Sağdaki eylem düğmeleri ve üstteki arayüz de yazıyı örter (genel bilgi, bu oturumda doğrulamadım). HUD'un y≈260'ta olması üst bölgeye yakın; telefonda gerçek yerleşimle test edildiğine dair kayıt yok.
- **Eksik seçenek:** Seçenekler stil ekseninde; "hareket motoru ortak, yüzey değişken" ayrı bir seçenek olarak yazılmamış (C bunu kısmen kapsıyor ama iskelet tanımında hareket yok, HUD/tipografi/ses var).
- **F5 tutarsızlığı:** Render 4 süreçle ~95-100 sn, yani toplamda yaklaşık 960 kare / 97 sn ≈ 10 kare/sn (hesap: 40 sn × 24 fps ÷ ~97 sn). Darboğaz render değil, her videoya özel sahne kodu yazımı; dosya "gerçek süre kaç saat" sorusunu açık bırakıyor.
- **F7:** Dans'ta ilk kare doğrulanmamış ("hatırladığı kadarıyla"). Ben de videoları açmadım (kuralları gereği yalnız üç dosyayı okudum); ilk kare iddiası benim için de doğrulanamadı durumunda.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Shorts üst süre sınırı Ekim 2024'te 60 sn'den 180 sn'ye çıktı | fact (ikincil kaynak; YouTube'un kendi sayfasını açmadım) | WebSearch: Social Media Today, Tubefilter, PhoTutorial haberleri |
| 31 Mart 2025'ten beri Shorts görüntülenmesi oynatma başlayınca/tekrarda sayılıyor, eski ölçüt "engaged views" adıyla Gelişmiş modda | fact (ikincil kaynak) | WebSearch: PPC Land, MobileSyrup, Gigazine, 9to5Google |
| 100 vs 1700 farkı hareketten kaynaklanır | assumption, desteksiz | n=2, çoklu karışıklık; test edilmedi |
| 12 fps'in 24 fps çıktıda kareleri ikilemesi | fact (teknik) | Tanım gereği; F1 Dans'ın 12 fps ve 24 fps format bilgisinden |
| Render darboğaz değil (~10 kare/sn toplam) | estimate | 960 kare ÷ ~97 sn, F5'teki render.log tabanlı |
| Türkçe için ~12-14 karakter/sn okunma | assumption | Genel okuma hızı; telefonda ölçülmedi |
| Sağ/üst arayüz de güvenli alanı daraltır | assumption | Genel Shorts bilgisi, doğrulanmadı |
| Ortak motion kiti video başı kod yükünü azaltır | estimate | F5'e göre her videoda yeni 4 dosya yazılıyor; ortak kitaplık tekrarı keser; süre kazancı ölçülmedi |

## 4. Risks from this seat

- **A (değiştirme):** Hareket kalitesi her videoda rastgele; sessiz başarısızlık: yazı belirmesi, kesme ritmi, kamera tutarsızlığı izleyiciye "amatör" sinyali verir, ama kimse şikayet etmez, sadece kaydırır.
- **B (sabit kimlik):** Hareket tek şablona bağlanır, sahne çeşitliliği kaybolur; kullanıcının "her video farklı" isteğiyle çatışır. Hareket bakımından en güvenli ama en sıkıcı.
- **C (hibrit):** Yanlış kurulursa "iskelet" fazla büyür ve cilt sadece renk değişimine döner. Ayrıca ortak motor ile Pillow'un yavaşlığı arasında sapma olursa render süresi artar (varsayım).
- **D (deney):** Hareketi tek başına izole etmek zor; hareketi değiştirmek tüm sahne kodunu etkiler.
- **E (haftada 3-4):** Hareket için en iyi seçenek (video başı daha çok cila), ama dağıtım olasılığı düşer (E5 doğrulanmadı).
- **Sessiz risk:** Aşırı hareket; kelime kelime beliren altyazı ile kamera hareketi aynı anda okunurluğu bozar (benim kırmızı çizgim). QA bunu yakalayamaz çünkü "hareket var" kontrolü okunurluğu ölçmez.

## 5. The cheapest decisive step

**Adım:** (1–2 saat, ek yayın gerektirmez) Dört videoda ffmpeg `select='gt(scene,0.1)'` ile saniye başına kesme/sahne değişim sayısı ve piksel farkı çıkar. Bunu YouTube Studio'daki Emu ve Dans için tutma eğrisi + "izlenenlere karşı kaydıranlar" oranıyla yan yana koy. Ek olarak Titanik/Zanzibar yayınlandıysa onlarına da bak.

**Şimdiden karar:**
- Tutma eğrisinde düşüş hareketin durağan olduğu saniyelere denk gelirse (örn. 0-3 sn veya sahne geçişlerinde sert çukur), motion kitini zorunlu yaparım ve kesme tavan/taban kurallarını sıkılaştırırım.
- Emu ve Dans'ın ilk 3 sn düşüşü aynıysa ve hareket yoğunluğu farklıysa, hareketi ilk-3-sn kaldıracı saymam; motion bütçesini kanca/ses işine bırakır, kiti "asgari ortak kit" düzeyinde tutarım (A'ya yaklaşırım).
- Studio verisi (Emu ve Dans) hiç alınamazsa tutumum aynı kalır ama güvenim "low" olur.

## 6. Conditions and red lines

Desteklerim, eğer:
- Ortak motion kiti (`motion.py`) yazılır: easing seti (en fazla 3 eğri: ease-out cubic, ease-in-out, overshoot), tek kamera fonksiyonu, tek kelime-belirme fonksiyonu, tek döngü kapanışı.
- Ek maliyet ölçülür: yeni video başına sahne kodu süresi yazılıp 3 videoda karşılaştırılır; kit bunu azaltmıyorsa pipeline'ın itirazı geçerlidir.

Kabul etmem:
- Okunmayı bozan hareket (yazı hareket ederken okunmuyorsa red); 3 sn'den uzun durağan kare.
- Video başına 2'den fazla sarsıntı, 1'den fazla flaş.
- İlk kare ile son karede sıçrama (QA'ya "son 0,5 sn easing" kontrolü eklenmeli).
- Stop-motion (12 fps) yalnız bilinçli istisna olarak, haftada en çok 1.

**Kanal anayasasına öneri maddeler:**
1. Her 2-3 sn'de bir görsel değişim; hiçbir kare 3 sn'den uzun durağan değil.
2. Üç easing eğrisi dışında hareket yok.
3. Video başına en çok 2 sarsıntı, 1 flaş.
4. Her yazı, okunma süresi kadar ekranda kalır; hareket eden yazı okunur olmalı.
5. Son 0,5 sn ilk kareye easing ile kapanır.
6. Stop-motion/düşük fps yalnız istisna.
7. Yeni cilt, ortak motion kitini değiştirmeden eklenir.

## 7. One line

Sabit olan boya değil ritimdir: tek bir motion kiti kilitlensin, cilt değişsin, ve önce Emu ile Dans'ın tutma eğrisi hareket yoğunluğuyla yan yana okunsun; veri hareketin kaldıraç olmadığını gösterirse motion bütçesini küçültürüm.
