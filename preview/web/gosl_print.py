"""Five vector review plates for sections 4.2–4.6; never included in web export."""
from pathlib import Path
import argparse, json
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import HexColor
import chapter1_print as common
import gosl_landscapes as G
from gosl_publication import SECTIONS, NOTES, EDITION, CHAPTER_CLOSE, figure_number

INK, MUTED, LINE, WASH = '#18394c', '#4d6573', '#bacbd3', '#f1f6f8'
ACCENTS = {'models':'#087984','cloud':'#2d5f9f','database':'#8c6928','riscv':'#8a4a42','pytorch':'#76508b'}
PW, PH = landscape(A3)
MARGIN = 36
WEB = 'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/04/'

def write_pdf(output, font, work, page_offset=0, total_pages=5):
    work.mkdir(parents=True, exist_ok=True)
    manuscript=json.dumps([G.DATA,SECTIONS,NOTES,CHAPTER_CLOSE],ensure_ascii=False)+Path(__file__).read_text()
    common.font_setup(font,work,subset_text=manuscript)
    c=Canvas(str(output),pagesize=(PW,PH),pageCompression=1)
    c.setTitle('GOSD 2026 · 4.2—4.6 技术全景与研究框架')
    c.setAuthor('GOSD 2026')
    def text(x,y,value,size=10,color=INK,align='left'):
        c.setFillColor(HexColor(color));c.setFont(common.FONT,size)
        getattr(c,{'left':'drawString','center':'drawCentredString','right':'drawRightString'}[align])(x,PH-y,str(value))
    def rect(x,y,w,h,fill='#ffffff',stroke=LINE,r=3):
        c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.45)
        c.roundRect(x,PH-y-h,w,h,r,stroke=1,fill=1)
    def line(x,y,x2,y2,color=LINE,width=.6):
        c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x,PH-y,x2,PH-y2)
    def wrapped(x,y,value,width,size=10,leading=14,color=INK):
        rows=common.wrap(value,width,size)
        for i,row in enumerate(rows):text(x,y+i*leading,row,size,color)
        return y+len(rows)*leading
    scale=(PW-2*MARGIN)/G.W
    for page,d in enumerate(G.DATASETS,1):
        m=SECTIONS[d['id']];accent=ACCENTS[d['id']]
        text(MARGIN,25,'GOSD 2026  /  第四章 全球开源技术全景洞察',9,MUTED)
        text(PW-MARGIN,25,'全景与研究框架 · 2026.10',9,MUTED,'right')
        text(MARGIN,54,d['number']+' '+m['title'],21,INK)
        end=wrapped(MARGIN,77,m['intro'],PW-2*MARGIN,11.2,15)
        assert end<=107,(d['id'],'intro',end)
        c.bookmarkPage(d['id']);c.addOutlineEntry(d['number']+' '+m['title'],d['id'])
        # The Web inspector is interactive; the PDF uses the same category geometry
        # and project names, with clickable names and a compact reading note below.
        top=110
        X=lambda x:MARGIN+x*scale
        Y=lambda y:top+(y-54)*scale
        boxes,groups=G.geometry(d);cats=G.names(d)
        for group in groups:
            x,w=group['x'],group['w']
            text(X(x),Y(74),group['group']['name'],19*scale,accent)
            text(X(x+w),Y(74),group['group']['subtitle'],12*scale,MUTED,'right')
            line(X(x),Y(94),X(x+w),Y(94),accent,1.2)
        for b in boxes:
            category=cats[b['id']];x,y,w,h=b['x'],b['y'],b['w'],b['h']
            rect(X(x),Y(y),w*scale,h*scale,r=3)
            rect(X(x+1),Y(y+1),(w-2)*scale,30*scale,WASH,WASH,r=2)
            text(X(x+10),Y(y+21),category['name'],14*scale,INK)
            text(X(x+w-10),Y(y+21),str(category['count'])+' 项' if b['cells'] else '本样本未覆盖',11*scale,MUTED,'right')
            for cell in b['cells']:
                p=cell['project'];px,py,cw,ch=cell['x'],cell['y'],cell['w'],cell['h']
                size=14*scale;available=(cw-34)*scale
                while (len(common.wrap(G.display_name(d,p),available,size))>2 or len(common.wrap(G.display_name(d,p),available,size))*(size+scale)>ch*scale-1) and size>11*scale:size-=.25
                rows=common.wrap(G.display_name(d,p),available,size);leading=size+1*scale
                assert len(rows)*leading<=ch*scale-1,(d['id'],p['name'])
                start=Y(py)+ch*scale/2-(len(rows)-1)*leading/2+size*.35
                rect(X(px+2),Y(py+ch/2-10),23*scale,20*scale,WASH,WASH,r=2)
                mark=str(p.get('rank','')) if d['id']=='models' else p['name'][0].upper()
                text(X(px+13.5),Y(py+ch/2+4),mark,11*scale,accent,'center')
                for i,row in enumerate(rows):text(X(px+32),start+i*leading,row,size)
                c.linkURL(p['url'],(X(px),PH-Y(py+ch),X(px+cw),PH-Y(py)),relative=0,thickness=0)
        text(PW/2,724,figure_number(d)+'  '+m['caption'],12,INK,'center')
        text(PW/2,741,m['scope'],9.2,MUTED,'center')
        # A concise interpretation and four future questions, not research findings.
        rows=common.wrap(m['reading'],PW-2*MARGIN,9.4)
        assert len(rows)==1,(d['id'],'reading',len(rows))
        text(MARGIN,758,m['reading'],9.4,MUTED)
        line(MARGIN,771,PW-MARGIN,771)
        final=page==len(G.DATASETS)
        text(MARGIN,781 if final else 787,'后续研究 · 待补充证据与分析',10,accent)
        colw=(PW-2*MARGIN-24)/2
        for i,(title,question) in enumerate(m['questions']):
            x=MARGIN+(i%2)*(colw+24);y=(795+(i//2)*13) if final else (803+(i//2)*15)
            value=title+'：'+question
            assert pdfmetrics.stringWidth(value,common.FONT,9.2)<=colw,(d['id'],title)
            text(x,y,value,9.2)
        if final:
            assert pdfmetrics.stringWidth(CHAPTER_CLOSE,common.FONT,10.2)<=PW-2*MARGIN
            text(MARGIN,823,CHAPTER_CLOSE,10.2,accent)
        text(MARGIN,835,'来源：报告原始清单与分类记录  ·  项目名可点击核查；图中位置与面积不表示规模或真实依赖。',8,MUTED)
        c.linkURL(d['source']['url'],(MARGIN,0,MARGIN+150,16),relative=0,thickness=0)
        text(PW-MARGIN,835,f'{page+page_offset} / {total_pages}',8,MUTED,'right')
        c.showPage()
    c.save()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--font',type=Path,required=True);parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--page-offset',type=int,default=0);parser.add_argument('--total-pages',type=int,default=5)
    args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    write_pdf(args.output,args.font,args.work,args.page_offset,args.total_pages)
    print('Created five landscape-only review plates:',args.output)
