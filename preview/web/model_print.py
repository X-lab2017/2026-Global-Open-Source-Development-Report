"""Local M-Ranking review PDF; Top 10 display, Top 100 analytical sample."""
from pathlib import Path
import argparse,json,collections,math
import fitz
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import PageBreak
import chapter1_print as common
import vmap_print as vp
from project_print import fittext
import model_publication as p
import gosr_content as g
EDITION='2026-10-21-m-ranking-print-v3'
ROOT=Path(__file__).resolve().parents[1]/'content/gosr'
SNAP=json.loads((ROOT/'model-rankings-snapshot.json').read_text())
REF=json.loads((ROOT/'model-organization-reference.json').read_text())['publishers']
ROWS=SNAP['rows']; W=vp.PWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';CYAN='#279FA9';PALE='#F3F8FA';TRACK='#E1EDF2'
TASKS={'text-generation':'文本生成','image-text-to-text':'多模态理解','text-to-image':'图像生成','robotics':'机器人','automatic-speech-recognition':'语音识别','any-to-any':'全模态生成','fill-mask':'掩码补全','image-text-to-video':'图文生成视频','unidentified':'未识别'}
COLORS=['#156993','#279fa9','#8971b3','#b78229','#5c8a3c','#b76a47','#597fa9','#976880','#7b8991']
fmt=lambda v,d=2:'待补' if v is None else f'{float(v):,.{d}f}'
class Figure(vp.Figure):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.logos=[]
 def logo(self,publisher,x,y,size=15):
  file=REF.get(publisher,{}).get('logo_file')
  if file:self.logos.append((file,x,y,size))
  else:self.text(x+size/2,y+size*.78,'?' if publisher=='未识别' else publisher[:2],7,MUTED,'center')
 def paint(self,c,x,top,width):
  super().paint(c,x,top,width);scale=width/self.width
  for file,px,py,size in self.logos:
   c.drawImage(ImageReader(str(ROOT/'model-org-logos'/file)),x+px*scale,top-(py+size)*scale,width=size*scale,height=size*scale,preserveAspectRatio=True,anchor='c',mask='auto')

def bar(f,x,y,w,value,maximum,color=BLUE):
 f.rect(x,y,w,4,TRACK,TRACK,1)
 if value is not None and value>0:f.rect(x,y,w*value/maximum,4,color,color,1)

def groups(key,rs=ROWS):
 d=collections.defaultdict(list)
 for r in rs:d[r[key]].append(r)
 out=sorted(d.items(),key=lambda kv:(kv[0] in ['未识别','unidentified'],-len(kv[1]),int(kv[1][0]['rank'])))
 result=[];last=None;rank=0
 for i,(k,items) in enumerate(out):
  if len(items)!=last:rank=i+1
  result.append({'key':k,'rows':items,'count':len(items),'rank':None if k in ['未识别','unidentified'] else rank,'top20':sum(int(r['rank'])<=20 for r in items),'best':int(items[0]['rank']),'tasks':len({r['task_tag'] for r in items if r['task_tag']!='unidentified'})});last=len(items)
 return result
TG=groups('task_tag');OG=groups('publisher')

def lead():
 f=Figure(p.FIGURES[0],'图 3-6-1',height=375)
 f.text(0,14,'Top 100 样本 · 原榜前 10 名',11,TEAL);f.rect(0,27,W,23,PALE,PALE,0)
 for x,t,a in [(4,'原榜次 / 模型版本','left'),(326,'ModelRank','right'),(359,'主任务','center'),(430,'衍生数','right'),(W-4,'下载量','right')]:f.text(x,42,t,8.2,MUTED,a)
 for i,r in enumerate(ROWS[:10]):
  y=64+i*27
  if i%2==0:f.rect(0,y-12,W,27,'#F7FAFB','#F7FAFB',0)
  owner,name=r['model_id'].split('/',1) if '/' in r['model_id'] else ('',r['model_id'])
  f.text(4,y+3,f'{r["rank"]:02}',8.7,MUTED);f.logo(r['publisher'],24,y-8,13)
  fittext(f,43,y-3,owner+'/' if owner else '发布账户未识别',184,7.5,MUTED);fittext(f,43,y+10,name,184,9.5)
  bar(f,232,y+1,30,r['modelrank_value'],ROWS[0]['modelrank_value']);f.text(326,y+4,fmt(r['modelrank_value']),9,INK,'right')
  fittext(f,337,y+4,TASKS[r['task_tag']],48,8.2);f.text(430,y+4,fmt(r['n_derivatives'],0),8.7,INK,'right');f.text(W-4,y+4,fmt(r['downloads'],0),8.7,INK,'right')
 f.text(0,334,'ModelRank 衡量复用网络影响力；完整 Top 100 可在 Web 版查询。',8.4,MUTED)
 f.text(0,347,'衍生数与下载量为月记录，非当月新增或独立使用人数；详细统计窗口待补。',8.4,MUTED)
 return f.caption()

def tasks():
 f=Figure(p.FIGURES[1],'图 3-6-2',height=305)
 f.text(0,14,'A  主任务分布 · 同一版本仅计入一个类别',11,TEAL)
 f.text(306,36,'Top 100 / 个',8.5,MUTED,'right');f.text(401,36,'前 20 名 / 个',8.5,MUTED,'right');f.text(W,36,'已识别账户 / 个',8.5,MUTED,'right')
 for i,r in enumerate(TG):
  y=61+i*23;label=TASKS[r['key']];n=r['count'];pubs={x['publisher'] for x in r['rows'] if x['publisher']!='未识别'}
  if i%2==0:f.rect(0,y-13,W,23,'#F7FAFB','#F7FAFB',0)
  f.rect(4,y-7,7,7,COLORS[i],COLORS[i],1);f.text(18,y,label,9.5,INK);bar(f,123,y-4,144,n,52,COLORS[i]);f.text(306,y,str(n),10,INK,'right');f.text(401,y,str(r['top20']),10,INK,'right');f.text(W-4,y,str(len(pubs)),10,INK,'right')
 f.text(0,274,'Top 100 中 1 个版本对应 1%；未知任务保留分母，账户数不可跨任务相加。',8.2,MUTED)
 return f.caption()

