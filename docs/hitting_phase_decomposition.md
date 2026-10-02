# Swing Phase Profiles & Bat Speed

## Setup

Run `notebooks/hitting/09_hitting_phase_decomposition.ipynb` after installing the
repository requirements. It is self-contained, has six code cells with cleared
outputs, and does not require earlier notebooks to run first. It can also run
outside the repository, using the current working directory for inputs/outputs.

For standalone setup, run this in a separate notebook cell and restart the kernel:

```python
%pip install numpy pandas scipy matplotlib scikit-learn ipython
```

The first run downloads about 155 MB of missing official Dataset v1 joint-angle
and joint-velocity archives, plus metadata and POI CSVs. Archives are checked
against published SHA-256 values; subsequent runs reuse local CSVs. Set
`AUTO_DOWNLOAD=False` to require existing files. Input CSV hashes, package
versions, model feature lists, settings, and cohort sizes are saved in a manifest.

## Phase definitions

The [official hitting documentation](https://github.com/drivelineresearch/openbiomechanics/blob/main/baseball_hitting/README.md)
provides front-foot contact, foot plant, and ball contact in the full-signal
files. It does not supply a swing-initiation timestamp in those tables.

| Phase | Start | End | Meaning |
|---|---|---|---|
| Approach | 150 ms before front-foot contact | Front-foot contact at 10% bodyweight | Fixed observation window; not measured stride onset |
| Landing | Front-foot contact | Foot plant at 100% bodyweight | Official event-defined window |
| Early post-plant | Foot plant | Analytical plant-to-contact boundary | First 50% by default; 40% and 60% sensitivity |
| Late post-plant | Analytical boundary | Ball contact | Remainder of the plant-to-contact window |
| Early follow-through | Ball contact | 50 ms after contact | Description only; excluded from prediction |

These windows are an operational decomposition, not a validated set of biological
swing phases. The approach window does not capture each hitter's entire load or
stride. Percent-of-time boundaries are retrospective and require knowing when
contact occurred; this is an assessment analysis, not live forecasting.

## Measurements and exclusions

Each predictive phase includes duration; signed changes in pelvis and torso
axial angles, torso extension, pelvis tilt, lead-knee flexion, and rear-elbow
flexion; mean/change of signed torso-minus-pelvis separation; and directional
mean/peak velocities of pelvis, torso, lead knee, and rear elbow. Separation is
computed from the processed axial angles and is not identical to every OBP
POI x-factor convention. Pelvis/torso forward rotation is positive. Knee/elbow
extension is negative in hitting data; their directional peak uses the negated
signal, while means retain the published sign.

Angles are unwrapped before interpolation. The already processed signals are
used without another filter. Each phase includes its exact interpolated event
boundaries on each table's own time grid. Missing samples are not imputed or
bridged. Duplicate IDs/time keys fail explicitly. Missing, unordered, inconsistent,
out-of-recording events, irregular sampling, nonfinite features, and windows
shorter than two 360 Hz marker sampling intervals fail extraction. Reasons are
saved for every swing and split setting.

Body and bat controls are height, mass, bat weight, bat length, and hitting side.
No bat angular velocity, bat speed, batted-ball measurement, or follow-through
feature is included as a predictor. Full-signal inputs do not contain the four
C3D head markers used by study 07, so this study covers posture, separation, and
body-joint motion without adding a head-displacement estimate.

## Outcomes and models

The primary outcome is processed resultant bat speed at contact
(`bat_speed_mph_contact_x`). Blast sensor bat speed and measured exit velocity
are separate exploratory secondary outcomes. These are distinct measurements;
there is no substitution between them when values are missing. Metadata and POI
join one-to-one on processed `session_swing`, not C3D filename swing numbers.
Motion-derived bat speed shares a measurement system with body kinematics;
Blast speed provides a useful separate sensor comparison, but also has its own
measurement limitations. Exit velocity depends on pitch and impact conditions
that these models do not fully adjust for.

Within each outcome, all three split definitions use the intersection of valid
swings and identical hitter folds. Outcome-complete cohorts can differ between
bat speed, Blast speed, and exit velocity; compare prediction errors within an
outcome. Models include a training-mean baseline, body/bat controls, each phase
alone with controls, all phases, and removal of one phase at a time.

Five outer folds hold out entire hitters. Four inner folds select a ridge penalty
from a predefined grid. Two seeded repetitions expose fold sensitivity. Scaling
and tuning use training data only. Ridge fitting weights each hitter equally;
MAE averages errors within hitter and then across hitters. The scaler uses
training-swing means/variances. Fold membership and tuning choices are exported.

A duration sensitivity repeats the 50% split analysis using only swings with
80–200 ms from foot plant to contact. This is a pragmatic screen consistent with
previous hitting analyses in this repository, not a validated biological cutoff.
The subset is evaluated with its own grouped folds; raw main-versus-subset
changes should not be read as a paired treatment comparison.

Ablation is the increase in held-out MAE when a phase is removed. Positive values
indicate additional predictive information within that model. Correlated phases
share information, and a negative estimate means the reduced model predicted
better. Ablations do not add to a total contribution and are not percentages of
bat speed or evidence that changing a phase will increase performance.

Intervals use 2,000 paired hitter bootstrap resamples of fixed held-out errors,
after averaging repeats within hitter. They do not rerun the whole training/CV
process and can underrepresent training uncertainty. Comparisons are exploratory,
with no multiplicity adjustment. They do not constitute an independent external
validation sample.

## Initial results

A full Dataset v1 run retained 642 of 677 swings from 97 hitters. Thirty-five
swings had missing or unordered official events. All three split definitions
retained the same swings. Blast speed was available for 613 swings from 96
hitters; exit velocity for 637 swings from 96 hitters.

At the 50% boundary, the primary all-phase model had hitter-weighted held-out
MAE of 3.28 mph, compared with 3.47 mph for body/bat controls and 3.93 mph for
the training-mean baseline. The paired improvement over controls was 0.19 mph
with a conditional 95% interval of -0.11 to +0.51 mph. The added predictive
value of the full feature set over controls is therefore uncertain.

Removing early post-plant features increased primary MAE by 0.29 mph
(conditional interval +0.12 to +0.47). It had the largest phase-ablation point
estimate across the 40%, 50%, and 60% boundaries in the full sample. However,
the 80–200 ms screen excluded another 27 swings and retained 615 swings from
93 hitters. In that subset, the early post-plant ablation fell to +0.03 mph
(interval -0.12 to +0.19), and removing late post-plant features improved
prediction. A robust single phase winner is not established.

Secondary all-phase MAE was 4.40 mph for Blast speed and 4.97 mph for exit
velocity at the 50% split. Improvements over their corresponding controls were
also uncertain. These findings describe generalization to held-out hitters
within this dataset, not a demonstrated coaching intervention.

## Outputs

`results/hitting_phase_decomposition/` contains swing features, exclusion audits,
follow-through descriptions, outcome cohort sizes, held-out predictions, tuning
choices, fold membership, model errors, per-repeat errors, phase ablations,
hitter profiles, sample-relative percentiles, and the run manifest.
`figures/hitting_phase_decomposition/` contains a selected swing timeline, primary
model/ablation comparisons, and post-plant split sensitivity. Set `SELECTED_SWING`
to another retained processed ID to inspect it.

Profiles average each hitter's available retained swings; they are descriptions,
not fitted player forecasts. Percentiles refer only to this sample, with one
assessment session per hitter in Dataset v1. They are not norms, mechanical
grades, or prescribed targets. Raw files and individual-trial outputs are
excluded from Git.

## Validation

Run `python -m unittest discover -s tests -p test_hitting_phase_decomposition.py -v`.
Eight tests check phase coverage and event ordering, exact-boundary time-weighted
features, hitting extension signs, gaps/short windows, angle unwrapping, nested
hitter-disjoint folds, equal hitter weighting, and training-only scaling.

All six notebook cells were executed directly against official Dataset v1 data.
The three generated figures and exported fold audits were inspected.

Review the [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
before using or distributing data or derived results.
