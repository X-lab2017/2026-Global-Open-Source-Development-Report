"""Publication C-Map: source-aligned vector maps and complete shared prose."""
from pathlib import Path
import argparse,hashlib,json,math,shutil
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak,NextPageTemplate
import chapter1_print as common
import vmap_print as vp
import vmap_publication as brand
import cmap_publication as p
D=p.DATA;GEO=vp.GEO;BY={r['id']:r for r in D['countries']};PWIDTH=vp.PWIDTH;LWIDTH=vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
COLORS=brand.SERIES_COLORS;DASH=brand.SERIES_DASH
PALETTE={'Europe':0,'United States':1,'China':2,'India':3,'Global South representatives':4}
KEYS=['Europe','China','United States','Global South representatives','India']
Figure=vp.Figure;FigureFlow=vp.FigureFlow
num=lambda v:f'{math.trunc((v/10000+1e-10)*100)/100:,.2f}'
short=lambda s:s.replace('特别行政区','').replace('壮族自治区','').replace('回族自治区','').replace('维吾尔自治区','').replace('自治区','').replace('省','').replace('市','')

def map_panel(f,scope,x,y,w,neutral=False,labels=True):
 rr=D['countries' if scope=='world' else 'provinces'];by={r['id']:r for r in rr};mx=max(r['value'] for r in rr);sc=w/880
 for g in GEO[scope]:
  if g.get('kind')=='line':f.path(g['d'],x,y,sc,None,MUTED,.4);continue
  r=by.get(g['id']);fill='#eff3f5' if neutral else (brand.MAP_COLORS[min(5,int(r['value']/mx*5.999))] if r else '#e6e8ea')
  if g['id']=='100000_JD':fill='#ffffff'
  f.path(g['d'],x,y,sc,fill,'#9cacb6',.35)
 if labels:
  for code in (['US','CN','DE','IN','BR'] if scope=='world' else ['110000','310000','440000','710000','510000']):
   g=next(z for z in GEO[scope] if z['id']==code);xx=x+g['center'][0]*sc;yy=y+g['center'][1]*sc;name=short(g['name']);tw=common.pdfmetrics.stringWidth(name,common.FONT,9)+5
   f.rect(xx-tw/2,yy-9,tw,13,'#ffffff','#ffffff',1);f.text(xx,yy+1,name,9,INK,'center')
 return mx

def legend(f,x,y,mx):
 for i,c in enumerate(brand.MAP_COLORS):f.rect(x+i*12,y-7,12,7,c,c,0)
 f.text(x+80,y,'0—'+num(mx)+' 万 OpenRank',8.5,MUTED)

def global_figure():
 f=Figure(p.FIGURES['global']['title'],'图 2-2-1',LWIDTH,461)
 vp.title(f,0,13,'A  全球贡献分布 · 2025年')
 mx=map_panel(f,'world',0,35,440);legend(f,0,279,mx)
 f.text(458,43,'贡献前十',10,INK);f.text(651,43,'万 OpenRank',9,MUTED,'right');f.text(LWIDTH,43,'活跃位次',9,MUTED,'right')
 for i,r in enumerate(D['countries'][:10]):
  yy=67+i*20;f.text(458,yy,f'{i+1:02} '+short(r['name']),9.3,INK);f.text(651,yy,num(r['value']),9.3,INK,'right');f.text(LWIDTH,yy,str(r['active_rank']),9.3,INK,'right');f.line([(458,yy+6),(651,yy+6)],LINE,.4)
 f.line([(0,302),(LWIDTH,302)],LINE,.6);vp.title(f,0,324,'B  贡献趋势 · 2021—2025自然年')
 for j,k in enumerate(['GLOBAL','US','CN']):
  tr=D['trends'][k];x=j*257;f.text(x,345,{'GLOBAL':'全球','US':'美国','CN':'中国'}[k],9.5,INK)
  vp.line_chart(f,x,350,235,79,[v/10000 for v in tr['values']],tr['labels'],COLORS[0],tr['axis_max']/10000,'万 OpenRank',endpoint=False)
 vp.notes(f,444,'来源：OpenDigger')
 return f.caption()

