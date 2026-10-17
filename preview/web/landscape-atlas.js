/* Architectural plates for 4.1-01/02. All figures and data outside the atlas stay independent. */
(function (root) {
  "use strict";
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
  const T = (x, y, s, a = "") => `<text x="${x}" y="${y}" ${a}>${E(s)}</text>`;
  const F = (v, d = 1) =>
    v === null || v === undefined
      ? "—"
      : Number(v).toLocaleString("zh-CN", { maximumFractionDigits: d });
  const BUTTON = (a, v, label, x, y, w = 144) =>
    `<g role="button" tabindex="0" data-atlas-command="${a}" data-value="${E(v)}" aria-label="${E(label)}"><rect x="${x}" y="${y}" width="${w}" height="25" rx="5" fill="var(--gv-surface)" stroke="var(--atlas-line)"/>${T(x + w / 2, y + 17, label, 'text-anchor="middle" font-size="13" fill="var(--atlas-accent)" font-weight="650"')}</g>`;
  const ROUTES = {
    "Agent Infra": [
      {
        id: "all",
        name: "完整全景",
        description:
          "从任务入口向下看：构建与编排，再到执行时需要的知识、工具与环境。",
        keys: [],
      },
      {
        id: "coding",
        name: "构建编码助手",
        description: "从编码入口理解工作流、框架、工具与隔离环境如何分工。",
        keys: [
          "Agentic coding",
          "Coding workflows & harnesses",
          "Code-first frameworks",
          "Tools, web & computer use",
          "Development sandboxes",
          "Observability & evaluation",
        ],
      },
      {
        id: "knowledge",
        name: "构建知识助手",
        description:
          "从助手与对话入口理解：框架组织任务，知识与记忆维持上下文。",
        keys: [
          "Personal AI assistants",
          "Chatbot workspaces",
          "Workflow & agent builders",
          "Code-first frameworks",
          "Memory, knowledge & context",
          "Observability & evaluation",
        ],
      },
      {
        id: "execution",
        name: "让 Agent 执行任务",
        description:
          "从编排到工具执行：协议连接能力，沙箱提供执行环境，观测记录过程。",
        keys: [
          "Multi-agent orchestration",
          "Workflow & agent builders",
          "Protocols & interoperability",
          "Tools, web & computer use",
          "Development sandboxes",
          "Observability & evaluation",
        ],
      },
    ],
    "Model Infra": [
      {
        id: "all",
        name: "完整全景",
        description:
          "从算力与数据向上看：训练形成模型能力，后训练做适配，服务层对外提供调用。",
        keys: [],
      },
      {
        id: "training",
        name: "训练一个模型",
        description:
          "沿数据、计算、训练与后训练理解各模块的职责；实际方案可选用不同模块。",
        keys: [
          "Compute & scheduling",
          "Data · Labeling",
          "Data · Integration",
          "Data · Governance",
          "Pre-Train · Framework & parallel",
          "Pre-Train · Compiler & accelerator",
          "Pre-Train · Evaluation & observability",
          "Post-Train · RL & environments",
          "Post-Train · Supervised fine-tuning",
        ],
      },
      {
        id: "serving",
        name: "部署一个模型",
        description:
          "从资源调度、计算加速到推理、部署与模型接入，观察服务侧的分工。",
        keys: [
          "Compute & scheduling",
          "Pre-Train · Compiler & accelerator",
          "Serving · Inference",
          "Serving · Deploy",
          "Model API gateways",
        ],
      },
      {
        id: "robotics",
        name: "构建具身应用",
        description:
          "结合数据、训练与交互环境，观察机器人基础设施在模型栈中的位置。",
        keys: [
          "Compute & scheduling",
          "Data · Labeling",
          "Data · Integration",
          "Pre-Train · Framework & parallel",
          "Pre-Train · Robotics infra",
          "Post-Train · RL & environments",
          "Serving · Inference",
        ],
      },
    ],
  };
  function boot({ D, M, register, openProject }) {
    for (const [id, layer] of [
      ["al-agent", "Agent Infra"],
      ["al-model", "Model Infra"],
    ]) {
      const panel = document.getElementById(id);
      if (!panel || panel.dataset.atlasReady) continue;
      panel.dataset.atlasReady = "true";
      const svg = panel.querySelector(".atlas-svg"),
        board = svg.querySelector(".atlas-board"),
        inspector = svg.querySelector(".atlas-inspector");
      const pp = M.projects(layer),
        LAST = D.months.length - 1;
      const c = {
        month: LAST,
        lens: "structure",
        route: "all",
        section: null,
        project: null,
        query: "",
        zoom: false,
      };
      const routes = ROUTES[layer],
        cards = [...svg.querySelectorAll("[data-atlas-section]")],
        tiles = [...svg.querySelectorAll("[data-atlas-project]")];
      const input = panel.querySelector("[data-atlas-search]"),
        month = panel.querySelector("[data-atlas-month]");
      const routeHost = panel.querySelector(".atlas-routes");
      routeHost.innerHTML =
        "<span>场景聚焦</span>" +
        routes
          .map(
            (r) =>
              `<button type="button" data-atlas-route="${r.id}" aria-pressed="${r.id === "all"}">${r.name}</button>`,
          )
          .join("");
      routeHost.append(panel.querySelector(".al-chart-tools"));
      const catname = (k) => D.sections[k].name;
      const currentRoute = () => routes.find((r) => r.id === c.route);
      function trend(values) {
        const x = 840,
          y = 810,
          w = 260,
          h = 46,
          max = Math.max(...values.filter(M.num), 1);
        let path = "",
          connected = false;
        values.forEach((v, i) => {
          if (v === null) {
            connected = false;
            return;
          }
          path += `${connected ? "L" : "M"}${x + (w * i) / (values.length - 1)},${y + h - (h * v) / max}`;
          connected = true;
        });
        return (
          T(
            x,
            y - 9,
            "18 个月 OpenRank",
            'font-size="12" fill="var(--gv-muted)"',
          ) +
          `<path d="M${x},${y + h}H${x + w}" stroke="var(--atlas-line)"/><path d="${path}" fill="none" stroke="var(--atlas-accent)" stroke-width="2"/>` +
          T(
            x,
            y + h + 15,
            D.months[0],
            'font-size="11" fill="var(--gv-muted)"',
          ) +
          T(
            x + w,
            y + h + 15,
            D.months[LAST],
            'font-size="11" text-anchor="end" fill="var(--gv-muted)"',
          ) +
          `<path d="M${x + (w * c.month) / LAST},${y - 1}V${y + h + 2}" stroke="var(--gv-muted)" stroke-dasharray="3 3"/>`
        );
      }
      function zoom() {
        if (c.zoom && c.section) {
          const node = cards.find((g) => g.dataset.atlasSection === c.section);
          const [x, y, w, h] = node.dataset.box.split(" ").map(Number),
            scale = Math.min(1500 / (w + 20), 660 / (h + 20), 3.2);
          board.setAttribute(
            "transform",
            `translate(${824 - (x + w / 2) * scale} ${423 - (y + h / 2) * scale}) scale(${scale})`,
          );
        } else board.removeAttribute("transform");
      }
      function selectSection(key) {
        if (currentRoute().keys.length && !currentRoute().keys.includes(key))
          c.route = "all";
        c.query = "";
        input.value = "";
        c.section = c.section === key && !c.project ? null : key;
        c.project = null;
        c.zoom = false;
        render();
      }
      function selectProject(id) {
        const p = pp.find((x) => x.id === id);
        if (!p) return;
        if (
          currentRoute().keys.length &&
          !currentRoute().keys.includes(p.section)
        )
          c.route = "all";
        c.query = "";
        input.value = "";
        c.section = p.section;
        c.project = id;
        render();
      }
      function command(action, value) {
        if (action === "reset") {
          c.section = null;
          c.project = null;
          c.zoom = false;
          c.query = "";
          c.route = "all";
          input.value = "";
        }
        if (action === "zoom") c.zoom = !c.zoom;
        if (action === "project") return selectProject(value);
        if (action === "more") return openProject(c.project, c.month);
        render();
      }
      function bindButtons(nodes, callback) {
        nodes.forEach((n) => {
          n.onclick = (e) => {
            e?.preventDefault();
            callback(n);
          };
          n.onkeydown = (e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              callback(n);
            }
          };
        });
      }
      bindButtons([...svg.querySelectorAll("[data-atlas-category]")], (n) =>
        selectSection(n.dataset.atlasCategory),
      );
      svg.querySelectorAll("[data-atlas-category]").forEach(
        (n) =>
          (n.ondblclick = (e) => {
            e.preventDefault();
            c.section = n.dataset.atlasCategory;
            c.project = null;
            c.zoom = true;
            render();
          }),
      );
      bindButtons(tiles, (n) => selectProject(n.dataset.atlasProject));
      function detail(rows, scopeProjects) {
        const p = pp.find((x) => x.id === c.project),
          r = rows.find((x) => x.key === c.section),
          route = currentRoute();
        let title,
          desc,
          sub,
          series,
          value,
          caption,
          second,
          label,
          buttons = "";
        if (p) {
          const pr = M.projectRows(layer, p.section, c.month).find(
            (x) => x.key === p.id,
          );
          title = p.name;
          desc = p.repo + " · " + catname(p.section);
          sub = `${pr.state} · 类内份额 ${pr.share === null ? "—" : F(pr.share * 100) + "%"} · ${p.language || "语言未标注"}`;
          series = p.trend;
          value = pr.value;
          caption = "所选月 OpenRank";
          second = pr.rank === null ? "—" : "#" + pr.rank;
          label = "类内位次";
          buttons += BUTTON("more", "", "完整项目资料 ↗", 1424, 847);
        } else if (r) {
          title = r.name;
          desc = D.sections[c.section].description;
          const top = M.projectRows(layer, c.section, c.month)
            .filter((x) => x.value !== null)
            .slice(0, 3);
          sub = "";
          let x = 84;
          top.forEach((pr, i) => {
            const w = Math.min(226, Math.max(90, pr.name.length * 7 + 26));
            sub += BUTTON("project", pr.key, `${i + 1} ${pr.name}`, x, 846, w);
            x += w + 6;
          });
          series = D.months.map(
            (_, i) =>
              M.categories(layer, i).find((x) => x.key === c.section).value,
          );
          value = r.value;
          caption = `${r.coverage}/${r.count} 项目有值`;
          second = r.rank === null ? "—" : "#" + r.rank;
          label = "本大类位次";
        } else {
          const keys = route.keys.length ? route.keys : M.sections(layer);
          title =
            route.id === "all"
              ? "从结构开始，逐层探索"
              : route.name + " · 功能组合示意";
          desc = route.description;
          sub = `${keys.length} 个模块 · ${scopeProjects.length} 个项目${c.query ? " · 搜索高亮 " + scopeProjects.filter((p) => (p.name + " " + p.repo + " " + catname(p.section)).toLowerCase().includes(c.query)).length + " 项" : ""} · 点击模块或项目，详情将在这里更新。`;
          series = D.months.map((_, i) =>
            scopeProjects.reduce((s, p) => s + (M.value(p, i) || 0), 0),
          );
          value = scopeProjects.reduce(
            (s, p) => s + (M.value(p, c.month) || 0),
            0,
          );
          caption = "关注范围 OpenRank";
          second =
            scopeProjects.filter((p) => M.value(p, c.month) !== null).length +
            "/" +
            scopeProjects.length;
          label = "观测覆盖";
        }
        let out =
          '<rect x="64" y="782" width="1520" height="97" rx="9" fill="var(--atlas-soft)" stroke="var(--atlas-line)"/>';
        const titleSize = Math.min(22, 720 / (title.length * 0.8));
        out += T(84, 810, title, `font-size="${titleSize}" font-weight="700"`);
        // Descriptions are short Chinese role statements or repository identifiers, not raw metadata walls.
        out += T(
          84,
          834,
          desc,
          `font-size="${Math.min(15.5, 720 / Math.max(desc.length * 0.85, 1))}" fill="var(--gv-muted)"`,
        );
        out +=
          c.section && !p
            ? sub
            : T(84, 860, sub, 'font-size="13" fill="var(--gv-muted)"');
        out +=
          trend(series) +
          T(
            1130,
            816,
            F(value),
            'font-size="25" font-weight="700" fill="var(--atlas-accent)"',
          ) +
          T(1130, 840, caption, 'font-size="12" fill="var(--gv-muted)"') +
          T(1290, 816, second, 'font-size="22" font-weight="700"') +
          T(1290, 840, label, 'font-size="12" fill="var(--gv-muted)"');
        out += BUTTON("reset", "", "恢复全景", 1424, 790);
        if (c.section)
          out += BUTTON(
            "zoom",
            "",
            c.zoom ? "返回总览" : "放大这个模块",
            1424,
            818,
          );
        out += buttons;
        const fragment = new window.DOMParser().parseFromString(
          '<svg xmlns="http://www.w3.org/2000/svg">' + out + "</svg>",
          "image/svg+xml",
        );
        inspector.replaceChildren(
          ...Array.from(fragment.documentElement.childNodes).map((n) =>
            document.importNode(n, true),
          ),
        );
        bindButtons(
          [...inspector.querySelectorAll("[data-atlas-command]")],
          (n) => {
            const action = n.dataset.atlasCommand;
            command(action, n.dataset.value);
            if (action !== "more") {
              const next = inspector.querySelector(`[data-atlas-command="${action}"]`) ||
                tiles.find(tile => tile.dataset.atlasProject === c.project) ||
                inspector.querySelector('[data-atlas-command="reset"]');
              next?.focus({ preventScroll: true });
            }
          },
        );
      }
      function render() {
        const rows = M.categories(layer, c.month),
          route = currentRoute(),
          max = Math.max(...pp.map((p) => M.value(p, c.month) || 0), 1);
        const scopeProjects = pp.filter(
          (p) => !route.keys.length || route.keys.includes(p.section),
        );
        let matches = 0;
        for (const g of cards) {
          const key = g.dataset.atlasSection,
            r = rows.find((x) => x.key === key);
          const relevant =
            (!route.keys.length || route.keys.includes(key)) &&
            (!c.section || c.section === key);
          g.setAttribute("opacity", relevant ? "1" : "0.22");
          g.querySelector(".atlas-category-bg").setAttribute(
            "stroke",
            c.section === key ? "var(--atlas-accent)" : "var(--atlas-line)",
          );
          g.querySelector(".atlas-category-bg").setAttribute(
            "stroke-width",
            c.section === key ? "2.5" : "1.2",
          );
          g.querySelector("[data-atlas-category]").setAttribute(
            "aria-pressed",
            String(c.section === key),
          );
          let label =
            c.lens === "structure"
              ? `${r.count} 项`
              : c.lens === "influence"
                ? `OR ${F(r.value)}`
                : r.change === null
                  ? "环比 —"
                  : `${r.change > 0 ? "↑" : r.change < 0 ? "↓" : "→"} ${F(Math.abs(r.change) * 100)}%`;
          if (key === "Compute & scheduling") label = "";
          g.querySelector(".atlas-category-stat").textContent = label;
        }
        for (const g of tiles) {
          const p = pp.find((x) => x.id === g.dataset.atlasProject),
            value = M.value(p, c.month),
            prev = c.month ? M.value(p, c.month - 1) : null;
          const change =
            value !== null && prev !== null && prev !== 0
              ? (value - prev) / prev
              : null;
          const hit =
            !c.query ||
            (p.name + " " + p.repo + " " + catname(p.section))
              .toLowerCase()
              .includes(c.query);
          if (hit) matches++;
          const selected = c.project === p.id;
          g.setAttribute("aria-pressed", String(selected));
          g.setAttribute("opacity", hit ? "1" : "0.14");
          const bg = g.querySelector(".atlas-project-bg");
          let strength = 0,
            tint = "var(--atlas-accent)";
          if (c.lens === "influence" && value !== null)
            strength = 0.06 + (0.3 * Math.log1p(value)) / Math.log1p(max);
          if (c.lens === "change" && change !== null && change !== 0) {
            strength = 0.08 + 0.24 * Math.min(Math.abs(change), 1);
            tint = change >= 0 ? "var(--atlas-up)" : "var(--atlas-down)";
          }
          if (selected) strength = Math.max(strength, 0.19);
          bg.setAttribute("fill", tint);
          bg.setAttribute("fill-opacity", String(strength));
          bg.setAttribute(
            "stroke",
            selected
              ? "var(--gv-goldDisplay)"
              : c.lens !== "structure" && value === null
                ? "var(--gv-muted)"
                : "none",
          );
          bg.setAttribute("stroke-width", selected ? "2.5" : "1");
          bg.setAttribute(
            "stroke-dasharray",
            !selected && value === null ? "3 3" : "none",
          );
          const bar = g.querySelector(".atlas-value-bar");
          bar.setAttribute("fill", tint);
          bar.setAttribute(
            "width",
            c.lens === "influence" && value !== null
              ? String(
                  (Number(bar.dataset.maxWidth) * Math.log1p(value)) /
                    Math.log1p(max),
                )
              : c.lens === "change" && change !== null
                ? String(
                    Number(bar.dataset.maxWidth) *
                      Math.min(Math.abs(change), 1),
                  )
                : "0",
          );
          g.querySelector("title").textContent =
            `${p.name} · ${p.repo}\n${D.months[c.month]} OpenRank ${F(value)} · ${M.status(p, c.month)}\n月环比 ${change === null ? "不可计算" : (change > 0 ? "+" : "") + F(change * 100) + "%"}\n点击查看图内详情`;
        }
        svg.querySelector(".atlas-period").textContent =
          `${D.months[c.month]} · ${c.lens === "structure" ? "固定分类 / 空间位置不随排名变化" : c.lens === "influence" ? "色带强度 = OpenRank（对数刻度）" : "青绿 = 上升 / 橙色 = 下降 / 无色 = 不可比或不变"}`;
        panel
          .querySelectorAll("[data-atlas-lens]")
          .forEach((b) =>
            b.setAttribute(
              "aria-pressed",
              String(b.dataset.atlasLens === c.lens),
            ),
          );
        panel
          .querySelectorAll("[data-atlas-route]")
          .forEach((b) =>
            b.setAttribute(
              "aria-pressed",
              String(b.dataset.atlasRoute === c.route),
            ),
          );
        zoom();
        detail(rows, scopeProjects);
        const attention = [
          route.name,
          c.section ? catname(c.section) : "",
          c.project ? pp.find((p) => p.id === c.project).name : "",
          c.query ? "搜索：" + c.query : "",
          c.zoom ? "模块放大" : "",
          c.lens === "structure"
            ? "技术结构"
            : c.lens === "influence"
              ? "影响力"
              : "月度变化",
        ]
          .filter(Boolean)
          .join(" / ");
        panel.querySelector(".al-readout").textContent =
          `${attention} · ${c.query ? matches + " 个搜索匹配 · " : ""}${D.months[c.month]} · 所有项目保持原位。${c.lens === "change" ? "项目环比要求前后两月都有值且前月非零；模块环比仅用共同有值项目。" : "点击模块或项目可更新图内详情。"}`;
        register(id, {
          rows: pp.map((p) => ({
            类别: catname(p.section),
            项目: p.name,
            仓库: p.repo,
            OpenRank: M.value(p, c.month),
            状态: M.status(p, c.month),
            场景关注:
              !route.keys.length || route.keys.includes(p.section)
                ? "是"
                : "否",
            搜索匹配:
              !c.query ||
              (p.name + " " + p.repo + " " + catname(p.section))
                .toLowerCase()
                .includes(c.query)
                ? "是"
                : "否",
            数据来源: p.observationSources[c.month],
          })),
          sim: false,
          scope: layer,
          period: D.months[c.month],
          attention,
        });
      }
      panel.querySelectorAll("[data-atlas-lens]").forEach(
        (n) =>
          (n.onclick = () => {
            c.lens = n.dataset.atlasLens;
            render();
          }),
      );
      panel.querySelectorAll("[data-atlas-route]").forEach(
        (n) =>
          (n.onclick = () => {
            c.route = n.dataset.atlasRoute;
            c.section = null;
            c.project = null;
            c.zoom = false;
            render();
          }),
      );
      panel.querySelector("[data-atlas-reset]").onclick = () => {
        c.lens = "structure";
        command("reset", "");
      };
      input.oninput = () => {
        c.query = input.value.trim().toLowerCase();
        c.zoom = false;
        c.section = null;
        c.project = null;
        c.route = "all";
        render();
      };
      month.onchange = () => {
        c.month = Number(month.value);
        render();
      };
      render();
    }
  }
  root.LandscapeAtlas = { boot };
})(typeof globalThis !== "undefined" ? globalThis : this);
