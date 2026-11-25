# 이산위상 연구실 — 그림 제작 명세서

> 상태 (2026-11-26): **표지 26/26 반영 완료** — 받은 그림은 2048×1152로, 정확한 픽셀 격자가 없는 그림이라 다시 줄이거나 압축하지 않고 받은 파일 그대로 썼어요. 공유 미리보기(img/og)는 `tools/make_og.py`가 표지를 왼쪽에 두고 오른쪽 빈 곳에 제목을 써서 만들어요. 아래 지시문은 다시 그릴 때 쓰는 원본이에요.

## 1. 공용 규칙

- 그림체: **16비트 RPG 픽셀아트**(연구실 표지 지침), **흰 배경(#ffffff)**. 그림 안에 글자·숫자·기호를 넣지 않는다(글자는 HTML로).
- 시리즈 표지 콘셉트: 「픽셀 열지도(이산) 위로 매끈한 바람길(연속)」 — `cover/cover_prompt.md` 참고. 원작 만화·애니 캐릭터는 쓰지 않고 연구실 식구만 그린다.
- 크기: 생성 원본 1920×1080(픽셀 격자 480×270을 4배). 줄일 때는 `NEAREST` 정수배만, 무손실 WebP로 저장.
- 미공개 X1~X3은 검은 실루엣(눈만 보임).
- 생성 순서: ① cover_00을 먼저 받아 그림체 확인 → ② 그 그림을 참고 그림으로 함께 올려 나머지 생성.
- 반영: `img/cover/cover_NN.webp`를 넣고 `python3 tools/build.py`를 다시 돌리면 대체 표지가 그림으로 바뀌어요. og는 같은 그림을 1200×630으로 잘라 `img/og/og_NN.webp`로 덮어써요.

## 2. 필요한 그림 전체

| 키 | 페이지 | 상태 | 등장 |
|---|---|---|---|
| cover_00 | index.html | 반영 완료 | 박사, 조수 하루, 시아, 모아 |
| cover_01 | 01_open_sets.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 조수 하루 |
| cover_02 | 02_closed_sets_boundary.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 시아 |
| cover_03 | 03_basis.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X2 |
| cover_04 | 04_discrete_vs_indiscrete.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_05 | 05_topology_as_table.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X3 |
| cover_06 | 06_connectedness.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X1 |
| cover_07 | 07_paths_in_punctured_plane.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_08 | 08_compactness.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 주판봇 |
| cover_09 | 09_hausdorff_compact.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 시아 |
| cover_10 | 10_smallest_neighborhoods.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_11 | 11_order_and_neighbor_matrix.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X2 |
| cover_12 | 12_pixel_paradox.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 조수 하루 |
| cover_13 | 13_khalimsky.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X3 |
| cover_14 | 14_groups_and_matrices.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X1 |
| cover_15 | 15_orbits_quotients.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 시아 |
| cover_16 | 16_proper_actions.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 초파리 연구원 |
| cover_17 | 17_tiles_dirichlet.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X2 |
| cover_18 | 18_lattices_modular.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 조수 하루 |
| cover_19 | 19_covering_spaces.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_20 | 20_deck_galois.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X3 |
| cover_21 | 21_functors_adjunction.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 시아 |
| cover_22 | 22_ultrafilters_stone_cech.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_23 | 23_extremal_profinite.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 미공개 X3 |
| cover_24 | 24_final_review.html | 반영 완료 | 박사, 초파리 연구원, 주판봇, 인턴 모아 |
| cover_practice | practice/index.html | 반영 완료 | 박사, 시아, 모아, X3 |

## 3. 표지 지시문

### cover_00 — 오리엔테이션

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a wind tunnel in a bright lab: a large blocky pixel heatmap (blue→green→yellow→orange square blocks) with thin smooth black streamlines flowing left to right around it; Haru stands in front of it, the Doctor points at it, the other characters gather. Characters: the Doctor (wild grey hair, round glasses, white lab coat), Haru the assistant (pink-and-navy twin buns), intern Sia (long black hair, maid-style uniform), intern Moa (long light-brown hair, red bow), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_01 — 열린 집합 — 이웃을 정하는 세 규칙

비유: 놀이터 비유 / 모임 명부 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a playground with a fence; a child stands in the middle with a soft green margin around her, another stands right at the fence with no margin. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), Haru the assistant (pink-and-navy twin buns). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_02 — 닫힌 집합과 경계 — 안쪽 · 바깥 · 물가

비유: 호수 비유 / 출입 명단 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a lake seen from above with a shoreline drawn as a dotted ring; one character stands in the water, one on land, one exactly on the shore. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Sia (long black hair, maid-style uniform). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_03 — 기저 — 작은 블록으로 위상 쌓기

