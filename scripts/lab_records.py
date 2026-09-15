"""Explicit mode-aware attempt accounting; no instrument control.

Without a plan this is descriptive only. Four-label certification delegates to
the existing analyzer and its unchanged fixed-N plan. Native eight-label data
never enter that analyzer. Inputs are preserved; output directories must be new.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from analyze_trials import analyze

ROUTES = {'su4': (4, 4), 'su8-embed': (8, 4), 'su8-walsh': (8, 8)}
FIELDS = ['trial_id', 'condition_id', 'calibration_id', 'phase_code_id',
          'receiver_id', 'preparation_id', 'hidden_label', 'click_mask',
          'source_herald_time', 'gate_open_time', 'gate_close_time',
          'energy_bound_id', 'quality_flags', 'mode_count', 'record_status']
SCHEMA = {
    'version': 1, 'fields': FIELDS,
    'mask_convention': 'integer sum(2**port for each clicked logical output port); port 0 is least significant bit',
    'route_mode_and_label_counts': ROUTES,
    'allowed_quality_flags': ['', 'NONE', 'integrity_rejected'],
    'failure_rule': 'zero/multiple clicks, any inactive-port click, and integrity_rejected stay in N and yield inconclusive',
    'record_status': 'SYNTHETIC_NOT_AN_EXPERIMENT or externally declared real-data status',
    'times': 'Real records require gate_open_time and gate_close_time on a laboratory common clock; source_herald_time is optional for clock-defined trials; synthetic timestamps may be blank; no hardware time unit is invented',
    'labels': 'offline scoring join only: seal receiver records before joining separately held hidden labels',
    'trial_definition': 'one upstream clock/herald gate per attempted P0 exposure; output detection never creates the trial',
    'native_eight_limit': 'descriptive C/E/F only; no four-label frontier or certification',
}


def new_output(path: Path) -> Path:
    """Never use protected evidence as output, even for a new child directory."""
    path = path.resolve()
    blocked = [ROOT / 'baseline', ROOT / 'provenance', ROOT / 'audits',
               ROOT / 'repairs', ROOT / 'integrations', ROOT / 'sources', ROOT / 'studies']
    if any(path == p or p in path.parents for p in blocked):
        raise ValueError('Output would enter preserved evidence')
    results = ROOT / 'results'
    runs = results / 'runs'
    if (path == results or results in path.parents) and not runs in path.parents:
        raise ValueError('Fresh result output must be below results/runs/')
    path.mkdir(parents=True, exist_ok=False)
    return path


def summarize(route: str, rows: list[dict], plan: dict | None = None,
              allow_synthetic: bool = False) -> tuple[dict, list[dict]]:
    if route not in ROUTES:
        raise ValueError('Unknown mode route')
    modes, labels = ROUTES[route]
    if not rows:
        raise ValueError('At least one attempted interrogation is required')
    if plan is not None and labels != 4:
        raise ValueError('Native eight-mode data have descriptive analysis only; no four-label plan')
    counts = {'correct': 0, 'wrong': 0, 'inconclusive': 0}
    mask_counts = [0] * (1 << modes)
    confusion = [[0] * (labels + 1) for _ in range(labels)]
    label_counts = [0] * labels
    failures = {'no_click': 0, 'multiple_click': 0, 'leakage': 0, 'integrity_rejected': 0}
    group_fields = ('condition_id', 'preparation_id', 'calibration_id', 'phase_code_id', 'receiver_id', 'energy_bound_id')
    groups = {}
    ids, adapted, changed = set(), [], []
    for row in rows:
        missing = set(FIELDS) - row.keys()
        if missing:
            raise ValueError('Missing raw fields: ' + ','.join(sorted(missing)))
        rid = row['trial_id']
        if not rid or rid in ids:
            raise ValueError('Missing/duplicate trial id')
        ids.add(rid)
        mode_count, label, mask = int(row['mode_count']), int(row['hidden_label']), int(row['click_mask'])
        if mode_count != modes or not 0 <= label < labels or not 0 <= mask < 1 << modes:
            raise ValueError('Invalid mode count, hidden label, or full-width mask')
        if row['quality_flags'] not in SCHEMA['allowed_quality_flags']:
            raise ValueError('Unknown quality flag; do not silently reject or drop a record')
        if row['record_status'] != 'SYNTHETIC_NOT_AN_EXPERIMENT':
            if any(not row[k] for k in ('gate_open_time', 'gate_close_time')):
                raise ValueError('Real records require acquisition gate timestamps')
        rejected = row['quality_flags'] == 'integrity_rejected'
        leakage = bool(mask >> labels)
        single = mask.bit_count() == 1
        fail = rejected or leakage or not single
        decision = labels if fail else mask.bit_length() - 1
        key = 'inconclusive' if fail else ('correct' if decision == label else 'wrong')
        counts[key] += 1
        group_key = tuple(row[field] for field in group_fields)
        group = groups.setdefault(group_key, {**dict(zip(group_fields, group_key)),
            'counts': {'correct': 0, 'wrong': 0, 'inconclusive': 0}})
        group['counts'][key] += 1
        mask_counts[mask] += 1
        label_counts[label] += 1
        confusion[label][decision] += 1
        failures['no_click'] += int(mask == 0)
        failures['multiple_click'] += int(mask.bit_count() > 1)
        failures['leakage'] += int(leakage)
        failures['integrity_rejected'] += int(rejected)
        if labels == 4:
            mapped = dict(row)
            # A fail-only remapping is explicit. Full detector data stay in the
            # original CSV, all-mask histogram, and per-row change ledger.
            mapped_mask = 0 if rejected or leakage else mask
            mapped['click_mask'] = str(mapped_mask)
            mapped['mode_count'] = '4'
            adapted.append(mapped)
            if mapped_mask != mask:
                changed.append({'trial_id': rid, 'original_mask': mask,
                                'analysis_mask': mapped_mask,
                                'leakage': leakage, 'integrity_rejected': rejected})
    n = len(rows)
    for group in groups.values():
        group['N'] = sum(group['counts'].values())
        group.update({symbol: group['counts'][key] / group['N'] for symbol, key in
                      [('C', 'correct'), ('E', 'wrong'), ('F', 'inconclusive')]})
    result = {
        'status': 'DESCRIPTIVE_ONLY', 'route': route, 'N': n,
        'counts': counts,
        'per_condition_preparation': list(groups.values()),
        'pooled_rates_warning': 'Use per_condition_preparation to compare retuned inputs; pooled rates combine different conditions',
        'C': counts['correct'] / n, 'E': counts['wrong'] / n,
        'F': counts['inconclusive'] / n,
        'label_counts': label_counts,
        'all_mask_counts': mask_counts,
        'mask_width': modes,
        'confusion_columns': list(range(labels)) + ['inconclusive'],
        'confusion_rows_hidden_label': confusion,
        'failure_diagnostics_may_overlap': failures,
        'fail_only_remapping': changed,
        'data_status': sorted({row['record_status'] for row in rows}),
        'calibration_or_source_claims': 'None established by descriptive accounting',
    }
    if plan is not None:
        if any(row['record_status'] == 'SYNTHETIC_NOT_AN_EXPERIMENT' for row in rows) and not plan.get('synthetic'):
            raise ValueError('Synthetic records cannot use a real-data plan')
        certificate = analyze(plan, adapted, allow_synthetic=allow_synthetic)
        if certificate['counts'] != counts:
            raise ArithmeticError('Four-label adapter changed outcome accounting')
        result['four_label_conditional_certificate'] = certificate
    return result, adapted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route', choices=ROUTES, required=True)
    parser.add_argument('--trials', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--allow-synthetic', action='store_true')
    args = parser.parse_args()
    with args.trials.open(newline='') as handle:
        rows = list(csv.DictReader(handle))
    plan = json.loads(args.plan.read_text()) if args.plan else None
    result, adapted = summarize(args.route, rows, plan, args.allow_synthetic)
    result['source_csv_sha256'] = hashlib.sha256(args.trials.read_bytes()).hexdigest()
    output = new_output(args.output)
    (output / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    if adapted:
        with (output / 'adapted_four_label_trials.csv').open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(adapted)
    print(json.dumps({'output': str(output), 'N': result['N'], 'counts': result['counts'],
                      'status': result['status']}))


if __name__ == '__main__':
    main()
