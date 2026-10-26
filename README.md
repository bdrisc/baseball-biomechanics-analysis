# Baseball Biomechanics Analysis

This repository contains applied baseball biomechanics studies built with Python and Driveline Baseball's public [OpenBiomechanics Project](https://github.com/drivelineresearch/openbiomechanics). The analyses examine pitching sequencing, pitching release consistency, hitting posture, contact-point consistency, posture-change timing, hitting pelvis–torso rotation and uprighting onset, head movement and repeatability, delivery-phase profiles, swing-phase profiles, stride movement consistency, head/trunk/pelvis release-position repeatability, individual swing consistency profiles, lead-hand path shape through rotation, and lower-body movement strategies and ground reaction force estimation using raw and processed motion-capture, force-plate, and point-of-impact data.

The purpose of the project is to turn biomechanical time-series data into interpretable measures that can support player evaluation, research, and player-development conversations.

## Projects

| Study | Research question | Primary data | Notebook |
|---|---|---|---|
| Kinematic Sequencing and Velocity | How do directional rotation peaks, signed timing gaps, and observed sequence order relate to fastball velocity? | Pitching joint angular velocities, POI metrics, and metadata | [View notebook](notebooks/pitching/01_kinematic_sequencing.ipynb) |
| Trunk Stability and Release Consistency | Is greater trunk-angle variability at ball release associated with greater release-point dispersion? | Pitching joint angles, landmarks, and metadata | [View notebook](notebooks/pitching/02_trunk_stability_release.ipynb) |
| Hinge Integrity During the Stride | How much does the upper-body-to-thigh hinge angle change from pre-stride through front-foot plant? | Hitting landmarks and metadata | [View notebook](notebooks/hitting/03_hinge_integrity.ipynb) |
| Posture Loss and Contact-Point Consistency | Is greater post-plant posture loss associated with more variable hand position and HitTrax point-of-impact depth at contact? | Hitting landmarks, POI metrics, and HitTrax data | [View notebook](notebooks/hitting/04_posture_contact_consistency.ipynb) |
| Uprighting Velocity and Rotational Timing | How quickly do hitters change torso and pelvis posture after foot plant, and when do those peaks occur relative to axial rotation? | Hitting joint angles, joint angular velocities, POI metrics, and metadata | [View notebook](notebooks/hitting/05_uprighting_velocity.ipynb) |
| Pelvis–Torso Separation Timing | How long does the pelvis rotate before the torso begins sustained rotation toward the mound? | Hitting joint angles and metadata | [View notebook](notebooks/hitting/06_pelvis_torso_separation_timing.ipynb) |
| Head Movement, Repeatability & Batted-Ball Outcomes | Are within-session head movement and across-swing head repeatability associated with bat speed, exit velocity, and contact-depth variability? | Hitting C3D head/wrist markers, landmarks, metadata, POI, and HitTrax | [View notebook](notebooks/hitting/07_head_stability_contact_quality.ipynb) |
| Delivery Phase Profiles & Pitch Velocity | Which pre-release phases add held-out predictive information about fastball velocity, and how do selected joint energy estimates vary by phase? | Pitching angles, angular velocities, energy flow, metadata, and POI | [View notebook](notebooks/pitching/08_pitching_phase_decomposition.ipynb) |
| Pre-Landing Pelvis and Torso Bend Loss | How much posture change occurs before landing, and when does it begin relative to axial rotation? | Hitting joint angles, velocities, landmarks, metadata and POI | [View notebook](notebooks/hitting/11_stride_bend_loss.ipynb) |
| Swing Phase Profiles & Bat Speed | Which pre-contact windows add predictive information about bat speed, and how sensitive are results to phase definitions? | Hitting joint angles, angular velocities, metadata, and POI | [View notebook](notebooks/hitting/09_hitting_phase_decomposition.ipynb) |
| Pelvis–Torso Uprighting Offset | Does the pelvis begin uprighting before the torso, and how do first versus final movement episodes affect lag and consistency? | Hitting joint angles, metadata, optional POI and landmarks | [View notebook](notebooks/hitting/12_pelvis_torso_uprighting_offset.ipynb) |
| Attack Angle Repeatability | Do higher-level hitters show less contact attack-angle variability, and is the comparison sensitive to individual hitters? | Hitting metadata and official POI attack angles, bat speed, and exit velocity | [View notebook](notebooks/hitting/13_swing_plane_consistency.ipynb) |
| Stride Movement Consistency Before Landing | How do pelvis and torso movement amount, direction reversals, and within-session trajectory repeatability differ before foot contact and during landing? | Hitting joint angles, metadata, and optional POI outcomes | [View notebook](notebooks/hitting/14_stride_movement_consistency.ipynb) |
| Head & Trunk Stability and Release Consistency | How do head/trunk repeatability and pelvis translation relate to hand-release positional clustering, and does head stability add held-out predictive information? | Pitching C3D head/pelvis markers, joint angles, landmarks, metadata, and POI | [View notebook](notebooks/pitching/15_head_trunk_release_consistency.ipynb) |
| Individual Swing Consistency Profiles | How repeatable are a hitter’s pelvis and torso angle trajectories across reps, and how sensitive are profiles to phase duration? | Hitting joint angles, metadata, and optional POI context | [View notebook](notebooks/hitting/16_individual_swing_fingerprints.ipynb) |
| Lead-Hand Path Shape Through Rotation | How much does the lead wrist descend and travel around the hitter before contact, and how repeatable is its trajectory? | Hitting wrist/hip landmarks, metadata, and optional POI outcomes | [View notebook](notebooks/hitting/17_lead_hand_path_shape.ipynb) |

