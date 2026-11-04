# TE2 — Teknik kalite · Erişilebilirlik / Okunurluk — Medici Parça 1 (TUR 1)

Üye: TE2 (erişilebilirlik: telefon, TV, aydınlık/karanlık ortam). Bağımsız ilk bakış; başka üyenin dosyası okunmadı.

---
## 1. Karar

**RED — 7,0 / 10** (eşik ≥9).

Alt puanlar: fotosensitivite 10 · SRT (okuma hızı, satır bölme, yazım) 8,5 · ekran yazısı yerleşimi/kenar/HUD 5,5 · ekran yazısı kontrastı ve boyutu 6 · karanlık/aydınlık ortam 6,5 · kapak okunurluğu 7.

Neden RED: (1) üç çekim kümesinde özel adlar ekran kenarında kesiliyor ya da HUD'un altında kalıyor (kamera uzayında çizilen plakalar); bunlar herkesin göreceği ve düzeltmesi kolay hatalar. (2) Anlatının omurgasındaki birkaç yazı (tarih etiketleri, "ne gördüğünü… biliyoruz" nakaratı, "ESKİ PAPA" yazıtı, bitiş ekranı etiketleri) pratikte okunmuyor (ölçülen kontrast 1,3–2,7:1). (3) Kanal verisine göre izleyicinin %48'i telefonda; yazıların %43'ü 28–36 px aralığında ve satır içi (dikey) telefon görünümünde bu boyutlar okuma eşiğinin altında. İyi tarafı: flaş/fotosensitivite temiz, Türkçe karakterler kusursuz, SRT büyük ölçüde sağlam, plakalı yazılar çok okunaklı (12–17:1).

---
## 2. Ne gördüm / neye dayandım

**Sınırlarım:** videoyu oynatamadım, sesi dinleyemedim. Hareketi ve süreyi kare dizilerinden ve ölçümden çıkardım; ekranda yazının kaç saniye kaldığını okuma süresiyle karşılaştırmadım (ölçmedim).

Yaptıklarım (betikler `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/te2/` altında: `lumseries.py`, `srt_an.py`, `audit4.py`, `contrast_all.py`):

- **Kanıt paketi:** `kurul/tam_01…12`, `genel_01…04`, `gecis_*.png`, `hareket.json`, `qa_flow_ozet.txt`, `teknik.json` (1920×1080, 24 fps, yuv420p, BT.709 etiketli, 601,88 sn).
- **Tüm 14.443 kare** mp4'ten 192×108'e indirilip kare başına göreli parlaklık (WCAG sRGB doğrusallaştırma) ve 4×4 bölge ızgarası çıkarıldı: flaş/parlaklık analizi. (`hareket.json` 0,5 sn adımlıdır; 1 Hz altı örnekleme flaşı göstermez, bu yüzden kare kare yeniden ölçtüm.)
- **Her çekimden 1 kare** (95 çekim) ve ek hedefli tam çözünürlüklü kareler ffmpeg ile çıkarılıp gözle incelendi (≈70 kare).
- **Yazı kutusu denetimi:** motorun bir kopyasını (proje dışında, scratch) alıp `drawTextBlob`/`draw_spr` çağrılarını sarmaladım; 95 çekim × 3 zamanda = 285 kare çizdirip her yazının gerçek ekran kutusunu, boyutunu, rengini kaydettim (tek işlem, her seferinde ≈75 sn; bu "render yok" kuralının ince bir yorumudur, proje dosyalarına yazmadım, tam render yapmadım). Bunu 312 benzersiz dizgeyi glif kapsaması için de kullandım.
- **Kontrast:** yazı kutusunun arkasındaki gerçek video pikselleri (yüzdelik yöntemi) ile WCAG oranı. Yöntem kaba (ince Cinzel vuruşlarında alt tahmin eğilimi); sıralama için güvenilir, tam sayıları ±%20 oku.
- **SRT:** `yayin/medici_P1_tr.srt` ayrıştırıldı (166 repliği; UTF-8, BOM yok, LF).
- **Kapaklar:** A/B/C 1280×720'den 168×94 ve 246×138'e indirilip koyu/açık zeminde, gri değerde baktım; harf yüksekliği ve kontrast ölçtüm; kanal referanslarıyla (Sisifos, Orfeus, Şarlken) kıyasladım.
- **Renk körlüğü:** Machado (2009) benzetimiyle (deuteranopi, tritanopi) anlamı renkle taşınan iki çekim.
- **Belgeler:** `STIL_REHBERI.md` §6 (yazı kuralları), `qa_flow` kapıları, `cilt_medici.py` (ink/gilt/name_plate/stamp/Theme), `sk.py` (yazı tipleri, `tr_upper`).

