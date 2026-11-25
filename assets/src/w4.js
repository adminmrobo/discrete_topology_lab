/* 위젯 모음 4: 이산위상 연구실에서 새로 만든 그림 실험
   bdry(안쪽·닫힘·경계) · basis(기저 점검) · tbl01(위상을 0/1 표로) · hsep(떼어 놓기) · nbrmat(이웃 행렬)
   mat2(2×2 행렬로 점 옮기기) · latbasis(격자의 기본 벡터와 넓이) · DUELS.expr(계산 판정) */
(function(){
'use strict';
var U=window.WU,C=window.WC,E=U.E,H=U.H,svg=U.svg,ctrl=U.ctrl,btn=U.btn,radio=U.radio,slider=U.slider,out=U.out,tx=U.tx,isTop=U.isTop,lab=U.lab,subsets=U.subsets;
function pc(m){var c=0;while(m){c+=m&1;m>>=1;}return c;}
function sortSets(a){return a.slice().sort(function(x,y){return pc(x)-pc(y)||x-y;});}
var TOPS={
  discrete:function(n){return subsets(n);},
  indiscrete:function(n){return [0,(1<<n)-1];},
  chain:function(n){var a=[0];for(var k=1;k<=n;k++)a.push((1<<k)-1);return a;},
  sier:function(n){return [0,1,(1<<n)-1];},
  split:function(n){return n===4?[0,3,12,15]:[0,1,6,7];},
  bad:function(n){return [0,1,2,(1<<n)-1];}
};
var TNAME={discrete:'이산(전부)',indiscrete:'밀착(∅와 전체)',chain:'줄 세우기',sier:'작은 예',split:'두 덩어리',bad:'규칙 깨진 예'};
function names(n){return ['1','2','3','4','5'].slice(0,n);}

/* 1. 안쪽 · 닫힘 · 경계 (점 n개의 유한 공간) */
W.bdry=function(el,o){
  var n=o.n||4,full=(1<<n)-1,nm=names(n),T=TOPS[o.preset||'chain'](n),A=o.A||3;
  var c=ctrl(el);radio(c,'위상:',(o.presets||['discrete','chain','split','indiscrete']).map(function(k){return [k,TNAME[k]];}),o.preset||'chain',function(k){T=TOPS[k](n);draw();});
  var c2=ctrl(el);H('span','glabel','집합 A에 넣을 점:',c2);
  var bs=nm.map(function(x,i){return btn(c2,'점 '+x,function(){A^=(1<<i);draw();},!!(A>>i&1));});
  var s=svg(el,640,130,'점 '+n+'개 위의 집합 A와 그 안쪽, 닫힘, 경계'),ou=out(el);
  function interior(S){var r=0;T.forEach(function(m){if((m&S)===m)r|=m;});return r;}
  function closure(S){return full&~interior(full&~S);}
  function draw(){bs.forEach(function(b,i){b.setAttribute('aria-pressed',A>>i&1?'true':'false');});
    var I=interior(A),Cl=closure(A),B=Cl&~I;s.innerHTML='';
    for(var i=0;i<n;i++){var x=80+i*(480/(n-1||1)),inI=I>>i&1,inB=B>>i&1,inA=A>>i&1;
      E('circle',{cx:x,cy:60,r:24,fill:inI?'#e7f5ec':inB?'#fdf3e1':'#fff',stroke:inI?C.g:inB?C.a:C.mu,'stroke-width':inA?4:2,'stroke-dasharray':inA?'':'5 4'},s);
      tx(s,x-5,66,nm[i],{'font-weight':700});tx(s,x-22,112,inI?'안쪽':inB?'경계':'바깥',{fill:inI?C.g:inB?C.a:C.mu});}
    var open=T.indexOf(A)>=0,closed=T.indexOf(full&~A)>=0;
    ou.innerHTML='<p>열린 집합 목록: '+sortSets(T).map(function(m){return lab(m,n,nm);}).join(', ')+'</p>'+
      '<p>A = <b>'+lab(A,n,nm)+'</b> → 안쪽(A 속에 들어가는 열린 집합을 모두 합친 것) = <b class="g">'+lab(I,n,nm)+'</b>, 닫힘(A를 감싸는 가장 작은 닫힌 집합) = <b>'+lab(Cl,n,nm)+'</b>, 경계 = 닫힘 − 안쪽 = <b class="a">'+lab(B,n,nm)+'</b></p>'+
      '<p>A는 '+(open?'열린 집합':'열린 집합이 아님')+', '+(closed?'닫힌 집합':'닫힌 집합이 아님')+(open&&closed?' → <b>열리면서 닫힌 집합</b>이라 경계가 비어 있어요.':'.')+'</p>';}
  draw();
};

/* 2. 기저 점검기: 블록 모음이 기저인가 (느슨한 문장 vs 정확한 조건) */
W.basis=function(el,o){
  var n=4,nm=names(n),full=15,on={};
  var P={single:[1,2,4,8],interval:[3,6,12,2,4],trap:[7,14,4],gap:[3,6]};
  var PN={single:'1인실 블록',interval:'겹치는 구간 블록',trap:'함정 블록',gap:'빠진 점 있음'};
  function preset(k){on={};P[k].forEach(function(m){on[m]=1;});draw();}
  var c=ctrl(el);H('span','glabel','미리 정한 블록:',c);Object.keys(P).forEach(function(k){btn(c,PN[k],function(){preset(k);});});
  var g=ctrl(el);g.setAttribute('role','group');g.setAttribute('aria-label','블록 고르기');
  var bs=sortSets(subsets(n).filter(function(m){return m;})).map(function(m){var b=btn(g,lab(m,n,nm),function(){on[m]=!on[m];draw();},false);b.dataset.m=m;return b;});
  var ou=out(el);
  function draw(){var B=Object.keys(on).filter(function(k){return on[k];}).map(Number);
    bs.forEach(function(b){b.setAttribute('aria-pressed',on[+b.dataset.m]?'true':'false');});
    var cov=0;B.forEach(function(m){cov|=m;});var r1=cov===full;
    var loose=true,exact=true,badL=null,badE=null;
    B.forEach(function(a){B.forEach(function(b){if(a>=b)return;var I=a&b;if(!I)return;
      var some=B.some(function(m){return m!==a&&m!==b&&(m&I)===m;})||B.some(function(m){return m===I;});if(!some){loose=false;badL=badL||[a,b];}
      for(var i=0;i<n;i++)if(I>>i&1){var ok=B.some(function(m){return (m>>i&1)&&(m&I)===m;});if(!ok){exact=false;badE=badE||[a,b,i];}}});});
    var U={0:1};B.forEach(function(m){Object.keys(U).map(Number).forEach(function(u){U[u|m]=1;});});
    var T=Object.keys(U).map(Number);if(r1)U[full]=1;T=Object.keys(U).map(Number);var t=isTop(T,n),top=t.r1&&t.r2&&t.r3;
    var h='<p class="'+(r1?'g':'r')+'">조건 ① 모든 점이 어떤 블록에 들어 있다: '+(r1?'통과':'실패 — 빠진 점 '+nm.filter(function(x,i){return !(cov>>i&1);}).join(', '))+'</p>';
    h+='<p class="'+(loose?'g':'r')+'">(원자료의 느슨한 문장) 두 블록의 겹친 곳이 다른 블록 하나를 품는다: '+(loose?'통과':'실패 — '+lab(badL[0],n,nm)+' ∩ '+lab(badL[1],n,nm))+'</p>';
    h+='<p class="'+(exact?'g':'r')+'">조건 ② (정확한 조건) 겹친 곳의 <b>점마다</b>, 그 점을 담고 겹친 곳 안에 들어가는 블록이 있다: '+(exact?'통과':'실패 — '+lab(badE[0],n,nm)+' ∩ '+lab(badE[1],n,nm)+'의 점 '+nm[badE[2]]+'을 담는 블록이 그 안에 없음')+'</p>';
    h+='<p>블록을 합쳐 만든 집합 '+T.length+'개: '+sortSets(T).map(function(m){return lab(m,n,nm);}).join(', ')+'</p>';
    h+='<p class="'+(top?'g':'a')+'">→ '+(top?'세 규칙을 지키는 위상이 돼요. 이 블록들은 기저예요.':'위상이 되지 않아요'+(t.b3?' (겹친 곳 '+lab(t.b3[0]&t.b3[1],n,nm)+'이 목록에 없음)':'')+'.')+'</p>';
    if(loose&&!exact)h+='<p class="a"><b>함정 발견:</b> 느슨한 문장은 통과했지만 정확한 조건은 실패했어요. 원자료의 문장만 믿으면 기저가 아닌 것을 기저라고 착각해요.</p>';
    ou.innerHTML=h;}
  preset(o.preset||'interval');
};

/* 3. 위상을 0/1 표로: 행 = 열린 집합, 열 = 점. 두 행의 OR(합집합) · AND(교집합) */
W.tbl01=function(el,o){
  var n=o.n||3,nm=names(n),T=TOPS[o.preset||'chain'](n),pick=[];
  var c=ctrl(el);radio(c,'위상:',(o.presets||['chain','sier','discrete','bad']).map(function(k){return [k,TNAME[k]];}),o.preset||'chain',function(k){T=TOPS[k](n);pick=[];draw();});
  var box=H('div','tw',null,el),ou=out(el);
  function row(m){return nm.map(function(x,i){return m>>i&1;});}
  function draw(){var S=sortSets(T);
    var h='<table class="m01"><thead><tr><th>열린 집합 \\ 점</th>'+nm.map(function(x){return '<th>'+x+'</th>';}).join('')+'<th>고르기</th></tr></thead><tbody>';
    S.forEach(function(m){var sel=pick.indexOf(m)>=0;h+='<tr><th>'+lab(m,n,nm)+'</th>'+row(m).map(function(v){return '<td class="'+(v?'on':'')+(sel?' hot':'')+'">'+v+'</td>';}).join('')+
      '<td><button type="button" class="bt" data-m="'+m+'" aria-pressed="'+sel+'">'+(sel?'골랐음':'고르기')+'</button></td></tr>';});
    box.innerHTML=h+'</tbody></table>';
    [].forEach.call(box.querySelectorAll('button[data-m]'),function(b){b.onclick=function(){var m=+b.dataset.m,i=pick.indexOf(m);if(i>=0)pick.splice(i,1);else{pick.push(m);if(pick.length>2)pick.shift();}draw();};});
    var t=isTop(T,n),r='<p>표의 크기: 가로줄(행) '+S.length+'개 × 세로줄(열) '+n+'개. 가로줄 하나가 「0과 1로 쓴 열린 집합 하나」예요.</p>';
    if(pick.length===2){var a=pick[0],b=pick[1],or=a|b,and=a&b;
      r+='<p>고른 두 줄: ['+row(a).join(' ')+'] 와 ['+row(b).join(' ')+']</p>';
      r+='<p>자리마다 「하나라도 1이면 1」(합집합, OR) → ['+row(or).join(' ')+'] = '+lab(or,n,nm)+' — '+(T.indexOf(or)>=0?'<span class="g">표에 있음</span>':'<span class="r">표에 없음 → 규칙 2 위반</span>')+'</p>';
      r+='<p>자리마다 「둘 다 1이어야 1」(교집합, AND) → ['+row(and).join(' ')+'] = '+lab(and,n,nm)+' — '+(T.indexOf(and)>=0?'<span class="g">표에 있음</span>':'<span class="r">표에 없음 → 규칙 3 위반</span>')+'</p>';}
    else r+='<p class="note">「고르기」로 두 줄을 골라 보세요. 두 줄을 자리마다 비교해 합집합·교집합 줄을 만들어 줘요.</p>';
    r+='<p class="'+(t.r1&&t.r2&&t.r3?'g':'r')+'">세 규칙 점검: '+(t.r1&&t.r2&&t.r3?'통과 — 이 표는 위상이에요.':'실패 — 이 표는 위상이 아니에요.')+'</p>';
    ou.innerHTML=r;}
  draw();
};

/* 4. 떼어 놓기: 점 x0와 집합 Y를 겹치지 않는 동네로 */
W.hsep=function(el,o){
  var st={mode:o.mode||'finite',x0:0.05,N:5},Yf=[0.3,0.48,0.66,0.9];
  var s=svg(el,640,190,'수직선 위의 점 x0와 집합 Y, 그리고 둘을 떼어 놓는 동네들');
  var c=ctrl(el);radio(c,'집합 Y:',[['finite','점 4개 (유한)'],['seq','1, 1/2, 1/3, … (끝없음)']],st.mode,function(v){st.mode=v;sync();draw();});
  var c2=ctrl(el),sl=slider(c2,'x0의 자리',0,0.25,0.01,st.x0,function(v){st.x0=v;draw();return v.toFixed(2);});
  var c3=ctrl(el),sn=slider(c3,'Y에서 본 점 수 N',1,200,1,st.N,function(v){st.N=v;draw();return String(v);});
  var ou=out(el);
  function sync(){c2.style.display=st.mode==='finite'?'':'none';c3.style.display=st.mode==='seq'?'':'none';}
  function X(v){return 40+v*560;}
  function draw(){s.innerHTML='';var x0=st.mode==='seq'?0:st.x0,Y=st.mode==='seq'?[]:Yf;
    if(st.mode==='seq')for(var k=1;k<=st.N;k++)Y.push(1/k);
    E('line',{x1:20,y1:110,x2:620,y2:110,stroke:C.mu,'stroke-width':2},s);
    var rmin=Infinity;Y.forEach(function(y,i){var r=Math.abs(y-x0)/2;rmin=Math.min(rmin,r);
      if(i<12){E('rect',{x:X(y-r),y:118+(i%3)*10,width:r*2*560,height:6,fill:'rgba(30,85,200,.25)'},s);}
      E('circle',{cx:X(y),cy:110,r:Y.length>40?2:5,fill:C.b},s);});
    E('rect',{x:X(x0-rmin),y:76,width:Math.max(1,rmin*2*560),height:14,fill:'rgba(19,115,58,.3)',stroke:C.g},s);
    E('circle',{cx:X(x0),cy:110,r:6,fill:C.r},s);tx(s,X(x0)-8,100,'x0',{fill:C.r,'font-weight':700});
    tx(s,X(x0)+10,70,'x0의 동네 (반지름 '+rmin.toFixed(4)+')',{fill:C.g});tx(s,430,170,'파란 막대: Y의 점마다 잡은 동네',{fill:C.b,'font-size':12});
    var h='<p>Y의 점마다 「x0까지 거리의 절반」을 반지름으로 동네를 잡으면, x0 쪽 동네와 Y 쪽 동네가 겹치지 않아요.</p>';
    h+='<p>x0 쪽 동네를 모두 겹친 곳 = 반지름이 가장 작은 것 = <b>'+rmin.toFixed(4)+'</b></p>';
    if(st.mode==='finite')h+='<p class="g">Y의 점이 유한 개(4개)라 가장 작은 반지름도 0보다 커요. x0를 Y에서 떼어 놓는 데 성공! → x0는 Y의 닫힘 밖, Y는 닫힌 집합.</p>';
    else h+='<p class="a">N개만 보면 반지름 1/(2N) = '+(1/(2*st.N)).toFixed(4)+'. N을 끝없이 키우면 0으로 줄어요. 0은 Y에 없지만 Y에서 떼어 놓을 수 없어요 → Y는 닫힌 집합이 아니고, 그래서 콤팩트도 아니에요. (Y에 0을 더한 집합은 콤팩트예요.)</p>';
    ou.innerHTML=h;}
  sync();draw();
};

/* 5. 이웃 행렬: M[p][q]=1 ⇔ q가 p의 가장 작은 이웃 O_p에 들어 있음 */
W.nbrmat=function(el,o){
  var n=4,nm=o.names||['1','2','3','4'];
  var P={discrete:[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],indiscrete:[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]],
    kh:[[1,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,1,1]],chain:[[1,0,0,0],[1,1,0,0],[1,1,1,0],[1,1,1,1]],broken:[[1,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,1]]};
  var PN={discrete:'이산 (단위행렬)',indiscrete:'밀착 (전부 1)',kh:'칼림스키 조각',chain:'줄 세우기',broken:'규칙 깨진 예'};
  var M=JSON.parse(JSON.stringify(P[o.preset||'kh']));
  var c=ctrl(el);radio(c,'미리 정한 표:',Object.keys(P).map(function(k){return [k,PN[k]];}),o.preset||'kh',function(k){M=JSON.parse(JSON.stringify(P[k]));draw();});
  var box=H('div','tw',null,el),ou=out(el);
  function draw(){var h='<table class="m01"><thead><tr><th>p \\ q</th>'+nm.map(function(x){return '<th>'+x+'</th>';}).join('')+'<th>O_p (p의 가장 작은 이웃)</th></tr></thead><tbody>';
    for(var p=0;p<n;p++){h+='<tr><th>'+nm[p]+'</th>';for(var q=0;q<n;q++)h+='<td class="'+(M[p][q]?'on':'')+'"><button type="button" data-p="'+p+'" data-q="'+q+'" aria-label="'+nm[p]+'행 '+nm[q]+'열, 지금 '+M[p][q]+'">'+M[p][q]+'</button></td>';
      h+='<td>{'+nm.filter(function(x,q){return M[p][q];}).join(', ')+'}</td></tr>';}
    box.innerHTML=h+'</tbody></table>';
    [].forEach.call(box.querySelectorAll('button[data-p]'),function(b){b.onclick=function(){var p=+b.dataset.p,q=+b.dataset.q;M[p][q]=M[p][q]?0:1;draw();var nb=box.querySelector('button[data-p="'+p+'"][data-q="'+q+'"]');if(nb)nb.focus();};});
    var refl=true,bd=null;for(var i=0;i<n;i++)if(!M[i][i]){refl=false;bd=bd==null?i:bd;}
    var trans=true,bt=null;for(var p2=0;p2<n;p2++)for(var q2=0;q2<n;q2++)if(M[p2][q2])for(var r=0;r<n;r++)if(M[q2][r]&&!M[p2][r]){trans=false;bt=bt||[p2,q2,r];}
    var anti=true;for(var a=0;a<n;a++)for(var b2=a+1;b2<n;b2++)if(M[a].join()===M[b2].join())anti=false;
    var t='<p class="'+(refl?'g':'r')+'">규칙 ① 대각선이 모두 1 (자기 이웃엔 자기가 있다): '+(refl?'통과':'실패 — '+nm[bd]+'행 '+nm[bd]+'열이 0')+'</p>';
    t+='<p class="'+(trans?'g':'r')+'">규칙 ② q가 p의 이웃이면 q의 이웃 줄이 p의 줄 안에 들어간다: '+(trans?'통과':'실패 — '+nm[bt[1]]+'∈O_'+nm[bt[0]]+', '+nm[bt[2]]+'∈O_'+nm[bt[1]]+'인데 '+nm[bt[2]]+'∉O_'+nm[bt[0]])+'</p>';
    t+='<p>'+(refl&&trans?'<span class="g">이 표는 알렉산드로프 공간 하나를 정해요.</span> '+(anti?'줄이 모두 달라서 점들이 서로 구별돼요(T0) → 순서 그림(부분순서)으로 그릴 수 있어요.':'똑같은 줄이 있어요 → 그 점들은 구별이 안 돼요. 순서가 아니라 「준순서」예요.'):'<span class="r">두 규칙을 지켜야 「가장 작은 이웃」 표가 돼요.</span>')+'</p>';
    ou.innerHTML=t+'<p class="note">표의 자리를 눌러 0과 1을 바꿔 보세요. 이산 위상은 대각선만 1인 표(단위행렬), 밀착 위상은 전부 1인 표예요.</p>';}
  draw();
};

/* 6. 2×2 행렬로 점 옮기기 (작용·궤도) */
W.mat2=function(el,o){
  var PM={id:[[1,0],[0,1]],rot:[[0,-1],[1,0]],flip:[[-1,0],[0,1]],stretch:[[2,0],[0,0.5]],shear:[[1,1],[0,1]]};
  var PN={id:'그대로 (단위행렬)',rot:'90° 돌리기',flip:'좌우 뒤집기',stretch:'가로 2배 · 세로 절반',shear:'옆으로 밀기'};
  var st={m:o.preset||'rot',x:o.x!=null?o.x:2,y:o.y!=null?o.y:1,k:o.k||4};
  var c=ctrl(el);radio(c,'행렬:',(o.presets||['rot','flip','stretch','shear','id']).map(function(k){return [k,PN[k]];}),st.m,function(k){st.m=k;draw();});
  var c2=ctrl(el);slider(c2,'점 P의 x',-3,3,1,st.x,function(v){st.x=v;draw();return String(v);});slider(c2,'y',-3,3,1,st.y,function(v){st.y=v;draw();return String(v);});
  var c3=ctrl(el);slider(c3,'몇 번 찍을까',1,8,1,st.k,function(v){st.k=v;draw();return v+'번';});
  var s=svg(el,420,420,'좌표평면 위 점 P와 행렬로 옮긴 점들'),ou=out(el);
  var S=30,O=210;function X(v){return O+v*S;}function Y(v){return O-v*S;}
  function mul(A,p){return [A[0][0]*p[0]+A[0][1]*p[1],A[1][0]*p[0]+A[1][1]*p[1]];}
  function f(v){return Math.abs(v-Math.round(v))<1e-9?String(Math.round(v)):v.toFixed(3).replace(/0+$/,'');}
  function draw(){s.innerHTML='';for(var g=-6;g<=6;g++){E('line',{x1:X(g),y1:Y(-6.5),x2:X(g),y2:Y(6.5),stroke:g?'#eef1f4':C.mu},s);E('line',{x1:X(-6.5),y1:Y(g),x2:X(6.5),y2:Y(g),stroke:g?'#eef1f4':C.mu},s);}
    var A=PM[st.m],p=[st.x,st.y],pts=[p],det=A[0][0]*A[1][1]-A[0][1]*A[1][0];
    for(var i=0;i<st.k;i++){p=mul(A,p);pts.push(p);}
    var seen={},back=-1;pts.forEach(function(q,i){var key=f(q[0])+','+f(q[1]);if(i&&key===f(pts[0][0])+','+f(pts[0][1])&&back<0)back=i;});
    for(var j=1;j<pts.length;j++){var a=pts[j-1],b=pts[j];E('line',{x1:X(a[0]),y1:Y(a[1]),x2:X(b[0]),y2:Y(b[1]),stroke:C.a,'stroke-width':1.5,'stroke-dasharray':'4 3'},s);}
    pts.forEach(function(q,i){var vis=Math.abs(q[0])<=6.5&&Math.abs(q[1])<=6.5;if(!vis)return;E('circle',{cx:X(q[0]),cy:Y(q[1]),r:i?5:7,fill:i?C.b:C.r},s);tx(s,X(q[0])+7,Y(q[1])-6,i?String(i):'P',{'font-size':12,fill:i?C.b:C.r});});
    var A0=A,p0=[st.x,st.y],q1=mul(A0,p0);
    ou.innerHTML='<p>행렬 <b>[['+A[0].map(f).join(', ')+'], ['+A[1].map(f).join(', ')+']]</b> 을 점 P = ('+st.x+', '+st.y+')에 곱하면:</p>'+
      '<p>새 x = '+f(A[0][0])+'×'+st.x+' + '+f(A[0][1])+'×'+st.y+' = <b>'+f(q1[0])+'</b>, 새 y = '+f(A[1][0])+'×'+st.x+' + '+f(A[1][1])+'×'+st.y+' = <b>'+f(q1[1])+'</b></p>'+
      '<p>찍은 자리들(궤도의 일부): '+pts.map(function(q){return '('+f(q[0])+', '+f(q[1])+')';}).join(' → ')+'</p>'+
      '<p>행렬식(넓이가 몇 배가 되나) = '+f(A[0][0])+'×'+f(A[1][1])+' − '+f(A[0][1])+'×'+f(A[1][0])+' = <b>'+f(det)+'</b> → '+(det!==0?'<span class="g">0이 아니라 되돌릴 수 있는 움직임이에요(군의 원소가 될 수 있음).</span>':'<span class="r">0이라 되돌릴 수 없어요.</span>')+'</p>'+
      (back>0?'<p class="g">'+back+'번 찍으니 P로 돌아왔어요. 궤도가 유한 개(점 '+back+'개)예요.</p>':(st.x===0&&st.y===0?'<p class="a">원점 (0, 0)은 어떤 행렬을 곱해도 그대로예요 → 모든 도장이 원점을 고정(안정자가 전체).</p>':'<p class="a">'+st.k+'번 안에는 P로 돌아오지 않았어요.</p>'));}
  draw();
};

/* 7. 격자의 기본 벡터와 넓이 = |행렬식| */
W.latbasis=function(el,o){
  var PB={std:[1,0,0,1],skew:[1,0,1,1],other:[2,1,1,1],half:[2,0,0,1],flat:[1,1,2,2]};
  var PN={std:'(1,0)과 (0,1)',skew:'(1,0)과 (1,1)',other:'(2,1)과 (1,1)',half:'(2,0)과 (0,1)',flat:'(1,1)과 (2,2)'};
  var v=(PB[o.preset||'std']).slice();
  var c=ctrl(el);radio(c,'기본 벡터:',Object.keys(PB).map(function(k){return [k,PN[k]];}),o.preset||'std',function(k){v=PB[k].slice();upd();});
  var c2=ctrl(el),r=[];['u의 x','u의 y','v의 x','v의 y'].forEach(function(nm,i){r.push(slider(c2,nm,-3,3,1,v[i],function(x){v[i]=x;draw();return String(x);}));});
  function upd(){r.forEach(function(e,i){e.value=v[i];e.dispatchEvent(new Event('input'));});}
  var s=svg(el,420,420,'두 기본 벡터로 만든 격자와 기본 평행사변형'),ou=out(el);
  var S=30,O=210;function X(x){return O+x*S;}function Y(y){return O-y*S;}
  function draw(){s.innerHTML='';var det=v[0]*v[3]-v[1]*v[2],hit={};
    for(var gx=-6;gx<=6;gx++)for(var gy=-6;gy<=6;gy++)E('circle',{cx:X(gx),cy:Y(gy),r:2.5,fill:'#c9d1d9'},s);
    if(det!==0)for(var m=-14;m<=14;m++)for(var n=-14;n<=14;n++){var px=m*v[0]+n*v[2],py=m*v[1]+n*v[3];if(Math.abs(px)<=6&&Math.abs(py)<=6){hit[px+','+py]=1;E('circle',{cx:X(px),cy:Y(py),r:5,fill:C.b},s);}}
    E('polygon',{points:[[0,0],[v[0],v[1]],[v[0]+v[2],v[1]+v[3]],[v[2],v[3]]].map(function(p){return X(p[0])+','+Y(p[1]);}).join(' '),fill:'rgba(163,92,0,.22)',stroke:C.a,'stroke-width':2},s);
    E('line',{x1:X(0),y1:Y(0),x2:X(v[0]),y2:Y(v[1]),stroke:C.r,'stroke-width':3},s);E('line',{x1:X(0),y1:Y(0),x2:X(v[2]),y2:Y(v[3]),stroke:C.g,'stroke-width':3},s);
    tx(s,X(v[0])+4,Y(v[1])-4,'u',{fill:C.r,'font-weight':700});tx(s,X(v[2])+4,Y(v[3])-4,'v',{fill:C.g,'font-weight':700});
    var tot=169,k=Object.keys(hit).length;
    ou.innerHTML='<p>u = ('+v[0]+', '+v[1]+'), v = ('+v[2]+', '+v[3]+') → 행렬 [['+v[0]+', '+v[2]+'], ['+v[1]+', '+v[3]+']]의 행렬식 = '+v[0]+'×'+v[3]+' − '+v[2]+'×'+v[1]+' = <b>'+det+'</b></p>'+
      (det===0?'<p class="r">행렬식이 0 — 두 벡터가 한 줄 위에 있어 평행사변형이 납작해요. 바닥을 덮는 타일이 되지 못해요.</p>':
      '<p>주황 타일(기본 평행사변형)의 넓이 = |행렬식| = <b>'+Math.abs(det)+'</b>. 그림 안 정수 점 '+tot+'개 중 파란 격자점 '+k+'개.</p>'+
      (Math.abs(det)===1?'<p class="g">넓이 1 → 모든 정수 점을 빠짐없이 닿아요. 모양은 달라도 (1,0)·(0,1)과 <b>같은 격자</b>예요.</p>':'<p class="a">넓이 '+Math.abs(det)+' → 정수 점 가운데 대략 '+Math.abs(det)+'개에 1개만 닿아요. 더 성긴 격자(부분 격자)예요.</p>'));}
  draw();
};

/* 계산 판정: 페이지 데이터의 duel.calc = {expr, fly, robo, fmt} */
DUELS.expr=function(){var c=(window.PAGE&&PAGE.duel&&PAGE.duel.calc)||{};var v;try{v=Function('"use strict";return ('+c.expr+');')();}catch(e){v=NaN;}
  function same(a,b){return typeof a==='number'&&typeof b==='number'?Math.abs(a-b)<1e-9:String(a)===String(b);}
  return {fly:same(v,c.fly),robo:same(v,c.robo),report:String(c.fmt||'계산 결과: {v}').replace(/\{v\}/g,'<b>'+v+'</b>')};};
})();
