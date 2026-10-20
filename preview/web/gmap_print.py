"""Vector print composition of G-Map; preserves observations and simulation labels."""
from pathlib import Path
import argparse,json,hashlib,shutil
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak
import chapter1_print as common
import vmap_print as vp
import gmap_publication as p
D=p.D;M=D['simulation'];W=vp.PWIDTH;INK,MUTED,TEAL,LINE=vp.INK,vp.MUTED,vp.TEAL,vp.LINE
COL=['#156993','#279FA9','#9973B7','#886400']
def figure(i,h=450):return vp.Figure(p.FIGURES[i-1][2],f'图 2-7-{i}',height=h)
def tag(f,label='模拟数据｜待替换'):
 f.rect(0,0,160,21,'#FFF4CF','#D8B74A',.5);f.text(8,14,label,10,'#755600')
def line(f,x,y,w,h,rows,keys,labels,unit):
 f.text(x,y,unit,8.5,MUTED);L=x+34;R=x+w-7;T=y+17;B=y+h-21;maxv=max(r[k] for r in rows for k in keys)*1.12
 for j in range(3):
  v=maxv*j/2;yy=B-(B-T)*j/2;f.line([(L,yy),(R,yy)],LINE,.4);f.text(L-4,yy+3,f'{v:.1f}' if maxv<10 else f'{v:,.0f}',8.5,MUTED,'right')
 for i,k in enumerate(keys):
  pts=[(L+j*(R-L)/(len(rows)-1),B-r[k]/maxv*(B-T)) for j,r in enumerate(rows)];f.line(pts,COL[i%4],1.3)
  for xx,yy in pts:f.dot(xx,yy,1.6,COL[i%4])
 for j,r in enumerate(rows):f.text(L+j*(R-L)/(len(rows)-1),B+14,str(r.get('year',r.get('period',''))),8.5,MUTED,'center')
 for j,t in enumerate(labels):f.text(x+j*w/max(1,len(labels)),y+h+5,t,8.5,COL[j%4])
def table(f,x,y,width,heads,rows,rowh=24):
 widths=[width/len(heads)]*len(heads)
 for j,t in enumerate(heads):f.text(x+sum(widths[:j])+5,y,t,8.5,MUTED)
 for i,row in enumerate(rows):
  yy=y+rowh*(i+1);f.line([(x,yy+6),(x+width,yy+6)],LINE,.4)
  for j,t in enumerate(row):f.text(x+sum(widths[:j])+5,yy,str(t),8.5,INK)
def world():
 f=figure(1,330);tag(f);f.text(W,14,'三类地域关系分别计量',9,MUTED,'right');sc=305/880
 for g in D['world']:f.path(g['d'],0,37,sc,None if g.get('kind')=='line' else '#E6E8EA','#91AAB9',.4)
 for r in M['map']['records']:
  g=next(g for g in D['world'] if g['id']==r['id']);f.dot(g['center'][0]*sc,37+g['center'][1]*sc,2+r['values'][0]**.5,COL[0])
 f.text(0,220,'地图点面积：治理支持组织条目（模拟）',8.5,MUTED)
 table(f,312,45,W-312,['地区','组织','维护','部署'],[[r['name'],*r['values']] for r in M['map']['records']],18)
 for i,(t,d) in enumerate([('组织登记地','观察谁提供规则与资源'),('维护者所在地','观察谁承担持续维护'),('公共应用所在地','观察技术在哪里使用')]):
  x=i*171;f.text(x,260,t,10,COL[i]);f.text(x,279,d,8.5,MUTED)
 f.text(0,302,'地区数值全部模拟；无数据地区不表示没有活动，三层不能相加。',8.5,MUTED);return f.caption()
def governance():
 f=figure(2,465);f.text(0,14,'2022—2026 报告年度 · 来源：报告编制组原表',9,MUTED)
 rows=D['series']['foundation'];line(f,0,42,245,105,rows,['active_repositories'],['基金会活跃仓库'],'个');line(f,263,42,240,105,rows,['foundation_project_openrank_share_pct'],['基金会项目 OpenRank 份额'],'%')
 rows=D['series']['licenses'];line(f,0,190,245,105,rows,['MIT','Apache-2.0'],['MIT','Apache-2.0'],'活跃仓库 / 个');line(f,263,190,240,105,rows,['BSD-3-Clause','GPL-3.0','AGPL-3.0'],['BSD-3','GPL-3','AGPL-3'],'活跃仓库 / 个')
 rows=D['series']['mulan'];line(f,0,337,245,88,rows,['cumulative_active_repositories'],['木兰：累计活跃仓库'],'个');line(f,263,337,240,88,rows,['project_openrank_influence'],['木兰：项目 OpenRank'],'影响力')
 f.text(0,447,'各指标独立纵轴；许可数量不能推算全局覆盖率，累计不等同于当年活跃。',8.5,MUTED);return f.caption()
