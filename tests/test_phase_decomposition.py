import ast
import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks/pitching/08_pitching_phase_decomposition.ipynb'
cells = json.loads(NOTEBOOK.read_text())['cells']
ns = {}
exec(''.join(cells[0]['source']), ns)
for cell in cells[1:]:
    for node in ast.parse(''.join(cell['source'])).body:
        if isinstance(node, ast.FunctionDef):
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(NOTEBOOK), 'exec'), ns)


class PhaseDecompositionTests(unittest.TestCase):
    def test_exact_boundary_integration_uses_seconds(self):
        g = pd.DataFrame({'time': np.arange(0, 1.01, .01), 'power': 100.})
        t, values = ns['phase_window'](g, ['power'], .205, .405)
        self.assertEqual(t[0], .205)
        self.assertEqual(t[-1], .405)
        self.assertAlmostEqual(ns['trapezoid'](values[:, 0], t), 20.)

    def test_generation_absorption_and_signed_transfer_separate(self):
        t = np.arange(0, 1.01, .01)
        ag = pd.DataFrame({'time': t, **{c: 100 * t for c in ns['ANGLE_COLS']}})
        vg = pd.DataFrame({'time': t, **{c: np.full(len(t), 100) for c in ns['VELO_COLS']}})
        eg = pd.DataFrame({'time': t})
        for joint in ns['ENERGY_JOINTS']:
            eg[joint + '_energy_generated'] = 100.
            eg[joint + '_energy_transfer_stp'] = -50.
            eg[joint + '_energy_transfer_jfp'] = 30.
        events = dict(fp_10_time=.1, fp_100_time=.2, MER_time=.4, BR_time=.6, MIR_time=.7)
        f, e, status = ns['extract_phase'](ag, vg, eg, 'acceleration', events, 10.)
        self.assertEqual(status, 'available')
        self.assertAlmostEqual(f['duration_ms'], 200.)
        self.assertAlmostEqual(e['shoulder_generation_j_kg'], 2.)
        self.assertAlmostEqual(e['shoulder_absorption_j_kg'], 0.)
        self.assertAlmostEqual(e['shoulder_transfer_stp_signed_j_kg'], -1.)
        self.assertAlmostEqual(e['shoulder_transfer_jfp_signed_j_kg'], .6)

    def test_signal_gaps_and_bad_windows_rejected(self):
        g = pd.DataFrame({'time': np.arange(0, 1.01, .01), 'x': 1.})
        g.loc[30, 'x'] = np.nan
        with self.assertRaisesRegex(ValueError, 'gaps'):
            ns['phase_window'](g, ['x'], .2, .4)
        with self.assertRaisesRegex(ValueError, 'outside'):
            ns['phase_window'](g, ['x'], -.1, .1)

    def test_axial_angles_unwrap_before_interpolation(self):
        g = pd.DataFrame({'time': [0., .01, .02], 'pelvis_angle_z': [179., -179., -177.]})
        _, a = ns['phase_window'](g, ['pelvis_angle_z'], .005, .015)
        self.assertAlmostEqual(a[-1, 0] - a[0, 0], 2.)

    def test_pitchers_do_not_cross_validation_folds(self):
        ids = np.repeat(np.arange(20).astype(str), 4)
        splits = list(ns['group_splits'](ids, 5, 2026))
        visits = np.zeros(len(ids), dtype=int)
        for train, test in splits:
            self.assertFalse(set(ids[train]) & set(ids[test]))
            visits[test] += 1
        np.testing.assert_array_equal(visits, 1)

    def test_pitcher_weights_and_training_only_scaler(self):
        ids = ['a', 'a', 'a', 'b']
        weights = ns['pitcher_weights'](ids)
        self.assertAlmostEqual(sum(weights[:3]), weights[3])
        x = pd.DataFrame({'feature': [0., 1., 2., 3.]})
        model = ns['fit_ridge'](x, np.arange(4.), np.array(ids), 1.)
        self.assertAlmostEqual(model.named_steps['standardscaler'].mean_[0], 1.5)


if __name__ == '__main__':
    unittest.main()
