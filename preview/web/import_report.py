#!/usr/bin/env python3
"""Refresh the Preview's generated snapshot from canonical report sources."""
from pathlib import Path
import argparse,csv,hashlib,json,shutil,subprocess

def run(repo,ref):
    root=Path(__file__).resolve().parents[1]
    selected=sorted((repo/'chapters/chapter1').glob('*.md'))+[repo/'appendices/附录A-指标体系与数据来源.md',repo/'data/meta/数据可用性清单.md']
    documents={p.relative_to(repo).as_posix():p.read_text() for p in selected}
    def rows(name):
        with (repo/'data/meta'/name).open(newline='') as f:return list(csv.DictReader(f))
    inventory=rows('dataset_inventory.csv')
    current={p.relative_to(repo).as_posix() for p in (repo/'data/processed').rglob('*.csv')}
    assert current=={x['path'] for x in inventory},'Update data/meta/dataset_inventory.csv when adding processed datasets'
    for row in inventory:
        assert hashlib.sha256((repo/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    hashes={p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in documents}
    snapshot={'source_ref':ref,'updated_at':'2026-10-12','documents':documents,'indicators':rows('osdi_indicator_dictionary.csv'),'datasets':inventory,'sources':rows('source_register.csv'),'chapter_map':rows('chapter_indicator_map.csv'),'content_sha256':hashes,'repository_paths':[p.relative_to(repo).as_posix() for folder in ['chapters','appendices','data','figures','editorial','outline','planning'] for p in (repo/folder).rglob('*') if p.is_file()]}
    (root/'content/report.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    assets=root/'content/report-assets';assets.mkdir(exist_ok=True)
    for filename in ['fig-1-0-1_report_logic.svg','fig-1-2-1_osdg_framework.svg']:
        shutil.copy2(repo/'figures/chapter1'/filename,assets/filename)
    for filename in ['osdi_indicator_dictionary.csv','chapter_indicator_map.csv','dataset_inventory.csv','source_register.csv','osdg-framework.json']:
        shutil.copy2(repo/'data/meta'/filename,assets/filename)
    data=assets/'data';data.mkdir(exist_ok=True)
    for item in inventory:shutil.copy2(repo/item['path'],data/Path(item['path']).name)
    print(f'Imported {len(documents)} manuscript files, {len(snapshot["indicators"])} definitions and {len(inventory)} unchanged datasets from {ref}.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,required=True);parser.add_argument('--source-ref',required=True)
    args=parser.parse_args();run(args.repo_root.resolve(),args.source_ref)
