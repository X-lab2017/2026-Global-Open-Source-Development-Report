"""Five ranking-first review sections, sharing the approved company visual system."""
import html
import base64
import json
import re
from pathlib import Path

E = lambda value: html.escape(str(value), quote=True)
PLANS = json.loads(Path(__file__).with_name('ranking-plans.json').read_text())
CONFIG = {
    '1': dict(letter='R', noun='地区', scopes=['region','province','city'], sources=['region','province','city','regionCountries'], views=[['ranking','structure','compare','location'],['counts','representatives'],['paired','cities']], lead='从地区名次，辨识全球开源协作的重要节点。', limits='全球行政区、中国省级与中国城市分别排序。开发者数量的单位为万，不直接解释为活跃开发者或人才密度。地理 ID 与边界版本待补，定位视图先呈现底表归属。'),
    '3': dict(letter='F', noun='基金会', scopes=['foundation'], sources=['foundation','foundationMonth'], views=[['ranking','compare'],['ranking','compare'],['monthly','change','records']], lead='从基金会整体，到旗下社区，再看位次变化。', limits='总榜原值保留；Linux 基金会含子基金会。旗下组织单独排名，模拟数值不回算整体。代表项目按当前官方名录核对；全球月度表只覆盖八家基金会。'),
    '4': dict(letter='P', noun='项目', scopes=['project','chinaProject'], sources=['project','chinaProject','projectCountries','rising'], views=[['ranking','structure','compare'],['country','domain','rising'],['overview','detail','records']], lead='从项目位次，到技术领域，再到贡献来源。', limits='全球前 30 名与中国 Top 30 保留原表；全球第 31—100 位为模拟补位。原表国家与组织标签不等同于历史发起地。项目贡献数量、国家份额、组织与仓库分组均为模拟。'),
    '5': dict(letter='E', noun='新势力', scopes=['newRepo','newProject'], sources=['newRepo','newProject','domains','languages'], views=[['ranking','launch','compare'],['ranking','portfolio','compare'],['domains','cohort','languages']], lead='从新仓库，到新项目，看技术供给如何形成。', limits='仓库与项目独立排名；新仓库可以属于老项目，新项目要求纳入仓库全部本期新建。领域原表汇总与编辑分类分开，创建批次不是历史热度。'),
    '6': dict(letter='M', noun='模型', scopes=['models'], sources=['models','tasks','publishers','series'], views=[['ranking','reuse','compare'],['ranking','landscape','coverage'],['ranking','mix','compare']], lead='从模型影响力，到任务结构，再到发布组织。', limits='2026-08 真实 Top 100，前 20 保留报告高精度。任务与组织账户各自统计版本数量，未知置底；组织账户不按母公司合并，分值不相加。官方身份资料另标核验日期。'),
}

READINGS = {
    '1':'规模与网络位置，呈现不同的组合。',
    '3':'先明确主体边界，再理解头部位置。',
    '4':'一个项目，可以连接多个仓库与维护群体。',
    '5':'单仓库聚集与多仓库供给，形成不同的早期路径。',
    '6':'头部影响力，同时分布在多个系列与版本。',
}
INTROS = {
    '1':['以全球 Top 100 行政区为样本，按国家入榜数量排序。默认展开前十名及并列国家，国旗帮助识别，代表名称帮助定位。点击国家可回到 Top 30 主榜继续查看。','左侧保留完整省级排行榜，点击省份即可联动右侧城市节点。省级名次、数值与城市原榜次同屏呈现，各自保留统计层级，城市值不加总回算省级值。'],
    '3':['沿着 2025 年 7 月至 2026 年 6 月的月度记录，查看八家基金会的位置变化。月度轨迹、起止位移与原始记录可以相互核对。','从托管项目进入维护支持：哪些项目获得支持，核心维护者的覆盖是多少，不同组织承担什么角色？以下全部使用虚构基金会与项目演示。'],
    '4':['国家汇总、编辑领域分类与中国跃升记录分别阅读。','从头部项目展开贡献国家、组织力量与仓库组。贡献数量与分组均为模拟。'],
    '5':['领域与语言分别描述新仓库 Top 30 的技术结构；创建时间帮助判断新项目和新仓库拥有多长的可观察窗口。','从首次公开可协作日开始，按相同的 30、60、90 天窗口观察参与、留存与维护角色。以下项目全部为虚构；观察不足 90 天的对象保留未成熟状态。'],
    '6':['同一份 Top 20，可以从任务、发布者和系列三个角度阅读。系列表只覆盖其中 18 个版本，另外两个版本单列保留。','以虚构模型 M0—M4 演示派生、量化、合并与适配器关系。可调整起点、跳数、类型与日期，区分已核验和待核验的模拟证据。'],
}

