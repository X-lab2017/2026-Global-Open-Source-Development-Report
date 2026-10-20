"""Check GOSO evidence, source preservation and review delivery boundaries."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,csv,hashlib,json,math,xml.etree.ElementTree as ET
import goso_content as goso

parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
out=args.output
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.charts=[];self.fields=[];self.count_sections=0;self.ids=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if 'data-goso-chart' in a:self.charts.append(a['data-goso-chart'])
        if 'data-review-key' in a:self.fields.append(a['data-review-key'])
        if tag=='section' and a.get('id','') in [f'ch02-s0{i}' for i in range(1,8)]:self.count_sections+=1

views=goso.views();vlist=[v for vv in views.values() for v in vv]
assert len(vlist)==17 and len({v['id'] for v in vlist})==17
evidence=json.loads((out/'assets/goso/evidence-manifest.json').read_text())
assert len(evidence['files'])==15 and evidence['source_ref']==goso.REF
for k,entry in evidence['files'].items():
    p=out/'assets/report/data'/Path(entry['path']).name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['path']
for v in vlist:
    assert all(len(s['values'])==len(v['x']) for s in v['series'])
    assert all(x is None or math.isfinite(x) for s in v['series'] for x in s['values'])
    ET.fromstring((out/'assets/goso'/f'{v["id"]}.svg').read_text())
platform=next(v for v in vlist if v['id']=='platforms')
atom=next(s for s in platform['series'] if s['key']=='GitCode')
assert atom['label']=='AtomGit' and atom['values'][:2]==[None,None]
assert 'GitCode' in (out/'assets/report/data'/Path(goso.FILES['platforms']).name).read_text().splitlines()[0]
coverage=next(v for v in vlist if v['id']=='coverage')
known,unknown=coverage['series'][0]['values']
assert known==71578 and unknown==2990573 and known+unknown==3062151
assert round(unknown/(known+unknown)*100,2)==97.66
active=goso.rows('active');assert round((float(active[-1]['China'])/float(active[-2]['China'])-1)*100,1)==42.0
models=goso.rows('models');assert round((float(models[-1]['models'])/float(models[-2]['models'])-1)*100,1)==58.3
assert round((float(models[-1]['publishers'])/float(models[-2]['publishers'])-1)*100,1)==48.4
influence=goso.rows('influence');assert round((float(influence[-1]['China'])/float(influence[0]['China'])-1)*100)==160
for lang in ['zh','en']:
    text=(out/f'2026/{lang}/chapters/02/index.html').read_text();page=Page(text)
    assert page.count_sections==7 and page.charts==[]
    assert len(page.fields)==4 and len(page.ids)==len(set(page.ids))
    # I-Map no longer renders an empty project-count placeholder.
    for term in ['AtomGit','前 5%','当前浏览器','23 个图组','统计范围与指标说明']:assert term in text,term
    # Source snapshots are shared by inline and on-demand source panels.
    for key,entry in evidence['files'].items():
        assert (out/'assets/report/data'/Path(entry['path']).name).is_file(),key
    for n,count in enumerate([3,4,3,4,3,3,3],1):
        for i in range(1,count+1):assert f'fig-2-{n}-{i}' in page.ids
    assert text.count('class="goso-section-nav"')==7
    for key in ('fig-2-3-1','fig-2-3-2','fig-2-3-3','fig-2-4-1','fig-2-4-2','fig-2-4-3','fig-2-4-4','fig-2-4-5'):assert key in page.ids,key
assert (out/'assets/goso/GOSO-review-draft.md').exists()
print('PASS: GOSO seven sections, 23 numbered interactive figures and 17 preserved static observation views, 15 original datasets, coverage/growth claims, AtomGit alias with missing values, four review fields and static exports.')
# Chapter opening follows the reviewed seven-section manuscript.
import goso_intro
assert (goso.ROOT.parent/'chapters/chapter2/本章介绍.md').read_text()==goso_intro.manuscript()
for lang in ['zh','en']:
    text=(out/f'2026/{lang}/chapters/02/index.html').read_text()
    opening=text[text.index('id="goso-intro"'):text.index('id="ch02-s01"')]
    for paragraph in [goso_intro.INTRO,goso_intro.QUESTION,goso_intro.READING,*goso_intro.SCOPE,*[f[1] for f in goso_intro.FINDINGS]]:assert paragraph in opening
    assert '2025 自然年' not in opening and '2026-10-16' not in opening
    for i in range(1,8):assert f'href="#ch02-s0{i}"' in opening
print('PASS: chapter opening shares canonical prose and seven reading destinations')
