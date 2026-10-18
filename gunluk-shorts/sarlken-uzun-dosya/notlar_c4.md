# Bölüm 4 — Worms'ta Bir Keşiş · yazar notları (BÖLÜM YAZARI B)

**Dosyalar:** `scenes_c4.py` (SHOTS) · `kinds_c4.py` (c4_ önekli çekim türleri + `c4_nave` sahnesi) · `bw_lib.py` (ortak yardımcılar: push, paper, stamp2, tag, curve_arrow, chain_links, draw_medal2, `bw_theatre` güvenli sarmalayıcı, `scene_pt`) · `icons_b.py` (b_ simgeleri: b_press, b_friends, b_body, b_drop, b_heart, b_flame, b_saltire, b_forbid…).
**Süre** 113.9 sn · **20 çekim** (bölüm kartı hariç) · ort. 5.7 sn/çekim · `--check`: **uyarı yok** (ort. ≈ 100 ms/kare, en ağır `c4_dawn_scroll` ≈ 195 ms; paylaşılan makinede CPU yoğunken değerler ≈ 2× çıkabilir).
**Renk kodu:** Habsburg kızıl/altın · Protestan petrol (teal) · mühür/damga kırmızı · parşömen sıcak bej. Anlatı ritmi: yargı salonu gerilimi; sayfa/damga/sayaç çekimleri arasına lab dioramaları serpiştirildi.

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | map | 0:00 | 3.8 | worms_harita | Almanya (taralı bölge, "ALMANYA"), WORMS nabız halkaları, "NİSAN 1521" plakası |
| 2 | bw_theatre / reichstag | 0:03.8 | 3.1 | reichstag | Lab `reichstag`: koridorda tek başına keşiş, masada kitaplar, tahtta imparator, kalabalık; kamera keşişe iner (geçiş 0.4 sn fade); sol üstteki parlak pencere HUD bölüm başlığını yuttuğu için `bw_lib.hud_scrim` ile ince karartma (HUD sönerken silinir) |
| 3 | c4_duel | 0:06.9 | 3.6 | karl_luther | İki madalya: V. KARL (altın, "21 yaşında") ↔ MARTİN LUTHER (petrol); aralarında kılıç simgesi |
| 4 | c4_theses | 0:10.5 | 6.2 | 95_madde | Parşömen "95 MADDE" satır satır yazılır; günah affı = kese+sikke üstünde yasak halkası; sayaç 95; "DÖRT YIL ÖNCE · 1517" |
| 5 | map | 0:16.8 | 3.7 | matbaa_yayildi | Matbaa simgesi (Almanya'nın orta-doğusundaki çıkış noktasından) 12 Alman şehrine yayılan altın çizgiler; tüm Almanya kadrajda |
| 6 | c4_safeconduct | 0:20.5 | 5.1 | guvenli_gecis | GÜVENLİ GEÇİŞ belgesi + K mührü; 3×7 gün ızgarası ve büyük sayaç 1→21 "GÜN" (sayaç "yirmi bir" sözcükleriyle bitiyor) |
| 7 | c4_books | 0:25.6 | 6.8 | kitaplar | Keşiş siluet, masaya düşen 9 kitap, mum, pencere; "SENİN Mİ?" → "HEPSİ?" |
| 8 | c4_answer | 0:32.4 | 8.8 | almanca_latince | Kum saati çevrilir "BİR GÜN" → iki belge ALMANCA / LATİNCE → "VAZGEÇMİYOR" |
| 9 | c4_protocol | 0:41.2 | 10.1 | tutanakta_yok | Meşhur söz kelime kelime belirir → hayalete döner + **RİVAYET** → RESMÎ TUTANAK (söz yok; boşluk) → mor mürekkeple sonradan eklenir → **TUTANAKTA YOK / SONRADAN EKLENMİŞ** |
| 10 | c4_dawn_scroll | 0:51.3 | 4.1 | bildiri | Şafak, sur silueti; açılan ferman "İMPARATORUN BİLDİRİSİ", mühür |
| 11 | c4_ancestors | 0:55.4 | 9.3 | atalar | Üç kemer: kartal (ALMAN İMPARATORLARI), kale (İSPANYA KRALLARI), kızıl Burgonya haçı (BURGONYA DÜKLERİ); sonra Roma anahtarları + zincirle bağlanma |
| 12 | bw_theatre / c4_nave | 1:04.6 | 6.4 | bin_yil | Kendi yazdığım gotik nef: ışığa doğru tek başına küçük keşiş; "BİN YIL", soru işareti |
| 13 | c4_pledge | 1:11.0 | 8.3 | alti_sey | Altı madalyon (KRALLIKLAR, DOSTLAR, BEDEN, KAN, CAN, RUH) sırayla gelir, ortada "DAVA" haçına toplanır |
| 14 | c4_backdate | 1:19.4 | 7.3 | ferman_geriye | WORMS FERMANI parşömeni; zaman ekseni (LUTHER AYRILDI → FERMANIN TARİHİ ← İMZA); geri ok; **GERİYE DÖNÜK TARİHLİ** damgası |
| 15 | c4_banned | 1:26.6 | 6.2 | yasak | Luther madalyası + **KANUN DIŞI** damgası; OKUMAK / BASMAK / SATMAK satırları üstü çizilir |
| 16 | bw_theatre / road_night | 1:32.9 | 3.7 | gece_yolu | Lab `road_night`: meşaleli atlılar (4), “KAÇIRILDI” |
| 17 | bw_medal | 1:36.6 | 4.3 | seçmen | Frederik madalyası, levha "SAKSONYA SEÇMENİ" (dip geçişi) |
| 18 | bw_theatre / tower (wartburg) | 1:40.8 | 6.0 | wartburg | Lab `tower/wartburg`: yazan figür, mum; "WARTBURG KALESİ", “ŞÖVALYE JÖRG” |
| 19 | c4_book | 1:46.8 | 3.3 | yeni_ahit | Açık kitap; "YENİ AHİT"; sağ sayfaya "ALMANCA" başlığıyla yazı yazılır (tüy kalem, mum) |
| 20 | c4_finale | 1:50.1 | 3.7 | fikir | FERMAN parşömeni alttan yanar; sağda altın alev "FİKİR" |

Çekim türü çeşitliliği: harita ×2, lab diorama ×3 (+ kendi nef sahnem), madalya ×2 (+duel/banned içinde), belge/parşömen ×8, sayaç/ızgara, kum saati, zincir/anahtar, ferman yanışı. Hiçbir tür üst üste 3'ten fazla gelmiyor.

## 2. Bilinen kusurlar / dürüst notlar
- **İlk-kare pişirme maliyeti** (tek seferlik): harita ilk karesi ≈ 2.6 sn (karo önbelleği), lab sahneleri ilk kare 3–7 sn (reichstag ≈ 6–7 sn). Sıralı render'da sorun değil.
- **`--check` artefaktı:** bir çekimin ön-geçiş penceresine (geçiş süresi kadar önce) sonraki çekimin ilk pişirmesi düşüyor ve önceki çekimin ölçümüne yazılıyor; #1→#2 geçişini 0.4 sn'lik fade yaptım ki yanlış "YAVAŞ" uyarısı çıkmasın. Gerçek render'a etkisi yok.
- **Wartburg:** lab figürü (yazar) sakalsız — anlatıdaki "sakal bırakıp" görsele yansımıyor (lab kusuru). Kimlik değişikliği anlatısı etiketle (“ŞÖVALYE JÖRG”) taşınıyor.
- **Reichstag:** kalabalık siluetleri birbirine benzer, keşiş figürü figür-lab sürümüyle güncellenir (lab notu). **road_night:** alt 1/4 geniş siyah (lab notu); etiket sol üstte, çakışma yok.
- **c4_protocol:** iki damga bilerek üst üste biniyor ve kâğıt kenarından taşıyor (kauçuk damga görünümü); metinler okunaklı. Meşhur sözün tırnak işaretleri ilk karelerde kelimelerden uzak (tek kelime varken).
- **c4_backdate:** zaman ekseni şematik; ekranda **gün/tarih YOK** (metin 8 Mayıs / imza 25–26 Mayıs kaynakta tutarsız: A2 #8). "Fermanın tarihi" işareti ayrılıştan önceye konuldu (geriye dönük).
- **Matbaa haritası:** 12 Alman şehri adsız nokta (adlar anlatıda/araştırmada yok). YONETMEN_NOTLARI s3'ün istediği **WİTTENBERG etiketi YAZILMADI** (anlatıda ve `arastirma/*.md` / `kaynaklar.md`'de geçmiyor → kaynak kapısı); çıkış noktası yine Wittenberg koordinatında ama adsız. Etiket istenirse `scenes_c4.py` matbaa çekimine `cities=[dict(lon=12.65, lat=51.87, name="WİTTENBERG", kind="town", at=("c4s3","Matbaa",-0.2), side="r", size=34)]` eklenir.
- **c4_ancestors / c4_pledge:** armalar ve simgeler stilize (kartal = Alman imparatorları, kale = Kastilya, kızıl çapraz = Burgonya); gerçek arma değil.
- `c4_nave` lab sahnesi değil; perspektifli gotik kemerlerden oluşan basit, kendi yazdığım diorama.
- Levha/etiketlerde Türkçe büyük harf kuralı: **MARTİN LUTHER** (İ'li).

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| NİSAN 1521 · WORMS | 1 | evet (c4s1) | CONFIRMED (A2 #2) |
| ALMANYA (bölge etiketi) | 1 | c4s3'te "Almanya'ya" | etiket (ayrıca A1/A2 bağlamı) — "Kutsal Roma İmparatorluğu" yazmadım (anlatı/araştırmada yok) |
| V. KARL · İmparator · 21 yaşında | 3 | evet (c4s2) | CONFIRMED (A1 #1; 21 yıl 2 ay) |
| MARTİN LUTHER · Keşiş | 3, 15 | evet | CONFIRMED (A2 #5; 'keşiş' çevirilerde monk/friar ayrışır) |
| DÖRT YIL ÖNCE · **1517** | 4 | "dört yıl önce" evet; **1517 türetilmiş** (1521−4) + YONETMEN_NOTLARI s3 | HAFIZA H13 → web doğruladı (yayılma hızı kaynağa göre değişir; ekranda hız iddiası yok) |
| 95 MADDE · GÜNAH AFFI SATIŞI | 4 | evet | HAFIZA H13 (web doğruladı) |
| matbaa çizgileri (adsız çıkış noktası) | 5 | evet ("Matbaa … Almanya'ya yaydı") | YORUM/şematik; **WİTTENBERG etiketi kaldırıldı** (kaynak kapısı) |
| GÜVENLİ GEÇİŞ · 21 GÜN | 6 | evet | CONFIRMED (A2 #1) |
| SENİN Mİ? · HEPSİ? | 7 | evet | CONFIRMED +H14 (soran Trier yetkilisi; ekranda isim yok) |
| BİR GÜN · ALMANCA · LATİNCE · VAZGEÇMİYOR | 8 | evet | CONFIRMED (A2 #2) |
| “Ben buradayım, başka türlü yapamam” + **RİVAYET · TUTANAKTA YOK · SONRADAN EKLENMİŞ** | 9 | evet | RİVAYET (A2 #4, ANEKDOT) — damgalar anlatıdaki hedge'in aynısı |
| RESMÎ TUTANAK · İMPARATORUN BİLDİRİSİ | 9, 10 | evet | CONFIRMED (A2 #5–#6); bildirinin dili/okuyan ekranda belirtilmedi |
| ALMAN İMPARATORLARI · İSPANYA KRALLARI · BURGONYA DÜKLERİ | 11 | evet | CONFIRMED (A2 #5; çeviri) |
| BİN YIL | 12 | evet | CONFIRMED (A2 #5) |
| KRALLIKLAR · DOSTLAR · BEDEN · KAN · CAN · RUH · DAVA | 13 | evet | CONFIRMED (A2 #5; kelimesi kelimesine alıntı değil, çeviri) |
| WORMS FERMANI · LUTHER AYRILDI / FERMANIN TARİHİ / İMZA · GERİYE DÖNÜK TARİHLİ | 14 | evet | NİTELİKLİ (A2 #8: tarihler kaynaklarda çelişkili → ekranda tarih yok) |
| KANUN DIŞI · OKUMAK / BASMAK / SATMAK | 15 | evet | CONFIRMED (A2 #9) |
| “KAÇIRILDI” | 16 | evet | CONFIRMED (A2 #10; tırnaklı) |
| SAKSONYA SEÇMENİ · **Frederik** | 17 | "Saksonya Seçmeni" evet; **"Frederik" adı hayır** | A2 #1/#10 'Frederick' — adın yazılışı Türkçeleştirildi |
| WARTBURG KALESİ · “ŞÖVALYE JÖRG” | 18 | evet | CONFIRMED +H15 ('Şövalye' = Junker, genç soylu) |
| YENİ AHİT · ALMANCA | 19 | evet | CONFIRMED +H15 (Yeni Ahit çevirisi araştırmada yok, düşük risk); sayfaya "LATİNCE" yazmadım |
| FERMAN · FİKİR | 20 | evet | YORUM (özet; A2 #9 'hiç tam uygulanmadı') |

## 4. Montaj/ses için vurgu anları (global sn)
RİVAYET damgası 361.7 · TUTANAKTA YOK damgası 364.3 · SONRADAN EKLENMİŞ damgası 365.5 · güvenli geçiş mührü 338.8 · 21 sayacı 340.0–340.6 · kitaplar masaya düşer 341.7 (+0.2 sn aralıkla 9 kitap) · kum saati çevrilir 351.2 · bildiri mührü 370.2 · GERİYE DÖNÜK damgası 400.4 · KANUN DIŞI damgası 403.6 · Yeni Ahit yazılmaya başlar 424.6 · ferman tutuşur 428.4.

## 5. Ana ajana istekler / bulgular
1. **compose.py — Türkçe büyük harf hatası:** bölüm kartı ve sol üst HUD başlığı `.upper()` ile üretiliyor: "WORMS'TA **BIR** KEŞ**I**Ş" → doğrusu "WORMS'TA **BİR** KEŞİŞ" (c11: "ADAMIN KEND**I**S**I**" → "KENDİSİ"). Türkçe-farkında büyük harf (i→İ, ı→I) gerekli; HUD ikonlarının alt yazıları da kontrol edilmeli.
2. **`SH.draw_medal`** her karede `medal_image` + blur üretiyor (önbellek yok). `bw_lib.draw_medal2` (lru_cache'li sprite + gölge) aynı görünümü 2–3× hızlı çiziyor; ana kodda benzer önbellek önerilir.
3. **Varsayılan geçiş:** `tr` verilmezse sert kesme; bütün çekimlerimde `tr=` açık verildi (başka yazarlar da dikkat etmeli).
4. **Sahne önbelleği** (`stage._SCENES`) yalnız 5 sahne tutuyor; aynı sahneye başka `p` ile dönülürse yeniden pişer (3–8 sn).
5. **`bw_theatre`** (bw_lib): lab sahnesi hata verirse render çökmesin diye yer tutucu çizer ve stderr'e "[bw_theatre] '…' sahnesi hata verdi" yazar — final render logunda bu satırı arayın (şu an 0 hata).
6. **Hız ipucu (tüm yazarlar için):** `bw_lib.py` içinde kare başı maliyeti ≈ yarıya indiren önbellekli yardımcılar var — `static_backdrop` (bg+ışın+duo_glow tek blit), `dust2` (saveLayer'sız toz), `draw_icon2` (gölge/ışıma bulanıklığı önbellekli), `gold2` (altın yazı ışıması önbellekli), `glow_blit`, `bw_medal` (önbellekli madalya; `shots.medal` ile aynı parametreler). Paylaşılan `sk.dust`, `icons.draw_icon`, `Frame.gold(glow=)` ve `SH.draw_medal` en pahalı kalemler; ortak dosyalara yazmadım.
7. Ekranda **1517** (türetilmiş: 1521−4; `kaynaklar.md` H13'te geçiyor) var; kaldırmak: `c4_theses`'de `year_at`. WİTTENBERG etiketi kaynak kapısı gereği çıkarıldı (bkz. §2).
