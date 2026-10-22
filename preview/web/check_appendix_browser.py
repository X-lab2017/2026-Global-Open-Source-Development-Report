"""Check Appendix A in Chromium at desktop and phone widths, in both themes."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from urllib.parse import urlsplit
import argparse,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--base-path',default='');args=p.parse_args()
base=args.base_path.rstrip('/')
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):
  if base and path.startswith(base+'/'):path=path[len(base):]
  return super().translate_path(path)
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(args.output.resolve())))
Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_address[1]}'
qa=ROOT/'tmp/publication-review';qa.mkdir(parents=True,exist_ok=True)
checks=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  for lang in ['zh','en']:
   for width in [1440,390]:
    for theme in ['light','dark']:
     page=browser.new_page(viewport={'width':width,'height':960},reduced_motion='reduce')
     errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
     response=page.goto(origin+base+f'/2026/{lang}/methodology/',wait_until='networkidle')
     assert response.status==200
     page.evaluate('(theme)=>{document.documentElement.dataset.theme=theme}',theme)
     page.evaluate('document.fonts.ready')
     assert page.locator('.methods-publication h3').count()==8
     measure=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,tables:[...document.querySelectorAll(".methods-publication .reader-table-wrap")].map(e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,width:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflowX})),paragraphs:[...document.querySelectorAll(".methods-publication .manuscript>p")].map(e=>({width:e.getBoundingClientRect().width,font:parseFloat(getComputedStyle(e).fontSize)}))})''')
     assert measure['scroll']<=width+1,('page overflow',lang,width,theme,measure)
     assert all(t['left']>=0 and t['right']<=width+1 and t['overflow'] in ['auto','scroll'] for t in measure['tables']),measure
     assert all(x['width']>=260 and x['font']>=15 for x in measure['paragraphs']),measure
     assert not errors,errors
     link=page.locator('.methods-download a').get_attribute('href')
     assert page.request.get(origin+link).status==200
     page.screenshot(path=str(qa/f'web-{lang}-{width}-{theme}.png'),full_page=True,animations='disabled')
     checks.append({'lang':lang,'width':width,'theme':theme,'horizontal_overflow':False,'js_errors':errors})
     page.close()
  page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':960})
  page.goto(origin+base+'/2026/zh/methodology/')
  assert page.locator('.methods-publication h3').count()==8 and page.locator('.methods-download a').is_visible()
  page.close();browser.close()
finally:server.shutdown();server.server_close()
(qa/'browser-checks.json').write_text(json.dumps({'chromium':checks,'no_javascript_content':True,'screenshots_reviewed_manually':False},indent=2)+'\n')
print('PASS: Appendix A in Chromium, Chinese/English, 1440/390px, light/dark, reduced motion, PDF download, no JavaScript errors or page overflow; content remains available without JavaScript.')
