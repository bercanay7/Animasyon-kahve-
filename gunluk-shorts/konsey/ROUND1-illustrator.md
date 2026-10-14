# ROUND 1: Karakter ve illüstrasyon sanatçısı (illustrator)

**Dossier:** DOSSIER-01-kanal-yonu.md. **Addenda read:** yok (ADDENDUM-01*.md aranıp bulunamadı; klasörde bu adla dosya yoktu, yani "yok" değil "bu aramada bulunamadı").
**Round 1, independent:** no other member's report was read before this one was written.

**Position:** C (hibrit) ama dar: şekil dili, silüet kuralları ve küçük bir tekrar eden kadro SABİT; "cilt" (kara kalem, kâğıt kesme, blueprint) yalnız ortak vektör sahnenin üstüne giydirilen en çok 3 işleme geçidi olsun. Her gün sıfırdan yeni çizim dili (A) kabul etmem.
**Confidence:** medium (stil kuralı için orta; "hangi ciltler tutuyor" için düşük, çünkü veri yok)

## 1. Position and why

1. **Koltuğumun ölçütü okunabilirlik ve duygu; stil değil.** Bir çizim 360 px genişlikte (1080 px çıktının telefonda 3 kat küçük hali), 1 sn'de "bu kim, ne yapıyor" demiyorsa estetik değeri sıfırdır. Bu açıdan stil çeşitliliği benim için bir hedef değil, bir risk: her yeni stil, silüeti yeniden öğretmek demek.
2. **Sabit silüet sözlüğü ucuz, sabit stil pahalıdır.** Karakteri (Kurye, kalabalık, askeri, hayvan) bir kez tasarlayıp geometrik temel şekillerle (daire, trapez, dikdörtgen) vektör olarak tutarsak, kara kalem / kâğıt kesme / blueprint bir işleme geçidi (gürültü + kenar sapması, kenar kaydırma + gölge, yalnız çizgi) olur. Böylece yeni video = yeni sahne düzeni, yeni çizim motoru değil. Bu pipeline'ın "çok stil = çok bakım" itirazını da azaltır (tahmin, aşağıda).
3. **Tamamen farklı stil, kod tabanlı çizimde karakterin ölüm yeridir.** Pillow ile kemik animasyonu yok; jest kısıtlı. Stil değişince karakterin jestlerini her seferinde yeniden kurmak gerekir; zaman çizime değil, "tutarlılık tamiri"ne gider. Sonuç, ayrıntı artıp ifade azalır: tam kaçınmak istediğim şey.
4. **Kullanıcının "her video farklı" isteğini kısmen karşılarım.** Love, Death & Robots benzetmesinin hakkı: konuya göre cilt değişsin (Titanik = blueprint doğal, Dans = kâğıt kesme uygun). Ama iskelet (kanca kartı, HUD, ilk karedeki ana nesne ve karakter oranı) sabit.
5. **Kaybım:** tek tek videolarda sanatsal özgürlük; en güçlü ve en tuhaf stil denemeleri. **Kazancım:** her çizimin amacı belli ve okunur olur.

## 2. Where the dossier is wrong, incomplete or mis-posed

- **Stil, ses ve konu karışık (confound).** Emu (kara kalem, seslendirmeli, 1700) ile Dans (kâğıt kesme, 12 fps, 100) karşılaştırması, stil + konu + kanca + ses sürümü + yayın zamanı aynı anda değişmiş karşılaştırmadır. E1 "konu ve kanca" diyor ama stil/akıcılık (24 fps karşılık 12 fps) listede yok. Dans'ın 12 fps stop-motion hissi, Shorts beslemesinde "takılıyor" gibi okunmuş olabilir. **Tahmin, doğrulanmadı.**
- **Eksik bilgi: kare görselleri.** Dosyada hiçbir videonun ilk karesi / 2. saniyesi / küçük boyutlu görünümü yok. İllüstrasyon kararını görmeden veriyoruz. F7 "kare görseliyle yeniden doğrulanmadı" diyor; yani en kritik karelerin kendisi masada değil.
- **C seçeneği kötü tanımlı.** "Değişen illüstrasyon cildi" ya yalnız renk/doku filtresi mi, ya baştan yeni çizim kodu mu? İkincisi A'nın pahalı hali. Doğru soru: "Ortak sahne grafiği (scene graph) + kaç işleme geçidi?"
- **Eksik seçenek: sabit kadro.** Seçenek listesinde tekrar eden bir kahraman/mascot (Kurye) yok. Kanal adı "Zaman Kuryesi" zaten bir karakter fikri taşıyor; hiçbir seçenek bunu kullanmıyor.
- **F1: Zanzibar seslendirmesiz.** Sesin yokluğu ile stilin etkisi ayrışmıyor; bu video stil karşılaştırmasında dışarıda tutulmalı.
- **Dosyada bulamadım (yok demiyorum):** hangi videonun hangi çizim yönteminin (düz illüstrasyon, kömür, kolaj, blueprint) sahne başına kaç ayrı çizim nesnesi gerektirdiği. F5 "yeni sahne kodu gerekir" diyor ama süre dağılımı yok.

## 3. Evidence

