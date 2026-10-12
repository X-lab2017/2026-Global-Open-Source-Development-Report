#!/usr/bin/env python3
"""Build the bilingual GOSD report portal from the report manifest."""
from pathlib import Path
import argparse,html,json,math,re,shutil
import build_reader as reader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
BASE=''
SEED=ROOT/'content/assets'
M=reader.M
F=json.loads((SEED/'framework.json').read_text())
DATA=json.loads((ROOT/'content/chart-data.js').read_text().split('=',1)[1].strip().rstrip(';'))
E=lambda s:html.escape(str(s),quote=True)
NAV=[('overview','报告概览','Overview',''),('report','报告全文','Report','report'),('data','指标与数据','Indicators & data','data/'),('presentation','互动演示','Interactive','presentation/'),('film','宣传影片','Film','film/'),('release','发布中心','Release centre','release/')]
SEARCH=[]
def tr(lang,z,e):return z if lang=='zh' else e
def home(lang):return '/' if lang=='zh' else '/en/'
def path(lang,route):return '/2026/'+lang+'/'+route

def navurl(lang,key):
    route=next(n[3] for n in NAV if n[0]==key)
    return home(lang) if not route else path(lang,'' if route=='report' else route)
def a(url,label,cls='inline-link',extra=''):return f'<a href="{E(url)}" class="{cls}" {extra}>{label}</a>'
def p(text,cls=''):return f'<p class="{cls}">{E(text)}</p>'
def note(lang):return '<div class="reader-note">'+tr(lang,'架构工作版 v0.4 · 本版用于对齐报告结构、阅读方式与发布形态。正文和年度结论仍在逐章整理与核验。','Architecture preview v0.4 · Review the report structure, reading experience and publication formats. Chapter text and annual findings are still being organized and verified.')+'</div>'
def section(sid,title,body):return f'<section id="{sid}" class="content-block"><h2>{title}</h2>{body}</section>'
def chain(lang):
    items=[('GOSD',tr(lang,'报告品牌 · 全球开源发展报告','Report · Global Open Source Development Report'),tr(lang,'承载年度研究、证据与行动建议，是整套报告的统一标识。','The common identity for the annual research, evidence and recommended actions.')),('OSDG',tr(lang,'发展目标 · 连接 UN SDGs','Development goals · Linked to UN SDGs'),tr(lang,'以开源发展目标（OSDGs）连接开源发展与可持续发展议题。','Open Source Development Goals (OSDGs) connect open source development with sustainability.')),('OSDI',tr(lang,'量化评估 · 指标体系','Quantitative assessment · Indicators'),tr(lang,'将发展目标转化为可观测、可解释、可追踪的指标。','Translate the goals into observable, interpretable and traceable measures.'))]
    return '<div class="identity-chain" aria-label="GOSD → OSDG → OSDI">'+''.join(f'<div class="identity-item"><b>{x[0]}{(" <span aria-hidden=\"true\">→</span>" if i<2 else "")}</b><small>{x[1]}</small>{p(x[2])}</div>' for i,x in enumerate(items))+'</div>'

def wheel(lang):
    def point(r,angle):return (170+r*math.sin(math.radians(angle)),170-r*math.cos(math.radians(angle)))
    def arc(r1,r2,s,e):
        x,y=point(r2,s);x2,y2=point(r2,e);x3,y3=point(r1,e);x4,y4=point(r1,s)
        return f'M{x:.2f},{y:.2f} A{r2},{r2} 0 0,1 {x2:.2f},{y2:.2f} L{x3:.2f},{y3:.2f} A{r1},{r1} 0 0,0 {x4:.2f},{y4:.2f} Z'
    out=['<svg viewBox="0 0 340 340" role="group" aria-label="'+tr(lang,'OSDG 四支柱、十维度，可选择探索','OSDG: explore four pillars and ten dimensions')+'">']
    for i,pillar in enumerate(F['P']):
        dims=[d for d in F['D'] if d[4]==i]
        start=i*90
        out.append(f'<a href="{path(lang,"data/goals/")}#pillar-{i+1}" aria-label="{E(pillar[1 if lang=="zh" else 2])}"><title>{E(pillar[1 if lang=="zh" else 2])}</title><path d="{arc(66,106,start+2,start+88)}" fill="var(--p{i+1})"/><text x="{point(85,start+45)[0]:.1f}" y="{point(85,start+45)[1]+4:.1f}" text-anchor="middle" font-size="13" fill="#082a42">X{i+1}</text></a>')
        for j,d in enumerate(dims):
            s=start+j*90/len(dims)+1;e=start+(j+1)*90/len(dims)-1;x,y=point(129,(s+e)/2)
            out.append(f'<a href="{path(lang,"data/goals/")}#dimension-{d[0].replace(".","-")}" aria-label="{E(d[1 if lang=="zh" else 2])}"><title>{E(d[1 if lang=="zh" else 2])}</title><path d="{arc(112,149,s,e)}" fill="var(--p{i+1})" opacity=".65"/><text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="12" fill="#082a42">{d[0]}</text></a>')
    out.append('<text x="170" y="172" class="wheel-center" font-size="28" font-weight="600">OSDG</text><text x="170" y="191" class="wheel-center" font-size="8" letter-spacing="2">GOALS</text></svg>')
    return ''.join(out)

def header(lang,active,route,is_home=False):
    t=lambda z,e:tr(lang,z,e);other='en' if lang=='zh' else 'zh'
    counterpart=home(other) if is_home else path(other,route)
    links=''.join(a(navurl(lang,n[0]),n[1 if lang=='zh' else 2],'','aria-current="page"' if n[0]==active else '') for n in NAV)
    return f'''<a class="skip" href="#main">{t('跳至正文','Skip to content')}</a><header class="site-header"><div class="header-inner"><a class="gosd-brand" href="{home(lang)}" aria-label="{t('GOSD 全球开源发展报告首页','GOSD report home')}"><span class="gosd-wordmark">GOSD</span><span class="brand-caption">{t('全球开源发展报告','GLOBAL OPEN SOURCE')}<small>{t('GLOBAL OPEN SOURCE DEVELOPMENT','DEVELOPMENT REPORT')}</small></span><span class="brand-year">2026</span></a><nav id="site-nav" aria-label="{t('主要导航','Main navigation')}">{links}</nav><div class="header-tools"><button id="search-open" type="button" aria-label="{t('搜索报告','Search the report')}" title="{t('搜索报告','Search the report')}"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/></svg></button><a id="language-link" href="{counterpart}" lang="{other}">{t('EN','中文')}</a><button id="theme-toggle" type="button" aria-pressed="false">{t('深色','Dark')}</button><button id="nav-toggle" class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{t('菜单','Menu')}</button></div></div></header>'''
