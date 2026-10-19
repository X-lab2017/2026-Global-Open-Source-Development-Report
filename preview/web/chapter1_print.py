"""Complete Chapter 1: shared manuscript and seven publication views.

Usage: python3 preview/web/chapter1_print.py --font /path/NotoSansCJKsc-Regular.otf
Requires reportlab and fontTools. No browser, network, or screenshot dependency.
"""
from pathlib import Path
import argparse, gzip, hashlib, html, json, math, os, re, shutil, sys
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, BaseDocTemplate, PageTemplate, Frame, Flowable, PageBreak
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'preview/web'))
from chapter_visuals import SDGS, SDG_COLORS, DPG, DIM_NOTES, sdg_text_color
from chapter1_publication import FIGURES,PDF_NAME,MANIFEST_NAME,EDITION
from chapter1_theme_map import PILLARS,MAPS

INTRO = 'chapters/chapter1/本章介绍.md'
SECTION = 'chapters/chapter1/1.1-开源-数字公共品与可持续发展引擎.md'
SECTIONS=[SECTION,'chapters/chapter1/1.2-OSDGs-开源发展目标框架.md','chapters/chapter1/1.3-OSDI-开源发展度量体系.md']
SOURCES=[INTRO,*SECTIONS]
INK, MUTED, TEAL, BLUE, PURPLE, GREEN = '#18394c', '#4d6573', '#087984', '#2d5f9f', '#76508b', '#407a51'
LINE, WASH = '#a9bbc4', '#f2f6f7'
FONT = 'GOSD'
WEB = 'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/01/'
FIG_NAMES = [v[3] for v in FIGURES.values()]
BODY_SIZE = 11.2
PRINT_WIDTH = A4[0] - 92


def plain(text):
    return text.replace('**', '')


def font_setup(path, work, extra_text=""):
    """Convert a small OFL font subset to TrueType for reliable PDF embedding."""
    from fontTools.ttLib import TTFont as FTFont
    from fontTools import subset
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    font = FTFont(path)
    source = extra_text + Path(__file__).read_text() + ''.join((ROOT/p).read_text() for p in SOURCES)
    source += json.dumps([SDGS, DPG], ensure_ascii=False)
    source += (ROOT / 'preview/content/story-data.json').read_text()
    source += (ROOT / 'preview/content/manifest.json').read_text()
    source += (ROOT / 'preview/content/report.json').read_text()
    source += (ROOT / 'preview/web/chapter1_publication.py').read_text()
    source += json.dumps([DIM_NOTES,PILLARS,MAPS],ensure_ascii=False)
    opts = subset.Options(); opts.layout_features = []
    sub = subset.Subsetter(options=opts); sub.populate(text=source + ''.join(chr(i) for i in range(32, 127))); sub.subset(font)
    output = work / 'gosd-print-subset.ttf'
    if 'glyf' in font:
        font.save(output)
    else:
        gs = font.getGlyphSet(); order = font.getGlyphOrder(); upm = font['head'].unitsPerEm
        glyphs = {}
        for name in order:
            pen = TTGlyphPen(gs); gs[name].draw(Cu2QuPen(pen, max_err=1, reverse_direction=True)); glyphs[name] = pen.glyph()
        fb = FontBuilder(upm, isTTF=True); fb.setupGlyphOrder(order); fb.setupCharacterMap(font.getBestCmap())
        fb.setupGlyf(glyphs); fb.setupHorizontalMetrics(dict(font['hmtx'].metrics))
        fb.setupHorizontalHeader(ascent=font['hhea'].ascent, descent=font['hhea'].descent)
        fb.setupNameTable({'familyName': 'GOSD Noto Sans SC', 'styleName': 'Regular', 'uniqueFontIdentifier': 'GOSDPrintSubset', 'fullName': 'GOSD Noto Sans SC', 'psName': 'GOSD-NotoSansSC'})
        fb.setupOS2(sTypoAscender=font['OS/2'].sTypoAscender, sTypoDescender=font['OS/2'].sTypoDescender,
                    usWinAscent=font['OS/2'].usWinAscent, usWinDescent=font['OS/2'].usWinDescent)
        fb.setupPost(); fb.setupMaxp(); fb.save(output)
    pdfmetrics.registerFont(TTFont(FONT, output))
    pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=FONT, italic=FONT, boldItalic=FONT)


