# Pelvis and Torso Bend Loss Before Landing

Run `notebooks/hitting/11_stride_bend_loss.ipynb` with the repository requirements.
The notebook is self-contained and also supports execution outside the repository.
It reuses `data/raw/hitting/` CSVs and downloads missing official Dataset v1 files,
checking the published archive SHA-256 values. Core angle/velocity archives total
about 155 MB; the optional landmarks animation adds about 66 MB.

## Scope and conventions

This study measures posture change before landing, complementing study 03's
hinge measurements, study 05's post-plant uprighting, study 06's rotation onsets,
and study 09's phase profiles. It uses motion capture, not a CV pelvis estimator.

The primary window is 150 ms before `fp_10_time` to `fp_10_time`. Sensitivities
use 100 and 200 ms. Landing spans `fp_10_time` to `fp_100_time`. These events
represent 10% and 100% bodyweight front-foot loading. The fixed lookback is not
measured toe-off, first move, or the full stride. The released full-signal tables
do not provide a toe-off event.

OBP pelvis X is posterior (+)/anterior (-) tilt and torso X is extension
(+)/flexion (-). Positive end-minus-start differences describe movement toward
posterior tilt/extension. The notebook exports OBP angles and signed changes,
without asserting an absolute forward-bend calibration. Approximately 10 degrees
from the motivating Driveline case is not used as a diagnostic threshold.

## Measurements

For pelvis and torso independently, outputs include angle at window start,
front-foot contact and full plant; net pre-contact change; maximum positive
excursion from window start; landing and total changes; peak pre-contact rate;
time of that peak; and cumulative positive-rate duration. Duration counts sampled
intervals with increasing angle and can be sensitive to small signal fluctuations.
Maximum excursion preserves an uprighting move that is recovered before landing.

Angles are unwrapped and evaluated at exact interpolated boundaries. The default
uses the official processed traces without another filter. Positive axial
rotation velocities come from the independent published Z channels. Additional
8/12/16 Hz zero-phase filtering is tested as an offline sensitivity only.

Onsets require at least 10 ms continuously above the larger of 15% of the positive
search-window peak or an absolute floor. Primary floors are 20 deg/s for uprighting
and 60 deg/s for rotation, with 10/40 and 30/80 deg/s sensitivities. Search spans
window start to ball contact. These estimates are retrospective, including the
threshold's dependence on the subsequent peak. A qualifying run at the left
boundary is censored. Missing and censored onsets do not receive a numerical
timing offset. A negative bend-minus-rotation offset means uprighting onset leads
rotation onset. Rate floors and run length are analytical choices, not biological
definitions or validated diagnostic cutoffs.

Nonfinite signals, sampling gaps, inconsistent or unordered events, missing table
coverage and short windows are excluded with explicit reasons. Missing outcomes
do not exclude a swing from descriptive measurements. Duplicate join keys fail
explicitly. Tables are validated and interpolated on their own time grids. Only
requested signal windows are checked for nonfinite values; unused velocity
endpoints can be missing in the official files. Filtering uses an additional
100 ms of angle data on each side and requires complete coverage of that padding.

## Visuals and outcomes

The selected-swing plot shows angle change, uprighting rate, axial rotation and
events. Default selection is nearest the median pelvis net change, independent
of outcomes. Set `SELECTED_SWING` to a retained processed ID to inspect another.

The optional HTML animation synchronizes a landmark skeleton with angle traces.
Global Y-Z is approximately a sagittal projection before rotation, not a body-local
angle calculation. The hip-to-shoulder line illustrates trunk geometry; hip
centers do not supply a pelvic sagittal axis. The animation is reconstructed
motion capture, not camera footage. Set `MAKE_SKELETON_ANIMATION=False` to skip it.

Exploratory correlations compare signed changes and onset offsets with measured
attack angle, contact bat speed, Blast speed and exit velocity. Between-hitter
estimates use equally weighted hitter means with at least three paired swings.
Within-hitter estimates correlate pooled athlete/session-centered residuals with
at least three paired swings per group; those estimates remain swing-weighted.
Whole-hitter bootstrap intervals use 1,000 resamples. Fewer than five hitters
produce no estimate. No multiplicity-adjusted significance claim is made.
Pitch location and other confounders are not controlled, and associations do not
establish that modifying posture improves performance. Single-session variation
is not a test-retest reliability estimate.

Window sensitivity uses the common retained cohort. Filter/threshold comparisons
are paired within retained swings and show the available numerical onset counts.
The fixed window and onset definitions remain limitations even if results are
stable across these settings.

## Outputs

Generated files go under already ignored directories:

- `results/hitting_phase_decomposition/stride_bend_loss/`: swing measurements,
  hitter/session profiles, onset counts, exclusion audits, relationships,
  sensitivity comparisons, per-window features and a manifest with input hashes.
- `figures/hitting_phase_decomposition/stride_bend_loss/`: timeline/cohort PNGs
  and the selected-swing HTML animation.

Saved notebook outputs are cleared. Raw inputs and individual derived results
are not committed. Review the upstream data license before sharing derived data.

## Validation

`python -m unittest discover -s tests -p test_stride_bend_loss.py -v`

Seven tests execute the notebook's extraction functions and check exact-boundary
interpolation, signs, recovered excursions, onset censoring, brief spikes,
sampling gaps, nonfinite values, event disagreement/order, coverage and angle
unwrapping and unused velocity endpoints. Dataset execution results should be assessed separately from these
controlled numerical checks.

All eight code cells were executed against the official Dataset v1 files.
The primary run retained 642 of 677 swings from 97 hitters; 27 exclusions
had missing official events and eight had unordered events. All 642 swings were retained under the 100, 150
and 200 ms windows. Median signed pre-contact change was -1.90 degrees for the
pelvis and -1.57 degrees for the torso. These negative values describe gaining
bend in this window, rather than universal pre-landing uprighting. The figures,
onset counts, generated animation and sensitivity outputs were checked locally.
