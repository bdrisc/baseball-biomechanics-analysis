# OpenBiomechanics Data Setup

Raw data are not stored in this repository. Download the required files from Driveline Baseball's official [OpenBiomechanics repository](https://github.com/drivelineresearch/openbiomechanics) and [Dataset v1 release](https://github.com/drivelineresearch/openbiomechanics/releases/tag/dataset-v1).

## Required Files

```text
data/
└── raw/
    ├── pitching/
    │   ├── metadata.csv
    │   ├── poi_metrics.csv
    │   ├── joint_velos.csv
    │   ├── joint_angles.csv
    │   └── landmarks.csv
    └── hitting/
        ├── metadata.csv
        ├── landmarks.csv
        ├── joint_angles.csv
        ├── joint_velos.csv
        ├── poi_metrics.csv
        └── hittrax.csv
```

| Local file | Official source |
|---|---|
| `data/raw/pitching/metadata.csv` | `baseball_pitching/data/metadata.csv` |
| `data/raw/pitching/poi_metrics.csv` | `baseball_pitching/data/poi/poi_metrics.csv` |
| `data/raw/pitching/joint_velos.csv` | Extract `pitching_joint_velos.zip` from Dataset v1 |
| `data/raw/pitching/joint_angles.csv` | Extract `pitching_joint_angles.zip` from Dataset v1 |
| `data/raw/pitching/landmarks.csv` | Extract `pitching_landmarks.zip` from Dataset v1 |
| `data/raw/hitting/metadata.csv` | `baseball_hitting/data/metadata.csv` |
| `data/raw/hitting/landmarks.csv` | Extract `hitting_landmarks.zip` from Dataset v1 |
| `data/raw/hitting/joint_angles.csv` | Extract `hitting_joint_angles.zip` from Dataset v1 |
| `data/raw/hitting/joint_velos.csv` | Extract `hitting_joint_velos.zip` from Dataset v1 |
| `data/raw/hitting/poi_metrics.csv` | `baseball_hitting/data/poi/poi_metrics.csv` |
| `data/raw/hitting/hittrax.csv` | `baseball_hitting/data/poi/hittrax.csv` |

The pitching and hitting files named `metadata.csv` and `landmarks.csv` are different datasets. Keep each file in its corresponding discipline folder.

The posture/contact study also uses the hitting POI and HitTrax tables. HitTrax `poi_z` is treated as a point-of-impact depth coordinate, not as hand depth.

The uprighting-velocity study uses the hitting joint-angle and joint-velocity tables. It differentiates filtered pelvis and torso X angles for posture-change rates and uses the official Z-axis angular velocities to locate axial-rotation peaks.

The pelvis–torso separation-timing study uses the hitting joint-angle and metadata tables. Its frame annotations identify rows in the sampled joint-angle CSV, not synchronized video frames.

The head-stability study additionally uses `hitting_c3d.zip` from Dataset v1, extracted under `data/raw/hitting/c3d/`. It reads four head markers and both wrist-marker pairs with `ezc3d`, and uses `landmarks.csv` for event times and wrist-trajectory validation. The notebook downloads these inputs automatically when absent, verifies official archive hashes, and excludes ambiguous joins. C3D filename swing numbers must not be used directly as processed swing IDs.

The first six studies do not require raw C3Ds. Hitting study 07 and pitching study 15 require the appropriate discipline-specific C3D archives. Study 07 does not require joint-angle or joint-velocity tables. None of the studies requires force-plate archives or media files.

## Data Relationships

- Pitching tables join on `session_pitch`.
- Hitting landmarks, POI, and HitTrax tables join on `session_swing`.
- Full-signal tables also use `time` for within-trial observations.

## Data Use

OpenBiomechanics data and biomechanics documentation have their own license and usage restrictions. Review the current [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md) before using or redistributing any data.

## Delivery Phase Decomposition

The phase-decomposition notebook also requires `data/raw/pitching/energy_flow.csv`,
extracted from the official `pitching_energy_flow.zip` Dataset v1 asset. It reads
joint angles, angular velocities, energy flow, metadata, and POI metrics, and
fetches missing files automatically. The three processed archives total about
115 MB and are verified against published SHA-256 hashes.

Events are `fp_10_time`, `fp_100_time`, `MER_time`, `BR_time`, and `MIR_time`.
Signal tables are validated independently and integrated on their own time grids.
Full-signal columns containing `energy_generated` and `energy_transfer` represent
power; their time integrals are energy estimates. Generation, absorption, and
transfer channels remain separate. Individual-pitch results and figures are
local outputs excluded from Git.

## Swing Phase Decomposition

Study 09 reads hitting `joint_angles.csv`, `joint_velos.csv`, `metadata.csv`, and
`poi_metrics.csv`. It automatically downloads missing Dataset v1 files and verifies
the two archive hashes (about 155 MB total). Existing CSVs are reused and hashed in
the run manifest. No C3D, landmark, force-plate, or HitTrax inputs are needed.

Official events are `fp_10_time`, `fp_100_time`, and `contact_time`. Full-signal
velocity columns use names such as `pelvis_angular_velocity_z`, rather than the
pitching table's `pelvis_velo_z`. Marker-derived inputs are sampled at 360 Hz.
Hitting knee/elbow extension is negative under the processed OBP conventions.

The primary outcome is POI `bat_speed_mph_contact_x`; `blast_bat_speed_mph_x`
and `exit_velo_mph_x` are modeled separately as secondary outcomes. Joins use
processed `session_swing` IDs with one-to-one validation. Bat kinematics are not
predictors. The early/late post-plant boundary is an analytical fraction of
plant-to-contact time, not an official swing-initiation event. Individual swing
results and figures are local outputs excluded from Git.

