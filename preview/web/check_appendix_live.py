"""Verify the actual deployed A/B PDFs, bundle, prose and download entries."""
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urljoin
import base64,hashlib,json
import fitz
from playwright.sync_api import sync_playwright
import appendix_publication as A
import appendix_b_publication as B
import appendices_publication as AB
ROOT=Path(__file__).resolve().parents[2]
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/'
def fetch(path):
 with urlopen(Request(WEB+path,headers={'User-Agent':'GOSD-publication-check'}),timeout=45) as r:return r.read()
results={};metas={}
for name,module in [('appendix-a',A),('appendix-b',B),('appendices',AB)]:
 meta=json.loads(fetch('assets/report/'+name+'/edition-manifest.json?v='+module.EDITION))
 assert meta['edition']==module.EDITION,('old edition',name,meta['edition'],module.EDITION)
 for source,digest in meta.get('source_sha256',{}).items():assert digest==hashlib.sha256((ROOT/source).read_bytes()).hexdigest()
 raw=fetch('assets/report/'+name+'/'+module.PDF_NAME+'?v='+module.EDITION)
 assert hashlib.sha256(raw).hexdigest()==meta['pdf_sha256']
 doc=fitz.open(stream=raw,filetype='pdf');assert len(doc)==meta['pages']
 results[name]={'pages':len(doc),'edition':meta['edition'],'pdf_sha256':meta['pdf_sha256']};metas[name]=meta
 if name=='appendix-b':
  for i,page in enumerate(doc):
   png=page.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).tobytes('png')
   print('REVIEW_IMAGE_LIVE_PDF_B_'+str(i+1)+' '+base64.b64encode(png).decode(),flush=True)
assert metas['appendices']['parts'][0]['pdf_sha256']==metas['appendix-a']['pdf_sha256']
assert metas['appendices']['parts'][1]['pdf_sha256']==metas['appendix-b']['pdf_sha256']
with sync_playwright() as p:
 browser=p.chromium.launch()
 for letter,route,count in [('a','methodology/',8),('b','appendices/dpg/',6)]:
  for lang,width,theme in [('zh',1440,'light'),('zh',390,'dark'),('en',1440,'light'),('en',390,'dark')]:
   page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
   response=page.goto(WEB+f'2026/{lang}/'+route,wait_until='networkidle');assert response.status==200
   page.evaluate('(theme)=>document.documentElement.dataset.theme=theme',theme);page.evaluate('document.fonts.ready')
   assert page.locator('.methods-publication h3').count()==count
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   for selector in ['.methods-download a','.appendix-companions a']:
    for link in page.locator(selector).all():assert page.request.get(urljoin(WEB,link.get_attribute('href'))).status==200
   if letter=='b':
    png=page.screenshot(animations='disabled')
    print('REVIEW_IMAGE_LIVE_WEB_B_'+lang+'_'+str(width)+'_'+theme+' '+base64.b64encode(png).decode(),flush=True)
   page.close()
 browser.close()
for lang in ['zh','en']:
 raw=fetch(f'2026/{lang}/downloads/').decode()
 assert all(module.PDF_NAME in raw for module in [A,B,AB])
front=json.loads(fetch('assets/report/frontmatter/edition-manifest.json'))
front_pdf=fetch('assets/report/frontmatter/'+front['pdf_file'])
assert hashlib.sha256(front_pdf).hexdigest()==front['pdf_sha256']
front_doc=fitz.open(stream=front_pdf,filetype='pdf')
toc=''.join(front_doc[i].get_text() for i in [1,2])
assert '附录 C' not in toc and '宣言来源与收录说明' not in toc and '附录 B' in toc
results['frontmatter_pages']=len(front_doc);results['two_appendices']=True
print('LIVE_PUBLICATION_VERIFIED '+json.dumps(results,ensure_ascii=False),flush=True)
