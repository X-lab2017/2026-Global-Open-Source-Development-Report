"""Editorial reading layer: a visible structure with evidence on demand.
Preserves source figures, tables, stable anchors and canonical definitions.
"""
import html,json,re
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
FIGURES={'fig-report-logic':('图 1-0-1','全书结构与研究路径','Report structure'), 'fig-linux':('图 1-1-1','Linux：长期协作','Linux collaboration'), 'fig-models':('图 1-1-2','开放模型：持续衍生','Open model derivatives'), 'fig-public-goods':('图 1-1-3','SDGs 与数字公共品','SDGs and digital public goods'), 'fig-osdg-goals':('图 1-2-1','OSDGs 目标框架','OSDGs goals framework'), 'fig-osdi-map':('图 1-3-1 / 表 1.3.1','OSDI 三级结构与指标探索','OSDI structure and indicators')}

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
    # Source citations are retained in one local disclosure instead of repeated exits.
    sources=[]
    cut=next((i for i,x in enumerate(root.children) if isinstance(x,Node) and x.tag=='h3' and '资料与口径' in x.text()),None)
    if cut is not None:sources=root.children[cut:];root.children=root.children[:cut]
    for n in root.walk():
        if n.tag in ('h3','h4') and not any(p.has('chapter-table-figure') or p.has('chapter-explorer') or p.has('chapter-one-visual') for p in root.walk() if n in list(p.walk())):
            plain_heading(n)
            if n.children and isinstance(n.children[0],str):n.children[0]=re.sub(r'^\d+\.\s*','',n.children[0])
    # Compact every source table without discarding it. Long tables keep paging.
    for fig in [n for n in root.walk() if n.tag=='figure']:
        if fig.has('chapter-table-figure'):
            parent=next(p for p in [root,*root.walk()] if fig in p.children)
            title=next(n.text() for n in fig.walk() if n.tag=='h4')
            if parent.tag=='details':parent.add('reading-reference');summary=next(n for n in parent.children if isinstance(n,Node) and n.tag=='summary');summary.children=[t(lang,'对照表 · ','Reference · ')+E(title)]
            else:
                wrapper=fragment('<details class="reading-reference chapter-table-reference"><summary>'+t(lang,'对照表 · ','Reference · ')+E(title)+'</summary></details>')[0]
                parent.children[parent.children.index(fig)]=wrapper;wrapper.children.append(fig)
        elif fig.attrs.get('id') in FIGURES:
            meta=FIGURES[fig.attrs['id']];fig.add('foundation-figure');fig.set('data-reading-number',meta[0]);fig.set('data-reading-title',meta[1 if lang=='zh' else 2]);fig.set('data-slide-key',fig.attrs.get('data-slide-key') or fig.attrs['id'])
    # Adjacent source captions repeat what is already in the chart. Move them to
    # the chart's source notes, retaining limitations and attribution verbatim.
    latest=None
    for x in list(root.children):
        if not isinstance(x,Node):continue
        if x.tag=='figure' or x.tag=='details' and x.has('chapter-table-reference'):latest=x
        if x.tag=='p' and re.match(r'\s*(图|表)\s*1[-.]',re.sub('<[^>]+>','',x.html())):
            if latest:
                cap=next((a for a in latest.walk() if a.tag=='figcaption'),None)
                if cap:cap.children+=fragment('<div class="reading-source-note">'+x.html()+'</div>');root.children.remove(x)
    # Group narrative modules, keeping all legacy heading IDs.
    grouped=[];current=None
    for x in root.children:
        if isinstance(x,Node) and x.tag=='h3':
            current=fragment('<section class="reading-module" aria-labelledby="'+x.attrs.get('id','')+'"></section>')[0];grouped.append(current)
        if current:current.children.append(x)
        else:grouped.append(x)
    root.children=grouped
    if sources:
        sources[0].children=[t(lang,'来源与口径','Sources and scope')]
        detail=fragment('<details class="reading-reference reading-sources"><summary>'+t(lang,'来源与方法说明','Sources and methodology')+'</summary></details>')[0];detail.children+=sources
        detail.children+=fragment('<p class="reading-source-actions">'+link(source(src),t(lang,'GitHub 原稿 ↗','Source manuscript ↗'))+' · '+link(url(lang,'data/sources/'),t(lang,'数据目录 →','Data catalogue →'))+'</p>')
        root.children.append(detail)
    return tree.root.html()

