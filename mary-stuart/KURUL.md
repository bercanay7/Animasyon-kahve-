# Mary Stuart ve I. Elizabeth: kurul kaydı

## Kurulsuz üretim (kullanıcının kararı, 18 Kasım 2026)
Kullanıcı: "Bu kurul olayını burada kullanmayalım. Sadece ihtiyaç duyduğun yerde Fable'ı bir danışman olarak kullanabilirsin." Bağımsız kurul toplanmıyor; kapılar başkan denetimiyle geçiyor, ≥9 eşiği bağımsız ölçülmüyor. Fable tek danışman olarak yalnız gerekli noktalarda: senaryo (kaynak/doğruluk + hassasiyet) ve paketleme.

| Kapı | Durum | Denetim |
|---|---|---|
| Talep kontrolü + paketleme taslağı | Kurulsuz | Başkan; otomatik tamamlama + Türkçe video izlenmeleri (`uretim_plani.md`) |
| Üslup | Kullanıcının kararı | İlk deneme (Milton gravürü) kullanıcı itirazıyla bırakıldı; `silent-film` + `archive-lighttable` örnekleri kullanıcıya gösterildi, onay alındı |
| Kaynaklar | Başkan | K01–K41 (birinci el metinler `kaynak/metin/`), Z01–Z10 (Zweig, çalışma alanındaki Almanca metinden) |
| Senaryo rev0 → rev1 | **Fable danışman** (tek tur) + başkan | Aşağıda |

