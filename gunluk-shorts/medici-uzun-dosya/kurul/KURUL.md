# Medici Parça 1 — Bağımsız Kurul Kayıtları

Yöntem: kök `CLAUDE.md` (kullanıcı kararı, 1 Kasım). Her alanda en az iki bağımsız üye, farklı mercekler; önce bağımsız ilk bakış, sonra çapraz eleştiri, sonra başkan (ana oturum) doğrular, karar verir ve buraya yazar. Eşik ≥ 9/10. Kaynak-doğruluk ve hassasiyet-hukuk üyelerinin veto hakkı var. Kurul sesi dinleyemez (yalnız kare, ASR dökümü, ölçüm).

Raporlar: `kurul/tur1/<KOD>.md` · kanıt: `out_p1/kurul/` (kurul_kanit.py) · brif: `kurul/KURUL_BRIFI_P1.md`

---

## Tur 1 — 4 Kasım 2026 (P1 v1: `out_p1/medici_P1.mp4`, 601,8 sn)

### Üyeler ve puanlar

| Kod | Alan · mercek | Puan | Karar |
|---|---|---|---|
| AN1 | Animasyon · hareket fiziği, kamera, geçiş zanaati | 6,5 | RED |
| AN2 | Animasyon · kurgu ritmi, mizansen, yönetmenlik | 7,0 | RED |
| SA1 | Sanat yönetimi · renk, ışık, kompozisyon, kapak | 7,5 (render 8,0) | RED |
| SA2 | Sanat yönetimi · dönem doğruluğu, katman/okunurluk hataları | 5,0 | RED |
| KA1 | Kaynak · olgu ve sayı denetimi (veto) | 6,0 | RED |
| KA2 | Kaynak · yöntem dürüstlüğü, hassasiyet, hukuk (veto) | 7,0 | RED |
| PK1 | Paket · kapak/başlık, tıklama vaadi | 6,0 | RED |
| PK2 | Paket · izleyici tutma, açılış, vaat-karşılık | 6,0 | RED |
| TE1 | Teknik · render, kodlama, ses ölçümü | 8,0 | RED |
| TE2 | Teknik · erişilebilirlik, okunurluk, kontrast | 7,0 | RED |

Sonuç: **RED (10/10)**. Hiçbir üye eşiğe yaklaşmadı; ortak engelleyiciler: (1) anlatımda 3 olgu hatası, (2) c2'nin "kart vadisi" (403–589 sn) ve kamera tekdüzeliği, (3) katman/plaka taşmaları ve dönem hataları, (4) kapak vaadi ile açılışın uyuşmaması.

### Motor sorusu (kullanıcı: "bu animasyon ve çizim motorundan emin misin?")

