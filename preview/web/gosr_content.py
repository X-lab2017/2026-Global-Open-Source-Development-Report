"""GOSR: pinned repository evidence, editorial interpretation and native charts."""
from pathlib import Path
import csv,html,json,shutil
from goso_brand import css,resolve
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'content/gosr'
PROV=json.loads((DIR/'provenance.json').read_text())
REF=PROV['commit']; REPO='https://github.com/'+PROV['repository']+'/blob/'+REF+'/'
E=lambda x:html.escape(str(x),quote=True)
LABELS={'rank':'原榜名次','province':'行政区（英文）','province_zh':'省级行政区','country':'国家（英文）','country_zh':'国家','developer_count_10k':'开发者数量（万）','city':'城市','company':'企业（英文）','company_zh':'企业','openrank':'OpenRank','active_repos':'活跃仓库数','active_developers':'活跃开发者数','foundation':'基金会（英文）','foundation_zh':'基金会','project':'项目','initiator_zh':'发起组织','entries_in_top100':'入榜行政区数量','representative_divisions':'代表行政区','projects_in_top100':'入榜项目数量','representative_projects':'代表项目','repo':'仓库','platform':'平台','created_at':'创建日期','repo_count':'仓库数量','first_repo_created_at':'首个仓库创建日期','domain':'技术领域','share_pct':'占比（%）','openrank_sum':'OpenRank 合计','language':'主要语言','model_id':'模型','publisher':'发布者','country_code':'国家编码','task':'任务','modelrank_value':'ModelRank','model_url':'模型地址','models':'模型数','model_series':'模型系列','ranked_versions':'入榜版本','cur_rank':'本期名次','prev_rank':'基期名次','rank_delta':'位次变化','year':'年度标签','month':'月份'}
# File prefix, title, label field, metric fields. Nothing is re-ranked at ingestion.
SPECS=[
('region','table-3-1-1','全球行政区 Top 30','province_zh',['openrank','developer_count_10k']),
('province','table-3-1-3','中国省级行政区 Top 30','province_zh',['openrank','developer_count_10k']),
('city','table-3-1-4','中国城市 Top 30','city',['openrank','developer_count_10k']),
('regionCountries','table-3-1-2','全球行政区 Top 100 · 国家分布','country_zh',['entries_in_top100']),
('company','table-3-2-1','全球企业 Top 30','company_zh',['openrank','active_repos','active_developers']),
('chinaCompany','table-3-2-2','中国企业 Top 30','company_zh',['openrank','active_repos','active_developers']),
('foundation','table-3-3-1','全球基金会 · 21 家','foundation_zh',['openrank','active_developers']),
('project','table-3-4-1','全球项目 Top 30','project',['openrank','active_developers']),
('chinaProject','table-3-4-3','中国项目 Top 30','project',['openrank','active_developers']),
('projectCountries','table-3-4-2','全球项目 Top 100 · 发起组织国家分布','country_zh',['projects_in_top100']),
('newRepo','table-3-5-1','新创建仓库 Top 30','repo',['openrank','active_developers']),
('newProject','table-3-5-2','新创立项目 Top 30','project',['openrank','active_developers','repo_count']),
('domains','table-3-5-3','新仓库 Top 30 · 技术领域','domain',['repo_count','openrank_sum']),
('languages','table-3-5-4','新仓库 Top 30 · 主要语言','language',['repo_count']),
('models','fig-3-6-1','模型影响力 Top 20','model_id',['modelrank_value']),
('publishers','fig-3-6-2','模型 Top 20 · 发布者分布','publisher',['models']),
('tasks','fig-3-6-3','模型 Top 20 · 任务分布','task',['models']),
('series','table-3-6-1','Qwen 与 Llama · 系列分布','model_series',['models']),
]
def read(prefix):
 p=next((DIR/'data').glob(prefix+'_*'));return p.name,list(csv.DictReader(p.open()))
