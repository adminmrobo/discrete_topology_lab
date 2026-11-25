/* 위젯 모음 5: 활용 편
   raster(연속 모양을 픽셀로) · vessel(혈관 영상 이진화) · mesh(삼각형 메시 찢기·오일러 수) · sensor(센서망 연결·음영) · barcode(점 구름 지속성) · water(물 빠지기·이산 모스) */
(function(){
'use strict';
var U=window.WU,C=window.WC,E=U.E,H=U.H,svg=U.svg,ctrl=U.ctrl,btn=U.btn,radio=U.radio,slider=U.slider,out=U.out,tx=U.tx;
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function gauss(R){var u=R()||1e-9,v=R();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
function UF(n){var p=[];for(var i=0;i<n;i++)p.push(i);function f(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x];}return x;}return {find:f,union:function(a,b){a=f(a);b=f(b);if(a===b)return false;p[a]=b;return true;}};}
/* 격자에서 덩어리 세기: 값이 val인 자리끼리, k=4 또는 8 이웃 */
function label(G,W,Hh,val,k){var lab=new Int32Array(W*Hh),c=0,D=k===8?[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]:[[1,0],[-1,0],[0,1],[0,-1]];
  for(var y=0;y<Hh;y++)for(var x=0;x<W;x++){var i=y*W+x;if(G[i]!==val||lab[i])continue;c++;var q=[i];lab[i]=c;while(q.length){var a=q.pop(),ax=a%W,ay=(a-ax)/W;
    for(var d=0;d<D.length;d++){var bx=ax+D[d][0],by=ay+D[d][1];if(bx<0||by<0||bx>=W||by>=Hh)continue;var b=by*W+bx;if(G[b]===val&&!lab[b]){lab[b]=c;q.push(b);}}}}
  return {n:c,lab:lab};}

/* 1. 연속 모양을 픽셀로: 해상도에 따라 덩어리·구멍 수가 바뀌나 */
W.raster=function(el,o){
  var SH={ring:{n:'고리 (도넛 단면)',f:function(x,y){var r=Math.hypot(x-.5,y-.5);return r>=.25&&r<=.36;},t:[1,1]},
          eight:{n:'8자 (구멍 2개)',f:function(x,y){var a=Math.hypot(x-.3,y-.5),b=Math.hypot(x-.7,y-.5);return (a>=.12&&a<=.2)||(b>=.12&&b<=.2);},t:[1,2]},
          two:{n:'두 섬',f:function(x,y){return Math.hypot(x-.3,y-.5)<=.15||Math.hypot(x-.72,y-.5)<=.15;},t:[2,0]}};
  var st={s:o.shape||'ring',N:o.N||8};
  var c=ctrl(el);radio(c,'모양:',Object.keys(SH).map(function(k){return [k,SH[k].n];}),st.s,function(v){st.s=v;draw();});
  var c2=ctrl(el);slider(c2,'해상도 (한 줄 픽셀 수)',4,48,1,st.N,function(v){st.N=v;draw();return v+' × '+v;});
  var s=svg(el,300,300,'연속 모양과 그 픽셀 그림'),ou=out(el);
  function draw(){var N=st.N,G=new Uint8Array(N*N),f=SH[st.s].f;for(var y=0;y<N;y++)for(var x=0;x<N;x++)G[y*N+x]=f((x+.5)/N,(y+.5)/N)?1:0;
    var obj=label(G,N,N,1,8),bg=label(G,N,N,0,4),holes=0,seen={};
    for(var i=0;i<N*N;i++){if(G[i])continue;var x=i%N,yy=(i-x)/N;if(x===0||yy===0||x===N-1||yy===N-1)seen[bg.lab[i]]=1;}
    for(var b=1;b<=bg.n;b++)if(!seen[b])holes++;
    s.innerHTML='';var cs=280/N;for(i=0;i<N*N;i++){x=i%N;yy=(i-x)/N;if(G[i])E('rect',{x:10+x*cs,y:10+yy*cs,width:cs-.6,height:cs-.6,fill:C.b},s);}
    if(st.s==='ring'){E('circle',{cx:150,cy:150,r:.25*280,fill:'none',stroke:C.a,'stroke-dasharray':'4 3'},s);E('circle',{cx:150,cy:150,r:.36*280,fill:'none',stroke:C.a,'stroke-dasharray':'4 3'},s);}
    var t=SH[st.s].t,ok=obj.n===t[0]&&holes===t[1];
    ou.innerHTML='<p>진짜 모양: 덩어리 <b>'+t[0]+'</b>개, 구멍 <b>'+t[1]+'</b>개</p><p>'+N+' × '+N+' 픽셀 그림: 덩어리 <b>'+obj.n+'</b>개 (대각선까지 이웃), 구멍 <b>'+holes+'</b>개 (가로세로로 바깥과 안 이어진 빈 곳)</p>'+
      '<p class="'+(ok?'g':'r')+'">'+(ok?'픽셀 그림이 진짜 모양의 덩어리·구멍 수를 지켰어요.':'해상도가 낮아서 모양이 바뀌었어요. 덩어리나 구멍 수가 진짜와 달라요.')+'</p>';}
  draw();
};

/* 2. 혈관 영상: 밝기 기준(임계값)으로 혈관을 골라내면 몇 조각? */
W.vessel=function(el,o){
  var Wd=64,Ht=40,R=rng(o.seed||7),I=new Float32Array(Wd*Ht),st={t:o.t||0.5,mode:o.mode||'cut'};
  var segs=[[2,20,30,20,2.2,.92],[30,20,60,8,1.6,.72],[30,20,60,32,1.6,.72],[18,20,26,5,1.1,.55],[44,14,52,3,.9,.47],[44,26,55,38,.9,.47],[12,20,16,36,1.0,.52]];
  for(var y=0;y<Ht;y++)for(var x=0;x<Wd;x++){var v=.18+.06*gauss(R);segs.forEach(function(g){var dx=g[2]-g[0],dy=g[3]-g[1],L=dx*dx+dy*dy,u=Math.max(0,Math.min(1,((x-g[0])*dx+(y-g[1])*dy)/L)),d=Math.hypot(x-g[0]-u*dx,y-g[1]-u*dy);if(d<=g[4])v=Math.max(v,g[5]*(1-.15*u)+.05*gauss(R));});I[y*Wd+x]=v;}
  var c=ctrl(el);slider(c,'밝기 기준 (임계값)',0.2,0.8,0.01,st.t,function(v){st.t=v;draw();return v.toFixed(2);});
  if(o.mode==='edge'){var c2=ctrl(el);radio(c2,'보기:',[['cut','골라낸 혈관'],['edge','테두리만']],'edge',function(v){st.mode=v;draw();});}
  var s=svg(el,640,400,'합성 혈관 영상과 골라낸 혈관 조각'),ou=out(el);
  function draw(){var G=new Uint8Array(Wd*Ht);for(var i=0;i<Wd*Ht;i++)G[i]=I[i]>=st.t?1:0;var L=label(G,Wd,Ht,1,8),cnt={};for(i=0;i<Wd*Ht;i++)if(L.lab[i])cnt[L.lab[i]]=(cnt[L.lab[i]]||0)+1;
    var big=0,bigk=0,tot=0;Object.keys(cnt).forEach(function(k){tot+=cnt[k];if(cnt[k]>big){big=cnt[k];bigk=+k;}});
    var small=Object.keys(cnt).filter(function(k){return cnt[k]<6;}).length,edge=0;s.innerHTML='';var cs=10;
    for(i=0;i<Wd*Ht;i++){var x=i%Wd,y=(i-x)/Wd,g=Math.round(255*Math.min(1,I[i]));
      var fill='rgb('+g+','+g+','+g+')';
      if(G[i]){var isBig=L.lab[i]===bigk;var bd=false;[[1,0],[-1,0],[0,1],[0,-1]].forEach(function(d){var bx=x+d[0],by=y+d[1];if(bx<0||by<0||bx>=Wd||by>=Ht||!G[by*Wd+bx])bd=true;});
        if(bd&&isBig)edge++;
        if(st.mode==='edge')fill=bd&&isBig?'#c1302c':(isBig?'#f2d6d4':'#e9b949');else fill=isBig?'#1e55c8':'#e9b949';}
      E('rect',{x:x*cs,y:y*cs,width:cs,height:cs,fill:fill},s);}
    ou.innerHTML='<p>기준 '+st.t.toFixed(2)+' 이상인 자리를 혈관으로 골랐어요 → 조각 <b>'+L.n+'</b>개 (가장 큰 조각이 골라낸 자리의 '+(tot?Math.round(100*big/tot):0)+'%)</p>'+
      (st.mode==='edge'?'<p>가장 큰 혈관 조각의 테두리 자리: <b>'+edge+'</b>개 (가로세로 이웃 중 하나라도 혈관 밖이면 테두리 — 02장의 「경계」)</p>':'')+
      '<p class="'+(L.n===1?'g':'a')+'">'+(L.n===1?'혈관이 한 조각으로 이어졌어요. 실제 혈관 구조와 맞아요.':(small?'작은 점 조각 '+small+'개는 잡음일 가능성이 커요. ':'')+(st.t>0.55?'기준이 높아서 가는 혈관이 끊겼을 수 있어요.':'기준이 낮아 배경 잡음이 섞였을 수 있어요.'))+'</p>';}
  draw();
};

/* 3. 삼각형 메시: 삼각형을 빼며 V − E + F와 구멍 세기 */
W.mesh=function(el,o){
  if(o.mode==='closed')return closed(el,o);
  var cols=6,rows=4,S=46,on=[],T=[];
  for(var r=0;r<rows;r++)for(var c=0;c<cols;c++){var a=r*(cols+1)+c,b=a+1,d=a+cols+1,e=d+1;T.push([a,b,e]);T.push([a,e,d]);}
  function preset(k){on=T.map(function(){return true;});if(k==='hole'){[14,15,16,17,26,27,28,29].forEach(function(i){on[i]=false;});}
    if(k==='two'){for(var r2=0;r2<rows;r2++){on[r2*12+6]=false;on[r2*12+7]=false;}}
    if(k==='tear'){[0,1,12,13].forEach(function(i){on[i]=false;});}draw();}
  var c0=ctrl(el);H('span','glabel','미리 정한 모양:',c0);[['full','온전한 판'],['hole','가운데 구멍'],['tear','가장자리 찢김'],['two','두 조각']].forEach(function(p){btn(c0,p[1],function(){preset(p[0]);});});
  var s=svg(el,330,230,'삼각형 메시. 삼각형을 눌러 빼거나 넣기'),ou=out(el);
  function P(v){var x=v%(cols+1),y=(v-x)/(cols+1);return [20+x*S,20+y*S];}
  function draw(){var used={},edges={},F=0;s.innerHTML='';
    T.forEach(function(t,i){var pts=t.map(P);var pg=E('polygon',{points:pts.map(function(p){return p.join(',');}).join(' '),fill:on[i]?'#dbe7f6':'#fff',stroke:on[i]?'#8aa4c8':'#eef1f4','stroke-width':1,style:'cursor:pointer',tabindex:0,role:'button','aria-label':'삼각형 '+(i+1)+(on[i]?' 있음':' 없음')},s);
      pg.addEventListener('click',function(){on[i]=!on[i];draw();});pg.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();on[i]=!on[i];draw();}});
      if(!on[i])return;F++;t.forEach(function(v){used[v]=1;});[[t[0],t[1]],[t[1],t[2]],[t[2],t[0]]].forEach(function(e){var k=Math.min(e[0],e[1])+'-'+Math.max(e[0],e[1]);edges[k]=(edges[k]||0)+1;});});
    var V=Object.keys(used).length,Ek=Object.keys(edges),Ecount=Ek.length,bd=Ek.filter(function(k){return edges[k]===1;});
    bd.forEach(function(k){var ab=k.split('-').map(Number),p=P(ab[0]),q=P(ab[1]);E('line',{x1:p[0],y1:p[1],x2:q[0],y2:q[1],stroke:C.r,'stroke-width':3},s);});
    var vid={},n=0;bd.forEach(function(k){k.split('-').forEach(function(v){if(vid[v]==null)vid[v]=n++;});});var uf=UF(n);bd.forEach(function(k){var ab=k.split('-');uf.union(vid[ab[0]],vid[ab[1]]);});
    var loops={};Object.keys(vid).forEach(function(v){loops[uf.find(vid[v])]=1;});var nl=Object.keys(loops).length;
    var tuf=UF(T.length),eo={};T.forEach(function(t,i){if(!on[i])return;[[t[0],t[1]],[t[1],t[2]],[t[2],t[0]]].forEach(function(e){var k=Math.min(e[0],e[1])+'-'+Math.max(e[0],e[1]);if(eo[k]!=null)tuf.union(eo[k],i);else eo[k]=i;});});
    var pcs={};T.forEach(function(t,i){if(on[i])pcs[tuf.find(i)]=1;});var np=Object.keys(pcs).length,chi=V-Ecount+F,holes=np-chi;
    ou.innerHTML='<p>꼭짓점 V = <b>'+V+'</b>, 모서리 E = <b>'+Ecount+'</b>, 삼각형 F = <b>'+F+'</b> → V − E + F = <b>'+chi+'</b></p>'+
      '<p>빨간 선 = 삼각형 하나에만 붙은 모서리(가장자리·찢어진 곳): <b>'+bd.length+'</b>개, 빨간 고리 <b>'+nl+'</b>개</p>'+
      '<p>조각 <b>'+np+'</b>개, 구멍 <b>'+holes+'</b>개 (평평한 판에서는 V − E + F = 조각 수 − 구멍 수)</p>'+
      '<p class="'+(holes===0&&np===1?'g':'a')+'">'+(holes===0&&np===1?'구멍 없는 한 조각 판이에요. 가장자리를 찢어도(모서리만 파여도) 구멍 수는 그대로예요.':'구멍이나 떨어진 조각이 있어요. 3D 프린터로 뽑기 전에 고쳐야 할 곳이에요.')+'</p>';}
  preset(o.preset||'full');
  function closed(el,o){var st={n:6,m:4,k:'torus'};
    var SOL={tetra:['정사면체',4,6,4],octa:['정팔면체',6,12,8],cube:['정육면체(삼각형으로 나눔)',8,18,12],torus:['도넛 (n × m 격자)',0,0,0],double:['손잡이 2개 도넛',10,24,12]};
    var c=ctrl(el);radio(c,'닫힌 모양:',Object.keys(SOL).map(function(k){return [k,SOL[k][0]];}),st.k,function(v){st.k=v;draw2();});
    var c2=ctrl(el);slider(c2,'도넛 격자 n',3,12,1,st.n,function(v){st.n=v;draw2();return String(v);});slider(c2,'m',3,10,1,st.m,function(v){st.m=v;draw2();return String(v);});
    var s2=svg(el,420,150,'V, E, F 막대'),ou2=out(el);
    function draw2(){var q=SOL[st.k],V=q[1],Ed=q[2],F=q[3];if(st.k==='torus'){V=st.n*st.m;Ed=3*st.n*st.m;F=2*st.n*st.m;}
      var chi=V-Ed+F,g=(2-chi)/2;s2.innerHTML='';var mx=Math.max(V,Ed,F);[['V 꼭짓점',V,C.b],['E 모서리',Ed,C.a],['F 삼각형',F,C.g]].forEach(function(b,i){var w=300*b[1]/mx;E('rect',{x:100,y:15+i*42,width:w,height:28,fill:b[2]},s2);tx(s2,10,34+i*42,b[0]);tx(s2,106+w,34+i*42,String(b[1]),{'font-weight':700});});
      ou2.innerHTML='<p>V − E + F = '+V+' − '+Ed+' + '+F+' = <b>'+chi+'</b> → 손잡이(구멍) 수 g = (2 − '+chi+') ÷ 2 = <b>'+g+'</b></p>'+
        '<p class="note">닫힌 곡면에서는 삼각형을 얼마나 잘게 나누든 V − E + F가 같아요(도넛은 n, m을 바꿔도 늘 0). 그래서 컴퓨터가 「구멍 몇 개짜리 물체인가」를 숫자 하나로 판정해요.</p>';}
    draw2();}
};

