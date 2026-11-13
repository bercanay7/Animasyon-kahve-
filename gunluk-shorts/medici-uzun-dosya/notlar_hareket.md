# Hareket, kurgu ve denetim motoru — notlar (ENG-B, 4 Kasım 2026)

Kaynak: kurul tur 1 (`kurul/KURUL.md` B.4–10; AN1, AN2, SA1, PK2, TE1, TE2). Motor baştan yazılmadı; üst katmanlar iyileştirildi.
Dosyalar: `anim.py` (yeni), `cilt_cam.py` (kamera ön ayarları), `cilt_fx.py` (geçiş süresi, sert kesme, HUD, giornata), `compose.py` (kesme, geçiş
ilerlemesi, otomatik kamera, deklanşör, parça sonu bekleme, bitiş ekranı, HUD gizleme), `shots.py` (`shutter=`, `family=`, `hud=`, `tr="cut"`),
`cilt_kinds.py` (fresk başlığı), `cilt_wall.py` (giornata dikişi, WALL_VER 4), `qa_flow.py` (yeni kapılar). Eski sahneler değişmeden çalışır:
açık sayılı `cam=` değerleri birebir aynı kamera durumunu verir (eski/yeni karşılaştırma farkı 0; `python3 cilt_cam.py`, `python3 anim.py` öz sınama).

## 1. Geçişler ve sert kesme

```python
shot(..., tr="cut")                                   # birinci sınıf sert kesme (tr=None da kesmedir)
shot(..., tr=("cut", dict(carry=False)))              # kesmede kamera dursun (varsayılan: kamera kesmede HAREKETLİ — kesme hareket üstünde)
shot(..., tr=("slide", 0.3, dict(dir="r")))           # "vuruş" geçişi (sayı/liste ritmi)
shot(..., tr=("yikama", 2.2), link="color")           # "uzun" geçiş (veba, ölüm, bölüm sonu)
```
- Süre aralığı **0,25–2,4 sn** (`cilt_fx.TR_MIN/TR_MAX`), tüm geçişlerde. Tür alt sınırı (`TR_MIN_KIND`; 6 karede kaba sıçrıyorlar): candle 0,6 · iris 0,4 ·
  yikama 0,5 · sayfa 0,45 · giornata 0,5. Önerilen tempo: vuruş 0,25–0,4 (slide/carry/zoomthru/light) · standart 0,7–1,0 · uzun 1,6–2,4.
  `place="before"` geçiş giden çekimin %85'iyle sınırlıdır (2,4 sn geçiş için giden çekim ≥ 2,9 sn).
- Yeni geçişlerde gelen çekimin yerel saati `süre + doğum` kadar önce başlar (`lead`): mutlak yerel `at=` değerleri bu kadar erken gelir (çapalılar etkilenmez).
  Uzun geçişte lead büyür (iris 2,4 → 3,3 sn). Kesmede lead yoktur. Kesmede `link=` gerekmez (`"audio"`, `"cam"` önerilir).
- Geçiş ilerlemesi kareye kuantlı: N karelik geçişte k = (j+1)/(N+1) → ilk geçiş karesi giden çekimin, son geçiş karesi gelen çekimin kopyası değil (AN1-E7).
  Kare testi (9 geçiş × 0,25/0,9/2,4 sn = 27 durum): k doğru, **özdeş ardışık kare 0**, hata 0 → `out_p1/duzeltme/ENG-B/gecis_test_k015-085.jpg`.

## 2. Kamera ön ayarları (`cam=`)

Açık sayı verilen eski biçimler aynen çalışır. Miktar verilmezse **süreye bağlı**; `cam=` hiç verilmezse Program **tohumlu, ağırlıklı** bir hareket seçer.

