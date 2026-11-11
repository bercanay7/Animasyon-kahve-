---
name: karakter
description: Karakter ve nesne hareketi — 12 animasyon prensibi (squash-stretch, anticipation, overshoot, follow-through), GSAP easing, kodla iskelet, matter-js fizik. Bir şeyi hareket ettirirken, canlı/ağır/yaylı hissi ayarlarken kullan.
---
# Karakter ve hareket

Çalışan referans: `araclar/ornek-sahne.html` (başlık düşüşü = anticipation → stretch → squash → elastic overshoot).

## Prensip → GSAP tarifi
| Prensip | Uygulama |
|---|---|
| Anticipation | Hareketten önce ters yöne 0.15-0.2 sn (`power2.out`) |
| Squash & stretch | Hızda uzat (sy 1.2, sx 0.85), çarpmada ez (sy 0.7, sx 1.25); **hacim sabit**: sx ≈ 1/sy; ayak noktasında ölçekle |
| Ease in/out | Düşüş `power3.in`, fırlama `power3.out`, yumuşak `sine.inOut`; `linear` yalnız mekanik |
| Overshoot / settle | `back.out(2)` veya `elastic.out(1, 0.35)` |
| Follow-through | Eklentiler ana gövdeden 2-4 kare geç hareket eder (offset'li tween) |
| Arcs | Doğrusal yol yerine yay (iki eksende farklı ease) |
| Timing | 30 fps'de hızlı aksiyon 6-8 kare, vurgu 12-18 kare; vuruşa oturt (120 BPM = 0.5 sn) |
| Staging | Kare başına tek odak; öteki şeyler durur/sönükleşir |
| Exaggeration | Önce abartılı yap, sonra %70'e çek |

## Kodla iskelet
Eklem hiyerarşisi: `ctx.save(); translate(eklem); rotate(açı); çiz; alt-eklemler; ctx.restore()`. Açıları GSAP ile sür; sönümlü yay (follow-through) için `a += (hedef-a)*k` yerine **t'ye bağlı** `Math.exp(-d*t)*Math.cos(w*t)` kullan (deterministik).

## Fizik (matter-js, MIT)
Sabit adım (`1000/FPS/4`), seed'li başlangıç, **önceden simüle et** → kare dizisi sakla. Aksi halde render sırası/atlanan kareler farklı sonuç verir.

## Kaçın
Spine/Live2D (ücretli lisans); render içinde `Math.random()`/`Date.now()`.

## Yay sönümü ve ease rolleri
- Yay sönümü (damping): 1.0 sıçramaz · 0.7–0.85 "premium/ağırbaşlı" · 0.4–0.6 oyuncu · <0.3 çizgi film. **Yalnızca konum/boyut sıçrar; opacity ve renk asla.**
- Rol bazlı ease: giriş = uzun kuyruklu ease-out (`expo.out`, `power4.out`); kamera/renk akışı = `power2.inOut`; çıkış/zoom-through = `power3.in`; `linear` yalnızca dönme, progress bar, sabit hız.
- Süre: hızlı hareket 0.3–0.6 sn tek tween; çıkışlar girişten %40–50 kısa.
- Çakışma (overlap): sonraki öğe öncekinin %30–50'sinde başlar. Stagger: harf ≈ 1 kare, kelime 60–120 ms, liste 40–80 ms.
- Punch-in/pan: medyanın kendisini değil sarmalayıcıyı ölçekle/taşı. Konum için `left/top` yerine transform.
- Kaçın: başlıkta sürekli "nefes/yüzme" döngüsü; her sahnede aynı giriş; her şeye fade+slide-up.
- Shake: `sin/cos` ofseti, 6-8 karede söner; pulse: %80–120 (kalp atışı = iki hızlı pulse + duraklama); parçacık patlaması: seed'li, hızı zamanla söner.
