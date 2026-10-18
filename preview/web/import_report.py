#!/usr/bin/env python3
"""Refresh the Preview's generated snapshot from canonical report sources."""
from pathlib import Path
import argparse,csv,hashlib,json,shutil,subprocess
from datetime import datetime,timezone
import chapter_visuals

def run(repo,ref):
    root=Path(__file__).resolve().parents[1]
    selected=sorted((repo/'chapters/chapter1').glob('*.md'))+[repo/'appendices/附录A-指标体系与数据来源.md',repo/'data/meta/数据可用性清单.md']
    documents={p.relative_to(repo).as_posix():p.read_text() for p in selected}
    front_paths=['outline/执行摘要.md','chapters/引言-人工智能时代的开源发展.md','outline/目录.md']
    front={'source_ref':ref,'documents':{p:(repo/p).read_text() for p in front_paths},'content_sha256':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in front_paths}}
    (root/'content/frontmatter.json').write_text(json.dumps(front,ensure_ascii=False,indent=2)+'\n')
    def rows(name):
        with (repo/'data/meta'/name).open(newline='') as f:return list(csv.DictReader(f))
    inventory=rows('dataset_inventory.csv')
    current={p.relative_to(repo).as_posix() for p in (repo/'data/processed').rglob('*.csv')}
    indexed={x['path'] for x in inventory}
    assert indexed<=current,'Dataset inventory references missing processed files'
    for row in inventory:
        assert hashlib.sha256((repo/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    # Register new files in the generated Preview catalog only. Their presence
    # does not establish an indicator mapping or change an approved figure.
    new_paths=sorted(current-indexed)
    for path in new_paths:
        source=repo/path
        with source.open(newline='',encoding='utf-8-sig') as f:
            reader=csv.DictReader(f);records=list(reader);fields=reader.fieldnames or []
        inventory.append({'dataset_id':source.stem,'path':path,'row_count':str(len(records)),
            'fields':';'.join(fields),'chapter':source.parent.name.removeprefix('chapter'),
            'use_scope':'文件目录与原表下载；未自动纳入已审核图表',
            'related_indicators':'','status':'已入库；方法说明与指标映射待补',
            'review_note':'Preview 自动登记字段、行数与校验值；分析口径和内容核验待负责人确认。',
            'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    assert len({Path(x['path']).name for x in inventory})==len(inventory),'Duplicate download filename'
    hashes={p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in documents}
    snapshot={'source_ref':ref,'updated_at':datetime.now(timezone.utc).date().isoformat(),'documents':documents,'indicators':rows('osdi_indicator_dictionary.csv'),'datasets':inventory,'sources':rows('source_register.csv'),'chapter_map':rows('chapter_indicator_map.csv'),'content_sha256':hashes,'repository_paths':[p.relative_to(repo).as_posix() for folder in ['chapters','appendices','data','figures','editorial','outline','planning'] for p in (repo/folder).rglob('*') if p.is_file()]}
    (root/'content/report.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    assets=root/'content/report-assets';assets.mkdir(exist_ok=True)
    for filename in ['fig-1-0-1_report_logic.svg','fig-1-2-1_osdg_framework.svg','fig-1-1-1_linux_collaboration.svg','fig-1-1-2_model_derivatives.svg','fig-1-1-3_sdgs_dpga.svg','fig-1-3-1_osdi_explorer.svg','fig-1-1-2_qwen_case.svg','fig-1-3-2_theme_maps.svg']:
        shutil.copy2(repo/'figures/chapter1'/filename,assets/filename)
    (assets/'chapter1').mkdir(exist_ok=True)
    chapter_files=['本章介绍.md','1.1-开源-数字公共品与可持续发展引擎.md','1.2-OSDGs-开源发展目标框架.md','1.3-OSDI-开源发展度量体系.md']
    for i,name in enumerate(chapter_files):shutil.copy2(repo/'chapters/chapter1'/name,assets/'chapter1'/('section-'+str(i)+'.md'))
    for filename in ['osdi_indicator_dictionary.csv','chapter_indicator_map.csv','source_register.csv','osdg-framework.json']:
        shutil.copy2(repo/'data/meta'/filename,assets/filename)
    with (assets/'dataset_inventory.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(inventory[0]));writer.writeheader();writer.writerows(inventory)
    data=assets/'data';data.mkdir(exist_ok=True)
    for item in inventory:shutil.copy2(repo/item['path'],data/Path(item['path']).name)
    action=root/'content/action';action.mkdir(exist_ok=True)
    shutil.copy2(repo/'chapters/chapter6/action-framework.json',action/'chapter6.json')
    for svg in (repo/'figures/chapter6').glob('*.svg'):shutil.copy2(svg,action/svg.name)
    chapter_visuals.import_story(repo,ref)
    if new_paths:print(f'Preview catalog: {len(new_paths)} new files registered with pending methods; canonical inventory preserved.')
    print(f'Imported {len(documents)} manuscript files, {len(snapshot["indicators"])} definitions and {len(inventory)} unchanged datasets from {ref}.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,required=True);parser.add_argument('--source-ref',required=True)
    args=parser.parse_args();run(args.repo_root.resolve(),args.source_ref)
