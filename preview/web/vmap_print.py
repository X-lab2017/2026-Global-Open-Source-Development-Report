"""Vector 2.1 publication pilot, generated from the same manuscript and data as web."""
from pathlib import Path
import argparse,hashlib,html,json,math,os,re,shutil
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Flowable,PageBreak,NextPageTemplate,Paragraph
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_publication as p
from vmap_maps import number
ROOT=p.ROOT.parent
INK,MUTED,TEAL,LINE,WASH=common.INK,common.MUTED,common.TEAL,common.LINE,common.WASH
GEO=json.loads((p.ROOT/'content/vmap/map-geometry.json').read_text())
D=p.DATA;BY={r['id']:r for r in D['countries']}
PWIDTH=A4[0]-92;LWIDTH=A4[1]-92

class Figure(common.Figure):
 def __init__(self,title,label,width=PWIDTH,height=300):
  super().__init__(title,label,height=height);self.width=width
 def caption(self,continued=False):
  self.text(self.width/2,self.height-5,self.label+('（续）' if continued else '')+'  '+self.title,10.2,INK,'center')
  return self
 def path(self,d,x,y,scale,fill,stroke='#91a8b5',lw=.4):
  self.ops.append(('map',(d,x,y,scale,fill,stroke,lw)))
 def svg(self):
  chunks=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img"><title>{html.escape(self.label+" "+self.title)}</title><rect width="100%" height="100%" fill="white"/><g font-family="Noto Sans CJK SC,Noto Sans SC,sans-serif">']
  for kind,a in self.ops:
   if kind=='map':
    d,x,y,scale,fill,stroke,lw=a
    chunks.append(f'<path d="{d}" transform="translate({x},{y}) scale({scale})" fill="{fill or "none"}" stroke="{stroke}" stroke-width="{lw/scale}" fill-rule="evenodd"/>')
   else:
    temp=common.Figure('','');temp.ops=[(kind,a)];frag=temp.svg();chunks.append(frag.split('sans-serif">',1)[1].rsplit('</g></svg>',1)[0])
  return ''.join(chunks)+'</g></svg>'
 def paint(self,c,x,top,width):
  factor=width/self.width
  c.saveState();c.translate(x,top);c.scale(factor,factor)
  for kind,a in self.ops:
   if kind=='map':
    d,ox,oy,scale,fill,stroke,lw=a;c.saveState();c.setStrokeColor(HexColor(stroke));c.setLineWidth(lw)
    if fill:c.setFillColor(HexColor(fill))
    path=c.beginPath()
    for match in re.finditer(r'([MLZ])([^MLZ]*)',d):
     op,values=match.groups()
     if op=='Z':path.close();continue
     nums=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',values)]
     getattr(path,'moveTo' if op=='M' else 'lineTo')(ox+nums[0]*scale,-oy-nums[1]*scale)
    c.drawPath(path,stroke=1,fill=bool(fill),fillMode=0);c.restoreState()
   else:
    temp=common.Figure('','');temp.ops=[(kind,a)];temp.paint(c,0,0,640)
  c.restoreState()

def title(f,x,y,text):f.text(x,y,text,10.5,INK)
def badge(f,x,y,text,width):
 f.rect(x,y-12,width,20,'#fff3d9','#a36b12',3);f.text(x+7,y+1,text,9.1,'#704400')
def notes(f,y,text,width=None):return f.lines(0,y,text,width or f.width,9,13,MUTED)

