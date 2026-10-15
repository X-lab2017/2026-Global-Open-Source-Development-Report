"""Observed project samples plus an explicit, reproducible residual-source scenario."""
from pathlib import Path
import csv, json

def build_flows(base,countries,legacy):
    by={r['id']:r for r in countries}
    codes={'China':'CN','United States':'US','Canada':'CA','Germany':'DE','Singapore':'SG','India':'IN','Czechia':'CZ','Sweden':'SE','Bulgaria':'BG','United Kingdom':'GB','France':'FR','Netherlands':'NL','Switzerland':'CH','Poland':'PL'}
    raw=list(csv.DictReader((base/'source/repository-project-sources.csv').open()))
    edges=[dict(source=codes[r['developer_country']],target=codes[r['project_country']],value=float(r['openrank']),share_pct=float(r['share_pct']),kind='observed',period='2026 report table',display=True) for r in raw]
    targets={}
    for target in ['CN','US']:
        rr=[r for r in edges if r['target']==target];total=sum(r['value'] for r in rr);share=round(sum(r['share_pct'] for r in rr),2)
        # Shares are rounded in the original; this is an approximate inferred denominator.
        inferred_total=total/(share/100);residual=inferred_total-total
        excluded={r['source'] for r in rr};candidates=[r for r in countries if r['id'] not in excluded and r['value']>0]
        weights=sum(r['value'] for r in candidates)
        estimates=[dict(source=r['id'],target=target,value=residual*r['value']/weights,share_pct=(100-share)*r['value']/weights,kind='estimated',period='illustrative scenario: 2026 residual weighted by 2025 GitHub contribution',display=False) for r in candidates]
        estimates.sort(key=lambda r:-r['value'])
        geo_estimates=[r for r in estimates if by[r['source']]['coordinates']]
        top_sources={r['source'] for r in geo_estimates[:12]}
        visible=[r for r in geo_estimates if r['source'] in top_sources or r['source'] in ['BR','ID','VN','PH','EG','ZA']]
        for r in visible:r['display']=True
        edges.extend(estimates)
        targets[target]=dict(observed_value=round(total,2),observed_share_pct=share,residual_share_pct=round(100-share,2),estimated_full_sample=inferred_total,estimated_residual=residual,displayed_estimates=len(visible),displayed_estimate_value=sum(r['value'] for r in visible))
    report_values={'CN':float(legacy[-1]['China']),'US':float(legacy[-1]['United States']),'IN':float(legacy[-1]['India'])}
    result=dict(observed_period='2026 report table; project sample scope pending',targets=targets,edges=edges,report_values=report_values,
        method='对各目的地：表列前十贡献合计 ÷ 前十份额合计，近似推得样本分母；剩余份额按未列来源的 2025 GitHub 开发者贡献权重分配。该跨期权重仅是情景假设，含原表份额舍入误差；不代表实测流量、完整全球网络或未来预测。显示每个目的地最强 12 条估算边并纳入全球南方六国；选线不改变权重，其余保留下载。未另行推算其他目的地。',
        legend='实线＝2026表列来源；金色虚线＝未列来源估算；粗细与光点方向表达样本贡献规模与开发者来源→项目归属，不表示人员迁移。',
        scope='国家汇总点：报告2026仅有中、美、印独立国家值，其他国家留空；GitHub2025视图保留236地区原值。国家点与项目样本边的统计总体不同，不要求流量与节点总量守恒。',
        source='source/repository-project-sources.csv')
    (base/'flows.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    with (base/'flows.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['source','target','value','share_pct','kind','period','display'],lineterminator='\n');w.writeheader();w.writerows(edges)
    return result
