/* G-Map review: synthetic observations remain distinct from repository series. */
(()=>{'use strict';
const D=window.GOSD_GMAP;if(!D||!document.querySelector('.gmap-review'))return;
const M=D.simulation,$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const S={world:'supply',governance:'practices',support:'scatter',public:'evidence',ai:'matrix',country:'CN',actor:'all',mock:true,practice:'0:0',role:0,year:2026,foundation:'active_repositories',license:'MIT',project:6,threshold:12,fund:0,sector:0,outcome:0,check:'0:0',permission:'2:3'};
const C=['var(--gm-brand)','var(--gm-teal)','var(--gm-purple)','var(--gm-gold)'];
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=x=>Number(x).toLocaleString('zh-CN',{maximumFractionDigits:2});
const base=(document.querySelector('meta[name="gosd-base"]')?.content||'/report').replace(/\/$/,'');
const asset=n=>base+'/assets/gmap/'+n;
const buttons=(key,rows,val)=>rows.map(([v,l])=>`<button data-gm-set="${key}:${v}" aria-pressed="${String(v)===String(val)}">${l}</button>`).join('');
const select=(key,rows,val,label)=>`<label>${label} <select data-gm-select="${key}" aria-label="${label}">${rows.map(([v,l])=>`<option value="${v}" ${String(v)===String(val)?'selected':''}>${esc(l)}</option>`).join('')}</select></label>`;
const sim=txt=>`<div class="gm-evidence"><b>模拟演示 · 非实测 · 非预测</b>${txt?' · '+txt:''}</div>`;
const note=txt=>`<div class="gm-note">${txt}</div>`;
const side=(title,body)=>`<aside class="gm-side"><span class="gm-eyebrow">观察与解释</span><h5>${title}</h5>${body}</aside>`;
const split=(main,aside)=>`<div class="gm-split"><div class="gm-main">${main}</div>${aside}</div>`;
const stat=(label,value,unit='')=>`<div class="gm-readout"><span>${label}</span><strong class="gm-big">${value}<small>${unit}</small></strong></div>`;
const foot=(key,text)=>{$('#gm-'+key+'-foot').textContent=text;};
const svg=(label,body,w=850,h=385)=>`<svg viewBox="0 0 ${w} ${h}" role="group" aria-label="${label}"><title>${label}</title>${body}</svg>`;
function line(rows,fields,{unit='',height=345,year=S.year,synthetic=false}={}){
 const W=850,H=height,L=70,R=36,T=35,B=52,values=rows.flatMap(r=>fields.map(f=>r[f.key])),max=Math.max(...values)*1.12||1;
 const x=i=>L+i*(W-L-R)/(rows.length-1),y=v=>H-B-(v/max)*(H-T-B);
 let o='';for(let i=0;i<5;i++){let v=max*i/4;o+=`<line x1="${L}" y1="${y(v)}" x2="${W-R}" y2="${y(v)}" class="gm-axis"/><text x="${L-12}" y="${y(v)+5}" text-anchor="end">${num(v>=1000?Math.round(v):Math.round(v*10)/10)}</text>`;}
 o+=`<text x="${L}" y="17">${unit}${synthetic?' · 模拟':''}</text>`;
 rows.forEach((r,i)=>{o+=`<text x="${x(i)}" y="${H-19}" text-anchor="middle">${r.year||r.period}</text>`;if(r.year===year)o+=`<line x1="${x(i)}" x2="${x(i)}" y1="${T}" y2="${H-B}" stroke="var(--gm-gold)" stroke-dasharray="4 5"/>`;});
 fields.forEach((f,j)=>{o+=`<path d="${rows.map((r,i)=>(i?'L':'M')+x(i)+','+y(r[f.key])).join('')}" fill="none" stroke="${C[j]}" stroke-width="3" ${synthetic?'stroke-dasharray="6 4"':''}/>`;rows.forEach((r,i)=>{o+=`<circle cx="${x(i)}" cy="${y(r[f.key])}" r="${r.year===year?7:5}" fill="${synthetic?'var(--gm-surface)':C[j]}" stroke="${C[j]}" stroke-width="2" ${r.year?`data-gm-set="year:${r.year}" tabindex="0" role="button" aria-label="${r.year}，${f.label} ${r[f.key]} ${unit}"`:''}><title>${r.year||r.period} · ${f.label}：${num(r[f.key])} ${unit}${synthetic?'（模拟）':'（仓库已有，待核验）'}</title></circle>`;});});
 return svg('趋势：'+fields.map(f=>f.label).join('、'),o,W,H)+`<div class="gm-legend">${fields.map((f,j)=>`<span><i style="background:${C[j]}"></i>${f.label}</span>`).join('')}</div>`;
}
function world(){
 const layer=['supply','maintenance','application'].indexOf(S.world),labels=['治理支持组织条目','共同维护关系条目','公共部署证据条目'],r=M.map.records.find(r=>r.id===S.country),v=r=>layer===0&&S.actor!=='all'?r.actors[+S.actor]:r.values[layer],max=Math.max(...M.map.records.map(v));
 let body=D.world.map(f=>`<path d="${f.d}" fill="var(--gm-empty)" stroke="var(--gm-surface)" stroke-width=".45"><title>${esc(f.name)}</title></path>`).join('');
 if(S.mock)body+=M.map.records.filter(r=>v(r)>0).map(r=>{const f=D.world.find(f=>f.id===r.id),n=v(r),radius=Math.sqrt(n/max)*20;return `<g data-gm-set="country:${r.id}" tabindex="0" role="button" aria-pressed="${r.id===S.country}" aria-label="${r.name}，${labels[layer]} ${n}，模拟"><circle cx="${f.center[0]}" cy="${f.center[1]}" r="${radius}" fill="${C[layer]}" fill-opacity=".3" stroke="${r.id===S.country?'var(--gm-gold)':C[layer]}" stroke-width="${r.id===S.country?3:1.5}" stroke-dasharray="3 2"/><circle cx="${f.center[0]}" cy="${f.center[1]}" r="3" fill="${C[layer]}"/><title>${r.name} · ${num(n)} 条（模拟）</title></g>`;}).join('');
 const chart=svg('全球'+labels[layer]+'地图，所有点值为模拟；中国包含台湾省',body,880,470).replace('<svg ','<svg class="gm-map" ');
 $('#gm-world').innerHTML=split(`<div class="gm-controls">${buttons('mock',[['yes','含模拟演示'],['no','仅看已核验']],S.mock?'yes':'no')}${layer===0?select('actor',[['all','全部类型'],...M.map.actors.map((a,i)=>[i,a])],S.actor,'主体'):''}</div>${sim(S.mock?'点大小表示条目数，不代表能力评分':'模拟已隐藏；本轮尚未接入已核验地理记录')}${chart}<div class="gm-map-key"><span class="gm-dot-key"></span><span>虚线点＝模拟 · 代表位置，非精确地址</span><em></em><span>灰色＝没有接入数据</span></div>${note(['组织登记地；全球组织的服务范围不全部归于总部国家。','维护者所在地；按项目和实质维护记录建立关系，不以一次提交推断长期维护。','应用所在地；一项方案可在多地部署，不与组织或维护条目相加。'][layer])}`,side(S.mock?r.name:'等待核验记录',`${S.mock?select('country',M.map.records.map(r=>[r.id,r.name]),S.country,'定位'):''}${stat(labels[layer],S.mock?v(r):'—','条')}${S.mock?'<span class="gm-badge forecast">虚构样本 · 10 个地区</span>':'<p>真实记录待补。切回模拟可继续评审图形。</p>'}<p>${['谁提供治理支持？关注多类机构能否提供规则、资源和责任入口。','应用地区是否也参与维护？需要连接同一项目的角色与地区记录。','公共使用在哪里发生？需要具体实施方、时间与可追溯来源。'][layer]}</p>${note('未知地域独立存储，当前没有设定数量。DPG 名录认可与研究候选分别标记；此图不表示任何真实项目获认可。')}`));
 foot('world','设计模拟 · 三层分开计量 · 地图几何沿用 V-Map / A-Map');
}
const practiceCols=['决策记录','角色晋升','利益冲突','申诉渠道','安全响应','退出交接'],practiceLabels=['未发现','有记录','待核验'];
function governance(){let main='',aside='';
 if(S.governance==='practices'){
  const [r,c]=S.practice.split(':').map(Number),types=['社区协作','企业主导','基金会托管','公共机构'];
  main=sim('四个虚构项目；不代表治理类型的平均水平')+`<div class="gm-table-wrap"><table class="gm-practice"><thead><tr><th>虚构项目</th>${practiceCols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>${M.governance.map((row,i)=>`<tr><th>${String.fromCharCode(65+i)} · ${types[i]}</th>${row.map((v,j)=>`<td><button class="gm-state-${v}" data-gm-set="practice:${i}:${j}" aria-pressed="${S.practice===i+':'+j}">${practiceLabels[v]}</button></td>`).join('')}</tr>`).join('')}</tbody></table></div><div class="gm-legend"><span>○ 未发现公开记录</span><span>● 有记录，真实性另核验</span><span>△ 仅自述 / 待核验</span></div>`+note('未知、未检查和不适用应另列；本矩阵不把它们折算成 0 分。点选任意单元格查看查证要求。');
  aside=side('项目 '+String.fromCharCode(65+r)+' · '+practiceCols[c],`<span class="gm-badge forecast">模拟状态：${practiceLabels[M.governance[r][c]]}</span><p>${['查找规则、议程、决议记录及实际执行时间。','查找参与门槛、晋升流程、提名与退出记录。','查找机构关联披露、回避规则及处理记录。','查找可用的申诉渠道、处理责任人和记录。','查找安全报告入口、响应责任与修复流程。','查找接班人、权限移交、归档与迁移说明。'][c]}</p>${note('示例证据字段：项目 ID、文件 URL、版本、核验日期、检查人、证据状态。此虚构项目没有真实证据链接。')}`);
 }else if(S.governance==='roles'){
  const R=M.roles;main=sim('同一虚构项目 K；每种角色独立计量')+`<div class="gm-role-bars">${R.roles.map((n,i)=>{let total=R.counts[i].reduce((a,b)=>a+b,0);return `<button class="gm-role-row" data-gm-set="role:${i}" aria-pressed="${S.role===i}"><span>${n}<small>${total} 个角色记录</small></span><span class="gm-stacked">${R.counts[i].map((v,j)=>`<i style="width:${v/total*100}%;background:${C[j]}">${Math.round(v/total*100)}%</i>`).join('')}</span></button>`;}).join('')}</div><div class="gm-legend">${R.actors.map((n,j)=>`<span><i style="background:${C[j]}"></i>${n}</span>`).join('')}</div>`+note('一人可同时承担多个角色，各行人数不能相加。机构关联需按同一观察期核验。');
  aside=side(R.roles[S.role],`<p>模拟角色记录按机构关联分组：</p><div class="gm-detail-list">${R.actors.map((n,j)=>`<div><span>${n}</span><b>${R.counts[S.role][j]}</b></div>`).join('')}</div><p>观察哪些参与者进入评审、合并、发布和委员会。</p>${note('贡献记录不直接推断表决权；角色数量也不代表实际决策影响力。')}`);
 }else if(S.governance==='foundation'){
  const count=S.foundation==='active_repositories',r=D.series.foundation.find(r=>r.year===S.year);
  main=`<div class="gm-controls">${buttons('foundation',[['active_repositories','活跃仓库数'],['foundation_project_openrank_share_pct','OpenRank 份额']],S.foundation)}${select('year',D.years.map(y=>[y,y]),S.year,'报告年')}</div><div class="gm-evidence gm-existing"><b>仓库已有 · 待口径与复现核验</b> · 2022—2026</div>`+line(D.series.foundation,[{key:S.foundation,label:count?'基金会活跃仓库':'基金会项目 OpenRank 份额'}],{unit:count?'个':'%'})+note('两类指标各用独立纵轴。份额分母和基金会项目清单尚待补充。');
  aside=side('基金会项目的五年观察',stat(String(S.year),num(r[S.foundation]),count?'个':'%')+`<p>2022 → 2026</p><strong class="gm-emphasis">${count?'+5.9%':'＋0.30 个百分点'}</strong><p>${count?'3,163 → 3,350 个活跃仓库':'2.63% → 2.93% 的 OpenRank 份额'}</p>`+note('此处不是 NeutralityRatio。正式托管比例需要同范围已核验托管项目与项目总体。'));
 }else{
  const keys=Object.keys(D.series.licenses[0]).filter(k=>k!=='year'),r=D.series.licenses.find(r=>r.year===S.year),m=D.series.mulan.find(r=>r.year===S.year);
  main=`<div class="gm-controls">${select('license',keys.map(k=>[k,k]),S.license,'许可证')}${select('year',D.years.map(y=>[y,y]),S.year,'报告年')}</div><div class="gm-evidence gm-existing"><b>仓库已有 · 待核验</b> · 五类许可数量，缺整体分母</div>`+line(D.series.licenses,[{key:S.license,label:S.license}],{unit:'活跃仓库 / 个'})+note('显示来源表中的五类许可证。多许可处理、受检总体与未知许可待补，不推算全局许可覆盖率。');
  aside=side(S.license,stat(String(S.year),num(r[S.license]),'个')+`<div class="gm-callout"><h5>本土实践 · 木兰宽松许可</h5><p>${S.year} 累计活跃仓库 <b>${m.cumulative_active_repositories}</b> 个</p><p>项目 OpenRank <b>${num(m.project_openrank_influence)}</b></p></div>`+note('木兰累计口径不等同当年活跃。许可数量和影响力的同步变化不能证明治理效果；宽松许可不等于更高公共价值。'));
 }
 $('#gm-governance').innerHTML=split(main,aside);foot('governance',['foundation','licenses'].includes(S.governance)?'来源：报告仓库三份原始 CSV · 文件名保留旧节号 2-6 · 时间窗及样本待核验':'模拟演示 · 逐项观察治理实践和实际角色 · 不生成治理总分');
}
function support(){let main='',aside='';const Q=M.support;
 if(S.support==='scatter'){
  const W=850,H=365,L=65,R=40,T=26,B=52,x=v=>L+v/1400*(W-L-R),y=v=>H-B-v/30*(H-T-B);let body='';
  for(const v of [0,6,12,18,24,30])body+=`<line x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}" class="gm-axis"/><text x="${L-12}" y="${y(v)+5}" text-anchor="end">${v}</text>`;
  for(const v of [0,300,600,900,1200])body+=`<text x="${x(v)}" y="${H-23}" text-anchor="middle">${v}</text>`;
  body+=`<text x="${L}" y="16">资金可支持月数 · 月（模拟）</text><text x="${W-R}" y="${H-3}" text-anchor="end">下游依赖项目数（模拟）</text><line x1="${L}" x2="${W-R}" y1="${y(S.threshold)}" y2="${y(S.threshold)}" stroke="var(--gm-gold)" stroke-width="2" stroke-dasharray="7 5"/><text x="${W-R}" y="${y(S.threshold)-8}" text-anchor="end">${S.threshold} 个月参考线</text>`;
  Q.project.forEach((n,i)=>{body+=`<g data-gm-set="project:${i}" tabindex="0" role="button" aria-label="项目 ${n}，依赖 ${Q.downstream[i]}，支持 ${Q.funding_months[i]} 个月，维护者 ${Q.maintainers[i]} 人，模拟" aria-pressed="${S.project===i}"><circle cx="${x(Q.downstream[i])}" cy="${y(Q.funding_months[i])}" r="${Math.sqrt(Q.maintainers[i])*6}" fill="var(--gm-teal)" fill-opacity=".2" stroke="${S.project===i?'var(--gm-gold)':'var(--gm-teal)'}" stroke-width="${S.project===i?3:2}"/><text x="${x(Q.downstream[i])+18}" y="${y(Q.funding_months[i])+5}">${n}</text></g>`;});
  main=`<div class="gm-controls">${select('project',Q.project.map((n,i)=>[i,'项目 '+n]),S.project,'查看')}${select('threshold',[[6,'6 个月'],[12,'12 个月'],[18,'18 个月'],[24,'24 个月']],S.threshold,'参考线')}</div>${sim('点面积表示活跃维护者数')}${svg('下游依赖与维护支持：虚构项目 A 至 J',body,W,H)}${note('参考线用于讨论支持周期，可调整；不是风险等级或安全结论。未知预算项目应另列。')}`;
  aside=side('虚构项目 '+Q.project[S.project],stat('可支持时长',Q.funding_months[S.project],'个月')+`<div class="gm-mini"><div><b>${Q.downstream[S.project]}</b><small>下游项目</small></div><div><b>${Q.maintainers[S.project]}</b><small>活跃维护者</small></div></div><p>后续核验：关键用途、维护预算、已确认资金、志愿投入及角色替补。</p>`+note('高依赖与较少支持的交集，是访谈和资助评估入口，不自动说明项目不安全。'));
 }else if(S.support==='workload'){
  const W=M.workload,rows=W.periods.map((period,i)=>({period,opened:W.opened[i],reviewed:W.reviewed[i],backlog:W.backlog[i]}));
  main=sim('虚构项目 K · 四个季度')+line(rows,[{key:'opened',label:'新进入 PR'},{key:'reviewed',label:'获人工评审 PR'},{key:'backlog',label:'期末未结 PR'}],{unit:'条',synthetic:true})+note('期初积压 20 条；每季结案 70 / 85 / 100 / 120 条。期末积压＝期初＋新进入－结案。获评审不等于结案。');
  aside=side('评审能力是否跟上？',stat('第四季 · 期末未结',170,'条')+'<p>新进入 190 条；获得人工评审 124 条。评审条目可来自往期积压，不能据此计算当季评审率。</p>'+note('应同时观察首次人工响应、结案时间、未解决分布和变更复杂度。不能从活动曲线判断 AI 贡献比例。'));
 }else if(S.support==='funding'){
  const F=M.funding;main=sim('已确认现金支持结构；不含志愿劳动')+`<div class="gm-role-bars">${F.projects.map((n,i)=>`<button class="gm-role-row" data-gm-set="fund:${i}" aria-pressed="${S.fund===i}"><span>项目 ${n}</span><span class="gm-stacked">${F.mix[i].map((v,j)=>v?`<i style="width:${v}%;background:${C[j]}">${v}%</i>`:'').join('')}</span></button>`).join('')}</div><div class="gm-legend">${F.sources.map((n,i)=>`<span><i style="background:${C[i]}"></i>${n}</span>`).join('')}</div>`+note('同一年度、同一项目内的支持结构，每行合计 100%。实物资源和未到账承诺单列，不能直接相加。');
  aside=side('虚构项目 '+F.projects[S.fund],'<div class="gm-detail-list">'+F.sources.map((n,j)=>`<div><span>${n}</span><b>${F.mix[S.fund][j]}%</b></div>`).join('')+'</div><p>来源集中意味着需要了解续约期限与替代安排；多来源本身也不保证稳定。</p>'+note('支持来源、资金时长与用途限制应联合观察，而不是只看总金额。'));
 }else{
  const R=M.succession;main=sim('虚构项目 K · 关键岗位接续')+`<div class="gm-table-wrap"><table><thead><tr><th>角色</th><th>主要承担者</th><th>可替补者</th><th>交接材料</th></tr></thead><tbody>${R.roles.map((n,i)=>`<tr><th>${n}</th><td>${R.primary[i]} 人</td><td>${R.backup[i]} 人</td><td>${R.handoff[i]}</td></tr>`).join('')}</tbody></table></div>`+note('“可替补”需验证权限、知识与可用时间。不同角色可能由同一人承担，不跨行汇总人数。');
  aside=side('接续是可持续性的一部分','<div class="gm-callout"><h5>模拟观察：安全响应</h5><p>1 位主要承担者，尚无可替补者。下一步应核验真实可用性与应急安排。</p></div><p>可以支持共同评审、发布演练、知识文档和权限交接。</p>'+note('归档也可以是合理生命周期选择；应观察是否有迁移说明和服务衔接。'));
 }
 $('#gm-support').innerHTML=split(main,aside);foot('support','模拟演示 · 维护过程、现金支持、志愿投入和角色接续分别观察');
}
function publicValue(){let main='',aside='';const P=M.public;
 if(S.public==='evidence'){
  const colors=C.slice(0,3),names=['有公共目标','有部署记录','有结果评价'];main=sim('同一场景内，后一级包含于前一级；可跨场景重复')+`<div class="gm-evidence-chart">${P.fields.map((n,i)=>`<button class="gm-evidence-row" data-gm-set="sector:${i}" aria-pressed="${S.sector===i}"><span>${n}</span><span class="gm-evidence-bars">${P.counts[i].map((v,j)=>`<i style="width:${v/28*100}%;background:${colors[j]}"><b>${v}</b></i>`).join('')}</span></button>`).join('')}</div><div class="gm-legend">${names.map((n,j)=>`<span><i style="background:${colors[j]}"></i>${n}</span>`).join('')}</div>`;
  aside=side(P.fields[S.sector],`<span class="gm-badge forecast">模拟条目 · 不表示真实项目覆盖</span><div class="gm-detail-list">${names.map((n,j)=>`<div><span>${n}</span><b>${P.counts[S.sector][j]}</b></div>`).join('')}</div><p>三层证据分别回答“想做什么”“在哪里使用”“观察到什么变化”。</p>`+note('领域可多标签，不能跨领域求全球去重总量。没有结果材料不等于没有价值，也不能视为已有改善。'));
 }else if(S.public==='partnership'){
  main=sim('虚构教育部署 E · 本地共建路径')+`<div class="gm-partners">${[['需求与选择','学校、教师与学生','记录任务、语言和可及性需求，参与方案选择。'],['共同适配','当地技术团队 + 上游','完成语言、弱网络与设备适配，保留变更记录。'],['部署与培训','实施机构 + 社区','明确数据责任、培训安排和服务支持入口。'],['持续维护','本地维护者 + 项目社区','跟踪问题修复、权限交接和下一年度预算。'],['回馈上游','本地伙伴 + 核心维护者','以代码、翻译、文档、案例与规则建议回馈。'],['结果评价','服务对象 + 评价团队','保留评价方法，记录改善、无变化和不利结果。']].map(([t,a,b],i)=>`<article><small>0${i+1}</small><h5>${t}</h5><b>${a}</b><p>${b}</p></article>`).join('')}</div>`;
  aside=side('本地能力留下了吗？','<p>谁提出需求、谁能调整方案、谁持续维护，应与部署记录一起保留。</p><div class="gm-callout"><h5>案例证据清单</h5><p>实施方 · 地点 · 时间<br>适配记录 · 培训材料<br>运维责任 · 上游回馈<br>评价方法 · 结果材料</p></div>'+note('此案例未声称获得 DPG 认可。正式案例应独立查验名录身份、有效期与核心方案版本。'));
 }else{
  const r=P.outcomes[S.outcome],max=Math.max(r.before,r.after)*1.25;
  main=`<div class="gm-controls">${select('outcome',P.outcomes.map((r,i)=>[i,r.name]),S.outcome,'案例')}</div>${sim('效果观察的呈现样例，不是因果结论')}<div class="gm-outcome"><h5>${r.metric}</h5>${[['观察前',r.before],['观察后',r.after]].map(([n,v],i)=>`<div><span>${n}</span><b style="width:${v/max*76}%;background:${C[i]}"></b><strong>${v}${r.unit}</strong></div>`).join('')}<p>${r.period} · 样本 ${r.n} · 全部数值虚构</p></div>`+note(r.caveat);
  aside=side('结果需要方法支持',`<p>对象：${r.name}<br>指标：${r.metric}<br>样本：${r.n} 条模拟记录</p><div class="gm-callout"><h5>正式采集时补充</h5><p>选择与退出规则、缺失记录、同期变化、评价机构及可复核材料。</p></div>`+note('下载量、注册数、实际服务人数与结果变化不可互换；跨项目也不简单加总受益人数。'));
 }
 $('#gm-public').innerHTML=split(main,aside);foot('public','模拟演示 · 公共目标、部署记录、结果评价分层 · 名录认可独立核验');
}
function ai(){let main='',aside='';const A=M.ai;
 if(S.ai==='matrix'){
  const names=['代码','模型','数据'],[r,c]=S.check.split(':').map(Number);
  main=sim('每类资产、每项检查的适用且已检查分母均设为 100')+`<div class="gm-table-wrap"><table class="gm-ai-table"><thead><tr><th>责任检查项</th>${names.map(n=>`<th>${n}</th>`).join('')}</tr></thead><tbody>${A.checks.map((n,i)=>`<tr><th>${n}</th>${names.map((_,j)=>`<td><button style="--coverage:${A.coverage[j][i]}%" data-gm-set="check:${j}:${i}" aria-pressed="${S.check===j+':'+i}">${A.coverage[j][i]}%</button></td>`).join('')}</tr>`).join('')}</tbody></table></div>`+note('比例表示“有可核验记录”的模拟覆盖；仅自述、未发现、不适用和未检查应独立保存。不建立加权总分。');
  aside=side(names[r]+' · '+A.checks[c],stat('有可核验记录 / 适用且已检查',A.coverage[r][c],'%')+`<p>${A.coverage[r][c]} / 100 个模拟样本</p><p>${['是否有明确责任主体、反馈入口与处理承诺？','能否连接来源、许可、版本及变更记录？','使用条件、再分发条件与适用范围是否明确？','已知限制、失败情境及风险是否有记录？','是否在当地语言、场景和设备条件下评测？','变更、修复、通知与撤回由谁执行？'][c]}</p>`+note('材料存在不证明内容真实；本地评测不自动适用于其他部署。未检查规模在本轮未设定。'));
 }else if(S.ai==='review'){
  const R=A.review;main=sim('同一季度的新提交队列，后续观察至同一截止日')+`<div class="gm-table-wrap"><table><thead><tr><th>来源标记</th><th>提交 PR</th><th>获人工评审</th><th>已合并</th></tr></thead><tbody>${R.groups.map((n,i)=>`<tr><th>${n}</th><td>${R.submitted[i]}</td><td>${R.human_reviewed[i]} <small>(${Math.round(R.human_reviewed[i]/R.submitted[i]*100)}%)</small></td><td>${R.merged[i]}</td></tr>`).join('')}</tbody></table></div><div class="gm-callout"><h5>把生产与审阅放在同一队列中观察</h5><p>记录来源标记、首次人工评审、合并、关闭和仍未解决状态。按变更规模与复杂度分层，再比较处理情况。</p></div>`;
  aside=side('标记需有依据','<p>“AI 辅助披露”来自作者声明或可靠记录；“自动化账户”来自账户类型。两者不等同。</p><p>该模拟设定中已合并条目均在获人工评审子集内；正式数据需验证实际合并规则。</p>'+note('无法可靠识别的来源应保留未知。不根据文本风格判断 AI 生成，也不由此比较贡献质量。'));
 }else{
  const P=A.permissions,[r,c]=S.permission.split(':').map(Number);
  main=sim('权限安排样例，不代表任何产品的默认设置')+`<div class="gm-table-wrap"><table class="gm-permission-table"><thead><tr><th>示例角色</th>${P.scopes.map(n=>`<th>${n}</th>`).join('')}</tr></thead><tbody>${P.actors.map((n,i)=>`<tr><th>${n}</th>${P.states[i].map((v,j)=>`<td><button data-gm-set="permission:${i}:${j}" class="gm-state-${v}" aria-pressed="${S.permission===i+':'+j}">${['未授予','限定授权','人工批准'][v]}</button></td>`).join('')}</tr>`).join('')}</tbody></table></div><div class="gm-callout"><h5>每项授权附带责任记录</h5><p>授权人 · 目标仓库 · 操作范围 · 有效期限 · 审批记录 · 撤回入口。合并与发布记录关联到具体版本。</p></div>`;
  aside=side(P.actors[r]+' · '+P.scopes[c],`<span class="gm-badge">${P.legend[P.states[r][c]]}</span><p>${['该角色在示例中未获得此项能力。需要时另行评估和授权。','仅在预先指定的资源与操作范围内执行，保留操作记录。','每次操作由明确的责任人审核批准；不能由既有贡献自动推导权限。'][P.states[r][c]]}</p>`+note('权限需要可撤回、可过期。贡献身份、决策权与发布责任分别记录。'));
 }
 $('#gm-ai').innerHTML=split(main,aside);foot('ai','模拟演示 · 跨资产逐项检查 · 不构成认证、安全承诺或统一评分');
}
const renders={world,governance,support,public:publicValue,ai};
const owner={country:'world',actor:'world',mock:'world',practice:'governance',role:'governance',year:'governance',foundation:'governance',license:'governance',project:'support',threshold:'support',fund:'support',sector:'public',outcome:'public',check:'ai',permission:'ai'};
const sourceText={world:['本轮地图三层全部为合成数据，10 个地区仅为演示样本。未知地域数量未设定，各层记录可能重复，不能相加。','组织登记地、维护者所在地、部署所在地分别存储；地图几何继承 V-Map / A-Map，中国包含台湾省。DPG 名录认可需另外核验，不由地图值推断。'],governance:['治理实践与角色分布使用虚构项目。已有基金会、许可与木兰 CSV 原值保留，显示编号改为 2-7-2，原文件名仍为 2-6。','报告年依词典为上年 7 月 1 日至当年 6 月 30 日；原表执行窗口、样本、OpenRank 分母及多许可处理待核验。Top5 许可没有总体分母，不能推算许可覆盖率。'],support:['全部为模拟。散点中依赖、资金月数和维护者数各自计量；12 个月仅是可调整的讨论参考。现金支持与实物、志愿劳动、未到账承诺分别记录。','积压使用期初＋新进入－结案核对。人工评审不等于结案。成熟低变更项目可能无需频繁提交，应结合情境解释。'],public:['全部为模拟场景和虚构部署。公共目标、部署记录、结果评价为嵌套证据层，不能堆叠相加。领域可多标签，不跨领域计算去重总量。','DPG 认可关注核心方案，不替代本地实施评价。正式证据需有项目、部署、实施方、时间、来源和方法；前后变化不直接证明因果。'],ai:['全部为模拟。每类资产每项适用且完成检查的分母设为 100。未检查规模未设定；不适用、自述待核验、未发现与已核验记录分别保存。','AI 来源标记需要披露或可靠记录。权限示例用于讨论责任安排，不代表产品默认权限，不构成标准认证或任意加权总分。']};
let lastSource=null;
function showSource(k){const o=$(`[data-gm-overlay="${k}"]`);lastSource=$(`[data-gm-source="${k}"]`);o.innerHTML=`<button class="gm-source-close" data-gm-close="${k}">返回图表 ×</button><span class="gm-eyebrow">METHOD & EVIDENCE</span><h4>口径与来源</h4>${sourceText[k].map(t=>`<p>${t}</p>`).join('')}<p><a href="${asset('simulation.json')}" download>模拟底表 ↓</a> · <a href="${asset('source-manifest.json')}" download>完整来源清单 ↓</a></p>${k==='governance'?'<ul>'+['fig-2-6-1_foundation_share_and_active_repositories.csv','fig-2-6-2_active_repository_license_trend.csv','fig-2-6-3_mulan_permissive_license_trend.csv'].map((f,i)=>`<li><a href="${asset(f)}" download>${['基金会五年原表','五类许可五年原表','木兰许可五年原表'][i]} ↓</a></li>`).join('')+'</ul>':''}<p class="gm-quiet">本轮是内容与交互评审；模拟值不进入真实世界结论。</p>`;o.hidden=false;o.querySelector('button').focus();}
function closeSource(k){$(`[data-gm-overlay="${k}"]`).hidden=true;lastSource?.focus();}
function set(k,v){S[k]=['role','year','project','threshold','fund','sector','outcome'].includes(k)?+v:k==='mock'?v==='yes':v;renders[owner[k]]();}
document.addEventListener('click',e=>{const t=e.target.closest('[data-gm-tab],[data-gm-set],[data-gm-source],[data-gm-close]');if(!t)return;if(t.dataset.gmTab){const [k,v]=t.dataset.gmTab.split(':');S[k]=v;$$(`[data-gm-tab^="${k}:"]`).forEach(b=>b.setAttribute('aria-pressed',b===t));renders[k]();}else if(t.dataset.gmSet){const [k,...rest]=t.dataset.gmSet.split(':');set(k,rest.join(':'));}else if(t.dataset.gmSource)showSource(t.dataset.gmSource);else closeSource(t.dataset.gmClose);});
document.addEventListener('change',e=>{const k=e.target.dataset.gmSelect;if(k)set(k,e.target.value);});
document.addEventListener('keydown',e=>{const b=e.target.closest('svg [data-gm-set]');if(b&&['Enter',' '].includes(e.key)){e.preventDefault();b.dispatchEvent(new MouseEvent('click',{bubbles:true}));}if(e.key==='Escape'){const o=$('.gm-source-overlay:not([hidden])');if(o){e.preventDefault();e.stopPropagation();closeSource(o.dataset.gmOverlay);}}},true);
Object.values(renders).forEach(fn=>fn());
})();
