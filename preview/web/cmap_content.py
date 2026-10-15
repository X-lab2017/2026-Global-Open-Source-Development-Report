"""C-Map manuscript and four single-screen figures, with inspectable source data."""
from pathlib import Path
import json,html,math,shutil
import vmap_maps

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'content/cmap'
DATA=json.loads((BASE/'data.json').read_text());GEO=vmap_maps.GEO
E=lambda s:html.escape(str(s),quote=True)
def num(v):return vmap_maps.number(v/10000) if v is not None else '—'
TITLE='全球开源贡献地图（C-Map）'
QUESTION='如何看见并支持全球协作网络中的贡献，让开放投入成为长期发展的能力？'
POSITION='本节对应 OSDGs 的 X2“技术产出与开放供给”、2.1“代码产出”，以 OSDI 的 OpenRankContrib 为主指标方向，辅以 X1 的 DevScale 观察参与与贡献的差异，呼应 SDG 9 与 SDG 17。份额、增量和平均贡献是诊断性分析。当前地图保留源平台“开发者 OpenRank 贡献度”的名称；具体算法类型、年度聚合与跨平台规则核验后，再完成正式 OSDI 映射。'
FINDING='全球贡献版图正在变化，协作价值需要被更充分地识别。按本报告采用的五域统计口径，2026 年中国开发者 OpenRank 贡献度达到 442.92 万，高于美国的 423.97 万；2022—2026 年累计增长 231.6%，成为近五年贡献格局变化的主要增量来源之一。全球南方与新兴地区应作为共同建设者进入长期合作；持续、可信的贡献观察，则有助于将这种投入连接到地区发展与公共价值。'
WINDOW='本节主叙事与五年比较采用报告 2022—2026 五域表口径。二维地图保留 OpenShare 对应的 GitHub 2025 自然年参照；地球可切换两种点位口径，并叠加 2026 项目样本来源。实线为表列关系，金色虚线为可选情景估算，二者不混为实测。'
STORIES=[
 ('全球：让贡献在协作关系中被看见',[
  '活动次数回答“做了多少”，协作网络进一步追问“与谁共同建设、形成了怎样的关系、这种投入能否延续”。OpenRank 将网络关系引入评价，并通过历史继承体现时间上的连续性。全域算法观察开发者与仓库之间的关系，社区算法进一步观察项目内 Issue、PR 等协作。两类方法有不同的对象和参数，不能仅凭数值名称混用。',
  '图 2-2-1 复现附件的贡献分布：2025 自然年全球开发者 OpenRank 贡献度约 1,894.35 万，美国约 423.68 万，中国约 121.03 万。德国在活跃规模中排第五，在贡献度中排第二；印度与巴西的贡献度分别约 89.86 万和 62.39 万。不同排序说明参与版图与贡献版图具有不同结构，也说明全球南方已经具有值得识别的现实贡献。',
  '计数指标仍适合观察活动规模、处理速度和工作负荷；网络指标补充协作结构与长期积累的视角。在 AI 降低内容与代码生成成本的背景下，更需要将活动计数、关系证据和实际采用结合起来，避免把大量生成活动直接等同于有效贡献。任何一个网络分数也不能独自证明代码质量、社会效益或算法免受操纵。']),
 ('五域：中国成为近五年全球开源贡献格局变化的主要增量来源',[
  '按与附件一致的 GitHub 自然年底表，巴西、印度尼西亚、越南、菲律宾、埃及和南非六国的贡献度合计约 105.70 万，较上一自然年增加约 2.81 万；印度另列。这些是全球南方的观察样本，并非其全体。已有贡献应成为平等合作、共同维护和议题设置的依据，不能只把这些地区理解为人才供给地或技术接受方。',
  '按本报告采用的五域统计口径，2026 年欧洲开发者 OpenRank 贡献度达到 650.16 万，中国达到 442.92 万，高于美国的 423.97 万，约高 4.5%。2022—2026 年，中国贡献度累计增长 231.6%，明显高于欧洲的 37.6% 和美国的 24.5%；最近一年同比增长约 47.2%。中国成为近五年全球贡献格局变化的主要增量来源之一。图 2-2-2 默认展示这条五年变化主线，并保留平台参照入口以便查证。',
  '开发者贡献与项目影响力还需要分开观察。同为 2025 自然年的 OpenShare 项目影响力底表中，美国约 188.16 万，中国约 55.08 万，美国约为中国的 3.4 倍。这一独立参照说明，中国开发者贡献总量的提升，并不意味着项目影响位置已经同步改变。贡献如何连接到长期维护、项目采用和全球影响，是下一节 I-Map 继续回答的问题。']),
 ('中国：从地区贡献观察走向公共发展能力',[
  '中国下钻显示，2025 自然年北京、上海、广东的贡献度分别约 25.50 万、23.15 万和 15.41 万，合计约占全国 52.9%；浙江和台湾省分别约 14.10 万和 14.01 万。头部地区之外，四川、江苏、湖北等节点也具有可观测贡献。图 2-2-3 将全国趋势、区域结构和地区详情补齐，使地图能够支持多角度的持续观察。',
  '贡献规模和平均贡献回答不同问题。平均值同时受参与结构、观测覆盖和分母大小影响；在完整 34 地区数据中，小基数地区也可能出现较高值。本图将平均贡献保留为探索性视图，同时显示活跃人数与小基数提示。原稿前十样本继续留作对照，不据此将地区贴上“效率高低”或“人才优劣”的标签。',
  '更有价值的方向，是建立具有公信度的地区开源贡献观察：公开方法与数据边界，让地区看见自身变化、可学习的协作实践和需要支持的环节。将贡献投入与教育、科研、产业创新、数字公共品和 SDG 相关实践联系起来，以具名项目、持续维护和公共受益证据补充指标。中国的探索可作为区域案例，供其他国家结合本地条件检验和借鉴。'])
]
STRATEGIES=[
 ('认可并推动全球可持续协作网络',[
  '国际组织、基金会、公共资助方和企业，可共同将持续协作网络视为数字时代的重要公共能力。监测从孤立的提交量和活动数扩展到开发者、项目及维护者之间的关系，关注贡献能否得到回应、合作能否跨越组织和地域、共同建设能否长期延续。',
  '采用可解释、可复核、能够跨期追踪的关系指标，并结合代码评审、维护和实际采用证据，支持使整个网络受益的投入。这样的度量应帮助资源流向有价值的协作，减少围绕单一计数的短期激励。']),
 ('让全球南方与新兴地区的贡献获得相称认可',[
  '在国际议题、项目治理和资源支持中充分识别全球南方与新兴地区已经形成的贡献。推动本地社区作为共同设计者、维护者和决策参与者进入长期合作，支持多语种协作、导师网络和双向知识流动。',
  '中国的快速增长说明，新兴地区能够成为全球开放投入的重要增量来源。应把这种贡献作为组织长期合作、支持共同维护和参与治理的重要依据。与此同时，把开发者贡献、项目影响力和公共价值分层观察，为包括中国在内的合作伙伴提供更准确的发展路径，而不是用单一名次替代对生态的理解。']),
 ('建立可信的地区贡献观察，连接社会经济发展',[
  '可在中国探索公开、持续、可复核的地区开源贡献监测与比较机制：以年度贡献画像、变化趋势和同类地区对标为主要形式，保留排序作为查阅工具，同时提供覆盖说明、异议反馈和证据修订入口。让比较服务于识别投入、学习经验和组织合作。',
  '将开源贡献观察逐步接入地方数字能力建设、产业创新、教育科研和可持续发展评估。贡献指标可以作为辅助证据，不直接等同于官方 SDG 指标或行政绩效，不必以排名奖惩作为运行前提。以长期项目、共同维护和公共服务采用验证实际成效，推动 AI 时代的开放投入更稳定地进入社会经济发展过程。'])
]
GAPS=[
 '按作者确认，主叙事采用报告五域口径：中国 442.92 万、美国 423.97 万。后续在方法附录补充算法版本、平台构成、年度聚合与地域归属细则；不将其与自然年地图拼接。',
 '补齐欧洲成员清单和五域同口径五年序列；核对平均贡献分子与活跃分母的对象范围。原始记录、未知和小基数均保留。',
 '补充全球南方共同维护、地区贡献监测与公共受益案例；补全项目来源表的分母、未知归属和完整关系，再以实测替换地球中的估算层。'
]
FLOW_INSIGHT='贡献总量与项目汇聚能力并不等同。来源表中，中国开发者向美国项目样本贡献 24,420.69 OpenRank，反向为 1,980.46，前者约为后者的 12.3 倍；两组项目的本土贡献份额分别为 79.22% 和 38.28%。这些不同侧面的观察提示，支持贡献投入，还需要支持项目连接外部参与者、共同维护与长期采用的能力。来源表只覆盖中美项目样本，不能据此判断一个国家在全球网络中的净输出或净输入；完整地域关系仍需补充。'
def prose(ps):return ''.join('<p>'+E(p)+'</p>' for p in ps)
def frame(key,n,title,sub,body,caption):
    return f'<figure id="fig-cmap-{key}" class="chapter-one-visual cmap-figure" data-slide-key="cmap-{key}" data-slide-height="860" data-lang="zh"><header class="viz-heading"><span class="eyebrow">图 2-2-{n} / C-MAP</span><h4>{title}</h4><p>{sub}</p></header>{body}<figcaption>{caption}</figcaption></figure>'
