"""Emit small rendered-page images for publication review from remote builds."""
from pathlib import Path
import base64
import fitz
import appendix_publication as A
import appendix_b_publication as B
ROOT=Path(__file__).resolve().parents[2]
def emit(name,data):print('REVIEW_IMAGE_'+name+' '+base64.b64encode(data).decode(),flush=True)
for letter,module in [('A',A),('B',B)]:
 for i,page in enumerate(fitz.open(module.DIRECTORY/module.PDF_NAME)):
  emit('PDF_'+letter+'_'+str(i+1),page.get_pixmap(matrix=fitz.Matrix(1.1,1.1)).tobytes('png'))
qa=ROOT/'tmp/publication-review'
for name in ['view-a-zh-1440-light','view-b-zh-1440-light','view-b-zh-390-light','view-b-zh-1440-dark','view-b-en-390-dark','view-b-standard-1440','view-b-standard-390']:
 emit(name,(qa/(name+'.png')).read_bytes())
