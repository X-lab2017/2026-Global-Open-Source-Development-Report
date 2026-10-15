/* Resolve chapter-local tokens in standalone SVG exports; no network requests. */
(()=>{const chapter=document.querySelector('.goso-chapter');if(!chapter)return;globalThis.GosoBrand={resolve(text){const style=getComputedStyle(chapter);return text.replace(/var\((--[\w-]+)(?:,\s*([^)]*))?\)/g,(_,key,fallback)=>style.getPropertyValue(key).trim()||fallback||'#10334D');}};})();
