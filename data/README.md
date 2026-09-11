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
        └── landmarks.csv
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

The pitching and hitting files named `metadata.csv` and `landmarks.csv` are different datasets. Keep each file in its corresponding discipline folder.

The raw C3D archives, force-plate tables, media files, and other full-signal tables are not required for these three notebooks.

## Data Relationships

- Pitching tables join on `session_pitch`.
- Hitting tables join on `session_swing`.
- Full-signal tables also use `time` for within-trial observations.

## Data Use

OpenBiomechanics data and biomechanics documentation have their own license and usage restrictions. Review the current [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md) before using or redistributing any data.
