"""Check completeness of the published Chapter 6 PDF against the shared source."""
from pathlib import Path
import argparse,json,re
import fitz
p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);a=p.parse_args()
D=json.loads((Path(__file__).resolve().parents[2]/'chapters/chapter6/action-framework.json').read_text())
doc=fitz.open(a.pdf);normalize=lambda t:re.sub(r'\s+','',t);text=normalize(''.join(p.get_text() for p in doc))
required=[D[k]['zh'] for k in ['intro','position','scope']]
required += [v['zh'] for v in D['synthesis']['paragraphs']]
required += [v['zh'] for f in D['synthesis']['findings'] for v in f['paragraphs']]
required += [D['synthesis'][k]['zh'] for k in ['figure_lead','after']]
required += [v['zh'] for v in D['closing']['paragraphs']]+[D['closing']['final']['zh']]
required += [t['body']['zh'] for t in D['tasks']]
required += [a['intro']['zh'] for a in D['actors']]
for action in D['actions']:
 required += [action[k]['zh'] for k in ['title','why','body']]
 for group,fields in [('steps',['title','body']),('roles',['who','work']),('watch',['label','detail'])]:
  required += [v[k]['zh'] for v in action[group] for k in fields]
missing=[t for t in required if normalize(t) not in text];assert not missing,missing
for i,page in enumerate(doc):
 assert page.rect.width<page.rect.height,(i,'not portrait')
 for b in page.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l['spans']:
    x0,y0,x1,y1=s['bbox'];assert x0>=35 and x1<=page.rect.width-35 and y0>=20 and y1<=page.rect.height-16,(i,s)
    assert s['size']>=8,(i,'undersized text',s)
assert '证据与范围' not in text
assert doc.get_toc(),'missing outline'
print(f'PASS: {len(doc)} portrait pages; {len(required)} shared passages; all steps, roles and follow-up notes; text bounds, minimum type and bookmarks.')
