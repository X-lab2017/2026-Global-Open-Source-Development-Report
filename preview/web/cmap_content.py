"""C-Map web presentation, sharing the full research manuscript with PDF."""
from pathlib import Path
import json,html,math,shutil
import vmap_maps
from cmap_publication import *
import cmap_publication as publication
BASE=ROOT/'content/cmap';GEO=vmap_maps.GEO
E=lambda s:html.escape(str(s),quote=True)
def num(v):return vmap_maps.number(v/10000) if v is not None else '—'
def prose(ps,insight=False):
    out=[]
    for text in ps:
        if insight and '。' in text:
            a,b=text.split('。',1);out.append('<p><strong>'+E(a+'。')+'</strong>'+E(b)+'</p>')
        else:out.append('<p>'+E(text)+'</p>')
    return ''.join(out)
def frame(key,n,title,sub,body,caption):
    spec=FIGURES[key];title=spec['title']
    figure=f'<figure id="fig-cmap-{key}" class="chapter-one-visual cmap-figure" data-slide-key="cmap-{key}" data-slide-height="860" data-reflow-minimum-width="700" data-lang="zh" aria-labelledby="fig-cmap-{key}-title"><header class="viz-heading"><span class="eyebrow">图 2-2-{n} / C-MAP</span><h4 id="fig-cmap-{key}-title">{title}</h4><p>{sub}</p></header>{body}<figcaption><span class="cm-caption-note">{spec["note"]}</span></figcaption></figure>'
    views=''.join(f'<div class="cm-print-panel cm-print-{o}"><img src="/assets/cmap/print/{name}" alt="图 2-2-{n} {title}，出版分面 {i+1}"></div>' for i,(name,o) in enumerate(zip(spec['files'],spec['orientation'])))
    return figure+'<div class="cm-publication-views">'+views+'</div>'
def btn(key,value,text,pressed=False,hint=''):
    description=f' title="{E(hint)}" aria-description="{E(hint)}"' if hint else ''
    return f'<button type="button" data-{key}="{value}" aria-pressed="{str(pressed).lower()}"{description}>{text}</button>'
def svg_map(scope):
    rows=DATA['countries' if scope=='world' else 'provinces'];by={r['id']:r for r in rows};maximum=max(r['value'] for r in rows)
    out=[f'<svg viewBox="0 0 880 470" preserveAspectRatio="xMidYMid meet" data-cm-svg="{scope}" role="group" aria-label="'+('全球贡献地图，全球地域分布' if scope=='world' else '中国贡献地图，含台湾省、港澳及南海附图')+'">']
    for f in GEO[scope]:
        if f.get('kind')=='line':out.append(f'<path d="{f["d"]}" fill="none" stroke="var(--muted)" stroke-width=".7"/>');continue
        r=by.get(f['id']);fill=f'var(--gv-m{min(5,int(r["value"]/maximum*5.999))})' if r else 'var(--gv-empty)'
        attrs=f' data-cm-region="{f["id"]}" data-center="{f["center"][0]},{f["center"][1]}" role="button" tabindex="0" aria-label="{E(f["name"])}，贡献度 {num(r["value"])} 万 OpenRank"' if r else ''
        out.append(f'<path d="{f["d"]}" fill="{fill}" stroke="var(--line)" stroke-width=".65" fill-rule="evenodd"{attrs}><title>{E(f["name"])}</title></path>')
    for code in (['US','CN','DE','IN','BR','ID'] if scope=='world' else ['110000','310000','440000','330000','710000','510000']):
        f=next(x for x in GEO[scope] if x['id']==code);x,y=f['center'];name=f['name'].replace('省','').replace('市','')
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" class="cm-map-label">{name}</text>')
    return ''.join(out)+'</svg>'
