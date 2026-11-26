# Şart: dikey mitoloji Shorts serisi (ilk deneme, 23 Kasım 2026)

Her Shorts bir mitin içindeki **tek cümlelik şart**: bir uyarı, bir yasak, bir koşul. İzleyici adı tanıyor, sonu biliyor, ama ne söylendiğini hatırlamıyor.
İlk saniyede şart duyulur ve yazılı görünür; görüntüde onu çiğnemek üzere olan figür vardır. Mit baştan anlatılmaz; şartla çiğnendiği an arasındaki mesafe kısaltılır.
Yön: kullanıcının yön metni (`analiz/2026-11-24-shorts-yon-prompt.md`, Fable). Bu deneyin kararları ve yönün yetmediği yerler: `geriye_bakis.md`.

| Shorts | Şart (ilk saniye) | Çiğnendiği an | Süre | Görüntü |
|---|---|---|---|---|
| `narkissos/` | “Oğlum uzun yaşayacak mı?” → “Kendini tanımazsa.” (kâhin Tiresias) | “O benim.” (0:12) | 28,1 sn | filmin vazo planları, dikey mercekle; yüz ve yansıması üst üste |
| `gilgamis/` | “Haydi: altı gün yedi gece uyumadan dur.” (Utnapiştim) | “uyku hemen bir sis gibi üstüne çöktü” (0:05) | 34,5 sn | dikey için yazılmış kil kabartma planları; yedi ekmek tablet satırları gibi üst üste |

## Hat (komutlar depo kökünden)
```bash
python3 shorts-sart/tools/ses.py shorts-sart/narkissos          # kesitleri filmin vo.wav'ından keser; zaman.js + timeline.js
python3 shorts-sart/narkissos/audio/score.py                    # bu Shorts'un müziği → audio/music.wav
python3 shorts-sart/tools/miks.py shorts-sart/narkissos         # -14 LUFS miks + müziğin saniye saniye düzeyi
node shorts-sart/tools/kare.js shorts-sart/narkissos /tmp/k --her=1   # kurguya bakış kareleri (--yazisiz: sessiz okuma testi)
node /home/user/Animasyon-kahve-/shorts-sart/tools/render.js shorts-sart/narkissos   # 1080×1920, 30 fps, H.264 CRF 18, BT.709
```
Gılgamış için `gilgamis/vo/vo.wav` önce filmin kendi aracıyla üretilir (`cd gilgamis && python3 tools/build_vo.py`; depoya girmez).

## Dosyalar
- `lib/sart.js`: ortak çalışma zamanı. İki kip: `film` (filmin planları film zamanında, kesit kesit; dikey mercek anahtar kareleri) ve `yerli` (dikey için yazılmış planlar Shorts zamanında). Üstüne kanca yazısı (ilk karede tam), sözcük sözcük altyazı.
- `<proje>/kurgu.js`: kesitler (`a`: filmdeki anlatım aralığı; `v`: görüntünün film zamanı; `lens`: [u, cx, cy, k]), kanca, altyazı. Saf JSON; ses aracı da okur.
- `<proje>/index.html`: `<base href="/<film>/">` ile filmin motorunu yükler (sunucu depo kökünden: `tools/sunucu.js`).
- `gilgamis/core_dikey.js`: filmin `core.js`'i, yalnız W×H = 1080×1920. `gilgamis/sahneler.js`: altı dikey plan.

## Kurallar (bu serinin)
- **Şart ilk saniyede:** yazı ilk karede tam görünür (giriş animasyonu yok). Sesin şarta girdiği an eldeki kayda bağlı: Gılgamış'ta "altı gün" 1,0 sn'de, Narkissos'ta ilk söz 0,2 sn'de annenin sorusu, "Kendini tanımazsa" 2,1–3,2 sn (25 Kasım; ilk sürümde 3,0–4,1 sn, "Kâhinin cevabı tek bir şarttır" girişiyle). İçeriksiz giriş sözü ilk saniyeye konmaz.
- **Ses filmden, müzik yeni:** anlatım kesitleri gerçek duraklamalarda kesilir (`ses.py` kelime bölünürse uyarır). Müzik her Shorts için o Shorts'un zaman çizelgesine yazılır; filmin müziğini kesmek kesit uçlarında sıçrar.
- **Döngü:** son kare ile ilk kare aynı mekânda/tonda; müzik son 0,8 sn söner, ilk 20 ms'de açılır (tıkırtısız başa dönüş).
- **Güvenli alan:** yazılar x 140–940, y 220–1440 (üstte arama çubuğu, sağda düğmeler, altta başlık ve kanal adı).
- **Dikey mercek sınırı (film kipi):** `k ≥ 1,78` ve `cy ≥ 960/k`; altında dünyanın dışı ve meander bordürü görünür. Ayna çevirmeli planlar (`s2_flip`) mercekte bozulur: tuval ortasından aynalanır, yazılar karenin dışına düşer (Narkissos P061 bu yüzden kullanılmadı).
- **Ölçüt:** izlemeye devam eden ≥ %60 (CLAUDE.md). İlk iki üç Shorts okunmadan kalıp kural sayılmaz.

## Açılış laboratuvarı (25 Kasım; kullanıcının kararı: Instagram hesabı açılmaz)
Kaynak fikir: Instagram "trial reels" sistemi (aynı gövde, çok sayıda açılış, takipçi olmayanlara deneme). YouTube'da deneme yayını yok; aynı Shorts'u farklı açılışlarla birden çok kez yüklemek tekrarlayan içerik riski taşır ve küçük sinyali böler. Bu yüzden yalnız YouTube'a uyan yarısı alındı:
- **Her Shorts'tan önce 20 açılış adayı** yazılır (Fable ya da başkan); yapısı en farklı 3–5'i kalır (aynı cümlenin yazılışları değil: şartla, ihlalle, sonuçla, soruyla, sayıyla açılış). Ses önce filmin kaydından aranır; yoksa tek açılış cümlesi kullanıcı onayıyla seslendirilir.
- **Yayına tek açılış çıkar.** Öğrenme Shorts'lar arası sırayla olur: her yeni Shorts bir açılış yapısını sınar, sonuç `analiz/tahminler.md`'ye yazılır. Karar oranla verilir (izlemeye devam eden, 20. ve 48. saat), görüntülemeyle değil; ~1 B izleyicide birkaç puanlık fark yok sayılır.
- **Sıra:** soru (Narkissos, 24 Kasım) → şart (Narkissos 26 Kasım, Gılgamış 4 Aralık) → sonraki Shorts ihlalle ya da sonuçla açılır (ör. Gılgamış kaydında hazır: "Gılgamış oturdu ve uyku hemen bir sis gibi üstüne çöktü." / "Ölümü yenmeye gelen adam, bir uykuyu yenememişti.").
