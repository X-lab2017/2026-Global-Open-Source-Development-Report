// Shared layout -> native, editable presentation objects. No screenshot slides.
import fs from 'node:fs/promises';
export async function addSlides(presentation, start, end, coverReference) {
 const data=JSON.parse(await fs.readFile(process.env.GOSD_DECK_JSON||new URL('./build/deck.json',import.meta.url),'utf8'));
 const none={style:'solid',fill:'none',width:0};
 const font='Noto Sans CJK SC';
 for(let i=start;i<end;i++) {
  const d=data.slides[i];
  const slide=i===0?presentation.slides.getItem(0):presentation.slides.add({width:1280,height:720});
  slide.background.fill='#091B2B';
  for(const [j,e] of d.elements.entries()) {
   const position={left:e.x,top:e.y,width:e.w,height:e.h};
   if(e.type==='text') {
    const shape=slide.shapes.add({geometry:'textbox',name:d.id+'-text-'+j,position,fill:'none',line:none});
    // Each source-authored line remains separate, without additional auto-wrapping.
    shape.text=e.text.replace('点击指标可查看口径与数据状态。','定义与数据状态见讲者备注。').replace('“正文与来源”','讲者备注');
    shape.text.style={fontSize:e.size,typeface:font,color:e.color,bold:e.bold,alignment:e.align,verticalAlignment:'top',wrap:'none',autoFit:'none',insets:0,lineSpacing:1.35};
   } else if(e.type==='shape')slide.shapes.add({geometry:e.geometry||(e.r?'roundRect':'rect'),name:d.id+'-shape-'+j,position,fill:e.fill,line:none});
   else if(e.type==='line')slide.shapes.add({geometry:'line',name:d.id+'-line-'+j,position,fill:'none',line:{style:'solid',fill:e.color,width:e.width}});
   else if(e.type==='asset'&&coverReference){
    const source=coverReference.startsWith('library-file:')?{path:coverReference}:{blob:new Uint8Array(await fs.readFile(coverReference)),contentType:'image/png'};
    slide.images.add({...source,alt:'报告原有的共同创造圆盘标识',fit:'contain',position});
   }
   else if(e.type==='chart') {
    const bar=e.kind==='bar';
    slide.charts.add(bar?'bar':'line',{
     position,categories:bar?[...e.categories].reverse():e.categories,
     series:e.series.map(s=>({name:s.name,values:bar?[...s.values].reverse():s.values,fill:s.color,line:{style:'solid',fill:s.color,width:3}})),
     hasLegend:!bar,legend:{position:'bottom',textStyle:{typeface:font,fontSize:18,fill:'#AABCCB'}},
     ...(bar?{barOptions:{direction:'bar',grouping:'clustered',gapWidth:52},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'#,##0',textStyle:{typeface:font,fontSize:17,fill:'#F4F8FC'}}}:{lineOptions:{smooth:false}}),
     chartFill:'#091B2B',plotAreaFill:'#091B2B',chartLine:none,plotAreaLine:none,
     xAxis:{visible:true,textStyle:{typeface:font,fontSize:bar?16:11,fill:'#AABCCB'},line:none,majorGridlines:none},
     yAxis:{visible:true,min:0,max:e.max,majorUnit:bar?(e.max===250000?50000:200000):25,textStyle:{typeface:font,fontSize:16,fill:'#AABCCB'},line:none,majorGridlines:{style:'solid',fill:bar?'none':'#315064',width:bar?0:1},numberFormatCode:bar?'#,##0':'0"%"'}
    });
   }
  }
  let notes=d.speakerNotes;
  if(d.indicatorCodes)notes+='\n\n【本页指标定义与状态】\n'+data.indicators.filter(r=>d.indicatorCodes.includes(r.indicator_code)).map(r=>Object.entries(r).map(([k,v])=>k+': '+v).join('\n')).join('\n\n');
  slide.speakerNotes.text=notes;
 }
 return {count:presentation.slides.items.length,added:[start+1,end]};
}
