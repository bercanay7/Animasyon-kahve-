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

## 3. Ölçümler
(aşağıda — son koşu)

## 4. Bilinen kusurlar
(aşağıda — son koşu)

## 5. c0–c16 uyum tablosu
(aşağıda — son koşu)

## 6. Ana ajandan istekler
(aşağıda — son koşu)