def clean(s):
    return re.sub(r'\[\d+\]', '', s)

def figure(s, group, data):
    p, c = PLANS[s], CONFIG[s]
    title = p['groups'][group-1][1]
    labels = p['groups'][group-1][2].split('／')
    tabs = ''.join(f'<button data-rr-view="{key}" aria-pressed="{str(i==0).lower()}">{E(label)}</button>' for i,(key,label) in enumerate(zip(c['views'][group-1],labels)))
    simulated = (s=='3' and group==2) or (s=='4' and group==3)
    period = ('排名与数值均为模拟' if s=='3' else '模拟演示 · 非实测、非预测') if simulated else p['period']
    fallback = ''
    if group == 1 or (s=='5' and group==2):
        d = data['newProject' if s=='5' and group==2 else c['scopes'][0]]
        if s=='6':
            snapshot=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/model-rankings-snapshot.json').read_text())
            d={**d,'title':'全球模型影响力 Top 100','rows':snapshot['rows']}
        keys = ['rank', d['label']] + d['metrics']
        fallback = '<table class="cr-fallback"><caption>'+E(d['title'])+'</caption><thead><tr>'+''.join('<th>'+E(k)+'</th>' for k in keys)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(r.get(k,''))+'</td>' for k in keys)+'</tr>' for r in d['rows'])+'</tbody></table>'
    note = '以原榜名次与指标横条为主。搜索覆盖完整榜单，点击名称查看档案，最多选三个同类对象对照。' if group==1 else ('全部对象和关系为虚构，用来评审观察方式；不进入真实榜单。' if simulated else '辅助观察保留自己的统计范围与分母；可切换视图、查看来源并下载当前数据。')
    if s=='5': note=['单个代码仓库独立排名。增加领域、所属项目和创建窗口；保留完整仓库路径与原表日期。','项目按原表归并，点击仓库数展开有证据的关联仓库。项目分值与人数不由仓库行简单相加。','原表分类和编辑分类分别保留。创建批次回溯本期入榜名单，帮助观察技术供给形成节奏，不等于历史月度热度。'][group-1]
    if s=='6': note=['2026-08 真实 Top 100；前 20 保留报告原始精度。任务、衍生数和下载量来自对应月记录，模型卡资料另标核验日。','任务数量榜、构成方格与供给覆盖分别呈现分类结构；每个版本只计入一个 API 主任务。未知置底并保留分母。','发布组织按平台账户分别统计，展示入榜数量、Top 20 内数量、任务覆盖、最佳模型位次与分值中位数。组织资料不改变历史榜单统计单位。'][group-1]
    if s=='4': note=['全球榜扩展为 Top 100 评审名单：前 30 名为报告原表，第 31—100 位的位次与数值为模拟。领域为编辑分类，国家沿用原表标签。','国家图直接使用真实 Top 100 汇总；领域图默认原表 Top 30。未识别放在最后并保留在分母，中国跃升表保留两期原始记录。','榜次与项目名称取自原表前十；贡献数量、国家份额、匿名组织与仓库分组均为模拟，不代表真实项目主导国。'][group-1]
    if s=='3': note=['全球 21 家原榜主体与数值保持不变。代表项目来源见档案；项目名可直接打开官方介绍。','真实组织与代表项目，排名、OpenRank 与开发者数均为模拟。只在旗下组织样本内比较，不与总榜相加。','全球月度轨迹为报告底表；Linux 基金会旗下组织轨迹为模拟。名次越小越靠前。'][group-1]
    eyebrow=('E-RANKING / '+('REPOSITORY' if group==1 else 'PROJECT') if s=='5' and group<3 else 'RANK HISTORY' if s=='3' and group==3 else 'F-RANKING / LF FAMILY' if s=='3' and group==2 else 'M-RANKING / TASKS' if s=='6' and group==2 else 'M-RANKING / ORGANIZATIONS' if s=='6' and group==3 else c['letter']+'-RANKING' if group==1 else 'SUPPLEMENT '+str(group-1))
    return f'''<figure class="cr-figure rr-figure" id="fig-3-{s}-{group}"><div class="cr-stage rr-stage goso-unified-canvas" data-slide-key="ranking-{s}-{group}" data-slide-height="{900 if (s in ['4','6'] and group==1) or (s=='5' and group<3) else 820}" data-lang="zh" data-rr-section="{s}" data-rr-group="{group}" role="group" aria-label="{E(title)}"><div class="cr-board">
<header class="cr-head"><div><span class="cr-eyebrow">图 3-{s}-{group} / {eyebrow}</span><h4>{E(title)}</h4></div><div class="cr-head-right"><span>{E(period)}</span><button data-rr-action="source">口径与来源 ↗</button></div></header>
<div class="cr-toolbar"></div><nav class="cr-tabs" aria-label="{E(title)}视图">{tabs}</nav><div class="cr-body">{fallback}</div><footer class="cr-foot"><span class="cr-status" role="status"></span><button data-rr-action="image">导出 SVG ↓</button><button data-rr-action="export">下载当前数据 ↓</button></footer><div class="cr-overlay" hidden role="dialog" aria-modal="true" aria-label="详细信息"></div></div></div><figcaption>{note}</figcaption></figure>'''

