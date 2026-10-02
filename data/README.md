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

The first six studies do not require raw C3Ds. The head-stability study does not require joint-angle or joint-velocity tables. None of the nine notebooks requires force-plate archives or media files.

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
