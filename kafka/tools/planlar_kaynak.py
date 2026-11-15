"""Plan listesi (yönetmen): python3 tools/planlar_kaynak.py → animatik/planlar.json + planlar.js
Alanlar: id, at (çapa: 'B02' cümle başı, 'B02@kelime'), olcek (genis/orta/yakin/ayrinti/levha/ters), set, ne (görüntü), yazi.
Kural: böcek hiç çizilmez (ne gölgesi ne bacağı); Gregor yalnız geri dönüşte insan olarak görünür. Kamera çoğunlukla yerden (Gregor'un bakışı)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = [
 # BİR SABAH (Ki)
 ('P01','A01','yakin','KAPI',"Yerden: karanlık oda, aralık kapı; kapıdan yere düşen ışık şeridi; şeritte kırmızı elma (kapak A karesi). Şerit yavaşça genişler",''),
 ('P02','A01@sevenler','ters','KAPI',"Aşağıdan: kapı boşluğunda üç siluet (baba, anne, Grete) arkadan ışıklı, aşağıya bakıyor",''),
 ('P03','A02','levha','KITAP',"Kara blok; başlık oyulur",'DÖNÜŞÜM|FRANZ KAFKA · 1915'),
 ('P04','A02@Gregor','genis','ODA',"Yüksekten oda: yatak, kabarık yorgan yavaşça inip kalkar; pencerede yağmur; duvarda çerçeveli resim",''),
 ('P05','A03','ayrinti','SAAT',"Çalar saat: yelkovan altı buçukta, saniye ibresi ilerler",''),
 ('P06','A04@treni','genis','TREN',"İstasyon: tren kalkıyor, buhar oyulur; peron boş",''),
 ('P07','A04@patron','ters','PATRON',"Aşağıdan: yüksek kürsüde patron silueti, aşağıya konuşur",''),
 ('P08','A05','ayrinti','CERCEVE',"Duvarda boş çerçeve: bıçak oymaya başlar, içi kara kalır",''),
 ('P09','A06','orta','AILE',"Aile portresi: baba, anne, Grete yan yana; Grete'nin üstüne ışık",''),
 # HAYVAN SESİ
 ('P10','B01','genis','YOL',"Gezici satıcı: kumaş örnekleri çantasıyla yağmurda yürüyen Gregor (insan, geri dönüş) ; bölüm başlığı",'HAYVAN SESİ'),
 ('P11','B01@borcu','ayrinti','PARA',"Masada borç senetleri ve sikkeler; bir el sikkeleri iter",''),
 ('P12','B02','orta','KORIDOR',"Koridor: kapalı kapının önünde melon şapkalı müdür yardımcısı, baston; anne ve baba arkada",''),
 ('P13','B03','yakin','KORIDOR',"Müdür yardımcısının baş profili, kapıya eğilmiş; alıntı oyulur",'“BU BİR HAYVAN SESİYDİ.”'),
 ('P14','B04','ayrinti','KILIT',"Kilitte anahtar yavaşça döner (oyulmuş ak anahtar)",''),
 ('P15','B04@merdivenlere','genis','MERDIVEN',"Merdiven boşluğu: müdür yardımcısı aşağı kaçar, palto eteği uçuşur",''),
 ('P16','B05','ters','KAPI',"Aşağıdan: baba bastonu kaldırmış, gazete elinde, üstümüze yürür; arkasından ışık",''),
 ('P17','B06','yakin','KAPI',"Kapı kapanır, ışık şeridi daralıp kaybolur",''),
 # SÜT VE ELMA
 ('P18','C01','orta','KAPI',"Grete eşikte diz çöker, elinde kâse; bölüm başlığı",'SÜT VE ELMA'),
 ('P19','C02','ayrinti','KASE',"Yerde süt kâsesi, beyaz ekmek parçaları yüzer; süt halkalanır",''),
 ('P20','C03','ayrinti','YEMEK',"Eski gazete üstünde yarı çürük sebzeler, peynir, kemikler",''),
 ('P21','C04','yakin','GRETE',"Grete'nin profili, aşağı bakıyor; kandil ışığı",''),
 ('P22','C05','ters','KAPI',"Aşağıdan: kapıda üniformalı baba, kep, ak oyulmuş düğmeler, dimdik",''),
 ('P23','C06','ayrinti','BUFE',"Büfede meyve tabağı; babanın eli kırmızı elmaları alır",''),
 ('P24','C06@attı','genis','ODA',"Yerde kırmızı elmalar yuvarlanır, çarpışır",''),
 ('P25','C07','yakin','ODA',"Bir elma karanlığa uçar ve orada kırmızı bir leke olarak kalır",''),
 ('P26','C07@çürüdü','ayrinti','ODA',"Karanlıktaki kırmızı leke yavaşça kararır",''),
 # KAPININ ARKASINDAKİ HESAP
 ('P27','D01','orta','GECMIS',"Geri dönüş: Gregor (insan) eve girer, şapkasını asar; bölüm başlığı",'KAPININ ARKASINDAKİ HESAP'),
 ('P28','D02','genis','SOFRA',"Lamba altında sofra: Gregor parayı masaya koyar, aile oturuyor",''),
 ('P29','D03','yakin','SOFRA',"Masada para; eller alır, kimse başını kaldırmaz; alıntı oyulur",'“PARAYI MİNNETLE ALIYORLARDI…”'),
 ('P30','D04','yakin','KAPI',"Kapı aralığından içeri: lamba altında baba küçük bir kasa açıyor (Gregor'un bakışı)",''),
 ('P31','D05','ayrinti','KASA',"Kasanın içi: sikke yığınları büyür",''),
 ('P32','D05@borcu','genis','YOL',"Geri dönüş: Gregor yağmurda, çantası elinde, bitmeyen tren yolları",''),
 ('P33','D06','yakin','KAPI',"Karanlık taraftan kapı aralığı; ışık",''),
 ('P34','D07','ayrinti','KAPI',"Kapı aralığı yakın; kamera yavaşça başını sallar gibi iner kalkar",''),
 ('P35','D08','orta','TERAZI',"Eski terazi: bir kefede Gregor'un fotoğrafı, ötekinde sikkeler; sikkeler ağır basar",''),
 ('P36','D09','orta','KEMAN',"Geri dönüş: pencere önünde keman çalan Grete; Gregor (insan) dinliyor",''),
 # O DEĞİL, BU
 ('P37','E01','genis','UCLU',"Üç pencereli baskı: bankada baba, lamba altında dikiş diken anne, tezgâhta Grete",''),
 ('P38','E02','ayrinti','ESIK',"Eşikte bir ayak tabağı içeri iter; duvarda kir izleri; bölüm başlığı",'O DEĞİL, BU'),
 ('P39','E03','orta','SALON',"Salon: üç sakallı kiracı masada, Grete keman çalıyor",''),
 ('P40','E04','yakin','SALON',"Kiracılar başlarını kapıya çevirir; ayağa kalkarlar",''),
 ('P41','E05','orta','SALON',"Grete eliyle masaya vurur; baba ve anne oturuyor; alıntı oyulur",'“KARDEŞİMİN ADINI AĞZIMA ALMAYACAĞIM.”'),
 ('P42','E06','yakin','SALON',"Baba başını ellerine almış; Grete ayakta",''),
 ('P43','E07','ayrinti','KASE',"Boş, tozlu süt kâsesi (P19'un aynası)",''),
 ('P44','E08','genis','ODA',"Gece oda: kapının altından ince ışık; pencere karanlık",''),
 ('P45','E09','genis','PENCERE',"Pencere: kilise kulesi, gök aydınlanır (ışık oyulur)",''),
 ('P46','E10','genis','TRAMVAY',"Güneşli kır yolunda tramvay",''),
 ('P47','E11','orta','TRAMVAY',"Tramvayın içi: anne ve baba Grete'ye bakıyor",''),
 ('P48','E12','orta','TRAMVAY',"Grete ayağa kalkıp kollarını açar; arkasında oyulmuş güneş",''),
 # GÖRÜNMEYEN BÖCEK
 ('P49','F01','ayrinti','KITAP',"1915 ilk baskı (kendi çizimimiz): kitap kapağı, kapakta yalnız aralık kapı",''),
 ('P50','F02','ayrinti','MEKTUP',"Masada mektup, el yazısı satırlar; alıntı oyulur",'“BÖCEĞİN KENDİSİ ÇİZİLEMEZ.”'),
 ('P51','F03','ters','KAPI',"P02'nin aynası: kapıda aile aşağıya bakıyor",''),
 ('P52','F04','orta','KAFKA',"Gece: masa başında yazan bir adam silueti (dönem silueti), lamba; zarf; alıntı",'“YAZDIKLARIM HEP SENİN HAKKINDAYDI.”'),
 ('P53','F05','genis','BUGUN',"Bugün: gece apartman koridoru, kapalı kapılar; birinin altından ışık",''),
 ('P54','F06','orta','BUGUN',"Kapının arkasında yatağın kenarında oturan bugünün insanı (kapüşonlu)",''),
 ('P55','F07','yakin','KAPI',"Açılış karesi geri döner: aralık kapı, ışık şeridi, kırmızı elma; soru oyulur",'SENİ Mİ SEVİYORLARDI?'),
 ('P56','F08@camus','genis','SON',"Tepede kaya ve küçük figür (Sisifos'a köprü); ZAMAN KURYESİ; bitiş ekranı alanı",''),
]
ids = [p[0] for p in P]; assert len(ids) == len(set(ids))
out = [dict(id=a, at=b, olcek=c, set=d, ne=e, yazi=f) for a, b, c, d, e, f in P]
json.dump({'planlar': out}, open(os.path.join(ROOT, 'animatik', 'planlar.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'animatik', 'planlar.js'), 'w').write('window.PLAN = ' + json.dumps({p['id']: p for p in out}, ensure_ascii=False) + ';\n')
print(len(out), 'plan')
