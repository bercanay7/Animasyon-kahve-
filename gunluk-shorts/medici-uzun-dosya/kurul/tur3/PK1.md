# PK1 — TUR 3 · Paket: kapak/başlık, tıklama vaadi · Medici Parça 1 (v3)

**Sınır:** videoyu oynatamadım, sesi dinleyemedim.

**Neye baktım (v3, `out_p1/medici_P1.mp4`, 601,54 sn, 14.437 kare):**
- ffmpeg ile kare çıkardım:
  - 0–4,2 sn, 0,25 sn adımla (kapak yankısı);
  - 588–601,5 sn, 0,5 sn adımla ve 591–594 sn, 1/12 sn adımla (bitiş ekranı);
  - bölüm çapaları: 101,5 · 181,5 · 214,8 · 278,2 · 341,5 · 413,2 · 432,0 · 487,0 sn;
  - vaat ödemeleri: 68,3 · 339,5 · 346 · 390,2 · 394,5 sn;
  - tur 2'de "ucuz" dediğim yerler: 40 · 46 · 371,5 · 476,5 · 481 · 495 · 498,5 · 556 · 562 sn.
- Kapaklar `kapak_P1_K1/K2.jpg` (5 Kasım 07:07): kendi ölçümüm + `out_p1/kapak/kapak_qa_P1.png/.json`.
- Paket `studio_paketi_P1/00–05`, `yayin/bolumler_P1.txt`, `yayin/YAYIN_TASLAK.md`, `kurul/sonraki_parcalar_notlari.md`, `paket_P1.py`, `kapak_qa.py`.
- `kurul/KURUL.md` (tur 2 sonucu ve v3 planı), `kurul/tur3/KA2.md` (T3 görüşü).

Kanıt dosyaları `/tmp/claude-0/-home-user/ad251a99-58f4-5d1d-a24b-a2064ec20b78/scratchpad/pk1t3/` içinde:
- `yanki_v3.png`, `bitis_ekrani_v3.png`, `bitis_597.png`;
- `glints_v3.png`, `qa_feed.jpg`;
- `bolum_capalari_v3.png`, `vaat_odeme_v3.png`, `ucuz_kontrol_v3.png`.

**Kural notu (açıkça):** denetim için `python3 paket_P1.py` çalıştırdım. Betik paket dosyalarını yeniden yazdı:
- yazılan dosyalar: `studio_paketi_P1/00–05` ve `yayin/bolumler_P1.txt`;
- içerik aynı kaldı: betik 11:44:06'dan beri değişmedi; girdiler de değişmedi (`timeline.json` 4 Kasım 22:13, mp4 08:48); betik zamana ya da rastgele sayıya bağlı değil; dosya boyutları birebir aynı;
- değişen yalnız dosya tarihleri (11:44 → 11:49).

"Diğer dosyalara dokunma" kuralına aykırıydı; başkana bildiriyorum. SHA-256 ilk 16 hane, karşılaştırma için:

| Dosya | SHA-256 (ilk 16 hane) |
|---|---|
| `00_yayin_adimlari.txt` | ba8d0f187df1bc08 |
| `02_aciklama.txt` | cc3c7b46d58702aa |
| `03_sabit_yorum.txt` | 2b54f4c397b4370a |
| `05_bolumler.txt` ve `bolumler_P1.txt` | 142585e62f718dfb |

---

## 1. Karar

**ONAY — 9,5 / 10.** Tur 2'deki iki koşulum (Y1, Y2) ve Y3–Y6, Y8 kapandı. Y7 kısmen kapandı: kod doğru, ama QA görseli eski. Yeni bulgular küçük; hiçbiri engelleyici değil.

