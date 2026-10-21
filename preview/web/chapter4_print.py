"""Assemble the private, complete Chapter 4 review PDF with continuous navigation."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import fitz
import landscape_publication as P
from gosl_publication import SECTIONS, figure_number
from gosl_landscapes import DATASETS

ROOT = Path(__file__).resolve().parents[2]
WEB = 'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/04/'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    first, rest = args.work/'opening-and-4-1.pdf', args.work/'sections-4-2-to-4-6.pdf'
    subprocess.run([sys.executable, str(ROOT/'preview/web/landscape_print.py'), '--font', str(args.font), '--output', str(first), '--whole-chapter', '--total-pages', '17'], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT/'preview/web/gosl_print.py'), '--font', str(args.font), '--output', str(rest), '--work', str(args.work/'font'), '--page-offset', '12', '--total-pages', '17'], cwd=ROOT, check=True)
    doc = fitz.open()
    for path, expected in [(first,12),(rest,5)]:
        with fitz.open(path) as part:
            assert len(part)==expected, (path,len(part))
            doc.insert_pdf(part)
    toc = [[1,P.CHAPTER_TITLE,1],[2,'4.1 '+P.TITLE,2]]
    figure_pages = [3,4,5,6,6,7,7,8,9,9,10,10,11]
    for i, ((_, title), page) in enumerate(zip(P.FIGURES,figure_pages),1):
        toc.append([3,f'图 4-1-{i} {title}',page])
    toc.append([3,P.ACTION_TITLE,12])
    for page,d in enumerate(DATASETS,13):
        m=SECTIONS[d['id']]
        toc.extend([[2,d['number']+' '+m['title'],page],[3,figure_number(d)+' '+m['caption'],page]])
    doc.set_toc(toc)
    layout=json.loads((ROOT/'tmp/pdfs/a-landscape/layout.json').read_text())
    guide=next(x for x in layout if x.get('kind')=='guide')
    for i,page in enumerate([2,13,14,15,16,17]):
        x=46+(i%2)*262;y=guide['top']+(i//2)*62
        doc[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(x,y,x+241,y+56),'page':page-1,'to':fitz.Point(0,0)})
    doc.set_metadata({'title':'GOSD 2026 · 第四章 全球开源技术全景洞察','author':'GOSD / 全球开源发展报告','subject':'章首与 4.1—4.6；18 幅图；4.2—4.6 为技术全景与研究框架','keywords':'GOSD, GOSL, 20261021-chapter4-v3','creator':'GOSD shared Web/PDF manuscript'})
    doc.save(args.output,garbage=4,deflate=True)
    assert len(doc)==17 and len(doc.get_toc())==26
    print(f'{args.output}: {len(doc)} pages, {len(doc.get_toc())} bookmarks')

if __name__=='__main__':
    main()
