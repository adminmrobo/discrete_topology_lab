#!/usr/bin/env python3
"""이산위상 연구실 조립 스크립트.
content/chNN.py(챕터 데이터) → NN_slug.html, content/index_data.py → index.html
사용: python3 tools/build.py [--sprites PATH_TO_character_pack]
"""
import importlib.util, json, re, os, sys, html, glob, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'content'))
from common import REFS, AUTHOR, SITE, SERIES, CHAPTERS, PEOPLE  # noqa

TODAY = '2026-11-25'
PXFIX = open(os.path.join(ROOT, 'tools', 'pxfix.html'), encoding='utf-8').read().strip()
USED = set()  # (who, mood)


def esc(s):
    return html.escape(str(s), quote=True)


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, 'content', name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


GLOSS = {}


def rich(s):
    """[[용어]] → 용어 말풍선, 그 외 HTML은 그대로"""
    def rep(m):
        t = m.group(1)
        key, _, shown = t.partition('|')
        shown = shown or key
        d = GLOSS.get(key)
        if not d:
            return shown
        return '<span class="jt" data-t="%s" data-d="%s">%s</span>' % (esc(key), esc(d), shown)
    s = MAT.sub(matrep, str(s))
    return re.sub(r'\[\[(.+?)\]\]', rep, s)


MAT = re.compile(r'\[\[([^\[\]]+?), ([^\[\]]+?)\], \[([^\[\]]+?), ([^\[\]]+?)\]\]')


def matrep(m):
    a, b, c, d = m.groups()
    return ('<span class="mat" role="img" aria-label="2×2 행렬: 첫 줄 %s, %s / 둘째 줄 %s, %s"><span class="br" aria-hidden="true">[</span>'
            '<span class="cells" aria-hidden="true"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></span><span class="br" aria-hidden="true">]</span></span>') % (a, b, c, d, a, b, c, d)


def img(who, mood, cls='who', extra=''):
    USED.add((who, mood))
    return '<img class="%s" data-who="%s" data-mood="%s" alt="" aria-hidden="true"%s>' % (cls, who, mood, extra)


def say(who, mood, text, name=None):
    nm = name or PEOPLE[who][0]
    return '<div class="say" data-who="%s">%s<div><b class="name">%s</b><p>%s</p></div></div>' % (
        who, img(who, mood), esc(nm), rich(text))


def says(lst):
    return ''.join(say(*x) for x in lst)


def head(title, desc, depth=0, og=None):
    up = '../' * depth
    og = og or (up + 'img/og/og_index.webp')
    return f'''<!DOCTYPE html><html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="article">
<meta property="og:image" content="{esc(og)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/lab.css">
{PXFIX}
</head><body>'''


def foot_scripts(depth=0, kg=True):
    up = '../' * depth
    s = f'<script src="{up}assets/sprites.js"></script><script src="{up}assets/widgets.js"></script><script src="{up}assets/lab.js"></script>'
    if kg:
        s += f'<script src="{up}assets/js/kgx.js"></script>'
    return s + '</body></html>'


def footer_html(prev, nxt, extra=''):
    p = '<a href="%s">← %s</a>' % (prev[0], esc(prev[1])) if prev else '<span></span>'
    n = '<a href="%s">%s →</a>' % (nxt[0], esc(nxt[1])) if nxt else '<span></span>'
    return f'''<footer><div class="wrap">{extra}
<div class="nextprev">{p}{n}</div>
<p>글 · {AUTHOR['name']} (<a href="{AUTHOR['site']}">{AUTHOR['site']}</a>) · {AUTHOR['org']}</p>
<p class="note">시리즈 「{SERIES}」 · 캐릭터 그림은 연구실 캐릭터 팩(adminmrobo/fruitfly-lab-expressions)을 쓰며 허락 없이 다시 쓸 수 없습니다.</p>
</div></footer>'''


