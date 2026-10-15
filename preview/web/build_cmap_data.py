"""Build traceable C-Map data and a source-aligned globe surface, with separated observed and scenario flows."""
from pathlib import Path
import csv,json,hashlib,math
from build_vmap_geometry import in_ring,centroid

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'content/cmap';SRC=BASE/'source'
def read(name):return json.loads((SRC/name).read_text())
def build():
    contribution=read('calendar-contribution.json');cn=read('calendar-CN-contribution.json')
    developers=read('calendar-developers.json');cn_developers=read('calendar-CN-developers.json')
    geo=json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
    spec=json.loads((ROOT/'content/vmap/map-provenance.json').read_text())['scopes']['world']
    positions={}
    for f in geo['world']:
        positions[f['id']]=[(f['center'][0]-spec['offset'][0])/spec['uniform_scale']/.75+spec['geographic_bounds'][0],spec['geographic_bounds'][3]-(f['center'][1]-spec['offset'][1])/spec['uniform_scale']]
    def rows(source,dev,scope):
        active={r['code']:r for r in dev['leaderboards'][1]['data']}
        byname={f['name']:f['id'] for f in geo['china']}
        out=[]
        for r in source['leaderboards'][0]['data']:
            a=active.get(r['code']);code=r['code'] if scope=='world' else byname.get(r['name_zh'])
            assert code,r
            out.append(dict(id=code,source_code=r['code'],name=r['name_zh'],en=r['name'],value=r['value'],change=r['change'],growth=r['change']/(r['value']-r['change'])*100 if r['value']!=r['change'] else None,rank=r['rank'],active=a['value'] if a else None,active_rank=a['rank'] if a else None,average=r['value']/a['value'] if a and a['value'] else None,coordinates=positions.get(code) if scope=='world' else None))
        return out
    countries=rows(contribution,developers,'world');provinces=rows(cn,cn_developers,'china');by={r['id']:r for r in countries}
    members=['BR','ID','VN','PH','EG','ZA'];south={k:sum(by[c][k] for c in members) for k in ['value','active','change']};south.update(id='SOUTH6',name='全球南方六国',members=members,growth=south['change']/(south['value']-south['change'])*100)
    legacy=list(csv.DictReader((SRC/'repository-contribution-trend.csv').open()))
    influences={r['code']:r for r in read('calendar-influence-reference.json')['leaderboards'][0]['data']}
    data={'period':read('calendar-meta.json')['period'],'updated_at':read('calendar-meta.json')['summary']['updatedAt'],'source':'https://open-share.com/insight/open-world/gosd','platform':'GitHub','metric':'Developer OpenRank Contribution','metric_mapping_status':'Source label retained; community/global algorithm and annual aggregation awaiting verification for formal OSDI mapping.','countries':countries,'provinces':provinces,'south6':south,'global_value':contribution['trends'][0]['values'][-1],'global_region_sum':round(sum(r['value'] for r in countries),2),'trends':{'GLOBAL':contribution['trends'][0],'US':contribution['trends'][1],'CN':contribution['trends'][2]},'legacy':{'years':[int(r['year']) for r in legacy],'labels':{'Europe':'欧洲','China':'中国','United States':'美国','Global South representatives':'全球南方六国','India':'印度'},'series':{k:[float(r[k]) for r in legacy] for k in legacy[0] if k!='year'},'status':'原稿五域序列 · 平台、算法与年度聚合待对齐'},'project_reference':{'US':influences['US']['value'],'CN':influences['CN']['value'],'ratio_us_cn':influences['US']['value']/influences['CN']['value'],'period':'2025 natural year','metric':'Project OpenRank Influence'},'average_status':'同版数值相除的探索性诊断；分子与活跃分母对象范围待核，不是正式 OSDI 测算。','globe_edges_status':'conceptual_network_and_observed_sample_with_optional_residual_scenario'}
    from build_cmap_flows import build_flows
    data['flows']=build_flows(BASE,countries,legacy)
    data['legacy']['status']='报告采用的 2022—2026 五域口径；平台与聚合细则在方法说明中补充。'
    (BASE/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    for name,rr in [('countries',countries),('provinces',provinces)]:
        with (BASE/(name+'.csv')).open('w',newline='') as f:
            keys=['id','name','value','change','growth','rank','active','active_rank','average'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rr)
    # Full original outlines become spherical coast/country boundaries. Dots are visual texture only.
    original=json.loads((ROOT/'content/vmap/source/world.json').read_text());surface=[];dots=[]
    for g in geo['world']:
        feature=original['features'][g['source_feature']];geom=feature['geometry'];polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
        for poly in polys:
            if not poly or not poly[0]:continue
            before=len(dots)
            outer=poly[0];surface.append({'id':g['id'],'points':outer})
            minx=min(p[0] for p in outer);maxx=max(p[0] for p in outer);miny=min(p[1] for p in outer);maxy=max(p[1] for p in outer)
            for iy in range(math.ceil(miny/1.8),math.floor(maxy/1.8)+1):
                lat=iy*1.8;step=1.8/max(.25,math.cos(math.radians(lat)))
                for ix in range(math.ceil(minx/step),math.floor(maxx/step)+1):
                    point=[ix*step,lat]
                    if in_ring(point,outer) and not any(in_ring(point,hole) for hole in poly[1:]):dots.append([round(point[0],3),round(lat,3),g['id']])
            if len(dots)==before:
                _,point=centroid(outer)
                if not in_ring(point,outer):point=outer[0]
                dots.append([round(point[0],3),round(point[1],3),g['id']])
    (BASE/'globe-surface.json').write_text(json.dumps({'outlines':surface,'dots':dots,'source':'../vmap/source/world.json','geojson_sha256':hashlib.sha256((ROOT/'content/vmap/source/world.json').read_bytes()).hexdigest(),'note':'Dots are a cartographic texture, not developers. Country anchor locations are geometric centroids, not cities or project locations.'},ensure_ascii=False,separators=(',',':')))
    # Native vector fallback for print, non-WebGL and the loading state.
    def project(lon,lat):
        a=math.radians(lon-100);b=math.radians(lat);tilt=math.radians(22);x=math.cos(b)*math.sin(a);y=math.sin(b)*math.cos(tilt)-math.cos(b)*math.cos(a)*math.sin(tilt);z=math.sin(b)*math.sin(tilt)+math.cos(b)*math.cos(a)*math.cos(tilt);return 430+220*x,270-220*y,z
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 540"><defs><radialGradient id="o"><stop stop-color="#224e68"/><stop offset="1" stop-color="#071d31"/></radialGradient></defs><rect width="860" height="540" fill="#091f34"/><circle cx="430" cy="270" r="227" fill="none" stroke="#58c7d5" stroke-opacity=".25" stroke-width="6"/><circle cx="430" cy="270" r="220" fill="url(#o)"/>']
    for lon,lat,code in dots:
        x,y,z=project(lon,lat)
        if z>0:svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.5" fill="#81ccd5" opacity="{.3+.7*z:.2f}"/>')
    svg.append('</svg>');(BASE/'globe-fallback.svg').write_text(''.join(svg))
    records=[]
    for p in sorted(SRC.iterdir()):
        if p.is_file():records.append({'file':'source/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (BASE/'provenance.json').write_text(json.dumps({'retrieved_date':'2026-10-15','sources':records,'source_root':'https://selfoss.open-digger.cn/openshare/overview/','github_repository':'X-lab2017/2026-Global-Open-Source-Development-Report','repository_contribution_blob':'08cd16a82a5cbb7acc4818db651775ab4d617076','geometry_reference':'../vmap/map-provenance.json','method_urls':['https://open-digger.cn/docs/user-docs/metrics/openrank','https://open-digger.cn/docs/user-docs/metrics/global-openrank','https://open-digger.cn/docs/user-docs/metrics/community-openrank'],'reference_project':'https://github.com/janarosmonaliev/github-globe','reference_source_blob':'fd2262c04f4b5deb96015fd1136ce7249de63364','runtime':'Three.js 0.170.0 + OrbitControls; locally served; no flight data reused','globe_network':'114 fictional nodes / 384 relations illustrate mutual reinforcement and historical continuity, not scores. Data mode separates 20 observed project-sample edges from optional residual-source scenario; see flows.json.'},ensure_ascii=False,indent=2)+'\n')
    print(f'C-Map: {len(countries)} countries/regions, {len(provinces)} provinces, {len(dots)} cartographic land dots; 20 observed project-sample edges; explicit residual-source scenario.')
if __name__=='__main__':build()
