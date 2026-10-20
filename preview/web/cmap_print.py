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
 vp.title(f,0,13,'A  全球贡献分布');f.text(LWIDTH,13,'GitHub · 2025.07.01—2026.06.30',9,MUTED,'right')
 mx=map_panel(f,'world',0,35,440);legend(f,0,279,mx)
 f.text(458,43,'贡献前十',10,INK);f.text(651,43,'万 OpenRank',9,MUTED,'right');f.text(LWIDTH,43,'活跃位次',9,MUTED,'right')
 for i,r in enumerate(D['countries'][:10]):
  yy=67+i*20;f.text(458,yy,f'{i+1:02} '+short(r['name']),9.3,INK);f.text(651,yy,num(r['value']),9.3,INK,'right');f.text(LWIDTH,yy,str(r['active_rank']),9.3,INK,'right');f.line([(458,yy+6),(651,yy+6)],LINE,.4)
 f.line([(0,302),(LWIDTH,302)],LINE,.6);vp.title(f,0,324,'B  GitHub 贡献趋势 · 2022—2026报告年度')
 for j,k in enumerate(['GLOBAL','US','CN']):
  tr=D['trends'][k];x=j*257;f.text(x,345,{'GLOBAL':'全球','US':'美国','CN':'中国'}[k],9.5,INK)
  vp.line_chart(f,x,350,235,79,[v/10000 for v in tr['values']],tr['labels'],COLORS[0],tr['axis_max']/10000,'万 OpenRank',endpoint=False)
 vp.notes(f,444,'来源：OpenDigger / OpenShare。贡献位次与活跃位次均为同平台、同年度记录。')
 return f.caption()

def current_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-2-2',height=246);vp.title(f,0,13,'A  五域当前规模与最近一年变化')
 f.text(420,38,'贡献度 / 万',9,MUTED,'right');f.text(PWIDTH,38,'同比',9,MUTED,'right');series=D['legacy']['series']
 for i,k in enumerate(KEYS):
  yy=61+i*28;v=series[k][-1];f.text(0,yy,'全球南方六国' if k=='Global South representatives' else D['legacy']['labels'][k],9.4,INK);f.rect(97,yy-10,232*v/7000000,12,COLORS[PALETTE[k]],COLORS[PALETTE[k]],0);f.text(420,yy,f'{v/10000:,.2f}',9.4,INK,'right');f.text(PWIDTH,yy,f'+{(v/series[k][-2]-1)*100:.1f}%',9.4,INK,'right')
 f.line([(97,193),(329,193)],LINE,.5);f.text(97,207,'0',8.5,MUTED);f.text(329,207,'700',8.5,MUTED,'right')
 vp.notes(f,225,'2026报告年度 · 来源：报告编制组五域综合统计。')
 return f.caption()

