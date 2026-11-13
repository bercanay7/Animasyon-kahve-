# ROUND 2: Algoritma ve analitik uzmanı (analitik)

**Read:** ROUND1-TALLY.md, ADDENDUM-01A.md, DOSSIER-01, VERIFICATION.md ve 21 Tur 1 raporu (ROUND2 dosyalarına bakılmadı).

**Vote:** A
**Changed from round 1:** no
**Confidence:** medium (süreç için yüksek; "hangi cilt/ses doğru" için düşük)

## 1. Vote and reason

A, ama tally'deki hâliyle değil, ölçüm kurallarıyla sıkılaştırılmış hâliyle. Gerekçem tek: şu an elimizde 4 video ve birbirine karışmış 5 değişken var; B ve C ilk 14 günde cilt çeşitliliği ekleyerek bu karışıklığı sürdürür. (Ek 3'ün ilk kare ölçümü kanca hipotezinin önceliğini biraz artırdı, oyu değiştirmedi; bkz. bölüm 3.)

**Kanal Anayasası'na girecek somut kurallar (G soruları):**
- **G1 Cilt:** İlk 14 gün 1 cilt (seçim veriyle değil, yazılı kuralla; sonuç bakılmadan). Sonra tavan 3. Gerekçe (varsayım: videolar arası viewed% sd ≈ 8 puan, ölçülmedi): 90 günde haftada 5 video ≈ 64 video; 3 ciltte hücre başı ≈ 21, ayırt edilebilir fark ≈ 7 puan; 4 ciltte hücre başı 16, ≈ 8 puan. Tavan 4 kazanç sağlamaz. Yeni cilt, öncekiyle ≥5 videoda denendikten sonra ve her seferinde tek cilt eklenir.
- **G2 Sıklık/süre:** Ölçüm penceresinde haftada 5 kabul (14 gün ≈ 10 video; günlük 14 video, SE oranı √(14/10) ≈ 1,18: sıklık istatistiksel gerekçe değildir, kararı pipeline/qc versin). Süre penceresinde 40 sn ±3 sabit: ortalama izlenme % süreye bağlı olduğu için süre ayrı bir eksendir, kancayla birlikte oynamaz. 25–32 sn ayrı, sonraki test.
- **G3 Ses:** Erkek, kuru, sabit varsayılandır; değişiklik yükü kadın sesindedir. Kör test: aynı metin, rastgele sıra, telefon hoparlörü, −14 LUFS. 5 kişide "≥4/5 tercih" sadece veto filtresidir; şans eseri ≥4/5 olasılığı %19 (ikili seçimde). Geçiş için 8 dinleyicide ≥7/8 tercih (şansla ≈ %3,5) ve ≤1 "robot".
- **G4 Kapılar:** Kapı sonuçları (geçti/kaldı, dakika) günlüğe yazılır; kapı sürümü kilitlidir. Bütçe kararı qc/pipeline'ındır, ben yalnız kaydı şart koşarım.
- **G5 Ölçüt:** Birincil: "izlenenlere karşı kaydıranlar" (viewed %); ikincil: ortalama izlenme %. Pencere 48 sa (işaret) ve 7. gün (karar). Video, akışta gösterilme ≥300 ise analize girer (varsayım; altındaki "yetersiz maruz kalma" diye etiketlenir). Her ekran görüntüsü metrik adı ve tarihiyle saklanır (Ek 1: 24 Ağu 2026 sayım değişikliği UNVERIFIED).
- **Tasarım:** 14 günde tek eksen = kanca tipi (R: rakam/çelişki kartı; S: merak/soru kartı), tanımları ilk videodan önce yazılı. Konu türüne göre eşleşmiş çift; çiftte hangi videonun R aldığına yazı-tura karar verir. Ayırt edilebilir fark: 5 çift ≈ 14 puan, 10 çift ≈ 10 puan. Hüküm: 5/5 çift aynı yönde ve ortanca fark ≥10 puan; 4/5 yalnız "ipucu". 10 çiftte ≥9/10 (şansla %1,1) "etki var". Yani 14. gün kararı yön verir, hüküm 28. gündedir.
- **G7 İlk adım:** 4 videonun Studio dışa aktarımı (Shown, viewed %, ort. izlenme %, trafik kaynağı, yayın damgası). Emu–Dans viewed% farkı ≤10 puansa "dağıtım şansı" (E1 düşer); ≥25 puansa E1 desteklenir. Yeniden yükleme yeni videodur.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| artdir | "Cilt-konu eşlemesi" | **Disagree, sert** | Cildi konuya bağlamak, cilt ile konuyu mükemmel karıştırır (r=1): hangi etkinin hangisinden geldiği bir daha ayrılamaz. Cilt atamasını rastgele/ön kayıtlı yap, konuya göre değil. |
| retention | 40 sn → 25–32 sn, aynı pencerede kanca testi | **Disagree** | Süre ikinci eksen; ortalama izlenme % kısa videoda mekanik olarak yükselir. +10 puan eşiği de 7 video/kolda gürültü tabanında (≈12 puan). Sıralı: önce kanca, sonra süre. Haklı olduğu yer: ilk iş Studio verisi, "ham görüntülenme değil" ölçütü. |
| seslendirme | ≥4/5 tercih eşiği | **Kısmen** | Kör test ve yankı kapalı varsayılan doğru. Ama 4/5 şansla %19; kadın sesi için 7/8. |
| seytan | Haftada 4–5, tek değişken | **Agree** | Sıklık düşüşü örnek kaybı değil (yukarıdaki √ oranı); hakkı: günlük zorunluluk ölçmeyi bozmaz ama kaliteyi bozabilir. Yanlışı: "60. gün 2 kat medyan" hedefi gürültü içinde ölçülemez. |
| buyume | 7+7 konu bölmesi, ">%30 geri kalma" | **Kısmen** | 7+7 bölme ayrı bir eksen daha açar; çift tasarım daha güçlü. Engaged views/kaydıran oranı doğru ölçüt. |
| izleyici / kanca | 5 kişilik test, yazı-tura kanca | **Agree** | Kanca randomizasyonu tam benim istediğim; 5 kişi yön göstergesidir, kanıt değil. |

