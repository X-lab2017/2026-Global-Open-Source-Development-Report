"""Pinned community network and separately published global OpenRank values."""
from pathlib import Path
import json, math, hashlib
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'content/tmap/network-concept.json'
RAW=ROOT/'content/tmap/community-snapshot.json'
SOURCE_CODE='https://github.com/X-lab2017/open-digger/blob/5c2ffc4f5b3dd37ebcb20514c7abfee6853bd830/src/cron/tasks/communityOpenrank.ts'
KINDS={'u':'developer','i':'issue','p':'pull','r':'repo'}
COLORS={'developer':'#bb5475','issue':'#39806a','pull':'#b47717','repo':'#6755a3'}
SHORT={'i1623':'获取 Star 与 Fork 数据','p1616':'补充开发者标签','p1614':'社区贡献查询接口','i1624':'OpenDigger 双周报告','i1617':'申请开源排行榜收录'}
ANCHORS={'u78625977':(172,300),'u8512426':(498,210),'u36896360':(641,67),'u40617667':(440,475),'u178247524':(700,319),'u68376741':(627,452),'u113612424':(320,470),'u68068018':(150,83),'r288431943':(365,239)}
MODES=[
 dict(id='participation',title='参与',chapter='2.1',question='谁参与了共同工作？',insight='8 个账户，通过问题讨论和变更请求参与同一个项目。'),
 dict(id='contribution',title='贡献',chapter='2.2',question='贡献如何在项目中形成？',insight='讨论、提交与评审形成协作关系，社区 OpenRank 沿这些关系识别项目内贡献。'),
 dict(id='influence',title='影响力',chapter='2.4',question='放到更广的网络中看呢？',insight='全域指标来自更广泛的协作网络；当前图中只呈现一个项目内的关系。')]
def positions(nodes,pairs):
 xy={k:list(v) for k,v in ANCHORS.items()};tasks=[n for n in nodes if n['kind'] in ('issue','pull')]
 for k,n in enumerate(tasks):
  users=[e['source'] for e in pairs if e['target']==n['id']];cx=sum(xy[u][0] for u in users)/len(users);cy=sum(xy[u][1] for u in users)/len(users)
  xy[n['id']]=[cx+100*math.cos(k*2.399963),cy+95*math.sin(k*2.399963)]
 for _ in range(300):
  nxt={}
  for n in tasks:
   x,y=xy[n['id']];fx=(375-x)*.001;fy=(275-y)*.001
   for o in nodes:
    if o['id']==n['id']:continue
    dx=x-xy[o['id']][0];dy=y-xy[o['id']][1];d=max(math.hypot(dx,dy),.5);minimum=69 if o['kind']=='developer' else 58 if o['kind']=='repo' else 40
    force=200/d**2+max(0,minimum-d)*.6;fx+=dx/d*force;fy+=dy/d*force
   for e in pairs:
    if e['target']!=n['id']:continue
    dx=xy[e['source']][0]-x;dy=xy[e['source']][1]-y;d=max(math.hypot(dx,dy),.5);f=.025*(d-95);fx+=dx/d*f;fy+=dy/d*f
   nxt[n['id']]=[max(35,min(765,x+max(-4,min(4,fx)))),max(48,min(500,y+max(-4,min(4,fy))))]
  xy.update(nxt)
 return {k:tuple(round(v,2) for v in p) for k,p in xy.items()}
def payload():
 raw=json.loads(RAW.read_text());nodes=[]
 for n in raw['nodes']:
  kind=KINDS[n['id'][0]];label=n['name'] if kind=='developer' else 'OpenDigger' if kind=='repo' else ('I #' if kind=='issue' else 'PR #')+n['id'][1:]
  nodes.append(dict(**n,kind=kind,label=label,short=SHORT.get(n['id'],n['name']),global_value=raw['global_values'].get(n['id'],{}).get('value')))
 pairs=[e for e in raw['links'] if e['source'].startswith('u')];xy=positions(nodes,pairs);by={n['id']:n for n in nodes};repo=next(n for n in nodes if n['kind']=='repo')
 for n in nodes:
  n['x'],n['y']=xy[n['id']];n['neighbors']=[e['target'] if e['source']==n['id'] else e['source'] for e in pairs if n['id'] in (e['source'],e['target'])]
  incoming=[dict(id=e['source'],label=by[e['source']]['label'],value=.85*e['weight']*by[e['source']]['community']) for e in raw['links'] if e['target']==n['id']]
  incoming.sort(key=lambda v:-v['value']);n['components']=incoming+[dict(id='self',label='自身初值与历史',value=.15*n['initial'])]
  if n['kind']!='repo':n['components'].append(dict(id=repo['id'],label='项目背景',value=.85*repo['community']/(len(nodes)-1)))
  else:n['components'].append(dict(id='background',label='协作节点的背景回流',value=.85*.05*sum(o['community'] for o in nodes if o!=n)))
  n['reconstructed']=sum(c['value'] for c in n['components'])
 return dict(version='20261020-community',status='observed_historical_case',label='真实历史案例 · 2024.09',repo=raw['repo'],month=raw['month'],nodes=nodes,links=raw['links'],pairs=pairs,modes=MODES,default_selected='u36896360',colors=COLORS,source_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),sources=[dict(title='OpenDigger 社区网络历史数据',url=raw['source']['url']),dict(title='社区 OpenRank 指定版本源码',url=SOURCE_CODE),dict(title='社区网络交互参考',url='https://codepen.io/frank-zsy/pen/abjMXBV')],method=dict(scope='社区值是项目内贡献，全域值来自独立发布的全域指标；此局部网络不能重新算出全域影响力。',values='保留公开文件数值；未取得的全域值记为缺失，不补零。',decomposition='按指定源码的保留项、关系传播项和项目背景项还原；输入已舍入，分项合计与发布值可能有末位差异。',reference='CodePen 用作网络、排行与来源明细的交互参照；背景项按指定源码的传播系数计算。',top5='此案例不用于判定全域前 5%，也不替代 2.1、2.2 的地域统计。'))
def export(out):
 data=payload();FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');dest=out/'assets/tmap';dest.mkdir(parents=True,exist_ok=True)
 (dest/'network-concept.json').write_text(FILE.read_text());(dest/'network-concept.js').write_text('window.TMAP_NETWORK='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
if __name__=='__main__':FILE.write_text(json.dumps(payload(),ensure_ascii=False,indent=2)+'\n')