/* 4. 센서망: 통신 연결(덩어리)과 음영 지역(빈 곳) */
W.sensor=function(el,o){
  var R=rng(o.seed||21),Wd=320,Ht=220,P=[],st={r:o.r||26,mode:o.mode||'net'};for(var i=0;i<(o.n||16);i++)P.push([18+R()*(Wd-36),18+R()*(Ht-36)]);
  var c=ctrl(el);slider(c,'센서 반경',8,60,1,st.r,function(v){st.r=v;draw();return v+'m';});
  var c2=ctrl(el);btn(c2,'갇힌 음영 가운데에 센서 하나 더',function(){var h=holes();if(h.best){P.push(h.best);draw();}});btn(c2,'처음 배치로',function(){P=P.slice(0,o.n||16);draw();});
  var s=svg(el,Wd,Ht,'센서 배치와 통신 연결, 음영 지역'),ou=out(el);
  function holes(){var g=6,cols=Math.floor(Wd/g),rows=Math.floor(Ht/g),G=new Uint8Array(cols*rows);
    for(var y=0;y<rows;y++)for(var x=0;x<cols;x++){var px=x*g+g/2,py=y*g+g/2,cov=P.some(function(p){return Math.hypot(p[0]-px,p[1]-py)<=st.r;});G[y*cols+x]=cov?1:0;}
    var L=label(G,cols,rows,0,4),inner=0,edge=0,best=null,bs=0,cnt={},touch={},sx={},sy={};
    for(var i=0;i<cols*rows;i++){var k=L.lab[i];if(!k)continue;var x2=i%cols,y2=(i-x2)/cols;cnt[k]=(cnt[k]||0)+1;sx[k]=(sx[k]||0)+x2;sy[k]=(sy[k]||0)+y2;if(x2===0||y2===0||x2===cols-1||y2===rows-1)touch[k]=1;}
    var bt=0,btb=null;Object.keys(cnt).forEach(function(k){var ctr=[(sx[k]/cnt[k])*g+g/2,(sy[k]/cnt[k])*g+g/2];if(touch[k]){edge++;if(cnt[k]>bt){bt=cnt[k];btb=ctr;}}else{inner++;if(cnt[k]>bs){bs=cnt[k];best=ctr;}}});if(!best)best=btb;
    return {G:G,cols:cols,rows:rows,g:g,inner:inner,edge:edge,best:best,area:Object.keys(cnt).reduce(function(a,k){return a+cnt[k];},0)/(cols*rows)};}
  function draw(){s.innerHTML='';var h=holes();
    for(var i=0;i<h.cols*h.rows;i++)if(!h.G[i]){var x=i%h.cols,y=(i-x)/h.cols;E('rect',{x:x*h.g,y:y*h.g,width:h.g,height:h.g,fill:'#fbe3e1'},s);}
    P.forEach(function(p){E('circle',{cx:p[0],cy:p[1],r:st.r,fill:'rgba(30,85,200,.10)',stroke:'rgba(30,85,200,.35)'},s);});
    var uf=UF(P.length),ne=0;for(var a=0;a<P.length;a++)for(var b=a+1;b<P.length;b++)if(Math.hypot(P[a][0]-P[b][0],P[a][1]-P[b][1])<=2*st.r){uf.union(a,b);ne++;E('line',{x1:P[a][0],y1:P[a][1],x2:P[b][0],y2:P[b][1],stroke:C.g,'stroke-width':1.5},s);}
    var comp={};P.forEach(function(p,i){comp[uf.find(i)]=1;});var nc=Object.keys(comp).length;
    P.forEach(function(p,i){E('circle',{cx:p[0],cy:p[1],r:4,fill:i>=(o.n||16)?C.a:C.b},s);});
    ou.innerHTML='<p>센서 <b>'+P.length+'</b>개, 통신선 <b>'+ne+'</b>개 (두 원이 겹치면 연결) → 통신 덩어리 <b>'+nc+'</b>개 '+(nc===1?'<span class="g">— 모두 이어졌어요</span>':'<span class="r">— 끊긴 무리가 있어요</span>')+'</p>'+
      '<p>음영 지역(분홍): 안쪽에 갇힌 구멍 <b>'+h.inner+'</b>곳, 가장자리 빈 곳 <b>'+h.edge+'</b>곳, 빈 넓이 약 <b>'+Math.round(100*h.area)+'%</b></p>'+
      '<p class="note">'+(st.mode==='net'?'통신 덩어리는 06장의 「연결」을 그래프로 센 것이에요.':'안쪽에 갇힌 음영은 「센서망 속 구멍」이에요. 반경을 키우거나 센서를 더하면 구멍이 메워져요.')+'</p>';}
  draw();
};

