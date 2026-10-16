"""A-Map: global distribution, five-year growth and asset composition."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
FIGURES=[
 ('world','GLOBAL ASSET SUPPLY','全球开源资产供给地图',[('code','代码仓库'),('models','模型仓库'),('datasets','数据仓库')],'从同一张世界地图，看三类资产的供给节点','底图沿用 OpenShare 已确认形态，中国包含台湾省。代码国家分布为模拟；模型、数据集保留原稿前 14 国读数，其余为模拟补齐。可切换为仅看已提供数据。'),
 ('growth','FIVE-YEAR ASSET GROWTH','开源资产五年增长',[('overview','增长总览'),('commits','代码提交'),('code','代码仓库'),('models','模型仓库'),('datasets','数据仓库')],'2022—2026 · 各指标独立计量、分别标记证据','代码仓库保留四平台原表；模型为 2026-09-13 快照回溯队列。2022—2024 提交量、2022—2025 数据集规模及 AtomGit 两个缺年使用模拟；2026 提交量为管理层全年预测。'),
 ('structure','ASSET CATEGORIES & EVOLUTION','开源资产类别与演进',[('code','代码技术类别'),('models','模型任务类别'),('datasets','数据任务类别')],'当年看结构 · 五年看方向 · 点击类别继续探索','代码仓库类别数量为模拟；OpenRank 切换使用附件折线的近似读数及 2026 情景。模型、数据集当期任务标签来自接口，历史类别序列为模拟。标签记录不等同去重仓库。')
]

def figure(i):
 key,en,title,tabs,context,caption=FIGURES[i-1]
 return f'''<figure id="fig-2-5-{i}" class="am-figure"><div class="am-stage goso-unified-canvas" data-lang="zh" data-slide-key="amap-{i}" data-slide-height="820" role="group" aria-label="{title}"><div class="am-board">
 <header class="am-board-head"><div><span class="am-eyebrow">图 2-5-{i} / {en}</span><h4>{title}</h4></div><button data-am-source="{key}">口径与来源</button></header>
 <div class="am-toolbar"><div class="am-tabs" aria-label="{title}视图">{''.join(f'<button data-am-tab="{key}:{v}" aria-pressed="{str(j==0).lower()}">{label}</button>' for j,(v,label) in enumerate(tabs))}</div><span class="am-context">{context}</span></div>
 <div id="am-{key}" class="am-panel" aria-live="polite"></div><footer class="am-board-foot"><span id="am-{key}-foot"></span><a href="/assets/amap/source-manifest.json" download>来源清单 ↓</a></footer>
 <div class="am-source-overlay" data-am-overlay="{key}" hidden></div></div></div><figcaption>{caption}</figcaption></figure>'''

def section(lang='zh'):
 if lang!='zh':return '<section id="ch02-s05"><h2>2.5 Global open-source asset map (A-Map)</h2><p>The three-figure interactive review is currently available in Chinese.</p><a href="/2026/zh/chapters/02/#ch02-s05">Open A-Map →</a></section>'
 return '''<section id="ch02-s05" class="chapter-section goso-section amap-review">
 <div class="section-topline">2.5 / A-MAP</div><h2>全球开源资产地图（A-Map）</h2><p class="goso-question">AI 时代的开放资产在哪里生成、增长多快，又正在向哪些领域演进？</p>
 <div class="goso-map-position"><strong>目标与指标定位</strong><p>本节对应 OSDGs 的 X2“技术产出与开放供给”：用 OSDI 的 ActiveRepo、OpenModelRelease、OpenDatasetRelease 观察代码、模型与数据供给，用 ModelSupplierDiv、DataSupplierDiv 追踪供应方的地域与主体多样性。技术类别数量是结构诊断，类别 OpenRank 影响力衔接 X3 的网络影响观察；二者分别计量。正式指标测算仍需核验开放资格、统计窗口及去重规则。</p><a href="/2026/zh/data/indicators/">回到第一章的 OSDI 指标词典 →</a></div>
 <h3>核心发现</h3><p><strong>开放供给正在从代码扩展为代码、模型与数据共同支撑的资产体系。</strong>前四节观察参与、贡献、项目影响与人才积累，本节转向这些力量共同创造的资产：先看全球分布，再看生产与供给的增长，最后辨识类别结构及其演进方向。</p>
 <div class="am-findings"><p><b>01 · 分布看节点</b>同一地区在不同资产上的供给位置可以不同，需要分别观察。</p><p><b>02 · 增长看节奏</b>生产活动明显加速，各平台与资产的扩张节奏需要分开读。</p><p><b>03 · 类别看方向</b>从总量进入技术与任务结构，辨识需要共同建设的互补资产。</p></div>
 <p class="am-review-banner"><strong>审阅样稿 · 含模拟与预测</strong> 为呈现完整研究结构，本轮补齐部分缺失序列和分布。图中逐项标记“来源表值 / 原稿读数 / 模拟 / 预测”；模拟结果供选型，不作为正式结论。</p>
 <nav class="goso-map-route" aria-label="资产地图图组"><a href="#fig-2-5-1">01 全球分布</a><a href="#fig-2-5-2">02 五年增长</a><a href="#fig-2-5-3">03 类别演进</a></nav>
 <section class="am-section"><div class="am-section-head"><span>01 / 全球分布</span><div><h3>三类资产，在同一张世界地图上分别观察。</h3><p>切换代码、模型与数据仓库，比较供应方的地域分布。模型和数据地图以原稿组织样本为依据；代码地图先演示未来国家归属底表接入后的阅读方式。平台总量、已提供读数与模拟补齐始终分层呈现。</p></div></div>'''+figure(1)+'''
 <div class="am-insight"><b>洞察 01</b><div><h4>供给位置因资产而异，多中心共建需要更细的观察。</h4><p>在原稿的发布单位样本中，美国模型数量份额约为 63.4%，数据集数量份额约为 47.8%；中国对应份额约为 8.3% 和 10.9%。这说明同一地区在不同资产中的供给结构并不相同。样本不能代表 Hugging Face 全体仓库，模拟区域也不参与这一结论。对全球合作而言，应识别更多可持续供给节点，让不同地区围绕自身能力和在地需求参与共建。</p></div></div></section>
 <section class="am-section"><div class="am-section-head"><span>02 / 五年增长</span><div><h3>生产进入更大量级，资产扩张仍有不同节奏。</h3><p>将代码提交与三类仓库并列观察。代码提交描述生产活动，代码仓库观察持续活跃的资产容器，模型与数据仓库反映新增的能力供给。总览便于把握变化，四平台细图保留规模差异与不同增长路径。</p></div></div>'''+figure(2)+'''
 <div class="am-insight"><b>洞察 02</b><div><h4>增长需要同时看基数、增量与持续供给。</h4><p>报告原表中，2026 年 GitHub、Gitee 活跃仓库分别约为 632.9 万和 438.9 万，较上年增长约 8.5% 和 13.3%；AtomGit 在较低基数上快速扩张，GitLab 也保持增长。与此同时，GitHub 管理层披露的提交量由 2025 年约 10 亿次，走向按 2026 年当时速率推算的全年约 140 亿次。这一提交口径不限公开开源仓库，作为生产背景使用。平台活动的跃升提示承载、审阅与维护需求正在变化；不同口径仍应保留各自时间窗，不能相加为全球去重资产总量。</p></div></div></section>
 <section class="am-section"><div class="am-section-head"><span>03 / 类别演进</span><div><h3>从“增长多少”，进一步追问“增长在哪里”。</h3><p>用矩形树图呈现当年的类别结构，用折线图呈现五年演进。代码按技术领域观察，模型与数据按任务标签组织；点选类别可查看细分任务和对应趋势。代码还可切换至附件中的 OpenRank 影响力视角，理解数量与网络位置的不同含义。</p></div></div>'''+figure(3)+'''
 <div class="am-insight"><b>洞察 03</b><div><h4>关键能力需要互补资产，分类观察应服务共建方向。</h4><p>已有任务标签记录中，模型供给的文本生成条目较多，数据集供给中的机器人任务也十分突出。代码、模型与数据面向不同环节，不能仅以某一类资产的数量判断能力是否完整。当前五年类别曲线中的模拟部分用于讨论研究结构；正式数据补齐后，再判断哪些领域持续成长、哪些供给需要加强，并与第四章技术全景和第五章模型生态研究衔接。</p></div></div></section>
 <section class="am-actions"><span class="am-eyebrow">FROM ASSET OBSERVATION TO SHARED DEVELOPMENT</span><h3>三个主张：长期观测、扩大节点、完善互补供给。</h3><div><article><b>01</b><h4>建立跨资产的长期观测</h4><p>平台与研究机构共同维护代码、模型、数据的稳定标识、来源记录和年度序列，分别跟踪发布、活跃、维护与复用，让开放供给的变化可查证、可比较。</p></article><article><b>02</b><h4>培育更多持续供给节点</h4><p>支持全球南方及其他地区围绕本地语言、知识和公共需求形成长期供给能力。通过区域平台、研究机构与全球社区合作，让更多地方参与资产生产、维护与共同决策。</p></article><article><b>03</b><h4>补齐关键领域的互补资产</h4><p>围绕重要技术与公共需求，同步支持代码工具、模型、数据和评测材料。把资助延伸到文档、许可、适配与维护，以可复用的资产组合承接 AI 时代的增长。</p></article></div></section>
 <details class="am-methods"><summary>本轮哪些数据需要后续替换？</summary><p>① 地图：代码仓库国家归属，以及模型、数据原稿前 14 国以外的完整底表。② 增长：2022—2024 同口径代码提交量、2022—2025 数据仓库快照、AtomGit 两个缺年。③ 类别：代码主类别仓库数、技术领域 OpenRank 精确原表，以及模型、数据任务标签的历年快照。模拟与原稿读数已逐行标记，可直接按文件替换。</p><p>2026 提交量保留管理层前瞻预测性质；图像近似读数保留近似标记。地图不将开发者所在地等同于仓库归属，不将托管服务器位置当作供给方国家。</p><a href="/assets/amap/geography-v3.csv" download>地图数据 ↓</a> · <a href="/assets/amap/growth-v3.csv" download>五年序列 ↓</a> · <a href="/assets/amap/categories-v3.csv" download>类别数据 ↓</a> · <a href="/assets/amap/simulation-v3.json" download>模拟与外推说明 ↓</a></details>
 <p class="goso-bridge">人才与协作持续产生开放资产，资产又为新的参与和创新提供基础。下一节 D-Map 将转向跨地域合作，讨论这些供给如何连接更多共同建设者。</p><div class="am-end-nav"><a href="#ch02-s04">← 回看人才 T-Map</a><a href="#ch02-s06">继续：全球开源多样性 D-Map →</a></div>
 <noscript><p>启用 JavaScript 可探索交互图；本节底表与模拟说明可通过上方链接下载。</p></noscript></section>'''

def export(out):
 shutil.copytree(ROOT/'content/amap',out/'assets/amap',dirs_exist_ok=True)
 for name in ['amap.js','amap.css']:shutil.copy2(ROOT/'web'/name,out/name)
