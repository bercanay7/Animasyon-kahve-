# İlk tam kurgu kurulu (tur 1): ortak brif

Film: "Zaman Kuryesi" kanalı için Milton, *Kayıp Cennet* ve Şeytan'ın iç yolculuğu. 25:46, 1920×1080, 30 fps, Canvas 2D ile kodla çizilen Doré gravürü üslubu, Türkçe anlatım (yapay zekâ sesi), 142 plan. Senaryo ve seslendirme önceki kapılardan geçti; **bu kapıda görüntü, kurgu ve ekran yazıları değerlendirilir.** Senaryo metni ve ses bu turda değişmez (bir yazım ya da olgu hatası bulursan yine de yaz).

Sen bağımsız bir kurul üyesisin. Öteki üyelerin raporunu görmeden kendi merceğinle bakarsın. Kibar olmak zorunda değilsin; amaç filmi yayın öncesi 9/10'a taşımak. Emin olmadığın yeri "emin değilim" diye yaz, uydurma. Gördüğün kareye dayan; bakmadığın planı puanlama.

## Malzeme
Proje kökü: `/home/user/Animasyon-kahve-/milton/`
- **Özet sayfaları** (her plandan bir kare, 640 px; etikette plan kimliği, set, cümle çapası, zaman, süre): `kurul/kurgu_tur1/ozet/bas/` (planın %12'si), `orta/` (%50), `son/` (%90); her biri 8 sayfa. Önce bunlara bak.
- **Tam boy kareler** (1920×1080 PNG, planın ortası): `/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/kurgu2/kare/` (dosya adı film zamanı: `t0176.44.png` = 176,44. sn). %12 ve %90 kareleri: `.../scratchpad/kurgu2a/kare/`, `.../scratchpad/kurgu2b/kare/`.
- **İstediğin andan kare almak:** `cd /home/user/Animasyon-kahve-/milton && node shot.js <kendi scratchpad klasörün> 176.44 176.4733 ...` (film zamanı, saniye; ardışık kare için +0,0333). Kendi klasörün: `/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/kurul_<adın>/`. Arka planda tam film render'ı sürüyor; makine yavaş olabilir, kareleri 10–20'lik gruplar hâlinde iste.
- **Render edilmiş parçalar** (24 sn'lik H.264 parçaları, hazır oldukça): `.parts/c000.mp4` (0–24 sn), `c001.mp4` (24–48 sn) … Hareketi ölçmek için `ffmpeg`/`ffprobe` kullanabilirsin. Henüz olmayan parçayı bekleme; `shot.js` ile ardışık kare al.
- **Plan listesi ve zamanlar:** `python3 tools/plan_zaman.py` (hepsi) ya da `python3 tools/plan_zaman.py NIF P109` (set ya da plan). Plan tarifleri: `animatik/planlar.json` (kadraj, hareket, ekran yazısı).
- **Senaryo:** `senaryo.json` (`alt` alanı ekrandaki altyazı metni). **Altyazı:** `milton.tr.srt`. **Zaman çizelgesi:** `timeline.js`.
- **Üslup kuralları ve kırmızı çizgiler:** `lib/acts/KILAVUZ.md`. **Önceki kurul kayıtları ve başkan kararları:** `KURUL.md` (özellikle "Görsel kırmızı çizgiler", "Kapı 2", "Kapı 2b" ve "Sahne üretimi ve yönetmen düzeltme turu").
- Sahne kodu: `lib/acts/*.js`, `lib/sahne/*.js` (okuyabilirsin; **hiçbir dosyayı değiştirme**, commit yapma).

## Bilinmesi gerekenler
- Kanal verisi: izleyicinin %48'i telefonda, %22'si TV'de; %38'i Türkçe altyazıyla izliyor; kayıp ilk 10–15 saniyede; bölümlü yapı tutuyor. Telefon sınaması için kareye 427 px genişlikte de bak.
- Alt bant (y > 880) altyazıya ayrılmıştır; ekran yazıları oraya gelmez.
- Kapak A'nın yazısı "BEN CEHENNEMİM"; açılış karesi (A01) bu vaadi ilk 5 saniyede karşılamak için kuruldu. A01 → G07 → L07 aynı karenin üç çağrısıdır; L09 onun aynasıdır.
- Sesi dinleyemezsin; ritmi `timeline.js`'teki cümle/kelime zamanları ve plan süreleriyle değerlendir.
- Üslubun bilinen sınırı: kodla çizimde yüz, el ve karmaşık beden hareketi zayıftır; film siluet, kompozisyon, ışık ve az ama anlamlı hareket üzerine kuruludur. "Elle çizilmiş gibi olsun" bir bulgu değildir; "şu kare şu yüzden ucuz/okunmaz duruyor ve şöyle düzelir" bir bulgudur.

## Rapor (kendi dosyana yaz: `kurul/kurgu_tur1/<adın>.md`)
1. **Puan** (0–10, bir ondalık) ve **ONAY / RED** (eşik 9,0; hiçbir ölçüt 7'nin altında olamaz). Ölçütlerini ve ağırlıklarını kendi merceğine göre 4–6 madde olarak sen koy, her birine puan ver.
2. **Engelleyici bulgular** (varsa): yayına bu hâliyle çıkılamaz dediğin şeyler.
3. **Sıralı düzeltme listesi** (en çok 15 madde; en çok kazandıracak olan en üstte). Her madde: plan kimliği ve film zamanı, 1920×1080 koordinatıyla yer, sorun (ilk kez gören biri ne sanıyor?), somut düzeltme, beklenen kazanç (puan). Baktığın karenin yolunu yaz.
4. **İyi olan ve korunması gereken** (en çok 5 madde).
5. **En emin olmadığım nokta.**
Son mesajında raporun yolunu, puanı, kararı ve ilk beş bulguyu ver.
