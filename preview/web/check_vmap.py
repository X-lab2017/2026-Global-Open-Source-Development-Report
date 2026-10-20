"""Source fidelity, map shape preservation, time windows and narrative consistency."""
from pathlib import Path
import argparse,hashlib,json,csv,math,re
from html.parser import HTMLParser
import vmap_content as v
from build_vmap_geometry import points
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();assets=args.output/'assets/vmap'
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.figures=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='figure' and 'vmap-figure' in a.get('class',''):self.figures.append(a)
data=json.loads((assets/'fig-2-1-2_platform-coverage.json').read_text());by={r['id']:r for r in data['countries']}
assert data['domestic']['cross_github_deduplicated'] is True and data['domestic']['active_approx']==120
assert math.isclose(by['CN']['active'],250.482488) and math.isclose(by['CN']['total'],1838.6391)
assert len(data['countries'])==242 and len(data['provinces'])==34
assert math.isclose(sum(r['active'] for r in data['provinces']),by['CN']['active'],abs_tol=34*.005/10000)
assert {'710000','810000','820000'}<={r['id'] for r in data['provinces']}
source_cn=json.loads((assets/'source/report-CN-developers.json').read_text())
assert math.isclose(next(r['increase'] for r in data['provinces'] if r['id']=='350000'),next(r['change'] for r in source_cn['leaderboards'][1]['data'] if r['code']=='CN-FJ')/10000)
assert math.isclose(data['groups']['SOUTH6']['active'],sum(by[k]['active'] for k in ['BR','ID','VN','PH','EG','ZA']))
assert data['observation_period']['start']=='2025-07-01' and data['observation_period']['end_exclusive']=='2026-07-01'
assert data['source_checks']['attachment_readings_verified']==40
assert data['trend']['years']==[2022,2023,2024,2025,2026] and data['trend']['estimated'] is False
assert all(t['labels']==['2022','2023','2024','2025','2026'] for t in data['snapshot_trends'])
assert (assets/'fig-2-1-2_five-year-source.csv').read_bytes()==(v.ROOT/'content/report-assets/data/fig-2-1-3_five_region_active_developers_trend.csv').read_bytes()
for name,meta in data['images'].items():assert hashlib.sha256((assets/name).read_bytes()).hexdigest()==meta['sha256']
for name,meta in data['source_registry'].items():assert hashlib.sha256((assets/'source'/name).read_bytes()).hexdigest()==meta['sha256']
rows=list(csv.DictReader((assets/'fig-2-1-2_platform-coverage.csv').open()));assert len(rows)==242
assert next(r for r in rows if r['country_code']=='CN')['cross_github_overlap_status']=='deduplicated'
five=list(csv.DictReader((v.ROOT.parent/'data/processed/chapter2/fig-2-1-2_five_region_total_developers.csv').open()))
assert [r['total'] for r in data['five_group_records']]==[int(r['developers'])/10000 for r in five]
assert next(r for r in data['five_group_records'] if r['id']=='EU')['active']==675.3891
geo=json.loads((assets/'map-geometry.json').read_text());spec=json.loads((assets/'map-provenance.json').read_text())
assert spec['aspect_scale']==.75 and spec['shape_simplification'] is False
assert not any(r['id'] in ['TW','HK','MO'] for r in geo['world'])
# Every original vertex must survive the same affine transform; no per-axis fitting.
count=0
for scope in ['world','china']:
 conf=spec['scopes'][scope];source=json.loads((assets/'source'/conf['geojson']).read_text())['features'];bounds=conf['geographic_bounds'];scale=conf['uniform_scale'];ox,oy=conf['offset']
 assert len(geo[scope])==len(source)
 assert abs(conf['shape_ratio']-(1.9376827002527939 if scope=='world' else 1.2982827242169506))<1e-10
 for r in geo[scope]:
  pts=list(points(source[r['source_feature']]['geometry']['coordinates']));nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',r['d'])))
  assert len(nums)==len(pts)*2
  for i,(x,y) in enumerate(pts):
   xx=ox+(x-bounds[0])*.75*scale;yy=oy+(bounds[3]-y)*scale
   assert abs(nums[i*2]-xx)<=.000501 and abs(nums[i*2+1]-yy)<=.000501
   assert 0<=nums[i*2]<=880 and 0<=nums[i*2+1]<=412.001
   count+=1
for lang in ['zh','en']:
 text=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();page=Page();page.feed(text)
 assert len(page.ids)==len(set(page.ids))
 assert [f['id'] for f in page.figures]==['fig-vmap-global','fig-vmap-comparison','fig-vmap-china']
 part=text[text.index('id="ch02-s01"'):text.index('id="ch02-s02"')]
 assert part.count('<img')==4 and part.count('data-map-svg=')==3
 assert part.count('class="vmap-publication-views"')==3
 assert part.count('preserveAspectRatio="xMidYMid meet"')==3
 for number in ['图 2-1-1 /','图 2-1-2 /','图 2-1-3 /']:assert part.count(number)==1
 for title,_ in v.STRATEGIES:assert title in part
 compact=re.sub(r'\s+','',part)
 assert '2026报告年度' in compact and '国内补充' in compact and '台湾省' in compact and '34个省级地区' in compact
 assert '中国下钻保留旧版结构参考' not in text
 assert 'DevScale' in part and 'SDG 8' in part and 'SDG 9' in part
 assert 'data-vmap-view="trend"' in part and re.search(r'<script src="[^"]*/vmap\.js" defer>',text)
manuscript=(args.output/'assets/goso/GOSO-review-draft.md').read_text();assert v.manuscript() in manuscript
print(f'PASS: {count:,} source vertices retain OpenShare shape; 242 region / 34 province records; verified 2026 report window, confirmed five-group series, numbered figures and matching manuscript.')
