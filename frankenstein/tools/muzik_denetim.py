import wave, json, re, sys, numpy as np
SP=sys.argv[1]; SR=48000
def rd(p, mono=True):
    w=wave.open(p); n=w.getnframes(); ch=w.getnchannels(); x=np.frombuffer(w.readframes(n),np.int16).astype(np.float32)/32768
    x=x.reshape(-1,ch); return x.mean(1) if mono else x
vo=rd(SP+'/vo48.wav'); mu=rd('audio/music.wav'); ef=rd('audio/efekt.wav'); mix=rd('audio/mix.wav')
fin={k:rd(f'{SP}/{k}.wav') for k in ['frankenstein','frankenstein_youtube','frankenstein_telefon']}
n=min(len(vo),len(mu),len(ef),len(mix),*[len(v) for v in fin.values()])
vo,mu,ef,mix=vo[:n],mu[:n],ef[:n],mix[:n]
# hizalama: son dosya ile mix arasındaki gecikme
def lag(a,b,m=4000):
    seg=slice(SR*60,SR*70); A=a[seg]; best=(0,-1)
    for d in range(-m,m+1,1):
        B=b[SR*60+d:SR*70+d]; c=np.dot(A,B)
        if c>best[1]: best=(d,c)
    return best[0]
# hızlı: FFT korelasyonu
def lagf(a,b):
    A=a[SR*60:SR*80]; B=b[SR*60:SR*80]; m=1<<int(np.ceil(np.log2(2*len(A))))
    c=np.fft.irfft(np.fft.rfft(A,m)*np.conj(np.fft.rfft(B,m)),m); k=int(np.argmax(c)); return k if k<m//2 else k-m
for k,v in fin.items(): print(k,'gecikme (örnek):',lagf(v[:n],mix))
# küresel kazançlar: mix ≈ a·vo + b·mu + c·ef
X=np.stack([vo,mu,ef],1); coef,*_=np.linalg.lstsq(X[::7],mix[::7],rcond=None); print('kazançlar vo/müzik/efekt:',np.round(coef,4))
res=mix-X@coef; print('artık / mix enerji oranı dB:',10*np.log10(np.mean(res**2)/np.mean(mix**2)))
TL=open('timeline.js').read(); CUES=json.loads(re.search(r'window\.CUES = (\{.*?\});',TL,re.S).group(1))
konus=np.zeros(n,bool)
for c in CUES.values(): konus[int(c['s']*SR):int(c['e']*SR)]=True
# yüksek geçiren (telefon hoparlörü vekili, >300 Hz) — FFT ile bloklar
def hp(x,fc=300):
    out=np.zeros_like(x); B=SR*8
    for i in range(0,len(x),B):
        s=x[i:i+B]; F=np.fft.rfft(s); f=np.fft.rfftfreq(len(s),1/SR); F[f<fc]=0; out[i:i+B]=np.fft.irfft(F,len(s))
    return out
M=mu*coef[1]; V=vo*coef[0]; E=ef*coef[2]
Mh=hp(M); Vh=hp(V)
sec=n//SR
def db(x): return 20*np.log10(np.sqrt(np.mean(x[:sec*SR].reshape(sec,SR)**2,1))+1e-9)
dM,dV,dMh,dVh,dE=db(M),db(V),db(Mh),db(Vh),db(E)
kz=konus[:sec*SR].reshape(sec,SR).mean(1)>.5
# son dosyada müzik gerçekten var mı: her saniye son dosyanın artığına müzik izdüşümü
F=fin['frankenstein_youtube'][:n]
bf=[]
for s in range(sec):
    sl=slice(s*SR,(s+1)*SR); Xs=np.stack([V[sl],M[sl],E[sl]],1)
    if np.sqrt(np.mean(M[sl]**2))<1e-4: bf.append(np.nan); continue
    c,*_=np.linalg.lstsq(Xs,F[sl],rcond=None); bf.append(c[1])
bf=np.array(bf)
np.savez(SP+'/muzik.npz',dM=dM,dV=dV,dMh=dMh,dVh=dVh,dE=dE,kz=kz,bf=bf)
print(f'süre {sec} sn')
print('müzik düzeyi (son miks, dBFS): medyan %.1f | konuşmada %.1f | konuşma dışı %.1f'%(np.median(dM),np.median(dM[kz]),np.median(dM[~kz])))
print('müzik-ses farkı konuşmada (dB): medyan %.1f, en kötü %%10: %.1f'%(np.median(dM[kz]-dV[kz]),np.percentile(dM[kz]-dV[kz],10)))
print('>300 Hz müzik-ses farkı konuşmada: medyan %.1f'%np.median(dMh[kz]-dVh[kz]))
print('>300 Hz müzik / tüm müzik enerji (dB) medyan %.1f'%np.median(dMh-dM))
print('son dosyada müzik kazancı oranı (1=tam): medyan %.3f, min %.3f, <0.8 saniye: %s'%(np.nanmedian(bf),np.nanmin(bf),list(np.where(bf<.8)[0])))
for th in [-50,-55,-60]: print(f'müzik {th} dBFS altı saniyeler:',list(np.where(dM<th)[0]))
print('telefonda (>300Hz) müzik -55 altı saniye sayısı:',int((dMh<-55).sum()))
