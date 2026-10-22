"""Rebuild source-backed publication PDFs for local and Actions builds."""
from pathlib import Path
from urllib.request import urlopen,Request
import hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
PIN='523d033d6cb47f4a80c58a35753646f5c3608a78'
URL='https://raw.githubusercontent.com/notofonts/noto-cjk/'+PIN+'/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf'
work=ROOT/'tmp/publication-fonts';work.mkdir(parents=True,exist_ok=True)
font=work/'NotoSansCJKsc-Regular.otf'
if not font.exists():
 with urlopen(Request(URL,headers={'User-Agent':'GOSD-publication'}),timeout=90) as response:font.write_bytes(response.read())
assert font.read_bytes()[:4]==b'OTTO','Expected the pinned OpenType font'
print('Font commit:',PIN,'SHA256:',hashlib.sha256(font.read_bytes()).hexdigest(),flush=True)
for name in ['appendix_print.py','frontmatter_print.py']:
 subprocess.run([sys.executable,str(ROOT/'preview/web'/name),'--font',str(font)],cwd=ROOT,check=True)