# ───────────────────────── 지식 그래프 자동 생성 ─────────────────────────
def build_kg(ch):
    page = ch['slug']
    nodes, edges = [], []
    topic = 'lab:topic/' + ch['kgid']
    nodes.append({'id': topic, 'type': 'Topic', 'label': {'ko': ch['title'], 'en': ch['en']}, 'page': page, 'anchor': '#top',
                  'status': 'known', 'confidence': 'high', 'domain': ['math'], 'family': 'discrete-topology',
                  'definition': {'ko': ch['q']}})
    prev = None
    for i, st in enumerate(ch['stages'], 1):
        k = st['kg']
        cid = 'lab:concept/' + k['id']
        nodes.append({'id': cid, 'type': k.get('type', 'Concept'), 'label': {'ko': k['ko'], 'en': k['en']},
                      'definition': {'ko': k['def']}, 'page': page, 'anchor': '#lv%d' % i, 'level': min(5, 1 + ch['no'] // 4),
                      'status': 'known', 'confidence': 'high', 'domain': ['math'], 'family': 'discrete-topology',
                      'evidence': k.get('ev', []), 'source': [{'cite': r} for r in k.get('refs', [])], 'match': [],
                      'tags': [ch['title']]})
        edges.append({'s': cid, 'p': 'lab:partOf', 'o': topic})
        if prev:
            edges.append({'s': prev, 'p': 'lab:prerequisiteOf', 'o': cid})
        prev = cid
        an = 'lab:analogy/' + k['id'] + '-daily'
        nodes.append({'id': an, 'type': 'Analogy', 'label': {'ko': st['pair'][2] if len(st['pair']) > 2 else '일상 비유', 'en': 'analogy'},
                      'definition': {'ko': re.sub('<.*?>|\\[\\[|\\]\\]', '', st['pair'][0])[:140]}, 'page': page, 'anchor': '#lv%d' % i,
                      'status': 'known', 'confidence': 'mid', 'domain': ['math'], 'match': []})
        edges.append({'s': an, 'p': 'lab:analogyOf', 'o': cid})
        lim = 'lab:limitation/' + k['id']
        nodes.append({'id': lim, 'type': 'Limitation', 'label': {'ko': '한계: ' + k['ko'], 'en': 'limitation of ' + k['en']},
                      'definition': {'ko': re.sub('<.*?>|\\[\\[|\\]\\]', '', st['limit'])[:160]}, 'page': page, 'anchor': '#lv%d' % i,
                      'status': 'known', 'confidence': 'mid', 'domain': ['math'], 'match': []})
        edges.append({'s': cid, 'p': 'lab:hasLimitation', 'o': lim})
    for j, fx in enumerate(ch.get('fixes', []), 1):
        cl = 'lab:claim/%s-fix%d' % (ch['kgid'], j)
        nodes.append({'id': cl, 'type': 'Claim', 'label': {'ko': '원자료 바로잡기 %d' % j, 'en': 'correction %d' % j},
                      'definition': {'ko': re.sub('<.*?>', '', fx['text'])}, 'page': page, 'anchor': fx['anchor'],
                      'status': 'known', 'confidence': 'high', 'domain': ['math'],
                      'source': [{'cite': r, 'loc': fx.get('loc', '')} for r in fx['refs']], 'match': []})
        for r in fx['refs']:
            edges.append({'s': cl, 'p': 'lab:assertedIn', 'o': 'lab:work/' + r})
    q = 'lab:question/' + ch['kgid']
    nodes.append({'id': q, 'type': 'Question', 'label': {'ko': ch['q'], 'en': 'core question'}, 'page': page, 'anchor': '#top',
                  'status': 'known', 'confidence': 'high', 'domain': ['math'], 'match': []})
    edges.append({'s': topic, 'p': 'lab:raises', 'o': q})
    for pre in ch.get('pre', []):
        edges.append({'s': 'lab:concept/' + pre, 'p': 'lab:prerequisiteOf', 'o': 'lab:concept/' + ch['stages'][0]['kg']['id']})
    for r in ch['refs']:
        nodes.append({'id': 'lab:work/' + r, 'type': 'Work', 'label': {'ko': REFS[r]['title'], 'en': REFS[r]['title']},
                      'page': page, 'anchor': '#export', 'status': 'known', 'confidence': 'high', 'domain': ['math'], 'match': []})
    for st, k in [(s, s['kg']) for s in ch['stages']]:
        for r in k.get('refs', []):
            edges.append({'s': 'lab:concept/' + k['id'], 'p': 'lab:assertedIn', 'o': 'lab:work/' + r})
    ids = {x['id'] for x in nodes}
    edges = [e for e in edges if e['s'] in ids and e['o'] in ids]
    return {'version': '1.0', 'page': page, 'nodes': nodes, 'edges': edges}


def json_ld(kg, meta):
    ctx = {'@vocab': 'urn:lab:', 'lab': 'urn:lab:', 'skos': 'http://www.w3.org/2004/02/skos/core#', 'schema': 'https://schema.org/'}
    g = [{'@id': 'urn:lab:page/' + meta['number'], '@type': ['schema:LearningResource', 'schema:WebPage'], 'schema:name': meta['title'],
          'schema:inLanguage': 'ko', 'schema:educationalLevel': meta['educationalLevel'], 'schema:author': AUTHOR['name']}]
    for n in kg['nodes']:
        o = {'@id': n['id'], '@type': ['lab:' + n['type']], 'skos:prefLabel': [{'@value': n['label']['ko'], '@language': 'ko'}]}
        if n.get('definition'):
            o['skos:definition'] = [{'@value': n['definition']['ko'], '@language': 'ko'}]
        g.append(o)
    return {'@context': ctx, '@graph': g}


def refs_csl(ids):
    out = []
    for r in ids:
        R = REFS[r]
        out.append({'id': r, 'type': R['type'], 'title': R['title'], 'author': R['author'],
                    'issued': {'date-parts': [[R['year']]]} if R.get('year') else {},
                    'publisher': R.get('publisher', ''), 'container-title': R.get('container', ''),
                    'volume': R.get('volume', ''), 'page': R.get('pages', ''),
                    'lab': {'work': 'lab:work/' + r, 'role': R.get('role', 'background'), 'supports': [], 'locs': [],
                            'verified': R['verified']}})
    return out


def page_meta(ch):
    return {'title': ch['title'], 'number': '%02d' % ch['no'], 'series': SERIES, 'about': ['lab:topic/' + ch['kgid']],
            'basedOn': ch['refs'], 'educationalLevel': '입문 (중학생 이상)', 'creator': [{'name': AUTHOR['name'], 'role': 'author'}],
            'contributor': [{'name': 'AI 보조 제작', 'role': 'assistant'}], 'date': TODAY, 'version': '1.0', 'language': ['ko'],
            'license': '', 'url': SITE + ch['slug'] + '.html', 'registry': 'KG_00_registry 0.2',
            'learningResourceType': 'interactive explainer', 'seeAlso': '',
            'suggestedCitation': '%s (2026). %s. %s %02d, v1.0.' % (AUTHOR['name'], ch['title'], SERIES, ch['no'])}


def jscript(id_, obj, typ='application/json'):
    s = json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')
    return '<script type="%s" id="%s">%s</script>' % (typ, id_, s)


# ───────────────────────── 챕터 페이지 ─────────────────────────
LEVEL, MINUTES, BASIC = {}, {}, []
STARS = {1: '입문 ●○○', 2: '보통 ●●○', 3: '도전 ●●●'}
DEEP = set()
NICK = {}
GROUPS = ('픽셀조', '바람조')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content'))
try:
    from easy import EASY
except ImportError:
    EASY = {}


def chapter(ch, prevc, nextc):
    global GLOSS
    GLOSS = dict(ch.get('gloss', {}))
    n = ch['no']
    stg = ch['stages']
    navl = ''.join('<a href="#lv%d">%d단계%s</a>' % (i, i, '·심화' if (ch['no'], i) in DEEP else '') for i in range(1, len(stg) + 1))
    o = [head('%02d %s — %s' % (n, ch['title'], SERIES), ch['q'], og='img/og/og_%02d.webp' % n)]
    o.append(f'<nav class="top" aria-label="이 페이지 목차"><a class="logo" href="index.html">이산위상 연구실</a><a href="#easy">4컷·쉬운 길</a><a href="#three">3줄 요약</a><a href="#class">수업</a><a href="#map">큰 그림</a>{navl}<a href="#ai">AI 판단</a><a href="#duel">대결</a><a href="#sum">정리</a><a href="#kg">색인</a><a href="#export">꾸러미</a></nav><div id="prog"></div>')
    # 표지 (대체 표지)
    cc = ['doc', 'fly', 'robo', ch['star'][0]]
    cm = ['front', 'magnify', 'smile', ch['star'][1]]
    chars = ''.join(img(w, m, cls='', extra=(' class="flipx"' if False else '')) for w, m in zip(cc, cm))
    o.append(cover_html('cover_%02d' % n, ch['title'], '%s · %02d장' % (ch['pillar_name'], n), ch['sub'], '%s 표지 — 박사, 초파리 연구원, 주판봇, %s' % (ch['title'], PEOPLE[ch['star'][0]][0]), chars=list(zip(cc, cm))))
    # 히어로
    kp = ''.join('<div class="kpi %s"><b>%s</b><span>%s</span></div>' % (c, esc(v), rich(t)) for c, v, t in ch['kpis'])
    o.append(f'''<header class="hero"><div class="wrap">
<div class="kicker">{esc(ch['pillar_name'])} · {n:02d}장 · 오늘의 수업: {esc(ch['format'][0])} · {'기본 과정' if n in BASIC else '심화 과정'} · 난이도 {STARS[LEVEL.get(n, 2)]} · 쉬운 길 약 5분 · 본편 약 {MINUTES.get(n, 25)}분{' + 심화 단계 약 10분' if (n, 3) in DEEP else ''}</div>
<h1>{esc(ch['title'])}</h1>
<p class="q">핵심 질문 — {esc(ch['q'])}</p>
<p>{rich(ch['intro'])}</p>
<div class="kpis">{kp}</div>
<p class="note">숫자 요약은 이 장의 예시 계산에서 나온 값입니다(실제 데이터가 아닌 설명용 값).</p>
{says(ch['hero_say'])}
</div></header>''')
    # 3줄
    ab = ''.join('<li><b>%s</b> — %s</li>' % (esc(a), esc(b)) for a, b in ch.get('abbr', []))
    o.append(f'''<div class="wrap"><div class="three" id="three"><h2>처음 오신 분께 — 이 페이지를 3줄로</h2><ol>
<li><b>무엇을:</b> {rich(ch['three'][0])}</li><li><b>왜 중요한가:</b> {rich(ch['three'][1])}</li><li><b>생활·현장에서는:</b> {rich(ch['three'][2])}</li></ol>
<p class="note">행렬·벡터, 복잡한 공식을 몰라도 됩니다. 그림을 움직여 보고, 밑줄 친 말을 누르면 뜻이 나옵니다.</p>
{('<details><summary>영어 기호·약어 풀이 (펼치기)</summary><ul>'+ab+'</ul></details>') if ab else ''}
</div>{infog_html(ch)}</div>''')
    # 쉬운 길: 하루의 몰래 4컷 + 쉬운 비유 + 쉬운 퀴즈 + 이론 구간 안내
    o.append(easy_html(ch, nextc))
    # 등장인물
    castl = ''.join('<div>%s<div><span class="role">%s</span><b>%s</b><span>%s</span></div></div>' % (
        img(w, PEOPLE[w][2], cls=''), esc(PEOPLE[w][1]), esc(PEOPLE[w][0]), esc(ch.get('castnote', {}).get(w, PEOPLE[w][3]))) for w in
        ['doc', 'fly', 'robo', 'sia', 'moa', 'asst', 'x1', 'x2', 'x3'])
    prevlink = '<a href="%s">%s</a>' % (prevc[0], esc(prevc[1])) if prevc else '없음 (첫 장)'
    o.append(f'''<section class="level" id="cast"><div class="wrap"><details><summary><b>등장인물 — 선생님 1명, 조교 2명, 수강생 6명</b> (펼치기)</summary>
<div class="cast">{castl}</div>
{nick_html(n)}
<p class="note">이 페이지 사용법: 밑줄 친 말을 누르면 뜻이 나옵니다(Esc로 닫기). 단계마다 그림을 직접 움직여 보고, 끝의 확인 퀴즈로 점검하세요. 앞 장: {prevlink}</p>
</details></div></section>''')
    # 수업 형식
    k = ch['klass']
    groups = ''
    if k.get('groups', True):
        g1 = ''.join(img(w, 'e13', cls='') for w in ['sia', 'asst', 'x1'])
        g2 = ''.join(img(w, 'e13', cls='') for w in ['moa', 'x2', 'x3'])
        groups = f'<div class="groups"><div>{g1} <b>1조 「{GROUPS[0]}」</b> 시아 · 하루 · X1</div><div>{g2} <b>2조 「{GROUPS[1]}」</b> 모아 · X2 · X3</div></div>'
    flow = ''.join('<li>%s</li>' % rich(x) for x in k['flow'])
    o.append(f'''<section class="level" id="class"><div class="wrap"><h2>오늘의 수업 — {esc(ch['format'][0])}</h2>
<div class="klass"><span class="fmt">{esc(ch['format'][0])}</span><p>{rich(ch['format'][1])}</p>{groups}<ol>{flow}</ol></div>
<div class="talk">{says(k['talk'])}</div></div></section>''')
    # 왜
    wy = ''.join('<div><b class="n">%d</b><b>%s</b><p>%s</p></div>' % (i + 1, esc(a), rich(b)) for i, (a, b) in enumerate(ch['why']))
    o.append(f'<section class="level" id="why"><div class="wrap"><h2>왜 이 주제를 배우나</h2><div class="steps">{wy}</div></div></section>')
    # 큰 그림
    m = ch['map']
    rc = ''.join('<div class="recap"><b>30초 복습 — %s</b><br>%s</div>' % (esc(a), rich(b)) for a, b in ch.get('recap', []))
    o.append(f'''<section class="level" id="map"><div class="wrap"><h2>큰 그림 — 지금 어디쯤 있나</h2>
<div class="map3"><div><small>앞에서 배운 것</small>{rich(m[0])}</div><i aria-hidden="true">→</i><div class="now"><small>이번 장</small>{rich(m[1])}</div><i aria-hidden="true">→</i><div><small>다음에 쓰는 곳</small>{rich(m[2])}</div></div>
{rc}<p>{rich(m[3])}</p></div></section>''')
    # 단계
    for i, st in enumerate(stg, 1):
        h = stage_html(ch, i, st)
        if (ch['no'], i) in DEEP:
            h = ('<div class="wrap"><details class="deepbox"><summary><b>%d단계 · 심화 — %s</b><br><span class="note">이 장에서 가장 어려운 단계예요. 접어 둔 채 넘어가도 다음 장과 조교 대결을 읽는 데 문제없어요. 궁금하면 펼쳐 보세요.</span></summary></div>' % (i, esc(st['title']))
                 + h + '<div class="wrap"></details></div>')
            h = h.replace('<div class="wrap"></details></div>', '</details></div>').replace('</summary></div>', '</summary>', 1)
        o.append(h)
    # AI 판단 코너
    a = ch['ai']
    o.append(f'''<section class="level" id="ai"><div class="wrap"><div class="aic"><h3>AI 판단 코너 — AI가 낸 답, 그대로 믿어도 될까?</h3>
<p>{rich(a['setup'])}</p><div class="aiout">{esc(a['out'])}</div>
<div class="quiz" data-quiz="ai"></div>
{say('doc', 'board', a['doc'])}</div></div></section>''')
    # 대결
    d = ch['duel']
    o.append(f'''<section class="level" id="duel"><div class="wrap"><h2>조교 대결 — {esc(d['title'])}</h2>
<p>{rich(d['setup'])}</p>
<div class="duel"><div class="vs"><div class="side fly">{img('fly', 'point', cls='')}<b style="color:var(--c-fly)">초파리 연구원</b><p>「{rich(d['fly'])}」</p></div>
<div class="vsm" aria-hidden="true">VS</div>
<div class="side robo">{img('robo', 'calc', cls='')}<b style="color:var(--c-robo)">주판봇</b><p>「{rich(d['robo'])}」</p></div></div>
<div class="ctrl" style="justify-content:center"><button class="bt primary duel-run" type="button">계산으로 판정하기</button></div>
<div class="verdict" aria-live="polite"><p class="note">누가 맞을지 먼저 예상해 보고 단추를 누르세요. 판정은 계산 결과로만 합니다.</p></div></div>
{('<div class="panel"><div class="ptitle">판정 계산 들여다보기</div><div data-w="%s" data-o="%s"></div></div>' % (d['w'], esc(json.dumps(d.get('o', {}), ensure_ascii=False)))) if d.get('w') else ''}
</div></section>''')
    USED.update({('fly', 'e16'), ('fly', 'cry'), ('robo', 'happy'), ('robo', 'cry'), ('asst', 'report'), ('doc', 'verdict')})
    # 정리
    rows = ''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (rich(a), rich(b), rich(c), rich(e)) for a, b, c, e in ch['sum'])
    chain = ' → '.join('<span class="tag nn">%s</span>' % esc(s['kg']['ko']) for s in stg)
    o.append(f'''<section class="level" id="sum"><div class="wrap"><h2>정리 — 개념정리 한눈에</h2>
{flow_html(ch, prevc, nextc)}
<p>개념정리 흐름: {chain}</p>
<div class="tw"><table class="tb"><thead><tr><th>개념</th><th>한 줄 뜻</th><th>일상 비유</th><th>비유의 한계</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>''')
    # 아웃트로
    o.append(f'''<section class="level" id="outro"><div class="wrap"><h2>수업을 마치며</h2><div class="outro">{says(ch['outro'])}</div>
<p class="note">다음 장 예고: {rich(ch['next_hint'])}</p></div></section>''')
    # 지식 색인 + 꾸러미
    o.append('<section class="level" id="kg"><div class="wrap"><h2>지식 색인 — 이 페이지에서 찾아보기</h2><div id="kg-mount"></div></div></section>')
    o.append('<section class="level" id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미 — 이 페이지의 지식을 가져가기</h2><div id="export-mount"></div></div></section>')
    # 바닥글
    srcrows = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (esc(REFS[r]['short']), esc(REFS[r]['use'])) for r in ch['refs'])
    examples = ''.join('<li>%s</li>' % rich(x) for x in ch['examples'])
    extra = f'''<h3>출처</h3><div class="tw"><table class="tb"><thead><tr><th>자료</th><th>이 페이지에서 쓴 곳</th></tr></thead><tbody>{srcrows}</tbody></table></div>
<h3>예시값·설명용 모형인 것</h3><ul>{examples}</ul>'''
    if n in BASIC and n != BASIC[-1]:
        nb = BASIC[BASIC.index(n) + 1]
        nc = [c for c in ALL if c['no'] == nb][0]
        if nextc and not nextc[0].startswith(nc['slug']):
            extra += '<p class="rest"><b>기본 과정만 따라가는 중이라면</b> 다음은 <a href="%s.html">%02d %s</a>예요. (사이의 장은 심화 과정)</p>' % (nc['slug'], nb, esc(nc['title']))
    o.append(footer_html(prevc, nextc, extra))
    kg = build_kg(ch)
    meta = page_meta(ch)
    quiz = {('q%d' % i): mix(s['quiz'], n * 10 + i) for i, s in enumerate(stg, 1)}
    quiz['ai'] = mix(a['quiz'], n * 10 + 9)
    if EASY.get(n):
        quiz['qe'] = mix([EASY[n]['quiz']], n * 10 + 7)
    o.append(jscript('page-data', {'quiz': quiz, 'duel': {'run': d['run'], 'lesson': d['lesson'], 'calc': d.get('calc')}}))
    o.append(jscript('kg-raw', kg))
    o.append(jscript('kg-ld', json_ld(kg, meta), 'application/ld+json'))
    o.append(jscript('refs-csl', refs_csl(ch['refs'])))
    o.append(jscript('page-meta', meta))
    o.append(foot_scripts())
    return '\n'.join(o)


