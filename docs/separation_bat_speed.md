# Pelvis–Torso Separation Magnitude, Timing & Bat Speed

## Question and relationship to earlier studies

Do pelvis–torso separation magnitude and timing relate to bat speed, and do the
same associations appear between hitters and across swings within one hitter's
session? Does timing add predictive information beyond magnitude?

Study 06 describes rotation onset order. Study 09 evaluates broad swing phases
against bat speed at contact. Study 20 isolates separation, uses published maximum
bat speed as its primary outcome, and separates between-hitter associations,
within-session associations, and prediction for held-out hitters.

## Running

Run `notebooks/hitting/20_separation_bat_speed.ipynb` with the repository's
requirements installed. The notebook is standalone, code-only, and has no Python
comments. Its completed execution is saved so GitHub displays figures and tables.
Run All recomputes the analysis; it can also run outside the repository, using the
current working directory as its root.

The notebook reuses or downloads Dataset v1 `joint_angles.csv`, `joint_velos.csv`,
`metadata.csv`, and `poi_metrics.csv` under `data/raw/hitting/`. Missing signal
archives total approximately 155 MB; their SHA-256 checksums are verified before
extraction. Every input CSV is hashed in the run manifest. Raw C3Ds are not needed:
this version uses the published processed kinematics rather than reconstructing
an anatomical model from markers.

Run numerical checks with:

```bash
python -m unittest discover -s tests -p test_separation_bat_speed.py -v
```

## Measurements

The primary separation signal is the signed difference of unwrapped processed
pelvis and torso axial angles: **pelvis minus torso**. Positive values mean the
pelvis is farther rotated toward the mound. Difference wrapping is reconciled
before unwrapping; the already handedness-adjusted OBP angles are not mirrored
again. This difference is a proxy and is not identical to anatomical relative
rotation, muscle stretch, stored energy, or energy transfer.

The relative-rotation sensitivity uses **negative `torso_pelvis_angle_z`**, giving
the same intended pelvis-leading positive direction. Both definitions are retained
in the convention audit. POI `x_factor_fp_z` is compared descriptively, without
assuming it matches the signal-table foot-plant event or coordinate convention.
The discrepancy is not automatically treated as an error to repair. Published
angular velocities are used directly, rather than assuming they equal derivatives
of Euler axial angles; their disagreement with differentiated angles is exported
as a descriptive audit, not a pass/fail validity criterion.

| Metric | Definition |
|---|---|
| Maximum separation | Largest signed separation from 150 ms before front-foot contact through ball contact |
| Separation at plant/contact | Exact-event interpolated values |
| Peak separation timing | Milliseconds before contact; also percentage of plant-to-contact time, allowing negative percentages for pre-plant peaks |
| Separation closure | Maximum separation minus separation at contact |
| Onset lag | Torso sustained rotation onset minus pelvis sustained rotation onset, in milliseconds |
| Velocity peak lag | Torso minus pelvis directional angular-velocity peak time, each searched from plant through contact |
| Segment peak rates | Maximum published forward angular velocities from plant through contact |

The onset search starts 150 ms before front-foot contact and ends at the respective
segment's post-plant velocity peak. The threshold is the larger of 60 degrees/s
and 15% of that peak, sustained for at least 10 ms using actual timestamps. These
are analytical definitions, not measured swing initiation. A signal already above
threshold at the search boundary is left-censored; its onset and lag are missing,
not assigned to the boundary. No-onset and censored flags are exported separately.
Timing resolution is limited by the approximately 360 Hz sampled data and rounded
CSV timestamps. Peak timestamps are sampled maxima; exact ties select the first.

Plant-to-contact traces are interpolated to 101 points for figures. Rates, durations,
onsets and lags are computed on real-time grids before normalization. Each signal
table is processed on its own timestamps, with interpolated event boundaries.
Normalization does not supply velocities or erase pre-plant measurements.

## Eligibility

IDs and time keys must be unique. Metadata must identify hitter, session and side.
Events must be finite, constant within a trial, ordered, and consistent between
angle and velocity tables. Required windows must lie within the recording and
have at least two sampling intervals. Nonfinite interior samples and irregular
time grids fail extraction. Nonfinite leading/trailing derivative rows are trimmed
without imputation; the remaining signal must still cover the entire analysis
window. Events and gaps are never repaired.

Magnitude measurements survive missing onsets. Prediction models use the
intersection complete for controls, all five separation features, segment rates,
and the selected outcome, so every compared model uses the same swings and folds.
Outcome cohorts can differ. Per-feature association cohorts can also differ and
are explicitly counted. Nonpositive speeds and nonpositive body/bat dimensions
are treated as missing.

## Outcomes

- **Primary:** POI `bat_speed_mph_max_x`, OBP's published maximum resultant bat speed.
  Its exact maximum-search interval is not established by this notebook. It must
  not be described as a newly reconstructed pre-contact maximum or maximum bat
  angular velocity.
- **Secondary:** `bat_speed_mph_contact_x`, resultant bat speed at contact.
- **Secondary:** `blast_bat_speed_mph_x`, Blast Motion sensor speed, analyzed
  independently without filling missing values from either motion-capture metric.

The processed kinematics and primary speed share a measurement system. Agreement
with a separate sensor is useful context but does not eliminate measurement bias.

## Associations

