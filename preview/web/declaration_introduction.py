"""Declaration-led introduction. Preserve the source text with native reading anchors."""
import html
import json
import re
from pathlib import Path
import declaration_diagram
import frontmatter_publication as publication

ROOT = Path(__file__).resolve().parents[1]
E = lambda value: html.escape(str(value), quote=True)

def inline(value):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', E(value))


def render(lang):
    t = lambda z, e: z if lang == 'zh' else e
    documents = json.loads((ROOT / 'content/frontmatter.json').read_text())['documents']
    key = 'chapters/引言-人工智能时代的开源发展.md' if lang == 'zh' else 'chapters/introduction.en.md'
    blocks = documents[key].strip().split('\n\n')
    first_heading = next(i for i, b in enumerate(blocks) if b.startswith('### '))
    preamble = [b for b in blocks[:first_heading] if not b.startswith('# ')]
    title = blocks[first_heading][4:]
    subtitle = blocks[first_heading + 1].strip('*').strip()
    out = '<article class="declaration-introduction" lang="' + ('zh-CN' if lang == 'zh' else 'en') + '"><div class="declaration-opening">' + ''.join('<p>' + inline(p) + '</p>' for p in preamble) + '</div>'
    out += declaration_diagram.render(lang)
    out += '<div class="declaration-document" id="declaration-text"><header class="declaration-title"><span>DECLARATION / ' + t('宣言收录文本', 'TEXT INCLUDED IN THIS REPORT') + '</span><h2>' + E(title) + '</h2><p>' + E(subtitle) + '</p></header>'
    if lang == 'en':
        out += '<p class="declaration-translation-note">English translation prepared for this report.</p>'
    section = 0
    principle = 0
    in_principle = False
    in_section = False
    for block in blocks[first_heading + 2:]:
        if block.startswith('### ') or block.startswith('#### '):
            if in_principle:
                out += '</div></article>'
                in_principle = False
            if block.startswith('### '):
                if in_section:
                    out += '</section>'
                section += 1
                in_section = True
                if section == 6:
                    out += '</div>'  # End the declaration before the editorial bridge.
                out += '<section class="declaration-section' + (' declaration-bridge' if section == 6 else '') + '" id="introduction-' + str(section) + '"><h2>' + E(block[4:]) + '</h2>'
            else:
                out += '<h3 class="declaration-layer-title">' + E(block[5:]) + '</h3>'
        elif block.startswith('**原则') or block.startswith('**Principle '):
            if in_principle:
                out += '</div></article>'
            principle += 1
            in_principle = True
            out += '<article class="declaration-principle" id="declaration-principle-' + str(principle) + '"><h4><span>0' + str(principle) + '</span><strong>' + E(block.strip('*')) + '</strong></h4><div>'
        elif block.startswith('**') and block.endswith('**'):
            out += '<p class="' + ('declaration-motto' if in_principle else 'declaration-final-line') + '">' + E(block[2:-2]) + '</p>'
        else:
            out += '<p>' + inline(block) + '</p>'
    if in_principle:
        out += '</div></article>'
    if in_section:
        out += '</section>'
    assert section == 6 and principle == 7, 'The declaration must retain all sections and seven principles'
    out += '<nav class="front-next-reading" aria-label="' + t('开始正文阅读', 'Begin the report') + '"><div><small>' + t('下一步 · 从愿景进入研究', 'NEXT · FROM VISION TO RESEARCH') + '</small><strong>' + t('第一章：从开放协作到公共价值', 'Chapter 1: from collaboration to public value') + '</strong><span>' + t('从开源故事出发，理解发展目标与观察方法。', 'Start with open source stories, then explore goals and methods.') + '</span></div><a class="front-next-primary" href="/2026/' + lang + '/chapters/01/">' + t('开始阅读 →', 'Start reading →') + '</a></nav><p class="declaration-source-note" id="declaration-source">' + t('宣言依据报告收录文本；', 'The declaration follows the text retained in the report; ') + '<a href="https://f16qo26uhe1.feishu.cn/wiki/BBjrwWhukifCqukvEwSct9EYnMf">' + t('指定来源', 'designated source') + '</a>。' + t('英文为本报告译文。', 'The English text is a translation prepared for this report.') + '</p></article>'
    return out+publication.download(lang)
