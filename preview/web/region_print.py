"""Local review PDF for the GOSR opening and section 3.1; does not publish assets."""
from pathlib import Path
import argparse,json,hashlib
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import region_publication as p
import gosr_content as g
D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
fmt=lambda v:f'{float(v):,.2f}'
FLAG_DIR=Path(__file__).resolve().parents[1]/'content/gosr/flags'
FLAGS=json.loads((FLAG_DIR/'provenance.json').read_text())['countries']
FLAG_PLACEMENTS=[]
BLUE='#156993';PALE='#F3F8FA';TRACK='#E1EDF2'
class Figure(vp.Figure):
 def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.flags=[]
 def flag(self,country,x,y,w=15):
  country=''.join(c for c in country if not 0x1F1E6<=ord(c)<=0x1F1FF).strip()
  assert country in FLAGS,country
  self.flags.append((country,x,y,w,w*.75))
 def paint(self,c,x,top,width):
  super().paint(c,x,top,width);scale=width/self.width
  for country,px,py,w,h in self.flags:
   ax,ay=c.absolutePosition(x+px*scale,top-py*scale)
   FLAG_PLACEMENTS.append({'page':c.getPageNumber()-1,'country':country,'rect':[ax,c._pagesize[1]-ay,ax+w*scale,c._pagesize[1]-ay+h*scale]})
def bar(f,x,y,w,value,maximum,color=BLUE):
 f.rect(x,y,w,4,TRACK,TRACK,1)
 f.rect(x,y,w*value/maximum,4,color,color,1)
