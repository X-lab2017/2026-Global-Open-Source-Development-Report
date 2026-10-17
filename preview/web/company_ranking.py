"""Ranking-first company prototype; original evidence stays byte-identical."""
import html
import json
import base64
from pathlib import Path

E=lambda s:html.escape(str(s),quote=True)

def figure(n,title,sub,tabs,body=''):
    return f'''<figure class="cr-figure" id="fig-3-2-{n}"><div class="cr-stage goso-unified-canvas" data-slide-key="company-{n}" data-slide-height="820" data-lang="zh" data-cr-group="{n}" role="group" aria-label="{title}"><div class="cr-board">
<header class="cr-head"><div><span class="cr-eyebrow">图 3-2-{n} / {'C-RANKING' if n==1 else 'SUPPLEMENT '+str(n-1)}</span><h4>{title}</h4></div><div class="cr-head-right"><span>{sub}</span><button data-cr-action="source">口径与来源 ↗</button></div></header>
<div class="cr-toolbar"></div><nav class="cr-tabs" aria-label="{title}视图">{''.join(f'<button data-cr-view="{key}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(key,label) in enumerate(tabs))}</nav>
<div class="cr-body">{body}</div><footer class="cr-foot"><span class="cr-status" role="status"></span><button data-cr-action="image">导出 SVG ↓</button><button data-cr-action="export">下载当前数据 ↓</button></footer>
<div class="cr-overlay" hidden role="region" aria-label="详细信息"></div></div></div><figcaption>{['以 OpenRank 排名为主序，仓库与关联开发者作为补充。点击企业查看档案，勾选后可进行对照。','位次用于观察所选企业的历史位置；历史表不是每年完整的企业榜单。','补充观察 · 用共同项目连接企业，以已合并 PR 展示贡献构成。全部为虚构演示；共同贡献体现协作联系，不直接等于正式合作。'][n-1]}</figcaption></figure>'''

def section(DATA,REPO):
    # The server-rendered table is retained as a complete no-script / print fallback.
    rows=DATA['company']['rows']
    fallback='<table class="cr-fallback"><caption>全球企业 OpenRank Top 30 · 2025.07—2026.06</caption><thead><tr><th>名次</th><th>企业</th><th>OpenRank</th><th>活跃仓库</th><th>关联活跃开发者</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(r[k])+'</td>' for k in ['rank','company_zh','openrank','active_repos','active_developers'])+'</tr>' for r in rows)+'</tbody></table>'
    out=['''<section class="chapter-section gosr-section cr-section" id="ch03-s02"><div class="section-topline"><span>3.2 / C-RANKING</span><span>企业榜单 · 交互评审版 1.2</span></div><h2>全球开源企业影响力排行榜</h2><p class="cr-lead">看见企业在全球开源协作网络中的位置。</p><p class="cr-intro">以 OpenRank 排列本期企业影响力，结合仓库与开发者规模，进一步观察长期变化和项目共建。</p><nav class="cr-section-nav" aria-label="企业排行榜阅读路径"><a href="#fig-3-2-1" aria-current="location">本期排行榜 ↓</a><a href="#fig-3-2-2">位次变化</a><a href="#fig-3-2-3">企业共同贡献</a></nav>''']
    out.append(figure(1,'全球开源企业影响力 Top 30','2025.07—2026.06 · OpenRank',[('ranking','本期排行榜'),('structure','参与结构'),('scatter','规模与影响'),('compare','企业对照')],fallback))
    out.append('''<div class="cr-reading"><span>榜单观察 01</span><h3>头部位置与参与结构，提供不同的观察线索。</h3><p>微软与华为位居全球企业榜前二，OpenRank 分别为 167,060.26 和 141,253.65。微软关联的活跃开发者更多，华为关联的活跃仓库更多。三个指标从不同角度描述企业参与，可结合具体项目继续理解。</p></div>
<section class="cr-supplement" id="cr-history"><div class="cr-supplement-heading"><span>补充观察 01 / 排名轨迹</span><h3>从本期榜单，回看长期位置与近期变化。</h3><p>年度榜提供整个统计期的比较；月度位次帮助定位变化发生的时间。选择榜单中的企业，继续查看可用历史。</p></div>''')
    out.append(figure(2,'企业影响力位次变化','所选企业的历史回溯',[('annual','年度位次'),('monthly','月度位次'),('change','期间变化'),('evidence','变化证据')]))
    out.append('''<div class="cr-reading"><span>榜单观察 02</span><h3>年度格局之下，月度位次已出现变化。</h3><p>底表显示，华为在 2026 年 3—6 月的全球月度榜中位于微软之前；字节跳动在 2026 年 4—6 月的中国月度榜中位于阿里巴巴之前。本期年度榜仍分别由微软、阿里巴巴领先。不同统计窗口应结合阅读。</p></div></section>
<section class="cr-supplement" id="cr-community"><div class="cr-supplement-heading"><span>补充观察 02 / 虚构案例</span><h3>哪些企业，正在同一项目中共同贡献？</h3><p>以项目为连接，观察企业间的共同贡献。点击企业或连线，查看共同项目、各方贡献及其占比；再通过矩阵与明细核对联系。以下企业与项目全部为虚构演示。</p></div>''')
    out.append(figure(3,'企业共同贡献与协作网络','模拟演示 · 非实测、非预测',[('network','企业协作网'),('projects','项目贡献构成'),('shared','共同项目矩阵'),('evidence','贡献明细')]))
    out.append('''</section><details class="cr-method-inline"><summary>来源、统计窗口与解释边界</summary><p>本期使用两张 Top 30 企业榜和四张历史位次表，报告期为 2025.07—2026.06。历史表各覆盖本期所选十家企业，不能据此推算整个行业历年的进入、退出或集中度。早期年度起止范围仍待核验。</p><p>位次变化不等于影响力增长率；月度名次不能平均为年度排名。OpenRank 不直接表示治理质量、商业价值或模型能力。企业项目关系和角色需单独核验，虚构案例不纳入真实榜单。</p>''')
    for key in ['company','chinaCompany','globalYear','globalMonth','chinaYear','chinaMonth']:
        d=DATA[key];out.append(f'<p><a href="/assets/gosr/data/{d["file"]}" download>{E(d["title"])} · 原始 CSV ↓</a> · <a href="{REPO}data/processed/chapter3/{d["file"]}" target="_blank" rel="noopener">来源底表 ↗</a></p>')
    out.append('</details><nav class="cr-end-nav"><a href="#fig-3-2-1">↑ 返回企业排行榜</a><a href="#ch03-s03">继续阅读 · 基金会排行榜 →</a></nav></section>')
    logo_dir=Path(__file__).resolve().parents[1]/'content/gosr/company-logos'
    manifest=json.loads((logo_dir/'manifest.json').read_text())
    logos={key:{'file':item['filename'],'data':'data:image/png;base64,'+base64.b64encode((logo_dir/'assets'/item['filename']).read_bytes()).decode()} for key,item in manifest.items()}
    out.append('<script id="company-logos" type="application/json">'+json.dumps(logos,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    return ''.join(out)