def footer(lang):
    t=lambda z,e:tr(lang,z,e)
    return f'''<footer class="shell site-footer"><div class="footer-brand"><strong>GOSD</strong><div>{t('2026 全球开源发展报告','Global Open Source Development Report 2026')}<small>{t('架构工作版 v0.4 · PREVIEW','Architecture preview v0.4 · PREVIEW')}</small></div></div><div class="footer-links">{a(path(lang,'release/'),'发布资料' if lang=='zh' else 'Release materials','')}{a(path(lang,'methodology/'),t('方法与范围','Methods & scope'),'')}{a(path(lang,'release/versions/'),t('版本记录','Version history'),'')}{a('#top',t('回到顶部 ↑','Back to top ↑'),'')}</div></footer><dialog id="site-search" class="site-search" aria-labelledby="search-title"><div class="search-dialog-head"><h2 id="search-title">{t('搜索报告','Search the report')}</h2><button id="search-close" aria-label="{t('关闭搜索','Close search')}">×</button></div><div class="search-body"><label for="search-input">{t('查找章节、研究问题与指标','Find chapters, research questions and indicators')}</label><input id="search-input" type="search" placeholder="{t('例如：模型、公共价值、DevScale','e.g. models, public value, DevScale')}" autocomplete="off"><div id="search-results" class="search-results" aria-live="polite"></div></div></dialog>'''

def sidebar(lang,active,route,unit=None):
    t=lambda z,e:tr(lang,z,e);rows=[]
    if active=='report':
        rows=[('',t('全书目录','Contents'))]+[(u['route'],(u.get('number','')+' '+u['title'][lang]).strip()) for u in reader.UNITS]
    elif active=='data':rows=[('data/',t('指标与数据概览','Overview')),('data/goals/',t('OSDG 目标框架','OSDG goals')),('data/indicators/',t('OSDI 指标词典','OSDI indicators')),('data/explore/',t('图表与数据探索','Charts and data')),('methodology/',t('附录 A · 方法与范围','Appendix A · Methods'))]
    elif active=='release':rows=[('release/',t('发布中心','Release centre')),('downloads/',t('资料下载与引用','Downloads and citation')),('release/news/',t('动态与解读','Updates and insights')),('release/versions/',t('版本与更新','Versions and updates'))]
    elif active=='presentation':rows=[('presentation/',t('报告架构导览','Report architecture tour')),('presentation/#demo',t('进入演示','Open the presentation'))]
    elif active=='film':rows=[('film/',t('影片概览','Film overview')),('film/#film-status',t('制作进度','Production status')),('film/#related',t('相关内容','Related material'))]
    out=['<div class="nav-label">'+t('栏目目录','IN THIS SECTION')+'</div>']
    for r,label in rows:
        out.append(a(path(lang,r),E(label),'','aria-current="page"' if r==route else 'aria-current="location"' if r=='release/news/' and route.startswith(r) else ''))
        if r==route and route=='data/goals/':
            out.extend(a('#dimension-'+d[0].replace('.','-'),E(d[0]+' '+d[1 if lang=='zh' else 2]),'local-section') for d in F['D'])
        if unit and r==route:
            out.extend(a('#'+s['id'],E(s['number']+' '+s['title'][lang]),'local-section') for s in unit.get('sections',[]))
    return '<aside class="sidebar-wrap"><button class="side-toggle" type="button" aria-expanded="false" aria-controls="section-nav">'+t('栏目目录','Section contents')+' <span>＋</span></button><nav class="book-nav" id="section-nav" aria-label="'+t('栏目目录','Section contents')+'">'+''.join(out)+'</nav></aside>'

def emit(lang,route,active,title,deck,content,unit=None,scripts='',is_home=False):
    t=lambda z,e:tr(lang,z,e)
    address=home(lang) if is_home else path(lang,route)
    SEARCH.append({'lang':lang,'title':title,'description':deck,'url':address,'category':next(n[1 if lang=='zh' else 2] for n in NAV if n[0]==active)})
    if is_home:main='<main id="main" class="portal-main shell">'+content+'</main>'
    else:
        category=next(n[1 if lang=='zh' else 2] for n in NAV if n[0]==active)
        crumbs=a(home(lang),t('首页','Home'),'')+'<span class="sep">/</span>'
        if navurl(lang,active)!=address:crumbs+=a(navurl(lang,active),category,'')+'<span class="sep">/</span>'
        crumbs+='<span aria-current="page">'+E(title)+'</span>'
        pnav=''
        if unit:
            at=reader.UNITS.index(unit);previous=reader.UNITS[at-1] if at else None;following=reader.UNITS[at+1] if at<len(reader.UNITS)-1 else None
            pnav='<nav class="reader-page-nav" aria-label="'+t('前后篇章','Adjacent pages')+'">'+(a(path(lang,previous['route']),'← '+E(previous['title'][lang]),'') if previous else a(path(lang,''),t('← 全书目录','← Contents'),''))+(a(path(lang,following['route']),E(following['title'][lang])+' →','') if following else a(path(lang,'release/'),t('发布中心 →','Release centre →'),''))+'</nav>'
        main=f'<div class="shell"><nav class="breadcrumbs" aria-label="{t("当前位置","Breadcrumb")}">{crumbs}</nav><a class="return-source" id="return-source" hidden></a></div><div class="shell reader-head"><span class="eyebrow">GOSD / 2026 · {E(category)}</span><h1>{E(title)}</h1><p class="deck">{E(deck)}</p><div class="reader-meta"><span>{t("架构工作版 v0.4","Architecture preview v0.4")}</span><span>2025.07 — 2026.06</span></div></div><div class="shell reader-layout">{sidebar(lang,active,route,unit)}<main id="main" class="reader-main" data-page-title="{E(title)}">{content}{pnav}</main></div>'
    document=f'''<!doctype html><html lang="{'zh-CN' if lang=='zh' else 'en'}" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · GOSD 2026</title><meta name="description" content="{E(deck)}"><meta name="theme-color" content="#F3F8FA"><meta name="gosd-base" content="{E(BASE)}"><link rel="icon" href="/assets/gosd-mark.svg"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/reader.css"><link rel="stylesheet" href="/portal.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('osdg-theme')==='dark'?'dark':'light'}}catch{{}}</script><script src="/portal.js" defer></script>{scripts}</head><body id="top" data-section="{active}">{header(lang,active,route,is_home)}{main}{footer(lang)}</body></html>'''
    document=re.sub(r'(?P<attr>href|src)="/(?P<rest>[^/])',lambda match:match['attr']+'="'+BASE+'/'+match['rest'],document) if BASE else document
    dst=OUT/address.lstrip('/')/'index.html';dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(document)

