const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
(async()=>{ const b=await chromium.launch({args:['--disable-web-security']}); const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.log('[err]',e.message)); p.on('console',m=>console.log('[page]',m.text()));
 await p.goto('file://'+path.resolve(__dirname,process.argv[2]||'hiz.html')); await p.evaluate(()=>window.ready);
 console.log(await p.evaluate(()=>window.bench?bench(10):prof()));
 const b64=await p.evaluate(()=>document.getElementById('c').toDataURL('image/png').split(',')[1]); fs.writeFileSync(process.argv[3]||'/tmp/claude-0/-home-user/11d2c568-95b3-5772-9108-19223f852e25/scratchpad/hiz.png',Buffer.from(b64,'base64')); await b.close(); })();
