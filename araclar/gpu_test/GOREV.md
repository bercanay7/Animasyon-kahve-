# GÖREV: GPU'lu Blender üslup testi (Theo'nun odası)

Bu dosya, kullanıcının bilgisayarında (Windows, ekran kartlı) çalışan Claude Code oturumu için yazıldı. Görevi baştan sona sen yaparsın. Kullanıcıya yalnız gerçekten onun yapması gereken bir şey çıkarsa sorarsın (ör. bir sitede oturum açmak).

## Neden
- Kullanıcının kararı (27 Kasım, `CLAUDE.md` §İş akışı 7): kalite önce gelir. Hazır yüksek kaliteli varlıklar, yüzlü ve iyi modellenmiş insanlar, fiziksel ışık ve GPU'lu Blender serbest.
- Bulut oturumunda GPU yok: yazılımla WebGL, iskeletten örülmüş "manken" figürler. Twitter'daki three.js ve Blender işleriyle aradaki fark bu.
- Bu test, aynı sahnenin yeni hatla ne kadar iyi olduğunu gösterecek. Başarılı olursa "Van Gogh'a Kim İnandı?" videosunun figürlü planları bu hatla yeniden çizilebilir.

## 0. Hazırlık
1. Depoyu güncelle ve test dalına geç. Çalışma klasörün deponun kopyası değilse önce klonla: `https://github.com/bercanay7/Animasyon-kahve-`.
   ```
   git fetch origin claude/3d-puppet-drawing-shader-4ca4y8
   git checkout claude/3d-puppet-drawing-shader-4ca4y8
   git pull
   ```
2. Ekran kartını doğrula: `nvidia-smi`. NVIDIA değilse Cycles'ta HIP (AMD) ya da oneAPI (Intel) kullanılır. Hangi kartın olduğunu `SONUC.md`'ye yaz.
3. Blender 4.2 ya da üstü kurulu mu bak: `blender --version`.
   - Yoksa `winget install BlenderFoundation.Blender`. Bu kurulum kullanıcının bilgisayarına yazılım ekler; önce kullanıcıya tek cümleyle sor.
   - Komut yolda değilse Blender genelde `C:\Program Files\Blender Foundation\Blender 4.x\blender.exe` altındadır.
4. `CLAUDE.md`'yi oku. Özellikle şu bölümler: "Hassasiyet ve hukuk", "Dış varlıklar", git kuralları (Türkçe commit, sonunda atıf satırları).

## 1. Sahne: Theo van Gogh'un Paris odası, gece, 1888
Referans kare bulut hattından: `van-gogh/` filminin A01 planı. Karşılaştırma için kullanıcı bu kareyi `araclar/gpu_test/referans/` altında da bulur; yoksa bu adımı atla.
- **Mekân:** küçük bir oda.
  - Ahşap döşeme, sıvalı ve hafif lekeli duvar.
  - Solda uzun bir pencere: dışarıda gece Paris çatıları, ay ışığı.
  - Sağda bir yazı masası; üstünde gaz lambası, birkaç kâğıt ve sarı zarflar.
  - Masanın yanında şövale ve tuval.
