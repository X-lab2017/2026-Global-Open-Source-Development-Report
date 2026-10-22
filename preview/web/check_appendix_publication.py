"""Verify Appendix A prose parity, publication geometry and the two-appendix structure."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,json,re
import fitz
from appendix_publication import DIRECTORY,PDF_NAME
ROOT=Path(__file__).resolve().parents[2]
class Text(HTMLParser):
 def __init__(self,raw):super().__init__();self.parts=[];self.feed(raw)
 def handle_data(self,data):self.parts.append(data)
def plain(s):return re.sub(r'[#*\x60|]','',re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s))
def norm(s):return re.sub(r'\s+','',plain(s))
def blocks(text):
 for line in text.splitlines():
  if not line.strip() or line.startswith('# ') or re.match(r'^\|[\s:|\-]+\|$',line):continue
  for cell in line.strip('|').split('|'):yield norm(cell)
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();out=args.output
 m=json.loads((ROOT/'preview/content/manifest.json').read_text());apps=[x for x in m['back_matter'] if x['kind']!='downloads']
 assert [x['id'] for x in apps]==['appendix-a','appendix-b']
 assert all(x['kind']!='declaration' for x in m['back_matter'])
 for lang,source in [('zh','appendices/附录A-指标体系与数据来源.md'),('en','appendices/appendix-a.en.md')]:
  raw=(out/f'2026/{lang}/methodology/index.html').read_text()
  body=raw.split('<article class="methods-publication">',1)[1].split('</article>',1)[0]
  text=norm(''.join(Text(body).parts))
  for b in blocks((ROOT/source).read_text()):assert b in text,('web',lang,b[:80])
  assert 'translation is in preparation' not in body
  assert len(re.findall(r'<h3 id=',body))==8
  for route in ['', 'chapters/06/', 'methodology/', 'appendices/dpg/','downloads/']:
   h=(out/f'2026/{lang}'/route/'index.html').read_text()
   assert '附录 C：' not in h and 'Appendix C:' not in h and '附录 B：宣言' not in h
  redirect=(out/f'2026/{lang}/appendices/declaration/index.html').read_text()
  assert 'http-equiv="refresh"' in redirect and '#declaration-source' in redirect
  intro=(out/f'2026/{lang}/introduction/index.html').read_text()
  assert 'id="declaration-source"' in intro
 search=json.loads((out/'assets/search-index.json').read_text())
 assert not any('/appendices/declaration/' in x['url'] for x in search)
 meta=json.loads((DIRECTORY/'edition-manifest.json').read_text());pdf=DIRECTORY/PDF_NAME
 assert hashlib.sha256(pdf.read_bytes()).hexdigest()==meta['pdf_sha256']
 assert (out/'assets/report/appendix-a'/PDF_NAME).read_bytes()==pdf.read_bytes()
 for src,digest in meta['source_sha256'].items():assert hashlib.sha256((ROOT/src).read_bytes()).hexdigest()==digest
 doc=fitz.open(pdf);assert len(doc)==meta['pages'] and len(doc.get_toc())==8
 text=norm(''.join(b[4] for p in doc for b in p.get_text('blocks') if b[1]>=50 and b[3]<790))
 for b in blocks((ROOT/'appendices/附录A-指标体系与数据来源.md').read_text()):
  assert b in text,('pdf',b[:100])
 qa=ROOT/'tmp/publication-review';qa.mkdir(parents=True,exist_ok=True)
 for i,page in enumerate(doc):
  assert abs(page.rect.width-595.28)<1 and abs(page.rect.height-841.89)<1
  assert len(page.get_text().strip())>100,('empty page',i+1)
  for block in page.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     assert x0>=44 and x1<=page.rect.width-44 and y0>=15 and y1<=page.rect.height-12,('text outside margins',i+1,span['bbox'],span['text'])
     assert span['size']>=8,('small type',i+1,span['text'])
  page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(qa/f'appendix-a-{i+1:02d}.png')
 (qa/'checks.json').write_text(json.dumps({'appendices':2,'appendix_a_pages':len(doc),'web_languages':['zh','en'],'source_parity':True,'a4_portrait':True,'manual_visual_review':'pending: local execution environment unavailable'},indent=2)+'\n')
 print(f'PASS: two appendices; eight sections; complete bilingual web and {len(doc)}-page A4 PDF; source hashes, redirects, search, type sizes and text bounds.')
if __name__=='__main__':main()
