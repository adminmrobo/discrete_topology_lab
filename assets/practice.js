/* 마지막 장 · 실전 연습장: 이산위상 사업장 시뮬레이터 (외부 라이브러리 없음, 기록은 현재 탭에만)
   map(픽셀 지도사무소) · tile(바닥 타일 공장) · clock(나머지 시계탑) */
(function(){
'use strict';
var U=window.WU,C=window.WC,E=U.E,H=U.H;
var root=document.getElementById('sim');if(!root)return;
function el(tag,cls,html,par){return H(tag,cls,html,par);}
function sv(par,w,h,label){var s=E('svg',{viewBox:'0 0 '+w+' '+h,width:'100%',role:'img','aria-label':label});s.style.maxWidth=w+'px';par.appendChild(s);return s;}
function tx(s,x,y,t,at){var e=E('text',Object.assign({x:x,y:y,'font-size':12,fill:'#16212b','font-family':'inherit'},at||{}),s);e.textContent=t;return e;}
function says(lines){return lines.map(function(l){return '<div class="say" data-who="'+l[0]+'"><img class="who" data-who="'+l[0]+'" data-mood="'+l[1]+'" alt="" aria-hidden="true"><div><b class="name">'+window.Cast.names[l[0]]+'</b><p>'+l[2]+'</p></div></div>';}).join('');}
function card(par,lab,val,good){return '<div class="'+(good===true?'good':good===false?'bad':'')+'"><span>'+lab+'</span><b>'+val+'</b></div>';}

/* ── 탭 ── */
var SC=[{k:'map',t:'픽셀 지도사무소'},{k:'tile',t:'바닥 타일 공장'},{k:'clock',t:'나머지 시계탑'}];
var tabs=el('div','ctrl',null,root);tabs.setAttribute('role','tablist');var panes={},tbtn={};
SC.forEach(function(s){var b=el('button','bt',s.t,tabs);b.type='button';b.setAttribute('role','tab');b.onclick=function(){show(s.k);history.replaceState(null,'','#'+s.k);};tbtn[s.k]=b;
  var p=el('div','tabpane',null,root);p.id='pane-'+s.k;p.setAttribute('role','tabpanel');p.hidden=true;panes[s.k]=p;});
function show(k){if(!panes[k])k='map';SC.forEach(function(s){panes[s.k].hidden=s.k!==k;tbtn[s.k].setAttribute('aria-selected',s.k===k?'true':'false');tbtn[s.k].setAttribute('aria-pressed',s.k===k?'true':'false');});}

function frame(p,o){
  el('h2',null,o.title,p);
  el('div','three','<b>상황</b> — '+o.situ,p);
  var env=el('div','panel',null,p);env.style.borderLeft='6px solid var(--gfp)';el('div','ptitle','초록 상자 · 시장 환경 (내가 못 바꾸는 조건)',env);
  var dec=el('div','panel',null,p);dec.style.borderLeft='6px solid var(--info)';el('div','ptitle','파란 상자 · 내 결정',dec);
  var sc=el('div','sc4',null,p);sc.setAttribute('aria-live','polite');
  var g=el('div','twobox',null,p);var g1=el('div','panel',null,g),g2=el('div','panel',null,g);
  var talk=el('div','talk',null,p);
  var ms=el('div','explain',null,p);el('h3',null,'미션 3개 — 조작한 뒤에 자동 판정',ms);var ml=el('ol',null,null,ms);
  var back=el('p','note','배운 곳 다시 보기: '+o.back,p);
  return {env:env,dec:dec,sc:sc,g1:g1,g2:g2,talk:talk,ml:ml};
}
function missions(F,list){var lis=list.map(function(m){var li=el('li',null,'<b>'+m+'</b> <span class="mstat note">아직 시도 전</span>',F.ml);return li;});
  return function(i,state){var s=lis[i].querySelector('.mstat');if(state==='ok'){s.className='mstat g';s.textContent='통과 ✓';}else if(state==='try'){s.className='mstat a';s.textContent='진행 중';}};}
function radioRow(par,label,opts,cur,on){el('span','glabel',label,par);var bs=opts.map(function(o){var b=el('button','bt',o[1],par);b.type='button';b.setAttribute('aria-pressed',o[0]===cur?'true':'false');b.onclick=function(){bs.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});on(o[0]);};return b;});return bs;}
function sliderRow(par,label,min,max,step,val,fmt,on){var w=el('div','ctrl',null,par);el('span','glabel',label,w);var r=el('input',null,null,w);r.type='range';r.min=min;r.max=max;r.step=step;r.value=val;r.setAttribute('aria-label',label);var v=el('span','val',fmt(val),w);r.oninput=function(){v.textContent=fmt(+r.value);on(+r.value);};return r;}

