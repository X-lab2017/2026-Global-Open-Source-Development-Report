"""Guard T-Map data identity, common prose, chart families and publication bounds."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,hashlib,re,xml.etree.ElementTree as ET
import tmap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args();base=args.output/'assets/tmap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
assert spec['edition']==p.EDITION and spec['pages']==6
assert spec['figure_pages']=={'2-4-1':2,'2-4-2':3,'2-4-3':4,'2-4-4':5}
assert spec['pdf_sha256']==digest(dest/p.PDF_NAME)
assert digest(dest/p.PDF_RELEASE_NAME)==digest(dest/p.PDF_NAME)
assert spec['release_pdf']==p.PDF_RELEASE_NAME and spec['revision']==p.PDF_REVISION
for name in ['GOSD-2026-section-2-4-20261020-network.pdf','GOSD-2026-section-2-4-20261020-community.pdf']:
 assert digest(dest/name)==digest(dest/p.PDF_NAME)
for retired in ['network-concept.json','network-concept.js','community-snapshot.json','print/fig-2-4-1_network.svg']:
 assert not (base/retired).exists(),retired
assert not (args.output/'tmap-network.js').exists()
expected={'observations.json':'35105a5e3d4087ff65cbab22800e0b4e84fec984b6fdf9fde95e9c21bda94813','simulation.json':'339625dc705debecb7b7bf35e59cbdc01fec7edaebc6ec2a1fe67a98b366f025'}
assert spec['data_sha256']==expected
for name,sha in expected.items():assert digest(base/name)==sha
assert hashlib.sha256(p.manuscript().encode()).hexdigest()==spec['manuscript_sha256']
css=(args.output/'tmap-publication.css').read_text()
for selector,area,row in [('.viz-heading','heading',1),('.tm-toolbar','toolbar',2),('.tm-panel','chart',3),('figcaption','caption',4)]:
 assert f'.tmap-review .tmap-figure.screen-slide>{selector}'+'{'+f'grid-area:{area};grid-row:{row};grid-column:1'+'}' in css,('T-Map grid row',selector)
assert (p.ROOT.parent/'chapters/chapter2/2.4-全球开源人才地图-T-Map.md').read_text()==p.manuscript()
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.ACTION_INTRO,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s04"'):html.index('id="ch02-s05"')];text=norm(''.join(Text(section).parts))
 for t in paragraphs:assert norm(t) in text,t
 assert section.count('class="tm-download"')==1 and section.count('class="tm-print-view"')==4
 assert f'print/{p.PDF_RELEASE_NAME}' in section and f'print/{p.PDF_NAME}' not in section
 scripts=re.findall(r'<script[^>]+src="([^"]+)"',html)
 assert all('network-concept.js' not in url and 'tmap-network.js' not in url for url in scripts)
 assert section.count('data-slide-height="860"')==4 and 'goso-unified-canvas' not in section
 assert section.count('模拟数据｜待替换')>=3
 for key,f in p.FIGURES.items():assert section.index(f'id="tm-story-{key}"')<section.index(f'id="fig-{f["id"]}"')
 for stale in ['理解人才','PsiACE','社区网络','data-tm-world=','全球约 35 万','全球人才总量为','只供版式评审','定位记录','AI 贡献角色','贡献角色','成长接续：','人才成长、留存与接续','data-tm-china="records"','data-tm-connect="ai"']:assert stale not in section
 assert section.count('data-tm-china=')==2 and section.count('data-tm-connect=')==2
 assert '<summary>统计范围与指标说明</summary>' in section
ns={'s':'http://www.w3.org/2000/svg'}
for key,f in p.FIGURES.items():
 tree=ET.parse(dest/f['file']);assert tree.getroot().find('s:title',ns) is not None
 for t in tree.findall('.//s:text',ns):assert 8.5<=float(t.attrib['font-size'])<=11.2,(f['file'],t.text)
 if key in ('connect',):assert '模拟数据｜待替换' in ''.join(tree.getroot().itertext())
for key,scope in [('world','world'),('china','china'),('connect','world')]:
 geo=json.loads((p.ROOT/'content/vmap/map-geometry.json').read_text())[scope];paths=[x for x in ET.parse(dest/p.FIGURES[key]['file']).findall('.//s:path',ns) if 'transform' in x.attrib];assert len(paths)==len(geo)
 for path,g in zip(paths,geo):assert path.attrib['d']==g['d'] and path.attrib['fill-rule']=='evenodd'
assert round((p.D['regions']['China'][-1]/p.D['regions']['China'][-2]-1)*100,1)==8.1
assert sum(v[-1]-v[0] for k,v in p.D['cities'].items() if k in ['北京','上海'])==356
if args.pdf:
 import fitz
 doc=fitz.open(dest/p.PDF_NAME);assert len(doc)==6 and [i+1 for i,page in enumerate(doc) if page.rect.width>page.rect.height]==[2]
 text=norm(''.join(page.get_text() for page in doc))
 for stale in ['图2-4-5','贡献角色','定位记录','AI贡献角色','AI领域×贡献角色','成长接续：','人才成长、留存与接续']:assert stale not in text
 assert all(term not in text for term in ['图2-4-1（续）','从真实协作理解','PsiACE','社区OpenRank'])
 for t in paragraphs:assert norm(t) in text,t
 for page in doc:
  assert norm(p.PDF_REVISION) in norm(page.get_text())
  assert not page.get_images()
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:assert span['size']>=8 and span['bbox'][0]>=0 and span['bbox'][1]>=0 and span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15
 assert len(doc.get_toc())>=9
print('PASS: T-Map pinned data, common prose, four figure groups, no explanatory network, six-page versioned publication'+('; PDF text and bounds checked' if args.pdf else ''))
