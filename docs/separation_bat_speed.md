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

## Matched sensor and definition robustness audit

Maximum and plant separation are compared on the same complete swings under the
axial-angle-difference and relative torso–pelvis definitions, against published
maximum, contact and Blast speed. Eligibility requires all three outcomes, both
magnitude metrics under both definitions, and at least three complete swings per
hitter/session/side. The reviewed common cohort contains 610 swings from 94 hitters.
Missing outcomes are never filled from another measurement system.

Regressions center predictors and outcomes within session/side, adjust centered
plant-to-contact duration and weight hitters equally. Two thousand whole-hitter
bootstrap samples refit the centered regressions. Identical resampling draws
preserve paired definition/sensor comparisons. Per-hitter sufficient statistics
reproduce direct weighted least squares; removing a hitter's contribution refits
the slope exactly. Numerical checks compare these calculations with direct fits.
Omission sign stability does not mean every omitted-sample confidence interval
excludes zero.

FDR adjustment covers six cluster-robust coefficient tests separately for maximum
and plant separation. Paired slope contrasts are exploratory, without multiplicity
adjustment. They are not external replications or causal comparisons.

## Adjustment for segment peak angular velocities

The same matched cohort is checked for complete pelvis/torso peak rates. In the
reviewed run all 610 swings and 94 hitters remain. Each magnitude/definition/outcome
combination is fitted twice: separation plus duration, and separation plus duration
plus both segment peak angular velocities. All variables are centered within the
same session/side groups and hitters remain equally weighted.

Duration and velocity columns are rescaled by fixed constants for numerical
conditioning; the separation slope remains in mph per degree. Two thousand paired
whole-hitter bootstrap samples refit both models. Slopes, paired changes, omission
ranges and design diagnostics (condition number, remaining separation variance and
VIF) are exported. Full-rank and direct-fit equivalence checks run in the notebook.
FDR covers six tests within each magnitude/model family. Paired slope-change
intervals remain exploratory. Conditioning on contemporaneous rates changes the
association being estimated; this is not causal mediation or proof of a mechanism.

## Final Dataset v1 findings

The main extraction retained **642 swings from 97 hitters**; 27 swings had missing
or inconsistent events and eight had invalid chronology. One retained swing had
an unavailable onset lag. Primary grouped prediction used 641 swings from 97
hitters; Blast prediction used 612 swings from 96 hitters. The matched robustness
and velocity-adjustment audits used **610 swings from 94 hitters**. These cohorts
answer different questions and should not be combined as independent evidence.

### Magnitude: consistent within-session association

After adjusting duration and both segment peak rates on the matched cohort:

| Separation definition | Outcome | Slope (mph/degree) | 95% hitter-bootstrap interval | FDR q |
|---|---|---:|---|---:|
| Axial-angle difference | Published maximum speed | +0.289 | +0.196 to +0.402 | <0.001 |
| Axial-angle difference | Blast speed | +0.227 | +0.059 to +0.394 | 0.013 |
| Relative torso–pelvis rotation | Published maximum speed | +0.241 | +0.145 to +0.381 | <0.001 |
| Relative torso–pelvis rotation | Blast speed | +0.186 | +0.033 to +0.351 | 0.021 |

All four coefficient directions remained positive after omitting each hitter.
Contact-speed results were also positive. Within these sessions, greater maximum
separation was associated with higher speed across the tested definitions and
measurement systems, including after conditioning on segment rotation rates.
This does not establish an individual response to increasing separation.

### Timing: sensitive to the definition

The separate duration-adjusted within-session slope for earlier maximum separation
was +0.030 mph/ms with the axial-angle difference (hitter-clustered interval +0.002
to +0.059), versus +0.004 mph/ms with relative rotation (-0.008 to +0.015). The
native separate timing test did not survive its five-test FDR family. A conditional
joint-model timing association was present for the native definition, but remains
exploratory and does not establish a general timing target.

Relative rotation shifted peak-separation timing by a paired median 16.6 ms and
gave hitter timing-rank agreement of 0.770 with the axial-angle difference.
The definitions are not interchangeable.

### Prediction: no clear added value

For published maximum speed, body/bat controls had held-out hitter-weighted MAE
of **3.468 mph**, versus **3.526 mph** with magnitude and timing. Paired improvement
was **-0.058 mph** (conditional 95% interval **-0.196 to +0.083**). Controls plus
segment peak rates had MAE of 3.328 mph, versus 3.321 mph after adding separation;
paired improvement was +0.007 mph (interval -0.134 to +0.144). Neither comparison
establishes added predictive value. Conditional error intervals and refitted
association intervals quantify different uncertainties.

### Player-development interpretation

Separation magnitude can support descriptive review of a hitter's swings alongside
rotation rates and context. The study does not justify prescribing extra
separation, a universal angle, a timing target or an expected mph gain. Short
sessions, restricted athlete coverage, shared measurement systems, measurement
error and unmeasured pitch/impact context limit inference. Omission stability does
not establish test–retest reliability, external validity or a coaching response.

## Outputs

`results/separation_bat_speed/` contains swing measurements, exclusions, profiles,
convention/design audits, separate and joint associations, influence checks,
matched measurement sensitivities, model errors, paired comparisons, held-out
predictions, tuning choices, fold membership, cohort counts, input hashes and a
self-contained `study_summary.html`. Figures go to
`figures/separation_bat_speed/`. Both directories and raw inputs are ignored by Git.
The final nine-cell notebook retains its executed tables and figures for review.
The closing evidence summary includes compact magnitude, timing and predictive
comparisons, interpretation and scope. The generated HTML report leads with this
summary and puts detailed tables in expandable supporting sections.

Additional outputs include `robustness_matched_swings.csv`,
`robustness_within_session_slopes.csv`, `robustness_hitter_omissions.csv`, paired
sensor/definition contrasts and bootstrap arrays; velocity-adjusted slopes,
matched cohort, paired changes, omissions and collinearity diagnostics; and
`final_magnitude_summary.csv`, `final_timing_summary.csv`,
`final_prediction_summary.csv` and `final_conclusions.txt`. Final evidence figures
are `final_magnitude_evidence.png` and `final_timing_prediction.png`.

Source definitions: [OBP hitting documentation](https://github.com/drivelineresearch/openbiomechanics/blob/main/baseball_hitting/README.md).
Review the [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
before using or distributing data or derived results.
