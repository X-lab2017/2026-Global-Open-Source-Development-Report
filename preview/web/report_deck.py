"""A single-screen review narrative reusing the report's canonical chart documents."""
from pathlib import Path
import csv,html,json,re,shutil
from goso_reading import Tree
ROOT=Path(__file__).resolve().parents[1]
VERSION='review-1.0'
REVISION='review-1.0.1'
DATE='2026-10-16'
E=lambda x:html.escape(str(x),quote=True)
TOPICS=[
 ('V-Map','活跃','谁在参与，参与如何持续？','把实际参与纳入长期监测','全球 → 五域 → 中国；区分 GitHub 参照与国内平台补充情景。','X1 · 1.1','DevScale',['fig-vmap-global','fig-vmap-comparison','fig-vmap-china'],['全球全景','五域与五年','中国节点']),
 ('C-Map','贡献','参与形成了怎样的协作贡献？','让持续协作获得相称的认可','从活动计数进入关系与时间；开发者贡献、项目来源样本和估算分别阅读。','X2 · 2.1','OpenRankContrib',['fig-cmap-global','fig-cmap-comparison','fig-cmap-china','fig-cmap-globe'],['全球贡献','五域变化','中国贡献','协作地球']),
 ('I-Map','项目影响力','哪些项目汇聚了全球协作？','以长期共建积累全球影响','贡献投入与项目影响力的地域分布并不重合；观察对象和历史积累都很重要。','X3 · 3.1','OpenRankInflu',['fig-2-3-1','fig-2-3-2','fig-2-3-3'],['全球全景','贡献 × 影响力','中国项目成长']),
 ('T-Map','人才','谁在支撑开源的长期发展？','让人才监测服务真实成长','同时观察规模、增量与成长机会；城市数量变化不能直接解释为人才迁移。','X1 / X3 · 3.1','HighImpactTalent',['fig-2-4-1','fig-2-4-2','fig-2-4-3','fig-2-4-4','fig-2-4-5'],['全球人才','五域动能','中国节点','成长与接续','连接与 AI 潜力']),
 ('A-Map','资产','AI 时代共同创造了哪些开放资产？','建立代码、模型、数据的长期观测','供给位置因资产而异；仓库存量、活跃仓库、发布量与提交事件分别计量。','X2 · 2.1—2.3','ActiveRepo · OpenModelRelease · OpenDatasetRelease',['fig-2-5-1','fig-2-5-2','fig-2-5-3'],['全球供给','五年增长','类别与演进']),
 ('D-Map','多样性','谁能进入并持续参与全球共建？','把参与机会推进为共建机会','贡献的来源、流向与持续性共同构成多样性；中美对照只解释当前覆盖的样本。','X1 · 1.2 / X3','GlobalCollabShare · AcademicShare',['fig-2-6-2','fig-2-6-1','fig-2-6-3'],['协作流向 · 双图联动','参与广度','持续共建']),
 ('G-Map','治理与社会公益','开放投入怎样形成持久公共价值？','把维护、治理与受益证据连接起来','许可和托管提供证据入口；公共价值还需要采用、维护与真实受益的证据。','X4 · 4.1—4.2','治理成熟度 · 公共福祉',['fig-2-7-1','fig-2-7-2','fig-2-7-3','fig-2-7-4','fig-2-7-5'],['治理与公共品','制度演进','持续支持','公共服务','AI 责任'])
]

def compact(s):return re.sub(r'\s+',' ',html.unescape(s)).strip()
def extract(out):
    figures={};sections={}
    for ch in ['01','02']:
        root=Tree((out/f'2026/zh/chapters/{ch}/index.html').read_text()).root
        for node in root.walk():
            if node.has('foundation-figure') or node.has('goso-reading-figure'):
                fid=node.attrs['id'];title=next((compact(x.text()) for x in node.walk() if x.tag in ('h3','h4')),fid)
                caption=' '.join(compact(x.text()) for x in node.walk() if x.tag=='figcaption')
                figures[fid]={'id':fid,'chapter':ch,'title':title,'number':node.attrs.get('data-figure-number',node.attrs.get('data-reading-number','')),'caption':caption,'source':f'/2026/zh/chapters/{ch}/#{fid}'}
            if node.has('goso-reading-section'):
                position=next((compact(x.text()) for x in node.walk() if x.has('goso-position')),'')
                actions=[]
                for x in node.walk():
                    if x.has('goso-action'):
                        title=next((compact(y.text()) for y in x.walk() if y.tag in ('h4','h3')),'')
                        ps=[compact(y.text()) for y in x.walk() if y.tag=='p']
                        actions.append({'title':title,'body':ps[0] if ps else compact(x.text())})
                sections[node.attrs['id']]={'position':position,'actions':actions}
    return figures,sections

