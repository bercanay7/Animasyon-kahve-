# ROUND 1: Algoritma ve analitik uzmanı (analitik)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md aradım, klasörde bulunamadı; "yok" demiyorum, yalnızca bu klasörde bulunmadı).
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** n=4 ve her değişken aynı anda oynamışken hiçbir yön "kanıtlanmış" sayılamaz; önce 14 gün boyunca ses, iskelet ve görsel cildi DONDUR, ölçümü düzelt, yalnız konu türü ile kancayı sırayla değiştir; ses ve stil sorularını sonra, tek tek ve ucuz izleyici testiyle çöz.
**Confidence:** medium (süreç kararında yüksek, hangi yönün doğru olduğunda düşük)

## 1. Position and why

1. **Gözlem sayısı faktör sayısından küçük.** 4 video, 4 farklı stil, 3 farklı ses durumu (seslendirmesiz, ilk ses, yeni ses), 4 farklı konu, farklı kanca, farklı yayın günü. Bunlar tam karışık (confounded). Emu 1700 vs Dans 100 farkını konuya, kancaya, sese, stile, yayın saatine ya da şansa bağlayamayız. Bu koltuğun işi tam olarak bunu söylemek.
2. **17 kat fark "olağan gürültü" olabilir.** Shorts görüntülenmeleri ağır kuyruklu dağılır (varsayım: log-normal benzeri). Aynı kanalda aynı formatta 10–50 kat fark görmek yeni kanalda şaşırtıcı değil. n=1'e n=1 karşılaştırması ne ses ne stil hakkında bilgi verir.
3. **Gerçek etkiler küçük, 90 günde görülmesi zor.** Güç hesabı (bölüm 3): 2 kat etkiyi (ör. "ses X, ses Y'den 2x izlenir") ham izlenmeyle ayırt etmek hücre başına ~45 video ister. Günde 1 video ile 90 günde toplam 90 video var. Yani stil/ses A/B'sini ham izlenmeyle yapmak mümkün değil; daha az gürültülü ölçütler (kaydırma oranı, ortalama izlenme %) ve ucuz dışsal izleyici testi gerekir.
4. **Bu yüzden A ("hiçbir şeyi değiştirme") de, "her şeyi şimdi değiştir" de kötü.** A'nın kendisi her gün stil ve yankı ayarı değiştiriyor, yani sürekli ve kayıtsız bir deney; hiçbir şey öğretmez. Tam B (hepsini dondur) ise yanlış şeyi dondurmuş olabilir. Önerim C'nin zamanlı hâli: ilk 14 gün her şey sabit, yalnız bir eksen oynar.
5. **Kayıp tarafım:** Küçük kanalda hız ve sezgi de gerekir; mükemmel deney peşinde hareketsiz kalmak kendi kör noktam. Bu yüzden önerdiğim dondurma günlük yayını durdurmaz, sadece neyin değişeceğini sınırlar.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Seçenek D kötü kurulmuş.** "10–14 gün, aynı metin iki ses" iki sorun taşır: (a) aynı içeriği iki kez yayınlamak, ikinci yayının birinciden etkilenmesi (sıra/yorgunluk etkisi) ve yinelenen içerik riski; kontrolsüz. (b) 10–14 yayın = en fazla 5–7 video/hücre; ham izlenmede hiçbir şey ayırt etmez. Eşleştirilmiş tasarım ya da dışsal test gerekir.
- **F2'deki "izlendi" sayısı tanımsız.** Yayınlanma saati, ölçüm tarihi ve metrik (başlatma/tekrar sayımı mı, "engaged views" mi) belli değil. Aynı videonun 12 Ekim'deki ve 14 Ekim'deki sayısı yaşa göre farklıdır; Emu ve Dans'ı farklı yaşta karşılaştırıyor olabiliriz. Dans "çok az", sonra "100": ölçüm penceresi eşit değil.
- **F3 / yeniden yükleme sorusu eksik:** Emu yeniden seslendirildi. Yeniden yüklendiyse yeni video sayılır, dağıtım sıfırlanır; sadece sürüm değiştiyse başka. Dosya bunu ayırmıyor. Bu, "ses etkisi" yorumunu doğrudan bozar.
- **F7 doğrulanmamış** ("üretici ajanın hatırladığı kadarıyla"). Dans'ın ilk karesi için kanca kartı iddiası, kare çıkarılarak 1 dakikada kontrol edilebilir; hâlâ tartışma konusu yapılmış.
- **E7 kısmen kontrol edildi:** web aramasında (ikincil kaynaklar, resmî YouTube sayfası okunamadı) Shorts üst süresinin 3 dakikaya çıkarıldığı (Ekim 2024) ve görüntülenme sayımının 2025 Mart'ta başlatma/tekrar bazına kaydığı görülüyor; bir kaynak 2026'da yeni bir değişiklik iddia ediyor ama doğrulanamadı. Kanal 40 sn olduğu için süre kuralı bağlayıcı değil; sayım kuralı ise F2'yi yorumlamayı etkiler. Resmî yardım sayfası kontrolü doğrulayıcıya kalıyor.
- **Eksik değişkenler:** yayın saati, kanal yaşı, ilk dalga (test kitlesi) dağıtımı, kayıtlı yayın günlüğü yok. Ölçüt olarak ham izlenme seçilmiş; kaydırma oranı ve ortalama izlenme % birincil olmalı.
- **Zanzibar ve Titanik sonuçları bilinmiyor:** iki veri noktası daha var; "yalnızca iki sayı" bilgisi belki yarı kadar eksik. Sormadan yargı yok.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| 4 video ve 4 stil, 3 ses durumu, bağımsız değişkenler aynı anda değişti | fact | DOSSIER F1, F3 |
| Emu vs Dans = 17x fark, n=1 vs n=1 | fact | DOSSIER F2 |
| 2x etkiyi ayırt etmek için hücre başına ~45 video gerekir (log-sd≈1,2; α=0,05; güç 0,8) | estimate | n ≈ 2·(2,8·σ/δ)², σ=1,2 (varsayım), δ=ln2=0,69 → ≈47. 17x fark için δ=2,83 → ≈3 |
| Shorts izlenmeleri ağır kuyruklu, log-sd≈1–1,5 | assumption | Genel bilgi; kanalın kendi verisiyle test edilecek |
| Shorts üst süresi 3 dk (Ekim 2024); sayım 2025 Mart'ta değişti | fact (ikincil kaynak, resmî sayfa doğrulanmadı) | Web araması: socialmediatoday.com, async.com, piktochart.com özetleri |
| 2026'da yeni bir sayım değişikliği olduğu iddiası | assumption | Tek ikincil kaynak; doğrulanamadı |
| Studio'da "izlenenlere karşı kaydıranlar" ve trafik kaynağı var | assumption | Dosyanın kendisi (bölüm 6) söylüyor; ben arayüzü görmedim |

