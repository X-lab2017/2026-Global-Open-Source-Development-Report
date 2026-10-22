"""Check the deployed appendix and return compact review images in Actions logs."""
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import URLError
import base64,hashlib,json,re,time
from appendix_publication import EDITION
import fitz
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/'
def fetch(path):
 with urlopen(Request(WEB+path,headers={'User-Agent':'GOSD-publication-check'}),timeout=45) as r:return r.read()
meta=json.loads(fetch('assets/report/appendix-a/edition-manifest.json?v='+EDITION))
assert meta['edition']==EDITION,('old edition',meta['edition'],EDITION)
source='appendices/附录A-指标体系与数据来源.md'
assert meta['source_sha256'][source]==hashlib.sha256((ROOT/source).read_bytes()).hexdigest()
raw=fetch('assets/report/appendix-a/GOSD-2026-appendix-a.pdf')
assert hashlib.sha256(raw).hexdigest()==meta['pdf_sha256']
doc=fitz.open(stream=raw,filetype='pdf');assert len(doc)==meta['pages']
for i,page in enumerate(doc):
 png=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).tobytes('png')
 print('REVIEW_IMAGE_PDF_'+str(i+1)+' '+base64.b64encode(png).decode(),flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch()
 for lang,width,theme in [('zh',1440,'light'),('zh',1440,'dark'),('zh',390,'light'),('zh',390,'dark'),('en',1440,'light'),('en',390,'dark')]:
  page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
  response=page.goto(WEB+f'2026/{lang}/methodology/',wait_until='networkidle')
  assert response.status==200
  page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme)
  page.evaluate('document.fonts.ready')
  assert page.locator('.methods-publication h3').count()==8
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  png=page.screenshot(animations='disabled')
  print('REVIEW_IMAGE_WEB_'+lang+'_'+str(width)+'_'+theme+' '+base64.b64encode(png).decode(),flush=True)
  page.close()
 browser.close()
front=json.loads(fetch('assets/report/frontmatter/edition-manifest.json'))
front_pdf=fetch('assets/report/frontmatter/'+front['pdf_file'])
assert hashlib.sha256(front_pdf).hexdigest()==front['pdf_sha256']
front_doc=fitz.open(stream=front_pdf,filetype='pdf')
toc=''.join(front_doc[i].get_text() for i in [1,2])
assert '附录 C' not in toc and '宣言来源与收录说明' not in toc and '附录 B' in toc
print('LIVE_PUBLICATION_VERIFIED '+json.dumps({'edition':meta['edition'],'appendix_a_pages':len(doc),'pdf_sha256':meta['pdf_sha256'],'frontmatter_pages':len(front_doc),'two_appendices':True,'source_sha256':meta['source_sha256'][source]},ensure_ascii=False),flush=True)
