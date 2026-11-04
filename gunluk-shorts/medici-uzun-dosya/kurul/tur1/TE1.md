# TE1 — Teknik kalite: RENDER VE KODLAMA DENETÇİSİ (Medici Parça 1, TUR 1)

Üye: TE1 · Mercek: render ve kodlama (renk etiketi/matris, kare hızı ve ritmi, segment birleşimleri, bandlaşma/blok/gren, bit hızı ve yükleme uygunluğu, ses ölçümü, faststart/konteyner). Diğer üyelerin raporlarına bakmadım.

## 1. Karar

**RED — 8,0 / 10** (eşik ≥9). Konteyner, ses, segment birleşimleri, kare ritmi ve yükleme uygunluğu sağlam. RED'in nedeni tek kesin ve ucuz kusur: **piksel verisi BT.601 matrisiyle YUV'ye çevrilmiş, ama akış BT.709 etiketli** (bölüm 3, madde 1). Oynatıcılar ve YouTube dosyayı 709 olarak açtığı için tüm film hafifçe sapmış renkle görünür (kiremit/kubbe/mühür kırmızıları turuncuya kayar). Düzeltme tek satır; P1'in kodlaması deterministik olduğu için yeniden üretmek ≈17 dk. Madde 1–2 düzelirse alan puanı ≥9 olur.

Alt puanlar: konteyner/yükleme 9,5 · ses ölçümleri 9,5 · segment birleşimleri 10 · kare hızı/ritim 9 · renk etiketi/matris 5 · bandlaşma/blok/gren 8 · hareket bulanıklığı 7,5 · bit hızı/kodlayıcı ayarı 7,5.

**Sınırım (açık yazıyorum):** Videoyu oynatamadım, sesi duyamadım. Her şey ffprobe/ffmpeg ölçümü, çözülmüş kare/PNG incelemesi ve motorun kaynak karesiyle karşılaştırmadır. Kulakla doğrulanacaklar (özel ad okunuşu, miks dengesi, ses-görüntü olay eşleşmesinin hissi) kullanıcıya aittir.

## 2. Ne gördüm / neye dayandım

Kanıtlar `out_p1/medici_P1.mp4`, `out_p1/seg/*`, `render.py`, `compose.py`, `sk.py`, `cilt_medici.py`, `out_p1/audio_report.txt`, `kurul/*` ve kanal tarafında `/home/user/sisifos-wt/sisifos/render.js` + `lib/main.js`. Ölçümlerin hepsi kendi çalıştırmamdır (kurul/ paketine ek).

**Konteyner / kodlama (ffprobe + MP4 kutu ayrıştırma + x264 SEI)**
- H.264 High@4.0, yuv420p 8 bit, progressive, 1920×1080, 24/1 CFR, `avc1`, `colr nclx 1/1/1`, `color_range=tv`. Ses AAC-LC 48 kHz stereo, 205 kb/sn. Süre 601,880 sn, 601.885.753 bayt.
- `moov` ofset 32'de, `mdat`'tan önce: **faststart tamam**. Edit list'ler tutarlı (video media_time 1024/12288 = B-kare gecikmesi, ses 1024 = AAC ön dolgusu); iki akışın başlangıcı 0.
- x264: `crf=19, preset medium eşdeğeri (ref=3, subme=7, me=hex), aq=1:1.0, psy_rd=1.00:0.00, bframes=2, keyint=48, scenecut=40, open_gop=0, vbv_maxrate=9000, vbv_bufsize=18000`.
- Bit hızı: video ort. 7,79 Mb/sn; saniye bazında p10 3,05 · medyan 7,89 · p90 11,74 · p99 16,97 · maks 19,90 Mb/sn; 3 sn pencerede maks 12,3. YouTube önerisi 1080p24 SDR için ≈8 Mb/sn: uyumlu. Boyut 601 MB (sınır 256 GB), yükleme/işleme için sorun yok.
- Tam çözme: `ffmpeg -v error -f framemd5` 14.443 kareyi hatasız çözdü (uyarı/hata yok).
- Küçük eksikler: `pasp` yok (SAR belirtilmemiş), ses dili `und`, Sisifos hattı `language=tur` yazıyor.

