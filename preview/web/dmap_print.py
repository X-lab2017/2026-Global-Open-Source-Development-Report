"""D-Map vector publication, using exactly the web manuscript and source values."""
from pathlib import Path
import argparse,json,hashlib,shutil,math
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import dmap_publication as p
D=p.D;Figure,FigureFlow=vp.Figure,vp.FigureFlow
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
PW,LW=vp.PWIDTH,vp.LWIDTH
COL={'US':'#168b92','CN':'#397da6','DE':'#936c9e','GB':'#a87f2e','IN':'#558247','OTH':'#788991'}
PAL=['#647f96','#8c6f75','#6b8281','#a07580','#658395','#8a8264','#6b7894','#767895']
ORDER=['US','CN','DE','GB','CA','FR','IN','NL','CH','PL','SG','CZ','BG','SE']
color=lambda c:COL[c] if c in COL else PAL[ORDER.index(c)%len(PAL)]
nm=lambda c:'未列来源' if c=='OTH' else D['names'][c]
num=lambda v:f'{v:,.2f}'
def trend(f,codes,x,y,w,h,maxv):
 left=x+30;right=x+w-8;top=y+8;bottom=y+h-22
 for i in range(4):
  yy=bottom-(bottom-top)*i/3;f.line([(left,yy),(right,yy)],LINE,.4);f.text(left-5,yy+3,str(int(maxv*i/3))+'%',8.5,MUTED,'right')
 for i,yr in enumerate(D['years']):f.text(left+i*(right-left)/4,bottom+15,str(yr),8.5,MUTED,'center')
 for j,c in enumerate(codes):
  pts=[(left+i*(right-left)/4,bottom-r['values'][c]/maxv*(bottom-top)) for i,r in enumerate(D['shares'])];f.line(pts,color(c),1.5,[None,[8,4],[3,3],[10,3,2,3],[5,3]][j%5])
  for xx,yy in pts:f.dot(xx,yy,1.8,color(c))
def breadth_figure():
 f=Figure(p.FIGURES['breadth']['title'],'图 2-6-1',LW,461);vp.title(f,0,13,'A  全球贡献来源 · 2025自然年');by={r['code']:r['value'] for r in D['countries']};mx=max(by.values());sc=420/880;colors=['#dbeaf0','#b7d0dd','#89b3c8','#6095b1','#397b9e','#156993']
 for g in D['world']:
  v=by.get(g['id']);fill='#e6e8ea' if v is None else colors[min(5,int(math.log10(v+1)/math.log10(mx+1)*5.999))];f.path(g['d'],0,28,sc,None if g.get('kind')=='line' else fill,'#9cacb6',.25)
 for code in ['US','CN','IN','BR']:
  g=next(r for r in D['world'] if r['id']==code);xx,yy=g['center'][0]*sc,28+g['center'][1]*sc;f.rect(xx-12,yy-9,24,14,'#ffffff','#ffffff',1);f.text(xx,yy+1,nm(code),8.5,INK,'center')
 for i,c in enumerate(colors):f.rect(i*17,260,17,7,c,c,0)
 f.text(109,267,'低 → 高 · 对数色阶',8.5,MUTED);f.rect(270,260,12,7,'#e6e8ea',LINE,0);f.text(290,267,'未收录',8.5,MUTED)
 vp.title(f,450,13,'地区贡献度前十');f.text(LW,34,'OpenRank',8.5,MUTED,'right')
 for i,r in enumerate(D['countries'][:10]):
  yy=53+i*21;f.text(450,yy,f'{i+1:02}  '+r['name_zh'],9,INK);f.text(LW,yy,num(r['value']),9,INK,'right');f.line([(450,yy+6),(450+292*r['value']/mx,yy+6)],TEAL,1.4)
 f.line([(0,286),(LW,286)],LINE,.6);vp.title(f,0,305,'B  五年贡献份额 · 2022—2026报告年度');trend(f,['US','DE','CN','GB','IN'],0,329,420,101,30);trend(f,['OTH'],466,329,284,101,60)
 for j,c in enumerate(['US','DE','CN','GB','IN']):
  xx=j*82;f.line([(xx,319),(xx+12,319)],color(c),1.5,[None,[8,4],[3,3],[10,3,2,3],[5,3]][j]);f.text(xx+17,322,nm(c),8.5,INK)
 f.text(466,322,'其他国家合计：50.53% → 51.38%',9,INK)
 vp.notes(f,442,'来源：OpenDigger；报告编制组。地图快照与年度份额分别计量。');return f.caption()