### Ölçülen özet

| Başlık | Sonuç |
|---|---|
| Flaş (WCAG 2.3.1 / Harding ölçütü) | 1 sn pencerede ≥3 parlaklık tepe noktası yok (global eşik 0,10 ve 0,07). 16 hücre + 24 komşu çift (≈%6–12 alan) taramasında en kötü 5 dönüm noktası/sn (397,4 sn, `slide` geçişinde kolon geçişi; 2,5 flaş/sn, tek hücre) |
| En sert parlaklık adımları | tek yönlü: 350,54 sn +0,22 (bölüm kartından çıplak kesme), 77,96 sn −0,13; 107,2–107,4 sn ve 358,0–358,1 sn `light` geçişlerinde 0,25 sn'de +0,34/+0,36. Hiçbiri 1 sn içinde tekrarlanmıyor |
| Kırmızı flaş | doygun kırmızı alan değişimi yok (damgalar ekranın <%2'si, 0,3 sn) |
| Karanlık | ortalama göreli parlaklık: tüm video 0,36; ilk dakika 0,13; kare başına ortalama <0,10 olan süre 91 sn (%15); <0,03 olan toplam ≈11,4 sn (25,6; 103,7–107,0; 192,0; 194,8–196,0; 203,5; 205,8–212,0; 522,7) |
| Yazı boyutu (ekran px, 691 yazı kaydı, HUD hariç) | en küçük 25,2 px (KIYMETLİ ŞEYLER), 25,4 px (YABANCILARIN MERAKI); yazı içeren örneklerin %37'sinde en küçük yazı <33 px, %64'ünde <40 px; en büyük yazı medyanı 52 px, p10 38 px |
| Kontrast (486 yazı örneği) | medyan 6,9:1; %18 <3:1; %30 <4,5:1; benzersiz yazıların (221) en iyi anlarında %25'i <4,5:1 |
| Türkçe | 312 benzersiz dizgede eksik glif yok; ekran yazılarında "İ/ı/Ş/Ğ/Ç/Ö/Ü" doğru (yalnız yabancı adlarda tutarsızlık, bkz. Ö12) |
| SRT | ortalama 13,8 kar/sn, medyan 13,8, azami 18,7; >17 kar/sn 15 replik; ≤2 satır × ≤42 karakter; en kısa 1,07 sn |

---
## 3. Sıralı düzeltme listesi

Koordinatlar 1920×1080. HUD kutusu ölçüldü: x 1498–1882, y 18–104. Altyazı bandı y 938–1042. Başlık güvenli alanı (±%5) x 96–1824, y 54–1026; STİL_REHBERİ kuralı kenardan ≥90 px.

### ENGELLEYİCİ

**E1. "XXIII. JOHANNES" ekran dışına taşıyor; Konstanz plakası taşıyor; Cossa plakası HUD'a değiyor.** Çekim #72 `c2_borc`, 436,6–449,9 sn (taşma ≈443,8–449,9).
- Kare 446,5 sn: "XXIII. JOHANNES" 1408–2010 px aralığında çiziliyor, son harfler (ES) ekran dışında kalıyor. Neden: `c2_kinds.py:250` `name_plate("XXIII. JOHANNES","PAPA", cx_=1650, w=480)`; yazı 498 px, plaka 480 px (negatif iç boşluk), kamera ölçeği 1,048.
- Aynı karede "KONSTANZ KONSİLİ · 1415" (`c2_kinds.py:254–255`): plaka 760 px, yazı ≈883 px (46 px + track 8) → yazı plakanın iki yanından 60 px taşıyor ve sol kenara 38 px yaklaşıyor.
- "BALDASSARRE COSSA" plakası (`c2_kinds.py:226`, y=95, kamera ile y'≈74) üst sağ köşesiyle HUD'un altına giriyor (x 1498–1670).
- **Yap:** Johannes plakasını `cx_≈1480, w≥620` ya da yazıyı `fit_size(…, 400)` ile sığdır; sağ kenar ≤1830 (kamera ölçeği dahil). Konstanz plakasını `w=960` yap veya yazıyı 38 px'e indir, x≥120. Cossa plakasını `y≥130`, `cx_≈1180`'e al (HUD ile ≥20 px boşluk).

**E2. "VILLANI'NİN KARDEŞİ" plakası HUD'un altında ve sağ kenarda.** Çekim #28 `c1_kardes`, görünür ≈180,5–184,6 sn (kare 183,4 sn).
- Yazı x ≈1071–1930, y 77–131; HUD ile örtüşüyor ve plakanın sağ kenarı (1850+) ekrana dayanıyor; son harfler ("KARDEŞİ") HUD'un altında. Neden: `c1_kinds.py:882` `name_plate("VILLANI'NİN KARDEŞİ","PERUZZİ'DE ÇALIŞIYORDU", cx_=1400, y=gy-790, w=660)`; yazı 650 px, plaka 660 px (iç boşluk 5 px).
- **Yap:** yazı ≤40 px (ya da iki satır), `w≥740`, `cx_≈1240`, `y≥130`. Sol plakayla (GIOVANNI VILLANI, cx_=520) simetri korunur.

**E3. "iki kalem" çekimlerinde adlar ekran kenarında kesiliyor, HUD altında kalıyor, ANEKDOT damgası altyazı bandına iniyor.** Çekimler #88 ve #89 `c2_kalemler`, 557,5–573,7 sn.
- Plakalar ve damga kamera uzayında çiziliyor (`c2_kinds.py:551–556`, `:586–588`) ve kamera anahtar kareleri `(-200,0,1.0)→(330,10,1.4)` (`scenes_c2.py:204–209`) onları dışarı itiyor. Kare 560,6 sn: "MACHIAVELLİ" x −72…543 (ilk harfler kesik), "BİR ASIR SONRA" x −175…179; "CAVALCANTI" x 1051–1633, y 28–86 → HUD altında ("CAVALCANT" + kutu). Kare 571,3 sn (zum 1,4): "MACHIAVELLİ" hâlâ sol kenardan −47 px taşıyor, iki ad da üst güvenli alanın (54 px) dışında (y 44–100) ve "CAVALCANTI" x 1051–1619 ile HUD'a biniyor.
- "ANEKDOT" damgası (`:588`, 960,880) 564,8 sn'de x 310–920, y 920–1070: altyazı bandının içinde ve alt kenardan kesik; SRT açıkken damgayı örter. Bu kaynak-sınıfı damgası, yani kritik bilgi.
- **Yap:** adları ve damgayı kameradan bağımsız ekran uzayında çiz (`cam.end` sonrası veya `P.plate/P.stamp` ovl ile): plakalar `y≥125`, `x∈[140,1780]`; damga `y≤880` ve altyazı bandının üstünde. Alternatif: kamera yolunu plakalar kadraja sığacak şekilde daralt.

### ÖNEMLİ

**Ö1. "31 EKİM 1737" etiketi okunmuyor.** Çekim #4 `oda`, 26,2–29,5 sn (anlatıcı bu tarihi 26,27 sn'de söylüyor). `scenes_c0.py:41` `kick="31 EKİM 1737"`: 34 px gri-bej, dekoratif sınır bandı üstünde, kontrast ≈1,6:1 (kare 28,4 sn: neredeyse görünmez). **Yap:** `CM.name_plate/tablet` içine al ya da ≥48 px + koyu scrim; hedef ≥4,5:1.

**Ö2. Videonun ilk yazısı ekranın üst kenarına yapışık ve zayıf.** Çekim #0 `skyline`, 0,4–3,8 sn: "18 ŞUBAT 1743 · FLORANSA" y≈3–40 (üst kenardan 3 px), 40 px, bej üstüne bej kontrast ≈1,9:1. **Yap:** taban çizgisi y≥110 (başlık güvenli alan), 48 px, plaka ya da scrim (`k_skyline` kick yerleşimi, `cilt_kinds4.py:140`).

**Ö3. Nakarat ekranda ömrünün çoğunda okunmuyor.** Çekim #36 `c1_yazi`, 212,5–217,2 sn: "NE GÖRDÜĞÜNÜ, NE YAZDIĞINI BİLİYORUZ" (y≈735, 44 px, krem #F0E2B8 ince Cinzel SemiBold, kahverengi kâğıt): 1,6:1 (213,5–214,5) → 2,7:1 (215,5) → 4,3:1 (216,8 sn, çekim bitmek üzere). Çekimin tüm anlam yükü bu cümle. (`c1_kinds.py:951,968`; solma `cx.amt(w_at,0.7,off=0.3)`.) **Yap:** renk #FFF4D6, boyut ≥54, `title` (700) yüzü, solmayı 0,35 sn ve çapadan −0,3 sn'ye çek; yazı çekim sonuna kadar tam kalsın; hedef ≥7:1. Not (benim alanım değil, tek cümle): ekran yazısı "ne gördüğünü… biliyoruz" diyor, anlatı "ne gördüğünü yazdığını biliyoruz"; kaynak üyeleri bakmalı.

**Ö4. "ESKİ PAPA" yazıtı (Cossa'nın mezarı) düşük kontrast.** Çekim #74 `c2_mezar`, 457,6–469,8 sn: yaldız yazı, zeytin-bej levha üstünde 2,4:1; ayrıca levhada ortalı değil (sola kaymış ≈30 px). Bu, anlatıdaki "eski papa" alıntısının ekran karşılığı. **Yap:** levhayı açık krem yap ve yazıyı koyu mürekkep "oyma" göster, ya da yaldızı ≥%40 parlat; ortala.

**Ö5. Dört serbest yazı etiketi (plakasız) çok düşük kontrastlı.**
- "FLORANSA" (62 px, krem/altın, gökyüzü üstünde) çekim #18 `p1_pano`, 110,1–115,6 sn: ≈1,7:1.
- "GÜN" birimi (63 px, soluk yaldız, koyu zemin) çekim #5 `c0_takvim`, 29,5–32,1 sn: ≈1,6:1 ("114" okunuyor, birimi yok denecek kadar sönük; `c0_kinds.py:53`).
- Ana başlıktaki slogan "BANKA ÖLDÜ, GÜZELLİK KALDI" çekim #16 `fresco_title`, 101,2–107,7 sn: 1,5:1 (103,2 sn) → 2,5:1 (104–105 sn) → 5,3:1 (105,8) → 7,4:1 (106,4). Yani 6,5 sn'lik çekimin ilk 4 sn'sinde okunmuyor (`cilt_kinds.py:69–70` `sub` solma).
- "YAZILDIĞINA GÖRE" damgası (çekim #43, 253–262 sn) ≈4,0:1 ve pencerenin önünde parçalı; "KUR FARKI" (çekim #62, 375,8–380,3) en iyi 3,3:1 (büyük puntoda sınırda, çekimin ödeme sözcüğü).
**Yap:** her biri için koyu mürekkep + açık halo ya da plaka; solmayı kısalt (slogan ≤1,0 sn'de ≥4,5:1).

**Ö6. Bitiş ekranı etiketleri neredeyse görünmüyor.** Çekim #94 `outro`, 594,9–601,9 sn: "SIRADAKİ PARÇA" ve "ABONE OL · ZAMAN KURYESİ" (28 px, `compose.py:466`) 1,3–1,9:1; etiket bölgesindeki en parlak piksel 96/255 (yani yazı nominal #E6D3A0 değil, soluk). "TESLİMAT TAMAM" 1,5–2,2:1. YouTube bitiş-ekranı öğeleri bu yuvaların üstüne bindirilecek ama etiketler yine de pişmiş görüntüde. **Yap:** etiketleri ≥40 px, tam opak, scrim; bitiş ekranı sönmesini son 1,2 sn'ye bırak; "TESLİMAT TAMAM" ≥36 px, #F2D98A.

**Ö7. Altyazı bandı (y 938–1042) ile çakışan ekran öğeleri.** SRT açıkken (izleyicinin %38'i Türkçe altyazı kullanıyor) örtülür:
- "BARSELONA" harita etiketi (çekim #61 `p1_map`, 368–376 sn): y 969–998.
- "ANEKDOT" damgası (E3'te).
- Belge kenarındaki "XII/XIII" madde numaraları (çekim #9, 54–57 sn; dekoratif, düşük öncelik).
- Sınırda: "8.952 HANE" (çekim #78, 497 sn) alt kenarı 938; "OĞULLARI" (çekim #82, 515 sn) 945.
`qa_flow` "Altyazı bölgesi" kapısı bunları göremiyor: kapı tür-düzen tablosundan nominal konum ve kamera kayması tahmin ediyor (`qa_flow.py:144,361–377`), kamera ölçeğini ve serbest çizimleri (harita etiketi) kapsamıyor. **Yap:** etiketi yukarı al (y≤900), kapıyı gerçek çizim kutularıyla (bkz. motor sorusu) yeniden yaz.

**Ö8. Aşırı karanlık, düşük ışıklı ortamda "siyah" kalan çekimler.** Telefonda dışarıda/otomatik parlaklıkta ve LCD TV'de aydınlık odada içerik kayboluyor:
- Çekim #35 `c1_toprak`, 205,8–212,0 sn (6,2 sn): ortalama göreli parlaklık 0,001–0,033 (206,4–209 sn arası 0,003–0,006); ilk 2,5 sn'de çukur ve toprak katmanları neredeyse yok. Anlatı o sırada toplu mezarı anlatıyor ("katman katman toprak").
- Çekim #31 `p1_oda`, 192,0–196,5 sn: hasta odası, ortalama 0,051 (en düşük 0,004; 1,4 sn'si <0,03).
- Çekim #16, 103,7–107,0 sn (3,25 sn, koyu mavi pano; sanatsal, "MEDİCİ" yaldızı okunuyor; sorun değil, yalnız slogan için Ö5'e bak).
**Yap:** koyu çekimlerde taban parlaklığı yükselt (gama kaldırma ya da çukur çevresine soluk rim ışığı), hedef kare ortalaması ≥0,03 ve çukur/toprak katmanlarının ayırt edilebilmesi. Toplam ≈11 sn; yeniden render maliyeti düşük (2 çekim).

**Ö9. SRT düzeltmeleri.** Genel durum iyi (ortalama 13,8 kar/sn). Yine de:
- Tek–dört sözcüklük, 1,07–1,16 sn'lik kısa/yetim replikler (11 adet; okuyucuya titreme gibi gelir): #20 "çıkarılamayacaktı.", #58 "anlatır.", #75 "isyancının değil.", #94 "kazanmaktı.", #95 "Çözüm, kambiyodaydı.", #107 "vicdan komitesi.", #131 "“eski papa”.", #133 "Yazıt kaldı.", #158 "başka bir şey yazar:", #162 "olarak çizer.", #166 "kapatılacaktı.". Bu cümleler 5,5 sn üst sınırı yüzünden bölünmüş. **Yap:** önceki replikle yeniden dengele (ör. #93–95: "Zor olan, Kilise'nin “faiz günahtır”" / "dediği bir çağda" / "onu huzurla kazanmaktı."), ya da son replik süresini bir sonraki replikten önceki boşluğa 0,3–0,6 sn uzat.
- >17 kar/sn 15 replik; #95 (18,7), #100 (18,4), #82 (18,3), #6 (17,9). Bitişi sonraki replikten önceki boşluğa 0,2–0,6 sn uzatınca #6 15,2, #13 13,5, #82 14,8, #95 13,7, #100 15,5, #158 11,5 olur; 15'inin hepsi ≤17'ye girer. **Yap:** bu 15 replikte bitiş zamanını uzat (görüntü/ses bütünlüğüne dokunmaz).
- Sayı/unvan/bileşik bölünmeleri (okumayı yavaşlatır): #47/#48 "III. | Edward'ın" (replik sınırında), #41/#42 "okuma | yazmanın" (replik sınırında) ve #41'de satır sonu "doksan | bin", #146 "yüz | elli bini", #150 "yüz seksen | bin", #33 "üç | buçuk", #70 "yazıldığına | göre", #35 "bu | altına", #38 "eski | bir". **Yap:** satır sonunu bu çiftlerden sonra/önce al (`make_srt.py` `wrap2` + replik bölme kuralına "sayı+birim, unvan+ad, bileşik fiil bölünmez" ekle).
- Yazım: özel adlar ekranla tutarlı (Giovanni di Bicci, Piccarda Bueri, Baldassarre Cossa, XXIII. Johannes, V. Martinus, Treccani, De Roover, Tracy Parks, Orsanmichele). Düz tırnak (`'`, 66 kez) ile eğik çift tırnak (`“ ”`, 3 kez) karışık; her ikisi de YouTube'da sorunsuz, istenirse tek tip.

**Ö10. Kapaklar: okunurluk (168×94 / 246×138, gri, koyu/açık zemin).**

| Kapak | Ana yazı harf yüksekliği (kare %'si) | Kontrast | 168×94 | 246×138 | Not |
|---|---|---|---|---|---|
| A (MEDİCİ freski) | ≈%15 ("MEDİCİ"); alt satır ≈%3,9; "ZAMAN KURYESİ" ≈%2,1 | 7,8:1 / 7,5:1 / 5,1:1 | "MEDICI" ve arma okunuyor; alt satır ve ZAMAN KURYESİ okunmaz (3,5–2 px) | MEDİCİ rahat; alt satır zor | yaldız benekleri harfin etrafında gürültü yapıyor (gri testte belirgin); "ALTIN" kelimesinin T-I harflerinin üstünde altın yıldız var |
| B (BİR SÖZLEŞME / BİR ŞEHRİ BAĞLADI) | ≈%9,7 ve ≈%7,2 | 10:1 / 14:1 | iki satır da okunuyor (en iyisi) | rahat | ikinci satır belgenin üst kenarına oturuyor, sorun değil |
| C (FLORİN / VE ÇİFTE DEFTER) | ≈%13,2 ve ≈%4,7 | 13,4:1 / 18,6:1 | "FLORIN" okunuyor; "VE ÇİFTE DEFTER" okunmaz (≈4,4 px) | alt satır zor (≈6,5 px) | kancayı taşıyan "ÇİFTE DEFTER" en küçük yazı |

- Kanal kuralı (CLAUDE.md "Kapak dersleri": harf yüksekliği ≥%18) üçünde de sağlanmıyor; referans kapaklar (gözle tahmin) Orfeus ≈%20, Sisifos ≈%14–15, Şarlken ≈%15. **Yap:** B'de iki satırı +%40 büyüt (ilk satır ≥%14), C'de "VE ÇİFTE DEFTER" ≥%8 ya da kaldır, A'da alt satırı kaldır/büyüt ve harfin arkasındaki beneklenmeyi sadeleştir.
- Sağ alt süre rozeti bölgesi (1280×720'de x≈960–1250, y≈553–689): A ve C boş; B'de yalnız belge makarasının ucu giriyor (yazı yok). Sol alt "1 PARÇA /7" rozeti 220×98 px (%17×%14) ve 168'de "1 /7" okunuyor.
- Renk körlüğü: kapak anlamı renge bağlı değil.

**Ö11. Yazı boyutu tabanı (telefon, satır içi/dikey).** Kural ana ≥40 / etiket ≥26 / ikincil ≥22 px'e uyuluyor (yalnız iki dizge ≈25 px: "KIYMETLİ ŞEYLER" ve "YABANCILARIN MERAKI", `fit_size` plakaya sığdırırken kısıyor; c0 "gerekçe" üç gerekçe etiketi 25–30 px ve bunlar anlatının asıl vurgusu). Ancak bu eşikler tam ekran içindir: satır içi dikey telefonda (≈412 dp genişlik, ölçek 0,215) 28 px = 6 dp, 40 px = 8,6 dp; Material okuma tabanı ≈12 dp. Geniş aralıklı büyük harf Cinzel SemiBold (x-yüksekliği büyük harfle aynı) küçük puntoda sözcük şeklini kaybeder. TV'de (55", 3 m) 26 px ≈ 19 ark-dakika: sınırda tamam. **Yap:** tabanları etiket ≥34, ana ≥46, ikincil ≥30 px'e çıkar (Sisifos tabanı ≈34 px, ağırlık 700–800); 28–32 px'lik rol satırlarını ("KRONİKÇİ · ESKİ DARPHANE…", "AKTARDIĞINA GÖRE") Cormorant Bold küçük harf/cümle düzenine geçir.

**Ö12. Yabancı özel adlarda büyük harf tutarlılığı.** Aynı ekranda "MACHIAVELLİ" (İ) ve "CAVALCANTI" (I) (çekim #88–89); "PERUZZİ", "BARDİ", "MEDİCİ" noktalı iken "GIOVANNI", "VILLANI", "BOCCACCIO", "CIOMPI", "COSIMO", "TRECCANI" noktasız. `sk.tr_upper` doğru çalışıyor ama ekran dizgeleri elle büyük harf yazıldığı için kural uygulanmıyor. **Yap:** tek kural seç (Türkçe kuralı: tüm "i" → "İ", ya da özgün yazım korunarak "I"); `CM.ink`'e küçük harfli kaynaktan `tr_upper` ile çeviri koy ve ad sözlüğü tut. Seri başlığı "MEDİCİ" olduğundan Türkçe kural tutarlı olur.

### KÜÇÜK

- **K1.** HUD yıl rulosu kenara çok yakın: sağdan 38 px, üstten 18 px (başlık güvenli alanın dışında; modern TV/YouTube'da aşırı tarama yok ama eski TV'de kesilir ve mobil oynatıcı üst sağ kontrolleri dokunuşta üstüne biner). **Yap:** x_sağ ≤1830, y_üst ≥54 (kutuyu 48 px içeri al); bölüm başı kicker'ı (K2) ile birlikte yeniden yerleştir.
- **K2.** Bölüm etiketi "I · FLORİN ŞEHRİ"/"II · DEFTERİN SİHRİ" x=78, üst y=44 (kural ≥90/≥54); çekim #17, #18, #57. Plakaya içeri çek: x≥96, y≥60.
- **K3.** SRT: 9 yerde komşu replikler arası 20 ms, 2 yerde 50–69 ms (YouTube çakışmayı reddettiği için bilerek); sorun yok.
- **K4.** `zoomthru` geçişleri 20 kez, ≈5× ölçek hızlanması 0,5 sn içinde (`cilt_fx.py:591`, `depth=5.0`). Fotosensitivite eşiğinin altında ama vestibüler hassasiyet için sık; en çok 12 kullanıma indirmek ya da `depth=3.5` yeterli.
- **K5.** `p1_timeline` (çekim #70) eksen yılları 29–30 px, soluk umber 2,7–3,2:1; "1340/1407" kırmızı 49 px 2,6–3,0:1. Eksen yazısını #4A3420'ye, 34 px'e çıkar.
- **K6.** Çekim #62 `c2_nolist` "BORÇ ✗ FAİZ ✗": kırmızı çarpı vuruşları "BORÇ"/"FAİZ" harflerini örtüyor (R ve İ okunması zorlaşıyor). Çarpıyı inceltip harflerin üstünden değil altından geçir. Anlam renge bağlı değil (X/✓ biçim farkıyla ayrışıyor; deuteranopi benzetiminde de okunuyor).
- **K7.** Hareket: `hareket.json` ve geçiş şeritlerinde okunurluğu bozan bir şey görmedim. 24 fps'te hareket bulanıklığı yalnız geçişlerde olduğundan sürekli yan kaydırmada (`pan` 220–300 px / 4–5 sn ≈ 3 px/kare) TV'de hafif titreme beklenebilir (bu benim alanım dışı; TE1 baksın).

---
## 4. En emin olmadığım nokta

1. **Telefon okunurluğunun gerçek ölçeği.** Satır içi dikey mi, tam ekran yatay mı izlendiğini bilmiyorum; kanal verisi yalnız cihazı veriyor (telefon %48, TV %22). Ö11'deki "yetersiz" yargısı satır içi dikey içindir; tam ekran yatayda 26–34 px sınırda tamam. Gerçek cihazda bir kez bakmak bu yargıyı kesinleştirir.
2. **Kontrast sayıları:** yüzdelik yöntemi ve ince vuruşlar yüzünden ±%20 sapabilir; sıralama ve yön (hangi yazılar kötü) güvenilir. En kötü beş maddeyi (Ö1, Ö2, Ö3, Ö5 FLORANSA/GÜN, Ö6) gözle de doğruladım. Damga (`stamp`) kutularını kamera/döndürme yüzünden güvenilir ölçemedim; E3 ve Ö7 damga bulgularını videodan kareyle doğruladım.
3. **Sürenin okumaya yetip yetmediği** (yazının ekranda kalma süresi) ölçülmedi, yalnız kare örnekleriyle baktım.

---
## 5. Motor sorusu — okunurluk açısından

**Yazı sistemi (CM.ink/gilt, Cinzel/Cormorant/EB Garamond, boyutlar) ve yerleşim kuralları telefonda/TV'de yeterli mi?** Yazı sistemi kendi başına sağlam: vektör çizim (kamera zumunda keskin), HarfBuzz şekillendirme, 14 yüz ve Türkçe karakterlerde sıfır eksik (312 dizge tarandı), plakalı yazılar 12–17:1. Ama yerleşim ve kontrast için çalışma zamanında hiçbir güvence yok: her yazı elle yazılmış piksel koordinatıyla, çoğu kamera uzayında çiziliyor; `qa_flow`'un "altyazı bölgesi" kapısı tür-düzen tablosundan tahmin ediyor ve bu yüzden "0 ihlal" derken ben 3 çekim kümesinde kesilen ad (E1–E3) ve altyazı bandında 3 öğe buldum. Sistemin 14 yüzünden örneklediğim 285 karede yalnız 5'i çıktı (title_m 141, title 107, fell_i 25, cap_i 25, cap_b 14 benzersiz dizge; `body` EB Garamond hiç yok): yazının neredeyse tamamı büyük harf (Cinzel SemiBold/Bold geniş aralıklı, rol satırları Cormorant italik büyük harf); bu, başlıklar için güzel, 28–34 px'lik uzun rol/etiket satırlarında ise sözcük şekli kaybolup okuma hızı düşüyor.

**Sisifos hattıyla kıyas:** Sisifos'ta yazı az, kısa, tek aile (Cinzel 700–800) ve 34–190 px (taban ≈34); kameradan bağımsız ekran uzayında; 5 sn'lik cümlelere sığar. Medici'de yazı yoğun (bir çekimde 3–6 etiket), 25–34 px'te %43, 600 ağırlık, track 4–14 ve kamera uzayında. Tür zenginliği (35 çekim türü) arttıkça her türün kendi plaka/kick yerleşimi çoğalıyor ve ortak bir güvenli alan sözleşmesi yok. HUD (yıl rulosu) ortak ama yazı yerleşimi HUD'u tanımıyor.

**Yeniden yazmaya/başka motora değer mi?** Hayır. Yazı çizimi doğru; eksik olan bir "okunurluk güvence katmanı". Mevcut motoru iyileştirmek yeterli ve ucuz.

**En yüksek getirili 3 iyileştirme (maliyet ≈ kodlama günü; her biri yeniden render gerektirir, P1'de etkilenen ≈15 çekim ≈1,5–2 dk video ≈ 3–4 dk render):**
1. **Yazı kutusu kapısı + güvenli alan kıskacı** (≈1–1,5 gün). `qa_flow`'a gerçek çizimden yazı kutusu denetimi (`drawTextBlob`/`draw_spr` sarmalayıcı; bugün 285 kare ≈75 sn çalışıyor): ekran kenarı (≥90/54), HUD dışlama dikdörtgeni (1480–1900 × 10–112), altyazı bandı (938–1042), en küçük boyut tabanı. Aynı kodda `CM.ink/name_plate/stamp` içinde otomatik kıskaç (`clamp` + `fit_size`) ve kamera-bağımsız ekran-uzayı katmanı. E1–E3, Ö7, K1–K2 sınıfını bitirir. İlk sürümü bu değerlendirmenin `audit4.py` betiğinden çıkarmak yarım gün.
2. **Kontrast güvencesi** (≈1–1,5 gün). `CM.ink` çizmeden önce arka plan piksellerinin (bbox'ın 1/4 çözünürlüklü örneği, ≈1–2 ms/yazı) kontrastını ölç; <4,5:1 ise otomatik yumuşak scrim/halo ya da plaka. Serbest `kick`/etiketlerin tamamı (Ö1, Ö2, Ö3, Ö5, Ö6) için tek noktada çözüm; `fg3` (#6A5238, #AFA27C) ve "yaldız açık zeminde" kombinasyonları için palet düzeltmesi.
3. **Tip ölçeği ve karanlık tabanı** (≈0,5–1 gün kod + parça başına ≈17 dk render × 7 parça). Etiket ≥34, ana ≥46, ikincil ≥30 px; 28–32 px rol satırlarını Cormorant Bold cümle düzenine al; yazı sistemine merkezi `tr_upper` + özel ad sözlüğü (Ö12); koyu "gece/hasta/çukur" çekimlerine ortalama ≥0,03 parlaklık tabanı (Ö8).

Dürüst kısıt: Bu iyileştirmeler P2–P7'ye de aynı hataları taşıyacak; motor değişikliği P1 render'ından önce yapılırsa yeniden render sayısı azalır. Sesi dinleyemediğim için okuma süresi/senkron değerlendirmesini ses üyelerine bırakıyorum.

---
## 6. Geçenler (kısa)

- Fotosensitivite: geçti (bkz. tablo). 24 fps'te en sık tekrar eden parlaklık ramp'ı 1 sn'de tek yönlü.
- SRT biçimi: UTF-8, ≤2 satır × ≤42 karakter, çakışma yok, ≥1,07 sn, VTT eşleşiyor.
- Türkçe glifler/İ-ı: hatasız; "resmî", "AKTARDIĞINA", "KIYMETLİ" doğru.
- Renk körlüğü: X/✓ ve harita rotası (kırmızı/mavi çizgi) biçim/ışık farkıyla ayrışıyor; deuteranopi/tritanopi benzetiminde anlam kaybı yok.
- BT.709 etiketleri doğru (`teknik.json`).