def spark(series):
    vals=series['values'];lo=0;span=series.get('axis_max') or max(vals) or 1
    path=' '.join(f'{"M" if i==0 else "L"}{8+i*73},{51-(v-lo)/span*36:.2f}' for i,v in enumerate(vals))
    return f'<svg viewBox="0 0 310 77" role="img" aria-label="2021至2025自然年贡献趋势"><path d="{path}" fill="none" stroke="var(--cyan)" stroke-width="2.5"/>'+''.join(f'<text x="{8+i*73}" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">{year}</text>' for i,year in enumerate(series['labels']))+'</svg>'
def cards(scope):
    if scope=='world':
        return ''.join('<article><small>'+title+'</small><strong>'+num(DATA['trends'][key]['values'][-1])+'<em> 万</em></strong>'+spark(DATA['trends'][key])+'</article>' for key,title in [('GLOBAL','全球贡献 · 五年趋势'),('US','美国贡献 · 五年趋势'),('CN','中国贡献 · 五年趋势')])
    rows=DATA['provinces'];total=DATA['trends']['CN']['values'][-1];top=sum(r['value'] for r in rows[:3]);other=sum(r['value'] for r in rows[3:10]);rest=sum(r['value'] for r in rows[10:])
    return '<article><small>中国贡献 · 五年趋势</small><strong>'+num(total)+'<em> 万</em></strong>'+spark(DATA['trends']['CN'])+'</article><article><small>贡献结构 · 34 个省级地区</small><div class="cm-stack">'+''.join(f'<i style="width:{v/total*100}%;background:var(--gv-s{i})"></i>' for i,v in enumerate([top,other,rest]))+'</div><div class="cm-shares">'+''.join(f'<span>{label}<b>{v/total*100:.1f}%</b></span>' for label,v in [('京沪粤',top),('第4—10位',other),('其余24地',rest)])+'</div></article><article data-cm-profile><small>所选地区 · 北京市</small><strong>25.50<em> 万 OpenRank</em></strong><p>活跃规模与同比随所选地区更新。</p></article>'
def map_figure(scope):
    world=scope=='world';rr=DATA['countries' if world else 'provinces']
    controls='<div class="cm-toolbar"><div class="cm-tabs" role="group" aria-label="着色指标">'+btn('cm-metric','value','贡献规模',True)+btn('cm-metric','growth','同比变化')+(btn('cm-metric','average','平均贡献 · 样本') if not world else '')+'</div>'
    controls+=('<div class="cm-tabs">'+btn('cm-scope','world','全球',True)+btn('cm-scope','china','中国下钻 ↘')+'</div>' if world else '<span class="cm-compact-note" data-cm-coverage>34 个省级地区</span>')+'</div>'
    layers=''.join(f'<div data-cm-layer="{s}"'+(' hidden' if s!=scope else '')+'>'+svg_map(s)+'</div>' for s in (['world','china'] if world else ['china']))
    rank=''.join(f'<button type="button" data-cm-row="{r["id"]}"><span>{r["rank"]:02}</span><strong>{r["name"]}</strong><b>{num(r["value"])}</b></button>' for r in rr[:8])
    body=f'<div class="cm-map-module" data-cm-map="{scope}">{controls}<div class="cm-meta"><span data-cm-period>2025 自然年 · 万 OpenRank</span><span data-cm-context>{"全球贡献" if world else "中国34个省级地区"} · 万 OpenRank</span></div><div class="cm-map-layout"><div class="cm-map-stage"><div class="cm-map-viewport">{layers}<div class="cm-map-zoom"><button type="button" data-cm-zoom="in" aria-label="放大">＋</button><button type="button" data-cm-zoom="out" aria-label="缩小">−</button><button type="button" data-cm-zoom="reset">复位</button></div></div><div class="cm-map-readout" data-cm-readout role="status">悬停读数 · 点击锁定'+(' · 点击中国下钻' if world else '')+f'</div></div><aside class="cm-rank"><h5>地区排名 <small data-cm-rank-unit>万 OpenRank</small></h5><input type="search" data-cm-search aria-label="搜索地区" placeholder="搜索地区或代码"><div data-cm-rank>{rank}</div><div class="cm-pager"><button type="button" data-cm-page="prev" aria-label="上一页">←</button><span data-cm-page-status>1 / {math.ceil(len(rr)/8)}</span><button type="button" data-cm-page="next" aria-label="下一页">→</button></div></aside></div><div class="cm-legend"><i></i><span data-cm-scale>线性色阶：0—{num(max(r["value"] for r in rr))} 万 OpenRank</span><span data-cm-extra>未列地区不按零处理</span></div><div class="cm-cards" data-cm-cards>{cards(scope)}</div></div>'
    caption=''
    return frame('global' if world else 'china',1 if world else 3,'全球开发者 OpenRank 贡献全景' if world else '中国开源贡献全景 · 区域结构与发展观察','地图与排名联动，底部查看趋势与区域结构。',body,caption)