def homepage(lang):
    t=lambda z,e:tr(lang,z,e)
    cover=f'''<figure class="cover-art" aria-label="{t('报告封面预览','Report cover preview')}"><div class="report-cover"><div class="cover-top"><b>GOSD</b><span>2026</span></div><div class="cover-title">{t('全球开源<br>发展报告','Global Open Source<br>Development Report')}<small>GLOBAL OPEN SOURCE<br>DEVELOPMENT REPORT</small></div><div class="cover-geography"></div><div class="cover-gridline"><i></i><i></i><i></i><i></i></div><div class="cover-markers"></div><div class="cover-bottom">INCLUSION · QUALITY · PARTICIPATION · IMPACT</div></div><figcaption>{t('年度报告 · 架构工作版','ANNUAL REPORT · ARCHITECTURE PREVIEW')}</figcaption></figure>'''
    out=[f'<section class="cover-hero"><div class="cover-copy"><span class="eyebrow"><span class="status-dot"></span> GOSD / GLOBAL OPEN SOURCE DEVELOPMENT</span><h1><span class="hero-year">2026</span>{t("全球开源发展报告","Global Open Source<br>Development Report")}</h1><div class="cover-english">{t("GLOBAL OPEN SOURCE DEVELOPMENT REPORT","全球开源发展报告")}</div><p class="annual-subtitle">{t("从普惠到质量，<em>从参与到影响。</em>","From inclusion to quality.<br><em>From participation to impact.</em>")}</p><p class="hero-description">{t("以开放连接人才、技术与公共价值。用一套共同的目标与指标，理解人工智能时代的全球开源发展。","Connecting talent, technology and public value through openness. A shared framework for understanding open source development in the age of AI.")}</p><div class="hero-actions">{a(path(lang,""),t("开始阅读 <span>↗</span>","Read the report <span>↗</span>"),"primary")}{a(path(lang,"presentation/"),t("快速了解报告 →","Take a guided tour →"),"text-link")}</div></div>{cover}</section>']
    out.append('<div class="journey-rail"><strong>'+t('一份报告，多种进入方式','ONE REPORT, MANY WAYS IN')+'</strong><div class="steps">'+('<i>→</i>'.join(t('了解 阅读 查证 观看 复用','Understand Read Verify Watch Reuse').split()))+'</div></div>')
    descriptions=[t('执行摘要、六章与附录','Summary, six chapters and appendices'),t('目标、指标、方法与数据','Goals, measures, methods and data'),t('按步骤了解整份报告','Explore the report step by step'),t('影片筹备中 · 查看进度','In preparation · View status'),t('下载、引用、动态与版本','Downloads, citation and updates')]
    out.append('<div class="resource-strip">'+''.join(a(navurl(lang,n[0]),'<b>'+n[1 if lang=='zh' else 2]+' <span>↗</span></b><small>'+d+'</small>','') for n,d in zip(NAV[1:],descriptions))+'</div>')
    descriptions=[t('观察人才、地域、协作与开放资产的年度变化。','Observe annual changes in talent, regions, collaboration and open assets.'),t('从地区、企业、基金会与项目榜单，理解贡献和生态影响。','Explore contributions and influence across regions, companies, foundations and projects.'),t('观察关键技术领域的项目网络、组织结构与演进趋势。','Examine project networks, organization and change across key technology fields.'),t('连接模型供给、生态衍生、复用与开放治理。','Connect model supply, ecosystem derivatives, reuse and open governance.'),t('将四个核心章节的观察，转化为有证据支持的行动建议。','Translate observations from the four core chapters into evidence-based action.')]
    out.append('<section class="portal-section" id="questions"><span class="eyebrow">01 / FIVE RESEARCH QUESTIONS</span><h2>'+t('五个问题，从观察走向行动。','Five questions, from observation to action.')+'</h2>'+p(t('GOSO、GOSR、GOSL、GOSM 四个核心章节展开研究，第六章连接行动建议。第一章提供共同的目标与指标基础。','Four core chapters — GOSO, GOSR, GOSL and GOSM — develop the research; Chapter 6 connects it to action. Chapter 1 provides the shared goals and indicators.'),'portal-intro')+'<div class="questions-grid research-questions">'+''.join(a(path(lang,ch['route']),f'<span>0{i+1} / {ch.get("label",t("行动建议","ACTION"))} · {t("第"+ch["number"]+"章","CHAPTER "+ch["number"])}</span><h3>{E(ch["question"][lang])}</h3><p>{descriptions[i]}</p>','question-link') for i,ch in enumerate(M['chapters'][1:]))+'</div></section>')
    out.append('<section class="portal-section" id="framework"><span class="eyebrow">02 / A SHARED FRAMEWORK</span><h2>'+t('从报告，到目标，再到度量。','From the report to goals and measures.')+'</h2>'+chain(lang)+'<div class="framework-panel"><div class="wheel-container">'+wheel(lang)+'</div><div><span class="eyebrow">OSDG / OPEN SOURCE DEVELOPMENT GOALS</span><h3>'+t('四个支柱，连接可持续发展。','Four pillars connect to sustainable development.')+'</h3>'+p(t('OSDGs 承接联合国 SDGs 的发展视角，OSDI 提供本报告的量化观察框架。圆盘表达分类结构；映射说明在指标页面展开。','OSDGs connect the UN SDGs’ development perspective to open source. OSDI provides the report’s measurement framework. The disk represents categories; mappings are available in the indicator pages.'))+'<div class="framework-stats">'+''.join('<div><b>'+n+'</b><small>'+v+'</small></div>' for n,v in [('4',t('发展支柱','Pillars')),('10',t('观察维度','Dimensions')),('29',t('指标定义','Indicator definitions'))])+'</div>'+a(path(lang,'data/goals/'),t('探索目标与指标 →','Explore goals and indicators →'),'text-link')+'</div></div></section>')
    out.append('<section class="portal-section" id="contents"><div class="section-heading"><div><span class="eyebrow">03 / INSIDE THE REPORT</span><h2>'+t('六章，读懂开源发展的全貌。','Six chapters on open source development.')+'</h2></div>'+a(path(lang,''),t('全书目录 ↗','Full contents ↗'),'quiet-link')+'</div><div class="chapter-index-grid">'+''.join(a(path(lang,c['route']),'<span class="num">'+c['number']+' / '+E(c.get('label',c['phase'][lang]))+'</span><h3>'+E(c['title'][lang])+'</h3>'+p(c['question'][lang]),'',f'id="chapter-{int(c["number"])}"') for c in M['chapters'])+'</div></section>')
    out.append('<section class="portal-section" id="explore"><span class="eyebrow">04 / GO FURTHER</span><h2>'+t('让证据可以查，让内容可以用。','Explore the evidence. Reuse the content.')+'</h2><div class="feature-links">'+a(path(lang,'data/explore/'),'<small>01 / DATA EXPLORER</small><h3>'+t('观察全球参与的变化','Explore changes in participation')+'</h3>'+p(t('查看已有图表试读，切换年度、地区与指数视角。','Explore the draft chart by year, region and indexed growth.')),'')+a(path(lang,'data/indicators/'),'<small>02 / OSDI DICTIONARY</small><h3>'+t('每个指标，从定义开始','Start with each indicator')+'</h3>'+p(t('按支柱检索指标，查看角色、维度与 SDG 映射。','Browse by pillar, role, dimension and SDG mapping.')),'')+a(path(lang,'release/'),'<small>03 / RELEASE CENTRE</small><h3>'+t('找到可用的发布资料','Find available release materials')+'</h3>'+p(t('统一获取报告、数据清单、阅读指南与版本信息。','Access report links, data lists, the reading guide and versions.')),'')+'</div></section>')
    out.append('<section class="portal-section" id="about"><div class="about-grid"><div><span class="eyebrow">ABOUT THIS EDITION</span><h2>'+t('一个持续完善的报告系统。','A report system that grows with the research.')+'</h2>'+p(t('本版先对齐报告的逻辑、内容结构与阅读体验。参与者围绕同一组章节、指标和证据展开工作，读者可按自己的问题进入，并在报告、方法与数据之间往返。','This edition aligns the report logic, structure and reading experience. Contributors work from shared chapters, indicators and evidence; readers can move between the report, methods and data.'))+'</div><dl class="about-facts"><dt>'+t('统计期','Period')+'</dt><dd>2025.07.01 — 2026.06.30</dd><dt>'+t('结构','Structure')+'</dt><dd>'+t('6 章 · 30 个小节 · 3 个附录','6 chapters · 30 sections · 3 appendices')+'</dd><dt>'+t('当前版本','Version')+'</dt><dd>'+t('v0.4 架构工作版 · PREVIEW','v0.4 architecture preview · PREVIEW')+'</dd><dt>'+t('最新解读','Reading guide')+'</dt><dd>'+a(path(lang,'release/news/reading-guide/'),t('如何使用本报告 →','How to use this report →'))+'</dd></dl></div></section>')
    return ''.join(out)

