"""Assemble the private Chapter 5 review with shared opening, running pages and bookmarks.

Section PDFs come from their existing generators; rendered files stay outside git.
"""
from pathlib import Path
from io import BytesIO
import argparse,json
import fitz
from lxml import etree
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import chapter1_print as common
import gosm_opening_content as P
import gosm_supply_content as S51

def main():
    ap=argparse.ArgumentParser()
    for name in ['font','output','work','framework','s51','s52','s53']:ap.add_argument('--'+name,type=Path,required=True)
    a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
    source=a.framework.read_bytes()
    common.font_setup(a.font,a.work,subset_text=P.manuscript()+''.join(S51.NOTES)+source.decode()+Path(__file__).read_text())
    root=etree.fromstring(source)
    for node in root.iter():
        node.attrib.pop('style',None)
        if etree.QName(node).localname=='text':node.set('font-family',common.FONT)
    fig=svg2rlg(BytesIO(etree.tostring(root)));scale=(A4[0]-92)/fig.width;fig.scale(scale,scale);fig.width*=scale;fig.height*=scale
    body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(common.INK),wordWrap='CJK',spaceAfter=10)
    styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=20,leading=30,spaceAfter=12),'heading':ParagraphStyle('heading',parent=body,fontSize=14,leading=23,spaceAfter=12,textColor=HexColor(common.TEAL)),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=10)}
    layout=[]
    def draw_page(c,items,footer):
        w,h=A4;y=h-64
        c.setFillColor(HexColor(common.TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(common.MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第五章 全球开源大模型发展洞察')
        for item in items:
            if isinstance(item,tuple):
                text,style=item;para=common.paragraph(text,styles[style]);_,hh=para.wrap(w-92,1200);assert y-hh>=57,(text[:30],y,hh);para.drawOn(c,46,y-hh);layout.append({'text':text,'y':y,'height':hh});y-=hh+styles[style].spaceAfter
            else:
                assert y-fig.height>=57;renderPDF.draw(fig,c,46,y-fig.height);y-=fig.height+14
        c.setStrokeColor(HexColor(common.LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.setFillColor(HexColor(common.MUTED));c.drawString(46,28,footer);c.showPage()
    front=a.work/'opening.pdf';c=Canvas(str(front),pagesize=A4,invariant=1)
    draw_page(c,[('第五章 全球开源大模型发展洞察','title'),(P.TITLE,'heading'),(P.LEDE,'body'),(P.CONTEXT,'body'),*[(x+y,'body') for x,y in P.FINDINGS],(P.SCOPE,'note')],'第五章 · 模型供给、复用与开放条件')
    draw_page(c,[(P.FRAMEWORK_LEAD,'body'),fig,(P.OUTLOOK,'body')],'第五章 · 模型生态观察框架');c.save()
    doc=fitz.open();toc=[[1,'第五章 全球开源大模型发展洞察',1],[2,P.TITLE,1],[2,'图 5-0-1 模型生态观察框架',2]]
    starts={}
    for label,path in [('opening',front),('5.1',a.s51),('5.2',a.s52),('5.3',a.s53)]:
        with fitz.open(path) as part:
            offset=len(doc);starts[label]=offset;doc.insert_pdf(part)
            if label in ['5.1','5.2','5.3']:
                for level,title,page in part.get_toc():toc.append([level+1,title,page+offset])
    for i,page in enumerate(doc):
        w,h=page.rect.width,page.rect.height
        page.add_redact_annot(fitz.Rect(w-82,h-42,w-33,h-10),fill=(1,1,1));page.apply_redactions(images=0,graphics=0)
        num=str(i+1);page.insert_text((w-46-fitz.get_text_length(num,fontsize=8.2),h-28),num,fontsize=8.2,color=(.38,.44,.49))
    doc.set_toc(toc);doc.set_metadata({'title':'GOSD 2026 · 第五章 全球开源大模型发展洞察','author':'GOSD / 全球开源发展报告','subject':'20261022-ch5-review · 章首与 5.1—5.3 完整评审版'})
    doc.save(a.output,garbage=4,deflate=True)
    (a.work/'assembly.json').write_text(json.dumps({'pages':len(doc),'starts':starts,'openingLayout':layout,'sections':[str(a.s51),str(a.s52),str(a.s53)]},ensure_ascii=False,indent=2))
    print(f'{a.output}: {len(doc)} pages; section starts {starts}')

if __name__=='__main__':main()
