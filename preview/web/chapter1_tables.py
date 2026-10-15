"""Compact, semantic Chapter 1 tables; JavaScript only adds presentation/paging."""
import html
E=lambda value:html.escape(str(value),quote=True)
SPECS={
 '小节':('第一章阅读路线','Chapter 1 reading route',[23,22,32,23]),
 '研究问题':('五个研究问题，连接五个研究与行动板块','Five questions for research and action',[58,42]),
 '观察面向':('三种变化：资产、社区与治理','Three changes: assets, communities and governance',[15,27,32,26]),
 '公共价值路径':('表 1.1.1 · 从开放实践到公共价值','Table 1.1.1 · From open practice to public value',[19,31,36,14]),
 '目标内涵':('表 1.2.1 · 四大支柱与十个维度','Table 1.2.1 · Four pillars, ten dimensions',[23,23,27,27]),
 '当前指标关联的 SDGs':('表 1.2.2 · OSDGs 与 SDGs 的研究关联','Table 1.2.2 · Research links to SDGs',[22,17,28,33]),
 '使用者':('表 1.2.3 · 框架的应用路径','Table 1.2.3 · Applications of the framework',[24,38,38]),
 '支柱／维度':('表 1.3.2 · 二十九项指标总表','Table 1.3.2 · All 29 indicators',[25,24,27,10,14]),
 '方法':('表 1.3.3 · 三类方法的不同用途','Table 1.3.3 · Three methods, distinct uses',[28,36,36]),
 '月份':('模型衍生 · 完整月度数据','Model derivatives · Monthly data',[28,24,24,24]),
}
def render(rows,lang,fid,cell,source_url=None):
    zh=lang=='zh';spec=next((SPECS[x] for x in rows[0] if x in SPECS),None)
    if fid=='table-model-months':spec=SPECS['月份']
    title=spec[0 if zh else 1] if spec else ('数据对照表' if zh else 'Data table')
    widths=spec[2] if spec else [100/len(rows[0])]*len(rows[0])
    count=len(rows)-1;long=count>8;height=720 if long else 580 if count<=3 else 680 if len(rows[0])>=4 else 620
    out=f'<figure id="{fid}" class="chapter-table-figure" data-slide-key="{fid}" data-slide-height="{height}" data-lang="{lang}" aria-labelledby="{fid}-title"><div class="table-slide-heading"><span class="eyebrow">GOSD / CHAPTER 01 · REFERENCE</span><h4 id="{fid}-title">{E(title)}</h4><span class="table-total">{count} '+('项记录' if zh else 'records')+'</span></div>'
    out+='<div class="table-slide-body"><table class="chapter-compact-table"><colgroup>'+''.join(f'<col style="width:{w}%">' for w in widths)+'</colgroup><thead><tr>'+''.join('<th scope="col">'+cell(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'
    for row in rows[1:]:out+='<tr>'+''.join(('<th scope="row">' if i==0 else '<td>')+cell(c)+('</th>' if i==0 else '</td>') for i,c in enumerate(row))+'</tr>'
    out+='</tbody></table></div>'
    if long:out+='<nav class="table-pagination" hidden aria-label="'+('数据表分页' if zh else 'Table pages')+'"></nav>'
    out+='<figcaption>'+('按原稿保留完整内容；' if zh else 'Complete source content retained; ')+('切换页码逐页查阅，打印时显示全部记录。' if zh and long else '以对照关系组织阅读。' if zh else 'page through records; printing includes all rows.' if long else 'read across each comparison.')
    if source_url:out+=f' <a class="inline-link" href="{E(source_url)}">'+('查看来源 ↗' if zh else 'View source ↗')+'</a>'
    out+='</figcaption></figure>'
    if long:out='<details class="chapter-table-reference"><summary>'+('查阅完整数据表 · ' if zh else 'Browse the full data table · ')+str(count)+(' 项记录' if zh else ' records')+'</summary>'+out+'</details>'
    return out
