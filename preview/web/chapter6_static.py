"""Editable SVG companions generated from the same Chapter 6 action records."""
from pathlib import Path
import html,json,unicodedata
from chapter6_content import FILES,CYCLE_POS,CYCLE_EDGES,manuscript
E=lambda s:html.escape(str(s),quote=True)
INK='#18394c';MUTED='#587382';BRAND='#156993';LINE='#cadce5';PAPER='#f3f8fa';PALE='#e5f0f4'
class SVG:
 def __init__(self,title,kicker,subtitle):
  self.o=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800" role="img"><title>'+E(title)+'</title><rect width="1280" height="800" fill="'+PAPER+'"/><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8" fill="'+BRAND+'"/></marker></defs><g font-family="Noto Sans CJK SC,Arial,sans-serif" fill="'+INK+'">']
  self.text(28,42,kicker,13,BRAND,600);self.text(28,87,title,30,INK,600);self.text(28,120,subtitle,16,MUTED)
 def text(self,x,y,s,size=18,color=INK,weight=400):self.o.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{E(s)}</text>')
 def lines(self,x,y,text,width,size=18,line=29,color=INK,max_lines=None,weight=400):
  arr=[];s='';units=0
  tokens=list(text) if any(unicodedata.east_asian_width(c) in 'WF' for c in text) else [w+' ' for w in text.split()]
  for token in tokens:
   n=sum(1 if unicodedata.east_asian_width(c) in 'WF' else .55 for c in token)
   if s and (units+n)*size>width:arr.append(s.rstrip());s='';units=0
   s+=token;units+=n
  if s:arr.append(s.rstrip())
  if max_lines is not None:assert len(arr)<=max_lines,(text,len(arr),max_lines,width,size)
  for i,row in enumerate(arr):self.text(x,y+i*line,row,size,color,weight)
  return len(arr)*line
 def box(self,x,y,w,h,fill='#fff',stroke=LINE):self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}"/>')
 def path(self,d,opacity=.5):self.o.append(f'<path d="{d}" stroke="{BRAND}" stroke-width="1.8" fill="none" opacity="{opacity}" marker-end="url(#arrow)"/>')
 def end(self,lang):
  self.text(28,781,'行动路径示意 · 连线不表示数量、权重或已经验证的因果关系。' if lang=='zh' else 'Action pathways · Lines do not encode quantities, weights or established causal effects.',12,MUTED)
  return ''.join(self.o)+'</g></svg>'
