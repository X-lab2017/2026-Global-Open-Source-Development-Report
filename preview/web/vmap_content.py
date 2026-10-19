"""V-Map: global participation, transparent coverage and regional cooperation."""
from pathlib import Path
import html,json,shutil
import vmap_maps

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/vmap/fig-2-1-2_platform-coverage.json').read_text())
E=lambda s:html.escape(str(s),quote=True)
ASSET='/assets/vmap/'
from vmap_publication import (TITLE, QUESTION, POSITION, FINDING, SNAPSHOT_NOTE, STORIES,
 STRATEGIES, INDICATOR_FEEDBACK, GAPS, FIGURES, PDF_NAME, EDITION, SERIES_COLORS, SERIES_DASH)
import vmap_publication as publication

def prose(paragraphs):return ''.join('<p>'+E(p)+'</p>' for p in paragraphs)

def rows(kind):
    if kind=='countries':return sorted((r for r in DATA['countries'] if r['active'] is not None),key=lambda r:-r['active'])[:10]
    by={r['id']:r for r in DATA['countries']}
    return [by['US'],dict(id='EU',name='欧洲',total=None,active=None),by['CN'],by['IN'],DATA['groups']['SOUTH6']]

def plot(key):
    limit=4000 if key=='total' else 500
    title='开发者总量' if key=='total' else '活跃开发者'
    body=[]
    for r in rows('regions'):
        v=r[key]
        body.append(f'<div class="vmap-bar-row"><span class="vmap-label">{r["name"]}</span><div class="vmap-track">'+(f'<i class="vmap-github" style="width:{v/limit*100:.5f}%"></i>' if v is not None else '<span class="vmap-missing">待同步</span>')+f'</div><b class="vmap-value">{vmap_maps.number(v)}</b></div>' if v is not None else f'<div class="vmap-bar-row"><span class="vmap-label">{r["name"]}</span><div class="vmap-track"><span class="vmap-missing">待同步</span></div><b class="vmap-value">—</b></div>')
    return f'<div class="vmap-plot" data-vmap-plot="{key}"><h5>{title}<small>万人 · GitHub</small></h5><div class="vmap-bar-list">'+''.join(body)+f'</div><div class="vmap-axis"><span>0</span><span>{limit:,} 万人</span></div></div>'

def frame(key,number,title,subtitle,body,caption,height=800):
    spec=FIGURES[key]; title=spec['title']
    figure=f'<figure class="chapter-one-visual vmap-figure" id="fig-vmap-{key}" data-lang="zh" data-slide-key="vmap-{key}" data-slide-height="{height}" data-reflow-minimum-width="700" style="--vmap-height:{height}px"><header class="viz-heading"><span class="eyebrow">{number} / V-MAP</span><h4>{title}</h4><p>{subtitle}</p></header>'+body+f'<figcaption><strong>{number} {title}</strong><span>{spec["note"]}</span></figcaption></figure>'
    views=''.join(f'<div class="vmap-print-panel vmap-print-{orientation}"><img src="/assets/vmap/print/{name}" alt="{number} {title}，出版分面 {i+1}"></div>' for i,(name,orientation) in enumerate(zip(spec['files'],spec['orientation'])))
    return figure+'<div class="vmap-publication-views" aria-label="'+number+' 静态出版视图">'+views+'</div>'

def image_figure(kind):
    world=kind=='global'
    title='全球开发者总量与活跃全景' if world else '中国下钻全景 · 区域参与与节点'
    subtitle='同看规模与活跃 · 悬停读数、点击联动，选择中国下钻' if world else '全国 → 省级地区 → 参与画像 · 让区域结构可查、可比较'
    number='图 2-1-1' if world else '图 2-1-3'
    filename='global-openshare.png' if world else 'china-openshare-20261015.png'
    caption=f'<a href="{DATA["source"]}" target="_blank" rel="noopener">来源平台 ↗</a> · <a href="{ASSET+filename}" target="_blank" rel="noopener">核对原图 ↗</a> · <a href="{ASSET}fig-2-1-2_platform-coverage.json" download>交互图数据 ↓</a> · <a href="/assets/vmap/map-provenance.json">同源底图说明</a> · 2025自然年；增量对照2024年。'
    return frame(kind,number,title,subtitle,vmap_maps.body('world' if world else 'china',DATA),caption,860)

