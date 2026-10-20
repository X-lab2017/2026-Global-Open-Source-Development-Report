from goso_reading import web_paragraph
"""Publication gate: D-Map source identity, independent samples and shared prose."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,hashlib,re,xml.etree.ElementTree as ET
import dmap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args();base=args.output/'assets/dmap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
assert spec['edition']==p.EDITION and spec['pages']==5
assert spec['figure_pages']=={'2-6-1':2,'2-6-2':3,'2-6-3':4}
assert spec['pdf_sha256']==digest(dest/p.PDF_NAME)==digest(dest/p.PDF_RELEASE_NAME)
expected={'data.json':'811a932193490b9e2597216f8f9f3ea6f05f2293b1d5034596e7ee50e59d7224','source/fig-2-5-1_country_contribution_share_trend.csv':'638892993df7769167436e6101ff27620c46117bdaa7358ebf8b4696ab9c6811','source/fig-2-5-2_cross_border_project_contribution_flow.csv':'aa9e64aaf25ad6c653061e48f39a92d64692d57d1b2963e4eb99dc74cdc7fc9b','source/table-2-5-1_china_us_project_contribution_top10.csv':'590aeb718d75dabf12d334f24d1b54b61867eb0ac458ec8b9fae077c8bb62d3c'}
assert spec['data_sha256']==expected
for name,sha in expected.items():assert digest(base/name)==sha
assert spec['manuscript_sha256']==hashlib.sha256(p.manuscript().encode()).hexdigest()
assert (p.ROOT.parent/'chapters/chapter2/2.5-全球开源多样性地图-D-Map.md').read_text()==p.manuscript()
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.ACTION_INTRO,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s06"'):html.index('id="ch02-s07"')];text=norm(''.join(Text(section).parts))
 for t in paragraphs:assert norm(web_paragraph(t,6)) in text,t
 assert section.count('class="dm-download"')==1 and section.count('class="dm-print-view"')==3
 assert f'print/{p.PDF_RELEASE_NAME}' in section and section.count('data-slide-height="860"')==3
 for key,f in p.FIGURES.items():assert section.index(f'id="dm-story-{key}"')<section.index(f'id="fig-{f["id"]}"')
 for stale in ['goso-unified-canvas','假设社区','持续共建地图','data-dm-dataset','AcademicShare']:assert stale not in section
 assert '<summary>统计范围与指标说明</summary>' in section
css=(args.output/'dmap-publication.css').read_text()
for selector,area,row in [('.viz-heading','heading',1),('.dm-toolbar','toolbar',2),('.dm-panel','chart',3),('figcaption','caption',4)]:assert f'.dmap-review .dm-figure.screen-slide>{selector}'+'{'+f'grid-area:{area};grid-row:{row};grid-column:1'+'}' in css
js=(args.output/'dmap.js').read_text()
for stale in ['renderCocreation','S.dataset','S.weight','缓慢拓宽']:assert stale not in js
ns={'s':'http://www.w3.org/2000/svg'}
for f in p.FIGURES.values():
 tree=ET.parse(dest/f['file']);assert tree.getroot().find('s:title',ns) is not None
 for t in tree.findall('.//s:text',ns):assert 8.5<=float(t.attrib['font-size'])<=11.2
D=p.D
assert len(D['flows'])==60 and len({r['source'] for r in D['flows']})==14
for c,local in [('CN',79.22),('US',38.28)]:
 rows=[r for r in D['sourceShares'] if r['target']==c];assert round(sum(r['share'] for r in rows),2)==100
 assert next(r['share'] for r in rows if r['source']==c)==local
assert round(sum(r['value'] for r in D['flows'] if r['target']=='US'),2)==402786.40
assert round(sum(r['value'] for r in D['flows'] if r['target']=='CN'),2)==52614.39
if args.pdf:
 import fitz
 doc=fitz.open(dest/p.PDF_NAME);assert len(doc)==5 and [i+1 for i,page in enumerate(doc) if page.rect.width>page.rect.height]==[2]
 text=norm(''.join(page.get_text() for page in doc))
 for t in paragraphs:assert norm(t) in text,t
 for page in doc:
  assert not page.get_images()
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:assert span['size']>=8 and span['bbox'][0]>=0 and span['bbox'][1]>=0 and span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15
 assert len(doc.get_toc())>=7
print('PASS: D-Map pinned source data, separate denominators, common prose and five-page vector publication'+('; PDF text and bounds checked' if args.pdf else ''))
