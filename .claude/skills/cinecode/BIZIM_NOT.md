# cinecode: Zaman Kuryesi için kullanım notu

Kaynak: https://github.com/sarpstar/cinecode (MIT; yazar Sarp Yıldız). Alındığı sürüm: commit c8a3e75 (13 Kasım 2026). `docs/media/` (13 MB tanıtım görselleri) alınmadı.

## Nasıl kurulu
- `.claude/skills/cinecode/` altında, ama `disable-model-invocation: true` ile: **yalnız kullanıcı `/cinecode` yazınca çalışır.** Kanal videolarında kendiliğinden devreye girmez.
- Nedeni: cinecode kendi iş akışını yürütür (kendi soru turu, kendi jürisi, kendi dış sesi: Gemini ya da ücretsiz Türkçe sesler) ve etkinken çalışan kancaları var (UserPromptSubmit, Stop, PreToolUse). Her video isteğinde kendiliğinden açılsaydı bizim hattımızla (CLAUDE.md, kurul, Emrullah sesi, kredi kuralı) yarışırdı.
- **İki kullanım:**
  1. **`/cinecode`:** kanal dışı işler (reklam, kısa film, müzik videosu, deneme) için cinecode'un kendi akışı.
  2. **Başvuru kütüphanesi:** Zaman Kuryesi videolarında aşağıdaki dosyalar elle açılıp okunur. Bu durumda **kanalın kuralları önce gelir:** anlatıcı yalnız ElevenLabs "Emrullah"; kurul ve kapılar CLAUDE.md'deki gibi; kredi harcayan üretim kullanıcı onayıyla.

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

## Arşiv ve hazır malzeme (cinecode'un belgesellerinden ders)
cinecode belgeselleri koddan çizimin yanında gerçek arşiv malzemesi kullanıyor: kamu malı arşiv fotoğrafları ve tablolar (Wikimedia Commons, ABD Ulusal Arşivi NARA, ABD Donanması, Imperial War Museum, Met Müzesi), NASA görselleri, Pixabay görüntüleri, Freesound sesleri, Poly Haven dokuları. Hepsi açıklamadaki künyede tek tek yazılı. Bizim tarih videolarımız (Tarihin Dönüm Noktaları) için de kullanılabilir. Kurallar:
- **Kamu malı (PD) ve CC0:** serbest. Künye yine yazılır (kaynak ve arşiv numarası).
- **CC BY:** künyede ad, eser, lisans ve bağlantı zorunlu.
- **CC BY-SA:** değiştirilerek kullanılırsa (kırpma, renk, canlandırma) "aynı lisansla paylaş" şartı tartışmalıdır. Önce PD/CC0 alternatif aranır; yoksa hukuk kuruluna sorulur.
- **Pixabay Content License:** YouTube'da kullanılabilir; tek başına yeniden satılamaz.
- **Freesound:** her sesin lisansı ayrı (CC0, BY, BY-NC). **BY-NC para kazanan kanalda kullanılmaz.**
- Her varlık `araclar/ASSETS.md`'ye ve videonun `youtube.md` künyesine işlenir; `templates/LICENSES.csv` biçimi kullanılabilir. `lisans-kontrol` becerisi uygulanır.
- Gerçek kişi fotoğrafları için hassasiyet kurulu bakar (CLAUDE.md: gerçek kişiye söz uydurulmaz).
