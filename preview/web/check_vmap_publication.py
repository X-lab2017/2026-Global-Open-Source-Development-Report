from goso_reading import web_paragraph
"""Meaningful publication gates: shared prose, unchanged data and geometry, legible exports."""
from pathlib import Path
import argparse,hashlib,json,re,xml.etree.ElementTree as ET
from html.parser import HTMLParser
import vmap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args()
asset=args.output/'assets/vmap';dest=asset/'print';spec=json.loads((dest/'publication-spec.json').read_text())
ns={'s':'http://www.w3.org/2000/svg'}
assert spec['baseline']=='GOSD-PUB-20261020' and spec['pages']==6
assert hashlib.sha256((dest/p.PDF_NAME).read_bytes()).hexdigest()==spec['pdf_sha256']
assert hashlib.sha256((asset/'fig-2-1-2_platform-coverage.json').read_bytes()).hexdigest()==spec['source_sha256']
assert hashlib.sha256(p.manuscript().encode()).hexdigest()==spec['manuscript_sha256']
assert (asset/'chapter-2-1.md').read_text().strip()==p.manuscript().strip()
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
def norm(s):return re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.ACTION_INTRO,p.BRIDGE,p.QUESTION,p.POSITION,p.FINDING,p.SNAPSHOT_NOTE,p.INDICATOR_FEEDBACK,*p.GAPS]+[t for _,paras in p.STORIES+p.STRATEGIES for t in paras]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();text=norm(''.join(Text(html).parts))
 for paragraph in paragraphs:assert norm(web_paragraph(paragraph,1)) in text,paragraph
 assert html.count('class="vmap-publication-views"')==3
 assert html.count('vmap-print-panel')==4
 assert p.PDF_NAME in html
 section=html[html.index('id="ch02-s01"'):html.index('id="ch02-s02"')]
 for i,kind in enumerate(['global','regions','china']):
  fig=['global','comparison','china'][i]
  assert section.index('id="vmap-'+kind+'"') < section.index('id="fig-vmap-'+fig+'"') < section.index('data-figure-reading="'+kind+'"')
 assert section.count('class="vmap-download"')==1
 assert p.ACTION_TITLE in section
 assert '<summary>统计范围与指标说明</summary>' in section
 assert '同源正文 · 三幅图组' not in section
 assert 'class="vmap-print-evidence"' in section
for f in p.FIGURES.values():
 for name in f['files']:
  tree=ET.parse(dest/name)
  for text in tree.findall('.//s:text',ns):assert 8<=float(text.attrib['font-size'])<=11.2,(name,text.text)
  assert tree.getroot().find('s:title',ns) is not None
baseline=json.loads((args.output/'assets/baselines/goso-publication-v2.json').read_text())
assert spec['chapter_baseline']==baseline['id']=='GOSO-PUB-20261020'
for path,digest in baseline['reference_sha256'].items():
 assert hashlib.sha256((p.ROOT/path).read_bytes()).hexdigest()==digest,path
assert 'GOSO-PUB-20261020' in (args.output/'assets/baselines/current.json').read_text()
geo=json.loads((asset/'map-geometry.json').read_text())
for scope,name in [('world','fig-2-1-1_global.svg'),('china','fig-2-1-3_china.svg')]:
 tree=ET.parse(dest/name);paths=[x for x in tree.findall('.//s:path',ns) if 'transform' in x.attrib]
 assert len(paths)==len(geo[scope])
 for x,g in zip(paths,geo[scope]):
  assert x.attrib['d']==g['d']
  assert re.fullmatch(r'translate\([\d.]+,[\d.]+\) scale\([\d.]+\)',x.attrib['transform'])
  assert x.attrib['fill-rule']=='evenodd'
colors=p.SERIES_COLORS;history=ET.parse(dest/'fig-2-1-2_bc_history-scenario.svg')
assert '口径待核验' not in ''.join(history.getroot().itertext()) and '条件情景' not in ''.join(history.getroot().itertext())
assert '问卷调研去重得到' in ''.join(history.getroot().itertext())
assert spec['figure_pages']['2-1-3']==5
for i,color in enumerate(colors):
 paths=[x for x in history.findall('.//s:path',ns) if x.attrib.get('stroke')==color and x.attrib.get('stroke-width')=='1.6']
 assert paths
 if p.SERIES_DASH[i]:assert any(x.attrib.get('stroke-dasharray')==','.join(map(str,p.SERIES_DASH[i])) for x in paths)
if args.pdf:
 import fitz
 pdf=fitz.open(dest/p.PDF_NAME);assert len(pdf)==6
 assert [i+1 for i,page in enumerate(pdf) if page.rect.width>page.rect.height]==[2]
 body=norm(''.join(page.get_text() for page in pdf))
 for paragraph in paragraphs:assert norm(paragraph) in body,paragraph
 for page in pdf:
  assert not page.get_images(),'Vector publication figures must remain vector'
  for b in page.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    for span in line['spans']:
     assert all(v>=0 for v in span['bbox'][:2])
     assert span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15
     assert span['size']>=8
 assert len(pdf.get_toc())>=8
print('PASS: 2.1 shared manuscript, three figure groups/four publication panels, source hashes, original map paths, color/dash parity, evidence labels and final-size typography'+('; six-page vector PDF and one landscape page' if args.pdf else ''))
