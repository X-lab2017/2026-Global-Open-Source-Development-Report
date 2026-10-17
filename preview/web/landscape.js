/* 4.1: pure calculations are shared with the regression checks below the UI. */
(function (root) {
  "use strict";
  function model(D) {
    const P = D.projects,
      keys = Object.keys(D.sections),
      num = (x) => x !== null && Number.isFinite(x),
      sum = (a) => a.reduce((s, x) => s + x, 0);
    const projects = (scope) =>
      P.filter((p) => scope === "all" || p.layer === scope);
    const sections = (scope) =>
      keys.filter((k) => projects(scope).some((p) => p.section === k));
    const value = (p, m) => p.trend[m];
    const status = (p, m) =>
      num(value(p, m))
        ? "有观测"
        : p.created.slice(0, 7) > D.months[m]
          ? "尚未创建"
          : "无观测";
    function rank(rows) {
      rows.sort(
        (a, b) =>
          (b.value ?? -Infinity) - (a.value ?? -Infinity) ||
          a.key.localeCompare(b.key),
      );
      let prev = null,
        r = 0;
      rows.forEach((x, i) => {
        if (x.value === null) {
          x.rank = null;
          return;
        }
        if (x.value !== prev) r = i + 1;
        x.rank = r;
        prev = x.value;
      });
      return rows;
    }
    function rawCategories(scope, m) {
      return rank(
        sections(scope).map((key) => {
          let pp = projects(scope).filter((p) => p.section === key),
            vv = pp.map((p) => value(p, m)).filter(num);
          return {
            key,
            name: D.sections[key].name,
            count: pp.length,
            coverage: vv.length,
            value: vv.length ? sum(vv) : null,
          };
        }),
      );
    }
    function categories(scope, m) {
      let rows = rawCategories(scope, m),
        total = sum(rows.map((r) => r.value || 0)),
        prev = m > 0 ? rawCategories(scope, m - 1) : [];
      return rows.map((r) => {
        let pp = projects(scope).filter((p) => p.section === r.key),
          both =
            m > 0
              ? pp.filter((p) => num(value(p, m)) && num(value(p, m - 1)))
              : [],
          a = sum(both.map((p) => value(p, m - 1))),
          b = sum(both.map((p) => value(p, m))),
          old = prev.find((p) => p.key === r.key);
        return {
          ...r,
          share: total && r.value !== null ? r.value / total : null,
          change: a ? (b - a) / a : null,
          common: both.length,
          rankChange: r.rank && old?.rank ? old.rank - r.rank : null,
        };
      });
    }
    function projectRows(scope, section, m) {
      let pp = projects(scope).filter((p) => p.section === section),
        total = sum(pp.map((p) => value(p, m)).filter(num));
      return rank(
        pp.map((p) => ({
          key: p.id,
          name: p.name,
          repo: p.repo,
          value: value(p, m),
          state: status(p, m),
          share: num(value(p, m)) && total ? value(p, m) / total : null,
          change:
            m > 0 &&
            num(value(p, m)) &&
            num(value(p, m - 1)) &&
            value(p, m - 1) !== 0
              ? (value(p, m) - value(p, m - 1)) / value(p, m - 1)
              : null,
        })),
      );
    }
    function concentration(scope, m) {
      return categories(scope, m)
        .map((r) => {
          let pp = projectRows(scope, r.key, m).filter((p) => p.value !== null);
          return {
            ...r,
            openrank: r.value,
            rank: null,
            value: r.value
              ? sum(pp.slice(0, 3).map((p) => p.value)) / r.value
              : null,
          };
        })
        .sort((a, b) => (b.value ?? -1) - (a.value ?? -1));
    }
    function shift(scope, start, end) {
      let pp = projects(scope).filter((p) =>
          p.trend.slice(start, end + 1).every(num),
        ),
        a = sum(pp.map((p) => value(p, start))),
        b = sum(pp.map((p) => value(p, end)));
      return sections(scope)
        .map((key) => {
          let group = pp.filter((p) => p.section === key),
            av = sum(group.map((p) => value(p, start))),
            bv = sum(group.map((p) => value(p, end)));
          return {
            key,
            name: D.sections[key].name,
            count: group.length,
            before: a ? av / a : null,
            after: b ? bv / b : null,
            value: a && b ? bv / b - av / a : null,
            cohort: pp.length,
          };
        })
        .sort((x, y) => (y.value ?? -Infinity) - (x.value ?? -Infinity));
    }
    const countryCache = new Map();
    function country(scope, section, period, m) {
      const cacheKey = JSON.stringify([scope, section, period, m]);
      if (countryCache.has(cacheKey)) return countryCache.get(cacheKey);
      let ss = sections(scope),
        rr = D.simulation.filter(
          (r) =>
            ss.includes(r.section) &&
            (section === "all" || r.section === section) &&
            (period === "month"
              ? r.month === m
              : r.month <= m &&
                r.month >=
                  Math.max(
                    0,
                    m - (period === "rolling" ? 12 : Number(period)) + 1,
                  )),
        ),
        rows = D.countries.map((c) => {
          let subset = rr.filter((r) => r.country === c.code),
            actors = new Set(subset.flatMap((r) => r.actors));
          return {
            ...c,
            key: c.code,
            value: sum(subset.map((r) => r.value)),
            developers: actors.size,
          };
        }),
        total = sum(rows.map((r) => r.value));
      const result = rank(
        rows.map((r) => ({ ...r, share: total ? r.value / total : 0 })),
      );
      countryCache.set(cacheKey, result);
      return result;
    }
    function countryCategories(scope, code, period, m) {
      let rows = sections(scope).map((key) => {
          let r = country(scope, key, period, m).find((c) => c.code === code);
          return {
            key,
            name: D.sections[key].name,
            value: r.value,
            categoryShare: r.share,
            developers: r.developers,
          };
        }),
        total = sum(rows.map((r) => r.value));
      return rows
        .map((r) => ({ ...r, share: total ? r.value / total : 0 }))
        .sort((a, b) => b.value - a.value);
    }
    return {
      projects,
      sections,
      value,
      status,
      categories,
      projectRows,
      concentration,
      shift,
      country,
      countryCategories,
      rank,
      num,
    };
  }
  root.LandscapeModel = model;
  if (typeof module !== "undefined") module.exports = model;
})(typeof globalThis !== "undefined" ? globalThis : this);

