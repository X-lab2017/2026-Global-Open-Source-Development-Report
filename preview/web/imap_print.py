"""I-Map: shared manuscript and source-locked vector publication figures."""
from pathlib import Path
import argparse,hashlib,json,shutil
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import vmap_publication as brand
import imap_publication as p
D=p.D;S=p.SNAPSHOT;ROOT=p.ROOT.parent
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
PWIDTH,LWIDTH=vp.PWIDTH,vp.LWIDTH
G=p.GROUPS;LABEL=p.LABELS;COLORS=[brand.SERIES_COLORS[i] for i in [1,2,0,4,3]];DASH=[brand.SERIES_DASH[i] for i in [1,2,0,4,3]]
Figure,FigureFlow=vp.Figure,vp.FigureFlow
wan=lambda n:f'{n/10000:,.2f}'

def chart(f,keys,x,y,w,h,maximum,unit='万 OpenRank'):
 left=x+31;right=x+w-6;top=y+17;bottom=y+h-23
 for i in range(5):
  v=maximum*i/4;yy=bottom-(bottom-top)*i/4;f.line([(left,yy),(right,yy)],LINE,.45);f.text(left-6,yy+3,f'{v:g}',8.5,MUTED,'right')
 f.text(x,y+3,unit,8.5,MUTED)
 for i,yr in enumerate(D['years']):f.text(left+i*(right-left)/4,bottom+16,str(yr),8.5,MUTED,'center')
 for k in keys:
  idx=G.index(k);pts=[(left+i*(right-left)/4,bottom-v/10000/maximum*(bottom-top)) for i,v in enumerate(D['series']['influence'][k])];f.line(pts,COLORS[idx],1.6,DASH[idx])
  for xx,yy in pts:f.dot(xx,yy,2,COLORS[idx])

def global_figure():
 f=Figure(p.FIGURES['world']['title'],'图 2-3-1',LWIDTH,461);vp.title(f,0,13,'A  全球项目影响力 · 2025自然年')
 rows=S['leaderboards'][0]['data'];by={r['code']:r for r in rows};mx=rows[0]['value'];sc=440/880
 for g in vp.GEO['world']:
  r=by.get(g['id']);fill=brand.MAP_COLORS[min(5,int(r['value']/mx*5.999))] if r else '#e6e8ea'
  f.path(g['d'],0,35,sc,None if g.get('kind')=='line' else fill,'#9cacb6',.35)
 for code in ['US','CN']:
  g=next(z for z in vp.GEO['world'] if z['id']==code);xx=g['center'][0]*sc;yy=35+g['center'][1]*sc;f.rect(xx-13,yy-10,26,14,'#ffffff','#ffffff',1);f.text(xx,yy,by[code]['name_zh'],9,INK,'center')
 for i,c in enumerate(brand.MAP_COLORS):f.rect(i*12,277,12,7,c,c,0)
 f.text(81,284,'0—'+wan(mx)+' 万 OpenRank',8.5,MUTED);f.rect(255,277,12,7,'#e6e8ea',LINE,0);f.text(274,284,'未收录',8.5,MUTED)
 for j,label in enumerate(['国家前六','企业前六']):
  x=458+j*153;f.text(x,40,label,10,INK);f.text(x,57,'万 OpenRank',8.5,MUTED)
  for i,r in enumerate(S['leaderboards'][j]['data'][:6]):
   yy=84+i*32;f.text(x,yy,f'{i+1:02} '+(r['name_zh'] or r['name']),9.1,INK);f.text(x+136,yy+15,wan(r['value']),9.1,INK,'right');f.line([(x,yy+20),(x+136*r['value']/S['leaderboards'][j]['data'][0]['value'],yy+20)],COLORS[0],1.6)
 f.line([(0,302),(LWIDTH,302)],LINE,.6);vp.title(f,0,324,'B  影响力趋势 · 2021—2025自然年')
 for j,tr in enumerate(S['trends']):
  x=j*257;f.text(x,345,['全球','美国','中国'][j],9.5,INK);vp.line_chart(f,x,350,235,79,[v/10000 for v in tr['values']],tr['labels'],COLORS[1 if j==2 else 0],[300,200,60][j],'万 OpenRank',endpoint=False)
 vp.notes(f,444,'来源：OpenDigger');return f.caption()

