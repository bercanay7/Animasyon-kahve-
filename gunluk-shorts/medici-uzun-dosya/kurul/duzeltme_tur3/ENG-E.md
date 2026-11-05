# ENG-E · Kurul tur 3 düzeltmeleri: motor, c0 ve c1 (Medici P1 v3.1)

- **Tarih:** 05.11.2026
- **Alan (brif):** `anim.py`, `compose.py`, `c0_kinds.py`, `scenes_c0.py`, `scenes_c1.py`, `cilt_oda.py`, `kapak_medici.py`. `p1_ortak.py`'ye **yalnız ekleme** (0 satır silindi/değişti, 54 satır eklendi). `cilt_cam.py` brifte benimdi ama değiştirmem gerekmedi (yalnız `CUT_SLOPE`, `_end_factor`, `hermite` kullanıldı).
- **Dokunmadıklarım:** `c2_kinds.py`, `scenes_c2.py` (SCN-3), `c1_kinds.py`, `cilt_fx.py`, `cilt_pano.py`, `cilt_medici.py`, `shots.py`, `qa_flow.py`. Anlatım, ses, `timeline.json`, altyazı değişmedi.
- **Yapmadıklarım:** render, miks, git, kapak PNG/JPG üretimi.
- **Kanıtlar:** `out_p1/duzeltme/tur3/ENG-E/` (01–08, hepsi JPEG ≤ 670 KB). Ölçüm betikleri: `…/scratchpad/enge/` (`olc_shutter.py`, `olc_misc.py`, `fr_probe.py`, `lonca_probe.py`, `dogrula.py`, `doku_yalniz.py`, `tex_scan.py`).
- **Brife sonradan eklenen maddeler (koordinatör):** TE1-Y9 (doku dikişi), TE2-G4 (FRANSIZCA), TE2-G5 (CİOMPİ LONCASI), TE2-G6 (bitiş satırı). Hepsi bu raporda.

## 0. Kısa sonuç