def datasets():
 out={}
 for key,prefix,title,label,metrics in SPECS:
  file,rows=read(prefix);out[key]={'id':key,'file':file,'title':title,'label':label,'metrics':metrics,'rows':rows,'period':'2026 年 8 月 · ModelRank v1' if key in ('models','publishers','tasks','series') else '2025.07 — 2026.06','kind':'bars'}
 for key,prefix,title in [('globalYear','fig-3-2-1','全球企业 · 年度位次'),('globalMonth','fig-3-2-2','全球企业 · 月度位次'),('chinaYear','fig-3-2-3','中国企业 · 年度位次'),('chinaMonth','fig-3-2-4','中国企业 · 月度位次'),('foundationMonth','fig-3-3-1','基金会 · 月度位次')]:
  file,rows=read(prefix);out[key]={'id':key,'file':file,'title':title,'rows':rows,'kind':'history','period':'2016—2026 年度标签；2026 为本报告统计期' if 'Year' in key else '2025.07 — 2026.06'}
 return out
DATA=datasets()
def fmt(x):
 try:return f'{float(x):,.2f}'.rstrip('0').rstrip('.') if '.' in str(x) else f'{int(x):,}'
 except (ValueError,TypeError):return str(x) if x not in ('',None) else '—'
def display(x):return str(x).replace('GitCode','AtomGit')
def table(rows):
 keys=list(rows[0]);return '<div class="reader-table-wrap"><table class="reader-table"><thead><tr>'+''.join('<th scope="col">'+E(LABELS.get(k,k))+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(fmt(display(r[k])))+'</td>' for k in keys)+'</tr>' for r in rows)+'</tbody></table></div>'
def svg(d):
 if d['kind']=='history':return ''
 metric=d['metrics'][0];rows=sorted(d['rows'],key=lambda r:float(r[metric]),reverse=True)[:10];maximum=max(float(r[metric]) for r in rows) or 1
 bits=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {60+len(rows)*42}" role="img" aria-label="{E(d["title"])}"><title>{E(d["title"])} · {E(LABELS.get(metric,metric))}</title><rect width="100%" height="100%" fill="{css("surface")}"/>']
 for i,r in enumerate(rows):
  y=22+i*42;name=display(r[d['label']]);short=name if len(name)<29 else name[:26]+'…';v=float(r[metric]);bits.append(f'<g><title>{E(name)}：{fmt(v)}</title><text x="260" y="{y+17}" text-anchor="end" font-family="sans-serif" font-size="13" fill="{css("ink")}">{E(short)}</text><rect x="276" y="{y}" width="{v/maximum*490:.2f}" height="25" rx="3" fill="{css("s0")}"/><text x="{288+v/maximum*490:.2f}" y="{y+17}" font-family="sans-serif" font-size="12" fill="{css("ink")}">{fmt(v)}</text></g>')
 bits.append('</svg>');return ''.join(bits)
def panel(pid,keys,title,note):
 d=DATA[keys[0]];history=d['kind']=='history'
 return f'''<article class="gosr-panel" id="{pid}" data-boards="{','.join(keys)}"><div class="gosr-panel-head"><span class="eyebrow">GOSR / {'RANK TRAJECTORY' if history else 'EVIDENCE EXPLORER'}</span><h3>{E(title)}</h3><p>{E(note)}</p></div><div class="gosr-controls" hidden></div><p class="gosr-context">{E(d['title'])} · {E(d['period'])}</p><div class="gosr-legend"></div><div class="gosr-plot">{svg(d)}</div><p class="gosr-readout" aria-live="polite">悬停或键盘聚焦图中对象，查看精确数值。</p><div class="gosr-actions"><a class="gosr-csv" href="/assets/gosr/data/{d['file']}" download>原始 CSV ↓</a><a class="gosr-source" href="{REPO}data/processed/chapter3/{d['file']}">GitHub 底表 ↗</a><button class="gosr-svg" type="button" hidden>当前图 SVG ↓</button></div><details class="gosr-table"><summary>查看完整底表 · {len(d['rows'])} 行</summary><div class="gosr-table-content">{table(d['rows'])}</div></details><noscript><p>交互需要 JavaScript；完整底表与 CSV 可直接阅读。</p></noscript></article>'''
