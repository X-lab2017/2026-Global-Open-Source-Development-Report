"""Local Chapter 4 opening + 4.1 review PDF. No PDF is copied into Web assets."""
from pathlib import Path
import argparse,json,math,subprocess
import fitz
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import landscape_publication as p
import landscape_atlas as atlas
ROOT=Path(__file__).resolve().parents[2]
W,LW=vp.PWIDTH,vp.LWIDTH
INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
BLUE='#156993';PURPLE='#7853A2';PALE='#F3F8FA';GOLD='#A56E10'
COLORS=['#156993','#9670B8','#25949A','#B47D27','#578548','#AB6252','#687FAD','#A27B92','#89959D']
D={};M={}
fmt=lambda x:f'{x:,.2f}'
class Figure(vp.Figure):
 def __init__(self,i,height,width=W):super().__init__(p.FIGURES[i-1][1],f'图 4-1-{i}',width,height);self.logos=[]
 def logo(self,file,x,y,size=9):
  if file and (ROOT/'preview/content/landscape/logos'/file).exists():self.logos.append((file,x,y,size))
 def paint(self,c,x,top,width):
  super().paint(c,x,top,width);sc=width/self.width
  for file,xx,yy,sz in self.logos:c.drawImage(ImageReader(str(ROOT/'preview/content/landscape/logos'/file)),x+xx*sc,top-(yy+sz)*sc,sz*sc,sz*sc,mask='auto')
def fittext(f,x,y,s,w,size=8.5,color=INK):
 fs=min(size,w/max(pdfmetrics.stringWidth(s,common.FONT,1),1));assert fs>=6.5,(s,fs);f.text(x,y,s,fs,color)
def bar(f,x,y,w,value,maxval,color=BLUE):
 f.rect(x,y,w,4,'#E1EDF2','#E1EDF2',1)
 if value is not None and value>0:f.rect(x,y,w*value/maxval,4,color,color,1)
def stamp(f,text,sim=False):
 f.text(0,13,('模拟数据 · ' if sim else '')+text,9,GOLD if sim else TEAL)