def sources_figure():
 f=Figure(p.FIGURES['sources']['title'],'图 2-6-2',height=301)
 for j,c in enumerate(['CN','US']):
  x=j*263;w=240;rows=[r for r in D['sourceShares'] if r['target']==c];local=next(r['share'] for r in rows if r['source']==c)
  unlisted=next(r['share'] for r in rows if r['source']=='OTH');cross=sum(r['share'] for r in rows if r['source'] not in (c,'OTH'))
  vp.title(f,x,13,nm(c)+'项目');offset=0
  for value,colour in [(local,'#326f9e'),(cross,'#16808a'),(unlisted,'#788991')]:
   f.rect(x+w*offset/100,27,w*value/100,19,colour,colour,0);offset+=value
  f.text(x,61,f'本土 {local:.2f}%',8.5,INK);f.text(x+79,61,f'已列跨境 {cross:.2f}%',8.5,INK);f.text(x+w,61,f'未列 {unlisted:.2f}%',8.5,INK,'right')
  f.text(x,82,'来源',8.5,MUTED);f.text(x+178,82,'OpenRank',8.5,MUTED,'right');f.text(x+w,82,'份额',8.5,MUTED,'right')
  for i,r in enumerate(rows[:10]):
   y=101+i*16;f.text(x,y,f'{i+1:02} '+nm(r['source']),8.8,INK);f.text(x+178,y,num(r['value']),8.8,INK,'right');f.text(x+w,y,f'{r["share"]:.2f}%',8.8,INK,'right');f.line([(x,y+5),(x+90*r['share']/100,y+5)],color(r['source']),1)
  f.text(x,269,'未列来源 '+f'{rows[-1]["share"]:.2f}%',8.5,MUTED)
 return f.caption()
def network_figure():
 f=Figure(p.FIGURES['network']['title'],'图 2-6-3',height=330);rows=[r for r in D['flows'] if r['target'] in ['CN','US']];src=[c for c in ORDER if any(r['source']==c for r in rows)];dest=['US','CN'];H=218;top=35;pad=6;total=sum(r['value'] for r in rows);scale=(H-pad*(len(src)-1))/total
 def layout(ids,key):
  out={};y=top
  for c in ids:
   v=sum(r['value'] for r in rows if r[key]==c);out[c]={'y':y,'h':v*scale,'cur':0,'v':v};y+=v*scale+pad
  return out
 a=layout(src,'source');b=layout(dest,'target');left=83;right=390
 f.text(0,14,'贡献来源',9.5,INK);f.text(right+16,14,'项目归属',9.5,INK)
 for r in rows:
  s,t=a[r['source']],b[r['target']];yy1=s['y']+s['cur'];yy2=t['y']+t['cur'];hh=r['value']*scale;s['cur']+=hh;t['cur']+=hh;upper=[];lower=[]
  for i in range(41):
   z=i/40;xx=(1-z)**3*(left+7)+3*(1-z)**2*z*200+3*(1-z)*z*z*280+z**3*right;yy=(1-z)**3*yy1+3*(1-z)**2*z*yy1+3*(1-z)*z*z*yy2+z**3*yy2;upper.append((xx,yy));lower.append((xx,yy+hh))
  cc=color(r['source']);rgb=[int(cc[i:i+2],16) for i in (1,3,5)];tint='#'+''.join(f'{round(v*.5+255*.5):02x}' for v in rgb);f.polygon(upper+list(reversed(lower)),tint)
 for ids,lay,x,leftside in [(src,a,left,True),(dest,b,right,False)]:
  labels=[]
  for c in ids:labels.append(max(lay[c]['y']+lay[c]['h']/2,labels[-1]+12 if labels else top))
  if labels[-1]>top+H:
   labels[-1]=top+H
   for i in range(len(labels)-2,-1,-1):labels[i]=min(labels[i],labels[i+1]-12)
  for c,yy in zip(ids,labels):
   q=lay[c];f.rect(x,q['y'],7,max(.35,q['h']),color(c),color(c),0);f.line([(x if leftside else x+7,q['y']+q['h']/2),(x-6 if leftside else x+13,yy)],color(c),.45)
   f.text(x-10 if leftside else x+17,yy+3,nm(c),8.5,INK,'right' if leftside else 'left')
   if not leftside:f.text(x+17,yy+16,num(q['v']),8.5,MUTED)
 f.line([(0,271),(PW,271)],LINE,.5);f.text(0,288,'中国 → 美国：43,542.15',9,INK);f.text(PW,288,'中国 → 中国：44,698.58',9,INK,'right');f.text(0,308,'单位：OpenRank。线宽表示贡献度；与来源份额表分别计量。',8.5,MUTED);return f.caption()
