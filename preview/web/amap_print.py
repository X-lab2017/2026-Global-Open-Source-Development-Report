"""A-Map vector figures and the canonical web/PDF manuscript."""
from pathlib import Path
import argparse,json,hashlib,shutil,math
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import amap_publication as p
D=p.D;Figure,FigureFlow=vp.Figure,vp.FigureFlow
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
PW,LW=vp.PWIDTH,vp.LWIDTH
COL=dict(zip(D['platforms'],p.PALETTE))
def code_figure():
 f=Figure(p.FIGURES['code']['title'],'图 2-5-1',height=331);vp.title(f,0,13,'四个平台的五年趋势');f.text(PW,13,'2022—2026报告年度 · 万个',8.5,MUTED,'right')
 width=(PW-3*16)/4
 for j,(name,values) in enumerate(D['platforms'].items()):
  x=j*(width+16);left=x+22;right=x+width-7;top=52;bottom=122;maximum=[700,500,70,16][j]
  f.text(x,36,name,9.5,INK)
  for frac in [0,.5,1]:
   yy=bottom-(bottom-top)*frac;f.line([(left,yy),(right,yy)],LINE,.4);f.text(left-4,yy+3,f'{maximum*frac:g}',8.5,MUTED,'right')
  pts=[]
  for i,v in enumerate(values):
   xx=left+i*(right-left)/4
   if i in [0,2,4]:f.text(xx,bottom+14,str(D['years'][i]),8.5,MUTED,'center')
   if v is not None:pts.append((xx,bottom-v/10000/maximum*(bottom-top)))
  f.line(pts,COL[name],1.4)
  for xx,yy in pts:f.dot(xx,yy,1.8,COL[name])
  xx,yy=pts[-1];f.text(xx,yy-6,f'{values[-1]/10000:.2f}',8.5,COL[name],'right')
 f.text(0,155,'趋势纵轴分别定标；下方规模条形使用同一刻度。',8.5,MUTED)
 f.line([(0,164),(PW,164)],LINE,.6);vp.title(f,0,183,'2026报告年度：规模、净增与同比')
 for x,t in [(0,'平台'),(326,'活跃仓库 / 个'),(428,'净增 / 个'),(PW,'同比')]:f.text(x,204,t,8.5,MUTED,'left' if x==0 else 'right')
 for j,(name,values) in enumerate(D['platforms'].items()):
  yy=225+j*23;v=values[-1];prev=values[-2];f.text(0,yy,name,9,INK);f.rect(70,yy-9,153*v/7000000,10,COL[name],COL[name],0)
  f.text(326,yy,f'{v:,}',9,INK,'right');f.text(428,yy,f'+{v-prev:,}',9,INK,'right');f.text(PW,yy,f'+{(v/prev-1)*100:.1f}%',9,INK,'right')
 f.text(0,312,'来源：报告编制组。平台记录分别计量；AtomGit 前两年缺值保留为空。',8.5,MUTED);return f.caption()
