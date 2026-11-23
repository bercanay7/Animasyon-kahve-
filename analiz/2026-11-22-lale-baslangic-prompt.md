Yeni video: **Lale Çılgınlığı** ("Tarihin Dönüm Noktaları" serisi). Baştan sona üret.
- Kararlar senin, başkan sensin. Kurul, puanlama ve çok ajanlı akış yok (19 Kasım kararı); bir konuda emin değilsen bana sor.
- ElevenLabs ve görsel üretim gibi kredi harcayan her çağrıdan önce karakter × çekim hesabını bana bildir ve onay al.

## 1. Önce oku
- `CLAUDE.md` (bütün kurallar ve yayın sonrası dersler), `sisifos/README.md`, `sisifos/yayin.md`.
- En yeni iki proje: `dorian-gray/geriye_bakis.md` ve `dorian-gray/uretim_plani.md` (karma üslup, Mary Stuart piyanosu, kapak, yayın), `narkissos/uretim_plani.md` (cümle düzeyinde hizalama).
- `analiz/tahminler.md` ve `araclar/analiz/tempo_kontrol.py`.
- Konunun seçim gerekçesi: `analiz/2026-11-22-turkce-bosluk.md`, `analiz/2026-11-21-konu-adaylari-3.md`; iki dilli arama aracı `araclar/talep/iki_dil.py`.

## 2. Neden bu konu
Kullanıcının ölçütü: dünyada yankı bulmuş, Türkçede kaynağı az, Türkiye'yi ilgilendirmesi gereken konu.
- İngilizcede "tulip mania" için ilk 10 videonun medyanı ~204 B. Türkçede "lale çılgınlığı" için en çok izlenen video ~17 B.
- Türkiye bağı: lale Avrupa'ya İstanbul'dan gitti ve Osmanlı'nın kendi "Lale Devri" var.
- Bugünkü karşılığı kripto, döviz ve altın kovalayan izleyici.

## 3. Omurga fikri
Bu bir öneri; kaynakla sınanacak, tutmayan çıkarılacak. Ana fikir: **iki lale çılgınlığı, iki efsane.**
- **Lalenin yolculuğu:**
  - Habsburg elçisi Busbecq İstanbul'da laleyi görüyor; mektupları 1581'de yayımlandı. "Tulipan" adının tülbentten geldiği anlatılır; bunu doğrula.
  - Clusius laleyi 1593'te Leiden'e götürüyor.
- **Hollanda, 1636–37:**
  - Semper Augustus soğanı, Haarlem meyhanelerinde elde olmayan soğanın alım satımı (*windhandel*), Şubat 1637 çöküşü.
  - Fiyat iddialarını ("bir ev fiyatı", florin rakamları) kaynaktan doğrula.
  - Kamu malı kaynaklar: 1637 broşürleri (*Samenspraeck tusschen Waermondt ende Gaergoedt*), Mackay, *Extraordinary Popular Delusions* (1841).
- **Efsane 1:**
  - Mackay'in hikâyeleri: lale soğanını soğan sanıp yiyen denizci, iflas edenler.
  - Anne Goldgar, *Tulipmania* (2007): arşivde iflas dalgası bulunmuyor; çöküş sonradan bir ahlak hikâyesine dönüştü. Kitap telifli, yalnız fikirler kendi cümlelerimizle aktarılır.
- **İstanbul, 1718–1730:**
  - Kişiler ve olaylar: III. Ahmed, Nevşehirli İbrahim Paşa, çırağan şenlikleri.
  - Lale fiyatları 1726–27'de tepe yaptı ve devlet işe karıştı. Nasıl karıştığını (narh mı, tavan mı, ferman metni) birincil ya da akademik kaynaktan kesinleştir. İlk ipucu: YÖK Açık Bilim 20.500.12812/630392, *Lale Devri'nin Lalesi*.
  - 1730'da Patrona Halil isyanı.
- **Efsane 2:**
  - "Lale Devri" adı dönemin kendisinden değil, sonradan konmuş olabilir (Ahmed Refik, 1913?). Can Erimtan, *Ottomans Looking West?* Doğrula.
  - Doğrulanırsa iki çılgınlık aynı yerde buluşur: ikisini de sonradan anlatılan hikâye büyüttü.
