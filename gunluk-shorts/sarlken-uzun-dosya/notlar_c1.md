# notlar_c1 — Bölüm I · Dört Tahtın Çocuğu (c1)  ·  yazar: bölüm yazarı A

Dosyalar: `scenes_c1.py` (çekim listesi), `shots_c1.py` (özel çekim türleri `c1_yol`, `c1_evli`, `c1_cift`, `c1_delilik`, `c1_dort_dil`, `c1_ortak_kral`, `c1_halk`), `kit_a.py` (A yazarının ortak yardımcıları: çapa sarmalayıcı, `a_map`, `a_medals`, `a_doc`, `a_theatre`, levha/işaret/para/zincir/mum çizimleri, kendi kabartma simgeleri `c1_sarmal`, `c1_gul`, `c1_at`, bölge üreticileri `c1_flandre`, `c1_aragon`, `c1_kastilya`).
Sürüm: yamalı anlatıya göre (c1s4 "iki yaşına basmamış kuzeni", c1s12 "yaklaşık kırk üç yıl" + "belge bilinmiyor"). Son durum: bölüm kartı/ana başlık hariç 23 kendi çekimim, 119 sn (ortalama 5,2 sn/çekim); lab sahneleri `tower` (oda-lab) ve `sea` (sahne-lab) bağlı; "[sahne: … henüz yok]" yok.

## (a) Çekim listesi özeti
| # | tür | etiket | süre | ne gösteriyor |
|---|---|---|---|---|
| 1 | a_map | gent_harita | 6.2 | Avrupa → Flandre bölgesi + GENT işareti, "24 ŞUBAT 1500" tarih levhası; kabartmalı kara |
| 2 | c1_evli | juana_filip | 7.0 | Juana ve Filip madalyaları, aralarında iki halka (evlilik); isim levhaları |
| 3 | tree | soy_agaci | 4.1 | dört büyükanne-büyükbaba (Maria, Maksimilyan, Fernando, İsabel) → Filip ve Juana → Şarlken |
| 4 | a_map | dort_ulke | 5.2 | dört miras sırayla yanar: Burgonya (Hollanda + Franche-Comté), Avusturya, Aragon (+ Napoli/Sicilya/Sardunya), Kastilya |
| 5 | c1_yol | miras_yolu | 8.5 | Şarlken madalyası → İspanya tahtı; "İKİ YAŞINA BASMAMIŞ KUZEN" mumu, "5 AY" noktaları, mum sönünce yol açılır, taç bronzdan altına döner |
| 6 | c1_cift | evlilik_olum | 5.6 | dört taç; EVLİLİK (halkalar) ve ÖLÜM (kuru kafa) |
| 7 | a_map | burgos | 4.1 | Burgos'a yaklaşma (dip geçişi), "6 YAŞINDA", Filip oniks madalyası |
| 8 | a_map | tordesillas_harita | 3.9 | Tordesillas'a yaklaşma, "1509" |
| 9 | a_theatre (tower) | kule_juana | 7.2 | oda-lab kule hücresi (Tordesillas, gece, mum, oturan kadın siluet), yavaş itme; 1509 → 1555 "46 YIL" çubuğu |
| 10 | c1_delilik | delilik_siyaset | 6.3 | spiral (DELİLİK?) ↔ taç (SİYASET?), ortada soru işareti, TARTIŞMALI damgası |
| 11 | a_medals | karl_margareta | 3.4 | küçük Şarlken + Margareta (hala) madalyaları |
| 12 | a_map | mechelen | 3.6 | Mechelen'e yaklaşma, "ANA DİLİ: FRANSIZCA" (zambak) |
| 13 | c1_dort_dil | dort_dil | 9.0 | haç / gül / kılıç / at simgeleri + ESPAÑOL, ITALIANO, FRANÇAIS, DEUTSCH + RİVAYET damgası |
| 14 | quote | soz_alinti | 3.3 | "ŞARLKEN'E ATFEDİLEN SÖZ" alıntı kartı (sözün kendisi; altyazı değil) |
| 15 | a_timeline_s | 43_yil | 7.0 | 1558 ÖLÜM → 1601 İLK YAZILI KAYIT, YAKLAŞIK 43 YIL, BELGE BİLİNMİYOR damgası |
| 16 | medal | fernando_oldu | 4.3 | Fernando oniks madalya, "† 1516" (dip geçişi) |
| 17 | c1_ortak_kral | ortak_kral | 5.7 | Şarlken madalyası + zincirle bağlı parmaklıklı Juana madalyası; KASTİLYA ve ARAGON armaları; taç |
| 18 | a_theatre (sea) | firtina | 6.1 | sahne-lab fırtına: 5 karaka, şimşek, yağmur; "EYLÜL 1517" (whip geçişi) |
| 19 | a_map | tazones_rota | 3.7 | SANTANDER (hedef, kesikli rota) / gerçek rota + gemi → Tazones, "KÜÇÜK BALIKÇI KÖYÜ" |
| 20 | a_theatre (sea) | tazones_koyu | 1.9 | alacakaranlıkta Tazones kıyısı, "TAZONES" |
| 21 | c1_halk | yeni_halk | 4.9 | akşam limanında kalabalık siluet, Şarlken madalyası "17 YAŞINDA · KRAL", üç soru işareti |
| 22 | a_map | valladolid_harita | 2.7 | Valladolid'e yaklaşma, "1518" |
| 23 | a_doc | kortes_talebi | 5.6 | parşömen: VALLADOLID KORTESİ · 1518; "Kastilyacayı öğren." (altı çizili) / "Yabancı danışmanlarını gönder." |