def foundation_section(data,repo):
    s='3'
    out=['''<section class="chapter-section gosr-section cr-section rr-section" id="ch03-s03"><div class="section-topline"><span>3.3 / F-RANKING</span><span>基金会榜单 · 交互评审版 1.2</span></div><h2>全球开源基金会影响力排行榜</h2><p class="cr-lead">从基金会整体，到旗下社区，再看位次变化。</p><p class="cr-intro">先看全球基金会的影响力与代表项目，再展开 Linux 基金会旗下的子基金会和伞形社区。两级榜单分别阅读，时序图帮助观察各自的位置变化。</p><nav class="cr-section-nav" aria-label="基金会榜单阅读路径"><a href="#fig-3-3-1">全球基金会榜 ↓</a><a href="#fig-3-3-2">Linux 基金会旗下组织榜</a><a href="#fig-3-3-3">位次变化</a></nav>''']
    out.append(figure(s,1,data))
    out.append('''<p class="fr-brief-reading">Linux 基金会、开放原子开源基金会与 Apache 软件基金会位列原榜前三。代表项目作为理解组织范围的入口；点击项目可查看官方介绍。</p><section class="cr-supplement fr-rank-supplement" id="rr-3-supp-2"><div class="cr-supplement-heading"><span>第二级榜单 / LINUX FOUNDATION</span><h3>展开 Linux 基金会，观察旗下组织与代表项目。</h3><p>参照官方 Landscape，选择主要子基金会与伞形社区进行内部比较。组织和项目名称有官方来源；本图排名与指标数值暂为模拟，供评审。</p></div>''')
    out.append(figure(s,2,data))
    out.append('''</section><section class="cr-supplement" id="rr-3-supp-3"><div class="cr-supplement-heading"><span>时序观察 / 排名轨迹</span><h3>同一层级内，看哪些位置稳定、哪些发生变化。</h3><p>切换全球基金会与 Linux 基金会旗下组织，查看月度轨迹、期间位移和记录。全球范围沿用现有八家基金会月度底表；旗下组织轨迹为模拟。</p></div>''')
    out.append(figure(s,3,data))
    out.append('''</section><details class="cr-method-inline"><summary>来源与统计口径</summary><p>总榜保留原始 21 家主体、名次与分值，统计期为 2025.07—2026.06。Linux 基金会在原表中含子基金会；新增内部榜单不与整体条目混排，不加总回算整体 OpenRank。原表中的其他主体边界保持原样。</p><p>代表项目根据当前官方名录核对，不表示完整项目清单，也不表示其必然纳入本期分值。旗下组织的排名、数值与月度轨迹均为模拟，官方来源只支持名称与项目关系。</p><p>月度名次不平均为年度排名。缺失保持缺失，不补零；名次变化不等于影响力增长率。</p><p><a href="https://landscape.linuxfoundation.org/" target="_blank" rel="noopener">Linux 基金会官方 Landscape ↗</a> · <a href="/assets/gosr/foundation-reference.json" download>组织与代表项目来源清单 ↓</a></p>''')
    for key in ['foundation','foundationMonth']:
        d=data[key]
        out.append(f'<p><a href="/assets/gosr/data/{d["file"]}" download>{E(d["title"])} · 原始 CSV ↓</a> · <a href="{repo}data/processed/chapter3/{d["file"]}" target="_blank" rel="noopener">固定版本来源 ↗</a></p>')
    out.append('</details><nav class="cr-end-nav"><a href="#fig-3-3-1">↑ 返回基金会排行榜</a><a href="#ch03-s04">继续阅读 · 项目排行榜 →</a></nav></section>')
    return ''.join(out)