def btn(key,value,text,pressed=False):return f'<button type="button" data-{key}="{value}" aria-pressed="{str(pressed).lower()}">{text}</button>'
def svg_map(scope):
    rows=DATA['countries' if scope=='world' else 'provinces'];by={r['id']:r for r in rows};maximum=max(r['value'] for r in rows)
    out=[f'<svg viewBox="0 0 880 470" preserveAspectRatio="xMidYMid meet" data-cm-svg="{scope}" role="group" aria-label="'+('全球贡献地图，中国含台湾省' if scope=='world' else '中国贡献地图，含台湾省、港澳及南海附图')+'">']
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
    vals=series['values'];lo=min(vals);span=max(vals)-lo or 1
    path=' '.join(f'{"M" if i==0 else "L"}{8+i*73},{51-(v-lo)/span*36:.2f}' for i,v in enumerate(vals))
    return f'<svg viewBox="0 0 310 77" role="img" aria-label="2021至2025贡献趋势"><path d="{path}" fill="none" stroke="var(--cyan)" stroke-width="2.5"/>'+''.join(f'<text x="{8+i*73}" y="73" font-size="11" text-anchor="middle" fill="var(--muted)">{year}</text>' for i,year in enumerate(series['labels']))+'</svg>'
def cards(scope):
    if scope=='world':
        return ''.join('<article><small>'+title+'</small><strong>'+num(DATA['trends'][key]['values'][-1])+'<em> 万</em></strong>'+spark(DATA['trends'][key])+'</article>' for key,title in [('GLOBAL','全球贡献 · 五年趋势'),('US','美国贡献 · 五年趋势'),('CN','中国贡献 · 五年趋势')])
    rows=DATA['provinces'];total=DATA['trends']['CN']['values'][-1];top=sum(r['value'] for r in rows[:3]);other=sum(r['value'] for r in rows[3:10]);rest=sum(r['value'] for r in rows[10:])
    return '<article><small>中国贡献 · 五年趋势</small><strong>'+num(total)+'<em> 万</em></strong>'+spark(DATA['trends']['CN'])+'</article><article><small>贡献结构 · 34 个省级地区</small><div class="cm-stack">'+''.join(f'<i style="width:{v/total*100}%;background:var(--gv-s{i})"></i>' for i,v in enumerate([top,other,rest]))+'</div><div class="cm-shares">'+''.join(f'<span>{label}<b>{v/total*100:.1f}%</b></span>' for label,v in [('京沪粤',top),('第4—10位',other),('其余24地',rest)])+'</div><p>规模结构用于观察；不代表绩效评级。</p></article><article data-cm-profile><small>所选地区 · 北京市</small><strong>25.50<em> 万 OpenRank</em></strong><p>点击地图或列表，查看贡献、人数与变化。</p></article>'
