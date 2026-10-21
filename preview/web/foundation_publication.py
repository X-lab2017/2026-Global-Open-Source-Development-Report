"""F-Ranking publication manuscript shared by Web and review PDF."""
from html import escape as E
from goso_reading import Tree,Node,fragment,remove

EDITION='2026-10-21-f-ranking-publication-v1'
TITLE='全球开源基金会影响力排行榜（F-Ranking）'
INTRO='基金会为跨组织协作提供项目托管、社区支持与共同维护的组织基础。基金会榜先观察这些组织在开源协作网络中的位置，再沿旗下组织和代表项目，寻找可以落实支持的具体对象。'
QUESTION='哪些基金会具有较高的开源影响力，如何结合组织层级与月度变化识别共建对象？'
POSITION='以 OpenRank 观察协作影响力，以活跃开发者补充参与规模，对应 OSDGs 的共同创造与可持续视角。整体与旗下组织分别阅读，榜单不直接评价治理质量。'
FINDING='Linux 基金会、开放原子和 Apache 位居全球榜前三；月度记录中，头部成员稳定，第二、第三位发生过交换。旗下组织视图提供进一步观察的结构，但其排名与数值仍为模拟。'
FIGURES=['全球基金会影响力与参与规模','Linux 基金会旗下组织比较（模拟）','基金会月度位次变化']
STORIES=[
 ('3.3.1 整体格局：结合组织范围理解影响力',[
 '全球榜保留 21 个基金会条目。Linux 基金会、开放原子和 Apache 的 OpenRank 分别为 196,128.27、99,965.35 和 81,247.51，活跃开发者分别为 63,940、23,173 和 19,251 人。图 3-3-1 将两个指标并列，呈现各组织的影响力与参与规模。',
 '整体与单列组织可能存在范围重叠。原榜的 Linux 基金会条目包含旗下组织，同时又单列 OpenInfra；这些分值和开发者数不能简单相加，也不能据此推算全球生态份额。比较后仍需核对各条目覆盖的项目与仓库。',
 '代表项目帮助把组织比较转向具体工作。项目入口用于了解维护对象，并非本期指标的完整统计清单。Ruby Foundation 的主体及项目关系尚待核验，保留原榜名称和数值，不以名称相近的组织替代。']),
 ('3.3.2 旗下组织：从整体观察进入具体领域',[
 'Linux 基金会体系覆盖云原生、人工智能、网络、安全等多个领域。图 3-3-2 列出 16 个旗下组织示例及其代表项目，展示如何在同一层级开展比较；组织与项目有参考资料，名次、OpenRank 和开发者数均为模拟。',
 '领域与项目提供了寻找共建对象的线索。CNCF 对应 Kubernetes 等云原生项目，OpenSSF 对应 Sigstore 等软件供应链安全项目。现有模拟值只用于演示比较方式，不能据此判断哪个领域贡献最大或最值得投入。',
 '组织关系与统计映射需要分别维护。这些组织不全是独立法律实体，也不是 Linux 基金会的完整名录；代表项目参考资料核对至 2026 年 10 月 17 日，不能替代截至 6 月 30 日的报告期映射。旗下数值不回算整体。']),
 ('3.3.3 月度变化：稳定成员中的位置交换',[
 '2025 年 7 月至 2026 年 6 月，八家基金会的月度记录中，Linux 基金会始终位列第 1。开放原子与 Apache 在 2025 年 10 月、2026 年 1 月交换第二、第三位，其余月份开放原子居前。图 3-3-3 同时呈现头部稳定与局部换位。',
 '月度名次是继续核查的线索。位置交换不等于影响力分值增长，也不能用月度名次平均得出全年排名。可在换位月份核查项目活动、参与者和组织映射，判断变化来自持续协作还是统计范围调整。',
 '真实轨迹与模拟轨迹保持分开。全球视图保留八家基金会的原始记录；旗下组织的月度视图仍为模拟。缺失月份留空，不补零，也不跨越空缺连线，避免把未提供的记录画成已发生的变化。'])]
