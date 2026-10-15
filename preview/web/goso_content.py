"""GOSO review chapter: source-backed evidence, narrative and accessible charts."""
from pathlib import Path
import csv, hashlib, html, json, math

ROOT=Path(__file__).resolve().parents[1]
REF='95ffe2d3ae52191555a40af25e1a00b26ffc65cc'
REPO='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/'+REF+'/'
E=lambda x:html.escape(str(x),quote=True)
COLORS=['var(--gv-s0, #156993)', 'var(--gv-s1, #279FA9)', 'var(--gv-s2, #4E87C5)', 'var(--gv-s3, #9973B7)', 'var(--gv-s4, #5C8A3C)', 'var(--gv-s5, #C08A2D)', 'var(--gv-s6, #8C5B3F)', 'var(--gv-s7, #6B7F8C)']
LABELS={'Europe':'欧洲','United States':'美国','China':'中国','India':'印度','Global South representatives':'全球南方六国','Germany':'德国','United Kingdom':'英国','Other countries':'其他国家','GitCode':'AtomGit','Canada':'加拿大','Singapore':'新加坡','Czechia':'捷克','Sweden':'瑞典','France':'法国','Netherlands':'荷兰','台湾':'台湾省','台北':'台北（台湾省）','Japan':'日本','Australia':'澳大利亚','Brazil':'巴西'}
RC={'China':'var(--gv-s0, #156993)','United States':'var(--gv-s1, #279FA9)','Europe':'var(--gv-s2, #4E87C5)','India':'var(--gv-s3, #9973B7)','Global South representatives':'var(--gv-s4, #5C8A3C)'}
FILES={
 'total':'chapter2/fig-2-1-2_five_region_total_developers.csv',
 'active':'chapter2/fig-2-1-3_five_region_active_developers_trend.csv',
 'contribution':'chapter2/fig-2-2-2_five_region_openrank_contribution_trend.csv',
 'influence':'chapter2/fig-2-3-2_five_region_project_openrank_influence_trend.csv',
 'talent':'chapter2/fig-2-4-4_china_top10_city_talent_trend.csv',
 'share':'chapter2/fig-2-5-1_country_contribution_share_trend.csv',
 'foundation':'chapter2/fig-2-6-1_foundation_share_and_active_repositories.csv',
 'licenses':'chapter2/fig-2-6-2_active_repository_license_trend.csv',
 'mulan':'chapter2/fig-2-6-3_mulan_permissive_license_trend.csv',
 'platforms':'chapter2/fig-2-7-1_platform_active_repository_trend.csv',
 'province':'chapter2/table-2-2-1_china_province_openrank_per_capita_top10.csv',
 'cities':'chapter2/table-2-4-1_china_city_talent_top10.csv',
 'cross':'chapter2/table-2-5-1_china_us_project_contribution_top10.csv',
 'models':'chapter5/fig-5-1-1_hf_cumulative_models_publishers.csv',
 'geography':'chapter5/fig-5-1-2_country_model_contribution.csv',
}
def rows(key):
    with (ROOT/'content/report-assets/data'/Path(FILES[key]).name).open(newline='') as f:return list(csv.DictReader(f))
def source(key):return REPO+'data/processed/'+FILES[key]
def dataurl(key):return '/assets/report/data/'+Path(FILES[key]).name
def number(x):return None if x in ('',None) else float(x)
def fmt(v,unit=''):
    if v is None:return '—'
    if abs(v)>=10000:return f'{v/10000:,.2f}万'
    return f'{v:,.2f}'.rstrip('0').rstrip('.') if v!=int(v) else f'{int(v):,}'
def line(vid,key,title,unit,note,columns=None,labels=None,x='year'):
    rr=rows(key);columns=columns or [k for k in rr[0] if k!=x];labels=labels or {}
    return dict(id=vid,key=key,title=title,kind='line',unit=unit,note=note,x=[r[x] for r in rr],series=[dict(key=k,label=labels.get(k,LABELS.get(k,k)),color=RC.get(k,COLORS[i%len(COLORS)]),values=[number(r[k]) for r in rr]) for i,k in enumerate(columns)],source=source(key),csv=dataurl(key))
def bars(vid,key,title,unit,note,label,value,filter_fn=None):
    rr=[r for r in rows(key) if filter_fn is None or filter_fn(r)]
    return dict(id=vid,key=key,title=title,kind='bar',unit=unit,note=note,x=[LABELS.get(r[label],r[label]) for r in rr],series=[dict(key=value,label=title,color=COLORS[0],values=[number(r[value]) for r in rr])],source=source(key),csv=dataurl(key))

