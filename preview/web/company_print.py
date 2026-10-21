"""Local C-Ranking review PDF; shares manuscript, tables and simulation with Web."""
from pathlib import Path
import argparse,json,math
import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate,Spacer
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import company_publication as p
import gosr_content as g

D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';PALE='#F3F8FA';TRACK='#E1EDF2'
COLORS=['#287f9f','#c17038','#8c69b2','#258f72','#ba587e','#687b40','#5571bd','#ae8b22','#527885','#995d45']
LOGO_DIR=Path(__file__).resolve().parents[1]/'content/gosr/company-logos'
LOGOS=json.loads((LOGO_DIR/'manifest.json').read_text())
IMAGE_PLACEMENTS=[]
fmt=lambda v,d=2:f'{float(v):,.{d}f}'

class Figure(vp.Figure):
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.images=[]
 def logo(self,company,x,y,size=17):
  if company in LOGOS:
   self.rect(x-1,y-1,size+2,size+2,'#ffffff',LINE,2)
   self.images.append((company,x,y,size))
 def paint(self,c,x,top,width):
  super().paint(c,x,top,width);scale=width/self.width
  for company,px,py,size in self.images:
   ax,ay=c.absolutePosition(x+px*scale,top-py*scale)
   IMAGE_PLACEMENTS.append({'page':c.getPageNumber()-1,'company':company,'rect':[ax,c._pagesize[1]-ay,ax+size*scale,c._pagesize[1]-ay+size*scale]})

def bar(f,x,y,w,value,maximum,color=BLUE):
 f.rect(x,y,w,4,TRACK,TRACK,1);f.rect(x,y,w*value/maximum,4,color,color,1)

def main_figure():
 f=Figure(p.FIGURES[0],'图 3-2-1',LW,461);cw=(LW-22)/2
 for j in range(2):
  x=j*(cw+22);f.text(x,13,'全球企业 Top 30'+(' · 16—30' if j else ' · 1—15'),11,TEAL)
  f.rect(x,25,cw,22,PALE,PALE,0)
  for xx,label in [(x+5,'名次 / 企业'),(x+cw-111,'OpenRank'),(x+cw-58,'仓库 / 个'),(x+cw-5,'开发者 / 人')]:f.text(xx,40,label,8.3,MUTED,'left' if xx==x+5 else 'right')
  for i,r in enumerate(D['company']['rows'][j*15:(j+1)*15]):
   y=53+i*24.7
   if i%2==0:f.rect(x,y-2,cw,24.7,'#F7FAFB','#F7FAFB',0)
   f.text(x+5,y+12,f'{int(r["rank"]):02}',9,MUTED)
   f.logo(r['company'],x+25,y+2,16)
   size=min(9.1,105/pdfmetrics.stringWidth(r['company_zh'],common.FONT,1))
   f.text(x+47,y+10,r['company_zh'],size,INK)
   country=''.join(ch for ch in r['country_zh'] if not 0x1F1E6<=ord(ch)<=0x1F1FF)
   f.text(x+47,y+21,country,7.2,MUTED)
   bar(f,x+158,y+16,89,float(r['openrank']),167060.26)
   f.text(x+cw-111,y+10,fmt(r['openrank']),9,INK,'right')
   f.text(x+cw-58,y+12,fmt(r['active_repos'],0),8.8,INK,'right')
   f.text(x+cw-5,y+12,fmt(r['active_developers'],0),8.8,INK,'right')
 f.text(0,440,'开发者为企业关联活跃开发者，不等于企业员工；条形从零起，使用同一尺度。',8.5,MUTED)
 return f.caption()