def data_overview(lang):
    t=lambda z,e:tr(lang,z,e)
    cards=[('data/goals/',t('OSDG 目标框架','OSDG goals'),t('四支柱、十维度，连接可持续发展。','Four pillars and ten dimensions connect to sustainable development.')),('data/indicators/',t('OSDI 指标词典','OSDI indicators'),t('检索 29 项指标，查看角色与 SDG 映射。','Explore 29 indicators, their roles and SDG mappings.')),('data/explore/',t('图表与数据探索','Charts and data'),t('交互查看现有初稿图表及其数据表。','Explore existing draft charts and their data tables.')),('methodology/',t('方法、范围与局限','Methods, scope and limitations'),t('查阅统计期、平台边界、映射与核验规则。','Review periods, platforms, mapping and verification rules.'))]
    return note(lang)+chain(lang)+'<div class="pillar-cards">'+''.join(a(path(lang,r),'<h3>'+title+'</h3>'+p(desc)+'<span>↗</span>','pillar-card',f'style="--pillar-color:var(--p{i+1})"') for i,(r,title,desc) in enumerate(cards))+'</div>'+section('evidence',t('从问题到证据，可来回查阅。','Move between questions and evidence.'),p(t('每章回答研究问题；图表连接数据表与来源；指标解释观察什么，方法说明如何统计。当前指标清单是框架定义，尚不代表 29 项测算均已完成。','Chapters pose research questions; figures link to tables and sources; indicators explain what is observed; methods explain how it is measured. The current list defines the framework and does not imply that all 29 measures are complete.')))

def goals(lang):
    t=lambda z,e:tr(lang,z,e)
    out=[chain(lang),'<div class="framework-panel"><div class="wheel-container">'+wheel(lang)+'</div><div><h2>'+t('四支柱 · 十维度','Four pillars · Ten dimensions')+'</h2>'+p(t('内圈为四个发展支柱，外圈依次按 2 / 3 / 3 / 2 组织十个维度。圆盘表示分类结构，不表示权重或排名。','The inner ring shows four pillars. Ten outer dimensions are grouped 2 / 3 / 3 / 2. The disk shows categories, not weights or rankings.'))+p(t('本报告将开源发展目标简称为 OSDGs，视觉标识使用 OSDG。下方指标所列 SDG 编号，是本报告研究框架的议题对应关系。','The goals are referred to as OSDGs in prose and OSDG in the visual identity. SDG numbers in the indicators describe thematic mappings in this report’s research framework.'),'small-note')+'</div></div>']
    for i,pillar in enumerate(F['P']):
        rows=[]
        for d in F['D']:
            if d[4]!=i:continue
            measures=[m for m in F['MEAS'] if m[0]==d[0]]
            links=' · '.join(a(path(lang,'data/indicators/')+'#indicator-'+m[2],E(m[1] if lang=='zh' else DATA['indicatorEnglish'][F['MEAS'].index(m)])) for m in measures)
            rows.append('<div class="dimension-block" id="dimension-'+d[0].replace('.','-')+'"><h3>'+d[0]+' '+E(d[1 if lang=='zh' else 2])+'</h3>'+p(t(f'{len(measures)} 项指标定义',f'{len(measures)} indicator definitions'),'small-note')+'<p>'+links+'</p></div>')
        out.append(section('pillar-'+str(i+1),pillar[0]+' · '+E(pillar[1 if lang=='zh' else 2]),p(DATA['pillarDescriptions'][i][0 if lang=='zh' else 1])+''.join(rows)))
    out.append(a(path(lang,'chapters/01/'),t('回到第一章：目标与指标体系 →','Read Chapter 1: Goals and indicators →')))
    return ''.join(out)