/* ═════════ 1. 픽셀 지도사무소 ═════════ */
(function(){
  var p=panes.map,F=frame(p,{title:'픽셀 지도사무소 — 섬과 호수를 몇 개로 셀까',
    situ:'항공 사진을 픽셀(이산 공간)로 받아 섬(땅 덩어리)과 호수(물 덩어리)를 세어 보고서를 내요. 땅 픽셀과 물 픽셀에 각각 「옆자리 규칙」(4-이웃 / 8-이웃)을 정해야 해요. 고객은 「고리 모양 섬은 한 섬, 그 안의 호수는 바다와 따로」라는 상식과 맞는 보고서를 원해요.',
    back:'<a href="../12_pixel_paradox.html">12장 픽셀의 연결 역설</a> · <a href="../13_khalimsky.html">13장 칼림스키</a> · <a href="../06_connectedness.html">06장 연결</a>'});
  var MAPS={A:{n:'지도 A · 마름모 고리 섬',g:function(x,y){return Math.abs(x-6)+Math.abs(y-6)===4?1:0;}},
            B:{n:'지도 B · 대각선 강과 두 섬',g:function(x,y){if(x===y)return 0;if(Math.abs(x-y)===1)return 0;return (x<y?(x<4&&y<10):(y<5&&x>5&&x<11))?1:0;}},
            C:{n:'지도 C · 체크무늬 갯벌',g:function(x,y){return (x>2&&x<10&&y>2&&y<10)?((x+y)%2===0?1:0):0;}}};
  var N=13,st={m:'A',L:'4',W:'4'},hist={paradoxSeen88:false,maps:{},changed:false};
  var e=F.env;radioRow(e,'항공 사진:',Object.keys(MAPS).map(function(k){return [k,MAPS[k].n];}),'A',function(v){st.m=v;hist.changed=true;run();});
  var d=F.dec;var d1=el('div','ctrl',null,d);radioRow(d1,'땅 규칙:',[['4','4-이웃 (십자)'],['8','8-이웃 (왕 걸음)']],'4',function(v){st.L=v;hist.changed=true;run();});
  var d2=el('div','ctrl',null,d);radioRow(d2,'물 규칙:',[['4','4-이웃 (십자)'],['8','8-이웃 (왕 걸음)']],'4',function(v){st.W=v;hist.changed=true;run();});
  var mk=missions(F,['역설이 없는 규칙 조합을 찾아 지도 A의 섬·호수를 상식대로 세기','함정 관찰: 땅·물 모두 8-이웃일 때 지도 A의 호수가 바다와 이어지는 것 보기','조건 바꾸기: 지도 A·B·C 모두에서 같은 조합이 역설 없이 유지되는지 확인']);
  var s1=sv(F.g1,300,300,'픽셀 지도와 덩어리 색칠'),s2=sv(F.g2,300,220,'규칙 조합별 섬·호수 개수 막대 그래프');
  var D4=[[1,0],[-1,0],[0,1],[0,-1]],D8=D4.concat([[1,1],[1,-1],[-1,1],[-1,-1]]);
  function comps(G,val,rule){var lab={},c=0,D=rule==='8'?D8:D4;for(var y=0;y<N;y++)for(var x=0;x<N;x++){if(G[y][x]!==val||lab[x+','+y])continue;c++;var q=[[x,y]];lab[x+','+y]=c;while(q.length){var a=q.pop();D.forEach(function(dd){var bx=a[0]+dd[0],by=a[1]+dd[1];if(bx<0||by<0||bx>=N||by>=N)return;if(G[by][bx]===val&&!lab[bx+','+by]){lab[bx+','+by]=c;q.push([bx,by]);}});}}return {n:c,lab:lab};}
  function grid(m){var G=[];for(var y=0;y<N;y++){G.push([]);for(var x=0;x<N;x++)G[y].push(MAPS[m].g(x,y));}return G;}
  function hasDiag(G){for(var y=0;y<N-1;y++)for(var x=0;x<N-1;x++){var a=G[y][x],b=G[y][x+1],c=G[y+1][x],dd=G[y+1][x+1];if(a===dd&&b===c&&a!==b)return true;}return false;}
  function analyze(m,L,W){var G=grid(m),l=comps(G,1,L),w=comps(G,0,W);var par=hasDiag(G)&&L===W;return {G:G,land:l,water:w,par:par};}
  function run(){var A=analyze(st.m,st.L,st.W),cols=['#a35c00','#13733a','#9b3fb5','#c9302c','#2f6f8f','#5b6874'];
    s1.innerHTML='';var cs=280/N;for(var y=0;y<N;y++)for(var x=0;x<N;x++){var v=A.G[y][x],k=x+','+y,id=v?A.land.lab[k]:A.water.lab[k];
      E('rect',{x:10+x*cs,y:10+y*cs,width:cs-1,height:cs-1,fill:v?cols[(id-1)%cols.length]:(id===1?'#dbe9f6':'#9cc3e6')},s1);}
    var combos=[['4','4'],['4','8'],['8','4'],['8','8']];s2.innerHTML='';
    combos.forEach(function(cb,i){var R=analyze(st.m,cb[0],cb[1]),x0=20+i*70,cur=cb[0]===st.L&&cb[1]===st.W;
      var hL=Math.min(140,R.land.n*8),hW=Math.min(140,R.water.n*20);
      E('rect',{x:x0,y:170-hL,width:22,height:hL,fill:C.a,opacity:cur?1:.45},s2);E('rect',{x:x0+26,y:170-hW,width:22,height:hW,fill:C.b,opacity:cur?1:.45},s2);
      tx(s2,x0,186,cb[0]+'/'+cb[1],{'font-weight':cur?700:400});tx(s2,x0,200,R.par?'역설':'정상',{fill:R.par?C.r:C.g,'font-size':11});
      tx(s2,x0,165-hL,String(R.land.n),{'font-size':10,fill:C.a});tx(s2,x0+26,165-hW,String(R.water.n),{'font-size':10,fill:C.b});});
    tx(s2,10,14,'주황 = 섬 수, 파랑 = 물 덩어리 수 (진한 것이 내 선택)',{'font-size':11,fill:C.mu});
    var ok=!A.par;
    F.sc.innerHTML=card(0,'섬 (땅 덩어리)',A.land.n+'개')+card(0,'물 덩어리 (바다 + 호수)',A.water.n+'개')+card(0,'대각선 역설',A.par?'있음':'없음',ok)+card(0,'보고서 신뢰도',ok?'상식과 맞음':'다시 확인 필요',ok);
    var fl=A.par?(st.L==='8'?'땅도 물도 대각선을 건너. 고리 섬이 호수를 못 가둬.':'땅도 물도 대각선을 못 건너. 이어진 섬이 조각나 보여.'):'대각선에서 땅과 물 중 한쪽만 건너가. 그래야 모순이 없어.';
    F.talk.innerHTML=says([['doc',ok?'judge':'think',ok?'이 조합이면 보고서를 내도 좋아요. 섬 '+A.land.n+'개, 물 덩어리 '+A.water.n+'개.':'역설이 있어요. 같은 규칙을 땅과 물에 모두 쓰면 대각선에서 모순이 생겨요.'],['asst','report','지금 '+st.L+'/'+st.W+' 규칙: 섬 '+A.land.n+'개, 물 덩어리 '+A.water.n+'개예요.'],['fly','magnify',fl],['robo','calc',st.L==='8'&&st.W==='8'?'8/8이면 다 이어지니까 완벽하죠!':'숫자가 나왔으니 이대로 보고서 제출해요!']]);window.Cast.fill(F.talk);
    if(st.m==='A'&&st.L==='8'&&st.W==='8')hist.paradoxSeen88=true;
    if(ok)hist.maps[st.m+st.L+st.W]=1;
    if(hist.changed){mk(0,ok&&st.m==='A'?'ok':'try');}
    if(hist.paradoxSeen88)mk(1,'ok');else if(hist.changed)mk(1,'try');
    var combo=st.L+st.W,all=['A','B','C'].every(function(m){return hist.maps[m+combo];});if(all&&ok)mk(2,'ok');else if(Object.keys(hist.maps).length)mk(2,'try');}
  run();
})();

