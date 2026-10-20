# Study 17: Lead-Hand Path Shape Through Rotation

## Question and scope

How much does the lead hand descend and travel around the hitter between foot plant and contact, and how repeatable is that trajectory within a hitter-session-side?

The motivating observation supplied for this project was a “down and around bat path.” This study operationalizes its downward and around-body components using a **lead-wrist joint-center proxy**. No article URL, author, or full text was supplied; this is an independent measurement design inspired by that excerpt, not a replication or validation of the article. Hand motion cannot establish barrel motion, bat attack angle, time in the hitting zone, or mechanically desirable movement.

## Run

Open `notebooks/hitting/17_lead_hand_path_shape.ipynb` and Run All using the repository requirements. The standalone, code-only notebook contains no Python comments or Markdown cells. Saved outputs are cleared.

Missing official Dataset v1 hitting inputs download automatically:

- `data/raw/hitting/landmarks.csv`, extracted from the roughly 66 MB `hitting_landmarks.zip` release asset. Its published SHA-256 is checked before extraction.
- `data/raw/hitting/metadata.csv` for exact `session_swing`, hitter, session, batting side, and body height.
- Optional `data/raw/hitting/poi_metrics.csv` for bat-speed and exit-velocity context. Set `LOAD_OPTIONAL_OUTCOMES=False` to omit these analyses.

Set `AUTO_DOWNLOAD=False` to use existing local inputs only. Raw C3Ds, joint angles, force plates, and camera video are unnecessary. Input CSV SHA-256 hashes and processing settings are saved in the run manifest. Existing local CSVs are reused and hashed rather than silently replaced; equivalence to the official data is not inferred from their names.

The notebook can run independently from the current directory if the repository is absent. `MIN_SWINGS=5` controls profile eligibility. `SELECTED_PROFILE=None` chooses the first eligible final-100-ms profile deterministically; supply a `(hitter_id, session_id, hitter_side)` tuple to select another. The generated HTML report includes every eligible final-100-ms profile.

## Data and coordinate conventions

