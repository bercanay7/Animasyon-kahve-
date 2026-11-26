#!/usr/bin/env python3
"""Kırpma kipindeki Shorts sayfasını filmin film.html'inden kurar: python3 shorts-sart/tools/sayfa.py shorts-sart/<proje>
Filmin betikleri aynı sırayla yüklenir (<base href="/<film>/">); ardından kurgu, zaman, uyum katmanı (renderAt, READY) ve lib/sart.js.
Uyum katmanı: eski motorlarda (sisifos, prometheus, ikaros) renderAt ve READY yok; window.ready + renderFrame(MB) ile kurulur."""
import json, re, sys
from pathlib import Path
P = Path(sys.argv[1]).resolve(); ROOT = Path(__file__).resolve().parents[2]
K = json.loads(re.search(r'window\.KURGU\s*=\s*(\{.*\});?\s*$', (P / 'kurgu.js').read_text(encoding='utf-8'), re.S).group(1))
film = K['film']; html = (ROOT / film / 'film.html').read_text(encoding='utf-8')
src = re.findall(r'<script src="([^"]+)"></script>', html)
css = re.findall(r'<link rel="stylesheet" href="([^"]+)">', html)
ad = P.name
out = [f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>Şart: {ad} (dikey Shorts, kırpma kipi)</title>
<!-- tools/sayfa.py üretti. Taban filmin klasörü (görseller, fontlar göreli); Shorts dosyaları mutlak yolla. Sayfa ?rs=2 ile açılır. -->
<base href="/{film}/">''']
out += [f'<link rel="stylesheet" href="{c}">' for c in css]
out.append('<link rel="stylesheet" href="/narkissos/fonts.css"><!-- Bebas Neue (kanca ve altyazı) -->')
out.append('<style>html,body{margin:0;background:#000}canvas{display:block;width:100vw;height:auto}</style></head><body>')
out.append('<canvas id="c" width="1920" height="1080"></canvas>')
out += [f'<script src="{s}"></script>' for s in src]
out.append(f'''<script src="/shorts-sart/{ad}/kurgu.js"></script>
<script src="/shorts-sart/{ad}/zaman.js"></script>
<script>
if (!window.renderAt) window.renderAt = (t, mb = 1) => {{ if (mb > 1) renderFrameMB(t, mb); else renderFrame(t); return document.getElementById('c'); }};
if (!('READY' in window) || !window.READY) (window.ready || Promise.resolve()).then(() => document.fonts.load('400 40px "Bebas Neue"', 'ĞİŞÖÜÇ')).then(() => {{ window.READY = true; }});
</script>
<script src="/shorts-sart/lib/sart.js"></script>
</body></html>''')
(P / 'index.html').write_text('\n'.join(out) + '\n', encoding='utf-8'); print(P / 'index.html', len(src), 'betik')
