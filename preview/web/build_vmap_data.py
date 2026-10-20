"""Rebuild V-Map report-year observations, preserving raw source snapshots."""
from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'preview/content/vmap'
def read(name):return json.loads((P/name).read_text())
def write(name,data):(P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
d=read('fig-2-1-2_platform-coverage.json');oldprovinces=d['provinces'];world=read('source/report-developers.json');china=read('source/report-CN-developers.json');meta=read('source/data-meta.json')
def merge(source,province=False):
 out={};ids={r['en']:r['id'] for r in oldprovinces}
 for board,key,change in zip(source['leaderboards'],['total','active'],['total_increase','increase']):
  for r in board['data']:
   code=ids[r['name']] if province else r['code']
   row=out.setdefault(code,dict(id=code,name=r['name_zh'],en=r['name'],total=None,active=None,increase=None,total_increase=None))
   row[key]=r['value']/10000;row[change]=r['change']/10000 if r.get('change') is not None else None
 return sorted(out.values(),key=lambda r:-(r['active'] if r['active'] is not None else -1))
d['countries']=merge(world);d['provinces']=merge(china,True);by={r['id']:r for r in d['countries']}
d['observation_period']=dict(start='2025-07-01',end_exclusive='2026-07-01',time_dimension='report_year',report_year=2026,label='2025 年 7 月 1 日至 2026 年 6 月 30 日')
d['comparison_period']=dict(start='2024-07-01',end_exclusive='2025-07-01',label='2025报告年度')
d['scope']='GitHub · 2026报告年度';d['source']=d['report_period_source'];d['source_updated_at']=meta['summary']['updatedAt']
d['snapshot_trends']=world['trends'];d['global_total']=world['trends'][0]['values'][-1]/10000;d['global_active']=world['trends'][1]['values'][-1]/10000
attribution='报告编制组根据国内 Gitee、AtomGit 等官方平台数据，结合问卷调研去重得到。'
d['domestic'].update(cross_github_deduplicated=True,status='编制组确认的国内平台补充统计',source=attribution,confirmed_on='2026-10-20',period=d['observation_period'])
for field in ['total','active','increase']:d['groups']['SOUTH6'][field]=sum(by[k][field] for k in d['groups']['SOUTH6']['members'])
d['group_notes']={'EU':'五域原稿汇总，已由编制组确认并与原稿图交叉核对。','SOUTH':'五域原稿的全球南方代表组；五域不构成全球穷尽划分。','SOUTH6':'GitHub 底表中的巴西、印度尼西亚、越南、菲律宾、埃及、南非合计，保留为额外观察组。'}
total=list(csv.DictReader((ROOT/'data/processed/chapter2/fig-2-1-2_five_region_total_developers.csv').open()))
history=list(csv.DictReader((ROOT/'data/processed/chapter2/fig-2-1-3_five_region_active_developers_trend.csv').open()))
codes=['US','EU','CN','IN','SOUTH'];d['five_groups']=codes;d['five_group_records']=[dict(id=code,name='全球南方代表组' if code=='SOUTH' else r['region_zh'],total=int(r['developers'])/10000,active=float(history[-1][r['region']])/10000) for code,r in zip(codes,total)]
d['trend'].update(status='编制组确认 · 2022—2026报告年度',warning='',period_convention='标注年份为报告年度：前一年7月1日至当年6月30日。')
d['five_group_source']=dict(total='data/processed/chapter2/fig-2-1-2_five_region_total_developers.csv',active='data/processed/chapter2/fig-2-1-3_five_region_active_developers_trend.csv',confirmation='2026-10-20 编制组确认并提供原稿两图交叉核对',scope='原稿五域综合统计；与 GitHub 地图分别注明来源，不重复叠加国内补充量。')
d['province_source']=dict(source='https://selfoss.open-digger.cn/openshare/overview_half_year/CN/developers.json',national_active=by['CN']['active'],province_coverage='34个省级地区',increase_period='2025报告年度',description='沿用 OpenShare 报告年度省级分布；开发者总量为平台估计。')
for name in ['report-developers.json','report-CN-developers.json']:
 d['source_registry'][name]=dict(url='https://selfoss.open-digger.cn/openshare/overview_half_year/'+('CN/' if 'CN-' in name else '')+'developers.json',sha256=hashlib.sha256((P/'source'/name).read_bytes()).hexdigest(),role='当前报告年度地图、排名与趋势数据')
for name,v in d['source_registry'].items():
 if name.startswith('calendar-'):v['role']='历史自然年快照，仅归档，不用于当前2.1图件'
d['source_registry']['report-CN-developers-reference.json']['role']='同一报告年度省级源文件的早期留存，与本次下载逐字节一致'
for name,v in d['images'].items():v['status']='历史截图参考；当前版以报告年度底表为准'
d['source_checks'].update(matching_screenshot='原稿五域两图与仓库总量、历史序列交叉核对',world_active_region_sum=sum(r['active'] or 0 for r in d['countries']))
d['source_checks']['world_active_difference']=d['global_active']-d['source_checks']['world_active_region_sum']
write('fig-2-1-2_platform-coverage.json',d)
with (P/'fig-2-1-2_platform-coverage.csv').open('w') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['country_code','country_zh','github_total_10k','github_active_10k','displayed_increase_10k','domestic_active_approx_10k','cross_github_overlap_status','observation_period'])
 for r in d['countries']:w.writerow([r['id'],r['name'],r['total'],r['active'],r['increase'],120 if r['id']=='CN' else '', 'deduplicated' if r['id']=='CN' else 'not_applicable','2025-07-01 / 2026-07-01 (exclusive)'])
with (P/'fig-2-1-3_china-provinces.csv').open('w') as f:
 keys=['id','name','total','active','increase','total_increase'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(d['provinces'])
print('Report-year rows:',len(d['countries']),len(d['provinces']),'China',by['CN']['active'])
rr=d['provinces'];print('China shares',[sum(r['active'] for r in group)/by['CN']['active']*100 for group in [rr[:3],rr[3:10],rr[10:]]]);print('South samples',[(k,by[k]['active']) for k in ['IN','BR','ID']]);print('South share',sum(by[k]['active'] for k in ['IN','BR','ID'])/d['global_active']*100)
