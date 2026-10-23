# Sisifos: Ölümü Zincirleyen Adam

Sisifos efsanesini ve Albert Camus'nün *Sisifos Söyleni* denemesini anlatan, yaklaşık 7 dakikalık animasyonlu YouTube videosu.
Görseller Yunan siyah figürlü vazo resmi üslubunda (yeraltı sahneleri kırmızı figürlü, modern bölüm beyaz zeminli) baştan sona kodla çizilir.

## Teslim dosyaları
| Dosya | İçerik |
|---|---|
| `sisifos.mp4` | 1920×1080, 30 fps, H.264 + AAC, -14 LUFS |
| `kapak.png` | YouTube kapak görseli, 1280×720 |
| `sisifos.tr.srt` | Türkçe altyazı |
| `youtube.md` | Başlık, bölüm zaman damgalı açıklama, kaynaklar, etiketler |

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
python3 tools/mix.py              # → audio/mix.wav
node render.js sisifos.mp4        # WORKERS=4 MB=4 CRF=20; FROM/TO ile kısmi render
python3 tools/srt.py              # altyazı
SCENE=kapak node shot.js out 5    # kapak karesi
node shot.js out 12.5 140.2       # tek tek kareler (inceleme için)
```
