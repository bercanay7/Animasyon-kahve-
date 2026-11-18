# Narkissos ve Eko → narsisizm: üretim planı

Başlangıç: 18 Kasım 2026. Bağlam: `BASLANGIC.md`, `analiz/2026-11-18-sisifos-sonme.md`, `analiz/2026-11-18-konu-adaylari.md`.
**Çalışma düzeni (kullanıcının kararı, 18 Kasım):** kurul yok (`KURUL.md` tutulmaz). Başkan kendi denetler; gerektiğinde bağımsız bir model (Fable 5.2) danışman olarak dışarıdan bakar. Ölçütler ve kanal kuralları (CLAUDE.md) aynen geçerli.

## 1. Talep kontrolü (18 Kasım 2026)
Ölçüm: `python3 araclar/talep/talep.py …` (YouTube Türkçe otomatik tamamlama + aramadaki ilk 10 videonun izlenmeleri). Medyan gürültülü: "narsisizm" bugün 152 B, dün 202 B verdi.

| Sorgu | Öneri | İlk 10 medyan | Öne çıkan öneriler |
|---|---|---|---|
| **narsisizm** | 12 | **152 B** | nedir, nasıl tedavi edilir, belirtileri, film |
| narsisizm nedir | 1 | 139 B | |
| **narsist kişilik bozukluğu** | 14 | **109 B** | tedavisi, belirtileri, nedir, kadın |
| narsist | 14 | 81 B | nasıl başa çıkılır, narsistle aşk, narsist anne |
| **kendini sevmek** | 14 | **125 B** | için neler yapılabilir, meditasyon, "kendini sevmek normaldir" |
| narkissos | 9 | 6,5 B | "narkissos hikayesi"; geri kalanı konu dışı (şarkı, yarışma) |
| narkissos efsanesi / narkissos ve eko | 3 / 4 | ~0,7 B | "narcissus hikayesi" |
| narsisizm mitoloji / narsisizm freud | 2 / 3 | <1 B | |
| nergis efsanesi / eko nimfa | 2 / 2 | ~3 B / 0 | konu dışı |
| *kontrol:* sisifos / dönüşüm kafka | 14 / 14 | 33 B / 31 B | "sisifos meme", "sisifos edit" |

**Okuma:**
- (a) **Tanıdık kapı güçlü, ama mitte değil kavramda:** "narsisizm" ve "narsist kişilik bozukluğu" Sisifos ve Kafka'nın 3–5 katı. "Narkissos" Milton düzeyinde zayıf. Kapı kelimesi başlıkta **narsisizm** (ya da narsist), mit içeriktir.
- **İkinci kapı "kendini sevmek"** (125 B): kişisel gelişim araması. Başlıkta narsisizmle yan yana durursa iki talebi birden yakalar.
- **Politika uyarısı:** "narsist" önerileri ilişki ve tanı yönlü ("nasıl başa çıkılır", "narsist anne", "tedavisi"). Bu açılar kullanılmaz (BASLANGIC, hassasiyet). Video teşhis koymaz, tavsiye vermez; kavramın tarihini ve mitin okumasını anlatır.
- (b) **Kişisel soru:** "Kendini sevmek ne zaman hastalığa döner?" izleyicinin kendi hayatına soruluyor ve iki kapıyı birden taşıyor. Aşağıda adaylar.

