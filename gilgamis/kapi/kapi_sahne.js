const SAHNE={
 // manzara: Uruk surları, hurmalar
 sur:{o:{zemin:.2},f:(R,t)=>{R.cam(960+t*20,560,1);R.kilZemin(-200,-200,2400,1400);
   DK.friz(R,-100,2100,120,960);
   DK.sur(R,-100,2100,760,420,{});
   for(let i=0;i<6;i++)DK.hurma(R,120+i*360,960,300+i%2*40,{meyve:i%2});
   FIG.fig(R,700,950,330,{tip:'gilgamis',f:1,kol:[[1.4,.4],[.2,.3]],bacak:[[.15,-.1],[-.12,.05]]});
   FIG.fig(R,1060,950,320,{tip:'ursa',f:-1,kol:[[.6,.8],[.1,.2]]});
 }},
 // orta plan: Gılgamış ve Enkidu boğuşma
 kavga:{o:{zemin:.2},f:(R,t)=>{R.cam(960,540,1.15);R.kilZemin(-200,-200,2400,1400);
   DK.tugla(R,300,150,1700,880,{z:.3});
   FIG.fig(R,780,900,620,{tip:'gilgamis',f:1,egilme:.35,kol:[[1.5,.2],[1.2,.6]],bacak:[[.4,-.2],[-.35,.1]]});
   FIG.fig(R,1140,900,630,{tip:'enkidu',f:-1,egilme:.35,kol:[[1.4,.4],[1.0,.7]],bacak:[[.35,-.1],[-.4,.15]],tohum:3});
 }},
 // yakın plan: yatağın başı, meşale
 yatak:{o:{zemin:.18,L:{int:.35,amb:.2,col:[.6,.55,.6],pts:[{x:1500,y:300,z:300,r:1500,i:1.5,col:[1.1,.72,.42]}]}},f:(R,t)=>{R.cam(960,560,1);R.kilZemin(-200,-200,2400,1400);
   DK.yatak(R,250,1350,650,{});
   FIG.fig(R,300,640,820,{tip:'enkidu',don:PI/2,f:-1,kol:[[.05,0],[0,0]],bacak:[[0,0],[0,0]],basO:{kapali:true}});
   FIG.fig(R,1500,900,560,{tip:'gilgamis',f:-1,otur:1,egilme:.5,bas:.4,kol:[[1.6,.9],[1.2,1.2]],giysi:'etek'});
 }},
 // yılan ve bitki
 yilan:{o:{zemin:.2,L:{dir:[-.4,-.7,.6]}},f:(R,t)=>{R.cam(960,540,1.3);R.kilZemin(-200,-200,2400,1400);
   DK.dalga(R,0,1920,700,{renk:'#4C6A9A',faz:t});
   const p=[];for(let i=0;i<18;i++)p.push([700+i*45+Math.sin(i*.7+t*2)*0,620+Math.sin(i*.8+t*3)*40]);
   DK.yilan(R,p,60);
   DK.bitki(R,640,640,220,{});
   DK.civi(R,100,100,1800,380,{});
 }},
};
SAHNE.pozlar={o:{zemin:.2},f:(R,t)=>{R.cam(960,560,1);R.kilZemin(-200,-200,2400,1400);
 const tips=['gilgamis','enkidu','samhat','siduri','utna','ursa'];
 tips.forEach((tp,i)=>FIG.fig(R,180+i*300,900,520,{tip:tp,f:1,kol:[[.3,.4],[-.1,.2]]}));
}};
SAHNE.otur={o:{zemin:.2},f:(R,t)=>{R.cam(960,560,1);R.kilZemin(-200,-200,2400,1400);
 FIG.fig(R,500,900,560,{tip:'gilgamis',f:1,otur:1,egilme:.35,bas:.3,kol:[[1.9,1.2],[1.6,1.3]]});
 FIG.fig(R,1300,900,560,{tip:'utna',f:-1,otur:1,kol:[[.6,.6],[.2,.2]]});
}};
