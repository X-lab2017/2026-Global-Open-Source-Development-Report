"""Verify source records, report-year scope and the immutable observed network."""
from pathlib import Path
import argparse,json,hashlib,csv,math
from html.parser import HTMLParser
import cmap_content
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
root=Path(__file__).resolve().parents[1];base=out/'assets/cmap';data=json.loads((base/'data.json').read_text())
assert len(data['countries'])==238 and len(data['provinces'])==34
assert data['period']['start']=='2025-07-01' and data['period']['endExclusive']=='2026-07-01'
by={r['id']:r for r in data['countries']};cn={r['id']:r for r in data['provinces']}
assert by['CN']['value']==936846.83 and by['US']['value']==3321044.53
assert not {'TW','HK','MO'}.intersection(by) and {'710000','810000','820000'}.issubset(cn)
for scope,stem in [('countries','report-'),('provinces','report-CN-')]:
 source=json.loads((base/'source'/f'{stem}contribution.json').read_text());raw={r['code']:r for r in source['leaderboards'][0]['data']}
 dev=json.loads((base/'source'/f'{stem}developers.json').read_text());active={r['code']:r for r in dev['leaderboards'][1]['data']}
 for row in data[scope]:
  assert row['value']==raw[row['source_code']]['value'] and row['change']==raw[row['source_code']]['change']
  assert row['active']==active[row['source_code']]['value']
  assert math.isclose(row['average'],row['value']/row['active'])
assert math.isclose(sum(r['value'] for r in cn.values()),by['CN']['value'],abs_tol=.011)
assert data['global_value']==14125100.55 and data['trends']['CN']['labels']==['2022','2023','2024','2025','2026']
source=list(csv.DictReader((root.parent/'data/processed/chapter2/fig-2-2-2_five_region_openrank_contribution_trend.csv').open()))
for key,values in data['legacy']['series'].items():assert values==[float(r[key]) for r in source]
assert round((data['legacy']['series']['China'][-1]/data['legacy']['series']['United States'][-1]-1)*100,1)==4.5
assert data['globe_edges_status']=='observed_sample_with_uniform_visual_enhancement'
for item in json.loads((base/'provenance.json').read_text())['sources']:assert hashlib.sha256((base/item['file']).read_bytes()).hexdigest()==item['sha256']
surface=json.loads((base/'globe-surface.json').read_text());assert surface['geojson_sha256']==hashlib.sha256((root/'content/vmap/source/world.json').read_bytes()).hexdigest()
assert any(p[2]=='CN' and 120<p[0]<122.5 and 22<p[1]<26 for p in surface['dots'])
class Inspect(HTMLParser):
 def __init__(self,text):super().__init__();self.ids=[];self.figures=[];self.paths={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='figure' and 'cmap-figure' in a.get('class',''):self.figures.append(a)
  if 'data-cm-region' in a:self.paths[a['data-cm-region']]=a['d']
for lang in ['zh','en']:
 text=(out/f'2026/{lang}/chapters/02/index.html').read_text();page=Inspect(text);section=text[text.index('id="ch02-s02"'):text.index('id="ch02-s03"')]
 assert len(page.ids)==len(set(page.ids))
 assert [f['id'] for f in page.figures]==['fig-cmap-global','fig-cmap-comparison','fig-cmap-china','fig-cmap-globe']
 assert all(f['data-slide-height']=='860' and f['data-reflow-minimum-width']=='700' for f in page.figures)
 for scope in ['world','china']:
  for g in cmap_content.GEO[scope]:
   if g['id'] in page.paths:assert g['d']==page.paths[g['id']]
 for n in range(1,5):assert f'图 2-2-{n} / C-MAP' in section
 for term in ['机制示意','虚构节点','残差估算','2025 自然年','算法对象范围待核','欧洲成员口径待补']:assert term not in section,term
 assert '增强 ×3' in section and '20 条实际记录' in section and '统计范围与指标说明' in section
assert (base/'vendor/three.module.js').stat().st_size>500000
assert "from './three.module.js'" in (base/'vendor/OrbitControls.js').read_text()
assert (base/'chapter-2-2.md').read_text()==cmap_content.manuscript()
flows=data['flows'];assert len(flows['edges'])==20 and all(r['kind']=='observed' for r in flows['edges'])
raw=list(csv.DictReader((root/'content/report-assets/data/table-2-5-1_china_us_project_contribution_top10.csv').open()))
for r,e in zip(raw,flows['edges']):assert float(r['openrank'])==e['value'] and float(r['share_pct'])==e['share_pct']
assert len({e['source'] for e in flows['edges']})==14
for code in {e[k] for e in flows['edges'] for k in ['source','target']}:assert by[code]['coordinates']
for target,expected,coverage in [('CN',29666.1,93.24),('US',244808.4,77.94)]:
 rr=[r for r in flows['edges'] if r['target']==target];t=flows['targets'][target]
 assert math.isclose(sum(r['value'] for r in rr),expected)
 assert math.isclose(sum(r['share_pct'] for r in rr),coverage)
 assert round(t['observed_share_pct']+t['unlisted_share_pct'],2)==100
 assert len([r for r in rr if r['source']==target])==1
assert flows['enhancement']['adds_observations'] is False
assert 'DEMO_NODES' not in (out/'cmap-globe.js').read_text() and 'estimated' not in (out/'cmap-globe.js').read_text()
print('PASS: C-Map report-year sources, 238 regions/34 provinces, four figures, confirmed five-group comparison and 20 immutable source relationships with display-only enhancement.')
