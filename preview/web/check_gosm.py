#!/usr/bin/env python3
"""Verify Chapter 5 source boundaries, aggregates, relationship endpoints and exports."""
import argparse,collections,csv,gzip,hashlib,json
from pathlib import Path
import gosm_content as G
import build_gosm_supply_data as S

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
d=G.payload();out=a.output/'assets/gosm'
page=(a.output/'2026/zh/chapters/05/index.html').read_text()
assert page.count('data-gm-chart=')==1+sum(len(t['figures']) for t in G.TOPICS)
assert 'gosm.js?v='+G.VERSION in page and 'gosm.css?v='+G.VERSION in page
assert all(f'id="{t["id"]}"' in page for t in G.TOPICS)
assert len(G.TOPICS)==3 and sum(len(t['actions']) for t in G.TOPICS)==9
assert '各图按来源标注统计期与快照' in page
assert all(len(t['figures'])==len(t['narratives']) for t in G.TOPICS)
for k,name in G.FILES.items():
    assert (out/'data'/name).read_bytes()==(G.REPO/'data/processed/chapter5'/name).read_bytes(),name
assert json.loads((out/'data.json').read_text())==d
for key,rows in S.build().items():
    name=S.NAMES[key]+'.csv'
    assert (out/'data'/name).read_text()==S.text_csv(rows)[0],name
assert d['supply51']['meta']['containsSimulatedData'] is False
assert '.s51-panel {' in (a.output/'gosm-supply.css').read_text(), 'Supply layout selector must match the 5.1 article class'
assert '.s52-panel {' in (a.output/'gosm-influence.css').read_text(), 'Influence layout selector must match the 5.2 article class'
assert all('s52-panel gm-compact-panel' in page.split('data-gm-chart="'+k+'"')[0][-80:] for k in ['network','flows','head'])
assert json.loads((out/'supply-scenarios.json').read_text())['dataStatus']=='simulated'
assert G.TOPICS[0]['figures']==['world','cnus','china']
assert G.TOPICS[1]['figures']==['network','flows','head']
assert '基座来源→派生发布' in page
assert sum(r['weight'] for r in d['flows'] if r['source']=='CN')==5888
assert sum(r['weight'] for r in d['flows'] if r['target']=='US')==7513
assert next(r['weight'] for r in d['flows'] if r['source']=='CN' and r['target']=='US')==4639
assert '四个角度' not in page and 'gm-explore' not in page
assert all('data-gm-chart="'+key+'"' not in page for key in ['publishers','supply','release','portfolio','scenarios'])
assert sum(r['models'] for r in d['quadrants'])==870
assert sum(r['n'] for r in d['openRegions'])==870
assert sum(r['models'] for r in d['openPublishers'])==870
assert all(r['double_high']<=r['high_open']<=r['models'] for r in d['openPublishers'])
assert len(d['head'])==78 and len({r['month'] for r in d['head']})==26
for r in d['head']:assert r['china']+r['us']+r['other_known']+r['unknown']==r['k']
for r in d['derivation']:assert abs(r['derived_models']/r['models']*100-r['derived_pct'])<1e-9
known=[r for r in d['countries'] if r['region_code']]
assert sum(r['models'] for r in known)==71578
assert sum(r['models'] for r in d['countries'])==3062151
for key in ['models','downloads_all_time','likes']:
    assert abs(sum(r[key+'_known_share_pct'] for r in known)-100)<1e-6
    assert abs(sum(r[key+'_global_share_pct'] for r in d['countries'])-100)<1e-6
pairs=collections.Counter()
for r in d['flows']:pairs[tuple(sorted((r['source'],r['target'])))]+=r['weight']
assert sum(pairs.values())==10943 and len(pairs)==139 and pairs[('CN','US')]==4782
net=d['network'];nodes={n['id']:n for n in net['nodes']};edges=net['edges']
assert len(nodes)==len(net['nodes'])==5777 and len(edges)==5111
assert len({(e['source'],e['target']) for e in edges})==5111
up=collections.Counter();down=collections.Counter()
for e in edges:
    assert e['source'] in nodes and e['target'] in nodes
    assert e['type']=='declared-base-model' and e['source']!=e['target']
    up[e['target']]+=1;down[e['source']]+=1
for n in nodes.values():assert n['upstreamCount']==up[n['id']] and n['downstreamCount']==down[n['id']]
overview={r['id'] for r in net['overview']}
assert len(overview)==677 and sum(e['source'] in overview and e['target'] in overview for e in edges)==681
assert len(net['bases'])==12 and len({nodes[r['id']]['publisher'] for r in net['bases']})==12
for r in net['overview']:assert 0<=r['overviewX']<=1600 and 0<=r['overviewY']<=1120
assert net['meta']['snapshotAtDeclared'].startswith('2026-10-16')
current=d['opennessCurrent'];assert len(current['models'])==len({m['model_id'] for m in current['models']})==884
q=collections.Counter(m['strict_quadrant'] for m in current['models'])
assert q=={'低完整-高开放':497,'低完整-低开放':212,'高完整-高开放':117,'高完整-低开放':58}
assert sum(m['license_evidence_differs_from_grade'] for m in current['models'])==22
assert len(d['cases']['models'])==4
for m in d['cases']['models']:
    assert len(m['revision'])==40 and m['checked_at']=='2026-10-17'
    assert len(m['fields'])==6
    for f in m['fields'].values():
        assert f['status'] in {'observed','unknown','not-applicable'}
        assert f['sources'] and all(u.startswith('https://') for u in f['sources'])
for f in G.DIR.glob('*.gz'):
    assert gzip.decompress(f.read_bytes())==(out/f.stem).read_bytes(),f.name
assert (out/'methods.md').exists() and (out/'openness-evidence-884.json').exists()
for name in ['gosm.js','gosm.css','gosm-network.mjs','gosm-supply.js','gosm-supply.css','gosm-influence.js','gosm-influence.css']:
    assert (a.output/name).read_bytes()==(G.ROOT/'web'/name).read_bytes()
appendix=(a.output/'2026/zh/appendices/dpg/index.html').read_text()
assert '本报告不授予认证' in appendix and '8.5 分' not in appendix
print('PASS GOSM: 10 figures and 9 actions; 9 source-identical CSVs; explicit denominators; 5,777 models / 5,111 declared relationships; 677-node overview; separate 870 / 884 openness cohorts; four pinned official cases; lossless exports.')
