// Dikey Shorts render: node /home/user/Animasyon-kahve-/narkissos/shorts/render_dikey.js [çıktı.mp4]
// WORKERS=3 (ayrı Chromium'lar; aynı tarayıcıdaki sayfalar tek GPU sürecini paylaşır), MB=4 hareket bulanıklığı.
// Ses: audio/mix.wav (filmin son miksi) shorts/dikey.js'teki kesitlerle kesilir; kesit uçlarında 15 ms yumuşatma; kapanışta miksin
// kuyruğu (sonraki cümle başlamadan) söner. Çıktı 1080×1920, 30 fps, H.264 CRF 18, BT.709, AAC 256k, ses dili tur.
const { chromium } = require('playwright');
const { fork, spawnSync } = require('child_process');
const path = require('path'), fs = require('fs');
const { serve, ROOT } = require('../tools/sunucu');
const FPS = 30, MB = +(process.env.MB || 4), N = +(process.env.WORKERS || 3);
const TMP = path.join(ROOT, 'shorts', '.kareler');

async function worker() {
  const { a, b, port } = JSON.parse(process.env._JOB);
  const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  await p.goto(`http://127.0.0.1:${port}/shorts_dikey.html?render=1&notext=1`);
  await p.waitForFunction(() => window.READY, null, { timeout: 180000 });
  for (let i = a; i < b; i++) {
    const b64 = await p.evaluate(({ t, mb }) => renderShort(t, mb).toDataURL('image/jpeg', .96).split(',')[1], { t: i / FPS, mb: MB });
    fs.writeFileSync(path.join(TMP, `k${String(i).padStart(5, '0')}.jpg`), Buffer.from(b64, 'base64'));
    if ((i - a) % 60 === 0) process.send({ i });
  }
  await br.close(); process.exit(0);
}

async function main() {
  const out = path.resolve(process.argv[2] || path.join(ROOT, 'shorts', 'narkissos_dikey.mp4'));
  fs.rmSync(TMP, { recursive: true, force: true }); fs.mkdirSync(TMP, { recursive: true });
  const srv = await serve(); const port = srv.address().port;
  // kurgu bilgisi sayfadan (tek kaynak: shorts/dikey.js)
  const br = await chromium.launch(); const pg = await br.newPage();
  await pg.goto(`http://127.0.0.1:${port}/shorts_dikey.html?render=1&notext=1`);
  await pg.waitForFunction(() => window.READY, null, { timeout: 180000 });
  const S = await pg.evaluate(() => ({ DUR: SHORTS.DUR, K: SHORTS.KESIT.map(k => [k.s0, k.s1]), F12: (window.CUES.F12 || {}).s }));
  await br.close();
  const NF = Math.round(S.DUR * FPS); console.log(`süre ${S.DUR.toFixed(2)} sn, ${NF} kare, ${N} işçi`);
  const t0 = Date.now();
  await Promise.all([...Array(N)].map((_, w) => new Promise((res, rej) => {
    const a = Math.floor(NF * w / N), b = Math.floor(NF * (w + 1) / N);
    const c = fork(__filename, [], { env: { ...process.env, _JOB: JSON.stringify({ a, b, port }) } });
    c.on('message', m => process.stdout.write(`\r[${w}] ${m.i}/${b}  ${((Date.now() - t0) / 1000) | 0} sn   `));
    c.on('exit', code => code === 0 ? res() : rej(new Error('işçi ' + w)));
  })));
  srv.close(); console.log(`\nkareler bitti (${((Date.now() - t0) / 1000) | 0} sn)`);
  // ses: kesitler + kapanış kuyruğu (sonraki cümleden 0,1 sn önce biter, son 0,6 sn söner), toplam süreye tamamlanır
  const mix = path.join(ROOT, 'audio', 'mix.wav');
  const last = S.K[S.K.length - 1][1], kuyruk = Math.max(0, Math.min(S.DUR - S.K.reduce((a, k) => a + k[1] - k[0], 0), (S.F12 || 1e9) - .1 - last));
  const parts = S.K.map(([a, b], i) => `[0:a]atrim=${a}:${b},asetpts=PTS-STARTPTS,afade=t=in:d=.015,afade=t=out:st=${(b - a - .015).toFixed(3)}:d=.015[k${i}]`);
  parts.push(`[0:a]atrim=${last}:${last + kuyruk},asetpts=PTS-STARTPTS,afade=t=out:st=${Math.max(0, kuyruk - .6).toFixed(3)}:d=${Math.min(.6, kuyruk).toFixed(3)}[ku]`);
  const fc = parts.join(';') + ';' + S.K.map((_, i) => `[k${i}]`).join('') + `[ku]concat=n=${S.K.length + 1}:v=0:a=1,apad=whole_dur=${S.DUR.toFixed(3)}[a]`;
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(TMP, 'k%05d.jpg'), '-i', mix,
    '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
    '-vf', 'scale=in_range=full:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-metadata:s:a:0', 'language=tur', '-t', S.DUR.toFixed(3), '-movflags', '+faststart', out], { stdio: 'inherit' });
  if (r.status !== 0) throw new Error('ffmpeg');
  fs.rmSync(TMP, { recursive: true, force: true });
  console.log('yazıldı:', out);
}
if (process.env._JOB) worker(); else main().catch(e => { console.error(e); process.exit(1); });
