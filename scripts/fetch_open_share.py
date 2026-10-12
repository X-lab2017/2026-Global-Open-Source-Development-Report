#!/usr/bin/env python3
"""Fetch open-share.com GOSD map data (OpenDigger open-world overview).

Data source: https://open-share.com/insight/open-world/gosd
Endpoints (discovered from the site's frontend bundle):
  - world:   https://selfoss.open-digger.cn/openshare/overview/{metric}.json
  - country: https://selfoss.open-digger.cn/openshare/overview/{CC}/{metric}.json
  - half-year variant: overview_half_year/...
Metrics: developers | contribution | influence
GeoJSON: https://open-share.com/geo/{world|CN|US}.json

Output: data/raw/2026/external/open-share/*.json (one file per view,
named world-{metric}[-half-year].json / {CC}-{metric}.json)
"""
import json
import sys
import urllib.request
from pathlib import Path

BASE = "https://selfoss.open-digger.cn/openshare"
GEO_BASE = "https://open-share.com/geo"
METRICS = ["developers", "contribution", "influence"]
COUNTRIES = ["CN", "US"]  # drill-down enabled on the platform
OUT = Path(__file__).resolve().parent.parent / "data" / "raw" / "2026" / "external" / "open-share"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 gosd-report-fetcher"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = []
    for metric in METRICS:
        jobs.append((f"{BASE}/overview/{metric}.json", f"world-{metric}.json"))
        jobs.append((f"{BASE}/overview_half_year/{metric}.json", f"world-{metric}-half-year.json"))
        for cc in COUNTRIES:
            jobs.append((f"{BASE}/overview/{cc}/{metric}.json", f"{cc}-{metric}.json"))
    ok, fail = 0, 0
    for url, name in jobs:
        try:
            data = fetch(url)
            (OUT / name).write_bytes(data)
            json.loads(data)  # sanity check
            print(f"ok   {name} ({len(data)} bytes)")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {e}", file=sys.stderr)
            fail += 1
    print(f"done: {ok} fetched, {fail} failed -> {OUT}")


if __name__ == "__main__":
    main()
