from goso_reading import web_paragraph
"""Shared text, source geometry, final typography and the printable C-Map edition."""
from pathlib import Path
import argparse,json,hashlib,re,xml.etree.ElementTree as ET
from html.parser import HTMLParser
import cmap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args();base=args.output/'assets/cmap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
assert spec['baseline']=='GOSO-PUB-20261020' and spec['edition']==p.EDITION and spec['pages']==6
assert hashlib.sha256((dest/p.PDF_NAME).read_bytes()).hexdigest()==spec['pdf_sha256']
assert hashlib.sha256((base/'data.json').read_bytes()).hexdigest()==spec['data_sha256']
assert hashlib.sha256(p.manuscript().encode()).hexdigest()==spec['manuscript_sha256']
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.ACTION_INTRO,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s02"'):html.index('id="ch02-s03"')];text=norm(''.join(Text(section).parts))
 for paragraph in paragraphs:assert norm(web_paragraph(paragraph,2)) in text,paragraph
 assert section.count('class="cm-download"')==1 and section.count('class="cm-publication-views"')==4
 for key in p.FIGURES:assert section.index(f'id="cmap-{key}"')<section.index(f'id="fig-cmap-{key}"')<section.index(f'data-cmap-reading="{key}"')
 assert 'data-goso-source-notes=' in section
ns={'s':'http://www.w3.org/2000/svg'}
for f in p.FIGURES.values():
 for name in f['files']:
  tree=ET.parse(dest/name)
  for text in tree.findall('.//s:text',ns):assert 8.5<=float(text.attrib['font-size'])<=11.2,(name,text.text)
  assert tree.getroot().find('s:title',ns) is not None
geo=json.loads((p.ROOT/'content/vmap/map-geometry.json').read_text())
for scope,name in [('world','fig-2-2-1_global.svg'),('china','fig-2-2-3_china.svg'),('world','fig-2-2-4_network.svg')]:
 paths=[x for x in ET.parse(dest/name).findall('.//s:path',ns) if 'transform' in x.attrib];assert len(paths)==len(geo[scope])
 for path,g in zip(paths,geo[scope]):assert path.attrib['d']==g['d'] and path.attrib['fill-rule']=='evenodd'
assert spec['figure_pages']=={'2-2-1':2,'2-2-2':3,'2-2-3':4,'2-2-4':5}
if args.pdf:
 import fitz
 doc=fitz.open(dest/p.PDF_NAME);assert len(doc)==6
 assert [i+1 for i,page in enumerate(doc) if page.rect.width>page.rect.height]==[2]
 text=norm(''.join(page.get_text() for page in doc))
 for paragraph in paragraphs:assert norm(paragraph) in text,paragraph
 for page in doc:
  assert not page.get_images()
  for b in page.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    for span in line['spans']:
     assert span['size']>=8 and span['bbox'][0]>=0 and span['bbox'][1]>=0
     assert span['bbox'][2]<page.rect.width-20 and span['bbox'][3]<page.rect.height-15
 assert len(doc.get_toc())>=9
print('PASS: C-Map shared manuscript, four groups/four vector panels, same map geometry, six-page layout and final-size typography'+('; PDF content and page bounds checked' if args.pdf else ''))
