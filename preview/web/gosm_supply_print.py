"""Private 5.1 publication PDF, sharing prose, source records and map geometry."""
from pathlib import Path
import argparse,json,math,re
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
import chapter1_print as common
import vmap_print as vp
import gosm_content as G
import gosm_supply_content as P

ROOT=Path(__file__).resolve().parents[2]
INK,MUTED,LINE,TEAL=vp.INK,vp.MUTED,vp.LINE,vp.TEAL
BLUE,GOLD,MAP='#167D91','#B4792E','#156993'
W,LW=A4[0]-92,A4[1]-92
D=G.payload();O=D['supply51'];T=P.TOPIC
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/05/#s51-evidence'
fmt=lambda n:f'{n:,.0f}'
def compact(n):
    return f'{n/1e8:.2f}亿' if n>=1e8 else f'{n/1e4:.2f}万' if n>=1e4 else fmt(n)
def country(asset,code):return next(r for r in O['assets'][asset]['countries'] if r['code']==code)
def blend(color,a):
    rgb=[int(color[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{round(255+(v-255)*a):02x}' for v in rgb)
def figure(key,height,width=W,suffix=''):
    num,title,_,_=P.FIGS[key]
    return vp.Figure(title,f'图 {num}'+suffix,width,height)
def mapdraw(f,scope,rows,k,x,y,w,h):
    geo=O['geometry'][scope];coords=[]
    for g in geo:
        vals=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',g['d'])];coords+=list(zip(vals[::2],vals[1::2]))
    xmin,xmax=min(a for a,b in coords),max(a for a,b in coords);ymin,ymax=min(b for a,b in coords),max(b for a,b in coords)
    scale=min(w/(xmax-xmin),h/(ymax-ymin));ox=x+(w-(xmax-xmin)*scale)/2-xmin*scale;oy=y+(h-(ymax-ymin)*scale)/2-ymin*scale
    by={r['code']:r for r in rows};mx=max(r[k] for r in rows)
    for g in geo:
        r=by.get(g['id'] if scope=='world' else g.get('source_code'))
        fill=blend(MAP,.12+.83*math.log1p(r[k])/math.log1p(mx)) if r and r['organizations'] else '#f1f4f6'
        f.path(g['d'],ox,oy,scale,None if g.get('kind')=='line' else fill,'#a7b7c1',.35)
    wanted=['CN','US','FR','IN','BR'] if scope=='world' else ['110000','330000','310000','440000','710000']
    for g in geo:
        if g['id'] not in wanted:continue
        xx,yy=g['center'];xx=ox+xx*scale;yy=oy+yy*scale
        if scope=='china':
            dx,dy={'310000':(24,-9),'330000':(-10,16),'710000':(20,6)}.get(g['id'],(0,0));f.line([(xx,yy),(xx+dx,yy+dy)],MUTED,.4);xx+=dx;yy+=dy
        text=g['name'].replace('省','').replace('市','')
        f.rect(xx-len(text)*4.3-2,yy-9,len(text)*8.6+4,12,'#ffffff','#ffffff',1);f.text(xx,yy,text,8.6,INK,'center')

def series(f,rows,x,y,w,h,title,color,value_key,annual=False):
    vals=[r[value_key] for r in rows];mx=max(vals)*1.15;px=x+44;py=y+22;pw=w-56;ph=h-40
    f.text(x,y+9,title,10,color);f.text(x+w,y+9,compact(vals[-1]),10,INK,'right')
    for a in [0,.5,1]:
        yy=py+ph*(1-a);f.line([(px,yy),(px+pw,yy)],LINE,.4);f.text(px-6,yy+2.6,compact(mx*a),8,MUTED,'right')
    points=[(px+i*pw/(len(rows)-1),py+ph*(1-v/mx)) for i,v in enumerate(vals)];f.line(points,color,1.6)
    for i in [0,len(rows)-1]:
        date=rows[i].get('date',rows[i].get('month'));f.text(points[i][0],py+ph+13,date[:4] if annual else date[2:],8,MUTED,'left' if i==0 else 'right')
    if annual:
        f.text(x+130,y+9,f'较上年同日 +{100*(vals[-1]/vals[-2]-1):.1f}%',8.5,MUTED)

def world():
    f=figure('world',470,LW);a=O['assets']['models'];rows=a['countries']
    f.text(0,10,'地域组织样本 · 826 个账号 · 73,088 个模型 · 12,502 个配套数据集',10,TEAL)
    f.text(0,29,'模型数量的地域分布；2026-10-17 读取，接口未声明统一统计日',8.5,MUTED)
    mapdraw(f,'world',rows,'models',0,40,490,204)
    f.text(0,255,'对数色阶；灰白为样本未覆盖，不解释为零供给。',8,MUTED)
    x=510;f.text(x,28,'国家 / 地区',9,MUTED);f.text(LW,28,'模型数 / 样本份额',9,MUTED,'right')
    rank=sorted([r for r in rows if r['organizations']],key=lambda r:-r['models'])[:8]
    for i,r in enumerate(rank):
        yy=49+i*25;f.text(x,yy,str(i+1)+'  '+r['name_zh'],9.5);f.text(LW,yy,fmt(r['models'])+' / '+f'{100*r["models"]/a["summary"]["models"]:.1f}%',9.5,INK,'right');f.rect(x,yy+6,(LW-x)*r['models']/rank[0]['models'],2,BLUE,BLUE,0)
    f.line([(0,269),(LW,269)],LINE,.5)
    for i,(key,title,color) in enumerate([('models','年度回溯：模型仓库',BLUE),('publishers','年度回溯：发布账号',GOLD)]):series(f,D['supply'],i*(LW+24)/2,280,(LW-24)/2,77,title,color,key,True)
    for i,(key,title,color) in enumerate([('models','月度新增：模型仓库',BLUE),('datasets','月度新增：数据集',GOLD)]):series(f,O['global'][key]['monthlyNew'][-12:],i*(LW+24)/2,364,(LW-24)/2,76,title,color,'count')
    f.text(0,451,'年度：2026-09-13 可见样本回溯，各年均为 9 月 13 日。月度：截至 2026-07，末月完整性未说明。',8,MUTED)
    return f.caption()

def comparison(asset):
    ismodel=asset=='models';f=figure('cnus',426,suffix='（A）' if ismodel else '（B）');cn=country(asset,'CN');us=country(asset,'US');a=O['assets'][asset];aw=(W-12)/2
    f.text(0,12,('A  模型' if ismodel else 'B  配套数据集')+' · 同一地域组织样本 · 2026-10-17 读取',10,TEAL)
    metrics=[('activeProviders','有资产的发布账号','个账号'),(asset,'资产数量','个仓库'),('downloads','累计下载','次'),('likes','点赞','次')]
    for i,(k,label,unit) in enumerate(metrics):
        x=(i%2)*(aw+12);y=25+(i//2)*64;f.rect(x,y,aw,56,'#f5f9fb',LINE,4);f.text(x+10,y+14,label+' / '+unit,8.7,MUTED)
        for j,(name,row,color) in enumerate([('中国',cn,BLUE),('美国',us,GOLD)]):
            xx=x+10+j*aw/2;f.text(xx,y+32,name,8,color);f.text(xx+aw/2-15,y+32,compact(row[k]),10.1,color,'right');f.text(xx,y+47,f'样本份额 {100*row[k]/a["summary"][k]:.2f}%',8,MUTED)
    f.text(0,166,'发布账号按累计下载量排序；条形使用各国份额，分母包含本国全部关联账号。',8,MUTED)
    for j,(code,name,color) in enumerate([('CN','中国',BLUE),('US','美国',GOLD)]):
        x=j*(aw+12);c=country(asset,code);rows=sorted([r for r in O['organizationProfiles'] if r['countryCode']==code],key=lambda r:-r[asset]['downloads']);den=c['downloads'];top=c['concentration']['downloads']['top3Share']
        f.text(x,187,name,11,color);f.text(x+aw,187,f'前三账号 {100*top:.1f}%',10,color,'right')
        for i,r in enumerate(rows[:6]):
            y=207+i*24;label=r['name'];parts=common.wrap(label,aw-52,8.5);assert len(parts)<=2,label
            for n,s in enumerate(parts):f.text(x+15,y+n*9,s,8.5)
            f.text(x,y,str(i+1),8,MUTED);share=r[asset]['downloads']/den;f.text(x+aw,y,f'{100*share:.1f}%',9,INK,'right');f.rect(x+15,y+14,(aw-15)*share,2,color,color,0)
        px=x+20;py=359;pw=aw-28;ph=41;acc=0;points=[(px,py+ph)]
        for i,r in enumerate(rows):acc+=r[asset]['downloads'];points.append((px+pw*(i+1)/len(rows),py+ph*(1-acc/den)))
        f.line([(px,py+ph),(px+pw,py)],LINE,.6);f.line(points,color,1.1);f.text(x,py+4,'100%',8,MUTED);f.text(x,py+ph,'0',8,MUTED);f.text(px,py+ph+10,'0',8,MUTED);f.text(px+pw,py+ph+10,'100% 账号',8,MUTED,'right');f.text(x+40,py-4,'累计下载份额；斜线为等量参照',8,MUTED)
    return f.caption()

def china():
    f=figure('china',374);a=O['assets']['models'];rows=[r for r in a['divisions'] if r['parent_id']==':divisions/CN'];cn=country('models','CN');unknown={'code':'unassigned','name_zh':'省级归属待补',**cn['unassignedDivision']}
    f.text(0,11,'中国样本 · 147 个组织账号 · 6,093 个模型',10,TEAL);f.text(0,29,'135 个组织已有省级归属；12 个组织待补，保留全国分母。',8.3,MUTED)
    mapdraw(f,'china',rows,'models',0,48,302,246)
    f.text(0,309,'对数色阶；含台湾省及南海诸岛。未覆盖不表示零供给。',8,MUTED)
    x=320;f.text(x,52,'地区',8.5,MUTED);f.text(W,52,'模型 / 组织',8.5,MUTED,'right')
    ranking=sorted([r for r in rows if r['organizations']]+[unknown],key=lambda r:-r['models'])[:9]
    for i,r in enumerate(ranking):
        label=r['name_zh'] if r['code']=='unassigned' else r['name_zh'].replace('特别行政区','').replace('省','').replace('市','')
        y=75+i*25;f.text(x,y,label,8.8);f.text(W,y,fmt(r['models'])+' / '+str(r['organizations']),8.8,INK,'right');f.rect(x,y+7,(W-x)*r['models']/ranking[0]['models'],2,BLUE,BLUE,0)
    f.line([(0,324),(W,324)],LINE,.5)
    for i,(label,value) in enumerate([('京沪浙粤模型份额','88.8%'),('浙江模型累计下载','44.45 亿次'),('北京配套数据集','480 个')]):
        x=i*W/3;f.text(x,340,label,8.5,MUTED);f.text(x,356,value,11,TEAL)
    return f.caption()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
    common.font_setup(args.font,args.work,subset_text=P.manuscript()+json.dumps(O,ensure_ascii=False)+Path(__file__).read_text())
    body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=9)
    styles={'body':body,'title':ParagraphStyle('title',parent=body,fontSize=18,leading=28,spaceAfter=15),'heading':ParagraphStyle('heading',parent=body,fontSize=12.8,leading=21,spaceAfter=9,textColor=HexColor(TEAL)),'note':ParagraphStyle('note',parent=body,fontSize=9,leading=14,spaceAfter=8),'action':ParagraphStyle('action',parent=body,fontSize=11.4,leading=19,spaceAfter=6,textColor=HexColor(TEAL))}
    c=Canvas(str(args.output),pagesize=A4,invariant=1);c.setTitle('GOSD 2026 · 5.1 供给与贡献');c.setAuthor('GOSD / 全球开源发展报告');count=0;layout=[]
    def t(s,style='body'):return(s,style)
    def page(items,wide=False):
        nonlocal count
        count+=1;w,h=landscape(A4) if wide else A4;c.setPageSize((w,h));y=h-64;cw=w-92
        c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第五章 全球开源大模型发展洞察')
        for item in items:
            if isinstance(item,tuple):
                text,style=item;para=common.paragraph(text,styles[style]);_,hh=para.wrap(cw,1000);assert y-hh>=57,(count,text[:30],y,hh);para.drawOn(c,46,y-hh);layout.append({'page':count,'text':text,'y':y,'height':hh});y-=hh+styles[style].spaceAfter
                if style in ['title','heading']:key='p'+str(len(layout));c.bookmarkPage(key);c.addOutlineEntry(text,key,0 if style=='title' else 1,False)
            else:
                assert y-item.height>=57,(count,item.title,y,item.height);item.paint(c,46,y,item.width);y-=item.height+11;key='fig'+str(count);c.bookmarkPage(key);c.addOutlineEntry(item.label+' '+item.title,key,2,False)
        if count==2:
            c.setFont(common.FONT,8);c.setFillColor(HexColor(TEAL));c.drawString(46,49,'口径与来源：固定快照、样本覆盖与原始记录（在线）');c.linkURL(WEB,(46,46,350,58),relative=0,thickness=0)
        c.setStrokeColor(HexColor(LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.setFillColor(HexColor(MUTED));c.drawString(46,28,'5.1 供给与贡献');c.drawRightString(w-46,28,str(count));c.showPage()
    page([t('5.1 供给与贡献','title'),t(T['lede']),t('研究问题：'+T['question']),t('指标定位：'+T['metric'],'note'),t('核心发现：'+T['core_finding']),t(T['window_note'],'note'),t(T['narratives'][0][0],'heading'),*[t(s) for s in T['insights']['world']]])
    page([world()],True)
    page([t(T['narratives'][1][0],'heading'),t(T['insights']['cnus'][0]),comparison('models')])
    page([t(T['insights']['cnus'][1]),comparison('datasets'),t(T['insights']['cnus'][2])])
    page([t(T['narratives'][2][0],'heading'),t(T['insights']['china'][0]),china(),t(T['insights']['china'][1])])
    page([t(T['insights']['china'][2]),t(T['action_lead'],'heading'),*[z for who,title,body,key in T['actions'] for z in [t(who+'：'+title,'action'),t(body+T['action_followups'][key])]],t(P.BRIDGE)])
    c.save();(args.work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2));print(f'{args.output}: {count} pages')

if __name__=='__main__':main()
