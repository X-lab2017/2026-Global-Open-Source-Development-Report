"""Three original G-Map figures, shared encoding and manuscript for print."""
from pathlib import Path
import argparse,json,hashlib,shutil
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak
import chapter1_print as common
import vmap_print as vp
import gmap_publication as p
D=p.D;W=vp.PWIDTH;INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
COL=['#156993','#007D87','#76549D','#8A631F','#426C9D']
def chart(key,index):
 f=vp.Figure(p.FIGURES[index-1][2],f'图 2-7-{index}',height=300)
 rows=D['series'][key];lic=key=='licenses';L=35;R=W-98 if lic else W-40;T=35;B=240
 maximum=80000 if lic else 4000 if key=='foundation' else 500
 rightmax=4 if key=='foundation' else 3500
 x=lambda i:L+22+i*(R-L-44)/4
 y=lambda v:B-v/maximum*(B-T)
 yr=lambda v:B-v/rightmax*(B-T)
 fmt=lambda v:f'{v:,.0f}' if v==int(v) else f'{v:,.2f}'.rstrip('0').rstrip('.')
 f.text(L,12,'累计活跃仓库 / 个' if key=='mulan' else '活跃仓库 / 个',8.5,MUTED)
 if not lic:f.text(R,12,'OpenRank 占比 / %' if key=='foundation' else '项目 OpenRank',8.5,MUTED,'right')
 for j in range(5):
  yy=B-j*(B-T)/4;f.line([(L,yy),(R,yy)],LINE,.4);f.text(L-5,yy+3,fmt(maximum*j/4),8.5,MUTED,'right')
  if not lic:f.text(R+6,yy+3,fmt(rightmax*j/4)+('%' if key=='foundation' else ''),8.5,MUTED)
 if lic:
  fields=['MIT','Apache-2.0','BSD-3-Clause','GPL-3.0','AGPL-3.0']
  for j,k in enumerate(fields):
   pts=[(x(i),y(r[k])) for i,r in enumerate(rows)];f.line(pts,COL[j],1.4)
   for xx,yy in pts:f.dot(xx,yy,2,COL[j])
   f.text(x(4)+9,y(rows[-1][k])+(-4 if j==2 else 9 if j==3 else 3),k,8.5,COL[j])
 else:
  a='active_repositories' if key=='foundation' else 'cumulative_active_repositories';b='foundation_project_openrank_share_pct' if key=='foundation' else 'project_openrank_influence'
  for i,r in enumerate(rows):
   top=y(r[a]);small=B-top<20;f.rect(x(i)-19,top,38,B-top,'#DCEBF2',COL[0],0);f.text(x(i),top-7 if small else B-12,fmt(r[a]),8.5,INK,'center')
  pts=[(x(i),yr(r[b])) for i,r in enumerate(rows)];f.line(pts,COL[1],1.5)
  for i,(xx,yy) in enumerate(pts):f.dot(xx,yy,2.8,COL[1]);f.rect(xx-16,yy-17,32,11,'#FFFFFF','#FFFFFF',0);f.text(xx,yy-8,fmt(rows[i][b])+('%' if key=='foundation' else ''),8.5,COL[1],'center')
 for i,r in enumerate(rows):f.text(x(i),B+16,str(r['year']),8.5,MUTED,'center')
 f.text(0,276,'来源：报告编制组原表'+(' · 左轴柱形、右轴折线；两轴均从零起' if not lic else ' · 五种许可证使用同一纵轴'),8.5,MUTED)
 return f.caption()
class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.7 全球开源治理与社会公益地图');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);args=ap.parse_args();work=p.ROOT.parent/'tmp/pdfs/gmap';work.mkdir(parents=True,exist_ok=True);out=p.ROOT.parent/'output/pdf'/p.PDF_NAME;out.parent.mkdir(parents=True,exist_ok=True);dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D['series'],ensure_ascii=False))
 figs=[chart(key,i) for i,key in enumerate(['foundation','licenses','mulan'],1)]
 for i,f in enumerate(figs,1):(dest/f'fig-2-7-{i}.svg').write_text(f.svg())
 for name in ['fig-2-7-2-continued.svg','fig-2-7-4.svg','fig-2-7-5.svg']:
  q=dest/name
  if q.exists():q.unlink()
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'h':ParagraphStyle('h',parent=body,fontSize=16,leading=24,spaceAfter=14,keepWithNext=True),'s':ParagraphStyle('s',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('n',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,sty='body'):story.append(common.paragraph(t,styles.get(sty,body)))
 para('2.7 '+p.TITLE,'h');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note')
 for i,(title,ps) in enumerate(p.STORIES):
  if i:story.append(PageBreak())
  if i==1:
   a,b=p.STORIES[0][1][1].split('。',1);para('**'+a+'。**'+b)
  para(title,'s');para(ps[0]);story.append(vp.FigureFlow(figs[i],f'2-7-{i+1}'))
  if i:
   a,b=ps[1].split('。',1);para('**'+a+'。**'+b)
 story.append(PageBreak());para(p.ACTION_TITLE,'s')
 for title,ps in p.STRATEGIES:para(title,'s');[para(t) for t in ps]
 para('统计范围与指标说明','s');[para(t,'note') for t in p.NOTES];para(p.BRIDGE)
 doc=Doc(out);doc.build(story);shutil.copy2(out,dest/p.PDF_NAME);(p.BASE/'chapter-2-7.md').write_text(p.manuscript());(p.ROOT.parent/'chapters/chapter2/2.6-全球开源治理与社会公益地图-G-Map.md').write_text(p.manuscript())
 spec={'edition':p.EDITION,'pages':doc.page,'figure_pages':doc.figures,'pdf':p.PDF_NAME,'release_pdf':p.PDF_RELEASE_NAME,'data_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in p.BASE.glob('*.csv')},'manuscript_sha256':hashlib.sha256(p.manuscript().encode()).hexdigest(),'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'verification':{'pdf_render':'four portrait pages visually checked','browser_pixels':'not_run','physical_print':'not_run'}}
 (dest/'publication-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
