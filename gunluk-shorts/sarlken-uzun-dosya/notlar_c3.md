# notlar_c3 — Bölüm III · Şehirlerin İsyanı (c3)  ·  yazar: bölüm yazarı A

Dosyalar: `scenes_c3.py` (çekim listesi), `shots_c3.py` (özel çekim türü `c3_bayram`), `stage_c3.py` (kendi dioramam `c3_sokak`: meşaleli Kastilya sokağı), `kit_a.py` (ortak yardımcılar; `a_map`, `a_medals`, `a_theatre`).
Sürüm: yamalı anlatıya göre (c3s2 "tepkiyle karşılandı"). Son durum: bölüm kartı hariç 11 kendi çekimim, 49,9 sn (ortalama 4,5 sn/çekim); lab sahneleri `field` ve `siege` (sahne-lab, Toledo şehri) bağlı; "[sahne: … henüz yok]" yok. Ton: kan kırmızısı + gri yağmur (haritalarda kırmızı ton, yağmur kaplaması).

## (a) Çekim listesi özeti
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | a_map | ispanyadan_ayrilis | 3.7 | Avrupa/İspanya kırmızı tonlu harita, yağmur; deniz rotası + kesikli kara rotası → AACHEN + taç; rota üstünde gemi |
| 2 | a_map | sehirlerde_tepki | 7.0 | Kastilya haritası; "YABANCI DANIŞMANLAR" ve "VERGİ" kartları; 14 kızıl şehir ışığı; yumruk simgesi + şok halkaları |
| 3 | a_theatre (c3_sokak) | komunero_isyani | 3.7 | gece Kastilya sokağı, meşaleli kalabalık, kızıl sancaklar; "1520" + "KOMÜNERO İSYANI" (whip geçişi) |
| 4 | a_map | villalar_harita | 3.3 | Villalar'a yaklaşma, "23 NİSAN 1521", yağmur |
| 5 | a_theatre (field) | villalar_savas | 2.9 | sahne-lab savaş alanı, yağmur; ön planda kraliyet süvarisi hücumu, karşıda Komünero kitlesi; kamera süvariyi izler (whip geçişi) |
| 6 | a_medals | uc_onder | 5.9 | Padilla, Bravo, Maldonado oniks madalyaları, "ERTESİ GÜN" levhası, İDAM damgası (dip geçişi) |
| 7 | a_theatre (siege) | toledo_pacheco | 5.5 | sahne-lab kuşatma (Toledo, alacakaranlık, yağmur, yangın); TOLEDO levhası, María Pacheco gümüş madalyası, AYLARCA kum saati |
| 8 | a_map | valensiya_germania | 6.2 | Valensiya bölgesi; ESNAF LONCALARI levhası; altın "GERMANÍA" |
| 9 | a_map | kastilya_leon | 2.7 | Kastilya-León bölgesi, "BUGÜN" |
| 10 | c3_bayram | bayram | 4.1 | kale sancağı, flamalar, kıvılcımlar; "23 NİSAN" + "BAYRAM" |
| 11 | a_map | ilk_ders | 4.7 | dört taht (Kastilya, Aragon, Burgonya, Avusturya) taçları; Şarlken yalnız Kastilya'da; diğerlerine kırmızı X'li kesikli çizgiler; "İLK DERS" damgası |

Geçişler: savaş/isyan vurgularında `whip` (kısa), ölüm çekiminde `dip`, geri kalanı `fade`. Kamera: her haritada yaklaşma/itme; diorama çekimlerinde yavaş itme veya takip.

