"""youtube.md üretir: başlık seçenekleri, açıklama (bölüm zaman damgaları timeline.js'ten), kaynaklar ve künye, etiketler.
Bölüm damgası = bölüm kartının açıldığı an (ilk cümleden 1,8 sn önce; ilk bölüm 0:00).
Kullanım: python3 tools/youtube.py"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js = open(os.path.join(ROOT, 'timeline.js')).read()
CUES = json.loads(re.search(r'window\.CUES = (.*?);\n', js, re.S).group(1))
DUR = float(re.search(r'window\.DUR = ([\d.]+)', js).group(1))
segs = json.load(open(os.path.join(ROOT, 'senaryo.json')))['segments']
first = []
for s in segs:
    if not first or first[-1][0] != s['bolum']: first.append((s['bolum'], s['id']))
ts = lambda x: f'{int(x // 60)}:{int(x % 60):02d}'
chap = [('0:00', first[0][0])] + [(ts(max(0, CUES[i]['s'] - 1.8)), b) for b, i in first[1:]]
roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII']
lines = [f'{t} {"" if k == 0 else roman[k] + ". "}{b}' for k, (t, b) in enumerate(chap)]
out = f"""# YouTube: Prometheus (Türkçe)

## Başlık
Öneri (kapak A ile): `Prometheus: Ateşi Bile Bile Çalan Titan | Azra Erhat'ın Okuması`
Kapak B ile: `Prometheus: Asıl Tutsak Zeus muydu? | Aiskhylos ve Azra Erhat`
Not: "Test ve karşılaştır" sürerken başlık değiştirilmez.

## Açıklama
```
Tanrılardan ateşi bile bile çalıp insanlara veren Titan… ve onu zincire vuran Zeus'un asıl tutsak olduğu fikri.
Azra Erhat, 1967'de Aiskhylos'un Zincire Vurulmuş Prometheus'unu Sabahattin Eyüboğlu'yla Türkçeye çevirirken yazdığı önsözde bu oyunu bir duruşma gibi okur: bilinç, özgürlük ve "kıyamet de kopsa son söz özgür düşüncenindir."

Bölümler
{chr(10).join(lines)}

Kaynaklar
• Aiskhylos, Zincire Vurulmuş Prometheus, çev. Sabahattin Eyüboğlu ve Azra Erhat, önsöz: Azra Erhat (Ağustos 1967). Türkiye İş Bankası Kültür Yayınları, Hasan Âli Yücel Klasikler Dizisi. Erhat'ın görüşleri bu önsözden aktarılmış, kısa alıntılar sayfa numarasıyla verilmiştir; oyundan ve Hesiodos'tan yapılan alıntılar bu video için kendi çevirimizdir.
• Hesiodos, Theogonia (Tanrıların Doğuşu) ve İşler ve Günler.
• Franz Kafka, Dava (Der Prozess, 1925).
• J. W. von Goethe, "Prometheus" (1774).
• Mary Shelley, Frankenstein; or, The Modern Prometheus (1818).
• Kai Bird ve Martin J. Sherwin, American Prometheus (2005); Christopher Nolan, Oppenheimer (2023). Videoda film görüntüsü kullanılmamıştır.

Anlatım: Emrullah (ElevenLabs). Müzik: özgün, kodla sentezlendi. Animasyon: Yunan vazo resmi üslubunda, kodla çizildi.
Bedelini bile bile, o ateşi yine de verir miydin? Yorumlarda yaz.

#Prometheus #AzraErhat #Aiskhylos #YunanMitolojisi #Felsefe
```

## Etiketler
Prometheus, Prometheus mitolojisi, Zincire Vurulmuş Prometheus, Aiskhylos, Azra Erhat, Sabahattin Eyüboğlu, Hesiodos, Theogonia, Yunan mitolojisi, mitoloji, felsefe, özgürlük, Zeus, Pandora, Kafka Dava, Frankenstein, Oppenheimer, American Prometheus, tragedya, Zaman Kuryesi

## Bitiş ekranı
Son 20 saniye ({ts(DUR - 20)}–{ts(DUR)}). Solda video öğesi (Sisifos), sağda abone öğesi: filmde ikisi için çerçeve çizildi (video x 150–870, y 180–585; abone x 1250–1650, y 230–630).
"""
open(os.path.join(ROOT, 'youtube.md'), 'w').write(out)
print('\n'.join(lines))
