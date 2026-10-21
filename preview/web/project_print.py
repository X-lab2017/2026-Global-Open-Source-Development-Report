"""P-Ranking review PDF: shared manuscript and unchanged source data."""
from pathlib import Path
import argparse,json,collections,re
import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import region_print as flags
import project_publication as p
import gosr_content as g
D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';PALE='#F3F8FA';TRACK='#E1EDF2';GOLD='#765214'
ROOT=Path(__file__).resolve().parents[1]/'content/gosr'
REF=json.loads((ROOT/'project-reference.json').read_text());SIM=json.loads((ROOT/'project-review-simulated.json').read_text())
COLORS=['#ba613c','#276c8a','#5d8f83','#9b7b39','#726b9e','#b9798a','#6f93a4','#bdc5ca']
Figure=flags.Figure
fmt=lambda v,d=2:f'{float(v):,.{d}f}'
clean=lambda s:re.sub('[\U0001f1e6-\U0001f1ff]','',s)

def bar(f,x,y,w,value,maximum,color=BLUE):
 f.rect(x,y,w,4,TRACK,TRACK,1);f.rect(x,y,w*float(value)/maximum,4,color,color,1)
def fittext(f,x,y,t,width,size=9,color=INK):
 f.text(x,y,t,min(size,width/max(pdfmetrics.stringWidth(t,common.FONT,1),.1)),color)
def country(f,c,x,y,size=8.7):
 c=clean(c) or '未识别'
 if c in flags.FLAGS:f.flag(c,x,y-10,14);f.text(x+19,y,c,size,INK)
 else:f.text(x,y,c,size,MUTED)
def leading():
 f=Figure(p.FIGURES[0],'图 3-4-1',height=245)
 f.text(0,14,'全球榜前五 · 完整 Top 30 见续图',11,TEAL)
 f.text(373,38,'OpenRank',8.8,MUTED,'right');f.text(W,38,'活跃开发者 / 人',8.8,MUTED,'right')
 for i,r in enumerate(D['project']['rows'][:5]):
  y=61+i*32;f.text(0,y,f'{int(r["rank"]):02}',10,MUTED);f.text(24,y,r['project'],10.4,INK)
  country(f,r['country_zh'],200,y,8.7);bar(f,24,y+10,349,r['openrank'],75809.42)
  f.text(373,y,fmt(r['openrank']),10,INK,'right');f.text(W,y,fmt(r['active_developers'],0),10,INK,'right')
 f.text(0,218,'国家沿用原表标签；条形从零起，分值与人数分别阅读。',8.6,MUTED)
 return f.caption()

def global_rank():
 f=Figure(p.FIGURES[0],'图 3-4-1',LW,461);cw=(LW-24)/2
 for j in range(2):
  x=j*(cw+24);f.text(x,13,'全球 Top 30 · '+('1—15' if j==0 else '16—30'),11,TEAL)
  f.rect(x,25,cw,23,PALE,PALE,0)
  for xx,t,a in [(x+4,'原榜次 / 项目','left'),(x+cw-67,'OpenRank','right'),(x+cw-4,'开发者 / 人','right')]:f.text(xx,40,t,8.5,MUTED,a)
  for i,r in enumerate(D['project']['rows'][15*j:15*(j+1)]):
   y=61+i*24.2
   if i%2==0:f.rect(x,y-11,cw,24.2,'#F7FAFB','#F7FAFB',0)
   f.text(x+4,y+1,f'{int(r["rank"]):02}',9,MUTED);c=clean(r['country_zh']) or '未识别'
   if c in flags.FLAGS:f.flag(c,x+26,y-9,14)
   fittext(f,x+46,y,r['project'],126,9.6);fittext(f,x+46,y+10,c+' · '+REF['projects'][r['project']]['domain'],129,7.2,MUTED)
   bar(f,x+178,y-2,43,r['openrank'],75809.42)
   f.text(x+cw-67,y+2,fmt(r['openrank']),8.8,INK,'right');f.text(x+cw-4,y+2,fmt(r['active_developers'],0),8.8,INK,'right')
 f.text(0,433,'国家为原表标签，领域为编辑分类。不同条目可能覆盖重叠仓库，不加总分值与人数。',8.6,MUTED)
 return f.caption(True)

