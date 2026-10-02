# Delivery Phase Profiles & Pitch Velocity

## Setup

Install the updated repository requirements and run every cell of
`notebooks/pitching/08_pitching_phase_decomposition.ipynb`. It contains code cells
only, with cleared outputs, and can also run independently in the current
working directory. Earlier notebooks do not need to run first.

For a standalone installation, use this in a separate notebook cell:

```python
%pip install numpy pandas scipy matplotlib scikit-learn ipython
```

Restart the kernel after installing packages. The first run downloads about
115 MB of missing official Dataset v1 archives: pitching joint angles, angular
velocities, and energy flow. Published archive hashes are verified; later runs
reuse local CSVs. Set `AUTO_DOWNLOAD=False` to require existing inputs.

## Phase boundaries

| Phase | Start | End | Role |
|---|---|---|---|
| Landing | Foot contact at 10% bodyweight | Foot plant at 100% bodyweight | Prediction and description |
| Cocking | Foot plant | Maximum shoulder external rotation | Prediction and description |
| Acceleration | Maximum external rotation | Ball release | Prediction and description |
| Early follow-through | Ball release | Maximum internal rotation | Description only |

These are event-defined windows, not an exhaustive decomposition of the entire
delivery. Pre-landing stride motion is outside this version. The landing window
can be only a few 360 Hz samples; short-window peaks should be interpreted
cautiously. Follow-through measurements are excluded from velocity predictors.

## Measurements and quality checks

Each pre-release phase has duration, signed pelvis/torso rotation change,
trunk-posture and lead-knee angle change, and directional mean/peak angular
velocities for pelvis, torso, shoulder internal rotation, and elbow extension.
Shoulder rotation remains a joint-level proxy. Axial angles are unwrapped before
interpolation. Processed OBP signals are used without another filter.

Pitch IDs must be unique in metadata/POI; time keys must be unique in signal
tables. Missing, unordered, inconsistent, or out-of-recording boundaries and
signal gaps fail explicitly. Each table uses its own time grid, with exact
interpolated phase endpoints. No imputation bridges missing motion samples.

Selected lead-knee, shoulder, and elbow energy-flow columns are power signals
in watts. Positive and negative parts of generated power are integrated over
real seconds to estimate generation and absorption, respectively. Signed joint
force-power and segment torque-power transfer channels are integrated separately.
All energy features are divided by body mass, yielding J/kg. Transfer channels
are not added across joints, and this is not a whole-body energy budget.

The source [Visual3D pipeline](https://github.com/drivelineresearch/openbiomechanics/blob/main/baseball_pitching/code/v3d/CMO.v3s)
documents power calculations; the [pitching documentation](https://github.com/drivelineresearch/openbiomechanics/blob/main/baseball_pitching/README.md)
documents events and POI energy summaries. An explicit shoulder/elbow cross-check
compares foot-plant-to-release integrals with official POI values. The initial
median absolute differences were 2.094 J and 0.006 J for shoulder/elbow
generation, and 0.176 J and 2.810 J for absorption. The definitions/sampling are
not numerically identical; estimates are labeled descriptive rather than exact
reproductions of the POI summaries.

## Predictive comparisons

Fastballs are the sole pitch type. The outcome is measured pitch velocity.
Models compare a training-mean baseline, body size, each phase's kinematics,
all pre-release kinematics, and removal of one phase at a time. An energy-complete
cohort compares kinematics alone with kinematics plus energy, and removes each
phase's combined kinematic/energy block from the latter model. Comparisons within
each cohort use the same pitches and outer folds.

Five outer folds hold out whole pitchers. Four inner folds, also grouped by
pitcher, select the ridge penalty from a predefined grid. Scaling is fit inside
each training split. Two seeded repeats show fold sensitivity. Training losses
and reported errors give pitchers equal weight despite different pitch counts.

Phase ablation is the change in held-out mean absolute error when a phase's
features are removed. Positive values indicate additional predictive information.
Correlated adjacent phases share information, so these values do not sum to a
total contribution or establish causal importance. Body-size adjustment also
does not remove every possible confounder.

Intervals use 2,000 paired pitcher bootstrap resamples of the fixed held-out
errors, after averaging repeats within pitcher. They do not refit the full
nested-validation procedure and can underrepresent training/fold uncertainty.
All comparisons are exploratory. Sample-relative profile percentiles describe
this dataset; they are not mechanical grades, targets, or MLB norms.

## Initial results and sensitivity

The initial run retained 402 of 411 fastballs from 100 pitchers. The full
kinematic model had MAE 2.97 mph versus 3.69 mph for body size. Adding energy
features reduced MAE to 2.28 mph; the paired improvement was 0.69 mph with a
conditional bootstrap interval of 0.31–1.06 mph.

Acceleration had the largest kinematic ablation point estimate in the full
sample (+0.30 mph). A sensitivity excludes phases longer than the predefined
pragmatic limits: landing 100 ms, cocking 300 ms, acceleration 80 ms. Five pitches
were flagged; the remaining 397 pitches still represented 100 pitchers. Cocking
had the largest kinematic point estimate in that subset. These limits are
sensitivity screens, not validated biological thresholds. There is no stable
single phase winner from these comparisons.

## Outputs and validation

`results/phase_decomposition/` contains extraction audits, pitch features,
energy summaries, follow-through descriptions, held-out predictions, model
metrics, per-repeat metrics, tuning choices, fold membership, paired ablations,
POI cross-checks, pitcher profiles, sample percentiles, and an input-hash manifest.
`figures/phase_decomposition/` contains phase timelines, model comparisons, and
selected-joint generation profiles. Change `SELECTED_PITCH` to inspect another
retained pitch. Raw inputs and generated individual-trial outputs remain local
and excluded from Git.

Run `python -m unittest discover -s tests -p test_phase_decomposition.py -v`.
Tests check elapsed-time integration, signed energy handling, gaps, phase
boundaries, angle unwrapping, pitcher-disjoint folds, training weights, and
training-only scaling. All seven notebook cells were executed directly against
official Dataset v1 data, and the generated figures were visually inspected.

These observational assessment results identify measurements worth studying;
they do not validate a coaching intervention. Review the
[OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
before using or distributing data or derived outputs.