**Kare hızı ve ritim**
- 14.443 paketin tamamı süre 512/12288 = 1/24 sn, PTS boşluğu/çakışması yok, tek tip CFR. 14.443 karenin MD5'lerinde **sıfır tekrar** (donmuş/çiftlenmiş kare yok). Siyah/ölü kare yok; yalnız tasarımlı koyu "dip"ler (ort. parlaklık <6: 25,7 · 192,0 · 206,1 · 522,7 sn çevresi, toplam 16 kare). `qa_flow` çıktısında "Donma (ffmpeg): PAS" idi; ffmpeg `freezedetect`'i çalıştırmadım, yerine kare MD5 tekrarı (sıfır) ve kare farkı koşularına baktım. Ardışık kare farkı gren düzeyinin (<0,3) altında kalan en uzun koşu 47 kare (1,96 sn, bir GOP); ortalama optik akış <0,2 px/kare olan en uzun koşu 2,92 sn (358,8 sn) ve 1,96 sn'lik çok sayıda koşu (431–478 sn metin/belge çekimleri). Bunlar donma değil, çok yavaş itme (alt-piksel/kare) + ince gren; yönetmenlik üyelerine bilgi olarak not.
- Çekim içi hareket bulanıksız ölçüm (Farneback akışı, 14.443 kare, 480×270'de global öteleme+yakınlaşma uydurması): çekim içi medyan kamera hızı 0,24 px/kare; p90 3,5; p99 12,5 px/kare (1920 ölçeği). Çekim içi karelerin %27,8'inde >1 px/kare, %11,5'inde (≈59 sn) >3, %5,2'sinde (≈27 sn) >5, %2,3'ünde (≈12 sn) >8 px/kare. Geçiş içi (karelerin %14,9'u) medyan 6,9 px/kare ama geçişlerde yönlü bulanıklık var ve kaliteli (s195 karesi 1:1: temiz yatay çizgilenme, gren üstte). Yani film büyük ölçüde sakin; bulanıksız hızlı çekim içi hareket kısa bir azınlık.

**Segment birleşimleri (her 1200 karede, 12 birleşim)**
- Her segment (13 adet) ayrı ayrı çözüldü; segmentlerin kare MD5 dizisi final dosyanın dizisiyle **birebir aynı** (ilk 14.443 kare); her birleşim karesi (n=1200k) IDR. SPS+PPS 13 segmentte ve finalde **tek ve aynı** (parametre kümesi değişmiyor, oynatıcıda yeniden başlatma riski yok).
- Görsel: 12 birleşim için n−1 | n | n+1 üçlüsü çıkarıldı. İçerik sıçraması yok (1255→1254→1253 yıl sayacı, harita imleci, hesap okulu öğrencileri akışı sürüyor).
- İstatistik: birleşim karesinde kare farkı/yerel medyan oranı sakin çekimlerde 2,1–4,5; **sıradan 48'lik GOP IDR karelerinin oranı da 3,4 (medyan)**. Yani birleşim, normal anahtar-kare tazelemesinden ayırt edilemiyor. Ortalama parlaklık sıçraması ≤0,57 düzey (200,0 sn birleşimi geçiş ortasında, beklenen). IDR karesinin HF enerjisi komşuya oranı 0,97–1,06 (nabız yok).
- Determinizm kanıtı: çekirdeğin kare üreticisi (`compose.Program(part=1).frame(n)`) iki ayrı süreçte, farklı sırayla, n=3000/1200/7008 için **bit-birebir aynı MD5**'i verdi. 1199/1200 karelerinde de aynı. Yani paralel/segmentli/kısmî yeniden render güvenli.
- Tek gerçek birleşim-benzeri kusur **kuyrukta**: aşağıda madde 5.

