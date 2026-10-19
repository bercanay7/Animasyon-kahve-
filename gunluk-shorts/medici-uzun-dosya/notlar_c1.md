# notlar_c1 — Florin Şehri (1252–1397 · 240 sn · gerçek ses)

Dosyalar: `scenes_c1.py` (39 çekim; 3 longtake), `c1_kinds.py` (özel türler), `p1_ortak.py`, `yonetmen_c1.md`.
Özel türler: `c1_cicek` (florin → zambak → kurt), `c1_darphane`, `c1_okul`, `c1_agi` (Peruzzi/Bardi şube ağı), `c1_edward`, `c1_kardes`, `c1_toprak` (toprak katman kesiti), `c1_yazi`, `c1_lonca`, `c1_machiavelli`, `c1_kademe`, `c1_kose`, `c1_sokak` (sehir/sokak sarmalayıcısı; `people=[…at=çapa]`, `door_at`).

## Kısıtlar (uygulananlar)
- **Ağır sahneler (veba 13–20, Ciompi'nin ezilişi 29–30): mizah KAPALI, şiddet gösterilmez.** Veba = renk solması (doygunluk + soğuk ton; "gece/şafak/çan" iddiası yok), boş sokak, kapanan kapı, boş oda, toprak katmanı kesiti; ceset/beden/kan çizilmez. Ciompi'nin bastırılması = kızıl pigment yıkama (kan değil) + loncaların milis alayı; hiçbir beden yok.
- Numerik kartlar akışın içinde (sayaçlar `count_up`, statik bekleme kartı yok): 3,5 GRAM · 2 CM · 90.000 KİŞİ · 15 ŞUBE · 12 YAŞINDA · 1.500 FLORİN · 10.000 FLORİN.
- Rakam okunurluğu: tüm sayaçların son değeri, çıkış geçişi başlamadan ≥0,4 sn önce oturur (90.000: 0,43; 12: 0,12 — kısa çekim; 1.500: 0,70).
- **Kaynak sınıfı damgaları:** VILLANI'YE GÖRE, BİR KAYNAĞA GÖRE, AKTARILANA GÖRE, AKTARILIR, YAZILDIĞINA GÖRE (○); KURGU (Machiavelli konuşması); KAYBEDENLERİN AİLESİNDEN (tarafsızlık notu).
- İsim/sayı etiketleri yalnız script'te geçenler (Salvestro levhası "SALVESTRO · MEDİCİ AİLESİNİN BAŞKA KOLU · GONFALONIERE SEÇİLDİ"; script'te olmayan "de'" soyadı kaldırıldı). Salvestro Giovanni'nin ATASI olarak gösterilmez (ağaç: başka kol).
- Telif/yüz: Dante, Villani, Boccaccio, Stefani, Machiavelli, Michele di Lando siluet/levha; hiçbir gerçek yüz yok; Giovanni di Bicci bronz madalya (profil, uydurma yüz değil, madalya stili).
- Dokunulmayanlar: motor/dünya/cilt dosyaları, `sfx_cues_p1.json`, `out_p1/*`.

## Ekrandaki olgular ve kaynak sınıfı
| ekran | cümle | sınıf |
|---|---|---|
| 1252 dönen florin; "Floransa kendi altınını basıyor" | c1s1 | ◐ M1:#4 + YORUM |
| 3,5 GRAM · 2 CM · NEREDEYSE SAF ALTIN | c1s2 | ◐ M1:#4,§4A (brif ekran kartı) |
| DANTE · lanetli çiçek (florin → zambak → kurt) | c1s3–4 | ◐ ifade M1:D01 (terzina yok; çeviri bize ait) |
| GIOVANNI VILLANI · KRONİKÇİ · ESKİ DARPHANE YÖNETİCİSİ | c1s5 | ◐ M1:#12,D02 |
| 1338 · 90.000 KİŞİ · VILLANI'YE GÖRE; HESAP OKULLARI | c1s6–7 | ◐ "Villani'ye göre" M1:D02 |
| ÇOK ŞUBELİ BANKA; 1330'LAR; PERUZZİ 15 ŞUBE; BİR KAYNAĞA GÖRE; Medici arması ✗ | c1s8 | ○ M1:#11,düz2,mit2 |
| BARDİ + PERUZZİ söner; III. EDWARD · ÖDENMEDİ; 1340'LAR | c1s9 | ◐ M1:#13,düz2 ("gösterilir") |
| VILLANI'NİN KARDEŞİ · PERUZZİ'DE ÇALIŞIYORDU · KAYBEDENLERİN AİLESİNDEN | c1s10 | ◐ M1:#14,D08 |
| MART – TEMMUZ 1348 (veba, renk söner) | c1s11 | ◐ M1:#15,düz2 |
| BOCCACCIO · ANLATIR (sağlıklılar kaçar, hasta yalnız, kapılar kapanır) | c1s12 | ◐ M1:D03 ("anlatır"; beden yok) |
| MARCHIONNE DI COPPO STEFANI · 12 YAŞINDA; YILLAR SONRA; KATMAN KATMAN | c1s13 | ◐ M1:D04 (birebir söz yok) |
| NE DÜŞÜNDÜĞÜNÜ BİLMİYORUZ / NE GÖRDÜĞÜNÜ, NE YAZDIĞINI BİLİYORUZ | c1s14 | YORUM (kalıp) |
| 1378; SALVESTRO · MEDİCİ AİLESİNİN BAŞKA KOLU; AKTARILANA GÖRE; AKTARILIR | c1s15–16 | ○ M1:#18 |
| 21 lonca arması (görsel sıra; metin etiketi yok; brif kalemi); yün işçisinin kesikli boş arması; susturulmuş balon | c1s17 | ◐ M1:#19,D06 |
| 22 TEMMUZ 1378 · CIOMPI · MICHELE DI LANDO · ÇEKİLDİ | c1s18 | ◐ M1:#19,D06 |
| VERGİDE ADALET · İŞÇİLERE LONCA HAKKI · KAMU BORCUNUN AZALTILMASI · YAZILDIĞINA GÖRE | c1s19 | ○ M1:#19 (tek kaynak) |
| MACHIAVELLİ · MEDİCİ SİPARİŞİ · KURGU (adsız isyancı, konuşma ruloşu) | c1s20–21 | ◐ M1:D07,mit11 |
| AĞUSTOS SONU (milis alayı); kızıl yıkama (beden yok) | c1s22–23 | ◐ M1:#21 |
| SEÇKİNLER bir kademe yukarıda; MEDİCİ aşağıda; kır gelirleri | c1s24 | ◐ M1:D09 |
| GIOVANNI DI BICCI · KÜÇÜK BİR PAY | c1s25 | ◐ M1:D09 |
| ROMA · VIERI DI CAMBIO'NUN BANKASI; ALACAK/BORÇ; DEVRALDI; 1390'LARIN BAŞI | c1s26 | ◐ M1:#23,#24 |
| PICCARDA BUERI'NİN ÇEYİZİ · 1.500 FLORİN; EVLİLİK SÖZLEŞMESİ · İLK SERMAYE | c1s27 | ◐ M1:#23,D09 |
| 1397; ORSANMICHELE; VIA PORTA ROSSA × VIA CALIMALA | c1s28 | ◐ M1:#25,D10 |
| 10.000 FLORİN; BİR MASA VE BİR DEFTER; faiz günahtır (haç) | c1s29–32 | ◐/YORUM M1:#26,K2 |

