"""A-Map publication gate: source identity, separate scopes and shared prose."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,hashlib,re,csv,xml.etree.ElementTree as ET
import amap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args();base=args.output/'assets/amap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
assert spec['edition']==p.EDITION and spec['pages']==4
assert spec['figure_pages']=={'2-5-1':1,'2-5-2':2,'2-5-3':3}
assert spec['pdf_sha256']==digest(dest/p.PDF_NAME)==digest(dest/p.PDF_RELEASE_NAME)
expected={'observations.json':'3c2d9175cefcb5789db936160f6e786a84cb5d8dd609bc4de4a28b667000eb95','fig-2-7-1_platform_active_repository_trend.csv':'996852657b99c3fe9843cb0594bfe8a84fe750dedf68d4b658909b7ae1afd9de','comparison-groups.json':'77e950e1180a381d75e21e35cf4cb16eb471fecb341c98dfc96131bf8ed424c1'}
assert spec['data_sha256']==expected
for name,sha in expected.items():assert digest(base/name)==sha
assert spec['manuscript_sha256']==hashlib.sha256(p.manuscript().encode()).hexdigest()
assert (p.ROOT.parent/'chapters/chapter2/2.7-全球开源资产地图-A-Map.md').read_text()==p.manuscript()
assert (base/'chapter-2-5.md').read_text()==p.manuscript()
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.ACTION_INTRO,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s05"'):html.index('id="ch02-s06"')];text=norm(''.join(Text(section).parts))
 for t in paragraphs:assert norm(t) in text,t
 assert section.count('class="am-download"')==1 and section.count('class="am-print-view"')==3
 assert f'print/{p.PDF_RELEASE_NAME}' in section and section.count('data-slide-height="860"')==3
 for key,f in p.FIGURES.items():assert section.index(f'id="am-story-{key}"')<section.index(f'id="fig-{f["id"]}"')
 for stale in ['goso-unified-canvas','提交事件','data-am-mock','data-am-forecast','类别演进']:assert stale not in section
 assert '<summary>统计范围与指标说明</summary>' in section
 assert '/assets/amap/publication-data.js?v=20261020-v3' in html and '/assets/amap/data.js' not in html
css=(args.output/'amap-publication.css').read_text()
for selector,area,row in [('.viz-heading','heading',1),('.am-toolbar','toolbar',2),('.am-panel','chart',3),('figcaption','caption',4)]:assert f'.amap-review .am-figure.screen-slide>{selector}'+'{'+f'grid-area:{area};grid-row:{row};grid-column:1'+'}' in css
js=(args.output/'amap.js').read_text()
for stale in ['GOSD_AMAP','S.mock','commitsForecast','renderCategory']:assert stale not in js
ns={'s':'http://www.w3.org/2000/svg'}
for f in p.FIGURES.values():
 tree=ET.parse(dest/f['file']);assert tree.getroot().find('s:title',ns) is not None
 for t in tree.findall('.//s:text',ns):assert 8.5<=float(t.attrib['font-size'])<=11.2
D=p.D
assert D['platforms']['AtomGit'][:2]==[None,None]
raw=list(csv.DictReader((base/'fig-2-7-1_platform_active_repository_trend.csv').open()))
for i,row in enumerate(raw):
 for col,platform in [('GitHub','GitHub'),('Gitee','Gitee'),('GitCode','AtomGit'),('GitLab','GitLab')]:assert D['platforms'][platform][i]==(int(row[col]) if row[col] else None)
for key,total,downloads,cn,us in [('models',72280,60000691937,6017,45801),('datasets',12291,806478232,1338,5871)]:
 a=D['assets'][key];assert len(a['countries'])==14 and a['total']==total and a['downloads']==downloads
 assert sum(r['count'] for r in a['countries'])<total
 assert next(r['count'] for r in a['countries'] if r['id']=='CN')==cn
 assert next(r['count'] for r in a['countries'] if r['id']=='US')==us
 assert set(a['downloadShares'])=={'US','CN'}
 # Same metric colors and bar family in both renderers; no inferred country downloads.
 svg=(dest/p.FIGURES[key]['file']).read_text();assert p.PALETTE[0] in svg and p.PALETTE[1] in svg
assert 'opacity="${S.region' not in js
assert 'am-download-key' in js and 'am-map-stage' in js
assert "p.PALETTE[k] if k==0 else '#FFFFFF'" in (p.ROOT/'web/amap_print.py').read_text()
# Europe is a checked subtotal, never a synthetic full-region total or a zero download.
assert len(D['comparison']['memberCodes'])==28
for key,expected_count,n in [('models',10084,6),('datasets',2359,5)]:
 e=D['comparison']['assets'][key];assert e['count']==expected_count and len(e['members'])==n
 assert e['count']==sum(r['count'] for r in D['assets'][key]['countries'] if r['id'] in e['members'])
 assert e['downloadShare'] is None and e['quantityScope']=='listed_country_subtotal'
assert 'data-am-tab="code:' not in section
assert 'grid-template-columns:repeat(4,minmax(0,1fr))' in (args.output/'amap.css').read_text()
if args.pdf:
 import fitz
 doc=fitz.open(dest/p.PDF_NAME);assert len(doc)==4 and all(page.rect.width<page.rect.height for page in doc)
 text=norm(''.join(page.get_text() for page in doc))
 for t in paragraphs:assert norm(t) in text,t
 for page in doc:
  assert not page.get_images()
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:assert span['size']>=8 and span['bbox'][0]>=0 and span['bbox'][1]>=0 and span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15
 assert len(doc.get_toc())>=7
print('PASS: A-Map original values, missing-value preservation, distinct denominators, common prose and four-page portrait vector publication'+('; PDF text and bounds checked' if args.pdf else ''))