def history_figure():
 f=Figure(p.FIGURES['comparison']['title'],'图 2-2-2',height=510);vp.title(f,0,13,'B  五年变化 · 规模与增长共同观察')
 left,right,top,bottom=34,326,57,262
 for v in [0,175,350,525,700]:
  yy=bottom-v/700*(bottom-top);f.line([(left,yy),(right,yy)],LINE,.5);f.text(left-6,yy+3,str(v),8.5,MUTED,'right')
 f.text(0,39,'万 OpenRank',9,MUTED)
 for i,y in enumerate(D['legacy']['years']):f.text(left+i*(right-left)/4,bottom+17,y,8.5,MUTED,'center')
 for j,k in enumerate(KEYS):
  vals=D['legacy']['series'][k];c=PALETTE[k];pts=[(left+i*(right-left)/4,bottom-v/10000/700*(bottom-top)) for i,v in enumerate(vals)];f.line(pts,COLORS[c],1.6,DASH[c]);
  for xx,yy in pts:f.dot(xx,yy,1.9,COLORS[c])
  yy=65+j*43;f.line([(345,yy-3),(365,yy-3)],COLORS[c],1.6,DASH[c]);f.text(373,yy,'全球南方六国' if k=='Global South representatives' else D['legacy']['labels'][k],9.2,INK);f.text(373,yy+15,f'五年 +{(vals[-1]/vals[0]-1)*100:.1f}%',9,MUTED)
 f.line([(0,310),(PWIDTH,310)],LINE,.6);vp.title(f,0,335,'C  中美结论的适用范围 · 同一报告年度')
 for j,(title,cn,us,note) in enumerate([('编制组五域综合统计',4429200.83,4239710.05,'中国高于美国约4.5%'),('GitHub 单平台地域底表',BY['CN']['value'],BY['US']['value'],'美国贡献度仍高于中国')]):
  x=j*262;f.rect(x,350,241,103,'#f3f7f8',LINE,3);f.text(x+12,370,title,9.5,INK);f.text(x+12,394,'中国 '+num(cn)+' 万',10,INK);f.text(x+12,415,'美国 '+num(us)+' 万',10,INK);f.text(x+12,439,note,9,TEAL)
 vp.notes(f,475,'两套来源的覆盖范围不同，不将差额解释为国内平台净贡献。')
 vp.notes(f,489,'来源：报告编制组；OpenDigger / OpenShare。')
 return f.caption(True)

def china_figure():
 f=Figure(p.FIGURES['china']['title'],'图 2-2-3',height=475);vp.title(f,0,13,'A  中国省级贡献分布');vp.title(f,329,13,'B  全国趋势 / 万 OpenRank')
 mx=map_panel(f,'china',0,29,315);tr=D['trends']['CN'];vp.line_chart(f,326,45,177,145,[v/10000 for v in tr['values']],tr['labels'],COLORS[0],150,'',endpoint=False);legend(f,0,210,mx)
 f.text(PWIDTH,210,'GitHub · 2026报告年度',9,MUTED,'right');f.line([(0,229),(PWIDTH,229)],LINE,.5)
 for x,t,a in [(0,'贡献前十地区','left'),(235,'贡献度 / 万','right'),(365,'活跃开发者 / 万人','right'),(PWIDTH,'平均贡献 / 人','right')]:f.text(x,249,t,9.2,INK,a)
 for i,r in enumerate(D['provinces'][:10]):
  yy=270+i*16;f.text(0,yy,f'{i+1:02} '+short(r['name']),9.1,INK);f.text(235,yy,num(r['value']),9.1,INK,'right');f.text(365,yy,num(r['active']),9.1,INK,'right');f.text(PWIDTH,yy,f'{r["average"]:.3f}',9.1,INK,'right');f.line([(0,yy+5),(PWIDTH,yy+5)],LINE,.3)
 vp.notes(f,443,'京沪粤合计占全国约52.9%。平均贡献为同期贡献度除以活跃规模。')
 vp.notes(f,457,'来源：OpenDigger / OpenShare。全部34地保留于地图与数据表。')
 return f.caption()

