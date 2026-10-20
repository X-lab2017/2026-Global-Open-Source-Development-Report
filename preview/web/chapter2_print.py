"""Assemble the reviewed sections without reflowing their accepted figure pages."""
from pathlib import Path
import argparse, io, json, hashlib
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Spacer
import chapter1_print as common
import goso_intro as intro
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'content/report-assets/chapter2'
PDF_NAME='GOSD-2026-chapter2.pdf'
EDITION='2026-10-20-chapter2-acceptance'
MAPS=['vmap','cmap','imap','tmap','amap','dmap','gmap']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);args=ap.parse_args()
 work=ROOT.parent/'tmp/pdfs/chapter2';work.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
 paths=[ROOT/f'content/{m}/print/GOSD-2026-section-2-{i}.pdf' for i,m in enumerate(MAPS,1)]
 readers=[PdfReader(p) for p in paths];starts=[];offset=2
 for r in readers:starts.append(offset+1);offset+=len(r.pages)
 common.font_setup(args.font,work,subset_text=intro.manuscript()+'本章目录阅读说明第二章全球开源生态观测地图完整打印版页0123456789')
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(common.INK),wordWrap='CJK',spaceAfter=9)
 heading=ParagraphStyle('heading',parent=body,fontSize=16,leading=24,spaceAfter=16)
 sub=ParagraphStyle('sub',parent=body,fontSize=12.6,leading=21,textColor=HexColor(common.TEAL),spaceBefore=10,spaceAfter=8)
 story=[]
 def add(t,style=body):story.append(common.paragraph(t,style))
 add(intro.TITLE,heading);add(intro.QUESTION,sub);add(intro.INTRO);add('本章主要观察',sub)
 for title,text,*_ in intro.FINDINGS:add('**'+title+'。**'+text)
 story.append(PageBreak());add('本章目录与阅读说明',heading);add(intro.READING)
 links=[]
 for i,((code,title,question),start) in enumerate(zip(intro.TOPICS,starts),1):
  add(f'2.{i} {title}（{code}） · {start}');add(question)
 add('阅读说明',sub)
 for t in intro.SCOPE:add(t)
 def frame(c,doc):
  w,h=c._pagesize;c.setFillColor(HexColor(common.TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(common.MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(common.LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'第二章 · 完整打印版');c.drawRightString(w-46,28,str(doc.page))
 front=work/'opening.pdf';SimpleDocTemplate(str(front),leftMargin=46,rightMargin=46,topMargin=58,bottomMargin=56).build(story,onFirstPage=frame,onLaterPages=frame)
 assert len(PdfReader(front).pages)==2,'Opening pagination changed; update contents before assembly'
 writer=PdfWriter();writer.append(front);writer.add_outline_item('第二章 全球开源生态观测地图（GOSO）',0);writer.add_outline_item('本章目录与阅读说明',1)
 for i,(reader,start) in enumerate(zip(readers,starts),1):
  writer.append(reader,outline_item=f'2.{i} {intro.TOPICS[i-1][1]}（{intro.TOPICS[i-1][0]}）',import_outline=True)
 # Replace only the section-local folio, retaining all accepted page artwork.
 for i,page in enumerate(writer.pages):
  if i<2:continue
  w,h=float(page.mediabox.width),float(page.mediabox.height);buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(w,h));c.setFillColorRGB(1,1,1);c.rect(w-70,21,35,18,fill=1,stroke=0);c.setFont(common.FONT,8.2);c.setFillColor(HexColor(common.MUTED));c.drawRightString(w-46,28,str(i+1));c.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0])
 # Add contents-page navigation using the actual rendered text positions.
 import fitz
 doc=fitz.open(front)
 for i,start in enumerate(starts,1):
  hits=doc[1].search_for(f'2.{i} ')
  assert hits,f'Missing contents entry {i}'
  y=hits[0];writer.add_annotation(1,Link(rect=(46,float(doc[1].rect.height)-y.y1,549,float(doc[1].rect.height)-y.y0),target_page_index=start-1))
 writer.set_page_label(0,len(writer.pages)-1,style='/D',start=1)
 writer.add_metadata({'/Title':intro.TITLE,'/Subject':'七节完整出版稿；各图保留真实时间窗与数据状态','/Author':'GOSD 报告编制组'})
 out=DEST/PDF_NAME
 with out.open('wb') as f:writer.write(f)
 digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 manifest={'edition':EDITION,'pdf':PDF_NAME,'pages':len(writer.pages),'opening_pages':2,'sections':[{'section':f'2.{i}','map':m,'start_page':s,'pages':len(r.pages),'sha256':digest(p)} for i,(m,s,r,p) in enumerate(zip(MAPS,starts,readers,paths),1)],'pdf_sha256':digest(out)}
 (DEST/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
