"""Her planın ortasından tam boy kare (1280 px): plan_<id>.jpg + planlar.txt (id, zaman, ölçek, set).
Kullanım: python3 tools/plan_kareleri.py film.mp4 çıktı_klasörü"""
import sys, os, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mp4, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
SH = json.load(open(os.path.join(ROOT, 'vo', 'shots.json')))
f = lambda s: '%d:%04.1f' % (int(s) // 60, s % 60)
with open(os.path.join(out, 'planlar.txt'), 'w') as o:
    for x in SH:
        t = (x['at'] + x['end']) / 2
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.3f' % t, '-i', mp4, '-frames:v', '1', '-vf', 'scale=1280:720', '-q:v', '3', os.path.join(out, 'plan_%s.jpg' % x['id'])], check=True)
        o.write('%s\t%s–%s\t%s\t%s\n' % (x['id'], f(x['at']), f(x['end']), x.get('olcek', ''), x.get('set', '')))
print(len(SH), 'plan')
