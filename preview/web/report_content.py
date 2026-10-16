"""Source-backed reading and evidence views for the GOSD Preview."""
from pathlib import Path,PurePosixPath
from urllib.parse import quote,urlsplit,unquote
import html,json,re,posixpath
import chapter_visuals
import chapter1_tables

ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'content/report.json').read_text())
E=lambda s:html.escape(str(s),quote=True)
T=lambda lang,z,e:z if lang=='zh' else e
REPO='https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/'
CH1='chapters/chapter1/'
INTRO=CH1+'本章介绍.md'
METHOD='appendices/附录A-指标体系与数据来源.md'
PARTS=[CH1+x for x in ['1.1-开源-数字公共品与可持续发展引擎.md','1.2-OSDGs-开源发展目标框架.md','1.3-OSDI-开源发展度量体系.md']]
IND={r['indicator_code']:r for r in R['indicators']}
DS={r['path']:r for r in R['datasets']}
def path(lang,route):return '/2026/'+lang+'/'+route
def a(url,label,cls='inline-link',extra=''):return f'<a href="{E(url)}" class="{cls}" {extra}>{label}</a>'
def p(s,cls=''):return f'<p class="{cls}">{E(s)}</p>'
def source(name):
    ref=R['source_ref'] if name in R['repository_paths'] else 'docs/osdg-report-publication-plan-20261011'
    return REPO+ref+'/'+quote(name,safe='/')
def anchor(title,prefix):
    title=re.sub(r'[*`\[\]]','',title)
    return prefix+'-'+re.sub(r'[^\w\u3400-\u9fff-]+','-',title).strip('-').lower()
def mapped_url(href,src,lang):
    u=urlsplit(href)
    if u.scheme or u.netloc:return href if u.scheme in ['http','https','mailto'] else '#'
    name=posixpath.normpath(posixpath.join(posixpath.dirname(src),unquote(u.path)))
    if name==INTRO:return path(lang,'chapters/01/')+'#chapter-intro'
    if name in PARTS:return path(lang,'chapters/01/')+'#ch01-s0'+str(PARTS.index(name)+1)
    if name==METHOD:return path(lang,'methodology/')
    if name=='data/meta/数据可用性清单.md':return path(lang,'data/sources/')
    if name=='data/meta/osdi_indicator_dictionary.csv':return path(lang,'data/indicators/')
    if name in DS:return path(lang,'data/sources/')+'#dataset-'+DS[name]['dataset_id']
    if name.startswith('figures/chapter1/') and (ROOT/'content/report-assets'/Path(name).name).exists():return '/assets/report/'+Path(name).name
    if name.startswith('data/meta/') and (ROOT/'content/report-assets'/Path(name).name).exists():return '/assets/report/'+Path(name).name
    return source(name)+(('#'+u.fragment) if u.fragment else '')
