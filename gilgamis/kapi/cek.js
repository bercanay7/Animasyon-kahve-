const {chromium}=require('playwright');const {serve}=require('../tools/sunucu');const fs=require('fs');
(async()=>{const srv=await serve(),port=srv.address().port;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('HATA',e.message));p.on('console',m=>console.log('k:',m.text()));
await p.goto(`http://127.0.0.1:${port}/kapi/kapi.html`);await p.waitForFunction(()=>window.READY);
const out=process.argv[2];for(const s of process.argv.slice(3)){const [ad,t]=s.split('@');
 const tm=await p.evaluate(([a,t])=>window.kare(a,+t||0),[ad,t]);
 await p.screenshot({path:`${out}/${ad}${t?'_'+t:''}.png`});console.log(ad,tm.map(x=>x.toFixed(0)).join(' / '),'ms');}
await b.close();srv.close();})();