| Parça | Tur 2 | Tur 3 | Not |
|---|---:|---:|---|
| Kapak K1 | 9,5 | **9,5** | Zemin açıldı, ışın yok, tek odak; ölçüler korundu |
| Kapak K2 | 9,0 | **9,5** | Arma 8 top (videoyla tutarlı); ışın yok; odak payı %78 → %88 |
| Başlık T1 | 9,0 | **9,0** | Değişmedi |
| Açıklama | 8,0 | **9,5** | İlk damga 0:00; yöntem cümlesi dürüst ("bütün figürler temsilîdir") |
| Bölümler | 9,0 | **9,5** | v3'te yeniden doğruladım |
| Sabit yorum | 9,5 | **9,5** | — |
| Etiketler | 9,0 | **9,0** | — |
| Yayın adımları + test planı | 7,0 | **9,5** | `00_yayin_adimlari.txt` eksiksiz; tek artık YAYIN_TASLAK §6 m. 8 (G2) |

---

## 2. Tur 2 maddelerimin durumu

| Madde | Durum | Kanıt |
|---|---|---|
| **Y1 (koşul)** açıklamada listeden önce "5:39" | **KAPANDI** | Açıklamadaki ilk damga "0:00", 1291. karakterde (9 damganın ilki). 2. satır artık damgasız: "…faiz yasağı ve 'vicdan komitesi' de bu parçada." `paket_P1.py` 240–245. satırlar ilk damga 0:00 değilse hata veriyor. `00_yayin_adimlari.txt` "başka zaman damgası EKLEME" diye uyarıyor ve yayından sonra 9 bölümün çubukta görünmesini kontrol ettiriyor |
| **Y2 (koşul)** eski yayın belgeleri | **KAPANDI (P1 için)** | YAYIN_TASLAK'ta P1 başlık satırı T1; T2/T3 yedek olarak duruyor. §3 P1 bloğu artık yalnız "geçerli metin: `studio_paketi_P1/02_aciklama.txt`" diyor; eski iki vaat hatası kalktı. P2'nin "Önceki" satırı yeni başlıkla. §6 m. 1: "K1 varsayılan + K2 test, ESKI yüklenmez". §6 m. 4: "paket üreticisinden, P1'de 9". §7: "● 51". `bolumler_P1.txt` = `05_bolumler.txt` (aynı özet). Tek artık §6 m. 8 (G2); P1'i etkilemiyor |
| **Y3** tek sayfalık yayın adımları | **KAPANDI (biri değiştirilerek)** | `00_yayin_adimlari.txt` şunları yazıyor: varsayılan K1 ve ilk yüklenen; yankı açıklaması; Test ve Karşılaştır (başlık sabit, 14 gün, sonuçsuzsa K1); özellik yoksa 72 saat + gösterim başına izlenme süresi; K2 kazanırsa açılış kırpılmaz; bitiş ekranı 9:52; sabit yorum; T2/T3 (T3 yalnız kaynak üyesi onayıyla) |
| ↳ Y3 bitiş ekranı sol öğesi | **DEĞİŞTİRİLDİ (başkan, PK2-Y2) — katılıyorum** | Önerdiğim "oynatma listesi" P1 yayınlandığında yalnız P1'i içerir ve izleyiciyi aynı videoya döndürür; PK2 haklı. Yeni öğe "İzleyiciye en uygun video", P2 çıkınca P2 |
| ↳ Y3 "9:52" iddiası | **DOĞRULANDI** | Çıkış 591,9 sn'de başlıyor; çerçeveler 592,0'da giriyor, ≈592,9'da tam (`bitis_ekrani_v3.png`). 9:52 → sona 9,5 sn: YouTube'un 5–20 sn aralığında |
| **Y4** koyu temada kenar | **KAPANDI** | QA: K1 kenar 38,4 / koyu pay %8,5; K2 37,9 / %10,6. Kendi ölçümüm 37,9 / 37,6, ortalamalar 68 / 60 (tur 2'de 54 / 46). Hero kontrastı 10,1:1 ve 10,4:1 (≥ 7; tur 2'de öngördüğüm ≈ 9,8). `kapak_qa.py` test 6 eşikleri: kenar ≥ 35, pay ≤ %35 |
| **Y5** parıltı yıldızları | **KAPANDI (kapak + video)** | `glints_v3.png`: kilitte ve kese ağzında ışınsız yumuşak parlama. Kapak yankısında 0,5–3,0 sn ışın yok; 3,25 sn'deki ışık geçişi yıldızsız (`yanki_v3.png`) |
| **Y6** K2 arması | **KAPANDI** | Kesede 8 top, halka dizilişte; videodaki 1397–1429 bölüm kartıyla aynı (341,5 sn) |
| **Y7** maket süresi | **KISMEN** | `kapak_qa.py` 175–180. satırlarda süreyi ffprobe ile dosyadan alıyor (kod doğru). Ama QA görseli 07:07'de, v3 videosu 08:48'de üretildi; akış maketi hâlâ **9:58** gösteriyor, v3 **10:01**. Bkz. G1 |
| **Y8** seri öneki / NEDEN | **KAPANDI** | `kurul/sonraki_parcalar_notlari.md` ("Seri başlık öneki (PK1-Y8)") + YAYIN_TASLAK §2 notu |
| İsteğe bağlı K3 (silüetli kapak) | **AÇIK (isteğe bağlı, puanlanmadı)** | Ancak 48. saatte TO %2'nin altında kalırsa |
| Tur 2 bölüm 4 önerileri (kullanıcı sorusu) | **ÇOĞU KAPANDI** | Ayrıntı bölüm 4'te. Kalan: 0:33–0:58 sözleşme sayfası |

