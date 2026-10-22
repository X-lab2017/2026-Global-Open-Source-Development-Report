"""Render source-backed appendices from its canonical Markdown with the report's print typography."""
from pathlib import Path
from urllib.parse import quote
import argparse,hashlib,html,json,re
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Table,TableStyle,KeepTogether,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
from appendix_publication import DIRECTORY,EDITION,PDF_NAME
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'appendices/附录A-指标体系与数据来源.md'
EN_SOURCE=ROOT/'appendices/appendix-a.en.md'
LETTER='A'
TITLE='指标、数据与研究方法'
FONT=common.FONT
WIDTH=A4[0]-92
INK='#18343e';TEAL='#087d80';MUTED='#526b76';LINE='#d4e2e5'
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/'
STYLES={}
def styles():
 b=ParagraphStyle('body',fontName=FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=9,rightIndent=11.2,allowWidows=0,allowOrphans=0)
 STYLES.update(body=b,title=ParagraphStyle('title',parent=b,fontSize=21,leading=30,spaceAfter=15,keepWithNext=True),
  section=ParagraphStyle('section',parent=b,fontSize=14.5,leading=23,spaceBefore=17,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),
  note=ParagraphStyle('note',parent=b,fontSize=9,leading=15,textColor=HexColor(MUTED),spaceAfter=13),
  cell=ParagraphStyle('cell',parent=b,fontSize=9.8,leading=16,spaceAfter=0,rightIndent=0,allowWidows=1,allowOrphans=1))
def destination(href):
 if href.startswith(('https://','http://')):return href
 if href.startswith('/2026/'):return WEB+href.lstrip('/')
 name=Path(href).name
 route={'osdi_indicator_dictionary.csv':'2026/zh/data/indicators/',
        '附录A-指标体系与数据来源.md':'2026/zh/methodology/',
        'cases.json':'assets/gosm/cases.json',
        'dataset_inventory.csv':'assets/report/dataset_inventory.csv',
        'source_register.csv':'assets/report/source_register.csv',
        '附录-开源人工智能数字公共产品-DPG-评估框架.md':'2026/zh/appendices/dpg/'}.get(name)
 return WEB+route if route else 'https://github.com/X-lab2017/2026-Global-Open-Source-Development-Report/blob/main/'+quote(href.lstrip('../'))
def inline(text):
 tokens=[]
 def save(m):
  tokens.append('<link href="'+html.escape(destination(m[2]),quote=True)+'" color="'+TEAL+'">'+html.escape(m[1])+'</link>')
  return '\x00'+str(len(tokens)-1)+'\x00'
 text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',save,text)
 text=html.escape(text)
 text=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)
 text=re.sub(r'\x60([^\x60]+)\x60',r'\1',text)
 return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],text)
def broken_lines(text,width,size):
 # Keep closing punctuation with its phrase; reserve one em for hanging punctuation.
 tokens=re.findall(r'[A-Za-z0-9]+(?:[._/-][A-Za-z0-9]+)*|\s+|.',text)
 lines=[];line=''
 for token in tokens:
  if line and pdfmetrics.stringWidth(line+token,FONT,size)>width and token not in '，。；：、！？）》”’%':
   carry=''
   if line[-1] in '（《“‘':carry=line[-1];line=line[:-1]
   lines.append(line.rstrip());line=carry+token.lstrip()
  else:line+=token
 if line:lines.append(line.rstrip())
 return lines
def para(s,key='body',width=None):
 cls=common.ManuscriptParagraph if key=='body' else Paragraph
 if key in ['body','cell'] and '[' not in s:
  available=(WIDTH-11.2 if key=='body' else width)-STYLES[key].fontSize
  markup='<br/>'.join(html.escape(x) for x in broken_lines(s,available,STYLES[key].fontSize))
 else:markup=inline(s)
 return cls(markup,STYLES[key])
class Document(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=60,bottomMargin=57,title='2026 全球开源发展报告 · 附录 '+LETTER+'：'+TITLE,author='GOSD',pageCompression=1,invariant=1)
  self.headings=[]
  self.addPageTemplates(PageTemplate('appendix',[Frame(46,57,WIDTH,A4[1]-117,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPageEnd=self.draw_page))
 def draw_page(self,c,doc):
  c.saveState();c.setFont(FONT,8.5);c.setFillColor(HexColor(MUTED))
  c.drawString(46,A4[1]-35,'GOSD 2026 / 全球开源发展报告')
  c.drawRightString(A4[0]-46,A4[1]-35,'附录 '+LETTER+' · '+TITLE)
  c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,A4[0]-46,43)
  c.setFont(FONT,8.2);c.drawString(46,28,'2026.10.22 · 与在线正文同源');c.drawRightString(A4[0]-46,28,LETTER+' — '+str(doc.page));c.restoreState()
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='section':
   title=f.getPlainText();key=title.split()[0];self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,0)
   self.headings.append({'text':title,'page':self.page})
def flow():
 lines=SOURCE.read_text().splitlines();out=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('# '):
   out.extend([para('附录 '+LETTER,'note'),para(line[2:].split('：',1)[-1],'title')]);i+=1;continue
  if line.startswith('## '):
   if LETTER=='B' and not line.startswith('## B.1 '):out.append(PageBreak())
   out.append(para(line[3:],'section'));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
    i+=1
   columns=len(rows[0]);widths=([WIDTH*.28,WIDTH*.72] if LETTER=='B' else [WIDTH*.23,WIDTH*.77]) if columns==2 else [WIDTH*.20,WIDTH*.39,WIDTH*.41]
   table=Table([[para(x,'cell',widths[j]-20) for j,x in enumerate(row)] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT',spaceBefore=3,spaceAfter=14)
   table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#edf5f6')),('TEXTCOLOR',(0,0),(-1,0),HexColor(TEAL)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.6,HexColor(LINE)),('LINEBELOW',(0,1),(-1,-1),.35,HexColor(LINE))]))
   out.append(KeepTogether([table]));continue
  parts=[line];i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|')):
   parts.append(lines[i].strip());i+=1
  out.append(para(' '.join(parts)))
 return out
def main():
 global SOURCE,EN_SOURCE,LETTER,TITLE,DIRECTORY,EDITION,PDF_NAME
 p=argparse.ArgumentParser();p.add_argument('--font',type=Path,required=True);p.add_argument('--appendix',choices=['a','b'],default='a');args=p.parse_args()
 if args.appendix=='b':
  import appendix_b_publication as pub
  SOURCE=ROOT/'appendices/附录-开源人工智能数字公共产品-DPG-评估框架.md';EN_SOURCE=ROOT/'appendices/appendix-b.en.md'
  LETTER='B';TITLE='模型开放条件与数字公共品研究参照';DIRECTORY=pub.DIRECTORY;EDITION=pub.EDITION;PDF_NAME=pub.PDF_NAME
 work=ROOT/('tmp/pdfs/appendix-'+args.appendix);work.mkdir(parents=True,exist_ok=True);DIRECTORY.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=SOURCE.read_text()+Path(__file__).read_text());styles()
 pdf=DIRECTORY/PDF_NAME;doc=Document(pdf);doc.build(flow())
 import fitz
 pages=len(fitz.open(pdf))
 manifest={'edition':EDITION,'pages':pages,'pdf_file':PDF_NAME,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'body_font_pt':11.2,'body_leading_pt':18.6,'headings':doc.headings,'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE,EN_SOURCE]}}
 (DIRECTORY/'edition-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
