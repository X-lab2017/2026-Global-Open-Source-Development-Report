#!/usr/bin/env python3
"""Extract factual model lineage only; no reference-site source code is reused."""
import csv,hashlib,json,collections,math,pathlib,sys
ROOT=pathlib.Path(__file__).parent
LIVE='--live' in sys.argv
SRC=ROOT/('huggingface-live.json' if LIVE else 'source/visualization/public/data/huggingface.json')
PREFIX='lineage-live' if LIVE else 'lineage'
GRAPH=json.loads(SRC.read_text())
COMMIT='7f69f2fbd27860f1f207be197dfe0597216d7b0d'
BASE='https://github.com/yaoyao-pig/OG-And-HG-2026'
raw_edges=[e for e in GRAPH['edges'] if e.get('kind')=='base-model' and e.get('inferred')==0]
source_ids=sorted({i for e in raw_edges for i in(e['s'],e['t'])})
base_counts=collections.Counter(e['t'] for e in raw_edges)
child_counts=collections.Counter(e['s'] for e in raw_edges)
meta={
 'title':'模型声明的基座—派生关系样本',
 'snapshotAtDeclared':GRAPH['meta']['snapshotAt'],
 'snapshotDateStatus':('Live artifact revision/date matches official upstream Dataset API on 2026-10-17; full sampling not independently reconstructed.' if LIVE else 'Reference artifact declares this date; original upstream revision returns HTTP 404 on 2026-10-17. Not independently reconstructed.'),
 'collectedAt':'2026-10-17',
 'sourceRepository':BASE,
 'sourceCommit':COMMIT,
 'sourceFile':('https://yaoyao-pig.github.io/OG-And-HG-2026/data/huggingface.json' if LIVE else BASE+'/blob/'+COMMIT+'/visualization/public/data/huggingface.json'),
 'sourceFileSHA256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
 'sourceBuildDefinition':BASE+'/blob/'+COMMIT+'/visualization/scripts/build_hf_graph.py#L564-L570',
 'upstreamDataset':GRAPH['meta']['sourceUrl'],
 'upstreamRevisionDeclared':GRAPH['meta']['sourceRevision'],
 'upstreamLicenseDeclared':'apache-2.0',
 'sourceRepositoryLicense':'No LICENSE file found at pinned commit. Presentation code not copied; metadata/relations extracted with provenance.',
 'edgeDirection':'source = base model; target = derived model. Original s=derived,t=base has been reversed.',
 'edgeType':'model-card-declared-base-model',
 'relationSubtypes':'Original export collapses finetune/adapter/other into base-model; no subtype inferred.',
 'countryCoverage':'No publisher-country field in source graph; do not infer from account names.',
 'nodeSizeSuggestion':'Within-sample direct downstream model count; not ModelRank.',
 'layoutSemantics':'x/y preserve the reference graph coordinates. Original layout used observed and inferred relations; positions are navigational, not quantitative.',
 'selection':'All endpoints of base-model edges with inferred=0 from the fixed 24,000-artifact reference graph.',
 'sampling':GRAPH['meta']['provenance']['samples'],
 'excluded':dict(collections.Counter(e['kind'] for e in GRAPH['edges'] if e['kind']!='base-model' or e.get('inferred')!=0)),
 'limitations':['Non-random contiguous 12,000-model input sample, not all Hugging Face models.','Only relationships whose two endpoints are present were retained by upstream.','One edge per unordered node pair was retained by upstream priority rules; parallel relationship types are not preserved.','Descriptions/downloads/likes are source snapshot metadata; neither capability scores nor ModelRank.','Separate from report country-flow snapshot dated 2026-09-13.']
}
def export(ids,selected_edges,out,extra=None):
 ids=sorted(ids); ix={v:k for k,v in enumerate(ids)}
 nodes=[]
 for i in ids:
  n=GRAPH['nodes'][i]
  nodes.append({'id':n['name'],'name':n['name'].split('/',1)[-1],'publisher':n['name'].split('/',1)[0], 'url':n['url'],'task':n.get('areas',{}).get('task',{}).get('primary','unspecified-model'),'library':n.get('areas',{}).get('library',{}).get('primary','model-hub'),'downloads':n.get('downloads'),'likes':n.get('likes'),'x':n['x'],'y':n['y'],'upstreamCount':child_counts[i],'downstreamCount':base_counts[i], 'originalNodeIndex':i,'sourceCommunity':n.get('c')})
 edges=[{'source':GRAPH['nodes'][e['t']]['name'],'target':GRAPH['nodes'][e['s']]['name'],'s':ix[e['t']],'t':ix[e['s']],'type':'declared-base-model','weight':1} for e in selected_edges]
 adj=collections.defaultdict(set)
 for e in edges:adj[e['s']].add(e['t']);adj[e['t']].add(e['s'])
 comps=[];unseen=set(range(len(ids)))
 while unseen:
  todo=[min(unseen)];comp=[];unseen.remove(todo[0])
  while todo:
   i=todo.pop();comp.append(i)
   for j in sorted(adj[i]):
    if j in unseen:unseen.remove(j);todo.append(j)
  comps.append(comp)
 comps.sort(key=lambda a:(-len(a),a[0]))
 m={**meta,'nodeCount':len(nodes),'edgeCount':len(edges),'componentCount':len(comps),'largestComponent':len(comps[0]),**(extra or{})}
 payload={'meta':m,'nodes':nodes,'edges':edges}
 (ROOT/(out+'.json')).write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
 for kind,rows in [('nodes',nodes),('edges',edges)]:
  with (ROOT/(out+'-'+kind+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return payload
full=export(source_ids,raw_edges,PREFIX+'-full')
# A compact multi-base view: twelve most referenced bases plus every observed direct child.
# Tie-breaker is model identifier. Keep all source edges between selected nodes, including multi-base models.
ranked=sorted(base_counts,key=lambda i:(-base_counts[i],GRAPH['nodes'][i]['name']))
top=[]; publishers=set()
for i in ranked:
 publisher=GRAPH['nodes'][i]['name'].split('/',1)[0]
 if not LIVE or publisher not in publishers:
  top.append(i);publishers.add(publisher)
 if len(top)==12:break
subset=set(top)
for e in raw_edges:
 if e['t'] in top:subset.add(e['s'])
es=[e for e in raw_edges if e['s']in subset and e['t']in subset]
sample=export(subset,es,PREFIX+'-overview',{'selection':('Order bases by within-sample direct downstream count, tie-break by model ID; select at most one base per publishing account until twelve accounts are represented. Include all direct children and every source lineage edge between selected nodes.' if LIVE else 'Twelve bases with the most direct downstream models in the reference sample (ties by model ID), all of their direct children, and every source lineage edge between selected nodes.'),'selectedBases':[{'id':GRAPH['nodes'][i]['name'],'downstreamCount':base_counts[i]}for i in top]})
# Conceptual fallback coordinates built from the selected base clusters only; original x/y retained.
# Not a statistical distance. Model assignment chooses the most-referenced selected direct base.
byid={n['id']:n for n in sample['nodes']}; selected_names=[GRAPH['nodes'][i]['name']for i in top]
upstreams=collections.defaultdict(list)
for e in sample['edges']:upstreams[e['target']].append(e['source'])
assign={}
for name in byid:
 candidates=[b for b in selected_names if b==name or b in upstreams[name]]
 assign[name]=candidates[0] if candidates else selected_names[0]
for q,base in enumerate(selected_names):
 cx=220+(q%4)*390;cy=200+(q//4)*360
 members=sorted([n for n,b in assign.items() if b==base and n!=base])
 if base in byid:byid[base].update({'overviewX':cx,'overviewY':cy,'overviewCluster':q,'overviewBase':base})
 for k,name in enumerate(members):
  # Golden-angle spiral keeps dense groups readable without suggesting an order.
  theta=k*math.pi*(3-math.sqrt(5));rad=35+math.sqrt((k+1)/max(1,len(members)))*112
  byid[name].update({'overviewX':round(cx+rad*math.cos(theta),2),'overviewY':round(cy+rad*math.sin(theta),2),'overviewCluster':q,'overviewBase':base})
sample['meta']['overviewLayout']='1600×1120; deterministic direct-base clusters; original x/y retained separately. Display positions are not statistical distances.'
(ROOT/(PREFIX+'-overview.json')).write_text(json.dumps(sample,ensure_ascii=False,separators=(',',':'))+'\n')
(ROOT/(PREFIX+'-provenance.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{x:v['meta'][x]for x in ['nodeCount','edgeCount','componentCount','largestComponent']}for k,v in [('full',full),('overview',sample)]},indent=2))
