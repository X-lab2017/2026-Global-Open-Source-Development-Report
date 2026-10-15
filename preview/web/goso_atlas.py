"""Geographic reading layer. Report CSVs and the dated OpenShare display snapshot stay separate."""
from pathlib import Path
import json,html,math,shutil,re
import goso_content as g
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'content/goso-atlas'
E=lambda x:html.escape(str(x),quote=True)
GEO=json.loads((ASSETS/'geometry.json').read_text())
SNAP=json.loads((ASSETS/'open-share-snapshot.json').read_text())
ORIGINAL=json.loads((ASSETS/'originals.json').read_text())
COLORS=['var(--gv-m0, #DCEBF2)','var(--gv-m1, #BCD8E4)','var(--gv-m2, #8FBFD3)','var(--gv-m3, #5B9FBE)','var(--gv-m4, #337FA6)','var(--gv-m5, #156993)']
CITY={'北京':[116.4,39.9],'上海':[121.5,31.2],'杭州':[120.2,30.3],'深圳':[114.1,22.5],'台北':[121.6,25.0],'成都':[104.1,30.7],'广州':[113.3,23.1],'武汉':[114.3,30.6],'南京':[118.8,32.1],'苏州':[120.6,31.3]}
COUNTRIES={'China':'CN','United States':'US','Canada':'CA','Germany':'DE','Singapore':'SG','India':'IN','Czechia':'CZ','Sweden':'SE','Belgium':'BE','United Kingdom':'GB','France':'FR','Netherlands':'NL','Australia':'AU','Japan':'JP','Switzerland':'CH','Finland':'FI','Bulgaria':'BG','Poland':'PL'}
def pchina(lon,lat):return [round(80+(lon-73)*11.2,2),round(25+(54-lat)*10,2)]
def payload():
    out={'geometry':{scope:[{k:v for k,v in f.items() if k!='d'} for f in features] for scope,features in GEO.items()},'snapshot':SNAP,'cities':[],'flows':[],'assets':[]}
    for r in g.rows('cities'):
        city=r['city'];out['cities'].append({'id':city,'name':('台北（台湾省）' if city=='台北' else city),'value':int(r['talent_count']),'center':pchina(*CITY[city]),'series':[{'year':r2['year'],'value':int(r2[city])} for r2 in g.rows('talent')]})
    for r in g.rows('cross'):
        out['flows'].append({'id':COUNTRIES.get(r['developer_country'],r['developer_country']),'name':dict(g.LABELS, Bulgaria='保加利亚', Poland='波兰', Switzerland='瑞士').get(r['developer_country'],r['developer_country']),'target':COUNTRIES[r['project_country']],'value':float(r['openrank']),'share':float(r['share_pct'])})
    for r in g.rows('geography'):
        if r['region_code']:out['assets'].append({'id':r['region_code'],'name':r['country'],'models':int(r['models']),'downloads':int(r['downloads_all_time']),'likes':int(r['likes']),'share':float(r['models_known_share_pct'])})
    return out

def defs():
    return '<svg class="atlas-definitions" aria-hidden="true" width="0" height="0"><defs>'+''.join('<path id="geo-'+scope+'-'+E(f['id'])+'" d="'+f['d']+'"/>' for scope,fs in GEO.items() for f in fs)+'</defs></svg>'

def color(v,values):
    if v is None:return 'var(--gv-empty, #E0EBF0)'
    vv=sorted(x for x in values if x>0);cap=math.ceil(vv[min(len(vv)-1,int(len(vv)*.95))]) if vv else 1
    return COLORS[min(5,max(0,int(v/cap*5.999)))]

def default_rows(kind):
    p=payload()
    if kind in ('v','c','i'):
        metric={'v':'developers','c':'contribution','i':'influence'}[kind];return SNAP['sets'][metric+'-world']['rows']
    if kind=='t':return p['cities']
    if kind=='d':return [dict(x) for x in p['flows'] if x['target']=='CN']
    return [dict(x,value=x['models']) for x in p['assets']]

