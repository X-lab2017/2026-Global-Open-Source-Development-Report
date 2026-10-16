/* One illustrative case, three measurement lenses. No simulated OpenRank scores. */
(()=>{'use strict';
const people=[
 {id:'lin',name:'小林',country:'A 国',projects:[0,1],role:'提出问题、提交修复',community:'小林提出水情显示问题，并提交修复 PR；他的作用由具体协作关系来理解。'},
 {id:'maya',name:'Maya',country:'C 国',projects:[0,2],role:'评审代码',community:'Maya 评审修复方案，帮助改进代码。评审与提交共同构成社区协作。'},
 {id:'ana',name:'Ana',country:'D 国',projects:[0,2],role:'讨论与验证',community:'Ana 在 Issue 中补充复现信息并反馈验证结果，让问题能够被共同解决。'},
 {id:'leo',name:'Leo',country:'B 国',projects:[0,1],role:'维护与合入',community:'Leo 维护水情工具，检查并合入修改；维护工作也是贡献网络的一部分。'},
 {id:'sam',name:'Sam',country:'E 国',projects:[2],role:'参与另一项目',community:'Sam 本期参与公共地图，未参与水情工具；他的贡献应在相应社区中观察。'}
];
const projects=[{title:'水情工具',sub:'面向公共需求的开源工具',owner:'B 国主体发起',ids:[0,1,2,3]}, {title:'数据工具',sub:'整理与复用开放数据',owner:'C 国主体发起',ids:[0,3]}, {title:'公共地图',sub:'呈现社区中的公共信息',owner:'D 国主体发起',ids:[1,2,4]}];
const lenses=[
 {name:'参与',metric:'活跃开发者规模',code:'DevScale',question:'有多少人在行动？',summary:'看人群规模',map:10,
  steps:['发生参与','按人去重','观察规模'],
  titles:['先看见具体的参与者','跨项目参与，仍然是同一个人','本期活跃规模：5 人'],
  descriptions:['同一统计期内，5 位开发者在 3 个项目中发生有效协作。先识别人，再观察参与规模。','小林同时参与水情工具和数据工具。跨项目汇总时，同一身份只计一次。','示例中共有 9 组“人—项目”参与关系；按人去重后，是 5 位活跃开发者。'],
  object:'统计期内发生有效协作的开发者',method:'统一时间、平台范围与身份口径',result:'计量结果：人数。开发者总量另行统计。'},
 {name:'贡献',metric:'社区 OpenRank 贡献度',code:'OpenRankContrib',question:'在社区中发挥什么作用？',summary:'看社区协作',map:11,
  steps:['进入社区','展开协作','理解贡献'],
  titles:['进入“水情工具”社区','一次修复，需要多种协作','从协作网络理解贡献'],
  descriptions:['把镜头移到一个项目内部：Issue、PR 和参与者共同组成更细致的协作网络。','小林提出问题并修复；Ana 补充验证；Maya 评审；Leo 合入。不同角色共同推进项目。','社区 OpenRank 结合协作单元、行为关系及历史信息评价贡献，帮助看见多种贡献角色。'],
  object:'项目内的开发者、Issue 与 PR',method:'通过社区协作网络评价贡献',result:'计量结果：贡献度。本例不演算分值。'},
 {name:'影响力',metric:'全域 OpenRank 影响力',code:'OpenRankInflu',question:'在全球网络中处于什么位置？',summary:'看全域联系与长期积累',map:12,
  steps:['拉远镜头','连接项目','加入时间'],
  titles:['拉远到跨项目的协作网络','开发者连接不同项目','网络联系，也包含历史积累'],
  descriptions:['全域网络包含开发者与仓库。本例用 3 个单仓库项目，展示其中一小部分关系。','小林连接水情工具与数据工具；Maya 和 Ana 连接水情工具与公共地图。项目通过开发者产生联系。','有影响力的项目吸引深入参与；开发者也在协作中积累影响力。评价部分继承历史，关注长期建设。'],
  object:'全域开发者—仓库协作网络',method:'关系网络与历史积累共同参与评价',result:'此处观察项目侧影响力；全域算法也评价开发者。'}
];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const px=i=>100+i*200;
function icon(kind,x,y){const shapes={repo:'M2 3h19v22H2z M7 3v22 M11 9h6 M11 14h6',person:'M15 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10 M4 28v-3a11 11 0 0 1 22 0v3',issue:'M14 2a12 12 0 1 0 0 24 12 12 0 0 0 0-24 M14 8v8 M14 20h.1',pr:'M5 7v15 M20 22V10q0-5-7-5 M5 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6 M5 21a3 3 0 1 0 0 6 3 3 0 0 0 0-6 M20 21a3 3 0 1 0 0 6 3 3 0 0 0 0-6',check:'M3 14l7 7L25 5'};return `<g transform="translate(${x} ${y})" class="cl-icon"><path d="${shapes[kind]}"/></g>`;}
function person(i,s,inactive=false){const p=people[i],selected=s.person===p.id;return `<g class="cl-person ${selected?'is-selected':''} ${inactive?'is-outside':''}" transform="translate(${px(i)-76} 228)" data-concept-person="${p.id}" role="button" tabindex="0" aria-pressed="${selected}" aria-label="追踪 ${p.name}，${p.country}，${p.role}"><title>${p.name} · ${p.role}；点击追踪</title><rect width="152" height="60" rx="12"/>${icon('person',12,13)}<text x="51" y="26" class="cl-person-name">${p.name}</text><text x="51" y="46" class="cl-small">${p.country}${inactive?' · 其他社区':''}</text></g>`;}
function badge(i,x,y,s){return `<g class="cl-member ${s.person===people[i].id?'is-selected':''}" transform="translate(${x} ${y})" data-concept-person="${people[i].id}" role="button" tabindex="0" aria-pressed="${s.person===people[i].id}" aria-label="追踪 ${people[i].name}"><rect width="57" height="26" rx="6"/><text x="28.5" y="18" text-anchor="middle">${people[i].name}</text></g>`;}
function edge(i,j,s,extra=''){const selected=!s.person||s.person===people[i].id;return `<path class="cl-link ${selected?'is-related':'is-muted'} ${extra}" pathLength="1" style="--i:${i+j}" d="M${px(i)} 228 C${px(i)} 180 ${172+j*328} 195 ${172+j*328} 143"/>`;}
function project(j,s){const p=projects[j],related=!s.person||people.find(x=>x.id===s.person).projects.includes(j),x=24+j*328;
 return `<g class="cl-project ${related?'is-related':'is-muted'}" transform="translate(${x} 22)">${s.lens===2&&s.step===2?'<rect class="cl-history" x="-5" y="-8" width="296" height="120" rx="12"/><rect class="cl-history" x="5" y="-4" width="296" height="120" rx="12"/>':''}<rect class="cl-project-face" width="296" height="121" rx="12"/>${icon('repo',18,20)}<text x="57" y="38" class="cl-project-name">${p.title}</text><text x="18" y="68" class="cl-small">${s.lens===2?p.owner:p.sub}</text>${s.lens===0?p.ids.map((i,k)=>badge(i,18+k*64,83,s)).join(''):`<text x="18" y="99" class="cl-repo-meta">${p.ids.length} 位示例参与者 · 单仓库项目</text>`}</g>`;
}
function participation(s){let paths='';if(s.step>0)for(let j=0;j<3;j++)for(const i of projects[j].ids)paths+=edge(i,j,s);
 let traces='';if(s.step===1)projects.forEach((p,j)=>p.ids.forEach((i,k)=>{const x=24+j*328+18+k*64,y=105;traces+=`<g class="cl-dedup-trail" transform="translate(${x} ${y})" aria-hidden="true"><g style="--dx:${px(i)-28-x}px;--dy:${241-y}px;--delay:${(j+k)*80}ms"><rect width="57" height="26" rx="6"/><text x="28.5" y="18" text-anchor="middle">${people[i].name}</text></g></g>`;}));return paths+projects.map((_,j)=>project(j,s)).join('')+people.map((_,i)=>person(i,s)).join('')+traces+`<text class="cl-diagram-caption" x="500" y="318" text-anchor="middle">${['同一批人，参与不同项目','按身份合并跨项目记录；小林仍只计 1 人','本期 9 组参与关系 → 去重后 5 位活跃开发者'][s.step]}</text>`;
}
function contribution(s){const selected=s.person,rels=[[0,0],[2,0],[0,1],[1,1],[3,1]],items=[['issue','Issue #12','水位显示异常','小林提出 · Ana 补充验证'],['pr','PR #18','修复水位读取','小林提交 · Maya 评审'],['repo','水情工具','修复进入项目','Leo 检查并合入']];
 let out=s.step>0?rels.map(([i,j])=>edge(i,j,s)).join(''):'';
 if(s.step>0)out+='<path class="cl-workflow" pathLength="1" d="M320 84H352 M648 84H680"/><path class="cl-arrow" d="m344 79 8 5-8 5 m328-10 8 5-8 5"/>';
 items.forEach(([kind,title,desc,role],j)=>{const relevant=!selected||(j===0?['lin','ana']:j===1?['lin','maya','leo']:['lin','maya','ana','leo']).includes(selected);out+=`<g style="--j:${j}" class="cl-artifact ${relevant?'is-related':'is-muted'}" transform="translate(${24+j*328} 22)"><rect width="296" height="121" rx="12"/>${icon(kind,18,20)}<text x="58" y="38" class="cl-project-name">${title}</text><text x="18" y="68" class="cl-artifact-title">${desc}</text><text x="18" y="100" class="cl-small">${role}</text></g>`;});
 out+=people.map((_,i)=>person(i,s,i===4)).join('');
 return out+`<text class="cl-diagram-caption" x="500" y="318" text-anchor="middle">${['项目内部：开发者与 Issue、PR 之间的协作','提出、讨论、提交、评审与合入，共同推进一次修复','观察协作中的作用与关系，而不只累计操作次数'][s.step]}</text>`;
}
function influence(s){let out='';for(let j=0;j<3;j++)for(const i of projects[j].ids)out+=edge(i,j,s,s.step>0?'cl-global-link':'');
 out+=projects.map((_,j)=>project(j,s)).join('')+people.map((_,i)=>person(i,s)).join('');
 return out+`<g class="cl-diagram-history"><text class="cl-diagram-caption" x="500" y="318" text-anchor="middle">${['从社区内部，拉远到开发者—项目网络','开发者是跨项目的桥梁；点击人物，追踪他的连接','历史积累 ＋ 本期协作 → 本期全域网络评价'][s.step]}</text></g>`;
}
function svg(s){return `<svg class="cl-scene-svg" viewBox="0 0 1000 332" aria-label="${lenses[s.lens].metric}原理示意：虚构的五位开发者与三个项目"><title>${lenses[s.lens].titles[s.step]}</title><desc>虚构案例，用于解释指标原理。人物和项目不是报告实测样本，不计算 OpenRank 分值。可点击人物追踪关系。</desc>${[participation,contribution,influence][s.lens](s)}</svg>`;}
function personNote(s){const p=people.find(x=>x.id===s.person);if(!p)return ['点击图中任一人物','追踪同一位开发者，观察三个视角下的不同含义。'];if(s.lens===0)return [p.name+' · 参与者',`${p.name}参与${p.projects.map(i=>projects[i].title).join('、')}；本期活跃人数中只计 1 人。`];if(s.lens===1)return [p.name+' · '+p.role,p.community];return [p.name+' · '+(p.projects.length>1?'跨项目连接':'项目参与'),`${p.name}${p.projects.length>1?'连接':'参与'}${p.projects.map(i=>projects[i].title).join('与')}。评价还需结合全域关系与历史。`];}
function html(s){const c=lenses[s.lens],note=personNote(s);return `<div class="deck-concept cl-explainer" data-lens="${s.lens}" data-step="${s.step}" data-playing="${s.playing}">
 <div class="cl-lenses" role="group" aria-label="三个观察视角">${lenses.map((x,i)=>`<button data-detail="${i}" aria-pressed="${s.lens===i}"><span class="cl-lens-number">0${i+1}</span><strong>${x.name}</strong><span class="cl-lens-question">${x.question}</span><small>${x.metric}</small></button>`).join('')}</div>
 <div class="cl-case-toolbar"><span><b>同一个案例</b> · 5 位开发者，共建 3 个开放工具 <em>虚构示例</em></span><div><button data-concept-action="play" aria-pressed="${s.playing}">${s.playing?'Ⅱ 暂停讲解':'▶ '+(s.lens===2&&s.step===2?'重新讲解':'连续讲解')}</button><button data-concept-action="reset">↺ 重置</button><button data-concept-action="sources">口径与来源</button></div></div>
 <div class="cl-main"><section class="cl-visual" aria-label="协作案例演示"><div class="cl-scene-heading"><span>${['观察人群 · 去重计数','进入社区 · 看见具体协作','拉远镜头 · 全域关系与时间'][s.lens]}</span><small>点击人物，追踪关系</small></div><div class="cl-scene" data-scene-key="${s.lens}-${s.step}">${svg(s)}</div><div class="cl-steps" role="group" aria-label="本视角的三个讲解步骤">${c.steps.map((x,i)=>`<button data-concept-step="${i}" aria-pressed="${s.step===i}"><span>${i+1}</span>${x}<i aria-hidden="true"></i></button>`).join('')}</div></section>
 <aside class="cl-explanation"><div class="cl-metric">${c.metric}<code>${c.code}</code></div><h3>${c.titles[s.step]}</h3><p class="cl-description">${c.descriptions[s.step]}</p><div class="cl-person-note" aria-live="polite"><strong>${note[0]}</strong><p>${note[1]}</p></div><div class="cl-result">${c.result}</div><button class="cl-map-link" data-jump="${c.map}">进入 ${['V-Map 活跃地图','C-Map 贡献地图','I-Map 影响力地图'][s.lens]} →</button></aside></div>
 <div class="cl-takeaway ${s.geography?'is-geography':''}">${s.geography?'<div><strong>同一次跨国协作，两种地域观察</strong><p>A 国的小林，为 B 国主体发起的水情工具贡献。贡献来源看人在哪里；项目影响力看经核验的项目主体归属。这是两种观察，并非同一分值的转移。</p></div>':'<div><strong>参与看规模 · 贡献看社区协作 · 影响力看全域联系与长期积累</strong><p>同一段协作，从三个视角理解；三类指标各自测量，彼此补充。</p></div>'}<button data-concept-action="geography" aria-pressed="${s.geography}">${s.geography?'返回概念要点 ↶':'为什么国家格局不同？ →'}</button></div></div>`;}
function sources(base){return `<p><b>示例边界：</b>5 位开发者、3 个单仓库项目及其行为均为虚构的机制演示。人数从本例身份与参与关系计算；未计算或预测 OpenRank 分值。线条表示协作关系，出现顺序用于讲解，不表示算法迭代或因果效果。</p><p><b>参与：</b>使用本报告 DevScale 工作定义：统计期内至少发生一次纳入范围的有效协作行为，按可核验身份去重。实际报告需要披露平台覆盖、机器人过滤和跨平台身份映射；账号总量与本期活跃人数分开观察。</p><p><b>贡献：</b>社区 OpenRank 使用项目内部的 Issue、PR 等协作数据构建网络。图中只展示一次修复的部分关系；真实评价使用完整社区网络与对应参数。跨社区、跨期和地域聚合须随数据说明。</p><p><b>影响力：</b>全域 OpenRank 的网络同时包含开发者与仓库，二者通过协作关系联系；共享开发者让项目相互联系。本例未把项目投影图当作实际计算网络。算法部分继承历史；本页及 I-Map 重点解释项目侧，开发者侧见人才观察。</p><p><b>地域聚合：</b>贡献来源采用开发者所在地；项目侧影响力使用经核验的项目主体归属。多仓库项目、组织和国家的汇总遵循报告披露的映射与聚合规则，不默认把任意仓库值相加；未知归属另列。</p><ul><li><a href="https://open-digger.cn/docs/user-docs/metrics/community-openrank" target="_blank" rel="noopener noreferrer">OpenDigger · 社区 OpenRank 贡献度 ↗</a></li><li><a href="https://open-digger.cn/docs/user-docs/metrics/global-openrank" target="_blank" rel="noopener noreferrer">OpenDigger · 全域 OpenRank 影响力 ↗</a></li><li><a href="${base}/assets/report/osdi_indicator_dictionary.csv" target="_blank" rel="noopener noreferrer">本报告 · OSDI 指标字典 ↗</a></li></ul>`;}
window.GOSDConcept=Object.freeze({html,sources,people,lenses});
})();