def map_panel(f,scope,x,y,w):
 rows=D['countries'] if scope=='world' else D['provinces'];by={r['id']:r for r in rows};mx=max(r['active'] or 0 for r in rows);sc=w/880
 for g in GEO[scope]:
  if g.get('kind')=='line':f.path(g['d'],x,y,sc,None,MUTED,.45);continue
  r=by.get(g['id']);v=r['active'] if r else None
  fill=('#ffffff' if g['id']=='100000_JD' else '#E6E8EA') if v is None else p.MAP_COLORS[min(5,int(v/mx*5.999))]
  f.path(g['d'],x,y,sc,fill)
 # Explicit labels remain readable at final print size; same geometry is never stretched.
 ids=['US','BR','CN','IN','ID'] if scope=='world' else ['110000','310000','440000','710000','510000']
 for code in ids:
  g=next(r for r in GEO[scope] if r['id']==code);xx=x+g['center'][0]*sc;yy=y+g['center'][1]*sc
  name=g['name'].replace('省','').replace('市','');tw=pdfmetrics.stringWidth(name,common.FONT,9.2)+6
  f.rect(xx-tw/2,yy-9,tw,13,'#ffffff','#ffffff',1);f.text(xx,yy+1,name,9.2,INK,'center')
 return mx

def map_legend(f,x,y,w,mx):
 for i,c in enumerate(p.MAP_COLORS):f.rect(x+i*13,y-8,13,7,c,c,0)
 f.text(x+84,y,'0—'+number(mx)+' 万人',8.5,MUTED)
 f.rect(x+230,y-8,12,7,'#E6E8EA',LINE,0);f.text(x+248,y,'未收录',8.5,MUTED)

def ranks(f,rows,key,x,y,w,step=19):
 title(f,x,y,('开发者总量' if key=='total' else '活跃开发者')+' · 前十 / 万人')
 rr=sorted((r for r in rows if r[key] is not None),key=lambda r:-r[key])[:10];mx=rr[0][key]
 for i,r in enumerate(rr):
  yy=y+22+i*step;name=r['name'].replace('省','').replace('市','').replace('特别行政区','')
  f.text(x,yy,f'{i+1:02} {name}',9.3,INK);f.text(x+w,yy,number(r[key]),9.3,INK,'right')
  f.line([(x,yy+5),(x+w*r[key]/mx,yy+5)],p.SERIES_COLORS[0],1.7)

def line_chart(f,x,y,w,h,values,labels,color,maximum,unit='万人',dash=None,endpoint=True):
 left=x+32;right=x+w-9;top=y+12;bottom=y+h-24
 for frac in [0,.5,1]:
  yy=bottom-(bottom-top)*frac;f.line([(left,yy),(right,yy)],LINE,.45)
  f.text(left-6,yy+3,f'{maximum*frac:,.0f}',8.5,MUTED,'right')
 points=[(left+i*(right-left)/(len(values)-1),bottom-v/maximum*(bottom-top)) for i,v in enumerate(values)]
 f.line(points,color,1.5,dash)
 for (xx,yy),yr in zip(points,labels):f.dot(xx,yy,2,color);f.text(xx,bottom+14,yr,8.5,MUTED,'center')
 if endpoint:
  for i in [0,-1]:
   xx,yy=points[i];f.text(xx+(3 if i==0 else -3),yy-6,number(values[i]),9,color,'left' if i==0 else 'right')
 f.text(x+w-9,y-3,unit,8.5,MUTED,'right')

def global_figure():
 f=Figure(p.FIGURES['global']['title'],'图 2-1-1',LWIDTH,461)
 title(f,0,13,'A  全球活跃分布与两类规模排名');f.text(LWIDTH,13,'GitHub · 2025.07.01—2026.06.30',9,MUTED,'right')
 mx=map_panel(f,'world',0,35,424);map_legend(f,0,263,424,mx)
 ranks(f,D['countries'],'total',442,42,143,19);ranks(f,D['countries'],'active',607,42,143,19)
 f.line([(0,302),(LWIDTH,302)],LINE,.6)
 title(f,0,323,'B  全球规模趋势 · 2022—2026报告年度')
 for j in range(2):
  tr=D['snapshot_trends'][j];x=j*390
  f.text(x,342,['全球开发者总量','全球活跃开发者'][j],9.5,INK)
  line_chart(f,x,345,360,87,[v/10000 for v in tr['values']],tr['labels'],p.SERIES_COLORS[0],p.SNAPSHOT_AXIS_MAX_PEOPLE[j]/10000)
 notes(f,444,'来源：OpenDigger / OpenShare。')
 return f.caption()

