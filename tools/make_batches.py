#!/usr/bin/env python3
"""docs/IMG_specs.md의 표지 지시문을 그림 도구에 붙여 넣을 묶음(docs/IMG_prompts_batches.md)으로 나눈다."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = open(os.path.join(ROOT, 'docs', 'IMG_specs.md'), encoding='utf-8').read()
covers = re.findall(r'### (cover_\w+) — (.+?)\n.*?```\n(.+?)\n```', spec, re.S)
face = re.search(r'## 4\..*', spec, re.S).group(0)

L = ['# 표지 그림 요청 묶음 — 이산위상 연구실 (원형 지키기 판)', '',
     '> 먼저 받은 표지는 캐릭터가 원형을 잃어 쓰지 않아요(`docs/CHARACTER_REVIEW.md`). 이 묶음은 캐릭터 팩의 정체성 문장과 기준 그림으로 다시 쓴 지시문이에요.', '',
     '## 공통으로 함께 올릴 것 (모든 묶음)', '',
     '- **기준 그림 `lab6_lineup.png`** (캐릭터 팩 adminmrobo/fruitfly-lab-expressions) — 캐릭터 모양의 유일한 기준',
     '- 표정 그림 E13(기본 얼굴): 박사, 초파리 연구원, 주판봇, 조수 하루, 시아, 모아',
     '- 2번 묶음부터: 원형 점검표를 통과한 cover_00',
     '- 공통 조건: 16:9, 1920×1080(480×270 픽셀 격자를 4배), 16비트 RPG 픽셀아트, 흰 배경, 그림 안 글자·숫자 없음, 오른쪽 46%는 빈 여백', '',
     '## 받은 뒤 원형 점검 (하나라도 틀리면 다시 요청)', '',
     '- [ ] 초파리: 몸이 **검은색**, 빨간 겹눈, 남색 헬멧(노란 줄), 케이블', '- [ ] 박사: **짙은 회흑색** 뾰족 머리 + 앞머리 흰 줄, 청록 안경, 흰 가운 + 검은 조끼',
     '- [ ] 주판봇: **베이지 브라운관 모니터** 몸, 초록 화면 얼굴, 무한궤도, 손에 주판', '- [ ] 하루: 분홍 머리 + 남색 줄, 머리 위 두 동그란 머리 뭉치, 라벤더 후드',
     '- [ ] 시아: 검은 긴 머리, **머리 장식 없음**, 검은 메이드 옷 + 회색 리본', '- [ ] 모아: **재색 베이지** 긴 웨이브 머리, 흰 프릴 머리띠, 카멜 카디건', '',
     '## 저장 이름 체크리스트', '']
L += ['- [ ] `img/cover/%s.webp` — %s' % (k, t) for k, t, _ in covers]
L += ['']
groups = [covers[:1]] + [covers[i:i + 4] for i in range(1, len(covers), 4)]
for gi, g in enumerate(groups, 1):
    L += ['## 묶음 %d — %s' % (gi, ', '.join(k for k, _, _ in g)), '']
    if gi == 1:
        L += ['이 묶음을 먼저 받아 원형 점검표로 확인한 뒤 다음 묶음으로 가요.', '']
    for k, t, p in g:
        L += ['### %s — %s' % (k, t), '', '```', p, '```', '']
L += ['## 묶음 %d — 표정 추가 (E27)' % (len(groups) + 1), '', face.split('\n', 1)[1].strip(), '']
open(os.path.join(ROOT, 'docs', 'IMG_prompts_batches.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('batches', len(groups), 'groups,', len(covers), 'covers')