/* 5. 점 구름 지속성: 원 위 점들 + 잡음, 반경 ε를 키울 때 덩어리(β₀)와 구멍(β₁) */
W.barcode=function(el,o){
  var n=o.n||18,st={noise:o.noise!=null?o.noise:0.12,eps:o.eps||0.6,seed:o.seed||5},X=[];
  function gen(){var R=rng(st.seed);X=[];for(var i=0;i<n;i++){var t=2*Math.PI*i/n+0.15*gauss(R);X.push([Math.cos(t)+st.noise*gauss(R),Math.sin(t)+st.noise*gauss(R)]);}}
  var c=ctrl(el);slider(c,'잡음 크기',0,0.5,0.01,st.noise,function(v){st.noise=v;gen();pre();draw();return v.toFixed(2);});
  var c2=ctrl(el);slider(c2,'연결 거리 ε',0,2,0.02,st.eps,function(v){st.eps=v;draw();return v.toFixed(2);});
  var s=svg(el,640,300,'점 구름과 연결선, 그리고 막대(바코드)'),ou=out(el);
  function D(a,b){return Math.hypot(X[a][0]-X[b][0],X[a][1]-X[b][1]);}
  function betti(eps){var ed=[],idx={};for(var a=0;a<n;a++)for(var b=a+1;b<n;b++)if(D(a,b)<=eps){idx[a+','+b]=ed.length;ed.push([a,b]);}
    var uf=UF(n),c0=n;ed.forEach(function(e){if(uf.union(e[0],e[1]))c0--;});
    var Ew=Math.ceil(ed.length/32)||1,piv={},rank=0;
    for(a=0;a<n;a++)for(b=a+1;b<n;b++){if(idx[a+','+b]==null)continue;for(var d=b+1;d<n;d++){if(idx[a+','+d]==null||idx[b+','+d]==null)continue;
      var v=new Uint32Array(Ew);[idx[a+','+b],idx[a+','+d],idx[b+','+d]].forEach(function(k){v[k>>5]^=(1<<(k&31))>>>0;});
      for(var w=Ew-1;w>=0;w--){while(v[w]){var hb=31-Math.clz32(v[w]),key=w*32+hb;if(piv[key]){var pv=piv[key];for(var z=0;z<Ew;z++)v[z]^=pv[z];}else{piv[key]=v;rank++;w=-1;break;}}}}}
    var b1=(ed.length-(n-c0))-rank;return {b0:c0,b1:b1,ed:ed};}
  var prof=[],h0=[];
  function pre(){prof=[];for(var k=0;k<=50;k++){var e=k*0.04;prof.push([e,betti(e).b1]);}
    var es=[];for(var a=0;a<n;a++)for(var b=a+1;b<n;b++)es.push([D(a,b),a,b]);es.sort(function(p,q){return p[0]-q[0];});var uf=UF(n);h0=[];es.forEach(function(e){if(uf.union(e[1],e[2]))h0.push(e[0]);});}
  function draw(){var B=betti(st.eps);s.innerHTML='';var cx=150,cy=150,sc=90;
    B.ed.forEach(function(e){E('line',{x1:cx+X[e[0]][0]*sc,y1:cy-X[e[0]][1]*sc,x2:cx+X[e[1]][0]*sc,y2:cy-X[e[1]][1]*sc,stroke:'rgba(19,115,58,.55)'},s);});
    X.forEach(function(p){E('circle',{cx:cx+p[0]*sc,cy:cy-p[1]*sc,r:4,fill:C.b},s);});
    var bx=320,bw=300,scx=function(e){return bx+bw*e/2;};tx(s,bx,18,'덩어리 막대 (H₀)',{fill:C.b,'font-size':12});
    var bars=h0.slice().sort(function(a,b){return b-a;}).slice(0,10);bars.forEach(function(d,i){E('line',{x1:scx(0),y1:30+i*8,x2:scx(Math.min(2,d)),y2:30+i*8,stroke:C.b,'stroke-width':4},s);});
    E('line',{x1:scx(0),y1:22,x2:scx(2),y2:22,stroke:C.b,'stroke-width':4,'stroke-dasharray':'2 2'},s);
    tx(s,bx,130,'구멍 막대 (H₁) — 구멍 수가 유지된 구간',{fill:C.r,'font-size':12});var mx=0;prof.forEach(function(p){mx=Math.max(mx,p[1]);});
    for(var k=1;k<=Math.min(mx,6);k++){var st0=null,en=null;prof.forEach(function(p){if(p[1]>=k){if(st0==null)st0=p[0];en=p[0];}});if(st0!=null)E('line',{x1:scx(st0),y1:140+k*12,x2:scx(en+0.04),y2:140+k*12,stroke:C.r,'stroke-width':5},s);}
    E('line',{x1:scx(st.eps),y1:10,x2:scx(st.eps),y2:230,stroke:C.k,'stroke-dasharray':'4 3'},s);tx(s,scx(st.eps)+4,240,'ε = '+st.eps.toFixed(2),{'font-size':11});
    [0,0.5,1,1.5,2].forEach(function(v){tx(s,scx(v)-6,262,String(v),{'font-size':10,fill:C.mu});});
    var longest=0,a0=null;for(k=1;k<=1;k++){var s0=null,e0=null;prof.forEach(function(p){if(p[1]>=1){if(s0==null)s0=p[0];e0=p[0];}});if(s0!=null)longest=e0+0.04-s0;}
    ou.innerHTML='<p>ε = '+st.eps.toFixed(2)+'에서 덩어리 β₀ = <b>'+B.b0+'</b>, 구멍 β₁ = <b>'+B.b1+'</b> (연결선 '+B.ed.length+'개)</p>'+
      '<p>구멍 막대의 길이(가장 긴 것) ≈ <b>'+longest.toFixed(2)+'</b> — '+(longest>0.5?'<span class="g">길게 버티는 구멍 = 진짜 고리 모양이에요.</span>':'<span class="a">짧게 나타났다 사라지는 구멍 = 잡음일 가능성이 커요.</span>')+'</p>'+
      '<p class="note">막대(바코드)는 ε를 0에서 2까지 키우며 「언제 생겨서 언제 사라졌나」를 그린 것이에요. 이 페이지는 점 '+n+'개의 비토리스–립스 복합체로 구멍 수를 직접 세었어요.</p>';}
  gen();pre();draw();
};

