"""Verify C-Map source fidelity, map identity and the observed/conceptual boundary."""
from pathlib import Path
import argparse,json,hashlib,csv,math
from html.parser import HTMLParser
import cmap_content

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
root=Path(__file__).resolve().parents[1];data=json.loads((out/'assets/cmap/data.json').read_text())
assert len(data['countries'])==236 and len(data['provinces'])==34
by={r['id']:r for r in data['countries']};cn={r['id']:r for r in data['provinces']}
assert by['CN']['value']==1210375.59 and by['US']['value']==4236888.42
assert not {'TW','HK','MO'}.intersection(by)
assert {'710000','810000','820000'}.issubset(cn)
for scope,file in [('countries','calendar-contribution.json'),('provinces','calendar-CN-contribution.json')]:
    source=json.loads((root/'content/cmap/source'/file).read_text())
    raw={r['code']:r for r in source['leaderboards'][0]['data']}
    for row in data[scope]:
        assert row['value']==raw[row['source_code']]['value']
        assert row['change']==raw[row['source_code']]['change']
        if row['active']:assert math.isclose(row['average'],row['value']/row['active'])
assert math.isclose(sum(r['value'] for r in cn.values()),by['CN']['value'],abs_tol=.011)
assert round(data['global_value']-data['global_region_sum'],2)==420087.61
assert math.isclose(sum(by[c]['value'] for c in data['south6']['members']),data['south6']['value'])
assert round(data['project_reference']['ratio_us_cn'],1)==3.4
assert data['legacy']['years']==[2022,2023,2024,2025,2026]
assert data['trends']['CN']['labels']==['2021','2022','2023','2024','2025']
assert data['globe_edges_status']=='conceptual_network_and_observed_sample_with_optional_residual_scenario'
sources=json.loads((out/'assets/cmap/provenance.json').read_text())['sources']
for item in sources:assert hashlib.sha256((out/'assets/cmap'/item['file']).read_bytes()).hexdigest()==item['sha256']
surface=json.loads((out/'assets/cmap/globe-surface.json').read_text())
assert surface['geojson_sha256']==hashlib.sha256((root/'content/vmap/source/world.json').read_bytes()).hexdigest()
assert any(p[2]=='CN' and 120<p[0]<122.5 and 22<p[1]<26 for p in surface['dots'])
class Inspect(HTMLParser):
    def __init__(self,text):super().__init__();self.ids=[];self.figures=[];self.paths={};self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='figure' and 'cmap-figure' in a.get('class',''):self.figures.append(a)
        if 'data-cm-region' in a:self.paths[a['data-cm-region']]=a['d']
for lang in ['zh','en']:
    text=(out/f'2026/{lang}/chapters/02/index.html').read_text();page=Inspect(text)
    assert len(page.ids)==len(set(page.ids))
    assert [f['id'] for f in page.figures]==['fig-cmap-global','fig-cmap-comparison','fig-cmap-china','fig-cmap-globe']
    assert all(f['data-slide-height']=='860' for f in page.figures)
    for scope in ['world','china']:
        for g in cmap_content.GEO[scope]:
            if g['id'] in page.paths:assert g['d']==page.paths[g['id']]
    for n in range(1,5):assert f'图 2-2-{n} / C-MAP' in text
    for term in ['机制示意','非真实跨国流量','报告五年趋势','平均贡献 · 探索','可信的地区贡献观察','2025 自然年','官方 SDG 指标']:
        assert term in text,term
assert (out/'assets/cmap/vendor/three.module.js').stat().st_size>500000
assert "from './three.module.js'" in (out/'assets/cmap/vendor/OrbitControls.js').read_text()
assert (out/'assets/cmap/chapter-2-2.md').read_text()==cmap_content.manuscript()
print('PASS: C-Map 236 regions / 34 provinces, unchanged source geometry, separate annual scopes, four numbered single-screen figures, observed data vs conceptual network and local licensed 3D dependencies.')

flows=data['flows'];observed=[r for r in flows['edges'] if r['kind']=='observed'];assert len(observed)==20
source=list(csv.DictReader((root/'content/report-assets/data/table-2-5-1_china_us_project_contribution_top10.csv').open()))
assert [r['value'] for r in observed]==[float(r['openrank']) for r in source]
for target,expected in [('CN',29666.1),('US',244808.4)]:
    rows=[r for r in flows['edges'] if r['target']==target];t=flows['targets'][target]
    assert math.isclose(sum(r['value'] for r in rows if r['kind']=='observed'),expected)
    assert math.isclose(sum(r['value'] for r in rows if r['kind']=='estimated'),t['estimated_residual'])
    assert math.isclose(sum(r['share_pct'] for r in rows),100)
    assert len([r for r in rows if r['kind']=='estimated' and r['display']])==t['displayed_estimates']
    assert {'BR','ID','VN','PH','EG','ZA'}.issubset({r['source'] for r in rows if r['kind']=='estimated' and r['display']})
    assert all(r['value']>=0 and math.isfinite(r['value']) for r in rows)
assert flows['report_values']['CN']==4429200.83 and flows['report_values']['US']==4239710.05
assert (out/'assets/cmap/flow-method.md').is_file()
print('PASS: report China/US values, 20 unaltered sample flows, residual conservation, strongest flows plus six-country scenario coverage and published method.')
