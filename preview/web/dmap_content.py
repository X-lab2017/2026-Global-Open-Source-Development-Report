"""D-Map web and print use the same publication manuscript."""
import html,shutil
from dmap_publication import *
E=lambda s:html.escape(str(s),quote=True)
def prose(ps,insight=False):
 def one(t):
  if not insight:return '<p>'+E(t)+'</p>'
  a,b=t.split('。',1);return '<p><strong>'+E(a+'。')+'</strong>'+E(b)+'</p>'
 return ''.join(map(one,ps))
def figure(key):
 f=FIGURES[key];tabs={'breadth':[('map','全球分布'),('trend','五年变化')],'sources':[],'network':[('sankey','贡献路径'),('chord','连接网络'),('map','协作地图')]}[key]
 controls='<div class="dm-tabs" role="group" aria-label="观察视角">'+''.join(f'<button data-dm-tab="{key}:{v}" aria-pressed="{str(i==0).lower()}">{t}</button>' for i,(v,t) in enumerate(tabs))+'</div>' if tabs else '<span>本土、已列跨境与未列来源</span>'
 return f'''<figure id="fig-{f['id']}" class="chapter-one-visual dm-figure" data-slide-key="dmap-{f['id'][-1]}" data-slide-height="860" data-reflow-minimum-width="700" data-lang="zh" aria-labelledby="dm-{key}-title"><header class="viz-heading"><span class="eyebrow">图 {f['id']} / D-MAP</span><h4 id="dm-{key}-title">{f['title']}</h4></header><div class="dm-toolbar">{controls}<span class="dm-context" id="dm-{key}-context"></span></div><div class="dm-panel" id="dm-{key}"></div><figcaption><span id="dm-{key}-foot">{f['note']}</span><button data-dm-source="{key}">口径与来源</button></figcaption><div class="dm-source-overlay" data-dm-overlay="{key}" hidden></div><noscript><img src="/assets/dmap/print/{f['file']}" alt="{f['title']}"></noscript></figure><div class="dm-print-view"><img src="/assets/dmap/print/{f['file']}" alt="图 {f['id']} {f['title']}"></div>'''
def section(lang='zh'):
 out=[f'<section id="ch02-s06" class="chapter-section goso-section dmap-review"><div class="section-topline">2.6 / D-MAP</div><h2>{TITLE}</h2><p class="dm-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="goso-map-position"><strong>目标与指标定位</strong><p>{POSITION}</p><a href="/2026/{lang}/data/indicators/#indicator-GlobalCollabShare">跨地域协作指标</a></div><h3>核心发现</h3><p class="dm-core-finding">{FINDING}</p><p class="goso-map-window">{WINDOW}</p><nav class="dm-reading-route" aria-label="D-Map 阅读路径">']
 for key,label in [('breadth','全球来源'),('sources','中美对照'),('network','贡献连接'),('actions','行动建议')]:out.append(f'<a href="#dm-story-{key}">{label}</a>')
 out.append(f'<a class="dm-download" href="/assets/dmap/print/{PDF_RELEASE_NAME}" download="{PDF_RELEASE_NAME}">下载本节 PDF ↓</a></nav>')
 for (title,ps),key in zip(STORIES,FIGURES):out.extend([f'<div class="goso-prose dm-story" id="dm-story-{key}"><h3>{title}</h3>'+prose(ps[:1])+'</div>',figure(key),'<div class="goso-prose dm-interpretation">'+prose(ps[1:],True)+'</div>'])
 out.append('<div class="dm-actions" id="dm-story-actions"><h3>'+ACTION_TITLE+'</h3><p>'+ACTION_INTRO+'</p>')
 for i,(title,ps) in enumerate(STRATEGIES,1):out.append(f'<article><span>0{i}</span><h4>{title}</h4>'+prose(ps)+'</article>')
 out.append('</div><details class="goso-gap"><summary>统计范围与指标说明</summary>'+prose(NOTES)+'<p><a href="/assets/dmap/source-manifest.json" download>数据来源清单</a></p></details><div class="dm-print-evidence">'+prose(NOTES)+'</div><p class="goso-bridge">'+BRIDGE+'</p></section>')
 return ''.join(out)
def export(out):
 (BASE/'chapter-2-6.md').write_text(manuscript())
 shutil.copytree(BASE,out/'assets/dmap',dirs_exist_ok=True)
 shutil.copy2(BASE/'print'/PDF_NAME,out/'assets/dmap/print'/PDF_RELEASE_NAME)
 shutil.copy2(BASE/'print'/PDF_NAME,out/'assets/dmap/print/GOSD-2026-section-2-6-20261020.pdf')
 for f in ['dmap.js','dmap.css','dmap-publication.css']:shutil.copy2(ROOT/'web'/f,out/f)
