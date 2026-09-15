"""Independent matrix/record checks for bounded handover examples.

These establish the code mapping and accounting, not calibration or experimental
advantage. Existing theorem routines and numerical tolerances are unchanged.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'src'))
from lab_reference import (RECIPES, build_recipe, ideal_law, law_rates, optical_targets,
                           phase_code, preparation_unitary, sample_rows)
from lab_records import FIELDS, new_output, summarize
from theory import photon_score


class LabMatrixTests(unittest.TestCase):
    def test_walsh_entries_and_exact_integer_orthogonality(self):
        z = phase_code('su8-walsh').astype(int)
        expected_rows = ['++++++++', '+-+-+-+-', '++--++--', '+--++--+',
                         '++++----', '+-+--+-+', '++----++', '+--+-++-']
        self.assertEqual([''.join('+' if x == 1 else '-' for x in row) for row in z], expected_rows)
        np.testing.assert_array_equal(z.T @ z, 8 * np.eye(8, dtype=int))
        flips = np.ones((8, 8)) - 2 * np.eye(8)
        self.assertFalse(np.array_equal(flips.T @ flips, 8 * np.eye(8)))

    def test_all_port_routes_and_common_su_phases(self):
        for route, labels, modes in [('su4', 4, 4), ('su8-embed', 4, 8), ('su8-walsh', 8, 8)]:
            with self.subTest(route=route):
                target = optical_targets(route, np.ones(labels), np.ones(labels) / labels)
                decoded = target['output_intensities_by_label']
                np.testing.assert_allclose(decoded[:, :labels], np.eye(labels), atol=2e-15, rtol=0)
                np.testing.assert_allclose(decoded[:, labels:], 0, atol=2e-15, rtol=0)
                np.testing.assert_allclose(target['preparation_matrix'][:, 0], target['input_amplitudes'], atol=2e-15, rtol=0)
                for matrix in [target['preparation_matrix'], target['decoder_su'], *target['hidden_operations_su']]:
                    np.testing.assert_allclose(matrix.conj().T @ matrix, np.eye(modes), atol=3e-15, rtol=0)
                    self.assertAlmostEqual(np.linalg.det(matrix).real, 1., places=13)
                    self.assertAlmostEqual(np.linalg.det(matrix).imag, 0., places=13)
                expected_phase = 0. if route == 'su8-walsh' else np.pi / modes
                self.assertEqual(target['hidden_su_common_global_phase_radians'], expected_phase)
                for j in range(labels):
                    np.testing.assert_allclose(target['hidden_operations_su'][j],
                        np.exp(1j * expected_phase) * target['hidden_operations'][j], atol=1e-15, rtol=0)

    def test_embedding_preserves_active_input_and_receiver(self):
        p = np.array([.1, .2, .3, .4])
        eta = [.8, .7, .6, .2]
        four = optical_targets('su4', eta, p)
        eight = optical_targets('su8-embed', eta, p)
        np.testing.assert_allclose(eight['decoder'][:4, :4], four['decoder'], atol=0, rtol=0)
        np.testing.assert_allclose(eight['decoder'][4:, 4:], np.eye(4), atol=0, rtol=0)
        expected_preparation = np.eye(8)
        expected_preparation[:4, :4] = four['preparation_matrix']
        np.testing.assert_allclose(eight['preparation_matrix'], expected_preparation, atol=2e-15, rtol=0)
        np.testing.assert_allclose(eight['output_amplitudes_by_label'][:, :4], four['output_amplitudes_by_label'], atol=0, rtol=0)
        np.testing.assert_allclose(eight['input_amplitudes'][4:], 0, atol=0, rtol=0)
        self.assertLess(np.linalg.norm(eight['device_loss_contraction'].T @ eight['device_loss_contraction'] - np.eye(8)), 2.)
        self.assertFalse(np.allclose(eight['device_loss_contraction'].T @ eight['device_loss_contraction'], np.eye(8)))

    def test_native8_rule_against_independent_eigenproblem_and_amplitudes(self):
        eta = np.array([.7, .61, .52, .43, .34, .25, .16, .07])
        for penalty in [1 / 7, 1., 5., 20.]:
            with self.subTest(penalty=penalty):
                solved = photon_score(eta, penalty)
                v = np.sqrt(eta)
                matrix = (1 + penalty) * np.outer(v, v) / 8 - penalty * np.diag(eta)
                values, vectors = np.linalg.eigh(matrix)
                independent_p = vectors[:, -1] ** 2
                np.testing.assert_allclose(solved['p'], independent_p, atol=2e-14, rtol=0)
                self.assertAlmostEqual(solved['score'], values[-1], places=13)
                target = optical_targets('su8-walsh', eta, solved['p'])
                rates = law_rates(ideal_law(target), 8)
                for key in ['C', 'E', 'F']:
                    self.assertAlmostEqual(rates[key], solved[key], places=13)
                beta = solved['score']
                self.assertAlmostEqual((1 + penalty) * np.sum(eta / (beta + penalty * eta)) / 8, 1., places=13)
        inverse_p = (1 / eta) / (1 / eta).sum()
        rates = law_rates(ideal_law(optical_targets('su8-walsh', eta, inverse_p)), 8)
        self.assertAlmostEqual(rates['C'], 8 / (1 / eta).sum(), places=14)
        self.assertAlmostEqual(rates['E'], 0., places=14)
        # A lower penalty requires vacuum guesses, so the click-only teaching
        # analyzer must not be mistaken for the full minimum-error endpoint.
        lower = photon_score(eta, .05)
        passive = law_rates(ideal_law(optical_targets('su8-walsh', eta, lower['p'])), 8)
        self.assertGreater(lower['C'] - .05 * lower['E'], passive['C'] - .05 * passive['E'])

    def test_registered_forecasts_and_reverse_receiver(self):
        target, forecast, law, _ = build_recipe('p1')
        self.assertAlmostEqual(forecast['forecast_score_lambda_5'], .5865207654, places=8)
        self.assertAlmostEqual(forecast['classical_upper'], .5356220106, places=8)
        self.assertEqual(forecast['registered_fixed_N_example'], 500000)
        target, forecast, law, _ = build_recipe('p2', 'su8-embed')
        self.assertAlmostEqual(forecast['forecast_score_lambda_5'], .4264871934, places=8)
        self.assertAlmostEqual(forecast['robust_photon_upper'], .2220224979, places=9)
        self.assertEqual(forecast['registered_fixed_N_example'], 50000)
        np.testing.assert_array_equal(target['decoder'], np.eye(8))
        np.testing.assert_allclose(forecast['coherent_incident_energies'], [.33, .33, .33, 0], atol=2e-14, rtol=0)
        alpha = target['coherent_incident_amplitudes']
        displacement = target['coherent_displacement_for_common_su_hidden_phase']
        for j in range(4):
            out = target['device_loss_contraction'] @ target['hidden_operations_su'][j] @ alpha + displacement
            other = np.delete(out, j)
            np.testing.assert_allclose(other, 0, atol=1e-15, rtol=0)

    def test_invalid_preparation_or_mode_map_rejected(self):
        for vector in [np.array([1., 1.]), np.array([float('nan'), 0.]), np.array([-.6, .8])]:
            with self.assertRaises(ValueError):
                preparation_unitary(vector)
        with self.assertRaises(ValueError):
            optical_targets('su8-walsh', [.7] * 4, [.25] * 4)
        with self.assertRaises(ValueError):
            optical_targets('su4', [.7] * 4, [.25] * 3 + [float('nan')])


class LabRecordTests(unittest.TestCase):
    def records(self, route='su8-embed'):
        target, _, law, meta = build_recipe('commission-' + route)
        return sample_rows(route, law, meta, 12, 7)

    def test_every_eight_bit_mask_accounted_in_embedding(self):
        rows = self.records()
        rows = [dict(rows[0], trial_id=str(mask), hidden_label='0', click_mask=str(mask)) for mask in range(256)]
        result, adapted = summarize('su8-embed', rows)
        self.assertEqual(result['N'], 256)
        self.assertEqual(result['counts'], {'correct': 1, 'wrong': 3, 'inconclusive': 252})
        self.assertEqual(result['all_mask_counts'], [1] * 256)
        self.assertEqual(result['failure_diagnostics_may_overlap']['leakage'], 240)
        self.assertEqual(len(adapted), 256)
        self.assertEqual(sum(sum(row) for row in result['confusion_rows_hidden_label']), 256)
        self.assertEqual(rows[128]['click_mask'], '128')
        self.assertEqual(adapted[128]['click_mask'], '0')

    def test_rejected_no_multiple_and_leakage_remain_in_N(self):
        rows = self.records()[:5]
        for row, mask in zip(rows, [0, 3, 16, 1, 1]):
            row.update(hidden_label='0', click_mask=str(mask))
        rows[3]['quality_flags'] = 'integrity_rejected'
        result, adapted = summarize('su8-embed', rows)
        self.assertEqual(result['counts'], {'correct': 1, 'wrong': 0, 'inconclusive': 4})
        self.assertEqual(result['N'], 5)
        self.assertEqual(adapted[3]['click_mask'], '0')

    def test_descriptive_conditions_are_not_hidden_by_pooling(self):
        rows = self.records()[:4]
        for i, row in enumerate(rows):
            row.update(hidden_label='0', click_mask='1' if i < 2 else '0',
                       preparation_id='uniform' if i < 2 else 'lambda_5')
        summary, _ = summarize('su8-embed', rows)
        groups = {item['preparation_id']: item for item in summary['per_condition_preparation']}
        self.assertEqual(groups['uniform']['C'], 1.)
        self.assertEqual(groups['lambda_5']['F'], 1.)
        self.assertEqual(sum(item['N'] for item in groups.values()), 4)

    def test_native8_descriptive_only_and_bit7_is_label7(self):
        rows = self.records('su8-walsh')
        rows[0].update(hidden_label='7', click_mask='128')
        result, adapted = summarize('su8-walsh', rows)
        self.assertEqual(result['counts']['correct'], 12)
        self.assertEqual(result['mask_width'], 8)
        self.assertEqual(adapted, [])
        with self.assertRaisesRegex(ValueError, 'descriptive analysis only'):
            summarize('su8-walsh', rows, {'fixed_N': len(rows)})

    def test_four_label_adapter_invokes_existing_fixed_N_contract(self):
        target, _, law, metadata = build_recipe('p1', 'su8-embed')
        rows = sample_rows('su8-embed', law, metadata, 32, 9)
        rows[0]['click_mask'] = '128'
        plan = json.loads((ROOT / 'templates/primary_plan.example.json').read_text())
        with self.assertRaisesRegex(ValueError, 'Expected exactly 500000'):
            summarize('su8-embed', rows, plan, allow_synthetic=True)
        # This modified tiny plan is an isolated unit fixture only, never an
        # altered preregistration or a generated teaching plan.
        fixture = dict(plan, fixed_N=32)
        result, _ = summarize('su8-embed', rows, fixture, allow_synthetic=True)
        self.assertEqual(result['counts'], result['four_label_conditional_certificate']['counts'])
        self.assertEqual(result['four_label_conditional_certificate']['status'], 'SYNTHETIC_NOT_AN_EXPERIMENT')
        with self.assertRaisesRegex(ValueError, 'Synthetic records'):
            summarize('su8-embed', rows, dict(fixture, synthetic=False))

    def test_malformed_records_refused(self):
        variants = [('click_mask', '256'), ('hidden_label', '4'), ('mode_count', '4'),
                    ('quality_flags', 'unregistered_exclusion')]
        for key, value in variants:
            with self.subTest(field=key):
                rows = self.records()
                rows[0][key] = value
                with self.assertRaises(ValueError):
                    summarize('su8-embed', rows)
        rows = self.records()
        rows[1]['trial_id'] = rows[0]['trial_id']
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            summarize('su8-embed', rows)
        with self.assertRaises(ValueError):
            summarize('su4', [])

    def test_outputs_never_replace_existing_or_frozen_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileExistsError):
                new_output(Path(directory))
        for name in ['baseline/new-lab-run', 'results/new-lab-run', 'audits/new-lab-run', 'provenance/new-lab-run', 'studies/new-lab-run']:
            with self.subTest(path=name), self.assertRaises(ValueError):
                new_output(ROOT / name)

    def test_runnable_cli_round_trip_and_generated_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'fresh'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/lab_reference.py'),
                '--recipe', 'commission-su8-walsh', '--sample-attempts', '16', '--output', str(target)],
                cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            analysis = Path(directory) / 'analyzed'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/lab_records.py'),
                '--route', 'su8-walsh', '--trials', str(target / 'synthetic_trials.csv'), '--output', str(analysis)],
                cwd=ROOT, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((analysis / 'summary.json').read_text())['N'], 16)
        examples = ROOT / 'examples/lab'
        self.assertTrue(examples.is_dir())
        self.assertEqual({p.parent.name for p in examples.glob('*/MANIFEST.json')},
                         {'commission-su4', 'commission-su8-embed', 'commission-su8-walsh', 'm1', 'p1', 'p2'})
        if examples.exists():
            for manifest_path in examples.glob('*/MANIFEST.json'):
                manifest = json.loads(manifest_path.read_text())
                for name, expected in manifest['files'].items():
                    with self.subTest(example=manifest_path.parent.name, file=name):
                        self.assertEqual(hashlib.sha256((manifest_path.parent / name).read_bytes()).hexdigest(), expected)
                with (manifest_path.parent / 'synthetic_trials.csv').open(newline='') as handle:
                    rows = list(csv.DictReader(handle))
                summary = json.loads((manifest_path.parent / 'synthetic_summary.json').read_text())
                fresh, _ = summarize(summary['route'], rows)
                self.assertEqual(fresh['counts'], summary['counts'])
                self.assertTrue(all(row['record_status'] == 'SYNTHETIC_NOT_AN_EXPERIMENT' for row in rows))


if __name__ == '__main__':
    unittest.main()