## 2. Kaynak
- `kaynak/ovidius_met3_336-512.txt`: Latince metin, satır numaralı (Magnus 1892, Perseus aracılığıyla).
- **Kaynaktaki sürpriz (ilk okuma, senaryo aşamasında kaynakla denetlenecek):**
  - **"copia" yankısı.** Narkissos Eko'yu "ante emoriar, quam sit tibi copia nostri" (391: bana sahip olmana izin vermektense ölürüm) diye reddeder. Eko yalnız "sit tibi copia nostri" (392: bana sahip ol) diyebilir. Havuzda Narkissos kendine "inopem me copia fecit" (466: sahip olduğum şey beni yoksul kıldı) der. Eko'ya söylediği kelime sonunda kendi ağzından ona döner. Ovidius bu kelimeyi Eko'nun yankısıyla bağlıyor.
  - **"Iste ego sum: sensi, nec me mea fallit imago"** (463: o benim, anladım, hayalim beni kandırmıyor). Narkissos cahil değil; bildiği hâlde ayrılamıyor (BASLANGIC'teki sürpriz önerisi kaynakta doğrudan var).
  - "O utinam a nostro secedere corpore possem!" (467: keşke bedenimden ayrılabilsem). Sevdiğini kendinden uzaklaştırmak istiyor; "kendine âşık" basitlemesinin tersi.
  - Tiresias: "si se non noverit" (348: kendini tanımazsa). Delfi'nin "kendini tanı"sının tersine çevrilmiş hâli.
  - Ölümden sonra bile Styks'in suyunda kendine bakar (504–505). Eko son "vale"yi tekrarlar (501) ve ağıtlara yankıyla eşlik eder (507).

## 3. Başlık adayları (CLAUDE.md: en az 10; her biri beş soruyla elenir)
Sorular: **K**işisel soru mu · **N**efes (tek nefeste okunur mu) · **Y**arı tahmin ettirir, ele vermez mi · **Ka**pı kelimesi içinde mi · **B**ağlamsız anlaşılır mı.

| # | Aday | K | N | Y | Ka | B | Not |
|---|---|---|---|---|---|---|---|
| 1 | Kendini Sevmek Ne Zaman Narsisizme Döner? \| Narkissos'un Hikâyesi | ✓ | ✓ | ✓ | ✓✓ | ✓ | İki kapı (kendini sevmek + narsisizm). Vaadi videoda karşılanmalı: cevap kavram tarihinden ve mitten gelir, tavsiyeden değil |
| 2 | Bildiğin Hâlde Bırakamıyor musun? \| Narsisizmin Kökenindeki Efsane | ✓ | ~ | ✓ | ✓ | ✓ | Sürprizi ("bilmek yetmiyor") taşır; biraz uzun |
| 3 | Herkes mi Narsist Oldu, Yoksa Kelime mi Değişti? \| Narkissos ve Eko | ~ | ✓ | ✓ | ✓ | ✓ | Toplumsal soru; "narsist" arayanı yakalar. Video bu soruyu cevaplamaya yetmezse vaat boşa düşer |
| 4 | Kendine Bakmaktan Vazgeçebilir misin? \| Narsisizm ve Narkissos | ✓ | ✓ | ✓ | ✓ | ✓ | Yumuşak, kişisel; "bakmak" ekran çağrışımı da taşır |
| 5 | Aynada Aradığın Kim? \| Narsisizm ve Narkissos Efsanesi | ✓ | ✓ | ✗ | ✓ | ✓ | Cevabı tahmin ettirmiyor; genel ve şiirsel |
| 6 | Narsist Kendini Sever mi? \| Narkissos'un 2000 Yıllık Cevabı | ~ | ✓ | ✓ | ✓ | ✓ | Kaynak destekliyor (467), ama "narsist kendini sevmez" bilimsel olarak tartışmalı; hassas |
| 7 | Ekranına Bakmayı Neden Bırakamıyorsun? \| Narkissos ve Narsisizm | ✓ | ✓ | ✓ | ✓ | ✓ | Güçlü ama vaadi telefon bağımlılığı; video bunu bir bölümde anlatıyor. Yanıltma riski |
| 8 | Narsisizm Nedir? Hepsi Bir Havuzda Başladı \| Narkissos ve Eko | ✗ | ✓ | ~ | ✓✓ | ✓ | "narsisizm nedir" araması (139 B); kişisel soru yok |
| 9 | Seni Yalnız Tekrar Eden Biri mi Var? \| Narsisizm ve Eko | ✓ | ✓ | ~ | ✓ | ✗ | Eko açısı; ilişki teşhisine kayar (hassasiyet: kullanılmaz) |
| 10 | Kendini Sevmek Suç mu? \| Narsisizmin Kökenindeki Efsane | ✓ | ✓ | ✓ | ✓✓ | ✓ | 1'in sert hâli; "suç" kelimesi yanlış çerçeve (mit cezayı aşka değil kibre verir) |
| 11 | Narkissos Yansımasının Kendisi Olduğunu Biliyordu \| Narsisizm | ✗ | ✓ | ✓ | ✓ | ~ | Sürpriz cümlesi; kişisel değil, bilgi merakı (İkaros'un zayıflığı) |
| 12 | Hiç Kendi Yansımana Takıldın mı? \| Narsisizmin Kökeni: Narkissos | ✓ | ✓ | ~ | ✓ | ✓ | 4'e yakın; "takılmak" günlük dil |

**Başkanın ön seçimi (iskelet ve senaryodan sonra kesinleşir):** **1. aday.** İki tanıdık kapıyı ("kendini sevmek", "narsisizm") tek kişisel soruda birleştiriyor. Cevabı yarı tahmin ettiriyor (bir sınır var), ama sınırın ne olduğunu vermiyor. Son iki video da "…mi?" sorusuyla bitiyordu; bu aday "ne zaman" sorusuyla ayrılıyor. **Yedek: 4. aday** ("Kendine Bakmaktan Vazgeçebilir misin?"); sürprizi ("bilmek yetmiyor") ve su→ekran köprüsünü birlikte taşır. Yanıltma riski nedeniyle elenenler: 7 (vaat telefon), 9 (ilişki teşhisi), 10 (yanlış çerçeve).

## 4. Kapak fikirleri (iki ayrı vaat, iki ayrı kompozisyon; ayrıntı üslup seçilince)
- **A, "ortadan başlamak":** Narkissos suya eğilmiş, yüzü yansımasına birkaç parmak uzaklıkta. Tek odak yansımadaki göz: karenin en parlak noktası. Yansıma ¾ yüz, gerçek baş karanlık siluet. Vaat: "kendini gördü ve bırakamadı". Yazı 2–3 kelime ("O BENİM" ya da "BİLİYORDU"). 4–6 kelimelik deneme: "KENDİNİ TANIDI, YİNE DE BAKTI".
- **B, "karşıtlık":** solda ışıkta suya bakan Narkissos, sağda karanlıkta kayaya karışmış Eko. Eko'nun yankısı yazı olarak görünür (son kelimenin tekrarı, giderek silikleşen harfler). Vaat: "biri yalnız kendini, öteki yalnız başkasını duyuyor".
- **Yedek C, "su → ekran":** havuzun yüzeyi telefon ekranı, yansımadaki yüz ekranda. İzleyicinin hayatına en yakın vaat, ama videonun yalnız bir bölümünü anlatıyor; yanıltmaması için ancak senaryo bu köprüyü güçlü kurarsa denenir.
- Kapak yazısı hassasiyetten geçer: "NARSİST" kelimesi tek başına kapakta kullanılmaz (teşhis vaadi gibi okunur).

## 5. Üslup (18 Kasım 2026)
Araştırma: yedi dilim (Lemo'nun 99 üslubu, cinecode, kendi yedi motorumuz, GitHub, sanat tarihi ve lisans), bir sentez, sekiz iddia doğrulaması ve Fable 5.2'nin bağımsız denetimi. Ham raporlar oturumun çalışma alanında kaldı; Lemo belgeleri CC BY-NC olduğu için depoya alınmadı. Başkanın önerisi **kullanıcı tarafından onaylandı** (18 Kasım, aşağıdaki "Kullanıcının kararları").

### Başkanın önerisi
**Ana üslup: vazo** (kendi motorumuz, `prometheus/lib`). Üslup kapısında aynı sahneyle **risografa** (Lemo `risograph`) karşı sınanır. Risograf aşağıdaki dört ölçütün dördünde de açık farkla kazanırsa seçilir; beraberlik vazoya gider. Sentez risografı birinci koymuştu; Fable 5.2 ve iddia doğrulamaları vazoyu öne aldı. Başkan doğrulamalara katılıyor.

**Neden vazo:**
- **Çalışan kanıt:** insan figürü, yansıma ve gözyaşı halkası birlikte çalışan tek aday (ajan denemesi; yakın planda karşılıklı profil).
- **Küçük boyda okunurluk:** 168 ve 120 px'te en okunaklı deneme. `odak.py` iki tepeyi de yüze ve yansımasına koyuyor; figür/zemin ayrışması 0,92.
  - Risografta bu değer 0,66–0,69 ve ilk odak kare kenarına gidiyor.
  - Risografın yakın plan başı kuş gibi okunuyor.
- **Hız:** 4 alt örnekli hareket bulanıklığıyla kare başına 0,35–0,50 sn; 4 işçiyle neredeyse doğrusal ölçekleniyor. Risograf 1,2–4,4 sn ve 4 işçide yalnız ~1,8 kat hızlanıyor.
- **Formül:** Sisifos'unkiyle aynı (vazo üslubunda mit, başlıkta bugüne sorulan soru). Prometheus da bu üslupla 2. gün kanalın en büyük göz atma testini aldı (17,6 B; `analiz/2026-11-17-kanal-ortalamasi.md`). Üslubun tıklamadaki payı ayrıca ölçülemiyor; ama yeni izleyiciyi geri çevirdiğine dair veri de yok.
- **Tazelik:** son dört video (Milton, İkaros, Kafka, Ran) baskı ve mürekkep dilindeydi, vazo ise 18 gündür kullanılmadı. Risograf beşinci baskı dili olurdu.
- **Kanal kuralı:** CLAUDE.md'nin sırasına uyuyor (önce kendi motorlarımız).

**Vazonun açıkları (kapıda çözülecek):**
- **Kaynak yok:** bilinen hiçbir Yunan vazosunda Narkissos tasvir edilmemiş; en eski kesin tasvirler Roma dönemine ait (Pompeii freskleri, gemmalar). Üslup serinin görsel kimliği olarak kullanılır; anlatıda "Narkissos'un antik tasviri" diye sunulmaz.
- **Yalnız profil var,** yani ¾ yüz kuralı karşılanmıyor. Kapakta karşılıklı profil denenir; alttaki yüz halkayla bozulur, böylece asimetri hem görsel hem hikâye taşır.
- **Baş:** denemedeki genç kel gibi okunuyor; yeni bir baş gerekir (saç, genç yüz).
- **Duruş:** geniş planda dört ayak üstünde eğilmek secde gibi okunuyor. Yerine uzanma ya da kayaya yaslanma kullanılır.
- **Denenmeyenler:** yansımanın seyreltik sırla koyulaşması ve siyah sırdan siyah cama geçiş henüz denenmedi.

**Neden rakip risograf, kazıma film değil:**
- Risograf açık zeminli, çağdaş bir dergi illüstrasyonu dili. Kapı gerçekten "koyu ve antik mi, açık ve çağdaş mı?" sorusunu sınar.
- Yansıma risografın gölgelendiricisinde hazır (`riso.js:50–68`). Eksik olanlar halka ve oval havuz maskesi.
- Yarım ton noktası ekran pikseline dönüşebilir; bu köprüyü yalnız risograf kurar.
- Kazıma film de koyu zeminli; vazoyla karşılaştırmak az şey öğretir. Onun fikirleri vazoya taşınır: kazınarak yazılan ve her tekrarda solan söz, bedeni sönen figür.

**Kapı kuralları (önceden yazıldı):**
- **Süre:** vazoya yarım gün, risografa en çok bir gün.
- **Sahne:**
  - manzara: pınar ve orman kenarı;
  - orta plan: giyinik genç uzanmış, suya bakıyor;
  - yakın plan: "öpüşme ekseni" (III 427), yüz ve yansıması çene çeneye.
- **15 sn'lik hareket:** gözyaşı (`Wd`) → halka → yansımanın toparlanması; "sum" sözcüğünde tanıma; su kenarının telefon kenarına dönmesi.
- **Ekler:** 0–5 sn'lik "cam → havuz" açılış denemesi ve 1280×720 kapak taslağı (süre rozeti bölgesi boş).
- **Risografın kazanma şartları:**
  1. yakın plan baş, planı görmemiş bir alt ajana "genç bir insan" diye okunuyor;
  2. 246, 168 ve 120 px'te, koyu ve açık akışta yüz ve yansıma vazodakinden iyi okunuyor (`odak.py`);
  3. 480p ve 360p kodlamada yarım ton titremiyor (hare deseni yok);
  4. hareket bulanıklığı açık, tek işçi ve boş makinede kare başına ≤ 1,5 sn.
- **İki adayda da:**
  - hassasiyet bakışı: hale, haç, secde, çıplaklık, altı köşeli yıldız;
  - sessiz okuma testi;
  - 15 sn'nin CRF 18 dosya boyu.

### Öteki adaylar
| Aday | Kaynak | Neden ana üslup değil |
|---|---|---|
| Kazıma film | Lemo `scratch-film` | En ucuz yeni motor (0,13–0,41 sn/kare); Eko ve nergis ortamın kendi hareketiyle çözülüyor. Ama koyu zemin ve ince çizgi telefonda zor okunur, koyu akışta kapak kenarı kayboluyor, arşiv belgesi bu dile girmiyor |
| Neon tüpler | Lemo `neon-tubes` | Kavrama en yakın üslup ("görünmek için yapılmış ışık") ve en iyi hazır yansıma. Ama GPU'da 3,5–5 sn/kare ve 4 işçi hızlandırmıyor (9 dk ≈ 17 saat render); 6–8 günlük iş; Türkçe tüp harfleri yok. 24–25 Kasım'a sığmaz |
| Roma mozaiği | yeni motor | En özgün fikir: taştan piksele; Hatay'daki Narkissos ve Eko mozaiği Türk izleyiciye kapı. Hazır motor yok, 5–7 gün |
| Tek çizgi | Lemo `one-line` | 8 dk'lık tek yol elle yazılmalı; 168 px'te soluk; "tek çizgi yüz" kendini sevme afişlerinin klişesi |
| GitHub | p5.brush, three-painterly, webgl-water, WebGL-Fluid | Tam motor yok: p5.brush'ın 1080p hızı ölçülmedi ve kapakta karşıtlığı düşük, webgl-water'ın lisans dosyası yok, WebGL-Fluid ağ çağrısı ve rastgelelik içeriyor |

Reddedilen ~35 üslubun gerekçeleri ham raporlarda. Başlıcaları:
- ink-wash, woodcut, silkscreen, engraving: son dört videonun tekrarı;
- crayon-book, paper-popup, silent-film, shadow-puppet: alay riski;
- manga-panels, comic-history: karakterleri yapay zekâyla üretilmiş;
- gilded-illumination, stained-glass, art-deco: hale ve dua kitabı çağrışımı.

### Üsluptan bağımsız alınacaklar
- **Analitik halka:** kapalı biçimli dalga, `Wd()` zamanına bağlanır, CPU'da etkin sınır kutusuyla çizilir. 4 işçide ölçüldü: medyan ~17 ms, kare özeti işçiler arasında aynı. Hazır kütüphaneler (jquery.ripples, WebGL-Fluid) rAF, `Date.now` ve `Math.random` ile sürüldüğü için doğrudan alınmaz.
- **flubber** (MIT): biçim dönüşümleri (beden → nergis, havuz kıyısı → telefon dikdörtgeni). Bağımlılıklarıyla birlikte `araclar/ASSETS.md`'ye yazılır.
- **Yansımanın fiziği:** yansıma, nesnenin suya uzaklığı kadar aşağıda görünür. "O benim" anı ve kapak yalnız yakın planda kurulur; geniş planda yansıma kadraj dışına düşer.
- **Ayrışan yansıma** (Milton P043): mitte yansıma birebir taklit eder, bugün bölümünde ayrışır (sunulan benlik).
- **Göz ↔ nergis:** Divan şiirinde nergis gözdür (ikincil kaynak; Pala'nın sözlüğü görülmedi). Beyaz taç yaprak göz akı, safran göbek iris olur; Ovidius III 509–510 ile örtüşür.

### Gerçek görsel araları (Ran yöntemi; lisanslar doğrulandı)
- **Met 401131:** Antonio Tempesta, *Narkissos pınar başında*, 1606 (CC0).
- **Met 419135:** Jacques Callot, *Lux Claustri* 22. levha (1621–35, CC0).
  - Levhanın başında "L'excez de l'Amour propre est cause de sa perte" yazıyor: "Öz-sevginin aşırılığı yıkımının sebebidir". Bu, Ellis'ten ~270 yıl önce (görselden okundu).
  - Kitap bir manastır amblem kitabı; levha yalnız resim ve bu satırla kırpılır. Diz üstü eğilen figür hassasiyet bakışından geçer.
- **Ellis 1898** (*Alienist and Neurologist* 19, archive.org `alienistneurolog1918unse`): yalnız "Narcissus-like" cümlesi kırpılır; makale başlığı gösterilmez.
- **Freud 1914** (*Jahrbuch* VI, archive.org `jb61914`, PD Mark): yalnız ilk sayfa.
- **Gösterilmeyenler:**
  - Caravaggio ve Pompeii fotoğrafları: İtalya'da D.Lgs. 42/2004 md. 108 kâr amaçlı kullanımı izne ve ücrete bağlıyor.
  - Hatay mozaiği fotoğrafları: CC BY-SA, ayrıca 2863 sayılı Kanun md. 34 gereği Bakanlık izni gerekiyor.
  - Waterhouse'un tablosunun bütünü.

### Kaynak notları (senaryoda doğrulanacak)
- Yaygın Türkçe anlatımlardaki "suya atlayıp boğuldu" Ovidius'ta yok; Narkissos erir (III 487–490).
- İngilizce Wikipedia'nın "Narcissism" maddesinde Ellis ve Näcke için "1889" yazıyor. Ellis'in makalesi 1898 Nisan sayısında (archive.org'dan doğrulandı); Näcke'nin tarihi kaynağından doğrulanacak.

## 6. Kullanıcının kararları (18 Kasım 2026)
- **Üslup:** öneri (a) onaylandı. Vazo ile risograf aynı sahneyle sınanır; §5'teki kapı kuralları geçerli.
- **Yorumun omurgası: "bilmek yetmiyor".** Narkissos yansımanın kendisi olduğunu anlar ("Iste ego sum", III 463) ve yine de ayrılamaz. Eko ve kavramın tarihi bu omurgaya bağlanır, ayrı tezler olarak durmaz.
- **Açılış:** film siyah telefon camında kendine bakan biriyle açılır, cam havuza döner (Fable 5.2'nin önerisi). İskelete ve üslup kapısına alınır.
- **CLAUDE.md "geniş kitle dersi":** değiştirilmez. Başkan Prometheus cümlesini 2. gün testine karşı okumuştu; kullanıcının kastettiği, 17 Kasım'da günlük gösterimin 1–2 B arasında gidip geldiğiydi (dalga sürmedi).

## 7. İskelet (18 Kasım 2026; senaryodan önce)
**Seçim: Kişōtenketsu** (giriş → gelişme → dönüş → birleştirme). Her bölümde ABT denetimi yapılır (Ve… Ama… Bu yüzden…).

**Gerekçe:**
- Omurga ("bilmek yetmiyor") tek bir dönüşe dayanıyor: herkes Narkissos'un yansımanın kendisi olduğunu bilmediğini sanır, oysa o anlar ve yine de ayrılamaz (III 463–467). Kişōtenketsu'nun "ten"i tam olarak bu: beklenmedik bilgi ya da bakış.
- Mit çatışmasız değil (Juno, Eko'nun reddi, Nemesis'in laneti), ama kahramanın asıl sınavı bir rakip değil, kendi bilgisi. Harmon çemberinin "ihtiyaç" ve "dönüş" adımları zorlanırdı.
- **Önceki iskeletler:** Ran = Harmon çemberi, Kafka = Kişōtenketsu, İkaros = Harmon (sonradan). Art arda aynı iskelet gelmiyor. Kafka'dan farklı süs: çerçeve hikâye (bugünün genci) ve dönüşün kaynakta satır numarasıyla duruyor olması.

**Kahraman:** Narkissos. Çerçevede bugünün genci (izleyicinin yerine geçen, telefon camına bakan kişi) soruyu taşır. Kurye fikriyle örtüşür: izleyici geçmişe gider, bir soruyla döner. Eko karşı kutuptur: yalnız başkasının sözüyle var olur. Narkissos yalnız kendini görür, Eko yalnız başkasını duyar.

**Tek cümlelik vaat:** "Narkissos sonunda baktığı yüzün kendisi olduğunu anladı; o hâlde kendini sevmek ne zaman insanı bırakmayan bir şeye döner?"

**Kanca kuralları:** İkaros ve Kafka dersleri (kancanın arkasına bilinen bağlam ya da alıntı konmaz); Ran kuralı (hikâye en geç ~0:45'te başlar).

| Adım | İçerik | Kaynak | Taslak cümle aralığı* |
|---|---|---|---|
| **0. Kanca** (0–20 sn) | Siyah telefon camında kendine bakan genç; cam havuza döner. İlk cümlede soru: herkesin bildiği hikâyenin unutulan yanı, "sonunda anladı", ve "o hâlde neden kalkıp gitmedi?" (Baştan beri biliyordu denmez: 425 ve 430'da bilmiyor, 463'te anlıyor) Başlığın sorusu ("kendini sevmek ne zaman…") burada sorulur, cevabı sona saklanır | III 463 (yalnız ima) | A01–A04 |
| **Ki (giriş)** (~0:20–1:30) | Hikâye hemen başlar. Nehir perisi Liriope'nin oğlu doğar. Kehanet: "kendini tanımazsa" uzun yaşar. Merak döngüsü: kendini tanımak nasıl ölüm olur? Ama: on altı yaşında (351: 3×5+1) herkes onu ister, kimse ona dokunamaz (355) | III 344–355 (348) | B01–B08 |
| **Shō (gelişme)** (~1:30–3:30) | Eko: Juno'nun cezası, yalnız son sözleri tekrarlamak. Ormanda karşılaşma, yankı diyaloğu. Ret: "bana sahip olmana izin vermektense ölürüm" / Eko: "bana sahip ol" (*copia*, 391–392). Eko'nun bedeni erir, sesi kalır. Reddedilen, adı verilmemiş biri beddua eder; Rhamnusia (Nemesis'in yer adıyla anılan sıfatı) kabul eder (406). Havuz: dokunulmamış su, susuzluk, âşık oluş, yanılsama. Anlatıcı Ovidius'un ona seslenişini taşır ("saf çocuk", 432) | III 356–436 | C01–C14, D01–D10 |
| **Ten (dönüş)** (~3:30–5:00) | **"Iste ego sum: o benim, anladım; hayalim beni kandırmıyor"** (463). Bilmek yetmiyor: "sahip olduğum şey beni yoksul kıldı" (466, *copia* Eko'ya söylediği sözle döner); "keşke bedenimden ayrılabilsem" (467). Gözyaşı suyu bulandırır, hayal kaçar: "kalsın, hiç değilse bakayım" (474–479). Narkissos'un son sözü bir elvedadır, onu geri veren Eko'dur (501); Eko ağıtlara da yankıyla katılır (507). Erir; boğulmaz (487–490). Yerinde safran göbekli, ak yapraklı çiçek (509–510); Styks'te bile kendine bakar (504–505) | III 463–510 | E01–E14 |
| **Ketsu (birleştirme)** (~5:00–7:00) | Mit çiçeği ona bağlar (Ovidius çiçeğe ad vermez; "mit böyle anlatır" diye çerçevelenir), sonra bir davranışa ad olur. Ad zinciri: Callot'un gravürüyle 1646'da basılan bir manastır kitabında "öz-sevginin aşırılığı yıkımının sebebidir" (yazı Callot'un değil, baskının) → Ellis 1898 "Narcissus-like tendency" → Näcke 1899, Ellis'i anarak "Narcismus" → Freud 1914 (terimi Näcke'ye verir, 1920'de Ellis'e düzeltir). **Başlığın cevabı** Freud'dan (doğrulandı, `kaynak/DOGRULAMA.md`): her insanın birincil bir narsisizmi vardır (s.13), yani kendini sevmek gelişimin olağan, erken bir parçasıdır ("ilk evre" denmez, s.4). Sorun öz-sevginin varlığı değil, libidonun dünyadan çekilip ego'da birikmesidir (s.2, 10–11): "sonunda sevmeye başlamak gerekir, hastalanmamak için" (s.11). Seven kişi narsisizminden bir parça verir ve onu ancak sevilerek geri alır (s.21). Freud Narkissos mitini anmaz: mitle bağ anlatıcının yorumudur, Freud'a mal edilmez. Bu, Eko'yu duyamayan Narkissos'tur. Teşhis yok, tavsiye yok. Su → ekran: genç yine camda. Son soru izleyiciye: "Biliyorsun. Peki yetiyor mu?" Abone çağrısı bu son anın içinde, ardından yorum uzatılmaz | Freud 1914; Ellis 1898; Met 419135 | F01–F12 |

\* **Bu tablodaki aralıklar rev0'a aittir; geçerli eşleme §10'da.** Cümle kimlikleri bölüm harfi + sıra. Senaryo kesinleşince bu tablo gerçek numaralarla güncellenir (Kafka'daki numara kayması dersi). Çıkarılan cümlenin numarası boş bırakılır.

**Açık merak döngüleri (soru → cevap):**
1. "Sonunda anladı; o hâlde neden gitmedi?" (A) → E (463–467): bilmek sevgiyi geri döndürmeye yetmedi.
2. "Kendini tanımak nasıl ölüm olur?" (Tiresias, B) → E: tanıdığı an sonun başladığı an.
3. "Narkissos'un Eko'ya söylediği söz" (C, *copia*) → E (466): Ovidius aynı kelimeyi kullanır (391'de "sahip olma", 466'da "bolluk"); "söz ona döner" anlatıcının okumasıdır, "Ovidius bilerek yaptı" denmez.
4. Başlığın sorusu (A) → F (Freud): cevap tavsiye değil, kavramın kendi tanımı.
5. Çerçeve: camdaki genç (A) → F: aynı camda, aynı soru.

**Kapakla uyum:** Kapak A ("O BENİM", yüz ve yansıması) filmin ilk 5 saniyesinde camdaki yüzle karşılanır; açılış görüntüsü kapak kompozisyonuyla aynı eksende kurulur. Kapak B (Narkissos ve Eko karşıtlığı) C bölümünün görüntüsüyle karşılanır.

**Başlık notu:** ön seçim 1. aday ("Kendini Sevmek Ne Zaman Narsisizme Döner?") korunur; cevabı F'de Freud'dan gelir. Omurga "bilmek yetmiyor" olduğu için 2. aday ("Bildiğin Hâlde Bırakamıyor musun?") Test ve karşılaştır'da ikinci vaat olarak değerlendirilir. Karar senaryodan sonra.

**Kaynak denetimi yapıldı (18 Kasım):** `kaynak/DOGRULAMA.md`. Yukarıdaki satırlar buna göre düzeltildi. Ek uyarılar: Ellis'in kırpması "This Narcissus-like tendency … self-admiration" ile sınırlı kalır (cinsiyetçi "kadınlarda ayna" çerçevesi ekrana taşınmaz); Näcke'nin tanımı anlatılmaz, yalnız adın doğuşu söylenir; DSM üçlüsü yalnız ikincil kaynak olarak ve teşhis dili olmadan; susuzluk imgesi 413–416'ya dayandırılır (Magnus 415 ve 417'yi sahte sayar); 399'daki taşa dönüş "derler" diye aktarılır.

**Doğrulanacaklar listesi (tamamlandı):**
- Ovidius satırları: 344–355, 391–392, 432, 463–467, 474–479, 487–490, 501, 504–505, 509–510.
- Freud 1914'te birincil ve ikincil narsisizm ayrımı (Almanca metinden).
- Ellis 1898 cümlesi.
- Näcke 1899'un künyesi.
- Callot levhasının tarihi.

**Ek karar (kullanıcı, 18 Kasım):** üslup kapısının sonucunda kararı Fable 5.2 verir; kullanıcıya sorulmaz. Başkan Fable'ın kararını uygular. Yalnız kaynak ya da hassasiyet engelleyici bulgusu varsa (veto kuralı) kararı kayda gerekçesiyle yazıp düzeltir.

## 8. Üslup kapısı sonucu (18 Kasım 2026): VAZO (Fable 5.2'nin kararı, şartlı)
Ayrıntı: `kapi/FABLE_KAPI.md`. Kodlar `kapi/vazo/`, `kapi/riso/`; kareler ve mp4'ler oturumun çalışma alanında.

| Ölçüt | Sonuç |
|---|---|
| 1. Yakın plan baş "genç insan" okunuyor | Risograf net önde ("erkek, 18–25"). Vazo genç okunuyor ama "üstü çıplak kadın" okumasına kayıyor |
| 2. 246/168/120 px | Karışık. D planında yansıma risografta daha görünür, koyu akışta kenarı duruyor. Kapakta vazo önde (tek odak yansıyan gözde, yazı karşıtlığı yüksek) |
| 3. 480p/360p | İkisi de hare ve titreme göstermiyor. Ama YouTube bit hızında risograf 1080p PSNR 26,8 dB, vazo 49,2 dB |
| 4. Kare süresi (mb=4, tek işçi) | Risograf 0,82 sn ortalama, geçiyor. 4 işçide 9 dk: vazo ≈ 1,26 sa, risograf ≈ 2,02 sa |
| Ek: dosya boyu | 19,5 sn CRF 18: vazo 10,6 MB, risograf 102 MB (9,6 kat) |
| Ek: açılış | Vazoda telefon 0,3. saniyede telefon okunuyor; risografta akvaryum, lavabo, pencere okundu |
| Hassasiyet | Engelleyici bulgu yok. Düzeltilecekler: vazo D planında çıplak okunan beden, E'de hale okunan elips, burundan sarkan çizgi; risografta dudak teması ve kapak "O BENİM" birlikte aşk vaadi gibi okunuyor |

**Karar:** kapı kuralı gereği vazo; risograf dört ölçütün dördünde açık fark yapmadı. **Şart:** Fable'ın on düzeltmesi yapılır, sonra D_benim ve C planı görmemiş okura yeniden sorulur. Okuma yine "çıplak kadın" ya da "secde" çıkarsa kapı yeniden açılır. Risograftan alınacaklar:
- kısa saçlı, kulağı açık efeb başı;
- halkada yansımanın koyu lekeye dağılması (120 px'te görünür);
- kıyı çizgisi ve kesik su ufku;
- kıyıdaki nergisler;
- "yabancı yansıma" fikri;
- suya yansımayan kapak yazısı.

**Başkanın notu:** §5'teki "vazo 0,35–0,50 sn/kare" prototipe aitti; kapı sahnesinde vazo mb=4 ile ortalama 1,0 sn (p90 1,82). Render planı 4 işçiyle ölçülen değere (9 dk ≈ 1,3 saat) göre yapılır.

## 9. Senaryo denetimi ve rev1 (18 Kasım 2026)
Dört bağımsız mercek: kaynak (8/10), hassasiyet (7,5), Türkçe seslendirme (7) ve Fable 5.2 dramaturji (7). "Engelleyici" ve "düzeltilmeli" bulguların her birini ikinci bir ajan çürütmeye çalıştı. rev1 süzgeçten geçen bulgularla yazıldı: 63 cümle, 893 kelime (rev0: 70 cümle). Kimlikler yeniden numaralandı; plan listesi rev1'e göre yazılacak (Kafka numara kayması dersi).

**Uygulananlar:**
- **Kanca:** A01 soru oldu ("Bugün bir camda kendine kaç kez baktın?"). Kapak sözü "O benim" ilk 15 saniyede duyuluyor (A03). Liriope adı ve Jüpiter anlatımdan çıktı (ad yükü). "Herkes bilir" tekrarı kalktı.
- **Yankı Türkçede yankı oldu:** "Kim var burada?" / "Burada!". Copia cümlesinde yankılanan kısım sonda: "Önce ölürüm, sonra bana sahip olursun." / "Bana sahip olursun." (III 391–392). E08'de söz kendiliğinden dönüyor; filoloji notu ekran yazısına gitti.
- **Hitap:** baştan sona "sen".
- **Merak döngüleri:**
  - L2 (kehanet) E10'da anlatımda kapanıyor;
  - D07'ye bölümün küçük sorusu eklendi ("Bilse, kalkıp gider miydi?");
  - F01'e bölümün sorusu eklendi;
  - L1'in "neden"i F09'da veriliyor (Eko'nun sesi hep yakınındaydı, o başını sudan kaldıramadı).
- **Kaynak düzeltmeleri:**
  - D05 çeviri hatası ("seven de o, sevilen de");
  - E06 "kendime duyduğum aşk";
  - D01 "ağaçtan düşen dal";
  - D02–D03 notları (415 ve 417'yi Magnus sahte sayar, TLL ve Loeb tutar);
  - F02 simge cümlesi (Alciato 1550 notu);
  - F06–F08 Freud: "birincil", "sorun ne zaman" çerçevesi, alıntı koşuluyla birlikte ("engellendiği için sevemeyen").
- **Ad bölümü** (Callot, Ellis, Näcke) tek hamlede ve bir soruyla. Teşhis çekincesi kelimenin doğduğu yere (F04) taşındı; doruğun ortasından çıktı.
- **Son:**
  - F10: Ovidius'a yalnız bir dönüş ("Narkissos'u bitiren yalnız kendini sevmesi değildi"; III 354'teki gurur yok sayılmıyor).
  - F11: neyin bilindiği adlandırıldı.
  - F12: Camus atfı soruya döndü ("Peki Sisifos'a yetti mi?"); doğrulanmamış "özgürleştirdi" kalktı.
- **Seslendirme:** tts'de adlar ve yıllar okunuşla yazıldı (Froyd, Hevlok Elis, Nekke, Stiks, Narkissus, yıllar yazıyla). Altyazıda doğru yazım.

**Reddedilenler (gerekçesiyle):**
- **A01'i çoğul yapmak** ("kendimize bakıyoruz"; hassasiyet): süzgeç reddetti. Soru biçimi suçlama tonunu zaten kaldırıyor; tekil hitap çerçevenin kendisi.
- **A05'e baştan teşhis uyarısı:** reddedildi. Kancayı keser; uyarı F04'te anlatımda, açıklamada ve sabit yorumda var.
- **E04'ü "Bu benim, ta kendim!" yapmak** (ses): reddedildi. Kapak sözü "O BENİM" ile birebir aynı kalmalı; "iste" yakını işaret etse de Türkçede "o benim" doğal.
- **D02–D03'ü "katı yol"la değiştirmek:** reddedildi. TLL ve Loeb iki dizeyi de tutuyor; not doğru yazıldı.
- **Başlığı değiştirmek** (hassasiyet "vaat" bulgusu): süzgeç reddetti. Cevap F06–F07'de sorunun kendi kelimeleriyle veriliyor ("ne zaman soruna döner").

**Başlık:** 1. aday kalır ("Kendini Sevmek Ne Zaman Narsisizme Döner? | Narkissos'un Hikâyesi"). Test ve karşılaştır'da ikinci vaat 2. aday değil, **4. aday** ("Kendine Bakmaktan Vazgeçebilir misin? | Narsisizm ve Narkissos"); senaryonun son sorusuyla aynı. Bunu Fable önerdi, başkan kabul etti. 2. aday bağlamsız okununca bağımlılık vaadi gibi duruyor.
**Kapak B yazısı:** "BİLİYORDU" kullanılmaz (425, 430'da bilmiyor). 4–6 kelimelik deneme: "ANLADI. YİNE DE KALKAMADI."

## 10. Senaryo rev2: gerileme kontrolü ve onay (18 Kasım 2026)
- **Kaynak (veto):** 9/10, şartlı onay; engelleyici bulgu yok. **Fable 5.2:** 8,5/10, şartlı; "üç düzeltme uygulanırsa 9, yeni tur gerekmez".
- Uygulananlar:
  - C07/E08: "Ancak ben ölünce bana sahip olursun." Ret kesinleşti, yankı yine son sözlerde.
  - F09: "O ise gözünü sudan ayıramadı." 440–441'de başını kaldırıp ormana seslendiği için "başını kaldıramadı" kaynakla çelişiyordu; "hep yakınındaydı" da kalktı.
  - E09: 468, Narkissos'un kendi sözü olarak tırnak içinde.
  - C02: ceza nedeni "kandırdığı için" (366).
  - B01, B03, B04: kaynağa yakın.
  - F02–F05 (Fable D1): ahlak dersi → tıbbın konusu → Freud dönüşü açık kuruldu. Ellis ve Näcke'nin adları sesten ekran künyesine indi (Medici ad yükü dersi).
  - F11 (D2): "Peki bilmek, gözünü ayırmaya yeter mi?" Somut soru F09'a ve 4. başlık adayına bağlanıyor.
  - A03 (D3): "anladı"nın nesnesi eklendi.
  - Fable'ın önerileri: "ne demişti" kalıbının üçlenmesi kırıldı (E10 "Kâhinin şartını hatırla"); E05'te "bilmek" sözü E10'a saklandı; C09 "Sahibine geri dönecek"; F09 "Freud miti anmaz; bağı biz kuralım"; D01 listesi kısaldı.
- **Başkanın kararı:** senaryo rev2 **ONAY**. Kaynak 9 ve Fable'ın şartları karşılandı. Kalan tek açık kulak sorusu: C07'nin red olarak duyulması. Seslendirmeden sonra kullanıcının kulağına bırakılır.
- **Reddedilen:** Fable O5 ("Cevabını yorumlara yaz" sesten çıksın). Kanalın amacı etkileşim (CLAUDE.md "kanal yönü"); soru somutlaştığı için seste kalıyor.

**İskelet → rev2 cümle eşlemesi** (63 cümle, 896 kelime, tahmini ~7:40–8:30):

| Adım | Cümleler |
|---|---|
| 0. Kanca | A01–A05 |
| Ki (giriş) | B01–B06 |
| Shō (gelişme) | C01–C12 (Eko), D01–D11 (havuz) |
| Ten (dönüş) | E01–E17 |
| Ketsu (birleştirme) | F01–F12 |

| Döngü | Açılış → kapanış |
|---|---|
| L1 | A04 → E05 → F09–F10 |
| L2 | B02–B03 → E10 |
| L3 | C08–C09 → E07–E08 |
| L4 (başlık) | A05 → F07–F08 |
| Çerçeve | A01 → F11 |
| Bölüm soruları | D07, F01 |

**Sıradaki:**
1. Seslendirme için kredi hesabı (karakter × çekim) kullanıcıya bildirilir ve açık onay alınır.
2. Plan listesi rev2'ye göre yazılır.