비유: 레고 비유 / 배달 구역 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a table of toy building blocks (single cubes and long bricks) being stacked into shapes; one wrong stack wobbles. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X2 (black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_04 — 이산 위상과 밀착 위상 — 모두 섬 vs 모두 한 덩어리

비유: 섬 비유 / 단체 티셔츠 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a sea dotted with tiny islands, each with one little house, next to a big single continent; two teams debating on a stage. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_05 — 위상을 0과 1의 표로 — 행렬 첫 만남과 위상 세기

비유: 출석부 비유 / 해상도 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. an attendance board made of rows of lit and unlit square lamps (pure on/off pattern, no digits). Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X3 (small black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_06 — 끊김과 연결 — 한 섬인가, 군도인가

비유: 섬과 바다 비유 / 징검돌 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. stepping stones across a stream, every stone separate; a team drawing a line across the water between two groups of islands. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X1 (black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_07 — 구멍이 셀 수 있게 많아도 — 평면의 길은 끊기지 않는다

비유: 광장 기둥 비유 / 번호표 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a plaza with many small pillars; a character walks a path that bends once to slip between pillars. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_08 — 콤팩트 — 우산 몇 개면 다 덮일까

비유: 우산 비유 / 숨은 그림 찾기 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a schoolyard being covered by umbrellas; one corner near the edge stays uncovered by a thin gap. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), Jupanbot (boxy abacus robot with a screen face). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_09 — 떼어 놓기 — 콤팩트한 집합은 왜 닫혀 있나

비유: 담장 비유 / 안전지대 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. two neighbour houses separated by a fence built exactly halfway; a safety zone glowing around one point among four obstacles. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Sia (long black hair, maid-style uniform). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_10 — 가장 작은 이웃 — 알렉산드로프 공간과 느슨한 규칙

비유: 단짝 무리 비유 / 동아리 연합 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a classroom where each student has a small glowing circle of best friends; one student sits inside a bigger shared circle. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_11 — 순서 그림과 이웃 행렬 — 내 섬을 위아래로 줄 세우기

비유: 선수 과목표 비유 / 섬 출석표 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a course-prerequisite chart drawn as dots connected upward by lines, like a small family tree on a whiteboard. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X2 (black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_12 — 픽셀의 연결 역설 — 옆자리를 어떻게 정할까

비유: 바둑판 비유 / 체스 왕 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a large pixel picture of a diamond-shaped ring of black pixels on white; a chess king piece slipping diagonally through a corner gap. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), Haru the assistant (pink-and-navy twin buns). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_13 — 칼림스키 직선과 평면 — 홀수는 열리고 짝수는 닫힌다

비유: 징검다리 비유 / 바둑판 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a creek with alternating stepping stones and small wooden bridges; a checkerboard floor where some tiles are marked as joints. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X3 (small black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_14 — 군 — 되돌릴 수 있는 움직임과 2 × 2 행렬

비유: 타일 돌리기 비유 / 회전 버튼 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. students acting as rubber stamps rotating a big square tile by quarter turns on the floor. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X1 (black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_15 — 궤도 · 안정자 · 접은 공간

비유: 회전문 비유 / 달력 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a revolving door with a person at the tip leaving footprints in four places and a person at the central pillar staying still; a ribbon of the number line being wrapped into a circle. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Sia (long black hair, maid-style uniform). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_16 — 얌전한 작용의 등급 — 도장이 말썽을 부릴 때

비유: 컨베이어 비유 / 늘였다 줄인 사진 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a conveyor belt moving boxes in steps over floor marks; a photo being stretched wide and squashed thin repeatedly. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_17 — 대표 타일과 디리클레 영역 — 한 조각으로 바닥 전체를

비유: 반 대표 비유 / 기지국 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a floor being tiled with one square tile copied everywhere, and a honeycomb map split into nearest-tower regions. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X2 (black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_18 — 격자와 모듈러 군 — 타일 넓이는 행렬식

비유: 비스듬한 타일 비유 / 축척 지도 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a slanted parallelogram tile pattern on a floor next to a tall narrowing chimney-shaped field stretching upward. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), Haru the assistant (pink-and-navy twin buns). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_19 — 덮개 공간과 길 들어올리기 — 나선형 주차장

비유: 나선형 주차장 비유 / 경사로 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a spiral parking garage seen from the side, a car driving up the ramp; dotted lines drop from each floor to the same spot on the ground. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_20 — 층 바꾸기와 갈루아 대응 — 덮개와 부분군의 짝짓기

비유: 회전 초밥 비유 / 시계 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a conveyor-belt sushi counter with six plate spots rotating as a whole; two clocks (12-hour and 24-hour) stacked. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X3 (small black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_21 — 함자와 짝 — 이산 옷 입히기와 옷 벗기기

비유: 복장 규정 비유 / 옷 가게 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a costume shop with a "no dress code" door everyone walks through, and a fitting room where outfits are put on and taken off. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Sia (long black hair, maid-style uniform). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_22 — 무한 끝의 점 — 울트라필터와 스톤-체흐

비유: 학급 회의 비유 / 바람 방향 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. an endless field at sunset with many flags planted at the far horizon, each flag fluttering in a different wind direction. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_23 — 아주 끊긴 공간과 프로유한 — 먼지처럼 끊긴 두 공간

비유: 모래섬 비유 / 맞물린 시계 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. sand islets clustering toward one point on a beach; a tall clock tower where each floor has a clock with more ticks, gears meshing between floors. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), unrevealed student X3 (small black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_24 — 종합 — 기말 쪽지시험과 졸업 발표

비유: 요약 노트 비유 / 졸업 앨범 비유

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. a graduation ceremony in the lab: four pillars labelled only by icons (dots, island, stamp, flag), students holding diplomas. Characters: the Doctor (wild grey hair, round glasses, white lab coat), the Fruit-fly researcher (tiny fly in a lab coat with a magnifier), Jupanbot (boxy abacus robot with a screen face), intern Moa (long light-brown hair, red bow). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```

### cover_practice — 실전 연습장

```
16-bit SNES-era RPG pixel art, clean white background (#ffffff), daytime lab feeling. three small shop fronts in a row: a map office with pixel island maps, a floor-tile factory with slanted tiles, and a clock tower; the Doctor and students in front. Characters: the Doctor (wild grey hair, round glasses, white lab coat), intern Sia (long black hair, maid-style uniform), intern Moa (long light-brown hair, red bow), unrevealed student X3 (small black silhouette, only eyes visible). Keep the right 46% of the image as empty white space for a title. No letters, no numbers, no symbols in the picture. Crisp outlines, limited palette.
```
