#!/usr/bin/env node
/**
 * fetch_atom_data.js — 抓取 ATOM 项目（https://www.atomproject.ai/）图表源数据
 *
 * ATOM 站点无公开 API，16 张图表的源数据以内嵌 JS 字面量形式存在于
 * Next.js 页面 chunk 中。本脚本下载页面 → 定位 page chunk → 提取全部
 * 图表数据集 → 保存为 JSON 快照。
 *
 * 用法：node scripts/fetch_atom_data.js [输出目录]
 * 默认输出：data/raw/<当前年>/external/atom/
 */
const fs = require('fs');
const path = require('path');

const OUT_DIR = process.argv[2] || path.join('data', 'raw', String(new Date().getFullYear()), 'external', 'atom');
const BASE = 'https://www.atomproject.ai';

// 图表标题清单（与页面 16 张图一一对应，顺序敏感；站点改版后需核对）
const TITLES = [
  'fig-01_huggingface-weekly-user-share-by-region',   // date, us/europe/china/unaffiliated/other
  'fig-02_catching-the-llama-cumulative-downloads',   // date, qwen/metaLlama/mistral/google/deepseek/others
  'fig-03_global-regional-model-adoption',            // date, china/unitedStates/europe
  'fig-04_models-worldwide-cumulative-downloads',     // period, usa/china/eu
  'fig-05_new-open-model-players',                    // period, zaiOrg/nvidia/openai/moonshotai/minimax/deepseek/huggingface
  'fig-06_qwen-ecosystem-dec2025-downloads',          // name, qwen vs all others
  'fig-07_qwen3-effect-5-models-vs-6-orgs',           // name, qwen3 models vs orgs
  'fig-08_share-of-downloads-by-size-tier',           // sizeTier, deepseek/qwen
  'fig-09_share-of-downloads-by-parameter-count',     // bucket, percentOfTotal/downloads
  'fig-10_americas-new-entrants',                     // period, nvidia/allenai/ibm/ai21/arcee
  'fig-11_ai-user-share-by-country',                  // period, unitedStates/china (Microsoft data)
  'fig-12_open-model-inference-market-share',         // date, deepseek/meta/mistral/qwen/openai/minimax/xiaomi/google/zhipu/moonshot/other (OpenRouter)
  'fig-13_ai-user-share-yearly',                      // year, usa/china
  'fig-14_community-elo-rankings-lmarena',            // month, usScore/usModel/chinaScore/chinaModel/otherScore/otherModel
  'fig-15_performance-intelligence-artificialanalysis', // date, usa/china/eu
  'fig-16_derivatives-per-base-model',                // period, qwen/llama/deepseek/mistral/openai
];

function extractBalanced(s, startIdx) {
  let depth = 0, inStr = false, quote = '', esc = false;
  for (let i = startIdx; i < s.length; i++) {
    const c = s[i];
    if (inStr) {
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (c === quote) inStr = false;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = true; quote = c; continue; }
    if (c === '[') depth++;
    if (c === ']') { depth--; if (depth === 0) return s.slice(startIdx, i + 1); }
  }
  return null;
}

async function main() {
  const html = await (await fetch(BASE + '/')).text();
  const m = html.match(/\/_next\/static\/chunks\/app\/page-[a-f0-9]+\.js/);
  if (!m) throw new Error('未找到 page chunk，站点结构可能已改版');
  const chunkUrl = BASE + m[0];
  console.log('page chunk:', chunkUrl);
  const src = await (await fetch(chunkUrl)).text();

  const seen = new Set();
  const datasets = [];
  const patterns = [/([A-Za-z_$][\w$]*)\s*=\s*\[\{/g, /data:\[\{/g];
  for (const re of patterns) {
    let mm;
    while ((mm = re.exec(src)) !== null) {
      const arrStart = mm.index + mm[0].length - 2;
      const block = extractBalanced(src, arrStart);
      if (!block || block.length > 200000 || seen.has(block)) continue;
      let data;
      try { data = Function('"use strict"; return (' + block + ')')(); } catch { continue; }
      if (!Array.isArray(data) || !data.length || typeof data[0] !== 'object' || !data[0]) continue;
      const keys = Object.keys(data[0]);
      if (!keys.some(k => typeof data[0][k] === 'number')) continue; // 跳过签署人/FAQ 等文本数组
      seen.add(block);
      datasets.push({ keys, rows: data.length, data });
    }
  }

  if (datasets.length !== TITLES.length) {
    console.warn(`警告：提取到 ${datasets.length} 个数据集，与预期 ${TITLES.length} 个不一致，请核对站点改版情况`);
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const manifest = [];
  datasets.forEach((r, i) => {
    const name = TITLES[i] || `fig-${String(i + 1).padStart(2, '0')}_unmapped`;
    const file = name + '.json';
    fs.writeFileSync(path.join(OUT_DIR, file), JSON.stringify(r.data, null, 1));
    manifest.push({ file, rows: r.rows, keys: r.keys });
    console.log(`${file}: ${r.rows} rows`);
  });
  fs.writeFileSync(path.join(OUT_DIR, 'manifest.json'),
    JSON.stringify({ source: BASE, page_chunk: chunkUrl, exported_at: new Date().toISOString(), datasets: manifest }, null, 2));
  console.log('TOTAL:', datasets.length, '->', OUT_DIR);
}

main().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