## Bilinen kusurlar
1. `p1_sehir` / `c1_sokak` / `c1_darphane` / `c1_kardes` kendi kamera yolunda (`cams=` anahtar kareli; `cam=` varlık işareti); `c1_darphane` ve `c1_kardes` tek çekim içinde iki alt çekim (kesme yok, `link="cam"`).
2. Uzun planlar: c1_agi 13,7 sn, c1_machiavelli 14,1 sn, son oda 16,3 sn (longtake; her biri kamera/yazı akışıyla dolu, qa_flow durgunluk 0,5 sn).
3. `p1_oda` "talepler" çekimi ve veba odası kısa (2,2–4,0 sn) — geçiş pencereleri yüzünden ms/kare ölçümü şişebiliyor; ortalama ≈120 ms/kare.
4. Şehir/sokak ölçekli çizimde "Floransa'nın üstüne kızıl yıkama" tek renkli lavdır; gerçek kan/beden görüntüsü yok, ama kızıl ton "kan" çağrışımı yapar (kaynak "en kanlı günlerinden biri" diyor; kasıtlı).
5. Medici arması (c1_agi'de ✗) kod çizimi; Medici'nin armasının palle sayısı/biçimi Rönesans hanedanlığa göre stilize.

## Ana ajandan istekler
- `p1_counter`/engine `counter` türü çapa tuple'ı kabul etmiyor (`at=("c1s2","üç",-0.2)` → TypeError); çözüm: `p1_emblem` + `P.count_up` bindirmesi. İstek: `counter` `at=` için anchor desteği.
- `OWN_CAMERA` kayıtlarında `oda`/`sehir`/`p1_*` sarmalayıcıları çalışma anında ekleniyor; kalıcı kayıt istenir.
- `qa_flow --chapters c1` tek bölüm koşusunda olay yoğunluğu yapay sapıyor (c1s1 c0'ın outro penceresine düşüyor); gerçek kapı `--part 1`.

## Kapı sonuçları (qa_flow --part 1)
Durgunluk GEÇTİ (en uzun 0,5 sn) · kamera %100 (92/92) · gerekçeli geçiş %100, çıplak fade %0 · çekim uzunluğu GEÇTİ (c1 medyan 5,73 sn; longtake hariç 5,56; max 16,3 sn longtake) · tür tekrarı 0 · çapa: mutlak %3 (tüm P1) · yön 0 uyarı (c1: 1 bilinçli: `slide l` Villani; skyline `pan l` kanlı gün de ters yönde ama kartta gerekçeli) · altyazı bölgesi boş · yönetmen kartı 39 satır = 39 çekim · olay yoğunluğu %96 (Parça 1; c1'de olaysız: c1s30, c1s31 — son uzun planın sakin kısmı; pop etiket + sikke yayı + parıltı eklendi, ölçüm eşiğini geçmedi ama yoğunluk kapısı yeşil). `preview_chapter.py c1 --check`: uyarı yok; ort. ≈120–126 ms/kare (≈11,5–12 dk tek çekirdek); yalnız #15 (hasta yalnız, candle girişi/çıkışı) örneği ≈270 ms (geçiş penceresi artefaktı).

Görsel denetim: tüm çekimlerin kontak sayfaları görüldü; `--clip` ile florin → panorama iris'i (105,5–107,3 sn), lonca → Ciompi slide'ı (236,1–237,9 sn), Villani → veba yıkaması (180,3–182,1 sn) kare kare akıyor.
