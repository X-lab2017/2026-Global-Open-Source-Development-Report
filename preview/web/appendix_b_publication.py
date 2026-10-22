"""Appendix B publication metadata shared by the reader and downloads."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[2]
EDITION='2026-10-22-openness'
PDF_NAME='GOSD-2026-appendix-b.pdf'
DIRECTORY=ROOT/'preview/content/report-assets/appendix-b'
PDF_URL='/assets/report/appendix-b/'+PDF_NAME+'?v='+EDITION
def metadata():return json.loads((DIRECTORY/'edition-manifest.json').read_text())
def download(lang):
 t=lambda z,e:z if lang=='zh' else e
 m=metadata()
 return '<aside class="methods-download"><div><strong>'+t('附录 B · 离线阅读','Appendix B · Read offline')+'</strong><span>'+t('与网页使用同一正文','Chinese PDF from the same manuscript')+'</span></div><a href="'+html.escape(PDF_URL,quote=True)+'">'+t('下载 PDF · '+str(m['pages'])+' 页 ↓','Download PDF · '+str(m['pages'])+' pages ↓')+'</a></aside>'
