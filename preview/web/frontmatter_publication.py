"""Shared editorial copy and edition metadata for the report's opening pages."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[2]
EDITORIAL=json.loads((ROOT/'outline/frontmatter-editorial.json').read_text())
PDF_NAME='GOSD-2026-opening-and-chapter1.pdf'
EDITION='2026-10-22-two-appendices'
MANIFEST=ROOT/'preview/content/report-assets/frontmatter/edition-manifest.json'
WEB='https://www.x-lab.info/2026-Global-Open-Source-Development-Report/'
def copy(key,lang):return EDITORIAL[key][lang]
def download(lang):
 t=lambda z,e:z if lang=='zh' else e
 m=json.loads(MANIFEST.read_text())
 return '<aside class="front-print-edition"><div><strong>'+t('离线阅读 · 前置内容与第一章','Read offline · Opening pages and Chapter 1')+'</strong><p>'+html.escape(copy('pdf_scope',lang))+'</p></div><a href="/assets/report/frontmatter/'+PDF_NAME+'?v='+EDITION+'">'+t('下载 PDF · '+str(m['pages'])+' 页 ↓','Download PDF · '+str(m['pages'])+' pages ↓')+'</a></aside>'