**Değişmeyen ama yeniden sınadığım yerler (gerileme yok):**
- *Bölüm çapaları (`bolum_capalari_v3.png`):* anlatım zaman çizelgesi değişmemiş (toplam 590,23 sn, cümle başları aynı); video yalnız 10 sn'lik çıkış kadar uzadı. Damgalar v3'te doğru içeriğe düşüyor: 1:41 florin "1252" · 3:01 VEBA çipi · 3:34 "1378" alayı · 4:37 "MEDİCİ'NİN BU KOLU" · 5:41 "BÖLÜM II DEFTERİN SİHRİ" · 6:53 DEBITORI/CREDITORI · 7:12 GİOVANNİ (Cossa) · 8:07 "CATASTO · 1427".
- *Vaat ödemeleri (`vaat_odeme_v3.png`):* K1 0:00–0:03,25 yankı + 1:08 haritada aynı kilit. K2 5:39 "FAİZ GÜNAHTIR" → 5:46 "KİLİSE: FAİZ = TEFECİLİK" → 6:30 kese + "FAİZ ✗" → 6:34 "MÜŞTERİ: KİLİSE".
- *Kapak ölçüleri:* "MEDİCİ" büyük harfi 132 px (%18,3), "FAİZ" 160 px (%22,2); süre rozeti ve fare simgesi bölgeleri temiz (QA "ihlal 0"); boyutlar 0,27 / 0,23 MB, sRGB.
- *Metin paketi:* başlık 56 karakter, açıklama 3.473, sabit yorum 451, etiketler 311.
- *Altyazı:* `studio_paketi_P1` kopyası kök dizindekiyle birebir aynı (SRT ve VTT).
- *Açıklama ekleri* (KA2-D14 TEMSİLÎ cümlesi, Machiavelli/Cavalcanti çeviri-özet notu) ilk iki satıra dokunmuyor; vaadi değiştirmiyor.

---

## 3. Gerilemeler ve yeni sorunlar

**G1 — [KÜÇÜK; saniyeler, render yok] QA görseli v3'ten önce üretilmiş.**
- `kapak_qa_P1.png` akış maketi Medici süresini "9:58" gösteriyor; v3 10:01.
- Ne yapılmalı: `python3 kapak_qa.py --part 1` yeniden çalıştırılsın. Kapaklar değişmediği için başka bir sonuç değişmez.

