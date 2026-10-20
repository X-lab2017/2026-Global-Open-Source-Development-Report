"""Guard the publication cleanup boundary and the assembled Chapter 2 edition."""
from pathlib import Path
import argparse,hashlib,json
from goso_reading import Tree,normalize
import vmap_content,cmap_content,goso_maps,amap_content,dmap_content,gmap_content
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--pdf',action='store_true');args=ap.parse_args()
sections=[vmap_content.section('zh'),cmap_content.section('zh'),goso_maps.section('imap','zh'),goso_maps.section('tmap','zh'),amap_content.section('zh'),dmap_content.section('zh'),gmap_content.section('zh')]
# Empty panels and dialogs are live script targets, not redundant editorial text.
count=0
for n,raw in enumerate(sections,1):
 after=Tree(normalize(raw,n,'zh')).root
 for el in Tree(raw).root.walk():
  if el.tag not in ('div','p') or el.children or not el.attrs:continue
  assert any(x.tag==el.tag and all(x.attrs.get(k)==v for k,v in el.attrs.items()) for x in after.walk()),el.attrs
  count+=1
for lang in ['zh','en']:
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text()
 for marker in ['data-vmap-trend','data-cm-comparison-body','data-globe-explanation','id="gm-foundation"','id="dm-sources"']:
  assert marker in html,marker
for c,expected in [('CN',(79.22,14.02,6.76)),('US',(38.28,39.66,22.06))]:
 rows=[r for r in dmap_content.D['sourceShares'] if r['target']==c]
 actual=(next(r['share'] for r in rows if r['source']==c),round(sum(r['share'] for r in rows if r['source'] not in (c,'OTH')),2),next(r['share'] for r in rows if r['source']=='OTH'))
 assert actual==expected
print(f'PASS: {count} live empty containers retained and three source buckets verified')

# Web reading cleanup: one calendar, concise downloads, preserved chart surfaces.
from goso_reading import REPORT_PERIOD, web_window
for lang in ('zh','en'):
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text()
 assert html.count(REPORT_PERIOD)==1
 assert '阅读说明 · 时间、范围与图件' not in html
 assert '评审预览' not in html
 assert 'class="goso-section-nav"' not in html
 for n in range(1,8):
  if web_window(n):assert web_window(n) in html
 assert html.count('下载本节 PDF')==7
print('PASS: one chapter calendar, five explicit exceptions, seven section PDFs, no editorial navigation')

for lang in ('zh','en'):
 html=(args.output/f'2026/{lang}/chapters/02/index.html').read_text()
 assert '<summary>统计范围与指标说明</summary>' not in html
 assert html.count('data-goso-source-notes=')==7
print('PASS: seven section method blocks relocated to on-demand source notes')
