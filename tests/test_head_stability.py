import ast
import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'notebooks/hitting/07_head_stability_contact_quality.ipynb'
cells = json.loads(NOTEBOOK.read_text())['cells']
namespace = {}
exec(''.join(cells[0]['source']), namespace)
for cell in cells[1:]:
    for node in ast.parse(''.join(cell['source'])).body:
        if isinstance(node, ast.FunctionDef):
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(NOTEBOOK), 'exec'), namespace)


class HeadStabilityTests(unittest.TestCase):
    def test_gap_limit_and_no_edge_extrapolation(self):
        xyz = np.column_stack([np.arange(10, dtype=float)] * 3)
        xyz[4:6] = np.nan
        repaired, count = namespace['interpolate_short_gaps'](xyz)
        np.testing.assert_allclose(repaired[:, 0], np.arange(10))
        self.assertEqual(count, 2)
        xyz[3:7] = np.nan
        with self.assertRaisesRegex(ValueError, 'gap'):
            namespace['interpolate_short_gaps'](xyz)
        xyz = repaired.copy()
        xyz[0] = np.nan
        with self.assertRaisesRegex(ValueError, 'edge'):
            namespace['interpolate_short_gaps'](xyz)

    def test_displacement_units_and_window(self):
        fs = 360
        t = np.arange(721) / fs
        center = np.column_stack([np.full(len(t), .2), np.full(len(t), .5), 1.5 + .1 * t])
        offsets = np.array([[-.04, -.05, 0], [.04, -.05, 0], [-.04, .05, 0], [.04, .05, 0]])
        trial = dict(fs=fs, head=center[:, None, :] + offsets[None, :, :])
        g = pd.DataFrame(dict(fp_100_time=[1.], contact_time=[1.15]))
        row, curve, _ = namespace['head_features'](trial, g, 2., 'R', 12)
        self.assertAlmostEqual(row['plant_vertical_range_cm'], 1.5, delta=.01)
        self.assertAlmostEqual(row['late100_vertical_range_cm'], 1., delta=.01)
        self.assertAlmostEqual(row['plant_max_disp_pct_height'], .75, delta=.005)
        np.testing.assert_allclose(curve[0], 0, atol=1e-8)
        self.assertAlmostEqual(curve[-1, 2], 1.5, delta=.01)

    def test_trajectory_match_ignores_filename_swing_number(self):
        fs = 360
        t = np.arange(100) / fs
        wrists = np.stack([np.column_stack([t, t ** 2, 1 + t]),
                           np.column_stack([t + .1, t ** 2, 1 + t])], axis=1)
        def group(offset):
            g = pd.DataFrame({'time': np.round(t, 4)})
            for i, side in enumerate(('l', 'r')):
                for a, axis in enumerate('xyz'):
                    g[side + 'wjc_' + axis] = wrists[:, i, a] + offset
            return g
        namespace['groups'] = {'492_3': group(0), '492_6': group(.1)}
        trial = dict(fs=fs, head=np.zeros((100, 4, 3)), wrists=wrists, original_swing=6)
        swing, error, _ = namespace['match_trial'](trial, ['492_6', '492_3'])
        self.assertEqual(swing, '492_3')
        self.assertEqual(error, 0)
        namespace['groups']['492_6'] = group(0)
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            namespace['match_trial'](trial, ['492_6', '492_3'])

    def test_within_session_model_removes_session_offsets(self):
        rng = np.random.default_rng(1)
        rows = []
        for athlete in range(20):
            for swing in range(6):
                movement, bat = rng.normal(size=2)
                rows.append(dict(user=str(athlete), session_key=str(athlete), head=movement,
                                 bat=bat, ev=100 * athlete + 2 * movement + 3 * bat))
        result = namespace['within_session_model'](pd.DataFrame(rows), 'ev', ['head', 'bat'],
                                                    'synthetic', bootstraps=100)
        self.assertEqual(result['status'], 'estimated')
        self.assertAlmostEqual(result['coefficient'], 2., places=8)
        self.assertEqual(result['n_athletes'], 20)

    def test_empty_repeatability_sample_is_explicit(self):
        table = pd.DataFrame(columns=['session_key'])
        summary = namespace['summarize_sessions'](table, 6)
        result = namespace['clustered_spearman'](summary, 'trajectory_rms_pct_height',
                                                 'ev_sd_mph', 'n_ev', 6)
        self.assertEqual(result['status'], 'insufficient sessions')


if __name__ == '__main__':
    unittest.main()