| # | Görev | Durum | Kurul maddesi |
|---|---|---|---|
| 1 | Küçük hızlı nesnelerde deklanşör: nesneler GERÇEK hızlarını bildiriyor | **Kapandı** | AN1-Y7 (motor tarafı) |
| 2 | 43,9 sn kesme girişinde duruş (`c0_belge`) + OWN_CAMERA/kendi kamera taraması | **Kapandı** (+ #14 `c0_kuyruk`) | AN1-Y-N3 |
| 3 | Açılış yankısı: yeni K1 zemini; kilitteki beyaz parıltı | **Kapandı** (a ve b) | PK2-Y8 |
| 4 | 271,1 sn kırmızı taşıma geçişi | **Kapandı** (mürekkep şeridi) | PK2-Y9 |
| 5 | 1737 belgesi: zikzak → asemik el yazısı | **Kapandı** | SA1-N3 |
| 6 | Dünyaya kilitli kâğıt dokusunda ayna dikişleri | **Kapandı** | TE1-Y9 |
| 7 | FRANSIZCA damgası sağ kenarda | **Kapandı** | TE2-G4 |
| 8 | CİOMPİ LONCASI etiketi sağ kenarda | **Kapandı** (sahne kamerasıyla; ayrıntı §8) | TE2-G5 |
| 9 | Bitiş ekranı "2/7 · COSİMO…" satırı | **Kapandı** | TE2-G6 |

**Son kapı:** `qa_flow.py --part 1` → §10.

---

## 1. Küçük hızlı nesnelerde deklanşör (AN1-Y7)

**Sorun (ölçtüm):** deklanşör hızlı küçük nesneyi görmüyordu. Akış ölçümü (`compose._flow_feats`) yalnız karenin ≥%3'ü ≥16 px/kare giderse tetikliyor; sikke, kitap, kulp karenin %0,05–0,3'ü. `anim.hint_speed` P1'de yalnız damga yaklaşmasında sabit 9,0 ile çağrılıyordu (darbe anı ve sonrası 0).

**Ne yaptım**
- `anim.py` (yeni, geriye uyumlu yardımcılar; eski işlevlerin imzası değişmedi):
  - `speed_pts`, `hint_pts` (anim.py:516, 529): nesnenin aynı noktalarının (kutu köşeleri + merkez) t ± 1/48 sn konumu → px/kare. Noktalar **o anki tuval dönüşümüyle** ekrana eşlenir; çizim oda/belge düzlemindeyse kamera ölçeği de girer.
  - `box_pts`, `stamp_pts` (547, 556): damga pozunun (öteleme, dönme, ezilme) köşeleri.
  - `hint_shake` (574): tüm karenin sarsıntısı (`jolt`).
  - `hint_pop` + `cm_stamp_scale` / `cm_seal_scale` / `cm_stamp_box` (584–611): `CM.stamp` ve `CM.wax_seal`'ın "çarpma" ölçeği (1,8× / 1,55× → 1×).
  - `stamp_ovl` (anim.py:~470–490): sabit 9,0 kalktı; **bütün profillerde** yaklaşma + darbe sonrası 0,6 sn gerçek hız. `impact_ovl` ve `stamp_ovl` sarsıntısı da hızını bildiriyor.
- `p1_ortak.py` (yalnız ekleme): `prop_arc` (541), `coin_arc` (463: yaydaki konum + dikey eksende dönen kenar), `seal_drop` (1017), `stamp` (221). Yeni yardımcılar `_arc_pos`, `_hint_arc`, `_hint_coin`, `_hint_seal_drop` (547–595).
- `c0_kinds.py`: takvimde savrulan yapraklar (`_leaf_fly_pts` 59, çağrı 141), belge mühürleri (315, 319), FRANSIZCA damgası (339), yuvarlanan sikke (669–675).
- `kapak_medici.py`: yankıda kapanan kulp (605) ve kulp sarsıntısı (625). **Yalnız canlı yankıda**; kapak karesi deklanşörsüz (`engine_frame shutter=False`), kapak değişmez.
- **Yan etki düzeltmesi (motor, geriye uyumlu):** takvim yaprakları bütün kareyi alt örneklemeye soktuğunda hızla sayan "N GÜN" sayacı alt kareler arasında değişip hayalet rakama dönüştü (30,79 sn "83/84"). `compose._render_shot`'a nominal kare saati `cx.t_nom` eklendi (compose.py:641; alt örneklerde `g_nom=g`, 804). Takvim sayacı bunu okuyor (c0_kinds.py:162). Öteki türler etkilenmez (yeni öznitelik).

**Önce / sonra** (`olc_shutter.py`, tam program karesi; `N` = alt örnek sayısı, 0 = bulanıklık yok):

| An | Nesne | İpucu önce → sonra (px/kare) | N önce → sonra |
|---|---|---|---|
| 0,50 | kapanan kilit kulbu (yankı) | 0 → 12,2 | 0 → 3 |
| 30,42 / 30,79 | takvim yaprakları | 0 → 58,8 / 71,7 | 0 → 5 / 7 |
| 41,92–42,00 | FRANSIZCA damgası (çarpma) | 0 → 127 / 131 / 63 | 5 → 7 |
| 95,29 / 95,42 | yuvarlanan sikke | 0 → 353 / 190 | 0 / 3 → 7 / 7 |
| 236,25 / 236,29 | CİOMPİ (squash, yaklaşma) | 9,0 → 36,7 / 40,4 | 3 → 5 |
| 236,33 / 236,42 | CİOMPİ (darbe sonrası) | 0 → 12,3 / 8,4 | 0 → 3 |
| 290,71 / 290,83 | sikke yayı (c1s25) | 0 → 37,3 / 32,8 | 0 → 5 |
| 300,83–301,04 | uçan kitap (`prop_arc`) | 0 → 31,0 / 30,3 / 28,3 | 0 → 5 / 5 / 3 |
| 309,13 | İLK SERMAYE (bounce, sekme) | 0 → 11,6 | 0 → 3 |
| 331,58 / 339,00 | sikke yayları (c1s31, c1s32) | 0 → 57,0 / 55,2 | 0 → 5 |

- **`shutter_stats`** (aynı 33 kare): bulanık kare 12 → 26; ek çizim 30 → 94; ek süre 5,3 → 14,8 sn; boşluk doldurma 7 → 20.
- **Kanıt:** `01_deklansor_once_sonra.jpg` (önce / sonra / takvim sayacı keskin).
- **Maliyet (tahmin, ölçmedim):** etki yalnız bu olayların karelerinde. P1'de ≈400 kare (≈%3) 3–7 alt örnek alıyor; bunların bir kısmı zaten akışla bulanıyordu (#7 belge kamerası). Tam render süresine etkisi kabaca +%5–10.
- **P2–P7:** `stamp_ovl`/`impact_ovl` P2–P7 sahnelerinde kullanılmıyor (grep). `p1_ortak` yalnız P1. Yeni `anim` yardımcıları ve `cx.t_nom` geriye uyumlu; varsayılan eşikler (`SHUTTER_V_HINT` = 8 vb.) değişmedi. c2'de (SCN-3) 8 `prop_arc`, 8 `stamp_ovl`, 2 `impact_ovl` bu ipuçlarını kendiliğinden alır.

## 2. Kesme girişinde duruş (AN1-Y-N3)

**Neden:** `c0_belge` OWN_CAMERA. Kamera `cams=` anahtarları arasında smoothstep (`_cr`): her anahtarda hız 0. #8'in ilk anahtarı kesmenin kendisi (hız 0), ilk aralık 3,36 sn'de yalnız %3,8 itme. #7'nin son anahtarı kesmeden 0,05 sn önce; sonra kamera duruyordu. `cam="hand"` beyanı OWN_CAMERA olduğu için hiç uygulanmıyor (değiştirmedim).

**Ne yaptım** (`c0_kinds.py`)
- `_cr_cut` (215): `_cr` ile aynı, ama uçta eğim alır. Uç aralık Hermite'tir (dış uçta e, iç uçta 0; e ≤ 3 için tekdüze, aşma yok). Anahtarın ötesinde hız tau = 0,6 sn'de sönümlenir (`cilt_pano.pchip` ile aynı uzatma). e0 = e1 = 0 iken `_cr` ile bit-birebir aynı.
- `_doc_cam` (245): e = `cilt_cam._end_factor(False, cut_in/cut_out)` → yalnız **sert kesme** uçlarında `CUT_SLOPE`. `k_belge` (273) ve belgeye bağlı "13 MADDE" sayacı `belge_sayac` (1036) aynı işlevi kullanıyor; sayaç belgeye bağlı kalıyor.
- Geçişli uçlara (zoomthru/carry) bilerek dokunmadım. CARRY uygulansaydı #10'un 1,1 sn'lik geçiş öncesinde belge ≈%27 küçülürdü; istenmeyen görünür bir değişiklik.
- **Tarama** (benim dosyalarımdaki OWN_CAMERA ve kendi kamerası olan türler):
  - `p1_oda`/`p1_pano` (cilt_oda/cilt_pano): ENG-D'nin `PanoCam` kuralı zaten uygulanıyor.
  - `kapak_kilit`, `k_outro`: kesmeye bağlı değil (geçiş / kart).
  - **`c0_kuyruk` (#14, 77,97 sn kesme):** kendi kaydırması `ease_io(u, 2)` ile sıfır hızdan başlıyordu. Kesme ucunda `cilt_cam.hermite(u, CUT_SLOPE, …)` (c0_kinds.py:510–515); kesme yoksa eski eğri aynen.

**Önce / sonra**

| Ölçüm | Önce | Sonra |
|---|---|---|
| #8 ilk adım (ENG-D yöntemi: çekim tek başına, 480×270) | 0,194 (ikinci adım 0,177) | **0,473** (ikinci adım 0,490) |
| #7 son adım (aynı yöntem) | 0,532 | 2,144 |
| Program karesi 43,917 / 43,958 sn (320×180, post dahil) | 0,312 / 0,308 | 0,528 / 0,531 |
| #14 ilk adım (ENG-D yöntemi) | 0,404 (ENG-D v3 tablosu) | **2,864** (ikinci adım 2,849) |

- #8'de ilk adım ikinci adıma eşit: kamera kesmeye ortalama hızıyla giriyor, sıfırdan hızlanmıyor. Hareket yine yavaş (sahnenin beyanı: 3,36 sn'de %3,8), ama duruş yok.
- AN1'in videodaki 0,07 ölçümünü birebir yeniden üretemem: H.264'ten geçmiş videoyu ölçmüş; ben program karesini ölçtüm.
- **P2–P7:** `c0_belge` P7'de (c16s3) de var; girişi zoomthru, çıkışı slide, yani kesme ucu yok → kamerası bit-birebir aynı. `c0_kuyruk` yalnız P1.

## 3. Açılış yankısı (PK2-Y8)

**(a) Zemin:** `scenes_c0.py:28–31`. Yankı artık `**KP.KAPAK_ZEMIN["K1"]` ile çiziliyor: ton (52, 32, 26), vinyet 0,30, ışın yok. Eskiden `KAPAK_SAHNE`'nin yakın-siyah tonu (18, 10, 15) ve türün varsayılan vinyeti 0,75 kullanılıyordu.

**(b) Beyaz parıltı:**
- `kapak_medici.parilti` (213)'e `sicak=False` seçeneği eklendi. True iken beyaz çekirdek yok: pirinç üstünde yatık, yumuşak, sıcak renkli (#F0B45A) yansıma, ekran (screen) karışımıyla; renk kırpılıp beyaza patlamıyor.
- `k_kapak_kilit` (536)'a `parilti_sicak=False` parametresi eklendi. Yankı True veriyor.
- Varsayılanlar değişmedi: kapak karesi yeniden üretilse de aynı çıkar.

**Önce / sonra** (`olc_misc.py yanki`; 168 px küçük resimde 4 px kenar halkası, kapak_qa yöntemi):

| | Kenar grisi | Gri < 25 payı | Kilit bölgesinde ≥250 piksel (x 750–840, y 680–770) |
|---|---|---|---|
| Yankı 0,3–3,0 sn, önce | 16,0–23,1 | %84–87 | 709–2283 |
| Yankı 0,3–3,0 sn, sonra | **37,8–44,5** | **%7–8** | **186–224** (kalan parlaklık pirinç kabartmasının kendi ışığı; beyaz leke yok) |
| K1 kapak JPG | 38,4 | %11 | — |

- **Kanıt:** `03_yanki_once_sonra.jpg` (kilit 2× ve tam kare).
- Kapak PNG/JPG yeniden üretilmedi. Yankıda ayrıca belge yazısı asemik oldu (§5); kapak PNG'sinde zikzak duruyor (168 px'te görünmüyor; brif bunu kabul ediyor).
- **P2–P7:** yalnız P1 yankısı. Yeni parametreler varsayılanla kapalı.

## 4. Kırmızı taşıma geçişi (PK2-Y9)

- `scenes_c1.py:240` (#48 `c1_lonca` girişi, yalnız bu geçiş): `strip="banner"` → **`strip="ink"`** (koyu mürekkep şeridi, kuru fırça izi).
- Önce `paper`'ı denedim. Ama `cilt_fx._strip_layer` kâğıt şeridinin ortasına **kırmızı balmumu mühür** çiziyor (cilt_fx.py:867, seçeneği yok, benim dosyam değil). Kırmızı daire kalacağı için mürekkep tonunu seçtim.
- Motor varsayılanı değişmedi. #40'taki öteki `banner` geçişi (c1s17, "21 lonca") aynen duruyor.
- **Kanıt:** `04_tasima_gecisi_once_sonra.jpg` (271,0–271,3 sn).
- **P2–P7:** etkisi yok.

## 5. 1737 belgesi: asemik el yazısı (SA1-N3)

**Ne yaptım** (`cilt_oda.py:432–720`)
- `_script_img` artık `_script_img_asemic` (574) üretiyor. Eski zikzak `_script_img_zigzag` (646) adıyla aynen duruyor; `SCRIPT_ASEMIC = False` (439) eski görünüme döner.
- **Harf alfabesi yok** (ilk denemem harf şablonluydu; "Stemmen", "les" gibi okunabilir diziler çıktı, attım). Yordamsal kalem izi kullanıyorum:
  - taban ile x-yüksekliği arasında salınan minimler (kemer / çanak / sivri bağlantı), ovaller;
  - üst/alt uzantı ilmekleri, uzun-s benzeri dikme;
  - satır başında büyük harf benzeri kıvrım.
- Brifin istediği özellikler:
  - değişken x-yüksekliği (satır ve sözcük başına);
  - sözcük araları;
  - sağa eğim ≈11–13°;
  - basınç: inen vuruş kalın, çıkan kıl çizgi;
  - mürekkep vuruş başında koyu (ilk ≈10 px kalın + koyu nokta), sözcük boyunca açılıyor; her 3–7 sözcükte "hokkaya batırma";
  - düzensiz satır sonları;
  - düşük kontrast (sözcük katmanı alfa 0,52–0,76, eski zikzak 0,75–0,92 ve 3,4 px).
- Tohumlu ve deterministik.
- **Çözünürlük:** görüntü 2× (`SCRIPT_RES`) ve mipmap'li. 2,5× yakın planda büyütme ≤1,25×; küçük ölçekte (odalardaki belgeler, 0,085–0,3) titreşmiyor.
- `doc_sheet` (≈694–735): ölçeği görüntü genişliğinden okuyor. Kısmi yazımda (`shown`) kırpma uzantı paylarıyla (`SCRIPT_ASC/DESC` 22,5 / 12,5) yapılıyor; yazılmamış satırın üst ilmekleri erken görünmüyor.
- **Değişmeyenler:**
  - satır tabanları aynı (top 150, adım 35/40);
  - Romen rakamları, III. satır vurgusu (altın leke + sinabar çizgi aynı hizada; 55,8 sn karesinde doğrulandı);
  - mühürler;
  - ITALIANO/FRANSIZCA vuruşları (FRANSIZCA'nın yeri §7'de bilerek değişti).
- **Gerçek Fransızca cümle yok.**
- **Kanıt:** `05_belge_asemik_once_sonra.jpg`: 36,5 / 40,6 / 46,0 / 48,2 / 55,0 / 55,8 sn ve tam çözünürlük kırpıntıları (2,24× ve III. madde ≈2,3×).
- **Maliyet:** görüntü başına ≈2 sn, süreç başına (tohum, satır sayısı) için bir kez (önbellekli). Bellek ≈18 MB/görüntü.
- **P2–P7:** `doc_sheet`'i kullanan her yer değişir: 1743 odasının masadaki belgesi, oda sahne nesneleri, öteki odalardaki küçük belgeler, P7'nin `c0_belge`'si (c16s3), kapak sahnesi. Brif bunu kabul ediyor. Kapak PNG'leri yeniden üretilmedi.

## 6. Kâğıt dokusunda ayna dikişleri (TE1-Y9)

**Neden:** `compose._tooth_warp` 1920×1080'lik tek dokuyu `BORDER_REFLECT` ile çarpıtıyordu; doku koordinatı görüntü dışına taşınca aynalanıyordu.

**Ne yaptım** (`compose.py:195–345`)
- `tooth_periodic` (237): `cilt_wall.tooth` ile **aynı model ve sabitler**: kum taneleri σ 0,95 / 1,6 / 2,6, ince gaussian 0,65, iri 7,0, gözenek; Sobel ışığı 0,55·gx + 0,65·gy; aynı normalleştirme.
- Fark: her süzgeç periyodik sınırla yapılıyor (`_blur_wrap`: np.pad wrap + kırpma; `_sobel_wrap`: np.roll ile aynı 3×3 çekirdek).
- Karo periyodu 3840×2160 (`TOOTH_TILE`), çarpıtma `BORDER_WRAP` ile.
- **Hız:** ofset periyoda indiriliyor ve karo sarmalı dolguyla (`TOOTH_PAD` 3072×1728) genişletiliyor. k ≤ 1,6'da örneklenen her nokta dizinin içinde kalıyor (hızlı yol); daha büyük k için karo + `BORDER_WRAP` (doğru, daha yavaş).
- `PAPER_WRAP = False` (202) eski davranışa döner. Ekrana sabit yol (`_tooth1`, `PAPER_WORLD=False`) değişmedi.

**Doğrulama**

| Ölçüm | Önce | Sonra |
|---|---|---|
| 2 sn'lik tarama (301 kare): ekran içinde dikişli kare | 138 (%46; TE1: %44) | dikiş yok (karo periyodik; aşağıdaki ölçüm) |
| Aynı taramada **yalnız doku görüntüsü**, 129 dikiş sütununda ayna korelasyonu | medyan **0,900** (en az 0,606) | medyan **0,055** (en çok 0,096); dokunun kendi iç dağılımı medyan 0,046, en çok 0,103 |
| 110,0 sn, x=1537 (gökyüzü bandı, tam kare) | 0,973 (bant medyanı 0,041) | **0,109** (dokusuz taban 0,086) |
| 292,5 sn, x=1491 (deniz) | 0,224 | **0,186** (dokusuz taban 0,185: kalan değer içerikten) |
| Döşeme sınırında (2×2 karo) ayna korelasyonu, üç bant | — | iç dağılımın %99,7 / %62,5 / %17,4 yüzdeliğinde (rastlantısal) |
| İstatistik (eski / yeni) | ort. 229,40 · std 8,16 · yüksek geçiren std 7,76 · özilinti(1) 0,560 · ışık imzası 0,393 | 229,40 · 8,17 · 7,77 · 0,560 · 0,392 |
| Çarpıtma süresi (120 gerçek matris) | medyan 2,09 ms · p90 7,71 ms | medyan **1,56 ms** · p90 **1,69 ms** |
| Periyodun ekranda görünmesi | — | P1'de k en çok 1,331 → ekran en çok 2556×1438 doku px < periyot 3840×2160: hiçbir karede periyot tekrar etmiyor |

- **Görsel:** `06_doku_dikisi_3x_once_sonra.jpg` (3×: 110,0 sn gökyüzünde "fermuar" simetrisi önce var, sonra yok; 292,5 sn deniz).
- **Bulgu (benim alanım dışında):** 110,0 sn'de x≈1754'te ayrı bir ayna simetrisi var (0,916). Doku ekrana sabitken de 0,896 → **içerikten**. Büyük olasılıkla `cilt_pano` set kenarı aynalaması (ENG-D `EDGE_FILL`, "taşan şerit aynalanmış dekorla dolar"). `cilt_pano.py` benim dosyam değil; dokunmadım.
- **P2–P7:** dünyaya kilitli doku bütün parçalarda aynı yoldan geçer; dikiş hepsinde kalkar (iyileşme). Doku deseni yeni rastgele karo (istatistik aynı). Kapak yeniden üretilirse doku deseni de yeni karodan gelir (üretmedim).

## 7. FRANSIZCA damgası sağ kenarda (TE2-G4)

- `c0_kinds.py:187` `FR_XY = (65, −40)` (eski (150, −40)), kullanım 338–339.
- Belge düzleminde 85 px sola. Aynı belge düzlemi olduğu için #7, #8 ve #10'da aynı yer (süreklilik).
- **Ölçüm** (`fr_probe.py`: `CM.stamp` çağrısında tuval dönüşümü yakalandı; harf kutusu, kırmızı çerçeve, kâğıt fiş):

| An | Harflerin sağ ucu, önce → sonra | Çerçeve sağ, önce → sonra | Fiş sağ, önce → sonra |
|---|---|---|---|
| #8 43,9 sn | 1878 → 1700 | 1954 → 1776 | 2001 → 1823 |
| #8 46,6 sn | 1911 → 1726 | 1989 → 1804 | 2038 → 1853 |
| #8 48,2 sn (en kötü) | 1939 → **1748** | 2019 → **1829** | 2069 → **1879** |
| #7 41,95 sn (damga iner) | — | — | harfler 562–1482: kadraj ortası |
| #10 56,2 sn | 1897 → 1715 | 1974 → 1792 | 2022 → 1840 |

- TE2'nin ölçütü (harfin sağ ucu ≤ 1830) 81 px payla sağlandı. Çerçeve de ≤ 1830, fiş ekranın içinde.
- **Kanıt:** `07_fransizca_lonca_bitis_once_sonra.jpg`.
- **P2–P7:** P7'nin `c0_belge`'si FRANSIZCA çizmiyor (`fr_at=None`); etkisi yok.

## 8. CİOMPİ LONCASI etiketi (TE2-G5)

**Sınır:** etiketin yeri `c1_kinds.k_lonca` içinde sabit (kalkanın sağı; dünya x ≈ 1391–1855). Bu dosya benim değil. Dünya konumu zaten güvenli çizginin dışında olduğundan, z ≥ 1 olan hiçbir `pull` odağı etiketi içeri alamıyordu.

**Ne yaptım** (`scenes_c1.py:236–240`, sahne düzeyi)
- `cam=("pull",)` yerine aynı geri çekilişi veren anahtar kareli kamera: odak (1072, 597) aynı, zum %6,8 → 0. İçerik 100 px sola.
- Etiket metni ve tür değişmedi.

**Ölçüm** (`lonca_probe.py`, etiket kutusunun ekran kenarları):

| An | Önce | Sonra |
|---|---|---|
| 271,0 sn (geçiş) | 1416–1917 | 1314–1811 |
| 271,6 sn | 1413–1908 | 1313–1808 |
| 274,0 sn | 1401–1878 | 1304–1787 |

- TE2 ölçütü (en az 60 px sola, ≤1827) sağlandı.
- **Bedeli:** kalkan ızgarası bu çekimde ≈100 px sola kaydı (sol pay ≈50, sağ ≈150 px). Sağdaki boşluğu etiket dolduruyor; gözle kabul edilebilir buldum.
- Kalıcı çözüm `c1_kinds.py`'de etiketin konumu. Sahibine iletilmeli.
- **P2–P7:** etkisi yok.

## 9. Bitiş ekranı satırı (TE2-G6)

**Ne yaptım** (`compose.py`)
- `NEXT_PART_LINE` (47) küçük harfle yazıldı ve çizimde `sk.tr_upper`'dan geçiyor (949) → "2/7 · COSİMO: SÜRGÜN VE DÖNÜŞ".
- Punto 28 → **34** (`OUTRO_SUB_SIZE`, 50). 34'ün altına inilmiyor; sığmazsa önce harf aralığı daralıyor (957–962).
- Yuvaların üst kenarı 610 → **556** (`OUTRO_SLOT_Y`, 49). Bütün yığın (yuva, etiket, satır) 54 px yukarı.

**Ölçüm** (596,0 sn tam kare, piksel): yuva çerçevesi y 555–848 · "SIRADAKİ PARÇA" y 865–904 · alt satır **y 916–952** (önce 973–994; en az 42 px yukarı), x 263–916; yuvayla ve sağ etiketle çakışma yok.
- **Kanıt:** `08_bitis_satiri_sonra.jpg`, `07_…`.
- Yayın adımları yuvaları piksel olarak değil "çerçevelerin üstüne yerleştir" diye tarif ediyor (`00_yayin_adimlari.txt`); metin değişmesi gerekmiyor. Studio'da öğeler yeni çerçevelere oturtulmalı.
- **P2–P7:** `k_outro` ortak: yuvalar her parçada 54 px yukarıda. `NEXT_PART_LINE` yalnız parça 1 için tanımlı; P2–P6 satırları küçük harfle eklenmeli (`tr_upper` büyütür).

## 10. Son kapı: qa_flow --part 1

**1. koşu** (12:56–13:03; çıktı `…/scratchpad/enge_qa.txt`): **19 GEÇTİ · 1 KALDI · 1 UYARI · 1 PAS**.

```
✗ Ölçülen hareket             KALDI    1 çekim >6 sn ve hareketsiz (medyan MAD<1.25)
✓ Beyan ↔ gerçekleşen kamera  GEÇTİ    42 çekim ölçüldü: ulaşmıyor 0, kısmen 0, gerçekleşen <%50/ters 0; kadraj koruması 0; …
✓ Aynı görüntü kesmesi        GEÇTİ    38 sert kesme: kesin sıçrama 0, sınırda 0, muaf 0
✓ Yerleşim (ENG-A)            GEÇTİ    qa_yerlesim P1: 303 kare, 77 levha kaydı · İHLAL 0 …
✓ Dönem (ENG-A)               GEÇTİ    qa_donem P1 [dönem katmanı açık]: 306 kare, 323 dönem kaydı · İHLAL 0 · uyarı 0
  [Ölçülen hareket]
    - #63 p1_map 'poliçe gider, para döner: kur farkı' 361.1s (7.7 sn): medyan 0.901
ÖZET: 19 GEÇTİ · 1 KALDI · 1 UYARI · 1 PAS
```

**KALDI'nın kaynağı c2 (#63, SCN-3'ün `scenes_c2.py`'si); benim değişikliklerimden bağımsız.** Kanıt:
- QA bu kapıda kareleri `post=False` çiziyor (`qa_flow.py:1074`, 1282): kâğıt dokusu, gren ve deklanşör ölçüme hiç girmiyor. Öteki değişikliklerim #63'te yalnız hız ipucu çağrısı ekliyor; piksel değiştirmiyor.
- **A/B denemesi** (`m63.py`):
  - Yalıtılmış bir klasörde (sembolik bağlar) benim 9 dosyam tur öncesi yedekleriyle, c2 dosyaları SCN-3'ün güncel hâliyle çalıştırıldı.
  - #63 medyanı yine **0,901**; 14 değerin hepsi bit düzeyinde aynı.
- **Neden kalıyor:**
  - SCN-3 bu turda #63'ün beyanını `("pull",)` → `("push", {"rate": 0.012})` yaptı (kendi brifi Y-N1).
  - Eski `("pull",)` beyanı bellekte denenince de medyan 0,949. Yani c2'nin bugünkü içeriğiyle #63 iki beyanla da 1,25 eşiğinin altında; v3'te (ENG-D koşusu) bu kapı geçiyordu.
  - Örnek değerler: 2,88 · 0,88 · 0,79 · 0,76 · 0,78 · 2,41 · 3,33 · 4,34 · 0,90 · 0,83 · 3,67 · 0,80 · 1,71 · 0,76. Rota çizilirken hareket var; aralarda harita durağan.
- **Öneri (SCN-3 / başkan):** #63'te itme oranını ≈%2–3/sn'ye çıkarmak ya da kazanç sikkesi salınımını çekim boyunca sürdürmek (SCN-3 brifi Y-N1 zaten bunu istiyor).

**UYARI:** yön denetimi (#15 `p1_skyline`), ENG-D'den beri kabul edilmiş eski uyarı (AN1-Y12). v3'teki ikinci UYARI (#63 kadraj koruması) SCN-3'ün değişikliğiyle kalktı.

**Benim alanımdaki kapılar:** hepsi GEÇTİ.
- "Beyan ↔ gerçekleşen kamera": 42 çekim, 0 ihlal; #48'in yeni anahtar kareli kamerası dahil.
- "Aynı görüntü kesmesi": 38/0.
- "Yerleşim": İHLAL 0; FRANSIZCA'nın yeni yeri ve bitiş ekranının yeni düzeni dahil.
- "Dönem": İHLAL 0.
- "Durgunluk", "Altyazı bölgesi", "Kamera hareket yeterliliği".

QA2_YER_TUTUCU

## 11. Açık kalanlar ve en emin olmadığım noktalar

1. **Asemik yazıda harf benzeri parçalar.**
   - Sözcük ya da cümle oluşmuyor. 2,5× kırpıntılarda okunur bir sözcük görmedim; başlıkta tesadüfen çıkan "Lien"i (gerçek Fransızca sözcük) üretici ayarıyla giderdim.
   - Ama yer yer "la", "n" gibi iki harflik parçalar okunabiliyor; asemik el yazısında bu tümüyle önlenemez.
   - P2–P7'deki öteki tohumlu belgelere tek tek bakmadım.
2. **Deklanşör maliyeti.** Olay karelerinde ölçtüm, tam video için yalnız tahmin ettim (+%5–10). Tam render'da `shutter_stats`'a bakılmalı.
3. **#48'in kadrajı 100 px sola kaydı** (§8). Kalıcı çözüm etiketin `c1_kinds`'teki yeri.
4. **Kesme girişi (#8).** Duruş yok, ama sahnenin beyan ettiği hareket bu aralıkta zaten yavaş (3,36 sn'de %3,8). Kesmenin "canlı" okunması için sahne anahtarı değişebilir; anahtarlara dokunmadım.
5. **110,0 sn x≈1754'teki içerik aynalaması** (`cilt_pano`, §6): benim alanım değil; ayrı bir iş olarak bakılmalı.
6. **Kapak tutarlılığı.** Yankı artık yeni zeminde, sıcak parıltıyla ve asemik belgeyle çiziliyor. Kapak PNG'leri eski (zikzak belge; parıltı beyaz). 168 px'te fark görünmez; büyük boyutta yan yana konursa belge yazısı farklı.
7. **TE1'in "aynı karelerde" isteği.** Analitik kanıt (periyodik karo, `paper_matrix` taraması, 129 sütun) ve iki karede tam görüntü ölçümü var. 301 karenin hepsini tam kare olarak yeniden çizmedim.
8. **Paylaşımlı çalışma.** QA koşuları sırasında SCN-3'ün c2 dosyaları da değişiyordu (md5 farklı). QA sonucu iki ajanın o anki ortak durumunu ölçer.
   - 1. koşudaki #63 KALDI'sını SCN-3'ün kendi koşusu da gördü.
   - SCN-3 `scenes_c2.py`'yi 13:12:36'da değiştirdi. Ardından aynı yöntemle #63 medyanı **3,407** (eşik 1,25) ölçtüm ve son QA'yı ondan sonra koştum (§10, 2. koşu).
   - SCN-3 bundan sonra c2'yi yine değiştirirse son durum için onun raporundaki QA geçerlidir.
9. **Geçici dosyalar.** Kare dökümlerimi (≈77 MB PNG) ve A/B denemesi için kurduğum bağ klasörünü sildim. Ölçüm betikleri ve JSON'lar `…/scratchpad/enge/`'de duruyor (küçük).
