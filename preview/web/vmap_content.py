"""V-Map: global participation, transparent coverage and regional cooperation."""
from pathlib import Path
import html,json,shutil
import vmap_maps

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/vmap/fig-2-1-2_platform-coverage.json').read_text())
E=lambda s:html.escape(str(s),quote=True)
ASSET='/assets/vmap/'
from vmap_publication import (TITLE, INTRO, QUESTION, POSITION, FINDING, SNAPSHOT_NOTE, STORIES, FIGURE_AFTER, ACTION_TITLE, ACTION_INTRO, BRIDGE,
 STRATEGIES, INDICATOR_FEEDBACK, GAPS, FIGURES, PDF_NAME, EDITION, SERIES_COLORS, SERIES_DASH)
import vmap_publication as publication

def prose(paragraphs,insight=False):
    def render(text):
        if insight and '。' in text:
            head,tail=text.split('。',1);return '<strong>'+E(head+'。')+'</strong>'+E(tail)
        return E(text)
    return ''.join('<p>'+render(p)+'</p>' for p in paragraphs)

def rows(kind):
    if kind=='countries':return sorted((r for r in DATA['countries'] if r['active'] is not None),key=lambda r:-r['active'])[:10]
    return DATA['five_group_records']

def plot(key):
    limit=4000 if key=='total' else 800
    title='开发者总量' if key=='total' else '活跃开发者'
    body=[]
    for r in rows('regions'):
        v=r[key]
        body.append(f'<div class="vmap-bar-row"><span class="vmap-label">{r["name"]}</span><div class="vmap-track">'+(f'<i class="vmap-github" style="width:{v/limit*100:.5f}%"></i>' if v is not None else '<span class="vmap-missing">待同步</span>')+f'</div><b class="vmap-value">{vmap_maps.number(v)}</b></div>' if v is not None else f'<div class="vmap-bar-row"><span class="vmap-label">{r["name"]}</span><div class="vmap-track"><span class="vmap-missing">待同步</span></div><b class="vmap-value">—</b></div>')
    return f'<div class="vmap-plot" data-vmap-plot="{key}"><h5>{title}<small>万人 · 五域统计</small></h5><div class="vmap-bar-list">'+''.join(body)+f'</div><div class="vmap-axis"><span>0</span><span>{limit:,} 万人</span></div></div>'

def frame(key,number,subtitle,body,height=800):
    spec=FIGURES[key]; title=spec['title']
    figure=f'<figure class="chapter-one-visual vmap-figure" id="fig-vmap-{key}" data-lang="zh" data-slide-key="vmap-{key}" data-slide-height="{height}" data-reflow-minimum-width="700" style="--vmap-height:{height}px"><header class="viz-heading"><span class="eyebrow">{number} / V-MAP</span><h4>{title}</h4><p>{subtitle}</p></header>'+body+f'<figcaption><strong>{number} {title}</strong><span>{spec["note"]}</span></figcaption></figure>'
    views=''.join(f'<div class="vmap-print-panel vmap-print-{orientation}"><img src="/assets/vmap/print/{name}" alt="{number} {title}，出版分面 {i+1}"></div>' for i,(name,orientation) in enumerate(zip(spec['files'],spec['orientation'])))
    return figure+'<div class="vmap-publication-views" aria-label="'+number+' 静态出版视图">'+views+'</div>'

def image_figure(kind):
    world=kind=='global'
    subtitle='参与基础与当期活跃，是两个互补的观察尺度。' if world else '地理分布、全国趋势与区域结构，共同呈现参与基础。'
    number='图 2-1-1' if world else '图 2-1-3'
    return frame(kind,number,subtitle,vmap_maps.body('world' if world else 'china',DATA),860)

