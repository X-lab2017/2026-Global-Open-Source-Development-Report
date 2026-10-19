"""A source-faithful declaration map, with shared content for HTML and SVG."""
import html
from pathlib import Path
import unicodedata

E = lambda value: html.escape(str(value), quote=True)
PRINCIPLES = [
    ('坚持开放互联', 'Open interconnection', '万物智联，普惠共生', 'Intelligent connections, inclusive coexistence'),
    ('坚持安全可信', 'Security & trust', '透明算法，信任基石', 'Transparent algorithms, foundations of trust'),
    ('坚持数据伦理', 'Data ethics', '算法向善，责任共担', 'Algorithms for good, shared responsibility'),
    ('坚持多元包容', 'Diversity & inclusion', '众智共创，价值共享', 'Collective creation, shared value'),
    ('坚持全球协作', 'Global collaboration', '跨界协同，智能互联', 'Collaboration across boundaries, connected intelligence'),
    ('坚持绿色智能', 'Green intelligence', '低碳驱动，创新致远', 'Low-carbon progress, lasting innovation'),
    ('坚持开源普惠', 'Inclusive open source', '智能为公，成果共享', 'Intelligence for the public, shared achievements'),
]
LAYERS = [
    ('筑牢智能时代基石', 'Foundations for the age of intelligence', [1, 2]),
    ('夯实伦理治理支柱', 'Pillars of ethical governance', [3, 4, 5]),
    ('共创社会价值未来', 'Co-creating a future of social value', [6, 7]),
]
STAGES = [
    ('时代呼唤', 'The call of our time', '迈向智能协作新纪元', 'Towards a new era of intelligent collaboration'),
    ('共同愿景', 'Our shared vision', '构建智能共治的数字文明', 'A digital civilization of shared intelligent governance'),
    ('核心原则', 'Core principles', '三层框架 · 七项原则', 'Three layers · Seven principles'),
    ('行动共识', 'A consensus for action', '迈向全球 AI 治理新格局', 'Towards a new landscape of global AI governance'),
]


def content(lang):
    t = lambda z, e: z if lang == 'zh' else e
    return {
        'title': t('全球开源与人工智能国际合作宣言', 'Declaration on International Cooperation in Open Source and Artificial Intelligence'),
        'subtitle': t('开源共创智能未来：迈向全球 AI 治理新纪元', 'Co-creating an intelligent future through open source'),
        'context': t('从“计算互联”走向“智能共生”', 'From connected computing to intelligent coexistence'),
        'vision': t('开放 · 包容 · 安全 · 可持续', 'Open · Inclusive · Secure · Sustainable'),
        'action': t('政府、企业、学界与公民社会携手，深化 AI 治理、算力共享、人才培育合作。', 'Governments, businesses, academia and civil society: cooperate on AI governance, shared compute and talent development.'),
        'closing': t('开源创新，属于全人类；智能未来，由我们共同创造。', 'Open source innovation belongs to all humanity; together, we create an intelligent future.'),
    }



def wrapped(value, width, size):
    """Conservative line wrapping keeps exported and interactive labels identical."""
    cjk = any(unicodedata.east_asian_width(c) in 'WF' for c in value)
    tokens, sep = (list(value), '') if cjk else (value.split(' '), ' ')
    measure = lambda s: sum(1 if unicodedata.east_asian_width(c) in 'WF' else .56 for c in s) * size
    lines, line = [], ''
    for token in tokens:
        candidate = line + (sep if line else '') + token
        if line and measure(candidate) > width:
            lines.append(line)
            line = token
        else:
            line = candidate
    return lines + [line]


