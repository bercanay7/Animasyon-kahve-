# ROUND 2: Motion designer (motion)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no
**Confidence:** medium

## 1. Vote and reason

C'yi seçiyorum (haftada 5, 3 günlük tampon, cilt tavanı 3, ilk 14 günde en çok 2 cilt). Round 1'deki "hibrit, iskelet önce hareket dilidir" tutumum sürüyor. Gerekçe motion koltuğundan: günlük + kapı + yeni cilt, cilaya ayrılacak süreyi (kelime belirme, son 0,5 sn kapanış, okunurluk) ilk eriyen kalemdir. Bu kalemler QA'da yeşil yanıp izleyicide "amatör" hissi verir.

**Yeni ölçüm (kendi yöntemim):** `ffmpeg select='gt(scene,T)'` ile dört videoda sahne-değişim sayısı (global kare farkı vekili). T=0,1: Zanzibar 22, Emu 5, Dans 26, Titanik 24. T=0,3: 7 / 0 / 0 / 3. T=0,05: 57 / 28 / 295 / 36 (Dans'taki 295, 12 fps oynaklığıdır). En çok izlenen Emu en az kesmeli çıktı. Sınırlar: n=2 izlenme sayısı, ölçüt belirsiz (Ek 01A m.1), tutma eğrisi yok. Sonuç: "kesme yoğunluğu kaldıraçtır" varsayımım zayıfladı; motion kitini asgari tutuyorum.

Tur 2 sorularına yanıtlarım (anayasa maddesi önerisi):
- **Cilt (S1):** tavan 3. İlk 14 günde 2 (kara kalem, kâğıt kesme; yeni kod yok). Cilt, yazılı konu-cilt eşlemesiyle atanır. Kanca kura ile atanır, böylece kanca ile cilt çaprazlanır ve kanca karşılaştırması bulanmaz.
- **Sıklık/süre (S2):** haftada 5, tampon 1 güne inerse 3–4. Süre ilk 14 günde 40 sn ± 0,5 kalır, çünkü tek eksen kanca. Süre ikinci tek-eksen testi olur (30 sn = 48 vuruş @96 BPM = 720 kare). Ses TTS süresi vuruş ızgarasına uzatılarak değil, ızgara ±1 vuruş esnetilerek uydurulur.
- **Kapılar (S4):** hareket kontrolleri otomatik olmalı (insan süresi ≤1 dk): `freezedetect` ile 3 sn'den uzun durağan kare yok; yazı birimi ekranda ≥ max(1,0 sn; karakter/13 sn) kalır (13 k/sn varsayım); video başına ≤2 sarsıntı, ≤1 flaş; son 0,5 sn easing ile ilk kareye kapanır. Rapor her render'da yeniden üretilir (Ek 01A m.9: bayat rapor).
- **Ölçüt (S5):** katılıyorum: kaydıran oranı + ortalama izlenme %, 48 sa ve 7 gün. Motion'a özel okuma: tutma eğrisindeki en dik orta düşüş, sahne geçişine ya da ≥2 sn düşük hareket aralığına ±1 sn yakınsa ≥3 videoda, kural sıkılaşır; değilse kit asgari kalır.
- **Kanca (S6):** kart kare 0'da tam kurulmuş olmalı (giriş animasyonu yok; kare 0 hem kapak hem son karedir). Hareket ≤0,3 sn'de başlar (hafif kamera itişi), ilk görsel değişim ≤2 sn. Yazı ≤6 kelime, ≥64 px, ≤2 satır.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| analitik | İlk 14 gün cildi dondur | Kısmen karşıyım | Kendi güç hesabınız (hücre başına ~47 video) 14 videoda cilt etkisinin iki tasarımda da okunamayacağını söylüyor. Dondurmak ölçüm gücü kazandırmaz. Korunması gereken şey kanca karşılaştırmasıdır; kura-atamalı kanca cilde ortogonaldir. Dondurma yalnız kullanıcının isteğini bekletir. Tek eksen ve yayın günlüğü maddelerinize katılıyorum. |
| pipeline | Ortak motor, ≤4 cilt, Titanik taşıma ölçümü | Büyük ölçüde katılıyorum, tavanda ayrılıyorum | Kitim ancak sizin ölçümünüz kit başına süre düşürürse geçerli; ölçüm ön koşuldur. Tavan 4 değil 3: her cilt hareket kitiyle ayrı okunurluk testi ister. Cilt başına ≤90 dk (artdir) sınırı iyi. |
| buyume | Tek imza blueprint olsun | Katılmıyorum | Seçimin kanıtı yok; yalnız "Titanik'te zaten var" denmiş. Ölçülen tek zayıf ipucu tersini gösteriyor (en çok izlenen Emu, kara kalem), n=2 ve karışık. Dondurulacaksa seçim kanıtla değil eşlemeyle yapılmalı. |
| kanca | Kanca ≤9 kelime | Katılmıyorum | 9 kelime 64 px'te 2–3 satır eder. Retention'ın ~3 kelime/sn okuma varsayımıyla ~3 sn; ilk saniye bütçesini aşar. ≤6 kelime (thumb ile uyumlu), kalanını ses taşısın. Kare 0 kuralı, başlık kartının fade-in ile açılmasını da yasaklıyor. |
| muzik | 96 BPM, 15 karelik ızgara | Katılıyorum, bir koşulla | Kesme ve kelime belirmesini ızgaraya bağlamak sahne senkronunu otomatikleştirir. Ancak 40,0 sn'yi TTS'e dayatmak anlatıcı temposunu bozar; ızgara anlatıma ±1 vuruş esner. Kare 0'da tek imza vuruşu, kare-0 kart kuralımla çakışmıyor. |
| seytan | Yeni cilt yok, tek değişken | Çoğunlukla katılıyorum | Emu ve Dans cildi zaten var; iki mevcut cilt yeni kod getirmez, kural ihlal edilmez. Ama kit kodu "yeni değişken" sayılırsa A, bugünkü her video için yeniden icat düzenini sürdürür. Kit, 0. günde ortak taban olmalı. |

## 3. Corrections accepted or disputed

- **Ek 01A m.3 (ilk kare ölçümü):** kabul. Emu'da kare 0'da skor tabelası tam kurulu; bu, kare-0 kuralımın çalışan örneği. Dans'ta kanca yok ama kâğıt-kesme oynaklığı en yüksek; "durağan" değil, "okunur vaadi olmayan hareket" sorunu var.
- **m.1 (metrik) ve m.2 (3 dk):** kabul. Kesme yoğunluğu ile 1700/100 ilişkisi kurmuyorum; yukarıdaki ölçüm yalnız "motion kaldıraç mı" kuşkusunu besler. 40 sn tercih, ikinci tek-eksen testidir.
- **m.10 (üst/sağ arayüz):** kabul. HUD sayacı hareketli olduğu için göz tam arayüzle çakışabilecek y≈260 bölgesine çekiliyor. Yazı katmanı ekran uzayında sabit olmalı, kamera hareketine girmemeli (renktipo ile uyumlu); güvenli alan ölçüsü denemeyle doğrulanana kadar geçici.
- **m.9 (bayat QA):** kabul. Hareket kontrolleri qa.py'ye girecekse her render'da yeniden koşmalı.

## 4. What would reverse this vote

- Pipeline'ın Titanik taşıması >3 gün sürerse ya da ikinci cilt ≥90 dk eklerse: A'ya (tek cilt) geçerim; paylaşılan kit yoksa cilt çeşitliliği hareket kalitesini düşürür.
- 3 günlük tampon 14 gün boyunca korunur ve kapı ≤10 dk kalırsa: B'ye (günlük) geçerim; haftada 5 yalnız tampon kuralıdır.
- Emu ve Dans'ın ilk 3 sn düşüşü aynı çıkarsa oy değişmez; motion bütçesini kanca/ses işine bırakır, kiti asgari tutarım.

## 5. Dissent to record

none. Not: sonuç A çıkarsa, kayda geçmesi gereken şerhim: hareket kiti "yeni değişken" sayılmamalı, 0. günde ortak taban olarak yazılmalı. Aksi halde A, bugünkü "her video hareket kurallarını yeniden icat eder" düzenini ölçümsüz sürdürür.
