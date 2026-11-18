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

## 5. Üslup
(araştırma sürüyor; sonuçlar buraya)
