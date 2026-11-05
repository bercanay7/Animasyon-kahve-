# BRİF — ENG-E · v3.1 "motor, c0 ve c1" paketi (kurul tur 3 bulguları)

Sen Medici Parça 1'in v3.1 düzeltme ajanısın. P = `/home/user/Animasyon-kahve-/gunluk-shorts/medici-uzun-dosya`.

Kurul tur 3'te 10 üyeden 8'i ONAY verdi. Kalan bulgular engelleyici değil, ama puanı yükseltecekler.
- Video v3: `P/out_p1/medici_P1.mp4`.
- Tur 3 raporları: `P/kurul/tur3/<KOD>.md`. Önce oku: AN1.md (Y7, Y-N3), PK2.md (§2 Y8, Y9), SA1.md (§4 N3).
- Tur 2 motor ajanının raporu: `P/kurul/duzeltme_tur2/ENG-D.md`.

## Dosya sahipliği
- **Senin:** `anim.py`, `cilt_cam.py`, `compose.py`, `c0_kinds.py`, `scenes_c0.py`, `scenes_c1.py`, `cilt_oda.py`, `kapak_medici.py` (kapak dosyalarını YENİDEN ÜRETME).
- **Paralel çalışan SCN-3'ün:** `c2_kinds.py`, `scenes_c2.py`. Bunlara dokunma.
- `p1_ortak.py` ortak: yalnız ekleme yap, raporda belirt.
- Anlatım, ses, `timeline.json` ve altyazı DEĞİŞMEZ.
- Motor değişikliği P2–P7'yi de etkiler: geriye uyumlu kal, varsayılanları sessizce değiştirme.

## İşler

### 1. Küçük hızlı nesnelerde deklanşör (AN1 Y7, motor tarafı)
- 180° bulanıklık kamerada ve büyük alanda çalışıyor, küçük hızlı nesnede çalışmıyor.
- `anim.hint_speed` yalnız `anim.py:472` (sabit 9,0) ve `c2_kinds.py` (4,0) içinde çağrılıyor. Eşik `compose.SHUTTER_V_HINT` = 8.
- Ne yapılacak:
  - Damga düşüşü (`anim.stamp_ovl` "drop" ve "bounce"), uçan nesne yayları (`p1_ortak.prop_arc` vb.) ve senin dosyalarındaki öteki hızlı küçük nesneler gerçek hızlarını bildirsin (`anim.speed_of`).
  - c2'deki florin yağmurunu SCN-3 yapıyor.
  - Alt-kare örneklemesinin bu nesnelerde gerçekten devreye girdiğini ölç: önce ve sonra bir kare + `shutter_stats`.

### 2. Kesme girişinde 1 karelik duruş (AN1 Y-N3)
- 43,9 sn: #8 `c0_belge` "hand" kamerası; kesme sonrası ilk adım 0,07.
- `c0_belge` kendi kamerasını `_cam_keys`/`_cr` ile kuruyor (`c0_kinds.py`). Sert kesmeyle birleşen uçta `cilt_cam.CUT_SLOPE` uygulanmalı (`cilt_cam` ≈400–421 mantığı).
- Aynı sorunu `OWN_CAMERA` kullanan senin dosyalarındaki öteki türlerde de tara.

### 3. Açılış yankısı (PK2 Y8)
- 0–3,3 sn.
- (a) Yankı hâlâ eski K1 görünümünde: 0,6 sn karesinin kenar grisi 17, yeni kapağınki 38; zemin daha koyu. Yeni K1 kapağıyla aynı zemin olsun: `kapak_medici.KAPAK_ZEMIN["K1"]` = ton (52,32,26), vinyet 0,30, ışın yok.
- (b) Kilidin sol üst köşesinde 0,3–3,0 sn arası küçük beyaz parıltı (≈x 760–830, y 690–760). Kalksın ya da yumuşak sıcak bir yansımaya dönsün.
- İlgili kod: `scenes_c0.py` `_ECHO` (`isinlar=False`), `k_kapak_kilit` varsayılanları (`vinyet=0.75`, `isinlar=True`).
- Kapak PNG'leri değişmez.

### 4. Kırmızı geçiş (PK2 Y9)
- 271,1–271,4 sn, #47 `p1_procession` → #48 `c1_lonca` taşıma (carry) geçişi: kırmızı bant ve mühür benzeri daireler.
- "isyanı ezdi" cümlesinin hemen ardından geldiği için "kan" çağrışımına açık.
- Rengi nötrleştir: kâğıt ya da mürekkep tonu. Yalnız bu geçiş; motor varsayılanı değişmesin.

### 5. 1737 belgesi: zikzak yer tutucu satırlar (SA1 N3)
- Nerede: #7, #8 ve #10 `c0_belge`, 34,6–56,7 sn. ≈17 sn tam ekran; kamera 2,5×'e dek yaklaşıyor.
- Sorun: gövde satırları zikzak çizgi. c2'de sayfalar gerçek harflerle yazıldığı için bu "çizilmemiş" gibi okunuyor.
- **Kısıt:** belgenin Fransızca özgün metni kaynaklarımızda yok; kaynak üyeleri uydurma metne izin vermez. Bu yüzden gerçek Fransızca cümle YAZMA.
- Yapılacak: zikzağı **asemik el yazısına** çevir. 18. yüzyıl Fransız yazı eli gibi akan, ama sözcük oluşturmayan döngülü çizgiler:
  - değişken x-yüksekliği; üst ve alt uzantılar;
  - sözcük araları; satır başında büyük harf benzeri bir kıvrım;
  - hafif sağa eğim; mürekkebin vuruş başında koyulaşması;
  - düzensiz satır sonları.
- Düşük kontrastlı ve deterministik olsun (tohumlu). 2,5× yakın planda da "okunamayan eski el yazısı" gibi görünsün, zikzak gibi değil.
- Değişmeyecekler: Romen rakamları, III. satır vurgusu (altın leke + sinabar çizgi; satır hizası aynı), mühürler, ITALIANO/FRANSIZCA vuruşları.
- Satırlar `cilt_oda.doc_sheet` içinde çiziliyor. Aynı işlevi başka yerler (1743 odasındaki belge, kapak) kullanıyorsa onlar da değişir. Sorun değil, ama kapak PNG'lerini yeniden üretme.

## Kurallar ve kapılar
- **Kare kontrolü:** `python3 /tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/v3/kare.py <ad> t1 t2 … --w 640 --cols 4`
  - Program karesi üretir; kontak sayfası `…/scratchpad/v3/<ad>.png`.
  - Hareket ölçümü için ardışık kareler al.
- **Son kapı:** `cd P && python3 qa_flow.py --part 1 > /tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/enge_qa.txt 2>&1`
  - 19 kapının hepsi GEÇTİ olmalı.
  - ≈6 dk, 2 süreç; en çok iki kez koş.
  - SCN-3 de koşabilir: aynı anda ikiniz koşarsa bellek yeter (15 GB), ama kendi ağır işinle aynı anda koşma.
- **Yasaklar:** render.py yok, git commit/push yok (başkan yapar), `pkill -f` yok.
- **Disk sınırlı (≈2,9 GB boş):** kare dökümlerini sil. Kanıt JPEG kontak sayfaları (her biri ≤1 MB) `P/out_p1/duzeltme/tur3/ENG-E/` altına.

## Teslim
- Rapor `P/kurul/duzeltme_tur3/ENG-E.md`. Her madde için:
  - ne yaptığın;
  - dosya:satır;
  - önce ve sonra kanıtı;
  - P2–P7'ye etkisi.
- Son mesajında kısa özet ve qa_flow'un son satırları olsun.
