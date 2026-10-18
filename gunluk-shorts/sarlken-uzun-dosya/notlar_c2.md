# notlar_c2 — Bölüm II · Taç Satılık (c2)  ·  yazar: bölüm yazarı A

Dosyalar: `scenes_c2.py` (çekim listesi), `shots_c2.py` (özel çekim türleri `c2_yedi_koltuk`, `c2_gosteri`, `c2_terazi`, `c2_pay`, `c2_para`, `c2_borc_terazi`, `c2_plus_ultra`), `kit_a.py` (ortak yardımcılar; `a_map`, `a_medals`, `a_g_doc` = yeşil tonlu düzeltilmiş belge, `a_g_medal`, terazi/para/zincir çizimleri).
Sürüm: yamalı anlatıya göre (c2s7 "yaklaşık 543.000", c2s9 "Bazı tarihçilere göre … Almanya için en iyi"). Son durum: bölüm kartı hariç 18 kendi çekimim, 88,5 sn (ortalama 4,9 sn/çekim); lab sahneleri `counting_house`, `electors_hall`, `aachen` (oda-lab) bağlı; "[sahne: … henüz yok]" yok. Ton: koyu yeşil + para altını.

## (a) Çekim listesi özeti
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | a_g_medal | maksimilyan_oldu | 4.4 | Maksimilyan oniks madalya; büyük "OCAK 1519" yukarı çıkıp küçülür |
| 2 | c2_yedi_koltuk | yedi_secmen | 5.2 | taç; KALITSAL (soy ağacı simgesi, üstü çizilir); yedi kızıl seçmen şapkası + "YEDİ SEÇMEN" |
| 3 | a_medals | karl_fransuva | 3.6 | Şarlken ↔ I. FRANÇOIS madalyaları, kılıç simgesi |
| 4 | c2_gosteri | henry_gosteri | 6.4 | perdeli spot ışığında VIII. HENRY madalyası, silik hayalet madalyalar, "GÖSTERİ" |
| 5 | c2_terazi | terazi_pazarlik | 3.1 | terazi: oy ↔ altın paralar (pazarlık) |
| 6 | a_theatre (counting_house) | sayim_odasi_850bin | 4.7 | oda-lab sayım odası + "yaklaşık 850.000 FLORİN" sayacı |
| 7 | c2_pay | fugger_payi | 4.4 | çubuk 543/850, ÜÇTE İKİ işareti, "YAKLAŞIK 543.000 FLORİN", altın parıltı |
| 8 | a_g_medal | fugger | 3.9 | Jakob Fugger bronz madalya + AUGSBURG levhası |
| 9 | a_map | frankfurt_harita | 3.6 | Frankfurt'a yaklaşma, "28 HAZİRAN 1519", Almanya tonu |
| 10 | a_theatre (electors_hall) | yedi_oy | 3.2 | oda-lab seçmen salonu, yedi koltuk dolu, "7 / 7" |
| 11 | c2_para | parayi_aldi | 3.4 | yedi şapka + kese + düşen paralar; BAZI TARİHÇİLERE GÖRE damgası |
| 12 | a_map | almanya_icin_en_iyi | 4.9 | Almanya altın; yedi şapkadan Almanya'ya oklar; "ALMANYA" |
| 13 | c2_borc_terazi | rusvet_borc | 8.2 | terazi: RÜŞVET ? (TARTIŞMALI) ↔ BORÇ (defter, GERÇEK); sonra zincirli taç |
| 14 | a_g_doc | yazili_soz | 10.5 | parşömen "YAZILI SÖZ · 1519": iki satır + mum mühür |
| 15 | a_map | aachen_harita | 3.8 | Aachen'e yaklaşma, "23 EKİM 1520", ŞARLMAN madalyası |
| 16 | a_theatre (aachen) | aachen_taç | 2.9 | oda-lab Aachen: diz çöken figür, taç iner (zoom geçişi) |
| 17 | c2_plus_ultra | plus_ultra | 2.9 | iki sütun + kurdele "PLUS ULTRA" / "DAHA ÖTEYE" |
| 18 | a_map | herkul_sutunlari | 9.6 | Cebelitarık; RİVAYET damgası; sütun çağrıları; "NON PLUS ULTRA" bandında NON üstü çizilip silinir; batıya rota + gemi |

