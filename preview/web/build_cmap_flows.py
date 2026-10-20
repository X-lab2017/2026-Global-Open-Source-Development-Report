"""Measured sample values stay immutable; only the common visual scale changes."""
import csv,json
def build_flows(base,countries,legacy):
    codes={'China':'CN','United States':'US','Canada':'CA','Germany':'DE','Singapore':'SG','India':'IN','Czechia':'CZ','Sweden':'SE','Bulgaria':'BG','United Kingdom':'GB','France':'FR','Netherlands':'NL','Switzerland':'CH','Poland':'PL'}
    raw=list(csv.DictReader((base/'source/repository-project-sources.csv').open()))
    edges=[dict(id=f'flow-{i+1:02}',source=codes[r['developer_country']],target=codes[r['project_country']],value=float(r['openrank']),share_pct=float(r['share_pct']),kind='observed',period='2026 report year',display=True) for i,r in enumerate(raw)]
    targets={}
    for target in ['CN','US']:
        rr=[r for r in edges if r['target']==target];local=next(r for r in rr if r['source']==target)
        share=round(sum(r['share_pct'] for r in rr),2)
        targets[target]=dict(observed_value=round(sum(r['value'] for r in rr),2),observed_share_pct=share,unlisted_share_pct=round(100-share,2),local_value=local['value'],local_share_pct=local['share_pct'],cross_border_listed_value=round(sum(r['value'] for r in rr if r['source']!=target),2))
    result=dict(period={'reportYear':2026,'start':'2025-07-01','endExclusive':'2026-07-01'},edges=edges,targets=targets,
        report_values={'CN':float(legacy[-1]['China']),'US':float(legacy[-1]['United States']),'IN':float(legacy[-1]['India'])},
        enhancement={'default_multiplier':3,'allowed_multipliers':[1,3],'operation':'uniform_visual_width_scale','formula':'render_width = common_multiplier * base_width(value)','preserves':['source','target','value','share_pct','edge_count'],'adds_observations':False},
        source='source/repository-project-sources.csv',
        scope='2026报告年度中美项目贡献来源前十样本；20条表列关系，14个来源国家。未列来源保留为份额，不分配到任何国家。',
        method='所有节点来自原表国家，所有连线来自原表关系。本土贡献用同国回环表示。增强模式将每条线的视觉宽度统一乘以3；数值、份额、方向和关系数不变。光点仅表示流向，不代表新增开发者或事件。',
        legend='蓝色：中国项目；青色：美国项目。箭头从开发者所在地指向项目归属地；同国回环表示本土贡献。')
    (base/'flows.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    with (base/'flows.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(edges[0]),lineterminator='\n');w.writeheader();w.writerows(edges)
    return result
