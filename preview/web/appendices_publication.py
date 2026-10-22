"""Shared appendix reading links and the source-preserving A/B PDF bundle."""
from pathlib import Path
import hashlib,html,json
import appendix_publication as A
import appendix_b_publication as B
ROOT=Path(__file__).resolve().parents[2]
EDITION='2026-10-22-appendices'
DIRECTORY=ROOT/'preview/content/report-assets/appendices'
PDF_NAME='GOSD-2026-appendices-A-B.pdf'
PDF_URL='/assets/report/appendices/'+PDF_NAME+'?v='+EDITION
def metadata():return json.loads((DIRECTORY/'edition-manifest.json').read_text())
def companions(current,lang):
 t=lambda z,e:z if lang=='zh' else e
 route,label=('appendices/dpg/',t('附录 B · 开放条件与公共品','Appendix B · Openness and public goods')) if current=='a' else ('methodology/',t('附录 A · 指标、数据与方法','Appendix A · Measures, data and methods'))
 return '<nav class="appendix-companions" aria-label="'+t('附录阅读','Appendix reading')+'"><a href="/2026/'+lang+'/'+route+'">'+label+' →</a><a href="'+html.escape(PDF_URL,quote=True)+'">'+t('附录 A＋B 合订 PDF','Appendices A + B · Chinese PDF')+' ↓</a></nav>'
def main():
 from pypdf import PdfReader,PdfWriter
 DIRECTORY.mkdir(parents=True,exist_ok=True)
 writer=PdfWriter();parts=[]
 for letter,module in [('A',A),('B',B)]:
  meta=module.metadata();start=len(writer.pages);reader=PdfReader(module.DIRECTORY/module.PDF_NAME)
  writer.append(reader,import_outline=False)
  parent=writer.add_outline_item('附录 '+letter, start)
  for h in meta['headings']:writer.add_outline_item(h['text'],start+h['page']-1,parent=parent)
  writer.set_page_label(start,len(writer.pages)-1,style='/D',prefix=letter+'-',start=1)
  parts.append({'appendix':letter,'start_page':start+1,'pages':meta['pages'],'edition':meta['edition'],'pdf_sha256':meta['pdf_sha256'],'source_sha256':meta['source_sha256']})
 writer.add_metadata({'/Title':'2026 全球开源发展报告 · 附录 A、B','/Author':'GOSD / 全球开源发展报告','/Subject':'指标、数据与研究方法；模型开放条件与数字公共品研究参照'})
 pdf=DIRECTORY/PDF_NAME
 with pdf.open('wb') as stream:writer.write(stream)
 meta={'edition':EDITION,'pdf_file':PDF_NAME,'pages':len(writer.pages),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'parts':parts}
 (DIRECTORY/'edition-manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(meta,ensure_ascii=False))
if __name__=='__main__':main()
