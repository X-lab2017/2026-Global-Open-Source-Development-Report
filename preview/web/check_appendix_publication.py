"""Verify both appendices' prose, PDF geometry, bundle and report integration."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,json,re
import fitz
import appendix_publication as A
import appendix_b_publication as B
import appendices_publication as AB
ROOT=Path(__file__).resolve().parents[2]
SPECS=[('a',A,'methodology/','appendices/附录A-指标体系与数据来源.md','appendices/appendix-a.en.md',8),('b',B,'appendices/dpg/','appendices/附录-开源人工智能数字公共产品-DPG-评估框架.md','appendices/appendix-b.en.md',6)]
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
 assert all(x['status']=='published' and x['source_path_en'] for x in apps)
 search=json.loads((out/'assets/search-index.json').read_text())
 assert not any('/appendices/declaration/' in x['url'] for x in search)
 qa=ROOT/'tmp/publication-review';qa.mkdir(parents=True,exist_ok=True)
 docs={};results={}
 for letter,module,route,zh,en,count in SPECS:
  for lang,source in [('zh',zh),('en',en)]:
   raw=(out/f'2026/{lang}'/route/'index.html').read_text()
   body=raw.split('<article class="methods-publication">',1)[1].split('</article>',1)[0]
   text=norm(''.join(Text(body).parts))
   for b in blocks((ROOT/source).read_text()):assert b in text,('web',letter,lang,b[:80])
   assert 'translation is in preparation' not in body
   assert len(re.findall(r'<h3 id=',body))==count
   assert 'GOSD-2026-appendices-A-B.pdf' in body
   assert ('/appendices/dpg/' if letter=='a' else '/methodology/') in body
   assert len([x for x in search if x['lang']==lang and '/'+route+'#' in x['url']])>=count
  meta=module.metadata();pdf=module.DIRECTORY/module.PDF_NAME
  assert hashlib.sha256(pdf.read_bytes()).hexdigest()==meta['pdf_sha256']
  assert (out/'assets/report'/('appendix-'+letter)/module.PDF_NAME).read_bytes()==pdf.read_bytes()
  for src,digest in meta['source_sha256'].items():assert hashlib.sha256((ROOT/src).read_bytes()).hexdigest()==digest
  doc=fitz.open(pdf);docs[letter]=doc
  assert len(doc)==meta['pages'] and len(doc.get_toc())==count
  text=norm(''.join(b[4] for p in doc for b in p.get_text('blocks') if b[1]>=50 and b[3]<790))
  for b in blocks((ROOT/zh).read_text()):assert b in text,('pdf',letter,b[:100])
  for i,page in enumerate(doc):
   assert abs(page.rect.width-595.28)<1 and abs(page.rect.height-841.89)<1
   assert len(page.get_text().strip())>100,('empty page',letter,i+1)
   for block in page.get_text('dict')['blocks']:
    for line in block.get('lines',[]):
     for span in line['spans']:
      x0,y0,x1,y1=span['bbox']
      assert x0>=44 and x1<=page.rect.width-44 and y0>=15 and y1<=page.rect.height-12,('text outside margins',letter,i+1,span['bbox'],span['text'])
      assert span['size']>=8,('small type',letter,i+1,span['text'])
   page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(qa/f'appendix-{letter}-{i+1:02d}.png')
  results[letter]={'pages':len(doc),'source_parity':True,'a4_portrait':True,'pdf_sha256':meta['pdf_sha256']}
 for lang in ['zh','en']:
  for route in ['', 'chapters/06/', 'methodology/', 'appendices/dpg/','downloads/']:
   raw=(out/f'2026/{lang}'/route/'index.html').read_text()
   assert '附录 C：' not in raw and 'Appendix C:' not in raw and '附录 B：宣言' not in raw
  redirect=(out/f'2026/{lang}/appendices/declaration/index.html').read_text()
  assert 'http-equiv="refresh"' in redirect and '#declaration-source' in redirect
  assert 'id="declaration-source"' in (out/f'2026/{lang}/introduction/index.html').read_text()
  downloads=(out/f'2026/{lang}/downloads/index.html').read_text()
  for module in [A,B,AB]:assert module.PDF_NAME in downloads
 meta=AB.metadata();pdf=AB.DIRECTORY/AB.PDF_NAME;bundle=fitz.open(pdf)
 assert (out/'assets/report/appendices'/AB.PDF_NAME).read_bytes()==pdf.read_bytes()
 assert hashlib.sha256(pdf.read_bytes()).hexdigest()==meta['pdf_sha256']
 assert len(bundle)==len(docs['a'])+len(docs['b'])==meta['pages']
 assert len(bundle.get_toc())==16 and [x[1] for x in bundle.get_toc() if x[0]==1]==['附录 A','附录 B']
 offset=0
 for letter in ['a','b']:
  for i,page in enumerate(docs[letter]):
   assert bundle[offset+i].get_text()==page.get_text()
   assert bundle[offset+i].get_pixmap().samples==page.get_pixmap().samples
   assert bundle[offset+i].get_label()==letter.upper()+'-'+str(i+1)
  offset+=len(docs[letter])
 cases=json.loads((ROOT/'preview/content/gosm/cases.json').read_text())
 for model in cases['models']:
  assert model['revision'][:8] in (ROOT/SPECS[1][3]).read_text()
 (qa/'checks.json').write_text(json.dumps({'appendices':results,'bundle_pages':len(bundle),'manual_visual_review':'pending rendered-page inspection'},indent=2)+'\n')
 print('PASS: complete bilingual A/B manuscripts; original sample records; source hashes, search, navigation and downloads; PDF geometry; bundle pages pixel-identical to separate PDFs; hierarchical bookmarks and A/B page labels.')
if __name__=='__main__':main()
