"""GOSM: evidence-led model supply, reuse networks, and openness."""
from pathlib import Path
import csv,gzip,hashlib,html,json,shutil
import gosm_supply_content as S51
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
DIR=ROOT/'content/gosm'
VERSION=S51.VERSION
REF='c397b97c273803c6828396d422164909bfeb383c'
BASE='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/'+REF+'/'
E=lambda x:html.escape(str(x),quote=True)
FILES={
 'supply':'fig-5-1-1_hf_cumulative_models_publishers.csv',
 'countries':'fig-5-1-2_country_model_contribution.csv',
 'monthly':'fig-5-1-3_country_monthly_new_models.csv',
 'derivation':'fig-5-2-1_hf_cumulative_derivation.csv',
 'flows':'fig-5-2-2_cross_country_derivation_flows.csv',
 'head':'fig-5-2-3_modelrank_country_head_trend.csv',
 'quadrants':'fig-5-3-1_openness_quadrants.csv',
 'openRegions':'fig-5-3-2_openness_region_structure.csv',
 'openPublishers':'fig-5-3-3_openness_publisher_types.csv'}

def rows(key):
    data=list(csv.DictReader((REPO/'data/processed/chapter5'/FILES[key]).open(encoding='utf-8-sig')))
    for r in data:
        for k,v in r.items():
            if v=='':r[k]=None;continue
            try:r[k]=float(v) if '.' in v else int(v)
            except ValueError:pass
    return data

def load_optional(name,default):
    p=DIR/name
    if p.exists():return json.loads(p.read_text())
    zipped=p.with_suffix(p.suffix+'.gz')
    return json.loads(gzip.decompress(zipped.read_bytes())) if zipped.exists() else default

def payload():
    d={key:rows(key) for key in FILES}
    d.update(version=VERSION,sourceRef=REF,files=FILES,sourceBase=BASE+'data/processed/chapter5/',network=load_optional('network.json',{'nodes':[],'edges':[]}),cases=load_optional('cases.json',[]),opennessCurrent=load_optional('openness-current.json',{}),method=load_optional('openness-method.json',{}))
    # The reviewed C-Map supplies geography IDs and source-aligned geometry.
    cd=json.loads((ROOT/'content/cmap/data.json').read_text())
    en={r['en']:r['id'] for r in cd['countries']}
    en.update({'United States of America':'US','United States':'US','Russian Federation':'RU','South Korea':'KR','North Korea':'KP','Czech Rep.':'CZ','Dem. Rep. Korea':'KP','Republic of Korea':'KR','Côte d\'Ivoire':'CI'})
    geo=json.loads((ROOT/'content/vmap/source/world.json').read_text());world=[]
    for f in geo['features']:
        name=f['properties']['name']
        if name=='Antarctica':continue
        g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']];parts=[]
        for poly in polys:
            for ring in poly:
                coords=[(round((lon+180)*2.45,1),round((85-lat)*2.75,1)) for lon,lat,*_ in ring]
                if coords:parts.append('M'+'L'.join(f'{x},{y}' for x,y in coords)+'Z')
        world.append({'name':name,'code':en.get(name),'d':''.join(parts)})
    d['supply51']=S51.payload()
    d['world']=world
    d['geography']=[{'id':r['id'],'name':r['name'],'en':r['en'],'coordinates':r.get('coordinates')} for r in cd['countries']]
    return d