## Pelvis–Torso Uprighting Offset

Study 12 uses hitting `joint_angles.csv` and `metadata.csv`. Optional outcome analysis
uses `poi_metrics.csv`; the synchronized joint-center animation uses `landmarks.csv`.
No velocity archive, C3D, force-plate, or camera-video input is needed. Missing official
Dataset v1 files download automatically, and angle/landmark archive hashes are checked.
Set `MAKE_ANIMATION=False` to skip the landmark archive.

Pelvis X is posterior (+)/anterior (-) tilt; torso X is extension (+)/flexion (-).
The study compares first sustained threshold crossings with the final qualifying
positive-rate episode ending near contact. CSV sample rows are not video frames.
Raw data, individual derived tables, and animation HTML remain local and ignored.
See [the study guide](../docs/pelvis_torso_uprighting_offset.md).

## Attack Angle Repeatability

Study 13 uses only hitting `metadata.csv` and `poi_metrics.csv`, joining on `session_swing`. It reads the official `attack_angle_contact_x`, `bat_speed_mph_contact_x`, and `exit_velo_mph_x` POI fields. No C3D or full-signal archive is required. Missing Dataset v1 CSVs download automatically; existing files are reused and their SHA-256 hashes are recorded. The notebook summarizes variability within sessions, compares playing levels, and runs whole-hitter omission checks. See [the study guide](../docs/swing_plane_consistency.md).

## Head & Trunk Stability and Release Consistency (Study 15)

Study 15 reads pitching `metadata.csv`, `poi_metrics.csv`, `joint_angles.csv`, and `landmarks.csv`, plus the `pitching_c3d.zip` Dataset v1 asset. It can download missing official inputs automatically (set `AUTO_DOWNLOAD=False` for local-only runs), verifies the official archive SHA-256 digests, and extracts C3D files under `data/raw/pitching/c3d/`. C3D downloads can be large. Raw files are not committed.

Each C3D is joined through the **exact** `metadata.filename_new` field and checked against the processed trial's time grid; C3D filename pitch numbers must not be interpreted as the processed `session_pitch` suffix. The analysis uses `BR_time` to interpolate release values and align the final 100 ms of movement. Head translation is the four-marker `LFHD/RFHD/LBHD/RBHD` centroid. The pelvis reference is the `LASI/RASI/LPSI/RPSI` marker centroid, not an anatomical pelvis center. Trunk angles use `torso_angle_x/y/z` from processed joint angles.

The primary outcome is sample-SD-based RMS dispersion of **hand joint-center** positions in global lateral/vertical coordinates (Y/Z), *not tracked baseball release location or command*. The diagnostic examines both global and pelvis-relative head/hand positions, lateral and vertical components separately, fixed cohort comparisons, pitcher-held-out prediction, and leave-one-pitcher-out influence. Subtracting the same pelvis reference from head and hand can introduce mathematical coupling. Minimum complete trial count is four pitches per session, with three- and five-pitch sensitivity checks.

Run the notebook at `notebooks/pitching/15_head_trunk_release_consistency.ipynb`. Generated CSVs, run manifests, and audit files go to `results/head_trunk_release_consistency/`, with figures under `figures/head_trunk_release_consistency/`; both are ignored by Git. See [the study guide](../docs/head_trunk_release_consistency.md) for reproducibility and interpretation.

## Individual Swing Consistency Profiles (Study 16)

Study 16 uses hitting `joint_angles.csv` and `metadata.csv`, with optional `poi_metrics.csv` for bat-speed and exit-velocity context. It reads `pelvis_angle_x/z` and `torso_angle_x/z`, joins on unique `session_swing` IDs, and groups by hitter, session, and batting side. Events are `fp_10_time`, `fp_100_time`, and `contact_time`. All phases and angle channels require complete coverage and chronological annotations.

Missing Dataset v1 files download automatically; the joint-angle archive is verified against its expected SHA-256 and reused CSV hashes are recorded. No C3D, landmarks, velocity, force-plate, or video input is needed. The duration audit preserves primary annotations and exports separate screened cohorts and session eligibility. Generated CSVs, curves, HTML, and audit outputs stay under `results/individual_swing_fingerprints/`, with plots under `figures/individual_swing_fingerprints/`; both are ignored. See [the study guide](../docs/individual_swing_fingerprints.md).

## Lead-Hand Path Shape (Study 17)

Study 17 uses hitting `landmarks.csv` and `metadata.csv`, with optional `poi_metrics.csv`. It selects the anatomical lead wrist (`lwjc` for right-handed hitters; `rwjc` for left-handed hitters), retains global and moving-hip-midpoint-relative trajectories, and mirrors left-handed Y for display and sweep. Processed coordinates are metres with X toward the pitcher, Y toward the right-handed box, and Z upward. The hip reference is the midpoint of `left_hip` and `right_hip`. `lhjc/rhjc` are used in a separate landmark-choice sensitivity.

Primary windows are ordered foot plant to contact and the independent fixed final 100 ms. Missing or disordered foot events do not invalidate a fixed contact window. Missing official inputs download automatically; the roughly 66 MB `hitting_landmarks.zip` is SHA-256 checked before extraction. No C3D or angle/velocity archive is required. Additional filtering uses precontact signals with reflection at contact; no later follow-through is used beyond possible endpoint interpolation between bracketing samples. Input hashes and settings are recorded.

Run All writes per-swing measurements, eligibility and duration audits, session profiles, matched filter/window/landmark sensitivities, an HTML profile selector, and figures under the ignored `results/lead_hand_path_shape/` and `figures/lead_hand_path_shape/` directories. See [the study guide](../docs/lead_hand_path_shape.md). The wrist/hand-center proxy must not be interpreted as barrel trajectory or bat attack angle.
