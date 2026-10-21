"""F-Ranking publication manuscript shared by Web and review PDF."""
from html import escape as E
from goso_reading import Tree,Node,fragment,remove

EDITION='2026-10-21-f-ranking-publication-v2'
TITLE='全球开源基金会影响力排行榜（F-Ranking）'
INTRO='基金会通过项目托管、社区支持和维护协调，为跨组织协作提供基础。基金会榜从整体影响力出发，再进入旗下组织与代表项目，帮助寻找具体的共建对象。'
QUESTION='哪些基金会具有较高的开源影响力，如何从组织层级与月度变化中识别共建线索？'
POSITION='以 OpenRank 观察协作影响力，以活跃开发者补充参与规模，对应 OSDGs 的共同创造与可持续视角。整体与旗下组织分别比较，榜单不直接评价治理质量。'
FINDING='Linux 基金会、开放原子和 Apache 位居全球榜前三；月度记录中，第二、第三位发生过交换。阅读榜单时，既要观察位置变化，也要辨明整体与旗下组织的范围。'
FIGURES=['全球基金会影响力与参与规模','Linux 基金会旗下组织比较（模拟）','基金会月度位次变化']
STORIES=[
 ('3.3.1 整体格局：结合组织范围理解影响力',[
 '全球榜列出 21 个基金会条目。Linux 基金会、开放原子和 Apache 的 OpenRank 分别为 196,128.27、99,965.35 和 81,247.51。图 3-3-1 将影响力与活跃开发者并列，并提供代表项目入口。',
 '整体与单列组织可能存在范围重叠。Linux 基金会条目包含旗下组织，原榜又单列 OpenInfra，因此分值和开发者数不能简单相加，也不能据此推算全球生态份额。深入比较前，应核对各条目覆盖的项目与仓库。',
 '代表项目帮助读者找到具体的维护对象。这些入口并非本期指标的完整统计清单。Ruby Foundation 的主体与项目关系仍待核验，保留原榜名称和数值，不以名称相近的组织替代。']),
 ('3.3.2 旗下组织：从整体观察进入具体领域',[
 '图 3-3-2 展开 Linux 基金会体系中的 16 个组织示例，涵盖云原生、人工智能、网络与安全等领域。组织与项目有参考资料，名次、OpenRank 和开发者数均为模拟，仅用于展示比较方式。',
 '从领域进入项目，才能判断具体支持需求。例如，可沿 CNCF 了解 Kubernetes 的维护工作，沿 OpenSSF 了解 Sigstore 的安全协作。模拟排名不用于判断哪个领域贡献最大或应优先获得投入。',
 '组织名录不等于报告期统计范围。示例并非完整名录，各组织也不全是独立法律实体；项目参考资料核对至 2026 年 10 月 17 日，不能替代截至 6 月 30 日的报告期映射，旗下数值不回算整体。']),
 ('3.3.3 月度变化：稳定成员中的位置交换',[
 '2025 年 7 月至 2026 年 6 月，八家基金会的月度记录中，Linux 基金会始终第 1。2025 年 10 月、2026 年 1 月，Apache 位列第 2、开放原子第 3，其余月份顺序相反。图 3-3-3 呈现头部稳定与局部换位。',
 '月度换位提示进一步核查。它不等于分值增长，月度名次也不能平均为全年排名。可核查换位月份的项目活动、参与者和组织映射，判断变化是否持续，以及统计范围是否调整。',
 '两类轨迹保持清楚区分。全球视图为八家基金会的真实记录，旗下组织视图为模拟。缺失月份留空，不补零或跨空缺连线。'])]
ACTION_TITLE='3.3.4 行动建议：把组织支持落实到共同维护'
ACTION_INTRO='支持对象要落实到项目，支持效果要落实到维护任务。'
ACTIONS=[
 ('基金会：明确项目范围与维护责任','持续维护组织、项目与仓库的对应关系，记录托管、迁移和责任交接时间。为重点项目明确维护团队与支持周期，按期检查关键问题处理和人员接续。'),
 ('公共部门与资助方：围绕具体维护需求安排支持','与基金会共同确定待支持的项目、任务和复核时间。检查阶段成果、维护缺口及支持是否接续，将资源安排建立在具体需求上。'),
 ('企业与社区：组织跨机构的长期共建','围绕共同依赖的项目分担测试、文档和安全响应，明确负责人。定期检查贡献接纳、问题关闭和参与者持续贡献情况，补上无人承担的维护任务。')]
BRIDGE='基金会支持组织协作，项目承载共同成果。下一节转向项目榜，观察具体成果的影响力。'
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
 from pathlib import Path
 import json
 logos=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/foundation-logos/manifest.json').read_text())
 out += [para(BRIDGE),'</section>','<script id="foundation-logos" type="application/json">'+json.dumps({k:{'file':v['filename']} for k,v in logos.items()},ensure_ascii=False).replace('<','\\u003c')+'</script>']
 return ''.join(out)

def manuscript():
 out=['# 3.3 '+TITLE,*paragraphs()[:4]]
 for i,(h,ps) in enumerate(STORIES,1):out += ['## '+h,ps[0],f'图 3-3-{i} '+FIGURES[i-1],*ps[1:]]
 out += ['## '+ACTION_TITLE,ACTION_INTRO]
 for h,t in ACTIONS:out += ['### '+h,t]
 return '\n\n'.join(out+[BRIDGE])+'\n'
