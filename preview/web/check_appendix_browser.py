"""Check both appendices in Chromium, including narrow, dark and no-script reading."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
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
  for letter,route,count in [('a','methodology/',8),('b','appendices/dpg/',6)]:
   for lang in ['zh','en']:
    for width in [1440,390]:
     for theme in ['light','dark']:
      page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
      errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
      response=page.goto(origin+base+f'/2026/{lang}/'+route,wait_until='networkidle')
      assert response.status==200
      page.evaluate('(theme)=>{document.documentElement.dataset.theme=theme}',theme)
      page.evaluate('document.fonts.ready')
      assert page.locator('.methods-publication h3').count()==count
      measure=page.evaluate('''()=>({scroll:document.documentElement.scrollWidth,tables:[...document.querySelectorAll(".methods-publication .reader-table-wrap")].map(e=>({left:e.getBoundingClientRect().left,right:e.getBoundingClientRect().right,overflow:getComputedStyle(e).overflowX})),paragraphs:[...document.querySelectorAll(".methods-publication .manuscript>p")].map(e=>({width:e.getBoundingClientRect().width,font:parseFloat(getComputedStyle(e).fontSize)}))})''')
      assert measure['scroll']<=width+1,('page overflow',letter,lang,width,theme,measure)
      assert all(t['left']>=0 and t['right']<=width+1 and t['overflow'] in ['auto','scroll'] for t in measure['tables']),measure
      assert all(x['width']>=260 and x['font']>=15 for x in measure['paragraphs']),measure
      assert not errors,errors
      for selector in ['.methods-download a','.appendix-companions a']:
       for link in page.locator(selector).all():assert page.request.get(origin+link.get_attribute('href')).status==200
      page.screenshot(path=str(qa/f'web-{letter}-{lang}-{width}-{theme}.png'),full_page=True,animations='disabled')
      if letter=='b' or (lang=='zh' and width==1440 and theme=='light'):
       page.screenshot(path=str(qa/f'view-{letter}-{lang}-{width}-{theme}.png'),animations='disabled')
      if letter=='b' and lang=='zh' and theme=='light':
       page.locator('.methods-publication h3').nth(3).scroll_into_view_if_needed()
       page.screenshot(path=str(qa/f'view-b-standard-{width}.png'),animations='disabled')
      checks.append({'appendix':letter,'lang':lang,'width':width,'theme':theme,'horizontal_overflow':False,'js_errors':errors})
      page.close()
   page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':1000})
   page.goto(origin+base+'/2026/zh/'+route)
   assert page.locator('.methods-publication h3').count()==count and page.locator('.methods-download a').is_visible()
   page.close()
  browser.close()
finally:server.shutdown();server.server_close()
(qa/'browser-checks.json').write_text(json.dumps({'chromium':checks,'no_javascript_content':True,'screenshots_reviewed_manually':False},indent=2)+'\n')
print('PASS: A/B Chromium checks, Chinese/English, 1440/390px, light/dark, reduced motion, PDF and companion links, no JavaScript errors or body overflow; both appendices readable without JavaScript.')