def project_section(data,repo):
    s='4'
    out=['<section class="chapter-section gosr-section cr-section rr-section" id="ch03-s04"><div class="section-topline"><span>3.4 / P-RANKING</span><span>项目榜单 · 交互评审版 1.2</span></div><h2>全球开源项目影响力排行榜</h2><p class="cr-lead">从项目位次，到技术领域，再到贡献来源。</p><p class="cr-intro">以 Top 100 项目榜单为主体，结合技术领域、原表国家与组织标签认识项目；再看榜单分布，以及头部项目的贡献来自哪些国家和力量。</p><nav class="cr-section-nav" aria-label="项目榜单阅读路径"><a href="#fig-3-4-1">项目 Top 100 ↓</a><a href="#fig-3-4-2">分布与位次变化</a><a href="#fig-3-4-3">头部项目贡献来源</a></nav>']
    out.append(figure(s,1,data))
    out.append('<section class="cr-supplement" id="rr-4-supp-2"><div class="cr-supplement-heading"><span>榜单结构 / 分布与变化</span><h3>哪些国家、哪些领域进入榜单？哪些项目向前移动？</h3><p>国家分布保留真实 Top 100 汇总，未识别项目置底。领域图按统一的九类编辑分类展开；中国跃升记录独立展示。</p></div>')
    out.append(figure(s,2,data))
    out.append('</section><section class="cr-supplement" id="rr-4-supp-3"><div class="cr-supplement-heading"><span>榜单观察 01 / 贡献来源</span><h3>一个项目，可以连接多个仓库与维护群体。</h3><p>从全球原榜前十出发，对比各项目的贡献国家分布；点击项目，联动查看组织力量与仓库分工。数值暂用模拟，供评审观察方式。</p></div>')
    out.append(figure(s,3,data))
    out.append('</section><details class="cr-method-inline"><summary>来源、模拟范围与统计口径</summary><p>全球前 30 名、中国 Top 30、Top 100 国家汇总和中国跃升表均保留报告原值。全球第 31—100 位采用真实项目名称补齐界面，位次、OpenRank 与活跃开发者均为模拟，不是正式全球排名。</p><p>原表的国家与组织标签可能包含现托管方，不能直接视为历史发起国家或发起者。项目领域与细分方向为依据官方介绍的编辑分类；官网只支持身份和技术用途，不支持模拟排名。</p><p>贡献图以合并 PR 数为单位。模拟联合表将每条 PR 归入一个国家、一个组织和一个仓库组，各视图总量一致。国家表示贡献者所在地，未识别保留在分母；独立贡献者与组织未识别分开。贡献领先不等于治理控制权，真实主导力量待数据补齐后判断。</p><p><a href="/assets/gosr/project-reference.json" download>官方入口与编辑分类 ↓</a> · <a href="/assets/gosr/project-review-simulated.json" download>模拟名单与贡献联合表 ↓</a></p>')
    for key in CONFIG[s]['sources']:
        d=data[key]
        out.append(f'<p><a href="/assets/gosr/data/{d["file"]}" download>{E(d["title"])} · 原始 CSV ↓</a> · <a href="{repo}data/processed/chapter3/{d["file"]}" target="_blank" rel="noopener">固定版本来源 ↗</a></p>')
    out.append('</details><nav class="cr-end-nav"><a href="#fig-3-4-1">↑ 返回项目排行榜</a><a href="#ch03-s05">继续阅读 · 开源新势力 →</a></nav></section>')
    return ''.join(out)

