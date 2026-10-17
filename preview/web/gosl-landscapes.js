/* Chapter 4 frameworks: independent controls; existing 4.1 state stays untouched. */
(() => {
  "use strict";
  const payload = document.querySelector("#gosl-data");
  if (!payload) return;
  const data = JSON.parse(payload.textContent);
  const ns = "http://www.w3.org/2000/svg";
  const esc = (s) =>
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
  const number = (n) =>
    n === null || n === undefined
      ? "—"
      : new Intl.NumberFormat("zh-CN", { maximumFractionDigits: 2 }).format(n);
  const width = (s) =>
    [...String(s)].reduce(
      (n, c) =>
        n +
        (c.charCodeAt(0) > 255
          ? 1
          : "MW@#%".includes(c)
            ? 0.82
            : "il.:|!'".includes(c)
              ? 0.29
              : 0.54),
      0,
    );
  const lines = (s, w, size) => {
    const a = [];
    let t = "";
    for (const c of String(s)) {
      if (t && width(t + c) * size > w) {
        a.push(t);
        t = "";
      }
      t += c;
    }
    if (t) a.push(t);
    return a;
  };
  const txt = (x, y, s, size = 16, attrs = "") =>
    `<text x="${x}" y="${y}" font-size="${size}" ${attrs}>${esc(s)}</text>`;
  const multiline = (x, y, s, w, size = 16, attrs = "") =>
    lines(s, w, size)
      .map((t, i) => txt(x, y + i * (size + 5), t, size, attrs))
      .join("");
  const replaceSvg = (node, markup) => {
    const xml = new DOMParser().parseFromString(
      `<svg xmlns="${ns}">${markup}</svg>`,
      "image/svg+xml",
    );
    node.replaceChildren(
      ...Array.from(xml.documentElement.childNodes).map((n) =>
        document.importNode(n, true),
      ),
    );
  };
  const save = (content, type, name) => {
    const u = URL.createObjectURL(new Blob([content], { type }));
    const a = document.createElement("a");
    a.href = u;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(u), 1000);
  };
  const contexts = [];
  data.datasets.forEach((d) => {
    const el = document.querySelector(`[data-gl-plate="${d.id}"]`);
    if (!el) return;
    const svg = el.querySelector(".gl-svg"),
      board = el.querySelector(".gl-board"),
      inspector = el.querySelector(".gl-inspector");
    const defaultInspector = inspector.innerHTML;
    const cats = Object.fromEntries(d.categories.map((c) => [c.id, c]));
    const projects = Object.fromEntries(d.projects.map((p) => [p.id, p]));
    const state = {
      group: "all",
      category: null,
      project: null,
      query: "",
      zoom: false,
      page: 0,
    };
    const catNode = (key) =>
      Array.from(el.querySelectorAll("[data-gl-category]")).find(
        (n) => n.dataset.glCategory === key,
      );
    const matched = (p) =>
      !state.query ||
      [p.repo, p.name, p.owner, ...p.tags.map((k) => cats[k].name)]
        .join(" ")
        .toLocaleLowerCase()
        .includes(state.query);
    function renderTable(all = false) {
      const records = d.projects.filter(matched),
        pages = Math.max(1, Math.ceil(records.length / 8));
      state.page = Math.min(state.page, pages - 1);
      const rows = all
        ? records
        : records.slice(state.page * 8, state.page * 8 + 8);
      el.querySelector(".gl-table-host").innerHTML =
        `<div class="gl-table-scroll"><table><thead><tr><th scope="col">项目 / 模型</th><th scope="col">主展示类别</th><th scope="col">${esc(d.metric)}</th><th scope="col">分类依据</th></tr></thead><tbody>${rows.length ? rows.map((p) => `<tr><td><button data-gl-row="${esc(p.id)}">${esc(p.repo)}</button></td><td>${esc(cats[p.category].name)}</td><td>${number(p.value)}</td><td><a href="${esc(p.classificationSource)}" target="_blank" rel="noopener">${esc(p.classification)} ↗</a>${p.note ? `<small>${esc(p.note)}</small>` : ""}</td></tr>`).join("") : '<tr><td colspan="4">没有匹配记录。清空搜索可查看完整清单。</td></tr>'}</tbody></table></div><div class="gl-table-pager"><span>${records.length} 条${state.query ? "匹配记录" : "记录"} · ${esc(d.period)}</span><div><button data-gl-page="-1" ${!state.page ? "disabled" : ""}>上一页</button><span>${state.page + 1} / ${pages}</span><button data-gl-page="1" ${state.page >= pages - 1 ? "disabled" : ""}>下一页</button></div></div>`;
    }
    function renderInspector() {
      const p = projects[state.project],
        c = cats[state.category];
      const link = el.querySelector("[data-gl-project-link]");
      link.href = p ? p.url : c ? c.source : d.source.url;
      link.textContent = p
        ? "查看项目来源 ↗"
        : c
          ? "查看分类依据 ↗"
          : "查看数据来源 ↗";
      let readout = "点击分区或项目在图内查看详情；所有分类始终保留。";
      if (!c) {
        replaceSvg(inspector, defaultInspector);
      } else {
        const leftTitle = p ? p.repo : c.name;
        let size = 23;
        while (lines(leftTitle, 690, size).length > 2 && size > 15) size--;
        const label = p ? "PROJECT / 项目定位" : "CATEGORY / 技术类别";
        const detail = p ? cats[p.category].name : c.description;
        let mark = p ? number(p.value) : String(c.count);
        let content = `<rect x="24" y="926" width="1552" height="132" rx="5" fill="var(--gv-raised)" stroke="var(--gv-line)"/>${txt(42, 948, label, 11, 'fill="var(--gl-accent)" letter-spacing="1"')}${multiline(42, 976, leftTitle, 690, size, 'font-weight="650"')}${multiline(42, 1030, detail, 700, 13, 'fill="var(--gv-muted)"')}`;
        content += `<path d="M770 945V1040 M1125 945V1040" stroke="var(--gv-line)"/>${txt(795, 950, p ? d.metric : "入库样本", 12, 'fill="var(--gv-muted)"')}${txt(795, 989, mark, 30, 'fill="var(--gl-accent)" font-weight="650"')}${multiline(795, 1016, p ? d.period : "仅计本图主展示类别；可点击项目查看", 300, 12, 'fill="var(--gv-muted)"')}`;
        const labels = p
          ? p.tags.map((k) => cats[k].name).join(" / ")
          : "功能分组供阅读与定位，不代表市场份额";
        content +=
          txt(
            1150,
            950,
            p ? "完整技术标签" : "阅读提示",
            12,
            'fill="var(--gv-muted)"',
          ) + multiline(1150, 976, labels, 400, 14, 'fill="var(--gv-ink)"');
        replaceSvg(inspector, content);
        readout = p
          ? `${p.repo} · ${p.description || ""} ${p.note || ""}｜分类：${p.classification}`
          : `${c.name} · ${c.count} 条样本。${c.description} ${c.count ? "选择项目，查看原始数值与归类说明。" : "当前清单未收录此类项目，欢迎补充一手来源。"}`;
      }
      if (state.query)
        readout = `搜索“${el.querySelector("[data-gl-search]").value}”：${d.projects.filter(matched).length} 条匹配记录。${readout}`;
      el.querySelector(".gl-readout").textContent = readout;
    }
    function update() {
      el.querySelectorAll("[data-gl-focus]").forEach((b) =>
        b.setAttribute(
          "aria-pressed",
          String(b.dataset.glFocus === state.group),
        ),
      );
      el.querySelectorAll("[data-gl-category]").forEach((n) => {
        const activeGroup =
          state.group === "all" || n.dataset.glGroup === state.group;
        const any = d.projects.some(
          (p) => p.category === n.dataset.glCategory && matched(p),
        );
        const dim =
          !activeGroup ||
          (state.category && n.dataset.glCategory !== state.category) ||
          (state.query && !any);
        n.style.opacity = dim ? "0.27" : "1";
        n.classList.toggle(
          "is-selected",
          n.dataset.glCategory === state.category,
        );
        n.querySelector("[data-gl-select-category]").setAttribute(
          "aria-pressed",
          String(n.dataset.glCategory === state.category),
        );
      });
      el.querySelectorAll("[data-gl-project]").forEach((n) => {
        const p = projects[n.dataset.glProject];
        n.style.opacity = matched(p) ? "1" : "0.24";
        n.classList.toggle("is-selected", p.id === state.project);
        n.setAttribute("aria-pressed", String(p.id === state.project));
      });
      const zoom = el.querySelector("[data-gl-zoom]");
      zoom.disabled = !state.category;
      zoom.textContent = state.zoom ? "返回全景" : "放大模块";
      zoom.setAttribute("aria-pressed", String(state.zoom));
      if (state.zoom && state.category) {
        const [x, y, w, h] = catNode(state.category)
          .dataset.box.split(" ")
          .map(Number);
        const scale = Math.min(1510 / w, 785 / h, 2.6),
          tx = 800 - (x + w / 2) * scale,
          ty = 505 - (y + h / 2) * scale;
        board.setAttribute(
          "transform",
          `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${scale.toFixed(4)})`,
        );
      } else board.removeAttribute("transform");
      renderInspector();
      renderTable();
    }
    function selectProject(id) {
      const p = projects[id];
      if (!p) return;
      state.project = id;
      state.category = p.category;
      state.group = "all";
      update();
    }
    el.addEventListener("click", (e) => {
      const b = e.target.closest(
        "button,[data-gl-project],[data-gl-select-category]",
      );
      if (!b) return;
      if (b.hasAttribute("data-gl-focus")) {
        state.group = b.dataset.glFocus;
        state.category = null;
        state.project = null;
        state.zoom = false;
        update();
      }
      if (b.hasAttribute("data-gl-reset")) {
        Object.assign(state, {
          group: "all",
          category: null,
          project: null,
          query: "",
          zoom: false,
          page: 0,
        });
        el.querySelector("[data-gl-search]").value = "";
        update();
      }
      if (b.hasAttribute("data-gl-project")) selectProject(b.dataset.glProject);
      if (b.hasAttribute("data-gl-row")) selectProject(b.dataset.glRow);
      if (b.hasAttribute("data-gl-select-category")) {
        state.category = b.dataset.glSelectCategory;
        state.project = null;
        state.group = "all";
        update();
      }
      if (b.hasAttribute("data-gl-zoom") && state.category) {
        state.zoom = !state.zoom;
        update();
      }
      if (b.hasAttribute("data-gl-page")) {
        state.page += Number(b.dataset.glPage);
        renderTable();
      }
      if (b.hasAttribute("data-gl-csv")) {
        const cell = (v) => '"' + String(v ?? "").replace(/"/g, '""') + '"';
        const rows = [
          [
            "section",
            "repo_or_model",
            "display_category",
            "all_labels",
            "value",
            "metric",
            "period",
            "classification_status",
            "classification_source",
            "notes",
          ],
          ...d.projects.map((p) => [
            d.number,
            p.repo,
            cats[p.category].name,
            p.tags.map((k) => cats[k].name).join(" / "),
            p.value,
            d.metric,
            d.period,
            p.classification,
            p.classificationSource,
            p.note,
          ]),
        ];
        save(
          "\uFEFF" + rows.map((r) => r.map(cell).join(",")).join("\r\n"),
          "text/csv;charset=utf-8",
          `${d.number}-${d.id}-projects.csv`,
        );
      }
      if (b.hasAttribute("data-gl-svg")) exportSvg();
      if (b.hasAttribute("data-gl-full")) openFull(el, d);
    });
    el.addEventListener("keydown", (e) => {
      const node = e.target.closest(
        "[data-gl-project],[data-gl-select-category]",
      );
      if (node && (e.key === "Enter" || e.key === " ")) {
        e.preventDefault();
        node.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      }
    });
    el.querySelector("[data-gl-search]").addEventListener("input", (e) => {
      state.query = e.target.value.trim().toLocaleLowerCase();
      state.page = 0;
      state.category = null;
      state.project = null;
      state.zoom = false;
      state.group = "all";
      update();
    });
    function exportSvg() {
      const clone = svg.cloneNode(true);
      clone.setAttribute("xmlns", ns);
      clone.setAttribute("viewBox", "0 0 1600 1230");
      clone.setAttribute("width", "1600");
      clone.setAttribute("height", "1230");
      clone.setAttribute(
        "font-family",
        "Noto Sans CJK SC,Microsoft YaHei,sans-serif",
      );
      clone.setAttribute("fill", "var(--gv-ink)");
      clone
        .querySelectorAll(
          ".gl-category.is-selected .gl-category-box,.gl-project.is-selected .gl-project-box",
        )
        .forEach((n) => {
          n.setAttribute("stroke", "var(--gl-accent)");
          n.setAttribute("stroke-width", "2");
        });
      const tail = document.createElementNS(ns, "g");
      clone.appendChild(tail);
      const active = state.project
        ? projects[state.project].repo
        : state.category
          ? cats[state.category].name
          : state.group === "all"
            ? "全部结构"
            : d.groups.find((g) => g.id === state.group).name;
      replaceSvg(
        tail,
        `<rect x="0" y="1100" width="1600" height="130" fill="var(--gv-surface)"/>${txt(24, 1125, `${d.number}-01 · ${d.title} · ${active}${state.query ? " · 搜索：" + state.query : ""}`, 15, 'fill="var(--gv-ink)"')}${txt(24, 1154, d.period + " · " + data.version, 13, 'fill="var(--gv-muted)"')}${multiline(24, 1180, "来源：" + d.source.url, 1540, 12, 'fill="var(--gv-muted)"')}`,
      );
      clone
        .querySelectorAll("[tabindex],[role],[aria-pressed]")
        .forEach((n) => {
          n.removeAttribute("tabindex");
          n.removeAttribute("aria-pressed");
        });
      const style = getComputedStyle(el);
      let xml = new XMLSerializer().serializeToString(clone);
      xml = xml.replace(
        /var\((--[\w-]+)\)/g,
        (_, k) => style.getPropertyValue(k).trim() || "#10334D",
      );
      save(
        xml,
        "image/svg+xml;charset=utf-8",
        `${d.number}-${d.id}-${document.documentElement.dataset.theme || "light"}.svg`,
      );
    }
    update();
    contexts.push({ renderTable });
  });
  const modal = document.querySelector("#gl-fullscreen");
  let active = null,
    placeholder = null,
    returnFocus = null;
  function themeLabel() {
    const dark = document.documentElement.dataset.theme === "dark";
    modal.querySelector("[data-gl-theme]").textContent = dark
      ? "切换浅色"
      : "切换深色";
    modal
      .querySelector("[data-gl-theme]")
      .setAttribute("aria-pressed", String(dark));
  }
  function openFull(plate, d) {
    if (active) return;
    returnFocus = document.activeElement;
    placeholder = document.createComment("landscape position");
    plate.before(placeholder);
    active = plate;
    modal.querySelector("strong").textContent =
      `${d.number}-01 / ${d.short}技术全景`;
    document.querySelector("#gl-fullscreen-body").append(plate);
    document.body.classList.add("gl-modal-open");
    themeLabel();
    modal.showModal();
    modal.querySelector("[data-gl-close]").focus();
  }
  function restore() {
    if (!active) return;
    placeholder.replaceWith(active);
    active = null;
    placeholder = null;
    document.body.classList.remove("gl-modal-open");
    returnFocus?.focus();
  }
  modal
    .querySelector("[data-gl-close]")
    .addEventListener("click", () => modal.close());
  modal.addEventListener("close", restore);
  modal
    .querySelector("[data-gl-theme]")
    .addEventListener("click", () =>
      document.querySelector("#theme-toggle")?.click(),
    );
  document.addEventListener("gosdthemechange", themeLabel);
  window.addEventListener("beforeprint", () =>
    contexts.forEach((c) => c.renderTable(true)),
  );
  window.addEventListener("afterprint", () =>
    contexts.forEach((c) => c.renderTable()),
  );
})();
