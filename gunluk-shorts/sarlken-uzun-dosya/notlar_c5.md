# Bölüm 5 — İmparator Hep Başka Yerde · yazar notları (BÖLÜM YAZARI B)

**Dosyalar:** `scenes_c5.py` (SHOTS) · `kinds_c5.py` (c5_ önekli çekim türleri, harita `extra`'ları, köylü overlay'i) · `bw_lib.py` · `icons_b.py` · `rider_b.py` (Tiziano çerçevesindeki atlı siluet).
**Süre** 108.6 sn · **21 çekim** (kart hariç; hedef 16–20'nin bir fazlası — #4/#5 aynı lab sahnesinde iki ayrı overlay, #10/#11 kısa anlatı parçaları) · ort. 5.2 sn/çekim · `--check`: **uyarı yok** (ort. ≈ 106 ms/kare; en ağır `c5_authors` ≈ 220 ms [ilk-kullanım ikon pişirmesi], `c5_ideas` ≈ 160 ms; CPU yoğunken ≈ 2× çıkabilir).
**Ton:** yol/kervan — toprak, duman, harita okları; sonunda c0'ın salonuna dönüş. Renk kodu: Habsburg kızıl · Protestan petrol · Fransa kraliyet mavisi · Osmanlı orman yeşili · gümüş = Tiziano/anma.

## 1. Çekim listesi
| # | tür | bölüm içi | süre | etiket | ne gösteriyor |
|---|---|---|---|---|---|
| 1 | map | 0:00 | 5.4 | almanyadan_ayrildi | Almanya (taralı) → taç Worms'tan İspanya'ya uçar; "9 YIL" kum saati paneli; geri dönüş yolu kırmızı kesikli + yasak halkası |
| 2 | map | 0:05.4 | 5.6 | uc_cephe | Taç ortada; İSPANYA (kızıl), FRANSA (mavi), OSMANLI (yeşil) bölgelerinden taca üç ok |
| 3 | c5_ideas | 0:11.0 | 3.0 | fikirler_yayildi | Alev simgesinden uçuşan risale yaprakları, "LUTHER'İN FİKİRLERİ" (whip geçişle bir sonrakine) |
| 4 | bw_theatre / field | 0:14.1 | 3.3 | koylu_savasi | Lab `field`: alacakaranlık, dirgenli köylüler, haçlı bayraklar, duman/ateş; "1524", "KÖYLÜ SAVAŞI" |
| 5 | bw_theatre / field | 0:17.3 | 4.3 | luther_istememisti | Aynı sahne, kamera yaklaşır; Luther madalyası + yasak halkası + "LUTHER İSTEMEMİŞTİ"; "70.000 – 100.000 KİŞİ ÖLDÜ" + "TAHMİN" |
| 6 | c5_speyer | 0:21.6 | 7.2 | speyer | 1529 · SPEYER; jeton sütunları KATOLİK ÇOĞUNLUK ↔ AZINLIK; WORMS FERMANI parşömeni + "YENİDEN YÜRÜRLÜKTE" damgası |
| 7 | c5_protest | 0:28.9 | 7.8 | protestan | BİRKAÇ PRENS (kalkanlar), 14 ŞEHİR (kule); "İTİRAZ" etiketi; PROTESTO → **PROTESTAN** (O→AN harf dönüşümü) |
| 8 | c5_confession | 0:36.7 | 6.6 | augsburg_itirafi | 1530 · AUGSBURG; etiket PROTESTANLAR; belge "AUGSBURG İTİRAFI" yazılır, mühürlenir, imparatorun tacına doğru kayar |
| 9 | c5_authors | 0:43.3 | 4.2 | ana_yazar | LUTHER (solgun + yasak halkası) ↔ MELANCHTHON (parlak, "ANA YAZAR", tüy kalem) |
| 10 | c5_refuse | 0:47.5 | 2.9 | kabul_etmedi | V. KARL madalyası yan dönüp arkasını çevirir; belge; **KABUL EDİLMEDİ** damgası |
| 11 | c5_league | 0:50.4 | 3.2 | smalkalden | Sekiz petrol kalkan halka olur, zincirle kapanır; "ŞMALKALDEN BİRLİĞİ" |
| 12 | c5_wait | 0:53.6 | 7.1 | yatisinca_1546 | Zaman çizelgesi 1521 WORMS · 1529 SPEYER · 1530 AUGSBURG; FRANSA/OSMANLI simgeleri "YATIŞTI" ile sönükleşir; 1546 SAVAŞ |
| 13 | c5_plan | 1:00.7 | 5.9 | muhlberg_plan | Parşömen savaş planı: 24 NİSAN 1547, ELBE, MÜHLBERG, iki yakada birlikler, sis, kızıl geçiş oku; "şematik çizim" |
| 14 | bw_theatre / field | 1:06.6 | 3.0 | sis_elbe | Lab `field`: sisli sabah, nehirde (sığ geçit) atlı/süngülü Habsburg ordusu, kızıl Burgonya haçı bayrağı |
| 15 | bw_medal | 1:09.6 | 2.5 | secmen_esir | Johann Friedrich madalyası, levha "SAKSONYA SEÇMENİ", **ESİR** damgası (dip geçişi) |
| 16 | c5_titian | 1:12.1 | 9.5 | tiziano_cerceve | Tiziano madalyası + "BİR YIL SONRA"; altın çerçevede fırça darbeleriyle boyanan zırhlı atlı siluet, defne; "tek başına" anında kararma |
| 17 | c5_moritz | 1:21.6 | 8.0 | moritz | ZAFER: defne solar → 1552; SAKSONYALI MORİTZ ↔ V. KARL madalyaları, aralarında zincir kopar (ESKİ MÜTTEFİK) |
| 18 | bw_theatre / road_night | 1:29.6 | 4.5 | innsbruck_gece | Lab `road_night`: yağmurlu dağ gecesi, meşaleli atlı kafile (**sedye yok**); "İNNSBRUCK · GECE" |
| 19 | c5_peace | 1:34.0 | 7.7 | augsburg_barisi | AUGSBURG BARIŞI · EYLÜL 1555; iki niş KATOLİK / LUTHERCİLİK (ikincisi kesikli → açılır); mühür |
| 20 | bw_medal | 1:41.7 | 3.7 | ferdinand | Ferdinand madalyası, levha "FERDİNAND · Kardeşi · yürüten" |
| 21 | bw_theatre / hall | 1:45.4 | 3.2 | salon_son | Lab `hall` — **c0 ile aynı sahne ve aynı çift figür** (kolunu genç prensin omzuna dayamış yaşlı adam, **BASTONSUZ**; `scenes_d.draw_pair`, c0 s2 ile aynı yerleşim x≈1130 ve aynı kamera hareketi); son 1 sn siyaha çözülür |

## 2. Bilinen kusurlar / dürüst notlar
- **METIN_DEGISIKLIKLERI uygulandı:** c5s3 "Luther istememişti" (madalya + yasak + levha); c5s10 etiket yalnız **"BİR YIL SONRA"** (yıl yazılmadı, simgesel portre); c5s12 **sedye/litter yok**, hasta imparator belirsiz (yalnız meşaleli atlı kafile).
- **Lab bayrakları genel:** `field` sahnesinin bayrakları jenerik (köylülerde krem haçlı; Mühlberg'de Protestan tarafta petrol haçlı, Habsburg tarafta kızıl Burgonya haçı). Tarihsel sancak değildir.
- **Mühlberg planı şematik:** nehir, birlik blokları ve ok yerleşimi coğrafi/askeri doğruluk iddia etmez; ekranda "şematik çizim" notu var. Sayı/birlik büyüklüğü yazılmadı (kaynaklar çelişkili: A2 #17–#18).
- **Tiziano çerçevesi:** gerçek tablo değil; fırça darbesiyle boyanan, esinlenmiş atlı siluet. "Simge" vurgusu anlatıdaki gibi; yıl (1548) ekranda yok.
- **Köylü Savaşı** çekimlerinde bayraklı kalabalık jenerik; "TAHMİN" etiketi 70–100 bin aralığının kesin olmadığını vurgular.
- **Kısa çekimler:** #10 (2.9 sn), #11 (3.2 sn), #15 (2.5 sn) anlatının kendi parçalanmasından; geçişler kısaltıldı.
- **c5_ideas**: uçuşan şeffaf yapraklar (≈ 160 ms/kare); bir sonraki çekime whip geçişi sırasında iki çekim birlikte çizildiği için o pencerede ≈ 2× görünür (normal).
- İlk-kare pişirme (tek seferlik): harita ≈ 2.6 sn, lab sahneleri 3–7 sn.
- Büyük harf Türkçe kuralına göre: **SAKSONYALI MORİTZ, İNNSBRUCK, FERDİNAND, TİZİANO**.

## 3. Ekrandaki olgular ve kaynak sınıfı (sınıf = `kaynaklar.md` cümle tablosu)
| Ekran metni / öğe | Çekim | Anlatıda | Sınıf / dayanak |
|---|---|---|---|
| WORMS · ALMANYA · taç İspanya'ya · 9 YIL · geri dönüş yasağı | 1 | evet (c5s1) | HAFIZA H16 (web: "dokuz yıl" doğrulandı, 1521–1530) **[Risk ORTA]**; İspanya varış noktası c5s2 bağlamı |
| İSPANYA · FRANSA · OSMANLI okları | 2 | evet | NİTELİKLİ (A2 #15; popüler/eğitim kaynakları) |
| LUTHER'İN FİKİRLERİ | 3 | evet | NİTELİKLİ (A2 #11) |
| 1524 · KÖYLÜ SAVAŞI · 70.000 – 100.000 KİŞİ ÖLDÜ · TAHMİN | 4–5 | evet | NİTELİKLİ (A2 #11: aralık) **[Risk DÜŞÜK]** |
| LUTHER İSTEMEMİŞTİ | 5 | evet (düzeltilmiş c5s3) | A2 #11 (Luther isyana karşıydı) |
| 1529 · SPEYER · KATOLİK ÇOĞUNLUK · AZINLIK · WORMS FERMANI · YENİDEN YÜRÜRLÜKTE | 6 | evet ("azınlık" ima) | CONFIRMED (A2 #9, #13) |
| BİRKAÇ PRENS · 14 ŞEHİR · İTİRAZ · PROTESTO · PROTESTAN | 7 | evet | NİTELİKLİ (A2 #13: 5–6 prens + 14 şehir; ad kökeni) |
| 1530 · AUGSBURG · PROTESTANLAR · **AUGSBURG İTİRAFI** | 8 | yıl/şehir evet; **belge adı anlatıda yok** | CONFIRMED (A2 #14, 25 Haziran 1530); ad `kaynaklar.md` c5s6'da geçiyor |
| LUTHER · MELANCHTHON · ANA YAZAR | 9 | evet | CONFIRMED (A2 #14) |
| V. KARL · KABUL EDİLMEDİ | 10 | evet | HAFIZA H17 (Confutatio 3 Ağu 1530; web doğruladı) **[Risk ORTA]** |
| ŞMALKALDEN BİRLİĞİ | 11 | evet | HAFIZA H17 (Birlik Şubat 1531; web doğruladı) |
| 1521 WORMS · 1529 SPEYER · 1530 AUGSBURG · YATIŞTI · FRANSA · OSMANLI · 1546 SAVAŞ | 12 | evet | 1546 = HAFIZA H18 **[Risk ORTA]** (araştırmada yok; web Crépy/Osmanlı mütarekesi 1544–45 bağlamı); diğer yıllar diğer cümlelerden |
| 24 NİSAN 1547 · MÜHLBERG · ELBE | 13–14 | evet | CONFIRMED (A2 #16; bir müze 25 Nisan diyor); "sisli sabah" anlatıda |
| SAKSONYA SEÇMENİ · **Johann Friedrich** · ESİR | 15 | "Saksonya Seçmeni esir düştü" evet; **ad anlatıda yok** | CONFIRMED (A2 #16 'John Frederick yakalandı'); ad Almanca yazım |
| TİZİANO · BİR YIL SONRA | 16 | evet | HAFIZA H19 **[Risk ORTA]** (1548/Prado ekranda yok) |
| ZAFER · 1552 · SAKSONYALI MORİTZ · ESKİ MÜTTEFİK | 17 | evet | HAFIZA H20 (Mart–Ağustos 1552; web doğruladı) **[Risk ORTA]** |
| İNNSBRUCK · GECE | 18 | evet | HAFIZA H21 (gece kaçış doğrulandı; **sedye kaldırıldı**, görselde de yok) |
| AUGSBURG BARIŞI · EYLÜL 1555 · KATOLİK · LUTHERCİLİK | 19 | evet | HAFIZA H22 (25 Eylül 1555; ekranda gün yok) |
| FERDİNAND · Kardeşi · yürüten | 20 | evet | HAFIZA H23 (Diet Şubat 1555, Ferdinand başkanlığında) |
| salon (c0 ile aynı) | 21 | "Tam bir ay sonra, o büyük salonda" | HAFIZA H24 (H22'ye bağlı) |

## 4. Montaj/ses için vurgu anları (global sn)
Köylü Savaşı etiketi 449.0 · LUTHER İSTEMEMİŞTİ levhası 450.3 · 70.000–100.000 sayacı 452.0 · YENİDEN YÜRÜRLÜKTE damgası 459.8 · PROTESTAN (O→AN) 466.9 · KABUL EDİLMEDİ damgası 481.9 · Şmalkalden zinciri kapanır 484.9 · Elbe geçiş oku 498.3 · ESİR damgası 503.7 · zafer yaprakları solar 516.5 · müttefik zinciri kopar 520.6 · Augsburg Barışı mührü 530.7.

## 5. Ana ajana istekler / bulgular
1. **compose.py Türkçe büyük harf hatası** (bkz. notlar_c4.md #1): bölüm kartı / HUD başlığı.
2. **`SH.draw_medal` önbelleksiz** — c5'te 7 madalya kullanımı var (authors, refuse, moritz, titian, bw_medal ×2): `bw_lib.draw_medal2` / `bw_medal` önbellekli sürümü 2–3× hızlı. **Hız ipucu:** `bw_lib.py` ayrıca `static_backdrop`, `dust2`, `draw_icon2`, `gold2`, `glow_blit` içerir (kare başı maliyeti ≈ yarıya indirir; ayrıntı notlar_c4.md #6).
3. **Hall (c0 geri çağrı) — kaynak kapısı uyarısı:** görev notundaki `p=dict()` ile salonun VARSAYILAN çiftini (`scenes_lib.Hall`, `emperor=True` → `pair_old_prince`) çizdirdiğinizde **bastonlu ve kılıçlı** figür çıkıyor (METIN_DEGISIKLIKLERI c0s4: baston YOK). Bu yüzden son çekimde c0'ın yaptığı gibi `p=dict(emperor=False, extra=…)` ile yazar D'nin bastonsuz `d_pair` figürünü (`scenes_d.draw_pair`, yalnız import; c0 dosyasına dokunmadım) kullandım. **Başka bölümlerde `hall` varsayılan `p` ile çağrılıyorsa aynı baston sorunu olabilir** — `scenes_lib.Hall` varsayılanı (ortak dosya) `d_pair`'e çevrilebilir.
4. **`bw_theatre`** sarmalayıcı: lab hatası stderr'e "[bw_theatre] … hata verdi" yazar; şu an 0 hata (field, road_night, hall çalışıyor).
5. Sahne önbelleği 5 sahne: c5'te `field` farklı `p` ile 3 kez (köylü ×2 aynı `p` → önbellekten; Mühlberg ayrı) — sorunsuz.
