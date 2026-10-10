import ast
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt

ROOT = Path(__file__).resolve().parents[1]
NB = json.loads((ROOT/'notebooks/hitting/12_pelvis_torso_uprighting_offset.ipynb').read_text())
source = next(''.join(c['source']) for c in NB['cells']
              if c['cell_type']=='code' and 'def detect_final_episode(' in ''.join(c['source']))
scope = dict(np=np,pd=pd,butter=butter,sosfiltfilt=sosfiltfilt,
    EVENTS=['fp_10_time','fp_100_time','contact_time'],SEGMENTS=('pelvis','torso'),
    LOOKBACK_S=.150,FILTER_HZ=None,RATE_FLOOR_DPS=20.,PEAK_FRACTION=.15,
    SUSTAIN_S=.010,FINAL_EPISODE_CONTACT_GAP_S=.030)
nodes = [n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)
         or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='extract_first' for t in n.targets)]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'<notebook functions>','exec'),scope)

def sample(lag=.035):
    t = np.arange(-.4,.251,1/360)
    p = -.08
    return pd.DataFrame(dict(time=t,fp_10_time=-.05,fp_100_time=0.,contact_time=.12,
        pelvis_angle_x=-20+12/(1+np.exp(-(t-p)/.009)),
        torso_angle_x=-35+18/(1+np.exp(-(t-p-lag)/.009))))

class TestUprightingOffset(unittest.TestCase):
    def test_final_episode_skips_earlier_movement(self):
        t=np.arange(0,.401,.002)
        r=np.zeros(len(t));r[5:20]=50;r[170:]=100
        first=scope['detect_onset'](t,r)
        final=scope['detect_final_episode'](t,r,.4)
        self.assertAlmostEqual(first['time'],.01)
        self.assertAlmostEqual(final['time'],.34)
        self.assertEqual(final['qualifying_positive_episodes'],2)

    def test_no_fallback_outside_contact_allowance(self):
        t=np.arange(0,.401,.002)
        r=np.zeros(len(t));r[5:20]=50
        final=scope['detect_final_episode'](t,r,.4)
        self.assertEqual(final['state'],'not_detected')
        self.assertTrue(np.isnan(final['time']))

    def test_short_terminal_spike_does_not_qualify(self):
        t=np.arange(0,.401,.002)
        r=np.zeros(len(t));r[-3:]=100
        self.assertEqual(scope['detect_final_episode'](t,r,.4)['state'],'not_detected')

    def test_threshold_censoring_and_episode_boundary_are_separate(self):
        t=np.arange(0,.401,.002)
        censored=scope['detect_final_episode'](t,np.ones(len(t))*50,.4)
        self.assertEqual(censored['state'],'left_censored')
        self.assertTrue(np.isnan(censored['time']))
        r=np.ones(len(t));r[170:]=100
        observable=scope['detect_final_episode'](t,r,.4)
        self.assertEqual(observable['state'],'detected')
        self.assertTrue(observable['episode_left_censored'])
        self.assertAlmostEqual(observable['time'],.34)

    def test_signed_lag_preserves_both_orders(self):
        for lag in [.035,-.025]:
            row=scope['extract'](sample(lag))
            self.assertTrue(row['onset_pair_valid'])
            self.assertTrue(row['final_onset_pair_valid'])
            self.assertEqual(np.sign(row['uprighting_offset_ms']),np.sign(lag))
            self.assertEqual(np.sign(row['final_uprighting_offset_ms']),np.sign(lag))
            self.assertAlmostEqual(row['plant_to_contact_ms'],120.)
            self.assertAlmostEqual(row['loading_to_plant_ms'],50.)

    def test_missing_onsets_are_not_zero_lag(self):
        g=sample();g['pelvis_angle_x']=0.
        row=scope['extract'](g)
        self.assertFalse(row['onset_pair_valid'])
        self.assertFalse(row['final_onset_pair_valid'])
        self.assertTrue(np.isnan(row['uprighting_offset_ms']))
        self.assertTrue(np.isnan(row['final_uprighting_offset_ms']))

    def test_contact_allowance_changes_detection_without_fallback(self):
        t=np.arange(0,.401,.002)
        r=np.zeros(len(t));r[150:190]=100
        self.assertEqual(scope['detect_final_episode'](t,r,.4,contact_gap=.030)['state'],'detected')
        self.assertEqual(scope['detect_final_episode'](t,r,.4,contact_gap=.010)['state'],'not_detected')

    def test_gaps_nonfinite_events_and_coverage(self):
        with self.assertRaisesRegex(ValueError,'sampling'):
            scope['extract'](sample().drop(index=100))
        g=sample();g.loc[100,'torso_angle_x']=np.nan
        with self.assertRaisesRegex(ValueError,'nonfinite'):
            scope['extract'](g)
        g=sample();g['contact_time']=-.01
        with self.assertRaisesRegex(ValueError,'unordered'):
            scope['extract'](g)
        g=sample();g.loc[0,'fp_10_time']=-.1
        with self.assertRaisesRegex(ValueError,'inconsistent'):
            scope['extract'](g)
        with self.assertRaisesRegex(ValueError,'coverage'):
            scope['extract'](sample(),lookback=.5)

if __name__=='__main__':
    unittest.main()
