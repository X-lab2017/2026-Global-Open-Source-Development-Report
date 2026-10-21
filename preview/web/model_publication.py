"""M-Ranking manuscript shared by Web and print; month and account boundaries preserved."""
from html import escape as E
from goso_reading import Tree,fragment,remove

EDITION='2026-10-21-m-ranking-publication-v1'
TITLE='全球开源模型影响力排行榜（M-Ranking）'
INTRO='模型可以被微调、改编或作为其他模型的基础，复用关系由此形成网络。本节从模型版本出发，观察复用影响力、任务分布与发布账户，为选择研究对象、应用试点和维护支持提供线索。'
QUESTION='哪些模型版本在复用网络中具有较高影响力，不同任务由哪些发布账户提供？'
POSITION='以 ModelRank 观察模型复用网络影响力，对应 OSDGs 的共同创造视角。本节采用 2026 年 8 月快照；分值不代表能力测试成绩，入榜也不等于开放程度认定。'
FINDING='Top 100 中，文本生成与多模态理解合计占 79 个版本；Qwen 与 google 两个发布账户合计占 56 个。头部集中之外，榜单还覆盖机器人、图像、语音等任务。'
FIGURES=['模型复用影响力与附加指标（2026 年 8 月）','入榜模型的任务分布与供给覆盖（2026 年 8 月）','发布账户的入榜数量与任务布局（2026 年 8 月）']
STORIES=[
 ('3.6.1 模型版本：从复用影响识别关键对象',[
  'Qwen/Qwen3.8-27B 以 ModelRank 27,930.09 位居首位，Qwen/Qwen3.5-9B-Base 与 meta-llama/Llama-3.1-8B 随后，分别为 14,343.72 和 14,144.49。图 3-6-1 保留具体版本，结合衍生模型数与下载量，提供进一步了解复用情况的入口。',
  '复用影响与应用适配需要分别判断。同一系列的基础版、指令版和不同参数版本各有记录，不能将其合并为一个模型或相加得到系列能力。选定候选版本后，还需围绕实际任务验证效果、部署成本与维护条件。',
  '下载和衍生数量提供辅助线索。这些数值来自该月记录，详细统计窗口与去重规则仍待补充，不能解释为当月新增或独立使用人数。已核对的 20 份模型卡反映 2026 年 10 月 17 日状态，许可与权重访问条件也应按具体版本阅读。']),
 ('3.6.2 任务分布：从头部位置走向供给覆盖',[
  'Top 100 中，文本生成有 52 个版本，多模态理解 27 个；前 20 名中，两类分别有 11 个和 7 个。图 3-6-2 将任务数量与发布账户覆盖并列，既看主要方向，也看不同任务的供给来源。',
  '较少入榜的任务仍有值得跟踪的对象。机器人与图像生成各有 1 个版本进入前 20，完整 Top 100 还包括全模态生成、语音识别等类别。数量描述的是这份榜单的构成，不能据此评价任务的重要性或市场规模。',
  '供给覆盖需要结合具体版本理解。一个账户可以提供多类任务，同一版本则按榜单主任务归入一类；3 个任务未识别的版本保留在分母中。任务与账户交叉表有助于寻找替代供给，但不能直接证明模型可替换或组织之间存在合作。']),
 ('3.6.3 发布账户：识别供给来源与集中程度',[
  'Qwen 有 41 个版本入榜，google 有 15 个，meta-llama 与 unsloth 各有 6 个。前 20 名则来自 Qwen、meta-llama、lerobot 和 krea 四个账户。图 3-6-3 将入榜数量与任务布局结合，帮助区分供给广度和头部位置。',
  '账户数量榜保留平台上的发布边界。100 个版本来自 23 个已识别账户，另有 1 个版本的账户未识别。Qwen 与 Tongyi-MAI、meta-llama 与 FacebookAI 等分别统计，不自动并入母公司；多个版本也不等于多个独立模型家族。',
  '集中程度提示需要继续核查的依赖。采购方和公共平台可从入榜账户进入具体模型，核查维护主体、上游依赖和替代方案。账户入榜数量与分值中位数各有用途，不合成为组织影响力总分，也不替代对维护承诺和使用条件的审查。'])]
ACTION_TITLE='3.6.4 行动建议：把复用影响转化为可靠供给'
ACTION_INTRO='以具体版本和使用场景组织试点，让支持落到可核查的维护与复用记录上。'
ACTIONS=[
 ('模型团队：让版本与上游关系可追踪','完善模型卡、许可证、权重访问条件、版本变更和上游声明，提供可复现的使用示例。持续观察问题响应、下游反馈与兼容性修复，明确停止维护或替换版本的安排。'),
 ('企业与公共平台：围绕实际任务验证候选模型','为同一任务选择可比较的版本，记录效果、成本、部署约束与依赖，保留替代方案。按约定周期复测关键任务，检查版本更新是否带来回归，并将修复反馈给上游团队。'),
 ('公共部门与资助方：支持公共复用条件','围绕公共需求支持评测、文档、适配与维护，明确负责团队、交付记录和复核时间。观察成果是否被外部采用、问题是否得到处理及资助结束后的维护延续，不以入榜数量替代成效评价。')]
BRIDGE='本章从地区、组织、项目到模型识别了具体的协作主体与成果。下一章转向技术领域，进一步理解这些力量在不同方向上的分布。'
NOTES=[
 '3.6 采用 2026-08 模型月榜快照，例外于报告年度。Top 100 的前 20 名保留原报告高精度值，21—100 使用公开 API 原精度；不改动原榜次，不恢复已撤掉的月度历史排名图。ModelRank 表示复用网络影响力，不等于能力测试成绩或开放程度认定。',
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
