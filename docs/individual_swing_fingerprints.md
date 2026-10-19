# Individual Swing Consistency Profiles

Study 16 describes how one hitter reproduces pelvis and torso angle trajectories within a session. It extends Study 14's stride analysis through ball contact and produces a selectable assessment report rather than a mechanical quality grade.

## Setup

Run all ten cells of `notebooks/hitting/16_individual_swing_fingerprints.ipynb` using the repository requirements. The notebook is code-only, has no Python comments, and has cleared saved outputs. It runs independently of earlier notebooks and also supports execution outside the repository using the current working directory.

Inputs are `data/raw/hitting/joint_angles.csv` and `metadata.csv`. Optional `poi_metrics.csv` supplies bat speed and exit velocity for context only. Missing official OpenBiomechanics Dataset v1 files download automatically. The downloaded joint-angle archive is checked against its expected SHA-256; hashes of reused CSVs are recorded in the run manifest. No C3D, landmarks, joint velocities, force-plate archive, or video is required.

Set `AUTO_DOWNLOAD=False` to require local inputs or `LOAD_OPTIONAL_OUTCOMES=False` to skip outcomes. `MIN_VALID_SWINGS` defaults to five, with four- and six-swing eligibility sensitivities. `SELECTED_HITTER_SESSION` accepts an eligible `(hitter_id, session_id, hitter_side)` tuple of strings; `None` selects the first eligible profile.

The HTML report includes every eligible session and works without external scripts. Open `results/individual_swing_fingerprints/individual_swing_fingerprints.html` in a browser to select a session, switch between absolute and start-relative angles, and highlight an individual swing. Highlighting changes the display only. Optional `ipywidgets` controls provide previews in compatible notebook environments; the HTML report does not require that package.

## Events, signals, and eligibility

| Phase | Boundaries |
|---|---|
| Approach | Fixed 150 ms before `fp_10_time` through `fp_10_time` |
| Landing | `fp_10_time` through `fp_100_time` |
| Post-plant | `fp_100_time` through `contact_time` |

The foot events describe the published front-foot loading annotations. The approach is not measured stride onset or the full stride. All three events must be finite, consistent within a trial, and strictly chronological. Each phase requires at least seven sampling intervals. Complete coverage, regular increasing time grids, finite values in all four channels, and a unique metadata match are required. Duplicate metadata IDs and angle ID/time keys fail explicitly.

Channels are `pelvis_angle_x`, `torso_angle_x`, `pelvis_angle_z`, and `torso_angle_z`. Pelvis X is posterior (+)/anterior (-) tilt; torso X is extension (+)/flexion (-). Z angles retain the source conventions. Batting sides are analyzed separately rather than silently mirrored or pooled.

Each retained swing supplies all phases and channels, so their primary cohort is consistent. Curves are unwrapped and interpolated to 101 points within each phase. Whole-curve shifts of 360 degrees align phase starting branches within a session. The primary analysis uses the published processed signals without additional smoothing.

Separate phase normalization preserves event boundaries but hides duration differences. Phase duration means, SDs, and ranges are therefore reported in real milliseconds. The focused duration diagnostic also plots trajectories against time relative to ball contact.

## Profile measurements

| Measurement | Definition |
|---|---|
| Absolute curves | Retain differences in starting angle and movement |
| Start-relative curves | Subtract each swing's own starting angle separately within each phase |
| Across-swing band | Session mean ± one pointwise sample SD, using `ddof=1` |
| RMS trajectory SD | Square root of the trapezoidal integral of pointwise sample variance over 0–1 phase progress |
| Peak SD and location | Largest pointwise SD and its phase progress percentage |
| Event angle SD | Across-swing SD at the phase start and end |
| Leave-one-out distance | RMS difference between one swing and the mean curve of every other retained session swing in that channel, phase, and angle view |
| Omission influence | Change in RMS trajectory SD after removing one swing |

Pelvis, torso, posture, rotation, and timing measures remain separate; no combined consistency score is calculated. SD bands describe observed spread, not confidence intervals or normal-mechanics ranges. Start-relative curves reset at each phase boundary and should not be read as one continuous baseline-referenced swing.

Omission diagnostics explicitly report remaining sample size and whether it meets the original reporting minimum. They can describe four remaining swings in a primary five-swing session without treating that diagnostic as an eligible primary report. Unusual reps are candidates for review, not automatic errors.

## Duration audit and sensitivity design

The audit flags landing and post-plant durations above pooled complete-swing `Q3 + 3 × IQR`, with those fences frozen before screening. The fixed-duration approach is not screened. These are statistical review flags, not physiological validity labels; event annotations and primary profiles are preserved.

