# Açık kaynak adaylar (inceleme kaydı)

İncelenen depolar: alınanlar, alınmayanlar ve sonraki işe kalanlar. Bir şey alınmadan önce `lisans-kontrol` becerisi uygulanır ve `araclar/ASSETS.md`'ye yazılır.

**Ölçütler (sırayla):**
1. Ticari kullanıma izin veren lisans (kanal para kazanıyor).
2. Ücretli API'ye ya da yapay zekâ görsel/video üretimine bağlı olmamak.
3. Ağ çağrısı ve telemetri olmamak.
4. Hattımıza takılabilmek: Canvas 2D ya da tarayıcı, kare kare deterministik render, `S()`/`Wd()` çekim sistemi.
5. Bizde gerçekten eksik bir şeyi karşılamak.

## 14 Kasım 2026 turu
| Depo | Karar | Gerekçe |
|---|---|---|
| JDhruv14/line-art-animation (MIT) | **Alındı** | Yürüyüş/koşu çözücüsü, yay ve sarkaç bizde yoktu. Ayak kayması sıfır. `araclar/hareket/` (uyarlama), `araclar/vendor/line-art-animation/` (özgün). SVG çizgi-sanat üslubu da yeni bir üslup seçeneği (kitap ve felsefe videoları). |
| lemomo-ai/lemo-opuscar 2.x | **Kısmen** | 38 yeni üslup ve güncel motorlar. Kod MIT; belgeler CC BY-NC (film yapma izniyle). Depo herkese açık olduğu için belgeler kopyalanmadı: `araclar/lemo/KATALOG.md` + `getir.sh` (sabit commit). |
| Anil-matcha/vox-ai-motion-graphics-generator (MIT) | **Alınmadı** | Bütün hat ücretli MuAPI'ye bağlı: görseller yapay zekâyla üretiliyor, hareket Veo ile, ses MiniMax TTS ile. Kanalın kodla çizim, Emrullah sesi ve kredi kurallarıyla çelişir. Hikâye iskeletleri `yonetmenlik` becerisinde zaten var; müzik kısma (sidechain ducking) `mix.py`'de zaten var. "Vox üslubu" da başka bir markanın görünümünü taklit eder. |
| iart-ai/motion-skills (MIT dizin) | **Paket paket** | Çoğu Remotion, After Effects ya da ücretli yapay zekâya dayanıyor ve alınmadı. `generative-illustration-skills` LICENSE dosyası yok; OpenRouter, Recraft ve Lyria kullanıyor; alınmadı. Değerli olan `javascript-animation-skills` (aşağıda). |

## Sonraki işe kalan adaylar (araştırma ajanının raporu; başkan doğrulaması gerekir)
| Aday | Lisans (rapora göre) | Ne işe yarar | Öneri |
|---|---|---|---|
| iart-ai/javascript-animation-skills | MIT | `soundtrack/scripts/sync-check.mjs`: kesme vuruşa ±100 ms içinde düşüyor mu, kesmede +6 dB'yi aşan "irkilten" ses sıçraması var mı. Ses/miks kurulunda eksik bir ölçüm. | **Ses kapısında uyarla.** `ai-music.md` (OpenRouter) alınmaz. |
| acamposuribe/p5.brush | MIT | Kurşun kalem, kömür, suluboya dolgu, tarama; tohum verilebilir. p5'siz sürümü var. | **Üslup karesinde dene.** WebGL2 zorunlu; başsız Chromium'da hız ve kare kare aynı sonucu verip vermediği test edilir. |
| MontrealCorpusTools/Montreal-Forced-Aligner | kod MIT; Türkçe model ve sözlük CC BY 4.0 | Whisper'sız zorunlu hizalama; metni bildiğimiz için daha kesin kelime zamanı verir. | **Al, ama kurulum kullanıcının ortamında** (conda). Model atfı açıklamaya yazılır. İkaros'taki `hizala.py`'nin yerini tutabilir. |
| KilledByAPixel/ZzFX, chr15m/jsfxr | MIT / Unlicense | Prosedürel küçük efektler (vuruş, tık, kıvılcım), WAV çıktısıyla. | **Al** (`lib/sfx.js` → `export_sfx.js` hattına). |
| abey79/vpype, LingDong-/fishdraw | MIT | Kalemli çizici tarama yöntemleri; prosedürel gravür benzeri çizim. | Yalnız fikir (gravür motoru için). |
| theatre-js/theatre | çekirdek Apache-2.0, studio AGPL | Anahtar kare ve kamera düzenleyici. | Yalnız fikir; bakımı durmuş, `film.js` ile çakışır. |
| readbeyond/aeneas | AGPL-3.0 | Cümle düzeyinde hizalama. | Alma: 2020'den beri bakımsız; MFA daha iyi. |
| MahmoudAshraf97/ctc-forced-aligner | kod BSD-2, model **CC BY-NC** | Hizalama. | **Alma:** model ticari kullanıma kapalı. |

Bulunamayanlar:
- **Lisansı doğrulanmış bir kapak/akış test aracı:** bizim `mkfeed.py` yeterli.
- **`figure.js`'ten güçlü bir 2D iskelet/IK:** Spine ücretli, Rive'ın düzenleyicisi kapalı kaynak.

## 17 Kasım 2026: kapak araçları ve bir beceri
| Aday | Karar | Gerekçe |
|---|---|---|
| sybil-solutions/inference-optimisation-skill (MIT) | **Alınmadı** | Bilgisayarda çalışan dil modeli sunucusunu (vLLM, SGLang, llama.cpp) hızlandırır; hattımızda yerel model yok. Yöntemi ("önce tavanı hesapla, tek şey değiştir, ölç") Ran'ın "önce ölç, sonra hızlandır" dersinde zaten var. |
| Kapaktan tıklanma tahmini yapan modeller: TubeCLIP, z03 (Hugging Face), YT-ML, vortexv7/engagevision-yt | **Alınmadı** | TubeCLIP ve z03 ticari kullanıma kapalı (CC BY-NC). EngageVision MIT ama 2024'ten beri güncellenmeyen küçük bir deneme. Hepsi yüz ağırlıklı kanallarla eğitilmiş; siluet ve gravür kapağını doğru puanlamaz. |
| Akış önizleme eklentileri (PrevYou vb.) | **Gerek yok** | Asıl PrevYou deposu bulunamadı (GitHub aramasında yalnız boş kopyalar). Kapak test setindeki akış taklidi (`mkfeed.py` mantığı) aynı işi görüyor. |
| matthias-k/DeepGaze (göz izleme tahmini) | **Alınmadı** | Depoda LICENSE yok (`setup.py`'de MIT satırı yorumda), yani kullanım izni yok; büyük model ister. |
| Spektral artık belirginlik (Hou & Zhang, CVPR 2007) | **Yazıldı** | `araclar/kapak/odak.py`: eğitilmiş model yok, yalnız numpy + PIL; parlaklık + iki renk karşıtlığı kanalı. Kanalın 14 kapağında denendi: Sisifos'ta anahtar, Milton'da alev, Kafka'da elma 1. odak çıktı. Tıklanmayı tahmin etmez; "göz amaçladığımız yere mi gidiyor?" sorusunu ölçer. |