def mix(items, seed):
    """정답 자리가 한쪽에 몰리지 않게 선택지 순서를 정해진 규칙으로 돌린다(빌드마다 같은 결과)."""
    out = []
    for j, q in enumerate(items):
        k = (seed * 7 + j * 3) % len(q['o'])
        o = q['o'][k:] + q['o'][:k]
        out.append(dict(q, o=o, a=(q['a'] - k) % len(q['o'])))
    return out


def infog_html(ch):
    d = None
    if not d:
        return ''
    cards = ''.join('<div class="ic"><b class="n">%d</b><div><b>%s</b><p>%s</p></div></div>' % (i + 1, esc(h), rich(t)) for i, (h, t) in enumerate(d['cards']))
    return ('<figure class="infog" id="infog"><div class="ihead"><span>한눈에 보기 · 원자료 인포그래픽 한국어판</span><b>%s</b></div>'
            '<div class="ibody"><div class="icards">%s</div><div class="idia">%s<figcaption>%s</figcaption></div></div>'
            '<p class="note">원자료(영어) 그림 %02d번을 한국어로 다시 그렸어요. 원자료에서 바로잡은 곳은 이 그림에 이미 반영했어요.</p></figure>') % (
        esc(d['title']), cards, DIA[d['dia']](), esc(d['cap']), d['src'])


