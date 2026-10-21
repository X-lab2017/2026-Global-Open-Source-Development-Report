"""M-Ranking manuscript shared by Web and print; month and account boundaries preserved."""
from html import escape as E
from goso_reading import Tree,fragment,remove

EDITION='2026-10-21-m-ranking-publication-v2'
TITLE='全球开源模型影响力排行榜（M-Ranking）'
INTRO='模型经微调、改编后，可以成为后续开发的基础。沿着这些复用关系观察具体版本，再结合任务与发布账户，有助于选择值得研究、试用和持续维护的对象。'
QUESTION='哪些模型版本在复用网络中具有较高影响力，不同任务由哪些发布账户提供？'
POSITION='ModelRank 衡量复用网络影响力，对应 OSDGs 的共同创造视角；本节采用 2026 年 8 月快照。模型能力与开放条件需另行核查。'
FINDING='Top 100 中，文本生成与多模态理解合计占 79 个版本；Qwen 与 google 两个发布账户合计占 56 个。头部集中之外，榜单还覆盖机器人、图像、语音等任务。'
FIGURES=['模型影响力、衍生数与下载量（2026 年 8 月）','入榜模型的任务分布与供给覆盖（2026 年 8 月）','发布账户的入榜数量与任务布局（2026 年 8 月）']
STORIES=[
 ('3.6.1 模型版本：识别重要的复用基础',[
  'Qwen/Qwen3.8-27B 以 ModelRank 27,930.09 位居首位，Qwen/Qwen3.5-9B-Base 与 meta-llama/Llama-3.1-8B 随后。图 3-6-1 将影响力与衍生、下载记录并列，提供深入了解这些版本的线索。',
  '同一系列的不同版本，需要分别选择。基础版、指令版和不同参数版本的用途与部署条件可能不同，不能相加得到系列能力。ModelRank 帮助识别复用影响，实际选型仍需验证任务效果、部署成本与维护条件。',
  '复用记录与模型卡补充不同信息。下载量和衍生数来自月记录，统计窗口与去重规则待补，不能当作当月新增或独立用户。20 份已核对模型卡反映 2026 年 10 月 17 日状态，用于了解版本、许可及权重访问条件，不替代 8 月榜单。']),
 ('3.6.2 任务分布：理解方向与供给覆盖',[
  'Top 100 中，文本生成有 52 个版本，多模态理解 27 个；前 20 名中，两类分别有 11 个和 7 个。图 3-6-2 进一步展开各任务的发布账户，帮助从总体分布进入具体供给。',
  '数量较少的任务也有头部复用对象。机器人与图像生成各有 1 个版本进入前 20，Top 100 还涵盖全模态生成、语音识别等方向。面向专门需求选择模型时，这些对象同样值得核查；入榜数量不代表任务的重要性或市场规模。',
  '同一任务可以沿不同账户寻找候选版本。交叉表按每个版本的一个主任务计数，3 个任务未识别的版本保留在分母中。它提供比较入口，模型能否替换仍需任务评测；同列或同行也不表示账户之间存在合作。']),
 ('3.6.3 发布账户：区分供给广度与头部位置',[
  'Qwen 有 41 个版本入榜，google 有 15 个，meta-llama 与 unsloth 各有 6 个。图 3-6-3 同时列出前 20 名数量与任务覆盖，帮助区分账户的入榜广度和头部位置。',
  '发布账户是识别供给来源的起点。100 个版本来自 23 个已识别账户，另有 1 个版本的账户未识别。同一组织的不同账户分别统计，不自动并入母公司；账户下的多个版本也不等于多个独立模型家族。',
  '入榜广度与头部位置并不一致。google 的 15 个版本均在第 21—100 位；lerobot 与 krea 各有 2 个版本入榜，其中各有 1 个进入前 20。选择合作对象时，应结合具体任务和维护安排，不把数量或分值中位数合成为组织影响力总分。'])]
