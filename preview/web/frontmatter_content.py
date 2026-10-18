"""Publication entry pages backed by the canonical front-matter manuscripts."""
from pathlib import Path
import html,json,re
import report_architecture
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
M=json.loads((ROOT/'content/manifest.json').read_text())
def tr(lang,z,e):return z if lang=='zh' else e
def link(lang,route,label,cls=''):return '<a class="'+cls+'" href="/2026/'+lang+'/'+route+'">'+E(label)+'</a>'
def architecture(lang):
 return '<div class="architecture-block">'+report_architecture.render(lang)+'<img class="architecture-print" src="/assets/report/fig-1-0-1_report_logic.svg" alt="'+tr(lang,'全书研究结构','Report research structure')+'"></div>'
def manuscript(key):return json.loads((ROOT/'content/frontmatter.json').read_text())['documents'][key]
def render_text(text,prefix):
 out=[];index=0
 for block in text.strip().split('\n\n'):
  if block.startswith('# '):continue
  if block.startswith('## '):
   index+=1;out.append('<h2 id="'+prefix+'-'+str(index)+'">'+E(block[3:])+'</h2>');continue
  s=E(block);s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s);out.append('<p>'+s+'</p>')
 return '<div class="front-publication-prose" lang="zh-CN">'+''.join(out)+'</div>'
def translation(lang):return '' if lang=='zh' else '<p class="reader-note">The Chinese text is shown below; the English translation is in preparation. Navigation and the structure diagram are available in English.</p>'
def summary(lang):
 t=lambda z,e:tr(lang,z,e)
 return '<article class="front-publication">'+translation(lang)+'<nav class="front-publication-nav" aria-label="'+t('摘要阅读导航','Summary navigation')+'">'+link(lang,'introduction/',t('阅读引言','Introduction'))+link(lang,'',t('全书目录','Contents'))+link(lang,'chapters/01/',t('价值与方法','Values and methods'))+'</nav>'+render_text(manuscript('outline/执行摘要.md'),'summary')+'<section class="front-architecture-section"><h2>'+t('一张图，看清全书结构','The report at a glance')+'</h2>'+architecture(lang)+'</section></article>'
def introduction(lang):
 t=lambda z,e:tr(lang,z,e)
 return '<article class="front-publication">'+translation(lang)+render_text(manuscript('chapters/引言-人工智能时代的开源发展.md'),'introduction')+'<section class="front-architecture-section"><h2>'+t('沿着研究路径，选择你的入口','Choose your entry into the research')+'</h2>'+architecture(lang)+'</section><div class="front-publication-nav">'+link(lang,'summary/',t('先读执行摘要 →','Read the summary →'))+link(lang,'chapters/01/',t('进入第一章 →','Start Chapter 1 →'))+'</div></article>'
def contents(lang):
 t=lambda z,e:tr(lang,z,e)
 out='<div class="front-contents"><nav class="front-publication-nav" aria-label="'+t('前置篇目','Front matter')+'">'+link(lang,'summary/',t('执行摘要','Executive summary'))+link(lang,'introduction/',t('引言','Introduction'))+'</nav><p class="front-contents-lead">'+t('六章、三十个小节：从共同目标出发，以互补的观察理解生态，再把证据连接到行动。','Six chapters and thirty sections connect shared goals, complementary observations and action.')+'</p>'+architecture(lang)+'<div class="front-contents-grid">'
 for c in M['chapters']:
  out+='<section class="front-chapter-card"><div class="section-topline">'+t('第'+c['number']+'章','CHAPTER '+c['number'])+' · '+c.get('label','FOUNDATION' if c['number']=='1' else 'ACTION')+'</div><h2>'+link(lang,c['route'],c['title'][lang])+'</h2><p>'+E(c['question'][lang])+'</p><nav aria-label="'+E(c['title'][lang])+'">'
  for sec in c['sections']:out+=link(lang,c['route']+'#'+sec['id'],sec['number']+' '+sec['title'][lang])
  out+='</nav></section>'
 out+='</div><section class="front-appendices"><h2>'+t('附录与方法','Appendices and methods')+'</h2><div class="front-publication-nav">'+''.join(link(lang,u['route'],u['title'][lang]) for u in M['back_matter'] if u['kind'] in ['methods','declaration','dpg'])+'</div></section><p class="front-edition-note">'+t('本版：第一章正式发布；第二、三、五章正文与图表已上线；第四章深入展开 4.1，其余小节先提供框架与首幅全景；第六章保留已确定的结构。','This edition: Chapter 1 is published; Chapters 2, 3 and 5 have text and charts; Chapter 4 develops 4.1 in depth and provides the other landscapes; Chapter 6 retains its agreed structure.')+'</p></div>'
 return out
