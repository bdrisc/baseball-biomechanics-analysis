# Attack Angle Repeatability

## Scope

Study 13 compares contact attack-angle variability across recorded OBP hitter sessions and playing levels. The measurement is the official POI `attack_angle_contact_x` in degrees. It is not a hand-path proxy, full bat-path reconstruction, or a measure of long-term swing reliability.

## Run

Place `13_swing_plane_consistency.ipynb` in `notebooks/hitting/` and run all cells using the repository environment. Required packages are NumPy, pandas, SciPy, and Matplotlib. IPython provides formatted notebook output; a plain-text fallback is included.

Inputs are `data/raw/hitting/metadata.csv` and `poi_metrics.csv`. Missing inputs download from the official Dataset v1 tag. Existing inputs are reused; SHA-256 values and package versions are saved in the manifest. Set `DATA_DIR_OVERRIDE` or `PROJECT_ROOT_OVERRIDE` in the first cell when using other folders. The notebook also runs outside the repository.

## Measurements

Trials join one-to-one on `session_swing`. Missing identities, unmatched trials, nonfinite angles, and angles outside the vertical -90 to +90 degree range are excluded and audited. Negative angles are retained. Missing or nonpositive outcomes exclude only the corresponding outcome analysis.

The primary metric is sample attack-angle SD within a hitter-session, using at least five valid swings. Unscaled median absolute deviation and interquartile range are also recorded. Hitter summaries average qualifying session estimates equally, keeping session-to-session changes separate from within-session variation. Group comparisons weight hitters equally.

The planned contrast is MiLB minus college mean hitter SD. High-school and independent groups are descriptive. Hitter-bootstrap intervals use 3,000 resamples; groups with fewer than five hitters receive no interval.

Outcome analyses use sessions with at least five paired angle/outcome trials. Three Spearman relationships examine mean exit velocity, exit-velocity SD, and mean bat speed. The notebook reports hitter-bootstrap intervals, raw p-values, and Benjamini-Hochberg q-values for the planned three-test family.

## Sensitivity and influence

Four-, five-, and six-trial eligibility thresholds test the minimum-count choice. Repeated sampling of exactly five trials per qualifying session checks count imbalance; the resulting ranges are subsampling ranges, not confidence intervals.

Leave-one-hitter-out checks remove all sessions belonging to each hitter. The group diagnostic omits each MiLB and college hitter, recalculating SD differences and conditional bootstrap intervals, plus MAD point estimates. Outcome diagnostics omit each hitter from the relevant paired cohort and recalculate Spearman rho. They do not select a preferred subset or replace the full-cohort p-values.

## Reviewed findings

The completed Dataset v1 run retained 661 swings from 94 hitters at the five-swing threshold. College hitters averaged 4.196 degrees SD (71 hitters); MiLB hitters averaged 2.868 degrees (7 hitters). The difference was -1.328 degrees, with a 95% bootstrap interval of -2.194 to -0.293 degrees.

All 78 individual group omissions preserved the negative SD difference. MiLB omissions ranged from -1.696 to -1.184 degrees; college omissions ranged from -1.360 to -1.201 degrees. None of their bootstrap intervals included zero.

The four-swing comparison and the full-cohort MAD comparison had intervals including zero. Six-swing eligibility left only three MiLB hitters. Outcome correlations were weak (rho -0.159, +0.200, and -0.017 respectively) and none passed the FDR adjustment.

## Interpretation

These results describe this laboratory sample. Playing level does not establish an elite-hitter classification. Seven MiLB hitters and few swings per hitter limit precision and generalization. Bootstrap intervals are conditional on estimated short-session SDs. Omission checks address individual influence rather than confounding or population representativeness.

Pitch height, location, and task demands can require appropriate changes in attack angle. The analysis does not adjust for those factors. Lower variability is not automatically better and does not justify a mechanical prescription.

## Outputs

CSV tables, the quality audit, run manifest, and generated interpretation are written to `results/swing_plane_consistency/`. Six PNG figures are written to `figures/swing_plane_consistency/`. Individual derived data and raw files remain local. Saved notebook outputs are cleared.

## Sources

- [OBP Dataset v1](https://github.com/drivelineresearch/openbiomechanics/releases/tag/dataset-v1)
- [Hitting documentation](https://github.com/drivelineresearch/openbiomechanics/tree/main/baseball_hitting)
- [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
