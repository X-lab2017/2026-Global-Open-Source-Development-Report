"""Local E-Ranking review PDF, using the same manuscript and preserved source tables."""
from pathlib import Path
import argparse,json,collections
import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import region_print as flags
from project_print import fittext,clean
import emerging_publication as p
import gosr_content as g
D=g.DATA;W=vp.PWIDTH;LW=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';CYAN='#4B96A0';PALE='#F3F8FA';Figure=flags.Figure
REF=json.loads((Path(__file__).resolve().parents[1]/'content/gosr/emerging-reference.json').read_text())
COLORS=['#276c8a','#ba613c','#5d8f83','#9b7b39','#726b9e','#6f93a4']
SHORT=['AI 基础软件','智能体与 Agent 工具','操作系统与智能终端','应用与游戏平台','桌面环境与开发者工具','教育与开发者服务']
fmt=lambda v,d=2:f'{float(v):,.{d}f}'

def bar(f,x,y,w,value,maximum,color=BLUE):
 f.rect(x,y,w,4,'#E1EDF2','#E1EDF2',1)
 if float(value)>0:f.rect(x,y,w*float(value)/maximum,4,color,color,1)

def repo_lead():
 f=Figure(p.FIGURES[0],'图 3-5-1',height=226)
 f.text(0,14,'新仓库前五 · 完整 Top 30 见续图',11,TEAL)
 f.text(376,36,'OpenRank',8.5,MUTED,'right');f.text(W,36,'活跃开发者 / 人',8.5,MUTED,'right')
 for i,r in enumerate(D['newRepo']['rows'][:5]):
  y=59+i*28;f.text(0,y,f'{int(r["rank"]):02}',9,MUTED);f.text(23,y,r['repo'],9.7,INK)
  bar(f,23,y+10,283,r['openrank'],7047.46);f.text(376,y,fmt(r['openrank']),10,INK,'right');f.text(W,y,fmt(r['active_developers'],0),10,INK,'right')
 f.text(0,202,'单仓库分别排名；创建记录不等于技术首次出现。',8.6,MUTED)
 return f.caption()

def repo_full():
 f=Figure(p.FIGURES[0],'图 3-5-1',LW,461);cw=(LW-22)/2
 for j in range(2):
  x=j*(cw+22);f.text(x,14,'新仓库 Top 30 · '+('1—15' if j==0 else '16—30'),11,TEAL)
  f.rect(x,26,cw,24,PALE,PALE,0)
  for xx,t,a in [(x+4,'原榜次 / 完整仓库路径','left'),(x+253,'OpenRank','right'),(x+298,'开发者 / 人','right'),(x+cw-4,'平台 / 创建日','right')]:f.text(xx,42,t,8.1,MUTED,a)
  for i,r in enumerate(D['newRepo']['rows'][15*j:15*(j+1)]):
   y=63+i*24.5
   if i%2==0:f.rect(x,y-12,cw,24.5,'#F7FAFB','#F7FAFB',0)
   owner,name=r['repo'].split('/',1);f.text(x+4,y+3,f'{int(r["rank"]):02}',8.8,MUTED)
   fittext(f,x+24,y-3,owner+'/',159,7.5,MUTED);fittext(f,x+24,y+9,name,159,8.8)
   bar(f,x+189,y+1,17,r['openrank'],7047.46);f.text(x+253,y+4,fmt(r['openrank']),8.5,INK,'right');f.text(x+298,y+4,fmt(r['active_developers'],0),8.5,INK,'right')
   f.text(x+cw-4,y-3,r['platform'],7.5,MUTED,'right');f.text(x+cw-4,y+9,r['created_at'],7.2,INK,'right')
 f.text(0,438,'创建日期沿用原表；迁移、镜像与分叉需另行核验。条形从零起，原榜名次保留。',8.6,MUTED)
 return f.caption(True)

def project_rank(start,end):
 n=end-start;step=19 if n<=10 else 18;h=81+n*step
 f=Figure(p.FIGURES[1],'图 3-5-2',height=h)
 f.text(0,14,f'新项目 Top 30 · {start+1}—{end}',11,TEAL);f.rect(0,26,W,24,PALE,PALE,0)
 for x,t,a in [(4,'原榜次 / 项目','left'),(255,'纳入仓库','right'),(337,'OpenRank','right'),(402,'开发者 / 人','right'),(W-4,'首仓创建日','right')]:f.text(x,42,t,8.4,MUTED,a)
 for i,r in enumerate(D['newProject']['rows'][start:end]):
  y=64+i*step
  if i%2==0:f.rect(0,y-13,W,step,'#F7FAFB','#F7FAFB',0)
  f.text(4,y,f'{int(r["rank"]):02}',8.8,MUTED);c=clean(r['country_zh'])
  if c in flags.FLAGS:f.flag(c,24,y-9,12)
  else:f.text(25,y,'—',8,MUTED)
  fittext(f,43,y,r['project'],157,9.6);f.text(255,y,r['repo_count'],9.1,INK,'right');f.text(337,y,fmt(r['openrank']),9.1,INK,'right');f.text(402,y,fmt(r['active_developers'],0),9.1,INK,'right');f.text(W-4,y,r['first_repo_created_at'],8.1,INK,'right')
 # Keep an explicit unknown label without repeating a country column on every row.
 f.text(0,h-20,'国旗沿用原表国家标签；“—”表示未识别。项目范围及资格沿用原表。',8.1,MUTED)
 return f.caption(start>0)

