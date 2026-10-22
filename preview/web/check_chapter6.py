#!/usr/bin/env python3
"""Validate the chapter contract, source consistency and published reading links."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,xml.etree.ElementTree as ET
from chapter6_content import manuscript,FILES
ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
D=json.loads((ROOT/'chapters/chapter6/action-framework.json').read_text());snapshot=json.loads((ROOT/'preview/content/action/chapter6.json').read_text());assert D==snapshot
assert len(D['synthesis']['findings'])==3 and len(D['evidence_notes'])==3
assert any('2.1' in l['label']['zh'] for l in D['evidence'][0]['links'])
assert len(D['tasks'])==3 and len(D['actors'])==3 and len(D['actions'])==9
assert len({a['id'] for a in D['actions']})==9
assert {(a['actor'],a['task']) for a in D['actions']}=={(a['id'],t['id']) for a in D['actors'] for t in D['tasks']}
assert (ROOT/'chapters/chapter6/第六章-未来展望与政策建议.md').read_text()==manuscript(D)
for lang in ['zh','en']:
 text=(args.output/f'2026/{lang}/chapters/06/index.html').read_text();page=Page(text);ids=[a['id'] for tag,a in page.tags if 'id'in a]
 assert len(ids)==len(set(ids));assert all(f'ch06-s0{i}'in ids for i in range(1,6))
 assert sum('data-action-figure'in a for tag,a in page.tags)==5
 assert sum('data-action-article'in a for tag,a in page.tags)==9
 for a in D['actions']:assert 'action-'+a['id'] in ids
 assert 'chapter6.js' in text and 'chapter6.css' in text
 for key,stem in FILES.items():
  f=args.output/'assets/action'/(stem+('' if lang=='zh' else '-en')+'.svg');svg=ET.parse(f).getroot();assert svg.attrib['viewBox'] in ['0 0 880 1000','0 0 880 1060','0 0 880 1260','0 0 880 1360'];assert len(svg.findall('.//{http://www.w3.org/2000/svg}text'))>15
  assert f.read_bytes()==(ROOT/'figures/chapter6'/f.name).read_bytes()
 assert ('持续共同创造及其公共价值' if lang=='zh' else 'Sustained co-creation and its public value')in text
for route in ['','introduction/']:
 t=(args.output/'2026/zh'/route/'index.html').read_text();assert '第六章保留已确定的结构' not in t;assert '完整建议将结合各章证据继续完善' not in t
print('PASS: Chapter 6 has five sections, three shared tasks, nine uniquely mapped actions, five bilingual diagrams and ten matching editable print figures. Canonical manuscript and snapshot agree.')