FIGS={
 'framework':('5-0-1','模型生态观察框架','从同一个模型出发，切换供给、复用和开放三个视角。','framework'),
 'supply':('5-1-1','供给增长：模型与发布者','从模型数量走向参与供给的主体基础。','supply'),
 'world':('5-1-2','全球模型供给与获取图谱','同一张地图，比较模型供给、获取与社区关注。','countries'),
 'release':('5-1-3','新增供给：节奏与发布事件','选择国家与月份，理解持续发布和集中适配。','monthly'),
 'cnus':('5-1-4','中美专题：从规模到生态位置','在各自统计范围内，对照供给、下载、关注与头部席位。','countries,head'),
 'derivation':('5-2-1','再创造的规模：模型派生趋势','同时观察派生数量和在可见模型中的比例。','derivation'),
 'network':('5-2-2','模型复用网络：从一个基座到更多创造','展开可核验的基座—派生关系，探索具体模型的上下游。','network'),
 'flows':('5-2-3','跨地区复用：连接从哪里发生','保留表列关系的样本范围，观察国家间的复用关联。','flows'),
 'head':('5-2-4','头部模型：地域构成如何变化','比较不同榜单深度，并沿月份观察席位结构。','head'),
 'openness':('5-3-1','模型开放结构：完整性 × 开放性','两个维度分别阅读，分类依据可以就近查阅。','quadrants'),
 'open-groups':('5-3-2','开放条件：地区与发布主体的差异','数量与比例一同查看，比较同一评估样本的分组结构。','openRegions,openPublishers'),
 'dossiers':('5-3-3','模型开放档案：逐项核对具体版本','从分类走向证据：权重、代码、数据说明和许可各有来源。','cases')}

