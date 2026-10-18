"""A concise bilingual executive summary with source-backed evidence and actions."""
import html
import json
from pathlib import Path
import overview_visuals

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/executive-summary.json').read_text())
ACTION = json.loads((ROOT / 'content/action/chapter6.json').read_text())
E = lambda value: html.escape(str(value), quote=True)


def text(value, lang):
    return E(value[lang])


def link(route, label, lang, cls=''):
    return '<a class="' + cls + '" href="/2026/' + lang + '/' + route + '">' + E(label) + ' <span aria-hidden="true">↗</span></a>'


def number(value, lang):
    return f'{value:.2f} 万' if lang == 'zh' else f'{value / 100:.2f}m'


def evidence(item, lang):
    t = lambda z, e: z if lang == 'zh' else e
    kind = item['id']
    out = '<figure class="es-evidence" aria-labelledby="es-chart-' + kind + '"><h4 id="es-chart-' + kind + '">' + text(item['visual_title'], lang) + '</h4>'
    if kind == 'participation':
        maximum = max(row['developers'] for row in item['rows'])
        out += '<div class="es-rank-bars">'
        for row in item['rows']:
            out += '<div class="es-rank-row"><div class="es-rank-label"><strong>' + text(row['name'], lang) + '</strong><small>' + text(row['country'], lang) + '</small></div><div class="es-rank-value"><b>' + number(row['developers'], lang) + '</b><span>' + t('开发者', 'developers') + '</span></div><div class="es-bar-track" aria-hidden="true"><i style="--bar-width:' + str(row['developers'] / maximum * 100) + '%"></i></div><span class="es-rank-badge"><small>OpenRank</small><b>#' + str(row['rank']) + '</b></span></div>'
        out += '</div>'
    elif kind == 'technology':
        out += '<div class="es-projects">'
        for project in item['projects']:
            out += '<div><strong>' + E(project['name']) + '</strong><span>OpenRank <b>#' + str(project['rank']) + '</b></span></div>'
        out += '</div><div class="es-tech-layers"><div>' + overview_visuals.icon('gosl', 'es-icon') + '<span><strong>Agent Infra</strong><small>' + t('智能体基础设施', 'Agent infrastructure') + '</small></span></div><div>' + overview_visuals.icon('gosm', 'es-icon') + '<span><strong>Model Infra</strong><small>' + t('模型基础设施', 'Model infrastructure') + '</small></span></div></div>'
    elif kind == 'models':
        out += '<div class="es-growth-legend"><span><i class="es-before"></i>2025-09-13</span><span><i></i>2026-09-13</span></div><div class="es-growth-bars">'
        for metric in item['metrics']:
            out += '<div class="es-growth-row"><div class="es-growth-label"><strong>' + text(metric['name'], lang) + '</strong><b>+' + E(metric['growth']) + '</b></div>'
            for key in ['before', 'after']:
                out += '<div class="es-growth-value es-' + key + '"><div class="es-bar-track" aria-hidden="true"><i style="--bar-width:' + str(metric[key] / metric['after'] * 100) + '%"></i></div><span>' + number(metric[key], lang) + '</span></div>'
            out += '</div>'
        out += '</div><p class="es-chart-note">' + t('两组分别以本期数量为满宽。', 'Each pair is scaled to its own current count.') + '</p>'
    else:
        out += '<ol class="es-evidence-questions">'
        for i, question in enumerate(item['questions'], 1):
            out += '<li><span aria-hidden="true">0' + str(i) + '</span><div><strong>' + text(question['title'], lang) + '</strong><p>' + text(question['body'], lang) + '</p></div></li>'
        out += '</ol>'
    return out + '<figcaption>' + text(item['scope'], lang) + '</figcaption></figure>'