| Lower-Body Movement Strategies & Ground Reaction Force Estimation | Do lower-body kinematics add predictive information beyond modeled COM movement for selected pre-contact force measures in unseen hitters? | Hitting joint angles, modeled COM and other landmarks, force plates, metadata, and POI context | [View notebook](notebooks/hitting/18_lower_body_force_proxies.ipynb) |
| Pelvis–Torso Separation & Bat Speed | Do separation magnitude and timing relate to maximum bat speed between hitters, within sessions, and in held-out hitter models? | Hitting angles, angular velocities, metadata, and POI | [View notebook](notebooks/hitting/20_separation_bat_speed.ipynb) |

## Key Findings

### 1. Kinematic Sequencing and Velocity

- A clean run on the official Dataset v1 pitching files retained 402 of 411 fastballs from 100 pitchers. Eight had missing foot-plant events; one had foot plant after release. All valid peak orders and signed timing gaps are retained.
- Pelvis and torso rotation peaks are measured between foot plant and ball release. The shoulder internal-rotation peak is measured through 50 ms after release because 155 retained pitches peak in that extension. Fifteen retained pitches have a peak at a search-window boundary. The plotted curves remain normalized between foot plant and release.
- Shoulder internal rotation is a joint-level proxy, not upper-arm segment rotation. The selected positive shoulder velocity peak matches the official point-of-interest shoulder-IR measure (median absolute difference 0.0 deg/s). The pelvis-to-torso gap likewise matches the OBP timing field (median absolute difference 0.0 ms).
- The pitcher-weighted rate of observed pelvis–torso–shoulder-IR order was 75.3% in the higher-velocity group and 70.2% in the lower-velocity group. The bootstrap 95% interval for their 5.1 percentage-point difference was approximately -11 to +20 points. Pelvis-to-torso timing had little correlation with pitcher mean fastball velocity (`r = 0.028`, `p = 0.783`).
- Peak torso and shoulder internal-rotation velocities had exploratory positive pitcher-level correlations with pitch velocity (`r = 0.323` and `r = 0.292`, respectively). These multiple descriptive comparisons do not establish causation or a mechanical prescription.

### 2. Trunk Stability and Release Consistency

- Trunk kinematic variability and release-point dispersion had a moderate positive relationship (`r = 0.457`, `p = 0.0007`).
- The estimated slope was 0.00567 meters of additional release dispersion per degree of combined trunk variability.
- The 95% confidence interval for the slope was 0.00261 to 0.00873 meters per degree.
- Only sessions containing at least five pitches were retained.

### 3. Hinge Integrity During the Stride

- Of 677 available swings, 650 complete swings from 98 athletes met the event and data-quality requirements.
- The mean hinge angle was 157.75 degrees 150 ms before front-foot contact, 155.53 degrees at front-foot contact, and 162.67 degrees at front-foot plant.
- The swing-level mean change from pre-stride to front-foot plant was +4.91 degrees. The athlete-weighted estimate was +4.68 degrees, with an athlete-bootstrap 95% confidence interval of +2.46 to +6.91 degrees.
- Forty-eight percent of swings opened by more than 5 degrees, 31.2% remained within plus or minus 5 degrees, and 20.8% closed by more than 5 degrees.
- Athlete-level hinge change had exploratory correlations of `r = 0.25` with exit velocity and `r = 0.19` with bat speed. These associations are descriptive and should not be interpreted as causal.

### 4. Posture Loss and Contact-Point Consistency

- The notebook computes post-plant posture loss, time to peak trunk tilt, normalized hand position at contact, and HitTrax point-of-impact depth variability.
- The primary analysis aggregates swing-level metrics by athlete-session, retains sessions with at least five complete swings, and reports Spearman associations with athlete-level bootstrap intervals.
- The study is intentionally framed as an association and variability analysis. It does not label cut balls, measure true smash factor, or claim causation.
- In this sample, posture loss was not meaningfully related to hand-contact variability. Time to peak trunk tilt had a small positive association with HitTrax depth variability (`rho = 0.258`, unadjusted `p = 0.022`), but the result is exploratory and was one of three tested relationships.