def flow_html(ch, prevc, nextc):
    nk = {a: b for a, b, c in NICK.get(ch['no'], [])}
    items = []
    for i, st in enumerate(ch['stages'], 1):
        k = st['kg']
        deep = (ch['no'], i) in DEEP
        items.append('<div class="fs%s"><small>%d단계%s</small><b>%s</b><span>%s</span></div>' % (
            ' deep' if deep else '', i, ' · 심화' if deep else '', esc(k['ko']), esc(st['pair'][2] if len(st['pair']) > 2 else '')))
    pv = '<div class="fe"><small>앞에서</small><span>%s</span></div>' % rich(ch['map'][0])
    nx = '<div class="fe"><small>다음에 쓰는 곳</small><span>%s</span></div>' % rich(ch['map'][2])
    arrow = '<i aria-hidden="true">→</i>'
    return ('<figure class="flowmap"><div class="ihead"><span>한 장 정리 그림</span><b>%s — 개념이 이어지는 길</b></div><div class="frow">%s</div>'
            '<figcaption>%s</figcaption></figure>') % (esc(ch['title'].split(' — ')[0]), arrow.join([pv] + items + [nx]), rich(ch['stages'][-1]['interp'] if not (ch['no'], len(ch['stages'])) in DEEP else ch['stages'][0]['interp']))


