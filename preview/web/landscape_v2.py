"""4.1 reviewed landscape: one pinned cohort, monthly evidence, explicit simulation."""
from pathlib import Path
import csv, json, math, random, textwrap
import landscape_content as L
E=L.E
MONTHS=[f'2025-{m:02d}' for m in range(9,13)]+[f'2026-{m:02d}' for m in range(1,9)]
COUNTRIES=[('US','美国','#3c84b5'),('CN','中国','#d18739'),('DE','德国','#8771ae'),('IN','印度','#42a597'),('GB','英国','#c76f88'),('JP','日本','#8f984a'),('CA','加拿大','#6483cc'),('OTHER','其他','#8998a4'),('UNKNOWN','未知','#b6bcc2')]

def simulation():
    """Synthetic actors overlap across categories: scope counts must be a set union."""
    rng=random.Random(341);out=[]
    for si,(key,*_) in enumerate(L.SECTIONS):
        weights=[rng.uniform(.3,1.2) for _ in range(7)]+[.65,.45]
        weights[0]*=2.5;weights[1]*=2.1
        if si in [4,7,23]:weights[1]*=2.5
        if si in [14,20]:weights[0]*=1.6
        for mi in range(12):
            w=[v*(1+.20*math.sin(mi*.46+ci*.7+si*.2)) for ci,v in enumerate(weights)]
            den=sum(w)
            for ci,(code,*_) in enumerate(COUNTRIES):
                # Each category-month totals 4000/12; weights are unrelated to real OpenRank.
                value=4000/12*w[ci]/den
                pool=[2400,2200,1200,1500,1000,900,850,1400,1100][ci]
                count=max(3,round(value*1.8))
                actors=[f'SIM-{code}-{(si*(pool//25)+mi*7+j)%pool:04d}' for j in range(min(pool,count))]
                out.append({'section':key,'month':mi,'country':code,'value':value,'actors':actors})
    return out

def world_paths():
    # Reuse the report's reviewed world geometry, including its China presentation.
    world=json.loads((L.ROOT/'content/vmap/source/world.json').read_text())
    codes={'United States':'US','China':'CN','Germany':'DE','India':'IN','United Kingdom':'GB','Japan':'JP','Canada':'CA'}
    result=[]
    for f in world['features']:
        name=f['properties']['name']
        if name=='Antarctica':continue
        geo=f['geometry'];polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
        parts=[]
        for poly in polys:
            for ring in poly:
                pts=[(round((lon+180)*2.45,1),round((85-lat)*2.75,1)) for lon,lat,*_ in ring]
                if pts:parts.append('M'+'L'.join(f'{x},{y}' for x,y in pts)+'Z')
        result.append({'name':name,'code':codes.get(name),'d':''.join(parts)})
    return result

def payload():
    return {'version':'4.1-v2','months':MONTHS,'projects':L.PROJECTS,'sections':L.SECMAP,'countries':[{'code':c,'name':n,'color':x} for c,n,x in COUNTRIES],'simulation':simulation(),'world':world_paths(),'source':L.REPO+'data/agentic-ai-projects.csv','commit':L.REF}

def select(id,options,label):
    return f'<label>{label}<select id="{id}">'+''.join(f'<option value="{E(v)}">{E(t)}</option>' for v,t in options)+'</select></label>'

