import ast
import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks/hitting/09_hitting_phase_decomposition.ipynb'
cells = json.loads(NOTEBOOK.read_text())['cells']
ns = {}
exec(''.join(cells[0]['source']), ns)
for cell in cells[1:]:
    for node in ast.parse(''.join(cell['source'])).body:
        if isinstance(node, ast.FunctionDef):
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(NOTEBOOK), 'exec'), ns)


class HittingPhaseTests(unittest.TestCase):
    def test_phases_cover_fixed_approach_through_contact_without_overlap(self):
        events = dict(fp_10_time=.5, fp_100_time=.52, contact_time=.68)
        for fraction in (.4, .5, .6):
            bounds = ns['phase_bounds'](events, fraction)
            pairs = list(bounds.values())
            self.assertAlmostEqual(pairs[0][0], .35)
            self.assertEqual(pairs[-1][1], .68)
            for left, right in zip(pairs, pairs[1:]):
                self.assertEqual(left[1], right[0])
            self.assertAlmostEqual(bounds['early_postplant'][1], .52 + fraction * .16)

    def test_unordered_events_and_invalid_fraction_fail(self):
        with self.assertRaisesRegex(ValueError, 'unordered'):
            ns['phase_bounds'](dict(fp_10_time=.5, fp_100_time=.4, contact_time=.6))
        with self.assertRaisesRegex(ValueError, 'fraction'):
            ns['phase_bounds'](dict(fp_10_time=.4, fp_100_time=.5, contact_time=.6), 1.)

    def test_exact_boundaries_and_time_weighted_mean(self):
        t = np.arange(0, 1.001, .01)
        ag = pd.DataFrame({'time': t, **{c: 100 * t for c in ns['ANGLE_COLS']}})
        vg = pd.DataFrame({'time': t, **{c: 200 * t for c in ns['VELO_COLS']}})
        f = ns['extract_phase'](ag, vg, .205, .405)
        self.assertAlmostEqual(f['duration_ms'], 200.)
        self.assertAlmostEqual(f['pelvis_angle_z_change_deg'], 20.)
        self.assertAlmostEqual(f['pelvis_angular_velocity_z_mean_dps'], 61.)

    def test_hitting_extension_direction_is_negative(self):
        t = np.arange(0, 1.001, .01)
        ag = pd.DataFrame({'time': t, **{c: t for c in ns['ANGLE_COLS']}})
        vg = pd.DataFrame({'time': t, **{c: -100 * t for c in ns['VELO_COLS']}})
        f = ns['extract_phase'](ag, vg, .2, .4)
        self.assertAlmostEqual(f['rear_elbow_angular_velocity_x_directional_peak_dps'], 40.)
        self.assertAlmostEqual(f['rear_elbow_angular_velocity_x_mean_dps'], -30.)

    def test_gaps_outside_windows_and_short_phases_rejected(self):
        t = np.arange(0, 1.001, .01)
        g = pd.DataFrame({'time': t, 'x': 1.})
        g.loc[30, 'x'] = np.nan
        with self.assertRaisesRegex(ValueError, 'gaps'):
            ns['phase_window'](g, ['x'], .2, .4)
        with self.assertRaisesRegex(ValueError, 'outside'):
            ns['phase_window'](g, ['x'], -.1, .1)
        ag = pd.DataFrame({'time': t, **{c: t for c in ns['ANGLE_COLS']}})
        vg = pd.DataFrame({'time': t, **{c: t for c in ns['VELO_COLS']}})
        with self.assertRaisesRegex(ValueError, 'shorter'):
            ns['extract_phase'](ag, vg, .2, .203)

    def test_wrapped_axial_angles_interpolate_continuously(self):
        g = pd.DataFrame({'time': [0., .01, .02], 'pelvis_angle_z': [179., -179., -177.]})
        _, a = ns['phase_window'](g, ['pelvis_angle_z'], .005, .015)
        self.assertAlmostEqual(a[-1, 0] - a[0, 0], 2.)

    def test_outer_and_inner_folds_hold_out_entire_hitters(self):
        ids = np.repeat(np.arange(25).astype(str), 3)
        visits = np.zeros(len(ids), dtype=int)
        for train, test in ns['group_splits'](ids, 5, 2026):
            self.assertFalse(set(ids[train]) & set(ids[test]))
            visits[test] += 1
            for inner_train, inner_test in ns['group_splits'](ids[train], 4, 2027):
                self.assertFalse(set(ids[train][inner_train]) & set(ids[train][inner_test]))
                self.assertFalse(set(ids[test]) & set(ids[train][inner_train]))
        np.testing.assert_array_equal(visits, 1)

    def test_hitter_weighting_and_training_only_scaler(self):
        ids = np.array(['a', 'a', 'a', 'b'])
        weights = ns['hitter_weights'](ids)
        self.assertAlmostEqual(sum(weights[:3]), weights[3])
        x = pd.DataFrame({'feature': [0., 1., 2., 3.]})
        model = ns['fit_ridge'](x, np.arange(4.), ids, 1.)
        model.predict(pd.DataFrame({'feature': [1000.]}))
        self.assertAlmostEqual(model.named_steps['standardscaler'].mean_[0], 1.5)


if __name__ == '__main__':
    unittest.main()