def cover_html(key, title, label, subt, alt, up='', chars=None):
    fp = os.path.join(ROOT, 'img', 'cover', key + '.webp')
    if os.path.exists(fp):
        try:
            from PIL import Image
            cw, chh = Image.open(fp).size
        except Exception:
            cw, chh = 1920, 1080
        return (f'<div class="cover has-img" id="top"><img class="cimg" src="{up}img/cover/{key}.webp" width="{cw}" height="{chh}" alt="{esc(alt)}">'
                f'<div class="ctext"><span class="no">{esc(label)}</span><h1>{esc(title)}</h1><p>{esc(subt)}</p></div></div>')
    cc = ''.join(img(w, m, cls='') for w, m in (chars or [('doc', 'front'), ('fly', 'magnify'), ('robo', 'smile'), ('asst', 'smile')]))
    seed = sum(map(ord, key)) % 97 + 3
    return (f'<div class="cover" id="top" role="img" aria-label="{esc(alt)}"><canvas class="bgpx" data-seed="{seed}" data-motif="{seed % 4}" aria-hidden="true"></canvas>'
            f'<span class="badge">표지 그림 준비 중 · docs/IMG_specs.md</span><div class="cchars">{cc}</div>'
            f'<div class="ctext"><span class="no">{esc(label)}</span><h1>{esc(title)}</h1><p>{esc(subt)}</p></div></div>')