Çekim #14 (belge) 10,5 sn: anlatı cümlesi 9,3 sn; belge iki satırı sırayla açılır, mühür "kuracaktı" sözcüğünde basılır. Geçişler çoğunlukla `fade`; Aachen taç çekimi `zoom`.

## (b) Bilinen kusurlar
- Sayaçlar ve çubuk (850.000, 543.000) animasyon sırasında ara değerlerden geçiyor (örn. "624.759"); son değer ilgili sözcükte tam oturuyor. Ara değerler veri iddiası değil, sayma animasyonu.
- 850.000 ve 543.000 kaynaklarda aralık/farklı (825–852 bin; 500–550 bin; 543–544 bin) — ekranda "YAKLAŞIK"; ÜÇTE İKİ işareti 543/850 ≈ 0,64'ü gösteren yaklaşık oran.
- Seçmen siluetleri (electors_hall) ve şapka simgeleri kimliksiz; yedi seçmenin ad/ünvan iddiası yok (anlatıda da yok).
- Almanya bölgesi modern ülke çokgenine benzer; 1519 İmparatorluğu'nun sınırı değil (anlatı "Almanya" diyor). Haritalar yaklaşık ("SINIRLAR YAKLAŞIKTIR" yazısı bölge çekimlerinde çıkıyor).
- Herkül Sütunları çağrıları: Calpe/Abyla yaklaşık konumda; sütunlar simge (ölçeksiz).
- "YAZILI SÖZ" belgesi seçim kapitülasyonunun metni değil, anlatının yakın parafrazı (iki satır; alıntı işareti yok); madde sayısı yazılmadı (A1 #15'te 34 madde 19. yy kaynağı).
- Terazi çekimleri (c2_terazi, c2_borc_terazi) sembolik; ölçek/oran iddiası yok. c2_borc_terazi sonunda terazi bilerek soluklaşıyor (taç odağa gelsin), son saniyede RÜŞVET/BORÇ etiketleri zor okunur — anlatı o anda taca geçiyor.
- Henry, François, Fugger, Maksimilyan, Şarlman yüzleri madalya-lab'ın stilize portreleri.
- `--check` ms/kare ölçümü duvar saatiyle; yük altında tek tek çekimler dalgalanıyor. Ölçülen: ortalama ≈ 145–225 ms/kare, en yavaş çekim ≈ 370 ms (c2_gosteri: perde + spot + hayalet madalyalar); hiçbiri 450 ms'yi aşmıyor. Tahmini tek çekirdek render ≈ 5–8 dk.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- "OCAK 1519", Maksimilyan'ın ölümü — HAFIZA H7 (web özeti doğruladı: 12 Ocak 1519, Wels); ekranda yalnız "OCAK 1519".
- KALITSAL (üstü çizili) / YEDİ SEÇMEN — CONFIRMED (c2s2; A1 #11).
- I. FRANÇOIS (Fransa Kralı) — CONFIRMED (c2s3; A1 #11). Şarlken alt başlığı "Kastilya ve Aragon Kralı" — CONFIRMED (c1s13; A1 #7–#8).
- VIII. HENRY, GÖSTERİ — CONFIRMED (c2s4; A1 #11: "geç, sembolik").
- Terazi (oy ↔ para) — NİTELİKLİ (c2s5; A1 #14, #12–#13; "açıkça" ifadesi A1'de yok, makul).
- "yaklaşık 850.000 FLORİN" — NİTELİKLİ (c2s6; A1 #12: 825–852 bin; A4 #12: 851.585 / 850.000).
- "YAKLAŞIK 543.000 FLORİN", ÜÇTE İKİ, JAKOB FUGGER, AUGSBURG — NİTELİKLİ +H8 (c2s7; A1 #13, A4 #12). "Augsburglu" ayrıntısı araştırmada yok (H8; web özeti doğruladı).
- "28 HAZİRAN 1519", Frankfurt, "7 / 7" — CONFIRMED (c2s8; A1 #11).
- BAZI TARİHÇİLERE GÖRE damgası, ALMANYA — NİTELİKLİ +H9 (c2s9; A1 #14, Cohn 2001: "parayı alıp Almanya için en iyisini yaptı"). Metin yamasıyla "iki taraftan da" iddiası kaldırıldı; ekranda yalnız şapkalar → ALMANYA.
- RÜŞVET ? / TARTIŞMALI, BORÇ / GERÇEK — NİTELİKLİ (c2s10; A1 #14, #12–#13; A4 #12–#13). Taç + zincir = "imparator, tacını takmadan önce borçluydu" — YORUM (görsel metafor).
- "YAZILI SÖZ · 1519": prenslerin ayrıcalıklarına saygı, birlikte yönetecek konsey — CONFIRMED (c2s11; A1 #15: 3.07.1519; Reichsregiment). "1519" yılı belgelerden (anlatıda yok).
- "23 EKİM 1520", Aachen, ŞARLMAN — CONFIRMED +H10 (c2s12; A1 #16). "Şarlman'ın şehri" ayrıntısı araştırmada yok (H10, düşük). Not: bu taç Alman-Roma Kralı tacı; imparatorluk tacı Bologna 24.02.1530 (A1 #16) — ekranda yazılmadı.
- PLUS ULTRA / DAHA ÖTEYE — CONFIRMED (c2s13; A1 #21).
- RİVAYET damgası, "NON PLUS ULTRA" / "DAHA ÖTESİ YOK", NON'un silinmesi — RİVAYET (c2s14; A1 #21: sütunlardaki yazı efsane; devizin tersine çevrilmesi CONFIRMED). Damga şart olduğu için "Rivayete göre" sözcüğünde basılır.
- Ekrandaki hiçbir sayı/ad/tarih anlatı ya da `kaynaklar.md`/`arastirma/*.md` dışından gelmiyor. Altyazı yok. HUD alanları boş.

## (d) Ana ajandan istekler / uyarılar
1. `shots.py:449` (`doc`): kâğıt tohumu `hash(title) % 97` süreçler arası kararsız (çok süreçli render'da belge kenarı kareler arasında değişir). Belge çekimlerim için düzeltilmiş `a_doc`/`a_g_doc` (kit_a; `zlib.crc32`). Öneri: `shots.py`'de `zlib.crc32` ya da render'da `PYTHONHASHSEED=0`.
2. `shots.py` `doc`, `align="c"`: açılış kırpması sol kenardan başladığı için ortalı satırların sağı hiç açılmıyor ("…gösterile" / "…kuru" gibi yarım kalıyor). `a_doc`'ta düzelttim (`x_left = -genişlik/2`).
3. `shots.py` `medals`: `at + 0.4` çapa demetiyle `TypeError`; `kit_a.a_medals` çapa destekli yedeği (başkaları da kullanabilir).
4. `name_plate` metni `w`'ye sığdırmıyor; uzun adlarda `w`'yi elle verdim.
5. `a_map` (kit_a): `map` şablonu + kabartma dokusu + `tint`'in döşemeye pişirilmesi + kamera yolu ön pişirmesi; ana `mapview()` örneğine yalnız çağrı süresince geçici öznitelik takar. Dileyen bölümler kullanabilir.
6. Kullandığım lab parçaları: simge `elector_hat` (simge-lab; kendi `c2_kurhut` denemem yerine geçti), temel simgeler `imperial_crown`, `coinbag`, `family`, `book`; sahneler `counting_house` (parametre `coins_t` çekim başına göre yerel saniye), `electors_hall`, `aachen`. Lab'ların API'si değişirse (özellikle `p` anahtarları) bu çekimler yer tutucuya düşebilir; `a_theatre` sarmalayıcısı çökmeyi önler ama "[sahne hata: …]" yazısı nihai videoda görünmemeli — render öncesi son `--check` önerilir.
