"""Runnable laboratory teaching recipes using established scientific routines.

No driver, voltage recipe, calibration result, or experimental acquisition is
provided. Every generated attempt is conspicuously synthetic and descriptive.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from optics import coherent_nulling_masks, rates_from_masks, source_click_probabilities
from photon_support import reverse_support_upper
from theory import (classical_score_upper, fixed_n_radius, four_code, photon_score,
                    robust_contrast_upper, transmissions)
from lab_records import FIELDS, ROUTES, SCHEMA, new_output, summarize

RECIPES = ('commission-su4', 'commission-su8-embed', 'commission-su8-walsh', 'm1', 'p1', 'p2')


def phase_code(route: str) -> np.ndarray:
    if route not in ROUTES:
        raise ValueError('Unknown route')
    if route != 'su8-walsh':
        return four_code()
    return np.array([[(-1) ** ((i & j).bit_count()) for j in range(8)] for i in range(8)], dtype=float)


def preparation_unitary(amplitudes: np.ndarray) -> np.ndarray:
    """One deterministic SO(m) completion with first column the positive input."""
    a = np.asarray(amplitudes, dtype=float)
    if a.ndim != 1 or len(a) < 2 or not np.all(np.isfinite(a)) or np.any(a < 0) or not np.isclose(a @ a, 1, atol=1e-13, rtol=0):
        raise ValueError('Input must be a normalized nonnegative real amplitude vector')
    e0 = np.eye(len(a))[:, 0]
    if np.linalg.norm(a - e0) < 1e-14:
        return np.eye(len(a))
    w = (e0 - a) / np.linalg.norm(e0 - a)
    matrix = np.eye(len(a)) - 2 * np.outer(w, w)
    matrix[:, 1] *= -1
    return matrix


def optical_targets(route: str, eta, p) -> dict:
    modes, labels = ROUTES[route]
    eta = transmissions(eta)
    p = np.asarray(p, dtype=float)
    if eta.shape != (labels,) or p.shape != (labels,) or np.any(p < 0) or not np.all(np.isfinite(p)) or not np.isclose(p.sum(), 1, rtol=0, atol=1e-13):
        raise ValueError('Preparation/loss must have exactly the active label count')
    code = phase_code(route)
    decoder = np.eye(modes)
    decoder[:labels, :labels] = code.T / np.sqrt(labels)
    operations = np.repeat(np.eye(modes)[None, :, :], labels, axis=0)
    for j in range(labels):
        operations[j, :labels, :labels] = np.diag(code[:, j])
    loss = np.eye(modes)
    loss[:labels, :labels] = np.diag(np.sqrt(eta))
    amplitudes = np.zeros(modes)
    amplitudes[:labels] = np.sqrt(p)
    preparation = preparation_unitary(amplitudes)
    # Fix once for every hidden setting. Native Walsh operators already have
    # determinant +1. Four flips have det -1 and share the same correction.
    receiver_phase = np.pi / modes if np.linalg.det(decoder) < 0 else 0.0
    hidden_phase = np.pi / modes if np.linalg.det(operations[0]) < 0 else 0.0
    output = np.array([decoder @ loss @ operation @ amplitudes for operation in operations])
    return {
        'route': route, 'modes': modes, 'labels': labels,
        'port_order': list(range(modes)),
        'binary_port_order': [format(i, '03b') for i in range(8)] if modes == 8 else [format(i, '02b') for i in range(4)],
        'active_ports': list(range(labels)), 'vacuum_input_ports': list(range(labels, modes)),
        'matrix_convention': 'columns=input ports; rows=output ports; photon input occupies logical source port 0 before preparation',
        'eta_active': eta, 'input_probabilities_active': p, 'input_amplitudes': amplitudes,
        'preparation_matrix': preparation, 'phase_code_active': code,
        'hidden_operations': operations, 'device_loss_contraction': loss,
        'decoder': decoder,
        'decoder_su_global_phase_radians': receiver_phase,
        'decoder_su': np.exp(1j * receiver_phase) * decoder,
        'hidden_su_common_global_phase_radians': hidden_phase,
        'hidden_operations_su': np.exp(1j * hidden_phase) * operations,
        'common_phase_warning': 'One shared phase factor across ALL labels only; per-label compiler phase normalization changes the coherent problem',
        'unused_loss_entries': 'Identity on nominal inactive vacuum modes is a bookkeeping convention, not a measured loss specification',
        'output_amplitudes_by_label': output,
        'output_intensities_by_label': abs(output) ** 2,
        'combined_transfer_by_label': np.array([decoder @ loss @ operation @ preparation for operation in operations]),
        'combined_transfer_role': 'Classical transfer check only; answer-dependent compilation is not hidden-label interrogation',
        'phase_operation_role': 'Independent hidden control after P0; phases alone cannot implement T',
        'loss_role': 'Independent attenuation or justified device model between P0 and P1; receiver/detector loss is separate',
        'compiler_interface': 'Translate logical matrix/port ordering with the laboratory compiler; no vendor adapter or voltage settings are supplied',
    }


def ideal_law(targets: dict) -> np.ndarray:
    labels, modes = targets['labels'], targets['modes']
    law = np.zeros((labels, 1 << modes))
    intensities = targets['output_intensities_by_label']
    for j in range(labels):
        law[j, 0] = max(0., 1 - intensities[j].sum())
        for port in range(modes):
            law[j, 1 << port] = intensities[j, port]
    return law


def law_rates(law: np.ndarray, labels: int) -> dict:
    if not np.all(np.isfinite(law)) or np.min(law) < -1e-14 or not np.allclose(law.sum(axis=1), 1, atol=1e-12, rtol=0):
        raise ValueError('Invalid unconditional mask law')
    correct = sum(law[j, 1 << j] for j in range(labels)) / labels
    conclusive = law[:, [1 << j for j in range(labels)]].sum() / labels
    return {'C': float(correct), 'E': float(conclusive - correct), 'F': float(1 - conclusive)}


def embed_law(law: np.ndarray, route: str) -> np.ndarray:
    if route == 'su4':
        return law
    result = np.zeros((4, 256))
    result[:, :16] = law
    return result


def jsonable(obj):
    if isinstance(obj, np.ndarray):
        if np.iscomplexobj(obj):
            return {'real': obj.real.tolist(), 'imag': obj.imag.tolist()}
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {key: jsonable(value) for key, value in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [jsonable(item) for item in obj]
    return obj


def build_recipe(recipe: str, chip: str = 'su4') -> tuple[dict, dict, np.ndarray, dict]:
    if recipe not in RECIPES or chip not in ('su4', 'su8-embed'):
        raise ValueError('Unknown recipe or four-label chip route')
    forecast = {'status': 'HYPOTHETICAL_MODEL_NOT_LAB_DATA', 'recipe': recipe,
                'synthetic_sample_role': 'Small descriptive example; registered trial budgets are unchanged',
                'environment': {'python': platform.python_version(), 'numpy': np.__version__}}
    metadata = {'condition_id': recipe, 'calibration_id': 'EXAMPLE_ONLY',
                'phase_code_id': 'physical_four_one_pi_flips_common_optical_phase',
                'receiver_id': 'D_Jhalf_minus_I_fixed', 'preparation_id': recipe,
                'energy_bound_id': 'EXAMPLE_ONLY'}
    if recipe.startswith('commission-'):
        route = {'commission-su4': 'su4', 'commission-su8-embed': 'su8-embed',
                 'commission-su8-walsh': 'su8-walsh'}[recipe]
        m = ROUTES[route][1]
        eta = np.ones(m)
        targets = optical_targets(route, eta, np.ones(m) / m)
        law = ideal_law(targets)
        example_eta = np.array([.7] * (m - 1) + [.14])
        retuned = photon_score(example_eta, 5.)
        forecast.update({'question': 'Classical wave transfer and phase-code routing check; not source-class certification',
                         'synthetic_record_model': 'Ideal single-photon categorical teaching draws from the calculated intensities; these are not laser threshold-detector statistics or classical measurements',
                         'equal_loss_ideal_rates': law_rates(law, m),
                         'lossy_teaching_eta': example_eta,
                         'photon_only_penalty_threshold': 1 / (m - 1),
                         'lossy_teaching_penalty': 5., 'lossy_teaching_photon_rule': retuned,
                         'native8_comparison_limit': 'Walsh photon theorem specialization only; no exact four-symbol classical frontier, four-mode robustness transfer, or source-class advantage claim'})
        if m == 8:
            metadata['phase_code_id'] = 'walsh8_binary_dot_i_j_common_optical_phase'
            metadata['receiver_id'] = 'walsh8_transpose_over_sqrt8_fixed'
    elif recipe == 'm1':
        route = chip
        eta = np.array([.7, .7, .7, .14])
        preparations = {'uniform': np.ones(4) / 4,
                        'zero_error': (1 / eta) / (1 / eta).sum(),
                        'lambda_1': photon_score(eta, 1.)['p'],
                        'lambda_5': photon_score(eta, 5.)['p']}
        conditions = {}
        for name, p in preparations.items():
            target = optical_targets(route, eta, p)
            rates = law_rates(ideal_law(target), 4)
            conditions[name] = {'p': p, 'input_amplitudes': target['input_amplitudes'],
                                'preparation_matrix': target['preparation_matrix'],
                                **rates, 'score_lambda_1': rates['C'] - rates['E'],
                                'score_lambda_5': rates['C'] - 5 * rates['E']}
        targets = optical_targets(route, eta, preparations['lambda_5'])
        law = ideal_law(targets)
        forecast.update({'conditions': conditions, 'sample_condition': 'lambda_5',
                         'fixed_receiver': 'D4 (embedded when requested); no held-out training',
                         'registered_meaning': 'Input-retuning mechanism; descriptive finite scan does not prove global optimality or source-class advantage'})
        metadata['preparation_id'] = 'lambda_5'
    elif recipe == 'p1':
        route = chip
        eta = np.array([.7, .7, .7, .56])
        optimum = photon_score(eta, 5.)
        targets = optical_targets(route, eta, optimum['p'])
        law4 = source_click_probabilities(eta, optimum['p'], [.029, .97, .001], .92, 1e-6, .035)
        law = embed_law(law4, route)
        rates = rates_from_masks(law4)
        upper = classical_score_upper(robust_contrast_upper(.7, [.003] * 4), .98, 5.)
        forecast.update({'ideal_photon_rule': optimum, 'forecast_rates': rates,
                         'forecast_score_lambda_5': rates['C'] - 5 * rates['E'],
                         'classical_upper': upper, 'registered_fixed_N_example': 500000,
                         'alpha_stat': .00025, 'shared_calibration_failure_allocation': .0005,
                         'statistical_radius': fixed_n_radius(500000, 5., .00025),
                         'tail_score_subtraction': .002,
                         'hypothetical_inputs': {'source_pn': [.029, .97, .001], 'post_device_detection': .92,
                                                'dark_per_detector_per_gate': 1e-6, 'independent_gaussian_path_phase_sigma': .035,
                                                'operator_radius': .003, 'mean_energy_upper': .98},
                         'registered_plan': 'templates/primary_plan.example.json',
                         'comparison': 'All permitted classical source mixtures and receivers, under justified P0/P1 bounds'})
        metadata['condition_id'] = 'P1_moderate_imbalance'
    else:
        route = chip
        eta = np.array([.7, .7, .7, .035])
        # Existing forecast's water-filling prescription; independent scalar
        # implementation of the same declared coherent nulling illumination.
        fill = lambda log_level: np.maximum((np.log(eta) - log_level) / (4 * eta), 0)
        level = brentq(lambda value: fill(value).sum() - .99, -100., float(np.log(eta.max())), xtol=5e-324, rtol=9e-16)
        energies = fill(level)
        targets = optical_targets(route, eta, energies / .99)
        # P2 is displaced direct-path readout. It does not use D4. Keep this
        # distinction explicit in both targets and matrix transfer checks.
        identity = np.eye(ROUTES[route][0])
        targets['decoder'] = identity
        targets['decoder_su'] = identity.astype(complex)
        targets['decoder_su_global_phase_radians'] = 0.
        targets['receiver_role'] = 'Identity path routing plus separately confirmed coherent displacement after P1, then clicks; no D4'
        incident_alpha = np.zeros(ROUTES[route][0])
        incident_alpha[:4] = np.sqrt(energies)
        displacement = -targets['device_loss_contraction'] @ incident_alpha
        output = np.array([targets['device_loss_contraction'] @ op @ incident_alpha + displacement for op in targets['hidden_operations']])
        targets.update({'coherent_incident_amplitudes': incident_alpha,
                        'coherent_incident_energy_active': energies,
                        'coherent_displacement_at_P1': displacement,
                        'coherent_displacement_for_common_su_hidden_phase': np.exp(1j * targets['hidden_su_common_global_phase_radians']) * displacement,
                        'displacement_phase_rule': 'If the hidden compiler physically adds the common SU phase c, use -c T alpha; canonical -T alpha assumes O_j or compensation of that common phase',
                        'output_amplitudes_by_label': output,
                        'output_intensities_by_label': abs(output) ** 2,
                        'combined_transfer_by_label': np.array([targets['device_loss_contraction'] @ op @ targets['preparation_matrix'] for op in targets['hidden_operations']]),
                        'combined_transfer_role': 'Linear transfer before displacement; displacement is affine and needs a reference/coupler, not a unitary matrix'})
        law4 = coherent_nulling_masks(eta, energies, .92, 1e-6, 1e-4, .035)
        law = embed_law(law4, route)
        rates = rates_from_masks(law4)
        nominal, upper = reverse_support_upper(eta, 5., .003)
        forecast.update({'coherent_incident_energies': energies, 'coherent_nominal_mean': .99,
                         'coherent_mean_upper': 1., 'forecast_rates': rates,
                         'forecast_score_lambda_5': rates['C'] - 5 * rates['E'],
                         'nominal_photon_support_upper': nominal, 'robust_photon_upper': upper,
                         'registered_fixed_N_example': 50000, 'alpha_stat': .00025,
                         'shared_calibration_failure_allocation': .0005,
                         'statistical_radius': fixed_n_radius(50000, 5., .00025),
                         'hypothetical_inputs': {'post_device_detection': .92, 'dark_per_detector_per_gate': 1e-6,
                                                'residual_poisson_background_per_output': 1e-4, 'independent_gaussian_path_phase_sigma': .035,
                                                'operator_radius': .003},
                         'registered_plan': 'templates/reverse_plan.example.json',
                         'comparison': 'Implemented coherent receiver versus entire declared four-path one-photon upper bound'})
        metadata['condition_id'] = 'P2_severe_imbalance'
        metadata['receiver_id'] = 'coherent_displacement_nulling_fixed'
    forecast['route'] = route
    forecast['synthetic_spare_port_model'] = 'No extra dark/leakage assumed in teaching model; all real spare-port outcomes must be recorded'
    forecast['mask_probabilities_by_label'] = law
    return targets, forecast, law, metadata


def sample_rows(route: str, law: np.ndarray, metadata: dict, n: int, seed: int) -> list[dict]:
    if type(n) is not int or n < 1:
        raise ValueError('Sample attempts must be a positive integer')
    modes, labels = ROUTES[route]
    if law.shape != (labels, 1 << modes):
        raise ValueError('Mask law width does not match route')
    law_rates(law, labels)
    rng = np.random.default_rng(seed)
    hidden = rng.integers(0, labels, size=n)
    rows = []
    for i, label in enumerate(hidden):
        mask = int(rng.choice(1 << modes, p=law[label] / law[label].sum()))
        row = {name: '' for name in FIELDS}
        row.update(metadata)
        row.update({'trial_id': f'SYNTHETIC-{i:07d}', 'hidden_label': str(int(label)),
                    'click_mask': str(mask), 'mode_count': str(modes), 'quality_flags': 'NONE',
                    'record_status': 'SYNTHETIC_NOT_AN_EXPERIMENT'})
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', choices=RECIPES, required=True)
    parser.add_argument('--chip', choices=('su4', 'su8-embed'), default='su4', help='Four-label recipes only')
    parser.add_argument('--sample-attempts', type=int, default=256, help='Descriptive synthetic sample only; does not alter registered N')
    parser.add_argument('--seed', type=int, default=20260915)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    targets, forecast, law, metadata = build_recipe(args.recipe, args.chip)
    rows = sample_rows(targets['route'], law, metadata, args.sample_attempts, args.seed)
    summary, _ = summarize(targets['route'], rows)
    summary['seed'] = args.seed
    output = new_output(args.output)
    for name, obj in [('target_matrices.json', targets), ('forecast.json', forecast),
                      ('synthetic_summary.json', summary), ('RECORD_SCHEMA.json', SCHEMA)]:
        (output / name).write_text(json.dumps(jsonable(obj), indent=2, allow_nan=False) + '\n')
    with (output / 'synthetic_trials.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    if args.recipe.startswith('commission-'):
        with (output / 'commissioning_transfer_reference.csv').open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=['hidden_label', 'input_port', 'output_port',
                'target_real', 'target_imag', 'target_intensity', 'record_status'])
            writer.writeheader()
            for label, matrix in enumerate(targets['combined_transfer_by_label']):
                for input_port in range(targets['modes']):
                    for output_port in range(targets['modes']):
                        value = matrix[output_port, input_port]
                        writer.writerow({'hidden_label': label, 'input_port': input_port, 'output_port': output_port,
                            'target_real': float(value.real), 'target_imag': float(value.imag),
                            'target_intensity': float(abs(value) ** 2), 'record_status': 'TARGET_NOT_A_MEASUREMENT'})
    manifest = {'status': 'SYNTHETIC_TEACHING_OUTPUT', 'recipe': args.recipe,
                'seed': args.seed, 'sample_attempts': args.sample_attempts,
                'files': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(output.iterdir())}}
    (output / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'route': targets['route'],
                      'sample_attempts': args.sample_attempts, 'status': forecast['status']}))


if __name__ == '__main__':
    main()
