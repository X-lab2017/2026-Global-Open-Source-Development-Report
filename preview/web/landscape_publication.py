"""Chapter 4 opening and 4.1: a shared publication manuscript; observed data unchanged."""
from html import escape as E
from goso_reading import Tree,Node,fragment,remove
EDITION='2026-10-21-a-landscape-publication-v1'
CHAPTER_TITLE='第四章 全球开源技术全景洞察（GOSL）'
CHAPTER_QUESTION='开源技术如何分工协作，哪些基础能力值得持续支持？'
CHAPTER_INTRO='第三章从榜单识别重要主体与成果，本章将项目放回技术结构，观察它们共同提供了哪些能力。六个领域分别覆盖智能体、模型、云基础设施、数据库、处理器架构与深度学习生态，为技术选型、公共投入和跨组织协作提供参照。'
CHAPTER_OBSERVATIONS=[('从项目名单走向能力结构','全景图按功能组织项目，帮助读者寻找互补能力与可进一步核查的替代实现。项目被收录不代表已经形成实际依赖关系，也不构成采购推荐。'),('从单月位置走向连续观察','有连续数据的领域，同时观察类别与项目的影响力、集中度和样本覆盖。不同领域的分类、来源与时间窗各自保留，不合成为跨领域总榜。'),('从技术供给走向共同维护','先辨认需要的能力，再核查开放条件、实际采用与维护需求。公共支持应落实到可交付的上游工作，并持续观察贡献接纳和维护接续情况。')]
TOPICS=[('Agentic AI','理解应用、编排与运行支撑'),('AI 大模型','观察模型供给与任务结构'),('云基础设施','梳理部署、运行与服务能力'),('数据库系统','比较数据管理与处理能力'),('RISC-V','连接指令架构与软硬件生态'),('PyTorch 生态','观察模型开发与工程协作')]
PERIOD='本报告默认统计期为 2025 年 7 月 1 日至 2026 年 6 月 30 日。4.1 使用 2025 年 3 月至 2026 年 8 月的月度记录；其余领域保留各自来源的快照时间。'
TITLE='Agentic AI 全景洞察（A-Landscape）'
INTRO='智能体将模型能力接入具体任务，需要应用入口、编排框架、工具环境和模型基础设施共同支撑。本节以 145 个精选项目为固定样本，从技术分工进入协作影响力，再观察类别内部的集中与变化。'
QUESTION='智能体生态由哪些能力共同支撑，影响力分布与项目集中度提示了哪些维护重点？'
POSITION='技术分类描述功能分工；OpenRank 观察开源协作网络影响力，不代表模型能力、市场规模或使用量。'
FINDING='2026 年 8 月，个人助手、推理引擎和编码代理位居样本类别影响力前三。个人助手的影响力主要集中于两个头部项目；采用连续可比样本后，多代理编排的份额上升较明显。国家贡献图为模拟示例，不用于判断真实地域格局。'
HISTORY_NOTE='月度位次在每个月分别计算，比较图的位次覆盖全领域 25 类。类别有值项目数变化时，需要回到共同样本进一步核查；曲线用于定位变化，不单凭位次判断投入成效。'
FIGURES=[('al-agent','Agent Infra 技术全景'),('al-model','Model Infra 技术全景'),('al-category-rank','技术类别影响力分布'),('al-category-heat','两层技术类别的月度位次变化'),('al-category-trend','重点类别的影响力轨迹比较'),('al-project-rank','类别内项目排名与历史变化'),('al-concentration','类别内头部项目集中度'),('al-shift','共同样本的类别份额变化'),('al-country-rank','国家贡献分布与排名（模拟）'),('al-country-detail','国家贡献的技术类别结构（模拟）'),('al-country-stack','技术类别中的国家贡献份额（模拟）'),('al-specialization','国家相对专长比较（模拟）'),('al-country-trend','国家贡献份额的月度变化（模拟）')]
STORIES=[
('land-map','4.1.1 技术结构：连接任务、执行与模型能力',[
 '两张全景分别展示 Agent Infra 的 86 个项目、12 个类别，以及 Model Infra 的 59 个项目、13 个类别。前者从任务入口延伸到编排与运行支撑，后者覆盖模型服务、训练、数据和计算。图中位置表示功能分层，不表示项目之间已经存在依赖关系。',
 '全景的价值在于辨认协作所需的完整能力。构建编码或知识助手，除了应用入口，还需进一步核查工具连接、上下文管理、执行环境和评测能力；模型部署则需要结合推理、数据与计算环节判断适配条件。项目数量不能直接当作能力完备度。']),
('land-trends','4.1.2 影响力分布：从类别进入具体项目',[
 '2026 年 8 月，140 个项目有观测值，样本 OpenRank 合计 5,706.38。个人助手、推理引擎、编码代理分别为 752.76、662.78 和 563.09，合计占当月有值样本的 34.7%；它们分属应用与模型基础设施，提示技术供给需要跨层协作。',
 '类别排名同时受项目变化与观测覆盖影响。18 个月中，有值项目由 93 个变为 140 个。因此，月度位次适合定位变化发生在哪些类别，不能直接把类别总量变化解释为同一批项目的增长。',
 '类别之内仍需辨认具体维护对象。个人助手类别的 OpenClaw 与 Hermes Agent，2026 年 8 月 OpenRank 分别为 303.24 和 277.91，两者合计占该类别的 77.2%。这一集中结构为后续维护需求调研提供线索，但不能据此推定用户规模或商业竞争地位。']),
('land-extensions','4.1.3 结构变化：区分头部集中与可比增长',[
 '集中度将类别总量分解到项目。个人助手前三个项目占该类别当月 OpenRank 的 82.4%，推理引擎为 67.5%，编码代理为 48.8%。类别收录项目较少时，前三占比自然较高，应结合项目数量与观测覆盖理解。',
 '共同样本更适合观察已有项目的结构变化。2025 年 9 月至 2026 年 8 月，107 个项目每月均有观测。在这一共同样本内，多代理编排的份额从 1.33% 升至 6.58%，增加 5.25 个百分点；编码代理从 16.85% 降至 11.55%，减少 5.30 个百分点。',
 '连续可比与新项目进入回答不同问题。共同样本排除了中途创建或缺少观测的项目，其中个人助手仅有 2 个项目，不能代表该类别当前 7 个项目的完整供给。应将当期分布与共同样本变化并读，再核查推动变化的具体项目。']),
('land-country','4.1.4 贡献观察：用模拟示例说明分析方法',[
 '以下五图使用同一组独立模拟数据，展示从地域分布进入类别结构、相对专长和月度变化的分析路径。图中的国家名、数值与排序均不构成实测发现，模拟贡献量也不能与前述项目 OpenRank 相加。',
 '贡献份额与相对专长需要分别理解。份额回答某国在当前范围占多少；相对专长 LQ 比较该国在某类别的份额与其总体份额，1 为参照线。隐藏曲线不改变统计分母，“其他”和“未知”始终保留。',
 '地域结论需等待真实贡献数据。接入时应保留完整贡献者集合、公开所在地的时间信息和未知来源，跨项目去重人数，并单独识别机器人。所在地不等于国籍，贡献份额也不等于项目治理权。'])]