| Claim | Type | Source or method |
|---|---|---|
| 4 videonun 4 farklı stili var, ikisinin izlenmesi biliniyor (1700, 100) | fact | Dossier F1, F2 |
| Emu–Dans farkını stil açıklamaz/açıklar kararı verilemez; n=2, çok değişken | estimate | Dossier E1; karşılaştırma tasarımı (confound sayımı: konu, stil, fps, kanca, yayın zamanı en az 5) |
| 1080 px çıktı telefonda ~360 px'te görünür; 3 px görünür çizgi için ≥9 px stroke gerekir | estimate | Basit ölçek hesabı (1080/360 = 3); telefon boyutu varsayımı |
| 12 fps, 24 fps akışta daha takılgan okunabilir | assumption | Genel animasyon bilgisi; kanal verisiyle sınanmadı |
| Ortak vektör sahne + işleme geçidi modeli Pillow/numpy ile mümkün | estimate | Pillow'da maske + gürültü/ofset/gölge; bu hatta denenmedi, prototip gerekli |
| Silüet okunabilirliği tutmayı etkiler | assumption | Retention verisi yok |

## 4. Risks from this seat

- **A (hiçbir şeyi değiştirme):** sessiz risk, kalabalık ve ayrıntılı sahnelerin 360 px'te okunmaması; günlük hız baskısıyla stil kalitesi "yarım" kalır. Kanalı kimse "kötü" demez, sadece kaydırır.
- **B (tam sabit kimlik):** tek stil yanlış seçilirse tüm ilk videolar farklı görünür ve geri dönüş zor; ayrıca blueprint gibi dar bir stil her konuya uymaz (Emu'yu blueprint ile anlatmak zor).
- **C:** işleme geçidi sahne kompozisyonunu bozarsa (kara kalem gürültüsü küçük nesneleri yutar) okunabilirlik düşer; bunun sessiz hali "güzel ama ne olduğu anlaşılmıyor".
- **D/E:** E (haftada 3–4) çizim kalitesi için en iyisi ama büyüme ölçütüyle çatışır; D'de stili bir deney değişkeni yaparsak kanalın kendisi bozulur.

## 5. The cheapest decisive step

**Adım (1 saatten az, ek video yok):** 4 videonun her birinden 3 kare (0. sn, 2. sn, ortada bir sahne) 270×480 px boyuta indir; ilk kare için ayrıca bulanık (blur) sürümü yap. 5 kişiye (arketip izleyiciye benzeyen, konuyu bilmeyen) göster, tek soru: "Bu karede ne oluyor / kim kim?" Ölç: konuyu ve ana nesneyi doğru adlandırma yüzdesi, stil başına.
**Eşik (şimdiden):**
- Dört stilde de kare başına ≥4/5 doğru ise: silüet sorunu yok; stilin sabitlenmesi için ben baskı yapmam, konu/kanca/ses odaklı kararlara oy veririm (pozisyonumu A'ya yaklaştırırım).
- Yalnız Dans veya Zanzibar'da <3/5 ise: o iki stil "yasaklı" olur (kâğıt kesme ve düz illüstrasyon yeniden onay ister); C'yi dar tutarım.
- Üç stilde <3/5 ise: B yönünde (tek sabit, okunabilir cilt) oy veririm.
Ayrıca Studio'dan Emu ve Dans için "ilk 3 sn kaydıran oranı" açılırsa, ilk kare okunurluğu ile eşleştiririm.

## 6. Conditions and red lines

C'yi şu koşullarla desteklerim:
- Ortak sahne grafiği ve en çok 3 işleme geçidi (kara kalem, kâğıt kesme, blueprint); dördüncüyü eklemek için önce bir video içinde okunabilirlik testi.
- 24 fps; 12 fps yalnızca ayrı "kasıtlı" sahnelerde, tüm videoda değil.
- Kabul etmem: konuyu anlatmayan dekor, 360 px'te okunmayan ince çizgi, ilk karede ana nesnenin kadrajın %30'undan küçük olması, güvenli alanın dışında yüz/jest.

**Kanal anayasasına önerilen maddeler (illüstrasyon):**
1. **Silüet testi:** Her sahnenin ana nesnesi siyah-beyaz 270×480 kareye indiğinde tek bakışta adlandırılabilmeli; geçemeyen sahne yayınlanmaz.
2. **Boyut:** Ana nesne/karakter yükseklik ≥ kadrajın %35'i; çizgi kalınlığı ≥ 9 px (1080 ölçeğinde).
3. **Sınırlı palet:** video başına en çok 4 renk + 1 vurgu; vurgu rengi hep kanca/HUD sayacında.
4. **Sınırlı jest:** karakter başına en çok 3 poz/ifade (bakış, korku, şaşkınlık gibi); karmaşık anatomi yok.
5. **Sabit iskelet:** kanca kartı, HUD (y≈260), Kurye imza nesnesi (köşede küçük sabit karakter/sembol) her videoda aynı.
6. **Cilt kotası:** 3 cilt; art arda iki gün aynı ciltten kaçınılmaz değil, ama yeni cilt eklemek için 1 haftalık okunabilirlik testi şart.
7. **Dekor yasağı:** her çizim nesnesi bir anlatı cümlesine bağlanmalı; bağlanmayan çizim silinir.

## 7. One line

Çizimi sade, silüeti sabit, kadroyu küçük tut; stili yalnız ortak çizimin üstüne giydirilen üç işleme geçidiyle değiştir ve ilk iş olarak mevcut karelerin 270×480'de okunup okunmadığını 5 kişiyle sına.