def inline(text,src,lang):
    tokens=[]
    def keep(value):tokens.append(value);return '\x00'+str(len(tokens)-1)+'\x00'
    text=re.sub(r'`([^`]+)`',lambda m:keep(a(path(lang,'data/indicators/')+'#indicator-'+m[1],'<code>'+E(m[1])+'</code>') if m[1] in IND else '<code>'+E(m[1])+'</code>'),text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:keep(a(mapped_url(m[2],src,lang),E(m[1]))),text)
    text=E(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',text)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],text)
def headings(src,prefix):
    return [(anchor(m[2],prefix),m[2],len(m[1])) for m in re.finditer(r'^(#{2,4}) (.+)$',R['documents'][src],re.M)]
def render(src,lang,prefix,skip_title=True):
    text=R['documents'][src]
    if src==PARTS[2]:
        text=re.sub(r'\*\*图 1-3-1：OSDI 指标地图。\*\*[^\n]*', '', text)
        text=re.sub(r'\*\*表 1.3.1：OSDI 的三级结构。\*\*[^\n]*', '', text)
    lines=text.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('# '):
            if not skip_title:out.append('<h2>'+inline(line[2:],src,lang)+'</h2>')
            i+=1;continue
        h=re.match(r'^(#{2,6}) (.+)',line)
        if h:
            level=min(len(h[1])+1,6);hid=anchor(h[2],prefix)
            out.append(f'<h{level} id="{hid}">{inline(h[2],src,lang)} <a class="heading-anchor" href="#{hid}" aria-label="{T(lang,"链接至此处","Link to this heading")}">#</a></h{level}>');i+=1;continue
        img=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if img:
            kind=chapter_visuals.FIGURES.get(Path(img[2]).name)
            if kind:
                out.append(chapter_visuals.render(kind,lang,R,source));i+=1;continue
            url=mapped_url(img[2],src,lang)
            out.append(f'<figure class="report-figure"><a href="{E(url)}" data-figure="true" aria-label="{E(T(lang,"放大图表：","Enlarge figure: ")+img[1])}"><img src="{E(url)}" alt="{E(img[1])}" loading="lazy"></a><figcaption>'+T(lang,'点击放大 · ','Enlarge · ')+a(url,T(lang,'下载 SVG ↓','Download SVG ↓'),'','download')+'</figcaption></figure>');i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[s.strip() for s in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',s) for s in cells):rows.append(cells)
                i+=1
            if src==PARTS[2] and rows[0][0]=='层级':continue
            if src.startswith(CH1):
                fid=prefix+'-table-'+str(i)
                out.append(chapter1_tables.render(rows,lang,fid,lambda c:inline(c,src,lang),source(src)))
                continue
            folded=src==PARTS[2] and rows[0][0]=='支柱／维度'
            if folded:out.append('<details class="osdi-reference-table"><summary>'+T(lang,'完整指标清单（29项，查证用）','Full indicator table (29 measures)')+'</summary>')
            out.append('<div class="reader-table-wrap" role="region" tabindex="0" aria-label="'+T(lang,'报告数据表，可横向滚动','Report table, horizontally scrollable')+'"><table class="reader-table"><thead><tr>'+''.join('<th scope="col">'+inline(c,src,lang)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c,src,lang)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>')
            if folded:out.append('</details>')
            continue
        if line.startswith('$$'):
            # The one canonical Activity equation, rendered without an external runtime.
            assert 'A_{u,r,m}' in line and 'sqrt' in line
            out.append('<div class="math-equation" role="math" aria-label="Activity equals the square root of weighted event counts; repository activity sums contributor activity.">A<sub>u,r,m</sub> = √(Σ<sub>i</sub> w<sub>i</sub> c<sub>i,u,r,m</sub>)<span>；</span>A<sub>r,m</sub> = Σ<sub>u</sub> A<sub>u,r,m</sub></div>');i+=1;continue
        if line.startswith('> '):out.append('<blockquote>'+inline(line[2:],src,lang)+'</blockquote>');i+=1;continue
        li=re.match(r'^(- |\d+\. )(.+)',line)
        if li:
            ordered=li[1]!='- ';tag='ol' if ordered else 'ul';out.append('<'+tag+'>')
            while i<len(lines):
                item=re.match(r'^'+(r'\d+\. ' if ordered else '- ')+r'(.+)',lines[i].strip())
                if not item:break
                out.append('<li>'+inline(item[1],src,lang)+'</li>');i+=1
            out.append('</'+tag+'>');continue
        para=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||>|- |\d+\. |!\[|\$\$)',lines[i].strip()):para.append(lines[i].strip());i+=1
        out.append('<p>'+inline(' '.join(para),src,lang)+'</p>')
    return '<div class="manuscript" lang="zh-CN">'+''.join(out)+'</div>'
def translation_note(lang):
    return '' if lang=='zh' else '<div class="reader-note">The reviewed Chinese manuscript is shown below. The English translation is in preparation; interface labels and navigation remain available in English.</div>'
def source_bar(src,lang):
    return '<div class="source-bar"><span>'+T(lang,'正文与事实源：GitHub','Manuscript source: GitHub')+'</span>'+a(source(src),T(lang,'查看本页原稿 ↗','View source manuscript ↗'))+a(path(lang,'data/sources/'),T(lang,'查数据与来源 →','Data and sources →'))+'</div>'
def chapter(lang):
    import reading_experience,sys
    return reading_experience.chapter(lang,sys.modules[__name__])

def methods(lang):
    return '<div class="reader-note">'+T(lang,'数据进展：数据目录按已入库文件更新；下文附录保留历史方法记录。新增模型数据采用各表标注的月度或快照窗口，不统一归入代码报告年度。','Data update: the base catalogue contains 50 processed CSVs; section 4.1 lists its supplementary evidence separately. The source appendix below retains its earlier 34-file inventory and method record. New model data retain their stated monthly or snapshot windows.')+'</div>'+translation_note(lang)+source_bar(METHOD,lang)+'<details class="local-toc" open><summary>'+T(lang,'方法目录','Methods contents')+'</summary><nav>'+''.join(a('#'+hid,E(label),'') for hid,label,level in headings(METHOD,'method') if level==2)+'</nav></details>'+render(METHOD,lang,'method')
def feature(lang):
    return '<section class="chapter-feature"><div><span class="eyebrow">NEW / CHAPTER 01</span><h2>'+T(lang,'先读第一章，建立共同的研究坐标。','Start with Chapter 1.<br>A shared basis for the research.')+'</h2>'+p(T(lang,'从 Linux 的全球协作到开放模型的复用，理解 AI 时代的开源变化；沿着价值、目标与指标，进入整份报告。','From Linux collaboration to open model reuse, explore changes in open source and the report’s values, goals and measures.'))+a(path(lang,'chapters/01/'),T(lang,'阅读第一章 →','Read Chapter 1 →'),'text-link')+'</div><div class="feature-route">'+''.join(a(path(lang,'chapters/01/')+'#ch01-s0'+str(i+1),'<small>1.'+str(i+1)+'</small><strong>'+T(lang,z,e)+'</strong><span>↗</span>','') for i,(z,e) in enumerate([('开源的公共价值','Public value'),('OSDGs 目标框架','OSDGs goals'),('OSDI 指标体系','OSDI measures')]))+'</div></section>'
def evidence_summary(lang):
    count=sum(bool(x['related_data_paths']) for x in R['indicators'])
    return '<div class="evidence-stats">'+''.join('<div><b>'+str(n)+'</b><span>'+T(lang,z,e)+'</span></div>' for n,z,e in [(29,'指标工作定义','Working definitions'),(len(R['datasets']),'已入库 CSV','Repository CSVs'),(count,'指标有关联资料','Indicators with related files')])+'</div>'+p(T(lang,'文件入库、指标测算和结论复核是不同状态。外部故事快照单独引用，不计入 OSDI。','File availability, completed measurements and reviewed findings are distinct states. External story snapshots are cited separately and excluded from OSDI.'),'small-note')
def indicators(lang,search,framework,english):
    t=lambda z,e:T(lang,z,e)
    out=[p(t('从定义进入方法，再查关联数据。展开任一指标，查看适用对象、计算口径、缺失处理与后续核验条件。','Start with a definition, follow the method and inspect related data. Expand a measure to see its scope, calculation, missing-data rules and evidence gaps.')),evidence_summary(lang),translation_note(lang)]
    opts='<option value="">'+t('全部支柱','All pillars')+'</option>'+''.join(f'<option value="{i+1}">{E(x[1 if lang=="zh" else 2])}</option>' for i,x in enumerate(framework['P']))
    out.append('<form class="filter-bar" id="indicator-filters" role="search"><label>'+t('查找指标','Find an indicator')+'<input type="search" name="q" id="indicator-q" placeholder="OpenRank / SDG / GOSR"></label><label>'+t('发展支柱','Pillar')+'<select name="pillar" id="indicator-pillar">'+opts+'</select></label><button type="reset">'+t('重置筛选','Reset filters')+'</button></form><p class="result-count" id="indicator-count" aria-live="polite"></p><div id="indicator-list">')
    for i,r in enumerate(R['indicators']):
        code=r['indicator_code'];title=r['indicator_name_zh'] if lang=='zh' else english[i];available=bool(r['related_data_paths'])
        out.append(f'<details class="indicator-entry" id="indicator-{code}" data-pillar="{r["pillar_id"][1:]}" data-search="{E((" ".join(r.values())+" "+english[i]+" SDG "+r["sdg_links"]).lower())}"><summary><span class="indicator-code">{code}</span><strong>{E(title)}</strong><span class="data-badge">'+t('有关联资料' if available else '待补数据','Related files' if available else 'Data pending')+'</span></summary><div class="indicator-detail"><p>'+a(path(lang,'data/goals/')+'#dimension-'+r['dimension_id'].replace('.','-'),r['dimension_id']+' '+E(r['dimension_name_zh'] if lang=='zh' else r['dimension_name_en']))+' · SDG '+E(r['sdg_links'])+' · '+E(r['role'])+'</p><dl class="definition-grid" lang="zh-CN">')
        for key,label in [('definition','定义'),('subjects','适用对象'),('calculation_rule','计算口径'),('unit','单位'),('period_rule','统计期'),('missing_rule','缺失处理'),('method_status','方法状态'),('data_status','数据状态'),('remaining_evidence','复核待办')]:out.append('<dt>'+label+'</dt><dd>'+E(r[key])+'</dd>')
        out.append('</dl>')
        data=[x for x in r['related_data_paths'].split(';') if x]
        if data:out.append('<details class="related-data"><summary>'+t('关联数据','Related data')+f' · {len(data)}</summary><ul>'+''.join('<li>'+a(path(lang,'data/sources/')+'#dataset-'+DS[x]['dataset_id'],E(Path(x).name))+'</li>' for x in data)+'</ul></details>')
        out.append('<div class="section-actions">'+a(path(lang,'methodology/'),t('查阅方法 →','Read methods →'))+a(path(lang,'chapters/01/')+'#ch01-s03',t('回到 1.3 →','Return to 1.3 →'))+'</div></div></details>')
        search.append({'lang':lang,'title':title+' · '+code,'description':r['dimension_name_zh']+' · '+r['definition'],'url':path(lang,'data/indicators/')+'#indicator-'+code,'category':'OSDI'})
    out.append('</div><p id="indicator-empty" hidden>'+t('没有匹配的指标，请调整筛选条件。','No matching indicators. Adjust the filters.')+'</p><div class="section-actions">'+a('/assets/report/osdi_indicator_dictionary.csv',t('下载完整指标字典 CSV ↓','Download full dictionary CSV ↓'),'','download')+a('/assets/report/chapter_indicator_map.csv',t('下载章节映射 CSV ↓','Download chapter map CSV ↓'),'','download')+'</div>')
    return ''.join(out)
def datasets(lang,search):
    t=lambda z,e:T(lang,z,e)
    out=[evidence_summary(lang),'<div class="reader-note">'+t('数据目录与当前入库文件同步，专题补充证据在相应图表中就近说明。代码年度、模型月度与补充快照按各表说明区分。原始文件与数据值保持不变。','The catalogue follows the current repository inventory; supplementary evidence is linked beside the relevant figures. Annual code data, monthly model data and supplemental snapshots retain their own observation windows.')+'</div><form class="filter-bar" id="dataset-filters" role="search"><label>'+t('查找数据','Find a dataset')+'<input type="search" id="dataset-q" placeholder="OpenRank / GOSR / DevScale"></label><label>'+t('所属章节','Chapter')+'<select id="dataset-chapter"><option value="">'+t('全部章节','All chapters')+'</option><option value="2">GOSO · 2</option><option value="3">GOSR · 3</option><option value="4">GOSL · 4</option><option value="5">GOSM · 5</option></select></label><button type="reset">'+t('重置筛选','Reset filters')+'</button></form><p id="dataset-count" aria-live="polite"></p><div id="dataset-list">']
    for r in R['datasets']:
        label={'2':'GOSO','3':'GOSR','4':'GOSL','5':'GOSM'}.get(r['chapter'],'GOSD');file=Path(r['path']).name
        out.append(f'<details class="dataset-entry" id="dataset-{r["dataset_id"]}" data-chapter="{r["chapter"]}" data-search="{E((" ".join(r.values())+" "+label).lower())}"><summary><small>{label} · {r["row_count"]} '+t('行','rows')+'</small><strong>'+E(file)+'</strong></summary><div class="dataset-detail">'+p(r['review_note'])+'<dl class="definition-grid"><dt>'+t('字段','Fields')+'</dt><dd><code>'+E(r['fields'].replace(';',' · '))+'</code></dd><dt>'+t('状态','Status')+'</dt><dd>'+E(r['status'])+'</dd><dt>'+t('候选关联','Candidate links')+'</dt><dd>'+(' · '.join(a(path(lang,'data/indicators/')+'#indicator-'+x,E(x)) for x in r['related_indicators'].split(';') if x) or t('背景或样本结构资料','Background or sample structure'))+'</dd><dt>SHA-256</dt><dd><code>'+r['sha256']+'</code></dd></dl><div class="section-actions">'+a('/assets/report/data/'+file,t('下载原 CSV ↓','Download original CSV ↓'),'','download')+a(source(r['path']),t('GitHub 原文件 ↗','GitHub source ↗'))+a(path(lang,'methodology/')+'#'+anchor('A.7 现有数据与外部案例的边界','method'),t('方法与范围 →','Methods and scope →'))+'</div></div></details>')
        search.append({'lang':lang,'title':file,'description':label+' · '+r['related_indicators'],'url':path(lang,'data/sources/')+'#dataset-'+r['dataset_id'],'category':t('数据来源','Data sources')})
    out.append('</div><p id="dataset-empty" hidden>'+t('没有匹配的数据，请调整筛选条件。','No matching files. Adjust the filters.')+'</p><div class="section-actions">'+a('/assets/report/dataset_inventory.csv',t('下载文件清单 CSV ↓','Download file inventory CSV ↓'),'','download')+a('/assets/report/source_register.csv',t('下载引用来源 CSV ↓','Download source register CSV ↓'),'','download')+'</div><section class="content-block" id="external-stories"><h2>'+t('开篇故事，独立保留来源','Opening stories: separate sources')+'</h2>'+p(t('LFX korg 与 ATOM 快照仅作外部背景引用，不进入 OSDI 指标、正式榜单或上述文件计数。每个故事在第一章标明时间、样本及解释边界。','LFX korg and ATOM snapshots are external background references, excluded from OSDI, formal rankings and the file count above. Chapter 1 states their dates, samples and limitations.'))+a(path(lang,'chapters/01/')+'#ch01-s01',t('阅读故事与原始引用 →','Read the stories and original citations →'))+'</section>')
    return ''.join(out)