Five secondary scenarios apply the statistical fence, landing caps of 200/300/400 ms, or a post-plant cap of 200 ms. Fixed caps are analytical sensitivity settings, not validated limits. Each scenario omits the same trial IDs from every phase, channel, and angle view, then recomputes session profiles with the original minimum.

Paired changes compare the same surviving hitter-session-side profiles before and after screening. Lost profiles are exported in a separate eligibility table; they do not silently disappear into cohort averages. Summaries include median paired and absolute changes, the 90th percentile and maximum absolute change, and descriptive rank agreement. These comparisons do not establish test–retest reliability.

Lookback sensitivity compares 100/150/200 ms approach windows on common complete swings, with session eligibility recalculated. Landing and post-plant results remain unchanged on that common cohort. Four/five/six-swing sensitivities expose dependence on reporting eligibility.

## Reviewed Dataset v1 results

The executed run retained 627 of 677 swings and produced 85 eligible hitter-session-side profiles at the five-swing minimum. Fifty trials were excluded: 15 had missing/inconsistent foot-contact events, 12 had missing/inconsistent full-plant events, eight had unordered events, 14 had landing phases shorter than seven sampling intervals, and one had a post-plant phase below that minimum.

Landing duration had a median of 44.5 ms and an upper review fence of 158.5 ms. Seventy-four retained swings exceeded that fence. Post-plant duration had a median of 127.8 ms, a 205.1 ms upper fence, and no flags.

| Scenario | Retained swings | Eligible profiles | Lost primary profiles |
|---|---:|---:|---:|
| Primary | 627 | 85 | 0 |
| Statistical upper fence | 553 | 73 | 12 |
| Landing ≤200 ms | 573 | 75 | 10 |
| Landing ≤300 ms | 596 | 80 | 5 |
| Landing ≤400 ms | 612 | 84 | 1 |
| Post-plant ≤200 ms | 627 | 85 | 0 |

Individual effects can be substantial: hitter `000130`, session `000273`, left-handed, had a 10.067-degree reduction in absolute pelvis axial-rotation trajectory SD during landing under the statistical fence or 200 ms landing cap, with six swings reduced to five. This is an influence result, not proof that an omitted rep was invalid.

The focused hitter `000009`, session `000123`, right-handed, had nine landing intervals ranging from 441.7 to 647.2 ms, averaging 509.6 ms. Every swing exceeds each landing cap, so this profile loses eligibility in those scenarios. Its actual-time plots show an extended interval preceding the rapid pre-contact motion; they cannot independently establish whether an annotation is incorrect.

All 627 primary swings were available for each tested approach lookback. Minimums of four, five, and six swings yielded 92, 85, and 62 eligible profiles respectively.

## Outputs and verification

Main outputs go to `results/individual_swing_fingerprints/`: swing features, session counts, curve and timing metrics, leave-one-out distances, omission influence, lookback/minimum sensitivities, compressed normalized trajectories, interpretation, input hashes/settings, and the interactive HTML report. Selected-session figures go to `figures/individual_swing_fingerprints/`.

The `phase_duration_audit/` subdirectories contain trial/session duration flags, distributions, scenario membership, cohort counts, eligibility attrition, screened profiles, paired changes and summaries, audit settings, focused trial durations, and plots. Duration review notices are also shown within the primary HTML report.

The complete workflow was executed on official Dataset v1 inputs. Inline checks cover exact phase boundaries, angle wrapping, offset-versus-shape separation, sample SD, leave-one-out references, malformed event order, short windows, sampling gaps, missing signals, and window coverage. Additional checks verify nested duration cohorts, reporting eligibility, and unchanged comparisons when a screen omits no swings. Report selection, both angle views, and swing highlighting were functionally checked across all 85 sessions; saved figures were visually reviewed.

Generated data and reports remain local and ignored by Git. Running the cleared notebook regenerates them.

## Interpretation limits

This study describes within-session repeatability, not an ideal swing, mechanical quality, a causal coaching prescription, or a persistent biometric identity. Five-swing estimates can be sensitive to individual reps. Pitch context and assessment conditions are not fully controlled. Optional bat speed and exit velocity are context, with no fitted performance association.

The source measurements are motion-capture angles. Single-view iPhone computer vision does not directly recover these 3D axial angles; camera view, occlusion, event timing, accuracy, and repeated-session agreement need separate validation before transferring the workflow to phone-derived proxies.

Source: [OpenBiomechanics](https://github.com/drivelineresearch/openbiomechanics), [Dataset v1](https://github.com/drivelineresearch/openbiomechanics/releases/tag/dataset-v1), and [data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md).