On üyenin onu: **motoru baştan yazma, iyileştir.** Gerekçeler: Skia (Chromium'un da kullandığı 2B motor) çizim kalitesinin sınırı değil; sorunlar motorun ÇEKİRDEĞİNDE değil üst katmanlarında:
- mizansen (dünya/figür sahnesi yerine kart üstüne kart),
- kamera tekdüzeliği (95 hareketin 78'i itme/push),
- çekim içi hareket bulanıklığı yok (hızlı hareket "kayıyor"),
- dönem/yıl denetimi yok (kubbe, arma, bayrak, madalya yazıtı yıla bakmıyor),
- yerleşim korumaları yok (plaka genişliği, HUD çakışması),
- paketleme (kapak/başlık) ayrı bir zanaat olarak ele alınmamış.

Başkan kararı: motor korunur; aşağıdaki iyileştirmeler motor + sahne + paket katmanlarında uygulanır.

### Başkan doğrulaması (birincil metin)

Kurul üyeleri birincil metinlere erişemediklerini yazdı (WebFetch DNS hatası). Başkan, doğrudan bağlantıyla Gutenberg, Wikisource, Treccani ve archive.org'a erişti (HTTP 200):
- Machiavelli, *History of Florence* (Gutenberg #2464), III. kitap: Salvestro de' Medici Mayıs–Haziran 1378 Signoria'sı için **kurayla** ("was drawn Gonfalonier") gonfaloniere oldu; Temmuz 1378 Ciompi ayaklanmasında görevdeki gonfaloniere **Luigi Guicciardini**'ydi; isyancılar Salvestro'yu şövalye yaptı. → KA1-K2 / KA2-Ö1 **doğrulandı** (c1s18 "ve Salvestro çekildi" yanlış) ve c1s16'daki "halkın alkışıyla seçilmişti" ifadesi de kaynağa uymuyor (kura).
- Aynı eser, IV. kitap: Giovanni di Bicci'nin ölüm döşeği konuşması ("I die content…", kıskançlığın verilenden değil istenenden doğması) ve "istenmeden" verilen sadakalar → c2s29 ve c2s32 parafrazları **doğrulandı** (●).

### Kabul edilen düzeltmeler

#### A. Anlatım (SES YAMASI — ElevenLabs "Emrullah", eleven_v4, generations_count=1, tekrar yok)

| Cümle | Eski | Yeni | Dayanak |
|---|---|---|---|
| c2s7 | "Tracy Parks'ın aktardığına göre…" | "Tim Parks'ın aktardığına göre mevduata gelince, faiz sözleşmeye yazılmaz; banker bunu kendi takdiriyle, bir lütuf olarak öderdi." | KA1-K1, KA2-E1 (zorunlu) |
| c1s18 | "…gonfaloniere oldu ve Salvestro çekildi." | "22 Temmuz'da Ciompi denen bu işçiler Palazzo Vecchio'yu ele geçirdi; bir yün tarayıcısı, Michele di Lando, gonfaloniere oldu." | KA1-K2, KA2-Ö1 + Machiavelli III (zorunlu) |
| c1s11 | "…ve Temmuz'a kadar kaldı." | "Veba, 1348 Mart'ında geldi ve yaz boyunca şehri bırakmadı." | KA1-K3, KA2-Ö2 (Stefani "Eylül" / Boccaccio "Mart–Temmuz"; iki kaynakla da uyumlu) |
| c1s16 | "Aktarılana göre o yazın başında, … halkın alkışıyla … seçilmişti." | "O yılın Mayıs'ında, Medici ailesinin başka bir kolundan Salvestro, kurayla şehrin başı sayılan gonfaloniere olmuştu." | Başkan doğrulaması (Machiavelli III: "drawn") |
| c1s23 | "Floransa tarihinin en kanlı günlerinden biri sayılır." | "Yün işçilerinin kısa ömürlü loncası kaldırıldı; yönetimden de dışlandılar." | KA1-V5 (dayanaksız üstünlük iddiası) |
| c1s24 | "Medici adı o yıllarda…" | "Medici'nin bu kolu o yıllarda şehrin seçkinlerinin bir kademe altındaydı; kır gelirleriyle geçiniyordu." | KA1-V4, KA2-K1 |
| c2s27 | "…büyük torunu Lorenzo'nun kaydına göre…" | "İleride Muhteşem diye anılacak torununun oğlu Lorenzo'nun kaydına göre, bıraktığı servet yüz seksen bin florin dolayındaydı." | KA1-V6, KA2-Ö7 (DBI "bisnipote") |

**Başkan bulgusu (yamadan sonra, ASR + süre analizi):** orijinal ElevenLabs kaydında iki sözcük yutulmuştu ve kurul bunu duyamazdı: **c2s1** "Çözüm, kambiyodaydı." cümlesinde "Çözüm," yok (0,70 sn'lik koşu yalnız "kambiyodaydı"; ASR "Cambio'daydı"), **c1s26** başındaki "Roma'da" yok (önceki cümleyle arası 0,24 sn; ASR "Vieri di Cambio'nun bankasında çalıştı"). İkisi de yeniden üretildi; ilk sözcük yine yutulmasın diye başa kesilecek bağlam kondu ("Bölüm iki." / "Küçük bir pay aldı."), kırpılan klip yerel ASR ile doğrulandı ("Çözüm, kambiyodaydı." · "Roma'da Vieri di Cambio'nun bankasında çalıştı…"). Toplam yama: 9 cümle, 942 kredi.

**Birincil kaynak teyidi (KAY ajanı + başkan doğrulaması, `kurul/teyit_P1.md`):** 71 iddia satırından 43'ü birincil/otoriter metinle ● (Villani, Boccaccio, Stefani, Dante, Machiavelli III–IV İtalyanca, Cavalcanti, de Roover tam metin, Treccani DBI). Üç anlatım hatası daha bulundu ve yamalandı: **c1s10** (Peruzzi ortağı Villani'nin kardeşi değil kendisi — DBI), **c2s20** (aforoz tehdidi belgeli ama kaynağı Treccani değil de Roover n. 45; 'rivayet' değil), **c2s21** (kasa memurluğu 1422'den 22 yıl kesintisiz + 18 yıl aralıklı — DBI). Başkan, KAY'ın c2s20 için 'aforoz hiçbir yerde yok' hükmünü de Roover dipnotuyla düzeltti. Etiketlerde 46 cümle ● oldu. **Toplam ses yaması: 12 cümle, 1460 kredi.** Hizalayıcı "seste bulunmayan sözcük" raporu artık her yamada denetlenir.

Kullanıcının "Düzeltmeleri uygula" talebi ücretli yama için açık onaydır. Kota yetmezse: c1s18 için KA1'in ücretsiz yedeği (250,94–252,40 sn susturma), diğerleri ekran/altyazı düzeltmesiyle sınırlı kalır ve bu belgeye yazılır.

#### B. Motor (ENG-A: yerleşim/dönem/görsel hata · ENG-B: hareket/kurgu/denetim)

ENG-A
1. `name_plate`: metin genişliğine göre otomatik genişlik (sabit `w` artık alt sınır), güvenli alan x∈[90, 1830], HUD dikdörtgeninden kaçınma (SA1-E1/E2, SA2).
2. Dönem katmanı (yıl = HUD yılı, `cx.year`): Duomo kubbesi (<1420 yok; 1420–36 yarım; 1436–61 fenersiz; ≥1461 fener; ≥1471 top+haç), Campanile (1338 alt katlar, 1348 yarı, ≥1359 tam), Medici arması (≤1464 mavi zambaklı top yok), bayrak izin listesi (1378'de Medici sancağı yok), madalya yazıtı (PATER PATRIAE yalnız ≥1464) (SA2, KA1-S4).
3. Perde kum saati biçimi (`cilt_oda`), madalyadaki dikdörtgen artefakt, giornata yıkamasının yumuşatılması (`cilt_wall`) (SA1/SA2).

ENG-B
4. HUD küçülür (~300×66, kenardan ≥72 px) (SA1, TE).
5. Geçişler: süre aralığı 0,25–2,4 sn; sert kesme birinci sınıf (`tr="cut"`); geçişin ilk karesindeki çift kare hatası (k=(n+1)/N) (AN1).
6. Seçici deklanşör/hareket bulanıklığı (hızlı çekimlerde) (AN1).
7. `anim.py`: hazırlık (anticipation), oturma (settle), sarsıntı, göz kırpma; damga (stamp) çeşitliliği (AN1).
8. Hıza bağlı itme (push) ve kamera çeşitliliği (AN1/AN2).
9. `qa_flow` yeni kapılar: plaka/HUD güvenli alan; ardışık itme ≤ 5; ardışık kart ≤ 4 ve ≤ 75 sn'de bir dünya çekimi; sert kesme payı; geçiş süresi dağılımı (σ); ölçülen hareket; `qa_donem` dönem denetimi (AN2/SA2).
10. Bitiş ekranı etiket kontrastı (#E9C770, ≥34 px); parça sonu bekleme 1,2–1,5 sn; fresk başlığı daha hızlı kurulsun → c0 kart boşluğu 6,5 → ~4,5 sn (AN2/PK2/TE).

#### C. Sahneler (P1 sahne yazarı)

c0: kicker yeri/boyu + kapak yankısı (0,3–3,5 sn, kapağın vaadi ilk 5 sn'de), yatak odası kesmesi 9,2 sn, plaka "MEDİCİ'NİN SON ÜYESİ", 3. madde kartı alıntı işaretsiz ("3. MADDE · ÖZET" / "Koleksiyonlar Floransa'dan ve Büyük Dukalık'tan çıkarılamaz."), harita "SINIR YAKLAŞIKTIR", "çıkarılamayacaktı"da zincir + asma kilit, 1737 koridor figürleri siluet, gerekçe madalyonu hareketi.
c1: dönem kubbesi; nötr Ciompi bayrakları + halk kadrosu; abaküs → sayma bezi + yazılı rakamlar; şematik Peruzzi kalkanı, Bardi düğümleri; "MART 1348 · YAZ BOYUNCA"; "ÇEKİLDİ" kalkar; YIL_AT'a 1390'lar adımı; c1_agi ve Machiavelli çekimi yeniden sahnelenir (iki figür + raf); yol haritası çipleri; iris rengi kırmızı/beyaz; lonca armalarına "TEMSİLÎ".
c2: **403–589 sn kart vadisi dünya/figür sahnelerine çevrilir** (Konstanz salonu, Martinus taht odası, catasto sokağı, yazıcı odaları, kambiyo figürleri, çift kayıt animasyonu); "PİSA PAPASI · BUGÜN KARŞI PAPA SAYILIR"; Cossa = Johannes etiketi; Strozzi "1427'NİN EN ZENGİNİ"; "150.000'İ AŞKIN"; "1407 VENEDİK" kalkar; madalya "COSMVS · MEDICES"; Cosimo yaşı 39; YIL_AT 1410/1419/1420; mezar gisant; anahtar yönü/tiara; hediye kutusu → kese; sert kesmeler, kamera çeşitliliği, montaj; parça sonu bekleme.

#### D. Kapak (PK1/PK2/SA1)

K1 "SON MEDİCİ / MİRASI KİLİTLEDİ" (1743 odası, belge + zincir + asma kilit, tek parlak odak) ve K2 "FAİZ YASAKTI" (kese + florin yağmuru, kayışta palle). Cinzel 900; kahraman başlık ≥ %18 yükseklik; rozet "1/7" 150×74 sol altta (süre rozeti köşesi boş); `kapak_qa.py` (246/168/120 px, gri, akış maketi, bölge denetimi).

#### E. Paket metni (PK1/PK2/KA2)

Başlık T1: "Medici Ailesi (1/7): Faiz Yasakken Nasıl Zengin Oldular?"; açıklamanın ilk 2 satırı (PK1 3d); KA2-E2: yöntem cümlesi dürüst, kaynak listesi P1'de gerçekten dayanılanlar, ilk paragraf düzeltilir; bölümler yeniden zamanlanır; sabit yorum soru ile başlar; etiketlerden Lorenzo/Cosimo/Uffizi çıkar (P1'de yoklar), "Medici bankası, Mediciler, faiz yasağı, kambiyo" eklenir; `kaynaklar_P1.md`'ye teyit karar tablosu (KA2-E3), `SURUM_KUNYESI_P1.md`, `yayin_gunlugu.jsonl`.

#### F. Teknik (TE1/TE2) — başkan doğruladı

- **Renk matrisi (TE1, engelleyici):** render.py rgb24'ü swscale varsayılanıyla BT.601'e çevirip BT.709 etiketliyordu (kırmızılar turuncuya kayıyordu). Başkan sentetik testle doğruladı (eski: yamalarda 12 düzeye varan sapma; yeni: ≤ 3). Düzeltme uygulandı: `scale=in_range=pc:out_range=tv:out_color_matrix=bt709,setsar=1`, `-color_range tv`.
- **Kodlayıcı (TE1):** preset slow, aq-mode 3, psy-rd 1.0:0.15, VBV 24M/48M (9M/18M zor anları kıstırıyordu, SSIM 0,90). Uygulandı.
- **Mux (TE1):** `-shortest` son 3 kareyi kırpıyordu → süre videodan alınır; ses/görüntü dili `tur`. Uygulandı.
- **Okunurluk (TE2):** kamera uzayında çizilen plakaların ekran güvenli alanına/HUD dışına kıstırılması, otomatik kontrast scrim'i (küçük yazı ≥ 4,5:1, büyük ≥ 3:1), tip tabanı 34/46 px (ENG-A); düşük kontrastlı anahtar yazılar, altyazı bandındaki etiketler, 206–212 sn karanlık çukur, nakarat metninin anlatımla eşitlenmesi (sahne yazarı); 11 yetim ve 15 hızlı altyazı repliği (başkan, make_srt). Fotosensitivite temiz.
- **Hareket bulanıklığı (TE1/AN1/SA1):** 24 fps'te kalınır; uyarlamalı deklanşör (ENG-B).

### Kullanıcı sorusu (4 Kasım): "Bu çizim tarzı çok mu basit, ucuz, yapay zekâ mı kokuyor?"

Kurulda kimse "ucuz" demedi; "yapay zekâ kokusu" diyen olmadı (görseller üretken YZ değil, kodla çiziliyor; tipik YZ izleri yok). PK2: "ucuz hissetmedim, şablon hissettim" — yüzey kalitesi (kâğıt, mum ışığı, sikke kabartması, geçişler, panoramalar) Sisifos çıtasında; sorun sahne dili: çekimlerin yarısı "parşömen üstüne ikon + etiket + damga", 78/95 aynı itme, 7:00–9:40 "dokulu slayt gösterisi", tekrar eden bir insan çapası yok. SA1: "fresk ve defter" dili konu için doğru ve kanalın en zengin çıtası; tavan insan yüzü/eli/oyunculuk (figürler küçük, temas gölgesi yok, madalya portreleri en zayıf çizim). Çareler bu turun düzeltmelerinde (C: figürlü eylem sahneleri, Giovanni insan çapası, figür ölçeği; B: kamera çeşitliliği, deklanşör; ENG-A: temas gölgesi, madalya portreleri). **Tur 2'de sanat ve paket üyelerine bu soru açıkça sorulacak.**

### Kullanıcı sorusu (4 Kasım): "Tema olarak madalyon kullanmamıza kurul ne diyor?"

Motif olarak **destekleniyor, ama tek başına insan yerine geçmemeli**: AN2 "madalya = kişi motifi"ni korunacaklar listesine koydu; PK1 yüz gerektiren parçalarda (P3 Lorenzo/Pazzi, P6 kraliçeler) motorun yüz zayıflığını madalya/nesneyle çözmeyi ve kapak ailesinde madalyayı öneriyor (Şarlken'in madalyalı kapağı alanında 9/10); PK2 madalya/sikke malzemesini "pahalı" buldu; KA2 hukuken temiz (benzerlik iddiası yok). Çekinceler: SA1/PK2 — videoda tekrar eden bir **insan çapası** yok; madalyalar durağan ve videonun tek "yüzleri", çizimleri zayıf (→ madalya v3 ekibi). KA1 — portre madalyası 1438'den önce yok (Pisanello), Giovanni'nin (†1429) madalyası olamaz → 1438 öncesi "TEMSİLÎ" damgası (motor otomatik).
**Başkan kararı (P2–P7 için yönetmenlik ilkesi):** madalya "kişi kartı" olarak kalır ama kısa ve hareketli (ışık/dönüş/kabartma), asıl insan çapası figürlerdir (P1'de Giovanni artık figür). Motif P2'de tarihsel zemin kazanır: ilk Rönesans portre madalyası Pisanello'nun 1438'de, Ferrara–Floransa Konsili için gelen VIII. İoannis Palaiologos'a yaptığı madalyadır (P2/c5 Konsil anlatısı) — madalyanın kendisi hikâyeye girebilir; P3'te Bertoldo'nun Pazzi Komplosu madalyası (1478) gerçek bir tarihsel nesnedir. Bu iki bilgi P2/P3 araştırmasında birincil/otoriter kaynakla doğrulanmadan anlatıma girmez.

### Reddedilen / değiştirilen öneriler

- **PK2 Ü1–Ü8 (ücretli cümle ekleme/çıkarma, izleyici tutma için):** reddedildi. Kullanıcı kuralı: içerik izleyici tutma için kesilmez. Yerine ücretsiz görsel karşılıklar: kapak yankısı (K2), yol haritası çipleri (K7), kambiyo/çift kayıt animasyonu (K9).
- **KA2 Ö6 (Studio "Değiştirilmiş veya yapay içerik" → Evet):** değiştirildi. Kanal uygulaması "Hayır" + açıklamada yapay zekâ sesi satırı (CLAUDE.md kanal dersleri) korunur; içerik gerçekçi insan/olay taklidi değil, açıkça çizim animasyon. Muhalefet şerhi: KA2 "Evet"i öneriyor; karar kullanıcıya bildirilir.
- **Motoru baştan yazma:** önerilmedi; kullanıcının sorusuna yanıt olarak kayda geçti.

### Tur 2 planı

Aynı üyeler (SendMessage ile, aynı bağlam), yeni render + kanıt seti; raporlar `kurul/tur2/<KOD>.md`. Üyeler tur 1 maddelerinin kapanıp kapanmadığını tek tek işaretler; yeni puan verir.

---

## Tur 2 — 4 Kasım 2026 (P1 v2)

### KA1 (olgu ve sayı, veto) — 1. aşama: anlatım + kaynak + paket → **ONAY 9,0** (anlatım 9,5 · kaynak 9,5 · paket 8,5; ekran v2 render sonrası ayrıca)

Tur 1 anlatım maddelerinin hepsi kapandı; başkanın ek yamaları (c1s10 DBI, c2s20 de Roover n. 45, c2s21 DBI) birincil/otoriter metinle birebir. KA1 ayrıca iki yeni kaynağa erişti: **Casciu 2006** (*La Principessa saggia*; Aile Sözleşmesi on üç madde, Fransızca özgün, III. madde) ve **Online Catasto of 1427** (Brown Üniv.; 9.780 hane, 137 hane = %29,8, en zengini Strozzi). Başkan kararları (hepsi uygulandı):
- **N1** Tim Parks "gerçekten okunanlar" altından çıktı → "Anlatımda anılan (kitap okunmadı; bilgi de Roover'da doğrulandı)".
- **N2** Casciu 2006 ve Online Catasto kaynak listesine eklendi; **N8** Stefani rubrica numarasına baskı notu; **V3** DBI maddesine "karşı papa".
- **N3** ekran Strozzi rakamı: iki kaynak (162.925 Wikipedia / 162.906 Online Catasto) → "≈163.000 FLORİN · YAKLAŞIK".
- **N4** Villani levhası → "1300'DE PERUZZİ ORTAĞI · ŞİRKETİ 1341'DE BATTI"; **N5** Cavalcanti → "HAPİSTE · ≈1440".
- **N7** kulak kontrolüne orijinal kayıttan c2s8 ("Faiz değil, hediye.") ve c1s6 ("ona göre") eklendi; **N10** YAYIN_TASLAK'taki "Tracy Parks" ve okunmamış kaynaklar kaldırıldı; **N11** etiketler: c0s4, c0s8, c0s11, c2s23, c2s30 ● (toplam 51 ●).
- Türkçe ek: "5:39'de" → "5:39'da" (paket üreticisi artık okunuşa göre ek seçiyor).

### KA2 (yöntem, hassasiyet, hukuk; veto) — 1. aşama → **RED 8,0** (Y1 + paket satırları düzelirse 9,0; Y1+Y2 sesle yamalanırsa 9,5)

Tur 1'den E1, E3, Ö1, Ö2, Ö7, Ö8, K1 kapandı; KA2 12 yamanın hepsini kendi yerel Whisper'ıyla döktü, metinle uyumlu. Yeni bulgular ve başkan kararları:
- **Y1 (engelleyici) c2s10** — başkan de Roover tam metninde doğruladı: Roma şubesinin 1402'de 4.000, 1420'de 6.000 florin sermayesi vardı; "the capital had already been withdrawn in 1426", 1429 sözleşmesinde "no corpo". Eski cümle de Roover'ın Averardo de' Medici'nin ayrı bankası için yazdığını Giovanni'ye bağlıyordu (araştırma notu M1:D19 hatası). **Ses yaması**: "De Roover'a göre Roma şubesi zamanla sermayesiz çalışır hale geldi; kasayı Kilise'nin yatırdığı para dolduruyordu." Ekran kartı "SERMAYE · 1426'DA ÇEKİLDİ".
- **Y2 c2s30** — başkan DBI "Cavalcanti, Giovanni"de doğruladı: Stinche'de ≈10 yıl, Istorie'yi hapiste yazdı (olaylar 1420–1440). **Ses yaması**: "Cavalcanti ise 1430'larda, hapisteyken, olaya daha yakın bir kalemle başka bir şey yazar: …"; levhalar "1430'LAR · HAPİSTE".
- **Y3 paket** — çelişki cümlesi daraltıldı ("önemli çelişkilerde…"), Tim Parks "okunmadı; özet notlarına dayanır" diye ayrı satırda, sabit yorum dayanak satırı (1427 sayımı için Online Catasto). KA2'nin önerdiği "137 hane hesabını okuyamadık" cümlesi kullanılmadı, çünkü KA1 aynı turda Online Catasto'da doğruladı.
- **Y6 şablon** — YAYIN_TASLAK'ta "Tracy Parks", okunmamış kaynaklar ve Studio "Evet" düzeltildi (başkan kararı "Hayır" + açıklama satırı; KA2 muhalefet şerhi kayıtlı).
- **Y7** — ses lisansı ve Studio kararı SURUM_KUNYESI_P1.md'ye yazılacak (ElevenLabs kütüphane sesi "Emrullah", professional; taklit değil, sahibinin lisansla paylaştığı ses).
- **Y8** — kulak kontrolüne "aforozla" (c2s20), "kambiyodaydı" (c2s1) ve "Cavalcanti" (c2s30) özellikle işaretlendi.
- Toplam ses yaması: **14 cümle, 1840 kredi**.
