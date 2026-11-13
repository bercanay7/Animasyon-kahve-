# Medici c6–c16 — inceleme düzeltmelerinin uygulama raporu (19 Ekim 2026)

Kaynak: `inceleme_c6_c16.md`. Dokunulan dosyalar: `scr_c6.py … scr_c16.py` (c6'dan c16'ya hepsi), `script.py` (yalnız docstring). `scr_c0…c5` DOKUNULMADI; `ses_paketi.py --kontrol` c0–c5 için "metin değişti" uyarısı vermedi (sha aynı). Git kullanılmadı (commit/push yok).

## 1. Özet

- **Cümle sayısı HİÇBİR bölümde değişmedi** (c6 27 · c7 47 · c8 34 · c9 28 · c10 36 · c11 38 · c12 35 · c13 38 · c14 26 · c15 19 · c16 25). Kimlikler kaymadı; brif/docstring kimlik güncellemesi gerekmedi. Rapor c7s19'un silinmesini önermişti: SİLİNMEDİ, köprü cümlesine çevrildi.
- 28 sözcüğü aşan cümle yok (en uzun 28: c6; kontrol: `S.sentences()` ile söylenen sözcük sayımı).
- Toplam söz 7270 → 7403 (≈71,3 → 72,6 dk). Parçalar: P3 10,1 · P4 8,4 · P5 11,3 · P6 10,9 · P7 10,7 dk.
- **ElevenLabs maliyeti:** tüm film 53.205 → **54.238 karakter/kredi** (≈ $10,85); c6–c16 (üretilecek) 37.613 → **38.646 kredi ≈ $7,73** (+1.033 kredi, +$0,21). Bölüm başına karakter: c6 3132 · c7 4716 · c8 3455 · c9 2937 · c10 3837 · c11 4719 · c12 3958 · c13 3786 · c14 3018 · c15 2604 · c16 2484.

## 2. Aynen uygulananlar (cümle kimliği → özet)