def focused_section(number,data,repo):
    s=str(number)
    settings={
        1:dict(title='全球开源地区影响力排行榜',short='地区榜单',lead='从全球行政区，到中国省市，看见开源协作节点。',intro='各层级独立排名。主榜保留影响力和开发者规模，国家分布与省市联动帮助定位重要节点。',nav=['地区排行榜','国家入榜分布','中国省市节点'],heads=[('榜单结构 / 国家分布','哪些国家拥有更多入榜行政区？','以全球 Top 100 行政区为样本，保留并列名次，默认展开前十名及并列国家。'),('节点观察 / 省市联动','省级位置与城市节点，在同一图中阅读。','完整省级榜与城市原榜次联动显示，省级和城市数值各自保留，不相加。')]),
        5:dict(title='全球新势力开源仓库与项目排行榜',short='新势力榜单',lead='从新仓库，到新项目，看技术供给如何形成。',intro='先看单个新仓库，再看由仓库组成的新项目。两个排行榜各自保留位次，关联视图连接对象，技术领域和创建批次补充结构观察。',nav=['新仓库排行榜','新项目排行榜','技术领域与创建批次'],heads=[('第二级榜单 / 新项目','从单仓库进入多仓库项目。','新仓库可以属于老项目；新项目要求纳入仓库全部在本期新建。点击仓库数，展开已核对的关联对象。'),('技术观察 / 领域与批次','哪些技术密集出现，又在哪些批次形成？','领域图比较仓库与项目的不同结构，创建日期追溯本期入榜对象的形成节奏。原表分类与编辑分类分别保留。')]),
        6:dict(title='全球开源模型影响力排行榜',short='模型榜单',lead='从模型影响力，到任务结构，再到发布组织。',intro='以 2026 年 8 月真实 Top 100 为主体，分别观察任务供给结构与发布组织布局。',nav=['模型 Top 100','任务结构与覆盖','发布组织榜'],heads=[('任务观察 / 分类与覆盖','影响力前列，聚集了哪些任务？','数量榜呈现分类位置，构成方格展示样本占比，覆盖图连接任务与发布账户。'),('组织观察 / 发布与供给','哪些组织持续提供入榜模型，覆盖怎样的任务？','按发布账户统计入榜版本，结合头部位置、任务覆盖和分值中位数观察。组织身份有证据可查，同一母公司下不同账户分别保留。')])}
    q=settings[number];c=CONFIG[s]
    out=[f'<section class="chapter-section gosr-section cr-section rr-section" id="ch03-s0{s}"><div class="section-topline"><span>3.{s} / {c["letter"]}-RANKING</span><span>{q["short"]} · 交互评审版 1.2</span></div><h2>{q["title"]}</h2><p class="cr-lead">{q["lead"]}</p><p class="cr-intro">{q["intro"]}</p><nav class="cr-section-nav" aria-label="{q["short"]}阅读路径">'+''.join(f'<a href="#fig-3-{s}-{i}">{label}{" ↓" if i==1 else ""}</a>' for i,label in enumerate(q['nav'],1))+'</nav>']
    out.append(figure(s,1,data))
    for group,(eyebrow,title,description) in enumerate(q['heads'],2):
        out.append(f'<section class="cr-supplement" id="rr-{s}-supp-{group}"><div class="cr-supplement-heading"><span>{eyebrow}</span><h3>{title}</h3><p>{description}</p></div>')
        out.append(figure(s,group,data));out.append('</section>')
    out.append('<details class="cr-method-inline"><summary>来源与统计口径</summary><p>'+c['limits']+'</p>')
    if number==1:out.append('<p>全球行政区、中国省级和中国城市分别排序。开发者单位为万，省级与城市值不相加；入榜数量不代表国家影响力份额。</p>')
    if number==5:out.append('<p>仓库和首仓创建日期均沿用原表，不等同于项目成立或技术诞生。官网关系只用于关联导航，不替代报告完整仓库映射；CANN 的 68 仓库保留原值，不自动归入所有 Ascend 仓库。</p><p>技术领域原表汇总与逐项编辑分类分别显示。创建批次仅追溯本期入榜名单，不推断全生态历史热度或增长速度。</p><p><a href="/assets/gosr/emerging-reference.json" download>仓库、项目关联与编辑分类证据 ↓</a></p>')
    if number==6:out.append('<p>公开模型站前 20 名与报告的模型、顺序和两位小数值一致；原始高精度保持不变，21—100 名按公开月榜补齐。下载、点赞、衍生数是对应月记录的附加指标，不表示当月新增，详细窗口与去重口径待补。</p><p>模型卡资料核验于 2026-10-17，与 2026-08 榜单分开。参数的范围因模型而异，许可证名称不等于开放程度评分。国家仅原报告 20 项已有标签，其余不按发布者名称推断。</p><p><a href="http://47.100.76.186:9529/models" target="_blank" rel="noopener">OpenGauge 模型站 ↗</a> · <a href="/assets/gosr/model-rankings-snapshot.json" download>原始模型榜快照 ↓</a> · <a href="/assets/gosr/model-reference.json" download>官方模型卡参考 ↓</a></p>')
    for key in c['sources']:
        d=data[key];out.append(f'<p><a href="/assets/gosr/data/{d["file"]}" download>{E(d["title"])} · 原始 CSV ↓</a> · <a href="{repo}data/processed/chapter3/{d["file"]}" target="_blank" rel="noopener">固定版本来源 ↗</a></p>')
    nextlink=f'<a href="#ch03-s0{number+1}">继续阅读下一榜单 →</a>' if number<6 else '<a href="#gosr-review">本章数据与口径 →</a>'
    out.append(f'</details><nav class="cr-end-nav"><a href="#fig-3-{s}-1">↑ 返回{q["short"]}</a>{nextlink}</nav></section>');return ''.join(out)

