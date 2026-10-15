"""A-Landscape sample: distinct annual and current cohorts, pinned evidence."""
from pathlib import Path
import csv,json,html,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];DIR=ROOT/'content/landscape'
E=lambda x:html.escape(str(x),quote=True)
P=json.loads((DIR/'provenance.json').read_text());REF=P['landscape_commit'];REPORTREF=P['report_commit']
REPO='https://github.com/antgroup/agentic-ai-landscape/blob/'+REF+'/'
REPORT='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/'+REPORTREF+'/'
SECTIONS=[
('Agentic coding','编码代理','application','把需求转化为代码、变更与测试，提供人机协作的任务入口。'),
('Coding workflows & harnesses','编码工作流与工具链','application','组织编码任务的上下文、规则与执行流程。'),
('Personal AI assistants','个人助手','application','围绕个人任务、日常工具和持续上下文提供协助。'),
('Chatbot workspaces','聊天工作区','application','以对话和工作区承载模型、知识与工具的交互。'),
('Multi-agent orchestration','多代理编排','framework','组织多个 Agent 的角色、任务分工与交接。'),
('Workflow & agent builders','工作流与代理构建','framework','用可视化或声明式流程连接任务、模型和工具。'),
('Code-first frameworks','代码优先框架','framework','为开发者提供构建 Agent 应用的程序接口与框架。'),
('Memory, knowledge & context','记忆、知识与上下文','runtime','组织可检索知识、长期记忆和任务状态。'),
('Protocols & interoperability','协议与互操作','runtime','定义 Agent、工具及界面之间可共同使用的接口。'),
('Tools, web & computer use','工具与计算机使用','runtime','把模型输出连接到浏览器、业务工具与可执行动作。'),
('Development sandboxes','开发沙箱','runtime','为代码执行提供环境、隔离与生命周期管理。'),
('Observability & evaluation','可观测与评估','runtime','记录执行过程、评估任务结果并定位失败。'),
('Model API gateways','模型 API 网关','model','模型调用入口、路由与接入管理。'),
('Serving · Deploy','服务部署','model','组织模型服务的部署和运行。'),
('Serving · Inference','推理引擎','model','支撑模型推理执行与资源效率。'),
('Post-Train · RL & environments','强化学习与环境','model','为后训练提供交互环境与强化学习工具。'),
('Post-Train · Supervised fine-tuning','监督微调','model','支持模型的任务适配和监督训练。'),
('Pre-Train · Framework & parallel','训练框架与并行','model','承载训练计算与分布式执行。'),
('Pre-Train · Evaluation & observability','训练评估与观测','model','观察训练过程、实验与模型行为。'),
('Pre-Train · Robotics infra','机器人基础设施','model','为具身任务提供训练和开发工具。'),
('Pre-Train · Compiler & accelerator','编译器与加速','model','连接模型计算与底层硬件。'),
('Data · Labeling','数据标注','model','组织训练数据的标注与质量过程。'),
('Data · Integration','数据集成','model','连接和处理模型工作流中的数据。'),
('Data · Governance','数据治理','model','维护数据结构、版本与可管理性。'),
('Compute & scheduling','计算与调度','model','为模型计算组织资源、调度和运行管理。')]
STAGES={'application':('任务入口','面向使用者，把目标带入系统。'),'framework':('构建与编排','把任务拆解为可组织、可接续的执行过程。'),'runtime':('运行与治理','为行动提供上下文、接口、隔离和证据。'),'model':('模型基础设施','为任务执行供应数据、训练、推理与计算能力。')}
SECMAP={s[0]:{'name':s[1],'stage':s[2],'description':s[3]} for s in SECTIONS}
def rows(file):return list(csv.DictReader((DIR/'data'/file).open(encoding='utf-8-sig')))
def rf(prefix):return next((DIR/'data').glob(prefix+'*')).name
FILES={k:rf('fig-4-1-'+str(i)+'_') for i,k in enumerate(['annual','monthly','subfields','countries','scatter'],1)}
FILES['canonical']='agentic-ai-projects.csv';FILES['study']='collaboration-thread-estimates-bootstrap-2026.csv'
R={k:rows(v) for k,v in FILES.items()}
NAMES=json.loads((DIR/'names.json').read_text());LOGOS=json.loads((DIR/'logos.json').read_text());annual={r['repo_id']:r for r in R['annual']};canonical={r['repo_id']:r for r in R['canonical']}
def number(x):return float(x) if x not in ('',None) else None
PROJECTS=[]
for r in R['canonical']:
 if r['landscape_action'] not in ['keep','add']:continue
 sec=SECMAP[r['landscape_section']];owner=r['repo_name'].split('/')[0].lower();logo=LOGOS.get(owner);logo=logo if logo and (DIR/'logos'/logo).exists() else None
 PROJECTS.append({'id':r['repo_id'],'repo':r['repo_name'],'name':NAMES.get(r['repo_name'].lower(),r['repo_name'].split('/')[-1]),'description':r['description'],'layer':r['landscape_layer'],'section':r['landscape_section'],'stage':sec['stage'],'reason':r['selection_reason'],'caveat':r['selection_caveat'],'license':r['license'],'language':r['language'] or '未标注','created':r['created_at'],'pushed':r['pushed_at'],'aug':number(r['openrank_2608']),'jul':number(r['openrank_2607']),'participantsJuly':number(r['participants_2607']),'trend':json.loads(r['openrank_trend_2509_2608'] or '[]'),'annual':number(annual.get(r['repo_id'],{}).get('total_openrank')),'logo':logo})
