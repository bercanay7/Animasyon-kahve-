# Bölüm 12 — Bırakmak · yazar notları (BÖLÜM YAZARI D)

**Dosyalar:** `scenes_c12.py` (SHOTS) · `shots_c12.py` (c12_ önekli türler: `c12_clock`, `c12_forty`, `c12_transfer`, `c12_reason`, `c12_crackcoin`, `c12_rumor`; `crack_pts/_crack`, `candle_draw`) · `scenes_d.py` (`d_hall_gold` sahnesi = `hall` + alçak güneş huzmeleri + sıcak zemin yansıması; `d_pair` bastonsuz çift figür; kamera/ekran dönüşümleri) · `d_common.py` (D ortak: `A()`, `wd_counter`, `wd_medals`, `wd_medal_swap`, `tag`, `tag_seq`, `nplate`, `cameo` …).
**Süre** 96.5 sn · **18 çekim** (bölüm kartı hariç) · ort. 5.4 sn/çekim · `--check`: **uyarı yok** (bölüm ort. ≈ 115–127 ms/kare (makine yüküne göre), en ağır çekim ≤ 170 ms; 2× süper-örnekli stage.py ile ölçüldü).
**Ton:** ağır, veda eğilimli; c0'ın aynası. Aynı salon, **farklı ışık ve kamera:** c0'da gün ışığı + kalabalığa süzülme, burada ağır altın ışık + kapıdan giriş + tahtta kimse yok. Damgalar: **YORUM** (s6), **RİVAYET** (s9b), **ÇALIŞMAYA GÖRE** (s9a). Saat anlatıda "saat üç sularında" → ekranda "≈ 15.00".

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | c12_clock | 0:00.0 | 7.0 | saat_uc | "BRÜKSEL" kicker, "25 EKİM 1555", altın kadran: akrep XII → III ("üç" sözünde), halkalar; "≈ 15.00" |
| 2 | theatre / tower | 0:07.0 | 2.9 | kule_juana | Oda-lab `tower/tordesillas`: mumlu hücre, pencere, Juana siluet; "ALTI AY ÖNCE", "JUANA / annesi" levhaları; kamera Juana'ya yaklaşır |
| 3 | wd_counter | 0:09.9 | 3.5 | juana_46 | Juana oniks madalyası + "46 YIL / Tordesillas" sayacı |
| 4 | theatre / d_hall_gold | 0:13.4 | 9.7 | salon_ikinci | Aynı salon, ağır altın ışık; çift yakın sütunun arkasından girer (x 110→900), "GENEL DEVLETLER" levhası; "WİLLEM / Orange Prensi" levhası çifti takip eder |
| 5 | wd_medals | 0:23.1 | 3.7 | felipe_mary | FELİPE (Oğlu) · MARY (Kız kardeşi) |
| 6 | c12_forty | 0:26.8 | 7.0 | kirk_yil | Zaman çizgisi 1555 → 1515 (bar sağdan sola uzar); solda yaşlı Karl, sağda "15 YAŞINDA" genç Karl; "40 YIL"; genç Karl'a taç |
| 7 | map | 0:33.8 | 6.7 | devir_harita | Hollanda (bugün) → İspanya (Ocak 1556) yakınlaşma; FELİPE madalya + levha; "25 EKİM 1555 / bugün", "OCAK 1556 / gelecek" |
| 8 | c12_transfer | 0:40.5 | 8.4 | devir_semasi | Solda ŞARLKEN; üç kart: HOLLANDA → FELİPE (25 Ekim 1555 · şimdi), İSPANYA → FELİPE (Ocak 1556), İMPARATORLUK UNVANI → FERDİNAND (1556 – 1558) |
| 9 | c12_reason | 0:48.9 | 4.5 | neden_gut | "TARİHÇİLERİN SAYDIĞI NEDENLER"; gut (yanan ayak) + kum saati; GUT · YORGUNLUK; **YORUM** damgası |
| 10 | c12_reason | 0:53.4 | 5.3 | neden_evrensel | Altın küre + haç; "gerçekleşmeyeceğinin" sözünde küre çatlar; "EVRENSEL İMPARATORLUK" |
| 11 | c12_crackcoin | 0:58.7 | 5.7 | felipe_iflas | FELİPE madalyası; çapraz kılıçlı sikke ("SAVAŞTA"), çatlar ("İFLASA YAKIN") |
| 12 | map | 1:04.4 | 4.6 | donus_1556 | Hollanda → İspanya deniz rotası, gemi; "EYLÜL 1556" |
| 13 | map | 1:09.0 | 3.7 | yuste_harita | İspanya içinde kesikli rota, YUSTE'ye derin yakınlaşma; "ŞUBAT 1557" |
| 14 | theatre / cloister | 1:12.7 | 2.3 | yuste_avlu | Oda-lab `cloister` (alacakaranlık): avlu, çeşme, tek figür |
| 15 | theatre / chapel | 1:14.9 | 6.2 | ayin | Oda-lab `chapel`: altın sunak, diz çökmüş figürler; **ÇALIŞMAYA GÖRE** damgası |
| 16 | c12_rumor | 1:21.2 | 5.4 | tabut_rivayet | Soğuk, kesik çizgili hayalet tabut (dioramadan bilerek ayrı), iki mum, soru işareti; **RİVAYET** damgası |
| 17 | theatre / bedroom | 1:26.6 | 8.2 | yatak_odasi | Oda-lab `bedroom`: yatakta hasta; sağ altta "31 AĞUSTOS 1558" → "BÜYÜK OLASILIKLA / sıtma" → "21 EYLÜL 1558"; ateş nabzı (kırmızı vinyet), "öldü"de mum söner; kamera yaklaşır |
| 18 | wd_medal_swap | 1:34.7 | 1.7 | elli_sekiz | Oniks V. KARL madalyası · "58 yaşında · 1500 – 1558", son saniyede siyaha solar |

