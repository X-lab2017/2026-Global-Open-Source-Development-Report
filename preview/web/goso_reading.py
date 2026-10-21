"""Shared editorial structure for the seven GOSO sections.

Standard-library only. Preserve chart markup, data, original anchors and topic
semantics; add a common reading and navigation layer around reviewed content.
"""
from html import escape
from html.parser import HTMLParser
import re

TOPICS=[('V-Map','活跃','参与从哪里开始'),('C-Map','贡献','参与形成怎样的协作贡献'),('I-Map','影响力','项目如何积累全球影响'),('T-Map','人才','谁在支撑长期发展'),('A-Map','资产','共同创造了哪些开放资产'),('D-Map','多样性','谁能进入并持续参与共建'),('G-Map','治理与公益','如何持续维护并形成公共价值')]
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Node:
    def __init__(self,tag='',attrs=(),raw='',closed=False):
        self.tag=tag;self.attrs=dict(attrs);self.raw=raw;self.closed=closed;self.children=[];self.dirty=False
    def has(self,cls):return cls in (self.attrs.get('class') or '').split()
    def set(self,key,value):self.attrs[key]=str(value);self.dirty=True
    def add(self,*classes):self.set('class',' '.join(dict.fromkeys((self.attrs.get('class') or '').split()+list(classes))))
    def walk(self):
        for c in self.children:
            if isinstance(c,Node):
                yield c;yield from c.walk()
    def text(self):return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
    def html(self):
        body=''.join(c.html() if isinstance(c,Node) else c for c in self.children)
        if not self.tag:return body
        start=self.raw if not self.dirty else '<'+self.tag+''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())+('/>' if self.closed else '>')
        return start+body+('' if self.closed or self.tag in VOID else '</'+self.tag+'>')

class Tree(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=False);self.root=Node();self.stack=[self.root];self.feed(text)
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs,self.get_starttag_text());self.stack[-1].children.append(n)
        if tag not in VOID:self.stack.append(n)
    def handle_startendtag(self,tag,attrs):self.stack[-1].children.append(Node(tag,attrs,self.get_starttag_text(),True))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)
    def handle_entityref(self,name):self.handle_data('&'+name+';')
    def handle_charref(self,name):self.handle_data('&#'+name+';')
    def handle_comment(self,data):self.handle_data('<!--'+data+'-->')

def fragment(text):return Tree(text).root.children
def remove(root,target):
    for parent in [root,*root.walk()]:
        if target in parent.children:parent.children.remove(target);return

# Web consolidates the shared reporting calendar; PDFs remain self-contained.
REPORT_PERIOD='统计期：2025 年 7 月 1 日至 2026 年 6 月 30 日。历史年份均指前一年 7 月至当年 6 月；自然年、快照与累计样本的差异见图 2-1-1“口径与来源”。'
def web_window(n):
    return {1:'',2:'地图采用 2025 自然年数据，历史序列为 2021—2025 年；五域比较与项目来源采用报告年度，平均贡献为前十样本。',3:'全球地图采用 2025 自然年数据及 2021—2025 年历史序列；五域与项目样本采用报告年度。',4:'全球地图采用 2026 年 7 月快照，五域与十城采用报告年度。图 2-4-4 为模拟数据。',5:'代码采用报告年度；模型与数据集为发布单位的累计样本，不代表平台全量。',6:'全球地图为 2025 自然年快照；年度序列与中美样本采用报告年度。来源份额表与贡献流向表分别阅读。',7:''}[n]

def web_paragraph(text,n):
    module=__import__(['vmap','cmap','imap','tmap','amap','dmap','gmap'][n-1]+'_publication')
    original=getattr(module,'WINDOW',getattr(module,'SNAPSHOT_NOTE',''))
    return web_window(n) if text==original else text

