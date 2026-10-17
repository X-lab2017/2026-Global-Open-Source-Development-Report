"""Pinned osdg-brand tokens; native SVG adapter for the GOSO report."""
from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE='7fe12a5b03698df25be3d56e31aa8e9777febe1b'
TOKENS=json.loads((ROOT/'content/brand/visual-tokens-v5.json').read_text())
SERIES={'light':['#156993','#279FA9','#4E87C5','#9973B7','#5C8A3C','#C08A2D','#8C5B3F','#6B7F8C'],'dark':['#76D5E4','#68C8CC','#77A9DE','#AD8ACC','#A0C86C','#F2D15C','#E8A06A','#8FA9BB']}
BANDS={'light':['#DCEBF2','#BCD8E4','#8FBFD3','#5B9FBE','#337FA6','#156993'],'dark':['#123750','#1C5A7A','#2A7D9C','#3FA3B8','#68C8CC','#A0E6D8']}
def values(theme):
    t=dict(TOKENS['themes'][theme]);t.update({'empty':'#E0EBF0' if theme=='light' else '#123750','axis':'#B9CDD8' if theme=='light' else '#3A657D','split':'#DDE9EE' if theme=='light' else '#234E66'})
    t.update({f's{i}':c for i,c in enumerate(SERIES[theme])});t.update({f'm{i}':c for i,c in enumerate(BANDS[theme])});return {k:v for k,v in t.items() if isinstance(v,str)}
def css(key):return 'var(--gv-'+key+', '+values('light')[key]+')'
def resolve(text,theme='light'):
    vv=values(theme)
    return re.sub(r'var\(--gv-([\w]+),\s*#[0-9a-fA-F]{6}\)',lambda m:vv[m[1]],text)
def export(out):
    cssout=[]
    for theme in ['light','dark']:
        selector='.goso-chapter,.cr-stage' if theme=='light' else '[data-theme="dark"] .goso-chapter,[data-theme="dark"] .cr-stage'
        cssout.append(selector+'{'+''.join('--gv-'+k+':'+v+';' for k,v in values(theme).items())+'}')
    cssout.append((ROOT/'web/goso-brand.css').read_text())
    (out/'goso-brand.css').write_text('\n'.join(cssout))
    dest=out/'assets/goso-brand';shutil.copytree(ROOT/'content/brand',dest,dirs_exist_ok=True)
    (dest/'provenance.json').write_text(json.dumps({'repository':'X-lab2017/osdg-brand','commit':SOURCE,'adapter':'Native SVG; colors, themes, P95 and accessible controls. No React dependency.','series':SERIES,'map_bands':BANDS},ensure_ascii=False,indent=2))