| `cam=` | Ne | Örnek |
|---|---|---|
| `"push"` / `("push",)` / `("push", "auto")` | süreye bağlı itme: miktar = 0,039·süre^0,47 (2,5 sn %6 · 8 sn %10,5 · 13 sn %13); hız kısa çekimde ≈2,4 %/sn, uzunda ≈0,9 %/sn; tohumla ±%12, eğri çeşidi (io/out/in), odak merkezi hafif kayar | `cam="push"` |
| `("push", 0.08)` | eski sabit itme | |
| `("push", dict(rate=0.012))` | hızla: %1,2/sn × süre | |
| `("pull" …)` | aynı kurallarla çekme | `cam=("pull",)` |
| `("pan", "r"\|"l"[, px])` | yatay kayma, duvar ×0,40; px yoksa 34 px/sn (110–300) | `cam=("pan", "r")` |
| `("truck", "r"\|"l"[, px])` | yanal kaydırma, derin paralaks (duvar ×0,15); px yoksa 26 px/sn (90–240) | `cam=("truck", "l", 180)` |
| `("tilt", "up"\|"down"[, px])` | dikey çevirme hissi (duvar ×0,85); px yoksa 20 px/sn (70–180) | `cam=("tilt", "down")` |
| `("crane", "up"\|"down"[, px])` | dikey kaydırma + paralaks; px yoksa 22 px/sn | `cam=("crane", "up")` |
| `("orbit", derece)` | paralaks yörünge (≤12°) | `cam=("orbit", 8)` |
| `("whip", "r"\|"l"[, px][, dict(where, at, dur=0.30)])` | hızlı savrulma (420 px). `where="in"`: çekim savrulmanın içinde başlar, aşmayla oturur; `"out"`: son `dur` sn'de hazırlık + hızlanarak çıkar (ardından `tr="cut"`); `at=çapa` → çekim içi savrulma | `cam=("whip", "r", dict(where="out"))` → sonraki `tr="cut", cam=("whip", "r", dict(where="in"))` |
| `"hand"` / `"drift"` / `("hand", titreşim_px)` | elde mikro sürüklenme: yavaş gezinme (≈0,1–0,35 Hz, 6 px; `wander=`) + 1 px titreşim + ±0,12° + yarım itme | `cam="hand"` |
| `"hand2"` | güçlü elde (şiddet anları) | |
| `("rack", a, b[, dict(at, dur, r, sigma, axis)])` | odak kaydırma; `axis="y"`: düzlemsel derinlik — odak bandı a.y → b.y kayar, ön (alt) / arka (üst) bulanır | `cam=("rack", (960, 880), (960, 330), dict(axis="y", at=("c2s5", "Cossa", -0.1), dur=1.2, r=170))` |
| `("track", ad)` / anahtar kareler | eski | |

Her biçime eklenebilen `dict`: `pivot=`, `push=`, `hand=`, `drift=`, **`ease="io"|"out"|"in"|"lin"`** ("out" = hızlı giriş, uzun yumuşak çıkış),
**`shake=[(çapa, genlik_px[, süre]), …]`** (darbe sarsıntısı, 2–5 px, 0,25 sn). Örnek: `cam=("push", 0.06, dict(ease="out", shake=[(("c2s9", "damga", 0.0), 4)]))`.

**`cam=` verilmezse** (`compose.Program._auto_cams`, `cilt_cam.auto_spec`): push %28 · pull %13 · pan %18 · truck %11 · hand %12 · tilt/crane/orbit %6'şar;
önceki çekimin ailesi ve push↔pull seçilmez; <2,6 sn'de yörünge/dikey yok; şerit türlerinde pan ağırlıklı; yön bölümdeki son açık `cam=`'den (yoksa r/up).
Tohum çekim içeriğinden (`Shot.stable_seed`): parça/tam film aynı. `Shot.cam_auto=True`; qa tablosunda "auto" görünür. Kendi kamerası olan türlere
(oda/pano/sehir/build ve p1_ sarmalayıcıları) dokunulmaz — onlarda hareket `cams=`/`path=` ile yazılır.

## 3. Seçici deklanşör (hareket bulanıklığı)

`shot(..., shutter="auto")` (varsayılan) · `True` (hep, ≥3 örnek) · `False` · `5` (zorunlu 5 örnek) · `dict(at=çapa, dur=sn, n=5)` (pencere) · `dict(angle=180)`.

