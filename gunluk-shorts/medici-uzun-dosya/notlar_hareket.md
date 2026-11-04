# Hareket, kurgu ve denetim motoru — notlar (ENG-B, 4 Kasım 2026)

Kaynak: kurul tur 1 (`kurul/KURUL.md` B.4–10; AN1, AN2, SA1, PK2, TE1, TE2). Motor baştan yazılmadı; üst katmanlar iyileştirildi.
Dosyalar: `anim.py` (yeni), `cilt_cam.py` (kamera ön ayarları), `cilt_fx.py` (geçiş süresi, sert kesme, HUD, giornata), `compose.py` (kesme, geçiş
ilerlemesi, otomatik kamera, deklanşör, parça sonu bekleme, bitiş ekranı), `shots.py` (`Shot.shutter`, `tr="cut"`), `cilt_kinds.py` (fresk başlığı),
`cilt_wall.py` (giornata dikişi), `qa_flow.py` (yeni kapılar). Eski sahne dosyaları değişmeden çalışır (açık `cam=` değerleri birebir aynı kamera verir).

## 1. Geçişler ve sert kesme

```python
shot(..., tr="cut")                                   # birinci sınıf sert kesme (tr=None da kesmedir)
shot(..., tr=("cut", dict(carry=False)))              # kesmede kamera dursun (varsayılan: kamera kesmede HAREKETLİ — kesme hareket üstünde)
shot(..., tr=("slide", 0.3, dict(dir="r")))           # "vuruş" geçişi (sayı/liste ritmi)
shot(..., tr=("yikama", 2.2), link="color")           # "uzun" geçiş (veba, ölüm, bölüm sonu)
```
- Süre aralığı **0,25–2,4 sn** (`cilt_fx.TR_MIN/TR_MAX`), tüm geçişlerde (eski 1,0 sn kırpması kalktı). Önerilen üç tempo: vuruş 0,25–0,4 · standart 0,7–1,0 · uzun 1,6–2,4.
  `place="before"` geçiş giden çekimin son `süre` sn'sini kullanır ve giden çekimin %85'iyle sınırlıdır (2,4 sn geçiş için giden çekim ≥ 2,9 sn).
- Yeni geçişlerde gelen çekimin yerel saati `süre + doğum` kadar önce başlar (`lead`); mutlak yerel `at=` değerleri bu kadar erken gelir (çapalılar etkilenmez).
  Uzun geçişte lead büyür (iris 2,4 sn → 3,3 sn): mutlak saniyeli `at=` kullanıyorsan `at = lead + x` yaz ya da çapaya geç.
