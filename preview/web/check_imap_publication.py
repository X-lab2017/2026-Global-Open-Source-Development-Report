from goso_reading import web_paragraph
"""Protect I-Map data versions, prose, static figures and publication bounds."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,hashlib,re,xml.etree.ElementTree as ET
import imap_publication as p
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--pdf',action='store_true');args=parser.parse_args();base=args.output/'assets/imap';dest=base/'print';spec=json.loads((dest/'publication-spec.json').read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
assert spec['edition']==p.EDITION and spec['pages']==5
assert spec['figure_pages']=={'2-3-1':2,'2-3-2':3,'2-3-3':4}
assert spec['pdf_sha256']==digest(dest/p.PDF_NAME)
expected={'observations.json':'00115083eb0bc90c07fc940d0ee6664e4ce09507c97ea5e3802067d7f80b5c67','influence.json':'523b4bbfb9b598e5d8154003cecb1a56fce890fff3df42ed63f2761f826882b6'}
assert spec['data_sha256']==expected
for name,sha in expected.items():assert digest(base/name)==sha
assert hashlib.sha256(p.manuscript().encode()).hexdigest()==spec['manuscript_sha256']
class Text(HTMLParser):
 def __init__(self,s):super().__init__();self.parts=[];self.feed(s)
 def handle_data(self,s):self.parts.append(s)
norm=lambda s:re.sub(r'\s+','',s)
paragraphs=[p.INTRO,p.QUESTION,p.POSITION,p.FINDING,p.WINDOW,p.ACTION_TITLE,p.ACTION_INTRO,p.BRIDGE,*p.NOTES]+[t for _,ps in p.STORIES+p.STRATEGIES for t in ps]
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text();section=html[html.index('id="ch02-s03"'):html.index('id="ch02-s04"')];text=norm(''.join(Text(section).parts))
 for t in paragraphs:assert norm(web_paragraph(t,3)) in text,t
 assert section.count('class="im-download"')==1 and section.count('class="im-print-view ')==3
 for key,f in p.FIGURES.items():assert section.index(f'id="im-{key}"')<section.index(f'id="fig-{f["id"]}"')<section.index(f'data-im-reading="{key}"')
 assert re.findall(r'data-im-china-view="([^"]+)"',section)==['growth','sources']
 for stale in ['20.78%','61.72%','273.1万','89.7%']:assert stale not in section
 assert 'data-goso-source-notes=' in section
ns={'s':'http://www.w3.org/2000/svg'}
for f in p.FIGURES.values():
 tree=ET.parse(dest/f['file']);assert tree.getroot().find('s:title',ns) is not None
 for t in tree.findall('.//s:text',ns):assert 8.5<=float(t.attrib['font-size'])<=11.2,(f['file'],t.text)
geo=json.loads((p.ROOT/'content/vmap/map-geometry.json').read_text())['world'];paths=[x for x in ET.parse(dest/p.FIGURES['world']['file']).findall('.//s:path',ns) if 'transform' in x.attrib]
assert len(paths)==len(geo)
for path,g in zip(paths,geo):assert path.attrib['d']==g['d'] and path.attrib['fill-rule']=='evenodd'
for country,wanted in [('China',[79.22,14.02,6.76]),('United States',[38.28,39.66,22.06])]:
 rows=[r for r in p.D['international'] if r['project_country']==country];local=next(r['share_pct'] for r in rows if r['developer_country']==country);total=sum(r['share_pct'] for r in rows);assert [round(local,2),round(total-local,2),round(100-total,2)]==wanted
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
 assert len(doc.get_toc())>=8
print('PASS: I-Map unchanged data, shared prose, three vector figures, five-page PDF and source-share boundaries'+('; PDF text and page bounds checked' if args.pdf else ''))