def data(out):
    figures,sections=extract(out)
    manifest=json.loads((ROOT/'content/manifest.json').read_text())
    with (ROOT/'content/report-assets/osdi_indicator_dictionary.csv').open() as f:indicators=list(csv.DictReader(f))
    slides=[]
    def add(title,part,kind,claim,note='',source='/2026/zh/introduction/',views=None,**kw):
        slides.append(dict(id=f's{len(slides)+1:02d}',title=title,part=part,kind=kind,claim=claim,note=note,source=source,views=views or [],**kw))
    def views(ids,labels):return [dict(figure=figures[fid],label=label) for fid,label in zip(ids,labels)]
    add('全球开源发展报告','GOSD / 2026','cover','从普惠到质量，从参与到影响。','概览 · 引言 · 第一章 · 第二章',source='/')
    add('先看全貌，再进入证据','概览 / REPORT ARCHITECTURE','chart','目标与指标，为四个核心研究章节提供共同坐标。','本次展开第一章与 GOSO；其余章节保留在全书结构中。',source='/2026/zh/chapters/01/#chapter-intro',views=views(['fig-report-logic'],['全书结构']))
    add('一个内核，连接持续的全球协作','引言与公共价值 / STORY 01','chart','开源的生命力，来自跨组织、跨地域的持续建设。','Linux 故事用于理解协作机制；背景故事数据不纳入 OSDI 指标测算。',source='/2026/zh/chapters/01/#fig-linux',views=views(['fig-linux'],['Linux · 持续协作']))
    add('一次开放，延伸到下一次创造','引言与公共价值 / STORY 02','chart','AI 时代，开放的对象从代码延伸到模型、数据与复用关系。','模型衍生是观察复用的线索；不自动等于开放资格或社会影响。',source='/2026/zh/chapters/01/#fig-models',views=views(['fig-models'],['模型 · 衍生与复用']))
    add('以可持续发展理解开源公共价值','第一章 / 1.1 VALUE','chart','开放技术需要连接可持续发展与真实公共需求。','SDGs 提供价值参照；DPGA 提供数字公共品的实践入口。',source='/2026/zh/chapters/01/#fig-public-goods',views=views(['fig-public-goods'],['SDGs × 数字公共品']))
    add('OSDGs：朝哪里发展','第一章 / 1.2 GOALS','chart','四个支柱、十个维度，让复杂生态拥有共同的发展语言。','这是本报告的开源发展目标框架，不等同于联合国官方 SDG 指标体系。',source='/2026/zh/chapters/01/#fig-osdg-goals',views=views(['fig-osdg-goals'],['目标框架']))
    add('OSDI：如何用证据判断变化','第一章 / 1.3 INDICATORS','chart','先看全貌，再沿支柱、维度和指标逐层探索。','29 项工作指标分别解释规模、供给、网络效应与公共价值，不自动合成为一个总分。',source='/2026/zh/chapters/01/#fig-osdi-map',views=views(['fig-osdi-map'],['指标探索']))
    add('如何理解开源的参与、贡献与影响力？','方法 / THREE LENSES, ONE CASE','concept','参与看人群规模，贡献看社区协作，影响力看全域联系与长期积累。','同一虚构案例、三个观察视角：点击连续讲解，或逐步探索；点击人物追踪关系。示例人数可计数，不演算 OpenRank 分值。',source='/2026/zh/chapters/01/#ch01-s03')
    add('GOSO：用七幅地图观察全球生态','第二章 / SEVEN THEMATIC MAPS','route','从谁在参与，走向如何共同创造持久公共价值。','点击任一主题进入；也可以按当前顺序连续讲解。',source='/2026/zh/chapters/02/')
    for i,(code,title,question,action,claim,pillar,indicator,ids,labels) in enumerate(TOPICS,1):
        add(f'2.{i} 全球开源{title}地图',f'GOSO / {code.upper()}','chart',claim,action,source=f'/2026/zh/chapters/02/#ch02-s0{i}',views=views(ids,labels),topic=i,question=question,mapping=pillar+' · '+indicator)
    add('把七个观察，连成三条研究主线','综合 / CROSS-MAP INSIGHTS','synthesis','观察规模，也观察关系、持续性与公共价值。','以下是对现有章节的综合归纳；模拟图只用于提出问题，不进入实测判断。',source='/2026/zh/chapters/02/')
    add('让证据指向可以持续的行动','行动 / FROM EVIDENCE TO ACTION','actions','以长期监测、全球共建和持续支持，承接开放投入。','行动方向摘自第二章七节建议，供评审整合；第六章后续进一步展开。',source='/2026/zh/chapters/02/')
    add('回到 OSDI：哪些指标正在支撑观察？','框架反馈 / INDICATOR CONNECTIONS','coverage','从章节中的实际对应关系，反向检视指标体系。','高亮表示本节“目标与指标定位”明确提及，不等于完成正式测算；未高亮不代表全报告未使用。',source='/2026/zh/chapters/01/#ch01-s03')
    add('一起评审，让报告更清晰、更有影响','评审 / REVIEW TOGETHER','review','先对齐主线与体验，再集中完善证据与判断。','保留／加强／调整 · 每条意见对应一个页码、图号和具体视图。',source='/2026/zh/')
    for i,s in enumerate(slides):
        s['notes']=[s['claim'],s['note']]
        if s['kind']=='concept':s['notes'] += ['参与：本例 9 组人—项目关系，去重后 5 位活跃开发者；开发者总量与本期活跃人数分开。','贡献：进入水情工具社区，围绕 Issue 与 PR 看见提出、讨论、提交、评审与合入；社区 OpenRank 使用完整协作网络。','影响力：拉远到开发者—仓库全域网络，共享开发者连接项目，评价部分继承历史。本例重点解释项目侧，不计算分值。','地域观察：贡献来源看开发者所在地；项目影响力分布看经核验的项目主体归属。人物、项目与国别均为虚构示例。']
        if s.get('topic'):s['notes'].append(sections['ch02-s0'+str(s['topic'])]['position'])
    # Explicit mentions only: no invented indicator-to-chapter coverage or completion claim.
    coverage={str(i):[r['indicator_code'] for r in indicators if re.search(r'(?<![A-Za-z])'+re.escape(r['indicator_code'])+r'(?![A-Za-z])',sections['ch02-s0'+str(i)]['position'])] for i in range(1,8)}
    assert len(slides)==20 and len(figures)==32 and len(indicators)==29
    return dict(version=VERSION,revision=REVISION,date=DATE,slides=slides,figures=figures,topics=[dict(code=t[0],title=t[1],question=t[2],action=t[3],slide=10+i) for i,t in enumerate(TOPICS)],sections=sections,indicators=indicators,coverage=coverage,chapters=manifest['chapters'])

