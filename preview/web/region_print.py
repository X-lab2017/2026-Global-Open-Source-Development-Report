"""Local review PDF for the GOSR opening and section 3.1; does not publish assets."""
from pathlib import Path
import argparse,json,hashlib
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import region_publication as p
import gosr_content as g
D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
fmt=lambda v:f'{float(v):,.2f}'
def global_figure():
 f=vp.Figure(p.FIGURES[0],'图 3-1-1',LW,456)
 for j in range(2):
  x=j*(LW/2+8);ww=LW/2-17
  f.text(x,12,'全球行政区 Top 30'+('（续）' if j else ''),10.5,INK)
  for xx,txt,align in [(x,36,'left')]:pass
  f.text(x,35,'原榜次 / 地区',8.5,MUTED);f.text(x+ww-80,35,'OpenRank',8.5,MUTED,'right');f.text(x+ww,35,'开发者 / 万',8.5,MUTED,'right')
  for i,r in enumerate(D['region']['rows'][j*15:(j+1)*15]):
   y=56+i*24;name=r['province_zh'];f.text(x,y,f'{int(r["rank"]):02}  '+name,9,INK);f.text(x+ww-80,y,fmt(r['openrank']),9,INK,'right');f.text(x+ww,y,fmt(r['developer_count_10k']),9,INK,'right')
   f.line([(x+20,y+6),(x+20+(ww-110)*float(r['openrank'])/50883.8,y+6)],'#156993',2)
 f.text(0,430,'口径与来源',8.5,TEAL)
 return f.caption()
def countries_figure():
 f=vp.Figure(p.FIGURES[1],'图 3-1-2',height=241)
 rs=D['regionCountries']['rows'];top=sorted(rs,key=lambda r:-int(r['entries_in_top100']));leaders=top[:13]
 f.text(0,13,'入榜行政区数量 / 个',9,MUTED);f.text(W,13,'Top 100 · 32 国',9,MUTED,'right')
 for j in range(2):
  for i,r in enumerate(leaders[j*7:(j+1)*7]):
   x=j*(W/2+10);y=37+i*23;v=int(r['entries_in_top100']);f.text(x,y,r['country_zh'],9,INK);f.rect(x+48,y-9,v/25*145,10,'#156993','#156993',0);f.text(x+207,y,str(v),9,INK,'right')
 f.text(0,208,'其余 19 国各有 1 个行政区入榜；五个入榜最多的国家合计 61 个。',8.5,MUTED)
 return f.caption()
def china_figure():
 f=vp.Figure(p.FIGURES[2],'图 3-1-3',height=365)
 left=220;right=252
 f.text(0,13,'A  中国省级榜前 10',10.5,INK);f.text(left,32,'OpenRank',8.5,MUTED,'right')
 for i,r in enumerate(D['province']['rows'][:10]):
  y=51+i*18;v=float(r['openrank']);f.text(0,y,f'{int(r["rank"]):02} '+r['province_zh'],9,INK);f.text(left,y,fmt(v),9,INK,'right');f.line([(78,y-3),(78+66*v/10188.3,y-3)],'#156993',3)
 f.text(right,13,'B  广东与浙江的入榜城市',10.5,INK)
 for k,province in enumerate(['广东省','浙江省']):
  yy=38+k*104;r=next(r for r in D['province']['rows'] if r['province_zh']==province)
  f.text(right,yy,province+f' · 省级第 {r["rank"]} 名',9.5,TEAL)
  cs=[r for r in D['city']['rows'] if r['province_zh']==province]
  for i,c in enumerate(cs):
   y=yy+20+i*20;f.text(right+10,y,f'{int(c["rank"]):02} '+c['city'],9,INK);f.text(W,y,fmt(c['openrank']),9,INK,'right')
 f.line([(0,235),(W,235)],LINE,.5);f.text(0,253,'C  全国城市榜前 10 · 原榜次与 OpenRank',10,INK)
 for i,r in enumerate(D['city']['rows'][:10]):
  x=(i//5)*(W/2+10);y=274+(i%5)*16
  f.text(x,y,f'{int(r["rank"]):02} '+r['city'],8.8,INK);f.text(x+W/2-20,y,fmt(r['openrank']),8.8,INK,'right')
 return f.caption()
class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'章首与 3.1 样章 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Chapter3-Opening-Section3-1-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/r-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+str(p.CHAPTER_TOPICS)+json.dumps({k:D[k] for k in ['region','province','city','regionCountries']},ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 add(p.CHAPTER_TITLE,'chapter');add(p.CHAPTER_QUESTION,'section');add(p.CHAPTER_INTRO);add('本章主要观察','section')
 for h,t in p.CHAPTER_FINDINGS:add('**'+h+'。**'+t)
 add('本章主题','section')
 for i,(code,title,desc) in enumerate(p.CHAPTER_TOPICS,1):add(f'3.{i} {title}（{code}-Ranking） · {desc}','note')
 add(p.PERIOD,'note');story.append(PageBreak())
 add('3.1 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);story += [NextPageTemplate('landscape'),PageBreak(),vp.FigureFlow(global_figure(),'3-1-1'),NextPageTemplate('portrait'),PageBreak()]
 for t in p.STORIES[0][1][1:]:add(t)
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);story.append(vp.FigureFlow(countries_figure(),'3-1-2'))
 for t in p.STORIES[1][1][1:]:add(t)
 story.append(PageBreak());add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(vp.FigureFlow(china_figure(),'3-1-3'))
 for t in p.STORIES[2][1][1:]:add(t)
 story.append(PageBreak());add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE);doc=Doc(a.output);doc.build(story)
 import fitz
 pdf=fitz.open(a.output)
 for pg in pdf:
  for r in pg.search_for('口径与来源'):pg.insert_link({'kind':fitz.LINK_URI,'from':r,'uri':'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/03/#fig-3-1-1'})
 pdf.saveIncr()
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':p.EDITION},ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