## 3. Corrections accepted or disputed

- **Ek 1 (metrik/sayım):** Kabul; F2'deki 1700/100 ham izlenme olabilir ve E1 üstüne kurulamaz. Ek 11: Studio verisi yok; "yok" değil "aranmadı".
- **Ek 3 (ilk kareler):** Kabul. Kancalı: Emu, Titanik; kancasız: Dans, Zanzibar. Bilinen sonuç yalnız Emu–Dans. Zanzibar ve Titanik sayısı gelirse 4 noktalı doğal karşılaştırma olur; ama dört cilt/ses farklı. Şansla "kancalı iki video tepede" olasılığı 1/6 ≈ %17: ipucu, kanıt değil.
- **Ek 9 (bayat QA):** Kabul; sürüm künyesi (hangi render, hangi ses, hangi QA) günlüğe girmeli, yoksa değişken izlenemez.

## 4. What would reverse this vote

(a) Emu/Dans viewed% farkı ≤10 puan ve Zanzibar ile Titanik tutma verisi de benzerse (kanca/konu yok): B/C'ye kayarım, çünkü dondurmanın öğrenme getirisi küçük çıkar. (b) Gerçek izleyici testinde (≥8 kişi) aynı iskelette farklı ciltlerin viewed% (veya 2 sn anlama) farkı tutarlı biçimde ≥10 puan çıkarsa cilt çeşitliliği ölçülmüş demektir. (c) Kullanıcı 14 günlük cilt dondurmasını reddederse "iki cilt, rastgele atama" tek analitik açıdan kabul edilebilir sapmadır.

## 5. Dissent to record

17 üye cilt çeşitliliğini ilk günden savunuyor; gerekçeleri (estetik, üretim, okunabilirlik) birbirinden bağımsız ama hiçbiri bu kanalda ölçülmüş bir veriye dayanmıyor. Çeşitlilik tercihi meşrudur; ben tek şeyi kayda geçiriyorum: ilk 14 günde cilt değiştirmek ve ilerleyen günlerde cilt-konu eşlemesi yapmak, 90 günün sonunda bile "ne işe yaradı?" sorusunu yanıtsız bırakır. Yanıtsızlığın bedeli videoların değil, bir sonraki üç ayın kararlarının bedelidir. Dondurmanın kendi riski gerçek (yanlış kimliği erken kilitlemek, yaratıcı yorgunluk); bunu azaltan şey kilidi geri alınabilir tutan yazılı günlük ve 28. gündeki ön kayıtlı hükümdür.
