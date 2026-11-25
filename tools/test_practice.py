#!/usr/bin/env python3
"""실전 연습장 미션 판정 검사: 정답 조작을 흉내 내 판정이 「통과」로 바뀌는지, 조작 전에는 통과가 아닌지 확인"""
import asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_HELP = '''
window.T = {
  pane: k => document.getElementById('pane-' + k),
  click: (k, label, nth) => { const bs = [...T.pane(k).querySelectorAll('button')].filter(b => b.textContent.trim() === label); bs[nth || 0].click(); },
  slide: (k, label, v) => { const r = [...T.pane(k).querySelectorAll('input[type=range]')].find(x => x.getAttribute('aria-label') === label); r.value = v; r.dispatchEvent(new Event('input')); },
  stat: k => [...T.pane(k).querySelectorAll('.mstat')].map(s => s.textContent.trim()),
};'''


async def main():
    fails = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page()
        await pg.route('**/fonts.g*/**', lambda r: r.abort())
        await pg.goto('file://' + os.path.join(ROOT, 'practice', 'index.html'))
        await pg.evaluate(JS_HELP)
        async def stat(k):
            return await pg.evaluate('T.stat(%r)' % k)
        def expect(name, got, want):
            ok = all((g.startswith('통과')) == w for g, w in zip(got, want))
            print(('OK  ' if ok else 'FAIL'), name, got)
            if not ok: fails.append(name)
        for k in ('map', 'tile', 'clock'):
            expect(k + ' 시작 상태(통과 없음)', await stat(k), [False, False, False])
        # 지도: 땅 8, 물 4 → 미션1 / 물 8 → 미션2 / 물 4로 돌리고 B, C 방문 → 미션3
        await pg.evaluate("T.click('map','8-이웃 (왕 걸음)',0)")
        expect('map 미션1 (8/4)', await stat('map'), [True, False, False])
        await pg.evaluate("T.click('map','8-이웃 (왕 걸음)',1)")
        expect('map 미션2 (8/8 관찰)', (await stat('map'))[1:2], [True])
        await pg.evaluate("T.click('map','4-이웃 (십자)',1)")
        for m in ('지도 B · 대각선 강과 두 섬', '지도 C · 체크무늬 갯벌'):
            await pg.evaluate("T.click('map',%r,0)" % m)
        expect('map 미션3 (A·B·C 유지)', (await stat('map'))[2:], [True])
        # 타일: v = (1, 1) → 행렬식 1, 비표준 → 미션1 / u = (1, 1) → 납작 → 미션2 / 다시 u = (1, 0), 추가 공사비 40 → 미션3
        await pg.evaluate("T.slide('tile','v의 x',1)")
        expect('tile 미션1 (넓이 1 비표준)', (await stat('tile'))[:1], [True])
        await pg.evaluate("T.slide('tile','u의 y',1)")
        expect('tile 미션2 (납작)', (await stat('tile'))[1:2], [True])
        await pg.evaluate("T.slide('tile','u의 y',0)")
        await pg.evaluate("T.slide('tile','빠진 구멍 하나 추가 공사비(천 원)',45)")
        expect('tile 미션3 (두 환경)', (await stat('tile'))[2:], [True])
        # 시계탑: −1 채우기 → 미션1 / 2층 −1 → 미션2 / K = 6, −1 채우기 → 미션3
        await pg.evaluate("T.click('clock','정수 −1로 채우기')")
        expect('clock 미션1 (−1)', (await stat('clock'))[:1], [True])
        await pg.evaluate("T.click('clock','−1',1)")
        expect('clock 미션2 (어긋남 관찰)', (await stat('clock'))[1:2], [True])
        await pg.evaluate("T.slide('clock','시계탑 층 수 K',6)")
        await pg.evaluate("T.click('clock','정수 −1로 채우기')")
        expect('clock 미션3 (층 수 바꿔 유지)', (await stat('clock'))[2:], [True])
        await b.close()
    print('실패', len(fails))
    return len(fails)


if __name__ == '__main__':
    sys.exit(1 if asyncio.run(main()) else 0)