def coverage():
 f=Figure(p.FIGURES[1],'图 3-6-2',height=285)
 f.text(0,14,'B  任务 × 发布账户 · 单元格为入榜版本数',11,TEAL)
 pubs=[x['key'] for x in OG[:8]];cols=pubs+['其余账户'];left=109;cw=(W-left)/9
 for j,k in enumerate(cols):fittext(f,left+j*cw+1,40,k,cw-2,7.5,MUTED)
 for i,t in enumerate(TG):
  y=54+i*20;f.text(0,y+13,TASKS[t['key']],8.7,INK)
  for j,k in enumerate(cols):
   n=sum(r['publisher']==k if k!='其余账户' else r['publisher'] not in pubs for r in t['rows'])
   # Darker cells encode more versions; printed integers remain authoritative.
   a=.12+.78*math.sqrt(n/52) if n else 0
   rgb=[int(255*(1-a)+c*a) for c in [21,105,147]];color='#'+''.join(f'{v:02x}' for v in rgb) if n else '#F3F8FA'
   f.rect(left+j*cw,y,cw-4,17,color,color,2);f.text(left+j*cw+(cw-4)/2,y+12,str(n) if n else '—',8.5,'#FFFFFF' if a>.62 else INK,'center')
 f.text(0,250,'前 8 个账户单列，其余含未识别账户；“—”为 0，合计 100 个版本。',8.2,MUTED)
 return f.caption(True)

def organizations():
 f=Figure(p.FIGURES[2],'图 3-6-3',height=320);cw=(W-20)/2
 f.text(0,14,'入榜数量 · 23 个已识别账户及 1 个未识别类别',11,TEAL)
 for j in range(2):
  x=j*(cw+20);f.rect(x,29,cw,22,PALE,PALE,0)
  for xx,t,a in [(x+4,'数量榜次 / 发布账户','left'),(x+cw-65,'版本','right'),(x+cw-32,'前20','right'),(x+cw-3,'任务','right')]:f.text(xx,44,t,7.7,MUTED,a)
  for i,r in enumerate(OG[j*12:(j+1)*12]):
   y=66+i*18.7
   if i%2==0:f.rect(x,y-13,cw,18.7,'#F7FAFB','#F7FAFB',0)
   f.text(x+4,y,str(r['rank']) if r['rank'] else '—',8.1,MUTED);f.logo(r['key'],x+22,y-10,13);fittext(f,x+40,y,r['key'],cw-116,8.7)
   f.text(x+cw-65,y,str(r['count']),9.5,INK,'right');f.text(x+cw-32,y,str(r['top20']),8.7,INK,'right');f.text(x+cw-3,y,str(r['tasks']),8.7,INK,'right')
 f.text(0,293,'同数量并列；账户各自统计，任务数不含未识别类别，不合成组织影响力。',8.1,MUTED)
 return f.caption()

class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第三章 全球开源影响力排行榜');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'3.6 模型 · 2026.10.21');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Section3-6-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/m-ranking');work.mkdir(parents=True,exist_ok=True)
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps([ROWS,REF,TASKS],ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',rightIndent=8,spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=15,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=9,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,spaceBefore=7,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7)};story=[]
 def add(t,style='body'):story.append(common.paragraph(t,styles.get(style,body)))
 def interpret(t):h,t=t.split('。',1);add('**'+h+'。**'+t)
 def figure(f,key):story.append(vp.FigureFlow(f,key))
 add('3.6 '+p.TITLE,'chapter');add(p.INTRO);add('研究问题：'+p.QUESTION);add('指标定位：'+p.POSITION,'note');add('核心发现：'+p.FINDING);add(p.STORIES[0][0],'section');add(p.STORIES[0][1][0]);figure(lead(),'3-6-1-lead')
 story.append(PageBreak())
 for t in p.STORIES[0][1][1:]:interpret(t)
 add(p.STORIES[1][0],'section');add(p.STORIES[1][1][0]);figure(tasks(),'3-6-2-counts')
 for t in p.STORIES[1][1][1:]:interpret(t)
 story.append(PageBreak());figure(coverage(),'3-6-2-coverage');add(p.STORIES[2][0],'section');add(p.STORIES[2][1][0]);figure(organizations(),'3-6-3')
 story.append(PageBreak())
 for t in p.STORIES[2][1][1:]:interpret(t)
 add(p.ACTION_TITLE,'section');add(p.ACTION_INTRO)
 for h,t in p.ACTIONS:add(h,'subsection');add(t)
 add(p.BRIDGE)
 doc=Doc(a.output);doc.title='GOSD 2026 · 3.6 '+p.TITLE;doc.subject='M-Ranking 图文出版样章';doc.build(story)
 (work/'layout.json').write_text(json.dumps({'pages':doc.page,'figures':doc.figures,'paragraphs':doc.locations,'edition':EDITION,'manuscript_edition':p.EDITION,'model_display_rows':10,'analytical_sample_rows':len(ROWS)},ensure_ascii=False,indent=2));print(json.dumps({'pdf':str(a.output),'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
