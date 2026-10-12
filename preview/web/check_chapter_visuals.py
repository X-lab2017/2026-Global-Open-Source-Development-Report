#!/usr/bin/env python3
"""Check the figure integration against source snapshots and canonical definitions."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,json,csv
class FigurePage(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.scripts={};self.active=None;self.feed(text)
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.tags.append((tag,d))
        if tag=='script' and d.get('type')=='application/json':self.active=d['id'];self.scripts[self.active]=''
    def handle_data(self,data):
        if self.active:self.scripts[self.active]+=data
    def handle_endtag(self,tag):
        if tag=='script':self.active=None
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--repo-root',type=Path);args=p.parse_args()
root=Path(__file__).resolve().parents[1];story=json.loads((root/'content/story-data.json').read_text());report=json.loads((root/'content/report.json').read_text())
if args.repo_root:
    for key,source in story['files'].items():
        raw=args.repo_root/source['path'];assert hashlib.sha256(raw.read_bytes()).hexdigest()==source['sha256']
        original=json.loads(raw.read_text())
        if key=='models':assert original==story['models']
        else:
            assert story[key]['total']==original['meta']['total']
            assert story[key]['rows']==[{k:row[k] for k in ['name','contributions','percentage']} for row in original['data'][:10]]
assert story['models'][-1]=={'date':'Feb 26','china':70,'unitedStates':26,'europe':4}
assert len(story['models'])==28 and story['contributors']['total']==45855 and story['organizations']['total']==5686
with (args.output/'assets/report/model-derivatives-story.csv').open(newline='') as f:
    exported=list(csv.DictReader(f))
assert [{k:(v if k=='date' else int(v)) for k,v in row.items()} for row in exported]==story['models']
for lang in ['zh','en']:
    page=FigurePage((args.output/f'2026/{lang}/chapters/01/index.html').read_text())
    ids=[a['id'] for _,a in page.tags if 'id' in a]
    assert all(x in ids for x in ['fig-linux','fig-models','fig-public-goods','fig-osdg-goals','fig-osdi-map'])
    for attr,count in [('data-linux-kind',2),('data-month',28),('data-sdg',17),('data-dpg',9),('data-goal',14),('data-indicator',29),('data-indicator-role',4)]:
        nodes=[a for _,a in page.tags if attr in a];assert len(nodes)==count,(attr,len(nodes))
        assert all('aria-pressed' in a for a in nodes)
    decoded={key:json.loads(value) for key,value in page.scripts.items()}
    assert decoded['model-viz-data']==story['models']
    assert decoded['linux-viz-data']['organizations']==story['organizations']
    assert decoded['linux-viz-data']['contributors']==story['contributors']
    assert decoded['indicators-viz-data']=={row['indicator_code']:row for row in report['indicators']}
    assert len(decoded['goals-viz-data'])==14
    assert {x for v in decoded['goals-viz-data'].values() for x in v['indicators']}=={r['indicator_code'] for r in report['indicators']}
    assert any(a.get('src','').endswith('/chapter-visuals.js') for _,a in page.tags)
    assert any(a.get('href','').endswith('/chapter-visuals.css') for _,a in page.tags)
print('PASS: five bilingual interactive figures; 28 exact monthly observations, 14 framework hotspots, 17 SDGs, 9 DPG criteria, 29 canonical indicators; raw data unchanged.')