def indicators(lang):
    t=lambda z,e:tr(lang,z,e)
    opts='<option value="">'+t('全部支柱','All pillars')+'</option>'+''.join(f'<option value="{i+1}">{E(p[1 if lang=="zh" else 2])}</option>' for i,p in enumerate(F['P']))
    out=[note(lang),'<p>'+t('北极星指标观察关键结果，驱动指标观察发展动能，诊断指标观察结构与健康。当前先对齐名称、角色与映射；计算公式、字段口径及测算状态随核验补齐。','North Star indicators track outcomes, drivers track momentum, and diagnostics track structure and health. Names, roles and mappings are available; formulas, field definitions and measurement status will follow verification.')+'</p>',f'<form class="filter-bar" id="indicator-filters" role="search"><label>{t("查找指标","Find an indicator")}<input type="search" name="q" id="indicator-q" placeholder="{t("名称、代码或 SDG 编号","Name, code or SDG number")}"></label><label>{t("发展支柱","Pillar")}<select name="pillar" id="indicator-pillar">{opts}</select></label><button type="reset">{t("重置筛选","Reset filters")}</button></form><p class="result-count" id="indicator-count" aria-live="polite"></p><div id="indicator-list">']
    roles={'北极星':'North Star','驱动':'Driver','诊断':'Diagnostic'}
    for idx,m in enumerate(F['MEAS']):
        title=m[1] if lang=='zh' else DATA['indicatorEnglish'][idx];d=next(d for d in F['D'] if d[0]==m[0]);pi=d[4]
        out.append(f'<details class="indicator-entry" id="indicator-{m[2]}" data-pillar="{pi+1}" data-search="{E((m[1]+" "+DATA["indicatorEnglish"][idx]+" "+m[2]+" SDG "+m[4]).lower())}"><summary><span class="indicator-code">{m[2]}</span><strong>{E(title)}</strong></summary><div class="indicator-detail"><p>{t("发展维度","Dimension")}：{a(path(lang,"data/goals/")+"#dimension-"+d[0].replace(".","-"),E(d[0]+" "+d[1 if lang=="zh" else 2]))}</p><p>{t("指标角色","Role")}：{m[3] if lang=="zh" else roles[m[3]]}</p><p>{t("关联可持续发展目标","SDG mapping")}：{E(m[4].replace(","," · "))}</p><p class="small-note">{t("定义状态：框架条目已建立；公式、字段与覆盖范围待核验。","Definition status: framework entry established; formulas, fields and coverage await verification.")}</p>{a(path(lang,"methodology/"),t("查看方法与研究边界 →","Methods and research scope →"))}</div></details>')
        SEARCH.append({'lang':lang,'title':title+' · '+m[2],'description':d[1 if lang=='zh' else 2]+' · SDG '+m[4],'url':path(lang,'data/indicators/')+'#indicator-'+m[2],'category':'OSDI'})
    out.append('</div><p id="indicator-empty" class="empty-message" hidden>'+t('没有匹配的指标，请调整关键词或支柱。','No matching indicators. Try another keyword or pillar.')+'</p><div class="section-actions">'+a('/assets/osdi-indicators.csv',t('下载指标清单 CSV ↓','Download indicator CSV ↓'),'','download')+a(path(lang,'data/goals/'),t('查看目标框架 →','Explore the goals →'))+'</div>')
    return ''.join(out)

def explore(lang):
    t=lambda z,e:tr(lang,z,e)
    return f'''<div class="data-scope">{t('图表试读 · 保留现有初稿中的 2022—2026 数据。主统计期与地区口径仍需按附录 A 逐项核验；“全球南方代表组”不代表全球南方整体，组间不宜相加。','Draft chart preview · Uses the existing 2022–2026 draft values. Periods and regional definitions still require verification against Appendix A. The Global South representative group is not the whole Global South; groups should not be added together.')}</div><section id="developer-trend"><div class="chart-header"><div><h2>{t('活跃开发者的区域变化','Active developers across regions')}</h2><p class="small-note">{t('切换绝对规模或增长指数；选择地区，查看对应年度。','Switch between counts and indexed growth, select regions and inspect a year.')}</p></div><div class="chart-switch" aria-label="{t('图表口径','Chart measure')}"><button data-chart-mode="count" aria-pressed="true">{t('规模','Count')}</button><button data-chart-mode="index" aria-pressed="false">{t('2022 = 100','2022 = 100')}</button></div></div><div class="chart-pair"><div><div class="chart-canvas" id="chart-canvas"></div><div class="year-control"><label for="chart-year">{t('年度','Year')}</label><input id="chart-year" type="range" min="2022" max="2026" step="1" value="2026"><output id="chart-year-label" for="chart-year">2026</output></div></div><div class="chart-legend" id="chart-legend"></div></div><p id="chart-selection" class="sr-only" aria-live="polite"></p><div class="chart-actions"><button id="chart-table-toggle" aria-expanded="false" aria-controls="chart-table-wrap">{t('查看数据表','View data table')}</button>{a('/assets/active-developers.csv',t('下载原始试读数据 CSV ↓','Download draft data CSV ↓'),'','download')}{a(path(lang,'methodology/'),t('方法与范围 →','Methods and scope →'),'')}{a(path(lang,'chapters/02/')+'#ch02-s01',t('回到报告 2.1 →','Read report section 2.1 →'),'')}</div><div id="chart-table-wrap" class="table-container" hidden></div><noscript><p>{t('启用 JavaScript 可交互查看图表；数据 CSV 始终可下载。','Enable JavaScript to use the chart. The CSV is always available.')}</p></noscript></section><section class="content-block" id="trace"><h2>{t('沿着来源继续查证','Follow the evidence')}</h2><p>{t('本图承接第二章 2.1 全球开源活跃地图，指标对应 DevScale。正式发布前须统一地区成员、平台范围、活跃判定及年度时间窗。','This chart supports the participation observation in section 2.1 and the DevScale indicator. Region membership, platform scope, activity thresholds and annual windows must be aligned before release.')}</p><div class="front-links">{a(path(lang,'data/indicators/')+'#indicator-DevScale','DevScale →')}{a(reader.source(M['chapters'][1]['sections'][0]['source_path']),t('查看章节初稿 ↗','View chapter source ↗'))}</div></section>'''

