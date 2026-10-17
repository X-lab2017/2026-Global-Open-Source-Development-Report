"""Section 5.1: global supply, China–US comparison and China drilldown."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='gosm-supply-v4-compact'
FIGS={
 'world':('5.1-01','全球模型与数据供给全景','上看国家分布与发布组织，下看模型、数据集的增长轨迹。','supply51'),
 'cnus':('5.1-02','中美供给比较：规模与发布主体','从组织、模型和配套数据的规模，进入发布账号与头部集中度。','supply51'),
 'china':('5.1-03','中国模型供给地图','全国—省级地区—发布组织，在一张图中理解中国的供给基础。','supply51'),
}
TOPIC=dict(
 id='ch05-s01',n='5.1',en='SUPPLY & CONTRIBUTION',title='供给与贡献',
 question='模型与数据供给如何增长，主要由谁提供，又在哪里形成参与基础？',
 lede='先看全球供给的规模与增长，再比较中美总量背后的发布主体，最后从中国地图进入地区和具体组织。三幅图沿同一条路径回答：资产如何积累，供给如何组织，参与如何落地。',
 metric='X2 技术产出与开放供给 · OpenModelRelease / ModelSupplierDiv，并以配套数据观察衔接 OpenDatasetRelease。模型仓库与发布账号分别计数；下载表示获取活动，点赞表示社区关注。公开可见不等于已核验全部开源条件。',
 findings=[
  ('供给增长，需要同时看资产与参与基础','报告同一快照的年度回溯中，模型数较上年同日增长58.3%，发布账号增长48.4%。全球图把年度积累与模型、数据集的月度新增分别呈现。','world'),
  ('中美供给，呈现不同的主体结构','本次组织样本中，中国与美国的模型下载量前三账号份额分别为79.3%和33.1%。总量与头部集中度一起看，才能辨识谁在支撑供给。','cnus'),
  ('中国观察，可以落到地区与具体组织','中国样本包括147个组织、6,093个模型。其中135个组织具有省级归属，另12个组织保留待补记录；地图支持继续查看发布者。','china')],
 figures=list(FIGS),
 narratives=[
  ('视角一｜从全球分布，看供给如何积累','平台总览记录315.88万个模型、109.30万个数据集。地图呈现可定位组织的供给分布，下方趋势进一步回答增长来自哪些资产、发生在哪些月份。月度新增与年度回溯使用各自的统计窗口；切换国家只改变地域观察，全球增长曲线保持清晰标注。'),
  ('视角二｜从中美总量，看谁在支撑供给','中美是本节的重点比较对象。模型与配套数据分别观察，发布账号、数量、下载和关注构成四个比较维度。点击数量、下载或关注，上方对照与下方发布者排行使用同一指标；再切换头部集中度，理解总量由少数账号还是更广泛的参与者形成。'),
  ('视角三｜从中国地图，看参与基础如何落地','国家总量需要落实到地区和组织。中国图沿全国、省级地区、发布账号逐层展开，把供给规模与具体主体放在一起。未覆盖地区保持留白，省级归属待补单列；这些可查证的组织节点，为后续合作、维护和区域支持提供观察入口。')],
 actions=[
  ('公共部门与研究机构','建立模型与数据的持续供给观察','同时跟踪资产增长与发布者基础，固定统计窗口和地域覆盖，保留未知归属。把模型版本、发布账号和配套数据分别记录，形成可复核的长期序列。','world'),
  ('企业、平台与开源社区','支持多元供给，重视关键发布者的持续维护','将头部账号的维护需求与更广泛的参与机会一起考虑。支持模型和配套数据的版本化发布、清晰说明与持续维护，并结合实际获取和后续复用评价支持效果。','cnus'),
  ('地区、高校与合作伙伴','以具体组织为节点，扩大协作参与','从地区内已有的发布组织和真实任务出发，连接高校、企业与社区开展共同维护。资源支持对应可查证的组织、资产和维护记录，避免仅凭地区仓库数量评价成效。','china')],
 related=[('1.3 OSDI · 供给与多样性','/2026/zh/chapters/01/#ch01-s03'),('2.1 V-Map · 规模与增长','/2026/zh/chapters/02/#ch02-s01'),('2.5 A-Map · 资产积累','/2026/zh/chapters/02/#ch02-s05'),('3.6 M-Ranking · 模型影响力','/2026/zh/chapters/03/#ch03-s06')])

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
    out.append('<nav class="gm-section-nav" aria-label="5.1 阅读路径"><a href="#gm-world">01 全球全景</a><a href="#gm-cnus">02 中美专题</a><a href="#gm-china">03 中国观察</a><a href="#gm-actions-1">行动建议</a></nav>')
    out.append('<div class="gm-findings">'+''.join(f'<a href="#gm-{f}"><span>{i+1:02d} / 核心发现</span><h3>{a}</h3><p>{b}</p></a>' for i,(a,b,f) in enumerate(t['findings']))+'</div>')
    out.append('<p class="s51-evidence-strip"><b>两层证据</b> 平台补充快照：2026-10-17读取；报告基线：2026-09-13。各图独立标注。<span>全球增长 → 中美结构 → 中国参与</span></p>')
    for i,(key,(title,body)) in enumerate(zip(t['figures'],t['narratives'])):
        out.append(f'<div class="gm-narrative"><h3>{title}</h3><p>{body}</p></div>'+panel(key))
    out.append('<section class="gm-actions" id="gm-actions-1"><span class="eyebrow">FROM EVIDENCE TO ACTION</span><h3>从供给增长，走向持续参与</h3><div>'+''.join(f'<article><span>{w}</span><h4>{a}</h4><p>{b}</p><a href="#gm-{f}">查看对应证据 ↗</a></article>' for w,a,b,f in t['actions'])+'</div></section>')
    out.append('<nav class="gm-topic-end"><a href="#gm-framework">返回模型生态观察框架 ↑</a><a href="#ch05-s02">哪些供给成为再创造的起点？进入5.2 →</a></nav></section>')
    return ''.join(out)