def gallery(section):
 imgs=[i for i in PROV['images'] if i['section']==section]
 return '<details class="gosr-original"><summary>查看附件原图 · '+str(len(imgs))+' 幅（历史稿件，数值以本页底表为准）</summary><div class="gosr-gallery">'+''.join(f'<figure><a href="/assets/gosr/original/{i["file"]}" target="_blank" rel="noopener"><img loading="lazy" width="{i["width"]}" height="{i["height"]}" src="/assets/gosr/original/{i["file"]}" alt="{E(i["source"])} 第 {i["page"]} 页原图，点击查看大图"></a><figcaption>附件第 {i["page"]} 页 · 点击打开原尺寸</figcaption></figure>' for i in imgs)+'</div></details>'
def finding(k,title,text):return f'<div class="gosr-finding"><span>{k}</span><div><h3>{title}</h3><p>{text}</p></div></div>'
def implications(text,limit):return f'<div class="gosr-implications"><h3>从发现到行动</h3><p>{text}</p><p class="gosr-limit"><strong>解释边界：</strong>{limit}</p></div>'
def chapter(lang):
 if lang!='zh':return '<div class="reader-note">The GOSR review draft is now available in Chinese, with six ranking dimensions, source tables and interactive comparisons. English editorial translation will follow the Chinese review.</div><p id="gosr-review"><a href="/2026/zh/chapters/03/#gosr-review">Review the evidence gaps →</a></p><p><a href="/2026/zh/chapters/03/">Read the interactive GOSR chapter →</a></p>'+''.join(f'<section id="ch03-s0{i}"><h2>{i}. {name}</h2><a href="/2026/zh/chapters/03/#ch03-s0{i}">Read this section →</a></section>' for i,name in enumerate(['Regions','Companies','Foundations','Projects','Emerging projects','Models'],1))
 out=['<div class="goso-chapter gosr-chapter"><div class="gosr-intro"><span class="eyebrow">CHAPTER 03 / GLOBAL OPEN SOURCE RANKINGS</span><h2>谁在把贡献，<br>转化为全球影响力？</h2><p class="gosr-lede">从地区到组织，从项目到模型。六个观察窗口，辨识协作网络中的关键节点，以及正在变化的影响力结构。</p><p>GOSO 回答生态分布在哪里，GOSR 进一步追问谁在组织协作、承载贡献与推动复用。本章以 OpenDigger 支持的 OpenRank 为代码生态的主要量尺，以 ModelRank 补充模型复用网络的观察。榜单提供可查证的结构信号，并与第一章 OSDGs 的包容性、可持续性和多样性目标相连接。</p><div class="gosr-period"><span><b>代码生态</b>2025.07 — 2026.06 / OpenRank</span><span><b>模型生态</b>2026.08 / ModelRank v1</span></div></div>']
 cards=[('R','区域','加利福尼亚州','50,883.80','OpenRank'),('C','企业','微软','167,060.26','OpenRank'),('F','基金会','Linux 基金会家族','196,128.27','OpenRank'),('P','项目','OpenHarmony','75,809.42','OpenRank'),('E','新势力','CANN','14,719.47','OpenRank · 项目'),('M','模型','Qwen3.8-27B','27,930.09','ModelRank')]
 out.append('<nav class="gosr-overview" aria-label="六类榜单">'+''.join(f'<a href="#ch03-s0{i}"><span class="gosr-letter">{k}</span><span>{name} / {k}-Ranking</span><strong>{winner}</strong><b>{value}</b><small>{metric} · 本期榜首 →</small></a>' for i,(k,name,winner,value,metric) in enumerate(cards,1))+'</nav>')
 out.append('<p class="gosr-method">六类榜单分别排序，不合成跨对象总榜。OpenRank 不等于治理质量或商业价值；ModelRank 不等于模型能力得分或开放许可证评级。项目按标签聚合仓库，仓库数与项目数不能互换。<a href="/2026/zh/methodology/">查看方法基础 →</a></p>')
 sections=[('R','行政区划','影响力有地理重心，参与规模不是唯一解释。'),('C','开源企业','年度格局相对稳定，月度位次已出现变化。'),('F','开源基金会','头部集中，需要与组织归并口径一起阅读。'),('P','开源项目','基础软件与 AI 工具共同占据影响力前列。'),('E','新势力项目','从仓库冷启动，到有组织的项目供给。'),('M','开源大模型','从单个模型，观察系列复用与任务覆盖。')]
 for i,(tag,name,headline) in enumerate(sections,1):
  out.append(f'<section class="chapter-section gosr-section" id="ch03-s0{i}"><div class="section-topline"><span>3.{i} / {tag}-Ranking</span><span>数据已接入 · 内容评审稿</span></div><h2>{name}影响力排行榜</h2><p class="gosr-thesis">{headline}</p>')
  if i==1:
   out.append(finding('01','规模优势与协作影响，需要分开比较','全球行政区榜中，加利福尼亚州以 50,883.80 居首，英格兰为 36,398.10。北京、上海分别为第 14、16 位。切换“开发者数量”后可以看到：参与规模与 OpenRank 的排序并不相同。扩大参与是基础，持续有效的协作同样值得关注。'))
   out.append(panel('gosr-regions',['region','province','city'],'从全球行政区，到中国省市','选择地理层级与指标。三个榜单独立统计，不把城市与省级行政区合并排序；台湾省及其城市在中国范围内展示。'))
   out.append(finding('02','中国城市榜呈现多中心结构','北京、上海在城市榜居前，杭州以 4,388.79 高于深圳的 3,570.17；台北、广州、成都等城市也进入前列。这个截面支持“多中心”的观察，尚不能单独证明城市位次跨年上升，更不能将城市差异直接归因于某一家企业或某项政策。'))
   out.append(panel('gosr-region-counts',['regionCountries'],'Top 100 中，哪些国家拥有更多入榜行政区？','美国 25 个，印度 12 个，中国 7 个。分母为入榜的 100 个行政区，数量不代表各国 OpenRank 份额，也受行政区划粒度影响。'))
   out.append(implications('地方支持政策可以同时关注参与规模、协作影响与人才培养，进一步核对本地贡献流向哪些项目，再决定资源投入。','省级与城市级位置识别覆盖可能不同；本地底表仅提供各 Top 30，不能用其合计推算全国总量或覆盖率。'))
  elif i==2:
   out.append(finding('01','微软与华为位居前二，投入结构并不相同','微软本期 OpenRank 为 167,060.26，华为为 141,253.65，两者相差 25,806.61。微软的活跃开发者更多，华为的活跃仓库更多。两类规模指标与影响力不能简单互相替代；组织参与开源的方式，是比单一位次更值得追踪的问题。'))
   out.append(panel('gosr-companies',['company','chinaCompany'],'企业榜：位次之外，比较参与结构','按 OpenRank、活跃仓库数或活跃开发者数排序。切换指标只改变当前图的顺序，表格保留原榜名次。'))
   out.append(finding('02','月度领先，不等同于年度领先','底表显示，华为自 2026 年 3 月起在所列月份超过微软；中国企业榜中，字节跳动自 2026 年 4 月起超过阿里巴巴。但本报告年度榜仍分别以微软、阿里巴巴领先。月度图呈现变化发生的时点，年度榜呈现整个统计期的结果，两者并不矛盾。'))
   out.append(panel('gosr-company-history',['globalMonth','globalYear','chinaMonth','chinaYear'],'企业位次轨迹：短期变化与长期位置','默认选取前三个对象；可同时比较最多 8 条轨迹。排名 1 位于上方，空值保留为缺失；坐标范围随选择变化，不截断低位排名。历史年度标签与 2026 统计期的边界仍需补齐说明。'))
   out.append(implications('企业评估可以把持续贡献、开发者参与和项目协作结合起来。对阶段性跃升，优先检查贡献来自哪些项目、能否在多个统计期维持，再讨论战略意义。','数据证明位次变化，不直接证明 AI 投入的因果作用；不以榜单倒推企业商业策略。年度与月度排名不能相加、平均或替代影响力分值。'))
  elif i==3:
   foundation=DATA['foundation']['rows'];share=sum(float(x['openrank']) for x in foundation[:3])/sum(float(x['openrank']) for x in foundation[:10])*100
   out.append(finding('01','Linux 家族领先，前三家占头部样本的大部分','Linux 基金会采用包含子基金会的合并口径，本期 OpenRank 为 196,128.27；开放原子、Apache 随后。前三家合计占 Top 10 基金会 OpenRank 的 '+f'{share:.1f}%'+ '。这个比例描述头部样本的集中程度，不能写成整个开源生态的份额。'))
   out.append(panel('gosr-foundations',['foundation'],'基金会榜：合并口径与参与规模','Linux 家族作为一个汇总对象。不同基金会覆盖的项目规模与组织结构不同，开发者计数也不能直接跨组织相加。'))
   out.append(finding('02','前三家成员稳定，第二、第三位有交换','Linux 家族在 12 个月均居首。开放原子与 Apache 在 2025 年 10 月、2026 年 1 月交换第二、第三位，因此附件中“前三位全年不变”的描述需要修正。稳定的是头部成员，而不是每个月的名次。'))
   out.append(panel('gosr-foundation-history',['foundationMonth'],'基金会月度位次','逐月核对头部稳定性，同时保留第二梯队的名次变化。'))
   out.append(implications('基金会的下一步评价宜补充维护者多样性、治理参与和项目可持续性证据。高影响力项目的集中托管，是观察治理责任的入口。','OpenRank 反映协作网络影响，不足以证明治理质量、治理信任或项目长期健康；子基金会归并清单和开发者去重规则待补。'))
  elif i==4:
   out.append(finding('01','OpenHarmony 居首，AI 基础设施与工具进入前列','OpenHarmony 的 OpenRank 为 75,809.42，约为第二名 Azure（29,382.06）的 2.58 倍。PyTorch 第 4、vLLM 第 7、CANN 第 13，体现了 AI 基础软件在头部项目样本中的位置。榜单也包含开发工具、语言、操作系统等多种项目形态。'))
   out.append(panel('gosr-projects',['project','chinaProject'],'项目榜：全球视野与中国样本','项目为标签聚合对象，可包含多个仓库。表格同时提供活跃开发者与发起组织，帮助辨识项目背后的协作结构。'))
   out.append(finding('02','归属结构，描述的是发起组织而非贡献者国籍','最新仓库底表中，Top 100 项目按发起组织归属，美国 69 个、中国 7 个、未识别 9 个；附件旧表的 63 个美国项目和 13 个未识别项目不再用于新版分析。中国入榜项目包括 OpenHarmony、openEuler、CANN、Ascend、MindSpore、PaddlePaddle、Cangjie。'))
   out.append(panel('gosr-project-countries',['projectCountries'],'Top 100 项目的发起组织国家分布','这是独立提供的 Top 100 汇总表；本页详细项目榜只有 Top 30。未识别归属保留，不按项目名称推断国家。'))
   out.append(implications('公共部门与基金会可关注关键基础软件的持续维护；项目团队可把维护者梯队、治理透明度和跨组织协作作为影响力之后的跟踪问题。','发起组织所在地不代表贡献者所在地，也不等同于控制权或受益范围。项目标签映射和覆盖清单尚需补充，榜单结论限于当前样本。'))
  elif i==5:
   out.append(finding('01','仓库榜与项目榜揭示两种不同的启动路径','openclaw/openclaw 以 7,047.46 位居新仓库榜首，创建日期为 2025 年 11 月 24 日。项目榜首 CANN 的 OpenRank 为 14,719.47，纳入 68 个仓库。单仓库的快速聚集与多仓库的组织化供给，都可能形成影响，但不能按相同对象规模直接比较。'))
   out.append(panel('gosr-emerging',['newRepo','newProject'],'新势力：仓库与项目分榜观察','按原稿定义，新项目要求纳入的仓库均在本期新建；创建日期反映仓库或项目标记的起点，不一定等于技术的诞生时间。'))
   out.append(finding('02','新仓库样本偏向 AI 基础软件','人工标注底表中，AI 基础软件占新仓库 Top 30 的 18 个（60%），AI 智能体与 Agent 工具占 4 个。语言表中 Python 15 个、C++ 12 个。两张分布表分别描述技术方向和主要语言，不能互相替代，也不能外推到全球全部新仓库。'))
   out.append(panel('gosr-emerging-structure',['domains','languages'],'新仓库的技术与语言结构','领域分布采用人工标注复核；计数按仓库，不按项目。OpenRank 合计与仓库数量表达不同信息。'))
   out.append(implications('支持新项目时，可同时跟踪吸引外部协作者的能力、维护连续性与真实复用证据；对集中创建的多仓库项目，需要区分组织供给与外部社区扩展。','“新建”不必然意味着从零研发或技术原创。现有底表不足以判断冷启动机制与持续留存，技术领域分类规则也应随数据版本公开。'))
  else:
   out.append(finding('01','Qwen 的头部位置，体现在多个系列和版本','2026 年 8 月 Top 20 中，Qwen 占 16 席；首位 Qwen3.8-27B 的 ModelRank 为 27,930.09，约为第二位 Qwen3.5-9B-Base 的 1.95 倍。多个系列共同入榜，提示应把版本、派生和复用关系作为连续生态来观察。'))
   out.append(panel('gosr-models',['models'],'模型榜：观察复用网络中的影响','分值来自 OpenGauge ModelRank v1 的 score_normalized：当月归一化 score × 当月模型数量。本期模型数 931,886；分值是数值尺度，不是百分比。'))
   out.append(finding('02','发布者集中，任务覆盖仍有分化','按发布者归属，中国 16 席、美国 4 席；这反映入榜模型的发布者分布，不代表全球模型市场份额。文本生成 11 席、多模态理解 7 席，机器人与图像生成各 1 席。主流任务之外，专门任务也能形成可观察的复用影响。'))
   out.append(panel('gosr-model-structure',['tasks','publishers','series'],'从任务、发布者与系列三个角度看 Top 20','任务数与发布者数均以 Top 20 为分母。系列表仅覆盖 Qwen 与 Llama 的 18 个模型，不包含另两家发布者。'))
   out.append(implications('模型发布者可以完善版本连续性、模型卡与复用路径；使用者还应结合任务能力、许可证和开放属性进行选择。进一步的复用网络与开放性分析将连接 <a href="/2026/zh/chapters/05/#ch05-s02">第五章 GOSM →</a>。','ModelRank 与 OpenRank 的对象、算法与统计期不同，不能相加或同轴比较；分值高不等于性能更强、训练更开放或许可证更宽松。'))
  out.append(gallery(f'3.{i}')+'</section>')
 out.append('''<section class="chapter-section" id="gosr-review"><span class="eyebrow">REVIEW / EVIDENCE & NEXT STEPS</span><h2>本轮审阅，聚焦三个方法缺口</h2><p>已按最新底表修正基金会月度变化、项目归属数量与模型统计期。下面的缺口影响比较解释，集中保留，后续补充后再深化结论。</p><ol><li><strong>对象与覆盖：</strong>企业、基金会、项目的仓库映射版本，跨平台合并及开发者去重规则，Linux 子基金会归并清单。</li><li><strong>历史可比性：</strong>2016—2025 年度标签对应的起止日期；“跃升先锋”表的明确基期。目前不据此扩写跨年因果结论。</li><li><strong>机制证据：</strong>重大位次变化对应的项目或事件，以及新仓库技术分类规则；用来区分观测到的变化与变化原因。</li></ol><p>GitHub 为事实源。本章 25 份 CSV 固定到仓库版本 <code>'''+REF[:12]+'''</code>，下载文件保持原始字节。附件原图仅供稿件对照；数值及统计口径以本版底表和说明为准。</p><p><a href="/assets/gosr/provenance.json">数据与原图来源清单 ↓</a> · <a href="'''+REPO+'''data/README.md">仓库指标与数据说明 ↗</a> · <a href="/2026/zh/chapters/02/">返回 GOSO →</a></p><details><summary>补充底表：项目两期名次对比（基期待确认）</summary>'''+table(read('table-3-4-4')[1])+'''<a href="/assets/gosr/data/'''+read('table-3-4-4')[0]+'''" download>原始 CSV ↓</a></details>'''+gallery('intro')+'''</section><script id="gosr-data" type="application/json">'''+json.dumps({'datasets':DATA,'labels':LABELS,'source':REPO},ensure_ascii=False).replace('<','\\u003c')+'</script></div>')
 return ''.join(out)
def export(out):
 shutil.copytree(DIR,out/'assets/gosr',dirs_exist_ok=True)
 for key,d in DATA.items():
  if d['kind']=='bars':(out/'assets/gosr'/f'{key}.svg').write_text(resolve(svg(d)))