- **İksir:** "Herkes alıyor diye sen de alır mıydın?" ve "Balonu fiyat mı büyütür, hikâye mi?"
  - Yatırım tavsiyesi verme.
  - Bugünden belirli bir varlık, kişi ya da kurum adı anma.

## 4. Akış
Hepsi `lale-cilginligi/` klasöründe, CLAUDE.md'deki sırayla.
1. **`uretim_plani.md`:**
   - Talep kontrolü: `araclar/talep/talep.py` ve `iki_dil.py`, kontrol satırlarıyla.
   - **En az 10 başlık adayı** ve seçim gerekçesi. Tanıdık kapı başlıkta önde olsun: "lale", "Lale Devri", "balon". Başlık ≤ 45 karakter.
   - İki kapak taslağı: iki ayrı vaat, CLAUDE.md'deki kompozisyon menüsünden iki farklı kalıp.
   - İskelet: tablodan seç ve cümle numaralarıyla yaz. Merak döngülerini yaz (soru → cevabı olan olay). Bir önceki videonun iskeletini yaz.
2. **Senaryo (`senaryo.json`):**
   - Kancadan hikâyeye köprü sıfır cümle; hikâye en geç 0:45'te başlar.
   - Somut olay tutar, soyut çözümleme düşürür: karşılaştırma olaydan sonra tek cümle olur.
   - Merak sorusunun cevabı bir olaydır.
   - Doruğu taşıyacak kişiler (İbrahim Paşa, Patrona Halil) ilk perdede adıyla ve görüntüsüyle ekilir.
   - Bağlam bilgisi ilgili sahnenin yanına konur.
   - Abone çağrısı ve iksir hikâyenin son anının içinde verilir.
3. **Tempo ve tahminler:** `tempo_kontrol.py`'yi çalıştır, her işaretli cümleye "olay" ya da "soyut" de. 3 tempo tahminini **yayından önce** `analiz/tahminler.md`'ye yaz.
4. **Kaynak denetimi seslendirmeden önce:** `kaynak/DOGRULAMA.md` yaz; her tarih, fiyat ve alıntı kaynağıyla. Kamu malı metinleri depoya al.
5. **Seslendirme:** Emrullah sesi. `voice_id`'yi `creative_list_voices` ile bul; kredi onayını al.
6. **Üslup:** önce kendi motorlarımız, sonra cinecode, sonra Lemo.
   - Önerim Dorian'daki gibi fikrin görüntünün kuralı olması: dünya gravür (`milton` motoru), yalnız laleler renkli. Renk değer demek: çöküş anında laleler rengini yitirir.
   - Gerçek görseller: 1630'ların Hollanda lale kitapları ve Levnî minyatürleri (*Surname-i Vehbi*). Her birinin lisansını tek tek kontrol et, `araclar/ASSETS.md`'ye kaydet, tam boyda her köşesine bak.
   - Üslup kapısı tek kare değil: manzara + orta plan figür + yakın plan + 15 sn hareket.
7. **Hassasiyet, görüntüyle birlikte:**
   - III. Ahmed'i "sefih padişah" diye karikatürleştirme; Patrona Halil isyanındaki şiddeti gösterme.
   - Dini figür ve vaaz çağrışımı olmasın (Kalvinist vaazlar ya da cami içi).
   - Kıyafet ve amblemleri tara.
8. **Müzik ve efekt:** müzik videonun tonuna göre yeni yazılır. Saniye saniye düzey eğrisini bas.
9. **Render, kapak ve yayın:**
   - Render, iki kapak, `yayin.md` (bölüm damgaları, künye, kaynaklar), SRT, üç teslim kopyası (`SendUserFile`).
   - Shorts yayından birkaç gün sonra.
   - İstersen sonda Fable'a tek son yorum yaptır.
10. **Yayın tarihi:** Dorian Gray 30 Kasım'da çıkıyor; aralık en az 5–7 gün. Tarihi benimle kesinleştir.

Her iş parçasından sonra commit ve push yap. Video bitince dal `main`'e birleştirilir. CLAUDE.md'ye "Lale Çılgınlığı dersleri" bölümünü ve tablo satırını ekle.
