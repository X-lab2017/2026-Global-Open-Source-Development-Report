"""A small reproducible teaching network, never an observed OpenRank ranking."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'content/tmap/network-concept.json'
NODES=[
 {'id':'A','kind':'developer','name':'开发者 A','x':170,'y':102},
 {'id':'B','kind':'developer','name':'开发者 B','x':648,'y':118},
 {'id':'C','kind':'developer','name':'开发者 C','x':75,'y':270},
 {'id':'D','kind':'developer','name':'开发者 D','x':275,'y':398},
 {'id':'E','kind':'developer','name':'开发者 E','x':395,'y':66},
 {'id':'F','kind':'developer','name':'开发者 F','x':694,'y':367},
 {'id':'P1','kind':'project','name':'基础库','x':256,'y':224},
 {'id':'P2','kind':'project','name':'开发工具','x':548,'y':280},
 {'id':'P3','kind':'project','name':'应用项目','x':465,'y':440},
]
EDGES=[('A','P1',6),('A','P3',2),('B','P2',6),('B','P3',2),('C','P1',2),('D','P1',1),('E','P1',1),('E','P3',1),('F','P2',12)]
CHECKPOINTS=[0,1,2,4,8,16,32,120]
MODES=[
 {'id':'participation','title':'参与','chapter':'2.1','question':'谁在参与？','legend':'圆：开发者；方：项目。圆大小相同，每位活跃开发者计 1 人。','insight':'6 位开发者都在参与，人数不区分投入多少。','unit':'人'},
 {'id':'contribution','title':'贡献','chapter':'2.2','question':'各自投入了多少？','legend':'线越粗、节点越大，示意贡献强度越高。','insight':'F 的贡献强度最高；A 与 B 的贡献强度同为 8。','unit':'示意值'},
 {'id':'influence','title':'影响力','chapter':'2.4','question':'这些连接形成怎样的影响？','legend':'影响沿协作关系传播，节点越大，示意影响值越高。','insight':'A 与 B 贡献相同，网络影响不同；影响还取决于协作对象及其连接。','unit':'%'}
]

def scenario(rewire=False):
 edges=[dict(source=a,target='P1' if rewire and a=='B' and b=='P2' else b,weight=w) for a,b,w in EDGES]
 ids=[n['id'] for n in NODES];adj=[[0.0]*9 for _ in ids]
 for e in edges:
  i,j=ids.index(e['source']),ids.index(e['target']);adj[i][j]+=e['weight'];adj[j][i]+=e['weight']
 totals=[sum(row) for row in adj];seed=[1/6 if i<6 else 0 for i in range(9)];r=seed[:];all_steps=[r]
 for _ in range(CHECKPOINTS[-1]):
  r=[.15*seed[j]+.85*sum(r[i]*adj[i][j]/totals[i] for i in range(9)) for j in range(9)];all_steps.append(r)
 shares=[x/sum(r[:6])*100 for x in r[:6]]
 return dict(edges=edges,totals=totals,steps=[all_steps[k] for k in CHECKPOINTS],developer_shares=shares,delta_last=max(abs(a-b) for a,b in zip(all_steps[-1],all_steps[-2])))

def payload():
 return dict(version='20261020-network',status='teaching_simulation',label='教学模拟 · 非真实排名',nodes=NODES,modes=MODES,checkpoints=CHECKPOINTS,scenarios={'base':scenario(),'rewired':scenario(True)},method={'name':'简化加权传播示意','damping':.85,'seed':'六位开发者均分起始值，项目起始值为零。','transition':'双向协作边按各节点出边权重归一；每轮 15% 回到开发者初值，85% 沿关系传播。','contribution':'连线权重为人工设定的示意贡献强度，不等于提交次数，也不是社区 OpenRank 的计算结果。','influence':'开发者份额由开发者节点传播值归一；仅用于同一示意网络内比较。','scope':'本图借鉴 PageRank 的递归传播思想解释网络影响，不复现正式 OpenRank。正式评价还包括活跃增值、历史继承等机制。'},sources=[{'title':'全域 OpenRank 影响力','url':'https://open-digger.cn/docs/user-docs/metrics/global-openrank'},{'title':'OpenRank 开源评价系列算法介绍','url':'https://open-digger.cn/blog/2025-08-09-openrank-introduction'}])

def export(out):
 data=payload();FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');dest=out/'assets/tmap';dest.mkdir(parents=True,exist_ok=True)
 (dest/'network-concept.json').write_text(FILE.read_text());(dest/'network-concept.js').write_text('window.TMAP_NETWORK='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')

if __name__=='__main__':
 FILE.write_text(json.dumps(payload(),ensure_ascii=False,indent=2)+'\n')
