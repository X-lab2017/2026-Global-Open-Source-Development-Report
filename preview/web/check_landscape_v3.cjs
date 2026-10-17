/* Numerical regressions: real cohort, missing data, comparable denominators,
   and independent simulated actors. No browser/runtime dependencies. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const makeModel = require("./landscape.js");
const D = JSON.parse(
  fs.readFileSync(
    process.argv[2] || "preview/dist/assets/landscape/v3-data.json",
    "utf8",
  ),
);
const M = makeModel(D),
  near = (a, b, epsilon = 1e-8) =>
    assert(Math.abs(a - b) < epsilon, `${a} != ${b}`);
assert.equal(D.version, "4.1-v3");
assert.equal(D.projects.length, 145);
assert.equal(new Set(D.projects.map((p) => p.id)).size, 145);
assert.equal(M.projects("Agent Infra").length, 86);
assert.equal(M.projects("Model Infra").length, 59);
assert.equal(M.sections("all").length, 25);
assert.equal(M.sections("Agent Infra").length, 12);
assert.equal(M.sections("Model Infra").length, 13);
const coverage = [
  93, 99, 107, 107, 108, 111, 116, 118, 122, 125, 130, 135, 140, 141, 142, 140,
  135, 140,
];
for (let m = 0; m < 18; m++) {
  const rr = M.categories("all", m);
  assert.equal(
    rr.reduce((s, r) => s + r.coverage, 0),
    coverage[m],
  );
  near(
    rr.reduce((s, r) => s + (r.share || 0), 0),
    1,
  );
  near(
    rr.reduce((s, r) => s + (r.value || 0), 0),
    D.projects.reduce((s, p) => s + (p.trend[m] || 0), 0),
  );
  for (const scope of ["all", "Agent Infra", "Model Infra"]) {
    const countries = M.country(scope, "all", "month", m);
    near(
      countries.reduce((s, r) => s + r.share, 0),
      1,
    );
    for (const key of M.sections(scope)) {
      const pp = M.projectRows(scope, key, m),
        expected = D.projects.filter((p) => p.section === key);
      assert.equal(pp.length, expected.length);
      assert(pp.every((p) => p.value !== null || p.rank === null));
      assert(
        pp
          .filter((p) => p.value !== null)
          .every((p, i, a) => i === 0 || a[i - 1].value >= p.value),
      );
      const country = M.country(scope, key, "month", m);
      near(
        country.reduce((s, r) => s + r.share, 0),
        1,
      );
    }
  }
}
near(
  M.categories("all", 17).reduce((s, r) => s + r.value, 0),
  5706.38,
);
near(
  M.categories("Agent Infra", 17).reduce((s, r) => s + r.value, 0),
  3306.63,
);
near(
  M.categories("Model Infra", 17).reduce((s, r) => s + r.value, 0),
  2399.75,
);
const assistants = M.projectRows("all", "Personal AI assistants", 17);
near(
  assistants.reduce((s, r) => s + r.value, 0),
  752.76,
);
near(
  assistants.slice(0, 2).reduce((s, r) => s + r.value, 0),
  581.15,
);
assert(assistants[0].repo.toLowerCase().includes("openclaw"));
const claw = D.projects.find(
  (p) => p.repo.toLowerCase() === "openclaw/openclaw",
);
assert(claw);
assert.equal(M.status(claw, 6), "尚未创建");
assert.equal(
  M.projectRows("all", "Personal AI assistants", 6).find(
    (p) => p.key === claw.id,
  ).rank,
  null,
);
const missing = D.projects.find(
  (p) => p.trend[17] === null && p.created.slice(0, 7) <= "2026-08",
);
assert.equal(M.status(missing, 17), "无观测");
const shifts = M.shift("all", 14, 17);
near(
  shifts.reduce((s, r) => s + (r.value || 0), 0),
  0,
);
const common = D.projects.filter((p) =>
  p.trend.slice(14, 18).every((v) => v !== null),
);
assert.equal(shifts[0].cohort, common.length);
const a = common.reduce((s, p) => s + p.trend[14], 0),
  b = common.reduce((s, p) => s + p.trend[17], 0);
for (const r of shifts) {
  const pp = common.filter((p) => p.section === r.key);
  near(
    r.value,
    pp.reduce((s, p) => s + p.trend[17], 0) / b -
      pp.reduce((s, p) => s + p.trend[14], 0) / a,
  );
}
assert(
  M.concentration("all", 17).every(
    (r) => r.value === null || (r.value > 0 && r.value <= 1.000000001),
  ),
);
const country = M.country("all", "all", "rolling", 17);
near(
  country.reduce((s, r) => s + r.value, 0),
  100000,
);
for (const r of country) {
  const entries = D.simulation.filter(
    (x) => x.country === r.code && x.month >= 6,
  );
  assert.equal(r.developers, new Set(entries.flatMap((x) => x.actors)).size);
  assert(entries.every((x) => x.actors.every((a) => a.startsWith("SIM-"))));
  const cc = M.countryCategories("all", r.code, "rolling", 17);
  near(
    cc.reduce((s, c) => s + c.share, 0),
    1,
  );
  near(
    cc.reduce((s, c) => s + c.value, 0),
    r.value,
  );
}
assert(
  country.some(
    (r) =>
      M.sections("all").reduce(
        (s, k) =>
          s +
          M.country("all", k, "rolling", 17).find((c) => c.code === r.code)
            .developers,
        0,
      ) > r.developers,
  ),
);
const zeros = JSON.parse(JSON.stringify(D));
zeros.projects[0].trend[0] = 0;
zeros.projects[0].trend[1] = null;
const Z = makeModel(zeros);
assert.equal(Z.status(zeros.projects[0], 0), "有观测");
assert.notEqual(Z.status(zeros.projects[0], 1), "有观测");
console.log(
  "PASS 4.1 v3: 145 projects; 25 categories; 18 monthly coverage checks; 5706.38 latest total; dynamic project rankings; zero/missing/creation distinctions; common-cohort shifts; synthetic shares conserved; actor unions deduplicated.",
);

for (const win of [6, 12, 18]) {
  const countries = M.country("all", "all", win, 17);
  near(
    countries.reduce((s, r) => s + r.value, 0),
    (100000 * win) / 12,
  );
  near(
    countries.reduce((s, r) => s + r.share, 0),
    1,
  );
  for (const r of countries) {
    const actors = new Set(
      D.simulation
        .filter((x) => x.country === r.code && x.month >= 18 - win)
        .flatMap((x) => x.actors),
    );
    assert.equal(r.developers, actors.size);
  }
}
assert.equal(D.months[0], "2025-03");
assert.equal(D.months.at(-1), "2026-08");
assert(
  D.projects.every(
    (p) => p.trend.length === 18 && p.observationSources.length === 18,
  ),
);
const path = require("node:path"),
  crypto = require("node:crypto");
const assets = path.dirname(
  process.argv[2] || "preview/dist/assets/landscape/v3-data.json",
);
const manifest = JSON.parse(
  fs.readFileSync(path.join(assets, D.historySnapshot), "utf8"),
);
assert.equal(manifest.files.filter((x) => x.file).length, 144);
for (const item of manifest.files.filter((x) => x.file)) {
  const bytes = fs.readFileSync(
    path.join(assets, "opendigger-20261017", item.file),
  );
  assert.equal(
    crypto.createHash("sha256").update(bytes).digest("hex"),
    item.sha256,
  );
  const history = JSON.parse(bytes),
    p = D.projects.find((x) => x.id === item.repo_id);
  for (let m = 0; m < 6; m++) {
    if (p.observationSources[m] === item.url)
      assert.equal(p.trend[m], history[D.months[m]]);
  }
}
console.log(
  "PASS v3 windows: 6/12/18 month country denominators and actor unions; 144 hashed historical snapshots; real values traceable to source.",
);