def comparison_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-3-2',height=410)
 vp.title(f,0,13,'A  五年趋势 · 2022—2026报告年度');vp.title(f,306,13,'B  2026贡献与影响力')
 chart(f,G[:3],0,31,280,177,200)
 for j,k in enumerate(G[:3]):
  x=j*88;f.line([(x,225),(x+15,225)],COLORS[j],1.6,DASH[j]);f.text(x+20,228,LABEL[k],8.8,INK)
 f.text(0,251,'全球南方六国与印度 · 独立纵轴',9.4,INK);chart(f,G[3:],0,262,280,94,.8)
 f.line([(0,361),(15,361)],COLORS[3],1.5,DASH[3]);f.text(20,364,'全球南方六国',8.5,INK);f.line([(150,361),(165,361)],COLORS[4],1.5,DASH[4]);f.text(170,364,'印度',8.5,INK)
 f.text(306,36,'万 OpenRank · 两种归属',8.5,MUTED)
 for j,k in enumerate(G):
  yy=61+j*60;vals=[D['series'][s][k][-1]/10000 for s in ['contribution','influence']];f.text(306,yy,LABEL[k],9.4,COLORS[j])
  for t,v in enumerate(vals):
   ty=yy+17+t*17;f.text(306,ty,['贡献','影响力'][t],8.5,MUTED);f.rect(345,ty-6,105*v/[700,200][t],4,COLORS[j],COLORS[j],0);f.text(PWIDTH,ty,f'{v:,.2f}',8.8,INK,'right')
 f.text(306,360,'贡献轴 0—700',8.5,MUTED);f.text(306,375,'影响力轴 0—200',8.5,MUTED)
 vp.notes(f,393,'来源：报告编制组');return f.caption()

def china_figure():
 f=Figure(p.FIGURES['china']['title'],'图 2-3-3',height=434);vp.title(f,0,13,'A  中国增长与项目样本 · 2026报告年度')
 chart(f,['China'],0,37,228,165,80)
 f.text(0,228,'2022—2026：增长159.9%',9.5,COLORS[1]);f.text(0,249,'2026：相当于美国41.2%',9.5,INK)
 f.text(260,36,'中国项目样本前十',9.5,INK);f.text(PWIDTH,36,'OpenRank',8.5,MUTED,'right')
 for i,r in enumerate(D['chinaProjects'][:10]):
  yy=58+i*20;f.text(260,yy,f'{i+1:02} '+r['project'],9,INK);f.text(PWIDTH,yy,f'{r["openrank"]:,.2f}',9,INK,'right');f.line([(260,yy+5),(PWIDTH,yy+5)],LINE,.35)
 f.line([(0,271),(PWIDTH,271)],LINE,.6);vp.title(f,0,291,'B  中美项目贡献来源 · 独立来源样本')
 for j,k in enumerate(['China','United States']):
  rows=[r for r in D['international'] if r['project_country']==k];local=next(r['share_pct'] for r in rows if r['developer_country']==k);cross=sum(r['share_pct'] for r in rows)-local;unknown=100-local-cross;x=j*262;color=COLORS[1 if j==0 else 0]
  f.text(x,315,LABEL[k]+'项目',9.5,color);start=x
  for frac,c in [(local,color),(cross,'#a8c9cc'),(unknown,'#e4e8eb')]:f.rect(start,325,241*frac/100,12,c,c,0);start+=241*frac/100
  f.text(x,356,f'本土 {local:.2f}%',9,INK);f.text(x,373,f'已列跨境 {cross:.2f}% · 未列 {unknown:.2f}%',8.8,MUTED)
 vp.notes(f,399,'来源：报告编制组。中国前30项样本中，前两项合占53.7%。');return f.caption()

class Doc(vp.Doc):
 def __init__(self,path):
  super().__init__(path);self.title='GOSD 2026 · 2.3 全球开源项目影响力地图';self.subject='三幅影响力图组与共用研究正文'
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.3 全球开源项目影响力地图 · I-Map');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

def build(output,figs):
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=16,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.6,leading=21,spaceBefore=12,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,fontSize=11.2,leading=19,spaceBefore=8,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,s='body'):story.append(common.paragraph(t,styles.get(s,body)))
 def lead(i):
  title,ps=p.STORIES[i];para(title,'section')
  for t in ps[:p.FIGURE_AFTER[i]]:para(t)
 def after(i):
  for t in p.STORIES[i][1][p.FIGURE_AFTER[i]:]:
   a,b=t.split('。',1);para('**'+a+'。**'+b)
 para('2.3 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0);after(0)
 story.extend([NextPageTemplate('landscape'),PageBreak(),FigureFlow(figs[0],'2-3-1'),NextPageTemplate('portrait'),PageBreak()])
 for i in [1,2]:lead(i);story.append(FigureFlow(figs[i],f'2-3-{i+1}'));after(i);story.append(PageBreak())
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,ps) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for t in ps:para(t)
 para('统计范围与指标说明','section')
 for t in p.NOTES:para(t,'note')
 para(p.BRIDGE);doc=Doc(output);doc.build(story);return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=ROOT/'output/pdf'/p.PDF_NAME);args=parser.parse_args();work=ROOT/'tmp/pdfs/imap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False)+json.dumps(S,ensure_ascii=False)+Path(vp.__file__).read_text())
 figs=[global_figure(),comparison_figure(),china_figure()];dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 for spec,fig in zip(p.FIGURES.values(),figs):(dest/spec['file']).write_text(fig.svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.BASE/'chapter-2-3.md').write_text(p.manuscript());digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256={n:digest(p.BASE/n) for n in ['observations.json','influence.json']},manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
if __name__=='__main__':main()
