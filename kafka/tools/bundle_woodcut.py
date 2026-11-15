"""LemoLab woodcut motorunu (ES modülleri, lib/vendor/) tek klasik betiğe paketler: python3 tools/bundle_woodcut.py → lib/woodcut.bundle.js
Her modül kendi kapsamında; import satırları __M.<modül> bağlarına, export'lar dönüş nesnesine çevrilir. Genel adlar: WC, WCL, WCT.
Tek davranış değişikliği: mkStroke'ta tohum verilmezse Math.random yerine nokta özeti (render işçileri arası belirlenimcilik)."""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = os.path.join(R, 'lib', 'vendor')
mods = [('lib', 'core/lib.js'), ('knife', 'woodcut/engine/knife.js'), ('hatch', 'woodcut/engine/hatch.js'), ('print', 'woodcut/engine/print.js'), ('filter', 'woodcut/engine/filter.js'), ('index', 'woodcut/engine/index.js'), ('trans', 'woodcut/trans.js')]
KEY = {'/core/lib.js': 'lib', './knife.js': 'knife', './hatch.js': 'hatch', './print.js': 'print', './filter.js': 'filter'}
out = ["// woodcut.bundle.js: LemoLab woodcut motoru (MIT, commit d33bdea) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.\n// Üretici: kafka/tools/bundle_woodcut.py. Genel ad: WC (index API), WCL (core/lib), WCT (trans).\n'use strict';\nconst __M = {};\n"]
for name, path in mods:
    s = open(os.path.join(V, path), encoding='utf-8').read()
    s = re.sub(r"^import \{([^}]*)\} from '([^']+)';", lambda m: 'const { ' + ', '.join(n.strip() for n in m.group(1).split(',')) + ' } = __M.' + KEY[m.group(2)] + ';', s, flags=re.M)
    ex = []
    m = re.search(r"^export \{([^}]*)\};", s, flags=re.M | re.S)
    if m: ex += [n.strip() for n in m.group(1).split(',') if n.strip()]; s = s[:m.start()] + s[m.end():]
    ex += re.findall(r"^export (?:const|let|function|class) (\w+)", s, flags=re.M)
    for mm in re.finditer(r"^export const (.+)$", s, flags=re.M): ex += re.findall(r"(?:^|,\s*)(\w+)\s*=", mm.group(1))
    s = re.sub(r"^export ", '', s, flags=re.M)
    if name == 'knife': s = s.replace("seed: o.seed ?? Math.random() * 1000", "seed: o.seed ?? (Math.abs(pts[0][0] * 12.9898 + pts[0][1] * 78.233) % 1000)  /* Zaman Kuryesi: Math.random yerine nokta özeti (işçiler arası belirlenimcilik) */")
    body = ''.join(f"if (typeof {n} !== 'undefined') __e.{n} = {n};\n" for n in dict.fromkeys(ex))
    out.append(f"__M.{name} = (() => {{\n{s}\nconst __e = {{}};\n{body}return __e;\n}})();\n")
out.append("window.WC = __M.index; window.WCL = __M.lib; window.WCT = __M.trans;\n")
open(os.path.join(R, 'lib', 'woodcut.bundle.js'), 'w', encoding='utf-8').write(''.join(out)); print('lib/woodcut.bundle.js')
