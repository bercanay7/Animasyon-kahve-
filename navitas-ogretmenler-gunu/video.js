// Hareketli Story/Reel: node video.js [story|feed] [çıktı.mp4]
//   FRAMES=0,45,90 → yalnız PNG kareler (kareler/ klasörüne)
//   MB=4 → hareket bulanıklığı alt kare sayısı (180° obtüratör, kareye ortalı; 1 = kapalı)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const fmt = process.argv[2] || 'story';
const out = process.argv[3] || path.join(__dirname, `ogretmenler-gunu-${fmt}.mp4`);
const MB = +(process.env.MB || 4);
const audio = path.join(__dirname, 'ses.wav');
(async () => {
  const H = fmt === 'feed' ? 1350 : 1920;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: H } });
  await p.goto('file://' + path.resolve(__dirname, 'animasyon.html') + '?f=' + fmt);
  await p.evaluate(() => window.ready);
  const { DUR, FPS } = await p.evaluate(() => ({ DUR: window.DUR, FPS: window.FPS }));
  const shot = async t => { await p.evaluate(t => window.render(t), t); return p.screenshot({ type: 'png' }); };
  if (process.env.FRAMES) {
    const dir = path.join(__dirname, 'kareler'); fs.mkdirSync(dir, { recursive: true });
    for (const f of process.env.FRAMES.split(',').map(Number))
      fs.writeFileSync(path.join(dir, `${fmt}-${String(f).padStart(3, '0')}.png`), await shot(f / FPS));
    await b.close(); return;
  }
  const n = Math.round(DUR * FPS);
  // alt kareler: her karede MB örnek, kare süresinin ilk yarısına yayılır (180° obtüratör);
  // ffmpeg tmix ortalamasını alır, select her MB'den birini tutar.
  const vf = MB > 1 ? `tmix=frames=${MB},select='not(mod(n+1\\,${MB}))',setpts=N/${FPS}/TB,` : '';
  const args = ['-y', '-f', 'image2pipe', '-framerate', String(FPS * MB), '-i', '-',
    ...(fs.existsSync(audio) ? ['-i', audio] : ['-f', 'lavfi', '-t', String(DUR), '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']),
    '-map', '0:v', '-map', '1:a', '-vf', vf + 'format=yuv420p', '-r', String(FPS),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out];
  const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < n; i++) for (let s = 0; s < MB; s++) {
    const buf = await shot(Math.max(0, i + (MB > 1 ? (s / (MB - 1) - 0.5) * 0.5 : 0)) / FPS); // 180°, faz -90°: kareye ortalı
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0 && s === 0) process.stdout.write(`\r${i}/${n}`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('\nHazır:', out);
})();
