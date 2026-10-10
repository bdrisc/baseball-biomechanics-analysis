# Pelvis–Torso Uprighting Offset

Run `notebooks/hitting/12_pelvis_torso_uprighting_offset.ipynb` with the repository
requirements. It contains only code cells and runs independently of the earlier
studies. Save it under `notebooks/hitting/` and run all cells. Standalone execution
uses the working directory when the repository cannot be located.

## Inputs and conventions

The notebook reuses hitting `joint_angles.csv` and `metadata.csv`. Missing official
OpenBiomechanics Dataset v1 files download automatically, with verified SHA-256
hashes for the angle and optional landmark archives. POI outcomes are optional;
missing outcomes do not remove swings from descriptive timing analyses. Set
`MAKE_ANIMATION=False` to skip the approximately 66 MB landmark archive.

Pelvis X is posterior (+)/anterior (-) tilt. Torso X is extension (+)/flexion (-).
Increasing angles describe the operational uprighting directions. They are
different segment coordinates, not interchangeable absolute forward-bend angles.
This study measures posture-change sequencing, distinct from study 06's axial
rotation sequencing and study 05's peak timing.

Events are 10% front-foot loading (`fp_10_time`), full loading (`fp_100_time`), and
ball contact (`contact_time`). The search starts 150 ms before 10% loading and
ends at contact. It is not measured toe-off or the full stride.

## Two onset definitions

Angles are unwrapped and differentiated with real seconds. The default reuses
official processed traces without extra filtering; differentiation includes
25 ms of context on each side. Optional zero-phase filtering uses 100 ms of
context. Missing, inconsistent or unordered events, inadequate coverage,
nonfinite signals, time gaps, and missing identities are audited. Duplicate keys
fail explicitly. Exact angle boundaries are interpolated; onset times remain
on the sampled grid.

For each segment, the rate threshold is the larger of 20 deg/s or 15% of its
positive search-window peak. A crossing must persist at least 10 ms, measured
from the first to last sample in the qualifying run.

- **First sustained onset:** first qualifying threshold run anywhere in the
  search window. A qualifying run starting at the first sample is left-censored.
- **Final episode near contact:** last contiguous positive-rate episode that
  contains a qualifying threshold run and ends within 30 ms of contact. Its onset
  is the first qualifying crossing inside that episode. Zero crossings separate
  episodes; gaps are not merged. There is no fallback to an earlier episode
  outside the contact allowance. A threshold run starting at the first sample
  is left-censored. An episode extending to the search boundary is separately
  flagged, even when its threshold crossing is observable later.

These retrospective definitions depend on later movement. Neither is a validated
real-time detector or ground-truth physiological onset. The second definition
distinguishes early posture adjustments from the final qualifying movement,
without presuming that it is the correct definition for every research question.

Signed lag is `1000 * (torso onset - pelvis onset)`. Positive means pelvis first;
negative means torso first. Missing and censored pairs receive no numerical lag.
Differences within one median sample interval are labeled unresolved. Sampling
rows and sample offsets are not synchronized camera-video frames.

## Duration audits and consistency

All retained trials remain in the full analysis. Inspection flags identify an
absolute first-onset lag over 100 ms and loading-to-plant duration over 150 ms.
They are analytical inspection thresholds, not automatic declarations of bad
data or biomechanical diagnoses.

Separate sensitivity cohorts require plant-to-contact duration of 80–200 ms,
then also loading-to-plant duration at most 150 ms. The same trial subsets are
used when comparing definitions. Both full and restricted counts are reported.

Session profiles include median lag, SD, IQR, order fractions and detection
counts. Consistency estimates require at least five detected pairs. SD and IQR
describe within-session variability, not test–retest reliability. Cohort timing
uses one median per hitter; bootstrap intervals resample hitters equally.

## Sensitivity and performance comparisons

