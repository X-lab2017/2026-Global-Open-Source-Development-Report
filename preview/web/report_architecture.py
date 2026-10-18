"""Shared report architecture: one authored graph for home, front matter and Chapter 1."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
FRAME=[('sdg','UN SDGs','价值参照与研究启发','Shared values and inspiration','17 项可持续发展目标','17 sustainable development goals',28),('osdg','OSDGs','开源发展目标','Open source development goals','4 大支柱 · 10 个维度','4 pillars · 10 dimensions',460),('osdi','OSDI','开源发展目标指标体系','The OSDGs Indicator System','29 项指标 · 分项观测','29 indicators · distinct observations',892)]
CORE=[('GOSO','生态观测地图','Ecosystem maps','规模与结构','Scale and structure',28),('GOSR','影响力排行榜','Influence rankings','贡献与影响','Contribution and influence',342),('GOSL','技术全景洞察','Technology landscapes','分类与演进','Structure and evolution',656),('GOSM','大模型发展洞察','Open model ecosystems','供给、复用与开放','Supply, reuse and openness',970)]
COLORS=['#279FA9','#4E87C5','#9973B7','#82AE53']
EDGES=[('sdg','osdg','M388 195H460'),('osdg','osdi','M820 195H892')]
for i,c in enumerate(CORE):
 x=c[-1]+141;EDGES.extend([('osdi',c[0],f'M1072 244V282H{x}V310'),(c[0],'action',f'M{x} 416V444H640V469')])
def section_label(section,lang):
 title=section['title'][lang]
 if lang!='zh':return title
 short={'1.1':'共同创新与公共价值','1.2':'OSDGs 发展目标','1.3':'OSDI 指标与方法','6.1':'核心洞察与趋势展望','6.2':'政府与国际组织','6.3':'企业与组织','6.4':'社区与全球合作','6.5':'持续共同创造及其公共价值'}
 return short.get(section['number'],title.replace('全球开源','').replace('全球新势力开源项目排行榜','新势力项目排行榜').replace('全球行政区划影响力排行榜','行政区划影响力排行榜'))
def render(lang):
 t=lambda z,e:z if lang=='zh' else e;m=json.loads((ROOT/'content/manifest.json').read_text())
 out='<figure class="chapter-explorer logic-explorer architecture-flow" id="fig-report-logic" data-lang="'+lang+'" data-slide-key="structure"><div class="explorer-heading"><div><span class="eyebrow">GOSD / REPORT ARCHITECTURE</span><h3>'+t('从共同目标，到可验证的证据与行动','From shared goals to evidence and action')+'</h3><p>'+t('第一章建立价值与方法基础；四个研究板块交叉观察，第六章汇聚行动。','Shared goals support four research perspectives and a common direction for action.')+'</p></div></div><button type="button" class="architecture-foundation" data-logic-chapter="1" aria-controls="logic-detail-1" aria-expanded="true">'+t('第一章 · 价值、目标与方法','Chapter 1 · Values, goals and methods')+'</button><button type="button" class="architecture-motion" data-architecture-motion aria-pressed="false">'+t('流动连线','Animate links')+'</button><svg class="architecture-edges" viewBox="0 0 1280 800" aria-hidden="true"><defs><marker id="architecture-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L7 3.5L0 7" fill="var(--brand)"/></marker></defs>'
 for a,b,d in EDGES:out+='<path class="architecture-edge" data-arc-from="'+a+'" data-arc-to="'+b+'" d="'+d+'" marker-end="url(#architecture-arrow)"/>'
 out+='</svg>'
 for key,title,z,e,nz,ne,x in FRAME:
  out+='<button type="button" class="architecture-node architecture-framework" style="left:'+str(x)+'px" data-logic-framework="'+key+'" aria-controls="logic-framework-detail" aria-expanded="false"><b>'+title+'</b><strong>'+t(z,e)+'</strong><span>'+t(nz,ne)+'</span></button>'
 out+='<div class="architecture-stage-label">'+t('四个核心研究板块','FOUR COMPLEMENTARY RESEARCH PERSPECTIVES')+'</div>'
 for i,(code,z,e,nz,ne,x) in enumerate(CORE):
  out+='<button type="button" class="architecture-node architecture-core" style="left:'+str(x)+'px;--arc-color:'+COLORS[i]+'" data-logic-chapter="'+str(i+2)+'" aria-controls="logic-detail-'+str(i+2)+'" aria-expanded="false"><b>'+code+'</b><strong>'+t(z,e)+'</strong><span>'+t('第'+str(i+2)+'章 · '+nz,'Chapter '+str(i+2)+' · '+ne)+'</span></button>'
 out+='<button type="button" class="architecture-node architecture-action" data-logic-chapter="6" aria-controls="logic-detail-6" aria-expanded="false"><strong>'+t('第六章 · 从研究证据形成行动建议','Chapter 6 · From evidence to action')+'</strong><span>'+t('三项共同任务 · 九条主体建议','Three shared tasks · Nine actor recommendations')+'</span></button><div class="architecture-inspector">'
 for i,c in enumerate(m['chapters']):
  out+='<section class="logic-detail" id="logic-detail-'+str(i+1)+'"'+(' hidden' if i else '')+'><div class="architecture-detail-heading"><small>'+t('第'+str(i+1)+'章','CHAPTER '+str(i+1))+'</small><h4>'+E(c['title'][lang].split('（')[0])+'</h4><p>'+E(c['question'][lang])+'</p>'
  if i==5:out+='<div class="logic-shared-tasks"><small>'+t('五个小节 · 三项共同任务 · 九条主体建议','Five sections · Three tasks · Nine recommendations')+'</small></div>'
  out+='</div><nav class="architecture-section-links" aria-label="'+t('选择小节','Choose a section')+'">'
  for sec in c['sections']:out+='<a href="/2026/'+lang+'/'+c['route']+'#'+sec['id']+'" aria-label="'+E(sec['number']+' '+sec['title'][lang])+'"><b>'+sec['number']+'</b><span>'+E(section_label(sec,lang))+'</span><i aria-hidden="true">↗</i></a>'
  out+='</nav></section>'
 out+='<section id="logic-framework-detail" hidden aria-live="polite"></section></div><figcaption>'+t('图 1-0-1 · 六章共同指向持续共同创造及其公共价值。连线表示研究路径，不代表评分权重。','Figure 1-0-1 · Six chapters connect sustained co-creation and public value. Links show the research path, not scoring weights.')+'</figcaption></figure>'
 return out

def static_svg():
 o=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800"><rect width="1280" height="800" fill="#f4f8fa"/><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L7 3.5L0 7" fill="#6c8793"/></marker></defs><g font-family="Noto Sans CJK SC,sans-serif" fill="#18394c">']
 def text(x,y,s,size=18,fill='#18394c',weight=400):o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{E(s)}</text>')
 def box(x,y,w,h,fill='#fff'):o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="#cadce5"/>')
 text(28,44,'GOSD / REPORT ARCHITECTURE',14,'#267386',600);text(28,88,'从共同目标，到可验证的证据与行动',32,weight=600);text(28,120,'第一章建立价值与方法基础；四个研究板块交叉观察，第六章汇聚行动。',17,'#587382')
 for a,b,d in EDGES:o.append(f'<path d="{d}" fill="none" stroke="#6c8793" stroke-width="2" marker-end="url(#arrow)"/>')
 for key,title,z,e,nz,ne,x in FRAME:
  box(x,146,360,98);text(x+20,177,title,23,weight=600);text(x+20,205,z,18);text(x+20,230,nz,14,'#587382')
 text(28,267,'四个核心研究板块',15,weight=600)
 for i,(code,z,e,nz,ne,x) in enumerate(CORE):
  box(x,310,282,106);text(x+20,343,code,26,COLORS[i],600);text(x+20,373,z,19,weight=600);text(x+20,400,'第'+str(i+2)+'章 · '+nz,14,'#587382')
 box(390,469,500,76,'#18394c');text(440,502,'第六章 · 从研究证据形成行动建议',22,'#fff',600);text(486,530,'三项共同任务 · 九条主体建议',16,'#d7e5ed')
 box(28,582,1224,145);text(52,619,'一条贯穿全书的研究路径',20,weight=600)
 for i,line in enumerate(['以共同目标组织观察，结合地图、榜单、技术全景与模型生态理解发展。','从研究证据形成可落实、可追踪的行动，支持持续共同创造及其公共价值。']):text(52,658+i*32,line,20,'#587382')
 text(28,777,'图 1-0-1 · 连线表示研究路径，不代表评分权重；四大支柱交叉服务于各研究板块。',14,'#587382');o.append('</g></svg>');return ''.join(o)
if __name__=='__main__':
 p=ROOT.parent/'figures/chapter1/fig-1-0-1_report_logic.svg';p.write_text(static_svg());p.with_name('fig-1-0-1_report_logic.editable.svg').write_text(static_svg());print(p)
