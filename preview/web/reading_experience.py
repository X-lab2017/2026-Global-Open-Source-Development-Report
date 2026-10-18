"""Editorial reading layer: a visible structure with evidence on demand.
Preserves source figures, tables, stable anchors and canonical definitions.
"""
import html,json,re
import chapter1_theme_map
import frontmatter_content as frontmatter
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
    out.append('<nav class="foundation-route" aria-label="'+t_('本章阅读路径','Chapter reading path')+'">'+''.join(link('#ch01-s0'+str(i+1),'<small>1.'+str(i+1)+'</small><strong>'+t_(*SHORT[i])+'</strong><span>'+t_(*QUESTIONS[i])+'</span>') for i in range(3))+'</nav>')
    intro=prepare_manuscript(report.render(report.INTRO,lang,'intro'),lang,'intro',report.INTRO,report.source)
    # The introduction's table of contents is retained as reference; the route above
    # and the interactive architecture provide the primary navigation.
    out.append('<section class="foundation-intro" id="chapter-intro"><div class="section-topline">GOSD / RESEARCH PATH</div><h2>'+t_('从开放协作到公共价值','From public value to evidence and action')+'</h2>'+intro+'</section>')
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

def home_sections(lang,chain,wheel):
    t_=lambda z,e:t(lang,z,e)
    out='<div class="journey-rail"><strong>'+t_('了解—阅读—查证—观看—复用','Understand — Read — Verify — Watch — Reuse')+'</strong><span>'+t_('一份报告，一条清晰的研究路径','One report, one clear research path')+'</span></div>'
    out+='<section class="portal-section reading-home-section" id="framework"><span class="eyebrow">01 / THE REPORT AT A GLANCE</span><h2>'+t_('一张图，读懂全书结构','The report at a glance')+'</h2><p>'+t_('从共同目标出发，沿着地图、榜单、技术全景与模型生态理解开源发展，再把证据连接到行动。','Start from shared goals, explore maps, rankings, technology landscapes and model ecosystems, then connect evidence to action.')+'</p>'+frontmatter.architecture(lang)+link(url(lang,'chapters/01/'),t_('阅读第一章：价值、目标与指标 →','Read Chapter 1: values, goals and indicators →'))+'</section>'
    out+='<section class="portal-section reading-home-section" id="contents"><span id="questions" class="reading-anchor"></span><span class="eyebrow">02 / SIX CHAPTERS · FIVE QUESTIONS</span><h2>'+t_('六章结构，五个研究问题','Six chapters, five research questions')+'</h2><p>'+t_('第一章建立研究基础；GOSO、GOSR、GOSL、GOSM 展开四个核心观察；第六章汇聚行动建议。','Chapter 1 establishes the foundation; GOSO, GOSR, GOSL and GOSM develop the research; Chapter 6 connects it to action.')+'</p><div class="reading-chapter-grid">'
    for i,c in enumerate(M['chapters']):
        detail=t_('价值 · OSDGs · OSDI','Values · OSDGs · OSDI') if i==0 else t_('七个主题 · 26 幅交互图','Seven themes · 26 interactive figures') if i==1 else t_('六类主体与影响观察','Six ranking dimensions') if i==2 else t_('4.1 深入专题 · 五个领域全景','In-depth 4.1 · Five more landscapes') if i==3 else t_('供给 · 复用 · 开放治理','Supply · Reuse · Open governance') if i==4 else t_('五节 · 三项共同任务 · 九条主体建议','Five sections · Three tasks · Nine recommendations')
        out+='<a href="'+url(lang,c['route'])+'" id="chapter-'+str(i+1)+'" class="'+('reading-foundation-link' if i==0 else 'question-link')+'"><small>'+t_('第'+str(i+1)+'章','CHAPTER '+str(i+1))+' · '+c.get('label','FOUNDATION' if i==0 else 'ACTION')+'</small><h3>'+E(c['title'][lang])+'</h3><p>'+E(c['question'][lang])+'</p><span>'+detail+' <b aria-hidden="true">↗</b></span></a>'
    out+='</div></section><section class="portal-section reading-home-section" id="explore"><span class="eyebrow">03 / FOLLOW THE EVIDENCE</span><h2>'+t_('阅读之后，就近查证与复用','Read, verify and reuse')+'</h2><div class="reading-resource-grid">'+''.join(link(url(lang,r),'<h3>'+t_(z,e)+'</h3><p>'+t_(zd,ed)+'</p><span aria-hidden="true">↗</span>') for r,z,e,zd,ed in [('data/','指标与数据','Indicators and data','查看定义、来源与统计边界。','Definitions, sources and scope.'),('presentation/','互动演示','Interactive presentation','从全书结构进入单屏探索。','Explore the report one screen at a time.'),('release/','发布资料','Release materials','获取可用资料、引用与版本记录。','Find materials, citations and versions.')])+'</div></section>'
    out+='<section class="portal-section reading-home-section" id="about"><span class="eyebrow">ABOUT GOSD</span><h2>'+t_('连接开源实践与可持续发展','Connect open source practice and sustainable development')+'</h2><p>'+t_('本报告由中国科协联合国咨商开源创新专委会牵头，连接中国开源实践与全球可持续发展议题。正文、数据与方法随研究持续更新。第一章已正式发布，报告以持续共同创造及其公共价值为共同方向。','Led by the Open Source Innovation Committee of CAST’s UN Consultative Committee, the report connects Chinese open source practice with global sustainability. Text, data and methods evolve with the research. Chapter 1 is published; the report focuses on sustained co-creation and its public value.')+'</p>'+link(url(lang,'introduction/'),t_('阅读引言 →','Read the introduction →'))+'</section>'
    return out
