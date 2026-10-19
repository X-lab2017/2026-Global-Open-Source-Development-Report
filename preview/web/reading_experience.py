"""Editorial reading layer: a visible structure with evidence on demand.
Preserves source figures, tables, stable anchors and canonical definitions.
"""
import html,json,re
import chapter1_theme_map
import frontmatter_content as frontmatter
import overview_visuals as overview
from pathlib import Path
from goso_reading import Tree,Node,fragment,remove
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'content/manifest.json').read_text())
E=lambda x:html.escape(str(x),quote=True)
def t(lang,z,e):return z if lang=='zh' else e
def link(url,label,cls=''):return f'<a href="{E(url)}" class="{cls}">{label}</a>'
def url(lang,route):return '/2026/'+lang+'/'+route
SHORT=[('公共价值','Public value'),('OSDGs 目标框架','OSDGs goals'),('OSDI 指标体系','OSDI indicators')]
QUESTIONS=[('为什么研究开源？','Why study open source?'),('开源朝哪里发展？','Where should it develop?'),('如何用证据观察？','How can evidence reveal change?')]
FIGURES={'fig-report-logic':('图 1-0-1','全书结构与研究路径','Report structure'), 'fig-linux':('图 1-1-1','Linux：长期协作','Linux collaboration'), 'fig-models':('图 1-1-2','开放模型：宏观趋势与衍生实例','Open model derivatives'), 'fig-public-goods':('图 1-1-3','SDGs × DPGA','SDGs and digital public goods'), 'fig-osdg-goals':('图 1-2-1','OSDGs 目标框架','OSDGs goals framework'), 'fig-osdi-map':('图 1-3-1','OSDI 三级结构与指标探索','OSDI structure and indicators')}

def plain_heading(n):
    for a in list(n.walk()):
        if a.has('heading-anchor'):remove(n,a)
    return n.text()

def prepare_manuscript(markup,lang,prefix,src,source):
    tree=Tree(markup);root=next(x for x in tree.root.walk() if x.has('manuscript'))
    # Remove obsolete preview notices, preserving scientific boundaries in the prose.
    for x in list(root.children):
        if isinstance(x,Node) and x.tag=='blockquote':
            if '本节问题' in x.text() or 'Preview v0.6' in x.text():root.children.remove(x)
    # Publication prose has no reference tables or repeated source controls.
    for n in list(root.walk()):
        if any(n.has(c) for c in ('chapter-table-reference','chapter-table-figure','viz-source','reading-source-note')):
            remove(root,n)
    for n in root.walk():
        if n.tag in ('h3','h4'):plain_heading(n)
    for fig in [n for n in root.walk() if n.tag=='figure']:
        fid=fig.attrs.get('id')
        if fid not in FIGURES:continue
        meta=FIGURES[fid];fig.add('foundation-figure');fig.set('data-reading-number',meta[0]);fig.set('data-reading-title',meta[1 if lang=='zh' else 2]);fig.set('data-slide-key',fig.attrs.get('data-slide-key') or fid)
        for cap in [n for n in fig.walk() if n.tag=='figcaption']:
            for n in list(cap.walk()):
                if n.tag=='a':remove(cap,n)
        for n in list(fig.walk()):
            if n.has('osdi-foot-tools'):
                for a in list(n.walk()):
                    if a.tag=='a':remove(n,a)
        # A static companion makes later print/PDF independent of interaction state.
        svg={'fig-report-logic':'fig-1-0-1_report_logic.svg','fig-linux':'fig-1-1-1_linux_collaboration.svg','fig-models':'fig-1-1-2_model_derivatives.svg','fig-public-goods':'fig-1-1-3_sdgs_dpga.svg','fig-osdg-goals':'fig-1-2-1_osdg_framework.svg','fig-osdi-map':'fig-1-3-1_osdi_explorer.svg'}[fid]
        if fid in ('fig-report-logic','fig-linux','fig-models','fig-public-goods'):
            svg='print/'+svg
        parent=next(n for n in [root,*root.walk()] if fig in n.children)
        parent.children.insert(parent.children.index(fig)+1,fragment('<img class="chapter-print-figure" src="/assets/report/'+svg+'" alt="'+E(meta[1 if lang=='zh' else 2])+'">')[0])
    # Group narrative modules, keeping all legacy heading IDs.
    grouped=[];current=None
    for x in root.children:
        if isinstance(x,Node) and x.tag=='h3':
            current=fragment('<section class="reading-module" aria-labelledby="'+x.attrs.get('id','')+'"></section>')[0];grouped.append(current)
        if current:current.children.append(x)
        else:grouped.append(x)
    root.children=grouped
    return tree.root.html()