PROJECTS.sort(key=lambda r:(list(SECMAP).index(r['section']),-(r['aug'] or 0),r['repo']))
UNMATCHED=[r for r in R['annual'] if r['repo_id'] not in canonical]
PAYLOAD={'projects':PROJECTS,'sections':SECMAP,'stages':STAGES,'report':{k:R[k] for k in ['annual','monthly','subfields','countries','scatter']},'source':REPO,'files':FILES,'sourceReport':REPORT,'unmatched':UNMATCHED}
def link(url,label):return f'<a href="{E(url)}">{E(label)}</a>'
def source(k):return (REPO+('insights/260912_open_collaboration_ai/research/' if k=='study' else 'data/') if k in ('canonical','study') else REPORT+'data/processed/chapter4/')+FILES[k]
def actions(k):return '<div class="land-actions">'+link('/assets/landscape/data/'+FILES[k],'原始 CSV ↓')+link(source(k),'固定版本底表 ↗')+'</div>'
def table(rr):
 keys=list(rr[0]);return '<div class="reader-table-wrap"><table class="reader-table"><thead><tr>'+''.join('<th scope="col">'+E(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(r[k] or '—')+'</td>' for k in keys)+'</tr>' for r in rr)+'</tbody></table></div>'
def fulltable(k,title='查看完整底表'):return '<details class="land-table"><summary>'+title+f' · {len(R[k])} 行</summary>'+table(R[k])+actions(k)+'</details>'
def finding(n,title,body):return f'<div class="land-finding"><span>{n}</span><div><h3>{title}</h3><p>{body}</p></div></div>'
def staticmap():
 out=[]
 for stage in ['application','framework','runtime']:
  out.append(f'<section class="land-stage"><div class="land-stage-title"><b>{STAGES[stage][0]}</b><span>{STAGES[stage][1]}</span></div><div class="land-zones">')
  for key,zh,st,desc in SECTIONS:
   if st!=stage:continue
   projects=[p for p in PROJECTS if p['section']==key];out.append(f'<div class="land-zone"><h4>{zh}<small>{len(projects)}</small></h4><p>{desc}</p><div class="land-chips">')
   for p in projects:out.append('<a href="https://github.com/'+E(p['repo'])+'">'+E(p['name'])+'</a>')
   out.append('</div></div>')
  out.append('</div></section>')
 return ''.join(out)
def gallery():
 out=['<details class="land-original"><summary>对照原图 · 5 幅附件图与 2 张仓库全景图</summary><p>原图保留原有样本与制作时点。最新项目数量按主表重新计算，图中 logo 和旧说明不作为实时统计。</p><div class="land-gallery">']
 for i in P['draft_images']:out.append(f'<figure><a href="/assets/landscape/original/{i["file"]}" target="_blank" rel="noopener"><img loading="lazy" src="/assets/landscape/original/{i["file"]}" width="{i["width"]}" height="{i["height"]}" alt="4.1 初稿第 {i["page"]} 页原图"></a><figcaption>附件第 {i["page"]} 页 · 点击查看原尺寸</figcaption></figure>')
 for name in ['landscape_agent_infra.png','landscape_model_infra.png']:out.append(f'<figure><a href="/assets/landscape/original/{name}" target="_blank" rel="noopener"><img loading="lazy" src="/assets/landscape/original/{name}" alt="仓库全景原图 {name}"></a><figcaption>'+link(REPO+'insights/260527-agentic_landscape/'+name,'仓库全景原图与来源 ↗')+'</figcaption></figure>')
 return ''.join(out)+'</div></details>'
