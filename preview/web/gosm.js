/* GOSM — scoped, source-linked, dependency-free charts. Network 3D is optional. */
(() => {
  "use strict";
  const dataEl = document.getElementById("gosm-data");
  if (!dataEl) return;
  const D = JSON.parse(dataEl.textContent),
    root = document.querySelector(".gm-chapter");
  const BASE = document.querySelector('meta[name="gosd-base"]')?.content || "";
  const asset = (p) => `${BASE}/assets/gosm/${p}`;
  const $ = (s, e = document) => e.querySelector(s),
    $$ = (s, e = document) => Array.from(e.querySelectorAll(s));
  const esc = (x) =>
    String(x ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const fmt = (n, d = 0) =>
    Number(n).toLocaleString("zh-CN", {
      maximumFractionDigits: d,
      minimumFractionDigits: d,
    });
  const compact = (n) =>
    n >= 1e8
      ? fmt(n / 1e8, 1) + "亿"
      : n >= 1e4
        ? fmt(n / 1e4, 1) + "万"
        : fmt(n, 1).replace(/\.0$/, "");
  const sum = (a, k) => a.reduce((s, r) => s + (+r[k] || 0), 0);
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const countryNames = {
    CN: "中国",
    US: "美国",
    FR: "法国",
    DE: "德国",
    GB: "英国",
    CA: "加拿大",
    JP: "日本",
    KR: "韩国",
    IN: "印度",
    AE: "阿联酋",
    SG: "新加坡",
    RU: "俄罗斯",
    NL: "荷兰",
    CH: "瑞士",
    ES: "西班牙",
    AU: "澳大利亚",
    TW: "中国台湾",
    HK: "中国香港",
    IL: "以色列",
    FI: "芬兰",
    SE: "瑞典",
  };
  const cname = (c) =>
    countryNames[c] || D.geography.find((r) => r.id === c)?.name || c;
  const byCode = new Map(
    D.countries.filter((r) => r.region_code).map((r) => [r.region_code, r]),
  );
  const models = new Map(D.network.nodes.map((r) => [r.id, r]));
  const parents = new Map(),
    children = new Map();
  D.network.edges.forEach((e) => {
    if (!parents.has(e.target)) parents.set(e.target, []);
    parents.get(e.target).push(e.source);
    if (!children.has(e.source)) children.set(e.source, []);
    children.get(e.source).push(e.target);
  });
  const quadrants = [
    "高完整-高开放",
    "低完整-高开放",
    "高完整-低开放",
    "低完整-低开放",
  ];
  const panels = $$("[data-gm-chart]"),
    states = new Map();
  const defaults = {
    framework: { lens: "supply", example: D.cases.models[0].model_id },
    supply: { mode: "scale" },
    world: { metric: "models", denom: "known", countries: [] },
    release: {
      months: 12,
      countries: ["CN", "US", "FR", "DE"],
      month: "2026-07",
    },
    cnus: { k: 20 },
    derivation: { mode: "both" },
    network: {
      view: "overview",
      dimension: "2d",
      node: D.network.bases[0]?.id,
      hops: 1,
      direction: "both",
      zoom: 1,
      panX: 0,
      panY: 0,
    },
    flows: { country: "", limit: 15 },
    head: { k: 20, months: 12, mode: "share", month: "2026-08" },
    openness: { sample: "report", quadrant: "", query: "", model: "", page: 0 },
    "open-groups": { group: "region", mode: "share" },
    dossiers: {
      selected: D.cases.models.slice(0, 2).map((r) => r.model_id),
      field: "all",
    },
  };
  panels.forEach((p) => states.set(p, { ...defaults[p.dataset.gmChart] }));
  let C = {},
    palette = [];
  function colors() {
    const dark = document.documentElement.dataset.theme === "dark";
    C = dark
      ? {
          bg: "#123B58",
          paper: "#0D2F49",
          raised: "#194864",
          ink: "#F6FBFF",
          muted: "#B4CEDC",
          line: "#3A5B70",
          brand: "#76D5E4",
          gold: "#EFC179",
          unknown: "#7892A3",
        }
      : {
          bg: "#FFFFFF",
          paper: "#F3F8FA",
          raised: "#E5F0F4",
          ink: "#10334D",
          muted: "#526E7F",
          line: "#C8D9E2",
          brand: "#156993",
          gold: "#A76B24",
          unknown: "#8199A7",
        };
    palette = dark
      ? [
          "#76D5E4",
          "#EFC179",
          "#ABA8F0",
          "#84D7B0",
          "#F29F96",
          "#8DBBF0",
          "#E2A9D7",
          "#CFD088",
        ]
      : [
          "#167D91",
          "#B4792E",
          "#7664B2",
          "#36845B",
          "#BC665D",
          "#4A7DAF",
          "#9D6895",
          "#77842E",
        ];
  }
  const colorCountry = (c) =>
    c === "CN"
      ? palette[0]
      : c === "US"
        ? palette[1]
        : c === "FR"
          ? palette[2]
          : c === "DE"
            ? palette[3]
            : C.unknown;
  const txt = (
    x,
    y,
    s,
    size = 18,
    fill = C.ink,
    anchor = "start",
    extra = "",
  ) =>
    `<text x="${x}" y="${y}" fill="${fill}" font-size="${size}" text-anchor="${anchor}" ${extra}>${esc(s)}</text>`;
  const line = (x, y, x2, y2, c = C.line, w = 1, extra = "") =>
    `<line x1="${x}" y1="${y}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}" ${extra}/>`;
  const box = (x, y, w, h, fill = C.raised, stroke = "none", rx = 10) =>
    `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}"/>`;
  const action = (key, value, label, content) =>
    `<g role="button" tabindex="0" aria-label="${esc(label)}" data-gm-action="${key}" data-value="${esc(value)}" class="gm-svg-action">${content}<title>${esc(label)}</title></g>`;
  function svg(body, w = 1200, h = 570, label = "数据图") {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" class="gm-svg" role="img" aria-label="${esc(label)}" style="font-family:Inter,'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif;background:${C.bg}"><rect width="${w}" height="${h}" fill="${C.bg}"/>${body}</svg>`;
  }
  function btn(key, value, label, active = false, extra = "") {
    return `<button type="button" data-gm-action="${key}" data-value="${esc(value)}" aria-pressed="${active}" ${extra}>${esc(label)}</button>`;
  }
  function seg(key, items, value, label = "") {
    return `<div class="gm-control-group">${label ? `<span>${label}</span>` : ""}<div class="gm-segment">${items.map(([v, l]) => btn(key, v, l, String(v) === String(value))).join("")}</div></div>`;
  }
  const chips = (key, items, selected, label) =>
    `<div class="gm-control-group"><span>${label}</span><div class="gm-chips">${items.map(([v, l]) => btn(key, v, l, selected.includes(v))).join("")}</div></div>`;
  const stat = (value, label, detail = "") =>
    `<div><strong>${esc(value)}</strong><span>${esc(label)}</span>${detail ? `<small>${esc(detail)}</small>` : ""}</div>`;
  const stats = (items) =>
    `<div class="gm-stats">${items.map((a) => stat(...a)).join("")}</div>`;
  const legend = (items) =>
    `<div class="gm-legend">${items.map(([name, c]) => `<span><i style="background:${c}"></i>${esc(name)}</span>`).join("")}</div>`;
  const note = (s) => `<p class="gm-note">${s}</p>`;
  const link = (url, label) =>
    `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(label)} ↗</a>`;
  function set(p, controls, view, readout, rows, source) {
    $(".gm-controls", p).innerHTML = controls;
    $(".gm-view", p).innerHTML = view;
    $(".gm-readout", p).innerHTML = readout || "";
    p.gmRows = rows || [];
    if ($(".gm-source-body", p)) $(".gm-source-body", p).innerHTML = source;
    p.gmTableDirty = true;
    if ($(".gm-table", p).open) fillTable(p);
  }
  function source(keys, explanation) {
    return `<p>${explanation}</p><p>${keys.map((k) => link(asset("data/" + D.files[k]), "原表 " + D.files[k])).join(" · ")}</p><p>${link(asset("provenance.json"), "来源与文件指纹")} · ${link(asset("methods.md"), "完整方法")}</p>`;
  }
  function fillTable(p) {
    const rows=p.gmRows||[],keys=Object.keys(rows[0]||{}),s=states.get(p);
    const isSupply=p.classList.contains("gm-compact-panel");
    const size=isSupply?8:100;
    const pages=Math.max(1,Math.ceil(rows.length/size));s.tablePage=Math.min(s.tablePage||0,pages-1);
    const start=isSupply?s.tablePage*size:0;
    const pager=isSupply?`<div class="s51-table-pager">${btn("table-page","prev","← 上一页",false,start===0?"disabled":"")}<span>${rows.length?start+1:0}—${Math.min(start+size,rows.length)} / ${rows.length} 条</span>${btn("table-page","next","下一页 →",false,s.tablePage===pages-1?"disabled":"")}</div>`:"";
    $(".gm-table-host",p).innerHTML=rows.length?pager+`<table><thead><tr>${keys.map(k=>`<th scope="col">${esc(k)}</th>`).join("")}</tr></thead><tbody>${rows.slice(start,start+size).map(r=>`<tr>${keys.map(k=>`<td>${esc(typeof r[k]==="object"?JSON.stringify(r[k]):r[k])}</td>`).join("")}</tr>`).join("")}</tbody></table>`+note("完整记录保留在图顶“数据 CSV”导出中。") : note("此视角没有匹配记录。");
    p.gmTableDirty=false;
  }
  function plot(
    rows,
    series,
    {
      xkey = "date",
      x = 85,
      y = 65,
      w = 1045,
      h = 355,
      max = null,
      unit = "",
      pointAction = "",
      labelEvery = 1,
      percent = false,
    } = {},
  ) {
    const highest =
      max ||
      Math.max(...rows.flatMap((r) => series.map((s) => +r[s.key] || 0)), 1) *
        1.12;
    const px = (i) => x + (i * w) / Math.max(1, rows.length - 1),
      py = (v) => y + h - (v / highest) * h;
    let out = "";
    for (let j = 0; j <= 4; j++) {
      const v = (highest * j) / 4;
      out +=
        line(x, py(v), x + w, py(v)) +
        txt(
          x - 15,
          py(v) + 6,
          percent ? fmt(v, 0) + "%" : compact(v),
          16,
          C.muted,
          "end",
        );
    }
    out += txt(x, y - 25, unit, 17, C.muted);
    rows.forEach((r, i) => {
      if (i % labelEvery === 0 || i === rows.length - 1)
        out += txt(
          px(i),
          y + h + 32,
          String(r[xkey]).replace("-09-13", ""),
          16,
          C.muted,
          "middle",
        );
    });
    series.forEach((s) => {
      const path = rows
        .map((r, i) => (i ? "L" : "M") + px(i) + "," + py(+r[s.key] || 0))
        .join(" ");
      out += `<path d="${path}" fill="none" stroke="${s.color}" stroke-width="3.5" stroke-linejoin="round"/>`;
      rows.forEach((r, i) => {
        const label = `${r[xkey]} · ${s.name}：${fmt(r[s.key], percent ? 2 : 0)}${percent ? "%" : ""}`;
        const circ = `<circle cx="${px(i)}" cy="${py(r[s.key])}" r="5" fill="${C.bg}" stroke="${s.color}" stroke-width="2.5"/><circle cx="${px(i)}" cy="${py(r[s.key])}" r="14" fill="transparent"/><title>${esc(label)}</title>`;
        out += pointAction ? action(pointAction, r[xkey], label, circ) : circ;
      });
    });
    return out;
  }
  function framework(p, s) {
    const lenses = {
      supply: {
        name: "供给与贡献",
        question: "谁发布了什么？",
        body: "把模型版本、发布账户、国家归属与时间放在一起，观察供给基础及结构。",
        metric: "模型数 · 发布者数 · 月度新增",
        signal: "下载与点赞：获取和关注信号",
        link: "#ch05-s01",
        chapter: "5.1",
        prior: "第二章 A-Map → 第三章 E / M-Ranking",
      },
      reuse: {
        name: "网络与影响力",
        question: "谁在此基础上继续创造？",
        body: "沿明确声明的基座关系，查看后续派生与跨地区连接，再对照 ModelRank 头部构成。",
        metric: "派生关系 · 跨地区连接 · ModelRank",
        signal: "关系数量与榜单席位分别呈现",
        link: "#ch05-s02",
        chapter: "5.2",
        prior: "第二章 D-Map → 第三章 M-Ranking",
      },
      open: {
        name: "开放与公共价值",
        question: "能获取哪些材料，如何继续使用？",
        body: "对照具体版本的权重、代码、数据说明与许可，让开放分类有可复核的证据。",
        metric: "材料完整性 · 开放条件 · 版本档案",
        signal: "观察分类、OSI 定义、DPGA 认可分别判断",
        link: "#ch05-s03",
        chapter: "5.3",
        prior: "第一章 OSDGs / OSDI → 第二章 G-Map",
      },
    };
    const l = lenses[s.lens],
      active = s.lens,
      example =
        D.cases.models.find((m) => m.model_id === s.example) ||
        D.cases.models[0],
      record = models.get(example.model_id);
    let body =
      txt(40, 37, "同一个模型，三个可切换的观察视角", 20, C.muted) +
      txt(1155, 37, "概念框架 · 不表达因果效应", 15, C.muted, "end");
    const paths = [
      ["supply", "M310 180 C360 180 370 225 425 225"],
      ["reuse", "M775 225 C830 225 825 180 880 180"],
      ["open", "M600 390 L600 302"],
    ];
    paths.forEach(
      ([k, d]) =>
        (body += `<path d="${d}" stroke="${k === active ? C.brand : C.line}" stroke-width="${k === active ? 4 : 2}" fill="none" stroke-dasharray="${k === active ? "0" : "5 7"}"/>`),
    );
    body +=
      box(425, 145, 350, 157, C.raised, C.brand, 16) +
      txt(600, 180, "MODEL / VERSION", 17, C.brand, "middle") +
      txt(600, 226, example.title, 27, C.ink, "middle", 'font-weight="650"') +
      txt(
        600,
        267,
        "固定版本 · " + example.revision.slice(0, 10),
        17,
        C.muted,
        "middle",
      );
    [
      [
        "supply",
        40,
        90,
        270,
        180,
        "01 / 供给主体",
        example.publisher,
        "发布账户 · 材料见模型卡",
      ],
      [
        "reuse",
        880,
        90,
        280,
        180,
        "02 / 复用网络",
        record ? record.downstreamCount + " 个直接下游" : "样本未覆盖",
        "2026-10-16 · 非随机关系样本",
      ],
      [
        "open",
        370,
        390,
        460,
        110,
        "03 / 开放条件",
        example.fields.license.label,
        "权重 · 代码 · 数据信息 · 许可",
      ],
    ].forEach(
      ([k, x, y, w, h, a, b, c]) =>
        (body += action(
          "lens",
          k,
          lenses[k].question,
          box(
            x,
            y,
            w,
            h,
            k === active ? C.raised : C.bg,
            k === active ? C.brand : C.line,
            12,
          ) +
            txt(x + 24, y + 33, a, 17, k === active ? C.brand : C.muted) +
            txt(x + 24, y + 70, b, 26, C.ink) +
            txt(x + 24, y + (h === 110 ? 94 : 112), c, 17, C.muted),
        )),
    );
    body +=
      txt(
        80,
        330,
        "5.1 · 规模与结构",
        18,
        active === "supply" ? C.brand : C.muted,
      ) +
      txt(
        905,
        330,
        "5.2 · 连接与演变",
        18,
        active === "reuse" ? C.brand : C.muted,
      ) +
      txt(
        40,
        525,
        "观察单位保持一致；每项指标保留各自的时间、范围与分母。",
        17,
        C.muted,
      );
    set(
      p,
      seg(
        "lens",
        [
          ["supply", "01 供给与贡献"],
          ["reuse", "02 网络与影响力"],
          ["open", "03 开放与公共价值"],
        ],
        active,
      ) +
        seg(
          "example",
          D.cases.models.map((m) => [m.model_id, m.title]),
          example.model_id,
          "同一版本，切换视角",
        ),
      svg(
        body,
        1200,
        550,
        "模型生态观察框架：发布主体、模型版本、复用网络和开放条件",
      ) +
        `<div class="gm-framework-focus"><div><span>${l.chapter} / ${l.name}</span><h4>${l.question}</h4><p>${l.body}</p></div><div><b>${l.metric}</b><p>${l.signal}</p><a href="${l.link}">进入本节 →</a></div></div>`,
      note(
        `${l.prior}。当前示例 ${esc(example.model_id)}：${link(example.fixed_card_url, "固定版本材料")} · ${link("#gm-dossiers", "开放档案")}。供给身份与开放材料核验于2026-10-17；派生数量仅指10月16日关系样本。指标映射不合成新的生态总分。`,
      ),
      Object.entries(lenses).map(([id, r]) => ({
        模型版本: example.model_id,
        固定提交: example.revision,
        视角: r.name,
        问题: r.question,
        指标: r.metric,
        前文: r.prior,
      })),
      `<p>本框架由报告研究问题组织，连接 OSDGs / OSDI、第二章生态地图、第三章榜单与第四章技术全景。模型版本、发布账户、机构与国家不能互相替代。它是阅读与证据组织框架，不是因果模型。</p><p>${link(BASE + "/2026/zh/chapters/01/#ch01-s03", "OSDI 指标")} · ${link(BASE + "/2026/zh/chapters/04/", "技术全景")} · ${link(asset("methods.md"), "方法与对象边界")}</p>`,
    );
  }
  function supply(p, s) {
    let a = D.supply,
      body = "",
      series;
    if (s.mode === "index") {
      a = a.map((r) => ({
        ...r,
        models_index: (r.models / D.supply[0].models) * 100,
        publishers_index: (r.publishers / D.supply[0].publishers) * 100,
      }));
      series = [
        { key: "models_index", name: "模型", color: palette[0] },
        { key: "publishers_index", name: "发布账户", color: palette[1] },
      ];
      body = plot(a, series, { unit: "指数 · 2022 同日 = 100" });
    } else {
      body =
        txt(85, 32, "累计模型", 22, C.ink) +
        plot(a, [{ key: "models", name: "模型", color: palette[0] }], {
          x: 85,
          y: 95,
          w: 450,
          h: 310,
          unit: "模型数",
        }) +
        txt(685, 32, "发布账户", 22, C.ink) +
        plot(a, [{ key: "publishers", name: "发布账户", color: palette[1] }], {
          x: 685,
          y: 95,
          w: 450,
          h: 310,
          unit: "账户数",
        });
    }
    const now = D.supply.at(-1),
      prev = D.supply.at(-2);
    set(
      p,
      seg(
        "mode",
        [
          ["scale", "数量 · 分开坐标"],
          ["index", "增长对照 · 2022 = 100"],
        ],
        s.mode,
      ),
      stats([
        [
          compact(now.models),
          "可见模型",
          `较上一年回溯值 +${fmt((now.models / prev.models - 1) * 100, 1)}%`,
        ],
        [
          compact(now.publishers),
          "发布账户",
          `较上一年回溯值 +${fmt((now.publishers / prev.publishers - 1) * 100, 1)}%`,
        ],
        [
          fmt(now.models / now.publishers, 2),
          "模型 / 发布账户",
          "总体比值，不代表典型账户",
        ],
      ]) +
        svg(body, 1200, 475, "2022—2026年可见模型与发布账户的累计回溯") +
        (s.mode === "index"
          ? legend(series.map((r) => [r.name, r.color]))
          : ""),
      note(
        "2026-09-13 可见样本，按创建时间回溯。账户包括个人与组织；不等于独立模型家族或开发者人数。",
      ),
      a,
      source(
        ["supply"],
        "年度点位均为9月13日，来自同一2026年快照的创建时间回溯；不是各年独立全量存档。数量视图两个面板各有坐标，增长对照统一设2022年=100。",
      ),
    );
  }
  function world(p, s) {
    const metric = {
        models: "模型数",
        downloads_all_time: "累计下载",
        likes: "点赞",
      }[s.metric],
      known = D.countries
        .filter((r) => r.region_code)
        .sort((a, b) => b[s.metric] - a[s.metric]),
      total = sum(D.countries, s.metric),
      kn = sum(known, s.metric),
      denom = s.denom === "known" ? kn : total,
      max = known[0][s.metric];
    let map = txt(35, 35, metric + " · 色深按数量（平方根刻度）", 20, C.muted);
    D.world.forEach((r) => {
      let v = byCode.get(r.code)?.[s.metric],
        selected = s.countries.includes(r.code),
        opacity = v === undefined ? 1 : 0.14 + 0.86 * Math.sqrt(v / max),
        fill = v === undefined ? C.raised : C.brand;
      map +=
        `<g transform="translate(30 50)">` +
        action(
          "country",
          r.code || "",
          r.code && byCode.has(r.code)
            ? `${cname(r.code)} · ${metric} ${fmt(v)}`
            : `${r.name} · 未在可识别样本中列出`,
          `<path d="${r.d}" fill="${fill}" fill-opacity="${opacity}" stroke="${selected ? C.gold : C.bg}" stroke-width="${selected ? 2.4 : 0.6}"/>`,
        ) +
        `</g>`;
    });
    map +=
      box(35, 505, 15, 10, C.raised) +
      txt(59, 515, "未列出 / 未识别", 16, C.muted) +
      txt(900, 515, "点击地图或右侧国家 · 最多比较 3 个", 16, C.muted, "end");
    const list = known
      .slice(0, 15)
      .map(
        (r, i) =>
          `<button data-gm-action="country" data-value="${r.region_code}" aria-pressed="${s.countries.includes(r.region_code)}"><span>${String(i + 1).padStart(2, "0")} ${esc(cname(r.region_code))}</span><strong>${fmt((r[s.metric] / denom) * 100, 2)}%</strong><i style="width:${(r[s.metric] / max) * 100}%"></i></button>`,
      )
      .join("");
    const selected = s.countries.map((c) => byCode.get(c)).filter(Boolean);
    set(
      p,
      seg(
        "metric",
        [
          ["models", "模型供给"],
          ["downloads_all_time", "累计下载"],
          ["likes", "社区点赞"],
        ],
        s.metric,
      ) +
        seg(
          "denom",
          [
            ["known", "已识别国家内份额"],
            ["global", "平台总量内份额"],
          ],
          s.denom,
        ) +
        btn(
          "clear",
          "",
          "清空选择",
          false,
          s.countries.length ? "" : "disabled",
        ),
      stats([
        [
          fmt((kn / total) * 100, 1) + "%",
          "此指标国家识别覆盖",
          "分母：平台该指标总量",
        ],
        [fmt(known.length), "已识别国家 / 地区", "组织归属口径"],
        [fmt(kn), `已识别部分 · ${metric}`, "826 个组织的模型样本"],
      ]) +
        `<div class="gm-map-layout"><div>${svg(map, 950, 540, "全球模型供给与获取分布")}</div><aside class="gm-ranking" aria-label="国家前15名"><h4>前 15 · ${metric}</h4>${list}</aside></div>`,
      selected.length
        ? stats(
            selected.map((r) => [
              fmt((r[s.metric] / denom) * 100, 2) + "%",
              cname(r.region_code),
              `${metric} ${fmt(r[s.metric])}`,
            ]),
          )
        : note(
            "地图默认不选国家。选择后在图内并列比较；份额切换会改变分母，不改变数量。",
          ),
      known.map((r) => ({
        国家: cname(r.region_code),
        指标: metric,
        数量: r[s.metric],
        份额_pct: (r[s.metric] / denom) * 100,
        分母: s.denom === "known" ? "国家可识别部分" : "平台总量",
        快照: "2026-09-13",
      })),
      source(
        ["countries"],
        "国家是归属可识别的发布组织所在地，不是开发者国籍或实际使用者所在地。个人账户不进入组织国家比较，未知归属保留在平台总量中。该部分71,578个模型约占平台模型2.3%，累计下载约占79.9%。",
      ),
    );
  }
  function release(p, s) {
    const rows = D.monthly.slice(-s.months),
      series = s.countries.map((c) => ({
        key: c,
        name: cname(c),
        color: colorCountry(c),
      })),
      selected = rows.find((r) => r.month === s.month) || rows.at(-1);
    let body = plot(rows, series, {
      xkey: "month",
      pointAction: "month",
      unit: "当月新建且快照时仍可见的模型",
    });
    const idx = rows.indexOf(selected),
      x = 85 + (idx * 1045) / (rows.length - 1);
    body += line(x, 60, x, 420, C.line, 1, 'stroke-dasharray="4 6"');
    set(
      p,
      seg(
        "months",
        [
          [6, "6 个月"],
          [12, "12 个月"],
        ],
        s.months,
      ) +
        chips(
          "country",
          ["CN", "US", "FR", "DE"].map((c) => [c, cname(c)]),
          s.countries,
          "国家 / 地区",
        ),
      svg(body, 1200, 485, "四国月度新建模型数") +
        legend(series.map((r) => [r.name, r.color])) +
        `<div class="gm-month-control"><label>查看月份 <input type="range" min="0" max="${rows.length - 1}" value="${rows.indexOf(selected)}" data-gm-range="release" aria-label="查看新增模型月份"></label><b>${selected.month}</b></div>`,
      stats(
        s.countries.map((c) => [
          fmt(selected[c]),
          cname(c),
          selected.month + " 新建模型",
        ]),
      ) +
        (selected.month === "2026-07" && s.countries.includes("FR")
          ? note(
              "<b>原稿核验案例：</b>法国 7 月的 784 个新增中，755 个来自 OpenMed，其中 751 个为集中发布的 Android 适配、4 个为 MLX 适配。该案例解释发布事件，不据此推断全部新增的性质。",
            )
          : note(
              "点击折线点或拖动月份。基础发布、微调、量化与适配应结合模型记录解释；当前来源覆盖 12 个月。",
            )),
      rows.map((r) =>
        Object.fromEntries(["month", ...s.countries].map((k) => [k, r[k]])),
      ),
      source(
        ["monthly"],
        "窗口为2025-09—2026-08，来自2026-09-13快照按创建月份回溯，仅保留原表四国。OpenMed事件解释沿用5.1原稿核验记录；尚未补充逐条原始发布清单。",
      ),
    );
  }
  function cnus(p, s) {
    const cn = byCode.get("CN"),
      us = byCode.get("US");
    const metrics = [
      ["models", "模型供给"],
      ["downloads_all_time", "累计下载"],
      ["likes", "社区点赞"],
    ];
    let b =
      txt(35, 32, "供给、获取与关注", 23) +
      txt(35, 61, "2026-09-13 · 已识别国家组织样本内份额", 16, C.muted);
    metrics.forEach(([key, name], i) => {
      let y = 104 + i * 111,
        x = 210,
        w = 900;
      const c = cn[key + "_known_share_pct"],
        u = us[key + "_known_share_pct"];
      b +=
        txt(35, y + 25, name, 20) +
        box(x, y, w, 35, C.raised, "none", 3) +
        box(x, y, (w * c) / 100, 35, palette[0], "none", 0) +
        box(x + (w * c) / 100, y, (w * u) / 100, 35, palette[1], "none", 0) +
        txt(
          x,
          y + 64,
          `中国 ${fmt(c, 2)}% · ${compact(cn[key])}`,
          17,
          palette[0],
        ) +
        txt(
          x + 400,
          y + 64,
          `美国 ${fmt(u, 2)}% · ${compact(us[key])}`,
          17,
          palette[1],
        ) +
        txt(1110, y + 64, `其他 ${fmt(100 - c - u, 2)}%`, 15, C.muted, "end");
    });
    const h = D.head.filter((r) => r.k === s.k).at(-1);
    b +=
      line(35, 427, 1150, 427) +
      txt(35, 470, `ModelRank Top ${s.k} · 2026-08`, 23) +
      txt(35, 500, "头部席位 · 分母包含未知归属", 16, C.muted);
    [
      ["中国", h.china, palette[0]],
      ["美国", h.us, palette[1]],
      ["其他已识别", h.other_known, C.muted],
      ["未知归属", h.unknown, C.unknown],
    ].forEach(([label, n, c], i) => {
      b +=
        txt(
          440 + i * 185,
          472,
          `${n} 席`,
          30,
          c,
          "middle",
          'font-weight="650"',
        ) +
        txt(
          440 + i * 185,
          504,
          `${label} · ${fmt((n / s.k) * 100, 1)}%`,
          16,
          C.muted,
          "middle",
        );
    });
    set(
      p,
      seg(
        "k",
        [
          [20, "Top 20"],
          [100, "Top 100"],
          [1000, "Top 1000"],
        ],
        s.k,
        "头部观察深度",
      ),
      svg(b, 1200, 550, "中美模型生态专题：供给份额与ModelRank头部席位") +
        legend([
          ["中国", palette[0]],
          ["美国", palette[1]],
          ["其他 / 未知", C.unknown],
        ]),
      note(
        `<b>读图：</b>美国在此可识别样本中的供给与下载份额较高；中国点赞份额高于模型供给份额。当前 Top ${s.k} 中，中美分别占 ${fmt((h.china / s.k) * 100, 1)}% 与 ${fmt((h.us / s.k) * 100, 1)}%。这些维度不能合并为国家能力总分。`,
      ),
      [
        ...metrics.map(([key, name]) => ({
          维度: name,
          中国: cn[key],
          美国: us[key],
          中国份额: cn[key + "_known_share_pct"],
          美国份额: us[key + "_known_share_pct"],
          范围: "已识别国家的组织模型",
          日期: "2026-09-13",
        })),
        {
          维度: `ModelRank Top ${s.k}`,
          中国: h.china,
          美国: h.us,
          中国份额: (h.china / s.k) * 100,
          美国份额: (h.us / s.k) * 100,
          范围: `${s.k}个模型版本，未知${h.unknown}席`,
          日期: h.month,
        },
      ],
      source(
        ["countries", "head"],
        "上半图份额分母为国家可识别的组织模型；下半图分母为所选榜单深度，保留未知归属。累计下载不是独立用户或能力，点赞不是实质贡献，榜单席位不是影响力得分份额。不同统计日期与覆盖分别标注。",
      ),
    );
  }
  function derivation(p, s) {
    const a = D.derivation,
      n = a.at(-1),
      prev = a.at(-2);
    let b =
      txt(85, 32, "派生规模", 23) +
      plot(
        a,
        [{ key: "derived_models", name: "派生模型", color: palette[0] }],
        { x: 85, y: 95, w: 450, h: 310, unit: "模型数" },
      ) +
      txt(685, 32, "派生占比", 23) +
      plot(a, [{ key: "derived_pct", name: "派生占比", color: palette[1] }], {
        x: 685,
        y: 95,
        w: 450,
        h: 310,
        max: 35,
        percent: true,
        unit: "派生模型 / 可见模型",
      });
    set(
      p,
      "",
      stats([
        [
          compact(n.derived_models),
          "派生模型",
          `较上一年回溯值 +${fmt((n.derived_models / prev.derived_models - 1) * 100, 1)}%`,
        ],
        [
          fmt(n.derived_pct, 2) + "%",
          "可见模型中的派生比例",
          `较上一年 ${fmt(n.derived_pct - prev.derived_pct, 2)} 个百分点`,
        ],
      ]) + svg(b, 1200, 475, "模型派生数量与派生比例"),
      note(
        "两个面板使用独立纵轴。派生识别依赖声明和可见元数据，缺少标记不能解释为没有复用。",
      ),
      a,
      source(
        ["derivation"],
        "2026-09-13可见样本的累计创建时间回溯，模型与派生数量来自同一底表。派生比例=派生模型数/可见模型数；数量与比例分别观察。",
      ),
    );
  }
  const pairs = (() => {
    const m = new Map();
    D.flows.forEach((r) => {
      const k = [r.source, r.target].sort().join("|");
      m.set(k, (m.get(k) || 0) + r.weight);
    });
    return [...m]
      .map(([k, weight]) => ({
        a: k.split("|")[0],
        b: k.split("|")[1],
        weight,
      }))
      .sort((a, b) => b.weight - a.weight);
  })();
  const flowCountries = [...new Set(pairs.flatMap((r) => [r.a, r.b]))]
    .map((id) => ({
      id,
      weight: pairs
        .filter((r) => r.a === id || r.b === id)
        .reduce((s, r) => s + r.weight, 0),
    }))
    .sort((a, b) => b.weight - a.weight);
  function flows(p, s) {
    const visible = pairs
        .filter((r) => !s.country || r.a === s.country || r.b === s.country)
        .slice(0, s.limit),
      ids = s.country
        ? [s.country, ...visible.map((r) => (r.a === s.country ? r.b : r.a))]
        : [...new Set(visible.flatMap((r) => [r.a, r.b]))];
    const pos = new Map(
      ids.map((id, i) => {
        const a = -Math.PI / 2 + (i * 2 * Math.PI) / ids.length;
        return [id, { x: 450 + Math.cos(a) * 300, y: 305 + Math.sin(a) * 220 }];
      }),
    );
    let b = txt(
      35,
      32,
      s.country
        ? cname(s.country) + " · 主要复用关联"
        : "跨地区连接 · 主要关联对",
      22,
    );
    visible.forEach((r) => {
      const a = pos.get(r.a),
        z = pos.get(r.b);
      b += `<path d="M${a.x},${a.y} Q450,305 ${z.x},${z.y}" stroke="${s.country ? C.brand : C.line}" stroke-opacity=".7" stroke-width="${1 + 8 * Math.sqrt(r.weight / visible[0].weight)}" fill="none"><title>${esc(cname(r.a) + " ↔ " + cname(r.b) + "：" + fmt(r.weight))}</title></path>`;
    });
    ids.forEach((id, i) => {
      const a = pos.get(id);
      b += action(
        "flow-country",
        id,
        cname(id) + " · 查看关联",
        `<circle cx="${a.x}" cy="${a.y}" r="${id === s.country ? 17 : 10}" fill="${id === s.country ? C.gold : palette[i % palette.length]}"/>` +
          txt(
            a.x,
            a.y + (a.y < 305 ? -20 : 33),
            cname(id),
            18,
            C.ink,
            "middle",
          ),
      );
    });
    const list = visible
      .map(
        (r, i) =>
          `<div><span>${String(i + 1).padStart(2, "0")} ${esc(cname(r.a))} ↔ ${esc(cname(r.b))}</span><strong>${fmt(r.weight)}</strong><i style="width:${(r.weight / visible[0].weight) * 100}%"></i></div>`,
      )
      .join("");
    set(
      p,
      chips(
        "flow-country",
        flowCountries.slice(0, 12).map((r) => [r.id, cname(r.id)]),
        s.country ? [s.country] : [],
        "选择国家 / 地区",
      ) +
        seg(
          "limit",
          [
            [10, "前 10 对"],
            [15, "前 15 对"],
            [25, "前 25 对"],
          ],
          s.limit,
        ) +
        btn("clear", "", "全部国家", !s.country),
      stats([
        [fmt(sum(pairs, "weight")), "可识别跨国关系", "139 个无向国家对"],
        [fmt(flowCountries.length), "涉及国家 / 地区", "双端归属已识别"],
        ["43.7%", "中美关联占此样本比例", "4,782 对 · 不代表全球复用总量"],
      ]) +
        `<div class="gm-flow-layout"><div>${svg(b, 900, 590, "跨地区模型复用关联网络，线不表达方向")}</div><aside class="gm-flow-list"><h4>关联对 · ${s.country ? cname(s.country) : "全样本"} / 当前 ${visible.length} 对</h4>${list}</aside></div>`,
      note(
        "线宽表示样本关系数；圆周位置仅便于阅读。原表未说明 source / target 的基座角色，因此合并双向计数，展示无向关联。",
      ),
      visible.map((r) => ({
        地区A: cname(r.a),
        地区B: cname(r.b),
        关系数: r.weight,
        快照: "2026-09-13",
        方向: "无向合并",
      })),
      source(
        ["flows"],
        "原表186行，合并双向后139个无向国家对，关系数合计10,943不变。只覆盖双端国家可识别的跨国关系，不含国内复用；不能解释为实际部署量或使用者所在地。",
      ),
    );
  }
  function head(p, s) {
    const rows = D.head.filter((r) => r.k === s.k).slice(-s.months),
      keys = [
        ["china", "中国", palette[0]],
        ["us", "美国", palette[1]],
        ["other_known", "其他已识别", palette[2]],
        ["unknown", "未知归属", C.unknown],
      ];
    let b = txt(
      70,
      35,
      `ModelRank Top ${s.k} · ${s.mode === "share" ? "席位份额" : "席位数"}`,
      22,
    );
    const x = 80,
      y = 85,
      w = 1040,
      h = 330,
      step = w / rows.length,
      bw = Math.min(56, step * 0.72);
    for (let i = 0; i <= 4; i++)
      b +=
        line(x, y + h - (i * h) / 4, x + w, y + h - (i * h) / 4) +
        txt(
          x - 13,
          y + h - (i * h) / 4 + 6,
          s.mode === "share" ? 25 * i + "%" : fmt((s.k * i) / 4),
          16,
          C.muted,
          "end",
        );
    rows.forEach((r, i) => {
      let bottom = y + h;
      let bar = "";
      keys.forEach(([k, label, c]) => {
        const bh = (r[k] / s.k) * h;
        bar += box(
          x + i * step + (step - bw) / 2,
          bottom - bh,
          bw,
          bh,
          c,
          "none",
          1,
        );
        bottom -= bh;
      });
      b += action(
        "month",
        r.month,
        `${r.month}：中国${r.china}，美国${r.us}，其他${r.other_known}，未知${r.unknown}`,
        bar,
      );
      if (i % (rows.length > 12 ? 2 : 1) === 0 || i === rows.length - 1)
        b += txt(
          x + (i + 0.5) * step,
          y + h + 32,
          r.month.slice(2),
          16,
          C.muted,
          "middle",
        );
    });
    const selected = rows.find((r) => r.month === s.month) || rows.at(-1);
    set(
      p,
      seg(
        "k",
        [
          [20, "Top 20"],
          [100, "Top 100"],
          [1000, "Top 1000"],
        ],
        s.k,
      ) +
        seg(
          "months",
          [
            [6, "6 个月"],
            [12, "12 个月"],
            [18, "18 个月"],
          ],
          s.months,
        ) +
        seg(
          "mode",
          [
            ["share", "席位份额"],
            ["count", "席位数"],
          ],
          s.mode,
        ),
      svg(b, 1200, 475, "ModelRank头部模型国家席位构成逐月变化") +
        legend(keys.map((r) => [r[1], r[2]])) +
        `<div class="gm-month-control"><label>查看月份 <input type="range" min="0" max="${rows.length - 1}" value="${rows.indexOf(selected)}" data-gm-range="head" aria-label="查看头部席位月份"></label><b>${selected.month}</b></div>`,
      stats(
        keys.map(([k, label]) => [
          fmt(selected[k]) + " 席",
          label,
          fmt((selected[k] / s.k) * 100, 1) + "%",
        ]),
      ) +
        note(
          "各月按模型版本计席位，分母保留未知归属。点击柱形或拖动月份即可查看明细，不把席位数称为贡献或影响力份额。",
        ),
      rows,
      source(
        ["head"],
        "来源覆盖2024-07—2026-08，共26个月；展示最近6、12或18个月。各月Top 20/100/1000独立统计；榜单深度变化不构成同一模型群体的纵向比较。",
      ),
    );
  }
  function networkSlice(s) {
    let nodes = [],
      edges = [],
      positions = new Map(),
      levels = new Map();
    if (s.view === "overview") {
      D.network.overview.forEach((r) =>
        positions.set(r.id, {
          x: r.overviewX * 0.75,
          y: r.overviewY * 0.75,
          cluster: r.overviewCluster,
        }),
      );
      nodes = D.network.overview.map((r) => models.get(r.id));
    } else if (s.view === "all") {
      nodes = D.network.nodes;
      const xs = nodes.map((n) => n.x),
        ys = nodes.map((n) => n.y),
        xmin = Math.min(...xs),
        xmax = Math.max(...xs),
        ymin = Math.min(...ys),
        ymax = Math.max(...ys);
      nodes.forEach((n) =>
        positions.set(n.id, {
          x: 60 + ((n.x - xmin) / (xmax - xmin)) * 1080,
          y: 55 + ((n.y - ymin) / (ymax - ymin)) * 720,
          cluster: n.sourceCommunity % 12,
        }),
      );
    } else {
      levels.set(s.node, 0);
      for (const direction of s.direction === "both"
        ? [-1, 1]
        : s.direction === "up"
          ? [-1]
          : [1]) {
        let frontier = [s.node];
        for (let hop = 1; hop <= s.hops; hop++) {
          const next = [];
          frontier.forEach((id) =>
            (direction < 0 ? parents : children).get(id)?.forEach((n) => {
              if (!levels.has(n)) {
                levels.set(n, direction * hop);
                next.push(n);
              }
            }),
          );
          frontier = next;
        }
      }
      nodes = [...levels.keys()].map((id) => models.get(id)).filter(Boolean);
      positions.set(s.node, { x: 600, y: 410, cluster: 0 });
      for (const level of [-2, -1, 1, 2]) {
        const group = nodes
            .filter((n) => levels.get(n.id) === level)
            .sort((a, b) => a.id.localeCompare(b.id)),
          r = Math.abs(level) === 1 ? 260 : 460;
        group.forEach((n, i) => {
          const a = -1.32 + ((i + 0.5) * 2.64) / group.length,
            side = level < 0 ? -1 : 1;
          positions.set(n.id, {
            x: 600 + side * Math.cos(a) * r,
            y: 410 + Math.sin(a) * r * 0.76,
            cluster: level < 0 ? 1 : 0,
          });
        });
      }
    }
    const ids = new Set(nodes.map((n) => n.id));
    edges = D.network.edges.filter(
      (e) => ids.has(e.source) && ids.has(e.target),
    );
    return { nodes, edges, positions, levels };
  }
  function networkSvg(s, slice) {
    const { nodes, edges, positions } = slice;
    let body = "";
    if (s.view === "lineage")
      body =
        txt(40, 35, "上游基座", 21, palette[1]) +
        txt(1160, 35, "下游派生", 21, palette[0], "end") +
        line(600, 65, 600, 770, C.line, 1, 'stroke-dasharray="4 7"');
    else
      body =
        txt(
          35,
          32,
          s.view === "overview"
            ? "12 个发布账户 · 主要基座及直接派生"
            : "全部可见声明关系 · 固定样本",
          20,
          C.muted,
        ) +
        txt(
          1160,
          32,
          `${fmt(nodes.length)} 模型 / ${fmt(edges.length)} 关系`,
          17,
          C.muted,
          "end",
        );
    let graph = "";
    const near = new Set([
      s.node,
      ...(children.get(s.node) || []),
      ...(parents.get(s.node) || []),
    ]);
    edges.forEach((e) => {
      const a = positions.get(e.source),
        b = positions.get(e.target),
        active = e.source === s.node || e.target === s.node;
      graph += `<path d="M${a.x},${a.y} Q${(a.x + b.x) / 2},${(a.y + b.y) / 2 - 13} ${b.x},${b.y}" stroke="${active ? C.brand : C.line}" stroke-width="${active ? 1.8 : 0.8}" stroke-opacity="${active ? 0.85 : s.view === "all" ? 0.25 : 0.5}" fill="none" ${s.view === "lineage" && nodes.length < 70 ? 'marker-end="url(#gm-edge-arrow)"' : ""}><title>${esc(e.source + " → " + e.target)}</title></path>`;
    });
    nodes.forEach((n) => {
      const p = positions.get(n.id),
        selected = n.id === s.node,
        r = selected
          ? 11
          : clamp(2.8 + Math.sqrt(n.downstreamCount || 0) * 0.65, 3, 12),
        opacity = s.view === "lineage" || near.has(n.id) ? 1 : 0.72;
      graph += action(
        "node",
        n.id,
        n.id + " · 样本内直接下游 " + n.downstreamCount,
        `<circle cx="${p.x}" cy="${p.y}" r="${r + 5}" fill="transparent"/><circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${selected ? C.gold : palette[(p.cluster || 0) % palette.length]}" fill-opacity="${opacity}" stroke="${selected ? C.ink : C.bg}" stroke-width="${selected ? 2 : 0.6}"/>`,
      );
    });
    if (s.view === "overview")
      D.network.bases.forEach((n) => {
        const p = positions.get(n.id);
        if (p)
          graph += txt(
            p.x,
            p.y - 22,
            n.id.length > 37 ? n.id.slice(0, 35) + "…" : n.id,
            15,
            C.ink,
            "middle",
            'paint-order="stroke" stroke="' +
              C.bg +
              '" stroke-width="5" stroke-linejoin="round"',
          );
      });
    else
      nodes
        .filter(
          (n) =>
            n.id === s.node || (s.view === "lineage" && nodes.length <= 32),
        )
        .forEach((n) => {
          const p = positions.get(n.id);
          graph += txt(
            p.x,
            p.y + 26,
            n.name.length > 32 ? n.name.slice(0, 30) + "…" : n.name,
            16,
            C.ink,
            "middle",
            'paint-order="stroke" stroke="' + C.bg + '" stroke-width="4"',
          );
        });
    const transform = `translate(${600 + s.panX} ${410 + s.panY}) scale(${s.zoom}) translate(-600 -410)`;
    body +=
      `<defs><marker id="gm-edge-arrow" viewBox="0 0 10 10" refX="13" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="${C.brand}"/></marker></defs><g data-gm-camera transform="${transform}">${graph}</g>` +
      txt(
        35,
        810,
        "位置用于导航；大小为样本内直接下游数。声明关系：基座 → 派生。",
        16,
        C.muted,
      );
    return svg(body, 1200, 840, "模型基座与派生关系网络，可搜索或选择模型");
  }
  function nodeDetail(s, slice) {
    const n = models.get(s.node);
    if (!n) return note("选择模型查看关系。");
    const list = (ids, title) =>
      `<div class="gm-neighbors"><h5>${title} <span>${ids.length}</span></h5>${
        ids.length
          ? ids
              .slice()
              .sort(
                (a, b) =>
                  (models.get(b)?.downstreamCount || 0) -
                    (models.get(a)?.downstreamCount || 0) || a.localeCompare(b),
              )
              .slice(0, 30)
              .map((id) => btn("node", id, id, false))
              .join("")
          : note("此样本未记录。")
      }${ids.length > 30 ? note("面板列出前 30 个；全部关系可在谱系图和 CSV 中查看。") : ""}</div>`;
    return `<aside class="gm-node-detail"><span class="eyebrow">MODEL / ${s.view === "lineage" ? "LINEAGE" : "SELECTED"}</span><h4>${esc(n.id)}</h4><p>${esc(n.task || "任务未记录")} · ${esc(n.library || "框架未记录")}</p>${stats(
      [
        [fmt(n.upstreamCount), "记录的直接上游"],
        [fmt(n.downstreamCount), "记录的直接下游"],
      ],
    )}<div class="gm-node-actions">${btn("view", "lineage", "展开该模型谱系", s.view === "lineage")}${link(n.url, "模型卡")}</div>${note(slice.positions.has(n.id) ? "已选模型以金色标记。" : "该模型不在当前概览；展开谱系查看。")}${list(parents.get(n.id) || [], "直接上游")}${list(children.get(n.id) || [], "直接下游")}</aside>`;
  }
  let threeModule;
  function network(p, s) {
    if (p.gm3d) {
      if (p.gm3dView === s.view) s.orbit = p.gm3d.snapshot();
      p.gm3d.dispose();
      p.gm3d = null;
    }
    const slice = networkSlice(s),
      view = networkSvg(s, slice),
      controls =
        seg(
          "view",
          [
            ["overview", "簇群全景"],
            ["all", "全部关系"],
            ["lineage", "所选谱系"],
          ],
          s.view,
        ) +
        seg(
          "dimension",
          [
            ["2d", "2D"],
            ["3d", "3D"],
          ],
          s.dimension,
        ) +
        (s.view === "lineage"
          ? seg(
              "direction",
              [
                ["both", "上下游"],
                ["up", "上游"],
                ["down", "下游"],
              ],
              s.direction,
            ) +
            seg(
              "hops",
              [
                [1, "1 层"],
                [2, "2 层"],
              ],
              s.hops,
            )
          : "") +
        `<div class="gm-control-group gm-search-wrap"><label for="gm-model-search">搜索模型</label><input id="gm-model-search" type="search" data-gm-search="network" placeholder="模型名称或发布账户" autocomplete="off" aria-controls="gm-model-results"><div id="gm-model-results" class="gm-search-results"></div></div><div class="gm-zoom">${btn("zoom", "in", "＋")}${btn("zoom", "out", "−")}${btn("reset", "", "复位")}</div>`;
    const rows = slice.edges.map((e) => ({
      基座: e.source,
      派生: e.target,
      关系类型: "模型卡声明的基座",
      快照: "2026-10-16",
    }));
    set(
      p,
      controls,
      `<div class="gm-network-layout"><div class="gm-network-stage" data-dimension="${s.dimension}">${view}<div class="gm-three-host" ${s.dimension === "3d" ? "" : "hidden"}></div><span class="gm-stage-hint">${s.dimension === "3d" ? "拖动旋转 · 滚轮缩放 · 点击选模型" : "拖动空白处平移 · ＋/− 缩放 · 点击选模型"}</span></div>${nodeDetail(s, slice)}</div>`,
      note(
        `<b>2026-10-16 参考快照：</b>完整关系样本 ${fmt(D.network.nodes.length)} 模型 / ${fmt(D.network.edges.length)} 条边。首屏选择 12 个发布账户各自样本内派生最多的基座及其直接派生（677 模型）；可切换全部关系或搜索任一模型。此非随机样本不代表平台全量。`,
      ),
      rows,
      `<p>数据来自 ${link(D.network.meta.sourceFile, "参考项目快照")}，上游 ${link(D.network.meta.upstreamDataset, "Hugging Face hub-stats")}，固定 revision <code>${esc(D.network.meta.upstreamRevisionDeclared)}</code>。已剔除任务相似、同作者等推断关系，只保留明确声明的 base-model 边并统一为基座→派生。</p><p>上游采用按数据集顺序取前12,000模型的非随机样本，只保留双端可见关系；原图每对节点按优先级保留一条边。全图坐标继承原布局，概览为确定性簇群布局；位置、距离与3D纵深均无统计含义，节点大小不是ModelRank。没有国家字段，不按名称推断。</p><p>${link(asset("network.json"), "完整模型与关系 JSON")} · ${link(asset("lineage-live-provenance.json"), "抽取与许可记录")} · ${link(asset("extract_lineage.py"), "可复现抽取脚本")}</p>`,
    );
    p.gmNetworkSlice = slice;
    const stage = $(".gm-network-stage", p),
      sv = $("svg", stage);
    bindPan(p, sv);
    if (s.dimension === "3d") {
      const token = (p.gmRenderToken || 0) + 1;
      p.gmRenderToken = token;
      const host = $(".gm-three-host", stage);
      host.innerHTML = '<p class="gm-three-status">正在载入 3D 视图…</p>';
      (
        threeModule ||
        (threeModule = import(`${BASE}/gosm-network.mjs?v=${D.version}`))
      )
        .then((m) => {
          if (
            p.gmRenderToken !== token ||
            states.get(p).dimension !== "3d" ||
            !host.isConnected
          )
            return;
          host.innerHTML = "";
          p.gm3d = m.mount(host, {
            nodes: slice.nodes,
            edges: slice.edges,
            positions: [...slice.positions],
            orbit: s.orbit,
            selected: s.node,
            colors: { ...C, palette },
            onSelect: (id) => {
              s.node = id;
              draw(p);
            },
          });
          p.gm3dView = s.view;
          stage.classList.add("gm-three-ready");
        })
        .catch(() => {
          if (host.isConnected) {
            host.innerHTML =
              '<p class="gm-three-status">此环境无法使用 WebGL，已保留可交互 2D 网络。</p>';
            stage.classList.add("gm-three-failed");
          }
        });
    }
  }
  function bindPan(p, sv) {
    let drag = null;
    sv.addEventListener("pointerdown", (e) => {
      if (e.button !== 0 || e.target.closest("[data-gm-action]")) return;
      const s = states.get(p);
      drag = { x: e.clientX, y: e.clientY, px: s.panX, py: s.panY };
      sv.setPointerCapture?.(e.pointerId);
    });
    sv.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const s = states.get(p),
        r = sv.getBoundingClientRect(),
        scale = 1200 / Math.max(r.width, 1);
      s.panX = drag.px + (e.clientX - drag.x) * scale;
      s.panY = drag.py + (e.clientY - drag.y) * scale;
      const g = $("[data-gm-camera]", sv);
      g?.setAttribute(
        "transform",
        `translate(${600 + s.panX} ${410 + s.panY}) scale(${s.zoom}) translate(-600 -410)`,
      );
    });
    sv.addEventListener("pointerup", () => (drag = null));
    sv.addEventListener("pointercancel", () => (drag = null));
  }
  function opennessRows(s) {
    if (s.sample === "current")
      return D.opennessCurrent.quadrants.map((r) => ({
        quadrant: r.name,
        models: r.models,
        share_pct: r.share_pct,
      }));
    return D.quadrants.map((r) => ({
      quadrant: r.completeness + "-" + r.openness,
      models: r.models,
      share_pct: r.share_pct,
    }));
  }
  function openMatches(s) {
    return D.opennessCurrent.models.filter(
      (m) =>
        (!s.quadrant || m.strict_quadrant === s.quadrant) &&
        (!s.query ||
          (m.model_id + " " + m.story_org + " " + m.country)
            .toLowerCase()
            .includes(s.query.toLowerCase())),
    );
  }
  function openBrowser(p, s) {
    const arr = openMatches(s),
      size = 7,
      pages = Math.max(1, Math.ceil(arr.length / size));
    s.page = clamp(s.page, 0, pages - 1);
    const list = arr.slice(s.page * size, (s.page + 1) * size),
      selected = D.opennessCurrent.models.find((m) => m.model_id === s.model);
    return `<div class="gm-open-list"><div class="gm-list-top"><b>${fmt(arr.length)} 个匹配模型</b><span>${s.page + 1} / ${pages}</span></div>${list.map((m) => `<button data-gm-action="open-model" data-value="${esc(m.model_id)}" aria-pressed="${s.model === m.model_id}"><b>${esc(m.model_id)}</b><span>${esc(m.strict_final_grade)} · ${esc(m.country === "Unknown" ? "归属未知" : m.country)}</span></button>`).join("") || note("没有匹配模型。")}<div class="gm-pager">${btn("page", "prev", "← 上一页", false, s.page === 0 ? "disabled" : "")}${btn("page", "next", "下一页 →", false, s.page >= pages - 1 ? "disabled" : "")}</div></div><div class="gm-open-model">${
      selected
        ? `<span class="eyebrow">SOURCE RECORD / 2026-10-17</span><h4>${esc(selected.model_id)}</h4><p>${esc(selected.country)} · ${esc(selected.story_org)} · ${esc(selected.org_type)}</p>${stats(
            [
              [selected.strict_completeness_level, "源站完整性等级"],
              [selected.openness_level, "源站开放性等级"],
            ],
          )}${selected.license_evidence_differs_from_grade ? '<p class="gm-evidence-note">许可判级依据待复核：源站最终等级与该条许可证据值不一致，保留原值。</p>' : ""}<p>${link(selected.official_url, "模型主页")}</p>${selected.evidence.map((e) => `<div class="gm-evidence-row"><b>${esc({ L2_training: "训练信息", L3_train_code: "训练代码", L3_train_data: "训练数据", model_license_grade: "许可等级依据" }[e.field] || e.field)}</b>${e.urls.map((u, i) => link(u, "源评估证据 " + (i + 1))).join(" · ")}</div>`).join("")}<p class="gm-note">证据入口来自源站，本报告未逐条重新评估。许可字段的 complete 不等于许可文件已公开。</p>`
        : note(
            "选择左侧模型，在此查看源站等级与证据入口。原报告870个模型未取得身份清单，因此仅补充快照支持此浏览。",
          )
    }</div>`;
  }
  function openness(p, s) {
    const rows = opennessRows(s),
      n = sum(rows, "models"),
      bgs = [palette[0], palette[2], palette[1], C.unknown];
    let body =
      txt(670, 32, "材料完整性 →", 19, C.muted, "middle") +
      txt(35, 65, "开放条件 ↑", 19, C.muted);
    const positions = {
      "低完整-高开放": [115, 80],
      "高完整-高开放": [650, 80],
      "低完整-低开放": [115, 310],
      "高完整-低开放": [650, 310],
    };
    rows.forEach((r) => {
      let [x, y] = positions[r.quadrant],
        idx = quadrants.indexOf(r.quadrant),
        selected = s.quadrant === r.quadrant;
      body += action(
        "quadrant",
        r.quadrant,
        r.quadrant + "，" + r.models + "个模型",
        box(
          x,
          y,
          495,
          195,
          selected ? C.raised : C.bg,
          selected ? C.brand : C.line,
          12,
        ) +
          box(x + 24, y + 24, 7, 28, bgs[idx], "none", 3) +
          txt(x + 48, y + 46, r.quadrant.replace("-", " · "), 23) +
          txt(
            x + 26,
            y + 111,
            fmt(r.models),
            44,
            bgs[idx],
            "start",
            'font-weight="650"',
          ) +
          txt(
            x + 470,
            y + 111,
            fmt((r.models / n) * 100, 2) + "%",
            30,
            C.ink,
            "end",
          ) +
          txt(
            x + 26,
            y + 158,
            r.quadrant.startsWith("高") ? "L3—L5" : "L1—L2",
            17,
            C.muted,
          ) +
          txt(
            x + 470,
            y + 158,
            r.quadrant.endsWith("高开放") ? "O2—O4" : "O1",
            17,
            C.muted,
            "end",
          ),
      );
    });
    const controls =
      seg(
        "sample",
        [
          ["report", "报告样本 · 870"],
          ["current", "补充快照 · 884"],
        ],
        s.sample,
      ) + btn("clear", "", "清空分类", false, s.quadrant ? "" : "disabled");
    const browser =
      s.sample === "current"
        ? `<div class="gm-browser"><div class="gm-browser-search"><label for="gm-open-search">在补充样本中搜索</label><input id="gm-open-search" type="search" data-gm-search="openness" placeholder="模型、发布账户或国家（源站英文）" value="${esc(s.query)}"></div><div class="gm-open-browser-results">${openBrowser(p, s)}</div></div>`
        : "";
    const rowsExport =
      s.sample === "current"
        ? openMatches(s).map((m) => ({
            模型: m.model_id,
            国家: m.country,
            主体: m.story_org,
            完整性: m.strict_completeness_level,
            开放性: m.openness_level,
            分类: m.strict_quadrant,
            许可判级待核: m.license_evidence_differs_from_grade,
            日期: "2026-10-17",
          }))
        : rows;
    set(
      p,
      controls,
      svg(body, 1200, 550, "材料完整性与开放条件四分类") +
        note(
          `当前：<b>${s.sample === "report" ? "870 个原评估模型 · 2026-09-14 提取" : "884 个补充记录 · 2026-10-17 提取"}</b>。${s.quadrant ? "所选 " + s.quadrant + "。" : ""}等面积卡片用于分类阅读，面积不代表数量。`,
        ) +
        browser,
      note(
        "高完整= L3—L5，高开放= O2—O4，均沿用源评估分组。“高开放”不自动表示符合 OSI 定义或 DPGA 认可。两份快照的个体对应未核验，不解释为同群体的进步。",
      ),
      rowsExport,
      source(
        ["quadrants"],
        "原报告870模型保留原汇总。补充884模型为2026-10-17当前API记录，不替换原集合。完整判级算法和O1—O4权利判断表未取得，本报告不重算认证。当前补充实际仅有O1/O2/O3，O4为0。",
      ) +
        `<p>${link(asset("openness-current.json"), "补充884模型记录")} · ${link(asset("openness-evidence-884.json"), "源评估逐项证据")} · ${link(asset("openness-method.json"), "L1—L5材料清单与方法限制")}</p>`,
    );
  }
  function openGroups(p, s) {
    const region = s.group === "region",
      rows = region ? D.openRegions : D.openPublishers,
      denom = (r) => (region ? r.n : r.models);
    let cats = region ? quadrants : [quadrants[0], "其余高开放", "低开放"],
      cs = region
        ? [palette[0], palette[2], palette[1], C.unknown]
        : [palette[0], palette[2], C.unknown];
    const vals = (r) =>
        region
          ? quadrants.map((k) => r[k])
          : [
              r.double_high,
              r.high_open - r.double_high,
              r.models - r.high_open,
            ],
      max = s.mode === "share" ? 100 : Math.max(...rows.map(denom));
    let b = txt(
      35,
      35,
      region ? "地区结构 · 原报告 870 模型" : "发布主体结构 · 原报告 870 模型",
      23,
    );
    rows.forEach((r, i) => {
      let y = 85 + i * 78,
        name = region ? r.group : r.publisher_type,
        n = denom(r),
        v = vals(r),
        x = 220;
      b +=
        txt(35, y + 22, name, 20) +
        txt(
          35,
          y + 45,
          `n = ${n}${!region ? " · " + r.organizations + " 个主体" : ""}`,
          15,
          C.muted,
        );
      v.forEach((n, j) => {
        const w = ((s.mode === "share" ? (n / denom(r)) * 100 : n) / max) * 860;
        b += box(x, y, Math.max(0, w), 36, cs[j], "none", 0);
        if (w > 55)
          b += txt(
            x + w / 2,
            y + 24,
            s.mode === "share" ? fmt((n / denom(r)) * 100, 1) + "%" : n,
            15,
            C.bg,
            "middle",
            'font-weight="650"',
          );
        x += w;
      });
      b += txt(
        1150,
        y + 24,
        fmt((v[0] / n) * 100, 1) + "%",
        18,
        palette[0],
        "end",
      );
    });
    b += txt(1150, 60, "双高比例", 16, C.muted, "end");
    const h = region ? 520 : 450;
    set(
      p,
      seg(
        "group",
        [
          ["region", "地区"],
          ["publisher", "发布主体"],
        ],
        s.group,
      ) +
        seg(
          "mode",
          [
            ["share", "组内比例"],
            ["count", "模型数量"],
          ],
          s.mode,
        ),
      svg(b, 1200, h, "开放评估样本按地区或发布主体的分类结构") +
        legend(cats.map((r, i) => [r, cs[i]])),
      note(
        region
          ? "每个地区使用本组模型数作分母；“未知归属”保留，不推断地域。原评估样本的比例不代表各国所有模型。"
          : "双高属于高开放的子集；图中拆分为“双高、其余高开放、低开放”三个互斥部分。主体数量与模型数量分别标注，不混作分母。",
      ),
      rows,
      source(
        region ? ["openRegions"] : ["openPublishers"],
        "2026-09-14提取的既有870模型评估，不是当日重新评估。各组样本量不同，缺少总体随机抽样基础，比例只用于该集合的结构观察。发布类型原表没有完整四象限，不能补造。",
      ),
    );
  }
  function dossiers(p, s) {
    const selected = D.cases.models.filter((m) =>
        s.selected.includes(m.model_id),
      ),
      fields = Object.entries(D.cases.field_labels).filter(
        ([k]) => s.field === "all" || k === s.field,
      );
    let table = `<div class="gm-dossier-scroll"><table class="gm-dossiers"><thead><tr><th scope="col">证据维度</th>${selected.map((m) => `<th scope="col"><span>${esc(m.publisher)}</span><h4>${esc(m.title)}</h4>${link(m.fixed_card_url, "固定版本模型卡")}</th>`).join("")}</tr></thead><tbody>${fields
      .map(
        ([key, label]) =>
          `<tr><th scope="row">${esc(label)}</th>${selected
            .map((m) => {
              const f = m.fields[key];
              return `<td><b class="gm-status gm-status-${f.status}">${esc(f.label)}</b><p>${esc(f.detail)}</p><div>${f.sources.map((url, i) => link(url, "依据 " + (i + 1))).join(" · ")}</div></td>`;
            })
            .join("")}</tr>`,
      )
      .join("")}</tbody></table></div>`;
    // A compact exportable summary accompanies the evidence-first HTML table.
    let b = txt(35, 35, "版本化开放档案 · 2026-10-17 补充核验", 23);
    selected.forEach((m, i) => {
      const x = 250 + (i * 900) / selected.length;
      b += txt(x + 20, 84, m.title, 18);
      fields.forEach(([key, label], j) => {
        const f = m.fields[key];
        if (i === 0) b += txt(35, 138 + j * 60, label, 18);
        b +=
          box(x, 110 + j * 60, 880 / selected.length, 44, C.raised, "none", 6) +
          txt(
            x + 14,
            138 + j * 60,
            f.status === "observed" ? "已观察 · " + f.label : "待核实",
            15,
            f.status === "observed" ? C.brand : C.gold,
          );
      });
    });
    set(
      p,
      chips(
        "case",
        D.cases.models.map((m) => [m.model_id, m.title]),
        s.selected,
        "选择 1—3 个版本",
      ) +
        seg(
          "field",
          [["all", "全部材料"], ...Object.entries(D.cases.field_labels)],
          s.field,
          "查看维度",
        ),
      table +
        `<div class="gm-dossier-svg" hidden>${svg(b, 1200, 155 + fields.length * 60, "模型开放证据简表")}</div>`,
      note(
        "案例为目的性选择，不代表870或884模型总体。已观察表示找到相关材料或声明；具体完整程度见说明。“待核实”不表示材料不存在。各项不合成分数，不作 OSI 或 DPGA 认证。",
      ),
      selected.flatMap((m) =>
        fields.map(([k, label]) => ({
          模型: m.model_id,
          版本: m.revision,
          核验日期: m.checked_at,
          材料: label,
          状态: m.fields[k].status,
          结论: m.fields[k].label,
          说明: m.fields[k].detail,
          来源: m.fields[k].sources.join(" | "),
        })),
      ),
      `<p>四个案例固定具体模型版本，权重、代码、数据说明、许可与维护入口逐项查阅一手来源；核验日期2026-10-17。正文表中的每项判断都有对应来源。仓库提交与官方材料记录：${link(asset("cases.json"), "完整版本档案 JSON")}。</p><p>${link("https://opensource.org/ai/open-source-ai-definition", "OSI OSAID 1.0")} · ${link("https://www.digitalpublicgoods.net/standard", "DPG Standard")}。研究分级、定义与正式认可分别适用。</p>`,
    );
  }
  const supply51 = window.createGOSM51(D, {asset,esc,fmt,compact,txt,line,box,action,svg,btn,seg,chips,note,link,set,source,colors:()=>({C,palette})});
  panels.forEach(p=>{if(supply51.defaults[p.dataset.gmChart])states.set(p,JSON.parse(JSON.stringify(supply51.defaults[p.dataset.gmChart])));});
  const influence52 = window.createGOSM52(D, {base:BASE,asset,esc,fmt,compact,txt,line,box,action,svg,btn,seg,note,link,set,source,draw:p=>draw(p),colors:()=>({C,palette})});
  panels.forEach(p=>{if(influence52.defaults[p.dataset.gmChart])states.set(p,JSON.parse(JSON.stringify(influence52.defaults[p.dataset.gmChart])));});
  const openness53 = window.createGOSM53(D, {asset,esc,fmt,compact,txt,line,box,action,svg,btn,seg,note,link,set,source,draw:p=>draw(p),state:p=>states.get(p),colors:()=>({C,palette})});
  panels.forEach(p=>{if(openness53.defaults[p.dataset.gmChart])states.set(p,JSON.parse(JSON.stringify(openness53.defaults[p.dataset.gmChart])));});
  const renderers = {
    framework,
    supply,
    world,
    release,
    cnus,
    derivation,
    network,
    flows,
    head,
    openness,
    "open-groups": openGroups,
    dossiers,
  };
  Object.assign(renderers, supply51.renderers, influence52.renderers, openness53.renderers);
  function draw(p) {
    renderers[p.dataset.gmChart](p, states.get(p));
    if (p.dataset.gmChart === "network")
      $("[data-gm-svg]", p).textContent =
        states.get(p).dimension === "3d" ? "2D SVG ↓" : "SVG ↓";
    p.dataset.gmReady = "true";
  }
  function selectAction(p, key, v) {
    const s = states.get(p),
      id = p.dataset.gmChart;
    if (supply51.handle(p,s,key,v) || influence52.handle(p,s,key,v) || openness53.handle(p,s,key,v)) {
      const preserveFocus=p.contains(document.activeElement);
      draw(p);
      if(openness53.own(p)&&key==="evidence")p.querySelector('[data-gm-action="closeEvidence"]')?.focus();
      else if(openness53.own(p)&&key==="closeEvidence")p.querySelector('[data-gm-action="evidence"][data-value="'+s.field+'"]')?.focus();
      else if(preserveFocus)Array.from(p.querySelectorAll('[data-gm-action]')).find(el=>el.dataset.gmAction===key&&el.dataset.value===String(v))?.focus();
      return;
    }
    if (key === "clear") {
      if (id === "world") s.countries = [];
      if (id === "flows") s.country = "";
      if (id === "openness") {
        s.quadrant = "";
        s.model = "";
        s.page = 0;
      }
    } else if (key === "country") {
      if (id === "world" && !byCode.has(v)) return;
      const arr = s.countries;
      if (arr.includes(v)) {
        if (id === "release" && arr.length === 1) return;
        s.countries = arr.filter((x) => x !== v);
      } else {
        if (id === "world" && arr.length >= 3) arr.shift();
        s.countries = [...arr, v];
      }
    } else if (key === "flow-country") s.country = s.country === v ? "" : v;
    else if (key === "node") {
      if (!models.has(v)) return;
      s.node = v;
      if (s.view === "lineage") {
        s.zoom = 1;
        s.panX = 0;
        s.panY = 0;
      }
    } else if (key === "zoom") {
      if (s.dimension === "3d" && p.gm3d) {
        p.gm3d.zoom(v === "in" ? 0.8 : 1.25);
        return;
      }
      s.zoom = clamp(s.zoom * (v === "in" ? 1.25 : 0.8), 0.4, 6);
    } else if (key === "reset") {
      s.zoom = 1;
      s.panX = 0;
      s.panY = 0;
      if (p.gm3d) {
        p.gm3d.reset();
        return;
      }
    } else if (key === "case") {
      if (s.selected.includes(v)) {
        if (s.selected.length === 1) return;
        s.selected = s.selected.filter((id) => id !== v);
      } else {
        if (s.selected.length >= 3) s.selected.shift();
        s.selected = [...s.selected, v];
      }
    } else if (key === "open-model") s.model = v;
    else if (key === "page") s.page += v === "next" ? 1 : -1;
    else if (key === "quadrant") {
      s.quadrant = s.quadrant === v ? "" : v;
      s.page = 0;
      s.model = "";
    } else {
      if (["k", "months", "hops", "limit"].includes(key)) s[key] = +v;
      else s[key] = v;
      if (key === "sample") {
        s.page = 0;
        s.quadrant = "";
        s.query = "";
        s.model = "";
      }
      if (key === "view") {
        s.orbit = null;
        s.zoom = 1;
        s.panX = s.panY = 0;
      }
    }
    draw(p);
  }
  function csvText(rows) {
    const keys = Object.keys(rows[0] || {}),
      cell = (v) => {
        let s = String(v ?? "");
        if (/^[=+@\t\r-]/.test(s) && !/^[-+]?(\d|\.\d)/.test(s)) s = "'" + s;
        return '"' + s.replace(/"/g, '""') + '"';
      };
    return (
      "\uFEFF" +
      [
        keys,
        ...rows.map((r) =>
          keys.map((k) =>
            typeof r[k] === "object" ? JSON.stringify(r[k]) : r[k],
          ),
        ),
      ]
        .map((r) => r.map(cell).join(","))
        .join("\r\n")
    );
  }
  function download(content, type, name) {
    const url = URL.createObjectURL(new Blob([content], { type })),
      a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.append(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function exportSvg(p) {
    if(openness53.own(p)){download(openness53.publication(p,states.get(p)),"image/svg+xml;charset=utf-8",`GOSM-${p.dataset.gmChart}-publication.svg`);return;}
    if(influence52.own(p)){download(influence52.publication(p,states.get(p)),"image/svg+xml;charset=utf-8",`GOSM-${p.dataset.gmChart}-publication.svg`);return;}
    const el = $(".gm-svg", p);
    if (!el) return;
    const clone = el.cloneNode(true),
      vb = clone.getAttribute("viewBox").split(" ").map(Number),
      h = vb[3],
      w = vb[2];
    clone.setAttribute("viewBox", `0 0 ${w} ${h + 108}`);
    clone.setAttribute("width", w);
    clone.setAttribute("height", h + 108);
    clone.removeAttribute("class");
    clone.querySelectorAll("foreignObject").forEach(n=>n.remove());
    const add = document.createElementNS("http://www.w3.org/2000/svg", "g");
    add.innerHTML =
      box(0, h, w, 108, C.paper, "none", 0) +
      txt(p.classList.contains("s51-panel") ? w/2 : 30, h + 30, $("h3", p).textContent, 18, C.ink, p.classList.contains("s51-panel") ? "middle" : "start") +
      txt(
        30,
        h + 56,
        "GOSD 2026 · " + D.version + " · 当前视角；详见图内口径与来源",
        14,
        C.muted,
      ) +
      txt(30, h + 82, `来源 / 范围：${exportStamp(p)}`, 13, C.muted);
    clone.append(add);
    download(
      new XMLSerializer().serializeToString(clone),
      "image/svg+xml;charset=utf-8",
      `GOSM-${p.dataset.gmChart}-${document.documentElement.dataset.theme}.svg`,
    );
  }
  function exportStamp(p) {
    const id = p.dataset.gmChart,
      s = states.get(p);
    if (supply51.own(p)) return supply51.stamp(p,s);
    if (influence52.own(p)) return influence52.stamp(p,s);
    if (openness53.own(p)) return openness53.stamp(p,s);
    if (id === "network")
      return "参考项目 / hub-stats · 2026-10-16 · 非随机声明关系样本";
    if (id === "openness")
      return (
        "OpenGauge · " +
        (s.sample === "report"
          ? "870模型原评估，2026-09-14提取"
          : "884补充记录，2026-10-17提取")
      );
    if (id === "dossiers")
      return (
        "官方模型卡与仓库 · 2026-10-17 · " +
        s.selected.length +
        "个独立补充案例"
      );
    if (id === "open-groups")
      return "OpenGauge · 870模型原评估 · 2026-09-14提取";
    if (id === "head")
      return "ModelRank原表 · " + s.months + "个月至2026-08 · Top " + s.k;
    if (id === "cnus")
      return "OpenGauge 2026-09-13 / ModelRank 2026-08 · 各自样本分母";
    if (id === "framework")
      return "版本示例框架 · 官方材料2026-10-17 / 关系样本2026-10-16";
    return "Hugging Face / OpenGauge · 2026-09-13可见样本 · 原报告底表";
  }
  const dialog = $("#gm-fullscreen"),
    body = $("#gm-fullscreen-body");
  let current = null,
    placeholder = null,
    returnFocus = null;
  function closeFull() {
    if (!current) return;
    const old = current;
    placeholder.replaceWith(old);
    placeholder = null;
    current = null;
    if (dialog.open) dialog.close();
    document.documentElement.classList.remove("gm-modal-open");
    returnFocus?.focus();
  }
  function openFull(p) {
    if (current === p) return;
    const originalFocus = document.activeElement;
    if (p.classList.contains("gm-compact-panel")) {
      if ($(".gm-source",p)) $(".gm-source",p).open=false; $(".gm-table",p).open=false;
    }
    if (current) {
      const old = current;
      placeholder.replaceWith(old);
    }
    placeholder = document.createElement("div");
    placeholder.className = "gm-placeholder";
    p.before(placeholder);
    body.replaceChildren(p);
    current = p;
    returnFocus = originalFocus;
    $(".gm-fullscreen-bar strong", dialog).textContent = $("h3", p).textContent;
    document.documentElement.classList.add("gm-modal-open");
    if (!dialog.open) dialog.showModal();
    $("[data-gm-close]", dialog).focus();
  }
  document.addEventListener("click", (e) => {
    const menu=document.querySelector('[data-s51-menu][open]');
    if(menu&&!menu.contains(e.target))menu.open=false;
    const el = e.target.closest("button,[data-gm-action]");
    if (!el) return;
    if (el.hasAttribute("data-gm-close")) {
      closeFull();
      return;
    }
    if (el.hasAttribute("data-gm-prev") || el.hasAttribute("data-gm-next")) {
      if (current)
        openFull(
          panels[
            (panels.indexOf(current) +
              (el.hasAttribute("data-gm-next") ? 1 : -1) +
              panels.length) %
              panels.length
          ],
        );
      return;
    }
    if (el.hasAttribute("data-gm-theme")) {
      $("#theme-toggle")?.click();
      return;
    }
    const p = el.closest("[data-gm-chart]");
    if (!p) return;
    const exportMenu=el.closest('[data-s51-menu]');
    if(exportMenu){exportMenu.open=false;exportMenu.querySelector('summary').focus();}
    if (el.hasAttribute("data-gm-action")) {
      selectAction(p, el.dataset.gmAction, el.dataset.value);
      return;
    }
    if (el.hasAttribute("data-gm-full")) {
      openFull(p);
      return;
    }
    if (el.hasAttribute("data-gm-table") && p.classList.contains("gm-compact-panel")) {
      const d = $(".gm-table", p);
      if ($(".gm-source", p)) $(".gm-source", p).open = false;
      d.open = !d.open;
      if (d.open) { fillTable(p); d.querySelector("summary").focus(); }
      return;
    }
    if (el.hasAttribute("data-gm-source")) {
      const d = $(".gm-source", p);
      d.open = !d.open;
      if (p.classList.contains("gm-compact-panel")) {
        $(".gm-table", p).open = false;
        if (d.open) d.querySelector("summary").focus();
      } else if (d.open) d.scrollIntoView({ block: "nearest", behavior: "smooth" });
      return;
    }
    if (el.hasAttribute("data-gm-csv"))
      download(
        csvText(p.gmRows || []),
        "text/csv;charset=utf-8",
        `GOSM-${p.dataset.gmChart}.csv`,
      );
    if (el.hasAttribute("data-gm-svg")) exportSvg(p);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const menu=document.querySelector('[data-s51-menu][open]');
      if(menu){e.preventDefault();e.stopPropagation();menu.open=false;menu.querySelector('summary').focus();return;}
      const overlay = document.querySelector(".gm-compact-panel .gm-source[open],.gm-compact-panel .gm-table[open]");
      if (overlay) {
        e.preventDefault(); e.stopPropagation(); overlay.open=false;
        const trigger=overlay.closest(".gm-compact-panel").querySelector(overlay.classList.contains("gm-source")?"[data-gm-source],[data-gm-action=standardDetails]":"[data-gm-table]");
        (trigger?.closest("[data-s51-menu]")?.querySelector("summary")||trigger)?.focus();
        return;
      }
    }
    if (
      (e.key === "Enter" || e.key === " ") &&
      e.target.matches("g[data-gm-action]")
    ) {
      e.preventDefault();
      e.target.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    }
  });
  document.addEventListener("keydown",e=>{if(e.key!=="Escape")return;const p=e.target.closest?.(".s53-panel");if(p&&states.get(p)?.detail){e.preventDefault();e.stopPropagation();states.get(p).detail=false;draw(p);p.querySelector('[data-gm-action="evidence"]')?.focus();}});
  document.addEventListener("input", (e) => {
    const p = e.target.closest("[data-gm-chart]");
    if (!p) return;
    const s = states.get(p),
      q = e.target.value;
    if(influence52.input(p,s,e) || openness53.input(p,s,e))return;
    if(supply51.input(p,s,e)){const type=e.target.dataset.s51Search; const cursor=e.target.selectionStart;draw(p);const next=p.querySelector(`[data-s51-search="${type}"]`);next?.focus();try{next?.setSelectionRange(cursor,cursor);}catch{}return;}
    if (e.target.dataset.gmSearch === "network") {
      $("#gm-model-results", p).innerHTML = q.trim()
        ? D.network.nodes
            .filter((n) => n.id.toLowerCase().includes(q.toLowerCase()))
            .sort((a, b) => b.downstreamCount - a.downstreamCount)
            .slice(0, 8)
            .map((n) => btn("node", n.id, n.id))
            .join("") || "<p>没有匹配模型。</p>"
        : "";
    }
    if (e.target.dataset.gmSearch === "openness") {
      s.query = q;
      s.page = 0;
      $(".gm-open-browser-results", p).innerHTML = openBrowser(p, s);
      p.gmRows = openMatches(s).map((m) => ({
        模型: m.model_id,
        国家: m.country,
        完整性: m.strict_completeness_level,
        开放性: m.openness_level,
        分类: m.strict_quadrant,
        快照: "2026-10-17",
      }));
      p.gmTableDirty = true;
      if ($(".gm-table", p).open) fillTable(p);
    }
    if (e.target.dataset.gmRange) {
      const rows =
        e.target.dataset.gmRange === "head"
          ? D.head.filter((r) => r.k === s.k).slice(-s.months)
          : D.monthly.slice(-s.months);
      s.month = rows[+q].month;
      const focus = e.target.dataset.gmRange;
      draw(p);
      $(`[data-gm-range="${focus}"]`, p).focus();
    }
  });
  document.addEventListener("change",e=>{const p=e.target.closest("[data-gm-chart]");if(!p)return;if(supply51.change(p,states.get(p),e)){const k=e.target.dataset.s51Select;draw(p);p.querySelector(k?`[data-s51-select="${k}"]`:"[data-s51-metric-select]")?.focus();return;}if(influence52.change(p,states.get(p),e) || openness53.change(p,states.get(p),e))draw(p);});
  panels.forEach((p) =>
    $(".gm-table", p).addEventListener("toggle", () => {
      if ($(".gm-table", p).open && p.gmTableDirty) fillTable(p);
    }),
  );
  dialog.addEventListener("cancel", (e) => {
    e.preventDefault();
    closeFull();
  });
  dialog.addEventListener("close", () => {
    if (current) closeFull();
  });
  function redrawTheme() {
    colors();
    panels.forEach(draw);
  }
  colors();
  panels.forEach(draw);
  window.addEventListener("gosdthemechange", redrawTheme);
  // The shared toggle may change the attribute without dispatching a custom event.
  let lastTheme = document.documentElement.dataset.theme;
  new MutationObserver(() => {
    const t = document.documentElement.dataset.theme;
    if (t !== lastTheme) {
      lastTheme = t;
      redrawTheme();
    }
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
  window.GOSM = {
    version: D.version,
    data: D,
    panels,
    states,
    draw,
    networkSlice,
    influence52,
    openness53,
    csvText,
    exportStamp,
  };
})();
