"""Shared research manuscript and publication contract for section 2.1."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/vmap/fig-2-1-2_platform-coverage.json').read_text())
EDITION='2026-10-20-vmap-report-year'
PDF_NAME='GOSD-2026-section-2-1.pdf'
TITLE='全球开源活跃地图（V-Map）'
QUESTION='全球开源的活跃力量在哪里，如何让参与基础转化为长期共同建设的能力？'
POSITION='本节对应 OSDGs 的 X1“人才规模与多样性”、1.1“规模与密度”，主用指标方向为活跃开发者规模（DevScale），衔接 SDG 8、SDG 9。开发者总量用于观察参与基础，活跃规模用于观察统计期内的参与；二者均不能单独代表贡献质量或公共价值。'
FINDING='全球开源参与基础持续扩大，欧洲、美国、中国、印度及全球南方代表国家共同构成多中心格局。平台覆盖影响我们对规模的观察；中国的区域结构则呈现头部集聚与多节点支撑并存的特点。'
SNAPSHOT_NOTE='除特别说明外，本报告统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日。历史图中的年份指报告年度，均为前一年 7 月至当年 6 月。'
STORIES=[
('2.1.1 全球参与：让已有力量更可见',[
 '本报告期，GitHub 全球开发者总量约 1.94 亿，活跃开发者约 2,890.36 万。图 2-1-1 同时呈现世界分布、两类排名和五年趋势。英国的开发者总量高于德国，活跃规模却低于德国，说明参与基础与当期参与是两个不同侧面。',
 '从 2022 至 2026 报告年度，全球开发者总量从约 8,367 万增至约 1.94 亿，活跃规模从约 1,543 万增至约 2,890 万。规模持续扩大，为共同建设提供了更广泛的基础；其能否转化为持续贡献，需要在后续地图中检验。',
 '印度、巴西、印度尼西亚的活跃规模分别为 285.08 万、193.45 万和 48.66 万，合计约 527 万，占全球活跃规模约 18.2%。这些代表性样本说明，全球南方已有广泛的参与基础。国际合作应让本地社区与维护者参与议题提出、技术决策和长期维护。']),
('2.1.2 五域比较：看规模、演变与平台覆盖',[
 '图 2-1-2 依据报告编制组的五域统计，将美国、欧洲、中国、印度和全球南方代表组并列。开发者总量分别约为 3,030 万、3,015 万、2,919 万、2,458 万和 2,033 万。五域是观察框架，不构成全球的穷尽划分。',
 '五年活跃序列中，欧洲由约 370 万增至 675 万，持续保持领先；美国由约 252 万增至 465 万，中国由约 238 万增至 455 万。印度与全球南方代表组分别由约 126 万、135 万增至 272 万、300 万，呈现不断扩大的参与基础。',
 '平台覆盖同样影响对中国规模的观察：GitHub 报告年度活跃规模为 250.48 万，国内平台补充约 120 万，扩展后约为 370 万。补充量由报告编制组根据 Gitee、AtomGit 等官方平台数据，结合问卷调研去重得到。该平台比较与五域综合统计分别呈现，国内补充量不再叠加到五域中国值中。']),
('2.1.3 中国实例：让区域节点连接长期合作',[
 '图 2-1-3 将中国 34 个省级地区的分布、双榜、全国趋势与区域份额集中呈现。北京、上海、广东合计约 132 万活跃开发者，占全国约 52.6%；第 4—10 位地区约占 36.0%，其余 24 地约占 11.5%。',
 '从 2022 至 2026 报告年度，中国在 GitHub 上的活跃规模从约 129 万增至约 250 万。头部集聚与多点支撑并存，区域合作可围绕真实项目连接高校、企业与社区，拓展持续参与和共同维护的机会。'])]
STRATEGIES=[
('将实际参与纳入长期监测',[
 '国际组织、政府与公共资助方可持续观察活跃规模、地域分布和长期变化，优先补齐覆盖不足地区的观测与参与支持。沿用统一报告年度、有效行为与去重规则，结合国际和国内平台完善参与画像。',
 '将规模观察与后续贡献、维护和公共服务采用相连接，使教育、社区和基础设施投入具有可追踪的反馈。']),
('让全球南方成为长期共建伙伴',[
 '让本地需求、社区经验和维护者意见进入议题设置与治理过程。支持围绕共同需求的长期项目、双向交流、多语种文档及本地维护者成长。',
 '以持续贡献、共同维护、当地采用和受益证据评价合作，避免仅以参与人数衡量效果。']),
('以区域节点拓展持续参与机会',[
 '以中国区域结构为实例，围绕真实需求和可持续维护条件，探索区域节点连接高校、企业与社区的合作方式；其他国家可结合自己的城市和教育网络开展实践。',
 '为资源较少地区提供远程参与和共同维护入口，重点观察更多地区能否持续参与、合作能否延续，以及本地需求是否得到回应。'])]
INDICATOR_FEEDBACK='DevScale 是主用指标方向。总量是背景变量，地域份额和集中度是派生分析；活跃增量不等于首次贡献者人数。本节未计算新人增长、人口密度或跨地域协作比例。'
GAPS=[
 '地图与国家榜采用 OpenDigger / OpenShare 的 GitHub 报告年度底表；五域规模和历史序列采用编制组确认的原稿统计。不同平台覆盖的统计分别展示。',
 '国内约 120 万为编制组确认的去重补充量，仅用于平台覆盖比较，不分摊到省级地区，也不重复叠加到五域综合统计。']
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
 out=['# 2.1 '+TITLE,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING,SNAPSHOT_NOTE]
 for (title,paras),fig in zip(STORIES,FIGURES.values()):
  out+=['## '+title,*paras,'图 '+fig['id']+' '+fig['title']]
 out+=['## 2.1.4 行动建议']
 for title,paras in STRATEGIES:out+=['### '+title,*paras]
 out+=['## 指标与证据说明',INDICATOR_FEEDBACK,*GAPS]
 return '\n\n'.join(out)+'\n'

def specification():
 specs=[]
 for i,(key,f) in enumerate(FIGURES.items()):
  specs.append(dict(figure='图 '+f['id'],question=STORIES[i][0],claim=STORIES[i][1][0],data_scope=f['status'],web_default=['世界活跃地图＋双榜＋同源趋势','编制组五域规模；2026报告年度','中国活跃地图＋双榜＋全国趋势'][i],print_panels=[['A 世界地图与双榜','B 总量和活跃五年趋势'],['A 当前五域双指标','B 五域五年演变','C 国内平台补充比较'],['A 省级活跃地图','B 全国活跃趋势','总量和活跃前十','C 区域份额']][i],exploration_only=['地区详情、总量着色、中国下钻','国家前十、起点指数、年份与组别聚焦','所选省级详情、总量着色、缩放'][i],design_status='pilot_for_review',evidence_status=['report_year_source','author_confirmed_five_groups_and_domestic','report_year_provincial_source'][i],simulated=False,source='fig-2-1-2_platform-coverage.json',assets=f['files']))
 return specs