def guide():
 f=vp.Figure('','',height=194)
 for i,(t,s) in enumerate(p.TOPICS):
  x=(i%2)*262;y=(i//2)*62;f.line([(x,y),(x+241,y)],LINE,.6);f.text(x,y+19,f'4.{i+1}  {t}',11,TEAL);f.text(x,y+40,s,9.4,INK)
 return f
def architecture(i):
 layer=['Agent Infra','Model Infra'][i-1];f=Figure(i,455,LW);groups=[x for x in atlas.LAYOUTS[layer]];cw=(LW-24)/3
 # Print cards regroup within the same functional bands; all projects remain present.
 if i==1:sets=[groups[:4],groups[4:7],groups[7:]];bands=['任务入口 / APPLICATIONS','构建与编排 / FRAMEWORK','运行支撑 / RUNTIME']
 else:sets=[groups[:5],groups[5:9],groups[9:]];bands=['模型服务与后训练','预训练与加速','数据与计算']
 pp=[q for q in D['projects'] if q['layer']==layer]
 stamp(f,f'{layer} · {len(pp)} 个项目 / {len(groups)} 个类别')
 for col,gg in enumerate(sets):
  x=col*(cw+12);f.rect(x,24,cw,24,PURPLE if i==1 else BLUE,PURPLE if i==1 else BLUE,3);f.text(x+9,40,bands[col],9.2,'#FFFFFF')
  records=[]
  for g in gg:
   key=g[0];ps=[q for q in pp if q['section']==key];rows=math.ceil(len(ps)/2);records.append((key,ps,rows))
  totalrows=sum(z[2] for z in records);rowheight=min(22,(373-len(records)*23-(len(records)-1)*6)/totalrows);y=54
  for key,ps,rows in records:
   h=23+rows*rowheight;f.rect(x,y,cw,h,PALE,LINE,3);name=D['sections'][key]['name'];fittext(f,x+7,y+15,name,cw-35,9.2,TEAL);f.text(x+cw-7,y+15,str(len(ps)),8.3,MUTED,'right')
   for j,q in enumerate(ps):
    xx=x+7+(j%2)*(cw-10)/2;yy=y+23+(j//2)*rowheight;f.logo(q['logo'],xx,yy,8);lines=common.wrap(q['name'],(cw-10)/2-18,8.1)
    assert len(lines)<=2,(q['name'],lines)
    for k,line in enumerate(lines):f.text(xx+11,yy+7+k*8.5,line,8.1,INK)
   y+=h+6
  assert y<=438,(layer,y)
 f.text(0,437,'功能分层示意，非项目依赖图；标识为仓库所有者图标。固定分类，全部项目保留。',8.2,MUTED)
 return f.caption()
def rank():
 f=Figure(3,362);stamp(f,'2026-08 · 全部 25 类 · OpenRank / 观测覆盖')
 rows=M['categories'][-1];cw=(W-22)/2
 for j,rr in enumerate([rows[:13],rows[13:]]):
  x=j*(cw+22)
  for i,r in enumerate(rr):
   y=40+i*23.7;color=PURPLE if next(q['layer'] for q in D['projects'] if q['section']==r['key'])=='Agent Infra' else BLUE
   f.text(x,y,f'{r["rank"]:02}',7.7,MUTED);fittext(f,x+17,y,r['name'],cw-94,8.2);f.text(x+cw,y,fmt(r['value']),8.1,INK,'right');bar(f,x+17,y+5,cw-58,r['value'],rows[0]['value'],color);f.text(x+cw,y+12,f'{r["coverage"]}/{r["count"]}',7.2,MUTED,'right')
 f.text(0,335,'紫色 Agent Infra；蓝色 Model Infra。140 / 145 个项目有值，缺失不补零。',8.1,MUTED)
 return f.caption()
def lines(f,series,x,y,w,h,maximum,rank=False,start=6,unit='',labels=True):
 left=x+24;right=x+w-7;top=y+9;bottom=y+h-22
 for v in ([1,math.ceil(maximum/2),maximum] if rank else [0,maximum/2,maximum]):
  frac=(v-1)/(maximum-1) if rank else v/maximum
  yy=top+(bottom-top)*frac if rank else bottom-(bottom-top)*frac
  f.line([(left,yy),(right,yy)],LINE,.4);f.text(left-5,yy+3,f'{v:.0f}',7.5,MUTED,'right')
 for k,s in enumerate(series):
  pts=[]
  for i,val in enumerate(s['values'][start:]):
   if val is None:
    if len(pts)>1:f.line(pts,s.get('color',COLORS[k%len(COLORS)]),1.15)
    pts=[];continue
   xx=left+(right-left)*i/(17-start);yy=top+(val-1)/(maximum-1)*(bottom-top) if rank else bottom-val/maximum*(bottom-top);pts.append((xx,yy))
  if len(pts)>1:f.line(pts,s.get('color',COLORS[k%len(COLORS)]),1.3)
 for idx in [start,(start+17)//2,17]:f.text(left+(right-left)*(idx-start)/(17-start),bottom+14,D['months'][idx],7.2,MUTED,'center')
 if unit:f.text(x,y-3,unit,7.8,MUTED)
 if labels:
  xx=x
  for k,s in enumerate(series):f.rect(xx,y+h+1,7,3,s.get('color',COLORS[k%len(COLORS)]),s.get('color',COLORS[k%len(COLORS)]),0);f.text(xx+11,y+h+5,s['name'],8.2,INK);xx+=len(s['name'])*8.2+29
 return bottom

def overview():
 f=Figure(4,286);stamp(f,'2025-09—2026-08 · 位次仅在同一大类内比较；灰线保留其余类别')
 for j,layer in enumerate(['Agent Infra','Model Infra']):
  y=32+j*115;hist=M['layerHistory'][j];tops=[r['key'] for r in hist[-1][:3]];ss=[]
  for r in hist[-1][::-1]:ss.append({'name':r['name'],'color':COLORS[tops.index(r['key'])] if r['key'] in tops else '#C4CED3','values':[next(t['rank'] for t in h if t['key']==r['key']) for h in hist]})
  f.text(0,y,layer,9.3,TEAL);lines(f,ss,0,y+10,W-100,83,len(hist[-1]),rank=True,labels=False)
  for k,key in enumerate(tops):f.text(W-91,y+29+k*21,D['sections'][key]['name'],8.1,COLORS[k])
 return f.caption()
def compare():
 f=Figure(5,203);stamp(f,'2025-09—2026-08 · 全领域 25 类统一位次')
 keys=['Personal AI assistants','Serving · Inference','Agentic coding'];ss=[{'name':D['sections'][k]['name'],'values':[next(r['rank'] for r in rr if r['key']==k) for rr in M['categories']]} for k in keys]
 lines(f,ss,0,31,W,133,25,rank=True)
 return f.caption()
def projects():
 f=Figure(6,232);stamp(f,'个人助手 · 2026-08 排名 / 2025-09—2026-08 历史位次')
 rows=M['projects'];left=215
 for i,r in enumerate(rows):
  y=40+i*22;f.text(0,y,str(i+1),8,MUTED);fittext(f,16,y,r['name'],108,8.4);bar(f,126,y-4,44,r['value'],rows[0]['value']);f.text(left,y,fmt(r['value']),8.2,INK,'right')
 selected=rows[:3];ps=[next(q for q in D['projects'] if q['id']==r['key']) for r in selected];series=[]
 for q in ps:
  vv=[]
  for month in range(18):
   rr=sorted([x for x in D['projects'] if x['section']==q['section'] and x['trend'][month] is not None],key=lambda x:-x['trend'][month]);vv.append(next((j+1 for j,x in enumerate(rr) if x['id']==q['id']),None))
  series.append({'name':q['name'],'values':vv})
 lines(f,series,236,28,W-236,135,7,rank=True,labels=False)
 for i,s in enumerate(series):f.text(254,176+i*12,s['name'],8,COLORS[i])
 return f.caption()
def concentration():
 f=Figure(7,254);stamp(f,'2026-08 · 前三项目占类别有值项目 OpenRank 的份额')
 rows=M['concentration'];cw=(W-20)/2
 for j,rr in enumerate([rows[:13],rows[13:]]):
  for i,r in enumerate(rr):
   x=j*(cw+20);y=35+i*15.2;fittext(f,x,y,r['name'],135,7.8);bar(f,x+136,y-4,cw-177,r['value'],1,PURPLE);f.text(x+cw,y,f'{r["value"]*100:.1f}%',8,INK,'right')
 return f.caption()
def shift():
 f=Figure(8,421);stamp(f,'2025-09—2026-08 · 107 个连续有值项目 · 份额变化 / 百分点')
 f.text(0,34,'类别',8,MUTED);f.text(220,34,'期初 → 期末',8,MUTED,'right');f.text(W,34,'变化',8,MUTED,'right');center=350;scale=18
 for i,r in enumerate(M['shift']):
  y=50+i*13.4;fittext(f,0,y,r['name'],145,8);f.text(220,y,f'{r["before"]*100:.2f}% → {r["after"]*100:.2f}%',8,INK,'right');v=r['value']*100;color=TEAL if v>=0 else PURPLE;f.rect(min(center,center+v*scale),y-6,abs(v)*scale,6,color,color,0);f.text(W,y,f'{v:+.2f}',8,INK,'right')
 f.line([(center,40),(center,381)],LINE,.7);f.text(center,394,'0',8,MUTED,'center')
 return f.caption()
def countrymap():
 f=Figure(9,251);stamp(f,'2025-09—2026-08 · 全领域 · 不代表真实贡献',True)
 rr=M['countries'];by={r['code']:r for r in rr};mapped=sorted(r['share'] for r in rr if r['code'] not in ['OTHER','UNKNOWN']);cap=mapped[-2]+.7*(mapped[-1]-mapped[-2]);colors=['#DCECF6','#ADD4E8','#73B4D6','#4194BE','#1D719D','#145477']
 for g in D['world']:
  r=by.get(g.get('code'));col=colors[min(5,int(r['share']/cap*6))] if r else '#E6E8EA';f.path(g['d'],0,28,.375,None if g.get('kind')=='line' else col,'#A4B3BC',.25)
 for i,r in enumerate(rr):
  y=42+i*20;f.text(355,y,r['name'],8.4,INK);bar(f,405,y-4,52,r['share'],rr[0]['share']);f.text(W,y,f'{r["share"]*100:.1f}%',8,INK,'right')
 for j,col in enumerate(colors):f.rect(j*17,211,17,5,col,col,0)
 f.text(108,217,f'0—{cap*100:.1f}%（P95 封顶）',7.8,MUTED);f.text(0,231,'其他与未知仅列数值，不分配到地图区域。',8,MUTED)
 return f.caption()
def countrydetail():
 f=Figure(10,278);stamp(f,'2025-09—2026-08 · 美国示例 · 类别贡献占该国模拟总量',True)
 rows=next(x['rows'] for x in M['countryCats'] if x['code']=='US');cw=(W-22)/2
 for j,rr in enumerate([rows[:13],rows[13:]]):
  for i,r in enumerate(rr):
   x=j*(cw+22);y=38+i*17;fittext(f,x,y,r['name'],134,7.8);bar(f,x+136,y-4,cw-177,r['share'],max(z['share'] for z in rows));f.text(x+cw,y,f'{r["share"]*100:.1f}%',8,INK,'right')
 return f.caption()
def dots(i,lq=False):
 f=Figure(i,263);stamp(f,'2025-09—2026-08 · Agent Infra · '+('相对专长 LQ' if lq else '类别内贡献份额'),True)
 selected=['US','CN','DE'];left=156;right=W-40;top=44;step=14.5;base={r['code']:r['share'] for r in M['baseAgent']}
 maxv=2 if lq else .55
 for frac in [0,1/3,2/3,1]:
  x=left+(right-left)*frac;f.line([(x,top-12),(x,top+step*11+6)],LINE,.5);f.text(x,top+step*11+18,f'{frac*maxv:.1f}' if lq else f'{frac*maxv*100:.0f}%',7.6,MUTED,'center')
 if lq:
  x=left+(right-left)/maxv;f.line([(x,top-12),(x,top+step*11+6)],GOLD,.9)
 for j,r in enumerate(M['countryByCategory']):
  y=top+j*step;fittext(f,0,y+3,r['name'],147,8.1)
  for k,code in enumerate(selected):
   val=next(x['share'] for x in r['rows'] if x['code']==code);val=val/base[code] if lq else val;assert val<=maxv,(i,val);f.dot(left+(right-left)*val/maxv,y,2.6,COLORS[k])
 for k,s in enumerate(['美国','中国','德国']):f.dot(8+k*65,234,2.6,COLORS[k]);f.text(16+k*65,237,s,8.3,INK)
 f.text(W,237,'1 = 与该国总体份额相当' if lq else '分母包含其他与未知',8,MUTED,'right')
 return f.caption()
def countrytrend():
 f=Figure(13,213);stamp(f,'2025-09—2026-08 · 全领域 · 单月贡献份额',True)
 ss=[{'name':name,'values':[next(r['share']*100 for r in rr if r['code']==code) for rr in M['countryHistory']]} for code,name in [('US','美国'),('CN','中国'),('GB','英国')]];lines(f,ss,0,34,W,137,50,unit='%')
 return f.caption()
def main():
 global D,M
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Chapter4-Opening-Section4-1-Review-20261021.pdf'));a=ap.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True);work=ROOT/'tmp/pdfs/a-landscape';work.mkdir(parents=True,exist_ok=True)
 D=json.loads((ROOT/'_site/assets/landscape/v3-data.json').read_text())
 js='''const d=JSON.parse(require('fs').readFileSync('_site/assets/landscape/v3-data.json')),m=require('./preview/web/landscape.js')(d);console.log(JSON.stringify({categories:d.months.map((_,i)=>m.categories('all',i)),layerHistory:['Agent Infra','Model Infra'].map(s=>d.months.map((_,i)=>m.categories(s,i))),projects:m.projectRows('all','Personal AI assistants',17),concentration:m.concentration('all',17),shift:m.shift('all',6,17),countries:m.country('all','all',12,17),countryCats:d.countries.map(c=>({code:c.code,rows:m.countryCategories('all',c.code,12,17)})),countryByCategory:m.sections('Agent Infra').map(k=>({key:k,name:d.sections[k].name,rows:m.country('Agent Infra',k,12,17)})),baseAgent:m.country('Agent Infra','all',12,17),countryHistory:d.months.map((_,i)=>m.country('all','all','month',i))}));'''
 M=json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,text=True));(work/'metrics.json').write_text(json.dumps(M,ensure_ascii=False,indent=2))
 common.font_setup(a.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps([D['projects'],D['sections'],D['countries']],ensure_ascii=False))
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8)
 styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=17,leading=27,spaceAfter=15),'heading':ParagraphStyle('heading',parent=body,fontSize=12.8,leading=21,spaceAfter=9,textColor=HexColor(TEAL)),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=7),'action':ParagraphStyle('action',parent=body,fontSize=11.4,leading=19,spaceAfter=5,textColor=HexColor(TEAL))}
 c=Canvas(str(a.output),pagesize=A4,invariant=1);c.setTitle('GOSD 2026 · 第四章章首与 4.1 Agentic AI');c.setAuthor('GOSD / 全球开源发展报告');page=0;layout=[]
 def t(s,style='body'):return (s,style)
 def pageout(items,wide=False):
  nonlocal page
  page+=1;size=landscape(A4) if wide else A4;w,h=size;c.setPageSize(size);y=h-64;cw=w-92
  c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第四章 全球开源技术全景洞察')
  for item in items:
   if isinstance(item,tuple):
    text,style=item;para=common.paragraph(text,styles[style]);_,hh=para.wrap(cw,1000);assert y-hh>=57,(page,text[:35],y,hh);para.drawOn(c,46,y-hh);layout.append({'page':page,'text':text,'y':y,'height':hh});y-=hh+styles[style].spaceAfter
    if style in ['title','heading']:
     key='h'+str(len(layout));c.bookmarkPage(key);c.addOutlineEntry(text,key,0 if style=='title' else 1,False)
   else:
    assert y-item.height>=57,(page,item.title,y,item.height);item.paint(c,46,y,item.width);y-=item.height+10
  c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.setFillColor(HexColor(MUTED));c.drawString(46,28,'第四章章首与 4.1 Agentic AI');c.drawRightString(w-46,28,str(page));c.showPage()
 pageout([t(p.CHAPTER_TITLE,'title'),t(p.CHAPTER_QUESTION,'heading'),t(p.CHAPTER_INTRO),*[t('**'+h+'。**'+b) for h,b in p.CHAPTER_OBSERVATIONS],guide(),t(p.PERIOD,'note')])
 pageout([t('4.1 '+p.TITLE,'title'),t(p.INTRO),t('研究问题：'+p.QUESTION),t('指标定位：'+p.POSITION,'note'),t('核心发现：'+p.FINDING),t(p.STORIES[0][1],'heading'),*[t(x) for x in p.STORIES[0][2]],t(p.NOTES[0],'note'),t('观测窗口：2025-03—2026-08。当前分类回溯，未观测与尚未创建均不补零。','note')])
 pageout([architecture(1)],True);pageout([architecture(2)],True)
 pageout([t(p.STORIES[1][1],'heading'),t(p.STORIES[1][2][0]),rank(),t(p.STORIES[1][2][1])])
 pageout([overview(),compare(),t(p.HISTORY_NOTE)])
 pageout([projects(),t(p.STORIES[1][2][2]),t(p.STORIES[2][1],'heading'),t(p.STORIES[2][2][0]),concentration()])
 pageout([t(p.STORIES[2][2][1]),shift(),t(p.STORIES[2][2][2])])
 pageout([t(p.STORIES[3][1],'heading'),t(p.STORIES[3][2][0]),countrymap(),countrydetail()])
 pageout([dots(11),t(p.STORIES[3][2][1]),dots(12,True)])
 pageout([countrytrend(),t(p.STORIES[3][2][2]),t(p.ACTION_TITLE,'heading'),*[z for h,b in p.ACTIONS for z in [t(h,'action'),t(b)]],t(p.BRIDGE)])
 c.save();(work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2));doc=fitz.open(a.output);print(f'{a.output}: {len(doc)} pages, {a.output.stat().st_size:,} bytes')
if __name__=='__main__':main()
