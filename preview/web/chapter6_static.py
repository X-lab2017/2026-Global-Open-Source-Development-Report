"""Complete portrait publication views of the Chapter 6 relationship diagrams.

The web keeps interactive 1280×800 canvases. Print expands every action in the
same order, with identical task mapping, steps, roles and observation labels.
No quantitative or causal meaning is assigned to arrows.
"""
from pathlib import Path
import html,json,unicodedata
from chapter6_content import FILES,FIG_TITLES,FIG_NUMBERS,manuscript
E=lambda s:html.escape(str(s),quote=True)
INK='#18394c';MUTED='#587382';BRAND='#156993';LINE='#cadce5';PAPER='#ffffff';PALE='#edf5f8'
class SVG:
 def __init__(self,key,lang,height=1000):
  self.key,self.lang,self.height=key,lang,height
  self.o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="880" height="{height}" viewBox="0 0 880 {height}" role="img"><title>'+E(FIG_TITLES[key][lang])+'</title><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L7 3.5L0 7" fill="#156993"/></marker></defs><rect width="880" height="'+str(height)+'" fill="'+PAPER+'"/><g font-family="Noto Sans CJK SC,Arial,sans-serif" fill="'+INK+'">']
 def text(self,x,y,s,size=17,color=INK,weight=400,anchor='start'):
  assert y<=self.height-5,(y,s)
  self.o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{E(s)}</text>')
 def lines(self,x,y,text,width,size=17,line=25,color=INK,max_lines=None,weight=400):
  arr=[];s='';units=0
  tokens=list(text) if any(unicodedata.east_asian_width(c) in 'WF' for c in text) else [w+' ' for w in text.split()]
  for token in tokens:
   n=sum(1 if unicodedata.east_asian_width(c) in 'WF' else .53 for c in token)
   if s and (units+n)*size>width:
    carry=''
    if token in '，。；：！？、）】》”’' or s[-1] in '（【《“‘':carry=s[-1];s=s[:-1]
    arr.append(s.rstrip());s=carry;units=sum(1 if unicodedata.east_asian_width(c) in 'WF' else .53 for c in carry)
   s+=token;units+=n
  if s:arr.append(s.rstrip())
  if max_lines is not None:assert len(arr)<=max_lines,(self.key,text,len(arr),max_lines,width,size)
  for i,row in enumerate(arr):self.text(x,y+i*line,row,size,color,weight)
  return len(arr)*line
 def box(self,x,y,w,h,fill=PAPER,stroke=LINE):self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>')
 def path(self,d,opacity=.5):self.o.append(f'<path d="{d}" stroke="{BRAND}" stroke-width="1.5" fill="none" opacity="{opacity}" marker-end="url(#arrow)"/>')
 def arrow(self,x,y):self.o.append(f'<path d="M{x-4} {y-7}L{x} {y}L{x+4} {y-7}" fill="none" stroke="{BRAND}" stroke-width="1.5"/>')
 def end(self):
  title=('图 ' if self.lang=='zh' else 'Figure ')+FIG_NUMBERS[self.key]+' '+FIG_TITLES[self.key][self.lang]
  self.text(440,self.height-41,title,18,INK,600,'middle')
  self.text(440,self.height-13,'前文证据与行动建议的关系示意；连线不表示数量、权重或已验证的因果关系。' if self.lang=='zh' else 'Proposed pathways; lines do not encode quantity, weight or established causality.',14.5,MUTED,400,'middle')
  return ''.join(self.o)+'</g></svg>'
