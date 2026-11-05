# v3.2 cila turu · ENG-E (maddeler 8–10)

- **Tarih:** 05.11.2026
- **Brif:** `kurul/duzeltme_tur3/BRIF_v32_CILA.md`
- **Dosyalarım:** `cilt_oda.py`, `c0_kinds.py`, `scenes_c0.py`, `scenes_c1.py`, `c1_kinds.py`. `c2_kinds.py`, `scenes_c2.py` (SCN-3) ve `p1_ortak.py`'ye dokunmadım.
- **Değişmeyenler:** anlatım, ses, altyazı, sayılar, etiket metinleri.
- **Yapmadıklarım:** render, commit, kapak PNG'si (başkan üretecek).
- **Kanıtlar:** `out_p1/duzeltme/v32/ENG-E/` (3 JPEG, en büyüğü 752 KB). Ölçüm betikleri `…/scratchpad/enge/` (`ad_probe.py`, `v32_olc.py`, `kanit_v32.py`). Kare dökümleri silindi.

## Özet

| # | Madde | Durum | Kanıt |
|---|---|---|---|
| 8 | Asemik el: kançılarya düzeni (SA2-G1) | **Kapandı** | `v32_08_asemik_el_once_sonra.jpg` |
| 9 | 1737 genel planında iki ad (TE2-G11) | **Kapandı** | `v32_09_adlar_once_sonra.jpg` |
| 10 | #48 levhaları × arma ızgarası (SA1-G1, AN2) | **Kapandı** | `v32_10_lonca_levhalar_once_sonra.jpg` |

**Bir aksama:** `c1_kinds.py`'yi düzenlerken sabitleri `@ckind` dekoratörü ile `def k_lonca` arasına yazdım. Dosya birkaç dakika içe aktarılamadı ve SCN-3'ün kare kontrolü durdu. SCN-3 haber verdi, hemen düzelttim. O andan sonra her düzenlemeden sonra derleme denetimi yaptım.

## 8. Asemik el (SA2-G1)

**Ne yapıldı** (`cilt_oda.py`; yazı motoru tek yer, belgeyi çizen her yer değişir)
- **Eğim 20–25°:** `ASM_SLANT` = tan 20°…tan 25° (564; seçim 630).
  - Eski aralık tan 0,20–0,24, yani 11–13,5°.
  - P1 belgesinde (tohum 3, 13 satır) **21,7°**.
  - Sözcük başına oynama ±0,03 → ±0,015 (`ASM_SLANT_WORD`, 565, 671).
- **x-yüksekliği satır içinde sabit, değişkenlik yarıya:**
  - sözcük başına ±%8 → ±%4 (668);
  - birim başına ±%13 → ±%6,5 (519);
  - satırlar arası ±%6 → ±%4 (656);
  - birim genişliği daha düzenli (520), kalem titreşimi 0,055 → 0,04·hx;
  - taban dalgası 0,7 → 0,4 px; satır eğimi ±0,6 → ±0,4 px/800.
- **Kançılarya düzeni, düzenli sözcük araları:** hl·(0,55 + 0,45·r) yerine hl·(0,85 + 0,12·r) (`ASM_SPACE`, 566, 672). Aralıklar hem düzenli hem biraz daha açık.
- **Başlık:** 47,0 sn yakın planında harf parçası gibi okunan iri başlık "sözcükleri" kalktı. Yerine süslü kalem çizgisi (trait de plume) geldi (`_asm_rule`, 581; çağrı 649): ortası şişkin, uçlara doğru incelen hafif S dalgası, iki uçta içe kıvrılan sarmal, ortada küçük baklava. Harf ya da sözcük biçimi yok.
- **Satır başı:** v3.1'in harfe benzeyen üç ayrı büyük harf biçimi yerine tek tip süs kıvrımı (`_asm_initial`, 569). Yükselen ilmek, alt kıvrım ve çıkış kuyruğu var; ilmeğe paralel ince ikinci çizgi kançılarya "cadel"ini andırıyor. Kullanılmayan `_asm_cap` kaldırıldı.
- **#8 yakın planı (2,1–2,24×), gövde ≈%70:**
  - `doc_sheet`'e `script_alpha=1.0` parametresi (727, 765); yalnız yazı sönükleşir, kâğıt ve mühür değil.
  - `k_belge` bunu iletir (`c0_kinds.py:264, 275`).
  - Yalnız #8'de `script_alpha=0.7` (`scenes_c0.py:98`).
  - ITALIANO yazımı ve sinabar çizgi ayrı katmanda tam alfa, yani önde.
- **Gerçek sözcük:** üretici harf alfabesi kullanmıyor (yordamsal kalem izi). Başlıkta artık hiç harf benzeri öğe yok.
- **Değişmeyenler:** satır tabanları (III. madde vurgusu ve Romen rakamları hizada; 55,8 sn karesinde doğrulandı), mühürler, FRANSIZCA ve ITALIANO.

**Önce / sonra** (`v32_08…jpg`)
- Kareler: 36,5 · 40,6 · 47,0 · 48,2 · 55,8 sn; ayrıca 0,6 sn yankı ve 34,0 sn 1743 odası inişi (bozulma yok).
- Tam çözünürlük kırpıntılar:
  - 47,0 sn başlık bölgesi: önce iri sözde başlık, sonra süs çizgisi;
  - 48,2 sn: sonra gövde sönük, ITALIANO önde.

**Etki:** `doc_sheet`'i kullanan her yer yeni eli alır (1743 odası, yankı, P7'nin `c0_belge`'si, odalardaki belgeler). Kapak PNG'si yeniden üretilince K1'deki belge de değişir (başkan).

