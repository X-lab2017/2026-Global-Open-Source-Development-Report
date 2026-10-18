"""Homepage: an illustrative open ecosystem, OpenDigger data core, and report framework."""
import html,json,math,random
from pathlib import Path

def render(lang):
    zh=lang=='zh'; e=html.escape; t=lambda z,en:z if zh else en
    f=json.loads((Path(__file__).resolve().parents[1]/'content/assets/framework.json').read_text())
    entities=[
        ('代码','Code','开放仓库中的代码与协作记录，留下持续开发和共同维护的足迹。','Open repositories record ongoing development, collaboration and shared maintenance.'),
        ('模型','Models','开放模型连接训练成果、复用和衍生，扩展下一次创造的起点。','Open models connect released capabilities with reuse and derivatives.'),
        ('数据集','Datasets','可获取、可理解的数据，为研究、训练与验证提供基础。','Accessible, understandable datasets support research, training and validation.'),
        ('开发者','Developers','开发者贡献知识与经验，在跨项目协作中连接整个生态。','Developers connect the ecosystem through their knowledge and collaboration.'),
        ('工具','Tools','开发、评测与运行工具，帮助开放成果更容易被使用和维护。','Development, evaluation and runtime tools make open work easier to use and maintain.'),
        ('Agent','Agents','Agent 将模型、工具与任务连接起来，形成新的应用与协作方式。','Agents connect models, tools and tasks into new applications and ways of working.')]
    labels={}; eco=[]; report=[]
    for i,(z,en,dz,de) in enumerate(entities):
        key=f'e{i}';labels[key]={'title':t(z,en),'description':t(dz,de),'detail':t('开源生态对象','Open ecosystem object'),'group':'eco','index':i}
        eco.append(f'<button type="button" class="star-node-label eco-label eco-label-{i}" data-key="{key}" aria-pressed="false" tabindex="-1"><span>{t(z,en)}</span></button>')
    descriptions=['让更多人参与，让不同的经验进入共同创造。','让代码、模型与数据成为可以继续使用的成果。','让成果在协作与复用中，连接更多创造者。','让开放协作持续运行，并回应共同的社会需要。'] if zh else ['More people and diverse experiences contribute to shared creation.','Code, models and data become foundations others can build upon.','Collaboration and reuse connect contributions to new creators.','Sustained collaboration responds to shared societal needs.']
    for i,p in enumerate(f['P']):
        key=f'r{i}';labels[key]={'title':p[1 if zh else 2],'description':descriptions[i],'detail':' · '.join(d[1 if zh else 2] for d in f['D'] if d[4]==i),'group':'pillar','index':i,'href':f'/2026/{lang}/chapters/01/'}
        short=(['人才','供给','连接','价值'] if zh else ['Talent','Supply','Connection','Public value'])[i]
        report.append(f'<button type="button" class="star-node-label report-label report-label-{i} pillar-label" data-key="{key}" style="--label-color:var(--star-{i})" aria-pressed="false" tabindex="-1"><span class="star-dot"></span><span>X{i+1} {short}</span></button>')
    chapters=[('GOSO','开源发展地图','Open source maps','从地域与协作网络，观察参与、贡献与影响力的分布。','Explore participation, contribution and influence across places and networks.'),('GOSR','开源发展榜单','Open source rankings','以可比指标，观察不同主体的位置与变化。','Compare the positions and trajectories of ecosystem participants.'),('GOSL','技术领域全景','Technology landscapes','沿技术分类，观察项目、子领域与开放生态的演进。','Explore projects, subfields and the evolution of open technology.'),('GOSM','开放模型生态','Open model ecosystems','观察模型供给、复用衍生与开源开放程度。','Explore model supply, reuse, derivatives and degrees of openness.')]
    for i,(code,z,en,dz,de) in enumerate(chapters):
        key=f'r{i+4}';labels[key]={'title':code+' · '+t(z,en),'description':t(dz,de),'detail':t(f'第 {i+2} 章 · 研究视角',f'Chapter {i+2} · Research lens'),'group':'chapter','index':i,'href':f'/2026/{lang}/chapters/{i+2:02}/'}
        report.append(f'<button type="button" class="star-node-label report-label report-label-{i+4} chapter-label" data-key="{key}" aria-pressed="false" tabindex="-1"><span>{code}</span></button>')
    rng=random.Random(2026);groups=[]
    for i in range(6):
        nodes=[];lines=[]
        for j in range(13):
            a=math.radians(-90+i*60+rng.uniform(4,56));r=rng.uniform(90,225);x=250+math.cos(a)*r;y=250+math.sin(a)*r
            px,py=min(nodes,key=lambda p:(p[0]-x)**2+(p[1]-y)**2) if nodes else (250+math.cos(a)*70,250+math.sin(a)*70)
            nodes.append((x,y));lines.append(f'<path d="M {px:.1f} {py:.1f} L {x:.1f} {y:.1f}"/>')
        groups.append(f'<g class="star-cluster" data-cluster="{i}">'+''.join(lines)+''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2"/>' for x,y in nodes)+'</g>')
    flows=[];vertical=[]
    for i in range(14):
        y=112+i*16;end=170+i*9;d=f'M {220+i%3*10} {y} C 340 {y-35} 405 {end+35} 555 {end}'
        v=f'M {250+(i-7)*9} 330 C {160+i*12} 440 {340-i*8} 490 {250+(i-7)*7} 600'
        for target,path in [(flows,d),(vertical,v)]: target.append(f'<path d="{path}"/><path class="star-bridge-pulse" style="--flow-delay:-{i*.63}s;--flow-duration:{6+i%5}s" d="{path}"/>')
    return f'''<section class="cocreation" aria-label="{t('共创星图','Co-creation constellation')}" data-lang="{lang}" data-labels="{e(json.dumps(labels,ensure_ascii=False),quote=True)}">
      <div class="star-heading"><span>OPEN ECOSYSTEM → GOSD</span><button type="button" class="star-motion" aria-pressed="false">{t('暂停动态','Pause motion')}</button></div>
      <div class="star-scene"><svg class="star-bridge" viewBox="0 0 700 460" preserveAspectRatio="none" aria-hidden="true">{''.join(flows)}</svg><svg class="star-bridge-mobile" viewBox="0 0 500 900" preserveAspectRatio="none" aria-hidden="true">{''.join(vertical)}</svg>
       <div class="star-side star-ecosystem"><div class="star-stage"><canvas class="star-cosmos" tabindex="0" role="button" aria-expanded="false" aria-controls="star-eco-labels" aria-label="{t('共创星云；点击探索生态对象，拖动或使用方向键旋转','Co-creation galaxy; activate to explore ecosystem objects, drag or use arrow keys to rotate')}"></canvas><svg class="star-network" viewBox="0 0 500 500" aria-hidden="true">{''.join(groups)}</svg>
        <button type="button" class="star-core" aria-expanded="false" aria-controls="star-eco-labels" aria-label="{t('OpenDigger 数据内核，展开生态对象','OpenDigger data core; explore ecosystem objects')}"><img src="/assets/opendigger-core.png" width="320" height="320" alt=""><strong>OpenDigger</strong></button>
        <canvas class="star-cosmos-front" aria-hidden="true"></canvas><div class="star-labels star-eco-labels" id="star-eco-labels" aria-hidden="true">{''.join(eco)}</div></div>
        <button type="button" class="star-explore" data-expand="eco" aria-expanded="false" aria-controls="star-eco-labels">{t('探索生态对象','Explore the ecosystem')} <span aria-hidden="true">＋</span></button></div>
       <div class="star-side star-report-side"><div class="star-report"><div class="star-book-float"><button type="button" class="star-book" aria-expanded="false" aria-controls="star-report-labels" aria-label="{t('展开报告的四支柱与四个研究章节','Explore the report’s four pillars and four research chapters')}"><span class="star-book-face"><span class="star-book-top">GOSD <small>2026</small></span><span class="star-book-title">{t('全球开源<br>发展报告','Global Open Source<br>Development Report')}</span><span class="star-book-english">GLOBAL OPEN SOURCE<br>DEVELOPMENT REPORT</span><span class="star-book-disc"><img src="/assets/cocreation-disc-dark.svg" alt="OSDG" width="252" height="252"></span><span class="star-book-line"></span><span class="star-book-bottom">INCLUSION · QUALITY<br>PARTICIPATION · IMPACT</span></span><span class="star-book-spine">GOSD · 2026</span></button></div>
        <div class="star-labels star-report-labels" id="star-report-labels" aria-hidden="true">{''.join(report)}</div></div>
        <button type="button" class="star-explore" data-expand="report" aria-expanded="false" aria-controls="star-report-labels">{t('探索报告结构','Explore the report')} <span aria-hidden="true">＋</span></button></div></div>
      <div class="star-popover" id="star-popover" role="region" aria-label="{t('标签说明','About this label')}" hidden><div class="star-popover-heading"><strong></strong><button type="button" class="star-popover-close" aria-label="{t('关闭说明','Close explanation')}">×</button></div><p></p><small></small><a href="/2026/{lang}/chapters/01/" hidden>{t('进入阅读','Read more')} ↗</a></div>
      <div class="star-detail"><h2>{t('开放，共同创造','Open. Create. Together.')}</h2><p>{t('从开放生态的数据，到理解发展的证据。','From open ecosystem data to evidence that informs development.')}</p></div>
      <div class="star-footer"><span>{t('拖动旋转 · 点击展开 · 悬停了解','Drag to rotate · Click to explore · Hover to learn')}</span><span>{t('生态与数据流为示意','Illustrative ecosystem and data flows')}</span></div>
    </section>'''
