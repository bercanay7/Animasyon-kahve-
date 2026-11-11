"""YouTube bölüm zaman damgalarını timeline'dan üretir: python3 tools/bolum_damga.py
Bölüm, kartının ilk karesinde başlar (kart planının çapası); ilk satır 0:00 olmak zorunda."""
import re, subprocess, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AD = [('P001', 'Ben cehennemim'), ('P008', 'Kör şair'), ('P018', 'Işık taşıyan'), ('P030', 'Dokuz gün'),
      ('P040', 'Cehennemde kral'), ('P056', 'Kapıdaki bekçiler'), ('P065', 'Güneşe itiraf'), ('P083', "Aden'de bir yabancı"),
      ('P095', 'Yılanın içinde'), ('P104', 'Alkış'), ('P115', 'Bütün dünya önlerindeydi'), ('P119', 'İki okuma: Blake mi, Lewis mi?'), ('P131', 'Bir damla yaş')]
rows = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'plan_zaman.py')], capture_output=True, text=True).stdout.split('\n')
T = {r.split()[0]: float(r.split()[1]) for r in rows if r.strip()}
for i, (pid, ad) in enumerate(AD):
    t = 0 if i == 0 else int(T[pid])
    print(f'{t // 60}:{t % 60:02d} {ad}')
