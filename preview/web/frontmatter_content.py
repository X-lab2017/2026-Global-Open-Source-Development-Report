"""Context-specific entry pages backed by the canonical front-matter manuscripts."""
from pathlib import Path
import html,json,re
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
 t=lambda z,e:tr(lang,z,e)
 out='<article class="front-publication">'+translation(lang)+render_text(manuscript('outline/执行摘要.md'),'summary')
 out+='<nav class="front-summary-next" aria-label="'+t('从摘要继续阅读','Continue from the summary')+'"><span>'+t('查看支撑这些发现的研究','Explore the research behind these findings')+'</span><div>'
 for c in M['chapters'][1:5]:out+=link(lang,c['route'],t('第'+c['number']+'章 · ','Chapter '+c['number']+' · ')+{'2':t('生态地图','Maps'),'3':t('影响力榜单','Rankings'),'4':t('技术全景','Landscapes'),'5':t('模型生态','Models')}[c['number']])
 out+='</div>'+link(lang,'chapters/06/',t('阅读第六章：行动建议 →','Read Chapter 6: recommended actions →'),'front-summary-action')+'</nav></article>'
 return out

def introduction(lang):
 t=lambda z,e:tr(lang,z,e)
 return '<article class="front-publication">'+translation(lang)+render_text(manuscript('chapters/引言-人工智能时代的开源发展.md'),'introduction')+'<nav class="front-next-reading" aria-label="'+t('开始正文阅读','Begin the report')+'"><div><small>'+t('下一步 · 建立共同理解','NEXT · ESTABLISH A SHARED FOUNDATION')+'</small><strong>'+t('第一章：从开放协作到公共价值','Chapter 1: from collaboration to public value')+'</strong><span>'+t('从两个开源故事出发，理解发展目标与观察方法。','Start with two open source stories, then explore goals and methods.')+'</span></div>'+link(lang,'chapters/01/',t('开始阅读 →','Start reading →'),'front-next-primary')+'</nav><p class="front-alternative">'+t('已有明确问题？','Have a specific question?')+' '+link(lang,'',t('从目录直接进入小节 →','Choose a section from the contents →'))+'</p></article>'

def contents(lang):
 t=lambda z,e:tr(lang,z,e)
 out='<div class="front-contents"><nav class="front-publication-nav" aria-label="'+t('前置篇目','Front matter')+'">'+link(lang,'summary/',t('执行摘要','Executive summary'))+link(lang,'introduction/',t('引言','Introduction'))+'</nav><p class="front-contents-lead">'+t('六章、三十个小节。可从第一章顺序阅读，也可按问题直接进入小节。','Six chapters and thirty sections. Read from Chapter 1 or go directly to the question that interests you.')+'</p>'
 groups=[('foundation','建立共同基础','Establish a shared foundation',M['chapters'][:1]),('research','从四个视角理解生态','Explore four research perspectives',M['chapters'][1:5]),('action','从研究走向行动','Connect research to action',M['chapters'][5:])]
 for n,(key,z,e,chapters) in enumerate(groups,1):
  out+='<section class="front-contents-group front-group-'+key+'" aria-labelledby="contents-'+key+'"><h2 id="contents-'+key+'"><small>0'+str(n)+'</small>'+t(z,e)+'</h2><div class="front-contents-grid">'
  for c in chapters:
   out+='<article class="front-chapter-card"><div class="section-topline">'+t('第'+c['number']+'章','CHAPTER '+c['number'])+' · '+c.get('label','FOUNDATION' if c['number']=='1' else 'ACTION')+'</div><h3>'+link(lang,c['route'],c['title'][lang])+'</h3><p>'+E(c['question'][lang])+'</p><nav aria-label="'+E(c['title'][lang])+'">'
   for sec in c['sections']:out+=link(lang,c['route']+'#'+sec['id'],sec['number']+' '+sec['title'][lang])
   out+='</nav></article>'
  out+='</div></section>'
 out+='<section class="front-appendices"><h2>'+t('附录与方法','Appendices and methods')+'</h2><div class="front-publication-nav">'+''.join(link(lang,u['route'],u['title'][lang]) for u in M['back_matter'] if u['kind'] in ['methods','declaration','dpg'])+'</div></section><p class="front-edition-note">'+t('本版：第一章正式发布；第二、三、五章正文与图表已上线；第四章深入展开 4.1，其余小节先提供框架与首幅全景；第六章图文与九条建议已上线，供审阅。','This edition: Chapter 1 is published; Chapters 2, 3 and 5 have text and charts; Chapter 4 develops 4.1 in depth and provides the other landscapes; Chapter 6 provides text, diagrams and nine recommendations for review.')+'</p></div>'
 return out
