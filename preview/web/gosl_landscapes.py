"""Chapter 4 shared framework and first evidence-backed landscape for 4.2–4.6."""
from pathlib import Path
import csv, html, json, math, shutil
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/gosl/landscapes.json').read_text())
DATASETS=DATA['datasets']
VERSION=DATA['version']
REPO='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report'
W,H=1600,1100
TOP,BOTTOM=106,906
E=lambda s:html.escape(str(s),quote=True)
def text(x,y,s,size=16,attrs=''):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" {attrs}>{E(s)}</text>'
def names(d):return {c['id']:c for c in d['categories']}
def weighted_length(s):return sum(1 if ord(c)>255 else .82 if c in 'MW@#%' else .29 if c in 'il.:|!\'' else .54 for c in s)
def wrap(s,width,size=14,limit=None):
    lines=[];line=''
    for char in s:
        if line and weighted_length(line+char)*size>width:
            lines.append(line);line=''
        line+=char
    if line:lines.append(line)
    return lines

def geometry(d):
    """Columns encode functional families; within each, every category remains visible."""
    cats=names(d);groups=d['groups'];gap=18;x=24;usable=W-48-gap*(len(groups)-1)
    weights=[math.sqrt(sum(cats[k]['count'] for k in g['categories'])+len(g['categories'])*2+2) for g in groups]
    if d['id']=='models':weights=[1]*3
    if d['id']=='cloud':weights=[1]*4
    blocks=[];group_boxes=[]
    for gi,(g,weight) in enumerate(zip(groups,weights)):
        width=usable*weight/sum(weights)
        cols=3 if width>=610 and d['id']!='models' else 2
        base=[]
        for key in g['categories']:
            c=cats[key];items=[p for p in d['projects'] if p['category']==key]
            rowheight=38 if d['id']=='models' else 28
            cw=(width-20)/cols
            for p in items:
                if len(wrap(p['name'],cw-34,11.5))>2:rowheight=max(rowheight,45)
            height=32 if not items else 35+math.ceil(len(items)/cols)*rowheight+8
            base.append((key,items,height,rowheight))
        available=BOTTOM-TOP-(len(base)-1)*7
        needed=sum(b[2] for b in base)
        # Non-overlapping project tiles keep a readable base height; the gate catches capacity regressions.
        assert needed<=available, (d['id'],g['id'],needed,available)
        extra=(available-needed)/max(1,sum(bool(b[1]) for b in base))
        y=TOP
        for key,items,height,rowheight in base:
            hh=height+(extra if items else 0)
            cellspace=(hh-45)/max(1,math.ceil(len(items)/cols)) if items else rowheight
            cells=[]
            for pi,p in enumerate(items):
                px=x+10+(pi%cols)*cw;py=y+35+(pi//cols)*cellspace
                cells.append({'project':p,'x':px,'y':py,'w':cw-5,'h':cellspace})
            blocks.append({'id':key,'group':g['id'],'x':x,'y':y,'w':width,'h':hh,'cells':cells})
            y+=hh+7
        group_boxes.append({'group':g,'x':x,'w':width})
        x+=width+gap
    return blocks,group_boxes

def project_svg(p,x,y,w,h,d):
    available=w-34;size=14
    while len(wrap(p['name'],available,size))>2 and size>11.5:size-=.5
    lines=wrap(p['name'],available,size)
    assert len(lines)<=3,(d['id'],p['name'],available)
    lh=size+1;start=y+h/2-(len(lines)-1)*lh/2+size*.35
    body=f'<rect class="gl-project-box" x="{x}" y="{y+1}" width="{w}" height="{h-2}" rx="3" fill="var(--gv-surface)" stroke="transparent"/>'
    mark=str(p.get('rank','')) if d['id']=='models' else p['name'][:1].upper()
    body+=f'<rect x="{x+2}" y="{y+h/2-10}" width="23" height="20" rx="3" fill="var(--gv-raised)"/>'+text(x+13.5,y+h/2+4,mark,11,'text-anchor="middle" fill="var(--gl-accent)" font-weight="650"')
    body+=f'<text x="{x+32}" y="{start}" font-size="{size}" fill="var(--gv-ink)">'+''.join(f'<tspan x="{x+32}" dy="{0 if i==0 else lh}">{E(s)}</tspan>' for i,s in enumerate(lines))+'</text>'
    return f'<g class="gl-project" role="button" tabindex="0" data-gl-project="{E(p["id"])}" data-gl-category-key="{E(p["category"])}" aria-label="{E(p["repo"])}，查看详情" aria-pressed="false"><title>{E(p["repo"])}</title>{body}</g>'

def plate_svg(d):
    boxes,groups=geometry(d);cats=names(d)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" class="gl-svg" viewBox="0 0 {W} {H}" role="group" aria-label="{E(d["short"])}技术全景"><rect width="{W}" height="{H}" fill="var(--gv-surface)"/>',text(24,36,d['en'],25,'font-weight="700" fill="var(--gl-accent)"'),text(W-24,34,f'{d["count"]} 条入库记录 / {d["categoryCount"]} 个技术类别',16,'text-anchor="end" fill="var(--gv-muted)"')]
    out.append('<defs><clipPath id="gl-clip-'+d['id']+'"><rect x="16" y="57" width="1568" height="856"/></clipPath></defs><g clip-path="url(#gl-clip-'+d['id']+')"><g class="gl-board">')
    for g in groups:
        x,w=g['x'],g['w'];out.append(f'<path d="M{x} 94H{x+w}" stroke="var(--gl-accent)" stroke-width="2"/>'+text(x,74,g['group']['name'],19,'font-weight="700"')+text(x+w,74,g['group']['subtitle'],12,'text-anchor="end" fill="var(--gv-muted)"'))
    for b in boxes:
        c=cats[b['id']];x,y,w,h=b['x'],b['y'],b['w'],b['h'];empty=not b['cells']
        out.append(f'<g class="gl-category" data-gl-category="{E(c["id"])}" data-gl-group="{E(b["group"])}" data-box="{x} {y} {w} {h}"><rect class="gl-category-box" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="var(--gv-surface)" stroke="var(--gv-line)"/><g class="gl-category-title" role="button" tabindex="0" data-gl-select-category="{E(c["id"])}" aria-label="{E(c["name"])}，{c["count"]} 条样本" aria-pressed="false"><rect x="{x+1}" y="{y+1}" width="{w-2}" height="30" rx="3" fill="var(--gv-raised)"/>'+text(x+10,y+21,c['name'],14,'font-weight="650"')+text(x+w-10,y+21,'本样本未覆盖' if empty else str(c['count'])+' 项',11,'text-anchor="end" fill="var(--gv-muted)"')+'</g>')
        for cell in b['cells']:out.append(project_svg(cell['project'],cell['x'],cell['y'],cell['w'],cell['h'],d))
        out.append('</g>')
    out.append('</g></g><g class="gl-inspector">'+inspector_default(d)+'</g>'+text(24,1082,'分区表示功能关系；面积与位置不表示市场份额或依赖强度。无样本不等于该技术不存在。',12,'fill="var(--gv-muted)"')+'</svg>')
    return ''.join(out)

def inspector_default(d):
    return f'<rect x="24" y="926" width="1552" height="132" rx="5" fill="var(--gv-raised)" stroke="var(--gv-line)"/>'+text(42,955,'从全景开始，按需探索',23,'font-weight="650"')+text(42,983,'点击技术类别或项目，详情留在本图；搜索定位后可放大模块。',16,'fill="var(--gv-muted)"')+text(42,1013,d['period'],14,'fill="var(--gv-muted)"')+text(1230,968,str(d['count']),32,'fill="var(--gl-accent)" font-weight="650"')+text(1230,995,'条入库记录',14,'fill="var(--gv-muted)"')+text(1435,968,str(d['categoryCount']),32,'fill="var(--gl-accent)" font-weight="650"')+text(1435,995,'个技术类别',14,'fill="var(--gv-muted)"')

def contribution_url(d):
    body=f'## {d["number"]} {d["title"]}\n\n补充类型：分类修订 / 项目补全 / 数据与口径 / 核心发现 / 应用案例 / 行动建议\n\n### 建议补充的内容\n\n\n### 一手来源与日期\n\n\n### 样本、统计窗口与适用边界\n\n\n### 希望署名的信息（可选）\n'
    return REPO+'/issues/new?'+urlencode({'title':f'[{d["number"]} 共建] ', 'body':body})

def chapter_overview():
    cards=[('4.1','Agentic AI','任务入口 → 编排 → 执行','145 项目 · 25 类','深入样章','#ch04-s01')]+[(d['number'],d['short'],d['groups'][0]['name']+' → '+d['groups'][-1]['name'],f'{d["count"]} 条记录 · {d["categoryCount"]} 类','全景与框架','#ch04-s0'+d['number'][-1]) for d in DATASETS]
    return '''<section id="gosl-overview" class="gl-overview"><div class="gl-overview-top"><span class="eyebrow">CHAPTER 04 / OPEN SOURCE LANDSCAPES</span><span>全景与共建评审版 · 2026.10</span></div><h2>六个领域，读懂开源技术结构</h2><p>从一个项目走向完整技术分工。本章以 4.1 作为深入样章，其余五节先开放技术全景与研究框架，邀请熟悉各领域的研究者、维护者和使用者共同补充。</p><nav class="gl-directory" aria-label="第四章六个领域">'''+''.join(f'<a href="{href}"><div><span>{num}</span><small>{status}</small></div><h3>{title}</h3><p>{route}</p><footer>{counts}<b>查看全景 ↗</b></footer></a>' for num,title,route,counts,status,href in cards)+'''</nav><div class="gl-overview-foot"><p>本轮开放：技术分类、项目定位与来源记录。后续补充：核心发现、演变趋势、贡献结构与行动建议。</p><a href="#gosl-contribute">参与本章共建 ↗</a></div></section>'''

def framework_section(d):
    sid='ch04-s0'+d['number'][-1];pid='gl-'+d['id'];pending=sum(p['category']=='pending' for p in d['projects'])
    controls='<div class="gl-groups" role="group" aria-label="功能分区"><button data-gl-focus="all" aria-pressed="true">全部结构</button>'+''.join(f'<button data-gl-focus="{E(g["id"])}" aria-pressed="false">{E(g["name"])}</button>' for g in d['groups'])+'</div>'
    controls+='<div class="gl-control-row"><label>快速定位<input type="search" data-gl-search placeholder="搜索项目、发布者或技术类别"></label><button data-gl-reset>恢复全景</button><button data-gl-zoom disabled>放大模块</button><a data-gl-project-link href="'+d['source']['url']+'" target="_blank" rel="noopener">查看数据来源 ↗</a></div>'
    sourceText='原表任务分类与排序' if d['id']=='models' else 'OpenDigger 技术标签；主展示类别与完整标签分别保留' if d['id'] in ['cloud','database'] else '报告原有类别 + 项目一手说明；功能归类供共建复核'
    empty=''.join(f'<article><span>{i+2:02d} / 待补充</span><h4>{name}</h4><div class="gl-writing-space" aria-label="{name}内容待补充"></div><p>{hint}</p></article>' for i,(name,hint) in enumerate([('核心发现','预留研究判断及对应证据。'),('排行与演变','预留项目、子类别及时间变化。'),('贡献与协作','预留参与主体、贡献结构和案例。'),('行动建议','预留面向维护者、采用方与支持方的建议。')]))
    return f'''<section class="chapter-section gl-section" id="{sid}" data-gosl-section="{d['id']}"><header class="gl-section-header"><div class="gl-section-top"><span>{d['number']} / {d['en']}</span><span>全景已上线 · 正文待共建</span></div><h2>{d['title']}</h2><p class="gl-question">{d['question']}</p><p>{d['intro']}</p><dl class="gl-section-spec"><div><dt>观察对象</dt><dd>{d['count']} 条入库记录 · {d['categoryCount']} 个技术类别{f' · {pending} 条分类待核' if pending else ''}</dd></div><div><dt>指标定位</dt><dd>{d['metric']} · 本轮仅作为图内原始记录查看</dd></div><div><dt>研究路径</dt><dd>技术结构 → 项目与类别演变 → 贡献与协作 → 行动建议</dd></div></dl></header><article id="{pid}" class="gl-plate" data-gl-plate="{d['id']}" data-accent="{d['accent']}"><header class="gl-plate-heading"><div><span class="eyebrow">{d['number']}-01 / THE LANDSCAPE</span><h3>{d['short']} · 技术结构全景</h3></div><div class="gl-tools"><button data-gl-full>全屏</button><button data-gl-svg>SVG ↓</button><button data-gl-csv>清单 CSV ↓</button></div></header><p class="gl-scope">{d['scope']}</p><div class="gl-controls">{controls}</div><div class="gl-canvas">{plate_svg(d)}</div><p class="gl-readout" aria-live="polite">点击分区或项目在图内查看详情；所有分类始终保留。</p><details class="gl-data"><summary>查看完整项目清单与分类来源</summary><div class="gl-table-host"></div><noscript><p><a href="/assets/gosl/{d['id']}-projects.csv" download>下载完整清单 CSV ↓</a></p></noscript></details><p class="gl-source">来源：<a href="{d['source']['url']}">报告原始清单</a> · {sourceText}。<a href="/assets/gosl/{d['id']}-projects.csv" download>完整分类记录 ↓</a> · <a href="#gosl-methods">分类与口径说明 ↗</a></p></article><section class="gl-outline" aria-label="{d['number']}待共建内容"><div class="gl-outline-title"><h3>本节研究框架</h3><a href="{E(contribution_url(d))}" target="_blank" rel="noopener">补充本节材料 ↗</a></div><div class="gl-outline-grid">{empty}</div><p class="gl-needed">欢迎补充：{d['need']}</p></section></section>'''

def section_fragments():
    return ''.join(framework_section(d) for d in DATASETS)+f'''<section id="gosl-contribute" class="gl-contribute"><span class="eyebrow">BUILD THIS LANDSCAPE TOGETHER</span><h2>从一张全景开始，共同补全技术生态</h2><p>欢迎纠正分类、补充项目、提供一手数据与实践案例。可以从熟悉的一节开始，说明来源、日期和适用范围；研究判断与行动建议在证据齐备后逐步填写。</p><div class="gl-contribute-links"><a href="{REPO}/issues/new">提交材料与建议 ↗</a><a href="/assets/gosl/contribution-template.md" download>下载共建模板 ↓</a><a href="{REPO}/blob/main/preview/content/gosl/landscapes.json">查看可维护的分类清单 ↗</a></div></section><section id="gosl-methods" class="gl-methods"><h3>全景样本与分类口径</h3><details><summary>分类表示什么，哪些内容仍待补充？</summary><p>4.2—4.6 的项目和数值来自报告已有 CSV；本次未重新抓取排名，也未生成趋势或国家贡献结论。云与数据库使用固定版本的 OpenDigger 标签，以仓库 ID 和标签引用关系匹配。一个仓库可能具有多个标签；全景只放置一次，其余标签在图内详情和下载中保留，因此本图类别数量不能直接复算原稿多标签的年度分类汇总。</p><p>RISC-V 与 PyTorch 使用报告既有类别，结合项目自身说明作功能归类；这是供评审的编辑分类，不冒充原年度统计的项目映射。缺少证据或与技术主题不符的样本单列“分类与样本待核”。PyTorch 周边仓库不自动代表基金会正式托管项目。面积与位置用于组织阅读，功能相邻不证明真实依赖或兼容。</p></details><details><summary>数据时点、开放资格与下载</summary><p>模型图为 2026-10-02 快照，六任务领域各取近 30 天下载量 Top 16；下载量不是用户数、能力评分或 ModelRank。公开模型样本不自动满足开源资格。其余四图仅保留原表的项目 OpenRank 值和 2026 年标记，具体起止窗口仍待核验，不扩写同比结论。原始数据不补零、不跨图合并，分类未覆盖不表示技术不存在。</p><p><a href="/assets/gosl/landscapes.json" download>下载全部全景记录 JSON ↓</a> · <a href="/assets/gosl/provenance.json">来源指纹与分类版本 ↗</a> · <a href="https://github.com/X-lab2017/open-digger/tree/{DATA['classificationRef']}/labeled_data/technology">OpenDigger 分类版本 ↗</a></p></details></section><dialog id="gl-fullscreen" aria-label="技术全景全屏查看"><div class="gl-fullscreen-bar"><strong>技术全景</strong><div><button data-gl-theme>切换深色</button><button data-gl-close>退出全屏 ×</button></div></div><div id="gl-fullscreen-body"></div></dialog><script type="application/json" id="gosl-data">'''+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'

def english_framework():
    return '<div id="gosl-overview" class="reader-note">Chapter 4 has one in-depth Agentic AI section and five Chinese interactive landscape frameworks. Analysis in sections 4.2–4.6 remains open for contributions.</div>'+''.join(f'<section id="ch04-s0{i}" class="chapter-section"><h2>{number} {title}</h2><p>{status}</p><a href="/2026/zh/chapters/04/#ch04-s0{i}">Explore the Chinese landscape →</a></section>' for i,number,title,status in [(1,'4.1','Agentic AI','In-depth sample with landscapes, evolution and contributions.')]+[(int(d['number'][-1]),d['number'],d['en'].title(),'Landscape and research framework available; findings and further analysis are pending.') for d in DATASETS])

def export(out):
    dest=out/'assets/gosl';dest.mkdir(parents=True,exist_ok=True)
    (dest/'landscapes.json').write_text(json.dumps(DATA,ensure_ascii=False,separators=(',',':')))
    provenance={'version':VERSION,'source_policy':'Existing report observations unchanged; display classifications recorded separately.','classification_ref':DATA['classificationRef'],'datasets':[{'id':d['id'],'count':d['count'],'source':d['source']} for d in DATASETS]}
    (dest/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
    for d in DATASETS:
        cats=names(d)
        with (dest/(d['id']+'-projects.csv')).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f);w.writerow(['section','repo_or_model','display_category','all_labels','value','metric','period','classification_status','classification_source','notes'])
            for p in d['projects']:w.writerow([d['number'],p['repo'],cats[p['category']]['name'],' / '.join(cats[k]['name'] for k in p['tags']),p['value'],d['metric'],d['period'],p['classification'],p['classificationSource'],p['note']])
    shutil.copy2(ROOT/'docs/chapter4-contribution-template.md',dest/'contribution-template.md')
