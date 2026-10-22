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
import chapter1_print as common
from chapter1_print import Figure,PrintFigure,paragraph,FONT,PRINT_WIDTH,INK,MUTED,TEAL,BLUE,PURPLE,GREEN,WASH,LINE
import frontmatter_publication as pub
import executive_summary as summary
from declaration_diagram import PRINCIPLES,LAYERS,STAGES,content as declaration_content
ROOT=Path(__file__).resolve().parents[2]
M=json.loads((ROOT/'preview/content/manifest.json').read_text())
DATA=summary.DATA
COVER_FONT=FONT
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

def declaration_figure():
 c=declaration_content('zh');f=Figure(c['title'],'',height=461)
 f.rect(0,12,640,98,WASH,LINE);f.text(320,35,c['title'],14,INK,'center')
 f.text(320,55,c['subtitle'],11.5,MUTED,'center')
 for i,stage in enumerate(STAGES[:2]):
  x=166+i*308;f.text(x,77,stage[0],11.5,TEAL,'center');f.text(x,98,stage[2],12,INK,'center')
 f.line([(308,90),(332,90)],TEAL,1);f.line([(328,86),(332,90),(328,94)],TEAL,1)
 f.text(0,131,'核心原则 · 三层框架，七项原则',11.8,MUTED)
 for i,(name,_,indices) in enumerate(LAYERS):
  x=i*220;color=[TEAL,PURPLE,GREEN][i]
  f.line([(320,110),(320,143),(x+100,143),(x+100,156)],color,1.1)
  f.rect(x,156,200,195,WASH,color);f.text(x+100,177,'第'+'一二三'[i]+'层',11.5,color,'center')
  f.text(x+100,198,name,13,INK,'center');f.line([(x+12,210),(x+188,210)],LINE,.7)
  ys=[244,309] if len(indices)==2 else [235,282,329]
  for y,n in zip(ys,indices):
   p=PRINCIPLES[n-1];f.text(x+100,y,f'{n:02d}  '+p[0],12.5,INK,'center');f.text(x+100,y+17,p[2],11.5,MUTED,'center')
  f.line([(x+100,351),(x+100,366),(320,366),(320,379)],color,1.1)
 f.rect(0,379,640,61,WASH,LINE);f.text(320,396,'行动共识',11.5,TEAL,'center')
 f.text(320,416,STAGES[3][2],13,INK,'center')
 f.text(320,432,'政府 · 企业 · 学界 · 公民社会  |  AI 治理 · 算力共享 · 人才培育',11.2,MUTED,'center')
 f.text(320,459,c['closing'],11.5,MUTED,'center')
 return f