def china_figure():
 f=Figure(p.FIGURES[0],'图 3-2-1',height=248)
 f.text(0,13,'中国企业榜前 10',11,TEAL)
 f.rect(0,23,W,22,PALE,PALE,0)
 for x,s in [(5,'名次 / 企业'),(W-134,'OpenRank'),(W-70,'仓库 / 个'),(W-5,'关联开发者 / 人')]:f.text(x,38,s,8.5,MUTED,'left' if x==5 else 'right')
 for i,r in enumerate(D['chinaCompany']['rows'][:10]):
  y=59+i*16.7
  if i%2==0:f.rect(0,y-11,W,16.7,'#F7FAFB','#F7FAFB',0)
  f.text(5,y,f'{int(r["rank"]):02}',8.5,MUTED);f.logo(r['company'],25,y-10,12)
  f.text(44,y,r['company_zh'],9.1,INK);bar(f,179,y-5,105,float(r['openrank']),141253.65)
  f.text(W-134,y,fmt(r['openrank']),9,INK,'right');f.text(W-70,y,fmt(r['active_repos'],0),9,INK,'right');f.text(W-5,y,fmt(r['active_developers'],0),9,INK,'right')
 return f.caption(True)

def history_panel(f,x,y,w,h,scope,freq,label):
 ds=D[scope+('Year' if freq=='annual' else 'Month')];time='year' if freq=='annual' else 'month'
 rows=[r for r in ds['rows'] if freq!='annual' or r[time]>='2022'];names=p.HISTORY_SELECTION[scope]
 allnames=list(ds['rows'][0])[1:];color=lambda n:COLORS[allnames.index(n)]
 f.text(x,y+12,label,10.5,TEAL)
 for i,n in enumerate(names):
  xx=x+i*w/4;company=next(r['company'] for r in D['company' if scope=='global' else 'chinaCompany']['rows'] if r['company_zh']==n)
  f.logo(company,xx,y+23,11);f.text(xx+16,y+32,n,8.3,color(n))
 left=x+23;right=x+w-58;top=y+52;bottom=y+h-29
 maximum=max(int(r[n]) for r in rows for n in names if r[n]!='');minimum=1
 yy=lambda v:top+(v-minimum)/(maximum-minimum)*(bottom-top)
 xx=lambda i:left+i*(right-left)/(len(rows)-1)
 ticks=sorted(set(round(1+(maximum-1)*i/3) for i in range(4)))
 for v in ticks:
  f.line([(left,yy(v)),(right,yy(v))],LINE,.45);f.text(left-7,yy(v)+3,str(v),8,MUTED,'right')
 for i,r in enumerate(rows):
  label=r[time] if freq=='annual' else r[time][5:]
  f.text(xx(i),bottom+13,label,7.7,MUTED,'center')
 ends=[]
 for n in names:
  points=[]
  for i,r in enumerate(rows):
   if r[n]=='':
    if len(points)>1:f.line(points,color(n),1.5)
    points=[];continue
   xy=(xx(i),yy(int(r[n])));points.append(xy);f.dot(*xy,2,color(n))
  if len(points)>1:f.line(points,color(n),1.5)
  if rows[-1][n]!='':ends.append([yy(int(rows[-1][n])),n,int(rows[-1][n])])
 ends.sort();last=top-12
 for end in ends:end.append(max(end[0],last+13));last=end[3]
 if ends and ends[-1][3]>bottom:
  ends[-1][3]=bottom
  for i in range(len(ends)-2,-1,-1):ends[i][3]=min(ends[i][3],ends[i+1][3]-13)
 for actual,n,v,lab in ends:
  f.line([(right,actual),(right+9,lab),(right+14,lab)],color(n),.8);f.text(right+18,lab+3,str(v),8.5,color(n))

def history_figure():
 f=Figure(p.FIGURES[1],'图 3-2-2',LW,461);cw=(LW-28)/2
 history_panel(f,0,0,cw,198,'global','annual','A  全球企业 · 2022—2026 年度标签')
 history_panel(f,cw+28,0,cw,198,'china','annual','B  中国企业 · 2022—2026 年度标签')
 f.line([(0,204),(LW,204)],LINE,.5)
 history_panel(f,0,215,cw,198,'global','monthly','C  全球企业 · 2025.07—2026.06 月度')
 history_panel(f,cw+28,215,cw,198,'china','monthly','D  中国企业 · 2025.07—2026.06 月度')
 f.text(0,434,'各面板分别标注位次尺度，第 1 名在上；年度起止范围待核验。月度横轴跨 2025 年 7 月至 2026 年 6 月。',8.4,MUTED)
 return f.caption()