### 5. Uprighting Velocity and Rotational Timing

- Of 677 available swings, 615 swings from 93 athletes met the event-window and signal-quality requirements. Eighty-four athlete-sessions contained at least five retained swings for the outcome analysis.
- Median peak torso uprighting velocity was 484.3 degrees per second; median peak pelvis posterior-tilt velocity was 353.0 degrees per second.
- The median torso uprighting peak occurred 33.3 ms after peak torso axial rotation. Uprighting lagged rotation by more than 20 ms in 72.8% of swings, occurred within plus or minus 20 ms in 26.2%, and led by more than 20 ms in 1.0%.
- Peak torso uprighting speed was not clearly related to bat speed, exit velocity, or attack angle. A later uprighting peak relative to rotation had a modest association with bat speed (`rho = 0.284`, unadjusted `p = 0.009`, FDR-adjusted `q = 0.053`) and is treated as exploratory.
- Results were stable across 8 Hz, 12 Hz, and 16 Hz filter choices: peak-speed rank correlations were 0.986–0.998 and median absolute timing differences were 0.0–2.7 ms.

### 6. Pelvis–Torso Separation Timing

- An exploratory notebook detects sustained pelvis and torso axial rotation onset using filtered joint-angle time series and reports the signed onset lag and positive-only separation window.
- Of 677 available swings, 615 from 93 athletes passed the event and signal filters. The pelvis reached the sustained rotation threshold first in 614 swings; one was torso first. Median pelvis-first onset lag and the median of athlete-level medians were both 50.0 ms.
- With 8–16 Hz filters, the median signed lag was 50.0–52.8 ms and 99.7–100% of retained swings were classified pelvis first. Changing the tested absolute rate floor from 40 to 80 degrees per second did not change the retained count or median at a given cutoff.
- Plots show angles and angular rates with onset markers, sampled row indices, and front-foot contact/plant/ball-contact events. These are sample descriptions under a specific onset threshold; they do not establish an ideal separation window or a causal relation to hitting performance.

### 7. Head Movement, Repeatability & Batted-Ball Outcomes

- The notebook estimates translation using the centroid of four head markers (`LFHD`, `RFHD`, `LBHD`, `RBHD`). It separates movement within a swing from repeatability across swings; it does not measure gaze, head orientation, or true contact efficiency.
- C3D filename swing numbers do not always equal processed `session_swing` IDs. Joins require athlete/session/handedness agreement, identical frame counts and time grids, and a close match between C3D wrist-marker midpoints and processed wrist-center trajectories. Ambiguous or unmatched trials are excluded and audited.
- A full Dataset v1 run matched 669 C3D trials to the 677 processed swings and retained 624 swings from 96 athletes after event and marker-quality checks. At 12 Hz, median maximum head displacement from foot plant through contact was 6.09 cm.
- The primary model compared 581 complete swings within 83 athlete-sessions, accounting for bat speed at contact. The estimated exit-velocity difference was +0.12 mph per additional one percentage point of body-height-normalized head displacement, with an athlete-bootstrap 95% interval of -0.26 to +0.49 mph. This sample did not show a clear relationship between greater head displacement and exit velocity conditional on bat speed.
- Head-trajectory repeatability and exit-velocity variability had a weak session-level association (`rho = 0.138`, bootstrap 95% interval -0.092 to +0.355). Contact-depth variability had an exploratory positive association (`rho = 0.261`, interval +0.034 to +0.459), but pitch location can also affect contact depth. These findings do not establish an ideal head movement or a causal coaching prescription.
- Movement rankings were stable across 8, 12, and 16 Hz filters (rank correlations at least 0.997 for the tested metrics). The notebook also checks four-, five-, and six-swing minimums for repeatability estimates.

The [study guide](docs/head_stability.md) explains setup, metric definitions, quality checks, model interpretation, and generated outputs.

### 8. Delivery Phase Profiles & Pitch Velocity

