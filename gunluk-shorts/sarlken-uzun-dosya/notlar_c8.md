# notlar_c8 — Bölüm VIII · Akdeniz'de Barbaros (c8)  ·  yazar: bölüm yazarı C

Dosyalar: `scenes_c8.py`, `stage_c8.py` (c8_konsey, c8_zafer [yedek kutlama kartı, kullanılmıyor]), `stage_c678.py` (ortak).
Yeni (yamalı) anlatıya göre: c8s5 "Habsburg çevresinde kutlandı", c8s8 "Sonraki yıllarda" ('30 YIL' sayacı YOK), c8s9 "beş yüz kadar" (≈500), c8s11 "çağrılmadığı anlatılır" (damga ANLATILIR).
Son durum: 15 çekim + bölüm kartı, 71.9 sn; sahne-lab `sea` ve `siege` (Halkulvadi) bağlı; "[sahne: … henüz yok]" yok. `--check`: uyarı yok, bölüm ortalaması ≈ 150 ms/kare (en yavaş çekim ≈ 225 ms).

## (a) Çekim listesi özeti (15 çekim + bölüm kartı)
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | c678_sahne (sea) | akdeniz_kadirgalar | 3.5 | şafakta 8 yeşil bayraklı Osmanlı kadırgası; AKDENİZ |
| 2 | medal | barbaros | 3.8 | BARBAROS HAYREDDİN PAŞA (forest madalya); "1534" |
| 3 | map | istanbul_tunus | 4.1 | İstanbul → Tunus rotası (gemi simgesi ilerler), KAPTAN-I DERYA (Barbaros), 1534 |
| 4 | c678_medals | karl_doria | 5.9 | V. Karl + Andrea Doria; "filosuyla" deyince iki madalya arasında kesikli rota üstünde altın gemi ilerler; BİZZAT; TUNUS SEFERİ · 1535 |
| 5 | c678_sahne (siege) | halkulvadi | 5.6 | Halkulvadi kalesi (`city="halkulvadi"`, gündüz, top ateşi, kıyıda kadırgalar); "düştü" deyince yeşil hilal sancaklar yerini Habsburg haçlı sancaklara bırakır (`ov_flagswap`); TEMMUZ 1535, HALKULVADİ, TUNUS ALINDI |
| 6 | c678_cift | 20bin_esir | 2.9 | 20.000 ESİR · SERBEST KALDI (zincir simgesi), altta kalabalık siluet bandı (serbest kalan esirler) + YAKLAŞIK damgası |
| 7 | c678_sahne (sea harbor) | zafer_kutlama | 4.1 | liman alacakaranlığı: sallanan çanlar, çubuktan açılan Habsburg sancakları, defne, ZAFER; HABSBURG ÇEVRESİNDE |
| 8 | c678_sahne (sea night) | gece_deniz_filo | 5.0 | gece denizi, ufukta Osmanlı filosu; Barbaros madalyası |
| 9 | map | preveze_harita | 3.7 | Preveze işareti, "28 EYLÜL 1538" |
| 10 | c678_sahne (sea) | preveze_savas | 6.8 | Preveze deniz savaşı (dusk, toplar, barut dumanı, köz); PREVEZE · 28 EYLÜL 1538; PAPALIK/VENEDİK/İMPARATOR (birleşik filo) vs BARBAROS; GERİ ÇEKİLDİ |
| 11 | map | dogu_akdeniz_ustunluk | 5.7 | doğu Akdeniz'de yeşil dalga, Osmanlı donanması; AKDENİZ'İN DOĞUSU (30 YIL YOK) |
| 12 | map | cezayir_harita | 3.8 | Cezayir, 1541, kuzeyden kıyıya okla çıkış |
| 13 | c678_cift | 500_24bin | 4.2 | ≈ 500 YELKENLİ · ≈ 24.000 ASKER (ikinci sayaç gelince ilki sola kayar); altta ufuk çizgisinde büyüyen gemi filosu + asker bandı |
| 14 | c678_sahne (sea storm) | cezayir_firtina | 6.8 | fırtına, şimşek (anlatıya bağlı flashes), gemiler batar; BARUT ISLANDI; ≈ 150 GEMİ BATTI (YAKLAŞIK) |
| 15 | c8_konsey | cortes_konsey | 6.0 | savaş konseyi masası, BOŞ sandalye, kapıda Cortés madalyası; KONSEYE ÇAĞRILMADI + ANLATILIR damgası |

