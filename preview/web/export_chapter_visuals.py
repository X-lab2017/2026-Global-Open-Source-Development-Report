"""Sync standalone figure links to the canonical publication views.

Regenerate with chapter1_print.py first; no independent legacy chart rendering.
"""
from pathlib import Path
import argparse,shutil
from chapter1_publication import FIGURES

def main(repo):
    target=repo/'figures/chapter1'
    for item in FIGURES.values():
        name=item[3]+'.svg';source=target/'print'/name
        if not source.exists():raise SystemExit('Generate publication views with chapter1_print.py --font first')
        shutil.copy2(source,target/name)
    shutil.copy2(target/'fig-1-0-1_report_logic.svg',target/'fig-1-0-1_report_logic.editable.svg')
    print('Synced seven publication views; no alternate encodings or palettes.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo-root',type=Path,required=True)
    main(parser.parse_args().repo_root.resolve())
