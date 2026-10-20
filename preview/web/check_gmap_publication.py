"""G-Map gate: retain sources, synchronize prose, preserve print legibility."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,hashlib,re
import gmap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');a=parser.parse_args()
base=a.output/'assets/gmap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
expected={'fig-2-6-1_foundation_share_and_active_repositories.csv':'87daef3d6e3a2ffcb5badbe5a29d1058d7bed11f2ea2fe541353f508d61cb03b','fig-2-6-2_active_repository_license_trend.csv':'1dcd66ec2178fe5bc30fcdffa63789cd867be4afe15df58f8503af65c36286be','fig-2-6-3_mulan_permissive_license_trend.csv':'9754fe533dfeb8d09464e680e0a2c97225facbcb73cf958d45d3f21039813635'}
assert spec['edition']==p.EDITION and spec['pages']==4 and spec['data_sha256']==expected
for name,sha in expected.items():assert digest(base/name)==sha,name
assert spec['pdf_sha256']==digest(dest/p.PDF_NAME)==digest(dest/p.PDF_RELEASE_NAME)
assert spec['manuscript_sha256']==hashlib.sha256(p.manuscript().encode()).hexdigest()
assert (base/'chapter-2-7.md').read_text()==p.manuscript()
assert (p.ROOT.parent/'chapters/chapter2/2.6-全球开源治理与社会公益地图-G-Map.md').read_text()==p.manuscript()
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(a.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s07"'):];txt=norm(''.join(Text(section).parts))
 for t in paragraphs:assert norm(t) in txt,t
 assert section.count('data-slide-height="860"')==3
 assert f'print/{p.PDF_RELEASE_NAME}' in section
 assert '<summary>统计范围与指标说明</summary>' in section
 for i in range(1,4):assert f'图 2-7-{i}' in section
js=(a.output/'gmap.js').read_text()
assert 'D.simulation' not in js and 'gm-country-rank' not in js
assert 'data-gm-license' in js and 'data-gm-year' in js
assert spec['figure_pages']=={'2-7-1':1,'2-7-2':2,'2-7-3':3}
assert not (base/'simulation.json').exists() and not (base/'data.js').exists()
data=json.loads((base/'publication-data.js').read_text().split('=',1)[1].rstrip(';\n'))
assert set(data)=={'series'} and data['series']==p.D['series']
assert 'data-gm-tab' not in section and 'fig-2-7-4' not in section and 'fig-2-7-5' not in section
if a.pdf:
 import fitz
 doc=fitz.open(dest/p.PDF_NAME);assert len(doc)==4 and all(page.rect.width<page.rect.height for page in doc)
 txt=norm(''.join(page.get_text() for page in doc))
 for t in paragraphs:assert norm(t) in txt,t
 for page in doc:
  assert not page.get_images()
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:assert span['size']>=8 and span['bbox'][0]>=0 and span['bbox'][1]>=0 and span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15,span
print('PASS: G-Map source hashes, shared Web/PDF prose, three original figures, four portrait pages and scope labels'+('; PDF text and bounds checked' if a.pdf else ''))