def views():
    five='年度序列：2022—2026 报告年；五组为美国、中国、欧洲、印度及巴西、印尼、越南、菲律宾、埃及、南非六国。不是完整全球分区，组间人口和平台覆盖不同。'
    out={
    'v':[
      line('active','active','活跃开发者：五组年度比较','人',five+' 活跃人数与账户存量分别展示，不由两张表推算活跃率。'),
      bars('total','total','开发者总量：2026 年存量','人','存量表标记 as_of=2026；具体快照日待补。与年度活跃表不作除法。','region','developers')],
    'c':[
      line('contribution','contribution','开发者 OpenRank 贡献度','OpenRank',five+' 表列来源为 OpenDigger、Gitee、AtomGit；算法版本、平台合并与年度聚合说明待补。'),
      bars('province','province','人均协作贡献：省级样本','OpenRank / 活跃开发者','2026 年表列前十地区。人均值为贡献度除以活跃开发者，按原表保留两位小数；不是人口密度、劳动生产率或人才质量评分。','region','openrank_per_active_developer')],
    'i':[line('influence','influence','项目 OpenRank 影响力','OpenRank',five+' 地区按项目归属聚合；项目映射清单待补。项目影响力与开发者贡献度是不同指标，不能相除得到“转化率”。')],
    't':[
      bars('cities','cities','高影响力人才：十城市样本','人','原表截至 2026 年 7 月，属于单独标注的快照；人才采用个人年度全域 OpenRank 前 5% 的工作定义，基准集合与年度汇总说明待补。','city','talent_count'),
      line('talent','talent','同一组城市的五年变化','人','2022—2026 年固定十城市序列，不解释为每年重新选出的全球或全国 Top 10；人数变化不等于人才迁移。')],
    'd':[
      bars('china-sources','cross','中国项目：贡献来源前十','%','2026 年项目样本；按原表 share_pct 展示，前十合计 93.24%，未补齐部分不重归一化。项目清单与分母处理待补。','developer_country','share_pct',lambda r:r['project_country']=='China'),
      bars('us-sources','cross','美国项目：贡献来源前十','%','2026 年项目样本；按原表 share_pct 展示，前十合计 77.94%，未补齐部分不重归一化。不是开发者人数或迁移流。','developer_country','share_pct',lambda r:r['project_country']=='United States'),
      line('country-share','share','固定五国与其他国家：贡献份额','%','2022—2026；原表列五国与其他国家合计为 100%。本图来源范围与 2.2 五组贡献总值未对齐，独立展示，不据此反推统一全球总量。')],
    'g':[
      line('foundation-share','foundation','基金会项目的 OpenRank 份额','%','2022—2026；基金会项目样本及份额分母待补。它表示影响力份额，不是基金会托管项目比例，也不直接证明治理成效。',['foundation_project_openrank_share_pct'],{'foundation_project_openrank_share_pct':'基金会项目份额'}),
      line('foundation-count','foundation','基金会活跃仓库数','个','2022—2026；仅展示原表基金会样本，不与份额共用坐标轴。',['active_repositories'],{'active_repositories':'活跃仓库'}),
      line('licenses','licenses','五类许可证的活跃仓库','个','2022—2026；展示五类许可证样本数量。全部受检仓库、多许可和未知许可分母待补，不推算全球许可覆盖率。'),
      line('mulan-count','mulan','木兰宽松许可证：累计活跃仓库','个','2022—2026；字段为累计活跃仓库数，不等同当年活跃数量。',['cumulative_active_repositories'],{'cumulative_active_repositories':'累计活跃仓库'}),
      line('mulan-influence','mulan','木兰宽松许可证：项目影响力','OpenRank','2022—2026；影响力与采用数量分别呈现，不能由同步增长推断许可证产生了治理效果。',['project_openrank_influence'],{'project_openrank_influence':'项目影响力'})],
    'a':[
      line('platforms','platforms','代码资产：平台活跃仓库','个','2022—2026；依作者确认，GitCode 列统一显示为 AtomGit，原始 CSV 字段保留。2022、2023 年空值不是零；合并前后覆盖变化待补，各平台不去重相加。'),
      line('models','models','模型供给：累计可见模型','个','补充观察 · 2026-09-13 快照回溯各年同日。按该日仍可见的仓库创建时间回溯，非历年独立历史快照；不并入截至 6 月的报告年度。',['models'],{'models':'累计模型'},x='date'),
      line('publishers','models','模型供给：累计发布者','个','补充观察 · 2026-09-13 快照回溯。发布者为平台发布身份，不等同独立企业或自然人数；保留原表口径。',['publishers'],{'publishers':'累计发布者'},x='date')]
    }
    rr=rows('geography');unknown=sum(int(r['models']) for r in rr if not r['region_code']);known=sum(int(r['models']) for r in rr if r['region_code'])
    out['a'].append(dict(id='coverage',key='geography',title='模型地域观察：归属信息覆盖率',kind='coverage',unit='个',note='补充观察 · 2026-09-13。全部 3,062,151 个模型中，71,578 个有已识别国家，覆盖 52 国；其余保留未知。未知表示发布方归属未识别，不表示这些模型缺乏价值。',x=['国家已识别','国家未知'],series=[dict(key='models',label='模型数',color=COLORS[0],values=[known,unknown])],source=source('geography'),csv=dataurl('geography')))
    out['v']=[]  # V-Map now uses the independently sourced current snapshot.
    return out