def comparison_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-2-2',height=410);vp.title(f,0,13,'A  五域趋势 · 2022—2026报告年度');vp.title(f,337,13,'B  2026规模与同比')
 left,right,top,bottom=29,306,50,242
 for v in [0,175,350,525,700]:
  yy=bottom-v/700*(bottom-top);f.line([(left,yy),(right,yy)],LINE,.5);f.text(left-6,yy+3,str(v),8.5,MUTED,'right')
 f.text(0,36,'万 OpenRank',8.5,MUTED)
 for i,y in enumerate(D['legacy']['years']):f.text(left+i*(right-left)/4,bottom+17,y,8.5,MUTED,'center')
 for j,k in enumerate(KEYS):
  vals=D['legacy']['series'][k];c=PALETTE[k];pts=[(left+i*(right-left)/4,bottom-v/10000/700*(bottom-top)) for i,v in enumerate(vals)];f.line(pts,COLORS[c],1.6,DASH[c])
  for xx,yy in pts:f.dot(xx,yy,1.9,COLORS[c])
  yy=46+j*43;f.line([(337,yy-3),(353,yy-3)],COLORS[c],1.6,DASH[c]);f.text(360,yy,'全球南方六国' if k=='Global South representatives' else D['legacy']['labels'][k],9.2,INK)
  f.rect(337,yy+8,162*vals[-1]/7000000,5,COLORS[c],COLORS[c],0);f.text(337,yy+28,f'{vals[-1]/10000:,.2f} 万',9.2,INK);f.text(PWIDTH,yy+28,f'+{(vals[-1]/vals[-2]-1)*100:.1f}%',9,MUTED,'right')
 f.line([(0,280),(PWIDTH,280)],LINE,.6);vp.title(f,0,301,'中美差距的变化 · 中国减美国');f.text(PWIDTH,301,'2026：中国高于美国4.5%',9.4,COLORS[2],'right')
 for i,y in enumerate(D['legacy']['years']):
  diff=(D['legacy']['series']['China'][i]-D['legacy']['series']['United States'][i])/10000;x=i*103;center=x+44;width=abs(diff)/220*43;color=COLORS[2] if diff>=0 else COLORS[1]
  f.text(center,324,str(y),9,MUTED,'center');f.line([(center,333),(center,353)],LINE,.6);f.rect(center if diff>=0 else center-width,337,width,9,color,color,0);f.text(center,370,f'{diff:+.2f} 万',9,INK,'center')
 vp.notes(f,391,'来源：报告编制组')
 return f.caption()

def china_figure():
 f=Figure(p.FIGURES['china']['title'],'图 2-2-3',height=460);vp.title(f,0,13,'A  中国省级贡献分布 · 2025年');vp.title(f,329,13,'B  全国趋势 / 万 OpenRank')
 mx=map_panel(f,'china',0,29,315);tr=D['trends']['CN'];vp.line_chart(f,326,45,177,145,[v/10000 for v in tr['values']],tr['labels'],COLORS[0],150,'',endpoint=False);legend(f,0,210,mx)
 f.line([(0,229),(PWIDTH,229)],LINE,.5)
 vp.title(f,0,250,'贡献规模前十');vp.title(f,270,250,'平均贡献前十 · 样本')
 for i,(r,a) in enumerate(zip(D['provinces'][:10],D['province_average_reference'])):
  yy=273+i*15;f.text(0,yy,f'{i+1:02} '+short(r['name']),9.1,INK);f.text(230,yy,num(r['value'])+' 万',9.1,INK,'right');f.line([(0,yy+5),(230,yy+5)],LINE,.3)
  f.text(270,yy,f'{i+1:02} '+short(a['name']),9.1,INK);f.text(PWIDTH,yy,f'{a["average"]:.3f} / 人',9.1,INK,'right');f.line([(270,yy+5),(PWIDTH,yy+5)],LINE,.3)
 vp.notes(f,432,'京沪粤占全国52.9%。来源：OpenDigger；平均贡献：报告编制组。')
 return f.caption()

