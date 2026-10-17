"""Guard complete source coverage and legible, non-overlapping first landscapes."""
import argparse, collections, csv, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
import gosl_landscapes as G
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
repo=Path(__file__).resolve().parents[2]
page=(args.output/'2026/zh/chapters/04/index.html').read_text()
assert page.count('data-gl-plate=')==5
assert page.count('class="gl-writing-space"')==20
assert page.count('id="gosl-overview"')==1 and page.count('id="gosl-contribute"')==1
assert 'gosl-landscapes.js?v='+G.VERSION in page
assert sum(d['count'] for d in G.DATASETS)==436
expected={'models':96,'cloud':86,'database':93,'riscv':78,'pytorch':83}
for d in G.DATASETS:
    source=repo/d['source']['path']
    assert hashlib.sha256(source.read_bytes()).hexdigest()==d['source']['sha256'], d['id']
    rows=list(csv.DictReader(source.open(encoding='utf-8-sig')))
    key='model_id' if d['id']=='models' else 'repo_name'
    value='downloads' if d['id']=='models' else 'total_openrank'
    assert len(rows)==d['count']==expected[d['id']]
    originals={r[key]:float(r[value]) for r in rows}
    assert {p['repo']:p['value'] for p in d['projects']}==originals
    assert len({p['id'] for p in d['projects']})==d['count']
    cats=G.names(d);counts=collections.Counter(p['category'] for p in d['projects'])
    assert all(c['count']==counts[c['id']] for c in d['categories'])
    assert sum(c['count'] for c in d['categories'])==d['count']
    assert sorted(k for g in d['groups'] for k in g['categories'])==sorted(cats)
    for p in d['projects']:
        assert p['category'] in p['tags'] and set(p['tags'])<=set(cats)
        assert p['url'].startswith('https://') and p['classificationSource'].startswith('https://')
        assert p['classification'] and p['note']
    if d['id']=='riscv':assert counts['pending']==3
    if d['id']=='pytorch':assert counts['pending']==1
    boxes,groups=G.geometry(d)
    for i,b in enumerate(boxes):
        assert b['y']>=G.TOP and b['y']+b['h']<=G.BOTTOM+.01
        assert b['x']>=24 and b['x']+b['w']<=1576.01
        for a in boxes[i+1:]:
            overlap=min(b['x']+b['w'],a['x']+a['w'])-max(b['x'],a['x'])>1 and min(b['y']+b['h'],a['y']+a['h'])-max(b['y'],a['y'])>1
            assert not overlap,(d['id'],a['id'],b['id'])
        for cell in b['cells']:
            assert cell['x']>=b['x'] and cell['x']+cell['w']<=b['x']+b['w']
            assert cell['y']>=b['y']+32 and cell['y']+cell['h']<=b['y']+b['h']+.01
    svg=ET.fromstring(G.plate_svg(d));nodes=svg.findall('.//{*}g[@data-gl-project]')
    assert len(nodes)==d['count']
    projects={p['id']:p for p in d['projects']}
    for n in nodes:
        label=''.join(n.find('{*}text').itertext()) if n.find('{*}text') is not None else ''
        # Project names are in tspans; marks are separate direct text elements.
        actual=''.join(t.text or '' for t in n.findall('.//{*}tspan'))
        assert actual==projects[n.attrib['data-gl-project']]['name']
    exported=list(csv.DictReader((args.output/'assets/gosl'/f'{d["id"]}-projects.csv').open(encoding='utf-8-sig')))
    assert len(exported)==d['count'] and {r['repo_or_model'] for r in exported}==set(originals)
assert (repo/'chapters/chapter4/4.2-AI-大模型全景洞察.md').exists()
assert json.loads((args.output/'assets/gosl/landscapes.json').read_text())==G.DATA
print('PASS GOSL: all 436 source rows and values preserved; 74 categories plus 4 pending samples; non-overlapping geometry; full project names; five first landscapes and 20 intentionally empty analysis slots; complete CSV/JSON exports.')