def gov_continued():
 f=vp.Figure('治理实践与角色参与（模拟）','图 2-7-2',height=420);tag(f)
 cols=['项目','决策','晋升','冲突','申诉','安全','交接'];labels=['未发现','有记录','待核验'];table(f,0,47,W,cols,[[chr(65+i)]+[labels[v] for v in row] for i,row in enumerate(M['governance'])],28)
 f.text(0,195,'虚构项目 K · 各治理角色的机构关联',10,INK);R=M['roles']
 for i,name in enumerate(R['roles']):
  yy=224+i*29;f.text(0,yy,name,9,INK);total=sum(R['counts'][i]);x=95
  for j,v in enumerate(R['counts'][i]):
   width=320*v/total;f.rect(x,yy-11,width,17,COL[j],COL[j],0);f.text(x+width/2,yy+1,f'{v/total*100:.0f}%',8.5,'#FFFFFF','center');x+=width
  f.text(W,yy,str(total)+' 条',8.5,MUTED,'right')
 for j,n in enumerate(R['actors']):f.text(j*170,373,n,9,COL[j])
 f.text(0,395,'角色记录可重叠，不跨行加总人数；有公开记录不等于已核实执行。',8.5,MUTED);return f.caption(continued=True)
def support():
 f=figure(3,470);tag(f);q=M['support'];L=33;R=260;T=58;B=235
 f.text(0,42,'A  依赖与支持 · 点大小为维护者数',9,INK)
 for v in [0,12,24]:
  yy=B-v/30*(B-T);f.line([(L,yy),(R,yy)],LINE,.4);f.text(L-5,yy+3,str(v),8.5,MUTED,'right')
 for v in [0,600,1200]:f.text(L+v/1400*(R-L),252,str(v),8.5,MUTED,'center')
 yy=B-12/30*(B-T);f.line([(L,yy),(R,yy)],COL[3],.8,[3,2])
 for i,n in enumerate(q['project']):
  x=L+q['downstream'][i]/1400*(R-L);y=B-q['funding_months'][i]/30*(B-T);f.dot(x,y,2+q['maintainers'][i]**.5,COL[1]);f.text(x+6,y+3,n,8.5,INK)
 f.text(0,269,'纵轴：资金月数；横轴：下游项目数',8.5,MUTED)
 f.text(286,42,'B  评审与积压 · 虚构项目 K',9,INK);z=M['workload'];rows=[{'period':str(i+1)+'季','opened':z['opened'][i],'reviewed':z['reviewed'][i],'backlog':z['backlog'][i]} for i in range(4)];line(f,280,62,223,170,rows,['opened','reviewed','backlog'],['新进入','获评审','未结'],'PR 条目')
 f.text(0,300,'C  已确认现金支持结构（%）',9,INK);F=M['funding'];table(f,0,321,260,['项目','企业','公共','基金会','社区'],[[n,*F['mix'][i]] for i,n in enumerate(F['projects'])],23)
 f.text(286,300,'D  关键岗位接续',9,INK);z=M['succession'];table(f,282,321,221,['角色','主责','替补'],[[n,z['primary'][i],z['backup'][i]] for i,n in enumerate(z['roles'])],23)
 f.text(0,449,'全部模拟；12 个月仅为讨论参考线。获评审不等于结案，岗位人数不跨行相加。',8.5,MUTED);return f.caption()
def public():
 f=figure(4,460);tag(f);P=M['public'];f.text(0,43,'A  公共目标、部署与结果评价 · 嵌套证据层',10,INK)
 for i,name in enumerate(P['fields']):
  y=67+i*27;f.text(0,y+8,name,9,INK)
  for j,v in enumerate(P['counts'][i]):f.rect(95,y-8+j*7,v/30*295,5,COL[j],COL[j],0);f.text(100+v/30*295,y-3+j*7,str(v),8.5,MUTED)
 for i,t in enumerate(['目标声明','具体部署','结果评价']):f.text(i*167,290,t,9,COL[i])
 f.text(0,318,'B  模拟部署前后变化 · 不证明因果',10,INK)
 for i,row in enumerate(P['outcomes']):
  x=i*260;f.text(x,342,row['name'],9,INK);f.text(x,365,row['metric']+'：'+str(row['before'])+' → '+str(row['after'])+' '+row['unit'],10,COL[0]);f.text(x,385,'样本 '+str(row['n'])+' · '+row['period'],8.5,MUTED)
 f.text(0,415,'本地共建：需求提出 → 适配部署 → 培训运维 → 反馈上游',9,INK);f.text(0,438,'全部模拟；三层证据不能相加，DPG 认可不替代本地结果评价。',8.5,MUTED);return f.caption()
