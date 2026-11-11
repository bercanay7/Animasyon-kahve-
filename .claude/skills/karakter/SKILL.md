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
