/* The draft series are read verbatim from the existing, unchanged content.js. */
(() => {
  'use strict';
  const data=window.OSDG_DATA;if(!data)return;
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const zh=document.documentElement.lang.startsWith('zh'),t=(z,e)=>zh?z:e;
  const params=new URLSearchParams(location.search),regions=data.regions,trend=data.trend;
  const valid=regions.map(r=>r[0]);
  let mode=params.get('mode')==='index'?'index':'count';
  let year=Math.max(2022,Math.min(2026,parseInt(params.get('year'),10)||2026));
  let selected=(params.get('regions')||'').split('|').filter(r=>valid.includes(r));
  if(!selected.length)selected=valid.slice();
  let table=params.get('table')==='1';
  const legend=$('#chart-legend');
  regions.forEach(r=>{
    const label=document.createElement('label'),input=document.createElement('input'),info=document.createElement('span'),name=document.createElement('span'),value=document.createElement('span');
    input.type='checkbox';input.value=r[0];input.checked=selected.includes(r[0]);info.className='legend-info';name.textContent=r[zh?1:2];value.className='legend-value';value.dataset.region=r[0];info.append(name,value);label.append(input,info);legend.append(label);
    input.addEventListener('change',()=>{if(!input.checked&&selected.length===1){input.checked=true;return;}selected=$$('#chart-legend input:checked').map(x=>x.value);render();});
  });
  const svgNS='http://www.w3.org/2000/svg';
  function element(name,attrs={},text){const node=document.createElementNS(svgNS,name);Object.entries(attrs).forEach(([key,value])=>node.setAttribute(key,value));if(text!==undefined)node.textContent=text;return node;}
  const value=(row,key)=>mode==='index'?row[key]/trend[0][key]*100:row[key];
  const format=v=>mode==='index'?v.toFixed(1):v.toLocaleString(zh?'zh-CN':'en-US');
  function persist(){const url=new URL(location.href);url.searchParams.set('mode',mode);url.searchParams.set('year',year);url.searchParams.set('regions',selected.join('|'));table?url.searchParams.set('table','1'):url.searchParams.delete('table');history.replaceState(null,'',url);}
  function render(save=true){
    if(save)persist();
    const dark=document.documentElement.dataset.theme==='dark';
    const w=650,h=330,left=53,right=24,top=35,bottom=43,pw=w-left-right,ph=h-top-bottom;
    const max=Math.max(...trend.flatMap(row=>selected.map(key=>value(row,key))));
    const upper=mode==='index'?Math.ceil(max/50)*50:Math.ceil(max/1000000)*1000000;
    const x=yr=>left+(yr-2022)/4*pw,y=v=>h-bottom-v/upper*ph;
    const svg=element('svg',{viewBox:`0 0 ${w} ${h}`,role:'img','aria-labelledby':'trend-title trend-desc'});
    svg.append(element('title',{id:'trend-title'},t('2022—2026 活跃开发者区域变化','Active developers by region, 2022–2026')));
    svg.append(element('desc',{id:'trend-desc'},t(`当前查看 ${year} 年，${mode==='index'?'2022 为 100 的指数':'开发者人数'}。完整数值可展开数据表。`,`Inspecting ${year}, ${mode==='index'?'indexed to 2022 = 100':'developer counts'}. Expand the data table for complete values.`)));
    svg.append(element('text',{x:left,y:15,class:'chart-axis-label'},mode==='index'?'2022 = 100':t('单位：百万人','Millions of developers')));
    for(let i=0;i<=4;i++){const v=upper*i/4;svg.append(element('line',{x1:left,y1:y(v),x2:w-right,y2:y(v),class:'chart-gridline'}));svg.append(element('text',{x:left-10,y:y(v)+4,'text-anchor':'end',class:'chart-axis-label'},mode==='index'?Math.round(v):(v/1000000).toFixed(1)));}
    trend.forEach(row=>svg.append(element('text',{x:x(row.year),y:h-15,'text-anchor':'middle',class:'chart-axis-label'},row.year)));
    svg.append(element('line',{x1:x(year),y1:top,x2:x(year),y2:h-bottom,stroke:'var(--muted)','stroke-dasharray':'3 5',opacity:'.5'}));
    regions.forEach(r=>{
      const label=[...legend.children].find(l=>l.querySelector('input').value===r[0]);
      label.style.setProperty('--series-color',r[dark?4:3]);label.querySelector('.legend-value').textContent=format(value(trend.find(row=>row.year===year),r[0]));
      label.querySelector('input').disabled=selected.length===1&&selected.includes(r[0]);
      if(!selected.includes(r[0]))return;
      const line=element('path',{d:trend.map((row,i)=>(i?'L':'M')+x(row.year)+','+y(value(row,r[0]))).join(' '),stroke:r[dark?4:3],class:'chart-line'});svg.append(line);
      trend.forEach(row=>{const circle=element('circle',{cx:x(row.year),cy:y(value(row,r[0])),r:row.year===year?4.6:2.6,fill:r[dark?4:3]});circle.append(element('title',{},`${r[zh?1:2]} · ${row.year}: ${format(value(row,r[0]))}`));svg.append(circle);});
    });
    $('#chart-canvas').replaceChildren(svg);$('#chart-year').value=year;$('#chart-year-label').value=year;
    $$('[data-chart-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.chartMode===mode)));
    $('#chart-selection').textContent=t(`已选择 ${year} 年，${selected.length} 个地区。`,`Selected ${year}, ${selected.length} regions.`);
    const tableNode=document.createElement('table');tableNode.className='chart-table';
    const caption=document.createElement('caption');caption.textContent=t('当前所选地区的完整年度数据','Complete annual data for the selected regions')+' · '+(mode==='index'?'2022 = 100':t('人数','Developers'));tableNode.append(caption);
    const head=document.createElement('thead'),headRow=document.createElement('tr');
    [t('年度','Year'),...regions.filter(r=>selected.includes(r[0])).map(r=>r[zh?1:2])].forEach(text=>{const th=document.createElement('th');th.scope='col';th.textContent=text;headRow.append(th);});head.append(headRow);tableNode.append(head);
    const body=document.createElement('tbody');trend.forEach(row=>{const tr=document.createElement('tr'),th=document.createElement('th');th.scope='row';th.textContent=row.year;tr.append(th);regions.filter(r=>selected.includes(r[0])).forEach(r=>{const td=document.createElement('td');td.textContent=format(value(row,r[0]));tr.append(td);});body.append(tr);});tableNode.append(body);$('#chart-table-wrap').replaceChildren(tableNode);
    $('#chart-table-wrap').hidden=!table;$('#chart-table-toggle').setAttribute('aria-expanded',String(table));$('#chart-table-toggle').textContent=table?t('收起数据表','Hide data table'):t('查看数据表','View data table');
  }
  $$('[data-chart-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.chartMode;render();}));
  $('#chart-year').addEventListener('input',e=>{year=Number(e.target.value);render();});
  $('#chart-table-toggle').addEventListener('click',()=>{table=!table;render();});
  document.addEventListener('gosdthemechange',()=>render(false));
  window.addEventListener('popstate',()=>{const p=new URLSearchParams(location.search);mode=p.get('mode')==='index'?'index':'count';year=Math.max(2022,Math.min(2026,parseInt(p.get('year'),10)||2026));const next=(p.get('regions')||'').split('|').filter(x=>valid.includes(x));selected=next.length?next:valid.slice();table=p.get('table')==='1';$$('#chart-legend input').forEach(input=>input.checked=selected.includes(input.value));render(false);});
  render(false);
})();
