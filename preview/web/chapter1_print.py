"""Publication views of four existing figures; PDF reads the canonical manuscript.

Usage: python3 preview/web/chapter1_print.py --font /path/NotoSansCJKsc-Regular.otf
Requires reportlab and fontTools. No browser, network, or screenshot dependency.
"""
from pathlib import Path
import argparse, gzip, hashlib, html, json, os, re, shutil, sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'preview/web'))
from chapter_visuals import SDGS, SDG_COLORS, DPG

INTRO = 'chapters/chapter1/本章介绍.md'
SECTION = 'chapters/chapter1/1.1-开源-数字公共品与可持续发展引擎.md'
INK, MUTED, TEAL, BLUE, PURPLE, GREEN = '#18394c', '#4d6573', '#087984', '#2d5f9f', '#76508b', '#407a51'
LINE, WASH = '#a9bbc4', '#f2f6f7'
FONT = 'GOSD'
WEB = 'https://www.x-lab.info/2026-Global-Open-Source-Development-Report/2026/zh/chapters/01/'
FIG_NAMES = ['fig-1-0-1_report_logic', 'fig-1-1-1_linux_collaboration', 'fig-1-1-2_model_derivatives', 'fig-1-1-3_sdgs_dpga']
PAGE_NAMES = ['章首', '全书结构', '1.1 / 共同维护', '图 1-1-1 / Linux', '1.1 / 后续创造', '图 1-1-2 / 开放模型', '1.1 / 公共价值', '图 1-1-3 / SDGs × DPGA']


def canonical():
    intro = (ROOT / INTRO).read_text()
    body = (ROOT / SECTION).read_text()
    parts = re.split(r'(?m)^## ', body)[1:]
    return intro, [(p.splitlines()[0], '\n'.join(p.splitlines()[1:]).strip()) for p in parts]


def paragraphs(text):
    return [p.strip() for p in text.split('\n\n') if p.strip() and not p.startswith(('#', '!['))]


def plain(text):
    return text.replace('**', '')


def font_setup(path, work):
    """Convert a small OFL font subset to TrueType for reliable PDF embedding."""
    from fontTools.ttLib import TTFont as FTFont
    from fontTools import subset
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    font = FTFont(path)
    source = Path(__file__).read_text() + (ROOT / INTRO).read_text() + (ROOT / SECTION).read_text()
    source += json.dumps([SDGS, DPG], ensure_ascii=False)
    source += (ROOT / 'preview/content/story-data.json').read_text()
    source += (ROOT / 'preview/content/manifest.json').read_text()
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
        if ch == '\n' or (line and pdfmetrics.stringWidth(line + ch, FONT, size) > width):
            lines.append(line); line = ''
            if ch == '\n': continue
        line += ch
    if line: lines.append(line)
    return lines


class Figure:
    def __init__(self, title, label, subtitle, height=840):
        self.ops = []; self.width = 640; self.height = height
        self.title = title
        self.text(0, 18, label, 14, TEAL)
        self.text(0, 61, title, 28)
        self.text(0, 91, subtitle, 15, MUTED)

    def text(self, x, y, value, size=15, color=INK, align='left'):
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
        c.restoreState()


