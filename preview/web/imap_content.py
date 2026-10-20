"""I-Map editorial layout; all essential prose is shared with the print edition."""
import html,shutil
from imap_publication import *
E=lambda x:html.escape(str(x),quote=True)
def btn(key,value,label,selected=False):return f'<button type="button" data-im-{key}="{value}" aria-pressed="{str(selected).lower()}">{label}</button>'
def tabs(key,items):return '<div class="im-tabs" role="group" aria-label="观察视角">'+''.join(btn(key,v,t,i==0) for i,(v,t) in enumerate(items))+'</div>'
def pager(key):return f'<div class="im-pager"><button type="button" data-im-{key}-page="prev" aria-label="上一页">←</button><span data-im-{key}-page-status></span><button type="button" data-im-{key}-page="next" aria-label="下一页">→</button></div>'
def prose(ps,insight=False):
 out=[]
 for s in ps:
  if insight:
   a,b=s.split('。',1);out.append('<p><strong>'+E(a+'。')+'</strong>'+E(b)+'</p>')
  else:out.append('<p>'+E(s)+'</p>')
 return ''.join(out)
def frame(key,n,body):
 f=FIGURES[key]
 return f'<figure id="fig-2-3-{n}" class="chapter-one-visual imap-figure" data-slide-key="imap-{n}" data-slide-height="860" data-reflow-minimum-width="700" data-lang="zh" aria-labelledby="im-{key}-title"><header class="viz-heading"><span class="eyebrow">图 2-3-{n} / I-MAP</span><h4 id="im-{key}-title">{f["title"]}</h4></header>{body}<figcaption><span class="im-caption-note">{f["note"]}</span></figcaption><noscript><p>静态图保留完整主要信息。</p><img src="/assets/imap/print/{f["file"]}" alt="{f["title"]}"></noscript></figure><div class="im-print-view im-print-{f["orientation"]}"><img src="/assets/imap/print/{f["file"]}" alt="图 {f["id"]} {f["title"]}"></div>'
def world():
 body='<div class="im-module" data-im-world><div class="im-toolbar">'+tabs('world-view',[('map','全球全景'),('concept','理解影响力'),('aggregation','汇总路径')])+'<span class="im-meta">2025 自然年</span></div><div class="im-world-content" data-im-world-body></div></div>'
 return frame('world',1,body)
def comparison():
 body='<div class="im-module" data-im-comparison><div class="im-toolbar">'+tabs('compare-view',[('trend','五年趋势'),('contrast','贡献 × 影响力'),('index','累计增长（2022＝100）')])+'<span class="im-meta" data-im-compare-period>2026 报告年度</span></div><div class="im-comparison-body" data-im-compare-body></div><div class="im-years" data-im-years></div></div>'
 return frame('comparison',2,body)
def china():
 body='<div class="im-module" data-im-china><div class="im-toolbar">'+tabs('china-view',[('growth','增长与项目'),('sources','协作来源')])+'<span class="im-meta">2026 报告年度 · 项目样本</span></div><div class="im-china-body"><div class="im-china-main" data-im-china-body></div><aside class="im-projects"><h5>中国项目样本 <small>30 项</small></h5><input type="search" data-im-project-search aria-label="搜索项目或组织" placeholder="搜索项目或组织"><div data-im-project-list></div>'+pager('project')+'<div class="im-project-detail" data-im-project-detail role="status"></div></aside></div></div>'
 return frame('china',3,body)
def section(lang='zh'):
 out=[f'<section id="ch02-s03" class="chapter-section goso-section imap-review"><div class="section-topline">2.3 / I-MAP</div><h2>{TITLE}</h2><p class="im-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="goso-map-position"><strong>目标与指标定位</strong><p>{POSITION}</p></div><h3 id="im-findings">核心发现</h3><p class="im-core-finding">{FINDING}</p><p class="goso-map-window">{WINDOW}</p><nav class="im-reading-route" aria-label="I-Map 阅读路径">']
 for key,label in [('world','全球分布'),('comparison','五域比较'),('china','中国观察'),('actions','行动建议')]:out.append(f'<a href="#im-{key}">{label}</a>')
 out.append(f'<a href="/assets/imap/print/{PDF_NAME}" download class="im-download">下载本节 PDF ↓</a></nav>')
 for i,((title,ps),key) in enumerate(zip(STORIES,FIGURES)):
  out.append(f'<div class="goso-prose im-story" id="im-{key}"><span id="{key}" class="goso-anchor"></span><h3>{title}</h3>'+prose(ps[:FIGURE_AFTER[i]])+'</div>')
  out.append([world,comparison,china][i]())
  out.append(f'<div class="goso-prose im-interpretation" data-im-reading="{key}">'+prose(ps[FIGURE_AFTER[i]:],True)+'</div>')
 out.append('<div class="actions im-actions" id="im-actions"><span id="actions" class="goso-anchor"></span><h3>'+ACTION_TITLE+'</h3><p>'+ACTION_INTRO+'</p>')
 for i,(title,ps) in enumerate(STRATEGIES):out.append(f'<article><span>0{i+1}</span><div><h4>{title}</h4>'+prose(ps)+'</div></article>')
 out.append('</div><details class="goso-gap" id="im-evidence"><summary>统计范围与指标说明</summary>'+prose(NOTES)+'<p><a href="/assets/imap/influence.json" download>地图数据</a> · <a href="/assets/imap/fig-2-3-2_five_region_project_openrank_influence_trend.csv" download>五域序列</a> · <a href="/assets/imap/table-3-4-3_china_project_openrank_top30.csv" download>项目样本</a></p></details><div class="im-print-evidence">'+prose(NOTES)+'</div><p class="goso-bridge">'+BRIDGE+'</p></section>')
 return ''.join(out).replace('/2026/zh/','/2026/'+lang+'/')
def export(out):
 (BASE/'chapter-2-3.md').write_text(manuscript())
 shutil.copytree(BASE,out/'assets/imap',dirs_exist_ok=True,ignore=shutil.ignore_patterns('section.html'))