def china_rank():
 f=Figure(p.FIGURES[0],'图 3-4-1',height=337)
 f.text(0,14,'中国 Top 30 · 前十概览',11,TEAL)
 f.rect(0,25,W,23,PALE,PALE,0)
 for x,t,a in [(4,'原榜次 / 项目与组织标签','left'),(373,'OpenRank','right'),(W-4,'开发者 / 人','right')]:f.text(x,40,t,8.5,MUTED,a)
 for i,r in enumerate(D['chinaProject']['rows'][:10]):
  y=62+i*23.9
  if i%2==0:f.rect(0,y-12,W,23.9,'#F7FAFB','#F7FAFB',0)
  f.text(4,y,f'{int(r["rank"]):02}',9,MUTED);f.text(28,y-2,r['project'],10,INK);fittext(f,28,y+8,r['initiator_zh'] or '未识别',191,7.6,MUTED)
  bar(f,228,y-2,68,r['openrank'],75809.42);f.text(373,y,fmt(r['openrank']),9.3,INK,'right');f.text(W-4,y,fmt(r['active_developers'],0),9.3,INK,'right')
 f.text(0,309,'中国榜独立排序；完整 30 项保留于 Web。',8.6,MUTED)
 return f.caption(True)

def distribution():
 f=Figure(p.FIGURES[1],'图 3-4-2',height=700)
 f.text(0,14,'A  国家标签 · Top 100 项目',11,TEAL)
 f.rect(0,25,W,24,PALE,PALE,0)
 f.text(5,41,'数量排名 / 国家',8.8,MUTED);f.text(404,41,'项目数',8.8,MUTED,'right');f.text(W-5,41,'样本占比',8.8,MUTED,'right')
 rows=sorted(D['projectCountries']['rows'],key=lambda r:(clean(r['country_zh'])=='未识别',-int(r['projects_in_top100'])))
 rank=0;last=None
 for i,r in enumerate(rows):
  y=65+i*22;v=int(r['projects_in_top100']);c=clean(r['country_zh']);unknown=c=='未识别'
  if v!=last:rank=i+1
  last=v
  if i%2==0 or unknown:f.rect(0,y-14,W,22,'#F7FAFB','#F7FAFB',0)
  f.text(5,y,'—' if unknown else str(rank),9,MUTED);country(f,c,31,y,9.5)
  bar(f,141,y-4,215,v,69,MUTED if unknown else BLUE)
  f.text(404,y,str(v),10,INK,'right');f.text(W-5,y,str(v)+'%',10,INK,'right')
 f.text(0,356,'独立 Top 100 汇总；未识别保留，同数量并列。',8.6,MUTED)
 f.line([(0,377),(W,377)],LINE,.6)
 f.text(0,402,'B  技术领域 · 全球 Top 30 项目',11,TEAL)
 f.text(0,426,'编辑分类 / 每项一个主领域',8.8,MUTED);f.text(W,426,'项目数 / 样本占比',8.8,MUTED,'right')
 counts=collections.Counter(REF['projects'][r['project']]['domain'] for r in D['project']['rows'])
 rows=sorted([(k,counts[k]) for k in REF['domains'] if counts[k]],key=lambda x:-x[1])
 for i,(name,n) in enumerate(rows):
  y=451+i*26;f.text(0,y,name,10,INK);f.text(W,y,f'{n} 项 · {n/30:.1%}',9.7,INK,'right');bar(f,178,y-4,178,n,8)
 f.text(0,662,'分类覆盖全球详细榜 30 项；与上方 Top 100 国家汇总分别计算。',8.6,MUTED)
 return f.caption()

def rising():
 f=Figure(p.FIGURES[1],'图 3-4-2',height=345)
 f.text(0,14,'中国项目两期记录 · 基期日期待确认',11,TEAL)
 f.rect(0,26,W,24,PALE,PALE,0)
 for x,t,a in [(5,'项目','left'),(178,'基期 → 本期','left'),(355,'位次变化','right'),(W-4,'本期 OpenRank','right')]:f.text(x,42,t,8.7,MUTED,a)
 for i,r in enumerate(D['rising']['rows']):
  y=68+i*24
  if i%2==0:f.rect(0,y-15,W,24,PALE,PALE,0)
  f.text(5,y,r['project'],10,INK);f.text(178,y,r['prev_rank']+' → '+r['cur_rank'],10,INK)
  f.text(355,y,r['rank_delta'],10,TEAL,'right');f.text(W-4,y,fmt(r['openrank']),9.5,INK,'right')
 f.lines(0,313,'“新进”不折算位移；各表保留原始精度，不计算增长率。',W,8.6,12,MUTED)
 return f.caption(True)

def marginal(project,key,labels):
 rows=[r for r in SIM['contribution_records'] if r['project']==project];total=sum(r['merged_prs'] for r in rows)
 return [(v if isinstance(v,str) else v['name'],sum(r['merged_prs'] for r in rows if r[key]==(v if isinstance(v,str) else v['id']))/total*100,COLORS[i%8]) for i,v in enumerate(labels)]
