"""Two views in the original model story canvas; preserve both source scopes."""
from pathlib import Path
import json,gzip,html
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
def enhance(markup,lang):
 t=lambda z,e:z if lang=='zh' else e
 source='Qwen/Qwen2.5-7B';names=[source,source+'-Instruct',source+'-Instruct-1M','Qwen/Qwen2.5-Coder-7B','Qwen/Qwen2.5-Math-7B']
 data=json.loads(gzip.decompress((ROOT/'content/gosm/network.json.gz').read_bytes()));edges={(x['source'],x['target']) for x in data['edges']};assert all((source,n) in edges for n in names[1:])
 marker='<div class="model-readout">';start=markup.index(marker);bound=markup.index('<p class="viz-boundary">',start)
 tabs='<div class="model-story-tabs" role="group" aria-label="'+t('模型故事视角','Model story views')+'"><button type="button" data-model-story-view="macro" aria-controls="model-story-macro" aria-pressed="true">'+t('宏观趋势','Macro trends')+'</button><button type="button" data-model-story-view="qwen" aria-controls="model-story-qwen" aria-pressed="false">'+t('Qwen 实例','Qwen case')+'</button><span>'+t('从生态构成，走近一次具体的再创造','From ecosystem patterns to a concrete example')+'</span></div>'
 def node(i):
  name=names[i];display=name.split('/')[1]
  return '<button type="button" class="qwen-story-node '+('qwen-base' if i==0 else 'qwen-child')+'" data-qwen-node="'+str(i)+'" aria-controls="qwen-story-detail" aria-pressed="'+str(i==0).lower()+'"><small>'+t('基础模型' if i==0 else '直接下游','BASE MODEL' if i==0 else 'DIRECT DESCENDANT')+'</small><strong>'+E(display)+'</strong></button>'
 detail='<span class="viz-label">'+t('局部案例 · 选定 4 个直接下游','LOCAL CASE · FOUR SELECTED DESCENDANTS')+'</span><strong>Qwen2.5-7B</strong><p>'+t('一项基础模型被用于后续开发，新的发布面向不同用途。选择节点或连线，了解它们的联系。','A foundation model supports further releases for different uses. Select a node or edge to inspect the declaration.')+'</p><dl><dt>'+t('完整 ID','Full ID')+'</dt><dd>Qwen/Qwen2.5-7B</dd><dt>'+t('来源快照','Snapshot')+'</dt><dd>2026-10-16</dd><dt>'+t('关系含义','Edge meaning')+'</dt><dd>'+t('发布者声明的基础模型','Publisher-declared base model')+'</dd></dl><a class="inline-link" href="/2026/'+lang+'/chapters/05/#ch05-s02">'+t('进入 5.2 完整网络 →','Explore the full network in 5.2 →')+'</a>'
 case='<section id="model-story-qwen" class="qwen-story-panel" data-model-story-panel="qwen" hidden><div class="qwen-story-graph"><div class="qwen-graph-label">'+t('一次发布，连接多种后续创造','One release, several subsequent creations')+'</div><svg viewBox="0 0 760 480" aria-hidden="true">'
 for y in [90,198,306,414]:case+=f'<path d="M265 250 C340 250 340 {y} 450 {y}"/>'
 case+='</svg>'+node(0)+'<div class="qwen-children">'
 for i in range(1,5):case+='<div class="qwen-child-row"><button type="button" class="qwen-edge" data-qwen-edge="'+str(i)+'" aria-pressed="false" aria-controls="qwen-story-detail" aria-label="'+E(t('查看声明关系：','Inspect declared edge: ')+names[i])+'">↗</button>'+node(i)+'</div>'
 case+='</div></div><aside id="qwen-story-detail" class="qwen-story-detail" aria-live="polite">'+detail+'</aside></section><p class="viz-boundary model-story-scope" data-model-story-scope="qwen" hidden>'+t('第五章 2026-10-16 关系快照中的局部案例；节点等大，位置仅为排布。连线不推断训练细节、贡献比例或正式合作关系，与宏观趋势的样本和统计期分别说明。','A local case from the Chapter 5 snapshot dated 2026-10-16. Equal-sized nodes; positions are for layout. Declared edges do not verify training procedures or contribution shares. This is a separate sample and period from the macro trend.')+'</p><script type="application/json" id="qwen-story-data">'+json.dumps({'nodes':names,'base':source,'snapshot':'2026-10-16'},ensure_ascii=False).replace('<','\\u003c')+'</script>'
 markup=markup[:start]+tabs+'<div id="model-story-macro" data-model-story-panel="macro">'+markup[start:bound]+'</div>'+case+markup[bound:]
 markup=markup.replace('<p class="viz-boundary">ATOM','<p class="viz-boundary model-story-scope" data-model-story-scope="macro">ATOM',1)
 markup=markup.replace('查看 28 个月的新增微调与衍生模型构成；归属按基础模型发布方记录。','先看 28 个月的新增衍生构成，再切换 Qwen 实例，理解一次发布如何延伸。')
 markup=markup.replace('Explore 28 months of new fine-tunes and derivatives, attributed to base-model publishers.','Explore 28 months of derivative composition, then a concrete Qwen example.')
 markup=markup.replace('图 1-1-2 · 从模型供给到生态衍生：月度构成变化。','图 1-1-2 · 开放模型的宏观趋势与 Qwen 衍生实例。').replace('Figure 1-1-2 · From model supply to derivatives: monthly composition.','Figure 1-1-2 · Model derivative trends and a Qwen example, with separate evidence scopes.')
 # Sources remain available in the same source dialog for either view.
 prefix='<span class="viz-source">';where=markup.index(prefix)+len(prefix)
 markup=markup[:where]+'<a class="inline-link" href="/assets/gosm/network.json.gz">'+t('Qwen 关系样本 ↓','Qwen graph sample ↓')+'</a> · <a class="inline-link" href="/assets/report/fig-1-1-2_qwen_case.svg" download>'+t('Qwen 实例静态图 ↓','Qwen case SVG ↓')+'</a> · '+markup[where:]
 return markup