def chapter(lang,report):
    t_=lambda z,e:t(lang,z,e)
    out=['<div class="foundation-reading">',report.translation_note(lang),'<div class="reading-tools"><span>'+t_('第一章 · 价值、目标与指标','Chapter 1 · Values, goals and indicators')+'</span><button data-print>'+t_('打印本章','Print chapter')+'</button></div><progress class="reading-progress" id="reading-progress" max="100" value="0" aria-label="'+t_('本章阅读进度','Chapter reading progress')+'"></progress>']
    out.append('<aside class="chapter-sample-edition" aria-label="'+t_('章首与 1.1 双版本样章','Opening and section 1.1 sample editions')+'"><div><strong>'+t_('章首＋1.1 · 双版本样章','Opening + 1.1 · two editions')+'</strong><span>'+t_('同一份完整正文；网页交互探索，PDF 独立阅读。','One complete manuscript; explore online or read the self-contained Chinese PDF.')+'</span></div>'+link('/assets/report/chapter1/GOSD-2026-chapter1-sample.pdf',t_('阅读 PDF · 8 页 ↗','Read PDF · 8 pages ↗'),'chapter-sample-pdf')+'</aside>')
    route='<nav class="foundation-route" aria-label="'+t_('本章阅读路径','Chapter reading path')+'">'+''.join(link('#ch01-s0'+str(i+1),'<small>1.'+str(i+1)+'</small><strong>'+t_(*SHORT[i])+'</strong><span>'+t_(*QUESTIONS[i])+'</span>') for i in range(3))+'</nav>'
    intro=prepare_manuscript(report.render(report.INTRO,lang,'intro'),lang,'intro',report.INTRO,report.source)
    # Introduce the chapter's purpose before asking the reader to choose a path.
    intro=intro.replace('<figure ',route+'<figure ',1)
    out.append('<section class="foundation-intro" id="chapter-intro" aria-label="'+t_('本章导读与全书结构','Chapter introduction and report structure')+'">'+intro+'</section>')
    for i,src in enumerate(report.PARTS):
        s=M['chapters'][0]['sections'][i];sid=s['id']
        body=prepare_manuscript(report.render(src,lang,sid),lang,sid,src,report.source)
        # Update publication status without inventing a formula or changing a score.
        body=body.replace('具体关系识别、模型去重、算法版本及结果将在 GOSM 资料补齐后更新。','仓库已收录 ModelRank v1 月度结果与模型复用资料；关系识别、模型去重、算法版本及结果复现仍需核验，月度榜单不等于年度汇总。')
        modules=[(hid,re.sub(r'^\d+\.\s*','',label)) for hid,label,level in report.headings(src,sid) if level==2 and '资料与口径' not in label]
        out.append('<section class="chapter-section foundation-section" id="'+sid+'" aria-labelledby="'+sid+'-title"><div class="section-topline">1.'+str(i+1)+' / '+['VALUE','GOALS','INDICATORS'][i]+'</div><h2 id="'+sid+'-title">'+E(s['title'][lang])+'</h2><p class="foundation-question">'+E(s['question'][lang])+'</p><nav class="foundation-modules" aria-label="'+t_('本节模块','Section modules')+'">'+''.join(link('#'+hid,'<small>'+str(k+1).zfill(2)+'</small>'+E(label)) for k,(hid,label) in enumerate(modules))+'</nav>'+body)
        prev=('#chapter-intro',t_('全书结构','Report structure')) if i==0 else ('#ch01-s0'+str(i),t_(*SHORT[i-1]))
        nex=('#ch01-s0'+str(i+2),t_(*SHORT[i+1])) if i<2 else (url(lang,'chapters/02/'),t_('第二章 · GOSO','Chapter 2 · GOSO'))
        out.append('<nav class="foundation-section-nav" aria-label="'+t_('继续阅读','Continue reading')+'">'+link(prev[0],'← '+prev[1])+link(nex[0],nex[1]+' →')+'</nav></section>')
    out.append('<section class="reading-bridge" id="theme-maps"><span class="section-topline">FROM FRAMEWORK TO OBSERVATION</span><h2>'+t_('带着目标与指标，进入七个主题地图','Follow goals and measures into seven thematic maps')+'</h2><p>'+t_('从关心的发展目标出发，找到相应的观察主题，再进入第二章查看具体的格局与变化。','Start with a development goal, find a theme, then explore its patterns and changes in Chapter 2.')+'</p>'+chapter1_theme_map.render(lang)+'<img class="chapter-print-figure" src="/assets/report/fig-1-3-2_theme_maps.svg" alt="'+t_('四大支柱与七个主题地图的阅读导览','Four pillars and seven thematic maps')+'"></section></div>')
    return ''.join(out)

