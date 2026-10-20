"""Reproduce the user-selected previous snapshot and original manuscript; observed flows stay immutable."""
from pathlib import Path
import csv,json,hashlib
from build_cmap_flows import build_flows
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'content/cmap';SRC=BASE/'source'
def read(name):return json.loads((SRC/name).read_text())
def build():
    meta=read('calendar-meta.json');assert meta['period']['start']=='2025-01-01' and meta['period']['endExclusive']=='2026-01-01'
    contribution=read('calendar-contribution.json');cn=read('calendar-CN-contribution.json')
    geo=json.loads((ROOT/'content/vmap/map-geometry.json').read_text());spec=json.loads((ROOT/'content/vmap/map-provenance.json').read_text())['scopes']['world']
    positions={g['id']:[(g['center'][0]-spec['offset'][0])/spec['uniform_scale']/.75+spec['geographic_bounds'][0],spec['geographic_bounds'][3]-(g['center'][1]-spec['offset'][1])/spec['uniform_scale']] for g in geo['world'] if g.get('kind')!='line'}
    def rows(source,dev,scope):
        active={r['code']:r for r in dev['leaderboards'][1]['data']};names={f['name']:f['id'] for f in geo['china']};out=[]
        for r in source['leaderboards'][0]['data']:
            a=active.get(r['code']);code=r['code'] if scope=='world' else names[r['name_zh']]
            out.append(dict(id=code,source_code=r['code'],name=r['name_zh'],en=r['name'],value=r['value'],change=r['change'],growth=r['change']/(r['value']-r['change'])*100 if r['value']!=r['change'] else None,rank=r['rank'],active=a['value'] if a else None,active_rank=a['rank'] if a else None,average=r['value']/a['value'] if a and a['value'] else None,coordinates=positions.get(code) if scope=='world' else None))
        return out
    countries=rows(contribution,read('calendar-developers.json'),'world');provinces=rows(cn,read('calendar-CN-developers.json'),'china');by={r['id']:r for r in countries}
    members=['BR','ID','VN','PH','EG','ZA'];south={k:sum(by[c][k] for c in members) for k in ['value','active','change']};south.update(id='SOUTH6',name='全球南方六国',members=members)
    legacy=list(csv.DictReader((SRC/'repository-contribution-trend.csv').open()))
    data=dict(edition='2026-10-20-cmap-review2',period=meta['period'],updated_at=meta['summary']['updatedAt'],source='https://selfoss.open-digger.cn/openshare/overview/',platform='OpenShare geographic snapshot',metric='Developer OpenRank Contribution',countries=countries,provinces=provinces,south6=south,global_value=contribution['trends'][0]['values'][-1],global_region_sum=round(sum(r['value'] for r in countries),2),trends=dict(zip(['GLOBAL','US','CN'],contribution['trends'])),
        legacy={'years':[int(r['year']) for r in legacy],'labels':{'Europe':'欧洲','China':'中国','United States':'美国','Global South representatives':'全球南方六国','India':'印度'},'series':{k:[float(r[k]) for r in legacy] for k in legacy[0] if k!='year'},'status':'编制组五域综合统计 · 2022—2026报告年度'},
        average_status='同一报告年度、同一平台的地区贡献度除以活跃开发者；全部34地保留，分母不足1000标注小基数。',
        globe_edges_status='observed_sample_with_uniform_visual_enhancement',flows=build_flows(BASE,countries,legacy))
    for k,m in [('GLOBAL',22000000),('US',5000000),('CN',1500000)]:data['trends'][k]['axis_max']=m
    refs=list(csv.DictReader((SRC/'repository-province-average.csv').open()))
    name_ids={r['name']:r for r in provinces}
    data['province_average_reference']=[dict(id=name_ids[r['region']]['id'],source_code=name_ids[r['region']]['source_code'],name=r['region'],en=name_ids[r['region']]['en'],rank=int(r['rank']),average=float(r['openrank'])/float(r['active_developers']),value=float(r['openrank']),active=float(r['active_developers']),source='original_manuscript_top10') for r in refs]
    data['average_status']='原稿平均贡献Top10单独呈现，不与地图快照拼接或外推至其余地区。'
    (BASE/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    for name,rr in [('countries',countries),('provinces',provinces)]:
        with (BASE/(name+'.csv')).open('w',newline='') as f:
            keys=['id','name','value','change','growth','rank','active','active_rank','average'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rr)
    source_names=['calendar-meta.json','calendar-contribution.json','calendar-CN-contribution.json','calendar-developers.json','calendar-CN-developers.json','repository-contribution-trend.csv','repository-project-sources.csv','repository-province-average.csv']
    provenance=dict(retrieved_date='2026-10-15',restored_on='2026-10-20',restoration_basis='用户指定回到上一版地图快照及原稿；恢复236地区、34省级地区与原五年序列。',sources=[{'file':'source/'+name,'sha256':hashlib.sha256((SRC/name).read_bytes()).hexdigest()} for name in source_names],source_root=data['source'],report_period=meta['period'],geometry_reference='../vmap/map-provenance.json',accepted_report_series='data/processed/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.csv',claim_scope='中国高于美国限于原稿2026报告年度五域开发者贡献度汇总。地图为2025自然年快照，未据此建立同年平台拆分。',globe_network='20 observed sample relationships; no estimated sources; all rendering widths use a common optional multiplier of 3.',archived_sources='report-* retain the superseded report-year snapshot; not used in the current maps.',upstream_scope='保留原快照数值；不再将接口断言为纯GitHub原始统计。计算规则与平台构成不由本次排版更改。',mechanism='The restored fictional mechanism is isolated from observed source-flow data.')
    (BASE/'provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'countries':len(countries),'provinces':len(provinces),'global':data['global_value'],'CN':by['CN']['value'],'US':by['US']['value'],'observed_edges':len(data['flows']['edges'])},ensure_ascii=False))
if __name__=='__main__':build()
