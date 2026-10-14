# Data Format

CSV is produced by the [converter macros](/csv-convert) in `csv_convert/`, one
per *role*. Each converter has its own column layout; there is no single shared
schema. Files are named `<input-stem>.<role>.csv` (e.g.
`msf_9x130_0001.trk_hits.csv`), so the role in the filename tells you which
layout to expect.

This page documents the **`edm4eic_trk_hits`** converter in full, as the worked
example — it is the richest per-hit dump and the one the background plots use.
The other converters follow the same conventions (leading `evt` index,
`prt_*` truth columns, SI units); read their `.cxx` headers in `csv_convert/`
for the exact columns.

## `trk_hits` — one row per tracker-hit association

Each row joins three things:

- the reconstructed tracker hit (`edm4eic::TrackerHit`),
- the underlying simulation hit (`edm4hep::SimTrackerHit`),
- the `MCParticle` that produced the simulation hit.

This makes every row self-contained: it carries enough truth and reconstructed
information to be used standalone for analysis or ML training. The header is
written by `HitRecord::make_csv_header()` in `csv_convert/edm4eic_trk_hits.cxx`.

### Event and indexing

| Column      | Type   | Description                                         |
| ----------- | ------ | --------------------------------------------------- |
| `evt`       | uint64 | Event number within the run                         |
| `hit_index` | uint64 | Index of the hit-association in its collection      |
| `prt_index` | uint64 | Index of the `MCParticle` that produced the sim hit |

### Particle identification & kinematics

| Column        | Unit  | Description                                                      |
| ------------- | ----- | ---------------------------------------------------------------- |
| `prt_pdg`     | —     | PDG code (e.g. `11` = e⁻, `211` = π⁺, `2212` = proton)           |
| `prt_gen_status`  | —     | Generator status: `1` = primary from generator, `0` = G4-created |
| `prt_origin`  | —     | Provenance: `0` unknown, `1` signal, `2` G4-gen from signal, `3` background, `4` G4-gen from background |
| `prt_energy`  | GeV   | Total energy                                                     |
| `prt_charge`  | e     | Electric charge                                                  |
| `prt_mom_x/y/z` | GeV/c | Momentum components                                            |

> `prt_origin` is the key column for background studies: it separates
> signal-derived hits from the mixed-in background cocktail.

### Particle vertex (production point)

| Column                     | Unit | Description                |
| -------------------------- | ---- | -------------------------- |
| `prt_vtx_time`             | ns   | Time at production vertex  |
| `prt_vtx_pos_x/y/z`        | mm   | Vertex position components |

### Particle endpoint (decay / absorption)

| Column                     | Unit | Description                                                    |
| -------------------------- | ---- | -------------------------------------------------------------- |
| `prt_end_time`             | ns   | Time at endpoint (currently mirrors `prt_vtx_time` in EDM4hep) |
| `prt_end_pos_x/y/z`        | mm   | Endpoint position components                                   |

### Tracker hit detector info

| Column               | Type   | Description                                            |
| -------------------- | ------ | ------------------------------------------------------ |
| `trk_hit_cell_id`    | uint64 | Full cell ID (encodes the detector hierarchy)          |
| `trk_hit_system_id`  | uint64 | Detector system ID (low byte of `cell_id`)             |
| `trk_hit_system_name`| string | Human-readable detector name (e.g. `SiBarrelVertex`)   |

### Tracker hit position, time, and uncertainties

| Column                                             | Unit  | Description                            |
| -------------------------------------------------- | ----- | -------------------------------------- |
| `trk_hit_pos_x/y/z`                                | mm    | Reconstructed hit position             |
| `trk_hit_time`                                     | ns    | Reconstructed hit time                 |
| `trk_hit_pos_err_xx`, `trk_hit_pos_err_yy`, `trk_hit_pos_err_zz` | mm² | Diagonal of the position covariance |
| `trk_hit_time_err`                                 | ns    | Time uncertainty                       |
| `trk_hit_edep`                                     | GeV   | Energy deposited in the sensor         |
| `trk_hit_edep_err`                                 | GeV   | Energy-deposition uncertainty          |

## Detector coverage

`edm4eic_trk_hits` iterates over all standard ePIC tracker hit-association
collections:

```
B0TrackerRawHitAssociations           ForwardOffMTrackerRawHitAssociations
BackwardMPGDEndcapRawHitAssociations   ForwardRomanPotRawHitAssociations
ForwardMPGDEndcapRawHitAssociations    MPGDBarrelRawHitAssociations
OuterMPGDBarrelRawHitAssociations      RICHEndcapNRawHitsAssociations
SiBarrelRawHitAssociations             SiBarrelVertexRawHitAssociations
SiEndcapTrackerRawHitAssociations      TOFBarrelRawHitAssociations
TOFEndcapRawHitAssociations
```

Calorimeter associations are handled by a **separate** converter,
`edm4eic_calo_clusters.cxx` (one row per cluster↔MCParticle association), rather
than being written into the tracker-hit CSV.

## Loading the CSV

```python
import pandas as pd

df = pd.read_csv("msf_9x130_0001.trk_hits.csv")
print(df.shape, df.columns.tolist()[:6])

# Filter one event
event_0 = df[df["evt"] == 0]

# Keep only primary particles
primaries = df[df["prt_gen_status"] == 1]

# Signal-only vs background hits
signal = df[df["prt_origin"].isin([1, 2])]
background = df[df["prt_origin"].isin([3, 4])]

# Group by detector system
hits_per_system = df.groupby("trk_hit_system_name").size()
```

For visualisation of a single event, see
`analyses/time-vs-z-plots/background_analysis.py`, which produces `time vs z`
scatter plots colored by `prt_gen_status`.