def comparison():
    body='<div data-cm-comparison><div class="cm-toolbar"><div class="cm-tabs" aria-label="趋势尺度">'+btn('cm-index','absolute','贡献规模',True)+btn('cm-index','index','累计增长（2022＝100）',hint='各区域当年贡献度除以其2022年贡献度，再乘100。指数200表示比起点增长100%，不是同比；右侧排名仍显示所选年的贡献规模。')+'</div><span class="cm-comparison-status" data-cm-comparison-status>2026 报告年度</span></div><div class="cm-comparison-body cm-comparison-integrated" data-cm-comparison-body></div><div class="cm-gap-chart" data-cm-gap></div></div>'
    return frame('comparison',2,'','上看五域趋势与排名，下看中美差距变化。',body,'')
def globe():
    body='<div class="cm-globe" data-cm-globe data-mode="mechanism"><div class="cm-toolbar"><div class="cm-tabs" aria-label="观察视角">'+btn('globe-mode','mechanism','协作机制 · 示意',True)+btn('globe-mode','projects','全部项目')+'</div><div class="cm-globe-tools"><button type="button" data-globe-motion aria-pressed="true">暂停流动</button><button type="button" data-globe-rotate aria-pressed="false">自动旋转</button><button type="button" data-globe-reset>复位</button></div></div>'
    body+='<div class="cm-globe-layout"><div class="cm-earth" data-globe-stage tabindex="0" role="group" aria-label="三维协作地球，方向键旋转，加减键缩放"><img src="/assets/cmap/globe-mechanism-1.svg" alt="协作机制示意，虚构节点与关系" class="cm-globe-fallback"><div class="cm-globe-badge" data-globe-badge>协作机制 · 示意</div><div class="cm-globe-subbar" data-globe-project-controls hidden><div class="cm-tabs" aria-label="视觉增强">'+btn('globe-enhance','1','标准线宽')+btn('globe-enhance','3','增强 ×3',True)+'</div></div><div class="cm-globe-legend" data-globe-legend></div><div class="cm-globe-hint" data-globe-hint>拖动旋转 · 点击节点聚焦关系</div><div class="cm-globe-tooltip" data-globe-tooltip hidden></div></div><aside class="cm-globe-panel">'
    body+='<div data-globe-mechanism-panel><div class="cm-globe-steps">'+''.join(btn('globe-step',str(i),label,i==1) for i,label in enumerate(['活动','关系','持续投入']))+'</div><h5 data-globe-title>开发者与项目相互成就</h5><div data-globe-explanation></div><div class="cm-globe-principle" data-globe-principle></div><button type="button" class="cm-clear-focus" data-globe-clear hidden>显示完整网络</button></div>'
    body+='<div data-globe-project-panel hidden><div class="cm-project-heading"><h5>中美项目贡献来源</h5>'+btn('globe-target','all','两国同看',True)+'</div><div data-globe-shares></div><div class="cm-globe-mini" aria-label="来源关系筛选">'+btn('globe-filter','all','全部来源',True)+btn('globe-filter','cross','跨境')+btn('globe-filter','local','本土')+'</div><div class="cm-flow-list" data-globe-list></div><div class="cm-pager"><button type="button" data-globe-page="prev" aria-label="上一页">←</button><span data-globe-page-status></span><button type="button" data-globe-page="next" aria-label="下一页">→</button></div><div class="cm-flow-detail" data-globe-detail></div></div></aside></div><div class="cm-globe-bottom" data-globe-bottom></div></div>'
    return frame('globe',4,'','理解协作机制，比较中美项目的贡献来源。',body,'')