def map_figure(scope):
    world=scope=='world';rr=DATA['countries' if world else 'provinces']
    controls='<div class="cm-toolbar"><div class="cm-tabs" role="group" aria-label="着色指标">'+btn('cm-metric','value','贡献规模',True)+btn('cm-metric','growth','同比变化')+(btn('cm-metric','average','平均贡献 · 探索') if not world else '')+'</div>'
    controls+=('<div class="cm-tabs">'+btn('cm-scope','world','全球',True)+btn('cm-scope','china','中国下钻 ↘')+'</div>' if world else '<a href="#fig-cmap-global">↑ 返回全球贡献地图</a>')+'</div>'
    layers=''.join(f'<div data-cm-layer="{s}"'+(' hidden' if s!=scope else '')+'>'+svg_map(s)+'</div>' for s in (['world','china'] if world else ['china']))
    rank=''.join(f'<button type="button" data-cm-row="{r["id"]}"><span>{r["rank"]:02}</span><strong>{r["name"]}</strong><b>{num(r["value"])}</b></button>' for r in rr[:8])
    body=f'<div class="cm-map-module" data-cm-map="{scope}">{controls}<div class="cm-meta"><span>OpenDigger / OpenShare · GitHub · 2025 自然年</span><span data-cm-context>{"全球贡献" if world else "中国34个省级地区"} · 万 OpenRank</span></div><div class="cm-map-layout"><div class="cm-map-stage">{layers}<div class="cm-map-zoom"><button type="button" data-cm-zoom="in" aria-label="放大">＋</button><button type="button" data-cm-zoom="out" aria-label="缩小">−</button><button type="button" data-cm-zoom="reset">复位</button></div><div class="cm-map-readout" data-cm-readout role="status">悬停读数 · 点击锁定'+(' · 点击中国下钻' if world else '')+f'</div></div><aside class="cm-rank"><h5>地区贡献观察 <small data-cm-rank-unit>万 OpenRank</small></h5><input type="search" data-cm-search aria-label="搜索地区" placeholder="搜索地区或代码"><div data-cm-rank>{rank}</div><div class="cm-pager"><button type="button" data-cm-page="prev" aria-label="上一页">←</button><span data-cm-page-status>1 / {math.ceil(len(rr)/8)}</span><button type="button" data-cm-page="next" aria-label="下一页">→</button></div></aside></div><div class="cm-legend"><i></i><span data-cm-scale>线性色阶：0—{num(max(r["value"] for r in rr))} 万 OpenRank</span><span data-cm-extra>缺失不等于零 · 点击列表也可选中地区</span></div><div class="cm-cards" data-cm-cards>{cards(scope)}</div></div>'
    caption=f'<a href="/assets/cmap/{"world" if world else "china"}-reference.png" target="_blank">附件原图 ↗</a> · <a href="/assets/cmap/{"countries" if world else "provinces"}.csv" download>完整数据 CSV ↓</a> · <a href="/assets/cmap/provenance.json">来源与口径</a> · <a href="/assets/vmap/map-provenance.json">同源底图</a>'
    return frame('global' if world else 'china',1 if world else 3,'全球开发者 OpenRank 贡献全景' if world else '中国开源贡献全景 · 区域结构与发展观察','观察贡献规模与变化 · 地图、地区列表与详情联动',body,caption)
