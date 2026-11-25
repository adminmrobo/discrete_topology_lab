import asyncio,sys
from playwright.async_api import async_playwright
async def m(page,sel,out,w=1280,clicks=()):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':w,'height':900})
        await pg.goto('file:///home/claude/discrete_topology_lab/'+page); await pg.wait_for_timeout(400)
        for c in clicks:
            await pg.click(c); await pg.wait_for_timeout(200)
        el=await pg.query_selector(sel); await el.screenshot(path=out)
        await b.close()
a=sys.argv; asyncio.run(m(a[1],a[2],a[3],int(a[4]) if len(a)>4 else 1280,a[5:]))
