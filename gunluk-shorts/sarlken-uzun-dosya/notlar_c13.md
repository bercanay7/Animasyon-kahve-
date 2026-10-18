# Bölüm 13 — Hesap · yazar notları (BÖLÜM YAZARI D)

**Dosyalar:** `scenes_c13.py` (SHOTS) · `shots_c13.py` (c13_ önekli türler: `c13_open`, `c13_network`, `c13_split`, `c13_crown`, `c13_balance`, `c13_game`, `c13_life`, `c13_final`; `branches_extra`, `reform_extra`) · `shots_c9.py` (`circum_extra`: dünya turu rotası c9 ile ortak) · `shots_c12.py` (`crack_pts/_crack` çatlak yardımcısı) · `d_common.py` (D ortak: `A()`, `wd_vs`, `tag`, `cameo`, `draw_medal_plain` …).
**Süre** 80.8 sn (+ compose'un 7 sn kapanışı) · **14 çekim** (bölüm kartı ve outro hariç) · ort. 5.8 sn/çekim · `--check`: **uyarı yok** (bölüm ort. ≈ 125–150 ms/kare (makine yüküne göre), en ağır çekim ≤ 225 ms; 2× süper-örnekli stage.py ile ölçüldü).
**Ton:** son bölüm — açılan altın ışık, sonra sade soru. **'BİRÇOK TARİHÇİ' damgası YOK** (c13s5 metni değişti). **Son çekim = beş cephe + "HANGİSİNİ BIRAKIRDIN?"**; kapanış compose'ta 7 sn eklenir. Bölüm genelinde tüm beş cephe ikonları HUD'da yanık.

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | c13_open | 0:00.0 | 3.8 | besinci_cephe | Beş cephe sırası (dördü sönük, beşincisi yanar), "BEŞİNCİ CEPHE", büyük miras (aile ağacı) simgesi, "MİRAS" |
| 2 | c13_network | 0:03.8 | 8.5 | akrabalik_agi | Dört taç/taht (BURGONYA, AVUSTURYA, ARAGON, KASTİLYA) sırayla; hepsi ortadaki genç Karl madalyasına bağlanır; "tek ülke" lekesi ("değil" sözünde) dağılır; evlilik halkalı ağ; "AKRABALIK AĞI" |
| 3 | c13_split | 0:12.3 | 5.3 | kartal_ikiye | Karl → Habsburg kartalı → "HABSBURG HANEDANI"; "kola" sözünde çatlar, "ayrıldı"da ikiye açılır, yarılar renklenir (kızıl / bronz) |
| 4 | map | 0:17.6 | 5.8 | iki_kol_harita | "İSPANYA KOLU" (İspanya, Napoli, Milano, Hollanda — Habsburg kırmızısı) + FELİPE madalyası; "AVUSTURYA KOLU" (Avusturya, Bohemya, Habsburg Macaristan'ı — turuncu) + FERDİNAND madalyası |
| 5 | c13_crown | 0:23.4 | 3.6 | tac_catlar | "EVRENSEL HIRİSTİYAN İMPARATORLUK" kicker; altın taç boydan boya çatlar, yarılar kayar |
| 6 | map | 0:27.0 | 4.9 | reform_yayilir | Almanya turkuaz (protestan); "REFORM" noktasından dalgalar; "AUGSBURG" şehri; "AUGSBURG BARIŞI", "LUTHERCİLİK TANINDI" |
| 7 | c13_balance | 0:31.9 | 7.4 | denge_terazi | "AVRUPA"; taç sol kefede ağır ("tek imparatorluk") → "yerine"de kalkar, kiriş sönümlü salınır → sekiz renkli kalkan iki kefeye dizilir; "DENGE" |
| 8 | map | 0:39.2 | 5.4 | dunya_kuculdu | Dünya haritası, ilk dünya turu rotası (c9 ile aynı şematik rota, daha hızlı), "1519 – 1522" |
| 9 | map | 0:44.6 | 2.4 | atlantik_ticaret | Atlantik: Sevilla → Karayipler/Panama (altın) ve Yeni İspanya → Sevilla (gümüş) rotaları, gemiler; "SEVİLLA", "TİCARET YOLU" |
| 10 | wd_vs | 0:47.0 | 5.2 | tartisma_hatirla | "SÖMÜRGECİLİĞİN AHLÂKI": SEPÚLVEDA ⟷ LAS CASAS madalyaları, ortada sallanan terazi |
| 11 | c13_game | 0:52.2 | 7.0 | oyun_paneli | Jenerik strateji-oyunu arayüzü: üst kaynak çubuğu (simge + dolgu, sayı yok), mini harita (Karl'ın kendi devletleri sırayla yanar, tek taç hepsine ince çizgiyle bağlanır), "DEVLETLER" listesi (hepsinde aynı hükümdar madalyası), "KİŞİSEL BİRLİK — 1 HÜKÜMDAR · ÇOK DEVLET" kartı |
| 12 | c13_life | 0:59.2 | 4.0 | oyun_degil_omur | "OYUN" üstü kırmızı çizgiyle çizilir → kum saati + "ÖMÜR"; 1500 ⟶ 1558 çubuğu uzar |
| 13 | wd_vs | 1:03.2 | 7.0 | kaybeden_kim | ŞARLKEN (O mu?) ⟷ FİKİR (küre üstünde taç; "Tek adam, bütün dünya?"), ortada büyük soru işareti |
| 14 | c13_final | 1:10.2 | 10.7 | hangisini_birakirdin | **Son çekim:** beş cephe (1 BANKACI · 2 KEŞİŞ · 3 KRAL · 4 SULTAN · 5 MİRAS) sırayla gelir; "HANGİSİNİ BIRAKIRDIN?"; "YORUMLARDA YAZ" balonu; vurgu cephelerde sırayla dolaşır |
| — | outro (compose) | 1:20.8 | 7.0 | | "ZAMAN KURYESİ · TESLİMAT TAMAM" + beş cephe + bitiş ekranı yuvaları |

Tür çeşitliliği: özel ×8, harita ×4, karşılaştırma ×2. Hiçbir tür üst üste 3'ü geçmiyor (haritalar 8–9 ardışık 2).

## 2. Bilinen kusurlar / dürüst notlar
1. **Oyun paneli jenerik:** gerçek bir oyunun arayüzü veya markası DEĞİL; tüm metinler Türkçe. Kaynak çubukları dekoratif (sayı yok). Devlet listesinde **yalnız Karl'ın kendi hükmettiği devletler** var (Kastilya, Aragon, Napoli, Sardunya, Hollanda, Milano); Avusturya/Bohemya Ferdinand'ındı, bilinçli olarak yok. Mini harita panele ekran-merkezli çizilip kaydırılıyor (`mapsk.Cam` cx/cy kaydırması karo seçimini bozduğu için).
2. **Reform haritası:** Almanya'nın tamamı protestan renginde (modern sınır, yaklaşık); dalgaların çıktığı nokta Wittenberg koordinatlarında ama **şehir adı yazılmadı** ("REFORM" etiketi): araştırma dosyalarında Wittenberg geçmiyor (c4 yazarının da aynı kapı kararı).
3. **Kalkanlar** (denge) jenerik renkli kalkanlar: belirli devletleri temsil etmiyor, etiketsiz; sayı sekiz ('birbirini dengeleyen devletler' için çokluk).
4. **Kartal** iki yarıya bölünen stilize `eagle` simgesi: gerçek arma değil. Yarılar kızıl/bronz renge döner (İspanya kolu / Avusturya kolu çağrışımı; ayrıca haritada rengi bağlanır).
5. **Dünya turu** şematik ve c9 ile aynı rota (bilinçli yankı); Pasifik geçişi antimeridyende bölünüyor. **Atlantik ticaret rotaları** üç şematik çizgi (tam filo rotası değil).
6. **FİKİR yuvası** (s8) küre + taç soyut simgesi: 'tek adamın bütün dünyayı taşıyabileceği fikri' görseli; yorum, olgu değil.
7. **Son çekim 10.7 sn:** beş ikon tam yerinde sakin; yalnız vurgu dolaşıyor. Altta balon "YORUMLARDA YAZ"; ilerleme çubuğuna 14 px mesafede.
8. **c13_open** bölüm kartından sonra ilk çekim; `fade` yok (kart geçişi compose'ta).
9. **`wd_vs` ×2** (s6c, s8) aynı türün iki farklı kullanımı: biri madalya-madalya, diğeri madalya-soyut simge.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| BEŞİNCİ CEPHE · MİRAS (+ dört sönük cephe) | 1 | evet (c13s1) | YORUM (çerçeve) |
| BURGONYA · AVUSTURYA · ARAGON · KASTİLYA · AKRABALIK AĞI · halkalar | 2 | evet ('dört büyük taht … akrabalık ağı') | YORUM (A1 #2: dört hane; evlilik halkaları: Maksimilyan–Mary, Ferdinand–Isabella, Philip–Joanna genel bilgi/A1) |
| HABSBURG HANEDANI (kartal ikiye) | 3 | evet (c13s3) | CONFIRMED (A5 #24; metin 'bıraktıklarıyla … iki kola ayrıldı', 'ölünce' yok) |
| İSPANYA KOLU → FELİPE (Oğlu) · AVUSTURYA KOLU → FERDİNAND (Kardeşi) | 4 | evet (c13s3) | CONFIRMED (A5 #24; A1 #19). Harita bölgeleri yaklaşık |
| EVRENSEL HIRİSTİYAN İMPARATORLUK (çatlayan taç) | 5 | evet (c13s4) | CONFIRMED (A5 #24) |
| REFORM · AUGSBURG · AUGSBURG BARIŞI · LUTHERCİLİK TANINDI | 6 | evet (c13s4 'Augsburg Barışı Lutherciliği tanıdı') | CONFIRMED (A5 #24); Almanya boyaması yaklaşık |
| AVRUPA · DENGE (terazi, kalkanlar) | 7 | evet (c13s5, YORUM: 'birçok tarihçi' kalktı) | YORUM (damga yok) |
| 1519 – 1522 · dünya turu rotası | 8 | evet (c13s6 'ilk dünya turu') | CONFIRMED (A4 #17); rota şematik |
| TİCARET YOLU · SEVİLLA · Atlantik rotaları | 9 | evet ('Atlantik bir ticaret yolu oldu') | YORUM (A4 #11); Sevilla/rota şematik |
| SÖMÜRGECİLİĞİN AHLÂKI · SEPÚLVEDA ⟷ LAS CASAS | 10 | evet ('en bilinen büyük tartışma') | YORUM +H38 ('ilk' denmiyor; Montesinos 1511 öncül); isimler CONFIRMED (A4 #21) |
| KİŞİSEL BİRLİK · 1 HÜKÜMDAR — ÇOK DEVLET · HÜKÜMDAR · DEVLETLER (KASTİLYA, ARAGON, NAPOLİ, SARDUNYA, HOLLANDA, MİLANO) | 11 | evet (c13s7 'kişisel birlik') | YORUM +H39 (oyun terimi KISMEN doğrulandı; resmî kaynak yok). Devlet adları Karl'ın hükmettikleri: CONFIRMED (A1/A5) |
| OYUN (üstü çizili) · ÖMÜR · 1500 ⟶ 1558 | 12 | evet ('oyun olarak değil, ömür olarak') | YORUM; yıllar CONFIRMED (A1 #1) |
| ŞARLKEN · FİKİR · soru işareti | 13 | evet (c13s8) | YORUM (retorik soru) |
| 1 BANKACI · 2 KEŞİŞ · 3 KRAL · 4 SULTAN · 5 MİRAS · HANGİSİNİ BIRAKIRDIN? · YORUMLARDA YAZ | 14 | evet (c13s9) | YORUM (etkileşim çağrısı) |

## 4. Montaj/ses için vurgu anları (global sn)
Beşinci cephe 1198.9 · dört taht 1202.8 · kartal çatlar/açılır 1214.7–1214.9 · taç çatlar 1224.6 · AUGSBURG 1227.6 · denge terazi (taç kalkar) 1233.2 · dünya turu 1241.2 · tartışma (terazi) 1246.0 · "kişisel birlik" kartı 1252.8 · ÖMÜR 1260.2 · son soru 1272.0 · yorum balonu 1273.8.

## 5. Ana ajana istekler / bulgular
1. **compose.py / shots.py — Türkçe büyük harf:** `title.upper()` (HUD: compose.py:203; bölüm kartı: shots.py:264–265; sayaç birimi shots.py:541) "i"→"I" yaptığından İ noktaları kayboluyor (c9: "YENI DÜNYA … VICDAN"). c13'ün "HESAP" başlığı etkilenmiyor. Öneri: `s.replace("i","İ").replace("ı","I").upper()`.
2. **Kapanış (outro) bağlantısı:** `c13_final` 0.9 sn `fade` ile giriyor; compose'un 7 sn'lik outro'su son çekimin hemen ardından başlıyor. `c13_final` sonunda ikonlar tam görünür kalıyor (kararma yok) → outro'ya `fade`/çapraz geçiş eklenirse yumuşak olur.
3. **Paylaşılan `medals/emblem/doc/quote/counter` türleri** demet çapalarla çalışmıyor (`at + x`); c13'te `wd_vs` (çapalı kopya) kullanıldı.
4. **`sk.text_width("")`** boş dizgede çöküyor; **`shot(label=…)` ↔ tür `label` çakışması**; **`theatre` önbelleği ~5 sahne** (c13'te diorama yok); **`check()` geçiş penceresi yanlış pozitifi** (c13'te etkilenmedi).
5. **Bölüm kartı girişi sert kesme** (`chapter_card`a `tr` verilmiyor): c12'nin son kare siyaha solduğu için yumuşak, ama genel olarak kart önünde kısa siyaha dalış önerilir.
6. **Reform haritasında Wittenberg adı yok** (kaynak kapısı). Eklenmek istenirse araştırma dosyalarına Wittenberg/95 Tez maddesi girmeli; kod: `shots_c13.reform_extra` içinde etiket "REFORM" → ad.
7. **Madalya çizim hızı (öneri):** `SH.draw_medal` her karede görüntüyü yeniden boyutlayıp gölgeyi bulanıklaştırıyor (ölçüm ≈ 74 ms/çizim, 640 px). `d_common.fast_medal` aynı görünümü önbellekli görüntü + önbellekli gölgeyle çiziyor (≈ 26 ms/çizim; 3 test karesinde en büyük piksel farkı 1/255). D bölümlerindeki tüm madalyalar (`wd_*`, `cameo`, `c9_durer`, `c12_*`, `c13_*`) bunu kullanıyor; aynı önbelleği ortak `shots.draw_medal`a almak tüm bölümlerde madalya çekimlerini ≈ 2–3× hızlandırır (paylaşılan `medal` türü hâlâ yavaş yolu kullanıyor).
8. **qa_program.py / qa_text.py sonuçları (04:25 UTC):** `--static` engelleyici/uyarı yok; örnekleme (140 kare, 2 işçi) 3 uyarı verdi ve üçü de tek seferlik ilk-kare pişirmesi: yüksek zoom harita karoları (`yuste_harita`, zoom 6.6) ilk karede ≈ 6 sn sürüyor, sonraki kareler ≈ 100–150 ms; büyük simge sprite'ı ve ilk madalya pişirmesi yük altında 450–590 ms'ye çıkabiliyor (`--check` ısınmış önbellekle < 220 ms). `qa_text.py` yalnız yazıyla yazılmış sayıları ("elli beş", "kırk altı", "on sekiz", "yaklaşık yüz bin"), sayaç ara değerlerini ve kaynaklı yılları (1500–1558, 1519–1522, 1515 = 1555−40) işaretledi; hepsi bilinçli/kaynaklı.
