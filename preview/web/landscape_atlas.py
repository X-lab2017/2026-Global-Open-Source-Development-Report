"""Fixed-position, architectural landscape plates; editorial roles, not dependencies."""
import math
import landscape_content as L

E = L.E
W, H = 1600, 900

# Category coordinates deliberately encode functional groupings. They never use rank.
LAYOUTS = {
    'Agent Infra': [
        ('Agentic coding', 64, 92, 982, 145, 4),
        ('Coding workflows & harnesses', 64, 242, 982, 74, 4),
        ('Personal AI assistants', 1064, 92, 520, 140, 3),
        ('Chatbot workspaces', 1064, 242, 520, 74, 3),
        ('Multi-agent orchestration', 64, 350, 748, 84, 3),
        ('Workflow & agent builders', 824, 350, 760, 84, 3),
        ('Code-first frameworks', 64, 442, 1520, 82, 6),
        ('Memory, knowledge & context', 64, 558, 436, 136, 3),
        ('Protocols & interoperability', 510, 558, 362, 136, 2),
        ('Tools, web & computer use', 882, 558, 340, 136, 2),
        ('Observability & evaluation', 1232, 558, 352, 136, 2),
        ('Development sandboxes', 64, 702, 994, 64, 5),
    ],
    'Model Infra': [
        ('Model API gateways', 64, 92, 772, 66, 4),
        ('Serving · Deploy', 64, 165, 772, 64, 3),
        ('Serving · Inference', 64, 236, 772, 80, 4),
        ('Post-Train · RL & environments', 854, 92, 730, 124, 3),
        ('Post-Train · Supervised fine-tuning', 854, 224, 730, 92, 3),
        ('Pre-Train · Framework & parallel', 64, 350, 930, 106, 3),
        ('Pre-Train · Evaluation & observability', 1006, 350, 280, 106, 1),
        ('Pre-Train · Robotics infra', 1298, 350, 286, 106, 1),
        ('Pre-Train · Compiler & accelerator', 64, 464, 1520, 80, 4),
        ('Data · Labeling', 64, 578, 342, 106, 2),
        ('Data · Integration', 418, 578, 496, 106, 2),
        ('Data · Governance', 926, 578, 658, 106, 4),
        ('Compute & scheduling', 64, 718, 1520, 48, 4),
    ],
}

SHORT = {
    'Coding workflows & harnesses': '编码工作流 / Harness',
    'Workflow & agent builders': '工作流与 Agent 构建',
    'Protocols & interoperability': '协议与互操作',
    'Tools, web & computer use': '工具 / 浏览器 / 计算机',
    'Pre-Train · Evaluation & observability': '训练评估与观测',
}

