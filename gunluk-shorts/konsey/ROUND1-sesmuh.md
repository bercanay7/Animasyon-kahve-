# ROUND 1: Ses mühendisi (sesmuh)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md için Glob ile arandı; klasörde bulunamadı. Bu "aradım, bulamadım"dır, "yoktur" değildir).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Önce ses kimliği sabitlensin: tek anlatıcı, varsayılan KURU konuşma (yankı 0), ölçülmüş ve telefon hoparlöründe doğrulanmış tek bir miks şablonu; sonra diğer her şey. C (hibrit) seçeneğini, ses katmanı B kadar sabit olmak şartıyla desteklerim. A'yı (ses ayarı videoya göre değişsin) reddederim.
**Confidence:** medium

## 1. Position and why

1. **Kuru ses varsayılan olmalı.** Kullanıcı yeni sesi için "yankılı geliyor" dedi (F3). Yankı, kısa biçimde anlaşılırlığın ilk düşmanıdır: kuyruğu bir sonraki heceyi örter, telefon hoparlörü (tek küçük sürücü, bas yok) bunu daha da kötüleştirir. Öneri: anlatıcıda reverb mix 0; atmosfer gerekirse yalnızca müzik/efekt bus'ına, konuşmaya değil. "Sinematik" his anlaşılırlığın bedeliyle satın alınmaz.
2. **Ses kimliği sabit olmalı, videoya göre oynanmamalı.** Dosya A'yı "kuru/yankılı ayarı videoya göre" diye tarif ediyor; bu, her videoda ayrı bir miks demek, yani ölçülemeyen değişken. Tek bir `narrator.py` ön ayarı (EQ, kompresör, yankı=0, LUFS hedefi) kanal anayasasına sayısal değerleriyle yazılsın.
3. **Müzik konuşmanın altında kalmalı, ducking zorunlu.** Konuşma varken müzik yatağı konuşmadan en az 14–18 dB (kısa-süreli LUFS farkı) aşağıda; konuşma yokken yükselir. Zanzibar'ın seslendirmesiz olması (F1) ayrı bir tutarsızlık: müzik-yalnız video, ses kimliği olmayan videodur.
4. **Kazanım/kayıp:** Koltuğum anlaşılırlıkta kazanır; kaybı, atmosferin sadeleşmesi ve "klas" arayan kullanıcının beklentisi. Kullanıcı "klas ama heyecanlı" istedi; ben "klas"ı yankıyla değil temiz kompresyon + hafif sıcaklık EQ'su + iyi sessizlik yönetimiyle veririm.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **F4'te belirsiz/muhtemelen yanlış ifade:** "kuru oran ~%8,5". Kuru oran %8,5 ise karışımın %91,5'i yaş (yankılı) demektir; bu, kullanıcının "yankılı" şikâyetiyle uyumlu ama başka şeyi kastediyorsa (yaş oran %8,5) kayda yanlış girmiştir. Hangisi olduğu kodda (`ses-lab/narrator.py`) kontrol edilmeli; ben dosyayı açmadım (kurallar gereği yalnız üç dosya). Doğrulanamadı.
- **F4: "kelime hata oranı ~%20 (çoğu yabancı ad)"** iki şeyi karıştırır: Whisper'ın kendi Türkçe/yabancı ad hatası ile Piper'ın gerçek yanlış telaffuzu. WER yalnız bir vekil ölçüttür; izleyicinin anlaması değildir. Ayrıca %20 kabaca beş kelimede bir hata; sayı ve ad ağırlıklı hataysa videonun "olgu" yükünü taşıyan kelimeler yanlış okunuyor olabilir (dil ve olgu koltukları bunu daha iyi yargılar).
- **Eksik: hoparlör doğrulaması hiç yapılmamış.** Dosyada ne LUFS çıktıları ne telefon dinlemesi ne spektrum var. F6 "LUFS/true peak" ölçüldüğünü söylüyor ama değerleri yok. "−14 LUFS" bir hedef; gerçek değerler dosyada yok.
- **−14 LUFS çerçevesi kısmen yanlış kurulmuş olabilir.** İkincil kaynaklara göre YouTube yalnız yüksek sesi aşağı çeker, sessiz sesi yükseltmez (aşağıdaki tablo). Yani −14'ün altında kalan video sessiz kalır; −14 "tavan" gibi davranır. Hedefi −14 integrated, true peak ≤ −1 dBTP olarak yazmak doğru; ama Shorts'ta insanlar çoğunlukla ses kısık dinler, kısa süreli seviyeler ve konuşma oranı integrated değerden önemlidir.
- **E2 ("ses izlenmeyi etkiler") kötü kurulmuş:** F3'e göre Emu'nun hangi sesle yayınlandığı bilinmiyor; ses, konu, stil, saat aynı anda değişti. Analitik koltuğuyla aynı fikirdeyim: n=2'den ses nedensellik çıkmaz. Ama bu, sesi önemsiz kılmaz; sesin "ucuz düzeltilebilir ve geri alınabilir" olması onu önceliklendirir.
- **Yanlış soru:** "kadın mı erkek mi" ses teknolojisi sorusundan önce kalite sorusudur. WORLD ile f0×1,55 ve formant×1,14 dönüşümü kulakla dinlenmedi (F4); vokoder artefaktı (metalik/boğuk "s" ve "ş") Türkçe'de yüksek frekanslı ünsüzleri bozar. Dinlenmemiş bir sesi karar masasına koymak erken.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| YouTube yalnız −14 LUFS üstündeki sesi aşağı normalleştirir, düşük sesi yükseltmez | fact (ikincil kaynaklar; birincil YouTube yardım sayfası doğrulanmadı) | WebSearch: Youlean, Ian Shepherd/Meterplugs ve Shotcut forum özetleri; sorgu "YouTube loudness normalization -14 LUFS" |
| YouTube referansını 2019'da −14 LUFS'a çekti | fact (ikincil) | Meterplugs/Ian Shepherd yazısı, aynı arama |
| Yankı telefon hoparlöründe konuşma anlaşılırlığını düşürür | estimate | Genel akustik bilgisi; bu kanalın sesinde ölçülmedi |
| Piper çıktısı + yaş yankı, kullanıcıya "yankılı" geldi | fact (kullanıcı gözlemi) | Dosya F3 |
| WORLD dönüşümünün Türkçe "s/ş/ç" netliğini bozma riski | assumption | Vokoder genel bilgisi; sesi dinlemedim |
| Müzik konuşmanın 14–18 dB altında olmalı | estimate | Mühendislik pratiği; bu kanal için test edilmedi |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** Videoya göre değişen yankı/müzik düzeyi = sessiz hata. Hiçbir QA bunu yakalamaz çünkü LUFS tutsa bile anlaşılırlık düşebilir. Kullanıcı sesten zaten rahatsız; sessiz kayıp izleyici güveni.
- **B/C:** Sabit bir miks yanlış sabitlenirse (ör. kısık dinleyen telefon için hep fazla sıkıştırılmış) tüm videolar aynı hatayı taşır. Bu yüzden ön ayar önce doğrulanıp sonra donmalı.
- **Sessiz hata:** Dosya sonundaki/başındaki tık sesi, AAC kodlamasından sonra true peak taşması (WAV'da −1 dBTP olan ses AAC sonrası aşabilir), kanal başına farklı seviye. QA "dosyada" ölçer; yüklemeden sonraki sürümü ölçmez.
- **D (deney):** Ses deneyi için en az iki sürüm üretmek gerekir; ucuz ama yalnızca gerçek dinleyiciyle anlamlıdır.

## 5. The cheapest decisive step

**Yarım günlük "hoparlör ve A/B" testi (≈0 maliyet):** Aynı Emu metni, kuru (yankı 0) ve mevcut yaş sürüm olmak üzere, ayrıca erkek vs. dönüştürülmüş kadın sesi; hepsi −14 LUFS'a eşit seviyede. Bir telefonun hoparlöründe, kısık ve orta ses seviyesinde, 5 kişiye (izleyici arketipine yakın, kör) "hangisini anlayarak sonuna kadar dinlerdin, yabancı adları anladın mı?" diye sor. Ayrıca bir cümlelik ad listesiyle (Zanzibar, Strasbourg, Robertson, Titan) telaffuz testi.
**Kararı değiştirecek sonuç (şimdiden):** Kuru sürüm 5 kişiden en az 3'ünde açıkça tercih edilmezse (yaş sürüm eşit ya da üstün), yankıyı sıfırlama kuralından vazgeçip düşük (<%15) bir oran kabul ederim. Kadın dönüştürülmüş ses 5 kişiden en az 4'ünde "doğal" bulunmazsa veya "s/ş" netliğini kaybediyorsa kadın sesine karşı çıkarım; erkek sesi sabitlerim. Bu n=5 yön göstergesidir, istatistik değil.

## 6. Conditions and red lines

Desteklerim, eğer: (a) anlatıcıda yankı varsayılan 0, (b) konuşma varken müzik ducking ile en az 14 dB altında, (c) integrated −14 LUFS ±1, true peak ≤ −1 dBTP, AAC kodlamasından sonra yeniden ölçülmüş, (d) her video için telefon hoparlöründe 30 sn'lik dinleme kaydı QA'da işaretlenmiş, (e) ilk ve son örnekte fade (en az 5–10 ms) ve DC kayması yok, (f) yabancı ad/sayı için telaffuz sözlüğü ve kuru test cümleleri.
Reddederim: sesi bastıran müzik, aşırı yankı, tık sesi, her videoda farklı ses ayarı, dinlenmemiş (kulak testsiz) bir sesi yayına sokmak, seslendirmesiz video (Zanzibar tipi) kanal imzasını bozuyorsa.

Kanal anayasasına önerilen maddeler: (1) Tek anlatıcı kimliği; ses parametreleri sürümlü dosyada. (2) Yankı konuşmada 0. (3) Hedef −14 LUFS integrated, ≤ −1 dBTP, kodlama sonrası ölçüm. (4) Müzik ducking ≥ 14 dB, müzik yatağı konuşmasız saniyelerde yükselebilir. (5) Yayın öncesi telefon hoparlörü dinlemesi, kayıtla. (6) Yabancı ad sözlüğü zorunlu; WER ≤ %10 (adlar hariç ölçülür) QA eşiği. (7) Her videoda en fazla 2 vurgu efekti türü; ucuz stok efekt yok.

## 7. One line

Kuru, sabit, ölçülmüş ve telefon hoparlöründe doğrulanmış tek bir anlatıcı sesi olmadan stilin ve konunun ne kadar iyi olduğunun önemi yok; önce 5 kişilik kör A/B testi, sonra ses şablonunu dondurun.