ACTION_TITLE='4.1.5 行动建议：把技术观察转化为持续维护'
ACTIONS=[('公共部门与资助机构：围绕共用能力配置支持','结合全景结构和真实采用需求，选择需要长期维护的工具、接口与评测基础设施，明确负责团队、交付任务和支持周期。以被上游接纳的成果、关键问题解决情况和维护接续记录观察进展。'),('企业与研究机构：围绕具体项目承担上游工作','在拟采用的类别中核查开放条件、兼容性、维护状态与替代实现，选择可持续承担的修复、文档、评测或互操作任务。持续跟踪贡献是否被接纳、版本升级是否顺利，以及团队是否形成稳定维护能力。'),('平台与观测团队：同时记录变化与证据缺口','按月保存分类、样本和数据版本，分别发布当期全样本与连续可比样本结果，记录新增项目与缺失原因。真实地域数据补齐后，再发布国家层面的实测分析，并同步披露未知来源与去重方法。')]
BRIDGE='智能体全景展示了模型能力如何被组织成可执行的任务。下一节转向 AI 大模型，进一步观察模型供给与任务结构。'
NOTES=['固定分类来自 antgroup/agentic-ai-landscape，提交 e330d75ea4ca314bc81f6868df63425c8acca5e3。145 个项目按 repo_id 去重，每个项目计入一个主要类别；这是精选样本，不是全球项目普查。','月度窗口为 2025-03—2026-08。2025-03—2025-08 的历史记录来自 2026-10-17 固定的 OpenDigger 快照；2025-09—2026-08 保留既有固定值。分类为当前版本的历史回溯，不推断历史项目总体。','无观测和尚未创建均保留缺失，不补零。类别 OpenRank 为有值项目之和；份额以所选范围全部有值项目为分母。环比使用两月共同有值项目；份额变化使用整个窗口每月均有值的项目。','图 4-1-9 至图 4-1-13 为固定种子 341 生成的独立模拟数据。模拟开发者按标识集合去重，不跨类别直接相加；其他与未知保留分母，不分配到虚构地图区域。']
def para(s,cls=''):return f'<p class="{cls}">{E(s)}</p>'
def interpretation(s):
 h,b=s.split('。',1);return '<p class="lp-interpretation"><strong>'+E(h)+'。</strong>'+E(b)+'</p>'