## (b) Bilinen kusurlar
- #14 fırtına: `flashes=[1.45, 3.4, 4.7, 5.8]` ve `sink_t=(...)` yerel saniye cinsinden sabit yazıldı (çekim c8s10 −0.2 sn'de başlar); anlatı süreleri değişirse yeniden hesap gerekir.
- #13 etiketleri: "≈" Cinzel'de var (denetlendi); oklar (→) Cinzel'de yok (kullanılmadı).
- c8_zafer (alternatif kutlama kartı) kullanılmıyor; yedek olarak kodda duruyor.
- Preveze çekiminde tarafların renkleri/yarım ay–haç otomatik (sea sahnesi): Venedik bayrağı turkuaz, Papalık altın. Bölge çokgenleri mapdata'ya ait; Preveze/doğu Akdeniz haritalarındaki kaba dikdörtgen kara parçaları (Epir/Rodos kutusu) mapdata'nın şematik poligonları.
- Halkulvadi sahnesindeki kale lab'ın şematik çizimi (gerçek La Goulette değil); sancak değişimi yalnız kale sancaklarında (gemilerdeki sancaklar sabit).
- `--check` ms/kare duvar saatiyle ölçüldüğünden yoğun makinede geçiş penceresine düşen kısa çekimler sahte uyarı verebilir. CPU süresiyle en yüksek 205 ms (c8 ortalama ≈ 140 ms).

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- Barbaros Hayreddin Paşa, sultanın amirali; 1534 kaptan-ı derya, Tunus — CONFIRMED (A3 #12; gün tutarsız, yalnız yıl).
- 1535: Şarlken Doria'nın filosuyla bizzat Tunus'ta — CONFIRMED (A3 #13; H28 DOĞRULANDI). Temmuz 1535 Halkulvadi düştü; ≈20 bin esir — CONFIRMED (A3 #13) → YAKLAŞIK damgası.
- Kutlama: Habsburg çevresinde — NİTELİKLİ/HAFIZA H29 (KISMEN: Sicilya girişleri, Vermeyen halıları): ekranda "HABSBURG ÇEVRESİNDE".
- Preveze 28 Eylül 1538; Papalık+Venedik+İmparator birleşik filosu geri çekildi — CONFIRMED (A3 #14; sonuç yorumları ayrışır, "geri çekildi" nötr).
- Sonraki yıllarda doğu Akdeniz'de Osmanlı üstünlüğü — H30 (sayı kaldırıldı): ekranda sayı yok.
- Cezayir 1541; ≈500 yelkenli; ≈24.000 asker — NİTELİKLİ (A3 #15) → ≈ işaretiyle. Fırtına, barut ıslandı, ≈150 gemi battı — NİTELİKLİ (A3 #15) → YAKLAŞIK damgası.
- Cortés orada, savaş konseyine çağrılmadığı anlatılır — CONFIRMED/NİTELİKLİ (A3 #16, Gómara hattı): damga ANLATILIR. (A3 #17 zümrüt anekdotu KONMADI.)
- Filo/kalabalık/asker bantları yalnız süs siluetleridir: sayıları temsil etmez, ekranda sayı olarak yazılmaz.

## (d) Ana ajandan istekler / uyarılar
1. Sea ve siege sahneleri sorunsuz çalışıyor; `flashes=[...]` ve `sink_t=(...)` yerel saniyelerle yazıldı (anlatı değişirse yeniden hesap gerekir).
2. Aynı `sea` sahnesini farklı gemi listeleriyle kullanan çekimlerde `theatre` önbellek anahtarı listeleri dışladığı için benzersiz skaler `tag=` kullandım (diğer yazarlar için de geçerli).
3. `shots.py` genel şablonlarındaki demet çapa çökmesi için bkz. notlar_c6.md (d)-1.
