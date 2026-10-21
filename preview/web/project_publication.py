"""P-Ranking manuscript shared by the Web and publication PDF."""
from html import escape as E
from goso_reading import Tree,fragment,remove

EDITION='2026-10-21-p-ranking-publication-v1'
TITLE='全球开源项目影响力排行榜（P-Ranking）'
INTRO='项目将开发者、企业与基金会的投入转化为可持续使用的成果。项目榜从具体协作对象出发，连接影响力、技术领域与贡献来源，为识别共同维护的重点提供线索。'
QUESTION='哪些项目形成较高的协作影响力，它们分布在哪些领域，怎样进一步理解其维护基础？'
POSITION='以 OpenRank 观察协作影响力，以活跃开发者补充参与规模，对应 OSDGs 的共同创造与可持续视角。沿用原表项目归并，不与单个仓库混排。'
FINDING='OpenHarmony 位居全球项目榜首，PyTorch、vLLM 等 AI 基础软件进入前列。原表国家标签、技术领域和贡献来源回答不同问题，需要分别阅读。'
FIGURES=['项目影响力与参与规模','项目样本分布与两期位次变化','头部项目贡献来源与组织结构（模拟）']
STORIES=[
 ('3.4.1 项目格局：从头部位置理解协作对象',[
  '全球详细榜保留 30 个项目，OpenHarmony 的 OpenRank 为 75,809.42，Azure 为 29,382.06；PyTorch、vLLM 分列第 4、第 7。图 3-4-1 并列呈现影响力与活跃开发者，中国项目另设 Top 30 分榜。',
  '影响力与参与规模提供互补线索。例如，VSCode 的活跃开发者为 24,897 人，高于 OpenHarmony 的 12,640 人，但 OpenRank 排序不同。人数并不直接决定协作网络中的位置，也不宜据此计算项目效率。',
  '项目名称背后可能是不同范围的仓库集合。Azure、C#/.Net 等聚合条目与具体软件项目并存，进一步比较须核对纳入仓库及其重叠关系。主榜默认展示真实前 30 名；第 31—100 位模拟补位仅在明确标注后查看，不用于研究结论。']),
 ('3.4.2 样本结构：分别观察归属、领域与位次',[
  '独立的 Top 100 国家汇总中，美国标签项目 69 个、中国 7 个，另有 9 个未识别。全球详细 Top 30 的编辑分类中，AI 与机器学习为 8 项，编程语言与运行时为 5 项。图 3-4-2 分别展示这两种样本结构，并保留中国项目两期名次。',
  '国家标签不等于贡献来源。原表组织字段包含公司、基金会与托管方，不能一律解释为历史发起者；国家汇总也不代表贡献者所在地或治理权。领域数量仅描述所选样本，不能外推为全球技术规模。',
  '位次变化提供复核线索。中国项目记录中，Ascend 从第 151 位到第 4 位，CANN 与 AgentScope 标为“新进”。由于基期日期未提供，本节不生成月度轨迹或增长率，也不把“新进”解释为技术首次出现。']),
 ('3.4.3 贡献结构：把项目标签与协作来源分开',[
  '图 3-4-3 以全球原榜前十的项目名称演示贡献分析：先看各地合并 PR 的份额，再展开组织与仓库组。全部贡献数量、国家分布及组织和仓库分组均为模拟，只用于说明分析方式。',
  '同一份贡献记录可以从不同侧面阅读。以 OpenHarmony 的模拟示例为例，16,000 条合并 PR 中，中国来源占 65%；组织维度则区分企业、社区机构、独立贡献者与未知归属。两种分布使用同一分母，不能再相加。',
  '未知来源应留在分母中。示例将“其他已识别”与“未识别”分开，已声明的独立贡献者也不并入组织未知项。贡献份额即使较高，也不能直接证明治理控制权；真实维护责任仍需结合维护者和项目治理证据。'])]