SECTIONS=[
 dict(key='v',code='V-MAP',name='全球开源活跃地图',question='参与基础在扩大，哪些地区正在更快地释放活跃力量？',headline='欧洲活跃规模领先，中国增速让中美差距收窄。',pillars=['DevScale'],kpi='42.0%',kpi_label='中国活跃开发者同比增长',
 paragraphs=[('从存量进入当期参与','2026 年开发者总量表中，美国、欧洲与中国分别约为 3029.8 万、3014.8 万和 2918.7 万。相近的账户存量提供了一个起点；年度活跃开发者更接近本章关心的现实协作基础。欧洲在活跃人数表中以 675.4 万居五组首位，美国为 465.2 万，中国为 454.5 万。'),('看增量，也看仍然存在的差距','中国活跃人数比上一报告年增加约 134.5 万，同比增长 42.0%；美国和欧洲分别增长约 31.2% 和 29.8%。中美活跃人数差距收窄至约 10.6 万。印度与全球南方六国分别达到 272.4 万和 300.5 万，同比增长约 28.4% 和 29.2%。广泛参与为更多地区进入开放协作提供了基础。'),('普惠之后，需要继续追踪什么','对公共部门与社区来说，下一步值得观察的是新增参与者能否持续留下、进入有意义的协作，并获得成长机会。人数增长回答了参与规模的问题；贡献、人才与跨地域连接将进一步说明这种参与如何进入生态。')],
 takeaway='从“有多少开发者”继续追问“有多少人持续参与”。活跃增长是能力建设的入口，尚不能代替质量与公共成效。',gap='报告年度的全球及中国完整地域底表、未知所在地分组与存量快照日；补充地图快照已单独提供。',bridge='接下来，看参与者在协作网络中贡献了什么。'),
 dict(key='c',code='C-MAP',name='全球开源贡献地图',question='参与规模相近，协作贡献的结构是否也相同？',headline='欧洲保持贡献优势，中国在五组底表中超过美国。',pillars=['OpenRankContrib'],kpi='442.9万',kpi_label='中国表列开发者贡献度 · OpenRank',
 paragraphs=[('五组比较中的结构变化','2026 年五组开发者贡献表中，欧洲约为 650.2 万，中国为 442.9 万，美国为 424.0 万；中国该表数值高于美国约 18.9 万。与上一报告年相比，中国增长约 47.2%，欧洲与美国分别增长约 6.8% 和 8.9%。这组观察将关注点从参与数量推进到协作关系中的贡献。'),('增长速度与存量位置需要一起阅读','将 2022 年设为 100，可以看到各组相对自身起点的变化。2022—2026 年，中国表列贡献度增长约 231.6%，欧洲约 37.6%，美国约 24.5%。这个视角描述增长节奏；绝对值视角仍然保留既有规模差异。两个视图共同帮助读者避免只看排名或只看增速。'),('平均贡献提供了地方研究入口','省级样本中，浙江、台湾、上海的表列人均贡献值分别为 0.68、0.65、0.61。它提示区域研究可以同时观察规模和平均协作贡献，再结合具体项目与人才结构解释差异。平均值本身不足以说明劳动生产率，也不能为个人能力定级。')],
 takeaway='OpenRank 的价值在于让协作关系进入观察。地区贡献规模的变化，应继续连接到具体技术、项目与持续维护行为。',gap='OpenRank 算法版本、年度聚合及多平台合并记录；2.2 与 2.5 的统计范围差异说明。',bridge='贡献者所在地与项目归属地是两个观察维度。下一节转向项目。'),
 dict(key='i',code='I-MAP',name='全球开源项目影响力地图',question='贡献在哪里产生，项目影响力又积累在哪里？',headline='贡献与项目影响，在不同地区形成不同的集聚。',pillars=['OpenRankInflu'],kpi='约 160%',kpi_label='中国项目影响力较 2022 年增长',
 paragraphs=[('项目归属揭示不同的集中结构','2026 年项目归属表中，美国项目 OpenRank 影响力约为 175.1 万，中国约为 72.1 万，欧洲约为 18.3 万。欧洲在开发者贡献表中的领先位置，与这一项目影响力表中的位置并不相同。两张表描述不同对象，提示研究需要同时回答“谁在贡献”和“哪些项目连接了这些贡献”。'),('追赶速度与现有差距并存','2022—2026 年，中国项目影响力从约 27.7 万上升到 72.1 万，增长约 160%；美国从约 134.2 万上升到 175.1 万，增长约 30.5%。相对增长更快与存量仍有差距可以同时成立。读者可在绝对值与起点指数之间切换，观察两种事实。'),('把宏观差异交给后续章节解释','这组差异值得转化为具体研究：哪些项目、技术领域和组织贡献了增长？参与者与项目之间怎样形成长期连接？GOSR 提供主体样本，GOSL 提供技术分类和协作网络。现阶段不把宏观曲线归因于某个项目，也不把两个 OpenRank 指标相除得到转化效率。')],
 takeaway='把地区开源能力拆成参与、贡献与项目影响三个观察维度，有助于找到下一步需要投入的环节。',gap='项目—仓库历史映射清单、全球完整分母，以及关键项目对增长的分解。',bridge='项目之外，持续参与核心协作的人才，是理解生态长期能力的下一层。'),
 dict(key='t',code='T-MAP',name='全球开源人才地图',question='持续形成网络影响的人才，分布在哪里？',headline='北京、上海领跑，杭州与成都呈现增长活力。',pillars=['HighImpactTalent'],kpi='43.7%',kpi_label='成都固定样本人才数较 2022 年增长',
 paragraphs=[('先识别核心参与者，再讨论人才条件','本报告以个人年度全域 OpenRank 前 5% 作为高影响力开源人才的工作定义，尝试让持续协作与网络连接进入人才观察。它观察的是开源网络中的角色，不替代职业资格、学术成就或完整个人评价。'),('头部城市与增长节点同时存在','截至 2026 年 7 月的十城市表中，北京为 971 人，上海为 913 人，杭州为 486 人，深圳为 346 人，台北为 269 人。固定城市序列显示，成都从 2022 年的 126 人增至 181 人，增长约 43.7%；杭州从 350 人增至 486 人，增长约 38.9%。存量领先与增长活力可以出现在不同节点。'),('从城市数量走向培养与留存机制','城市差异为进一步研究高校、企业、项目与社区之间的连接提供了线索。真正值得追踪的是人才能否持续参与维护、承担评审与治理角色，以及新人怎样成长为长期贡献者。当前城市数量不能证明迁移或扩散；完整总体补齐前，也不推算北京、上海占全国人才的比例。')],
 takeaway='让人才政策关注持续贡献与成长路径，并用长期参与记录补充静态人数。',gap='前 5% 的基准集合、年度汇总与并列规则；全球完整人才底表及地区分母。',bridge='人才不仅在某个地方聚集，也通过项目跨越地域边界。'),
 dict(key='d',code='D-MAP',name='全球开源多样性地图',question='本土参与怎样与跨地域共建相连接？',headline='参与全球项目，与吸引全球共建，是两种互相促进的能力。',pillars=['GlobalCollabShare'],kpi='79.22%',kpi_label='中国项目样本表列本土贡献份额',
 paragraphs=[('用贡献来源观察协作结构','项目样本表中，中国项目的本土贡献份额为 79.22%；美国项目的本土贡献份额为 38.28%，中国来源贡献在美国项目表中占 7.78%。这些数值描述样本内的贡献来源结构。它们提示中国项目拥有较强的本土支撑，也为研究跨地域共同维护留下了问题。'),('多样性变化需要把幅度讲清楚','另一份固定国家份额表显示，美国、德国、中国、英国、印度五国的合计份额从 2022 年的 49.47% 变为 2026 年的 48.62%，减少 0.85 个百分点。它支持这组国家相对份额有所变化；还不足以证明所有国家之间更加均衡，或新参与国家数量增加。该表与 2.2 的来源范围尚未对齐，保留为独立观察。'),('把国际化落到共同工作的条件','国际化不仅体现为海外下载或一次性贡献，也涉及跨语言文档、贡献流程、维护者回应与治理参与。对社区来说，值得把“外部参与者能否持续留下”作为后续跟踪问题。完整贡献关系表补齐后，再进一步观察伙伴结构与长期连接。')],
 takeaway='将国际协作从参与来源的统计，推进到共同维护与共同治理的研究，与 SDG 17 的伙伴关系议题相连接。',gap='项目样本、来源份额完整分母、未知归属处理，以及完整跨地域贡献关系表。',bridge='持续的跨地域协作，需要组织、许可与公共利益方向作为支持。'),
 dict(key='g',code='G-MAP',name='全球开源治理与社会公益地图',question='哪些组织与规则，为持续协作提供条件？',headline='治理研究要同时观察组织承载、开放规则与公共实践。',pillars=['NeutralityRatio','ComplianceLicenseCov','DPGCoCreation'],kpi='+0.30',kpi_label='基金会项目影响力份额变化 · 百分点',
 paragraphs=[('基金会提供了可观察的组织入口','2022—2026 年，表列基金会活跃仓库从 3163 个增至 3350 个，增长约 5.9%；相关项目 OpenRank 份额从 2.63% 增至 2.93%。数量与份额都在上升，为研究基金会承载和连接开放协作提供了观察入口。治理效率、维护稳定性与公共效果仍需要独立证据。'),('许可证让复用条件进入研究','五类许可证样本中，MIT 活跃仓库从 57,782 个增至 71,760 个，Apache-2.0 从 37,809 个增至 47,820 个，其余三类也在期初与期末之间增长。木兰宽松许可证的累计活跃仓库从 27 个增至 391 个，项目影响力从 689 增至 2580。不同曲线分别描述采用与网络信号。'),('数字公共品需要补上具体的服务路径','第一章确立了开源与可持续发展的价值联系。本章进一步追问：哪些公共场景在使用这些成果，谁承担长期维护，公众怎样受益？基金会托管、开放许可与正式数字公共品身份分别记录。与 SDGs 的关联用于提出问题，实际公共成效通过具体项目和受益证据补充。')],
 takeaway='把“支持开源”进一步落实到长期维护、开放治理与可验证的公共场景，形成面向第六章的行动线索。',gap='基金会项目清单与份额分母；一个有来源的公共服务案例及其维护、采用和受益证据。',bridge='当协作对象从代码延伸到模型与数据，开放规则与持续维护的重要性进一步上升。'),
 dict(key='a',code='A-MAP',name='全球开源资产地图',question='AI 时代的开放供给正在怎样扩展，哪些信息仍需补齐？',headline='从代码到模型，供给扩张正在提出新的观测要求。',pillars=['OpenModelRelease','OpenDatasetRelease','AIAssetTransparency'],kpi='306.2万',kpi_label='Hugging Face 累计模型 · 2026-09-13',
 paragraphs=[('代码仓库仍是重要的协作载体','2026 年表列活跃仓库中，GitHub 约为 632.9 万、Gitee 约为 438.9 万、AtomGit 约为 60.4 万、GitLab 约为 11.8 万。依作者确认，原 GitCode 数据列以 AtomGit 品牌展示。平台整合与统计覆盖变化可能影响增长解释，因此本节保留曲线，不将品牌整合后的变化直接归因于生态自然增长。跨平台镜像与重复项目未消解前，不相加为全球唯一资产总量。'),('模型供给与发布主体共同扩张','新增模型底表记录：截至 2026 年 9 月 13 日，Hugging Face 累计可见模型为 3,062,151 个，发布者为 613,285 个。按该快照回溯的上一年同日数值分别为 1,934,821 和 413,213，增幅约 58.3% 与 48.4%。这些是报告期后的补充观察；模型记录、发布身份与完整开放程度分别理解。'),('研究覆盖率本身，也是一条重要信息','同一模型地域表中，国家已识别的模型为 71,578 个，占全部模型约 2.34%；其余约 97.66% 的发布方国家未知。已识别样本覆盖 52 个国家，但不能代表全部模型的地域结构。把未知明确展示出来，才能让地域叙事与证据覆盖相匹配。模型复用、派生与开放性评价将在 GOSM 中进一步展开。')],
 takeaway='AI 时代的观测需要同时说明供给规模、开放条件、复用关系和识别覆盖。以此连接 GOSM，而不是用发布数量代替生态质量。',gap='开放数据集供给底表、AtomGit 整合前后覆盖说明；模型与发布方归属补全计划。',bridge='七幅观察共同构成地区生态背景，后续章节将继续深入主体、技术网络与模型复用。')
]