def presentation(lang,out):
    d=data(out)
    payload=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    return '''<section id="demo" class="review-deck" aria-label="GOSD 20 页互动演示" data-version="'''+VERSION+'''"><div class="deck-viewport"><div class="deck-stage" id="deck-stage"><header class="deck-top"><div class="deck-identity"><b>GOSD</b><span>全球开源发展报告 <em>2026</em></span></div><span class="deck-edition">互动演示 · 评审版 1.0.1</span><button data-deck-action="unfocus" class="deck-exit-focus" hidden>返回讲解 ↙</button><button data-deck-action="outline">目录</button><button data-deck-action="fullscreen" aria-pressed="false">⛶ 全屏</button></header><div class="deck-heading"><span id="deck-part"></span><h2 id="deck-title"></h2></div><div class="deck-body" id="deck-body"></div><footer class="deck-controls"><button data-deck-action="prev" aria-label="上一页">← 上一页</button><span id="deck-counter" aria-live="polite"></span><button data-deck-action="next" aria-label="下一页">下一页 →</button><div class="deck-progress" aria-hidden="true"><i></i></div><button data-deck-action="notes">讲解提示</button><a id="deck-report" href="/2026/zh/">对应正文 ↗</a><button data-deck-action="share">复制评审链接</button><button data-deck-action="review">评审意见</button></footer><div class="deck-toast" role="status" hidden></div><div id="deck-pool" hidden></div></div></div><p class="deck-mobile-hint">建议横屏或使用桌面浏览器；左右方向键翻页，Page Up / Page Down 可在图内翻页。</p><noscript><p>互动演示需要启用 JavaScript。可直接阅读<a href="/2026/zh/chapters/01/">第一章</a>与<a href="/2026/zh/chapters/02/">第二章</a>。</p></noscript></section><dialog class="deck-dialog" id="deck-dialog"><div class="deck-dialog-head"><h2 id="deck-dialog-title"></h2><button data-deck-close aria-label="关闭">关闭 ×</button></div><div id="deck-dialog-body"></div></dialog><script type="application/json" id="gosd-deck-data">'''+payload+'''</script>'''

def export(out,base):
    for name in ['review-deck.css','review-deck.js','concept-lenses.css','concept-lenses.js','presentation-embed.css','presentation-embed.js']:
        shutil.copy2(ROOT/'web'/name,out/name)
    # Use the fully built, unchanged Chinese chart documents. The bridge only
    # opens their existing presentation dialog; all chart/data implementations stay shared.
    for ch in ['01','02']:
        original=(out/f'2026/zh/chapters/{ch}/index.html').read_text()
        doc=original.replace('</head>',f'<link rel="stylesheet" href="{base}/presentation-embed.css"><script src="{base}/presentation-embed.js" defer></script></head>')
        doc=doc.replace('<body id="top"','<body class="deck-embed-mode" id="top"')
        target=out/f'presentation/charts/ch{ch}/index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc)
    directory=out/'assets/presentation';directory.mkdir(parents=True,exist_ok=True)
    d=data(out)
    (directory/'review-1.0.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
    lines=['# GOSD 互动演示 · 评审版 1.0.1','',f'版本日期：{DATE}。范围：概览、引言、第一章与第二章。','']
    for n,s in enumerate(d['slides'],1):
        lines += [f'## {n:02d} · {s["title"]}','',s['claim'],'',s['note'],'',*([x+'\n' for x in s['notes'][2:]] if s['kind']=='concept' else []),f'正文：{base}{s["source"]}','']
    lines += ['## 评审记录模板','','页码／图号：','当前视图链接：','意见类型：保留／加强／调整','具体问题：','修改建议：','补充证据：','']
    (directory/'review-script.md').write_text('\n'.join(lines))