/* ═════════ 2. 바닥 타일 공장 ═════════ */
(function(){
  var p=panes.tile,F=frame(p,{title:'바닥 타일 공장 — 기본 벡터 두 개로 비용 줄이기',
    situ:'넓이 48 m²의 바닥에 평행사변형 타일을 깔아요. 바닥에는 1 m 간격 정수 자리마다 배선 구멍이 있고, 타일 꼭짓점(격자점)이 구멍 위에 와야 조명을 달 수 있어요. 타일 모양은 기본 벡터 u, v로 정하고, 한 장 넓이는 |행렬식|이에요. 꼭짓점이 닿지 않은 구멍은 따로 추가 공사를 해야 해요.',
    back:'<a href="../18_lattices_modular.html">18장 격자와 행렬식</a> · <a href="../17_tiles_dirichlet.html">17장 대표 타일</a> · <a href="../14_groups_and_matrices.html">14장 행렬</a>'});
  var A=48,st={S:10,P:30,u:[1,0],v:[0,1]},hist={changed:false,envP:{},flatSeen:false};
  var e=F.env;sliderRow(e,'타일 한 장 시공비(천 원)',5,40,1,st.S,function(x){return x+'천 원';},function(x){st.S=x;hist.changed=true;run();});
  sliderRow(e,'빠진 구멍 하나 추가 공사비(천 원)',5,60,1,st.P,function(x){return x+'천 원';},function(x){st.P=x;hist.changed=true;run();});
  var d=F.dec,rs=[];['u의 x','u의 y','v의 x','v의 y'].forEach(function(nm,i){rs.push(sliderRow(d,nm,-3,3,1,[1,0,0,1][i],String,function(x){if(i<2)st.u[i]=x;else st.v[i-2]=x;hist.changed=true;run();}));});
  var mk=missions(F,['구멍을 모두 덮으면서(넓이 1) (1, 0)·(0, 1)이 아닌 기본 벡터 쌍 찾기','함정 관찰: 행렬식이 0이 되는(납작한) 기본 벡터 만들어 보기','조건 바꾸기: 추가 공사비가 시공비보다 클 때, 두 가지 이상 환경에서 넓이 1이 가장 싼지 확인']);
  var s1=sv(F.g1,300,300,'격자와 기본 평행사변형'),s2=sv(F.g2,300,220,'타일 넓이별 총비용 그래프');
  function cost(dd){return dd<=0?Infinity:Math.round(A/dd*st.S+A*(1-1/dd)*st.P);}
  function run(){var det=st.u[0]*st.v[1]-st.u[1]*st.v[0],ad=Math.abs(det);
    s1.innerHTML='';var S=22,O=150;function X(x){return O+x*S;}function Y(y){return O-y*S;}
    for(var gx=-6;gx<=6;gx++)for(var gy=-6;gy<=6;gy++)E('circle',{cx:X(gx),cy:Y(gy),r:2,fill:'#c9d1d9'},s1);
    if(ad)for(var m=-14;m<=14;m++)for(var n=-14;n<=14;n++){var px=m*st.u[0]+n*st.v[0],py=m*st.u[1]+n*st.v[1];if(Math.abs(px)<=6&&Math.abs(py)<=6)E('circle',{cx:X(px),cy:Y(py),r:4,fill:C.b},s1);}
    E('polygon',{points:[[0,0],st.u,[st.u[0]+st.v[0],st.u[1]+st.v[1]],st.v].map(function(q){return X(q[0])+','+Y(q[1]);}).join(' '),fill:'rgba(163,92,0,.25)',stroke:C.a,'stroke-width':2},s1);
    s2.innerHTML='';var best=1,bc=cost(1);for(var k=1;k<=6;k++)if(cost(k)<bc){bc=cost(k);best=k;}
    var mx=0;for(k=1;k<=6;k++)mx=Math.max(mx,cost(k));
    var pts=[];for(k=1;k<=6;k++){var cx=30+(k-1)*48,cy=180-150*cost(k)/mx;pts.push(cx+','+cy);E('circle',{cx:cx,cy:cy,r:k===ad?7:4,fill:k===best?C.g:k===ad?C.b:C.mu},s2);tx(s2,cx-4,200,String(k),{'font-size':11});}
    E('polyline',{points:pts.join(' '),fill:'none',stroke:C.mu},s2);tx(s2,10,14,'가로: 타일 넓이 |행렬식|, 점 크기: 내 선택(파랑) · 최저(초록)',{'font-size':11,fill:C.mu});
    var tiles=ad?A/ad:0,miss=ad?A*(1-1/ad):A,tot=cost(ad);
    F.sc.innerHTML=card(0,'타일 한 장 넓이 |행렬식|',ad?ad+' m²':'0 (납작)',ad===1)+card(0,'필요한 타일',ad?tiles.toFixed(0)+'장':'불가',ad>0)+card(0,'빠진 구멍',ad?miss.toFixed(0)+'개':'—',ad===1)+card(0,'총비용',ad?tot.toLocaleString()+'천 원':'—',ad===best);
    F.talk.innerHTML=says([['doc',ad===best?'judge':'think',ad===0?'두 벡터가 한 줄 위예요. 타일이 납작해서 바닥을 못 덮어요.':ad===best?'이 넓이가 지금 환경에서 가장 싸요. 좋은 결정이에요.':'지금 환경에선 넓이 '+best+'가 더 싸요. 그래프를 보세요.'],['asst','report','행렬식 '+st.u[0]+'×'+st.v[1]+' − '+st.v[0]+'×'+st.u[1]+' = '+det+'. 타일 '+(ad?tiles.toFixed(0)+'장, 빠진 구멍 '+miss.toFixed(0)+'개':'계산 불가')+'.'],['fly','magnify',ad===1&&!(st.u[0]===1&&st.u[1]===0&&st.v[0]===0&&st.v[1]===1)?'모양은 비스듬해도 행렬식 1이면 구멍을 하나도 안 빠뜨려.':'벡터 길이 말고 행렬식을 봐. 그게 타일 넓이야.'],['robo','coin',ad>1?'타일이 크면 장수가 줄어 무조건 이득이죠!':'타일이 작으면 장수가 늘어 손해 아닐까요?']]);window.Cast.fill(F.talk);
    if(ad===0)hist.flatSeen=true;
    var nonstd=!(st.u[0]===1&&st.u[1]===0&&st.v[0]===0&&st.v[1]===1)&&!(st.u[0]===0&&st.u[1]===1&&st.v[0]===1&&st.v[1]===0);
    if(hist.changed)mk(0,ad===1&&nonstd?'ok':'try');
    if(hist.flatSeen)mk(1,'ok');else if(hist.changed)mk(1,'try');
    if(st.P>st.S&&ad===1&&best===1)hist.envP[st.S+'/'+st.P]=1;
    if(Object.keys(hist.envP).length>=2)mk(2,'ok');else if(hist.changed)mk(2,'try');}
  run();
})();

