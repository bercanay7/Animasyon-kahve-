# Kanal Anayasası analizi (v1 → v2) — 2026-10-17

**Tek cümle:** Anayasa iyi bir *kalite ve doğruluk* belgesiydi, zayıf bir *büyüme motoruydu*: kadans, ölçüm, platform bilgisi, lisans/politika ve kapasite modeli ya eksikti ya da gerçekle çelişiyordu. v2 bunları kapattı (`KANAL_ANAYASASI.md`), `YOL_HARITASI.md` bunları bir işletim ritmine bağladı.

**En önemli üç şey (ayrıntı §4):**
1. **Ses lisansı:** şu an kullandığımız `dfki` sesinin veri seti **CC BY-NC-SA 4.0** (ticari kullanım yok, atıf gerekir). `fettah` ve `fahrettin` seslerinin veri seti **CC0**. Henüz gelir yokken sorun değil; ama gelir/sponsor başlamadan çözülmeli ve izleyici sese alışmadan geçmek ucuzdur. (B5)
2. **Üretim yayını geçti:** 3 hazır video (#5–#7) bekliyor, Titanik'in düzeltilmiş sürümü yüklenmedi; kanalın tek dağıtım testi 14 Ekim'e kadar yalnız 1 videoya yapıldı. Öğrenme döngüsü kurulmadan motor ve cilt geliştirilmiş. (B1, B2)
3. **Ölçüm tasarımı gerçekle uyuşmuyordu:** v1, her biri ≥7 videoluk 2×2 deney ve 28. videoda hüküm istiyordu; gerçek hız (Özel video ≈4–6 saat) ve §12 kararları (her videoda yeni cilt) bunu imkânsız kıldı. Yerine teşhis okuması, referans sınıfı ve "çatlak" kuralı konuldu. (B3, B4)

## 1. Neye baktım, neye bakamadım

| Kaynak | Ne için | Not |
|---|---|---|
| `KANAL_ANAYASASI.md` v1 + §12 (8 madde), `RECOMMENDATION`, `DOSSIER-01`, `ADDENDUM-01A`, `ROUND2` (buyume, retention), `VERIFICATION` | kuralların gerekçesi, muhalefet | kurul **simüle**; sayısal eşikler "varsayım" (belgenin kendi sözü) |
| Gerçek veri: Studio ekran görüntüleri, 2026-10-14 (`konsey/veri/`) | kanalın gerçek performansı | 3 gün öncesi; n çok küçük |
| Git günlüğü, `yayin_gunlugu.jsonl`, sürüm künyeleri, konu havuzu | üretim hızı, durum | günlükte yalnız #5–#7 var |
| Yerel `MODEL_CARD` dosyaları (`dfki`; `fettah`, `fahrettin` GitHub sürüm dosyasından indirildi) | ses lisansı | **birincil kanıt** |
| 17 web araması (özetler) | platform durumu, Ekim 2026 | tümü ikincil; resmî YouTube Help sayfaları açılamadı |
| Bakamadığım | canlı Studio verisi (bağlı araç yok: Supermetrics "YouTube" ve "YouTube Public Data" kimlik doğrulamasız, Metricool'de yalnız Navitas markası), rakip kanallar, 14 Ekim sonrası yayın durumu | — |

## 2. Gerçek veri ne diyor (Studio, 14 Ekim 18:17 yerel)

Kanal 4 günlük: 28 günde **1.728 görüntülenme, 4,8 saat, +5 abone (toplam 6).**

| Video | Yayın | Ort. izlenme | Ort. % | Views |
|---|---|---|---:|---:|
| Emu ("Ordu 20.000 Kuşa Savaş Açtı…") | 11 Eki | 0:22 | %54,2 | **1.624** |
| Dans ("Bir Kadın Dansa Başladı…") | 12 Eki | 0:23 | %56,9 | 25 |
| Antik Mısır maaş | 10 Eki | 0:19 | %62,4 | 23 |
| Zanzibar | 10 Eki | 0:27 | %64,1 | 22 |
| Romalılar (kendi kendini tamir eden beton) | 10 Eki | 0:49 | %103,7 | 19 |
| Moğol yam postası | 10 Eki | 0:32 | %53,0 | 15 |
| Titanik v1 (6 sa 43 dk) | 14 Eki | — | %275 | 9 |

**Okuma (hipotez, kanıt değil; n≈1):**
1. **%94'ü tek video (Emu).** Dağıtım "var/yok" gibi davranıyor: Emu Shorts akışından %97,2 (1.625 görüntülenme); Dans akışta **%0** (28 görüntülenme: arama %71,4, kanal sayfası %28,6); diğer videolar 15–25 görüntülenmede kalmış (gösterilme verisi yok).
2. **Emu akış testini geçti, genişlemedi:** ilk günde ≈1.200 görüntülenme, sonra yatay. **Stayed to watch %43 / swiped away %57**; ort. izlenme 0:22 (video 0:40); Engaged views 683 (%42); Unique viewers 643 → **izleyici başına 2,53 izleme**; abone +2 (%0,12).
   → Kitlenin yarısından fazlası ilk saniyelerde kayıyor; kalanlar ortalama iki buçuk kez izliyor. Bu, **içeriğin değil ilk saniyenin** (kart, ses, ilk cümle) sorununa benziyor.
3. **Canlı Emu sürümü 0:40, ilk sesli sürüm** (11 Eki); repodaki son sürüm 43 sn ve yeni ses (12 Eki). v1'in "Emu baz çizgisi" bu yüzden eski sesle ölçülmüş; ses etkisi hakkında hüküm çıkmaz.
4. **Arama niyeti:** Dans'ın arama terimleri "dans eden kadın", "gece dans eden kadın", "sırf kadın" — başlık yanlış niyet çekti; Emu'nun arama terimleri konuyla ilgisiz (toplamın %1,4'ü).
5. Romalılar %103,7 (n=19) ve Titanik %275 (n=9) tekrar izlemeyi gösterir ama örneklem anlamsız (kendi izlemelerimiz dahil olabilir).

## 3. Anayasa'nın karnesi

| Bölüm | Karne | Neden | v2'de |
|---|---|---|---|
| §0 üç karar | Eskimiş | gerçek kararlar §12'de ve oturumlarda | karar günlüğü |
| §1 kimlik | İçi boş | "tek yazı ailesi/altyazı/vurgu rengi" §12-1 ile çelişiyor | gerçekten sabit olanlar yazıldı |
| §2 cilt | Kalktı | tavan 3 + yazı-tura §12-1 ile iptal | cilt politikası + okunabilirlik değişmezleri |
| §3 kanca | **Güçlü** | tek ölçülebilir kaldıraç; Emu verisi ilk-saniye tezini destekliyor | korundu + ilk 2 sn ilkesi |
| §4 ses | İyi, lisans kör noktası | `dfki` = CC BY-NC-SA | lisans kapısı + geçiş |
| §5 kapılar | **Güçlü** | 7 yanıltıcı ifadeyi yakaladı (VERIFICATION) | + Uyum kapısı, kaynak sınıfı ●◐○ |
| §6 hat | Gerçekçi değil | video başı ≤90 dk, haftada 5 | kulvarlar, kapasite, haftada 3 |
| §7 metin | İyi | — | + atıf satırı, kare-0 kapak |
| §8 ölçüt | Yön doğru, mekanik gerçekçi değil | 2×2 ≥7/hücre, +%30 hedef | teşhis okuması, referans sınıfı |
| §9 tetikleyici | Eskimiş | cilt rotasyonu vb. | yeniden yazıldı |
| §10 eylemler | Bayat | Titanik "yayınlanmadan önce" denmiş; v1 canlıydı | güncellendi |
| §11 sınırlar | Güncellendi | — | — |
| §12 kullanıcı kararları | Korundu | — | +madde 9, 10 |

## 4. Bulgular

**B1. Deney tasarımı gerçekle uyuşmuyor.** v1 §8: hücre başına ≥7 video, 2×2 (cilt × kanca), hüküm 28. videoda. §12-1: her konu yeni cilt → "cilt" artık bir eksen değil, her video ayrı bir ilk kare. Özel video ≈4–6 saat; haftada 3 yayında 28 video ≥9 hafta. Gerçek örneklem: dağıtılmış 1 video. Ek olarak tek bir videonun oranı bile gürültülü: n=300 gösterilmede %43'ün %95 aralığı ≈ ±5,6 puan, 1.000'de ±3,1; videolar arası değişim bundan büyük. **Eylem:** teşhis okuması + referans sınıfı + "aynı yönde ≥3 video" kuralı; 3 öğrenme sorusu (E1 kulvar, E2 kanca türü, E3 saat). (§8)

**B2. Üretim yayını geçti; öğrenme döngüsü kurulmadı.** Zaman çizelgesi: 10 Eki 4 yükleme, 11 Emu, 12 Dans, 14 Titanik v1; 15 Eki #5, 16 #6, 17 #7 üretildi — günlükte üçü de "hazır (yayınlanmadı)". Algoritmaya sinyal ancak yayınla gider; her bekleyen video kaçırılmış bir test. Üstelik her yeni cilt bir mühendislik işi (Pellagra'da bir oturum). **İlerleme birimi "yayınlanmış ve ölçülmüş video" olmalı, "motor özelliği" değil.** **Eylem:** önce birikmişi yayınla (Faz 0), sonra sabit kadans (§15), yayın kuyruğu `YOL_HARITASI.md` §5.

**B3. "Sabit iskelet" içi boşalmıştı.** v1 §1 tek yazı ailesi, tek altyazı biçimi, tek vurgu rengi, ≤8 sabit efekt istiyordu; §12-1 altyazı ve HUD biçemini konuya göre değiştirdi (Sıtma: mono; Dune: serif; Pellagra: Fraunces/Alfa Slab). Bugün gerçekten sabit olanlar: kare-0 kartı + döngü, anlatıcı + ses paleti, anlamlı HUD sayacı, tempo, kapılar. İzleyicinin kanalı tanıyacağı şey yazı tipi değil **ses + kanca dilbilgisi + sayaç + ses tonu**. **Eylem:** §1 bunu açıkça yazıyor; Kısa kulvarında "sezon" cildi öneriliyor (tanınırlık + üretim maliyeti), karar kullanıcıda.

**B4. Ölçüm platform gerçeğinden kopuk ve el emeği.** (a) "Views" Mart 2025'ten (Shorts) ve 24 Ağustos 2026'dan (tüm biçimler) beri ilk karede sayılıyor [P] → kalite ölçütü değil. (b) v1'in baz çizgisi "ilk 14 videonun medyanı", hedef "+%30" keyfî. (c) Veri girişi ekran görüntüsü ve elle; şeması yok; günlükte metrik alanı yok. (d) İki darboğazı birbirinden ayırmıyordu: **dağıtıma girmek** (gösterilme) ve **ilk saniye** (stayed to watch). **Eylem:** metrik sırası §8, `olcum/olcum.csv` ve protokol, haftalık gözden geçirme (§16).

**B5. Lisans ve politika boşluğu (yüksek etki).**
- **Ses:** `dfki` MODEL_CARD: "Dataset: marytts/dfki-ot-data, License: CC BY-NC-SA 4.0". Yani ticari kullanım yok, atıf gerekir (şu an hiçbir açıklamada yok), paylaşım aynı lisansla. `fettah` ve `fahrettin`: veri seti NabuCasa/voice-datasets, **CC0**. Üçü de "lessac" ABD İngilizcesi sesinden ince ayarlı; taban modelin kalıtım etkisi belirsiz (hukuki görüş değil). Tek geçişli Whisper ölçümü (aynı 6 cümle, n küçük): `fahrettin` ort. WER 0,083, `dfki` 0,111, `fettah` 0,322 ("Dışkı" → "Beşki") → **CC0 adayı olarak `fahrettin` Whisper'a göre en az `dfki` kadar anlaşılır**; tınıyı kulak belirler: `konsey/ses_testi/lisans_karsilastirma/` (A/B/C kör test).
- **YPP eşikleri [P]:** Kademe 1: 500 abone + 90 günde ≥3 yükleme + 3.000 saat veya 3 M Shorts görüntülenmesi; Kademe 2: 1.000 abone + 4.000 saat veya 10 M Shorts görüntülenmesi. **1 Şubat 2027'den itibaren yeni başvuranlar için 8.000 saat veya 20 M** (ikincil haberler; doğrulanmalı). 6 abone/1,7 bin görüntülenmeyle gelir 2027 başından önce gerçekçi bir hedef değil; bu, **kaliteyi hızdan önde tutmak için serbestlik** de demek.
- **Özgün olmayan içerik [P]:** kitlesel üretilmiş/şablondan çıkma/tekrarlı içerik para kazanmaya uygun değil; yapay anlatım kendi başına engel değil; özgün senaryo ve gerçek editoryal katkı korur. "Sabit iskelet + günlük yayın + TTS" şablon izlenimi verebilir; savunma özgün kaynaklı metin, her konuya özgü görsel, kullanıcı editoryal onayı ve kayıtlardır (§14-U1). §12-1 (her konu yeni cilt) bu açıdan **koruyucu**.
- **Sentetik ifşa [P]:** animasyon/stilize içerik için gerekmez (YouTube blog, 2024); genel TTS için resmî ifade bulunamadı; gerçekçi görsel ve gerçek ses klonu kullanılmaz.
- **Hassas konu:** Pellagra (dışkı), hastalık/tıp konuları eğitici bağlam ve uyarı gerektirir; sarı simge (sınırlı reklam) gelir başlamadan etkisiz.
**Eylem:** §4 lisans kapısı, §14 uyum kapısı; ses kararı Gün 28'de okunur, Gün 60'ta uygulanır.
- **Güncelleme (2026-10-18):** kullanıcı kör testte A'yı seçti; **A = `fahrettin`** (veri seti CC0). Ancak üç Türkçe Piper modeli de "lessac" sesinden ince ayarlıdır; lessac'ın Blizzard 2013 veri seti lisansı yaygın olarak *araştırma amaçlı* okunur ve türev modellere etkisi için yetkili yanıt yok (ikincil: Piper tartışmaları). **CC0 sesler `dfki`'den daha düşük risklidir, sıfır riskli değildir.** Shorts için `fahrettin`'e geçildi; ticari kullanım öncesi insan/lisanslı ses ya da yazılı risk kabulü (G60). Kaynaklar: https://github.com/rhasspy/piper/discussions/271 · https://huggingface.co/rhasspy/piper-voices/discussions/94

**B6. Yayındaki doğruluk borcu.** Titanik v1 canlı (başlık "6 ürkütücü…", konsey bu ifadeleri düzeltmişti; v2 hazır); depoda kaydı olmayan 3 video (Antik Mısır, Romalılar, Moğol) kaynak kapısından geçmemiş; Zanzibar seslendirmesiz (Anayasa "sessiz video yok" diyor); Emu/Dans düzeltmeleri sabit yorumda yapıldı mı bilinmiyor; Emu'nun canlı sürümü eski sürüm. Kanalın tek farklılaşması "kaynaklı ve doğru" olacaksa vitrin önce temizlenmeli. **Eylem:** Faz 0: Titanik v1 ve 4 eski video **özel (private)** (silme yok, analitik kalır, geri açılabilir); Emu/Dans sabit yorum ve başlık düzeltmesi. (§10)

**B7. Niş ve vaat bulanık.** Yayınlananlar: savaş (Zanzibar), kuş savaşı (Emu), dans salgını, Titanik, Mısır maaşı, Roma betonu, Moğol postası; son üç üretim ve konu havuzu ise **"bilinenin ters yüzü" halk sağlığı/bilim** (pellagra, sıtma, sığır vebası, oralit, iyot, kurşunlu benzin, arsenik, karantina). YouTube izleyiciyi konuya göre kümeler; tek tutarlı vaat ve 2–3 sütun, "bu kanal ne verir"i öğretir. **Öneri:** P1 Ters Köşe Dosyaları (≈%60), P2 Tuhaf Olaylar (≈%30; kanalın tek dağıtım alan videosu Emu bu aileden), P3 Takvim Çıpası (≈%10). Karar kullanıcıda. (§15)

**B8. Kapasite modeli yoktu.** v1: video başı ≤90 dk, haftada 5 (40 sn şablonu varsayımı). Gerçek: Özel ≈4–6 saat; render 5,5 dk; TTS 5,5 dk/tur (1–3 tur); QA 0,5 dk. Yani günlük/haftada 5 bu biçimde kapıları aşındırır (v1'in kendi riski: "sessiz hata"). **Eylem:** iki kulvar (Kısa ≈2 saat hedef, Özel ≈4–6 saat), haftada 3, tampon ≥2. Kullanıcı günlük isterse önce Kısa kulvarı yeniden kullanılabilir cilde taşınır. (§15)

**B9. Kurulun yeri.** 21 koltuk simüleydi; çıktısı kural ve doğrulama bulguları açısından değerli (7 yanıltıcı ifade, metrik tanımı karışıklığı, HUD riski) ama sayısal eşikleri kanıt değil (belgenin kendi uyarısı). "Veri yok" sonucunu tekrar etti; veri artık var (az da olsa). **Öneri:** rutin kararlarda kurul toplanmaz; büyük çatallanmalarda (ses lisansı, uzun video pilotu) 3–5 koltuklu kırmızı takım yeterli.

## 5. Korunacak çekirdek (v2'de dokunulmadı)

1. Kare 0 kanca kartı = kapak = son kare; açık döngü. 2. Vaat ödenir; vaat videonun söylediğinden fazlasını içermez. 3. Kaynak kapısı ve mutlak sözcük yasağı. 4. Telaffuz kapısı ve 10 sn kulak kontrolü. 5. `qa.py` kapıları (kare, boş kare, HUD, ilk ses, durağan pencere, freezedetect, LUFS/peak). 6. Kuru erkek anlatıcı, −14 LUFS. 7. Sabit yorum = kaynak + tek soru; 24 saatte cevap. 8. Başlıkta arama niyeti kontrolü. 9. Kapı gevşemez, kadans düşer. 10. §12 kullanıcı kararları.

## 6. Karar bekleyenler (kullanıcıya; öneriyle)

Ayrıntı ve varsayılanlar: `YOL_HARITASI.md` §11. Özet: kadans (haftada 3), Titanik v1/eski videolar (private), Sıtma (yeniden yap), Dune (Aralık çıpası), ses (A/B/C testi → CC0 geçiş), cilt politikası (Özel: yeni, Kısa: sezon), yayın saati (20:00), niş/sütunlar, atıf satırı.

## 7. Bu analizi ne çürütür (bilinmeyenler)

- Gerçek eşikler (gösterilme, stayed to watch) resmî değil; topluluk tahmini. **Kendi referans sınıfımız** (son 5 video) birkaç haftada daha güvenilir olacak.
- Emu'nun bir kez genişlemeyip durması konudan mı kancadan mı sesten mi (eski ses) zamandan mı bilinmiyor; Pellagra ve sonraki 4–5 video bunu ayırmaya başlar.
- 75–150 sn Shorts'ın dağıtımı bilinmiyor: **E1 bunu ölçer**; Pellagra'nın ilk 72 saati ilk işarettir.
- Eski 4 videonun (kayıtsız) gerçek içeriği bu oturumda görülmedi.
- Platform bilgisi ikincil; resmî YouTube sayfaları kullanıcı erişiminde üç ayda bir okunur.

## 8. Kaynaklar (hepsi ikincil, arama özeti düzeyinde; yerel MODEL_CARD'lar birincil)

- Algoritma/Shorts: vidIQ https://vidiq.com/blog/post/understanding-youtube-algorithm/ · quso.ai https://quso.ai/blog/youtube-shorts-algorithm · Fastlane https://www.usefastlane.ai/blog/youtube-shorts-algorithm-2026 · Kineclip https://kineclip.com/blog/youtube-shorts-algorithm-2026/
- Shorts/uzun video ayrımı (YouTube temsilcisi aktarımı): Social Media Today https://www.socialmediatoday.com/news/youtube-shares-new-insight-into-how-to-use-shorts-to-boost-your-channel-per/628491 · Search Engine Journal https://www.searchenginejournal.com/youtube-shorts-algorithm-explained-in-qa-format/
- Stayed-to-watch/benchmark (resmî değil): Bytecap https://www.bytecap.io/research/youtube-shorts-retention-benchmarks · Subscribr https://subscribr.ai/p/youtube-shorts-analytics-metrics-viral · Creator Essentials https://www.creatoressentials.com/glossary/stayed-to-watch/
- Süre: quso.ai https://quso.ai/research/youtube-shorts-length · Bytecap https://www.bytecap.io/research/best-youtube-shorts-length · Adobe Express https://www.adobe.com/express/learn/blog/youtube-shorts-length-study
- Görüntülenme sayımı (24 Ağustos 2026): PPC Land https://ppc.land/youtube-counts-views-from-the-first-frame-across-all-formats-on-august-24/ · vidIQ https://vidiq.com/blog/post/youtube-view-count-update/ · exchange4media https://www.exchange4media.com/digital-news/youtube-changes-how-it-counts-views-videos-to-register-views-from-first-frame-157545.html
- YPP eşikleri: AIR Media-Tech https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide · PPC Land (Şubat 2027) https://ppc.land/new-youtube-creators-face-8-000-hour-bar-for-ad-revenue-from-february-2027/
- Özgün olmayan içerik: NarrationBox https://narrationbox.com/blog/youtube-ai-voice-policy-explained-clearly · YTGrowth https://ytgrowth.io/blog/youtube-ai-policy · AuditSocials https://www.auditsocials.com/blog/youtube-inauthentic-content-policy-2026-mass-produced-ai-generated-monetization-creators-brands
- Sentetik içerik ifşası: YouTube Blog (Mart 2024) https://blog.youtube/news-and-events/disclosing-ai-generated-content · AIR Media-Tech https://air.io/en/youtube-glossary/what-is-youtubes-ai-content-disclosure-policy
- Shorts küçük resimleri: PPC Land https://ppc.land/youtube-ends-2-year-wait-for-shorts-thumbnails-but-blocks-a-b-testing/ · Relevant Audience https://www.relevantaudience.com/social-media-marketing/youtube-shorts-custom-thumbnails-no-ab-testing/
- SEO: Clipspeed https://www.clipspeed.ai/blog/youtube-shorts-seo-optimization-guide.html · vidIQ https://vidiq.com/blog/post/youtube-seo/
- Kadans/huni: Fluxnote https://fluxnote.io/guides/youtube-shorts-upload-frequency-2026 · AIR Media-Tech https://air.io/en/audience-growth/how-to-grow-your-youtube-channel-in-2026
- Ses lisansı: yerel `ses-modelleri/ex_dfki/.../MODEL_CARD` (CC BY-NC-SA 4.0); `fettah`/`fahrettin` MODEL_CARD (k2-fsa/sherpa-onnx `tts-models` sürüm dosyaları; CC0); Hugging Face dfki kartı https://huggingface.co/rhasspy/piper-voices/blob/6fb8245d6d27fef8988272e0c8e9f5018da1bbbf/tr/tr_TR/dfki/medium/MODEL_CARD
- Dune: Part Three (18 Aralık 2026, ABD): Vikipedi https://en.wikipedia.org/wiki/Dune:_Part_Three