Geçişler: çoğu `fade`; ölüm anlarında `dip` (Burgos, Fernando), fırtınada `whip`. Her çekimde kamera/itme hareketi veya sürekli animasyon var (donuk kare yok). Çekim yoğunluğu ortalama 5,2 sn.

## (b) Bilinen kusurlar
- Harita sınırları yaklaşık: Flandre, Aragon, Kastilya bölgeleri `kit_a` içinde ülke poligonlarından türetilmiş el yapımı çokgenler (1500 öncesi gerçek sınırlar değil). Bölge gösteren haritalarda `map` şablonunun kendi "SINIRLAR YAKLAŞIKTIR" yazısı çıkıyor.
- Yüksek yakınlaştırmada (zoom 7–8) kara yalnızca kabartma dokusu + etiket; ayrıntı yok (tek şehir vurgusu için bilinçli).
- Tordesillas kulesi: Juana yüzsüz siluet (oda-lab); "46 YIL" çubuğunun bitiş yılı 1555 anlatıda söylenmiyor (kaynaktan; bkz. (c)).
- Kalkan armaları (Kastilya: kale, Aragon: dört kırmızı çubuk) ve gemi sancakları (haç) basitleştirilmiş; heraldik doğruluk iddiası yok.
- Fırtına sahnesindeki beş karaka sahne-lab'ın varsayılan kıyafeti (kırmızı haç yelkenli); Tazones köyü lab'ın stilize kıyısı, gerçek plan değil.
- `c1_halk` kalabalığı dar bir şeritte duran siluet figürler (figür-lab); sol yarıda madalya + levha, orta boş. Tempo kısa (4,9 sn) olduğundan kabul edildi.
- `quote` kartı sözü tam metin olarak yazıyor; anlatıdaki c1s12 cümlesini değil, tartışılan sözün kendisini gösteren bir kart (altyazı değil), yine de istenirse çıkarılabilir.
- Valladolid belgesi iki satırlık yakın parafraz (alıntı işareti yok): "Kastilyacayı öğren. / Yabancı danışmanlarını gönder."
- `--check` ms/kare ölçümü duvar saatiyle yapılıyor; makine yüküne duyarlı. Düşük yükte (load avg ≈ 2,5) ölçülen: ortalama ≈ 108 ms/kare, en yavaş çekim 162 ms (c1_halk); yoğun yükte (load avg 6–12) aynı çekimler 170–215 ms ortalama ve tek tek 250–400 ms'ye çıkabiliyor. Hiçbir çekim 450 ms'yi aşmıyor. Tahmini tek çekirdek render ≈ 5 dk (düşük yük).