def asset_figure(key):
 a=D['assets'][key];is_model=key=='models';title='模型' if is_model else '数据集'
 f=Figure(p.FIGURES[key]['title'],'图 '+p.FIGURES[key]['id'],height=370)
 vp.title(f,0,13,'A  地域供给');f.text(0,32,f'完整样本：{a["total"]:,} 个{title}',9,INK)
 by={r['id']:r['count'] for r in a['countries']};mx=max(by.values());sc=302/880;colors=['#DCEBF2','#BCD8E4','#8FBFD3','#5B9FBE','#337FA6','#156993']
 for g in D['world']:
  v=by.get(g['id']);fill='#e6e8ea' if v is None else colors[min(5,int(math.log10(v+1)/math.log10(mx+1)*5.999))]
  f.path(g['d'],0,43,sc,None if g.get('kind')=='line' else fill,'#9cacb6',.25)
 for code,name in [('US','美国'),('CN','中国')]:
  g=next(r for r in D['world'] if r['id']==code);xx,yy=g['center'][0]*sc,43+g['center'][1]*sc;f.rect(xx-12,yy-9,24,14,'#ffffff','#ffffff',1);f.text(xx,yy+1,name,8.5,INK,'center')
 for i,c in enumerate(colors):f.rect(i*12,210,12,7,c,c,0)
 f.text(79,217,'低 → 高 · 对数色阶',8.5,MUTED);f.rect(219,210,12,7,'#e6e8ea',LINE,0);f.text(237,217,'未列明',8.5,MUTED)
 vp.title(f,321,13,'供给数量排行');f.text(PW,13,'数量 / 个',8.5,MUTED,'right')
 for i,r in enumerate(a['countries']):
  yy=33+i*13.7;f.text(321,yy,f'{i+1:02}  '+r['name'],8.7,INK);f.text(PW,yy,f'{r["count"]:,}',8.7,INK,'right')
  f.line([(321,yy+3.5),(321+170*r['count']/mx,yy+3.5)],TEAL,.75)
 f.line([(0,231),(PW,231)],LINE,.6);vp.title(f,0,250,'B  中美欧：数量与下载份额')
 for j,(c,label) in enumerate(zip(p.PALETTE,['数量份额','下载份额'])):
  xx=325+j*90;f.rect(xx,242,12,8,c,c,0);f.text(xx+18,250,label,9,INK)
 europe=D['comparison']['assets'][key]
 for j,(country,label) in enumerate([('CN','中国'),('US','美国'),('EU','欧洲 *')]):
  x=j*172;left=x+27;right=x+118;f.text(x,271,label,9,INK)
  count=by[country] if country!='EU' else europe['count'];download=a['downloadShares'].get(country)
  for k,(v,label) in enumerate([(count/a['total']*100,'数量'),(download,'下载')]):
   yy=289+k*19;f.text(x,yy,label,8.5,INK)
   if v is None:f.line([(left,yy-3),(left+34,yy-3)],MUTED,.6,[3,2]);f.text(x+158,yy,'待补',8.5,MUTED,'right')
   else:f.rect(left,yy-9,(right-left)*v/100,10,p.PALETTE[k],p.PALETTE[k],0);f.text(x+158,yy,f'{v:.1f}%',8.5,INK,'right')
  f.line([(left,316),(right,316)],LINE,.5);f.text(left,329,'0',8.5,MUTED);f.text(right,329,'100%',8.5,MUTED,'right')
 f.text(0,347,f'* 欧洲数量为已列{len(europe["members"])}国小计（数量下限）；下载待补。来源：Hugging Face。',8.5,MUTED)
 return f.caption()
class Doc(vp.Doc):
 def __init__(self,path):super().__init__(path);self.title='GOSD 2026 · 2.5 全球开源资产地图';self.subject='同源正文、代码增长、模型供给与数据供给'
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.5 全球开源资产地图');c.drawCentredString(w/2,28,p.PDF_REVISION);c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def build(output,figs):
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=16,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.5,leading=21,spaceBefore=12,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,fontSize=11.2,leading=19,spaceBefore=8,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,s='body'):story.append(common.paragraph(t,styles.get(s,body)))
 def lead(i):para(p.STORIES[i][0],'section');para(p.STORIES[i][1][0])
 def after(i):
  for t in p.STORIES[i][1][1:]:a,b=t.split('。',1);para('**'+a+'。**'+b)
 para('2.5 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0)
 story.extend([FigureFlow(figs[0],'2-5-1'),PageBreak()]);after(0)
 for i in [1,2]:lead(i);story.append(FigureFlow(figs[i],f'2-5-{i+1}'));story.append(PageBreak());after(i)
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,ps) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for t in ps:para(t)
 para('统计范围与指标说明','section')
 for t in p.NOTES:para(t,'note')
 para(p.BRIDGE);doc=Doc(output);doc.build(story);return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=p.ROOT.parent/'output/pdf'/p.PDF_NAME);args=parser.parse_args();work=p.ROOT.parent/'tmp/pdfs/amap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+p.PDF_REVISION+json.dumps(D,ensure_ascii=False)+Path(vp.__file__).read_text())
 figs=[code_figure(),asset_figure("models"),asset_figure("datasets")];dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 for spec,fig in zip(p.FIGURES.values(),figs):(dest/spec['file']).write_text(fig.svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.BASE/'chapter-2-5.md').write_text(p.manuscript());digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,release_pdf=p.PDF_RELEASE_NAME,revision=p.PDF_REVISION,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256={str(f.relative_to(p.BASE)):digest(f) for f in [p.BASE/'observations.json',p.BASE/'fig-2-7-1_platform_active_repository_trend.csv',p.BASE/'comparison-groups.json']},manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
if __name__=='__main__':main()