TOPICS=[
 dict(id='ch05-s01',n='5.1',en='SUPPLY & CONTRIBUTION',title='供给与贡献',question='谁在构建模型供给，增长中包含什么？',lede='模型成为可获取的技术资产，也形成新的协作入口。供给规模、发布者基础与持续适配共同构成观察起点；中美对照进一步揭示规模、获取和头部生态位置的不同组合。',metric='X2 模型开放供给 · OpenModelRelease / ModelSupplierDiv；下载与点赞分别作为获取和关注信号。公开仓库尚需开放资格与去重核验。',findings=[('规模与发布基础同步扩大','当前可见样本中，2026 年累计模型为 306.22 万，发布账户为 61.33 万；较上一年同日回溯值分别增长 58.3% 和 48.4%。','supply'),('中美在供给与头部席位上呈现不同结构','已识别国家样本中，美国模型数量与累计下载居前；2026 年 8 月 ModelRank Top 20 中中国占 16 席、美国 4 席，Top 100 为 46 与 49 席。','cnus'),('适配也构成新增供给','原稿核对的法国 2026 年 7 月高峰，主要来自 OpenMed 的设备适配。新增仓库需要结合发布类型解释。','release')],figures=['supply','world','release','cnus'],narratives=[('从累计规模走向供给基础','发布账户可能是个人或组织，不等于开发者人数。年度点位均按 2026-09-13 仍公开可见的模型回溯创建时间；它们描述同一可见样本的积累过程。'),('谁在提供模型，谁受到关注','国家比较只包含归属已识别的组织模型。该部分约占平台模型数量的 2.3%，却覆盖约 79.9% 的累计下载；图中同时披露覆盖情况，避免把识别样本推广为全部研发活动。'),('理解月度高峰中的具体贡献','持续发布与集中适配都可能扩大可用供给。基础模型、微调、量化和终端适配的作用不同，应在项目记录中保留类型和上游来源。'),('中美对照：规模、关注与头部结构','美国在已识别组织样本中的模型数量和累计下载具有明显规模；中国的下载与点赞份额均高于其模型数量份额，在最头部 ModelRank 样本中也占较多席位。榜单扩展到 Top 1000 时，结构再次变化，提示“头部位置”与“供给广度”需要同时观察。')],actions=[('公共部门','支持持续、可复用的供给','把维护、任务覆盖与部署适配纳入支持项目的交付要求，跟踪后续可核验复用。','supply'),('企业与社区','把模型与交付说明共同发布','明确版本、上游、任务、适配与维护状态，帮助使用者识别差异和贡献路径。','release'),('平台与研究机构','用可比范围观察中美生态','分别维护发布账户、版本与系列映射，保留未知归属，定期核验同范围的规模与头部结构。','cnus')],related=[('2.5 A-Map · 资产积累','/2026/zh/chapters/02/#ch02-s05'),('3.5 E-Ranking · 新供给','/2026/zh/chapters/03/#ch03-s05'),('3.6 M-Ranking · 模型与组织','/2026/zh/chapters/03/#ch03-s06')]),
 dict(id='ch05-s02',n='5.2',en='NETWORKS & INFLUENCE',title='网络与影响力',question='哪些模型成为再创造的起点，复用如何扩展？',lede='一个模型的生态作用，在后续开发者如何使用、改进和延伸它的过程中逐步显现。从派生规模进入具体网络，再观察跨地区连接与头部结构，让影响力拥有可以追溯的关系背景。',metric='X3 模型影响力 · ModelRank。派生关系、下载与点赞分别呈现；网络图布局和节点大小不生成新的 ModelRank 得分。',findings=[('派生规模扩大，占比并非同步上升','2026 年可见派生模型为 85.87 万，占可见模型的 28.04%；2025 年对应回溯比例为 29.14%。数量与比例表达不同变化。','derivation'),('关系解释模型怎样被继续创造','网络保留明确声明的基座—派生关系。相同任务只说明用途相近，不作为派生关系连接。','network'),('观察深度会改变地域构成','2026 年 8 月 Top 20、Top 100、Top 1000 中，中国席位分别为 16、46、200，美国为 4、49、388；未知归属分别为 0、4、330。','head')],figures=['derivation','network','flows','head'],narratives=[('先看规模，再看关系','派生标记依赖平台元数据的可见性与识别规则。没有记录不直接表示没有复用；同一批可见模型的回溯趋势也不等于各年独立留存的全量历史。'),('沿着模型谱系，理解生态影响','选择一个基座或派生模型，查看已记录的上游和下游；网络全景帮助定位簇群，谱系视图帮助读清关系。模型可以有多个上游，节点的位置只是阅读布局。'),('把跨地区复用放回样本边界','原表保留双端国家可识别的 10,943 对跨国关系。它表示发布主体之间的复用关联，不表示使用者所在地、资金流向或实际部署量。'),('从榜单名单走向结构变化','第三章展示具体模型、任务和发布账户；这里观察各月头部样本的席位构成。模型版本逐项计数，份额分母保留未知归属，避免把识别覆盖变化误读为生态增减。')],actions=[('公共部门与资助方','支持可复用的基础能力','结合真实上下游关系识别持续被采用的基础模型，同时核查维护需求和适用场景。','network'),('企业与社区','让下游改进能够回到上游','记录明确的派生来源、版本和改进类型，并通过问题反馈、文档和维护协作形成共同积累。','network'),('平台与合作机构','建设可追溯的关系记录','持续维护基座、派生、组织归属和时间信息，为跨地区合作提供可核验对象。','flows')],related=[('1.3 OSDI · 从关系理解影响','/2026/zh/chapters/01/#ch01-s03'),('2.6 D-Map · 跨地区连接','/2026/zh/chapters/02/#ch02-s06'),('3.6 M-Ranking · 模型榜','/2026/zh/chapters/03/#ch03-s06')]),
 dict(id='ch05-s03',n='5.3',en='OPENNESS & PUBLIC VALUE',title='开源开放与分级体系',question='模型开放了什么，人们能够怎样继续使用与改进？',lede='开放条件决定哪些材料可以获取、怎样使用以及能否继续改进。把分类结果连接到具体版本的材料和许可，才能使开放供给成为可讨论、可复核的共同基础。',metric='X4 开源善治与公共价值 · AIAssetTransparency / LicenseOpenness / ComplianceLicenseCov。原评估分级与 OSI 定义、DPGA 正式认可分别维护。',findings=[('开放条件与材料完整性并不相同','870 个原评估模型中，483 个属于低完整、高开放；同时高完整、高开放的有 117 个，占 13.45%。','openness'),('分组比例要结合样本规模','原评估样本包含中国 404、美国 258 个模型；企业模型为 711 个。地区和主体类型的比例分别使用本组分母。','open-groups'),('具体版本的证据更有助于使用','权重可得、推理可运行、训练可复现与许可权利是不同检查项。模型档案逐项列出一手来源与仍未知的信息。','dossiers')],figures=['openness','open-groups','dossiers'],narratives=[('两个维度，回答不同问题','完整性观察技术材料的提供程度；开放性观察原评估采用的许可与使用条件分组。本图保留既有 L/O 分级，不把“高开放”自动解释为符合 OSI 开源 AI 定义。'),('在同一评估样本内比较','地区、组织类型的样本数量差异较大，比例不代表总体代表性或评估质量。保持同一原评估集合，才能读清不同分组的结构。'),('从分类回到可核验的开放档案','独立补充的模型案例固定具体版本，检查许可、权重、推理与训练代码、数据说明及维护入口。文档存在只是证据入口，不直接证明完整复现或公共价值效果。')],actions=[('公共部门与资助方','试点可核验的开放交付要求','明确需要提供的模型材料、许可说明和维护记录，逐项检查交付完整性。','dossiers'),('企业与研究机构','发布版本化开放档案','让代码、权重、数据说明和许可对应到具体版本，并保留变更日期与依据。','dossiers'),('平台与基金会','公开评估规则与复核入口','解释分级依据、样本边界与未知项；正式公共品认可依相应程序核验。','openness')],related=[('1.2 OSDGs · 公共价值','/2026/zh/chapters/01/#ch01-s02'),('2.7 G-Map · 治理与公益','/2026/zh/chapters/02/#ch02-s07'),('附录 C · AI 数字公共品','/2026/zh/appendices/dpg/')])]