Her çekim içi karede (geçiş kareleri hariç — onların kendi bulanıklığı var): (a) `cam=` analitik ekran hızı (`cilt_cam.screen_speed`), (b) önceki kareden
ölçülen akış (Farneback 240×135): **küresel** afin hız (kamera ya da türün iç kamerası; TE1 yöntemi) ve **nesne** alanı (değişimi hareketle açıklanan,
>16 px/kare pikseller), (c) `anim.hint_speed`. Tetik: analitik ≥4 · küresel ≥8 · karenin ≥%3'ü nesne · ipucu ≥8 px/kare → 180° pozlamada (½ kare) N alt kare
**yeniden çizilir** ve ortalanır (post ve HUD'dan önce; çekim sınırı aşılmaz): N=3; ≥30 px/kare 5; ≥60 → 7. Örnekler arası boşluk >3 px ise ilk/son
örnek arası piksel akışıyla doldurulur (zum/paralaks doğru). Yeniden çizim olduğu için ekrana sabit yazı/levha keskin kalır.
QA çağrıları (`frame(n, post=False)`) deklanşörsüzdür; `Program(part=N, shutter=False)` tümden kapatır. İstatistik: `Program.shutter_stats`.
Hızlı nesne çizen kod: `anim.hint_speed(cx, px_per_frame)`.

## 4. `anim.py` — hareket yardımcıları (figür kitine bağlı değil)

Zaman: `t = cx.t`, `t0 = cx.at(çapa)`. Hepsi deterministik ve alt-kare zamanında sürekli.

| işlev | ne | 1 satır örnek |
|---|---|---|
| `anticip(t, t0, dur, back=0.12, pre=0.22)` | hazırlık: t0'dan önce ters yöne −back, t0'dan dur sn'de 1 | `y = y0 - 140 * anim.anticip(cx.t, cx.at(("c2s4", "attı", 0)), 0.35)` |
| `settle(t, t0, dur=0.45, over=0.12)` | oturma: t0+dur'da varır, %12 aşar, sönümlü oturur | `x = lerp(-300, 960, anim.settle(cx.t, cx.at(a), 0.5))` |
| `wobble(t, t0, amp=1, freq=3, decay=5)` | darbe sonrası sönümlü salınım | `rot = 6 * anim.wobble(cx.t, t_hit)` |
| `shake(t, t0, dur=0.25, amp=4, seed=0)` | sarsıntı → (dx, dy) | `dx, dy = anim.shake(cx.t, t_hit, amp=3, seed=cx.seed)` |
| `blink(t, seed=0, every=(2.4, 5.6), dur=0.16)` | göz kırpma: 0 açık … 1 kapalı | `eye_h = 9 * (1 - anim.blink(cx.t, seed=7))` |
| `breathe(t, seed=0, amp=1, hz=0.22)` | boşta nefes | `s = 1 + 0.006 * anim.breathe(cx.t, seed=3)` |
| `keyed(t, keys)` | anahtar kare (parça başına eğri) | `x = anim.keyed(cx.t, [(0, 200), (1.2, 900, "out"), (2.0, 960, "settle")])` |
| `stamp_pose(t, t0, profile)` | `squash` ezilme · `spin` dönme · `bounce` sekme · `drop` eski · `ink` mürekkep | `p = anim.stamp_pose(cx.t, t_hit, "spin")` |
| `stamp(f, text, x, y, t, t0, profile, …)` | profilli damga + gölge sıçraması + mürekkep yayılması; darbe zarfı döner | `anim.stamp(cx.f, "ANEKDOT", 1500, 300, cx.t, cx.at(a), "bounce")` |
| `stamp_ovl(text, x, y, at, profile=…, jolt_amp=0)` | p1_ortak.ov ile ovl (at = DARBE anı) | `P.ov(..., anim.stamp_ovl("MİT", 1480, 260, ("c2s14", "mit", 0), "squash", jolt_amp=3))` |
| `impact_ovl(at, amp=4, dur=0.25)` | çapada tüm kareyi sarsar (ovl listesinin SONUNA) | `P.ov(..., anim.impact_ovl(("c1s9", "çöktü", 0), amp=5))` |
| `jolt(f, dx, dy)` | çizilmiş kareyi kaydır | `anim.jolt(cx.f, *anim.shake(cx.t, t_hit))` |
| `hint_speed(cx, v)` / `speed_of(p0, p1, dt)` | deklanşöre hızlı nesne ipucu | `anim.hint_speed(cx, anim.speed_of(p_prev, p_now, 1/24))` |

Damga çeşitliliği (AN1-E8): bölümde ≤2 kez aynı profil; `squash` vurgu, `spin` itiraz, `bounce` mizah, `ink` sessiz kaynak notu.

## 5. HUD, parça sonu, bitiş ekranı, fresk başlığı, diğer

- HUD 300×66, sağ/üst kenardan 72 px: `cilt_fx.HUD_RECT = (1548, 72, 1848, 138)`, kaçınma alanı `cilt_fx.hud_keepout()` (+18 px).
  `shot(..., hud=False)` ya da `HUD_SKIP` türleri (kartlar, `kapak_kilit`, `kapak_kese`) HUD/ilerleme/bölüm etiketini gizler; geçişte yumuşak söner/doğar.
  Bölüm etiketi `cilt_fx.CHAPTER_TAG_XY = (96, 60)` (TE2-K2).
- Parça sonu: anlatının bittiği bölüm sonundan sonra `compose.END_HOLD = 1,3` sn (son sözcükten ≈1,4 sn nefes), sonra bitiş geçişi; sahne modülü `END_HOLD`
  ile değiştirebilir. Video 1,3 sn uzar → miks kuyruğu `compose.TAIL = 8,3` (`miks.py --tail 8.3`).
- Bitiş ekranı: etiketler #E9C770, ≥37 px (Cinzel, ≥34 px korunur), koyu levha üstünde, vinyetten sonra; "TESLİMAT TAMAM" 36 px #F2D98A. Uç ekran yuvaları
  (330, 610, 520×292) ve (1070, 610, 520×292).
- Fresk başlığı: panel 0–1,5 sn, MEDİCİ 0,55'te girer / 1,4 sn'de tam; 4,5 sn kartta çıkış geçişine dek ≥2,2 sn tam okunur. Önerilen `CARD_GAP["c0"] = 4.5`.
- Giornata: duvar yama tonu kenarı ≈σ6 px yumuşak + ±5 px düzensiz, ton farkı %60, dikiş daha ince (`cilt_wall` v4); geçiş/açılım yumuşak cepheli (≈70 px) ve yumuşak
  kenarlı (≈10 px), k=1'de dikiş izi kalmaz.
- `Program(shots=…)` modunda `cx.year = None` (donem.py sözleşmesi); geçiş şeridi palle'si o anın HUD yılıyla (`donem.arms_variant`).

## 6. qa_flow yeni kapılar (`python3 qa_flow.py --part N`; `--fast` statik; `--no-eng-a`)

| kapı | ölçüt | eşik |
|---|---|---|
| Ardışık itme | gerçek kamera ailesi (cam=; kendi kameralı türlerde cams/path) | ≤5 |
| Kart dizisi | aile haritası (`p1_`/`pN_` öneki soyulur; `shot(family=…)` ya da sahne modülünde `AILE={tür: aile}`) | ardışık kart ≤4 · ≤75 sn'de bir dünya/figür |
| Sert kesme payı | bölüm içi sınırlarda kesme | ≥%15 |
| Geçiş süresi dağılımı | tasarlı geçiş sürelerinin σ'sı | ≥0,25 sn |
| Ölçülen hareket | 0,5 sn adımlı kare farkı medyanı (geçişler hariç) | >6 sn çekimde ≥1,25 (kurulun "durgun" dediği çekimler 0,47–1,25) |
| Yerleşim / Dönem (ENG-A) | `qa_yerlesim.py` / `qa_donem.py` alt süreçte | çıkış kodu 0 |

## 7. Ölçümler

- **Kurulun P1 v1'i (yeni motorla, v1 çizelgesi):** 6 KALDI — itme dizisi 21 (403,6–557,5 sn), kart dizisi 20 (403,6–544,5 sn), dünyasız 141 sn, kesme %3 (3/89),
  σ 0,02 sn, hareketsiz 13 çekim (c0_gerekce, c1_agi, Machiavelli ×2, c1_kademe, kose, medal, timeline, network, c2_borc, mezar, rivayet, stacked).
- **Sahne yazarının güncel P1'i (4 Kas 16:55):** itme 4 ✓ · kart 4 / dünyasız 21 sn ✓ · kesme %36 ✓ · σ 0,38 ✓ · hareketsiz 2 (#72 network 0,68; #82 emblem 0,86) ✗ ·
  tür tekrarı 2 (p1_oda ×4, Cavalcanti) ✗ · ENG-A yerleşim 0 / dönem 0 ihlal ✓.
- **Deklanşör maliyeti** (kurulun P1'i, her 10 sn'de 0,75 sn ardışık pencere, 1080 kare): taban 210 → 258 ms/kare = **+%23,2** (bulanık kare %8,9; kare başına
  0,20 ek çizim; ölçüm 14,5 ms/kare). En hızlı anlarda (39,6–42,6 + 48,9–51,1 sn) +%197 (bilinçli: 85/136 kare, N=3/5/7). Daha çok hızlı hareket yazıldıkça maliyet artar.
- Kanıt: `out_p1/duzeltme/ENG-B/` — `deklansor_once_sonra.mp4` (yan yana), `deklansor_1e1_*.jpg`, `gecis_test_k015-085.jpg`, `hud_once_sonra.jpg`,
  `bitis_once_sonra.jpg`, `fresk_once_sonra.jpg`, `kapak_hudsuz_ve_bolum_etiketi.jpg`, `giornata_duvar_once_sonra.jpg`.