- Segments landing (foot contact to foot plant), cocking (foot plant to maximum external rotation), acceleration (maximum external rotation to release), and descriptive early follow-through (release to maximum internal rotation). Only pre-release features enter velocity models.
- A full Dataset v1 run retained 402 of 411 fastballs from 100 pitchers. Nine pitches had missing or unordered pre-release events. A separate sensitivity excludes five pitches with unusually long phase annotations, retaining 397 pitches from the same 100 pitchers.
- Repeated nested validation holds out whole pitchers: five outer folds, four inner folds, two seeded repeats. Scaling and ridge penalty selection use training data only. Prediction errors weight pitchers equally.
- The all-phase kinematic model had held-out MAE of 2.97 mph, compared with 3.69 mph for the body-size baseline. Adding selected joint energy-flow features reduced MAE to 2.28 mph on the same 402-pitch cohort. The paired pitcher-bootstrap improvement was 0.69 mph (95% interval 0.31–1.06).
- Removing acceleration kinematics increased MAE by 0.30 mph in the full sample, while removing cocking increased it by 0.23 mph. In the long-phase sensitivity, cocking had the larger point estimate. This does not establish a stable single phase winner or a causal contribution to ball speed.
- Power signals are integrated over real seconds to estimate mass-normalized generation, absorption, and separate signed transfer channels at the lead knee, shoulder, and elbow. Estimates are cross-checked against official POI summaries; sampling/definition differences are reported rather than assumed away. No whole-body energy total or percentage of velocity is calculated.

See the [phase study guide](docs/phase_decomposition.md) for definitions, validation limits, setup, and output descriptions.

### 9. Swing Phase Profiles & Bat Speed

- Uses official foot-contact, foot-plant, and contact events, a fixed 150 ms approach window, and analytical early/late post-plant splits at 40%, 50%, and 60% of plant-to-contact time. Follow-through is descriptive only; these fractions are not annotated swing-initiation events.
- The primary analysis retained 642 of 677 swings from 97 hitters. Thirty-five swings had missing or unordered official events. Nested validation holds out entire hitters, fits scaling/tuning within training folds, repeats two seeded splits, and weights hitters equally.
- At the 50% split, contact-bat-speed MAE was 3.28 mph for all phases versus 3.47 mph for body/bat controls. The paired improvement was 0.19 mph with a conditional bootstrap interval of -0.11 to +0.51 mph; additional value over controls is uncertain.
- Early post-plant features had the largest phase-ablation estimate across the three analytical boundaries in the main sample. Their removal increased MAE by 0.29 mph at the 50% split. After excluding 27 swings outside 80–200 ms plant-to-contact, the estimate fell to 0.03 mph with an interval crossing zero. No robust single phase winner or causal coaching prescription is established.
- Blast speed (613 swings, 96 hitters) and exit velocity (637 swings, 96 hitters) are separate secondary outcomes. Bat kinematics and post-contact features are not predictors. This study connects posture, separation, and body-joint movement; head-marker analysis remains in study 07.

See the [hitting phase study guide](docs/hitting_phase_decomposition.md) for setup, exact definitions, findings, and limitations.

### 12. Pelvis–Torso Uprighting Offset

- Compares first sustained uprighting with the final qualifying positive-rate episode approaching contact. Signed lag is torso onset minus pelvis onset; positive values mean pelvis first.
- The reviewed Dataset v1 run retained 642 of 677 swings from 97 hitters. The first-onset detector returned 640 pairs and a median swing lag of +2.7 ms. The final-episode detector returned 642 pairs, a median swing lag of 0.0 ms, and a median hitter lag of 0.0 ms (hitter-bootstrap 95% interval -5.6 to +5.5 ms).
- Final onset order was pelvis first in 42.7% of swings, torso first in 41.9%, and unresolved within one sample interval in 15.4%. The combined duration sensitivity retained 544 swings and also had a median final lag of 0.0 ms.
- A +716.6 ms first-onset offset reflected an early pelvis movement paired with later torso uprighting. Selecting the final episode yielded +2.7 ms for that trial. This changes the operational measurement rather than establishing a ground-truth onset.
- Final-episode order was unchanged among comparable detected pairs under 10/30/50 ms contact-gap choices. Relative-threshold and filter choices still changed individual labels: roughly 85–87% agreement for tested relative thresholds and 75% at 8 Hz.
- Performance associations were generally weak; one restricted within-session bat-speed association was exploratory among multiple comparisons. No universal pelvis-first sequence, ideal lag, or causal performance benefit is established.

See the [uprighting-offset study guide](docs/pelvis_torso_uprighting_offset.md) for definitions, duration audits, findings, setup, and output descriptions.

### 13. Attack Angle Repeatability

- Measures official contact attack-angle variability within hitter-sessions. It does not measure full 3D bat-path or swing-plane consistency.
- The reviewed Dataset v1 run retained 661 swings from 94 hitters with at least five valid swings per session. College hitters (71) averaged 4.20 degrees of within-session attack-angle SD; MiLB hitters (7) averaged 2.87 degrees.
- The MiLB minus college difference was -1.33 degrees, with a conditional hitter-bootstrap 95% interval of -2.19 to -0.29 degrees. The four-swing sensitivity and robust MAD comparison had intervals including zero; the six-swing threshold retained only three MiLB hitters.
- Omitting each MiLB hitter produced differences from -1.70 to -1.18 degrees; omitting each college hitter produced differences from -1.36 to -1.20 degrees. No omission reversed the difference, and all 78 SD omission intervals remained below zero. These are influence checks, not independent replications.
- Associations with mean exit velocity, exit-velocity variability, and mean bat speed were weak and did not pass the three-test FDR adjustment. The small MiLB cohort, short sessions, and unmeasured pitch context limit generalization.

