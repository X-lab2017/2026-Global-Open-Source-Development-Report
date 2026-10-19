"""Check the shared manuscript, publication views and downloadable PDF identity."""
from pathlib import Path
import argparse, hashlib, json, re, xml.etree.ElementTree as ET

from chapter1_publication import FIGURES,PDF_NAME,MANIFEST_NAME
from chapter1_visual_contract import MODEL_SERIES,MODEL_TICKS

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--inspect-pdf',action='store_true');args=p.parse_args()
assets=ROOT/'preview/content/report-assets'
m=json.loads((assets/'chapter1'/MANIFEST_NAME).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in m['manuscript_sha256'].items():
    assert sha(ROOT/path)==digest, f'Regenerate chapter after manuscript edit: {path}'
pdf=assets/'chapter1'/PDF_NAME
assert sha(pdf)==m['pdf_sha256'] and pdf.read_bytes().startswith(b'%PDF-')
assert sha(ROOT/'preview/content/gosm/network.json.gz')==m['qwen_sha256']
for record in m['source_files'].values():assert sha(ROOT/record['path'])==record['sha256']
files=sorted((ROOT/'figures/chapter1/print').glob('*.svg'));assert len(files)==7
for f in files:
    svg=ET.fromstring(f.read_text());assert f.read_bytes()==(assets/'print'/f.name).read_bytes()
    assert f.read_bytes()==(ROOT/'figures/chapter1'/f.name).read_bytes(), 'Standalone export drift'
    assert f.read_bytes()==(assets/f.name).read_bytes(), 'Download export drift'
    texts=svg.findall('.//{http://www.w3.org/2000/svg}text')
    caption=texts[-1]
    assert caption.get('x')=='320' and caption.get('text-anchor')=='middle'
    assert float(caption.get('y'))>float(svg.get('height'))-10
    expected=next(v for v in FIGURES.values() if v[3]+'.svg'==f.name)
    assert ' '.join(caption.text.split())==expected[0]+' '+expected[1]
    sizes=[float(n.attrib['font-size']) for n in svg.iter() if 'font-size' in n.attrib]
    assert max(sizes)*(595.2755905511812-92)/640<=m['body_font_pt'],f'Figure text exceeds body text: {f.name}'
assert len(m['manuscript_sha256'])==4 and len(m['figure_ids'])==7
assert (assets/'chapter1/GOSD-2026-chapter1-sample.pdf').read_bytes()==pdf.read_bytes(), 'Keep shared sample URLs working'
assert sha(ROOT/'data/meta/osdi_indicator_dictionary.csv')==m['indicator_dictionary_sha256']
indicators=json.loads((ROOT/'preview/content/report.json').read_text())['indicators']
assert len(indicators)==29
public_svg=ET.fromstring((ROOT/'figures/chapter1/print/fig-1-1-3_sdgs_dpga.svg').read_text())
assert len(public_svg.findall('.//{http://www.w3.org/2000/svg}polygon'))==17
assert len([n for n in public_svg.findall('.//{http://www.w3.org/2000/svg}rect') if n.get('width')=='98'])==9
assert '开放软件 · 开放数据 · 开放 AI 系统 · 开放内容' not in ET.tostring(public_svg,encoding='unicode')
# Prevent the original regression: the same monthly composition must remain a
# stacked chart with the same raw heights, bottom-to-top order and region colors.
model=ET.fromstring((ROOT/'figures/chapter1/print/fig-1-1-2_model_derivatives.svg').read_text())
bars=[n for n in model.findall('.//{http://www.w3.org/2000/svg}rect') if abs(float(n.get('width'))-(596/28-4))<.001]
story=json.loads((ROOT/'preview/content/story-data.json').read_text())
assert len(bars)==84
for i,row in enumerate(story['models']):
    bottom=121+150-26
    for j,(key,_,__,color) in enumerate(MODEL_SERIES):
        bar=bars[i*3+j];height=150*row[key]/100;bottom-=height
        assert abs(float(bar.get('height'))-height)<.001
        assert abs(float(bar.get('y'))-bottom)<.001 and bar.get('fill')==color
for _,label in MODEL_TICKS:assert label in ''.join(model.itertext())
if args.output:
    assert (args.output/'assets/report/chapter1'/pdf.name).read_bytes()==pdf.read_bytes()
    for lang in ['zh','en']:
        text=(args.output/f'2026/{lang}/chapters/01/index.html').read_text()
        assert text.count('class="chapter-download-edition"')==1
        assert pdf.name+'?v='+m['edition'] in text
        assert 'class="public-assets"' not in text
        assert text.count('id="fig-theme-maps"')==1
        assert text.count('class="chapter-print-figure"')==7
        for v in FIGURES.values():
            caption=(v[0]+' '+v[1]) if lang=='zh' else (v[0].replace('图','Figure')+' '+v[2])
            assert '<figcaption>'+caption+'</figcaption>' in text,caption
        assert all(f'<small>1.1.{i}</small>' in text for i in range(1,5))
        for section,count in [(1,4),(2,6),(3,3)]:
            assert all(f'1.{section}.{i} ' in text for i in range(1,count+1))
        for f in files:
            assert '/assets/report/print/'+f.name in text
            assert (args.output/'assets/report/print'/f.name).read_bytes()==f.read_bytes()
            assert (args.output/'assets/report'/f.name).read_bytes()==f.read_bytes()
        from goso_reading import Tree
        nodes=list(Tree(text).root.walk())
        month_bars=[n for n in nodes if n.has('month-bar')]
        assert len(month_bars)==28
        for i,bar in enumerate(month_bars):
            segments=[n for n in bar.walk() if n.has('stack-segment')]
            assert len(segments)==3
            for segment,(key,_,__,color) in zip(segments,MODEL_SERIES):
                assert segment.has('region-'+key)
                assert f"height:{story['models'][i][key]}%" in segment.attrs['style']
                assert 'background:'+color in segment.attrs['style']
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
    def outline_titles(items):
        return [title for item in items for title in (outline_titles(item) if isinstance(item,list) else [item['/Title']])]
    assert outline_titles(reader.outline)==[x['text'] for x in m['headings']]
    assert len(m['headings'])==17
    atlas=pages[m['figure_pages']['1-3-1']-1]
    goals=pages[m['figure_pages']['1-2-1']-1]
    for item in indicators:
        assert normalize(item['indicator_name_zh']) in atlas
        assert normalize(item['dimension_name_zh']) in atlas and normalize(item['dimension_name_zh']) in goals
    for role in ['北极星','驱动','诊断']:assert role in atlas
    from chapter1_theme_map import MAPS
    themes=pages[m['figure_pages']['1-3-2']-1]
    for i,item in enumerate(MAPS):assert item[1] in themes and '2.'+str(i+1) in themes
    assert '所有模型ID均带' not in narrative and '与A分属不同样本' not in narrative
    assert normalize('开放软件 · 开放数据 · 开放 AI 系统 · 开放内容') not in narrative
print(f'PASS: one manuscript, seven publication views, {m["pages"]}-page PDF; source and publication hashes agree.'+(' Full prose, nearby figures, numbered headings, 20 ranking rows, 26 goal/condition labels, 10 dimensions, 29 indicators, seven themes and embedded CJK font verified.' if args.inspect_pdf else ''))
