#!/usr/bin/env python3
"""
fetch_lfx_data.py — 抓取 LFX Insights（https://insights.linuxfoundation.org）项目数据

LFX Insights 前端调用公开 JSON API：{api}/api/widget/<类别>/<指标>
本脚本抓取指定项目的贡献者类指标快照，保存为 JSON。

用法：
  python scripts/fetch_lfx_data.py <project-slug> [输出目录]
示例：
  python scripts/fetch_lfx_data.py korg
  python scripts/fetch_lfx_data.py korg data/raw/2026/external/lfx

注意：
- 贡献计数为 GrimoireLab 口径的"贡献活动数"（commit/issue/PR 等行为计数），
  与 OpenDigger 的 OpenRank 不同源，报告中引用需注明口径。
- 留存(retention)等接口需要额外时间参数，本脚本仅抓取免参可用的端点。
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

API = "https://insights.linuxfoundation.org/api"

# 贡献者类免参可用端点（activity-types 另附查询参数）
ENDPOINTS = {
    "contributor-leaderboard": "contributors/contributor-leaderboard?limit=100&includeCollaborations=false",
    "organization-leaderboard": "contributors/organization-leaderboard?limit=100&includeCollaborations=false",
    "active-contributors": "contributors/active-contributors",
    "active-organizations": "contributors/active-organizations",
    "geographical-distribution": "contributors/geographical-distribution?includeCollaborations=false",
    "contributor-dependency": "contributors/contributor-dependency?includeCollaborations=false",
    "organization-dependency": "contributors/organization-dependency?includeCollaborations=false",
    "activity-types": "contributors/activity-types?includeCollaborations=false",
}


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "open-source-report-data-pipeline/1.0",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python fetch_lfx_data.py <project-slug> [输出目录]")
        return 2
    slug = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        "data", "raw", str(datetime.now().year), "external", f"lfx-{slug}")

    os.makedirs(out_dir, exist_ok=True)
    manifest = []
    for name, ep in ENDPOINTS.items():
        url = f"{API}/widget/{ep}&project={slug}" if "?" in ep else f"{API}/widget/{ep}?project={slug}"
        try:
            data = fetch(url)
        except Exception as e:  # noqa: BLE001 - 记录失败端点继续抓取
            print(f"  !! {name}: {e}")
            manifest.append({"file": f"{name}.json", "status": "failed", "error": str(e)})
            continue
        with open(os.path.join(out_dir, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        size = os.path.getsize(os.path.join(out_dir, f"{name}.json"))
        print(f"  ok {name}: {size} bytes")
        manifest.append({"file": f"{name}.json", "status": "ok", "endpoint": f"/api/widget/{ep}", "bytes": size})

    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"source": "https://insights.linuxfoundation.org",
                   "project": slug, "exported_at": datetime.now(timezone.utc).isoformat(),
                   "endpoints": manifest}, f, ensure_ascii=False, indent=2)
    print("DONE ->", out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