See the [repeatability study guide](docs/swing_plane_consistency.md) for setup, measurements, sensitivity checks, and output descriptions.

### 14. Stride Movement Consistency Before Landing

- Separates within-swing angle variability, net change, excess angular travel, threshold-confirmed direction reversals, and across-swing trajectory repeatability. Greater movement is not automatically less repeatable or mechanically worse.
- Uses a fixed 150 ms window before front-foot contact, with 100/200 ms sensitivities, and a separate contact-to-full-plant landing phase. Each phase has independent event and signal eligibility. The fixed window is not measured stride onset or the entire stride.
- The reviewed Dataset v1 run retained 662 approach swings from 98 hitters and 635 landing swings. Ninety-one approach sessions and 86 landing sessions met the five-swing minimum. Hitter-weighted mean start-relative trajectory SD was 0.809 degrees for pelvis and 0.708 degrees for torso in the approach window.
- An event audit identified 13 approach trials with annotated foot contact after ball contact. A consistent sensitivity omits those trial IDs, recomputes session/outcome profiles, and retains 649 approach swings with 89 eligible sessions. Mean pelvis/torso trajectory SD falls to 0.717/0.572 degrees, while medians change little (0.647/0.500 to 0.645/0.493 degrees). The full sample remains primary; annotations are not repaired.
- The eight main between-hitter correlations changed by at most 0.022 under the chronology screen. Screened start-relative torso variability had exploratory associations of `rho = -0.230` with mean bat speed and `rho = -0.261` with mean exit velocity. Start-relative pelvis variability was essentially unrelated to either. These are observational, multiple exploratory comparisons.
- Approach trajectory rankings were stable under additional 8/12/16 Hz filters (rank correlations 0.995–1.000), but more sensitive to window length. Reversal frequency depends on the chosen angular threshold. The study does not establish an ideal movement pattern, a validated smoothness/quality score, or test–retest reliability.

See the [stride movement study guide](docs/stride_movement_consistency.md) for definitions, event audits, influence checks, setup, and outputs.

### 15. Head & Trunk Stability and Release Consistency

- In the executed OpenBiomechanics Dataset v1 run, 408 of 411 fastballs passed head-marker, trunk-angle, and hand-joint-center extraction. The primary four-pitch minimum retained 324 pitches across 68 independent pitcher-sessions; three- and five-pitch sensitivities retained 90 and 52 sessions.
- The primary outcome is *lateral/vertical dispersion of the throwing-hand joint center at the release event*, not tracked baseball location or target accuracy. Within-session Spearman correlations with this dispersion were `rho = 0.820` for absolute head-position variability and `rho = 0.429` for trunk-angle variability.
- The focused matched-session diagnostic found `rho = 0.462` for pelvis-relative head variability versus global hand dispersion and `rho = 0.677` when *both* head and hand positions were measured relative to pelvis. Shared whole-body translation contributes to the global correlation, while subtracting the same pelvis position from both measurements also introduces mathematical coupling.
- Lateral associations were substantially stronger than vertical associations: absolute head vs. absolute hand variability was `rho = 0.865` on the lateral axis versus `rho = 0.253` vertically. These axis-specific results are exploratory.
- In repeated, pitcher-held-out nested ridge validation, adding absolute head variability to speed/height/pitch-count/pelvis/trunk controls reduced global hand-dispersion MAE from 0.886 to 0.676 cm (paired improvement 0.210 cm, pitcher-bootstrap 95% interval 0.101–0.319). Pelvis-relative head variability improved the same model by only 0.026 cm (interval -0.039 to 0.084). For pelvis-relative hand dispersion, the corresponding relative-head improvement was 0.067 cm (interval -0.013 to 0.136).
- Leave-one-pitcher-out correlation ranges were 0.812–0.836 (absolute/absolute), 0.438–0.498 (pelvis-relative head/global hand), and 0.663–0.709 (relative/relative). Results describe a small observational assessment sample of 2–5 fastballs per pitcher, not command, causal mechanics, or a player-specific coaching rule.

See the [head/trunk release consistency study guide](docs/head_trunk_release_consistency.md) for source files, matching and eligibility criteria, metric definitions, diagnostics, validation, and interpretation.

### 16. Individual Swing Consistency Profiles

