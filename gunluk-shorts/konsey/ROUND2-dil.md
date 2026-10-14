# ROUND 2: Türkçe dil editörü (dil)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** no
**Confidence:** medium

## 1. Vote and reason

C: B'nin tamamı (sabit iskelet, en çok 3 cilt, tek kuru ses, kapılar), ama haftada 5 video ve 3 günlük tampon. Tur 1'deki "hibrit + tek ses + Türkçe kapı" tutumumun sürdürülebilir hâli; harf olarak B'ye değil C'ye kayıyorum çünkü dil hatasının asıl ilacı zamandır, kod değil. Aynı gün yazılıp yayınlanan metni yazarından başka kimse okumamıştır; tampon "ertesi sabah ikinci okuma" penceresi verir (çıkarım; kanıtı, tampon kurulunca yakalanan hata sayısı).

**G sorularına yanıtım (Anayasa'ya girmesi için):**
- **Kapı (Soru 4):** Türkçe kapı zorunlu, bütçe ≤ 8 dk/video. Beş kural: (1) ekran metni ile okunuş ayrı; sayı/yıl harfle yazılır (kodda `göster=söylenen` zaten var). (2) Sözlükte olmayan her özel ad ve her ğ'li ya da sert ünsüz yığınlı sözcük için 10 sn kulak kontrolü; sözlük girdisini Whisper değil insan kulağı onaylar. (3) Video başına ≤ 3 sayı, aralık 2 sayı sayılır, sesli aralık "X ile Y arası". (4) Cümle ≤ 14 kelime. (5) Sözlük anahtarları Türkçe-duyarlı küçük harfle aranır. 8 dk'yı aşan kapı olursa o kural otomatikleştirilir ya da öneriye iner.
- **Kanca (Soru 6):** ekran metni ≤ 7 kelime ve ≤ 40 karakter, ≥ 64 px; "≤ 4 kelime" (retention) Türkçede ek ve edatı atıp telgraf dili yaptırır. İlk sesli cümle ≤ 10 kelime. Vaat denetimi: kancadaki her sayı ve yargı sözcüğü ("kehanet", "tek", "en") video metninde karşılık bulur; bulmazsa dil ve olgu birlikte reddeder.
- **Ses (Soru 3):** erkek kuru ses sabit. Kadın dönüşümü ancak kör testte ≥ 4/5 tercih, ≤ 1/5 "robot" ve s/ş/ç/z netliği işaretli ise geçer. Test metni üç sese de aynı sözlükle verilir.
- **Süre (Soru 2):** ölçtüm: Emu 92, Dans 78, Titanik 77 ekran sözcüğü (`*/tts.py` SENTENCES, 40–43 sn). Senarist'in 95–110'u bu hızın üstünde. Tavan: 40 sn için ≤ 90, 25–32 sn için ≤ 65 sözcük.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| sesmuh | "WER adlar hariç ≤ %10" | disagree | Adları dışarıda bırakan ölçüt hatanın yaşadığı yeri gizler. Adlar ayrı raporlanır, sözlükteki adlarda 0 hata. WER yalnız tarama aracıdır, kapı değil. |
| seslendirme | Kör test, ≥ 4/5, adı yazdırma | agree, with change | Testin ses ölçtüğünden emin olmak için ad hatası önce sözlükle sıfırlanmalı. Yoksa "robot" yargısı yanlış okunan adı da kapsar. |
| retention | İlk karede ≤ 4 kelime | disagree | Mevcut Titanik kartı 5 kelime ("TİTANİK'TEN 14 YIL ÖNCE YAZILDI"), 4'e inince ek düşer. ≤ 7 kelime / ≤ 40 karakter öneriyorum. Karşı kanıt: izleyici testinde 7 kelimelik kartın 2 sn'de okunmaması. |
| olgu | Çelişkili sayıda aralık söylensin | agree, with change | Doğru ama sesli "38–45" ağırdır. "Otuz sekiz ile kırk beş dakika arası" bir kez, tam aralık sabit yorumda. Aralık sayı bütçesinden 2 düşer. |
| senarist | Yabancı ad bütçesi, 95–110 kelime | agree / disagree | Ad bütçesine katılıyorum. 95–110 ölçülen 77–92'nin üstünde; Emu'daki 15 kelimelik cümle (J) zaten sınırı aşıyor. |
| pipeline | Tek ses dosyası + sözlük, sürüm künyesi | agree | Sözlüğü ses yapılandırmasına bağlamak şart; sözlük sürümü videoyla kayda girsin. |

## 3. Corrections accepted or disputed

- **Ek 05 (WER sınırı): kabul, daha da ağır.** `ses-lab/check_voice.py` referans olarak `show` metnini kullanıyor, `say`'i değil; sözlükle düzeltilen ad ("Futility=fyutiliti") ölçümde hata sayılır. Ortalama cümle başına WER'in ortalamasıdır, kısa cümleler ağır basar.
- **Ek 11 (video metinleri yok): daraltıyorum.** Metinler `*/tts.py` içinde var; okudum.
- **Kendi Tur 1'imden geri çekilenler:** (a) "Sözlük yok": mekanizma var (`lex.json`, `LEX`), ama tek girdi var ("yığılanlar"). (b) "Normalizasyonsuz WER": `asr.py` rakamları harfe çeviriyor ve İ'yi ele alıyor; bu iki itirazım zayıflar. (c) "Büyük harf riski": depoda `.upper()` çağrısı bulunmadı (grep); risk yalnız ileride otomatik büyük harf eklenirse. Aynı yerde gerçek bir hata var: `narrator.py` `core.lower()` kullanıyor; `'İstanbul'.lower()` ve `'Isparta'.lower()` Türkçe karşılığa eşit değil (`python3 -I` ile denendi), yani İ/I ile başlayan sözlük girdileri sessizce eşleşmez.
- **Yeni bulgu (kod okuması):** `lexsearch.py` yazımı "Whisper'ın en iyi anladığına" göre seçiyor, kulağa göre değil. Hedef listesinde "çılgınlık", "sahne", "histeri", "zehirlenmesi" gibi sıradan sözcükler var. Sorun yalnız yabancı ad değil; ğ ve ünsüz yığını da (hata kaynağı Whisper mı Piper mı, ayrılamıyor).

## 4. What would reverse this vote

- Kapı, tampon varken bile ≤ 8 dk'yı aşarsa C yerine E'ye (haftada 3–4) giderim.
- Tampon kurulur ve ilk 14 günde ikinci okumada hiç hata yakalanmazsa B'ye dönerim (tampon gereksiz).
- Gerçek izleyici testinde mevcut ifade tarzı (kısa, telgraf kanca) benim kuralımdan daha çok anlaşılırsa kanca kuralımı gevşetirim (kartımdaki koşul).
- 40 öğelik telaffuz sınavında sözlüksüz ad hatası ≤ %5 ve yıl/sayı %100 çıkarsa kapı "öneri"ye iner.

## 5. Dissent to record

B çoğunluk seçeneği ve günlük yayını koruyor. Benim itirazım: hata türü sessiz ve yoruma dönüşmeyen bir hata (izleyici kaydırır). Aynı gün yazılıp yayınlanan metni yazarından başka kimse okumaz. "10 dakikalık kapı" bir kontrol listesidir, okuma değildir. Haftada 5 ve 3 günlük tampon, yayın ritmini kaybettirmeden bu okumayı mümkün kılar; günlük hız ise kapıyı aşındıran ilk baskıdır. Büyüme kaybı (buyume, kanca) gerçek ama ölçülmemiş.
