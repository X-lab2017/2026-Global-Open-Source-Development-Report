"""P-Ranking manuscript shared by the Web and publication PDF."""
from html import escape as E
from goso_reading import Tree,fragment,remove

EDITION='2026-10-21-p-ranking-publication-v2'
TITLE='全球开源项目影响力排行榜（P-Ranking）'
INTRO='开源项目承载开发者、企业与基金会的共同投入。本节从项目影响力、技术领域和协作来源出发，为确定持续维护的重点提供线索。'
QUESTION='哪些项目具有较高的协作影响力，它们分布在哪些领域，维护支持应如何落实？'
POSITION='OpenRank 衡量协作影响力，活跃开发者反映参与规模，对应 OSDGs 的共同创造与可持续视角。项目沿用原表归并，不与单个仓库混排。'
FINDING='OpenHarmony 位居全球项目榜首，PyTorch、vLLM 等 AI 基础软件位居前列；影响力名次与开发者规模并不一致。'
FIGURES=['项目影响力与参与规模','项目样本分布与两期位次变化','头部项目贡献来源与组织结构（模拟）']
STORIES=[
 ('3.4.1 项目格局：影响力与参与规模',[
  '图 3-4-1 并列呈现项目的 OpenRank 与活跃开发者。全球详细榜含 30 项，OpenHarmony、Azure 分列前两位，PyTorch、vLLM 分列第 4、第 7；中国项目另设独立 Top 30 分榜。',
  '参与人数与影响力需要结合阅读。VSCode 有 24,897 名活跃开发者，多于 OpenHarmony 的 12,640 人，OpenRank 名次却低于后者。人数不能替代协作网络中的影响力，也不宜用两项指标的比值评价项目效率。',
  '比较项目，先确认仓库范围。Azure、C#/.Net 等聚合条目与具体软件项目并存，纳入仓库及其重叠关系仍需核对，不能直接加总分值或人数。榜外模拟补位仅用于展示，不纳入研究结论。']),
 ('3.4.2 样本结构：国家、领域与位次',[
  '图 3-4-2 从国家标签、技术领域和两期名次三个角度观察样本。独立 Top 100 国家汇总中，美国标签项目 69 个、中国 7 个，未识别 9 个；全球详细 Top 30 中，AI 与机器学习为 8 项，编程语言与运行时为 5 项。两组分布分别计算。',
  '项目标签描述归属，贡献记录说明协作来源。原表组织字段包含公司、基金会与托管方，不能一律解释为历史发起者；国家标签也不代表贡献者所在地或治理权。领域分类仅描述入榜样本，不代表全球技术规模。',
  '名次上升提示关注，具体变化仍需复核。中国项目两期记录中，Ascend 从第 151 位升至第 4 位，CANN 与 AgentScope 标为“新进”。基期日期尚未明确，无法据此判断变化速度；“新进”也不等于技术首次出现。']),
 ('3.4.3 贡献结构：从项目标签到协作来源',[
  '图 3-4-3 借用全球原榜前十的项目名称，演示如何从各地合并 PR 份额追溯组织与仓库组。全部贡献数量与分组均为模拟，用于说明分析方法，不作为这些项目的实测发现。',
  '国家与组织是同一批贡献的两个观察维度。OpenHarmony 的模拟示例含 16,000 条合并 PR，中国来源占 65%；按组织归属，又可分为企业、社区机构、独立贡献者与未知项。两种分布分母相同，份额不能相加。',
  '保留未知项，才能看清证据覆盖范围。示例将“其他已识别”与“未识别”分开，也将已声明的独立贡献者与组织未知项分开。贡献份额不能直接证明治理控制权；判断维护责任还需结合维护者分工与治理规则。'])]
ACTION_TITLE='3.4.4 行动建议：围绕具体项目组织持续维护'
ACTION_INTRO='将项目榜作为选择维护对象的起点，再核实实际依赖、维护缺口与责任安排。'
ACTIONS=[
 ('项目维护团队：明确范围与接续责任','维护项目、仓库和版本的对应清单，记录迁移与归并；为关键模块明确维护人及接续安排。定期检查问题响应时间、贡献接纳情况和关键模块是否有人持续维护。'),
 ('企业与基金会：围绕共同依赖分担任务','识别产品与服务依赖的开源项目，与维护者约定测试、文档、安全响应等任务和支持周期。定期核对任务交付、上游接纳及跨组织维护人员的持续参与。'),
 ('公共部门与资助方：支持可验证的公共维护','结合公共服务依赖和维护缺口选择支持对象，明确责任团队、交付成果与复核时间。按期检查成果是否进入上游、资助期后维护是否延续，避免仅按一次排名配置资源。')]
BRIDGE='项目榜呈现已有的协作积累；下一节转向新仓库与新项目，观察新的技术供给如何形成。'
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
