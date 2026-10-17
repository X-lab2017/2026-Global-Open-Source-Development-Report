"""Section 5.1: global supply, China–US comparison and China drilldown."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='gosm-supply-v2'
FIGS={
 'world':('5.1-01','全球模型与数据供给全景','从全球规模进入国家分布；选择国家，可在本图继续查看发布组织。','supply51'),
 'cnus':('5.1-02','中美对照：组织、模型与配套数据','同一批已识别国家的发布组织，比较供给规模、下载与社区关注。','supply51'),
 'publishers':('5.1-03','中美发布者：谁在支撑供给？','并排查看发布账号，切换规模与集中度，理解总量背后的主体结构。','supply51'),
 'china':('5.1-04','中国模型供给地图','全国—省级地区—发布组织，所有选择与详情都在同一张图中。','supply51'),
 'supply':('5.1-05','供给增长：模型、数据与发布基础','年度回溯与月度新增分别观察；每个视图保留自己的统计窗口。','supply51'),
 'release':('5.1-06','发布节奏与事件透镜','从月度高峰进入具体发布事件，理解新增模型中的不同供给活动。','monthly'),
 'portfolio':('5.1-07','模型与数据集：发布者的配套结构','一个点代表一个发布账号；看模型供给与配套数据如何分布。','supply51'),
 'scenarios':('5.1-08','供给角色与持续参与：情景实验','调整投入构成与参与假设，探索下一阶段值得持续观测的内容。','simulation'),
}
TOPIC=dict(
 id='ch05-s01',n='5.1',en='SUPPLY & CONTRIBUTION',title='供给与贡献',
 question='谁在构建模型与数据供给，怎样形成持续参与的基础？',
 lede='从全球分布进入中美比较，再深入中国的地区与发布组织。供给规模、模型获取与社区关注共同呈现生态结构；模型与配套数据一起观察，让持续发布和部署适配的作用更清楚。',
 metric='X2 技术产出与开放供给 · OpenModelRelease / ModelSupplierDiv，并以配套数据观察衔接 OpenDatasetRelease。下载与点赞分别作为获取和关注信号。公开仓库与发布账号分别计数；模型家族归并、正式开放资格与供给方实体归并仍需核验。',
 findings=[
  ('同时看见模型与配套数据','平台总览记录 315.88 万个模型、109.30 万个数据集。国家视图另用 826 个组织样本；全平台规模与地域样本分别展示。','world'),
  ('中美总量背后，发布主体结构不同','本次组织样本中，下载量前三账号占中国模型下载量的 79.3%，美国为 33.1%。下载集中度与模型数量分布需要共同观察。','publishers'),
  ('中国观察可以落到具体组织','中国样本包含 147 个组织、6,093 个模型。省级条目覆盖其中 135 个组织，另外 12 个组织保留“省级归属待补”。','china')],
 figures=list(FIGS),
 narratives=[
  ('全球全景｜让供给与获取同时可见','模型、数据集与运行演示共同组成可获取的资产基础。全球总览呈现平台规模，地图聚焦已识别国家的组织样本。图内切换模型与配套数据，比较数量、下载和关注，并继续查看具体发布账号。'),
  ('中美专题｜比较多种供给，理解不同位置','中美在模型生态中是重要观察对象。本节将组织、模型、配套数据集、累计下载和社区关注并列呈现。国家归属沿用发布组织标签，下载不表示使用者所在地，也不作为模型能力评分。'),
  ('从国家总量，进一步看到发布主体','相同规模可以由不同数量和类型的账号形成。模型与数据集分别排序，比较头部份额与完整账号分布；同一企业的多个账号尚未归并，因此这里观察发布账号的集中度。'),
  ('中国观察｜从地区进入具体发布组织','全国规模需要与地区分布、发布组织和可获取资产一起阅读。沿用第二章地图底图，保留全部省级地区；未覆盖与观测为零分别表达，省级归属待补的记录仍计入全国。'),
  ('进一步探索｜规模如何形成，增长怎样变化？','报告年度点位观察当前可见模型与发布账号的积累过程；平台月表观察模型、数据集的新增节奏。两类序列截止时间不同，在独立视图中展示，避免把更新日期当成同一统计窗口。'),
  ('发布高峰，需要回到具体事件解释','2025年9月至2026年8月，中美法德的发布节奏存在差异。原稿中法国2026年7月的高峰主要来自OpenMed集中发布的设备适配版本，提示新增仓库同时包含基础开发、改进与部署适配。'),
  ('看见模型之外的配套资产','在这批模型发布组织中，部分账号同时提供数据集，部分账号以模型发布为主。散点图显示账号的资产组合，帮助寻找可进一步研究的配套实践；数量关系本身不证明模型采用了某个数据集。'),
  ('模拟实验｜把下一步的问题具体化','供给角色和发布者持续参与尚缺少完整的可比底表。本图使用明确标注的教学情景，让读者调整供给构成与留存假设，探索需要补充哪些观测。情景结果不用于中美排名、核心发现或政策成效判断。')],
 actions=[
  ('公共部门与研究机构','建立持续、可比较的模型与数据供给观察','统一发布账号、模型版本与数据集的统计窗口，持续记录供给方分布、发布节奏与未知归属。以可复核的模型—数据资产记录支持长期观察，避免仅按仓库总数安排资源。','cnus'),
  ('企业、平台与开源社区','支持多层次供给与长期维护','同时识别基础开发、微调、量化、部署适配与配套数据的作用；为持续维护保留资源，发布清晰的上游、版本、适配和使用说明。结合真实下载与后续复用，观察维护投入的作用。','release'),
  ('地区、高校与合作伙伴','扩大参与基础，形成可持续的协作节点','从具体组织和真实任务出发，连接地区、高校、企业与社区开展共同维护；关注头部账号的持续维护需求，也为其他参与者提供稳定入口。以共同维护记录、参与分布和具体采用证据跟踪进展。','china')],
 related=[('1.3 OSDI · 供给与多样性','/2026/zh/chapters/01/#ch01-s03'),('2.5 A-Map · 资产积累','/2026/zh/chapters/02/#ch02-s05'),('3.6 M-Ranking · 模型影响力','/2026/zh/chapters/03/#ch03-s06')])

def payload():
    p=ROOT/'content/gosm/supply-observation.json'
    d=json.loads(p.read_text()) if p.exists() else {}
    geo=json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
    prov=json.loads((ROOT/'content/cmap/data.json').read_text())['provinces']
    codes={r['id']:r['source_code'] for r in prov}
    d['geometry']={'world':geo['world'],'china':[{**f,'source_code':codes.get(f['id'])} for f in geo['china']]}
    return d

def section(t,panel,E):
    out=[f'<section id="ch05-s01" class="chapter-section gm-topic s51-topic"><header class="gm-topic-header"><span class="eyebrow">5.1 / SUPPLY & CONTRIBUTION</span><h2>{t["title"]}</h2><p class="gm-question">{t["question"]}</p><p>{t["lede"]}</p><details class="gm-metric"><summary>指标定位与前文衔接</summary><p>{t["metric"]}</p><div class="gm-related">'+''.join(f'<a href="{u}">{l} ↗</a>' for l,u in t['related'])+'</div></details></header>']
    out.append('<nav class="gm-section-nav" aria-label="5.1 阅读路径"><a href="#gm-world">01 全球全景</a><a href="#gm-cnus">02 中美专题</a><a href="#gm-china">03 中国观察</a><a href="#s51-explore">04 进一步探索</a><a href="#gm-actions-1">行动建议</a></nav>')
    out.append('<div class="gm-findings">'+''.join(f'<a href="#gm-{f}"><span>{i+1:02d} / 核心发现</span><h3>{a}</h3><p>{b}</p></a>' for i,(a,b,f) in enumerate(t['findings']))+'</div>')
    out.append('<p class="s51-evidence-strip"><b>两层证据</b> 平台补充快照：2026-10-17读取；报告基线：2026-09-13。各图独立标注。<span>7幅实测图 · 1幅模拟情景</span></p>')
    for i,(key,(title,body)) in enumerate(zip(t['figures'],t['narratives'])):
        if i==4:out.append('<div class="s51-explore-heading" id="s51-explore"><span class="eyebrow">FURTHER EXPLORATION</span><h3>四个角度，继续理解供给结构</h3><p>从增长、发布事件与资产配套进入具体问题；最后一幅为独立的模拟实验。</p></div>')
        out.append(f'<div class="gm-narrative"><h3>{title}</h3><p>{body}</p></div>'+panel(key))
    out.append('<section class="gm-actions" id="gm-actions-1"><span class="eyebrow">FROM EVIDENCE TO ACTION</span><h3>让持续、多样的供给成为共同基础</h3><div>'+''.join(f'<article><span>{w}</span><h4>{a}</h4><p>{b}</p><a href="#gm-{f}">查看对应证据 ↗</a></article>' for w,a,b,f in t['actions'])+'</div></section>')
    out.append('<nav class="gm-topic-end"><a href="#gm-framework">返回模型生态观察框架 ↑</a><a href="#ch05-s02">哪些供给成为再创造的起点？进入5.2 →</a></nav></section>')
    return ''.join(out)