def current_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-1-2',height=239)
 title(f,0,13,'A  五域规模 · 2026报告年度')
 rows=D['five_group_records']
 for j,key in enumerate(['total','active']):
  x=j*263;w=240;limit=4000 if key=='total' else 800
  title(f,x,38,('开发者总量' if key=='total' else '活跃开发者')+' / 万人')
  for i,r in enumerate(rows):
   yy=63+i*27;f.text(x,yy,('全球南方' if r.get('id')=='SOUTH' else r['name']),9.2,INK)
   v=r[key]
   if v is None:f.text(x+100,yy,'未提供',9.2,MUTED);continue
   f.rect(x+83,yy-9,95*v/limit,10,p.SERIES_COLORS[0],p.SERIES_COLORS[0],0);f.text(x+w,yy,number(v),9.2,INK,'right')
  f.line([(x+83,183),(x+178,183)],LINE,.6);f.text(x+83,195,'0',8.5,MUTED);f.text(x+178,195,str(limit),8.5,MUTED,'right')
 notes(f,214,'来源：报告编制组。全球南方为代表组；五域不构成全球穷尽划分。')
 return f.caption()

def history_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-1-2',height=603)
 title(f,0,13,'B  五域活跃规模演变 · 2022—2026报告年度')
 f.text(0,37,'每年统计期：前一年7月1日至当年6月30日',9,MUTED)
 left=37;right=323;top=76;bottom=278
 for v in [0,200,400,600,800]:
  yy=bottom-v/800*(bottom-top);f.line([(left,yy),(right,yy)],LINE,.5);f.text(left-7,yy+3,str(v),9,MUTED,'right')
 for i,yr in enumerate(D['trend']['years']):f.text(left+i*(right-left)/4,bottom+17,yr,9,MUTED,'center')
 f.text(0,65,'万人',9,MUTED)
 for j,r in enumerate(D['trend']['series']):
  pts=[(left+i*(right-left)/4,bottom-v/800*(bottom-top)) for i,v in enumerate(r['values'])]
  f.line(pts,p.SERIES_COLORS[j],1.6,p.SERIES_DASH[j])
  for xx,yy in pts:f.dot(xx,yy,2,p.SERIES_COLORS[j])
  ly=85+j*39;f.line([(347,ly-3),(369,ly-3)],p.SERIES_COLORS[j],1.6,p.SERIES_DASH[j]);f.text(376,ly,('全球南方' if r.get('id')=='SOUTH' else r['name']),9.2,INK)
  f.text(376,ly+15,f'{r["values"][0]:.2f} → {r["values"][-1]:.2f}',9,MUTED)
 notes(f,320,'来源：报告编制组五域历史统计。')
 f.line([(0,348),(PWIDTH,348)],LINE,.6)
 title(f,0,372,'C  平台覆盖比较 · 活跃开发者 / 万人')
 f.line([(0,397),(16,397)],p.SERIES_COLORS[0],3);f.text(23,400,'GitHub',9,MUTED)
 f.line([(91,397),(107,397)],p.SERIES_COLORS[1],3);f.text(114,400,'中国国内平台补充约120万（去重）',9,MUTED)
 for i,code in enumerate(['US','CN','IN']):
  r=BY[code];yy=430+i*34;x=66;w=320
  f.text(0,yy,r['name'],9.5,INK);f.rect(x,yy-11,w*r['active']/500,13,p.SERIES_COLORS[0],p.SERIES_COLORS[0],0)
  if code=='CN':
   x0=x+w*r['active']/500;ww=w*120/500;f.rect(x0,yy-11,ww,13,'#edf6f5',p.SERIES_COLORS[1],0)
   for xx in range(math.ceil(x0),int(x0+ww),6):f.line([(xx,yy+2),(min(xx+7,x0+ww),yy-11)],p.SERIES_COLORS[1],.8)
  f.text(PWIDTH,yy,'约'+str(round(r['active']+D['domestic']['active_approx'])) if code=='CN' else number(r['active']),9.5,INK,'right')
 f.line([(66,516),(386,516)],LINE,.6);f.text(66,529,'0',8.5,MUTED);f.text(386,529,'500',8.5,MUTED,'right')
 notes(f,550,'国内补充依据：报告编制组根据 Gitee、AtomGit 等官方平台数据，结合问卷调研去重得到。其他国家仅展示 GitHub 覆盖。')
 notes(f,578,'统计期：2025.07.01—2026.06.30。来源：OpenDigger / OpenShare；报告编制组。')
 return f.caption(True)

