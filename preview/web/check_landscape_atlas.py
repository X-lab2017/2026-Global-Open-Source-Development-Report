"""Check complete and non-overlapping architecture plates without browser assumptions."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import landscape_atlas as A

parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
payload=json.loads((args.output/'assets/landscape/v3-data.json').read_text())
seen=[]
for layer,layout in A.LAYOUTS.items():
    expected={p['id'] for p in payload['projects'] if p['layer']==layer}
    root=ET.fromstring(A.map_svg(layer))
    assert root.attrib['viewBox']=='0 0 1600 900'
    nodes=[n for n in root.iter() if 'data-atlas-project' in n.attrib]
    ids=[n.attrib['data-atlas-project'] for n in nodes]
    assert len(ids)==len(set(ids)) and set(ids)==expected
    seen+=ids
    categories=[n for n in root.iter() if 'data-atlas-section' in n.attrib]
    assert len(categories)==(12 if layer=='Agent Infra' else 13)
    boxes=[]
    for g in categories:
        x,y,w,h=map(float,g.attrib['data-box'].split())
        assert x>=0 and y>=58 and x+w<=1600 and y+h<=774
        for ox,oy,ow,oh in boxes:
            assert x>=ox+ow or ox>=x+w or y>=oy+oh or oy>=y+h
        boxes.append((x,y,w,h))
        rects=[]
        for tile in [n for n in g.iter() if 'data-atlas-project' in n.attrib]:
            r=next(n for n in tile if n.attrib.get('class')=='al-atlas-project-bg')
            px,py,pw,ph=[float(r.attrib[k]) for k in ['x','y','width','height']]
            assert x<=px and y<=py and px+pw<=x+w and py+ph<=y+h
            for ox,oy,ow,oh in rects:
                assert px>=ox+ow or ox>=px+pw or py>=oy+oh or oy>=py+ph
            rects.append((px,py,pw,ph))
            p=next(p for p in payload['projects'] if p['id']==tile.attrib['data-atlas-project'])
            assert p['section']==g.attrib['data-atlas-section']
            assert any(n.text==p['name'] for n in tile)
            assert tile.attrib['role']=='button' and tile.attrib['tabindex']=='0'
assert len(seen)==145 and len(set(seen))==145
page=(args.output/'2026/zh/chapters/04/index.html').read_text()
assert 'data-atlas-version="4.1-atlas-v1"' in page
assert 'landscape-atlas.js?v=4.1-polish-v1' in page
assert page.count('data-atlas-month')==2 and page.count('data-atlas-search')==2
assert 'data-search=' not in page and 'id="al-month"' not in page
print('PASS structural atlas: 145 unique projects, 25 exact categories, two 1600×900 plates, non-overlapping module/project bounds, complete names, keyboard controls and independent local selectors.')