def sidebar(lang,report):
    t_=lambda z,e:t(lang,z,e)
    out='<div class="nav-label">'+t_('第一章 · 阅读路径','CHAPTER 1 · READING PATH')+'</div>'+link(url(lang,''),t_('← 全书目录','← Contents'))+link(url(lang,'introduction/'),t_('引言','Introduction'))+link('#chapter-intro',t_('全书结构','Report structure'))
    for i,src in enumerate(report.PARTS):
        sec=M['chapters'][0]['sections'][i];out+='<div class="focus-group" data-reading-section="'+sec['id']+'">'+link('#'+sec['id'],E(sec['number']+' '+sec['title'][lang]),'local-section')+'<div class="focus-subsections" hidden>'
        out+=''.join(link('#'+hid,E(re.sub(r'^\d+\.\s*','',label))) for hid,label,level in report.headings(src,sec['id']) if level==2 and '资料与口径' not in label)
        out+='</div></div>'
    out+='<div class="focus-next">'+link(url(lang,'chapters/02/'),t_('第二章 · GOSO →','Chapter 2 · GOSO →'))+'</div>'
    return out

def introduction(lang,unit):
    t_=lambda z,e:t(lang,z,e)
    raw=(ROOT/unit['source_path']).read_text();paras=[x.strip() for x in raw.split('\n\n') if x.strip() and not x.startswith(('#','>'))]
    # This describes the intended report window; existing snapshots retain theirs.
    paras[2]=paras[2].replace('历史序列按相同年度窗口组织。','年度比较应在相同窗口下进行；当前图表同时保留来源标注的自然年、报告年度、月度与快照数据，尚未对齐的序列分别说明。')
    paras[3]='全书从目标与指标出发，依次进入生态观测、影响力评估、技术全景和大模型发展，最终落到展望与行动。当前可从第一章建立价值与方法坐标，再进入第二章七个主题地图；也可按问题选择第三章榜单和第四章 Agentic AI 专题。需要复核或复用研究时，可从图表的口径与来源入口进入数据说明与方法附录。执行摘要与综合行动建议随各章证据核验继续完善。'
    groups=[('intro-context','为什么需要这份报告','Why this report',paras[0]),('intro-framework','共同的目标与研究语言','Shared goals and research language',paras[1]),('intro-scope','读懂证据的范围','Understand the scope',paras[2]),('intro-reading','从哪里开始阅读','Where to start',paras[3]),('intro-action','从研究走向共同建设','From research to co-creation',paras[4])]
    out='<div class="report-introduction">'
    if lang!='zh':out+='<p class="reader-note">The Chinese introduction is shown below; translation is in preparation.</p>'
    out+='<nav class="intro-route" aria-label="'+t_('引言阅读路径','Introduction reading path')+'">'+''.join(link('#'+sid,t_(z,e)) for sid,z,e,_ in groups)+'</nav>'
    for i,(sid,z,e,body) in enumerate(groups):
        out+='<section class="reading-module" id="'+sid+'"><div class="section-topline">0'+str(i+1)+'</div><h2>'+t_(z,e)+'</h2><p lang="zh-CN">'+E(body)+'</p>'
        if sid=='intro-reading':
            out+='<div class="intro-start">'+''.join(link(url(lang,route),'<strong>'+t_(zh,en)+'</strong><span>'+t_(zd,ed)+'</span>') for route,zh,en,zd,ed in [('chapters/01/','建立共同理解','Build shared understanding','第一章 · 价值、目标与指标','Chapter 1 · Values, goals and indicators'),('chapters/02/','观察全球生态','Observe the ecosystem','第二章 · 七个主题地图','Chapter 2 · Seven thematic maps'),('data/','复核研究证据','Inspect the evidence','指标、数据与方法','Measures, data and methods')])+'</div>'
        out+='</section>'
    out+='</div>'
    return out