def china_figure():
 f=Figure(p.FIGURES['china']['title'],'图 2-1-3',height=508)
 title(f,0,13,'A  中国省级活跃分布')
 title(f,330,13,'B  全国活跃规模 / 万人')
 f.text(330,34,'2022—2026报告年度',9,MUTED)
 mx=map_panel(f,'china',0,30,318)
 tr=D['snapshot_trends'][2]
 line_chart(f,326,55,177,140,[v/10000 for v in tr['values']],tr['labels'],p.SERIES_COLORS[0],p.SNAPSHOT_AXIS_MAX_PEOPLE[2]/10000,unit='')
 map_legend(f,0,210,318,mx)
 f.text(PWIDTH,210,'GitHub · 2026报告年度',9,MUTED,'right')
 f.line([(0,224),(PWIDTH,224)],LINE,.6)
 ranks(f,D['provinces'],'total',0,245,236,15.5)
 ranks(f,D['provinces'],'active',267,245,236,15.5)
 title(f,0,428,'C  区域活跃份额')
 rr=sorted(D['provinces'],key=lambda r:-r['active'])
 values=[sum(r['active'] for r in rr[:3]),sum(r['active'] for r in rr[3:10]),sum(r['active'] for r in rr[10:])]
 x=0
 for i,(label,v) in enumerate(zip(['京沪粤','第4—10位','其余24地'],values)):
  share=v/BY['CN']['active'];w=PWIDTH*share;f.rect(x,441,w,13,p.SERIES_COLORS[i],p.SERIES_COLORS[i],0)
  if i:f.line([(x,441),(x,454)],'#ffffff',1)
  tx=x+w/2;x+=w;f.text(PWIDTH if i==2 else tx,474,label+' '+f'{share*100:.1f}%',9,INK,'right' if i==2 else 'center')
 notes(f,491,'来源：OpenDigger / OpenShare。开发者总量为平台估计；份额独立取整。')
 return f.caption()

class FigureFlow(Flowable):
 def __init__(self,fig,key):super().__init__();self.fig=fig;self.key=key;self.width=fig.width;self.height=fig.height;self.spaceBefore=8;self.spaceAfter=8
 def draw(self):self.fig.paint(self.canv,0,self.height,self.width)
class Doc(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=A4,title='GOSD 2026 · 2.1 全球开源活跃地图',author='GOSD / 全球开源发展报告',subject='同源正文、三幅图组与复杂图件出版样章',invariant=1)
  self.locations=[];self.figures={};self.headings=[]
  for name,size in [('portrait',A4),('landscape',landscape(A4))]:
   w,h=size;self.addPageTemplates(PageTemplate(name,[Frame(46,57,w-92,h-121,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],pagesize=size,onPage=self.frame))
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图')
  c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.1 全球开源活跃地图 · V-Map');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
 def afterFlowable(self,f):
  if isinstance(f,FigureFlow):self.figures[f.key]=self.page
  if isinstance(f,Paragraph):
   self.locations.append(dict(page=self.page,text=f.getPlainText(),style=f.style.name))
   if f.style.name in ['chapter','section','subsection']:
    level={'chapter':0,'section':1,'subsection':2}[f.style.name];key='h'+str(len(self.headings));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,level,False);self.headings.append(dict(page=self.page,text=f.getPlainText(),level=level))

