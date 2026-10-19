"""A policy-facing executive summary: one manuscript, complete in web and PDF."""
import html,json
from pathlib import Path
import frontmatter_publication as publication
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/executive-summary.json').read_text())
E=lambda value:html.escape(str(value),quote=True)

def paragraphs(lang):
    """Canonical ordered prose; no interface instructions or chart-dependent claims."""
    yield 'headline',DATA['headline'][lang]
    yield 'lead',DATA['lead'][lang]
    yield 'body',DATA['thesis'][lang]
    yield 'heading',DATA['findings_title'][lang]
    for item in DATA['findings']:
        yield 'finding',(item['id'],item['title'][lang],item['body'][lang])
    yield 'heading',DATA['priorities_title'][lang]
    yield 'body',DATA['priorities_intro'][lang]
    for item in DATA['priorities']:
        yield 'priority',(item['id'],item['title'][lang],item['body'][lang])
    yield 'closing',DATA['closing'][lang]
    yield 'scope',DATA['scope'][lang]

def render(lang):
    t=lambda z,e:z if lang=='zh' else e
    out=['<article class="executive-summary" lang="'+('zh-CN' if lang=='zh' else 'en')+'">']
    out+=['<section class="es-opening" id="summary-1"><h2>'+E(DATA['headline'][lang])+'</h2><p class="es-lead">'+E(DATA['lead'][lang])+'</p><p>'+E(DATA['thesis'][lang])+'</p></section>']
    out+=['<section class="es-section" id="summary-2"><h2>'+E(DATA['findings_title'][lang])+'</h2>']
    for f in DATA['findings']:
        out+=['<div class="es-finding" id="es-panel-'+f['id']+'"><h3>'+E(f['title'][lang])+'</h3><p>'+E(f['body'][lang])+'</p></div>']
    out+=['</section><section class="es-section" id="summary-3"><h2>'+E(DATA['priorities_title'][lang])+'</h2><p>'+E(DATA['priorities_intro'][lang])+'</p>']
    for f in DATA['priorities']:
        out+=['<div class="es-priority"><h3>'+E(f['title'][lang])+'</h3><p>'+E(f['body'][lang])+'</p></div>']
    out+=['</section><section class="es-conclusion" id="summary-4"><p class="es-closing">'+E(DATA['closing'][lang])+'</p><p class="es-scope">'+E(DATA['scope'][lang])+'</p></section></article>']
    out+=['<nav class="es-reading-links" aria-label="'+t('继续阅读','Continue reading')+'"><a href="/2026/'+lang+'/introduction/">'+t('引言 · 共同愿景 →','Introduction · Shared vision →')+'</a><a href="/2026/'+lang+'/">'+t('全书目录 →','Contents →')+'</a></nav>']
    return ''.join(out)+publication.download(lang)

def manuscript(lang):
    lines=['# '+('执行摘要' if lang=='zh' else 'Executive summary')]
    for kind,value in paragraphs(lang):
        if kind=='headline':lines.append('## '+value)
        elif kind=='heading':lines.append('## '+value)
        elif kind in ['finding','priority']:lines+=['### '+value[1],value[2]]
        else:lines.append(value)
    return '\n\n'.join(lines)+'\n'
