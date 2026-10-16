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
    function country(scope, section, period, m) {
      let ss = sections(scope),
        rr = D.simulation.filter(
          (r) =>
            ss.includes(r.section) &&
            (section === "all" || r.section === section) &&
            (period === "rolling" || r.month === m),
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
      return rank(
        rows.map((r) => ({ ...r, share: total ? r.value / total : 0 })),
      );
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
  if (D.version !== "4.1-v2") return;
  const M = globalThis.LandscapeModel(D),
    $ = (id) => document.getElementById(id),
    base = document.querySelector('meta[name="gosd-base"]')?.content || "",
    P = D.projects;
  const state = {
    scope: "all",
    month: 11,
    category: "Personal AI assistants",
    countryScope: "all",
    country: "US",
    period: "rolling",
    heat: "rank",
    categoryMode: "value",
    projectView: "line",
    limit: 10,
    start: 8,
    end: 11,
    picks: [],
  };
  const chartData = {},
    pages = {},
    colours = [
      "#3c84b5",
      "#d18739",
      "#42a597",
      "#b76d96",
      "#8771ae",
      "#8f984a",
      "#6483cc",
      "#8998a4",
      "#b6bcc2",
    ];
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
  const signed = (v, unit = "") =>
    v === null ? "—" : (v > 0 ? "+" : "") + F(v, 1) + unit;
  const scopeName = () => (state.scope === "all" ? "整个领域" : state.scope);
  const countryScopeName = () =>
    state.countryScope === "all"
      ? scopeName()
      : D.sections[state.countryScope].name;
  const periodName = () =>
    state.period === "rolling"
      ? "2025-09—2026-08（12 个月）"
      : D.months[state.month];
  function shade(q, base = [0, 125, 135]) {
    q = Math.max(0, Math.min(1, q));
    const rgb = base.map((v) => Math.round(242 + (v - 242) * q));
    return "#" + rgb.map((v) => v.toString(16).padStart(2, "0")).join("");
  }
  function contrastInk(hex) {
    const rgb = hex
      .slice(1)
      .match(/../g)
      .map((x) => parseInt(x, 16) / 255)
      .map((v) => (v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
    const lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
    return lum > 0.179 ? "#091b29" : "#ffffff";
  }
  function text(x, y, s, attrs = "") {
    return `<text x="${x}" y="${y}" ${attrs}>${E(s)}</text>`;
  }
  function svg(w, h, body, label) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" role="group" aria-label="${E(label)}"><rect width="${w}" height="${h}" fill="var(--gv-surface)"/>${body}</svg>`;
  }
  function mark(attr, label, body) {
    return `<g role="button" tabindex="0" ${attr} aria-label="${E(label)}"><title>${E(label)}</title>${body}</g>`;
  }
  function bindMarks(el) {
    el.querySelectorAll("[data-category]").forEach(
      (n) => (n.onclick = () => chooseCategory(n.dataset.category)),
    );
    el.querySelectorAll("[data-project]").forEach(
      (n) =>
        (n.onclick = (e) => {
          e.preventDefault();
          projectDialog(n.dataset.project);
        }),
    );
    el.querySelectorAll("[data-country]").forEach(
      (n) =>
        (n.onclick = () => {
          state.country = n.dataset.country;
          renderCountry();
        }),
    );
    el.querySelectorAll('[role="button"]').forEach(
      (n) =>
        (n.onkeydown = (e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            n.click();
          }
        }),
    );
  }
  function setChart(
    id,
    markup,
    rows,
    readout,
    sim = false,
    scopeOverride = null,
    periodOverride = null,
  ) {
    const el = $(id);
    el.querySelector(".al-view").innerHTML = markup;
    el.querySelector(".al-readout").textContent = readout;
    chartData[id] = {
      rows,
      sim,
      scope: scopeOverride || (sim ? countryScopeName() : scopeName()),
      period: periodOverride || (sim ? periodName() : D.months[state.month]),
    };
    pages[id] = Math.min(
      pages[id] || 0,
      Math.max(0, Math.ceil(rows.length / 8) - 1),
    );
    renderTable(id);
    bindMarks(el);
  }
  function renderTable(id, print = false) {
    const host = $(id).querySelector(".al-data-body"),
      rows = chartData[id].rows,
      keys = rows.length ? Object.keys(rows[0]) : [],
      page = pages[id] || 0,
      start = print ? 0 : page * 8,
      end = print ? rows.length : Math.min(start + 8, rows.length);
    host.innerHTML = rows.length
      ? `<div class="al-table-wrap"><table><thead><tr>${keys.map((k) => `<th scope="col">${E(k)}</th>`).join("")}</tr></thead><tbody>${rows
          .slice(start, end)
          .map(
            (r) =>
              `<tr>${keys.map((k) => `<td>${E(r[k] === null ? "—" : typeof r[k] === "number" ? F(r[k], Number.isInteger(r[k]) ? 0 : 2) : r[k])}</td>`).join("")}</tr>`,
          )
          .join(
            "",
          )}</tbody></table></div><div class="al-pager"><button type="button" data-page="-1" ${start === 0 ? "disabled" : ""}>上一页</button><span>${start + 1}—${end} / ${rows.length} 行</span><button type="button" data-page="1" ${end === rows.length ? "disabled" : ""}>下一页</button></div>`
      : "<p>该范围没有可用记录。</p>";
    host.querySelectorAll("[data-page]").forEach(
      (b) =>
        (b.onclick = () => {
          pages[id] += Number(b.dataset.page);
          renderTable(id);
        }),
    );
  }
  function bars(
    rows,
    {
      kind = "value",
      attr = "data-category",
      label = "OpenRank",
      max = null,
      diverging = false,
      rightLabel = "观测 / 项目",
      heightRows = 25,
    } = {},
  ) {
    const W = 1280,
      rowH = 30,
      H = 90 + Math.max(rows.length, heightRows) * rowH,
      left = 290,
      right = 1120,
      zero = diverging ? 705 : left,
      maxv =
        max ?? Math.max(...rows.map((r) => Math.abs(r.value || 0)), 0.0001),
      scale = (diverging ? 390 : right - left) / maxv;
    let b =
      text(left, 27, label, 'font-size="17" fill="var(--gv-muted)"') +
      text(
        1252,
        27,
        rightLabel,
        'font-size="16" text-anchor="end" fill="var(--gv-muted)"',
      );
    rows.forEach((r, i) => {
      let y = 61 + i * rowH,
        v = r.value,
        w = Math.abs(v || 0) * scale,
        x = diverging ? (v < 0 ? zero - w : zero) : left,
        display =
          kind === "share"
            ? pct(v)
            : kind === "pp"
              ? signed(v === null ? null : v * 100, " pp")
              : F(v);
      let inner =
        `<rect x="5" y="${y - 20}" width="1265" height="29" fill="${i % 2 === 0 ? "var(--gv-raised)" : "transparent"}"/>` +
        text(15, y, (r.rank ? r.rank + ". " : "") + r.name, 'font-size="18"') +
        `<rect x="${x}" y="${y - 16}" width="${w}" height="20" rx="3" fill="${diverging && v < 0 ? "#c58452" : "var(--gv-cyan)"}"/>` +
        text(
          diverging ? 1140 : Math.min(left + w + 10, 1130),
          y,
          display,
          'font-size="17"',
        ) +
        text(
          1252,
          y,
          r.coverage !== undefined
            ? `${r.coverage}/${r.count}`
            : r.count !== undefined
              ? String(r.count)
              : "",
          'font-size="15" text-anchor="end" fill="var(--gv-muted)"',
        );
      b += attr
        ? mark(`${attr}="${E(r.key)}"`, `${r.name}：${display}`, inner)
        : inner;
    });
    if (diverging)
      b += `<path d="M${zero} 37V${H - 22}" stroke="var(--gv-muted)"/>`;
    return svg(W, H, b, label);
  }
  function lines(
    series,
    {
      percent = false,
      label = "OpenRank",
      start = 0,
      end = 11,
      height = 490,
    } = {},
  ) {
    const W = 1280,
      H = height,
      L = 86,
      R = 1210,
      T = 40,
      B = 350,
      vals = series
        .flatMap((s) => s.values.slice(start, end + 1))
        .filter(M.num),
      max = Math.max(...vals, percent ? 0.1 : 1) * 1.1;
    let b = "";
    for (let i = 0; i <= 4; i++) {
      let y = B - ((B - T) * i) / 4;
      b +=
        `<path d="M${L} ${y}H${R}" stroke="var(--gv-line)"/>` +
        text(
          L - 12,
          y + 6,
          percent ? pct((max * i) / 4) : F((max * i) / 4, 0),
          'text-anchor="end" font-size="17"',
        );
    }
    for (let i = start; i <= end; i++) {
      let x = L + ((R - L) * (i - start)) / Math.max(end - start, 1);
      b += text(
        x,
        B + 29,
        D.months[i].slice(2),
        'text-anchor="middle" font-size="16"',
      );
    }
    series.forEach((s, j) => {
      let path = "",
        colour = s.color || colours[j % colours.length],
        connected = false;
      s.values.forEach((v, i) => {
        if (i < start || i > end) return;
        if (v === null) {
          connected = false;
          return;
        }
        let x = L + ((R - L) * (i - start)) / Math.max(end - start, 1),
          y = B - ((B - T) * v) / max;
        path += (connected ? "L" : "M") + x.toFixed(2) + "," + y.toFixed(2);
        connected = true;
        b += `<circle cx="${x}" cy="${y}" r="4" fill="${colour}" tabindex="0"><title>${E(s.name)} · ${D.months[i]} · ${percent ? pct(v) : F(v)}</title></circle>`;
      });
      b += `<path d="${path}" fill="none" stroke="${colour}" stroke-width="3"/>`;
      let x = 85 + (j % 3) * 390,
        y = 420 + Math.floor(j / 3) * 25;
      b +=
        `<path d="M${x} ${y - 5}h22" stroke="${colour}" stroke-width="4"/>` +
        text(x + 30, y, s.name, 'font-size="17"');
    });
    return svg(W, H, b, label);
  }
  function heat(
    rows,
    months,
    { mode = "rank", label = "月度矩阵", project = false } = {},
  ) {
    const W = 1280,
      L = 286,
      col = 78,
      rowH = 29,
      H = 95 + Math.max(rows.length, project ? 16 : 25) * rowH;
    let b = "";
    months.forEach(
      (m, j) =>
        (b += text(
          L + j * col + col / 2,
          29,
          m.slice(2),
          'text-anchor="middle" font-size="16"',
        )),
    );
    let all = rows.flatMap((r) => r.values).filter(M.num),
      max = Math.max(...all, 1),
      rankmax = Math.max(...all, 2);
    rows.forEach((r, i) => {
      let y = 43 + i * rowH;
      b += mark(
        `${project ? "data-project" : "data-category"}="${E(r.key)}"`,
        r.name,
        text(12, y + 20, r.name, 'font-size="18"'),
      );
      r.values.forEach((v, j) => {
        let q =
            v === null ? 0 : mode === "rank" ? 1 - (v - 1) / rankmax : v / max,
          alpha = v === null ? 0 : 0.08 + 0.8 * q,
          cell = shade(q),
          display =
            v === null
              ? "—"
              : mode === "rank"
                ? String(v)
                : mode === "share"
                  ? F(v * 100, 1)
                  : F(v, 0);
        b += `<g tabindex="0"><title>${E(r.name)} · ${months[j]} · ${v === null ? "无观测" : mode === "share" ? pct(v) : F(v, mode === "rank" ? 0 : 2)}${r.coverages ? " · 覆盖 " + r.coverages[j] : ""}</title><rect x="${L + j * col}" y="${y}" width="${col - 3}" height="${rowH - 3}" rx="3" fill="${v === null ? "var(--gv-raised)" : cell}" stroke="var(--gv-line)" stroke-width=".4"/>${text(L + j * col + col / 2 - 1, y + 19, display, `font-size="15" text-anchor="middle" fill="${v === null ? "var(--gv-ink)" : contrastInk(cell)}"`)}</g>`;
      });
    });
    return svg(W, H, b, label);
  }
  function categoryOptions() {
    const ss = M.sections(state.scope);
    for (const id of ["al-category", "al-country-scope"]) {
      const el = $(id),
        old = el.value;
      el.innerHTML =
        (id === "al-country-scope"
          ? '<option value="all">当前观测范围 · 全部类别</option>'
          : "") +
        ss
          .map(
            (k) => `<option value="${E(k)}">${E(D.sections[k].name)}</option>`,
          )
          .join("");
      el.value = id === "al-category" ? state.category : state.countryScope;
      if (!el.value) el.value = old;
    }
  }
  function resetPicks() {
    state.picks = M.projectRows(state.scope, state.category, state.month)
      .filter((r) => r.value !== null)
      .slice(0, 3)
      .map((r) => r.key);
  }
  function chooseCategory(key) {
    if (!M.sections(state.scope).includes(key)) return;
    state.category = key;
    state.countryScope = key;
    $("al-category").value = key;
    $("al-country-scope").value = key;
    resetPicks();
    renderProjects();
    renderCountry();
  }
  function renderMaps() {
    for (const [id, layer] of [
      ["al-agent", "Agent Infra"],
      ["al-model", "Model Infra"],
    ]) {
      const el = $(id),
        rows = M.categories(layer, state.month);
      el.querySelectorAll(".al-map-card").forEach((g) => {
        const r = rows.find((x) => x.key === g.dataset.section);
        g.querySelector(".al-map-stat").textContent =
          `${r.count} 项目 · OR ${F(r.value)} · ${r.coverage}/${r.count} 有值`;
      });
      el.querySelector(".al-map-period").textContent =
        `${D.months[state.month]} · 真实观测 · ${M.projects(layer).length} 项目`;
      chartData[id] = {
        rows: M.projects(layer).map((p) => ({
          类别: D.sections[p.section].name,
          项目: p.name,
          仓库: p.repo,
          OpenRank: M.value(p, state.month),
          观测状态: M.status(p, state.month),
        })),
        sim: false,
        scope: layer,
        period: D.months[state.month],
      };
      renderTable(id);
      el.querySelector(".al-readout").textContent =
        `${layer} 全量项目始终保留；当前月份 ${rows.reduce((a, r) => a + r.coverage, 0)} / ${M.projects(layer).length} 有观测。`;
      bindMarks(el);
    }
  }
  function renderCategories() {
    let rows = M.categories(state.scope, state.month);
    $("al-global-status").textContent =
      `${rows.reduce((s, r) => s + r.coverage, 0)} / ${M.projects(state.scope).length} 项目有值 · OpenRank ${F(rows.reduce((s, r) => s + (r.value || 0), 0))}`;
    setChart(
      "al-category-rank",
      bars(rows),
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
      `${scopeName()} · ${D.months[state.month]} · 位次变化以相邻月为参照，受观测覆盖影响；环比只使用两月共同有值项目。`,
    );
    let history = D.months.map((_, i) => M.categories(state.scope, i)),
      hr = rows.map((r) => ({
        key: r.key,
        name: r.name,
        values: history.map((h) => {
          let a = h.find((x) => x.key === r.key);
          return a[
            state.heat === "rank"
              ? "rank"
              : state.heat === "share"
                ? "share"
                : "value"
          ];
        }),
        coverages: history.map((h) => {
          let a = h.find((x) => x.key === r.key);
          return `${a.coverage}/${a.count}`;
        }),
      }));
    setChart(
      "al-category-heat",
      heat(hr, D.months, { mode: state.heat }),
      history.flatMap((hh, i) =>
        hh.map((r) => ({
          月份: D.months[i],
          子类别: r.name,
          位次: r.rank,
          OpenRank: r.value,
          份额: pct(r.share),
          观测覆盖: `${r.coverage}/${r.count}`,
        })),
      ),
      `${scopeName()} · 2025-09—2026-08 · 行顺序按当前月份排列，单元格位次每月独立计算；悬停或聚焦查看精确值与覆盖。`,
      false,
      null,
      "2025-09—2026-08",
    );
  }
  function renderProjects() {
    const name = D.sections[state.category].name,
      history = D.months.map((_, i) =>
        M.categories(state.scope, i).find((r) => r.key === state.category),
      );
    setChart(
      "al-category-trend",
      lines(
        [
          {
            name,
            values: history.map((r) =>
              state.categoryMode === "share" ? r.share : r.value,
            ),
          },
        ],
        { percent: state.categoryMode === "share" },
      ),
      history.map((r, i) => ({
        月份: D.months[i],
        子类别: name,
        OpenRank: r.value,
        领域份额: pct(r.share),
        有观测: r.coverage,
        项目数: r.count,
      })),
      `${name} · 份额分母：${scopeName()}当月全部有值项目。`,
      false,
      name,
      "2025-09—2026-08",
    );
    const rows = M.projectRows(state.scope, state.category, state.month),
      show = state.limit === "all" ? rows : rows.slice(0, 10);
    setChart(
      "al-project-rank",
      bars(show, { attr: "data-project", rightLabel: "", heightRows: 16 }),
      rows.map((r) => ({
        位次: r.rank,
        项目: r.name,
        仓库: r.repo,
        OpenRank: r.value,
        类内份额: pct(r.share),
        环比: pct(r.change),
        状态: r.state,
      })),
      `${name} · ${D.months[state.month]} · ${rows.filter((r) => r.value !== null).length}/${rows.length} 有值 · 当前显示 ${show.length} 项；完整记录保留全部项目。`,
      false,
      name,
    );
    $("al-project-picks").innerHTML = rows
      .map(
        (r) =>
          `<label><input type="checkbox" value="${E(r.key)}" ${state.picks.includes(r.key) ? "checked" : ""}>${E(r.name)}</label>`,
      )
      .join("");
    $("al-project-picks").hidden = state.projectView === "rank";
    $("al-project-picks")
      .querySelectorAll("input")
      .forEach(
        (n) =>
          (n.onchange = () => {
            if (n.checked) {
              if (state.picks.length >= 5) {
                n.checked = false;
                $("al-project-trend").querySelector(".al-readout").textContent =
                  "最多同时比较 5 个项目，请先取消一个项目。";
                return;
              }
              state.picks.push(n.value);
            } else state.picks = state.picks.filter((x) => x !== n.value);
            renderProjectTrend();
          }),
      );
    renderProjectTrend();
  }
  function renderProjectTrend() {
    const pp = M.projects(state.scope).filter(
        (p) => p.section === state.category,
      ),
      name = D.sections[state.category].name,
      rows = pp.flatMap((p) =>
        D.months.map((m, i) => ({
          月份: m,
          项目: p.name,
          OpenRank: M.value(p, i),
          位次: M.projectRows(state.scope, state.category, i).find(
            (r) => r.key === p.id,
          ).rank,
          状态: M.status(p, i),
          曲线已选: state.picks.includes(p.id) ? "是" : "否",
        })),
      );
    let graph;
    if (state.projectView === "rank") {
      const rr = M.projectRows(state.scope, state.category, state.month).map(
        (p) => ({
          key: p.key,
          name: p.name,
          values: D.months.map(
            (_, i) =>
              M.projectRows(state.scope, state.category, i).find(
                (r) => r.key === p.key,
              ).rank,
          ),
        }),
      );
      graph = heat(rr, D.months, { project: true });
    } else {
      let ss = state.picks
        .map((id) => P.find((p) => p.id === id))
        .map((p) => ({ name: p.name, values: p.trend }));
      graph = ss.length
        ? lines(ss, { height: 559 })
        : '<p class="al-empty">请选择 1—5 个项目查看趋势。</p>';
    }
    setChart(
      "al-project-trend",
      graph,
      rows,
      `${name} · 2025-09—2026-08 · ${state.projectView === "rank" ? "每个月在全部有观测的类内项目中重新计算位次。" : "已选 " + state.picks.length + " 个项目；对比选择保留，切换类别时重置。"} 空值状态见完整记录。`,
      false,
      name,
      "2025-09—2026-08",
    );
  }
  function countryMap(rows) {
    const W = 1400,
      H = 620,
      max = Math.max(...rows.map((r) => r.share), 0.01);
    let b =
      text(16, 30, "贡献份额 · 模拟", 'font-size="22" font-weight="650"') +
      text(
        920,
        30,
        "国家 / 去重开发者 / 贡献量 / 份额",
        'font-size="18" fill="var(--gv-muted)"',
      );
    b += '<g transform="translate(12,65)">';
    D.world.forEach((f) => {
      let r = rows.find((c) => c.code === f.code),
        q = r ? r.share / max : 0,
        selected = r && r.code === state.country,
        fill = r ? "#3987b0" : "var(--gv-empty)",
        alpha = r ? 0.2 + 0.8 * q : 1;
      let path = `<path d="${f.d}" fill="${fill}" fill-opacity="${alpha}" stroke="${selected ? "var(--gv-goldDisplay)" : "var(--gv-line)"}" stroke-width="${selected ? 2 : 0.5}"/>`;
      b += r
        ? mark(
            `data-country="${r.code}"`,
            `${r.name} · 模拟贡献份额 ${pct(r.share)}`,
            path,
          )
        : path;
    });
    b += "</g>";
    rows.forEach((r, i) => {
      let y = 72 + i * 48,
        sel = r.code === state.country;
      let row =
        `<rect x="910" y="${y - 24}" width="478" height="44" rx="5" fill="${sel ? "var(--gv-raised)" : "transparent"}" stroke="${sel ? "var(--gv-goldDisplay)" : "transparent"}"/>` +
        text(925, y + 3, `${i + 1} ${r.name}`, 'font-size="20"') +
        text(
          1125,
          y + 3,
          F(r.developers, 0),
          'font-size="19" text-anchor="end"',
        ) +
        text(1250, y + 3, F(r.value, 0), 'font-size="19" text-anchor="end"') +
        text(1370, y + 3, pct(r.share), 'font-size="19" text-anchor="end"');
      b += mark(`data-country="${r.code}"`, r.name + " " + pct(r.share), row);
    });
    b +=
      text(
        20,
        540,
        "浅 → 深：贡献份额由低到高；金色边界为所选国家。",
        'font-size="18"',
      ) +
      text(
        20,
        570,
        "灰色：未单列数值；其他与未知仅在榜单中列出。",
        'font-size="17" fill="var(--gv-muted)"',
      ) +
      text(
        20,
        604,
        "SIM-341 · 独立模拟数据，不表示真实国家格局。",
        'font-size="17" fill="var(--gv-muted)"',
      );
    return svg(W, H, b, "模拟国家贡献地图与排行");
  }
  function countryStacks() {
    const ss = M.sections(state.scope),
      H = 130 + 25 * 31,
      L = 290,
      W = 1280,
      bw = 930;
    let b = "";
    D.countries.forEach((c, i) => {
      let x = 15 + (i % 5) * 245,
        y = 22 + Math.floor(i / 5) * 28;
      b +=
        `<rect x="${x}" y="${y - 12}" width="15" height="15" fill="${c.color}"/>` +
        text(x + 22, y + 1, c.name, 'font-size="17"');
    });
    let records = [];
    ss.forEach((key, i) => {
      const rr = M.country(state.scope, key, state.period, state.month);
      let x = L,
        y = 94 + i * 31,
        body = text(12, y + 18, D.sections[key].name, 'font-size="18"');
      D.countries.forEach((c) => {
        const r = rr.find((a) => a.code === c.code),
          w = r.share * bw;
        body += `<rect x="${x}" y="${y}" width="${w}" height="24" fill="${c.color}"><title>${E(r.name)} ${pct(r.share)}</title></rect>`;
        if (w > 70)
          body += text(
            x + w / 2,
            y + 17,
            F(r.share * 100, 0) + "%",
            `font-size="14" text-anchor="middle" fill="${contrastInk(c.color)}"`,
          );
        x += w;
        records.push({
          子类别: D.sections[key].name,
          国家: r.name,
          贡献量: r.value,
          类内份额: pct(r.share),
          类内开发者: r.developers,
        });
      });
      b += mark(
        `data-category="${E(key)}"`,
        D.sections[key].name + "，查看国家排行",
        body,
      );
    });
    return { graph: svg(W, H, b, "各子类别模拟国家贡献结构"), rows: records };
  }
  function renderCountry() {
    const rows = M.country(
        state.scope,
        state.countryScope,
        state.period,
        state.month,
      ),
      whole = M.country(state.scope, "all", state.period, state.month);
    setChart(
      "al-country-rank",
      countryMap(rows),
      rows.map((r) => ({
        国家: r.name,
        去重开发者: r.developers,
        模拟贡献量: r.value,
        当前范围份额: pct(r.share),
        当前领域总份额: pct(whole.find((c) => c.code === r.code).share),
      })),
      `${countryScopeName()} · ${periodName()} · 模拟贡献量与真实 OpenRank 独立；人数在当前范围与统计期内去重。`,
      true,
    );
    let cc = M.countryCategories(
        state.scope,
        state.country,
        state.period,
        state.month,
      ),
      cn = D.countries.find((c) => c.code === state.country).name;
    setChart(
      "al-country-detail",
      bars(
        cc.map((r) => ({ ...r, value: r.share })),
        {
          kind: "share",
          label: "占该国在当前领域全部贡献的份额",
          rightLabel: "",
        },
      ),
      cc.map((r) => ({
        子类别: r.name,
        模拟贡献量: r.value,
        该国贡献分布: pct(r.share),
        该类中国家份额: pct(r.categoryShare),
        类内去重开发者: r.developers,
      })),
      `${cn} · ${scopeName()}全部类别 · ${periodName()} · 类别人数不可直接相加。`,
      true,
      `${cn} / ${scopeName()}`,
    );
    const stack = countryStacks();
    setChart(
      "al-country-stack",
      stack.graph,
      stack.rows,
      `${scopeName()} · ${periodName()} · 固定国家颜色；每个类别的全部贡献（包括其他与未知）合计 100%。`,
      true,
      scopeName(),
    );
    renderSpecialization();
    renderCountryTrend();
  }
  function renderConcentration() {
    const rr = M.concentration(state.scope, state.month);
    setChart(
      "al-concentration",
      bars(rr, {
        kind: "share",
        max: 1,
        label: "Top 3 / 该类有观测项目 OpenRank",
      }),
      rr.map((r) => ({
        子类别: r.name,
        Top3占比: pct(r.value),
        项目数: r.count,
        有观测: r.coverage,
        OpenRank合计: r.openrank,
      })),
      `${scopeName()} · ${D.months[state.month]} · 仅在有观测项目中计算。项目少于 3 个的类别，集中度为 100% 并不等于异常。`,
    );
  }
  function renderShift() {
    const rr = M.shift(state.scope, state.start, state.end);
    setChart(
      "al-shift",
      bars(rr, {
        kind: "pp",
        diverging: true,
        label: "领域份额变化（百分点）",
        rightLabel: "共同样本项目数",
      }),
      rr.map((r) => ({
        子类别: r.name,
        共同样本项目数: r.count,
        起点份额: pct(r.before),
        终点份额: pct(r.after),
        变化百分点: r.value === null ? null : r.value * 100,
        整个领域共同样本: r.cohort,
      })),
      `${scopeName()} · ${D.months[state.start]} → ${D.months[state.end]} · ${rr[0]?.cohort || 0} 个项目在区间每个月都有观测；分母仅为这组共同样本。`,
      false,
      scopeName(),
      `${D.months[state.start]}—${D.months[state.end]}`,
    );
  }
  function renderSpecialization() {
    const ss = M.sections(state.scope),
      whole = M.country(state.scope, "all", state.period, state.month),
      W = 1280,
      L = 290,
      cw = 102,
      H = 95 + 25 * 29;
    let b = "";
    D.countries.forEach(
      (c, j) =>
        (b += text(
          L + j * cw + cw / 2,
          30,
          c.name,
          'font-size="17" text-anchor="middle"',
        )),
    );
    let records = [];
    ss.forEach((key, i) => {
      let y = 46 + i * 29,
        rr = M.country(state.scope, key, state.period, state.month);
      b += mark(
        `data-category="${E(key)}"`,
        D.sections[key].name,
        text(12, y + 19, D.sections[key].name, 'font-size="18"'),
      );
      D.countries.forEach((c, j) => {
        let r = rr.find((x) => x.code === c.code),
          den = whole.find((x) => x.code === c.code).share,
          lq = den ? r.share / den : null,
          alpha =
            lq === null ? 0 : Math.min(0.85, 0.12 + Math.abs(lq - 1) * 0.5),
          cell = shade(alpha, lq >= 1 ? [0, 125, 135] : [197, 132, 82]);
        b += `<g tabindex="0"><title>${E(r.name + " / " + D.sections[key].name)}：LQ ${F(lq)}</title><rect x="${L + j * cw}" y="${y}" width="${cw - 3}" height="26" rx="3" fill="${cell}"/>${text(L + j * cw + cw / 2, y + 19, F(lq), `text-anchor="middle" font-size="16" fill="${contrastInk(cell)}"`)}</g>`;
        records.push({
          子类别: D.sections[key].name,
          国家: c.name,
          类内贡献份额: pct(r.share),
          领域贡献份额: pct(den),
          LQ: lq,
        });
      });
    });
    setChart(
      "al-specialization",
      svg(W, H, b, "模拟国家技术专长 LQ"),
      records,
      `${scopeName()} · ${periodName()} · 蓝色 ≥ 1、橙色 < 1；其他和未知仍纳入分母，其 LQ 不解释为国家专长。`,
      true,
      scopeName(),
    );
  }
  function renderCountryTrend() {
    const all = D.months.map((_, i) =>
        M.country(state.scope, state.countryScope, "month", i),
      ),
      ss = D.countries.map((c) => ({
        name: c.name,
        color: c.color,
        values: all.map((rr) => rr.find((x) => x.code === c.code).share),
      }));
    setChart(
      "al-country-trend",
      lines(ss, { percent: true, label: "模拟月度国家贡献份额" }),
      all.flatMap((rr, i) =>
        rr.map((r) => ({
          月份: D.months[i],
          国家: r.name,
          贡献份额: pct(r.share),
          模拟贡献量: r.value,
          月内去重开发者: r.developers,
        })),
      ),
      `${countryScopeName()} · 2025-09—2026-08 · 每月分母包含所有国家、其他与未知。`,
      true,
      countryScopeName(),
      "2025-09—2026-08",
    );
  }
  function projectDialog(id) {
    const p = P.find((x) => x.id === id);
    if (!p) return;
    const d = $("al-project-dialog"),
      r = M.projectRows(p.layer, p.section, state.month).find(
        (x) => x.key === id,
      );
    $("al-project-detail").innerHTML =
      `<span class="eyebrow">${E(D.sections[p.section].name)} / ${E(p.layer)}</span><h3 id="al-dialog-title">${E(p.name)}</h3><p><a href="https://github.com/${E(p.repo)}" target="_blank" rel="noopener">${E(p.repo)} ↗</a></p><p>${E(p.description)}</p><div class="al-dialog-metrics"><div><b>${F(r.value)}</b><span>${D.months[state.month]} OpenRank</span></div><div><b>${r.rank ?? "—"}</b><span>类别内位次 · ${E(r.state)}</span></div><div><b>${pct(r.share)}</b><span>类别内份额</span></div></div><div class="al-view">${lines([{ name: p.name, values: p.trend }])}</div><p>创建于 ${E(p.created.slice(0, 10))} · 许可证元数据 ${E(p.license || "未标注")} · ${E(p.language)}</p><details><summary>选入理由与来源</summary><p>${E(p.reason)}</p><p>${E(p.caveat)}</p><a href="${E(D.source)}">固定版本主表 ↗</a><p>NOASSERTION 表示元数据未给出明确标识，不是许可结论。创建前与无观测月份均留空。</p></details>${tableHTML(
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
      meta = ["数据性质", "范围", "统计期", "来源或生成规则"];
    let rows = [
      headers.concat(meta),
      ...d.rows.map((r) =>
        headers
          .map((k) => r[k])
          .concat([
            d.sim ? "模拟数据" : "真实观测",
            d.scope,
            d.period,
            d.sim ? "SIM-341 / independent synthetic contributions" : D.source,
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
    let note = `${d.sim ? "模拟数据 · 不用于事实判断" : "真实观测"} | ${d.scope} | ${d.period}`;
    let result = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h + 130}" font-family="Noto Sans CJK SC,Microsoft YaHei,sans-serif" fill="${style.getPropertyValue("--gv-ink").trim() || "#173b50"}"><rect width="${w}" height="${h + 130}" fill="${style.getPropertyValue("--gv-surface").trim() || "#fff"}"/>${text(16, 32, title, 'font-size="24" font-weight="700"')}${text(16, 62, note, 'font-size="17"')}<g transform="translate(0,80)">${content}</g>${text(16, h + 110, d.sim ? "SIM-341 · 固定种子模拟，人数按模拟身份去重。" : "来源：antgroup/agentic-ai-landscape @ " + D.commit.slice(0, 7) + " · 空值不补零", 'font-size="14"')}</svg>`;
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
  document.querySelectorAll("[data-zoom]").forEach(
    (s) =>
      (s.onchange = () => {
        const v = $(s.dataset.zoom).querySelector(".al-view svg");
        v.style.width = Number(s.value) * 100 + "%";
        v.style.maxWidth = "none";
      }),
  );
  document.querySelectorAll("[data-search]").forEach(
    (input) =>
      (input.oninput = () => {
        const el = $(input.dataset.search),
          q = input.value.trim().toLowerCase();
        let count = 0;
        el.querySelectorAll("[data-project]").forEach((n) => {
          const p = P.find((x) => x.id === n.dataset.project),
            hit = !q || (p.name + " " + p.repo).toLowerCase().includes(q);
          n.classList.toggle("al-dim", !hit);
          if (hit) count++;
        });
        el.querySelector(".al-readout").textContent = q
          ? `找到 ${count} 个匹配项目；全景结构与统计分母保持不变。`
          : "已显示全部项目。";
      }),
  );
  $("al-scope").onchange = (e) => {
    state.scope = e.target.value;
    const ss = M.sections(state.scope);
    if (!ss.includes(state.category)) state.category = ss[0];
    state.countryScope = "all";
    categoryOptions();
    resetPicks();
    renderAll();
  };
  $("al-month").onchange = (e) => {
    state.month = Number(e.target.value);
    renderAll();
  };
  $("al-category").onchange = (e) => chooseCategory(e.target.value);
  $("al-country-scope").onchange = (e) => {
    state.countryScope = e.target.value;
    if (state.countryScope !== "all") {
      state.category = state.countryScope;
      $("al-category").value = state.category;
      resetPicks();
      renderProjects();
    }
    renderCountry();
  };
  $("al-country-period").onchange = (e) => {
    state.period = e.target.value;
    renderCountry();
  };
  $("al-heat-mode").onchange = (e) => {
    state.heat = e.target.value;
    renderCategories();
  };
  $("al-category-mode").onchange = (e) => {
    state.categoryMode = e.target.value;
    renderProjects();
  };
  $("al-project-limit").onchange = (e) => {
    state.limit = e.target.value;
    renderProjects();
  };
  $("al-project-view").onchange = (e) => {
    state.projectView = e.target.value;
    renderProjects();
  };
  $("al-shift-start").value = "8";
  $("al-shift-end").value = "11";
  function changeWindow() {
    state.start = Number($("al-shift-start").value);
    state.end = Number($("al-shift-end").value);
    if (state.end <= state.start) {
      state.end = state.start + 1;
      $("al-shift-end").value = String(state.end);
    }
    renderShift();
  }
  $("al-shift-start").onchange = changeWindow;
  $("al-shift-end").onchange = () => {
    state.end = Number($("al-shift-end").value);
    if (state.end <= state.start) {
      state.start = state.end - 1;
      $("al-shift-start").value = String(state.start);
    }
    renderShift();
  };
  function renderAll() {
    renderMaps();
    renderCategories();
    renderProjects();
    renderCountry();
    renderConcentration();
    renderShift();
  }
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
  categoryOptions();
  resetPicks();
  renderAll();
})();
