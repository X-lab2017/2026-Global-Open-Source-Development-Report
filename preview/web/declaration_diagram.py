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


def render(lang):
    t = lambda z, e: z if lang == 'zh' else e
    c = content(lang)
    svg = '/assets/declaration/overview-' + lang + '.svg'
    out = f'''<figure class="declaration-flow" id="declaration-overview" data-declaration-flow data-lang="{lang}" aria-labelledby="declaration-map-title">
<figcaption class="df-toolbar"><div><span>DECLARATION / OVERVIEW</span><h2 id="declaration-map-title">{t('一图读懂宣言', 'The declaration at a glance')}</h2></div><div class="df-tools"><button type="button" data-df-motion hidden aria-pressed="false">{t('暂停流线', 'Pause flow')}</button><button type="button" data-df-fullscreen hidden aria-pressed="false">{t('全屏', 'Full screen')}</button><a href="{svg}" download>{t('下载图', 'Download')} <span aria-hidden="true">↓</span></a></div></figcaption>
<div class="df-canvas"><svg class="df-wires" aria-hidden="true" focusable="false"></svg>
<a href="#declaration-text" class="df-title df-node" data-df-node="title"><strong>{E(c['title'])}</strong><span class="df-subtitle">{E(c['subtitle'])}</span></a>
<div class="df-premises">'''
    for i, key in enumerate(['context', 'vision']):
        stage = STAGES[i]
        out += f'''<a href="#introduction-{i+1}" class="df-stage df-node" data-df-node="{key}"><span class="df-stage-label"><b>0{i+1}</b> {t(*stage[:2])}</span><strong>{t(*stage[2:])}</strong><span class="df-stage-caption">{E(c[key])}</span></a>'''
    out += f'''</div><div class="df-core"><a href="#introduction-3" class="df-core-heading df-node" data-df-node="core"><span class="df-stage-label"><b>03</b> {t(*STAGES[2][:2])}</span><strong>{t(*STAGES[2][2:])}</strong></a><div class="df-layers">'''
    for i, (zh, en, indices) in enumerate(LAYERS, 1):
        out += f'''<section class="df-layer df-layer-{i}" data-df-group="{i}" aria-labelledby="df-layer-title-{i}"><h3 class="df-layer-heading df-node" id="df-layer-title-{i}" data-df-node="layer-{i}"><small>{t('第' + '一二三'[i-1] + '层', 'LAYER 0' + str(i))}</small><strong>{t(zh, en)}</strong></h3><div class="df-principles">'''
        for n in indices:
            p = PRINCIPLES[n-1]
            out += f'''<a href="#declaration-principle-{n}" class="df-principle df-node" data-df-node="principle-{n}"><span class="df-principle-number">0{n}</span><span class="df-principle-copy"><strong>{t(*p[:2])}</strong><span>{t(*p[2:])}</span></span><span class="df-link-arrow" aria-hidden="true">↗</span></a>'''
        out += '</div></section>'
    out += f'''</div></div><a href="#introduction-4" class="df-action df-node" data-df-node="action"><span class="df-stage-label"><b>04</b> {t(*STAGES[3][:2])}</span><strong>{t(*STAGES[3][2:])}</strong><span>{E(c['action'])}</span></a>
</div><div class="df-footer"><strong>{E(c['closing'])}</strong><span>{t('点击节点，阅读宣言正文', 'Select a node to read the declaration')} <i aria-hidden="true">↗</i></span></div><img class="df-print" src="{svg}" alt="{E(t('宣言全景：时代呼唤、共同愿景、三层七项原则与行动共识', 'Declaration overview: context, vision, three layers of principles and action'))}" loading="lazy"></figure>'''
    return out


def wrapped(value, width, size):
    """Conservative CJK/Latin line breaking for the standalone vector export."""
    tokens = list(value) if any(unicodedata.east_asian_width(c) in 'WF' for c in value) else value.split(' ')
    sep = '' if tokens == list(value) else ' '
    measure = lambda s: sum(1 if unicodedata.east_asian_width(c) in 'WF' else .58 for c in s) * size
    lines, line = [], ''
    for token in tokens:
        next_line = line + (sep if line else '') + token
        if line and measure(next_line) > width:
            lines.append(line)
            line = token
        else:
            line = next_line
    return lines + [line]


