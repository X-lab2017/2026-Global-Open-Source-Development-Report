"""GOSR opening and R-Ranking: one manuscript for Web and PDF."""
from html import escape as E
from goso_reading import Tree, Node, fragment, remove
EDITION='2026-10-21-r-ranking-publication-v2'
CHAPTER_TITLE='第三章 全球开源影响力排行榜（GOSR）'
CHAPTER_QUESTION='开源影响力集中在哪里，哪些主体支撑了持续协作？'
CHAPTER_INTRO='第二章呈现全球开源的分布格局，本章进一步观察具体参与者与成果。从地区寻找协作节点，从企业与基金会了解组织投入，再从项目、新势力与模型观察成果供给。六类榜单共同帮助决策者识别值得深入了解和支持的对象。'
CHAPTER_FINDINGS=[
 ('结合规模理解影响力','开发者人数、仓库数量与网络影响力描述不同侧面。同一主体在这些指标上的排名差异，有助于发现值得继续研究的参与结构。'),
 ('按对象层级展开比较','地区、企业、基金会、项目与模型分别排名；整体与子组织、项目与仓库也保留各自边界，便于识别具体的协作主体。'),
 ('用连续记录观察变化','本期榜单提供当前格局，历史记录用于追踪位置变化。对新仓库和模型版本，还需结合创建时间、复用关系与实际使用，观察其影响能否延续。')]
CHAPTER_TOPICS=[('R','地区','寻找地域协作节点'),('C','企业','观察企业投入与参与结构'),('F','基金会','理解跨组织共建'),('P','项目','识别重要的共同成果'),('E','新势力','观察新仓库与新项目'),('M','模型','了解模型复用影响')]
PERIOD='除特别说明外，统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日；模型榜采用 2026 年 8 月快照。'
TITLE='全球行政区划影响力排行榜（R-Ranking）'
INTRO='地区榜从全球行政区、中国省级行政区和中国城市三个层级，观察开源参与规模与协作影响。将同类地区放在一起比较，可以为地方寻找对标对象、为高校和企业寻找合作伙伴提供起点。'
QUESTION='哪些地区具有较高的开源影响力，参与规模与影响力排名有何差异？'
POSITION='以 OpenRank 观察协作网络影响力，以开发者数量补充参与规模，对应 OSDGs 的规模、多样性与共同创造视角。三个层级分别比较。'
FINDING='开发者数量较多的地区，影响力排名未必更高。全球 Top 100 行政区分布在 32 个国家，既有头部集中，也有广泛分布；中国省市榜则进一步指向可开展合作调研的城市。'
FIGURES=['地区影响力与参与规模排名','全球 Top 100 行政区的国家分布','中国省市影响力联动']
STORIES=[
 ('3.1.1 地区比较：规模与影响力排名并不一致',[
 '加利福尼亚州与英格兰位居全球行政区影响力榜前两位，OpenRank 分别为 50,883.80 和 36,398.10；北京市、上海市分别位列第 14 和第 16。图 3-1-1 将影响力与开发者数量并列，帮助辨识两种排名之间的差异。',
 '参与规模相近，协作影响仍可能不同。卡纳塔克邦的开发者数量为 570.53 万，多于英格兰的 487.08 万，但 OpenRank 位列第 8。这一差异提示我们继续考察项目结构、维护角色与跨地区联系，而非将分值换算为个人贡献效率。',
 '地区对标应从相近的统计层级和产业背景出发。全球榜中的州、省、构成国等行政区粒度不同；选定对象后，还需结合连续记录观察变化，才能判断本期差异是否持续。']),
 ('3.1.2 入榜分布：头部集中与多国分布并存',[
 '全球 Top 100 行政区中，美国占 25 席，印度 12 席，巴西 9 席，德国 8 席，中国 7 席，五国合计 61 席。图 3-1-2 从国家分布观察这些重要地域节点，补充单个地区排名的视角。',
 '头部集中之外，仍有广泛的合作对象。全部入榜行政区分布在 32 个国家，其中 19 国各有 1 个。寻找伙伴时，既可关注拥有多个入榜地区的国家，也可沿特定项目寻找较小的地域节点。',
 '入榜数量反映样本中的地域分布，并非各国 OpenRank 份额。Top 100 国家汇总与 Top 30 详细榜单分别提供分布和数值信息，未入榜也不等于没有开源活动。']),
 ('3.1.3 省市联读：从区域位置走向具体城市',[
 '中国省级榜中，北京、上海居前，广东、台湾、浙江随后；城市榜前五为北京、上海、杭州、深圳和台北。图 3-1-3 将两个层级联动，便于在区域背景下识别具体城市。',
 '一个省级地区可以拥有多个入榜城市。广东对应深圳、广州和珠海，分别位列全国城市榜第 4、第 6 和第 29；浙江对应杭州和宁波，其中杭州位列第 3。省市记录各自统计，城市数值不加总回算省级值。',
 '从城市名单进入项目，才能找到具体合作方向。地方、高校和企业可进一步核查这些城市共同参与的项目、承担的维护职责及跨城市联系，将地域比较转化为可执行的共建任务。'])]
