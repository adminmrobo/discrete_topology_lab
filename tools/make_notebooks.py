#!/usr/bin/env python3
"""활용 편 주피터 노트북 5개를 만들고 실제로 실행해 결과까지 저장한다.
필요 패키지: numpy scipy matplotlib scikit-image networkx trimesh ripser nbformat nbclient ipykernel"""
import os, nbformat
from nbclient import NotebookClient

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'notebooks')
os.makedirs(OUT, exist_ok=True)
SETUP = ("# 처음 한 번만: 필요한 패키지 설치 (구글 코랩이면 앞에 !를 붙여 그대로 실행)\n"
         "# pip install numpy scipy matplotlib scikit-image networkx trimesh ripser")

NB = {
'25_discrete_data': ('25장 · 컴퓨터 속 데이터는 왜 이산인가 — 해상도가 모양을 바꾼다', [
 ('md', '연속인 고리(도넛 단면)를 여러 해상도의 픽셀 그림으로 바꾸고, **덩어리 수**와 **구멍 수**가 지켜지는지 셉니다. 덩어리는 대각선까지 이웃(8-이웃), 바깥 빈 곳은 가로세로 이웃(4-이웃)으로 셉니다(12장).'),
 ('code', '''import numpy as np
from scipy import ndimage

def ring(N, r_in=0.25, r_out=0.36):
    """[0,1]x[0,1] 위의 고리를 N x N 픽셀로 (픽셀 가운데가 고리 안이면 1)"""
    c = (np.arange(N) + 0.5) / N
    X, Y = np.meshgrid(c, c)
    r = np.hypot(X - 0.5, Y - 0.5)
    return ((r >= r_in) & (r <= r_out)).astype(int)

def count(G):
    obj, n_obj = ndimage.label(G, structure=np.ones((3, 3)))          # 8-이웃
    bg, n_bg = ndimage.label(1 - G)                                     # 4-이웃(기본값)
    border = set(np.unique(np.concatenate([bg[0], bg[-1], bg[:, 0], bg[:, -1]]))) - {0}
    return n_obj, n_bg - len(border)                                    # 덩어리, 구멍

for N in [4, 6, 8, 12, 16, 24, 48]:
    n_obj, holes = count(ring(N))
    print(f"{N:>2} x {N:<2}  덩어리 {n_obj}  구멍 {holes}  {'OK' if (n_obj, holes) == (1, 1) else '모양이 바뀜'}")'''),
 ('md', '해상도가 너무 낮으면 고리가 끊기거나 구멍이 막혀서 「덩어리 1, 구멍 1」이 깨집니다. 컴퓨터가 연속인 세상을 이산 데이터로 저장할 때 모양(위상)이 바뀔 수 있다는 뜻이에요.'),
 ('code', '''import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 4, figsize=(10, 2.6))
for a, N in zip(ax, [6, 8, 16, 48]):
    a.imshow(ring(N), cmap='Blues'); a.set_title(f"{N} x {N}  {count(ring(N))}"); a.axis('off')
plt.tight_layout(); plt.show()'''),
]),
'26_image_vessel': ('26장 · 디지털 이미지와 의료 영상 — 혈관은 끊기지 않았을까', [
 ('md', '합성 혈관 영상에 **밝기 기준(임계값)**을 바꿔 가며 혈관을 골라내고, 조각(연결 성분) 수와 테두리(경계)를 셉니다. 실제 CT·MRI 분석에서 쓰는 순서와 같아요.'),
 ('code', '''import numpy as np
from scipy import ndimage
from skimage.segmentation import find_boundaries

rng = np.random.default_rng(7)
H, W = 40, 64
I = 0.18 + 0.06 * rng.standard_normal((H, W))
segs = [(2,20,30,20,2.2,.92),(30,20,60,8,1.6,.72),(30,20,60,32,1.6,.72),(18,20,26,5,1.1,.55),(44,14,52,3,.9,.47),(44,26,55,38,.9,.47),(12,20,16,36,1.0,.52)]
yy, xx = np.mgrid[0:H, 0:W]
for x0, y0, x1, y1, w, v in segs:
    dx, dy = x1 - x0, y1 - y0
    u = np.clip(((xx - x0) * dx + (yy - y0) * dy) / (dx * dx + dy * dy), 0, 1)
    d = np.hypot(xx - x0 - u * dx, yy - y0 - u * dy)
    I = np.where(d <= w, np.maximum(I, v * (1 - .15 * u) + .05 * rng.standard_normal((H, W))), I)

for t in [0.30, 0.40, 0.45, 0.50, 0.60, 0.70]:
    mask = I >= t
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    sizes = np.bincount(lab.ravel())[1:]
    print(f"기준 {t:.2f}: 조각 {n:>3}개, 가장 큰 조각 {sizes.max() if n else 0:>4}자리")'''),
 ('md', '기준이 낮으면 배경 잡음까지 혈관으로 잡혀 조각이 많아지고, 너무 높으면 가는 혈관이 끊깁니다. 작은 조각을 지우고(잡음 제거) 테두리를 뽑아 봅니다.'),
 ('code', '''raw = I >= 0.45
lab0, n0 = ndimage.label(raw, structure=np.ones((3, 3)))
sizes = np.bincount(lab0.ravel()); sizes[0] = 0
mask = np.isin(lab0, np.where(sizes >= 6)[0])                 # 6자리보다 작은 조각 = 잡음으로 보고 지우기
lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
edge = find_boundaries(mask, mode='inner')
print("잡음 제거 뒤 조각:", n, " 테두리 자리:", int(edge.sum()))
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(11, 2.8))
ax[0].imshow(I, cmap='gray'); ax[0].set_title('영상')
ax[1].imshow(lab, cmap='tab20'); ax[1].set_title(f'조각 {n}개')
ax[2].imshow(edge, cmap='Reds'); ax[2].set_title('테두리')
for a in ax: a.axis('off')
plt.tight_layout(); plt.show()'''),
]),
'27_mesh': ('27장 · 3D 메시 — 구멍 났나, 찢어졌나', [
 ('md', '3D 물체는 수많은 삼각형(메시)으로 저장됩니다. **V − E + F**(오일러 수)와 **삼각형 하나에만 붙은 모서리**(가장자리)를 세면 구멍·찢어짐을 판정할 수 있어요. `trimesh`를 씁니다.'),
 ('code', '''import numpy as np, trimesh

def report(name, m):
    V, E, F = len(m.vertices), len(m.edges_unique), len(m.faces)
    chi = V - E + F
    g = (2 - chi) / 2 if m.is_watertight else None
    print(f"{name:<14} V={V:>4} E={E:>4} F={F:>4}  V-E+F={chi:>3}  물샐틈없음={m.is_watertight}  손잡이 수={g}")

report('정육면체', trimesh.creation.box())
report('공(이십면체)', trimesh.creation.icosphere(subdivisions=2))
report('도넛', trimesh.creation.torus(major_radius=1.0, minor_radius=0.3))'''),
 ('md', '공은 삼각형을 아무리 잘게 나눠도 V − E + F = 2, 도넛은 0입니다. 이제 공에서 삼각형 몇 개를 지워 「구멍 난 메시」를 만들고 가장자리 모서리를 찾습니다.'),
 ('code', '''m = trimesh.creation.icosphere(subdivisions=2)
keep = np.ones(len(m.faces), bool); keep[:6] = False          # 삼각형 6개 지우기
hole = trimesh.Trimesh(m.vertices, m.faces[keep], process=True)
# 삼각형 하나에만 붙은 모서리 = 가장자리 (찢어지거나 뚫린 곳)
edges = np.sort(hole.edges, axis=1)
uniq, cnt = np.unique(edges, axis=0, return_counts=True)
boundary = uniq[cnt == 1]
report('구멍 난 공', hole)
print('가장자리 모서리 수:', len(boundary))'''),
]),
'28_sensor': ('28장 · 네트워크와 센서망 — 끊긴 곳, 빈 곳 찾기', [
 ('md', '센서를 무작위로 놓고 반경을 바꿔 가며 **통신 덩어리 수**(그래프의 연결 성분)와 **음영 지역**(어느 센서도 닿지 않는 곳)을 셉니다. `networkx`를 씁니다.'),
 ('code', '''import numpy as np, networkx as nx
from scipy import ndimage

rng = np.random.default_rng(21)
W, H, n = 320, 220, 16
P = np.column_stack([18 + rng.random(n) * (W - 36), 18 + rng.random(n) * (H - 36)])

def analyze(r, P=P):
    G = nx.Graph(); G.add_nodes_from(range(len(P)))
    for a in range(len(P)):
        for b in range(a + 1, len(P)):
            if np.hypot(*(P[a] - P[b])) <= 2 * r:     # 두 원이 겹치면 통신
                G.add_edge(a, b)
    gx, gy = np.meshgrid(np.arange(3, W, 6), np.arange(3, H, 6))
    d = np.min(np.hypot(gx[..., None] - P[:, 0], gy[..., None] - P[:, 1]), axis=2)
    uncovered = d > r
    lab, k = ndimage.label(uncovered)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return nx.number_connected_components(G), k - len(border), uncovered.mean()

for r in [15, 20, 26, 32, 40, 50]:
    c, inner, frac = analyze(r)
    print(f"반경 {r:>2}m: 통신 덩어리 {c:>2}개, 안쪽 음영 구멍 {inner}곳, 빈 넓이 {frac:.0%}")'''),
 ('md', '반경이 작으면 통신이 끊기고 음영이 넓습니다. 「안쪽에 갇힌 음영」은 센서망 속 **구멍**이에요. 안쪽에 갇힌 음영 가운데 가장 큰 곳 한가운데에 센서를 하나 더 놓아 봅니다.'),
 ('code', '''r = 26
gx, gy = np.meshgrid(np.arange(3, W, 6), np.arange(3, H, 6))
d = np.min(np.hypot(gx[..., None] - P[:, 0], gy[..., None] - P[:, 1]), axis=2)
lab, k = ndimage.label(d > r)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
sizes = np.bincount(lab.ravel()); sizes[0] = 0
for b in border: sizes[b] = 0                                   # 가장자리 빈 곳 말고 안쪽에 갇힌 구멍만
big = sizes.argmax()
new = np.array([[gx[lab == big].mean(), gy[lab == big].mean()]])
print('추가 전:', analyze(r)[:2], ' 추가 후:', analyze(r, np.vstack([P, new]))[:2])'''),
]),
'29_tda': ('29장 · 위상 데이터 분석(TDA) — 점 구름의 모양을 바코드로', [
 ('md', '잡음 섞인 원 위의 점 구름과 아무 모양 없는 점 구름에 **지속 호몰로지**(ripser)를 계산해, 오래 버티는 구멍 막대(H₁)가 있는지 봅니다.'),
 ('code', '''import numpy as np
from ripser import ripser

rng = np.random.default_rng(5)
n = 60
t = 2 * np.pi * rng.random(n)
circle = np.column_stack([np.cos(t), np.sin(t)]) + 0.12 * rng.standard_normal((n, 2))
blob = 0.6 * rng.standard_normal((n, 2))

for name, X in [('원 + 잡음', circle), ('뭉친 점', blob)]:
    h1 = ripser(X)['dgms'][1]
    life = (h1[:, 1] - h1[:, 0]) if len(h1) else np.array([0.0])
    print(f"{name:<6} H1 막대 {len(h1):>2}개, 가장 긴 막대 {life.max():.2f}, 둘째 {np.sort(life)[-2] if len(life) > 1 else 0:.2f}")'''),
 ('md', '원은 막대 하나가 압도적으로 길고(진짜 구멍), 뭉친 점은 짧은 막대뿐(잡음)입니다. 이번에는 이산 모스 이론의 생각 — **중요한 자리만 남기기** — 을 1차원 땅 높이로 확인합니다.'),
 ('code', '''h = [6,3,5,8,2,4,7,9,5,1,3,6,8,4,6,10,7,3,5,8]     # 페이지의 「물 빠지기」 실험과 같은 땅

def sublevel_pairs(h):
    """물 높이를 올리며 웅덩이가 생기고(골짜기) 합쳐지는(봉우리) 높이를 짝짓기 — 나이 많은 웅덩이가 살아남음"""
    n = len(h); parent = list(range(n)); born = {}; active = set(); pairs = []
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in sorted(range(n), key=lambda i: (h[i], i)):
        active.add(i); born[i] = h[i]
        for j in (i - 1, i + 1):
            if j in active:
                a, b = find(i), find(j)
                if a == b: continue
                young, old = (a, b) if born[a] > born[b] else (b, a)
                if born[young] < h[i]: pairs.append((born[young], h[i]))
                parent[young] = old
    pairs.append((min(h), float('inf')))
    return sorted(pairs)

P = sublevel_pairs(h)
mins = sum(1 for i, v in enumerate(h) if (i == 0 or h[i-1] > v) and (i == len(h)-1 or h[i+1] > v))
print('웅덩이 막대 (생김 → 합쳐짐):', P)
print(f'땅 {len(h)}자리 중 골짜기 바닥 {mins}곳만 막대를 만든다 → 나머지는 계산에서 빼도 됨 (이산 모스의 생각)')'''),
]),
}


def main():
    for key, (title, cells) in NB.items():
        nb = nbformat.v4.new_notebook()
        nb.cells.append(nbformat.v4.new_markdown_cell('# ' + title + '\n\n이산위상 연구실 활용 편 · 글 안상선. 그대로 위에서부터 실행하면 돼요.'))
        nb.cells.append(nbformat.v4.new_code_cell(SETUP))
        for kind, src in cells:
            nb.cells.append(nbformat.v4.new_markdown_cell(src) if kind == 'md' else nbformat.v4.new_code_cell(src))
        nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
        NotebookClient(nb, timeout=240, kernel_name='python3', resources={'metadata': {'path': OUT}}).execute()
        p = os.path.join(OUT, key + '.ipynb'); nbformat.write(nb, p)
        print('==', key)
        for c in nb.cells:
            if c.cell_type == 'code':
                for o in c.get('outputs', []):
                    if o.get('output_type') == 'stream': print(o['text'].rstrip())
                    if o.get('output_type') == 'error': print('ERROR', o['ename'], o['evalue'])


if __name__ == '__main__':
    main()
