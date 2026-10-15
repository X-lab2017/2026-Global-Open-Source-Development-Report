"""Reproduce OpenShare's public GeoJSON map layout (ECharts default aspectScale=.75).
No reprojection or independent horizontal/vertical fitting. Source outlines are retained.
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'content/vmap';SOURCE=ASSET/'source'
ASPECT=.75
VIEW=[880,470];PADDING=[24,18,24,60]

def points(value):
    if isinstance(value,list) and len(value)>=2 and isinstance(value[0],(int,float)):
        yield value[:2]
    else:
        for child in value:yield from points(child)

def centroid(ring):
    area=0;x=0;y=0
    for a,b in zip(ring,ring[1:]+ring[:1]):
        cross=a[0]*b[1]-b[0]*a[1];area+=cross;x+=(a[0]+b[0])*cross;y+=(a[1]+b[1])*cross
    if abs(area)<1e-10:return 0,ring[0][:2]
    return abs(area),[x/(3*area),y/(3*area)]

def in_ring(point,ring):
    x,y=point;inside=False
    for a,b in zip(ring,ring[1:]+ring[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:inside=not inside
    return inside

def build():
    data=json.loads((ASSET/'fig-2-1-2_platform-coverage.json').read_text());by_name={r['en']:r for r in data['countries']};by_code={r['id']:r for r in data['countries']}
    aliases={'Aland':'AX','Cape Verde':'CV','Swaziland':'SZ','S. Geo. and S. Sandw. Is.':'GS'}
    out={};spec={'reference':'https://open-share.com/insight/open-world/gosd','aspect_scale':ASPECT,'projection':'No custom projection. Longitude/latitude affine layout with ECharts geoJSON aspectScale 0.75.','viewport':VIEW,'padding':PADDING,'shape_simplification':False,'scopes':{}}
    for scope,name in [('world','world.json'),('china','CN.json')]:
        raw=(SOURCE/name).read_bytes();geo=json.loads(raw);features=geo['features'];allpts=list(points([f['geometry']['coordinates'] for f in features]));xs=[p[0] for p in allpts];ys=[p[1] for p in allpts];bounds=[min(xs),min(ys),max(xs),max(ys)]
        w=(bounds[2]-bounds[0])*ASPECT;h=bounds[3]-bounds[1];aw=VIEW[0]-PADDING[0]-PADDING[2];ah=VIEW[1]-PADDING[1]-PADDING[3];scale=min(aw/w,ah/h);ox=PADDING[0]+(aw-w*scale)/2;oy=PADDING[1]+(ah-h*scale)/2
        def project(lon,lat):return [round(ox+(lon-bounds[0])*ASPECT*scale,3),round(oy+(bounds[3]-lat)*scale,3)]
        records=[]
        for index,f in enumerate(features):
            prop=f['properties'];g=f['geometry'];lines=g['type'] in ('LineString','MultiLineString');name_=prop.get('name','')
            if scope=='world':
                row=by_name.get(name_) or by_code.get(aliases.get(name_));code=row['id'] if row else 'geometry-'+str(index);label=row['name'] if row else {'N. Cyprus':'塞浦路斯北部','Siachen Glacier':'锡亚琴冰川'}.get(name_,name_ or '未标注地区')
            else:
                code=prop.get('code') or ('100000_JDX' if lines else '100000_JD');label=prop.get('fullname',name_)
            if g['type']=='Polygon':rings=g['coordinates']
            elif g['type']=='MultiPolygon':rings=[ring for poly in g['coordinates'] for ring in poly]
            elif g['type']=='MultiLineString':rings=g['coordinates']
            elif g['type']=='LineString':rings=[g['coordinates']]
            else:raise ValueError(g['type'])
            paths=[]
            for ring in rings:
                paths.append('M'+'L'.join(','.join(map(str,project(*xy[:2]))) for xy in ring)+('' if lines else 'Z'))
            center=prop.get('center')
            if not center:
                _,center=max((centroid(r) for r in rings),key=lambda pair:pair[0])
            records.append({'id':code,'name':label,'en':name_,'d':''.join(paths),'center':project(*center),'kind':'line' if lines else 'polygon','source_feature':index})
        out[scope]=records;spec['scopes'][scope]={'geojson':name,'sha256':hashlib.sha256(raw).hexdigest(),'geographic_bounds':bounds,'shape_ratio':w/h,'uniform_scale':scale,'offset':[ox,oy],'source_features':len(features),'rendered_features':len(records)}
        if scope=='world':
            cn=next(f for f in features if f['properties']['name']=='China');assert any(in_ring([121,23.5],poly[0]) for poly in cn['geometry']['coordinates'] if poly),'Source world China must contain Taiwan'
            assert not any(r['id'] in ['TW','HK','MO'] for r in records)
        else:assert {'710000','810000','820000','100000_JD','100000_JDX'}.issubset({r['id'] for r in records})
    (ASSET/'map-geometry.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')))
    (ASSET/'map-provenance.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
    print('OpenShare geometry: world ratio %.6f / China ratio %.6f; original outlines, common .75 aspect, uniform fit.'%(spec['scopes']['world']['shape_ratio'],spec['scopes']['china']['shape_ratio']))
if __name__=='__main__':build()
