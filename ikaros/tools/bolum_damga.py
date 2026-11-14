"""YouTube bölüm zaman damgalarını timeline'dan üretir: python3 tools/bolum_damga.py
Bölüm, kartının ilk karesinde başlar (kart planının çapası); ilk satır 0:00 olmak zorunda."""
import re, subprocess, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AD = [('P01', 'İki uyarı'), ('P04', 'Havaya kimse sahip değil'), ('P09', 'Mum ve tüy'), ('P20', 'Tanrılar gibi'), ('P27', 'İkaros, neredesin?'), ('P33', 'Kekliğin sevinci'), ('P43', 'Üç uçuş')]
rows = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'plan_zaman.py')], capture_output=True, text=True).stdout.split('\n')
T = {r.split()[0]: float(r.split()[1]) for r in rows if r.strip()}
for i, (pid, ad) in enumerate(AD):
    t = 0 if i == 0 else int(T[pid])
    print(f'{t // 60}:{t % 60:02d} {ad}')
