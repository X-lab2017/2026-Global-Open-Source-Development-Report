"""T-Map vector figures and complete print manuscript, using pinned source values."""
from pathlib import Path
import argparse,hashlib,json,math,shutil
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import vmap_publication as brand
import tmap_publication as p
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
Figure,FigureFlow=vp.Figure,vp.FigureFlow
PW,LW=vp.PWIDTH,vp.LWIDTH
D,S=p.D,p.SIM
G=['United States','China','Europe','Global South representatives','India']
LABEL=['美国','中国','欧洲','全球南方六国','印度']
COLORS=[brand.SERIES_COLORS[i] for i in [1,2,0,4,3]]
DASH=[None,[7,3],[2,3],[9,3,2,3],[5,3]]
num=lambda v:f'{v:,}'
def map_draw(f,scope,x,y,w,by=None):
 sc=w/880
 for g in vp.GEO[scope]:
  v=by.get(g['id']) if by else None
  fill='#e6e8ea' if v is None else '#ffffff' if v==0 else brand.MAP_COLORS[0 if v<100 else 1 if v<500 else 2 if v<2000 else 3 if v<5000 else 4 if v<10000 else 5]
  f.path(g['d'],x,y,sc,None if g.get('kind')=='line' else fill,'#9cacb6',.3)
 return sc
def trend(f,series,x,y,w,h,maxv):
 left=x+32;right=x+w-7;top=y+15;bottom=y+h-24
 f.text(x,y+3,'人',8.5,MUTED)
 for i in range(4):
  v=maxv*i/3;yy=bottom-(bottom-top)*i/3;f.line([(left,yy),(right,yy)],LINE,.4);f.text(left-5,yy+3,num(round(v)),8.5,MUTED,'right')
 for j,yr in enumerate(D['years']):f.text(left+j*(right-left)/4,bottom+16,str(yr),8.5,MUTED,'center')
 for k,vs in series.items():
  idx=G.index(k);pts=[(left+j*(right-left)/4,bottom-v/maxv*(bottom-top)) for j,v in enumerate(vs)];f.line(pts,COLORS[idx],1.4,DASH[idx])
  for xx,yy in pts:f.dot(xx,yy,2,COLORS[idx])
