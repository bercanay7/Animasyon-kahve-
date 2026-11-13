# SA1 — Sanat ve üslup · Mercek: SANAT YÖNETMENİ
Medici Parça 1/7 · TUR 1 (son render + kapak + yayın paketi kapısı)

## 1. Karar
**RED — 7,5 / 10** (eşik ≥9).
Alt puanlar: son render sanat yönetimi **8,0** · kapaklar **7,5** (A 6,5 · B 7,5 · C 8,0) · yayın paketinin görsel bütünlüğü (SRT/açıklama metinleri bu merceğin dışında, bakılmadı) · ağırlıklı sonuç 7,5.

Tek cümle: Fresk ve defter cildi gerçekten kendi kimliğini kurmuş, panorama/oda/sikke/geçiş işleri kanalın en zengin çıtası; ama (a) ekran yazısı levhaları kare dışına taşıyıp HUD'un altında kalıyor, bir isim ("XXIII. JOHANNES") ekranda eksik harfle çıkıyor, (b) portre madalyalarında görünür dikdörtgen artefakt var, (c) kapaklar kanal referanslarının en koyu/en küçük yazılıları. Bunlar sanat tavanını değil işçilik kusurunu gösteriyor, yani 9'a çıkmak mümkün.

Not: Videoyu oynatamadım, sesi dinleyemedim. Hareketin kalitesi (figür animasyonu, pan titremesi, geçiş akıcılığı) hakkında yalnız kare şeritleri ve `hareket.json` eğrisiyle konuşabiliyorum; hareket yargılarım "kareden çıkarım"dır.

## 2. Ne gördüm / neye dayandım
- `out_p1/kurul/genel_01…04.png` (64 kare, ≈9,4 sn adım), `tam_01…12` (12 tam çözünürlüklü kare), `gecis_iris/carry/light/dip/zoomthru/ana_baslik_c1.png` şeritleri, `hareket.json`, `qa_flow_ozet.txt` (92 çekim tablosu).
- Kendi çıkardığım ≈45 ek kare (ffmpeg, 1920×1080 ve 1280 ölçekli): 0,3–3,0 sn açılış; 80, 106, 133, 142, 180, 207–212, 233, 335, 345, 405, 430, 433, 447, 475, 497, 509, 533, 538, 560, 563, 569, 586, 592, 594, 598, 601 sn; ayrıca kontrastlı kırpmalar (madalya, kâğıt yamaları). Dosyalar: `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/f/` (ör. `k_tops.png` levha–HUD çakışmaları, `c_coin.png` madalya dikdörtgeni, `h_1.8.png` açılış, `thumbs.png` kapak küçük boy karşılaştırması).
- Kapaklar: `yayin/kapak_P1_A/B/C.jpg` + `kapak_P1_kontrol.png`; karşılaştırma: `sisifos/kapak.png`, `kapak_b.png`, `orfeus/kapak_final_A_arkana_bakma.jpg`, `sarlken_kapak/kapak_yeni_1_madalyalar.jpg`, `_2_salon.jpg`; Sisifos figür kıyası için `sisifos/sisifos_shorts.mp4` (5/14/24/34. sn kareleri).
- Kod: `cilt_medici.py` (name_plate), `c1_kinds.py`, `c2_kinds.py`, `cilt_kinds4.py` (skyline kick), `cilt_wall.py` (giornata), `kapak_medici.py`; `STIL_REHBERI.md`, `YONETMENLIK_REHBERI.md`, `USLUP_REHBERI.md`.
- Ölçümler: 168×94 küçük boyda ortalama/95. yüzdelik parlaklık (A 35/87 · B 80/185 · C 40/133; referanslar Sisifos 86/153, Sisifos-B 78/187, Orfeus-A 111/212, Şarlken-1 69/194); bitiş ekranı etiket kontrastı (≈1,5–1,6:1); `hareket.json`: 1203 örneğin 383'ü (%32) <2,0 kare farkı birimi.
- Tür dağılımı (qa_flow tablosundan sınıflandırdım, ±%5): yaklaşık %48 süre "dünya/sahne" çekimi (skyline, oda, pano, şehir, alay, figür kiti), ≈%52 kart/diyagram çekimi (harita, madalya, defter, belge, sikke, sayaç, ağ, soy ağacı, yığın).