def wrap(text, width, size):
    lines = []; line = ''
    for ch in text:
        if ch == '\n' or (line and ch not in '，。；：、！？）》”' and pdfmetrics.stringWidth(line + ch, FONT, size) > width):
            lines.append(line); line = ''
            if ch == '\n': continue
        line += ch
    if line: lines.append(line)
    return lines


class Figure:
    def __init__(self, title, label, subtitle='', height=600):
        self.ops = []; self.width = 640; self.height = height
        self.title = title;self.label=label;self.finalized=False

    def finish(self):
        """Remove the former header band; keep the centered caption beneath all content."""
        assert not self.finalized
        shifted=[]
        for kind,a in self.ops:
            a=list(a)
            if kind in ['text','rect','dot']:a[1]-=26
            elif kind in ['line','polygon']:a[0]=[(x,y-26) for x,y in a[0]]
            shifted.append((kind,tuple(a)))
        self.ops=shifted;self.caption_y=self.height-3
        self.text(320,self.caption_y,self.label+'  '+self.title,13,INK,'center')
        self.height+=2;self.finalized=True
        return self

    def text(self, x, y, value, size=15, color=INK, align='left'):
        if len(color)==4:color='#'+''.join(ch*2 for ch in color[1:])
        self.ops.append(('text', (x, y, str(value), size, color, align)))

    def lines(self, x, y, value, width, size=15, leading=23, color=INK):
        rows = wrap(value, width, size)
        for i, row in enumerate(rows): self.text(x, y+i*leading, row, size, color)
        return y + len(rows)*leading

    def rect(self, x, y, w, h, fill='#ffffff', stroke=LINE, radius=5):
        self.ops.append(('rect', (x,y,w,h,fill,stroke,radius)))

    def line(self, pts, color=LINE, width=1, dash=None):
        self.ops.append(('line', (pts,color,width,dash)))

    def dot(self, x, y, r=3, color=TEAL):
        self.ops.append(('dot', (x,y,r,color)))

    def polygon(self, points, color):
        self.ops.append(('polygon', (points,color)))

    def svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{self.height}" viewBox="0 0 640 {self.height}" role="img"><title>{html.escape(self.title)}</title><rect width="640" height="{self.height}" fill="white"/><g font-family="Noto Sans CJK SC,Noto Sans SC,sans-serif">']
        for kind, a in self.ops:
            if kind == 'text':
                x,y,s,size,color,align=a
                o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="'+{'left':'start','center':'middle','right':'end'}[align]+'">'+html.escape(s)+'</text>')
            elif kind == 'rect':
                x,y,w,h,fill,stroke,rad=a;o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{fill}" stroke="{stroke}"/>')
            elif kind == 'line':
                pts,color,width,dash=a; d='M'+' L'.join(f'{x} {y}' for x,y in pts)
                extra=' stroke-dasharray="'+','.join(map(str,dash))+'"' if dash else ''
                o.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>')
            elif kind == 'dot':
                x,y,r,color=a;o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
            elif kind == 'polygon':
                points,color=a;o.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="{color}"/>')
        return ''.join(o)+'</g></svg>'

    def paint(self, c, x, top, width):
        scale = width / self.width
        c.saveState(); c.translate(x, top); c.scale(scale, scale)
        for kind, a in self.ops:
            if kind == 'text':
                px,py,s,size,color,align=a;c.setFillColor(HexColor(color));c.setFont(FONT,size)
                {'left':c.drawString,'center':c.drawCentredString,'right':c.drawRightString}[align](px,-py,s)
            elif kind == 'rect':
                px,py,w,h,fill,stroke,rad=a;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.8)
                c.roundRect(px,-py-h,w,h,rad,stroke=1,fill=1)
            elif kind == 'line':
                pts,color,lw,dash=a;c.setStrokeColor(HexColor(color));c.setLineWidth(lw);c.setDash(dash or [])
                p=c.beginPath();p.moveTo(pts[0][0],-pts[0][1])
                for px,py in pts[1:]:p.lineTo(px,-py)
                c.drawPath(p);c.setDash([])
            elif kind == 'dot':
                px,py,r,color=a;c.setFillColor(HexColor(color));c.circle(px,-py,r,stroke=0,fill=1)
            elif kind == 'polygon':
                points,color=a;c.setFillColor(HexColor(color));p=c.beginPath();p.moveTo(points[0][0],-points[0][1])
                for px,py in points[1:]:p.lineTo(px,-py)
                p.close();c.drawPath(p,stroke=0,fill=1)
        c.restoreState()