def chapter(lang):
 m=json.loads((ROOT/'content/manifest.json').read_text());ch=m['chapters'][3]
 if lang!='zh':
  intro='<div class="reader-note">Section 4.1 is available as a Chinese interactive sample. Annual report evidence and the newer repository landscape are kept separate.</div><section id="ch04-s01"><h2>4.1 Agentic AI landscape</h2>'+link('/2026/zh/chapters/04/#ch04-s01','Read the interactive sample →')+'</section>'
  return intro+''.join(f'<section class="chapter-section" id="{s["id"]}"><h2>{E(s["number"]+" "+s["title"][lang])}</h2><p>This section retains its outline and source manuscript.</p>'+link(REPORT+s['source_path'],'View source manuscript ↗')+'</section>' for s in ch['sections'][1:])
 out=['<div class="goso-chapter land-chapter"><p class="reader-note">GOSL 样章 · 本轮聚焦 4.1；4.2—4.6 保留章节入口，后续按样章经验推进。</p><section class="land-intro"><span class="eyebrow">GOSL / FROM RANKINGS TO ECOSYSTEM STRUCTURE</span><h2>从项目位次，走向技术结构。</h2><p>第三章辨识关键参与者，第四章把项目放回技术链条：它解决什么问题，依赖哪些公共能力，又如何形成可持续的协作。Agentic AI 是本章的第一个观察窗口。</p></section><section class="chapter-section" id="ch04-s01"><div class="section-topline"><span>4.1 / A-LANDSCAPE</span><span>交互样章 · 内容评审稿</span></div><h2>Agentic AI 全景洞察</h2><p class="land-thesis">任务入口在扩展，<br>竞争正延伸到执行与协作的基础设施。</p><p class="land-lede">编码代理构成年度样本的最大方向；但要把模型带入持续工作的场景，还需要编排、上下文、工具、隔离与评估。本节结合年度数据和近期全景，把“谁更受关注”推进到“哪些能力正在形成生态”。</p>']
 total=sum(float(x['2026']) for x in R['subfields']);first=float(R['subfields'][0]['2026'])/total*100;four=sum(float(x['2026']) for x in R['subfields'][:4])/total*100
 out.append('<div class="land-kpis">'+''.join(f'<div><strong>{v}</strong><span>{label}</span><small>{note}</small></div>' for v,label,note in [('69','年度核心项目','2025.07 — 2026.06'),('12','年度技术方向','报告分类口径'),(f'{first:.1f}%','编码代理影响力占比','分母：12 类 OpenRank 合计'),(f'{four:.1f}%','前四类方向合计占比','编码 / 助手 / 框架 / 构建')])+'</div>')
 out.append('<nav class="land-jump" aria-label="4.1 阅读路径">'+''.join(link('#land-'+k,title) for k,title in [('map','① 看懂全景'),('annual','② 查验年度变化'),('cases','③ 理解结构变化'),('action','④ 形成行动'),('evidence','证据与待补')])+'</nav>')
 out.append('<div class="land-window"><div><b>年度证据</b><p>报告仓库：69 个核心项目、12 个技术方向，2025 年 7 月—2026 年 6 月；用于年度结构与月度变化。</p></div><div><b>近期全景</b><p>Landscape 主表固定至 2026-09-27 提交，选入 Agent Infra 86 个、Model Infra 59 个；最新月度指标为 2026 年 8 月。它是分类与案例补充，不改写年度样本。</p></div></div>')
 out.append('<section id="land-map" class="land-block"><span class="eyebrow">01 / EXPLORE THE STACK</span><h3 class="land-heading">先看能力之间的位置，再看项目。</h3><p>仓库将 Agent Infra 分为任务入口、构建与编排、运行与治理；Model Infra 提供数据、训练、推理及调度能力。下面是项目分类图，不是产品优劣排名，也不表示这些项目存在已经验证的直接依赖关系。</p><noscript><p>交互图表需要启用 JavaScript；下方全景中的仓库链接、完整数据表和 CSV 下载仍可使用。</p></noscript><div class="land-explorer"><div class="land-controls" id="land-controls" hidden></div><p id="land-map-status" class="land-status" aria-live="polite">Agent Infra · 86 个精选项目 · 点击项目查看 GitHub</p><div id="land-map-grid">'+staticmap()+'</div><div class="land-empty" id="land-map-empty" hidden>没有匹配项目。请清空搜索或更换分层。</div><p class="land-scope">选入规则：主表的 landscape_action 为 keep 或 add。每个项目按仓库指定的一个主要分区展示；未入选不等于没有价值。图标沿用仓库的所有者标识，名称用于区分项目。NOASSERTION 表示许可证元数据未给出明确标识，不是许可结论。</p>'+actions('canonical')+'</div><dialog id="land-project-dialog" aria-labelledby="land-project-title"><button class="land-dialog-close" type="button" aria-label="关闭项目详情">×</button><div id="land-project-detail"></div></dialog></section>')
 out.append('<section id="land-annual" class="land-block"><span class="eyebrow">02 / ANNUAL EVIDENCE</span><h3 class="land-heading">结构集中，与头部换位同时发生。</h3>')
 out.append(finding('A','编码代理占年度样本的 37.6%，前四类占 75.0%','报告子领域表中，编码代理 OpenRank 为 28,176.2；个人助手、代码优先框架、工作流与代理构建构成其后的主要方向。占比描述的是本报告的核心样本，不是全部 Agentic AI 项目，也不是市场份额。'))
 out.append('<article class="land-panel" id="land-field-panel"><div class="land-panel-head"><h4>技术方向：规模与五年变化</h4><p>选择年度或点击技术方向，查看 2022—2026 的对应数值。历史零值保留，不把零值视为该技术尚不存在。</p></div><div class="land-controls" hidden><label>报告年度<select id="land-field-year">'+''.join(f'<option {"selected" if y==2026 else ""}>{y}</option>' for y in range(2022,2027))+'</select></label><label>显示方式<select id="land-field-mode"><option value="absolute">OpenRank 原值</option><option value="share">占当年 12 类合计</option></select></label></div><div id="land-field-chart" class="land-chart"></div><p id="land-field-detail" class="land-readout" aria-live="polite">选择图中的技术方向，查看年度变化。</p><div id="land-field-trend" class="land-chart land-mini"></div>'+actions('subfields')+fulltable('subfields')+'</article>')
 out.append(finding('B','同一组头部项目，领先者随月份改变','所列 10 个项目中，2025 年 7 月 Claude Code 为 636.5；2026 年 3 月 OpenClaw 达到 1,871.7；到 6 月 OpenClaw 为 592.2，Hermes Agent 为 518.9。月度图支持头部换位的观察，但无法单凭这一变化确定产品机制、采用规模或收入增长。'))
 out.append('<article class="land-panel" id="land-month-panel"><div class="land-panel-head"><h4>头部项目月度变化</h4><p>固定 10 个项目的 12 个月数据，不是每月重新选出的 Top 10。切换热力表与趋势线；曲线最多同时比较 6 个项目。</p></div><div class="land-controls" hidden><label>图表形式<select id="land-month-mode"><option value="heat">月度热力表</option><option value="trend">项目趋势线</option></select></label></div><div id="land-month-legend" class="land-legend"></div><div id="land-month-chart" class="land-chart"></div><p id="land-month-detail" class="land-readout" aria-live="polite">聚焦单元格或曲线节点，可查看对应月份与数值。</p>'+actions('monthly')+fulltable('monthly')+'</article>')
 out.append('<details class="land-secondary"><summary>进一步核对：国家贡献与双口径散点图</summary><p>以下两张表保留原稿的重要观察方向，但字段说明尚不完整。国家表按同一子领域原值比较；散点图横轴使用 Project OpenRank、纵轴使用原字段 OpenRank，两者不作为同一个指标相除或合成评分。</p><article class="land-panel"><h4>技术子领域的 Top 3 国家</h4><div class="land-controls" hidden><label>技术方向<select id="land-country-field">'+''.join('<option>'+E(r['子领域'])+'</option>' for r in R['subfields'])+'</select></label></div><div id="land-country-chart" class="land-chart"></div><p class="land-scope">原稿称“国家贡献 OpenRank”；具体聚合对象、位置归属和归一化规则待补。当前只有 Top 3，不推算全球占比，也不把多个子领域相加。</p>'+actions('countries')+fulltable('countries')+'</article><article class="land-panel"><h4>项目双口径关联分布 · 12 个头部样本</h4><div id="land-scatter-chart" class="land-chart"></div><p id="land-scatter-detail" class="land-readout" aria-live="polite">横纵轴均使用对数尺度，原始数值见底表。纵轴 OpenRank 的汇总规则待确认，暂不据此判断生产效率、因果关系或贡献质量。</p>'+actions('scatter')+fulltable('scatter')+'</article></details></section>')
 out.append('<section id="land-cases" class="land-block"><span class="eyebrow">03 / FROM PROJECTS TO CAPABILITIES</span><h3 class="land-heading">比“下一个热门项目”更持久的，是执行所需的公共能力。</h3><p>仓库的阶段研究与项目自述提示了三条值得跟踪的变化。下面是对材料的研究解读，不能替代采用率或技术成熟度测量。</p><div class="land-case-grid">')
 for title,body,names,path in [
 ('从编码助手到任务环境','编码入口之外，工具链、沙箱与编排开始成为独立分区。竞争问题从“能否生成代码”延伸到“能否保留上下文、控制执行并验证结果”。',['Claude Code','Codex','OpenCode'],'insights/260527-agentic_landscape/260527_agentic_ai_cn.md'),
 ('从知识检索到持续上下文','记忆、知识与上下文被单列为运行能力。重点不是把所有 RAG 工具改名为 Agent，而是观察状态、检索和长期任务如何连接。',['RAGFlow','OpenViking','Milvus'],'insights/case_studies/05-AI-Memory-Evolution.md'),
 ('从搭建工作流到组织协作','代码优先框架、工作流构建与多代理编排对应不同开发方式。项目定位的变化可以提示生态方向，却不能直接证明可靠性或更低成本。',['Dify','LangChain','Deer Flow'],'insights/260527-agentic_landscape/260527_agentic_ai_cn.md')]:
  out.append('<article><h4>'+title+'</h4><p>'+body+'</p><small>'+E(' · '.join(names))+'</small><p>'+link(REPO+path,'阅读仓库研究原文 ↗')+'</p></article>')
 out.append('</div><div class="land-runtime"><h4>沿着执行过程，检查五类运行能力</h4><p>这是阅读与评审路径，不是强制架构或成熟度评分。点击能力，可回到全景查看对应项目。</p><div>'+''.join(f'<button type="button" data-runtime="{E(key)}"><b>{i+1:02d} / {label}</b><span>{desc}</span></button>' for i,(key,label,desc) in enumerate([('Memory, knowledge & context','上下文','任务需要记住什么？'),('Protocols & interoperability','接口','各系统如何互通？'),('Tools, web & computer use','行动','如何进入真实工具？'),('Development sandboxes','隔离','执行边界在哪里？'),('Observability & evaluation','证据','如何知道完成得好不好？')]))+'</div></div>')
 out.append('<article class="land-study"><span class="eyebrow">SUPPLEMENT / COLLABORATION EVIDENCE</span><h4>有 Agent 参与，不等于 Agent 独立完成协作。</h4><p>仓库另一项研究在 100 个仓库中各抽取 50 条 Issue/PR，形成 5,000 条线程样本（2026 年 1—8 月）。补充证据帮助本报告从协作影响力进一步追问：谁在发起、谁在响应、谁在审阅？</p><div class="land-study-grid">')
 for metric,title in [('agent_participation_present','可见 Agent 参与'),('agent_participation_opened_thread','Agent 发起线程'),('agent_review_event_present','PR 中可见 Agent review')]:
  r=next(x for x in R['study'] if x['metric']==metric);out.append(f'<div><strong>{float(r["point_estimate"])*100:.2f}%</strong><b>{title}</b><small>样本分母 {int(r["eligible_threads"]):,} · 95% 区间 {float(r["ci_low_95"])*100:.2f}%—{float(r["ci_high_95"])*100:.2f}%</small></div>')
 out.append('</div><p class="land-scope">公开可见参与不是 AI 生成代码比例，也不能捕获未披露的本地 AI 使用。样本按仓库等额抽取，不代表全生态流量；区间描述所选仓库内的抽样不确定性。此项研究与年度 69 项目样本分开，不据此宣称生产率提升。</p>'+actions('study')+link(REPO+'insights/260912_open_collaboration_ai/research/research-question-evidence-matrix.md','查看研究问题、证据和因果边界 ↗')+'</article></section>')
 out.append('<section id="land-action" class="land-block"><span class="eyebrow">04 / IMPLICATIONS FOR OPEN DEVELOPMENT</span><h3 class="land-heading">把开放的优势，落实为可验证、可复用的能力。</h3><div class="land-action-grid">'+''.join('<article><span>'+who+'</span><h4>'+title+'</h4><p>'+body+'</p><small>'+goal+'</small></article>' for who,title,body,goal in [
 ('维护者与技术建设者','让执行有边界，让结果有证据','优先完善机器可读接口、测试、故障恢复、观测与贡献规则；在影响力之外，持续跟踪维护负担与外部贡献的完成情况。','连接 OSDGs：可持续性与协作质量'),
 ('企业与采用方','按任务验收，按系统评估','从结果可验证的工作流开始，以任务完成、人工接管、成本和失败恢复检验系统；项目热度作为候选线索，不替代采用验证。','连接 OSDGs：可获得性与实际使用能力'),
 ('产业组织与公共部门','支持可共同使用的基础能力','关注互操作协议、公开评测、数据与工具适配，让不同规模的团队能够参与、迁移和改造，降低对单一入口的依赖。','连接 OSDGs：包容性、多样性与公共价值')])+'</div><p>'+link('/2026/zh/chapters/01/#ch01-s02','回到第一章 OSDGs 目标框架 →')+'</p></section>')
 out.append('<section id="land-evidence" class="land-block"><span class="eyebrow">EVIDENCE / REVIEW NOTES</span><h3 class="land-heading">来源、边界与本轮待补</h3><p>报告年度值与近期仓库数据均固定到明确提交；CSV 原样保留。全景使用主表筛选，未沿用旧研究文本或衍生导出中的历史项目数量。</p><ol><li><strong>样本映射：</strong>69 个年度项目有 66 个可按 repo_id 对齐近期主表，另 3 个保留待补；近期分类不回填历史年度统计。</li><li><strong>月度总量：</strong>已入库月度表只含 10 个项目，不能复算原稿的全景月总量。因此本版暂不采用“3 月整体 8,413”及“OpenClaw 占整体 22.2%”等依赖全量分母的判断。</li><li><strong>第二种 OpenRank：</strong>国家表与散点表的汇总对象、归一化及完整样本待补；暂不合成评分，也不扩写全池贡献总量。</li><li><strong>历史窗口：</strong>补齐 2022—2025 年度字段的精确起止日及样本边界，之后再深化跨年可比解释。</li></ol><details><summary>待对齐的 3 个年度项目</summary>'+table(UNMATCHED)+'</details>'+fulltable('annual','年度 69 个核心项目清单')+gallery()+'<p>'+link('/assets/landscape/provenance.json','完整来源与 SHA-256 清单 ↓')+' · '+link(REPO+'README.md','Landscape 仓库说明 ↗')+' · '+link('/2026/zh/chapters/03/','返回 GOSR →')+'</p></section></section>')
 for s in ch['sections'][1:]:out.append(f'<section class="chapter-section land-pending" id="{s["id"]}"><div class="section-topline"><span>{s["number"]}</span><span>后续章节入口</span></div><h2>{E(s["title"]["zh"])}</h2><p>{E(s["question"]["zh"])}</p>'+link(REPORT+s['source_path'],'阅读仓库初稿 ↗')+'</section>')
 out.append('<script id="landscape-data" type="application/json">'+json.dumps(PAYLOAD,ensure_ascii=False).replace('<','\\u003c')+'</script></div>')
 return ''.join(out)
def export(out):shutil.copytree(DIR,out/'assets/landscape',dirs_exist_ok=True)
