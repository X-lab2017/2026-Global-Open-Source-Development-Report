"""F-Ranking review PDF: shared prose, immutable source values, explicit simulations."""
from pathlib import Path
import argparse,json
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import foundation_publication as p
import gosr_content as g

D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';PALE='#F3F8FA';TRACK='#E1EDF2';GOLD='#765214'
ROOT=Path(__file__).resolve().parents[1]/'content/gosr'
REF=json.loads((ROOT/'foundation-reference.json').read_text())
SIM=json.loads((ROOT/'foundation-lf-simulated.json').read_text())
COLORS=['#287f9f','#c17038','#8c69b2','#258f72','#ba587e','#687b40','#5571bd','#ae8b22','#527885','#995d45','#7461a7','#35877e','#a36b88','#807b4c','#4b6c8a','#9a7441']
fmt=lambda v,d=2:f'{float(v):,.{d}f}'

def bar(f,x,y,w,value,maximum):
 f.rect(x,y,w,4,TRACK,TRACK,1);f.rect(x,y,w*float(value)/maximum,4,BLUE,BLUE,1)
def fittext(f,x,y,t,width,size=9,color=INK):
 f.text(x,y,t,min(size,width/pdfmetrics.stringWidth(t,common.FONT,1)),color)

def leading_figure():
 f=vp.Figure(p.FIGURES[0],'图 3-3-1',height=280)
 f.text(0,16,'全球榜前五 · 完整 21 个条目见续图',11,TEAL)
 f.text(365,38,'OpenRank',8.8,MUTED,'right');f.text(W,38,'活跃开发者 / 人',8.8,MUTED,'right')
 for i,r in enumerate(D['foundation']['rows'][:5]):
  y=64+i*36
  f.text(0,y,f'{int(r["rank"]):02}',10,MUTED);fittext(f,24,y,r['foundation_zh'],200,10.2)
  bar(f,24,y+10,341,r['openrank'],196128.27)
  f.text(365,y,fmt(r['openrank']),10.2,INK,'right');f.text(W,y,fmt(r['active_developers'],0),10.2,INK,'right')
 f.text(0,248,'条形从零起；组织范围可能重叠，不加总分值或人数。',8.6,MUTED)
 return f.caption()

def global_figure():
 f=vp.Figure(p.FIGURES[0],'图 3-3-1',LW,461)
 f.text(0,13,'全球榜 · 21 个原始条目',11,TEAL)
 f.rect(0,25,LW,22,PALE,PALE,0)
 for x,s,align in [(5,'名次','left'),(35,'基金会','left'),(419,'OpenRank','right'),(493,'活跃开发者 / 人','right'),(514,'代表项目 / 计划','left')]:f.text(x,40,s,8.5,MUTED,align)
 for i,r in enumerate(D['foundation']['rows']):
  y=60+i*17.7;ref=REF['global'][r['foundation']]
  if i%2==0:f.rect(0,y-11,LW,17.7,'#F7FAFB','#F7FAFB',0)
  f.text(5,y,f'{int(r["rank"]):02}',8.7,MUTED)
  fittext(f,35,y,r['foundation_zh'],205,9)
  bar(f,253,y-4,85,r['openrank'],196128.27)
  f.text(419,y,fmt(r['openrank']),9,INK,'right');f.text(493,y,fmt(r['active_developers'],0),9,INK,'right')
  projects=' / '.join(q['name'] for q in ref.get('projects',[])) or '项目关系待核验'
  fittext(f,514,y,projects,LW-519,8.6,MUTED)
 f.text(0,436,'条形从零起；组织范围可能重叠，不加总。代表项目为阅读入口，非完整统计清单。',8.6,MUTED)
 return f.caption(True)

def children_figure():
 f=vp.Figure(p.FIGURES[1],'图 3-3-2',height=470)
 f.rect(0,0,W,25,'#FFF4DC','#D2B16F',3);f.text(10,17,'模拟 · 名次、OpenRank 与开发者数均非实测',10,GOLD)
 f.rect(0,35,W,22,PALE,PALE,0)
 for x,s,a in [(4,'位次 / 组织与领域','left'),(248,'OpenRank','right'),(313,'开发者 / 人','right'),(329,'代表项目','left')]:f.text(x,50,s,8.2,MUTED,a)
 for i,r in enumerate(SIM['rows']):
  ref=next(c for c in REF['children'] if c['id']==r['id']);y=70+i*23.5
  if i%2==0:f.rect(0,y-11,W,23.5,'#F7FAFB','#F7FAFB',0)
  f.text(4,y+2,f'{int(r["rank"]):02}',8.8,MUTED);fittext(f,26,y,ref['short'],128,9.2);fittext(f,26,y+8.7,ref['field'],128,7.6,MUTED)
  bar(f,162,y+5,86,r['openrank'],62500);f.text(248,y,fmt(r['openrank']),9,INK,'right');f.text(313,y+2,fmt(r['active_developers'],0),9,INK,'right')
  lines=[];line=''
  for q in ref.get('projects',[]):
   candidate=(line+' / ' if line else '')+q['name']
   if line and pdfmetrics.stringWidth(candidate,common.FONT,8.6)>W-334:lines.append(line);line=q['name']
   else:line=candidate
  if line:lines.append(line)
  for j,line in enumerate(lines):fittext(f,329,y-1+j*10.5,line,W-334,8.6,MUTED)
 f.text(0,445,'16 个组织示例，非完整名录；模拟值不回算 Linux 基金会整体。',8.4,MUTED)
 return f.caption()

