"""C-Ranking interactive figures and shared publication manuscript."""
import html,json,base64
from pathlib import Path
import company_publication as pub
E=lambda s:html.escape(str(s),quote=True)

def figure(n,data):
 titles=['全球开源企业影响力 Top 30','企业影响力位次变化','企业共同贡献与协作网络']
 tabs=[[('ranking','本期排行榜'),('structure','参与结构'),('scatter','规模与影响'),('compare','企业对照')],[('annual','年度位次'),('monthly','月度位次'),('change','期间变化'),('evidence','变化证据')],[('network','企业协作网'),('projects','项目贡献构成'),('shared','共同项目矩阵'),('evidence','贡献明细')]]
 fallback=''
 if n==1:
  fallback='<table class="cr-fallback"><caption>全球企业 OpenRank Top 30</caption><thead><tr><th>名次</th><th>企业</th><th>OpenRank</th><th>活跃仓库</th><th>关联活跃开发者</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(r[k])+'</td>' for k in ['rank','company_zh','openrank','active_repos','active_developers'])+'</tr>' for r in data['company']['rows'])+'</tbody></table>'
 caption=f'图 3-2-{n} {pub.FIGURES[n-1]}'
 return f'''<figure class="cr-figure rp-figure" id="fig-3-2-{n}"><div class="cr-stage cp-stage goso-unified-canvas" data-slide-key="company-{n}" data-reflow-minimum-width="700" data-slide-height="{[880,780,840][n-1]}" data-lang="zh" data-cr-group="{n}" role="group" aria-label="{E(titles[n-1])}"><div class="cr-board">
<header class="cr-head"><h4>{titles[n-1]}</h4></header><div class="cr-toolbar"></div><nav class="cr-tabs" aria-label="{titles[n-1]}视图">{''.join(f'<button data-cr-view="{key}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(key,label) in enumerate(tabs[n-1]))}</nav>
<div class="cr-body">{fallback}</div><footer class="cr-foot rp-foot"><span class="cr-status" role="status"></span></footer><div class="rp-caption">{E(caption)}</div><div class="cr-overlay" hidden role="region" aria-label="详细信息"></div></div></div><figcaption class="rp-sr-caption">{E(caption)}</figcaption></figure>'''

def section(DATA,REPO):
 out=[pub.section(DATA,figure)]
 logo_dir=Path(__file__).resolve().parents[1]/'content/gosr/company-logos'
 manifest=json.loads((logo_dir/'manifest.json').read_text())
 logos={key:{'file':item['filename'],'data':'data:image/png;base64,'+base64.b64encode((logo_dir/'assets'/item['filename']).read_bytes()).decode()} for key,item in manifest.items()}
 out.append('<script id="company-logos" type="application/json">'+json.dumps(logos,ensure_ascii=False).replace('<','\\u003c')+'</script>')
 out.append('<script id="company-collaboration" type="application/json">'+json.dumps(pub.COLLABORATION,ensure_ascii=False)+'</script>')
 return ''.join(out)
