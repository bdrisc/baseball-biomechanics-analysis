# Head & Trunk Stability and Release Consistency

Study 15: [notebooks/pitching/15_head_trunk_release_consistency.ipynb](../notebooks/pitching/15_head_trunk_release_consistency.ipynb)

## Research question

Do pitchers with more repeatable head and trunk kinematics also have less dispersed hand-joint-center positions at ball release? How much of this association reflects global body positioning and pelvis translation, and does pelvis-relative head motion add information beyond trunk and pelvis variability?

**Scope:** release-position repeatability, not observed pitch command. The OpenBiomechanics dataset does not provide measured target locations or validated baseball positions at the release event. The hand joint center is a proxy, not the tracked baseball release point. These are observational associations rather than causal prescriptions.

## Data and setup

1. Install packages from [requirements.txt](../requirements.txt) and open the notebook from anywhere inside the cloned repository.
2. Run the cells in order. The notebook reuses local files in `data/raw/pitching/`; when `AUTO_DOWNLOAD=True`, missing official OBP Dataset v1 assets download and archive hashes are checked.
3. Required inputs: `metadata.csv`, `poi_metrics.csv`, `joint_angles.csv`, `landmarks.csv`, and `pitching_c3d.zip` (extracted to `data/raw/pitching/c3d/`). The C3D download can be large. No force-plate, video, or energy-flow archive is required.
4. Trial matching uses the exact anonymized C3D filename in `metadata.filename_new`; the matching pitch must also satisfy time-grid and quality checks. Never infer the processed pitch ID from the filename pitch number.
5. Generated analyses are saved locally in `results/head_trunk_release_consistency/` and plots in `figures/head_trunk_release_consistency/`; both are gitignored. Saved notebook outputs are cleared in the repository copy, so run all cells to reproduce the results.

## Definitions and methodology

- `BR_time` defines release; the final 100 ms are aligned to the event on a common 51-point time grid.
- The absolute head-center proxy is the centroid of C3D markers `LFHD`, `RFHD`, `LBHD`, and `RBHD`. The pelvis reference is the arithmetic centroid of `LASI`, `RASI`, `LPSI`, and `RPSI`. Neither measure provides head orientation or an anatomical pelvis joint center.
- Head centroids are smoothed with a fourth-order zero-phase Butterworth filter at 12 Hz. Sensitivity checks use 8 and 16 Hz; incomplete or inconsistent marker tracks are audited and excluded.
- Torso flexion/extension, lateral tilt, and axial rotation come from processed `torso_angle_x/y/z`.
- Global release-position dispersion is `sqrt(SD(hand_y)^2 + SD(hand_z)^2)` in centimeters, using across-pitch **sample SD** (`ddof=1`). Individual lateral and vertical SDs and 3D dispersion are supplementary. This is a within-session spread, not a measure of accuracy.
- Head and trunk release variability use across-pitch SD at `BR_time`. Pre-release trajectory RMS measures between-pitch trajectory variability; subtracting each trajectory's starting position produces a *shape* repeatability descriptor distinct from global position.
- The focused diagnostic compares absolute head/global hand, pelvis-relative head/global hand, global head/pelvis-relative hand, pelvis-relative head/pelvis-relative hand, and pelvis translation/global hand on **matched** session cohorts. Each axis (Y and Z) is also examined separately.
- The primary eligibility rule is at least four complete fastballs in a pitcher-session; three and five are sensitivity thresholds. Because Dataset v1 has only 2–5 fastballs per session, group estimates are noisy.
- Spearman correlations use pitcher/session bootstrap intervals. Adjusted OLS results use HC3 uncertainty; ridge models use repeated nested cross-validation holding out entire pitchers, with training-only scaling and alpha selection. Paired differences in held-out MAE are summarized by pitcher-bootstrap intervals.
- Leave-one-pitcher-out checks refit adjusted descriptive models and recompute correlations. Cross-validation influence checks *omit a pitcher from existing held-out predictions*, not from re-trained cross-validation models.

## Results from the executed October 17, 2026 notebook

| Metric | Observed result |
|---|---:|
| Available OBP fastballs | 411 / 100 pitchers |
| Matched usable trials | 408 |
| Primary sample (at least 4 complete pitches) | 324 pitches / 68 pitchers |
| Primary global head spread vs. global hand spread | Spearman rho = 0.820 |
| Trunk release SD vs. global hand spread | rho = 0.429 |
| Pelvis-relative head vs. global hand spread | rho = 0.462 |
| Pelvis-relative head vs. pelvis-relative hand spread | rho = 0.677 |
| Global head vs. global hand, lateral Y | rho = 0.865 |
| Global head vs. global hand, vertical Z | rho = 0.253 |

The strong global head–global hand relationship diminishes when the head is expressed relative to pelvis, suggesting that common body translation contributes substantially. Conversely, relative head and relative hand variables share the same pelvis subtraction; their association cannot be interpreted as independent head-to-hand coordination without accounting for this mathematical coupling.

**Held-out prediction:** With global hand dispersion as the target, adding *absolute head* variability to speed/height/pitch-count/pelvis/trunk controls lowered repeated grouped-CV MAE from 0.886 cm to 0.676 cm (improvement 0.210 cm; pitcher-bootstrap 95% interval 0.101 to 0.319). Adding *pelvis-relative head* variability instead lowered MAE from 0.886 to 0.860 cm (improvement 0.026 cm; interval -0.039 to 0.084). For pelvis-relative hand dispersion, relative head variability changed MAE from 0.671 to 0.604 cm (improvement 0.067 cm; interval -0.013 to 0.136).

**Adjusted exploratory models:** Relative head variability had a standardized coefficient of 0.328 cm (HC3 interval -0.010 to 0.667) for the global hand target and 0.489 cm (interval 0.200 to 0.778) for the pelvis-relative hand target. Multiple related comparisons were examined; do not interpret isolated p-values as confirmatory.

**Influence:** Removing one pitcher at a time yielded rho 0.812–0.836 for global/global, 0.438–0.498 for relative-head/global-hand, and 0.663–0.709 for relative/relative. No single pitcher drove the reported associations.

## Interpretation and limitations

- Head and hand positions in the same global lab reference frame can covary because the entire body has moved. Pelvis subtraction helps probe shared translation but also creates shared-denominator coupling when used on both sides of the association.
- Lateral associations exceed vertical associations in this sample; this is not evidence that vertical control is unimportant for pitch location.
- The pelvis four-marker centroid is not an anatomical joint center. Head translation is not head orientation, gaze, or perceptual stability.
- Each pitcher contributes only a few throws from essentially one assessment; session-level variability estimates are imprecise and may not generalize across days or games.
- There is no tracked baseball release position, pitch target, or plate-location outcome. Do **not** label these outcomes as command.
- Small held-out prediction differences are exploratory and do not establish causal impact, mechanical optimality, or individualized interventions.
- Raw data and derived trial/session tables are omitted from GitHub; rerun the notebook to regenerate them.

## Generated outputs

The notebook writes trial-eligibility audits, matched pitch feature tables, session feature tables, association and sample-size checks, nested-CV predictions and MAE comparisons, adjusted regressions, and run manifests in `results/head_trunk_release_consistency/`.

The pelvis-relative follow-up additionally writes matched-cohort comparisons, lateral/vertical screens, leave-one-pitcher-out influence diagnostics, and a focused manifest under `results/head_trunk_release_consistency/focused_pelvis_relative_diagnostic/`. Its four-panel scatter diagnostics, coordinate-specific estimates, model comparisons, and influence plots appear in `figures/head_trunk_release_consistency/focused_pelvis_relative_diagnostic/`.
