# cinecode: Zaman Kuryesi için kullanım notu

Kaynak: https://github.com/sarpstar/cinecode (MIT; yazar Sarp Yıldız). Alındığı sürüm: commit c8a3e75 (13 Kasım 2026). `docs/media/` (13 MB tanıtım görselleri) alınmadı.

## Neden etkin beceri değil, başvuru kütüphanesi
- Özgün `SKILL.md` (burada `SKILL.kaynak.md` adıyla) kendi iş akışını yürütür: kendi soru turu, kendi kurulu, kendi dış ses (Gemini ya da ücretsiz Türkçe sesler) ve her mesajda çalışan kancalar (UserPromptSubmit, Stop, PreToolUse). `.claude/skills/` altına konsaydı her video isteğinde bizim hattımızla (CLAUDE.md, kurul, Emrullah sesi, kredi kuralı) yarışırdı.
- Bu yüzden `araclar/cinecode/` altında duruyor ve otomatik yüklenmiyor. Kullanılacak parça elle açılıp okunur.
- **Kanalın kuralları önce gelir:** anlatıcı yalnız ElevenLabs "Emrullah"; kurul yöntemi ve kapılar CLAUDE.md'deki gibi; kredi harcayan üretim kullanıcı onayıyla.

## Neye bakılır
| Ne | Nerede | Ne zaman |
|---|---|---|
| 61 üslup tarifi (malzeme, çizgi yasası, renk mantığı, kamera, "ne değildir") | `styles/*.md`; `styles/index.json` | Yeni videoda üslup seçerken ve üslup karesini kurarken. Kanala uygun olanlar: `engraving` (Milton'ın akrabası; çizgi şişme yasası), `woodcut`, `ukiyoe`, `shadow-puppet`, `silent-film`, `ink-wash`, `papercut-red`, `paper-popup`, `stained-glass`, `archive-lighttable`, `halftone-dossier`, `briefing-board`, `teardown`, `watercolor`, `risograph` |
| Uzun YouTube belgeseli (perdeler, merak haritası, kaynaklı metin) | `references/film-mode.md`, `references/writing.md` | Senaryo aşamasında; bizim Kahramanın Yolculuğu ve `yonetmenlik` becerisiyle birlikte |
| Bağımsız izleyici / jüri | `references/jury.md` | Kurul brifleri yazılırken (soğuk göz, tahmin testi) |
| Kamera hareketleri, hareket tasarımı | `references/camera-moves.md`, `references/motion.md`, `references/motion-design.md` | Animatik ve sahne üretiminde |
| Ses tasarımı, miks | `references/sound.md`, `scripts/master_audio.py`, `scripts/mix.py` | Ses kapısında; bizim `tools/mix.py` ile karşılaştırarak |
| Tipografi (Türkçesi denenmiş açık lisanslı fontlar) | `references/typography.md`, `references/type-library.json` | Ekran yazısı ve kapak |
| Görüntü denetimi | `scripts/qc.py`, `scripts/scene_check.py` | Render sonrası teknik kalite |
| Müzik videosu, vuruş ızgarası | `references/music-video.md`, `scripts/beat_grid.py` | Shorts'ta müziğe kesme |
| Varlık ve lisans | `references/assets-and-licences.md`, `templates/LICENSES.csv` | Arşiv görseli kullanılırsa |

## Dikkat
- Bazı betikler internetten veri çeker (Wikipedia, NASA, Cleveland Müzesi, iNaturalist, fontsource, kenney.nl). Ağ politikası bunları engelleyebilir; çalıştırmadan önce oku.
- `styles/` içindeki bazı tarifler ayrıca LemoLab'ın MIT lisanslı çalışmasından uyarlanmış (`styles/LICENSE-lemo-opuscar`).
- Tarif dosyaları İngilizcedir. Bizim motorumuz (`milton/lib/`) Canvas 2D; cinecode'un Film modu three.js kullanır. Tarifler motordan bağımsız okunabilir.
