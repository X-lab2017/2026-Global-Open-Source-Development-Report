/* Progressive interaction for the source-backed Chapter 1 figures. */
(() => {
  'use strict';
  const $=(s,root=document)=>root.querySelector(s), $$=(s,root=document)=>[...root.querySelectorAll(s)];
  const zh=document.documentElement.lang.startsWith('zh'), t=(z,e)=>zh?z:e;
  const base=$('meta[name="gosd-base"]')?.content||'', lang=zh?'zh':'en';
  const data=id=>{const el=document.getElementById(id);return el?JSON.parse(el.textContent):null;};
  const initial=new URLSearchParams(location.search);
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const route=tail=>`${base}/2026/${lang}/${tail}`;
  const anchor=(url,label)=>`<a class="inline-link" href="${escape(url)}">${escape(label)}</a>`;
  const remember=(key,value)=>{const url=new URL(location.href);value!==''?url.searchParams.set(key,String(value)):url.searchParams.delete(key);history.replaceState(null,'',url);};
  function inspect(nodes,select){
    nodes.forEach((node,i)=>{
      node.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse')select(node,false);});
      node.addEventListener('focus',()=>select(node,false));
      node.addEventListener('click',()=>select(node,true));
      node.addEventListener('keydown',e=>{
        if(['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].includes(e.key)){
          e.preventDefault();let n=e.key==='Home'?0:e.key==='End'?nodes.length-1:(i+(['ArrowRight','ArrowDown'].includes(e.key)?1:-1)+nodes.length)%nodes.length;
          nodes[n].focus();select(nodes[n],true);
        }else if(node.tagName.toLowerCase()==='g'&&['Enter',' '].includes(e.key)){e.preventDefault();select(node,true);}
      });
    });
  }
  function pressed(nodes,selected){nodes.forEach(n=>n.setAttribute('aria-pressed',String(n===selected)));}

  const linux=data('linux-viz-data');
  if(linux){
    let kind=initial.get('linux')==='contributors'?'contributors':'organizations';
    const selectedRows={organizations:0,contributors:0};
    const buttons=$$('[data-linux-kind]');
    function showRow(i){
      const row=linux[kind].rows[i];if(!row)return;
      const panel=$('#linux-selection');panel.replaceChildren();
      const name=document.createElement('strong'),value=document.createElement('span');name.textContent=row.name;
      value.textContent=row.contributions.toLocaleString('en-US')+' · '+t('本类榜单占比 ','Share in this leaderboard ')+row.percentage+'%';panel.append(name,value);
      selectedRows[kind]=i;
      $$('.linux-bar').forEach((b,j)=>{b.classList.toggle('is-selected',i===j);b.setAttribute('aria-pressed',String(i===j));});
    }
    function showKind(value,save){
      if(!linux[value])return;kind=value;
      pressed(buttons,buttons.find(b=>b.dataset.linuxKind===kind));
      $('#linux-series-title').textContent=kind==='organizations'?t('组织榜单前 10 条记录','First 10 organization records'):t('贡献者榜单前 10 条记录','First 10 contributor records');
      const container=$('#linux-bars');container.replaceChildren();const rows=linux[kind].rows, max=rows[0].contributions;
      rows.forEach((row,i)=>{
        const b=document.createElement('button');b.type='button';b.className='linux-bar';b.dataset.row=String(i);b.setAttribute('aria-label',`${row.name} · ${row.contributions.toLocaleString('en-US')} · ${row.percentage}%`);
        const name=document.createElement('span');name.className='bar-name';name.title=row.name;
        const rank=document.createElement('i');rank.textContent=String(i+1).padStart(2,'0');name.append(rank,document.createTextNode(row.name));
        const track=document.createElement('span');track.className='bar-track';const fill=document.createElement('span');fill.style.width=(row.contributions/max*100)+'%';track.append(fill);
        const value=document.createElement('b');value.textContent=row.contributions.toLocaleString('en-US');b.append(name,track,value);container.append(b);
      });
      inspect($$('.linux-bar'),node=>showRow(Number(node.dataset.row)));showRow(selectedRows[kind]);if(save)remember('linux',kind);
    }
    buttons.forEach(b=>b.addEventListener('click',()=>showKind(b.dataset.linuxKind,true)));showKind(kind,false);
  }

  const models=data('model-viz-data');
  if(models){
    const buttons=$$('[data-month]'), slider=$('#model-month');
    const months={Jan:'01',Feb:'02',Mar:'03',Apr:'04',May:'05',Jun:'06',Jul:'07',Aug:'08',Sep:'09',Oct:'10',Nov:'11',Dec:'12'};
    function select(index,save){
      if(!Number.isInteger(index)||index<0||index>=models.length)return;
      const row=models[index],[m,y]=row.date.split(' '),date='20'+y+'.'+months[m];
      $('#model-current-month').textContent=date;$('#model-month-label').textContent=date;slider.value=String(index);slider.setAttribute('aria-valuetext',date);
      $('#model-china-share').textContent=String(row.china);$$('[data-model-value]').forEach(n=>n.textContent=row[n.dataset.modelValue]+'%');
      pressed(buttons,buttons[index]);$('#model-announcement').textContent=date+' · '+t('中国','China')+' '+row.china+'% · '+t('美国','US')+' '+row.unitedStates+'% · '+t('欧洲','Europe')+' '+row.europe+'%';
      $$('[data-month-step]').forEach(b=>b.disabled=Number(b.dataset.monthStep)<0?index===0:index===models.length-1);
      if(save)remember('modelMonth',index);
    }
    inspect(buttons,(node,save)=>select(Number(node.dataset.month),save));slider.addEventListener('input',()=>select(Number(slider.value),true));
    $$('[data-month-step]').forEach(b=>b.addEventListener('click',()=>select(Number(slider.value)+Number(b.dataset.monthStep),true)));
    const raw=initial.get('modelMonth'),index=raw===null?models.length-1:Number(raw);select(Number.isInteger(index)&&index>=0&&index<models.length?index:models.length-1,false);
  }

  const sdgs=data('sdg-viz-data');
  if(sdgs){
    const nodes=$$('[data-sdg]');
    function select(n,save){
      const number=Number(n.dataset.sdg);pressed(nodes,n);const box=$('#sdg-selection');box.replaceChildren();
      const b=document.createElement('b'),name=document.createElement('span');b.textContent='SDG '+number;name.textContent=sdgs[number-1];box.append(b,name);if(save)remember('sdg',number);
    }
    inspect(nodes,select);select(nodes.find(n=>n.dataset.sdg===initial.get('sdg'))||nodes[8],false);
  }
  const dpg=data('dpg-viz-data');
  if(dpg){
    const nodes=$$('[data-dpg]');
    function select(n,save){
      const index=Number(n.dataset.dpg),row=dpg[index];pressed(nodes,n);
      const box=$('#dpg-selection');box.replaceChildren();const strong=document.createElement('strong'),p=document.createElement('p');strong.textContent=row.title;p.textContent=row.description;box.append(strong,p);if(save)remember('dpg',index);
    }
    inspect(nodes,select);select(nodes.find(n=>n.dataset.dpg===initial.get('dpg'))||nodes[0],false);
  }

  const goals=data('goals-viz-data');
  if(goals){
    const nodes=$$('[data-goal]');
    function select(n,save){
      const key=n.dataset.goal,row=goals[key];pressed(nodes,n);
      $('#goal-select').value=key;
      $('#goal-selection').innerHTML=`<div class="goal-detail-copy"><span class="viz-label">${t('目标解读','GOAL NOTES')}</span><strong>${escape(row.title)}</strong><p>${escape(row.question)}</p><small>${escape(row.boundary)}</small></div><div class="goal-detail-indicators"><span class="viz-label">${t('对应指标','RELATED INDICATORS')}</span><div>${row.indicators.map(code=>anchor(route('data/indicators/')+'#indicator-'+code,code)).join('')}</div></div>`;
      $('#goal-selection').style.setProperty('--selected-pillar',row.color);if(save)remember('goal',key);
    }
    inspect(nodes,select);select(nodes.find(n=>n.dataset.goal===initial.get('goal'))||nodes[0],false);
    $('#goal-select').addEventListener('change',e=>{const node=nodes.find(n=>n.dataset.goal===e.target.value);if(node)select(node,true);});
  }

  const indicators=data('indicators-viz-data');
  if(indicators){
    const nodes=$$('[data-indicator]'),roles=$$('[data-indicator-role]'),chapterRoutes={GOSO:'02',GOSR:'03',GOSL:'04',GOSM:'05'};
    function select(n,save){
      const code=n.dataset.indicator,row=indicators[code];pressed(nodes,n);
      const chapters=row.chapter_tags.split(';').filter(c=>chapterRoutes[c]).map(c=>anchor(route('chapters/'+chapterRoutes[c]+'/'),c)).join('');
      $('#indicator-selection').innerHTML=`<div><span class="viz-label">${escape(code)} · ${escape(row.role)}</span><strong>${escape(row.indicator_name_zh)}</strong><p>${escape(row.definition)}</p><div class="indicator-calculation"><small>${t('计算口径','Calculation')}</small>${escape(row.calculation_rule)}</div></div><div><span class="viz-label">${t('证据与用途','EVIDENCE & USE')}</span><p>${escape(row.data_status)}</p><small>${escape(row.remaining_evidence)}</small><div class="indicator-chapters">${chapters}</div>${anchor(route('data/indicators/')+'#indicator-'+code,t('查看完整定义与关联数据 →','Full definition and related files →'))}</div>`;
      if(save)remember('indicator',code);
    }
    function role(n,save){
      const selected=n.dataset.indicatorRole;let count=0;pressed(roles,n);
      nodes.forEach(b=>{const match=!selected||b.dataset.role===selected;b.classList.toggle('is-muted',!match);if(match)count++;});
      $('#atlas-role-count').textContent=t(`突出显示 ${count} / 29 项`,`Highlighting ${count} / 29 measures`);if(save)remember('role',selected);
    }
    inspect(nodes,select);roles.forEach(n=>n.addEventListener('click',()=>role(n,true)));
    select(nodes.find(n=>n.dataset.indicator===initial.get('indicator'))||nodes[0],false);role(roles.find(n=>n.dataset.indicatorRole===initial.get('role'))||roles[0],false);
  }
})();
