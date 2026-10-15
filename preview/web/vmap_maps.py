"""SVG geography and linked comparison surfaces for the V-Map chapter."""
from pathlib import Path
import json,html,math
ROOT=Path(__file__).resolve().parents[1]
GEO=json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
E=lambda s:html.escape(str(s),quote=True)
COLORS=['var(--gv-m0,#DCEBF2)','var(--gv-m1,#BCD8E4)','var(--gv-m2,#8FBFD3)','var(--gv-m3,#5B9FBE)','var(--gv-m4,#337FA6)','var(--gv-m5,#156993)']
def number(v):
    if v is None:return '—'
    if 0<v<.01:return '＜0.01'
    return f'{math.trunc(v*100+math.copysign(1e-8,v))/100:,.2f}'
def map_svg(scope,data,standalone=False,prefix=None):
    rows=data['countries'] if scope=='world' else data['provinces'];by={r['id']:r for r in rows};maximum=max(r['active'] or 0 for r in rows)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 470" preserveAspectRatio="xMidYMid meet" data-map-svg="{scope}" role="group" aria-label="'+('世界地图，中国含台湾省' if scope=='world' else '中国省级地图，含台湾省及南海诸岛')+'"><rect width="880" height="470" fill="var(--gv-bg,#F3F8FA)"/>']
    for f in GEO[scope]:
        if f.get('kind')=='line':
            out.append('<path d="'+f['d']+'" fill="none" stroke="var(--muted,#4C697B)" stroke-width=".7" pointer-events="none"/>');continue
        r=by.get(f['id']);v=r.get('active') if r else None;c=('var(--paper,#fff)' if f['id']=='100000_JD' else 'var(--vm-empty,#E6E8EA)') if v is None else COLORS[min(5,int(v/maximum*5.999))]
        attrs=f' data-map-center="{f["center"][0]},{f["center"][1]}" data-map-id="{f["id"]}" data-map-name="{E(f["name"])}" fill="{c}" stroke="var(--line,#B9CDD8)" stroke-width=".65" fill-rule="evenodd" role="button" tabindex="{0 if r else -1}" aria-label="{E(f["name"])}，活跃开发者{number(v)}万人"'
        out.append('<path d="'+f['d']+'"'+attrs+'><title>'+E(f['name'])+' · '+('未收录' if v is None else number(v)+' 万人')+'</title></path>')
    labels=['US','CN','BR','IN','ID'] if scope=='world' else ['110000','310000','440000','710000','510000']
    for code in labels:
        f=next(x for x in GEO[scope] if x['id']==code);x,y=f['center'];label=f['name'].replace('市','').replace('省','')
        # Beijing, Shanghai and Taiwan remain separate selectable locations.
        width=len(label)*14+8
        out.append(f'<g pointer-events="none"><rect x="{x-width/2}" y="{y-16}" width="{width}" height="22" rx="3" fill="var(--paper,#fff)" fill-opacity=".9"/><text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="var(--ink,#10334D)">{label}</text></g>')
    out.append('</svg>');return ''.join(out)

def ranking(rows,key):
    rr=sorted((r for r in rows if r[key] is not None),key=lambda r:-r[key])[:10]
    return ''.join(f'<button type="button" data-map-row="{r["id"]}" data-rank-metric="{key}" aria-pressed="false"><span>{i+1:02}</span><strong>{E(r["name"])}</strong><b>{number(r[key])}</b><i style="width:{r[key]/rr[0][key]*100:.4f}%"></i></button>' for i,r in enumerate(rr))

def detail(row,national,scope="world"):
    return '<span class="vm-card-label">所选地区 · '+E(row['name'])+'</span><div class="vm-pair"><span>总量<b>'+number(row['total'])+'</b></span><span>活跃<b>'+number(row['active'])+'</b></span></div><p>活跃份额 '+f'{row["active"]/national*100:.1f}%'+(' · 占中国全国值' if scope=='china' else ' · 占全球值')+'</p>'

def sparkline(values,width=150,height=35):
    lo=min(values);hi=max(values);span=hi-lo or 1
    pts=[(4+i*(width-8)/(len(values)-1),height-4-(v-lo)/span*(height-8)) for i,v in enumerate(values)]
    line=' '.join(('M' if i==0 else 'L')+str(round(x,2))+','+str(round(y,2)) for i,(x,y) in enumerate(pts))
    dots=''.join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2" fill="var(--cyan,#156993)"><title>{2021+i}：{number(v/10000)} 万人</title></circle>' for i,((x,y),v) in enumerate(zip(pts,values)))
    return f'<svg class="vm-sparkline" viewBox="0 0 {width} {height}" role="img" aria-label="2021至2025自然年趋势"><path d="{line}" fill="none" stroke="var(--cyan,#156993)" stroke-width="2"/>{dots}</svg>'

def cards(scope,data):
    if scope=='china':
        total=next(r['active'] for r in data['countries'] if r['id']=='CN');rr=sorted(data['provinces'],key=lambda r:-r['active'])
        top=sum(r['active'] for r in rr[:3]);middle=sum(r['active'] for r in rr[3:10]);rest=sum(r['active'] for r in rr[10:])
        first='<span class="vm-card-label">中国活跃规模 · 同源五年趋势</span><div class="vm-national-trend"><strong class="vm-big">234.46<small> 万</small></strong>'+sparkline(data['snapshot_trends'][2]['values'])+'</div><p>2021—2025自然年 · 国内约120万另列情景。</p>'
        second='<span class="vm-card-label">区域参与结构 · 34个省级地区</span><div class="vm-stack">'+''.join(f'<i style="width:{v/total*100}%;background:var(--gv-s{i},#156993)"></i>' for i,v in enumerate([top,middle,rest]))+'</div><div class="vm-shares">'+''.join(f'<span>{n}<b>{v/total*100:.1f}%</b></span>' for n,v in [('京沪粤',top),('第4—10位',middle),('其余24地',rest)])+'</div><p>省级合计与全国一致；总量字段为平台估计值。</p>'
        third=detail(rr[0],total,'china')
    else:
        first='<span class="vm-card-label">全球规模与趋势 · 2021—2025</span><div class="vm-pair vm-with-sparks"><span>开发者总量<b>约1.80亿</b>'+sparkline(data['snapshot_trends'][0]['values'],150,28)+'</span><span>活跃开发者<b>2,762.10万</b>'+sparkline(data['snapshot_trends'][1]['values'],150,28)+'</span></div>'
        second='<span class="vm-card-label">全球南方观察样本 · 活跃万人</span><div class="vm-south">'+''.join('<button type="button" data-map-row="'+r['id']+'"><span>'+r['name']+'</span><i style="width:'+str(r['active']/273.28*100)+'%"></i><b>'+number(r['active'])+'</b></button>' for r in data['countries'] if r['id'] in ['IN','BR','ID'])+'</div>'
        third=detail(next(r for r in data['countries'] if r['id']=='CN'),data['global_active'])
    return f'<article data-map-card="overview">{first}</article><article data-map-card="structure">{second}</article><article data-map-card="detail" aria-live="polite">{third}</article>'

def body(scope,data):
    rows=data['countries'] if scope=='world' else data['provinces']
    controls='<div class="vmap-controls vm-map-controls"><div role="group" aria-label="地图着色指标"><button type="button" data-map-metric="total" aria-pressed="false">开发者总量</button><button type="button" data-map-metric="active" aria-pressed="true">活跃开发者</button></div>'
    if scope=='world':controls+='<div role="group" aria-label="地理范围"><button type="button" data-map-scope="world" aria-pressed="true">全球</button><button type="button" data-map-scope="china" aria-pressed="false">中国下钻 ↘</button></div>'
    else:controls+='<a class="vm-back" href="#fig-vmap-global">↑ 返回全球全景</a>'
    controls+='</div>'
    layers=''.join('<div data-map-layer="'+s+'"'+(' hidden' if s!=scope else '')+'>'+map_svg(s,data,prefix=scope+"-"+s)+'</div>' for s in (['world','china'] if scope=='world' else ['china']))
    return controls+'<div class="vm-map-meta"><span>OpenDigger / OpenShare · GitHub · 2025自然年</span><span data-map-context>'+('全球 · 同版国家／地区底表' if scope=='world' else '中国 · 34个省级地区')+' · 缺失不等于零</span></div><div class="vm-map-layout"><aside class="vm-rank"><h5>开发者总量 <small>万人 · 前十</small></h5><div data-map-rank="total">'+ranking(rows,'total')+'</div></aside><div class="vm-map-center">'+layers+'<div class="vm-map-zoom" role="group" aria-label="地图缩放"><button type="button" data-map-zoom="in" aria-label="放大所选地区">＋</button><button type="button" data-map-zoom="out" aria-label="缩小地图">−</button><button type="button" data-map-zoom="reset">复位</button></div><div class="vm-map-readout" role="status" aria-live="polite" data-map-readout>悬停查看 · 点击锁定地区'+(' · 点击中国下钻' if scope=='world' else '')+'</div></div><aside class="vm-rank"><h5>活跃开发者 <small>万人 · 前十</small></h5><div data-map-rank="active">'+ranking(rows,'active')+'</div></aside></div><div class="vm-map-legend"><span class="vm-scale"></span><span data-map-scale>线性色阶：0—'+number(max(r['active'] or 0 for r in rows))+' 万人</span><i></i><span>未收录</span><span class="vm-unit-note">中国含台湾省 · 省级不分摊国内补充量</span></div><div class="vm-map-cards">'+cards(scope,data)+'</div>'
