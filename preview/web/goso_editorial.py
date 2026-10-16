"""Editorial figure types for non-geographic questions; every width is source-backed."""
import html, json
import goso_content as g
E=lambda s:html.escape(str(s),quote=True)
INK='var(--gv-ink, #10334D)';MUTED='var(--gv-muted, #4C697B)'

def sankey_svg():
    import goso_atlas as atlas
    rows=atlas.payload()['flows'];names={r['id']:r['name'] for r in rows};totals={k:sum(r['value'] for r in rows if r['id']==k) for k in names};order=sorted(totals,key=totals.get,reverse=True)
    sums={k:sum(r['value'] for r in rows if r['target']==k) for k in ['CN','US']};scale=(425-(len(order)-1)*12)/sum(totals.values());y=53;left={};right={};leftoff={};rightoff={}
    for key in order:left[key]=y;leftoff[key]=0;y+=totals[key]*scale+12
    y=70
    for key in ['CN','US']:right[key]=y;rightoff[key]=0;y+=sums[key]*scale+70
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 550" role="group" aria-label="开发者贡献来源到中美项目的桑基图"><text x="32" y="25" font-size="12" fill="'+MUTED+'">开发者所在地 · 表列贡献来源</text><text x="674" y="25" font-size="12" fill="'+MUTED+'">项目归属地 · 前十来源合计</text>']
    for i,r in enumerate(rows):
        y1=left[r['id']]+leftoff[r['id']];y2=right[r['target']]+rightoff[r['target']];h=r['value']*scale;leftoff[r['id']]+=h;rightoff[r['target']]+=h;c='var(--gv-s0, #156993)' if r['target']=='CN' else 'var(--gv-s1, #279FA9)';target='中国项目' if r['target']=='CN' else '美国项目'
        label=f"{r['name']} → {target}：{r['value']:,.2f} OpenRank，占该项目样本贡献 {r['share']}%"
        d=f'M200 {y1}C420 {y1} 430 {y2} 655 {y2}L655 {y2+h}C430 {y2+h} 420 {y1+h} 200 {y1+h}Z'
        out.append(f'<path d="{d}" fill="{c}" fill-opacity=".35" data-ribbon="{i}" data-flow-target="{r["target"]}" data-description="{E(label)}" tabindex="0" role="button" aria-label="{E(label)}"><title>{E(label)}</title></path>')
    for key in order:
        y=left[key];h=totals[key]*scale
        out.append(f'<rect x="187" y="{y}" width="13" height="{h}" rx="1" fill="var(--gv-brand, #156993)"/><text x="176" y="{y+h/2+4}" text-anchor="end" fill="{INK}" font-size="11">{E(names[key])}</text>')
    for key in ['CN','US']:
        y=right[key];h=sums[key]*scale;c='var(--gv-s0, #156993)' if key=='CN' else 'var(--gv-s1, #279FA9)';name='中国项目' if key=='CN' else '美国项目'
        out.append(f'<rect x="655" y="{y}" width="16" height="{h}" rx="2" fill="{c}"/><text x="690" y="{y+h/2-8}" fill="{INK}" font-size="17">{name}</text><text x="690" y="{y+h/2+16}" fill="{c}" font-size="17">{sums[key]:,.2f}</text><text x="690" y="{y+h/2+35}" fill="{MUTED}" font-size="10">OpenRank · 表列前十来源</text>')
    out.append('<text x="32" y="534" fill="'+MUTED+'" font-size="10">带宽 = OpenRank 贡献度；两组均仅绘制原表前十来源，不补齐或重归一化。</text></svg>')
    return ''.join(out)