ACTION_TITLE='3.3.4 行动建议：把组织支持落实到共同维护'
ACTION_INTRO='影响力榜帮助定位组织，项目的实际维护需求决定支持如何落地。'
ACTIONS=[
 ('基金会：明确项目范围与维护责任','维护组织、项目、仓库之间的对应关系，记录托管与迁移时间，为重点项目列出维护团队和支持周期。通过责任交接、关键问题处理和持续贡献者参与观察进展。'),
 ('公共部门与资助方：围绕具体维护需求安排支持','与基金会共同确认需要支持的项目和任务，约定阶段成果与复核时间。跟踪任务完成、资金支持的延续和维护职责接续，避免仅按榜单名次分配资源。'),
 ('企业与社区：组织跨机构的长期共建','围绕共同依赖的项目分担测试、文档、安全响应等工作，明确各方负责人。定期检查贡献接纳、问题关闭和外部参与者留存，识别仍无人承担的维护任务。')]
BRIDGE='基金会提供协作的组织基础，项目承载具体成果。下一节转向项目榜，进一步观察哪些共同成果形成了较高影响力。'
NOTES=[
 '3.3 全球榜保留 21 个原始条目；真实月度表覆盖其中八家，时间为 2025-07 至 2026-06。Linux 基金会整体含旗下组织，原表又单列 OpenInfra 等条目；范围可能重叠，不加总分值或开发者数，不推算生态份额。',
 '3.3 代表项目仅为阅读入口，不是完整项目清单或本期统计映射。组织与项目参考资料核对于 2026-10-17，晚于报告期末；Ruby Foundation 主体关系仍待核验，DuckDB Foundation 的国家字段未提供，均保留原始状态。',
 '图 3-3-2 的 16 个旗下组织与项目有参考资料，但名次、OpenRank、开发者数及图 3-3-3 中的旗下组织月度轨迹均为模拟。样本不全是独立法律实体，也不是完整名录，不回算 Linux 基金会整体。缺失不补零，不跨缺失连线；位次变化不等于分值增长。']

def paragraphs():
 return [INTRO,'研究问题：'+QUESTION,'指标定位：'+POSITION,'核心发现：'+FINDING]+[t for _,ps in STORIES for t in ps]+[ACTION_INTRO]+[t for _,t in ACTIONS]+[BRIDGE]

def figure(i,data):
 import rankings
 tree=Tree(rankings.figure('3',i,data));root=next(n for n in tree.root.walk() if n.tag=='figure');root.add('fp-figure')
 stage=next(n for n in root.walk() if n.has('rr-stage'));stage.add('fp-stage');stage.set('data-slide-height',{1:840,2:840,3:760}[i]);stage.set('data-reflow-minimum-width','700')
 board=next(n for n in root.walk() if n.has('cr-board'))
 for n in list(root.walk()):
  if n.has('cr-eyebrow') or n.tag=='figcaption':remove(root,n)
  if n.has('cr-head-right'):n.children=[]
  if n.attrs.get('data-rr-action') in ('source','image','export'):remove(root,n)
  if n.has('cr-foot'):n.add('rp-foot')
 board.children+=fragment(f'<div class="rp-caption">图 3-3-{i} {E(FIGURES[i-1])}</div>')
 root.children+=fragment(f'<figcaption class="rp-sr-caption">图 3-3-{i} {E(FIGURES[i-1])}</figcaption>')
 return tree.root.html()

def section(data):
 from region_publication import para,interpretation
 out=['<section class="chapter-section gosr-section cr-section rr-section rp-section fp-section" id="ch03-s03">','<div class="section-topline"><span>3.3 / F-RANKING</span></div>',f'<h2>3.3 {TITLE}</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'rp-position'),para('核心发现：'+FINDING)]
 for i,(title,ps) in enumerate(STORIES,1):
  out += [f'<h3>{E(title)}</h3>',para(ps[0]),figure(i,data)]
  out += [interpretation(t) for t in ps[1:]]
 out += [f'<h3 id="rr-3-actions">{ACTION_TITLE}</h3>',para(ACTION_INTRO)]
 for title,t in ACTIONS:out += [f'<h4 class="rp-action-title">{E(title)}</h4>',para(t)]
 return ''.join(out+[para(BRIDGE),'</section>'])

def manuscript():
 out=['# 3.3 '+TITLE,*paragraphs()[:4]]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-3-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