## (b) Bilinen kusurlar
- Haritalar kırmızı tonlu ve sınırlar yaklaşık: `c1_kastilya`, `c3_valensiya`, `c3_castilla_leon` bölgeleri `kit_a`'da ülke poligonlarından türetilmiş çokgenler (Kastilya-León = bugünkü özerk bölgeye yakın kaba şekil; 1521 Kastilya Krallığı değil). "SINIRLAR YAKLAŞIKTIR" yazısı bölge çekimlerinde `map` şablonundan çıkıyor.
- Villalar savaşı sahne-lab `field`'ın stilize figürleriyle: Komünero tarafı "köylü" figürleri (gerçekte şehir milisleri ağırlıklı), sancağı sahnenin varsayılan armalı (haç) sancağı — tarihsel Komünero sancağı değil; renk mor (`#5A3A8A`, yeşil seçilirse sahne otomatik yarım ay çiziyor, o yüzden kaçındım). Kraliyet süvarisi kırmızı (`#8E1F26`).
- Toledo sahne-lab `siege` sahnesinin stilize tepe şehri (Alcázar, katedral kulesi, sur); gerçek topografya/plan değil. Yangın/top ateşi görsel efekt; kuşatma ayrıntısı iddiası yok. Şehir katmanı lab'da 1× piksel yoğunluğunda pişiyor: yakın planda yamaçtaki evlerin ve surların kenarları basamaklı görünüyor; bu yüzden kamerayı zoom 1,4'te tuttum (Alcázar + sancak tam kadrajda).
- Sokak dioraması (`c3_sokak`) figürleri figür-lab siluetleri; sancaklardaki kale simgesi genel (belirli bir şehir armamı değil).
- c3_bayram sancağı kale simgeli genel bayrak (Castilla y León bayrağının birebir taklidi değil: kale + aslan çeyrekleri yok).
- Şehir kırmızıları (14 ışık) Kastilya'daki şehirlerin kabaca konumları, isimsiz (hangi şehirlerin ayaklandığı iddiası yok).
- Çekim #5 (2,9 sn) ve #9 (2,7 sn) kısa; anlatı cümlesinin parçalarına denk geliyor.
- `--check` ms/kare ölçümü duvar saatiyle yapılıyor; makine yüküne duyarlı. Düşük yükte (load avg ≈ 2,5) ölçülen: ortalama ≈ 113 ms/kare, en yavaş çekim 222 ms (#3 c3_sokak: ≈50 figür + meşale alevleri); yoğun yükte ortalama 145–170 ms, tek tek 360 ms'ye kadar. Hiçbir çekim 450 ms'yi aşmıyor. Geçişte gelen çekimin ilk karesindeki lab önbellek pişirmesi (~1 sn) bir önceki çekimin örnek karesine denk gelirse ölçümü şişirebilir (whip süresini 0,4 sn tuttum). Tahmini tek çekirdek render ≈ 2–3 dk.

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- AACHEN işareti + rota (taç için İspanya'dan ayrılış) — CONFIRMED (Aachen tacı: c2s12; A1 #16); ayrılışın zamanlaması/yolu HAFIZA H11 (Mayıs 1520; web: sıra doğrulandı). Ekranda tarih/liman adı yok, yalnız şematik rota.
- YABANCI DANIŞMANLAR, VERGİ — HAFIZA H11 (kısmen A1 #10: yabancıların uzaklaştırılması, 600.000 dukat servicio). Anlatı "ihanet saydı" yerine "tepkiyle karşılandı" (yamalı); ekranda yalnız kartlar + öfke.
- "1520" + KOMÜNERO İSYANI — CONFIRMED (c3s3; A1 #17).
- "23 NİSAN 1521", VILLALAR, kraliyet ordusu isyancıları dağıttı — CONFIRMED (c3s4; A1 #17).
- "ERTESİ GÜN", İDAM, PADILLA / BRAVO / MALDONADO ("Komünero önderi") — CONFIRMED (c3s5; A1 #17). Kesin gün sayısı ("24 Nisan") ekrana yazılmadı; yalnız anlatıdaki "ertesi gün".
- TOLEDO, MARÍA PACHECO ("Padilla'nın dul eşi"), AYLARCA — CONFIRMED +H12 (c3s6; A1 #17 "birkaç ay daha direndi"). "Padilla'nın dul eşi" ilişkisi araştırmada yok (H12).
- VALENSİYA, ESNAF LONCALARI, GERMANÍA — NİTELİKLİ (c3s7; A1 #18: yıllar kaynağa göre 1519–1523 → anlatıda "aynı yıllarda"; ekranda yıl yok).
- BUGÜN, KASTİLYA-LEÓN, "23 NİSAN", BAYRAM — CONFIRMED (c3s8; A1 #17 notu: 23 Nisan = Castilla y León Günü).
- İLK DERS (dört taht, Şarlken yalnız Kastilya'da, kırmızı X) — YORUM (c3s9, anlatıcı sonucu); taht adları (Kastilya, Aragon, Burgonya, Avusturya) c1s3'ten (A1 #2).
- Ekrandaki hiçbir sayı/ad/tarih anlatı ya da `kaynaklar.md`/`arastirma/*.md` dışından gelmiyor. Altyazı yok. HUD alanları boş.

## (d) Ana ajandan istekler / uyarılar
1. `shots.py` `medals`: `at + 0.4` çapa demetiyle `TypeError`; `kit_a.a_medals` çapa destekli yedeği (tarih levhası `date=`, damga `stampt=`, `bgname=` ekli); başkaları da kullanabilir.
2. `shots.py:449` (`doc`): kâğıt tohumu `hash(title)` süreçler arası kararsız; c3'te belge çekimi yok ama diğer bölümlerde varsa `PYTHONHASHSEED=0` ya da `zlib.crc32` önerilir (bkz. notlar_c1 (d)1). `doc`'ta `align="c"` kırpma hatası da orada (satırın sağı açılmıyor); düzeltilmiş kopya `kit_a.a_doc`.
3. `name_plate` metni `w`'ye sığdırmıyor; `a_medals` için `pw` (levha genişliği) parametresi verdim.
4. `a_map` (kit_a): kabartma + `tint` döşemeye pişiyor, kamera yolu ön pişiriliyor; `MapView` örneğine yalnız çağrı süresince geçici öznitelik takar.
5. Lab bağımlılıkları: `scenes_field` (`SF.cam_on`), `scenes_siege` (`SG.cam_on_city`, `city="toledo"`). Lab API'si değişirse çekim #5 ve #7 yer tutucuya düşebilir ("[sahne hata: …]"); render öncesi son `--check` önerilir.
6. Süpersamplı yeni `stage.py` sonrası `c3_sokak` (kendi dioramam) ve lab sahnelerini yeniden taradım; görsel bozulma/kayma yok.
