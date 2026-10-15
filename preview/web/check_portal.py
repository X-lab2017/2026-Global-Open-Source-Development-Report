#!/usr/bin/env python3
"""Check generated links, project subpaths and the approved chapter structure."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import argparse,json
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.ids=[];self.nav=[];self.in_nav=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attributes=dict(attrs);self.tags.append((tag,attributes))
        if 'id' in attributes:self.ids.append(attributes['id'])
        if tag=='nav' and attributes.get('id')=='site-nav':self.in_nav=True
        if self.in_nav and tag=='a':self.nav.append(attributes)
    def handle_endtag(self,tag):
        if tag=='nav':self.in_nav=False
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--base-path',default='')
args=parser.parse_args();root=args.output.resolve();base=args.base_path.rstrip('/')
source=Path(__file__).resolve().parents[1]
pages={file:Page(file.read_text()) for file in root.rglob('*.html')}
errors=[];count=0

def check_url(url,origin):
    global count
    parsed=urlsplit(url)
    if parsed.scheme or parsed.netloc:return
    path=parsed.path
    if path.startswith('/'):
        if base and not path.startswith(base+'/'):
            errors.append(f'{origin}: path escapes the project: {url}');return
        path=path[len(base):] if base else path
        target=root/path.lstrip('/')
    else:target=origin.parent/path if path else origin
    if target.is_dir():target/='index.html'
    count+=1
    if not target.exists():errors.append(f'{origin}: missing {url}')
    elif parsed.fragment and target.suffix=='.html' and unquote(parsed.fragment) not in pages[target].ids:errors.append(f'{origin}: missing anchor {url}')

for file,page in pages.items():
    assert len(page.ids)==len(set(page.ids)),f'Duplicate IDs: {file}'
    assert sum(tag=='h1' for tag,d in page.tags)==1,file
    assert sum(d.get('aria-current')=='page' for d in page.nav)==1,file
    lang='en' if any(tag=='html' and d.get('lang')=='en' for tag,d in page.tags) else 'zh'
    expected=[base+('/en/' if lang=='en' else '/'),base+f'/2026/{lang}/']+[base+f'/2026/{lang}/{r}/' for r in ['data','presentation','film','release']]
    assert [d['href'] for d in page.nav]==expected,file
    for tag,attributes in page.tags:
        link=attributes.get('href') or attributes.get('src')
        if link:check_url(link,file)
    if file in [root/'index.html',root/'en/index.html']:
        questions=[d['href'] for tag,d in page.tags if d.get('class')=='question-link']
        assert questions==[base+f'/2026/{lang}/chapters/{n:02d}/' for n in range(2,7)],questions
m=json.loads((source/'content/manifest.json').read_text())
assert [c.get('label') for c in m['chapters'][1:5]]==['GOSO','GOSR','GOSL','GOSM']
assert len(m['research_questions'])==5
for lang in ['zh','en']:
    for chapter in m['chapters']:
        page=pages[root/'2026'/lang/chapter['route']/'index.html']
        assert sum(d.get('class')=='local-section' for tag,d in page.tags)==len(chapter['sections'])
        if chapter.get('label'):assert chapter['label'] in (root/'2026'/lang/chapter['route']/'index.html').read_text()
for entry in json.loads((root/'assets/search-index.json').read_text()):check_url(entry['url'],root/'index.html')
for name in ['active-developers.csv','osdi-indicators.csv','framework.json']:
    assert (root/'assets'/name).read_bytes()==(source/'content/assets'/name).read_bytes()
assert (root/'content.js').read_bytes()==(source/'content/chart-data.js').read_bytes()
assert len(pages)==51,len(pages)
assert (root/'2026/index.html').read_bytes()==(root/'2026/zh/index.html').read_bytes()
assert not errors,'\n'.join(errors)
print(f'PASS: {len(pages)} pages, {count} internal links/assets, 5 research questions, 4 core labels, unchanged data seeds; base={base or "/"}')