def poster(lang, *, compact=False, interactive=False, theme='light'):
    """A single vector artboard: no reflow when switching to or from full screen."""
    t = lambda z, e: z if lang == 'zh' else e
    c = content(lang)
    dark = theme == 'dark'
    palette = dict(paper='#0a2c49' if dark else '#f3f8fa', card='#10324d' if dark else '#f8fbfc',
                   ink='#f6fbff' if dark else '#10334d', muted='#bad2de' if dark else '#4c697b',
                   border='#7193a8' if dark else '#698c9f')
    accents = ['#79c4ce', '#bc9bd7', '#b0cd77'] if dark else ['#007d87', '#77538f', '#4d7029']
    width, height = (480, 650) if compact else (1280, 768)
    prefix = 'df-' + lang + ('-compact' if compact else '-wide')
    cls = 'df-svg df-compact' if compact else 'df-svg df-wide'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" class="{cls}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="group" aria-labelledby="{prefix}-title {prefix}-desc"><title id="{prefix}-title">{E(c["title"])}</title><desc id="{prefix}-desc">{E(t("时代呼唤与共同愿景，引出三层七项原则，汇聚为行动共识。选择原则可阅读正文。", "Context and vision lead to three layers of principles and a consensus for action. Select a principle to read the text."))}</desc>']
    s.append(f'<rect class="df-paper" width="{width}" height="{height}" fill="{palette["paper"]}"/>')

    def rect(x, y, w, h, kind='card', radius=8):
        fill = palette['card'] if kind == 'card' else 'transparent'
        stroke = palette['border'] if kind == 'card' else 'none'
        line_width = 1.8 if kind == 'card' else 1
        s.append(f'<rect class="df-{kind}-shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{line_width}" vector-effect="non-scaling-stroke"/>')

    def txt(x, y, value, size=20, kind='ink', weight=400, limit=None, leading=1.28, anchor='start', accent=0):
        color = accents[accent-1] if accent else palette[kind]
        lines = wrapped(value, limit, size) if limit else [value]
        s.append(f'<text class="df-text df-{kind}" x="{x}" y="{y}" font-family="Inter,Noto Sans CJK SC,PingFang SC,Microsoft YaHei,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">')
        for i, line in enumerate(lines):
            s.append(f'<tspan x="{x}" dy="{size*leading if i else 0}">{E(line)}</tspan>')
        s.append('</text>')
        return len(lines)

    def node(key, href, label, class_name='', x=None, y=None, w=None, h=None):
        tag = 'a' if interactive else 'g'
        attributes = f' href="{href}" tabindex="0" aria-label="{E(label)}"' if interactive else ''
        s.append(f'<{tag} class="df-node {class_name}" data-df-node="{key}"{attributes}>')
        if x is not None:
            rect(x, y, w, h, 'hit')
        return tag

    def close(tag):
        s.append(f'</{tag}>')

    def edge(d, keys, layer=0, common=False, phase=0):
        color = accents[layer-1] if layer else accents[0]
        s.append(f'<g class="df-edge" data-keys="{keys}" data-layer="{layer}" data-common="{str(common).lower()}" style="--df-phase:{phase}s" color="{color}"><path class="df-edge-base" d="{d}" fill="none" stroke="{color}" stroke-width="1.5" stroke-opacity=".38" stroke-dasharray="5 7" stroke-linecap="round"/>')
        if interactive:
            s.append(f'<path class="df-edge-glow" d="{d}" pathLength="100"/><path class="df-edge-pulse" d="{d}" pathLength="100"/>')
        s.append('</g>')

    # Flow channels live exclusively in the whitespace between the three tiers.
    if compact:
        edge('M240 140V190', 'title context vision core', common=True)
        for i, center in enumerate([83, 240, 397], 1):
            if center < 240:
                top = 'M240 190H93Q83 190 83 200V212'
                bottom = 'M83 500V511Q83 522 94 522H240'
            elif center > 240:
                top = 'M240 190H387Q397 190 397 200V212'
                bottom = 'M397 500V511Q397 522 386 522H240'
            else:
                top, bottom = 'M240 190V212', 'M240 500V522'
            edge(top, f'core layer-{i}', i, phase=-i*.65)
            edge(bottom, f'layer-{i} action', i, phase=-i*.65-2.7)
        edge('M240 522V544', 'action', common=True, phase=-3)
    else:
        edge('M640 176V222', 'title context vision core', common=True)
        for i, center in enumerate([216, 640, 1064], 1):
            if center < 640:
                top = 'M640 222H228Q216 222 216 234V252'
                bottom = 'M216 568V576Q216 590 230 590H640'
            elif center > 640:
                top = 'M640 222H1052Q1064 222 1064 234V252'
                bottom = 'M1064 568V576Q1064 590 1050 590H640'
            else:
                top, bottom = 'M640 222V252', 'M640 568V590'
            edge(top, f'core layer-{i}', i, phase=-i*.65)
            edge(bottom, f'layer-{i} action', i, phase=-i*.65-2.7)
        edge('M640 590V626', 'action', common=True, phase=-3)

    # One shared foundation, with two concise native links to the original sections.
    rect(10 if compact else 20, 10 if compact else 12, 460 if compact else 1240, 130 if compact else 164)
    tag = node('title', '#declaration-text', c['title'], 'df-title-link',
               18 if compact else 38, 18 if compact else 20, 444 if compact else 1204, 48 if compact else 89)
    if compact:
        txt(240, 37, c['title'], 20 if lang == 'zh' else 17, weight=650, limit=430, anchor='middle')
        if lang == 'zh':
            txt(240, 62, '开源共创智能未来', 14, 'muted', anchor='middle')
    else:
        txt(640, 57 if lang == 'zh' else 45, c['title'], 32 if lang == 'zh' else 27, weight=650, limit=1175, anchor='middle')
        txt(640, 89 if lang == 'zh' else 103, c['subtitle'], 20 if lang == 'zh' else 17, 'muted', anchor='middle')
    close(tag)
    for i, key in enumerate(['context', 'vision']):
        center = ([127, 353] if compact else [330, 950])[i]
        node_width = 206 if compact else 550
        tag = node(key, f'#introduction-{i+1}', t(*STAGES[i][:2]) + ' · ' + t(*STAGES[i][2:]), '', center-node_width/2, 77 if compact else 112, node_width, 52 if compact else 55)
        txt(center, 96 if compact else 131, f'0{i+1} / ' + t(*STAGES[i][:2]), 13 if compact else 16, 'accent', 600, accent=1, anchor='middle')
        short = t(STAGES[i][2], ['Towards intelligent collaboration', 'Shared governance for a digital civilization'][i])
        if compact:
            short = t(['迈向智能协作', '构建智能共治'][i], ['Intelligent collaboration', 'Shared governance'][i])
        txt(center, 120 if compact else 158, short, (16 if lang == 'zh' else 13) if compact else 20, weight=500, limit=node_width, anchor='middle')
        close(tag)
    arrow = 'M224 109H256m-5-5 5 5-5 5' if compact else 'M618 147H662m-6-6 6 6-6 6'
    s.append(f'<path class="df-small-arrow" d="{arrow}" fill="none" stroke="{accents[0]}" stroke-width="1.5"/>')

    tag = node('core', '#introduction-3', t('核心原则：三层框架，七项原则', 'Core principles: three layers, seven principles'), '', 10 if compact else 20, 151 if compact else 181, 300 if compact else 470, 29)
    txt(10 if compact else 20, 173 if compact else 205, t('03 / 核心原则 · 三层框架，七项原则', '03 / CORE PRINCIPLES · Three layers, seven principles'), 13 if compact else 17, 'muted', 500)
    close(tag)

    for i, (zh, en, indices) in enumerate(LAYERS, 1):
        x, y, w, h = (10+(i-1)*157, 212, 146, 288) if compact else (20+(i-1)*424, 252, 392, 316)
        s.append(f'<g class="df-layer df-layer-{i}" data-df-group="{i}">')
        rect(x, y, w, h)
        s.append(f'<path class="df-layer-cap" d="M{x+8} {y}H{x+w-8}" stroke="{accents[i-1]}" stroke-width="3" stroke-linecap="round"/>')
        tag = node(f'layer-{i}', '#introduction-3', t(zh, en), 'df-layer-heading', x+5, y+8, w-10, 80 if compact else 91)
        txt(x+w/2, y+(26 if compact else 31), t('第'+'一二三'[i-1]+'层', f'LAYER 0{i}'), 12 if compact else 16, 'accent', 600, accent=i, anchor='middle')
        txt(x+w/2, y+(52 if compact else (68 if lang == 'zh' else 58)), t(zh, en), (18 if lang == 'zh' else 14) if compact else (26 if lang == 'zh' else 23), weight=650, limit=w-(24 if compact else 48), anchor='middle')
        close(tag)
        if not compact:
            s.append(f'<path class="df-divider" d="M{x+24} 348H{x+w-24}" stroke="{palette["border"]}" stroke-width="1.1" stroke-opacity=".65" vector-effect="non-scaling-stroke"/>')
        rows = ([346, 438] if len(indices) == 2 else [328, 390, 452]) if compact else ([394, 498] if len(indices) == 2 else ([374, 446, 518] if lang == 'zh' else [374, 445, 516]))
        for n, baseline in zip(indices, rows):
            p = PRINCIPLES[n-1]
            top = baseline - (25 if compact else 26)
            tag = node(f'principle-{n}', f'#declaration-principle-{n}', t(*p[:2]) + '：' + t(*p[2:]), 'df-principle', x+7, top, w-14, 56 if compact else 68)
            name = t(p[0][2:] if compact else p[0], p[1])
            txt(x+w/2, baseline, f'{n:02d}  {name}', (19 if lang == 'zh' else 12) if compact else (23 if lang == 'zh' else 20), weight=600, limit=w-(24 if compact else 48), anchor='middle')
            if not compact:
                txt(x+w/2, baseline+25, t(*p[2:]), 19 if lang == 'zh' else 15, 'muted', limit=w-48, leading=1.2, anchor='middle')
            close(tag)
        s.append('</g>')

    # All three principle layers converge into the same action, without a return loop.
    tag = node('action', '#introduction-4', t(*STAGES[3][:2]) + '：' + c['action'], 'df-action')
    rect(10 if compact else 20, 544 if compact else 626, 460 if compact else 1240, 70 if compact else 100)
    txt(240 if compact else 640, 567 if compact else 650, t('04 / 行动共识', '04 / A CONSENSUS FOR ACTION'), 13 if compact else 16, 'accent', 600, accent=1, anchor='middle')
    action_title = t(STAGES[3][2], 'Cooperation for global AI governance')
    txt(240 if compact else 640, 595 if compact else 683, action_title, (22 if lang == 'zh' else 17) if compact else (28 if lang == 'zh' else 25), weight=650, limit=430 if compact else 1175, anchor='middle')
    if not compact:
        txt(640, 712, t('政府 · 企业 · 学界 · 公民社会  ｜  AI 治理 · 算力共享 · 人才培育', 'Governments · Business · Academia · Civil society  |  AI governance · Shared compute · Talent'), 17 if lang == 'zh' else 15, 'muted', limit=1175, anchor='middle')
    close(tag)
    txt(240 if compact else 640, 639 if compact else 755, (t(c['closing'], 'Open source for humanity. An intelligent future, created together.') if compact else c['closing']), (13 if lang == 'zh' else 10) if compact else (18 if lang == 'zh' else 16), 'muted', 500, anchor='middle', limit=450 if compact else 1210)
    return ''.join(s) + '</svg>'


