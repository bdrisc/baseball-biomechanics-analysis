import json
from pathlib import Path
import unittest
import numpy as np
from scipy.signal import butter, sosfiltfilt

ROOT = Path(__file__).resolve().parents[1]
nb = json.loads((ROOT / 'notebooks/hitting/17_lead_hand_path_shape.ipynb').read_text())
ns = {'np': np, 'butter': butter, 'sosfiltfilt': sosfiltfilt,
      'EVENTS': ['fp_10_time', 'fp_100_time', 'contact_time'],
      'WINDOWS': {'plant': None, 'late100': .1, 'late75': .075, 'late125': .125}}
exec(''.join(nb['cells'][2]['source']), ns)

class HandPathTests(unittest.TestCase):
    def test_known_geometry(self):
        code = ''.join(nb['cells'][3]['source']).split('measurement_checks()\nCONFIGS')[0]
        exec(code, ns)
        ns['measurement_checks']()

    def trial(self, side='R'):
        import pandas as pd
        t = np.arange(0, .301, 1/360)
        g = pd.DataFrame({'time': t, 'fp_10_time': .05, 'fp_100_time': .1, 'contact_time': .25})
        pelvis = np.column_stack([.2*t, .1*t, 1+.05*t])
        hand = pelvis + np.column_stack([-.3+2*t, -.4+.5*t, .5-t])
        if side == 'L':
            pelvis[:,1] *= -1
            hand[:,1] *= -1
        for prefix, xyz in [('lwjc',hand if side=='R' else hand+5),('rwjc',hand if side=='L' else hand+5),
                            ('left_hip',pelvis),('right_hip',pelvis)]:
            for i,a in enumerate('xyz'):
                g[prefix+'_'+a]=xyz[:,i]
        return g

    def test_anatomical_lead_selection_and_mirroring(self):
        prepare = ns['prepare_trial']
        t,r,ev = prepare(self.trial('R'),'R',None)
        tl,l,el = prepare(self.trial('L'),'L',None)
        np.testing.assert_allclose(r['pelvis_relative'],l['pelvis_relative'])
        np.testing.assert_allclose(r['global'],l['global'])
        m,c = ns['extract_window'](t,r,ev,'late100')
        self.assertAlmostEqual(m['pelvis_relative']['net_drop_cm'],10,places=6)
        self.assertAlmostEqual(m['global']['net_drop_cm'],9.5,places=6)

    def test_late_window_independent_of_foot_events(self):
        g=self.trial();g['fp_10_time']=np.nan;g['fp_100_time']=.3
        t,p,e=ns['prepare_trial'](g,'R',None)
        ns['extract_window'](t,p,e,'late100')
        with self.assertRaisesRegex(ValueError,'unordered'):
            ns['extract_window'](t,p,e,'plant')

    def test_missing_signal_and_coverage_rejected(self):
        g=self.trial();g.loc[30,'lwjc_z']=np.nan
        with self.assertRaisesRegex(ValueError,'nonfinite'):
            ns['prepare_trial'](g,'R',12)
        g=self.trial();g['contact_time']=.4
        with self.assertRaisesRegex(ValueError,'outside'):
            ns['prepare_trial'](g,'R',12)
        g=self.trial().drop(index=25)
        with self.assertRaisesRegex(ValueError,'irregular'):
            ns['prepare_trial'](g,'R',12)

    def test_no_postcontact_filter_dependence(self):
        g=self.trial();a=ns['prepare_trial'](g,'R',12)[1]
        g.loc[g.time>.253,['lwjc_x','lwjc_y','lwjc_z']]+=100
        b=ns['prepare_trial'](g,'R',12)[1]
        np.testing.assert_allclose(a['global'],b['global'])

    def test_sweep_unavailable_near_origin(self):
        t=np.linspace(0,.1,101)
        p=np.column_stack([.01*np.cos(t),.01*np.sin(t),t])
        self.assertTrue(np.isnan(ns['path_metrics'](t,p,True)['horizontal_sweep_deg']))

if __name__ == '__main__':
    unittest.main()
