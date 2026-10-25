# Lower-Body Movement Strategies and Ground Reaction Force Estimation

## Run

Open `notebooks/hitting/18_lower_body_force_proxies.ipynb` after installing the repository requirements and run all 16 cells in order. The notebook is code-only, contains no Python comments, and has cleared outputs. It runs independently of the earlier studies and can use the current directory outside the repository.

Missing official OpenBiomechanics Dataset v1 inputs download automatically: hitting joint angles, landmarks, force plates, metadata, and POI metrics. The three signal archives total about 168 MB; extracted CSVs need additional space. Archive SHA-256 values are verified, and reused input hashes are recorded. Set `AUTO_DOWNLOAD=False` for local-only inputs. No C3D or video files are needed.

## What is measured

Primary features and targets use the window from 150 ms before recorded ball contact to 10 ms before contact. This is a retrospective assessment window, not a whole-swing maximum or live forecast. Contact alignment and upstream signal processing remain part of the measurement assumptions.

| Measure | Definition |
|---|---|
| Lead vertical-force peak | Maximum lead-force Z, normalized to bodyweight |
| Total vertical-force peak | Maximum of summed lead/rear Z force, normalized to bodyweight |
| Lead braking impulse | Integral of the positive component of negative lead-force X, normalized to bodyweight, in BW·s |
| Lead-force peak timing | Time of maximum lead vertical force relative to recorded contact |
| COM features | Changes, velocities, and accelerations from the published modeled COM trajectory |
| Lower-body features | Pelvis translation, hip/knee motion and timing, and stance geometry |

The published `centerofmass_x/y/z` coordinates are model-derived COM estimates, not hip-midpoint coordinates. The hip midpoint is used separately for pelvis movement. Knee/hip extension rates negate flexion-angle derivatives. Pelvis/torso rotation rates are angle derivatives, not rotational power or torque.

Marker-derived data are sampled at 360 Hz and force at 1,080 Hz. Features and targets use their own checked time grids and exact interpolated boundaries. There is no exact-time inner join across sampling rates. Additional 8/12/16 Hz motion filters and 120/150/180 ms lookback settings expose processing sensitivity.

Primary predictors do not use force-derived foot-contact/plant events. A kinematic ankle-settling detector and an explicitly force-assisted official-plant benchmark are separate comparisons. Post-contact source traces appear only in measurement review figures.

## Models and validation

Five outer folds hold out entire hitters; four inner folds select ridge penalties. Two seeded repetitions expose fold sensitivity. Scaling and tuning use training data only, with equal hitter fitting/scoring weights. Main comparisons use identical trials, observed targets and outer hitter assignments.

The body-control model uses height, mass and handedness. COM-only ridge adds COM features; the full model adds pelvis/joint and stance features. Unfitted total-force physics uses the peak of `1 + COM vertical acceleration / g`; calibration is learned only within training folds. This formula does not allocate forces to individual feet.

Conditional intervals resample fixed per-hitter held-out errors. They omit full retraining uncertainty and are not multiple-comparison adjusted. These are exploratory comparisons within one dataset, not external validation of a retrospectively selected model.

## Reviewed findings

The completed run retained 645 swings from 96 hitters.

| Outcome | Simpler benchmark | Benchmark MAE | Full-model MAE | Full-model improvement, conditional 95% interval |
|---|---|---:|---:|---|
| Total vertical peak (BW) | Calibrated COM physics | 0.1643 | 0.1774 | -0.0132 [-0.0264, +0.0006] |
| Lead vertical peak (BW) | COM features + controls | 0.1704 | 0.1630 | +0.0074 [-0.0061, +0.0217] |
| Lead braking impulse (BW·s) | COM features + controls | 0.01052 | 0.01211 | -0.00158 [-0.00279, -0.00049] |

Positive improvement favors the full model. Additional lower-body features did not demonstrate a consistent advantage beyond the COM benchmarks. The COM-only braking model had lower error in both validation repeats and in rescoring sensitivities.

Peak-force timing was weak: full-model MAE was 18.00 ms versus 18.11 ms for the training-mean baseline. Eighty-six eligible hitter profiles formed two overlapping clusters, with silhouette 0.187 and median swing-resampling ARI 0.821. Stable resampled assignments do not establish distinct biological strategies or ideal mechanics.

## Force audit

Two primary windows had near-zero lead force. Trial `268_8` had substantial loading elsewhere in the recording and annotated foot contact/plant after recorded bat contact. Trial `378_8` had near-zero lead force throughout the recording. These patterns require review; they do not establish which annotation, plate assignment, or other source detail is wrong.

The broader audit flagged 19 chronology concerns. Their union with near-zero windows contains 20 swings. The combined omission sensitivity retained 625 swings from 95 hitters, preserving original outer fold assignments. Neither omission sensitivity clearly improved refitted-model error on identical surviving trials. No source timestamps or force signals are repaired; the full cohort remains primary.

Lead-loading screen checks rescore fixed predictions rather than refitting the COM-only models. Removing unusual outcomes changes the evaluation distribution and cannot by itself establish a better model.

## Outputs and interpretation

Results and the consolidated `study_summary.html` go to `results/lower_body_force_proxies_v3/`; figures go to `figures/lower_body_force_proxies_v3/`. Exports include measurements, eligibility reasons, force flags, folds, tuning records, predictions, paired comparisons, profile/resampling diagnostics, and input/package manifests. Raw and generated trial-level data stay local.

Numerical and validation checks run inside the notebook, including force signs and normalization, exact-boundary integration, event sampling without extrapolation, primary independence from foot-event annotations, uniform differentiation grids, hitter-disjoint folds, and matched comparison cohorts.

This study estimates selected window-specific force measures from processed optical motion capture. It does not establish a substitute for force plates, full force waveforms, muscle-force estimates, rotational power, causal coaching interventions, longitudinal reliability, or validity for phone video.

Sources: [OBP Dataset v1 hitting documentation](https://github.com/drivelineresearch/openbiomechanics/tree/dataset-v1/baseball_hitting), [model provenance](https://github.com/drivelineresearch/openbiomechanics/blob/dataset-v1/baseball_hitting/code/v3d/CMO.v3s), and [data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md).