def structures():
 f=Figure(p.FIGURES[2],'图 3-5-3',height=685)
 f.text(0,14,'A  新仓库领域 · 原表汇总',11,TEAL);f.text(335,14,'B  主要语言 · 原表汇总',11,TEAL)
 f.text(0,37,'各以新仓库 Top 30 为分母',8.6,MUTED);f.text(308,37,'数量 / 占比',8.6,MUTED,'right');f.text(W,37,'数量 / 占比',8.6,MUTED,'right')
 for i,r in enumerate(D['domains']['rows']):
  y=61+i*23;f.text(0,y,SHORT[i],9.1,INK);bar(f,143,y-4,91,r['repo_count'],18);f.text(308,y,f'{r["repo_count"]} · {r["share_pct"]}',9,INK,'right')
 for i,r in enumerate(D['languages']['rows']):
  y=61+i*23;f.text(335,y,r['language'],9.1,INK);bar(f,398,y-4,40,r['repo_count'],15);f.text(W,y,f'{r["repo_count"]} · {r["share_pct"]}',9,INK,'right')
 f.line([(0,200),(W,200)],LINE,.6)
 f.text(0,224,'C  同一编辑分类 · 仓库与项目分别计数',11,TEAL)
 f.text(292,246,'仓库 / 30',8.6,MUTED,'right');f.text(W,246,'项目 / 30',8.6,MUTED,'right')
 counts={d:collections.Counter(REF[k][r[D[d]['label']]]['domain'] for r in D[d]['rows']) for d,k in [('newRepo','repos'),('newProject','projects')]}
 for i,domain in enumerate(REF['domains']):
  y=268+i*23;f.text(0,y,SHORT[i],9.1,INK)
  for x,right,d,color in [(146,292,'newRepo',BLUE),(352,W,'newProject',CYAN)]:
   n=counts[d][domain];bar(f,x,y-4,right-x-29,n,30,color);f.text(right,y,str(n),9.5,INK,'right')
 f.text(0,405,'编辑分类每项一个主领域；赏金挑战仓库归入开发者服务，不改写原表。',8.3,MUTED)
 f.line([(0,424),(W,424)],LINE,.6)
 f.text(0,448,'D  本期名单的创建批次 · 每月左仓库、右项目',11,TEAL)
 months=[f'{2025 if i<6 else 2026}-{i+7 if i<6 else i-5:02}' for i in range(12)]
 left,right,top,bottom=23,W-7,468,573;step=(right-left)/12
 for value in [0,3,6,9]:
  y=bottom-value/9*(bottom-top);f.line([(left,y),(right,y)],LINE,.4);f.text(left-8,y+3,str(value),8,MUTED,'right')
 for i,month in enumerate(months):
  x=left+(i+.5)*step
  for j,(d,k,datekey) in enumerate([('newRepo','repos','created_at'),('newProject','projects','first_repo_created_at')]):
   total=0
   for q,domain in enumerate(REF['domains']):
    n=sum(1 for r in D[d]['rows'] if r[datekey].startswith(month) and REF[k][r[D[d]['label']]]['domain']==domain)
    if n:f.rect(x-13+j*14,bottom-(total+n)/9*(bottom-top),11,n/9*(bottom-top),COLORS[q],COLORS[q],0)
    total+=n
   if total:f.text(x-7.5+j*14,bottom-total/9*(bottom-top)-4,str(total),7.6,INK,'center')
  f.text(x,bottom+14,month[2:],7.7,MUTED,'center')
 for i,label in enumerate(SHORT):
  x=(i%3)*170;y=612+(i//3)*17;f.rect(x,y-8,8,8,COLORS[i],COLORS[i],0);f.text(x+13,y,label,7.9,MUTED)
 f.text(0,654,'创建批次仅回溯本期名单；项目采用首仓创建月，空月不代表生态没有新建对象。',8.3,MUTED)
 return f.caption()

class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'3.5 新势力 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Section3-5-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/e-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps([D,REF],ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 def interpret(t):h,t=t.split('。',1);add('**'+h+'。**'+t)
 def figure(f,key):story.append(vp.FigureFlow(f,key))
 add('3.5 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);figure(repo_lead(),'3-5-1-lead')
 story.extend([NextPageTemplate('landscape'),PageBreak()]);figure(repo_full(),'3-5-1-full');story.extend([NextPageTemplate('portrait'),PageBreak()])
 for t in p.STORIES[0][1][1:]:interpret(t)
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);figure(project_rank(0,10),'3-5-2-top');story.append(PageBreak());figure(project_rank(10,30),'3-5-2-rest')
 for t in p.STORIES[1][1][1:]:interpret(t)
 add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);story.append(PageBreak());figure(structures(),'3-5-3');story.append(PageBreak())
 for t in p.STORIES[2][1][1:]:interpret(t)
 add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE)
 doc=Doc(a.output);doc.title='GOSD 2026 · 3.5 '+p.TITLE;doc.subject='E-Ranking 图文出版样章';doc.build(story)
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
