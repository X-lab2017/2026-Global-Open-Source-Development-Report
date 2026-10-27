"""Private opening + Chapter 1 review. Does not change the public portal.

One content/layout model feeds the offline web deck and editable native slides.
Run: python3 preview/presentation-review/build_review.py --output PATH
"""
import argparse, ast, base64, csv, html, json, re, unicodedata
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BG='#091B2B'; FG='#F4F8FC'; MUTED='#AABCCB'; TEAL='#66D5CA'; BLUE='#72B6F2'; GOLD='#EFC77B'; PURPLE='#B7A5ED'; PANEL='#102C40'; LINE='#315064'
COLORS=[TEAL,BLUE,GOLD,PURPLE]
SOURCES={
 'summary':ROOT/'outline/执行摘要.md',
 'intro':ROOT/'chapters/引言-人工智能时代的开源发展.md',
 'chapter':ROOT/'chapters/chapter1/本章介绍.md',
 'value':ROOT/'chapters/chapter1/1.1-开源-数字公共品与可持续发展引擎.md',
 'goals':ROOT/'chapters/chapter1/1.2-OSDGs-开源发展目标框架.md',
 'methods':ROOT/'chapters/chapter1/1.3-OSDI-开源发展度量体系.md',
 'contents':ROOT/'outline/目录.md',
}
STORY=json.loads((ROOT/'preview/content/story-data.json').read_text())
SUMMARY=json.loads((ROOT/'outline/executive-summary.json').read_text())
IND=list(csv.DictReader((ROOT/'data/meta/osdi_indicator_dictionary.csv').open()))
FRAME=json.loads((ROOT/'preview/content/assets/framework.json').read_text())
THEMES=next(ast.literal_eval(n.value) for n in ast.parse((ROOT/'preview/web/chapter1_theme_map.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MAPS' for t in n.targets))
FIGS={p.stem:p.read_text() for p in (ROOT/'figures/chapter1').glob('*.svg') if not p.stem.endswith('.editable')}
SLIDES=[]

def wrap(t,w,size):
    capacity=w/size; lines=[]
    for par in t.split('\n'):
        line=''; used=0
        for char in par:
            n=1 if unicodedata.east_asian_width(char) in 'WF' else .55
            if used+n>capacity and line and char not in '，。、；：？！）】》”’%':
                lines.append(line);line='';used=0
            line+=char;used+=n
        lines.append(line)
    return '\n'.join(lines)

def box(s,x,y,w,h,fill=PANEL,stroke=None,r=0,**extra):
    s['elements'].append(dict(type='shape',x=x,y=y,w=w,h=h,fill=fill,stroke=stroke,r=r,**extra))

def text(s,t,x,y,w,h,size=26,color=FG,bold=False,align='left',**extra):
    s['elements'].append(dict(type='text',text=wrap(t,w,size),x=x,y=y,w=w,h=h,size=size,color=color,bold=bold,align=align,**extra))

def line(s,x,y,w,h=0,color=LINE,width=2,**extra):
    s['elements'].append(dict(type='line',x=x,y=y,w=w,h=h,color=color,width=width,**extra))

def new(id,title,part,claim,source='chapter',note='',figure=None):
    s=dict(id=id,title=title,part=part,claim=claim,source=source,note=note,figure=figure,elements=[])
    SLIDES.append(s)
    text(s,'GOSD  /  2026',52,30,350,25,18,TEAL,True)
    text(s,part,710,30,518,25,18,MUTED,False,'right')
    text(s,title,52,93,1176,78,42,FG,True)
    text(s,claim,54,176,1172,64,24,MUTED)
    line(s,54,652,1172)
    text(s,note or '2026 全球开源发展报告 · '+part,54,668,1064,36,15,MUTED)
    text(s,f'{len(SLIDES):02}',1140,669,86,24,17,TEAL,True,'right')
    return s

def cards(s,items,y=280,h=320,colors=None):
    gap=24;w=(1172-gap*(len(items)-1))/len(items)
    for i,(title,body) in enumerate(items):
        x=54+i*(w+gap);color=(colors or COLORS)[i%4]
        line(s,x,y,w,color=color,width=4)
        text(s,title,x,y+24,w,h/3,29,color,True)
        text(s,body,x,y+112,w,h-112,24)

def dimension(s,title,sub,items,color=TEAL):
    text(s,title,54,275,370,86,36,color,True)
    text(s,sub,54,390,340,196,25)
    for i,(a,b) in enumerate(items):
        y=273+i*(345/len(items))
        line(s,460,y,766,color=LINE)
        text(s,a,460,y+16,284,60,27,color,True)
        text(s,b,770,y+16,456,96,23)

def chart(s,kind,x,y,w,h,categories,series,max_value=100):
    s['elements'].append(dict(type='chart',kind=kind,x=x,y=y,w=w,h=h,categories=categories,series=series,max=max_value))

def main(out):
    s=new('cover','', '汇报演示 · 封面至第一章', '', 'contents', '中国科协联合国咨商开源创新专委会')
    text(s,'2026',54,113,700,90,78,TEAL,True)
    text(s,'全球开源\n发展报告',54,218,720,184,68,FG,True)
    text(s,'Global Open Source Development Report',58,425,740,42,25,MUTED)
    text(s,'从普惠到质量，从参与到影响',58,507,750,52,33,FG,True)
    text(s,'持续共同创造及其公共价值',58,575,750,35,24,TEAL)
    s['elements'].append(dict(type='asset',name='disc',x=864,y=220,w=328,h=328))

    s=new('overview','六章，一条清晰的阅读路径','全书概览','建立基础，展开观察，再把证据带回行动。','contents', '本次演示展开封面、前置内容与第一章；后续章节仅保留全书定位。','fig-1-0-1_report_logic')
    chapters=[('01','价值与方法','从开放协作到公共价值'),('02','生态地图','参与、贡献与全球联系'),('03','影响力榜单','地区、组织与项目'),('04','技术全景','技术分类与演进'),('05','模型生态','供给、复用与开放'),('06','共同任务与行动','主体责任与持续反馈')]
    for i,(n,a,b) in enumerate(chapters):
        x=54+(i%3)*398;y=272+(i//3)*149
        text(s,n,x,y,70,60,43,COLORS[0 if i==0 else 1 if i<5 else 3],True)
        text(s,a,x+83,y+2,290,42,27,FG,True);text(s,b,x+83,y+52,290,66,21,MUTED)
    text(s,'附录 A  指标与统计方法     /     附录 B  模型开放条件、数字公共品认可与公共用途',54,590,1170,40,22,MUTED)

    s=new('summary-participation','把参与基础，连接到持续贡献','执行摘要 · 主要发现 01—02','人数与影响力分别观察，支持也要延伸到维护责任。','summary')
    cards(s,[('参与 ≠ 影响','开发者基础提供发展条件。\n真实任务、成长机会与组织支持，帮助参与转化为持续贡献。'),('协作需要共同维护','企业连接研发与实践，基金会和社区承接跨组织协作，维护者让成果持续可用。'),('从榜单继续追问','哪些基础被反复使用？\n谁承担维护？\n使用者怎样回馈上游？')])

    s=new('summary-tech','AI 开源建设，扩展到完整技术体系','执行摘要 · 主要发现 03','应用创新依赖可复用的共同基础。','summary','摘要引用第四章研究定位；4.2—4.6 当前提供全景与框架，进一步分析待补。')
    cards(s,[('应用与任务','任务入口、智能体编排、工具和记忆，连接真实场景与技术供给。'),('模型与运行基础','训练、推理、评估与运行基础，承载上层开发和持续迭代。'),('共同建设方向','支持基础工具、互操作与公开评测，同时识别长期维护需求。')])

    s=new('summary-models','供给、复用与开放，各自需要证据','执行摘要 · 主要发现 04—05','增长展示积累；材料与许可决定后续使用的条件。','summary','三组证据分别解释：2026.09 同一可见快照回溯 / 826 个组织地域样本 / 870 个评估样本。')
    for i,(n,title,body) in enumerate([
        ('58.3%','可见模型数量增长','较上年同日；派生模型增长 52.3%。\n按同一快照内创建时间回溯。'),
        ('71.7%','中美模型数量合计份额','826 个组织账号的地域样本。\n不代表全球完整存量。'),
        ('13.4%','同时高完整与高开放','117 / 870 个评估样本。\n高开放组共 600 个。')]):
        x=54+i*399;text(s,n,x,283,375,92,64,COLORS[i],True);text(s,title,x,398,375,48,27,FG,True);text(s,body,x,469,366,130,23,MUTED)

    s=new('summary-tasks','三项共同任务，推动发展质量提升','执行摘要 · 行动方向','持续共同创造，需要人才、技术基础与治理共同支撑。','summary')
    cards(s,[('支持持续参与\n与人才成长','从首次贡献到持续贡献，再到共同维护，提供时间、认可与接续支持。'),('建设可维护、可复用\n的开放技术基础','把支持延伸到文档、测试、适配、问题响应和长期维护。'),('推进透明治理\n与可验证的公共价值','明确材料、许可和责任，以实际采用、受益范围与后续维护检验成果。')],y=267,h=350)

    s=new('declaration-vision','开源共创智能未来','引言 · 共同愿景','以《全球开源与人工智能国际合作宣言》为思想起点。','intro','本页为宣言导读；完整原文可在“正文与来源”中阅读。')
    text(s,'开放 · 包容 · 安全 · 可持续',54,286,1168,86,50,TEAL,True)
    cards(s,[('时代呼唤','从“计算互联”走向“智能共生”，回应智能鸿沟、技术封闭与全球性挑战。'),('共同愿景','使智能技术服务人类福祉，以多元参与、透明与贡献导向建立协作信任。'),('报告的回应','将共同愿景连接到具体问题：谁能参与、如何维护复用、公共价值如何验证。')],y=399,h=221)

    s=new('declaration-principles','七项原则，连接共同的价值起点','引言 · 宣言行动框架','三个层次相互衔接，价值主张与研究结论分别呈现。','intro','下列为导读摘编；宣言全文按报告原文保留。')
    for i,(a,b) in enumerate([('筑牢智能时代基石','01  开放互联\n02  安全可信'),('夯实伦理治理支柱','03  数据伦理\n04  多元包容\n05  全球协作'),('共创社会价值未来','06  绿色智能\n07  开源普惠')]):
        x=54+i*399;line(s,x,278,370,color=COLORS[i],width=4);text(s,a,x,310,370,65,28,COLORS[i],True);text(s,b,x,410,370,190,31)

    s=new('declaration-action','从共同愿景，走向证据与行动','引言 · 行动共识','政府、企业、学界与社区，共同支持开放协作。','intro')
    cards(s,[('务实合作','围绕 AI 治理、算力共享与人才培育形成合作任务。'),('持续对话','围绕伦理准则、跨境数据与版权等议题凝聚共识。'),('研究与行动','OSDGs 明确目标，OSDI 组织证据，各章观察连接共同任务与主体责任。')])

    s=new('chapter1','从开放协作到公共价值','第一章 · 共同研究语言','成果的规模、协作关系与开放程度，共同构成发展质量的观察。','chapter')
    cards(s,[('1.1  共同创新','Linux、模型复用与数字公共品：开放怎样连接持续创造与公共价值？'),('1.2  发展目标','四大支柱、十个维度：我们希望推动怎样的发展？'),('1.3  证据与方法','二十九项指标：怎样组织证据、比较差异并辨认局限？')])

    for key,title,total,unit in [('organizations','Linux：让组织投入与共同维护可见','5,686','组织条目'),('contributors','Linux：让具体贡献者进入视野','45,855','贡献者')]:
        s=new('linux-'+key,title,'1.1 · 持续共同创造','累计贡献记录，为理解全球协作提供一个具体入口。','value','LFX Linux Kernel · 2026.10.11 累计快照；前十条记录。两类榜单分母不同，占比不能相加。','fig-1-1-1_linux_collaboration')
        rows=STORY[key]['rows'];names=[r['name'] for r in rows]
        chart(s,'bar',54,261,856,367,names,[dict(name='贡献记录量',values=[r['contributions'] for r in rows],color=TEAL)],800000 if key=='organizations' else 250000)
        text(s,total,954,285,270,70,52,TEAL,True);text(s,unit,954,359,270,44,26)
        text(s,'累计记录展示谁参与过。\n年度活跃与维护责任，需结合跨期活动、审查与分工判断。',954,439,270,180,23,MUTED)

    s=new('model-trend','开放的影响，延伸到下一次创造','1.1 · 模型复用的宏观观察','新增衍生所采用的基础模型，发布方地区构成持续变化。','value','ATOM / Hugging Face 样本 · 2023.11—2026.02；地区指基础模型发布方。原始百分比保留取整差异。','fig-1-1-2_model_derivatives')
    chart(s,'line',54,272,879,351,[r['date'] for r in STORY['models']], [dict(name=n,values=[r[k] for r in STORY['models']],color=c) for n,k,c in [('中国','china',TEAL),('美国','unitedStates',BLUE),('欧洲','europe',GOLD)]])
    text(s,'2026.02',980,281,242,40,25,MUTED)
    for i,(label,n,c) in enumerate([('中国','70%',TEAL),('美国','26%',BLUE),('欧洲','4%',GOLD)]):
        text(s,label,980,345+i*86,95,40,26,c);text(s,n,1080,336+i*86,145,65,45,c,True)

    s=new('qwen-reuse','一个基础模型，连接多种后续用途','1.1 · Qwen 局部实例','发布者声明的关系，让“基于已有成果继续创造”更加具体。','value','2026.10.16 平台关系快照 · 仅选取四条直接关系；不验证训练过程，不分配贡献比例。','fig-1-1-2_qwen_case')
    box(s,54,365,330,105);text(s,'Qwen2.5-7B',76,394,290,56,36,TEAL,True)
    line(s,384,417,65);line(s,449,288,0,292)
    for i,(model,use) in enumerate([('Qwen2.5-7B-Instruct','对话'),('Qwen2.5-7B-Instruct-1M','长上下文'),('Qwen2.5-Coder-7B','编程'),('Qwen2.5-Math-7B','数学')]):
        y=254+i*98;line(s,449,y+38,65);text(s,model,535,y+11,495,46,27,FG,True);text(s,use,1070,y+11,156,46,26,COLORS[i]);line(s,515,y+79,711)

    s=new('sdgs','SDGs：明确希望改善的发展结果','1.1 · 发展方向与实践条件','十七项目标提供共同方向，具体公共成效需要场景中的证据。','value','目标关联不等于已获得数字公共品认可，也不意味着联合国对本报告框架、指标或排名的认证。','fig-1-1-3_sdgs_dpga')
    names=['无贫穷','零饥饿','良好健康与福祉','优质教育','性别平等','清洁饮水和卫生设施','经济适用的清洁能源','体面工作和经济增长','产业、创新和基础设施','减少不平等','可持续城市和社区','负责任消费和生产','气候行动','水下生物','陆地生物','和平、正义与强大机构','促进目标实现的伙伴关系']
    for i,name in enumerate(names):
        x=54+(i%6)*199;y=274+(i//6)*106
        text(s,f'{i+1:02}',x,y,181,34,23,TEAL,True);text(s,name,x,y+38,178,65,21)

    s=new('dpga','DPGA：核验开放成果的实践条件','1.1 · 数字公共品的九项要求','符合相应条件，与在地方实施中取得成效，需要分别验证。','value','来源：报告 1.1 对 DPGA 标准的说明。九项条件与十七项 SDGs 不作逐项对应。','fig-1-1-3_sdgs_dpga')
    requirements=['SDG 相关性','开放许可','清晰权属','平台独立性','文档','非个人识别数据提取','隐私与适用法律','标准与最佳实践','不造成伤害']
    for i,name in enumerate(requirements):
        x=54+(i%3)*399;y=273+(i//3)*108
        line(s,x,y,370);text(s,f'{i+1:02}',x,y+17,58,45,25,TEAL,True);text(s,name,x+68,y+17,302,65,27)

    s=new('public-value','公共价值，在使用与维护中持续验证','1.1 · 从案例回到共同任务','Linux、模型复用与数字公共品，提供三种互补的观察入口。','value')
    cards(s,[('持续参与','谁留下贡献？\n谁继续承担维护？\n新人怎样成长？'),('可维护、可复用','成果如何被理解和使用？\n后续创造依赖哪些条件？\n上游怎样得到支持？'),('可验证的公共价值','谁采用、谁受益？\n本地适配是否充分？\n责任与反馈能否延续？')])

    s=new('goals','OSDGs：四大支柱，十个维度','1.2 · 面向智能时代的发展目标','先找到关心的发展问题，再沿对应维度寻找证据。','goals','本报告的目标框架；宣言、OSDGs 与 OSDI 相互衔接，不作逐项对应，也不合成为总分。','fig-1-2-1_osdg_framework')
    for i,p in enumerate(FRAME['P']):
        x=54+i*298;line(s,x,278,272,color=COLORS[i],width=4);text(s,p[0],x,306,272,42,23,COLORS[i],True);text(s,p[1],x,361,272,88,31,FG,True)
        dims=[d[1] for d in FRAME['D'] if d[-1]==i];text(s,'\n'.join(dims),x,486,272,134,24,MUTED)

    detail=[
      ('talent','人才规模与多样性','参与基础',['规模、密度与进入','跨地区协作与机构结构'],[('规模与密度','活跃开发者、新人进入与人口相对密度，分别回答不同问题。'),('生态多样性','观察跨地区协作与学术机构参与，同时交代地域及机构归属的覆盖。')]),
      ('supply','技术产出与开放供给','开放供给',['代码、模型与数据','保留各自统计单位'],[('代码产出','活跃仓库与协作贡献，共同观察技术资源的积累。'),('模型开放供给','同时观察发布规模、供给方结构与开放条件。'),('数据开放供给','同时观察数据资产积累、发布者与后续使用条件。')]),
      ('connection','全球连接与网络效应','连接与复用',['从孤立数量走向关系','关注传播、集中与依赖'],[('代码影响力','项目、组织与人才在协作网络中的位置。'),('模型影响力','采用、社区参与和后续派生，提供互补信号。'),('数据集影响力','采用与可核验的复用关系，需要各自的来源。')]),
      ('governance','开源善治与公共价值','治理与公共价值',['关注责任与持续性','把技术条件连接到受益'],[('治理成熟度','谁负责治理与维护？参与是否集中？许可是否清楚？'),('公共福祉','数字公共品共建、开放条件与 AI 资产透明度，为场景验证提供入口。')])]
    for i,(id,title,sub,left,rows) in enumerate(detail):
        s=new('goal-'+id,title,'1.2 · 支柱 X'+str(i+1),'在共同框架中，保留不同问题各自的判断空间。','goals')
        dimension(s,sub,'\n'.join(left),rows,COLORS[i])

    s=new('goals-together','四个支柱，共同观察同一技术生态','1.2 · 框架如何共同工作','第二至第五章共同使用四个支柱，章节与支柱并非一一配对。','goals')
    cards(s,[('参与扩大之后','仍需检查维护资源是否充足，参与者能否成长并承担责任。'),('供给增长之后','仍需检查文档、许可与复用条件，避免只看发布数量。'),('影响形成之后','仍需检查贡献集中、治理与持续维护，避免单一排名替代整体判断。')])

    s=new('osdi','OSDI：把发展目标展开为可观察的问题','1.3 · 指标体系','四大支柱、十个维度、二十九项指标，共同组织证据。','methods','29 项为完整观察框架，不表示本期已全部测算。指标角色不代表因果关系或计算权重。','fig-1-3-1_osdi_explorer')
    cards(s,[('北极星指标','关注核心发展结果。\n例：活跃开发者规模、模型生态衍生力。'),('驱动指标','跟踪相关活动和投入。\n例：新晋开发者增速、模型采用度。'),('诊断指标','解释差异与约束。\n例：人才聚集密度、供给方多样性。')])

    groups=[('X1',None,'人才规模与多样性'),('X2',None,'技术产出与开放供给'),('X3','3.1','代码影响力'),('X3','models','模型与数据集影响力'),('X4',None,'开源善治与公共价值')]
    for j,(pid,dim,title) in enumerate(groups):
        rows=[r for r in IND if r['pillar_id']==pid and (not dim or r['dimension_id']==dim or dim=='models' and r['dimension_id'] in ['3.2','3.3'])]
        s=new('indicators-'+str(j+1),title+'：观察什么','1.3 · '+pid+' 指标','指标名称、角色与定义一起阅读；点击指标可查看口径与数据状态。','methods','来源：OSDI 指标字典。本页角色为框架设定，数据状态逐项记录，不以是否入库代替复现核验。','fig-1-3-1_osdi_explorer')
        s['indicatorCodes']=[r['indicator_code'] for r in rows]
        for i,r in enumerate(rows):
            x=54+(i%2)*600;y=263+(i//2)*91
            line(s,x,y,571,color=LINE)
            text(s,r['indicator_name_zh'],x,y+13,420,38,25,FG,True,indicator=r['indicator_code'])
            text(s,r['role'],x+445,y+16,125,33,21,COLORS[['北极星','驱动','诊断'].index(r['role'])],False,'right')
            text(s,r['dimension_name_zh']+' · '+r['indicator_code'],x,y+53,569,29,17,MUTED)

    s=new('opendigger','OpenDigger：让协作成为可观察的证据','1.3 · 代码生态的数据基础','从事件记录，连接到协作关系、指标与研究问题。','methods','150 亿条协作事件记录，截至 2026.06；按报告负责人更新口径。模型等其他资产保留各自来源。')
    text(s,'150 亿',54,280,450,102,76,TEAL,True);text(s,'协作事件记录',58,400,430,53,31)
    text(s,'反馈、讨论、提交与评审，留下可以持续观察的协作记录。',58,485,400,125,25,MUTED)
    for i,(a,b) in enumerate([('事件','记录实际发生的活动'),('关系','连接开发者与仓库'),('指标','在明确范围内聚合与计算'),('研究','解释参与、贡献与影响')]):
        y=266+i*88;text(s,a,568,y,128,48,29,TEAL,True);text(s,b,748,y+3,470,63,24);line(s,568,y+68,658)

    s=new('lenses','同一个项目，四个互补的问题','1.3 · 参与、贡献、影响与开放','先明确问题，再选择指标。示意场景不计算分值。','methods','教学示意；网络影响力不独立证明性能、安全性、治理质量或公共成效。')
    for i,(a,b,c) in enumerate([('参与','谁在实际行动','活跃人数与有效协作行为'),('贡献','贡献了什么','项目内部的任务与协作关系'),('影响','连接到哪些后续创造','更广泛的开发者与仓库网络'),('开放','允许怎样继续使用','材料、许可与具体版本条件')]):
        x=54+i*298;line(s,x,280,272,color=COLORS[i],width=4);text(s,a,x,310,272,74,44,COLORS[i],True);text(s,b,x,414,272,80,27,FG,True);text(s,c,x,523,272,100,23,MUTED)

    s=new('model-methods','模型生态：供给、网络与开放分开观察','1.3 · 模型证据的边界','ModelRank 观察衍生网络；开放分级观察材料与许可。','methods','SJ/T 12304—2026 已发布，2026.12.01 实施。平台样本保留原评估版本，未按发布版重新评级。')
    cards(s,[('供给与复用','模型、数据集与发布组织分别计量；基础模型声明展示后续创造的关系。'),('网络影响','纳入 2024.07—2026.08\n共 26 个月 ModelRank 资料。\n不代表能力测试，独立复现仍需核验。'),('开放条件','材料开放与许可开放分别判断。材料等级需满足本级及前置等级要求。')])

    s=new('comparison','比较之前，先对齐对象、时间和范围','1.3 · 共同的阅读约定','份额与排名，只在明确的比较集合中成立。','methods')
    cards(s,[('对象','开发者、仓库、模型版本与发布组织分别计量。\n下载量不等于实际用户数。'),('时间','主统计期：2025.07—2026.06。\n自然年、月度与快照按图阅读；样本回溯不能还原完整历史存量。'),('范围','明确平台覆盖、比较集合与未知归属。\n仓库数量不等于独立模型家族数。')])

    s=new('evidence','记录数据状态，也记录证据性质','1.3 · 证据的使用边界','定义、入库、使用与复现，分别记录；观测与模拟，逐图区分。','methods')
    text(s,'四种状态',54,274,420,50,31,TEAL,True)
    text(s,'有定义  /  已入库\n图表已使用  /  计算可复现',54,354,520,130,29)
    text(s,'一种状态成立，不代表其他状态自动成立。',54,530,510,74,24,MUTED)
    line(s,626,275,0,329)
    text(s,'四类证据',684,274,530,50,31,BLUE,True)
    text(s,'观测  /  派生\n模拟  /  预测',684,354,530,130,29)
    text(s,'模拟与预测用于探索，不作为事实排名或政策优先级的实证依据。',684,530,530,95,24,MUTED)

    s=new('theme-maps','带着发展问题，进入七个主题地图','1.3 · 从共同框架进入观察','同一主题可以回应多个目标；圆点表示阅读关联，不代表权重。','methods','图 1-3-2 的阅读导引；本次演示到第一章结束，不展开第二章数据分析。','fig-1-3-2_theme_maps')
    short=['活跃','贡献','项目影响','人才','资产','多样性','治理公益']
    for j,m in enumerate(THEMES):
        x=448+j*111;text(s,m[0]+'-Map',x,268,108,35,21,TEAL,True,'center');text(s,short[j],x,309,108,38,20,MUTED,False,'center')
    for i,p in enumerate(FRAME['P']):
        y=373+i*64;line(s,54,y-14,1172);text(s,p[0]+'  '+p[1],54,y,382,44,25,COLORS[i],True)
        for j,m in enumerate(THEMES):
            if p[0] in m[3]:
                s['elements'].append(dict(type='shape',geometry='ellipse',x=490+j*111,y=y+7,w=22,h=22,fill=COLORS[i]))

    s=new('closing','持续共同创造及其公共价值','第一章 · 共同起点','让更多人能够参与，让成果在维护与复用中发展，让受益可以验证。','chapter')
    for i,(a,b) in enumerate([('参与','获得机会，进入真实任务'),('维护','明确责任，延续共同基础'),('复用','理解条件，连接后续创造'),('反馈','检验受益，改进开放协作')]):
        x=54+i*298;text(s,f'0{i+1}',x,300,272,73,49,COLORS[i],True);text(s,a,x,404,272,66,39,FG,True);text(s,b,x,506,272,99,25,MUTED)

    # Keep short columns and compact labels on meaningful phrase boundaries.
    manual={
      'goals':{'人才规模与多样性':'人才规模\n与多样性','技术产出与开放供给':'技术产出\n与开放供给','全球连接与网络效应':'全球连接\n与网络效应','开源善治与公共价值':'开源善治\n与公共价值'},
      'sdgs':{'清洁饮水和卫生设施':'清洁饮水\n和卫生设施','经济适用的清洁能源':'经济适用的\n清洁能源','体面工作和经济增长':'体面工作\n和经济增长','产业、创新和基础设施':'产业、创新\n和基础设施','可持续城市和社区':'可持续城市\n和社区','负责任消费和生产':'负责任消费\n和生产','和平、正义与强大机构':'和平、正义\n与强大机构','促进目标实现的伙伴关系':'促进目标实现\n的伙伴关系'},
      'lenses':{'活跃人数与有效协作行为':'活跃人数\n有效协作行为','项目内部的任务与协作关系':'项目内部的任务\n与协作关系','更广泛的开发者与仓库网络':'更广泛的开发者\n与仓库网络','材料、许可与具体版本条件':'材料与许可\n具体版本的条件'},
      'closing':{'获得机会，进入真实任务':'获得参与机会\n进入真实任务','明确责任，延续共同基础':'明确维护责任\n延续共同基础','理解条件，连接后续创造':'理解使用条件\n连接后续创造','检验受益，改进开放协作':'检验实际受益\n改进开放协作'}
    }
    for s in SLIDES:
        for e in s['elements']:
            if e['type']=='text' and e['text'].replace('\n','') in manual.get(s['id'],{}):
                e['text']=manual[s['id']][e['text'].replace('\n','')]
        source=SOURCES[s['source']]
        s['sourcePath']=str(source.relative_to(ROOT))
        s['speakerNotes']=s['claim']+'\n\n'+s['note']+'\n\n来源：'+s['sourcePath']+'\n\n【对应正文】\n'+source.read_text()
    payload=dict(version='2026-10-27-chapter1-review-v1',scope='封面、前置内容、第一章',slides=SLIDES,indicators=IND,sources={k:p.read_text() for k,p in SOURCES.items()},figures=FIGS,summary=SUMMARY,story=STORY,assets={'disc':base64.b64encode((ROOT/'preview/content/assets/cocreation-disc-dark.svg').read_bytes()).decode()},pptUrl='https://chatgpt.com/space/page_2037254c9d4c8191bf94d8b54be8eb23')
    out.mkdir(parents=True,exist_ok=True)
    (out/'deck.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    template=(HERE/'review.html').read_text()
    (out/'GOSD-2026-Opening-Chapter1-Review.html').write_text(template.replace('__DECK_DATA__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))
    print(json.dumps({'slides':len(SLIDES),'indicators':len(IND),'figures':len(FIGS),'output':str(out)},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'build');main(p.parse_args().output)