def network_figure():
 f=Figure(p.FIGURES['globe']['title'],'图 2-2-4',height=489);vp.title(f,0,13,'A  实际来源关系 · 开发者所在地 → 项目归属地')
 w=440;x=(PWIDTH-w)/2;y=24;map_panel(f,'world',x,y,w,neutral=True,labels=False);sc=w/880;centers={g['id']:(x+g['center'][0]*sc,y+g['center'][1]*sc) for g in GEO['world']};mx=max(e['value'] for e in D['flows']['edges'])
 for e in sorted(D['flows']['edges'],key=lambda e:e['value']):
  a,b=centers[e['source']],centers[e['target']];c=COLORS[2] if e['target']=='CN' else COLORS[1];width=3*1.1*math.sqrt(e['value']/mx)
  if e['source']==e['target']:pts=[(a[0]+12*math.sin(t*math.tau),a[1]-10*(1-math.cos(t*math.tau))) for t in [i/48 for i in range(49)]]
  else:
   mid=((a[0]+b[0])/2,min(a[1],b[1])-min(57,abs(a[0]-b[0])*.3));pts=[((1-t)**2*a[0]+2*(1-t)*t*mid[0]+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*mid[1]+t*t*b[1]) for t in [i/48 for i in range(49)]]
  f.line(pts,c,width);xx,yy=pts[36];px,py=pts[35];angle=math.atan2(yy-py,xx-px);wing=3.2;f.line([(xx-wing*math.cos(angle-.6),yy-wing*math.sin(angle-.6)),(xx,yy),(xx-wing*math.cos(angle+.6),yy-wing*math.sin(angle+.6))],c,.8)
 for code in set(e['source'] for e in D['flows']['edges']):
  xx,yy=centers[code];f.dot(xx,yy,2.1,COLORS[2] if code=='CN' else COLORS[1] if code=='US' else MUTED)
  if code in ['CN','US','IN','CA']:f.text(xx,yy+13,BY[code]['name'],9,INK,'center')
 f.text(0,271,'线宽统一增强 ×3 · 原始贡献值与份额不变',8.8,MUTED)
 for j,target in enumerate(['CN','US']):
  x=j*262;rr=[e for e in D['flows']['edges'] if e['target']==target];color=COLORS[2] if target=='CN' else COLORS[1];f.text(x,292,('中国' if target=='CN' else '美国')+'项目 · 来源前十',9.7,color);f.text(x+175,292,'OpenRank',8.5,MUTED,'right');f.text(x+241,292,'原表份额',8.5,MUTED,'right')
  for i,e in enumerate(rr):
   yy=311+i*13;f.text(x,yy,BY[e['source']]['name'],8.7,INK);f.text(x+175,yy,f'{e["value"]:,.2f}',8.7,INK,'right');f.text(x+241,yy,f'{e["share_pct"]:.2f}%',8.7,INK,'right')
  t=D['flows']['targets'][target];f.text(x,450,f'已列 {t["observed_share_pct"]:.2f}% · 未列 {t["unlisted_share_pct"]:.2f}%',9,color)
 vp.notes(f,469,'来源：编制组中美项目来源前十表。未列来源不补造连线。')
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
 after(0);lead(1);story.append(FigureFlow(figs[1],'2-2-2-A'));story.append(PageBreak());story.append(FigureFlow(figs[2],'2-2-2-B'));after(1);story.append(PageBreak())
 lead(2);story.append(FigureFlow(figs[3],'2-2-3'));after(2);story.append(PageBreak())
 lead(3);story.append(FigureFlow(figs[4],'2-2-4'));after(3);story.append(PageBreak())
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
 figs=[global_figure(),current_figure(),history_figure(),china_figure(),network_figure()];dest=p.ROOT/'content/cmap/print';dest.mkdir(parents=True,exist_ok=True)
 names=[name for spec in p.FIGURES.values() for name in spec['files']]
 for name,fig in zip(names,figs):(dest/name).write_text(fig.svg())
 layout=build(args.output,figs);shutil.copy2(args.output,dest/p.PDF_NAME);(p.ROOT/'content/cmap/chapter-2-2.md').write_text(p.manuscript())
 digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
 manifest=dict(edition=p.EDITION,baseline='GOSO-PUB-20261020',pdf=p.PDF_NAME,pages=layout['pages'],figure_pages=layout['figures'],body_font_pt=11.2,chart_font_range_pt=[8.5,10.5],data_sha256=digest(p.ROOT/'content/cmap/data.json'),manuscript_sha256=hashlib.sha256(p.manuscript().encode()).hexdigest(),pdf_sha256=digest(args.output),figures=p.FIGURES,verification={'pdf_render':'pending','dom':'pending','browser_visual':'not_run_no_supported_browser','physical_print':'not_run'})
 (dest/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pdf':str(args.output),'pages':layout['pages'],'figure_pages':layout['figures']},ensure_ascii=False))
ROOT=p.ROOT.parent
if __name__=='__main__':main()