/* ═════════ 3. 나머지 시계탑 ═════════ */
(function(){
  var p=panes.clock,F=frame(p,{title:'나머지 시계탑 — 층층이 맞물린 시계로 수를 저장하기',
    situ:'시계탑 k층에는 눈금이 2ᵏ개인 시계가 있어요(1층 2개, 2층 4개, …). 위층 시계 바늘을 아래층 눈금 수로 나눈 나머지가 아래층 바늘과 같아야 「맞물림」이에요. 손님이 맡긴 수를 모든 층에 맞물리게 저장하면 보관료를 받고, 어긋난 층마다 수리비가 들어요.',
    back:'<a href="../23_extremal_profinite.html">23장 프로유한 공간과 2진 정수</a> · <a href="../20_deck_galois.html">20장 나머지 계산</a>'});
  var st={K:4,x:[1,1,1,1,1,1,1,1]},hist={changed:false,badSeen:false,Ks:{}};
  var e=F.env;sliderRow(e,'시계탑 층 수 K',2,8,1,st.K,function(x){return x+'층';},function(x){var old=st.K;st.K=x;for(var k=old;k<x;k++)st.x[k]=st.x[k-1];hist.changed=true;build();run();});
  var d=F.dec,box=el('div',null,null,d);
  function build(){box.innerHTML='';for(var k=1;k<=st.K;k++)(function(k){var w=el('div','ctrl',null,box);el('span','glabel',k+'층 (눈금 '+Math.pow(2,k)+'개) 바늘:',w);
      var minus=el('button','bt','−1',w);minus.type='button';var val=el('span','val',String(st.x[k-1]),w);val.dataset.k=k;var plus=el('button','bt','+1',w);plus.type='button';
      minus.onclick=function(){var m=Math.pow(2,k);st.x[k-1]=(st.x[k-1]-1+m)%m;hist.changed=true;run();};plus.onclick=function(){var m=Math.pow(2,k);st.x[k-1]=(st.x[k-1]+1)%m;hist.changed=true;run();};})(k);
    var q=el('div','ctrl',null,box);var b1=el('button','bt','정수 −1로 채우기',q);b1.type='button';b1.onclick=function(){for(var k=1;k<=st.K;k++)st.x[k-1]=Math.pow(2,k)-1;hist.changed=true;run();};
    var b2=el('button','bt','정수 5로 채우기',q);b2.type='button';b2.onclick=function(){for(var k=1;k<=st.K;k++)st.x[k-1]=5%Math.pow(2,k);hist.changed=true;run();};}
  build();
  var mk=missions(F,['모든 층을 맞물려 「−1」을 저장하기 (손으로 바늘을 맞춰도, 버튼을 써도 좋아요)','함정 관찰: 한 층만 어긋나게 만들어 수리비가 생기는 것 보기','조건 바꾸기: 층 수를 두 가지 이상으로 바꿔도 −1이 모든 층에 맞물리게 유지하기']);
  var s1=sv(F.g1,300,300,'층마다 시계와 바늘'),s2=sv(F.g2,300,220,'층마다 바늘 값과 눈금 수 그래프');
  function run(){[].forEach.call(box.querySelectorAll('.val[data-k]'),function(v){v.textContent=String(st.x[+v.dataset.k-1]);});
    var bad=[];for(var k=2;k<=st.K;k++){if(st.x[k-1]%Math.pow(2,k-1)!==st.x[k-2])bad.push(k);}
    var top=st.x[st.K-1],M=Math.pow(2,st.K),signed=top>=M/2?top-M:top,isMinus1=bad.length===0&&st.x.slice(0,st.K).every(function(v,i){return v===Math.pow(2,i+1)-1;});
    s1.innerHTML='';for(k=1;k<=st.K;k++){var cy=300-k*(280/(st.K+0.5)),r=Math.min(14,110/st.K),m=Math.pow(2,k),cx=40;
      var okk=bad.indexOf(k)<0;E('circle',{cx:cx,cy:cy,r:r,fill:'#fff',stroke:okk?C.g:C.r,'stroke-width':2},s1);
      var ang=2*Math.PI*st.x[k-1]/m-Math.PI/2;E('line',{x1:cx,y1:cy,x2:cx+r*0.85*Math.cos(ang),y2:cy+r*0.85*Math.sin(ang),stroke:C.k,'stroke-width':2},s1);
      tx(s1,cx+r+8,cy+4,k+'층: '+st.x[k-1]+' / '+m+'  (2진 '+st.x[k-1].toString(2).padStart(k,'0')+')',{'font-size':11,fill:okk?C.k:C.r});}
    s2.innerHTML='';for(k=1;k<=st.K;k++){var x0=20+(k-1)*(260/st.K),w=260/st.K-8,mm=Math.pow(2,k),h1=150*st.x[k-1]/255,h2=150*(mm-1)/255;
      E('rect',{x:x0,y:180-h2,width:w,height:h2,fill:'#eef2f6'},s2);E('rect',{x:x0,y:180-h1,width:w,height:Math.max(1,h1),fill:bad.indexOf(k)<0?C.b:C.r},s2);tx(s2,x0,196,k+'층',{'font-size':10});}
    tx(s2,10,14,'파랑 = 바늘 값, 회색 = 그 층의 최댓값(2ᵏ − 1)',{'font-size':11,fill:C.mu});
    var fee=bad.length?0:st.K*10,repair=bad.length*25;
    F.sc.innerHTML=card(0,'맞물린 층',(st.K-bad.length)+' / '+st.K,bad.length===0)+card(0,'어긋난 층',bad.length?bad.join(', ')+'층':'없음',bad.length===0)+card(0,'저장된 수 (맨 위 기준)',bad.length?'—':(signed+' (또는 '+top+')'),null)+card(0,'수입 − 수리비',(fee-repair)+'천 원',fee-repair>0);
    F.talk.innerHTML=says([['doc',bad.length?'think':'judge',bad.length?bad[0]+'층이 아래층과 맞물리지 않아요. 역극한의 점이 되려면 모든 층이 맞물려야 해요.':'모든 층이 맞물렸어요. 이 시계탑은 2진 정수 하나를 '+st.K+'자리까지 저장하고 있어요.'],['asst','report','맨 위 '+st.K+'층 바늘 '+top+' = 2진 '+top.toString(2).padStart(st.K,'0')+(isMinus1?' — 1이 끝까지 이어진 …1111, 곧 −1이에요!':'.')],['fly','magnify',bad.length?'위층을 아래층 눈금 수로 나눈 나머지를 직접 계산해 봐.':'층을 늘려도 맞물림이 유지되는지 확인해 봐. 새 층은 두 가지 중 하나야.'],['robo','calc',isMinus1?'음수를 시계에 넣다니 반칙 아닌가요…? 아, 맞물리긴 하네요.':'맨 위층만 맞으면 아래는 상관없죠!']]);window.Cast.fill(F.talk);
    if(bad.length)hist.badSeen=true;
    if(isMinus1)hist.Ks[st.K]=1;
    if(hist.changed)mk(0,isMinus1?'ok':'try');
    if(hist.badSeen)mk(1,'ok');else if(hist.changed)mk(1,'try');
    if(Object.keys(hist.Ks).length>=2&&isMinus1)mk(2,'ok');else if(hist.changed)mk(2,'try');}
  run();
})();

show((location.hash||'#map').slice(1));
addEventListener('hashchange',function(){show((location.hash||'#map').slice(1));});
window.PRACTICE_TEST={};
})();
