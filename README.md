# Baseball Biomechanics Analysis

This repository contains five applied baseball biomechanics studies built with Python and Driveline Baseball's public [OpenBiomechanics Project](https://github.com/drivelineresearch/openbiomechanics). The analyses examine pitching sequencing, pitching release consistency, hitting posture, contact-point consistency, and the timing of posture change relative to rotation using processed motion-capture and point-of-impact data.

The purpose of the project is to turn biomechanical time-series data into interpretable measures that can support player evaluation, research, and player-development conversations.

## Projects

| Study | Research question | Primary data | Notebook |
|---|---|---|---|
| Kinematic Sequencing and Velocity | Do segment timing and sequencing efficiency differ between higher- and lower-velocity pitchers? | Pitching joint angular velocities, POI metrics, and metadata | [View notebook](notebooks/pitching/01_kinematic_sequencing.ipynb) |
| Trunk Stability and Release Consistency | Is greater trunk-angle variability at ball release associated with greater release-point dispersion? | Pitching joint angles, landmarks, and metadata | [View notebook](notebooks/pitching/02_trunk_stability_release.ipynb) |
| Hinge Integrity During the Stride | How much does the upper-body-to-thigh hinge angle change from pre-stride through front-foot plant? | Hitting landmarks and metadata | [View notebook](notebooks/hitting/03_hinge_integrity.ipynb) |
| Posture Loss and Contact-Point Consistency | Is greater post-plant posture loss associated with more variable hand position and HitTrax point-of-impact depth at contact? | Hitting landmarks, POI metrics, and HitTrax data | [View notebook](notebooks/hitting/04_posture_contact_consistency.ipynb) |
| Uprighting Velocity and Rotational Timing | How quickly do hitters change torso and pelvis posture after foot plant, and when do those peaks occur relative to axial rotation? | Hitting joint angles, joint angular velocities, POI metrics, and metadata | [View notebook](notebooks/hitting/05_uprighting_velocity.ipynb) |

## Key Findings

### 1. Kinematic Sequencing and Velocity

- The higher-velocity group averaged a 21.56 ms pelvis-to-torso delay, compared with 19.36 ms for the lower-velocity group.
- Sequencing efficiency averaged 2.858 in the higher-velocity group and 2.809 in the lower-velocity group.
- Pitcher-level velocity was not significantly related to pelvis-to-torso delay (`r = 0.033`, `p = 0.5998`) or sequencing efficiency (`r = 0.104`, `p = 0.0930`).
- The analysis retains pitches whose detected peaks occur in pelvis-torso-arm order. Results therefore describe timing within correctly ordered sequences rather than the prevalence of sequencing breakdowns.

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

## Repository Structure

```text
baseball-biomechanics-analysis/
├── notebooks/
│   ├── pitching/
│   │   ├── 01_kinematic_sequencing.ipynb
│   │   └── 02_trunk_stability_release.ipynb
│   └── hitting/
│       ├── 03_hinge_integrity.ipynb
│       ├── 04_posture_contact_consistency.ipynb
│       └── 05_uprighting_velocity.ipynb
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

Run the notebooks in numerical order. Each notebook contains executed outputs and the complete reproducible workflow. Raw data are not committed; the hitting notebooks download missing official Dataset v1 inputs when run locally.

## Methods and Interpretation

The notebooks use event-based filtering, interpolation or temporal normalization, athlete/session aggregation, descriptive statistics, correlation analysis, regression, sensitivity testing, and bootstrap uncertainty estimates. These are observational analyses of the available OBP sample. Their findings identify associations and sample-level tendencies, not causal mechanical prescriptions for individual athletes.

## Data Source and License

Data come from Driveline Baseball's [OpenBiomechanics Project](https://github.com/drivelineresearch/openbiomechanics). The source project distributes code and data under separate licenses. Anyone reproducing these analyses should review the current [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md) and citation guidance before using the dataset.

No OpenBiomechanics raw data are redistributed in this repository.

## Author

Brendan Driscoll  
[GitHub](https://github.com/bdrisc)