def flow_panel():
    return '''<figure class="editorial-figure flow-figure" id="goso-collaboration" data-flow-figure><div class="editorial-figure-head"><div><span class="eyebrow">FIGURE 2.6 / COLLABORATION</span><h3>谁在贡献，谁的项目吸引了贡献？</h3></div><span class="atlas-period">2026 报告年 · 项目样本</span></div><div class="flow-statements"><div><span>中国项目 · 本土贡献</span><strong>79.22<small>%</small></strong></div><div><span>美国项目 · 本土贡献</span><strong>38.28<small>%</small></strong></div><p>参与全球项目与吸引全球共建，<br>是需要分别观察的两种能力。</p></div><div class="flow-filter" role="group" aria-label="突出项目归属"><button type="button" data-flow-filter="all" aria-pressed="true">全部连接</button><button type="button" data-flow-filter="CN" aria-pressed="false">聚焦中国项目</button><button type="button" data-flow-filter="US" aria-pressed="false">聚焦美国项目</button></div><div class="editorial-svg">'''+sankey_svg()+'''</div><div class="editorial-readout" data-flow-readout aria-live="polite">悬停或点选一条连接，查看贡献度与原表份额。</div><figcaption><p>这幅图描述协作贡献流向，不是人员迁移。中国、美国项目前十来源分别覆盖原表贡献的 93.24%、77.94%，未列来源未绘入。初稿桑基图与贡献来源表的数值不同，本版采用可下载的仓库底表。</p><a href="'''+g.source('cross')+'''" target="_blank" rel="noopener">核对来源 ↗</a> · <a href="'''+g.dataurl('cross')+'''" download>原始 CSV ↓</a></figcaption></figure>'''

def stack_svg():
    rows=g.rows('share');keys=[k for k in rows[0] if k!='year'];colors=['var(--gv-s1, #279FA9)','var(--gv-s2, #4E87C5)','var(--gv-s0, #156993)','var(--gv-s3, #9973B7)','var(--gv-s5, #C08A2D)','var(--gv-empty, #E0EBF0)'];out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 390" role="group" aria-label="2022 至 2026 固定五国和其他国家贡献份额">']
    for i,row in enumerate(rows):
        y=62+i*54;x=70;out.append(f'<text x="48" y="{y+21}" text-anchor="end" fill="{INK}" font-size="13">{row["year"]}</text>')
        for j,k in enumerate(keys):
            value=float(row[k]);width=value/100*796;label=g.LABELS.get(k,k);desc=f'{row["year"]} · {label} · {value:.2f}%'
            out.append(f'<g data-stack-segment="" data-description="{E(desc)}" tabindex="0" role="button" aria-label="{E(desc)}"><rect x="{x}" y="{y}" width="{width}" height="33" fill="{colors[j]}" stroke="white" stroke-width=".6"/><title>{E(desc)}</title>')
            if k in ['United States','China','Other countries']:out.append(f'<text x="{x+width/2}" y="{y+21}" text-anchor="middle" fill="'+('var(--gv-muted, #4C697B)' if j==5 else INK)+f'" font-size="11">{value:.2f}%</text>')
            out.append('</g>');x+=width
    x=70
    for k,c in zip(keys,colors):
        label=g.LABELS.get(k,k);out.append(f'<rect x="{x}" y="18" width="9" height="9" fill="{c}"/><text x="{x+16}" y="27" font-size="11" fill="{INK}">{label}</text>');x+=128
    for value in [0,25,50,75,100]:out.append(f'<text x="{70+value/100*796}" y="351" font-size="10" text-anchor="middle" fill="{MUTED}">{value}%</text>')
    out.append('</svg>');return ''.join(out)

def stack_panel():
    return '''<figure class="editorial-figure" id="goso-composition"><div class="editorial-figure-head"><div><span class="eyebrow">FIGURE 2.6 / CONTRIBUTION MIX</span><h3>固定五国份额小幅下降，结构变化仍需持续观察。</h3></div><span class="atlas-period">2022—2026 报告年</span></div><div class="composition-summary"><strong>49.47% <span>→</span> 48.62%</strong><p>五国合计份额下降 0.85 个百分点。<br>“其他国家”的份额增加，不等于已经证明所有国家更加均衡。</p></div><div class="editorial-svg">'''+stack_svg()+'''</div><div class="editorial-readout" data-stack-readout aria-live="polite">悬停或点选色块，查看当年贡献份额。</div><figcaption><p>五国为美国、德国、中国、英国和印度，使用固定名单。与 2.2 的数据范围尚未对齐，不拼接计算全球总量。</p><a href="'''+g.source('share')+'''" target="_blank" rel="noopener">核对来源 ↗</a> · <a href="'''+g.dataurl('share')+'''" download>原始 CSV ↓</a></figcaption></figure>'''