## 9. 1737 genel planında iki ad (TE2-G11)

**Ne yapıldı** (`scenes_c0.py:80–81`, başkanın parametreleriyle)
- `names_hide=[(0, ("c0s7", "Lorraine", -0.5), ("c0s8", -0.35))]`: Lorraine tarafındayken sol ad sönük; c0s8 −0,35'te geri gelir.
- `names_out=("c0s8", "on", -0.3)`: iki ad birlikte söner.

**Ölçüm** (`ad_probe.py`: `CM.ink` çağrısında tuval dönüşümü; kutu, alfa, ekranda görünen pay):

| sn | ANNA MARİA LUİSA | LORRAİNE TARAFI |
|---|---|---|
| 37,8 | α 0,39 söner (kenarda %81) | — |
| 38,2 | sönük | — |
| 39,3 | sönük | α 1,0, tam |
| 39,5 | α 0,44 geri geliyor, tam | α 1,0, tam |
| 39,7–40,0 | **α 1,0, tam** | **α 1,0, tam** |
| 40,05–40,25 | kamera Romen rakamlarına inerken alt kenardan çıkıyor (%100 → %28 görünür; α 1,0 → 0,81) | sağ kenardan çıkıyor (%79 → %4) |
| 40,3 | dışarıda (α 0,64, sönüyor) | dışarıda |

- **Önce:** 39,4–39,7 sn genel planda yalnız "LORRAİNE TARAFI" vardı.
- **Sonra:** 39,5–40,05 sn iki ad birlikte ve tam görünüyor.
- Brifteki sönme çapasıyla adlar 40,05–40,25 sn'de kamerayla birlikte kadrajdan çıkarken ≈0,2 sn kısmen görünüyor (`qa_yerlesim` yarım yazı eşiği 0,5 sn). Sabit değil, hareket hâlinde. Daha erken söndürmek istenirse ("on" −0,45 gibi) tek değer.
- **Kontrast:** renk ve punto değişmedi. TE2 39,6 sn'de "LORRAİNE TARAFI"nı 4,7:1 ölçmüştü; aynı renk ve zeminde sol ad için de benzer değer beklenir. Ben ayrıca ölçmedim.

## 10. #48 levhaları × arma ızgarası (SA1-G1, AN2)

**Ne yapıldı**
- **`c1_kinds.py` (artık benim):**
  - Arma ızgarasının üst sırası 270 → 300; sıra aralığı 190 → 175 (`LONCA_Y0/DY`, 573; kullanım 588).
  - **Alt sıra yerinde (650):** yeni Ciompi kalkanıyla ve boş yuvayla (1290, 810) çakışma doğmaz. "Izgarayı 70 px indir" seçeneği alt sırayı kalkana bindirirdi.
  - #40 (c1s17) de aynı ızgarayı kullanıyor; iki çekim tutarlı.
- **`scenes_c1.py:234–235`:** iki levha (200, 960) → (128, 900). Kutu y 86,7–169,3 (brif: ≈90–165), x ≈371–1429 (HUD dikdörtgeni x ≥ 1440'tan uzak). x=960'ta "KISA ÖMÜRLÜ…" 1489'a taşıyordu.
- **Aynı çekimdeki küçük not (SA1):** yün işçisi siluetinin çıkışı.
  - Eskiden 1,6 sn'de 760 px kayıp "ARMALAR TEMSİLÎ" üstünde soluyordu.
  - Şimdi 2,4 sn'de 1150 px **yürüyerek** (adım döngüsü `walker`, hız zemine eşli) kadrajdan tamamen çıkıyor; yalnız kadraj dışındayken sönüyor (`c1_kinds.py:600–623`).
  - Hızı deklanşöre bildiriliyor (`anim.hint_pts`).

**Ölçüm** (`v32_olc.py`: `_shield` çağrısında tuval dönüşümü yakalandı)
- **Önce:** levha kutusu y 158,7–241,3; üst sıra arma tepeleri y≈175–200 → ≈40–65 px örtüşme.
- **Sonra:** 274,1–277,7 sn boyunca arma tepesi ile levha alt kenarı arasında **en az 36,7 px** boşluk (SA1: ≥20). Kamera itmesi ve kalkan salınımı (±10 px) dahil.
- `v32_10…jpg`: 271,7–277,0 sn önce/sonra; levhalar armaların üstünde, figür yürüyerek çıkıyor.
- **Kamera:** v3.1'deki 100 px yatay kaydırma (TE2-G5, CİOMPİ LONCASI kenar payı) duruyor. TE2 tur 3b'de G5'i kapattı; dikey düzen bu kaydırmadan etkilenmiyordu (AN2 de böyle).

## Son kapı (qa_flow)

QA_V32_YER_TUTUCU

## Açık / emin olmadığım

1. **Satır başı süsü.** Harfe benzeyen üç biçim yerine tek tip süs kıvrımı koydum. Ama yükselen ilmek, el yazısı bağlamında yine bir "L"/"S" büyük harfini andırabilir; kançılarya elinde satır başı büyük harfi zaten beklenir. Başlıkta artık harf benzeri öğe yok.
2. **Adların çıkışı.** Brifin çapasıyla adlar ≈0,2 sn kenardan geçerek çıkıyor (§9). Tamamen kenar öncesi söndürmek için çapa ≈0,15 sn erkene alınabilir.
3. **Kapak.** K1 PNG'si yeniden üretilince belgedeki el ve başlık süsü değişecek (başkan).
