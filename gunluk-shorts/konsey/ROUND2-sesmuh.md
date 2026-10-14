# ROUND 2: Ses mühendisi (sesmuh)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, VERIFICATION.md ve 21 Tur 1 raporunun tamamı.

**Vote:** C
**Changed from round 1:** no
**Confidence:** medium

## 1. Vote and reason

C: B'nin sürdürülebilir hâli (haftada 5, 3 günlük tampon, ilk 14 günde en çok 2 cilt). Ses katmanı A, B ve C'de aynı kuralla donuyor; seçenekleri ayıran şey benim için ses ölçümünün yapılabileceği zamandır. Tampon, miksi kodlama sonrası ölçmeye ve ertesi gün taze kulakla dinlemeye yer açar. Günlük koşuda bu adım ilk atlanan adım olur.

Yeni ölçümlerim (yöntem: `ffmpeg ebur128=peak=true`, kodlanmış mp4 üzerinde):

| Dosya | Entegre | True peak | LRA |
|---|---|---|---|
| Emu_Savasi.mp4 | −14,1 | −4,0 dBTP | 2,0 LU |
| Titanik_Kehaneti.mp4 (kadın sürüm, varsayım) | −14,0 | **−0,9 dBTP** | 3,0 LU |
| Titanik_Kehaneti_erkek.mp4 | −14,1 | −2,0 dBTP | 2,9 LU |