def slides(lang):
    t=lambda z,e:tr(lang,z,e)
    return [
      (t('报告从什么问题出发？','What does the report ask?'),t('以开源发展为共同视角，理解人才、技术、连接与公共价值。','A shared view of development across talent, technology, connections and public value.'),[t('普惠 → 质量','Inclusion → Quality'),t('参与 → 影响','Participation → Impact')],''),
      (t('一条清晰的概念链','A clear conceptual chain'),t('GOSD 是报告品牌，OSDGs 连接可持续发展目标，OSDI 把目标转化为可观察的指标。','GOSD is the report identity. OSDGs connect to sustainable development; OSDI turns goals into measures.'),['GOSD → OSDG → OSDI'],'data/'),
      (t('四个支柱，共同观察发展','Four pillars of development'),t('十个维度与 29 项指标定义，为跨章节观察提供共同语言。','Ten dimensions and 29 indicator definitions provide a shared language across chapters.'),[p[1 if lang=='zh' else 2] for p in F['P']],'data/goals/'),
      (t('六章，从目标走向行动','Six chapters, from goals to action'),t('第一章奠定目标与方法；GOSO、GOSR、GOSL、GOSM 是四个核心章节；第六章连接行动。','Chapter 1 establishes the framework. GOSO, GOSR, GOSL and GOSM are the four core chapters. Chapter 6 connects the research to action.'),['GOSO · '+t('生态观测','Observatory'),'GOSR · '+t('影响力榜单','Rankings'),'GOSL · '+t('技术全景','Technology'),'GOSM · '+t('大模型洞察','Open models')],'report'),
      (t('每条发现，都能追到证据','Trace each finding to evidence'),t('章节、指标、图表、数据表与方法互相连接。图表试读展示这种阅读方式，年度结论仍待核验。','Chapters, indicators, figures, tables and methods connect. The draft chart demonstrates this reading model; annual findings still require verification.'),[t('发现 → 证据 → 解读 → 行动','Finding → Evidence → Interpretation → Action')],'data/explore/'),
      (t('从模型供给，看到生态影响','From model supply to ecosystem impact'),t('区分模型的开放供给、采用与衍生，并把开放治理作为独立的观察问题。','Distinguish open model supply, adoption and derivatives, while examining open governance in its own right.'),[t('供给','Supply'),t('复用','Reuse'),t('治理','Governance')],'chapters/05/'),
      (t('不同参与者，共同采取行动','Different participants, shared action'),t('面向政府与国际组织、企业与基金会、开发者社区，连接证据、建议与可跟踪的变化。','Connect evidence, recommendations and observable change for governments, international organizations, companies, foundations and developer communities.'),[t('政策','Policy'),t('生态','Ecosystems'),t('社区','Communities')],'chapters/06/'),
      (t('选择适合你的阅读入口','Choose your way into the report'),t('从概览理解全貌，进入全文，查证指标与数据，再获取可用的发布资料。','Start with the overview, read the report, verify indicators and data, then find available release materials.'),[t('了解 → 阅读 → 查证 → 观看 → 复用','Understand → Read → Verify → Watch → Reuse')],'release/')]

def presentation(lang):
    t=lambda z,e:tr(lang,z,e);ss=slides(lang)
    out=['<div class="reader-note">'+t('互动演示 · 当前为 8 页报告架构导览，可翻页、全屏查看，并进入对应内容。年度发现演示稿将在正文核验后完善。','Interactive presentation · An eight-slide tour of the report structure, with page controls, fullscreen and links to the corresponding content. The annual findings presentation will follow chapter verification.')+'</div><section class="demo-stage" id="demo" tabindex="0" aria-label="'+t('报告架构演示','Report architecture presentation')+'"><div class="demo-top"><b>GOSD</b><span>2026 / '+t('架构导览','ARCHITECTURE TOUR')+'</span></div><div id="demo-slides" aria-live="polite">']
    for i,(title,desc,tags,route) in enumerate(ss):
        href=home(lang) if not route else path(lang,'' if route=='report' else route)
        out.append(f'<article class="demo-content" data-slide="{i+1}" '+('hidden' if i else '')+'><span class="demo-tag">'+f'{i+1:02d} / 08</span><h2>'+title+'</h2>'+p(desc)+'<div class="demo-visual">'+''.join('<span>'+x+'</span>' for x in tags)+'</div>'+a(href,t('打开对应内容 ↗','Explore this topic ↗'),'demo-link')+'</article>')
    out.append('</div><div class="demo-controls"><button id="demo-prev" disabled>'+t('← 上一页','← Previous')+'</button><div><span id="demo-counter">1 / 8</span><button id="demo-fullscreen">'+t('全屏','Fullscreen')+'</button></div><button id="demo-next">'+t('下一页 →','Next →')+'</button></div></section><nav class="demo-outline" aria-label="'+t('演示目录','Presentation outline')+'">'+''.join(f'<button data-goto-slide="{i+1}"'+(' aria-current="step"' if not i else '')+'>'+f'{i+1:02d} '+title+'</button>' for i,(title,_,_,_) in enumerate(ss))+'</nav><p class="small-note">'+t('可用左右方向键翻页；Esc 退出全屏。演示页码会保留在链接中，方便从原处继续。','Use the left and right arrow keys. Esc exits fullscreen. The slide number is saved in the URL so you can resume where you left off.')+'</p>')
    return ''.join(out)