def section(number, data, repo):
    if number in [1,5,6]:return focused_section(number,data,repo)
    if number==3:return foundation_section(data,repo)
    if number==4:return project_section(data,repo)
    s = str(number)
    p, c = PLANS[s], CONFIG[s]
    intro = next((v for k,v in p['body'] if k=='开篇文案'),p['core'])
    out = [f'''<section class="chapter-section gosr-section cr-section rr-section" id="ch03-s0{s}"><div class="section-topline"><span>3.{s} / {c['letter']}-RANKING</span><span>{p['short']} · 交互评审版 1.2</span></div><h2>{E(p['title'])}</h2><p class="cr-lead">{E(c['lead'])}</p><p class="cr-intro">{E(clean(intro))}</p><nav class="cr-section-nav" aria-label="{c['noun']}榜单阅读路径"><a href="#fig-3-{s}-1">本期排行榜 ↓</a><a href="#rr-{s}-supp-2">补充 · {E(p['groups'][1][1])}</a><a href="#rr-{s}-supp-3">补充 · {E(p['groups'][2][1])}</a><a href="#rr-{s}-actions">行动主张</a></nav>''']
    out.append(figure(s,1,data))
    body = (READINGS[s], p['body'][1][1])
    out.append(f'<div class="cr-reading"><span>榜单观察 01</span><h3>{E(body[0])}</h3><p>{E(clean(body[1]))}</p></div><details class="cr-method-inline"><summary>核心问题与指标定位</summary><p><strong>{E(p["core"])}</strong></p><p>{E(c["limits"])}</p><a href="/2026/zh/data/indicators/">查看 OSDI 指标词典 →</a></details>')
    for group,key in [(2,'auxa'),(3,'auxb')]:
        a = p[key]
        out.append(f'<section class="cr-supplement" id="rr-{s}-supp-{group}"><div class="cr-supplement-heading"><span>补充观察 0{group-1} / {"虚构案例" if group==3 and s!="1" else "已有底表"}</span><h3>{E(a["title"])}</h3><p>{E(INTROS[s][group-2])}</p></div>')
        out.append(figure(s,group,data))
        if a.get('read'):
            out.append(f'<div class="cr-reading"><span>阅读线索</span><p>{E(clean(a["read"]))}</p></div>')
        out.append('</section>')
    out.append(f'<section class="cr-actions" id="rr-{s}-actions"><span class="cr-eyebrow">从观察到行动</span><h3>让榜单观察，连接下一步行动。</h3>')
    for i,(title,body) in enumerate(p['actions'],1):
        out.append(f'<article><span>0{i}</span><div><h4>{E(title)}</h4><p>{E(clean(body))}</p></div></article>')
    out.append(f'</section><details class="cr-method-inline"><summary>来源、统计窗口与解释边界</summary><p>{E(c["limits"])}</p><p>真实数据固定到报告底表版本，原始 CSV 保持不变。模拟探索仅使用虚构对象，筛选、档案与导出中均保留模拟标记。</p>')
    for key in c['sources']:
        d=data[key]
        out.append(f'<p><a href="/assets/gosr/data/{d["file"]}" download>{E(d["title"])} · 原始 CSV ↓</a> · <a href="{repo}data/processed/chapter3/{d["file"]}" target="_blank" rel="noopener">来源底表 ↗</a></p>')
    nextlink = f'<a href="#ch03-s0{number+1}">继续阅读下一榜单 →</a>' if number<6 else '<a href="#gosr-review">本章证据与后续补充 →</a>'
    out.append(f'</details><nav class="cr-end-nav"><a href="#fig-3-{s}-1">↑ 返回{c["noun"]}排行榜</a>{nextlink}</nav></section>')
    return ''.join(out)

