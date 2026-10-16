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

def normalize(text,n,lang):
    if lang!='zh':text=text.replace('/2026/zh/','/2026/'+lang+'/')
    tree=Tree(text);root=next((x for x in tree.root.walk() if x.attrs.get('id')==f'ch02-s0{n}'),None)
    if not root:return text
    root.add('goso-reading-section');root.set('data-map-index',n)
    # Some English sections intentionally link to the Chinese review.
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
        action.children=fragment((f'<span id="{aid}" class="goso-anchor" aria-hidden="true"></span>' if action.attrs.get('id')!=aid else '')+'<span class="goso-kicker">FROM OBSERVATION TO ACTION</span><h3>行动建议</h3><p class="goso-action-lead">'+lead+'</p>'+''.join(intros)+'<div class="goso-action-list">'+''.join(normalized)+'</div>')
    # Uniform local itinerary points to figures and actions.
    route=next((x for x in root.walk() if x.tag=='nav'),None)
    if route:
        route.add('goso-section-route');route.set('aria-label',f'2.{n} 本节阅读路径')
        items=[]
        for i,fig in enumerate(figures,1):
            title=next((x.text() for x in fig.walk() if x.tag in ('h3','h4')),'交互图')
            items.append(f'<a href="#fig-2-{n}-{i}"><b>0{i}</b>{title}</a>')
        items.append(f'<a href="#{aid}"><b>→</b>行动建议</a>');route.children=fragment(''.join(items))
    for x in root.walk():
        if x.tag=='details' and any(x.has(c) for c in ['goso-gap','tm-methods','am-methods','dm-methods','gm-methods']):
            x.add('goso-evidence');summary=next((a for a in x.children if isinstance(a,Node) and a.tag=='summary'),None)
            if summary:summary.children=['指标反馈与待补证据']
    for x in list(root.walk()):
        if any(x.has(c) for c in ['goso-map-end','tm-end-nav','am-end-nav','dm-end-nav','gm-end-nav']):remove(root,x)
    prev=(f'#ch02-s0{n-1}',f'2.{n-1} {TOPICS[n-2][1]}') if n>1 else (f'/2026/{lang}/chapters/01/#ch01-s03','1.3 方法基础')
    nex=(f'#ch02-s0{n+1}',f'2.{n+1} {TOPICS[n][1]}') if n<7 else (f'/2026/{lang}/chapters/03/','第三章 GOSR')
    root.children+=fragment(f'<nav class="goso-section-nav" aria-label="2.{n} 前后节导航"><a href="{prev[0]}">← {prev[1]}</a><a href="#goso-intro">本章总览</a><a href="#goso-review">评审与待补</a><a href="{nex[0]}">{nex[1]} →</a></nav>')
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
