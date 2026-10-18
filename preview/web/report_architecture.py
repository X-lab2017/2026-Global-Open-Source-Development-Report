"""The report's chapter map, shown once in Chapter 1 and reused in presentation."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
COLORS=['#279FA9','#4E87C5','#9973B7','#82AE53']
CORE=[('GOSO',['全球开源生态','观测地图'],['Global open source','ecosystem maps'],'规模与结构','Scale and structure'),('GOSR',['全球开源','影响力排行榜'],['Global open source','influence rankings'],'主体与影响','Actors and influence'),('GOSL',['全球开源技术','全景洞察'],['Global open source','technology landscapes'],'分类与演进','Structure and evolution'),('GOSM',['全球开源大模型','发展洞察'],['Global open model','development'],'供给、复用与开放','Supply, reuse and openness')]
QUESTIONS=[('为什么研究开源，如何用证据观察发展？','Why study open source, and how can evidence reveal its development?'),('参与、贡献与开放资产，在哪里积累？','Where do participation, contributions and open assets accumulate?'),('哪些地区、组织与项目形成关键影响？','Which regions, organizations and projects shape the ecosystem?'),('技术如何分类，各领域怎样演进？','How are technologies organized, and how do they evolve?'),('模型由谁供给，怎样复用与开放？','Who supplies models, and how are they reused and opened?'),('不同主体可以采取哪些共同行动？','What shared actions can different participants take?')]
EDGES=[]
for i in range(4):
 x=129+i*222
 EDGES.extend([('1',str(i+2),f'M462 264V320H{x}V350'),(str(i+2),'6',f'M{x} 526V560H462V612')])
SHORT_EN={'1.1':'Co-creation and public value','1.2':'OSDGs: development goals','1.3':'OSDI: indicators and methods','2.1':'Activity','2.2':'Contribution','2.3':'Project influence','2.4':'Talent','2.5':'Assets','2.6':'Diversity','2.7':'Governance and public value','3.1':'Regions','3.2':'Companies','3.3':'Foundations','3.4':'Projects','3.5':'Emerging projects','3.6':'Models','4.1':'Agentic AI','4.2':'AI models','4.3':'Cloud infrastructure','4.4':'Databases','4.5':'RISC-V','4.6':'PyTorch','5.1':'Supply and contribution','5.2':'Networks and influence','5.3':'Openness and classification','6.1':'Findings and outlook','6.2':'Governments and institutions','6.3':'Companies and organizations','6.4':'Communities and cooperation','6.5':'Sustained co-creation'}
def section_label(section,lang):
 if lang=='en':return SHORT_EN.get(section['number'],section['title'][lang])
 short={'1.1':'共同创新与公共价值','1.2':'OSDGs 发展目标','1.3':'OSDI 指标与方法','6.1':'核心洞察与趋势展望','6.2':'政府与国际组织','6.3':'企业与组织','6.4':'社区与全球合作','6.5':'持续共同创造及其公共价值'}
 return short.get(section['number'],section['title'][lang].replace('全球新势力开源项目排行榜','新势力项目排行榜').replace('全球开源','').replace('全球行政区划影响力排行榜','行政区划影响力排行榜'))
def render(lang):
 t=lambda z,e:z if lang=='zh' else e;m=json.loads((ROOT/'content/manifest.json').read_text())
 out='<figure class="chapter-explorer logic-explorer architecture-flow" id="fig-report-logic" data-lang="'+lang+'" data-slide-key="structure"><div class="explorer-heading"><div><span class="eyebrow">GOSD / READING THE REPORT</span><h3>'+t('六章，一条清晰的阅读路径','Six chapters, one clear reading journey')+'</h3><p>'+t('第一章建立基础；第二至第五章提供互补观察；第六章汇聚行动。','Chapter 1 sets the foundation; Chapters 2–5 provide evidence; Chapter 6 brings it into action.')+'</p></div></div><button type="button" class="architecture-motion" data-architecture-motion aria-pressed="false">'+t('流动连线','Animate links')+'</button><svg class="architecture-edges" viewBox="0 0 1280 800" aria-hidden="true"><defs><marker id="architecture-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L7 3.5L0 7" fill="var(--brand)"/></marker></defs>'
 for a,b,d in EDGES:out+='<path class="architecture-edge" data-arc-from="'+a+'" data-arc-to="'+b+'" d="'+d+'" marker-end="url(#architecture-arrow)"/>'
 out+='</svg><div class="architecture-stage-label stage-foundation">'+t('01 / 建立共同基础','01 / ESTABLISH A SHARED FOUNDATION')+'</div><button type="button" class="architecture-node architecture-foundation" data-logic-chapter="1" aria-controls="logic-detail-1" aria-expanded="false"><small>'+t('第一章','CHAPTER 1')+'</small><strong>'+E(m['chapters'][0]['title'][lang])+'</strong><span>'+t('价值参照 → 发展目标 → 观察指标','Shared values → Development goals → Observation indicators')+'<em>SDGs · OSDGs · OSDI</em></span></button>'
 out+='<div class="architecture-stage-label stage-research">'+t('02 / 四个互补视角，可按问题选择阅读','02 / FOUR PERSPECTIVES — FOLLOW YOUR QUESTION')+'</div>'
 for i,(code,z,e,nz,ne) in enumerate(CORE):
  out+='<button type="button" class="architecture-node architecture-core" style="left:'+str(28+i*222)+'px;--arc-color:'+COLORS[i]+'" data-logic-chapter="'+str(i+2)+'" aria-controls="logic-detail-'+str(i+2)+'" aria-expanded="false"><small>'+t('第'+str(i+2)+'章','CHAPTER '+str(i+2))+'</small><strong>'+'<br>'.join(z if lang=='zh' else e)+'</strong><b>'+code+'</b><span>'+t(nz,ne)+'</span></button>'
 out+='<div class="architecture-stage-label stage-action">'+t('03 / 从研究走向行动','03 / CONNECT RESEARCH TO ACTION')+'</div><button type="button" class="architecture-node architecture-action" data-logic-chapter="6" aria-controls="logic-detail-6" aria-expanded="false"><small>'+t('第六章','CHAPTER 6')+'</small><strong>'+E(m['chapters'][5]['title'][lang])+'</strong><span>'+t('三项共同任务 · 九条主体建议','Three shared tasks · Nine actor recommendations')+'</span></button>'
 out+='<aside class="architecture-inspector" aria-label="'+t('章节阅读入口','Chapter reading links')+'"><div class="architecture-inspector-bar"><span>'+t('选章阅读','CHAPTER GUIDE')+'</span><button type="button" data-architecture-reset hidden>'+t('返回导读','Reading guide')+'</button></div><section class="architecture-start" id="logic-start"><small>'+t('从全貌到具体问题','FROM OVERVIEW TO YOUR QUESTION')+'</small><h4>'+t('你想从哪里开始？','Where would you like to begin?')+'</h4><p>'+t('点选左侧章节，在这里查看该章的问题与小节。','Select a chapter on the left to see its question and sections here.')+'</p><nav class="architecture-start-links">'
 for route,z,e,detail,ed in [('chapters/01/#ch01-s01','顺序阅读','Read in sequence','从 1.1 共同创新与公共价值开始','Begin with co-creation and public value'),('','按需查阅','Browse by topic','打开全书目录，直接进入小节','Open the contents and choose a section'),('chapters/06/','关注行动','Explore the actions','查看三项共同任务与九条建议','Explore three tasks and nine recommendations')]:
  out+='<a href="/2026/'+lang+'/'+route+'"><strong>'+t(z,e)+' ↗</strong><span>'+t(detail,ed)+'</span></a>'
 out+='</nav></section>'
 for c in m['chapters']:
  n=c['number'];out+='<section class="logic-detail" id="logic-detail-'+n+'" hidden><div class="architecture-detail-heading"><small>'+t('第'+n+'章','CHAPTER '+n)+'</small><h4>'+E(c['title'][lang].split('（')[0])+'</h4><p>'+E(QUESTIONS[int(n)-1][0 if lang=='zh' else 1])+'</p></div><nav class="architecture-section-links" aria-label="'+E(c['title'][lang])+'">'
  for sec in c['sections']:out+='<a href="/2026/'+lang+'/'+c['route']+'#'+sec['id']+'" aria-label="'+E(sec['number']+' '+sec['title'][lang])+'"><b>'+sec['number']+'</b><span>'+E(section_label(sec,lang))+'</span><i aria-hidden="true">↗</i></a>'
  out+='</nav><a class="architecture-read-chapter" href="/2026/'+lang+'/'+c['route']+'">'+t('阅读本章全文 →','Read the complete chapter →')+'</a></section>'
 out+='</aside><figcaption>'+t('图 1-0-1 · 共同目标组织观察，研究证据连接行动。点选章节可查看阅读入口。','Figure 1-0-1 · Shared goals organize observations; evidence informs action. Select a chapter to explore.')+'</figcaption></figure>'
 return out

def static_svg():
 o=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800"><rect width="1280" height="800" fill="#f4f8fa"/><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#6c8793"/></marker></defs><g font-family="Noto Sans CJK SC,sans-serif" fill="#18394c">']
 def text(x,y,s,size=18,fill='#18394c',weight=400):o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{E(s)}</text>')
 def box(x,y,w,h,fill='#fff'):o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="#cadce5"/>')
 text(28,44,'GOSD / READING THE REPORT',13,'#267386',600);text(28,88,'六章，一条清晰的阅读路径',32,weight=600);text(28,119,'第一章建立基础；第二至第五章提供互补观察；第六章汇聚行动。',16,'#587382')
 for a,b,d in EDGES:o.append(f'<path d="{d}" fill="none" stroke="#6c8793" stroke-width="1.5" marker-end="url(#arrow)"/>')
 for y,label in [(147,'01 / 建立共同基础'),(302,'02 / 四个互补视角，可按问题选择阅读'),(594,'03 / 从研究走向行动')]:text(28,y,label,13,'#587382',500)
 box(28,164,868,100);text(48,190,'第一章',13,'#267386',600);text(48,220,'从开放协作到公共价值',25,weight=600);text(48,246,'价值参照 → 发展目标 → 观察指标',16,'#587382');text(630,246,'SDGs · OSDGs · OSDI',13,'#587382')
 for i,(code,z,e,nz,ne) in enumerate(CORE):
  x=28+i*222;box(x,350,202,176);o.append(f'<path d="M{x+6} 350H{x+196}" stroke="{COLORS[i]}" stroke-width="3"/>');text(x+16,378,'第'+str(i+2)+'章',13,'#267386',600)
  for j,line in enumerate(z):text(x+16,411+j*29,line,21,weight=600)
  text(x+16,475,code,17,COLORS[i],600);text(x+16,505,nz,13,'#587382')
 box(28,612,868,112);text(48,640,'第六章',13,'#267386',600);text(48,672,'未来展望与行动建议',25,weight=600);text(48,701,'三项共同任务 · 九条主体建议',16,'#587382')
 box(930,164,322,560,'#edf3f6');text(950,194,'阅读导引',13,'#267386',600);text(950,236,'从全貌到具体问题',22,weight=600)
 for y,head,lines in [(292,'顺序阅读',['第一章建立价值与方法基础，','再进入各章的研究与行动。']),(414,'按需查阅',['第二至第五章是互补视角，','可按关心的问题选择阅读。']),(536,'关注行动',['第六章连接三项共同任务','与九条主体建议。'])]:
  text(950,y,head,19,weight=600)
  for j,line in enumerate(lines):text(950,y+31+j*27,line,16,'#587382')
 text(28,777,'图 1-0-1 · 共同目标组织观察，研究证据连接行动。连线表示篇章联系，不代表评分权重。',13,'#587382');o.append('</g></svg>');return ''.join(o)
if __name__=='__main__':
 p=ROOT.parent/'figures/chapter1/fig-1-0-1_report_logic.svg';p.write_text(static_svg());p.with_name('fig-1-0-1_report_logic.editable.svg').write_text(static_svg());print(p)
