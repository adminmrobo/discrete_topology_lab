#!/usr/bin/env python3
"""docs/IMG_specs.md와 cover_manifest.json을 장 데이터에서 만든다."""
import os, json, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_EN = {  # 캐릭터 팩(fruitfly-lab-expressions) specs/*/00_character_core.md의 정체성 문장을 그대로 옮김
 'doc': 'the Professor (chibi male scientist with a big head, dark charcoal spiky hair with a white streak at the front, a small low ponytail at the back, very thick bold black eyebrows, teal-framed rectangular glasses, white lab coat over a black vest, black tie, black slacks; NOT grey hair, NO moustache)',
 'asst': 'Haru the assistant (chibi anime girl, long straight pink hair with navy blue streaks including a thick navy streak down the center of the bangs, two round messy hair buns on top, a small ahoge, big bright blue eyes, lavender hoodie with white drawstrings under an open white knee-length lab coat, blue jeans, lavender sneakers)',
 'sia': 'intern Sia (chibi maid intern, long straight jet-black hair to the waist, side-swept bangs, gray eyes, NO headdress, charcoal-black long-sleeved maid dress with white lace cuffs, large soft gray bow at the collar, long white frilled apron)',
 'moa': 'intern Moa (chibi maid intern, long ash-beige hair to the waist with wavy ends, white frilled maid headband, amber-brown eyes, camel knit cardigan over a white shirt with a red and navy plaid bow tie, white frilled apron, black skirt, brown loafers; NOT brown hair, NOT a big red bow)',
 'robo': 'Jupanbot (retro computer robot: its head-and-body is ONE beige rounded box CRT monitor with a thick dark brown outline, a big dark green screen face with mint pixel-block eyes and mouth, a short antenna topped by one small red-brown abacus bead, grey segmented arms with round mitten hands, no legs but two dark grey tank treads, holding a small wooden abacus in its hands; NOT a grey robot, the abacus is NOT its body)',
 'fly': 'the Fruit-fly researcher (tiny cartoon fruit fly with a dark charcoal-BLACK segmented insect body, large glossy red compound eyes, a retro dark blue helmet with a yellow-white center stripe and small round side bolts, magenta, purple and blue cables dangling from the back of the helmet, a tiny white lab coat over a black vest, translucent veined wings, six thin black legs; the body is NOT white)',
 'x1': 'unrevealed student X1 (chibi pure black silhouette, only two white eyes visible)', 'x2': 'unrevealed student X2 (chibi pure black silhouette, only two white eyes visible)', 'x3': 'unrevealed student X3 (small chibi pure black silhouette, only two white eyes visible)'}
SCENE = {
 0: 'a wind tunnel in a bright lab: a large blocky pixel heatmap (blue→green→yellow→orange square blocks) with thin smooth black streamlines flowing left to right around it; Haru stands in front of it, the Doctor points at it, the other characters gather',
 1: 'a playground with a fence; a child stands in the middle with a soft green margin around her, another stands right at the fence with no margin',
 2: 'a lake seen from above with a shoreline drawn as a dotted ring; one character stands in the water, one on land, one exactly on the shore',
 3: 'a table of toy building blocks (single cubes and long bricks) being stacked into shapes; one wrong stack wobbles',
 4: 'a sea dotted with tiny islands, each with one little house, next to a big single continent; two teams debating on a stage',
 5: 'an attendance board made of rows of lit and unlit square lamps (pure on/off pattern, no digits)',
 6: 'stepping stones across a stream, every stone separate; a team drawing a line across the water between two groups of islands',
 7: 'a plaza with many small pillars; a character walks a path that bends once to slip between pillars',
 8: 'a schoolyard being covered by umbrellas; one corner near the edge stays uncovered by a thin gap',
 9: 'two neighbour houses separated by a fence built exactly halfway; a safety zone glowing around one point among four obstacles',
 10: 'a classroom where each student has a small glowing circle of best friends; one student sits inside a bigger shared circle',
 11: 'a course-prerequisite chart drawn as dots connected upward by lines, like a small family tree on a whiteboard',
 12: 'a large pixel picture of a diamond-shaped ring of black pixels on white; a chess king piece slipping diagonally through a corner gap',
 13: 'a creek with alternating stepping stones and small wooden bridges; a checkerboard floor where some tiles are marked as joints',
 14: 'students acting as rubber stamps rotating a big square tile by quarter turns on the floor',
 15: 'a revolving door with a person at the tip leaving footprints in four places and a person at the central pillar staying still; a ribbon of the number line being wrapped into a circle',
 16: 'a conveyor belt moving boxes in steps over floor marks; a photo being stretched wide and squashed thin repeatedly',
 17: 'a floor being tiled with one square tile copied everywhere, and a honeycomb map split into nearest-tower regions',
 18: 'a slanted parallelogram tile pattern on a floor next to a tall narrowing chimney-shaped field stretching upward',
 19: 'a spiral parking garage seen from the side, a car driving up the ramp; dotted lines drop from each floor to the same spot on the ground',
 20: 'a conveyor-belt sushi counter with six plate spots rotating as a whole; two clocks (12-hour and 24-hour) stacked',
 21: 'a costume shop with a "no dress code" door everyone walks through, and a fitting room where outfits are put on and taken off',
 22: 'an endless field at sunset with many flags planted at the far horizon, each flag fluttering in a different wind direction',
 23: 'sand islets clustering toward one point on a beach; a tall clock tower where each floor has a clock with more ticks, gears meshing between floors',
 24: 'a graduation ceremony in the lab: four pillars labelled only by icons (dots, island, stamp, flag), students holding diplomas',
 25: 'a giant smartphone photo being zoomed in until square pixel blocks appear; a ring-shaped donut slice drawn in coarse pixels next to the same ring drawn in fine pixels',
 26: 'a hospital-style light box showing a blue branching blood-vessel pixel map; a tide gauge beside it with the water level slider half way; small yellow noise specks being swept away',
 27: 'a 3D printer on a workbench next to a low-poly triangle-mesh teacup and a triangle-mesh donut; one teacup has a small missing triangle patch glowing red at its edges, like a quilt with a torn patch',
 28: 'a hilly forest map seen from above with small sensor posts, each with a pale blue coverage circle; circles overlap into one ring, leaving one small uncovered red gap in the middle; a character carries one more sensor post toward the gap',
 29: 'students standing in a loose circle on a schoolyard reaching their arms out toward each other, with horizontal colored bars of different lengths floating above like a barcode; beside them a side view of a bumpy hill path with rain puddles at different depths',
 'practice': 'three small shop fronts in a row: a map office with pixel island maps, a floor-tile factory with slanted tiles, and a clock tower; the Doctor and students in front',
}


