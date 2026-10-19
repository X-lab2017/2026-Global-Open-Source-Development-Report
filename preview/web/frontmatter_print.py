"""Opening pages and Chapter 1, generated from the same editorial sources as the web."""
from pathlib import Path
import argparse,hashlib,html,json,os,re,shutil
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,PageBreak,Flowable,Spacer,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import fitz,io,xml.etree.ElementTree as ET
from pypdf import PdfReader,PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,NumberObject,TextStringObject
import chapter1_print as common
from chapter1_print import Figure,PrintFigure,paragraph,FONT,PRINT_WIDTH,INK,MUTED,TEAL,BLUE,PURPLE,GREEN,WASH,LINE
import frontmatter_publication as pub
import executive_summary as summary
from declaration_diagram import PRINCIPLES,LAYERS,content as declaration_content
ROOT=Path(__file__).resolve().parents[2]
M=json.loads((ROOT/'preview/content/manifest.json').read_text())
DATA=summary.DATA;ACTION=summary.ACTION
ASSETS=ROOT/'preview/content/report-assets/frontmatter'
INTRO='chapters/引言-人工智能时代的开源发展.md'
CHAPTER=ROOT/'preview/content/report-assets/chapter1/GOSD-2026-chapter1.pdf'
CHAPTER_META=json.loads(CHAPTER.with_name('chapter-manifest.json').read_text())
CHAPTER_FOLIOS={h['text'].split()[0]:h['page'] for h in CHAPTER_META['headings'] if h['level']==1}
SOURCES=['outline/frontmatter-editorial.json','outline/executive-summary.json','outline/执行摘要.md','outline/首页与阅读导引.md','outline/目录.md',INTRO]

