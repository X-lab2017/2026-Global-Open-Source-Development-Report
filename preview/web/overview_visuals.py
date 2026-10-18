"""Decorative, data-free navigation cues for the report overview."""

ICONS = {
    'overview': '<circle cx="12" cy="12" r="8.5"/><path d="m15.6 8.4-2.2 5-5 2.2 2.2-5Z"/>',
    'sequence': '<path d="M12 6C9 3.5 5.5 3.5 2.5 4.5v14C6 17.5 9 18 12 20c3-2 6-2.5 9.5-1.5v-14C18.5 3.5 15 3.5 12 6Zm0 0v14M6 8l3 1m6 0 3-1"/>',
    'topic': '<circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6M7 8h6m-6 4h4"/>',
    'goso': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
    'gosr': '<path d="M3 20h18M4 20V10h5v10m0 0V4h6v16m0 0v-7h5v7"/>',
    'gosl': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    'gosm': '<path d="m12 3 9 5-9 5-9-5 9-5Zm-9 9 9 5 9-5M3 16l9 5 9-5"/>',
    'data': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v7c0 4 16 4 16 0V5M4 12v7c0 4 16 4 16 0v-7"/>',
    'presentation': '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="m10 7 5 3-5 3V7Zm2 10v4m-4 0h8"/>',
    'release': '<path d="M7 3H4v18h16V8l-5-5H7Zm8 0v5h5M12 10v7m-3-3 3 3 3-3"/>',
    'action': '<circle cx="12" cy="12" r="8.5"/><path d="m7.5 12 3 3 6-6"/>',
    'together': '<circle cx="8" cy="7" r="3"/><path d="M2 20v-3a6 6 0 0 1 12 0v3m2-16a3 3 0 0 1 0 6m2 4a5 5 0 0 1 4 5v1"/>',
}


def icon(kind, css='overview-icon'):
    return f'<svg class="{css}" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">{ICONS[kind]}</svg>'


def flow(path, delay=0):
    return f'<path class="ov-track" d="{path}"/><path class="ov-flow" pathLength="100" style="--cue-delay:-{delay}s" d="{path}"/>'


def art(kind):
    view='0 0 200 100'
    if kind=='goso':
        drawing='<g class="ov-track"><circle cx="100" cy="50" r="38"/><ellipse cx="100" cy="50" rx="18" ry="38"/><path d="M62 50h76M70 28h60M70 72h60"/></g>'
        drawing+=flow('M72 64Q103 6 128 37',1)+flow('M71 29Q88 83 126 67',4)
        drawing+='<g class="ov-dot"><circle cx="72" cy="64" r="3"/><circle cx="128" cy="37" r="3"/><circle cx="71" cy="29" r="2.5"/><circle cx="126" cy="67" r="2.5"/></g>'
    elif kind=='gosr':
        drawing='<path class="ov-track" d="M29 82h143"/>'
        for i,(x,y,h) in enumerate([(35,48,34),(80,22,60),(125,59,23)]):
            drawing+=f'<rect class="ov-panel ov-highlight" style="--cue-delay:-{i*2.4}s" x="{x}" y="{y}" width="35" height="{h}" rx="4"/>'
        drawing+='<path class="ov-ink" d="m92 35 5 3 5-3-1 8h-8Z"/>'+flow('M35 29C52 29 59 11 76 11H154',2)
    elif kind=='gosl':
        drawing=flow('M29 49H170',1)+'<path class="ov-track" d="M70 27v46M130 27v46"/>'
        for i,(x,y,w) in enumerate([(20,15,45),(76,15,48),(135,15,45),(20,60,64),(95,60,30),(136,60,44)]):
            drawing+=f'<rect class="ov-panel ov-highlight" style="--cue-delay:-{i*1.2}s" x="{x}" y="{y}" width="{w}" height="25" rx="4"/><path class="ov-quiet" d="M{x+9} {y+12}h{w-18}"/>'
    elif kind=='gosm':
        drawing=flow('M61 50H98Q110 50 110 26H141',1)+flow('M61 50H141',3)+flow('M61 50H98Q110 50 110 74H141',5)
        drawing+='<rect class="ov-panel" x="23" y="33" width="38" height="34" rx="6"/><path class="ov-ink" d="m33 44 9-5 9 5-9 5-9-5m0 7 9 5 9-5"/>'
        for i,y in enumerate([14,38,62]):drawing+=f'<rect class="ov-panel ov-highlight" style="--cue-delay:-{i*2.4}s" x="141" y="{y}" width="35" height="24" rx="4"/><path class="ov-quiet" d="M151 {y+12}h15"/>'
    elif kind=='action':
        drawing=''.join(flow(f'M27 {y}H53Q77 {y} 77 50H113',i*2.4) for i,y in enumerate([20,50,80]))
        drawing+=''.join(f'<circle class="ov-panel" cx="20" cy="{y}" r="7"/>' for y in [20,50,80])
        for i in range(9):drawing+=f'<rect class="ov-panel ov-highlight" style="--cue-delay:-{i*.8}s" x="{116+i%3*23}" y="{19+i//3*23}" width="16" height="16" rx="3"/>'
    elif kind=='together':
        drawing='<ellipse class="ov-track" cx="100" cy="50" rx="72" ry="33"/><ellipse class="ov-track" cx="100" cy="50" rx="38" ry="45"/><circle class="ov-panel" cx="100" cy="50" r="14"/><path class="ov-ink" d="m94 50 4 4 8-8"/>'
        for i,p in enumerate(['M28 50Q58 6 100 36','M172 50Q143 96 100 64','M78 14Q124 2 133 29']):drawing+=flow(p,i*2.4)
        drawing+='<g class="ov-dot"><circle cx="28" cy="50" r="4"/><circle cx="172" cy="50" r="4"/><circle cx="78" cy="14" r="3.5"/><circle cx="128" cy="81" r="3.5"/></g>'
    else:
        view='0 0 320 80'
        if kind=='data':
            drawing='<rect class="ov-panel" x="12" y="10" width="106" height="60" rx="5"/><path class="ov-track" d="M12 30h106M12 50h106M45 10v60M81 10v60"/>'
            drawing+=flow('M118 40H216',1)+'<circle class="ov-panel ov-highlight" cx="248" cy="40" r="24"/><path class="ov-ink" d="m237 40 7 7 15-16"/>'
        elif kind=='presentation':
            drawing='<rect class="ov-panel" x="68" y="8" width="180" height="56" rx="5"/><path class="ov-track" d="M158 64v10m-24 0h48"/><path class="ov-ink" d="m148 24 23 12-23 12V24Z"/>'
            drawing+=flow('M83 57H232',1)
            for i,x in enumerate([22,284]):drawing+=f'<path class="ov-quiet" d="M{x} 25v23m7-18v13"/>'
        else:
            drawing='<rect class="ov-track" x="23" y="7" width="54" height="55" rx="4"/><rect class="ov-panel" x="15" y="14" width="54" height="55" rx="4"/><path class="ov-quiet" d="M26 29h28M26 41h21M26 53h26"/>'
            drawing+=flow('M69 40H207',1)+'<path class="ov-panel" d="M216 23h72v43h-72Z"/><path class="ov-ink" d="M252 12v36m-8-8 8 8 8-8M231 57h42"/>'
    return f'<svg class="overview-art overview-art-{kind}" viewBox="{view}" aria-hidden="true" focusable="false">{drawing}</svg>'
