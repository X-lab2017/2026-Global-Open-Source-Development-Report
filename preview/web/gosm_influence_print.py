"""Private 5.2 PDF from the shared manuscript and web publication SVGs.
Run check_gosm_influence_publication.cjs with an SVG output directory first.
"""
from pathlib import Path
from io import BytesIO
import argparse,json
from lxml import etree
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import chapter1_print as common
import gosm_influence_content as P

INK,MUTED,TEAL,LINE=common.INK,common.MUTED,common.TEAL,common.LINE
T=P.TOPIC
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/05/#s52-evidence'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);ap.add_argument('--figures',type=Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
    svgs={key:(a.figures/(key+'.svg')).read_bytes() for key in P.FIGS}
    common.font_setup(a.font,a.work,subset_text=P.manuscript()+''.join(b.decode() for b in svgs.values())+Path(__file__).read_text())
    figs={}
    for key,b in svgs.items():
        root=etree.fromstring(b)
        for node in root.iter():
            node.attrib.pop('style',None)
            if etree.QName(node).localname=='text':node.set('font-family',common.FONT)
        drawing=svg2rlg(BytesIO(etree.tostring(root)))
        assert drawing is not None,key
        width=A4[0 if key=='head' else 1]-92;scale=width/drawing.width;drawing.scale(scale,scale);drawing.width*=scale;drawing.height*=scale
        figs[key]=drawing
    body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=9)
    styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=18,leading=28,spaceAfter=15),'heading':ParagraphStyle('heading',parent=body,fontSize=12.8,leading=21,spaceAfter=9,textColor=HexColor(TEAL)),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=8),'action':ParagraphStyle('action',parent=body,fontSize=11.4,leading=19,spaceAfter=6,textColor=HexColor(TEAL))}
    c=Canvas(str(a.output),pagesize=A4,invariant=1);c.setTitle('GOSD 2026 · 5.2 网络与影响力');c.setAuthor('GOSD / 全球开源发展报告');count=0;layout=[]
    def t(s,style='body'):return(s,style)
    def page(items,wide=False):
        nonlocal count
        count+=1;w,h=landscape(A4) if wide else A4;c.setPageSize((w,h));y=h-(59 if wide else 64);cw=w-92
        c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第五章 全球开源大模型发展洞察')
        for item in items:
            if isinstance(item,tuple):
                text,style=item;para=common.paragraph(text,styles[style]);_,hh=para.wrap(cw,1000);assert y-hh>=49,(count,text[:30],y,hh);para.drawOn(c,46,y-hh);layout.append({'page':count,'text':text,'y':y,'height':hh});y-=hh+styles[style].spaceAfter
                if text=='固定快照、原始表与核验记录（在线）':c.linkURL(WEB,(46,y+styles[style].spaceAfter,340,y+styles[style].spaceAfter+hh),relative=0,thickness=0)
                if style in ['title','heading']:key='p'+str(len(layout));c.bookmarkPage(key);c.addOutlineEntry(text,key,0 if style=='title' else 1,False)
            else:
                key=item;fig=figs[key];assert y-fig.height>=49,(count,key,y,fig.height);renderPDF.draw(fig,c,46,y-fig.height);y-=fig.height+11;c.bookmarkPage('fig-'+key);c.addOutlineEntry('图 '+P.FIGS[key][0]+' '+P.FIGS[key][1],'fig-'+key,2,False)
        c.setStrokeColor(HexColor(LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.setFillColor(HexColor(MUTED));c.drawString(46,28,'5.2 网络与影响力');c.drawRightString(w-46,28,str(count));c.showPage()
    page([t('5.2 网络与影响力','title'),t(T['lede']),t('研究问题：'+T['question']),t('指标定位：'+T['metric'],'note'),t('核心发现：'+T['core_finding']),t(T['window_note'],'note'),t(T['narratives'][0][0],'heading'),*[t(s) for s in T['insights']['network']]])
    page(['network'],True)
    page([t(T['narratives'][1][0],'heading'),t(T['insights']['flows'][0]),'flows'],True)
    page([*[t(s) for s in T['insights']['flows'][1:]],t(T['narratives'][2][0],'heading'),*[t(s) for s in T['insights']['head']]])
    page(['head'])
    page([t(T['action_lead'],'heading'),*[z for who,title,body,key in T['actions'] for z in [t(who+'：'+title,'action'),t(body+T['action_followups'][key])]],t(P.BRIDGE),t('口径与来源','heading'),*[t(s,'note') for s in P.NOTES],t('固定快照、原始表与核验记录（在线）','note')])
    c.save();(a.work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2));print(f'{a.output}: {count} pages')

if __name__=='__main__':main()