ACTION_TITLE='3.6.4 行动建议：把复用影响转化为可靠供给'
ACTION_INTRO='围绕具体版本和使用场景开展试点，并保留可复核的维护与复用记录。'
ACTIONS=[
 ('模型团队：让版本与上游关系可追踪','完善模型卡、许可与权重访问条件、版本变更及上游声明，提供可复现的示例。按期检查问题响应和下游兼容性反馈，明确停止维护、迁移或替换版本的安排。'),
 ('企业与公共平台：围绕实际任务验证候选模型','为同一任务选择候选版本，记录效果、成本、部署约束与依赖，保留替代方案。按期复测关键任务，检查更新后的效果和兼容性，并向上游反馈问题与修复。'),
 ('公共部门与资助方：支持公共复用条件','围绕公共需求支持评测、文档、适配与维护，约定负责团队、成果和复核时间。检查外部采用、问题处理及资助结束后的维护情况，以可复用成果和持续支持观察成效。')]
BRIDGE='从地区到模型，本章识别了一组可继续核查的合作与维护对象。将榜单转化为行动，需要结合实际依赖，明确负责团队、支持任务与复核时间。下一章转向技术领域，进一步观察这些力量如何组织成生态。'
NOTES=[
 '3.6 采用 2026-08 模型月榜快照，例外于报告年度。Top 100 的前 20 名保留原报告高精度值，21—100 使用公开 API 原精度；筛选与排序保留原榜次。ModelRank 表示复用网络影响力，不等于能力测试成绩或开放程度认定。',
 '3.6 衍生模型数与下载量来自对应月记录，详细时间窗、去重和衍生计数规则尚待补充，不能称为当月新增或独立使用人数。模型卡仅核对原报告 20 个版本，核验日 2026-10-17；其余待核验不补零。国家标签同样只保留原报告 20 条，不能外推 Top 100 国家分布。',
 '图 3-6-2 每个版本使用一个 API 主任务；Top 100 有 8 个已识别任务类别及 3 个任务未识别的版本，未知保留分母。发布账户数在每个任务内部去重，跨任务不能相加。覆盖图前 8 个账户独立显示，剩余账户与未识别账户汇总显示，全部单元格合计 100；切换前 20 时分母相应为 20。',
 '图 3-6-3 按平台发布账户分别统计，23 个已识别账户加 1 个未识别类别，不自动合并母公司账号。任务和账户数量相同者并列、后续名次跳位，未知不参与数量排名。分值中位数仅描述入榜版本，不合计 ModelRank 为组织总影响力；数量占比不代表市场份额。官方身份和标识核验日为 2026-10-17。']

def paragraphs():
 return [INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING]+[t for _,ps in STORIES for t in ps]+[ACTION_INTRO]+[t for _,t in ACTIONS]+[BRIDGE]

def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('6',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('mp-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.add('mp-stage');stage.set('data-slide-height',760 if i==2 else 880);stage.set('data-reflow-minimum-width','700')
 board=next(n for n in root.walk() if n.has('cr-board'))
 for n in list(root.walk()):
  if n.has('cr-eyebrow') or n.tag=='figcaption':remove(root,n)
  if n.has('cr-head-right'):n.children=fragment('<span></span>')
  if n.attrs.get('data-rr-action') in ('source','image','export'):remove(root,n)
  if n.has('cr-foot'):n.add('rp-foot')
 board.children+=fragment(f'<div class="rp-caption">图 3-6-{i} {E(FIGURES[i-1])}</div>')
 root.children+=fragment(f'<figcaption class="rp-sr-caption">图 3-6-{i} {E(FIGURES[i-1])}</figcaption>')
 return tree.root.html()

def section(data):
 from region_publication import para,interpretation
 out=['<section class="chapter-section gosr-section cr-section rr-section rp-section mp-section" id="ch03-s06">','<div class="section-topline"><span>3.6 / M-RANKING</span></div>',f'<h2>3.6 {TITLE}</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'rp-position'),para('核心发现：'+FINDING)]
 for i,(title,ps) in enumerate(STORIES,1):out += [f'<h3>{E(title)}</h3>',para(ps[0]),figure(i,data)]+[interpretation(t) for t in ps[1:]]
 out += [f'<h3 id="rr-6-actions">{ACTION_TITLE}</h3>',para(ACTION_INTRO)]
 for title,t in ACTIONS:out += [f'<h4 class="rp-action-title">{E(title)}</h4>',para(t)]
 return ''.join(out+[para(BRIDGE),'</section>'])

def manuscript():
 out=['# 3.6 '+TITLE,*paragraphs()[:4]]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-6-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
