# ROUND 2: Üretim hattı mühendisi (pipeline)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no (Tur 1'de de hibrit/C idim. Yalnız ayrıntı sıkıldı: cilt tavanı 4'ten 3'e indi, "ölçüm iyi çıkarsa 6" sözümü geri çekiyorum; gerekçe artdir V3 ve qc'nin "her cilt yeni hata yüzeyi" argümanı.)
**Confidence:** medium

## 1. Vote and reason

**Yeni ölçüm (kendi yaptığım, kod okuması + `diff`):** `engine.py`, `compose.py`, `contact.py` üç videoda bayt bayt aynı; `render.py` 2 satır farklı. Yani ortak motor zaten var, kopyala-yapıştır olarak. Gerçekten çatallanan dosyalar: `ui.py` (113-143 farklı satır), `cues.py` (51-68) ve `audio.py` (246-255). Süre `cues.T`'den türüyor (`NF = round(cues.T*FPS)`), yani süre bir parametre. Sonuç: dosya F5'in "her video yeni kod" çerçevesi kısmen yanlış; asıl sızıntı **ses zincirinin her videoda çatallanması**. Ses kimliği sorunu tam burada üretiliyor.

C neden, A (dondur) değil: A'nın tek-cilt dondurması benim kararımın dayandığı tek ölçümü, 2. cilt maliyetini, 14 gün erteler ve bilinmeyen maliyet 15. günde baskı altında ilk kez ödenir. Dondurma disiplinini (motor, ses, iskelet) C'de de uyguluyorum; yalnız 2 cilt var.

**Anayasa yanıtları (G):**
- **G1 cilt:** tavan 3 (kara kalem, blueprint, kâğıt kesme). İlk 14 gün 2 cilt (blueprint + kara kalem, kod zaten var). Yeni cilt: mevcut cilt ≥5 videoda kullanıldıktan sonra, ek maliyet ≤90 dk.
- **G2 sıklık/süre:** haftada 5, 3 videoluk tampon; tampon <1 olursa otomatik 3-4/hafta. Varsayım: üretim kapasitesi 7/hafta ise tampon +2/hafta, ~11. günde 3'e ulaşır. Süre: ilk 14 gün 40,0 sn (tek değişken kuralı). Sonra 30,0 sn'ye geçiş maliyeti ≈0: 96 BPM'de 12 ölçü = 48 vuruş × 0,625 = 30,0 sn = 720 kare.
- **G3 ses:** tek `voice.json` (model, `reverb_wet=0.0`, sürüm). Kör test eşiği seslendirme'ninki: ≥4/5 tercih, ≤1/5 "robot". Ek: kadın WORLD adımı video başına ≤+5 dk ve `pyworld` sürümü kilitli olmalı.
- **G4 kapılar:** otomatik (0 dk insan): final mp4'ün sha256'sına bağlı QA raporu, AAC sonrası LUFS/peak, sözlük kapsaması, `tr_upper()` lint'i (`.upper()` yasak), `sources.md` satır sayısı, zorunlu `hook_card` alanı, ilk ses ≤0,5 sn. İnsan: tek oturum ≤15 dk. Günlük toplam ≤20 dk; 14 gün üst üste aşılırsa E'ye geçilir. Kaynak doğrulaması render gününde değil konu seçiminde (T-3), havuz ≥5 konu.
- **G5 ölçüt:** analitik'in 48 sa/7 gün penceresine katılıyorum. Hat ölçütü: video başı ≤90 dk (TTS beklemesi hariç), teknik yeniden yükleme 0/hafta. Yayın günlüğü (motor hash, cilt, ses) elle değil jsonl olarak otomatik yazılır.
- **G6 kanca:** kart alanı doldurulmadan render hata verir; ≤9 kelime lint'i; yerleşim değerleri `safe_area.json`'dan okunur. "Vaat ödendi" otomatik denetlenemez: `sources.md`'de "ödendiği saniye" alanı + insan imzası.
- **G7 en ucuz adım:** Titanik'i ortak motora taşı + 2. cilt, ≤1 gün. Karar kuralım Tur 1'deki gibi.
- **G8 Titanik kartı:** kart metni veri alanıdır, düzeltme ≈ render 100 sn (V47). Sözlü metin değişmiyorsa yeniden sentez gerekmez (varsayım: `tts.py` ayrı). Ama yeniden yükleme yeni video sayılır (analitik).

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| seytan | 14 gün tek cilt, zorunlu günlük yok | Yarı katılıyorum | Haftada 5 evet. Tek cilt hayır: 14 videoda cilt etkisi okunmaz (kendi hesabınız 7'ye 7'de ancak ~3x), ama cilt maliyeti ölçülür. Dondurmanın getirisi bende yok. |
| analitik | Dondur, tek eksen | Katılıyorum, bir yerde itiraz | "Motor donmuş olmalı" benim D riskimdi: motor v1.0 etiketlenir, yalnız hata düzeltmesi, her video hash taşır. Cilt 2 kalır; iki cildin etkisini ben de okumuyorum. |
| buyume | 14 gün tek cilt, sonra veriyle ekle | Kısmen yanlış | Cilt 2'nin ilk kez 15. günde, yayın baskısı altında yazılması en pahalı zamanlamadır. |
| olgu | Her iddia 2 kaynak, günde 15-20 dk, ikinci kişi | Kapıya evet, zamanlamaya hayır | Tek operatörlü hatta ikinci kişi yok; kapıyı T-3'e çekin, render gününde yalnız lint kalsın. |
| sesmuh | WER ≤%10 QA eşiği | Bloklayıcı olmasına hayır | Ek 5: ölçüm TTS ile Whisper hatasını ayırmıyor. Bilgi amaçlı kalsın, bloklayıcı kapı sözlük kapsaması + dinleme olsun. |
| muzik | 96 BPM, tam 40,0 sn | Katılıyorum, sabitlemeyin | Izgara parametrik olmalı (ölçü sayısı); retention 30 sn isterse maliyet sıfır. |
| dil | `.upper()` yasak, okunuş ≠ ekran metni | Katılıyorum | Lint ve `tr_upper()` ucuz. Kodda `.upper()` yok (grep, Titanik), ama kural tekrar yazılan `ui.py`'ye karşı sigorta. |

