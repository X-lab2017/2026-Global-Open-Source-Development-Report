"""Check pinned data, cohort separation and conclusion-critical derived values."""
from pathlib import Path
import argparse,hashlib,collections,json,sys
sys.path.insert(0,str(Path(__file__).parent))
import landscape_content as L
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=root/'dist');args=parser.parse_args()
for f in L.P['files']:
 p=L.DIR/f['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'];assert (args.output/'assets/landscape'/f['file']).read_bytes()==p.read_bytes()
assert len(L.R['annual'])==69 and len(L.R['canonical'])==279
assert collections.Counter(p['layer'] for p in L.PROJECTS)=={'Agent Infra':86,'Model Infra':59}
assert len({p['id'] for p in L.PROJECTS})==145
assert len({p['section'] for p in L.PROJECTS if p['layer']=='Agent Infra'})==12
assert len(L.UNMATCHED)==3
assert all(p['section'] in L.SECMAP for p in L.PROJECTS)
assert all(p['aug'] is None or p['aug']>=0 for p in L.PROJECTS)
total=sum(float(r['2026']) for r in L.R['subfields']);assert round(total,1)==74919.2
assert round(float(L.R['subfields'][0]['2026'])/total*100,1)==37.6
assert round(sum(float(r['2026']) for r in L.R['subfields'][:4])/total*100,1)==75.0
# A 0.8 difference across rounded tables must not silently rewrite source values.
assert sum(float(r['total_openrank']) for r in L.R['annual'])==74920.0
assert len(L.R['monthly'])==10 and len(L.R['monthly'][0])==13
assert len(L.R['countries'])==36 and len(L.R['scatter'])==12
assert len(L.P['draft_images'])==5
assert next(r for r in L.R['study'] if r['metric']=='agent_participation_present')['point_estimate']=='0.4316'
assert next(r for r in L.R['study'] if r['metric']=='agent_review_event_present')['eligible_threads']=='3567'
print('PASS 4.1: byte-identical pinned assets; annual 69/current 145 cohorts; 66 repo_id matches; 37.6% and 75.0% denominators; source rounding preserved; 10×12 month matrix; 36 country rows; 12 scatter samples; study denominators; 5 draft images.')
