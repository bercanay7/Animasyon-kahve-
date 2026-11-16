# Geriye bakış: Kurosawa, Ran (kanalın ilk film videosu)

## Ne çıktı
- **Film:** 8:02; 66 cümle, 63 plan; mürekkep resmi (Japon suiboku) üslubu, LemoLab ink-wash motoru (MIT) + bizim çizim ilkellerimiz (`lib/ran_cizim.js`: kale, ateş, xieyi figür, flüt); 5 gerçek görsel arası (Met CC0 ×3, Commons PD ×2); Emrullah sesi; özgün müzik (flüt, dron, taiko); 125 altyazı.
- **Kapaklar:** A "EKTİĞİNİ BİÇTİ" (filmin ilk karesi: yanan kale, inen yaşlı figür); B "KIRILMAZ SANDI" (kırık üç ok; 10. sn'de karşılanır).
- **Teslim:** `teslim/ran_ana.mp4` (H.264 CRF 18, 289 MB), `ran_youtube.mp4` (H.265 CRF 26, 66 MB, SSIM 0,980), `ran_telefon.mp4` (720p H.265, 17 MB). Render 4 işçiyle 96 dk (hızlı birleştiriciyle) + 5 parça düzeltme 25 dk; miks −14,3 LUFS, tepe −1,0 dBFS.
- **Shorts:** 28,3 sn (`ran_shorts.mp4`); açılış yanan kale + "Bir kale yanıyor"; kapanış "Sana yapılanla ne yaparsın?".
- **Yayın metinleri:** `youtube.md`, `yayin.md` (telif notu dahil).
- **Kredi:** seslendirme 13.008 (test 232 + 8 bölüm × 2 çekim); Scribe dökümü 466.
- **Kurul:** hiçbir kapıda toplanmadı (kullanıcının kararı, kullanım %90); ayrıntı `KURUL.md`.

## Talep kontrolü (senaryodan önce; ikinci uygulama)
| Ölçüt | Sonuç |
|---|---|
| (a) Tanınırlık | "ran" konuya ulaşmıyor (Milton düzeyi); "kurosawa" orta (kapı *Düşler*); **"kral lear" güçlü** (Haluk Bilginer, tirad, sesli kitap) |
| (b) Kişisel soru | "Yaptıkların bir gün sana döner mi?" (başlık) + "Sana yapılanla ne yaparsın?" (kapanış). Arama damarı: "nankör evlat" (Lear'ın kendi sözü), "miras kavgası", "evlat ayrımı" |
| Karar | Tanıdık kapı başlıkta önde: "Kurosawa'nın Kral Lear'ı"; "Ran" künyede ve açıklamada (kullanıcının onayı) |
| Sınama | Yayından sonra 48. saat ve 7. gün: TO Milton/İkaros'tan (%1–1,6) yüksek mi; "kral lear" araması trafik kaynaklarında görünüyor mu? |

## İşe yarayanlar
- **Kullanıcının kendi okuması omurga oldu.** Geçmiş sohbetteki üç notu (Nō oyunculuğu, "asıl yıkım iç savaş", Kaede'nin seçimi) kaynakla sınandı ve üçü de girdi: Kurosawa'nın Lear'a geçmiş vermesi (K1) "iç savaş"ı, Sue ile Kaede'nin karşıtlığı iksiri taşıdı.
- **Kullanıcının hatırladığı sahne kaynakla düzeltildi.** "Sondaki kör flüt sahnesi": kaynaklara göre flüt son sahnede çalınmıyor, kaybolmuş; bu eksiklik kapanışın sessizliği oldu ("Flütü yok. Ablası yok… Hiçbir ses yok"). "Körken çizdi" sözü de "gözleri iyice zayıflamışken" oldu.
- **Film telifine üslupla cevap.** Tek renk mürekkep + tek kırmızı, filmin renk kodlu sancaklarını, kostümlerini ve beyaz makyajını kendiliğinden dışarıda bıraktı; xieyi figür oyuncu benzerliğini engelledi. Kurosawa'nın resimleri için "göstermeyeceğim, hâlâ onun" cümlesi hem telif kuralı hem anlatı oldu.
- **Gerçek görseller yer yer.** Met Open Access API'si (`isPublicDomain`) lisansı tek çağrıda doğruluyor; 1937 fotoğrafında Kurosawa'nın arkasında bir Japon kalesi çıkması şanstı ama aramaya değdi.
- **Hazır motor + ölçerek hızlandırma.** cinecode/LemoLab ink-wash demo motoru tek betiğe paketlendi (`tools/bundle_ink.py`); render ilk denemede ~5 sa görünüyordu. Ölçüm (çizim ~10 ms, birleştirici 4–8 sn) durağan gürültünün her karede yeniden hesaplandığını gösterdi; ön geçişe alınca (`lib/comp_hizli.js`) görünüm aynı, süre ~10 kat kısa.

## İşe yaramayanlar ve dersler
1. **ElevenLabs kotası yarıda bitti.** 8 bölümün 6'sı "kota aşıldı" ile reddedildi (ücret alınmadı); kullanıcı kredi ekleyince aynı metinlerle sürdü. Ders: büyük üretimden önce kalan krediyi sor (bağlantının kullanım aracı izin istiyor; `account_get_usage` bu oturumda çalışmadı).
2. **Scribe'ın tahmin aracı yanıltıcı.** `estimate_only` 11 sn için 3,7, 74 sn için 24,8 kredi dedi; gerçek ücret 60 ve 406 (≈5,5 kredi/sn). Ders: döküm yalnız en riskli bölüme; tam döküm Whisper kurulana dek yapılmaz.
3. **Sözdizimi kazası.** Kapak düzenlemesinde bir `};` aramasıyla dosya kesildi; render işçileri eski kodla çalıştığı için zarar yok. Ders: düzenleme sonrası `new Function(...)` ile sözdizimi denetimi.
4. **Plan–cümle kayması yine görüldü.** P60/P61 bir cümle önde yazılmıştı (H07/H08 yerine H08/H09); "kelime yok" uyarısı yakaladı. Ders: plan listesi yazılırken cümle metni yanına konsun.
5. **file:// görselleri WebGL'i kirletiyor.** Gerçek görsel arası `Tainted canvases` hatası verdi; render ve kare araçları küçük bir yerel http sunucusuyla çalışıyor (`tools/kare_cek.js`, `render.js`).
6. **Wikimedia oran sınırı.** Commons API arka arkaya isteklerde boş döndü; 1953 fotoğrafı indirilemedi. `Special:FilePath` + bekleme işe yaradı.
7. **Kurulsuz üretim.** Bütün kapılar başkan denetimiyle geçti. Bilinen zayıflıklar aşağıda.

8. **Donukluk taraması işe yaradı.** İlk render'da 2 sn'den uzun beş donuk aralık çıktı (künye levhası, üç leke, bitmiş çizgi, kadrajdan çıkan tomar, soru levhası); hareket eklenip yalnız 5 parça yeniden render edildi. Kalan: bitiş ekranı ve 2 sn'lik boş yol.

## Bilinen zayıflıklar
- Figürler xieyi ve yüzsüz; bazı planlarda (P02 sırt, P34 yakın baş) biçim belirsiz kalabiliyor.
- Kapak B, A'dan zayıf (oklar küçük boyda ince); test sonucu ayırt edecek.
- Hassasiyet okuru görmedi: Amida resmi (figürsüz tomar), Sue'nün duruşu, Kaede'nin canavar olarak anılması; Japon kültürü klişe değil ama bağımsız bir göz iyi olurdu.
- Telaffuz yalnız döküm ve bir bölümün Scribe kontrolüyle sınandı; kulakla onay kullanıcıda.