def build(D,key,lang):
 L=lambda x:x[lang] if isinstance(x,dict) else x;t=lambda z,e:z if lang=='zh' else e
 if key=='overview':
  s=SVG(t('把四章观察，连接到三项共同任务','Connect four perspectives to three shared tasks'),'6-1-1 / EVIDENCE TO ACTION',t('共同任务跨越主体边界；九条建议需要各方配合。','Shared tasks cross actor boundaries; the nine recommendations need coordinated effort.'))
  for i,e in enumerate(D['evidence']):
   for task in e['tasks']:
    j=next(j for j,x in enumerate(D['tasks']) if x['id']==task);y=205+i*98;z=229+j*150;s.path(f'M312 {y}C390 {y} 410 {z} 488 {z}',.35)
  for i,task in enumerate(D['tasks']):
   for j,a in enumerate(D['actors']):
    y=229+i*150;z=229+j*150;s.path(f'M788 {y}C862 {y} 894 {z} 968 {z}',.25)
  for x,title in [(28,t('前文的四类观察','FOUR RESEARCH PERSPECTIVES')),(488,t('三项共同任务','THREE SHARED TASKS')),(968,t('三个主体 · 九条建议','THREE ACTORS · NINE ACTIONS'))]:s.text(x,155,title,12,MUTED)
  for i,e in enumerate(D['evidence']):
   y=168+i*98;s.box(28,y,284,74);s.text(44,y+24,e['code'],13,BRAND,600);s.lines(44,y+52,L(e['title']).split('：')[-1].split(': ')[-1].replace(' and ',' & '),250,16,23,max_lines=1)
  for i,task in enumerate(D['tasks']):
   y=172+i*150;s.box(488,y,300,114,PALE);s.text(508,y+27,task['n']+' / '+task['pillars'],13,BRAND);s.lines(508,y+61,L(task['short']),260,21,29,max_lines=2,weight=600)
  for i,a in enumerate(D['actors']):
   y=172+i*150;s.box(968,y,284,114);s.text(984,y+25,a['section']+' / '+t('三条建议','THREE ACTIONS'),12,BRAND);s.lines(984,y+57,L(a['short']),248,19,26,max_lines=1,weight=600);s.lines(984,y+83,L(a['role']),248,13,19,max_lines=2,color=MUTED)
  s.box(28,619,1224,119,PALE);s.text(50,650,t('共同目标，需要分工与协作','Shared goals need shared responsibilities'),20,INK,600);s.lines(50,685,t('公共支持改善条件，企业承担产品与维护责任，社区连接参与者与公共需求。三项任务相互支持，共同指向持续共同创造及其公共价值。','Public support improves conditions. Companies connect products and maintenance. Communities bring participants and public needs together. The three tasks support sustained co-creation and its public value.'),1170,18,28,max_lines=2,color=MUTED)
 elif key=='cycle':
  s=SVG(t('让一次创造，连接下一次创造','Connect one act of creation to the next'),'6-5-1 / SUSTAINED CO-CREATION',t('维护让成果延续，反馈让行动改进。','Maintenance sustains assets. Feedback improves action.'))
  for d in CYCLE_EDGES:s.path(d,.65)
  for i,v in enumerate(D['cycle']):
   x,y=CYCLE_POS[i];s.box(x,y,240,84);s.lines(x+17,y+31,L(v['title']),206,20,27,max_lines=1,weight=600);s.lines(x+17,y+57,L(v['subtitle']),206,12,17,max_lines=2,color=MUTED)
  s.text(490,350,'CO-CREATION',13,BRAND,600);s.lines(430,394,t('持续共同创造及其公共价值','Sustained co-creation and its public value'),420,30,43,max_lines=2,weight=600)
  s.box(28,660,1224,90,PALE);s.text(50,695,t('共同承担，持续检验','Share responsibility, examine progress'),20,INK,600);s.lines(50,725,t('把真实使用与结果带回下一轮支持，让共同创造能够不断延续。','Return actual use and outcomes to the next round of support so shared creation can continue.'),1175,17,25,max_lines=1,color=MUTED)
 else:
  actor=next(x for x in D['actors'] if x['id']==key);aa=[a for a in D['actions'] if a['actor']==key]
  s=SVG(L(actor['diagram']),actor['section'].replace('.','-')+'-1 / ACTION OVERVIEW',t('三条建议总览 · 网页版可逐条查看实施步骤、协作分工与后续观察。','Three recommendations · Explore steps, responsibilities and observations in the interactive edition.'))
  for x,title in [(28,t('行动建议','RECOMMENDATION')),(420,t('实施步骤','IMPLEMENTATION PATH')),(938,t('后续观察','WHAT TO OBSERVE'))]:s.text(x,163,title,13,BRAND,600)
  for i,a in enumerate(aa):
   y=187+i*174;s.box(28,y,350,150);s.text(48,y+29,a['number']+' / '+L(next(x for x in D['tasks'] if x['id']==a['task'])['short']),12,BRAND);s.lines(48,y+70,L(a['title']),310,22,31,max_lines=3,weight=600)
   s.path(f'M378 {y+75}H415');s.box(420,y,470,150,PALE)
   for k,step in enumerate(a['steps']):s.lines(440,y+36+k*43,str(k+1)+'  '+L(step['title']),430,17,22,max_lines=1)
   s.path(f'M890 {y+75}H933');s.box(938,y,314,150)
   for k,w in enumerate(a['watch']):s.lines(958,y+36+k*43,L(w['label']),274,17,22,max_lines=1)
  s.text(28,750,t('三项共同任务贯穿不同主体；具体实施应结合项目需要与当地条件。','The three shared tasks cut across actors. Adapt implementation to project needs and local context.'),14,MUTED)
 return s.end(lang)
def materialize(repo):
 D=json.loads((repo/'chapters/chapter6/action-framework.json').read_text());figs=repo/'figures/chapter6';figs.mkdir(exist_ok=True)
 for key,stem in FILES.items():
  for lang in ['zh','en']:(figs/(stem+('' if lang=='zh' else '-en')+'.svg')).write_text(build(D,key,lang))
 (repo/'chapters/chapter6/第六章-未来展望与政策建议.md').write_text(manuscript(D))
 print('Generated Chapter 6 manuscript and 10 editable SVG companions.')
if __name__=='__main__':materialize(Path(__file__).resolve().parents[2])
