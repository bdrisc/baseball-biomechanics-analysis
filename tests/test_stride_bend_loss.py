"""Exercise the notebook's actual extraction functions without downloads."""
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt

ROOT = Path(__file__).resolve().parents[1]
NB = json.loads((ROOT / 'notebooks/hitting/11_stride_bend_loss.ipynb').read_text())
scope = dict(np=np, pd=pd, butter=butter, sosfiltfilt=sosfiltfilt,
             EVENTS=['fp_10_time', 'fp_100_time', 'contact_time'],
             ANGLE_COLS=['pelvis_angle_x', 'torso_angle_x'],
             VELO_COLS=['pelvis_angular_velocity_z', 'torso_angular_velocity_z'],
             ONSET_FRACTION=.15, SUSTAIN_S=.010, UPRIGHT_FLOOR_DPS=20., ROTATION_FLOOR_DPS=60.)
source = next(''.join(c['source']) for c in NB['cells']
              if c['cell_type'] == 'code' and ''.join(c['source']).startswith('def validate_trace'))
exec(source.split('\nresults, audit =')[0], scope)

def sample():
    t = np.arange(-.3, .201, 1/360)
    angle = -25 + 10 * np.clip((t + .12)/.08, 0, 1)
    common = dict(time=t, fp_10_time=np.zeros(len(t)),
                  fp_100_time=np.full(len(t), .04), contact_time=np.full(len(t), .14))
    a = pd.DataFrame(dict(**common, pelvis_angle_x=angle, torso_angle_x=angle))
    v = pd.DataFrame(dict(**common, pelvis_angular_velocity_z=np.where(t >= -.02, 100., 0.),
                         torso_angular_velocity_z=np.where(t >= .01, 100., 0.)))
    return a, v

class TestStrideBendLoss(unittest.TestCase):
    def test_signed_change_and_exact_boundaries(self):
        a, v = sample()
        r, _ = scope['extract_swing'](a, v)
        self.assertAlmostEqual(r['pelvis_pre_uprighting_deg'], 10.)
        self.assertAlmostEqual(r['pelvis_pre_max_excursion_deg'], 10.)
        self.assertAlmostEqual(r['pelvis_landing_uprighting_deg'], 0.)
        self.assertLess(r['pelvis_bend_minus_rotation_ms'], 0)
        t, y = scope['boundary_window'](np.array([0., .01, .02, .03]),
                                       np.array([0., 1., 2., 3.]), .003, .027)
        self.assertAlmostEqual(y[0], .3)
        self.assertAlmostEqual(y[-1], 2.7)

    def test_censoring_and_no_onset(self):
        t = np.arange(0., .101, .001)
        on, status, _ = scope['sustained_onset'](t, np.full(len(t), 100.), 0., .1, 20.)
        self.assertTrue(np.isnan(on)); self.assertEqual(status, 'left_censored')
        on, status, _ = scope['sustained_onset'](t, np.zeros(len(t)), 0., .1, 20.)
        self.assertTrue(np.isnan(on)); self.assertEqual(status, 'not_detected')

    def test_brief_spike_does_not_qualify(self):
        t = np.arange(0., .101, .001); rate = np.zeros(len(t)); rate[20:25] = 100.
        self.assertEqual(scope['sustained_onset'](t, rate, 0., .1, 20.)[1], 'not_detected')

    def test_recovered_loss_and_negative_change(self):
        a, v = sample()
        t = a.time.to_numpy()
        pulse = np.where(t < -.08, 10*np.clip((t+.12)/.04, 0, 1),
                         10*np.clip((-t-.04)/.04, 0, 1))
        a['pelvis_angle_x'] = -25 + pulse
        r, _ = scope['extract_swing'](a, v)
        self.assertAlmostEqual(r['pelvis_pre_uprighting_deg'], 0.)
        self.assertGreater(r['pelvis_pre_max_excursion_deg'], 9.)
        a['pelvis_angle_x'] = -25 - 10*np.clip((t+.12)/.08, 0, 1)
        r, _ = scope['extract_swing'](a, v)
        self.assertAlmostEqual(r['pelvis_pre_uprighting_deg'], -10.)

    def test_gaps_nonfinite_and_event_disagreement(self):
        a, v = sample()
        with self.assertRaisesRegex(ValueError, 'gap'):
            scope['extract_swing'](a.drop(index=100), v)
        a, v = sample(); a.loc[100, 'pelvis_angle_x'] = np.nan
        with self.assertRaisesRegex(ValueError, 'nonfinite'):
            scope['extract_swing'](a, v)
        a, v = sample(); v['fp_100_time'] = .05
        with self.assertRaisesRegex(ValueError, 'disagree'):
            scope['extract_swing'](a, v)

    def test_event_order_coverage_and_unwrap(self):
        a, v = sample(); a['fp_100_time'] = -.01
        with self.assertRaisesRegex(ValueError, 'unordered'):
            scope['extract_swing'](a, v)
        a, v = sample()
        with self.assertRaisesRegex(ValueError, 'outside'):
            scope['extract_swing'](a, v, lookback=.5)
        t = np.arange(5.)
        x, _ = scope['angle_trace'](t, np.array([178., 179., -180., -179., -178.]))
        np.testing.assert_allclose(np.diff(x), 1.)

    def test_unused_velocity_endpoints_do_not_exclude_swing(self):
        a, v = sample()
        v.loc[v.index[0], 'pelvis_angular_velocity_z'] = np.nan
        v.loc[v.index[-1], 'torso_angular_velocity_z'] = np.nan
        r, _ = scope['extract_swing'](a, v)
        self.assertAlmostEqual(r['pelvis_pre_uprighting_deg'], 10.)

if __name__ == '__main__':
    unittest.main()