Tür çeşitliliği: diorama ×5 (hiçbiri 2'den fazla ardışık değil: 14–15 ardışık, 16 diorama değil), özel ×7 (saat, 40 yıl, devir şeması, neden ×2, iflas sikkesi, tabut), harita ×3, madalya/sayaç ×3.

## 2. Bilinen kusurlar / dürüst notlar
1. **Saat:** analog kadran + dijital "≈ 15.00" birlikte; dakika ibresi XII'de sabit (hafif titreme). Metin "sularında" dediği için "≈" konuldu (kesin saat yok).
2. **Salon çifti:** `emperor=False`; çift `extra` geri çağrısıyla çiziliyor (lab'ın hazır imparatoru yerine bastonsuz `d_pair`). Kalabalıkla çizim sırası doğru görünüyor; kapıdan girişte yürüme salınımı var, durunca duruyor.
3. **9.7 sn'lik tek salon çekimi** (c12s3 12.4 sn'lik cümle); içinde kamera hareketi + iki levha var, ardından Felipe/Mary madalyaları geliyor. İstenirse ikiye bölünebilir (bir sonraki sürümde `theatre` tekrarı pişirme maliyeti getirir).
4. **Kule çekimi:** kamera Juana'yı kadrajda tutacak biçimde ayarlandı (önce yakınlaşma başı kesiyordu).
5. **`c12_rumor`** diorama değil; bilerek: rivayet = kesik çizgili hayalet (kanıt zayıflığı), "çalışmaya göre" kısmı ise dolu diorama (kilise). İkisinin dili ayrıştırıldı.
6. **Yatak odası:** `dip` geçişi 0.85 sn (daha kısa geçişte `--check` yanlış pozitif veriyordu); mum "öldü"den 0.15 sn önce söner; ateş vinyeti "ateşi" → "sıtmaydı" arası.
7. **Son madalya siyaha solar** (`fade_out=1.0`); sonrasında compose'un c13 başlık kartı gelir (3 sn boşluk içinde).
8. **Avlu çekimi 2.3 sn:** c12s8'in ikinci yarısı; kısa ama cümle başına bir görsel olay kuralını sağlıyor.
9. **Harita bölgeleri** yaklaşık çokgenler ("SINIRLAR YAKLAŞIKTIR"); iki harita çekimi (Hollanda/İspanya) aynı boyama dilini kullanıyor.
10. **"WİLLEM / Orange Prensi"** levhası çiftin kamera dönüşümüyle hesaplanan konumunu izliyor; salon katman derinliği değişirse levha kayar.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| BRÜKSEL · 25 EKİM 1555 | 1 | evet (c12s1) | CONFIRMED (A5 #16) |
| ≈ 15.00 (saat üçe gelen akrep) | 1 | evet ('saat üç sularında') | NİTELİKLİ (A5 #17 Motley/Gutenberg, 19. yy 'as the clock struck three'); "≈" hedge'i |
| ALTI AY ÖNCE · JUANA · annesi | 2 | evet (c12s2) | CONFIRMED (A5 #12: ölüm 12 Nisan 1555) |
| 46 YIL · Tordesillas · JUANA · Kastilya Kraliçesi | 3 | evet ('kırk altı yıllık tutsaklığın') | CONFIRMED (A1 #3; A5 #12: 1509–1555). 'Tutsaklık' sözcüğü c1s9'daki delilik/siyaset tartışmasıyla gerilimli (DÜŞÜK risk) |
| GENEL DEVLETLER | 4 | evet (c12s3) | NİTELİKLİ (A5 #16–#17, Motley 19. yy) |
| WİLLEM · Orange Prensi | 4 | evet | NİTELİKLİ +H2 (Willem'in 'genç' olması: 1533 doğumlu, 22 yaşında; araştırmada teyit) |
| FELİPE · Oğlu; MARY · Kız kardeşi (madalyalar) | 5 | evet | NİTELİKLİ (A5 #16–#17: arkada oğlu ve kız kardeşi) |
| 1555 ← 40 YIL → 1515 · 15 YAŞINDA | 6 | evet (c12s4) | CONFIRMED (A5 #16: konuşmada 'tam 40 yıl önce, 15 yaşında'); A1 #6 (Ocak 1515) NİTELİKLİ |
| 25 EKİM 1555 (bugün) HOLLANDA · OCAK 1556 İSPANYA · İMPARATORLUK UNVANI 1556 – 1558 → FELİPE / FERDİNAND | 7, 8 | evet (c12s5) | NİTELİKLİ (A5 #19: 25 Eki 1555; 16 Oca 1556; unvan 27 Ağu 1556 – 14 Mar 1558); metindeki 'ancak 1556 ile 1558 arasında' hedge'i |
| TARİHÇİLERİN SAYDIĞI NEDENLER · GUT · YORGUNLUK · EVRENSEL İMPARATORLUK (çatlayan küre) · **YORUM** | 9, 10 | evet (c12s6 'Tarihçilerin saydığı') | CONFIRMED (A5 #18). A5 #18'in üçüncü nedeni (Protestan–Osmanlı–Fransa baskısı) listede yok |
| FELİPE · SAVAŞTA · İFLASA YAKIN | 11 | evet (c12s7) | CONFIRMED (A5 #18) |
| EYLÜL 1556 · Hollanda→İspanya rotası | 12 | evet (c12s8) | CONFIRMED (A5 #20); rota şematik |
| ŞUBAT 1557 · YUSTE | 13 | evet | CONFIRMED (A5 #20; Fundación Yuste 3 Şub 1557) |
| Avlu (manastır/konut) | 14 | evet ('küçük konut') | CONFIRMED +H36 ('küçük konut' ayrıntısı araştırmada yok) |
| Kilise + ÇALIŞMAYA GÖRE | 15 | evet (c12s9 'Bir çalışma … yazıyor') | NİTELİKLİ (A5 #22 tek akademik özet); damga cümledeki hedge'in aynısı |
| Hayalet tabut + RİVAYET | 16 | evet ('yalnızca rivayet') | RİVAYET (A5 #23 ANEKDOT) |
| 31 AĞUSTOS 1558 · BÜYÜK OLASILIKLA sıtma · 21 EYLÜL 1558 | 17 | evet (c12s10) | CONFIRMED (A5 #21: Britannica/PMC); 'büyük olasılıkla' hedge'i ekranda da var |
| V. KARL · 58 yaşında · 1500 – 1558 | 18 | evet ('Elli sekiz yaşındaydı') | CONFIRMED (A1 #1; 24.02.1500 → 21.09.1558 = 58 yıl 7 ay) |

## 4. Montaj/ses için vurgu anları (global sn)
Akrep hareketi 1104.5 · "üç" ve halka dalgaları 1105.0 · "46" sayacı 1109.4 · Willem levhası 1117.8 · "40 YIL" geri sarma 1127.5 · devir okları 1139.8 · YORUM damgası 1149.6 · küre çatlağı 1155.3 · iflas çatlağı 1161.3 · ÇALIŞMAYA GÖRE damgası 1174.6 · RİVAYET damgası 1184.4 · ateş vinyeti 1188.6 · mum söner 1193.4 · V. KARL levhası 1194.6.

## 5. Ana ajana istekler / bulgular
1. **compose.py / shots.py — Türkçe büyük harf:** `title.upper()` ("i"→"I") nedeniyle başlıklarda İ noktası kayboluyor (en görünür örnek c9: "YENI DÜNYA … VICDAN"). c12'nin "BIRAKMAK" başlığı doğru (ı dotless); yine de ortak bir `tr_upper` önerilir: `s.replace("i","İ").replace("ı","I").upper()` (compose.py:203, shots.py:264–265, shots.py:541).
2. **Paylaşılan `medals/emblem/doc/quote/counter` türleri** (`at + x`) demet çapalarla çalışmıyor; c12'de çapalı kopyalar `d_common.wd_*` (özellikle `wd_counter`, `wd_medals`, `wd_medal_swap`).
3. **`sk.text_width("")`** boş dizgede çöküyor (`d_common.tw()` korumalı). **`shot(label=…)` ↔ tür parametresi `label` çakışması** (paylaşılan `counter`): `wd_counter`'da `lab`.
4. **`theatre` sahne önbelleği ~5 sahne:** c12'de tower, hall(gold), cloister, chapel, bedroom = 5 farklı sahne; tekrar yok, sorun değil. Aynı sahneye farklı `p` ile dönülürse yeniden pişer (3–8 sn).
5. **`check()` yanlış pozitifi:** `dip`/`fade` geçiş penceresine düşen ölçüm, sonraki çekimin ilk pişirmesini öncekine yazıyor (yatak odası → 2 sn görünmüştü); `dip` 0.85 ile çözüldü, render'ı etkilemez.
6. **Bölüm kartı girişi sert kesme:** `chapter_card` `tr`siz; c12 son kare siyaha solduğu için c13 kartına geçiş yumuşak, ama diğer bölümlerde kartın önünde kısa siyaha dalış önerilir.
7. **Lab bağımlılıkları:** `tower(variant=tordesillas, candle)`, `bedroom(candle, fade_candle_t)`, `chapel(coffin)`, `cloister(time)` parametre adları değişirse c12 etkilenir. `d_hall_gold` lab `hall`'unun `layers()/dyn()` yapısına bağlı (katman 4'e ışık ekliyor).
8. **Madalya çizim hızı (öneri):** `SH.draw_medal` her karede görüntüyü yeniden boyutlayıp gölgeyi bulanıklaştırıyor (ölçüm ≈ 74 ms/çizim, 640 px). `d_common.fast_medal` aynı görünümü önbellekli görüntü + önbellekli gölgeyle çiziyor (≈ 26 ms/çizim; 3 test karesinde en büyük piksel farkı 1/255). D bölümlerindeki tüm madalyalar (`wd_*`, `cameo`, `c9_durer`, `c12_*`, `c13_*`) bunu kullanıyor; aynı önbelleği ortak `shots.draw_medal`a almak tüm bölümlerde madalya çekimlerini ≈ 2–3× hızlandırır (paylaşılan `medal` türü hâlâ yavaş yolu kullanıyor).
9. **qa_program.py / qa_text.py sonuçları (04:25 UTC):** `--static` engelleyici/uyarı yok; örnekleme (140 kare, 2 işçi) 3 uyarı verdi ve üçü de tek seferlik ilk-kare pişirmesi: yüksek zoom harita karoları (`yuste_harita`, zoom 6.6) ilk karede ≈ 6 sn sürüyor, sonraki kareler ≈ 100–150 ms; büyük simge sprite'ı ve ilk madalya pişirmesi yük altında 450–590 ms'ye çıkabiliyor (`--check` ısınmış önbellekle < 220 ms). `qa_text.py` yalnız yazıyla yazılmış sayıları ("elli beş", "kırk altı", "on sekiz", "yaklaşık yüz bin"), sayaç ara değerlerini ve kaynaklı yılları (1500–1558, 1519–1522, 1515 = 1555−40) işaretledi; hepsi bilinçli/kaynaklı.
