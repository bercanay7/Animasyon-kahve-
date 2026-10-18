# notlar_c7 — Bölüm VII · Sultan: Hiç Karşılaşmadılar (c7)  ·  yazar: bölüm yazarı C

Dosyalar: `scenes_c7.py`, `stage_c7.py` (c7_hukum, c7_taht, c7_vasal, c7_unvan, c7_yuk, c7_gunluk, c7_ates), `stage_c678.py` (ortak).
Yeni (yamalı) anlatıya göre: c7s11 "yedi yüz ile sekiz yüz arası bir garnizonla" → sayaç 700 – 800 KİŞİ · GARNİZON.
Son durum: 24 çekim + bölüm kartı, 106.5 sn (hedef aralığın 22'sinin biraz üstünde: Viyana yağmur/kar anlatısı iki ayrı sahne durumuna bölündü); sahne-lab `field` (Mohaç) ve `siege` (Viyana ×3, Güns) bağlı; "[sahne: … henüz yok]" yok. `--check`: uyarı yok, bölüm ortalaması ≈ 150 ms/kare (en yavaş çekim ≈ 235 ms).

## (a) Çekim listesi özeti (24 çekim + bölüm kartı)
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | medal | suleyman | 4.7 | KANUNİ SULTAN SÜLEYMAN (forest madalya) |
| 2 | c7_hukum | ayni_yillar | 3.4 | iki saltanat çubuğu: ŞARLKEN 1516→1556, SÜLEYMAN 1520→; kesişim "AYNI YILLAR" |
| 3 | map | uzaklik | 2.8 | İstanbul ↔ Brüksel: uçlarda iki madalya, kesikli çizgi, "BİLDİĞİMİZ KADARIYLA", HİÇ KARŞILAŞMADILAR |
| 4 | c678_sahne (field) | mohac | 5.8 | Mohaç: bataklık/nehir, alacakaranlık, süvari çarpışması, toz sisi; "29 AĞUSTOS 1526", MOHAÇ |
| 5 | medal | lajos | 4.0 | II. LAJOS (onyx) + alttan yükselen su/halkalar: kaçarken derede boğuldu |
| 6 | c7_taht | bos_taht_ferdinand | 5.9 | boş taç + soru işareti → Ferdinand madalyası |
| 7 | map | macar_bolunme | 2.5 | Macaristan: Ferdinand (Habsburg) ↔ Zapolya; MOHAÇ işareti |
| 8 | c7_vasal | zapolya_vasal | 3.8 | Zapolya madalyası – zincir – Osmanlı hilali: VASAL |
| 9 | map | viyana_yolu | 3.8 | İstanbul → Viyana yeşil rota, Süleyman madalyası rota başında; 1529 |
| 10 | c678_sahne (siege) | viyana_kusatma | 3.1 | Viyana kuşatması (`city="viyana"`, gündüz, top ateşi); "27 EYLÜL 1529", VİYANA |
| 11 | c678_cift | ordu_75_100bin | 5.8 | simge + ASKER → "yetmiş beş" deyince 75.000 – 100.000 sayılır (sayım başlayana dek rakam gizli); yeniçeri bandı büyür; MODERN TAHMİN damgası |
| 12 | c678_sahne (siege) | yagmur_camur | 1.4 | aynı kale, yağmur (`weather="rain"`: koyu bulut, yağmur çizgileri, çamur) |
| 13 | c678_sahne (siege) | erken_kar_cekilme | 4.1 | "erken kar": `time="dusk", weather="snow"` (beyaz çatı/zemin, kar taneleri); EKİM ORTASI; GERİ ÇEKİLME + yeşil çekilme oku |
| 14 | map | karl_italya | 6.6 | Barselona→Cenova→Bologna rotası, Karl madalyası (varışta BOLOGNA yazısı), imparatorluk tacı; Viyana: kuşatma |
| 15 | map | 1532_sefer | 4.8 | 1532: İstanbul → Güns yönü rota; HEDEF: İMPARATOR |
| 16 | c7_gunluk | sefer_gunlugu | 5.0 | OSMANLI SEFER GÜNLÜĞÜ 1532: okunur tek ifade “İspanya kralı” (gerisi karalama) |
| 17 | c678_sahne (siege) | guns_kale | 2.6 | Güns: tepe üstünde küçük kale (`city="guns"`), top ateşi, kameranın kaleye yaklaşması; GÜNS |
| 18 | c678_cift | guns_700_800_25 | 5.3 | 700 – 800 KİŞİ (GARNİZON) · 25 GÜN |
| 19 | map | ordular_karsilasmadi | 5.9 | Viyana yakınında imparatorluk ordusu (BEKLEDİ) / Güns yönünde Osmanlı ordusu; İKİ ORDU HİÇ KARŞILAŞMADI |
| 20 | c7_unvan | unvan_imparator_sultan | 9.0 | OSMANLI BELGELERİ → Karl: GENELLİKLE İMPARATOR (üstü çizilir) → İSPANYA KRALI; Süleyman: İMPARATOR · YALNIZCA SULTAN |
| 21 | c7_ates | ates_kes_1547 | 4.1 | ATEŞKES 1547, SÜRE: BEŞ YIL, iki mühür (S, F) |
| 22 | c678_cift | 30bin_altin | 3.5 | FERDİNAND ÖDEYECEKTİ: 30.000 ALTIN · HER YIL (arka planda yağan paralar; "otuz" deyince sayım) |
| 23 | map | macaristan_kayip | 5.1 | Habsburg (Viyana TUTULDU) / Macaristan'ın büyük bölümü KAYIP (yeşil) |
| 24 | c7_yuk | yuku_kardesi_tasidi | 3.4 | YÜKÜN ÇOĞU: Şarlken üstü çizili/soluk (ŞARLKEN DEĞİL) — Ferdinand parlak (Kardeşi) |

Not: Viyana kuşatma kicker'ı (x=620) ve GÜNS kicker'ı (x=560) kule/kale ile çakışmasın diye sola alındı. Geçişler: savaşlarda `whip`, harita/belge çekimlerinde `fade`/`wipe`/`zoom`.

## (b) Bilinen kusurlar
- Macaristan bölgeleri (`macar_habsburg`, `macar_osmanli`, `erdel`) yaklaşık çokgenler; 1526'daki Zapolya/Ferdinand tarafları şematik. Harita taban kitindeki kaba dikdörtgen bölgeler mapdata'ya ait.
- İki ordunun konumları (Viyana yakını / Güns) şematik: Şarlken'in o ordudaki varlığı iddia edilmedi (A3 #9 çelişkili) → yalnız "İMPARATORLUK ORDUSU"; hedef olarak "İMPARATOR" tacı çizildi, kişi madalyası konmadı.
- c7_hukum: Süleyman çubuğu 1560'a ok ile açık uçlu (ölüm yılı ekrana konmadı).
- Siege sahnesinde Viyana ve Güns kale silüetleri lab'ın şematik çizimleri (gerçek mimariye birebir uymaz); sancak renkleri tarafları gösterir (Habsburg haçlı kızıl-beyaz, Osmanlı yeşil hilal).
- Güns top isabetinde tek tük blok piksel enkaz kalıntısı görülebiliyor (lab'ın `_impacts`'i; hareket içinde belli olmuyor).
- #12 çok kısa (1.4 sn): anlatı "Yağmur, çamur ve erken kar" — yağmur ve çamur tek çekimde, kar ikinci çekimde; geçiş `fade 0.45`.
- `--check` ms/kare duvar saatiyle ölçüldüğünden yoğun makinede c7_vasal / c7_unvan gibi geçiş penceresine düşen çekimler sahte uyarı verebiliyor. CPU süresiyle en yüksek 376 ms (c7_vasal, fade penceresinde iki çekim birden), tipik 100–230 ms.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- Süleyman Kanuni; 1520'den sultan; Şarlken İspanya kralı 1516 / seçim 1519 — CONFIRMED (A3 #20). "AYNI YILLAR": Şarlken 1516–1556 (1556 = feragat; A5 #19 NİTELİKLİ).
- Hiç karşılaşmadılar — NİTELİKLİ (A3 #20), "BİLDİĞİMİZ KADARIYLA" metniyle.
- Mohaç 29 Ağustos 1526, II. Lajos'un boğulması — CONFIRMED (A3 #3). Çocuksuz; Ferdinand; soylular ikiye bölündü — CONFIRMED (A3 #3). Zapolya Osmanlı vasalı — NİTELİKLİ (A3 #4).
- Viyana 1529; 27 Eylül — CONFIRMED (A3 #5-6); ordu 75.000–100.000 — NİTELİKLİ → MODERN TAHMİN damgası. Ekim ortası geri çekilme, yağmur/çamur/kar — CONFIRMED (A3 #6).
- Şarlken o hafta İtalya'da (Barselona→Cenova→Bologna; taç) — CONFIRMED (A3 #7; Bologna 5 Kasım 1529, taç 24 Şubat 1530: ekrana tarih konmadı).
- 1532 sefer, günlükte "İspanya kralı" — CONFIRMED/NİTELİKLİ (A3 #2, #8). Güns: 700–800 kişi, 25 gün — CONFIRMED (A3 #8).
- Osmanlı belgeleri "imparator"ı yalnız sultana ayırır (genellikle) — NİTELİKLİ (A3 #2) → GENELLİKLE etiketi.
- 1547 beş yıllık ateşkes, Ferdinand yılda 30.000 altın — NİTELİKLİ (A3 #18; birim/taraf kaynağa göre değişir): ekranda yalnız "ALTIN".
- Viyana tutuldu; Macaristan'ın büyük bölümü kaybedildi; yükü Ferdinand taşıdı — NİTELİKLİ (A3 #19) / YORUM.

## (d) Ana ajandan istekler / uyarılar
1. `shots.py` genel şablonlarında demet çapa çöküyor (bkz. notlar_c6.md (d)-1); `c678_medals`, `c678_cift` ile aştım.
2. Aynı `theatre` sahnesini farklı p (özellikle liste: `armies`, `ships`) ile kullanırken önbellek anahtarı listeleri dışladığı için benzersiz skaler `tag=` verdim; diğer yazarlar için de geçerli.
3. `check` ölçümü CPU süresine (`time.process_time`) alınırsa yoğun makinede sahte uyarılar kalkar (isteğe bağlı).