## 3. Sıralı düzeltme listesi

### ENGELLEYİCİ (bunlar düzelmeden yayına çıkılmaz)
**E1. İsim levhaları ekran dışına taşıyor; bir ad eksik harfle çıkıyor.**
- 447–450 sn (c2_borc), levha sağda x≈1410–1920+, y≈440–590: **"XXIII. JOHANNES" → ekranda "XXIII. JOHANNE"** (S kare dışında; levha sağ kenarı kareyi aşıyor).
- 176–184 sn (c1_kardes): "VILLANI'NİN KARDEŞİ" harfleri levhanın iki kenarına değiyor/taşıyor (x≈1078–1780 kutuda metin x≈1085–1775, dolgu sıfır).
- 436–450 sn (c2_borc): "KONSTANZ KONSİLİ · 1415" levha (x 57–855) içinde "K" ve "5" kenara yapışık.
- Kök neden: `cilt_medici.py:727` `ww = max(wn + 110, 460) if w is None else w` — çağıran sabit `w` verince metin genişliği hiç kontrol edilmiyor (`c2_kinds.py:250` `w=480`, `:226` `w=680`, `c1_kinds.py:882` `w=660` …).
- Yapılacak: `ww = max(w or 0, wn + 110)` ve levhayı güvenli alana kelepçele (x ∈ [90, 1830]); tüm `name_plate(... w=…)` çağrılarını tara, etkilenen çekimleri yeniden çiz. Bu tür hata kullanıcının "tek hata kabul etmem" çizgisine denk: ekranda yanlış yazılmış ad.

**E2. Levha–HUD çakışması (HUD kutusu ≈ x1500–1880, y20–102).**
- 176–184 sn: "VILLANI'NİN KARDEŞİ" levhasının üst kenarı HUD'un altında.
- 436–450 sn: "BALDASSARRE COSSA" levhası (x≈960–1675, y≈270+) HUD'un altına giriyor.
- 557–571 sn (c2_kalemler): **"CAVALCANTI" son iki harfi (TI) HUD'un altında kalıyor** (560 sn karesi).
- Yönetmenlik rehberi "HUD alanı boş" diyor; `qa_flow` levha–HUD kesişimini ölçmüyor, kapı bu yüzden "geçti" diyor.
- Yapılacak: `name_plate` içinde HUD dikdörtgeni (1480,10,1900,118) ile kesişim testi: kesişirse y'yi ≥124'e it ya da levhayı sola kaydır. `qa_flow`'a "levha ∩ HUD = ∅ ve levha ⊂ güvenli alan (90 px)" kapısı ekle.

**E3. 557.5–570.9 sn (c2_kalemler, 13,3 sn): kamera kayarken iki isim levhası kareden çıkıyor.**
- 560 sn: "MACHIAVELLİ" sol kenardan taşıyor (x<0). 563 sn: ikisi de üstten kesik (başlık yarım). 569 sn: yalnız "1440'LARDA" alt satırı kalıyor.
- Tam da "hangisi söylendi: bilmiyoruz" cümlesinde hangi sayfanın kimin olduğu okunmuyor.
- Yapılacak: levhaları kamera dışı (ekrana sabit) katmana al ya da anahtar kareleri (−200→330 px, zoom 1,0→1,4) levhaları kapsayacak biçimde yeniden yaz.

**E4. Portre madalyalarında dikdörtgen artefakt.**
- 531–539 sn (Lorenzo): kafanın ve yüzün üstünde **yarı saydam açık dikdörtgen, ≈x585–980, y240–855** (538 sn karesinde yüzü bir kutuya alıyor; kontrast artırınca çarpıcı, normal karede de görünür). Aynı kabartma katmanının dik kesilmiş kenarı Giovanni (293–299, 507–511, 584–589 sn) ve Treccani (462–470 sn) madalyalarında "kafa arkası düz dikey çizgi + kutu kafa" olarak görünüyor.
- Yapılacak: kabartma/parıltı katmanını yüz konturuna klipler, gölge/parıltı katmanını dikdörtgen sınırı olmadan (alfa kenarı) kompozitle. Etkilenen çekimleri yeniden render et.

