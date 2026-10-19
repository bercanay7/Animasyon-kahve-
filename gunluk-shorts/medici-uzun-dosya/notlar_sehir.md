# Dış mekân / şehir dünyası — Lab-E notları (19 Ekim 2026)

Sözleşme: `STIL_REHBERI.md` §2 (sahiplik), §7; `YONETMENLIK_REHBERI.md` §2 kamera, §3 geçişler, §5 ışık. Bu iş Lab-A/B/C/D dosyalarına **dokunmaz**; yalnız okur.
Tek değişiklik (izinli): `cilt_kinds4.py` sonundaki korumalı import döngüsüne `"cilt_sehir"` eklendi (`for _m in ("cilt_deniz", "cilt_oda", "cilt_sehir")`).
`python3 -c "import shots, compose"` hatasız; `sehir` türü `shots.KINDS`'e kayıtlı ve `cilt_cam.OWN_CAMERA`'ya çalışma anında eklenir (kendi kamera yolu vardır; pano/build gibi: `cams=` kullanılır, `cam=` ön ayarı yalnız varsayılan yolun üstüne biner).

| dosya | ne |
|---|---|
| `cilt_sehir.py` | `sehir` çekim türü + dünyalar (meydan, sokak, kale/sur, kale/castel, kale/passetto, skyline_dikey) + yeniden kullanılabilir işlevler |
| `preview_sehir.py` | kontak sayfaları `out/frames/sehir_<ad>.png`, klipler `out/clips/sehir_<ad>.mp4`, `--ms`, `--bake`, `--at` |
| `out/_cache/world/sehir_*_<sürüm>.png` | kareaş önbelleği; sürüm = `cilt_sehir.py` içerik özeti (kod değişince eski kareaşlar otomatik silinir/yeniden pişer) |

## Komutlar (proje dizininden; `python3 -I` YOK)
```
python3 preview_sehir.py                       # tüm girdiler: sayfa + klip (2 işçi)  [arka planda çalıştır; ÇİFT çalıştırma: aynı mp4'e iki ffmpeg yazar]
python3 preview_sehir.py meydan_ates --no-clip # yalnız kontak sayfası
python3 preview_sehir.py meydan_ates --at 10.6 # tek tam çözünürlüklü kare → out/frames/sehir_meydan_ates_t10.6.png
python3 preview_sehir.py --ms                  # ms/kare (post dâhil; ortalama/medyan/en az/maks + bölüm dökümü)
python3 preview_sehir.py --bake                # soğuk önbellek kareaş pişirme süreleri
```
Girdiler: `meydan_ates, meydan_odun, meydan_palle, meydan_pencere, meydan_kalabalik, sokak_kapi_gunduz, sokak_kapi_gece, sokak_yuruyus, kale_sur, kale_castel, kale_passetto, skyline_dikey`.

## 1. API — `shot("sehir", a, scene=…, act=…, …)`