def render(lang):
    t = lambda z, e: z if lang == 'zh' else e
    out = '<article class="executive-summary" lang="' + ('zh-CN' if lang == 'zh' else 'en') + '">'
    out += '<section class="es-opening" id="summary-1" aria-labelledby="es-thesis"><span class="es-kicker">01 / ' + t('年度主张', 'THE CENTRAL IDEA') + '</span><h2 id="es-thesis">' + text(DATA['headline'], lang) + '</h2><p class="es-lead">' + text(DATA['lead'], lang) + '</p>'
    out += '<div class="es-framework" aria-label="' + t('四大支柱', 'Four development pillars') + '">'
    for code, zh, en, icon, color in [('X1', '人才', 'People', 'together', 'teal'), ('X2', '供给', 'Supply', 'gosm', 'blue'), ('X3', '连接', 'Connections', 'goso', 'purple'), ('X4', '价值', 'Value', 'action', 'green')]:
        out += '<div class="es-color-' + color + '">' + overview_visuals.icon(icon, 'es-icon') + '<span><small>' + code + '</small><strong>' + t(zh, en) + '</strong></span></div>'
    out += '</div><div class="es-framework-caption"><p>' + text(DATA['framework'], lang) + '</p>' + link('chapters/01/#ch01-s02', t('理解目标与指标', 'Explore goals and indicators'), lang) + '</div></section>'
    out += '<section class="es-section" id="summary-2" aria-labelledby="es-observations"><span class="es-kicker">02 / ' + t('关键观察', 'KEY OBSERVATIONS') + '</span><h2 id="es-observations">' + t('四个观察，读懂发展质量', 'Four observations on development quality') + '</h2><p class="es-section-intro">' + t('从参与基础到开放条件，选择一个视角，查看证据与行动含义。', 'Choose a perspective to explore its evidence and implications for action.') + '</p><div class="es-switcher" data-es-switcher>'
    out += '<div class="es-tabs" data-es-tabs aria-label="' + t('选择观察视角', 'Choose an observation') + '">'
    for i, item in enumerate(DATA['findings'], 1):
        out += '<button type="button" id="es-tab-' + item['id'] + '" data-es-target="es-panel-' + item['id'] + '" class="es-color-' + item['color'] + '"><span>0' + str(i) + '</span><strong>' + text(item['tab'], lang) + '</strong></button>'
    out += '</div>'
    for item in DATA['findings']:
        out += '<div id="es-panel-' + item['id'] + '" class="es-observation es-color-' + item['color'] + '" data-es-panel><div class="es-observation-body"><div class="es-observation-copy"><span class="es-code">' + E(item['code']) + '</span><h3>' + text(item['title'], lang) + '</h3><p>' + text(item['body'], lang) + '</p></div>' + evidence(item, lang) + '</div><div class="es-implication"><div>' + overview_visuals.icon('action', 'es-icon') + '<p><strong>' + t('行动启示', 'Implication') + '</strong>' + text(item['implication'], lang) + '</p></div><nav aria-label="' + t('查看本观察的章节证据', 'Explore this observation in the report') + '">' + ''.join(link(x['route'], x['label'][lang], lang) for x in item['links']) + '</nav></div></div>'
    out += '</div></section>'
    out += '<section class="es-section" id="summary-3" aria-labelledby="es-action-title"><span class="es-kicker">03 / ' + t('共同行动', 'SHARED ACTION') + '</span><h2 id="es-action-title">' + t('三项任务，由不同主体共同推进', 'Three shared tasks, with distinct responsibilities') + '</h2><p class="es-section-intro">' + t('三项任务贯穿政府、企业与社区。选择你的角色，查看第六章的三条对应建议。', 'The same tasks connect public institutions, companies and communities. Select a role to see its three recommendations from Chapter 6.') + '</p><div class="es-switcher" data-es-switcher><div class="es-tabs es-actor-tabs" data-es-tabs aria-label="' + t('选择行动主体', 'Choose an actor') + '">'
    for actor in ACTION['actors']:
        out += '<button type="button" id="es-tab-' + actor['id'] + '" data-es-target="es-panel-' + actor['id'] + '"><strong>' + text(actor['title'], lang) + '</strong></button>'
    out += '</div>'
    for actor in ACTION['actors']:
        out += '<div class="es-action-panel" id="es-panel-' + actor['id'] + '" data-es-panel><div class="es-actor-heading"><h3 data-actor-label="' + text(actor['title'], lang) + '">' + text(actor['role'], lang) + '</h3>' + link('chapters/06/#ch06-s0' + actor['section'].split('.')[1], t('展开建议 ', 'Read recommendations ') + actor['section'], lang) + '</div><ol class="es-action-list">'
        for task in ACTION['tasks']:
            action = next(a for a in ACTION['actions'] if a['actor'] == actor['id'] and a['task'] == task['id'])
            out += '<li><div class="es-task-name"><span>' + task['n'] + '</span><strong>' + text(task['short'], lang) + '</strong></div><div class="es-task-action"><h4>' + text(action['title'], lang) + '</h4><p>' + text(DATA['action_briefs'][action['id']], lang) + '</p></div></li>'
        out += '</ol></div>'
    out += '</div></section>'
    out += '<section class="es-section es-reading" id="summary-4" aria-labelledby="es-reading-title"><span class="es-kicker">04 / ' + t('继续阅读', 'CONTINUE READING') + '</span><h2 id="es-reading-title">' + t('带着问题，进入正文', 'Take your questions into the report') + '</h2><nav class="es-reading-links" aria-label="' + t('从摘要继续阅读', 'Continue from the summary') + '">'
    for route, icon, title, desc in [('introduction/', 'sequence', t('下一篇 · 引言', 'Next · Introduction'), t('从共同愿景与七项原则，进入全书研究。', 'Begin with the shared vision and seven principles.')), ('', 'topic', t('按问题选择小节', 'Find a section by question'), t('从全书目录直接进入关心的主题。', 'Use the contents to go straight to your topic.'))]:
        out += '<a href="/2026/' + lang + '/' + route + '">' + overview_visuals.icon(icon, 'es-icon') + '<span><strong>' + title + '</strong><small>' + desc + '</small></span><i aria-hidden="true">↗</i></a>'
    out += '</nav><div class="es-scope"><strong>' + t('阅读范围', 'Reading scope') + '</strong><p>' + text(DATA['scope'], lang) + '</p></div><p class="es-closing">' + text(DATA['closing'], lang) + '</p></section></article>'
    return out