### ÖNEMLİ
**Ö1. Açılış kicker'ı (0–3,8 sn).** "18 ŞUBAT 1743 · FLORANSA" harf üstleri y≈0'da kareye yapışık/kırpık (metin y≈0–32, x≈540–1440), zemin kahve üstüne ton-ton gri-kahve (düşük kontrast). Kod `cilt_kinds4.py` içinde `CM.kick(f, kick, W/2, 104, …)` diyor ama videoda y≈15–30'da; çerçeve/kamera dönüşümü kaydırıyor. İlk izlenim karesi: krem + yumuşak gölge ile gökyüzü içine (y≈135–175, ≥34 px) al ve `qa_flow` güvenli alan kapısına ekle.

**Ö2. Boş/durgun karede boşluk (429,5–435,5 sn, p1_network).** Işık geçişinden sonra ≈3–5 sn yalnız ince "MEDİCİ'NİN FARKI: YAPI" başlığı ve boş parşömen (kare farkı 0,4–1,1); ilk düğüm 432–433 sn'de beliriyor. `qa_flow` "durgunluk"u MAD<0,4 ile ölçtüğü için geçiyor. Şemanın iskeletini (soluk Floransa düğümü, ızgara, parçacık) geçiş biter bitmez göster; sözcük çapasını yalnız vurgu için kullan.

**Ö3. Çekimlerin yaklaşık üçte biri neredeyse sabit.** 1203 örneğin 383'ü (%32) <2,0 birim (ör. 70–77, 147–172, 429–436 sn). Kullanıcının "olabildiğince akan" talebine göre ritim/animasyon üyeleri değerlendirecek; sanat yönünden: kart çekimlerinde (≈%52 süre) ek bir derinlik katmanı yok (aşağıda iyileştirme 1).