def collaboration_figure():
 f=Figure(p.FIGURES[2],'图 3-2-3',height=335);d=p.COLLABORATION
 f.rect(0,0,W,25,'#FFF4DC','#D2B16F',3);f.text(10,17,'模拟 · 企业、项目与数值均为虚构',10,'#765214')
 f.text(0,47,'A  企业 A 的共同项目联系',10.2,TEAL);f.text(268,47,'B  项目内贡献构成 / 已合并 PR',10.2,TEAL)
 center=(113,177);peers=[(113,89),(211,145),(175,244),(51,244),(15,145)]
 for i,(px,py) in enumerate(peers,1):
  count=sum(a>0 and b>0 for a,b in zip(d['counts'][0],d['counts'][i]))
  f.line([center,(px,py)],BLUE,.8+count*.8)
  mx=(px+center[0])/2;my=(py+center[1])/2;f.rect(mx-7,my-8,14,16,'#ffffff','#ffffff',1);f.text(mx,my+3,str(count),9,BLUE,'center')
 for i,(x,y) in enumerate([center,*peers]):f.dot(x,y,14,COLORS[i]);f.text(x,y+3.7,chr(65+i),10.5,'#ffffff','center')
 f.text(0,278,'节点为虚构企业 A—F；线宽表示共同项目数。',8.2,MUTED)
 for i in range(6):
  xx=268+i*39;f.rect(xx,64,7,7,COLORS[i],COLORS[i],1);f.text(xx+11,71,chr(65+i),8.5,MUTED)
 for k in range(6):
  y=99+k*28;total=sum(row[k] for row in d['counts']);f.text(268,y,d['projects'][k],8.7,INK);f.text(W,y,str(total),8.7,INK,'right');off=268
  for i,rs in enumerate(d['counts']):
   if not rs[k]:continue
   width=rs[k]/total*(W-268);f.rect(off,y+5,width,8,COLORS[i],COLORS[i],0);off+=width
 f.text(268,278,'各行按项目总 PR 计算 100%，右侧为总量。',8.2,MUTED)
 f.line([(0,292),(W,292)],LINE,.5);f.text(0,308,'共同贡献不等于正式合作关系；所有模拟值与 Web 示例一致。',8.4,MUTED)
 return f.caption()

class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'3.2 企业影响力 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Section3-2-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/c-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 def interpret(t):head,tail=t.split('。',1);add('**'+head+'。**'+tail)
 add('3.2 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0])
 # A full, readable global ranking follows on its own landscape page.
 story += [NextPageTemplate('landscape'),PageBreak(),vp.FigureFlow(main_figure(),'3-2-1'),NextPageTemplate('portrait'),PageBreak()]
 for t in p.STORIES[0][1][1:]:interpret(t)
 story.append(vp.FigureFlow(china_figure(),'3-2-1-cont'))
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0])
 story += [NextPageTemplate('landscape'),PageBreak(),vp.FigureFlow(history_figure(),'3-2-2'),NextPageTemplate('portrait'),PageBreak()]
 for t in p.STORIES[1][1][1:]:interpret(t)
 add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(vp.FigureFlow(collaboration_figure(),'3-2-3'))
 story.append(PageBreak())
 for t in p.STORIES[2][1][1:]:interpret(t)
 add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE)
 doc=Doc(a.output);doc.title='GOSD 2026 · 3.2 '+p.TITLE;doc.subject='C-Ranking 图文出版样章';doc.build(story)
 pdf=fitz.open(a.output);images={}
 for place in IMAGE_PLACEMENTS:
  name=place['company'];images.setdefault(name,(LOGO_DIR/'assets'/LOGOS[name]['filename']).read_bytes())
  pdf[place['page']].insert_image(fitz.Rect(place['rect']),stream=images[name],keep_proportion=True)
 temp=a.output.with_suffix('.tmp.pdf');pdf.save(temp,garbage=4,deflate=True);pdf.close();temp.replace(a.output)
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':p.EDITION,'logos':IMAGE_PLACEMENTS},ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
