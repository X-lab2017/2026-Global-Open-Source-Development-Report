"""Context-specific entry pages backed by the canonical front-matter manuscripts."""
from pathlib import Path
import html,json,re
import executive_summary
import declaration_introduction
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(str(s),quote=True)
M=json.loads((ROOT/'content/manifest.json').read_text())
def tr(lang,z,e):return z if lang=='zh' else e
def link(lang,route,label,cls=''):return '<a class="'+cls+'" href="/2026/'+lang+'/'+route+'">'+E(label)+'</a>'
def manuscript(key):return json.loads((ROOT/'content/frontmatter.json').read_text())['documents'][key]
def render_text(text,prefix):
 out=[];index=0
 for block in text.strip().split('\n\n'):
  if block.startswith('# '):continue
  if block.startswith('## '):
   index+=1;out.append('<h2 id="'+prefix+'-'+str(index)+'">'+E(block[3:])+'</h2>');continue
  s=E(block);s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s);out.append('<p>'+s+'</p>')
 return '<div class="front-publication-prose" lang="zh-CN">'+''.join(out)+'</div>'
def translation(lang):return '' if lang=='zh' else '<p class="reader-note">The Chinese text is shown below; the English translation is in preparation. Navigation is available in English.</p>'
def summary(lang):
 return executive_summary.render(lang)

def introduction(lang):
 return declaration_introduction.render(lang)

def contents(lang):
 t=lambda z,e:tr(lang,z,e)
 out='<div class="front-contents"><nav class="front-contents-entry" aria-label="'+t('前置篇目','Front matter')+'">'
 for route,title,description in [('summary/',t('执行摘要','Executive summary'),t('把握主要发现与行动方向','Findings and action priorities')),('introduction/',t('引言','Introduction'),t('从宣言理解共同愿景与七项原则','The shared vision and seven principles'))]:
  out+='<a href="/2026/'+lang+'/'+route+'"><span><strong>'+title+'</strong><small>'+description+'</small></span><i aria-hidden="true">→</i></a>'
 out+='</nav>'
 groups=[('foundation','建立共同基础','Establish a shared foundation',M['chapters'][:1]),('research','从四个视角理解生态','Explore four research perspectives',M['chapters'][1:5]),('action','从研究走向行动','Connect research to action',M['chapters'][5:])]
 for n,(key,z,e,chapters) in enumerate(groups,1):
  out+='<section class="front-contents-group front-group-'+key+'" aria-labelledby="contents-'+key+'"><h2 id="contents-'+key+'"><small>0'+str(n)+'</small>'+t(z,e)+'</h2><div class="front-contents-grid">'
  for c in chapters:
   key=c.get('label','foundation' if c['number']=='1' else 'action').lower()
   chapter_label=t('第'+c['number']+'章','Chapter '+c['number'])+(' · '+c['label'] if c.get('label') else '')
   chapter_title=c['title'][lang].split('（')[0].split(' (')[0]
   out+='<article class="front-chapter-card front-chapter-'+key+'" id="contents-chapter-'+c['number']+'"><div class="section-topline">'+chapter_label+'</div><h3>'+link(lang,c['route'],chapter_title)+'</h3><p>'+E(c['question'][lang])+'</p><nav aria-label="'+E(c['title'][lang])+'">'
   for sec in c['sections']:out+=link(lang,c['route']+'#'+sec['id'],sec['number']+' '+sec['title'][lang])
   out+='</nav></article>'
  out+='</div></section>'
 out+='<section class="front-appendices" id="contents-appendices"><h2>'+t('附录与方法','Appendices and methods')+'</h2><div class="front-publication-nav">'+''.join(link(lang,u['route'],u['title'][lang]) for u in M['back_matter'] if u['kind'] in ['methods','declaration','dpg'])+'</div></section><p class="front-edition-note">'+t('本版范围：第四章深入展开 4.1，其余小节先提供全景与研究框架。各图保留数据范围与模拟标识，内容随研究持续更新。','This edition develops 4.1 in depth; the other Chapter 4 sections provide landscapes and research frameworks. Figures retain scope and simulation labels, and the report evolves with the research.')+'</p></div>'
 return out