def comparison():
    series=DATA['legacy']['series'];keys=list(series);maximum=max(max(v) for v in series.values())/10000*1.12
    svg='<svg viewBox="0 0 820 420" role="img" aria-label="报告2022至2026五域趋势">'
    for i in range(5):
        y=345-i*75;svg+=f'<path d="M60 {y}H790" stroke="var(--line)"/><text x="49" y="{y+5}" text-anchor="end">{maximum*i/4:.0f}</text>'
    for i,k in enumerate(keys):
        points=[(60+j*182.5,345-v/10000/maximum*300) for j,v in enumerate(series[k])]
        path=' '.join(('L' if j else 'M')+f'{x},{y}' for j,(x,y) in enumerate(points))
        svg+=f'<path d="{path}" fill="none" stroke="var(--gv-s{i})" stroke-width="{4 if k=="China" else 2}" opacity="{1 if k=="China" else .4}"/>'
    svg+=''.join(f'<text x="{60+i*182.5}" y="383" text-anchor="middle">{y}</text>' for i,y in enumerate(DATA['legacy']['years']))+'</svg>'
    fallback='<div class="cm-line-chart">'+svg+'</div><aside class="cm-series"><h5>2026 表列值</h5>'+''.join(f'<button type="button" data-cm-series="{k}" aria-pressed="{str(k=="China").lower()}"><i style="background:var(--gv-s{i})"></i><span>{DATA["legacy"]["labels"][k]}</span><b>{num(series[k][-1])}</b></button>' for i,k in enumerate(keys))+'<p>中国高于美国约4.5%；五年累计增长231.6%。</p><p>欧洲同期增长37.6%，美国增长24.5%。</p></aside>'
    body='<div data-cm-comparison><div class="cm-toolbar"><div class="cm-tabs" aria-label="比较视图">'+btn('cm-view','legacy','报告五年趋势',True)+btn('cm-view','current','GitHub 参照')+btn('cm-view','scope','数据口径说明')+'</div><div class="cm-tabs" data-cm-trend-controls>'+btn('cm-index','absolute','绝对值',True)+btn('cm-index','index','2022＝100')+'</div></div><p class="cm-comparison-status" data-cm-comparison-status>报告 2022—2026 五域口径 · 中国 442.92 万，高于美国 423.97 万</p><div class="cm-comparison-body" data-cm-comparison-body>'+fallback+'</div><p class="cm-comparison-note" data-cm-comparison-note>采用报告五域统计口径；五组非全球穷尽分区。GitHub 自然年参照与报告年度分开展示。</p></div>'
    return frame('comparison',2,'五域贡献变化 · 中国成为重要增量来源','2022—2026 · 贡献规模与增长率联动 · 点击地区突出对应趋势',body,'<a href="/assets/cmap/source/repository-contribution-trend.csv" download>原稿五域 CSV ↓</a> · <a href="/assets/cmap/data.json" download>本节数据与口径 ↓</a> · <a href="'+__import__('goso_content').source('contribution')+'">GitHub 原表 ↗</a>')
