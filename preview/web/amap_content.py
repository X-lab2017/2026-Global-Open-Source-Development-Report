"""A-Map web and print use the same publication manuscript."""
import html,shutil,json
from amap_publication import *
E=lambda s:html.escape(str(s),quote=True)
def prose(ps,insight=False):
 def one(t):
  if not insight:return '<p>'+E(t)+'</p>'
  a,b=t.split('。',1);return '<p><strong>'+E(a+'。')+'</strong>'+E(b)+'</p>'
 return ''.join(map(one,ps))
def figure(key):
 f=FIGURES[key];tabs={'code':[('overview','平台规模'),('categories','类别结构与增长')],'models':[('map','地域供给'),('compare','数量与下载'),('categories','类别结构与增长')],'datasets':[('map','地域供给'),('compare','数量与下载'),('categories','类别结构与增长')]}[key]
 controls=('<div class="am-tabs" role="group" aria-label="观察视角">'+''.join(f'<button data-am-tab="{key}:{v}" aria-pressed="{str(i==0).lower()}">{t}</button>' for i,(v,t) in enumerate(tabs))+'</div>')
 context=('<label>报告年度 <select data-am-year>'+''.join(f'<option value="{y}"'+(' selected' if y==2026 else '')+f'>{y}</option>' for y in D['years'])+'</select></label>') if key=='code' else '发布单位累计样本'
 return f'''<figure id="fig-{f['id']}" class="chapter-one-visual am-figure" data-slide-key="amap-{f['id'][-1]}" data-slide-height="860" data-reflow-minimum-width="700" data-lang="zh" aria-labelledby="am-{key}-title"><header class="viz-heading"><span class="eyebrow">图 {f['id']} / A-MAP</span><h4 id="am-{key}-title">{f['title']}</h4></header><div class="am-toolbar">{controls}<span class="am-context" id="am-{key}-context">{context}</span></div><div class="am-panel" id="am-{key}"></div><figcaption><span id="am-{key}-foot">{f['note']}</span><button data-am-source="{key}">口径与来源</button></figcaption><div class="am-source-overlay" data-am-overlay="{key}" hidden></div><noscript><img src="/assets/amap/print/{f['file']}" alt="{f['title']}"></noscript></figure><div class="am-print-view"><img src="/assets/amap/print/{f['file']}" alt="图 {f['id']} {f['title']}"></div><div class="am-print-view"><img src="/assets/amap/print/fig-{f['id']}_categories.svg" alt="图 {f['id']}（续） 类别结构与增长 · 模拟数据"></div>'''
def section(lang='zh'):
 out=[f'<section id="ch02-s05" class="chapter-section goso-section amap-review"><div class="section-topline">2.5 / A-MAP</div><h2>{TITLE}</h2><p class="am-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="goso-map-position"><strong>目标与指标定位</strong><p>{POSITION}</p><a href="/2026/{lang}/data/indicators/#indicator-ActiveRepo">有效活跃仓库指标</a></div><h3>核心发现</h3><p class="am-core-finding">{FINDING}</p><p class="goso-map-window">{WINDOW}</p><nav class="am-reading-route" aria-label="A-Map 阅读路径">']
 for key,label in [('code','代码资产'),('models','模型资产'),('datasets','数据资产'),('actions','行动建议')]:out.append(f'<a href="#am-story-{key}">{label}</a>')
 out.append(f'<a class="am-download" href="/assets/amap/print/{PDF_RELEASE_NAME}" download="{PDF_RELEASE_NAME}">下载本节 PDF ↓</a></nav>')
 for (title,ps),key in zip(STORIES,FIGURES):out.extend([f'<div class="goso-prose am-story" id="am-story-{key}"><h3>{title}</h3>'+prose(ps[:1])+'</div>',figure(key),'<div class="goso-prose am-interpretation">'+prose(ps[1:],True)+'</div>'])
 out.append('<div class="am-actions" id="am-story-actions"><h3>'+ACTION_TITLE+'</h3><p>'+ACTION_INTRO+'</p>')
 for i,(title,ps) in enumerate(STRATEGIES,1):out.append(f'<article><span>0{i}</span><h4>{title}</h4>'+prose(ps)+'</article>')
 out.append('</div><details class="goso-gap"><summary>统计范围与指标说明</summary>'+prose(NOTES)+'<p><a href="/assets/amap/source-manifest.json" download>数据来源清单</a></p></details><div class="am-print-evidence">'+prose(NOTES)+'</div><p class="goso-bridge">'+BRIDGE+'</p></section>')
 return ''.join(out)
def export(out):
 (BASE/'chapter-2-5.md').write_text(manuscript())
 (BASE/'publication-data.js').write_text('window.AMAP_DATA='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';\n')
 shutil.copytree(BASE,out/'assets/amap',dirs_exist_ok=True)
 shutil.copy2(BASE/'print'/PDF_NAME,out/'assets/amap/print'/PDF_RELEASE_NAME)
 for f in ['amap.js','amap.css','amap-publication.css']:shutil.copy2(ROOT/'web'/f,out/f)
