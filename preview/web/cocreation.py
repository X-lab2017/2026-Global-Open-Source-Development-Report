"""Brand-faithful, illustrative homepage constellation. No statistical encoding."""
import html,json,math,random
from pathlib import Path

def render(lang):
    zh=lang=='zh'; esc=html.escape
    f=json.loads((Path(__file__).resolve().parents[1]/'content/assets/framework.json').read_text())
    names=['人才','供给','连接','公共价值'] if zh else ['Talent','Supply','Connection','Public value']
    descriptions=['让更多人参与，让不同的经验进入共同创造。','让代码、模型与数据成为可以继续使用的成果。','让成果在协作与复用中，连接更多创造者。','让开放协作持续运行，并回应共同的社会需要。'] if zh else ['More people and diverse experiences contribute to shared creation.','Code, models and data become foundations others can build upon.','Collaboration and reuse connect each contribution to new creators.','Sustained collaboration responds to shared societal needs.']
    groups=[]; rng=random.Random(2026)
    # Official clockwise order: X1 upper-right, X2 lower-right, X3 lower-left, X4 upper-left.
    for i in range(4):
        nodes=[]; lines=[]
        for j in range(16):
            angle=math.radians(-85+i*90+rng.uniform(5,75)); r=rng.uniform(130,224)
            x=300+math.cos(angle)*r*1.14; y=245+math.sin(angle)*r
            nodes.append((x,y))
            if j:
                px,py=min(nodes[:-1],key=lambda p:(p[0]-x)**2+(p[1]-y)**2)
            else:
                px,py=300+math.cos(angle)*112,245+math.sin(angle)*112
            d=f'M {px:.1f} {py:.1f} Q {(px+x)/2+12:.1f} {(py+y)/2-9:.1f} {x:.1f} {y:.1f}'
            lines.append(f'<path class="star-edge" d="{d}"/>')
            if j%4==0: lines.append(f'<path class="star-flow" style="--delay:-{j+i*2}s" d="{d}"/>')
        circles=''.join(f'<circle class="star-node" cx="{x:.1f}" cy="{y:.1f}" r="{3.1 if j%5==0 else 1.8}"/>' for j,(x,y) in enumerate(nodes))
        groups.append(f'<g class="star-cluster" data-cluster="{i}" style="--cluster:var(--star-{i});--arrive:{i*.16}s">'+''.join(lines)+circles+'</g>')
    buttons=[]; details=[]
    for i,p in enumerate(f['P']):
        dims=[d[1 if zh else 2] for d in f['D'] if d[4]==i]
        buttons.append(f'<button type="button" class="star-pillar star-pillar-{i}" data-pillar="{i}" aria-pressed="false" aria-controls="star-detail"><span class="star-dot"></span><span>{names[i]}</span><small>X{i+1}</small></button>')
        details.append({'title':p[1 if zh else 2],'description':descriptions[i],'dimensions':' · '.join(dims)})
    data=esc(json.dumps(details,ensure_ascii=False),quote=True)
    return f'''<section class="cocreation" aria-label="{'共创星图' if zh else 'Co-creation constellation'}" data-lang="{lang}" data-pillars="{data}">
      <div class="star-heading"><span>OSDG / CO-CREATION</span><button type="button" class="star-motion" aria-pressed="false">{'暂停动态' if zh else 'Pause motion'}</button></div>
      <div class="star-stage"><canvas class="star-cosmos" tabindex="0" role="img" aria-label="{'三维共创星云；拖动或使用方向键旋转' if zh else '3D co-creation galaxy; drag or use arrow keys to rotate'}"></canvas><svg class="star-network" viewBox="0 0 600 490" aria-hidden="true"><g class="star-orbits"><ellipse cx="300" cy="245" rx="260" ry="213"/><circle cx="300" cy="245" r="132"/><path d="M 40 245 H 560 M 300 25 V 465"/></g>{''.join(groups)}<circle class="star-core-halo" cx="300" cy="245" r="113"/></svg>
      <button type="button" class="star-book" aria-pressed="false" aria-label="{'展开报告封面' if zh else 'Explore report cover'}"><span class="star-book-face"><span class="star-book-top">GOSD <small>2026</small></span><span class="star-book-title">{'全球开源<br>发展报告' if zh else 'Global Open Source<br>Development Report'}</span><span class="star-book-english">GLOBAL OPEN SOURCE<br>DEVELOPMENT REPORT</span><span class="star-book-disc"><img src="/assets/cocreation-disc-dark.svg" alt="OSDG" width="252" height="252"></span><span class="star-book-line"></span><span class="star-book-bottom">INCLUSION · QUALITY<br>PARTICIPATION · IMPACT</span></span><span class="star-book-spine">GOSD · 2026</span></button>{''.join(buttons)}</div>
      <div class="star-detail" id="star-detail" aria-live="polite" aria-atomic="true"><h2>{'开放，共同创造' if zh else 'Open. Create. Together.'}</h2><p>{'一次开放，可以连接下一次创造。' if zh else 'Each open contribution connects to the next creation.'}</p><div class="star-dimensions">{'探索四个支柱，理解开放的公共价值。' if zh else 'Explore four pillars of open development.'}</div></div>
      <div class="star-footer"><span>{'拖动旋转 · 共创关系示意' if zh else 'Drag to rotate · Illustrative network'}</span><button type="button" class="star-reset" hidden>{'返回全景' if zh else 'Reset view'}</button><a href="/2026/{lang}/chapters/01/">{'理解目标与指标' if zh else 'Explore goals and indicators'} ↗</a></div>
    </section>'''