FIGS.update(S51.FIGS)
TOPICS[0]=S51.TOPIC

def panel(key):
    num,title,desc,sources=FIGS[key]
    extra_tools='<button data-gm-table>数据表</button>' if key in S51.FIGS else ''
    close_hint='<span class="s51-close-hint"> · 关闭 ×</span>' if key in S51.FIGS else ''
    return f'''<article id="gm-{key}" class="gm-panel{' s51-panel' if key in S51.FIGS else ''}" data-gm-chart="{key}"><header class="gm-chart-head"><div><span class="eyebrow">图 {num} / {'OBSERVATION FRAMEWORK' if key=='framework' else 'MODEL ECOSYSTEM'}</span><h3>{title}</h3></div><div class="gm-tools"><button data-gm-full>全屏</button><button data-gm-source>口径与来源</button>{extra_tools}<button data-gm-svg>SVG ↓</button><button data-gm-csv>数据 CSV ↓</button></div></header><p class="gm-chart-deck">{desc}</p><div class="gm-controls"></div><div class="gm-view"></div><div class="gm-readout" aria-live="polite"></div><details class="gm-source"><summary>口径与来源{close_hint}</summary><div class="gm-source-body"></div></details><details class="gm-table"><summary>查看本图数据{close_hint}</summary><div class="gm-table-host"></div></details><noscript><p>交互需要启用 JavaScript。可从章末下载原始数据，并阅读正文。</p></noscript></article>'''