def build(output,figs):
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={
 'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=16,keepWithNext=True),
 'section':ParagraphStyle('section',parent=body,fontSize=12.6,leading=21,spaceBefore=12,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),
 'subsection':ParagraphStyle('subsection',parent=body,fontSize=11.2,leading=19,spaceBefore=8,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),
 'note':ParagraphStyle('note',parent=body,fontSize=9.5,leading=15,spaceAfter=8)}
 story=[]
 def para(s,style='body'):story.append(common.paragraph(s,styles.get(style,body)))
 def section(i):
  title,paras=p.STORIES[i];para(title,'section')
  for text in paras[:p.FIGURE_AFTER[i]]:para(text)
 def interpretation(i):
  for text in p.STORIES[i][1][p.FIGURE_AFTER[i]:]:
   head,tail=text.split('。',1);para('**'+head+'。**'+tail)
 para('2.1 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.SNAPSHOT_NOTE,'note');section(0)
 story.extend([NextPageTemplate('landscape'),PageBreak(),FigureFlow(figs[0],'2-1-1')]);story.extend([NextPageTemplate('portrait'),PageBreak()])
 interpretation(0);section(1);story.append(FigureFlow(figs[1],'2-1-2-A'));story.append(PageBreak());story.append(FigureFlow(figs[2],'2-1-2-BC'));interpretation(1);story.append(PageBreak())
 section(2);story.append(FigureFlow(figs[3],'2-1-3'));interpretation(2);story.append(PageBreak())
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,paras) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for text in paras:para(text)
 para('统计范围与指标说明','section');para(p.INDICATOR_FEEDBACK,'note')
 for text in p.GAPS:para(text,'note')
 para(p.BRIDGE)
 doc=Doc(output);doc.build(story)
 return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=ROOT/'output/pdf'/p.PDF_NAME);args=parser.parse_args()
 work=ROOT/'tmp/pdfs/vmap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 extra=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False)+json.dumps(GEO,ensure_ascii=False)
 common.font_setup(args.font,work,subset_text=extra)
 figs=[global_figure(),current_figure(),history_figure(),china_figure()]
 dest=p.ROOT/'content/vmap/print';dest.mkdir(parents=True,exist_ok=True)
 names=[name for spec in p.FIGURES.values() for name in spec['files']]
 for name,fig in zip(names,figs):(dest/name).write_text(fig.svg())
 # Retain previous direct-download URLs, pointing to the same complete one-page view.
 for name in ['fig-2-1-3_a_geography.svg','fig-2-1-3_bcd_structure.svg']:(dest/name).write_text(figs[3].svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME)
 (p.ROOT/'content/vmap/chapter-2-1.md').write_text(p.manuscript())
 manifest=dict(edition=p.EDITION,baseline='GOSD-PUB-20261020',chapter_baseline='GOSO-PUB-20261020',scope='2.1 完整正文与三幅图组；第二章其他小节未收录',pdf=p.PDF_NAME,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],source_sha256=hashlib.sha256((p.ROOT/'content/vmap/fig-2-1-2_platform-coverage.json').read_bytes()).hexdigest(),manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest(),figures=p.specification(),verification=dict(browser_visual='not_run_no_supported_browser',physical_print='not_run',pdf_render='pending_current_revision',grayscale='pending_current_revision',dom='pending_current_revision'))
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2))
 print(json.dumps(dict(pdf=str(args.output),pages=layout['pages'],figure_pages=layout['figures']),ensure_ascii=False))
if __name__=='__main__':main()
