# notlar_c0 — KANCA (Parça 1 açılışı · 101 sn · gerçek ses)

Dosyalar: `scenes_c0.py` (16 çekim), `c0_kinds.py` (özel türler), `p1_ortak.py` (Parça 1 ortak bindirme kurucuları + `p1_*` sarmalayıcılar), `yonetmen_c0.md`.
Çekim sırası: şehir silüeti → 1743 odası (zoomthru) → taht/yabancı birlik (iris) → Medici salonu → imza masası 1737 (candle) → 114 gün takvimi → masa/mühür (zoomthru) → belge (14,8 sn, tek kamera) → masa başı → III. madde → galeri (Vasari koridoru) → harita → gerekçe (üç madalyon) → Uffizi kuyruğu (audio) → banka köşesi → sikke/geri sarma (1252).

## Kısıtlar (uygulananlar)
- **Işık/ay:** pencerede AY/YILDIZ yok, "gece" iddiası yok. Oda `tod="dusk"` (alacakaranlık + mum havuzu, pencere nötr soluk cam); ilk çekim şehir silüeti de aynı sıcak "dusk" gökle. Kaynak saat/hava söylemiyor; "dusk" tod seçenekleri içinde en nötr olandır ("night" ay çizer, "day" mumu söndürür). Gerekçe `yonetmen_c0.md` "neden böyle" (2). Belge/saat geri sarma çekimleri `mode="night"` yalnız renk derecelendirmesidir (koyu lapis palet); gökyüzü/gece iddiası taşımaz.
- **Alıntı kartı:** "SÖZLEŞMENİN 3. MADDESİNİN ÖZETİ" — Anna Maria Luisa'ya ATFEDİLMEZ (c0_harita, `sinir_extra`).
- **Hook:** P1'de bölüm kartı yok, "ALTIN FLORİN" bindirmesi yok (P2+). İlk çekimin orta bandı boş; kick etiketi ("18 ŞUBAT 1743 · FLORANSA") üst bantta. `fresco_title` c0'dan sonra Program'ca eklenir.
- **Yüz/şiddet:** yatak, taht, masa, kuyruk figürleri SİLÜET (yüz yok); asker siluetleri yalnız yürür (hellebard), şiddet yok; ölüm odasında mizah kapalı.
- **c16 dönüşü:** c0'ın "banka köşesi" + geri sarma halkası, c16'daki aynı odaya ters yoldan dönüşün ön işaretidir (oda 1743 aynı `room="oda1743"`, aynı `ODA_DUSK`).
- Mutlak saniye yok: tüm çapalar cümle/sözcük kimliğine bağlı (qa_flow: mutlak %3 — tüm Parça 1).
- Dokunulmayanlar: `compose.py`, `shots.py`, `cilt_*.py`, `qa_flow.py`, `sfx_cues_p1.json`, `out_p1/*`, `parca.kullan()`.