def topic(t):
    if t['n']=='5.1':return S51.section(t,panel,E)
    k=int(t['n'][-1]);out=[f'''<section id="{t['id']}" class="chapter-section gm-topic"><header class="gm-topic-header"><span class="eyebrow">{t['n']} / {t['en']}</span><h2>{t['title']}</h2><p class="gm-question">{t['question']}</p><p>{t['lede']}</p><details class="gm-metric"><summary>指标定位与前文衔接</summary><p>{t['metric']}</p><div class="gm-related">'''+''.join(f'<a href="{url}">{label} ↗</a>' for label,url in t['related'])+'''</div></details></header><nav class="gm-section-nav" aria-label="本节阅读路径">'''+''.join(f'<a href="#gm-{key}">{i+1:02d} {FIGS[key][1].split("：")[0]}</a>' for i,key in enumerate(t['figures']))+f'<a href="#gm-actions-{k}">行动建议</a></nav><div class="gm-findings">'+''.join(f'<a href="#gm-{fig}"><span>{i+1:02d} / 核心发现</span><h3>{title}</h3><p>{body}</p></a>' for i,(title,body,fig) in enumerate(t['findings']))+'</div>']
    for i,(key,(title,body)) in enumerate(zip(t['figures'],t['narratives'])):
        out.append(f'<div class="gm-narrative"><h3>{title}</h3><p>{body}</p></div>'+panel(key))
    out.append(f'<section class="gm-actions" id="gm-actions-{k}"><span class="eyebrow">FROM EVIDENCE TO ACTION</span><h3>让观察连接到持续行动</h3><div>'+''.join(f'<article><span>{who}</span><h4>{title}</h4><p>{body}</p><a href="#gm-{fig}">查看对应证据 ↗</a></article>' for who,title,body,fig in t['actions'])+'</div></section>')
    nxt='#ch05-s0'+str(k+1) if k<3 else '/2026/zh/chapters/06/'
    label=TOPICS[k]['title'] if k<3 else '第六章 · 展望与行动'
    out.append(f'<nav class="gm-topic-end"><a href="#gm-framework">返回模型生态观察框架 ↑</a><a href="{nxt}">{label} →</a></nav></section>')
    return ''.join(out)

