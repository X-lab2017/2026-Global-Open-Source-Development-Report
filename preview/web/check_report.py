#!/usr/bin/env python3
"""Validate manuscript integration and ensure downloadable evidence is unchanged."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,csv,hashlib,json

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.figures=[];self.text=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='img':self.figures.append(a)
    def handle_data(self,text):self.text.append(text)

parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
root=Path(__file__).resolve().parents[1];out=args.output
r=json.loads((root/'content/report.json').read_text());m=json.loads((root/'content/manifest.json').read_text())
assert len(r['indicators'])==29 and len({x['indicator_code'] for x in r['indicators']})==29
assert len({x['pillar_id'] for x in r['indicators']})==4 and len({x['dimension_id'] for x in r['indicators']})==10
for entry in r['datasets']:
    p=out/'assets/report/data'/Path(entry['path']).name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['path']
    with p.open(newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==int(entry['row_count']),entry['path']
    assert not entry['path'].startswith('data/raw/')
for lang in ['zh','en']:
    chapter=Page((out/f'2026/{lang}/chapters/01/index.html').read_text())
    assert len(chapter.figures)==7 and all(x.get('alt') and x.get('class')=='chapter-print-figure' for x in chapter.figures)
    for section in m['chapters'][0]['sections']:assert section['id'] in chapter.ids
    body=' '.join(chapter.text)
    for term in ['45,855','5,686','70%','OpenDigger','ModelRank']:assert term in body,term
    assert not any(x in body for x in ['\x00','$$','**'])
    if lang=='en':assert 'translation is in preparation' in body
    # The complete chapter map belongs to Chapter 1; entry pages provide contextual navigation.
    for route in ['', 'summary/', 'introduction/']:
        entry=(out/f'2026/{lang}'/route/'index.html').read_text()
        assert 'id="fig-report-logic"' not in entry
    entry=(out/('index.html' if lang=='zh' else 'en/index.html')).read_text()
    assert 'id="fig-report-logic"' not in entry and 'home-reading-start' in entry
    methods=Page((out/f'2026/{lang}/methodology/index.html').read_text())
    assert '2.2235' in ' '.join(methods.text) and '34' in ' '.join(methods.text)
    data=Page((out/f'2026/{lang}/data/sources/index.html').read_text())
    for entry in r['datasets']:assert 'dataset-'+entry['dataset_id'] in data.ids
    indicators=Page((out/f'2026/{lang}/data/indicators/index.html').read_text())
    for row in r['indicators']:assert 'indicator-'+row['indicator_code'] in indicators.ids
print(f'PASS: complete Chapter 1 and methods, interactive report structure and downloadable static figures, 29 definitions, {len(r["datasets"])} byte-identical CSV downloads, bilingual status labels.')