def ai():
 f=figure(5,465);tag(f);A=M['ai'];f.text(0,43,'A  跨资产责任检查 · 每项适用且完成检查数为 100',10,INK)
 table(f,0,66,W,['检查项','代码（%）','模型（%）','数据（%）'],[[name,*[row[i] for row in A['coverage']]] for i,name in enumerate(A['checks'])],22)
 f.text(0,230,'B  贡献与人工评审 · 条目数',10,INK);z=A['review'];table(f,0,251,W,['披露分组','提交','人工评审','合并'],[[n,z['submitted'][i],z['human_reviewed'][i],z['merged'][i]] for i,n in enumerate(z['groups'])],23)
 f.text(0,346,'C  Agent 权限示例 · 0 未授予 / 1 限定授权 / 2 人工批准',9,INK);z=A['permissions'];table(f,0,369,W,['角色',*z['scopes']],[[n,*z['states'][i]] for i,n in enumerate(z['actors'])],20)
 f.text(0,446,'全部模拟；检查项分别呈现，不合成总分；未检查规模未设定。',8.5,MUTED);return f.caption()
class Doc(vp.Doc):
 def frame(self,c,doc):
  w,h=c._pagesize;c.saveState();c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0);c.setFont(common.FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告');c.drawRightString(w-46,h-37,'第二章 全球开源生态观测地图');c.setStrokeColor(HexColor(LINE));c.line(46,43,w-46,43);c.setFont(common.FONT,8.2);c.drawString(46,28,'2.7 全球开源治理与社会公益地图');c.drawRightString(w-46,28,str(doc.page));c.restoreState()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',type=Path,required=True);args=ap.parse_args();work=p.ROOT.parent/'tmp/pdfs/gmap';work.mkdir(parents=True,exist_ok=True);out=p.ROOT.parent/'output/pdf'/p.PDF_NAME;out.parent.mkdir(parents=True,exist_ok=True);dest=p.BASE/'print';dest.mkdir(parents=True,exist_ok=True)
 common.font_setup(args.font,work,subset_text=Path(__file__).read_text()+p.manuscript()+json.dumps(D,ensure_ascii=False))
 figs=[world(),governance(),support(),public(),ai()];extra=gov_continued()
 for i,f in enumerate(figs,1):(dest/f'fig-2-7-{i}.svg').write_text(f.svg())
 (dest/'fig-2-7-2-continued.svg').write_text(extra.svg())
 body=ParagraphStyle('body',fontName=common.FONT,fontSize=11.2,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
 styles={'h':ParagraphStyle('h',parent=body,fontSize=16,leading=24,spaceAfter=14,keepWithNext=True),'s':ParagraphStyle('s',parent=body,fontSize=12.5,leading=21,spaceBefore=10,spaceAfter=10,textColor=HexColor(TEAL),keepWithNext=True),'note':ParagraphStyle('n',parent=body,fontSize=9.5,leading=15,spaceAfter=8)};story=[]
 def para(t,sty='body'):story.append(common.paragraph(t,styles.get(sty,body)))
 def lead(i):para(p.STORIES[i][0],'s');para(p.STORIES[i][1][0])
 def after(i):a,b=p.STORIES[i][1][1].split('。',1);para('**'+a+'。**'+b)
 para('2.7 '+p.TITLE,'h');para(p.INTRO);para('研究问题：'+p.QUESTION);para('指标定位：'+p.POSITION,'note');para('核心发现：'+p.FINDING);para(p.WINDOW,'note');lead(0);story.extend([vp.FigureFlow(figs[0],'2-7-1'),PageBreak()]);after(0);lead(1);story.extend([vp.FigureFlow(figs[1],'2-7-2'),PageBreak()]);after(1);story.extend([vp.FigureFlow(extra,'2-7-2-continued'),PageBreak()])
 for i in [2,3,4]:lead(i);story.append(vp.FigureFlow(figs[i],f'2-7-{i+1}'));after(i);story.append(PageBreak())
 para(p.ACTION_TITLE,'s')
 for title,ps in p.STRATEGIES:para(title,'s');[para(t) for t in ps]
 para('统计范围与指标说明','s');[para(t,'note') for t in p.NOTES];para(p.BRIDGE)
 doc=Doc(out);doc.build(story);shutil.copy2(out,dest/p.PDF_NAME);(p.BASE/'chapter-2-7.md').write_text(p.manuscript())
 spec={'edition':p.EDITION,'pages':doc.page,'figure_pages':doc.figures,'pdf':p.PDF_NAME,'release_pdf':p.PDF_RELEASE_NAME,'data_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [p.BASE/'data.js',p.BASE/'simulation.json',*p.BASE.glob('*.csv')]},'manuscript_sha256':hashlib.sha256(p.manuscript().encode()).hexdigest(),'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'verification':{'pdf_render':'seven portrait pages visually checked','browser_pixels':'not_run','physical_print':'not_run'}}
 (dest/'publication-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'pages':doc.page,'figures':doc.figures},ensure_ascii=False))
if __name__=='__main__':main()