- Kesmede `link=` zorunlu değil (`"audio"`, `"cam"` önerilir). Kesmeye dönen çekimde lead kalkar (yerel saat t0'da başlar).
- Geçiş ilerlemesi kareye kuantlı: N karelik geçişte k = (j+1)/(N+1) → ilk geçiş karesi giden çekimin, son geçiş karesi gelen çekimin kopyası değildir
  (kurul AN1-E7 "çift kare" giderildi).

## 2. Kamera ön ayarları (`cam=`)

Açık sayı verilen eski biçimler aynen çalışır. Yeni: miktar verilmezse **süreye bağlı**; `cam=` hiç verilmezse Program **tohumlu, ağırlıklı** bir hareket seçer.

| `cam=` | Ne | Örnek |
|---|---|---|
| `"push"` / `("push",)` / `("push", "auto")` | süreye bağlı itme: miktar = 0,039·süre^0,47 (2,5 sn %6 · 4 sn %7,6 · 8 sn %10,5 · 13 sn %13); hız kısa çekimde ≈2,4 %/sn, uzunda ≈0,9 %/sn; tohumla ±%12, eğri çeşidi (io / out / in) ve odak merkezi hafif kayar | `cam="push"` |
| `("push", 0.08)` | eski sabit itme (%8) | |
| `("push", dict(rate=0.012))` | hız ile: %1,2/sn × süre | |
| `("pull" …)` | aynı kurallarla çekme | `cam=("pull",)` |
| `("pan", "r"\|"l"[, px])` | yatay kayma + duvar ×0,40; px yoksa 34 px/sn (110–300) | `cam=("pan", "r")` |
| `("truck", "r"\|"l"[, px])` | yanal kaydırma, derin paralaks (duvar ×0,15); px yoksa 26 px/sn (90–240) | `cam=("truck", "l", 180)` |
| `("tilt", "up"\|"down"[, px])` | dikey çevirme hissi (duvar ×0,85, içerikle birlikte); px yoksa 20 px/sn (70–180) | `cam=("tilt", "down")` |
| `("crane", "up"\|"down"[, px])` | dikey kaydırma + paralaks (eski); px yoksa 22 px/sn | `cam=("crane", "up")` |
| `("orbit", derece)` | paralaks yörünge (≤12°; içerik bir yöne, duvar ters) | `cam=("orbit", 8)` |
| `("whip", "r"\|"l"[, px][, dict(where=…, at=…, dur=0.30)])` | hızlı savrulma (varsayılan 420 px). `where="in"`: çekim savrulmanın içinde başlar, aşmayla oturur (kesmeden sonra); `"out"`: son `dur` sn'de hazırlık + hızlanarak çıkar (ardından `tr="cut"`); `at=çapa` → çekim içinde savrulma (hazırlık + oturma). Deklanşör yönlü bulanıklık verir | `cam=("whip", "r", dict(where="out"))` → sonraki çekim `tr="cut", cam=("whip", "r", dict(where="in"))` |
| `"hand"` / `"drift"` / `("hand", titreşim_px)` | elde mikro sürüklenme: yavaş gezinme (≈0,1–0,35 Hz, 6 px; `wander=`) + ince titreşim (1 px) + ±0,12° + süreye bağlı yarım itme | `cam="hand"` |
| `"hand2"` | güçlü elde (4 px titreşim) — yalnız şiddet anları | |
| `("rack", a, b[, dict(at, dur, r, sigma, axis)])` | odak kaydırma. `axis="y"`: düzlemsel derinlik — odak bandı a.y → b.y kayar, ön (alt) / arka (üst) bulanır; axis yoksa dairesel odak (eski) | `cam=("rack", (960, 880), (960, 330), dict(axis="y", at=("c2s5", "Cossa", -0.1), dur=1.2, r=170))` |
| `("track", ad)` / anahtar kareler | eski | |

Her biçime eklenebilen `dict`: `pivot=(x,y)`, `push=`, `hand=` (titreşim px), `drift=(dx,dy)`, **`ease="io"|"out"|"in"|"lin"`** (zaman eğrisi; "out" = hızlı giriş,
uzun yumuşak çıkış), **`shake=[(çapa, genlik_px[, süre]), …]`** (darbe sarsıntısı: damga, kapı, çekiç; 2–5 px, 0,25 sn).
Örnek: `cam=("push", 0.06, dict(ease="out", shake=[(("c2s9", "damga", 0.0), 4)]))`.

**`cam=` verilmezse** (`compose.Program._auto_cams`): ağırlıklar push %28 · pull %13 · pan %18 · truck %11 · hand %12 · tilt %6 · crane %6 · orbit %6;
önceki çekimin ailesi (ve push↔pull) seçilmez; kısa (<2,6 sn) çekimde yörünge/dikey yok; şerit türlerinde (skyline/frieze/procession) pan ağırlıklı;
yatay/dikey yön bölümdeki son açık `cam=`'den devralınır (varsayılan sağ/yukarı). Tohum çekim içeriğinden (`Shot.stable_seed`): parça ve tam filmde aynı.
Seçilen değer `Shot.cam`'e yazılır, `Shot.cam_auto=True` olur; qa tablosunda görünür. Kendi kamerası olan türlere (oda/pano/sehir/build ve p1_ sarmalayıcıları) dokunulmaz.

Yön sözleşmesi (§1-6) geçerli: yükseliş `r`/`up`, düşüş `l`/`down`. Kamera son pozunda yazı kenar payı ≥48 px (AN2-Ö5) sahne yazarının sorumluluğunda.

## 3. Seçici deklanşör (hareket bulanıklığı)

`shot(..., shutter="auto")` (varsayılan) · `shutter=True` (hep, hıza göre ≥3 örnek) · `shutter=False` · `shutter=5` (zorunlu 5 alt örnek) ·
`shutter=dict(at=çapa, dur=sn, n=5)` (yalnız bu pencerede zorunlu; dışında auto) · `dict(angle=180)` deklanşör açısı.

Karar (geçiş dışındaki her karede): hız = en büyük(**kamera analitiği** `cilt_cam.screen_speed`, **önceki kareden ölçülen akış** (Farneback 240×135; yalnız
değişimi hareketle açıklanan pikseller; türün iç kamerası ve nesneler dahil), **`anim.hint_speed` ipucu**). Kamera ≥ 3 px/kare ya da nesne/iç hareket ≥ 5 px/kare
→ 180° pozlamada (½ kare) N alt-kare yeniden çizilir ve ortalanır (post ve HUD'dan önce; çekim sınırı aşılmaz): N=3 (<12 px/kare), 5 (12–30), 7 (≥30).
Çok hızlı kamerada (savrulma) alt örnekler arası boşluk yönlü bulanıklıkla doldurulur. Ekrana sabit yazılar (ovl) gerçek yeniden çizimde keskin kalır.
Geçiş kareleri kendi bulanıklığını taşır (değişmedi). İstatistik: `Program.shutter_stats`. Maliyet ölçümü: §7. qa örneklemesinde kapalı (`Program(shutter=False)`).
Hızlı nesne çizen kod: `anim.hint_speed(cx, px_per_frame)` (ör. düşen sikke 26 px/kare) → o karede alt örnekleme garanti.

## 4. `anim.py` — hareket yardımcıları (figür kitine bağlı değil)

Zaman: `t = cx.t`, `t0 = cx.at(çapa)`. Hepsi deterministik ve alt-kare zamanında sürekli.

| işlev | ne | 1 satır örnek |
|---|---|---|
| `anticip(t, t0, dur, back=0.12, pre=0.22)` | hazırlık: t0'dan önce ters yöne −back, t0'dan dur sn'de 1 | `y = y0 - 140 * anim.anticip(cx.t, cx.at(("c2s4", "attı", 0)), 0.35)` |
| `settle(t, t0, dur=0.45, over=0.12)` | oturma: t0+dur'da hedefe varır, %12 aşar, sönümlü oturur | `x = lerp(-300, 960, anim.settle(cx.t, cx.at(a), 0.5))` |
| `wobble(t, t0, amp=1, freq=3, decay=5)` | darbe sonrası sönümlü salınım (0 çevresi) | `rot = 6 * anim.wobble(cx.t, t_hit)` |
| `shake(t, t0, dur=0.25, amp=4, seed=0)` | sarsıntı → (dx, dy) | `dx, dy = anim.shake(cx.t, t_hit, amp=3, seed=cx.seed)` |
| `blink(t, seed=0, every=(2.4, 5.6), dur=0.16)` | göz kırpma: 0 açık … 1 kapalı | `eye_h = 9 * (1 - anim.blink(cx.t, seed=7))` |
| `breathe(t, seed=0, amp=1, hz=0.22)` | boşta nefes [−amp, amp] | `s = 1 + 0.006 * anim.breathe(cx.t, seed=3)` |
| `keyed(t, keys)` | anahtar kare (parça başına eğri) | `x = anim.keyed(cx.t, [(0, 200), (1.2, 900, "out"), (2.0, 960, "settle")])` |
| `stamp_pose(t, t0, profile)` | damga pozu: `squash` ezilme · `spin` dönme · `bounce` sekme · `drop` eski · `ink` mürekkep | `p = anim.stamp_pose(cx.t, t_hit, "spin")` |
| `stamp(f, text, x, y, t, t0, profile, …)` | profilli damga (CM.stamp'ı sarar) + gölge sıçraması + mürekkep yayılması; darbe zarfını döndürür | `anim.stamp(cx.f, "ANEKDOT", 1500, 300, cx.t, cx.at(a), "bounce")` |
| `stamp_ovl(text, x, y, at, profile=…, jolt_amp=0)` | p1_ortak.ov ile ovl (at = DARBE anı; eski P.stamp'ta at iniş başıydı) | `P.ov(..., anim.stamp_ovl("MİT", 1480, 260, ("c2s14", "mit", 0), "squash", jolt_amp=3))` |
| `impact_ovl(at, amp=4, dur=0.25)` | çapada tüm kareyi kısa sarsar (ovl listesinin SONUNA) | `P.ov(..., anim.impact_ovl(("c1s9", "çöktü", 0), amp=5))` |
| `jolt(f, dx, dy)` | çizilmiş kareyi kaydır (sarsıntı uygulaması) | `anim.jolt(cx.f, *anim.shake(cx.t, t_hit))` |
| `hint_speed(cx, v)` / `speed_of(p0, p1, dt)` | deklanşöre hızlı nesne ipucu | `anim.hint_speed(cx, anim.speed_of(p_prev, p_now, 1/24))` |

Damga çeşitliliği (AN1-E8): aynı bölümde ≤2 kez aynı profil; `squash` vurgu, `spin` itiraz/ret, `bounce` mizah, `ink` sessiz kaynak notu.

## 5. HUD, parça sonu, bitiş ekranı, fresk başlığı

- HUD 300×66, sağ/üst kenardan 72 px: `cilt_fx.HUD_RECT = (1548, 72, 1848, 138)`; kaçınma alanı `cilt_fx.hud_keepout()` (+18 px). Levhalar bu alana girmez.
- Parça sonu: anlatının bittiği bölüm sonundan sonra `compose.END_HOLD = 1,3` sn son çekim sürer (son sözcükten ≈1,4 sn nefes), sonra bitiş geçişi.
  Sahne modülü `END_HOLD = …` ile değiştirebilir. **Video 1,3 sn uzar:** miks kuyruğu `compose.TAIL = 8,3` sn (bekleme + 7 sn bitiş ekranı) → `miks.py --tail 8.3`.
- Bitiş ekranı: etiketler (SIRADAKİ PARÇA / TÜM FİLM / ABONE OL) #E9C770, Cinzel 38 px, koyu levha üstünde, vinyetten sonra çizilir; "TESLİMAT TAMAM" 36 px #F2D98A.
  Uç ekran yuvaları 30 px yukarı: (330, 610, 520×292) ve (1070, 610, 520×292) — YouTube uç ekran öğeleri buna hizalanmalı.
- Fresk başlığı (`fresco_title`): panel 0–1,5 sn'de açılır, MEDİCİ 0,55'te girer, 1,4 sn'de tam; 4,5 sn kartta çıkış geçişine dek ≥2,2 sn tam okunur.
  Önerilen `ses_birlestir.CARD_GAP["c0"] = 4.5`.

## 6. qa_flow yeni kapılar

Bkz. `python3 qa_flow.py --part 1 [--fast]` çıktısı; eşikler ve P1 sayıları raporda (§8).

## 7. Ölçümler

(§3 deklanşör maliyeti ve §6 sayıları iş bitince eklenir.)
