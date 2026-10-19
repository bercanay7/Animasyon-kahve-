# MEDICI — Müzik / SFX / Miks hattı (notlar_ses.md)

Şarlken hattının (muzik.py · sfx.py · miks.py · miks_kur.py · ses_dsp.py) Medici'ye uyarlanmış, **tam sentez** (örnek dosya YOK, telifli melodi YOK), **tohumlu/deterministik**
sürümü. 17 bölüm = 17 müzik cue'su; yayın **7 parça** (≈10 dk), her parça AYRI miks edilir. Bu dosya hattın kullanım kılavuzu, cue/SFX tabloları, ölçüm
sonuçları, bilinen sınırlar ve ana ajandan isteklerdir. (Kod yorumları ve raporlar Türkçe.)

---
## 1. Kullanım komutları

Hepsi `gunluk-shorts/medici-uzun-dosya/` içinde. `MEDICI_PART=1..7` ZORUNLU; `out/` sembolik bağlantısı ve `parca.kullan()` ASLA kullanılmaz (tüm yollar `out_pN`).

```bash
MEDICI_PART=2 python3 miks_kur.py --kontrol                 # yalnız girdi tutarlılığı (dosyalar, süre, bölüm dizilimi, parça dışı bölüm, geçici ses, sfx_cues tazeliği)
MEDICI_PART=2 python3 miks_kur.py                           # FİNAL miks → out_p2/mix_audio.m4a (+ stem_music|voice|sfx.flac, sfx_cues_used.json, audio_report.txt)
MEDICI_PART=4 python3 miks_kur.py --onizleme --preview      # GEÇİCİ (Piper) ses / eksik bölüm: ONIZLEME_ önekiyle yazar; + out_p4/ses_onizleme/*.mp3 (20–30 sn kesitler)
MEDICI_PART=2 python3 miks_kur.py --gecis-sesleri           # önce görüntü motorundan (compose.Program) geçişleri okuyup out_p2/sfx_gecis.json üretir, sonra miks
MEDICI_PART=2 python3 miks_kur.py --sadece-gecis            # yalnız out_p2/sfx_gecis.json üret
MEDICI_PART=3 python3 muzik.py --cue c7 --out /tmp/c7.wav  # tek bölüm/kesit müzik önizleme (ducking'siz ham); --all: tüm parça; --diag c7: katman enerji tablosu
python3 sfx.py --list | --katalog | --render page_turn --out x.wav [--dur 2 --seed 3] | --all --out klasor | --gecis-ornegi
```
Seçenekler: `--fresh` (müzik önbelleğini yok say) · `--snr 20,24` (konuşma−müzik penceresi) · `--workers N` (**en çok 1**: paylaşımlı 16 GB makine; bir parça miksi ≈2,4 GB tepe bellek) · `--no-gecis` · `--no-stinger` · `--no-stems` · `--keep-wav`.
Deneme/fixture için `MEDICI_OUT_DIR=/yol` çıktı dizinini değiştirir (varsayılan `out_pN`).

**Koruma:** `miks.main()` final miksten (adsız çıktı) önce `parca.assert_gercek_ses()` çağırır — `out_pN/GECICI_SES.json` varsa (Piper) **DURUR**; eksik bölümlü parça da DURUR.
`--onizleme` ile (ya da geçici ses/eksik bölüm algılanınca) tüm çıktılar `ONIZLEME_` önekini alır ve final adıyla ASLA yazılmaz. `voice_chapters.json` içinde parçaya ait olmayan bölüm
(eski 3 parçalı düzenin kalıntısı) varsa hat DURUR (`script.PARTS` esastır).

Gerçek ses gelince: `ses_birlestir.py` + hizalayıcı yeni `voice.wav`/`voice_chapters.json`/`timeline.json` üretir → `MEDICI_PART=N python3 miks_kur.py` aynen yeniden çalışır:
müzik çıpaları ve SFX çıpaları **cümle kimliklerinden yeniden çözülür** (önbellek anahtarı = sentez kodu + çözülmüş spec + geometri + tohum; çıpa kayarsa yalnız o kesit yeniden üretilir).
Tam parça miksi ≈2–4 dk (müzik ~30 sn, kalan miks/master/AAC).

### Parçalar (tek doğru kaynak: `script.PARTS`; kod sabit kodlamaz)

