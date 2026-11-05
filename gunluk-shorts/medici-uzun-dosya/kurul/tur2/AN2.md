# AN2: Animasyon ve kurgu (kurgu ritmi, mizansen, yönetmenlik) · Medici Parça 1 · TUR 2 (v2)

Üye: AN2. Tarih: 5 Kasım 2026. Değerlendirilen: `out_p1/medici_P1.mp4` v2 (598,5 sn, 14.365 kare). Diğer üyelerin yalnız tur 1 raporlarını okudum (AN1, PK2, SA1); tur 2 raporlarını okumadım.

## 1. Karar

**RED: 8,4 / 10** (eşik ≥9; tur 1'de 7,0).

Tur 1'in ana engelleyicisi (403–589 sn "kart vadisi") ölçülerek kapandı. Kamera tekdüzeliği ve tek tempolu geçiş dili de kapandı. Ritim eğrisinde artık çukur yok. RED kararının nedenleri:
- Yeni bir engelleyici var: 471,7 sn'de papa elinde hançerle görünüyor. Anlatım "aforozla tehdit" diyor; görüntü fiziksel bir tehdit ekliyor.
- Sert kesme politikası 5 aynı kadraj sıçraması (jump cut) getirdi.
- 432,6–435,0 sn'de iki isim levhası üst üste biniyor.
- Tekdüzelik riski kartlardan odalara taşındı: aynı salon setleri ve aynı iki figürlü kompozisyon tekrar ediyor.

İlk üç madde düzelirse puan ≈9,1 (ONAY) olur. Set çeşitlemesi de yapılırsa ≈9,5.

## 2. Neye dayandım

**Sınır:** Videoyu oynatamadım, sesi duyamadım. Kare dizileri, ölçümler ve kodla değerlendirdim. Hareket ölçüsü 0,5 sn arayla alınmış iki karenin farkıdır (240×135 gri). Dünya/kart sınıfı `qa_flow` aile sütunundan (dunya/kart/figur) alındı; çekim ortası karelerle de doğruladım. "Kapsama" kaba bir vekil ölçüdür: arka plandan farklı piksellerin oranı.

**Kaynaklar:**
- `out_p1/kurul/qa_flow_ozet.txt` (106 satır, 17 GEÇTİ / 0 KALDI / 1 UYARI), `hareket.json` (1196 örnek), `timeline.json` (85 cümle), `genel_01…04`, `gecis_*` (kesme_1/8/9 dahil), `tam_05/09/10/11`.
- `notlar_c0–c2.md`, `yonetmen_c0–c2.md`, `notlar_hareket.md`, `notlar_madalya.md`, `scenes_c2.py`, `cilt_cam.py` (BAND_KINDS/attach), `cilt_oda.py` (salon varyantları), `KURUL.md`.
- Videodan kendim çıkardığım kareler: 106 çekim ortası karesi; her sert kesmenin önü ve arkası (kare doğruluğu); 15 zaman şeridi (431–440, 467–476, 486–494, 214–219, 268–271, 580–592, 85,5–86,6 sn ve diğerleri).
- Aynı setteki kesmelerde ORB + RANSAC ile ölçek ve kayma ölçümü (HUD ve çerçeve şeridi maskeli). Gerçek kesmeler (farklı görüntü) 3–4 inlier verir; aynı kadraj 150–1000 inlier verir.

### v1 → v2 temel ölçüler

| ölçü | v1 | v2 |
|---|---|---|
| çekim (kartlar dahil) | 95 | 106 |
| ort. / medyan / maks çekim | 6,34 / 5,80 / 16,3 sn | 5,64 / 5,75 / **10,0** sn |
| 12 sn üstü çekim | 9 | **0** |
| dakika başı kesme | 11, 9, 9, 12, 9, 10, 10, **6**, 11, 8 | 12, 10, 9, 13, 9, 9, 10, 12, 13, 9 |
| sert kesme | 4 / 94 | **39 / 105** (qa: %39) |
| tasarlı geçiş süresi | hep 0,9 sn (σ≈0,02) | 0,30–2,00 sn, σ 0,36 (qa 0,38) |
| geçişte geçen süre | %13,5 | %8,9 |
| itme (push) payı · en uzun aynı kamera dizisi | %82 · 26 | **%34 · 4** (pan 29, pull 11, truck 9, yol 8, tilt 6, crane 4) |
| dünya (W) süre payı | %29 | **%49** (figür dahil %53) |
| 403,6–589,5 sn: dünya payı / en uzun kart dizisi / dünyasız en uzun boşluk | %0 / 17 / 186 sn | **%41** (figür dahil %47) **/ 3 / 19,1 sn** (figür dahil 15,7) |
| dakika kapsaması | … 0,36 · 0,36 (7.–8. dk) | 0,75 0,56 0,62 0,56 0,65 0,62 0,54 **0,52 0,49** 0,54 |
| hareket örneklerinde ≤3 payı (tüm video / 7. dk / 8. dk) | %42 / %83 / %60 | **%22 / %25 / %27** |
| en uzun ≤3 koşusu | 12,5 sn | 6,0 sn (245–251, #44) |
| çekim içi medyanı <3 olan çekim | 38 / 95 | 18 / 106 |
| 1 cümleye değen çekim · cümle başına oturan kesme | 79 / 95 · 69 / 94 (−0,11 sn) | 95 / 106 · 75 / 105 (−0,13 sn) |

## 3. Tur 1 maddelerimin durumu

| madde | durum | kanıt |
|---|---|---|
| **E1** kart vadisi 403,6–589,5 (engelleyici) | **KAPANDI** | Aralıkta dünya payı %41 (figür dahil %47), en uzun kart dizisi 3, en uzun dünyasız boşluk 19,1 sn (figür dahil 15,7), kapsama 0,51. 7. dakikada ≤3 payı %83'ten %25'e indi. Önerdiğim bölmeler yapıldı: Cossa (431,6 oda) + Konstanz salonu (440,1); taht odası (460,4 / 466,9 / 471,7); catasto sokağı (486,4: kapı kapı yürüyen görevliler, şerit 486,5–493,5); Machiavelli/Cavalcanti odaları (539,4 / 545,2 / 552,5). Hedeflerim (her 60 sn'de dünya çekimi, ≤4 kart, 7.–8. dk kapsama ≥0,50) tuttu; 8. dk 0,49 ile sınırda. |
| **Ö1** 26 ardışık itme + hız | **KAPANDI** | En uzun aynı kamera dizisi 4; itme payı %34. Süreye bağlı itme var (`("push",)` = 0,039·süre^0,47). "Ardışık itme ≤5" ve "Ölçülen hareket" kapıları geçiyor. Tek tutarlı ters yön: Konstanz 440,1 `pan l`. |
| **Ö2** geçişler tek tempo, kesme yok | **KAPANDI** (yan etkisi §4-Ö1'de) | Sert kesme 39; süre σ 0,36. Uzun geçişler: veba yıkaması 2,0 (181,2), ölüm mumu 1,8 (518,3), kapı ışığı 1,6 (584,8). Vuruş geçişleri: slide 0,30–0,40 (152,2 / 197,3 / 277,7 / 566,2). Önerdiğim aynı set kesmeleri uygulandı (#4, #34, #58). **Ama:** aynı mekânda kesmeyi önerirken "kadraj ≥1,4× ya da açı değişsin" şartını yazmadım. Sıçramaların bir kısmı bu eksik tariften geliyor (bkz. §4-Ö1). |
| **Ö3** 1 çekim = 1 cümle kilidi, hızlanma yok | **KISMEN** (artık küçük) | 3 montaj grubu var (162,0–171,9 Peruzzi/Edward; 480,2–486,4 "22 YIL + 18 YIL"; 493,6–502,8 katasto 2,6 / 3,6 / 2,9 sn). Kesme yoğunluğu arttı, en uzun çekim 10 sn, #55'in 16,3 sn'si bölündü. Hâlâ açık: 95/106 çekim tek cümle; kesmeler cümle başının 0,13 sn önünde. Görüntünün sesi önden kestiği (0,6–1 sn) ya da cümleden sonra tutulduğu an yok. 14 kesmeli dakika yok. Onay için şart değil. |
| **Ö4** parça sonunda bekleme yok | **KAPANDI** | Son sözcük 590,11; bitiş ekranı 591,5 → 1,39 sn bekleme. Beklemede kule penceresindeki ışık söner (589,6'da var, 591,0'da yok). Sessiz kapanış bir olayla bitiyor. |
| **Ö5** itmenin kenar yazısını kırpması (445–449) | **KAPANDI** | Cossa sahnesi yeniden kuruldu. "COSSA = XXIII. JOHANNES · PİSA PAPASI…" levhası 437,6–440,1'de tam kadrajda. `qa_yerlesim` 0 ihlal (14 otomatik düzeltme). **Yeni:** levha–levha çakışması (§4-Ö2). Kapı bunu ölçmüyor. |
| **K1** açılış yatak odası 9,6 sn | **KAPANDI** | 0–3,7 kapak yankısı → ışık geçişi → oda 3,7–9,1 → 9,1'de sert kesme: arma + "ANNA MARIA LUISA". İlk 13 sn'de 3 görsel olay var. |
| **K2** tür tekrarı adla atlatılıyor | **KAPANDI** | Aile haritası (`p1_` öneki soyuluyor, `AILE`/`family=`). "Kart dizisi" kapısı geçiyor (en uzun 4, %55 dünya/figür). |
| **K3** 358–417 üç harita | **KAPANDI** | Brugge artık iki figürlü oda (351,6). Bu aralıkta 2 harita kaldı (361,1 ve 406,0). |
| **K4** c1→c2 bölüm kartı (isteğe bağlı) | **DEĞİŞMEDİ: KABUL** | 339,8–342,8 kart aynı. Tur 1'de "bırakmak da kabul" demiştim. Kart öncesi ve sonrası aynı banka seti (333,3 → 342,8). Süreklilik hissi korunuyor. |
| Motor önerilerim 1–3 (çeşitlilik kapıları, geçiş süre aralığı + kesme, hız bazlı kamera) | **UYGULANDI** | `qa_flow`'a 5 yeni kapı eklendi; `TR_MIN/TR_MAX` 0,25–2,4; `tr="cut"`; `auto_push`. |
| Korunacaklar | **KORUNDU** | 101 sn sikke → fresk başlık (gecis_ana_baslik_c1), 34,6 zoomthru, 49,4 carry, veba pasajı (181–209 sn: 8 çekim / 28 sn), madalya motifi (v3 kabartma), defterin dönüşü (511,7), çapalar (mutlak %2). |

## 4. Yeni sorunlar (önem sırasıyla)

**E1: ENGELLEYİCİ · 471,7–≈473,0 sn (#82) papanın elinde hançer (≈x 1240–1340, y 200–560).**
- `scenes_c2.py` ≈satır 186'da `kind="papa"` oyuncusu `action="threat"` alıyor. Bu, kitin "ŞİDDET İŞARETİ" eylemi (`cilt_anim.act_threat`: "saldırgan öne atılır, kolu hançerle yukarı kalkar"). Rehber §6'ya göre bu eylem yalnız Pazzi ve 1527 gibi şiddet anları içindir. Kareler: 471,8'de bıçak aşağıda, 472,6'da yüz hizasında; namlu, balçak ve topuz seçiliyor.
- Anlatım "aforozla tehdit etmiş" diyor; bu manevi bir yaptırım. Görüntü gerçek bir papayı (V. Martinus) bankacıya silah çekerken gösteriyor.
- Bu, Yönetmenlik Rehberi §12'nin yasakladığı şeydir: görüntü, anlatının söylemediği bir olguyu taşıyor (şiddet tehdidi). Kaynak/hassasiyet üyelerinin veto alanına da girer.
- Yapılacak: `action="point"` + elde papalık bullası (`c2_bulla` simgesi motorda var), ya da kalkık el + "AFOROZ TEHDİDİ" damgası.
- Maliyet: bir satır + tek segment render (≈4 dk).

**Ö1: ÖNEMLİ · aynı kadrajda kesme: sıçrama (jump cut).**
- Ölçüm: aynı setteki kesmelerde önceki son kare ile sonraki ilk kare karşılaştırıldı (ORB/RANSAC, maskeli).

| kesme | sn | kadraj değişimi | okunuş |
|---|---|---|---|
| #23 darphane | 130,44 | ×0,99, +80 px | kesin sıçrama; figürün pozu "zıplıyor" |
| #58 banka salonu | 333,30 | ×1,01, −156 px | kesin sıçrama; kamera atlıyor |
| #82 taht odası | 471,70 | ×1,19 | kesin sıçrama; kart "yakın iki kişilik" diyor ama 1,19× yakın plan okunmaz, papanın pozu patlıyor |
| #8 belge | 43,86 | ×1,21 | sınırda; vurgu itmesi gibi okunabilir |
| #46 Machiavelli odası | 258,36 | ×1,15 | sınırda; vurgu itmesi gibi okunabilir |

- Yapılacak: aynı mekânda kesme, kadrajı ≥1,4–1,5× değiştirsin ya da açıyı/nesneyi değiştirsin. Örnekler: #82'de mitra ve Giovanni'nin elleri için ≥2× ara plan; #46'da isyancının konuşma tomarına yakın plan. Ya da kesme yerine 0,3 sn'lik vuruş geçişi kullan, ya da iki çekimi anahtar kareli tek çekimde birleştir (#23, #58).
- Motor: `qa_flow`'a "aynı görüntü kesmesi" kapısı. Eşleşme inlier'ı ≥100 ve ölçek 0,8–1,35 ise UYARI; bilinçli kullanım için `jump=True`. ≈0,5 gün.

**Ö2: ÖNEMLİ · 432,6–435,0 sn (#74) isim levhaları üst üste biniyor.**
- "BALDASSARRE COSSA / KİLİSE ADAMI" (≈x 530–1270, y 190–335) "GIOVANNI" levhasının (≈x 310–730, y 300–400) üst kenarını ve harflerin tepesini örtüyor (çakışma ≈x 530–730, y 300–335; 2,4 sn).
- Bu, "özensiz otomatik yerleşim" gibi okunur.
- Yapılacak: GIOVANNI levhasını sola/aşağı al ya da COSSA levhasını GIOVANNI söndükten sonra (≈435,2) getir.
- Motor: `qa_yerlesim`'e levha–levha kesişim denetimi (≈0,25 gün).

**Ö3: ÖNEMLİ · tekdüzelik riski kartlardan odalara taşındı (set ve sahneleme tekrarı).**
- `p1_oda` 106 çekimin 33'ü (%31), c2'de 47'nin 17'si.
- Kodda `salon/napoli` varyantı (P4'teki Napoli sarayı için tasarlanmış) üç ayrı yeri oynuyor: Vieri'nin Roma bankası (294,1), Brugge (351,6), çifte kayıt kâtibi (412,7). `salon/medici` hem 1743 Medici salonu (20,0) hem "vicdan komitesi" (373,4).
- Aynı ağaçlı goblen papalık taht odasında ve Konstanz salonunda da asılı (440,1 / 460,4 / 466,9 / 471,7).
- c2'de yedi sahne aynı kompozisyon: iki ayakta profil figür, orta-geniş, düz yan bakış, aralarında nesne el değiştirir (351,6 / 379,2 / 391,4 / 431,6 / 466,9 / 471,7 / 506,7).
- 598 sn boyunca insan elinin ya da yüzünün tek bir yakın planı yok.
- Hem tekdüzelik hem yer okunurluğu riski: Brugge, Floransa'nın Medici salonuyla aynı görünüyor.
- Yapılacak:
  - Yer başına set farkı: Brugge'de Flaman pencere manzarası ve soğuk ışık; papalık ve Konstanz'da Medici ağacı goblenini kaldır. Varyant parametresiyle ≈0,5 gün.
  - Çok çekimli her sahnede bir ≥2× ara plan (el, nesne, kese, mitra, tüy kalem). Bu Ö1'deki sıçramaları da çözer.

**K1: KÜÇÜK · şerit ucunun açığa çıkması (alay frizi).**
- #39 (216,9–219,4 sn) ve #47 (269,0–271,0 sn) çekimlerinde sağ kenarda friz bitiyor ve ötesindeki parşömen görünüyor (≈x 1840–1910; tam_05_218s'de x≈1865).
- Neden: `cilt_cam.attach` şerit türünü adla tanıyor (`BAND_KINDS={"skyline","frieze","procession"}`). `p1_procession` sarmalayıcısı bu kümede yok. Ayrıca `truck` yerleşik kaydırmaya çevrilmiyor; bu yüzden örtme zumu uygulanmıyor.
- Yapılacak: `p1_` önekini soy (aile haritasındaki gibi) ya da şerit türlerinde `pan` kullan. ≈15 dk + 2 çekim render.

**K2: KÜÇÜK (kullanıcı sorusu açısından önemli) · yer tutucu "dalgalı çizgi" sayfalar ve seyrek şema kartları.**
- Dalgalı çizgili sayfalar: 534,5–539,4 (#95), 559,7–566,2 (#99), 566,2–569,0 (#100). Anlatım sözü okurken sayfa yalnız dalgalı çizgi yazıyor.
- Seyrek şema kartları: 416,0–431,6 (#71 zaman çizgisi, #72–#73 üç düğümlü ağ; kapsama 0,14–0,33, filmin en boş kareleri; tam_09_428s).
- Yapılacak: Cavalcanti ve Machiavelli sayfalarında anahtar sözü gerçek harflerle yazdır (ör. "SONSUZ HUZUR"). Ciompi dilekçesinde (#44) bu zaten yapılıyor. #71–#73'ü tek sürekli kamera hareketinde birleştir; ya da şemayı #70'teki kâtip odasının defterine oturt.

**K3: KÜÇÜK · 244,9–253,2 sn (#44) "Ciompi'nin talepleri" 8,3 sn'lik belge kartı.**
- v1'de oda çekimiydi; v2'de belge kartına döndü.
- Çekim içi medyan 1,49. 245–251 sn filmin en uzun düşük hareket koşusu (6 sn). Belgenin ≈%60'ı boş.
- Yapılacak: ≈4 sn'ye indir ve Signoria salonunda okunan dilekçe çekimiyle böl (set var: `salon/signoria`).

**K4: KÜÇÜK · 580,0–584,8 sn (#103) Cosimo kartı.**
- Levhalar ≈582,0'de giriyor; "39 YAŞINDAYDI" yalnız ≈582,8–583,5 arasında okunur. 1,6 sn'lik ışık geçişi 583,2'de başlıyor.
- Yaşın 11'den 39'a sayılması da tuhaf bir jest.
- Yapılacak: levhaları "Cosimo" sözcüğünde getir (≈580,6) ya da sayacı kaldır; çıkış geçişini ≤1,0 sn yap.

**K5: KÜÇÜK · 78,0–86,5 sn HUD "1737" gösteriyor, sahne "BUGÜN" (Uffizi kuyruğu).**
- Zaman sinyali çelişiyor.
- Yapılacak: bugünkü sahnelerde HUD'u gizle (`hud=False`) ya da "BUGÜN" yaz. SA2/TE ile çapraz bakılmalı.

**Çapraz not (tur 1 raporları):**
- SA1'in "tekrar eden insan çapası yok" bulgusu kapandı: Giovanni 285–576 sn arasında en az 9 sahnede aynı figür.
- PK2'nin "ucuz değil, şablon" teşhisine katılıyorum. v2'de bu his kartlardan oda ve sahneleme tekrarına geçti (Ö3).
- AN1'in E6'sı (aynı Machiavelli mizanseni) bilinçli motif olarak kabul edilebilir: 253 / 258 / 539 / 576 sn.

**Not (sorun değil):** `qa_flow` yön uyarısı (#15, 86,5 sn): Uffizi'den skyline'a `slide l` bilinçli "geriye bakış". Hareket bulanıklığıyla temiz akıyor (85,55–86,42 şeridi). Kabul.

## 5. Kullanıcının sorusu: "Bu çizim tarzı çok mu basit, ucuz görünüyor; yapay zekâ ile üretilmiş gibi mi duruyor?"

**Yapay zekâ izleri yok.** Eriyen el, bozuk harf ya da kareden kareye değişen ayrıntı görmedim. Yazılar keskin ve doğru. Giovanni dokuz ayrı sahnede aynı figür. Geçişler gerekçeli: 3,0–3,7 sn'de asma kilit parıltısından pencere ışığına; 101 sn'de sikkeden fresk başlığa; 86 sn'de hareket bulanıklıklı kayma.

**Tarzın kendisi de ucuz değil.** 1378 alay frizi (218 sn), Floransa panoramaları (108, 137 sn), kapak yankısı (0–3,7 sn), sikke ve madalya kabartması, veba renk solması (181–209 sn) ve catasto sokağı (486–493 sn) kanal çıtasında.

**Ucuz ve şablon okunan şey çizim değil, sahneleme ve tekrar.** Aynı salon üç ayrı şehri oynuyor (294 / 352 / 413 sn). c2'deki yedi sahne aynı "iki profil figür, arada nesne" kompozisyonu. Yer tutucu dalgalı çizgi sayfalar (534–569 sn) ve boş parşömen üstündeki üç düğümlü şema (416–432 sn) da bu hissi veriyor. En çok "özensiz otomatik montaj" gibi okunanlar: üst üste binen levhalar (432,6–435,0 sn) ve aynı kadrajda sıçrayan kesmeler (130,4 / 333,3 / 471,7 sn).

**Asıl risk izleyici algısında.** Sentetik ses, kit figürler ve bilgi kartlarının bir araya gelmesi, izleyicinin "yüzsüz otomatik kanal = YZ" diye etiketlediği imzaya yaklaşıyor. Bunun çaresi motor değiştirmek değil:
- yer başına set farkı;
- her sahnede bir el ya da nesne yakın planı;
- gerçek söz yazan sayfalar;
- bölüm başına bir "imza" sahne (bu parçada alay frizi ve catasto sokağı bunu kanıtlıyor).

## 6. En emin olmadığım nokta

**Sıçramaların oynatmada ne kadar rahatsız edeceği.** Ölçeği ve kaymayı ölçtüm ama hareketi göremiyorum. #8 ve #46'daki 1,15–1,21× kesmeler kamera kesme boyunca hareket hâlindeyken bilinçli "vurgu itmesi" gibi okunabilir. #23, #58 ve #82'den (pozun "zıpladığı" ve ölçeğin değişmediği kesmeler) eminim.

**Set tekrarının sıradan izleyicide fark edilip edilmeyeceği.** Varyantların renkleri farklı. Ama ağaçlı goblen ve masa düzeni birebir aynı. Bunu sinema gözüyle değil, kanalın "şablon mu?" sorusu açısından önemsiyorum.

Hançer bulgusundan ise eminim: 471,8 ve 472,6 sn karelerinde bıçak, balçak ve topuz seçiliyor; kodda `action="threat"`.
