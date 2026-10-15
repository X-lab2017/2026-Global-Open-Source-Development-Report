"""Data identity and conclusion-critical contracts for the GOSR preview."""
from pathlib import Path
import argparse,hashlib,json,csv,sys
sys.path.insert(0,str(Path(__file__).parent))
import gosr_content as g
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=root/'dist');args=parser.parse_args()
for f in g.PROV['files']:
 raw=(g.DIR/'data'/f['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['sha256']
 assert (args.output/'assets/gosr/data'/f['file']).read_bytes()==raw
 assert (root/'content/report-assets/data'/f['file']).read_bytes()==raw
for key,field,total in [('regionCountries','entries_in_top100',100),('projectCountries','projects_in_top100',100),('domains','repo_count',30),('languages','repo_count',30),('tasks','models',20),('publishers','models',20),('series','models',18)]:assert sum(float(r[field]) for r in g.DATA[key]['rows'])==total,(key,total)
f=g.DATA['foundationMonth']['rows'];assert [r['month'] for r in f if r['开放原子开源基金会']=='3']==['2025-10','2026-01'];assert all(r['Linux 基金会（含子基金会）']=='1' for r in f)
f=g.DATA['globalMonth']['rows'];assert [r['month'] for r in f if r['华为']=='1']==['2026-03','2026-04','2026-05','2026-06']
f=g.DATA['chinaMonth']['rows'];assert [r['month'] for r in f if r['字节跳动']=='2']==['2026-04','2026-05','2026-06']
f=g.DATA['models']['rows'];assert len([r for r in f if r['publisher']=='Qwen'])==16
assert round(float(g.DATA['company']['rows'][0]['openrank'])-float(g.DATA['company']['rows'][1]['openrank']),2)==25806.61
assert len(g.PROV['images'])==19
print('PASS GOSR: 25 byte-identical datasets; sample denominators; company/foundation monthly changes; model publisher count; 19 preserved originals.')
