"""Shorts son miksi (ffmpeg): <proje>/vo/vo.wav + <proje>/audio/music.wav → <proje>/audio/mix.wav (48 kHz stereo, -14 LUFS, ≤ -1 dBTP)
python3 shorts-sart/tools/miks.py <proje> [müzik_farkı_LU=11]
narkissos/tools/mix_ffmpeg.py'nin kopyası; Shorts'ta müzik filmden 2 LU önde (telefon hoparlörü, ilk saniyede sessizlik yok).
Ardından müziğin saniye saniye düzey eğrisini basar (CLAUDE.md: müziğin yokluğunu miks LUFS'u göstermez)."""
import subprocess, json, re, sys, os, wave
import numpy as np
ROOT = os.path.abspath(sys.argv[1]); A = lambda p: os.path.join(ROOT, p)
GAP = float(sys.argv[2]) if len(sys.argv) > 2 else 11.0
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
# müziğin düzey eğrisi (miksteki kazançla): saniye başına RMS dB
with wave.open(A('audio/music.wav')) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, w.getnchannels()).mean(1) / 32768 * 10 ** (g / 20)
sr = 48000; n = len(x) // sr
db = [20 * np.log10(np.sqrt(np.mean(x[i * sr:(i + 1) * sr] ** 2)) + 1e-9) for i in range(n)]
print('müzik düzeyi (dBFS, saniye saniye):', ' '.join(f'{d:.0f}' for d in db))
print(f'medyan {np.median(db):.1f} dB; −60 dB üstü saniye: {sum(d > -60 for d in db)}/{n}')