def network_figure():
 f=Figure(p.FIGURES['globe']['title'],'图 2-2-4',height=534)
 for i,(label,detail) in enumerate([('参与活动','贡献的起点'),('协作关系','共同建设'),('持续投入','维护与积累')]):
  xx=i*174;f.dot(xx+7,14,4,COLORS[0]);f.text(xx+18,17,label,9.5,INK);f.text(xx+18,32,detail,8.5,MUTED)
  if i<2:f.line([(xx+110,18),(xx+150,18)],LINE,.8);f.line([(xx+146,15),(xx+150,18),(xx+146,21)],LINE,.8)
 f.text(PWIDTH,48,'机制示意；下图为实际来源网络',8.5,MUTED,'right')
 w=440;x=(PWIDTH-w)/2;y=45;map_panel(f,'world',x,y,w,neutral=True,labels=False);sc=w/880;centers={g['id']:(x+g['center'][0]*sc,y+g['center'][1]*sc) for g in GEO['world']};mx=max(e['value'] for e in D['flows']['edges'])
 for e in sorted(D['flows']['edges'],key=lambda e:e['value']):
  a,b=centers[e['source']],centers[e['target']];c=COLORS[2] if e['target']=='CN' else COLORS[1];width=3*1.1*math.sqrt(e['value']/mx)
  if e['source']==e['target']:pts=[(a[0]+12*math.sin(t*math.tau),a[1]-10*(1-math.cos(t*math.tau))) for t in [i/48 for i in range(49)]]
  else:
   mid=((a[0]+b[0])/2,min(a[1],b[1])-min(57,abs(a[0]-b[0])*.3));pts=[((1-t)**2*a[0]+2*(1-t)*t*mid[0]+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*mid[1]+t*t*b[1]) for t in [i/48 for i in range(49)]]
  f.line(pts,c,width);xx,yy=pts[36];px,py=pts[35];angle=math.atan2(yy-py,xx-px);wing=3.2;f.line([(xx-wing*math.cos(angle-.6),yy-wing*math.sin(angle-.6)),(xx,yy),(xx-wing*math.cos(angle+.6),yy-wing*math.sin(angle+.6))],c,.8)
 for code in set(e['source'] for e in D['flows']['edges']):
  xx,yy=centers[code];f.dot(xx,yy,2.1,COLORS[2] if code=='CN' else COLORS[1] if code=='US' else MUTED)
  if code in ['CN','US','IN','CA']:f.text(xx-14 if code=='CA' else xx,yy-12 if code=='CA' else yy+13,BY[code]['name'],9,INK,'center')
 f.text(0,282,'线宽增强 ×3，数值不变。',8.8,MUTED)
 for j,target in enumerate(['CN','US']):
  x=j*262;rr=[e for e in D['flows']['edges'] if e['target']==target];color=COLORS[2] if target=='CN' else COLORS[1];t=D['flows']['targets'][target];cross=t['observed_share_pct']-t['local_share_pct'];label='中国' if target=='CN' else '美国'
  f.text(x,303,label+'项目 · 本土 '+f'{t["local_share_pct"]:.2f}%',9.6,color)
  offset=x
  for frac,fill in [(t['local_share_pct'],color),(cross,'#c1d9dc'),(t['unlisted_share_pct'],'#e4e8eb')]:
   f.rect(offset,310,241*frac/100,8,fill,fill,0);offset+=241*frac/100
  f.text(x,332,f'跨境已列 {cross:.2f}% · 未列 {t["unlisted_share_pct"]:.2f}%',8.5,MUTED)
  f.text(x,356,'来源前十',9.4,INK);f.text(x+175,356,'OpenRank',8.5,MUTED,'right');f.text(x+241,356,'原表份额',8.5,MUTED,'right')
  for i,e in enumerate(rr):
   yy=375+i*13;f.text(x,yy,BY[e['source']]['name'],8.7,INK);f.text(x+175,yy,f'{e["value"]:,.2f}',8.7,INK,'right');f.text(x+241,yy,f'{e["share_pct"]:.2f}%',8.7,INK,'right')
 vp.notes(f,511,'来源：报告编制组。深色：本土；浅色：跨境已列；灰色：未列。')
 return f.caption()

class Doc(vp.Doc):
 def __init__(self,path):
  super().__init__(path);self.title='GOSD 2026 · 2.2 全球开源贡献地图';self.subject='四幅贡献图组与共用研究正文'
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.2 全球开源贡献地图 · C-Map');c.drawRightString(w-46,28,str(doc.page));c.restoreState()

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
 para('2.2 '+p.TITLE,'chapter');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0)
 story.extend([NextPageTemplate('landscape'),PageBreak(),FigureFlow(figs[0],'2-2-1'),NextPageTemplate('portrait'),PageBreak()])
 after(0);lead(1);story.append(FigureFlow(figs[1],'2-2-2'));after(1);story.append(PageBreak())
 lead(2);story.append(FigureFlow(figs[2],'2-2-3'));after(2);story.append(PageBreak())
 lead(3);story.append(FigureFlow(figs[3],'2-2-4'));after(3);story.append(PageBreak())
 para(p.ACTION_TITLE,'section');para(p.ACTION_INTRO)
 for i,(title,ps) in enumerate(p.STRATEGIES,1):
  para(str(i)+' '+title,'subsection')
  for t in ps:para(t)
 para('统计范围与指标说明','section')
 for t in p.NOTES:para(t,'note')
 para(p.BRIDGE)
 doc=Doc(output);doc.build(story);return dict(pages=doc.page,figures=doc.figures,headings=doc.headings,paragraphs=doc.locations)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True);parser.add_argument('--output',type=Path,default=ROOT/'output/pdf'/p.PDF_NAME);args=parser.parse_args()
 work=ROOT/'tmp/pdfs/cmap';work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False)+json.dumps(GEO,ensure_ascii=False)+Path(vp.__file__).read_text())
 figs=[global_figure(),comparison_figure(),china_figure(),network_figure()];dest=p.ROOT/'content/cmap/print';dest.mkdir(parents=True,exist_ok=True)
 names=[name for spec in p.FIGURES.values() for name in spec['files']]
 for name,fig in zip(names,figs):(dest/name).write_text(fig.svg())
 for name in ['fig-2-2-2_a_current.svg','fig-2-2-2_b_history.svg']:(dest/name).write_text(figs[1].svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.ROOT/'content/cmap/chapter-2-2.md').write_text(p.manuscript())
 digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256=digest(p.ROOT/'content/cmap/data.json'),manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
ROOT=p.ROOT.parent
if __name__=='__main__':main()