def payload():
    flag_dir=Path(__file__).resolve().parents[1]/'content/gosr/flags'
    flags=json.loads((flag_dir/'provenance.json').read_text())['countries']
    flags={name:{'code':meta['code'],'data':'data:image/svg+xml;base64,'+base64.b64encode((flag_dir/meta['file']).read_bytes()).decode()} for name,meta in flags.items()}
    flag_script='<script id="region-flags" type="application/json">'+json.dumps(flags,ensure_ascii=False)+'</script>'
    foundation_reference=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/foundation-reference.json').read_text())
    foundation_reference['simulation']=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/foundation-lf-simulated.json').read_text())
    foundation_script='<script id="foundation-reference-data" type="application/json">'+json.dumps(foundation_reference,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    project_reference=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/project-reference.json').read_text())
    project_reference['simulation']=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/project-review-simulated.json').read_text())
    project_script='<script id="project-reference-data" type="application/json">'+json.dumps(project_reference,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    emerging=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/emerging-reference.json').read_text())
    emerging_script='<script id="emerging-reference-data" type="application/json">'+json.dumps(emerging,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    model_reference=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/model-reference.json').read_text())
    snapshot=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/model-rankings-snapshot.json').read_text())
    model_reference['snapshot']={k:v for k,v in snapshot.items() if k not in ['monthly_top100','history','months']}
    model_reference['organizations']=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/model-organization-reference.json').read_text())
    model_script='<script id="model-reference-data" type="application/json">'+json.dumps(model_reference,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    return model_script+emerging_script+project_script+foundation_script+flag_script+'<script id="rankings-data" type="application/json">'+json.dumps(CONFIG,ensure_ascii=False).replace('<','\\u003c')+'</script>'
