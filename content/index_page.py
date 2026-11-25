"""오리엔테이션(목차) 페이지 조립"""
import os, json

FORMAT_NOTE = {
    '첫 강의 + 쪽지시험': '박사의 짧은 강의 뒤 퀴즈로 바로 점검',
    '1:1 토론': '두 인턴이 서로 다른 편을 맡아 맞붙고, 조교가 근거를 실험으로 점검',
    '찬반 토론': '1조 「픽셀조」와 2조 「바람조」가 찬성·반대를 맡아 토론',
    '조별 과제': '두 조가 같은 과제를 다른 방법으로 풀어 비교',
    '조별 토론': '조마다 한 가지 주장을 맡아 토론 후 결론 정리',
    '계산배틀': '조교 둘이 숫자로 승부, 수강생은 손계산으로 검산',
    '발표수업': '한 조가 발표하고 다른 조가 질문',
    '발표 + 질의응답': '한 사람이 증명이나 결과를 발표하고, 질문에 실험으로 답함',
    '역할극 수업': '수강생이 「도장」(군의 원소)이 되어 직접 움직여 보기',
    '쪽지시험 + 졸업 발표': '기말 쪽지시험과 수강생 여섯의 한 줄 발표',
    '코딩 체험 (활용 편)': '그림 실험 뒤, 같은 계산을 파이썬 노트북으로 실행해 보기 (코드는 접혀 있어 몰라도 됨)',
}
FMT_KEY = {'1:1 토론 + 계산': '1:1 토론', '조별 과제 + 코딩 체험': '코딩 체험 (활용 편)', '찬반 토론 + 코딩 체험': '코딩 체험 (활용 편)', '계산배틀 + 코딩 체험': '코딩 체험 (활용 편)', '조별 발표 + 코딩 체험': '코딩 체험 (활용 편)', '1:1 토론 + 코딩 체험 (졸업 과제)': '코딩 체험 (활용 편)'}

TOPICS = {1: '점과 이웃', 2: '공간의 성질', 3: '움직임', 4: '끝과 보편', 5: '활용 편', 0: '종합'}


