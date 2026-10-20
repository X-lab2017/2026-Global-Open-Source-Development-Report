"""G-Map web / print from one manuscript."""
from gmap_publication import *
from html import escape as E
import shutil
def figure(i):
 key,en,title,tabs,context,caption=FIGURES[i-1]
 return f'''<figure id="fig-2-7-{i}" class="gm-figure"><div class="gm-stage chapter-one-visual goso-unified-canvas" data-lang="zh" data-slide-key="gmap-{i}" data-slide-height="860" data-reflow-minimum-width="700" role="group" aria-label="{title}"><div class="gm-board"><header class="gm-board-head"><div><span class="gm-eyebrow">图 2-7-{i} / {en}</span><h4>{title}</h4></div><button data-gm-source="{key}">口径与来源</button></header><div class="gm-toolbar"><div class="gm-tabs" aria-label="{title}视图">{''.join(f'<button data-gm-tab="{key}:{v}" aria-pressed="{str(j==0).lower()}">{label}</button>' for j,(v,label) in enumerate(tabs))}</div><span class="gm-context">{context}</span></div><div id="gm-{key}" class="gm-panel" aria-live="polite"></div><footer class="gm-board-foot"><span id="gm-{key}-foot"></span><a href="/assets/gmap/source-manifest.json" download>来源清单 ↓</a></footer><div class="gm-source-overlay" data-gm-overlay="{key}" role="region" aria-label="口径与来源" hidden></div></div></div><figcaption>图 2-7-{i} {title}</figcaption></figure>'''

def section(lang='zh'):
 out=[f'<section id="ch02-s07" class="chapter-section goso-section gmap-review"><div class="section-topline">2.7 / G-MAP</div><h2>{TITLE}</h2><p class="gm-prose">{INTRO}</p><p class="goso-question">{QUESTION}</p><div class="goso-map-position"><strong>目标与指标定位</strong><p>{POSITION}</p></div><h3>核心发现</h3><p class="gm-prose">{FINDING}</p><p class="gm-window">{WINDOW}</p><nav class="am-reading-route" aria-label="本节阅读路径">']
 for i,f in enumerate(FIGURES,1):out.append(f'<a href="#fig-2-7-{i}">{f[2]}</a>')
 out.append(f'<a href="/assets/gmap/print/{PDF_RELEASE_NAME}" download>下载本节 PDF ↓</a></nav>')
 for i,(title,ps) in enumerate(STORIES,1):
  a,b=ps[1].split('。',1)
  out.append(f'<section class="gm-section"><h3>{title}</h3><p class="gm-prose">{ps[0]}</p>'+figure(i)+f'<div class="gm-print-view"><img src="/assets/gmap/print/fig-2-7-{i}.svg" alt="图 2-7-{i} {FIGURES[i-1][2]}"></div>'+('<div class="gm-print-view"><img src="/assets/gmap/print/fig-2-7-2-continued.svg" alt="图 2-7-2 续图 治理实践与角色，模拟数据"></div>' if i==2 else '')+f'<p class="gm-prose"><strong>{a}。</strong>{b}</p></section>')
 out.append(f'<section class="gm-pub-actions"><h3>{ACTION_TITLE}</h3>')
 for i,(title,ps) in enumerate(STRATEGIES,1):out.append(f'<article><h4>{i} {title}</h4>'+''.join('<p class="gm-prose">'+t+'</p>' for t in ps)+'</article>')
 out.append('</section><details class="gm-methods"><summary>统计范围与指标说明</summary>'+''.join('<p>'+t+'</p>' for t in NOTES)+'</details><p class="gm-prose goso-bridge">'+BRIDGE+'</p></section>')
 return ''.join(out)
def export(out):
 (BASE/'chapter-2-7.md').write_text(manuscript())
 shutil.copytree(BASE,out/'assets/gmap',dirs_exist_ok=True)
 shutil.copy2(BASE/'print'/PDF_NAME,out/'assets/gmap/print'/PDF_RELEASE_NAME)
 for name in ['gmap.js','gmap.css']:shutil.copy2(ROOT/'web'/name,out/name)