def svg_chart(view,theme='light'):
    """Default static chart; interactive client uses the same geometry and values."""
    w=840;h=370 if view['kind']=='line' else max(210,52+len(view['x'])*34)
    ink='var(--gv-ink, #10334D)' if theme=='dark' else 'var(--gv-ink, #10334D)';grid='var(--gv-line, #CADCE5)' if theme=='dark' else 'var(--gv-line, #CADCE5)'
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{E(view["title"])}"><title>{E(view["title"])}</title><style>text{{font-family:Arial,"Noto Sans SC",sans-serif}}</style>']
    maxv=max((v for d in view['series'] for v in d['values'] if v is not None),default=1) or 1
    if view['kind']=='line':
        l,r,top,bottom=70,35,25,48;pw=w-l-r;ph=h-top-bottom
        for i in range(5):
            v=maxv*i/4;y=top+ph-ph*i/4
            s.append(f'<path d="M{l} {y}H{w-r}" stroke="{grid}"/><text x="{l-10}" y="{y+4}" text-anchor="end" fill="{ink}" font-size="11">{fmt(v)}</text>')
        for i,x in enumerate(view['x']):s.append(f'<text x="{l+i*pw/max(1,len(view["x"])-1)}" y="{h-20}" text-anchor="middle" fill="{ink}" font-size="11">{E(x[:4])}</text>')
        for d in view['series'][:8]:
            segment=[]
            for i,v in enumerate(d['values']):
                if v is None:
                    if segment:s.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{d["color"]}" stroke-width="2.5"/>');segment=[]
                    continue
                x=l+i*pw/max(1,len(view['x'])-1);y=top+ph-v/maxv*ph;segment.append(f'{x:.2f},{y:.2f}')
                s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{d["color"]}"><title>{E(d["label"])} · {view["x"][i]} · {fmt(v)} {E(view["unit"])}</title></circle>')
            if segment:s.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{d["color"]}" stroke-width="2.5"/>')
    elif view['kind']=='coverage':
        vals=view['series'][0]['values'];total=sum(vals);known=vals[0]/total
        s.append(f'<rect x="25" y="42" width="790" height="44" rx="5" fill="{grid}"/><rect x="25" y="42" width="{790*known}" height="44" rx="5" fill="var(--gv-s2, #4E87C5)"/>')
        for i,(label,val) in enumerate(zip(view['x'],vals)):
            s.append(f'<text x="25" y="{126+i*34}" fill="{ink}" font-size="17">{label} · {fmt(val)} · {val/total*100:.2f}%</text>')
    else:
        for i,(label,val) in enumerate(zip(view['x'],view['series'][0]['values'])):
            y=26+i*34
            s.append(f'<text x="142" y="{y+16}" text-anchor="end" fill="{ink}" font-size="12">{E(label)}</text><rect x="155" y="{y}" width="{max(1,val/maxv*570)}" height="22" rx="3" fill="{RC.get(label,COLORS[i%len(COLORS)])}"/><text x="{min(736,165+val/maxv*570)}" y="{y+16}" fill="{ink}" font-size="12">{fmt(val)}</text>')
    s.append('</svg>');return ''.join(s)