def build(B, chs):
    esc, img, says, rich = B.esc, B.img, B.says, B.rich
    B.GLOSS = {'이산 위상': '모든 부분집합이 열린 집합인 위상. 점 하나하나가 혼자 떨어진 섬이다.',
               '위상': '「누가 누구 근처인가」를 정한 열린 집합 목록. 세 규칙을 지켜야 한다.'}
    n = len(chs)
    o = [B.head(B.SERIES + ' · 오리엔테이션', '중학생도 따라오는 이산 위상 %d장 + 실전 연습장. 박사 선생님과 조교 둘, 수강생 여섯이 함께하는 연구실 해설 시리즈. 행렬·벡터를 처음 배우는 분을 위한 「첫걸음」 상자 포함.' % n)]
    o.append('<nav class="top" aria-label="목차"><a class="logo" href="index.html">이산위상 연구실</a><a href="#three">3줄 요약</a><a href="#cast">등장인물</a><a href="#pillars">네 기둥 · 활용</a><a href="#tracks">과정</a><a href="#toc">목차</a><a href="#how">수업 방식</a><a href="practice/index.html">실전 연습장</a></nav><div id="prog"></div>')
    o.append(B.cover_html('cover_00', '이산위상 연구실', '오리엔테이션 · 00', '점 하나하나가 섬인 세상 — %d장 + 실전 연습장' % n, '이산위상 연구실 표지 — 픽셀 열지도 위로 매끈한 바람길이 흐르는 풍동 앞의 조수 하루',
                            chars=[('doc', 'front'), ('asst', 'smile'), ('sia', 'smile'), ('moa', 'smile')]))
    o.append(f'''<header class="hero"><div class="wrap"><div class="kicker">연구실 해설 시리즈 · 이산 위상 · 심화·세분판</div><h1>이산위상 연구실 — 점 하나하나가 섬인 세상</h1>
<p class="q">핵심 질문 — 「모든 점이 혼자 떨어져 있다」는 가장 단순한 위상이, 왜 수학 곳곳의 재료가 될까?</p>
<p>[[이산 위상]]은 모든 점이 섬처럼 따로 떨어진 공간이에요. 너무 단순해서 반례로만 쓰일 것 같지만, 픽셀 그림, 타일 무늬, 나선형 덮개, 무한의 끝까지 곳곳에서 출발점이 돼요. 이 시리즈는 인포그래픽 20장의 내용을 {n}개의 짧은 장(장마다 2단계, 15~20분)으로 나눠, 그림을 직접 움직이며 배우게 만든 수업입니다.</p>
<div class="kpis"><div class="kpi g"><b>{n}장</b><span>한 장에 2단계, 15~20분</span></div><div class="kpi m"><b>4기둥</b><span>이웃 · 성질 · 움직임 · 끝</span></div><div class="kpi a"><b>{n}편</b><span>장마다 「하루의 몰래 4컷」</span></div><div class="kpi r"><b>5장 + 노트북 5개</b><span>활용 편 (TDA · 영상 · 메시 · 센서망)</span></div></div>''' + says([('doc', 'front', '안녕하세요, 이 연구실의 선생님 박사입니다. 행렬이나 벡터를 처음 보는 분도 괜찮아요. 처음 나올 때마다 「첫걸음」 상자에서 숫자 줄과 숫자 표부터 천천히 시작해요.'),
                                                                                                                                                                       ('asst', 'smile', '수식이 나오면 제가 먼저 손을 들게요. 같이 가요!')]) + '</div></header>')
    o.append('''<div class="wrap"><div class="three" id="three"><h2>처음 오신 분께 — 이 시리즈를 3줄로</h2><ol>
<li><b>무엇을:</b> 이웃을 정하는 규칙(위상)과 그 가장 촘촘한 끝인 이산 위상을, 네 기둥(점과 이웃 · 공간의 성질 · 움직임 · 끝과 보편)으로 배웁니다.</li>
<li><b>왜 중요한가:</b> 컴퓨터 속 데이터(픽셀, 목록, 나머지 계산)는 기본적으로 「따로 떨어진 점들」이에요. 그 위에서 연결·연속·대칭을 정확히 말하는 언어가 이산 위상이에요.</li>
<li><b>생활·현장에서는:</b> 사진 속 물체 세기, CT 영상의 혈관 잇기, 3D 모델의 구멍 찾기, 센서망의 음영 지역 찾기, 점 구름의 위상 데이터 분석(TDA)에 바로 쓰여요. 25~29장 「활용 편」에서 파이썬 노트북까지 다뤄요.</li></ol>
<p class="note"><b>어려우면 쉬운 길부터:</b> 모든 장 맨 앞에 「하루의 몰래 4컷」과 5분짜리 쉬운 길이 있어요. 이론(수식·행렬)은 접어 두었으니, 시아·모아처럼 머리가 아프면 펼치지 않고 지나가도 괜찮아요.</p>
<p class="note">각 장은 독립적으로 읽을 수 있지만 순서대로 읽으면 가장 편해요. 수식 상자를 건너뛰어도 그림 실험과 비유로 본문을 따라올 수 있어요.</p></div></div>''')
    castl = ''.join('<div>%s<div><span class="role">%s</span><b>%s</b><span>%s</span></div></div>' % (img(w, B.PEOPLE[w][2], cls=''), esc(B.PEOPLE[w][1]), esc(B.PEOPLE[w][0]), esc(B.PEOPLE[w][3]))
                    for w in ['doc', 'fly', 'robo', 'sia', 'moa', 'asst', 'x1', 'x2', 'x3'])
    g1 = ''.join(img(w, 'e13', cls='') for w in ['sia', 'asst', 'x1'])
    g2 = ''.join(img(w, 'e13', cls='') for w in ['moa', 'x2', 'x3'])
    o.append(f'''<section class="level" id="cast"><div class="wrap"><h2>등장인물 — 선생님 1명, 조교 2명, 수강생 6명</h2><div class="cast">{castl}</div>
<div class="groups"><div>{g1} <b>1조 「픽셀조」</b> 시아 · 하루 · X1</div><div>{g2} <b>2조 「바람조」</b> 모아 · X2 · X3</div></div>
<p class="note">조 이름은 이 연구실 표지에서 왔어요. 네모난 픽셀(이산)과 그 위를 매끈하게 흐르는 바람길(연속) — 이산과 연속의 만남이 이 시리즈의 큰 그림이에요.</p></div></section>''')
    pill = []
    for p in (1, 2, 3, 4, 5):
        items = ''.join('<li><a href="%s.html">%02d %s</a></li>' % (c['slug'], c['no'], esc(c['title'])) for c in chs if c.get('pillar') == p)
        pill.append('<div><b>%s · %s</b><ul>%s</ul></div>' % ('기둥 %d' % p if p < 5 else '덧붙임', TOPICS[p], items))
    fin = [c for c in chs if c.get('pillar') == 0]
    if fin:
        pill.append('<div><b>종합</b><ul>%s</ul></div>' % ''.join('<li><a href="%s.html">%02d %s</a></li>' % (c['slug'], c['no'], esc(c['title'])) for c in fin))
    o.append('''<section class="level" id="pillars"><div class="wrap"><h2>네 기둥과 활용 편 — 이 시리즈의 큰 그림</h2>
<p>원자료 인포그래픽은 이산 위상 아래 세 기둥(공간 분류 · 대수적 작용 · 범주적 보편)을 세웠어요. 이 연구실은 첫 기둥이 너무 커서 「점과 이웃」과 「공간의 성질」 둘로 나눠, 네 기둥으로 걸어요. 그 뒤 「활용 편」 다섯 장에서 배운 것을 실제 데이터(사진·CT·3D 메시·센서망·점 구름)에 써 봐요.</p>
<div class="steps">''' + ''.join(pill) + '''</div>
<details><summary>원자료 인포그래픽 보기 (영어 그림)</summary><img loading="lazy" src="img/source/src01.webp" width="1280" height="714" alt="이산 위상의 구조 — 세 기둥 개요 인포그래픽"></details>
</div></section>''')
    cards = ''.join('<a href="%s.html"><span class="n">%02d · %s</span><b>%s</b><span>%s</span><span class="fmt">%s</span></a>' % (
        c['slug'], c['no'], (('기둥 %d' % c['pillar'] if c['pillar'] < 5 else '활용 편') if c.get('pillar') else '종합') + ' · ' + B.STARS[B.LEVEL[c['no']]].split(' ')[0] + ' · 약 %d분' % B.MINUTES[c['no']] + (' <span class="track basic">기본</span>' if c['no'] in B.BASIC else ' <span class="track adv">심화</span>'), esc(c['title']), esc(c['q']), esc(c['format'][0])) for c in chs)
    cards += '<a href="practice/index.html"><span class="n">마지막 장</span><b>실전 연습장 — 이산위상 사업장 시뮬레이터</b><span>픽셀 지도사무소, 바닥 타일 공장, 나머지 시계탑을 직접 운영하며 배운 것을 써 봐요.</span><span class="fmt">시뮬레이터</span></a>'
    bas = ' → '.join('<a href="%s.html">%02d</a>' % (c['slug'], c['no']) for c in chs if c['no'] in B.BASIC) + ' → <a href="practice/index.html">실전 연습장</a>'
    adv = ', '.join('<a href="%s.html">%02d %s</a>' % (c['slug'], c['no'], esc(c['title'].split(' — ')[0])) for c in chs if c['no'] not in B.BASIC)
    o.append(f'''<section class="level" id="tracks"><div class="wrap"><h2>두 갈래 과정 — 어디까지 읽을까</h2>
<div class="steps"><div><b class="n">1</b><b>기본 과정 <span class="track basic">기본</span></b><p>처음 오신 분은 이 순서만 따라가도 실전 연습장까지 갈 수 있어요.</p><p>{bas}</p></div>
<div><b class="n">2</b><b>심화 과정 <span class="track adv">심화</span></b><p>기본 과정을 마친 뒤 도전하세요. 대학 이상에서 배우는 내용을 그림으로 맛보는 장이에요.</p><p>{adv}</p></div>
<div><b class="n">3</b><b>심화 단계 접기 · 첫걸음 상자</b><p>어려운 단계는 「심화」로 접어 두었어요. 펼치지 않아도 다음 장을 읽을 수 있어요. 행렬·벡터가 처음이면 「벡터·행렬 첫걸음」 상자를 먼저 보세요(05·08·11·12·13·14·15·16·17·18·20·21·23장).</p></div></div>
<p class="note">자매 시리즈: 같은 원자료로 만든 입문판 「위상수학 교실」(<a href="https://adminmrobo.github.io/topology_ai_lab/">topology_ai_lab</a>)이 있어요. 이 연구실은 장을 더 잘게 나누고, 이산 위상과 행렬·벡터에 초점을 맞춘 심화·세분판이에요.</p></div></section>''')
    o.append(f'<section class="level" id="toc"><div class="wrap"><h2>목차 — {n}장 + 실전 연습장</h2><div class="toc">{cards}</div></div></section>')
    def fk(c):
        return FMT_KEY.get(c['format'][0], c['format'][0])
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (esc(k), esc(v), ', '.join('%02d' % c['no'] for c in chs if fk(c) == k)) for k, v in FORMAT_NOTE.items())
    o.append(f'''<section class="level" id="how"><div class="wrap"><h2>수업 방식 — 장마다 다른 수업</h2>
<div class="tw"><table class="tb"><thead><tr><th>형식</th><th>어떻게 하나</th><th>나오는 장</th></tr></thead><tbody>{rows}</tbody></table></div>
<h3>한 장의 흐름</h3><div class="steps"><div><b class="n">1</b><b>3줄 요약과 수업 소개</b><p>무엇을·왜·어디에 쓰는지 먼저 봐요.</p></div><div><b class="n">2</b><b>단계 2개</b><p>박사의 상황 질문 → 왜 이 방법 / 하루의 수식 질문 → (벡터·행렬 첫걸음) → 그림 실험 → 풀이 → 퀴즈.</p></div><div><b class="n">3</b><b>AI 판단 · 조교 대결 · 정리</b><p>AI 답의 오류 찾기, 계산으로 가리는 조교 대결, 한눈에 보는 정리표.</p></div></div>
{says([('fly', 'magnify', '원자료 그림에서 틀린 곳은 「바꾼다」 상자로 표시해 뒀어. 모두 22곳이야. 원자료도 의심하면서 읽자고.'), ('robo', 'coin', '계산은 저한테 맡기세요! …물론 조교 대결에서 자주 틀리지만요.')])}</div></section>''')
    o.append(B.footer_html(None, (chs[0]['slug'] + '.html', '01 ' + chs[0]['title']) if chs else None,
                           '<p class="note">원자료: 사용자가 제공한 이산 위상 인포그래픽 20장(작성자 확인 필요). 이 시리즈의 숫자 예시는 모두 설명용 예시값입니다.</p>'))
    o.append(B.foot_scripts(kg=False))
    open(os.path.join(B.ROOT, 'index.html'), 'w', encoding='utf-8').write('\n'.join(o))
    print('built index')
