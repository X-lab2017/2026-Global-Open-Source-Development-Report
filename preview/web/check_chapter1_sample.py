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
    svg=ET.fromstring(f.read_text());assert f.read_bytes()==(assets/'print'/f.name).read_bytes()
    sizes=[float(n.attrib['font-size']) for n in svg.iter() if 'font-size' in n.attrib]
    assert max(sizes)*(595.2755905511812-92)/640<=m['body_font_pt'],f'Figure text exceeds body text: {f.name}'
public_svg=ET.fromstring((ROOT/'figures/chapter1/print/fig-1-1-3_sdgs_dpga.svg').read_text())
assert len(public_svg.findall('.//{http://www.w3.org/2000/svg}polygon'))==17
assert len([n for n in public_svg.findall('.//{http://www.w3.org/2000/svg}rect') if n.get('width')=='98'])==9
assert '开放软件 · 开放数据 · 开放 AI 系统 · 开放内容' not in ET.tostring(public_svg,encoding='unicode')
if args.output:
    assert (args.output/'assets/report/chapter1'/pdf.name).read_bytes()==pdf.read_bytes()
    for lang in ['zh','en']:
        text=(args.output/f'2026/{lang}/chapters/01/index.html').read_text()
        assert text.count('class="chapter-sample-edition"')==1
        assert pdf.name+'?v='+m['edition'] in text
        assert 'class="public-assets"' not in text
        assert all(f'<small>1.1.{i}</small>' in text for i in range(1,5))
        for section,count in [(1,4),(2,6),(3,3)]:
            assert all(f'1.{section}.{i} ' in text for i in range(1,count+1))
        for f in files:
            assert '/assets/report/print/'+f.name in text
            assert (args.output/'assets/report/print'/f.name).read_bytes()==f.read_bytes()
if args.inspect_pdf:
    from pypdf import PdfReader
    reader=PdfReader(pdf);assert len(reader.pages)==m['pages']
    normalize=lambda s:re.sub(r'\s+','',s.replace('**',''))
    pages=[normalize(page.extract_text()) for page in reader.pages]
    narrative=''.join(pages)
    for path in m['manuscript_sha256']:
        for para in (ROOT/path).read_text().split('\n\n'):
            if para.strip() and not para.startswith(('#','![')):
                assert normalize(para) in narrative, f'PDF lost manuscript paragraph: {para[:60]}'
                for fid in m['figure_ids']:
                    if '图 '+fid in para:
                        refpage=next(i+1 for i,text in enumerate(pages) if normalize(para) in text)
                        assert 0<=m['figure_pages'][fid]-refpage<=1, f'Figure too far from reference: {fid}'
    from chapter_visuals import SDGS,DPG
    public=pages[m['figure_pages']['1-1-3']-1]
    for item in [*SDGS,*DPG]:assert normalize(item[0]) in public,item[0]
    story=json.loads((ROOT/'preview/content/story-data.json').read_text())
    linux=pages[m['figure_pages']['1-1-1']-1]
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
    for heading in m['headings']:assert normalize(heading['text']) in pages[heading['page']-1]
    assert len(reader.outline)==2 and len(reader.outline[1])==2
    assert normalize('开放软件 · 开放数据 · 开放 AI 系统 · 开放内容') not in narrative
print(f'PASS: one manuscript, four publication views, {m["pages"]}-page PDF; source and publication hashes agree.'+(' Full prose, nearby figures, numbered headings, 20 ranking rows, 26 goal/condition labels and embedded CJK font verified.' if args.inspect_pdf else ''))