def static_svg(lang):
    """A light, editable, motion-free export for print and presentations."""
    t = lambda z, e: z if lang == 'zh' else e
    c = content(lang)
    ink, muted, navy = '#10334d', '#4c697b', '#123c55'
    accents = ['#007d87', '#77538f', '#486e2d']
    fills = ['#e9f5f4', '#f2edf6', '#f0f5e8']
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1050" viewBox="0 0 1440 1050" role="img" aria-labelledby="title desc"><title id="title">{E(c["title"])}</title><desc id="desc">{E(t("时代呼唤与共同愿景，引出三层七项原则，汇聚为行动共识。", "Context and vision lead to three layers of principles and a consensus for action."))}</desc><defs><marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L8 4L0 8" fill="#75959e"/></marker></defs><rect width="1440" height="1050" fill="#f3f8fa"/>']

    def rect(x, y, w, h, fill, stroke='none', r=12):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')

    def text(x, y, value, size=20, color=ink, weight=400, anchor='start', width=None):
        lines = wrapped(value, width, size) if width else [value]
        s.append(f'<text x="{x}" y="{y}" font-family="Noto Sans CJK SC,PingFang SC,Microsoft YaHei,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">')
        for i, line in enumerate(lines):
            s.append(f'<tspan x="{x}" dy="{size*1.4 if i else 0}">{E(line)}</tspan>')
        s.append('</text>')
        return len(lines) * size * 1.4

    def path(d, color='#75959e', arrow=True):
        s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"' + (' marker-end="url(#arrow)"' if arrow else '') + '/>')

    text(42, 36, 'GOSD 2026 / DECLARATION', 13, muted, 600)
    text(1398, 36, t('三层框架 · 七项原则', 'THREE LAYERS · SEVEN PRINCIPLES'), 13, muted, 500, 'end')
    rect(42, 56, 1356, 128, navy)
    title_size = 33 if lang == 'zh' else 28
    title_y = 110 if lang == 'zh' else 86
    th = text(720, title_y, c['title'], title_size, '#ffffff', 650, 'middle', 1200)
    text(720, title_y + th + 8, c['subtitle'], 18, '#c5e3e8', 400, 'middle')
    path('M376 184V214')
    rect(70, 214, 612, 126, '#ffffff', '#c8dce2')
    rect(758, 214, 612, 126, '#ffffff', '#c8dce2')
    for i, x in enumerate([94, 782]):
        text(x, 243, f'0{i+1} / {t(*STAGES[i][:2])}', 15, '#007d87', 650)
        text(x, 278 if lang == 'zh' else 272, t(*STAGES[i][2:]), 23 if lang == 'zh' else 18, ink, 600, width=555)
        text(x, 322, c[['context', 'vision'][i]], 16, muted, width=555)
    path('M682 277H758')
    path('M1064 340V358Q1064 368 1054 368H730Q720 368 720 378V392')
    rect(42, 392, 1356, 436, '#e9f1f4', '#d2e0e5')
    text(720, 425, '03 / ' + t(*STAGES[2][:2]), 17, '#007d87', 650, 'middle')
    text(720, 457, t(*STAGES[2][2:]), 24, ink, 650, 'middle')
    for i, (zh, en, indices) in enumerate(LAYERS):
        x = 66 + i * 444
        center = x + 210
        path(f'M720 470V480H{center}V494', accents[i], False)
        rect(x, 494, 420, 310, fills[i], '#d2e0e5')
        text(x+22, 522, t('第' + '一二三'[i] + '层', 'LAYER 0' + str(i+1)), 13, accents[i], 650)
        text(x+22, 552, t(zh, en), 23 if lang == 'zh' else 19, ink, 600, width=380)
        ys = [602, 715] if len(indices) == 2 else [592, 663, 734]
        for n, y in zip(indices, ys):
            p = PRINCIPLES[n-1]
            path(f'M{x+11} 575V{y+28}H{x+22}', accents[i], False)
            rect(x+22, y, 376, 66, '#ffffff', '#d2e0e5', 7)
            text(x+35, y+26, f'{n:02d}', 13, accents[i], 650)
            text(x+70, y+26, t(*p[:2]), 20 if lang == 'zh' else 18, ink, 650)
            text(x+70, y+(49 if lang == 'zh' else 43), t(*p[2:]), 16 if lang == 'zh' else 11.5, muted, width=308)
        path(f'M{center} 828V846H720V865', accents[i])
    rect(170, 865, 1100, 116, '#ffffff', '#b2cbd4')
    text(720, 894, '04 / ' + t(*STAGES[3][:2]), 15, '#007d87', 650, 'middle')
    text(720, 927, t(*STAGES[3][2:]), 25 if lang == 'zh' else 22, ink, 650, 'middle')
    text(720, 958, c['action'], 16 if lang == 'zh' else 14, muted, 400, 'middle', 1040)
    text(720, 1021, c['closing'], 20 if lang == 'zh' else 17, ink, 600, 'middle')
    return ''.join(s) + '</svg>'


def export(out):
    destination = Path(out) / 'assets/declaration'
    destination.mkdir(parents=True, exist_ok=True)
    for lang in ['zh', 'en']:
        (destination / f'overview-{lang}.svg').write_text(static_svg(lang))
