Yeni video: **Gılgamış** ("Mitler ve Felsefe" serisi). Baştan sona üret.
- Kararlar senin, başkan sensin. Kurul, puanlama ve çok ajanlı akış yok (19 Kasım kararı); bir konuda emin değilsen bana sor.
- ElevenLabs ve görsel üretim gibi kredi harcayan her çağrıdan önce karakter × çekim hesabını bana bildir ve onay al.

## 1. Önce oku
- `CLAUDE.md` (bütün kurallar ve yayın sonrası dersler), `sisifos/README.md`, `sisifos/yayin.md`.
- En yeni projeler:
  - `dorian-gray/geriye_bakis.md` (karma üslup, müzik denetimi, Fable'ın son yorumu);
  - `narkissos/uretim_plani.md` (mit videosu; cümle düzeyinde hizalama `tools/hizala_cumle.py`);
  - `kafka/geriye_bakis.md` ve `kafka/lib/` (ağaç baskı motoru; aşağıdaki üslup önerisinin çıkış noktası).
- `analiz/tahminler.md` ve `araclar/analiz/tempo_kontrol.py`.
- Araştırma: `analiz/2026-11-23-bosluk-2-ve-gilgamis.md`, `analiz/2026-11-23-turkce-medyan.md`; iki dilli arama aracı `araclar/talep/iki_dil.py`.

## 2. Neden bu konu
- **İzleyici isteği:** yorumlarda 2–3 izleyici Gılgamış'ı istedi.
- **Talep:** dünyada çok büyük (İngilizce "epic of gilgamesh" ilk 10 medyanı ~2 M). Türkçede orta ("gılgamış destanı" ~43 B, "gılgamış" ~122 B); Türkçe videoların çoğu söyleşi ya da sesli kitap.
- **Türkiye kapısı:** Hattuşa (Boğazköy, Çorum).
- **Telif:** metin kamu malı.

## 3. Kaynaktaki sürprizler
Araştırma dosyasında ayrıntılı; kaynak denetiminde her biri yeniden doğrulanır.
1. **Hattuşa:** Geç Tunç Çağı'ndan Gılgamış'a dair, diğer bütün yerlerin toplamından fazla metin Hattuşa'dan çıktı: Akadca, Hurrice ve Hititçe (Beckman, *The Hittite Gilgamesh*, 2019). Hititçe metin çeviri değil, kısaltılmış bir yeniden anlatım.
2. **2011, Süleymaniye Müzesi:** kaçakçılardan alınan V. tablet parçası 20 yeni dize ekledi (Al-Rawi ve George, 2014). Sedir Ormanı çığlık atan maymunlar, kuşlar ve böceklerle dolu bir cennet; kahramanlar onu kesip götürüyor.
3. **Siduri'nin öğüdü** ("yiyip iç, sevdiğini sev…") yalnız Eski Babil sürümünde var (Sippar tableti, ~MÖ 1700). Standart sürümde yok.
4. **1872:** George Smith XI. tableti (K.3375) okudu ve 3 Aralık 1872'de açıkladı. "Heyecandan soyundu" anekdotu doğrulanmadı; kullanılırsa "anlatılır ki" diye verilir.
5. **Halka yapı:** destan Uruk surlarıyla açılır ve surlarla kapanır (I. ve XI. tablet). Dizeleri karşılaştırarak doğrula.

## 4. Omurga fikri
Bu bir öneri; kaynakla sınanacak.
- **İskelet:** Kahramanın Yolculuğu. Kahraman Gılgamış; bedeli ödeyen ve yolu açan Enkidu.
- **Sıradan dünya:** Uruk'ta zorba kral.
- **Çağrı:** Enkidu'nun yaratılışı. Şamhat'la "insanlaşması" metinde cinseldir, ima ile anlatılır.
- **Sınavlar:** dostluk, Humbaba ve orman (2011 dizeleri), İştar ve Gök Boğası.
- **Kırılma:** Enkidu'nun ölümü; Gılgamış onu gömmeyip bekler (X. tablet; dizeleri doğrula).
- **Büyük sınav:** Utnapiştim'e yolculuk, Siduri, tufan anlatısı.
- **Doruk:** ölümsüzlük bitkisini bulur, yıkanırken yılan çalar ve deri değiştirir.
- **İksir:** surlar, yani iz bırakmak.
- **Kişisel soru (başlık adayı):** "Ölümsüz olabilseydin, neyi bırakırdın?" / "Sevdiğin ölünce ne yapardın?"
- **Türkiye kapısı:** Hattuşa, hikâyenin içinde ve ilgili sahnenin yanında verilir. Kancanın arkasına köprü olarak konmaz. Örnek: Gılgamış'ın adının Anadolu'ya ulaştığı an. Kapak ya da başlık adayı olarak da denenebilir.

## 5. Akış
Hepsi `gilgamis/` klasöründe, CLAUDE.md'deki sırayla.
1. **`uretim_plani.md`:**
   - Talep kontrolü: `talep.py` ve `iki_dil.py`; kontrol satırları "sisifos" ve "dönüşüm kafka".
   - **En az 10 başlık adayı** ve seçim gerekçesi. "Gılgamış" başlıkta önde olsun; ≤ 45 karakter. Art arda iki videoda aynı kalıp kullanılmaz.
   - İki kapak taslağı: iki ayrı vaat, kompozisyon menüsünden iki farklı kalıp (ör. yılan ve bitki, "ortadan başlamak"; Gılgamış ve Enkidu'nun bedeni, "karşıtlık").
   - İskelet ve merak döngüleri, cümle numaralarıyla. Bir önceki videonun iskeletini yaz.
2. **Senaryo (`senaryo.json`):**
   - Kancadan hikâyeye köprü sıfır cümle; hikâye en geç 0:45'te başlar.
   - Somut olay tutar: karşılaştırma ya da çıkarım olaydan sonra tek cümle olur, art arda iki soyut cümle olmaz.
   - Merak cevabı bir olaydır (yılan), kavram değil.
   - Enkidu, Şamhat, Humbaba ve Utnapiştim ilk perdede adıyla ve görüntüsüyle ekilir.
   - 1872 keşfi ve tablet bilgileri ilgili sahnenin yanına konur; bilim tarihine ayrı bir bölüm açılmaz.
   - Abone çağrısı ve iksir son sahnenin (surlar) içinde verilir.
3. **Tempo ve tahminler:** `tempo_kontrol.py`'yi çalıştır, her işaretli cümleye "olay" ya da "soyut" de. 3 tempo tahminini **yayından önce** `analiz/tahminler.md`'ye yaz.
4. **Kaynak denetimi seslendirmeden önce:** `kaynak/DOGRULAMA.md` yaz. Her dize tablet ve satır numarasıyla verilir.
   - Kamu malı metinler depoya alınır: Jastrow ve Clay, *An Old Babylonian Version of the Gilgamesh Epic* (1920, Gutenberg #11000); R. Campbell Thompson (1928–30; çevirmen 1941'de öldü, Türkiye'de kamu malı; lisansı kendin doğrula).
   - Andrew George'un çevirileri, Beckman ve Türkçe çeviriler telifli: yalnız fikir ve olgu kaynağı.
   - Dizeleri kamu malı çeviriden kendi Türkçemizle ver.
5. **Seslendirme:** Emrullah sesi. `voice_id`'yi `creative_list_voices` ile bul; kredi onayını al. Adların okunuşunu (Gılgamış, Enkidu, Utnapiştim, Şamhat, Humbaba, Siduri, Uruk) ilk denemede dinlenecekler listesine yaz.
6. **Üslup:** sıra önce kendi motorlarımız, sonra cinecode, sonra Lemo.
   - Önerim **silindir mühür baskısı**: hikâye kile yuvarlanan bir mühürle basılır, kamera mühürle birlikte yürür.
   - Hazır motorların hiçbirinde Mezopotamya kabartması yok. En yakını Kafka'nın ağaç baskı motoru (kendini oyan kabartma baskı). Kil tonu ve kabartma gölgesiyle uyarlamayı dene; uymazsa gerekçesiyle başka yol seç.
   - Figürler profilde ve siluette.
   - Gerçek görseller "yer yer" kullanılabilir: British Museum'daki tufan tableti, Hattuşa tabletleri, Asur kabartmaları. Lisanslarını tek tek kontrol et (CC0 ya da kamu malı), `araclar/ASSETS.md`'ye kaydet, tam boyda her köşesine bak.
   - Üslup kapısı tek kare değil: manzara + orta plan figür + yakın plan + 15 sn hareket.
7. **Hassasiyet, görüntüyle birlikte:**
   - Tufanı dinî anlatılarla karşılaştırma (Milton kararı); 1872'deki yankı yalnız tarih olarak verilir.
   - Şamhat ve İştar sahneleri ima ile anlatılır; Gök Boğası ve Humbaba şiddeti ölçülü.
   - Tanrı figürleri ve amblemler (kanatlı disk, yıldız) bugünkü dinî ya da siyasi simgelere benzemesin. Figür pozlarını render'dan önce tara.
   - Irak'tan kaçırılan eserler gerekirse yalnız olgu olarak anlatılır.
8. **Müzik ve efekt:** müzik videonun tonuna göre yeni yazılır (seri ya da kategori kuralı yok). Saniye saniye düzey eğrisini bas.
9. **Render, kapak ve yayın:**
   - Render, iki kapak, `yayin.md` (bölüm damgaları, künye ve kaynaklar), SRT, üç teslim kopyası (`SendUserFile`).
   - Shorts yayından birkaç gün sonra.
   - İstersen sonda Fable'a tek son yorum yaptır.
   - Gılgamış'ı isteyen yorumlara verilecek yanıt metnini `yayin.md`'ye yaz; yorumlara ben cevap veririm.
10. **Yayın tarihi:** sırada Dorian Gray (30 Kasım) ve Lale Çılgınlığı var; aralık en az 5–7 gün. Tarihi benimle kesinleştir.

Her iş parçasından sonra commit ve push yap. Video bitince dal `main`'e birleştirilir. CLAUDE.md'ye "Gılgamış dersleri" bölümünü ve tablo satırını ekle.
