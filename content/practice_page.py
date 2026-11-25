"""마지막 장 · 실전 연습장 조립"""
import os


def build(B, chs):
    B.USED.update({('doc', 'judge'), ('doc', 'think'), ('asst', 'report'), ('fly', 'magnify'), ('robo', 'calc'), ('robo', 'coin')})
    last = chs[-1]
    o = [B.head('마지막 장 · 실전 연습장 — ' + B.SERIES, '픽셀 지도사무소, 바닥 타일 공장, 나머지 시계탑을 운영하며 이산 위상 개념을 써 보는 시뮬레이터.', depth=1, og='../img/og/og_practice.webp')]
    o.append('<nav class="top" aria-label="실전 연습장 목차"><a class="logo" href="../index.html">이산위상 연구실</a><a href="#sim">사업장</a><a href="#wrap">마무리</a><a href="../%s.html">%02d장 종합</a></nav><div id="prog"></div>' % (last['slug'], last['no']))
    o.append(B.cover_html('cover_practice', '이산위상 사업장 시뮬레이터', '마지막 장 · 실전 연습장', '픽셀 지도사무소 · 바닥 타일 공장 · 나머지 시계탑', '실전 연습장 표지 — 세 사업장 앞의 박사와 수강생들', up='../',
                          chars=[('doc', 'front'), ('sia', 'smile'), ('moa', 'smile'), ('x3', 'e13')]))
    o.append('<header class="hero"><div class="wrap"><div class="kicker">마지막 장 · 실전 연습장</div><h1>이산위상 사업장 시뮬레이터</h1>'
             '<p class="q">핵심 질문 — 배운 개념으로 「가상 사업장」의 결정을 내리면, 숫자가 어떻게 달라질까?</p>'
             '<p>사업장 세 곳을 탭으로 골라 운영해 보세요. 초록 상자는 시장 환경(내가 못 바꾸는 조건), 파란 상자는 내 결정이에요. 성적표·그래프·캐릭터 대사가 바로 바뀌고, 미션 3개는 조작한 뒤에 자동으로 판정돼요. 주소 끝에 #map, #tile, #clock을 붙이면 그 사업장이 바로 열려요.</p>'
             + B.says([('doc', 'front', '마지막 장은 실습입니다. 정답은 계산이 판정해요. 사업장마다 미션 세 개, 모두 아홉 개!'), ('moa', 'cheer', '세 곳 다 운영해 볼래요!')]) + '</div></header>')
    o.append('<section class="level" style="padding-top:24px"><div class="wrap" id="sim"></div></section>')
    o.append('''<section class="level" id="wrap"><div class="wrap"><h2>마무리 — 세 사업장이 함께 묻는 질문</h2>
<p>세 사업장은 모두 「이산적인 재료(픽셀, 정수 격자, 유한한 시계)에 어떤 규칙을 주느냐가 숫자를 바꾼다」는 같은 질문을 던져요. 지도사무소에서는 옆자리 규칙이 섬의 수를, 타일 공장에서는 기본 벡터의 행렬식이 비용을, 시계탑에서는 층끼리의 맞물림이 「저장된 수」가 되는지를 정했어요. 결과 숫자를 믿기 전에 그 숫자를 만든 규칙을 먼저 확인하는 것 — 이것이 이 연구실이 말하는 「AI 결과를 판단하는 힘」이에요.</p>
<div class="lim"><b>모형의 한계</b> — 사업장의 숫자(시공비, 추가 공사비, 보관료, 지도 크기)는 모두 교육용 예시값이에요. 실제 영상 처리·건축 시공·암호 계산에는 훨씬 많은 조건이 붙어요. 이 페이지의 결과는 경영·투자 권고가 아닙니다.</div>
</div></section>''')
    o.append(B.footer_html(('../%s.html' % last['slug'], '%02d %s' % (last['no'], last['title'])), ('../index.html', '오리엔테이션으로'), ''))
    o.append('<script src="../assets/sprites.js"></script><script src="../assets/widgets.js"></script><script src="../assets/lab.js"></script><script src="../assets/practice.js"></script></body></html>')
    os.makedirs(os.path.join(B.ROOT, 'practice'), exist_ok=True)
    open(os.path.join(B.ROOT, 'practice', 'index.html'), 'w', encoding='utf-8').write('\n'.join(o))
    print('built practice')
