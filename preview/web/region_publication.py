"""GOSR opening and R-Ranking: one manuscript for Web and PDF."""
from html import escape as E
from goso_reading import Tree, Node, fragment, remove
EDITION='2026-10-21-r-ranking-publication-v1'
CHAPTER_TITLE='第三章 全球开源影响力排行榜（GOSR）'
CHAPTER_QUESTION='哪些地区、组织与成果形成了重要影响，如何把榜单观察转化为持续共建？'
CHAPTER_INTRO='第二章描绘全球开源的参与基础、贡献关系与成果分布。本章进一步把观察落到具体主体：从地区寻找协作节点，从企业与基金会识别投入和组织力量，再沿项目、新势力与模型追踪共同成果。榜单提供定位和比较的起点，帮助决策者选择需要进一步研究、支持和连接的对象。'
CHAPTER_FINDINGS=[
 ('参与规模与影响位置需要结合阅读','同一地区或组织，在人数、仓库数量和网络影响力上的排序可能不同。比较的重点，是辨识不同的参与结构，并沿具体项目查找协作机会。'),
 ('组织与成果需要分层观察','企业、基金会、项目与仓库具有不同边界。整体与子组织、项目与所含仓库分别排名，才能理解影响力由哪些协作关系承载。'),
 ('当期位置与持续变化需要不同证据','本期榜单用于观察当前格局；有连续记录的对象可以进一步比较位次变化。新建仓库和模型版本还需结合创建时间、复用关系及真实使用，观察影响能否延续。')]
CHAPTER_TOPICS=[('R','地区','定位协作发生的地域节点'),('C','企业','观察持续投入的产业力量'),('F','基金会','理解跨组织共建的承载主体'),('P','项目','识别具有网络影响的共同成果'),('E','新势力','观察新仓库与新项目的形成'),('M','模型','辨识模型复用网络中的重要节点')]
PERIOD='除特别说明外，统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日；模型榜采用 2026 年 8 月快照。'
TITLE='全球行政区划影响力排行榜（R-Ranking）'
INTRO='地区榜把第二章的空间分布进一步落到具体节点。全球行政区、中国省级行政区与中国城市分别提供一个观察层级，帮助读者寻找参与规模相近、协作位置不同的地区，形成更有针对性的对标与共建清单。'
QUESTION='哪些地区形成了重要的开源协作影响，参与规模与影响力的位置有何不同？'
POSITION='以 OpenRank 观察地区在协作网络中的影响，以开发者数量补充参与基础；衔接 OSDGs 的规模、多样性与共同创造视角。三个地区榜独立比较。'
FINDING='头部地区的参与规模与影响力呈现不同组合；全球 Top 100 行政区分布在 32 个国家；中国省级与城市榜共同呈现多个协作节点。地方支持需要从榜单位置继续追踪具体项目、维护角色与跨地区合作。'
FIGURES=['地区影响力与参与规模排名','全球 Top 100 行政区的国家分布','中国省市影响力联动']
STORIES=[
 ('3.1.1 地区比较：参与规模与影响位置并不同步',[
 '图 3-1-1 显示，加利福尼亚州以 50,883.80 的 OpenRank 位居全球行政区榜首，英格兰为 36,398.10。北京市与上海市分别位列第 14 和第 16，OpenRank 为 10,188.30 和 8,462.50。榜单同时列出开发者数量，使影响位置能够与参与基础一起阅读。',
 '规模相近或更大，并不必然对应更靠前的影响位置。卡纳塔克邦的开发者数量为 570.53 万，高于英格兰的 487.08 万，但 OpenRank 位列第 8。两项指标描述不同侧面，这种差异为进一步研究项目结构、维护角色与跨地区连接提供线索，不能直接解释为个人贡献效率的高低。',
 '对标对象应结合统计层级与参与背景选择。全球榜沿用原表中的州、省、构成国等地区记录，行政划分粒度并不完全相同；省级与城市级榜单也分别统计。当前截面能够说明本期位置，不能单独证明跨年赶超或某项政策的效果。']),
 ('3.1.2 入榜分布：头部集中，多国拥有重要节点',[
 '图 3-1-2 按入榜行政区数量观察全球 Top 100 的国家分布。美国入榜 25 个，印度 12 个，巴西 9 个，德国 8 个，中国 7 个，五国合计 61 个；全部入榜行政区分布在 32 个国家。',
 '入榜节点数量提供了不同于单点排名的空间视角。一国可以同时拥有多个靠前地区，也可以由少数节点进入榜单。这个分布有助于确定跨地区合作的调研范围，但不代表各国 OpenRank 份额，也不能直接作为生态韧性或发展质量的评分。',
 'Top 100 的国家汇总与 Top 30 的详细榜单是两份独立底表。前者用于观察入榜分布，后者用于查看具体地区的数值；不能用 Top 30 的名单补齐未提供的 100 个地区，也不能把未列入样本的地区解释为没有开源活动。']),
 ('3.1.3 省市联读：把区域位置落到具体协作节点',[
 '图 3-1-3 将省级榜与其对应的城市记录联动呈现。中国省级榜中，北京、上海居前，广东、台湾、浙江随后；城市榜中，北京、上海、杭州、深圳、台北位列前五。省级位置提供区域背景，城市记录帮助进一步定位协作节点。',
 '同一省级地区可以连接多个入榜城市。广东对应深圳、广州和珠海，分别位列全国城市榜第 4、第 6 和第 29；浙江对应杭州和宁波，其中杭州位列第 3。城市记录帮助将省级观察细化为可调研的节点，但省级与城市级的识别覆盖不同，城市值不加总回算省级值。',
 '节点清单需要继续连接项目与维护者。对地方、高校和企业而言，下一步可以核查这些城市共同参与了哪些项目、承担哪些维护职责，以及是否形成跨城市协作。当前榜单为调研提供起点，不足以把地区差异归因于某一家企业或某一项政策。'])]