def render(lang):
    t = lambda z, e: z if lang == 'zh' else e
    svg = '/assets/report/frontmatter/fig-intro-1.svg' if lang=='zh' else '/assets/declaration/overview-' + lang + '.svg'
    return f'''<figure class="declaration-flow" id="declaration-overview" data-declaration-flow data-lang="{lang}" aria-labelledby="declaration-map-title">
<div class="df-toolbar"><h2 id="declaration-map-title">{t('宣言全景', 'Declaration overview')}<span> / {t('从共识到行动', 'From vision to action')}</span></h2><div class="df-tools"><button type="button" data-df-motion hidden aria-pressed="false">{t('暂停流线', 'Pause flow')}</button><button type="button" data-df-fullscreen hidden aria-pressed="false">{t('全屏', 'Full screen')}</button><a href="{svg}" download>{t('下载图', 'Download')} <span aria-hidden="true">↓</span></a></div></div>
<div class="df-canvas">{poster(lang, interactive=True)}{poster(lang, compact=True, interactive=True)}</div><img class="df-print" src="{svg}" alt="{E(t('宣言全景：时代呼唤、共同愿景、三层七项原则与行动共识', 'Declaration overview: context, vision, three layers of principles and action'))}" loading="lazy"><figcaption class="df-caption">{t("图 引-1 宣言的共同愿景、七项原则与行动方向", "Figure Intro-1 Shared vision, seven principles and action")}</figcaption></figure>'''


def static_svg(lang, theme='light'):
    return poster(lang, theme=theme)


def export(out):
    destination = Path(out) / 'assets/declaration'
    destination.mkdir(parents=True, exist_ok=True)
    for lang in ['zh', 'en']:
        (destination / f'overview-{lang}.svg').write_text(static_svg(lang))