def reading_start_visual(kind):
    """Small illustrative reading cues, not charts or additional controls."""
    icons={
        'overview':'<circle cx="12" cy="12" r="8.5"/><path d="m15.6 8.4-2.2 5-5 2.2 2.2-5Z"/>',
        'sequence':'<path d="M12 6C9 3.5 5.5 3.5 2.5 4.5v14C6 17.5 9 18 12 20c3-2 6-2.5 9.5-1.5v-14C18.5 3.5 15 3.5 12 6Zm0 0v14M6 8l3 1m-3 3 3 1m6-4 3-1m-3 5 3-1"/>',
        'topic':'<circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6M7 8h6m-6 4h4"/>'}
    icon='<svg class="reading-start-icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'+icons[kind]+'</svg>'
    if kind=='overview':
        paths=['M64 18H84C119 18 111 40 145 40H194','M78 40H194','M64 62H84C119 62 111 40 145 40H194']
        drawing='<g class="reading-art-quiet"><path d="M18 18h34M18 40h48M18 62h34"/><circle cx="7" cy="18" r="2"/><circle cx="7" cy="40" r="2"/><circle cx="7" cy="62" r="2"/></g>'
        drawing+=''.join('<path class="reading-art-track" d="'+p+'"/><path class="reading-art-flow" pathLength="100" style="--cue-delay:-'+str(i*2.4)+'s" d="'+p+'"/>' for i,p in enumerate(paths))
        drawing+='<rect class="reading-art-sheet reading-art-focus" x="194" y="12" width="110" height="56" rx="6"/><path class="reading-art-ink" d="M209 26h49M209 39h78M209 52h61"/><path class="reading-art-check" d="m277 24 4 4 8-8"/>'
    elif kind=='sequence':
        drawing='<path class="reading-art-track" d="M34 64H284"/>'
        for i in range(6):
            x=15+i*50
            drawing+=f'<g class="reading-art-page" style="--cue-delay:-{(6-i)*1.2}s"><rect class="reading-art-sheet" x="{x}" y="10" width="38" height="42" rx="4"/><path class="reading-art-quiet" d="M{x+10} 20h18"/><text x="{x+19}" y="39">{i+1:02}</text><circle class="reading-art-stop" cx="{x+19}" cy="64" r="2.5"/></g>'
        drawing+='<circle class="reading-art-traveller" cx="34" cy="64" r="3"/>'
    else:
        paths=['M56 40H88C115 40 108 15 136 15H184','M56 40H184','M56 40H88C115 40 108 65 136 65H184']
        drawing='<circle class="reading-art-sheet" cx="29" cy="34" r="15"/><path class="reading-art-ink" d="m40 45 11 11M23 31h12m-12 6h8"/>'
        for i,p in enumerate(paths):
            y=6+i*25
            drawing+='<path class="reading-art-track" d="'+p+'"/><path class="reading-art-flow" pathLength="100" style="--cue-delay:-'+str(i*2.4)+'s" d="'+p+'"/>'
            drawing+=f'<g class="reading-art-topic" style="--cue-delay:-{i*2.4}s"><rect class="reading-art-sheet" x="184" y="{y}" width="120" height="18" rx="4"/><circle class="reading-art-stop" cx="195" cy="{y+9}" r="2"/><path class="reading-art-quiet" d="M206 {y+9}h{[73,50,62][i]}"/></g>'
    return icon,'<svg class="reading-start-art" viewBox="0 0 320 80" width="320" height="80" aria-hidden="true" focusable="false">'+drawing+'</svg>'