def manuscript(lang):
    """Readable print/reuse text, generated from the same bilingual content."""
    t = lambda z, e: z if lang == 'zh' else e
    lines = ['# ' + t('执行摘要', 'Executive summary'), DATA['headline'][lang], DATA['lead'][lang], '## ' + t('一个框架，连接目标与证据', 'One framework connects goals and evidence'), DATA['framework'][lang], '## ' + t('四个观察，读懂发展质量', 'Four observations on development quality')]
    for finding in DATA['findings']:
        lines += ['**' + finding['title'][lang] + '** ' + finding['body'][lang], t('行动启示：', 'Implication: ') + finding['implication'][lang], t('证据范围：', 'Scope: ') + finding['scope'][lang]]
    lines += ['## ' + t('三项共同任务，形成行动方向', 'Three shared tasks guide action')]
    for task in ACTION['tasks']:
        lines += ['**' + task['title'][lang] + t('。', '.') + '** ' + task['body'][lang]]
    for actor in ACTION['actors']:
        actions = [a for a in ACTION['actions'] if a['actor'] == actor['id']]
        lines += ['**' + actor['title'][lang] + '**', '\n'.join('- ' + a['title'][lang] + t('：', ': ') + DATA['action_briefs'][a['id']][lang] for a in actions)]
    lines += ['## ' + t('怎样使用这份报告', 'How to use this report'), t('第一章建立价值与方法基础，第二至第五章提供生态地图、影响力榜单、技术全景与模型生态观察，第六章连接共同任务与主体行动。可从第一章顺序阅读，也可从目录直接进入关心的小节。', 'Chapter 1 establishes values and methods. Chapters 2–5 provide ecosystem maps, influence rankings, technology landscapes and model observations. Chapter 6 connects shared tasks to action. Read in sequence or use the contents to find a section.'), DATA['scope'][lang], DATA['closing'][lang]]
    return '\n\n'.join(lines) + '\n'
