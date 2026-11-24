# Öğretmenler Günü hareketli Story: After Effects tekniklerinin kod karşılıkları

After Effects yok; aynı teknikler açık kaynak projelerden formül olarak alınıp `animasyon.html` içinde yeniden yazıldı (kod kopyalanmadı).

| AE tekniği | Bizde | Kaynak (lisans) |
|---|---|---|
| Easy Ease (F9) ve hız grafiği "influence" | `bezier()` çözücü; `E.easy` = (.333,0,.667,1), `E.arrive` = gelişte %80 influence | bodymovin `keyframeHelper.jsx` dönüşümü, gre/bezier-easing (MIT) |
| Inertial bounce ifadesi | `inertia()`: hız × sin(f·t) / e^(d·t); elmanın oturuşu | graymachine/Animoplex ifadesi (lisanssız: yalnız formül) |
| Spring (yay) | `spring()` kapalı çözüm; etiket, ayraç, yaprak, harfler | Motion Canvas `spring.ts` (MIT), cinecode `motion.md` (MIT) |
| Trim Paths | `pathLength="1"` + `stroke-dasharray`; çerçeve, kitaplar, sap, vurgu çizgisi | Motion Canvas `Curve` (MIT) |
| Text Animator + range selector | harf harf opaklık + y + bulanıklık, 0,055 sn stagger | lottie-web `TextSelectorProperty.js` (MIT) |
| Track Matte / maske açılışı | logo ve "İyi ki varsınız," taban çizgisinin arkasından yükselir | — |
| CC Light Sweep | başlıkta tek ışık bandı (maske gradyanı) | cinecode `lightSweep` (MIT) |
| Wiggle | `wiggle()`: tohumlu, zamana bağlı; süzülen tebeşir tozu | — |
| Squash & stretch, ikincil eylem, follow-through | elma konarken %6 ezilme, kitaplar 3 px çöker, toz bulutu; yaprak saptan sonra gelir | cinecode `motion.md` (12 ilke) |
| Motion blur (180°, faz −90°) | her kare 4 alt kare, ffmpeg `tmix` ile ortalama | AE / Remotion CameraMotionBlur mantığı (formül) |

Bilerek alınmayanlar: Remotion (3 kişiden büyük şirkette ücretli lisans), Theatre.js Studio (AGPL), GSAP eklentileri (açık kaynak değil), lisanssız gist kodu.
Araştırmacının "logo 7,4. saniyede gelsin" önerisi alınmadı: reklam verisine göre marka ilk 2 saniyede görünmeli (cinecode `purpose-ad.md`).

## Komutlar
```bash
python3 ses.py                       # ses.wav (yalnız numpy, sentez)
node video.js story                  # 1080x1920 Story/Reel
node video.js feed                   # 1080x1350 gönderi
FRAMES=0,75,150 node video.js story  # yalnız kontrol kareleri (kareler/)
MB=1 node video.js story             # hareket bulanıklığı kapalı, 4 kat hızlı
```
Önizleme: `animasyon.html?play` tarayıcıda döngüde oynar. Sesin son düzeyi `-16 LUFS` (yayın kopyasında ffmpeg ile limiter + loudnorm).