def chapter_entry_title(chapter,lang):
    title=chapter['title'][lang].split('（')[0].split(' (')[0]
    number=t(lang,'第'+chapter['number']+'章','Chapter '+chapter['number'])
    return '<span class="overview-chapter-number">'+E(number)+'</span> · '+E(title)

def home_sections(lang,chain,wheel):
    t_=lambda z,e:t(lang,z,e)
    stops=[('framework','overview','阅读起点','Start'),('contents','gosl','研究视角','Research'),('explore','data','查证复用','Resources'),('about','together','共同建设','Co-create')]
    out='<div class="overview-home"><nav class="overview-page-nav" aria-label="'+t_('本页导览','On this page')+'"><span>'+t_('本页导览','ON THIS PAGE')+'</span><div>'+''.join('<a href="#'+sid+'">'+overview.icon(kind)+'<span>'+t_(z,e)+'</span></a>' for sid,kind,z,e in stops)+'</div></nav>'
    out+='<section class="portal-section home-reading-start" id="framework" data-home-motion><span class="eyebrow">01 / START READING</span><h2>'+t_('找到你的阅读起点','Find your starting point')+'</h2><p>'+t_('先用摘要把握全貌，再从第一章建立共同语言，或按问题进入研究。','Start with the summary, build a shared foundation in Chapter 1, or follow a question into the research.')+'</p><nav aria-label="'+t_('选择阅读方式','Choose a reading path')+'">'
    for kind,route,z,e,detail,ed,anchor in [('overview','summary/','快速了解','Get the overview','执行摘要 · 把握主要发现与行动方向','Executive summary · Findings and actions',''),('sequence','chapters/01/','系统阅读','Read in sequence','第一章 · 价值、目标与观察方法','Chapter 1 · Values, goals and methods','chapter-1'),('topic','','按需查阅','Find a topic','全书目录 · 直接选择章节与小节','Contents · Choose a chapter or section','')]:
        icon,art=reading_start_visual(kind)
        description='<span class="reading-start-description">'+(chapter_entry_title(M['chapters'][0],lang) if kind=='sequence' else t_(detail,ed))+'</span>'
        out+='<a class="reading-start-card reading-start-'+kind+'" href="'+url(lang,route)+'"'+(' id="'+anchor+'"' if anchor else '')+'><strong>'+icon+'<span>'+t_(z,e)+'</span><i aria-hidden="true">↗</i></strong>'+description+art+'</a>'
    out+='</nav></section><section class="portal-section reading-home-section" id="contents"><span id="questions" class="reading-anchor"></span><span class="eyebrow">02 / FOUR RESEARCH PERSPECTIVES</span><h2>'+t_('从你关心的问题进入研究','Follow the question that matters to you')+'</h2><div class="reading-chapter-grid">'
    topics={
        'GOSO':('参与 · 贡献 · 影响力','Participation · Contribution · Influence'),
        'GOSR':('主体位置 · 影响力 · 变化','Positions · Influence · Change'),
        'GOSL':('技术分类 · 生态结构 · 演进','Categories · Structure · Evolution'),
        'GOSM':('模型供给 · 复用衍生 · 开放程度','Supply · Reuse · Openness')}
    for c in M['chapters'][1:5]:
        key=c['label'].lower()
        chapter_label=t_('第'+c['number']+'章','Chapter '+c['number'])+' · '+c['label']
        chapter_title=c['title'][lang].split('（')[0].split(' (')[0]
        out+='<a href="'+url(lang,c['route'])+'" id="chapter-'+c['number']+'" class="question-link overview-card overview-'+key+'" data-home-motion><small class="overview-chapter-eyebrow">'+E(chapter_label)+'</small><h3 class="overview-chapter-title">'+overview.icon(key)+'<span>'+E(chapter_title)+'</span></h3><div class="overview-card-body"><p>'+E(c['question'][lang])+'</p>'+overview.art(key)+'</div><span class="overview-card-footer"><span>'+t_(*topics[c['label']])+'</span><b>'+t_('进入本章','Explore chapter')+' <i aria-hidden="true">↗</i></b></span></a>'
    out+='</div><div class="home-action-next" id="chapter-6"><a class="home-action-link overview-action-card overview-card" data-home-motion href="'+url(lang,'chapters/06/')+'"><div><h3 class="overview-chapter-title">'+overview.icon('action')+'<span>'+chapter_entry_title(M['chapters'][5],lang)+'</span></h3><p>'+t_('把研究带回行动：三项共同任务，九条面向政府、企业与社区的建议。','Bring research into action: three shared tasks and nine recommendations for institutions, companies and communities.')+'</p></div>'+overview.art('action')+'<span class="overview-cta">'+t_('阅读行动建议','Read the recommendations')+' <i aria-hidden="true">→</i></span></a></div></section>'
    out+='<section class="portal-section reading-home-section" id="explore"><span class="eyebrow">03 / VERIFY & REUSE</span><h2>'+t_('阅读之后，就近查证与复用','Read, verify and reuse')+'</h2><div class="reading-resource-grid">'
    for kind,r,z,e,zd,ed,cta,ctae in [('data','data/','指标与数据','Indicators and data','查看定义、来源与统计边界。','Definitions, sources and scope.','查阅证据','Inspect evidence'),('presentation','presentation/','互动演示','Interactive presentation','进入单屏探索与讲解。','Explore the report one screen at a time.','开始探索','Start exploring'),('release','release/','发布资料','Release materials','获取可用资料、引用与版本记录。','Find materials, citations and versions.','查看资料','Find materials')]:
        out+='<a class="overview-card overview-resource overview-'+kind+'" data-home-motion href="'+url(lang,r)+'"><h3>'+overview.icon(kind)+'<span>'+t_(z,e)+'</span></h3><p>'+t_(zd,ed)+'</p>'+overview.art(kind)+'<span class="overview-resource-cta">'+t_(cta,ctae)+' <i aria-hidden="true">↗</i></span></a>'
    out+='</div></section>'
    out+='<section class="portal-section reading-home-section overview-about" id="about" data-home-motion><span class="eyebrow">04 / CONTINUED CO-CREATION</span><div class="overview-about-layout"><div><h2>'+overview.icon('together')+'<span>'+t_('连接开源实践与可持续发展','Connect open source practice and sustainable development')+'</span></h2><p>'+t_('本报告由中国科协联合国咨商开源创新专委会牵头，连接中国开源实践与全球可持续发展议题。正文、数据与方法随研究持续更新，报告以持续共同创造及其公共价值为共同方向。','Led by the Open Source Innovation Committee of CAST’s UN Consultative Committee, the report connects open source practice with global sustainability. Text, data and methods evolve with the research, supporting sustained co-creation and its public value.')+'</p><div class="overview-about-links">'+link(url(lang,'introduction/'),t_('阅读引言','Read the introduction')+' <i aria-hidden="true">→</i>')+link('https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/issues',t_('参与共同建设','Contribute to the report')+' <i aria-hidden="true">↗</i>')+'</div></div>'+overview.art('together')+'</div></section></div>'
    return out
