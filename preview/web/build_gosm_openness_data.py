import json,gzip,pathlib,hashlib,shutil
root=pathlib.Path(__file__).resolve().parents[2];portal=pathlib.Path(__file__).resolve().parents[1];d=portal/'content/gosm'
rank=json.loads((portal/'content/gosr/model-rankings-snapshot.json').read_text())
open_data=json.loads(gzip.decompress((d/'openness-current.json.gz').read_bytes()))
evidence=json.loads(gzip.decompress((d/'openness-evidence-884.json.gz').read_bytes()))
levels=[
 dict(id='L1',label='开放部署级',short='能部署',addition='权重、配置、分词器、推理脚本与环境',meaning='具备在本地环境运行基础推理所需的材料。',verify='运行最小推理示例，核对配置、输出和环境。',detail='提供可部署权重及校验信息、模型配置、可加载分词器、可运行推理示例，以及依赖版本、安装与硬件要求。'),
 dict(id='L2',label='模型理解级',short='能理解',addition='实现原理、训练过程与测试结果',meaning='在部署基础上，理解模型原理、训练过程与能力边界。',verify='核对原理、训练说明与测试结果是否自洽。',detail='继承 L1。补充架构与设计动机、训练流程与主要数据类别/规模、已知偏差与局限，以及测试指标、来源、设置和适用范围。'),
 dict(id='L3',label='训练公开级',short='能再训练',addition='训练代码、数据或完整来源与处理规则、环境',meaning='在理解基础上，复用核心训练组件并启动再训练。',verify='启动最小规模或数据子集训练，核对命令与参数。',detail='继承 L1—L2。提供可运行训练/对齐代码与提交记录、超参数和启动命令；提供可再训练数据集（许可与获取方式），或所有源数据集清单（版本、链接）及完整处理脚本或详细规则；同时提供锁定依赖、环境验证与硬件说明。仅有数据规模概要不能替代完整来源与处理链。'),
 dict(id='L4',label='模型验证级',short='能验证',addition='测试代码、数据、环境与无重叠说明',meaning='在训练公开基础上，独立验证模型的性能与行为。',verify='按公开配置，在至少一个公开数据集上复现实验。',detail='继承 L1—L3。提供测试脚本和完整配置（提示词、精度、采样等）、测试数据版本/来源/许可、测试环境与命令，以及训练与测试数据无重叠声明或证明方法。'),
 dict(id='L5',label='全链开源级',short='能全链复现',addition='预处理、清洗、原始数据说明与复现指南',meaning='在验证基础上，支持从数据准备到部署的端到端复现。',verify='从数据准备到部署跑通最小闭环，记录校验与误差。',detail='继承 L1—L4。提供数据预处理与清洗代码、混合/采样比例、去重/过滤规则、完整数据配方与来源分布，以及资源、启动、恢复和校验齐备的端到端指南。不分发原始数据时，仍需完整配方与来源清单。可采用关键阶段或代表性子集验证，但不降低材料披露要求。')]
opens=[
 dict(id='O1',label='有限制开放',short='存在实质限制',detail='对使用、修改、再分发或商业化存在实质限制，如不得改进其他模型、商业门槛、限定地域/行业，或要求显著品牌展示。应逐条核对预期用途。'),
 dict(id='O2',label='互惠开放',short='衍生须开放回馈',detail='允许使用、修改、再训练、验证和复现；衍生物再分发须按相同或兼容许可开放，承担相应回馈义务。'),
 dict(id='O3',label='宽松开放',short='主要保留权利声明',detail='授予广泛的使用、修改、再分发与商业化权利；无 O1 实质限制和 O2 回馈义务，主要保留版权、许可、免责声明和必要归属。'),
 dict(id='O4',label='零义务开放',short='无额外合同义务',detail='采用 CC0、Unlicense 或类似授权，不额外附加使用、修改、再分发的合同性义务；法律法规仍然适用。')]
rows={r['model_id']:{'rank':r['rank'],'score':r['modelrank_value']} for r in rank['rows']}
history={}
for month in rank['months']:
 path=portal/f'content/gosr/model-monthly-source/modelrank-{month}-top100.raw.json'
 for r in json.loads(path.read_text())['data']['rows']:
  history.setdefault(r['name'],{})[month]={'rank':r['rank'],'score':r['score_normalized']}
ids={r['model_id'] for r in open_data['models']}
joined=ids&rows.keys()
out={'version':'gosm-openness-v2-atlas','containsSimulatedStatistics':False,'standard':{'title':'人工智能 关键基础技术 大模型技术体系开源开放分级评估规范','version_note':'SJ/T 12304-2026；发布信息见publication字段。','pdf':'grading-specification-reference.pdf','scope':'具体版本的模型发布单元（MRU）；先确认累进完整性 L，再判断对应材料范围的许可开放性 O。','levels':levels,'openness':opens},'modelrank':{'period':rank['ranking_period'],'source_url':rank['ranking_source_url'],'snapshot_date':rank['retrieved_at'][:10],'months':rank['months'],'top_k':100,'matched_count':len(joined),'rows':rows,'history':history,'notes':rank['notes'][:4]},'indicators':{r['model_id']:r['indicators'] for r in evidence['models']},'platform_check':{'date':'2026-10-18','overview_url':'http://47.100.76.186:9529/api/openness/overview/','months_url':'http://47.100.76.186:9529/api/modelrank/months/','openness_n':884,'latest_modelrank_month':'2026-08','note':'核对公开页面声明的GET接口。月榜本次请求502，复用2026-10-17保存的同一月份Top100。'},'teaching_example':{'name':'Atlas-Demo v1.0','simulated':True,'note':'仅解释条件变化，不代表真实模型或正式评估。'}}
out['standard']['requirements']=json.loads((d/'standard-requirements.json').read_text())
out['standard']['publication']=json.loads((d/'standard-publication.json').read_text())
out['standard']['version_note']='SJ/T 12304-2026，工业和信息化部2026年第22号公告批准发布；2026-08-17发布，2026-12-01实施。条文解释依据用户提供的规范文本。附件原文件保留；其封面占位编号不作为标准发布状态的判断依据。'
(d/'openness53.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('Saved',len(joined),'exact ID joins;',len(history),'models observed in monthly Top100; data', (d/'openness53.json').stat().st_size)