def build(D,key,lang):
 L=lambda x:x[lang] if isinstance(x,dict) else x;t=lambda z,e:z if lang=='zh' else e
 s=SVG(key,lang,(1260 if key=='cycle' else 1360) if lang=='en' and key!='overview' else (1060 if key not in ['overview','cycle'] else 1000))
 if key=='overview':
  s.text(24,26,t('前五章证据 → 三项共同任务 → 主体分工','EVIDENCE → THREE SHARED TASKS → RESPONSIBILITIES'),16,BRAND,600)
  s.text(24,57,t('价值起点：第一章的持续共同创造及其公共价值','Starting point: sustained co-creation and its public value'),16,MUTED)
  for i,e in enumerate(D['evidence']):
   x=24+(i%2)*428;y=77+(i//2)*98;s.box(x,y,404,82)
   s.text(x+16,y+25,e['code'],14.5,BRAND,600)
   s.lines(x+16,y+55,L(e['title']),373,17,22,max_lines=2,weight=600)
  # Individual evidence-to-task connections retain the source mapping.
  for i,e in enumerate(D['evidence']):
   x=226+(i%2)*428;y=159+(i//2)*98
   for task in e['tasks']:
    j=next(j for j,v in enumerate(D['tasks']) if v['id']==task);tx=156+j*284
    s.path(f'M{x} {y}V{275+i*5}H{tx}V316',.3)
  for i,task in enumerate(D['tasks']):
   x=24+i*284;s.box(x,318,264,254,PALE)
   s.text(x+16,344,task['n']+' / '+task['pillars'],14.5,BRAND)
   s.lines(x+16,375,L(task['short']),232,18,26,max_lines=2,weight=600)
   s.lines(x+16,438,L(task['body']),232,16 if lang=='zh' else 15,24 if lang=='zh' else 20,max_lines=6 if lang=='zh' else 7,color=MUTED)
  for i in range(3):
   for j in range(3):s.path(f'M{156+i*284} 572C{156+i*284} 602 {156+j*284} 608 {156+j*284} 638',.24)
  for i,a in enumerate(D['actors']):
   x=24+i*284;s.box(x,640,264,154)
   s.text(x+16,667,a['section'],14.5,BRAND);s.lines(x+16,699,L(a['short']),232,18,25,max_lines=1,weight=600)
   s.lines(x+16,730,L(a['role']),232,16,23,max_lines=2,color=MUTED)
   nums=' · '.join(z['number'] for z in D['actions'] if z['actor']==a['id']);s.text(x+16,779,t('建议 ','Actions ')+nums,14.5,BRAND)
  s.box(24,827,832,92,PALE)
  s.lines(42,855,t('共同复盘：先明确对象、起点与观察周期，再持续记录参与、维护、使用与结果。根据证据调整支持，让每一轮行动成为下一轮共同创造的基础。','Review together: define the population, baseline and period; record participation, maintenance, use and outcomes. Adapt support using evidence so each round of action enables further co-creation.'),796,17,26,max_lines=3)
 elif key=='cycle':
  s.text(24,26,t('从参与到反馈：每个环节都需要责任主体与记录','FROM PARTICIPATION TO FEEDBACK: RESPONSIBILITIES AND RECORDS'),16,BRAND,600)
  # Six-stage cycle, arranged in two columns for portrait reading.
  step=267 if lang=='zh' else 342;boxh=212 if lang=='zh' else 280
  pos=[(24,68),(452,68),(452,68+step),(452,68+step*2),(24,68+step*2),(24,68+step)]
  paths=[f'M404 {68+boxh/2}H452',f'M642 {68+boxh}V{68+step}',f'M642 {68+step+boxh}V{68+step*2}',f'M452 {68+step*2+boxh/2}H404',f'M214 {68+step*2}V{68+step+boxh}',f'M214 {68+step}V{68+boxh}']
  for d in paths:s.path(d,.75)
  for i,v in enumerate(D['cycle']):
   x,y=pos[i];s.box(x,y,380,boxh,PALE if i==0 else PAPER)
   s.text(x+17,y+28,f'0{i+1}',14.5,BRAND);s.text(x+55,y+28,L(v['title']),18,INK,600)
   s.lines(x+17,y+59,L(v['subtitle']),346,16,23,max_lines=2,color=BRAND)
   s.lines(x+17,y+111,L(v['body']),346,16,24,max_lines=4 if lang=='zh' else 7,color=MUTED)
  s.text(440,s.height-136,t('持续共同创造及其公共价值','Sustained co-creation and its public value'),19,BRAND,600,'middle')
  s.text(440,s.height-101,t('维护让成果延续，反馈让行动改进。','Maintenance sustains assets. Feedback improves action.'),17,MUTED,400,'middle')
 else:
  actor=next(x for x in D['actors'] if x['id']==key);aa=[a for a in D['actions'] if a['actor']==key]
  s.text(24,26,t('实施步骤 → 协作分工 → 后续观察','STEPS → RESPONSIBILITIES → FOLLOW-UP'),16,BRAND,600)
  stride=320 if lang=='zh' else 420
  for i,a in enumerate(aa):
   y=50+i*stride;s.box(24,y,832,stride-18)
   s.text(40,y+27,a['number']+'  '+L(a['title']),19,INK,600)
   task=next(v for v in D['tasks'] if v['id']==a['task']);s.text(40,y+53,L(task['short']),14.5,BRAND)
   for k,step in enumerate(a['steps']):
    x=40+k*276
    s.box(x,y+68,250,132 if lang=='zh' else 204,PALE)
    s.lines(x+12,y+94,str(k+1)+'  '+L(step['title']),226,17,23,max_lines=2,weight=600)
    s.lines(x+12,y+143,L(step['body']),226,16,22,max_lines=3 if lang=='zh' else 6,color=MUTED)
    if k<2:s.path(f'M{x+250} {y+128}H{x+276}',.75)
    role=a['roles'][k]
    if lang=='zh':
     s.text(x,y+220,L(role['who']),14.5,MUTED)
     s.lines(x,y+245,L(role['work']),250,16,22,max_lines=2,color=MUTED)
    else:s.lines(x,y+278,L(role['who'])+' · '+L(role['work']),250,15,22,max_lines=4,color=MUTED)
    s.text(x,y+stride-31,L(a['watch'][k]['label']),16,BRAND,600)
 return s.end()
def materialize(repo):
 D=json.loads((repo/'chapters/chapter6/action-framework.json').read_text());figs=repo/'figures/chapter6';figs.mkdir(exist_ok=True)
 for key,stem in FILES.items():
  for lang in ['zh','en']:
   name=stem+('' if lang=='zh' else '-en')+'.svg';body=build(D,key,lang)
   (figs/name).write_text(body);(repo/'preview/content/action'/name).write_text(body)
 (repo/'chapters/chapter6/第六章-未来展望与政策建议.md').write_text(manuscript(D))
 print('Generated complete bilingual portrait diagrams and shared manuscript.')
if __name__=='__main__':materialize(Path(__file__).resolve().parents[2])