## 4. Risks from this seat

- **A:** Sessiz hata: her gün yeni stil ve yankı değişimi = ömür boyu karışık veri; 90 gün sonra hâlâ "neden" bilmeyiz. Görünür bir hata yok, bu yüzden tehlikeli.
- **B (tam dondurma):** Yanlış kimliği (ör. seslendirmesiz mi, kadın sesi mi) erkenden kilitleyebiliriz; geri dönüş ucuz değil.
- **C:** Cildi değiştirmeye devam edersek stil konudan ayrıştırılamaz; sessiz karışıklık yeniden girer.
- **D:** Küçük örneklemden büyük ders çıkarma; sonuç "kesin" gibi sunulursa en kötü hata budur.
- **E:** Sıklığı düşürmek örnek sayısını da düşürür; öğrenme hızı yarıya iner.

## 5. The cheapest decisive step

**Adım (maliyet ~30 dk, bugün):** YouTube Studio'dan 4 videonun her biri için aynı pencerede (yayından 48 saat sonra ve 7. gün) şunu dışa aktar: yayın zaman damgası, "izlenenlere karşı kaydıranlar" oranı, ortalama izlenme %, trafik kaynağı, görüntülenme; ayrıca her videonun ilk kareyi çıkar. Yanına 14 günlük yayın günlüğü başlat (konu türü, kanca tipi, ses sürümü, cilt, saat).
**Önceden karar:** Emu ve Dans'ın kaydırma oranı arasındaki fark ≤10 puan ise ve ikisi de Shorts akışı kaynaklıysa, 17x farkı "dağıtım dalgası/şans" sayarım ve "konu/kanca etkisi" (E1) tahminini düşürürüm: o durumda dondurma + daha çok örnek toplama. Fark ≥25 puan ve Dans'ın ilk karesinde gerçekten kanca yoksa, E1'i (kanca/konu) desteklerim ve ilk 14 günü kanca eksenine ayırırım. Eşik değerler varsayımdır, 4 videoluk veriyle ayarlanmamıştır.

## 6. Conditions and red lines

- Tek videodan "ses sorunu"/"stil sorunu" kesinliği yok (kırmızı çizgi).
- Aynı hafta içinde iki ekseni birden değiştirmek yok; ses sürümü değişikliği ayrıca kaydedilir.
- Yeniden yüklenen video yeni video sayılır, eski verisiyle birleştirilmez.
- Kararlar hücre başına en az 7 video ya da dışsal izleyici testiyle alınır; tek metrik ham izlenme olmaz.
- Destek koşulum: yayın günlüğü + sabit ölçüm penceresi (48 saat / 7 gün).

## 7. One line

İki videoyla karar verilmez: 14 gün her şeyi dondur, tek ekseni oynat, her yayını günlüğe yaz, 48 saat/7 gün penceresinde kaydırma oranına bak, ses ve stili ucuz izleyici testiyle ayrı çöz.

**Kanal anayasası için öneriler:** (1) Madde: Yayın günlüğü zorunludur. (2) Madde: Aynı anda tek eksen değişir. (3) Madde: Ölçüm penceresi 48 saat ve 7 gün, birincil ölçüt kaydırma oranı + ortalama izlenme %. (4) Madde: Yeniden yükleme yeni video sayılır. (5) Madde: Hücre başına <7 video ile "kazanan" ilan edilmez.