def film(lang):
    t=lambda z,e:tr(lang,z,e)
    return '<div class="film-poster"><span class="film-brand">GOSD / 2026</span><h2>'+t('全球开源发展报告<br>从参与到影响。','Global Open Source Development<br>From participation to impact.')+'</h2><span class="portal-status">'+t('宣传影片 · 筹备中','REPORT FILM · IN PREPARATION')+'</span><div class="cover-geography" aria-hidden="true"></div></div>'+section('film-status',t('影片进度','Production status'),p(t('本栏目为报告宣传影片保留统一入口。影片完成后将在此提供播放、字幕、文字稿与相关发布资料；当前尚无可播放的正式影片。','This is the common entry point for the report film. Playback, subtitles, a transcript and related materials will be added when production is complete. A finished film is not yet available.')))+section('related',t('现在可以先了解','Explore now'),'<div class="front-links">'+a(path(lang,'presentation/'),t('观看报告架构导览 →','View the report architecture tour →'))+a(path(lang,''),t('阅读报告 →','Read the report →'))+a(path(lang,'release/'),t('查看发布资料 →','Find release materials →'))+'</div>')

def assets(lang):
    t=lambda z,e:tr(lang,z,e)
    rows=[(t('在线报告','Online report'),t('中英文结构与导读，正文逐章完善。','Bilingual structure and reading guides; chapter text in progress.'),path(lang,''),t('开始阅读 ↗','Read ↗')),(t('指标清单 CSV','Indicator list CSV'),t('29 项指标定义、角色及 SDG 映射。','29 indicator definitions, roles and SDG mappings.'),'/assets/osdi-indicators.csv',t('下载 CSV ↓','Download CSV ↓')),(t('目录与结构 JSON','Report structure JSON'),t('六章、30 个稳定小节及附录的结构清单。','Six chapters, 30 stable sections and appendices.'),'/assets/report-manifest.json',t('下载 JSON ↓','Download JSON ↓')),(t('图表试读数据','Draft chart data'),t('既有初稿数值，统计口径待核验。','Existing draft values; statistical scope awaiting verification.'),'/assets/active-developers.csv',t('下载 CSV ↓','Download CSV ↓')),(t('互动架构导览','Interactive architecture tour'),t('8 页导览，可全屏并跳转到对应内容。','Eight slides with fullscreen and links to relevant content.'),path(lang,'presentation/'),t('打开演示 ↗','Open tour ↗')),(t('正式报告 PDF','Final report PDF'),t('待正文、图表与编辑审校完成后提供。','To follow chapter, figure and editorial review.'),None,t('待制作','Planned')),(t('宣传影片与字幕','Film and subtitles'),t('完成后从影片栏目统一提供。','Will be available in the film section.'),None,t('筹备中','In preparation')),(t('发布演示稿与媒体资料包','Launch deck and media kit'),t('随正式发布版本提供可复用材料。','Reusable materials to accompany the formal release.'),None,t('待发布','Planned'))]
    return '<div class="asset-list">'+''.join('<div class="asset-row"><div><h3>'+title+'</h3>'+p(desc)+'</div>'+(a(url,label,'','download' if url.endswith(('.csv','.json')) else '') if url else '<span class="pending">'+label+'</span>')+'</div>' for title,desc,url,label in rows)+'</div>'

def news_card(lang):
    t=lambda z,e:tr(lang,z,e)
    return a(path(lang,'release/news/reading-guide/'),'<time datetime="2026-10-12">2026.10.12 / '+t('阅读指南','READING GUIDE')+'</time><h3>'+t('了解—阅读—查证—观看—复用：如何使用本报告','Understand, read, verify, watch, reuse: a guide to the report')+'</h3>'+p(t('认识 GOSD、OSDG 与 OSDI 的分工，找到适合自己的阅读路径。','Understand GOSD, OSDG and OSDI, and choose your reading path.')),'news-card')

def releases(lang,downloads=False):
    t=lambda z,e:tr(lang,z,e)
    out=[note(lang),section('materials',t('报告与发布资料','Report and release materials'),assets(lang)),section('citation',t('引用与复用','Citation and reuse'),p(t('当前可引用为《2026 全球开源发展报告》架构工作版 v0.4，并注明访问日期和具体章节链接。正式报告题录、许可与最终引用格式将在发布版本确定。','For the current preview, use “Global Open Source Development Report 2026, architecture preview v0.4,” with your access date and a link to the relevant chapter. Formal bibliographic details, licensing and citation format will accompany the release.'))+p(t('指标清单用于说明框架；试读图表中的数值须核验后再作为研究结论引用。','The indicator list describes the framework; values in the draft chart need verification before being cited as research findings.'),'small-note'))]
    if not downloads:out.append(section('updates',t('动态与解读','Updates and insights'),news_card(lang)))
    return ''.join(out)

def guide(lang):
    t=lambda z,e:tr(lang,z,e)
    rows=[(t('了解','Understand'),t('报告概览','Overview'),home(lang),t('先看年度问题、概念链与六章结构。','Start with the annual questions, conceptual chain and six-chapter structure.')),(t('阅读','Read'),t('报告全文','Report'),path(lang,''),t('从摘要或感兴趣的章节进入，用左侧目录选择小节。','Start with the summary or a chapter; use the sidebar to select a section.')),(t('查证','Verify'),t('指标与数据','Indicators and data'),path(lang,'data/'),t('把指标、图表数据和方法放在一起核对。','Review indicators, chart data and methods together.')),(t('观看','Watch'),t('互动演示与宣传影片','Interactive and film'),path(lang,'presentation/'),t('用架构导览快速对齐，影片完成后在独立栏目观看。','Use the structure tour now; view the film in its own section when available.')),(t('复用','Reuse'),t('发布中心','Release centre'),path(lang,'release/'),t('查找当前可用材料、引用说明与版本记录。','Find available materials, citation guidance and version history.'))]
    return '<p class="small-note">2026.10.12 · '+t('架构工作版阅读指南','Architecture preview reading guide')+'</p>'+chain(lang)+''.join(section('step-'+str(i+1),f'0{i+1} / '+step,p(desc)+a(url,label+' →')) for i,(step,label,url,desc) in enumerate(rows))+section('navigation',t('随时知道自己在哪里','Keep your place'),p(t('顶栏始终保留六个栏目；左侧目录随栏目变化。面包屑标明当前位置，相关内容链接保留来处；切换语言会进入对应页面，图表筛选与演示页码可以继续保留。','The six top-level sections stay consistent, while the sidebar follows your section. Breadcrumbs show your location, topic links remember where you came from, language switching keeps the equivalent page, and charts and slides retain their state.')))