def nick_html(n):
    rows = NICK.get(n, [])
    if not rows:
        return ''
    cards = ''.join('<div><span class="role">원래 이름: %s</span><b>%s</b><span>%s</span></div>' % (esc(a), esc(b), esc(c)) for a, b, c in rows)
    return '<h3>용어 별명 카드 — 어려운 이름은 별명으로 기억하세요</h3><div class="nick">%s</div>' % cards


def theory_fold(title, inner):
    faces = img('sia', 'e27', cls='pain') + img('moa', 'e27', cls='pain')
    return ('<details class="theory"><summary><span class="tfaces">%s</span><span><b>이론 구간 — %s</b><br><span class="note">시아·모아도 머리를 감싼 곳이에요. 몰라도 그림 실험과 풀이를 따라올 수 있어요. 궁금하면 펼쳐 보세요.</span></span></summary>%s</details>' % (faces, esc(title), inner))


def comic_html(n, c):
    p1, p2, p3, p4 = c['panels']
    cap4 = c.get('cap4', '박사는 멀리서 못 본 척 웃었다.')
    def bub(who, t):
        return '<p class="bub b-%s"><b>%s</b>%s</p>' % (who, esc(PEOPLE[who][0].split(' ')[-1]), rich(t))
    panels = [
        ('pain', img('sia', 'e27', cls='') + img('moa', 'e27', cls=''), bub('sia', p1[0]) + bub('moa', p1[1]), '<span class="sfx" aria-hidden="true">지끈지끈</span>' + esc(c.get('cap1', '이론 시간. 시아와 모아가 머리를 감싸 쥐었다.'))),
        ('sneak', img('asst', 'e25', cls='') + img('sia', 'e05', cls='small') + img('moa', 'e05', cls='small'), bub('asst', p2), esc(c.get('cap2', '그때 하루가 박사 몰래 살금살금 다가왔다.'))),
        ('teach', img('asst', 'e08', cls=''), bub('asst', p3), esc(c.get('cap3', '하루의 비밀 설명 시간.'))),
        ('pop', img('sia', 'e19', cls='') + img('moa', 'e19', cls='') + img('asst', 'e16', cls='small'), bub('sia', p4[0]) + bub('moa', p4[1]), esc(cap4)),
    ]
    ps = ''.join('<div class="cp %s" data-step="%d"><span class="cno">%d</span><div class="cstage">%s</div><div class="cbubs">%s</div><p class="cc">%s</p></div>' % (k, i + 1, i + 1, im, bb, cc)
                 for i, (k, im, bb, cc) in enumerate(panels))
    return ('<figure class="comic" aria-label="하루의 몰래 4컷"><figcaption><b>하루의 몰래 4컷</b> — %s</figcaption><div class="cgrid">%s</div>'
            '<button type="button" class="bt creplay">4컷 다시 보기</button></figure>' % (esc(c['title']), ps))


