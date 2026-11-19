# Lemo-Opuscar kataloğu (kanal için seçki)

Kaynak: [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), commit `3a7132b` (12 Kasım 2026, sürüm 2.x). Depoda 99 üslup var. İndirmek için:
```bash
bash araclar/lemo/getir.sh <slug> [hedef]
```
Betik seyrek klonla yalnız o üslubu indirir ve depoya hiçbir şey yazmaz.

## Lisans: 2.0 ile değişti, dikkat
| Ne | Lisans | Bizim için anlamı |
|---|---|---|
| Kod (`demo/*.js`, `core/`, `tools/`) | MIT | Motor dosyaları videonun `lib/vendor/` klasörüne lisans metniyle kopyalanabilir (İkaros'taki `silk.js` gibi). |
| Belgeler (`STYLE.md`, `DEMO.md`, bütün `.md` dosyaları, görsel üretim istemleri) | CC BY-NC 4.0 + ek izin | Okunur, uygulanır ve kendi filmimiz için uyarlanır; izin ticari filmi de kapsar. Ama **bu depo herkese açık**, o yüzden belgeler buraya kopyalanmaz. Kendi notlarımız kendi cümlelerimizle yazılır. |
| Demo filmleri, posterler, kareler | CC BY 4.0 | Kullanmıyoruz. |
| Üçüncü taraf varlıklar (font, arşiv görüntüsü, ses) | Her birinin kendi lisansı | Her demonun `CREDITS` dosyasına bakılır. Bazı anlatım sesleri (Edge TTS, Doubao) hiçbir şekilde alınmaz. |
| Clawd karakteri, marka arayüzleri | Lisans yok | Alınmaz. |

- **Yaptığımız filmler bizimdir;** ticari olanlar dahil kredi gerekmez. Yine de açıklamaya iyi niyetle "Üslup: Lemo-Opuscar (LemoLab)" yazılabilir.
- **cinecode'daki 61 tarif** Lemo'nun 2.0 öncesi MIT sürümünden uyarlanmıştı. LICENSE'ın "Earlier versions" maddesine göre o sürümler kendi lisanslarını korur, yani cinecode etkilenmez.

## Bizde zaten olanlar
Lemo'nun bu üsluplarına cinecode tarifiyle (`.claude/skills/cinecode/styles/`) bakılır. Lemo'da bunların **güncel demo motorları** da var (getir.sh ile indirilir):
`engraving` (Milton motorumuzla karşılaştırılabilir), `woodcut`, `ukiyoe`, `shadow-puppet` (Karagöz geleneğine yakın; hassasiyet kuruluna sorulur), `ink-wash`, `stained-glass` (dinî imge riski var, hassasiyet kurulu), `papercut-red`, `paper-lantern`, `silent-film`, `watercolor`, `impasto`, `silkscreen-poster` (İkaros'ta kullanıldı).

## Yeni gelenlerden kanala uyanlar
Gözlem `style.json` dosyalarından alındı. "GL" sütunu motorun three.js/WebGL kullandığını gösterir: başsız Chromium'da yazılımsal GL ile yavaş render edilir, bu yüzden önce 15 sn deneme yapılır.

| Seri | Slug | Ne | GL | Dikkat |
|---|---|---|---|---|
| Tarihin Dönüm Noktaları | `map-explainer` | Küreden boğaza inen 3B harita anlatımı | var | Çok uygun: Viyana 1529, Zanzibar, Çanakkale. Uydu mozaiklerinin lisansı `CREDITS`'te; yapay zekâ görseli yok |
| | `comic-history` | Toprak el değiştirdikçe yırtılan, yapıştırılan karikatür harita | az | Karakter parçaları **yapay zekâyla üretilmiş** (demo `CREDITS`: Codex görsel üretimi). Karakterler alınmaz; yalnız harita ve kukla iskeleti tekniğine bakılır |
| | `newsreel` | 1920'ler haber filmi: ara yazı, gren, arşiv | yok | Arşiv görüntüsüne dayanır. Kamu malı kaynak gerekir (cinecode `BIZIM_NOT` arşiv kuralları) |
| | `vintage-collage` | Eski gravürlerden kolaj | az | Kaynak gravürler kamu malı olmalı; Doré/Milton çizgimizle akraba |
| | `visual-investigation`, `kino-montage` | Kaynakları tek saatte birleştiren yeniden kurgu; konstrüktivist montaj | az | Arşiv ağırlıklı. 29 Ekim ya da Medici gibi belgesel videolarda yapı fikri olarak |
| | `dark-documentary` | Radar taramalı bilim ve mühendislik belgeseli | var | Bilim tarihi bölümleri için |
| Mitler ve Felsefe | `gilded-illumination` | Altın varaklı, aydınlatmalı el yazması resmi | var | Tamamı kodla çizilmiş (`CREDITS`: fotoğraf ve yapay zekâ görseli yok). Masal ve mit için güçlü. **Hassasiyet:** Hristiyan el yazması çağrışımı var, kurul görüntüye bakar. İslam minyatürüne benzetilmez |
| | `scratch-film`, `printed-long-take` | Kazıma film; kazıma tahta tek plan | var | Karanlıkta ışıkla anlatım (Orfeus/Hades gibi yer altı sahneleri) |
| | `firefly-pointillism` | Işık noktalarıyla anlatılan masal | yok | Kısa doruk sahnesi ya da Shorts |
| | `double-exposure`, `silhouette-rhythm` | Çift pozlama açılış; vuruşa oturan siluetler | az | Bölüm açılışı ya da Shorts. Kanalın koyu siluet diliyle uyumlu |
| | `one-line` | Tek kesintisiz çizgiyle bir hayat | yok | Biyografi özetleri (Milton'ın hayatı gibi kısa ara bölümler) |
| Kitaplar / Ekrandaki Felsefe | `stick-explainer`, `chalkboard`, `colored-pencil` | Çöp adam bilim anlatımı; tebeşir tahtası; renkli kalem kesit çizimi | az | Psikoloji ve felsefe kavram anlatımları (TED-Ed çizgisi) |

### Narkissos taramasında ölçülenler (18 Kasım 2026)
Ayrıntı ve gerekçe: `narkissos/uretim_plani.md` §5. Süreler başsız Chromium + SwiftShader'da, üretimdeki JPEG `.96` hattıyla ve tek işçiyle, boş makinede ölçüldü. GL'li motorlarda `render(t)` hızlı döner; asıl bedel GPU'nun bitmesinde ve kare okumada ödenir. O yüzden hep çizim + okuma + JPEG toplamı ölçülür.

| Slug | Ne | Kare süresi | Not |
|---|---|---|---|
| `risograph` | Saydam üst baskı, yarım ton, kayık plakalar | 0,28–1,18 sn; hareket bulanıklığıyla medyan 2,3 sn; 4 işçide ~1,8 kat hızlanma | Su yansıması gölgelendiricide hazır (`riso.js:50–68`). Demo 24 fps için yazılmış; tohumu çağıran kod veriyor (`film.js:327`). CREDITS'e göre görsellerin hepsi kodla üretilmiş |
| `scratch-film` | Siyah emülsiyona kazınmış titrek çizgi | 0,13–0,41 sn; doğrusal ölçekleniyor | Saf Canvas2D, klasik betik, tohumlu rng. İnce çizgi 168 px'te kayboluyor |
| `neon-tubes` | Neon tabela, su birikintisinde yansıma ve halka | 3,5–5 sn (GPU); 4 işçi hızlandırmıyor | En iyi hazır yansıma motoru (`gl.js` 217–301). Tüp alfabesinde Türkçe harf yok. Demodaki haçlı eczane tabelası alınmaz |
| `paper-lantern`, `impasto` | | 10–37 sn ve 5,8–10,6 sn | Uzun film için fazla yavaş |

**Kanala uymayanlar (bakılmadı):** HUD, oyun, ürün, reklam, borsa ve haber kuşağı üslupları (`hologram-hud`, `pixel-rpg`, `glass-product`, `news-package`, `spreadsheet` …).

## Kullanım sırası (CLAUDE.md "Üslup ve çizim motoru seçimi")
1. Önce kendi motorlarımıza bakılır.
2. Uymuyorsa önce cinecode tarifine, ardından bu kataloğa bakılır.
3. Seçilen üslup `getir.sh` ile indirilir:
   - `STYLE.md` okunur;
   - `CREDITS` denetlenir;
   - motorda ağ çağrısı aranır (betik listeler);
   - 15 sn'lik deneme render yapılır.
4. Motor bizim çekim sistemimize takılır (`film.js`: `S()`, `Wd()`). Lemo'nun kendi akışı (soru turu, dış ses, müzik üretimi) kullanılmaz.
5. Kopyalanan her motor dosyası `araclar/ASSETS.md`'ye commit numarasıyla yazılır.