## Ekrandaki olgular ve kaynak sınıfı (kaynaklar_P1.md ile)
| ekran | cümle | sınıf |
|---|---|---|
| 18 ŞUBAT 1743 · FLORANSA; ANNA MARIA LUISA levhası | c0s1–2 | ◐ (M4:#107; 75 yaş 6 ay = hesap, ekranda yaş yok) |
| Medici arması (kod çizimi, duvar arması) | c0s3 | ◐ M4b:D15 |
| 5 YIL 7 AY ÖNCE (boş taht, hellebardlı siluetler) | c0s4 | ◐ M4:#99,D2 (hesap) |
| 31 EKİM 1737; 114 GÜN (takvim) | c0s6 | ◐ M4:#104 (114 gün = hesap, brif ekran kartı) |
| iki mühür; ANNA MARIA LUISA / LORRAINE TARAFI | c0s7 | ◐ M4b:b73 (imzacı adı söylenmez/yazılmaz) |
| 13 MADDE (sayaç) + Romen rakamları I–XIII | c0s8 | ◐ M4b:bD24,D10 |
| FRANSIZCA damgası; ITALIANO yazılır, çizilir | c0s8–9 | ◐ + YORUM (mizah: dil) |
| III. madde vurgusu (çevre kararır, sinabar çizgi) | c0s11 | ◐ M4b:bD23 |
| ÇEVİRİ damgası; GALERİLER · TABLOLAR · HEYKELLER · KÜTÜPHANELER · MÜCEVHERLER · ÖTEKİ KIYMETLİ ŞEYLER | c0s12 | ◐ çeviri lafzı M4b:bD23,b74 |
| BÜYÜK DUKALIK dolgusu (yaklaşık sınır, zincir/kilit) + özet kartı | c0s12 | ◐ (harita yaklaşık: ölçüsüz, sınır "temsilî") |
| DEVLETİN SÜSÜ · HALKIN YARARI · YABANCILARIN MERAKI | c0s13–14 | ◐ çeviri lafzı M4:§5.19 |
| Uffizi kuyruğu (siluet, sayı yok) | c0s15 | YORUM (bugünle çarpıştırma) |
| soru işareti; kılıç ✗ + sikke; 1737 → 1252 geri sarma halkası | c0s16–18 | YORUM / hesap (1743−1252 = 491 → "beş asra yakın") |

## Bilinen kusurlar
1. `c0_belge` (14,8 sn) ve `p1_oda` ilk iki çekim kendi kamera yolundadır (`cams=`); `cam=` yalnız varlık işaretidir (`OWN_CAMERA`: uygulanmaz; pikselce aynı olduğu doğrulandı).
2. Kısa (2,4 sn) III. madde çekimi, iki zoomthru'nun (giriş + çıkış) ortasında; `--check` ms/kare örnekleri geçiş penceresine denk gelip şişiriyor (#9: ≈330–380 ms, #7: ≈265–280 ms; çekimin tek başına maliyeti ≈110 ms; bölüm ortalaması ≈160–175 ms/kare — makine yüküne göre dalgalanır). Motorun eşiği 450 ms; hedef 250 ms'yi yalnız bu iki ölçüm aşıyor.
3. Harita çekimi "yaklaşık" sınırdır (Toskana poligonu `c0_kinds.ensure_toskana` ile yerelde kurulur); kartta bu ölçüsüzlük "temsilî" olarak geçer, kaynak sınıfı ◐.
4. Skyline (çekim 1) `tod="dusk"` gün batımı gökyüzüdür; ay yok, ama gökyüzü rengi "akşam üstü" hissi verir — kaynak saat söylemediği için nötr tutuldu; istenirse `tod="day"` ile değiştirilebilir (tek satır).

## Ana ajandan istekler (motor/dünya; ben dokunmadım)
- `mapsk.add_region(clip_to_land=True)`: Toskana poligonunda boş çokgen üretiyor (projeksiyon uyuşmazlığı). Yerel çözüm `c0_kinds.ensure_toskana`; kalıcı yama önerisi: `clip_to_land` poligonu bölgeyi Mercator'a çevirmeden kırpıyor.
- `cilt_cam.OWN_CAMERA` dosyada yalnız `pano`/`build` (+`sehir` kendi ekler); `oda` eksik. `p1_ortak.py` çalışma anında `p1_oda/p1_pano/p1_sehir/p1_build`'i ekliyor; resmî eklenirse `p1_oda` sarmalayıcısına gerek kalmaz.
- `qa_flow.py --chapters cK` tek bölümle koşunca olay yoğunluğunda yapay sapma veriyor (bölüm başı/sonu pencereleri komşu bölümden kopuk); gerçek kapı `--part 1`.

## Kapı sonuçları (qa_flow --part 1, tüm Parça 1; 92 çekim, 1197 örnek kare)
| kapı | sonuç |
|---|---|
| Durgunluk | GEÇTİ — en uzun durgun koşu 0,5 sn (eşik ≤1,5) |
| Kamera varlığı / yeterliliği | GEÇTİ — 92/92 `cam=` (%100); 0 zayıf |
| Gerekçeli geçiş | GEÇTİ — link %100 (89/89); çıplak fade %0; çıplak kesme 0 |
| Çekim uzunluğu | GEÇTİ — c0 medyan 5,99 sn (16 çekim; max 14,8 sn belge) |
| Tür tekrarı | GEÇTİ — 0 ihlal |
| Çapa denetimi | GEÇTİ — sözcük 239 · cümle 107 · mutlak 9 (%3) |
| Yön denetimi | GEÇTİ — 0 uyarı; c0 bilinçli yön bozma: banka köşesi `slide l` (kartta gerekçeli) |
| Altyazı bölgesi | GEÇTİ |
| Yönetmen kartı | `yonetmen_c0.md` 16 satır = 16 çekim, tür sırası aynı |
| Olay yoğunluğu | GEÇTİ — Parça 1 geneli %96 (82/85); olaysız cümleler: c0s8 (belge planında kamera zaten sürekli hareket ettiği için '13 MADDE'/FRANSIZCA vuruşu taban MAD'in 2,2 katına çıkmıyor), c1s30, c1s31 |
| `preview_chapter.py c0 --check` | uyarı yok; ort. ≈160–175 ms/kare, tahmini render ≈6,5–7 dk (yalnız #7 ve #9 örnekleri >250 ms; ikisi de geçiş penceresi artefaktı) |

Görsel denetim: kontak sayfaları tek tek görüldü; `--clip` ile oda → belge zoomthru'su (33,2–35,2 sn) ve belge → galeri zoomthru'su (55,8–57,6 sn) kare kare akıyor (kamera derinliği kesintisiz, boş kare yok).