| Parça | Bölümler | Perde(ler) | Açılış | Kapanış (7 sn kuyruk) |
|---|---|---|---|---|
| P1 | c0–c2 | ALTIN | c0 ile açılır; c0 sonunda ana başlık vuruşu (c0 t1 + 0,4 sn; c1 kartı = ana başlık) | "SIRADAKİ PARÇA": `dissolve` (açık beşli + gamba + tek lavta notası) |
| P2 | c3–c5 | ALTIN | t=0 doğrudan (kart yok; 1,2–4,8 sn "MEDİCİ / PARÇA 2" bindirmesi) | `dissolve` |
| P3 | c6–c7 | ALTIN → BEDEL | t=0 (c6); c7 normal kartla gelir (c6 kesit 2 "gölge" + bedel yayı köprüler) | `dissolve` |
| P4 | c8–c9 | BEDEL | t=0 | `dissolve` |
| P5 | c10–c11 | BEDEL | t=0 | c11 `end_kind="p2"`: çözülmeyen sus4 + hafif 'miras' hücresi (P6'ya köprü) |
| P6 | c12–c13 | MİRAS | t=0 ('miras' hücresi lavtada) | `dissolve` |
| P7 | c14–c16 | MİRAS | t=0 | "TÜM FİLM": c16 `end_kind="p3"` D majör çözülüş, ters 'miras' hücresi, son lavta notası, son sessizlik (soru açık değil) |

Perde (ALTIN c0–c6 · BEDEL c7–c11 · MİRAS c12–c16) **bölüm bazlıdır**: bölüm kartı vurgusunun rengi gelen bölümün perdesinden gelir (`muzik.flavor_of`).
Kuyruk 7 sn = `compose.OUTRO`; mix süresi = voice + 7 sn (kontrol listesinde doğrulanır).

---
## 2. Cue tablosu (bölüm → mod / tempo / ana fikir / çıpalar)

Ses kimliği: lavta (Karplus–Strong, çift kurs), klavsen, portatif org/regal, viola da gamba (drone + "çekilen yay"), formant süzgeçli koro pedi, çerçeve davulu + tef,
gong/çan (**yalnız müzikal tını; olay çanı değil**), timpani/alt-bas (yalnız vurgu). Tempo 52–84 bpm. Her cue kendi tonikinde; cue sınırlarında yalnız **açık beşli** (üçlüsüz) yatak
(`junction_pads`) → komşu cue'larla armonik çatışma olmaz; çapraz geçiş 4–7 sn (merkez = bölüm kartı boşluğunun ortası).
Motifler: **florin** (0-2-4-7 yükselen parlak figür; ALTIN) · **palle** (altılı 2+2+2 hemiola ritim) · **bedel** (alçak, tek çekilen gamba yayı; BEDEL imzası) ·
**miras** (iki aynı + düşen üçlü; c0'da düşen, c16'da `invert=True` TERS çevrilmiş yankı) · **lorenzo** (c6, 4 ölçülük yay) · **duomo** (c4 kubbe, yükselen–inen yay) · **donus** (1434; c10'da `donus_ters` geri sarılmış) · **yildiz** (c14 Jüpiter'in dört uydusu).
Çıpa gösterimi: `cNsK` cümle başı · `cNsK·sözcük±dt` sözcük çıpası · `·son` cümle sonu · `♪` tema girişi · `dur` kuru duraklama (stop) · `⌀[SESSİZ|−N dB]` müzik kapısı (sessizliğe giriş 0,6 sn önce).
**ÇAN KURALI:** c7 (26 Nisan) ve c10 (9 Kasım) cue'larında `bell` katmanı/olayı YOK; SFX'te de çan/gong olay sesi yasak (`sfx.POLICY_FORBID`: c7, c10, c13); bu bölümlerin bölüm kartı vurgusunda gong da kapatılır.

| Bölüm | Parça | Perde | Kesit: ruh hali · mod · tempo · ölçü · tonik | Ana fikir | Çıpalar (tema / olay / kapı) |
|---|---|---|---|---|---|
| c0 | P1 | ALTIN | solemn · dorian · 58 bpm · 4/4 · D2 | 1743 ölüm odası; sakin, ağırbaşlı. 'miras' hücresi (düşen üçlü) lavtada; c0 sonunda TEK vuruş + altın D majör + florin figürü (ana başlık). | ♪miras@c0s1; ♪miras@c0s6; ♪miras@c0s11; dur@c0s9·son-0.35 |
| c1 | P1 | ALTIN | curious · mixolydian · 72 bpm · 6/8 · G2 | florin şehri, 6/8 hafif dans, florin motifi; veba: renk solar (yalnız gamba); Ciompi: davul yükselir, 'ezildi'de ani sessizlik; tezgâh: florin geri döner. | ♪florin_uzun@c1s2·florin; ♪florin@c1s29·florindi-0.1; ♪florin_uzun@c1s30·masa; ♪bedel@c1s11; timp@c1s18; organ@c1s30; dur@c1s21·son-0.2; ⌀[-30 dB] c1s22·son-0.5→c1s23·son |
| c2 | P1 | ALTIN | dry · mixolydian · 70 bpm · 4/4 · A2 | defter: kuru, ironik 'tık-tık' arpej (klavsen), bas ostinato, ölçülü kuru duraklar (mizah); Giovanni'nin ölümü ve son sözler: yumuşar. | dur@c2s8·son-0.1; dur@c2s19·son-0.2; dur@c2s33·son-0.1; lute@c2s35·kule |
| c3 | P2 | ALTIN | tense · aeolian · 66 bpm · 4/4 · E2 | kule/sürgün: gerilim → sessiz güç; hücre: seyrek damla; torbalar: sinsi ostinato; 1434 dönüşü: 'dönüş' motifi (org+lavta). | ♪bedel@c3s9; ♪donus@c3s17·döndü-0.2; ♪donus@c3s17·döndü-0.2; dur@c3s3·son-0.1; dur@c3s10·son-0.1; dur@c3s32·son-0.1; organ@c3s33 |
| c4 | P2 | ALTIN | warm · mixolydian · 64 bpm · 4/4 · G2 | kubbe: sıcak; kubbe katman katman yükselir (duomo motifi); kutsamada koro+org koral; kefaret/yatırım sorusu açık kalır. | ♪duomo@c4s4·tasarımı; ♪duomo@c4s9; ♪duomo@c4s9; organ@c4s10; choir@c4s10; dur@c4s20·son-0.1; dur@c4s23·son-0.1; ⌀[-18 dB] c4s32→c4s32·son |
| c5 | P2 | ALTIN | warm · mixolydian · 63 bpm · 3/4 · D2 | konsil, kitap, Platon: 3/4 sarabande; Doğu heyeti alayı (davul); 1453 sessizlik; Orfik lir (lavta kadansı); Lorenzo'ya geçiş. | ♪nota@c5s11·lir+0.1; ♪nota@c5s21; timp@c5s4·düştü; gamba@c5s4·düştü; dur@c5s11·son-0.1; ⌀[-20 dB] c5s4·düştü→c5s4·son+0.6 |
| c6 | P3 | ALTIN | warm · ionian · 72 bpm · 4/4 · D2<br>grave · dorian · 54 bpm · 4/4 · D2 | Lorenzo: sıcak-hafif; Lorenzo teması (4 ölçü, yay biçimi); giostra: davul + hızlı arpej. Kesit 2: gölge (D dorian) + 'bedel' yayı → c7'ye köprü. | ♪lorenzo@c6s1; ♪lorenzo@c6s9; ♪lorenzo@c6s17·Muhteşem-0.3; ♪lorenzo@c6s17·Muhteşem-0.3; ♪lorenzo@c6s20·turnuva-0.2; ♪lorenzo@c6s25; dur@c6s19·son-0.1; ♪lorenzo@c6s26; ♪bedel@c6s27·ölecekti-1 |
| c7 | P3 | BEDEL | heavy · dorian · 56 bpm · 4/4 · D2<br>heavy · phrygian · 56 bpm · 4/4 · D2 | 26 Nisan 1478: AĞIR, mizah kapalı; kilise girişinde müzik yok (ayin yankısı + uğultu = SFX); V5–V7 YILDIZ AN: müzik ÇEKİLİR (0,6 sn önce), tam sessizlik; sonra D frigiyen. ÇAN YOK. | ♪bedel@c7s1; ⌀[SESSİZ] c7s2+1→c7s3·son-2; ⌀[SESSİZ] c7s15→c7s23·son; ♪bedel@c7s25; ♪nota@c7s38; ♪nota@c7s39; ♪bedel@c7s46·son; timp@c7s27·kapana; seq@c7s30·palle; seq@c7s30·palle+2.4; organ@c7s31·alkışlandı; gamba@c7s40 |
| c8 | P4 | BEDEL | serious · dorian · 66 bpm · 6/8 · A2 | Aslanın İni: ciddi, diplomatik, 6/8 deniz; 'Konuk muydu, rehine mi?' ve 'O sırada Lorenzo Napoli'deydi'de müzik çekilir; sonda şube ışıkları sönüyor. | dur@c8s9·son-0.1; dur@c8s31·son-0.1; lute@c8s34·Londra; lute@c8s34·Londra+1.5; lute@c8s34·Londra+3.2; lute@c8s34·Londra+5.2; lute@c8s34·Londra+7.6; ⌀[-24 dB] c8s11→c8s11·son-0.4; ⌀[SESSİZ] c8s19-0.1→c8s19·son |
| c9 | P4 | BEDEL | dry · aeolian · 60 bpm · 4/4 · G2 | defter kapanıyor: kuru-hüzünlü tık-tık; şubeler tek tek kapanır (inen lavta notaları); 'güzellik kaldı'da sıcak akor; sonda tehdit. | dur@c9s9·son-0.1; dur@c9s19·son-0.1; dur@c9s20·son-0.5; lute@c9s10·son-0.8; lute@c9s13·son-0.8; lute@c9s14·Milano; lute@c9s14·Avignon; lute@c9s14·Brugge; lute@c9s14·Venedik; organ@c9s27·güzellik-0.2; choir@c9s27·güzellik; organ@c9s28 |
| c10 | P5 | BEDEL | heavy · phrygian · 58 bpm · 4/4 · E2 | Rahip ve Kral: AĞIR, E frigiyen; 9 Kasım (c10s13–c10s20): KISA VURUŞLAR, yatak yok, 1 sn sessizlik, uzak trompet (SFX); ateş: lapis → közer; 'dönüş' motifi geri sarılmış. ÇAN YOK. | ♪donus_ters@c10s20·Şimdi-0.1; ♪donus_ters@c10s20·Şimdi-0.1; ♪bedel@c10s34; ♪florin3@c10s36·ordunun; timp@c10s13; dum@c10s14·Palazzo; tek@c10s14·girmek; seq@c10s15·kapandı-0.05; tek@c10s16·saat; tek@c10s16·saat+0.42; dum@c10s18·özgürlük-0.5; dum@c10s18·özgürlük; dur@c10s22·yırttı; dur@c10s28·son-0.1 … |
| c11 | P5 | BEDEL | heavy · phrygian · 54 bpm · 4/4 · D2<br>epic · mixolydian · 80 bpm · 4/4 · D2<br>heavy · aeolian · 52 bpm · 4/4 · D2 | Papa Oğulları: [Prato ağır] → [Leo X alayı görkemli-ironik, mizah V2–V3] → [Roma 1527–1537 ağır, kısa olay → sessizlik]; P5 sonu çözülmeyen sus4 ('p2'). | timp@c11s1; dur@c11s6·son-0.1; dur@c11s10·son-0.1; dur@c11s12·son-0.1; dum@c11s17·yüz; dum@c11s17·yedisi; dum@c11s18·kırk; timp@c11s28·kurşun; lute@c11s31·çıktı; lute@c11s33·vaat; gamba@c11s33·uyuyakalmıştı; dum@c11s34·döndü; dum@c11s34·öldürdüler; ⌀[SESSİZ] c11s34·son-1→c11s35·son-0.6 |
| c12 | P6 | MİRAS | cold · aeolian · 66 bpm · 4/4 · A2 | Dük: soğukkanlı-otoriter, makine gibi tık-tık + org pedalı; 1562 AĞIR, 'dört haftada üç ölüm'de tam sessizlik; Lepanto saygılı-nötr (zafer fanfarı yok); P6 açılışı 'miras' hücresi. | ♪miras@c12s1; ♪miras@c12s28·güzelliği; dur@c12s7·son-0.1; dur@c12s13·son-0.1; dur@c12s31·son-0.1; ⌀[-30 dB] c12s19→c12s25·son; ⌀[SESSİZ] c12s22·haftada-0.2→c12s22·son+0.2 |
| c13 | P6 | MİRAS | duo · aeolian · 60 bpm · 4/4 · A2<br>duo · lydian · 72 bpm · 3/4 · C3 | İki Kraliçe: [Catherine A aeolian; 1572'de neredeyse sessizlik; mit endüstrisi kuru duraklar] → [Marie C lidyen 3/4, Rubens galerisi görkemli-ironik, Köln'de soğuk sessizlik]. ÇAN YOK. | ♪bedel@c13s7; ♪nota@c13s21·gerçek; dur@c13s17·son-0.1; dur@c13s20·son-0.1; dur@c13s19·yüzyıla; ⌀[SESSİZ] c13s7·son-2→c13s7·son; ⌀[-30 dB] c13s11→c13s14·son-3; ⌀[SESSİZ] c13s14·son-3→c13s14·son; dur@c13s26·son-0.1; dur@c13s32·son-0.2; harp@c13s38·gökyüzüne; harp@c13s38·yazdırıyordu; ⌀[-28 dB] c13s35→c13s37·son |
| c14 | P7 | MİRAS | bright · lydian · 66 bpm · 3/4 · F2<br>bright · dorian · 54 bpm · 4/4 · D2<br>bright · lydian · 60 bpm · 3/4 · F2 | Yıldızlar, Notalar, Taşlar: [matbaa/sert taş F lidyen] → [Euridice: ÖZGÜN recitativo-tarzı süreklilik (klavsen+lavta+gamba) D dorian] → [Galileo'nun dört yıldızı, 1633 AĞIR süssüz, Cristofori envanteri, azalan satırlar]. | dur@c14s4·son-0.1; dur@c14s10·son-0.1; ♪yildiz@c14s12·üç-0.2; ♪nota@c14s12·dörde; ♪bedel@c14s18; organ@c14s14·yıldızları-0.3; dur@c14s17·son-0.1; dur@c14s24·son-0.1; ⌀[-16 dB] c14s18→c14s19·son; ⌀[-14 dB] c14s26·son-2.5→c14s26·son |
| c15 | P7 | MİRAS | weary · aeolian · 54 bpm · 4/4 · A2 | Son Medici'ler: yorgun, seyrek; üç katmanlı ölçek (2006 → 2010 → 2026) yükselen üç nota; aile ağacı: inen notalar; 'bir kadın ve imzalanacak bir sözleşme' → miras hücresi. | ♪bedel@c15s2·son; ♪bedel@c15s17·öldü; ♪miras@c15s19·kadın-0.3; lute@c15s4·2006; lute@c15s4·2010; harp@c15s5·2026; dur@c15s1·son-0.1; dur@c15s6·son-0.1; dur@c15s14·son-0.1; lute@c15s17·kendi; lute@c15s18·Viyana |
| c16 | P7 | MİRAS | solemn · dorian · 58 bpm · 4/4 · D2<br>dry · mixolydian · 72 bpm · 4/4 · D2<br>solemn · dorian · 54 bpm · 4/4 · D2 | Hesap: [c0'ın odasına dönüş: D dorian, 'miras' hücresi TERS ÇEVRİLMİŞ] → [kuşkucu orta: hafif kuru] → [sessiz kapanış, çözülüş (Picardy), son lavta notası, son sessizlik]. | ♪miras@c16s1; ♪miras@c16s5·çıkmayacak-0.6; ♪miras@c16s5·çıkmayacak-0.6; dur@c16s7·son-0.1; dur@c16s14·son-0.1; dur@c16s16·son-0.1; dur@c16s17·son-0.1; ♪miras@c16s23; ♪miras@c16s25·şehir-2.2 |


Öne çıkan sahneler: **c7 V5–V7 yıldız an** (c7s15→c7s23): müzik ÇEKİLİR (kapı `lead=0,6 sn`, `rel=4 sn`), tam sessizlik; mod değişimi (D dorian → frigiyen) sessizliğin İÇİNDE; V8'de yavaşça döner.
**c10 9 Kasım** (c10s13–c10s20): kısa vuruşlar, yatak yok, "kapandı"da 1 sn sessizlik (uzak trompet = SFX). **c11** üç kesit (Prato · Leo X alayı · Roma 1527–1537 ağır; "kısa olay → sessizlik").
**c14 Euridice**: `recit` katmanı = özgün recitativo-tarzı süreklilik (klavsen + lavta + gamba; D dorian; telifli melodi yok). **c15** yorgun/seyrek; üç yükselen nota 2006→2010→2026.

---
## 3. SFX kataloğu (`python3 sfx.py --katalog`)

65 efekt, hepsi fiziksel-modelleme tarzı sentez (filtreli gürültü + gövde modları + zarflar), `sfx(name, seed, dur, loop)` → float32 (n,2) 48 kHz, tepe −3 dBFS, deterministik. Döngü sesleri 8 sn **dikişsiz**.

- **kâğıt/yazı**: `page_turn` (sayfa çevirme), `paper_rustle` (kâğıt hışırtısı), `quill_scratch` (kalem/tüy çiziği), `wax_seal_stamp` (mühür), `stamp_thud` (damga çarpması), `letter_open` (mektup açılışı), `book_close` (defter kapanışı), `type_set` (harf dizimi (matbaa)), `press_thud` (baskı presi), `pin_stick` (harita iğnesi), `brush_stroke` (fırça darbesi)
- **para**: `coin_clink` (sikke şıngırtısı), `coin_pile` (sikke yığını), `coin_roll` (sikke yuvarlanır)
- **kapı/metal**: `door_bolt` (kapı sürgüsü), `door_bronze` (tunç kapı çarpması), `lock_click` (kilit/anahtar), `gate_thud` (ağır kapı çarpması (ahşap+zincir)), `knock_wood` (tahta vuruş), `knock_metal` (metal tık), `keyboard_action` (klavye mekanizması (klavsen/piyano)), `glass_chime` (lens/cam tınısı), `chisel_tap` (sert taş oyma)
- **kalabalık/mekân**: `crowd_murmur` (kalabalık uğultusu (sözsüz)), `crowd_chant` (ritmik kalabalık haykırışı (sözsüz)), `applause_far` (uzak alkış), `church_ambience` (kilise içi oda tonu), `footsteps` (adımlar (taş/ahşap)), `horse_hooves` (nal sesi (dörtnala/yürüyüş)), `hoof_far` (uzaklaşan tek at), `distant_trumpet` (uzak trompet)
- **doğa**: `fire_crackle` (ateş çıtırtısı), `candle_flame` (mum alevi (döngü)), `candle_snuff` (mum sönmesi), `sea_waves` (deniz dalgaları), `water_lap` (liman suyu (döngü)), `ship_creak` (gemi ahşap gıcırtısı), `rope_creak` (halat gerilimi), `wind` (rüzgâr), `rain` (yağmur), `thunder` (gök gürültüsü)
- **çan/gong/vuruş**: `church_bell` (kilise çanı (YALNIZ kaynaklı olay)), `bell_toll_low` (alçak çan (YALNIZ kaynaklı olay)), `gong_hit` (gong), `title_hit` (ana başlık vuruşu), `chapter_stinger` (bölüm kartı vurgusu (flavor=altin|bedel|miras)), `drum_hit` (çerçeve davulu vuruşu), `heartbeat` (kalp atışı), `tick` (kuru tık), `cannon_boom` (top (uzak, YALNIZ kuşatma)), `sword_clash` (kılıç (kullanma: şiddet gösterilmez)), `magic_chime` (büyülü çınlama (Şarlken'den; Medici'de kullanılmaz))
- **geçiş**: `whoosh` (whoosh (soldan sağa)), `whoosh_long` (uzun whoosh), `whoosh_dir` (yönlü whoosh (whip/wipe)), `wash_swell` (pigment yıkama), `plaster_scrape` (fresko sıva), `dip_drop` (siyaha iniş), `light_swell` (ışık huzmesi), `zoom_rush` (zum hücumu), `zoom_rush_long` (uzun zum-geçiş), `cloth_sweep` (şerit süpürüşü), `slide_glide` (kayma), `iris_ring` (iris (obj=florin|palle|sun|moon|dome|lens|seal)), `candle_out_in` (mum söner-yanar (candle))


**Kaynak politikası** (kod uygular, `resolve_cues` cue'yu atlar ve uyarır): c7/c10/c13'te `church_bell`, `bell_toll_low`, `gong_hit` YOK (gerçekten kaynaklıysa cue'ya `"kaynakli": true`) ·
`sword_clash`, `magic_chime` hiç kullanılmaz · kalabalık/uğultu **SÖZSÜZ** · şiddet/kan sesi yok · müzik sessizlik kapısında başlayan cue için bilgi uyarısı (kapı/kilit/sürgü hariç; bilinçliyse `"sessizlik_izni": true`).

---
## 4. Geçiş türü → ses eşlemesi (otomatik)

`compose.Program` geçişleri (`tr_eff`) → `sfx.transition_cues()` → `out_pN/sfx_gecis.json` (`miks_kur.py --gecis-sesleri`). Ses, geçişin **ortasında tepe yapacak** şekilde yerleştirilir
(`place="before"`: gelen çekimden önce biter; `place="after"`: gelen çekimin ilk d sn'si). Ağır bölümlerde kısılır (`TRANSITION_CH_TRIM`: c7 −5, c10 −4, c11 −4, c15 −3, c9/c12/c16 −2 dB);
müzik sessizlik kapılarında (c7 yıldız an vb.) HİÇ çalmaz; `link="audio"` (ses köprüsü) işaretli geçişte otomatik ses atlanır (sesi sahne yazarı cue olarak yazar); bölüm kartı/ana başlık/bitiş ekranı geçişleri atlanır (kendi ses tasarımı: `chapter_stinger`/`title_hit`).

| Motor geçişi | Ses (sfx adı) | Süre | Tepe | Seviye (dB) | Not |
|---|---|---|---|---|---|
| `fade` | — | — | — | — | ses yok (karışım zaten yumuşak) |
| `yikama` | `wash_swell` | geçiş süresi | 0.45 | -23 | bölüm kartı/ana başlık girişi dahil (kartlarda ayrıca stinger) |
| `sayfa` | `page_turn` | 1.1 | 0.35 | -20 | sayfa çevirme |
| `giornata` | `plaster_scrape` | geçiş süresi | 0.5 | -23 |  |
| `dip` | `dip_drop` | 2.6 | 0.12 | -20 | siyaha iniş; kısa 'vuruş' |
| `zoom` | `zoom_rush` | 0.9 | 0.8 | -24 |  |
| `whip` | `whoosh_dir` | 0.7 | 0.45 | -20 | dir=l/r |
| `wipe` | `whoosh_dir` | 0.9 | 0.5 | -24 | yumuşak whoosh |
| `iris` | `iris_ring` | 1.2 | 0.35 | -21 | obj=florin/palle/sun/moon/dome/lens/seal çekim opts'undan |
| `slide` | `slide_glide` | geçiş süresi | 0.5 | -24 |  |
| `zoomthru` | `zoom_rush_long` | 1.5 | 0.8 | -22 |  |
| `carry` | `cloth_sweep` | geçiş süresi | 0.5 | -23 |  |
| `light` | `light_swell` | 2.6 | 0.35 | -22 | ışık huzmesi |
| `candle` | `candle_out_in` | 3.0 | 0.15 | -21 | mum söner-yanar; kamera devri yok |


`python3 sfx.py --gecis-ornegi` tüm geçiş türleri için yerleşim örneği basar. `fade` seslendirilmez (karışım zaten yumuşak).

### Ses köprüsü / J-kesme / L-kesme kancaları
- **J-kesme** (sesi görüntüden önce başlat): cue'da `"erken": 0.4` (ör. kalabalık uğultusu görüntüden 0,4 sn ÖNCE girer) ya da `sfx.j_cut(ad, t_görüntü, lead=0.4)`.
- **L-kesme** (eski sesi kesmeden sürdür): `sfx.l_cut(ad, t_kesim, tail=0.6, dur=…)`; ya da döngü cue'ya `"bitis_capa": ["cNsK","end",+0.6]` + `"cik"`.
- **Ses köprüsü** (iki çekim arası): `sfx.ses_koprusu(ad_giden, ad_gelen, t_kesim, tail=0.5, lead=0.4)` → iki cue döner. Sözleşmede: giden cue `bitis_capa` ile kesimden sonra sürer, gelen cue `erken` ile kesimden önce girer.
- Örnekler: `sfx_cues_p3.json` → `c7-ayin-yankisi-1/2` (kilise girişi, J-kesme `erken: 0.4`), `c7-tunc-kapi` (kuyruğu sessizliğe uzanır, `sessizlik_izni`); `sfx_cues_p4.json` → `c8-kasa-kapagi` (kasa kapağı V3'e taşar); `sfx_cues_p5.json` → `c10-meydan` (uğultu V4 sonunda keskin kesilir) + `c10-kapi` (bölümün en sert sesi, ÇAN YOK) + `c10-tek-nal` (ardından 1 sn sessizlik).

---
## 5. `sfx_cues_pN.json` sözleşmesi (N = 1..7; proje kökünde; `script.PARTS`'a göre bölünmüştür)

UTF-8 JSON; kökte nesne (`{"surum":1,"parca":N,"bolumler":[…],"ayar":{…},"cues":[…]}`) ya da doğrudan liste. **Zaman çapaları cümle kimliğine bağlıdır** (ses yamalanınca yeniden çözülür); mutlak `t` yalnız denemede.

```json
{ "id": "c7-ayin-yankisi-1", "bolum": "c7", "ad": "church_ambience",
  "capa": ["c7s2", "Santa", 0.0],  "bitis_capa": ["c7s3", "end", 0.0],  "erken": 0.4,
  "seviye": -27, "pan": 0.0, "tohum": 3, "dongu": true, "gir": 0.8, "cik": 1.8, "bastir_db": -3,
  "parametre": {}, "sessizlik_izni": false, "kapali": false, "not": "J-kesme: ayin yankısı görüntüden 0,4 sn önce", "kaynak": "scenes_c7.py V1" }
```

| Alan (TR / EN eşdeğeri) | Anlam |
|---|---|
| `t` **veya** `capa` (anchor) | başlangıç: parça ses ekseninde sn, YA DA çapa: `["c7s17"]` · `["c7s17", 0.3]` (cümle başı + dt) · `["c7s17","sözcük",-0.1]` (sözcük başı + dt) · `["c7s17","end",0]` (cümle sonu + dt) |
| `erken` (lead) | sesi çapadan X sn ÖNCE başlat (J-kesme / ses köprüsü), varsayılan 0 |
| `ad` (name) | `sfx.py` adı (`python3 sfx.py --list`) — bilinmeyen ad cue'yu atlatır ve uyarır |
| `seviye` (gain_db) | dB; tepe −3 dBFS'e göre. Ambiyans −24…−30, olay −14…−22 (varsayılan −20) |
| `sure` (dur) / `dongu` (loop) / `bitis_capa` (end_anchor) | uzunluk (sn \| null=doğal); döngü sesi dikişsiz tekrar; `bitis_capa` süre yerine bitiş çapası |
| `gir` / `cik` (fade_in/out) | yumuşatma (sn); döngülerde varsayılan 1,2 |
| `bastir_db` (duck_db) | konuşma altında kısma (döngüde varsayılan −4, tekil seste 0) |
| `parametre` (params) | `{"root": Hz, "obj": "florin", "dir": "r", "flavor": "bedel", "kind": "stone", "n_steps": 8…}` |
| `pan` · `tohum` (seed) · `bolum` (ch) | −1…1 · tekrarlanabilirlik · yalnız kaynak-politikası denetimi için ipucu |
| `kapali` (off) · `sessizlik_izni` · `kaynakli` · `not` · `kaynak` | silmeden devre dışı · kapı içinde başlamaya izin · çan politikası istisnası (kaynak göster) · serbest metin |

`ayar`: `{"varsayilan_stinger": true, "gecis_sesleri": true}` — varsayılan bölüm kartı vurguları ve `sfx_gecis.json` kullanımı. Çapa çözülemeyen cue **atlanır ve uyarılır** (bölümü bu parçada olmayan cue sessizce atlanır).
Mevcut kuyruk: 7 dosyada 143 cue (37 farklı ses; parça başına ≈20) (anlatı + yönetmen brifinden ilk doldurma); sahne yazarları `sfx=` ipucuyla ya da doğrudan bu dosyalara ekler.

---
## 6. STIL_REHBERI §8 taslağı

> **Ana ajan için: aşağıyı `STIL_REHBERI.md` §8'e (Ses–görüntü kilidi) taşıyın.**

```
- Ses hattı geçişlerden OTOMATİK ses türetir (yikama→pigment yıkama, sayfa→sayfa çevirme, giornata→fresko sıva, dip→siyaha iniş, whip/wipe→whoosh, iris→halka (obj'a göre),
  slide/carry→kayma/şerit, zoom/zoomthru→hücum, light→ışık huzmesi, candle→mum söner-yanar, fade→sessiz). Bölüm kartı/ana başlık/bitiş ekranı hariç (kendi vurguları var). Müzik çekilen yıldız anlarda çalmaz.
- Otomatik sesi İSTEMİYORSAN geçişe `link="audio"` (ses köprüsü) yaz; o geçişin sesini kendin cue olarak verirsin (aşağıdaki sfx= ya da sfx_cues_pN.json).
- Çekime ipucu: shot(..., sfx=[("coin_clink", 1.2), ("page_turn", ["c2s5","sikke",0.0], -22), {"ad":"church_ambience","t":0,"erken":0.4,"dongu":True,"sure":8,"seviye":-27}]).
  Öğe = (ad, dt_sn | çapa [, seviye_dB]) ya da sözlük (anahtarlar sfx_cues_pN.json ile AYNI). dt, çekimin GÖRÜNÜR başlangıcından (Shot.t0) sn'dir; Shot.origin değil.
- Tercihen ÇAPA ver (["c7s17","sözcük",-0.1]); mutlak sn verme: gerçek ses gelince zamanlar kayar, çapa kendini yeniden çözer. Çekim içi uzun ambiyans için dongu+sure (ya da bitis_capa) kullan.
- Ses köprüsü / J-kesme: gelen sesi `erken` (sn) ile görüntüden ÖNCE başlat (kalabalık uğultusu 0,4 sn önce); giden sesi `bitis_capa`+`cik` ile kesimden sonra sürdür. Bu yerleri `yonetmen_cK.md` "Ses köprüleri" satırına da yaz.
- KAYNAK POLİTİKASI: c7, c10, c13'te çan/gong OLAY sesi yok (kaynakta yok; sahnede çan/saat/sarkaç da çizme); kalabalık/uğultu SÖZSÜZ; hançer/kılıç/kan sesi yok. Katalog: `python3 sfx.py --katalog` (65 ses).
- Müzik sessizlikleri (kapılar) cümle çapalarıyla `muzik.py` CUES'tadır (c7 V5–V7, c8 "Konuk muydu…", c10 9 Kasım, c12 1562, c13 1572…): bu aralıkta görüntüde ani vuruş/ses olayı planlama; gerekirse `sessizlik_izni`.
- Ses yazarlığı bölüm-bazlı perde rengi taşır (ALTIN c0–c6 · BEDEL c7–c11 · MİRAS c12–c16) ve parçadan bağımsızdır; parça başlığı bindirmesi (P2…P7, 1,2–4,8 sn) sırasında müzik doğrudan çalar.
- Kontrol: `MEDICI_PART=N python3 miks_kur.py --kontrol` (girdiler) · `--gecis-sesleri` (otomatik geçiş sesleri) · `--onizleme --preview` (ses_onizleme/*.mp3). Sözleşmenin tamamı: notlar_ses.md.
```

---
## 7. Miks zinciri ve hedefler

- **voice**: 80 Hz HPF → sıkıştırıcı (2:1, −24 dBFS, 10/120 ms) → +1,5 dB @3 kHz → 7 kHz üstü yüksek raf −2,5 dB + dinamik de-ess (5,2–9,8 kHz) → ham ses düzeyine makyaj kazancı → **konuşma-yalnız tepe sınırlayıcı** (tavan −6,8 dBTP, 5 ms ileri bakış / 80 ms bırakma; RMS geri eşitlenir). Gerekçe: konuşma crest'i ≈14 dB; −14 LUFS'ta tepeler tavanı aşar ve master limiter her hecede müzik yatağını da kısıp "nefes aldırır" (denemede master limiter maks. 7–9 dB, %7,6 süre >1 dB); tepeyi yalnız konuşmada ezince master limiter ≤1 dB'ye iner (>1 dB %0).
- **müzik**: `muzik.render_music` (ham, ort. −27,5 dBFS RMS) → 300 Hz–3 kHz arası ≈ −3 dB çukur → **konuşmaya duyarlı ducking**: konuşma−müzik farkı kapalı döngüyle **[20, 24] dB** aralığına çekilir
  (`snr_bias` ile bölüm yanlılığı: c7 +0,5, c15 +1,0 …); konuşma aralarında (bölüm kartı, parça başı/sonu) +9 dB "yükseliş"; sustuğu (kapı) pencereler seviyelemeye katılmaz → sessizlik gerçekten sessiz.
- **kavşak düzeltmesi**: kesit sonu ↔ sonraki kesit başı ortanca düzeyleri (kapılar hariç, 6 sn) >1 dB ayrışıyorsa uçlar birbirine çekilir (her uca ≤ ±3 dB, 10 sn yumuşak rampa); kavşak yatağı (`junction_pads`) kenarın YEREL gücüne göre ayarlanır; "kısık" kapılar en çok ~3,5 dB/sn ile geri açılır.
- **sfx**: kuyruk (`sfx_cues_pN.json` + `sfx_gecis.json` + varsayılan kart vurguları) → SFX bus; konuşma altında döngülerde −4 dB.
- **master**: true-peak duyarlı ileri bakışlı yumuşak limiter (tavan −1,8 dBTP; 8 ms ileri bakış / 120 ms bırakma) + **−14 LUFS** (BS.1770 kapılı) yinelemeli kalibrasyon; AAC 192k sonrası true-peak yeniden doğrulanır (≤ −1,0; gerekirse tavan düşürülür).
- **Bağımsız ölçüm**: kendi BS.1770 ölçümüm + ffmpeg `loudnorm` + `pyloudnorm`; true-peak 4× aşırı örnekleme + ffmpeg; kırpılma sayımı; DC ofset; Welch spektral denge; 8 sn pencerelerde konuşma−müzik; bölüm başına LUFS; geçiş sıçramaları; sessizlik bölgeleri; `timeline.json` ↔ `voice.wav` uyumu.

---
## 8. Ölçüm sonuçları

| Parça | Bölümler | Ses | Mix süresi | LUFS (BS.1770 / pyln) | TP wav / m4a (dBTP) | Konuşma−müzik ort. · p5 · en kötü 8 sn (dB) | Duck ort. (dB) | Limiter maks. / >1 dB | Bölüm geçişi 12 sn LUFS · 3 sn basamak (dB) | Kontrol |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | c0–c2 | ElevenLabs (gerçek) | 598 sn | -14.00 / -14.04 | -1.80 / -1.52 | 21.7 · 20.0 · 19.4 | -13.5 | 0.9 dB / %0.0 | 0.84 · 3.6 | 17 geçti / 0 kaldı |
| P2 | c3–c5 | ElevenLabs (gerçek) | 642 sn | -14.00 / -14.04 | -1.80 / -1.41 | 21.5 · 20.0 · 19.4 | -13.9 | 0.8 dB / %0.0 | 1.12 · 3.8 | 16 geçti / 1 kaldı |
| P3 | c6–c7 | — | (miks henüz alınmadı) | | | | | | | |
| P4 | c8–c9 | — | (miks henüz alınmadı) | | | | | | | |
| P5 | c10–c11 | — | (miks henüz alınmadı) | | | | | | | |
| P6 | c12–c13 | — | (miks henüz alınmadı) | | | | | | | |
| P7 | c14–c16 | — | (miks henüz alınmadı) | | | | | | | |

- **P1** sessizlik kapıları (müzik ≤ −80 dBFS beklenir): —
- **P2** sessizlik kapıları (müzik ≤ −80 dBFS beklenir): —; KALAN: ['timeline.json uyumu (cümle içi konuşma ≥ 0,70; cümle arası ≤ 0,10; bölüm sınırı ≤ 0,6 sn)  → 0.835 / 0.145']

Kontrol listesi (her `audio_report.txt` [10]): −14 ± 0,5 LUFS · pyloudnorm bağımsız ±0,6 · TP wav ve m4a ≤ −1,0 dBTP · kırpılma 0 · DC < 1e-3 · konuşma−müzik ≥ 19 dB (en kötü 8 sn ≥ 18,5; pencerelerin %80'i [19, 26]) ·
müzik nominal −24…−28 dBFS · süre = voice + 7 sn · boşluk yükselişi 8–10 dB · 12 sn LUFS sıçraması ≤ 1,5 dB · kavşakta 3 sn pencere basamağı ≤ 4 dB · her sessizlik kapısında müzik ≤ −80 dBFS · timeline uyumu.
Ayrıntı: `out_pN/[ONIZLEME_]audio_report.txt`.

---
## 9. Bilinen sınırlar

1. **Kulak yok:** tüm kalite güvencesi nesneldir (LUFS/TP/duck/denge/kavşak/sessizlik ölçümleri + tık dedektörü); müziğin ve efektlerin ESTETİĞİ dinlenip onaylanmadı — `out_pN/ses_onizleme/*.mp3` kesitleri bunun için (kullanıcı dinleyecek). Üretken müzik tohumlu; beğenilmeyen kesit için `muzik.py` CUES'ta o bölümün spec'i (yoğunluk eğrisi, çalgı, mod) ya da `--seed` değiştirilir, yalnız o kesit yeniden üretilir.
2. **P3–P7 geçici (Piper) sesle ölçüldü / ölçülecek** (`ONIZLEME_` önekli; final adıyla yazılmaz). Gerçek ses gelince konuşma temposu ve duraklar değişir: çıpalar kendini yeniden çözer, ama ducking/seviyeleme/kavşak ölçümleri tek komutla yeniden alınmalıdır. c6–c16 metinleri düzeltilirken cümle numaralandırması kayarsa `MEDICI_PART=N python3 miks_kur.py --kontrol` çözülemeyen/kaymış çapaları listeler (cue'lar `cNsK` kimliğine bağlıdır; sözcük çapası bulunamazsa cümle başına düşer).
3. **Zaman çizelgesi doğruluğu müzik/SFX çıpalarının doğruluğudur.** P2'de (`out_p2/timeline.json`, ASR hizalayıcı) c5s11–c5s21 (≈558–635 sn) bölgesi sorunlu: ses bu aralıkta durak bırakmadan akıyor (569,7–635,4 sn tek koşu), zaman çizelgesi ise cümleler arasına 0,55–0,95 sn boşluk varsayıyor → cümle zamanları birkaç sn kayabilir (kontrol listesinde "timeline uyumu" KALDI: cümle arası konuşma payı 0,145 > 0,10). Etkisi: c5'in son çıpalı olayları (yoğunluk eğrisi, c5s21 harp teması) ve SFX çıpaları birkaç sn erken/geç olabilir; mix seviyeleri etkilenmez. Hizalayıcı düzelince miks yeniden alınır.
4. **Otomatik geçiş sesleri henüz üretilmedi:** `compose.Program` çekim listesi (`scenes_cK.py`) tamamlanınca `miks_kur.py --gecis-sesleri` çalıştırılmalı; şu an `sfx_gecis.json` boş (yalnız `sfx_cues_pN.json` + bölüm kartı vurguları çalıyor). `sfx=` çekim ipucu motorda henüz yok (bkz. istekler).
5. **Limiter/tepe:** konuşma crest'i ≈14 dB olduğundan −14 LUFS'ta konuşma tepeleri sınırlanır; bu iş konuşma-yalnız sınırlayıcıdadır (%3–5 süre >1 dB, nadir tepeler 7–9 dB) ve master limiter ≤1 dB'dir. Çok dinamik/fısıltılı yeni sesler gelirse `VOICE_PEAK_DB` (miks.py) ayarlanır.
6. **Bölüm sınırı konuşma seviyesi eşlemesi** (≤ ±1,5 dB, 12 sn sabit + 6 sn rampa) doğal ifade farkını hafifçe düzleştirir; kapatmak için `voice_edge_match(..., tol=99)` yeterli.
7. **Kavşak ölçümü** bilinçli kapıları/kuru duraklarla çakışan pencereleri atar (tasarım gereği büyük düzey değişimi); geri kalan kavşak basamağı ≤ 4 dB (3 sn pencere) aranır. 1 sn adım yalnız bilgi amaçlıdır.
8. **Önbellek/bellek:** `out_pN/_audio_cache` (≈110 MB/parça, git'te yok), stem FLAC'ler ve `.m4a` git'te yok (`.gitignore`); `ses_onizleme/*.mp3` ve `audio_report.txt` git'e GİRER (parça başına ≈6–7 MB mp3). Bir parça miksi ≈2,4 GB tepe bellek, tek işçi, ≈3–4 dk.
9. SFX kuyruğu ilk doldurmadır (143 cue); sahne yazarlarının `sfx=` ipuçlarıyla zenginleşmesi beklenir. Kalabalık/uğultu SÖZSÜZ ve şiddetsizdir; `cannon_boom` yalnız c11 kuşatma anında (uzak, boğuk).
10. Gong/çan: BEDEL perdesinde müzikal tını olarak (kart vurgusu, finaller) serbest; c7/c10/c13 kart ve cue'larında hiç yok. Olay çanı hiçbir yerde yok (Capponi'nin "çanlarla yanıt" sözü anlatıda söylenir, sesi çalınmaz).

---
## 10. Ana ajandan istekler

1. **STIL_REHBERI §8'i** bu dosyadaki "STIL_REHBERI §8 taslağı" ile değiştirin (ben dokunmadım).
2. **`shots.shot(..., sfx=[...])`** parametresini motor kabul etsin: `Shot.sfx` olarak saklasın ve tür fonksiyonlarına `**params` içinde geçirmesin (şu an `Shot.params["sfx"]`a düşer; `sfx.sfx_hints_from_program` ikisini de okur). Öğe biçimi taslakta.
3. **`compose.py`**: `PART_CHAPTERS`/`PART_FIRST` 3 parçalı (S.PARTS'tan türetilmeli) — `Program(part=4..7)` bugün `ValueError` verir; `miks_kur.py --gecis-sesleri` `Program(part=N)` ile geçişleri okur. Ayrıca `Program` `shot.link == "audio"` ve `tr_eff` alanlarını sağlıyor (kullanıyorum); bölüm kartı çekimlerinin `label`ı "bölüm kartı …" / "ana başlık" / "bitiş ekranı" ile BAŞLAMALI (ses hattı bunlara otomatik ses koymaz).
4. **Hizalayıcı**: `out_p2/timeline.json` c5s11–c5s21 bölgesi (≈558–635 sn): ses durak bırakmadan akıyor, çizelge 0,55–0,95 sn boşluk varsayıyor → cümle zamanları kayık; yeniden hizalama/düzeltme (`ses_hizala_asr.py`) gerek. Diğer parçalarda da `miks_kur.py` raporunun [9] "timeline uyumu" satırına bakılmalı (cümle arası konuşma payı ≤ 0,10).
5. **Metin düzeltmesi (c6–c16) sonrası**: cümle kimlikleri kayarsa (ekleme/silme) `MEDICI_PART=N python3 miks_kur.py --kontrol` ile `sfx_cues_pN.json` ve `muzik.py` CUES çıpalarını denetleyin; kayma varsa bana/müzik ajanına haber verin (çıpalar `cNsK` kimliğine bağlıdır).
6. **Gerçek ses geldiğinde sırayla**: `ses_birlestir.py` → hizalayıcı → `MEDICI_PART=N python3 miks_kur.py --kontrol` → `MEDICI_PART=N python3 miks_kur.py --preview` (final adıyla; `GECICI_SES.json` kalkmış olmalı). Final mux/render öncesi `parca.assert_gercek_ses()` zaten çağrılıyor.
7. **Görüntü tarafı ses kilidi için**: yıldız an / sessizlik kapıları `muzik.py` CUES'ta cümle çapalarıyla duruyor (c7 V5–V7 = c7s15→c7s23 …); bu aralıklarda ani görsel vuruş/çan sarkacı (c7/c10 `st_bell`) bulunmamalı. Bitiş kuyruğu 7 sn (`compose.OUTRO`); P1…P6 "SIRADAKİ PARÇA", P7 "TÜM FİLM" ile uyumlu.
8. `ses_onizleme/*.mp3` (≈6–7 MB/parça) ve `audio_report.txt` dosyalarını commit'e dahil edip etmemeye siz karar verin (m4a, FLAC stem, önbellek `.gitignore`'da).

---
## 11. Dosyalar

**Kod:** `muzik.py` (üretken müzik + 17 cue), `sfx.py` (65 efekt + geçiş eşlemesi + JSON sözleşmesi + J/L-kesme kancaları), `miks.py` (voice zinciri, ducking, SFX bus, master, QA raporu, önizlemeler), `miks_kur.py` (tek komut), `ses_dsp.py` (ortak DSP).
**Veri:** `sfx_cues_p1.json … sfx_cues_p7.json` (143 cue).
**Rapor:** `notlar_ses.md` (bu dosya).
**Çıktılar (parça başına, `out_pN/`):** `[ONIZLEME_]mix_audio.m4a`, `[ONIZLEME_]stem_music|voice|sfx.flac`, `[ONIZLEME_]sfx_cues_used.json`, `[ONIZLEME_]audio_report.txt`, `ses_onizleme/` (`[ONIZLEME_]NN_ad_mix.mp3` + `_muzik.mp3` + `OKU_BENI.txt`; P1'de ayrıca `00_sfx_katalog_demo.mp3`), `_audio_cache/`.
