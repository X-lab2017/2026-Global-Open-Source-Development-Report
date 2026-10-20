"""Chapter 2 opening, aligned with the seven reviewed publication manuscripts."""
from html import escape as E
TITLE='第二章 全球开源生态观测地图（GOSO）'
DECK='从广泛参与，走向持续共同创造。'
INTRO='第一章提出持续共同创造及其公共价值的观察框架。本章将这一框架带入全球开源生态：用地域分布看参与基础，用时间序列看结构变化，用项目与贡献关系看协作连接，依次观察活跃参与、贡献、项目影响力、人才、资产、多样性和治理。'
QUESTION='全球开源力量分布在哪里，形成了怎样的贡献与成果，又如何延续为长期共建？'
FINDINGS=[
('参与扩大，作用位置各异','参与规模、开发者贡献和项目影响力呈现不同的地域排序。五域比较中，欧洲在活跃、贡献和高影响力人才规模上具有优势，美国保持项目影响力的规模优势，中国贡献与项目影响力增长较快。理解区域发展，需要同时观察规模、变化与所承担的作用。','ch02-s01','2.1—2.4'),
('供给增长，连接方式不同','四个代码平台的活跃仓库均增长；模型与数据集样本中，发布数量与下载使用呈现不同结构。地域来源比较进一步显示，中美项目连接本土与海外贡献的方式不同。资产发布、成果使用和跨地域共建，需要结合起来观察。','ch02-s05','2.5—2.6'),
('长期共建，需要组织与规则','基金会项目规模与影响份额有所扩大，主流许可证及木兰宽松许可证的采用持续增长。这些观察为组织支持与共享规则提供了实践入口。本章的共同指向，是把参与和成果积累连接到持续维护、清晰许可与稳定协作。','ch02-s07','2.7')]
READING='七节沿着三层问题展开：先看谁在参与、贡献如何形成、项目影响积累在哪里；再看人才、资产与跨地域连接；最后看支撑长期协作的组织与规则。'
TOPICS=[('V-MAP','活跃参与','参与基础有多大，分布在哪里？'),('C-MAP','协作贡献','参与如何形成共同建设的贡献？'),('I-MAP','项目影响力','哪些项目与地区积累了网络影响？'),('T-MAP','开源人才','支撑协作的高影响力人才在哪里？'),('A-MAP','开放资产','代码、模型与数据如何积累和使用？'),('D-MAP','多样性共建','不同地区的贡献如何连接项目？'),('G-MAP','治理与公益','组织与许可如何支撑长期共建？')]
SCOPE=['除特别说明外，统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日；历史年份采用对应报告年度。单独标注的快照、累计样本与平台补充分别阅读，具体范围见各节。','本章以 OpenDigger 为主要数据与方法基础，结合编制组确认的多平台统计和专题样本。人数、贡献度、项目影响力及资产数量分别计量；五域用于比较，不构成全球的穷尽分区。','网页与 PDF 共用研究正文及核心图形编码。网页支持进一步选择与比较；模拟类别图和机制示意均有标注，不作为实测发现。规模、排名与网络影响也不能单独证明治理质量或公共价值。']
def cover():
 return '<section class="goso-chapter-intro" id="goso-intro" aria-label="本章导读"><h2>本章导读</h2><p class="goso-intro-question">'+E(QUESTION)+'</p><p>'+E(INTRO)+'</p><h3>本章主要观察</h3>'+''.join('<p><strong>'+E(title)+'。</strong>'+E(text)+'</p>' for title,text,_,_ in FINDINGS)+'</section>'
def overview():
 return '<section class="goso-reading-guide goso-intro-route-lead" aria-label="本章阅读方式"><div><h3>本章阅读路径</h3><p>'+READING+'</p></div></section>'
def route():
 return '<nav class="foundation-route goso-chapter-route" aria-label="本章阅读路径">'+''.join(f'<a href="#ch02-s0{i}"><small>2.{i} / {code}</small><strong>{title}</strong><span>{question}</span></a>' for i,(code,title,question) in enumerate(TOPICS,1))+'</nav>'
def scope(lang):
 return '<details class="goso-scope"><summary>阅读说明 · 时间、范围与图件</summary>'+''.join('<p>'+E(t)+'</p>' for t in SCOPE)+'</details>'
def manuscript():
 out=['# '+TITLE,'## 本章导读',QUESTION,INTRO,'## 本章主要观察']
 for title,text,_,_ in FINDINGS:out+=['### '+title,text]
 out+=['## 七个主题的阅读路径',READING]
 out += [f'- 2.{i} {title}（{code}）：{question}' for i,(code,title,question) in enumerate(TOPICS,1)]
 return '\n\n'.join(out+['## 阅读说明',*SCOPE])+'\n'
