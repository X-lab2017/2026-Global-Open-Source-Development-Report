"""Shared 5.3 manuscript: separate materials, rights and observed evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='gosm-openness-v2-atlas'
PUBLICATION_VERSION='20261022-s53-publication'
FIGS={'openness': ('5-3-1', '模型开放分级与样本结构', '', 'quadrants'),
 'open-groups': ('5-3-2', '地域开放结构与完整交付', '', 'openRegions'),
 'dossiers': ('5-3-3', '发布主体的供给规模与开放实践', '', 'openPublishers,cases')}
TOPIC={'id': 'ch05-s03',
 'n': '5.3',
 'en': 'OPENNESS & SHARED INNOVATION',
 'title': '开源开放与分级体系',
 'question': '模型开放到了哪一步，哪些材料与许可条件能够支持更多人理解、改进和共同建设？',
 'lede': '模型能否被持续改进，既取决于使用与再分发的权利，也取决于训练、测试和复现材料是否齐备。承接 5.1 的供给分布与 5.2 的复用关系，本节以材料完整性和许可开放性两个维度，观察开放发布如何支撑共同创新。',
 'metric': '对应 OSDGs 的 X4“开源善治与公共价值”，以 AIAssetTransparency 和 LicenseOpenness 观察材料透明度与许可条件，并衔接 X2 的开放供给。ModelRank '
           '仅补充生态位置；材料、许可与影响力分别解释，不合成为总分。',
 'core_finding': '许可较开放，并不意味着训练与验证材料同样完整。870 个报告样本中，高开放模型为 600 个，同时达到高完整的为 117 '
                 '个。中、美、欧的高开放比例差异明显，双高比例却较为接近。企业承担主要供给，也贡献了最多的双高模型；支持共同创新，需要同时改善交付质量与验证能力。',
 'window_note': '统计主线为 870 个报告样本（2026-09-14 提取）；884 条平台记录与 4 个固定版本案例为 2026-10-17 的独立补充。ModelRank 月榜覆盖 '
                '2025-09—2026-08。各组证据保留真实日期，既有等级沿用源评估结果。',
 'figures': ['openness', 'open-groups', 'dossiers'],
 'narratives': [('5.3.1 开放条件：材料完整性与许可权利分别衡量', ''), ('5.3.2 地域比较：许可差异之外的共同交付问题', ''), ('5.3.3 发布主体：供给规模、开放实践与模型证据', '')],
 'insights': {'openness': ['图 5-3-1 以具体版本的模型发布单元（MRU）为对象，分别解释完整性 L 与开放性 O。L1—L5 从部署、理解延伸到训练公开、性能验证和全链复现，高等级包含低等级的全部要求；O1—O4 '
                           '描述相应材料的许可权利与义务。先确认材料满足哪个 L，再判断这一材料范围内的 O。宽松许可支持模型使用与改进，却不能替代完整的训练材料。',
                           '870 个报告样本中，低完整、高开放有 483 个，占 55.5%；高完整、高开放有 117 个，占 13.4%。在全部 600 个高开放模型中，双高占 19.5%。这里的高完整为 '
                           'L3—L5，高开放为 O2—O4，是结构比较的分组口径；O2 的互惠义务仍需按具体用途核对。',
                           '材料公开与验证通过应分别记录。权重能够下载、训练材料具有入口、第三方成功复现，是三个不同层次的证据。支持工作应进一步落实到完整数据来源与处理规则、可运行环境和验证记录。分级释义依据已发布的 SJ/T '
                           '12304-2026，自 2026 年 12 月 1 日起实施；本节不据此追溯重评既有样本。'],
              'open-groups': ['在 870 个报告样本中，中国 404 个、美国 258 个、欧洲 81 个。三组高开放比例分别为 84.9%、47.7% 和 65.4%；若同时要求高完整，比例分别为 13.9%、13.2% '
                              '和 13.6%。图 5-3-2 将四类结构与两项比例并列，显示许可条件的差异，尚未转化为同等幅度的完整交付差异。',
                              '地域规模与组内比例回答不同问题。中国样本中的双高模型为 56 个，美国 34 个，欧洲 11 个；比例接近不表示绝对数量相同。其余国家 65 个、归属未知 62 个均保留在总样本中。国家地图另用 '
                              '884 条平台记录，其中 820 条具有可识别归属，覆盖 25 个国家和地区；64 条未知单列，两套样本不能作为前后增长比较。',
                              '这一结果为跨机构合作提供了具体议题：共同补齐训练代码、完整数据来源与处理规则、评测配置及最小验证任务。现有样本并非随机抽样，原报告的精确统计年窗与欧洲成员范围仍待补充；地域比较描述已评估模型，不据此排列各国总体能力。'],
              'dossiers': ['企业发布了 711 个模型，占 870 个报告样本的 81.7%；其中 69 个为双高，组内比例为 9.7%，占全部 117 个双高模型的 '
                           '59.0%。非营利组织和高校、社区、个人账号的组内双高比例分别为 42.6%、30.0% 和 18.2%。图 5-3-3 '
                           '同时保留数量与比例：企业承担主要供给，其他主体的开放实践则提供了可共同借鉴的交付经验。',
                           '主体结构需要回到具体模型的材料与版本核验。884 条平台记录保留逐项材料、许可解释和来源，其中 22 条存在许可字段与最终等级不一致的线索，标为待复核。4 个独立案例提供固定提交的查证入口；例如 '
                           'OLMo-2 的权重、分阶段训练代码和数据入口形成了较完整的材料链，但观察到材料不等于独立跑通验证，也不直接授予等级。',
                           '平台记录与 2026 年 8 月 ModelRank Top100 按完整模型 ID 精确关联，得到 38 '
                           '条交集。月度位次用于寻找值得持续跟踪的对象；未覆盖月份保留空缺。开放快照与月榜日期不同、提交版本尚未完全对齐，不能据此判断开放程度导致影响力变化。持续维护应把材料修订、验证结果与下游反馈连接起来。']},
 'actions': [('公共部门、标准机构与平台',
              '建立版本化的开放交付记录',
              '围绕部署、再训练或独立验证的实际用途，明确所需材料与许可条件，记录模型版本、资源清单、授权范围、评估依据和验证日期。L 与 O 分别呈现，未知项与待复核项保留纠错入口。',
              'openness'),
             ('资助方、企业与研究机构',
              '为独立验证提供持续支持',
              '将可运行训练环境、完整数据来源与处理规则、评测配置和复现指南纳入支持范围，为第三方开展最小训练、评测和端到端验证提供计算资源与维护时间。',
              'open-groups'),
             ('企业、高校、基金会与开源社区',
              '把供给规模连接到共同维护',
              '结合企业的供给规模与高校、社区的开放实践，共建参考流程、公开任务和版本化证据档案。围绕真实需求组织共同评审与长期维护，让更多团队能够参与后续改进。',
              'dossiers')],
 'action_followups': {'openness': '核心材料缺少可验证许可时单独标示，不归入 O1。',
                      'open-groups': '以材料是否补齐、验证能否重复观察成效，并记录验证范围与失败原因。',
                      'dossiers': '同时关注高影响力模型与公共需求下的长尾模型，以问题解决、下游复用和参与者留存观察合作效果。'},
 'related': [],
 'action_lead': '5.3.4 行动建议：把开放条件落实为可验证的交付'}
NOTES=['规范依据：SJ/T 12304-2026，工信部 2026 年第 22 号公告，附件第 465 项；2026-08-17 发布，2026-12-01 实施。条文释义沿用提供的规范文本，完整材料清单见在线入口。开放分级不替代安全、合规或正式公共品认可。',
 '870 报告样本来自年度每周点赞增量 Top100 候选，经去重并保留官方基座与官方衍生，排除第三方改包及基础材料不足者。仅有汇总表，不生成 20 格细分或地域与主体的交叉统计。各组比例使用本组分母。',
 '884 平台记录为独立快照，未与 870 逐一对齐；差值 14 不表示净增长。地图按 country 字段汇总，位置按发布主体归属，未知单列；主体标签尚未合并为法律实体。22 条许可字段差异保留原等级，等待复核。',
 '4 个独立案例固定到 40 字符提交。已观察表示存在材料或声明，不表示独立验证成功；待核实不表示不存在。案例不加入统计样本，也不据此授予 L/O 等级。',
 'ModelRank 为 2025-09—2026-08 的 12 个月 Top100 快照；以完整模型 ID 精确匹配，2026-08 交集为 38 条。不合并别名或家族，未覆盖月份不补零或第 101 名；跨月归一化分数不作增长率。']
BRIDGE='模型供给、生态复用与开放条件共同构成持续创新的基础。后续行动需要把可追溯的观察转化为稳定支持，并在持续维护中检验公共价值。'

def payload():return json.loads((ROOT/'content/gosm/openness53.json').read_text())

def panel(key,E):
    num,title,_,_=FIGS[key]
    return f'''<article id="gm-{key}" class="gm-panel s53-panel gm-compact-panel" data-gm-chart="{key}" data-figure-number="图 {num}" aria-labelledby="gm-{key}-caption"><header class="gm-chart-head"><div class="gm-tools"><button data-gm-full>全屏</button><details class="s51-export-menu" data-s51-menu><summary>数据与导出 ▾</summary><div><button data-gm-table>查看数据表</button><button data-gm-svg>下载 SVG</button><button data-gm-csv>下载 CSV</button></div></details></div></header><div class="gm-controls"></div><div class="gm-view"></div><div class="gm-readout" aria-live="polite"></div><div class="s53-print-view" aria-hidden="true"></div><details class="gm-source"><summary>分级材料与证据说明<span class="s51-close-hint"> · 关闭 ×</span></summary><div class="gm-source-body"></div></details><details class="gm-table"><summary>查看本图数据<span class="s51-close-hint"> · 关闭 ×</span></summary><div class="gm-table-host"></div></details><footer class="s53-figure-caption"><h3 id="gm-{key}-caption">图 {num} {E(title)}</h3></footer><noscript><p>交互需要启用 JavaScript。正文与口径说明可直接阅读。</p></noscript></article>'''

def section(t,panel,E):
    para=lambda s:'<p>'+E(s)+'</p>'
    out=[f'<section id="ch05-s03" class="chapter-section gm-topic s53-topic" data-publication-edition="{PUBLICATION_VERSION}"><header class="gm-topic-header"><span class="eyebrow">5.3 / OPENNESS &amp; SHARED INNOVATION</span><h2>5.3 {E(t["title"])}</h2>'+para(t['lede'])+para('研究问题：'+t['question'])+'<p class="s53-position">'+E('指标定位：'+t['metric'])+'</p></header><p class="s53-core"><strong>核心发现：</strong>'+E(t['core_finding'])+'</p><p class="s53-window-note">'+E(t['window_note'])+'</p>']
    for key,(title,_) in zip(t['figures'],t['narratives']):
        ps=t['insights'][key];out.append(f'<section class="s53-perspective" id="s53-{key}"><h3>{E(title)}</h3>'+para(ps[0])+panel(key))
        if key=='openness':out.append('<details class="s53-source" id="s53-evidence"><summary>口径与来源</summary>'+''.join(para(n) for n in NOTES)+'<p><a href="/assets/gosm/openness53-methods.md">完整方法与样本边界</a> · <a href="/assets/gosm/openness-evidence-884.json">逐项证据</a> · <a href="/assets/gosm/cases.json">固定版本案例</a> · <a href="/assets/gosm/standard-publication.json">标准发布信息</a></p></details>')
        out.extend(para(s) for s in ps[1:]);out.append('</section>')
    out.append('<section class="s53-actions" id="gm-actions-3"><h3>'+E(t['action_lead'])+'</h3>')
    for who,title,body,key in t['actions']:out.append('<h4>'+E(who+'：'+title)+'</h4>'+para(body+t['action_followups'][key]))
    out.append(para(BRIDGE)+'</section></section>');return ''.join(out)

def manuscript():
    t=TOPIC;out=['# 5.3 '+t['title'],t['lede'],'研究问题：'+t['question'],'指标定位：'+t['metric'],'核心发现：'+t['core_finding'],t['window_note']]
    for key,(title,_) in zip(t['figures'],t['narratives']):out.extend(['## '+title,t['insights'][key][0],'图 '+FIGS[key][0]+' '+FIGS[key][1],*t['insights'][key][1:]])
    out.append('## '+t['action_lead'])
    for who,title,body,key in t['actions']:out.extend(['### '+who+'：'+title,body+t['action_followups'][key]])
    return '\n\n'.join([*out,BRIDGE,'## 口径与来源',*NOTES])+'\n'