/* 6. 물 빠지기(이산 모스 생각): 땅 높이 줄에서 물 높이를 올리며 웅덩이 생김·합쳐짐 */
W.water=function(el,o){
  var h=o.h||[6,3,5,8,2,4,7,9,5,1,3,6,8,4,6,10,7,3,5,8],n=h.length,st={lv:o.lv||4.5};
  var c=ctrl(el);slider(c,'물 높이',0.5,10.5,0.5,st.lv,function(v){st.lv=v;draw();return v.toFixed(1);});
  var s=svg(el,640,260,'땅 높이 막대와 물, 그리고 웅덩이 막대'),ou=out(el);
  var order=h.map(function(v,i){return i;}).sort(function(a,b){return h[a]-h[b]||a-b;}),pairs=[],uf=UF(n),born={},act={};
  order.forEach(function(i){act[i]=1;born[i]=h[i];var nb=[i-1,i+1].filter(function(j){return j>=0&&j<n&&act[j];});
    nb.forEach(function(j){var a=uf.find(i),b=uf.find(j);if(a===b)return;var young=born[a]>born[b]?a:b,old=young===a?b:a;if(born[young]<h[i])pairs.push([born[young],h[i],young]);uf.union(young,old);});
    var r=uf.find(i);if(born[r]==null)born[r]=h[i];});
  var root=uf.find(order[0]);pairs.push([h[order[0]],Infinity,root]);
  var mins=h.filter(function(v,i){return (i===0||h[i-1]>v)&&(i===n-1||h[i+1]>v);}).length,maxs=h.filter(function(v,i){return i>0&&i<n-1&&h[i-1]<v&&h[i+1]<v;}).length;
  function draw(){s.innerHTML='';var bw=14,base=180,sc=15;
    for(var i=0;i<n;i++){var y=base-h[i]*sc;E('rect',{x:20+i*bw,y:y,width:bw-1,height:h[i]*sc,fill:'#b98b5a'},s);if(h[i]<st.lv)E('rect',{x:20+i*bw,y:base-st.lv*sc,width:bw-1,height:(st.lv-h[i])*sc,fill:'rgba(30,85,200,.45)'},s);}
    E('line',{x1:15,y1:base-st.lv*sc,x2:20+n*bw+5,y2:base-st.lv*sc,stroke:C.b,'stroke-dasharray':'4 3'},s);
    var G=h.map(function(v){return v<st.lv?1:0;}),pools=0;for(i=0;i<n;i++)if(G[i]&&(i===0||!G[i-1]))pools++;
    var bx=330;tx(s,bx,16,'웅덩이 막대: 생긴 높이 → 옆 웅덩이와 합쳐진 높이',{'font-size':12,fill:C.b});
    pairs.slice().sort(function(a,b){return a[0]-b[0];}).forEach(function(p,k){var x0=bx+p[0]*28,x1=bx+Math.min(10.5,p[1])*28;E('line',{x1:x0,y1:32+k*14,x2:x1,y2:32+k*14,stroke:p[1]===Infinity?C.k:C.b,'stroke-width':6},s);tx(s,x1+4,36+k*14,p[1]===Infinity?'끝까지':(p[1]-p[0])+'',{'font-size':10,fill:C.mu});});
    E('line',{x1:bx+st.lv*28,y1:24,x2:bx+st.lv*28,y2:200,stroke:C.k,'stroke-dasharray':'3 3'},s);
    ou.innerHTML='<p>물 높이 '+st.lv.toFixed(1)+'에서 웅덩이 <b>'+pools+'</b>개</p><p>땅 '+n+'자리 중 「중요한 자리」는 골짜기 바닥 '+mins+'곳(웅덩이가 생김) + 봉우리 '+maxs+'곳(웅덩이가 합쳐짐)뿐이에요. 나머지 자리는 웅덩이 수를 바꾸지 않아요.</p>'+
      '<p class="note">이산 모스 이론은 바로 이 생각이에요 — 모양을 바꾸지 않는 자리들은 짝지어 지우고, 중요한 자리만 남겨 계산을 크게 줄여요. 막대가 길수록 오래 버틴 깊은 웅덩이(진짜 특징), 짧을수록 얕은 잡음이에요.</p>';}
  draw();
};
})();
