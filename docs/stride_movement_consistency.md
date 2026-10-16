# Pelvis and Torso Movement Consistency Before Landing

Run `notebooks/hitting/14_stride_movement_consistency.ipynb` with the repository requirements. The final notebook is code-only, with saved outputs cleared. It can run independently of the other studies, including outside the repository using the current working directory.

## Setup and data

Run all cells in order. The notebook reuses `data/raw/hitting/joint_angles.csv`, `metadata.csv`, and optional `poi_metrics.csv`. Missing official OpenBiomechanics Dataset v1 inputs download automatically. The joint-angle archive is checked against its expected SHA-256; input CSV hashes and settings are recorded in the run manifest. No C3D, landmarks, or joint-velocity archive is required. Set `AUTO_DOWNLOAD=False` to require local inputs.

Raw data and generated trial-level results are local outputs, not repository contents.

## Phase definitions and eligibility

The primary approach window is 150 ms before `fp_10_time` through `fp_10_time`; 100 and 200 ms are sensitivity settings. Landing runs from `fp_10_time` to `fp_100_time`. These official annotations describe front-foot loading at 10% and 100% bodyweight. They do not identify stride start or toe-off.

Approach requires a consistent finite foot-contact annotation. Landing additionally requires a consistent finite full-plant annotation after contact. Ball contact is not required for the primary extraction; it is examined separately in the chronology audit. A failed landing does not discard a valid approach measurement.

Each phase requires complete angle coverage, finite samples, a regular increasing time grid, and at least seven sampling intervals. Duplicate metadata IDs and angle ID/time keys fail explicitly. Events, omissions, and phase-specific reasons are exported. Exact boundaries are interpolated after angle unwrapping. The primary analysis uses the published processed traces without an additional filter.

Pelvis X is posterior (+)/anterior (-) tilt; torso X is extension (+)/flexion (-). These are published angle conventions, not a separate absolute forward-bend calibration or full 3D stability measure.

## Measurements

| Measurement | Definition |
|---|---|
| Angle SD | Time-weighted SD, integrated exactly for piecewise-linear angle interpolation |
| Net change | End angle minus start angle |
| Total angular travel | Sum of absolute consecutive angle changes on the native grid, including exact boundaries |
| Excess travel | Total travel minus absolute net change |
| Meaningful reversals | Hysteresis-based alternating excursions meeting the angular threshold, 0.5 degrees by default |
| Reversal frequency | Percentage of phase-valid session swings with at least one qualifying reversal |
| Absolute trajectory variability | RMS across 101 progress points of across-swing sample SD |
| Start-relative trajectory variability | The same calculation after subtracting each swing's starting angle |

The approach window has fixed duration and is aligned in actual milliseconds. Landing curves are normalized to 0–100% of their own duration, which can hide timing differences. Absolute and start-relative trajectories answer different repeatability questions.

Session profiles require five valid swings in the relevant phase. Swing metrics are summarized by session medians; reversal frequency uses all phase-valid swings. Profiles are averaged within hitter before cohort summaries so hitters receive equal weight. Cohort means, medians, and hitter-bootstrap intervals are exported.

Excess travel and reversal counts are descriptive path measures, not validated movement-smoothness scores. Angle SD includes genuine movement and does not independently establish instability.

## Robustness and exploratory outcomes

- Window sensitivity compares 100/150/200 ms on common retained swings.
- Additional 8/12/16 Hz zero-phase filters require 250 ms of context on each side. Phase-specific common cohorts are used for paired comparisons.
- Reversal thresholds of 0.25/0.5/1 degree expose dependence on the analytical rule.
- Four/five/six-swing minimums expose session-size dependence.
- Compact tables and plots report means, cohort sizes, ranking agreement, and absolute changes.

Between-hitter comparisons examine movement and repeatability against session outcome means/SDs, averaging sessions within hitter. Outcome summaries require at least five observations. Within-session comparisons subtract session means before pooled Spearman correlation; these estimates are swing-weighted. Intervals resample whole hitters with 1,000 draws. Motion-derived bat speed shares a measurement system with body angles. Pitch location and impact conditions are not fully controlled. The multiple comparisons are exploratory, without a significance-screening claim.

## Event chronology and influence audit

The focused case is hitter `000078`, session `000268`. Omitting each trial in turn identifies `268_8` as the main driver of trajectory variability. Its annotated foot contact is 61.2 ms after ball contact, putting ball contact inside the nominal approach window. Omitting it reduces that session's pelvis/torso start-relative trajectory SD from 7.236/9.334 to 0.653/0.388 degrees. Separate trial- and hitter-omission comparisons preserve the primary sample.

The broader chronology sensitivity applies one rule to every retained approach trial: omit IDs with consistent finite `fp_10_time > contact_time`. Those same IDs are omitted from both phase analyses, and session eligibility and outcome summaries are recomputed. Missing/inconsistent annotations are labeled uncheckable and retained in this sensitivity, not classified as confirmed chronology. This run had no uncheckable retained IDs.

The audit flags a window/event interpretation concern; it cannot determine which event is wrong. No event time is repaired. The full sample remains primary, and omission samples are nested influence checks rather than independent replications.

## Reviewed results

The complete Dataset v1 run retained 662 approach swings from 98 hitters and 635 landing swings. Five-swing eligibility retained 91 approach sessions and 86 landing sessions. Primary mean start-relative trajectory SD was 0.809 degrees for pelvis and 0.708 degrees for torso.

Excluding the 13 chronology-flagged IDs leaves 649 approach swings and 89 eligible sessions; landing retains 633 swings and 86 eligible sessions. Approach means become 0.717/0.572 degrees, while medians change from 0.647/0.500 to 0.645/0.493 degrees. This indicates greater influence on cohort averages than on the typical hitter's profile.

The eight main between-hitter correlations changed by at most 0.022 under this screen. Screened start-relative torso variability had correlations of -0.230 with mean bat speed and -0.261 with mean exit velocity; start-relative pelvis variability remained near zero. These results do not establish that reducing movement improves performance.

Approach trajectory ranking correlations under additional filters were 0.995–1.000. Comparing 100 ms with 150 ms gave 0.823 for pelvis and 0.865 for torso. Landing is unchanged by approach-lookback settings by construction. Reversal frequency depends on its threshold.

## Outputs and validation

Results are written to `results/stride_movement_consistency/`, including swing metrics, phase audits, session profiles, settings/minimum-size sensitivities, normalized trajectories, exploratory associations, interpretations, and a run manifest. The `focused_outlier_check/` and `chronology_sensitivity/` subdirectories contain the corresponding audits and recomputed comparisons. Figures use the parallel directory under `figures/stride_movement_consistency/`.

Inline checks cover exact-boundary interpolation, time-weighted SD, recovered travel, reversal thresholds/frequency, trajectory offsets, angle unwrapping, filtering, sampling gaps, nonfinite signals, independent phase eligibility, and chronology classification. The completed 13-cell notebook was run against the official dataset; figures, exclusions, cohort counts, and sensitivity outputs were reviewed. Saved outputs are cleared for reproduction.

This study describes within-session repeatability, not longitudinal reliability, full-stride motion, a mechanical quality grade, or causal performance effects.

See the [official hitting documentation](https://github.com/drivelineresearch/openbiomechanics/blob/dataset-v1/baseball_hitting/README.md), [movement smoothness discussion](https://doi.org/10.1186/s12984-015-0090-9), and [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md).