def tx(x, y, s, size=17, attrs=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" {attrs}>{E(s)}</text>'

def band(title, x, y, w):
    return f'<path d="M{x},{y+7}H{x+w}" stroke="var(--atlas-line)"/>' + tx(x+12,y+1,title,19,'font-weight="700" fill="var(--atlas-accent)" paint-order="stroke" stroke="var(--gv-surface)" stroke-width="8" stroke-linejoin="round"')

def category(key, x, y, w, h, cols):
    pp=[p for p in L.PROJECTS if p['section']==key]
    title=SHORT.get(key,L.SECMAP[key]['name'])
    compact=key=='Compute & scheduling'
    left=184 if compact else 10
    top=8 if compact else 31
    cw=(w-left-10)/cols
    rows=math.ceil(len(pp)/cols)
    ch=(h-top-6)/rows
    parts=[f'<g class="atlas-category" data-atlas-section="{E(key)}" data-box="{x} {y} {w} {h}">',
        f'<rect class="atlas-category-bg" x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="var(--gv-surface)" stroke="var(--atlas-line)" stroke-width="1.2"/>',
        f'<g role="button" tabindex="0" class="atlas-category-title" data-atlas-category="{E(key)}" aria-label="查看{E(title)}模块" aria-pressed="false"><title>{E(key)} · {E(L.SECMAP[key]["description"])}</title>',
        f'<rect x="{x+1}" y="{y+1}" width="{174 if compact else w-2}" height="{h-2 if compact else 27}" rx="6" fill="var(--atlas-soft)"/>',
        tx(x+12,y+26 if compact else y+20,title,16,'font-weight="650"'),
        '</g>',
        tx(x+w-10,y+19,'',12,'class="atlas-category-stat" text-anchor="end" fill="var(--gv-muted)"')]
    for i,p in enumerate(pp):
        px=x+left+(i%cols)*cw;py=y+top+(i//cols)*ch
        logo=min(25,ch-6);avail=cw-logo-18
        font=min(17,max(11.5,avail/max(1,len(p['name'])*.66)))
        yy=py+ch/2
        parts += [f'<g role="button" tabindex="0" class="atlas-project" data-atlas-project="{p["id"]}" data-atlas-category-key="{E(key)}" aria-pressed="false" aria-label="{E(p["name"])}，查看项目详情"><title>{E(p["name"])} · {E(p["repo"])}</title>',
            f'<rect class="atlas-project-bg" x="{px}" y="{py+1}" width="{cw-5}" height="{ch-2}" rx="4" fill="var(--atlas-accent)" fill-opacity="0" stroke="none"/>']
        if p['logo']:
            parts += [f'<rect x="{px+3}" y="{yy-logo/2}" width="{logo}" height="{logo}" rx="4" fill="#fff"/>',f'<image href="/assets/landscape/logos/{E(p["logo"])}" x="{px+3}" y="{yy-logo/2}" width="{logo}" height="{logo}" preserveAspectRatio="xMidYMid meet"/>']
        else: parts += [tx(px+7,yy+5,p['name'][0].upper(),16,'fill="var(--atlas-accent)" font-weight="700"')]
        parts += [tx(px+logo+9,yy+5,p['name'],round(font,2),'font-weight="550"'),
            f'<rect class="atlas-value-bar" x="{px+logo+9}" y="{py+ch-3}" width="0" height="2" fill="var(--atlas-accent)" data-max-width="{avail}"/>','</g>']
    parts += ['</g>']
    return ''.join(parts)

def map_svg(layer):
    agent=layer=='Agent Infra'
    count=86 if agent else 59
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="group" aria-label="{layer} 交互式结构全景" class="atlas-svg"><rect width="{W}" height="{H}" fill="var(--gv-surface)"/>',
        tx(64,35,layer+' Landscape',31,'font-weight="750" letter-spacing="-0.6"'),
        tx(1584,29,f'{count} 个项目 · {12 if agent else 13} 个类别',18,'text-anchor="end" fill="var(--atlas-accent)" font-weight="650"'),
        tx(1584,52,'',14,'class="atlas-period" text-anchor="end" fill="var(--gv-muted)"'),
        f'<defs><clipPath id="{"agent" if agent else "model"}-board-clip"><rect x="0" y="58" width="1600" height="716"/></clipPath></defs><g clip-path="url(#{"agent" if agent else "model"}-board-clip)"><g class="atlas-board">',
        '<rect x="14" y="83" width="30" height="683" rx="11" fill="var(--atlas-soft)" stroke="var(--atlas-line)"/>',
        f'<text transform="translate(34 430) rotate(-90)" text-anchor="middle" font-size="16" font-weight="700" fill="var(--atlas-accent)">{"任务入口 ← 编排构建 ← 运行支撑" if agent else "模型服务 ← 模型能力 ← 数据与算力"}</text>']
    if agent:
        parts += [band('APPLICATIONS / 任务入口',64,76,1520),band('AGENT FRAMEWORK / 构建与编排',64,334,1520),band('AGENT RUNTIME / 运行基础设施',64,542,1520)]
    else:
        parts += [band('SERVING / 模型服务',64,76,772),band('POST-TRAIN / 后训练',854,76,730),band('PRE-TRAIN / 训练与加速',64,334,1520),band('DATA / 数据基础',64,562,1520),band('COMPUTE / 算力底座',64,702,1520)]
    for args in LAYOUTS[layer]: parts.append(category(*args))
    if agent:
        parts += ['<rect x="1070" y="702" width="514" height="64" rx="7" fill="var(--atlas-soft)" stroke="var(--atlas-line)" stroke-dasharray="5 4"/>',tx(1084,728,'↓ 连接 Model Infra 的模型服务',18,'font-weight="650"'),tx(1084,751,'模型 API 网关 / 部署 / 推理，为 Agent 提供模型能力',14,'fill="var(--gv-muted)"')]
    parts += ['</g></g>', '<g class="atlas-inspector" aria-live="polite"></g>',tx(64,892,'功能关系示意 · 非项目依赖图。标识为仓库所有者图标；分类与样本沿用固定主表。',12,'fill="var(--gv-muted)"'),'</svg>']
    return ''.join(parts)

def controls(id, months):
    return f'''<div class="atlas-controls" aria-label="全景操作"><div class="atlas-control-row"><div class="atlas-lenses" role="group" aria-label="观察方式"><button type="button" data-atlas-lens="structure" aria-pressed="true">技术结构</button><button type="button" data-atlas-lens="influence" aria-pressed="false">影响力</button><button type="button" data-atlas-lens="change" aria-pressed="false">月度变化</button></div><label class="atlas-search">查找项目<input type="search" data-atlas-search placeholder="名称 / 仓库 / 类别" aria-label="查找{id}中的项目"></label><label>月份<select data-atlas-month>{''.join(f'<option value="{i}">{m}</option>' for i,m in reversed(list(enumerate(months))))}</select></label><button type="button" data-atlas-reset>恢复全景</button></div><div class="atlas-control-row atlas-routes" role="group" aria-label="从场景理解技术结构"></div><p class="atlas-hint">点模块标题看作用与代表项目，点项目看指标与轨迹。双击模块可放大；全屏可一页查看。</p></div>'''