def opening():
 return '<section class="lp-opening" id="gosl-overview"><h2>'+E(CHAPTER_QUESTION)+'</h2>'+para(CHAPTER_INTRO)+''.join(interpretation(h+'。'+b) for h,b in CHAPTER_OBSERVATIONS)+'<nav class="lp-topics" aria-label="第四章六个领域">'+''.join(f'<a href="#ch04-s0{i}"><span>4.{i}</span><strong>{E(t)}</strong><small>{E(d)}</small></a>' for i,(t,d) in enumerate(TOPICS,1))+'</nav>'+para(PERIOD,'lp-period')+'</section>'
def apply(html):
 tree=Tree(html);root=next(n for n in tree.root.walk() if n.has('al-chapter'));root.set('data-publication-edition',EDITION)
 old=next(n for n in root.walk() if n.attrs.get('id')=='ch04-s01');panels={n.attrs['id']:n for n in old.walk() if n.has('al-panel')}
 for i,(id,title) in enumerate(FIGURES,1):
  panel=panels[id];panel.set('aria-labelledby',id+'-caption');panel.set('data-figure-number',f'图 4-1-{i}')
  for n in list(panel.walk()):
   if n.has('al-description') or n.has('al-source') or n.has('al-atlas-hint') or 'data-svg' in n.attrs or 'data-csv' in n.attrs:remove(panel,n)
   elif n.has('al-panel-heading'):
    n.children=[x for x in n.children if isinstance(x,Node) and x.has('al-panel-meta')]
   elif n.has('al-badge') and not n.has('al-sim'):remove(panel,n)
   elif n.has('al-sim'):n.children=['模拟数据 · 不代表真实贡献']
   elif n.tag=='summary':n.children=['查看明细']
  panel.children+=fragment(f'<footer class="lp-caption"><h4 id="{id}-caption">图 4-1-{i} {E(title)}</h4></footer>')
  if i==1:panel.children+=fragment('<details class="lp-source" id="land-evidence"><summary>口径与来源</summary>'+''.join(para(n) for n in NOTES)+'</details>')
 out=['<section class="chapter-section lp-section" id="ch04-s01"><div class="lp-topline"><span>4.1 / A-LANDSCAPE</span><button type="button" data-al-theme aria-pressed="false">切换深色</button></div><h2>4.1 '+E(TITLE)+'</h2>',para(INTRO),para('研究问题：'+QUESTION),para('指标定位：'+POSITION,'lp-position'),para('核心发现：'+FINDING)]
 ids=[['al-agent','al-model'],['al-category-rank','al-category-heat','al-category-trend','al-project-rank'],['al-concentration','al-shift'],['al-country-rank','al-country-detail','al-country-stack','al-specialization','al-country-trend']]
 for i,(anchor,title,ps) in enumerate(STORIES):
  out += [f'<section class="al-section lp-story" id="{anchor}"'+(' data-atlas-version="4.1-atlas-v1"' if i==0 else '')+'><h3>'+E(title)+'</h3>',para(ps[0])]
  for j,id in enumerate(ids[i]):
   out.append(panels[id].html())
   if i==1 and j==0:out.append(interpretation(ps[1]))
   if i==1 and j==2:out.append(para(HISTORY_NOTE))
   if i==2 and j==0:out.append(interpretation(ps[1]))
   if i==3 and j==2:out.append(interpretation(ps[1]))
  out += [interpretation(ps[-1]),'</section>']
 out += ['<section class="al-section lp-story" id="land-action"><h3>'+E(ACTION_TITLE)+'</h3>']
 for title,body in ACTIONS:out += ['<h4 class="lp-action">'+E(title)+'</h4>',para(body)]
 out += [para(BRIDGE),'</section></section>']
 for n in list(root.children):
  if isinstance(n,Node) and n.attrs.get('id')=='gosl-overview':root.children[root.children.index(n):root.children.index(n)+1]=fragment(opening())
 at=root.children.index(old);root.children[at:at+1]=fragment(''.join(out))
 return tree.root.html()
def manuscript():
 return '\n\n'.join([CHAPTER_TITLE,CHAPTER_QUESTION,CHAPTER_INTRO,*[h+'。'+b for h,b in CHAPTER_OBSERVATIONS],*[t+' '+d for t,d in TOPICS],PERIOD,TITLE,INTRO,QUESTION,POSITION,FINDING,HISTORY_NOTE,*[x for _,h,ps in STORIES for x in [h,*ps]],*[t for _,t in FIGURES],ACTION_TITLE,*[h+'。'+t for h,t in ACTIONS],BRIDGE,*NOTES])
