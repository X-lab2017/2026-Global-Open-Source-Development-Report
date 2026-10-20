"""Publication shell around the existing T-Map interactions."""
import html,shutil
from tmap_publication import *
E=lambda v:html.escape(str(v),quote=True)
def prose(ps,insight=False):
 out=[]
 for t in ps:
  if insight:
   a,b=t.split('。',1);out.append('<p><strong>'+E(a+'。')+'</strong>'+E(b)+'</p>')
  else:out.append('<p>'+E(t)+'</p>')
 return ''.join(out)
def frame(key,n):
 f=FIGURES[key];modes={
 'world':('world',[('map','全球全景'),('concept','理解人才')]),
 'regions':('region-view',[('trend','五年趋势'),('growth','增长比较'),('position','规模 × 增速')]),
 'china':('china',[('map','城市全景'),('trend','十城变化'),('records','定位记录')]),
 'connect':('connect',[('flow','跨地域协作'),('transition','技术领域'),('ai','AI 贡献角色')])}
 attr,items=modes[key];buttons=''.join(f'<button type="button" data-tm-{attr}="{v}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(v,label) in enumerate(items))
 context={'world':'2026 年 7 月','regions':'','china':'十城样本','connect':'模拟数据｜待替换'}[key]
 control=('<label class="tm-year-label">报告年度 <select id="tm-region-year" aria-label="报告年度">'+''.join(f'<option value="{yr}"'+(' selected' if yr==2026 else '')+f'>{yr}</option>' for yr in D['years'])+'</select></label>') if key=='regions' else f'<span class="tm-context{ " tm-sim-badge" if n>3 else ""}"'+(' id="tm-world-context"' if key=='world' else '')+'>'+context+'</span>'
 info={'connect':'connections'}.get(key,key)
 return ('<span id="fig-2-4-5" class="goso-anchor" aria-hidden="true"></span>' if key=='connect' else '')+f'<figure id="fig-2-4-{n}" class="chapter-one-visual tmap-figure" data-slide-key="tmap-{n}" data-slide-height="860" data-reflow-minimum-width="700" data-lang="zh" aria-labelledby="tm-{key}-title"><header class="viz-heading"><span class="eyebrow">图 2-4-{n} / T-MAP</span><h4 id="tm-{key}-title">{f["title"]}</h4></header><div class="tm-toolbar"><div class="tm-tabs" role="group" aria-label="观察视角">{buttons}</div>{control}</div><div class="tm-panel" id="tm-{key}"></div><figcaption><span>{f["note"]}</span><button type="button" data-tm-info="{info}">口径与来源</button></figcaption><noscript><img src="/assets/tmap/print/{f["file"]}" alt="{f["title"]}"></noscript></figure><div class="tm-print-view"><img src="/assets/tmap/print/{f["file"]}" alt="图 {f["id"]} {f["title"]}"></div>'
def section(lang='zh'):
 out=[f'<section id="ch02-s04" class="chapter-section goso-section tmap-review"><div class="section-topline">2.4 / T-MAP</div><h2>{TITLE}</h2><p class="tm-introduction">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="goso-map-position"><strong>目标与指标定位</strong><p>{POSITION}</p><a href="/2026/{lang}/data/indicators/#indicator-HighImpactTalent">高影响力人才指标</a></div><h3 id="tm-findings">核心发现</h3><p class="tm-core-finding">{FINDING}</p><p class="goso-map-window">{WINDOW}</p><nav class="tm-reading-route" aria-label="T-Map 阅读路径">']
 for key,label in [('world','全球分布'),('regions','五域比较'),('china','中国城市'),('connect','协作连接'),('actions','行动建议')]:out.append(f'<a href="#tm-story-{key}">{label}</a>')
 out.append(f'<a href="/assets/tmap/print/{PDF_NAME}" download class="tm-download">下载本节 PDF ↓</a></nav>')
 for i,((title,ps),key) in enumerate(zip(STORIES,FIGURES),1):out.extend([f'<div class="goso-prose tm-story" id="tm-story-{key}"><h3>{title}</h3>'+prose(ps[:1])+'</div>',frame(key,i),'<div class="goso-prose tm-interpretation">'+prose(ps[1:],True)+'</div>'])
 out.append('<div class="tm-actions" id="tm-story-actions"><h3>'+ACTION_TITLE+'</h3><p>'+ACTION_INTRO+'</p>')
 for i,(title,ps) in enumerate(STRATEGIES,1):out.append(f'<article><span>0{i}</span><h4>{title}</h4>'+prose(ps)+'</article>')
 out.append('</div><details class="goso-gap"><summary>统计范围与指标说明</summary>'+prose(NOTES)+'<p><a href="/assets/tmap/observations.json" download>观测数据</a> · <a href="/assets/tmap/simulation.json" download>模拟参数</a></p></details><div class="tm-print-evidence">'+prose(NOTES)+'</div><p class="goso-bridge">'+BRIDGE+'</p><dialog id="tm-dialog" aria-labelledby="tm-dialog-title"><button type="button" id="tm-dialog-close" aria-label="关闭">×</button><h3 id="tm-dialog-title"></h3><div id="tm-dialog-body"></div></dialog><div id="tm-live" class="tm-sr" aria-live="polite"></div></section>')
 return ''.join(out)
def export(out):
 (BASE/'chapter-2-4.md').write_text(manuscript())
 shutil.copytree(BASE,out/'assets/tmap',dirs_exist_ok=True,ignore=shutil.ignore_patterns('section.html'))
