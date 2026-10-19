"""Five progressively enhanced, source-backed figures for Chapter 1."""
from pathlib import Path
import csv,hashlib,html,json,math,shutil
import chapter1_explorers
import chapter1_tables

ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
T=lambda lang,z,e:z if lang=='zh' else e
COLORS=['#087984','#2d5f9f','#76508b','#407a51']
SDG_COLORS=['#e5243b','#dda63a','#4c9f38','#c5192d','#ff3a21','#26bde2','#fcc30b','#a21942','#fd6925','#dd1367','#fd9d24','#bf8b2e','#3f7e44','#0a97d9','#56c02b','#00689d','#19486a']
SDGS=[('无贫穷','No poverty'),('零饥饿','Zero hunger'),('良好健康与福祉','Good health and well-being'),('优质教育','Quality education'),('性别平等','Gender equality'),('清洁饮水和卫生设施','Clean water and sanitation'),('经济适用的清洁能源','Affordable and clean energy'),('体面工作和经济增长','Decent work and economic growth'),('产业、创新和基础设施','Industry, innovation and infrastructure'),('减少不平等','Reduced inequalities'),('可持续城市和社区','Sustainable cities and communities'),('负责任消费和生产','Responsible consumption and production'),('气候行动','Climate action'),('水下生物','Life below water'),('陆地生物','Life on land'),('和平、正义与强大机构','Peace, justice and strong institutions'),('促进目标实现的伙伴关系','Partnerships for the goals')]
# Short translations and summaries of the DPGA's nine standard requirements.
DPG=[
 ('SDG 相关性','SDG relevance','说明与可持续发展目标的关联。','Explain the link to sustainable development.'),
 ('开放许可','Open licensing','提供允许复用的开放许可。','Provide an open licence for reuse.'),
 ('清晰权属','Clear ownership','说明数字成果的权属。','Identify who owns the digital solution.'),
 ('平台独立性','Platform independence','说明对封闭平台的依赖。','Explain dependencies on closed platforms.'),
 ('文档','Documentation','提供理解和采用所需的资料。','Provide information needed for adoption.'),
 ('非个人识别数据提取','Non-PII data extraction','在适用时支持非个人识别数据提取。','Enable extraction of non-personal data where applicable.'),
 ('隐私与适用法律','Privacy and applicable laws','披露隐私及适用法律要求。','Address privacy and applicable legal requirements.'),
 ('标准与最佳实践','Standards and best practices','遵循相关标准和实践。','Follow relevant standards and practices.'),
 ('不造成伤害','Do no harm','关注数据安全、有害内容与骚扰防护。','Address data security, harmful content and harassment.')]
PILLAR_NOTES=[
 ('让更多参与者进入开放协作，并获得持续成长与连接的机会。','Enable participation, growth and connections in open collaboration.','人数增长不直接证明公平、就业或教育效果。','More participants do not by themselves establish social outcomes.'),
 ('观察代码、模型与数据的产出，并区分可见、可获取与可复用条件。','Observe code, model and data supply alongside the conditions for reuse.','发布数量不能代替质量或完整开放程度。','Release counts do not establish quality or full openness.'),
 ('观察贡献怎样通过协作、采用与派生，在生态中形成影响。','Examine influence through collaboration, adoption and derivatives.','网络信号不直接折算成经济或社会收益。','Network signals do not directly quantify economic or social benefits.'),
 ('观察持续维护、治理、许可与公共利益导向的证据。','Examine evidence on maintenance, governance, licensing and public value.','托管或许可标签不能单独证明治理质量。','Hosting or licence labels alone do not establish governance quality.')]