(function () {
  "use strict";
  if (typeof document === "undefined") return;
  const dataNode = document.getElementById("landscape-data");
  if (!dataNode) return;
  const D = JSON.parse(dataNode.textContent);
  if (D.version !== "4.1-v3") return;
  const M = globalThis.LandscapeModel(D),
    P = D.projects,
    LAST = D.months.length - 1,
    $ = (id) => document.getElementById(id);
  const state = { month: LAST };
  const chartData = {},
    pages = {};
  const configs = {
    "al-category-rank": { scope: "all", month: LAST, focus: null },
    "al-category-heat": {
      scope: "Agent Infra",
      window: 12,
      metric: "rank",
      focus: null,
    },
    "al-category-trend": {
      categories: ["Personal AI assistants", "Agentic coding"],
      window: 12,
      metric: "rank",
    },
    "al-project-rank": {
      section: "Personal AI assistants",
      window: 12,
      metric: "rank",
      month: LAST,
      picks: [],
      page: 0,
    },
    "al-country-rank": {
      scope: "all",
      section: "all",
      window: 12,
      country: null,
    },
    "al-country-detail": {
      scope: "all",
      window: 12,
      country: "US",
      metric: "share",
    },
    "al-country-stack": {
      scope: "Agent Infra",
      window: 12,
      countries: ["US", "CN", "DE"],
      mode: "compare",
    },
    "al-concentration": {
      scope: "Agent Infra",
      month: LAST,
      section: "Personal AI assistants",
    },
    "al-shift": {
      scope: "Agent Infra",
      window: 12,
      section: "Personal AI assistants",
    },
    "al-specialization": {
      scope: "Agent Infra",
      window: 12,
      countries: ["US", "CN", "DE"],
    },
    "al-country-trend": {
      scope: "all",
      section: "all",
      window: 12,
      countries: ["US", "CN", "GB"],
    },
  };
  const palette = Array.from({ length: 8 }, (_, i) => `var(--gv-s${i})`);
  const countryColor = (code) => {
    const index = { US: 0, CN: 5, DE: 3, IN: 1, GB: 6, JP: 4, CA: 2, OTHER: 7 }[
      code
    ];
    return index === undefined ? "var(--gv-muted)" : palette[index];
  };
  const E = (s) =>
    String(s ?? "").replace(
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
  const F = (v, d = 2) =>
    v === null || v === undefined
      ? "—"
      : Number(v).toLocaleString("zh-CN", {
          maximumFractionDigits: d,
          minimumFractionDigits: d,
        });
  const pct = (v) =>
    v === null || v === undefined ? "—" : F(v * 100, 1) + "%";
  const signed = (v, unit = "") => {
    if (v === null) return "—";
    const rounded = Math.abs(v) < 0.05 ? 0 : v;
    return (rounded > 0 ? "+" : "") + F(rounded, 1) + unit;
  };
  const scopeName = (s) => (s === "all" ? "整个领域" : s);
  const catName = (k) => D.sections[k]?.name || "全部类别";
  const start = (c) => Math.max(0, LAST - c.window + 1);
  const period = (c) =>
    `${D.months[start(c)]}—${D.months[LAST]} · ${c.window} 个月`;
  const countryScope = (c) =>
    c.section && c.section !== "all" ? catName(c.section) : scopeName(c.scope);
  const cc = (code) => ({
    ...D.countries.find((c) => c.code === code),
    color: countryColor(code),
  });
  const text = (x, y, s, attrs = "") =>
    `<text x="${x}" y="${y}" ${attrs}>${E(s)}</text>`;
  const svg = (w, h, b, label) =>
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" role="group" aria-label="${E(label)}"><rect width="${w}" height="${h}" fill="var(--gv-surface)"/>${b}</svg>`;
  const mark = (action, value, label, b, selected = false) =>
    `<g role="button" tabindex="0" data-action="${action}" data-value="${E(value)}" aria-pressed="${selected}" aria-label="${E(label)}"><title>${E(label)}</title>${b}</g>`;
  function contrastInk(hex) {
    hex = hex.replace(/var\((--[\w-]+)\)/g, (_, key) =>
      getComputedStyle(document.querySelector(".al-chapter"))
        .getPropertyValue(key)
        .trim(),
    );
    let rgb = hex
      .slice(1)
      .match(/../g)
      .map((x) => parseInt(x, 16) / 255)
      .map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2] > 0.179
      ? "#091b29"
      : "#fff";
  }
  function optionSelect(id, field, label, options, value) {
    return `<label>${label}<select data-field="${field}" id="${id}-${field}">${options.map(([v, t]) => `<option value="${E(v)}" ${String(v) === String(value) ? "selected" : ""}>${E(t)}</option>`).join("")}</select></label>`;
  }
  function segment(field, options, value, label) {
    return `<div class="al-segment" role="group" aria-label="${label}">${options.map(([v, t]) => `<button type="button" data-action="${field}" data-value="${E(v)}" aria-pressed="${String(v) === String(value)}">${E(t)}</button>`).join("")}</div>`;
  }
  const windowControls = (c) =>
    segment(
      "window",
      [
        [6, "6 个月"],
        [12, "12 个月"],
        [18, "18 个月"],
      ],
      c.window,
      "时间窗口",
    );
  const scopeControls = (c, all = true) =>
    segment(
      "scope",
      [
        ...(all ? [["all", "整个领域"]] : []),
        ["Agent Infra", "Agent Infra"],
        ["Model Infra", "Model Infra"],
      ],
      c.scope,
      "观测范围",
    );
  const metricControls = (c) =>
    segment(
      "metric",
      [
        ["rank", "位次"],
        ["value", "OpenRank"],
        ["share", "份额"],
      ],
      c.metric,
      "比较指标",
    );
  function familyPicker(selected, multi = false) {
    return `<div class="al-family-picker" aria-label="${multi ? "比较子类别，最多三项" : "选择子类别"}">${[
      "Agent Infra",
      "Model Infra",
    ]
      .map(
        (layer) =>
          `<div class="al-family-group" role="group" aria-label="${layer}"><strong>${layer}</strong><div>${M.sections(
            layer,
          )
            .map(
              (k) =>
                `<button type="button" data-action="${multi ? "compare-category" : "project-category"}" data-value="${E(k)}" aria-pressed="${selected.includes(k)}" style="--al-choice-color:${multi ? palette[Math.max(0, selected.indexOf(k))] : "var(--gv-brand)"}">${E(catName(k))}</button>`,
            )
            .join("")}</div></div>`,
      )
      .join("")}</div>`;
  }
  function countryPicker(c, max = 9) {
    return `<fieldset class="al-country-picker"><legend>关注国家${max < 9 ? " · 最多 " + max + " 个" : ""}</legend><div>${D.countries.map((x) => `<label style="--al-choice-color:${countryColor(x.code)}"><input type="checkbox" data-country-check="${x.code}" ${c.countries.includes(x.code) ? "checked" : ""}>${x.name}</label>`).join("")}<button type="button" data-action="countries-reset">${max < 9 ? "默认三个" : "恢复默认"}</button>${max === 9 ? '<button type="button" data-action="countries-all">全部</button><button type="button" data-action="countries-none">清空</button>' : ""}</div></fieldset>`;
  }
  function categoryScopeSelect(id, c) {
    return optionSelect(
      id,
      "section",
      "子类别",
      [["all", "全部类别"], ...M.sections(c.scope).map((k) => [k, catName(k)])],
      c.section,
    );
  }
  function controls(id, html) {
    let panel = $(id),
      host = panel.querySelector(".al-local-controls");
    if (!host) {
      host = document.createElement("div");
      host.className = "al-local-controls";
      panel.querySelector(".al-view").before(host);
    }
    host.innerHTML = html;
    bindPanel(panel);
  }
  function bindPanel(panel) {
    panel.querySelectorAll("[data-action]").forEach((n) => {
      n.onclick = () => act(panel.id, n.dataset.action, n.dataset.value, n);
      if (n.getAttribute("role") === "button")
        n.onkeydown = (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            n.onclick();
          }
        };
    });
    panel
      .querySelectorAll("[data-field]")
      .forEach(
        (n) => (n.onchange = () => act(panel.id, n.dataset.field, n.value, n)),
      );
    panel
      .querySelectorAll("[data-country-check]")
      .forEach(
        (n) =>
          (n.onchange = () =>
            act(panel.id, "country-check", n.dataset.countryCheck, n)),
      );
    panel.querySelectorAll("[data-project]").forEach(
      (n) =>
        (n.onclick = (e) => {
          e.preventDefault();
          projectDialog(n.dataset.project, state.month);
        }),
    );
  }
  function feedback(id, message) {
    $(id).querySelector(".al-readout").textContent = message;
  }
  function act(id, action, value, trigger) {
    const c = configs[id];
    if (!c) return;
    if (action === "open-project") {
      projectDialog(value, c.month ?? LAST);
      return;
    }
    if (action === "compare-category") {
      const list = c.categories;
      if (list.includes(value)) {
        if (list.length === 1) {
          feedback(id, "至少保留一个子类别。");
          return;
        }
        list.splice(list.indexOf(value), 1);
      } else {
        if (list.length >= 3) {
          feedback(id, "最多比较 3 个子类别，请先取消一个已选项。");
          return;
        }
        list.push(value);
        configs["al-project-rank"].section = value;
        resetProjects();
        renderProject();
      }
    } else if (action === "project-category") {
      c.section = value;
      c.page = 0;
      resetProjects();
      const other = configs["al-category-trend"];
      if (!other.categories.includes(value))
        other.categories = [...other.categories.slice(-2), value];
      renderCompare();
    } else if (action === "country-check") {
      const max = id === "al-specialization" ? 3 : 9;
      if (trigger.checked) {
        if (c.countries.length >= max) {
          trigger.checked = false;
          feedback(id, `最多关注 ${max} 个国家，请先取消一个。`);
          return;
        }
        c.countries.push(value);
      } else c.countries = c.countries.filter((x) => x !== value);
    } else if (action === "countries-reset") {
      c.countries = ["US", "CN", id === "al-country-trend" ? "GB" : "DE"];
    } else if (action === "countries-all")
      c.countries = D.countries.map((x) => x.code);
    else if (action === "countries-none") c.countries = [];
    else if (action === "pick-project") {
      if (c.picks.includes(value)) c.picks = c.picks.filter((x) => x !== value);
      else {
        if (c.picks.length >= 3) {
          feedback(id, "最多比较 3 个项目，请先取消一个已选项目。");
          return;
        }
        c.picks.push(value);
      }
    } else if (action === "page") {
      c.page += Number(value);
    } else if (action === "focus") {
      c.focus = c.focus === value ? null : value;
    } else if (action === "category-focus") {
      c.section = value;
    } else if (action === "country") {
      c.country =
        id === "al-country-rank" && c.country === value ? null : value;
    } else if (action === "clear-country") c.country = null;
    else if (action === "window") {
      c.window = Number(value);
      if (id === "al-project-rank") {
        c.month = Math.max(start(c), c.month);
        c.page = 0;
      }
    } else if (action === "month" || action === "project-month") {
      c.month = Number(value);
      if (c.page !== undefined) c.page = 0;
    } else if (action === "scope") {
      c.scope = value;
      if (
        c.section &&
        c.section !== "all" &&
        !M.sections(c.scope).includes(c.section)
      )
        c.section =
          id === "al-concentration" || id === "al-shift"
            ? M.sections(c.scope)[0]
            : "all";
      if (c.focus && !M.sections(c.scope).includes(c.focus)) c.focus = null;
    } else c[action] = value;
    render(id);
    const sel = trigger.dataset.action
      ? `[data-action="${trigger.dataset.action}"][data-value="${E(trigger.dataset.value || "")}"]`
      : trigger.id
        ? "#" + trigger.id
        : null;
    if (sel) {
      try {
        $(id).querySelector(sel)?.focus({ preventScroll: true });
      } catch {}
    }
  }
  function setChart(
    id,
    markup,
    rows,
    readout,
    sim = false,
    scope = "整个领域",
    time = D.months[LAST],
    attention = "",
  ) {
    const el = $(id);
    el.querySelector(".al-view").innerHTML = markup;
    el.querySelector(".al-readout").textContent = readout;
    chartData[id] = { rows, sim, scope, period: time, attention };
    pages[id] = Math.min(
      pages[id] || 0,
      Math.max(0, Math.ceil(rows.length / 8) - 1),
    );
    renderTable(id);
    bindPanel(el);
  }
  function renderTable(id, print = false) {
    let host = $(id).querySelector(".al-data-body"),
      rows = chartData[id].rows,
      keys = rows.length ? Object.keys(rows[0]) : [],
      page = pages[id] || 0,
      first = print ? 0 : page * 8,
      last = print ? rows.length : Math.min(first + 8, rows.length);
    host.innerHTML = rows.length
      ? `<div class="al-table-wrap"><table><thead><tr>${keys.map((k) => `<th scope="col">${E(k)}</th>`).join("")}</tr></thead><tbody>${rows
          .slice(first, last)
          .map(
            (r) =>
              `<tr>${keys.map((k) => `<td>${E(r[k] === null ? "—" : typeof r[k] === "number" ? F(r[k], Number.isInteger(r[k]) ? 0 : 2) : r[k])}</td>`).join("")}</tr>`,
          )
          .join(
            "",
          )}</tbody></table></div><div class="al-pager"><button type="button" data-page="-1" ${first === 0 ? "disabled" : ""}>上一页</button><span>${first + 1}—${last} / ${rows.length} 行</span><button type="button" data-page="1" ${last === rows.length ? "disabled" : ""}>下一页</button></div>`
      : "<p>当前没有记录。</p>";
    host.querySelectorAll("[data-page]").forEach(
      (b) =>
        (b.onclick = () => {
          pages[id] += Number(b.dataset.page);
          renderTable(id);
        }),
    );
  }
  function trajectory(
    series,
    {
      x = 0,
      y = 0,
      width = 1280,
      height = 520,
      metric = "value",
      window = 12,
      rankMax = 25,
      focus = null,
      cursor = null,
      pointAction = null,
      seriesAction = null,
    } = {},
  ) {
    const first = LAST - window + 1,
      L = x + 70,
      R = x + width - 250,
      T = y + 40,
      B = y + height - 68,
      all = series
        .flatMap((s) => s.values.slice(first, LAST + 1))
        .filter(M.num),
      max =
        metric === "rank"
          ? rankMax
          : Math.max(...all, metric === "share" ? 0.01 : 1) * 1.1;
    const px = (i) => L + ((R - L) * (i - first)) / Math.max(window - 1, 1),
      py = (v) =>
        metric === "rank"
          ? T + ((B - T) * (v - 1)) / Math.max(max - 1, 1)
          : B - ((B - T) * v) / max;
    let b = "";
    const ticks =
      metric === "rank"
        ? [
            1,
            ...Array.from(
              { length: Math.floor(max / 5) },
              (_, i) => (i + 1) * 5,
            ),
          ].filter((v, i, a) => v <= max && a.indexOf(v) === i)
        : [0, 1, 2, 3, 4].map((v) => (max * v) / 4);
    if (metric === "rank" && !ticks.includes(max)) ticks.push(max);
    ticks.forEach((v) => {
      let yy = py(v);
      b +=
        `<path d="M${L} ${yy}H${R}" stroke="var(--gv-line)"/>` +
        text(
          L - 12,
          yy + 5,
          metric === "share" ? pct(v) : F(v, 0),
          'text-anchor="end" font-size="15"',
        );
    });
    for (let i = first; i <= LAST; i++) {
      if (window === 18 && (i - first) % 2 !== 0 && i !== LAST) continue;
      b += text(
        px(i),
        B + 29,
        D.months[i].slice(2),
        'font-size="14" text-anchor="middle"',
      );
    }
    if (cursor !== null && cursor >= first)
      b +=
        `<path d="M${px(cursor)} ${T - 10}V${B}" stroke="var(--gv-goldDisplay)" stroke-width="2" stroke-dasharray="5 5"/>` +
        text(
          px(cursor),
          T - 20,
          D.months[cursor],
          'font-size="13" text-anchor="middle" fill="var(--gv-muted)"',
        );
    const labels = [];
    for (const [j, s] of series.entries()) {
      const ink = s.color || palette[j % palette.length],
        dim = focus && s.key !== focus,
        opacity = dim ? 0.17 : 1;
      let path = "",
        connected = false,
        body = "";
      for (let i = first; i <= LAST; i++) {
        const v = s.values[i];
        if (!M.num(v)) {
          connected = false;
          continue;
        }
        const xx = px(i),
          yy = py(v);
        path += (connected ? "L" : "M") + xx.toFixed(1) + "," + yy.toFixed(1);
        connected = true;
        const title = `${s.name} · ${D.months[i]} · ${metric === "rank" ? "第 " + v + " 位" : metric === "share" ? pct(v) : F(v)}${s.coverage ? " · 覆盖 " + s.coverage[i] : ""}`;
        body += pointAction
          ? mark(
              pointAction,
              String(i),
              title,
              `<circle cx="${xx}" cy="${yy}" r="5" fill="${ink}"/>`,
            )
          : `<circle cx="${xx}" cy="${yy}" r="${series.length > 5 ? 3.5 : 4.5}" fill="${ink}" tabindex="0"><title>${E(title)}</title></circle>`;
      }
      body =
        `<path d="${path}" fill="none" stroke="${ink}" stroke-width="${dim ? 1.7 : 3}"/>` +
        body;
      b += `<g opacity="${opacity}" data-series="${E(s.key || s.name)}">${seriesAction ? mark(seriesAction, s.key, s.name, body, focus === s.key) : body}</g>`;
      const end = s.values[LAST];
      if (M.num(end))
        labels.push({
          key: s.key,
          name: s.name,
          value: end,
          actual: py(end),
          target: py(end),
          ink,
          opacity,
        });
    }
    labels.sort((a, b) => a.actual - b.actual);
    const gap = series.length > 5 ? 25 : 34;
    labels.forEach((l, i) => {
      l.target = Math.max(
        l.target,
        T + (i ? 0 : 0),
        i ? labels[i - 1].target + gap : T,
      );
    });
    if (labels.length && labels.at(-1).target > B) {
      labels.at(-1).target = B;
      for (let i = labels.length - 2; i >= 0; i--)
        labels[i].target = Math.min(
          labels[i].target,
          labels[i + 1].target - gap,
        );
    }
    labels.forEach((l) => {
      const val =
        metric === "rank"
          ? "#" + l.value
          : metric === "share"
            ? pct(l.value)
            : F(l.value);
      let label =
        `<path d="M${R + 5} ${l.actual}L${R + 22} ${l.target}H${R + 29}" stroke="${l.ink}" fill="none"/>` +
        text(
          R + 35,
          l.target + 5,
          l.name + "  " + val,
          'font-size="14" fill="var(--gv-ink)" font-weight="600"',
        );
      b += `<g opacity="${l.opacity}">${seriesAction ? mark(seriesAction, l.key, l.name, label, focus === l.key) : label}</g>`;
    });
    if (!series.length)
      b += text(
        (L + R) / 2,
        (T + B) / 2,
        "请选择关注对象",
        'font-size="20" text-anchor="middle" fill="var(--gv-muted)"',
      );
    if (series.length && !all.length)
      b += text(
        (L + R) / 2,
        (T + B) / 2,
        "该窗口没有可用观测",
        'font-size="20" text-anchor="middle" fill="var(--gv-muted)"',
      );
    b += text(
      L,
      y + height - 12,
      metric === "rank"
        ? "位次越靠上越领先；空值断开。"
        : metric === "share"
          ? "份额分母保持完整；空值断开。"
          : "OpenRank 原值；空值断开。",
      'font-size="13" fill="var(--gv-muted)"',
    );
    return b;
  }
  function barArea(
    rows,
    {
      x = 0,
      y = 0,
      width = 1280,
      height = 650,
      action = null,
      selected = null,
      percent = false,
      signedValues = false,
      label = "OpenRank",
      rightCoverage = false,
    } = {},
  ) {
    const rowH = Math.min(38, (height - 60) / Math.max(rows.length, 1)),
      left = x + Math.min(265, width * 0.36),
      right = x + width - 100,
      zero = signedValues ? (left + right) / 2 : left,
      max = Math.max(...rows.map((r) => Math.abs(r.value || 0)), 0.0001),
      scale = (signedValues ? (right - left) / 2 : right - left) / max;
    let b = text(left, y + 25, label, 'font-size="15" fill="var(--gv-muted)"');
    rows.forEach((r, i) => {
      let yy = y + 54 + i * rowH,
        w = Math.abs(r.value || 0) * scale,
        bx = signedValues && r.value < 0 ? zero - w : zero,
        display =
          r.value === null
            ? "—"
            : signedValues
              ? signed(r.value * 100, " pp")
              : percent
                ? pct(r.value)
                : F(r.value),
        chosen = selected === r.key;
      let row =
        `<rect x="${x + 5}" y="${yy - 21}" width="${width - 10}" height="${rowH - 2}" rx="4" fill="${chosen ? "var(--gv-raised)" : i % 2 ? "transparent" : "var(--gv-raised)"}" stroke="${chosen ? "var(--gv-goldDisplay)" : "transparent"}"/>` +
        text(
          x + 15,
          yy,
          (r.rank ? r.rank + ". " : "") + r.name,
          `font-size="${width < 850 ? 15 : 18}"`,
        ) +
        `<rect x="${bx}" y="${yy - 15}" width="${w}" height="18" rx="3" fill="${signedValues && r.value < 0 ? "var(--al-down)" : "var(--gv-cyan)"}"/>` +
        text(right + 9, yy, display, 'font-size="15"') +
        (rightCoverage
          ? text(
              x + width - 12,
              yy,
              `${r.coverage}/${r.count}`,
              'font-size="12" text-anchor="end"',
            )
          : "");
      b += action
        ? mark(action, r.key, r.name + " " + display, row, chosen)
        : row;
    });
    if (signedValues)
      b += `<path d="M${zero} ${y + 35}V${y + height - 5}" stroke="var(--gv-muted)"/>`;
    return b;
  }
  function categoryHistory(scope, key, metric) {
    return D.months.map(
      (_, i) => M.categories(scope, i).find((r) => r.key === key)[metric],
    );
  }
  function resetProjects() {
    let c = configs["al-project-rank"];
    c.picks = M.projectRows("all", c.section, c.month)
      .filter((r) => r.value !== null)
      .slice(0, 3)
      .map((r) => r.key);
    c.page = 0;
  }
  function renderMaps() {
    globalThis.LandscapeAtlas.boot({
      D,
      M,
      register: (id, data) => {
        chartData[id] = data;
        renderTable(id);
      },
      openProject: projectDialog,
    });
  }
  function renderRank() {
    const id = "al-category-rank",
      c = configs[id],
      rows = M.categories(c.scope, c.month);
    controls(
      id,
      scopeControls(c) +
        optionSelect(
          id,
          "month",
          "观测月份",
          D.months.map((m, i) => [i, m]).reverse(),
          c.month,
        ),
    );
    setChart(
      id,
      svg(
        1280,
        840,
        barArea(rows, { height: 820, action: "focus", selected: c.focus }),
        "子类别月度 OpenRank 排行",
      ),
      rows.map((r) => ({
        位次: r.rank,
        子类别: r.name,
        OpenRank: r.value,
        份额: pct(r.share),
        项目数: r.count,
        有观测: r.coverage,
        共同样本环比: pct(r.change),
        环比共同样本: r.common,
        位次变化: r.rankChange,
      })),
      `${scopeName(c.scope)} · ${D.months[c.month]}${c.focus ? " · " + catName(c.focus) + " 已聚焦" : ""} · 全部观测覆盖见精确数据；环比只计算相邻月共同有值项目。`,
      false,
      scopeName(c.scope),
      D.months[c.month],
    );
  }
  function renderOverview() {
    const id = "al-category-heat",
      c = configs[id],
      ss = M.sections(c.scope),
      history = D.months.map((_, i) => M.categories(c.scope, i));
    const overviewColor = (key) => {
      if (c.focus) return key === c.focus ? "var(--gv-brand)" : "var(--gv-s7)";
      const rank = history[LAST].find((r) => r.key === key).rank;
      return rank && rank <= 3 ? palette[rank - 1] : "var(--gv-s7)";
    };
    controls(
      id,
      scopeControls(c, false) +
        windowControls(c) +
        metricControls(c) +
        `<div class="al-focus-chips" aria-label="聚焦类别">${ss.map((k) => `<button type="button" data-action="focus" data-value="${E(k)}" aria-pressed="${c.focus === k}" style="--al-choice-color:${overviewColor(k)}">${E(catName(k))}</button>`).join("")}</div>`,
    );
    const series = ss.map((k) => ({
      key: k,
      name: catName(k),
      color: overviewColor(k),
      values: history.map((rr) => rr.find((r) => r.key === k)[c.metric]),
      coverage: history.map((rr) => {
        let r = rr.find((r) => r.key === k);
        return `${r.coverage}/${r.count}`;
      }),
    }));
    setChart(
      id,
      svg(
        1280,
        570,
        trajectory(series, {
          height: 570,
          metric: c.metric,
          window: c.window,
          rankMax: ss.length,
          focus: c.focus,
          seriesAction: "focus",
        }),
        "分类月度位次轨迹",
      ),
      history.slice(start(c)).flatMap((rr, j) =>
        rr.map((r) => ({
          月份: D.months[start(c) + j],
          子类别: r.name,
          大类内位次: r.rank,
          OpenRank: r.value,
          大类内份额: pct(r.share),
          覆盖: `${r.coverage}/${r.count}`,
          关注: c.focus === r.key ? "是" : "否",
        })),
      ),
      `${c.scope} · ${period(c)} · 位次和份额仅在本大类内计算；默认标注当前前三，其余保留灰色轨迹；点击名称或曲线可聚焦，再次点击恢复全部。`,
      false,
      c.scope,
      period(c),
      c.focus ? catName(c.focus) : "全部类别",
    );
  }
  function renderCompare() {
    const id = "al-category-trend",
      c = configs[id];
    controls(
      id,
      familyPicker(c.categories, true) +
        `<div class="al-control-row">${windowControls(c)}${metricControls(c)}<span class="al-control-note">已选 ${c.categories.length} / 3 · 全领域 25 类统一比较</span></div>`,
    );
    const history = D.months.map((_, i) => M.categories("all", i)),
      series = c.categories.map((k, i) => ({
        key: k,
        name: catName(k),
        color: palette[i],
        values: history.map((rr) => rr.find((r) => r.key === k)[c.metric]),
        coverage: history.map((rr) => {
          const r = rr.find((x) => x.key === k);
          return `${r.coverage}/${r.count}`;
        }),
      }));
    let cards = c.categories
      .map((k, i) => {
        let now = history[LAST].find((r) => r.key === k),
          before = history[start(c)].find((r) => r.key === k),
          move = now.rank && before.rank ? before.rank - now.rank : null;
        return `<div style="--al-choice-color:${palette[i]}"><b>${E(catName(k))}</b><span>当前 #${now.rank ?? "—"} · ${move === null ? "位次待补" : move > 0 ? "↑ " + move + " 位" : move < 0 ? "↓ " + -move + " 位" : "位次不变"}</span><small>OR ${F(now.value)} · ${now.coverage}/${now.count} 有值</small></div>`;
      })
      .join("");
    setChart(
      id,
      `<div class="al-compare-summary">${cards}</div>` +
        svg(
          1280,
          490,
          trajectory(series, {
            height: 490,
            metric: c.metric,
            window: c.window,
            rankMax: 25,
          }),
          "所选子类别排名与变化",
        ),
      history.slice(start(c)).flatMap((rr, j) =>
        rr
          .filter((r) => c.categories.includes(r.key))
          .map((r) => ({
            月份: D.months[start(c) + j],
            子类别: r.name,
            全领域位次: r.rank,
            OpenRank: r.value,
            全领域份额: pct(r.share),
            覆盖: `${r.coverage}/${r.count}`,
          })),
      ),
      `可跨 Agent / Model 选择 1—3 类。位次与份额分母始终为整个领域；最近选择的类别也会带入项目图。`,
      false,
      "整个领域",
      period(c),
      c.categories.map(catName).join(" / "),
    );
  }
  function renderProject() {
    const id = "al-project-rank",
      c = configs[id],
      rows = M.projectRows("all", c.section, c.month),
      numPages = Math.ceil(rows.length / 8);
    c.page = Math.max(0, Math.min(c.page, numPages - 1));
    const shown = rows.slice(c.page * 8, c.page * 8 + 8);
    controls(
      id,
      familyPicker([c.section]) +
        `<div class="al-control-row">${windowControls(c)}${metricControls(c)}${optionSelect(
          id,
          "month",
          "榜单月份",
          D.months
            .map((m, i) => [i, m])
            .slice(start(c))
            .reverse(),
          c.month,
        )}</div><div class="al-project-toolbar"><span>${E(catName(c.section))} · ${rows.length} 项目 · 勾选最多 3 项比较</span><div><button type="button" data-action="page" data-value="-1" ${c.page === 0 ? "disabled" : ""}>上一页</button><span>${c.page + 1} / ${numPages}</span><button type="button" data-action="page" data-value="1" ${c.page + 1 === numPages ? "disabled" : ""}>下一页</button></div></div>`,
    );
    let b =
      text(
        15,
        30,
        `${D.months[c.month]} 项目榜`,
        'font-size="21" font-weight="650"',
      ) +
      text(
        320,
        30,
        "OpenRank",
        'font-size="15" text-anchor="end" fill="var(--gv-muted)"',
      );
    shown.forEach((r, i) => {
      let y = 65 + i * 55,
        checked = c.picks.includes(r.key),
        ink = palette[c.picks.indexOf(r.key)] || "var(--gv-muted)",
        body =
          `<rect x="8" y="${y - 22}" width="365" height="48" rx="6" fill="var(--gv-raised)" stroke="${checked ? ink : "var(--gv-line)"}"/><rect x="18" y="${y - 6}" width="14" height="14" rx="2" fill="${checked ? ink : "var(--gv-surface)"}" stroke="${ink}"/>` +
          text(43, y + 4, `${r.rank ?? "—"} ${r.name}`, 'font-size="15"') +
          text(326, y + 4, F(r.value), 'font-size="14" text-anchor="end"');
      b += mark(
        "pick-project",
        r.key,
        `${r.name}，${checked ? "取消" : "加入"}比较，${F(r.value)}`,
        body,
        checked,
      );
      b += mark(
        "open-project",
        r.key,
        `查看 ${r.name} 详情`,
        `<circle cx="352" cy="${y}" r="12" fill="var(--gv-surface)" stroke="var(--gv-line)"/>` +
          text(352, y + 5, "i", 'font-size="16" text-anchor="middle"'),
      );
    });
    const histories = D.months.map((_, i) =>
        M.projectRows("all", c.section, i),
      ),
      series = c.picks.map((key, j) => {
        let p = P.find((p) => p.id === key);
        return {
          key,
          name: p.name,
          color: palette[j],
          values: histories.map(
            (rr) => rr.find((r) => r.key === key)[c.metric],
          ),
        };
      });
    b += trajectory(series, {
      x: 390,
      width: 890,
      height: 550,
      metric: c.metric,
      window: c.window,
      rankMax: rows.length,
      cursor: c.month,
      pointAction: "project-month",
    });
    b += text(
      15,
      535,
      `${c.page * 8 + 1}—${Math.min((c.page + 1) * 8, rows.length)} / ${rows.length} · 有值 ${rows.filter((r) => r.value !== null).length}/${rows.length}`,
      'font-size="13" fill="var(--gv-muted)"',
    );
    setChart(
      id,
      svg(1280, 560, b, "项目榜与历史曲线同图联动"),
      histories.slice(start(c)).flatMap((rr, j) =>
        rr.map((r) => ({
          月份: D.months[start(c) + j],
          项目: r.name,
          类内位次: r.rank,
          OpenRank: r.value,
          类内份额: pct(r.share),
          状态: r.state,
          曲线已选: c.picks.includes(r.key) ? "是" : "否",
        })),
      ),
      `${catName(c.section)} · 点击曲线上的月份节点，左侧切换到该月排行。当前比较 ${c.picks.length} 项；缺失月份留空，不计为零。`,
      false,
      catName(c.section),
      period(c),
      c.picks.map((k) => P.find((p) => p.id === k).name).join(" / "),
    );
  }
  function countryControls(
    id,
    c,
    { category = false, periodSelect = false } = {},
  ) {
    return (
      scopeControls(c) +
      (category ? categoryScopeSelect(id, c) : "") +
      (periodSelect
        ? optionSelect(
            id,
            "window",
            "统计期",
            [
              [6, "最近 6 个月"],
              [12, "最近 12 个月"],
              [18, "最近 18 个月"],
            ],
            c.window,
          )
        : windowControls(c))
    );
  }
  function renderCountryMap() {
    const id = "al-country-rank",
      c = configs[id],
      rows = M.country(c.scope, c.section, c.window, LAST);
    controls(
      id,
      countryControls(id, c, { category: true, periodSelect: true }) +
        `<button type="button" data-action="clear-country" ${c.country === null ? "disabled" : ""}>清除选择</button>`,
    );
    const mapped = rows
      .filter((r) => D.world.some((f) => f.code === r.code))
      .map((r) => r.share)
      .sort((a, b) => a - b);
    const p95Index = (mapped.length - 1) * 0.95;
    const cap = Math.max(
      0.0001,
      mapped[Math.floor(p95Index)] +
        (mapped[Math.ceil(p95Index)] - mapped[Math.floor(p95Index)]) *
          (p95Index % 1),
    );
    let b =
      text(16, 30, "贡献份额 · 模拟", 'font-size="22" font-weight="650"') +
      text(
        920,
        30,
        "国家 / 开发者 / 贡献量 / 份额",
        'font-size="18" fill="var(--gv-muted)"',
      ) +
      '<g transform="translate(12,65)">';
    D.world.forEach((f) => {
      let r = rows.find((c) => c.code === f.code),
        q = r ? Math.min(1, r.share / cap) : 0,
        chosen = r && r.code === c.country,
        path = `<path d="${f.d}" fill="${chosen ? "var(--gv-goldDisplay)" : r ? `var(--gv-m${Math.min(5, Math.floor(q * 6))})` : "var(--gv-empty)"}" stroke="${chosen ? "var(--gv-ink)" : "var(--gv-line)"}" stroke-width="${chosen ? 2.5 : 0.5}"/>`;
      b += r
        ? mark(
            "country",
            r.code,
            `${r.name} · 模拟贡献份额 ${pct(r.share)}`,
            path,
            chosen,
          )
        : path;
    });
    b += "</g>";
    rows.forEach((r, i) => {
      let y = 72 + i * 48,
        chosen = r.code === c.country,
        row =
          `<rect x="910" y="${y - 24}" width="478" height="44" rx="5" fill="${chosen ? "var(--gv-raised)" : "transparent"}" stroke="${chosen ? "var(--gv-goldDisplay)" : "transparent"}"/>` +
          text(925, y + 3, `${i + 1} ${r.name}`, 'font-size="20"') +
          text(
            1125,
            y + 3,
            F(r.developers, 0),
            'font-size="19" text-anchor="end"',
          ) +
          text(1250, y + 3, F(r.value, 0), 'font-size="19" text-anchor="end"') +
          text(1370, y + 3, pct(r.share), 'font-size="19" text-anchor="end"');
      b += mark("country", r.code, r.name + " " + pct(r.share), row, chosen);
    });
    const chosen = rows.find((r) => r.code === c.country);
    b +=
      text(
        20,
        540,
        chosen
          ? `已选择 ${chosen.name} · 贡献份额 ${pct(chosen.share)} · 去重开发者 ${F(chosen.developers, 0)}`
          : "未选择国家 · 地图保留完整分布",
        'font-size="19"',
      ) +
      text(20, 574, "份额 0", 'font-size="16" fill="var(--gv-muted)"') +
      Array.from(
        { length: 6 },
        (_, i) =>
          `<rect x="${90 + i * 32}" y="559" width="32" height="18" fill="var(--gv-m${i})"/>`,
      ).join("") +
      text(
        294,
        574,
        `${pct(cap)}+ · P95 封顶`,
        'font-size="16" fill="var(--gv-muted)"',
      ) +
      text(
        530,
        574,
        "灰色：未单列数值；金色：当前选择",
        'font-size="16" fill="var(--gv-muted)"',
      ) +
      text(
        20,
        604,
        "其他与未知保留在榜单和分母中。SIM-341 · 模拟数据。",
        'font-size="17" fill="var(--gv-muted)"',
      );
    setChart(
      id,
      svg(1400, 620, b, "国家贡献地图与排行"),
      rows.map((r) => ({
        国家: r.name,
        去重开发者: r.developers,
        模拟贡献量: r.value,
        贡献份额: pct(r.share),
        选中: r.code === c.country ? "是" : "否",
      })),
      `${countryScope(c)} · ${period(c)} · 地图与本图榜单互选，不改变下方国家技术分布图的选择。`,
      true,
      countryScope(c),
      period(c),
      chosen?.name || "未选择国家",
    );
  }
  function renderCountryDetail() {
    const id = "al-country-detail",
      c = configs[id],
      rows = M.country(c.scope, "all", c.window, LAST),
      details = M.countryCategories(c.scope, c.country, c.window, LAST),
      name = cc(c.country).name;
    controls(
      id,
      countryControls(id, c) +
        segment(
          "metric",
          [
            ["share", "贡献去向"],
            ["categoryShare", "类内份额"],
          ],
          c.metric,
          "分布口径",
        ),
    );
    let b =
      text(16, 30, "国家贡献排行", 'font-size="20" font-weight="650"') +
      text(
        395,
        30,
        `${name} · ${c.metric === "share" ? "贡献去向" : "各子类别中的贡献份额"}`,
        'font-size="21" font-weight="650"',
      );
    rows.forEach((r, i) => {
      let y = 72 + i * 49,
        chosen = r.code === c.country;
      let body =
        `<rect x="8" y="${y - 25}" width="350" height="44" rx="5" fill="${chosen ? "var(--gv-raised)" : "transparent"}" stroke="${chosen ? "var(--gv-goldDisplay)" : "var(--gv-line)"}"/>` +
        text(22, y + 3, `${i + 1} ${r.name}`, 'font-size="19"') +
        text(340, y + 3, pct(r.share), 'font-size="19" text-anchor="end"');
      b += mark("country", r.code, "选择 " + r.name, body, chosen);
    });
    const rr = details
      .map((r) => ({ ...r, value: r[c.metric] }))
      .sort((a, b) => b.value - a.value);
    b += barArea(rr, {
      x: 380,
      y: 36,
      width: 900,
      height: 590,
      percent: true,
      label:
        c.metric === "share"
          ? "占该国在当前领域全部贡献的比例"
          : "该国 / 该类别全部国家贡献",
    });
    b +=
      text(
        18,
        548,
        `${scopeName(c.scope)} · ${c.window} 个月`,
        'font-size="15" fill="var(--gv-muted)"',
      ) +
      text(
        18,
        575,
        "7 个具名国家 + 其他 / 未知",
        'font-size="14" fill="var(--gv-muted)"',
      ) +
      text(
        18,
        603,
        "点击左侧，右侧原位更新。",
        'font-size="14" fill="var(--gv-muted)"',
      );
    setChart(
      id,
      svg(1280, 650, b, "国家排名与技术贡献分布"),
      details.map((r) => ({
        国家: name,
        子类别: r.name,
        模拟贡献量: r.value,
        该国贡献去向: pct(r.share),
        类内国家份额: pct(r.categoryShare),
        类内去重开发者: r.developers,
      })),
      `${name} · ${scopeName(c.scope)} · ${period(c)} · “贡献去向”在该国的类别间合计 100%；“类内份额”的分母是各类别的全部国家贡献。`,
      true,
      `${scopeName(c.scope)} / ${name}`,
      period(c),
      name,
    );
  }
  function comparisonPlot(scope, countries, values, { lq = false } = {}) {
    const ss = M.sections(scope),
      W = 1280,
      H = 100 + Math.max(ss.length, 13) * 40,
      L = 285,
      R = 1190,
      T = 78,
      max =
        Math.max(
          ...values.flatMap((r) => countries.map((code) => r[code] ?? 0)),
          lq ? 1 : 0.01,
        ) * (lq ? 1.1 : 1.15),
      px = (v) => L + ((R - L) * v) / max;
    let b = "";
    countries.forEach((code, j) => {
      const c = cc(code),
        x = 15 + (j % 5) * 245,
        y = 23 + Math.floor(j / 5) * 25;
      b +=
        `<circle cx="${x + 7}" cy="${y - 5}" r="5" fill="${c.color}"/>` +
        text(x + 20, y, c.name, 'font-size="16"');
    });
    for (let j = 0; j <= 4; j++) {
      let val = (max * j) / 4,
        x = px(val);
      b +=
        `<path d="M${x} ${T - 7}V${H - 32}" stroke="var(--gv-line)"/>` +
        text(
          x,
          H - 9,
          lq ? F(val, 1) : pct(val),
          'font-size="14" text-anchor="middle"',
        );
    }
    if (lq)
      b +=
        `<path d="M${px(1)} ${T - 9}V${H - 32}" stroke="var(--gv-goldDisplay)" stroke-width="2" stroke-dasharray="6 5"/>` +
        text(px(1), T - 17, "LQ = 1", 'font-size="14" text-anchor="middle"');
    ss.forEach((k, i) => {
      let y = T + i * 40;
      b += text(15, y + 12, catName(k), 'font-size="17"');
      b += `<path d="M${L} ${y + 10}H${R}" stroke="var(--gv-line)" stroke-opacity=".5"/>`;
      countries.forEach((code, j) => {
        let v = values[i][code],
          yy =
            y +
            10 +
            (j - (countries.length - 1) / 2) *
              (countries.length > 3 ? 3.2 : 10),
          ink = cc(code).color;
        if (v === null || v === undefined) return;
        const xx = px(v);
        b += `<g tabindex="0"><title>${E(catName(k) + " / " + cc(code).name)} · ${lq ? "LQ " + F(v) : pct(v)}</title><circle cx="${xx}" cy="${yy}" r="${countries.length > 3 ? 3.5 : 4.5}" fill="${ink}"/>${countries.length <= 3 ? text(xx + 9, yy + 4, lq ? F(v) : pct(v), 'font-size="12" fill="var(--gv-ink)"') : ""}</g>`;
      });
    });
    if (!countries.length)
      b += text(
        760,
        H / 2,
        "请勾选至少一个国家",
        'font-size="21" text-anchor="middle" fill="var(--gv-muted)"',
      );
    return svg(W, H, b, lq ? "国家技术专长比较" : "国家贡献份额比较");
  }
  function renderCountryStack() {
    const id = "al-country-stack",
      c = configs[id],
      ss = M.sections(c.scope),
      tables = ss.map((k) => M.country(c.scope, k, c.window, LAST));
    controls(
      id,
      scopeControls(c, false) +
        windowControls(c) +
        segment(
          "mode",
          [
            ["compare", "国家份额对比"],
            ["structure", "100% 结构"],
          ],
          c.mode,
          "呈现方式",
        ) +
        countryPicker(c),
    );
    let graph;
    if (c.mode === "compare") {
      const vals = tables.map((rr) =>
        Object.fromEntries(rr.map((r) => [r.code, r.share])),
      );
      graph = comparisonPlot(c.scope, c.countries, vals);
    } else {
      const H = 130 + 13 * 37,
        L = 285,
        bw = 930;
      let b = "";
      c.countries.forEach((code, i) => {
        const r = cc(code),
          x = 15 + (i % 5) * 245,
          y = 24 + Math.floor(i / 5) * 25;
        b +=
          `<rect x="${x}" y="${y - 12}" width="14" height="14" fill="${r.color}"/>` +
          text(x + 21, y, r.name, 'font-size="16"');
      });
      ss.forEach((key, i) => {
        let x = L,
          y = 95 + i * 37,
          rr = tables[i],
          remaining = 0;
        b += text(15, y + 19, catName(key), 'font-size="17"');
        for (const code of c.countries) {
          let r = rr.find((x) => x.code === code),
            w = r.share * bw;
          b += `<g tabindex="0"><title>${E(catName(key) + " / " + r.name)} · ${pct(r.share)}</title><rect x="${x}" y="${y}" width="${w}" height="25" fill="${countryColor(r.code)}"/>${w > 70 ? text(x + w / 2, y + 17, pct(r.share), `font-size="13" text-anchor="middle" fill="${contrastInk(countryColor(r.code))}"`) : ""}</g>`;
          x += w;
        }
        remaining = rr
          .filter((r) => !c.countries.includes(r.code))
          .reduce((s, r) => s + r.share, 0);
        if (remaining > 1e-10)
          b += `<g tabindex="0"><title>未关注国家合计 ${pct(remaining)}</title><rect x="${x}" y="${y}" width="${remaining * bw}" height="25" fill="var(--gv-line)"/>${remaining * bw > 155 ? text(x + (remaining * bw) / 2, y + 17, "未关注 " + pct(remaining), 'font-size="13" text-anchor="middle"') : ""}</g>`;
      });
      graph = svg(1280, H, b, "关注国家与未关注国家的完整贡献结构");
    }
    setChart(
      id,
      graph,
      tables.flatMap((rr, i) =>
        rr.map((r) => ({
          子类别: catName(ss[i]),
          国家: r.name,
          模拟贡献量: r.value,
          类内份额: pct(r.share),
          关注: c.countries.includes(r.code) ? "是" : "否",
        })),
      ),
      `${c.scope} · ${period(c)} · 关注 ${c.countries.length} 个国家。份额分母始终包含全部国家、其他与未知；100% 视图将未勾选部分合并为“未关注国家”。`,
      true,
      c.scope,
      period(c),
      c.countries.map((k) => cc(k).name).join(" / ") || "未选择国家",
    );
  }
  function renderConcentration() {
    const id = "al-concentration",
      c = configs[id],
      rows = M.concentration(c.scope, c.month),
      rr = M.projectRows(c.scope, c.section, c.month).filter(
        (r) => r.value !== null,
      ),
      top = rr.slice(0, 3),
      sum = rr.reduce((s, r) => s + r.value, 0),
      selected = rows.find((r) => r.key === c.section);
    controls(
      id,
      scopeControls(c, false) +
        optionSelect(
          id,
          "month",
          "观测月份",
          D.months.map((m, i) => [i, m]).reverse(),
          c.month,
        ),
    );
    let b = barArea(rows, {
      width: 790,
      height: 560,
      action: "category-focus",
      selected: c.section,
      percent: true,
      label: "Top 3 占本类别有观测项目 OpenRank",
    });
    b +=
      text(835, 40, catName(c.section), 'font-size="24" font-weight="650"') +
      text(
        835,
        78,
        `Top 3 ${pct(selected?.value)} · ${selected?.coverage}/${selected?.count} 有值`,
        'font-size="18" fill="var(--gv-muted)"',
      );
    top.forEach((r, i) => {
      let y = 145 + i * 100,
        share = sum ? r.value / sum : null;
      b +=
        text(835, y, `${i + 1}. ${r.name}`, 'font-size="17"') +
        `<rect x="835" y="${y + 15}" width="${(share || 0) * 330}" height="16" rx="3" fill="${palette[i]}"/>` +
        text(1238, y + 29, pct(share), 'font-size="17" text-anchor="end"');
    });
    b +=
      text(
        835,
        490,
        `其余 ${Math.max(0, rr.length - 3)} 项目：${pct(sum ? 1 - top.reduce((s, r) => s + r.value, 0) / sum : null)}`,
        'font-size="17"',
      ) +
      text(
        835,
        525,
        "点击左侧类别，在此展开。",
        'font-size="15" fill="var(--gv-muted)"',
      );
    const exportRows = rows.map((r) => {
      let pp = M.projectRows(c.scope, r.key, c.month)
        .filter((x) => x.value !== null)
        .slice(0, 3);
      return {
        子类别: r.name,
        Top3占比: pct(r.value),
        项目数: r.count,
        有观测: r.coverage,
        OpenRank合计: r.openrank,
        Top3项目: pp.map((p) => p.name).join(" / "),
        Top3各自OpenRank: pp.map((p) => p.value).join(" / "),
      };
    });
    setChart(
      id,
      svg(1280, 580, b, "类别集中度与头部项目"),
      exportRows,
      `${c.scope} · ${D.months[c.month]} · 小样本类别更容易达到 100%；集中度只在有观测项目中计算。`,
      false,
      c.scope,
      D.months[c.month],
      catName(c.section),
    );
  }
  function commonSeries(c) {
    const pp = M.projects(c.scope).filter((p) =>
      p.trend.slice(start(c), LAST + 1).every(M.num),
    );
    return {
      count: pp.length,
      series: M.sections(c.scope).map((k) => ({
        key: k,
        name: catName(k),
        color: "var(--gv-brand)",
        values: D.months.map((_, m) => {
          if (m < start(c)) return null;
          let total = pp.reduce((s, p) => s + p.trend[m], 0),
            value = pp
              .filter((p) => p.section === k)
              .reduce((s, p) => s + p.trend[m], 0);
          return total ? value / total : null;
        }),
      })),
    };
  }
  function renderShift() {
    const id = "al-shift",
      c = configs[id],
      rows = M.shift(c.scope, start(c), LAST),
      common = commonSeries(c);
    controls(id, scopeControls(c, false) + windowControls(c));
    const row = rows.find((r) => r.key === c.section);
    let b = barArea(rows, {
      width: 730,
      height: 540,
      action: "category-focus",
      selected: c.section,
      signedValues: true,
      label: "份额变化（百分点）",
    });
    b +=
      text(780, 32, catName(c.section), 'font-size="22" font-weight="650"') +
      text(
        780,
        65,
        `${pct(row.before)} → ${pct(row.after)} · ${signed(row.value * 100, " pp")}`,
        'font-size="18" fill="var(--gv-muted)"',
      );
    // This compact inset omits endpoint labels to give the whole interval room.
    const s = common.series.find((r) => r.key === c.section),
      L = 800,
      R = 1230,
      T = 125,
      B = 440,
      max = Math.max(...s.values.filter(M.num), 0.01) * 1.15;
    let path = "";
    s.values.forEach((v, i) => {
      if (i < start(c) || v === null) return;
      let x = L + ((R - L) * (i - start(c))) / (c.window - 1),
        y = B - ((B - T) * v) / max;
      path += (path ? "L" : "M") + x + "," + y;
      b += `<circle cx="${x}" cy="${y}" r="4" fill="${s.color}" tabindex="0"><title>${D.months[i]} · ${pct(v)}</title></circle>`;
    });
    b += `<path d="${path}" fill="none" stroke="${s.color}" stroke-width="3"/>`;
    [0, 1, 2].forEach((i) => {
      let yy = B - ((B - T) * i) / 2;
      b +=
        `<path d="M${L} ${yy}H${R}" stroke="var(--gv-line)"/>` +
        text(
          L - 10,
          yy + 5,
          pct((max * i) / 2),
          'font-size="13" text-anchor="end"',
        );
    });
    b +=
      text(L, B + 28, D.months[start(c)], 'font-size="15"') +
      text(R, B + 28, D.months[LAST], 'font-size="15" text-anchor="end"') +
      text(
        780,
        520,
        `共同样本 ${common.count} 项目 · 该类 ${row.count} 项目`,
        'font-size="16" fill="var(--gv-muted)"',
      );
    setChart(
      id,
      svg(1280, 580, b, "共同样本份额迁移与类别轨迹"),
      common.series.flatMap((r) =>
        r.values.slice(start(c)).map((v, j) => ({
          月份: D.months[start(c) + j],
          子类别: r.name,
          共同样本份额: pct(v),
          整个范围共同项目数: common.count,
          该类共同项目数: rows.find((x) => x.key === r.key).count,
        })),
      ),
      `${c.scope} · ${period(c)} · ${common.count} 个项目在窗口每个月都有观测，全部变化使用同一组项目。点击类别查看右侧轨迹。`,
      false,
      c.scope,
      period(c),
      catName(c.section),
    );
  }
  function renderSpecialization() {
    const id = "al-specialization",
      c = configs[id],
      ss = M.sections(c.scope),
      whole = M.country(c.scope, "all", c.window, LAST),
      tables = ss.map((k) => M.country(c.scope, k, c.window, LAST));
    controls(
      id,
      scopeControls(c, false) + windowControls(c) + countryPicker(c, 3),
    );
    const values = tables.map((rr) =>
      Object.fromEntries(
        rr.map((r) => [
          r.code,
          whole.find((a) => a.code === r.code).share
            ? r.share / whole.find((a) => a.code === r.code).share
            : null,
        ]),
      ),
    );
    setChart(
      id,
      comparisonPlot(c.scope, c.countries, values, { lq: true }),
      tables.flatMap((rr, i) =>
        rr
          .filter((r) => c.countries.includes(r.code))
          .map((r) => ({
            子类别: catName(ss[i]),
            国家: r.name,
            类内贡献份额: pct(r.share),
            大类总贡献份额: pct(whole.find((x) => x.code === r.code).share),
            LQ: values[i][r.code],
          })),
      ),
      `${c.scope} · ${period(c)} · LQ = 类内贡献份额 ÷ 该国在本大类的总体份额；大于 1 表示相对专长。“其他／未知”不解释为国家专长。`,
      true,
      c.scope,
      period(c),
      c.countries.map((k) => cc(k).name).join(" / ") || "未选择国家",
    );
  }
  function renderCountryTrend() {
    const id = "al-country-trend",
      c = configs[id],
      history = D.months.map((_, i) =>
        M.country(c.scope, c.section, "month", i),
      ),
      series = c.countries.map((code) => ({
        key: code,
        name: cc(code).name,
        color: cc(code).color,
        values: history.map((rr) => rr.find((r) => r.code === code).share),
      }));
    controls(id, countryControls(id, c, { category: true }) + countryPicker(c));
    setChart(
      id,
      svg(
        1280,
        540,
        trajectory(series, { height: 540, metric: "share", window: c.window }),
        "关注国家的月度贡献份额",
      ),
      history.slice(start(c)).flatMap((rr, j) =>
        rr.map((r) => ({
          月份: D.months[start(c) + j],
          国家: r.name,
          模拟贡献量: r.value,
          贡献份额: pct(r.share),
          关注: c.countries.includes(r.code) ? "是" : "否",
        })),
      ),
      `${countryScope(c)} · ${period(c)} · 当前显示 ${c.countries.length} 条曲线；未显示国家的贡献仍保留在各月分母中。`,
      true,
      countryScope(c),
      period(c),
      c.countries.map((k) => cc(k).name).join(" / ") || "未选择国家",
    );
  }
  function render(id) {
    const f = {
      "al-category-rank": renderRank,
      "al-category-heat": renderOverview,
      "al-category-trend": renderCompare,
      "al-project-rank": renderProject,
      "al-country-rank": renderCountryMap,
      "al-country-detail": renderCountryDetail,
      "al-country-stack": renderCountryStack,
      "al-concentration": renderConcentration,
      "al-shift": renderShift,
      "al-specialization": renderSpecialization,
      "al-country-trend": renderCountryTrend,
    }[id];
    if (f) f();
  }
  function projectDialog(id, month = LAST) {
    const p = P.find((x) => x.id === id);
    if (!p) return;
    const d = $("al-project-dialog"),
      r = M.projectRows("all", p.section, month).find((x) => x.key === id);
    $("al-project-detail").innerHTML =
      `<span class="eyebrow">${E(catName(p.section))} / ${E(p.layer)}</span><h3 id="al-dialog-title">${E(p.name)}</h3><p><a href="https://github.com/${E(p.repo)}" target="_blank" rel="noopener">${E(p.repo)} ↗</a></p><p>${E(p.description)}</p><div class="al-dialog-metrics"><div><b>${F(r.value)}</b><span>${E(D.months[month])} · OpenRank</span></div><div><b>${r.rank ?? "—"}</b><span>类内位次 · ${E(r.state)}</span></div><div><b>${pct(r.share)}</b><span>类内份额</span></div></div><div class="al-view">${svg(1280, 490, trajectory([{ key: id, name: p.name, values: p.trend }], { height: 490, window: 18 }), "项目 18 个月观测")}</div><p>创建于 ${E(p.created.slice(0, 10))} · 许可证元数据 ${E(p.license || "未标注")} · ${E(p.language)}</p><details><summary>选入理由与来源</summary><p>${E(p.reason)}</p><p>${E(p.caveat)}</p><a href="${E(D.source)}">固定版本主表 ↗</a><p>前 6 个月来自固定 OpenDigger 快照；既有 12 个月保留原报告观测。</p></details>${tableHTML(
        ["月份", "OpenRank", "状态"],
        D.months.map((m, i) => [m, F(p.trend[i]), M.status(p, i)]),
      )}`;
    if (!d.open) d.showModal();
  }
  function tableHTML(keys, rows) {
    return `<div class="al-table-wrap"><table><thead><tr>${keys.map((k) => `<th>${E(k)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((x) => `<td>${E(x)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  }
  function download(name, data, mime) {
    const u = URL.createObjectURL(new Blob([data], { type: mime })),
      a = document.createElement("a");
    a.href = u;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(u), 2000);
  }
  function csvCell(x) {
    if (x === null || x === undefined) return "";
    let s = String(x);
    if (typeof x === "string" && /^[=+@-]/.test(s)) s = "'" + s;
    return '"' + s.replace(/"/g, '""') + '"';
  }
  function exportCSV(id) {
    const d = chartData[id],
      headers = d.rows.length ? Object.keys(d.rows[0]) : [],
      meta = ["数据性质", "范围", "统计期", "来源或生成规则", "关注对象"];
    let rows = [
      headers.concat(meta),
      ...d.rows.map((r) =>
        headers
          .map((k) => r[k])
          .concat([
            d.sim ? "模拟数据" : "真实观测",
            d.scope,
            d.period,
            d.sim
              ? "SIM-341 / independent synthetic contributions"
              : D.source + " + OpenDigger snapshot 2026-10-17",
            d.attention || "",
          ]),
      ),
    ];
    download(
      `${id}-${d.sim ? "SIMULATED" : "REAL"}-${d.period.replace(/[^\d-]/g, "")}.csv`,
      "\ufeff" + rows.map((r) => r.map(csvCell).join(",")).join("\r\n"),
      "text/csv;charset=utf-8",
    );
  }
  async function exportSVG(id) {
    const panel = $(id),
      original = panel.querySelector(".al-view svg");
    if (!original) {
      panel.querySelector(".al-readout").textContent =
        "当前没有可导出的图形，请先选择项目。";
      return;
    }
    let clone = original.cloneNode(true),
      d = chartData[id],
      vb = original.getAttribute("viewBox").split(/\s+/).map(Number),
      w = vb[2],
      h = vb[3],
      title = panel.querySelector("h4").textContent;
    const style = getComputedStyle(panel);
    for (const img of clone.querySelectorAll("image")) {
      try {
        const response = await fetch(img.getAttribute("href"));
        if (!response.ok) throw Error("image");
        const blob = await response.blob();
        img.setAttribute(
          "href",
          await new Promise((res, rej) => {
            const reader = new FileReader();
            reader.onload = () => res(reader.result);
            reader.onerror = rej;
            reader.readAsDataURL(blob);
          }),
        );
      } catch {
        img.remove();
      }
    }
    clone.querySelectorAll("a").forEach((a) => a.removeAttribute("href"));
    let content = new XMLSerializer()
      .serializeToString(clone)
      .replace(/^<svg[^>]*>/, "")
      .replace(/<\/svg>$/, "")
      .replace(
        /var\((--[\w-]+)\)/g,
        (_, k) => style.getPropertyValue(k).trim() || "#567",
      );
    let note = `${d.sim ? "模拟数据 · 不用于事实判断" : "真实观测"} | ${d.scope} | ${d.period} | ${d.attention || ""}`;
    let result = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h + 130}" font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif" fill="${style.getPropertyValue("--gv-ink").trim() || "#173b50"}"><rect width="${w}" height="${h + 130}" fill="${style.getPropertyValue("--gv-surface").trim() || "#fff"}"/>${text(16, 32, title, 'font-size="24" font-weight="700"')}${text(16, 62, note, 'font-size="17"')}<g transform="translate(0,80)">${content}</g>${text(16, h + 110, d.sim ? "SIM-341 · 固定种子模拟，人数按模拟身份去重。" : "来源：antgroup/agentic-ai-landscape @ " + D.commit.slice(0, 7) + " + OpenDigger 历史快照 · 空值不补零", 'font-size="14"')}</svg>`;
    download(
      `${id}-${d.sim ? "SIMULATED" : "REAL"}.svg`,
      result,
      "image/svg+xml;charset=utf-8",
    );
  }
  let activePanel = null,
    placeholder = null,
    returnFocus = null;
  function openFull(id) {
    if (activePanel) return;
    const dialog = $("al-fullscreen");
    activePanel = $(id);
    returnFocus = document.activeElement;
    placeholder = document.createComment("chart position");
    activePanel.before(placeholder);
    $("al-fullscreen-body").append(activePanel);
    dialog.querySelector("strong").textContent =
      activePanel.querySelector("h4").textContent;
    dialog.showModal();
    document.body.classList.add("al-modal-open");
    activePanel.querySelector("[data-expand]").textContent = "退出全屏";
  }
  function closeFull() {
    const d = $("al-fullscreen");
    if (d.open) d.close();
  }
  $("al-fullscreen").addEventListener("close", () => {
    if (!activePanel) return;
    placeholder.replaceWith(activePanel);
    activePanel.querySelector("[data-expand]").textContent = "全屏";
    activePanel = null;
    placeholder = null;
    document.body.classList.remove("al-modal-open");
    returnFocus?.focus({ preventScroll: true });
  });
  $("al-fullscreen").querySelector(".al-close").onclick = closeFull;
  $("al-project-dialog").querySelector(".al-close").onclick = () =>
    $("al-project-dialog").close();
  document
    .querySelectorAll("[data-expand]")
    .forEach(
      (b) =>
        (b.onclick = () =>
          activePanel ? closeFull() : openFull(b.dataset.expand)),
    );
  document
    .querySelectorAll("[data-csv]")
    .forEach((b) => (b.onclick = () => exportCSV(b.dataset.csv)));
  document.querySelectorAll("[data-svg]").forEach(
    (b) =>
      (b.onclick = async () => {
        const old = b.textContent;
        b.disabled = true;
        b.textContent = "导出中…";
        try {
          await exportSVG(b.dataset.svg);
        } finally {
          b.disabled = false;
          b.textContent = old;
        }
      }),
  );
  document.querySelectorAll('.al-chapter a[href^="#"]').forEach((a) =>
    a.addEventListener("click", () => {
      if (activePanel) closeFull();
    }),
  );
  const printDetails = [];
  window.addEventListener("beforeprint", () => {
    document.querySelectorAll(".al-data").forEach((d) => {
      printDetails.push([d, d.open]);
      d.open = true;
    });
    Object.keys(chartData).forEach((id) => renderTable(id, true));
  });
  window.addEventListener("afterprint", () => {
    printDetails.splice(0).forEach(([d, open]) => (d.open = open));
    Object.keys(chartData).forEach((id) => renderTable(id));
  });
  // The same site preference is used in reading mode, dialogs and exported SVGs.
  function syncThemeControls() {
    const dark = document.documentElement.dataset.theme === "dark";
    document.querySelectorAll("[data-al-theme]").forEach((button) => {
      button.textContent = dark ? "切换明亮" : "切换深色";
      button.setAttribute("aria-pressed", String(dark));
      button.setAttribute(
        "aria-label",
        dark ? "切换为明亮主题" : "切换为深色主题",
      );
    });
  }
  document.querySelectorAll("[data-al-theme]").forEach((button) => {
    button.onclick = () => {
      const toggle = $("theme-toggle");
      if (toggle) {
        toggle.click();
        return;
      }
      const next =
        document.documentElement.dataset.theme === "dark" ? "light" : "dark";
      document.documentElement.dataset.theme = next;
      try {
        window.localStorage.setItem("osdg-theme", next);
      } catch (_) {
        /* Private browsing can disable storage. */
      }
      document.dispatchEvent(new window.Event("gosdthemechange"));
    };
  });
  document.addEventListener("gosdthemechange", () => {
    syncThemeControls();
    renderCountryStack(); // Percentage labels need a newly computed ink contrast.
  });
  syncThemeControls();
  const readingLinks = [...document.querySelectorAll(".al-jump a")];
  const activateReading = (href) =>
    readingLinks.forEach((a) => {
      if (a.getAttribute("href") === href)
        a.setAttribute("aria-current", "location");
      else a.removeAttribute("aria-current");
    });
  readingLinks.forEach((a) =>
    a.addEventListener("click", () => activateReading(a.getAttribute("href"))),
  );
  if (window.IntersectionObserver) {
    const observer = new window.IntersectionObserver(
      (entries) => {
        const entry = entries
          .filter((e) => e.isIntersecting)
          .sort(
            (a, b) => a.boundingClientRect.top - b.boundingClientRect.top,
          )[0];
        if (entry) activateReading("#" + entry.target.id);
      },
      { rootMargin: "-15% 0px -65% 0px", threshold: 0 },
    );
    readingLinks.forEach((a) =>
      observer.observe(document.querySelector(a.getAttribute("href"))),
    );
  }
  resetProjects();
  renderMaps();
  Object.keys(configs).forEach(render);
})();
