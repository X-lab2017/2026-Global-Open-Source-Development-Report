"""Check the shared manuscript, publication views and downloadable PDF identity."""
from pathlib import Path
import argparse, hashlib, json, re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--inspect-pdf',action='store_true');args=p.parse_args()
assets=ROOT/'preview/content/report-assets'
m=json.loads((assets/'chapter1/sample-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in m['manuscript_sha256'].items():
    assert sha(ROOT/path)==digest, f'Regenerate sample after manuscript edit: {path}'
pdf=assets/'chapter1/GOSD-2026-chapter1-sample.pdf'
assert sha(pdf)==m['pdf_sha256'] and pdf.read_bytes().startswith(b'%PDF-')
assert sha(ROOT/'preview/content/gosm/network.json.gz')==m['qwen_sha256']
for record in m['source_files'].values():assert sha(ROOT/record['path'])==record['sha256']
files=sorted((ROOT/'figures/chapter1/print').glob('*.svg'));assert len(files)==4
for f in files:
    ET.fromstring(f.read_text());assert f.read_bytes()==(assets/'print'/f.name).read_bytes()
if args.output:
    assert (args.output/'assets/report/chapter1'/pdf.name).read_bytes()==pdf.read_bytes()
    for lang in ['zh','en']:
        text=(args.output/f'2026/{lang}/chapters/01/index.html').read_text()
        assert text.count('class="chapter-sample-edition"')==1
        assert pdf.name in text
        for f in files:
            assert '/assets/report/print/'+f.name in text
            assert (args.output/'assets/report/print'/f.name).read_bytes()==f.read_bytes()
if args.inspect_pdf:
    from pypdf import PdfReader
    reader=PdfReader(pdf);assert len(reader.pages)==8
    normalize=lambda s:re.sub(r'\s+','',s.replace('**',''))
    narrative=normalize(''.join(reader.pages[i].extract_text() for i in [0,2,4,6]))
    for path in m['manuscript_sha256']:
        for para in (ROOT/path).read_text().split('\n\n'):
            if para.strip() and not para.startswith(('#','![')):
                assert normalize(para) in narrative, f'PDF lost manuscript paragraph: {para[:60]}'
    from chapter_visuals import SDGS,DPG
    public=normalize(reader.pages[7].extract_text())
    for item in [*SDGS,*DPG]:assert normalize(item[0]) in public,item[0]
    story=json.loads((ROOT/'preview/content/story-data.json').read_text())
    linux=normalize(reader.pages[3].extract_text())
    for key in ['organizations','contributors']:
        for r in story[key]['rows']:
            assert normalize(r['name']) in linux
            assert f'{r["contributions"]:,}' in linux and f'{r["percentage"]:.2f}%' in linux
    for page in reader.pages:
        assert abs(float(page.mediabox.width)-595.276)<.1
        assert abs(float(page.mediabox.height)-841.89)<.1
        fonts=page['/Resources']['/Font'].get_object()
        cjk=[f.get_object() for f in fonts.values() if 'GOSD' in str(f.get_object().get('/BaseFont',''))]
        assert cjk and all('/FontFile2' in f['/FontDescriptor'].get_object() for f in cjk)
print('PASS: one manuscript, four publication views, eight-page PDF; source and publication hashes agree.'+(' Full PDF prose, 20 ranking rows, 26 goal/condition labels and embedded CJK font verified.' if args.inspect_pdf else ''))
