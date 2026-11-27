# Efekt tarifi kaynakları (27 Kasım 2026)

Kullanıcının paylaştığı "Claude Code ile video" depoları incelendi (alt ajan okudu, başkan lisans ve dosyaları doğruladı). Kural: kod kopyalanmaz, parametreler ve fikir kendi Canvas2D/WebGL2 kodumuza aktarılır. Apache-2.0 kodu kopyalanırsa değişiklik bildirimi gerekir. Lisanssız depo yalnız okunur.

| Depo | Lisans | Ne işe yarar | Karar |
|---|---|---|---|
| [kiselas/every-frame-is-code](https://github.com/kiselas/every-frame-is-code) | MIT | `draw(ctx,t)` düzeni (bizimkiyle aynı). `05-transitions.md`: iris, push, whip, light leak (Canvas2D); burn dissolve, luma wipe, wave (GLSL). `07-effects-cookbook.md`: durumsuz parçacık, ateş/duman, grain, mürekkep titremesi (line boil), sis katmanları, tanrı ışınları. `04-motion-easing.md`: derinlik katsayılı kamera. | al |
| [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | Apache-2.0 | `references/shots/transition/print-texture-transitions.md` (mürekkep yayılması geçişi), `camera/depth-layer-moves.md` (2.5D katman), `effects/riso-print-hits.md`. Kod TSX; parametreler değerli. | fikir olarak oku |
| [sub-level/marketing-videos](https://github.com/sub-level/marketing-videos) | MIT | Yalnız `src/lib/DustField.tsx`: derinlikli toz, her zerreye ayrı yol. | yalnız toz |
| [Leonxlnx/escapement](https://github.com/Leonxlnx/escapement) | MIT | `tools/edit.py`: orta tonda güçlü grain, halation, luma geçişi; `tools/exposure_check.py` pozlama denetimi. | fikir |
| [sirioberati/ai-filmmaking-camera-control-seedance-2-5](https://github.com/sirioberati/ai-filmmaking-camera-control-seedance-2-5) | MIT | 137 kamera hareketi kataloğu (`templates/INDEX.md`, `engine/cinematic/src/templates/cameras.ts`), ör. dolly zoom oranları. | kamera dili için oku |
| vibegameengine/video-motion-craft, mylxsw/cinematic-video-skill, berlinify/motion-lab (lisans yok), shrimbly/blockout | – | Remotion / reklam / yapay zekâ video hazırlığı. | gerek yok |

## Taşınmaya değer üç teknik (öneri; ilk uygun videoda üslup kapısında denenir)
1. **Mürekkep ya da kâğıt yanığı geçişi** (gürültü eşikli dissolve): yarıçapa `1+0.08·sin` düzensizlik, yeni sahnenin 20–42 px önünde giden mürekkep kenarı, geçiş bitince maske kalkar. Kural gereği yalnız mekân/zaman sıçramasında.
2. **Derinlikli toz ve kor parçacıkları:** zerrelerin çoğu uzakta, her biri kendi yolunda; tamamen `t`'ye bağlı (film.js ileri-geri sarma ve paralel işçilerle uyumlu). Donuk planlara hayat, ateş, toz.
3. **Çok düzlemli 2.5D paralaks:** katman katsayıları 0.35 / 0.7 / 1.4 (aralarında ≥2 kat), uzak katman solgun ve sisli, hareket bir noktada durur. Bulanıklık tam ekrana uygulanmaz (SwiftShader notu).

Zaten elimizde olanlar: kayık baskı (`kafka`), halation (`mary-stuart/lib/film.js`). Shotcraft parametreleri sahte malzemeyle ayarlanmış; gerçek karede yeniden sınanır.
