# MEDICI — Stil Rehberi ve Teknik Sözleşme (sahne yazarları için)

Bu belge, "Zaman Kuryesi — Medici (7 parça × ≈10 dk, 1920×1080, 24 fps)" videosunun görsel katmanını yazan herkesin (insan/ajan) uyacağı **teknik sözleşme ve iş akışıdır**.
Üç sözleşme birlikte okunur: `USLUP_REHBERI.md` (nasıl anlatılır) · `YONETMENLIK_REHBERI.md` (nasıl çekilir/kesilir/akar; on emir, kapılar) · **bu belge** (motor API'si, dosya sahipliği, komutlar, teslim).
Motor ayrıntısı: `notlar_yonetmen_motoru.md` (kamera/geçiş/Program/qa_flow) ve `notlar_dunya.md` (figür/panorama/yapım animasyonu; §7). Kullanıcının tek şartı: **"oldukça uğraşılmış ve profesyonel gözükmesi"**; isteği: **"olabildiğince akan ve çok animasyon; yönetmenlik olarak usta ol."**

> **Ses durumu:** P1–P2 (c0–c5) **gerçek** (ElevenLabs); P3–P7 (c6–c16) **GEÇİCİ** (Piper; kredi bekleniyor). Gerçek ses gelince zamanlar DEĞİŞİR. Bu yüzden sahne zamanlarını **cümle/sözcük çapasına** bağla (`("c7s5", -0.2)`, `("c7s17", "silahı", -0.1)`); mutlak saniye ≤%10 (qa_flow ölçer).

---
## 0. Hızlı başlangıç

```bash
cd /home/user/Animasyon-kahve-/gunluk-shorts/medici-uzun-dosya          # python3 -I KULLANMA
cat isemri/c7.md                               # BÖLÜM İŞ EMRİN: cümleler+zamanlar, brif ekran önerileri, tuzaklar, rehber imza sekansı, kısıtlar
python3 preview_chapter.py c7 --script         # cümle kimlikleri + zaman + kaynak sınıfı (çapa seçmek için)
python3 preview_chapter.py c7 --words c7s17    # cümlenin sözcükleri ve zamanları (sözcük çapası için)
python3 preview_chapter.py c7 --check          # çekim listesi (cam/geçiş dahil), uyarılar, ms/kare
python3 preview_chapter.py c7                  # kontak sayfası → out_pN/frames/c7_sheet_1.png (N = c7’nin parçası: 3)  (MUTLAKA Read ile gör!)
python3 preview_chapter.py c7 --shots 4,5 -k 4 # yalnız bu çekimler, çekim başına 4 kare
python3 preview_chapter.py c7 --at 83.4        # PARÇA-İÇİ saniyede tam çözünürlüklü kare → out_pN/frames/c7_t83.4.png
python3 preview_chapter.py c7 --clip 80 6      # 6 sn'lik küçük mp4 (sessiz)
python3 preview_chapter.py c7 --flow           # yönetmenlik kapıları (kamera/geçiş/link/çapa/olay yoğunluğu/durgunluk)
```
Örnek sahne satırları: `preview_reel.py` (14 çekim; her kamera ön ayarı ve geçiş bir kez) + `notlar_yonetmen_motoru.md` §1. **`out` bağlantısına veya `parca.kullan()`'a dokunma**: önizleme parça duyarlıdır (`Program(chapters=[cK], part=N)`), çıktı `out_pN/frames/` altına gider.
İş akışı: (1) `isemri/cK.md` oku → (2) önce `yonetmen_cK.md` taslağı (çekim tablosu: çapa, tür, cam, giriş geçişi, neden) → (3) `scenes_cK.py` → (4) `--check` + kontak sayfası + `--flow` döngüsü → (5) `notlar_cK.md`.

---
## 1. Film ve anlatı özeti

- Konu: Medici ailesi (1252–2026 bakışı): **para → itibar → iktidar → güzellik** zinciri; kaynak zorluğu: ● hiçbir olgu yok (birincil metin okunmadı), ◐/○ düzeyinde; rivayetler "rivayet", tartışmalı yerler "tartışmalı" denir.
- **7 parça (≈10 dk) · 3 Perde:** Yayın parçaları: P1 c0–c2 · P2 c3–c5 · P3 c6–c7 · P4 c8–c9 · P5 c10–c11 · P6 c12–c13 · P7 c14–c16 (`script.PARTS`). Perde (ALTIN c0–c6 · BEDEL c7–c11 · MİRAS c12–c16) bölüm bazlı ışık/renk paletidir, parçadan bağımsız. P2…P7 ilk bölümleriyle **doğrudan** açılır (bölüm kartı yok; ilk çekimde "MEDİCİ — PARÇA N — ad" başlık bindirmesi 1,2–4,8 sn; Program ekler — sen çizmezsin, ilk çekimin sol üst/orta bandını boş bırak). P1'de c0 → ana başlık (`fresco_title`) → c1. Parça içindeki bölümler arası normal bölüm kartı.
- Bölüm kartları (3 sn, canlı) ve parça kapanışı (bitiş ekranı 7 sn: "SIRADAKİ PARÇA"/"TÜM FİLM" + "ABONE OL") `compose.py` tarafından otomatik eklenir. **Sahne dosyası yalnız bölümün KENDİ çekimlerini içerir.**
- HUD (yıl rulosu + perde göstergesi) Program çizer; yıl değişimleri için isteğe bağlı `YIL_AT = [(çapa/saniye, yıl), …]`. HUD alanını (sağ üst, sol üst bölüm başı) boş bırak.
- Ses: ElevenLabs "Emrullah Uzun". **Altyazı ayrı (SRT) — ekrana altyazı basma;** ekrandaki yazılar anlatıyı tamamlar, tekrar etmez. Altyazı şeridini (1080p'de alt ≈ y 938–1042) metin/etiketlerle işgal etme (qa_flow denetler; tür düzeni gereği bazı türlerde uyarı normaldir).
- Kaynak sınıfı damgaları: anlatıda "rivayet/anlatılır/yazılır" geçen cümleler için ekranda **damga** (`ANEKDOT`, `○ TEK KAYNAK`, `YORUM`, `MİT`) — iş emrinin kaynak sütunu hangi cümlenin ne olduğunu söyler.
- Sayılar ve adlar ekrana, anlatıda **söylendiği anda** gelir (çapa: sözcüğün 0,1 sn öncesi). Yazım: Türkçe karakterler (İ ı Ş Ğ Ü Ö Ç) doğru, sayılar nokta ayraçlı (850.000), tarihler "26 Nisan 1478". Ekrana **yeni olgu koyma**: iş emrindeki/brifteki ekran önerileri ve kaynak tabloları dışına çıkma; emin değilsen koyma.
- **Kısıt önceliği:** brif §5 tuzaklar + §7'deki "YOK/söylenmez/gösterilmez" notları + `scr_cK.py` docstring > rehber imza sekansı. Kaynakta olmayan saat/hava/ışık/çan sesi/koku/yüz iddiası görüntüde de yoktur. c0 alıntı kartı **Anna Maria Luisa'ya atfedilmez** ("Sözleşmenin 3. maddesinin özeti"; c16 söyler).

---
## 2. Dosya haritası ve SAHİPLİK KURALLARI

| Dosya | Ne | Kim düzenler |
|---|---|---|
| `sk.py` | Skia çekirdek (Frame, yazı, efekt, post, easing, palet) | **ana ajan** |
| `shots.py`, `compose.py` | çekim şablonu/`shot()`/`Ctx`; Program (zaman, geçiş, kart, HUD, parça) | **ana ajan** |
| `cilt_medici.py`, `cilt_kinds*.py`, `cilt_fx.py`, `cilt_cam.py`, `cilt_anim.py`, `cilt_pano.py`, `cilt_build.py`, `cilt_figs.py`, `cilt_props.py`… | Medici cildi: duvar/palet, çekim türleri, geçişler, kamera, figür/pano/yapım motoru | **ana ajan** (motor-lab ajanları yazdı; sen düzenleme) |
| `medal.py`, `icons.py`, `heraldry.py`, `mapsk.py`, `stage*.py`, `scenes_lib.py` | madalya/simge/arma/harita/diorama altyapısı | **ana ajan**; eksik yetenek için kendi modülünde ekle |
| `scenes_cK.py` | **bölüm K'nın çekim listesi** (`SHOTS = [...]`, isteğe bağlı `YIL_AT`, `OUTRO_TR`) | bölüm yazarı (yalnız kendi bölümün) |
| `yonetmen_cK.md`, `notlar_cK.md` | yönetmen kartı; teslim notu | bölüm yazarı |
| `cK_<ad>.py` | senin eklediğin YENİ modüller (çekim türü, figür, simge) — ad çakışmasın diye bölüm önekli | ekleyen |

**Kurallar**
1. Ortak dosyaları DÜZENLEME. Eksik bir yetenek için kendi modülünde yaz: yeni çekim türü → `import cilt_medici as CM` → `@CM.ckind("c7_hancer") def k_x(cx, **p)` (kamera/link/longtake otomatik ayıklanır; bkz. notlar_yonetmen_motoru §1) ya da düz `@SH.kind(...)`; yeni madalya/simge anahtarı → `medal_extra.py`/`icons_extra.py` kalıbı (ekleme yap, mevcutları değiştirme). Modül `scenes_cK.py` içinde `import` edilerek kaydolur.
2. **git KULLANMA** (add/commit/push/pull yok; ana ajan toplu commit eder). Başka bölümün dosyasına dokunma.
3. CPU 4 çekirdek ve **paylaşımlı** (3–4 kişi çalışıyor): önizlemeyi gereksiz tekrarlama (`-k 2`, kontak sayfası 1×), tam çözünürlüğü yalnız ince ayarda iste; uzun işleri arka planda çalıştır, ön planda `sleep` kullanma.
4. Bitirince `notlar_cK.md` yaz: (a) çekim listesi özeti, (b) bilinen kusurlar, (c) ekrana koyduğun olgular + kaynak sınıfı, (d) ana ajandan istediğin ortak-kit değişikliği, (e) qa_flow çıktısı (kapılar).

---
## 3. Zaman çapaları ve sahne dosyası biçimi

```python
"""c7 — 26 Nisan 1478 ..."""
from shots import shot
import cilt_medici as CM            # türleri kaydeder (ckind'ler)
import cilt_kinds, cilt_pano, cilt_anim, cilt_build   # ihtiyacın olanları import et (pano/figür/yapım türleri)

SHOTS = [
    shot("skyline", ("c7s1", -0.2), cam=("crane", "down", 220), tr=("yikama", 0.9), link="material", label="Pazar sabahı skyline", kick="26 NİSAN 1478 · PAZAR"),
    shot("pano", ("c7s2", 0), pano="nave", cam=("track", "nef_boyunca"), tr=("zoomthru", 1.0, dict(at=(890, 510))), link="scale", longtake=True, label="nef"),
    ...
]
YIL_AT = [(("c7s1", 0), 1478)]
```
- `shot(kind, a, tr=None, label="", cam=None, link=None, longtake=False, montage=False, **tür_parametreleri)`: `a` = çekimin başlangıç çapası; **bitiş = bir sonraki çekimin başlangıcı** (son çekim bölüm sonuna kadar). Çekimler zaman sırasıyla.
- Çapa biçimleri (kamera anahtar karelerinde de): `12.5` (parça-içi saniye — **kaçın**) · `"c7s5"` · `("c7s5", -0.2)` · `("c7s5", "sözcük", ofset)` · `("c7s5", "sözcük", nth, ofset)` (aynı sözcük birden çok geçiyorsa). Sözcük araması aksan/harf büyüklüğüne duyarsız, alt dize eşleşir.
- Çekim içinde zaman: `cx.t` (yerel sn), `cx.at(anchor, key=None, off=0)`, `cx.amt(anchor, dur)` (0→1 yumuşak ilerleme), `cx.fade(i,o)`, `cx.pulse(hz)`, `cx.u`, `cx.dur`, `cx.seed`. Şablon parametrelerinde `at=("c7s5","bıçak",-0.1)` doğrudan verilir.
- **`lead`:** yeni geçişlerde (iris/slide/zoomthru/carry/light/candle) gelen çekimin yerel saati geçiş başlarken doğar; anlatı çapaları etkilenmez, ama **mutlak yerel saniyeler lead kadar erken gelir** — çapa kullan.
- Her çekime `label=` ver (denetim ve kontak sayfası için). Bilinmeyen geçiş adı / geçersiz `cam=` / çözülemeyen çapa Program kurulurken hata verir (preview_chapter hatayı açıklar).

**Ritim:** hedef çekim uzunluğu ağırlığa göre (rehber §4): vuruş 4–7 sn · açıklama/sayı 3–5 · yıldız an 8–14 (tek sürekli kamera, `longtake=True`) · ağır sahne 6–12 · mizah 2–3,5. 16 sn üstü yalnız `longtake`. 1,2 sn'den kısa çekim yok. Her cümlede ≥1 görsel olay. Üst üste ≥3 aynı tür yok (`montage=True` bilinçli seri istisnası). Bölüm başı (kartın hemen ardı) güçlü görselle açılır; bölüm sonu **kapı** çekimi bir sonrakinin ilk görüntüsünü ima eder.

---
## 4. Kamera ve geçişler (özet; ayrıntı: notlar_yonetmen_motoru.md)

- `cam=` **her çekimde açık** yazılır: `("push", 0.08)`, `("pull", 0.08)`, `("pan", "r"|"l", px[, dict(hand=1.5)])`, `("crane", "up"|"down", px)`, `("orbit", derece)`, `"hand"`/`"hand2"` (el kamerası; `hand2` yalnız Pazzi/Roma 1527/9 Kasım gibi dramatik kırılmalarda), `("rack", (x1,y1), (x2,y2)[, dict(at=…, dur=…, r=…)])`, `("track", yol_id)`, anahtar kareli `[(çapa, (x, y, zoom, rot)), …]`. `pan r` = kamera sağa gider, içerik sola akar.
- `pano`/`build` türleri **kendi kamera yolunu** kullanır (cam= uygulanmaz); `map` için `view=(lon,lat,zoom)`.
- Geçişler: `tr=(ad, süre ≤1,0[, opts])` — `yikama, sayfa, giornata` (malzeme) · `iris` (nesne ekranı doldurur: `obj="florin|palle|sun|moon|dome|lens|seal"`, `at`, `r` elle eşle) · `slide` · `zoomthru` · `carry` (`strip="ribbon|ink|banner|paper"`) · `light` · `candle` · `dip` (yalnız ölüm/zaman uçurumu) · `whip` (yalnız savaş/aksiyon) · `fade` (çıplak; bölümde ≤1, sayfa/pigment dışı nefes yerinde).
- **Her geçişe `link=` yaz:** `shape|color|dir|cam|scale|carry|light|material|audio` (gerekçeli geçiş ≥%70; çıplak fade ≤%10). Giden çekimin hareketi geçişte DEVAM eder, gelen çekim aynı yönde başlar — yön sözleşmesi: yükseliş/Medici **soldan sağa ve yukarı**, düşüş/tehdit **sağdan sola ve aşağı** (bölümde ≤1 bilinçli kırılma).

---
## 5. Çekim türleri kataloğu (`shots.KINDS`; 27 tür)

Parametreleri görmek için: `grep -n "ckind(\"ad\"" cilt_*.py` ve ilgili fonksiyonun imzası/docstring'i. Ortak: `at`/`*_at` çapa kabul eder; `mode="day"|"night"`; `perde` Program'dan otomatik gelir (bölüm perdesi); `seed`.

| tür | ne |
|---|---|
| `title`, `fresco_title`, `chapter_card`, `outro` | başlık kartı / ana başlık / bölüm kartı / bitiş ekranı (son üçü Program ekler) |
| `skyline`, `pano` (florence/nave/corridor), `frieze`, `procession` | Floransa silueti · uzun plan panoramaları · fresk alay frizi · yürüyen Gozzoli alayı |
| `map` | fresk harita (gündüz sıva-kâğıt / gece lapis); Şarlken `map` parametreleriyle uyumlu; `view=` + kamera ön ayarı |
| `build` (dome/uffizi) | zaman atlamalı yapım (çapa aralığında 0→1) |
| `medal`, `medals`, `emblem`, `palle`, `coin`, `iconrow` | bronz portre madalyası/yan yana madalyalar · tek simge · Medici arması (altı top) · dönen florin · simge sırası |
| `doc`, `letter`, `ledger`, `quote` | belge (mühür) · mühürlü mektup · defter (tüy kalem satır satır) · alıntı kartı |
| `counter`, `bars`, `stacked`, `timeline`, `tree`, `network` | sayaç · çubuk · parçalı çubuk · yıl cetveli · soy ağacı · ortaklık/akrabalık ağı |
| `black`, `cephe` | siyah yer tutucu · (eski Şarlken türü; kullanma) |

**Figür/insan hareketi, diorama ve yeni türler: §7.**

---
## 6. Görsel dil (Medici cildi: "fresk ve defter")

- Gündüz: sıva-kâğıt duvar, mürekkep, pigment; gece: lapis/kor, yaldız. Perde paleti rehber §5: ALTIN sıcak altın+sıva beyazı; BEDEL gece/şafak lacivert gölge + kızıl vurgu; MİRAS gün batımı/umber/soluk altın (c16 = c0'ın ışığı).
- Yazı: Cinzel (başlık, geniş `track`), Cormorant Garamond (etiket/alıntı), EB Garamond (gövde). Ana yazı ≥40 px, etiket ≥26 px, ikincil ≥22 px; kenarlardan ≥90 px içeride; aynı anda ekranda ≤2 satır "başlık" (belge/alıntı hariç).
- Hareket dili: yavaş itme/çekme, paralaks, toz/kıvılcım/duman; yazılar **yazılır/oyulur/damgalanır** (0,3 sn "çarpma"); sayaçlar sayar; hiçbir yazı ölü durmaz (hafif nefes).
- **Yasak:** düz beyaz zemin, sistem yazı tipi, clipart hissi, neon, ekranı dolduran paragraf, kaynak/olgu uydurma, gerçek kişi yüzü/sesi taklidi iddiası (madalyalar stilize), kan/şiddet gösterimi (taşıyıcı mecaz: işaret, gölge, pigment yıkama), Leonardo/Botticelli/Rubens/Gozzoli görsellerinin birebir kopyası (kodla yeniden çizilen temsil).

---
## 7. Dünya, figür ve yapım animasyonu (Lab-B teslimi; ayrıntı + örnek satırlar: `notlar_dunya.md`)

Üç yeni çekim türü + figür kiti (`import cilt_anim as FA`, `cilt_pano`, `cilt_build` — `cilt_kinds4` sonunda otomatik yüklenir; sahne dosyasında ayrıca import etmek gerekmez ama `FA`/`cilt_pano.st_*` kullanacaksan import et). Önizleme: `python3 preview_world.py [ad…]` → `out/frames/world_<ad>.png` ve `out/clips/world_<ad>.mp4` (13 hazır örnek: kit_walk/acts/riders/crowd, procession, pano_*, build_*). **Bu örneklere bak; her tür için örnek `shot(...)` satırı notlar_dunya §1'dedir.**

| tür | ne | önemli parametreler |
|---|---|---|
| `pano` | katmanlı **uzun plan** (≥3 paralaks derinliği, kareaş önbelleği); dünyalar: `florence` (Arno kıyısı, Ponte Vecchio, boya bezleri, tezgâh, revak altında yazan bankacı, Duomo'ya yürüyüş), `nave` (sütun sırası, ışık huzmesi, diz çöken/ayakta kalabalık, çan sarkacı, kaçan figürler), `corridor` (Arno üstünde Vasari Koridoru) | `pano=`, `tod="day|dusk|night"`, `cams=[(çapa,(x,y,zoom)),…]` (x = ana düzlem x'i, başlangıç ≈960), `stations=[dict(x, at=çapa \| at_frac, fn=callable)]` (`stations=[]` = yok), `kick`, `caption` |
| `build` | **kendini kuran** yapı: `dome` (kubbe sıra sıra, çarklı vinç, işçiler; son: fener+haç, iskele söküm, geri çekilme), `uffizi` (iki kanat, kat kat) | `build=`, `p=(çapa_a, çapa_b)` (ilerleme 0→1) ya da sayı, `orbit` (≤12°), `tod`, `kick`, `caption` |
| `procession` | Gozzoli "Magi" frizi: **gerçekten yürüyen** 3 sıra (sancaktar, atlı, sayfa, yaşlı/ruhban, muhafız), paralaks, toz, kuş | `dir="r|l"`, `density`, `mix=dict(rider=…, noble=…, page=…, banner=…, guard=…, elder=…, cleric=…, common=…)`, `speed`, `pan=("r", px)`, `seed` |

**Figür kiti** (kendi çekim türünde — `@CM.ckind("cK_ad")` — ya da `extra=fn(cx)` içinde): `FA.walker`, `FA.actor(kind, x, y, h, t, action=…)` (`idle talk bow kneel point cheer pray write count handshake threat work`), `FA.rider` (at: walk/trot/gallop), `FA.crowd(mode="mill|stand|kneel|cheer|march|run")`, `FA.procession`, `FA.threat` (hançer/şiddet **yalnız siluet jesti**; kan yok), `FA.atmo_birds`. Tipler: `tuccar banker rahip kardinal papa kesis soylu soylu_f asker halk cocuk denizci` (+takma adlar `FA.ALIAS`); `prop=` aksesuar (`staff crosier spear halberd pole book cross torch sack basket dagger quill hammer trowel coin`). Kostüm `seed` ile belirlenir (tekrarlanabilir). Ayrıntı ve kısıtlar notlar_dunya §1.1.

**Kısıtlar / dikkat:** (1) `pano=nave` varsayılan istasyonlarında **çan sarkacı (`st_bell`) var** — c7 (26 Nisan) ve c10 (9 Kasım) için kaynakta çan olayı YOK: `stations=[…]` ile çanı çıkar. (2) Ağır sahnede kalabalık/figür yalnız jest/siluet; kan yok. (3) Figürler yandan "kesme-bebek": yakın plan yüz için `medal`/madalya portresi kullan. (4) Yok/eksik (notlar_dunya §4–5): giostra çekimi (c6), dikey kule panosu, **gemi/deniz/liman** ve **iç mekân (oda/sokak/meydan/kale)** dünyaları (ayrı laboratuvarlarda yazılıyor: `cilt_deniz.py`, `cilt_oda.py` — hazır olunca buraya eklenir), veba renk solması. (5) Performans: pano/build/procession 100–175 ms/kare; `kit_crowd (58 kişi)` en ağır.

---
## 8. Ses–görüntü kilidi

- Görsel olaylar sfx kuyruğuna girer: müzik/efekt hattı (`muzik.py`, `sfx.py`, `miks.py`) geçiş türlerinden **otomatik** ses türetir; çekime `sfx=` ipucu verebilirsin (sözleşme: müzik ajanının `notlar_ses.md`'si; teslimden sonra buraya eklenecek). Ses köprüsü/J-kesme gereken yerleri `yonetmen_cK.md` "Ses köprüleri" satırına yaz.
- sfx kuyruğu için küresel zaman: `Shot.origin + cx.t` (lead dikkate alınır).

---
## 9. Teslim ve kapılar

- Teslim = `scenes_cK.py` + `yonetmen_cK.md` + `notlar_cK.md` + **kontak sayfasını gözle onay** + `python3 preview_chapter.py cK --flow` (kapılar: durgunluk ≤1,5 sn, kamera %100, gerekçeli geçiş ≥%70, çıplak fade ≤%10, tür tekrarı ≤2, çapa ≥%90, olay yoğunluğu ≥%95, yön, altyazı bölgesi) + `--check` (ms/kare ≤450; yavaş çekimde pişirme/önbellek).
- Ana ajan her bölümü gözle inceler (kontak sayfası + kısa klip); kapıları geçmeyen bölüm iade edilir.
- Performans: kare başına hedef ≤450 ms (tek çekirdek, post dahil). `dyn()` içinde bulanıklık/degrade/ışık huzmesi çizme; statik katmana pişir. Önbellek anahtarlarını `seed`/parametreyle kur.