def section(lang):
    out=[f'<section id="ch02-s02" class="chapter-section goso-section cmap-section"><div class="section-topline">2.2 / C-MAP</div><h2>{TITLE}</h2><p class="cm-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="cm-position"><strong>目标与指标定位</strong><p>{POSITION}</p></div><h3 id="cmap-findings">核心发现</h3><p>{FINDING}</p><p class="cm-window-note">{WINDOW}</p><nav class="cm-reading-route" aria-label="C-Map 阅读路径">']
    keys=list(FIGURES)
    for key,label in [('global','全球贡献'),('comparison','五域比较'),('china','中国区域'),('globe','协作连接'),('actions','行动建议')]:out.append(f'<a href="#cmap-{key}">{label}</a>')
    out.append(f'<a class="cm-download" href="/assets/cmap/print/{PDF_NAME}" download>下载本节 PDF ↓</a></nav>')
    for i,(title,ps) in enumerate(STORIES):
        key=keys[i];split=FIGURE_AFTER[i]
        out.append(f'<div class="goso-prose cm-story" id="cmap-{key}"><h3>{title}</h3>'+prose(ps[:split])+'</div>')
        out.append([lambda:map_figure('world'),comparison,lambda:map_figure('china'),globe][i]())
        out.append(f'<div class="goso-prose cm-interpretation" data-cmap-reading="{key}">'+prose(ps[split:],True)+'</div>')
    out.append('<div class="cm-actions" id="cmap-actions"><h3>'+ACTION_TITLE+'</h3><p>'+ACTION_INTRO+'</p>')
    for i,(title,ps) in enumerate(STRATEGIES):out.append(f'<article><span>0{i+1}</span><div><h4>{title}</h4>'+prose(ps)+'</div></article>')
    out.append('</div><details class="goso-gap" id="cmap-evidence"><summary>统计范围与指标说明</summary>'+prose(NOTES)+'<p class="cm-evidence-links"><a href="/assets/cmap/data.json" download>本节数据</a> · <a href="/assets/cmap/flows.csv" download>20条来源记录</a> · <a href="/assets/cmap/flow-method.md">增强显示说明</a></p></details>')
    out.append('<div class="cm-print-evidence"><h4>统计范围与指标说明</h4>'+prose(NOTES)+'</div><p class="goso-bridge">'+BRIDGE+'</p><script type="application/json" id="cmap-data">'+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></section>')
    return ''.join(out)
def manuscript():return publication.manuscript()
def export(out):
    (BASE/'chapter-2-2.md').write_text(manuscript());shutil.copytree(BASE,out/'assets/cmap',dirs_exist_ok=True)
    from goso_brand import values
    css=[]
    for theme in ['light','dark']:
        selector='.cmap-figure' if theme=='light' else '[data-theme="dark"] .cmap-figure'
        css.append(selector+'{'+''.join('--gv-'+k+':'+v+';' for k,v in values(theme).items())+'}')
    (out/'cmap.css').write_text('\n'.join(css)+'\n'+(ROOT/'web/cmap.css').read_text())
    for name in ['cmap.js','cmap-globe.js','cmap-globe-math.mjs','cmap-globe-analysis.mjs']:shutil.copy2(ROOT/'web'/name,out/name)