def table(v):
    return '<div class="reader-table-wrap"><table class="reader-table"><caption>'+E(v['title'])+' · '+E(v['unit'])+'</caption><thead><tr><th scope="col">'+('时间' if v['kind']=='line' else '对象')+'</th>'+''.join('<th scope="col">'+E(d['label'])+'</th>' for d in v['series'])+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(x)+'</th>'+''.join('<td>'+fmt(d['values'][i])+'</td>' for d in v['series'])+'</tr>' for i,x in enumerate(v['x']))+'</tbody></table></div>'

def figure(key,vv):
    v=vv[0];fid='goso-'+key
    options=''.join(f'<option value="{i}">{E(x["title"])}</option>' for i,x in enumerate(vv))
    return f'''<figure class="goso-figure" id="{fid}" data-goso-chart="{key}" aria-labelledby="{fid}-title">
      <div class="goso-chart-head"><span class="eyebrow">GOSO / {key.upper()} · 交互观察</span><h3 id="{fid}-title" data-chart-title>{E(v['title'])}</h3></div>
      <div class="goso-controls" hidden><label>观察内容<select data-view>{options}</select></label><label data-mode-label>比较方式<select data-mode><option value="absolute">原始数值</option><option value="index">起点指数 = 100</option></select></label><button type="button" data-reset>重置</button></div>
      <div class="goso-legend" data-legend>{''.join('<span><i style="background:'+d['color']+'"></i>'+E(d['label'])+'</span>' for d in v['series'])}</div>
      <div class="goso-chart-meta"><span data-unit>单位：{E(v['unit'])}</span><span class="goso-interaction-hint" hidden>选择图例聚焦 · 悬停或点选读数</span></div>
      <div class="goso-chart" data-chart>{svg_chart(v)}</div>
      <div class="goso-time-control" data-time-control hidden><label>观察年份 <output data-year-label></output><input type="range" data-year min="0" max="4" value="4" step="1" aria-label="观察年份"></label></div>
      <div class="goso-readout" data-readout aria-live="polite">{E(v['note'])}</div>
      <figcaption><p data-note>{E(v['note'])}</p><div class="goso-figure-links"><a data-source href="{v['source']}" target="_blank" rel="noopener">GitHub 数据 ↗</a><a data-csv href="{v['csv']}" download>原始 CSV ↓</a><a data-svg href="/assets/goso/{v['id']}.svg" download>当前图 SVG ↓</a><button type="button" data-share hidden>复制图表链接</button></div></figcaption>
      <details class="goso-data-table"><summary>查看数据表</summary><div data-table>{table(v)}</div></details>
      <noscript><p class="small-note">当前显示默认图与数据表；启用 JavaScript 可切换视图。其余观察视图见下方全部静态图。</p></noscript>
      <details class="goso-static-list"><summary>全部静态图与数据</summary><ul>{''.join('<li><a href="/assets/goso/'+x['id']+'.svg">'+E(x['title'])+'</a> · <a href="'+x['csv']+'" download>CSV</a></li>' for x in vv)}</ul></details>
    </figure>'''

