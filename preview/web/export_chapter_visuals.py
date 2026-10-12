#!/usr/bin/env python3
"""Generate editable static SVG counterparts of the four new interactive figures."""
from pathlib import Path
import argparse,csv,html,json,math
from chapter_visuals import DPG,SDG_COLORS,COLORS
E=lambda s:html.escape(str(s))
BG='#f7fafb';INK='#14364b';MUTED='#5d7583';LINE='#d7e2e7';TEAL='#087984'
def text(x,y,s,size=18,fill=INK,weight=400,anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{E(s)}</text>'
def rect(x,y,w,h,fill,stroke='none',sw=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def document(title,body,height):return f'<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="{height}" viewBox="0 0 1160 {height}" role="img"><title>{E(title)}</title><g font-family="Noto Sans SC,Arial,sans-serif">'+rect(0,0,1160,height,BG)+body+'</g></svg>'
def header(kicker,title):return rect(48,38,46,3,TEAL)+text(108,44,kicker,12,MUTED)+text(48,95,title,32,INK,550)
def main(repo):
    target=repo/'figures/chapter1';target.mkdir(parents=True,exist_ok=True)
    raw=repo/'data/raw/2026/external'
    org=json.loads((raw/'lfx-korg/organization-leaderboard.json').read_text());dev=json.loads((raw/'lfx-korg/contributor-leaderboard.json').read_text())
    s=header('GOSD / 1.1 · LINUX','一个内核，连接持续的全球协作')
    for x,num,label in [(48,org['meta']['total'],'组织 · 累计榜单记录'),(588,dev['meta']['total'],'贡献者 · 累计榜单记录')]:s+=rect(x,127,520,100,'#eaf3f4')+text(x+24,180,f'{num:,}',43,TEAL,500)+text(x+205,177,label,18)
    s+=text(48,265,'组织榜单前 10 条记录',16)+text(1110,265,'条形：接口 contributions 值',14,MUTED,anchor='end')
    for i,row in enumerate(org['data'][:10]):
        y=303+i*37;w=row['contributions']/org['data'][0]['contributions']*650
        s+=text(48,y+14,f'{i+1:02d}',11,MUTED)+text(85,y+14,row['name'],15)+rect(340,y,650,18,'#e7eef1')+rect(340,y,w,18,TEAL)+text(1110,y+14,f'{row["contributions"]:,}',14,anchor='end')
    s+=text(48,725,'图 1-1-1 · 来源：LFX Insights korg，仓库固定快照，导出于 2026-10-11。',16)+text(48,757,'累计查询未限定时间范围；不是年度活跃数，也不是 OpenRank。每类原文件各保留前 100 条记录。',14,MUTED)+text(48,786,'在线版可切换组织与贡献者，并选择条形查看接口占比。本图仅作外部背景，不进入 OSDI。',14,MUTED)
    (target/'fig-1-1-1_linux_collaboration.svg').write_text(document('Linux 协作记录',s,820))
    data=json.loads((raw/'atom/fig-03_global-regional-model-adoption.json').read_text());last=data[-1]
    s=header('GOSD / 1.1 · OPEN MODELS','开放的影响，延伸到下一次创造')+text(48,145,'2026.02',15,MUTED)+text(48,234,'70%',82,TEAL,500)+text(260,187,'当月新增微调与衍生模型',20)+text(260,222,'基于中国发布方的基础模型',20)
    for i,(k,label,c) in enumerate([('china','中国',TEAL),('unitedStates','美国','#2d5f9f'),('europe','欧洲','#9674a7')]):s+=rect(753,145+i*36,10,10,c)+text(780,155+i*36,label,17)+text(1096,155+i*36,str(last[k])+'%',19,anchor='end')
    x0=92;plotw=1004;h=285;top=300;bw=plotw/28
    for value in [100,50,0]:
        y=top+h*(1-value/100);s+=rect(x0,y,plotw,1,LINE)+text(74,y+5,str(value)+'%',12,MUTED,anchor='end')
    for i,row in enumerate(data):
        bottom=top+h
        for k,c in [('china',TEAL),('unitedStates','#2d5f9f'),('europe','#9674a7')]:
            rh=row[k]/100*h;bottom-=rh;s+=rect(x0+i*bw+3,bottom,bw-6,rh,c)
    for i,label in [(0,'2023.11'),(2,'2024.01'),(14,'2025.01'),(27,'2026.02')]:s+=text(x0+i*bw+bw/2,615,label,11,MUTED,anchor='middle')
    s+=text(48,665,'图 1-1-2 · ATOM 跟踪的 Hugging Face 样本，按基础模型发布方归属。',16)+text(48,698,'28 个月的月度构成。百分比保留原值；分项之和可能因取整不等于 100%。',14,MUTED)+text(48,728,'不是下载量、下游用户国籍或全球普查。外部背景案例，不进入 OSDI 或正式榜单。',14,MUTED)
    (target/'fig-1-1-2_model_derivatives.svg').write_text(document('开放模型衍生月度构成',s,770))
    s=header('GOSD / 1.1 · PUBLIC VALUE','联合国 SDGs × 数字公共品联盟 DPGA')+text(48,146,'发展目标：朝什么方向改善',18,MUTED)+text(570,146,'数字公共品：哪些条件有据可查',18,MUTED)
    cx,cy=272,383
    def point(rad,deg):return cx+rad*math.cos(math.radians(deg)),cy+rad*math.sin(math.radians(deg))
    for i,c in enumerate(SDG_COLORS):
        a=-90+i*360/17+1;b=-90+(i+1)*360/17-1;x,y=point(199,a);xx,yy=point(199,b);xxx,yyy=point(139,b);xxxx,yyyy=point(139,a);tx,ty=point(168,(a+b)/2)
        s+=f'<path d="M{x} {y} A199 199 0 0 1 {xx} {yy} L{xxx} {yyy} A139 139 0 0 0 {xxxx} {yyyy} Z" fill="{c}"/>'+text(tx,ty+6,str(i+1),17,'#fff',600,'middle')
    s+=text(cx,369,'UN SDGs',35,INK,600,'middle')+text(cx,407,'17 项共同目标',22,MUTED,400,'middle')+text(570,218,'DPGA',46,INK,700)+text(746,212,'Digital Public Goods Alliance',17,MUTED)
    for i,d in enumerate(DPG):
        x=570+i%3*180;y=255+i//3*111;s+=rect(x,y,167,98,'#eef4f6',LINE)+text(x+14,y+27,f'{i+1:02d}',13,TEAL)
        label=d[0]
        for n in range(0,len(label),7):s+=text(x+14,y+54+n//7*23,label[n:n+7],16)
    s+=rect(48,641,1063,64,'#eaf3f4')+text(580,680,'开放软件 · 开放数据 · 开放 AI 系统 · 开放内容',21,INK,400,'middle')+text(48,744,'图 1-1-3 · SDGs 提供目标方向，DPGA 标准提供数字公共品的可审查条件。',16)+text(48,777,'认定需通过标准评审；不将所有开源项目自动视为已获认定的数字公共品。',14,MUTED)+text(48,806,'来源：sdgs.un.org/goals · digitalpublicgoods.net/standard（DPG Standard：CC BY-SA 4.0）',13,MUTED)
    (target/'fig-1-1-3_sdgs_dpga.svg').write_text(document('SDGs 与 DPGA 关系示意',s,846))
    with (repo/'data/meta/osdi_indicator_dictionary.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    s=header('GOSD / 1.3 · OSDI ATLAS','从一个目标，走到一项可查证的指标')+text(48,130,'四个支柱 · 十个维度 · 二十九项指标｜在线版可按角色探索定义、方法和证据',16,MUTED)
    for i in range(4):
        group=[r for r in rows if r['pillar_id']=='X'+str(i+1)];x=48+i%2*548;y=162+i//2*464
        s+=rect(x,y,516,446,'#fff',LINE)+rect(x,y,516,4,COLORS[i])+text(x+20,y+38,'X'+str(i+1),24,COLORS[i],600)+text(x+72,y+36,group[0]['pillar_name_zh'],21,INK,500)
        py=y+61
        for dim in dict.fromkeys(r['dimension_id'] for r in group):
            selected=[r for r in group if r['dimension_id']==dim];s+=text(x+20,py+16,dim+' '+selected[0]['dimension_name_zh'],14,MUTED);py+=28
            for row in selected:
                has=bool(row['related_data_paths']);s+=f'<circle cx="{x+26}" cy="{py+7}" r="3.7" fill="{TEAL if has else "#fff"}" stroke="{TEAL if has else MUTED}"/>'+text(x+41,py+12,row['indicator_name_zh'],15)+text(x+283,py+12,row['indicator_code'],11,MUTED);py+=24
            py+=7
    s+=text(48,1118,'图 1-3-1 · 实心点：有关联资料；空心点：待补匹配数据。资料入库不等于测算完成。',16)+text(48,1150,'来源：统一指标字典；三种指标角色不构成评分权重，ModelRank 本期仍为概念说明。',14,MUTED)
    (target/'fig-1-3-1_osdi_explorer.svg').write_text(document('OSDI 指标地图',s,1190))
    print('Generated four editable SVG counterparts in',target)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-root',type=Path,required=True);a=p.parse_args();main(a.repo_root.resolve())
