"""Two focused interactive replacements on the v0.12 reading edition."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1]
M=json.loads((R/'content/manifest.json').read_text())
E=lambda x:html.escape(str(x),quote=True)
def tr(lang,z,e):return z if lang=='zh' else e
def href(lang,c):return '/2026/'+lang+'/'+c['route']
def logic(lang,r,source):
 from report_architecture import render
 return render(lang)

def indicators(lang,r,source):
 t=lambda z,e:tr(lang,z,e);rows=r['indicators']
 out='<figure class="chapter-explorer osdi-explorer" id="fig-osdi-map" data-lang="'+lang+'"><div class="explorer-heading"><div><span class="eyebrow">OSDI / INDICATOR EXPLORER</span><h3>'+t('一眼看全貌，逐层看指标','See the whole, explore the detail')+'</h3><p>'+t('左侧看全貌，右侧看指标。点击切换，画面保持不变。','Overview on the left, indicators on the right. Explore without scrolling.')+'</p></div><button class="osdi-reset" type="button" hidden>'+t('返回全貌','Reset overview')+'</button></div><div class="osdi-levels" aria-label="'+t('目标、维度、指标','Goals, dimensions and indicators')+'"><span><b>4</b>'+t('大支柱 · 目标','pillars · goals')+'</span><i aria-hidden="true">→</i><span><b>10</b>'+t('个维度 · 研究领域','dimensions · research areas')+'</span><i aria-hidden="true">→</i><span><b>29</b>'+t('项指标 · 具体观察','indicators · observations')+'</span></div><div class="osdi-overview">'
 for pi in range(1,5):
  group=[x for x in rows if x['pillar_id']=='X'+str(pi)];dims=list(dict.fromkeys(x['dimension_id'] for x in group));p=group[0]
  out+='<section class="osdi-pillar pillar-'+str(pi)+'"><button type="button" class="osdi-pillar-button" data-osdi-pillar="X'+str(pi)+'" aria-controls="osdi-detail" aria-pressed="false"><small>X'+str(pi)+'</small><strong>'+E(p['pillar_name_zh' if lang=='zh' else 'pillar_name_en'])+'</strong><span>'+str(len(dims))+t('维度',' dimensions')+' · '+str(len(group))+t('指标',' indicators')+'</span></button><div class="osdi-dimensions">'
  for dim in dims:
   items=[x for x in group if x['dimension_id']==dim];out+='<button type="button" data-osdi-dimension="'+dim+'" aria-pressed="false" aria-controls="osdi-detail"><small>'+dim+'</small><strong>'+E(items[0]['dimension_name_zh' if lang=='zh' else 'dimension_name_en'])+'</strong><span>'+str(len(items))+t('项',' measures')+' <i aria-hidden="true">＋</i></span></button>'
  out+='</div></section>'
 out+='</div><div class="osdi-detail" id="osdi-detail"><div class="osdi-breadcrumb" role="status">'+t('全貌 · 选择上方任一维度，查看对应指标','Overview · select a dimension above to view its indicators')+'</div><div class="osdi-empty">'+t('目标说明方向，维度组织问题，指标定义观察。','Goals set direction; dimensions organize questions; indicators define observations.')+'</div><div class="osdi-indicator-list" hidden>'
 for row in rows:
  code=row['indicator_code'];out+='<details class="osdi-measure" data-osdi-code="'+code+'" data-pillar="'+row['pillar_id']+'" data-dimension="'+row['dimension_id']+'" hidden><summary><span><b>'+E(row['indicator_name_zh'] if lang=='zh' else code)+'</b><small>'+E(code)+'</small></span><em>'+E(row['role'])+'</em><i aria-hidden="true">＋</i></summary><div class="osdi-measure-body"><p>'+E(row['definition'])+'</p><dl><dt>'+t('计算口径','Calculation')+'</dt><dd>'+E(row['calculation_rule'])+'</dd><dt>'+t('单位','Unit')+'</dt><dd>'+E(row['unit'])+'</dd><dt>'+t('SDG关联','SDG links')+'</dt><dd>'+E(row['sdg_links'])+'</dd></dl><details class="osdi-evidence"><summary>'+t('数据状态与方法边界','Evidence and methodology')+'</summary><p>'+E(row['data_status'])+'</p><p>'+E(row['remaining_evidence'])+'</p><p>'+E(row['period_rule'])+'；'+E(row['missing_rule'])+'</p></details></div></details>'
 out+='</div></div><div class="osdi-foot-tools"><button type="button" class="osdi-all" hidden>'+t('查看全部29项指标','View all 29 indicators')+'</button><a href="/assets/report/osdi_indicator_dictionary.csv" download>'+t('下载完整指标表 CSV ↓','Download indicator table CSV ↓')+'</a></div><figcaption>'+t('图 1-3-1 · OSDI三级结构与指标探索。目标—维度—指标不表示计算权重；资料入库不等于测算完成。','Figure 1-3-1 · Explore the three-level structure. Levels do not imply weights; available files do not mean completed measurements.')+'</figcaption><noscript><style>.osdi-explorer .osdi-indicator-list[hidden],.osdi-explorer .osdi-measure[hidden]{display:block!important}.osdi-explorer .osdi-empty{display:none}</style></noscript></figure>'
 out+='<script type="application/json" id="osdi-review-evidence">'+json.dumps(json.loads((R/'content/chapter1-evidence.json').read_text()),ensure_ascii=False).replace('<','\\u003c')+'</script>'
 return out