ACTION_TITLE='3.1.4 行动建议：让地区对标连接到共同项目'
ACTION_INTRO='把排名用于识别值得深入了解的对象，再用项目与协作证据决定支持方向。'
ACTIONS=[
 ('地方公共部门：建立可持续的对标清单','在相同统计层级内，选择参与规模和产业背景可比较的地区，持续记录参与规模、OpenRank 与重点项目的变化。观察同一组对象的连续表现，并记录范围调整，避免把短期换位直接作为政策绩效。'),
 ('高校与企业：把人才支持落实到维护任务','从本地参与较多的项目中选择共同维护任务，明确导师或维护者、参与团队与支持周期。以贡献是否被接纳、人员是否持续参与、关键维护职责是否有人接续，观察支持是否产生持续作用。'),
 ('平台与社区：围绕共同项目连接城市','核查不同城市共同参与的项目及维护需求，组织跨城市协作，并保留项目、任务、参与团队和阶段成果记录。观察合作是否在活动结束后延续，以及是否吸引新的持续贡献者。')]
BRIDGE='地区提供协作发生的空间，企业则是持续投入的重要主体。下一节将进入企业榜，观察组织影响力与参与结构。'
NOTES=[PERIOD,'OpenRank 与开发者数量分别计量，不计算人均效率或合成总分。开发者数量单位为万，不直接解释为活跃开发者。','全球行政区、中国省级与中国城市各有 30 条详细记录；国家分布表覆盖 100 个入榜行政区、32 个国家。数量相同的国家并列，后续名次跳位；“其余国家”为汇总项，不参与排名。','省级与城市分别保留原榜名次，城市数值不加总回算省级值。台湾省及其城市纳入中国范围。全球行政区粒度不同；地理稳定 ID 和边界版本待补，不据此生成精确行政区地图。','当前 3.1 底表不含历史位次，不能据此计算排名升降。原始值与缺失状态保持不变，筛选与排序只改变展示。','全章六类主体分别排名，不合成跨对象总榜。OpenRank 不等于治理质量或商业价值；ModelRank 不等于模型能力或开放许可证评级。其他小节中的模拟范围保留各图醒目标识。']
def paragraphs():
 return [CHAPTER_QUESTION,CHAPTER_INTRO,*[t for a in CHAPTER_FINDINGS for t in a],PERIOD,INTRO,QUESTION,POSITION,FINDING,*[p for _,ps in STORIES for p in ps],ACTION_INTRO,*[p for _,p in ACTIONS],BRIDGE]
def para(t,cls=''):return f'<p class="{cls}">{E(t)}</p>'
def opening():
 out=['<div class="rp-opening" id="gosr-reading-guide">',f'<h2>{E(CHAPTER_QUESTION)}</h2>',para(CHAPTER_INTRO),'<h3>本章主要观察</h3>']
 out += [para(t+'。'+b) for t,b in CHAPTER_FINDINGS]
 out += ['<nav class="rp-topics" aria-label="第三章六类榜单">'+''.join(f'<a href="#ch03-s0{i}"><span>3.{i} · {c}-Ranking</span><strong>{t}</strong><small>{d}</small></a>' for i,(c,t,d) in enumerate(CHAPTER_TOPICS,1))+'</nav>',para(PERIOD,'rp-period'),'</div>']
 return ''.join(out)
def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('1',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('rp-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.set('data-slide-height',760 if i!=2 else 800)
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
  out += [para(t,'rp-interpretation') for t in ps[1:]]
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