def globe():
    options=''.join(f'<option value="{r["id"]}"'+(' selected' if r['id']=='CN' else '')+'>'+E(r['name'])+'</option>' for r in DATA['countries'])
    body='<div class="cm-globe" data-cm-globe><div class="cm-toolbar"><div class="cm-tabs" aria-label="地球内容">'+btn('globe-mode','network','协作机制 · 示意',True)+btn('globe-mode','data','贡献分布 · 实测')+'</div><div class="cm-globe-tools"><button type="button" data-globe-motion aria-pressed="true">暂停流动</button><button type="button" data-globe-rotate aria-pressed="false">自动旋转</button><button type="button" data-globe-reset>复位</button></div></div><div class="cm-globe-layout"><div class="cm-earth" data-globe-stage tabindex="0" role="group" aria-label="交互式三维地球，拖动旋转，方向键调整视角，加减键缩放"><img src="/assets/cmap/globe-fallback.svg" alt="球面地图静态参照" class="cm-globe-fallback"><div class="cm-globe-badge" data-globe-badge>机制示意 · 非真实跨国流量</div><div class="cm-globe-lenses" data-globe-lenses hidden role="group" aria-label="贡献网络观察视角">'+btn('globe-lens','all','全景',True)+btn('globe-lens','out','看输出')+btn('globe-lens','in','看汇入')+btn('globe-lens','south','南方 · 估算')+'</div><div class="cm-globe-legend" data-globe-legend>青色开发者 · 金色共享项目 · 点击节点聚焦关系</div><div class="cm-globe-hint" data-globe-hint>加载 3D 视图…</div><div class="cm-globe-tooltip" data-globe-tooltip hidden></div></div><aside class="cm-globe-panel"><div data-globe-network-panel><span class="eyebrow">WHY NETWORKS MATTER</span><h5 data-globe-title>开发者与项目相互成就</h5><div class="cm-globe-steps" aria-label="探索网络原理">'+btn('globe-step','0','01 看活动')+btn('globe-step','1','02 看关系',True)+btn('globe-step','2','03 看长期')+'</div><div data-globe-explanation></div><div class="cm-globe-principle" data-globe-principle></div><small data-globe-network-note>114 个虚构节点、384 条关系；未计算 OpenRank 分数，地理位置仅作视觉布置。</small><button type="button" class="cm-clear-focus" data-globe-clear hidden>显示完整网络</button></div><div data-globe-data-panel hidden><span class="eyebrow">CONTRIBUTION &amp; CONNECTIONS</span><h5>贡献在哪里，又流向哪里？</h5><div class="cm-globe-mini" aria-label="贡献点统计口径">'+btn('globe-scope','report','报告 2026',True)+btn('globe-scope','github','GitHub 2025')+'</div><label>观察国家／地区<select data-globe-country>'+options+'</select></label><div data-globe-country-detail></div><div class="cm-globe-mini" aria-label="贡献来源图层">'+btn('globe-flow','sample','样本流向',True)+btn('globe-flow','scenario','＋估算')+btn('globe-flow','none','仅看点')+'</div><label>项目归属<select data-globe-target><option value="all">全部：中美项目</option><option value="CN">聚焦中国项目</option><option value="US">聚焦美国项目</option></select></label><p class="cm-flow-status" data-globe-flow-detail></p><a class="cm-flow-method" href="/assets/cmap/flow-method.md" target="_blank">估算方法与数据 ↓</a> · <a class="cm-flow-method" href="#ch02-s05">贡献来源分析 →</a></div></aside></div><div class="cm-globe-bottom" data-globe-bottom><span>活动：贡献的起点</span><span>关系：开发者 ↔ 共享项目</span><span>时间：历史继承与适当衰减</span></div></div>'
    return frame('globe',4,'从独立活动到持续协作','3D 交互式地球 · 节点、关系与时间 · 贡献分布叠加来源流向',body,'<a href="https://open-digger.cn/docs/user-docs/metrics/openrank" target="_blank" rel="noopener">OpenRank 方法 ↗</a> · <a href="/assets/cmap/flows.csv" download>来源与估算 CSV ↓</a> · <a href="/assets/cmap/source/repository-project-sources.csv" download>原始来源表 ↓</a> · <a href="/assets/cmap/THIRD-PARTY-NOTICES.md">3D 来源与许可</a>')
