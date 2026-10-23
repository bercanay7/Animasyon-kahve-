# Sisifos: Ölümü Zincirleyen Adam

Sisifos efsanesini ve Albert Camus'nün *Sisifos Söyleni* denemesini anlatan, yaklaşık 7 dakikalık animasyonlu YouTube videosu.
Görseller Yunan siyah figürlü vazo resmi üslubunda (yeraltı sahneleri kırmızı figürlü, modern bölüm beyaz zeminli) baştan sona kodla çizilir.

## Teslim dosyaları
| Dosya | İçerik |
|---|---|
| `sisifos_master.mp4` | 1920×1080, 30 fps, H.264 (CRF 18) + AAC, -14 LUFS (yerel; depoya girmez) |
| `sisifos_shorts.mp4` | Shorts: 1080×1920, 42,7 sn, kelime vurgulu altyazılar |
| `sisifos_en_master.mp4`, `sisifos_en.m4a` | İngilizce sürüm: ekran yazıları İngilizce + İngilizce ses / YouTube'a ikinci ses kanalı olarak eklenecek ses (-2 dBTP) |
| `kapak.png`, `en/kapak_en.png` | YouTube kapakları, 1280×720 ("ÖLÜMÜ ZİNCİRLEDİ" / "HE CHAINED DEATH") |
| `sisifos.tr.srt`, `en/sisifos.en.srt` | Türkçe ve İngilizce altyazı |
| `youtube.md`, `en/youtube_en.md` | Başlık, bölüm zaman damgalı açıklama, kaynaklar, etiketler |
| `yayin.md` | YouTube Studio'da yükleme, İngilizce ses kanalı, Shorts ve zamanlama adımları |

## Nasıl üretildi
1. **Senaryo:** `senaryo.json`. 58 cümle, 8 bölüm. `tts` alanı seslendirme, `alt` alanı altyazı metnidir.
2. **Anlatım:** ElevenLabs, "Emrullah" sesi (eleven_v4, ses etiketleriyle).
   - Her bölümün iki çekimi Whisper ile metne karşı doğrulandı ve en iyisi seçildi (`vo/secim.json`).
   - `tools/build_vo.py` çekimleri cümle aralarındaki boşluk planıyla birleştirip şu dosyaları üretir:
     - `vo/vo.wav`
     - kelime zamanlı `timeline.js`
3. **Animasyon:** `film.html` ve `lib/*.js` (Canvas 2D).
   - Her çekim, anlatımdaki bir cümleye (`S('B04')`) ya da kelimeye (`Wd('B04','rengini')`) bağlıdır. Ses değişirse görüntü de kendiliğinden kayar.
   - `lib/figure.js`: ileri ve ters kinematikli profil figür iskeleti.
   - `lib/act0.js` … `act7.js`: sahneler.
   - `lib/i18n.js`: ekrandaki yazıların İngilizce karşılıkları; sayfa `?lang=en` ile açılınca kullanılır.
4. **Ses tasarımı:**
   - `lib/sfx.js` efekt işaretlerini aynı zaman ifadeleriyle tanımlar. `tools/export_sfx.js` bunları `audio/sfx_events.json` dosyasına yazar.
   - Doğal sesler ElevenLabs ses efekti modelinden (`audio/sfx/*.mp3`). Vuruş, çan, rüzgâr geçişi gibi sesler `tools/mix.py` içinde sentezlenir.
5. **Müzik:** `audio/score.py`. Bu film için numpy/scipy ile sentezlenmiş özgün müzik.
6. **Miks:**
   - `tools/mix.py` müziği konuşma altında kısar ve efektleri yerleştirir.
   - Ortak yankı kullanır, sınırlayıcıdan geçirir ve -14 LUFS / -1 dBTP hedefine getirir.
   - Çıktı: `audio/mix.wav`.
7. **Render:** `render.js`
   - 4 paralel Chromium işçisi çalışır. Her karede 180° obtüratörle 4 alt örnekli hareket bulanıklığı uygulanır.
   - Parçalar yeniden kodlanmadan birleştirilip miks ile paketlenir.

```bash
python3 audio/score.py            # müzik → audio/music.wav
node tools/export_sfx.js          # efekt işaretleri
python3 tools/mix.py --stems      # → audio/mix.wav (+ stems)
python3 tools/mix.py --vo en/vo_en.wav --out audio/mix_en.wav --tp -2.0   # İngilizce dublaj miksi
python3 shorts/mix_shorts.py      # Shorts sesi
node render.js sisifos_master.mp4 # WORKERS=4 MB=4 CRF=18; parçalar .parts/ içinde kalıcı, ONLY=3,7 ile kısmi
SHORTS=1 CHUNK=6 node render.js sisifos_shorts.mp4   # dikey Shorts
Q='lang=en' PARTS=.parts_en AUDIO=audio/mix_en.wav node render.js sisifos_en_master.mp4   # İngilizce yazılı sürüm
python3 tools/srt.py              # altyazı
SCENE=kapak node shot.js out 5    # kapak karesi (SCENE=kapak_en: İngilizce)
node shot.js out 12.5 140.2       # tek tek kareler (inceleme için)
```