Kodda (`emu-savasi/audio.py` satır 188–193, 296–301, 320–330; Titanik'te duck satırı 260) ducking en çok 0,30 çarpanıdır (−10,5 dB). Master tavanı −6 dBFS örnek tepesidir ve tanh yumuşak diz kullanır. Sonuçlar:
- Titanik kadın sürümü benim ≤ −1 dBTP kuralımı 0,1 dB farkla aşıyor.
- qa.py ve audio.py WAV ölçüyor, yayın dosyasını ölçmüyor.
- LRA 2–3 LU, miks çok sıkıştırılmış. Konuşma yumuşak diz doygunluğuna giriyor olabilir; dinlemeyle doğrulanmadı.

**Tur 2 sorularına cevaplarım (Anayasa maddesi):**
- **Ses (S3):** Sabit kimlik erkek, yankı 0. Kadın dönüşümü şu koşulların hepsini sağlarsa geçer: kör A/B, aynı −14 LUFS, telefon hoparlörü (%50) ve kulaklık; n=5; ≥4/5 tercih; ≤1/5 "robot"; 6 yabancı adı yazdırma testinde erkekten kötü değil; s/ş/ç netliği dinlemede bozuk değil. Yankı için R1'deki "<%15 kabul" yedeğimi geri çekiyorum. Mevcut etkin ıslak pay %13,6 (Ek 4), yani eski yedeğim bugünkü hatayı onaylardı. Yeni tavan: anlatıda etkin ıslak pay 0; 3/5 yankıyı seçerse en çok %5.
- **Ses kapısı:** otomatik kısım (kodlanmış mp4'te −14 ±1 LUFS, ≤ −1 dBTP, ilk/son örnek tık ve DC kontrolü) ~30 sn sürer. İnsan kısmı tek dinleme, telefon hoparlörü %50, anlaşılmayan kelime hedefi 0, ~3 dk. Toplam kapı bütçesi 10 dk (qc) içinde ses payı ≤4 dk. Zorunlu kapılar: ses, Türkçe (dil), kaynak (olgu). Diğerleri öneri.
- **Müzik (muzik ile ortak):** konuşma sırasında müzik+efekt kısa-süreli LUFS'u konuşmadan ≥16 dB aşağıda; 14 dB altı QA hatası. Ducking çarpanı 0,70'ten 0,85'e (≈ −16 dB). Kalibrasyonu muzik'in Whisper+5 kişi testi yapsın.
- **Süre (S2):** 96 BPM'de 1 ölçü = 2,5 sn, yani 10/12/16 ölçü = 25/30/40 sn. Ses motoru hangisini seçerseniz uyar; ses açısından süre kararı serbest.
- **Kanca (S6):** kare 0'da tek vuruş ≤0,25 sn, ilk sesli kelime 0,35–0,5 sn. Vuruşun kuyruğu konuşmanın ≥20 dB altında.
- **Sürüm künyesi:** ses yapılandırma hash'i, Piper/pyworld/pyloudnorm sürümü ve ölçüm raporu videoyla kaydedilir.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| seslendirme | "≤%10 ıslak karışım" tavanı | Disagree | Etiket belirsiz, dosyadaki yanlış "%8,5 kuru" hatasının aynısı. Etkin kazançla yaz; anlatıda 0. Kör test eşiğine (≥4/5, ≤1/5) katılıyorum. |
| muzik | Konuşmanın 18–20 dB altı | Partly disagree | Telefon hoparlöründe 150 Hz altı yok. Yatak o kadar derine inerse duyulmaz ve yalnız maskeler. 16 dB'de başla, testle ayarla. Kare ızgarasına ve 3. sn girişine katılıyorum. |
| qc | "qa.py yeşil + insan imzası" | Agree, düzeltme ile | Ek 9'a göre LUFS qa.py'de değil. Kodlanmış mp4 ölçümü kapıya girmeli; Titanik −0,9 dBTP bunu gösteriyor. |
| seytan | Kadın sesi 14 günlük pencerede yok | Disagree | Kör test yayın değil, 1–2 saat; yayınlanan kanal değişmez. Yayına girmeyi erteleyin, ölçmeyi değil. Mevcut sesler zaten donmuş değil (Emu yeniden seslendirildi). |
| izleyici | Adlarda WER ≤%5, sıfır hata | Disagree | Ek 5: Whisper hatası TTS hatasından ayrılamıyor. Adları insan kulağı ve 6 adlık yazdırma testi denetlesin, ASR yalnız yardımcı. |
| pipeline | 3 günlük tampon, sürüm künyesi | Agree | Tampon ses ölçümüne zaman kazandırır. Künyeye ses hash'i ve ölçüm raporunu ekleyin. |

## 3. Corrections accepted or disputed

- **Ek 4 (yankı etiketi):** kabul. R1'de bunu şüphe olarak yazmıştım; kod okuyunca etkin ıslak pay 0,085×1,6 ≈ %13,6. Kadın sürümde 0 ve ölçülen kuru ses ayrıdır.
- **Ek 5 (Whisper %20):** kabul. WER kapı değil gösterge; yeni adlar için kulakla dinleme.
- **Ek 9 (bayat QA, LUFS yeri):** kabul, ölçümümle genişletiyorum: kodlama sonrası tepe değeri kimse ölçmüyor.
- **Dispute yok.** R1'deki "tık sesi riski"ni de düşürdüm: `master()` 2 ms fade-in ve 30 Hz yüksek geçiren uyguluyor, son 0,1 sn sessiz. Hâlâ otomatik denetlenmeli.

## 4. What would reverse this vote

- Kör testte yankılı sürüm ≥3/5 tercih edilirse yankı tavanını gevşetirim; oy aynı kalır.
- Seçenek A'ya (dondur ve ölç) dönerim, eğer kodlanmış mp4'ü ölçüp düzeltmek ve kör testi yapmak ilk 3 günde bitmezse. Günlük koşunun ses kapısını aşındırdığı görülürse (tampon 1 güne iner ve ses dinlemesi atlanırsa), yazılı otomatik geçiş zaten haftada 3–4'e düşer.
- Telefon hoparlöründe dinlemede mevcut miksin sorun çıkarmadığını görürsem ducking ve tavan değişiklikleri iner; oy aynı kalır.

## 5. Dissent to record

Seçenek düzeyinde yok. Ses kapısı için kayda geçsin: sıklık, cilt sayısı ve süre pazarlık konusu; kodlanmış dosyada −14 ±1 LUFS, ≤ −1 dBTP, anlatıda yankı 0 ve tek dinleme pazarlık konusu değil. Bu kapı "zaman yok" diye düşerse kanal, bugün Titanik'te olduğu gibi, kimsenin ölçmediği bir ses sorunuyla yayına çıkar.
