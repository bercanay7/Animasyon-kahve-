"""LemoLab ink-wash motorunu (ES modülleri, lib/vendor/) tek klasik betiğe paketler: python3 tools/bundle_ink.py → lib/ink.bundle.js
kafka/tools/bundle_woodcut.py'den uyarlandı. Modüller değiştirilmedi (Math.random yok; belirlenimci). Genel adlar: INK (ink), INKC (comp), INKL (land), INKH (hero), INKF (face), INKS (seal), INKW (wave), LIB (core/lib)."""
import re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = os.path.join(R, 'lib', 'vendor')
mods = [('lib', 'core/lib.js'), ('ink', 'ink-wash/ink.js'), ('comp', 'ink-wash/comp.js'), ('land', 'ink-wash/land.js'), ('hero', 'ink-wash/hero.js'),
        ('face', 'ink-wash/face.js'), ('seal', 'ink-wash/seal.js'), ('wave', 'ink-wash/wave.js')]
KEY = {'/core/lib.js': 'lib', './ink.js': 'ink', './comp.js': 'comp', './land.js': 'land', './hero.js': 'hero', './face.js': 'face', './seal.js': 'seal', './wave.js': 'wave'}
out = ["// ink.bundle.js: LemoLab ink-wash motoru (MIT, commit d33bdea) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.\n// Üretici: ran/tools/bundle_ink.py.\n'use strict';\nconst __M = {};\n"]
for name, path in mods:
    s = open(os.path.join(V, path), encoding='utf-8').read()
    def imp(m):
        names = [n.strip() for n in m.group(1).split(',') if n.strip()]
        names = [n.replace(' as ', ': ') for n in names]
        return 'const { ' + ', '.join(names) + ' } = __M.' + KEY[m.group(2)] + ';'
    s = re.sub(r"^import \{([^}]*)\} from '([^']+)';", imp, s, flags=re.M | re.S)
    assert not re.search(r'^import ', s, flags=re.M), (path, 'çözülmemiş import')
    ex = []
    for m in re.finditer(r"^export \{([^}]*)\};", s, flags=re.M | re.S): ex += [n.strip() for n in m.group(1).split(',') if n.strip()]
    s = re.sub(r"^export \{([^}]*)\};", '', s, flags=re.M | re.S)
    ex += re.findall(r"^export (?:const|let|function|class|async function) (\w+)", s, flags=re.M)
    for mm in re.finditer(r"^export (?:const|let) (.+)$", s, flags=re.M): ex += re.findall(r"(?:^|,\s*)(\w+)\s*=", mm.group(1))
    s = re.sub(r"^export ", '', s, flags=re.M)
    body = ''.join(f"if (typeof {n} !== 'undefined') __e.{n} = {n};\n" for n in dict.fromkeys(ex))
    out.append(f"__M.{name} = (() => {{\n{s}\nconst __e = {{}};\n{body}return __e;\n}})();\n")
out.append("window.LIB = __M.lib; window.INK = __M.ink; window.INKC = __M.comp; window.INKL = __M.land; window.INKH = __M.hero; window.INKF = __M.face; window.INKS = __M.seal; window.INKW = __M.wave;\n")
open(os.path.join(R, 'lib', 'ink.bundle.js'), 'w', encoding='utf-8').write(''.join(out)); print('lib/ink.bundle.js', sum(len(x) for x in out))
