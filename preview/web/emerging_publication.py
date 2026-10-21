"""E-Ranking manuscript shared by Web and print; original samples stay independent."""
from html import escape as E
from goso_reading import Tree,fragment,remove

EDITION='2026-10-21-e-ranking-publication-v1'
TITLE='全球新势力开源仓库与项目排行榜（E-Ranking）'
INTRO='新建仓库既可能承载新的协作尝试，也可能是既有项目的扩展或迁移。本节分别观察仓库与项目，寻找值得持续跟踪和支持的新生力量。'
QUESTION='哪些新建对象形成了协作影响，它们提供什么技术，如何从初期参与走向持续维护？'
POSITION='以 OpenRank 观察协作影响力，结合活跃开发者、创建时间与仓库范围，对应 OSDGs 的共同创造与可持续视角。仓库与项目分别排名。'
FINDING='新仓库样本以 AI 基础软件为主；新项目样本的编辑分类则更多落在智能体工具。两类榜单呈现不同层级的技术供给。'
FIGURES=['新仓库影响力与创建时间','新项目影响力与仓库关联','新势力样本的技术结构与创建批次']
STORIES=[
 ('3.5.1 新仓库：从创建记录观察协作起点',[
  '新仓库 Top 30 中，openclaw/openclaw 以 OpenRank 7,047.46 居首，活跃开发者为 18,624 人；cann/ops-transformer、cann/ops-nn 分列第二、第三。图 3-5-1 将影响力、参与规模与创建日期放在一起，保留完整仓库路径和平台。',
  '仓库新建，不等于技术从零开始。原表日期可能受到迁移、镜像或分叉影响；既有项目的新组件也可进入仓库榜。因此，榜单适合识别新的协作入口，判断技术原创性还需核对版本沿革与首次公开记录。',
  '创建时间决定可观察窗口的长短。榜首仓库原表创建于 2025 年 11 月 24 日，至报告期末为 219 天；这段窗口不等于持续活跃时长，也不能用累计 OpenRank 除以天数来评价增长速度。后续应跟踪贡献是否延续、外部参与者是否留下。']),
 ('3.5.2 新项目：把多仓库供给与维护责任连起来',[
  '新项目榜按原稿定义，要求纳入的仓库均在本期新建；名单与资格沿用原表。CANN 居首，OpenRank 为 14,719.47，纳入 68 个仓库；Hermes Agent、DeepAgents 随后，原表各纳入 1 个仓库。图 3-5-2 分别呈现项目指标与已有证据支持的仓库关联。',
  '关联仓库帮助理解项目，不能替代完整纳入清单。新仓库 Top 30 中有 8 个对象已核对与 CANN 的官方关系；它们只是当前入榜样本中的关联对象，不能代表全部 68 个仓库，也不能将所有 Ascend 命名空间仓库自动并入。',
  '项目范围明确后，才能讨论协作成效。项目分值与开发者数量保留原表记录，不由所展示的仓库行相加。Hive 的两榜数值存在差异，其本期映射仍待核验；进一步判断新项目资格和维护能力，需要完整仓库清单、创建记录与维护者分工。']),
 ('3.5.3 样本结构：技术方向、语言与创建批次',[
  '图 3-5-3 的原表领域汇总中，AI 基础软件占新仓库 Top 30 的 18 项，智能体与 Agent 工具占 4 项。按逐项编辑分类，新项目 Top 30 中有 25 项属于智能体工具。仓库与项目各有独立分母，不能将组件数量直接解释为独立项目数量。',
  '语言与领域回答不同问题。原表主要语言中，Python 为 15 个仓库、C++ 为 12 个，合计占样本的 90%；这描述实现语言，不代表技术价值或全球语言份额。原表领域汇总与编辑分类也分别保留，例如赏金挑战仓库在编辑分类中归入开发者服务。',
  '创建批次回看的是本期入榜名单。新仓库样本有 9 项创建于 2025 年 9 月；新项目的首仓记录在 2025 年 8 月和 2026 年 2 月各有 7 项。图中的空月只表示这份名单没有对应创建记录，不能据此推断整个生态的热度、增速或技术兴衰。'])]