def report_figure():
    f=Figure('全书结构与研究路径','图 1-0-1',height=316)
    f.rect(0,33,640,47,WASH)
    f.text(16,53,'第一章  从开放协作到公共价值',14,TEAL)
    f.text(16,72,'1.1 共同创新与公共价值  ·  1.2 OSDGs 发展目标  ·  1.3 OSDI 指标与方法',12)
    f.line([(320,80),(320,99)],TEAL,1.5);f.line([(316,94),(320,99),(324,94)],TEAL,1.5)
    items=[('第二章 · GOSO','全球开源生态观测地图','规模、分布与联系',TEAL),
           ('第三章 · GOSR','全球开源影响力排行榜','贡献主体与生态影响',PURPLE),
           ('第四章 · GOSL','全球开源技术全景洞察','技术分类与演进',BLUE),
           ('第五章 · GOSM','全球开源大模型发展洞察','模型供给、复用与开放',GREEN)]
    for i,(label,title,q,color) in enumerate(items):
        x=(i%2)*332;y=107+(i//2)*74
        f.rect(x,y,308,63);f.line([(x+1,y+1),(x+307,y+1)],color,2)
        f.text(x+14,y+18,label,12.5,color);f.text(x+14,y+38,title,14)
        f.text(x+14,y+55,q,12,MUTED)
    f.line([(320,245),(320,264)],TEAL,1.5);f.line([(316,259),(320,264),(324,259)],TEAL,1.5)
    f.rect(0,272,640,43,WASH);f.text(16,290,'第六章  未来展望与行动建议',14,TEAL)
    f.text(16,308,'三项共同任务 · 九条主体建议',12)
    return f


def linux_figure(s):
    f=Figure('Linux 组织与贡献者累计排行','图 1-1-1',height=568)
    for x,key,label,color in [(0,'organizations','组织条目',TEAL),(332,'contributors','贡献者记录',BLUE)]:
        f.rect(x,35,308,44,WASH);f.text(x+15,54,f'{s[key]["total"]:,}  '+label,14,color)
        f.text(x+15,72,'累计榜单总记录数',11.8,MUTED)
    for start,key,title,color in [(105,'organizations','A  组织榜单前 10 条',TEAL),(322,'contributors','B  贡献者榜单前 10 条',BLUE)]:
        rows=s[key]['rows'];f.text(0,start,title,14,color)
        f.text(503,start,'贡献记录量',12,MUTED,'right');f.text(640,start,'本类榜单占比',12,MUTED,'right')
        for i,row in enumerate(rows):
            y=start+24+i*18;f.text(0,y,f'{i+1:02d}',11.5,MUTED);f.text(28,y,row['name'],12.4)
            f.rect(260,y-9,155,8,'#e3e9ed','#e3e9ed',0)
            f.rect(260,y-9,155*row['contributions']/rows[0]['contributions'],8,color,color,0)
            f.text(503,y,f'{row["contributions"]:,}',12.4,INK,'right');f.text(640,y,f'{row["percentage"]:.2f}%',12.4,INK,'right')
    f.line([(0,527),(640,527)])
    f.lines(0,547,'LFX Linux Kernel 累计快照 · 2026-10-11。组织与个人占比分别计算；条形按各自榜首缩放。',640,11.8,17,MUTED)
    return f


def model_figure(s):
    f=Figure('开放模型的宏观趋势与 Qwen 衍生实例','图 1-1-2',height=618)
    f.text(0,51,'A  新增微调与衍生模型的基础模型发布方地区构成',14)
    colors=[BLUE,TEAL,PURPLE];keys=['china','unitedStates','europe'];names=['中国','美国','欧洲'];dashes=[None,[9,5],[2,5]]
    for i in range(3):
        x=i*170;f.line([(x,75),(x+31,75)],colors[i],2,dashes[i]);f.text(x+40,80,names[i],12.5)
    left,top,w,h=36,105,540,160
    for value in [0,25,50,75,100]:
        y=top+h-h*value/100;f.line([(left,y),(left+w,y)],LINE,.65);f.text(left-9,y+4,str(value)+'%',11.5,MUTED,'right')
    for key,color,dash in zip(keys,colors,dashes):
        pts=[(left+j*w/27,top+h-h*d[key]/100) for j,d in enumerate(s['models'])]
        f.line(pts,color,2.2,dash)
        for px,py in pts:f.dot(px,py,2.3,color)
        f.text(left+w+10,pts[-1][1]+4,str(s['models'][-1][key])+'%',12.5,color)
    for j,label in [(0,'2023.11'),(2,'2024.01'),(14,'2025.01'),(27,'2026.02')]:
        x=left+j*w/27;f.line([(x,265),(x,270)],MUTED,.8);f.text(x,286+(17 if j==2 else 0),label,11.5,MUTED,'center')
    f.lines(0,327,'ATOM 跟踪的 Hugging Face 样本，2023.11-2026.02。地区按基础模型发布方归属；保留来源取整百分比。',640,11.8,18,MUTED)
    f.line([(0,362),(640,362)]);f.text(0,387,'B  Qwen2.5-7B 与四个选定的直接下游',14)
    source='Qwen/Qwen2.5-7B';targets=[source+'-Instruct',source+'-Instruct-1M','Qwen/Qwen2.5-Coder-7B','Qwen/Qwen2.5-Math-7B']
    net=json.loads(gzip.decompress((ROOT/'preview/content/gosm/network.json.gz').read_bytes()))
    edges={(e['source'],e['target']) for e in net['edges']};assert all((source,t) in edges for t in targets)
    f.rect(0,470,219,54,WASH);f.text(109.5,491,'基础模型',12,TEAL,'center');f.text(109.5,513,'Qwen2.5-7B',14,INK,'center')
    for i,(name,use) in enumerate(zip(targets,['对话','长上下文','编程','数学'])):
        y=411+i*43;mid=y+18
        f.line([(219,497),(251,497),(251,mid),(283,mid)],LINE,1.3);f.line([(278,mid-4),(283,mid),(278,mid+4)],LINE,1.3)
        f.rect(284,y,356,36);f.text(298,y+14,use,11.5,TEAL);f.text(298,y+29,name.split('/')[1],13)
    f.text(0,593,'关系快照：2026-10-16。连线为发布者声明，展示四个选定下游。',11.8,MUTED)
    return f


def public_figure():
    f=Figure('联合国 SDGs × 数字公共品联盟 DPGA','图 1-1-3',height=579)
    f.text(153,52,'SDGs · 17 项发展目标',14,TEAL,'center');f.text(486,52,'DPGA · 9 项实践条件',14,TEAL,'center')
    cx,cy,outer,inner=153,190,112,76
    for i,color in enumerate(SDG_COLORS):
        start=-90+i*360/17+1;end=-90+(i+1)*360/17-1
        angle=lambda t:math.radians(start+(end-start)*t/24)
        points=[(cx+outer*math.cos(angle(t)),cy+outer*math.sin(angle(t))) for t in range(25)]
        points += [(cx+inner*math.cos(angle(t)),cy+inner*math.sin(angle(t))) for t in range(24,-1,-1)]
        f.polygon(points,color);mid=math.radians((start+end)/2)
        f.text(cx+94*math.cos(mid),cy+94*math.sin(mid)+4,str(i+1),12,sdg_text_color(color),'center')
    f.text(cx,184,'UN SDGs',14,INK,'center');f.text(cx,207,'可持续发展目标',12,MUTED,'center')
    # Numbered key preserves every goal name without hover or selection.
    for i,(z,e) in enumerate(SDGS):
        col=0 if i<9 else 1;row=i if i<9 else i-9;x=col*158;y=335+row*26
        f.rect(x,y-9,4,13,SDG_COLORS[i],SDG_COLORS[i],0);f.text(x+11,y,f'{i+1:02d}',10.8,MUTED)
        f.lines(x+33,y,z,122,11.2,13.5)
    for i,(z,e,zd,ed) in enumerate(DPG):
        x=332+(i%3)*105;y=78+(i//3)*154;w=98;h=144
        f.rect(x,y,w,h,WASH,LINE,4);f.text(x+w/2,y+23,f'{i+1:02d}',12,TEAL,'center')
        title=wrap(z,w-14,12.5)
        for j,line in enumerate(title):f.text(x+w/2,y+47+j*18,line,12.5,INK,'center')
        desc='数据安全、有害内容与骚扰防护。' if i==8 else zd
        for j,line in enumerate(wrap(desc,w-18,11.5)):f.text(x+w/2,y+86+j*16,line,11.5,MUTED,'center')
    f.text(0,575,'DPG 条件据 DPGA Standard 简述，CC BY-SA 4.0。',11.2,MUTED)
    return f


def goals_figure(rows):
    f=Figure(FIGURES['fig-osdg-goals'][1],'图 1-2-1',height=575)
    colors=[TEAL,BLUE,PURPLE,GREEN]
    questions=['谁能参与，怎样持续成长？','有哪些可用、可复用的成果？','贡献与成果怎样形成影响？','协作如何持续，价值如何实现？']
    for i,color in enumerate(colors):
        group=[r for r in rows if r['pillar_id']=='X'+str(i+1)]
        x=(i%2)*332;y=33+(i//2)*265;f.rect(x,y,308,248,WASH)
        f.line([(x+1,y+1),(x+307,y+1)],color,2)
        f.text(x+14,y+25,'X'+str(i+1)+'  '+group[0]['pillar_name_zh'],14,color)
        f.text(x+14,y+49,questions[i],12,MUTED)
        for j,dim in enumerate(dict.fromkeys(r['dimension_id'] for r in group)):
            item=next(r for r in group if r['dimension_id']==dim);dy=y+83+j*57
            f.text(x+14,dy,dim+'  '+item['dimension_name_zh'],13)
            f.lines(x+14,dy+20,DIM_NOTES[dim][0],280,11.8,17,MUTED)
    return f


def indicators_figure(rows):
    f=Figure(FIGURES['fig-osdi-map'][1],'图 1-3-1',height=658)
    f.text(0,42,'北极星：核心结果     驱动：活动与投入     诊断：差异与约束',12,MUTED)
    colors=[TEAL,BLUE,PURPLE,GREEN];y=63
    for i,color in enumerate(colors):
        group=[r for r in rows if r['pillar_id']=='X'+str(i+1)]
        dims=list(dict.fromkeys(r['dimension_id'] for r in group));cols=[[r for r in group if r['dimension_id']==d] for d in dims]
        h=65+max(map(len,cols))*21
        f.rect(0,y,640,h,WASH);f.line([(1,y+1),(639,y+1)],color,2)
        f.text(14,y+23,'X'+str(i+1)+'  '+group[0]['pillar_name_zh'],14,color)
        w=640/len(dims)
        for j,items in enumerate(cols):
            x=j*w+14
            if j:f.line([(j*w,y+40),(j*w,y+h-13)],LINE,.7)
            f.text(x,y+48,dims[j]+'  '+items[0]['dimension_name_zh'],12.5,INK)
            for k,r in enumerate(items):
                yy=y+72+k*21
                f.text(x,yy,r['indicator_name_zh'],11.8,INK)
                f.text((j+1)*w-13,yy,r['role'],11.5,color,'right')
        y+=h+12
    f.height=y+15
    return f


def themes_figure():
    f=Figure(FIGURES['fig-theme-maps'][1],'图 1-3-2',height=506)
    colors=[TEAL,BLUE,PURPLE,GREEN]
    f.text(0,42,'发展目标 · OSDGs',12,MUTED);f.text(274,42,'第二章 · GOSO',12,MUTED)
    for j,m in enumerate(MAPS):
        for code in m[3]:
            i=int(code[1])-1;y1=112+i*102;y2=86+j*57
            pts=[]
            for n in range(31):
                t=n/30;u=1-t
                pts.append((u**3*210+3*u*u*t*238+3*u*t*t*246+t**3*274,u**3*y1+3*u*u*t*y1+3*u*t*t*y2+t**3*y2))
            f.line(pts,colors[i],1.1)
    for i,p in enumerate(PILLARS):
        y=76+i*102;f.rect(0,y,210,72,WASH,colors[i])
        f.text(12,y+22,p[0],12,colors[i]);f.text(40,y+22,p[1],13)
        f.lines(12,y+46,p[3],187,11.5,16,MUTED)
    for j,m in enumerate(MAPS):
        y=61+j*57;f.rect(274,y,366,50)
        f.text(287,y+21,'2.'+str(j+1)+'  '+m[0]+'-Map  '+m[1],13,TEAL)
        f.text(287,y+40,m[4],11.5,MUTED)
    f.text(0,481,'连线表示阅读与研究联系，不代表计算权重。',11.8,MUTED)
    return f


class ManuscriptParagraph(Paragraph):
    def split(self, availWidth, availHeight):
        # Move short paragraphs intact instead of stranding two lines.
        return []


def paragraph(text, style):
    escaped=html.escape(text)
    escaped=re.sub(r'\*\*(.*?)\*\*',lambda m:'<font color="'+TEAL+'">'+m.group(1)+'</font>',escaped)
    cls=ManuscriptParagraph if style.name in ['body','opening'] else Paragraph
    return cls(escaped,style)


class PrintFigure(Flowable):
    def __init__(self, figure, fid):
        super().__init__();self.figure=figure;self.fid=fid
        self.width=PRINT_WIDTH;self.height=figure.height*PRINT_WIDTH/640
        self.spaceBefore=8;self.spaceAfter=14
    def draw(self):
        self.figure.paint(self.canv,0,self.height,self.width)


class ChapterDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(str(filename),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=64,bottomMargin=57,
                         title='GOSD 2026 第一章：从开放协作到公共价值',author='GOSD / 全球开源发展报告',
                         subject='网页与 PDF 共用完整研究底稿',pageCompression=1,invariant=1)
        self.section='第一章 从开放协作到公共价值';self.locations=[];self.fig_pages={};self.bookmarks=[]
        self.addPageTemplates(PageTemplate('report',[Frame(46,57,PRINT_WIDTH,A4[1]-121,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.page_frame,onPageEnd=self.page_footer))
    def page_frame(self,c,doc):
        c.saveState();w,h=A4;c.setFillColor(HexColor(TEAL));c.rect(46,h-36,27,2.5,fill=1,stroke=0)
        c.setFont(FONT,8.5);c.setFillColor(HexColor(MUTED));c.drawString(83,h-37,'GOSD 2026 / 全球开源发展报告')
        c.drawRightString(w-46,h-37,'第一章  从开放协作到公共价值')
        c.restoreState()
    def page_footer(self,c,doc):
        c.saveState();w,h=A4
        c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,43,w-46,43)
        c.setFillColor(HexColor(MUTED));c.setFont(FONT,8.2);c.drawString(46,28,self.section);c.drawRightString(w-46,28,str(doc.page));c.restoreState()
    def afterFlowable(self,flowable):
        if isinstance(flowable,PrintFigure):self.fig_pages[flowable.fid]=self.page
        if isinstance(flowable,Paragraph):
            text=flowable.getPlainText()
            self.locations.append({'page':self.page,'text':text,'style':flowable.style.name})
            if flowable.style.name in ['chapter','section','subsection']:
                level={'chapter':0,'section':1,'subsection':2}[flowable.style.name]
                key='heading-'+str(len(self.bookmarks));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(text,key,level,False)
                self.bookmarks.append({'level':level,'text':text,'page':self.page})
                if level>0:self.section=text


def build_pdf(figs, output):
    output.parent.mkdir(parents=True,exist_ok=True);os.environ['SOURCE_DATE_EPOCH']='1792368000'
    body=ParagraphStyle('body',fontName=FONT,fontSize=BODY_SIZE,leading=18.6,textColor=HexColor(INK),wordWrap='CJK',spaceAfter=8,allowWidows=0,allowOrphans=0)
    opening=ParagraphStyle('opening',parent=body,leading=18,spaceAfter=6)
    styles={
        1:ParagraphStyle('chapter',parent=body,fontSize=20,leading=29,spaceAfter=16,keepWithNext=True),
        2:ParagraphStyle('section',parent=body,fontSize=16,leading=24,spaceBefore=18,spaceAfter=12,keepWithNext=True),
        3:ParagraphStyle('subsection',parent=body,fontSize=12.6,leading=21,spaceBefore=14,spaceAfter=10,keepWithNext=True,textColor=HexColor(TEAL))}
    lookup={name:PrintFigure(fig,name.split('_')[0][4:]) for name,fig in zip(FIG_NAMES,figs)}
    story=[]
    for src in SOURCES:
        if src in SECTIONS:story.append(PageBreak())
        for block in (ROOT/src).read_text().split('\n\n'):
            block=block.strip()
            if not block:continue
            if block.startswith('# '):
                level=1 if src==INTRO else 2;story.append(paragraph(block[2:],styles[level]))
            elif block.startswith('## '):story.append(paragraph(block[3:],styles[3]))
            elif block.startswith('!['):
                name=re.search(r'/([^/]+)\.svg\)',block)[1];story.append(lookup[name])
            else:story.append(paragraph(block,opening if src==INTRO else body))
    doc=ChapterDoc(output);doc.build(story)
    return {'pages':doc.page,'figure_pages':doc.fig_pages,'headings':doc.bookmarks,'paragraph_pages':doc.locations}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'output/pdf'/PDF_NAME)
    args=parser.parse_args();work=ROOT/'tmp/pdfs/chapter1';work.mkdir(parents=True,exist_ok=True)
    font_setup(args.font,work)
    story=json.loads((ROOT/'preview/content/story-data.json').read_text())
    rows=json.loads((ROOT/'preview/content/report.json').read_text())['indicators']
    figs=[f.finish() for f in [report_figure(),linux_figure(story),model_figure(story),public_figure(),goals_figure(rows),indicators_figure(rows),themes_figure()]]
    svgdir=ROOT/'figures/chapter1/print';svgdir.mkdir(parents=True,exist_ok=True)
    assets=ROOT/'preview/content/report-assets/print';assets.mkdir(parents=True,exist_ok=True)
    for name,fig in zip(FIG_NAMES,figs):
        p=svgdir/(name+'.svg');p.write_text(fig.svg());shutil.copy2(p,assets/p.name)
    layout=build_pdf(figs,args.output)
    destination=ROOT/'preview/content/report-assets/chapter1'/PDF_NAME
    shutil.copy2(args.output,destination)
    # Keep existing shared download links working; all visible entry points use the complete chapter name.
    shutil.copy2(args.output,destination.with_name('GOSD-2026-chapter1-sample.pdf'))
    manifest={'scope':'第一章完整正文：章首、1.1、1.2、1.3','edition':EDITION,'pages':layout['pages'],'paper':'A4 portrait','pdf_file':PDF_NAME,
              'figure_pages':layout['figure_pages'],'headings':layout['headings'],'body_font_pt':BODY_SIZE,
              'manuscript_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
              'figure_ids':[v[0][2:] for v in FIGURES.values()],
              'indicator_dictionary_sha256':hashlib.sha256((ROOT/'data/meta/osdi_indicator_dictionary.csv').read_bytes()).hexdigest(),
              'pdf_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
              'source_files':story['files'],
              'qwen_sha256':hashlib.sha256((ROOT/'preview/content/gosm/network.json.gz').read_bytes()).hexdigest()}
    (ROOT/'preview/content/report-assets/chapter1'/MANIFEST_NAME).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (work/'layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2))
    print(json.dumps({'pdf':str(args.output),'bytes':args.output.stat().st_size,'pages':layout['pages'],'publication_figures':7},ensure_ascii=False))


if __name__=='__main__': main()
