"""Plan niyetleri (sessiz okuma testi için): sahneler.js'ten her planın ne göstermesi gerektiği (yorum satırı + kullanılan set) → animatik/denetim/niyet.json"""
import re, json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(R, 'lib/sahneler.js'), encoding='utf-8').read().split('\n')
SET = {'besikOda': 'beşikli karanlık oda, kış penceresi, mum', 'solway': 'Solway körfezi, deniz, uzak İngiliz kıyısı', 'harita': 'eski harita', 'salon': 'saray salonu, yüksek pencereler',
  'galeri': 'saray galerisi (Whitehall/Fotheringhay)', 'greenwich': 'Greenwich sarayında salon', 'bataklik': 'Solway Moss bataklığı, kırık mızraklar, sancak', 'kilise': 'taş kilise içi',
  'oda': 'taş oda', 'satranc': 'satranç tahtası (beyaz vezir Elizabeth, kırmızı vezir Mary)', 'tekne': 'balıkçı teknesi', 'kadirga': 'Fransız kadırgası', 'kapilar': 'Elizabeth üç kapalı kapının önünde',
  'isleme': 'işleme kasnağı (anka kuşu, "En ma fin est mon commencement")', 'yazMasa': 'mumlu masada mektup yazan el', 'belge': 'imza bekleyen belge', 'sandik': 'gümüş sandık ve mektuplar',
  'terazi': 'iki kefeli terazi', 'kumSaati': 'kum saati', 'kitap': 'açık kitap', 'kilit': 'kilit ve anahtar', 'yuzuk': 'kırmızı yastıkta kalp biçimli elmaslı yüzük', 'arma': 'arma (İskoçya aslanı; İngiltere yarısı)',
  'idamSalonu': 'Fotheringhay büyük salonu, siyah örtülü kürsü (balta/kütük yok)', 'kadife': 'kızıl kadife kumaş kıvrımları', 'fotheringhay': 'Fotheringhay şatosu', 'lochleven': 'Loch Leven gölündeki ada kalesi',
  'tepeler': 'tepeler ve ordular', 'bozkir': 'bozkır', 'gece': 'gece, ay', 'sapel': 'Westminster VII. Henry Şapeli: iki mezar, arada koridor', 'dava': 'Fotheringhay davası: lordlar ve Mary', 'kopek': 'küçük köpek', 'fici': 'bira fıçısı', 'at(': 'atlılar'}
out = {}
for i, l in enumerate(src):
    m = re.match(r"\s*(?:P|KART)\('([A-Z]+\d*[a-z]?)'", l)
    if not m: continue
    pid = m.group(1); com = ''
    for j in range(i - 1, max(-1, i - 4), -1):
        c = src[j].strip()
        if c.startswith('//'): com = c.lstrip('/ ').strip(); break
        if c.startswith('P(') or c.startswith('KART('): break
    j = i + 1
    while j < len(src) and not re.match(r"\S", src[j]): j += 1   # gövde: girintili devam satırları
    body = ' '.join(src[i:j])
    if l.strip().startswith('KART') or pid.startswith('K') and len(pid) == 2: n = 'ara yazı kartı (siyah, süslü çerçeve, metin)'
    elif 'fotoP(' in l: n = 'gerçek dönem gravürü/resmi (' + re.search(r"fotoP\('([^']+)'", l).group(1) + '), yavaş kamera'
    elif 'masaP(' in l: n = 'ışıklı masada dönem baskısı (' + re.search(r"masaP\('([^']+)'", l).group(1) + ')'
    else:
        used = [v for k, v in SET.items() if re.search(r'\b' + re.escape(k) + (r'' if k.endswith('(') else r'\('), body)]
        n = '; '.join(used[:3]) or 'çizim'
    out[pid] = (com + ' — ' if com else '') + n
ELLE = {'B02b': 'kralın tacı yastıkta, yanında mum; "ölür"de mum söner, duman', 'F04': 'Edinburgh sokağı: insanlar ortadaki tek adamı (Bothwell, sakallı, pelerinli) parmakla gösteriyor',
  'A07': 'karanlık odada boş ahşap beşik, kış penceresi, mum; iris açılır', 'B01': 'aynı beşik, daha yakın', 'B03b': 'beşiğe bir taç iner', 'G05b': 'beşiğe küçük bir taç iner (bebek James kral)',
  'E08': 'beşikte bebek', 'L16': 'beyaz bir tül havada süzülerek yere düşer', 'L18': 'kızıl kadifenin altından küçük bir köpek çıkar', 'H03b': 'gece, ay; çıplak yerde uyuyan pelerinli kadın, köz, dalda baykuş',
  'M09': 'Westminster VII. Henry Şapeli: iki yan nefte iki mezar (I. Elizabeth ve Mary Stuart), arada koridor', 'M09b': 'aynı şapel, koridora yakın', 'M10': 'şapel; kamera Elizabeth\'in mezarından Mary\'ninkine kayar; Zweig\'ın hükmü yazı olarak',
  'E05': 'duvarda gölgeler: silahlı adamlar girer, bir adam sürüklenir, mum devrilir (kan yok)', 'E06a': 'karanlıkta devrik masa ve tek mum', 'K08': 'karanlık koridor, fener söner (sessizce)'}
out.update(ELLE)
json.dump(out, open(os.path.join(R, 'animatik/denetim/niyet.json'), 'w'), ensure_ascii=False, indent=1)
print(len(out), 'plan niyeti')