def chapter(lang,report):
    t_=lambda z,e:t(lang,z,e)
    out=['<div class="foundation-reading">',report.translation_note(lang),'<div class="reading-tools"><span>'+t_('第一章 · 价值、目标与指标','Chapter 1 · Values, goals and indicators')+'</span><button data-print>'+t_('打印本章','Print chapter')+'</button></div><progress class="reading-progress" id="reading-progress" max="100" value="0" aria-label="'+t_('本章阅读进度','Chapter reading progress')+'"></progress>']
    out.append('<nav class="foundation-route" aria-label="'+t_('本章阅读路径','Chapter reading path')+'">'+''.join(link('#ch01-s0'+str(i+1),'<small>1.'+str(i+1)+'</small><strong>'+t_(*SHORT[i])+'</strong><span>'+t_(*QUESTIONS[i])+'</span>') for i in range(3))+'</nav>')
    intro=prepare_manuscript(report.render(report.INTRO,lang,'intro'),lang,'intro',report.INTRO,report.source)
    # The introduction's table of contents is retained as reference; the route above
    # and the interactive architecture provide the primary navigation.
    out.append('<section class="foundation-intro" id="chapter-intro"><div class="section-topline">GOSD / RESEARCH PATH</div><h2>'+t_('从公共价值，到证据与行动','From public value to evidence and action')+'</h2>'+intro+'</section>')
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
    out.append('<section class="reading-bridge"><span class="section-topline">FROM FRAMEWORK TO OBSERVATION</span><h2>'+t_('带着目标与指标，进入七个主题地图','Follow goals and measures into seven thematic maps')+'</h2><p>'+t_('第二章沿活跃、贡献、项目影响力、人才、资产、多样性、治理与社会公益展开；每节说明指标定位，并把证据连接到行动建议。','Chapter 2 connects activity, contribution, influence, talent, assets, diversity, governance and public value to measures and actions.')+'</p>'+link(url(lang,'chapters/02/'),t_('开始阅读第二章 →','Read Chapter 2 →'),'reading-next')+'</section></div>')
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
    out+='<section class="portal-section reading-home-section" id="framework"><span class="eyebrow">01 / SHARED LANGUAGE</span><h2>'+t_('报告、目标与指标，先建立共同理解','A shared language for the report, goals and measures')+'</h2>'+chain(lang)+'<div class="reading-home-framework"><div class="wheel-container">'+wheel(lang)+'</div><div><h3>'+t_('以 SDGs 为价值参照，观察开源的发展','Use SDGs as a reference for open source development')+'</h3><p>'+t_('OSDGs 提出发展方向，OSDI 组织观测证据。四大支柱、十个维度、二十九项指标交叉服务于四个核心研究章节，不自动合成为一个总分。','OSDGs frame development goals; OSDI organizes evidence. Four pillars, ten dimensions and 29 indicators cut across the four research chapters without automatically producing one score.')+'</p>'+link(url(lang,'chapters/01/'),t_('阅读第一章：价值、目标与指标 →','Read Chapter 1: values, goals and indicators →'))+'</div></div></section>'
    out+='<section class="portal-section reading-home-section" id="contents"><span id="questions" class="reading-anchor"></span><span class="eyebrow">02 / SIX CHAPTERS · FIVE QUESTIONS</span><h2>'+t_('六章结构，五个研究问题','Six chapters, five research questions')+'</h2><p>'+t_('第一章建立研究基础；GOSO、GOSR、GOSL、GOSM 展开四个核心观察；第六章汇聚行动建议。','Chapter 1 establishes the foundation; GOSO, GOSR, GOSL and GOSM develop the research; Chapter 6 connects it to action.')+'</p><div class="reading-chapter-grid">'
    for i,c in enumerate(M['chapters']):
        detail=t_('价值 · OSDGs · OSDI','Values · OSDGs · OSDI') if i==0 else t_('七个主题 · 26 幅交互图','Seven themes · 26 interactive figures') if i==1 else t_('六类主体与影响观察','Six ranking dimensions') if i==2 else t_('Agentic AI 专题已可阅读','Agentic AI sample available') if i==3 else t_('供给 · 复用 · 开放治理','Supply · Reuse · Open governance') if i==4 else t_('政府与国际组织 · 企业 · 社区','Governments · Organizations · Communities')
        out+='<a href="'+url(lang,c['route'])+'" id="chapter-'+str(i+1)+'" class="'+('reading-foundation-link' if i==0 else 'question-link')+'"><small>'+t_('第'+str(i+1)+'章','CHAPTER '+str(i+1))+' · '+c.get('label','FOUNDATION' if i==0 else 'ACTION')+'</small><h3>'+E(c['title'][lang])+'</h3><p>'+E(c['question'][lang])+'</p><span>'+detail+' <b aria-hidden="true">↗</b></span></a>'
    out+='</div></section><section class="portal-section reading-home-section" id="explore"><span class="eyebrow">03 / FOLLOW THE EVIDENCE</span><h2>'+t_('阅读之后，就近查证与复用','Read, verify and reuse')+'</h2><div class="reading-resource-grid">'+''.join(link(url(lang,r),'<h3>'+t_(z,e)+'</h3><p>'+t_(zd,ed)+'</p><span aria-hidden="true">↗</span>') for r,z,e,zd,ed in [('data/','指标与数据','Indicators and data','查看定义、来源与统计边界。','Definitions, sources and scope.'),('presentation/','互动演示','Interactive presentation','从全书结构进入单屏探索。','Explore the report one screen at a time.'),('release/','发布资料','Release materials','获取可用资料、引用与版本记录。','Find materials, citations and versions.')])+'</div></section>'
    out+='<section class="portal-section reading-home-section" id="about"><span class="eyebrow">ABOUT GOSD</span><h2>'+t_('连接开源实践与可持续发展','Connect open source practice and sustainable development')+'</h2><p>'+t_('本报告由中国科协联合国咨商开源创新专委会牵头，连接中国开源实践与全球可持续发展议题。GitHub 是正文、数据与方法的共同事实源；当前为持续完善的评审预览。','Led by the Open Source Innovation Committee of CAST’s UN Consultative Committee, the report connects Chinese open source practice with global sustainability. GitHub is the source of record for text, data and methods. This is an evolving review preview.')+'</p>'+link(url(lang,'introduction/'),t_('阅读引言 →','Read the introduction →'))+'</section>'
    return out