def comparison():
    controls='''<div class="vmap-controls" hidden><div role="group" aria-label="比较对象"><button type="button" data-vmap-view="regions" aria-pressed="true">五域比较</button><button type="button" data-vmap-view="countries" aria-pressed="false">国家比较</button><button type="button" data-vmap-view="trend" aria-pressed="false">五年演变</button></div><div role="group" aria-label="平台覆盖范围"><button type="button" data-vmap-scope="github" aria-pressed="true">仅 GitHub</button><button type="button" data-vmap-scope="extended" aria-pressed="false">补充中国国内平台</button></div></div>'''
    body=controls+'<div class="vmap-status" role="status" aria-live="polite">2026报告年度 · 五域规模</div><div class="vmap-comparison" data-vmap-chart>'+plot('total')+plot('active')+'</div><div class="vmap-trend" data-vmap-trend hidden></div><div class="vmap-legend"><span data-vmap-base-legend><i></i>编制组五域统计</span><span data-vmap-domestic-legend hidden><i class="vmap-domestic"></i>国内补充约120万</span></div><p class="vmap-scope-note" data-vmap-note>五域按原稿统计展示；国内补充量在国家比较中呈现。</p>'
    return frame('comparison','图 2-1-2','从规模、变化与覆盖范围，理解五域的相对位置。',body)

def section(lang):
    out=[f'<section class="chapter-section goso-section vmap-section" id="ch02-s01"><div class="section-topline">2.1 / V-MAP</div><h2>{TITLE}</h2><p class="vmap-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p>',
    '<div class="vmap-position"><strong>目标与指标定位</strong><p>'+E(POSITION)+'</p></div>',
    '<h3 class="vmap-part-title" id="vmap-findings">核心发现</h3><p>'+E(FINDING)+'</p><p class="vmap-window-note">'+E(SNAPSHOT_NOTE)+'</p>',
    f'<nav class="vmap-reading-route" aria-label="本节阅读路径"><a href="#vmap-global">全球参与</a><span>→</span><a href="#vmap-regions">五域比较</a><span>→</span><a href="#vmap-china">中国实例</a><span>→</span><a href="#vmap-actions">行动建议</a><a class="vmap-download" href="/assets/vmap/print/{PDF_NAME}" download>下载本节 PDF ↓</a></nav>']
    for i,(title,paras) in enumerate(STORIES):
        kind=['global','regions','china'][i];split=FIGURE_AFTER[i]
        out.append(f'<div class="goso-prose vmap-story" id="vmap-{kind}"><h3>{E(title)}</h3>'+prose(paras[:split])+'</div>')
        out.append(comparison() if i==1 else image_figure(kind))
        out.append(f'<div class="goso-prose vmap-interpretation" data-figure-reading="{kind}">'+prose(paras[split:],insight=True)+'</div>')
    out.append('<div class="vmap-strategies" id="vmap-actions"><h3>'+E(ACTION_TITLE)+'</h3><p class="vmap-action-intro">'+E(ACTION_INTRO)+'</p>')
    for i,(title,paras) in enumerate(STRATEGIES):out.append(f'<article class="vmap-action"><span class="vmap-action-number">0{i+1}</span><div><h4>{E(title)}</h4>'+prose(paras)+'</div></article>')
    out.append('</div><details class="goso-gap" id="vmap-evidence"><summary>统计范围与指标说明</summary><p>'+E(INDICATOR_FEEDBACK)+'</p><ol>'+''.join('<li>'+E(gap)+'</li>' for gap in GAPS)+'</ol><a href="/assets/vmap/fig-2-1-2_platform-coverage.json">数据与统计范围</a> · <a href="/assets/vmap/fig-2-1-2_five-year-source.csv">历史原表</a> · <a href="/assets/vmap/source/data-meta.json">报告年度元数据</a> · <a href="/assets/vmap/print/publication-spec.json">图件出版说明</a></details>')
    out.append('<div class="vmap-print-evidence"><h4>统计范围与指标说明</h4>'+prose([INDICATOR_FEEDBACK,*GAPS])+'</div>')
    out.append('<p class="goso-bridge">'+E(BRIDGE)+'</p><script type="application/json" id="vmap-data">'+json.dumps(dict(DATA,publication_style=dict(colors=SERIES_COLORS,dashes=SERIES_DASH)),ensure_ascii=False).replace('<','\\u003c')+'</script></section>')
    return ''.join(out)

def manuscript():
    return publication.manuscript().rstrip()

def export(out):
    target=out/'assets/vmap';shutil.copytree(ROOT/'content/vmap',target,dirs_exist_ok=True)
    text=manuscript()+'\n'
    (ROOT/'content/vmap/chapter-2-1.md').write_text(text)
    (target/'chapter-2-1.md').write_text(text)
