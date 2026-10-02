# Head Movement, Repeatability & Batted-Ball Outcomes

## Run

Install the repository requirements and run every cell of
`notebooks/hitting/07_head_stability_contact_quality.ipynb` in order. The notebook
contains code cells only and does not depend on a separate project module.
It can run inside the repository or independently, using the current working
directory when no repository root is found.

For a standalone installation:

```powershell
python -m pip install numpy pandas scipy matplotlib ezc3d statsmodels ipykernel
```

The first run downloads about 498 MB of official Dataset v1 C3D and landmark
archives, plus small metadata, POI, and HitTrax CSVs. Archives are checked against
their published SHA-256 digests. Later runs reuse local inputs. Set
`AUTO_DOWNLOAD=False` to require existing files. Raw inputs are excluded from Git.

## Trial identity and time alignment

The filename swing number is not a reliable processed swing ID. Some original
assessment swings are absent from the processed tables, so the numbering can
differ. The notebook restricts candidates to the same athlete, session, and
handedness; requires equal sample counts and a matching 360 Hz relative time
grid; then compares both C3D wrist-marker midpoints with the processed wrist
centers. It accepts an RMS coordinate error below 5 mm only when there is no
similarly close alternative. These midpoints are a matching reference, not a
new wrist-center model. Duplicate matches fail explicitly. Static calibration
files and unmatched trials are listed separately.

In the released sample, C3D point arrays and processed landmark arrays use
the same recording-relative sample origin. Matching the wrist trajectories
checks that origin directly; the C3D header's first-frame value is recorded
for inspection rather than silently added as a time offset.

## Measurements

The centroid of `LFHD`, `RFHD`, `LBHD`, and `RBHD` approximates head translation.
It is not an anatomical head center, eye position, or head orientation.

| Metric | Definition |
|---|---|
| Directional range | Maximum minus minimum centroid coordinate within the window |
| Net displacement | Coordinate at window end minus coordinate at window start |
| Maximum displacement | Greatest Euclidean distance from the centroid at window start |
| Height-normalized movement | Movement in centimeters divided by height in meters, giving percentage points of height |
| Trajectory repeatability | Root mean sample variance across all three axes, averaged over 101 foot-plant-to-contact samples |
| Contact dispersion | Root sum of sample variances of head displacement at contact |

Windows are foot plant through contact and the final 100 ms before contact.
The latter can begin before foot plant. Curves are anchored at each swing's
foot-plant head position, so repeatability reflects movement patterns rather
than absolute stance position. X points toward the pitcher; Z points upward;
Y is mirrored for left-handed swings for cross-hitter comparisons.

## Quality checks

- Missing/negative-residual head-marker samples and zero-coordinate samples
  are invalid. Only bounded gaps of at most three frames are interpolated.
- Missing/inconsistent events, events outside the recording, and plant-to-contact
  durations outside 40–400 ms are excluded.
- Filtering requires recording margins before and after the analysis windows.
  A fourth-order zero-phase Butterworth filter is applied to centroid position.
- Trials with more than 30 mm change in any head-marker pair distance in the
  filtering window are excluded as a tracking-quality screen. That screen is a
  pragmatic threshold, not a validated biological cutoff.
- Movement is recomputed at 8, 12, and 16 Hz. Primary results use 12 Hz.

## Statistical questions

The primary outcome is measured exit velocity. The primary predictor is maximum
head displacement from foot plant through contact, normalized by height. The
model centers all variables within athlete-session and includes bat speed at
contact. This estimates a within-session conditional association, without
claiming a causal effect or a direct measure of contact efficiency.

An additional model includes machine-pitch speed and horizontal/vertical pitch
location, using only complete paired observations. Bat speed as an outcome and
late vertical movement as a predictor are exploratory comparisons. The notebook
does not merge missing Blast values into motion-capture bat speed measurements.

Within-session models require at least five complete swings and 15 athletes.
Standard errors cluster by athlete and account for absorbed session effects in
the finite-sample correction. The notebook also resamples whole athletes 1,000
times for percentile bootstrap intervals. Session-level repeatability analyses
use Spearman correlations and athlete bootstrap intervals. Outcome dispersion
is calculated only when enough observed outcomes are present; four-, five-, and
six-swing minimums are compared. Other comparisons are exploratory, with
unadjusted p-values explicitly identified.

## Initial Dataset v1 results

The pipeline matched 669 C3D trials and retained 624 swings from 96 athletes.
At the primary cutoff, 25 processed trials lacked events/height, 18 failed event
order/range/duration checks, eight had no validated C3D match, and two failed the
head-marker distance screen.

The primary model used 581 swings from 83 athlete-sessions. Its coefficient was
+0.12 mph per additional percentage point of height in head displacement,
with a bootstrap 95% interval from -0.26 to +0.49 mph. The pitch/location-adjusted
estimate was approximately zero, with an interval from -0.41 to +0.42 mph.

Trajectory variability and exit-velocity SD had a weak association
(`rho = 0.138`, interval -0.092 to +0.355). An exploratory association with
contact-depth SD was positive (`rho = 0.261`, interval +0.034 to +0.459), but
contact depth also varies with pitch location. Neither analysis establishes an
ideal amount of head movement. A large movement can still be repeatable.

These machine-pitch assessments do not validate a game-performance prediction
or a coaching intervention. Small swing counts make individual session
variability estimates uncertain.

## Outputs

The notebook writes CSVs to `results/head_stability/`: C3D matching and extraction
audits, swing metrics, session summaries, within-session models, repeatability
associations, and filter sensitivity. A JSON manifest records parameters,
input CSV hashes, archive hashes, and interpretation limits.

Three PNGs under `figures/head_stability/` show an example swing, session
trajectory overlays, and outcome associations. Generated tables and figures
are local outputs excluded from Git. Change `SELECTED_SESSION` to inspect a
retained athlete-session; its identifier is listed in `session_summary.csv`.

## Validation and source

Run `python -m unittest discover -s tests -v`. Synthetic checks cover unit
conversion in displacement, window definitions, short-gap handling, ambiguous
trial matching, session centering, and insufficient repeatability samples.
The complete notebook was also run against official Dataset v1 data and all
three generated figures were visually inspected.

Source: [Driveline Baseball OpenBiomechanics Project](https://github.com/drivelineresearch/openbiomechanics).
Review the [OBP data license](https://github.com/drivelineresearch/openbiomechanics/blob/main/LICENSE-DATA.md)
before using or distributing data or derived data outputs. Raw data are not
redistributed here.