def history_figure(sim=False):
 height=235 if sim else 312;f=vp.Figure(p.FIGURES[2],'图 3-3-3',height=height)
 if sim:
  f.rect(0,0,W,25,'#FFF4DC','#D2B16F',3);f.text(10,17,'模拟月度轨迹 · 五个组织示例',10,GOLD)
  rows=SIM['monthly'];keys=[r['id'] for r in REF['children']];names=['cncf','pytorch','lf-ai-data','openjs','aaif'];label=lambda n:next(r['short'] for r in REF['children'] if r['id']==n);top=46
 else:
  rows=D['foundationMonth']['rows'];keys=list(rows[0])[1:];names=keys;short=['Linux 基金会','开放原子','Apache','NixOS','Rust','Python','Godot','Ruby'];label=lambda n:short[keys.index(n)];top=35
  f.text(0,13,'全球基金会 · 八家月度记录',11,TEAL)
 left=24;right=W-100;bottom=height-59;maximum=max(float(r[n]) for r in rows for n in names if r.get(n) not in ('',None))
 xx=lambda i:left+i*(right-left)/(len(rows)-1);yy=lambda n:top+(n-1)/(maximum-1)*(bottom-top)
 ticks=range(1,int(maximum)+1) if not sim else [1,4,8,12,16]
 for n in ticks:
  f.line([(left,yy(n)),(right,yy(n))],LINE,.45);f.text(left-7,yy(n)+3,str(n),8,MUTED,'right')
 for i,r in enumerate(rows):f.text(xx(i),bottom+14,r['month'][5:],8,MUTED,'center')
 ends=[]
 for n in names:
  color=COLORS[keys.index(n)%16];points=[]
  for i,r in enumerate(rows):
   if r.get(n) in ('',None):
    if len(points)>1:f.line(points,color,1.4)
    points=[];continue
   xy=(xx(i),yy(float(r[n])));points.append(xy);f.dot(*xy,2,color)
  if len(points)>1:f.line(points,color,1.4)
  if rows[-1].get(n) not in ('',None):ends.append([yy(float(rows[-1][n])),n,str(rows[-1][n]),color])
 ends.sort();last=top-14
 for e in ends:e.append(max(e[0],last+14));last=e[4]
 if ends[-1][4]>bottom:
  ends[-1][4]=bottom
  for i in range(len(ends)-2,-1,-1):ends[i][4]=min(ends[i][4],ends[i+1][4]-14)
 for actual,n,value,color,y in ends:
  f.line([(right,actual),(right+7,y),(right+12,y)],color,.7);f.text(right+16,y+3,label(n),8.6,color);f.text(W,y+3,value,8.6,color,'right')
 f.text(0,height-27,'2025 年 7 月—2026 年 6 月 · 第 1 名在上；缺失月份留空。',8.4,MUTED)
 return f.caption(sim)

class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'3.3 基金会影响力 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Section3-3-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/f-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps([D,REF,SIM],ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 def interpret(t):head,tail=t.split('。',1);add('**'+head+'。**'+tail)
 add('3.3 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);story.append(vp.FigureFlow(leading_figure(),'3-3-1-lead'))
 story += [NextPageTemplate('landscape'),PageBreak(),vp.FigureFlow(global_figure(),'3-3-1'),NextPageTemplate('portrait'),PageBreak()]
 for t in p.STORIES[0][1][1:]:interpret(t)
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);story.append(vp.FigureFlow(children_figure(),'3-3-2'));story.append(PageBreak())
 for t in p.STORIES[1][1][1:]:interpret(t)
 add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(vp.FigureFlow(history_figure(),'3-3-3'));story.append(PageBreak());story.append(vp.FigureFlow(history_figure(True),'3-3-3-cont'))
 for t in p.STORIES[2][1][1:]:interpret(t)
 add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE)
 doc=Doc(a.output);doc.title='GOSD 2026 · 3.3 '+p.TITLE;doc.subject='F-Ranking 图文出版样章';doc.build(story)
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':p.EDITION},ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
