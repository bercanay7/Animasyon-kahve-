# ROUND 2: Olgu denetçisi (tarih) (olgu)

**Read:** ROUND1-TALLY.md, every ADDENDUM-01*, and all Round 1 reports.

**Vote:** C
**Changed from round 1:** yes: VERIFICATION.md V4/V5/V10 (Emu), V16 (Titanik), V28/V30 (Dans) ve ADDENDUM-01A madde 6, 7, 8. Tur 1'de "dört videonun ikisinden fazlasında maddi hata çıkarsa haftada 4-5 veya kapıyı geçmeyen günü atlama zorunlu" demiştim. Doğrulayıcı üç videoda (Emu, Titanik, Dans) yanıltıcı ifade buldu; Zanzibar temiz. Eşik aşıldı.
**Confidence:** medium

## 1. Vote and reason

Kaynak kapısı, tally'deki B ile C arasında asıl ayrım noktasıdır. Dört videonun hiçbiri kapıdan geçmedi ve üçü niteleme gerektiren iddia taşıyor. Bu, "günlük yayın + kapı" kombinasyonunun bugüne kadar denenmediği, kapısız günlük yayının ise 3/4 oranında hata ürettiği anlamına gelir. Bu yüzden kapının aşınmasına karşı sigorta isteyen C'yi seçiyorum: haftada 5 yayın, 3 günlük tampon, ≥5 önceden doğrulanmış konuluk havuz.