Source: [OBP Dataset v1 hitting documentation](https://github.com/drivelineresearch/openbiomechanics/blob/dataset-v1/baseball_hitting/README.md) and [Dataset v1 release](https://github.com/drivelineresearch/openbiomechanics/releases/tag/dataset-v1).

- Processed landmark positions are in metres. Lengths are exported in centimetres. A hip-height plausibility check detects gross unit mismatches; it does not calibrate the measurements.
- X points toward the pitcher, Y toward the right-handed batter's box, and Z upward. These laboratory coordinates differ from HitTrax's axis conventions.
- Right-handed hitter: select `lwjc_x/y/z`. Left-handed hitter: select `rwjc_x/y/z`. Anatomical selection precedes mirroring.
- Left-handed Y coordinates are multiplied by −1 for comparable displays and sweep signs; X and Z are unchanged. Batting sides remain separate profile groups.
- The pelvis reference is the midpoint of `left_hip` and `right_hip` joint centers. It is an analytical hip midpoint, not a tracked pelvis marker or an exact anatomical pelvis origin.
- Global and moving-hip-midpoint-relative paths are both retained. Pelvis subtraction removes translation; it does **not** rotate the axes with the pelvis. The relative trajectory still contains body rotation.
- `lhjc/rhjc` hand joint centers are used only in a separate landmark-choice sensitivity. Wrist and hand centers are not interchangeable, and neither is the bat's sweet spot.

Metadata and POI swing keys must be unique; landmark swing/time pairs must be unique. Missing identity fields stop the run. Exact processed `session_swing` keys are used throughout.

## Windows and eligibility

The primary configurations are full foot plant to contact (`plant`) and the fixed final 100 ms (`late100`). Plant windows require consistent, ordered `fp_10_time < fp_100_time < contact_time` annotations. The final-100-ms window depends only on valid contact timing and signal coverage; missing or disordered foot events do not exclude it.

Each window requires at least 20 ms and seven sample intervals, complete coverage, increasing time, near-regular sampling, finite selected precontact wrist and hip coordinates, and contact within the recording. Invalid signals are excluded rather than interpolated across gaps. Analytical endpoints are interpolated between adjacent source observations; no trajectory is extrapolated. Each configuration/window receives a retained or exclusion-reason audit row.

The processed time grid is rounded, so interpolation to a uniform grid accommodates ordinary 0.0027/0.0028-second alternation. Primary smoothing is an additional fourth-order 12 Hz Butterworth SOS filter applied forward/backward separately to wrist and hip coordinates across the entire available precontact recording. The filter reflects at the contact boundary and does not use the later follow-through recording. A sample bracketing an off-grid contact time may contribute to endpoint interpolation. This is retrospective geometry, not a real-time estimator. Terminal angles remain sensitive to endpoint handling.

Profiles use 101 equally spaced times within each window. Fixed windows share real contact-relative time; plant windows are normalized by duration. Metric calculation uses the much denser uniform-time trajectory with interpolated endpoints, not only the 101 display points.

## Measurements

| Export field | Definition |
|---|---|
| `net_drop_cm` | 100 × (starting Z − contact Z). Positive is down; negative is a net rise. |
| `max_drop_cm` | 100 × (starting Z − lowest Z within the window). Includes an initial descent followed by recovery. |
| `lowest_height_time_ms` | Time of minimum height relative to contact; first minimum is selected on ties. |
| `arc_length_cm` | Sum of Euclidean distances along the full 3D trajectory, multiplied by 100. Not depth-height projected length. |
| `horizontal_sweep_deg` | Unwrapped final minus initial `atan2(Y,X)` around the moving hip midpoint. Positive is counterclockwise in handedness-normalized XY. Only computed for pelvis-relative paths, and unavailable if horizontal radius falls below 5 cm. Signed net sweep is not cumulative angular travel or isolated torso rotation. |
| `approach_angle_deg` | Least-squares 3D velocity over the final 20 ms; `atan2(vertical velocity, horizontal speed)` in degrees. Upward is positive. Unavailable below 0.1 m/s total fitted speed. This is hand-path direction, not bat attack angle or measured contact-zone entry. |
| `mean_curvature_per_m` | Speed-weighted mean of `norm(v × a) / norm(v)^3` over interior samples faster than 0.1 m/s. Two samples at each endpoint are omitted. Velocities/accelerations use second-order numerical gradients in real seconds. A descriptive processing-dependent shape measure. |
| `trajectory_rms_sd_cm` | Square root of the average across time of the sum of the three coordinate sample variances; multiplied by 100. Includes starting-position differences. |
| `start_relative_trajectory_rms_sd_cm` | Same measure after subtracting each swing's own window-start position. |

Drop and arc length are also exported as percentages of recorded body height. Per-profile means and sample SDs describe swings within hitter/session/side. Metric means omit unavailable individual metric values; profile counts refer to retained trajectories. SD bands depict observed across-swing spread, not confidence intervals, normal ranges, or test–retest reliability.

## Sensitivities and uncertainty

- Repeat measurements without additional smoothing and with 8/16 Hz cutoffs. “Raw” means the published processed coordinates without this notebook's additional filter; it does not mean unprocessed optical observations.
- Compare fixed 75/125 ms windows against final 100 ms on exactly matched swings.
- Replace the lead wrist center with the lead hand joint center in a separate sensitivity.
- Compare each metric using paired median signed change, median absolute change, matched count, and Spearman rank correlation, separately by window and coordinate frame. These are swing-level diagnostics, not independent-athlete inferential tests.
- Recompute profile eligibility with four/five/six swings. Report lost eligibility rather than treating profiles as interchangeable cohorts.
- Flag plant-to-contact intervals outside 80–200 ms and export separately recomputed profiles after omitting them. These bounds are analytical sensitivity settings, not physiological validity limits. Primary annotations and results remain intact.
- For population summaries, average sessions/sides within hitter, then weight hitters equally. Conditional 95% percentile bootstrap intervals resample whole hitters 1,000 times with seed 20261020. These describe this assessment sample and pipeline, not universal normative values.

Exploratory outcome analysis first averages eligible profile means within hitter and reports Spearman associations for three prespecified features (drop, arc length, horizontal sweep), two windows, and two outcomes. Benjamini–Hochberg adjustment spans all reported tests. It is a between-hitter analysis, not a within-hitter effect or predictive validation. Body size, contact height, pitch location, and playing level are not adjusted; no coaching prescription follows from these associations.

## Reviewed Dataset v1 run

- All 677 swings passed final-100-ms extraction. The five-swing minimum produced 94 hitter-session-side profiles from 94 hitters. Plant extraction retained 641 swings: 35 had missing/disordered foot events and one had a window shorter than the measurement minimum. Plant profiles numbered 87.
- With the primary 12 Hz processing, hitter-weighted pelvis-relative final-100-ms means were **−1.60 cm net drop** (a net rise), **6.52 cm maximum downward excursion**, **69.48 cm arc length**, **72.47° signed horizontal sweep**, and **+13.79° precontact approach angle**. Descent earlier in a window and net movement at contact answer different questions.
- Plant-to-contact pelvis-relative means were +3.58 cm net drop, 11.77 cm maximum excursion, 79.48 cm arc length, and 80.55° horizontal sweep. These use a different eligible cohort and time window; they are not paired phase comparisons.
- The no-additional-filter final-100-ms comparison had median absolute differences of 0.41 cm in drop, 0.55 cm in arc length, and 3.98° in approach angle. The 8 Hz filter reduced arc length by a median 10.82 cm versus 12 Hz. Absolute measurements, especially terminal direction, depend on processing choices even where rankings are similar.
- Replacing wrist with hand joint center increased final-100-ms net drop by a paired median 7.42 cm and arc length by 10.91 cm. This substantial landmark-choice sensitivity is a reason to retain the explicit **lead-wrist proxy** label, not evidence that either center is a validated bat-path measure.
- The plant duration screen flagged 26 intervals below 80 ms; none exceeded 200 ms. Four/five/six-swing thresholds yielded 98/94/68 final-100-ms profiles and 94/87/64 plant profiles.

These results do not establish that every hitter moves down through contact, that more drop/curvature is better, or that hand direction matches barrel direction.

## Outputs

Under `results/lead_hand_path_shape/`:

- `swing_measurements.csv`: every retained configuration/window/frame measurement and optional POI context.
- `eligibility_audit.csv`: retained trials and explicit exclusions.
- `session_profiles.csv`: profile counts, metric means/SDs, and primary trajectory spread.
- `hitter_weighted_summary.csv`: equal-hitter means and conditional bootstrap intervals.
- `matched_sensitivity.csv`: paired filter/window/landmark comparisons.
- `minimum_swing_sensitivity.csv`: four/five/six-swing profile counts and spread summaries.
- `duration_review.csv`, `duration_screened_profiles.csv`: primary duration flags and separately recomputed screened profiles.
- `exploratory_outcome_associations.csv`: between-hitter associations and adjusted p-values.
- `lead_hand_profiles.html`: self-contained profile selector with frame switching, swing highlighting, overhead paths, depth-height overlays, color-coded timing, and height bands. Opens offline with no external scripts.
- `run_manifest.json`: input hashes and processing provenance.

Under `figures/lead_hand_path_shape/`: `selected_hitter_profile.png` and `hitter_distributions.png`. Generated figures, reports, per-swing data, and raw source data remain local and are ignored by Git.

## Measurement verification

Run `python -m unittest discover -s tests -p test_lead_hand_path_shape.py -v` from the repository root. Six tests cover analytical straight-line/circular geometry, angle wrapping, descent/rebound, pelvis translation, anatomical side selection and left/right symmetry, independent fixed-window eligibility, malformed signals/coverage, postcontact filtering independence, and near-origin sweep rejection. Analytical checks also execute inside the notebook.