- **Tuval:** Vincent'in *Hasır Şapkalı Otoportre*'si (1887; Met, CC0): `van-gogh/gorsel/otoportre_hasir_sapka_1887_met436532.jpg`. Görüntü renk dokusu olarak tuvale basılır.
- **Figür:** Theo (31 yaşında, ince, koyu takım elbise, 1880'ler).
  - Masada oturup bir mektup okur ya da şövaleye bakarak ayakta durur. Hangisi daha iyi çıkarsa.
  - Yüz görünebilir (yeni kural), ama yaşayan birine ya da bir oyuncuya benzememeli.
- **Işık:**
  - Gaz lambası sıcak ana ışık: küçük yarıçaplı nokta ışık + alev için emisyon.
  - Pencereden soğuk, zayıf ay ışığı.
  - İsteğe bağlı: lamba çevresinde hafif hacimsel toz.
- **Kamera:** 35–50 mm. Odaya göz hizasından bakan geniş plan (A01 gibi): figür sırttan ya da ¾, lamba ve tuval kadrajda.

## 2. Varlıklar (yalnız ticari kullanıma izin veren lisans)
Her varlık için `araclar/ASSETS.md`'ye satır ekle: ad · kaynak URL · lisans · atıf şartı · tarih · dosya yolu. NC (ticari olmayan) lisans yasak. Lisansı doğrulanamayan varlık kullanılmaz.
- **Poly Haven (CC0, atıf gerekmez):** https://polyhaven.com, API: `https://api.polyhaven.com/assets?t=models` (ayrıca `t=hdris` ve `t=textures`).
  - Dosya adresleri: `https://api.polyhaven.com/files/<id>`.
  - Masa ya da büro, sandalye, eski kitaplar, lamba ya da fener, gerekirse şövaleye uygun ahşap.
  - Döşeme ve sıva dokuları (2k yeterli).
  - Gece ya da iç mekân HDRI (çok kısık, yalnız dolgu için).
- **İnsan** (sırayla dene):
  1. **Microsoft Rocketbox** (MIT; lisans metnini dosyayla tut): https://github.com/microsoft/Microsoft-Rocketbox
     - Riglenmiş gerçekçi insanlar. Koyu takımlı bir yetişkin erkek seç (ör. `Assets/Avatars/Adults/Business_Male_*`).
     - Klasörün tamamı çok büyük. Yalnız gereken avatarı indir: GitHub'da tek klasör ya da `git sparse-checkout`.
  2. Olmazsa **MPFB2** (MakeHuman'ın Blender eklentisi; ürettiği insan ve sistem varlıkları CC0): https://extensions.blender.org/ (MPFB).
  3. Kullanıcı isterse **Mixamo** (Adobe hesabı gerekir; karakter ve animasyonlar ticari kullanıma serbest). Oturum açmayı kullanıcı yapar.
- **Giysi:** Rocketbox takımı modern. Kadrajda ve lamba ışığında 1880'ler gibi okunması yeterli: koyu ceket, beyaz yaka. Okunmazsa yakayı ve ceket boyunu düzelt.

## 3. Render (Cycles, GPU)
Blender betiğini `araclar/gpu_test/oda_testi.py` olarak yaz. Komut satırından çalışsın:
```
blender -b -P araclar/gpu_test/oda_testi.py -- --cikti van-gogh/gpu_test
```
Cycles GPU açma kodu (Blender 4.x):
```python
import bpy
prefs = bpy.context.preferences.addons['cycles'].preferences
for tur in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
    try:
        prefs.compute_device_type = tur; prefs.get_devices()
        if any(d.type == tur for d in prefs.devices): break
    except Exception: pass
for d in prefs.devices: d.use = (d.type != 'CPU')
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'GPU'
sc.cycles.samples = 256; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = 'AgX'
```

**Çıktılar (`van-gogh/gpu_test/` içine):**
1. **`oda_renkli.png`:** tam renkli tek kare, 1920×1080.
2. **`oda_karma.png`:** filmin kuralıyla aynı kare. Dünya gri (grisaille, hafif sıcak siyah-beyaz), yalnız tuvaldeki tablo ve masadaki sarı zarflar renkli.
   - Yöntem: tuval ve zarflar için `Object Index` ya da Cryptomatte ile maske.
   - Compositor'da maske dışını desatüre et. Sıcak tonlama: siyah `#0b0a0a`, beyaz `#f7f0e1`.
3. **`oda_hareket.mp4`:** 6 saniye, 30 fps. Kamera yavaşça lambaya ve tuvale yaklaşır; figür nefes alır ve mektubun sayfasını çevirir (ya da başını hafifçe çevirir).
   - Gürültü kontrolü için kareler arası tohum sabit kalsın.
   - Kodlama: `ffmpeg -framerate 30 -i kare_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 oda_hareket.mp4`
4. **`SONUC.md`:**
   - ekran kartı;
   - Blender sürümü;
   - kare başına render süresi (tek kare ve hareketli kare ortalaması);
   - kullanılan varlıklar ve lisansları;
   - neyin iyi olduğu ve neyin hâlâ zayıf olduğu (yüz, el, giysi, ışık): dürüst bir değerlendirme.

**Kalite ölçütü** (kendi gözünle bak, kareyi aç):
- Figür manken gibi değil insan gibi okunuyor.
- Malzemeler gerçek: ahşap damar, sıva, kâğıt.
- Lamba ışığı fiziksel: yumuşak gölge, sıcak düşüş.

## 4. Hassasiyet (kalite kısıtı değil, kanalın korunması)
Tam boy karede bak. Şunlar olmamalı:
- haç gibi okunan çerçeve ya da şövale çıtası (kesişen iki çubuk);
- kan gibi kırmızı leke;
- asılı ya da havada duran beden;
- yaşayan birine benzeyen yüz.

`CLAUDE.md`'deki "Görüntüde yakalananlar" listesinin tamamı geçerli.

## 5. Teslim
- `van-gogh/gpu_test/` içindeki PNG'ler, MP4 ve `SONUC.md` ile `araclar/gpu_test/oda_testi.py` dosyasını commit et ve aynı dala push et.
  - İndirilen ham varlıkları (büyük FBX, HDRI, dokular) depoya koyma. `araclar/gpu_test/varlik/` altında tut ve `.gitignore`'a ekle.
  - MP4 50 MB'ı geçmesin.
  - Commit mesajı Türkçe, CLAUDE.md'deki biçimde.
- Kullanıcıya iki görseli ve videoyu göster. Bulut oturumundaki başkan (Van Gogh projesini yürüten oturum) sonuçları depodan çekip mevcut filmle yan yana karşılaştıracak.
