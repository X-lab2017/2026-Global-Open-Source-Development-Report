"""Reproduce three current 5.1 CSVs and preserve eight prior review CSVs from frozen, explicitly scoped observations."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = Path(__file__).resolve().parents[1] / 'content/gosm'
OUT = ROOT / 'data/processed/chapter5'
NAMES = {
    'panorama': 'fig-5-1-01_supply_panorama',
    'comparison': 'fig-5-1-02_china_us_comparison',
    'geography': 'fig-5-1-03_china_supply_map',
    'world': 'fig-5-1-01_global_supply_snapshot',
    'cnus': 'fig-5-1-02_china_us_supply',
    'publishers': 'fig-5-1-03_china_us_publishers',
    'china': 'fig-5-1-04_china_supply_geography',
    'growth': 'fig-5-1-05_supply_growth',
    'release': 'fig-5-1-06_monthly_release',
    'portfolio': 'fig-5-1-07_publisher_portfolio',
    'scenario': 'fig-5-1-08_supply_scenarios',
}


def text_csv(rows):
    stream = io.StringIO(newline='')
    columns = list(dict.fromkeys(k for row in rows for k in row))
    writer = csv.DictWriter(stream, columns, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue(), columns


def build():
    d = json.loads((CONTENT / 'supply-observation.json').read_text())
    scenarios = json.loads((CONTENT / 'supply-scenarios.json').read_text())
    rows = {k: [] for k in NAMES}
    stamp = dict(data_status='observed', retrieved_at=d['meta']['retrievedAtUTC'],
                 scope='country-linked model-publisher organization cohort', geography_as_of='not_documented')
    for asset, a in d['assets'].items():
        fields = ['organizations', 'activeProviders', asset, 'downloads', 'likes']
        for country in a['countries']:
            record = {**stamp, 'asset': asset, 'country_code': country['code'],
                      'country_name': country['name_zh'], **{k: country.get(k) for k in fields}}
            rows['world'].append(record)
            if country['code'] in ('CN', 'US'):
                for metric in ('activeProviders', asset, 'downloads', 'likes'):
                    value, denominator = country[metric], a['summary'][metric]
                    rows['cnus'].append({**stamp, 'asset': asset, 'country_code': country['code'],
                        'metric': metric, 'value': value, 'cohort_total': denominator,
                        'cohort_share_pct': 100 * value / denominator if denominator else 0})
        for metric in ('organizations', asset, 'downloads', 'likes'):
            assert sum(c[metric] for c in a['countries']) == a['summary'][metric], (asset, metric)
        cn = next(c for c in a['countries'] if c['code'] == 'CN')
        divisions = [r for r in a['divisions'] if r['parent_id'] == ':divisions/CN']
        for province in divisions + [{'code': 'unassigned', 'name_zh': '省级归属待补', **cn['unassignedDivision']}]:
            rows['china'].append({**stamp, 'asset': asset, 'entity_type': 'province',
                'code': province['code'], 'name': province['name_zh'],
                **{k: province.get(k) for k in ('organizations', asset, 'downloads', 'likes')}})
        for metric in ('organizations', asset, 'downloads', 'likes'):
            assert sum(p[metric] for p in divisions) + cn['unassignedDivision'][metric] == cn[metric]
        for code in ('CN', 'US'):
            orgs = [o for o in d['organizationProfiles'] if o['countryCode'] == code]
            summary = next(c for c in a['countries'] if c['code'] == code)
            assert sum(o[asset][asset] > 0 for o in orgs) == summary['activeProviders']
            for metric in (asset, 'downloads', 'likes'):
                assert sum(o[asset][metric] for o in orgs) == summary[metric]
        for org in d['organizationProfiles']:
            if org['countryCode'] in ('CN', 'US'):
                rows['publishers'].append({**stamp, 'asset': asset, 'country_code': org['countryCode'],
                    'publisher': org['name'], **org[asset]})
            if org['countryCode'] == 'CN':
                rows['china'].append({**stamp, 'asset': asset, 'entity_type': 'publisher',
                    'code': org['name'], 'name': org['name'], 'province_codes': ';'.join(org['divisionCodes']) or 'unassigned',
                    'organizations': 1, **org[asset]})
        for r in d['global'][asset]['monthlyNew']:
            rows['growth'].append({'data_status': 'observed', 'series': 'monthly_new', 'asset': asset,
                'period': r['month'], 'value': r['count'], 'snapshot': d['meta']['retrievedAtUTC'],
                'scope': 'platform monthly summary; latest available month 2026-07'})
    with (OUT / 'fig-5-1-1_hf_cumulative_models_publishers.csv').open() as f:
        annual = list(csv.DictReader(f))
    for r in annual:
        rows['growth'].append({'data_status': 'observed', 'series': 'annual_retrospective',
            'snapshot': '2026-09-13', 'scope': 'visible-at-snapshot creation-time retrospective', **r})
    with (OUT / 'fig-5-1-3_country_monthly_new_models.csv').open() as f:
        for r in csv.DictReader(f):
            rows['release'].append({'data_status': 'observed', 'snapshot': '2026-09-13',
                'scope': 'original report four-country monthly retrospective', **r})
    for org in d['organizationProfiles']:
        rows['portfolio'].append({**stamp, 'publisher': org['name'], 'country_code': org['countryCode'],
            'province_codes': ';'.join(org['divisionCodes']),
            **{f'{asset}_{metric}': value for asset in ('models', 'datasets') for metric, value in org[asset].items()}})
    for preset, percentages in scenarios['presets'].items():
        for role, percentage in zip(scenarios['roles'], percentages):
            rows['scenario'].append({'data_status': 'simulated', 'experiment': 'independent_role_mix',
                'preset': preset, 'role': role, 'percentage': percentage,
                'activities': scenarios['roleTotal'] * percentage / 100,
                'scope': scenarios['scope']})
    for rate in scenarios['retentionPercent']:
        for newcomers in scenarios['newcomers']:
            active = 0
            for month in range(1, 19):
                active = newcomers + active * rate / 100
                rows['scenario'].append({'data_status': 'simulated', 'experiment': 'independent_participation',
                    'retention_pct': rate, 'newcomers': newcomers, 'month': month, 'active': active,
                    'formula': scenarios['formula'], 'scope': scenarios['scope']})
    rows['panorama'] = [dict(record_type='country', **r) for r in rows['world']] + [dict(record_type='global_trend', **r) for r in rows['growth']]
    rows['comparison'] = [dict(record_type='indicator', **r) for r in rows['cnus']] + [dict(record_type='publisher', **r) for r in rows['publishers']]
    rows['geography'] = rows['china']
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rows = build()
    inventory_path = ROOT / 'data/meta/dataset_inventory.csv'
    with inventory_path.open() as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        inventory = []
    retained = b''.join(line for line in inventory_path.read_bytes().splitlines(keepends=True)
                        if not any(line.startswith((name + ',').encode()) for name in NAMES.values()))
    for key, records in rows.items():
        name = NAMES[key]
        text, fields = text_csv(records)
        path = OUT / (name + '.csv')
        if args.check:
            assert path.read_text() == text, str(path)
        else:
            path.write_text(text)
        inventory.append(dict(dataset_id=name, path=str(path.relative_to(ROOT)), row_count=len(records),
            fields=';'.join(fields), chapter='5', use_scope='5.1当前三图；独立注明日期与样本范围' if key in ('panorama','comparison','geography') else '5.1旧版八图归档；非当前正文',
            related_indicators='OpenModelRelease;ModelSupplierDiv;OpenDatasetRelease' if key != 'scenario' else '',
            status='完全模拟；独立情景' if key == 'scenario' else '实测快照；固定数据可复现',
            review_note='preview/web/build_gosm_supply_data.py；preview/content/gosm/supply-methods.md',
            sha256=hashlib.sha256(text.encode()).hexdigest()))
    if not args.check:
        f = io.StringIO(newline='')
        writer = csv.DictWriter(f, columns, lineterminator='\n')
        writer.writerows(inventory)
        inventory_path.write_bytes(retained + f.getvalue().encode())
    print('PASS: three current + eight archived 5.1 datasets reproduced; country / organization / China residual sums verified.')
