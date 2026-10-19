"""Check that the opening edition is complete, source-faithful and linked to the live report."""
from pathlib import Path
import argparse,json,re,hashlib,xml.etree.ElementTree as ET
from html.parser import HTMLParser
import frontmatter_publication as pub
import executive_summary as summary
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--inspect-pdf',action='store_true');args=p.parse_args()
m=json.loads(pub.MANIFEST.read_text());pdf=pub.MANIFEST.parent/pub.PDF_NAME
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
norm=lambda s:re.sub(r'\s+','',s.replace('**',''))
assert sha(pdf)==m['pdf_sha256']
for path,digest in m['manuscript_sha256'].items():assert sha(ROOT/path)==digest,path
assert sha(ROOT/'preview/content/report-assets/chapter1/GOSD-2026-chapter1.pdf')==m['chapter1_sha256']
assert (ROOT/'outline/执行摘要.md').read_text()==summary.manuscript('zh')
assert (ROOT/'outline/executive-summary.en.md').read_text()==summary.manuscript('en')
figs=list(pub.MANIFEST.parent.glob('*.svg'));assert len(figs)==1
svg=ET.fromstring(figs[0].read_text());texts=svg.findall('.//{http://www.w3.org/2000/svg}text')
assert '图 引-' not in ''.join(svg.itertext())
assert max(float(x.get('font-size')) for x in texts)*503.275590551/640<=11.2
if args.output:
 class Text(HTMLParser):
  def __init__(self,raw):super().__init__();self.s=[];self.feed(raw)
  def handle_data(self,data):self.s.append(data)
 for lang in ['zh','en']:
  raw=(args.output/f'2026/{lang}/summary/index.html').read_text();txt=norm(''.join(Text(raw).s))
  for kind,value in summary.paragraphs(lang):
   for part in (value[1:] if isinstance(value,tuple) else [value]):assert norm(part) in txt,(kind,part[:50])
  assert '<figure' not in raw.split('<article class="executive-summary"')[1].split('</article>')[0]
  assert 'data-es-switcher' not in raw and 'executive-summary.js' not in raw
  intro=(args.output/f'2026/{lang}/introduction/index.html').read_text();txt=norm(''.join(Text(intro).s))
  manuscript=(ROOT/('chapters/引言-人工智能时代的开源发展.md' if lang=='zh' else 'chapters/introduction.en.md')).read_text()
  for para in manuscript.split('\n\n'):
   if para.strip() and not para.startswith('#'):assert norm(para) in txt,para[:50]
  for file in [('index.html' if lang=='zh' else 'en/index.html'),f'2026/{lang}/index.html',f'2026/{lang}/summary/index.html',f'2026/{lang}/introduction/index.html']:
   h=(args.output/file).read_text();assert h.count('class="front-print-edition"')==1 and pub.PDF_NAME in h
 assert (args.output/'assets/report/frontmatter'/pub.PDF_NAME).read_bytes()==pdf.read_bytes()
if args.inspect_pdf:
 from pypdf import PdfReader
 import fitz
 r=PdfReader(pdf);assert len(r.pages)==m['pages'];pages=[norm(p.extract_text()) for p in r.pages];text=''.join(pages)
 for file in ['outline/执行摘要.md','chapters/引言-人工智能时代的开源发展.md']:
  for para in (ROOT/file).read_text().split('\n\n'):
   if para.strip() and not para.startswith('#'):
    for line in para.splitlines():
     line=line.removeprefix('- ').removeprefix('证据范围：').removeprefix('行动启示：')
     assert norm(line) in text,(file,line[:70])
 assert m['figure_pages'].keys()=={'declaration-overview'}
 front_text=''.join(pages[:m['front_pages']]);assert all(norm(v) not in front_text for v in ['PDF 页码 / 在线','前置篇目','图 引-1','图 摘-'])
 assert norm(pub.copy('cover_note','zh')) in pages[0]
 assert norm(pub.copy('cover_theme','zh')) in pages[0]
 toc=''.join(pages[1:3]);manifest=json.loads((ROOT/'preview/content/manifest.json').read_text())
 for chapter in manifest['chapters']:
  for s in chapter['sections']:assert norm(s['number']+' '+s['title']['zh']) in toc
 assert r.page_labels[1]=='i' and r.page_labels[m['front_pages']]=='1'
 for page in r.pages[1:3]:
  for a in page.get('/Annots',[]):
   annot=a.get_object();rect=[float(x) for x in annot['/Rect']];assert 0<=rect[0]<rect[2]<=595.3 and 0<=rect[1]<rect[3]<=841.9
 # Appending preserves every first-chapter page exactly, including fonts and graphics.
 chapter=fitz.open(ROOT/'preview/content/report-assets/chapter1/GOSD-2026-chapter1.pdf');merged=fitz.open(pdf)
 for i in range(len(chapter)):
  assert chapter[i].get_pixmap().samples==merged[m['front_pages']+i].get_pixmap().samples,f'Chapter page changed: {i+1}'
print(f'PASS: {m["pages"]}-page opening edition, a narrative executive summary and unnumbered declaration overview, same bilingual source prose and unchanged Chapter 1.'+(' PDF prose, contents, labels, links and all 12 appended page renderings verified.' if args.inspect_pdf else ''))
