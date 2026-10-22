"""Chapter 6: one shared source for the manuscript, action diagrams and print figures."""
from pathlib import Path
import html,json,shutil,math
ROOT=Path(__file__).resolve().parents[1]
PDF_NAME='GOSD-2026-chapter6.pdf'
PDF_URL='/assets/action/'+PDF_NAME
E=lambda x:html.escape(str(x),quote=True)
FILES={'overview':'fig-6-1-1_evidence_to_action','public':'fig-6-2-1_public_support','enterprise':'fig-6-3-1_organization_responsibility','community':'fig-6-4-1_global_cocreation','cycle':'fig-6-5-1_sustained_cocreation'}

def data():return json.loads((ROOT/'content/action/chapter6.json').read_text())
def tr(value,lang):return value[lang] if isinstance(value,dict) else value
def local_link(item,lang):return '<a href="/2026/'+lang+'/'+E(item['url'])+'">'+E(tr(item['label'],lang))+' ↗</a>'
def paras(values,lang):return ''.join('<p>'+E(tr(v,lang))+'</p>' for v in values)
FIG_TITLES={
 'overview': {'zh':'证据、共同任务与主体责任','en':'Evidence, shared tasks and responsibilities'},
 'public':{'zh':'公共支持的三条行动路径','en':'Three pathways for public support'},
 'enterprise':{'zh':'企业与组织的协作责任','en':'Collaboration responsibilities of organizations'},
 'community':{'zh':'社区与全球伙伴的共同建设','en':'Co-creation by communities and global partners'},
 'cycle':{'zh':'持续共同创造与行动反馈','en':'Sustained co-creation and feedback'}
}
FIG_NUMBERS=dict(zip(FILES,['6-1-1','6-2-1','6-3-1','6-4-1','6-5-1']))
def fig_start(key,number,title,sub,lang):
 return '<div class="action-figure-wrap"><figure id="'+FILES[key].split('_')[0]+'" class="chapter-explorer action-canvas ac-'+key+'" data-lang="'+lang+'" data-action-figure="'+key+'" data-slide-key="action-'+key+'"><div class="ac-heading"><span class="ac-kicker">'+('研究综合 · 行动路径' if lang=='zh' else 'RESEARCH SYNTHESIS · ACTION PATHWAYS')+'</span><h3>'+E(tr(FIG_TITLES[key],lang))+'</h3><p>'+E(sub)+'</p></div>'
def fig_end(key,lang):
 title=('图 ' if lang=='zh' else 'Figure ')+FIG_NUMBERS[key]+' '+tr(FIG_TITLES[key],lang)
 note='研究与行动关系示意；连线不表示数量、权重或已验证的因果关系。' if lang=='zh' else 'Proposed relationships; lines do not encode quantities, weights or established causal effects.'
 url='/assets/action/'+FILES[key]+('' if lang=='zh' else '-en')+'.svg'
 return '<figcaption><strong>'+E(title)+'</strong><span data-ac-caption-note>'+note+'</span></figcaption></figure><img class="action-print" src="'+url+'" alt="'+E(title)+'"><a class="action-figure-download" href="'+url+'" download>'+('下载完整静态图 SVG ↓' if lang=='zh' else 'Download complete static SVG ↓')+'</a></div>'
def edges(key,paths):
 s='<svg class="ac-edges" viewBox="0 0 1280 800" aria-hidden="true"><defs><marker id="ac-arrow-'+key+'" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8" fill="var(--brand)"/></marker></defs>'
 for f,t,d in paths:s+='<path class="ac-edge" data-from="'+f+'" data-to="'+t+'" d="'+d+'" '+('marker-mid' if key=='cycle' else 'marker-end')+'="url(#ac-arrow-'+key+')"/>'
 return s+'</svg>'
