"""Chapter 1 reading bridge: authored goal links, never quantitative weights."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
PILLARS=[('X1','人才规模与多样性','Talent & diversity','谁能参与，怎样持续成长？','Who participates and grows?'),('X2','技术产出与开放供给','Technology & open supply','有哪些可用、可复用的成果？','What can be used and reused?'),('X3','全球连接与网络效应','Connections & network effects','贡献与成果怎样连接起来？','How do contributions connect?'),('X4','开源善治与公共价值','Governance & public value','协作如何持续，价值如何实现？','How can collaboration endure?')]
MAPS=[
 ('V','活跃','Activity',['X1'],'参与规模 · 地域分布 · 变化趋势','Participation · Geography · Trends','从全球和中国的活跃开发者分布出发，看见开放协作的参与基础。','Start with active developers across the world and China to understand the participation base.'),
 ('C','贡献','Contribution',['X2'],'贡献来源 · 贡献强度 · 协作联系','Sources · Intensity · Collaboration','从贡献来自哪里、如何形成联系，理解参与怎样转化为共同创造。','Explore where contributions originate and how participation connects to co-creation.'),
 ('I','项目影响力','Project influence',['X3'],'影响分布 · 项目结构 · 时间变化','Distribution · Structure · Change','观察项目在协作网络中的影响，比较不同地区的结构与变化。','Observe project influence in collaboration networks and compare regional patterns over time.'),
 ('T','人才','Talent',['X1','X3'],'人才聚集 · 成长轨迹 · 全球连接','Concentration · Growth · Connections','从高影响力人才的分布与成长，理解长期贡献如何积累。','Follow the distribution and growth of influential contributors to understand sustained contribution.'),
 ('A','资产','Assets',['X2'],'代码 · 模型 · 数据','Code · Models · Data','把代码、模型和数据放在一起，观察开放技术基础怎样积累与复用。','Observe how code, model and data assets accumulate and support further reuse.'),
 ('D','多样性','Diversity',['X1','X3'],'参与结构 · 跨域协作 · 开放连接','Participation · Cross-region collaboration','观察不同地区的参与结构及其协作联系，理解多样性与连接的关系。','Compare participation and cross-region collaboration to understand diversity and connectivity.'),
 ('G','治理与社会公益','Governance & public value',['X4'],'治理实践 · 开放条件 · 公共价值','Governance · Openness · Public value','从治理实践和开放条件出发，寻找持续协作与公共价值的可观察证据。','Explore governance and openness as evidence for sustained collaboration and public value.')]
COLORS=['#087984','#2d5f9f','#76508b','#407a51']
def dataset(lang):
 zh=lang=='zh';manifest=json.loads((ROOT/'content/manifest.json').read_text())
 pillars=[dict(id=p[0],title=p[1 if zh else 2],question=p[3 if zh else 4]) for p in PILLARS]
 maps=[]
 for i,m in enumerate(MAPS):
  sec=manifest['chapters'][1]['sections'][i]
  maps.append(dict(id=m[0],title=m[1 if zh else 2],pillars=m[3],signals=m[4 if zh else 5],description=m[6 if zh else 7],question=sec['question'][lang],number=sec['number'],href='/2026/'+lang+'/chapters/02/#'+sec['id']))
 return dict(pillars=pillars,maps=maps)
def curves():
 for j,m in enumerate(MAPS):
  for p in m[3]:
   i=int(p[1])-1;y1=248+i*110;y2=199+j*72
   yield p,m[0],f'M288 {y1} C370 {y1},386 {y2},468 {y2}'
def render(lang):
 t=lambda z,e:z if lang=='zh' else e;d=dataset(lang)
 out='<figure class="chapter-explorer theme-map-explorer foundation-figure" id="fig-theme-maps" data-lang="'+lang+'" data-reading-number="图 1-3-2" data-reading-title="'+t('七个主题地图','Seven thematic maps')+'" data-slide-key="themes"><div class="explorer-heading"><div><span class="eyebrow">GOSO / SEVEN THEMATIC MAPS</span><h3>'+t('从发展目标，走进七个主题地图','From development goals to seven thematic maps')+'</h3><p>'+t('选择支柱或地图，沿着连线找到你的阅读入口。','Select a pillar or map to follow a reading path.')+'</p></div></div><div class="theme-map-controls"><button type="button" data-theme-reset>'+t('全部关联','All links')+'</button><button type="button" data-theme-motion aria-pressed="false">'+t('流动连线','Animate links')+'</button></div><div class="theme-map-label label-goals">'+t('发展目标 · OSDGs','DEVELOPMENT GOALS')+'</div><div class="theme-map-label label-maps">'+t('观察问题 · GOSO','OBSERVATION THEMES')+'</div><div class="theme-map-label label-read">'+t('从这里开始阅读','YOUR READING PATH')+'</div><svg class="theme-map-edges" viewBox="0 0 1280 800" aria-hidden="true">'
 for p,m,path in curves():out+='<path d="'+path+'" data-theme-edge="'+p+':'+m+'" class="theme-map-edge" style="--edge-color:var(--p'+p[1]+')"/>'
 out+='</svg><div class="theme-map-pillars">'
 for p in d['pillars']:out+='<button type="button" data-theme-pillar="'+p['id']+'" aria-pressed="false" aria-controls="theme-map-detail" style="--node-color:var(--p'+p['id'][1]+')"><small>'+p['id']+'</small><strong>'+E(p['title'])+'</strong><span>'+E(p['question'])+'</span></button>'
 out+='</div><div class="theme-map-nodes">'
 for m in d['maps']:out+='<button type="button" data-theme-node="'+m['id']+'" aria-pressed="false" aria-controls="theme-map-detail"><b>'+m['id']+'</b><span><strong>'+E(m['title'])+'</strong><small>'+E(m['signals'])+'</small></span><em>'+m['number']+'</em></button>'
 out+='</div><aside id="theme-map-detail" class="theme-map-detail" aria-live="polite"><small>'+t('七个角度 · 一幅生态全貌','SEVEN PERSPECTIVES · ONE ECOSYSTEM')+'</small><h4>'+t('先看参与，再看创造与价值','Participation, creation and value')+'</h4><p>'+t('七个主题相互补充：从谁在参与，看到贡献与影响，再进入人才、资产、多样性和治理。','The seven themes connect participation with contribution and influence, then talent, assets, diversity and governance.')+'</p><div class="theme-map-overview"><span>'+t('选择左侧支柱','Choose a pillar')+'</span><span>'+t('查看关联主题','Follow linked themes')+'</span><span>'+t('进入第二章对应小节','Open its Chapter 2 section')+'</span></div><a href="/2026/'+lang+'/chapters/02/">'+t('从第二章开始 →','Start Chapter 2 →')+'</a></aside><p class="theme-map-note">'+t('连线表示阅读与研究联系，不代表计算权重；一个主题可以回应多个发展目标。','Links show research and reading relationships, not weights; one theme can address several goals.')+'</p><figcaption>'+t('图 1-3-2 · 从共同目标到生态观察，连接持续共同创造及其公共价值。','Figure 1-3-2 · From shared goals to ecosystem observation, sustained co-creation and public value.')+'</figcaption><script type="application/json" id="theme-map-data">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script></figure>'
 return out

def static_svg():
 """Use the canonical publication view for every standalone export."""
 return (ROOT.parent/'figures/chapter1/print/fig-1-3-2_theme_maps.svg').read_text()

if __name__=='__main__':
 target=ROOT.parent/'figures/chapter1/fig-1-3-2_theme_maps.svg';target.write_text(static_svg());print(target)
