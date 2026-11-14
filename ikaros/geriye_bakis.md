# Geriye bakış: İkaros

## Ne çıktı
- **Film:** 5:55; 42 cümle, 52 plan; serigrafi seyahat afişi üslubu; Emrullah sesi; özgün müzik; 89 altyazı.
- **Kapaklar:**
  - A: "İKİ UYARI VARDI", güneşe bakan İkaros; filmin ilk karesiyle aynı figür.
  - B: "UNUTULAN UYARI", denize değen kanat ucu.
- **Shorts:** 37,5 sn, kanca "İKİ UYARI VARDI".
- **Yayın metinleri:** `youtube.md`, `yayin.md`.
- **Teslim:** YouTube kopyası (H.265, ~42 MB) ve telefon kopyası (~17 MB).
- **Kredi:** 9.206 (8 bölüm × 2 çekim); tahminle aynı.

## Kurul kapıları
Kullanıcının kullanım sınırı yüzünden her kapıda en çok iki birleşik mercekli üye toplandı.

| Kapı | Sonuç |
|---|---|
| Senaryo | 7,5 / 7,5 → **9,0 / 9,3 ONAY** (2 tur) |
| Üslup | 7,0 / 8,0 → 8,5 / 9,2 → **9,0 / 9,2 ONAY** (3 tur) |
| İlk tam kurgu | 7,6 / 7,5 RED, bir veto (P51). Düzeltildi; gerileme turu aşağıda |
| Kapak ve paket | A 8,0 / 7,5, B 7,0 / 6,0 → **A 9,0 / 9,0, B 9,0 / 8,5 + tek madde, paket 9,5 ONAY** |
| Ses ve miks, Shorts | Kurul toplanmadı (kullanım). Miks ölçümle hedefte (−14,3 LUFS, −1,3 dBTP); kulakla onay kullanıcıda |

## İşe yarayanlar
- **Kullanıcıyla yorumu birlikte kurmak.** Kullanıcının üç görüşü videonun omurgası oldu: "İkaros suçlu değil", "ya en iyisi ya hiç", "tek bir zirve anı için yaşamak". Kaynak kurulu bu yorumu metne dayandırdı: Ovidius suçu Daidalos'a yazar (VIII.240).
- **Ovidius'un kendisini okumak.** Herkesin bildiği hikâyenin içinden üç sürpriz çıktı ve hepsi doğrulanabilir: ikinci uyarı ve önce söylenişi, "kibir" yerine "cüret, sevinç, arzu", keklik.
- **Hazır motor almak.** cinecode tarifi ve LemoLab'ın MIT lisanslı `silk.js`'i yeni motor yazmanın yerini tuttu; üslup kapısı üç turda geçti (Milton'da altı tur).
- **Günün saati paleti.** Şafak, öğle, gün batımı, alacakaranlık, gece, şafak sırası hikâyenin duygusunu taşıdı. Tek bakışta bütün film tutarlı bir afiş dizisi gibi okunuyor.
- **Kelimeye bağlı rakle.** Dört palet değişimi "ama", "arzudan", "atmıştı" ve "önce" sözcüklerinde, plan içinde, görünür bıçakla geçiyor.

## İşe yaramayanlar ve dersler
1. **Kapta Whisper, scipy, soundfile ve pyloudnorm yoktu; `pip install` izin sisteminde reddedildi.** Kurulum gerektirmeyen yollar kuruldu:
   - `tools/hizala.py`: sessizliğe dayalı hizalama;
   - `audio/dsp_shim.py`: numpy ile scipy yerine geçen katman;
   - `tools/mix_ffmpeg.py`: ffmpeg loudnorm ile miks.

   Bedeli: telaffuz hatası otomatik yakalanmadı ve kelime zamanları cümle içinde ±0,4 sn tahmin. Shorts kesimleri bu yüzden vo.wav'daki gerçek duraklamadan yapılıyor. Sonraki oturum için kullanıcı ortamın kurulum betiğine ya da izinlerine `pip install openai-whisper scipy soundfile pyloudnorm` eklemeli.
2. **Donukluk.** İlk kurguda filmin %25,7'si tamamen donuktu: sabit kadrajlı afiş planları. Çare olarak varsayılan %3 yavaş yaklaşma ve kilit planlarda sözcüğe bağlı eylem eklendi. Ders: her plan çizilirken "bu planda ne hareket ediyor?" sorusu baştan sorulmalı.
3. **Palet değişimi plan başında görünmez.** Rakle yalnız çekimin içine düşen değişimde çizilir. Ders: palet değişimi plan listesinde sözcüğe bağlanır (`palat`).
4. **Karikatür okuması.** Koyu siluet, bembeyaz göz, kıvırcık yuvarlak baş ve çıkık ağız bir araya gelince kapak boyunda ırkçı karikatür (minstrel) okumasına kapı aralıyor. Göz küçük ve sıcak tonda olur, profil sade tutulur. Üslup kapısı bunu görmedi; kapak kurulu gördü.
5. **Kapak yazısı boyu.** Bebas'ta büyük harf yaklaşık 0,70 em. %18 için 1080 ölçeğinde font ≥ 290 px gerekir; 250 px %16,4'te kalıyordu.
6. **Alt bant altyazıya aittir.** Künye ve bilgi bandı yazıları y > 880'e konmaz; afiş dili ile altyazı çakıştı.
7. **Kurul kısaltması.** İki birleşik üye kullanım payını korudu ve bulgular isabetliydi. Ama ses/miks ile Shorts kurulsuz kaldı.

## Bilinen zayıflıklar
- Yüzler profil siluet; duygu duruşla ve başın açısıyla veriliyor.
- Kapak B ikinci planda kalıyor: insan figürü yok, vaadi daha soyut.
- Altyazıda 5 blok 17 kar/sn'yi aşıyor (anlatım hızı); birkaç satır bölmesi kusurlu (`srt.py`'ye özel ad + edat kuralı eklenmeli).
- İlk kez gören izleyicinin 0:30 tahmini düzeltmelerden sonra sınanmadı.