**Renk matrisi (kesin kanıt, üç yoldan)**
1. Sentetik: motorun `ff_cmd`'siyle (rgb24 → `-pix_fmt yuv420p -colorspace bt709`) 8 renk yaması kodlayıp YUV'yi okudum. Saf kırmızı Y/U/V = 81/90/240 (709 beklenen 62,6/102,3/240; **601 beklenen 81,5/90,2/240**). Yeşil Y=145 (709: 172,6; 601: 144,6). Matris 601; etiket 709. 709 olarak çözülünce kırmızı (255,0,0)→(255,23,0); yeşil (0,255,0)→(0,215,0).
2. Gerçek kareler: `compose.Program.frame(n)` kaynak karelerini (19 kare, 1,0–601,0 sn) final dosyadan çözülen karelerle karşılaştırdım. PSNR 601 çözümünde 709 çözümünden **her karede 0,3–2,4 dB yüksek** (ör. n=24: 38,09 vs 36,74; n=648: 38,78 vs 36,88; n=8412: 42,06 vs 39,61). Oynatıcıya giden (709) görüntüde çoğu karede ortalama ΔRGB R ≈+0,6…+2,4, B ≈−0,3…−1,7 (sıcak/sarı kayma). Doymuş bölgelerde (örnek: n=24, 192, 5520, 9840): kiremit/kubbe kırmızısı R +5…+6, **G +6…+11** (turuncuya kayar); koyu mavi G +2,4; altın/sarıda kareye göre B +1…+16 (n=24'te +16).
3. Düzeltilmiş boru hattını da denedim: `-vf scale=in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p` + `-color_range tv`. Aynı 8 yamada 709 çözümüyle gidiş-dönüş hatası ≤2 düzey (önceden 23/40 düzeye varıyordu).
- Kanal karşılaştırması: Sisifos `render.js` bunu doğru yapıyor (`scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709` + 709 etiketi). Medici hattında bu satır yok.
- Etiket tutarlılığı kendi içinde doğru (VUI + `colr` ikisi de 709, limited); sorun etiket değil piksel verisidir.

**Bandlaşma / blok / gren**
- Gren (6 desenlik `n%6` döngüsü, σ≈1,35 düzey) + kâğıt dokusu sakin gökyüzünü bandlaşmadan koruyor: t=1,0 sn gökyüzü degradesi JET renk haritasıyla büyütüldü, kontur yok.
- 16 px blok sınırı ölçümü (1204 kare, her 12. kare): oran medyan 0,986, p99 1,104. Tek aykırı 1,546 (209,0 sn, ort. parlaklık 10: koyu "çukur" sahnesi); 5× kazançla bakınca blok yok, eşmerkezli halkalar var.
- Düz-degrade (yassı plato) ölçümü: çerçevenin degrade bölgelerinin yerel std<0,6 olan payı: medyan %0, p90 %2,95, p99 %7,7, maks %18,2 (206,5 sn). Koyu kareler (ort. parlaklık <40) toplam ≈%2 zaman (≈13 sn). En kötü anlar: **100,0–100,5 sn** (yıldızlı lacivert açılış/başlık öncesi), **206,5–209,5 sn** (çukur, dip geçişi), **350,0 sn** (bölüm kartı karartması), **584,5 ve 600,0–600,5 sn** (bitiş ekranı). 209,0 sn karesi 5× kazançla çizildiğinde glow/vinyet degradesinde halkalı bandlaşma görünüyor; normal parlaklıkta zor seçiliyor. Çözülmüş kare, kaynak kareye göre HF enerjisinin %93,6–99,4'ünü koruyor (bulanık/plastik görünüm yok).
- Kodlama aslına sadakat (601 çözümü, gerçek kodlama hatası): PSNR 33,3–42,5 dB (medyan ≈38,8), SSIM 0,900–0,986. En düşükler yoğun hareket anları: n=960 (40,0 sn belge yakınlaşması, SSIM 0,900) ve n=9120 (380,0 sn slide geçişi, SSIM 0,901). Kalanı ≥0,964.
- VBV: maxrate 9M/bufsize 18M ile saniye başına tampon benzetimi (segment başları yenilenmiyor, o yüzden yaklaşık): tampon %25 altına ≈%3,5 zaman düşüyor, 45 kare alt-akış; 12M/24M'de hiç düşmüyor. En derin dipler: 204, 253, 310, 315, 354, 358, 368, 402, 574 sn çevresi. Yani CRF 19 en zor anlarda VBV tarafından kıstırılıyor; yukarıdaki iki düşük SSIM karesi bu davranışla uyumlu (nedenselliği kanıtlamadım).
- Anahtar-kare nabzı: 48 karelik GOP'ta sakin çekimde IDR karesinin önceki kareye farkı baz kare farkının ≈3,4 katı (≈1,2 düzey ort. mutlak fark vs 0,35). HF enerjisi I/P/B'de eşit (oran 1,01), yani blok/bulanıklık nabzı değil gren/doku yeniden örneklemesi. İzlenebilirliği düşük; küçük.

**Ses (ffmpeg ebur128/astats + örnek düzeyi, çözülmüş AAC üzerinde)**
- Entegre **−14,1 LUFS** (hedef −14,0; kendi raporu −14,00/−14,04), eşik −24,7, LRA 3,4 LU, **gerçek tepe −1,4 dBTP** (hedef ≤−1,0; AAC kodlama sonrası), örnek tepe L −1,50 / R −1,42 dBFS, kırpılan örnek 0, DC −3,9e-4 (−68 dBFS; sorun değil).
- L/R korelasyonu 0,990, S/M −23,1 dB: mono uyumlu, faz sorunu yok. L ve R RMS eşit (−16,97 dB).
- İlk örnek +4,1e-4 (−68 dBFS); ilk 1 ms zirvesi 0,0027, ilk 50 ms zirvesi 0,0071; 10 ms RMS: −52 … −70 dBFS, ardından ≈0,13–0,15 sn'de −51→−12 dBFS (≈20 ms'de yükselen anlatım girişi; örnek düzeyinde adım/DC sıçraması yok). Son 10 ms zirvesi 6e-6, son saniyede 100 ms RMS −48→−83 dBFS düzgün sönüm. Tam sessizlik 594,9–596,4 sn (≤−90 dBFS), kuyruk 601,6–601,8 sn <−70 dBFS.
- Ses 601,88 sn; çözülen örnek sayısı 28.891.136 (601,899 sn); video kuyruğu 601,792 sn (madde 5).
- **Ses-görüntü senkronu:** konteyner düzeyinde kesin (iki akış 0'da başlıyor, iki akış CFR/sabit örnek, kayma birikimi yok, edit list'ler tutarlı). Olay düzeyinde bağımsız bağıntı denedim (SFX stem'i ↔ kare farkı çapraz bağıntı; damga/mühür/çekiç işaretlerinin ardındaki yerel görsel tepe) ama sonuç kare-doğruluğunda ayrıştıramadı (SFX işaretleri geçişlerde öncü; damga hareketleri çok kareli). **Olay düzeyi senkronunu doğrulayamadım**; garantisi motorun tek `timeline.json` kaynağı olmasıdır. Kulak kontrolünde bakılacak noktalar: 104,00 sn `title_hit`, 41,97 sn FRANSIZCA damgası, 129,35–131,75 sn darphane çekici (4 vuruş).

**Yükleme/yayın dosyaları**
- Kapaklar 1280×720 JPEG (baseline, JFIF, ICC yok → sRGB), 177–238 KB (<2 MB). SRT son cue'su 9:54,977 < video 10:01,88. Bölümler dosyası 0:00 ile başlıyor, ≥3 bölüm, ≥10 sn. Uygun.

## 3. Sıralı düzeltme listesi

1. **[ENGELLEYİCİ] Renk matrisi 601↔709 uyuşmazlığı; tüm film, özellikle kırmızılar/altın.** `render.py` `ff_cmd` (satır ≈50–53): `-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709` yalnızca etiket yazıyor, dönüştürme matrisini belirlemiyor (swscale varsayılanı 601). NE YAPILMALI: `ff_cmd`'ye `-vf scale=in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p` ekle (önizleme `--scale` dalında `scale=…` ile birleştir) ve `-color_range tv` etiketle. Önce **P2–P7 render'ından önce** düzelt (şu an hiçbiri render edilmedi, maliyet sıfır). P1 için son kodlamayı yeniden üret: kaynak kareler saklanmadığı için sahneyi yeniden render eder (`out_p1/seg/*.done` sil, `python3 render.py --part 1 --all --workers 4`, ≈17 dk; kareler bit-birebir aynı çıkar, yalnız renk dönüşümü düzelir). Sonra `--concat` ve `--mux`. Doğrulama: sentetik yama testi (5 sn) ve gerçek karelerde PSNR(709 çözüm) ≥ PSNR(601 çözüm). Gerekçe ayrıca: `cmd_tam` (Tam Film) `-c copy` ile birleştirir; 7 parça aynı SPS/VUI/ayarla üretilmeli. Yedek yol (önermem): `-bsf:v h264_metadata=matrix_coefficients=6` ile 601 etiketlemek anlık ve kayıpsız ama oynatıcı/TV/YouTube'un karışık etiketi (709 primer + 601 matris) nasıl işlediğini burada sınayamadım.

2. **[ÖNEMLİ] x264 ayarı ve VBV (aynı yeniden kodlamada çözülür).** `crf 19 / medium / aq-mode 1 / psy-rd 1.0:0.0 / VBV 9M/18M` zor anları kıstırıyor (40,0 ve 380,0 sn SSIM 0,90) ve koyu degradeleri düzleştiriyor. NE YAPILMALI: Sisifos ayarını al: `-preset slow -crf 18 -x264-params aq-mode=3:aq-strength=0.9:psy-rd=1.0,0.15 -bf 3 -profile:v high`, `-maxrate 16M -bufsize 32M` (YouTube yüklemede VBV istemez; istersen tamamen kaldır). Beklenen: +%5–15 dosya (≈650–700 MB), kodlama süresi birkaç dk artar. **Ayarları P1 ve P2–P7 için aynı dondur** (Tam Film kopya birleştirmesi). `-g 48` kalsın (24 fps'te 2 sn; Sisifos'un 60'ı 30 fps içindir).

3. **[ÖNEMLİ→KÜÇÜK] Koyu degradelerde bandlaşma riski; YouTube yeniden kodlamasında kötüleşir.** Anlar: 100,0–100,5 sn (başlık öncesi lacivert), 206,5–209,5 sn (çukur; 1348 sahnesi, glow/vinyet halkaları), 350,0 sn (bölüm kartı), 584,5 sn ve 600,0–601,6 sn (bitiş ekranı; kapanışta koyu). NE YAPILMALI: (a) `aq-mode=3` (madde 2); (b) `cilt_medici.post()` içinde gren genliğini düşük parlaklıkta artır (ör. L<45'te σ 1,35→≈2,2) ve vinyet/glow katmanı `sk.vig_image`/`bg_image`'i 8 bite yuvarlamadan önce ±0,5 düzey üçgen dither ile üret; (c) isteğe bağlı: renk dönüşümünde `-sws_dither ed` ya da yuvarlama gürültüsü. Maliyet ≈0,5 gün, render süresine etkisi ihmal edilir. Kapanış ve bölüm kartları en kolay doğrulama anıdır (5× kazançla bakılınca halka kalmamalı).

4. **[KÜÇÜK→ÖNEMLİ P2–P7 için] Çekim içi hızlı kamera/nesne hareketi bulanıksız.** Ölçüm: ≈59 sn >3 px/kare, ≈27 sn >5 px/kare, ≈12 sn >8 px/kare. En belirgin anlar: **49,50–49,92 sn** (n=1188–1198; ≈25–30 px/kare ≈700 px/sn, metin satırları keskin), **39,58–42,12 sn** (belge yakınlaşması; 6 karede ≈%16 ölçek, n=950→956, kenarlar keskin), 54,4–55,8 sn, 111,4–114,7 sn, 189,96–191,5 sn, 196,6–205,5 sn, 246,5–251,9 sn, 280,5–282,0 sn, 299,67–299,92 sn (15,8 px/kare), 331,5–335,9 sn, 350,8–353,9 sn, 570,96–572,8 sn. NE YAPILMALI: `Program.frame()` içine uyarlamalı deklanşör (bölüm "Motor sorusu", madde 2 ve 3 ve maliyet). Yoğun örnekleme listesi QA kümesi olarak kullanılabilir. Sakin çekimlerde (medyan 0,24 px/kare) hiçbir şey yapma.

5. **[KÜÇÜK] Kuyrukta 3 kare kırpıldı; video 601,792 sn, ses 601,88 sn.** `render.py cmd_mux` `-shortest` kullanıyor: sessiz video 14.446 kare (601,917 sn), final 14.443 kare. Son 0,125 sn bitiş ekranı karartması; görsel etki yok, ama kayıp ve 88 ms bitiş farkı. NE YAPILMALI: `-shortest` kaldır; ses/video süresini mux öncesi eşitle (sesi `apad`+`-t` ya da videoyu `-t` ile ses süresine). `cmd_qa`'ya `nb_frames == ceil(total*24)` ve |video−ses| ≤1 kare kontrolü ekle (şu an yakalanmıyor).

6. **[KÜÇÜK] Dil ve SAR etiketleri.** `ffmpeg … -metadata:s:a:0 language=tur` (Sisifos'ta var) ve `-vf …,setsar=1` (ya da `-aspect 16:9`) ekle. `pasp` yok; YouTube kare piksel varsayar, sorun yaratmaz ama açık olması iyi.

7. **[KÜÇÜK] Anahtar-kare tazeleme nabzı (≈2 sn'de bir, sakin çekimde).** Madde 2'deki `psy-rd=1.0,0.15`, `aq-mode=3` ve `-bf 3` zaten yumuşatır; ayrıca `scenecut`'ı düşürmeden (40) `keyint=48` kalsın. Ayrı bir iş gerekmez; yeniden kodlamadan sonra bir sakin çekimde (ör. 431–436 sn) IDR/komşu kare farkı oranına bak (≤2,5 hedef).

8. **[KÜÇÜK] Birleşim noktası yok sorunu; yapılacak bir şey yok.** Raporlanan birleşimler temiz. Yalnız: `render.py --concat` çıktısına `ffprobe` doğrulama adımı (kare sayısı = toplam; SPS tekliği) eklenirse yeniden render'larda aynı güvence otomatik olur.

## 4. En emin olmadığım nokta

(a) Kıstırılan VBV ile iki düşük SSIM karesi arasındaki nedensellik: bit hızı kısıtı olduğunu simülasyonla gösterdim ama VBV'siz kodlayıp kıyaslamadım (disk %98 dolu, ağır render/kodlama çalıştırmadım). (b) Ses-görüntü olay düzeyi senkronu: konteyner düzeyinde kesin, olay düzeyinde kare-doğruluğunda kanıtım yok. (c) 601→709 düzeltmesinin YouTube yeniden kodlaması sonrası yarar derecesi: tek yönlü kesin (doğru piksel daha iyi), ama izleyicinin göreceği fark küçük olabilir (ortalama ΔRGB ≈2 düzey, doymuş kırmızıda ≈6–11 düzey). Yine de kanalın "tek hata" çizgisinde sıfır maliyetli olduğu için engelleyici saydım. (d) Koyu sahnelerdeki bandlaşmanın telefonda (OLED, düşük parlaklık) ne kadar görüneceği: yalnız 5× kazançla ölçtüm.

## 5. Motor sorusu: Python+Skia CPU hattı ↔ Chromium+Canvas2D hattı (teknik görüş)

**Karar: Yeniden yazmaya/Chromium'a geçmeye değmez; mevcut motor iyileştirilmeli.** Gerekçe, ölçümlerle:

- **Kalite:** İkisi de Skia ile rasterize eder (skia-python 144; Chromium Canvas2D de Skia). Çizgi/degrade/AA kalitesi aynı sınıf; Medici ek olarak deterministik numpy/cv2 son işlemi (bloom, derece, doku, gren) yapıyor. Kodlayıcıya giriş Medici'de kayıpsız ham RGB; Sisifos'ta `toDataURL('image/jpeg', .96)` ara JPEG nesli var (kayıplı, 4:2:0). Sisifos'un tek gerçek kalite avantajı **hareket bulanıklığı** (4 alt örnek, 180°) ve doğru renk matrisi/x264 ayarı; ikisi de Medici'de eklenebilir. Ölçülen kodlama sadakati kabul edilebilir (PSNR medyan ≈38,8 dB, SSIM ≥0,96, düşükler yoğun harekette).
- **Hız:** 14.446 kare = 3.803 işçi-sn (263 ms/kare/işçi, x264 dahil), 4 işçiyle duvar saati ≈16–17 dk (10 dk film). Chromium hattının süresi burada ölçülmedi; her kare 4 alt render + JPEG + base64 + sayfa IPC'si taşıdığı için daha hızlı olduğunu varsaymam. Python hattının bir kısıtı CPU çekirdeği; GPU yok.
- **Sağlamlık:** Medici'nin belirgin üstünlüğü: **bit-birebir deterministik** (3 kare, 2 süreç, farklı sıra: aynı MD5), 1200 karelik (50 sn) segmentler `.done` işaretiyle **parça parça devam edilebilir**, kare hatası önceki kareyi tekrarlayıp `errors.log`'a yazıyor (bu render'da hata yok), yazı tipleri depo içinde (`fonts/`), tarayıcı/GPU/sistem yazı tipi/Playwright sürümü bağımlılığı yok. Chromium hattı üretimde kanıtlı ama bu bağımsızlıklara sahip değil. Segment birleşimleri temiz (yukarıda kanıt).
- **Bakım:** Medici motoru ≈95 bin satır Python (çekirdek ≈30 bin satır `cilt_*`, `compose`, `sk`, `shots`, `qa_flow`, `render`); Sisifos ≈4,8 bin satır JS. ≈35 çekim türü, dünyalar (oda/şehir/deniz), figür kiti ve 12 geçiş Chromium'a taşınırsa hafta mertebesinde iş olur ve getiri yalnızca bulanıklık (Python'da ≈1 günde eklenebilir). Risk, kare kalitesi değil motorun karmaşıklığıdır; `qa_flow` kapıları ve deterministiklik bunu dengeliyor.
- **Kanal standardı / kare hızı:** YouTube 24 fps'i standart ilerlemeli hız olarak kabul eder; kanalda videolar arası aynı kare hızı **zorunlu veya algoritmik olarak gerekli değil**. 24 fps'in tek gerçek bedeli 60 Hz ekranlarda 3:2 kadans (hızlı kesin kenarlı hareketlerde titreme; 120 Hz ekran ve 24p TV bunu temiz gösterir). Filmin çekim içi hareketi büyük ölçüde <1 px/kare olduğundan fark yalnız yukarıdaki ≈12–27 sn'lik kısımlarda görünür. Tam Film için 7 parça aynı kare hızında olmalı (`-c copy` birleştirme); bu zaten 24.

**Fps/bulanıklık için ne yapılmalı ve maliyeti (öneri sırası):**
1. **24 fps'te kal; çekim içi uyarlamalı deklanşör bulanıklığı ekle.** `Program.frame(n)` içinde, hızı >≈3 px/kare olan kare/çekimlerde (kamera + figür hızı çekim tanımından ya da ucuz bir ön ölçümden) `_render_shot`'u g±0,25/FPS'te 3 kez çağır, **post()'tan önce** float32'de ortala; çekim sınırına taşırma (Sisifos `lo/hi` kıstırmasını al). Gereken kod ≈40–60 satır + `qa_flow`'a hız raporu. Geliştirme ≈1 gün. Render maliyeti: yalnız ≈%8–12 karede +2 render → P1'de ≈+10–15 % (≈+2–3 dk/parça). Hızlı çekimlerde (30–40 px/kare) 3 örnek aralıklı kopya yapar; o durumda kamera hızı bilindiği için yönlü çizgisel bulanıklık (`slide`'daki gibi, ≈5 ms) daha temiz. Bu yol "akan" hissini en ucuza artırır.
2. **30 fps (isteğe bağlı).** `FPS` 7 modülde ayrı tanımlı (`engine.py, sk.py, render.py, qa_flow.py, qa_program.py, qa_text.py, preview_reel.py`) + çekirdek dışı iki sabit 24 (`kapak_medici.py:42`, `preview.py:16`); GOP/segment ve gren döngüsü (n%6) yeniden ayarlanır. Geliştirme ≈0,5–1 gün (denetim + kısa QA). Render maliyeti +%25 (P1 ≈17→21 dk), dosya +%10–15. Yarar: 60 Hz'de 2:2 kadans, Sisifos/Shorts ile tek standart. Bulanıklığı çözmez, yalnız kadansı. Şu an yalnız P1 render edildiği için yeniden render yükü düşük; ancak 30 fps seçilirse madde 1 ile birlikte yapılmalı.
3. **Chromium'a geçiş: önermem.**

**En yüksek getirili 3 iyileştirme (maliyet):**
1. Renk dönüşümü + x264/VBV/etiket düzeltmesi, ardından P1 yeniden kodlama (kod 1–2 saat; P1 render ≈17–20 dk; P2–P7'de sıfır ek maliyet) ve `render.py --qa`'ya kare sayısı + ses/video süresi + 5 sn'lik sentetik matris testi eklenmesi (≈1–2 saat). Getiri: kesin renk düzeltmesi, kuyruk kaybının kapanması, Tam Film'in tutarlılığı.
2. Uyarlamalı deklanşör bulanıklığı (≈1 gün; +%10–15 render).
3. Karanlıkta dither/gren ve `aq-mode=3` (≈0,5 gün; render maliyeti ihmal edilir) + `qa` içine "düz-degrade payı" kapısı (benim ölçüm kodum ≈30 satır; eşik: kare başına <%5, kapanış/dip kareleri hariç <%8).

## 6. Kendi ölçümlerimin yeniden üretimi (kısa)
- Kare hash ve birleşim: `ffmpeg -i X -map 0:v:0 -f framemd5 -an out.txt` (final + 13 segment; fark = yalnız son 3 kare).
- Matris testi: `render.py ff_cmd` komutuna 8 düz renkli yama beslenir; YUV okunur; 601/709 beklenenle karşılaştırılır.
- Kaynak-karşılaştırma: `MEDICI_PART=1 python3 -c "import compose; compose.Program(part=1).frame(n)"` ve final'den `ffmpeg -ss … scale=in_color_matrix=bt709|bt601`.
- Ses: `ffmpeg -i medici_P1.mp4 -map 0:a:0 -af ebur128=peak=true -f null -` (−14,1 LUFS / −1,4 dBTP / LRA 3,4).
- Kare ritmi/hareket: `ffprobe -show_entries packet=pts,dts,duration` + Farneback (480×270) akışı.
