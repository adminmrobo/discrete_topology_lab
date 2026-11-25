#!/usr/bin/env python3
"""공유 미리보기(og) 임시 그림: 표지 그림이 나오기 전까지 쓰는 1200×630 픽셀 열지도 + 바람길 + 제목.
표지(img/cover/cover_NN.webp)가 생기면 그 그림을 잘라 다시 만든다."""
import os, sys, math, random, importlib.util
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
HEAT = [(30, 85, 200), (47, 143, 111), (19, 115, 58), (154, 163, 26), (216, 162, 26), (224, 122, 26)]


def og_from_cover(key, ckey, title, label):
    """표지가 있으면: 표지를 높이 630에 맞춰 왼쪽에 두고, 비워 둔 오른쪽에 제목을 쓴다."""
    cp = os.path.join(ROOT, 'img', 'cover', ckey + '.webp')
    if not os.path.exists(cp):
        return False
    c = Image.open(cp).convert('RGB'); w = round(c.width * 630 / c.height)
    c = c.resize((w, 630), Image.LANCZOS)
    big = Image.new('RGB', (1200, 630), 'white'); big.paste(c, (0, 0)); d = ImageDraw.Draw(big)
    x0 = 640; d.rectangle([x0 - 16, 0, 1200, 630], fill='white')
    f1 = ImageFont.truetype(FONT, 26); f2 = ImageFont.truetype(FONT, 46)
    d.rectangle([x0, 90, x0 + d.textlength(label, font=f1) + 24, 134], fill=(22, 33, 43)); d.text((x0 + 12, 93), label, font=f1, fill='white')
    lines, cur = [], ''
    for wd in title.split(' '):
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=f2) > 520 and cur: lines.append(cur); cur = wd
        else: cur = t
    lines.append(cur)
    for i, l in enumerate(lines[:5]): d.text((x0, 160 + i * 64), l, font=f2, fill=(22, 33, 43))
    d.text((x0, 560), '이산위상 연구실 · 글 안상선', font=f1, fill=(91, 104, 116))
    big.save(os.path.join(ROOT, 'img', 'og', 'og_%s.webp' % key), quality=88)
    return True


def og(key, title, label):
    ckey = {'index': 'cover_00', 'practice': 'cover_practice'}.get(key, 'cover_' + key)
    if og_from_cover(key, ckey, title, label):
        return
    W, H, px = 300, 158, 1  # 1/4 격자에서 그린 뒤 4배 NEAREST
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    rnd = random.Random(sum(map(ord, key)))
    for y in range(0, H, 6):
        for x in range(0, W, 6):
            if rnd.random() < .5: d.point((x, y), fill=(214, 226, 236))
    cx, cy, R = 225, 92, 52
    for y in range(-R, R + 1, 3):
        for x in range(int(-R * 1.2), int(R * 1.2) + 1, 3):
            dd = math.sqrt(x * x / 1.44 + y * y) / R
            if dd > 1: continue
            lv = min(5, int((1 - dd) * 6 + rnd.random() * .6))
            d.rectangle([cx + x, cy + y, cx + x + 2, cy + y + 2], fill=HEAT[lv])
    big = im.resize((1200, 632), Image.NEAREST).crop((0, 0, 1200, 630)); d = ImageDraw.Draw(big)
    for k in range(5):
        y0 = 150 + k * 80; pts = [(x, y0 + math.sin(x / 1200 * 9 + k) * 22) for x in range(560, 1200, 8)]
        d.line(pts, fill=(22, 33, 43), width=4)
    f1 = ImageFont.truetype(FONT, 30); f2 = ImageFont.truetype(FONT, 54)
    d.rectangle([60, 70, 60 + d.textlength(label, font=f1) + 28, 120], fill=(22, 33, 43)); d.text((74, 74), label, font=f1, fill='white')
    words, lines, cur = title.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f2) > 620 and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    for i, l in enumerate(lines[:4]): d.text((60, 150 + i * 72), l, font=f2, fill=(22, 33, 43))
    d.text((60, 560), '이산위상 연구실 · 글 안상선', font=f1, fill=(91, 104, 116))
    os.makedirs(os.path.join(ROOT, 'img', 'og'), exist_ok=True)
    big.save(os.path.join(ROOT, 'img', 'og', 'og_%s.webp' % key), lossless=True)


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(ROOT, 'content'))
    for i in range(1, 30):
        sp = importlib.util.spec_from_file_location('m', os.path.join(ROOT, 'content', 'ch%02d.py' % i)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        og('%02d' % i, m.CH['title'], '%02d장 · %s' % (i, m.CH['pillar_name']))
    og('index', '이산위상 연구실 — 점 하나하나가 섬인 세상', '오리엔테이션')
    og('practice', '이산위상 사업장 시뮬레이터', '마지막 장 · 실전 연습장')
    print('og 31장')