def governance_panel():
    rr=g.rows('foundation');panels=[('active_repositories','基金会样本活跃仓库','个','var(--gv-s2, #4E87C5)'),('foundation_project_openrank_share_pct','基金会项目影响力份额','%','var(--gv-s1, #279FA9)')];out=['<figure class="editorial-figure" id="goso-governance"><div class="editorial-figure-head"><div><span class="eyebrow">FIGURE 2.7 / INSTITUTIONAL SUPPORT</span><h3>项目承载规模与影响力份额，分别观察。</h3></div><span class="atlas-period">2022—2026 报告年</span></div><div class="governance-small-multiples">']
    for key,title,unit,color in panels:
        vals=[float(r[key]) for r in rr];mx=max(vals)*1.08;parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 280" role="group" aria-label="'+title+'">'];parts.append('<text x="30" y="28" fill="'+INK+'" font-size="14">'+title+'</text>')
        for tick in [0,.5,1]:
            y=216-tick*155;parts.append(f'<path d="M48 {y}H420" stroke="var(--gv-line, #CADCE5)"/><text x="40" y="{y+4}" text-anchor="end" fill="{MUTED}" font-size="10">{round(mx*tick,2):g}</text>')
        for i,(r,v) in enumerate(zip(rr,vals)):
            x=62+i*72;h=v/mx*155;y=216-h;desc=f'{r["year"]} · {title} · {v:g} {unit}'
            parts.append(f'<g data-stack-segment="" data-description="{E(desc)}" tabindex="0" role="button" aria-label="{E(desc)}"><rect x="{x}" y="{y}" width="43" height="{h}" rx="2" fill="{color}"/><title>{E(desc)}</title><text x="{x+21}" y="{y-9}" fill="{color}" font-size="12" text-anchor="middle">{v:g}</text><text x="{x+21}" y="240" text-anchor="middle" fill="{MUTED}" font-size="11">{r["year"]}</text></g>')
        parts.append('<text x="30" y="266" fill="'+MUTED+'" font-size="10">单位：'+unit+' · 纵轴从零开始</text></svg>');out.append('<div>'+''.join(parts)+'</div>')
    out.append('</div><div class="editorial-readout" data-stack-readout aria-live="polite">数量增长约 5.9%，份额提高 0.30 个百分点；两者不直接证明治理效率提升。</div><figcaption><a href="'+g.source('foundation')+'" target="_blank" rel="noopener">核对来源 ↗</a><p>继续通过许可证、维护机制与公共场景检验持续开放的条件。公共价值案例待补充。</p></figcaption></figure>');return ''.join(out)

def stage(kind,primary,comparison):
    choices=[('primary',{'v':'空间分布','c':'空间分布','i':'项目地图','t':'城市分布','d':'贡献流向','g':'治理观察','a':'模型地图'}[kind]),('comparison',{'v':'五域趋势','c':'贡献比较','i':'五域趋势','t':'城市比较','d':'数据比较','g':'许可证与趋势','a':'代码与模型趋势'}[kind])]
    if kind=='d':choices.insert(1,('composition','贡献结构'))
    buttons=''.join(f'<button type="button" id="stage-{kind}-{key}-tab" role="tab" aria-controls="stage-{kind}-{key}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" data-stage-tab="{key}">{label}</button>' for i,(key,label) in enumerate(choices))
    panels=[]
    for key,label in choices:
        body=primary if key=='primary' else stack_panel() if key=='composition' else comparison
        panels.append(f'<div id="stage-{kind}-{key}" role="tabpanel" aria-labelledby="stage-{kind}-{key}-tab" data-stage-panel="{key}">{body}</div>')
    return f'<div class="chapter-evidence" data-stage="{kind}"><div class="stage-tabs" role="tablist" aria-label="本节观察方式" hidden>{buttons}</div>'+''.join(panels)+'</div>'

def cover():
    return '''<section class="goso-cover" id="goso-intro"><div><span class="eyebrow">GOSO / OBSERVATORY 2026</span><h2>开源的全球格局，<br><em>与正在发生的结构变化。</em></h2><p>用地图看分布，用时间序列看变化，用协作关系看连接。<br>从参与规模，走向贡献质量与公共价值。</p></div><aside aria-label="本章年度观察"><a href="#ch02-s01"><span>活跃参与 / 中国实例</span><strong>234.46<small>万</small></strong><p>GitHub 基线 · 2025自然年</p></a><a href="#ch02-s02"><span>协作贡献 / 中国实例</span><strong>442.92<small>万</small></strong><p>报告 OpenRank · 2026</p></a><a href="#ch02-s03"><span>项目影响 / 中国</span><strong>约 160<small>%</small></strong><p>2022—2026 累计增长</p></a></aside></section>'''