ACTION_TITLE='3.4.4 行动建议：围绕具体项目组织持续维护'
ACTION_INTRO='把榜单中的项目转化为可核验、可持续支持的维护对象。'
ACTIONS=[
 ('项目维护团队：明确范围与接续责任','维护项目、仓库和版本的对应清单，记录迁移与归并变化；为关键模块明确维护人和接续安排。按期检查问题响应、贡献接纳及维护人员是否持续参与。'),
 ('企业与基金会：围绕共同依赖分担任务','识别产品与服务依赖的开源项目，与维护者约定测试、文档、安全响应等具体任务和支持周期。复核任务完成、上游接纳及跨组织维护者参与情况。'),
 ('公共部门与资助方：支持可验证的公共维护','结合公共服务依赖和维护缺口选择支持对象，明确交付成果、责任团队与复核时间。跟踪成果是否进入上游、维护是否延续，避免仅按一次排名配置资源。')]
BRIDGE='成熟项目展示已有协作积累；下一节转向新仓库与新项目，观察新的技术供给如何形成。'
NOTES=[
 '3.4 全球与中国详细榜各有 30 个项目，主榜默认真实记录；第 31—100 位的全球补位名次、OpenRank 与开发者数均为模拟。原始国家 Top 100 汇总独立提供，12 个已识别国家共 91 项、未识别 9 项，不能从模拟名单回算。',
 '3.4 项目是原表归并对象，包含项目生态与项目集合；仓库清单和重叠边界仍待核验，不能跨项目加总分值或人数。国家与组织字段保留原表标签，不一律解释为历史发起地或发起者。领域为依据官方介绍的编辑分类，资料核对日期为 2026-10-17，不替代报告期映射。',
 '图 3-4-2 的两期记录基期日期待确认，“新进”不折算位移，不生成增长率。各表保留原始精度，例如 CANN 两期表为 14,719.50，主榜为 14,719.47。',
 '图 3-4-3 仅项目名称与原榜次来自真实记录；全部贡献数量、国家份额、匿名组织和仓库分组均为模拟。合并 PR 唯一归入国家、组织、仓库组，国家为贡献者所在地，非国籍。未识别保留在分母；匿名组织仅在各项目内定义，不能跨项目合并，也不推断治理权。']

def paragraphs():
 return [INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING]+[t for _,ps in STORIES for t in ps]+[ACTION_INTRO]+[t for _,t in ACTIONS]+[BRIDGE]

def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('4',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('pp-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.add('pp-stage');stage.set('data-slide-height',{1:880,2:820,3:820}[i]);stage.set('data-reflow-minimum-width','700')
 board=next(n for n in root.walk() if n.has('cr-board'))
 for n in list(root.walk()):
  if n.has('cr-eyebrow') or n.tag=='figcaption':remove(root,n)
  if n.has('cr-head-right'):n.children=fragment('<span></span>')
  if n.attrs.get('data-rr-action') in ('source','image','export'):remove(root,n)
  if n.has('cr-foot'):n.add('rp-foot')
 board.children+=fragment(f'<div class="rp-caption">图 3-4-{i} {E(FIGURES[i-1])}</div>')
 root.children+=fragment(f'<figcaption class="rp-sr-caption">图 3-4-{i} {E(FIGURES[i-1])}</figcaption>')
 return tree.root.html()

def section(data):
 from region_publication import para,interpretation
 out=['<section class="chapter-section gosr-section cr-section rr-section rp-section pp-section" id="ch03-s04">','<div class="section-topline"><span>3.4 / P-RANKING</span></div>',f'<h2>3.4 {TITLE}</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'rp-position'),para('核心发现：'+FINDING)]
 for i,(title,ps) in enumerate(STORIES,1):
  out += [f'<h3>{E(title)}</h3>',para(ps[0]),figure(i,data)]+[interpretation(t) for t in ps[1:]]
 out += [f'<h3 id="rr-4-actions">{ACTION_TITLE}</h3>',para(ACTION_INTRO)]
 for title,t in ACTIONS:out += [f'<h4 class="rp-action-title">{E(title)}</h4>',para(t)]
 return ''.join(out+[para(BRIDGE),'</section>'])

def manuscript():
 out=['# 3.4 '+TITLE,*paragraphs()[:4]]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-4-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