- The executed Dataset v1 run retained 627 of 677 available swings and produced 85 hitter-session-side profiles at a five-swing minimum. Pelvis/torso tilt and axial rotation are overlaid across approach, landing, and post-plant phases, with absolute and phase-start-relative views.
- Mean ±1 sample-SD bands, pointwise spread, RMS trajectory SD, phase durations, leave-one-out swing distances, and omission diagnostics describe individual patterns without a combined quality grade. The HTML report supports session selection and swing highlighting.
- A pooled Q3 + 3×IQR duration audit flagged 74 landing intervals above 158.5 ms and no post-plant intervals. The primary sample is preserved; omitting flagged swings leaves 553 swings and 73 eligible profiles. Landing caps of 200/300/400 ms leave 573/596/612 swings and 75/80/84 profiles. These are sensitivity settings, not physiological validity limits.
- Some profiles are sensitive to individual reps: absolute pelvis-rotation trajectory SD during landing falls by 10.067 degrees for hitter `000130` under the statistical or 200 ms screen. Lost session eligibility is reported separately from matched-profile changes. The focused session `000009` / `000123` exceeds every tested landing cap and is reviewed in real time without repairing annotations.
- Minimums of four/five/six swings yield 92/85/62 profiles. The study describes within-session repeatability, not causal performance benefits, longitudinal reliability, or validated iPhone measurements.

See the [individual consistency study guide](docs/individual_swing_fingerprints.md) for definitions, eligibility, audit design, reviewed findings, and outputs.

### 17. Lead-Hand Path Shape Through Rotation

- Operationalizes the supplied “down and around” observation through separate vertical movement, 3D arc length, pelvis-relative horizontal sweep, final-20-ms hand-path direction, curvature, and trajectory repeatability. The lead wrist joint center is a hand-path proxy, not tracked barrel motion or bat attack angle.
- The reviewed Dataset v1 run retained all 677 swings for the fixed final 100 ms and produced 94 hitter-session-side profiles at a five-swing minimum. Plant-to-contact extraction retained 641 swings and 87 profiles. Fixed contact windows remain eligible independently of foot-event availability.
- With primary 12 Hz processing, hitter-weighted pelvis-relative final-100-ms means were −1.60 cm net drop (a net rise), 6.52 cm maximum downward excursion, 69.48 cm arc length, and 72.47° signed horizontal sweep. Earlier descent and net movement through contact are distinct measurements.
- Filter/window choices and landmark selection are explicitly audited. Replacing the wrist with the hand joint center increased net drop by a paired median 7.42 cm and arc length by 10.91 cm. No ideal path or causal performance benefit is established.
- A standalone HTML report supports hitter/session selection, coordinate-frame switching, swing highlighting, overhead paths, color-coded depth-height trajectories, and height variability bands.

See the [hand-path study guide](docs/lead_hand_path_shape.md) for definitions, reviewed findings, sensitivity checks, setup, and outputs.

### 18. Lower-Body Movement Strategies & Ground Reaction Force Estimation

- The executed Dataset v1 run retained 645 swings from 96 hitters. Force targets cover contact minus 150 ms through contact minus 10 ms, with motion and force signals measured on their own sampling grids.
- Repeated nested validation holds out entire hitters, fits scaling/tuning inside training folds, and weights hitters equally. Primary features do not use force-derived landing timestamps; an assisted benchmark and measurement audit are separate.
- For total vertical-force peak, training-calibrated COM physics had held-out MAE of 0.1643 bodyweights (BW), versus 0.1774 BW for the full lower-body + COM model. The full model's paired MAE improvement was -0.0132 BW (conditional hitter-bootstrap 95% interval -0.0264 to +0.0006), so added value beyond the simpler benchmark is not established.
- For lead vertical-force peak, COM-only and full-model MAEs were 0.1704 and 0.1630 BW; the paired improvement interval included zero. For lead braking impulse, COM-only performed better: 0.01052 versus 0.01211 BW·s. Adding lower-body features has not demonstrated a consistent predictive benefit beyond COM features in these models.
- The retained-trial audit flagged two near-zero lead-force windows and 19 landing/plant chronology concerns. Their union contains 20 swings. Separate omission sensitivities preserve the primary results and do not repair annotations; refitting did not clearly improve predictions on identical surviving trials.
- Eighty-six hitter profiles formed two overlapping descriptive clusters (silhouette 0.187; median swing-resampling ARI 0.821). Peak-force timing remained weak. These findings do not establish ideal mechanics, causal coaching prescriptions, full force waveforms, or validity for phone video.

See the [force-proxy study guide](docs/lower_body_force_proxies.md) for model comparisons, measurement definitions, validation limits, setup, and generated outputs.

### 20. Pelvis–Torso Separation Magnitude, Timing & Bat Speed