def easy_html(ch, nextc):
    n = ch['no']; e = EASY.get(n)
    if not e:
        return ''
    gate = ('<div class="gate"><span class="tfaces">%s</span><div><b>여기까지가 「쉬운 길」이에요.</b> 아래부터는 단계별 설명과 그림 실험, 그리고 접혀 있는 이론 구간이에요. '
            '시아·모아처럼 머리가 지끈거리면 <a href="%s">다음 장으로 바로 가도</a> 괜찮아요. 그림 실험만 해 봐도 충분해요.</div></div>') % (
        img('sia', 'e20', cls='') + img('moa', 'e20', cls=''), nextc[0] if nextc else 'index.html')
    return ('<section class="level" id="easy"><div class="wrap"><h2>쉬운 길 — 4컷과 비유로 먼저 (약 5분)</h2>%s'
            '<div class="easybox"><div><h3>한 줄 핵심</h3><p class="one">%s</p></div><div><h3>쉬운 비유</h3>%s</div></div>'
            '<div class="quiz" data-quiz="qe"></div>%s</div></section>') % (
        comic_html(n, e['comic']), rich(e['one']), ''.join('<p>%s</p>' % rich(x) for x in e['analogy']), gate)


def stage_html(ch, i, st):
    o = ['<section class="level" id="lv%d"><div class="wrap">' % i]
    tags = ''.join('<span class="tag %s">%s</span>' % (('fly' if t.startswith('일상') else 'nn'), esc(t)) for t in st['tags'])
    o.append('<div class="lvhead"><div class="hex" aria-hidden="true">%d</div><div><h2>%d단계 · %s</h2>%s</div></div>' % (i, i, esc(st['title']), tags))
    o.append(say('doc', 'board', '<b>상황 질문</b> — ' + st['situ']))
    if st.get('recap'):
        o.append('<div class="recap"><b>30초 복습 — %s</b><br>%s</div>' % (esc(st['recap'][0]), rich(st['recap'][1])))
    w, f = st.get('why'), st.get('math')
    if w:
        o.append('<div class="whybox"><h3>왜 이 방법을 쓰나</h3><ol><li><b>문제 상황:</b> %s</li><li><b>앞 방법의 한계:</b> %s</li><li><b>해법:</b> %s</li></ol><div class="easy"><b>쉽게 말하면</b> — %s</div></div>' % (
            rich(w[0]), rich(w[1]), rich(w[2]), rich(w[3])))
    th = []
    if f:
        rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (rich(a), esc(b), rich(c)) for a, b, c in f['parts'])
        tryit = ''.join('<p>%s</p>' % rich(x) for x in f['try'])
        th.append('<div class="mathbox"><h3>수학 수식을 어려워하는 조수가 대신 물어봅니다</h3>%s<p><b>학교 수학으로 보면:</b> %s</p>'
                  '<table class="sym"><thead><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr></thead><tbody>%s</tbody></table>'
                  '<div class="tryit"><b>숫자로 한 번 해 보기</b>%s</div>%s</div>' % (
                      say('asst', 'shock', f['q'], name='조수 하루 (수강생)'), rich(f['school']), rows, tryit,
                      say('asst', 'spark', f['comment'], name='조수 하루 (수강생)')))
    if st.get('vec'):
        v = st['vec']
        th.append('<div class="vecbox"><h3>벡터·행렬 첫걸음 — %s</h3>%s<div class="tryit">%s</div><p class="note">%s</p></div>' % (
            esc(v['title']), ''.join('<p>%s</p>' % rich(x) for x in v['body']), ''.join('<p>%s</p>' % rich(x) for x in v['try']), rich(v.get('note', '행렬·벡터를 처음 본다면 이 상자는 건너뛰어도 본문을 따라올 수 있어요.'))))
    if th:
        o.append(theory_fold('수식으로 보기' + (' · 벡터·행렬 첫걸음' if st.get('vec') else ''), ''.join(th)))
    p = st['pair']
    scn = 'img/scene/scene_%02d_lv%d.webp' % (ch['no'], i)
    simg = ('<img class="scene" loading="lazy" src="%s" width="1200" height="800" alt="%s 장면 그림">' % (scn, esc(p[2] if len(p) > 2 else '일상 비유'))) if os.path.exists(os.path.join(ROOT, scn)) else ''
    o.append('<div class="pair"><div><span class="tag fly">일상으로 치면</span>' + simg + '<p>%s</p></div><div><span class="tag nn">이산위상에서는</span><p>%s</p></div></div>' % (rich(p[0]), rich(p[1])))
    o.append('<div class="talk">%s</div>' % says(st['talk']))
    o.append('<div class="panel"><div class="ptitle">%s</div><div data-w="%s" data-o="%s"></div></div>' % (
        esc(st['panel']), st['w'], esc(json.dumps(st.get('o', {}), ensure_ascii=False))))
    ex = ''.join('<li>%s</li>' % rich(x) for x in st['explain'])
    o.append('<div class="explain"><h3>풀이 — 한 걸음씩</h3><ol>%s</ol><div class="lim"><b>이 단계의 한계</b> — %s</div><div class="interp"><b>박사의 해석</b> — %s</div></div>' % (
        ex, rich(st['limit']), rich(st['interp'])))
    if st.get('rest'):
        o.append('<div class="rest">%s</div>' % rich(st['rest']))
    if st.get('code'):
        rows = ''.join('<tr><td><code>%s</code></td><td>%s</td></tr>' % (esc(c), rich(m)) for c, m in st['code'])
        nb = ch.get('notebook')
        o.append('<details class="codebox"><summary><b>파이썬으로 보면</b> (몰라도 됩니다 — 코드 한 줄 + 뜻 한 줄)</summary><div class="tw"><table class="tb"><thead><tr><th>코드</th><th>뜻</th></tr></thead><tbody>%s</tbody></table></div>%s</details>' % (
            rows, ('<p class="note">전체 코드와 실행 결과: <a href="%s">%s</a> (주피터 노트북, 그대로 실행돼요)</p>' % (nb, esc(nb.split('/')[-1]))) if nb else ''))
    if st.get('src'):
        s = st['src']
        fixes = ''.join('<div class="fix">%s</div>' % rich(x) for x in s.get('fix', []))
        o.append('<details><summary>원자료 인포그래픽 보기 (영어 그림 · 이론 구간)</summary><p class="note">%s</p>%s<img loading="lazy" src="img/source/src%02d.webp" width="1280" height="714" alt="%s"></details>' % (
            rich(s['cap']), fixes, s['n'], esc(s['alt'])))
    if st.get('expert'):
        o.append('<details><summary>더 알고 싶은 분께 — 정확한 정의 (몰라도 됩니다)</summary>%s</details>' % rich(st['expert']))
    o.append('<div class="quiz" data-quiz="q%d"></div>' % i)
    o.append('</div></section>')
    return ''.join(o)