def sim_banner(f,text):
 f.rect(0,0,f.width,25,'#FFF4DC','#D2B16F',3);f.text(10,17,text,10,GOLD)
def contributions():
 f=Figure(p.FIGURES[2],'图 3-4-3',height=328)
 sim_banner(f,'模拟 · 项目名称真实，全部贡献数值与分组非实测')
 for i,c in enumerate(SIM['countries']):
  x=(i%4)*126;y=44+(i//4)*17;f.rect(x,y-8,8,8,COLORS[i],COLORS[i],0);f.text(x+12,y,c,8.3,MUTED)
 f.text(0,82,'全球原榜次 / 项目',8.5,MUTED);f.text(W,82,'合并 PR 份额 · 100%',8.5,MUTED,'right')
 for i,r in enumerate(D['project']['rows'][:10]):
  y=100+i*19.4;f.text(0,y+3,f'{int(r["rank"]):02}',8.8,MUTED);f.text(23,y+3,r['project'],9,INK);x=137
  for name,v,color in marginal(r['project'],'country',SIM['countries']):
   ww=(W-137)*v/100;f.rect(x,y-8,ww,15,color,color,0)
   if v>=12:f.text(x+ww/2,y+3,f'{v:.0f}%',7.4,'#ffffff','center')
   x+=ww
 f.text(0,303,'未识别保留在分母；条形表示贡献者所在地，不表示治理权。',8.5,MUTED)
 return f.caption()

def contribution_detail():
 f=Figure(p.FIGURES[2],'图 3-4-3',height=321)
 sim_banner(f,'模拟 · OpenHarmony 示例 / 同一份 16,000 条合并 PR')
 cw=(W-29)/2
 for j,(key,labels,title) in enumerate([('country',SIM['countries'],'A  贡献者所在地'),('organization',SIM['organizations'],'B  组织与独立贡献者')]):
  x=j*(cw+29);f.text(x,47,title,10.5,TEAL)
  rs=marginal('OpenHarmony',key,labels);rs.sort(key=lambda r:(r[0] in ['未识别','组织未识别'],-r[1]))
  for i,(name,value,color) in enumerate(rs):
   y=70+i*27;f.text(x,y,name,8.8,INK);f.text(x+cw,y,f'{value:.1f}%',9,INK,'right');bar(f,x,y+8,cw,value,100,color)
 f.text(0,294,'两个维度分母相同；已声明独立贡献者与组织未知项分开。',8.5,MUTED)
 return f.caption(True)

class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'3.4 项目影响力 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Section3-4-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/p-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps([D,REF,SIM],ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 def interpret(t):head,tail=t.split('。',1);add('**'+head+'。**'+tail)
 def figure(f,key):story.append(vp.FigureFlow(f,key))
 add('3.4 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);figure(leading(),'3-4-1-lead')
 story.extend([NextPageTemplate('landscape'),PageBreak()]);figure(global_rank(),'3-4-1-full');story.extend([NextPageTemplate('portrait'),PageBreak()])
 for t in p.STORIES[0][1][1:]:interpret(t)
 figure(china_rank(),'3-4-1-china');add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);story.append(PageBreak());figure(distribution(),'3-4-2');story.append(PageBreak());figure(rising(),'3-4-2-rising')
 for t in p.STORIES[1][1][1:]:interpret(t)
 add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(PageBreak());figure(contributions(),'3-4-3');figure(contribution_detail(),'3-4-3-detail');story.append(PageBreak())
 for t in p.STORIES[2][1][1:]:interpret(t)
 add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE)
 doc=Doc(a.output);doc.title='GOSD 2026 · 3.4 '+p.TITLE;doc.subject='P-Ranking 图文出版样章';doc.build(story)
 pdf=fitz.open(a.output);cache={}
 for place in flags.FLAG_PLACEMENTS:
  name=place['country']
  if name not in cache:
   svg=fitz.open(stream=(flags.FLAG_DIR/flags.FLAGS[name]['file']).read_bytes(),filetype='svg');cache[name]=fitz.open(stream=svg.convert_to_pdf(),filetype='pdf')
  pdf[place['page']].show_pdf_page(fitz.Rect(place['rect']),cache[name],0,keep_proportion=True)
 tmp=a.output.with_suffix('.tmp.pdf');pdf.save(tmp,garbage=4,deflate=True);pdf.close();tmp.replace(a.output)
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':p.EDITION},ensure_ascii=False,indent=2))
 print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
