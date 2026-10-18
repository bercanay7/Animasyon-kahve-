# ŞARLKEN — Stil Rehberi ve Teknik Sözleşme

Bu belge, "Zaman Kuryesi — Şarlken (21 dk, 16:9, 1920×1080, 24 fps)" videosunun görsel katmanını yazan herkesin (insan/ajan) uyacağı sözleşmedir.
Anlatım sesi **bitmiştir ve değişmez** (`out/timeline.json`: 174 cümle, sözcük düzeyinde zaman). Görseller bu zamana *çapalanır*.

Kullanıcının tek şartı: **"oldukça uğraşılmış ve profesyonel gözükmesi."** Bu, "karanlık mum ışığı + altın kabartma + kâğıt-tiyatro siluet" stilinde, sinematik bir belgesel hissi demek: sıradan slayt/ppt görünümü YOK, her çekimde ışık, derinlik, hareket, doku olacak.

---
## 0. Hızlı başlangıç (5 dakikada çalıştır)

```bash
cd /home/user/Animasyon-kahve-/gunluk-shorts/sarlken-uzun-dosya
python3 preview_chapter.py c3 --script        # bölümün cümleleri + kimlik + zaman (çapa seçmek için)
python3 preview_chapter.py c3 --check         # çekim listesi, uyarılar, ms/kare ölçümü
python3 preview_chapter.py c3                 # kontak sayfası → out/frames/c3_sheet_1.png  (MUTLAKA Read ile görüntüle!)
python3 preview_chapter.py c3 --shots 4,5 -k 4   # yalnız bu çekimler, çekim başına 4 kare
python3 preview_chapter.py c3 --at 283.4      # tam çözünürlüklü tek kare (global saniye) → out/frames/c3_t283.4.png
python3 preview_chapter.py c3 --clip 280 6    # 6 sn'lik küçük mp4
```
Örnek sahne dosyası: `scenes_c0.py` (en kısa yol: onu kopyalayıp düzenle). Boş çekim listesi olan bölümler siyah yer tutucu gösterir.
**Python'u `python3 -I` ile ÇALIŞTIRMA** (modül yolu bozulur). Çalışma dizini her zaman bu klasör.

---
## 1. Video ve anlatı özeti

