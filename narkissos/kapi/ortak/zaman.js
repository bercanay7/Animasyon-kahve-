// Üslup kapısı için sahte anlatım zaman çizelgesi (seslendirme yok). Hattımızdaki S()/Wd() bağlamasının küçük karşılığı.
// Kullanım: <script src="../ortak/zaman.js"></script> ; ZAMAN.yukle(json) ya da window.ZAMAN_JSON önceden atanır.
(function(g){
  var Z={veri:null};
  Z.yukle=function(j){Z.veri=j;return Z;};
  Z.S=function(id){var c=Z.veri.cumleler.find(function(x){return x.id===id;});if(!c)throw new Error('cümle yok: '+id);return {t0:c.t0,t1:c.t1};};
  Z.Wd=function(id,kel){var c=Z.veri.cumleler.find(function(x){return x.id===id;});var w=c&&c.kelimeler.find(function(x){return x.k.toLocaleLowerCase('tr')===kel.toLocaleLowerCase('tr');});if(!w)throw new Error('kelime yok: '+id+'/'+kel);return {t0:w.t0,t1:w.t1};};
  Z.plan=function(t){return Z.veri.planlar.find(function(p){return t>=p.t0&&t<p.t1;})||Z.veri.planlar[Z.veri.planlar.length-1];};
  g.ZAMAN=Z; g.S=Z.S; g.Wd=Z.Wd;
})(typeof window!=='undefined'?window:globalThis);
