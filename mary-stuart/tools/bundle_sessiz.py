"""LemoLab silent-film motorunu (ES modülleri, lib/vendor/) tek klasik betiğe paketler: python3 tools/bundle_sessiz.py → lib/sessiz.bundle.js
ran/tools/bundle_ink.py'den uyarlandı. Modüller değiştirilmedi (Math.random yok, ağ çağrısı yok). Genel adlar: SFI (ink), SFR (redraw), SFP (film: FilmPost, damage), SFC (cards)."""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = os.path.join(R, 'lib', 'vendor')
mods = [('ink', 'ink.js'), ('redraw', 'redraw.js'), ('film', 'film.js'), ('cards', 'cards.js')]
KEY = {'./ink.js': 'ink', './redraw.js': 'redraw', './film.js': 'film', './cards.js': 'cards'}
out = ["// sessiz.bundle.js: LemoLab silent-film motoru (MIT, commit 3a7132b) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.\n// Üretici: mary-stuart/tools/bundle_sessiz.py.\n'use strict';\nconst __M = {};\n"]
for name, path in mods:
    s = open(os.path.join(V, path), encoding='utf-8').read()
    def imp(m):
        names = [n.strip().replace(' as ', ': ') for n in m.group(1).split(',') if n.strip()]
        return 'const { ' + ', '.join(names) + ' } = __M.' + KEY[m.group(2)] + ';'
    s = re.sub(r"^import \{([^}]*)\} from '([^']+)';", imp, s, flags=re.M | re.S)
    assert not re.search(r'^import ', s, flags=re.M), (path, 'çözülmemiş import')
    ex = re.findall(r"^export (?:const|let|function|class|async function) (\w+)", s, flags=re.M)
    for mm in re.finditer(r"^export (?:const|let) (.+)$", s, flags=re.M): ex += re.findall(r"(?:^|,\s*)(\w+)\s*=", mm.group(1))
    s = re.sub(r"^export ", '', s, flags=re.M)
    body = ''.join(f"if (typeof {n} !== 'undefined') __e.{n} = {n};\n" for n in dict.fromkeys(ex))
    out.append(f"__M.{name} = (() => {{\n{s}\nconst __e = {{}};\n{body}return __e;\n}})();\n")
out.append("window.SFI = __M.ink; window.SFR = __M.redraw; window.SFP = __M.film; window.SFC = __M.cards;\n")
open(os.path.join(R, 'lib', 'sessiz.bundle.js'), 'w', encoding='utf-8').write(''.join(out)); print('lib/sessiz.bundle.js', sum(len(x) for x in out))