def normalize(text,n,lang):
    if lang!='zh':text=text.replace('/2026/zh/','/2026/'+lang+'/')
    tree=Tree(text);root=next((x for x in tree.root.walk() if x.attrs.get('id')==f'ch02-s0{n}'),None)
    if not root:return text
    root.add('goso-reading-section');root.set('data-map-index',n)
    # Keep reader navigation and PDF downloads; technical exports stay in the repository.
    for anchor in list(root.walk()):
        if anchor.tag != 'a':continue
        href=anchor.attrs.get('href','')
        if ('/assets/' in href and not href.split('?')[0].endswith('.pdf')) or '/data/indicators/' in href or href=='#fig-vmap-global' or '#goso-review' in href:
            remove(root,anchor)
    for node in reversed(list(root.walk())):
        if node.tag in ('p','div') and not node.attrs and not any(isinstance(c,Node) for c in node.children) and re.fullmatch(r'[\s·|]*',node.text()):remove(root,node)
    # Only named editorial paragraphs are changed; live chart containers are untouched.
    for node in list(root.children):
        if isinstance(node,Node) and node.tag=='p':
            updated=web_paragraph(node.text(),n)
            if updated!=node.text():
                if updated:node.children=[updated]
                else:remove(root,node)
    # The chapter overview and sidebar already provide navigation. Keep one PDF link.
    for nav in [x for x in root.walk() if x.tag=='nav']:
        pdfs=[x for x in nav.walk() if x.tag=='a' and '.pdf' in x.attrs.get('href','')]
        if pdfs:
            nav.children=pdfs
            nav.set('aria-label',f'2.{n} 分节下载')
    # Relocate section methodology to the chart source panels, not the reading flow.
    for node in list(root.walk()):
        if node.tag=='details' and any(x.tag=='summary' and x.text()=='统计范围与指标说明' for x in node.children if isinstance(x,Node)):
            node.tag='template';node.dirty=True;node.set('data-goso-source-notes',str(n))
            node.children=[x for x in node.children if not (isinstance(x,Node) and x.tag=='summary')]
        if any(node.has(c) for c in ['vmap-print-evidence','cm-print-evidence','im-print-evidence','tm-print-evidence','am-print-evidence','dm-print-evidence']):remove(root,node)
    notes=next(x for x in root.walk() if 'data-goso-source-notes' in x.attrs)
    for node in list(root.children):
        if isinstance(node,Node) and node.tag=='p' and node.text()==web_window(n) and web_window(n):
            root.children.remove(node);notes.children.insert(0,node)
    # Preserve script targets but relocate their displayed source copy on demand.
    for fig in [x for x in root.walk() if x.tag=='figure']:
        for node in fig.walk():
            is_footer=bool(re.fullmatch(r'(am|dm|gm)-.+-foot',node.attrs.get('id','')))
            source_text=node.tag in ('span','p') and node.text().strip().startswith('来源：')
            if is_footer or source_text or 'data-vmap-note' in node.attrs:
                node.set('data-goso-source-only','');node.set('hidden',None)
    excluded=set()
    for node in root.walk():
        if node.tag in ('figure','dialog','template'):excluded.update([node,*node.walk()])
    for node in root.walk():
        if node in excluded:continue
        if node.tag in ('p','article') or any(node.has(c) for c in ['cm-story','cm-interpretation','im-story','im-interpretation','tm-story','tm-interpretation','am-story','am-interpretation','dm-story','dm-interpretation']):node.add('goso-body-width')
    figures=[x for x in root.walk() if x.tag=='figure']
    if not figures:return tree.root.html()
    for c in root.children:
        if isinstance(c,Node) and c.tag=='h2':c.set('id',f'ch02-s0{n}-title');root.set('aria-labelledby',c.attrs['id']);break
    for x in root.walk():
        if any(x.has(c) for c in ['vmap-position','cm-position','goso-map-position']):x.add('goso-position')
        if any(x.has(c) for c in ['vmap-window-note','cm-window-note','goso-map-window','am-review-banner','dm-review-banner','gm-review-banner']):x.add('goso-evidence-note')
        if any(x.has(c) for c in ['am-findings','dm-findings','gm-findings']):x.add('goso-findings')
        if any(x.has(c) for c in ['finding','tm-finding','am-insight','dm-insight','gm-insight']):x.add('goso-finding')
        if any(x.has(c) for c in ['am-section-head','dm-section-head','gm-section-head','section-heading','tm-section-head']):x.add('goso-story-heading')
    # A stable figure number is available across all generations; old anchors remain.
    for i,fig in enumerate(figures,1):
        fid=f'fig-2-{n}-{i}';fig.add('goso-reading-figure');fig.set('data-figure-id',fid);fig.set('data-figure-number',f'图 2-{n}-{i}')
        if fig.attrs.get('id')!=fid:
            for parent in [root,*root.walk()]:
                if fig in parent.children:
                    at=parent.children.index(fig);parent.children[at:at]=fragment(f'<span id="{fid}" class="goso-anchor" aria-hidden="true"></span>');break
        stage=fig if fig.has('chapter-one-visual') else next((x for x in fig.walk() if x.has('goso-unified-canvas')),None)
        if stage:stage.add('goso-screen');stage.set('data-figure-id',fid);stage.set('data-figure-number',f'图 2-{n}-{i}');stage.set('data-map-code',TOPICS[n-1][0])
        # Every reusable canvas carries one compact, complete bottom caption.
        title=next((x.text() for x in fig.walk() if x.tag in ('h3','h4')),'交互图')
        caption=next((x for x in fig.walk() if x.tag=='figcaption'),None)
        if caption:
            for x in caption.children:
                if isinstance(x,Node):
                    x.set('data-goso-source-only','');x.set('hidden','')
            caption.children=[x for x in caption.children if isinstance(x,Node)]
            caption.children+=fragment('<strong class="goso-figure-caption">'+escape(f'图 2-{n}-{i} {title}')+'</strong>')
            if stage is not fig:
                footer=next((x for x in stage.walk() if x.tag=='footer'),None)
                if footer:
                    footer.children.append(caption.children.pop())
                    caption.set('hidden','');caption.set('data-goso-source-only','')
        for x in fig.walk():
            if x.tag=='button' and any(k in x.attrs for k in ('data-dialog','data-tm-info','data-am-source','data-dm-source','data-gm-source')):
                if x.attrs.get('data-dialog','').endswith('source') or 'data-dialog' not in x.attrs:
                    x.set('data-goso-source-only','');x.set('hidden','')
            if x.tag=='span' and (x.has('im-meta') or x.has('cm-comparison-status') or x.has('dm-context') or x.has('gm-context') or (x.has('tm-context') and not x.has('tm-sim-badge')) or 'data-cm-period' in x.attrs or x.text().startswith('OpenDigger / OpenShare')):
                x.set('data-goso-source-only','');x.set('hidden','')
        for x in fig.walk():
            if x.tag=='button' and (x.attrs.get('data-dialog') in ('world-source','china-source','comparison-source') or 'data-tm-info' in x.attrs):
                x.children=['口径与来源'];x.add('goso-source-button')
    # Same action structure, retaining every approved paragraph and observation cue.
    action=next((x for x in root.walk() if any(x.has(c) for c in ['vmap-strategies','cm-actions','actions','tm-actions','am-actions','dm-actions','gm-actions'])),None)
    aid=f'ch02-s0{n}-actions'
    if action:
        if action.attrs.get('id'):
            action.children[0:0]=fragment(f'<span id="{aid}" class="goso-anchor" aria-hidden="true"></span>')
        else:action.set('id',aid)
        action.add('goso-actions')
        articles=[x for x in action.walk() if x.tag=='article']
        heading=next((x for x in action.walk() if x.tag=='h3'),None)
        lead=heading.text() if heading else ''
        normalized=[]
        for i,article in enumerate(articles,1):
            children=[x for x in article.children if not (isinstance(x,Node) and x.tag in ('span','b') and re.fullmatch(r'\s*0?[123]\s*',x.text()))]
            content=''.join(x.html() if isinstance(x,Node) else x for x in children)
            normalized.append(f'<article class="goso-action"><span class="goso-action-number">0{i}</span><div class="goso-action-body">{content}</div></article>')
        intros=[x.html() for x in action.children if isinstance(x,Node) and x.tag=='p']
        # The former descriptive title remains a short lead above the three actions.
        action.children=fragment((f'<span id="{aid}" class="goso-anchor" aria-hidden="true"></span>' if action.attrs.get('id')!=aid else '')+'<h3>'+(lead if n in (1,2,3,4,5,6,7) else '行动建议')+'</h3>'+('' if n in (1,2,3,4,5,6,7) else '<p class="goso-action-lead">'+lead+'</p>')+''.join(intros)+'<div class="goso-action-list">'+''.join(normalized)+'</div>')
    # Uniform local itinerary points to figures and actions.
    route=next((x for x in root.walk() if x.tag=='nav'),None)
    if route:
        route.add('goso-section-route');route.set('aria-label',f'2.{n} 本节阅读路径')
        # Reviewed publication routes retain concise reading stops and PDF downloads.
        if n not in (1,2,3,4,5,6,7):
            items=[]
            for i,fig in enumerate(figures,1):
                title=next((x.text() for x in fig.walk() if x.tag in ('h3','h4')),'交互图')
                items.append(f'<a href="#fig-2-{n}-{i}"><b>0{i}</b>{title}</a>')
            items.append(f'<a href="#{aid}"><b>→</b>行动建议</a>');route.children=fragment(''.join(items))
    for x in root.walk():
        if x.tag=='details' and any(x.has(c) for c in ['goso-gap','tm-methods','am-methods','dm-methods','gm-methods']):
            x.add('goso-evidence');summary=next((a for a in x.children if isinstance(a,Node) and a.tag=='summary'),None)
            if summary and n not in (1,2,3,4,5,6,7):summary.children=['指标反馈与待补证据']
    for x in list(root.walk()):
        if any(x.has(c) for c in ['goso-map-end','tm-end-nav','am-end-nav','dm-end-nav','gm-end-nav']):remove(root,x)
    return tree.root.html()

