"""Complete Chapter 6 publication PDF from the shared manuscript and publication SVGs.

The released PDF is published with the chapter. All five figures are portrait;
each of the nine actions is expanded, including steps, roles and follow-up.
"""
from pathlib import Path
from io import BytesIO
import argparse,json,re
from lxml import etree
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,PageBreak,Spacer,KeepTogether
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import chapter1_print as common
from chapter6_content import data,manuscript,FILES,FIG_TITLES,FIG_NUMBERS

class Doc(BaseDocTemplate):
 def afterFlowable(self,flowable):
  if isinstance(flowable,Paragraph):
   self.records.append({'page':self.page,'text':flowable.getPlainText()})
   if flowable.style.name in ['title','section','heading']:
    key='h'+str(len(self.records));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flowable.getPlainText(),key,{'title':0,'section':1,'heading':2}[flowable.style.name],False)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
 D=data();R=Path(__file__).resolve().parents[2];svgs={key:(R/'figures/chapter6'/(stem+'.svg')).read_bytes() for key,stem in FILES.items()}
 common.font_setup(a.font,a.work,subset_text=manuscript(D)+json.dumps(D,ensure_ascii=False)+''.join(b.decode() for b in svgs.values())+Path(__file__).read_text())
 figs={};width=A4[0]-92
 for key,b in svgs.items():
  root=etree.fromstring(b)
  for node in root.iter():
   node.attrib.pop('style',None)
   if etree.QName(node).localname=='text':node.set('font-family',common.FONT)
  drawing=svg2rlg(BytesIO(etree.tostring(root)));scale=width/drawing.width;drawing.scale(scale,scale);drawing.width*=scale;drawing.height*=scale;figs[key]=drawing
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(common.INK),wordWrap='CJK',spaceAfter=9,splitLongWords=False,allowWidows=0,allowOrphans=0)
 styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=20,leading=30,spaceAfter=14,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=16,leading=25,spaceBefore=6,spaceAfter=12,keepWithNext=True),'heading':ParagraphStyle('heading',parent=body,fontSize=12.8,leading=21,spaceBefore=12,spaceAfter=9,keepWithNext=True,textColor=HexColor(common.TEAL)),'lead':ParagraphStyle('lead',parent=body,fontSize=13,leading=22,spaceAfter=14,textColor=HexColor(common.TEAL)),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=9,textColor=HexColor(common.MUTED)),'watch':ParagraphStyle('watch',parent=body,fontSize=9.5,leading=15,spaceAfter=12,textColor=HexColor(common.MUTED))}
 story=[];L=lambda v:v['zh'] if isinstance(v,dict) else v
 def p(v,style='body'):return common.paragraph(L(v),styles[style])
 def add(v,style='body'):story.append(p(v,style))
 def paras(vs):story.extend(p(v) for v in vs)
 def new():story.append(PageBreak())
 add('第六章 未来展望与行动建议','title');add(D['headline'],'lead');add(D['intro']);add(D['position'],'note');add(D['scope'],'note')
 sy=D['synthesis'];add('6.1 '+L(sy['title']),'section');add(sy['question'],'lead');paras(sy['paragraphs'])
 for i,f in enumerate(sy['findings']):
  if i==1:new()
  add(f['title'],'heading');paras(f['paragraphs'])
 add(sy['task_title'],'heading')
 for task in D['tasks']:
  add(task['title'],'heading');add(task['body'])
 new();add(sy['figure_lead']);story.append(figs['overview']);add(sy['after'],'note')
 for actor in D['actors']:
  new();add(actor['section']+' 面向'+L(actor['title'])+('的倡议' if actor['id']=='community' else '的建议'),'section');add(actor['intro']);story.append(figs[actor['id']])
  new()
  for i,action in enumerate([z for z in D['actions'] if z['actor']==actor['id']],1):
   watch='持续观察：'+'；'.join(L(w['label'])+'——'+L(w['detail']) for w in action['watch'])+'。'
   block=[p(actor['section']+'.'+str(i)+' '+L(action['title']),'heading'),p(action['why']),p(action['body']),p(watch,'watch')]
   story.append(KeepTogether(block))
 cl=D['closing'];new();add('6.5 '+L(cl['title']),'section');add(cl['question'],'lead');add(cl['paragraphs'][0]);story.append(figs['cycle'])
 new();paras(cl['paragraphs'][1:]);add(cl['final'],'lead');add(cl['invitation'],'lead')
 doc=Doc(str(a.output),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=60,bottomMargin=55,title='GOSD 2026 · 第六章 未来展望与行动建议',author='GOSD / 全球开源发展报告');doc.records=[]
 def page(c,doc):
  w,h=A4;c.saveState();c.setFillColor(HexColor(common.TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(common.MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第六章 未来展望与行动建议');c.setStrokeColor(HexColor(common.LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'持续共同创造及其公共价值');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
 frame=Frame(46,55,width,A4[1]-115,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
 doc.addPageTemplates(PageTemplate(id='portrait',frames=[frame],onPage=page));doc.build(story)
 (a.work/'layout.json').write_text(json.dumps(doc.records,ensure_ascii=False,indent=2));print(f'{a.output}: {doc.page} portrait pages')
if __name__=='__main__':main()
