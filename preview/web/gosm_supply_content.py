"""5.1 shared Web / PDF publication manuscript; retained source data."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION="20261021-s51-publication-v2"
FIGS={'world': ('5-1-1', '全球模型与数据供给全景', '全球分布与连续记录分别观察。', 'supply51'),
 'cnus': ('5-1-2', '中美模型与数据发布者排行', '按资产类型比较发布账号。', 'supply51'),
 'china': ('5-1-3', '中国模型供给的区域结构', '从省级分布进入发布组织。', 'supply51')}
BRIDGE='供给记录回答谁在发布、资产在哪里积累。下一节沿基座与派生关系继续追踪，观察哪些模型成为再创造的起点，以及复用如何连接不同主体。'
NOTES=['本节使用固定快照。平台总览标注 2026-10-16；地域组织记录于 2026-10-17 读取，接口未声明统一统计日。年度积累按 2026-09-13 仍可见仓库的创建时间回溯，各年点位均为 9 月 13 日，不代表报告年度或历年独立存档。',
 '地域样本含 826 个组织账号、73,088 个模型及 12,502 个配套数据集。模型数约覆盖平台总量的 2.31%，累计下载约覆盖 79.82%；数据集对应约为 1.14% 和 '
 '21.11%。两组日期与覆盖范围不同，覆盖比例仅供识别样本边界，不能作为严格同日统计。',
 '配套数据集沿用同一批模型发布组织，尚未覆盖独立数据发布者。发布账号可能属于个人或组织；地域组织账号未归并为企业集团。国家与省级位置依据账号归属，不表示全部研发、贡献或使用所在地。',
 '月度新增序列截至 2026-07，最新月完整性未说明；不补零、不与 10 月总览拼接。下载记录累计获取，点赞反映关注；两者均不等于使用人数、部署量或模型能力。公开可见仓库尚未逐项核验开源资格。',
 '中美榜单分别按所选资产与指标排序，并列值按账号名称排序；搜索保留原始位次，分页不删减记录。条形共用中美两国全部关联账号中的最大值，不随搜索或分页改变尺度。中国省级归属待补的 12 个组织、149 个模型和 41 '
 '个数据集保留在全国样本总量中；未覆盖地区不记为零供给。']
TOPIC={'id': 'ch05-s01',
 'n': '5.1',
 'en': 'SUPPLY & CONTRIBUTION',
 'title': '供给与贡献',
 'question': '全球模型与数据供给如何积累，哪些发布者与区域节点值得持续关注？',
 'lede': '模型发布为使用与改进提供起点，配套数据支撑训练、评测与适配。本节从全球积累进入中美发布者，再以中国区域分布观察协作节点，识别持续维护的重点。',
 'metric': '仓库数描述资产积累，发布账号描述供给主体；下载与点赞反映获取和关注。它们为 OSDI 的模型与数据开放供给指标提供线索，开放资格与实质贡献仍需进一步核验。',
 'core_finding': '年度回溯中，模型数与发布账号数分别增长 58.3% 和 48.4%。中美模型与配套数据集的头部发布者各有侧重；中国样本中，京沪浙粤集中了 88.8% 的模型。',
 'window_note': '默认报告期为 2025.07.01—2026.06.30。本节保留来源的实际窗口：平台总览 2026-10-16，地域记录 2026-10-17 读取，年度回溯快照 2026-09-13，月度新增截至 '
                '2026-07。各组证据分别比较。',
 'findings': [('资产与发布账号同步扩张', '同一报告快照的年度回溯中，模型数增长58.3%，发布账号数增长48.4%。', 'world'),
              ('模型与数据由不同发布者支撑', '按累计下载量排序，模型与配套数据集呈现不同的头部账号。', 'cnus'),
              ('区域集聚需要进一步落实到组织', '京沪浙粤占中国样本模型数的88.8%；147个组织中，12个仍缺省级归属。', 'china')],
 'figures': ['world', 'cnus', 'china'],
 'narratives': [('5.1.1 全球供给：区分资产积累与发布主体', ''), ('5.1.2 中美比较：从排行榜识别发布者', ''), ('5.1.3 中国观察：从区域集聚进入协作节点', '')],
 'insights': {'world': ['资产与发布账号同步扩张。2026 年 9 月 13 日的可见模型快照中，模型数从上年同日回溯的 193.48 万增至 306.22 万，增长 58.3%；发布账号从 41.32 万增至 61.33 万，增长 '
                        '48.4%。这些账号包含个人与组织，不等于开发者人数；回溯只覆盖快照时仍可见的资产。',
                        '全球规模与地域分布需要分开阅读。2026 年 10 月 16 日的平台总览记录约 315.88 万个模型和 109.30 万个数据集。地域样本覆盖 826 个组织账号；中美合计占该样本模型数的 '
                        '71.7%、累计下载量的 86.6%，这一比例不代表全平台或全球的国家贡献份额。',
                        '资产增长带来版本管理、文档与适配需求。持续观察发布、更新和退出，才能识别维护负担。月度新增记录可辅助判断发布节奏；最新月完整性未说明，末端回落尚不足以说明增长放缓。'],
              'cnus': ['模型排行榜将比较落到具体发布者。中国样本前三为 Qwen、BAAI 和 deepseek-ai，美国为 sentence-transformers、google-bert 和 '
                       'openai。榜单按累计下载量排序，中美使用相同单位与条形尺度。',
                       '配套数据集呈现另一组发布者：中国前三为 InternRobotics、zai-org 和 OpenGVLab，美国为 allenai、argilla 和 '
                       'huggingface。两类榜单沿用同一组织名录，配套数据尚未覆盖独立数据发布者。',
                       '维护支持应分别识别模型与数据的关键账号。结合真实采用、版本更新与问题反馈，核查文档、适配和维护需求。下载量提供获取信号，不能直接代表模型能力或实际采用规模。'],
              'china': ['区域集聚在样本中较为明显。中国样本的 147 个组织中，135 个已有省级归属，12 个仍待补充。北京、上海、浙江、广东合计 116 个组织、5,408 个模型，占全国样本模型数的 '
                        '88.8%；分母保留省级归属待补的 149 个模型。',
                        '不同指标指向不同节点。北京以 47 个组织居首，浙江以 1,726 个模型和约 44.45 亿次累计下载领先；配套数据集则由北京以 480 个数据集、约 1,615.56 '
                        '万次累计下载居首。组织基础、资产积累与获取活动，需要结合具体发布者判断。',
                        '区域节点可以连接高校、企业与社区，围绕实际需求组织开放任务、导师支持和后续维护，并保留跨地区远程参与入口。地图用于寻找合作对象，合作成效还需由项目记录检验。']},
 'action_lead': '5.1.4 行动建议：将供给积累转化为持续协作',
 'action_intro': '',
 'actions': [('国际组织、公共部门与研究机构', '持续维护可比较的供给记录', '固定窗口，分别记录模型、数据集和发布账号的新增、更新与退出，保留许可、版本、账号归属及未知项。支持覆盖不足地区的平台与社区共同补齐记录。', 'world'),
             ('公共资助方、平台与开源社区', '分别支持模型与数据维护', '围绕实际采用的模型、数据集和评测材料，核查版本更新、文档与适配负担，为关键维护者提供稳定支持，并为高校、中小团队和新参与者提供协作入口。', 'cnus'),
             ('地区、高校、企业与合作伙伴',
              '以区域节点组织开放任务',
              '从已有组织和本地需求出发，明确任务、导师与维护责任，提供跨地区远程参与机会。中国地图提供节点识别的实例，其他地区需结合自身供给和社区条件设计合作。',
              'china')],
 'action_followups': {'world': '持续观察记录覆盖率、发布者更新情况和退出原因的可核查程度。',
                      'cnus': '以版本维护、问题解决和可核验的下游复用检验支持效果。',
                      'china': '以参与者留存、跨地区维护关系延续和实际需求得到回应的情况检验成效。'},
 'related': []}

def payload():
    p=ROOT/'content/gosm/supply-observation.json'
    d=json.loads(p.read_text()) if p.exists() else {}
    geo=json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
    prov=json.loads((ROOT/'content/cmap/data.json').read_text())['provinces']
    codes={r['id']:r['source_code'] for r in prov}
    d['geometry']={'world':geo['world'],'china':[{**f,'source_code':codes.get(f['id'])} for f in geo['china']]}
    return d

def panel(key,E):
    num,title,_,_=FIGS[key]
    return f'''<article id="gm-{key}" class="gm-panel s51-panel gm-compact-panel" data-gm-chart="{key}" data-figure-number="图 {num}" aria-labelledby="gm-{key}-caption"><header class="gm-chart-head"><div class="gm-tools"><button data-gm-full>全屏</button><details class="s51-export-menu" data-s51-menu><summary>数据与导出 ▾</summary><div><button data-gm-table>查看数据表</button><button data-gm-svg>下载 SVG</button><button data-gm-csv>下载 CSV</button></div></details></div></header><div class="gm-controls"></div><div class="gm-view"></div><div class="gm-readout" aria-live="polite"></div><details class="gm-table"><summary>查看本图数据<span class="s51-close-hint"> · 关闭 ×</span></summary><div class="gm-table-host"></div></details><footer class="s51-caption"><h3 id="gm-{key}-caption">图 {num} {E(title)}</h3></footer><noscript><p>交互需要启用 JavaScript。正文与口径说明可直接阅读。</p></noscript></article>'''

def section(t,panel,E):
    para=lambda s:'<p>'+E(s)+'</p>'
    out=[f'<section id="ch05-s01" class="chapter-section gm-topic s51-topic" data-publication-edition="{VERSION}"><header class="gm-topic-header"><span class="eyebrow">5.1 / SUPPLY & CONTRIBUTION</span><h2>5.1 {E(t["title"])}</h2>'+para(t['lede'])+para('研究问题：'+t['question'])+'<p class="s51-position">'+E('指标定位：'+t['metric'])+'</p></header><p class="s51-core" id="s51-findings"><strong>核心发现：</strong>'+E(t['core_finding'])+'</p><p class="s51-window-note">'+E(t['window_note'])+'</p>']
    for key,(title,_) in zip(t['figures'],t['narratives']):
        ps=t['insights'][key]
        out.append(f'<section class="s51-perspective" id="s51-{key}"><h3>{E(title)}</h3>'+para(ps[0])+panel(key))
        if key=='world':
            out.append('<details class="s51-source" id="s51-evidence"><summary>口径与来源</summary>'+''.join(para(n) for n in NOTES)+'<p><a href="/assets/gosm/supply-observation.json">固定供给快照</a> · <a href="/assets/gosm/supply-methods.md">地域样本与核验</a> · <a href="/assets/gosm/data/fig-5-1-1_hf_cumulative_models_publishers.csv">年度回溯原表</a> · <a href="/assets/gosm/provenance.json">来源与文件指纹</a></p></details>')
        out.extend(para(s) for s in ps[1:]);out.append('</section>')
    out.append('<section class="s51-actions" id="gm-actions-1"><h3>'+E(t['action_lead'])+'</h3>')
    for who,title,body,key in t['actions']:
        out.append('<h4>'+E(who+'：'+title)+'</h4>'+para(body+t['action_followups'][key]))
    out.append(para(BRIDGE)+'</section></section>')
    return ''.join(out)

def manuscript():
    t=TOPIC;out=['# 5.1 '+t['title'],t['lede'],'研究问题：'+t['question'],'指标定位：'+t['metric'],'核心发现：'+t['core_finding'],t['window_note']]
    for key,(title,_) in zip(t['figures'],t['narratives']):
        out.extend(['## '+title,t['insights'][key][0],'图 '+FIGS[key][0]+' '+FIGS[key][1],*t['insights'][key][1:]])
    out.append('## '+t['action_lead'])
    for who,title,body,key in t['actions']:out.extend(['### '+who+'：'+title,body+t['action_followups'][key]])
    return '\n\n'.join([*out,BRIDGE,'## 口径与来源',*NOTES])+'\n'
