# Data Format

CSV files are written by [eic2ai](https://github.com/sroai/eic2ai), a single-pass
C++ converter that reads an eicrecon file (`.edm4eic.root`) and, when a role needs
it, the paired npsim file (`.edm4hep.root`) once, and writes one CSV per **role**.
The rows are identical to those of the older `csv_convert/` ROOT macros (except
the shared Λ decay codes and the added `truth_*` block of `reco_dis`); the column
names follow one shared vocabulary (below).

`eic2ai --list-columns` prints the header of every role, `eic2ai --list-writers`
the collections each role reads. [CSV Schema](./csv-schema) shows every file and
column, and which columns point into which file.

## Files

```
<stem>.<role>.csv.zip     default: one deflate ZIP64 entry named <stem>.<role>.csv
<stem>.<role>.csv         --compress none
<stem>.<role>.csv.gz      --compress gz
```

`<stem>` is the reco file name without `.eicrecon.edm4eic.root` or `.edm4eic.root`
(the sim file name without `.edm4hep.root` in sim-only runs), so
`k_lambda_18x275_5000evt_0022.edm4eic.root` gives
`k_lambda_18x275_5000evt_0022.trk_hits.csv.zip`. pandas reads the zip directly.

A role whose writer fails leaves no file; a file that exists is complete.

## Column vocabulary

Every column is `<prefix>_<quantity>`, and `evt` (the entry counter of the input
file) is the join key of every role.

| Prefix | Object |
| ------ | ------ |
| `prt` | the MC particle behind a hit, cluster or row |
| `trk_hit` | reconstructed tracker hit |
| `cal_hit` | digitized calorimeter hit |
| `clu` | calorimeter cluster |
| `rec` | reconstructed particle |
| `sim` | simulation truth aggregated over a calorimeter cell |

Units: GeV, GeV/c, mm, ns, rad, charge in e.

### Signal or background: `prt_origin`

| Value | Meaning |
| ----- | ------- |
| `0` | unknown |
| `1` | signal particle from the generator |
| `2` | Geant4 secondary of a signal particle |
| `3` | background particle from the generator |
| `4` | Geant4 secondary of a background particle |

The background merger adds a source-specific offset (a multiple of 1000, see
[Backgrounds](/ai-epic-background/background)) to the generator status of
background particles before Geant4 runs. Generator particles are classified by
`prt_gen_status` (`1` or `2` signal, `>= 1000` background); Geant4 secondaries
(`prt_gen_status = 0`) take the class of their first generator ancestor up the
parent chain.

## Roles

Every column of every role, with its meaning and unit, is on the [CSV Schema](./csv-schema) page. That page
is generated from one list, which the eic2ai CI checks against the columns eic2ai writes.

| Role | One row per | Needs |
| ---- | ----------- | ----- |
| [`trk_hits`](#trk-hits) | reconstructed tracker hit, with its MC particle | reco |
| [`cal_hits`](#cal-hits) | digitized calorimeter hit, truth-labeled from the sim cell | reco + sim |
| [`calo_clusters`](#calo-clusters) | cluster ↔ MC particle association | reco |
| [`mc_particles`](#mc-particles) | MC particle | reco |
| [`reco_particles`](#reco-particles) | reconstructed particle | reco |
| [`mc_dis`](#mc-dis) | event: generator DIS kinematics | reco |
| [`event_index`](#event-index) | processed event | any |
| [`reco_dis`](./csv-schema#reco_dis) | event: reconstructed DIS kinematics by seven methods, with truth | reco |
| `mcpart_lambda`, `lambda_acceptance`, `reco_ff_lambda`, `acceptance_ppim`, `acceptance_npi0`, `combinatorics_ppim`, `comb_candidates` | Λ analysis tables | reco or sim |

The Λ and DIS roles serve the [Meson Structure](https://jeffersonlab.github.io/meson-structure/)
analyses; the [CSV Schema](./csv-schema#mcpart_lambda) page lists their columns.

## `trk_hits` {#trk-hits}

One row per tracker hit association (raw hit → sim hit → MC particle), joined
with the reconstructed hit. Hits from these association collections:

```
B0TrackerRawHitAssociations            OuterMPGDBarrelRawHitAssociations
BackwardMPGDEndcapRawHitAssociations   RICHEndcapNRawHitsAssociations
ForwardMPGDEndcapRawHitAssociations    SiBarrelRawHitAssociations
ForwardOffMTrackerRawHitAssociations   SiBarrelVertexRawHitAssociations
ForwardRomanPotRawHitAssociations      SiEndcapTrackerRawHitAssociations
MPGDBarrelRawHitAssociations           TOFBarrelRawHitAssociations
TOFEndcapRawHitAssociations
```

Columns: [CSV Schema → `trk_hits`](./csv-schema#trk_hits).

## `cal_hits` {#cal-hits}

One row per digitized calorimeter hit. The reco file has no calorimeter hit ↔
particle association, so each hit is matched by `(evt, cellID)` to the sim hit
of the same cell in the paired `.edm4hep.root` file. A cell with several
contributing particles gets the `prt_origin` of the energy-majority class,
`label_purity` = that class's energy fraction, and the `prt_*` block of the
largest contributor of that class. A hit whose cell has no sim hit keeps its
features with `prt_origin = 0` and zeros in the `prt_*` block.

Calorimeters: `EcalBarrelScFiRecHits`, `EcalBarrelImagingRecHits`,
`EcalEndcapNRecHits`, `EcalEndcapPRecHits`, `HcalBarrelRecHits`,
`HcalEndcapNRecHits`, `HcalEndcapPInsertRecHits`, `LFHCALRecHits`,
`B0ECalRecHits`, `EcalFarForwardZDCRecHits`, `HcalFarForwardZDCRecHits`.

The `cal_hit_*` columns are the detector-level features; `sim_*`, `n_contrib`,
`label_purity` and `prt_*` are truth. Columns: [CSV Schema → `cal_hits`](./csv-schema#cal_hits).

## `calo_clusters` {#calo-clusters}

One row per cluster ↔ MC particle association, from a fixed list of 27
`*ClusterAssociations` collections (regular, truth and split-merge clusters of the
ECAL, HCAL, B0, ZDC and luminosity calorimeters); collections absent from a file
are skipped. Columns: [CSV Schema → `calo_clusters`](./csv-schema#calo_clusters).

## `mc_particles` {#mc-particles}

One row per particle of `MCParticles`. `prt_index` here is the same index as
`prt_index` in `trk_hits` and `calo_clusters` (both read the reco file's
`MCParticles`), so `(evt, prt_index)` joins a hit or cluster to its full particle
record. Columns: [CSV Schema → `mc_particles`](./csv-schema#mc_particles).

## `reco_particles` {#reco-particles}

One row per `ReconstructedParticles` entry, with the sizes of its relations
(clusters, tracks, daughters, PID hypotheses, and the hits behind them).
Columns: [CSV Schema → `reco_particles`](./csv-schema#reco_particles).

## `mc_dis` {#mc-dis}

One row per event with the generator's DIS kinematics, read from the event
parameters `dis_<name>` that the generator writes; the columns keep the
generator's names. A missing parameter leaves an empty field.
Columns: [CSV Schema → `mc_dis`](./csv-schema#mc_dis).

## `event_index` {#event-index}

One row per processed event: `evt`, `event_number` (from `EventHeader`),
`reco_collections`, `sim_collections` (collections in each frame, 0 without that
file). Its row count is the event count of a complete conversion.

## Loading the CSV

```python
import pandas as pd

hits = pd.read_csv("k_lambda_18x275_5000evt_0022.trk_hits.csv.zip")

event_0 = hits[hits["evt"] == 0]
primaries = hits[hits["prt_gen_status"] == 1]

signal = hits[hits["prt_origin"].isin([1, 2])]
background = hits[hits["prt_origin"].isin([3, 4])]

hits_per_system = hits.groupby("trk_hit_system_name").size()

# Full particle record of each hit
particles = pd.read_csv("k_lambda_18x275_5000evt_0022.mc_particles.csv.zip")
hits = hits.merge(particles[["evt", "prt_index", "prt_sim_status", "prt_parent_index"]],
                  on=["evt", "prt_index"])
```

Files written by the macros before the column unification use older names
(`prt_status`, `rec_collection`, `event`, …). `eic2ai/column_renames.py` holds
the old → new table per role; `rename_dataframe(df, role)` renames a loaded file.