## Senaryo: Fable denetimi (18 Kasım, rev0 üzerinde)
Puanlar: kaynak/doğruluk 6,5; hassasiyet 8; kanca/tutma 6,5; Türkçe/seslendirme 7,5. Altı engelleyici bulgu.
Başkan her iddiayı kaynakla sınadı:
- **M10 (engelleyici):** Zweig'in hükmü ters aktarılmış. Almanca metinde doğrulandı (8. bölüm: "Elisabeth, die Realistin, siegt in der Geschichte, Maria Stuart, die Romantikerin, in Dichtung und Legende"). Düzeltildi.
- **H07–H09:** Camden'e göre Mary haberci dönmeden geçti; "vaat etmişti" → "yardım sözü verecekti, ama Mary cevabı beklemedi".
- **G08:** "on bir ay sonra" (feragatten itibaren 9 ay) → "Adada on bir aya yakın kaldı".
- **E07:** kaçış iki gece sonra; düzeltildi.
- **A07:** "aynı adada" coğrafi hata; cümle "bir kez bile yüz yüze gelmedi" oldu.
- **Kanca:** A 102 → 74 kelime; ilk cümle tarihsiz ("Bir kraliçe idam edilmek üzere…"); kapak A'nın vaadi ~0:10'da.
- **Hassasiyet:** Bothwell bölümündeki "tutku mu, zorbalık mı?" oylaması kaldırıldı (tanık zorbalık yazıyor; bölüm sorusu "Bothwell'le neden evlendi?"); "şehidin rengi" anlatıcı hükmünden Mary'nin bakışına çevrildi; "hiç çocuğu olmadı / soyu bitti" → "varis bırakmadı / Tudor hanedanı sona erdi".
- Diğer 18 bulgu (F06 "sersemletti", M09 "birkaç metre" çıkarıldı, J04, L13 "bu taçtaki hakkı", B08 kararı II. Henri verdi, G09 anahtar rivayeti çıkarıldı, F03 yumuşatıldı, "elim olay", Zweig'e "romantik/gerçekçi" atfı, F09, Brantôme "saraylı", "beş saate yakın", Knox "sonradan yazacaktı", L09–L10 sıra, E10 "Melville'in duyduğuna göre", J10 "kopyanın üstüne", J01, "sayvan") ve Türkçe/okunuş düzeltmeleri (Size yalvarırım, Dudley'yi, Abbey'ye, Calais/Brantôme/Stuart/Fotheringhay/Paulet okunuşları, Türkçe büyük İ) uygulandı.
- **Reddedilen yok.** B bölümü önerilen ~120 yerine 148 kelimede kaldı (Brantôme'un "Elveda Fransa" anı korunsun diye; başkan kararı).
- Fable'ın önerisi: tam ikinci tur gerekmez; değişen cümlelerle tek gerileme kontrolü yeter. Başkan bu kontrolü kendisi yaptı (aşağıdaki sayım).

rev1: 172 cümle, 2.063 kelime, ~21,5 dk; tts 14.480 karakter.

## Üslup kapısı, kurgu ve ses (kurulsuz; başkan denetimi, 18 Kasım)
- **Üslup kapısı:** manzara (A03 Solway), orta plan (A01 gravür ve kırmızı), yakın plan (B09 Clouet), 26 sn hareketli açılış (`ornek/acilis_0-26_mix.mp4`). Bulgular ve uygulananlar: karanlık zeminlerdeki tarama "yağmur" gibi okunuyordu (tarama eşiği .42 → .70, yoğunluk .4); bulutlar boncuk dizisi (bulanık kütleler); kırmızı koyu kalıyordu (kırmızı, çizimin açılmış tonuyla çarpılıyor); gravürde kırmızı düz kesik gibiydi (koyuluk maskesi: yalnız koyu kumaş, yumuşak kenar).
- **Kurgu:** 220 plan, ortalama 5,7 sn. `tools/kontrol.js` denetimi: ara yazı kartları sürenin %17,2'si (sınır %20), kart ≤ 8 sn, ardışık aynı ölçek yalnız A05/A05b (bilerek: iki profil, aynı karede değil), eksik sözcük çapası yok. Kurgu özetleri: `tools/ozet.js`.
- **Hassasiyet bulguları (başkan, görüntüde):**
  - Dans sahnesinde havaya kalkmış düz kollar selama benzeyebilirdi → çiftler el ele.
  - Anka kuşu simetrik ve açık kanatlı çizilince amblem kartalına benziyordu → yandan, kıvrık kanatlı, alevden yükselen kuş.
  - **Finden gravürünün sol altındaki ek resim idam anını (balta, kütük) gösteriyor** → bu gravürün kullanıldığı her planda örtüldü (A01, L07b, L13, Shorts, kapak B kırpması). Gardiner 1790 baskısı (kesik baş) hiç kullanılmadı.
  - İdam salonu çiziminde kütük ve balta yok; ILN 1861 baskısı baltayı dışarıda bırakan kırpmayla.
- **Ses:** özgün piyano/armonyum eşliği ve efektler (numpy sentez), miks −14,2 LUFS, tepe −1,5 dBFS. L11 "Ve salon sustu" boyunca müzik yok. Kulakla son onay kullanıcıda.

## Paketleme: Fable danışman (18 Kasım)
Puanlar: başlık 7; kapak A 6,5; kapak B 7,5. Başkan her bulguyu kapak karelerinde doğruladı:
- **B, hassasiyet (engelleyici aday, kabul):** kırmızının içinde dikey koyu kıvrım çizgisi ve kitabın köşesinde kırmızı leke kan gibi okunuyordu (tam boy kırpmada doğrulandı) → kitap ve el kırmızıdan çıkarıldı, kırmızı daha düz ve yumuşak kenarlı. Aynı düzeltme filmdeki A01, L07b, L13 planlarına da uygulandı.
- **B (kabul):** üst beden soluk, "siyah elbise" okunmuyordu → gravür daha koyu (kontrast 1,45); baş kadraja girdi; "KIRMIZI" yazısına ince krem kontur (gri değerde kayboluyordu).
- **A (kabul):** taçlı dev siluet satranç taşı ya da kaide üstünde büst gibi okunuyordu → yerine I. Elizabeth'in gerçek madalya profili (16. yy, The Met CC0) gökte, sola, teknedeki Mary'ye bakıyor; Mary ve tekne büyütüldü (kırmızı etek, uzanan el), bir kürekçi ve direk çıkarıldı; film çiziği kapakta azaltıldı.
- **Başlık (kısmen kabul):** "I. Elizabeth" kapısı öne alındı ("… | I. Elizabeth ve Mary Stuart"). "Kalbini mi Dinlersin, Mantığını mı?" alınmadı: başlık filmin kendi sorusunu tekrar etmeli.
- **Kayda geçen uyarı:** iki kapak iki vaat, ama yalnız B aranan kelimeyi ("idam") taşıyor; B kazanırsa sebebin "kırmızı" mı "idam" mı olduğu ayrılamaz.
- Sonrası: odak ölçümü A 5 odak (1. odak Mary, %50/%62), B 4 odak (1. odak yazı); akış taklitlerinde ikisi de 168 px'te okunuyor (`kapak/test/`).