Settings test 100/150/200 ms lookbacks; 10/20/30 deg/s floors; 10/15/20% relative
thresholds; 5/10/20 ms persistence; additional 8/12/16 Hz filters; and absolute-only
20/40/80 deg/s thresholds. Final episodes additionally test 10/30/50 ms contact
allowances. Paired comparisons report timing changes, 95th-percentile changes,
order agreement and definite reversals. The first-onset analysis also compares a
fixed common detected cohort and exports per-swing stability across settings.

Exploratory outcome analyses compare each definition and duration cohort with
contact bat speed, exit velocity and attack angle. Between-hitter correlations
use one mean per hitter with at least five complete paired swings. Within-session
correlations center observations by hitter/session, remain swing-weighted, and
bootstrap whole hitters. Pitch location and other confounders are uncontrolled;
multiple comparisons are not used to claim significance or causation.

## Reviewed Dataset v1 execution

The user's executed notebook retained 642 of 677 swings from 97 hitters; 27 had
missing/inconsistent events and eight had unordered events. First sustained
onsets produced 640 pairs with median swing lag +2.7 ms. Final episodes produced
642 pairs, median swing and hitter lag 0.0 ms, and a hitter-bootstrap 95% interval
of -5.6 to +5.5 ms. Final order was pelvis first in 42.7%, torso first in 41.9%,
and unresolved within one sample in 15.4%. Eighty-seven sessions had at least
five detected final pairs.

The plant-to-contact restriction retained 615 swings; the combined restriction
retained 544 from 89 hitters. Both final-episode median swing lags remained 0.0 ms.
Seventy-eight swings were flagged for loading-to-plant duration.

Trial `440_8` had a first-onset lag of +716.6 ms and loading-to-plant duration
686.1 ms. The trace showed an early isolated pelvis movement. The final detector
selected pelvis onset +50.0 ms and torso onset +52.7 ms relative to plant, yielding
+2.7 ms and unresolved order. This was a definition comparison, not silent
outlier removal. Across the full sample, final lags ranged from -122.2 to +91.7 ms.

Contact-allowance changes produced no order changes among comparable detected
pairs; the 10 ms setting detected 641 pairs rather than 642. Threshold and
filter choices still changed individual labels: final-order agreement was
approximately 85–87% under relative-threshold changes and 75% at 8 Hz. This limits
individual classification even when the cohort median remains near zero.

Performance associations were generally weak. The combined duration cohort had
an exploratory within-session final-lag/bat-speed correlation of 0.116 (bootstrap
interval 0.013–0.227), one of many comparisons. It does not establish a stable
performance benefit. The findings support neither a universal pelvis-first
sequence nor an ideal lag to prescribe.

## Outputs and animation

Generated files stay under ignored directories:

- `results/pelvis_torso_uprighting_offset_v3/`: swing metrics, exclusions, session
  and hitter summaries, inspection/duration audits, definition comparisons,
  setting sensitivities, exploratory relationships, and a manifest with input
  hashes and settings.
- `figures/pelvis_torso_uprighting_offset_v3/`: full and central-distribution
  plots, selected and extreme trials, definition/sensitivity figures, and HTML
  animation.

The animation synchronizes joint centers with angle traces and a shared time
cursor. Landmarks must match the processed trial ID, time grid and events.
The global Y–Z view illustrates movement; it is not a body-local pelvic-tilt
estimator. This is reconstructed motion capture, not footage or measured bat/ball
motion. Review the upstream data license before distributing derived data.

Saved notebook outputs are cleared. Aggregate results above come from the reviewed
Dataset v1 execution; run all cells locally to regenerate individual outputs.

## Numerical validation

`python -m unittest discover -s tests -p test_uprighting_offset.py -v`

Controlled checks execute the notebook's actual functions without downloads.
They cover sustained crossings, sign conventions, separated episodes, contact
proximity, absent onsets, censoring, short spikes, and invalid signals/events.
The development smoke run also exercised exports, figures, sensitivity tables,
duration flags and animation. Those checks complement the user's full dataset
execution; they do not validate biological onset or individual coaching decisions.