class Cover(Flowable):
 """Flat print counterpart of the existing homepage book face."""
 def __init__(self):
  super().__init__();self.width=PRINT_WIDTH;self.height=690
 def draw(self):
  c=self.canv;c.saveState();x,y=c.absolutePosition(0,0);c.translate(-x,-y)
  w,h=A4;c.setFillColor(HexColor('#0a2c49'));c.rect(0,0,w,h,fill=1,stroke=0)
  def text(x,y,s,size=12,color='#ffffff',font=FONT):
   c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x,y,s)
  def svg_image(path,x,y,width):
   raw=Path(path).read_text();xml=ET.fromstring(raw)
   fills=dict(re.findall(r'\.([\w-]+)\s*\{\s*fill:\s*(#[0-9a-fA-F]+);',raw))
   for node in xml.iter():
    if node.get('class') in fills:node.set('fill',fills[node.get('class')])
   doc=fitz.open(stream=ET.tostring(xml),filetype='svg');page=doc[0];height=width*page.rect.height/page.rect.width
   pix=page.get_pixmap(matrix=fitz.Matrix(4,4),alpha=True);c.drawImage(ImageReader(io.BytesIO(pix.tobytes('png'))),x,y,width=width,height=height,mask='auto')
  # Same dark blue, cyan rule, two-line title, wheel and issuer mark as the web book.
  text(54,749,'GOSD',32,font='Helvetica-Bold');text(w-111,752,'2026',20,'#d1e5ed')
  c.setStrokeColor(HexColor('#83bec7'));c.setLineWidth(2);c.line(54,714,w-54,714)
  text(54,620,'全球开源',57,font=COVER_FONT);text(54,538,'发展报告',57,font=COVER_FONT)
  text(57,484,'GLOBAL OPEN SOURCE',13,'#bcd0db');text(57,462,'DEVELOPMENT REPORT',13,'#bcd0db')
  text(56,413,'从普惠到质量，从参与到影响。',15,'#ffffff')
  text(56,383,pub.copy('cover_theme','zh'),11.2,'#bcd0db')
  c.setStrokeColor(HexColor('#30536d'));c.setLineWidth(.8);c.circle(451,154,181,fill=0,stroke=1)
  svg_image(ROOT/'preview/content/assets/cocreation-disc-dark.svg',295,105,244)
  svg_image(ROOT/'preview/content/assets/ccosi-cn-white.svg',54,166,145)
  text(56,134,'INCLUSION · QUALITY',10,'#bcd0db');text(56,115,'PARTICIPATION · IMPACT',10,'#bcd0db')
  text(54,53,pub.copy('cover_note','zh')+'  |  2026.10.20',9.6,'#bcd0db')
  c.restoreState()

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
  row('全书目录'+('（续）' if self.second else ''),'',18)
  if not self.second:
   intro=paragraph(pub.copy('contents_intro','zh'),STYLES['note']);_,h=intro.wrap(PRINT_WIDTH,80);intro.drawOn(c,0,y-h);y-=h+18
   row('执行摘要',roman(self.page_map.get('执行摘要',4)-1),target='summary')
   row('引言：开源共创智能未来',roman(self.page_map.get('引言：开源共创智能未来',8)-1),target='intro');y-=9
  for ch in M['chapters'][3 if self.second else 0:6 if self.second else 3]:
   row('第'+ch['number']+'章 '+ch['title']['zh'],'1' if ch['number']=='1' else '',13,TEAL,target='chapter' if ch['number']=='1' else None,url=None if ch['number']=='1' else pub.WEB+'2026/zh/'+ch['route'])
   for s in ch['sections']:
    p=str(CHAPTER_FOLIOS[s['number']]) if s['number'] in CHAPTER_FOLIOS else None
    row(s['number']+' '+s['title']['zh'],p or '',11.2,url=None if p else pub.WEB+'2026/zh/'+ch['route']+'#'+s['id'],target=s['number'] if p else None)
   y-=12
  if self.second:
   row('附录与方法','',13,TEAL)
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
  c.setFont(FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(46,A4[1]-37,'GOSD 2026 / 全球开源发展报告')
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
 story += [P('执行摘要','chapter')]
 for kind,value in summary.paragraphs('zh'):
  if kind in ['headline','heading']:story.append(P(value,'section'))
  elif kind in ['finding','priority']:story += [P(value[1],'subsection'),P(value[2])]
  elif kind=='scope':story.append(P(value,'note'))
  else:story.append(P(value))
 story.append(PageBreak())
 raw=(ROOT/INTRO).read_text().split('\n\n');first=next(i for i,b in enumerate(raw) if b.startswith('### '))
 for block in raw[:first]:story.append(P(block[2:],'chapter') if block.startswith('# ') else P(block))
 story += [PrintFigure(figs[0],'declaration-overview'),PageBreak()]
 for i,block in enumerate(raw[first:]):
  block=block.strip()
  if not block:continue
  if block.startswith('### '):story.append(P(block[4:],'section'))
  elif block.startswith('#### '):story.append(P(block[5:],'subsection'))
  elif block.startswith('**原则'):story.append(P(block.strip('*'),'subsection'))
  else:story.append(P(block))
 story.append(P('宣言依据报告收录文本；指定来源：飞书文档《全球开源与人工智能国际合作宣言》。英文为本报告译文。','note'))
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
 p=argparse.ArgumentParser();p.add_argument('--font',type=Path,required=True);p.add_argument('--cover-font',type=Path);args=p.parse_args()
 manuscripts();work=ROOT/'tmp/pdfs/frontmatter';work.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
 extra=Path(__file__).read_text()+''.join((ROOT/x).read_text() for x in SOURCES)+json.dumps([M,DATA,PRINCIPLES,LAYERS,declaration_content('zh')],ensure_ascii=False)
 common.font_setup(args.font,work,extra);styles()
 global COVER_FONT
 if args.cover_font:
  cover_work=work/'cover-font';cover_work.mkdir(exist_ok=True)
  common.font_setup(args.cover_font,cover_work,font_name='GOSDCover',subset_text='全球开源发展报告');COVER_FONT='GOSDCover'
 figs=[declaration_figure()]
 (ASSETS/'declaration-overview.svg').write_text(figs[0].svg())
 for old in [*ASSETS.glob('fig-summary-*.svg'),ASSETS/'fig-intro-1.svg']:old.unlink(missing_ok=True)
 front=work/'front.pdf';doc=build_front(front,figs);doc=build_front(front,figs,{h['text']:h['page'] for h in doc.headings})
 out=ROOT/'output/pdf'/pub.PDF_NAME;out.parent.mkdir(parents=True,exist_ok=True);start,pages=assemble(front,doc,out);shutil.copy2(out,ASSETS/out.name)
 manifest={'edition':pub.EDITION,'pages':pages,'front_pages':start,'chapter_pages':pages-start,'pdf_file':pub.PDF_NAME,'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'chapter1_sha256':hashlib.sha256(CHAPTER.read_bytes()).hexdigest(),'manuscript_sha256':{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in SOURCES},'headings':doc.headings,'figure_pages':doc.figure_pages,'body_font_pt':11.2}
 pub.MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
