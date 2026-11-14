"""Plan listesi (yönetmen): python3 tools/planlar_kaynak.py → animatik/planlar.json + planlar.js
Alanlar: id, at (çapa: 'B02' cümle başı, 'B02@kelime' kelime), olcek (genis/orta/yakin/ayrinti/levha/ters), set, pal (palet saati değişimi; boşsa önceki sürer), ne (görüntü), yazi (ekran yazısı; kurul onaylı olmalı)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = [
 # İKİ UYARI (kanca: kapak A ile aynı kare)
 ('P01','A01','yakin','GOK','SAFAK',"İkaros güneşe bakıyor, kanat kökü; kapak karesi. Güneş halkaları yavaş genişler",''),
 ('P02','A02@güneşe','genis','GOK','',"Dev güneş diski, küçük kanatlı siluet ona doğru yükselir (tehlike yukarıda)",''),
 ('P03','A03','ayrinti','DNZ','',"Bir kanat ucu denize değer, tüy ıslanıp koyulaşır (unutulan uyarı: aşağıda). Dalga bantları",''),
 # HAVAYA KİMSE SAHİP DEĞİL
 ('P04','B02','genis','KIY','',"Seyahat afişi: Girit yalıyarı, deniz, şafak. Bilgi bandı basılır",'GİRİT|OVİDİUS · DÖNÜŞÜMLER · VIII. KİTAP'),
 ('P05','B02@labirent','ayrinti','LAB','',"Labirentin planı tepeden, duvar duvar basılır; girişte küçük Daidalos",''),
 ('P06','B03','genis','KIY','',"Ada denizin ortasında, çevresinde dalga halkaları; uzakta ufuk",''),
 ('P07','B03@yıllardır','yakin','KIY','',"Daidalos'un başı profilden, ufka bakıyor; ufukta uzak kara silueti (yurt)",''),
 ('P08','B04','orta','KIY','',"Daidalos kayalıkta, kolu göğe kalkar; kamera yukarı kayar: boş gök, martılar",''),
 # MUM VE TÜY
 ('P09','C01','ayrinti','ATL','',"Tüyler küçükten büyüğe dizilir (pan flüt gibi), ip bağlanır, sarı mum damlaları",''),
 ('P10','C02','orta','ATL','',"İkaros uçuşan tüyleri yakalıyor; Daidalos çalışıyor",''),
 ('P11','C02@başparmağıyla','ayrinti','ATL','',"Sarı mum diski, başparmak izi basılır; tüy uçları",''),
 ('P12','C03','yakin','ATL','',"İkaros bir tüyü güneşe doğru tutuyor; güneş arkada uğursuz büyük",''),
 ('P13','C04','genis','KIY','',"Daidalos kanatlarla havada asılı; aşağıda İkaros bakıyor",''),
 ('P14','C04@omuzlarına','orta','KIY','',"Daidalos kanatları oğlunun omuzlarına bağlar (üslup kapısı orta planı)",''),
 ('P15','C05','levha','UYR','',"Uyarı afişi: üç yatay bölge basılır: güneş / orta / deniz; ortada küçük figür",'ORTADAN UÇ'),
 ('P16','C06','ayrinti','UYR','',"Deniz bölgesi öne çıkar: dalga tüyü ağırlaştırıyor",'ÇOK ALÇAKTAN DA UÇMA'),
 ('P17','C06@sırrı','orta','KIY','ALACA',"Daidalos'un gölgesi uzar; ayağının dibinde çalılıkta bir keklik silueti (ön işaret)",''),
 ('P18','C07','genis','KIY','SAFAK',"Daidalos öne doğru işaret eder; İkaros arkasında",''),
 ('P19','C08','yakin','KIY','',"İki baş profilden: baba oğlunun alnını öper; tek damla gözyaşı (ışık mürekkebi)",''),
 # TANRILAR GİBİ
 ('P20','D01','genis','GOK','',"Kalkış: ikisi kayalıktan göğe; kamera izler (üslup kapısı uçuş sahnesi)",''),
 ('P21','D01@kuş','orta','GOK','',"Daidalos önde, başını çevirip oğluna bakıyor",''),
 ('P22','D02','ters','KIR','',"Aşağıdan: balıkçı, çoban, çiftçi başlarını kaldırır; gökte iki küçük kanatlı",''),
 ('P23','D03','yakin','KIR','',"Çiftçinin başı profilden, göğe bakıyor; gölgesi uzun",''),
 ('P24','D04','genis','GOK','OGLE',"İkaros babasını aşağıda bırakıp güneşe tırmanır (dikey kompozisyon)",''),
 ('P25','D04@yükseğe','yakin','GOK','',"İkaros'un yüzü güneşte, sevinç (açılış karesinin aynası)",''),
 ('P26','D05','levha','GOK','',"Göğe basılan üç kelime, sırayla",'KİBİR DEĞİL|CÜRET · SEVİNÇ · ARZU'),
 # İKAROS, NEREDESİN?
 ('P27','E01','ayrinti','GOK','BATIS',"Kanat kökünde mum damlaları akar, tüyler gevşer",''),
 ('P28','E02','orta','GOK','',"Çıplak kollar çırpıyor, tüyler savruluyor; dev güneş",''),
 ('P29','E03','genis','DNZ','',"Uzaktan: tüyler sarmal iner; denizde küçük bir halka kapanır (grafik çarpma yok)",''),
 ('P30','E04','orta','GOK','',"Boş gökte Daidalos tek başına döner, çağırır",''),
 ('P31','E05','ayrinti','DNZ','',"Dalgaların üstünde tüyler",''),
 ('P32','E05@toprağa','genis','DNZ','',"Afiş: adanın silueti alacakaranlıkta, başlık basılır (mezar yok)",'İKARYA'),
 # KEKLİĞİN SEVİNCİ
 ('P33','F01','orta','KEK','ALACA',"Kıyıda Daidalos sırtı dönük, diz çökmüş (uzak)",''),
 ('P34','F02','yakin','KEK','',"Çamurlu hendekte keklik, kanat çırpıyor, ötüyor",''),
 ('P35','F03','ayrinti','KEK','',"Kekliğin silueti yeniden basılır: aynı yerde bir çocuk silueti",'“Senin bitmeyecek suçun, Daidalos.”|DÖNÜŞÜMLER · VIII.240'),
 ('P36','F04','orta','ATL','SAFAK',"Atölye: çırak çocuk testere ve pergelle; arkada Daidalos bakıyor",''),
 ('P37','F04@testereyi','ayrinti','ATL','',"Balık kılçığı → testere, iki kollu pergel: icat afişi gibi basılır",''),
 ('P38','F05','genis','AKR','ALACA',"Akropolis kayası ve surları alacakaranlıkta; tepede iki küçük figür; kesme (itiş gösterilmez)",''),
 ('P39','F05@yalan','yakin','AKR','',"Daidalos'un profili, gözü; arkada boş kale kenarı",''),
 ('P40','F06','orta','AKR','',"Işık huzmesi: düşen küçük siluet tüy patlamasıyla kekliğe döner (Athena yalnız ışık ve baykuş)",''),
 ('P41','F07','genis','KEK','',"Keklik çitlerin üstünden alçaktan uçar; çit dibinde yuva",''),
 ('P42','F08','yakin','UYR','',"Uyarı afişi yeniden basılır; üstüne Daidalos'un profili kayık baskıyla düşer",''),
 # ÜÇ UÇUŞ
 ('P43','G01','genis','UCK','GECE',"Üç panelli afiş sırayla basılır: güneşe giden çocuk / alçakta keklik / ortada usta",''),
 ('P44','G02','orta','UCK','',"Orta panel büyür: ustanın silueti; orta bant çatlar",''),
 ('P45','G03','levha','UCK','',"Yazı afişi",'YA EN İYİSİ|YA HİÇ'),
 ('P46','G04','orta','UCK','',"Bölünmüş kare: solda usta (EN İYİSİ), sağda keklik (HİÇ)",''),
 ('P47','G05','genis','DNZ','',"Islanan tüyler yavaşça batar (alçak uçuşun düşüşü)",''),
 ('P48','G06','yakin','GOK','SAFAK',"İkaros'un uçuşu, sevinç; açılış karesi geri döner",''),
 ('P49','G07','ters','GOK','',"İkaros en tepede, bulutların üstünde; babası aşağıda küçük",''),
 ('P50','G08','genis','BRU','BRUEGEL',"Saygı karesi (kopya değil): önde saban süren çiftçi, gemi, göğe bakan çoban; köşede denizde iki küçük bacak",''),
 ('P52','G09','yakin','GOK','SAFAK',"Boş gök, güneş; tek tüy yükselir",'HANGİ YÜKSEKLİKTE UÇARDIN?'),
 ('P53','H01','genis','SON','GECE',"Bitiş ekranı: afiş çerçevesi, sağda video kutusu alanı, abone",'ZAMAN KURYESİ'),
]
out = [dict(zip(['id','at','olcek','set','pal','ne','yazi'], p)) for p in P]
# kelimeye bağlı palet değişimi (kurgu kurulu E: rakle anlamlı anlarda, plan içinde): plan kimliği → çapa
PALAT = {'P17': 'C06@ama', 'P27': 'D05@arzudan', 'P43': 'F08@atmıştı', 'P48': 'G06@önce'}
for o in out:
    if o['id'] in PALAT: o['palat'] = PALAT[o['id']]
for a, b in zip(out, out[1:]):
    if a['olcek'] == b['olcek']: print('UYARI: ardışık aynı ölçek', a['id'], b['id'], a['olcek'])
os.makedirs(os.path.join(ROOT, 'animatik'), exist_ok=True)
json.dump({'planlar': out}, open(os.path.join(ROOT, 'animatik', 'planlar.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'animatik', 'planlar.js'), 'w', encoding='utf-8').write('window.PLAN = ' + json.dumps({p['id']: p for p in out}, ensure_ascii=False) + ';\n')
print(len(out), 'plan')
