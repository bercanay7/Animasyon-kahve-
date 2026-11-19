# Dorian Gray üslup kapısı (19 Kasım 2026)

Üç aday aynı sahneyi çizer: XX. bölüm, çatı katındaki eski okul odası; lamba masada, Dorian sırtı dönük örtüyü çeker, portrede çökmüş yüz (8 sn, anlatımsız).

| Aday | Ne |
|---|---|
| `gravur` | `milton/lib/gravur.js` (kendi motorumuz): ton katmanı + tarama yamaları → baskı |
| `impasto` | Lemo-Opuscar `impasto` (WebGL2, bıçak darbesi yağlıboya); `vendor/` MIT |
| `karma` | dünya gravür, yalnız portrenin tuvali impasto (tek renkli istisna) |

## Dosyalar
- `sahne.js`: ortak sahne, düz değer planlı resim (her parça: yol, renk `c`, gravür taraması `h`, isteğe bağlı ton `ton`, impasto fırça ayarı `p`). Levhalar: oda, portre (genç/çökmüş, `curu`), örtü, Dorian, kol; zaman çizelgesi.
- `gravur_mod.js`: gravür çizici (ton = rengin parlaklığı; lamba ışığı ton katmanına "screen").
- `main.js`: aday seçici, impasto çizici (levha başına `Ref` → `paintRef` → darbe grubu), karma bindirme (tuval − örtü maskesi).
- `vendor/impasto.js`, `vendor/plate.js`: lemomo-ai/lemo-opuscar `3a7132b`, `styles/impasto/demo/engine/`, MIT (`vendor/LICENSE-MIT.txt`). Değiştirilmedi. Lemo'nun STYLE.md'si (CC BY-NC) depoya alınmadı.
- `render.js`: `node render.js <gravur|karma|impasto> <kareler|kapak|olc|video>`; çıktılar `OUT` (varsayılan scratchpad/kapi/<mod>). Kapak anı `KT` (varsayılan 3,75 sn).