def comparison():
    controls='''<div class="vmap-controls" hidden><div role="group" aria-label="比较对象"><button type="button" data-vmap-view="regions" aria-pressed="true">五域比较</button><button type="button" data-vmap-view="countries" aria-pressed="false">国家排名</button><button type="button" data-vmap-view="trend" aria-pressed="false">五年历史（待对齐）</button></div><div role="group" aria-label="平台覆盖范围"><button type="button" data-vmap-scope="github" aria-pressed="true">仅 GitHub</button><button type="button" data-vmap-scope="extended" aria-pressed="false">补充中国国内平台</button></div></div>'''
    body=controls+'<div class="vmap-status" role="status" aria-live="polite">2025自然年 · GitHub 中国活跃234.46万 · 国家榜第3</div><div class="vmap-comparison" data-vmap-chart>'+plot('total')+plot('active')+'</div><div class="vmap-trend" data-vmap-trend hidden></div><div class="vmap-legend"><span><i></i>GitHub</span><span data-vmap-domestic-legend hidden><i class="vmap-domestic"></i>国内约120万 · 净增情景</span></div><p class="vmap-scope-note" data-vmap-note>六国同版活跃合计300.79万；欧洲分组待对齐。仓库2022—2026历史序列单列，尚不用于本期增长结论。</p>'
    caption=f'<a href="{ASSET}fig-2-1-2_platform-coverage.csv" download>当前快照 CSV ↓</a> · <a href="{ASSET}fig-2-1-2_platform-coverage.json" download>口径与来源 JSON ↓</a> · <a href="{ASSET}fig-2-1-2_five-year-source.csv" download>五年原表 CSV ↓</a> · 版本与口径分列。'
    return frame('comparison','图 2-1-2','五域规模、活跃参与与五年演变','五域规模 / 国家排名 / 五年历史 · 当前自然年与历史原表分别标识',body,caption)

def section(lang):
    base='/2026/'+lang+'/'
    out=[f'<section class="chapter-section goso-section vmap-section" id="ch02-s01"><div class="section-topline">2.1 / V-MAP</div><h2>{TITLE}</h2><p class="goso-question">{QUESTION}</p>',
    f'<div class="vmap-publication-download"><a href="/assets/vmap/print/{PDF_NAME}" download>下载 2.1 PDF 样章 ↓</a><span>同源正文 · 三幅图组 · 2026.10.20</span></div>',
    '<div class="vmap-position"><strong>目标与指标定位</strong><p>'+E(POSITION)+'</p></div>',
    '<h3 class="vmap-part-title" id="vmap-findings">核心发现</h3><p>'+E(FINDING)+'</p><p class="vmap-window-note">'+E(SNAPSHOT_NOTE)+'</p>',
    '<nav class="vmap-reading-route" aria-label="本节阅读路径"><a href="#vmap-global">全球参与</a><span>→</span><a href="#vmap-regions">五域比较</a><span>→</span><a href="#vmap-china">中国实例</a><span>→</span><a href="#vmap-actions">行动建议</a></nav>']
    for i,(title,paras) in enumerate(STORIES):
        kind=['global','regions','china'][i]
        out.append(f'<div class="goso-prose vmap-story" id="vmap-{kind}"><h3>{E(title)}</h3>'+prose(paras)+'</div>')
        out.append(comparison() if i==1 else image_figure(kind))
    out.append('<div class="vmap-strategies" id="vmap-actions"><h3>2.1.4 行动建议</h3>')
    for i,(title,paras) in enumerate(STRATEGIES):out.append(f'<article class="vmap-action"><span class="vmap-action-number">0{i+1}</span><div><h4>{E(title)}</h4>'+prose(paras)+'</div></article>')
    out.append('</div><details class="goso-gap" id="vmap-evidence"><summary>指标与证据说明</summary><p>'+E(INDICATOR_FEEDBACK)+'</p><ol>'+''.join('<li>'+E(gap)+'</li>' for gap in GAPS)+'</ol><p>地图与当前规模使用 2025 自然年同版底表；万人读数沿用原平台截断方式。模拟、条件情景、平台估计与口径待核验分别标注。本节未新增模拟统计值。</p><a href="/assets/vmap/fig-2-1-2_platform-coverage.json">数据与统计范围</a> · <a href="/assets/vmap/fig-2-1-2_five-year-source.csv">历史原表</a> · <a href="/assets/vmap/source/calendar-meta.json">自然年元数据</a> · <a href="/assets/vmap/print/publication-spec.json">图件出版说明</a></details>')
    out.append('<p class="goso-bridge">V-Map 识别参与的广度、地域和观察边界；下一节 C-Map 进一步检验，这些参与形成了怎样的贡献。</p><script type="application/json" id="vmap-data">'+json.dumps(dict(DATA,publication_style=dict(colors=SERIES_COLORS,dashes=SERIES_DASH)),ensure_ascii=False).replace('<','\\u003c')+'</script></section>')
    return ''.join(out)

def manuscript():
    return publication.manuscript().rstrip()

def export(out):
    target=out/'assets/vmap';shutil.copytree(ROOT/'content/vmap',target,dirs_exist_ok=True)
    text=manuscript()+'\n'
    (ROOT/'content/vmap/chapter-2-1.md').write_text(text)
    (target/'chapter-2-1.md').write_text(text)