GENERIC = {'think': 'e09', 'firm': 'e12', 'explain': 'e07', 'guide': 'e08', 'proud': 'e16', 'smile': 'e13', 'cheer': 'e12', 'sparkle': 'e19', 'shock': 'e24', 'cry': 'e21', 'report': 'e07', 'spark': 'e01', 'sigh': 'e02', 'doze': 'e17', 'tea': 'e01', 'ok': 'e10', 'point': 'e08', 'board': 'e07', 'calc': 'e09', 'happy': 'e12', 'wow': 'e04', 'meh': 'e18', 'blush': 'e14', 'chart': 'e07', 'coin': 'e16', 'clip': 'e10', 'arms': 'e16', 'magnify': 'e07', 'front': 'e08', 'judge': 'e10', 'verdict': 'e18'}


def sprites_local():
    p = os.path.join(ROOT, 'assets', 'sprites.js')
    js = open(p, encoding='utf-8').read()
    have = set(re.findall(r'"([a-z0-9]+_e\d\d)":"data:', js))
    alias, miss = {}, []
    for who, mood in sorted(USED):
        k = who + '_' + mood
        if re.match(r'^e\d\d$', mood):
            if k not in have: miss.append(k)
            continue
        t = {'robo_sigh': 'robo_e20'}.get(k) or who + '_' + GENERIC.get(mood, 'zz')
        if t not in have: miss.append(k)
        alias[k] = t
    if miss:
        raise SystemExit('캐릭터 팩에 없는 표정: ' + ', '.join(sorted(set(miss))))
    js = '\n'.join(l for l in js.split('\n') if not l.startswith('var SPRITE_ALIAS=')).rstrip() + '\n'
    js += 'var SPRITE_ALIAS=' + json.dumps(alias, ensure_ascii=False) + ';\n'
    open(p, 'w', encoding='utf-8').write(js)
    print('sprites alias', len(alias))


def main():
    ws = ''.join(open(os.path.join(ROOT, 'assets', 'src', f), encoding='utf-8').read() + '\n' for f in ['w1.js', 'w2.js', 'w3.js', 'w4.js', 'w5.js'])
    open(os.path.join(ROOT, 'assets', 'widgets.js'), 'w', encoding='utf-8').write(ws)
    pack = None
    if '--sprites' in sys.argv:
        pack = sys.argv[sys.argv.index('--sprites') + 1]
    chs = []
    for c in CHAPTERS:
        if os.path.exists(os.path.join(ROOT, 'content', c[0] + '.py')):
            chs.append(load(c[0]).CH)
    for c in chs:
        LEVEL[c['no']] = c.get('level', 2); MINUTES[c['no']] = c.get('min', 15)
        if c.get('basic'): BASIC.append(c['no'])
        for i, st in enumerate(c['stages'], 1):
            if st.get('deep'): DEEP.add((c['no'], i))
        NICK[c['no']] = c.get('nick', [])
    global ALL
    ALL = chs
    for i, ch in enumerate(chs):
        prevc = (chs[i - 1]['slug'] + '.html', '%02d %s' % (chs[i - 1]['no'], chs[i - 1]['title'])) if i else ('index.html', '오리엔테이션')
        nextc = (chs[i + 1]['slug'] + '.html', '%02d %s' % (chs[i + 1]['no'], chs[i + 1]['title'])) if i + 1 < len(chs) else ('practice/index.html', '마지막 장 · 실전 연습장')
        open(os.path.join(ROOT, ch['slug'] + '.html'), 'w', encoding='utf-8').write(chapter(ch, prevc, nextc))
        print('built', ch['slug'])
    import index_page, practice_page
    index_page.build(sys.modules[__name__], chs)
    practice_page.build(sys.modules[__name__], chs)
    import shutil
    shutil.copy(os.path.join(ROOT, 'assets', 'src', 'practice.js'), os.path.join(ROOT, 'assets', 'practice.js'))
    sprites_local()


if __name__ == '__main__':
    main()
