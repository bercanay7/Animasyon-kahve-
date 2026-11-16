"""Son miks (scipy/pyloudnorm yok; ffmpeg ile): vo/vo.wav + audio/music.wav → audio/mix.wav (48 kHz stereo, -14 LUFS, ≤ -1 dBTP)
python3 tools/mix_ffmpeg.py [müzik_farkı_LU=13]
Müzik, anlatımın entegre ses yüksekliğinin GAP LU altına ayarlanır (konuşma altında ayrıca score.py kısar); toplam iki geçişli loudnorm."""
import subprocess, json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); A = lambda p: os.path.join(ROOT, p)
GAP = float(sys.argv[1]) if len(sys.argv) > 1 else 13.0
def lufs(path, extra=''):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', (extra + ',' if extra else '') + 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]); P = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1]); return I, P
vi, _ = lufs(A('vo/vo.wav')); mi, _ = lufs(A('audio/music.wav'))
g = (vi - GAP) - mi
print(f'anlatım {vi:.1f} LUFS, müzik {mi:.1f} LUFS → müzik kazancı {g:+.1f} dB')
pre = A('audio/_premix.wav')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', A('vo/vo.wav'), '-i', A('audio/music.wav'), '-filter_complex',
  f'[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0[v];[1:a]aresample=48000,volume={g:.2f}dB[m];[v][m]amix=inputs=2:normalize=0:duration=first[o]', '-map', '[o]', '-c:a', 'pcm_s24le', pre], check=True)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', pre, '-af', af + ',aresample=48000', '-c:a', 'pcm_s16le', A('audio/mix.wav')], check=True)
os.remove(pre)
I, P = lufs(A('audio/mix.wav')); print(f'mix.wav: {I:.2f} LUFS, tepe {P:.2f} dBFS')