def table(headers,rows):
    return '<div class="al-table-wrap"><table><thead><tr>'+''.join(f'<th scope="col">{E(x)}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{E(x)}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def map_svg(layer):
    sections=[s for s in L.SECTIONS if (s[2]=='model')==(layer=='Model Infra')]
    # Fixed four-column masonry. No rank-driven rearrangement when month changes.
    heights=[70]*4;cards=[];W=1440;cw=346;gap=12
    for key,zh,stage,desc in sections:
        pp=sorted([p for p in L.PROJECTS if p['section']==key],key=lambda p:p['name'].lower())
        col=min(range(4),key=lambda i:heights[i]);x=col*(cw+gap)+10;y=heights[col];h=85+math.ceil(len(pp)/2)*51
        heights[col]+=h+gap
        total=sum(p['aug'] or 0 for p in pp);cover=sum(p['aug'] is not None for p in pp)
        accent={'application':'#3c84b5','framework':'#8771ae','runtime':'#42a597','model':'#d18739'}[stage]
        card=f'<g class="al-map-card" data-section="{E(key)}"><rect x="{x}" y="{y}" width="{cw}" height="{h}" rx="9" fill="var(--gv-raised)" stroke="var(--gv-line)"/><rect x="{x}" y="{y+10}" width="4" height="{h-20}" rx="2" fill="{accent}"/><text x="{x+14}" y="{y+28}" font-size="20" font-weight="650">{E(zh)}</text><text class="al-map-stat" x="{x+14}" y="{y+53}" font-size="15" fill="var(--gv-muted)">{len(pp)} 项目 · OR {total:,.2f} · {cover}/{len(pp)} 有值</text>'
        for j,p in enumerate(pp):
            px=x+12+(j%2)*164;py=y+76+(j//2)*51
            name=p['name'];chunks=textwrap.wrap(name,width=16,break_long_words=True,break_on_hyphens=False)
            card+=f'<a href="https://github.com/{E(p["repo"])}" class="al-map-project" data-project="{p["id"]}" aria-label="{E(p["name"])} 项目详情"><title>{E(p["repo"])}</title><rect x="{px-4}" y="{py-13}" width="160" height="46" rx="5" fill="var(--gv-surface)"/>'
            if p['logo']:card+=f'<image href="/assets/landscape/logos/{E(p["logo"])}" x="{px}" y="{py-7}" width="24" height="24"/>'
            else:card+=f'<text x="{px+5}" y="{py+10}" font-size="19">{E(name[0].upper())}</text>'
            for k,chunk in enumerate(chunks[:2]):card+=f'<text x="{px+29}" y="{py+3+k*15}" font-size="14">{E(chunk)}</text>'
            card+='</a>'
        cards.append(card+'</g>')
    H=max(heights)+35
    legend=''.join(f'<rect x="{235+i*155}" y="20" width="12" height="12" fill="{c}"/><text x="{255+i*155}" y="32" font-size="16">{n}</text>' for i,(n,c) in enumerate([('任务入口','#3c84b5'),('构建与编排','#8771ae'),('运行与治理','#42a597')])) if layer=='Agent Infra' else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="group" aria-label="{layer} 完整分类全景"><rect width="{W}" height="{H}" fill="var(--gv-surface)"/><text x="12" y="33" font-size="27" font-weight="700">{layer}</text>{legend}<text class="al-map-period" x="1430" y="33" text-anchor="end" font-size="17">2026-08 · 真实观测 · {sum(len([p for p in L.PROJECTS if p["section"]==s[0]]) for s in sections)} 项目</text>'+''.join(cards)+f'<text x="12" y="{H-10}" font-size="14" fill="var(--gv-muted)">分类图不表示依赖关系；所有者图标用于识别，项目名称区分仓库。来源：antgroup/agentic-ai-landscape · {L.REF[:7]}</text></svg>'

def panel(id,num,title,desc,body='',sim=False,controls=''):
    badge='<span class="al-badge al-sim">模拟数据 · 不用于事实判断</span>' if sim else '<span class="al-badge">真实观测 · 固定样本</span>'
    return f'''<article class="al-panel" id="{id}" data-chart="{id}"><header class="al-panel-heading"><div><span class="eyebrow">{num}</span><h4>{title}</h4></div>{badge}</header><p class="al-description">{desc}</p><div class="al-controls">{controls}<div class="al-chart-tools"><button type="button" data-expand="{id}">全屏</button><button type="button" data-svg="{id}">SVG ↓</button><button type="button" data-csv="{id}">CSV ↓</button></div></div><div class="al-view">{body or '<p class="al-fallback">启用 JavaScript 可按月探索；下方为最新月份的静态数据，完整记录可下载。</p>'}</div><p class="al-readout" aria-live="polite"></p><details class="al-data"><summary>精确数据与完整记录</summary><div class="al-data-body"></div></details><p class="al-source">{'独立模拟数据 SIM-341 · 仅评审图形与交互。' if sim else '来源：Landscape 精选主表 · 最新观测 2026-08 · 空值不计作 0。'} <a href="#land-evidence">查看口径</a></p></article>'''

def chapter():
    cat=select('al-category',[(k,v['name']) for k,v in L.SECMAP.items()],'子类别')
    months=select('al-month',[(str(i),m) for i,m in reversed(list(enumerate(MONTHS)))],'观测月份')
    scope=select('al-scope',[('all','整个领域 · 145 项目'),('Agent Infra','Agent Infra · 86 项目'),('Model Infra','Model Infra · 59 项目')],'观测范围')
    top=sorted([(sum(p['aug'] or 0 for p in L.PROJECTS if p['section']==k),zh) for k,zh,*_ in L.SECTIONS],reverse=True)
    fallback=table(['子类别','2026-08 OpenRank'],[(n,f'{v:,.2f}') for v,n in top])
    out=['''<div class="goso-chapter al-chapter" data-landscape-version="4.1-v2"><section id="ch04-s01" class="chapter-section"><div class="section-topline"><span>4.1 / AGENTIC AI LANDSCAPE</span><span>2026.10.17 · 评审版</span></div><h2>Agentic AI：技术全景与生态演变</h2><p class="al-thesis">看清技术结构，<br>追踪影响力流动。</p><p class="al-lede">从完整分类图出发，逐月观察子领域与项目的位次变化，再看贡献来自哪里。两层基础设施、同一组精选项目，构成持续观察 Agentic AI 开源生态的窗口。</p><div class="al-kpis"><div><strong>145</strong><span>精选开源项目</span></div><div><strong>25</strong><span>技术子类别</span></div><div><strong>12</strong><span>个月 · 2025.09—2026.08</span></div><div><strong>140 / 145</strong><span>最新月份有观测值</span></div></div><nav class="al-jump" aria-label="4.1 阅读路径"><a href="#land-map">01 全景</a><a href="#land-trends">02 排行与演变</a><a href="#land-country">03 国家贡献</a><a href="#land-extensions">04 结构洞察</a><a href="#land-action">05 政策建议</a></nav><p class="al-note">项目与 OpenRank 使用仓库真实数据；国家贡献及相关扩展使用独立模拟数据。最新可用月份为 2026 年 8 月，不将缺失月份补成 0。</p>''']
    out.append(f'<div class="al-global al-controls">{scope}{months}<span id="al-global-status" aria-live="polite">140 / 145 项目有值 · OpenRank 5,706.38</span></div>')
    out.append('<section class="al-section" id="land-map"><span class="eyebrow">01 / THE LANDSCAPE</span><h3>两张全景，完整呈现技术分类</h3><p>Agent Infra 连接任务入口、构建编排与运行治理；Model Infra 提供数据、训练、推理和计算能力。分类位置保持固定，月份切换只更新影响力与覆盖情况。搜索可高亮项目，点击名称查看详情。</p>')
    for id,layer,num in [('al-agent','Agent Infra','4.1-01'),('al-model','Model Infra','4.1-02')]:
        out.append(panel(id,num,layer+' · '+('86 项目 / 12 类' if 'Agent' in layer else '59 项目 / 13 类'),'全量展示 · 名称与标识并列 · 横向滚动或全屏放大查看',map_svg(layer),controls=f'<label>查找项目<input type="search" data-search="{id}" placeholder="项目名称 / 仓库"></label><label>缩放<select data-zoom="{id}"><option value="1">适应宽度</option><option value="1.5">150%</option><option value="2">200%</option></select></label>'))
    out.append('</section><section class="al-section" id="land-trends"><span class="eyebrow">02 / MONTHLY EVOLUTION</span><h3>子类别与项目，逐月看位次和份额</h3><p>当前月份回答“影响力分布在哪里”，连续 12 个月回答“结构如何变化”。每个月独立计算排行，并同时呈现当月覆盖情况；历史变化描述的是当前精选样本的回溯，不等同于当时全领域的完整普查。</p>')
    out.append(panel('al-category-rank','4.1-03','子类别 OpenRank 排行','点击子类别联动项目榜与国家贡献；完整表含份额、覆盖率及可比项目环比。',fallback))
    out.append(panel('al-category-heat','4.1-04','12 个月的分类位次与份额','位次按月重排。颜色越深表示位次越高、原值或份额越大；同时关注覆盖变化。',controls=select('al-heat-mode',[('rank','月度位次'),('value','OpenRank 原值'),('share','当月领域份额')],'显示内容')))
    out.append(f'<div class="al-controls al-category-controls">{cat}<span>类别选择联动以下项目视图与国家贡献范围。</span></div>')
    out.append(panel('al-category-trend','4.1-05','所选子类别的影响力轨迹','同图查看数值或领域份额，选择类别后原位更新。',controls=select('al-category-mode',[('value','OpenRank 原值'),('share','当月领域份额')],'指标')))
    out.append(panel('al-project-rank','4.1-06','子类别内的项目排行','所选月份重新排序；切换完整榜单可查看全部项目。点击项目打开详情。',controls=select('al-project-limit',[('10','Top 10'),('all','全部项目')],'榜单范围')))
    out.append(panel('al-project-trend','4.1-07','项目趋势与全部项目位次','默认选取当前类别前 3 个项目，可对比 1—5 个项目；断线表示无观测，创建前不补零。',controls=select('al-project-view',[('line','项目 OpenRank 曲线'),('rank','全部项目位次矩阵')],'视图')+'<div id="al-project-picks" class="al-picks"></div>'))
    out.append('</section><section class="al-section" id="land-country"><span class="eyebrow">03 / GEOGRAPHY OF CONTRIBUTION</span><h3>贡献来自哪里，集中在哪些子领域</h3><p>以下国家图表使用一致的独立模拟数据，用于评审排行、地图及下钻方式。贡献所在地不代表国籍，贡献份额也不能直接推导项目治理权或产业控制力。</p>')
    country_scope=select('al-country-scope',[('all','当前观测范围 · 全部类别')]+[(k,v['name']) for k,v in L.SECMAP.items()],'国家贡献范围')
    out.append(panel('al-country-rank','4.1-08','国家贡献排行与世界分布','地图与榜单联动。点击国家查看其技术贡献分布；“其他”和“未知”始终保留在分母中。',sim=True,controls=country_scope+select('al-country-period',[('rolling','最近 12 个月 · 2025.09—2026.08'),('month','当前选定月份')],'统计期')))
    out.append(panel('al-country-detail','4.1-09','所选国家的技术贡献分布','点击国家后更新。下钻显示该国在各类别的贡献，以及各类别在该国贡献中的占比。',sim=True))
    out.append(panel('al-country-stack','4.1-10','每个子类别的国家贡献结构','各行合计 100%；国家颜色、图例顺序固定。点击子类别查看完整国家榜单。',sim=True))
    out.append('</section><section class="al-section" id="land-extensions"><span class="eyebrow">04 / STRUCTURAL INSIGHTS</span><h3>四个角度，进一步理解生态结构</h3>')
    out.append(panel('al-concentration','E1','头部集中度：每类 Top 3 占比','在所选月有观测的项目内计算。小样本类别天然容易集中，因此同时呈现项目数与观测覆盖。'))
    out.append(panel('al-shift','E2','结构迁移：共同观测样本的份额变化','默认比较 2026 年 5—8 月。仅保留所选起止区间每个月都有观测的项目，减轻新增观测对变化的干扰。',controls=select('al-shift-start',[(str(i),m) for i,m in enumerate(MONTHS[:-1])],'比较起点')+select('al-shift-end',[(str(i),m) for i,m in enumerate(MONTHS[1:],1)],'比较终点')))
    out.append(panel('al-specialization','E3','国家技术专长矩阵','LQ = 该国在子类别的贡献份额 ÷ 该国在当前整个观测范围的贡献份额。大于 1 表示相对专长，不等于绝对领先。',sim=True))
    out.append(panel('al-country-trend','E4','12 个月国家贡献份额演变','沿用上方国家贡献范围；每个月以该范围的全部贡献为分母，保留其他与未知。',sim=True))
    out.append('''</section><section class="al-section" id="land-action"><span class="eyebrow">05 / POLICY IMPLICATIONS</span><h3>从观测走向行动</h3><div class="al-policy"><article><span>01 / 技术结构</span><h4>按技术结构配置持续支持</h4><p>结合分类覆盖、头部集中度与维护需求，支持公共基础设施的长期维护、互操作与替代实现。份额低本身不能证明存在能力缺口；需补充采用情况、供给质量与维护者证据。</p><a href="#al-concentration">依据：全景、覆盖与集中度 →</a></article><article><span>02 / 实质贡献</span><h4>提升关键子领域的实质贡献</h4><p>把支持落实到上游维护、评测、文档与人才培养，并用贡献完成情况检验成效。真实国家贡献数据补齐后再判断地域差异；本版模拟国家图不支持国家优劣或治理主导权结论。</p><a href="#al-country-rank">依据：国家贡献与技术分布 →</a></article><article><span>03 / 持续观测</span><h4>用月度观测校准支持方向</h4><p>按月固定分类、样本与数据版本，记录项目进入退出、观测缺口和地域覆盖。趋势突变先核查数据、事件与样本，再调整支持方向，避免仅凭单月位次配置资源。</p><a href="#al-category-heat">依据：月度位次与共同样本变化 →</a></article></div></section>''')
    out.append(f'''<section class="al-section" id="land-evidence"><span class="eyebrow">METHODS & SOURCES</span><h3>来源与口径</h3><details><summary>样本、月份与缺失值如何处理</summary><p>固定主表中 keep / add 项目，按 repo_id 去重，得到 145 项目（Agent Infra 86、Model Infra 59），每个项目属于一个主要类别。12 个月为 2025-09—2026-08。主表提交：{L.REF}。分类为该版本的回溯分类，不推断历史分类或存活项目全貌。</p><p>子类别 OpenRank 是该月有值项目之和；份额分母是当前范围的全部有值项目之和。无观测与尚未创建均不当作零，覆盖率分母为当前固定样本。项目月度位次仅在有值项目中排序；子类别位次含覆盖变化，位次变化仅作描述。项目数值环比要求两月都有值且前月非零；类别环比只在两月共同有值项目中计算，同时报告共同样本数。</p></details><details><summary>国家贡献：本版模拟方法与真实数据接入规则</summary><p>本版使用固定随机种子 341 生成类别 × 国家 × 月份贡献，并建立 SIM 前缀的模拟开发者标识。同一开发者可跨类别出现，人数按当前范围与统计期的标识集合去重；不把类别人数直接相加。模拟贡献量与真实项目 OpenRank 独立，二者不可相加。本版不接入原有口径待核的国家 Top 3 表。</p><p>真实接入时：对每个项目及月份，将项目 OpenRank 按完整项目社区中开发者 Community OpenRank 比例分配到个人，再按有时间戳的公开所在地快照汇总国家。必须使用完整贡献者集合，不能以 Top 12 替代分母。机器人单独识别并披露；国家未知者保留为未知，人数跨项目去重。公开所在地不等于国籍或雇主所在地。</p><p>地图复用报告已采用的世界边界；没有单列数据的地理单元不分配“其他”总值。其他与未知仅在榜单中显示，不作为虚构地图区域着色。地图为示意，具体数值以榜单为准。</p></details><details><summary>导出、复核与原始记录</summary><p>各图 CSV 导出当前范围、月份、指标、覆盖与真实／模拟标识；SVG 导出保留标题、来源和筛选条件。大表每页 8 行，打印展开所有记录；搜索只高亮全景，不改变统计分母。</p><p><a href="/assets/landscape/data/agentic-ai-projects.csv" download>固定版本原始 CSV ↓</a> · <a href="{L.source('canonical')}">上游数据 ↗</a> · <a href="/assets/landscape/v2-data.json" download>全部视图数据 JSON ↓</a> · <a href="/assets/landscape/v2-observations.csv" download>145 × 12 月观测 CSV ↓</a> · <a href="/assets/landscape/v2-simulation.csv" download>模拟国家贡献 CSV ↓</a> · <a href="/assets/landscape/provenance.json">源文件指纹</a></p></details></section></section>''')
    ch=json.loads((L.ROOT/'content/manifest.json').read_text())['chapters'][3]
    for s in ch['sections'][1:]:out.append(f'<section class="chapter-section al-pending" id="{s["id"]}"><h2>{E(s["number"]+" "+s["title"]["zh"])}</h2><p>{E(s["question"]["zh"])}</p>{L.link(L.REPORT+s["source_path"],"阅读仓库初稿 ↗")}</section>')
    out.append('<dialog id="al-project-dialog" aria-labelledby="al-dialog-title"><button type="button" class="al-close">关闭 ×</button><div id="al-project-detail"></div></dialog><dialog id="al-fullscreen" aria-label="图表全屏查看"><div class="al-fullscreen-bar"><strong>图表全屏</strong><button type="button" class="al-close">退出全屏 ×</button></div><div id="al-fullscreen-body"></div></dialog><script type="application/json" id="landscape-data">'+json.dumps(payload(),ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></div>')
    return ''.join(out)

def export(out):
    dest=out/'assets/landscape';d=payload()
    (dest/'v2-data.json').write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
    with (dest/'v2-observations.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['data_status','repo_id','repo_name','layer','category','month','openrank','observation_status','source_commit'])
        for p in L.PROJECTS:
            for i,m in enumerate(MONTHS):
                v=p['trend'][i];status='observed' if v is not None else ('not_created' if p['created'][:7]>m else 'missing')
                w.writerow(['REAL',p['id'],p['repo'],p['layer'],p['section'],m,v,status,L.REF])
    with (dest/'v2-simulation.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['data_status','seed','category','month','country','simulated_contribution','synthetic_actor_ids'])
        for r in d['simulation']:w.writerow(['SIMULATED',341,r['section'],MONTHS[r['month']],r['country'],r['value'],';'.join(r['actors'])])