ACTION_TITLE='3.5.4 行动建议：支持新生力量形成持续维护'
ACTION_INTRO='将初期榜单作为观察起点，把支持落实到可追踪的维护任务。'
ACTIONS=[
 ('项目团队：补齐身份与维护记录','公布仓库范围、迁移沿革、版本记录和关键模块负责人，提供清晰的贡献入口。按月观察外部贡献接纳、问题响应时间与维护者持续参与，识别只有发布、缺少后续维护的环节。'),
 ('企业与基金会：把试用转化为上游协作','围绕实际需求开展适配、测试和文档工作，与维护者约定任务及支持周期。检查试用反馈是否形成上游修复、任务是否有人接续，再决定扩大投入。'),
 ('公共部门与资助方：分阶段检验支持效果','按公共需求和维护缺口选择试点，明确阶段成果、责任团队及复核时间。跟踪可复用版本、外部参与和资助期后的维护延续，不以短期名次或仓库数量替代成效评价。')]
BRIDGE='新生代码项目反映技术供给的形成；下一节转向模型版本，观察模型复用网络中的影响力。'
NOTES=[
 '3.5 仓库与项目各有独立 Top 30。新项目要求纳入仓库全部在报告期内新建，资格和数量沿用原表；完整仓库清单、迁移沿革及创建记录尚待逐项核验。创建日、首个纳入仓库创建日不等于技术诞生或项目成立日。创建至期末天数包含创建日，不代表活跃天数，不计算每日 OpenRank。',
 '3.5 官方关系仅支持身份与关联导航，不能替代本期聚合映射。CANN 原表纳入 68 个仓库，当前新仓库榜中有 8 个官方关联对象；不自动纳入其他 Ascend 仓库。Hive 仓库榜为 OpenRank 769.19、开发者 1,454 人，项目榜为 587.11、434 人，分别保留原值，映射待核验。组织和国家未知保持未知，不补猜。',
 '图 3-5-3 原表领域与语言汇总均以新仓库 30 项为分母；原表领域 OpenRank 合计只描述该表，不能跨对象回算项目分值。编辑分类每项一个主领域，仓库与项目各以 30 项为分母；PlatformNetwork/bounty-challenge 在原表分组与编辑分类中归属不同，不改写原表。官方用途及关联资料核对日期为 2026-10-17，不替代报告期快照。',
 '图 3-5-3 的创建批次与累计创建均回溯本期 Top 30 名单，不是历史月榜。零表示所选样本该月无创建记录，不代表整个生态没有新建对象。主要语言表不覆盖项目层，也没有提供技术领域与语言的逐仓交叉映射。']

def paragraphs():
 return [INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING]+[t for _,ps in STORIES for t in ps]+[ACTION_INTRO]+[t for _,t in ACTIONS]+[BRIDGE]

def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('5',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('ep-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.add('ep-stage');stage.set('data-slide-height',880 if i<3 else 760);stage.set('data-reflow-minimum-width','700')
 board=next(n for n in root.walk() if n.has('cr-board'))
 for n in list(root.walk()):
  if n.has('cr-eyebrow') or n.tag=='figcaption':remove(root,n)
  if n.has('cr-head-right'):n.children=fragment('<span></span>')
  if n.attrs.get('data-rr-action') in ('source','image','export'):remove(root,n)
  if n.has('cr-foot'):n.add('rp-foot')
 board.children+=fragment(f'<div class="rp-caption">图 3-5-{i} {E(FIGURES[i-1])}</div>')
 root.children+=fragment(f'<figcaption class="rp-sr-caption">图 3-5-{i} {E(FIGURES[i-1])}</figcaption>')
 return tree.root.html()

def section(data):
 from region_publication import para,interpretation
 out=['<section class="chapter-section gosr-section cr-section rr-section rp-section ep-section" id="ch03-s05">','<div class="section-topline"><span>3.5 / E-RANKING</span></div>',f'<h2>3.5 {TITLE}</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'rp-position'),para('核心发现：'+FINDING)]
 for i,(title,ps) in enumerate(STORIES,1):out += [f'<h3>{E(title)}</h3>',para(ps[0]),figure(i,data)]+[interpretation(t) for t in ps[1:]]
 out += [f'<h3 id="rr-5-actions">{ACTION_TITLE}</h3>',para(ACTION_INTRO)]
 for title,t in ACTIONS:out += [f'<h4 class="rp-action-title">{E(title)}</h4>',para(t)]
 return ''.join(out+[para(BRIDGE),'</section>'])

def manuscript():
 out=['# 3.5 '+TITLE,*paragraphs()[:4]]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-5-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