## (c) Ekrana koyduğum olgular ve kaynak sınıfı
- 24 Şubat 1500, Gent, Flandre — CONFIRMED (c1s1; A1 #1). "FLANDRE" etiketi anlatıdaki sözcük; bölge sınırı yaklaşık.
- Juana (Kastilya Kraliçesi), Filip (Burgonyalı, "Yakışıklı") — CONFIRMED +H3 (c1s2; A1 #1).
- Dört büyükanne-büyükbaba (MARİA/Burgonyalı, MAKSİMİLYAN, FERNANDO, İSABEL) ve dört miras (Burgonya, Avusturya, Aragon, Kastilya) — CONFIRMED (c1s3; A1 #1, #2). Aragon bölgesine Napoli/Sicilya/Sardunya da boyalı (A1 #2).
- "5 AY", "İKİ YAŞINA BASMAMIŞ KUZEN" — HAFIZA H4 (web özeti doğruladı: Miguel da Paz, 19 Tem 1500); ekranda isim yok, yalnız anlatıdaki ifade.
- EVLİLİK / ÖLÜM — YORUM (c1s5, özet).
- "6 YAŞINDA", Burgos, Filip — CONFIRMED (c1s6; A1 #3).
- Tordesillas, "1509", "46 YIL" (1509 → 1555 çubuğu) — CONFIRMED +H5 (c1s7–s8; A1 #3 "≈46 yıl", A5 #12 "12 Nis 1555"). "1555" anlatıda yok; araştırma belgelerinden.
- DELİLİK? / SİYASET? / TARTIŞMALI — CONFIRMED (c1s9; A1 #3 notu: "delilik teşhisi tartışmalı").
- Mechelen, Margareta (hala), "ANA DİLİ: FRANSIZCA" — NİTELİKLİ (c1s10; A1 #4 Mechelen yılları net değil, A1 #5 ilk dil Fransızca).
- Dört dil sözü (TANRI/ESPAÑOL, KADINLAR/ITALIANO, ERKEKLER/FRANÇAIS, ATI/DEUTSCH) — RİVAYET (ANEKDOT; c1s11; A1 #23) → RİVAYET damgası. Dil adları anlatıdaki dil adlarının özgün yazımı.
- 1558 ÖLÜM, 1601 İLK YAZILI KAYIT, YAKLAŞIK 43 YIL, BELGE BİLİNMİYOR — NİTELİKLİ (c1s12; A1 #23: ilk kayıt 1601, ölümden ≈43 yıl; "belge yok" olumsuz iddia, düşük risk). 1558 ve 1601 anlatıda söylenmiyor; belgelerden.
- Fernando "† 1516", Kastilya ve Aragon armaları, Juana (parmaklıklı) ile ortak kral — CONFIRMED (c1s13; A1 #7; ortak ilan A1 #8 NİTELİKLİ). Ekranda yalnız "1516" yılı (anlatıda söyleniyor).
- EYLÜL 1517, SANTANDER (hedef), TAZONES, KÜÇÜK BALIKÇI KÖYÜ — CONFIRMED +H6 (c1s14; A1 #9). "Balıkçı köyü" ayrıntısı araştırmada yok (H6, düşük).
- "17 YAŞINDA · KRAL" + soru işaretleri — NİTELİKLİ (c1s15; A1 #5 notu, tek popüler kaynak; "henüz iyi" yumuşatılmış). "17" anlatıda.
- VALLADOLID KORTESİ · 1518; "Kastilyacayı öğren." / "Yabancı danışmanlarını gönder." — NİTELİKLİ (c1s16; A1 #10; akademik doğrulama yok). 600.000 dukat servicio ekranda yok.
- Ekrandaki hiçbir sayı/ad/tarih anlatı ya da `kaynaklar.md`/`arastirma/*.md` dışından gelmiyor. Altyazı yok. HUD alanları (sağ üst 420×110; ilk 5,5 sn sol üst 800×90) boş.

## (d) Ana ajandan istekler / uyarılar
1. `shots.py:449` (`doc`): kâğıt tohumu `hash(title) % 97` — Python `hash()` her süreçte değişir; çok süreçli render'da belge kenarı kareler arasında titrer/değişir. Kendi belge çekimlerim için düzeltilmiş kopya `a_doc` (kit_a; `zlib.crc32`). Öneri: `shots.py`'de `zlib.crc32(title.encode()) % 97 + 3` ya da render'da `PYTHONHASHSEED=0`. Başka bölümlerin `doc` kullanan çekimleri etkilenir.
2. `shots.py` `doc`, `align="c"`: açılış kırpması sol kenardan başladığı için ortalı satırların sağ kısmı hiç açılmıyor (satır yarım kalıyor). `a_doc`'ta düzelttim (kırpma `x_left = -genişlik/2`). `doc`'u `align="c"` ile kullanan başka çekim varsa aynı sorunu görür.
3. `shots.py` `medals`: `it["at"] + 0.4` çapa demetiyle `TypeError`. Çözüm olarak `kit_a.a_medals` (çapa destekli; `date=`, `stampt=`, `ghost=`, `bgname=` ekli) — başkaları da kullanabilir.
4. `name_plate`: metni `w`'ye sığdırmıyor; uzun adlarda (örn. "KÜÇÜK ŞARLKEN") `w`'yi elle genişlettim.
5. `kit_a.a_map` (`map` şablonunun üstü): kara kabartma dokusu ve `tint` renk tonu döşeme önbelleğine pişiyor (kare başına ek maliyet yok) ve kamera yolundaki döşemeler çekimin ilk karesinde önceden pişiyor; yalnız çağrı süresince `MapView` örneğine geçici öznitelik takıp geri alıyor, kalıcı değişiklik yok. Aynı görünüm istenirse diğer bölümler `a_map`'i (`map` ile aynı parametreler + `need`, `stampt`, `relief`) kullanabilir.
6. `a_theatre` sarmalayıcısı lab sahnesi hata verirse yer tutucu çizer (önizleme/Program çökmesin); nihai render'da "[sahne hata: …]" yazısı görünürse ilgili lab sahnesi bozulmuş demektir.