def global_figure():
 f=Figure(p.FIGURES['world']['title'],'图 2-4-1',LW,461);vp.title(f,0,13,'A  人才地域分布 · 2026年7月');by={r['code']:r['value'] for r in D['world']};sc=map_draw(f,'world',0,48,472,by)
 for code in ['US','CN','IN','BR']:
  g=next(g for g in vp.GEO['world'] if g['id']==code);x=g['center'][0]*sc;y=48+g['center'][1]*sc;name=next(r['name'] for r in D['world'] if r['code']==code);f.rect(x-12,y-9,24,14,'#ffffff','#ffffff',1);f.text(x,y+1,name,9,INK,'center')
 labels=['1—99','100—499','500—1,999','2,000—4,999','5,000—9,999','≥10,000']
 for i,(c,label) in enumerate(zip(brand.MAP_COLORS,labels)):
  x=(i%3)*155;y=328+(i//3)*23;f.rect(x,y-7,17,8,c,c,0);f.text(x+22,y,label,8.8,MUTED)
 f.rect(0,371,17,8,'#e6e8ea',LINE,0);f.text(22,379,'未收录',8.8,MUTED);f.text(160,379,'单位：人',8.8,MUTED)
 vp.title(f,505,13,'B  源表人数前十');f.text(LW,37,'人',8.5,MUTED,'right')
 for i,r in enumerate(D['world'][:10]):
  y=63+i*33;f.text(505,y,f'{i+1:02}  '+r['name'],9.4,INK);f.text(LW,y,num(r['value']),9.4,INK,'right');f.line([(505,y+9),(505+240*r['value']/35005,y+9)],TEAL,2)
 vp.notes(f,422,'来源：报告编制组。地图快照与五域年度序列分别阅读。');return f.caption()
def regions_figure():
 f=Figure(p.FIGURES['regions']['title'],'图 2-4-2',height=372);vp.title(f,0,13,'A  五年趋势 · 2022—2026报告年度');trend(f,D['regions'],0,29,PW,184,60000)
 for j,k in enumerate(G):
  x=j*100;f.line([(x,218),(x+15,218)],COLORS[j],1.4,DASH[j]);f.text(x+20,221,LABEL[j],8.5,INK)
 vp.title(f,0,246,'B  2026年规模与增长');heads=[(0,'比较组'),(247,'人数'),(366,'同比净增'),(PW,'同比增幅')]
 for x,label in heads:f.text(x,266,label,8.5,MUTED,'left' if x==0 else 'right')
 for row,j in enumerate([2,0,1,3,4]):
  v=D['regions'][G[j]];y=284+row*14;f.text(0,y,LABEL[j],9,COLORS[j]);f.text(247,y,num(v[-1]),9,INK,'right');f.text(366,y,num(v[-1]-v[-2]),9,INK,'right');f.text(PW,y,f'{(v[-1]/v[-2]-1)*100:.1f}%',9,INK,'right')
 vp.notes(f,359,'来源：报告编制组');return f.caption()
def china_figure():
 f=Figure(p.FIGURES['china']['title'],'图 2-4-3',height=386);vp.title(f,0,13,'A  十城位置');sc=map_draw(f,'china',0,27,277)
 offsets={'北京':(14,-8),'上海':(20,-8),'台北':(17,12),'成都':(-15,-10),'深圳':(-12,20)}
 for k,vs in D['cities'].items():
  x0,y0=D['cityPoints'][k];x,y=x0*sc,27+y0*sc;f.dot(x,y,math.sqrt(vs[-1]/971)*5.2,TEAL)
  if k in offsets:
   dx,dy=offsets[k];f.line([(x,y),(x+dx,y+dy)],MUTED,.4);f.text(x+dx,y+dy-2,k,8.5,INK,'center')
 f.text(0,201,'圆面积表示人数 · 十城样本',8.5,MUTED)
 vp.title(f,304,13,'B  2026年人数');f.text(PW,34,'人',8.5,MUTED,'right')
 for i,(k,vs) in enumerate(D['cities'].items()):
  y=51+i*16;f.text(304,y,f'{i+1:02}  {k}',9,INK);f.text(PW,y,num(vs[-1]),9,INK,'right')
 vp.title(f,0,231,'C  同一十城的五年变化');f.dot(230,228,2.6,MUTED);f.text(238,231,'2022',8.5,MUTED);f.dot(284,228,3,TEAL);f.text(292,231,'2026',8.5,MUTED);f.text(PW,231,'五年增幅',8.5,MUTED,'right')
 x=lambda v:45+v/1050*350
 for v in [0,250,500,750,1000]:f.line([(x(v),242),(x(v),353)],LINE,.35);f.text(x(v),366,str(v),8.5,MUTED,'center')
 for i,(k,vs) in enumerate(D['cities'].items()):
  y=246+i*11.6;f.text(0,y+3,k,8.5,INK);f.line([(x(vs[0]),y),(x(vs[-1]),y)],LINE,1.5);f.dot(x(vs[0]),y,2.1,MUTED);f.dot(x(vs[-1]),y,2.3,TEAL);f.text(PW,y+3,f'+{(vs[-1]/vs[0]-1)*100:.1f}%',8.5,INK,'right')
 return f.caption()
def growth_figure():
 f=Figure(p.FIGURES['growth']['title'],'图 2-4-4',height=375);vp.badge(f,0,13,'模拟数据｜待替换',133);vp.title(f,0,45,'A  新人进入后的持续贡献');f.text(PW,45,'每队列1,000人',8.5,MUTED,'right')
 for j,m in enumerate([3,6,12,24]):f.text(145+j*101,67,f'第{m}个月',8.5,MUTED,'center')
 for i,row in enumerate(S['cohorts']):
  y=78+i*19;f.text(0,y+12,row['period'],9,INK)
  for j,v in enumerate(row['rates']):
   x=100+j*101;fill='#f3f5f6' if v is None else ['#e5f1f3','#c5e0e4','#91c4cd','#5ba4b1'][min(3,v//20)];f.rect(x,y,90,16,fill,fill,0);f.text(x+45,y+12,'未满观察期' if v is None else f'{v}%',8.5,INK,'center')
 vp.title(f,0,250,'B  人才留存 · 同一上年样本');f.text(PW,250,'每情景1,000人',8.5,MUTED,'right')
 for j,c in enumerate(S['retention']):
  x=j*262;f.text(x,271,c['name'],9,INK)
  for i,(label,v,color) in enumerate([('持续贡献',c['active'],TEAL),('仍在前5%',c['top'],COLORS[3])]):
   yy=287+i*17;f.text(x,yy,label,8.5,MUTED);f.rect(x+63,yy-6,v*1.6,5,color,color,0);f.text(x+240,yy,f'{v}%',8.5,INK,'right')
 vp.title(f,0,329,'C  接续条件 · 默认参数');f.text(0,346,'1,000人 × 45%持续贡献 × 12%条件比例 ＝ 54人',9,INK);f.text(PW,346,'非预测',8.5,MUTED,'right');return f.caption()
def connections_figure():
 f=Figure(p.FIGURES['connect']['title'],'图 2-4-5',height=408);vp.badge(f,0,13,'模拟数据｜待替换',133);vp.title(f,0,43,'A  跨地域协作 · 人才所在地 → 项目归属组');sc=map_draw(f,'world',0,52,290);codes=['US','CN','DE','BR','IN'];nodes=[next(g for g in vp.GEO['world'] if g['id']==c)['center'] for c in codes];x1,y1=nodes[1];x1*=sc;y1=52+y1*sc
 for j,(xx,yy) in enumerate(nodes):
  x2,y2=xx*sc,52+yy*sc
  if j!=1:
   mx=(x1+x2)/2;my=min(y1,y2)-abs(x2-x1)*.2;pts=[((1-t)**2*x1+2*(1-t)*t*mx+t*t*x2,(1-t)**2*y1+2*(1-t)*t*my+t*t*y2) for t in [k/32 for k in range(33)]];f.line(pts,TEAL,.6+S['flows'][1][j]/30,[3,2]);dx,dy=x2-pts[-2][0],y2-pts[-2][1];ll=math.hypot(dx,dy);ux,uy=dx/ll,dy/ll;f.polygon([(x2,y2),(x2-5*ux+2*uy,y2-5*uy-2*ux),(x2-5*ux-2*uy,y2-5*uy+2*ux)],TEAL)
  f.dot(x2,y2,3,COLORS[j])
 f.text(315,70,'中国来源 · 100条模拟关系',9,INK)
 for i,j in enumerate([0,2,3,4]):f.text(315,93+i*21,LABEL[j],8.8,INK);f.text(PW,93+i*21,str(S['flows'][1][j])+'条',8.8,INK,'right')
 f.text(0,211,'节点为分组示意位置；关系不表示迁居。',8.5,MUTED)
 vp.title(f,0,239,'B  技术领域转换 · 1,000人');vp.title(f,267,239,'C  AI领域 × 贡献角色')
 # Same source-to-target curve geometry as the web; all three sources remain visible in print.
 fr=S['transition']['from'];to=S['transition']['to'];m=S['transition']['matrix']
 for a,row in enumerate(m):
  for b,v in enumerate(row):
   y1=278+a*34;y2=278+b*34;pts=[]
   for i in range(33):
    t=i/32;pts.append(((1-t)**3*68+3*(1-t)**2*t*105+3*(1-t)*t*t*130+t**3*167,(1-t)**3*y1+3*(1-t)**2*t*y1+3*(1-t)*t*t*y2+t**3*y2))
   f.line(pts,['#93c6cb','#b5cadd','#aac39b'][a],v/38)
 for i,name in enumerate(fr):f.text(0,279+i*34,name,8.5,INK);f.text(0,292+i*34,str(sum(m[i]))+'人',8.5,MUTED)
 for i,name in enumerate(['基础软件','Agent/模型工具','数据协作']):f.text(174,279+i*34,name,8.5,INK);f.text(174,292+i*34,str(sum(row[i] for row in m))+'人',8.5,MUTED)
 labels=['代码','评审','文档','导师']
 for j,name in enumerate(labels):f.text(361+j*40,261,name,8.5,MUTED,'center')
 for i,name in enumerate(['AI基础软件','Agent工具','模型与推理','数据与评测','应用与集成']):
  y=281+i*18;f.text(267,y,name,8.5,INK)
  for j,v in enumerate(S['ai']['matrix'][i]):f.rect(346+j*40,y-10,33,14,'#e5f1f3','#e5f1f3',0);f.text(362+j*40,y+1,str(v),8.5,INK,'center')
 f.text(267,382,'每行100条模拟主角色记录',8.5,MUTED);return f.caption()
class Doc(vp.Doc):
 def __init__(self,path):super().__init__(path);self.title='GOSD 2026 · 2.4 全球开源人才地图';self.subject='完整研究正文与五幅人才地图图组'
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.4 全球开源人才地图 · T-Map');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def build(output,figs):
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=16,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.6,leading=21,spaceBefore=12,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,fontSize=11.2,leading=19,spaceBefore=8,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,s='body'):story.append(common.paragraph(t,styles.get(s,body)))
 def lead(i):para(p.STORIES[i][0],'section');para(p.STORIES[i][1][0])
 def after(i):
  for t in p.STORIES[i][1][1:]:
   a,b=t.split('。',1);para('**'+a+'。**'+b)
 para('2.4 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0);after(0)
 story.extend([NextPageTemplate('landscape'),PageBreak(),FigureFlow(figs[0],'2-4-1'),NextPageTemplate('portrait'),PageBreak()])
 for i in [1,2,3,4]:lead(i);story.append(FigureFlow(figs[i],f'2-4-{i+1}'));after(i);story.append(PageBreak())
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,ps) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for t in ps:para(t)
 para('统计范围与指标说明','section')
 for t in p.NOTES:para(t,'note')
 para(p.BRIDGE);doc=Doc(output);doc.build(story);return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=p.ROOT.parent/'output/pdf'/p.PDF_NAME);args=parser.parse_args();work=p.ROOT.parent/'tmp/pdfs/tmap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False)+json.dumps(S,ensure_ascii=False)+Path(vp.__file__).read_text())
 figs=[global_figure(),regions_figure(),china_figure(),growth_figure(),connections_figure()];dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 for spec,fig in zip(p.FIGURES.values(),figs):(dest/spec['file']).write_text(fig.svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.BASE/'chapter-2-4.md').write_text(p.manuscript());digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256={n:digest(p.BASE/n) for n in ['observations.json','simulation.json']},manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
if __name__=='__main__':main()