def static_map(kind,standalone=False):
    scope='china' if kind=='t' else 'world';rows=default_rows(kind);by={x['id']:x for x in rows};vals=[x['value'] for x in rows];fs=GEO[scope]
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 470" role="group" aria-label="交互地图，可通过地区列表查阅全部数值"><rect width="880" height="470" fill="var(--gv-bg, #F3F8FA)"/>']
    for y in [120,235,350]:parts.append(f'<path d="M25 {y}H855" stroke="var(--gv-split, #DDE9EE)" stroke-width=".5" stroke-dasharray="3 6"/>')
    for f in fs:
        row=by.get(f['id']);value=row['value'] if row else None;c=color(value,vals) if kind!='t' else 'var(--gv-empty, #E0EBF0)'
        tag='<path d="'+f['d']+'"' if standalone else '<use href="#geo-'+scope+'-'+E(f['id'])+'"'
        parts.append(tag+' fill="'+c+'" stroke="var(--gv-surface, #FFFFFF)" stroke-width=".6" fill-rule="evenodd" data-geo="'+E(f['id'])+'"><title>'+E(f['name'])+' · '+(E(row.get('display',g.fmt(value))) if row else '本视图未收录')+'</title></'+('path>' if standalone else 'use>'))
    if kind=='d':
        to=next(f['center'] for f in fs if f['id']=='CN')
        for row in rows:
            fr=next((f['center'] for f in fs if f['id']==row['id']),None)
            if not fr or row['id']=='CN':continue
            x,y=fr;xx,yy=to;mid=(x+xx)/2;raiseby=min(140,abs(xx-x)*.22+30)
            parts.append(f'<path d="M{x},{y} Q{mid},{min(y,yy)-raiseby} {xx},{yy}" fill="none" stroke="var(--gv-s0, #156993)" stroke-opacity=".65" stroke-width="{1+math.sqrt(row['value']/max(vals))*9}"><title>{E(row['name'])} → 中国 · {row['share']}%</title></path>')
    if scope=='china':parts.append('<rect x="690" y="260" width="135" height="188" fill="none" stroke="var(--gv-muted, #4C697B)" stroke-width=".7"/><text x="700" y="465" font-size="11" fill="var(--gv-muted, #4C697B)">南海诸岛</text>')
    if kind=='t':
        for row in rows:
            x,y=row['center'];rr=math.sqrt(row['value']/max(vals))*18
            parts.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="var(--gv-s0, #156993)" fill-opacity=".8" stroke="white" stroke-width="1.5" data-geo="{row["id"]}"><title>{row["name"]} · {row["value"]} 人</title></circle>')
    for code,label in ([('US','美国'),('CN','中国'),('BR','巴西'),('IN','印度'),('AU','澳大利亚')] if scope=='world' else []):
        f=next((f for f in fs if f['id']==code),None)
        if f:parts.append(f'<text x="{f["center"][0]}" y="{f["center"][1]}" fill="var(--gv-ink, #10334D)" font-size="12" text-anchor="middle" stroke="var(--gv-surface, #FFFFFF)" stroke-width="3" paint-order="stroke">{label}</text>')
    if standalone:
        parts[0]=parts[0].replace('0 0 880 470','0 0 880 540').replace('height="470"','height="540"')
        positive=sorted(v for v in vals if v>0);cap=math.ceil(positive[min(len(positive)-1,int(len(positive)*.95))]) if positive else 1
        label='圆面积 = 人才数量；固定十城市' if kind=='t' else '线宽 = 贡献度；表列来源' if kind=='d' else f'线性色阶 0—{cap:,}；P95 封顶，≥上限同色；未收录不等于零'
        period='OpenShare 2026-10 页面快照；显示值保留原精度' if kind in 'vci' else '2026-09-13 模型快照' if kind=='a' else 'GOSD 仓库底表；统计范围见本章'
        parts.append(f'<text x="24" y="493" fill="var(--gv-ink, #10334D)" font-size="12">GOSO · {E(label)}</text><text x="24" y="517" fill="var(--gv-muted, #4C697B)" font-size="10">{E(period)}</text>')
    parts.append('</svg>')
    import goso_brand
    return goso_brand.resolve(''.join(parts)) if standalone else ''.join(parts)

TITLES={'v':'开发者在哪里？','c':'协作贡献在哪里产生？','i':'项目影响力在哪里集聚？','t':'核心人才，落在城市网络上','d':'从开发者所在地，连接到项目归属地','a':'从发布规模，看模型供给的地理分布'}
METRICS={'v':'developers','c':'contribution','i':'influence','t':'talent','d':'flows','a':'models'}

def panel(kind):
    rows=default_rows(kind);fid='atlas-'+kind;snapshot=kind in ('v','c','i')
    source=SNAP['source'] if snapshot else g.source({'t':'cities','d':'cross','a':'geography'}[kind])
    period='OpenShare 页面快照 · 2026-10' if snapshot else {'t':'2026 年 7 月 · 固定十城市样本','d':'2026 报告年 · 中美项目样本','a':'2026-09-13 · 地域已识别模型'}[kind]
    opts=(([('developers','开发者总量'),('active','活跃开发者')] if kind=='v' else [('contribution','OpenRank 贡献度')] if kind=='c' else [('influence','OpenRank 影响力')]) if snapshot else {'t':[('talent','城市人才')],'d':[('flows','跨地域贡献流向')],'a':[('models','模型数量'),('downloads','累计下载'),('likes','点赞')]}[kind])
    tabs=''.join(f'<button type="button" data-atlas-metric="{k}" aria-pressed="{str(k==METRICS[kind]).lower()}">{t}</button>' for k,t in opts)
    scope='china' if kind=='t' else 'world'
    options=''.join(f'<option value="{E(r["id"] or r["name"])}">{E(r["name"])}</option>' for r in rows)
    note=('从 OpenShare 公开排行榜固定记录；保留页面显示精度，带“万”的数值为近似读数。地图只着色已收录条目，灰色不代表零。此快照不替代 2026 报告年度底表，平台差值未用于报告同比。' if snapshot else {'t':'圆面积表示人数；城市位置为示意点位。2026 值对应 7 月快照，切换年份展示固定十城市的原始序列。其他城市未收录，不代表没有开源人才。','d':'弧线从贡献者所在地指向所选项目归属地；宽度表示 OpenRank 贡献度，表示协作关系而非人员迁移。前十来源之外的份额不补零、不重归一化。','a':'地图仅覆盖 52 个已识别国家的 71,578 个模型。全部 3,062,151 个模型中，97.66% 的国家归属未知，单独保留；不可把已识别样本份额称作全球份额。'}[kind])
    result=f'''<figure class="atlas-panel" id="{fid}" data-atlas="{kind}" data-default-metric="{METRICS[kind]}" aria-labelledby="{fid}-title">
    <div class="atlas-heading"><div><span class="eyebrow">GOSO / SPATIAL OBSERVATION</span><h3 id="{fid}-title">{TITLES[kind]}</h3></div><span class="atlas-period">{period}</span></div>
    <div class="atlas-toolbar" data-atlas-enhanced hidden><div class="atlas-metrics" role="group" aria-label="地图观察维度">{tabs}</div>
    {('<div class="atlas-scope" role="group" aria-label="地理层级"><button type="button" data-scope="world" aria-pressed="true">← 全球</button><button type="button" data-scope="china" aria-pressed="false">中国省级 ↘</button></div>' if snapshot else '<label class="atlas-target">项目归属 <select data-atlas-target><option value="CN">中国项目</option><option value="US">美国项目</option></select></label>' if kind=='d' else '')}</div>
    <div class="atlas-context"><span data-atlas-context>{'全球 · '+str(len(rows))+' 个排行榜条目' if snapshot else period}</span><span data-atlas-hint>{'点选中国进入省级观察' if kind in ('v','c') else '悬停读数 · 点击锁定地区'}</span></div>
    <div class="atlas-workspace"><div class="atlas-map-wrap"><div class="atlas-map" data-atlas-map>{static_map(kind)}</div><div class="atlas-zoom" data-atlas-enhanced hidden><button type="button" data-zoom="in" aria-label="放大地图">＋</button><button type="button" data-zoom="out" aria-label="缩小地图">−</button><button type="button" data-zoom="reset" aria-label="重置地图">↺</button></div><div class="atlas-tooltip" role="status" data-atlas-tooltip hidden></div><div class="atlas-legend" data-atlas-legend><i></i><span>低 → 高 · P95 封顶；超过上限同色，原值见读数</span><b></b><span>本视图未收录</span></div></div>
    <aside class="atlas-ranking"><div class="atlas-ranking-head"><strong data-rank-title>地区读数</strong><label><span class="sr-only">查找地区</span><input type="search" data-atlas-search placeholder="查找国家 / 地区" aria-label="查找国家或地区"></label></div><div class="atlas-rank-list" data-atlas-ranking>{''.join('<button type="button" data-select="'+E(r['id'] or r['name'])+'"><span>'+str(i+1).zfill(2)+'</span><strong>'+E(r['name'])+'</strong><b>'+E(r.get('display',g.fmt(r['value'])))+'</b></button>' for i,r in enumerate(rows))}</div></aside></div>
    <div class="atlas-detail" data-atlas-detail aria-live="polite"><span>READ THE MAP</span><strong>{'从地图认识分布，从年度底表理解变化。' if snapshot else '选择地区，查看原始数值与统计范围。'}</strong></div>
    {'<div class="atlas-year" data-atlas-enhanced hidden><label>年份 <output data-atlas-year-label>2026</output><input type="range" min="2022" max="2026" value="2026" step="1" aria-label="人才观察年份" data-atlas-year></label></div>' if kind=='t' else ''}
    <figcaption><details class="atlas-data-note"><summary>统计范围与读数说明</summary><p data-atlas-note>{note}</p></details><div class="atlas-links"><a href="{source}" target="_blank" rel="noopener">{'OpenShare 原始平台' if snapshot else 'GitHub 数据底表'} ↗</a><a href="/assets/goso-atlas/{'open-share-snapshot.json' if snapshot else 'map-data.json'}" download>地图数据 JSON ↓</a><button type="button" data-atlas-export hidden>导出当前地图 SVG ↓</button><button type="button" data-atlas-share hidden>复制当前视图链接</button><span data-atlas-status role="status"></span></div><details class="atlas-provenance"><summary>地图与数据来源说明</summary><p>底图：<a href="https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/" target="_blank" rel="noopener">Natural Earth 1:50m</a>；中国省级底图：<a href="https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json" target="_blank" rel="noopener">DataV.GeoAtlas</a>。全球地图统一以中国呈现，中国省级视图包含台湾省、香港特别行政区和澳门特别行政区。统计范围由本图数据来源定义；快照捕获、显示精度及原图页码见 <a href="/assets/goso-atlas/README.md">来源记录</a>。</p></details></figcaption>
    <noscript><p>地图与地区读数已展示；启用 JavaScript 可切换维度、下钻和筛选。</p></noscript></figure>'''
    return re.sub(r'(?m)^[ \t]+$', '', result)

def original_gallery(kind):
    sec='2.'+str('vcitdga'.index(kind)+1);obj=ORIGINAL[sec]
    return '<details class="atlas-original"><summary>对照带图初稿 · '+str(len(obj['images']))+' 幅原图</summary><p>来自你提供的《'+E(obj['pdf'])+'》。保留原始图面用于核对；时间、范围或数值存在差异时，以本页注明的底表和快照为准。</p><div class="atlas-original-grid">'+''.join('<a href="/assets/goso-atlas/original/'+im['file']+'" data-original-image><img loading="lazy" src="/assets/goso-atlas/original/'+im['file']+'" width="'+str(im['width'])+'" height="'+str(im['height'])+'" alt="带图初稿 '+sec+' · 原图 '+str(i+1)+'，PDF 第 '+str(im['page'])+' 页"><span>原图 '+str(i+1)+' · 点击放大 ↗</span></a>' for i,im in enumerate(obj['images']))+'</div></details>'

def governance():
    return '''<div class="atlas-governance" aria-label="治理与公共价值观察框架"><article><span>01 / 组织承载</span><strong>3,350</strong><p>基金会样本活跃仓库<br>2026 报告年</p><a href="#goso-g">观察数量与影响力份额 ↓</a></article><article><span>02 / 复用规则</span><strong>71,760</strong><p>MIT 许可样本活跃仓库<br>2026 报告年</p><a href="#goso-g">比较五类许可证 ↓</a></article><article><span>03 / 公共实践</span><strong class="atlas-pending">待补案例</strong><p>应用场景 → 长期维护 → 受益证据<br>与 SDGs 建立可查证的联系</p><a href="#goso-review">补充公共价值证据 →</a></article></div>'''

def export(out):
    target=out/'assets/goso-atlas';shutil.copytree(ASSETS,target,dirs_exist_ok=True)
    (target/'map-data.json').write_text(json.dumps(payload(),ensure_ascii=False,separators=(',',':')))
    for kind in 'vcitda':(target/(kind+'-map.svg')).write_text(static_map(kind,True))
