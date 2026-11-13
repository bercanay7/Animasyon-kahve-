# Prometheus: müzik planı

Sentez yoluyla özgün müzik: `audio/score.py` (numpy/scipy). Sisifos'un çalgıları yeniden kullanılır (lir/kithara, aulos, yaylılar, koro, çerçeve davul, keçeli piyano), ama düzenleme ve motifler yeni.

## Katmanlara göre ses rengi (görüntüdeki üç vazo tekniğine eşlik eder)
| Katman | Görüntü | Müzik |
|---|---|---|
| Hesiodos, tanrıların soyu | siyah figür | Lir ve çerçeve davul. Rapsodun anlatısı gibi, epik. D Dorian. |
| Aiskhylos, oyun | kırmızı figür | Aulos (tragedya korosunun çalgısı), alçak yaylı bordon, zincir metali. D Frig, karanlık. |
| Erhat, modern okuma | beyaz zemin | Keçeli piyano ve yumuşak yaylılar. Sıcak, düşünceli. "Özgürdür"de D majör / Lidya. |

## Motifler
- **Ateş (Prometheus):** D–A–C–D. Beşli sıçrama, ardından küçük yedili üzerinden oktava. Önceden düşünen, ileri atılan bir çizgi. Açılışta aulos tek başına söyler.
- **Zincir (zorbalık):** D–C♯–C–B♭–A, inen kromatik dörtlü (ağıt basın kalıbı). Alçak yaylılarda, zincir metal tıkırtılarıyla.
- **Üç taht:** her taht devrilmesinde bir ağır davul darbesi (bum). Üçüncü darbe film boyunca bekletilir: D11'de ("Sıra kime gelecekti?") vurmaz, sessizlik olur. I06'daki görüntüde yalnız yankısı duyulur. J04'te zincir motifine dönüşür.
- **Doruk (J04, "Gerçekte Zeus köle… Prometheus özgürdür"):** zincir motifi tersine döner, inen dörtlü çıkan ateş motifine dönüşür. Söz anlam olarak orada döner.

## Bölümler (süreler `audio/cues.md`'den)
- **Açılış:** sessiz giriş, tek alev çıtırtısı. A01'de aulos ateş motifini söyler, A02 çekiç darbesinde zincir. A03 kartal: yaylı tremolo, kanat sesi. A04 "Prometheus": koro tek akor.
- **I–II (Erhat'ın sorusu, taht kavgası):** piyano → lir. Devrimlerde taht darbeleri. Titanomakhia'da savaş davulu (Sisifos'un Ares davulu yeniden düzenlenir).
- **III (dinmez öfke):** karanlık yaylılar. D11'de üçüncü darbe beklenir ama vurmaz, sessizlik.
- **IV (Mekone):** lir ostinatosu, kurnaz ve alaycı (Sisifos'un "kurnaz kral" ritim dili). Rezene sahnesinde ateş motifi tam hâliyle.
- **V–VI (duruşma, savunma):** aulos ve bordon. Çekiç darbeleri ses efektiyle senkron. F13'te "sayısız gülüş"te lirle su pırıltıları. F14'te müzik çekilir.
- **VII (tanıklar):** Okeanos sahnesi hafif. İo'da atsineği vızıltısı ve aulos kovalamacası.
- **VIII (sır):** Hermes için hızlı pizzicato. "Eyvah"ta kesik.
- **IX (zincirin öbür ucu):** donma, yalnız bordon. J04'te doruk.
- **X (fırtına):** gök gürültüsü ve davul, bütün çalgılar. I12'nin sonunda sessizlik, ardından tek aulos.
- **XI (Herakles → Oppenheimer):** lampadedromia koşusu için çerçeve davul ritmi. Oppenheimer'da beyaz gürültü ile kesik.
- **XII (başkaldıran yaratık):** piyano ve koro. K06'da ateş motifi D majörde tamamlanır.
- **XIII ve bitiş ekranı:** lir. Sisifos'un kaya motifi bir kez anılır (seri bağı); bitiş ekranı boyunca alev çıtırtısı.

## Miks
Sisifos'taki gibi: konuşma altında spektral kısma, önemli cümlelerde daha derin (PRIORITY). Hedef -14 LUFS / -1 dBTP. Fısıltı etiketli cümleler (F14 "Ama ne diyorum?") +6 dB.
