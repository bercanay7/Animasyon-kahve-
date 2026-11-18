"""Set iskeletleri: planlar.json'daki her plan için yer tutuculu set dosyaları ve film.html'deki <script> listesi.
python3 tools/iskelet_uret.py            # eksik set dosyalarını yazar (VAR OLANA DOKUNMAZ), film.html set bloğunu yeniler
python3 tools/iskelet_uret.py --denetle  # yalnız denetim: hangi plan hangi dosyada kayıtlı, eksik ya da fazla plan
Dosya düzeni: lib/sahne/s1/<set>.js (SAHİP-1), lib/sahne/s2/<set>.js (SAHİP-2). Bir set iki sahipte de varsa (HAVUZ, CAM …) iki dosya olur.
Yeni plan eklenince (planlar_kaynak.py) iskelet dosyasına elle eklenir; eklenmezse lib/eksik.js yer tutucusu devreye girer (konsolda uyarı)."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, 'planlar.json'), encoding='utf-8'))
SAHIP = {'SAHİP-1': 's1', 'SAHİP-2': 's2'}
gr = {}
for pid, p in P.items(): gr.setdefault((SAHIP[p['sahip']], p['set']), []).append(pid)

def kisa(s, n=150):
    s = re.sub(r'\s+', ' ', s).strip(); return s if len(s) <= n else s[:n - 1] + '…'

dosyalar = []
for (sh, st), ids in sorted(gr.items()):
    rel = f'lib/sahne/{sh}/{st.lower()}.js'; dosyalar.append(rel)
    fn = os.path.join(ROOT, rel)
    if '--denetle' in sys.argv or os.path.exists(fn): continue
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    L = [f"// {st} seti, {'SAHİP-1' if sh == 's1' else 'SAHİP-2'}: {', '.join(ids)}. Bu dosyayı yalnız bu sahip değiştirir.",
         "// Kurallar: lib/sahne/KILAVUZ.md. Yer tutucu: yt(id) + ytYazi(id); gerçek çizim gelince yerine planın kendi draw/over'ı konur.",
         "// Genel adlar set önekiyle başlar (ör. " + f"{sh}{st.lower()}_…" + "); başka dosyanın adıyla çakışmasın.",
         "'use strict';", '(() => {']
    for pid in ids:
        p = P[pid]
        L.append(f"  // {pid} · {p['olcek']} · {p['at']}" + (' · LEVHA' if p.get('levha') else '') + f" · {kisa(p['ne'])}")
        for e in p.get('eylem', []): L.append(f"  //   {e['at']}: {kisa(e['ne'], 110)}")
        if p.get('yazi'): L.append(f"  //   yazı: {kisa(p['yazi'], 130)}")
        L.append(f"  plan('{pid}', yt('{pid}'), {{ over: ytYazi('{pid}') }});")
    L.append('})();')
    open(fn, 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('yazıldı', rel)

# denetim: her plan tam bir dosyada
kayit = {}
for rel in dosyalar:
    fn = os.path.join(ROOT, rel)
    if not os.path.exists(fn): continue
    for pid in re.findall(r"plan\(\s*'(P\d{3})'", open(fn, encoding='utf-8').read()): kayit.setdefault(pid, []).append(rel)
eksik = [p for p in P if p not in kayit]; cift = {p: f for p, f in kayit.items() if len(f) > 1}; fazla = [p for p in kayit if p not in P]
yanlis = [(p, f[0]) for p, f in kayit.items() if p in P and f[0] != f"lib/sahne/{SAHIP[P[p]['sahip']]}/{P[p]['set'].lower()}.js"]
print(f'{len(dosyalar)} set dosyası, {len(kayit)}/{len(P)} plan kayıtlı'); print('eksik:', eksik or 'yok'); print('iki kez:', cift or 'yok'); print('planlar.json\'da olmayan:', fazla or 'yok'); print('yanlış dosyada:', yanlis or 'yok')

if '--denetle' not in sys.argv:
    h = os.path.join(ROOT, 'film.html'); s = open(h, encoding='utf-8').read()
    blok = '<!-- SETLER (tools/iskelet_uret.py yazar) -->\n' + '\n'.join(f'<script src="{d}"></script>' for d in dosyalar) + '\n<!-- /SETLER -->'
    s = re.sub(r'<!-- SETLER.*?<!-- /SETLER -->', blok, s, flags=re.S); open(h, 'w', encoding='utf-8').write(s); print('film.html set bloğu yenilendi')
