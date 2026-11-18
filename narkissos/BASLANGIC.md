# Narkissos ve narsisizm: yeni sohbet için başlangıç promptu (18 Kasım 2026)

Yeni bir videoya başlıyoruz: **Narkissos ve Eko miti → narsisizm**. Önce `CLAUDE.md`'yi baştan sona oku; kanalın bütün kuralları (Emrullah sesi, kredi onayı, kurul kapıları, talep kontrolü, 10 başlık adayı, iskelet, Ran ve Kafka dersleri, kurgu önerileri) orada. Proje klasörü `narkissos/`. Çalışma dalın oturumun verdiği dal; iş bitince `main`'e birleştirilir.

## Önce oku
- `analiz/2026-11-18-sisifos-sonme.md`: bu video neden önemli. Kanalın motoru Sisifos'tu ve söndü; yeni videolar büyük test almıyor. Bu video **yeni kapı** olmak için seçildi.
- `analiz/2026-11-18-konu-adaylari.md`: talep ölçümü ("narsisizm" ilk 10 medyanı ~200 B; "narkissos" zayıf, ~22 B). Kapı kelimesi **narsisizm**, mit içeriktir. Ölçüm aracı: `araclar/talep/talep.py`.
- `analiz/2026-11-18-kafka-48saat.md` ve `analiz/2026-11-17-kanal-ortalamasi.md`: ölçüt çizgisi (TO %1,8, 0:30 %61, ortalama izlenme %39,8; Kafka %45,4 ile en iyi).
- Bu dosyalar `main`'de yoksa `git fetch origin claude/peaceful-turing-d97m8o` yapıp oradan oku.

## Konu ve omurga (öneri; kullanıcıyla netleştir)
- **Kaynak:** Ovidius, *Metamorphoses* III (Narkissos ve Eko, yaklaşık 339–510). Latince metni satır numarasıyla `narkissos/kaynak/` altına al (İkaros dersi: sürpriz kaynağın kendisinde). Satır numaralarını kaynak denetçisi doğrular. Kritik anlar:
  - Tiresias'ın kehaneti ("kendini tanımazsa" uzun yaşar);
  - Juno'nun Eko'yu yalnız başkalarının son sözlerini tekrarlamaya mahkûm etmesi;
  - havuz;
  - Narkissos'un "o benim" diye **anladığı** an: bildiği hâlde ayrılamaz;
  - çiçeğe dönüşüm.
- **Sürpriz önerisi:** Narkissos cahil değildi. Yansımanın kendisi olduğunu anladı ve yine de ayrılamadı; bilmek yetmiyor. Eko ise karşı kutup: yalnız başkalarının sözüyle var olabiliyor. İkisi aynı yaranın iki ucu mu?
- **Bugüne köprü:**
  - Kavramın tarihi: Havelock Ellis 1898, Paul Näcke 1899, Freud 1914 "Narsisizm Üzerine". Tarihler ve atıflar kaynaktan doğrulanır.
  - Sağlıklı kendini sevme ile kişilik bozukluğu arasındaki fark.
  - Su yüzeyinin telefon ekranına dönüşmesi.
- **Kişisel soru taslakları:** "Kendini sevmek ne zaman hastalığa döner?" · "Aynada aradığın kim?" · "Herkes mi narsist oldu, yoksa kelime mi değişti?"
- **Hassasiyet ve politika (önemli):**
  - Video teşhis ya da tedavi vaadi vermez ("partnerin narsist mi?", "nasıl tedavi edilir" açıları yok). Otomatik tamamlamada bu aramalar çıksa da kullanılmaz.
  - YouTube'un "özgün olmayan içerik" kuralı, sağlık konusunda insan uzmanı gibi davranan yapay zekâ karakterlerini para kazanmaya uygun saymıyor. Anlatıcı uzman gibi tavsiye vermez; kavramı ve mit okumasını anlatır, kaynak gösterir.
  - Psikolojik rahatsızlık alay konusu yapılmaz.
  - Hassasiyet kurulu üslup karesi aşamasında çalışır.

