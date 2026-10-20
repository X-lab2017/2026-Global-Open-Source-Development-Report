"""Guard the I/T integration, figure color regression and evidence boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, csv, json, re

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
out=p.parse_args().output;root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))

for lang in ('zh','en'):
    text=(out/f'2026/{lang}/chapters/02/index.html').read_text();page=Page(text)
    canvases=[a for _,a in page.nodes if 'goso-unified-canvas' in a.get('class','')]
    assert len(canvases)==16
    assert {a['data-slide-key'] for a in canvases}=={f'{k}-{i}' for k,n in [('tmap',5),('amap',3),('dmap',3),('gmap',5)] for i in range(1,n+1)}
    assert all(a['data-slide-height']=='820' for a in canvases)
    imap=[a for _,a in page.nodes if 'imap-figure' in a.get('class','')]
    assert len(imap)==3 and all(a['data-slide-height']=='860' for a in imap)
    assert {a['data-slide-key'] for a in imap}=={'imap-1','imap-2','imap-3'}
    assert not any('data-tm-full' in a or 'data-fullscreen' in a for _,a in page.nodes)
    for term in ['OpenRankInflu','OpenRankContrib','HighImpactTalent','GlobalCollabShare','模拟演示','非预测','14.02%','39.66%','442.92','423.97']:
        assert term in text,term
    assert f'/2026/{lang}/data/indicators/#indicator-HighImpactTalent' in text

# @charset was accidentally parsed into the :root rule, invalidating every light
# token in the previous review. It must never pass the release gate again.
css=(out/'imap.css').read_text()
assert '@charset' not in css
assert not re.search(r'(?m)^\s*:root\s*\{',css)
skin=(out/'goso-map-system.css').read_text()
for token in ['--map0','--map5','--s0','--s4','--tm-ink','--tm-surface']:
    assert re.search(re.escape(token)+r'\s*:',skin),token
assert '[data-theme=dark] .imap-review' in skin
shared=(out/'chapter1-explorers.js').read_text()
assert 'goso-unified-canvas' in shared and 'chartOwner' in shared
for name in ('tmap',):
    js=(out/f'{name}.js').read_text()
    assert '.explorer-presentation.'+name+'-review[open]' in js
    assert 'meta[name=gosd-base]' in js

# Repository downloads remain byte-identical; simulated data never replaces them.
repo=root.parent
for key in ('imap','tmap'):
    for f in (out/'assets'/key).glob('*.csv'):
        candidates=list((repo/'data/processed').rglob(f.name))
        if candidates:assert f.read_bytes()==candidates[0].read_bytes(),f.name
sim=json.loads((out/'assets/tmap/simulation.json').read_text())
assert sim['evidence_status']=='simulated_design_only'
assert all(sum(row)==100 for row in sim['flows'])
assert all(sum(row)==100 for row in sim['ai']['matrix'])
assert sum(map(sum,sim['transition']['matrix']))==1000
i=json.loads((root/'content/imap/observations.json').read_text())
t=json.loads((root/'content/tmap/observations.json').read_text())
assert len(i['chinaProjects'])==30 and i['chinaProjectCounts']==[None]*5
assert len(t['world'])==175 and len(t['chinaRecords'])==370
assert 'geometry' not in i and 'geometry' not in t
for k in ('imap','tmap'):assert (out/'assets'/k/'data.js').exists()
print('PASS: 3 I-Map publication figures and 16 T/A/D/G presentations; scoped light/dark tokens; unchanged source CSVs; isolated simulations; shared source geometry.')