ACTION_TITLE='3.1.4 行动建议：围绕共同项目开展地区协作'
ACTION_INTRO='地区榜帮助选择对标对象，项目与维护需求则决定支持如何落地。'
ACTIONS=[
 ('地方公共部门：持续跟踪同一组对标地区','在同一统计层级内，选择参与规模和产业背景相近的地区，按年度跟踪开发者数量、OpenRank 与重点项目。同步记录统计范围调整，观察变化是否持续。'),
 ('高校与企业：为共同维护任务提供稳定支持','选择本地参与较多的项目，明确共同维护任务、负责团队与支持周期。通过贡献是否被接纳、人员是否持续参与、维护职责是否有人接续，观察支持效果。'),
 ('平台与社区：把跨城市交流转化为持续合作','围绕不同城市共同参与的项目，组织任务协作并记录阶段成果。继续跟踪活动结束后的合作、新加入的持续贡献者，以及尚未解决的维护需求。')]
BRIDGE='地区榜呈现协作发生的空间。下一节转向企业，进一步观察组织投入与参与结构。'
NOTES=[PERIOD,'OpenRank 与开发者数量分别计量，不计算人均效率或合成总分。开发者数量单位为万，不直接解释为活跃开发者。','全球行政区、中国省级与中国城市各有 30 条详细记录；国家分布表覆盖 100 个入榜行政区、32 个国家。数量相同的国家并列，后续名次跳位；“其余国家”为汇总项，不参与排名。','Top 100 国家汇总与 Top 30 详细名单是独立底表，不从 Top 30 推造完整 Top 100 名单。入榜数量不代表国家 OpenRank 份额或生态质量评分。','省级与城市分别保留原榜名次，城市数值不加总回算省级值。台湾省及其城市纳入中国范围。全球行政区粒度不同；地理稳定 ID 和边界版本待补，不据此生成精确行政区地图。','当前 3.1 底表不含历史位次，不能据此计算排名升降或判断政策效果。原始值与缺失状态保持不变，筛选与排序只改变展示。','全章六类主体分别排名，不合成跨对象总榜。OpenRank 不等于治理质量或商业价值；ModelRank 不等于模型能力或开放许可证评级。其他小节中的模拟范围保留各图醒目标识。']
def paragraphs():
 return [CHAPTER_QUESTION,CHAPTER_INTRO,*[t for a in CHAPTER_FINDINGS for t in a],PERIOD,INTRO,QUESTION,POSITION,FINDING,*[p for _,ps in STORIES for p in ps],ACTION_INTRO,*[p for _,p in ACTIONS],BRIDGE]
def para(t,cls=''):return f'<p class="{cls}">{E(t)}</p>'
def interpretation(t):
 head,tail=t.split('。',1)
 return f'<p class="rp-interpretation"><strong>{E(head)}。</strong>{E(tail)}</p>'
def opening():
 out=['<div class="rp-opening" id="gosr-reading-guide">',f'<h2>{E(CHAPTER_QUESTION)}</h2>',para(CHAPTER_INTRO),'<h3>本章主要观察</h3>']
 out += [interpretation(t+'。'+b) for t,b in CHAPTER_FINDINGS]
 out += ['<nav class="rp-topics" aria-label="第三章六类榜单">'+''.join(f'<a href="#ch03-s0{i}"><span>3.{i} · {c}-Ranking</span><strong>{t}</strong><small>{d}</small></a>' for i,(c,t,d) in enumerate(CHAPTER_TOPICS,1))+'</nav>',para(PERIOD,'rp-period'),'</div>']
 return ''.join(out)
def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('1',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('rp-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.add('rp-stage');stage.set('data-slide-height',760 if i!=2 else 800)
 board=next(n for n in root.walk() if n.has('cr-board'))
 for n in list(root.walk()):
  if n.has('cr-eyebrow') or n.tag=='figcaption':remove(root,n)
  if n.has('cr-head-right'):
   n.children=[x for x in n.children if isinstance(x,Node) and x.tag=='button' and i==1]
  if n.attrs.get('data-rr-action') in ('image','export'):remove(root,n)
  if n.has('cr-foot'):n.add('rp-foot')
 board.children+=fragment(f'<div class="rp-caption">图 3-1-{i} {E(FIGURES[i-1])}</div>')
 root.children+=fragment(f'<figcaption class="rp-sr-caption">图 3-1-{i} {E(FIGURES[i-1])}</figcaption>')
 return tree.root.html()
def section(data):
 out=['<section class="chapter-section gosr-section cr-section rr-section rp-section" id="ch03-s01">','<div class="section-topline"><span>3.1 / R-RANKING</span></div>',f'<h2>3.1 {TITLE}</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'rp-position'),para('核心发现：'+FINDING)]
 for i,(title,ps) in enumerate(STORIES,1):
  out += [f'<h3>{title}</h3>',para(ps[0]),figure(i,data)]
  out += [interpretation(t) for t in ps[1:]]
 out += [f'<h3 id="rr-1-actions">{ACTION_TITLE}</h3>',para(ACTION_INTRO)]
 for title,t in ACTIONS:out += [f'<h4 class="rp-action-title">{title}</h4>',para(t)]
 out += [para(BRIDGE),'<script id="rp-source-notes" type="application/json">']
 import json
 out += [json.dumps(NOTES,ensure_ascii=False),'</script></section>']
 return ''.join(out)
def manuscript():
 out=['# '+CHAPTER_TITLE,CHAPTER_QUESTION,CHAPTER_INTRO,'## 本章主要观察']
 for h,t in CHAPTER_FINDINGS:out += ['### '+h,t]
 out += [PERIOD,'# 3.1 '+TITLE,INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-1-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
