# ROUND 1: Üretim hattı mühendisi (pipeline)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md için klasörü taradım; dosya bulunmadı. Bu "aradım, bulamadım" demektir, "yoktur" demek değildir).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** Seçenek C, ama sıkı bir mühendislik şartıyla: tek ortak motor + kilitli bir "cilt" kataloğu (en fazla 4 cilt), her cilt veri dosyası olarak yazılır; yeni cilt ancak QA'dan geçip şablonlaştıktan sonra kullanılır. Her gün sıfırdan sahne kodu yazmak (bugünkü Seçenek A) bırakılmalı.
**Confidence:** medium

## 1. Position and why

1. **Darboğaz render değil, "her video yeni kod".** Dossier F5: render ~95–100 sn, ses dakikalar; ama her video yeni `scenes.py / ui.py / art.py / cues.py` istiyor. Render maliyeti sabit ve küçük; değişken ve riskli kısım, her gün yazılan yeni kod. Her yeni kod = yeni hata yüzeyi. Bu benim ölçütüm (süre ve hata oranı) için en kötü yapı.
2. **Günlük yayın, ancak "sahne = veri, motor = sabit" ise sürdürülebilir.** Hibrit tam bunu verir: sabit iskelet (kanca kartı, HUD y≈260, altyazı, güvenli alan, döngü, LUFS zinciri) bir kez yazılır ve test edilir; değişen yalnızca illüstrasyon cildi. Stil çeşitliliği isteyen kullanıcıyı da karşılar, bakım yükünü sınırlar.
3. **Ne kaybediyorum:** Seçenek B daha da ucuz olurdu (tek cilt = en az kod), ama kullanıcının açık isteğini (her videoda farklı sanat tarzı) kanıt olmadan çiğner. Hibritte bakım maliyeti cilt sayısıyla doğrusal artar; bu yüzden tavan koyuyorum.
4. **Ne kazanıyorum:** Yeni video süresi "kod yazma + hata ayıklama" yerine "metin + sahne verisi + render" olur; aynı motorda tek bir hata düzeltmesi tüm ciltleri iyileştirir.
5. **Yan etki:** Ses hattı da sabitlenmeli (tek anlatıcı yapılandırması, telaffuz sözlüğü). Dossier F4'te ~%20 kelime hata oranı var; bu bir üretim hatasıdır, tartışma konusu değil.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Seçenek A'nın maliyeti "ek maliyet yok" diye yazılmış: yanlış kurulmuş.** Her gün yeni stil = her gün yeni kod tabanı. Maliyet yok değil, her gün tekrar ödeniyor ve görünmüyor. (Olgu: F5'ten türetilmiş akıl yürütme.)
- **"Günde 1 video üretilebilmeli" ölçülmemiş.** F5 yalnızca "Titanik bir oturumda üretildi" diyor; insan/ajan süresi saat olarak yok. Ölçüm olmadan "sürdürülebilir mi" sorusu cevapsız. Bilinmeyen olarak işaretlenmeli.
- **Seçenek C'nin maliyeti "orta" ve Seçenek B'nin "1–2 gün" olarak verilmiş, kaynaksız.** Bunlar tahmin; yöntem yok. Benim tahminim ayrı (bkz. bölüm 3).
- **F3 tutarsız bir baz:** Emu'nun hangi sesle yayınlandığı belli değil, Zanzibar seslendirmesiz, Dans ve Titanik yeni anlatıcıyla. Ses ve stil ve konu aynı anda değişti; üretim açısından "hangi ses sürümü hangi videoda" kaydı yok. Bu bir sürümleme eksiği: videoyla birlikte kullanılan ses/cilt/motor sürümü (git hash) kayıt altına alınmıyor gibi görünüyor (varsayım; kod tabanını okumadım).
- **F4'teki WER ~%20, çoğu yabancı ad:** Whisper'ın sentetik Türkçe ve yabancı adlarda hatası, TTS hatasından ayrılamaz (ASR'nin kendi hatası da ölçüye giriyor). Ölçüt olarak sadece iş görür, mutlak sayı olarak güvenilmez.
- **E7 (Shorts süresi/metrik kuralları) doğrulanmamış:** Doğrulama aracı kullanmadım; 40 sn hedef hiçbir olası üst sınırı ihlal etmediği için hattımı etkilemiyor, doğrulayıcıya bırakıyorum.
- **Eksik seçenek:** "Motoru ve telaffuz sözlüğünü önce yap, kararı sonra ver" bir seçenek olarak yok; C ve D bununla birleşebilir: ilk 14 günde D deneyi, aynı motor üzerinde.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| Render ~95–100 sn, 4 süreç; ses sentez+miks dakikalar | fact | Dossier F5 (render.log) |
| Her videoda yeni sahne kodu yazılıyor | fact | Dossier F5 |
| Günlük yayının asıl maliyeti sahne kodu yazımı ve hata ayıklamadır | estimate | F5'ten çıkarım; yöntem: render süresi (~2 dk) ile "bir oturum" karşılaştırması. Ölçüm yok |
| Ortak motor + veri dosyalı sahne, yeni video süresini en az yarıya indirir | estimate | Genel yazılım pratiği; Titanik'i yeniden yazarak ölçülecek (bölüm 5) |
| QA kapsamı: kare, HUD, ilk/son kare, ≤0,3 sn yazısız, LUFS | fact | Dossier F6 |
| QA "his" kalitesini (merak, kanca) ölçmez | assumption | qc kartı ve F6 listesi: kanca/tutma kontrolü yok; kodu okumadım |
| Telaffuz sözlüğü hata oranını düşürür | estimate | Yöntem: aynı 20 yabancı adı sözlüksüz/sözlüklü sentezleyip Whisper ile kıyasla; henüz yapılmadı |
| Dossier'da ADDENDUM-01 yok | fact (aradım, bulamadım) | Glob: ADDENDUM-01*.md, sonuç boş |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** Sessiz hata: yeni stilde `qa.py`'nin kapsamadığı bir kusur (ör. yeni fontta Türkçe İ/Ş/Ğ eksik) fark edilmeden yayına çıkar. Üretici yorgunluğu geç görünür: günlük yeni kod, 2–3 hafta sonra bir günü atlatır ve kanal "günlük" vaadini kaybeder.
- **B (sabit kimlik):** Geçiş ~1–2 gün (tahmin) hat durması demek; bu sürede yayın aksarsa 3 günlük tampon yoksa gün atlanır.
- **C (hibrit):** Cilt sayısı sessizce artar ("bir tane daha ekleyelim"); her cilt bakım borcu. Motor sürümü değişince eski cilt kırılır (regresyon) ve fark edilmez.
- **D:** Deney sırasında motor değişirse deney geçersiz olur; yani motor donmuş olmalı.
- **E (haftada 3–4):** Hat açısından en güvenli, ama büyüme ölçütüyle çelişir; yayın sıklığının etkisi bu veride ölçülemez (E5).
- **Sessiz kırılgan nokta:** Piper/WORLD/ffmpeg sürümleri sabitlenmemişse (kilit dosyası yok varsayımı) bir güncelleme sesi veya miksi değiştirir ve hiç kimse fark etmez.

## 5. The cheapest decisive step

**Bir ölçüm:** Titanik videosunu (en yeni, tam QA'lı) "motor + veri" modeline taşı (sahne içeriği JSON/dict, kod tek motor) ve aynı motorda 2. bir cilt ile ikinci bir sahneyi çalıştır. Zaman damgalı kayıt tut: toplam çalışma süresi, ayrı olarak TTS bekleme süresi. Tahmini maliyet: yarım ila 1 iş günü. Aynı gün telaffuz sözlüğü testi (20 ad, ~1 saat).

**Karar kuralı (şimdiden):**
- Taşıma ≤ 1 gün VE yeni bir videonun (TTS beklemesi hariç) etkin üretim süresi ≤ 90 dk ise: C onaylanır, cilt tavanı 4 kalır.
- Taşıma 3 günü aşarsa VEYA QA geçmezse: pozisyonumu B'ye (tek cilt) çeviririm.
- Taşıma ≤ 2 saat ve cilt başına ek maliyet ≤ 1 saat çıkarsa: cilt çeşitliliği tavanını 6'ya çıkarmaya razıyım ve A'ya yakın bir serbestliğe itiraz etmem.

## 6. Conditions and red lines

Desteklerim, eğer:
- Motor ve cilt ayrı; yeni cilt = yeni veri/şablon dosyası, motor değişikliği değil.
- Her yayın öncesi `qa.py` çıkış kodu sıfırdan farklıysa yayın bloklanır (otomatik, manuel geçiş yok).
- Üç günlük hazır video tamponu (geç kalmaya karşı).
- Her video ile birlikte motor sürümü, cilt adı, ses yapılandırması ve metin kaydedilir.

Kabul etmem:
- "Bugün yeni kod, bugün yayın": test edilmemiş yeni cilt aynı gün yayına çıkamaz.
- Sabitlenmemiş bağımlılık sürümü.
- Elle yapılan, kayıt dışı ses düzeltmesi.

**Kanal anayasasına önerdiğim maddeler:**
1. Cilt kataloğu en çok 4 cilt; yeni cilt ancak 14 günde bir, QA'dan ve bir deneme render'ından sonra eklenir.
2. Sabit iskelet: kanca kartı (ilk karede), sayaç/HUD, altyazı, güvenli alan, döngü, −14 LUFS. İskelet kodu yalnızca motor sürümü yükseltmesiyle değişir.
3. Tek ses kimliği dosyası (anlatıcı + yankı ayarı + telaffuz sözlüğü); video başına ses değişimi yok.
4. Yayın kapısı: otomatik QA yeşil + elle 10 sn'lik "ilk kare/son kare/telefon" bakışı.
5. En az 3 günlük tampon; tampon 1 güne düşerse haftalık yayın Seçenek E'ye (3–4/hafta) otomatik geçer.
6. Her videoya sürüm künyesi (motor hash, cilt, ses).

## 7. One line

Günde bir video ancak ortak motor ve en fazla 4 kilitli cilt ile, otomatik QA kapısı ve 3 günlük tamponla sürdürülebilir; "her gün yeni kod" modeli bakım borcu üretir, ve bunu bir günlük Titanik taşıma ölçümüyle doğrulamadan kesin konuşmuyorum.
