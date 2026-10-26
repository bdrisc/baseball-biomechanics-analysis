import ast
import json
from pathlib import Path
import unittest
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

PATH = Path(__file__).resolve().parents[1] / 'notebooks/hitting/20_separation_bat_speed.ipynb'
NB = json.loads(PATH.read_text())
NS = dict(np=np, pd=pd, butter=butter, sosfiltfilt=sosfiltfilt, Ridge=Ridge, StandardScaler=StandardScaler,
          SEEDS=(20261026,20261027),
          EVENTS=['fp_10_time','fp_100_time','contact_time'],
          ANGLE_COLS=['pelvis_angle_z','torso_angle_z','torso_pelvis_angle_z'],
          RATE_COLS=['pelvis_angular_velocity_z','torso_angular_velocity_z'])
for cell in NB['cells']:
    tree = ast.parse(''.join(cell['source']))
    definitions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(PATH), 'exec'), NS)

class SeparationTests(unittest.TestCase):
    def signals(self):
        t = np.arange(181) / 360
        p = 100 * t
        torso = 60 * t
        a = pd.DataFrame(dict(time=t, pelvis_angle_z=p, torso_angle_z=torso, torso_pelvis_angle_z=torso-p))
        v = pd.DataFrame(dict(time=t,pelvis_angular_velocity_z=100+500*np.exp(-((t-.30)/.035)**2),
                              torso_angular_velocity_z=80+600*np.exp(-((t-.34)/.035)**2)))
        for g in (a,v):
            g['fp_10_time'],g['fp_100_time'],g['contact_time'] = .20,.25,.40
        return a,v

    def test_exact_window_boundaries(self):
        q,y = NS['window'](np.array([0.,1.,2.,3.]),np.array([0.,2.,4.,6.]),.3,2.7)
        np.testing.assert_allclose(q,[.3,1,2,2.7])
        np.testing.assert_allclose(y,2*q)

    def test_separation_sign_and_velocity_peak_lag(self):
        a,v = self.signals()
        row,_ = NS['extract'](a,v)
        self.assertAlmostEqual(row['plant_separation_deg'],10.)
        self.assertAlmostEqual(row['max_separation_deg'],16.)
        self.assertAlmostEqual(row['velocity_peak_lag_ms'],1000*(.3388888888888889-.30))
        self.assertTrue(row['peak_at_window_boundary'])
        self.assertTrue(row['pelvis_onset_censored'])
        self.assertTrue(np.isnan(row['onset_lag_ms']))

    def test_missing_endpoint_derivatives_are_trimmed(self):
        a,v = self.signals()
        v.loc[[0,len(v)-1],['pelvis_angular_velocity_z','torso_angular_velocity_z']] = np.nan
        row,_ = NS['extract'](a,v)
        self.assertAlmostEqual(row['plant_separation_deg'],10.)
        v.loc[v.time.between(.2,.3),'pelvis_angular_velocity_z'] = np.nan
        with self.assertRaises(ValueError): NS['extract'](a,v)

    def test_relative_convention(self):
        a,v = self.signals()
        row,_ = NS['extract'](a,v,definition='relative')
        self.assertAlmostEqual(row['plant_separation_deg'],10.)

    def test_missing_signal_and_bad_events_fail(self):
        a,v = self.signals()
        a.loc[10,'pelvis_angle_z'] = np.nan
        with self.assertRaises(ValueError): NS['extract'](a,v)
        a,v = self.signals()
        v['contact_time'] = .39
        with self.assertRaises(ValueError): NS['extract'](a,v)
        a,v = self.signals()
        a['fp_100_time'] = .45
        with self.assertRaises(ValueError): NS['extract'](a,v)

    def test_onset_requires_duration_and_marks_censoring(self):
        t = np.arange(101)*.002
        v = np.where((t>=.050)&(t<=.054),100.,0.)
        onset,censored = NS['onset'](t,v,0.,.2)
        self.assertTrue(np.isnan(onset))
        v[t>=.10] = 200.
        onset,censored = NS['onset'](t,v,0.,.2)
        self.assertAlmostEqual(onset,.10)
        self.assertFalse(censored)
        onset,censored = NS['onset'](t,np.ones(len(t))*200,0.,.2)
        self.assertTrue(censored)
        self.assertTrue(np.isnan(onset))

    def test_unwrap_and_time_normalization(self):
        np.testing.assert_allclose(NS['unwrap_deg']([170.,179.,-179.,-170.]),[170,179,181,190])
        a,v = self.signals()
        row,trace = NS['extract'](a,v)
        self.assertEqual(len(trace['pct']),101)
        self.assertAlmostEqual(trace['separation'][0],row['plant_separation_deg'])
        self.assertAlmostEqual(trace['separation'][-1],row['contact_separation_deg'])

    def test_grouped_folds_and_hitter_weighting(self):
        users = np.repeat(np.arange(20),np.arange(1,21))
        hits = np.zeros(len(users),int)
        for train,test in NS['folds'](users,5,10):
            self.assertFalse(set(users[train]) & set(users[test]))
            hits[test] += 1
        np.testing.assert_array_equal(hits,1)
        d = pd.DataFrame({'user':users})
        totals = pd.Series(NS['weights'](d)).groupby(d.user).sum()
        np.testing.assert_allclose(totals,totals.iloc[0])

    def test_scaling_fits_training_data_only(self):
        train = pd.DataFrame({'user':['a','a','b','b'],'x':[0.,1.,2.,3.],'y':[0.,2.,4.,6.]})
        test = pd.DataFrame({'x':[4.,100000.]})
        p = NS['ridge_predict'](train,test,['x'],'y',1.)
        single = NS['ridge_predict'](train,test.iloc[:1],['x'],'y',1.)
        self.assertAlmostEqual(p[0],single[0])

    def test_notebook_code_only_without_comments(self):
        import io, tokenize
        for c in NB['cells']:
            self.assertEqual(c['cell_type'],'code')
            tokens = tokenize.generate_tokens(io.StringIO(''.join(c['source'])).readline)
            self.assertFalse(any(t.type==tokenize.COMMENT for t in tokens))

if __name__ == '__main__':
    unittest.main()