| Kimlik | Değişiklik |
|---|---|
| c6s1 | P3 açılışı: "Cosimo'nun torunu Lorenzo de' Medici'yi yakın dostu Niccolò Valori anlatır…" ("en iyi dost" → "yakın dost") |
| c6s2 | "Floransa'nın bu tahtsız efendisi" (c5s19 geri çağrısı; şehir kurulur) |
| c6s4 | "Valori'ye atfedilen tarife göre koku duyusu da neredeyse yoktu." ("bile" kalktı) |
| c6s22 | Botticelli sancağı "…resmettiği anlatılır" (kip etiketle uyumlu); etiket ○/○ |
| c7s3 | Riario "16 ya da 17 yaşındaki" |
| c7s10 | "İtalyan Ansiklopedisi Treccani" (parçada ilk geçiş) |
| c7s22 | Tunç kapı: "sakristinin ağır tunç kapısını…"; kapı ustaları seste yok |
| c7s46 | "Aynı yıl bu olay bronza da döküldü…" ("o sabah bronza" hatası giderildi). c7s47 aynen kaldı |
| c8s1 | P4 açılışı: suikast + Salviati'nin asılması bağlamı, "Haziran 1478'de … aforoz", gün söylenmez |
| c9s7 | Portinari = Brugge'de yıllarca yardımcı, sonra "şubenin müdürü ve ortağı" ("genel müdür" belirsizliği bitti) |
| c9s11–s12 | Londra: "toplam … kredi verdi / Bir kısmı geri ödendi; kalanı için Güller Savaşı suçlanır, ama rakamlar kaynaktan kaynağa değişir" (kredi ≠ kalan borç) |
| c9s18 | "Tarihçi Raymond de Roover…", "genel bir banka krizi" |
| c9s21 | "Lorenzo'nun oğlu Piero kaçtı" |
| c9s28 | "Peki Medici'yi sürgüne gönderen o güne nasıl gelindi?…" |
| c10s1 | "Floransa'nın efendisi Lorenzo de' Medici" (P5 açılışı) |
| c10s12 | Sarzana: "Alpler'i aşıp gelen Fransa Kralı VIII. Charles'a" → "Sekizinci Şarl'a" (22 söz) |
| c11s6 | Alfonso d'Este atı artık "…yürüttüğü anlatılır" |
| c11s14 | Giulio = VII. Clemens bağı kuruldu (26 söz; Şarlken cümlesi hâlâ tek) |
| c11s22 | "Ne düşündüğünü bilmiyoruz…" kalıbı düz anlatıma çevrildi (kalıp c8s11, c10s17'de kaldı) |
| c11s30–s31 | Cumhuriyetin teslimi + saklanma geleneği ("söylenir") + bağışlama; 1975 odası "çizimleri Michelangelo'ya bağlamak tartışmalıdır" |
| c11 (PRON) | Mainz→Mayns, Luther→Lüter, Fabrizio→Fabritsyo, Ferruccio→Ferruçço (eski "Ferruççio"nun yerine), Castel→Kastel ("Castel Sant'Angelo" satırından sonra), d'Este→deste |
| c12s1 | P6 açılışı: "Floransa Dükü Alessandro'yu kuzeni öldürmüş… Medici'nin yan kolundan 17 yaşındaki Cosimo'yu" |
| c12s23 | "Rivayet ölümlerden çok sonra ortaya çıktı; ilk yazanını gösteremiyoruz." (araştırma sınırı literatür iddiası gibi çıkmıyor) |
| c12s35 | Kapı tek cümle: "Cosimo Floransa'da bir devlet kurarken, aynı yıllarda Paris'te…" (zaman geri sarmıyor) |
| c12 (PRON) | Mugello→Mucello |
| c13s4 | "Düğün Marsilya'daydı; gelin 14 yaşındaydı." |
| c13s17 | "Sonra her şey onun hanesine yazılmaya başladı…" (c12s31 "fatura" metaforu tekrarı kalktı) |
| c13s28 | `{Henri IV\|Dördüncü Henri}` → söylenen "Dördüncü Anri" |
| c13s29 | "Ne düşündüğünü…" kalıbı kaldırıldı |
| c14s1 | "Büyük Dük Cosimo'nun oğlu Kardinal Ferdinando" (hangi Cosimo) |
| c14 (PRON) | Scipione→Şipyone |
| c15s2 | "bir gün arayla" (19/20 Ekim 1587) |
| c15s3 | "ilk anlatıcısını gösteremiyoruz" |
| c15s13 | K1 giderildi: "tek kaynak hattı" iddiası kalktı; "yün geriledi, ipek gelişti diye yazılır" (27 söz) |
| c15s19 | "Toskana'yı yöneten erkek hat kapanmıştı…" |
| c16s2 | "istediği yerine gelmemiş" çıkarımı kaldırıldı |
| c16s8 | Tırnaksız: "Kaynaklar onu tek yaratıcı değil, en görünür patronlardan biri olarak anlatıyor." |
| c16s9 | Primavera "büyük olasılıkla" |
| c16s16 | "Capitoline ondan önce halka açılmıştı" |
| c16s19 | "Medici defterlerinin bir kısmı… Harvard'da" |
| Treccani tanımı | "İtalyan Ansiklopedisi Treccani": c7s10, c9s17, c11s35, c12s4, c15s15 (parçalardaki ilk geçişler; c6/c8/c10/c14/c16'da Treccani zaten yok) |
| c8 (PRON) | Bargello→Barcello, Poggio Imperiale→Pocco İmperyale (eski "Poççio") |
| c9 (PRON) | Raymond→Reymond (c2'deki "de Rover" ile tutarlı; global PRON etkisi c0–c5'te yok, doğrulandı) |
| c7 (PRON) | Maffei→Maffey (kimlik eşlemesi değişti; c14s22 "Scipione Maffei" de aynı okunur) |
| c7s19 | **Silinmedi.** "Giuliano 24 yaşındaydı." → "Ama hedef yalnız Giuliano değildi." (5 söz; iki kardeş planı c7s7'den; P7 paragrafı "Aynı anda Lorenzo'ya iki papaz saldırdı"ya köprü; ağır sahne, mizah yok). Yaş yalnız c6s27'de kaldı |

## 3. Uyarlananlar (rapordan farklı uygulandı; gerekçeli)

- **c16s3** — Rapordaki yedek cümle söylenince 30 sözcüktü (rapor "26" demişti; rakamlar söze çevrilince uzuyor) → 28 sözcük sınırını aşıyordu. "31 Ekim 1737'de imzalanan" → "1737'de imzalanan", "mülkiyeti alırken" düşürüldü, "o bir" → "bu bir": **26 söz**. Gün c0'da ve ekranda zaten var. c16 docstring'ine "1737" söylenen sayı olarak eklendi.
- **c12s24** — Rapordaki cümle (2026 DNA dahil) söylenince 32 sözcük (>28). Ayrıca 2026 çalışmasının "Francesco'nun kaburgaları" olarak c15'te açılması ve c15 docstring'i ("2026'daki Giovanni söylenmez") korunsun diye c12'ye yıl konmadı: "…şiddet izi görülmedi; sonraki kemik incelemeleri sıtmayla uyumlu bulgular verdi." (24 söz; "gösterdi" yerine "uyumlu bulgular verdi" — daha temkinli). Etiket 2010 TRSTMH + 2026 iScience'i anar, "makale açılmadı — yayın öncesi teyit".
- **c12s14** — Rapor "…koridorla uzatıldı" dedi; `sfx_cues_p6.json` c12s14'te **"koridora"** sözcüğüne çapa atıyor ve "koridorla" bu çapayı koparıyordu. Anlamı koruyarak: "1565'te Uffizi'nin üst katı, Palazzo Vecchio'yu Pitti Sarayı'na bağlayan, Arno'yu aşan bir koridora ulandı: iktidarın ofisinden evine kapalı bir yol." (Koridor ayrı yapı olarak anlatılıyor; "galeri koridora dönüştü" yanlışı yok.)
- **c13s38** — Rapordaki "kestiriyor, sahneletiyor, yazdırıyordu" iki sorun taşıyordu: (1) "sahneletmek" Türkçe değil ("sahnelettirmek"), (2) üç eylemde zaman karışıyordu. Uygulanan: "…ailenin Floransa'daki kolu Arapça harf kestirip, opera sahnelettirip, gökyüzüne de adını yazdırıyordu." muzik.py'nin c13s38'deki **"gökyüzüne" / "yazdırıyordu"** sözcük çapaları korundu.
- **c14s3** — Rapordaki "Daha bu baskılar çıkmadan, … ferman çıkmıştı" (çıkmadan/çıkmıştı yankısı) yerine "Bunlar basılmadan önce İstanbul'dan bir ferman çıkmıştı: …" (anlam aynı; ferman Ekim 1588 < baskılar 1590–94).
- **c14s4** (rapor "isteğe bağlı" demişti) — uygulandı: "evet, 1478'de Giuliano'yu vuranlardan biriyle aynı soyadı…". Hem P4'ten uzak izleyen için, hem de olgu için daha doğru: Giuliano'yu iki kişi vurdu.
- **c16s21** — Rapor "çürüttüğümüz → ayıkladığımız" dedi; "ayıkladığımız" anlamı bulanıklaştırıyor, tablo zaten düzeltilen mitlerin → "düzelttiğimiz".
- **c8s1** — Rapordaki "Floransa'nın kendisine de yasak" → "Floransa'ya da yasak" (cümle 28 söz sınırında kalıyordu → 27).
- **c9s12** — Etiketteki "mizah a: kaynaklar da uzlaşmıyor" korundu (c9 docstring'i bu mizaha izin veriyor).

## 4. Uygulanmayanlar (gerekçe)

- **c12s18 "çerçeve notu"** (Müslüman esirlerin de alındığı, esir satışı): dayanağı "genel bilgi ○ / HAFIZA"; araştırmada yok; kaynak kapısı HAFIZA'yı metne sokmaz ve "yeni olgu ekleme" kuralı var. **Teyit listesine** eklendi (Türk izleyici dengesi için değerli; Türkçe/İtalyanca kaynakla doğrulanırsa eklenebilir).
- **c11s17** ("yüz seksen dokuz kişilik … yüz kırk yedi kişi öldü"): muzik.py'nin **("c11s17","yedisi")** sözcük çapasını koparır; kazanç küçük zevk. Dokunulmadı.
- **c13s20** (ulus genellemesi → "Hem inceliği hem günahı…"): rapor "kimlik tahsis edilmedi/istenirse" demişti; mizah hedefi zaten "mit düzeni"; orijinal vuruş daha güçlü → bırakıldı.
- **c15s6 "kesinlik düzeyi"**, **c10 ritim notu** (s15/s17/s18 üç hedge), **c15s9–s10 bölme**, **Britannica/Treccani atıf azaltma**, **gonfaloniere/Opificio okunuşu**: rapor yedek cümle vermedi, "küçük/zevk" dedi; kaynak disiplini (hedge'ler kaynak sınıfından geliyor) ve cümle sayısı korunsun diye dokunulmadı.
- Rapor önerisi **yanlış çıkan yok**; reddedilen yalnız yukarıdakiler.

## 5. Bakım düzeltmeleri

- `scr_c7.py` docstring: "Parça 2'nin soğuk açılışı" → "Parça 3'ün ikinci bölümü"; K1 kapı notu: aforoz gün söylenmeden. `scr_c12.py` docstring: "Parça 3'ün soğuk açılışı" → "Parça 6'nın açılışı". `script.py` başlığı: eski "P1 = c0–c6…" bölümlemesi → güncel 7 parça + perde notu. `scr_c12s24` etiketindeki "2026 DNA GİRMEZ" kalktı.

## 6. Doğrulama

- `python3 script.py` hatasız; ortalamalar: c6 16,0 · c11 16,9 · c12 16,0 · **c15 19,0** (üst bant; rapor "yorgun ruh haline uyuyor" demişti, s13 +1 söz). `python3 script.py cN` ile değişen her cümlenin söylenen metni okundu (Lorentso de Mediçi, Sekizinci Şarl, Dördüncü Anri, Mayns/Lüter/Fabritsyo/Ferruçço/Kastel/deste, Barcello, Pocco İmperyale, Mucello, Reymond de Rover, Şipyone Maffey, tarihlerin harfle okunuşu doğru).
- `python3 ses_paketi.py --kontrol`: c0–c5 sha eşleşiyor; yeni toplam 54.238 kredi.
- `kaynak_tablosu.py --part 1..7`, `okunus_tablosu.py --part 1..7` (kaynaklar_P*.md, okunus_P*.md yenilendi), `is_emri.py --hepsi` hatasız.
- **Sözcük çapa denetimi** (muzik.py, miks.py, sfx_cues_p*.json içindeki `("cNsM","sözcük")` çapaları, yeni metne karşı): benim değişikliklerimden kaynaklanan kırık yok (c12s14 "koridora" düzeltildi). Kalan 8 kırık çapa değişiklikten ÖNCE de vardı (muzik.py c9s14 Avignon/Brugge, c10s14 Palazzo, c15s4 2006/2010, c15s5 2026; sfx_cues_p4.json c9s14 ×2) — ASR yazımına bağlı, gerçek ses sonrası yeniden bakılmalı. `notlar_oda.md`/`notlar_dunya.md`/`notlar_yonetmen_motoru.md` içindeki bazı çapalar (örn. c9s7 'kapandı', c7s16 'kapı', c15s4 'ofis') zaten metinde olmayan sözcüklere işaret ediyor (Lab ajanlarının notları; bana ait değil).

## 7. Başka ajanları / sonraki adımları ilgilendirenler

- **Scratch ses yeniden üretilmeli:** `ses_gecici.py cN` — **yalnız değişen bölümler: c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16** (hepsinde en az bir cümle değişti). `out_pN/timeline.json` zamanları (P3–P7) eskidir; benden düzeltilmedi. Gerçek ses Çarşamba üretilecekse scratch yalnız ara kontrol için gerekir.
- **Brif/iş emri alıntıları kısmen eskidi** (script.py tek kaynak): `brif/c7_brif.md` ekran kartı «17» artık "16 ya da 17", «24» kartı c7s19'da **söylenmiyor** (yaş c6s27'de; kart istenirse sessiz kalır) ve s46 alıntısı "o sabah bronza"; `brif/c8_brif.md` V1 alıntısı ("1 Haziran 1478'de…") ve ekran tarihi (belge görselinde gün gösterilebilir ama seste yok); `brif/c9`, `c10`, `c12`, `c13`, `c14` ilgili cümle alıntıları. Sahne yazarları cümle kimliğine ve `isemri/*.md` (yenilendi) tablosuna bakmalı.
- **Sahne/görsel etkileri:** c13s38 artık matbaa–opera–gökyüzü sırasını söylüyor (c14 sırasıyla uyumlu); c10s12'de "Fransız kampı" yerine "kamp" + "VIII. Charles" adı (c10s14'teki "Fransız kampından dönmüş" ile uyumlu); c12s14 koridor görseli "Uffizi üst kat → Arno üstü koridor → Pitti" olarak okunmalı.

## 8. Kalan "yayın öncesi teyit" kalemleri (raporun 15 kalemi + yeni)

Raporun listesi aynen geçerli (1 Riario yaşı · 2 aforoz/interdikt günleri · 3 Giuliano doğum günü · 4 Londra kredi rakamları · 5 Sassetti 1463↔1458/59 ve Goldthwaite · 6 Valori Vita · 7 Bandini zinciri · 8 Mehmed II 3 Mayıs 1481/Otranto Eylül 1481 [HAFIZA-Y, kaynaklar_P4'te hâlâ HAFIZA satırı] · 9 Alfonso d'Este/possesso · 10 Eleonora 29 Mart/Haziran/Temmuz · 11 Garzia/Giovanni sıtma kanıtı (2010 TRSTMH, 2026 iScience metni) · 12 Francesco/Bianca 19–20 Ekim · 13 Mustafa Ağa 1598 + Bandini/Branton fermanı 1587/1588 · 14 Vasari Koridoru/Uffizi 1565 ve 1769 · 15 Lepanto 12 gemi + Santo Stefano amacı). Ek:

16. **Michelangelo'nun cumhuriyetin düşüşünden sonra saklanması** (c11s30, yeni cümle; iki gelenek, "söylenir") — Condivi/Vasari, bm8.
17. **Santo Stefano'nun Müslüman esir alması** (c12s18 için reddedilen çerçeve cümlesi) — Türkçe/İtalyanca kaynak.
18. **1737 sözleşmesi "bir akademik yoruma göre devir koşulu"** (c16s3; tek özet ○).
19. **c8 Mehmed II / c12 Osmanlı İnebahtı yenilgisi** HAFIZA-Y satırları (c8s32, c12s33): Türkçe/Osmanlı kaynağı.
