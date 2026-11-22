#!/usr/bin/env python3
"""Plan listesi (yönetmen: başkan). Çalıştır: python3 tools/planlar_kaynak.py → planlar.json + planlar.js
Satır: (çapa, set, ölçek, kadraj, hareket, yazı, portre)
  çapa: film.js A() yazımı: 'B02', 'B02@kelime', 'B02@kelime#1', '+0.4'
  ölçek: G geniş · O orta · Y yakın · A ayrıntı · T ters açı (ardışık iki plan aynı ölçekte olmaz)
  portre: renkli tablo kadrajda mı ve hangi durumda (G genç · Z zalimlik çizgisi · Y yıllar · C çökmüş · I ikiyüzlü · '' yok)
Görsel kurallar (üretim planı §7):
  1) Dorian'ın yüzü yalnız portrede görünür; dünyada sırtı dönük, uzak ya da gölgede.
  2) Renk yalnız portrede (tablonun içindeki kırmızı imza dahil).
  3) Ölüm ve şiddet gölgeyle verilir; kan yok. Ölü yalnız yüzüklü el.
  4) Gerçek görseller: Doré levhaları doğrudan (zaten gravür), Sarony fotoğrafları ton katmanından gravüre çevrilir; Lippincott sayfası kâğıt olarak.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETLER = {
  'ODA': "Kilitli oda: evin en üst katındaki eski okul odası; gece, lamba, kitaplık, boyalı sandık, perdeli tablo (üslup kapısı sahnesi)",
  'STU': "Basil'in stüdyosu: haziran ışığı, büyük pencere, şövale, divan; Basil, Lord Henry, Dorian (sırtı dönük)",
  'BAH': "Bahçe: leylaklar, sedir; Doré 'bahçe partisi' kuruluş planı, sonra çizim",
  'BEL': "Belge: Sarony fotoğrafı (gravüre çevrilmiş), Lippincott's 1890 sayfaları, Önsöz sayfası; kâğıt üstünde",
  'LON': "Londra: Doré levhaları (gece, sis, gaz lambası), çizilmiş sokak siluetleri",
  'TIY': "Küçük tiyatro: sahne ışıkları, balkon dekoru, Sibyl (Juliet), loca; kulis",
  'EV':  "Dorian'ın evi: holde portre, şafak ışığı, panjur, fildişi çerçeveli el aynası, yazı masası",
  'SAL': "Salon: Lord Henry'nin oturduğu oda, piyano, sigara dumanı, sarı kitap",
  'MAH': "Mahkeme 1895: sanık kürsüsü, peruklu avukat silueti, kitap; galeri",
  'SON': "Kapanış: perdeli tablo, lamba; bitiş ekranı",
}
P = [
 # ── A: kanca (0:00–0:24) ──
 ('A01',            'ODA','Y', "Lamba alevi ve mor perdenin işlemeli kenarını tutan el; perde birkaç parmak kalkar, altı karanlık", "alev titrer, el perdeyi azar azar kaldırır", '', ''),
 ('A01@kimse',      'ODA','G', "Oda geniş: sırtı dönük Dorian, masada lamba, perdeli büyük çerçeve", "yavaş yaklaşma; Dorian'ın soluğu", '', ''),
 ('A02',            'BEL','O', "Sarony 1882 Wilde portresi (gravüre çevrilmiş), kâğıt üstünde", "yavaş yaklaşma", 'OSCAR WILDE · 1890', ''),
 ('A02@sordu',      'BEL','A', "Lippincott's Temmuz 1890 başlık sayfası: THE PICTURE OF DORIAN GRAY", "sayfa hafif kayar", '', ''),
 ('A03',            'ODA','Y', "Kapalı perde, altın işleme, lamba ışığı titrer; 'göreceğiz'de perde ürperir", "perdede rüzgârsız kıpırtı", '', ''),
 # ── B: portre ve dilek (0:24–1:32) ──
 ('B01',            'STU','G', "Stüdyo: büyük pencereden haziran ışığı, şövalede tablo, Basil fırçayla, kürsüde Dorian (sırtı dönük)", "Basil'in kolu fırçayla iner kalkar; ışıkta toz", 'LONDRA · HAZİRAN', 'G'),
 ('B01@Ressam',     'STU','O', "Basil şövalenin başında, fırça tuvalde; tuval bize dönük değil (yan)", "fırça darbeleri", '', ''),
 ('B01@Dorian',     'STU','Y', "Tuvalde genç yüz: son fırça darbeleri yüzü tamamlar (darbe darbe boyama)", "darbeler sırayla belirir", '', 'G'),
 ('B02',            'STU','O', "Basil tablodan geri çekilir, fırçayı bırakır; tablo onun yanında", "Basil'in omuzları düşer", '“İçine kendimden fazlasını koydum.”', 'G'),
 ('B03',            'STU','T', "Ters açı: divanda Lord Henry, sigara dumanı tavana kıvrılır", "duman", 'LORD HENRY', ''),
 ('B03@etkilemek',  'STU','A', "Duman ince bir çizgi gibi Dorian'ın kulağına doğru uzanır (kapak B)", "duman ilerler", '', ''),
 ('B04',            'BAH','G', "Doré'nin bahçe partisi levhası, sedir ağacı", "yavaş kaydırma", '', ''),
 ('B04@Gençlik',    'BAH','O', "Leylakların altında Henry konuşur (el hareketi), Dorian sırtı dönük dinler", "Henry'nin eli, leylak dalları", '“Gençlik, sahip olmaya değer tek şeydir.”', ''),
 ('B04@Zaman',      'BAH','A', "Leylak salkımı: yapraklar birer birer düşer", "düşen yapraklar", '', ''),
 ('B05',            'STU','O', "Dorian (sırtı dönük) bitmiş tablonun önünde; tabloda genç yüz bize bakar", "Dorian'ın başı hafif eğilir", '', 'G'),
 ('B06',            'STU','Y', "Tablonun yüzü yakın; önde Dorian'ın koyu omuz silueti", "yavaş yaklaşma", '“Ruhumu bile verirdim.”', 'G'),
 ('B07',            'BEL','A', "Lippincott's 1890, s.19: 'I would give everything!' satırı ışıkta; altta 1890/1891 karşılaştırma yazısı", "ışık satır boyunca kayar", '1890: “her şeyi verirdim” · 1891: “ruhumu verirdim”', ''),
 ('B07@Vayld',      'BEL','Y', "Kâğıt üstünde iki satır dizgi: 1890 / 1891; 'ruh' sözcüğü belirir", "satırlar belirir", '', ''),
 ('B08',            'STU','O', "Basil palet bıçağını tuvale kaldırır; Dorian'ın eli bıçağı tutar (siluetler)", "kol hızla kalkar, el yakalar", '“Bu cinayet olur!”', 'G'),
 # ── C: Sibyl (1:32–3:03) ──
 ('C01',            'LON','G', "Doré: eski evli, kalabalık yoksul sokak", "yavaş kaydırma", 'BİRKAÇ HAFTA SONRA', ''),
 ('C01@Sibil',      'TIY','O', "Küçük sahne, ayak ışıkları, balkon dekoru; Juliet kılığında Sibyl", "ışık titrer, Sibyl'in kolu kalkar", 'SIBYL VANE · 17', ''),
 ('C02',            'TIY','Y', "Locada Dorian'ın sırtı ve omzu, öne eğilmiş; ötede sahne ışığı", "Dorian öne eğilir", '', ''),
 ('C03',            'TIY','G', "Salon geniş: locada üç siluet; sahnede kaskatı Sibyl", "seyirci kıpırtısı", '', ''),
 ('C04',            'TIY','Y', "Sibyl profil siluet, eli göğsünde, ışık yüzünün kenarında", "baş eğilir", '', ''),
 ('C05',            'TIY','O', "Kulis: Dorian sırtını döner, Sibyl ona uzanır", "Dorian uzaklaşır", '“Aşkımı öldürdün.”', ''),
 ('C06',            'EV', 'G', "Şafakta Dorian'ın holü: duvarda portre; Dorian geçerken durur", "Dorian yürür ve durur", '', 'G'),
 ('C07',            'EV', 'Y', "Tablonun ağzı yakın: zalimlik çizgisi darbe darbe belirir", "çizgi boyanır", '', 'Z'),
 ('C08',            'EV', 'A', "Fildişi çerçeveli el aynası arkadan; aynaya bakan baş silueti; yansıma görünmez", "ayna kalkar", '', ''),
 ('C09',            'EV', 'O', "Panjur açılır, şafak ışığı tabloya vurur; zalimlik çizgisi yerinde", "ışık açılır", '', 'Z'),
 ('C10',            'EV', 'Y', "Yazı masası: kalem, mektup", "kalem yazar", '', ''),
 ('C10@Ama',        'EV', 'G', "Holde kapı açılır, eşikte Lord Henry'nin silueti", "kapı açılır", '', ''),
 ('C11',            'SAL','Y', "Lord Henry koltukta konuşur, sigara dumanı ağır ağır kıvrılır", "duman", '“Hiç gerçekten yaşamamıştı.”', ''),
 ('C12',            'LON','G', "Opera: localar, avize ışıkları (çizim)", "avize ışıkları titrer", '', ''),
 ('C13',            'ODA','O', "İki hizmetçi çerçeveyi merdivenden yukarı taşır (siluet)", "taşıyanlar yürür", '', ''),
 ('C13@Üstüne',       'ODA','Y', "Altın işlemeli mor örtü çerçevenin üstüne iner", "örtü iner", '', ''),
 ('C13@Kapıyı',     'ODA','A', "Anahtar kilitte döner, cebe girer", "anahtar döner", '', ''),
 # ── D: yıllar (3:03–3:41) ──
 ('D01',            'ODA','Y', "Tablo: yüz darbe darbe yaşlanır (yıllar)", "darbeler", '', 'Y'),
 ('D01@sarı',       'SAL','A', "Masada sarı kapaklı kitap (gravür), sayfalar kendiliğinden çevrilir", "sayfalar döner", '', ''),
 ('D02',            'LON','G', "Doré: gece, sis, kahve tezgâhında silindir şapkalılar", "yavaş yaklaşma", '', ''),
 ('D02@inanamaz',   'LON','O', "Kalabalık siluetler Dorian'ın geçişine döner; Dorian sırtı dönük, ışıkta", "başlar döner", '', ''),
 ('D03',            'ODA','G', "Merdiven ve kilitli kapı: lambalı Dorian girer", "kapı açılır", '', ''),
 ('D03@tablodaki',  'ODA','Y', "Tabloda yaşlanan yüz ve önde aynanın parlak kenarı", "ışık titrer", '', 'Y'),
 ('D04',            'ODA','O', "Dorian elinde aynayla tablonun karşısında; yansıma yalnız ışık", "baş ayna ile tablo arasında döner", '', 'C'),
 ('D05',            'ODA','G', "Oda geniş, kapı kapanır, lamba söner", "ışık azalır", '', ''),
 # ── E: Basil (3:41–4:45) ──
 ('E01',            'LON','G', "Doré: gaz lambası, sisli gece sokağı", "yavaş yaklaşma", 'SİSLİ BİR KASIM GECESİ', ''),
 ('E01@Basil',      'LON','O', "Gaz lambası altında iki siluet karşılaşır; Basil'in elinde çanta", "Basil yürür, durur", '', ''),
 ('E02',            'SAL','O', "Kütüphanede Basil konuşur, elleri açık; Dorian sırtı dönük ateşin önünde", "Basil'in eli", '“Günah insanın yüzüne yazılır.”', ''),
 ('E03',            'SAL','Y', "Dorian'ın omzu ve başı (arkadan); omuzlar güler", "omuz sarsılır", '“Gel. Sana ruhumu göstereyim.”', ''),
 ('E04',            'ODA','G', "Merdivende yükselen lamba, duvarda büyüyen gölgeler; lamba masaya konur", "lamba yükselir", '', ''),
 ('E05',            'ODA','O', "Perde çubuğundan kopar, yere düşer; çökmüş portre", "perde düşer", '', 'C'),
 ('E05@imzayı',     'ODA','A', "Tuvalin köşesinde parlak kırmızı imza: BASIL HALLWARD", "lamba ışığı imzaya kayar", '', 'C'),
 ('E06',            'ODA','T', "Ters açı: Basil Dorian'a döner, elleri açık", "Basil yaklaşır", '“Hiçbir zaman geç değildir.”', ''),
 ('E07',            'ODA','Y', "Tablonun sırıtan dudakları; önde Dorian'ın koyu silueti", "yaklaşma", '', 'C'),
 ('E08',            'ODA','A', "Boyalı sandığın üstünde bıçak, lamba ışığında parlar", "parıltı", '', ''),
 ('E09',            'ODA','G', "Duvarda iki gölge: biri yükselir; lamba devrilir, karanlık", "gölge, karanlık", '', ''),
 ('E10',            'ODA','O', "Sabah: boş oda, perde yeniden tablonun üstünde, kapı kilitli", "toz", '', ''),
 # ── F: dönüş (4:45–5:26) ──
 ('F01',            'SAL','G', "Salon: Dorian piyanoda (sırtı dönük), Henry divanda", "Dorian'ın elleri çalar", 'HAFTALAR SONRA', ''),
 ('F01@köy',        'BAH','Y', "Elma çiçekli bir bahçede uzaklaşan köy kızı silueti", "kız uzaklaşır, yapraklar", '', ''),
 ('F02',            'SAL','O', "Dorian çalmayı keser, döner (yüzü gölgede)", "dönüş", '“Sana Basil’i ben öldürdüm desem?”', ''),
 ('F02@güler',      'SAL','Y', "Henry güler, sigara dumanı", "duman", '“Cinayet işlemek sende yok, Dorian.”', ''),
 ('F03',            'SAL','A', "Piyanonun üstünde sarı kitap, Dorian'ın eli üstünde", "el kitaba bastırır", '“Beni bir kitapla zehirledin.”', ''),
 ('F04',            'SAL','O', "Henry ayağa kalkar, eldivenlerini alır", "Henry kalkar", '“Sanatın eyleme hiçbir etkisi yoktur.”', ''),
 ('F05',            'EV', 'G', "Gece, Dorian'ın evi; kütüphanede yalnız Dorian (sırtı dönük)", "ateş titrer", '', ''),
 # ── G: son (5:26–6:45) ──
 ('G01',            'EV', 'Y', "Fildişi Cupid'li ayna; yansıma yalnız ışık; 'çalar'da ayna yere düşer, gümüş kıymıklar", "ayna kalkar, düşer, kırılır", '“Beni mahveden güzelliğimdi.”', ''),
 ('G01@çalar',      'EV', 'A', "Ayna yere düşer, gümüş kıymıklar saçılır", "kırılma", '', ''),
 ('G02',            'EV', 'O', "Dorian'ın silueti; ışık sırayla üç nesneye düşer: perdeli tablo, Basil'in paleti, sarı kitap", "ışık nesneden nesneye", '', ''),
 ('G02@Henri',      'EV', 'A', "Sarı kitap ışıkta", "ışık", '', ''),
 ('G03',            'ODA','G', "Merdivende yükselen lamba (tek başına)", "lamba yükselir", '', ''),
 ('G04',            'ODA','O', "Perde çekilir (kapı sahnesi); tablo", "perde düşer", '', 'C'),
 ('G04@sinsilik',   'ODA','Y', "Tablonun gözleri ve ağzı: ikiyüzlülük kıvrımı darbe darbe belirir", "darbeler", '', 'I'),
 ('G05',            'ODA','T', "Ters açı: tablonun yanından Dorian'ın koyu silueti", "omuz düşer", '', 'I'),
 ('G06',            'ODA','O', "Dorian'ın omuzları güler; lamba titrer", "omuz sarsılır", '', ''),
 ('G07',            'ODA','Y', "Tablonun yüzü, ağır yaklaşma", "yaklaşma", '', 'I'),
 ('G07@yok',        'ODA','A', "Sandıkta parlayan bıçak", "parıltı", '', ''),
 ('G08',            'ODA','O', "Bıçak tuvale doğru kalkar; temas anında kesme", "kol iner", '', 'I'),
 ('G09',            'LON','G', "Dışarıdan ev: meydan, gece, ışıklı pencere; geçen iki beyefendi durur", "siluetler durur", '', ''),
 ('G10',            'ODA','G', "Hizmetçiler balkondan girer; duvarda genç, güzel portre", "kapı açılır, ışık", '', 'G'),
 ('G10@genç',       'ODA','Y', "Genç portre yakın, parlak", "yavaş yaklaşma", '', 'G'),
 ('G11',            'ODA','A', "Yerde yüzüklü, buruşmuş yaşlı el (gravür); yüz yok, kan yok", "lamba ışığı", '', ''),
 ('G11@tanırlar',   'ODA','G', "Geniş: duvarda genç portre, yerde karanlık bir biçim", "karanlık çöker", '', 'G'),
 # ── mahkeme ve iksir (6:45–8:16) ──
 ('G12',            'BEL','O', "Sarony 1882 (oturan, elinde kitap; gravüre çevrilmiş)", "yavaş yaklaşma", '1895', ''),
 ('G12@mahkemede',  'MAH','G', "Mahkeme salonu siluetleri: kürsü, galeri, sanık yeri", "kalabalık kıpırtısı", 'OLD BAILEY · 3 NİSAN 1895', ''),
 ('G12@sorar',      'MAH','O', "Peruklu avukat silueti elinde dergiyi tutar", "sayfa çevrilir", '', ''),
 ('G13',            'BEL','Y', "Önsöz sayfası (dizgi): 'There is no such thing as a moral or an immoral book.'", "satır ışıkta", '“Ahlaklı ya da ahlaksız kitap diye bir şey yoktur.”', ''),
 ('G13@Vayld#1',      'MAH','O', "Tanık kürsüsünde Wilde silueti (Sarony'den gravür), dimdik", "ışık", '“Sanata bakışım budur.”', ''),
 ('G14',            'ODA','O', "Perdeli tablo, lamba (bedeli tablo ödüyordu)", "alev", '', ''),
 ('G14@Gerçek',     'BEL','Y', "Sarony portresi; mürekkep alttan yükselir, yüzü yavaşça karartır", "karartma", '1895 · İKİ YIL', ''),
 ('G15',            'BEL','G', "Üç siluet yan yana (Basil, Henry, Dorian); sözcüklere bağlı etiketler", "siluetler sırayla ışıkta", '', ''),
 ('G15@başka',      'ODA','Y', "Dorian siluetinin yerine genç portre", "darbeler", '', 'G'),
 ('G16',            'ODA','O', "Genç portre; üstünde soru", "yaklaşma", 'GÜZELLİK BİR LANET Mİ?', 'G'),
 ('G16@Basil',      'STU','G', "Boş stüdyo, boş şövale, pencere ışığı", "ışık kayar", '“Günah yüze yazılır.”', ''),
 ('G16@yazılmadı',  'ODA','Y', "Genç yüzün üstüne çökmüş yüz darbe darbe boyanır", "darbeler", '', 'C'),
 ('G17',            'SON','G', "Açılıştaki oda: lamba, perdeli tablo; soru", "alev", 'KİMSE GÖRMESEYDİ?', ''),
 ('G17@Cevabınızı', 'SON','O', "Bitiş ekranı: perdeli tablo solda karanlıkta; sağda iki video yuvası için boşluk", "alev", '', ''),
]
def main():
    planlar, son = {}, None
    for i, (at, st, ol, kd, hr, yz, pr) in enumerate(P):
        pid = f'P{i + 1:03d}'
        assert st in SETLER, st
        if son: assert not (son[0] == st and son[1] == ol), f'{pid}: ardışık aynı set ve ölçek ({st} {ol})'
        planlar[pid] = {'id': pid, 'at': at, 'set': st, 'olcek': ol, 'kadraj': kd, 'hareket': hr, 'yazi': yz, 'portre': pr}
        son = (st, ol)
    json.dump({'_not': __doc__, 'setler': SETLER, 'planlar': planlar}, open(os.path.join(ROOT, 'planlar.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(ROOT, 'planlar.js'), 'w').write('// tools/planlar_kaynak.py tarafından üretildi\nwindow.PLAN = ' + json.dumps(planlar, ensure_ascii=False) + ';\n')
    print(len(planlar), 'plan')
main()