**Ö4. Açılış odası perdesi (3,8–13,3 sn, 9,6 sn'lik ilk "oda" çekimi).** Yatağın sağındaki perde (x≈650–740, y≈380–850) kum saati gibi büzülmüş, basamaklı/tırtıklı kenarlı; hero çekimde görünür artefakt. Uyuyan figür siyah bir blob, yorgan altında değil üstünde duruyor, yastıkla temas gölgesi yok. Perde pili genliğini sabitle, dikey daralmayı kaldır, kenarı anti-alias; gövdeye üstten tek yumuşak rim ışığı ver.

**Ö5. Bitiş ekranı etiketleri (594,9–601,9 sn).** "SIRADAKİ PARÇA" ve "ABONE OL · ZAMAN KURYESİ" koyu kahve üstüne koyu bronz; kontrast ≈1,5–1,6:1 ölçtüm. Etiketleri krem/altın (#E9C770) yap, ≥34 px, kutuların çerçevesini de aç.

**Ö6. Madalya portrelerinin çizim kalitesi.** Lorenzo (531–539 sn) düz küt saçla kadın başı gibi okunuyor, Giovanni'nin kafası kutu. Videodaki tek "yüz" bunlar. İlerideki parçalarda Cosimo, Lorenzo, Savonarola yüz taşıyacak; bu üreteç ele alınmadan P2–P7'de sorun çoğalır (iyileştirme 3).

**Ö7. Kağıt "giornata" yamaları (kart çekimlerinde).** Sert dikdörtgen tonlama farkları (ör. 431 sn x0–545, y595–965; 484 sn aynı yer; 536 sn solda). Fresk giornata fikri doğru (cilt_wall.py: "günlük sıva yaması" tasarım gereği), ama boş kartlarda dikiş/döşeme hatası gibi okunuyor. Kenarı 8–12 px yumuşat, çokgen kenarı hafif düzensizleştir, kart çekimlerinde ton farkını yarıya indir.

**Ö8. HUD kutusu çok büyük ve kenara yakın.** 380×82 px, sağdan 40 px (kendi kuralınız ≥90 px; TV'de %22 izleyici aşırı tarama riski). Koyu lacivert tek doymuş blok olarak gözü köşeye çekiyor ve levhalarla çakışma riskini artırıyor. ≈300×66 px'e indir, kenardan ≥72 px, levha varken opaklığını %70'e düşür.

**Ö9. Kapaklar (ayrıntı aşağıda "Kapak değerlendirmesi").** A: 168 px'te 95. yüzdelik parlaklık 87 (referanslar 153–212) ve MEDİCİ büyük harf yüksekliği ≈%15; B: yazı ≈%10, ikinci satır belgenin üst kenarına dayanıyor; C: koyu (ortalama 40), "VE ÇİFTE DEFTER" ≈%4,6 (168 px'te okunmuyor), yazı düz altın, sikke kabartmalı (üslup kopukluğu).

### KÜÇÜK
**K1.** 219 sn alay: bayrak kenarlarında basamaklanma (x≈100–270, y≈220–390) — kenar yumuşatma.
**K2.** 60 sn galeri: "TABLOLAR" yazısı üstünde yürüyen yarı saydam figür (x≈340–450) levhayla çakışıyor.
**K3.** 589–594 sn kule: kulenin solunda ince beyaz dikdörtgen sliver (x≈795–805, y≈675–950); kubbe/kule ölçeği tutmuyor (kubbe kule tabanından büyük görünüyor).
**K4.** Fresk başlık (101–108 sn) altyazı satırı "BANKA ÖLDÜ, GÜZELLİK KALDI" ile kapak A'daki "PARÇA 1/7 · ALTIN FLORİN" farklı: tutarlılık için kapak A de aynı satırı kullansın (kapak videoyu yanıltmaz).
**K5.** Sessiz: 206–212 sn "çukur" çekimi ilk 2–2,5 sn neredeyse siyah (kare farkı 0,6); telefon güneş altında kaybolabilir. Güçlü ve ölçülü bir sahne, ilk 1 sn'ye zemin parıltısı eklenmesi yeterli.

## Güçlü yanlar (korunmalı)
- Açılış (0–4 sn skyline, alacakaranlık gökyüzü, pigment kaybı) ve 1743 odası: sıcak mum ışığı, vinyet, ışık huzmeleri; "ana başlık freski" (101–108 sn, lapis zemin, yaldız harf, arma) tipografik olarak videonun en iyi karesi.
- Gozzoli tarzı alay (142, 219 sn) ve Floransa pazarı panoraması (113 sn): renk, desenli kumaş, kalabalık yoğunluğu, tutarlı çerçeve; çizim kalitesinin zirvesi bunlar.
- Malzeme işleri: sikke kabartması, anahtarlar, sandık, mühür, madalya kenarı; cilt dili (kâğıt, craquelure, giornata) tutarlı.
- Geçişler tasarlanmış: mercekten iris (13 sn), bayrak/şerit carry (49, 233 sn), ışık huzmesi (69 sn). Renk bilgi taşıyor: veba yıkaması (184–206 sn) ve çukur katmanları ölçülü, ağır.
- Kimlik bütünlüğü: HUD yıl plakası, çelenk çerçeve, Cinzel/Cormorant, perde paleti (ALTIN) bölümler arası kopmuyor.

## Kapak değerlendirmesi (sanat yönetmeni mercek; TO/paketleme üyesi ayrıca bakacak)
| | Güçlü | Zayıf | Ölçüm (168 px) |
|---|---|---|---|
| **A** MEDİCİ freski | Videonun ana başlığıyla birebir; lapis+altın, arma; marka plakası | Vaat yok (sadece etiket); ortada simetrik, durağan; kenarlarda ≈%17 genişlik boş koyu pay; yaldız leke gürültüsü başlıkla aynı renk, başlığı kirletiyor; "ZAMAN KURYESİ" ve alt satır 168 px'te okunmuyor | ort. 35 / p95 87 (en koyu), harf ≈%15 |
| **B** Sözleşme | En okunur (parlaklık 80/185), vaadi videonun kancasıyla aynı ("bir sözleşme bir şehri bağladı"); kırmızı/altın renk kontrastı | Belge düşük duygu; mühür ≈55 px ve odak değil; ikinci satır belgeye dayanıyor; sol siluet çamurlu; yazı yüksekliği ≈%10 | ort. 80 / p95 185 |
| **C** Florin | En güçlü sanat: eğik ışık, derinlik (arkada silik sikkeler), kabartma; asimetrik kompozisyon (sol sikke, sağ yazı) | Koyu (ort. 40); "FLORİN" ≈%13, alt satır ≈%4,6; yazı düz altın, sikke kabartmalı; "ÇİFTE DEFTER" vaadi görselleştirilmemiş; sağ yarının üçte biri boş | ort. 40 / p95 133 |

Sıralama (sanat): C > B > A. Paketleme için B'nin metni + C'nin görsel gücü birleşirse güçlü kapak çıkar.
Yapılacaklar (kapak): (1) A'yı tam taşma (full-bleed) yap, lapis'i ≈%25 aç, MEDİCİ büyük harf ≥130 px (%18), yaldız lekesini ortadan seyrelt, küçük satırları ≥44 px yap ya da kaldır; A'yı seri/oynatma listesi başlığı olarak tut. (2) B'de mühürü ≈160 px ve tek parlak odak yap, metne 30 px nefes ver, koyu degradeyi biraz aşağı uzat, ikinci satırı belgeden ayır. (3) C'de "FLORİN" ≥130 px ve sikkeyle aynı kabartma/gölge işlemini yazıya uygula (video başlık kartındaki `painted()` yazısı bunu zaten yapıyor), arkaya kırmızı çizgili defter kenarı ekleyip "ÇİFTE DEFTER"i görselleştir, p95 parlaklığı ≥170'e çıkar. Süre rozeti bölgesi (1280'de x≈960–1250, y≈553–689) üçünde de yazıdan boş: iyi.

## 4. En emin olmadığım nokta
(1) E1/E2'nin P1'de kaç çekimi etkilediğini tam saymadım; `name_plate(... w=…)` çağrısı `c1_kinds.py`/`c2_kinds.py` içinde ≥15 yerde var, ben altısında (JOHANNES, VILLANI'NİN KARDEŞİ, KONSTANZ KONSİLİ, COSSA, CAVALCANTI, MACHIAVELLİ) ekranda gördüm; gerisi "olası". (2) Madalya dikdörtgenini kod değil kare üzerinden "derleme hatası" olarak yorumluyorum (kontrast ve kenar geometrisi bunu söylüyor), niyetli bir "ışık yaması" olma ihtimali düşük ama sıfır değil. (3) Hareket kalitesini (figür yürüyüşü, pan titremesi, 24 fps'de bulanıksız kamera) yalnız kare farkıyla yorumladım; bu yüzden figür animasyonu puanım "çizim" üzerinden, hareket üzerinden değil. (4) P2–P7'yi görmedim; sanat konusu için çıkarımlarım P1 kanıtından ekstrapolasyon.

## 5. Motor sorusu: sanatsal tavan
**Kodla çizim motoru (Skia, yandan kesme-bebek, yüzsüz) bu konunun görsel anlatımı için yeterli mi?** Evet ama konunun yarısı için: "fresk ve defter" dili (belge, defter, harita, sikke, arma, panorama, mekân ışığı, tipografi) bankacılık ve şehir siyaseti için doğru ve P1'de kanalın en zengin çıtasını kuruyor. Tavan, **insan yüzü, el, oyunculuk ve sanat eserinin kendisi**: yüzler yok, eller sivri eldiven, madalyalar tek "yüz" ve en zayıf çizimler, figür pozları yürüme/yazma/çekiçleme ile sınırlı. Konunun P4–P7'deki sanat/Rönesans tarafı (Botticelli, Michelangelo, Leonardo, kubbe) için kodla yeniden çizilen resim izleyicinin zihnindeki özgün eserle kıyaslanır; mimari (kubbe, kule, saray) ve kabartma işi motorun gücüdür, boyalı figür kompozisyonu değil. Siyasi şiddet sahneleri (Pazzi, Savonarola) silüet+ışık+yıkama ile çözülebilir ve motorun bu yönü güçlü (veba/çukur sekansı kanıt).

**Sisifos'un vazo-resmi iskeletiyle kıyas:**
- *Sisifos güçlü:* figür ölçeği (kare yüksekliğinin %50–90'ı), iki tonlu keskin silüet, kazınmış çizgi (göz, sakal, kas) ile "yüz yok" sorununu üslubun kendisine çevirmesi, eklem yapısı/üst üste binme (diz çökme, kaya itme, kartal tutuşu), çekim içi 4 alt örnekli hareket bulanıklığı ve 30 fps. Her karede tek odak okunuyor. Vazo resminde zaten profil ve yüzsüzlük norm; kısıtlama üsluba dönmüş.
- *Medici güçlü:* mekân ve atmosfer (oda/pano/şehir), malzeme (kabartma, kâğıt, yaldız), kamera ve gerekçeli geçiş, bilgi tasarımı, tipografi, renkle anlatım; ≈35 çekim türü ve 92 çekimlik çeşitlilik. Sisifos'ta figüre bağımlı çözüm vardı; Medici figür olmayan konuları (borç, kambiyo, defter) diyagram+malzemeyle taşıyor.
- *Medici zayıf:* figür boyutu küçük (%15–35) ve 168 px küçük resimde kayboluyor; yüz/el boş; temas gölgesi yok (Machiavelli 272 sn, çekiççi 133 sn: figür "havada/zemine yapıştırılmış"); çekim içi hareket bulanıksız ve 24 fps; yarı süre kart çekimi (düz parşömen üstünde etiket+sikke); **tekrar eden bir insan çapası yok** (Sisifos kahramandı; Medici'de arma ve florin var, kişi yok).

**Yeniden yazmaya/başka motora değer mi?** Hayır. Chromium Canvas 2D de arka planda Skia kullanır; ilkel kalitesi aynı. Sisifos'un avantajı çizim motoru değil, figür modeli ve üslup tercihi (kazınmış çizgi + 2 ton + büyük ölçek) ve hareket bulanıklığı hattı. Medici motorunda bunlar eklenebilir; yeniden yazma haftalar ister ve tavanı yükseltmez. Mevcut motoru iyileştirmek doğru.

**En yüksek getirili 3 iyileştirme:**
1. **Işık–gölge–derinlik geçişi (≈1,5–2,5 gün; render +%5–10).** Her figür/nesnenin altına anahtar ışık yönüne eğik temas+yayılan gölge; çekim başına tek anahtar + rim ışığı; uzak plana atmosferik sis; kart çekimlerinde ön plan parçacık/lif katmanı; giornata kenarlarını yumuşatma. En çok görsel kalite/maliyet: çekimlerin ≈%100'ünde "kağıt bebek havada" ve "boş levha" hissini azaltır. Doku zaten güçlü; darboğaz doku değil.
2. **Portre madalya üreteci (≈1,5–2 gün) + isim levhası/HUD güvenli alan kapısı (≈0,5 gün).** Parametrik profil (kaş, burun, dudak, çene eğrileri; saç/kalpak/defne tipleri), her kişiye ayırt edici siluet (Cosimo, Lorenzo, Piero, Savonarola); dikdörtgen klip hatası kaldırılır. Yüz taşıyan tek araç olduğu için P2–P7'nin kritik yolu.
3. **Figür kiti v2 (≈4–6 gün).** Yüz mikro özellikleri (badem göz + kaş + ağız çizgisi, 3 boyutta), 6 el jesti (işaret, tüy kalem tutma, sunma, sayma, yumruk, açık el), binici oturuşu/diz bükümü, kumaş gecikmesi (ikincil hareket), 2–3 isimli kahraman rig'i (Giovanni, Cosimo, bankacı). İsteğe bağlı: hareket eden çekimler (pan/crane/yürüyüş) için 2 alt örnekli deklanşör (+%30–50 render süresi, yalnız o çekimlerde). Getirisi büyük, riski ve maliyeti yüksek; 1. ve 2. maddeden sonra yapılmalı.

## 6. Başka üyenin görüşü
Bilmiyorum, varsaymadım; bulgularım yalnız kendi kare incelememe ve yukarıdaki dosya/kod okumalarıma dayanıyor.