def load(i):
    sp = importlib.util.spec_from_file_location('m', os.path.join(ROOT, 'content', 'ch%02d.py' % i)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.CH


def prompt(scene, who):
    ch = ', '.join(NAME_EN[w] for w in who)
    return ('Use the attached reference lineup (lab6_lineup.png) and expression faces as the ONLY character design source; keep every character exactly on-model. '
            'Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, thick dark outlines, clean white background (#ffffff), daytime lab feeling. ' + scene + '. Characters: ' + ch +
            '. Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols, no watermark in the picture. '
            'Negative: off-model characters, redesigned characters, white fruit fly, grey-haired professor, grey robot, brown-haired Moa, headdress on Sia, blurry, 3D render, photorealistic.')


def main():
    chs = [load(i) for i in range(1, 40) if os.path.exists(os.path.join(ROOT, 'content', 'ch%02d.py' % i))]
    L = ['# 이산위상 연구실 — 그림 제작 명세서', '',
         '> 상태 (2026-11-26): **표지 다시 그리기 대기** — 먼저 받은 표지 26장은 캐릭터가 원형을 잃어(초파리 흰색, 박사 회색 머리, 모아 갈색 머리, 주판봇 회색 로봇 등) `img/cover_offmodel/`로 옮겼어요. 지금은 캔버스 대체 표지(캐릭터 팩 스프라이트)가 보여요. 아래 지시문은 캐릭터 팩 정체성 문장과 기준 그림(lab6_lineup.png)을 바탕으로 고친 판이에요. 평가와 결정은 `docs/CHARACTER_REVIEW.md`.', '',
         '## 1. 공용 규칙', '',
         '- 그림체: **16비트 RPG 픽셀아트**(연구실 표지 지침), **흰 배경(#ffffff)**. 그림 안에 글자·숫자·기호를 넣지 않는다(글자는 HTML로).',
         '- 시리즈 표지 콘셉트: 「픽셀 열지도(이산) 위로 매끈한 바람길(연속)」 — `cover/cover_prompt.md` 참고. 원작 만화·애니 캐릭터는 쓰지 않고 연구실 식구만 그린다.',
         '- 크기: 생성 원본 1920×1080(픽셀 격자 480×270을 4배). 줄일 때는 `NEAREST` 정수배만, 무손실 WebP로 저장.',
         '- 미공개 X1~X3은 검은 실루엣(눈만 보임).',
         '- 생성 순서: ① 캐릭터 팩의 lab6_lineup.png와 표정 그림(E13)을 **반드시 함께 첨부** → ② cover_00을 먼저 받아 `docs/CHARACTER_REVIEW.md`의 원형 점검표로 확인 → ③ 통과한 그림을 참고 그림으로 더해 나머지 생성.',
         '- 반영: `img/cover/cover_NN.webp`를 넣고 `python3 tools/build.py`를 다시 돌리면 대체 표지가 그림으로 바뀌어요. og는 같은 그림을 1200×630으로 잘라 `img/og/og_NN.webp`로 덮어써요.', '',
         '## 2. 필요한 그림 전체', '', '| 키 | 페이지 | 상태 | 등장 |', '|---|---|---|---|']
    L.append('| cover_00 | index.html | 다시 그리기 | 박사, 조수 하루, 시아, 모아 |')
    for c in chs:
        who = ['doc', 'fly', 'robo', c['star'][0]]
        L.append('| cover_%02d | %s.html | %s | %s |' % (c['no'], c['slug'], '새로 그리기' if c['no'] >= 25 else '다시 그리기', ', '.join(dict(doc='박사', fly='초파리 연구원', robo='주판봇', asst='조수 하루', sia='인턴 시아', moa='인턴 모아', x1='미공개 X1', x2='미공개 X2', x3='미공개 X3')[w] for w in who)))
    L.append('| cover_practice | practice/index.html | 다시 그리기 | 박사, 시아, 모아, X3 |')
    L += ['', '## 3. 표지 지시문', '', '### cover_00 — 오리엔테이션', '', '```', prompt(SCENE[0], ['doc', 'asst', 'sia', 'moa', 'fly', 'robo']), '```', '']
    for c in chs:
        L += ['### cover_%02d — %s' % (c['no'], c['title']), '', '비유: ' + ' / '.join(s['pair'][2] for s in c['stages']), '', '```', prompt(SCENE[c['no']], ['doc', 'fly', 'robo', c['star'][0]]), '```', '']
    L += ['### cover_practice — 실전 연습장', '', '```', prompt(SCENE['practice'], ['doc', 'sia', 'moa', 'x3']), '```', '']
    L += ['## 4. 표정 추가 요청 — E27 머리 감싸 쥐기 (시아 · 모아)', '', '이론 접기 상자와 4컷 첫 장면에 쓸 표정이에요. 받기 전까지는 E21·E24 표정에 흔들림 효과를 씌워 대신해요.', '',
          '```', 'Use the attached character sheet as the ONLY design source and keep the character exactly on-model. Same 16-bit pixel-art style, same canvas size and framing as the attached expression faces, plain light grey background. '
          'New expression E27 "head_clutch": both hands pressed to the sides of the head, eyes squeezed into swirls, a small sweat drop, mouth in a wobbly line, as if a math formula is too hard. No letters, no symbols. Character: ' + NAME_EN['sia'], '```', '',
          '```', 'Same request for: ' + NAME_EN['moa'], '```', '']
    open(os.path.join(ROOT, 'docs', 'IMG_specs.md'), 'w', encoding='utf-8').write('\n'.join(L))
    items = [{'id': 'cover_00', 'role': 'cover', 'path': 'index.html#top', 'status': 'regenerate', 'file': 'img/cover/cover_00.webp', 'size': [1920, 1080], 'grid': [480, 270], 'offmodel': 'img/cover_offmodel/cover_00.webp', 'note': '원형 상실 판은 img/cover_offmodel/에 보관, 새 지시문으로 다시 생성'}]
    items += [{'id': 'cover_%02d' % c['no'], 'role': 'cover', 'path': c['slug'] + '.html#top', 'status': 'regenerate' if c['no'] < 25 else 'placeholder', 'characters': ['doc', 'fly', 'jupanbot', c['star'][0]], 'file': 'img/cover/cover_%02d.webp' % c['no'], 'size': [1920, 1080], 'grid': [480, 270], 'note': '원형 상실 판은 img/cover_offmodel/에 보관, 새 지시문으로 다시 생성'} for c in chs]
    items.append({'id': 'cover_practice', 'role': 'cover', 'path': 'practice/index.html#top', 'status': 'regenerate', 'file': 'img/cover/cover_practice.webp', 'size': [1920, 1080], 'grid': [480, 270], 'note': '원형 상실 판은 img/cover_offmodel/에 보관, 새 지시문으로 다시 생성'})
    man = {'series_ko': '이산위상 연구실 — 점 하나하나가 섬인 세상', 'title_ko': '이산위상 연구실', 'site_title': '이산위상 연구실 · 중학생도 따라오는 이산 위상 29장(활용 편 5장 포함) + 실전 연습장',
           'site_url': 'https://adminmrobo.github.io/discrete_topology_lab/', 'updated': '2026-11-26',
           'ontology': {'pages': [{'path': c['slug'] + '.html', 'kg': True, 'export': True} for c in chs]}, 'languages': ['ko'], 'items': items}
    json.dump(man, open(os.path.join(ROOT, 'cover_manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('specs, manifest')


main()
