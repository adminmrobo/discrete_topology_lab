#!/usr/bin/env python3
"""docs/IMG_specs.md와 cover_manifest.json을 장 데이터에서 만든다."""
import os, json, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_EN = {'doc': 'the Doctor (wild grey hair, round glasses, white lab coat)', 'fly': 'the Fruit-fly researcher (tiny fly in a lab coat with a magnifier)', 'robo': 'Jupanbot (boxy abacus robot with a screen face)',
           'asst': 'Haru the assistant (pink-and-navy twin buns)', 'sia': 'intern Sia (long black hair, maid-style uniform)', 'moa': 'intern Moa (long light-brown hair, red bow)',
           'x1': 'unrevealed student X1 (black silhouette, only eyes visible)', 'x2': 'unrevealed student X2 (black silhouette, only eyes visible)', 'x3': 'unrevealed student X3 (small black silhouette, only eyes visible)'}
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
 'practice': 'three small shop fronts in a row: a map office with pixel island maps, a floor-tile factory with slanted tiles, and a clock tower; the Doctor and students in front',
}


def load(i):
    sp = importlib.util.spec_from_file_location('m', os.path.join(ROOT, 'content', 'ch%02d.py' % i)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.CH


def prompt(scene, who):
    ch = ', '.join(NAME_EN[w] for w in who)
    return ('16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. ' + scene + '. Characters: ' + ch +
            '. Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.')


def main():
    chs = [load(i) for i in range(1, 25)]
    L = ['# 이산위상 연구실 — 그림 제작 명세서', '',
         '> 상태 (2026-11-26): **표지 26/26 반영 완료** — 받은 그림은 2048×1152로, 정확한 픽셀 격자가 없는 그림이라 다시 줄이거나 압축하지 않고 받은 파일 그대로 썼어요. 공유 미리보기(img/og)는 `tools/make_og.py`가 표지를 왼쪽에 두고 오른쪽 빈 곳에 제목을 써서 만들어요. 아래 지시문은 다시 그릴 때 쓰는 원본이에요.', '',
         '## 1. 공용 규칙', '',
         '- 그림체: **16비트 RPG 픽셀아트**(연구실 표지 지침), **흰 배경(#ffffff)**. 그림 안에 글자·숫자·기호를 넣지 않는다(글자는 HTML로).',
         '- 시리즈 표지 콘셉트: 「픽셀 열지도(이산) 위로 매끈한 바람길(연속)」 — `cover/cover_prompt.md` 참고. 원작 만화·애니 캐릭터는 쓰지 않고 연구실 식구만 그린다.',
         '- 크기: 생성 원본 1920×1080(픽셀 격자 480×270을 4배). 줄일 때는 `NEAREST` 정수배만, 무손실 WebP로 저장.',
         '- 미공개 X1~X3은 검은 실루엣(눈만 보임).',
         '- 생성 순서: ① cover_00을 먼저 받아 그림체 확인 → ② 그 그림을 참고 그림으로 함께 올려 나머지 생성.',
         '- 반영: `img/cover/cover_NN.webp`를 넣고 `python3 tools/build.py`를 다시 돌리면 대체 표지가 그림으로 바뀌어요. og는 같은 그림을 1200×630으로 잘라 `img/og/og_NN.webp`로 덮어써요.', '',
         '## 2. 필요한 그림 전체', '', '| 키 | 페이지 | 상태 | 등장 |', '|---|---|---|---|']
    L.append('| cover_00 | index.html | 반영 완료 | 박사, 조수 하루, 시아, 모아 |')
    for c in chs:
        who = ['doc', 'fly', 'robo', c['star'][0]]
        L.append('| cover_%02d | %s.html | 반영 완료 | %s |' % (c['no'], c['slug'], ', '.join(dict(doc='박사', fly='초파리 연구원', robo='주판봇', asst='조수 하루', sia='인턴 시아', moa='인턴 모아', x1='미공개 X1', x2='미공개 X2', x3='미공개 X3')[w] for w in who)))
    L.append('| cover_practice | practice/index.html | 반영 완료 | 박사, 시아, 모아, X3 |')
    L += ['', '## 3. 표지 지시문', '', '### cover_00 — 오리엔테이션', '', '```', prompt(SCENE[0], ['doc', 'asst', 'sia', 'moa', 'fly', 'robo']), '```', '']
    for c in chs:
        L += ['### cover_%02d — %s' % (c['no'], c['title']), '', '비유: ' + ' / '.join(s['pair'][2] for s in c['stages']), '', '```', prompt(SCENE[c['no']], ['doc', 'fly', 'robo', c['star'][0]]), '```', '']
    L += ['### cover_practice — 실전 연습장', '', '```', prompt(SCENE['practice'], ['doc', 'sia', 'moa', 'x3']), '```', '']
    open(os.path.join(ROOT, 'docs', 'IMG_specs.md'), 'w', encoding='utf-8').write('\n'.join(L))
    items = [{'id': 'cover_00', 'role': 'cover', 'path': 'index.html#top', 'status': 'ok', 'file': 'img/cover/cover_00.webp', 'size': [2048, 1152], 'grid': None, 'note': 'Genspark 생성 원본 그대로(픽셀 격자 없음, 재압축 안 함)'}]
    items += [{'id': 'cover_%02d' % c['no'], 'role': 'cover', 'path': c['slug'] + '.html#top', 'status': 'ok', 'characters': ['doc', 'fly', 'jupanbot', c['star'][0]], 'file': 'img/cover/cover_%02d.webp' % c['no'], 'size': [2048, 1152], 'grid': None, 'note': 'Genspark 생성 원본 그대로(픽셀 격자 없음, 재압축 안 함)'} for c in chs]
    items.append({'id': 'cover_practice', 'role': 'cover', 'path': 'practice/index.html#top', 'status': 'ok', 'file': 'img/cover/cover_practice.webp', 'size': [2048, 1152], 'grid': None, 'note': 'Genspark 생성 원본 그대로(픽셀 격자 없음, 재압축 안 함)'})
    man = {'series_ko': '이산위상 연구실 — 점 하나하나가 섬인 세상', 'title_ko': '이산위상 연구실', 'site_title': '이산위상 연구실 · 중학생도 따라오는 이산 위상 24장 + 실전 연습장',
           'site_url': 'https://adminmrobo.github.io/discrete_topology_lab/', 'updated': '2026-11-26',
           'ontology': {'pages': [{'path': c['slug'] + '.html', 'kg': True, 'export': True} for c in chs]}, 'languages': ['ko'], 'items': items}
    json.dump(man, open(os.path.join(ROOT, 'cover_manifest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('specs, manifest')


main()