def section(lang):
    base='/2026/'+lang+'/'
    out=[f'<section id="ch02-s02" class="chapter-section goso-section cmap-section"><div class="section-topline">2.2 / C-MAP</div><h2>{TITLE}</h2><p class="goso-question">{QUESTION}</p><div class="cm-position"><strong>目标与指标定位</strong><p>{POSITION}</p><a href="{base}data/indicators/#indicator-OpenRankContrib">查阅 OSDI 指标定义 →</a></div><h3>核心发现</h3><p>{FINDING}</p><p class="cm-window-note">{WINDOW}</p><nav class="cm-reading-route" aria-label="C-Map 阅读路径">']
    for key,label in [('global','全球贡献'),('comparison','五域与变化'),('china','中国区域'),('globe','协作地球'),('actions','行动建议')]:out.append(f'<a href="#cmap-{key}">{label}</a>')
    out.append('</nav>')
    for i,(title,ps) in enumerate(STORIES):
        key=['global','comparison','china'][i];out.append(f'<div class="goso-prose cm-story" id="cmap-{key}"><h3>{title}</h3></div>');out.append([lambda:map_figure('world'),comparison,lambda:map_figure('china')][i]());out.append('<div class="goso-prose">'+prose(ps)+'</div>')
    out.append('<div class="goso-prose cm-story" id="cmap-globe"><h3>理解贡献：从独立活动到持续协作</h3><p>这幅地球把独立活动、相互成就和长期积累放在同一视野中。114 个虚构节点与 384 条协作关系演示网络原理；切换到贡献分布，可查阅报告口径或 GitHub 参照，并沿中美项目样本的真实来源关系探索贡献流向。金色虚线补充未列来源的情景估算，支持理解网络的可能结构，不作为实测或未来预测。</p></div>'+globe()+'<div class="goso-prose"><h4>从贡献规模，继续看连接的方向与结构</h4><p>'+FLOW_INSIGHT+'</p></div>')
    out.append('<div class="cm-actions" id="cmap-actions"><span class="eyebrow">FROM NETWORKS TO PUBLIC VALUE</span><h3>策略建议：把协作贡献连接到可持续发展</h3>')
    for i,(title,ps) in enumerate(STRATEGIES):out.append(f'<article><span>0{i+1}</span><div><h4>{title}</h4>'+prose(ps)+'</div></article>')
    out.append('</div><details class="goso-gap" id="cmap-evidence"><summary>OSDI 指标反馈与三项待补证据</summary><p>优先完善 OpenRankContrib 的数据映射，并与 DevScale 对齐对象和窗口；平均贡献作为探索性诊断。OpenRankInflu 留给 2.3，GlobalCollabShare 留给 2.5。网络原理不等同已观测的合作关系；关系监测与地区评估的实际成效仍需要案例证据。</p><ol>'+''.join('<li>'+E(x)+'</li>' for x in GAPS)+'</ol><p>全球贡献趋势汇总与地域明细相差 420,087.61，原因待核，不自动记为未知地区。中国省级合计与全国值差 0.01，保留源数舍入差。平均贡献的数据对象范围待核；图中“小基数”仅提示本节分母少于 1,000 的记录，不排除这些地区，也不构成质量评价。</p><a href="/assets/cmap/data.json">完整数据与口径 ↓</a> · <a href="/assets/cmap/source/repository-province-average.csv">原稿省级样本 ↓</a> · <a href="'+__import__('goso_content').source('province')+'">GitHub 原表 ↗</a> · <a href="/assets/cmap/source/calendar-influence-reference.json">项目影响力对照 ↓</a> · <a href="/assets/cmap/openrank-reference.png">作者方法示意附件 ↗</a></details><p class="goso-bridge">贡献来自哪些地区，与项目影响力积累在哪里，是两个不同问题。<a href="#ch02-s03">下一节 I-Map 沿项目维度继续观察 →</a></p><script type="application/json" id="cmap-data">'+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></section>')
    return ''.join(out)
def manuscript():
    out=['## 2.2 '+TITLE,'**研究问题：** '+QUESTION,'### 核心发现',POSITION,FINDING,WINDOW]
    for i,(title,ps) in enumerate(STORIES):out+=['### '+title,'**图 2-2-'+str(i+1)+'：** '+['全球贡献全景','五域贡献变化 · 中国成为重要增量来源','中国贡献全景'][i],*ps]
    out+=['### 图 2-2-4：从活动计数到全球协作网络','交互地球：114 个虚构节点与 384 条关系演示双向强化和长期积累；贡献分布叠加 20 条原表来源关系，可选残差来源估算层。实线与金色虚线区分表列样本和情景。报告口径的国家点仅有中、美、印，其他国家留空；GitHub 2025 参照保留完整分布。',FLOW_INSIGHT,'### 策略建议']
    for title,ps in STRATEGIES:out+=['#### '+title,*ps]
    out+=['### 待补证据',*GAPS,'数据、时期和来源：content/cmap/provenance.json；OpenRank 方法：https://open-digger.cn/docs/user-docs/metrics/openrank']
    return '\n\n'.join(out)+'\n'
def export(out):
    (BASE/'chapter-2-2.md').write_text(manuscript());shutil.copytree(BASE,out/'assets/cmap',dirs_exist_ok=True)
    from goso_brand import values
    css=[]
    for theme in ['light','dark']:
        selector='.cmap-figure' if theme=='light' else '[data-theme="dark"] .cmap-figure'
        css.append(selector+'{'+''.join('--gv-'+k+':'+v+';' for k,v in values(theme).items())+'}')
    (out/'cmap.css').write_text('\n'.join(css)+'\n'+(ROOT/'web/cmap.css').read_text())
    for name in ['cmap.js','cmap-globe.js','cmap-globe-math.mjs','cmap-globe-analysis.mjs']:shutil.copy2(ROOT/'web'/name,out/name)