def link(path,label):return '<a href="'+E(path)+'">'+E(label)+'</a>'
def chapter(lang):
    import goso_atlas as atlas
    import goso_editorial as editorial
    vv=views();base='/2026/'+lang+'/';all_data=json.dumps(vv,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    out=['<div class="goso-chapter" lang="zh-CN">',atlas.defs()]
    if lang=='en':out.append('<div class="reader-note" lang="en">GOSO review chapter: the Chinese manuscript and charts are shown below. English translation will follow editorial review.</div>')
    out.append('<div class="reading-tools"><span>GOSO 样章 · 2.1–2.4 已对齐 · 2026-10-15</span><div><a href="#goso-review">集中待补与评审</a><button data-print>打印本章</button></div></div><progress class="reading-progress" id="reading-progress" max="100" value="0" aria-label="本章阅读进度"></progress>')
    out.append(editorial.cover())
    out.append('<nav class="atlas-chapter-route" aria-label="七个地图视角">'+''.join('<a href="#ch02-s0'+str(i+1)+'"><b>'+s['code']+'</b><span>'+label+'</span></a>' for i,(s,label) in enumerate(zip(SECTIONS,['参与分布','协作贡献','项目影响','核心人才','跨国协作','治理公益','开放资产'])))+'</nav>')
    out.append('<details class="goso-scope"><summary>阅读说明 · 报告年度、地图快照与来源</summary><p>2.1 与本次 2.2 依据作者附件及 OpenShare 同版底表，采用 2025 自然年作为当前地图观察窗口；全球和中国地图按平台同源底图与比例绘制，中国包含 34 个省级地区。2.1 国内人数补充为条件情景；2.2 主叙事采用报告五域口径，中国贡献 442.92 万、高于美国 423.97 万，地图仍保留自然年平台参照。3D 地球分别展示虚构协作机制、实测贡献点和项目样本流向；金色虚线仅为可选的未列来源估算。2.3 同时保留 2025 自然年项目影响力快照与报告 2022—2026 年序列；2.4 的全球人才快照、五域和城市序列也分别标注。人才成长与连接模拟单列，不作为实测发现。其余小节保留各自范围，不混合计算。</p><p>早期地图采用 GitHub 固定版本 '+REF[:7]+'；本次新增图组的版本独立标注。具体文件与版本以各图就近来源说明为准；新增 2.3、2.4 复用仓库 5c31603 及 OpenShare 同源快照，并复用第五章模型底表；新增模型数据不是第一章 ATOM 外部故事快照。按作者确认开展跨年比较；尚缺的算法、样本和分母信息集中列在章末。</p><p>OpenDigger 提供主要数据与方法基础，OpenRank 帮助观察协作贡献和网络影响。账户存量、年度活跃、人才、项目和模型分别计量；五组比较不穷尽全球。未对齐的表不交叉计算，空值不补零。</p>'+link(base+'chapters/01/#ch01-s03','回到 1.3 · OSDI 方法基础')+' · '+link(base+'methodology/','完整方法与范围')+'</details>')
    for i,s in enumerate(SECTIONS):
        n=i+1;sid='ch02-s0'+str(n)
        if s['key']=='v':
            out.append(__import__('vmap_content').section(lang))
            continue
        if s['key']=='c':
            out.append(__import__('cmap_content').section(lang))
            continue
        if s['key'] in ('i','t'):
            out.append(__import__('goso_maps').section({'i':'imap','t':'tmap'}[s['key']],lang))
            continue
        out.append(f'<section class="chapter-section goso-section" id="{sid}"><div class="section-topline">2.{n} / {s["code"]}</div><h2>{s["name"]}</h2><p class="goso-question">{s["question"]}</p><div class="goso-judgment"><h3>{s["headline"]}</h3><div class="goso-kpi"><strong>{s["kpi"]}</strong><span>{s["kpi_label"]}</span></div></div>')
        primary=editorial.governance_panel() if s['key']=='g' else editorial.flow_panel() if s['key']=='d' else atlas.panel(s['key'])
        out.append(editorial.stage(s['key'],primary,figure(s['key'],vv[s['key']])))
        title,text=s['paragraphs'][0];out.append('<div class="goso-prose"><h3>'+title+'</h3><p>'+text+'</p></div>')
        out.append(atlas.original_gallery(s['key']))
        for title,text in s['paragraphs'][1:]:out.append('<div class="goso-prose"><h3>'+title+'</h3><p>'+text+'</p></div>')
        out.append('<aside class="goso-implication"><span>研究启示</span><p>'+s['takeaway']+'</p></aside>')
        out.append('<div class="goso-method-links">OSDI 查证入口（图表不等同完整指标测算）：'+' · '.join(link(base+'data/indicators/#indicator-'+k,k) for k in s['pillars'])+'</div>')
        out.append('<details class="goso-gap"><summary>待补证据 · '+s['name'].replace('全球开源','')+'</summary><p>'+s['gap']+'</p><div class="goso-blank">待补充</div>'+link('#goso-review','到章末填写评审备注 →')+'</details><p class="goso-bridge">'+s['bridge']+'</p></section>')
    out.append('<section class="goso-closing" id="goso-next"><span class="eyebrow">FROM OBSERVATION TO ACTION</span><h2>把差异变成下一步研究与行动的问题。</h2><p>七幅观测共同提示：开放参与的扩张是起点，持续贡献、共同维护和可复用供给构成不同的能力层次。对这些差异的理解，需要继续深入主体与技术网络，并以公共场景检验开放的价值。</p><div class="goso-next-grid">'+''.join(link(base+'chapters/'+n+'/',tag+' · '+label) for n,tag,label in [('03','GOSR','哪些主体形成影响'),('04','GOSL','技术网络如何演进'),('05','GOSM','模型怎样被复用与治理'),('06','行动建议','哪些条件值得持续投入')])+'</div></section>')
    out.append(review_panel(lang))
    out.append('<script type="application/json" id="goso-chart-data">'+all_data+'</script><script type="application/json" id="goso-atlas-data">'+json.dumps(atlas.payload(),ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></div>')
    return ''.join(out)

def review_panel(lang):
    gaps=[('scope','全章主张与阅读顺序','七节编号保持稳定，用三层路径串联；每节保留一个主张、主图与行动线索。'),('methods','数据口径与样本','算法版本、年度汇总、多平台合并、前 5% 基准、地区与项目样本说明。'),('geography','完整地图与分母','全球地理底表、人才完整总体、贡献来源完整关系，以及各项未知处理。'),('public','公共价值案例与开放数据','公共服务场景及受益证据；数据集供给底表与模型归属补全。')]
    out=['<section id="goso-review" class="goso-review"><span class="eyebrow">EDITORIAL REVIEW / 集中补充</span><h2>评审与待补材料</h2><p>缺口保留在相应小节，这里集中收集。备注仅保存在当前浏览器，可导出后交回；不会自动写入 GitHub。当前页面用于共同评审，后续正文与图表修订在确认后更新。</p>']
    out.append('<div class="goso-decisions"><strong>已落实的决定</strong><p>保留七节并优化衔接；开展跨年比较；GitCode 列按 AtomGit 品牌展示；缺失数据留白。附件旧称 OSIDX 统一为 OSDI，按平台推定国籍的旧建议采用现行所在地规则处理。</p></div>')
    for key,label,desc in gaps:out.append('<label class="goso-review-field" for="review-'+key+'"><strong>'+label+'</strong><span>'+desc+'</span><textarea id="review-'+key+'" data-review-key="'+key+'" rows="3" placeholder="待你补充"></textarea></label>')
    out.append('<div class="goso-review-actions"><button type="button" data-export-notes>导出评审备注 Markdown ↓</button><a href="/assets/goso/GOSO-review-draft.md" download>下载样章正文 Markdown ↓</a><span id="goso-note-status" role="status"></span></div><details><summary>本轮数据与编写记录</summary><p>核对 GitHub 最新提交 '+REF[:7]+'：第二章 13 份 CSV 未变，新增 16 份模型相关 CSV，数据目录现收录 50 份 processed CSV。本章复用两份模型供给底表，ModelRank、开放性与派生关系留给后续章节深入。原始 CSV 字段、数值及缺失均保留。</p><p>本章评审正文根据第一章、三级目录附件与本轮决策编写。原稿中的全球分母、人才占比和未验证因果判断未作为已证实结论。代码、数据与页面可继续复用为其他核心章节的样章模板。</p>'+link(REPO+'data/README.md','查看仓库数据说明 ↗')+'</details></section>')
    return ''.join(out)

def feature(lang):
    zh=lang=='zh';p='/2026/'+lang+'/chapters/02/'
    return '<section class="chapter-feature goso-feature"><div><span class="eyebrow">NEW / GOSO · CHAPTER 02</span><h2>'+('在世界地图上，读懂开源的变化。' if zh else 'Seven views of a changing ecosystem.')+'</h2><p>'+('从全球地图进入中国省级观察，联动地区读数与跨年趋势；通过人才点位、贡献流向和模型地域分布，读懂生态结构。' if zh else 'Explore the GOSO review chapter: regional trends, talent, collaboration, governance and open supply.')+'</p>'+link(p,'阅读 GOSO 样章 →' if zh else 'Read the GOSO chapter →')+'</div><div class="feature-route">'+''.join(link(p+'#ch02-s0'+str(n),label) for n,label in [(1,'01　参与、贡献与影响'),(4,'02　人才与跨地域连接'),(6,'03　治理与开放供给')])+'</div></section>'

def export(out):
    dest=out/'assets/goso';dest.mkdir(parents=True,exist_ok=True)
    import goso_atlas as atlas
    atlas.export(out)
    __import__('vmap_content').export(out)
    __import__('cmap_content').export(out)
    __import__('goso_maps').export(out)
    vv=views()
    for values in vv.values():
        for v in values:(dest/(v['id']+'.svg')).write_text(__import__('goso_brand').resolve(standalone_svg(v)))
    manuscript=['# 第二章 全球开源生态观测地图（GOSO）\n\n> 样章评审版 v0.10。数据版本 '+REF+'。尚未替换仓库正式原稿。\n\n在世界地图上，读懂开源的变化。\n\n七节沿规模、贡献与影响；人才与跨地域连接；治理与开放供给三层路径展开。地理交互图采用分别标注的 OpenShare 2026-10 页面快照、城市样本、贡献来源与模型地域底表；不将快照值并入报告年度结论。']
    for i,s in enumerate(SECTIONS):
        if s['key']=='v':
            manuscript.append(__import__('vmap_content').manuscript())
            continue
        if s['key']=='c':
            manuscript.append(__import__('cmap_content').manuscript())
            continue
        if s['key'] in ('i','t'):
            manuscript.append(__import__('goso_maps').manuscript({'i':'imap','t':'tmap'}[s['key']]))
            continue
        manuscript+=['\n## 2.'+str(i+1)+' '+s['name']+'（'+s['code']+'）\n\n**研究问题：** '+s['question']+'\n\n**核心判断：** '+s['headline']]
        for title,text in s['paragraphs']:manuscript+=['\n### '+title+'\n\n'+text]
        manuscript+=['\n**研究启示：** '+s['takeaway'],'\n**待补：** '+s['gap']+'\n\n[待填写]\n','\n**数据：**\n'+ '\n'.join('- ['+v['title']+']('+v['source']+')：'+v['note'] for v in vv[s['key']])]
    (dest/'GOSO-review-draft.md').write_text('\n'.join(manuscript)+'\n')
    (ROOT/'content/goso-review-draft.md').write_text('\n'.join(manuscript)+'\n')
    evidence={k:{'path':'data/processed/'+p,'sha256':hashlib.sha256((ROOT/'content/report-assets/data'/Path(p).name).read_bytes()).hexdigest()} for k,p in FILES.items()}
    (dest/'evidence-manifest.json').write_text(json.dumps({'source_ref':REF,'draft_status':'review','files':evidence},ensure_ascii=False,indent=2)+'\n')

def standalone_svg(v):
    import re
    chart=svg_chart(v);height=int(re.search(r'viewBox="0 0 840 (\d+)"',chart).group(1))
    inner=chart[chart.index('>')+1:chart.rfind('</svg>')]
    def wrap(text,limit=112):
        lines=[];line='';weight=0
        for c in text:
            step=2 if ord(c)>255 else 1
            if weight+step>limit:lines.append(line);line='';weight=0
            line+=c;weight+=step
        if line:lines.append(line)
        return lines
    note=wrap(('静态图显示前 8 条曲线；完整数据见 CSV。 ' if len(v['series'])>8 else '')+v['note']);legend=v['series'][:8] if v['kind']=='line' else []
    legend_rows=math.ceil(len(legend)/5);offset=78+legend_rows*25
    h=height+offset+75+len(note)*20
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {h}" role="img"><title>{E(v["title"])}</title><rect width="840" height="{h}" fill="var(--gv-surface, #FFFFFF)"/><g font-family="Arial,Noto Sans SC,sans-serif" fill="var(--gv-ink, #10334D)"><text x="28" y="30" font-size="11" fill="var(--gv-s2, #4E87C5)">GOSO · 全球开源生态观测地图 · 评审版 v0.10</text><text x="28" y="60" font-size="22">{E(v["title"])}</text>']
    for i,d in enumerate(legend):
        x=28+(i%5)*158;y=86+(i//5)*25
        s.append(f'<circle cx="{x}" cy="{y-4}" r="4" fill="{d["color"]}"/><text x="{x+10}" y="{y}" font-size="11">{E(d["label"])}</text>')
    s.append(f'<text x="28" y="{offset+10}" font-size="10">单位：{E(v["unit"])}</text></g><g transform="translate(0 {offset+15})">{inner}</g><g font-family="Arial,Noto Sans SC,sans-serif" fill="var(--gv-muted, #4C697B)" font-size="11">')
    for i,line in enumerate(note):s.append(f'<text x="28" y="{offset+height+40+i*20}">{E(line)}</text>')
    s.append(f'<text x="28" y="{h-15}" font-size="10">来源：{E(Path(FILES[v["key"]]).name)} · GitHub {REF[:7]}</text></g></svg>')
    return ''.join(s)