def overview(lang,D):
 t=lambda z,e:z if lang=='zh' else e
 s=fig_start('overview','图 6-1-1' if lang=='zh' else 'FIGURE 6-1-1',t('把四章观察，连接到三项共同任务','Connect four perspectives to three shared tasks'),t('选择观察、任务或主体，在同一图中查看联系与具体建议。','Select evidence, a task or an actor to explore connections and recommendations here.'),lang)
 paths=[]
 for i,e in enumerate(D['evidence']):
  for task in e['tasks']:
   j=next(j for j,x in enumerate(D['tasks']) if x['id']==task);y=205+i*98;z=229+j*150
   paths.append((e['id'],task,f'M312 {y}C390 {y} 410 {z} 488 {z}'))
 for i,task in enumerate(D['tasks']):
  for j,a in enumerate(D['actors']):
   y=229+i*150;z=229+j*150;paths.append((task['id'],a['id'],f'M788 {y}C862 {y} 894 {z} 968 {z}'))
 s+=edges('overview',paths)
 for x,text in [(28,t('前文的四类观察','FOUR RESEARCH PERSPECTIVES')),(488,t('三项共同任务','THREE SHARED TASKS')),(968,t('三个主体 · 九条建议','THREE ACTORS · NINE ACTIONS'))]:s+='<div class="ac-column-label" style="left:'+str(x)+'px">'+text+'</div>'
 for i,e in enumerate(D['evidence']):s+='<button type="button" class="ac-node ac-evidence" style="top:'+str(168+i*98)+'px" data-ac-evidence="'+e['id']+'" aria-pressed="false" aria-controls="ac-overview-detail"><small>'+e['code']+'</small><strong>'+E(tr(e['title'],lang).split('：')[-1].split(': ')[-1].replace(' and ',' & '))+'</strong></button>'
 for i,task in enumerate(D['tasks']):s+='<button type="button" class="ac-node ac-task" style="top:'+str(172+i*150)+'px" data-ac-task="'+task['id']+'" aria-pressed="false" aria-controls="ac-overview-detail"><small>'+t('共同任务 ','SHARED TASK ')+task['n']+' · '+task['pillars']+'</small><strong>'+E(tr(task['short'],lang))+'</strong></button>'
 for i,a in enumerate(D['actors']):s+='<button type="button" class="ac-node ac-actor" style="top:'+str(172+i*150)+'px" data-ac-actor="'+a['id']+'" aria-pressed="false" aria-controls="ac-overview-detail"><small>'+a['section']+' · '+t('三条建议','THREE RECOMMENDATIONS')+'</small><strong>'+E(tr(a['short'],lang))+'</strong><span>'+E(tr(a['role'],lang))+'</span></button>'
 s+='<div class="ac-overview-detail" id="ac-overview-detail" aria-live="polite"><div class="ac-detail-title"><small>'+t('从任务出发','START WITH A SHARED TASK')+'</small><h4>'+t('共同目标，需要分工与协作','Shared goals need shared responsibilities')+'</h4></div><div class="ac-detail-copy"><p>'+E(tr(D['tasks'][1]['body'],lang))+'</p><span>'+t('点击任一节点，查看相应的观察、任务或建议。','Select a node to inspect its evidence, task or recommendations.')+'</span></div></div>'
 return s+fig_end('overview',lang)
def actor_figure(actor,lang,D):
 t=lambda z,e:z if lang=='zh' else e;key=actor['id'];aa=[a for a in D['actions'] if a['actor']==key];a=aa[0]
 s=fig_start(key,('图 ' if lang=='zh' else 'FIGURE ')+actor['section'].replace('.','-')+'-1',tr(actor['diagram'],lang),t('选择一条建议，查看实施步骤、协作分工与后续观察。','Choose a recommendation to inspect its steps, responsibilities and follow-up observations.'),lang)
 s+='<div class="ac-action-tabs" role="group" aria-label="'+t('本节三条建议','Three recommendations')+'">'
 for x in aa:s+='<button type="button" data-ac-action="'+x['id']+'" aria-pressed="'+str(x is a).lower()+'" aria-controls="ac-'+key+'-plan"><b>'+x['number']+'</b><span>'+E(tr(x['short'],lang))+'</span></button>'
 s+='</div>'+edges(key,[('step-0','step-1','M376 342H466'),('step-1','step-2','M814 342H904')])+'<div class="ac-action-plan" id="ac-'+key+'-plan" aria-live="polite">'
 s+='<div class="ac-plan-label" data-ac-task-label>'+E(tr(next(v for v in D['tasks'] if v['id']==a['task'])['title'],lang))+'</div>'
 for i,step in enumerate(a['steps']):s+='<article class="ac-step" style="left:'+str(28+i*438)+'px"><h4 data-ac-step-title="'+str(i)+'">'+E(tr(step['title'],lang))+'</h4><p data-ac-step-body="'+str(i)+'">'+E(tr(step['body'],lang))+'</p></article>'
 s+='<div class="ac-roles-label">'+t('协作分工','SHARED RESPONSIBILITIES')+'</div><div class="ac-roles">'
 for i,role in enumerate(a['roles']):s+='<div><small data-ac-role-who="'+str(i)+'">'+E(tr(role['who'],lang))+'</small><strong data-ac-role-work="'+str(i)+'">'+E(tr(role['work'],lang))+'</strong></div>'
 s+='</div><div class="ac-watch-label">'+t('后续观察什么','WHAT TO OBSERVE NEXT')+'</div><div class="ac-watch">'
 for i,w in enumerate(a['watch']):s+='<div><b data-ac-watch-label="'+str(i)+'">'+E(tr(w['label'],lang))+'</b><p data-ac-watch-detail="'+str(i)+'">'+E(tr(w['detail'],lang))+'</p></div>'
 s+='</div></div>'
 return s+fig_end(key,lang)