- Konu: V. Karl (Şarlken, 1500–1558), Kutsal Roma İmparatoru + İspanya Kralı. Ana tez: **"beş cephe, tek adam"** — bankacı (0), keşiş/Reform (1), kral/Fransa (2), sultan/Osmanlı (3), miras (4).
  Beş cephe simgesi sağ üstte **HUD** olarak çıkar (`compose.py` otomatik; bölüme göre yanar). Sen HUD çizmezsin; sağ üst 420×110 px ve sol üst (bölümün ilk 5,5 sn'si) 800×90 px alanı boş bırak.
- Bölüm kartları (3 sn sessizlik) ve ana başlık (c1 öncesi) `compose.py` tarafından eklenir. Sahne dosyası yalnız bölümün KENDİ çekimlerini içerir.
- Ses: ElevenLabs, "Emrullah Uzun". Altyazı ayrı (SRT/ASS) — **ekrana altyazı basma**; ekrandaki yazılar anlatıyı tamamlar, tekrar etmez.
- Kaynak sınıfları (kanal anayasası): CONFIRMED / NİTELİKLİ / **ANEKDOT** ("rivayete göre" diye anlatılır) / YORUM / HAFIZA. Anlatıdaki her "rivayet/sonradan eklenmiş/tutanakta yok" cümlesi için ekranda **damga** (`stamp`) kullan: RİVAYET, TUTANAKTA YOK, SONRADAN, TARTIŞMALI, YAKLAŞIK. Anlatının söylediğinin ÖTESİNE geçen sayı/tarih/ad yazma.
- Sayılar ve adlar ekrana, anlatıda **söylendiği anda** gelir (çapa: sözcüğün 0,1 sn öncesi). Yazım: Türkçe karakterler (İ ı Ş Ğ Ü Ö Ç) doğru, sayılar nokta ayraçlı (850.000), tarihler "23 Ekim 1520".
- Araştırma tabloları (olgu doğrulama): `arastirma/*.md`. Ekrana yeni bir olgu koyacaksan oradan al; emin değilsen koyma.

---
## 2. Dosya haritası ve SAHİPLİK KURALLARI

| Dosya | Ne | Kim düzenler |
|---|---|---|
| `sk.py` | Skia çekirdek: Frame, yazı, rölyef/altın, efektler, post, easing, palet | **ana ajan** (sen düzenleme) |
| `shots.py` | çekim şablonları (`@kind`), `shot()`, `Ctx`, yardımcı çizimler | **ana ajan** |
| `compose.py` | Program: çekimleri zamana yerleştirir, geçiş, bölüm kartı, HUD, kapanış | **ana ajan** |
| `stage.py`, `scenes_lib.py` | diorama motoru, siluet figürler, salon sahnesi | **ana ajan** (figür türleri: figür-lab `figs_lab.py` ile; sahne aileleri: sahne-lab `scenes_sea.py/scenes_field.py/scenes_siege.py`) |
| `mapsk.py`, `mapdata.py` | harita çizici/veri | **ana ajan** |
| `medal.py`, `icons.py` | madalya portreleri, kabartma simgeler | **madalya-lab** (yalnız EKLEME yapar) + ana ajan; yeni kişi/simge: `medal_extra.py`, `icons_extra.py` |
| `scenes_cK.py` | **bölüm K'nın çekim listesi** (`SHOTS = [...]`) | bölüm yazarı (yalnız kendi bölümün) |
| `scenes_<aile>.py`, `stage_<ad>.py`, `icons_<ad>.py`, `figs_<ad>.py` | senin eklediğin YENİ modüller | ekleyen |

**Kurallar**
1. Ortak dosyaları (yukarıdaki "ana ajan" satırları) DÜZENLEME. Eksik bir yetenek için kendi modülünde yaz; ortak API'lere dışarıdan kanca vardır:
   - Yeni diorama sahnesi: kendi modülünde `import scenes_lib as SL` → `@SL.sc("ad") class X: layers(), dyn()` (örnek: `scenes_lib.Hall`). Modül, `scenes_cK.py` içinde `import` edilerek kaydolur.
   - Yeni çekim türü: `import shots as SH` → `@SH.kind("ad") def k_x(cx, **params)`. (Ad çakışmasın: `"c3_villalar"` gibi bölüme özel öntek kullan.)
   - Yeni siluet figür türü: `import stage as ST` → `@ST.fig("ad") def f(h, lean) -> skia.Path` (ayak (0,0), yukarı −y, boy h). İç ayrıntılı/degradeli zengin figür: `@ST.figx("ad") def f(h, lean): return sınır_yolu, çiz(canvas, col, rim)`. Kayıt kaydı otomatik: `figs_lab.py`/`figs_war.py` stage'e, `scenes_sea/field/siege/rooms.py` scenes_lib'e, `medal_extra.py`/`icons_extra.py` shots'a otomatik yüklenir (hata olursa uyarı basılır, kit bozulmaz). Kendi modülün için `sk.optional_import("ad")` kullanabilirsin ya da doğrudan `import` et.
   - Yeni harita bölgesi: `shots.mapview().add_region("ad", [[(lon,lat),...], ...])`.
   - Yeni madalya kişisi: `medal.PEOPLE["anahtar"] = dict(...)`, `medal.INSCR["anahtar"] = "..."` (madalya-lab bunu `medal_extra.py` içinde yapar; sen okuyup kullan).
2. **git KULLANMA** (commit/push/pull yok; ana ajan toplu commit eder). Başka bölümün dosyasına dokunma.
3. Aynı anda 6–7 kişi çalışıyor, CPU paylaşımlı: önizlemeyi gereksiz tekrarlama; `-k 2` yeterli, tam çözünürlüğü yalnız ince ayarda iste.
4. Bir bölümü bitirdiğinde `notlar_cK.md` yaz: (a) çekim listesi özeti, (b) bilinen kusurlar, (c) ekrana koyduğun olgular ve kaynak sınıfı, (d) ana ajandan istediğin ortak-kit değişikliği. Ana ajan bunu okur.

---
## 3. Zaman çapaları ve sahne dosyası biçimi

```python
"""Bölüm 3 — ..."""
from shots import shot
import scenes_lib      # theatre şablonunu kaydeder (diorama çekimi kullanacaksan şart)
import icons, sk
from sk import W, H

SHOTS = [
    shot("map", a=("c3s3", -0.3), tr=("fade", 0.8), cams=[(0.0, (-4, 41, 3.0)), (("c3s4", 2.0), (-5, 41.5, 4.0))],
         regions=[dict(name="ispanya", color="ispanya", at=("c3s3", "Komünero", 0.0))],
         cities=[dict(lon=-5.1, lat=41.7, name="VILLALAR", kind="battle", at=("c3s4", "Villalar", 0.0))], label="villalar_harita"),
    shot("theatre", a=("c3s5", -0.2), scene="field", cams=[...], p=dict(...), label="idam"),
    ...
]
```
- `shot(kind, a, tr=None, label="", **params)`: `a` = çekimin başlangıç çapası. **Bitiş = bir sonraki çekimin başlangıcı** (son çekim bölüm sonuna kadar sürer). Çekimler zaman sırasıyla verilir.
- Çapa biçimleri: `12.5` (bölüm başından değil **global** sn — kaçın), `("c3s5", -0.2)` (cümle başlangıcı ± ofset sn), `("c3s5","Padilla",0.0)` (cümledeki sözcüğün başlangıcı ± ofset; sözcük alt dize eşleşir, aksan/harf büyüklüğüne duyarsız), `("c3s5","Padilla",1,0.0)` (aynı sözcüğün 2. geçişi).
- Çekim içinde zaman: `cx.t` (yerel sn), `cx.at(anchor, key=None, off=0)` → yerel sn, `cx.amt(anchor, dur)` → 0→1 yumuşak ilerleme, `cx.fade(i,o)`, `cx.pulse(hz)`, `cx.u` (0..1 çekim ilerlemesi), `cx.dur`.
  Şablon parametrelerinde `at=("c3s5","Padilla",-0.1)` gibi çapalar doğrudan verilir.
- Geçiş `tr=("fade"|"dip"|"zoom"|"whip"|"wipe", süre)` **bu çekimin GİRİŞİ** içindir (önceki çekimle örtüşür; süre ≤ 1,0 sn). Varsayılan `("fade", 0.7)`. `dip`: zaman atlaması/ölüm/ağır an; `whip`: savaş/aksiyon; `zoom`: ifşa; `wipe`: harita↔harita kıta değişimi.
- Her çekime `label=` ver (denetim çıktısı ve kontak sayfası için).

**Ritim kuralları**
- Hedef çekim uzunluğu 3–8 sn (ort. ≈ 6 sn); **16 sn'yi aşma**; uzun cümlede ikinci çekim/kamera hareketi/yeniden çerçeve koy. 1,2 sn'den kısa çekim yok.
- Her cümlede en az bir **görsel olay** (yeni öğe, kamera hareketi, sayı, damga) olsun; hiç hareket etmeyen kare yok (en az yavaş itme/çekme %4–8).
- Üst üste 3'ten fazla aynı tür çekim koyma (map, map, map, map → kötü). Türleri harmanla: diorama ↔ harita ↔ madalya ↔ belge ↔ sayı ↔ alıntı ↔ zaman çizgisi ↔ simge.
- Bölüm başı güçlü bir görselle açılır (bölüm kartından sonra ilk 3 sn); bölüm sonu bir "vurgu çekimi" ile kapanır (damga/simge/sayı).

---
## 4. Görsel dil

**Palet** (`sk.PAL`, `sk.FAC`): zemin `#0D0704–#24160D` (sıcak kara), altın `#C9962B` / `#F0D27A` / koyu `#7A5518`, parşömen `#EBDDB5`, Habsburg kırmızısı `#8E1F26`, deniz `#0E1A24–#27455C`.
Cephe/hanedan renkleri `FAC`: habsburg/ispanya kırmızı, burgonya bordo, avusturya turuncu-kırmızı, fransa mavi `#27427A`, osmanlı yeşil `#2F6B4A`, papalik altın-sarı `#D4B64E`, protestan petrol `#1E5560`, venedik turkuaz `#2F7A8A`, ingiliz `#A8352C`, portekiz `#2D5A8E`.
**Madalya metal kodu**: gold = Habsburg ailesi; royal = Fransa; forest = Osmanlı; violet = Papalık/Kilise; teal = Reform (Luther, Melanchthon, Saksonya); crimson = İngiltere; bronze = bankerler, fatihler, Yeni Dünya; silver = diğer/tarafsız; ivory = sanatçı/yazar; onyx = yas/ölüm (seyrek).
**Yazı tipleri** (`face=`): `title`/`title_m`/`title_l` (Cinzel — başlık, büyük harf, geniş `track`), `cap`/`cap_b`/`cap_i` (Cormorant Garamond — etiket/altyazı/alıntı), `body`/`body_i` (EB Garamond), `fell`/`fell_i` (IM Fell — belge/parşömen), `map`/`map_i` (IM Fell English — harita).
**Boyut/okunabilirlik (1080p)**: ana yazı ≥ 40 px, etiket ≥ 26 px, en küçük ikincil metin ≥ 22 px; metin kenarlardan ≥ 90 px içeride; aynı anda ekranda ≤ 2 satır "başlık" (belge/alıntı hariç); gölge/koyu zemin olmadan açık zemin üstünde açık yazı yok.
**Hareket dili**: yavaş itme/çekme, hafif paralaks, süzülen toz/kıvılcım/duman; yumuşak giriş-çıkış (`ease_io`, `smooth`); yazılar 0,5–0,9 sn'de belirir, damgalar 0,3 sn'de "çarpar" (`back_out`), sayaçlar `ease_out` ile 1,6 sn; rotalar çizilir (prog); hiçbir şey ani belirmez.
**Işık**: tek sıcak ışık kaynağı (pencere/mum), kenar ışığı (rim), vinyet; yüksek kontrast, derin siyahlar. `post()` zaten ışıma+renk+gren ekler.
**Yasak**: düz beyaz zemin, varsayılan sistem yazı tipi, clipart hissi, çok renkli neon, ekranı dolduran paragraf, kaynak/olgu uydurma, gerçek kişinin sesini/yüzünü taklit etme iddiası (madalyalar stilize "madalya portresi"dir, fotoğraf değil).

---
## 5. Çekim türleri kataloğu (`shots.py`)

Ortak: `at`/`*_at` parametreleri çapa kabul eder; renkler hex veya `FAC` adı; `extra=fn(cx)` ile çekime özel ek çizim eklenir.

| tür | parametreler (varsayılan) | not |
|---|---|---|
| `title` | text, sub, kick, at, size=190, glow, face, rays, sub_at, kick_at, y=0.52 | büyük altın başlık; tarih kartı/ana başlık |
| `emblem` | icon, metal, size=460, at, kick, sub, caption, stampt=(metin,x,y,çapa[,boyut]), pos, extra | tek büyük kabartma simge + damga |
| `medal` | key, metal, name, role, dates, pos="c"/"l"/"r", size=700, at, plate_at, note, stampt, zoom, extra, flip | tek madalya portresi + isim levhası |
| `medals` | items=[dict(key,name,role,dates,at,metal,flip)], size, y, gap, title, vs (çapa → ortada kılıç simgesi), plates | yan yana madalyalar (karşılaştırma/rakipler) |
| `doc` | title, lines=[str \| (str, çapa)], w=1100, h=760, at, line_dt, seal, seal_at, hl=(x,y,w), hl_at, date, caption, stampt, pan, align, tone | yırtık parşömen + satır satır mürekkep + mühür |
| `quote` | text, who, src, at, size=64, stampt, face, mark, wrap, pos | büyük alıntı kartı |
| `counter` | value, unit, label, icon, at, dur, sub, size, prefix, suffix, decimals | sayan büyük sayı |
| `bars` | items=[(etiket,değer,renk[,çapa])], unit, title, maxv, valfmt | yatay çubuklar |
| `stacked` | parts=[(etiket,değer,renk[,çapa])], total_label, total, title | parçalı tek çubuk (örn. 850.000 = 543.000 + kalan) |
| `timeline` | a0, a1, events=[(yıl,etiket[,çapa,renk])], hl=(y0,y1,etiket[,çapa]), step, title | yıl cetveli, vurgulu aralık |
| `tree` | nodes=[dict(id,key\|icon,name,dates,x,y,at,metal,size,tag)], edges=[(a,b,çapa[,renk])], title | soy ağacı (madalyalar) |
| `map` | cam=(lon,lat,zoom) \| cams=[(çapa,(lon,lat,zoom)),…], style="night"\|"paper", regions, cities, routes, labels, icons_, notes, date, frame, compass, tint, approx, kick, extra(cx,cam,mv) | aşağıda ayrıntı |
| `iconrow` | items=[dict(icon,label,sub,at,metal)], title, size, y, hl | simge dizisi (beş cephe vb.) |
| `cephe` | fronts, now | beş cephe sahnesi |
| `theatre` | scene, cams=[(çapa,(x,y,zoom)),…], p=dict(...), vig, dust_n, overlay=fn(cx), fade_in, tint | **paralaks diorama** (aşağıda) |
| `black` | text | siyah ekran (+metin) |

`map` ayrıntı: `regions=[dict(name,color,at,alpha=.62,hatch,glow)]` (bölge adları aşağıda), `cities=[dict(lon,lat,name,kind="town|capital|battle|siege",at,side="r|l|t|b",size)]`,
`routes=[dict(pts=[(lon,lat),…],at,dur=1.8,color,width=5,dash=(10,8),label,arrow)]`, `labels=[dict(text,lon,lat,size,color,at,face,track,rot,swz)]`,
`icons_=[dict(kind=<simge adı>,lon,lat,size=70,at,metal,rot,bob)]` (rotada hareket için `route=[…], move_at, move_dur`), `notes=[dict(text,x,y,at,w,size,sub,align)]` (levha), `date="1555"` veya `(metin, çapa)`.
Kamera: zoom 1 = 32 px/derece; Avrupa genel ≈ 1.2–1.7, Akdeniz ≈ 2, tek ülke ≈ 3, şehir ≈ 6–8; Atlantik/Yeni Dünya ≈ 0.5–0.7. Büyük zoom değişiminde `cam_move` merkezi kendiliğinden karıştırır.
**Harita bölgeleri**: ispanya, napoli, napoli_kara, sicilya, sardunya, milano, papalik, venedik, hollanda, franche_comte, savoya, fransa, avusturya, bohemya, macar_habsburg, macar_osmanli, erdel, almanya, isvicre, britanya, irlanda, portekiz, osmanli_1520, osmanli_1550, osmanli_vassal, fas, cezayir, tunus, trablus, misir, aztek, yeni_ispanya, inka, peru_ispanya, brezilya, karl_kendi (Karl'ın doğrudan toprakları), ferdinand (Ferdinand'ın toprakları). Eksik bölge → `add_region` (bölüm 2). Sınırlar yaklaşıktır; `approx=True` altına "SINIRLAR YAKLAŞIKTIR" notunu koyar.
**Hızlı performans**: harita zemini döşeme önbelleğidir (kıyı/dalga/ışıma bir kez pişer). Bölgeler ve rotalar kare başına çizilir (≈6–11 ms/bölge) — aynı karede 8'den fazla bölgeyi aynı anda gösterme.

**Madalya anahtarları** (`medal.PEOPLE`): karl_genc, karl_olgun, karl_yasli, fransuva, henri8, luther, melanchthon, suleyman, barbaros, fugger, klemens, felipe2, juana, isabel (Portekizli İsabel, Karl'ın eşi), ferdinand (Karl'ın kardeşi), maksimilyan, kortes, pizarro, lascasas, moritz, orange, margareta, tiziano, durer, elkano, makedonya.
**Madalya-lab ekleri** (`medal_extra.py`; hazır olunca otomatik gelir, o zamana dek yedek yüz görünür, isim levhası yine doğru): filip (Yakışıklı Filip), fernando (Aragonlu Fernando), maria_burgonya (Burgonyalı Maria), isabel_kastilya, padilla, bravo, maldonado, maria_pacheco, frederik_bilge (Saksonya Seçmeni Frederik), johann_friedrich (esir Saksonya Seçmeni), louise_savoy, catherine_aragon, lajos2, zapolya, doria, atahualpa, magellan, sepulveda, moctezuma, welser, mary_macar (Karl'ın kız kardeşi Mary).
**Simgeler** (`icons.names()`): anchor, book, cannon, castle, coin, coinbag, coins, crescent, cross, crown, eagle, family, fleur, hourglass, imperial_crown, keys, laurel, monk, pyramid, question, quill, ring, scales, scroll, shield, ship, skull, star, sword, swords, torch, tower. Madalya-lab yeni simgeler ekler (`icons_extra.py`: press, chest, globe, compass, helmet, horse, gun, flag, candle, sun, feather, bell, ballot, gavel …).
Çizim: `icons.draw_icon(f, ad, x, y, size=120, metal="gold", alpha=1, rot=0, shadow=True, glow=0, flip=False)`; `metal`: gold bronze silver ivory crimson royal forest violet onyx teal.

---
## 6. Diorama ("kâğıt-tiyatro") sistemi

`theatre` çekimi: `shot("theatre", a=…, scene="hall", cams=[(çapa,(x,y,zoom)),…], p=dict(...))`. Kamera koordinatı sahne tuvali (1920×1080, merkez 960,540); zoom 1.0 = tam çerçeve; 1.5–2.2 yaklaşma.
Sahne = **katman listesi** (arkadan öne, her katman bir kez "pişirilir" → skia.Image, kare başına yalnız dönüşüm): derinlik `d`: 0 = sonsuz uzak (kaymaz), 1 = odak düzlemi, >1 yakın (daha çok kayar/büyür). Pişirme tuvali 1920×1080 + her yana 220 px pay (`MARGIN`).
Yeni sahne yazımı:
```python
import scenes_lib as SL, stage as ST, sk
from stage import MARGIN
@SL.sc("kule")
class Kule:
    def __init__(self, p): self.p = p
    def layers(self):                       # [(derinlik, fn(f))] — BİR KEZ çağrılır, ağır çizim burada serbest
        def L0(f): ST.sky_gradient(f, "#2A1A12", "#0D0704"); ...
        def L1(f): ...
        return [(0.1, L0), (0.5, L1), (1.0, L2), (1.4, L3)]
    def dyn(self):                          # {katman_idx: fn(f, t)} — HER KARE; yalnız küçük/ucuz öğeler
        def D2(f, t): ST.figure(f, "noble", 960, 900, 420, sway=math.sin(t)*0.01)
        return {2: D2}
```
**Kare bütçesi**: tüm kare ≤ 250 ms (ort. hedef ≈ 130). `dyn` içinde ASLA: bulanıklık/`blur=`, ışık huzmesi (`god_rays`/`light_rays`), tam ekran degrade, büyük path+blur. Bunların hepsini `layers()` içine (statik) koy. `dyn` yalnız: figür (önbellekli sprite), alev/kıvılcım/duman parçacığı (≤ 60 öğe), dalgalanan sancak, küçük ışıltı.
Yağmur/kar/duman/kor: `sk.rain(f,t,n,…)`, `sk.snow`, `sk.smoke(f,x,y,t,…)`, `sk.embers`, `sk.dust` — `overlay=` ya da `dyn` içinde çağır (ucuzdur).
**Stage ilkelleri** (`stage.py`): `arch, column, gothic_window, banner, floor_hall, dais, throne, chandelier, candle_flames, god_rays(pişirmede!), sky_gradient, hills, skyline, pines, sea_layers(statik), carrack`, figürler `figure(f, kind, x, y_ayak, h, col, rim, face=±1, alpha, sway, rot, lean, bob)`, `crowd(f, rows, x0, x1, y0, dy, h0, hs, kinds, …)`.
Figür türleri: noble, merchant, cardinal, scribe, monk, woman, emperor_old, prince, page, pikeman, landsknecht, janissary, knight, conquistador, sailor, native, seated, kneel, pair_old_prince — figür-lab geliştirir ve yenilerini ekler (ad aynı kalır).
Mevcut sahneler (`scenes_lib.py`): `hall` (Gotik saray salonu; p: crowd, emperor, emp_xy, emp_h, walk, throne, glow0, glow1, warm, extra).
**Planlanan sahne aileleri** (sahne-lab `scenes_sea.py` / `scenes_field.py` / `scenes_siege.py`, oda-lab `scenes_rooms.py`; hazır olunca API'leri `SAHNE_KATALOGU_deniz_savas.md` ve `SAHNE_KATALOGU_odalar.md` içinde belgelenir — **dosya yoksa/sahne kayıtsızsa çekim yer tutucu ("[sahne: ad — henüz yok]") çizer, Program yine çalışır; sahne gelince yeniden önizle**). Kamera `cams=[(çapa,(x,y,zoom)),…]` hepsinde aynıdır. Planlanan ad ve ana `p` anahtarları:
- `sea`: `mood="calm|dawn|dusk|night|storm"`, `ships=[dict(kind="carrack|galley|fishing", x=0..1, row=0..2, s=1.0, flag="#hex", heading=±1, rock=0..1, sink=0..1, burn=0..1)]`, `coast=None|"tazones"|"africa"|"harbor"`, `lightning`, `rain`, `moon`.
- `field`: `ground="plain|marsh|river|hills"`, `weather="clear|fog|rain|dawn|dusk|snow"`, `armies=[dict(side="#hex", kind="pike|cavalry|arquebus|peasants|mixed", x, row, n, dir=±1, charge=0..1)]`, `banners`, `smoke`, `river`, `castle_far=None|"pavia"|"toledo"`.
- `siege`: `city="roma|viyana|guns|halkulvadi|tenochtitlan|toledo"`, `time="day|dusk|night"`, `fire=0..1`, `weather`, `cannon_fire`, `ladders`.
- `tower` (`variant="tordesillas|cell|wartburg"`, `night`, `figure="woman|man|writer|none"`, `candle`), `counting_house` (`coins`, `clerks`), `ransom_room` (`fill_t=(t0,t1)` yerel sn), `cloister` (`time`), `bedroom` (`candle`, `fade_candle_t`), `chapel` (`coffin`), `reichstag` (`monk`, `books`, `emperor`), `debate_hall` (`lecterns=2`), `electors_hall` (`seats=7`), `aachen` (`crown_t`), `road_night` (`litter`, `riders`, `rain`, `mountains`).
Animasyon parametreleri çekim-yerel saniye alır (`fill_t=(1.0, 6.0)` = 1. ile 6. sn arasında dolar).
Siluet renk dili: figürler `#0C0705`'e yakın (koyu), kenar ışığı sıcak (`rim="#C58A44"`), uzak katmanlar sisle (`ST.fog`) açılır. Işık kaynağı olan her sahnede `f.circle(… shader=f.rad(…), blend=skia.BlendMode.kPlus)` ile sıcak parıltı.

---
## 7. Çekim tasarım tarifleri (hangi cümle → hangi çekim)

- **Kişi ilk kez anılır** → `medal` (isim levhası + rol + yıllar) ya da çok kişiyse `medals`; metal kodu yukarıda.
- **Karşılaştırma/rakipler** → `medals` + `vs=` kılıç. **Soy/akrabalık** → `tree`.
- **Tarih/olay + yer** → `map` (zoom-in + şehir işareti + tarih damgası) ardından o yerde `theatre`.
- **Hareket/seyahat** → `map` rotası (`routes`), üzerinde `icons_` ile gemi/at (`route=` ile ilerler).
- **Sayı** → `counter` (tek sayı) / `bars` (karşılaştırma) / `stacked` (pay) — sayı anlatıda söylenirken sayar.
- **Belge/mektup/ferman/antlaşma** → `doc` (satır satır; vurgulu ifade + mühür). **Sözün kendisi** → `quote` (+ gerekiyorsa RİVAYET/TUTANAKTA YOK damgası).
- **Süre/kronoloji** → `timeline` (vurgulu aralık: "43 YIL", "46 YIL"). **Kavram** → `emblem`/`iconrow`.
- **Savaş/kuşatma/fırtına/yolculuk** → `theatre` (field/siege/sea) + `whip` geçişi; duman/yağmur/kor ekle; kısa kesitler (3–5 sn).
- **Belirsizlik/tartışma** ("tarihçiler tartışıyor") → soru işareti simgesi + TARTIŞMALI damgası; tek kesin görsel çizme.

---
## 8. Teslim kontrol listesi (bölümü bitirmeden önce)

1. `python3 preview_chapter.py cK --check` → **uyarı yok**, tüm çekimler < 450 ms/kare.
2. Kontak sayfalarını **Read ile gör** (out/frames/cK_sheet_N.png): yazı taşması, üst üste binen etiket, kesik madalya, boş/çirkin kare, HUD alanı çakışması, okunmayan küçük yazı, yanlış Türkçe karakter var mı? Düzelt, yeniden bak.
3. Kritik 3–4 çekimi tam çözünürlükte (`--at`) incele (özellikle yazılı olanlar ve haritalar).
4. Anlatıyla senkron: sayılar/adlar söylendiği anda mı geliyor? (`--script` ile karşılaştır.)
5. Rivayet/belirsiz her cümlede damga var mı? Uydurma olgu yok mu?
6. `notlar_cK.md` yaz. (git yok.)