```python
shot("sehir", a, scene="meydan", act="ates"|"odun"|"palle"|"pencere"|"kalabalik", tod=None, cams=None, actors=None, stations=None, kick=None, caption=None,
     at=0.0, frame=True, seed=1, band=None, door=None, door_at=None, items_at=None, fire_at=None, fire_dur=None, fire0=0.72, gold_at=None,
     dir="l"|"r", n=24, flags="lily"|"medici"|"stripes"|"cross"|None, riders=0, cam=…, link=…, longtake=…, montage=…)
```
* `tod`: `day | dusk | night`; verilmezse act'e göre: ates→dusk, odun→night, palle→day, pencere→dusk, kalabalik→day, castel→dusk, diğerleri `mode`'a göre (gece modunda night). **Gece/alacakaranlık çekimlerine `mode="night"` ver** (Program post LUT'u buna göre; duvar/çerçeve gece duvarı olur).
* `cams=[(çapa,(x,y,zoom)),…]` pano ile aynı: x = ekran merkezinin ana düzlem x'i (≈960 başlangıç), y = dikey kayma (px, + aşağı), zoom ≥ 1 (0,85'e kadar güvenli). `skyline_dikey`'de **(x, yükseklik_px, zoom)** (yükseklik = ekran merkezinin kule tabanından yüksekliği). `cams` verilmezse act'e özgü, sinematik varsayılan yol çekim süresine yayılır (ease_io uçlarda).
* `cam=("push"|"pull"|"pan","r"|"l",px|"crane","up"|"down",px)` verilirse ve `cams` yoksa varsayılan yolun üstüne uygulanır (`hand/rack/orbit/track` yok sayılır).
* `actors=[dict(kind, x0|x, y, h, dir, speed, action="walk|idle|talk|cheer|point|bow…", seed, prop, flag, phase, t0, stil=dict(robe=…, robe2=…, hat_col=…), gate=(x, w))]`: dünya koordinatında ek figürler (`FA` kiti; speed>0 yürür). `gate`: figür geçide girerken küçülüp kararır (kemerli eşik). `actors=[]` → varsayılan figürler kalkar (sokak yürüyüşünde 3 figür).
* `stations=[dict(x, at|at_frac, fn=callable(ctx, st))]` pano ile aynı (meydan, sokak).
* `items_at=[çapa…]` (ates): eşyaların yığına DÜŞTÜĞÜ anlar (uçuş 0,95 sn öncesinde başlar; her eşyayı bir taşıyıcı sepet/çuvalla getirir, fırlatır, sonra halkaya katılıp coşar). `fire_at`: ilk kıvılcım; `fire_dur`: kıvılcım→inferno süresi (varsayılan 0,40·süre). `door="close"|"open"`, `door_at=çapa` (sokak). `gold_at` (palle): Medici penceresi altına döner.
* `kalabalik`: `dir="l"` (Ciompi tarzı: sağdan sola kabarır) / `"r"` (Cosimo dönüşü tarzı: soldan sağa), `flags` sancak deseni (lily = Floransa zambağı), `riders=n` sağdan sola gelip duran atlılar.

**Örnek satırlar**
```python
# c10 V6 → V7: eşleşmeli kesme (aynı kamera noktası/yığın merkezi PILE_X; V6 kamerası yığın merkezinde sabitlenir, V7 oradan başlar)
shot("sehir", ("c10s20", -0.2), scene="meydan", act="ates", mode="night", items_at=[("c10s20","ayna",0.0), ("c10s20","iskambil",0.0), ("c10s21",0.0)], fire_at=("c10s22","ateş",-0.3), link="light", longtake=True, label="Kibirler yanar")
shot("sehir", ("c10s24", 0.0), scene="meydan", act="odun", mode="night", tr=("light", 0.9, dict(at=(960, 650))), link="light", label="aynı meydan, odun + darağacı siluet")
# c7 V10–V11: atlılar sağdan sola durur, Medici kalabalığı soldan sağa kabarır → altın pencere
shot("sehir", ("c7s24", 0.0), scene="meydan", act="palle", kick="PALLE! PALLE!", link="dir", longtake=True, label="Palle")
shot("sehir", ("c7s27", 0.0), scene="meydan", act="pencere", mode="night", cam=None, link="light", label="pencereler kararır, ip çizgisi + gölge")
# c10 V4 (9 Kasım): kapı tek hamlede kapanır; c7 V4 (Via Larga): üç figür yürür, kemerli eşiğe girer
shot("sehir", ("c10s12", 0.0), scene="sokak", door="close", door_at=("c10s12","bir saat",0.0), tod="day", link="dir", label="9 Kasım kapı")
shot("sehir", ("c7s7", 0.0), scene="sokak", link="shape", label="Via Larga yürüyüşü")      # varsayılan yol: figürleri izler, kemerli eşikte biter
# c11: kuşatma (yün balyalı kule, ufukta çadırlar; kamera yavaş pull) ve Roma 1527
shot("sehir", ("c11s30", 0.0), scene="kale", act="sur", link="scale", label="San Miniato")
shot("sehir", ("c11s12", 0.0), scene="kale", act="castel", mode="night", label="Castel Sant'Angelo")
shot("sehir", ("c11s13", 0.0), scene="kale", act="passetto", link="dir", longtake=True, label="Passetto: papalık heyeti")
# c3: Palazzo Vecchio kulesine tek dikey plan (crane up)
shot("sehir", ("c3s1", 0.0), scene="skyline_dikey", tod="day", link="cam", longtake=True, label="kule")
```