## 3. Corrections accepted or disputed

- **Ek 9 (bayat QA):** kabul. Rapor dosya hash'ine bağlanmazsa "QA yeşil" kapısı sessiz yalan söyler. LUFS ölçümü `audio.py`'den QA'ya taşınır.
- **Ek 4 ve V44:** kabul. `narrator.py` içindeki 1,65/1,17 yorumu bayat (kod 1,55/1,14); temizlenir. `reverb_wet` adı "ıslak pay" olarak belgelenir.
- **Ek 10:** kabul. Güvenli alan rakamları (üst 290/alt 672) sabit kodlanmaz; ızgara çizili bir test karesi telefonda denenip `safe_area.json`'a yazılır.
- **Dosya F5, itirazım:** "her video yeni `scenes/ui/art/cues`" eksik; `audio.py` çatalı yazılmamış. Kanıt: yukarıdaki diff.

## 4. What would reverse this vote

Titanik taşıma >3 gün sürerse ya da taşınan videoda QA geçmezse A'ya (tek cilt, dondur) dönerim. Taşıma ≤2 saat ve cilt başına ek maliyet ≤1 saat çıksa bile tavan 3'te kalır. Kapı süresi pilotta 20 dk'yı aşarsa haftada 4'e inerim.

## 5. Dissent to record

B'yi (günlük yayın) savunanlara: günlük yayın + 30-60 dk kapı + ~90 dk üretim ≥2,5 saat/gün eder ve tampon sıfırdan başlar. İlk atlanan kapı sessiz hatadır; QA yeşil yanar, yanlış bilgi çıkar. Günlük hedef ancak 3 videoluk tampon kurulduktan sonra savunulabilir; o zaman sıklık yükseltilebilir, tersi mümkün değildir.
