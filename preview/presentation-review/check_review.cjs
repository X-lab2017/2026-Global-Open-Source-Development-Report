const { chromium } = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/playwright' : 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
(async()=>{
 const dir=process.argv[2], qa=path.join(dir,'qa');await fs.mkdir(qa,{recursive:true});
 const browser=await chromium.launch({...(process.env.GOSD_CHROMIUM_PATH?{executablePath:process.env.GOSD_CHROMIUM_PATH}:{}),args:['--no-sandbox','--disable-dev-shm-usage'],headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:950},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('file://'+path.join(dir,'GOSD-2026-Opening-Chapter1-Review.html'));
 await page.evaluate(()=>document.fonts.ready);
 const count=await page.evaluate(()=>GOSD_REVIEW.data.slides.length);
 const overflow=[];
 for(let i=0;i<count;i++){
  await page.evaluate(i=>GOSD_REVIEW.go(i),i);
  await page.locator('#stage').screenshot({path:path.join(qa,`web-${String(i+1).padStart(2,'0')}.png`)});
  const bad=await page.evaluate(()=>Array.from(document.querySelectorAll('#stage text')).map(e=>({text:e.textContent,box:e.getBBox()})).filter(({box:b})=>b.x<0||b.y<0||b.x+b.width>1281||b.y+b.height>721).map(x=>x.text));
  if(bad.length)overflow.push({slide:i+1,bad});
 }
 await page.evaluate(()=>GOSD_REVIEW.go(0));await page.keyboard.press('ArrowRight');if(await page.evaluate(()=>GOSD_REVIEW.current)!==1)throw Error('keyboard');
 await page.getByRole('button',{name:'目录',exact:true}).click();await page.locator('[data-goto="22"]').click();
 await page.getByRole('button',{name:'正文与来源',exact:true}).click();if(!await page.locator('.source').count())throw Error('source');await page.keyboard.press('Escape');
 await page.evaluate(()=>GOSD_REVIEW.go(24));await page.locator('[data-indicator]').first().click();if(!await page.locator('#drawer').textContent().then(s=>s.includes('数据状态')))throw Error('indicator');await page.keyboard.press('Escape');
 await page.evaluate(()=>GOSD_REVIEW.go(12));await page.locator('#month').fill('0');if(!await page.locator('#month-value').textContent().then(s=>s.includes('25%')))throw Error('month');
 await page.getByRole('button',{name:'评审意见',exact:true}).click();await page.locator('#review-text').fill('验证用评审记录');await page.getByRole('button',{name:'保存本页',exact:true}).click();await page.keyboard.press('Escape');
 await page.getByRole('button',{name:'评审意见',exact:true}).click();
 const reviewDownload=page.waitForEvent('download');await page.getByRole('button',{name:'导出全部意见',exact:true}).click();await(await reviewDownload).saveAs(path.join(qa,'review-download.json'));await page.keyboard.press('Escape');
 await page.evaluate(()=>localStorage.removeItem('gosd-ch1-review'));
 if(await page.locator('#ppt-data').textContent()){
  const pptDownload=page.waitForEvent('download');await page.getByRole('button',{name:'下载 PPTX',exact:true}).click();await(await pptDownload).saveAs(path.join(qa,'exported.pptx'));
 }
 await page.getByRole('button',{name:'浅色',exact:true}).click();await page.locator('#stage').screenshot({path:path.join(qa,'web-light.png')});
 await page.getByRole('button',{name:'全屏',exact:true}).click();const fullscreen=await page.evaluate(()=>!!document.fullscreenElement);if(fullscreen)await page.evaluate(()=>document.exitFullscreen());
 await page.setViewportSize({width:390,height:844});await page.getByRole('button',{name:'目录',exact:true}).click();await page.screenshot({path:path.join(qa,'web-mobile-index.png')});await page.keyboard.press('Escape');
 await page.goto('file://'+path.resolve(__dirname,'../content/assets/cocreation-disc-dark.svg'));await page.setViewportSize({width:504,height:504});await page.locator('svg').screenshot({path:path.join(dir,'disc.png'),omitBackground:true});
 await fs.writeFile(path.join(qa,'web-check.json'),JSON.stringify({count,errors,overflow,fullscreen,checks:['keyboard','index','source','indicator dictionary','month slider','review notes','light theme','mobile index']},null,2));
 console.log(JSON.stringify({count,errors,overflow,fullscreen}));await browser.close();
})();