def topic_guide():
 f=Figure('','',height=199);cw=(W-24)/2
 for i,(code,title,desc) in enumerate(p.CHAPTER_TOPICS):
  x=(i%2)*(cw+24);y=(i//2)*65
  f.line([(x,y+1),(x+cw,y+1)],LINE,.6)
  f.text(x,y+18,f'3.{i+1}  {code}-Ranking',8.7,MUTED)
  f.text(x,y+38,title,12,TEAL);f.text(x+53,y+38,desc,9.2,INK)
 return f

def global_figure():
 f=Figure(p.FIGURES[0],'图 3-1-1',LW,461)
 cw=(LW-24)/2
 for j in range(2):
  x=j*(cw+24)
  f.text(x,13,'全球行政区 Top 30'+(' · 16—30' if j else ' · 1—15'),11,TEAL)
  f.rect(x,25,cw,22,PALE,PALE,0)
  f.text(x+5,40,'名次 / 地区与国家',8.7,MUTED)
  f.text(x+cw-67,40,'OpenRank',8.7,MUTED,'right');f.text(x+cw-5,40,'开发者 / 万',8.7,MUTED,'right')
  for i,r in enumerate(D['region']['rows'][j*15:(j+1)*15]):
   y=52+i*24.7;v=float(r['openrank']);country=r['country_zh'];name=r['province_zh']
   if i%2==0:f.rect(x,y-1,cw,24.7,'#F7FAFB','#F7FAFB',0)
   f.text(x+5,y+12,f'{int(r["rank"]):02}',9,TEAL if int(r['rank'])<4 else MUTED)
   f.flag(country,x+24,y+3,15)
   fs=min(9.2,106/pdfmetrics.stringWidth(name,common.FONT,1))
   f.text(x+46,y+10,name,fs,INK);f.text(x+46,y+21,country,7.1,MUTED)
   bar(f,x+158,y+9,62,v,50883.8)
   f.text(x+cw-67,y+13,fmt(v),9.1,INK,'right')
   f.text(x+cw-5,y+13,fmt(r['developer_count_10k']),9.1,INK,'right')
 f.line([(0,428),(LW,428)],LINE,.5);f.text(0,442,'口径与来源',8.4,TEAL)
 return f.caption()

def countries_figure():
 f=Figure(p.FIGURES[1],'图 3-1-2',height=255)
 top=sorted(D['regionCountries']['rows'],key=lambda r:-int(r['entries_in_top100']))
 rows=top[:13]+[{'country_zh':'其余 19 国','entries_in_top100':19}];cw=(W-24)/2
 f.text(0,13,'入榜行政区数量 / 个',9,MUTED);f.text(W,13,'Top 100 · 32 国',9,MUTED,'right')
 for j in range(2):
  for i,r in enumerate(rows[j*7:(j+1)*7]):
   x=j*(cw+24);y=35+i*25;v=int(r['entries_in_top100']);rest=r['country_zh'].startswith('其余')
   if i%2==0:f.rect(x,y-11,cw,25,PALE,PALE,0)
   if not rest:f.flag(r['country_zh'],x+4,y-6,13)
   f.text(x+22,y+3,r['country_zh'],8.8,INK)
   bar(f,x+79,y-2,cw-109,v,25,MUTED if rest else BLUE)
   f.text(x+cw-6,y+3,str(v),9.3,INK,'right')
 f.text(0,221,'其余 19 国各有 1 个入榜行政区，合并显示；同数量国家并列。',8.4,MUTED)
 return f.caption()

def china_figure():
 f=Figure(p.FIGURES[2],'图 3-1-3',height=365);left=222;right=252
 f.text(0,13,'A  中国省级榜前 10',10.5,TEAL);f.text(left,32,'OpenRank',8.5,MUTED,'right')
 for i,r in enumerate(D['province']['rows'][:10]):
  y=51+i*18;v=float(r['openrank'])
  if i%2==0:f.rect(0,y-11,left,18,PALE,PALE,0)
  f.text(4,y,f'{int(r["rank"]):02}',8.6,MUTED);f.text(23,y,r['province_zh'],9,INK)
  bar(f,83,y-5,63,v,10188.3);f.text(left-4,y,fmt(v),9,INK,'right')
 f.text(right,13,'B  广东与浙江的入榜城市',10.5,TEAL);f.text(W,13,'OpenRank',8.5,MUTED,'right')
 for k,province in enumerate(['广东省','浙江省']):
  yy=38+k*101;r=next(r for r in D['province']['rows'] if r['province_zh']==province)
  f.rect(right,yy-14,W-right,95,PALE,PALE,4)
  f.text(right+9,yy,province+f' · 省级第 {r["rank"]} 名',9.5,TEAL)
  cs=[r for r in D['city']['rows'] if r['province_zh']==province]
  for i,c in enumerate(cs):
   y=yy+22+i*22;f.text(right+9,y,f'{int(c["rank"]):02}',8.6,MUTED);f.text(right+29,y,c['city'],9,INK)
   f.text(W-9,y,fmt(c['openrank']),9,INK,'right')
 f.line([(0,235),(W,235)],LINE,.5);f.text(0,253,'C  全国城市榜前 10 · 原榜次与 OpenRank',10,TEAL)
 cw=(W-24)/2
 for i,r in enumerate(D['city']['rows'][:10]):
  x=(i//5)*(cw+24);y=274+(i%5)*16
  f.text(x,y,f'{int(r["rank"]):02}',8.5,MUTED);f.text(x+23,y,r['city'],8.8,INK)
  bar(f,x+87,y-4,64,float(r['openrank']),9616.14)
  f.text(x+cw,y,fmt(r['openrank']),8.8,INK,'right')
 return f.caption()
class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,('第三章 / GOSR' if doc.page==1 else '3.1 地区')+' · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Chapter3-Opening-Section3-1-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/r-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+str(p.CHAPTER_TOPICS)+json.dumps({k:D[k] for k in ['region','province','city','regionCountries']},ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 add(p.CHAPTER_TITLE,'chapter');add(p.CHAPTER_QUESTION,'section');add(p.CHAPTER_INTRO);add('本章主要观察','section')
 for h,t in p.CHAPTER_FINDINGS:add('**'+h+'。**'+t)
 add('本章主题','section')
 story.append(vp.FigureFlow(topic_guide(),'chapter-topics'))
 add(p.PERIOD,'note');story.append(PageBreak())
 add('3.1 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);story += [NextPageTemplate('landscape'),PageBreak(),vp.FigureFlow(global_figure(),'3-1-1'),NextPageTemplate('portrait'),PageBreak()]
 for t in p.STORIES[0][1][1:]:add('**'+t.split('。',1)[0]+'。**'+t.split('。',1)[1])
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);story.append(vp.FigureFlow(countries_figure(),'3-1-2'))
 for t in p.STORIES[1][1][1:]:add('**'+t.split('。',1)[0]+'。**'+t.split('。',1)[1])
 story.append(PageBreak());add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(vp.FigureFlow(china_figure(),'3-1-3'))
 for t in p.STORIES[2][1][1:]:add('**'+t.split('。',1)[0]+'。**'+t.split('。',1)[1])
 story.append(PageBreak());add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE);doc=Doc(a.output);doc.title=p.CHAPTER_TITLE+' · 3.1 样章';doc.subject='第三章章首与 R-Ranking 出版样章 · 图文同步修订';doc.build(story)
 import fitz
 pdf=fitz.open(a.output)
 for pg in pdf:
  for r in pg.search_for('口径与来源'):pg.insert_link({'kind':fitz.LINK_URI,'from':r,'uri':'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/03/#fig-3-1-1'})
 cache={}
 for placement in FLAG_PLACEMENTS:
  country=placement['country']
  if country not in cache:
   raw=(FLAG_DIR/FLAGS[country]['file']).read_bytes();svg=fitz.open(stream=raw,filetype='svg');cache[country]=fitz.open(stream=svg.convert_to_pdf(),filetype='pdf')
  pdf[placement['page']].show_pdf_page(fitz.Rect(placement['rect']),cache[country],0,keep_proportion=True)
 temp=a.output.with_suffix('.tmp.pdf');pdf.save(temp,garbage=4,deflate=True);pdf.close();temp.replace(a.output)
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':p.EDITION,'flags':FLAG_PLACEMENTS},ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
