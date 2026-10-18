"""Section 5.1: evidence-led supply narratives and three interactive views."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='gosm-supply-v9-story'
FIGS={
 'world':('5.1-01','全球模型与数据供给全景','从全球增长进入国家分布与发布组织。','supply51'),
 'cnus':('5.1-02','中美供给比较：规模与发布主体','比较资产规模、获取活动与发布账号的集中度。','supply51'),
 'china':('5.1-03','中国模型供给地图','从省级分布进入具体组织，观察区域参与基础。','supply51'),
}
TOPIC=dict(
 id='ch05-s01',n='5.1',en='SUPPLY & CONTRIBUTION',title='供给与贡献',
 question='模型与数据供给在哪里积累，如何让快速增长转化为更广泛、可持续的共同创新？',
 lede='承接 2.1 对参与基础的观察，延续 3.2 从规模、排名进入具体主体的读法，本节依次观察全球增长、中美供给结构与中国区域节点，将“谁在发布”连接到“怎样支持持续共建”。',
 metric='本节对应 OSDGs 的 X2“技术产出与开放供给”，重点观察 2.2“模型开放供给”，并以配套数据衔接 2.3“数据开放供给”；与 OSDI 的 OpenModelRelease、ModelSupplierDiv、OpenDatasetRelease、DataSupplierDiv 对应，连接 SDG 9、SDG 10。当前以公开可见仓库、发布账号与地域结构提供观察依据；开放资格、统计窗口与主体去重完成核验后，方可纳入正式指标测算。下载与点赞作为获取、关注的补充信号，实质贡献与复用影响在后续小节继续检验。',
 core_finding='三幅图揭示了相互衔接的供给结构：模型资产与发布账号同步扩张，持续维护成为需要共同回应的问题；中美样本的规模与头部集中度并不呈现同一种格局，模型与数据集需要分别观察；中国样本集中于少数区域，但不同指标指向不同的组织节点。由此，本节将供给增长连接到持续观测、多元供给与区域协作三类行动。',
 window_note='读图口径｜平台总览标注 2026-10-16；地域组织样本于 2026-10-17 读取，接口未声明统一统计日；月度新增截至 2026-07，年度累计来自 2026-09-13 报告快照。各组证据分别呈现，不拼接为同一条增长曲线。',
 findings=[
  ('资产与发布账号同步扩张','同一报告快照的年度回溯中，模型数增长58.3%，发布账号数增长48.4%。','world'),
  ('规模与集中度揭示不同结构','中美模型下载量前三账号占比分别为79.3%和33.1%；配套数据集对应占比为29.1%和42.8%。','cnus'),
  ('区域集聚需要进一步落实到组织','京沪浙粤占中国样本模型数的88.8%；147个组织中，12个仍缺省级归属。','china')],
 figures=list(FIGS),
 narratives=[
  ('视角一｜全球供给：从资产增长，看持续参与的基础','规模与增长揭示供给的扩张，国家分布与发布组织帮助辨识这些资产由谁提供。'),
  ('视角二｜中美比较：从总量差异，看供给由谁支撑','将模型与配套数据分别比较，再从规模和获取活动进入具体发布者与账号集中度。'),
  ('视角三｜中国观察：从区域集聚，看协作如何落地','同看地区的组织基础、资产数量与获取活动，将区域观察落实到可查证的发布主体。')],
 insights={
  'world':[
   '平台总览记录约315.88万个模型仓库与109.30万个数据集。另据2026年9月13日同一报告快照的创建时间回溯，模型数从上年同日的193.48万增至306.22万，增长58.3%；发布账号从41.32万增至61.33万，增长48.4%。资产与发布账号同步扩张，且资产积累更快。这里的发布账号包含个人与组织，回溯记录反映快照时仍可见的资产，并非历年独立存档。',
   '地域地图进一步呈现826个组织账号及其73,088个模型、12,502个配套数据集。模型样本中，中美合计占数量的71.7%、累计下载量的86.6%；法国、德国等也有可见的供给基础。这说明中美是理解当前样本结构的重要入口，其他地区仍是寻找伙伴与观察多样性的必要组成。上述份额仅适用于地域组织样本，不能扩展为全平台或全球的国家贡献占比。',
   '增长使可供选择的资产更加丰富，也提出版本管理、文档和长期维护的需求。公共支持可将资产新增与发布者的持续参与一起跟踪，并为覆盖不足的地区补充观测与合作入口。图中月度趋势帮助定位新增发生的时间；最新月完整性尚未说明，因此不能仅凭末端回落判断增长放缓。'],
  'cnus':[
   '在同一地域组织样本内，美国有348个账号发布模型，合计46,314个模型；中国对应为147个账号、6,093个模型。切换配套数据集后，美国为230个发布账号、5,938个数据集，中国为112个账号、1,354个数据集。两类资产的发布者基础并不相同。延续3.2将规模与影响分开阅读的方法，这里的仓库数量、下载与点赞也需分别解释：它们提供供给和关注的线索，不能直接代表模型能力。',
   '总量背后的主体结构差异更加鲜明。按模型累计下载量，中国样本的Qwen、BAAI与deepseek-ai三个账号合计占79.3%，美国样本前三账号占33.1%；切换配套数据集后，两国前三账号占比分别为29.1%与42.8%。模型与数据的头部格局并不一致，不能由模型榜推断整个数据生态。集中度按各国当前资产的下载量分别计算，账号也尚未合并为企业集团。',
   '这一差异提示，支持供给既要了解关键发布者承担的维护需求，也要为更多参与者提供进入条件。模型、数据集与评测材料可分别识别维护对象和支持方式；跨国合作则可围绕可核验的版本、共同任务与复用关系展开。地域数据集仅覆盖同一批模型发布组织，尚不包含完整的独立数据发布者群体。'],
  'china':[
   '中国样本包含147个组织账号与6,093个模型，其中135个组织已有省级归属，12个仍待补充。北京、上海、浙江、广东合计116个组织、5,408个模型，占全国样本模型数的88.8%；分母保留省级归属待补的149个模型。这一结构呈现样本中的头部集聚，为进一步识别区域节点提供入口。',
   '同一张地图中的不同指标，指向不同的组织基础。北京以47个组织居首，浙江以1,726个模型和约44.45亿次累计下载领先；切换配套数据集后，北京以480个数据集、约1,615.56万次累计下载居首。组织数量、资产积累与获取活动因此需要结合具体发布者阅读。地域归属依据组织账号记录，不表示所有研发、贡献或使用均发生在该地区。',
   '中国提供了一个从全国观察走向区域协作的实例：可以由已有组织围绕真实需求连接高校、企业与社区，开放任务、提供导师支持并组织持续维护，同时为其他地区保留远程参与入口。地图有助于寻找合作对象，合作能否持续仍需由项目记录验证；未覆盖地区也应优先补充证据，不能据此认定当地没有模型供给。']},
 action_lead='策略建议：让供给增长形成可持续的共同创新基础',
 action_intro='从可持续发展与国际合作的视角，三条建议分别回应观测基础、供给主体与区域组织方式。中美比较帮助辨识结构差异，中国地图提供区域化实例，行动效果仍需通过后续参与、维护和复用记录检验。',
 actions=[
  ('国际组织、公共部门与研究机构','建立可持续更新的模型与数据供给观察','共同维护可复用的供给记录，分别跟踪模型、数据集与发布账号的新增、更新和退出，将地域分布与主体结构纳入长期观察。对覆盖不足的地区，支持本地平台与社区参与数据共建。','world'),
  ('公共资助方、平台与开源社区','兼顾关键发布者维护与多元主体参与','依据模型和数据集各自的供给结构安排支持：为被广泛获取、持续维护的资产提供稳定资源，也为高校、中小团队和新参与者提供发布、评测与协作入口。头部集中度用于发现需进一步核查的对象，具体支持仍结合维护负担与公共需求。','cnus'),
  ('地区、高校、企业与合作伙伴','以区域节点承接开放任务与长期合作','以中国的区域结构为实例，从已有组织和真实需求出发，连接高校、企业、社区与公共机构，组织任务开放、导师协作、公开评审和后续维护。其他国家可结合本地节点与社区条件探索相应做法。','china')],
 action_followups={
  'world':'固定统计窗口，保留版本、许可、账号归属及未知项，并说明平台覆盖变化。持续观察有多少发布者保持更新、哪些地区获得新的参与机会，使资源投入能够与后续变化对应。',
  'cnus':'支持版本化模型、配套数据说明、评测材料与问题反馈机制；在条件适合的共同任务上开展跨国合作。以持续维护、下游复用与新增参与者的贡献评估支持效果，下载与点赞保留为辅助信号。',
  'china':'为资源较少地区提供远程参与和共同维护入口，使合作机会能够从头部节点向外扩展。以参与者能否留存、跨地区维护关系能否延续、本地需求是否得到回应评价节点作用。'},
 related=[('1.3 OSDI · 模型与数据供给','/2026/zh/data/indicators/#indicator-OpenModelRelease'),('2.1 V-Map · 参与基础','/2026/zh/chapters/02/#ch02-s01'),('2.5 A-Map · 资产积累','/2026/zh/chapters/02/#ch02-s05'),('3.2 C-Ranking · 主体与结构','/2026/zh/chapters/03/#ch03-s02')])

def payload():
    p=ROOT/'content/gosm/supply-observation.json'
    d=json.loads(p.read_text()) if p.exists() else {}
    geo=json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
    prov=json.loads((ROOT/'content/cmap/data.json').read_text())['provinces']
    codes={r['id']:r['source_code'] for r in prov}
    d['geometry']={'world':geo['world'],'china':[{**f,'source_code':codes.get(f['id'])} for f in geo['china']]}
    return d

def section(t,panel,E):
    paras=lambda xs: ''.join('<p>'+E(p)+'</p>' for p in xs)
    out=[f'<section id="ch05-s01" class="chapter-section gm-topic s51-topic"><header class="gm-topic-header"><span class="eyebrow">5.1 / SUPPLY & CONTRIBUTION</span><h2>{E(t["title"])}</h2><p class="gm-question">{E(t["question"])}</p><p>{E(t["lede"])}</p><div class="s51-position"><strong>目标与指标定位</strong><p>{E(t["metric"])}</p><div class="gm-related">'+''.join(f'<a href="{u}">{E(l)} →</a>' for l,u in t['related'])+'</div></div></header>']
    out.append('<div class="s51-findings" id="s51-findings"><h3>核心发现</h3><p>'+E(t['core_finding'])+'</p></div><p class="s51-window-note">'+E(t['window_note'])+'</p>')
    out.append('<nav class="gm-section-nav" aria-label="5.1 阅读路径"><a href="#s51-world">01 全球增长</a><a href="#s51-cnus">02 中美结构</a><a href="#s51-china">03 中国实例</a><a href="#gm-actions-1">行动建议</a></nav>')
    for key,(title,body) in zip(t['figures'],t['narratives']):
        out.append(f'<section class="s51-perspective" id="s51-{key}"><div class="gm-narrative"><h3>{E(title)}</h3><p>{E(body)}</p></div>'+panel(key)+'<div class="s51-reading">'+paras(t['insights'][key])+'</div></section>')
    out.append('<section class="gm-actions s51-actions" id="gm-actions-1"><span class="eyebrow">FROM OBSERVATION TO ACTION</span><h3>行动建议</h3><p class="s51-action-lead">'+E(t['action_lead'])+'</p><p class="s51-action-intro">'+E(t['action_intro'])+'</p><div class="s51-action-list">')
    for i,(who,title,body,key) in enumerate(t['actions'],1):
        out.append(f'<article class="s51-action"><span class="s51-action-number">{i:02d}</span><div><h4>{E(title)}</h4><p class="s51-action-who">{E(who)}</p>'+paras([body,t['action_followups'][key]])+f'<a href="#gm-{key}">查看对应证据 →</a></div></article>')
    out.append('</div></section><nav class="gm-topic-end"><a href="#gm-framework">返回模型生态观察框架 ↑</a><a href="#ch05-s02">从供给进入复用：哪些模型成为再创造的起点？ →</a></nav></section>')
    return ''.join(out)


def manuscript():
    t=TOPIC
    out=['# 5.1 '+t['title'],'> '+t['question'],t['lede'],'## 目标与指标定位',t['metric'],'## 核心发现',t['core_finding'],t['window_note']]
    for key,(title,body) in zip(t['figures'],t['narratives']):
        out+=['## '+title,body,f'[图 {FIGS[key][0]}：{FIGS[key][1]}](https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/05/#gm-{key})',*t['insights'][key]]
    out+=['## 行动建议',t['action_lead'],t['action_intro']]
    for i,(who,title,body,key) in enumerate(t['actions'],1):
        out+=['### '+str(i)+' '+title,who,body,t['action_followups'][key]]
    out+=['## 前文衔接',*[f'[{label}]({url})' for label,url in t['related']],'## 来源与口径','[地域与平台补充快照](../../preview/content/gosm/supply-observation.json)；[年度累计原表](../../data/processed/chapter5/fig-5-1-1_hf_cumulative_models_publishers.csv)；[本章方法说明](../../preview/content/gosm/methods.md)。正文与交互版使用同一证据。']
    return '\n\n'.join(out)+'\n'
