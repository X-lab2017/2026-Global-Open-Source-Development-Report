"""Reviewed I/T maps, built through the same portal as V/C maps.

Authoring fragments and pinned snapshots live under content/. No source data in
the report repository is overwritten. Synthetic T-Map records stay separate.
"""
from pathlib import Path
import json, re, shutil
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

def section(key, lang='zh'):
    text = (ROOT/'content'/key/'section.html').read_text()
    return text.replace('/2026/zh/', '/2026/'+lang+'/')

def export(out):
    geometry = json.loads((ROOT/'content/vmap/map-geometry.json').read_text())
    for key in ('imap', 'tmap'):
        shutil.copytree(ROOT/'content'/key, out/'assets'/key, dirs_exist_ok=True, ignore=shutil.ignore_patterns('section.html'))
        (out/'assets'/key/'section.html').unlink(missing_ok=True)
        data = json.loads((ROOT/'content'/key/'observations.json').read_text())
        data['geometry'] = geometry['world'] if key == 'imap' else geometry
        if key == 'imap':
            data['snapshot'] = json.loads((ROOT/'content/imap/influence.json').read_text())
        js = 'window.'+key.upper()+'_DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'
        if key == 'tmap':
            js += 'window.TMAP_SIM='+(ROOT/'content/tmap/simulation.json').read_text().strip()+';\n'
        (out/'assets'/key/'data.js').write_text(js)
    for name in ('imap.css','imap.js','tmap.css','tmap.js','goso-map-system.css'):
        shutil.copy2(ROOT/'web'/name, out/name)

class Prose(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth=0; self.skip=0; self.chunks=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('figure','dialog','script','style','noscript'):
            self.skip+=1
        if not self.skip and tag in ('h2','h3','h4','p','summary','li'):
            self.chunks.append('\n\n'+({'h2':'## ','h3':'### ','h4':'#### '}.get(tag,'')))
    def handle_endtag(self, tag):
        if tag in ('figure','dialog','script','style','noscript'): self.skip=max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip:self.chunks.append(data)

def manuscript(key):
    parser=Prose(); parser.feed(section(key))
    return '\n'.join(line.rstrip() for line in ''.join(parser.chunks).strip().splitlines())
