"""Assemble chapter 3 locally; retain reviewed figure pages and add continuous navigation.

This command never copies PDFs into deployment assets or the Git repository.
"""
from pathlib import Path
import argparse,json,hashlib
import fitz
import region_publication as opening

EDITION='2026-10-21-chapter3-publication-v2'
FILES=['GOSD-2026-Chapter3-Opening-Section3-1-Review-20261021.pdf']+[f'GOSD-2026-Section3-{i}-Review-20261021.pdf' for i in range(2,7)]
MODULES=['region','company','foundation','project','emerging','model']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=Path('output/pdf'));ap.add_argument('--output',type=Path,default=Path('output/pdf/GOSD-2026-Chapter3-Review-20261021.pdf'));a=ap.parse_args()
 a.output.parent.mkdir(parents=True,exist_ok=True);work=Path('tmp/pdfs/chapter3');work.mkdir(parents=True,exist_ok=True)
 doc=fitz.open();toc=[[1,opening.CHAPTER_TITLE,1]];parts=[]
 for i,(name,module) in enumerate(zip(FILES,MODULES),1):
  p=a.input_dir/name;source=fitz.open(p);offset=len(doc);mod=__import__(module+'_publication')
  doc.insert_pdf(source,links=True,annots=True)
  local_toc=source.get_toc();section_page=next(page for level,title,page in local_toc if title.startswith(f'3.{i} '))
  for level,title,page in local_toc:
   if i==1 and page<section_page:continue
   toc.append([level+1,title,page+offset])
  parts.append({'section':f'3.{i}','title':mod.TITLE,'file':name,'edition':getattr(__import__(module+'_print'),'EDITION',mod.EDITION),'manuscript_edition':mod.EDITION,'start_page':offset+section_page,'pages':len(source),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  source.close()
 # Replace the local folio, including underlying text, without altering page artwork.
 for n,page in enumerate(doc,1):
  w,h=page.rect.width,page.rect.height;page.add_redact_annot(fitz.Rect(w-78,h-39,w-37,h-18),fill=(1,1,1));page.apply_redactions(images=0,graphics=0)
  label=str(n);size=8.2;page.insert_text((w-46-fitz.get_text_length(label,fontname='helv',fontsize=size),h-28),label,fontsize=size,fontname='helv',color=(.36,.44,.48))
 # The existing six-topic guide doubles as a compact, clickable contents page.
 page=doc[0]
 for i,((code,_,_),part) in enumerate(zip(opening.CHAPTER_TOPICS,parts),1):
  hits=page.search_for(f'3.{i} {code}-Ranking');assert len(hits)==1,(i,hits)
  hit=hits[0];right=page.rect.width-46 if i%2==0 else 46+(page.rect.width-92-24)/2
  label='p. '+str(part['start_page']);page.insert_text((right-fitz.get_text_length(label,fontname='helv',fontsize=8.2),hit.y1-1),label,fontsize=8.2,fontname='helv',color=(.36,.44,.48))
  page.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(hit.x0,hit.y0-6,right,hit.y1+38),'page':part['start_page']-1,'to':fitz.Point(0,0)})
 doc.set_toc(toc);doc.set_page_labels([{'startpage':0,'prefix':'','style':'D','firstpagenum':1}]);doc.set_metadata({'title':opening.CHAPTER_TITLE,'author':'GOSD 报告编制组','subject':'第三章完整出版审阅稿；六节同源正文、原始图件、连续页码与书签','keywords':'GOSD,GOSR,2026,OpenRank,ModelRank','creator':'GOSD publication workflow'})
 doc.save(a.output,garbage=4,deflate=True)
 manifest={'edition':EDITION,'pdf':a.output.name,'pages':len(doc),'sections':parts,'bookmarks':len(toc),'contents_links':6,'pdf_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest()}
 (work/'publication-spec.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
