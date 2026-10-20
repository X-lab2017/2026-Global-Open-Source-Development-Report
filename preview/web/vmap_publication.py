"""Shared research manuscript and publication contract for section 2.1."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/vmap/fig-2-1-2_platform-coverage.json').read_text())
EDITION='2026-10-20-vmap-chapter-baseline'
PDF_NAME='GOSD-2026-section-2-1.pdf'
TITLE='全球开源活跃地图（V-Map）'
INTRO='第一章将持续共同创造及其公共价值作为观察重点。本节先看这种创造的参与基础：有多少人在参与，分布在哪里，规模如何变化。参与的广度为协作提供条件，贡献、影响与公共价值还需要沿着后续证据继续观察。'
QUESTION='全球开源参与分布在哪里，怎样把不断扩大的参与基础转化为持续共建？'
POSITION='对应 OSDGs 的 X1“人才规模与多样性”、1.1“规模与密度”，以活跃开发者规模（DevScale）为主，结合开发者总量、地域份额与历史变化，衔接 SDG 8、SDG 9。'
FINDING='全球参与基础持续扩大，五域呈现多中心格局；平台覆盖影响对规模的判断。中国实例显示，头部地区集聚了较大份额，同时也有广泛的区域参与。共同的行动方向是让这些参与更容易延续为长期协作。'
SNAPSHOT_NOTE='除特别说明外，本报告统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日。历史图中的年份指报告年度，均为前一年 7 月至当年 6 月。'
STORIES=[
('2.1.1 全球参与：规模扩大，活跃程度各异',[
 '图 2-1-1 显示，本报告期 GitHub 全球开发者总量约 1.94 亿，活跃开发者约 2,890.36 万。两类排名并不完全一致：英国的开发者总量高于德国，活跃规模却低于德国。总量描述积累起来的参与基础，活跃规模则反映当期参与。',
 '从 2022 至 2026 报告年度，全球开发者总量增至原来的约 2.3 倍，活跃规模增至约 1.9 倍。两者均在扩大，但变化幅度不同。对生态发展而言，扩大参与入口与支持参与延续需要同时推进，不能用累积规模代替对当期活动的观察。',
 '全球南方已有的参与力量，应进入长期合作的视野。印度、巴西、印度尼西亚合计约 527 万活跃开发者，占全球活跃规模约 18.2%。这些代表性样本为寻找共建伙伴提供了入口；社区能否承担更多长期工作，还需结合贡献与维护记录判断。']),
('2.1.2 五域比较：多中心格局与平台覆盖',[
 '图 2-1-2 以美国、欧洲、中国、印度和全球南方代表组观察相对位置。按编制组五域统计，美国、欧洲和中国的开发者总量均接近 3,000 万，印度及全球南方代表组也已形成较大规模。五域是比较框架，不构成全球的穷尽划分。',
 '活跃规模展示出另一层差异。2026 报告年度，欧洲约为 675 万，高于其他四组；美国与中国分别约为 465 万和 455 万，较为接近。五年间，印度与全球南方代表组的活跃规模均超过各自 2022 年度的两倍。比较当前规模与变化轨迹，能够同时看见已有中心和正在扩大的参与力量。',
 '平台覆盖决定哪些参与能够被看见。GitHub 记录的中国活跃规模为 250.48 万，补充国内平台后约为 370 万。国内约 120 万由编制组依据 Gitee、AtomGit 等官方数据，结合问卷调研去重得到。它补充了国际平台的观察范围；五域综合统计单独呈现，不重复叠加这一补充量。']),
('2.1.3 中国实例：头部集聚与多地参与',[
 '中国的参与规模持续扩大，区域分布仍有明显集聚。图 2-1-3 显示，京沪粤合计约 132 万活跃开发者，占全国约 52.6%；第 4—10 位地区约占 36.0%，其余 24 地约占 11.5%。',
 '区域集聚为连接更多参与者提供了起点。中国活跃规模从 2022 报告年度约 129 万增至 2026 年度约 250 万，但汇总值不能说明同一批人是否持续参与。区域合作可依托已有项目和社区，连接高校、企业与维护者，进一步观察参与能否延续。'])]
FIGURE_AFTER=[2,2,1]
ACTION_TITLE='2.1.4 行动建议：把参与基础转化为长期共建'
ACTION_INTRO='规模和分布帮助识别已有力量，公共投入则应进一步支持这些力量持续参与。结合三组观察，本节提出以下行动方向。'
STRATEGIES=[
('建立跨平台、可持续的参与监测',[
 '政府、国际组织与平台可围绕统一报告年度持续记录参与规模、地域分布和变化，结合国际与国内平台完善覆盖。规模比较同时说明对象范围与去重规则，使资源配置建立在可比较的观察上。',
 '后续将参与记录与贡献、维护和实际采用相连接，重点跟踪新增参与能否延续、支持不足地区能否获得稳定的协作入口。']),
('让全球南方进入共同建设与治理',[
 '国际组织、基金会与项目社区可支持本地维护者参与议题提出、技术决策与长期维护，围绕当地需求开展共同项目，并配套多语种文档、导师支持和双向交流。',
 '合作评价应关注持续贡献、共同维护、当地采用及其受益证据，使参与人数之外的实际作用更可见。']),
('以区域节点拓展长期协作机会',[
 '高校、企业、社区与地方公共机构可依托已有项目建立合作节点，开放真实任务、评审机会和导师资源，让资源较少地区也能通过远程协作参与共同维护。',
 '区域投入应观察合作能否跨越单次活动、参与者能否逐步承担责任，以及本地需求是否得到持续回应。中国实例提供区域观察的入口，具体做法须结合当地条件验证。'])]
INDICATOR_FEEDBACK='开发者总量用于观察参与基础，活跃规模用于观察当期参与。地域份额与集中度为派生分析；活跃增量不等于首次参与人数，规模与排行也不能单独代表贡献质量。'
GAPS=[
 '全球与中国地图、国家比较采用 OpenDigger / OpenShare 的 GitHub 报告年度底表；五域规模与历史序列采用编制组确认的原稿统计。',
 '国内平台补充量不分摊到省级地区，也不重复叠加到五域综合统计。万人读数沿用平台截断方式，计算保留原始精度。']
BRIDGE='V-Map 回答了参与力量在哪里、规模如何变化。下一节 C-Map 将继续观察这些参与形成了怎样的协作贡献，从参与基础走向共同建设的实际过程。'
FIGURES={
 'global':{'id':'2-1-1','title':'全球开发者总量、活跃分布与增长','files':['fig-2-1-1_global.svg'],'orientation':['landscape'],'status':'2026报告年度 · GitHub','note':'来源：OpenDigger / OpenShare。地图为活跃规模。'},
 'comparison':{'id':'2-1-2','title':'五域规模、历史演变与平台覆盖','files':['fig-2-1-2_a_current.svg','fig-2-1-2_bc_history-scenario.svg'],'orientation':['portrait','portrait'],'status':'2026报告年度 · 编制组五域统计与平台比较','note':'来源：报告编制组；OpenDigger / OpenShare。'},
 'china':{'id':'2-1-3','title':'中国区域参与分布、排名与结构','files':['fig-2-1-3_china.svg'],'orientation':['portrait'],'status':'2026报告年度 · GitHub · 34个省级地区','note':'来源：OpenDigger / OpenShare；开发者总量为平台估计。'}
}
SERIES_COLORS=['#156993','#279FA9','#4E87C5','#9973B7','#5C8A3C']
SERIES_DASH=[None,[5,3],[2,2],[7,2,2,2],[9,3]]
SNAPSHOT_AXIS_MAX_PEOPLE=[200000000,30000000,3000000]
MAP_COLORS=['#DCEBF2','#BCD8E4','#8FBFD3','#5B9FBE','#337FA6','#156993']

def manuscript():
 out=['# 2.1 '+TITLE,INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING,SNAPSHOT_NOTE]
 for i,((title,paras),fig) in enumerate(zip(STORIES,FIGURES.values())):
  split=FIGURE_AFTER[i]
  out+=['## '+title,*paras[:split],'图 '+fig['id']+' '+fig['title'],*paras[split:]]
 out+=['## '+ACTION_TITLE,ACTION_INTRO]
 for title,paras in STRATEGIES:out+=['### '+title,*paras]
 out+=['## 统计范围与指标说明',INDICATOR_FEEDBACK,*GAPS,BRIDGE]
 return '\n\n'.join(out)+'\n'

def specification():
 specs=[]
 for i,(key,f) in enumerate(FIGURES.items()):
  specs.append(dict(figure='图 '+f['id'],question=STORIES[i][0],claim=STORIES[i][1][0],data_scope=f['status'],web_default=['世界活跃地图＋双榜＋同源趋势','编制组五域规模；2026报告年度','中国活跃地图＋双榜＋全国趋势'][i],print_panels=[['A 世界地图与双榜','B 总量和活跃五年趋势'],['A 当前五域双指标','B 五域五年演变','C 国内平台补充比较'],['A 省级活跃地图','B 全国活跃趋势','总量和活跃前十','C 区域份额']][i],exploration_only=['地区详情、总量着色、中国下钻','国家前十、起点指数、年份与组别聚焦','所选省级详情、总量着色、缩放'][i],design_status='chapter2_reference',narrative_order='问题与观察 → 图件证据 → 解释与行动',figure_after_paragraph=FIGURE_AFTER[i],evidence_status=['report_year_source','author_confirmed_five_groups_and_domestic','report_year_provincial_source'][i],simulated=False,source='fig-2-1-2_platform-coverage.json',assets=f['files']))
 return specs