class Doc(vp.Doc):
 def __init__(self,path):super().__init__(path);self.title='GOSD 2026 · 2.6 全球开源多样性地图';self.subject='同源正文、全球贡献来源、中美来源结构与跨地域连接'
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.6 全球开源多样性地图');c.drawCentredString(w/2,28,p.PDF_REVISION);c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def build(output,figs):
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'chapter':ParagraphStyle('chapter',parent=body,fontSize=16,leading=24,spaceAfter=16,keepWithNext=True),'section':ParagraphStyle('section',parent=body,fontSize=12.6,leading=21,spaceBefore=12,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'subsection':ParagraphStyle('subsection',parent=body,fontSize=11.2,leading=19,spaceBefore=8,spaceAfter=6,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('note',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,s='body'):story.append(common.paragraph(t,styles.get(s,body)))
 def lead(i):para(p.STORIES[i][0],'section');para(p.STORIES[i][1][0])
 def after(i):
  for t in p.STORIES[i][1][1:]:a,b=t.split('。',1);para('**'+a+'。**'+b)
 para('2.6 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0);after(0)
 story.extend([NextPageTemplate('landscape'),PageBreak(),FigureFlow(figs[0],'2-6-1'),NextPageTemplate('portrait'),PageBreak()])
 for i in [1,2]:lead(i);story.append(FigureFlow(figs[i],f'2-6-{i+1}'));after(i);story.append(PageBreak())
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,ps) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for t in ps:para(t)
 para('统计范围与指标说明','section')
 for t in p.NOTES:para(t,'note')
 para(p.BRIDGE);doc=Doc(output);doc.build(story);return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=p.ROOT.parent/'output/pdf'/p.PDF_NAME);args=parser.parse_args();work=p.ROOT.parent/'tmp/pdfs/dmap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+p.PDF_REVISION+json.dumps(D,ensure_ascii=False)+Path(vp.__file__).read_text())
 figs=[breadth_figure(),sources_figure(),network_figure()];dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 for spec,fig in zip(p.FIGURES.values(),figs):(dest/spec['file']).write_text(fig.svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.BASE/'chapter-2-6.md').write_text(p.manuscript());digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,release_pdf=p.PDF_RELEASE_NAME,revision=p.PDF_REVISION,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256={str(f.relative_to(p.BASE)):digest(f) for f in [p.BASE/'data.json',*sorted((p.BASE/'source').glob('*.csv'))]},manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
if __name__=='__main__':main()