def overview():
    return '<section class="goso-reading-guide" aria-label="本章阅读方式"><div><span class="goso-kicker">SEVEN MAPS · ONE READING PATH</span><h3>从参与基础，走向持续共建与公共价值。</h3><p>七个主题依次展开，每节采用同一阅读路径：<b>核心问题 → 指标定位 → 核心发现 → 交互证据 → 行动建议</b>。</p></div><p class="goso-guide-hint">图内点击切换与比较；右上角查阅口径或进入演示。来源记录、近似读数、预测和模拟分别标注，待补证据集中保留。</p></section>'

def figure_directory(sections):
    groups=[];total=0
    for n,text in enumerate(sections,1):
        tree=Tree(text);figs=[x for x in tree.root.walk() if x.tag=='figure'];links=[]
        for i,fig in enumerate(figs,1):
            title=next((x.text() for x in fig.walk() if x.tag in ('h3','h4')),'交互图')
            links.append(f'<a href="#fig-2-{n}-{i}"><span>图 2-{n}-{i}</span>{title}</a>')
        total+=len(links)
        if links:groups.append(f'<div><h4>2.{n} {TOPICS[n-1][1]} · {TOPICS[n-1][0]}</h4>'+''.join(links)+'</div>')
    return '<details class="goso-figure-directory"><summary>全章图表目录 · '+str(total)+' 个图组</summary><div>'+''.join(groups)+'</div></details>'
