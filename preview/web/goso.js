/* Progressively enhanced GOSO observations. Source rows are never rewritten. */
(() => {
  'use strict';
  const payload=document.getElementById('goso-chart-data');
  if(!payload)return;
  const charts=JSON.parse(payload.textContent),NS='http://www.w3.org/2000/svg';
  const base=document.querySelector('meta[name="gosd-base"]')?.content||'';
  const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const num=v=>v===null?'—':Math.abs(v)>=10000?(v/10000).toLocaleString('zh-CN',{maximumFractionDigits:2})+'万':v.toLocaleString('zh-CN',{maximumFractionDigits:2});
  const exact=v=>v===null?'—':v.toLocaleString('zh-CN',{maximumFractionDigits:8});
  const download=(text,name,type)=>{const url=URL.createObjectURL(new Blob([globalThis.GosoBrand?.resolve(text)||text],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  const colors=['var(--gv-s0, #156993)', 'var(--gv-s1, #279FA9)', 'var(--gv-s2, #4E87C5)', 'var(--gv-s3, #9973B7)', 'var(--gv-s4, #5C8A3C)', 'var(--gv-s5, #C08A2D)', 'var(--gv-s6, #8C5B3F)', 'var(--gv-s7, #6B7F8C)'];
  const controllers=[];
  document.querySelectorAll('[data-goso-chart]').forEach(fig=>{
    const key=fig.dataset.gosoChart,views=charts[key],prefix='goso-'+key;
    const $=s=>fig.querySelector(s),viewSelect=$('[data-view]'),modeSelect=$('[data-mode]'),year=$('[data-year]'),chart=$('[data-chart]');
    let vi=0,mode='absolute',selected=[],yi=0;
    const view=()=>views[vi];
    const readURL=()=>{
      const p=new URLSearchParams(location.search);vi=Math.max(0,views.findIndex(v=>v.id===p.get(prefix)));
      mode=p.get(prefix+'-mode')==='index'&&view().kind==='line'?'index':'absolute';
      selected=(p.get(prefix+'-series')||view().series.slice(0,8).map(s=>s.key).join('|')).split('|').filter(x=>view().series.some(s=>s.key===x));
      selected=selected.slice(0,8);
      if(!selected.length)selected=view().series.slice(0,8).map(s=>s.key);
      yi=view().x.indexOf(p.get(prefix+'-year'));if(yi<0)yi=view().x.length-1;
    };
    const saveURL=()=>{
      const u=new URL(location.href);u.searchParams.set(prefix,view().id);
      mode==='index'?u.searchParams.set(prefix+'-mode',mode):u.searchParams.delete(prefix+'-mode');
      selected.length===view().series.length?u.searchParams.delete(prefix+'-series'):u.searchParams.set(prefix+'-series',selected.join('|'));
      view().kind==='line'?u.searchParams.set(prefix+'-year',view().x[yi]):u.searchParams.delete(prefix+'-year');
      history.replaceState(null,'',u);
    };
    const transformed=s=>{
      const first=s.values.find(x=>x!==null&&x!==0);
      return s.values.map(x=>x===null?null:mode==='index'?(first?x/first*100:null):x);
    };
    const series=()=>view().series.filter(s=>selected.includes(s.key));
    function readout(point=null){
      const v=view();
      if(point){$('[data-readout]').innerHTML='<strong>'+esc(point.label)+'</strong><span>'+esc(point.x)+' · <b>'+num(point.raw)+'</b> '+esc(v.unit)+(mode==='index'?' · 指数 '+num(point.value):'')+'</span>';return;}
      if(v.kind==='line'){
        $('[data-readout]').innerHTML='<strong>'+esc(v.x[yi])+'</strong>'+series().map(s=>'<span>'+esc(s.label)+' <b>'+num(s.values[yi])+'</b>'+((s.values[yi]!==null&&mode==='index')?' <small>（指数 '+num(transformed(s)[yi])+'）</small>':'')+'</span>').join('');
      }else if(v.kind==='coverage'){
        const values=v.series[0].values,total=values.reduce((a,b)=>a+b,0);
        $('[data-readout]').innerHTML=v.x.map((x,i)=>'<span>'+esc(x)+' <b>'+exact(values[i])+'</b> · '+(values[i]/total*100).toFixed(2)+'%</span>').join('');
      }else $('[data-readout]').innerHTML='<span>按原表数值展示 · '+esc(v.unit)+' · 点选条形查看读数</span>';
    }
    function draw(forcedWidth){
      const v=view(),visible=series(),w=forcedWidth||Math.max(340,Math.round(chart.clientWidth||800));
      const h=v.kind==='line'?Math.round(Math.min(390,Math.max(300,w*.47))):v.kind==='coverage'?190:Math.max(210,58+v.x.length*35);
      const style=getComputedStyle(fig),ink=style.getPropertyValue('--ink').trim()||'var(--gv-ink, #10334D)',grid=style.getPropertyValue('--gv-split').trim()||'var(--gv-line, #CADCE5)';
      let svg='<svg xmlns="'+NS+'" viewBox="0 0 '+w+' '+h+'" role="img" aria-labelledby="'+prefix+'-svg-title"><title id="'+prefix+'-svg-title">'+esc(v.title)+'，单位：'+esc(mode==='index'?'起点指数':v.unit)+'</title><style>text{font-family:Arial,"Noto Sans SC",sans-serif}</style>';
      const dots=[];
      if(v.kind==='line'){
        const l=58,r=18,top=20,b=40,pw=w-l-r,ph=h-top-b;
        const max=Math.max(1,...visible.flatMap(s=>transformed(s).filter(x=>x!==null)))*1.06;
        for(let i=0;i<=4;i++){let y=top+ph-ph*i/4;svg+='<path d="M'+l+' '+y+'H'+(w-r)+'" stroke="'+esc(grid)+'"/><text x="'+(l-8)+'" y="'+(y+4)+'" text-anchor="end" font-size="11" fill="'+esc(ink)+'">'+num(max*i/4)+'</text>';}
        v.x.forEach((x,i)=>{const px=l+i*pw/Math.max(1,v.x.length-1);svg+='<text x="'+px+'" y="'+(h-13)+'" text-anchor="middle" font-size="11" fill="'+esc(ink)+'">'+esc(x.slice(0,4))+'</text>';});
        const cursor=l+yi*pw/Math.max(1,v.x.length-1);svg+='<path d="M'+cursor+' '+top+'V'+(top+ph)+'" stroke="'+esc(ink)+'" stroke-dasharray="3 5" opacity=".25"/>';
        visible.forEach(s=>{
          const vals=transformed(s);let points=[];
          const flush=()=>{if(points.length)svg+='<polyline points="'+points.join(' ')+'" fill="none" stroke="'+s.color+'" stroke-width="2.5" stroke-linejoin="round"/>';points=[];};
          vals.forEach((val,i)=>{
            if(val===null){flush();return;}
            const x=l+i*pw/Math.max(1,v.x.length-1),y=top+ph-val/max*ph;points.push(x+','+y);
            dots.push({x,y,color:s.color,raw:s.values[i],value:val,label:s.label,period:v.x[i],i});
          });flush();
        });
        dots.forEach((d,i)=>{const label=d.label+' · '+d.period+' · '+exact(d.raw)+' '+v.unit+(mode==='index'?' · 指数 '+num(d.value):'');svg+='<circle cx="'+d.x+'" cy="'+d.y+'" r="'+(d.i===yi?5:3.8)+'" fill="'+d.color+'" tabindex="0" data-point="'+i+'" aria-label="'+esc(label)+'"><title>'+esc(label)+'</title></circle>';});
      }else if(v.kind==='coverage'){
        const vals=v.series[0].values,total=vals.reduce((a,b)=>a+b,0),width=w-24,pct=vals[0]/total;
        svg+='<rect x="12" y="22" width="'+width+'" height="42" rx="5" fill="'+esc(grid)+'"/><rect x="12" y="22" width="'+(width*pct)+'" height="42" rx="5" fill="var(--gv-s2, #4E87C5)"/>';
        v.x.forEach((x,i)=>{svg+='<text x="12" y="'+(105+i*32)+'" font-size="14" fill="'+esc(ink)+'">'+esc(x)+' · '+exact(vals[i])+' · '+(vals[i]/total*100).toFixed(2)+'%</text>';});
      }else{
        const vals=v.series[0].values,max=Math.max(1,...vals.filter(x=>x!==null)),left=w<500?96:136,right=w<500?66:83,span=w-left-right;
        v.x.forEach((label,i)=>{
          const raw=vals[i],y=22+i*35,bw=raw===null?0:raw/max*span,title=label+' · '+exact(raw)+' '+v.unit;
          svg+='<g tabindex="0" data-bar="'+i+'" role="img" aria-label="'+esc(title)+'"><title>'+esc(title)+'</title><text x="'+(left-10)+'" y="'+(y+16)+'" text-anchor="end" font-size="11" fill="'+esc(ink)+'">'+esc(label)+'</text><rect x="'+left+'" y="'+y+'" width="'+Math.max(1,bw)+'" height="23" rx="3" fill="'+colors[i%colors.length]+'"/><text x="'+(left+bw+8)+'" y="'+(y+16)+'" fill="'+esc(ink)+'" font-size="11">'+num(raw)+'</text></g>';
        });
      }
      chart.innerHTML=svg+'</svg>';
      chart.querySelectorAll('[data-point]').forEach(el=>{
        const d=dots[+el.dataset.point],show=()=>readout({label:d.label,x:d.period,raw:d.raw,value:d.value});
        el.addEventListener('pointerenter',show);el.addEventListener('focus',show);el.addEventListener('click',()=>{yi=d.i;year.value=yi;$('[data-year-label]').textContent=v.x[yi];saveURL();draw();chart.querySelector('[data-point="'+el.dataset.point+'"]').focus({preventScroll:true});show();});
        el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click();}});
      });
      chart.querySelectorAll('[data-bar]').forEach(el=>{
        const i=+el.dataset.bar,show=()=>readout({label:v.x[i],x:'',raw:v.series[0].values[i],value:v.series[0].values[i]});
        el.addEventListener('pointerenter',show);el.addEventListener('focus',show);el.addEventListener('click',show);
        el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show();}});
      });
      chart.addEventListener('pointerleave',()=>readout(),{once:true});
    }
    function renderTable(){
      const v=view(),ss=v.kind==='line'?series():v.series;
      $('[data-table]').innerHTML='<div class="reader-table-wrap"><table class="reader-table"><caption>'+esc(v.title)+' · 原始数值 · '+esc(v.unit)+'</caption><thead><tr><th scope="col">'+(v.kind==='line'?'时间':'对象')+'</th>'+ss.map(s=>'<th scope="col">'+esc(s.label)+'</th>').join('')+'</tr></thead><tbody>'+v.x.map((x,i)=>'<tr><th scope="row">'+esc(x)+'</th>'+ss.map(s=>'<td>'+exact(s.values[i])+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
    }
    function render(){
      const v=view();if(v.series.length>8){v.series.forEach((s,i)=>s.color=colors[Math.max(0,selected.indexOf(s.key))%8]);}
      viewSelect.value=vi;modeSelect.value=mode;
      $('[data-chart-title]').textContent=v.title;$('[data-note]').textContent=(v.series.length>8?'每图最多显示 8 条曲线，可切换城市；完整数据见表格。 ':'')+v.note;
      $('[data-source]').href=v.source;$('[data-csv]').href=base+v.csv;
      $('[data-svg]').href=base+'/assets/goso/'+v.id+'.svg';
      $('[data-unit]').textContent=mode==='index'?'起点指数 = 100（各序列首个非空值）':'单位：'+v.unit;
      $('[data-mode-label]').hidden=v.kind!=='line';$('[data-time-control]').hidden=v.kind!=='line';
      year.max=v.x.length-1;year.value=yi;$('[data-year-label]').textContent=v.x[yi];
      const legend=$('[data-legend]');legend.innerHTML=v.kind==='line'?v.series.map(s=>'<button type="button" data-series="'+esc(s.key)+'" aria-pressed="'+selected.includes(s.key)+'"><i style="background:'+s.color+'"></i>'+esc(s.label)+'</button>').join(''):'';
      legend.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
        const k=b.dataset.series;if(selected.includes(k)){if(selected.length===1)return;selected=selected.filter(x=>x!==k);}else {if(selected.length>=8){$('[data-note]').textContent='每图最多显示 8 条曲线，请先取消一条；完整十城市数据可查表。 '+v.note;return;}selected.push(k);}
        saveURL();render();[...legend.querySelectorAll('button')].find(x=>x.dataset.series===k)?.focus({preventScroll:true});
      }));draw();readout();renderTable();
    }
    viewSelect.addEventListener('change',()=>{vi=+viewSelect.value;mode='absolute';selected=view().series.slice(0,8).map(s=>s.key);yi=view().x.length-1;saveURL();render();});
    modeSelect.addEventListener('change',()=>{mode=modeSelect.value;saveURL();render();});
    year.addEventListener('input',()=>{yi=+year.value;$('[data-year-label]').textContent=view().x[yi];saveURL();draw();readout();});
    $('[data-reset]').addEventListener('click',()=>{vi=0;mode='absolute';selected=view().series.slice(0,8).map(s=>s.key);yi=view().x.length-1;const u=new URL(location.href);[prefix,prefix+'-mode',prefix+'-series',prefix+'-year'].forEach(k=>u.searchParams.delete(k));history.replaceState(null,'',u);render();});
    $('[data-share]').addEventListener('click',async()=>{
      saveURL();const u=new URL(location.href);u.hash=prefix;
      try{await navigator.clipboard.writeText(u.href);$('[data-readout]').textContent='已复制当前图表链接（包含视图、系列和年份）。';}
      catch{$('[data-readout]').innerHTML='<label>复制当前链接 <input readonly aria-label="当前图表链接" value="'+esc(u.href)+'"></label>';$('[data-readout] input').select();}
    });
    $('[data-svg]').addEventListener('click',e=>{
      if(e.ctrlKey||e.metaKey||e.shiftKey)return;e.preventDefault();
      draw(840);
      const svg=chart.querySelector('svg').cloneNode(true),box=svg.getAttribute('viewBox').split(' ').map(Number),w=box[2],h=box[3];
      draw();
      const dark=document.documentElement.dataset.theme==='dark',bg=dark?'var(--gv-bg, #F3F8FA)':'var(--gv-surface, #FFFFFF)',ink=dark?'var(--gv-ink, #10334D)':'var(--gv-ink, #10334D)';
      const inner=svg.innerHTML.replace(/tabindex="0"/g,'');
      const v=view(),legend=series().map(s=>s.label).join(' · ');
      const noteLines=[];let noteLine='',noteWidth=0;for(const c of v.note){const cw=c.codePointAt(0)>255?2:1;if(noteWidth+cw>125){noteLines.push(noteLine);noteLine='';noteWidth=0;}noteLine+=c;noteWidth+=cw;}if(noteLine)noteLines.push(noteLine);
      const noteSVG=noteLines.map((line,i)=>'<text x="14" y="'+(h+124+i*16)+'">'+esc(line)+'</text>').join('');
      const exported='<svg xmlns="'+NS+'" viewBox="0 0 '+w+' '+(h+164+noteLines.length*16)+'"><rect width="100%" height="100%" fill="'+bg+'"/><g fill="'+ink+'" font-family="Arial,Noto Sans SC,sans-serif"><text x="14" y="25" font-size="16">'+esc(v.title)+'</text><text x="14" y="48" font-size="10">'+esc(mode==='index'?'起点指数 = 100（首个非空值）':'单位：'+v.unit)+'</text><text x="14" y="68" font-size="10">'+esc(legend)+'</text></g><g transform="translate(0 83)">'+inner+'</g><g fill="'+ink+'" font-family="Arial,Noto Sans SC,sans-serif" font-size="10"><text x="14" y="'+(h+105)+'">GOSO · 2026 全球开源发展报告 · 评审版</text>'+noteSVG+'<text x="14" y="'+(h+144+noteLines.length*16)+'">来源：'+esc(v.csv.split('/').pop())+' · 95ffe2d</text></g></svg>';
      download(exported,'GOSO-'+v.id+'-'+mode+'.svg','image/svg+xml;charset=utf-8');
    });
    $('.goso-controls').hidden=false;$('.goso-interaction-hint').hidden=false;$('[data-share]').hidden=false;
    readURL();render();controllers.push({readURL,render,draw});
    if(typeof ResizeObserver!=='undefined'){let width=0;new ResizeObserver(entries=>{const next=entries[0].contentRect.width;if(Math.abs(next-width)>1){width=next;draw();}}).observe(chart);}
  });
  window.addEventListener('popstate',()=>controllers.forEach(c=>{c.readURL();c.render();}));
  document.addEventListener('gosdthemechange',()=>controllers.forEach(c=>c.render()));
  const fields=[...document.querySelectorAll('[data-review-key]')],status=document.getElementById('goso-note-status'),storeKey='gosd-goso-review-v07';
  let saved={};try{saved=JSON.parse(localStorage.getItem(storeKey)||'{}');}catch{}
  fields.forEach(f=>{f.value=typeof saved[f.dataset.reviewKey]==='string'?saved[f.dataset.reviewKey]:'';f.addEventListener('input',()=>{try{localStorage.setItem(storeKey,JSON.stringify(Object.fromEntries(fields.map(x=>[x.dataset.reviewKey,x.value]))));status.textContent='已保存到当前浏览器';}catch{status.textContent='浏览器无法保存，请导出备注';}});});
  document.querySelector('[data-export-notes]').addEventListener('click',()=>{
    const text='# GOSO 样章评审备注\n\n数据版本：95ffe2d3ae52191555a40af25e1a00b26ffc65cc\n\n'+fields.map(f=>'## '+f.closest('label').querySelector('strong').textContent+'\n\n'+(f.value.trim()||'待补充')).join('\n\n')+'\n';
    download(text,'GOSO-review-notes.md','text/markdown;charset=utf-8');status.textContent='已导出评审备注';
  });
})();
