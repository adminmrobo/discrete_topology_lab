#!/usr/bin/env python3
"""캐릭터 팩에서 표정 그림을 더 가져와 assets/sprites.js에 넣는다 (96px WebP, 배경 투명).
사용: python3 tools/add_sprites.py <캐릭터 팩 폴더>"""
import base64, io, json, os, re, sys
from collections import deque
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = {'asst': 'haru', 'doc': 'doctor', 'fly': 'fruitfly', 'robo': 'jupanbot', 'sia': 'sia', 'moa': 'moa'}
WANT = {'sia': ['E01', 'E05', 'E15', 'E19', 'E20', 'E21', 'E24'], 'moa': ['E05', 'E15', 'E16', 'E20', 'E21', 'E24'],
        'asst': ['E04', 'E08', 'E19', 'E25'], 'doc': ['E01'], 'fly': ['E09']}


def clear_bg(im, tol=22):
    im = im.convert('RGBA'); w, h = im.size; px = im.load()
    if px[2, 2][3] == 0:
        return im
    seen = set(); q = deque()
    for x in range(w):
        q.append((x, 0)); q.append((x, h - 1))
    for y in range(h):
        q.append((0, y)); q.append((w - 1, y))
    ref = px[2, 2]
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h):
            continue
        seen.add((x, y)); r, g, b, a = px[x, y]
        if max(abs(r - ref[0]), abs(g - ref[1]), abs(b - ref[2])) > tol or max(r, g, b) - min(r, g, b) > 14:
            continue
        px[x, y] = (r, g, b, 0)
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return im


def main(pack):
    p = os.path.join(ROOT, 'assets', 'sprites.js'); js = open(p, encoding='utf-8').read()
    m = re.search(r'var SPRITE=(\{.*?\});', js, re.S); S = json.loads(m.group(1))
    for who, codes in WANT.items():
        d = os.path.join(pack, 'images', FOLDER[who])
        for c in codes:
            f = [x for x in sorted(os.listdir(d)) if x.startswith(c + '_')][0]
            im = clear_bg(Image.open(os.path.join(d, f)))
            side = max(im.size); sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
            sq = sq.resize((96, 96), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'WEBP', quality=90, method=6)
            S['%s_%s' % (who, c.lower())] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
            print('added', who, c, f)
    js = js[:m.start(1)] + json.dumps(S, separators=(',', ':')) + js[m.end(1):]
    js = re.sub(r'/\* 캐릭터 팩 .*?\*/', '/* 캐릭터 팩 https://github.com/adminmrobo/fruitfly-lab-expressions, 96px, %d장 */' % len(S), js, 1)
    open(p, 'w', encoding='utf-8').write(js)


if __name__ == '__main__':
    main(sys.argv[1])
