#!/usr/bin/env python3
"""Build bilingual architecture pages into the existing OSDG static site."""
from pathlib import Path
import argparse, html, json, shutil
import report_content as report
import goso_content as goso
import gosr_content as gosr
import landscape_content as landscape
import gosm_content as gosm
import frontmatter_content as frontmatter
import chapter6_content as action
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'content/manifest.json').read_text())
UNITS=M['front_matter']+M['chapters']+M['back_matter']
REPO='https://github.com/'+M['repository']+'/blob/'+M['source_ref']+'/'
STATES={'published':('正式发布','Published'),'preview':('正文已上线','Manuscript available'),'draft':('初稿入口','Draft available'),'outline':('结构已建立','Outline ready'),'source-confirmed':('来源已确定','Source selected')}
E=lambda s:html.escape(str(s),quote=True)
def source(path):return report.source(path)
def url(u,lang):return '/2026/'+lang+'/'+u['route']
def link(href,title,cls='inline-link'):return f'<a class="{cls}" href="{E(href)}">{E(title)}</a>'
def para(text):return '<p>'+E(text)+'</p>'
def table(headers,rows):
    return '<div class="reader-table-wrap"><table class="reader-table"><thead><tr>'+''.join('<th scope="col">'+E(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def validate():
    ids=[u['id'] for u in UNITS];routes=[u['route'] for u in UNITS]
    ids += [s['id'] for u in M['chapters'] for s in u['sections']]
    assert len(ids)==len(set(ids));assert len(routes)==len(set(routes))
    assert len(M['chapters'])==6 and sum(len(u['sections']) for u in M['chapters'])==30
    assert M['period']=={'start':'2025-07-01','end':'2026-06-30','historical_rule':'previous July 1 through report-year June 30'}
    for u in UNITS:
        for obj in [u]+u.get('sections',[]):
            for related in obj.get('related',[]):assert related in ids,related
            assert obj.get('status') in STATES
    print('Validated 6 chapters, 30 stable section IDs and cross-references.')

def body(u,lang):
    zh=lang=='zh';t=lambda z,e:z if zh else e
    if u['kind']=='summary':return frontmatter.summary(lang)
    if u['kind']=='introduction':return frontmatter.introduction(lang)
    if u['id']=='ch01':return report.chapter(lang)
    if u['id']=='ch02':return goso.chapter(lang)
    if u['id']=='ch03':return gosr.chapter(lang)
    if u['id']=='ch04':return landscape.chapter(lang)
    if u['id']=='ch05':return gosm.chapter(lang)
    if u['id']=='ch06':return action.chapter(lang)
    if u['kind']=='dpg':return gosm.appendix(lang)
    if u['kind']=='methods':return report.methods(lang)
    out=[]
    if 'sections' in u:
        out.append('<div class="reader-note">'+t('本页展示本章结构与呈现模式。各节保留初稿入口，核心发现与图表在逐章整理、核验后接入。','This page presents the chapter structure and presentation plan. Source drafts remain accessible; findings and figures will be integrated as each chapter is reviewed.')+'</div>')
        out.append('<div class="section-jump">'+''.join(link('#'+s['id'],s['number']+' '+s['title'][lang],'') for s in u['sections'])+'</div>')
        for s in u['sections']:
            status=STATES[s['status']][0 if zh else 1]
            out.append(f'<section class="chapter-section" id="{s["id"]}"><div class="section-topline"><span class="section-number">{s["number"]}</span><span>{status}</span></div><h2>{E(s["title"][lang])}</h2>')
            out.append(para(s['question'][lang]))
            out.append('<dl class="section-spec"><dt>'+t('拟呈现','Presentation')+'</dt><dd>'+E(s['presentation'][lang])+'</dd><dt>'+t('阅读顺序','Reading order')+'</dt><dd>'+t('研究问题 → 证据与解释 → 适用边界与启示','Research question → Evidence and interpretation → Scope and implications')+'</dd></dl>')
            out.append('<div class="section-actions">'+link(source(s['source_path']),t('阅读现有初稿 ↗','Read source draft ↗') if s['status']=='draft' else t('查看写作结构 ↗','View writing outline ↗'),'') )
            for rid in s.get('related',[]):
                parent=next((x for x in UNITS if x['id']==rid or any(y['id']==rid for y in x.get('sections',[]))),None)
                if parent:
                    child=next((x for x in parent.get('sections',[]) if x['id']==rid),None)
                    label=(child['number']+' '+child['title'][lang]) if child else parent['title'][lang]
                    out.append(link(url(parent,lang)+('#'+rid if child else ''),t('关联：','Related: ')+label,''))
            if s['number']=='1.2':out.append(link('/?lang='+lang+'#framework',t('探索 OSDG 圆盘 ↗','Explore the OSDG disk ↗'),''))
            if s['number']=='2.1':out.append(link('/?lang='+lang+'#chapter-2',t('查看现有图表试读 ↗','View the existing chart preview ↗'),''))
            out.append('</div></section>')
        out.append('<details class="chapter-section"><summary>'+t('章节组织原则','Chapter structure principles')+'</summary><div class="pattern">'+''.join(f'<span><b>{i+1:02d}</b>{E(x)}</span>' for i,x in enumerate(M['content_pattern'][lang]))+'</div>'+para(t('各章依研究问题组织叙事，不强制复用同一套小标题；证据、来源、边界与方法保持一致的可查证要求。','Narrative structure follows each chapter’s research question. Evidence, sources, limitations and methods remain consistently traceable.'))+'</details>')
    elif u['kind']=='methods':
        out.append('<h2>'+t('已经明确的研究边界','Established research scope')+'</h2>')
        rows=[(t('2026 主统计期','2026 period'),'2025-07-01 — 2026-06-30'),(t('历史年度','Historical periods'),t('2022—2026；上年 7 月至当年 6 月','2022–2026; previous July through report-year June')),(t('代码生态主范围','Primary code platform'),'GitHub'),(t('补充平台','Supplementary platforms'),'Gitee · AtomGit · GitLab'),(t('地区归属','Location'),t('公开位置标准化；各年度历史快照；未知单列','Standardized public profiles, annual historical snapshots, unknowns retained')),(t('项目榜单','Project rankings'),t('已核验项目样本，逐步扩充','Verified project sample, expanded in subsequent versions'))]
        out.append(table([t('范围','Scope'),t('安排','Approach')],rows))
        out.append('<h2>'+t('方法信息统一集中','A shared methods reference')+'</h2>'+para(t('指标定义、对象映射、算法版本、样本覆盖、缺失处理与局限集中在附录 A。各章图表通过稳定 ID 关联对应定义，详细核验随内容推进。','Appendix A collects indicator definitions, entity mappings, algorithm versions, sample coverage, missing-data treatment and limitations. Figures link to relevant definitions through stable IDs.')))
        out.append(link('/?lang='+lang+'#framework',t('浏览四支柱、十维度与 29 项指标 →','Explore the four pillars, ten dimensions and 29 indicators →')))
    elif u['kind']=='dpg':
        out.append('<div class="reader-note">'+t('研究评估框架草案。现有分级与案例待审阅，不作为已实施的官方认证。','Draft research assessment framework. Proposed classifications and cases require review and do not represent an implemented official certification.')+'</div>')
        out.append('<h2>'+t('从评估问题到可查证据','From assessment questions to evidence')+'</h2>')
        rows=[(t('概念与边界','Concepts and scope'),t('说明数字公共产品与本报告评估对象','Define digital public goods and the assessment scope')),(t('开放属性','Openness attributes'),t('组织访问、许可、互操作与治理证据','Organize evidence on access, licenses, interoperability and governance')),(t('研究评估矩阵','Research assessment matrix'),t('说明指标、评分依据与适用限制','Explain indicators, assessment rationale and limits')),(t('案例与行动','Cases and actions'),t('提供可复核案例，连接 5.3 开放治理','Provide verifiable cases linked to section 5.3'))]
        out.append(table([t('模块','Module'),t('作用','Purpose')],rows));out.append(link('/2026/'+lang+'/chapters/05/#ch05-s03',t('关联阅读：5.3 开源开放与分级体系 →','Related: 5.3 Openness and classification →')))
    elif u['kind']=='downloads':
        out.append('<h2>'+t('当前可获取','Available now')+'</h2><div class="front-links">'+link('/assets/osdi-indicators.csv',t('指标清单 CSV ↓','Indicator list CSV ↓'))+link('/assets/report-manifest.json',t('全书目录 JSON ↓','Report structure JSON ↓'))+link(source('outline/目录.md'),t('目录与原稿 ↗','Contents and drafts ↗'))+'</div>')
        out.append(para(t('指标清单描述框架，不是已经完成测算的研究结果。当前版本为架构预览，引用时请注明版本与访问日期。','The indicator list describes the framework, not completed measurements. This is an architecture preview; include the version and access date when referring to it.')))
        out.append(table([t('输出','Output'),t('当前进度','Current status')],[(t('中文在线报告','Chinese online report'),t('架构可浏览，正文逐章整理','Architecture available; chapter text being organized')),(t('英文在线报告','English online report'),t('结构导航已翻译，全文待中文定稿后审校','Navigation translated; full text awaits Chinese content finalization')),(t('正式 PDF','Final PDF'),t('待内容与静态图冻结后制作','To follow content and static-figure freeze')),(t('正式图表数据包','Final figure data package'),t('随图表核验与发布版本提供','To follow figure verification and release'))]))
        out.append('<button class="print-button" type="button" data-print>'+t('打印当前页面','Print this page')+'</button>')
    if u.get('source_path') and 'sections' not in u:
        out.append('<div class="section-actions">'+link(source(u['source_path']),t('查看对应源稿 ↗','View source draft ↗'),'')+'</div>')
    return ''.join(out)

def index_body(lang):
    return frontmatter.contents(lang)

def page(u,lang):
    zh=lang=='zh';t=lambda z,e:z if zh else e;other='en' if zh else 'zh'
    title=u['title'][lang] if u else t('沿着证据，读懂开源。','Follow the evidence. Understand open source.')
    deck=u['question'][lang] if u else M['theme'][lang]
    route=u['route'] if u else '';cur=u['id'] if u else ''
    nav=['<div class="nav-label">2026 / '+t('全书目录','CONTENTS')+'</div>',link('/2026/'+lang+'/',t('报告总览','Report overview'),'')]
    for obj in UNITS:
        label=(obj.get('number','')+' '+obj['title'][lang]).strip()
        nav.append('<a href="'+url(obj,lang)+'"'+(' aria-current="page"' if obj['id']==cur else '')+'>'+E(label)+'</a>')
    pnav=''
    if u:
        at=UNITS.index(u);prev=UNITS[at-1] if at else None;nxt=UNITS[at+1] if at+1<len(UNITS) else None
        pnav='<nav class="reader-page-nav" aria-label="'+t('前后篇章','Adjacent pages')+'">'+(link(url(prev,lang),'← '+prev['title'][lang],'') if prev else link('/2026/'+lang+'/',t('← 全书目录','← Contents'),''))+(link(url(nxt,lang),nxt['title'][lang]+' →','') if nxt else '')+'</nav>'
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en'}" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · OSDG 2026</title><meta name="description" content="{E(deck)}"><meta name="theme-color" content="#F3F8FA"><link rel="icon" href="/assets/Disc_Small-ColorLight.svg"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/reader.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('osdg-theme')==='dark'?'dark':'light'}}catch{{}}</script><script src="/reader.js" defer></script></head>
<body><a class="skip" href="#main">{t('跳至正文','Skip to content')}</a><header class="site-header"><div class="header-inner"><a class="brand" href="/?lang={lang}"><img class="light-logo" src="/assets/OSDG_Compact-ColorLight.svg" alt="OSDG" width="119" height="37"><img class="dark-logo" src="/assets/OSDG_Compact-ColorDark.svg" alt="OSDG" width="119" height="37"><span>REPORT / 2026</span></a><nav aria-label="{t('主要导航','Main navigation')}"><a href="/?lang={lang}">{t('报告首页','Home')}</a><a href="/2026/{lang}/" aria-current="location">{t('全书目录','Contents')}</a><a href="/?lang={lang}#framework">{t('指标体系','Framework')}</a></nav><div class="utilities"><a id="language-link" href="/2026/{other}/{route}">{t('EN','中文')}</a><span class="utility-divider"></span><button id="theme-toggle" type="button" aria-pressed="false">{t('深色','Dark')}</button></div></div></header>
<div class="shell reader-head"><span class="eyebrow">2026 EDITION / {t('全书架构预览','REPORT ARCHITECTURE PREVIEW')}</span><h1>{E(title)}</h1><p class="deck">{E(deck)}</p><div class="reader-meta"><span>2025.07 — 2026.06</span><span>{t('六章 · 30 个小节','6 chapters · 30 sections')}</span><span>{t('架构工作版 v0.2','Architecture v0.2')}</span></div></div>
<div class="shell reader-layout"><nav class="book-nav" aria-label="{t('全书目录','Report contents')}">{''.join(nav)}</nav><main id="main" class="reader-main">{body(u,lang) if u else index_body(lang)}{pnav}</main></div>
<footer class="shell"><div class="footer-brand"><strong>X-lab</strong><span>{E(M['title'][lang])}</span></div><div class="footer-links"><a href="/2026/{lang}/downloads/">{t('下载与引用','Downloads and citation')}</a><a href="{source('planning/FRAMEWORK_MODE.md')}">{t('制作说明 ↗','Production notes ↗')}</a></div></footer></body></html>'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();validate()
    args.output.mkdir(parents=True,exist_ok=True)
    for name in ['reader.css','reader.js']:shutil.copy2(ROOT/'web'/name,args.output/name)
    for lang in ['zh','en']:
        for unit in [None]+UNITS:
            dst=args.output/'2026'/lang/(unit['route'] if unit else '')/'index.html';dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(page(unit,lang))
    assets=args.output/'assets';assets.mkdir(exist_ok=True);shutil.copy2(ROOT/'content/manifest.json',assets/'report-manifest.json')
    print('Built 26 static reading pages with bilingual navigation, source links and print styles.')
if __name__=='__main__':main()