### Sahneler ve act'ler (görsel içerik)
* **meydan** (Signoria): Palazzo Vecchio (bugnato blok, iki sıra bifora, konsollu galeri + mazgal, Arnolfo kulesi: çan odası+çan siluetleri, külah, flama), Loggia dei Lanzi (üç kemer, yonca frizli teras), Medici tarzı palazzo (sol), genel palazzo (sağ), dar ara evler, uzak Duomo/çan kulesi/kuleler (paralaks), meşale demirleri, kaldırım, varil. Katmanlar: gök·tepe·uzak şehir·orta çatılar·ana düzlem·ön plan.
  * `ates`: basamaklı odun piramidi; ayna/iskambil/zar/peruk/çalgı (brif c10 V6'daki beş tür) taşıyıcılarla gelip havadan yığına düşer; ilk kıvılcım → çok dilli alev (degradeli dilimler, 16 kare döngü) → yükselen ateş, kıvılcım, duman (genç topaklar sıcak); ateş ışığı havuzu (alacakaranlık→kor), kalabalık çevrede halka (taşıyıcılar + 24 kişilik halka; ön sıra ateşin önünde), ateşe bakan ön plan siluet başlar. Kamera: yığının etrafında yarım daire paralaksı → yığın merkezinde SABİT.
  * `odun`: aynı kamera/aynı merkez; yığının yerinde dağınık odun + **darağacı SİLUETİ** (dikme+kiriş+payanda; beden/ip/ceset yok); alev söner, kor yatağı titrer ve solar, **kül sağa sürüklenir**, ince duman; halka yalnız siluet (önceden pişirilmiş, sallanır, bir kısmı kolunu kaldırır).
  * `palle`: Medici tarzı palazzonun kalkanı (yalnız bu act'te), kapısından kabaran Medici kalabalığı (sancaktarlar "palle" sancağı; coşku), sağdan dörtnalla gelip tırıs/yürüyüşle **duran** atlılar (toz izi), gün→sıcak akşam rengi, kamera Medici penceresine zum; pencere altın (`gold_at`). Şiddet yok.
  * `pencere`: cephe, alacakaranlık→gece; pencereler tek tek kararır, bir pencereden sarkan **ip çizgisi + duvara düşen gölge** (asılı beden yok; ucu püskül), çan odası penceresi son kararır; meşale, kuş, bulut, baca dumanı.
  * `kalabalik`: yukarıdaki kabaran kalabalığın genel sürümü (c1 Ciompi, c3 dönüş alayı, c10 V7 meydan kalabalığı).
* **sokak**: uzun palazzo cephesi (bugnato→sıva, taş bank, demir parmaklıklı zemin pencereleri, bifora, kepenkli üst pencereler, saçak+çatı+baca), **ağır kapı** (`door_heavy`: perçinli demir kuşak, halka; açılış/kapanış perspektifli) ve **androne** (kemerli geçit; iç içe tonoz, uçta ışık). Kapı TEK HAMLEDE kapanır (0,20 sn, hızlanarak; ardından sekme + halka sallanması + kamera sarsıntısı + toz + lento'dan dökülen toz taneleri). Ters yönde akan **siluet kalabalık** (ön plan 1,45 paralaks; yürüme döngüsü önceden pişirilmiş), iki yönlü ortam yürüyenleri, bankta konuşanlar, asılı bayraklar, baca dumanı. Gece: meşale, yanan pencereler, kapıdan sıcak ışık.
* **kale/sur**: San Miniato çan kulesi **yün balyalarıyla sarılı**, galeride iki top siluet; kilise (beyaz-yeşil mermer), yamacı izleyen Floransa surları (mazgal, kuleler, kapı kulesi, hasır sepetler), ufukta üç sıra **imparatorluk çadırı** + bayraklar (kızıl çapraz/altın zeminde kartal/lacivert), ocak dumanı, toz; yün tutamları rüzgârda; kuleyi dönen kuşlar; ön planda sallanan otlar; kamera: kuleye yakın → yavaş pull. İnsan/şiddet yok.
* **kale/castel**: Castel Sant'Angelo (silindir gövde, kör kemer şeridi, mazgal, üst kule, flama, köşe burçları) + Passetto duvarı (kör kemer sırası, üstte örtülü koridor, ok yarıkları, kiremit); uzakta Roma (eski San Pietro cephesi, kuleler, çamlar) ve **duman sütunları** (stilize; ceset/kan/yağma yok); nehir.
* **kale/passetto**: koridor **yan görünümü** tek plan (kesit): geri duvarda ok yarıkları (arkada duman/şehir görünür), ışık huzmeleri + toz, meşaleler, ön plan payandaları (figürler arkalarından geçer); **papalık heyeti** (Papa, 2 kardinal, rahip, 6 İsviçreli muhafız `asker`+`halberd`) kamera hızına eşit zemin hızıyla hızlı yürür, Papa'yı sarmalar. Pelerin ANEKDOT → çizilmedi.
* **skyline_dikey**: Palazzo Vecchio kulesine tek dikey plan (`crane up`): palazzo galerisinden kulenin gövdesi → mazgallı galeri → çan odası → külah → direk + flama; yanlarda uzak kuleler (Badia/Bargello tarzı, sisli), Duomo, çatılar, kuş sürüleri/halkaları, yarıklardan havalanan güvercinler, demir kollarda flamalar, 2 derinlikte bulut; yükseldikçe gök derinleşir ve güneş parıltısı artar.

### Yeniden kullanılabilir işlevler (`import cilt_sehir as SE`)
| işlev | ne |
|---|---|
| `palazzo_front(f, x, y, w, h, kind="vecchio"\|"medici"\|"generic", door=None\|0..1, T=Tint, seed, shield=False, tower=True, tower_x=0.60, leaves=True)` | cephe çizer; döner geometri sözlüğü (pencere kutuları, kapı, kule/flama/çan noktası). `palazzo_geom(...)` çizimsiz geometri |
| `door_heavy(f, x, y, h, open_amount, w=None, glow_k=0, swing=0)` | ağır ahşap kapı (0 kapalı … 1 açık); `portal(...)` kemerli taş çerçeve |
| `bonfire(f, x, y, size, t, seed, k=1.0, glow_a=1.0, tod="night", layout=None, smoke=True, embers=True)` | alev+kıvılcım+duman; önceden renklendirilmiş degrade sprite (SrcOver). k: 0 → kıvılcım … 1 inferno. `torch_flame` (ucuz meşale), `smoke_plume`, `smoke_column`, `ember_field`, `ash_field` |
| `tent_row(f, x0, x1, y, size, T, seed, depth)` + `tent_flags(c, pts, t)` | çadır dizisi (+ dinamik bayraklar); `tent_layout` çizimsiz yerleşim |
| `vecchio_tower`, `machico`, `crenel`, `bifora`, `loggia`, `san_miniato_front`, `castel_sant_angelo`, `bale_tower`, `wool_bale`, `cannon`, `gabion`, `stone_wall(clip=…)`, `street_facade`, `tunnel_arch` | mimari parçalar |
| `pyre`, `item_sprite`, `gallows_silhouette`, `light_pool`, `wash`, `silhouettize`, `walk_sil_set`, `flag_pennant`, `circling_birds` | yığın/eşya/darağacı siluet/ışık havuzu/örtü/siluet sprite'ları/flama/kuş halkası |
| `olaylar(scene, act, dur, **p)` | **SFX ajanı için** çekim-içi olay zamanları: `esya_dustu×n, ilk_kivilcim, alev_tam, kapi_hamlesi, kapi_carpar, atlilar_durur, kalabalik_coser, pencere_kararir×n` (küresel zaman = `Shot.origin + t`) |

## 2. Mimari ve performans notları
* `pano` motorunun sınıfları (`Layer`, `Ctx`, `PanoCam`, `World`) yeniden kullanıldı; `SLayer` yalnız önbellek adını (sürüm) değiştirir. `skyline_dikey` için dikey kareaş (`VLayer`) yazıldı (1024 satırlık dilimler, zemin altı dolgulu).
* Çizim sırası: katmanlar → dinamik katmanlar → `grade` (ekran uzayı: alacakaranlık/gece karartması, ışık havuzu) → `fx` (karartmadan sonra: ateş, pencere/meşale ışığı, ateşin önündeki kalabalık) → bant süsleri → metin → günışığı (yalnız gündüz) + toz + vinyet.
* **SrcOver her yerde** (kPlus/renk filtresi ≈6× yavaş): alev/kıvılcım/duman/parıltı önceden renklendirilmiş sprite; FA'nın `cf=` renk filtresi baş/ayakkabıyı etkilemediği için siluetler piksel düzeyinde (`silhouettize`) bir kez pişirilir.
* Kare başına ağır işler: ışık havuzu (≈8 ms), büyük parıltılar yarıçap kısıtlı; `FA.actor` ≈1,5 ms/figür (halka+taşıyıcı ≈35 figür); siluet figürler tek blit.
* Deterministik: tüm rastgelelik tohumlu (`_RS`); zaman çapaları `cx.at` ile çözülür (çözülemezse sayı/varsayılan).

## 3. Ölçümler (bu makine: 4 çekirdek, başka ajanlarla PAYLAŞIMLI; yük ortalaması 3–17 → süreler şişkin, boş makinede yaklaşık yarısı)
`python3 preview_sehir.py --ms` (çekim + RGB okuma + `CM.post`, tek çekirdek, 9 kare; ilk kare ısınma sayılmaz). Medyan / en az / maks (ms/kare) ve bölüm dökümü (medyan ms):

| girdi | medyan | en az | maks | döküm |
|---|---|---|---|---|
| meydan_ates | 226 | 162 | 304 | sahne 173 = fx 48 (alev+ön sıra) · dyn_main 39 (halka+taşıyıcı+yığın) · katmanlar ≈35 · grade 7 |
| meydan_odun | 162 | 155 | 196 | dyn_main 52 · fx 15 · grade 8 |
| meydan_palle | 200 | 130 | 299 | dyn_main 112 (24 kişi + 5 atlı + sancaklar) |
| meydan_pencere | 99 | 92 | 122 | |
| meydan_kalabalik | (ölçülecek) | | | |
| sokak_kapi_gunduz / gece | 114 / 114 | 97 / 108 | 290 / 300 (kapı çarpma kareleri: toz) | dyn_main 15–27 |
| sokak_yuruyus | 94 | 89 | 100 | |
| kale_sur | 105 | 93 | 170 | dyn_camp 10 |
| kale_castel | 108 | 102 | 152 | dyn_city 32 (duman sütunları) |
| kale_passetto | 157 | 124 | 200 | dyn_main 33 · dyn_city 19 |
| skyline_dikey | 211 | 99 | 273 | VLayer blit'leri (kare başına 3–6 büyük kareaş) |

Hedef ≤250 ms/kare (çekim+post, 1 çekirdek): hepsi medyanda altında; ates/palle yük altında 250'ye yaklaşır (tek tek kareler 300 civarı çıkabilir — paylaşımlı CPU gürültüsü; `en az` sütunu boş makine tahminidir).
İlk kare (kit/kareaş pişirme): 0,2–2,3 s (ates 2,3 s: 40+ kostüm kiti ısınır; süreç başına bir kez).
Kareaş pişirme (soğuk önbellek): bkz. `--bake` çıktısı aşağıda (tek koşu; hepsi ≪15 s).
Klipler: 24 fps, 960×540, 10–14 sn; hareket enerjisi (ardışık kare farkı, 240×135 gri) ve ölü kare sayısı `preview_sehir` çıktısında (ates 2,52 · odun 0,34 [gece: düşük kontrast; ölü kare 0]); ölü (kopya) kare yok.

## 4. Bilinen kusurlar
1. Figürler yandan kesme-bebek (FA kiti sınırı): yüz ayrıntısı yok; halka üyeleri yalnız `idle/talk/cheer` (geçişler yok); taşıyıcıların fırlatma hareketi ayrı bir jest değil, durup eşyanın uçması (el pozu `idle`).
2. `ates`: alev dilimli degrade sprite (fresk stilizasyonu; akışkan değil), 14 fps adımlı titreşim; yanan eşyalar kararmak yerine alfa ile solar; kalabalığın derinliği iki katman (y eşiği: arka/ön). Duman koyu mor; gündüz ateşi yok.
3. `odun`: siluet halka iki poz (duran/kolu kalkık) arasında yalnız sallanır; hareket enerjisi düşük (karanlık sahne). Darağacı yalnız siluet (kasıtlı).
4. `palle`: Medici sarayı mekânsal kısaltma (Signoria'nın solunda; gerçekte Via Larga); kalkan yalnız bu act'te; Lorenzo silüeti çizilmedi (yüz/kişi iddiası yok) — yalnız altın pencere. Gün→akşam rengi örtüyle (katmanlar gündüz pişirilmiş).
5. `pencere`: ip çizgisi ucu püskül (ilmik/beden yok); gölge basit paralelkenar; çan odası penceresi tek ışık.
6. `sokak`: androne'ye giren figür "derinleşme" efekti (küçül + yukarı + solarak kaybolur) gerçek 3B değil; ön plan siluet yürüme döngüsü zemin hızına oranlı oynatılır (ayak kayması gözetilmez); androne tonozu iç içe kemer şeritleri; kapı açıkken içeri bakış karanlık+sıcak ışık (iç mekân yok).
7. `kale/sur`: San Miniato cephesi stilize ("tapınak" hissi), insan yok → canlılık bayrak/duman/toz/kuş/yün tutamı/ot; sur yamacı basamaksız rampa; çadırlar ≤46 px.
8. `kale/castel`: Castel yan görünümde "kutu üstü kutu" (silindir yalnız yatay degrade ile); köprü yok; duman sütunları kalın/stilize.
9. `kale/passetto`: ok yarıkları dar, ışık huzmesi hafif; heyet hızı kamera hızından türetilir (kamera sabitse heyet durur); koridor iç aydınlık (gündüz); pelerin çizilmedi.
10. `skyline_dikey`: kule gövdesi sade (yarık+kuşak+flamalar); uzak kuleler 4 tekrar eden stil; kamera hızlı (≈350 px/s ortalama); `cam=("crane","up",px)` varsayılan yolun ÜSTÜNE biner (aşırıya kaçabilir: tek başına `cams` ver).
11. FA `cf=` renk filtresi baş/ayakkabıyı etkilemez (siluetler bu yüzden piksel düzeyinde); renk filtreli figür çizimi ≈2,2× yavaş — ön sıra figürlerde kullanılmadı.
12. Ortam: skia `Fontconfig warning … reset-dirs` satırları sistemden (bizden değil). Kapı çarpma karelerinde toz sprite'ları yüzünden tek kareler 250–300 ms.

## 5. c0–c16 uyum tablosu (brif §7 "Ekran önerileri / AKIŞ NOTU" bölümlerinden çıkarılan beklentiler)
| # | dünyanın karşıladığı | eksik / not |
|---|---|---|
| c0 / c16 | Palazzo Vecchio/Uffizi çevresi yok (metin/oda sekansları); `skyline_dikey` kule + `meydan` gün sahnesi kapı sonrası bağlantı için kullanılabilir | oda/belge sekansları Lab-D |
| c1 | V6 Ciompi/Palazzo Vecchio: `meydan` `act="kalabalik", dir="l"` (sağdan sola kabaran halk, zambak sancakları), `skyline_dikey` Palazzo Vecchio kulesi; V1–V9 Arno panoraması Lab-B (`pano florence`) | yün tarayıcısı silueti: `actors` ile `kesis`/`halk` + `prop` |
| c2 / c4 / c5 / c9 / c13 / c14 / c15 | c13 V4 "gece sokak dioraması (pencereler, şiddet yok, çan yok)": `sokak` `tod="night"`, `actors=[]`, `door=None` (Paris mimarisi değil, genel cephe); c9 V6 "Palazzo Medici saldırı": `meydan palle`'nin Medici cephesi (kalkan açık) ya da `sokak` — şiddet gösterilmez | defter/harita/grafik sekansları bu işin dışında |
| c3 | V1 Kule: `skyline_dikey` (`crane up` tek dikey plan; kule gövdesi→mazgal→çan odası→flama; yanlarda çatı/kuş); V4 dönüş alayı: `meydan kalabalik dir="r"` (soldan sağa kabaran halk) + Lab-B `procession` | Alberghettino dar yarık kadrajı (iç mekân) yok |
| c6 | giostra için atlı/kalabalık parçaları (`palle` atlıları, `kalabalik`) | giostra çekimi (iki atlı + bariyer) hazır değil |
| c7 | V4 `sokak` yürüyüş (üç figür soldan sağa, kemerli eşiğe girer, ters yönde siluet kalabalık); V9 Palazzo Vecchio cephesi (`pencere`/`ates` cephesi); V10–V11 `meydan palle` (atlılar sağdan sola durur, kalabalık soldan sağa kabarır, PALLE sancakları, Medici penceresi altın, kamera pencereye zum); V12 `meydan pencere` (alacakaranlık→gece, pencereler tek tek kararır, ip çizgisi + gölge) | nef/sakristi/Giuliano sahneleri Lab-B `nave` + Lab-D; Lorenzo siluet yok |
| c8 | — | rota haritası/Otranto: Lab-C/Lab-A |
| c10 | V4 9 Kasım `sokak door="close"` (tek hamle, toz+sarsıntı+sekme, kalabalık siluet ters paralaks, kapı gece/gündüz); V6 `meydan ates` (taşıyıcılar eşyayı getirip fırlatır, ilk kıvılcım→alev→yükselen ateş, halka, kamera yarım daire→sabit); V7 `meydan odun` **aynı kamera noktası/aynı yığın merkezi** (`PILE_X`), közer→kül, kül sağa sürüklenir, siluet halka; V7 sonu nehir/kül geçişi Lab-A | "KANIT YOK" damgası/manşet şeridi: dış `quote/title` türü; yazı fırça darbeleri dış tür |
| c11 | Floransa kuşatması: `kale sur` (San Miniato yün balyalı kule, iki top siluet, ufukta çadır/sancak, yavaş pull); Roma 1527: `kale castel` + `kale passetto` (yan görünüm tek plan, ok yarıkları, kemerler, papalık heyeti, uzakta duman) | Prato 1512, Michelangelo sur planı/Yeni Sakristi (harita/plan) bu işin dışında |
| c12 | Palazzo Vecchio–Uffizi–Pitti çevresi: `meydan` (gün), `skyline_dikey`; Uffizi yapımı Lab-B `build uffizi`, Vasari koridoru Lab-B `pano corridor` | Boboli/Pitti cepheleri ayrı (`palazzo_front kind="generic"` ile hızlı cephe) |

## 6. Ana ajandan istekler
* (isteğe bağlı) `cilt_cam.OWN_CAMERA` kümesine `"sehir"`'in dosyada da yazılması (şimdilik `cilt_sehir` içe aktarılırken çalışma anında ekleniyor; qa_flow bu kümeyi okuyor).
* (isteğe bağlı) sfx ajanı `cilt_sehir.olaylar(scene, act, dur, **parametreler)` çıktısını kuyruğa çevirebilir (ateş çıtırtısı, kapı çarpması, atlı nalları, kalabalık coşkusu).
* Çekimlerde `mode="night"` / `tod=` uyumu: gece/alacakaranlık sahnelerine `mode="night"` verilmeli (post LUT + duvar).
* Çalışma kuralı notu: `preview_sehir.py --workers 2` bile iki ağır süreç açar; bellek paylaşımlı olduğundan `--workers 1` kullan; aynı mp4'e iki koşu YAZDIRMA (ffmpeg dosyası bozulur).

## 7. Ekrana konan olgular / kaynak sınıfı
Bu dünya **hiçbir metin/sayı/tarih çizmez** (yalnız `kick/caption` parametresiyle gelen yazı, dış çağrının sorumluluğu). Görsel olgular: Palazzo Vecchio (kule, mazgal, çan odası), Loggia dei Lanzi, Medici kalkanı (altın zemin + altı kırmızı top; yalnız `palle`), Kibirler yığınında brif c10 V6'nın saydığı beş eşya türü (ayna, iskambil, zar, peruk, çalgı), San Miniato çan kulesinin balyalarla sarılması + iki top (görev tanımı, c11), imparatorluk çadırı/sancakları (kızıl çapraz, kartal; stilize), Castel Sant'Angelo + Passetto (örtülü koridor, ok yarıkları), İsviçreli muhafız (`asker`+`halberd`). Kaynaksız saat/hava/ışık iddiası yok: alacakaranlık/gece/dumanlı gök "görsel dil" (brif c7/c10 ile uyumlu); çan sesi/çalması yok (çan siluetleri hareketsiz); şiddet/ceset/kan/asılı beden yok (siluet, işaret, gölge, ip çizgisi).