Tur 2 soruları (G) için kuralım:
- **Q4 kapılar:** Kaynak kapısı yayını bloklar, öneri değildir. Her sayı/yıl/isim için 1 birincil ya da 2 bağımsız kaynak (qc'nin formülü). Tek tarafın öz-bildirimi ("rapora göre") nitelenir ve sesle söylenir. Bütçe 15-20 dk/video; ortalama 20 dk'yı aşarsa yayın 3-4/haftaya iner. Kaynak dosyası (`kaynaklar/YYYY-MM-DD.md`) yoksa `qa.py` çıkış kodu ≠ 0 olsun.
- **Q6 kanca:** Kanca cümlesi kaynak tablosunun 1. satırıdır. Kancadaki her sayı videoda gösterilir. Kaynaksız mutlak sözcük yok: "tek", "ilk", "en kısa", "kehanet", "batmaz". Denetim 2 dk: kanca-vaat-ödeme üçlüsü imzalanır.
- **Q8 Titanik:** İlk kart "14 YIL ÖNCE YAZILDI: KEHANET Mİ?" (soru, 6 kelime) olur; video "değil" diyerek öder. "6 BENZERLİK" kalacaksa farklar (tonaj, hız) bir cümleyle söylenir. "İkisi de batmaz diye tanıtıldı" yerine "basında 'pratikte batmaz' denmişti" (V16). "Sancak" UNVERIFIED olduğu için çıkar. 800 ft/24 bot değerlerinin hangi baskıdan geldiği doğrulanana kadar "yaklaşık" ve kaynaklı kullanılır.
- **Q1/Q2:** Cilt tavanı 3; ilk 14 günde 2. Süre: 25-32 sn kabul, yeter ki niteleme sığsın.
- **Q7:** En ucuz adım 4 videonun iddia-kaynak tablosu (~2 sa). Doğrulayıcı ikincil katmanı yaptı; kalan iş Meredith raporu gibi birincil kaynaklardır.

## 2. Response to other members

| Member | Point | Agree / disagree | Why |
|---|---|---|---|
| kanca | Emu'nun "20 bin kuşa savaş açtı" kancası model olsun | Kısmen karşı | Videoda "Bir ordu" deniyor; görev gücü üç kişi ve iki makineli tüfek (V10). "Üç asker, iki makineli tüfek, 20 bin kuş" hem doğru hem daha güçlü bir çelişki. Kanca-önce kuralına katılıyorum, "ordu" sözcüğüne değil. |
| topluluk | "10.000 mermi, 1.000 emu, ~10 mermi/kuş yuvarlama olarak savunulabilir" | Karşı | 986/9.860 komutanın öz-bildirimi; ilk fazda oran 12-50 mermi/kuş (Ek 6). "Tam 10" sahte hassasiyet. Yuvarlama değil kaynak niteleme sorunu. |
| senarist | "986/9.860 kaynaklarla uyuşuyor, doğru" | Karşı | Uyuşan tek şey, kaynakların aynı öz-bildirimi aktarması. Birincil rapor kimsede açılmadı (VERIFICATION §0). Dans'ta "sebep belirsiz = ödül yok" demesine de katılmıyorum: "dönemin kayıtları ölümü belirtmiyor" somut, doğrulanmış bir ödüldür (V30). |
| analitik | 14 gün dondur, aynı anda tek eksen | Katılıyorum, bir istisna | Hatalı iddia düzeltmesi deney değişkeni değildir; mevcut videolara sabit yorum ve açıklama düzeltmesi hemen yapılmalı. Yeniden yükleme yeni video sayılacağı için (analitik maddesi 4) düzeltme yeniden yükleme ile değil yorumla yapılır; yalnız ana sayı veya kanca yanlışsa yeniden yüklenir. |
| seytan | "İddia başına en az bir kaynak" | Karşı | Emu'nun 986 sayısı tek kaynaklı öz-bildirimdir ve yanıltıcı çıktı. Bir kaynak yetmez: 1 birincil ya da 2 bağımsız. Haftada 4-5 ve "gün zorunlu değil" önerisine katılıyorum. |
| retention | Kanca ≤4 kelime, süre 25-32 sn | Kısmen | Kısalığa itirazım yok. Ama niteleme ("rapora göre", 2 kelime) kanca değil ilk cümlede kalmalı ve atlanmamalıdır. |

## 3. Corrections accepted or disputed

Kabul: Ek 6 (Emu sayıları öz-bildirim), 7 (Titanik "batmaz"/"kehanet"), 8 (Dans ~400 üst sınır, ölüm iddiası geç kaynaklı), 9 (bayat QA raporu; QA kaynak denetlemiyor), 1-2 (metrik, 3 dk).

Sınır notu: VERIFICATION'ın "CONFIRMED" etiketi arama özetine dayanıyor (§0), birincil kaynak değil. Kendi kapım bunu "doğrulandı" saymaz; "ikincil düzeyde tutarlı" sayar. Bu itiraz düzeltmelere değil, 33 "CONFIRMED" satırının ağırlığınadır.

## 4. What would reverse this vote

- 4 videonun iddia-kaynak tablosu her video için ≤30 dk içinde, nitelemelerle birlikte temiz kapanır ve 14 günde kapı hiç yayın atlatmazsa B'ye (günlük) geçerim.
- Ortalama kapı süresi 20 dk'yı geçer ve ≥1/5 konu kaynak kapısında elenirse C'de kalır, sıklığı 3-4/haftaya indirmeyi savunurum.
- Tersi (daha sert): kapı kuralı "öneri"ye indirilirse hangi seçenek olursa olsun oyumu geri çekerim.

## 5. Dissent to record

B (günlük) çoğunluk görünümünde. Itirazım sıklığın kendisine değil, yazılı "o gün atlanır" cümlesinin yokluğuna. Kapısız günlük yayın dört denemede üç kez nitelemesiz sayı üretti; günlük baskı altında 15-20 dk'lık kapı ilk aşınan kalemdir. Her aşınma kanalın tek sermayesi olan güveni tüketir ve yorumlarda düzeltme kuyruğu olarak geri döner. Kapı yayını bloklamıyorsa B, A'nın yeniden etiketlenmiş halidir. Öneri B kabul edilirse üç şart yazılmalı: (1) kaynak dosyası yoksa yayın yok, (2) ≥5 doğrulanmış yedek konu, (3) 24 saatte düzeltme yorumu.