**G2 — [KÜÇÜK; P2'den önce] `YAYIN_TASLAK.md` §6 madde 8 eski talimatı taşıyor.**
- Satır: "Bitiş ekranı (son 7 sn): … sonraki parça yayınlanana dek **Oynatma listesi: Medici (7 parça)**".
- Bu hem 10 sn'lik yeni çıkışla hem de başkanın PK2-Y2 kararıyla ("İzleyiciye en uygun video") çelişiyor.
- P1'i etkilemez: YAYIN_TASLAK P1 için `00_yayin_adimlari.txt`'ye yönlendiriyor. Ama P2–P6 şablonuna yanlış talimat geçer: P2 çıktığında oynatma listesi P1 ile başlar ve izleyiciyi geriye gönderir.
- Ne yapılmalı: "son 10 sn (P1'de 9:52'den); sol yuva: sonraki parça yayınlanana dek 'İzleyiciye en uygun video', yayınlanınca o parça".

**G3 — [BİLGİ; eylem yok] İlk hafta bitiş ekranı vaadi ile öğe farklı.**
- Çizili yuvanın altında "SIRADAKİ PARÇA · 2/7 · COSIMO: SÜRGÜN VE DÖNÜŞ" yazıyor (597 sn, x 330–850, y 610–1010). P2 yayınlanana dek o yuvaya YouTube başka bir kanal videosu koyacak.
- KA2-N5 ile aynı görüşteyim: kabul. Videonun ömür boyu izlenmelerinin çoğu P2'den sonra gelecek (Sisifos'ta dalgalar 5.–8. günde geldi).
- `00_yayin_adimlari.txt` P2 günü değiştirmeyi zaten yazıyor; ek bir şey gerekmiyor.

Kapak, başlık, açılış uyumu ve paket metninde başka gerileme bulmadım.

---

## 4. Kullanıcının sorusu: "Bu çizim tarzı ucuz mu, yapay zekâ gibi mi?"

**Kısmen değişti, iyi yönde.** Tur 2'de "slayt şablonu" dediğim yerlerin çoğu düzeldi:
- c2'deki tek ikonlu kartlar masa defteri dünyasına taşındı: 7:56–8:01'de kasa memurluğu defteri, yanında anahtar, mum ve florin yığını; 8:15'te catasto defteri.
- Cavalcanti sayfasında artık gerçek İtalyanca satırlar ve yazılmakta olan Türkçe el yazısı var (9:22).
- Damgalar kâğıt fişin üstünde.
- Kapakta ve yankıda yıldız ışınları kalktı.

Kalan tek dikkat çekici yer videonun en çok izlenen dakikasında: 0:33–0:58'deki sözleşme sayfası hâlâ kıvrımlı sahte yazıyla dolu (0:40, 0:46). P1 için zorunlu değil. Ama c0 yeniden render edilirse ilk iş bu olmalı: sözleşmenin Fransızca III. maddesinden düşük kontrastlı gerçek satırlar.

Yapay zekâ izlenimi yok; bu yargım değişmedi.

---

## 5. En emin olmadığım nokta

1. **Bitiş ekranı öğelerinin çerçeveye oturması.** Videoya çizilen çerçeveler 1080p'de 520×290 px, yani genişliğin %27'si. Studio'nun video öğesinin bu boyuta küçültülüp küçültülemediğini buradan sınayamam. Küçülmezse öğe çerçeveden taşar; görsel bir kusur olur, işlevsel değil. Yayın günü bir bakış yeter.
2. **Açılan zeminin TO'ya etkisi.** Kanalın açık zeminli kapakları daha iyi tıklandı, ama nedensel değil. Kapak testinin sonucu bunu kısmen gösterecek.
3. **T3'ün onayı.** KA2 onayladı, KA1'in onayı bekleniyor. `00_yayin_adimlari.txt` bunu doğru biçimde koşula bağlıyor.
