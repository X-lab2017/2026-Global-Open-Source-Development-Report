"""Section 4.1 uses the pinned report theme, including detached dialog surfaces."""
import goso_brand as B

def mix(a,b,weight):
    aa=[int(a[i:i+2],16) for i in (1,3,5)]
    bb=[int(b[i:i+2],16) for i in (1,3,5)]
    return '#'+''.join(f'{round(x*weight+y*(1-weight)):02X}' for x,y in zip(aa,bb))

def tokens(theme):
    v=B.values(theme)
    out={'--gv-'+k:value for k,value in v.items()}
    agent=B.TOKENS['themes'][theme]['fills' if theme=='light' else 'acc'][2]
    out.update({'--al-agent':agent,'--al-model':v['brand'],'--al-up':v['cyan'],
                '--al-down':v['s6'],'--al-soft-selection':v['raised']})
    for name,accent in [('agent',agent),('model',v['brand'])]:
        out['--al-'+name+'-soft']=mix(accent,v['surface'],.08 if theme=='light' else .09)
        out['--al-'+name+'-line']=mix(accent,v['line'],.40)
    return out

def export(out):
    blocks=[]
    for theme in ['light','dark']:
        prefix='' if theme=='light' else '[data-theme="dark"] '
        selector=','.join(prefix+s for s in ['.al-chapter','#al-fullscreen','#al-project-dialog'])
        blocks.append(selector+'{'+''.join(k+':'+v+';' for k,v in tokens(theme).items())+'}')
    blocks.append('''
.al-atlas-panel{--atlas-accent:var(--al-agent);--atlas-soft:var(--al-agent-soft);--atlas-line:var(--al-agent-line);--atlas-up:var(--al-up);--atlas-down:var(--al-down)}
#al-model.al-atlas-panel{--atlas-accent:var(--al-model);--atlas-soft:var(--al-model-soft);--atlas-line:var(--al-model-line)}
''')
    (out/'landscape-theme.css').write_text('\n'.join(blocks))