def report_figure():
    f=Figure('六章，一条清晰的阅读路径','图 1-0-1 / READING THE REPORT','共同目标组织观察，研究证据连接行动。')
    f.rect(0,120,640,130,WASH)
    f.text(22,149,'第一章 / 建立共同基础',15,TEAL)
    f.text(22,185,'从开放协作到公共价值',24)
    f.text(22,218,'1.1 共同创新与公共价值 · 1.2 OSDGs · 1.3 OSDI',16,MUTED)
    f.line([(320,250),(320,281)],TEAL,2);f.line([(315,274),(320,281),(325,274)],TEAL,2)
    f.text(0,307,'第二至第五章 / 四个互补观察视角',18)
    items=[('第二章 · GOSO','全球开源生态观测地图','参与、贡献与开放资产，在哪里积累？',TEAL),
           ('第三章 · GOSR','全球开源影响力排行榜','哪些地区、组织与项目形成关键影响？',PURPLE),
           ('第四章 · GOSL','全球开源技术全景洞察','技术如何分类，各领域怎样演进？',BLUE),
           ('第五章 · GOSM','全球开源大模型发展洞察','模型由谁供给，怎样复用与开放？',GREEN)]
    for i,(label,title,q,color) in enumerate(items):
        x=(i%2)*332;y=330+(i//2)*147
        f.rect(x,y,308,128);f.line([(x+1,y+1),(x+307,y+1)],color,3)
        f.text(x+18,y+30,label,16,color);f.text(x+18,y+65,title,18)
        f.lines(x+18,y+93,q,272,14,21,MUTED)
    f.line([(320,612),(320,644)],TEAL,2);f.line([(315,637),(320,644),(325,637)],TEAL,2)
    f.rect(0,660,640,113,WASH);f.text(22,689,'第六章 / 从研究走向行动',15,TEAL)
    f.text(22,724,'未来展望与行动建议',24);f.text(22,754,'三项共同任务 · 九条主体建议',16,MUTED)
    f.text(0,812,'阅读提示：四个研究视角相互补充；连线表示篇章联系，不代表评分权重。',14,MUTED)
    return f


def linux_figure(s):
    f=Figure('一个内核，连接持续的全球协作','图 1-1-1 / LINUX · COLLECTIVE MAINTENANCE','累计贡献结构：组织与个人两个观察尺度。')
    for x,key,label,color in [(0,'organizations','组织条目',TEAL),(332,'contributors','贡献者记录',BLUE)]:
        f.rect(x,114,308,76,WASH);f.text(x+17,146,f'{s[key]["total"]:,}',30,color);f.text(x+17,173,label+' · 累计榜单总记录数',14,MUTED)
    for start,key,title,color in [(221,'organizations','A / 组织榜单前 10 条',TEAL),(498,'contributors','B / 贡献者榜单前 10 条',BLUE)]:
        rows=s[key]['rows']; f.text(0,start,title,18,color)
        f.text(490,start,'贡献记录量',13,MUTED,'right');f.text(640,start,'本类榜单占比',13,MUTED,'right')
        for i,row in enumerate(rows):
            y=start+26+i*23;f.text(0,y,f'{i+1:02d}',12,MUTED)
            f.text(28,y,row['name'],13)
            f.rect(260,y-10,155,9,'#e3e9ed','#e3e9ed',0)
            f.rect(260,y-10,155*row['contributions']/rows[0]['contributions'],9,color,color,0)
            f.text(503,y,f'{row["contributions"]:,}',13,INK,'right');f.text(640,y,f'{row["percentage"]:.2f}%',13,INK,'right')
    f.line([(0,767),(640,767)])
    f.lines(0,792,'LFX Linux Kernel 累计快照 · 2026-10-11。组织与个人占比分别计算，条形按各自榜首缩放。累计记录不等于年度活跃数，也不表示 OpenRank。',635,14,22,MUTED)
    return f


def model_figure(s):
    f=Figure('开放的影响，延伸到下一次创造','图 1-1-2 / OPEN MODELS · REUSE & DERIVATIVES','A 观察样本构成的变化；B 理解一次具体的后续创造。')
    f.text(0,131,'A / 新增微调与衍生模型的基础模型发布方地区构成',17)
    colors=[BLUE,TEAL,PURPLE];keys=['china','unitedStates','europe'];names=['中国','美国','欧洲'];dashes=[None,[9,5],[2,5]]
    for i in range(3):
        x=i*170;f.line([(x,158),(x+31,158)],colors[i],2.2,dashes[i]);f.text(x+40,163,names[i],14)
    left,top,w,h=36,192,540,206
    for value in [0,25,50,75,100]:
        y=top+h-h*value/100;f.line([(left,y),(left+w,y)],LINE,.65);f.text(left-9,y+4,str(value)+'%',12,MUTED,'right')
    for i,(key,color,dash) in enumerate(zip(keys,colors,dashes)):
        pts=[(left+j*w/27,top+h-h*d[key]/100) for j,d in enumerate(s['models'])]
        f.line(pts,color,2.4,dash)
        for px,py in pts:f.dot(px,py,2.5,color)
        f.text(left+w+10,pts[-1][1]+4,str(s['models'][-1][key])+'%',14,color)
    for j,label in [(0,'2023.11'),(2,'2024.01'),(14,'2025.01'),(27,'2026.02')]:
        x=left+j*w/27;f.line([(x,398),(x,404)],MUTED,.8)
        # Early ticks are labelled on separate lines to prevent collision.
        f.text(x,423+(17 if j==2 else 0),label,12,MUTED,'center')
    f.lines(0,466,'ATOM 跟踪的 Hugging Face 样本，2023.11-2026.02。地区按基础模型发布方归属；不是用户国籍或全球市场份额。保留来源取整百分比。',640,13.5,21,MUTED)
    f.line([(0,506),(640,506)])
    f.text(0,539,'B / Qwen2.5-7B 与四个选定的直接下游',17)
    source='Qwen/Qwen2.5-7B'
    targets=[source+'-Instruct',source+'-Instruct-1M','Qwen/Qwen2.5-Coder-7B','Qwen/Qwen2.5-Math-7B']
    net=json.loads(gzip.decompress((ROOT/'preview/content/gosm/network.json.gz').read_bytes()))
    edges={(e['source'],e['target']) for e in net['edges']};assert all((source,t) in edges for t in targets)
    f.rect(0,644,219,75,WASH);f.text(109.5,672,'基础模型',14,TEAL,'center');f.text(109.5,701,'Qwen2.5-7B',20,INK,'center')
    for i,(name,use) in enumerate(zip(targets,['对话','长上下文','编程','数学'])):
        y=561+i*54;mid=y+23
        f.line([(219,682),(251,682),(251,mid),(283,mid)],LINE,1.3)
        f.line([(278,mid-4),(283,mid),(278,mid+4)],LINE,1.3)
        f.rect(284,y,356,46);f.text(298,y+17,use,12,TEAL);f.text(298,y+36,name.split('/')[1],15)
    f.lines(0,811,'第五章快照 · 2026-10-16。所有模型 ID 均带 Qwen/ 前缀。连线为发布者声明，非训练验证；与 A 分属不同样本，不用于解释 A 的份额。',640,13.5,21,MUTED)
    return f


def public_figure():
    f=Figure('联合国 SDGs × 数字公共品联盟 DPGA','图 1-1-3 / PUBLIC VALUE · GOALS & CONDITIONS','发展方向与实践条件并列呈现，不作逐项对应。')
    f.text(0,136,'希望改善什么？',20,TEAL);f.text(332,136,'需要具备什么？',20,TEAL)
    f.text(0,163,'17 项发展目标',14,MUTED);f.text(332,163,'9 项实践条件',14,MUTED)
    for i,(z,e) in enumerate(SDGS):
        y=181+i*32
        f.rect(0,y,307,29,'#ffffff',LINE,2);f.rect(0,y,4,29,SDG_COLORS[i],SDG_COLORS[i],0)
        f.text(15,y+20,f'{i+1:02d}',13,MUTED);f.text(48,y+20,z,13.5)
    for i,(z,e,zd,ed) in enumerate(DPG):
        y=181+i*60
        f.rect(332,y,308,56,WASH,LINE,3);f.text(344,y+19,f'{i+1:02d}',12,TEAL)
        f.text(373,y+19,z,14)
        desc='数据安全、有害内容与骚扰防护。' if i==8 else zd
        f.lines(373,y+38,desc,254,12,15,MUTED)
    f.rect(0,745,640,67,WASH)
    f.text(16,770,'开放软件 · 开放数据 · 开放 AI 系统 · 开放内容',16)
    f.text(16,795,'目标相关性、标准符合性与地方实施成效，需要分别判断。',15,MUTED)
    f.text(0,837,'DPG 条件为简述；据 DPGA Standard 改编（CC BY-SA 4.0）。本图不表示认证。',12.5,MUTED)
    return f


def draw_para(c, text, x, top, width, size=11.2, leading=19.6, color=INK):
    escaped=html.escape(text)
    escaped=re.sub(r'\*\*(.*?)\*\*',lambda m:'<font color="'+TEAL+'">'+m.group(1)+'</font>',escaped)
    style=ParagraphStyle('body',fontName=FONT,fontSize=size,leading=leading,textColor=HexColor(color),wordWrap='CJK',splitLongWords=True)
    p=Paragraph(escaped,style);pw,ph=p.wrap(width,1000)
    p.drawOn(c,x,top-ph);return top-ph


def page_frame(c, number, name):
    w,h=A4; c.setFillColor(HexColor(TEAL));c.rect(46,h-37,30,3,fill=1,stroke=0)
    c.setFont(FONT,9);c.setFillColor(HexColor(MUTED));c.drawString(87,h-38,'GOSD 2026 / 全球开源发展报告')
    c.drawRightString(w-46,h-38,'第一章 · 章首与 1.1 样章')
    c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.line(46,45,w-46,45)
    c.setFont(FONT,8.5);c.drawString(46,29,name);c.drawRightString(w-46,29,f'{number:02d} / 08')
    c.bookmarkPage('page-'+str(number));c.addOutlineEntry(name,'page-'+str(number),0,False)


def narrative_page(c, number, title, kicker, paras, second=None):
    w,h=A4; page_frame(c,number,PAGE_NAMES[number-1]);x=46;width=w-92
    c.setFillColor(HexColor(TEAL));c.setFont(FONT,10);c.drawString(x,h-91,kicker)
    titlelines=wrap(title,width,23)
    y=h-131
    for line in titlelines:c.setFillColor(HexColor(INK));c.setFont(FONT,23);c.drawString(x,y,line);y-=33
    y-=10
    for p in paras:y=draw_para(c,p,x,y,width)-12
    if second:
        heading,more=second;y-=5;c.setFillColor(HexColor(TEAL));c.setFont(FONT,14);c.drawString(x,y,heading);y-=24
        for p in more:y=draw_para(c,p,x,y,width)-12
    assert y>65, f'Page {number} content overflow: {y:.1f}'
    # A running figure reference is navigational, not part of the research prose.
    c.setFillColor(HexColor(MUTED));c.setFont(FONT,9);c.drawString(x,62,'配图见下一页 / '+['图 1-0-1','图 1-1-1','图 1-1-2','图 1-1-3'][(number-1)//2])
    c.showPage()


def build_pdf(figs, output):
    intro,parts=canonical();output.parent.mkdir(parents=True,exist_ok=True)
    os.environ['SOURCE_DATE_EPOCH']='1792368000'  # 2026-10-19, reproducible edition date
    c=canvas.Canvas(str(output),pagesize=A4,pageCompression=1,invariant=1)
    c.setTitle('GOSD 2026 第一章：章首与 1.1 · 网页与 PDF 对照样章')
    c.setAuthor('GOSD / 全球开源发展报告');c.setSubject('一份完整研究底稿，网页与 PDF 两种编排。')
    narratives=[('从开放协作到公共价值','01 / 价值、目标与观察方法',paragraphs(intro),None),
                (parts[0][0],'1.1 / 开源、共同创新与公共价值',paragraphs(parts[0][1]),None),
                (parts[1][0],'1.1 / 从共同维护到下游复用',paragraphs(parts[1][1]),None),
                ('连接发展目标与实践条件','1.1 / SDGs 与数字公共品',paragraphs(parts[2][1]),(parts[3][0],paragraphs(parts[3][1])))]
    for i,(title,kicker,paras,second) in enumerate(narratives):
        narrative_page(c,2*i+1,title,kicker,paras,second)
        page_frame(c,2*i+2,PAGE_NAMES[2*i+1]);figs[i].paint(c,46,A4[1]-75,A4[0]-92)
        if i==0:
            c.linkURL(WEB,(46,58,A4[0]-46,75),relative=0)
            c.setFillColor(HexColor(MUTED));c.setFont(FONT,8.5);c.drawString(46,65,'同一份正文与图号；网页可进一步切换、点选与探索。')
        c.showPage()
    c.save()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--font',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=ROOT/'output/pdf/GOSD-2026-chapter1-sample.pdf')
    args=parser.parse_args();work=ROOT/'tmp/pdfs/chapter1';work.mkdir(parents=True,exist_ok=True)
    font_setup(args.font,work)
    story=json.loads((ROOT/'preview/content/story-data.json').read_text())
    figs=[report_figure(),linux_figure(story),model_figure(story),public_figure()]
    svgdir=ROOT/'figures/chapter1/print';svgdir.mkdir(parents=True,exist_ok=True)
    assets=ROOT/'preview/content/report-assets/print';assets.mkdir(parents=True,exist_ok=True)
    for name,fig in zip(FIG_NAMES,figs):
        p=svgdir/(name+'.svg');p.write_text(fig.svg());shutil.copy2(p,assets/p.name)
    build_pdf(figs,args.output)
    destination=ROOT/'preview/content/report-assets/chapter1/GOSD-2026-chapter1-sample.pdf'
    shutil.copy2(args.output,destination)
    manifest={'scope':'章首＋1.1','edition':'2026-10-19','pages':8,'paper':'A4 portrait',
              'manuscript_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [INTRO,SECTION]},
              'figure_ids':['1-0-1','1-1-1','1-1-2','1-1-3'],
              'pdf_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
              'source_files':story['files'],
              'qwen_sha256':hashlib.sha256((ROOT/'preview/content/gosm/network.json.gz').read_bytes()).hexdigest()}
    (ROOT/'preview/content/report-assets/chapter1/sample-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pdf':str(args.output),'bytes':args.output.stat().st_size,'pages':8,'publication_figures':4},ensure_ascii=False))


if __name__=='__main__': main()