def build():
    reader.validate()
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'assets').mkdir(exist_ok=True)
    for item in SEED.iterdir():shutil.copy2(item,OUT/'assets'/item.name)
    shutil.copy2(ROOT/'content/chart-data.js',OUT/'content.js')
    (OUT/'.nojekyll').write_text('')
    for src,dst in [('base.css','style.css'),('reader.css','reader.css'),('portal.css','portal.css'),('portal.js','portal.js'),('explore.js','explore.js')]:shutil.copy2(ROOT/'web'/src,OUT/dst)
    (OUT/'assets/gosd-mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#0a2c49"/><text x="32" y="41" text-anchor="middle" font-family="Arial,sans-serif" font-weight="bold" font-size="34" fill="#edf7fa">G</text><path d="M12 51h10" stroke="#279fa9" stroke-width="3"/><path d="M22 51h10" stroke="#4e87c5" stroke-width="3"/><path d="M32 51h10" stroke="#9973b7" stroke-width="3"/><path d="M42 51h10" stroke="#82ae53" stroke-width="3"/></svg>')
    for lang in ['zh','en']:
        t=lambda z,e:tr(lang,z,e)
        emit(lang,'','overview',t('全球开源发展报告','Global Open Source Development Report'),t('从普惠到质量，从参与到影响。','From inclusion to quality, from participation to impact.'),homepage(lang),is_home=True)
        emit(lang,'','report',t('报告全文','Read the report'),t('从目标到观测，从影响到行动。六章、30 个小节与三个附录，共同组织研究与证据。','From goals to observation, from impact to action. Six chapters, 30 sections and three appendices organize the research and evidence.'),reader.index_body(lang))
        for u in reader.UNITS:
            content=reader.body(u,lang).replace('/?lang='+lang+'#framework',path(lang,'data/goals/')).replace('/?lang='+lang+'#chapter-2',path(lang,'data/explore/'))
            active='data' if u['kind']=='methods' else 'release' if u['kind']=='downloads' else 'report'
            if u['kind']=='downloads':content=releases(lang,True)
            emit(lang,u['route'],active,u['title'][lang],u['question'][lang],content,unit=u)
            for s in u.get('sections',[]):SEARCH.append({'lang':lang,'title':s['number']+' '+s['title'][lang],'description':s['question'][lang],'url':path(lang,u['route'])+'#'+s['id'],'category':u['title'][lang]})
        pages=[('data/','data',t('指标与数据','Indicators and data'),t('连接发展目标、观测指标与可查证的研究方法。','Connect development goals, indicators and verifiable research methods.'),data_overview(lang)),('data/goals/','data',t('OSDG 目标框架','OSDG goals framework'),t('以可持续发展为连接，让开放的价值可以被共同理解。','Connect open source development with sustainable development.'),goals(lang)),('data/indicators/','data',t('OSDI 指标词典','OSDI indicator dictionary'),t('从目标到度量，29 项指标的共同定义入口。','From goals to measures: a shared entry point for 29 indicators.'),indicators(lang)),('data/explore/','data',t('图表与数据探索','Charts and data explorer'),t('读图、查表、了解口径，再回到报告中的问题。','Explore a figure, inspect its table and methods, then return to the report.'),explore(lang)),('presentation/','presentation',t('互动演示','Interactive presentation'),t('用一段可自主浏览的导览，了解整份报告的架构。','A self-guided tour of the report architecture.'),presentation(lang)),('film/','film',t('宣传影片','Report film'),t('用影像讲述开源发展与公共价值。','A film about open source development and public value.'),film(lang)),('release/','release',t('发布中心','Release centre'),t('报告、资料、动态与版本，在这里统一获取。','Find report materials, updates and versions in one place.'),releases(lang)),('release/news/','release',t('动态与解读','Updates and insights'),t('报告阅读指南、内容解读与后续发布动态。','Reading guides, insights and future release updates.'),news_card(lang)),('release/news/reading-guide/','release',t('如何使用本报告','How to use this report'),t('了解—阅读—查证—观看—复用。','Understand — Read — Verify — Watch — Reuse.'),guide(lang)),('release/versions/','release',t('版本与更新','Versions and updates'),t('了解当前版本完成了什么，以及后续内容如何接入。','See what is available in this version and what follows.'),section('v04',t('v0.4 · 四个核心章节与五个研究问题','v0.4 · Four core chapters and five research questions'),p(t('2026.10.12 · 加入 GOSO、GOSR、GOSL、GOSM 核心章节标识，五个研究问题对应第二至第六章。本版作为架构预览发布，研究正文与数据逐章核验后接入。','2026.10.12 · Added the GOSO, GOSR, GOSL and GOSM labels and five questions for Chapters 2–6. Published as an architecture preview; research text and data will be integrated chapter by chapter after review.')))+section('v03',t('v0.3 · 架构与体验审阅','v0.3 · Architecture and experience review'),p(t('2026.10.12 · 统一 GOSD 主品牌；建立六栏目导航、指标词典、架构演示与发布中心；补充当前位置、来源返回与页面状态保留。','2026.10.12 · GOSD identity, six-section navigation, indicator dictionary, structure tour and release centre; location, return paths and page-state preservation.')))+section('v02',t('v0.2 · 全书结构','v0.2 · Report structure'),p(t('建立六章、30 个小节、中英文目录与稳定的章节链接。','Six chapters, 30 sections, bilingual contents and stable chapter links.')))+section('next',t('后续 · 内容核验与正式发布','Next · Verification and release'),p(t('逐章接入正文与证据，完成统计口径核验，再制作正式 PDF、发布演示稿、影片及媒体资料。','Integrate and verify chapter text and evidence, align statistical scope, then produce the final PDF, launch deck, film and media materials.'))))]
        for route,active,title,deck,content in pages:emit(lang,route,active,title,deck,content,scripts='<script src="/content.js" defer></script><script src="/explore.js" defer></script>' if route=='data/explore/' else '')
    shutil.copy2(ROOT/'content/manifest.json',OUT/'assets/report-manifest.json')
    (OUT/'assets/search-index.json').write_text(json.dumps([{**item,'url':BASE+item['url']} for item in SEARCH],ensure_ascii=False,separators=(',',':')))
    print('Built',len(list(OUT.rglob('index.html'))),'bilingual pages;',len(SEARCH),'search entries.')
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--base-path',default='')
    args=parser.parse_args()
    OUT=args.output.resolve()
    BASE=('/'+args.base_path.strip('/')) if args.base_path.strip('/') else ''
    if not re.fullmatch(r'(?:/[A-Za-z0-9_.-]+)*',BASE):parser.error('Invalid base path')
    build()