def roman(n):
 s=''
 for value,letters in [(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
  while n>=value:s+=letters;n-=value
 return s

def manuscripts():
 for lang,name in [('zh','执行摘要.md'),('en','executive-summary.en.md')]:
  (ROOT/'outline'/name).write_text(summary.manuscript(lang))
 home=['# 2026 全球开源发展报告','从普惠到质量，从参与到影响。',pub.copy('hero_description','zh'),'## 找到你的阅读起点',pub.copy('reading_intro','zh'),pub.copy('reading_route','zh'),'## 连接开源实践与可持续发展',pub.copy('about','zh')]
 (ROOT/'outline/首页与阅读导引.md').write_text('\n\n'.join(home)+'\n')
 toc=['# 目录',pub.copy('contents_intro','zh'),'执行摘要','引言：开源共创智能未来']
 for c in M['chapters']:
  toc+=['## 第'+c['number']+'章 '+c['title']['zh'],'\n'.join('- '+s['number']+' '+s['title']['zh'] for s in c['sections'])]
 toc+=['## 附录','\n'.join('- '+u['title']['zh'] for u in M['back_matter'] if u['kind'] in ['methods','declaration','dpg']),pub.copy('edition_note','zh')]
 (ROOT/'outline/目录.md').write_text('\n\n'.join(toc)+'\n')

def summary_figure(item):
 f=Figure(item['figure_title']['zh'],'图 '+item['figure_id'],height=210)
 kind=item['id'];color={'participation':TEAL,'technology':BLUE,'models':PURPLE,'openness':GREEN}[kind]
 if kind=='participation':
  f.text(0,42,'地区',12,MUTED);f.text(460,42,'开发者（万人）',12,MUTED,'right');f.text(640,42,'OpenRank 位次',12,MUTED,'right')
  maximum=max(r['developers'] for r in item['rows'])
  for i,r in enumerate(item['rows']):
   y=78+i*49;f.text(0,y,r['name']['zh']+' · '+r['country']['zh'],13)
   f.rect(160,y-11,220,9,'#e1e8ec',color,0);f.rect(160,y-11,220*r['developers']/maximum,9,color,color,0)
   f.text(460,y,f'{r["developers"]:.2f}',13,INK,'right');f.text(640,y,'#'+str(r['rank']),14,color,'right')
 elif kind=='technology':
  for i,p in enumerate(item['projects']):
   x=i*220;f.rect(x,33,200,54,WASH,LINE);f.text(x+12,55,p['name'],14);f.text(x+12,74,'OpenRank #'+str(p['rank']),12,color)
  for i,(title,sub) in enumerate([('Agent Infra','智能体基础设施'),('Model Infra','模型基础设施')]):
   x=i*330;f.rect(x,105,310,51,WASH,LINE);f.text(x+12,126,title,13,color);f.text(x+12,144,sub,12)
 elif kind=='models':
  f.text(0,42,'当前快照内，按创建时间回溯',12,MUTED)
  for i,m in enumerate(item['metrics']):
   x=i*330;f.text(x,68,m['name']['zh'],14);f.text(x+310,68,'+'+m['growth'],14,color,'right')
   for j,(key,date) in enumerate([('before','2025-09-13'),('after','2026-09-13')]):
    y=97+j*32;f.text(x,y,date,11.5,MUTED);f.rect(x+82,y-9,140*m[key]/m['after'],8,'#b6a7c4' if j==0 else color,color,0);f.text(x+310,y,f'{m[key]:.2f} 万',12,INK,'right')
  f.text(0,155,'每组按本期数量分别缩放。',11.5,MUTED)
 else:
  for i,q in enumerate(item['questions']):
   x=i*220;f.rect(x,33,200,128,WASH,LINE);f.text(x+100,61,q['title']['zh'],13,color,'center');f.lines(x+14,91,q['body']['zh'],172,12,19)
 f.lines(0,184,item['scope']['zh'],640,11.3,17,MUTED)
 return f.finish()

def declaration_figure():
 f=Figure('宣言的共同愿景、七项原则与行动方向','图 引-1',height=431)
 f.rect(0,32,640,70,WASH,LINE);f.text(320,56,'全球开源与人工智能国际合作宣言',14,INK,'center');f.text(320,82,'时代呼唤 → 共同愿景：开放、包容、安全、可持续',12,MUTED,'center')
 for i,(name,_,indices) in enumerate(LAYERS):
  x=i*220;color=[TEAL,BLUE,GREEN][i]
  f.line([(320,102),(320,117),(x+100,117),(x+100,134)],color,1.1)
  f.rect(x,134,200,195,WASH,color);f.text(x+100,158,name,13,color,'center')
  for j,n in enumerate(indices):
   y=192+j*54;p=PRINCIPLES[n-1];f.text(x+100,y,f'{n:02d}  '+p[0],13,INK,'center');f.text(x+100,y+20,p[2],11.5,MUTED,'center')
  f.line([(x+100,329),(x+100,345),(320,345),(320,359)],color,1.1)
 f.rect(0,359,640,48,WASH,LINE);f.text(320,379,'行动共识：政府、企业、学界与公民社会携手',13,INK,'center');f.text(320,397,'深化 AI 治理、算力共享与人才培育合作',11.5,MUTED,'center')
 return f.finish()

class Cover(Flowable):
 def __init__(self):
  super().__init__();self.width=PRINT_WIDTH;self.height=690
 def draw(self):
  c=self.canv;c.setFillColor(HexColor(TEAL));c.rect(0,671,32,3,fill=1,stroke=0)
  def text(x,y,s,size=12,color=INK):c.setFont(FONT,size);c.setFillColor(HexColor(color));c.drawString(x,y,s)
  text(0,638,'GOSD / 2026',16,TEAL);text(0,586,'全球开源发展报告',30);text(0,557,'GLOBAL OPEN SOURCE DEVELOPMENT REPORT',10.5,MUTED)
  text(0,508,'从普惠到质量，从参与到影响。',17)
  p=paragraph(pub.copy('hero_description','zh'),STYLES['body']);_,h=p.wrap(PRINT_WIDTH,100);p.drawOn(c,0,474-h)
  def svg_image(path,x,y,width):
   raw=Path(path).read_text();xml=ET.fromstring(raw)
   fills=dict(re.findall(r'\.([\w-]+)\s*\{\s*fill:\s*(#[0-9a-fA-F]+);',raw))
   for node in xml.iter():
    if node.get('class') in fills:node.set('fill',fills[node.get('class')])
   doc=fitz.open(stream=ET.tostring(xml),filetype='svg');page=doc[0];height=width*page.rect.height/page.rect.width
   pix=page.get_pixmap(matrix=fitz.Matrix(4,4),alpha=True);c.drawImage(ImageReader(io.BytesIO(pix.tobytes('png'))),x,y,width=width,height=height,mask='auto')
  c.setFillColor(HexColor('#082a42'));c.circle(PRINT_WIDTH/2,263,128,fill=1,stroke=0)
  svg_image(ROOT/'preview/content/assets/cocreation-disc-dark.svg',PRINT_WIDTH/2-111,152,222)
  svg_image(ROOT/'preview/content/assets/ccosi-cn-blue.svg',0,33,148)
  text(PRINT_WIDTH-192,63,'2026 年 10 月 19 日',10,MUTED);text(PRINT_WIDTH-192,40,'前置内容与第一章 · 中文打印版',10,MUTED)

class Contents(Flowable):
 width=PRINT_WIDTH;height=650
 def __init__(self,second=False,page_map=None):super().__init__();self.width=PRINT_WIDTH;self.height=650;self.second=second;self.page_map=page_map or {};self.local_links=[]
 def draw(self):
  c=self.canv;y=624
  def row(title,right='',size=11.2,color=INK,url=None,target=None):
   nonlocal y
   c.setFillColor(HexColor(color));c.setFont(FONT,size);c.drawString(0,y,title)
   if right:c.setFont(FONT,10);c.setFillColor(HexColor(MUTED));c.drawRightString(PRINT_WIDTH,y,right)
   if url:c.linkURL(url,(0,y-3,PRINT_WIDTH,y+14),relative=1,thickness=0)
   if target:self.local_links.append({'front_page':c.getPageNumber()-1,'rect':(*c.absolutePosition(0,y-3),*c.absolutePosition(PRINT_WIDTH,y+14)),'target':target})
   y-=22
  row('全书目录'+('（续）' if self.second else ''),'PDF 页码 / 在线',18)
  if not self.second:
   intro=paragraph(pub.copy('contents_intro','zh'),STYLES['note']);_,h=intro.wrap(PRINT_WIDTH,80);intro.drawOn(c,0,y-h);y-=h+18
   row('执行摘要',roman(self.page_map.get('执行摘要',4)-1),target='summary')
   row('引言：开源共创智能未来',roman(self.page_map.get('引言：开源共创智能未来',8)-1),target='intro');y-=9
  for ch in M['chapters'][3 if self.second else 0:6 if self.second else 3]:
   row('第'+ch['number']+'章 '+ch['title']['zh'],'1' if ch['number']=='1' else '在线',13,TEAL,target='chapter' if ch['number']=='1' else None,url=None if ch['number']=='1' else pub.WEB+'2026/zh/'+ch['route'])
   for s in ch['sections']:
    p=str(CHAPTER_FOLIOS[s['number']]) if s['number'] in CHAPTER_FOLIOS else None
    row(s['number']+' '+s['title']['zh'],p or '',11.2,url=None if p else pub.WEB+'2026/zh/'+ch['route']+'#'+s['id'],target=s['number'] if p else None)
   y-=12
  if self.second:
   row('附录与方法','在线',13,TEAL)
   for u in M['back_matter']:
    if u['kind'] in ['methods','declaration','dpg']:row(u['title']['zh'],'',11.2,url=pub.WEB+'2026/zh/'+u['route'])
   y-=12
   for text in [pub.copy('pdf_scope','zh'),pub.copy('edition_note','zh'),pub.copy('reading_intro','zh'),pub.copy('about','zh')]:
    p=paragraph(text,STYLES['note']);_,h=p.wrap(PRINT_WIDTH,110);p.drawOn(c,0,y-h);y-=h+14

class FrontDoc(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=64,bottomMargin=57,title='2026 全球开源发展报告 · 前置内容与第一章',author='GOSD',pageCompression=1,invariant=1)
  self.headings=[];self.figure_pages={};self.toc_links=[]
  self.addPageTemplates(PageTemplate('front',[Frame(46,57,PRINT_WIDTH,A4[1]-121,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.header,onPageEnd=self.footer))
 def header(self,c,doc):
  if doc.page==1:return
  c.setFont(FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(46,A4[1]-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(A4[0]-46,A4[1]-37,'前置篇目')
 def footer(self,c,doc):
  if doc.page==1:return
  c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,A4[0]-46,43);c.setFont(FONT,8.2);c.setFillColor(HexColor(MUTED));c.drawString(46,28,'从普惠到质量，从参与到影响');c.drawRightString(A4[0]-46,28,roman(doc.page-1))
 def afterFlowable(self,f):
  if isinstance(f,Contents):self.toc_links+=f.local_links
  if isinstance(f,PrintFigure):self.figure_pages[f.fid]=self.page
  if isinstance(f,Paragraph) and f.style.name in ['chapter','section','subsection']:
   level={'chapter':0,'section':1,'subsection':2}[f.style.name];key='front-'+str(len(self.headings));title=f.getPlainText();self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level,False);self.headings.append({'text':title,'page':self.page,'level':level})

STYLES={}
def styles():
 b=ParagraphStyle('body',fontName=FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=9,allowWidows=0,allowOrphans=0)
 STYLES.update(body=b,note=ParagraphStyle('note',parent=b,fontSize=9.7,leading=16,textColor=HexColor(MUTED)),chapter=ParagraphStyle('chapter',parent=b,fontSize=20,leading=29,spaceAfter=16,keepWithNext=True),section=ParagraphStyle('section',parent=b,fontSize=15.5,leading=24,spaceBefore=16,spaceAfter=10,keepWithNext=True),subsection=ParagraphStyle('subsection',parent=b,fontSize=12.6,leading=21,textColor=HexColor(TEAL),spaceBefore=12,spaceAfter=8,keepWithNext=True))
def P(s,key='body'):return paragraph(s,STYLES[key])

def build_front(path,figs,page_map=None):
 story=[Cover(),PageBreak(),Contents(page_map=page_map),PageBreak(),Contents(True,page_map),PageBreak()]
 story += [P('执行摘要','chapter'),P(DATA['headline']['zh'],'section'),P(DATA['lead']['zh']),P(DATA['framework']['zh'])]
 for item,fig in zip(DATA['findings'],figs[:4]):
  story += [P(item['title']['zh'],'section'),P(item['body']['zh']),PrintFigure(fig,item['figure_id']),P('**行动启示：**'+item['implication']['zh'])]
 story += [P('三项共同任务，形成行动方向','section')]
 for task in ACTION['tasks']:story += [P('**'+task['title']['zh']+'。** '+task['body']['zh'])]
 for actor in ACTION['actors']:
  group=[P(actor['title']['zh'],'section')]
  for a in [a for a in ACTION['actions'] if a['actor']==actor['id']]:group.append(P('**'+a['title']['zh']+'：**'+DATA['action_briefs'][a['id']]['zh']))
  story.append(KeepTogether(group))
 story += [P('怎样使用这份报告','section'),P(pub.copy('reading_route','zh')),P(DATA['scope']['zh']),P(DATA['closing']['zh']),PageBreak()]
 raw=(ROOT/INTRO).read_text().split('\n\n');first=next(i for i,b in enumerate(raw) if b.startswith('### '))
 for block in raw[:first]:story.append(P(block[2:],'chapter') if block.startswith('# ') else P(block))
 story += [PrintFigure(figs[4],'引-1'),PageBreak()]
 for i,block in enumerate(raw[first:]):
  block=block.strip()
  if not block:continue
  if block.startswith('### '):story.append(P(block[4:],'section'))
  elif block.startswith('#### '):story.append(P(block[5:],'subsection'))
  elif block.startswith('**原则'):story.append(P(block.strip('*'),'subsection'))
  else:story.append(P(block))
 doc=FrontDoc(path);doc.build(story);return doc

def assemble(front,doc,output):
 r=PdfReader(front);writer=PdfWriter();writer.append(r,import_outline=True);start=len(r.pages);writer.append(CHAPTER,import_outline=True)
 # Contents' printed folios follow the front-matter Roman and chapter Arabic sequences.
 mapping={'summary':next(x['page']-1 for x in doc.headings if x['text']=='执行摘要'),'intro':next(x['page']-1 for x in doc.headings if x['text']=='引言：开源共创智能未来'),'chapter':start,**{number:start+folio-1 for number,folio in CHAPTER_FOLIOS.items()}}
 for link in doc.toc_links:writer.add_annotation(link['front_page'],Link(rect=link['rect'],target_page_index=mapping[link['target']]))
 writer.add_outline_item('封面',0);writer.add_outline_item('目录',1)
 writer.set_page_label(0,0,prefix='封面');writer.set_page_label(1,start-1,style='/r',start=1);writer.set_page_label(start,len(writer.pages)-1,style='/D',start=1)
 writer.add_metadata({'/Title':'2026 全球开源发展报告 · 前置内容与第一章','/Author':'GOSD / 全球开源发展报告','/Subject':'一份完整研究底稿，网页与 PDF 两种编排'})
 with output.open('wb') as f:writer.write(f)
 return start,len(writer.pages)

def main():
 p=argparse.ArgumentParser();p.add_argument('--font',type=Path,required=True);args=p.parse_args()
 manuscripts();work=ROOT/'tmp/pdfs/frontmatter';work.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
 extra=Path(__file__).read_text()+''.join((ROOT/x).read_text() for x in SOURCES)+json.dumps([M,ACTION,PRINCIPLES,LAYERS,declaration_content('zh')],ensure_ascii=False)
 common.font_setup(args.font,work,extra);styles()
 figs=[summary_figure(item) for item in DATA['findings']]+[declaration_figure()]
 for fig,name in zip(figs,['fig-summary-'+x['id'] for x in DATA['findings']]+['fig-intro-1']):(ASSETS/(name+'.svg')).write_text(fig.svg())
 front=work/'front.pdf';doc=build_front(front,figs);doc=build_front(front,figs,{h['text']:h['page'] for h in doc.headings})
 out=ROOT/'output/pdf'/pub.PDF_NAME;out.parent.mkdir(parents=True,exist_ok=True);start,pages=assemble(front,doc,out);shutil.copy2(out,ASSETS/out.name)
 manifest={'edition':pub.EDITION,'pages':pages,'front_pages':start,'chapter_pages':pages-start,'pdf_file':pub.PDF_NAME,'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'chapter1_sha256':hashlib.sha256(CHAPTER.read_bytes()).hexdigest(),'manuscript_sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in SOURCES},'headings':doc.headings,'figure_pages':doc.figure_pages,'body_font_pt':11.2}
 pub.MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