# Six equally spaced angles on one ellipse; arrows sit midway between cards.
def cycle_point(angle):
 a=math.radians(angle);return (640+420*math.cos(a),390+210*math.sin(a))
def cycle_arc(i):
 points=[cycle_point(-90+i*60+delta) for delta in [0,30,60]]
 return 'M%.3f %.3fA420 210 0 0 1 %.3f %.3fA420 210 0 0 1 %.3f %.3f'%tuple(v for p in points for v in p)
CYCLE_POS=[(round(x-120,3),round(y-42,3)) for x,y in [cycle_point(-90+i*60) for i in range(6)]]
CYCLE_EDGES=[cycle_arc(i) for i in range(6)]
def cycle(lang,D):
 t=lambda z,e:z if lang=='zh' else e
 s=fig_start('cycle','图 6-5-1' if lang=='zh' else 'FIGURE 6-5-1',t('让一次创造，连接下一次创造','Connect one act of creation to the next'),t('选择环节，观察参与、成果、使用与支持怎样相互衔接。','Select a stage to explore how participation, assets, use and support connect.'),lang)
 s+=edges('cycle',[(v['id'],D['cycle'][(i+1)%6]['id'],CYCLE_EDGES[i]) for i,v in enumerate(D['cycle'])])
 s+='<svg class="ac-edges ac-cycle-flow" viewBox="0 0 1280 800" aria-hidden="true"><path class="ac-cycle-pulse" pathLength="100" d="M640 180A420 210 0 1 1 640 600A420 210 0 1 1 640 180"/></svg>'
 s+='<button type="button" class="ac-cycle-motion" data-ac-cycle-motion aria-pressed="false">'+t('继续流动','Resume flow')+'</button>'
 s+='<div class="ac-cycle-center"><span>CO-CREATION</span><h4>'+t('持续共同创造<br>及其公共价值','Sustained co-creation<br>and its public value')+'</h4><p>'+t('维护让成果延续，反馈让行动改进。','Maintenance sustains assets.<br>Feedback improves action.')+'</p></div>'
 for i,v in enumerate(D['cycle']):
  x,y=CYCLE_POS[i];s+='<button type="button" class="ac-node ac-cycle-node" style="left:'+str(x)+'px;top:'+str(y)+'px" data-ac-cycle="'+v['id']+'" aria-pressed="false" aria-controls="ac-cycle-detail"><strong>'+E(tr(v['title'],lang))+'</strong><span>'+E(tr(v['subtitle'],lang))+'</span></button>'
 s+='<div class="ac-cycle-detail" id="ac-cycle-detail" aria-live="polite"><h4>'+t('共同承担，持续检验','Share responsibility,<br>examine progress')+'</h4><p>'+t('让更多人持续参与，让开放成果得到维护和复用，再以真实使用与结果改进下一轮支持。','Enable continued participation, maintain and reuse open assets, and use actual experience and outcomes to improve the next round of support.')+'</p></div>'
 return s+fig_end('cycle',lang)