DIM_NOTES={
 '1.1':('参与有多广，人才如何分布？','How broad is participation and how is talent distributed?'),
 '1.2':('参与者从哪里来，如何跨边界协作？','Who participates, and how do they collaborate across boundaries?'),
 '2.1':('协作怎样形成持续的软件产出？','How does collaboration sustain software output?'),
 '2.2':('有哪些模型供给，来自怎样的发布方？','Which models are supplied, and by whom?'),
 '2.3':('开放数据供给是否充分且多样？','Is open data supply broad and diverse?'),
 '3.1':('代码贡献如何形成生态影响？','How do code contributions create ecosystem influence?'),
 '3.2':('模型如何被采用、讨论和进一步派生？','How are models adopted, discussed and adapted?'),
 '3.3':('数据如何被采用，并支持后续复用？','How are datasets adopted and reused?'),
 '4.1':('谁参与治理，哪些规则有据可查？','Who governs, and which rules can be verified?'),
 '4.2':('开放技术如何面向公共利益？','How does open technology serve public interests?')}
FIGURES={'fig-1-0-1_report_logic.svg':'report-logic','fig-1-1-1_linux_collaboration.svg':'linux','fig-1-1-2_model_derivatives.svg':'models','fig-1-1-3_sdgs_dpga.svg':'public-goods','fig-1-2-1_osdg_framework.svg':'goals','fig-1-3-1_osdi_explorer.svg':'indicators'}
def path(lang,route):return '/2026/'+lang+'/'+route
def link(href,label,extra=''):return f'<a href="{E(href)}" class="inline-link" {extra}>{label}</a>'
def dump(value):return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def story():return json.loads((ROOT/'content/story-data.json').read_text())
def import_story(repo,ref):
    raw=repo/'data/raw/2026/external'
    files={'contributors':'lfx-korg/contributor-leaderboard.json','organizations':'lfx-korg/organization-leaderboard.json','models':'atom/fig-03_global-regional-model-adoption.json'}
    result={'source_ref':ref,'exported_at':'2026-10-11','use_scope':'External background only; excluded from OSDI and processed-data counts','files':{}}
    for key,rel in files.items():
        f=raw/rel;data=json.loads(f.read_text());result['files'][key]={'path':'data/raw/2026/external/'+rel,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
        if key=='models':result[key]=data
        else:result[key]={'total':data['meta']['total'],'saved_rows':len(data['data']),'rows':[{k:row[k] for k in ['name','contributions','percentage']} for row in data['data'][:10]]}
    (ROOT/'content/story-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assets=ROOT/'content/report-assets';assets.mkdir(exist_ok=True)
    with (assets/'model-derivatives-story.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['date','china','unitedStates','europe']);writer.writeheader();writer.writerows(result['models'])
    print('Imported external story samples: 2 leaderboards and 28 monthly observations; kept separate from OSDI.')
def fig_open(fid,kicker,title,desc,lang):
    return f'<figure id="{fid}" class="interactive-figure chapter-one-visual" data-slide-key="{fid}" data-lang="{lang}" data-viz="{fid}" aria-labelledby="{fid}-title"><div class="viz-heading"><span class="eyebrow">{kicker}</span><h4 id="{fid}-title">{title}</h4><p>{desc}</p></div>'
def fig_end(caption,source):
    zh=caption.startswith('图')
    filename=next((name for name in FIGURES if name[4:].split('_')[0] in caption),None)
    if filename and filename not in source:source+=' · '+link('/assets/report/'+filename,'下载静态 SVG ↓' if zh else 'Download static SVG ↓','download')
    return f'<figcaption>{caption}<span class="viz-source">{source}</span></figcaption><noscript><p class="viz-boundary">'+('启用 JavaScript 可切换图中视角。' if zh else 'Enable JavaScript to switch chart views.')+'</p></noscript></figure>'
def bar_rows(rows,lang):
    top=rows[0]['contributions'];out=[]
    for i,r in enumerate(rows):
        label=f'{r["name"]} · {r["contributions"]:,} · {r["percentage"]}%'
        out.append(f'<button type="button" class="linux-bar" data-row="{i}" aria-label="{E(label)}"><span class="bar-name" title="{E(r["name"])}"><i>{i+1:02d}</i>{E(r["name"])}</span><span class="bar-track"><span style="width:{r["contributions"]/top*100:.4f}%"></span></span><b>{r["contributions"]:,}</b></button>')
    return ''.join(out)
def linux(lang,r,source):
    t=lambda z,e:T(lang,z,e);s=story();org=s['organizations'];person=s['contributors']
    out=fig_open('fig-linux','01 / LINUX · COLLECTIVE MAINTENANCE',t('一个内核，连接持续的全球协作','One kernel, sustained global collaboration'),t('谁在贡献？切换组织与贡献者，选择条形查看贡献记录与占比。','Who contributes? Switch between organizations and contributors, then select a record.'),lang)
    out+='<div class="linux-kpis" role="group" aria-label="'+t('选择观察对象','Choose an observation unit')+'">'
    for key,d,z,e in [('organizations',org,'组织','Organizations'),('contributors',person,'贡献者','Contributors')]:
        out+=f'<button type="button" data-linux-kind="{key}" aria-pressed="{str(key=="organizations").lower()}"><strong>{d["total"]:,}</strong><span>{t(z,e)}<small>'+t('累计榜单总记录数','Cumulative leaderboard records')+'</small></span></button>'
    out+='</div><div class="viz-chart-label"><span id="linux-series-title">'+t('组织榜单前 10 条记录','First 10 organization records')+'</span><span>'+t('条形：贡献记录量','Bars: recorded contributions')+'</span></div><div id="linux-bars" class="linux-bars">'+bar_rows(org['rows'],lang)+'</div>'
    out+='<div id="linux-selection" class="viz-selection" aria-live="polite"><strong>Red Hat</strong><span>725,866 · '+t('本类榜单占比 14.95%','Share in this leaderboard 14.95%')+'</span></div><p class="viz-boundary">'+t('LFX 累计快照 · 2026-10-11。组织与个人占比分别计算；条形按各自榜首缩放。累计记录不等于年度活跃数，也不表示 OpenRank。','LFX cumulative snapshot · 11 October 2026. Each view has its own share denominator and bar scale. Counts are neither annual activity nor OpenRank.')+'</p>'
    out+='<script type="application/json" id="linux-viz-data">'+dump({'organizations':org,'contributors':person})+'</script>'
    return out+fig_end(t('图 1-1-1 · Linux 组织与贡献者累计排行。','Figure 1-1-1 · Cumulative Linux organization and contributor rankings.'),link(source(s['files']['organizations']['path']),t('组织快照 ↗','Organization snapshot ↗'))+' · '+link(source(s['files']['contributors']['path']),t('贡献者快照 ↗','Contributor snapshot ↗')))
def models(lang,r,source):
    t=lambda z,e:T(lang,z,e);s=story();data=s['models'];last=data[-1]
    out=fig_open('fig-models','02 / OPEN MODELS · REUSE & DERIVATIVES',t('开放的影响，延伸到下一次创造','Open impact extends into the next creation'),t('查看 28 个月的新增微调与衍生模型构成；归属按基础模型发布方记录。','Explore 28 months of new fine-tunes and derivatives, attributed to base-model publishers.'),lang)
    out+='<div class="model-readout"><div><span id="model-current-month">2026.02</span><strong><span id="model-china-share">70</span><small>%</small></strong><p>'+t('当月新增衍生基于中国发布方的基础模型','Of new derivatives used base models from Chinese publishers')+'</p></div><div class="model-measures" id="model-measures">'
    for key,name,color in [('china',t('中国','China'),'#4E87C5'),('unitedStates',t('美国','United States'),'#279FA9'),('europe',t('欧洲','Europe'),'#9973B7')]:out+=f'<div style="--region:{color}"><i></i><span>{name}</span><b data-model-value="{key}">{last[key]}%</b></div>'
    out+='</div></div><div class="stack-chart"><div class="stack-axis"><span>100%</span><span>50%</span><span>0%</span></div><div class="month-bars" role="group" aria-label="'+t('按月选择模型衍生占比','Select monthly model derivative shares')+'">'
    for i,d in enumerate(data):
        label=d['date']+f' · China {d["china"]}% · US {d["unitedStates"]}% · Europe {d["europe"]}%'
        out+=f'<button type="button" class="month-bar" data-month="{i}" aria-pressed="{str(i==len(data)-1).lower()}" aria-label="{E(label)}">'+''.join(f'<span class="stack-segment region-{key}" style="height:{d[key]}%"></span>' for key in ['china','unitedStates','europe'])+'</button>'
    out+='</div></div><div class="month-endpoints">'+''.join(f'<span data-month-tick="{i}" style="--tick:{(i+.5)/len(data)*100:.4f}%">{label}</span>' for i,label in [(0,'2023.11'),(2,'2024.01'),(14,'2025.01'),(27,'2026.02')])+'</div><div class="month-control"><label for="model-month">'+t('月份','Month')+f'</label><button type="button" data-month-step="-1" aria-label="'+t('上一个月','Previous month')+f'">‹</button><input id="model-month" type="range" min="0" max="{len(data)-1}" value="{len(data)-1}" step="1"><button type="button" data-month-step="1" aria-label="'+t('下一个月','Next month')+'">›</button><output id="model-month-label" for="model-month">2026.02</output></div><p id="model-announcement" class="sr-only" aria-live="polite"></p>'
    out+='<p class="viz-boundary">'+t('ATOM 跟踪的 Hugging Face 样本；地区指基础模型发布方归属，不是下游用户国籍。原始百分比保留，取整可能使分项之和不等于 100%。本图是外部背景案例，不进入 OSDI 或正式榜单。','ATOM’s tracked Hugging Face sample. Regions refer to base-model publishers, not downstream users. Original percentages are preserved; rounding can leave totals different from 100%. External background only, excluded from OSDI and formal rankings.')+'</p><script type="application/json" id="model-viz-data">'+dump(data)+'</script>'
    return out+fig_end(t('图 1-1-2 · 从模型供给到生态衍生：月度构成变化。','Figure 1-1-2 · From model supply to derivatives: monthly composition.'),link(source(s['files']['models']['path']),t('仓库固定快照 ↗','Fixed repository snapshot ↗'))+' · '+link('/assets/report/model-derivatives-story.csv',t('下载案例 CSV ↓','Download story CSV ↓'),'download')+' · '+link('https://www.atomproject.ai/','ATOM ↗'))+chapter1_tables.render([[t('月份','Month'),t('中国','China'),t('美国','US'),t('欧洲','Europe')]]+[[d['date']]+[str(d[k])+'%' for k in ['china','unitedStates','europe']] for d in data],lang,'table-model-months',E,'/assets/report/model-derivatives-story.csv')

def sdg_text_color(color):
    channels=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in channels]
    luminance=sum(c*w for c,w in zip(linear,[.2126,.7152,.0722]))
    return '#08202d' if luminance>.22 else '#fff'

def wheel_svg(lang):
    def pt(radius,deg):return (160+radius*math.cos(math.radians(deg)),160+radius*math.sin(math.radians(deg)))
    out=['<svg viewBox="0 0 320 320" class="sdg-wheel" role="group" aria-label="'+T(lang,'联合国 17 项可持续发展目标','The 17 UN Sustainable Development Goals')+'">']
    for i,(z,e) in enumerate(SDGS):
        start=-90+i*360/17+1;end=-90+(i+1)*360/17-1;a,b=pt(149,start);c,d=pt(149,end);ee,f=pt(106,end);g,h=pt(106,start);x,y=pt(128,(start+end)/2)
        pathd=f'M {a:.3f} {b:.3f} A 149 149 0 0 1 {c:.3f} {d:.3f} L {ee:.3f} {f:.3f} A 106 106 0 0 0 {g:.3f} {h:.3f} Z'
        out.append(f'<g data-sdg="{i+1}" role="button" tabindex="0" aria-pressed="{str(i==8).lower()}" aria-label="SDG {i+1} {E(T(lang,z,e))}"><path d="{pathd}" fill="{SDG_COLORS[i]}"/><text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" fill="{sdg_text_color(SDG_COLORS[i])}" font-family="Arial,sans-serif" font-size="13" font-weight="bold">{i+1}</text></g>')
    out+=['<text x="160" y="144" text-anchor="middle" class="sdg-center-label">UN SDGs</text><text x="160" y="176" text-anchor="middle" class="sdg-center-sub">'+T(lang,'17 项共同目标','17 shared goals')+'</text></svg>']
    return ''.join(out)
def public_goods(lang,r,source):
    t=lambda z,e:T(lang,z,e)
    out=fig_open('fig-public-goods','03 / PUBLIC VALUE · GOALS & CONDITIONS',t('联合国 SDGs × 数字公共品联盟 DPGA','UN SDGs × Digital Public Goods Alliance'),t('点选目标或条件，查看具体含义。','Select a goal or condition to read its meaning.'),lang)
    out+='<div class="public-goods-layout"><div class="sdg-side"><span class="viz-label">'+t('希望改善什么？ · 17 项发展目标','WHAT SHOULD IMPROVE? · 17 GOALS')+'</span>'+wheel_svg(lang)+'<div class="sdg-selection" id="sdg-selection" aria-live="polite"><b>SDG 9</b><span>'+t(*SDGS[8])+'</span></div></div><div class="dpga-side"><span class="viz-label">'+t('需要具备什么？ · 9 项实践条件','WHAT IS REQUIRED? · 9 CONDITIONS')+'</span><div class="dpga-wordmark">DPGA<small>Digital Public Goods Alliance</small></div><div class="dpg-grid">'
    for i,(z,e,zd,ed) in enumerate(DPG):out+=f'<button type="button" data-dpg="{i}" aria-pressed="{str(i==0).lower()}"><b>{i+1:02d}</b><span>{E(t(z,e))}</span></button>'
    out+='</div><div id="dpg-selection" class="dpg-selection" aria-live="polite"><strong>'+t(*DPG[0][:2])+'</strong><p>'+t(*DPG[0][2:])+'</p></div></div></div>'
    out+='<script type="application/json" id="sdg-viz-data">'+dump([t(z,e) for z,e in SDGS])+'</script><script type="application/json" id="dpg-viz-data">'+dump([{'title':t(z,e),'description':t(zd,ed)} for z,e,zd,ed in DPG])+'</script>'
    return out+fig_end(t('图 1-1-3 · 目标方向与数字公共品条件的关系示意，GOSD 绘制。','Figure 1-1-3 · Development goals and digital public good conditions, illustrated by GOSD.'),link('https://sdgs.un.org/goals','UN SDGs ↗')+' · '+link('https://www.digitalpublicgoods.net/standard','DPG Standard ↗')+' · '+link('https://creativecommons.org/licenses/by-sa/4.0/','DPG Standard: CC BY-SA 4.0'))
def goal_records(lang,r):
    t=lambda z,e:T(lang,z,e);out={}
    for pi in range(4):
        code='X'+str(pi+1);rows=[i for i in r['indicators'] if i['pillar_id']==code];first=rows[0];desc=PILLAR_NOTES[pi]
        out[code]={'title':code+' · '+first['pillar_name_zh' if lang=='zh' else 'pillar_name_en'],'question':t(*desc[:2]),'boundary':t(*desc[2:]),'indicators':[i['indicator_code'] for i in rows],'color':COLORS[pi]}
        for dim in dict.fromkeys(i['dimension_id'] for i in rows):
            selected=[i for i in rows if i['dimension_id']==dim];out[dim]={'title':dim+' · '+selected[0]['dimension_name_zh' if lang=='zh' else 'dimension_name_en'],'question':t(*DIM_NOTES[dim]),'boundary':t(*desc[2:]),'indicators':[i['indicator_code'] for i in selected],'color':COLORS[pi]}
    return out
def goal_panel(item,lang):
    t=lambda z,e:T(lang,z,e)
    return '<div class="goal-detail-copy"><span class="viz-label">'+t('目标解读','GOAL NOTES')+'</span><strong>'+E(item['title'])+'</strong><p>'+E(item['question'])+'</p><small>'+E(item['boundary'])+'</small></div><div class="goal-detail-indicators"><span class="viz-label">'+t('对应指标','RELATED INDICATORS')+'</span><div>'+''.join(link(path(lang,'data/indicators/')+'#indicator-'+code,E(code)) for code in item['indicators'])+'</div></div>'
def goals(lang,r,source):
    t=lambda z,e:T(lang,z,e);items=goal_records(lang,r)
    out=fig_open('fig-osdg-goals','04 / OSDGs · FRAMEWORK EXPLORER',t('四个支柱，十个观察维度','Four pillars, ten observation dimensions'),t('悬停或点击支柱与维度，查看目标内涵、解释边界和对应指标。','Hover or select a pillar or dimension to inspect its meaning, limits and indicators.'),lang)
    out+='<div class="goal-map"><div class="goal-hotspots">'
    for pi in range(4):
        code='X'+str(pi+1);group=[x for x in r['indicators'] if x['pillar_id']==code]
        out+=f'<div class="goal-pillar-row" style="--pillar:{COLORS[pi]}">'
        out+=f'<button type="button" class="goal-pillar-name" data-goal="{code}" aria-controls="goal-selection" aria-pressed="{str(pi==0).lower()}"><b>{code}</b><span>{E(group[0]['pillar_name_zh' if lang=='zh' else 'pillar_name_en'])}</span></button><div class="goal-dimension-buttons">'
        for dim in dict.fromkeys(x['dimension_id'] for x in group):
            first=next(x for x in group if x['dimension_id']==dim)
            out+=f'<button type="button" data-goal="{dim}" aria-controls="goal-selection" aria-pressed="false"><b>{dim}</b><span>{E(first['dimension_name_zh' if lang=='zh' else 'dimension_name_en'])}</span></button>'
        out+='</div></div>'
    out+='</div></div><label class="goal-mobile-select" for="goal-select">'+t('选择支柱或维度','Choose a pillar or dimension')+'<select id="goal-select">'+''.join('<option value="'+key+'">'+E(item['title'])+'</option>' for key,item in items.items())+'</select></label><div class="goal-selection" id="goal-selection" aria-live="polite">'+goal_panel(items['X1'],lang)+'</div><p class="viz-boundary">'+t('支柱和维度是分类结构，不表示权重或评分。四个评价支柱与 GOSO、GOSR、GOSL、GOSM 交叉对应。','Pillars and dimensions are categories, not weights or scores. They cut across GOSO, GOSR, GOSL and GOSM.')+'</p><script type="application/json" id="goals-viz-data">'+dump(items)+'</script>'
    return out+fig_end(t('图 1-2-1 · OSDGs 目标框架（交互版）。','Figure 1-2-1 · Interactive OSDGs framework.'),link('/assets/report/fig-1-2-1_osdg_framework.svg',t('下载原框架图 SVG ↓','Download framework SVG ↓'),'download')+' · '+link(path(lang,'data/goals/'),t('目标框架详解 →','Explore the goals →')))
def indicator_panel(row,lang):
    t=lambda z,e:T(lang,z,e);codes={'GOSO':'02','GOSR':'03','GOSL':'04','GOSM':'05'}
    return '<div><span class="viz-label">'+E(row['indicator_code'])+' · '+E(row['role'])+'</span><strong>'+E(row['indicator_name_zh'])+'</strong><p>'+E(row['definition'])+'</p><div class="indicator-calculation"><small>'+t('计算口径','Calculation')+'</small>'+E(row['calculation_rule'])+'</div></div><div><span class="viz-label">'+t('证据与用途','EVIDENCE & USE')+'</span><p>'+E(row['data_status'])+'</p><small>'+E(row['remaining_evidence'])+'</small><div class="indicator-chapters">'+''.join(link(path(lang,'chapters/'+codes[c]+'/'),E(c)) for c in row['chapter_tags'].split(';') if c in codes)+'</div>'+link(path(lang,'data/indicators/')+'#indicator-'+row['indicator_code'],t('查看完整定义与关联数据 →','Full definition and related files →'))+'</div>'
def indicators(lang,r,source):
    t=lambda z,e:T(lang,z,e);rows=r['indicators'];roles=[('',t('全部 29 项','All 29')),('北极星',t('北极星','North Star')),('驱动',t('驱动','Driver')),('诊断',t('诊断','Diagnostic'))]
    out=fig_open('fig-osdi-map','05 / OSDI · INDICATOR ATLAS',t('从一个目标，走到一项可查证的指标','From a goal to a verifiable measure'),t('按角色突出指标；悬停、聚焦或选择一个指标，查看它观察什么、如何计算、还缺哪些证据。','Highlight indicators by role. Hover, focus or select a measure to inspect its definition, calculation and evidence gaps.'),lang)
    out+='<div class="viz-role-filters" role="group" aria-label="'+t('指标角色','Indicator roles')+'">'+''.join(f'<button type="button" data-indicator-role="{E(key)}" aria-pressed="{str(not key).lower()}">{label}</button>' for key,label in roles)+'</div><div class="indicator-atlas">'
    for pi in range(4):
        group=[row for row in rows if row['pillar_id']=='X'+str(pi+1)];p0=group[0]
        out+=f'<div class="atlas-pillar" style="--pillar:{COLORS[pi]}"><div class="atlas-pillar-title"><b>X{pi+1}</b><span>'+E(p0['pillar_name_zh' if lang=='zh' else 'pillar_name_en'])+'</span></div>'
        for dim in dict.fromkeys(row['dimension_id'] for row in group):
            items=[x for x in group if x['dimension_id']==dim];out+='<div class="atlas-dimension"><span>'+dim+' · '+E(items[0]['dimension_name_zh' if lang=='zh' else 'dimension_name_en'])+'</span><div>'
            for row in items:
                available=bool(row['related_data_paths']);code=row['indicator_code'];short=row['indicator_name_zh'] if lang=='zh' else code
                out+=f'<button type="button" data-indicator="{code}" data-role="{row["role"]}" aria-pressed="{str(code=="DevScale").lower()}" aria-controls="indicator-selection" aria-label="{E(code+" "+row["indicator_name_zh"])}"><span class="availability-dot {"related" if available else "pending"}" aria-hidden="true"></span>{E(short)}</button>'
            out+='</div></div>'
        out+='</div>'
    out+='</div><div class="atlas-legend"><span><i class="availability-dot related"></i>'+t('有关联资料','Related files')+'</span><span><i class="availability-dot pending"></i>'+t('待补匹配数据','Data pending')+'</span><span id="atlas-role-count" aria-live="polite">'+t('突出显示 29 / 29 项','Highlighting 29 / 29 measures')+'</span></div><div id="indicator-selection" class="indicator-inspector" aria-live="polite">'+indicator_panel(rows[0],lang)+'</div><p class="viz-boundary">'+t('三种角色不构成评分权重；“有关联资料”不等于“指标已算完”。ModelRank 保留概念说明，外部故事数据不用于补齐指标。','Roles do not imply scoring weights. Related files do not mean completed measurements. ModelRank remains conceptual; external stories do not fill indicator gaps.')+'</p><script type="application/json" id="indicators-viz-data">'+dump({x['indicator_code']:x for x in rows})+'</script>'
    return out+fig_end(t('图 1-3-1 · OSDI 指标地图：4 个支柱、10 个维度、29 项指标。','Figure 1-3-1 · OSDI atlas: 4 pillars, 10 dimensions and 29 measures.'),link('/assets/report/osdi_indicator_dictionary.csv',t('统一指标字典 CSV ↓','Canonical indicator dictionary CSV ↓'),'download')+' · '+link(path(lang,'methodology/'),t('方法与范围 →','Methods and scope →')))
def render(kind,lang,r,source):
    if kind=='models':
        from chapter1_model_story import enhance
        return enhance(models(lang,r,source),lang)
    return {'linux':linux,'public-goods':public_goods,'goals':goals,'indicators':chapter1_explorers.indicators,'report-logic':chapter1_explorers.logic}[kind](lang,r,source)