## İş sırası
1. **Talep kontrolü ve paketleme taslağı:**
   - `araclar/talep/talep.py` ile "narsisizm", "narsist", "narkissos", "eko nimfa" ve kontrol satırları ölçülür.
   - 10 başlık adayı yazılır; kapı kelimesi başlıkta olur.
   - En az iki kapak fikri, **iki farklı kompozisyondan** seçilir (CLAUDE.md, kapak kompozisyonu seçenekleri). Örnek: "ortadan başlamak" (havuza eğilmiş figür) ve "karşıtlık" (Narkissos ve Eko).
   - Hepsi `narkissos/uretim_plani.md`'ye yazılır.
2. **İskelet** (`yonetmenlik` becerisi): son iki video Kafka = Kişōtenketsu, Ran = Harmon çemberi. Seçim ve gerekçe plana yazılır, merak döngüleri de.
   - Kanca kuralları: kancadan sonra hikâye en geç 0:45'te başlar. Kancanın hemen arkasına bilinen bağlam ya da alıntı konmaz (İkaros ve Kafka dersi).
   - İfşadan sonraki yorum kısa tutulur. Abone çağrısı hikâyenin son anının içinde verilir.
3. **Senaryo** (`senaryo.json`, cümle cümle) ve kurulu.
4. **Üslup kapısı.** Kullanıcı üslubu başka bir sohbette seçecek. Seçim gelmediyse şu adayları aynı sahneyle sına; uygulama ayrıntısı `CLAUDE.md` "Üslup ve çizim motoru seçimi", `araclar/lemo/KATALOG.md`, `araclar/lemo/getir.sh`:
   - **vazo** (hazır motor, `sisifos/lib` ve `prometheus/`);
   - **ışıklı kâğıt kutu** (cinecode `paper-lantern`, Lemo demo motoru, WebGL);
   - **tek çizgi** (cinecode `one-line`, Lemo motoru, WebGL'siz);
   - **kâğıt kesme** (Orfeus'un kapak ilkeleri `orfeus/kapak.js`; film hattı yok).

   Kapı her zamanki gibi manzara + orta plan figür + yakın plan + 15 sn hareket. Yansıma ve "su → ekran" geçişi mutlaka denenir.
5. **Seslendirme:** kredi hesabını (karakter × çekim) kullanıcıya bildir, açık onay al. Animasyon, ses ve miks, render, Shorts, kapak test seti, `yayin.md` sonra gelir.

## Bu videoda denenecekler (öneri)
- **Sessiz okuma testi:** kurgu özetinin yazısız kareleri, planı görmemiş yeni bir alt ajana verilir (CLAUDE.md, kurgu önerileri).
- **Yenilik ölçümü:** kesme ya da sözcüğe bağlı eylem olmadan 5 sn'yi aşan aralıklar listelenir.
- **Kapak araçları:**
  - `araclar/kapak/odak.py` ile göz ilk nereye gidiyor, ölçülür.
  - İki kapaktan biri 4–6 kelimelik yazıyla denenebilir.
- **Gerçek görsel araları:** Caravaggio'nun *Narkissos*'u (~1597–99) ve Waterhouse'un *Eko ve Narkissos*'u (1903) kamu malı olabilir. Lisans ve kaynak `kaynak/GORSELLER.md`'ye işlenir (Ran yöntemi).
- **Dil paketi:** `analiz/dil_denemesi.md` sonucu olumluysa İngilizce ve İspanyolca başlık, açıklama ve altyazı. Denetim `araclar/altyazi/denetle.py` ile yapılır.
- **Yayın zamanı:** Ran'dan (17 Kasım) en az 5–7 gün sonra, en erken ~24–25 Kasım. Shorts uzun videodan birkaç gün sonra çıkar (yayın aralığı denemesi).