- The final executed study separates within-session associations, between-hitter comparisons and prediction for held-out hitters. Main measurements retained 642 swings from 97 hitters; the matched definition/sensor audit retained 610 swings from 94 hitters.
- Maximum separation had positive within-session associations with published maximum and Blast speed under both axial-angle-difference and relative-rotation definitions. After conditioning on duration and pelvis/torso peak angular velocities, slopes ranged from +0.186 to +0.289 mph per degree; all four hitter-bootstrap intervals were above zero and survived their FDR family. No single-hitter omission reversed the coefficient direction. These are observational associations, not coaching effects.
- Timing was definition-sensitive: the separate within-session slope for earlier maximum separation was +0.030 mph/ms with the axial-angle difference, versus +0.004 mph/ms with relative rotation; the latter interval included zero. A general timing target is not established.
- Separation did not clearly improve held-out prediction. Body/bat control MAE was 3.468 mph, versus 3.526 mph with magnitude and timing; paired improvement was -0.058 mph (conditional 95% interval -0.196 to +0.083). The strongest magnitude associations do not establish a reliable predictive gain or a causal benefit from increasing separation.
- The final nine-cell notebook retains executed tables and figures, a consolidated evidence summary and supporting analyses. Run All produces an HTML report with expandable appendices. It is code-only, has no Python comments and requires no raw C3D download.

See the [study guide](docs/separation_bat_speed.md) for definitions, matched comparisons, inference procedures, validation and interpretation.

## Repository Structure

```text
baseball-biomechanics-analysis/
├── notebooks/
│   ├── pitching/
│   │   ├── 01_kinematic_sequencing.ipynb
│   │   ├── 02_trunk_stability_release.ipynb
│   │   ├── 08_pitching_phase_decomposition.ipynb
│   │   └── 15_head_trunk_release_consistency.ipynb
│   └── hitting/
│       ├── 03_hinge_integrity.ipynb
│       ├── 04_posture_contact_consistency.ipynb
│       ├── 05_uprighting_velocity.ipynb
│       ├── 06_pelvis_torso_separation_timing.ipynb
│       ├── 07_head_stability_contact_quality.ipynb
│       ├── 09_hitting_phase_decomposition.ipynb
│       ├── 11_stride_bend_loss.ipynb
│       ├── 12_pelvis_torso_uprighting_offset.ipynb
│       ├── 13_swing_plane_consistency.ipynb
│       ├── 14_stride_movement_consistency.ipynb
│       ├── 16_individual_swing_fingerprints.ipynb
│       ├── 17_lead_hand_path_shape.ipynb
│       ├── 18_lower_body_force_proxies.ipynb
│       ├── 19_rotation_onset_orientation.ipynb
│       └── 20_separation_bat_speed.ipynb
├── src/
│   └── obp_utils.py
├── data/
│   ├── README.md
│   └── raw/                 # Local only; excluded from Git
├── figures/
├── requirements.txt
└── README.md
```

## Running the Project

Clone the repository and create a virtual environment:

```powershell
git clone https://github.com/bdrisc/baseball-biomechanics-analysis.git
cd baseball-biomechanics-analysis
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Download the required OpenBiomechanics files separately and place them under `data/raw/pitching/` and `data/raw/hitting/`. Exact filenames and locations are documented in [data/README.md](data/README.md). Raw data are intentionally excluded from this repository.

Run the notebooks in numerical order. The notebooks contain reproducible workflows. The revised sequencing notebook was run against the official Dataset v1 pitching files for the findings above, but its saved outputs are cleared to avoid stale results when users run it on their own local files. Raw data are not committed; the hitting notebooks download missing official Dataset v1 inputs when run locally. The head-stability notebook requires `ezc3d` and `statsmodels` (included in requirements), downloads roughly 498 MB of C3D and landmark archives on its first run, and reuses local inputs thereafter. Its saved outputs are cleared; running all cells creates the plots and CSV summaries. It also works as a standalone notebook, using the current working directory when the repository is absent.

The phase-decomposition notebook requires `scikit-learn` (included in requirements). It automatically downloads roughly 115 MB of missing processed pitching archives, reuses local files, and runs independently of the earlier notebooks. Saved notebook outputs are cleared.

The hitter phase notebook also uses `scikit-learn`, downloads roughly 155 MB of missing hitting archives, and runs independently. Its code-only notebook has cleared outputs. Running all six cells creates results, profiles, and plots under `results/hitting_phase_decomposition/` and `figures/hitting_phase_decomposition/`.

Study 12 is a standalone, code-only notebook using the existing hitting joint-angle and metadata CSVs, with optional POI outcomes and a synchronized landmark animation. Missing official inputs download automatically and archive checksums are verified. Saved outputs are cleared; Run All generates local CSVs, figures, and HTML under `results/pelvis_torso_uprighting_offset_v3/` and `figures/pelvis_torso_uprighting_offset_v3/`. Its measurement checks run with `python -m unittest discover -s tests -p test_uprighting_offset.py -v`.

Study 13 is a standalone, code-only notebook using hitting metadata and POI CSVs. Missing Dataset v1 CSVs download automatically; local inputs are reused and hashed in the run manifest. Saved outputs are cleared. Run All writes CSVs and an interpretation under `results/swing_plane_consistency/`, and six figures under `figures/swing_plane_consistency/`. No C3D or full-signal archives are required.

Study 14 is a standalone, code-only notebook using hitting joint angles, metadata, and optional POI outcomes. Missing official inputs download automatically; the angle archive checksum is checked and input hashes are exported. Run All writes measurements, phase exclusions, sensitivity tables, event audits, and interpretations under `results/stride_movement_consistency/`, with plots under `figures/stride_movement_consistency/`. Outputs are cleared. No C3D or landmark archive is required. Numerical measurement and chronology-classification checks run inside the notebook.

Study 15 is a standalone, code-only pitching study requiring C3D head/pelvis markers, processed joint angles, landmarks, metadata, and POI metrics. The notebook downloads missing Dataset v1 inputs and verifies archive SHA-256 hashes. Its saved outputs are cleared; Run All writes extraction audits, session summaries, correlations, grouped model diagnostics, influence tests, and manifests under `results/head_trunk_release_consistency/`, and charts under `figures/head_trunk_release_consistency/`. The downloaded raw C3Ds may be large. See [the study guide](docs/head_trunk_release_consistency.md).

Study 16 is a standalone, code-only hitting notebook with no Python comments and cleared outputs. It uses joint angles, metadata, and optional POI context, downloads missing official inputs, verifies the angle archive, and records input hashes. Run All creates CSV profiles, duration audits, sensitivity comparisons, selected-session plots, and an interactive HTML report under `results/individual_swing_fingerprints/` and `figures/individual_swing_fingerprints/`. Optional notebook widgets are supported; the standalone HTML report needs no additional package. See the [study guide](docs/individual_swing_fingerprints.md).

Study 17 is a standalone, code-only hitting notebook with no Python comments and cleared outputs. It uses wrist/hip landmarks and metadata, with optional POI context. Missing Dataset v1 inputs download automatically; the roughly 66 MB landmark archive is verified before extraction and input CSV hashes are recorded. Run All creates measurements, profiles, filter/window/landmark sensitivities, duration and eligibility audits, figures, and a self-contained HTML profile report under `results/lead_hand_path_shape/` and `figures/lead_hand_path_shape/`. See the [study guide](docs/lead_hand_path_shape.md). Measurement checks run with `python -m unittest discover -s tests -p test_lead_hand_path_shape.py -v`.

Study 18 is a standalone, code-only hitting notebook with no Python comments. Its completed run is saved in the notebook so GitHub displays the charts, tables, and closing report. It automatically downloads missing Dataset v1 joint-angle, landmark, and force-plate archives (about 168 MB total), metadata, and POI files. Archive checksums and local input hashes are recorded. Run All generates grouped model comparisons, force-signal audits, omission sensitivities, movement profiles, figures, and a consolidated HTML summary under `results/lower_body_force_proxies_v3/` and `figures/lower_body_force_proxies_v3/`. Numerical and fold checks run inside the notebook. See [the study guide](docs/lower_body_force_proxies.md).

## Methods and Interpretation

The pre-landing bend-loss notebook (`11_stride_bend_loss.ipynb`) measures signed
pelvis/torso change in a fixed 150 ms window before front-foot contact, with
100/200 ms sensitivities, separate landing changes, censored onset estimates,
hitter/session summaries, and a synchronized landmark animation. The fixed
window is not measured toe-off or the full stride. See
[the methods and setup](docs/stride_bend_loss.md). Outputs are cleared; running
all cells downloads missing official inputs and generates local results.

The notebooks use event-based filtering, interpolation or temporal normalization, athlete/session aggregation, descriptive statistics, correlation analysis, regression, sensitivity testing, and bootstrap uncertainty estimates. These are observational analyses of the available OBP sample. Their findings identify associations and sample-level tendencies, not causal mechanical prescriptions for individual athletes.

## Data Source and License

Data come from Driveline Baseball's [OpenBiomechanics Project](https://github.com/drivelineresearch/openbiomechanics). The source project distributes code and data under separate licenses. Anyone reproducing these analyses should review the current [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md) and citation guidance before using the dataset.

No OpenBiomechanics raw data are redistributed in this repository.

## Author

Brendan Driscoll  
[GitHub](https://github.com/bdrisc)