Between-hitter rows average eligible swings within each hitter and use one row
per hitter. Spearman correlations are unadjusted. Separate per-feature OLS slopes
adjust height, mass, bat length and batting side, with HC3 intervals. Bat weight is
omitted **only from these inferential regressions**: 95 retained hitters have a
-3 oz bat drop and two have -2.5 oz; only one of those two remains in the Blast
cohort. Simultaneously adjusting bat length and weight creates unit leverage in
that cohort. Full-control slopes and maximum leverages are exported in the design
audit. All prediction models retain both bat length and bat weight.

Within-session analysis centers outcome, feature and plant-to-contact duration
within hitter/session/side groups with at least three complete swings. Weighted
regressions adjust centered duration, weight hitters equally, and cluster inference
by hitter. Separate joint regressions include all five centered magnitude/timing
features plus duration. These fixed-effect-style associations answer a different
question from held-out hitter prediction and do not estimate individual responses
to a coaching intervention. Stable body/bat properties are absorbed by centering.

Benjamini–Hochberg adjustments cover five feature tests within each outcome/level
family, and separately within each joint-outcome family. Sensitivity intervals are
exploratory and do not receive a blanket multiplicity correction. Leave-one-hitter
Spearman estimates assess influence, not independent replication.

## Prediction and incremental value

Models are a training-mean benchmark; body/bat controls; controls plus magnitude;
controls plus timing; controls plus both; controls plus pelvis/torso peak rates;
and controls plus rates and both separation groups. Bat and hand kinematics are
never predictors. Controls include height, mass, bat weight, bat length and side.

Two seeded repetitions use five outer hitter-disjoint folds and four inner folds.
Training-only, hitter-weighted scaling and ridge fitting are used. Inner held-out
hitter MAE chooses the ridge penalty. Whole hitters are kept out of training at
both levels. Every model within an outcome uses identical outer/inner partitions.
The analysis is retrospective and relies on known contact events.

Errors average equally across each hitter's swings and CV repeats, then equally
across hitters. Paired improvement is baseline MAE minus added-model MAE, so a
positive value favors added features. Intervals resample fixed paired hitter
errors 2,000 times, without repeating training or tuning, and therefore omit
model-refitting uncertainty. There is no external validation cohort.

## Sensitivities

Measurement checks vary onset floors (40/80 degrees/s), fractions (10%/20%),
lookback windows (100/200 ms), additional low-pass filtering (8/12/16 Hz), axial
versus relative rotation, a plant-to-contact duration screen (80–200 ms), and
omission of boundary separation peaks. Filtering uses precontact data with edge
padding, without follow-through samples beyond possible interpolation to contact.
These screens are analytical settings, not validated physiological limits.

Each measurement comparison matches swings and reports changes in hitter ranks,
between-hitter correlations and duration-adjusted within-session slopes/intervals.
Native-versus-relative predictive refits use their shared complete cohort and
identical folds. Duration-screen refits use a separate complete cohort and compare
models **within that cohort**; differences from full-cohort raw errors are not a
paired screening benefit. Predictive sensitivities use one seeded CV repeat.
An interior-peak predictive refit runs only if the screen changes eligibility.

## Reviewed Dataset v1 findings

The executed run retained **642 swings from 97 hitters**; 27 swings had missing or
inconsistent events and eight had invalid event chronology. One retained swing
had an unavailable onset lag. Primary grouped prediction used 641 swings from
97 hitters, and Blast prediction used 612 swings from 96 hitters.

For maximum bat speed, body/bat controls had held-out hitter-weighted MAE of
**3.468 mph**, versus **3.526 mph** after adding magnitude and timing. Paired
improvement was **-0.058 mph** (conditional 95% interval **-0.196 to +0.083**).
Adding separation to controls plus segment peak rates changed MAE by +0.007 mph
(interval -0.134 to +0.144). Neither establishes added predictive value.

Within-session, the separate maximum-separation model estimated **+0.258 mph per
degree** (hitter-clustered 95% interval +0.153 to +0.363), and plant separation
estimated +0.191 mph per degree (+0.092 to +0.290). Both survived their five-test
FDR family. These are conditional observational slopes, not effects of increasing
separation. The separate timing-of-maximum association did not survive its FDR
adjustment; onset and velocity-peak lag associations were also uncertain. In the joint within-session model, maximum separation remained associated with
speed (+0.295 mph/degree; interval +0.137 to +0.454), and earlier maximum
separation had a conditional association (+0.037 mph per additional ms before
contact; interval +0.009 to +0.065; FDR q=0.0245). These differ from the separate
feature estimates and should not be interpreted as independent replications.
Measurement-sensitivity estimates are exported to assess dependence on definitions.

Relative rotation shifted maximum-separation timing by a paired median **16.6 ms**
and gave hitter timing-rank agreement of **0.770** with the axial-angle difference.
The definitions should not be used interchangeably. Relative-rotation and duration
predictive checks did not establish that adding separation improves generalization.
Short sessions, limited athlete coverage and unmeasured pitch/impact context limit
player-level interpretation. No universal ideal separation or timing target is
established.

## Outputs

`results/separation_bat_speed/` contains swing measurements, exclusions, profiles,
convention/design audits, separate and joint associations, influence checks,
matched measurement sensitivities, model errors, paired comparisons, held-out
predictions, tuning choices, fold membership, cohort counts, input hashes and a
self-contained `study_summary.html`. Figures go to
`figures/separation_bat_speed/`. Both directories and raw inputs are ignored by Git.
The notebook retains its executed tables and figures for review.

Source definitions: [OBP hitting documentation](https://github.com/drivelineresearch/openbiomechanics/blob/main/baseball_hitting/README.md).
Review the [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
before using or distributing data or derived results.
