"""Attach the validated editable PPTX to the self-contained offline web deck."""
import base64,re,sys
from pathlib import Path
folder=Path(sys.argv[1])
pptx=folder/'GOSD-2026-Opening-Chapter1-Review-v2.pptx'
web=folder/'GOSD-2026-Opening-Chapter1-Review.html'
payload=base64.b64encode(pptx.read_bytes()).decode()
content,n=re.subn(r'(<script id="ppt-data" type="application/octet-stream">).*?(</script>)',lambda m:m[1]+payload+m[2],web.read_text(),count=1,flags=re.S)
assert n==1
web.write_text(content)
print('Attached validated PPTX; offline HTML has no network dependency.')