def chapter(lang):
 D=data();t=lambda z,e:z if lang=='zh' else e
 s='<article class="action-chapter" data-action-version="'+D['version']+'"><header class="action-opening"><span class="section-topline">CHAPTER 06 / FROM EVIDENCE TO ACTION</span><h2>'+E(tr(D['headline'],lang))+'</h2>'+paras([D['intro'],D['position']],lang)+'<p class="action-scope">'+E(tr(D['scope'],lang))+'</p><a class="action-pdf-link" href="'+PDF_URL+'" download>'+t('下载第六章 PDF · 11 页 ↓','Download Chapter 6 PDF · Chinese, 11 pages ↓')+'</a></header>'
 sy=D['synthesis'];s+='<section class="action-section" id="ch06-s01"><span class="section-topline">6.1 / INSIGHTS & SHARED TASKS</span><h2>6.1 '+E(tr(sy['title'],lang))+'</h2><p class="action-question">'+E(tr(sy['question'],lang))+'</p>'+paras(sy['paragraphs'],lang)
 for f in sy['findings']:s+='<div class="action-finding"><h3>'+E(tr(f['title'],lang))+'</h3>'+paras(f['paragraphs'],lang)+'</div>'
 s+='<h3 class="action-task-heading">'+E(tr(sy['task_title'],lang))+'</h3>'+paras([sy['figure_lead']],lang)+overview(lang,D)+'<div class="action-task-cards">'
 for task in D['tasks']:s+='<article><small>'+task['n']+' / '+task['pillars']+'</small><h3>'+E(tr(task['title'],lang))+'</h3><p>'+E(tr(task['body'],lang))+'</p></article>'
 s+='</div>'+paras([sy['after']],lang)+'</section>'
 for i,actor in enumerate(D['actors'],2):
  aa=[a for a in D['actions'] if a['actor']==actor['id']];s+='<section class="action-section" id="ch06-s0'+str(i)+'"><span class="section-topline">'+actor['section']+' / '+actor['id'].upper()+'</span><h2>'+actor['section']+' '+t('面向','For ')+E(tr(actor['title'],lang))+t('的倡议' if actor['id']=='community' else '的建议','')+'</h2>'+paras([actor['intro']],lang)+actor_figure(actor,lang,D)+'<div class="action-proposals">'
  for j,a in enumerate(aa,1):
   s+='<article class="action-proposal" id="action-'+a['id']+'" data-action-article="'+a['id']+'"><span class="action-proposal-number">'+a['number']+'</span><div><h3>'+actor['section']+'.'+str(j)+' '+E(tr(a['title'],lang))+'</h3>'+paras([a['why'],a['body']],lang)+'<div class="action-observe"><b>'+t('持续观察','Follow-up observation')+'</b><p>'+E(('；' if lang=='zh' else '; ').join(tr(w['label'],lang)+' — '+tr(w['detail'],lang) for w in a['watch']))+('。' if lang=='zh' else '.')+'</p></div></div></article>'
  s+='</div></section>'
 cl=D['closing'];s+='<section class="action-section action-closing" id="ch06-s05"><span class="section-topline">6.5 / SUSTAINED CO-CREATION</span><h2>6.5 '+E(tr(cl['title'],lang))+'</h2><p class="action-question">'+E(tr(cl['question'],lang))+'</p>'+paras(cl['paragraphs'][:1],lang)+cycle(lang,D)+paras(cl['paragraphs'][1:],lang)+'<div class="action-final"><p>'+E(tr(cl['final'],lang))+'</p><strong>'+E(tr(cl['invitation'],lang))+'</strong></div></section>'
 s+='<script type="application/json" id="chapter6-action-data">'+json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></article>'
 return s

def T(z,e):return {'zh':z,'en':e}
def link(label,url):return {'label':label,'url':url}
def manuscript(D,lang='zh'):
 L=lambda x:tr(x,lang);out=['# '+('第六章 ' if lang=='zh' else 'Chapter 6 · ')+L(D['title']),L(D['headline']),L(D['intro']),L(D['position']),L(D['scope'])]
 sy=D['synthesis'];out+=['## 6.1 '+L(sy['title']),L(sy['question']),*[L(x) for x in sy['paragraphs']]]
 for f in sy['findings']:out+=['### '+L(f['title']),*[L(x) for x in f['paragraphs']]]
 out+=['### '+L(sy['task_title']),L(sy['figure_lead']),f'![{L(FIG_TITLES["overview"])}](../../figures/chapter6/{FILES["overview"]}.svg)']
 for t in D['tasks']:out+=['#### '+t['n']+' '+L(t['title']),L(t['body'])]
 out+=[L(sy['after'])]
 for actor in D['actors']:
  out+=['## '+actor['section']+' '+('面向' if lang=='zh' else 'For ')+L(actor['title'])+(('的倡议' if actor['id']=='community' else '的建议') if lang=='zh' else ''),L(actor['intro']),f'![{L(FIG_TITLES[actor["id"]])}](../../figures/chapter6/{FILES[actor["id"]]}.svg)']
  for i,a in enumerate([a for a in D['actions'] if a['actor']==actor['id']],1):
   out+=['### '+actor['section']+'.'+str(i)+' '+L(a['title']),L(a['why']),L(a['body']),'**'+('持续观察' if lang=='zh' else 'Observe progress')+'：** '+'；'.join(L(w['label'])+'——'+L(w['detail']) for w in a['watch'])+'。']
 cl=D['closing'];out+=['## 6.5 '+L(cl['title']),L(cl['question']),L(cl['paragraphs'][0]),f'![{L(FIG_TITLES["cycle"])}](../../figures/chapter6/{FILES["cycle"]}.svg)',*[L(x) for x in cl['paragraphs'][1:]],L(cl['final']),'**'+L(cl['invitation'])+'**']
 return '\n\n'.join(out)+'\n'
def export(out):
 dest=out/'assets/action';shutil.copytree(ROOT/'content/action',dest,dirs_exist_ok=True)
 for f in ['chapter6.css','chapter6.js']:shutil.copy2(ROOT/'web'/f,out/f)
