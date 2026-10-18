# Bölüm 11 — Adamın Kendisi · yazar notları (BÖLÜM YAZARI B)

**Dosyalar:** `scenes_c11.py` (SHOTS) · `kinds_c11.py` (c11_ önekli çekim türleri, `cloister_overlay`, `gout_overlay`, gezi ağı `make_travel`, `road_overlay`) · `bw_lib.py` (ortak yardımcılar; `scene_pt` = overlay'i diorama nesnesine kilitler) · `icons_b.py` (b_gear, b_forbid…).
**Süre** 64.3 sn · **10 çekim** (kart hariç; hedef 10–12) · ort. 6.4 sn/çekim · `--check`: **uyarı yok** (ort. ≈ 118 ms/kare, en ağır `c11_machine` ≈ 150 ms; yoğun CPU'da değerler ≈ 2× çıkabilir).
**Ton:** yakın, sıcak, melankolik; mum ışığı kehribarı. Büyük diorama yok; madalya yakın planları, ince etiketler, iki sakin oda (manastır avlusu, yatak odası), iki harita. Renk kodu: altın = Habsburg/Karl, gümüş → oniks = İsabel'in ölümü, kızıl = acı/yasak.

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | c11_machine | 0:00 | 3.9 | makine_ve_adam | Beş çark (bankacı, keşiş, kral, sultan, miras simgeleri) yavaş döner; ortada V. KARL madalyası, "?" (retorik soru) |
| 2 | c11_chin | 0:03.9 | 6.8 | cene | Karl madalyası → çeneye yaklaşır; kesikli yay; "HABSBURG ÇENESİ" + "ağzı tam kapatamamak · çiğneme güçlüğü"; **YAZILIR** |
| 3 | c11_study | 0:10.6 | 10.9 | calisma_2019 | Parşömen: "2019 ÇALIŞMA"; altı hanedan portresi halkalarla bağlı; YÜZ ÖZELLİKLERİ ⇢ ? AKRABA EVLİLİKLERİ (ok kesikli+soru işaretine döner); **ÇALIŞMA KÜÇÜK**, **KESİN DEĞİL** damgaları |
| 4 | c11_wed | 0:21.5 | 4.9 | evlilik | "26 YAŞINDA"; V. KARL (altın) + İSABEL (gümüş, "Portekizli kuzeni"), aralarında yüzük |
| 5 | c11_loss | 0:26.4 | 4.3 | isabel_oldu | "1539"; İsabel madalyası gümüşten oniks'e solar; "35 YAŞINDA" |
| 6 | bw_theatre / cloister | 0:30.7 | 5.6 | manastir | Lab `cloister` (alacakaranlık, lambalı kemerler, tek keşiş): "YAKLAŞIK İKİ AY" + MANASTIR etiketi; "bir daha da evlenmedi" = yüzük üstünde yasak halkası (dip geçişi) |
| 7 | c11_black | 0:36.3 | 3.4 | siyah | Yaşlı Karl madalyası altından oniks'e; kenarlardan siyah örtü; **ANLATILIR** |
| 8 | bw_theatre / bedroom | 0:39.8 | 8.6 | gut_perhiz | Lab `bedroom`: yastıklara yaslı hasta, mum, komodin; bacakta üç kızıl zonklama (**GUT ATAKLARI**), alt sırada HAREKETSİZ · PERHİZ · BOL YEMEK; tabağın üstünde yasak halkası belirir ve "bol yemek"te erir; **YAZILIR**; kamera komodine yavaşça kayar |
| 9 | map | 0:48.4 | 12.0 | gezi_agi | Karl'ın kendi toprakları kızıl; taç durak durak gezer: ALMANYA → İTALYA → İSPANYA → HOLLANDA → FRANSA → TUNUS → CEZAYİR (anlatıdaki sırayla); "güzergâh şematiktir" |
| 10 | map | 1:00.4 | 3.8 | yollarda | Tüm rota; sol üstte yazı takımı + "MASA" çizilir; altın "YOLLARDA"; son 1 sn siyaha çözülür |

## 2. Bilinen kusurlar / dürüst notlar
- **METIN_DEGISIKLIKLERI uygulandı:** c11s5 "yaklaşık iki ay … çekildi, bir daha da evlenmedi" (etiket "YAKLAŞIK İKİ AY", MANASTIR; "iki ay" kesin yazılmadı); c11s7 "hareketsiz bıraktı" — etiket **HAREKETSİZ**, "yatağa bağlı" vurgusu yok.
- **Yatak odası:** lab sahnesi hastayı yatakta yastıklara yaslı gösteriyor; "hareketsiz" ile uyumlu ama yine de yatak imgesi taşıyor. Aynı oda c12s10'da (ölüm çekimi) tekrar kullanılıyor — burada ilk görünüş, orada "son"; istenmezse c11s7 için başka bir görsel (yemek masası/ayak minderi natürmort) yazılabilir.
- **2019 çalışması:** çalışmanın adı/yazarı/örneklem büyüklüğü ekranda yok (anlatıda da yok); portreler jenerik madalya-lab portreleri, gerçek çalışmanın görselleri değildir. Damgalar anlatıyla birebir: "çalışma küçüktü; kesin bir şey söylemiyor".
- **Çene çekimi:** madalya portresi stilize; yakın plan çeneye yaklaşmak için, anatomik doğruluk iddiası yok; "YAZILIR" ve alt satırdaki "çiğneme güçlüğü" anlatıdaki hedge'in aynısı.
- **Gezi ağı şematik:** duraklar ülke merkezleri, çizgiler eğri oklar (tarihsel güzergâh/sıra/yıl değil); ekranda "güzergâh şematiktir" notu + haritanın "SINIRLAR YAKLAŞIKTIR" notu var. Fransa seyahati araştırmada yok (H35, anlatıdan).
- Kısa yazılar (≈ 26–40 px) yalnız etiket/damga; ana metinler ≥ 40 px. HUD bölgeleri boş.
- İlk-kare pişirme (tek seferlik): harita ≈ 2.6 sn, `cloister`/`bedroom` ≈ 6–12 sn (stage.py süper-örnekleme sonrası ≈ 2×).
- Büyük harf Türkçe kuralına göre: İSABEL, ÇALIŞMA, KESİN DEĞİL, HAREKETSİZ.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| V. KARL · ? | 1 | evet (retorik soru) | YORUM |
| HABSBURG ÇENESİ · ağzı tam kapatamamak · çiğneme güçlüğü · YAZILIR | 2 | evet | NİTELİKLİ (A5 #14; A1 #22) — hedge 'yazılır' |
| 2019 · ÇALIŞMA · YÜZ ÖZELLİKLERİ ⇢ AKRABA EVLİLİKLERİ · ÇALIŞMA KÜÇÜK · KESİN DEĞİL | 3 | evet | CONFIRMED (A1 #22: Annals of Human Biology; Smithsonian) |
| 26 YAŞINDA · V. KARL · İSABEL · Portekizli kuzeni | 4 | evet | CONFIRMED +H33 (A5 #10; kuzenlik web doğruladı: anneleri kız kardeş) |
| 1539 · 35 YAŞINDA · İSABEL | 5 | evet | NİTELİKLİ (A5 #10: 1 Mayıs 1539, 35 yaş) |
| YAKLAŞIK İKİ AY · MANASTIR · bir daha da evlenmedi (yüzük + yasak) | 6 | evet | NİTELİKLİ (A5 #11 popüler kaynak, 'yaklaşık') **[Risk DÜŞÜK]** |
| ANLATILIR (siyah giyme) | 7 | evet | NİTELİKLİ (A5 #11) — hedge 'anlatılır' |
| GUT ATAKLARI · HAREKETSİZ · PERHİZ · BOL YEMEK · YAZILIR | 8 | evet | NİTELİKLİ +H34 (A5 #13–#14; 'yatağa bağladı' kaldırıldı) **[Risk ORTA→düşürüldü]** |
| ALMANYA · İTALYA · İSPANYA · HOLLANDA · FRANSA · TUNUS · CEZAYİR · güzergâh şematiktir | 9–10 | evet (sırayla) | YORUM +H35 (seyahat sayıları bulunamadı; Tunus/Cezayir A3 #13, #15) |
| MASA (üstü çizili) · YOLLARDA | 10 | evet | YORUM |

## 4. Montaj/ses için vurgu anları (global sn)
2019 çalışma yazısı 1042.8 · ÇALIŞMA KÜÇÜK damgası 1051.2 · KESİN DEĞİL damgası 1052.5 · yüzük 1057.2 · İsabel madalyası kararır 1061.8 · gut zonklamaları 1072.1 / 1072.7 / 1073.3 · YAZILIR rozeti 1079.3 · taç yola çıkar 1085.4 (durak sıçramaları sırayla) · "MASA" çizilir / YOLLARDA 1095.1.

## 5. Ana ajana istekler / bulgular
1. **compose.py Türkçe büyük harf hatası** (bkz. notlar_c4.md #1): bölüm kartı ve HUD başlığında "ADAMIN KEND**I**S**I**" → doğrusu "ADAMIN KENDİSİ".
2. **Hız ipucu (tüm yazarlar için):** `bw_lib.py` içinde kare başı maliyeti ≈ yarıya indiren önbellekli yardımcılar var — `static_backdrop` (bg+ışın+duo_glow tek blit), `dust2` (saveLayer'sız toz), `draw_icon2` (gölge/ışıma bulanıklığı önbellekli), `gold2` (altın yazı ışıması önbellekli), `glow_blit`, `bw_medal` (önbellekli madalya). Paylaşılan `sk.dust` (tam-ekran saveLayer), `icons.draw_icon` (her karede 2 blur), `Frame.gold(glow=)` (her karede blur) ve `SH.draw_medal` en pahalı kalemler; ortak dosyalara yazmak istemedim — isterseniz oraya taşıyın.
3. **Lab sahneleri ilk-kare pişirme maliyeti** stage.py süper-örnekleme güncellemesinden sonra ≈ 2×; sıralı render'da tek seferlik.
4. `bw_theatre` sarmalayıcı stderr'e "[bw_theatre] … hata verdi" yazar (şu an 0 hata): `cloister`, `bedroom` sorunsuz çalışıyor.