def chapter(lang):
    if lang!='zh':return '<div class="reader-note">The complete Chinese Chapter 5 review is available: model supply, China–US comparison, reuse networks and openness. Full English text will follow the Chinese review.</div>'+''.join(f'<section class="chapter-section" id="{t["id"]}"><h2>{t["n"]} {t["en"].title()}</h2><a href="/2026/zh/chapters/05/#{t["id"]}">Read and explore the Chinese chapter →</a></section>' for t in TOPICS)
    out=['''<div class="goso-chapter gm-chapter" data-gosm-version="gosm-supply-v4-compact"><header class="gm-opening"><div class="gm-topline"><span>CHAPTER 05 / GOSM</span><span>2026.10 · 5.1 深化评审版</span></div><h2>从模型供给，<br>走向可持续的共同创新。</h2><p class="gm-lead">谁在构建模型？哪些模型成为再创造的起点？开放条件又如何支撑后续使用？沿同一个模型，连接供给、复用与公共价值。</p><div class="gm-opening-links"><a href="#ch05-s01">01 供给与贡献</a><a href="#ch05-s02">02 网络与影响力</a><a href="#ch05-s03">03 开放与公共价值</a></div><p class="gm-opening-note">承接 OSDGs / OSDI 的目标与指标，联读第二章的生态地图、第三章的模型榜单和第四章的技术全景。</p></header>''',panel('framework')]
    out.extend(topic(t) for t in TOPICS)
    out.append('''<section id="gm-methods" class="gm-methods"><span class="eyebrow">METHODS & SOURCES</span><h3>把范围、时间与证据留在一起</h3><details><summary>供给、国家归属与年度回溯</summary><p>5.1 地域补充快照于2026-10-17读取，覆盖826个组织、73,088个模型和这些组织的12,502个配套数据集；地理接口未声明统一统计日。全平台总览标注2026-10-16，月表截至2026-07，分开显示。年度累计沿用2026-09-13报告快照，按当时仍可见模型的创建时间回溯，不是各年独立历史存档。个人账户不纳入组织国家比较，未识别部分单列。下载是获取活动、点赞是关注信号，均不等于用户数、模型能力或开发者实质贡献。</p></details><details><summary>ModelRank、谱系与国家关系</summary><p>ModelRank 国家席位使用 2024-07—2026-08 原始汇总，Top 20／100／1000 各有独立分母。模型网络使用单独标注的参考项目快照，仅连接明确的基座关系；任务相似和人工组织连线不进入派生证据。跨国关系底表仅含双端已识别的样本，角色方向未确认时采用无向配对观察。不同日期和覆盖的三类数据不直接合并计算。</p></details><details><summary>开放分类、补充核验与公共品</summary><p>三份原始开放统计来自既有 870 模型评估，2026-09-14 提取；高完整为 L3—L5，高开放为 O2—O4。分级是原评估方法，不能直接当作 OSI 开源 AI 资格或 DPGA 认可。当前补充记录与官方模型案例另标采集日期，不回填原样本。没有证据的检查项显示“待核”，不自动按否或零处理。</p><p>参照：<a href="https://opensource.org/ai/open-source-ai-definition" target="_blank" rel="noopener">OSI OSAID 1.0</a> · <a href="https://www.digitalpublicgoods.net/standard" target="_blank" rel="noopener">DPG Standard</a>。</p></details><details><summary>原始数据、复核与复用</summary><p><a href="/assets/gosm/provenance.json">数据来源与指纹 ↗</a> · <a href="/assets/gosm/data.json" download>本章完整数据 JSON ↓</a> · <a href="/assets/gosm/methods.md" download>本章方法说明 ↓</a>。各图 CSV 保留对象、日期和指标范围；SVG 导出保留当前视角、来源和时间。原始数据与可核验派生值分别记录。</p><ul>''')
    out.extend(f'<li><a href="/assets/gosm/data/{name}" download>{name} ↓</a></li>' for name in FILES.values())
    out.append('''</ul></details></section><dialog id="gm-fullscreen" aria-label="第五章图表全屏"><div class="gm-fullscreen-bar"><strong>模型生态</strong><div><button data-gm-prev>← 上一图</button><button data-gm-next>下一图 →</button><button data-gm-theme>切换主题</button><button data-gm-close>退出全屏 ×</button></div></div><div id="gm-fullscreen-body"></div></dialog><script type="application/json" id="gosm-data">'''+json.dumps(payload(),ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c')+'</script></div>')
    return ''.join(out)

def appendix(lang):
    if lang!='zh':return '<div class="reader-note">This research reference separates source assessment categories, OSI OSAID 1.0 and formal DPGA recognition.</div><p><a href="/2026/zh/appendices/dpg/">Read the Chinese reference →</a></p>'
    return '''<div class="reader-note">研究参照 · 2026-10-17 核对。报告观察、开放定义与正式公共品认可分别适用，本报告不授予认证。</div><section class="chapter-section"><h2>三种问题，分别回答</h2><div class="reader-table-wrap"><table class="reader-table"><thead><tr><th>层次</th><th>回答的问题</th><th>依据</th></tr></thead><tbody><tr><td>本报告的生态观察</td><td>模型提供了哪些材料，源评估怎样分组？</td><td>第五章 L/O 分类、版本化证据档案及明确的数据边界</td></tr><tr><td>OSI 开源 AI 定义</td><td>是否具备使用、研究、修改与分享的自由及所需材料？</td><td><a href="https://opensource.org/ai/open-source-ai-definition">OSAID 1.0 ↗</a></td></tr><tr><td>DPGA 正式认可</td><td>数字解决方案是否通过 DPG Standard 评审？</td><td><a href="https://www.digitalpublicgoods.net/standard">DPG Standard 与 Registry ↗</a></td></tr></tbody></table></div></section><section class="chapter-section"><h2>把开放条件连接到具体版本</h2><p>OSAID 1.0 将四项自由与修改系统所需的材料相联系，包括足够详细的训练数据信息、训练和运行的完整代码、模型参数及相应开放条款。训练数据信息要求不能简化为“所有原始数据必须全部公开”，权重可下载也不能独立证明整个系统符合定义。</p><p>本报告采用无总分的证据清单：权重、推理实现、完整预训练代码、数据说明、许可与维护入口。每项保留版本、日期和来源；证据不足显示“待核实”。不能将 RAIL 等带使用条件的许可笼统列为 OSI 认可许可，必须检查具体文本和适用对象。</p><p><a href="/2026/zh/chapters/05/#gm-dossiers">查看四个具体版本的开放档案 →</a></p></section><section class="chapter-section"><h2>从研究证据走向公共品认可</h2><p>DPGA 当前标准包括九项要求，涵盖 SDG 相关性、开放许可、权属、平台独立、文档、非个人数据提取、隐私及适用法律、标准与最佳实践，以及设计上的伤害防范。项目经相应程序评审后进入 Registry；联盟成员资格与项目认可属于不同事项。</p><p>本报告不设置“金牌／银牌 DPG”或自定义认证阈值。多语言、轻量部署、持续维护和多方参与可以作为发展建议，不能写成所有项目都必须满足的官方认证条件。</p></section><section class="chapter-section"><h2>本报告建议采用的交付记录</h2><ol><li>明确模型版本、发布主体、上游关系和更新日期。</li><li>逐项附上材料与许可的具体来源，区分已观察、待核实和不适用。</li><li>说明服务的公共问题、目标人群及可验证的使用效果。</li><li>为维护、问题反馈与版本变更保留持续记录；需要正式认可时按官方标准申请。</li></ol><p><a href="/assets/gosm/methods.md">下载第五章方法说明 ↓</a> · <a href="/assets/gosm/openness-method.json">查看原评估规则的已知范围 ↗</a> · <a href="/2026/zh/chapters/05/#ch05-s03">返回 5.3 开源开放与分级体系 →</a></p></section>'''

def export(out):
    dest=out/'assets/gosm';(dest/'data').mkdir(parents=True,exist_ok=True)
    for key,name in FILES.items():shutil.copy2(REPO/'data/processed/chapter5'/name,dest/'data'/name)
    for f in (REPO/'data/processed/chapter5').glob('fig-5-1-0*.csv'):shutil.copy2(f,dest/'data'/f.name)
    d=payload();(dest/'data.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
    p={'version':VERSION,'report_commit':REF,'sources':[{'key':key,'path':'data/processed/chapter5/'+name,'url':BASE+'data/processed/chapter5/'+name,'sha256':hashlib.sha256((dest/'data'/name).read_bytes()).hexdigest(),'rows':len(d[key])} for key,name in FILES.items()],'supply51':{'meta':d['supply51']['meta'],'sources':d['supply51']['sources'],'views':['global distribution and growth','China–US supply and publishers','China geography']},'network':d['network'].get('meta',{}),'openness':{k:v for k,v in d['opennessCurrent'].items() if k!='models'},'policy':'Original report CSV unchanged. Supply, network, current openness and official cases are separate dated evidence sets. Current 5.1 has three observed-data views; legacy exploratory datasets remain archived.'}
    (dest/'provenance.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
    for f in DIR.iterdir():
        if f.is_file():
            shutil.copy2(f,dest/f.name)
            if f.suffix=='.gz':(dest/f.stem).write_bytes(gzip.decompress(f.read_bytes()))

if __name__=='__main__':
    dest=REPO/'chapters/chapter5';dest.mkdir(exist_ok=True)
    for t in TOPICS:
        s=f'# {t["n"]} {t["title"]}\n\n> {t["question"]}\n\n{t["lede"]}\n\n## 指标定位\n\n{t["metric"]}\n\n## 核心发现\n\n'+ '\n\n'.join('**'+a+'。** '+b for a,b,_ in t['findings'])
        for key,(title,body) in zip(t['figures'],t['narratives']):s+='\n\n## '+title+'\n\n'+body+f'\n\n[图 {FIGS[key][0]}：{FIGS[key][1]}](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/05/#gm-{key})'
        s+='\n\n## 行动建议\n\n'+'\n\n'.join(f'**{who}：{title}。** {body}' for who,title,body,_ in t['actions'])+'\n\n## 来源与口径\n\n[原始数据与统计范围](../../data/README.md)；[本章方法说明](../../preview/content/gosm/methods.md)。正文与交互版使用同一证据，供整章评审。\n'
        (dest/(t['n']+'-'+t['title']+'.md')).write_text(s)
