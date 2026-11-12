# Genel değerlendirme: Milton, *Kayıp Cennet* ve Şeytan

## Ne çıktı
- 25:46'lık film: 139 cümlelik senaryo, 142 plan (+ 13 ek çekim), kodla çizilen özgün gravür üslubu, özgün müzik, Emrullah sesi, 384 altyazı.
- İki kapak, yayın metinleri, yayın talimatı. Shorts ve İngilizce dublaj yapılmadı.

## Kurul kapılarının dürüst dökümü
| Kapı | Sonuç |
|---|---|
| Senaryo | **Geçti** (tur 3: beş üye 9,03–9,38) |
| Üslup karesi | Geçmedi sayıldı: teknik 9,0; sanat 8,35; gravür 8,45 (altı tur). Üç üye "dil doğru, engelleyen bulgu yok" dedi; kalan değerlendirme hareketli sahneye taşındı |
| Kapak | A **geçti** (iki üyeden 9,0). B 9,0 ve 8,9 (eşiğe 0,07); ikinci test seçeneği |
| İlk tam kurgu | **Geçmedi; tek tur yapılabildi.** On üye 7,0–8,85 verdi (tipografi 7,3; altyazı 8,5; kaynak 8,85; hassasiyet 7,8; hukuk 8,8; tutma 7,6; ilk kez gören izleyici 7,0; kurgu 7,7; animasyon 7,8). Bulguların neredeyse hepsi uygulandı, ama **düzeltmelerden sonra gerileme turu yapılmadı**; sanat/gravür ve teknik/erişilebilirlik üyeleri bu kapıda hiç toplanmadı |
| Ses ve miks, son render, yayın paketi | Kurul toplanmadı. Miks ölçümle hedefte (−14 LUFS); kulakla onay kullanıcıda |

Yani "her aşama ≥ 9" kuralı senaryo ve ana kapak dışında tutturulamadı. Son filmdeki düzeltmeleri yalnız başkan (ana oturum) kare kare kontrol etti. Yeni oturumda ilk iş, güncel filmle aynı üyelere gerileme turu yaptırmak olmalı (üye kimlikleri ve raporları `kurul/kurgu_tur1/`).

## İşe yarayanlar
- **Orkestra düzeni (kullanıcının istediği):** ana oturum yönetmen ve başkan; her sahne setinin tek sahibi olan bir çizim ajanı (aynı ajan, turlar boyunca `SendMessage` ile sürdürüldü); kurul üyeleri ayrı ajanlar. Sahiplik ve süreklilik sayesinde düzeltme turları hızlı ve tutarlı oldu. Sonuç iyi; kalıcı yöntem olarak kaydedildi (kök `CLAUDE.md`).
- **Bütün filmi tek bakışta görmek** (`tools/kurgu_ozet.py`: her plandan bir kare). En büyük kalite sıçraması, başkanın kurula gitmeden bütün filmi yan yana görüp altı bölgeyi yeniden çizdirmesiyle geldi (kanca, cennet, savaş, Pandemonium, Nifates, son kare).
- **Bağımsız üyeler başkanın görmediğini gördü:** namaz safı gibi okunan selam, çarşaflı kadın gibi okunan Günah figürü, vaaz motifiyle çakışan "ŞEYTAN AĞLADI" yazısı, Kutsal Kalp tasvirine yaklaşan kapak, haç gibi okunan yıldız, Dor sütunlu cennet sarayı, bağışlanma sahnesindeki Şeytan. Bunların hiçbiri teknik hata değildi; hepsi yayından sonra sorun çıkarırdı.
- **Geri çağrı omurgası:** açılış karesi (soru) → 12:10 (itiraf) → 24:00 (zincir, cevap) → son kare (şairin içindeki ışık, ayna). Kapak A ile ilk kare aynı figür.
- **Kelimeye bağlı zamanlama:** her olay bir kelimeye bağlı; ses değişse görüntü kendiliğinden kayar. Animasyon üyesinin en çok övdüğü yan.

## İşe yaramayanlar ve dersler
- **Üslup kararı pahalıydı.** Gravür taraması kodla güzel duruyor, ama figür (yüz, el, beden) bu motorun zayıf yanı. İç çizgisiz beyaz figürler "kâğıt kesme/manken" okundu ve cennet ile savaş baştan çizildi. Ders: yeni üslupta ilk üslup karesi yalnız manzara değil, bir **orta plan figür** ve bir **yakın plan** da içermeli.
- **Tek durağan karede 9 almak gerçekçi değildi;** altı tur harcandı. Ders: üslup kapısı tek kare + 15 sn'lik hareketli sahne olarak kurulmalı.
- **Levhalar (yazı sayfaları) filmin dörtte biriydi** ve kurulun en çok eleştirdiği yer oldu ("PowerPoint hissi"). Ders: senaryoda deneme bölümleri için baştan görüntü fikri yazılmalı; levha, plan başına en çok 8 sn.
- **Aynı kadrajın tekrarı.** Sahne ajanları bir seti kurunca aynı kadrajı çok kullandı. Ders: plan listesinde her plana ölçek (geniş/orta/yakın/ayrıntı/ters açı) yazılmalı; ardışık iki plan aynı ölçekte olmamalı.
- **Yumuşak geçiş gravürde gri üretir.** Motor artık iki levhayı karıştırmayan eşik geçişi kullanıyor ve aynı mekânda kesiyor.
- **Kullanım sınırı dört kez doldu.** Aynı anda en çok üç ajan kuralı sonradan kondu; son turlar ikişer ajanla yürüdü. Ders: baştan ikişer ajan; büyük modeli yalnız çizim ve hassas kurul işlerine, küçük modeli ölçüm ve metin işlerine vermek.
- **ElevenLabs kredisi üretim ortasında bitti;** iki çekim sonradan üretildi. Ders: üretimden önce karakter sayısı × çekim sayısı hesaplanıp kullanıcıya bildirilmeli.

## Bilinen zayıflıklar (son filmde)
- İlk kez gören izleyicinin "9–12 dakika izlerim" tahmini düzeltmelerden sonra sınanmadı.
- Baş-omuz yakın planları beş kez aynı profil figürü; güneş diski başın arkasında hale gibi okunabilir (hassasiyet üyesine gösterilmedi).
- "Sıradan melek" (G05) ve ordunun üçte biri (C08, "konfeti") anlatım olmadan okunmuyor.
- Pandemonium geniş planlarında koyu oran hedefin üstünde; selam dalgası telefonda zor seçiliyor.
- 21:15'teki "Generalden" sözü iki çekimde de Whisper'a "genelden" gibi geldi; kulakla kontrol edilmeli.
